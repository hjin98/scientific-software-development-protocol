#!/usr/bin/env python3
"""Validate the repository-owned mutable SSDP release-state transaction."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = ROOT / "PROTOCOL-RELEASE-STATE.yaml"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
EVIDENCE_RE = re.compile(r"^[^@\s]+@[0-9a-f]{40}:[^#\s]+(?:#.+)?$")
REVIEW_STATES = {"NOT_RUN", "NO_PASS", "PASS"}
RATIFICATION_STATES = {"NOT_REQUESTED", "PENDING", "RATIFIED", "REJECTED"}


def _mapping(value: Any, where: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{where} must be a mapping")
        return {}
    return value


def _sha_or(value: Any, sentinels: set[str], where: str, errors: list[str]) -> str:
    text = str(value or "")
    if text in sentinels or SHA_RE.fullmatch(text):
        return text
    errors.append(f"{where} must be a lowercase 40-hex commit or one of {sorted(sentinels)}")
    return text


def _evidence(value: Any, where: str, errors: list[str], *, required: bool) -> str:
    text = str(value or "")
    if not required and text == "NONE":
        return text
    if not EVIDENCE_RE.fullmatch(text):
        errors.append(f"{where} must be NONE or immutable repository evidence SOURCE@SHA:path[#locator]")
    return text


def _git(root: Path, *args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode, result.stdout.strip()


def _front_matter(text: str, where: str, errors: list[str]) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{where} must begin with YAML front matter")
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"{where} YAML front matter is unterminated")
        return {}
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        errors.append(f"{where} YAML front matter is invalid: {exc}")
        return {}
    return _mapping(data, f"{where} YAML front matter", errors)


def _resolve_evidence_route(
    root: Path,
    project: str,
    value: str,
    where: str,
    errors: list[str],
) -> str | None:
    match = EVIDENCE_RE.fullmatch(value)
    if match is None:
        return None

    source = match.group("source")
    sha = match.group("sha")
    path = match.group("path")
    if source != project:
        errors.append(f"{where} must identify evidence in project {project}, not {source}")
        return None

    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts:
        errors.append(f"{where} path must be repository-relative without parent traversal")
        return None

    code, _ = _git(root, "cat-file", "-e", f"{sha}^{{commit}}")
    if code:
        errors.append(f"{where} commit {sha} is not resolvable")
        return None

    code, content = _git(root, "show", f"{sha}:{path}")
    if code:
        errors.append(f"{where} path {path!r} is not readable at commit {sha}")
        return None
    return content


def _check_review_evidence(
    root: Path,
    project: str,
    value: str,
    semantic_ref: str,
    review_state: str,
    where: str,
    errors: list[str],
) -> None:
    content = _resolve_evidence_route(root, project, value, where, errors)
    if content is None:
        return

    metadata = _front_matter(content, where, errors)
    if not metadata:
        return

    bound_refs = {
        str(metadata[key])
        for key in ("candidate_ref", "semantic_ref", "p1", "p2")
        if metadata.get(key)
    }
    if semantic_ref not in bound_refs:
        rendered = ", ".join(sorted(bound_refs)) if bound_refs else "NONE"
        errors.append(
            f"{where} does not bind candidate.semantic_ref {semantic_ref}; "
            f"review record binds {rendered}"
        )

    expected_status = {"PASS": "pass", "NO_PASS": "no-pass"}[review_state]
    actual_status = str(metadata.get("status") or "").strip().lower().replace("_", "-")
    if actual_status != expected_status:
        errors.append(
            f"{where} disposition {actual_status or 'MISSING'} does not match candidate.review.state {review_state}"
        )


def _check_version_ref(root: Path, version: str, ref: str, where: str, errors: list[str]) -> None:
    if not SHA_RE.fullmatch(ref):
        return
    code, _ = _git(root, "cat-file", "-e", f"{ref}^{{commit}}")
    if code:
        errors.append(f"{where} commit {ref} is not resolvable")
        return
    code, declared = _git(root, "show", f"{ref}:source/PROTOCOL_VERSION")
    if code:
        errors.append(f"{where} commit {ref} has no readable source/PROTOCOL_VERSION")
    elif declared.strip() != version:
        errors.append(f"{where} maps {version} to commit declaring {declared.strip()!r}")


def validate_release_state(data: Any, *, repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = _mapping(data, "release state", errors)
    if root.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if root.get("project") != "hjin98/scientific-software-development-protocol":
        errors.append("project identity is not the SSDP repository")

    accepted = _mapping(root.get("accepted_current"), "accepted_current", errors)
    accepted_version = str(accepted.get("version") or "")
    if not SEMVER_RE.fullmatch(accepted_version):
        errors.append("accepted_current.version must be semantic x.y.z")
    accepted_public = _sha_or(accepted.get("public_source_ref"), set(), "accepted_current.public_source_ref", errors)
    accepted_recovery = _sha_or(accepted.get("recovery_ref"), set(), "accepted_current.recovery_ref", errors)
    if SHA_RE.fullmatch(accepted_public) and accepted_public == accepted_recovery:
        errors.append("accepted_current public_source_ref and recovery_ref must be distinct")

    historical = _mapping(root.get("historical"), "historical", errors)
    for version, record in historical.items():
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            errors.append(f"historical version key {version!r} is not semantic x.y.z")
            continue
        if version == accepted_version:
            errors.append(f"historical[{version}] duplicates accepted_current.version")
        item = _mapping(record, f"historical[{version}]", errors)
        public = _sha_or(item.get("public_source_ref"), {"NONE"}, f"historical[{version}].public_source_ref", errors)
        recovery = _sha_or(item.get("recovery_ref"), {"NONE"}, f"historical[{version}].recovery_ref", errors)
        if SHA_RE.fullmatch(public) and public == recovery:
            errors.append(f"historical[{version}] public_source_ref and recovery_ref must be distinct")
        if repo_root is not None:
            if public != "NONE":
                _check_version_ref(repo_root, version, public, f"historical[{version}].public_source_ref", errors)
            if recovery != "NONE":
                _check_version_ref(repo_root, version, recovery, f"historical[{version}].recovery_ref", errors)

    candidate = _mapping(root.get("candidate"), "candidate", errors)
    candidate_version = str(candidate.get("version") or "")
    if not SEMVER_RE.fullmatch(candidate_version):
        errors.append("candidate.version must be semantic x.y.z")
    semantic_ref = _sha_or(candidate.get("semantic_ref"), {"UNFROZEN"}, "candidate.semantic_ref", errors)
    public_ref = _sha_or(candidate.get("public_source_ref"), {"UNAVAILABLE"}, "candidate.public_source_ref", errors)
    recovery_ref = _sha_or(candidate.get("recovery_ref"), {"UNAVAILABLE"}, "candidate.recovery_ref", errors)

    review = _mapping(candidate.get("review"), "candidate.review", errors)
    review_state = str(review.get("state") or "")
    if review_state not in REVIEW_STATES:
        errors.append(f"candidate.review.state must be one of {sorted(REVIEW_STATES)}")
    review_evidence = _evidence(\n        review.get("evidence_ref"),\n        "candidate.review.evidence_ref",\n        errors,\n        required=review_state in {"NO_PASS", "PASS"},\n    )

    ratification = _mapping(candidate.get("ratification"), "candidate.ratification", errors)
    ratification_state = str(ratification.get("state") or "")
    if ratification_state not in RATIFICATION_STATES:
        errors.append(f"candidate.ratification.state must be one of {sorted(RATIFICATION_STATES)}")
    _evidence(
        ratification.get("evidence_ref"),
        "candidate.ratification.evidence_ref",
        errors,
        required=ratification_state in {"RATIFIED", "REJECTED"},
    )

    if review_state in {"NO_PASS", "PASS"} and semantic_ref == "UNFROZEN":
        errors.append(f"Review {review_state} requires a frozen candidate.semantic_ref")
    if ratification_state in {"PENDING", "RATIFIED", "REJECTED"} and review_state != "PASS":
        errors.append(f"{ratification_state} ratification state requires Review PASS for the same candidate")
    if ratification_state in {"PENDING", "RATIFIED", "REJECTED"} and semantic_ref == "UNFROZEN":
        errors.append(f"{ratification_state} ratification state requires a frozen candidate.semantic_ref")
    if public_ref != "UNAVAILABLE":
        if review_state != "PASS" or ratification_state != "RATIFIED":
            errors.append("candidate.public_source_ref requires Review PASS and RATIFIED state")
        if semantic_ref == "UNFROZEN" or public_ref != semantic_ref:
            errors.append("candidate.public_source_ref must equal the exact reviewed/ratified candidate.semantic_ref")
    if recovery_ref != "UNAVAILABLE" and public_ref == "UNAVAILABLE":
        errors.append("candidate.recovery_ref requires an already published public_source_ref")
    if SHA_RE.fullmatch(public_ref) and public_ref == recovery_ref:
        errors.append("candidate.public_source_ref and candidate.recovery_ref must be distinct")

    if accepted_version == candidate_version:
        terminal = (
            review_state == "PASS"
            and ratification_state == "RATIFIED"
            and SHA_RE.fullmatch(public_ref) is not None
            and SHA_RE.fullmatch(recovery_ref) is not None
            and accepted_public == public_ref
            and accepted_recovery == recovery_ref
        )
        if not terminal:
            errors.append(
                "accepted_current cannot equal candidate.version until Review PASS, RATIFIED state, "
                "published exact candidate fallback, distinct recovery, and accepted mapping agreement are complete"
            )

    if repo_root is not None:
        _check_version_ref(repo_root, accepted_version, accepted_public, "accepted_current.public_source_ref", errors)
        _check_version_ref(repo_root, accepted_version, accepted_recovery, "accepted_current.recovery_ref", errors)
        if semantic_ref != "UNFROZEN":
            _check_version_ref(repo_root, candidate_version, semantic_ref, "candidate.semantic_ref", errors)
        if public_ref != "UNAVAILABLE":
            _check_version_ref(repo_root, candidate_version, public_ref, "candidate.public_source_ref", errors)
        if recovery_ref != "UNAVAILABLE":
            _check_version_ref(repo_root, candidate_version, recovery_ref, "candidate.recovery_ref", errors)

    return errors


def load(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--no-git", action="store_true", help="validate state semantics without realizing repository refs")
    args = parser.parse_args()
    path = args.path.resolve()
    try:
        data = load(path)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        print(f"{path}: {exc}")
        return 1
    errors = validate_release_state(data, repo_root=None if args.no_git else ROOT)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"{path}: release state is coherent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
