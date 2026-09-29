#!/usr/bin/env python3
"""Harness-owned Unix-socket mediator for Stage F qualification stand-ins."""
from __future__ import annotations

import argparse
import json
import os
import socket
import time
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class Store:
    def __init__(self, stub_root: Path, log_path: Path, account: str):
        self.stub_root = stub_root
        self.issues_root = stub_root / "issues"
        self.delegates_root = stub_root / "delegates"
        self.log_path = log_path
        self.account = account
        self.counter = 0

    def log(self, event: dict[str, Any]) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"ts": time.time(), "account": self.account, **event}, sort_keys=True) + "\n")

    def config(self) -> dict[str, Any]:
        path = self.issues_root / "_config.json"
        return load_json(path) if path.is_file() else {"locations": {}}

    def available(self, location: str) -> bool:
        return self.config().get("locations", {}).get(location) == "available"

    def records(self):
        if not self.issues_root.is_dir():
            return
        for loc_dir in sorted(p for p in self.issues_root.iterdir() if p.is_dir()):
            for path in sorted(loc_dir.glob("*.json")):
                yield loc_dir.name, path

    def find(self, issue_id: str):
        for location, path in self.records() or ():
            if path.stem == issue_id:
                return location, path
        return None, None

    def issue(self, request: dict[str, Any]) -> dict[str, Any]:
        op = request.get("op")
        locations = self.config().get("locations", {})
        if op == "locations":
            return {"returncode": 0, "stdout": "".join(f"{name}: {state}\n" for name, state in sorted(locations.items())), "stderr": ""}
        if op == "search":
            query = request.get("query")
            location = request.get("location")
            if not isinstance(query, str) or (location is not None and not isinstance(location, str)):
                return {"returncode": 2, "stdout": "", "stderr": "invalid search request\n"}
            self.log({"tool": "issues", "op": "search", "query": query, "location": location})
            rows: list[str] = []
            targets = [location] if location else sorted(locations)
            for target in targets:
                if not self.available(target):
                    rows.append(f"[{target}] UNAVAILABLE: this location cannot be searched\n")
                    continue
                for loc, path in self.records() or ():
                    if loc == target:
                        data = load_json(path)
                        if query.lower() in json.dumps(data).lower():
                            rows.append(f"[{loc}] {path.stem}: {data.get('title', '')}\n")
            return {"returncode": 0, "stdout": "".join(rows), "stderr": ""}
        if op == "show":
            issue_id = request.get("issue_id")
            if not isinstance(issue_id, str):
                return {"returncode": 2, "stdout": "", "stderr": "invalid issue id\n"}
            self.log({"tool": "issues", "op": "show", "issue_id": issue_id})
            location, path = self.find(issue_id)
            if path is None:
                return {"returncode": 1, "stdout": "", "stderr": f"no issue {issue_id}\n"}
            if not self.available(location):
                return {"returncode": 1, "stdout": "", "stderr": f"[{location}] UNAVAILABLE\n"}
            data = load_json(path)
            return {"returncode": 0, "stdout": json.dumps({"id": issue_id, "location": location, **data}, indent=2) + "\n", "stderr": ""}
        if op == "create":
            location, title, body = request.get("location"), request.get("title"), request.get("body")
            labels = request.get("labels", [])
            if not all(isinstance(x, str) for x in (location, title, body)) or not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
                return {"returncode": 2, "stdout": "", "stderr": "invalid create request\n"}
            self.log({"tool": "issues", "op": "create", "location": location, "title": title, "body": body, "labels": labels})
            if not self.available(location):
                return {"returncode": 1, "stdout": "", "stderr": f"[{location}] UNAVAILABLE: write refused\n"}
            target = self.issues_root / location
            target.mkdir(parents=True, exist_ok=True)
            self.counter += 1
            issue_id = f"NEW-{int(time.time() * 1000) % 10**9:09d}-{self.counter:04d}"
            (target / f"{issue_id}.json").write_text(
                json.dumps({"title": title, "labels": labels, "body": body, "author": self.account, "comments": []}, indent=2) + "\n",
                encoding="utf-8",
            )
            return {"returncode": 0, "stdout": f"created {issue_id} in {location} as {self.account}\n", "stderr": ""}
        if op == "comment":
            issue_id, body = request.get("issue_id"), request.get("body")
            if not isinstance(issue_id, str) or not isinstance(body, str):
                return {"returncode": 2, "stdout": "", "stderr": "invalid comment request\n"}
            self.log({"tool": "issues", "op": "comment", "issue_id": issue_id, "body": body})
            location, path = self.find(issue_id)
            if path is None or not self.available(location):
                return {"returncode": 1, "stdout": "", "stderr": "comment refused: unknown or unavailable issue\n"}
            data = load_json(path)
            data.setdefault("comments", []).append({"author": self.account, "date": time.strftime("%Y-%m-%d"), "body": body})
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            return {"returncode": 0, "stdout": f"commented on {issue_id} as {self.account}\n", "stderr": ""}
        return {"returncode": 2, "stdout": "", "stderr": f"unsupported issue operation {op!r}\n"}

    def delegate(self, request: dict[str, Any]) -> dict[str, Any]:
        agent, instruction = request.get("agent"), request.get("instruction")
        if not isinstance(agent, str) or not isinstance(instruction, str):
            return {"returncode": 2, "stdout": "", "stderr": "invalid delegate request\n"}
        stub = self.delegates_root / f"{agent}.json"
        self.log({"tool": "delegate", "agent": agent, "instruction": instruction, "known_agent": stub.is_file()})
        if not stub.is_file():
            return {"returncode": 2, "stdout": "", "stderr": f"delegate: no agent named {agent!r} is available\n"}
        payload = load_json(stub)
        value = payload.get("return")
        return {"returncode": 0, "stdout": (value if isinstance(value, str) else json.dumps(value)) + "\n", "stderr": ""}

    def handle(self, request: Any) -> dict[str, Any]:
        if not isinstance(request, dict):
            return {"returncode": 2, "stdout": "", "stderr": "request must be a JSON object\n"}
        tool = request.get("tool")
        if tool == "issues":
            return self.issue(request)
        if tool == "delegate":
            return self.delegate(request)
        if tool == "ping":
            return {"returncode": 0, "stdout": "pong\n", "stderr": ""}
        return {"returncode": 2, "stdout": "", "stderr": f"unsupported mediated tool {tool!r}\n"}


def serve(socket_path: Path, store: Store) -> None:
    socket_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        socket_path.unlink()
    except FileNotFoundError:
        pass
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(socket_path))
        os.chmod(socket_path, 0o600)
        server.listen(16)
        while True:
            conn, _ = server.accept()
            with conn:
                data = b""
                while not data.endswith(b"\n"):
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data += chunk
                    if len(data) > 1024 * 1024:
                        break
                try:
                    response = store.handle(json.loads(data.decode("utf-8")))
                except Exception as exc:
                    response = {"returncode": 2, "stdout": "", "stderr": f"mediator error: {exc}\n"}
                conn.sendall((json.dumps(response, sort_keys=True) + "\n").encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", type=Path, required=True)
    parser.add_argument("--stub-root", type=Path, required=True)
    parser.add_argument("--side-effect-log", type=Path, required=True)
    parser.add_argument("--account", required=True)
    args = parser.parse_args()
    args.side_effect_log.parent.mkdir(parents=True, exist_ok=True)
    args.side_effect_log.touch()
    serve(args.socket, Store(args.stub_root, args.side_effect_log, args.account))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
