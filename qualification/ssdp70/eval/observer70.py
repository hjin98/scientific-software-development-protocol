#!/usr/bin/env python3
"""Trusted provider-control / observation principal (Stage F SSDP 7.0, OMP profile).

One of the three accepted D3 principals. It

* owns the provider credential (read once from its own environment, never written anywhere),
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
import hashlib
import http.client
import os
import signal
import sys
import threading
from typing import Any
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence70  # noqa: E402
import muxhttp70 as mux  # noqa: E402

RESPONSE_EVIDENCE_LIMIT = 4 * 1024 * 1024
HOP_BY_HOP = {
    "host", "connection", "content-length", "transfer-encoding", "keep-alive", "te", "trailer",
    "upgrade", "proxy-authorization", "proxy-connection", "authorization", "accept-encoding",
}
OBSERVER_ID = "ssdp70-provider-observer-v1"


class Observer:
    def __init__(self, chain: evidence70.ChainWriter, upstream: str, credential: str | None,
                 placeholder: str, allowed_path: str, upstream_timeout: float, max_requests: int | None = None):
        self.chain = chain
        self.upstream = urlsplit(upstream)
        self.credential = credential
        self.placeholder = placeholder
        self.allowed_path = allowed_path
        self.upstream_timeout = upstream_timeout
        self.max_requests = max_requests
        self.lock = threading.Lock()
        self.request_count = 0
        self.refused_count = 0

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
            cls = http.client.HTTPSConnection if self.upstream.scheme == "https" else http.client.HTTPConnection
            upstream = cls(self.upstream.hostname, self.upstream.port or (443 if self.upstream.scheme == "https" else 80),
                           timeout=self.upstream_timeout)
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
            upstream.close()
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mux-in-fd", type=int, required=True)
    parser.add_argument("--mux-out-fd", type=int, required=True)
    parser.add_argument("--evidence-fd", type=int, required=True)
    parser.add_argument("--upstream", required=True, help="http(s)://host:port[/base]")
    parser.add_argument("--credential-env", default=None)
    parser.add_argument("--placeholder", required=True, help="the non-secret key the subject is configured with")
    parser.add_argument("--allowed-path", default="/v1/chat/completions")
    parser.add_argument("--upstream-timeout", type=float, default=600.0)
    parser.add_argument("--max-requests", type=int, default=None, help="supervisor-set inference request (turn) budget")
    args = parser.parse_args(argv)

    credential = None
    if args.credential_env:
        credential = os.environ.pop(args.credential_env, None)
        if credential is None:
            print("observer: provider credential variable is not set", file=sys.stderr)
            return 2

    chain = evidence70.ChainWriter(args.evidence_fd, OBSERVER_ID)
    observer = Observer(chain, args.upstream, credential, args.placeholder, args.allowed_path, args.upstream_timeout,
                        args.max_requests)
    chain.append("start", {
        "max_requests": args.max_requests,
        "observer": OBSERVER_ID,
        "allowed_path": args.allowed_path,
        "credential_configured": credential is not None,
        "placeholder_sha256": hashlib.sha256(args.placeholder.encode()).hexdigest(),
    })
    transport = mux.Mux(args.mux_in_fd, args.mux_out_fd, on_open=observer.serve)
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    transport.start()
    print("ready", flush=True)
    stop.wait()
    threading.Event().wait(0.2)  # let in-flight handlers finish their last record
    chain.close(requests=observer.request_count, refused=observer.refused_count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
