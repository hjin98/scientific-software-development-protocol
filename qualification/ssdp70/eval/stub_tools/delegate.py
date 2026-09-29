#!/usr/bin/env python3
"""Mediated scripted delegate stand-in for Protocol 7 qualification."""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
from pathlib import Path

def call_mediator(request: dict) -> int:
    socket_path = os.environ.get("SSDP70_MEDIATOR_SOCKET")
    if not socket_path:
        print("SSDP70_MEDIATOR_SOCKET is not configured", file=sys.stderr)
        return 2
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        conn.connect(socket_path)
        conn.sendall((json.dumps(request, sort_keys=True) + "\n").encode("utf-8"))
        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
    response = json.loads(data.decode("utf-8"))
    sys.stdout.write(response.get("stdout", ""))
    sys.stderr.write(response.get("stderr", ""))
    return int(response.get("returncode", 2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--instruction")
    group.add_argument("--instruction-file")
    args = parser.parse_args()
    instruction = args.instruction if args.instruction is not None else Path(args.instruction_file).read_text(encoding="utf-8")
    return call_mediator({"tool": "delegate", "agent": args.agent, "instruction": instruction})


if __name__ == "__main__":
    raise SystemExit(main())
