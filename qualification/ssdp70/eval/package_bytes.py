#!/usr/bin/env python3
"""H1 consumed package bytes (contract v2 section 3), replacing the retired package-access ledger.

6.6's `entry_and_burden` accounting: the bytes of every invoked SSDP entrypoint as installed plus the bytes of SSDP
files read. Reads come from native read events; every shell command that names the package path is counted
conservatively as a full read of every file it can reach (a named file, every file under a named directory, every
file a glob matches). The count is an upper bound for any access that names the package path or could assemble it from `/opt` or `ssdp`; a path built without ever writing those (a declared residual) is not detected.
"""
from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import Any

MOUNT = "/opt/ssdp/skills/"
SELECTOR_SUFFIX = re.compile(r":(?:raw|\d+(?:[-+]\d*)?(?:,\d+(?:[-+]\d*)?)*)$")
_NAMED = re.compile(r"/opt/ssdp(?P<skills>/skills)?(?P<rest>[^\s'\"`;|&<>(){}$,]*)")
_OBFUSCATED = re.compile(r"(?i)/opt\b|ssdp")
_ROOTISH = re.compile(r"""(?m)(?:^|[\s'"=:])(?:/|/opt(?:/[^\s'"]*)?)(?=$|[\s'"])""")   # a bare "/" or an /opt path given to a native tool


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


def _text(value: Any) -> str:
    """Every string inside a tool input, joined: the command itself, not its JSON escaping."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return "\n".join(_text(v) for v in value)
    return ""


def shell_reach(command: str, tree: dict[str, int], *, process: bool = True) -> set[str]:
    """Package files an action can reach (conservative). A path under the package is that file or everything below it;
    the package parent, a `..` beside a package path, or (for a process) any text that could assemble the path
    (`/opt`, `ssdp`) reaches the whole package."""
    reached: set[str] = set()
    named = False
    for match in _NAMED.finditer(command):
        named = True
        rest = match.group("rest").strip("/")
        if not match.group("skills") or ".." in rest or ".." in command:
            return set(tree)
        if any(ch in rest for ch in "*?["):
            reached |= {rel for rel in tree if fnmatch.fnmatch(rel, rest)}
        elif rest in tree:
            reached.add(rest)
        else:  # a directory, the package root, or an unmatched path: everything below it
            reached |= {rel for rel in tree if not rest or rel.startswith(rest + "/")}
    if not named and (_OBFUSCATED if process else _ROOTISH).search(command):
        return set(tree)
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
        if event.get("kind") not in ("tool_action", "resource_access"):
            continue
        process = "process_execution" in payload.get("semantic_capability_classes", [])
        reached = shell_reach(_text(payload.get("input")), tree, process=process)
        # a native action over the package (grep, glob, list) is counted like a shell command; a plain read of a named file adds nothing new
        shell.update({rel: tree[rel] for rel in reached if rel not in native})
        pending_read = event.get("kind") == "resource_access" and event.get("status") == "start"   # its result event carries the observation
        if any(is_owner_copy(rel, owner_name) for rel in reached) and not native_owner_target(event, owner_name) and not pending_read:
            owner.append({"sequence": int(event["sequence"]), "event_id": event.get("event_id"), "source": "shell-touch"})
    return {"native_files": native, "shell_files": shell, "owner_read_observed": owner, "owner_minor_exposure": [],
            "conservative": bool(shell)}
