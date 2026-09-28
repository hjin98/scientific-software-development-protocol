#!/usr/bin/env python3
"""Executor-side client for the harness-owned mediated issue stand-in."""
from __future__ import annotations
import argparse
import json
import os
import socket
import sys

def call_mediator(request: dict) -> int:
    socket_path = os.environ.get("SSDP70_MEDIATOR_SOCKET")
    if not socket_path:
        print("qualification mediator is not configured", file=sys.stderr)
        return 2
    payload = (json.dumps(request, sort_keys=True) + "\n").encode("utf-8")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        conn.connect(socket_path)
        conn.sendall(payload)
        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
    response = json.loads(data.decode("utf-8"))
    sys.stdout.write(str(response.get("stdout") or ""))
    sys.stderr.write(str(response.get("stderr") or ""))
    return int(response.get("returncode", 2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("locations")
    se = sub.add_parser("search"); se.add_argument("query"); se.add_argument("--location")
    sh = sub.add_parser("show"); sh.add_argument("issue_id")
    cr = sub.add_parser("create"); cr.add_argument("--location", required=True); cr.add_argument("--title", required=True); cr.add_argument("--body", required=True); cr.add_argument("--label", action="append", default=[])
    co = sub.add_parser("comment"); co.add_argument("issue_id"); co.add_argument("--body", required=True)
    args = parser.parse_args()
    request = {"tool": "issues", "op": args.cmd}
    if args.cmd == "search": request.update(query=args.query, location=args.location)
    elif args.cmd == "show": request["issue_id"] = args.issue_id
    elif args.cmd == "create": request.update(location=args.location, title=args.title, body=args.body, labels=args.label)
    elif args.cmd == "comment": request.update(issue_id=args.issue_id, body=args.body)
    return call_mediator(request)

if __name__ == "__main__":
    raise SystemExit(main())
