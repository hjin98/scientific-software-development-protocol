#!/usr/bin/env python3
"""Append-only, hash-linked evidence records shared by the qualification principals.

The trusted provider-control/observation principal and the qualification MCP bridge emit
records through a supervisor-owned descriptor; the supervisor verifies the chain. A record's
hash covers its principal, position, predecessor, kind and data, so a dropped, reordered,
altered or truncated (no `end` record) record is detectable by the verifier.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from typing import Any, Iterable

GENESIS = "0" * 64
SCHEMA = 1


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def record_hash(principal: str, seq: int, prev: str, kind: str, t_ns: int, data: Any) -> str:
    return hashlib.sha256(canonical({
        "schema": SCHEMA, "principal": principal, "seq": seq, "prev": prev,
        "kind": kind, "t_ns": t_ns, "data": data,
    })).hexdigest()


class ChainWriter:
    """Thread-safe append-only writer over a file descriptor owned by the supervisor."""

    def __init__(self, fd: int, principal: str):
        self._fd = fd
        self.principal = principal
        self._lock = threading.Lock()
        self._seq = 0
        self._prev = GENESIS
        self._closed = False

    def append(self, kind: str, data: Any) -> dict[str, Any]:
        with self._lock:
            if self._closed:
                raise RuntimeError("evidence chain is closed")
            t_ns = time.time_ns()
            data = {**data, "monotonic_ns": time.monotonic_ns()} if kind == "request" else data
            digest = record_hash(self.principal, self._seq, self._prev, kind, t_ns, data)
            record = {
                "schema": SCHEMA, "principal": self.principal, "seq": self._seq, "prev": self._prev,
                "kind": kind, "t_ns": t_ns, "data": data, "hash": digest,
            }
            line = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
            view = memoryview(line)
            while view:
                written = os.write(self._fd, view)
                view = view[written:]
            self._seq += 1
            self._prev = digest
            return record

    def close(self, **summary: Any) -> None:
        with self._lock:
            if self._closed:
                return
            t_ns = time.time_ns()
            data = {"records": self._seq, **summary}
            digest = record_hash(self.principal, self._seq, self._prev, "end", t_ns, data)
            line = json.dumps({
                "schema": SCHEMA, "principal": self.principal, "seq": self._seq, "prev": self._prev,
                "kind": "end", "t_ns": t_ns, "data": data, "hash": digest,
            }, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
            try:
                os.write(self._fd, line)
            finally:
                self._closed = True


def parse_chain(text: str, principal: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Verify a serialized chain. Returns (records, errors); errors make the evidence unusable."""
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    prev = GENESIS
    ended = False
    lines = [line for line in text.split("\n") if line.strip()]
    for index, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{principal} evidence line {index} is not valid JSON")
            continue
        if not isinstance(record, dict):
            errors.append(f"{principal} evidence line {index} is not an object")
            continue
        if ended:
            errors.append(f"{principal} evidence continues after its end record")
        if record.get("schema") != SCHEMA or record.get("principal") != principal:
            errors.append(f"{principal} evidence line {index} has the wrong schema/principal")
        if record.get("seq") != index:
            errors.append(f"{principal} evidence line {index} has sequence {record.get('seq')!r}")
        if record.get("prev") != prev:
            errors.append(f"{principal} evidence line {index} does not link to its predecessor")
        expected = record_hash(
            str(record.get("principal")), record.get("seq", -1), str(record.get("prev")),
            str(record.get("kind")), record.get("t_ns", 0), record.get("data"),
        )
        if record.get("hash") != expected:
            errors.append(f"{principal} evidence line {index} hash does not match its content")
        prev = record.get("hash") if isinstance(record.get("hash"), str) else prev
        if record.get("kind") == "end":
            ended = True
            data = record.get("data") if isinstance(record.get("data"), dict) else {}
            if data.get("records") != index:
                errors.append(f"{principal} evidence end record counts {data.get('records')!r}, found {index}")
        records.append(record)
    if not lines:
        errors.append(f"{principal} evidence is empty (no records, no end record)")
    elif not ended:
        errors.append(f"{principal} evidence is truncated: no end record")
    return records, errors


def records_of_kind(records: Iterable[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    return [record for record in records if record.get("kind") == kind]
