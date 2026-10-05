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
import tempfile
from pathlib import Path
from typing import Any

SCHEMA = 3
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
PARAMETERS = {
    "distinctiveness_floor": 48, "owner_line_floor": 48, "owner_load_quantum": 256,
    "clock_tolerance_ns": 5_000_000, "bracket_width_bound_ns": 500_000_000,
    "heartbeat_period_ns": 50_000_000, "heartbeat_gap_bound_ns": 250_000_000,
    "row_bound": MAX_LEDGER_ROWS, "marks_before_launch": True, "marks_after_teardown": True,
}


class LedgerWatcher:
    """Record package access for the lifetime of one subject run. Owned by the supervisor."""

    def __init__(self, root: Path, parameters: dict[str, Any] | None = None):
        self.root = Path(root)
        self.parameters = dict(PARAMETERS if parameters is None else parameters)
        self._heartbeat_dir = None
        self._heartbeat_wd = -1
        self._heartbeats: list[dict[str, Any]] = []
        self._interval = -1
        self._heartbeat_stop = threading.Event()
        self._heartbeat_thread = None
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
            self._heartbeat_dir = tempfile.TemporaryDirectory(prefix="ssdp-ledger-heartbeat-")
            self._heartbeat_wd = libc.inotify_add_watch(self.fd, os.fsencode(self._heartbeat_dir.name), IN_CREATE)
            if self._heartbeat_wd < 0:
                raise OSError(ctypes.get_errno(), "heartbeat mark failed")
            self._stop_r, self._stop_w = os.pipe()
            self.started_ns = time.time_ns()
            self._heartbeat()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            self._heartbeat_thread = threading.Thread(target=self._pulse, daemon=True)
            self._heartbeat_thread.start()
            self.established = True
        except OSError as exc:
            self.error = f"{type(exc).__name__}: {exc}"
            self._close()
        return self

    def _heartbeat(self) -> None:
        # Only IN_CREATE is marked. Unique filenames forbid kernel coalescing across intervals.
        with self._lock:
            index = len(self._heartbeats)
            row = {"index": index, "before_mono_ns": time.monotonic_ns(), "before_ns": time.time_ns()}
            fd = os.open(Path(self._heartbeat_dir.name) / str(index), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            row.update(after_ns=time.time_ns(), after_mono_ns=time.monotonic_ns())
            self._heartbeats.append(row)

    def _pulse(self) -> None:
        while not self._heartbeat_stop.wait(self.parameters["heartbeat_period_ns"] / 1e9):
            try:
                self._heartbeat()
            except OSError as exc:
                with self._lock:
                    self._read_errors.append(f"heartbeat: {exc}")
                return

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
                if wd == self._heartbeat_wd:
                    self._interval = int(name)
                    continue
                directory = self._wd.get(wd)
                rel = None if directory is None else (f"{directory}/{name}" if directory and name else directory or name)
                flags = tuple(sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if mask & bit))
                self._flags_seen.update(flags)
                key = (rel, bool(mask & IN_ISDIR), flags, self._interval)
                row = self._rows.get(key)
                if row is None:
                    if len(self._rows) >= self.parameters["row_bound"]:
                        self._rows_truncated = True
                        continue
                    self._rows[key] = {"rel": rel, "dir": key[1], "flags": list(flags),
                                       "interval": self._interval,
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
            self._heartbeat_stop.set()
            self._heartbeat_thread.join(15)
            self._heartbeat()
            os.write(self._stop_w, b"x")
            if self._thread is not None:
                self._thread.join(15)
            while self._drain_once():
                pass
            self.stopped_ns = time.time_ns()
        self._close()
        if self._heartbeat_dir is not None:
            self._heartbeat_dir.cleanup()
        with self._lock:
            events = sorted(self._rows.values(), key=lambda r: (r["interval"], str(r["rel"]), r["flags"]))
            read_errors = list(self._read_errors)
            truncated = self._rows_truncated
        return {
            "schema": SCHEMA, "mechanism": MECHANISM, "root": str(self.root),
            "established": self.established, "error": self.error,
            "watch_mask": sorted(FLAG_NAMES[bit] for bit in FLAG_NAMES if WATCH_MASK & bit),
            "watched_directories": list(self.directories), "tree_files": dict(sorted(self.tree_files.items())),
            "started_ns": self.started_ns, "stopped_ns": self.stopped_ns,
            "overflow": "overflow" in self._flags_seen,
            "read_errors": read_errors, "rows_truncated": truncated,
            "parameters": self.parameters, "heartbeats": self._heartbeats,
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


def contained_content(text: str, source: str, *, distinct_in=None, floor_bytes=PARTIAL_SUPPLY_MIN_BYTES) -> tuple[str, bool]:
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
    floor = min(floor_bytes, len(stripped.strip().encode("utf-8")))
    found = False
    for run in _runs(source, views):
        if len(run.encode("utf-8")) < floor:
            continue
        found = True
        if unique(run):
            return "partial", True
    return ("partial", False) if found else ("none", False)


def _result_events(events: list[dict[str, Any]], *, errors=False) -> list[tuple[int, str, dict[str, Any]]]:
    """Tool results the model actually received: sequence, text and the producing event."""
    rows = []
    for event in events:
        if event.get("kind") not in ("tool_action", "resource_access", "mutation", "issue_evidence_access"):
            continue
        payload = event.get("payload") or {}
        if event.get("status") not in (("result", "error") if errors else ("result",)) or payload.get("result_status") not in (("result", "error") if errors else ("result",)):
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


def is_owner_copy(rel: str, owner_name: str | None) -> bool:
    """One basename rule, shared with native read recognition."""
    return owner_name is not None and rel.rsplit("/", 1)[-1] == owner_name


SELECTOR_SUFFIX = re.compile(r":(?:raw|\d+(?:[-+]\d*)?(?:,\d+(?:[-+]\d*)?)*)$")


def native_owner_target(event: dict[str, Any], owner_name: str | None) -> bool:
    """The one test for a native read of an owner copy: consumed content (exact or partial) whose package path,
    resolved path or resource identity, after selector stripping, is an owner copy. Shared by the ledger accounting
    and the adapter, so the two owner-read records cannot disagree about which native reads count."""
    payload = event.get("payload") or {}
    consumed = payload.get("consumed_resource") or {}
    if event.get("kind") != "resource_access" or consumed.get("match") not in ("exact", "partial"):
        return False
    targets = (consumed.get("package_relative_path"), payload.get("resolved_resource_path"), payload.get("resource_identity"))
    return any(isinstance(t, str) and is_owner_copy(SELECTOR_SUFFIX.sub("", t), owner_name) for t in targets)


def owner_supply(events, corpus, owner_name, parameters):
    lines = {line for rel, text in corpus.items() if is_owner_copy(rel, owner_name)
             for line in text.splitlines() if len(line.encode()) >= parameters["owner_line_floor"]}
    positive, minor = [], []
    for seq, text, event in _result_events(events, errors=True):
        matched = {line for line in lines if any(line in output for output in text.splitlines())}
        if not matched:
            continue
        row = {"sequence": seq, "event_id": event.get("event_id"), "distinct_lines": len(matched),
               "bytes": sum(len(line.encode()) for line in matched), "source": "owner-class-supply"}
        (positive if len(matched) >= 2 and row["bytes"] >= parameters["owner_load_quantum"] else minor).append(row)
    for event in events:
        if native_owner_target(event, owner_name):
            positive.append({"sequence": int(event["sequence"]), "event_id": event.get("event_id"), "source": "native-read"})
    return positive, minor


def candidate_window(lower, upper, requests, events, lost=False):
    """Trace-ordered positions, never request stamps sorted by numeric time."""
    start = min((e["sequence"] for e in events), default=1)
    end = max((e["sequence"] for e in events), default=start)
    if lost or lower is None or upper is None:
        return {"start": start, "end": end, "timing_loss": True}
    earlier = [r for r in requests if r["t_ns"] < lower]
    later = [r for r in requests if r["t_ns"] > upper]

    def position(request):          # a request with no derivable, verified position (text-only turn, failed pairing) has None
        value = request.get("position")
        return value if isinstance(value, int) and not isinstance(value, bool) else None

    # Lower side: an absent or unpositioned earlier request starts the window at the beginning of the trace.
    lo = position(earlier[-1]) if earlier and position(earlier[-1]) is not None else start
    # Upper side: an unpositioned later request bounds nothing, so the window runs to the end of the trace.
    hi = position(later[0]) - 1 if later and position(later[0]) is not None else end
    if hi < lo:
        lo, hi = start, end         # an otherwise empty window is the whole trace (D3 window-end clarification)
    return {"start": lo, "end": hi, "timing_loss": False}


def timing(ledger, requests, parameters):
    """Derive loss from raw paired clocks against one fixed baseline; never trust drain times."""
    beats = ledger.get("heartbeats") or []
    if not isinstance(beats, list):
        return {}, ["malformed heartbeats"]
    tolerance = parameters["clock_tolerance_ns"]
    reasons, brackets = [], {}
    baseline = None
    tainted = False
    for i, beat in enumerate(beats):
        try:
            if not isinstance(beat, dict) or beat["index"] != i:
                raise ValueError("heartbeat order")
            offset = beat["before_ns"] - beat["before_mono_ns"]
            baseline = offset if baseline is None else baseline
            if (abs(offset - baseline) > tolerance
                    or abs(beat["after_ns"] - beat["after_mono_ns"] - baseline) > tolerance):
                tainted = True
                reasons.append(f"clock divergence at heartbeat {i}")
            if i:
                previous = beats[i-1]
                lower = previous["before_ns"] - tolerance
                upper = beat["after_ns"] + tolerance
                gap = beat["before_mono_ns"] - previous["after_mono_ns"]
                lost = tainted
                if gap > parameters["heartbeat_gap_bound_ns"] or gap < 0:
                    reasons.append(f"heartbeat gap at interval {i-1}")
                    lost = True
                if upper - lower > parameters["bracket_width_bound_ns"] or upper < lower:
                    reasons.append(f"bracket width at interval {i-1}")
                    lost = True
                brackets[i-1] = {"lower_ns": lower, "upper_ns": upper, "timing_loss": lost}
        except (KeyError, TypeError, ValueError):
            tainted = True
            reasons.append(f"malformed heartbeat {i}")
    if len(beats) < 2:
        reasons.append("heartbeat bracket ends missing")
    previous = None
    for request in requests:
        rt, mono = request.get("t_ns"), request.get("monotonic_ns")
        if (not isinstance(rt, int) or not isinstance(mono, int) or baseline is None
                or abs(rt-mono-baseline) > tolerance
                or (previous is not None and (rt < previous[0] or mono < previous[1]))):
            reasons.append("request stamps decrease or disagree with heartbeat baseline")
        if isinstance(rt, int) and isinstance(mono, int):
            previous = (rt, mono)
    # Request clock loss taints every window, never moves its beginning forward.
    if any("request stamps" in r for r in reasons):
        for bracket in brackets.values():
            bracket["timing_loss"] = True
    return brackets, sorted(set(reasons))


def account(ledger: dict[str, Any] | None, cut_ns: int | None, events: list[dict[str, Any]],
            skills_root: Path, *, extra_errors: list[str] | None = None, delivered: set[str] | None = None,
            owner_name: str | None = None, mount: str | None = None,
            request_stamps: dict[int, int] | None = None, request_records: list[dict[str, Any]] | None = None,
            parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    """Revision 8: supply proves positives; intact ledger and conservative windows permit negatives."""
    params = dict(PARAMETERS if parameters is None else parameters)
    # Coverage/correspondence is derived by the adapter from retained raw evidence.
    # Missing or malformed metadata cannot enable the window-dependent supply route.
    records_valid = isinstance(request_records, list) and all(isinstance(r, dict) for r in request_records)
    requests = list(request_records) if records_valid else []
    pairing_verified = bool(requests) and all(
        r.get("pairing_verified") is True and "position" in r
        and (r["position"] is None or type(r["position"]) is int)
        for r in requests)
    delivered = set(delivered or ())
    global_reasons = list(extra_errors or [])
    # Even a lost/absent ledger must not suppress content that demonstrably reached the model.
    tree = {p.relative_to(skills_root).as_posix(): p.stat().st_size for p in Path(skills_root).rglob("*") if p.is_file()}
    corpus = _load_corpus(Path(skills_root), tree)
    positive, minor = owner_supply(events, corpus, owner_name, params)
    result = {"schema": SCHEMA, "mechanism": MECHANISM, "parameters": params,
              "exact": False, "owner_floor_exact": False, "reasons": global_reasons,
              "cut_ns": cut_ns, "request_records": requests,
              "route_iii_available": pairing_verified,
              "route_iii_unavailable_reason": None if pairing_verified else "request/assistant-turn pairing is not verified",
              "opened_pre_request0": [], "opened_post_request0": [], "supplied": {},
              "explained_by_delivery": [], "unexplained": [], "consumed_files": {}, "opened_files": [],
              "owner_read_observed": positive, "owner_minor_exposure": minor, "owner_open_windows": [],
              "active_ssdp_bytes": None, "timing_reasons": []}
    if not isinstance(ledger, dict):
        global_reasons.append("package-access ledger is absent")
        return result
    if ledger.get("schema") != SCHEMA or ledger.get("mechanism") != MECHANISM:
        global_reasons.append("package-access ledger has an unknown schema or mechanism")
        return result
    if ledger.get("established") is not True:
        global_reasons.append(f"package-access ledger was not established: {ledger.get('error')}")
    if not isinstance(ledger.get("events"), list) or not isinstance(ledger.get("tree_files"), dict):
        global_reasons.append("package-access ledger is malformed")
        return result
    if ledger.get("tree_files") != tree:
        global_reasons.append("package-access ledger tree differs from installed package")
    if ledger.get("parameters") != params:
        global_reasons.append("package-access ledger parameters differ from frozen profile")
    for key, reason in (("overflow", "overflowed"), ("read_errors", "lost events to read errors"),
                        ("rows_truncated", "exceeded its retained-row bound")):
        if ledger.get(key):
            global_reasons.append(f"package-access ledger {reason}")
    brackets, timing_reasons = timing(ledger, requests, params)
    if cut_ns is not None and not requests:
        timing_reasons.append("request stamps missing")
        for bracket in brackets.values():
            bracket["timing_loss"] = True
    result["timing_reasons"] = timing_reasons
    opened = {}
    owner_rows = []
    ledger_events = ledger["events"]
    if (any(not isinstance(e, dict) or not isinstance(e.get("flags"), list)
            or not all(isinstance(f, str) for f in e["flags"])
            or not isinstance(e.get("rel"), (str, type(None)))
            or not isinstance(e.get("interval"), int) or isinstance(e.get("interval"), bool)
            or not isinstance(e.get("count"), int) or isinstance(e.get("count"), bool) or e["count"] < 1
            for e in ledger_events) or len(ledger_events) > params["row_bound"]):
        global_reasons.append("package-access ledger has malformed or excessive rows")
        return result
    for event in ledger_events:
        flags = set(event.get("flags") or [])
        rel = event.get("rel")
        bad = flags - READ_FLAGS - {"overflow"}
        if bad:
            global_reasons.append(f"package tree changed or lost observation ({sorted(bad)} on {rel!r})")
        if event.get("dir") or rel not in tree or "open" not in flags:
            continue
        bracket = brackets.get(event.get("interval"), {"lower_ns": None, "upper_ns": None, "timing_loss": True})
        lower, upper = bracket["lower_ns"], bracket["upper_ns"]
        lost = bracket["timing_loss"]
        if lower is None:
            timing_reasons.append(f"open without heartbeat bracket: {rel}")
        window = candidate_window(lower, upper, requests, events, lost)
        pre = cut_ns is None or lower is None or lower < cut_ns
        post = cut_ns is not None and (upper is None or upper >= cut_ns)
        if pre:
            window["start"] = min((e["sequence"] for e in events), default=1)
        row = {"file": rel, "bytes": tree[rel], "sha256": hashlib.sha256((Path(skills_root)/rel).read_bytes()).hexdigest(),
               "interval": event.get("interval"), "bracket": bracket, "window": window, "count": event.get("count"),
               "pre": pre, "post": post, "read": any(e.get("rel") == rel and e.get("interval") == event.get("interval")
                                                   and "access" in e.get("flags", []) for e in ledger["events"])}
        opened.setdefault(rel, []).append(row)
        result["opened_files"].append(row)
        if is_owner_copy(rel, owner_name):
            owner_rows.append(row)
    supplied = {}
    texts = _result_events(events)
    distinct_cache = {}
    def distinct_for(rel):
        def distinct(block):
            key = (rel, block)
            if key not in distinct_cache:
                distinct_cache[key] = not any(block in text for name, text in corpus.items() if name != rel)
            return distinct_cache[key]
        return distinct
    for rel, rows in opened.items():
        source = corpus.get(rel, "")
        sequences, routes, ids, best = [], [], [], "none"
        for sequence, text, event in texts:
            match, distinctive = contained_content(text, source, distinct_in=distinct_for(rel), floor_bytes=params["distinctiveness_floor"])
            if match == "none":
                continue
            route = None
            if distinctive and len(source.rstrip("\n").encode()) >= params["distinctiveness_floor"]:
                route = "distinctive"
            elif _names_path(event, rel, mount):
                route = "path-linked"
            elif pairing_verified and match == "exact" and len(source.encode()) >= params["distinctiveness_floor"] and any(
                    r["window"]["start"] <= sequence <= r["window"]["end"] for r in rows):
                route = "whole-file-in-window"
            if route:
                sequences.append(sequence); routes.append(route); ids.append(event.get("event_id"))
                best = "exact" if match == "exact" or best == "exact" else "partial"
        if sequences:
            supplied[rel] = {"match": best, "sequences": sequences, "event_ids": ids, "routes": routes,
                             "bytes": tree[rel], "sha256": rows[0]["sha256"]}
    for event in events:
        consumed = (event.get("payload") or {}).get("consumed_resource") or {}
        if event.get("kind") == "resource_access" and consumed.get("match") in ("exact", "partial"):
            rel = f"{consumed.get('logical_root')}/{consumed.get('package_relative_path') or 'SKILL.md'}"
            if rel not in opened:
                global_reasons.append(f"model consumed {rel!r} through a native read but the ledger recorded no open")
                continue
            row = supplied.setdefault(rel, {"match": consumed["match"], "sequences": [], "event_ids": [],
                                             "routes": [], "bytes": tree[rel], "sha256": opened[rel][0]["sha256"]})
            row["sequences"].append(event["sequence"]); row["event_ids"].append(event.get("event_id")); row["routes"].append("native")
    unexplained = []
    for rel, rows in opened.items():
        for row in rows:
            row["explanation"] = "delivered" if rel in delivered else "supplied" if rel in supplied else "unexplained"
            if row["pre"]:
                result["opened_pre_request0"].append(rel)
                if not (len(rel.split("/")) == 2 and rel.endswith("/SKILL.md")):
                    unexplained.append({"file": rel, "phase": "pre-request0", "reason": "runtime opened a non-entrypoint package file before request 0"})
            if row["post"]:
                result["opened_post_request0"].append(rel)
                if rel in delivered:
                    result["explained_by_delivery"].append(rel)
                elif rel not in supplied:
                    unexplained.append({"file": rel, "phase": "post-request0", "reason": "content not shown supplied"})
    for field in ("opened_pre_request0", "opened_post_request0", "explained_by_delivery"):
        result[field] = sorted(set(result[field]))
    result.update(supplied=supplied, unexplained=unexplained,
                  consumed_files={rel: row["bytes"] for rel, row in supplied.items()}, owner_open_windows=owner_rows)
    result["reasons"] = list(global_reasons)
    if unexplained:
        result["reasons"].append("package access not explained by supply: " + ", ".join(u["file"] for u in unexplained))
    result["exact"] = not result["reasons"]
    result["owner_floor_exact"] = not global_reasons and owner_name is not None and not (owner_rows and timing_reasons)
    if result["exact"]:
        counted = dict(result["consumed_files"])
        counted.update({rel: tree[rel] for rel in delivered if rel in tree})
        result["active_ssdp_bytes"] = sum(counted.values())
    return result
