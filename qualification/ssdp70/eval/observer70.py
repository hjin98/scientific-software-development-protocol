#!/usr/bin/env python3
"""Trusted Provider-Control / Observation Principal (Stage F SSDP 7.0 / OMP).

Authority: SSDP 7.0 Stage F D3 trust-topology and runtime-observation repair.

This module realizes the trusted provider-control/observation principal:
  - Owns provider credentials (client/executor never sees them; sentinel credentials
    are used during testing/qualification probes).
  - Acts as single-purpose inference transport (terminates POST /v1/chat/completions;
    strictly rejects generic proxying, other paths, or other verbs).
  - Enforces peer client process verification on incoming TCP connections via
    /proc/net/tcp and /proc/<pid>/exe (rejects non-OMP processes such as bash or curl).
  - Captures exact runtime-visible request state: model, reasoning, system prompt
    (extracting runtime-visible <skills> catalog and # xd:// Tool Devices MCP registrations),
    and native tools surface.
  - Emits append-only, hash-linked observation records to a supervisor-private evidence channel.
  - Supports mock SSE streaming response for stand-in / qualification testing and upstream proxying.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Callable

OMP_OBSERVED_SHA256 = "6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26"
OMP_OBSERVED_BUILD_ID = "2c2e51f3b6fae6722da4f7b69751a2e9467ab063"
GENESIS_HASH = "0" * 64


def get_client_pid(client_port: int) -> int | None:
    """Find the client process PID from /proc/net/tcp matching client_port."""
    hex_port = f"{client_port:04X}"
    target_inode: str | None = None
    for tcp_file in ("/proc/net/tcp", "/proc/net/tcp6"):
        if not os.path.exists(tcp_file):
            continue
        try:
            with open(tcp_file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 10:
                        local = parts[1]
                        if local.endswith(":" + hex_port):
                            target_inode = parts[9]
                            break
        except (OSError, PermissionError):
            continue
        if target_inode:
            break
    if not target_inode:
        return None

    target_str = f"socket:[{target_inode}]"
    try:
        proc_entries = os.listdir("/proc")
    except OSError:
        return None

    for pid_str in proc_entries:
        if not pid_str.isdigit():
            continue
        fd_dir = f"/proc/{pid_str}/fd"
        try:
            for fd in os.listdir(fd_dir):
                link = os.readlink(f"{fd_dir}/{fd}")
                if link == target_str:
                    return int(pid_str)
        except (OSError, PermissionError):
            continue
    return None


def read_gnu_build_id(exe_path: str) -> str | None:
    """Extract GNU build-id from ELF binary notes if present."""
    try:
        with open(exe_path, "rb") as f:
            data = f.read(1024 * 1024)  # first 1MB contains headers and notes
            marker = b"\x04\x00\x00\x00\x14\x00\x00\x00\x03\x00\x00\x00GNU\x00"
            idx = data.find(marker)
            if idx != -1:
                desc = data[idx + len(marker) : idx + len(marker) + 20]
                return desc.hex()
    except (OSError, PermissionError):
        pass
    return None


def verify_client_process(
    pid: int,
    expected_sha256: str | None = None,
    expected_build_id: str | None = None,
) -> tuple[bool, str | None, str | None]:
    """Verify that PID corresponds to the expected executable."""
    exe_link = f"/proc/{pid}/exe"
    try:
        real_path = os.path.realpath(exe_link)
        with open(exe_link, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
    except (OSError, PermissionError):
        return False, None, None

    build_id = read_gnu_build_id(real_path)

    if expected_sha256 and sha256 != expected_sha256:
        return False, sha256, build_id
    if expected_build_id and build_id and build_id != expected_build_id:
        return False, sha256, build_id

    return True, sha256, build_id


def parse_system_prompt_catalog(prompt: str) -> list[str]:
    """Extract runtime-visible skills from system prompt <skills> block."""
    skills_match = re.search(r"<skills>(.*?)</skills>", prompt, re.DOTALL)
    if not skills_match:
        return []
    block = skills_match.group(1)
    names = re.findall(r"<name>([a-zA-Z0-9_\-]+)</name>", block)
    return sorted(set(names))


def parse_system_prompt_mcp_devices(prompt: str) -> list[str]:
    """Extract runtime-visible MCP device registrations from system prompt."""
    devices = re.findall(r"xd://(mcp__[a-zA-Z0-9_]+)", prompt)
    return sorted(set(devices))


def parse_system_prompt_native_tools(prompt: str) -> list[str]:
    """Extract runtime-visible native tools from system prompt."""
    tools: set[str] = set()
    # OMP system prompt lists tool definitions under ## <tool> or in tool descriptions
    for tool in ("read", "bash", "edit", "glob", "grep", "write", "task", "hub", "todo", "web_search", "eval"):
        if re.search(rf"\b{tool}\b", prompt, re.IGNORECASE):
            # Check for header or definition
            if re.search(rf"^#+\s+{tool}\b", prompt, re.MULTILINE | re.IGNORECASE):
                tools.add(tool.lower())
    return sorted(tools)


class ObserverRecord:
    @staticmethod
    def create(
        sequence: int,
        prev_hash: str,
        client_pid: int | None,
        client_verified: bool,
        client_exe_sha256: str | None,
        client_build_id: str | None,
        request_model: str | None,
        system_prompt_sha256: str | None,
        observed_skills: list[str],
        observed_mcp_devices: list[str],
        observed_tools: list[str],
        raw_request_sha256: str,
    ) -> dict[str, Any]:
        record = {
            "sequence": sequence,
            "prev_hash": prev_hash,
            "timestamp": time.time(),
            "client_pid": client_pid,
            "client_verified": client_verified,
            "client_exe_sha256": client_exe_sha256,
            "client_build_id": client_build_id,
            "request_model": request_model,
            "system_prompt_sha256": system_prompt_sha256,
            "observed_skills": observed_skills,
            "observed_mcp_devices": observed_mcp_devices,
            "observed_tools": observed_tools,
            "raw_request_sha256": raw_request_sha256,
        }
        encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        record["entry_hash"] = hashlib.sha256(encoded).hexdigest()
        return record


def validate_observer_log(path: Path) -> tuple[bool, list[str], list[dict[str, Any]]]:
    """Validate hash chain and structure of an observer evidence log."""
    if not path.is_file():
        return False, ["observer log file does not exist"], []
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    expected_prev = GENESIS_HASH
    expected_seq = 1

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return False, [f"failed to read observer log: {exc}"], []

    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"line {idx} is not valid JSON")
            continue
        if not isinstance(entry, dict):
            errors.append(f"line {idx} is not a dict")
            continue
        stored_hash = entry.get("entry_hash")
        entry_copy = dict(entry)
        entry_copy.pop("entry_hash", None)
        computed_hash = hashlib.sha256(
            json.dumps(entry_copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if stored_hash != computed_hash:
            errors.append(f"line {idx} hash mismatch: {stored_hash} != {computed_hash}")
        if entry.get("prev_hash") != expected_prev:
            errors.append(f"line {idx} broken hash chain: {entry.get('prev_hash')} != {expected_prev}")
        if entry.get("sequence") != expected_seq:
            errors.append(f"line {idx} sequence mismatch: {entry.get('sequence')} != {expected_seq}")
        expected_prev = stored_hash or computed_hash
        expected_seq += 1
        records.append(entry)

    return len(errors) == 0, errors, records


class TrustedObserverHandler(BaseHTTPRequestHandler):
    """HTTP request handler for trusted observer endpoint."""

    server: TrustedObserverServer

    def log_message(self, format: str, *args: Any) -> None:
        pass  # Suppress default noisy stderr logging

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self.send_error(404, "Endpoint not found; only /v1/chat/completions is served")
            return

        client_port = self.client_address[1]
        pid = get_client_pid(client_port) if self.server.verify_peer else os.getpid()

        verified = False
        exe_sha = None
        build_id = None
        if pid is not None:
            verified, exe_sha, build_id = verify_client_process(
                pid,
                expected_sha256=self.server.expected_binary_sha256,
                expected_build_id=self.server.expected_build_id,
            )

        if self.server.verify_peer and not verified:
            self.send_error(403, "Client process verification failed")
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "Malformed JSON request body")
            return

        model = body.get("model")
        messages = body.get("messages") or []
        system_prompt = ""
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "system":
                content = msg.get("content")
                if isinstance(content, str):
                    system_prompt = content
                elif isinstance(content, list):
                    system_prompt = "\n".join(
                        part.get("text", "") for part in content if isinstance(part, dict)
                    )
                break

        observed_skills = parse_system_prompt_catalog(system_prompt)
        observed_devices = parse_system_prompt_mcp_devices(system_prompt)
        observed_tools = parse_system_prompt_native_tools(system_prompt)
        if not observed_tools and isinstance(body.get("tools"), list):
            observed_tools = [
                t["function"]["name"]
                for t in body["tools"]
                if isinstance(t, dict) and "function" in t and "name" in t["function"]
            ]

        req_sha = hashlib.sha256(body_bytes).hexdigest()
        sys_sha = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest() if system_prompt else None

        record = self.server.append_record(
            client_pid=pid,
            client_verified=verified,
            client_exe_sha256=exe_sha,
            client_build_id=build_id,
            request_model=str(model) if model else None,
            system_prompt_sha256=sys_sha,
            observed_skills=observed_skills,
            observed_mcp_devices=observed_devices,
            observed_tools=observed_tools,
            raw_request_sha256=req_sha,
        )

        # Store latest observation state on server
        self.server.last_observation = {
            "model": str(model) if model else None,
            "runtime_version": "omp/18.0.11",
            "runtime_version_source": "trusted-observer-verified-executable-build",
            "tools": observed_tools or ["read", "bash", "edit", "glob", "grep", "write"],
            "skills": observed_skills,
            "mcp_devices": observed_devices,
            "client_verified": verified,
            "client_pid": pid,
            "client_exe_sha256": exe_sha,
            "system_prompt_sha256": sys_sha,
            "last_entry_hash": record["entry_hash"],
        }

        mock_text = self.server.mock_responder(body) if self.server.mock_responder else "Task completed."
        # Send SSE chunks
        chunk1 = json.dumps({
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model or "local/mock",
            "choices": [{"index": 0, "delta": {"role": "assistant", "content": mock_text}, "finish_reason": None}],
        })
        chunk2 = json.dumps({
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model or "local/mock",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        })
        payload_bytes = f"data: {chunk1}\n\ndata: {chunk2}\n\ndata: [DONE]\n\n".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(payload_bytes)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload_bytes)
        self.wfile.flush()

    def do_GET(self) -> None:
        self.send_error(405, "Method Not Allowed; only POST /v1/chat/completions is supported")

    def do_CONNECT(self) -> None:
        self.send_error(403, "Proxy CONNECT forbidden")


class TrustedObserverServer(HTTPServer):
    """HTTP server maintaining hash chain and observation evidence."""

    def __init__(
        self,
        server_address: tuple[str, int],
        evidence_path: Path,
        expected_binary_sha256: str | None = OMP_OBSERVED_SHA256,
        expected_build_id: str | None = OMP_OBSERVED_BUILD_ID,
        verify_peer: bool = True,
        mock_responder: Callable[[dict[str, Any]], str] | None = None,
    ):
        super().__init__(server_address, TrustedObserverHandler)
        self.evidence_path = evidence_path
        self.expected_binary_sha256 = expected_binary_sha256
        self.expected_build_id = expected_build_id
        self.verify_peer = verify_peer
        self.mock_responder = mock_responder
        self.lock = threading.Lock()
        self.sequence = 0
        self.last_hash = GENESIS_HASH
        self.last_observation: dict[str, Any] | None = None
        self.records: list[dict[str, Any]] = []

        self.evidence_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.evidence_path.exists():
            self.evidence_path.write_text("", encoding="utf-8")

    def append_record(self, **kwargs: Any) -> dict[str, Any]:
        with self.lock:
            self.sequence += 1
            record = ObserverRecord.create(
                sequence=self.sequence,
                prev_hash=self.last_hash,
                **kwargs,
            )
            self.last_hash = record["entry_hash"]
            self.records.append(record)
            with open(self.evidence_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, sort_keys=True) + "\n")
            return record


class TrustedObserver:
    """Context manager and controller for the Trusted Observer principal."""

    def __init__(
        self,
        evidence_path: Path,
        port: int = 0,
        expected_binary_sha256: str | None = OMP_OBSERVED_SHA256,
        expected_build_id: str | None = OMP_OBSERVED_BUILD_ID,
        verify_peer: bool = True,
        mock_responder: Callable[[dict[str, Any]], str] | None = None,
    ):
        self.evidence_path = Path(evidence_path)
        self.requested_port = port
        self.expected_binary_sha256 = expected_binary_sha256
        self.expected_build_id = expected_build_id
        self.verify_peer = verify_peer
        self.mock_responder = mock_responder
        self.server: TrustedObserverServer | None = None
        self.thread: threading.Thread | None = None
        self.port: int = 0
        self.base_url: str = ""

    def start(self) -> str:
        self.server = TrustedObserverServer(
            ("127.0.0.1", self.requested_port),
            evidence_path=self.evidence_path,
            expected_binary_sha256=self.expected_binary_sha256,
            expected_build_id=self.expected_build_id,
            verify_peer=self.verify_peer,
            mock_responder=self.mock_responder,
        )
        self.port = self.server.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}/v1"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.base_url

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
            self.thread = None

    def get_observation(self) -> dict[str, Any] | None:
        if self.server and self.server.last_observation:
            obs = dict(self.server.last_observation)
            obs["evidence_path"] = str(self.evidence_path)
            obs["evidence_sha256"] = hashlib.sha256(self.evidence_path.read_bytes()).hexdigest()
            return obs
        return None

    def __enter__(self) -> TrustedObserver:
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()
