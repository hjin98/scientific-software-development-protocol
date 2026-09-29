#!/usr/bin/env python3
"""Qualification-owned deterministic model-provider stand-in (D4 verification only).

It replaces only the EXTERNAL model provider below the trusted provider-control/observation
principal: it speaks a minimal OpenAI-compatible `POST /v1/chat/completions` (SSE streaming)
and answers from a scripted scenario. It is never part of the accepted principal graph and is
not a credential store; a sentinel credential is only compared, never persisted.

Scenario JSON: {"steps": [step, ...], "on_exhaust": "stop"}
  step := {"text": "..."} | {"tool_calls": [{"name": str, "arguments": {...}}], "text": optional}
          | {"http_error": 500}     (test the provider-managed retry surface)
          | {"text": "...", "finish": "length"}   (output-token cap reached)
Step i answers the i-th /chat/completions request of the process (a request whose last message
is a tool result continues the scenario like any other request). Every request body is appended
to `--log` as one JSON line so tests can compare what the model actually received.
"""
from __future__ import annotations

import argparse
import json
import os
import socketserver
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class _State:
    def __init__(self, scenario: dict, log_path: str | None, expected_credential: str | None):
        self.scenario = scenario
        self.log_path = log_path
        self.expected_credential = expected_credential
        self.lock = threading.Lock()
        self.count = 0


def _sse(handler: BaseHTTPRequestHandler, chunks: list[dict]) -> None:
    handler.send_response(200)
    handler.send_header("content-type", "text/event-stream")
    handler.send_header("cache-control", "no-cache")
    handler.end_headers()
    for chunk in chunks:
        handler.wfile.write(b"data: " + json.dumps(chunk).encode() + b"\n\n")
    handler.wfile.write(b"data: [DONE]\n\n")
    handler.wfile.flush()


def _chunks(step: dict, index: int, model: str) -> list[dict]:
    base = {"id": f"stand-{index}", "object": "chat.completion.chunk", "model": model}
    out: list[dict] = []
    text = step.get("text")
    if text:
        out.append({**base, "choices": [{"index": 0, "delta": {"role": "assistant", "content": text}, "finish_reason": None}]})
    calls = step.get("tool_calls") or []
    for position, call in enumerate(calls):
        out.append({**base, "choices": [{"index": 0, "delta": {"role": "assistant", "tool_calls": [{
            "index": position,
            "id": call.get("id") or f"call_{index}_{position}",
            "type": "function",
            "function": {"name": call["name"], "arguments": json.dumps(call.get("arguments") or {})},
        }]}, "finish_reason": None}]})
    finish = step.get("finish") or ("tool_calls" if calls else "stop")
    out.append({**base, "choices": [{"index": 0, "delta": {}, "finish_reason": finish}],
                "usage": {"prompt_tokens": 10 + index, "completion_tokens": 5 if (text or calls) else 0,
                          "total_tokens": (15 if (text or calls) else 10) + index}})
    return out


def make_handler(state: _State):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):  # noqa: D401
            return

        def do_GET(self):
            self.send_response(404)
            self.send_header("content-length", "0")
            self.end_headers()

        def do_POST(self):
            length = int(self.headers.get("content-length") or 0)
            raw = self.rfile.read(length)
            with state.lock:
                index = state.count
                state.count += 1
                if state.log_path:
                    row = {
                        "index": index,
                        "path": self.path,
                        "authorization_ok": (
                            state.expected_credential is None
                            or self.headers.get("authorization") == f"Bearer {state.expected_credential}"
                        ),
                        "body": json.loads(raw.decode("utf-8") or "null") if raw else None,
                    }
                    with open(state.log_path, "a", encoding="utf-8") as handle:
                        handle.write(json.dumps(row, sort_keys=True) + "\n")
            steps = state.scenario.get("steps") or []
            if self.path.split("?")[0] not in ("/v1/chat/completions", "/chat/completions"):
                self.send_response(404)
                self.send_header("content-length", "0")
                self.end_headers()
                return
            if state.expected_credential is not None and self.headers.get("authorization") != f"Bearer {state.expected_credential}":
                self.send_response(401)
                self.send_header("content-length", "0")
                self.end_headers()
                return
            step = steps[index] if index < len(steps) else {"text": state.scenario.get("exhaust_text", "done")}
            if "http_error" in step:
                self.send_response(int(step["http_error"]))
                self.send_header("content-length", "0")
                self.end_headers()
                return
            _sse(self, _chunks(step, index, "stand-model"))
            self.close_connection = True

    return Handler


class _UnixHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    address_family = __import__("socket").AF_UNIX
    daemon_threads = True

    def server_bind(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        socketserver.TCPServer.server_bind(self)
        self.server_name = "unix"
        self.server_port = 0

    def get_request(self):
        request, _ = super().get_request()
        return request, ("unix", 0)


class _TcpServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


def serve(scenario: dict, *, unix: str | None = None, host: str = "127.0.0.1", port: int = 0,
          log: str | None = None, expected_credential: str | None = None):
    state = _State(scenario, log, expected_credential)
    handler = make_handler(state)
    server = _UnixHTTPServer(unix, handler) if unix else _TcpServer((host, port), handler)
    return server, state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--unix")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--log")
    parser.add_argument("--credential-env", help="name of an env var holding the credential the stand-in requires")
    args = parser.parse_args(argv)
    scenario = json.loads(open(args.scenario, encoding="utf-8").read())
    credential = os.environ.get(args.credential_env) if args.credential_env else None
    server, _ = serve(scenario, unix=args.unix, port=args.port, log=args.log, expected_credential=credential)
    print("ready", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
