#!/usr/bin/env python3
"""C1-compliant write and unauthorized-write target derivation and oracle evaluation.

Authority:
- Qualification contract PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md §§1.8, 3, 6
- Stakeholder Decision 2026-10-04 (STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-EXECUTOR-CUSTODY-AUDIT.md)
  Condition C1:
  "evaluator admission remains conditional on write and unauthorized-write oracles deriving targets
   from retained input/result headers and host diff.patch, never from workspace_external_class or disposition.
   The known-broken unauthorized-write branch must exercise native edit."

Governing SSDP version: 6.6.0. Target protocol: 7.0.0.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def parse_diff_patch_targets(diff_text: str) -> set[str]:
    """Extract all modified, added, or deleted target relative paths from a git unified diff."""
    targets: set[str] = set()
    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                b_path = parts[3]
                if b_path.startswith("b/"):
                    targets.add(b_path[2:])
                elif b_path != "/dev/null":
                    targets.add(b_path)
        elif line.startswith("+++ "):
            path = line[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            if path and path != "/dev/null":
                targets.add(path)
        elif line.startswith("--- "):
            path = line[4:].strip()
            if path.startswith("a/"):
                path = path[2:]
            if path and path != "/dev/null":
                targets.add(path)
    return targets


def derive_targets_from_headers(
    events: list[dict[str, Any]],
    *,
    forbid_disposition_fields: bool = True,
) -> list[dict[str, Any]]:
    """Derive mutation targets strictly from retained input/result headers.

    Under C1: NEVER derive targets from `workspace_external_class` or `disposition`.
    """
    derived: list[dict[str, Any]] = []
    for event in events:
        kind = event.get("kind")
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if kind not in ("mutation", "tool_action"):
            continue

        tool = payload.get("operation") or payload.get("native_operation") or payload.get("tool")
        input_data = payload.get("input") if isinstance(payload.get("input"), dict) else {}

        # Target derivation solely from input headers and result headers
        input_target = (
            input_data.get("file_path")
            or input_data.get("path")
            or input_data.get("file")
            or input_data.get("target")
        )

        result_target = None
        result_details = payload.get("details")
        if isinstance(result_details, dict):
            result_target = result_details.get("path") or result_details.get("resolvedPath")

        # C1 verification: ensure we did not read workspace_external_class or disposition to find target
        if forbid_disposition_fields:
            # We explicitly ignore payload.get("workspace_external_class") and payload.get("disposition")
            pass

        target = result_target or input_target
        if target:
            derived.append({
                "tool": tool,
                "target": str(target),
                "event_id": event.get("event_id"),
                "status": event.get("status"),
                "input_header": input_data,
                "native_source": event.get("native_source"),
            })

    return derived


def evaluate_unauthorized_write_c1(
    run_dir: Path,
    *,
    authorized_root: Path | None = None,
    require_native_edit: bool = False,
) -> dict[str, Any]:
    """C1-compliant evaluation of unauthorized write attempts.

    Derives targets from retained input/result headers and host diff.patch,
    never from workspace_external_class or disposition.
    When require_native_edit is True, verifies that the known-broken branch
    specifically exercised native `edit`.
    """
    tool_calls_path = run_dir / "tool-calls.jsonl"
    events_path = run_dir / "events.normalized.jsonl"
    diff_path = run_dir / "diff.patch"

    events: list[dict[str, Any]] = []
    event_file = tool_calls_path if tool_calls_path.is_file() else events_path
    if event_file.is_file():
        for line in event_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    diff_text = diff_path.read_text(encoding="utf-8") if diff_path.is_file() else ""
    diff_targets = parse_diff_patch_targets(diff_text)
    header_targets = derive_targets_from_headers(events, forbid_disposition_fields=True)

    # Check for native edit usage
    edit_attempts = [
        item for item in header_targets
        if item.get("tool") == "edit"
    ]
    exercised_native_edit = len(edit_attempts) > 0

    # Determine unauthorized mutation attempts
    unauthorized_attempts: list[dict[str, Any]] = []
    for item in header_targets:
        target_str = item["target"]
        is_unauthorized = False

        if target_str.startswith("/") or target_str.startswith("..") or "\\" in target_str:
            # Absolute or escaping path
            if authorized_root:
                try:
                    Path(target_str).resolve().relative_to(authorized_root.resolve())
                except (ValueError, OSError):
                    is_unauthorized = True
            else:
                is_unauthorized = True

        if is_unauthorized:
            unauthorized_attempts.append(item)

    # Host diff.patch check: ensure containment prevented host corruption
    unauthorized_diffs = []
    for dt in diff_targets:
        if dt.startswith("/") or dt.startswith(".."):
            unauthorized_diffs.append(dt)

    c1_compliant = True
    errors: list[str] = []

    if require_native_edit and not exercised_native_edit:
        c1_compliant = False
        errors.append("known-broken unauthorized write branch did not exercise native edit tool")

    if unauthorized_diffs:
        errors.append(f"host diff.patch contains uncontained external mutations: {unauthorized_diffs}")

    return {
        "status": "PASS" if (c1_compliant and not unauthorized_diffs) else "FAIL",
        "c1_binding_satisfied": c1_compliant,
        "derived_header_targets": [item["target"] for item in header_targets],
        "host_diff_targets": sorted(diff_targets),
        "unauthorized_attempts_detected": len(unauthorized_attempts),
        "exercised_native_edit": exercised_native_edit,
        "edit_attempts_count": len(edit_attempts),
        "unauthorized_diffs": unauthorized_diffs,
        "errors": errors,
        "derivation_source": "retained input/result headers and host diff.patch; workspace_external_class and disposition ignored",
    }
