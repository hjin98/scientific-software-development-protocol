#!/usr/bin/env python3
"""Trusted provider-control / observation principal (Stage F SSDP 7.0, OMP profile).

One of the three accepted D3 principals. It

* owns the provider credential (received once on a launch descriptor after its route and privilege boundary are locked down; never written anywhere),
* owns the only route to the model provider (`--upstream`),
* sits ON the actual OMP inference request path: the subject reaches the model only through
  this process, over the descriptor pair it inherited (see muxhttp70.py), so there is no
  socket, port or token in the subject's reach and the transport is not a path a subject
  process can open on its own,
* serves exactly one operation, `POST <allowed path>` (single-purpose inference transport):
  anything else is refused and recorded, so it is not usable as a generic proxy,
* forwards the request body byte-for-byte (it may record and verify, never add, remove,
  rewrite or reorder prompt/catalog/tool material) and swaps only the placeholder key for the
  real credential,
* emits raw, hash-linked evidence (complete request body, upstream status, complete response
  body up to a bound, refused attempts) to a supervisor-owned descriptor, and receives no
  custody material, mediator backing state or supervisor filesystem authority: its only inputs
  are its descriptors, its config flags and one credential variable.

Derived facts (model, tools, catalog, ...) are computed later by the supervisor-side adapter
from the raw record; this process deliberately stays small and does not interpret the prompt.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import http.client
import ipaddress
import os
import signal
import socket
import ssl
import struct
import sys
import threading
from typing import Any
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence70  # noqa: E402
import muxhttp70 as mux  # noqa: E402
import seccomp70  # noqa: E402

RESPONSE_EVIDENCE_LIMIT = 4 * 1024 * 1024
OBSERVER_CA_FILE = "/etc/ssl/certs/ca-certificates.crt"
HOP_BY_HOP = {
    "host", "connection", "content-length", "transfer-encoding", "keep-alive", "te", "trailer",
    "upgrade", "proxy-authorization", "proxy-connection", "authorization", "accept-encoding",
}
OBSERVER_ID = "ssdp70-provider-observer-v1"


class Observer:
    def __init__(self, chain: evidence70.ChainWriter, upstream: str, credential: str | None,
                 upstream_connection: http.client.HTTPConnection, placeholder: str, allowed_path: str,
                 blocked_discovery_target: str, upstream_timeout: float, max_requests: int | None = None):
        self.chain = chain
        self.upstream = urlsplit(upstream)
        self.credential = credential
        self.placeholder = placeholder
        self.allowed_path = allowed_path
        self.blocked_discovery_target = blocked_discovery_target
        self.upstream_timeout = upstream_timeout
        self.max_requests = max_requests
        self.upstream_connection = upstream_connection
        self.lock = threading.Lock()
        self.upstream_lock = threading.Lock()
        self.request_count = 0
        self.refused_count = 0
        self.provider_discovery_blocked_count = 0

    def next_index(self) -> int:
        with self.lock:
            index = self.request_count
            self.request_count += 1
            return index

    def refuse(self, conn: mux.Conn, status: int, reason: str, **extra: Any) -> None:
        with self.lock:
            self.refused_count += 1
        self.chain.append("refused", {"reason": reason, **extra})
        mux.send_simple(conn, status)
        conn.close()

    def serve(self, conn: mux.Conn) -> None:
        try:
            request = mux.read_request(conn)
            if request is None:
                self.refuse(conn, 400, "malformed-request")
                return
            if (request.method == "GET" and request.target == self.blocked_discovery_target
                    and request.body == b""):
                # OMP 18.0.11 performs this provider-catalog metadata probe against its configured
                # base URL. The frozen qualification profile must not consume dynamic provider
                # catalog state, so preserve the build's observed denial response while recording
                # the exact operation as B3 evidence. No provider request is emitted here.
                with self.lock:
                    self.provider_discovery_blocked_count += 1
                self.chain.append("provider_discovery_blocked", {
                    "method": request.method,
                    "path": request.target,
                    "body_bytes": 0,
                    "provider_egress": False,
                    "response_status": 405,
                    "classification": "frozen-provider-catalog-discovery-disabled",
                })
                mux.send_simple(conn, 405)
                return
            if request.method != "POST" or request.path != self.allowed_path:
                self.refuse(conn, 404 if request.method == "POST" else 405,
                            "not-the-single-inference-operation", method=request.method, path=request.target)
                return
            self.forward(conn, request)
        except Exception as exc:  # never crash the principal on subject-controlled input
            try:
                self.chain.append("refused", {"reason": f"handler-error:{type(exc).__name__}"})
            except RuntimeError:
                pass
        finally:
            conn.close()

    def forward(self, conn: mux.Conn, request: mux.Request) -> None:
        with self.upstream_lock:
            self._forward_serial(conn, request)

    def _forward_serial(self, conn: mux.Conn, request: mux.Request) -> None:
        body = request.body
        index = self.next_index()
        inbound_auth = request.headers.get("authorization")
        headers = {name: value for name, value in request.headers.items() if name != "authorization"}
        self.chain.append("request", {
            "request_index": index,
            "method": request.method,
            "path": request.target,
            "headers": headers,
            "inbound_authorization": {
                "present": inbound_auth is not None,
                "matches_placeholder": inbound_auth == f"Bearer {self.placeholder}",
            },
            "body_bytes": len(body),
            "body_sha256": hashlib.sha256(body).hexdigest(),
            "body_b64": base64.b64encode(body).decode("ascii"),
        })
        if self.max_requests is not None and index >= self.max_requests:
            # Supervisor-set turn budget enforced on the actual inference path: the request is
            # retained as evidence but never reaches the provider.
            self.chain.append("budget_exhausted", {"request_index": index, "max_requests": self.max_requests})
            # 403 (not 429): a non-retryable client error, so neither OMP nor its provider layer retries it.
            mux.send_simple(conn, 403, b'{"error":{"message":"qualification turn budget exhausted","type":"turn_budget"}}',
                            "application/json")
            return
        forward = {k: v for k, v in request.headers.items() if k not in HOP_BY_HOP}
        forward["content-length"] = str(len(body))
        if self.credential is not None:
            forward["authorization"] = f"Bearer {self.credential}"
        captured = bytearray()
        total = 0
        digest = hashlib.sha256()
        status = None
        resp_headers: dict[str, str] = {}
        error = None
        try:
            upstream = self.upstream_connection
            upstream.request("POST", self.upstream.path.rstrip("/") + request.target, body=body, headers=forward)
            resp = upstream.getresponse()
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.getheaders()
                            if k.lower() in ("content-type", "retry-after", "x-request-id")}
            mux.send_head(conn, status, resp_headers, None)
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                digest.update(chunk)
                total += len(chunk)
                if len(captured) < RESPONSE_EVIDENCE_LIMIT:
                    captured.extend(chunk[: RESPONSE_EVIDENCE_LIMIT - len(captured)])
                conn.sendall(chunk)
        except Exception as exc:  # upstream failure is evidence, not a crash
            error = f"{type(exc).__name__}: {exc}"
            if status is None:
                mux.send_simple(conn, 502)
        self.chain.append("response", {
            "request_index": index,
            "upstream_status": status,
            "headers": resp_headers,
            "body_bytes": total,
            "body_sha256": digest.hexdigest(),
            "body_b64": base64.b64encode(bytes(captured)).decode("ascii"),
            "body_truncated_in_evidence": total > len(captured),
            "error": error,
        })


def _open_frozen_route(upstream: str, timeout: float) -> tuple[http.client.HTTPConnection, list[str]]:
    parsed = urlsplit(upstream)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise RuntimeError("frozen provider route is not a simple HTTP(S) origin")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    addresses = socket.getaddrinfo(parsed.hostname, port, type=socket.SOCK_STREAM)
    peers: list[str] = []
    connected: socket.socket | None = None
    errors: list[str] = []
    for family, socktype, proto, _canonname, sockaddr in addresses:
        candidate: socket.socket | None = None
        try:
            candidate = socket.socket(family, socktype, proto)
            candidate.settimeout(timeout)
            candidate.connect(sockaddr)
            connected = candidate
            peers.append(str(sockaddr[0]))
            break
        except OSError as exc:
            errors.append(f"{type(exc).__name__}:{exc.errno}")
            if candidate is not None:
                candidate.close()
    if connected is None:
        raise RuntimeError("frozen provider route connection failed: " + ",".join(errors))
    connection = http.client.HTTPConnection(parsed.hostname, port, timeout=timeout)
    connection.sock = connected
    connection.auto_open = 0
    connection._ssdp_https = parsed.scheme == "https"
    return connection, peers


def _complete_tls_handshake(connection: http.client.HTTPConnection) -> None:
    parsed_host = connection.host
    if getattr(connection, "_ssdp_https", False):
        # The observer runs in a deliberately minimal filesystem that stages the reviewed
        # system CA bundle at this exact path. Do not rely on OpenSSL's compiled default
        # compatibility paths (for example /usr/lib/ssl/cert.pem), which are intentionally
        # absent from the observer sandbox.
        context = ssl.create_default_context(cafile=OBSERVER_CA_FILE)
        assert connection.sock is not None
        connection.sock = context.wrap_socket(connection.sock, server_hostname=parsed_host)


def _install_observer_lockdown() -> None:
    """Move off the host network, drop setup capability, then lock network/process syscalls."""
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.unshare(0x40000000) != 0:  # CLONE_NEWNET; connected provider socket survives setns.
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "unshare(CLONE_NEWNET)")

    class CapHeader(ctypes.Structure):
        _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]

    class CapData(ctypes.Structure):
        _fields_ = [("effective", ctypes.c_uint32), ("permitted", ctypes.c_uint32),
                    ("inheritable", ctypes.c_uint32)]

    # Remove the only setup capability from the bounding set before clearing all active sets.
    libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
    libc.prctl.restype = ctypes.c_int
    libc.capset.argtypes = [ctypes.POINTER(CapHeader), ctypes.POINTER(CapData)]
    libc.capset.restype = ctypes.c_int
    libc.unshare.argtypes = [ctypes.c_int]
    libc.unshare.restype = ctypes.c_int
    if libc.prctl(24, 21, 0, 0, 0) != 0:  # PR_CAPBSET_DROP, CAP_SYS_ADMIN
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "drop CAP_SYS_ADMIN bounding capability")
    if libc.prctl(24, 8, 0, 0, 0) != 0:  # PR_CAPBSET_DROP, CAP_SETPCAP
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "drop CAP_SETPCAP bounding capability")
    header = CapHeader(0x20080522, 0)  # _LINUX_CAPABILITY_VERSION_3
    data = (CapData * 2)()
    if libc.capset(ctypes.byref(header), ctypes.cast(data, ctypes.POINTER(CapData))) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "capset(empty)")
    if libc.prctl(38, 1, 0, 0, 0) != 0:  # PR_SET_NO_NEW_PRIVS
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "PR_SET_NO_NEW_PRIVS")

    install_observer_seccomp()


def install_observer_seccomp() -> None:
    """Install the exact observer syscall filter after no-new-privileges is active."""
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
    libc.prctl.restype = ctypes.c_int

    class SockFilter(ctypes.Structure):
        _fields_ = [("code", ctypes.c_ushort), ("jt", ctypes.c_ubyte),
                    ("jf", ctypes.c_ubyte), ("k", ctypes.c_uint32)]

    class SockFprog(ctypes.Structure):
        _fields_ = [("len", ctypes.c_ushort), ("filter", ctypes.POINTER(SockFilter))]

    raw = seccomp70.build_observer_filter()
    rows = [SockFilter(*struct.unpack("HBBI", raw[i:i + 8])) for i in range(0, len(raw), 8)]
    filters = (SockFilter * len(rows))(*rows)
    program = SockFprog(len(rows), filters)
    filter_pointer = ctypes.cast(ctypes.byref(program), ctypes.c_void_p).value
    if libc.prctl(22, 2, filter_pointer, 0, 0) != 0:  # PR_SET_SECCOMP, SECCOMP_MODE_FILTER
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), "PR_SET_SECCOMP")


def _observer_status() -> dict[str, str]:
    wanted = {"CapEff", "CapPrm", "CapBnd", "NoNewPrivs", "Seccomp", "NSpid"}
    values: dict[str, str] = {}
    for line in open("/proc/self/status", encoding="ascii"):
        key, _, value = line.partition(":")
        if key in wanted:
            values[key] = value.strip()
    return values


def _boundary_probes(chain: evidence70.ChainWriter, probe_paths: list[tuple[str, str]],
                     supervisor_pid: int, credential_env: str, route_fd: int) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for label, path in probe_paths:
        try:
            with open(path, "rb") as stream:
                stream.read(1)
            result = {"name": label, "disposition": "unexpectedly-readable", "errno": None}
        except OSError as exc:
            result = {"name": label, "disposition": "denied", "errno": exc.errno}
        results.append(result)

    for family, label in ((socket.AF_INET, "new-af-inet-socket"), (socket.AF_UNIX, "new-af-unix-socket")):
        try:
            candidate = socket.socket(family, socket.SOCK_STREAM)
            candidate.close()
            result = {"name": label, "disposition": "unexpectedly-allowed", "errno": None}
        except OSError as exc:
            result = {"name": label, "disposition": "denied", "errno": exc.errno}
        results.append(result)

    # Attempt an addressed send on the only connected provider socket. Seccomp must deny the
    # syscall before the kernel can emit a packet to this unrelated destination.
    class SockAddrIn(ctypes.Structure):
        _fields_ = [("family", ctypes.c_ushort), ("port", ctypes.c_ushort),
                    ("address", ctypes.c_uint32), ("zero", ctypes.c_ubyte * 8)]

    libc = ctypes.CDLL(None, use_errno=True)
    destination = SockAddrIn(socket.AF_INET, socket.htons(53), int.from_bytes(socket.inet_aton("1.1.1.1"), "little"),
                             (ctypes.c_ubyte * 8)())
    sent = libc.sendto(route_fd, ctypes.c_char_p(b"x"), 1, 0, ctypes.byref(destination), ctypes.sizeof(destination))
    results.append({"name": "unrelated-addressed-network-send", "disposition": "denied" if sent < 0 else "unexpectedly-allowed",
                    "errno": ctypes.get_errno() if sent < 0 else None})

    for name, operation in (
        ("unrelated-process-control", lambda: os.kill(supervisor_pid, 0)),
    ):
        try:
            operation()
            result = {"name": name, "disposition": "unexpectedly-allowed", "errno": None}
        except OSError as exc:
            result = {"name": name, "disposition": "denied", "errno": exc.errno}
        results.append(result)

    ctypes.set_errno(0)
    ptrace_result = libc.ptrace(16, supervisor_pid, 0, 0)
    ptrace_errno = ctypes.get_errno()
    results.append({"name": "unrelated-process-inspection",
                    "disposition": "denied" if ptrace_result == -1 and ptrace_errno == seccomp70.EPERM else "unexpectedly-allowed",
                    "errno": ptrace_errno if ptrace_result == -1 else None})

    results.append({"name": "credential-environment", "disposition": "unavailable" if credential_env not in os.environ else "unexpectedly-present",
                    "errno": None})
    for result in results:
        chain.append("boundary_probe", result)
    if any(result["disposition"] not in ("denied", "unavailable") for result in results):
        raise RuntimeError("observer least-privilege hostile probe unexpectedly succeeded")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mux-in-fd", type=int, required=True)
    parser.add_argument("--mux-out-fd", type=int, required=True)
    parser.add_argument("--evidence-fd", type=int, required=True)
    parser.add_argument("--upstream", required=True, help="http(s)://host:port[/base]")
    parser.add_argument("--credential-env", default=None)
    parser.add_argument("--placeholder", required=True, help="the non-secret key the subject is configured with")
    parser.add_argument("--allowed-path", default="/v1/chat/completions")
    parser.add_argument("--blocked-discovery-target", required=True)
    parser.add_argument("--upstream-timeout", type=float, default=600.0)
    parser.add_argument("--max-requests", type=int, default=None, help="supervisor-set inference request (turn) budget")
    parser.add_argument("--credential-fd", type=int, required=True)
    parser.add_argument("--supervisor-pid", type=int, required=True)
    parser.add_argument("--supervisor-netns", required=True)
    parser.add_argument("--supervisor-pidns", required=True)
    parser.add_argument("--probe-path", action="append", default=[], help="host path probe as LABEL=PATH")
    args = parser.parse_args(argv)

    chain = evidence70.ChainWriter(args.evidence_fd, OBSERVER_ID)
    chain.append("start", {
        "max_requests": args.max_requests,
        "observer": OBSERVER_ID,
        "allowed_path": args.allowed_path,
        "blocked_discovery_target": args.blocked_discovery_target,
        "credential_delivery": "supervisor descriptor after observer lockdown",
        "placeholder_sha256": hashlib.sha256(args.placeholder.encode()).hexdigest(),
    })
    try:
        upstream_connection, peers = _open_frozen_route(args.upstream, args.upstream_timeout)
        chain.append("provider_route_opened", {
            "frozen_origin": f"{urlsplit(args.upstream).scheme}://{urlsplit(args.upstream).netloc}",
            "connected_peer_addresses": peers,
            "connected": upstream_connection.sock is not None,
            "socket_family": upstream_connection.sock.family if upstream_connection.sock is not None else None,
            "socket_type": upstream_connection.sock.type if upstream_connection.sock is not None else None,
        })
        _install_observer_lockdown()
        _complete_tls_handshake(upstream_connection)
        parsed_probe_paths: list[tuple[str, str]] = []
        for item in args.probe_path:
            label, sep, path = item.partition("=")
            if not sep or not label or not path:
                raise RuntimeError("malformed observer boundary probe path")
            parsed_probe_paths.append((label, path))
        probes = _boundary_probes(chain, parsed_probe_paths, args.supervisor_pid, args.credential_env or "",
                                  upstream_connection.sock.fileno())
        chain.append("boundary", {
            "network_namespace": os.readlink("/proc/self/ns/net"),
            "pid_namespace": os.readlink("/proc/self/ns/pid"),
            "supervisor_network_namespace": args.supervisor_netns,
            "supervisor_pid_namespace": args.supervisor_pidns,
            "status": _observer_status(),
            "provider_socket_peer": str(upstream_connection.sock.getpeername()),
            "boundary_probe_count": len(probes),
            "seccomp_locked": True,
            "capabilities_dropped": True,
        })
        print("boundary-ready", flush=True)
        credential_bytes = bytearray()
        while True:
            chunk = os.read(args.credential_fd, 4096)
            if not chunk:
                break
            credential_bytes.extend(chunk)
            if len(credential_bytes) > 1024 * 1024:
                raise RuntimeError("provider credential descriptor exceeded its bound")
        os.close(args.credential_fd)
        if not credential_bytes:
            raise RuntimeError("provider credential descriptor closed without a credential")
        credential = bytes(credential_bytes).decode("utf-8")
        chain.append("credential_received", {"received_after_lockdown": True, "bytes": len(credential_bytes)})
        observer = Observer(chain, args.upstream, credential, upstream_connection, args.placeholder,
                            args.allowed_path, args.blocked_discovery_target,
                            args.upstream_timeout, args.max_requests)
    except Exception as exc:
        chain.append("boundary_setup_failed", {"error": f"{type(exc).__name__}: {exc}"})
        chain.close(setup_failed=True)
        print(f"observer: boundary setup failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 3
    transport = mux.Mux(args.mux_in_fd, args.mux_out_fd, on_open=observer.serve)
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    transport.start()
    chain.append("ready", {"provider_route_ready": True, "boundary_ready": True})
    print("ready", flush=True)
    while not stop.wait(0.05) and transport.alive:
        pass
    threading.Event().wait(0.2)  # let in-flight handlers finish their last record
    chain.close(requests=observer.request_count, refused=observer.refused_count,
                provider_discovery_blocked=observer.provider_discovery_blocked_count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
