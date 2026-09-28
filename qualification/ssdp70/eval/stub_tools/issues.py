#!/usr/bin/env python3
"""Issue-tracker stand-in (Protocol 7 qualification harness; evidence tooling only).

Usage:
  python tools/issues.py locations
  python tools/issues.py search QUERY [--location NAME]
  python tools/issues.py show ISSUE_ID
  python tools/issues.py create --location NAME --title TITLE --body BODY [--label L ...]
  python tools/issues.py comment ISSUE_ID --body BODY

Entries carry their native author: the account that wrote them. New writes are attributed
to the account this session runs under. Every write is logged. There is no network access.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("SSDP70_STUB_DIR", ".")) / "issues"
ACCOUNT = os.environ.get("SSDP70_ACCOUNT", "unknown-account")


def config() -> dict:
    path = ROOT / "_config.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"locations": {}}


def available(location: str) -> bool:
    return config().get("locations", {}).get(location) == "available"


def records():
    for loc_dir in sorted(p for p in ROOT.iterdir() if p.is_dir()) if ROOT.is_dir() else []:
        for path in sorted(loc_dir.glob("*.json")):
            yield loc_dir.name, path


def log(event: dict) -> None:
    with open(os.environ["SSDP70_SIDE_EFFECT_LOG"], "a", encoding="utf-8") as handle:
        handle.write(json.dumps({"ts": time.time(), "tool": "issues", "account": ACCOUNT, **event}) + "\n")


def find(issue_id: str):
    for location, path in records():
        if path.stem == issue_id:
            return location, path
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("locations")
    se = sub.add_parser("search"); se.add_argument("query"); se.add_argument("--location")
    sh = sub.add_parser("show"); sh.add_argument("issue_id")
    cr = sub.add_parser("create"); cr.add_argument("--location", required=True); cr.add_argument("--title", required=True)
    cr.add_argument("--body", required=True); cr.add_argument("--label", action="append", default=[])
    co = sub.add_parser("comment"); co.add_argument("issue_id"); co.add_argument("--body", required=True)
    args = parser.parse_args()
    locations = config().get("locations", {})
    if args.cmd == "locations":
        for name, state in sorted(locations.items()):
            print(f"{name}: {state}")
        return 0
    if args.cmd == "search":
        log({"op": "search", "query": args.query, "location": args.location})
        query = args.query.lower()
        targets = [args.location] if args.location else sorted(locations)
        for location in targets:
            if not available(location):
                print(f"[{location}] UNAVAILABLE: this location cannot be searched")
                continue
            for loc, path in records():
                if loc != location:
                    continue
                data = json.loads(path.read_text(encoding="utf-8"))
                haystack = json.dumps(data).lower()
                if query in haystack:
                    print(f"[{location}] {path.stem}: {data.get('title', '')}")
        return 0
    if args.cmd == "show":
        log({"op": "show", "issue_id": args.issue_id})
        location, path = find(args.issue_id)
        if path is None:
            print(f"no issue {args.issue_id}", file=sys.stderr); return 1
        if not available(location):
            print(f"[{location}] UNAVAILABLE", file=sys.stderr); return 1
        data = json.loads(path.read_text(encoding="utf-8"))
        print(json.dumps({"id": args.issue_id, "location": location, **data}, indent=2))
        return 0
    if args.cmd == "create":
        log({"op": "create", "location": args.location, "title": args.title, "body": args.body, "labels": args.label})
        if not available(args.location):
            print(f"[{args.location}] UNAVAILABLE: write refused", file=sys.stderr); return 1
        target = ROOT / args.location
        issue_id = f"NEW-{int(time.time() * 1000) % 10**9}"
        (target / f"{issue_id}.json").write_text(json.dumps({"title": args.title, "labels": args.label, "body": args.body,
                                                              "author": ACCOUNT, "comments": []}, indent=2), encoding="utf-8")
        print(f"created {issue_id} in {args.location} as {ACCOUNT}")
        return 0
    log({"op": "comment", "issue_id": args.issue_id, "body": args.body})
    location, path = find(args.issue_id)
    if path is None or not available(location):
        print("comment refused: unknown or unavailable issue", file=sys.stderr); return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("comments", []).append({"author": ACCOUNT, "date": time.strftime("%Y-%m-%d"), "body": args.body})
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"commented on {args.issue_id} as {ACCOUNT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
