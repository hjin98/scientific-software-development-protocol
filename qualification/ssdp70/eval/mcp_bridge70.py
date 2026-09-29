#!/usr/bin/env python3
"""Qualification MCP bridge (supervisor trust domain, not a fourth principal).

The frozen, unchanged qualification mediator (`stub_tools/mediator.py`) is a stdio MCP server.
OMP is a subject-side process and must not spawn it: a mediator running in the subject's
sandbox would put the stub root, side-effect log and account identity within the subject's
reach. Instead the supervisor runs the mediator here, outside the subject boundary, and OMP
reaches it through the declared MCP request/response interface only, as a streamable-HTTP MCP
server behind the same in-sandbox relay and descriptor-bound transport as the inference path.
Every JSON-RPC message in both directions is retained as hash-linked evidence (this is where
the raw `tools/list` surface is bound to the native tool ids).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import signal
import subprocess
import sys
import threading
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence70  # noqa: E402
import muxhttp70 as mux  # noqa: E402

BRIDGE_ID = "ssdp70-mcp-bridge-v1"


class Mediator:
    def __init__(self, argv: list[str], env: dict[str, str]):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, text=True, bufsize=1,
        )
        self.lock = threading.Lock()

    def exchange(self, message: Any) -> Any | None:
        line = json.dumps(message, separators=(",", ":"), sort_keys=True)
        with self.lock:
            if self.proc.poll() is not None:
                raise RuntimeError("mediator process has exited")
            assert self.proc.stdin is not None and self.proc.stdout is not None
            self.proc.stdin.write(line + "\n")
            self.proc.stdin.flush()
            if not isinstance(message, dict) or "id" not in message or message.get("id") is None:
                return None
            response = self.proc.stdout.readline()
            if not response:
                raise RuntimeError("mediator closed its output")
            return json.loads(response)

    def close(self) -> None:
        try:
            if self.proc.stdin:
                self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()


class Bridge:
    def __init__(self, mediator: Mediator, chain: evidence70.ChainWriter):
        self.mediator = mediator
        self.chain = chain
        self.session_id = secrets.token_hex(8)
        self.count = 0
        self.refused = 0
        self.lock = threading.Lock()

    def refuse(self, conn: mux.Conn, status: int, reason: str, **extra: Any) -> None:
        with self.lock:
            self.refused += 1
        self.chain.append("refused", {"reason": reason, **extra})
        mux.send_simple(conn, status)

    def serve(self, conn: mux.Conn) -> None:
        try:
            request = mux.read_request(conn)
            if request is None:
                self.refuse(conn, 400, "malformed-request")
                return
            if request.path != "/mcp":
                self.refuse(conn, 404, "path-not-mcp", path=request.target)
                return
            if request.method == "DELETE":
                mux.send_simple(conn, 200)
                return
            if request.method != "POST":
                self.refuse(conn, 405, "server-initiated-stream-not-offered", method=request.method)
                return
            self.post(conn, request)
        except Exception as exc:
            try:
                self.chain.append("refused", {"reason": f"handler-error:{type(exc).__name__}"})
            except RuntimeError:
                pass
        finally:
            conn.close()

    def post(self, conn: mux.Conn, request: mux.Request) -> None:
        body = request.body
        with self.lock:
            self.count += 1
            index = self.count
        self.chain.append("mcp_request", {
            "exchange_index": index,
            "body_bytes": len(body),
            "body_sha256": hashlib.sha256(body).hexdigest(),
            "body_b64": base64.b64encode(body).decode("ascii"),
            "session_header": request.headers.get("mcp-session-id"),
        })
        try:
            parsed = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.chain.append("mcp_response", {"exchange_index": index, "status": 400, "body_b64": ""})
            mux.send_simple(conn, 400)
            return
        batch = isinstance(parsed, list)
        responses: list[Any] = []
        try:
            for message in (parsed if batch else [parsed]):
                reply = self.mediator.exchange(message)
                if reply is not None:
                    responses.append(reply)
        except Exception as exc:
            text = f"{type(exc).__name__}: {exc}"
            self.chain.append("mcp_response", {"exchange_index": index, "status": 500, "error": text})
            mux.send_simple(conn, 500, text.encode(), "text/plain")
            return
        if not responses:
            self.chain.append("mcp_response", {"exchange_index": index, "status": 202, "body_b64": ""})
            mux.send_simple(conn, 202)
            return
        payload = json.dumps(responses if batch else responses[0], separators=(",", ":"), sort_keys=True).encode("utf-8")
        self.chain.append("mcp_response", {
            "exchange_index": index, "status": 200,
            "body_bytes": len(payload), "body_sha256": hashlib.sha256(payload).hexdigest(),
            "body_b64": base64.b64encode(payload).decode("ascii"),
        })
        mux.send_simple(conn, 200, payload, "application/json", {"mcp-session-id": self.session_id})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mux-in-fd", type=int, required=True)
    parser.add_argument("--mux-out-fd", type=int, required=True)
    parser.add_argument("--evidence-fd", type=int, required=True)
    parser.add_argument("mediator", nargs=argparse.REMAINDER, help="-- <mediator argv>")
    args = parser.parse_args(argv)
    mediator_argv = [a for a in args.mediator if a != "--"] if args.mediator and args.mediator[0] == "--" else args.mediator
    if not mediator_argv:
        print("bridge: no mediator argv", file=sys.stderr)
        return 2

    chain = evidence70.ChainWriter(args.evidence_fd, BRIDGE_ID)
    mediator = Mediator(mediator_argv, {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
    chain.append("start", {"bridge": BRIDGE_ID, "mediator_argv_sha256": hashlib.sha256(json.dumps(mediator_argv).encode()).hexdigest()})
    bridge = Bridge(mediator, chain)
    transport = mux.Mux(args.mux_in_fd, args.mux_out_fd, on_open=bridge.serve)
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    transport.start()
    print("ready", flush=True)
    stop.wait()
    threading.Event().wait(0.2)
    mediator.close()
    chain.close(exchanges=bridge.count, refused=bridge.refused)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
