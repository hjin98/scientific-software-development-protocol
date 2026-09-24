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
SEMVER_RE = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")
EVIDENCE_RE = re.compile(
    r"^(?P<source>[^@\s]+)@(?P<sha>[0-9a-f]{40}):(?P<path>[^#\s]+)(?:#(?P<locator>.+))?$"
)
REVIEW_STATES = {"NOT_RUN", "NO_PASS", "PASS"}
RATIFICATION_STATES = {"NOT_REQUESTED", "PENDING", "RATIFIED", "REJECTED"}


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


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


def _semver_tuple(value: str) -> tuple[int, int, int]:
    major, minor, patch = value.split(".")
    return int(major), int(minor), int(patch)


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
        data = yaml.load("\n".join(lines[1:end]), Loader=_UniqueKeySafeLoader)
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


def _bound_candidate_ref(
    metadata: dict[str, Any],
    where: str,
    errors: list[str],
) -> str | None:
    explicit_keys = [
        key for key in ("candidate_ref", "semantic_ref") if key in metadata
    ]
    if explicit_keys:
        explicit: dict[str, str] = {}
        for key in explicit_keys:
            value = str(metadata[key] or "")
            if not SHA_RE.fullmatch(value):
                errors.append(
                    f"{where} explicit {key} must be a lowercase 40-hex candidate commit"
                )
                return None
            explicit[key] = value
        values = set(explicit.values())
        if len(values) != 1:
            rendered = ", ".join(
                f"{key}={value}" for key, value in sorted(explicit.items())
            )
            errors.append(
                f"{where} has conflicting explicit candidate subject fields: {rendered}"
            )
            return None
        return next(iter(values))

    legacy: list[tuple[int, str, str]] = []
    for key, value in metadata.items():
        match = re.fullmatch(r"p(?P<index>\d+)", str(key).lower())
        if match:
            legacy.append((int(match.group("index")), str(key), str(value or "")))

    if not legacy:
        errors.append(
            f"{where} does not declare a candidate subject in "
            "candidate_ref, semantic_ref, or legacy pN metadata"
        )
        return None

    highest = max(index for index, _, _ in legacy)
    highest_fields = [
        (key, value)
        for index, key, value in legacy
        if index == highest
    ]
    for key, value in highest_fields:
        if not SHA_RE.fullmatch(value):
            errors.append(
                f"{where} legacy candidate subject field {key} must be a lowercase 40-hex candidate commit"
            )
            return None
    values = {value for _, value in highest_fields}
    if len(values) != 1:
        rendered = ", ".join(
            f"{key}={value}" for key, value in sorted(highest_fields)
        )
        errors.append(
            f"{where} has ambiguous legacy candidate subject fields: {rendered}"
        )
        return None
    return next(iter(values))


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

    bound_ref = _bound_candidate_ref(metadata, where, errors)
    if bound_ref is not None and semantic_ref != bound_ref:
        errors.append(
            f"{where} does not bind candidate.semantic_ref {semantic_ref}; "
            f"review record subject is {bound_ref}"
        )

    expected_status = {"PASS": "pass", "NO_PASS": "no-pass"}[review_state]
    actual_status = str(metadata.get("status") or "").strip().lower().replace("_", "-")
    if actual_status != expected_status:
        errors.append(
            f"{where} disposition {actual_status or 'MISSING'} does not match candidate.review.state {review_state}"
        )


def _check_ratification_evidence(
    root: Path,
    project: str,
    value: str,
    semantic_ref: str,
    ratification_state: str,
    where: str,
    errors: list[str],
) -> None:
    content = _resolve_evidence_route(root, project, value, where, errors)
    if content is None:
        return

    metadata = _front_matter(content, where, errors)
    if not metadata:
        return

    bound_ref = _bound_candidate_ref(metadata, where, errors)
    if bound_ref is not None and semantic_ref != bound_ref:
        errors.append(
            f"{where} does not bind candidate.semantic_ref {semantic_ref}; "
            f"ratification record subject is {bound_ref}"
        )

    expected_status = {"RATIFIED": "ratified", "REJECTED": "rejected"}[ratification_state]
    actual_status = str(metadata.get("status") or "").strip().lower().replace("_", "-")
    if actual_status != expected_status:
        errors.append(
            f"{where} disposition {actual_status or 'MISSING'} "
            f"does not match candidate.ratification.state {ratification_state}"
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
    project = str(root.get("project") or "")
    if project != "hjin98/scientific-software-development-protocol":
        errors.append("project identity is not the SSDP repository")

    accepted = _mapping(root.get("accepted_current"), "accepted_current", errors)
    accepted_version = str(accepted.get("version") or "")
    accepted_version_valid = SEMVER_RE.fullmatch(accepted_version) is not None
    if not accepted_version_valid:
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
        if accepted_version_valid:
            historical_order = _semver_tuple(version)
            accepted_order = _semver_tuple(accepted_version)
            if historical_order == accepted_order:
                errors.append(f"historical[{version}] duplicates accepted_current.version")
            elif historical_order > accepted_order:
                errors.append(
                    f"historical[{version}] must be older than accepted_current.version {accepted_version}"
                )
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
    candidate_version_valid = SEMVER_RE.fullmatch(candidate_version) is not None
    if not candidate_version_valid:
        errors.append("candidate.version must be semantic x.y.z")
    historical_versions = {
        _semver_tuple(version)
        for version in historical
        if isinstance(version, str) and SEMVER_RE.fullmatch(version)
    }
    if candidate_version_valid and _semver_tuple(candidate_version) in historical_versions:
        errors.append(f"candidate.version {candidate_version} duplicates a historical version")
    if (
        candidate_version_valid
        and accepted_version_valid
        and candidate_version != accepted_version
        and _semver_tuple(candidate_version) <= _semver_tuple(accepted_version)
    ):
        errors.append(
            "candidate.version must be newer than accepted_current.version while it is the active successor"
        )
    semantic_ref = _sha_or(candidate.get("semantic_ref"), {"UNFROZEN"}, "candidate.semantic_ref", errors)
    public_ref = _sha_or(candidate.get("public_source_ref"), {"UNAVAILABLE"}, "candidate.public_source_ref", errors)
    recovery_ref = _sha_or(candidate.get("recovery_ref"), {"UNAVAILABLE"}, "candidate.recovery_ref", errors)

    review = _mapping(candidate.get("review"), "candidate.review", errors)
    review_state = str(review.get("state") or "")
    if review_state not in REVIEW_STATES:
        errors.append(f"candidate.review.state must be one of {sorted(REVIEW_STATES)}")
    review_evidence = _evidence(
        review.get("evidence_ref"),
        "candidate.review.evidence_ref",
        errors,
        required=review_state in {"NO_PASS", "PASS"},
    )

    ratification = _mapping(candidate.get("ratification"), "candidate.ratification", errors)
    ratification_state = str(ratification.get("state") or "")
    if ratification_state not in RATIFICATION_STATES:
        errors.append(f"candidate.ratification.state must be one of {sorted(RATIFICATION_STATES)}")
    ratification_evidence = _evidence(
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
        if (
            review_state in {"NO_PASS", "PASS"}
            and semantic_ref != "UNFROZEN"
            and EVIDENCE_RE.fullmatch(review_evidence)
        ):
            _check_review_evidence(
                repo_root,
                project,
                review_evidence,
                semantic_ref,
                review_state,
                "candidate.review.evidence_ref",
                errors,
            )
        if (
            ratification_state in {"RATIFIED", "REJECTED"}
            and semantic_ref != "UNFROZEN"
            and EVIDENCE_RE.fullmatch(ratification_evidence)
        ):
            _check_ratification_evidence(
                repo_root,
                project,
                ratification_evidence,
                semantic_ref,
                ratification_state,
                "candidate.ratification.evidence_ref",
                errors,
            )

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
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeySafeLoader)


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
