#!/usr/bin/env python3
"""Supervisor-owned package-access ledger and exact resource accounting (Stage F SSDP 7.0).

D3 decision: `D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md` (pending independent D3 acceptance).

The qualification supervisor records, from the kernel, which regular files of the installed
protocol package any process opened while the subject ran (Linux inotify marks on the
supervisor's own host-side directories). The ledger bounds access; model-visible tool-result text
shows supply. A file counts as consumed only when its content reached the model. An opened file
that cannot be so explained makes the observation not exact, so a burden/owner claim is
INADMISSIBLE instead of resting on a lower bound.
"""
from __future__ import annotations

import ctypes
import hashlib
import os
import re
import select
import struct
import threading
import time
from pathlib import Path
from typing import Any

SCHEMA = 1
MECHANISM = "inotify-inode-marks"

IN_ACCESS, IN_MODIFY, IN_ATTRIB = 0x1, 0x2, 0x4
IN_CLOSE_WRITE, IN_CLOSE_NOWRITE, IN_OPEN = 0x8, 0x10, 0x20
IN_MOVED_FROM, IN_MOVED_TO, IN_CREATE, IN_DELETE = 0x40, 0x80, 0x100, 0x200
IN_DELETE_SELF, IN_MOVE_SELF = 0x400, 0x800
IN_UNMOUNT, IN_Q_OVERFLOW, IN_IGNORED, IN_ISDIR = 0x2000, 0x4000, 0x8000, 0x40000000
WATCH_MASK = (IN_ACCESS | IN_MODIFY | IN_ATTRIB | IN_CLOSE_WRITE | IN_CLOSE_NOWRITE | IN_OPEN
              | IN_MOVED_FROM | IN_MOVED_TO | IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MOVE_SELF)
FLAG_NAMES = {
    IN_ACCESS: "access", IN_MODIFY: "modify", IN_ATTRIB: "attrib", IN_CLOSE_WRITE: "close_write",
    IN_CLOSE_NOWRITE: "close_nowrite", IN_OPEN: "open", IN_MOVED_FROM: "moved_from", IN_MOVED_TO: "moved_to",
    IN_CREATE: "create", IN_DELETE: "delete", IN_DELETE_SELF: "delete_self", IN_MOVE_SELF: "move_self",
    IN_UNMOUNT: "unmount", IN_Q_OVERFLOW: "overflow", IN_IGNORED: "ignored",
}
READ_FLAGS = {"open", "access", "close_nowrite"}
EVENT_HEADER = struct.Struct("iIII")

# Minimum contiguous source content (bytes) that must appear in process output for a partial supply.
PARTIAL_SUPPLY_MIN_BYTES = 48


class LedgerWatcher:
    """Record package access for the lifetime of one subject run. Owned by the supervisor."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.fd = -1
        self._wd: dict[int, str] = {}
        self._events: list[dict[str, Any]] = []
        self._flags_seen: set[str] = set()
        self._stop_r = self._stop_w = -1
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self.established = False
        self.error: str | None = None
        self.started_ns: int | None = None
        self.stopped_ns: int | None = None
        self.tree_files: dict[str, int] = {}
        self.directories: list[str] = []

    def start(self) -> "LedgerWatcher":
        try:
            if not self.root.is_dir():
                raise OSError(f"package root {self.root} is not a directory")
            for current, dirs, files in os.walk(self.root):
                rel_dir = Path(current).relative_to(self.root).as_posix()
                rel_dir = "" if rel_dir == "." else rel_dir
                self.directories.append(rel_dir)
                for name in files:
                    path = Path(current) / name
                    self.tree_files[(f"{rel_dir}/{name}" if rel_dir else name)] = path.lstat().st_size
            libc = ctypes.CDLL(None, use_errno=True)
            self.fd = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
            if self.fd < 0:
                raise OSError(ctypes.get_errno(), "inotify_init1 failed")
            for rel_dir in self.directories:
                path = self.root / rel_dir if rel_dir else self.root
                wd = libc.inotify_add_watch(self.fd, os.fsencode(str(path)), WATCH_MASK)
                if wd < 0:
                    raise OSError(ctypes.get_errno(), f"inotify_add_watch failed for {rel_dir or '.'}")
                self._wd[wd] = rel_dir
            self._stop_r, self._stop_w = os.pipe()
            self.started_ns = time.time_ns()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            self.established = True
        except OSError as exc:
            self.error = f"{type(exc).__name__}: {exc}"
            self._close()
        return self

    def _drain_once(self) -> bool:
        try:
            buf = os.read(self.fd, 1 << 16)
        except BlockingIOError:
            return False
        except OSError:
            return False
        stamp = time.time_ns()
        offset = 0
        rows = []
        while offset + EVENT_HEADER.size <= len(buf):
            wd, mask, _cookie, length = EVENT_HEADER.unpack_from(buf, offset)
            raw = buf[offset + EVENT_HEADER.size: offset + EVENT_HEADER.size + length]
            name = raw.split(b"\0", 1)[0].decode("utf-8", "surrogateescape")
            offset += EVENT_HEADER.size + length
            directory = self._wd.get(wd)
            rel = None if directory is None else (f"{directory}/{name}" if directory and name else directory or name)
            flags = sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if mask & bit)
            rows.append({"t_ns": stamp, "rel": rel, "dir": bool(mask & IN_ISDIR), "flags": flags})
        with self._lock:
            self._events.extend(rows)
            for row in rows:
                self._flags_seen.update(row["flags"])
        return True

    def _run(self) -> None:
        while True:
            ready, _, _ = select.select([self.fd, self._stop_r], [], [])
            if self._stop_r in ready:
                return
            if self.fd in ready:
                self._drain_once()

    def _close(self) -> None:
        for fd in (self.fd, self._stop_r, self._stop_w):
            if fd >= 0:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self.fd = self._stop_r = self._stop_w = -1

    def stop(self) -> dict[str, Any]:
        """Stop, drain everything still queued by the kernel, and return the ledger record."""
        if self.established:
            os.write(self._stop_w, b"x")
            if self._thread is not None:
                self._thread.join(15)
            while self._drain_once():
                pass
            self.stopped_ns = time.time_ns()
        self._close()
        with self._lock:
            events = list(self._events)
        return {
            "schema": SCHEMA, "mechanism": MECHANISM, "root": str(self.root),
            "established": self.established, "error": self.error,
            "watch_mask": sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if WATCH_MASK & bit),
            "watched_directories": list(self.directories), "tree_files": dict(sorted(self.tree_files.items())),
            "started_ns": self.started_ns, "stopped_ns": self.stopped_ns,
            "overflow": "overflow" in {f for e in events for f in e["flags"]},
            "events": events,
        }


# --------------------------------------------------------------------------------- accounting

def contained_content(text: str, source: str) -> str:
    """How much of `source` appears contiguously in model-visible `text`: exact, partial or none."""
    if not text or not source:
        return "none"
    stripped = source.rstrip("\n")
    views = [text, re.sub(r"(?m)^\s*\d+[\t:|\-] ?", "", text)]
    for view in views:
        if stripped and stripped in view:
            return "exact"
    lines = source.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    floor = min(PARTIAL_SUPPLY_MIN_BYTES, len(stripped.strip().encode("utf-8")))
    for view in views:
        i = 0
        while i < len(lines):
            if not lines[i].strip() or lines[i] not in view:
                i += 1
                continue
            j = i + 1
            while j < len(lines) and "\n".join(lines[i:j + 1]) in view:
                j += 1
            if len("\n".join(lines[i:j]).encode("utf-8")) >= floor:
                return "partial"
            i = j
    return "none"


def _result_texts(events: list[dict[str, Any]]) -> list[tuple[int, str]]:
    """Tool results the model actually received: sequence and text."""
    rows = []
    for event in events:
        if event.get("kind") not in ("tool_action", "resource_access", "mutation", "issue_evidence_access"):
            continue
        payload = event.get("payload") or {}
        if event.get("status") != "result" or payload.get("result_status") != "result":
            continue
        text = payload.get("result_content")
        if isinstance(text, str) and payload.get("result_seen_by_model") is True:
            rows.append((int(event["sequence"]), text))
    return rows


def account(ledger: dict[str, Any] | None, cut_ns: int | None, events: list[dict[str, Any]],
            skills_root: Path, *, extra_errors: list[str] | None = None) -> dict[str, Any]:
    """Exact package accounting from the ledger and model-visible supply. Fail closed."""
    reasons: list[str] = list(extra_errors or [])
    result: dict[str, Any] = {
        "schema": SCHEMA, "mechanism": MECHANISM, "exact": False, "reasons": reasons,
        "cut_ns": cut_ns, "opened_pre_request0": [], "opened_post_request0": [],
        "supplied": {}, "unexplained": [], "consumed_files": {},
    }
    if not isinstance(ledger, dict):
        reasons.append("package-access ledger is absent")
        return result
    if ledger.get("schema") != SCHEMA or ledger.get("mechanism") != MECHANISM:
        reasons.append("package-access ledger has an unknown schema or mechanism")
        return result
    if ledger.get("established") is not True:
        reasons.append(f"package-access ledger was not established: {ledger.get('error')}")
        return result
    if not isinstance(ledger.get("events"), list) or not isinstance(ledger.get("tree_files"), dict):
        reasons.append("package-access ledger is malformed")
        return result
    if ledger.get("overflow"):
        reasons.append("package-access ledger overflowed; access is incomplete")
    tree = ledger["tree_files"]
    opened: dict[str, dict[str, Any]] = {}
    for event in ledger["events"]:
        flags = set(event.get("flags") or [])
        rel = event.get("rel")
        bad = flags - READ_FLAGS - {"overflow"}
        if bad:
            reasons.append(f"package tree changed or lost observation ({sorted(bad)} on {rel!r})")
        if event.get("dir") or rel is None or rel not in tree:
            continue
        if "open" in flags:
            row = opened.setdefault(rel, {"pre": False, "post": False})
            if cut_ns is None or int(event["t_ns"]) < cut_ns:
                row["pre"] = True
            else:
                row["post"] = True
    texts = _result_texts(events)
    host_root = Path(skills_root)
    for rel in sorted(opened):
        row = opened[rel]
        if row["pre"]:
            result["opened_pre_request0"].append(rel)
            parts = rel.split("/")
            if not (len(parts) == 2 and parts[1] == "SKILL.md"):
                result["unexplained"].append({"file": rel, "phase": "pre-request0",
                                              "reason": "runtime opened a non-entrypoint package file before request 0"})
        if row["post"]:
            result["opened_post_request0"].append(rel)
    # Supply: which package files' content reached the model, and through which events.
    supplied: dict[str, dict[str, Any]] = {}
    for rel in sorted(result["opened_post_request0"]):
        try:
            source = (host_root / rel).read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        sequences, best = [], "none"
        for sequence, text in texts:
            match = contained_content(text, source)
            if match != "none":
                sequences.append(sequence)
                best = "exact" if match == "exact" or best == "exact" else "partial"
        if sequences:
            supplied[rel] = {"match": best, "sequences": sequences, "bytes": int(tree[rel]),
                             "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest()}
    # Native consumption (hashline reads, skill:// reads) is judged by the adapter's `consumption`;
    # it must agree with the ledger.
    for event in events:
        payload = event.get("payload") or {}
        consumed = payload.get("consumed_resource") or {}
        if event.get("kind") == "resource_access" and consumed.get("match") in ("exact", "partial"):
            key = f"{consumed.get('logical_root')}/{consumed.get('package_relative_path') or 'SKILL.md'}"
            if key not in opened:
                reasons.append(f"model consumed {key!r} through a native read but the ledger recorded no open")
                continue
            row = supplied.setdefault(key, {"match": consumed["match"], "sequences": [], "bytes": int(tree.get(key, 0)),
                                            "sha256": consumed.get("resource_sha256")})
            row["sequences"].append(int(event["sequence"]))
            if consumed["match"] == "exact":
                row["match"] = "exact"
    for rel in sorted(result["opened_post_request0"]):
        if rel not in supplied:
            result["unexplained"].append({"file": rel, "phase": "post-request0",
                                          "reason": "package file was opened but its content is not shown to have reached the model"})
    result["supplied"] = supplied
    result["consumed_files"] = {rel: row["bytes"] for rel, row in supplied.items()}
    if result["unexplained"]:
        reasons.append("package access not explained by supply: "
                       + ", ".join(f"{u['file']} ({u['phase']})" for u in result["unexplained"]))
    result["exact"] = not reasons
    return result
