#!/usr/bin/env python3
"""H1 consumed package bytes (contract v2 section 3), replacing the retired package-access ledger.

6.6's `entry_and_burden` accounting: the bytes of every invoked SSDP entrypoint as installed plus the bytes of SSDP
files read. Reads come from native read events; every shell command that names the package path is counted
conservatively as a full read of every file it can reach (a named file, every file under a named directory, every
file a glob matches). The count is therefore an upper bound whenever a shell command touched the package.
"""
from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

MOUNT = "/opt/ssdp/skills/"
SELECTOR_SUFFIX = re.compile(r":(?:raw|\d+(?:[-+]\d*)?(?:,\d+(?:[-+]\d*)?)*)$")
_NAMED = re.compile(re.escape(MOUNT) + r"([^\s'\"`;|&<>(){}$,]*)")


def is_owner_copy(rel: str, owner_name: str | None) -> bool:
    return owner_name is not None and rel.rsplit("/", 1)[-1] == owner_name


def native_owner_target(event: dict[str, Any], owner_name: str | None) -> bool:
    """A native read that consumed (exactly or partly) an owner copy, after selector stripping."""
    payload = event.get("payload") or {}
    consumed = payload.get("consumed_resource") or {}
    if event.get("kind") != "resource_access" or consumed.get("match") not in ("exact", "partial"):
        return False
    targets = (consumed.get("package_relative_path"), payload.get("resolved_resource_path"), payload.get("resource_identity"))
    return any(isinstance(t, str) and is_owner_copy(SELECTOR_SUFFIX.sub("", t), owner_name) for t in targets)


def shell_reach(command: str, tree: dict[str, int]) -> set[str]:
    """Package files a shell command can reach through the package path it names (conservative)."""
    reached: set[str] = set()
    for match in _NAMED.finditer(command.replace("\\/", "/")):
        named = match.group(1).strip("/")
        if any(ch in named for ch in "*?["):
            reached |= {rel for rel in tree if fnmatch.fnmatch(rel, named)}
        elif named in tree:
            reached.add(named)
        else:  # a directory, the package root, or a path that cannot be matched: everything below it
            reached |= {rel for rel in tree if not named or rel.startswith(named + "/")}
    return reached


def account(events: list[dict[str, Any]], skills_root: Path, owner_name: str | None) -> dict[str, Any]:
    tree = {p.relative_to(skills_root).as_posix(): p.stat().st_size for p in Path(skills_root).rglob("*") if p.is_file()}
    native: dict[str, int] = {}
    owner: list[dict[str, Any]] = []
    shell: dict[str, int] = {}
    for event in events:
        payload = event.get("payload") or {}
        if event.get("kind") == "resource_access" and payload.get("result_status") == "result":
            path = payload.get("resolved_resource_path")
            if (payload.get("consumed_resource") or {}).get("match") in ("exact", "partial") and isinstance(path, str) and path.startswith(MOUNT):
                native[path.removeprefix(MOUNT)] = payload["resource_bytes"]
        if native_owner_target(event, owner_name):
            owner.append({"sequence": int(event["sequence"]), "event_id": event.get("event_id"), "source": "native-read"})
        if event.get("kind") == "tool_action" and "process_execution" in payload.get("semantic_capability_classes", []):
            reached = shell_reach(json.dumps(payload.get("input"), default=str), tree)
            shell.update({rel: tree[rel] for rel in reached})
            if any(is_owner_copy(rel, owner_name) for rel in reached):
                owner.append({"sequence": int(event["sequence"]), "event_id": event.get("event_id"), "source": "shell-touch"})
    return {"native_files": native, "shell_files": shell, "owner_read_observed": owner, "owner_minor_exposure": [],
            "conservative": bool(shell)}
