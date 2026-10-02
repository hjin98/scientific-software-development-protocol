#!/usr/bin/env python3
"""In-sandbox subject launcher and inference/MCP relay endpoint (SSDP 7.0 Stage F, OMP).

Runs as the first process INSIDE the subject sandbox (supervisor-authored, read-only mounted,
digest-recorded). It realizes the subject side of the two authorized cross-principal edges:

  * the single-purpose inference transport to the provider-control/observation principal, and
  * the declared MCP request/response interface to the qualification mediator,

and nothing else. The sandbox network namespace has only loopback, so the relay's loopback
listeners are the subject's only reachable services. Each edge is one inherited descriptor pair
(muxhttp70.py); those descriptors exist only in this process, which is made non-dumpable so
that /proc/<pid>/{mem,environ,fd} of this process are closed to every other sandbox process.
There is no socket path, port on the host, or token that a subject process could replay.

Authority is bound to the supervisor-authorized OMP process instance, not to "a process running
the OMP executable": a loopback connection is relayed only if its client-side socket is held by
exactly the OMP process this launcher started. A `bash`/subprocess started by OMP that opens
its own connection, a second copy of the OMP executable, or a process that merely inherited a
descriptor is refused and recorded. Nothing in the sandbox but this relay holds the transport descriptors.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import evidence70  # noqa: E402
import muxhttp70 as mux  # noqa: E402

LAUNCHER_ID = "ssdp70-subject-launcher-v1"
PR_SET_DUMPABLE = 4


def _hex_addr(ip: str, port: int) -> str:
    packed = socket.inet_aton(ip)
    return f"{packed[3]:02X}{packed[2]:02X}{packed[1]:02X}{packed[0]:02X}:{port:04X}"


def client_socket_inode(client: tuple[str, int], listener: tuple[str, int]) -> int | None:
    want_local, want_remote = _hex_addr(*client), _hex_addr(*listener)
    try:
        with open("/proc/net/tcp", encoding="ascii") as handle:
            next(handle)
            for row in handle:
                parts = row.split()
                if len(parts) >= 10 and parts[1] == want_local and parts[2] == want_remote:
                    return int(parts[9])
    except OSError:
        return None
    return None


def socket_holders(inode: int) -> set[int]:
    target = f"socket:[{inode}]"
    holders: set[int] = set()
    try:
        pids = [name for name in os.listdir("/proc") if name.isdigit()]
    except OSError:
        return holders
    for pid in pids:
        fd_dir = f"/proc/{pid}/fd"
        try:
            for fd in os.listdir(fd_dir):
                try:
                    if os.readlink(f"{fd_dir}/{fd}") == target:
                        holders.add(int(pid))
                        break
                except OSError:
                    continue
        except OSError:
            continue
    return holders


def describe(pid: int) -> dict:
    info: dict = {"pid": pid}
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as handle:
            info["cmdline"] = handle.read(400).replace(b"\0", b" ").decode("utf-8", "replace").strip()
        info["exe"] = os.readlink(f"/proc/{pid}/exe")
    except OSError:
        pass
    return info


class Relay:
    def __init__(self, name: str, port: int, transport: mux.Mux, allowed_pid: threading.Event,
                 omp_pid: list[int], chain: evidence70.ChainWriter):
        self.name = name
        self.port = port
        self.transport = transport
        self.allowed_pid = allowed_pid
        self.omp_pid = omp_pid
        self.chain = chain
        self.accepted = 0
        self.denied = 0
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind(("127.0.0.1", port))
        self.listener.listen(64)

    def serve(self) -> None:
        while True:
            try:
                conn, addr = self.listener.accept()
            except OSError:
                return
            threading.Thread(target=self._handle, args=(conn, addr), daemon=True).start()

    def _deny(self, conn: socket.socket, reason: str, holders: set[int]) -> None:
        self.denied += 1
        self.chain.append("relay_denied", {
            "relay": self.name, "reason": reason,
            "holders": [describe(pid) for pid in sorted(holders)],
        })
        conn.close()

    def _handle(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        self.allowed_pid.wait(timeout=30)
        listener_addr = conn.getsockname()
        inode = client_socket_inode(addr, listener_addr)
        if inode is None:
            self._deny(conn, "client-socket-not-identifiable", set())
            return
        holders = socket_holders(inode)
        if holders != {self.omp_pid[0]}:
            self._deny(conn, "client-socket-not-held-solely-by-the-authorized-OMP-process", holders)
            return
        if not self.transport.alive:
            self._deny(conn, "principal-transport-closed", holders)
            return
        self.accepted += 1
        virtual = self.transport.open()

        def to_principal() -> None:
            try:
                while True:
                    data = conn.recv(65536)
                    if not data:
                        break
                    virtual.sendall(data)
            except OSError:
                pass
            finally:
                virtual.close()

        threading.Thread(target=to_principal, daemon=True).start()
        try:
            while True:
                data = virtual.recv()
                if not data:
                    break
                conn.sendall(data)
        except OSError:
            pass
        finally:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()


def private_socket_pair() -> tuple[socket.socket, socket.socket]:
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    client = socket.create_connection(listener.getsockname())
    server, _ = listener.accept()
    listener.close()
    return client, server


def forward(source: socket.socket, target_fd: int) -> None:
    try:
        while True:
            data = source.recv(65536)
            if not data:
                return
            view = memoryview(data)
            while view:
                view = view[os.write(target_fd, view):]
    except OSError:
        return
    finally:
        source.close()


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_first(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return None


def main() -> int:
    config = json.load(open(sys.argv[1], encoding="utf-8"))
    libc = ctypes.CDLL(None, use_errno=True)
    libc.prctl(PR_SET_DUMPABLE, 0, 0, 0, 0)
    # This process is pid 1 of the subject sandbox and the only holder of the principal descriptors.
    # Close every other inherited descriptor so no leftover pipe/evidence end exists in the sandbox.
    keep = {0, 1, 2, config["status_fd"]}
    for spec in config["relays"]:
        keep.update((spec["read_fd"], spec["write_fd"]))
    for name in os.listdir("/proc/self/fd"):
        fd = int(name)
        if fd not in keep:
            try:
                os.close(fd)
            except OSError:
                pass

    chain = evidence70.ChainWriter(config["status_fd"], LAUNCHER_ID)

    omp_exe = config["omp_exe"]
    omp_sha = sha256_file(omp_exe)
    status_text = read_first("/proc/self/status") or ""
    facts = {
        "uid": os.getuid(),
        "ptrace_scope": read_first("/proc/sys/kernel/yama/ptrace_scope"),
        "seccomp_mode": next((l.split()[1] for l in status_text.splitlines() if l.startswith("Seccomp:")), None),
        "no_new_privs": next((l.split()[1] for l in status_text.splitlines() if l.startswith("NoNewPrivs:")), None),
        "cap_eff": next((l.split()[1] for l in status_text.splitlines() if l.startswith("CapEff:")), None),
        "netns_interfaces": sorted(os.listdir("/sys/class/net")) if os.path.isdir("/sys/class/net") else None,
        "omp_exe": omp_exe,
        "omp_exe_sha256": omp_sha,
        "omp_exe_expected_sha256": config.get("omp_exe_sha256"),
        "launcher_pid": os.getpid(),
    }
    chain.append("launcher_start", facts)
    if config.get("omp_exe_sha256") and omp_sha != config["omp_exe_sha256"]:
        chain.append("launcher_refused", {"reason": "omp-executable-digest-differs-from-frozen-identity"})
        chain.close()
        return 97

    # Runtime self-observation before OMP starts: the exact executable that will run reports its
    # own build, and reads the exact configuration files it will run with. Recorded verbatim.
    for probe in config.get("probes") or []:
        try:
            done = subprocess.run(
                probe["argv"], env=dict(config["env"]), cwd=config["cwd"], stdin=subprocess.DEVNULL,
                capture_output=True, timeout=probe.get("timeout_s", 60), close_fds=True,
            )
            chain.append("probe", {
                "name": probe["name"], "argv": probe["argv"], "returncode": done.returncode,
                "stdout_b64": __import__("base64").b64encode(done.stdout[:1 << 20]).decode("ascii"),
                "stderr_b64": __import__("base64").b64encode(done.stderr[:1 << 16]).decode("ascii"),
                "stdout_bytes": len(done.stdout),
            })
            if probe.get("name") == "effective-settings":
                if done.returncode != 0:
                    chain.append("launcher_refused", {"reason": f"effective-settings-probe-failed: rc={done.returncode}"})
                    chain.close()
                    return 98
                try:
                    payload = json.loads(done.stdout)
                    sr = payload.get("compaction.supersedeReads", {}).get("value")
                    du = payload.get("compaction.dropUseless", {}).get("value")
                    if sr is not False or du is not False:
                        chain.append("launcher_refused", {
                            "reason": f"profile-setting-mismatch: compaction.supersedeReads={sr!r}, compaction.dropUseless={du!r} (expected False)"
                        })
                        chain.close()
                        return 98
                except Exception as exc:
                    chain.append("launcher_refused", {"reason": f"effective-settings-probe-unparseable: {exc}"})
                    chain.close()
                    return 98
        except (subprocess.TimeoutExpired, OSError) as exc:
            chain.append("probe", {"name": probe["name"], "argv": probe["argv"], "error": f"{type(exc).__name__}: {exc}"})
            if probe.get("name") == "effective-settings":
                chain.append("launcher_refused", {"reason": f"effective-settings-probe-error: {type(exc).__name__}: {exc}"})
                chain.close()
                return 98

    omp_pid: list[int] = [0]
    ready = threading.Event()
    relays: list[Relay] = []
    for spec in config["relays"]:
        transport = mux.Mux(spec["read_fd"], spec["write_fd"])
        transport.start()
        relay = Relay(spec["name"], spec["port"], transport, ready, omp_pid, chain)
        relays.append(relay)
        threading.Thread(target=relay.serve, daemon=True).start()

    env = dict(config["env"])
    started = time.monotonic()
    # OMP's stdout/stderr are private loopback TCP connections to this process (the listener is
    # closed after the single accept). Unlike a pipe, a socket cannot be re-opened through
    # /proc/<pid>/fd/N, so no other sandbox process can inject into or read the native trace.
    out_client, out_server = private_socket_pair()
    err_client, err_server = private_socket_pair()
    proc = subprocess.Popen(
        config["omp_argv"], env=env, cwd=config["cwd"], stdin=subprocess.DEVNULL,
        stdout=out_client.fileno(), stderr=err_client.fileno(), close_fds=True, start_new_session=True,
    )
    out_client.close()
    err_client.close()
    pumps = [
        threading.Thread(target=forward, args=(out_server, 1), daemon=True),
        threading.Thread(target=forward, args=(err_server, 2), daemon=True),
    ]
    for pump in pumps:
        pump.start()
    omp_pid[0] = proc.pid
    exe_link = None
    try:
        exe_link = os.readlink(f"/proc/{proc.pid}/exe")
        st_proc = os.stat(f"/proc/{proc.pid}/exe")
        st_file = os.stat(omp_exe)
        same = (st_proc.st_dev, st_proc.st_ino) == (st_file.st_dev, st_file.st_ino)
    except OSError:
        same = None
    chain.append("omp_started", {"pid": proc.pid, "exe": exe_link, "exe_is_frozen_file": same})
    ready.set()

    # pid 1 must reap: poll for any child, watch the deadline, and stop OMP's process group on timeout.
    timed_out = False
    deadline = time.monotonic() + config["timeout_s"]
    status = None
    killed_at = None
    while status is None:
        try:
            pid, wait_status = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            break
        if pid == proc.pid:
            status = wait_status
            break
        now = time.monotonic()
        if now > deadline and not timed_out:
            timed_out = True
            killed_at = now
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
        if timed_out and killed_at is not None and now - killed_at > 10:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        time.sleep(0.05)
    if status is None:
        proc.returncode = 255
    elif os.WIFEXITED(status):
        proc.returncode = os.WEXITSTATUS(status)
    else:
        proc.returncode = -os.WTERMSIG(status)
    rc = proc.returncode
    for pump in pumps:
        pump.join(10)
    chain.append("omp_exit", {
        "returncode": rc, "timed_out": timed_out, "wall_s": round(time.monotonic() - started, 3),
        "relays": {r.name: {"accepted": r.accepted, "denied": r.denied} for r in relays},
    })
    chain.close()
    return 124 if timed_out else (rc if rc >= 0 else 128 - rc)


if __name__ == "__main__":
    raise SystemExit(main())
