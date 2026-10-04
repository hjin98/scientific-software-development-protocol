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
import json
import os
import re
import select
import struct
import threading
import time
from pathlib import Path
from typing import Any

SCHEMA = 2
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
# Bound on distinct (file, flags) rows retained in the ledger. Repeated events fold into one row
# (first/last stamp and count), so a subject's access volume cannot grow the record.
MAX_LEDGER_ROWS = 20000


class LedgerWatcher:
    """Record package access for the lifetime of one subject run. Owned by the supervisor."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.fd = -1
        self._wd: dict[int, str] = {}
        self._rows: dict[tuple, dict[str, Any]] = {}
        self._read_errors: list[str] = []
        self._rows_truncated = False
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
        except OSError as exc:
            # An unexpected read error is ledger loss, never silent: the record reports it.
            with self._lock:
                self._read_errors.append(f"{type(exc).__name__}: {exc}")
            return False
        stamp = time.time_ns()
        offset = 0
        with self._lock:
            while offset + EVENT_HEADER.size <= len(buf):
                wd, mask, _cookie, length = EVENT_HEADER.unpack_from(buf, offset)
                raw = buf[offset + EVENT_HEADER.size: offset + EVENT_HEADER.size + length]
                name = raw.split(b"\0", 1)[0].decode("utf-8", "surrogateescape")
                offset += EVENT_HEADER.size + length
                directory = self._wd.get(wd)
                rel = None if directory is None else (f"{directory}/{name}" if directory and name else directory or name)
                flags = tuple(sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if mask & bit))
                key = (rel, bool(mask & IN_ISDIR), flags)
                row = self._rows.get(key)
                if row is None:
                    if len(self._rows) >= MAX_LEDGER_ROWS:
                        self._rows_truncated = True
                        continue
                    self._rows[key] = {"rel": rel, "dir": key[1], "flags": list(flags),
                                       "first_ns": stamp, "last_ns": stamp, "count": 1}
                else:
                    row["last_ns"] = stamp
                    row["count"] += 1
                self._flags_seen.update(flags)
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
            events = sorted(self._rows.values(), key=lambda r: (r["first_ns"], str(r["rel"])))
            read_errors = list(self._read_errors)
            truncated = self._rows_truncated
        return {
            "schema": SCHEMA, "mechanism": MECHANISM, "root": str(self.root),
            "established": self.established, "error": self.error,
            "watch_mask": sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if WATCH_MASK & bit),
            "watched_directories": list(self.directories), "tree_files": dict(sorted(self.tree_files.items())),
            "started_ns": self.started_ns, "stopped_ns": self.stopped_ns,
            "overflow": "overflow" in {f for e in events for f in e["flags"]},
            "read_errors": read_errors, "rows_truncated": truncated,
            "events": events,
        }


# --------------------------------------------------------------------------------- accounting

_LINE_NUMBER = re.compile(r"(?m)^\s*\d+[\t:|\-] ?")


def _views(text: str) -> list[str]:
    return [text, _LINE_NUMBER.sub("", text)]


def _runs(source: str, views: list[str]):
    """Maximal contiguous runs of source lines that appear verbatim in a view of the output."""
    lines = source.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    for view in views:
        i = 0
        while i < len(lines):
            if not lines[i].strip() or lines[i] not in view:
                i += 1
                continue
            j = i + 1
            while j < len(lines) and "\n".join(lines[i:j + 1]) in view:
                j += 1
            yield "\n".join(lines[i:j])
            i = j


def contained_content(text: str, source: str, *, distinct_in=None) -> tuple[str, bool]:
    """How much of `source` appears contiguously in model-visible `text`.

    Returns (match, distinctive). `match` is exact, partial or none. `distinctive` says that the
    matched content (the whole source for exact, the qualifying run for partial) is contained in
    no other package file, so the match identifies this file rather than a twin or an overlap.
    `distinct_in(block)` answers that question; None treats every match as distinctive.
    """
    if not text or not source:
        return "none", False
    stripped = source.rstrip("\n")
    views = _views(text)
    unique = distinct_in or (lambda block: True)
    if stripped and any(stripped in view for view in views):
        return "exact", bool(unique(stripped))
    floor = min(PARTIAL_SUPPLY_MIN_BYTES, len(stripped.strip().encode("utf-8")))
    found = False
    for run in _runs(source, views):
        if len(run.encode("utf-8")) < floor:
            continue
        found = True
        if unique(run):
            return "partial", True
    return ("partial", False) if found else ("none", False)


def _result_events(events: list[dict[str, Any]]) -> list[tuple[int, str, dict[str, Any]]]:
    """Tool results the model actually received: sequence, text and the producing event."""
    rows = []
    for event in events:
        if event.get("kind") not in ("tool_action", "resource_access", "mutation", "issue_evidence_access"):
            continue
        payload = event.get("payload") or {}
        if event.get("status") != "result" or payload.get("result_status") != "result":
            continue
        text = payload.get("result_content")
        if isinstance(text, str) and payload.get("result_seen_by_model") is True:
            rows.append((int(event["sequence"]), text, event))
    return rows


def _names_path(event: dict[str, Any], rel: str, mount: str | None) -> bool:
    """Does the producing action's own input name this package file (path linkage)?"""
    given = json.dumps((event.get("payload") or {}).get("input"), sort_keys=True, default=str)
    prefix = re.escape(mount.rstrip("/") + "/") if mount else r"(?<![\w.\-])"
    return re.search(prefix + re.escape(rel) + r"(?![\w.\-])", given.replace("\\/", "/")) is not None


def _load_corpus(root: Path, tree: dict[str, Any]) -> dict[str, str]:
    corpus: dict[str, str] = {}
    for rel in tree:
        try:
            corpus[rel] = (root / rel).read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            corpus[rel] = ""
    return corpus


def account(ledger: dict[str, Any] | None, cut_ns: int | None, events: list[dict[str, Any]],
            skills_root: Path, *, extra_errors: list[str] | None = None, delivered: set[str] | None = None,
            owner_name: str | None = None, mount: str | None = None) -> dict[str, Any]:
    """Exact package accounting from the ledger and model-visible supply. Fail closed.

    `exact` answers the byte question (every opened file explained). `owner_read_exact` answers the
    narrower owner-read question: the ledger itself is intact and every opened owner copy is
    explained, whatever happened to unrelated files. `delivered` holds `<root>/SKILL.md` entries
    whose full content reached the model through the hash-linked request 0.
    """
    delivered = set(delivered or ())
    global_reasons: list[str] = list(extra_errors or [])
    result: dict[str, Any] = {
        "schema": SCHEMA, "mechanism": MECHANISM, "exact": False, "owner_read_exact": False, "reasons": global_reasons,
        "cut_ns": cut_ns, "opened_pre_request0": [], "opened_post_request0": [],
        "supplied": {}, "explained_by_delivery": [], "unexplained": [], "consumed_files": {},
    }
    if not isinstance(ledger, dict):
        global_reasons.append("package-access ledger is absent")
        return result
    if ledger.get("schema") != SCHEMA or ledger.get("mechanism") != MECHANISM:
        global_reasons.append("package-access ledger has an unknown schema or mechanism")
        return result
    if ledger.get("established") is not True:
        global_reasons.append(f"package-access ledger was not established: {ledger.get('error')}")
        return result
    if not isinstance(ledger.get("events"), list) or not isinstance(ledger.get("tree_files"), dict):
        global_reasons.append("package-access ledger is malformed")
        return result
    if ledger.get("overflow"):
        global_reasons.append("package-access ledger overflowed; access is incomplete")
    if ledger.get("read_errors"):
        global_reasons.append(f"package-access ledger lost events to read errors: {ledger['read_errors'][:3]}")
    if ledger.get("rows_truncated"):
        global_reasons.append("package-access ledger exceeded its retained-row bound")
    tree = ledger["tree_files"]
    opened: dict[str, dict[str, bool]] = {}
    for event in ledger["events"]:
        flags = set(event.get("flags") or [])
        rel = event.get("rel")
        bad = flags - READ_FLAGS - {"overflow"}
        if bad:
            global_reasons.append(f"package tree changed or lost observation ({sorted(bad)} on {rel!r})")
        if event.get("dir") or rel is None or rel not in tree:
            continue
        if "open" in flags:
            row = opened.setdefault(rel, {"pre": False, "post": False})
            if cut_ns is None or int(event["first_ns"]) < cut_ns:
                row["pre"] = True
            if cut_ns is not None and int(event["last_ns"]) >= cut_ns:
                row["post"] = True
    host_root = Path(skills_root)
    corpus = _load_corpus(host_root, tree)
    distinct_cache: dict[str, dict[str, bool]] = {}

    def distinct_for(rel: str):
        cache = distinct_cache.setdefault(rel, {})

        def distinct(block: str) -> bool:
            if block not in cache:
                cache[block] = not any(block in other for name, other in corpus.items() if name != rel and other)
            return cache[block]
        return distinct

    texts = _result_events(events)
    # Supply: which package files' content reached the model, through which events. Matching is
    # independent of the request-0 phase, so clock skew can change an exactness label but never
    # the counted bytes. A match counts only when it identifies the opened file: the matched
    # content is distinctive among package files, or the producing action's input names the file.
    supplied: dict[str, dict[str, Any]] = {}
    for rel in sorted(opened):
        source = corpus.get(rel, "")
        if not source:
            continue
        sequences, best = [], "none"
        for sequence, text, event in texts:
            match, distinctive = contained_content(text, source, distinct_in=distinct_for(rel))
            if match == "none":
                continue
            if not distinctive and not _names_path(event, rel, mount):
                continue
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
                global_reasons.append(f"model consumed {key!r} through a native read but the ledger recorded no open")
                continue
            row = supplied.setdefault(key, {"match": consumed["match"], "sequences": [], "bytes": int(tree.get(key, 0)),
                                            "sha256": consumed.get("resource_sha256")})
            row["sequences"].append(int(event["sequence"]))
            if consumed["match"] == "exact":
                row["match"] = "exact"
    unexplained: list[dict[str, Any]] = []
    for rel in sorted(opened):
        row = opened[rel]
        parts = rel.split("/")
        if row["pre"]:
            result["opened_pre_request0"].append(rel)
            if not (len(parts) == 2 and parts[1] == "SKILL.md"):
                unexplained.append({"file": rel, "phase": "pre-request0",
                                    "reason": "runtime opened a non-entrypoint package file before request 0"})
        if row["post"]:
            result["opened_post_request0"].append(rel)
            if rel in delivered:
                result["explained_by_delivery"].append(rel)
            elif rel not in supplied:
                unexplained.append({"file": rel, "phase": "post-request0",
                                    "reason": "package file was opened but its content is not shown to have reached the model"})
    result["supplied"] = supplied
    result["unexplained"] = unexplained
    result["consumed_files"] = {rel: row["bytes"] for rel, row in supplied.items()}
    reasons = list(global_reasons)
    if unexplained:
        reasons.append("package access not explained by supply: "
                       + ", ".join(f"{u['file']} ({u['phase']})" for u in unexplained))
    result["reasons"] = reasons
    result["exact"] = not reasons
    owner_blocked = owner_name is None or any(u["file"].rsplit("/", 1)[-1] == owner_name for u in unexplained)
    result["owner_read_exact"] = not global_reasons and not owner_blocked
    return result
