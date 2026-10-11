"""Assessment-only link-aware integrity reader; frozen executor core is unchanged.

Captured links denote target text, never host referent bytes. Legacy link text
requires the independently hash-verified supervisor inventory. All other complete
run checks remain owned by the original core; only its final integrity segment
is replaced, fail-closed and with separately pinned instrument provenance.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any
import core70
from core70 import (Requirements, ContractError, SCHEMA, EVIDENCE_INTEGRITY_ROOTS, load_json, sha256_file,
                    requirements_snapshot, _require_object, _valid_sha256, _safe_relative_file)

def _evidence_files(run: Path, requirements: Requirements) -> list[Path]:
    roots = list(dict.fromkeys((*EVIDENCE_INTEGRITY_ROOTS, *requirements.artifacts)))
    oracle_path = run / "oracle.json"
    if oracle_path.is_file():
        try:
            oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            oracle = {}
        results = oracle.get("results") if isinstance(oracle, dict) else {}
        if isinstance(results, dict):
            for row in results.values():
                if isinstance(row, dict):
                    for key in ("stdout_artifact", "stderr_artifact"):
                        value = row.get(key)
                        if isinstance(value, str) and value:
                            roots.append(value)
    files: dict[str, Path] = {}
    for name in roots:
        path = run / name
        if (path.is_symlink() or path.is_file()) and path.name != "evidence-integrity.json":
            files[path.relative_to(run).as_posix()] = path
        elif path.is_dir():
            for child in path.rglob("*"):
                if (child.is_symlink() or child.is_file()) and child.name != "evidence-integrity.json":
                    files[child.relative_to(run).as_posix()] = child
    return [files[key] for key in sorted(files)]


def _link_path(run: Path, rel: Any) -> Path | None:
    """Locate an object without allowing a symlink ancestor or following its target."""
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
        return None
    path = run / rel
    for parent in path.parents:
        if parent == run:
            return path
        if parent.is_symlink():
            return None
    return None


def _captured_links(run: Path, rows: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Authenticate the supervisor's legacy link inventory before interpreting it."""
    name = "final-tree-symlinks.json"
    path = _link_path(run, name)
    meta = [r for r in rows if isinstance(r, dict) and r.get("path") == name]
    if path is None or path.is_symlink() or not path.is_file() or len(meta) != 1:
        return {}, ["captured link inventory is absent, redirected or duplicated"]
    row = meta[0]
    if row.get("bytes") != path.stat().st_size or row.get("sha256") != sha256_file(path):
        return {}, ["captured link inventory hash/size changed"]
    try:
        data = load_json(path)
        entries = data["symlinks"]
        if data.get("schema") != 1 or not isinstance(entries, list):
            raise ValueError()
        links, seen = {}, set()
        for entry in entries:
            rel, target = entry["path"], entry["target"]
            if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                raise ValueError()
            full = "final-tree/" + rel
            candidate = _link_path(run, full)
            if candidate is None or not isinstance(target, str) or rel in seen:
                raise ValueError()
            seen.add(rel)
            # These fixed exclusions are declared by harness70.FINAL_TREE_IGNORE_BASE.
            # Unknown runtime/control exclusions are NOT inferred or silently waived.
            if any(part in {".git", ".qualification-tmp", "__pycache__"} for part in Path(rel).parts):
                continue
            if not candidate.is_symlink() or os.readlink(candidate) != target:
                return {}, ["captured link is missing or its target changed: " + full]
            links[full] = target
        tree = _link_path(run, "final-tree")
        if tree is None or tree.is_symlink() or not tree.is_dir():
            return {}, ["captured final tree is absent or redirected"]
        actual = {p.relative_to(run).as_posix() for p in tree.rglob("*") if p.is_symlink()}
        if actual != set(links):
            return {}, ["captured link inventory differs from actual tree"]
        return links, []
    except (ContractError, KeyError, TypeError, ValueError, OSError):
        return {}, ["captured link inventory is malformed"]


def _integrity_row(run: Path, path: Path) -> dict[str, Any]:
    rel = path.relative_to(run).as_posix()
    if _link_path(run, rel) is None:
        raise ContractError("evidence path traverses a symlink ancestor: " + rel)
    if path.is_symlink():
        target = os.readlink(path)
        content = os.fsencode(target)
        return {"path": rel, "type": "symlink", "target": target,
                "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    return {"path": rel, "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def write_evidence_integrity(run: Path, requirements: Requirements) -> dict[str, Any]:
    identity = _require_object(load_json(run / "run-identity.json"), "run identity")
    snapshot = requirements_snapshot(requirements)
    files = [_integrity_row(run, path) for path in _evidence_files(run, requirements)]
    payload = {
        "schema": SCHEMA,
        "run_identity_sha256": identity.get("identity_sha256"),
        "requirements_content_digests": snapshot["content_digests"],
        "files": files,
        "symlink_accounting": "link-text-v1",
    }
    (run / "evidence-integrity.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def validate_evidence_integrity(run: Path, requirements: Requirements) -> list[str]:
    path = run / "evidence-integrity.json"
    if not path.is_file():
        return ["evidence-integrity.json is missing"]
    try:
        payload = _require_object(load_json(path), "evidence integrity manifest")
        identity = _require_object(load_json(run / "run-identity.json"), "run identity")
    except ContractError as exc:
        return [str(exc)]
    errors: list[str] = []
    if payload.get("schema") != SCHEMA:
        errors.append("evidence integrity schema is unsupported")
    if payload.get("run_identity_sha256") != identity.get("identity_sha256"):
        errors.append("evidence integrity run identity does not match")
    expected_content = requirements_snapshot(requirements)["content_digests"]
    if payload.get("requirements_content_digests") != expected_content:
        errors.append("evidence integrity requirements content does not match")
    rows = payload.get("files")
    if not isinstance(rows, list):
        return errors + ["evidence integrity files list is malformed"]
    link_text = payload.get("symlink_accounting") == "link-text-v1"
    if payload.get("symlink_accounting") not in (None, "link-text-v1"):
        errors.append("evidence integrity symlink accounting is unsupported")
    legacy_links = {}
    if not link_text and ((run / "final-tree-symlinks.json").exists() or any(p.is_symlink() for p in _evidence_files(run, requirements))):
        legacy_links, link_errors = _captured_links(run, rows)
        errors.extend(link_errors)
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"evidence integrity row {index} is not an object")
            continue
        rel = row.get("path")
        raw = _link_path(run, rel)
        if rel in seen:
            errors.append(f"evidence integrity file {rel!r} is duplicated")
        if raw is not None and raw.is_symlink():
            seen.add(rel)
            if link_text:
                if row != _integrity_row(run, raw):
                    errors.append(f"evidence integrity link {rel!r} changed")
            elif rel not in legacy_links:
                errors.append(f"legacy evidence link {rel!r} has no authenticated captured target")
            # Legacy referent bytes were not captured evidence. Its link text is
            # independently authenticated above; never open the host referent.
            continue
        if row.get("type") == "symlink":
            errors.append(f"evidence integrity link {rel!r} was replaced")
        candidate = _safe_relative_file(run, rel) if raw is not None else None
        if candidate is None or not candidate.is_file():
            errors.append(f"evidence integrity file {rel!r} is unavailable")
            continue
        seen.add(rel)
        if row.get("bytes") != candidate.stat().st_size:
            errors.append(f"evidence integrity file {rel!r} size changed")
        if not _valid_sha256(row.get("sha256")) or sha256_file(candidate) != row.get("sha256"):
            errors.append(f"evidence integrity file {rel!r} hash changed")
    expected_paths = {path.relative_to(run).as_posix() for path in _evidence_files(run, requirements)}
    if not link_text:
        # Historical writers omitted directory/dangling links. Their full exact
        # inventory is authenticated by the retained supervisor metadata instead.
        expected_paths -= set(legacy_links) - seen
    if seen != expected_paths:
        missing = sorted(expected_paths - seen)
        extra = sorted(seen - expected_paths)
        if missing:
            errors.append(f"evidence integrity manifest omits files: {missing}")
        if extra:
            errors.append(f"evidence integrity manifest contains unexpected files: {extra}")
    return errors


def validate_complete_run(run: Path, identity: dict, requirements: Requirements) -> list[str]:
    errors = core70.validate_complete_run(run, identity, requirements)
    legacy = core70.validate_evidence_integrity(run, requirements)
    if legacy:
        if len(errors) < len(legacy) or errors[-len(legacy):] != legacy:
            return errors + ["assessment integrity replacement could not locate the exact frozen-core suffix"]
        errors = errors[:-len(legacy)]
    return errors + validate_evidence_integrity(run, requirements)
