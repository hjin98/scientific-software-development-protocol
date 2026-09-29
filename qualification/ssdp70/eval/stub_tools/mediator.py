#!/usr/bin/env python3
"""Qualification-owned dependency-free stdio MCP server for SSDP 7.0 Stage F stand-ins."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

SERVER_NAME = "ssdp70-qualification"
SERVER_VERSION = "1"
SERVER_ID = "ssdp70-qualification-stdio-v1"
PROTOCOL_VERSION = "2025-11-25"
STORE_IDENTITY = "ssdp70-private-issue-standin"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool(name: str, description: str, properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required or [],
            "additionalProperties": False,
        },
    }


TOOLS = (
    tool("issue_locations", "List qualification issue-store locations and availability.", {}),
    tool("issue_search", "Search the qualification-owned issue stand-in.", {
        "query": {"type": "string"}, "location": {"type": "string"},
    }, ["query"]),
    tool("issue_show", "Show one issue from the qualification-owned issue stand-in.", {
        "issue_id": {"type": "string"},
    }, ["issue_id"]),
    tool("issue_create", "Create one issue in an available qualification-owned stand-in location.", {
        "location": {"type": "string"}, "title": {"type": "string"}, "body": {"type": "string"},
        "labels": {"type": "array", "items": {"type": "string"}},
    }, ["location", "title", "body"]),
    tool("issue_comment", "Append a comment to one qualification-owned stand-in issue.", {
        "issue_id": {"type": "string"}, "body": {"type": "string"},
    }, ["issue_id", "body"]),
    tool("delegate", "Call one scripted qualification delegate.", {
        "agent": {"type": "string"}, "instruction": {"type": "string"},
    }, ["agent", "instruction"]),
)


class Store:
    def __init__(self, stub_root: Path, log_path: Path, account: str):
        self.stub_root = stub_root.resolve()
        self.issues_root = (self.stub_root / "issues").resolve()
        self.delegates_root = (self.stub_root / "delegates").resolve()
        self.log_path = log_path.resolve()
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
        for loc_dir in sorted(path for path in self.issues_root.iterdir() if path.is_dir()):
            for path in sorted(loc_dir.glob("*.json")):
                yield loc_dir.name, path

    def find(self, issue_id: str):
        for location, path in self.records() or ():
            if path.stem == issue_id:
                return location, path
        return None, None

    @staticmethod
    def result(returncode: int, stdout: str = "", stderr: str = "", **evidence: Any) -> dict[str, Any]:
        return {
            "returncode": returncode,
            "stdout": stdout,
            "stderr": stderr,
            "evidence": {"store_identity": STORE_IDENTITY, **evidence},
        }

    def issue_locations(self, args: dict[str, Any]) -> dict[str, Any]:
        locations = self.config().get("locations", {})
        return self.result(
            0, "".join(f"{key}: {value}\n" for key, value in sorted(locations.items())),
            operation="locations", object_ids=sorted(locations),
            before_object_version=None, after_object_version=None,
        )

    def issue_search(self, args: dict[str, Any]) -> dict[str, Any]:
        query, location = args.get("query"), args.get("location")
        if not isinstance(query, str) or (location is not None and not isinstance(location, str)):
            return self.result(2, stderr="invalid search request\n", operation="search", object_ids=[])
        self.log({"tool": "issues", "op": "search", "query": query, "location": location})
        locations = self.config().get("locations", {})
        rows: list[str] = []
        object_ids: list[str] = []
        for target in ([location] if location else sorted(locations)):
            if not self.available(target):
                rows.append(f"[{target}] UNAVAILABLE: this location cannot be searched\n")
                continue
            for loc, path in self.records() or ():
                if loc == target:
                    data = load_json(path)
                    if query.lower() in json.dumps(data).lower():
                        rows.append(f"[{loc}] {path.stem}: {data.get('title', '')}\n")
                        object_ids.append(path.stem)
        return self.result(
            0, "".join(rows), operation="search", query=query, object_ids=object_ids,
            before_object_version=None, after_object_version=None,
        )

    def issue_show(self, args: dict[str, Any]) -> dict[str, Any]:
        issue_id = args.get("issue_id")
        if not isinstance(issue_id, str):
            return self.result(2, stderr="invalid issue id\n", operation="show", object_ids=[])
        self.log({"tool": "issues", "op": "show", "issue_id": issue_id})
        location, path = self.find(issue_id)
        if path is None:
            return self.result(1, stderr=f"no issue {issue_id}\n", operation="show", object_ids=[issue_id])
        if not self.available(location):
            return self.result(1, stderr=f"[{location}] UNAVAILABLE\n", operation="show", object_ids=[issue_id])
        version = sha256_file(path)
        data = load_json(path)
        return self.result(
            0, json.dumps({"id": issue_id, "location": location, **data}, indent=2) + "\n",
            operation="show", object_ids=[issue_id],
            before_object_version=version, after_object_version=version,
        )

    def issue_create(self, args: dict[str, Any]) -> dict[str, Any]:
        location, title, body = args.get("location"), args.get("title"), args.get("body")
        labels = args.get("labels", [])
        if not all(isinstance(value, str) for value in (location, title, body)) or not isinstance(labels, list) or not all(isinstance(value, str) for value in labels):
            return self.result(2, stderr="invalid create request\n", operation="create", object_ids=[])
        self.log({"tool": "issues", "op": "create", "location": location, "title": title, "body": body, "labels": labels})
        if not self.available(location):
            return self.result(1, stderr=f"[{location}] UNAVAILABLE: write refused\n", operation="create", object_ids=[])
        target = self.issues_root / location
        target.mkdir(parents=True, exist_ok=True)
        self.counter += 1
        issue_id = f"NEW-{int(time.time() * 1000) % 10**9:09d}-{self.counter:04d}"
        path = target / f"{issue_id}.json"
        path.write_text(json.dumps({
            "title": title, "labels": labels, "body": body, "author": self.account, "comments": [],
        }, indent=2) + "\n", encoding="utf-8")
        return self.result(
            0, f"created {issue_id} in {location} as {self.account}\n",
            operation="create", object_ids=[issue_id],
            before_object_version=None, after_object_version=sha256_file(path),
        )

    def issue_comment(self, args: dict[str, Any]) -> dict[str, Any]:
        issue_id, body = args.get("issue_id"), args.get("body")
        if not isinstance(issue_id, str) or not isinstance(body, str):
            return self.result(2, stderr="invalid comment request\n", operation="comment", object_ids=[])
        self.log({"tool": "issues", "op": "comment", "issue_id": issue_id, "body": body})
        location, path = self.find(issue_id)
        if path is None or not self.available(location):
            return self.result(1, stderr="comment refused: unknown or unavailable issue\n", operation="comment", object_ids=[issue_id])
        before = sha256_file(path)
        data = load_json(path)
        data.setdefault("comments", []).append({
            "author": self.account, "date": time.strftime("%Y-%m-%d"), "body": body,
        })
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return self.result(
            0, f"commented on {issue_id} as {self.account}\n",
            operation="comment", object_ids=[issue_id],
            before_object_version=before, after_object_version=sha256_file(path),
        )

    def delegate(self, args: dict[str, Any]) -> dict[str, Any]:
        agent, instruction = args.get("agent"), args.get("instruction")
        if not isinstance(agent, str) or not isinstance(instruction, str):
            return self.result(2, stderr="invalid delegate request\n", operation="delegate", object_ids=[])
        stub = self.delegates_root / f"{agent}.json"
        self.log({"tool": "delegate", "agent": agent, "instruction": instruction, "known_agent": stub.is_file()})
        if not stub.is_file():
            return self.result(2, stderr=f"delegate: no agent named {agent!r} is available\n", operation="delegate", object_ids=[agent])
        value = load_json(stub).get("return")
        text = value if isinstance(value, str) else json.dumps(value)
        return self.result(0, text + "\n", operation="delegate", object_ids=[agent])

    def call(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        handlers = {
            "issue_locations": self.issue_locations, "issue_search": self.issue_search,
            "issue_show": self.issue_show, "issue_create": self.issue_create,
            "issue_comment": self.issue_comment, "delegate": self.delegate,
        }
        handler = handlers.get(name)
        if handler is None:
            return self.result(2, stderr=f"unsupported MCP tool {name!r}\n", operation="unknown", object_ids=[])
        return handler(args)


class Server:
    def __init__(self, store: Store, server_id: str):
        self.store = store
        self.server_id = server_id

    @staticmethod
    def result(request_id: Any, value: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": value}

    @staticmethod
    def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}

    def dispatch(self, request: Any) -> dict[str, Any] | None:
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
            return self.error(request.get("id") if isinstance(request, dict) else None, -32600, "Invalid Request")
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params") or {}
        if not isinstance(params, dict):
            return self.error(request_id, -32602, "Invalid params")
        if method == "notifications/initialized" or request_id is None:
            return None
        if method == "initialize":
            requested = params.get("protocolVersion")
            protocol = requested if isinstance(requested, str) and requested else PROTOCOL_VERSION
            return self.result(request_id, {
                "protocolVersion": protocol,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": f"Private Stage F qualification stand-ins ({self.server_id}).",
            })
        if method == "ping":
            return self.result(request_id, {})
        if method == "tools/list":
            return self.result(request_id, {"tools": list(TOOLS)})
        if method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            if not isinstance(name, str) or not isinstance(args, dict):
                return self.error(request_id, -32602, "Invalid tool call")
            payload = self.store.call(name, args)
            return self.result(request_id, {
                "content": [{"type": "text", "text": json.dumps(payload, sort_keys=True)}],
                "isError": payload["returncode"] != 0,
            })
        return self.error(request_id, -32601, "Method not found")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stub-root", type=Path, required=True)
    parser.add_argument("--side-effect-log", type=Path, required=True)
    parser.add_argument("--account-file", type=Path, required=True)
    parser.add_argument("--server-id", required=True)
    parser.add_argument("--expected-self-sha256", required=True)
    args = parser.parse_args()

    if args.server_id != SERVER_ID:
        print("server identity mismatch", file=sys.stderr)
        return 2
    actual_self = sha256_file(Path(__file__).resolve())
    if args.expected_self_sha256 != actual_self:
        print("server executable digest mismatch", file=sys.stderr)
        return 2
    stub_root = args.stub_root.resolve()
    log_path = args.side_effect_log.resolve()
    if not stub_root.is_dir() or not args.account_file.is_file():
        print("private MCP state is unavailable", file=sys.stderr)
        return 2
    account = args.account_file.read_text(encoding="utf-8").strip()
    if not account:
        print("private MCP account identity is empty", file=sys.stderr)
        return 2
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)

    server = Server(Store(stub_root, log_path, account), args.server_id)
    for line in sys.stdin:
        if not line.strip():
            continue
        request: Any = None
        try:
            request = json.loads(line)
            response = server.dispatch(request)
        except Exception as exc:
            request_id = request.get("id") if isinstance(request, dict) else None
            response = Server.error(request_id, -32603, f"Internal error: {exc}")
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":"), sort_keys=True) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
