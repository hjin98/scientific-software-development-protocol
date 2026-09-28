#!/usr/bin/env python3
"""Scripted delegate stand-in (Protocol 7 qualification harness; evidence tooling only).

Usage: python tools/delegate.py --agent NAME --instruction "TEXT"   (or --instruction-file PATH)

The delegate's return is fixed by the fixture and does not depend on the instruction.
Every call, including its full instruction, is logged for the delegate-request measure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--instruction")
    group.add_argument("--instruction-file")
    args = parser.parse_args()
    instruction = args.instruction if args.instruction is not None else Path(args.instruction_file).read_text(encoding="utf-8")
    stub = Path(os.environ["SSDP70_STUB_DIR"]) / "delegates" / f"{args.agent}.json"
    with open(os.environ["SSDP70_SIDE_EFFECT_LOG"], "a", encoding="utf-8") as log:
        log.write(json.dumps({"ts": time.time(), "tool": "delegate", "agent": args.agent, "instruction": instruction,
                              "known_agent": stub.is_file()}) + "\n")
    if not stub.is_file():
        print(f"delegate: no agent named {args.agent!r} is available", file=sys.stderr)
        return 2
    print(json.loads(stub.read_text(encoding="utf-8"))["return"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
