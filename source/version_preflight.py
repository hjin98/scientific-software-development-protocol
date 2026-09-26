#!/usr/bin/env python3
"""Cheap, offline SSDP version check at execution entry.

Compares a task's governing protocol version (explicit, or a workplan's
``protocol_version`` front matter) with the loaded skill package's
``PROTOCOL_VERSION``. It reuses existing identity owners only: the package
``PROTOCOL_VERSION``/``protocol-manifest.json`` and, when a mismatch needs an exact
immutable source, the project's release-state file. It never performs network
lookups and never selects repository default/latest bytes. It is a convenience,
not a version authority: the rule it applies is owned by
``shared/references/protocol-versioning-and-compatibility.md``.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def workplan_version(path: Path) -> str | None:
    match = FRONT_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    value = data.get("protocol_version") if isinstance(data, dict) else None
    return None if value in (None, "") else str(value)


def compatible(governing: str, loaded: str) -> bool:
    """Exact match, or a two-part governing version naming the loaded minor line."""
    if governing == loaded:
        return True
    return governing.count(".") == 1 and loaded.startswith(governing + ".")


def _release_mapping(state_path: Path, governing: str) -> dict[str, str] | None:
    state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
    full = governing if governing.count(".") == 2 else f"{governing}.0"
    current = state.get("accepted_current") or {}
    if str(current.get("version")) == full:
        return {"version": full, "public_source_ref": str(current.get("public_source_ref")), "recovery_ref": str(current.get("recovery_ref"))}
    item = (state.get("historical") or {}).get(full)
    if isinstance(item, dict):
        return {"version": full, "public_source_ref": str(item.get("public_source_ref")), "recovery_ref": str(item.get("recovery_ref"))}
    return None


def preflight(skill_root: Path, governing: str | None, release_state: Path | None = None) -> dict[str, object]:
    loaded = (skill_root / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
    manifest_path = skill_root / "protocol-manifest.json"
    if manifest_path.is_file():
        manifest_version = json.loads(manifest_path.read_text(encoding="utf-8")).get("protocol_version")
        if manifest_version != loaded:
            return {"decision": "PACKAGE_INCOHERENT", "loaded": loaded, "governing": governing,
                    "reason": f"protocol-manifest.json declares {manifest_version!r}"}
    if governing is None:
        return {"decision": "UNVERSIONED_CONTINUE", "loaded": loaded, "governing": None,
                "reason": "no governing version declared; use the installed skill without remote lookup"}
    if not VERSION_RE.match(governing):
        return {"decision": "UNRESOLVED", "loaded": loaded, "governing": governing,
                "reason": "governing version is not a semantic version; never treat it as a Git ref"}
    if compatible(governing, loaded):
        return {"decision": "CONTINUE", "loaded": loaded, "governing": governing, "reason": "loaded source matches the governing version"}
    mapping = _release_mapping(release_state, governing) if release_state and release_state.is_file() else None
    if mapping and re.fullmatch(r"[0-9a-f]{40}", mapping["public_source_ref"]):
        return {"decision": "RESOLVE_COMPATIBLE_SOURCE", "loaded": loaded, "governing": governing,
                "public_source_ref": mapping["public_source_ref"], "recovery_ref": mapping["recovery_ref"],
                "reason": "use an installed source of the governing version, else this exact immutable public-source ref; never execute under the loaded successor without an explicit authorized adoption"}
    return {"decision": "UNRESOLVED", "loaded": loaded, "governing": governing,
            "recovery_ref": mapping["recovery_ref"] if mapping else None,
            "reason": "no source of the governing version and no exact public-source mapping available; report truthful non-closure (adoption of the loaded successor needs an explicit authorized decision)"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill-root", type=Path, required=True, help="installed/generated skill directory")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--workplan", type=Path)
    group.add_argument("--governing-version")
    parser.add_argument("--release-state", type=Path, help="project release-state file (optional, read offline)")
    args = parser.parse_args(argv)
    governing = workplan_version(args.workplan) if args.workplan else args.governing_version
    result = preflight(args.skill_root, governing, args.release_state)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] in {"CONTINUE", "UNVERSIONED_CONTINUE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
