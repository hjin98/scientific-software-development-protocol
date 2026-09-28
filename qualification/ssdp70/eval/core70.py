#!/usr/bin/env python3
"""Portable Stage F qualification core for Protocol 7.0 evidence tooling.

This module owns only the D3-accepted execution/evidence semantics: stable identities,
profile/capability validation, normalized-event validation, run-bound requirement
manifests, fail-closed evidence states, exact scoring closure, and profile-admission
binding. Runtime-specific launch/translation stays in adapters.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCHEMA = 1
EVIDENCE_STATES = {
    "COMPLETE_ADMISSIBLE",
    "INADMISSIBLE",
    "MISSING_REQUIRED_EVIDENCE",
    "MALFORMED_EVIDENCE_OR_ASSESSMENT",
    "EXECUTION_ERROR",
    "UNRESOLVED",
}
QUALIFICATION_OUTCOMES = {"PASS", "FAIL", "UNRESOLVED", "NOT_EVALUATED"}
DISPOSITIONS = {"pass", "fail", "unresolved", "not-applicable"}
CAPABILITY_DECISIONS = {"ALLOW", "DENY", "SANDBOX/MEDIATE"}
UNKNOWN_CLASSIFICATIONS = {"arm-neutral", "uncontrolled"}

REQUIRED_CAPABILITY_CLASSES = (
    "catalog_root_activation",
    "workspace_read_search_list",
    "workspace_mutation",
    "process_execution",
    "delegation",
    "issue_evidence_store",
    "repository_object_store",
    "network_remote_service",
    "external_mutation",
    "credential_secret_service_account",
)

NORMALIZED_EVENT_KINDS = {
    "catalog_snapshot",
    "root_selection",
    "resource_access",
    "tool_action",
    "delegate_call",
    "delegate_return",
    "issue_evidence_access",
    "mutation",
    "network_external_action",
    "termination",
    "final_result",
    "usage_timing",
}

COMMON_EVENT_FIELDS = {
    "schema_version",
    "run_id",
    "event_id",
    "sequence",
    "actor_id",
    "kind",
    "native_source",
    "status",
    "timing",
    "payload",
}

EXECUTOR_ADMISSION_CHECKS = (
    "exact_subject_profile_identity",
    "fresh_arm_isolation",
    "capability_manifest",
    "raw_normalized_completeness",
    "fail_closed_evidence",
    "exact_scoring_closure",
    "cache_profile_core_identity_perturbation",
    "catalog_contamination",
    "containment_pre_effect",
    "custody_denial",
    "ordinary_entry_owner_read",
    "withheld_oracle_branches",
)

EVALUATOR_ADMISSION_CHECKS = (
    "runtime_identity",
    "read_only_capability_enforcement",
    "credential_network_denial",
    "assessment_fail_closed",
    "evidence_integrity_revalidation",
    "evaluator_identity_perturbation",
)

EVIDENCE_INTEGRITY_ROOTS = (
    "summary.json",
    "run-identity.json",
    "profile-snapshot.json",
    "capability-manifest-snapshot.json",
    "profile-admission.json",
    "requirements-snapshot.json",
    "final-report.md",
    "diff.patch",
    "side-effects.jsonl",
    "tool-calls.jsonl",
    "trace.jsonl",
    "events.normalized.jsonl",
    "normalization-map.json",
    "oracle.json",
    "stderr.txt",
    "issues-final",
    "oracle-output",
    "final-tree",
)


class ContractError(ValueError):
    """The portable qualification contract is malformed or violated."""


@dataclass(frozen=True)
class Requirements:
    artifacts: tuple[str, ...]
    oracles: tuple[dict[str, Any], ...]
    scoring_items: tuple[dict[str, Any], ...]
    artifact_manifest_digest: str
    oracle_manifest_digest: str
    scoring_manifest_digest: str


@dataclass(frozen=True)
class ProfileBundle:
    profile: dict[str, Any]
    capabilities: dict[str, Any]
    profile_key: dict[str, Any]
    profile_key_sha256: str
    capability_manifest_sha256: str


def stable_json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path | None) -> str | None:
    if root is None or not root.exists():
        return None
    if root.is_file():
        return sha256_file(root)
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load JSON {path}: {exc}") from exc


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be an object")
    return value


def load_profile(profile_path: Path, capability_path: Path) -> ProfileBundle:
    profile = _require_object(load_json(profile_path), "execution profile")
    capabilities = _require_object(load_json(capability_path), "capability manifest")
    if profile.get("schema") != SCHEMA:
        raise ContractError("execution profile schema is unsupported")
    if capabilities.get("schema") != SCHEMA:
        raise ContractError("capability manifest schema is unsupported")

    cap_map = capabilities.get("capabilities")
    if not isinstance(cap_map, dict):
        raise ContractError("capability manifest.capabilities must be an object")
    missing = [name for name in REQUIRED_CAPABILITY_CLASSES if name not in cap_map]
    if missing:
        raise ContractError(f"capability manifest is missing classes: {missing}")
    for name in REQUIRED_CAPABILITY_CLASSES:
        entry = cap_map[name]
        if not isinstance(entry, dict) or entry.get("decision") not in CAPABILITY_DECISIONS:
            raise ContractError(f"capability {name} has invalid decision")
        if not isinstance(entry.get("scope"), (str, list, dict)):
            raise ContractError(f"capability {name} must declare scope")

    required_profile = (
        "profile_id",
        "adapter_id",
        "agent_model",
        "provider_runtime",
        "reasoning_configuration",
        "workspace_realization",
        "install_mechanism",
        "budgets",
        "containment_policy",
        "network_external_write_policy",
        "credential_service_account_policy",
        "provider_managed_unknowns",
    )
    absent = [name for name in required_profile if name not in profile]
    if absent:
        raise ContractError(f"execution profile is missing fields: {absent}")
    unknowns = profile["provider_managed_unknowns"]
    if not isinstance(unknowns, list):
        raise ContractError("provider_managed_unknowns must be a list")
    for index, item in enumerate(unknowns):
        if not isinstance(item, dict):
            raise ContractError(f"provider_managed_unknowns[{index}] must be an object")
        if not isinstance(item.get("name"), str) or not item["name"]:
            raise ContractError(f"provider_managed_unknowns[{index}] has no name")
        if item.get("classification") not in UNKNOWN_CLASSIFICATIONS:
            raise ContractError(f"provider_managed_unknowns[{index}] has invalid classification")
        claims = item.get("sensitive_claims", ["*"])
        if not isinstance(claims, list) or not all(isinstance(x, str) and x for x in claims):
            raise ContractError(f"provider_managed_unknowns[{index}].sensitive_claims is invalid")

    cap_digest = stable_json_sha256(capabilities)
    profile_key = {
        "schema": SCHEMA,
        "profile_id": profile["profile_id"],
        "adapter_id": profile["adapter_id"],
        "agent_model": profile["agent_model"],
        "provider_runtime": profile["provider_runtime"],
        "reasoning_configuration": profile["reasoning_configuration"],
        "workspace_realization": profile["workspace_realization"],
        "install_mechanism": profile["install_mechanism"],
        "budgets": profile["budgets"],
        "capability_manifest_sha256": cap_digest,
        "containment_policy": profile["containment_policy"],
        "network_external_write_policy": profile["network_external_write_policy"],
        "credential_service_account_policy": profile["credential_service_account_policy"],
        "provider_managed_unknowns": unknowns,
    }
    return ProfileBundle(
        profile=profile,
        capabilities=capabilities,
        profile_key=profile_key,
        profile_key_sha256=stable_json_sha256(profile_key),
        capability_manifest_sha256=cap_digest,
    )


def profile_claim_errors(bundle: ProfileBundle, claims: Iterable[str]) -> list[str]:
    claims = set(claims)
    errors: list[str] = []
    for item in bundle.profile["provider_managed_unknowns"]:
        if item["classification"] != "uncontrolled":
            continue
        sensitive = set(item.get("sensitive_claims", ["*"]))
        if "*" in sensitive or not claims or sensitive & claims:
            errors.append(
                f"provider-managed dimension {item['name']!r} is uncontrolled for claims "
                f"{sorted(claims) if claims else ['*']}"
            )
    return errors


def _load_episode_manifest(path: Path, episode_id: str, label: str) -> tuple[Any, str]:
    raw = _require_object(load_json(path), label)
    if raw.get("schema") != SCHEMA:
        raise ContractError(f"{label} schema is unsupported")
    episodes = raw.get("episodes")
    if not isinstance(episodes, dict) or episode_id not in episodes:
        raise ContractError(f"{label} has no entry for episode {episode_id!r}")
    return episodes[episode_id], stable_json_sha256(raw)


def load_requirements(root: Path, episode_id: str) -> Requirements:
    artifacts, adigest = _load_episode_manifest(root / "required_artifacts.json", episode_id, "required artifacts")
    oracles, odigest = _load_episode_manifest(root / "required_oracles.json", episode_id, "required oracles")
    scoring, sdigest = _load_episode_manifest(root / "expected_scoring_items.json", episode_id, "expected scoring items")

    if not isinstance(artifacts, list) or not all(isinstance(x, str) and x for x in artifacts):
        raise ContractError("required artifacts entry must be a list of non-empty paths")
    if len(set(artifacts)) != len(artifacts):
        raise ContractError("required artifacts contains duplicates")

    if not isinstance(oracles, list):
        raise ContractError("required oracles entry must be a list")
    oracle_ids: set[str] = set()
    normalized_oracles: list[dict[str, Any]] = []
    for index, item in enumerate(oracles):
        if not isinstance(item, dict):
            raise ContractError(f"required oracle {index} must be an object")
        oid, rel = item.get("id"), item.get("path")
        if not isinstance(oid, str) or not oid or oid in oracle_ids:
            raise ContractError(f"required oracle {index} has invalid/duplicate id")
        if not isinstance(rel, str) or not rel:
            raise ContractError(f"required oracle {oid} has no path")
        oracle_ids.add(oid)
        normalized_oracles.append({"id": oid, "path": rel})

    if not isinstance(scoring, list):
        raise ContractError("expected scoring items entry must be a list")
    scoring_ids: set[str] = set()
    normalized_scoring: list[dict[str, Any]] = []
    for index, item in enumerate(scoring):
        if not isinstance(item, dict):
            raise ContractError(f"expected scoring item {index} must be an object")
        iid = item.get("id")
        if not isinstance(iid, str) or not iid or iid in scoring_ids:
            raise ContractError(f"expected scoring item {index} has invalid/duplicate id")
        measure = item.get("measure")
        if not isinstance(measure, str) or not measure:
            raise ContractError(f"expected scoring item {iid} has no measure")
        critical = item.get("critical")
        if not isinstance(critical, bool):
            raise ContractError(f"expected scoring item {iid} critical must be boolean")
        branch = item.get("branch")
        if not isinstance(branch, str) or not branch:
            raise ContractError(f"expected scoring item {iid} has no branch")
        allowed = item.get("allowed_dispositions")
        if not isinstance(allowed, list) or not allowed or not set(allowed) <= DISPOSITIONS:
            raise ContractError(f"expected scoring item {iid} allowed_dispositions is invalid")
        scoring_ids.add(iid)
        normalized_scoring.append({
            "id": iid,
            "measure": measure,
            "critical": critical,
            "branch": branch,
            "allowed_dispositions": list(allowed),
        })

    return Requirements(
        artifacts=tuple(artifacts),
        oracles=tuple(normalized_oracles),
        scoring_items=tuple(normalized_scoring),
        artifact_manifest_digest=adigest,
        oracle_manifest_digest=odigest,
        scoring_manifest_digest=sdigest,
    )


def requirements_snapshot(requirements: Requirements) -> dict[str, Any]:
    artifacts = list(requirements.artifacts)
    oracles = list(requirements.oracles)
    scoring = list(requirements.scoring_items)
    return {
        "schema": SCHEMA,
        "required_artifacts": artifacts,
        "required_oracles": oracles,
        "expected_scoring_items": scoring,
        "manifest_digests": {
            "required_artifacts": requirements.artifact_manifest_digest,
            "required_oracles": requirements.oracle_manifest_digest,
            "expected_scoring_items": requirements.scoring_manifest_digest,
        },
        "content_digests": {
            "required_artifacts": stable_json_sha256(artifacts),
            "required_oracles": stable_json_sha256(oracles),
            "expected_scoring_items": stable_json_sha256(scoring),
        },
    }


def _valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())


def _require_payload_keys(kind: str, payload: dict[str, Any], required: set[str], index: int, errors: list[str]) -> None:
    missing = required - set(payload)
    if missing:
        errors.append(f"normalized event {index} {kind} payload missing fields {sorted(missing)}")


def _validate_event_payload(kind: str, status: Any, payload: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    if kind == "catalog_snapshot":
        _require_payload_keys(kind, payload, {"logical_skill_ids", "model", "runtime_version", "resolved_package_identity"}, index, errors)
        skills = payload.get("logical_skill_ids")
        if not isinstance(skills, list) or not all(isinstance(x, str) and x for x in skills):
            errors.append(f"normalized event {index} catalog_snapshot logical_skill_ids is invalid")
        package = payload.get("resolved_package_identity")
        if not isinstance(package, dict) or not _valid_sha256(package.get("package_sha256")):
            errors.append(f"normalized event {index} catalog_snapshot resolved package identity is invalid")
    elif kind == "root_selection":
        _require_payload_keys(kind, payload, {"logical_root", "selection_mechanism", "native_operation", "input", "resolved_package_identity"}, index, errors)
        if not isinstance(payload.get("logical_root"), str) or not payload.get("logical_root"):
            errors.append(f"normalized event {index} root_selection logical_root is invalid")
        if not isinstance(payload.get("selection_mechanism"), str) or not payload.get("selection_mechanism"):
            errors.append(f"normalized event {index} root_selection mechanism is invalid")
        package = payload.get("resolved_package_identity")
        if not isinstance(package, dict) or not _valid_sha256(package.get("package_sha256")):
            errors.append(f"normalized event {index} root_selection resolved package identity is invalid")
    elif kind == "resource_access":
        _require_payload_keys(kind, payload, {
            "operation", "resource_identity", "input", "tool_use_id", "result_status",
            "result_reference", "result_sha256", "resolved_package_identity",
            "resource_sha256", "resource_bytes",
        }, index, errors)
        if not isinstance(payload.get("resource_identity"), str) or not payload.get("resource_identity"):
            errors.append(f"normalized event {index} resource_access resource_identity is invalid")
        if not isinstance(payload.get("input"), dict):
            errors.append(f"normalized event {index} resource_access input is invalid")
        if not isinstance(payload.get("tool_use_id"), str) or not payload.get("tool_use_id"):
            errors.append(f"normalized event {index} resource_access tool_use_id is invalid")
        if payload.get("result_status") not in {"pending", "result", "error"}:
            errors.append(f"normalized event {index} resource_access result_status is invalid")
        if status in {"result", "error"}:
            if not isinstance(payload.get("result_reference"), str) or not payload.get("result_reference"):
                errors.append(f"normalized event {index} resource_access result_reference is missing")
            if not _valid_sha256(payload.get("result_sha256")):
                errors.append(f"normalized event {index} resource_access result_sha256 is invalid")
            if "result_content" not in payload:
                errors.append(f"normalized event {index} resource_access result_content is missing")
        if payload.get("resource_sha256") is not None and not _valid_sha256(payload.get("resource_sha256")):
            errors.append(f"normalized event {index} resource_access resource_sha256 is invalid")
        if payload.get("resource_bytes") is not None and (
            not isinstance(payload.get("resource_bytes"), int) or isinstance(payload.get("resource_bytes"), bool) or payload["resource_bytes"] < 0
        ):
            errors.append(f"normalized event {index} resource_access resource_bytes is invalid")
    elif kind == "tool_action":
        _require_payload_keys(kind, payload, {
            "semantic_capability_classes", "native_operation", "input", "tool_use_id",
            "result_status", "result_reference", "result_sha256",
        }, index, errors)
        classes = payload.get("semantic_capability_classes")
        if not isinstance(classes, list) or not classes or not all(isinstance(x, str) and x for x in classes):
            errors.append(f"normalized event {index} tool_action capability classes are invalid")
        if status in {"result", "error"}:
            if not isinstance(payload.get("result_reference"), str) or not payload.get("result_reference"):
                errors.append(f"normalized event {index} tool_action result_reference is missing")
            if not _valid_sha256(payload.get("result_sha256")):
                errors.append(f"normalized event {index} tool_action result_sha256 is invalid")
            if "result_content" not in payload:
                errors.append(f"normalized event {index} tool_action result_content is missing")
    elif kind == "delegate_call":
        _require_payload_keys(kind, payload, {"delegate_id", "parent_actor", "request", "launched_work_relation", "tool_use_id"}, index, errors)
    elif kind == "delegate_return":
        _require_payload_keys(kind, payload, {"delegate_id", "parent_actor", "result_reference", "result_sha256", "result_content", "tool_use_id"}, index, errors)
        if not _valid_sha256(payload.get("result_sha256")):
            errors.append(f"normalized event {index} delegate_return result_sha256 is invalid")
    elif kind == "mutation":
        _require_payload_keys(kind, payload, {
            "operation", "logical_target", "workspace_external_class", "authorization_decision",
            "disposition", "input", "tool_use_id", "result_status", "result_reference", "result_sha256",
        }, index, errors)
        if status in {"result", "error"} and not _valid_sha256(payload.get("result_sha256")):
            errors.append(f"normalized event {index} mutation result_sha256 is invalid")
    elif kind == "network_external_action":
        _require_payload_keys(kind, payload, {
            "destination_service", "operation", "authorization_decision", "disposition",
            "input", "tool_use_id", "result_status", "result_reference", "result_sha256",
        }, index, errors)
        if status in {"result", "error"} and not _valid_sha256(payload.get("result_sha256")):
            errors.append(f"normalized event {index} network result_sha256 is invalid")
    elif kind == "issue_evidence_access":
        _require_payload_keys(kind, payload, {"operation", "resource_identity", "input", "result_status"}, index, errors)
    elif kind == "termination":
        _require_payload_keys(kind, payload, {"state", "native_return_state", "terminal_result_exists"}, index, errors)
        if not isinstance(payload.get("state"), str) or not payload.get("state"):
            errors.append(f"normalized event {index} termination state is invalid")
        if not isinstance(payload.get("native_return_state"), dict):
            errors.append(f"normalized event {index} termination native_return_state is invalid")
        if not isinstance(payload.get("terminal_result_exists"), bool):
            errors.append(f"normalized event {index} termination terminal_result_exists is invalid")
    elif kind == "final_result":
        _require_payload_keys(kind, payload, {"result_text", "artifact_reference"}, index, errors)
        if not isinstance(payload.get("result_text"), str):
            errors.append(f"normalized event {index} final_result result_text is invalid")
        if not isinstance(payload.get("artifact_reference"), str) or not payload.get("artifact_reference"):
            errors.append(f"normalized event {index} final_result artifact_reference is invalid")
    elif kind == "usage_timing":
        _require_payload_keys(kind, payload, {"duration_ms", "duration_unit", "usage", "usage_source"}, index, errors)
        if payload.get("duration_ms") is not None and not isinstance(payload.get("duration_ms"), (int, float)):
            errors.append(f"normalized event {index} usage_timing duration_ms is invalid")
        if payload.get("duration_unit") != "ms":
            errors.append(f"normalized event {index} usage_timing duration unit is invalid")
        if not isinstance(payload.get("usage_source"), str) or not payload.get("usage_source"):
            errors.append(f"normalized event {index} usage_timing source is invalid")
    return errors


def validate_normalized_events(events: list[dict[str, Any]], run_id: str) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    prior_sequence = -1
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"normalized event {index} is not an object")
            continue
        missing = COMMON_EVENT_FIELDS - set(event)
        if missing:
            errors.append(f"normalized event {index} missing fields {sorted(missing)}")
            continue
        if event.get("schema_version") != SCHEMA:
            errors.append(f"normalized event {index} has unsupported schema")
        if event.get("run_id") != run_id:
            errors.append(f"normalized event {index} has wrong run_id")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id or event_id in seen_ids:
            errors.append(f"normalized event {index} has invalid/duplicate event_id")
        else:
            seen_ids.add(event_id)
        sequence = event.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence <= prior_sequence:
            errors.append(f"normalized event {index} sequence is not strictly increasing")
        else:
            prior_sequence = sequence
        kind = event.get("kind")
        if kind not in NORMALIZED_EVENT_KINDS:
            errors.append(f"normalized event {index} has unknown kind")
        native_source = event.get("native_source")
        if not isinstance(native_source, dict):
            errors.append(f"normalized event {index} native_source is not an object")
        else:
            native_index = native_source.get("native_index")
            native_sha = native_source.get("native_sha256")
            if not isinstance(native_index, int) or isinstance(native_index, bool) or native_index < 0:
                errors.append(f"normalized event {index} native_index is invalid")
            if not _valid_sha256(native_sha):
                errors.append(f"normalized event {index} native_sha256 is invalid")
        status = event.get("status")
        if not isinstance(status, str) or not status:
            errors.append(f"normalized event {index} status is invalid")
        payload = event.get("payload")
        if not isinstance(payload, dict):
            errors.append(f"normalized event {index} payload is not an object")
        elif kind in NORMALIZED_EVENT_KINDS:
            errors.extend(_validate_event_payload(kind, status, payload, index))
    native_order = [
        event.get("native_source", {}).get("native_index")
        for event in events
        if isinstance(event, dict) and isinstance(event.get("native_source"), dict)
        and isinstance(event.get("native_source", {}).get("native_index"), int)
    ]
    if native_order != sorted(native_order):
        errors.append("normalized events reorder native event order")
    return errors


def validate_completeness_map(
    native_event_count: int,
    entries: list[dict[str, Any]],
    normalized_events: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    normalized_ids = {e.get("event_id") for e in normalized_events if isinstance(e, dict)}
    seen_native: set[int] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"completeness entry {index} is not an object")
            continue
        native_index = entry.get("native_index")
        if not isinstance(native_index, int) or isinstance(native_index, bool) or not (0 <= native_index < native_event_count):
            errors.append(f"completeness entry {index} has invalid native_index")
            continue
        if native_index in seen_native:
            errors.append(f"native event {native_index} is mapped more than once")
        seen_native.add(native_index)
        mapped = entry.get("mapped_event_ids")
        classification = entry.get("classification")
        oracle_relevant = entry.get("oracle_relevant")
        native_sha = entry.get("native_sha256")
        if not _valid_sha256(native_sha):
            errors.append(f"native event {native_index} has invalid native_sha256")
        if not isinstance(mapped, list) or not all(isinstance(x, str) and x for x in mapped):
            errors.append(f"native event {native_index} mapped_event_ids is invalid")
            mapped = []
        missing_ids = [eid for eid in mapped if eid not in normalized_ids]
        if missing_ids:
            errors.append(f"native event {native_index} maps unknown normalized ids {missing_ids}")
        if not isinstance(classification, str) or not classification:
            errors.append(f"native event {native_index} is unclassified")
        if not isinstance(oracle_relevant, bool):
            errors.append(f"native event {native_index} oracle_relevant is not boolean")
        elif oracle_relevant and not mapped:
            errors.append(f"oracle-relevant native event {native_index} is unmapped")
    if seen_native != set(range(native_event_count)):
        missing = sorted(set(range(native_event_count)) - seen_native)
        errors.append(f"native events missing from completeness map: {missing}")
    return errors


def validate_required_artifacts(run: Path, requirements: Requirements) -> list[str]:
    return [name for name in requirements.artifacts if not (run / name).exists()]


def validate_required_oracles(run: Path, requirements: Requirements) -> list[str]:
    oracle_path = run / "oracle.json"
    if not oracle_path.is_file():
        return [item["id"] for item in requirements.oracles]
    try:
        payload = json.loads(oracle_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [item["id"] for item in requirements.oracles]
    results = payload.get("results") if isinstance(payload, dict) else None
    if not isinstance(results, dict):
        return [item["id"] for item in requirements.oracles]
    missing: list[str] = []
    for item in requirements.oracles:
        row = results.get(item["id"])
        if not isinstance(row, dict) or row.get("executed") is not True:
            missing.append(item["id"])
            continue
        stdout_ref = row.get("stdout_artifact")
        stderr_ref = row.get("stderr_artifact")
        stdout_path = run / stdout_ref if isinstance(stdout_ref, str) else None
        stderr_path = run / stderr_ref if isinstance(stderr_ref, str) else None
        if stdout_path is None or not stdout_path.is_file() or stderr_path is None or not stderr_path.is_file():
            missing.append(item["id"])
            continue
        if not _valid_sha256(row.get("stdout_sha256")) or sha256_file(stdout_path) != row["stdout_sha256"]:
            missing.append(item["id"])
            continue
        if not _valid_sha256(row.get("stderr_sha256")) or sha256_file(stderr_path) != row["stderr_sha256"]:
            missing.append(item["id"])
    return missing


def validate_dispositions(dispositions: Any, requirements: Requirements) -> list[str]:
    errors: list[str] = []
    if not isinstance(dispositions, list):
        return ["dispositions is not a list"]
    expected = {item["id"]: item for item in requirements.scoring_items}
    seen: set[str] = set()
    for index, row in enumerate(dispositions):
        if not isinstance(row, dict):
            errors.append(f"disposition {index} is not an object")
            continue
        item_id = row.get("item")
        if not isinstance(item_id, str) or item_id not in expected:
            errors.append(f"disposition {index} has unknown item id {item_id!r}")
            continue
        if item_id in seen:
            errors.append(f"duplicate disposition for item {item_id}")
            continue
        seen.add(item_id)
        spec = expected[item_id]
        if row.get("measure") != spec["measure"]:
            errors.append(f"item {item_id} measure does not match manifest")
        if row.get("critical") is not spec["critical"]:
            errors.append(f"item {item_id} critical does not match manifest")
        result = row.get("result")
        if result not in spec["allowed_dispositions"]:
            errors.append(f"item {item_id} result {result!r} is not allowed")
    missing = sorted(set(expected) - seen)
    if missing:
        errors.append(f"missing dispositions for items: {missing}")
    return errors


def outcome_from_dispositions(dispositions: list[dict[str, Any]], requirements: Requirements) -> str:
    errors = validate_dispositions(dispositions, requirements)
    if errors:
        raise ContractError("cannot derive outcome from invalid dispositions: " + "; ".join(errors))
    results = {row["result"] for row in dispositions}
    if "fail" in results:
        return "FAIL"
    if "unresolved" in results:
        return "UNRESOLVED"
    return "PASS"


def _admission_checks_for_role(role: str) -> tuple[str, ...]:
    if role == "executor":
        return EXECUTOR_ADMISSION_CHECKS
    if role == "evaluator":
        return EVALUATOR_ADMISSION_CHECKS
    raise ContractError(f"unknown profile admission role {role!r}")


def _safe_relative_file(base: Path, relative: Any) -> Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    path = (base / rel).resolve()
    base_resolved = base.resolve()
    if path != base_resolved and base_resolved not in path.parents:
        return None
    return path


def admission_bundle_sha256(admission_path: Path | None, *, role: str = "executor") -> str | None:
    if admission_path is None:
        return None
    payload = _require_object(load_json(admission_path), "profile admission")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        raise ContractError("profile admission checks are malformed")
    evidence: dict[str, str] = {}
    for name in _admission_checks_for_role(role):
        row = checks.get(name)
        if not isinstance(row, dict):
            raise ContractError(f"profile admission check {name!r} is missing")
        path = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
        if path is None or not path.is_file():
            raise ContractError(f"profile admission check {name!r} evidence is unavailable")
        evidence[name] = sha256_file(path)
    return stable_json_sha256({"record": payload, "evidence": evidence})


def validate_profile_admission(
    admission_path: Path | None,
    *,
    mode: str,
    profile_key_sha256: str,
    adapter_sha256: str,
    core_sha256: str,
    capability_manifest_sha256: str,
    role: str = "executor",
) -> list[str]:
    if mode == "probe":
        return []
    if mode != "qualification":
        return [f"unknown execution mode {mode!r}"]
    if admission_path is None:
        return [f"qualification mode requires a {role} profile-admission record"]
    try:
        payload = _require_object(load_json(admission_path), "profile admission")
        expected_checks = set(_admission_checks_for_role(role))
    except ContractError as exc:
        return [str(exc)]
    required = {
        "schema": SCHEMA,
        "status": "ADMITTED",
        "role": role,
        "profile_key_sha256": profile_key_sha256,
        "adapter_sha256": adapter_sha256,
        "core_sha256": core_sha256,
        "capability_manifest_sha256": capability_manifest_sha256,
    }
    errors: list[str] = []
    for key, expected in required.items():
        if payload.get(key) != expected:
            errors.append(f"profile admission {key} does not match current realization")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        errors.append("profile admission checks are missing")
        return errors
    actual_checks = set(checks)
    missing = sorted(expected_checks - actual_checks)
    unknown = sorted(actual_checks - expected_checks)
    if missing:
        errors.append(f"profile admission is missing required checks: {missing}")
    if unknown:
        errors.append(f"profile admission has unknown checks: {unknown}")
    for name in sorted(expected_checks & actual_checks):
        row = checks[name]
        if not isinstance(row, dict):
            errors.append(f"profile admission check {name!r} is not an object")
            continue
        if row.get("status") != "PASS":
            errors.append(f"profile admission check {name!r} did not PASS")
        path = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
        expected_sha = row.get("evidence_sha256")
        if path is None or not path.is_file():
            errors.append(f"profile admission check {name!r} evidence is unavailable")
            continue
        if not _valid_sha256(expected_sha) or sha256_file(path) != expected_sha:
            errors.append(f"profile admission check {name!r} evidence hash does not match")
    return errors


def _contains_unfrozen_marker(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return "must-be-frozen" in lowered or "until-frozen" in lowered
    if isinstance(value, dict):
        return any(_contains_unfrozen_marker(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_unfrozen_marker(v) for v in value)
    return False


def validate_launch_identity(profile: dict[str, Any], command_identity: Any) -> list[str]:
    if not isinstance(command_identity, dict):
        return ["adapter did not expose launch command identity"]
    errors: list[str] = []
    if command_identity.get("model") != profile.get("agent_model"):
        errors.append("launched model does not match frozen execution profile")
    if command_identity.get("reasoning_configuration") != profile.get("reasoning_configuration"):
        errors.append("launched reasoning configuration does not match frozen execution profile")
    runtime = profile.get("provider_runtime")
    if isinstance(runtime, dict) and runtime.get("executable") is not None:
        if command_identity.get("executable") != runtime.get("executable"):
            errors.append("launched executable does not match frozen execution profile")
    if "native_allowed_tools" in profile and command_identity.get("allowed_tools") != profile.get("native_allowed_tools"):
        errors.append("launched allowed-tool set does not match frozen execution profile")
    if "native_disallowed_tools" in profile and command_identity.get("disallowed_tools") != profile.get("native_disallowed_tools"):
        errors.append("launched disallowed-tool set does not match frozen execution profile")
    return errors


def validate_runtime_observation(bundle: ProfileBundle, observation: Any) -> list[str]:
    errors: list[str] = []
    if _contains_unfrozen_marker(bundle.profile):
        errors.append("execution profile contains an unfrozen runtime/reasoning marker")
    if not isinstance(observation, dict):
        return errors + ["adapter did not expose runtime observation"]
    if observation.get("model") != bundle.profile.get("agent_model"):
        errors.append("runtime-observed model does not match frozen execution profile")
    runtime = bundle.profile.get("provider_runtime")
    expected_version = runtime.get("version") if isinstance(runtime, dict) else None
    observed_version = observation.get("runtime_version")
    if not isinstance(expected_version, str) or not expected_version:
        errors.append("execution profile has no frozen provider/runtime version")
    elif observed_version != expected_version:
        errors.append("runtime-observed provider/runtime version does not match frozen execution profile")
    return errors


def validate_claim_observability(events: list[dict[str, Any]], claims: Iterable[str]) -> list[str]:
    normalized = {str(claim).lower() for claim in claims}
    errors: list[str] = []
    successful_reads = [
        event for event in events
        if event.get("kind") == "resource_access"
        and event.get("status") == "result"
        and (event.get("payload") or {}).get("result_status") == "result"
    ]
    if any("owner-read" in claim for claim in normalized) and not successful_reads:
        errors.append("owner-read claim has no successful resource-access result evidence")
    burden_sensitive = any(
        token in claim
        for claim in normalized
        for token in ("t1", "t7", "t8", "burden", "active-byte")
    )
    if burden_sensitive:
        roots = [
            event for event in events
            if event.get("kind") == "root_selection"
            and isinstance((event.get("payload") or {}).get("resolved_package_identity"), dict)
        ]
        if not roots:
            errors.append("T1/T7/T8 burden claim has no resolved logical root-selection evidence")
        package_reads = [
            event for event in successful_reads
            if isinstance((event.get("payload") or {}).get("resolved_package_identity"), dict)
        ]
        if not package_reads:
            errors.append("T1/T7/T8 burden claim has no successful exact SSDP-resource evidence")
        for event in package_reads:
            payload = event.get("payload") or {}
            if not _valid_sha256(payload.get("resource_sha256")) or not isinstance(payload.get("resource_bytes"), int):
                errors.append("T1/T7/T8 burden claim lacks exact SSDP-resource byte/hash observability")
                break
    if any("ordinary-entry" in claim for claim in normalized):
        ordinary = [
            event for event in events
            if event.get("kind") == "root_selection"
            and str((event.get("payload") or {}).get("selection_mechanism", "")).startswith("ordinary")
        ]
        if not ordinary:
            errors.append("ordinary-entry claim has no observed ordinary root selection")
    return errors


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
        if path.is_file() and path.name != "evidence-integrity.json":
            files[path.relative_to(run).as_posix()] = path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.name != "evidence-integrity.json":
                    files[child.relative_to(run).as_posix()] = child
    return [files[key] for key in sorted(files)]


def write_evidence_integrity(run: Path, requirements: Requirements) -> dict[str, Any]:
    identity = _require_object(load_json(run / "run-identity.json"), "run identity")
    snapshot = requirements_snapshot(requirements)
    files = [
        {
            "path": path.relative_to(run).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in _evidence_files(run, requirements)
    ]
    payload = {
        "schema": SCHEMA,
        "run_identity_sha256": identity.get("identity_sha256"),
        "requirements_content_digests": snapshot["content_digests"],
        "files": files,
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
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"evidence integrity row {index} is not an object")
            continue
        rel = row.get("path")
        candidate = _safe_relative_file(run, rel)
        if candidate is None or not candidate.is_file():
            errors.append(f"evidence integrity file {rel!r} is unavailable")
            continue
        if rel in seen:
            errors.append(f"evidence integrity file {rel!r} is duplicated")
        seen.add(rel)
        if row.get("bytes") != candidate.stat().st_size:
            errors.append(f"evidence integrity file {rel!r} size changed")
        if not _valid_sha256(row.get("sha256")) or sha256_file(candidate) != row.get("sha256"):
            errors.append(f"evidence integrity file {rel!r} hash changed")
    expected_paths = {path.relative_to(run).as_posix() for path in _evidence_files(run, requirements)}
    if seen != expected_paths:
        missing = sorted(expected_paths - seen)
        extra = sorted(seen - expected_paths)
        if missing:
            errors.append(f"evidence integrity manifest omits files: {missing}")
        if extra:
            errors.append(f"evidence integrity manifest contains unexpected files: {extra}")
    return errors


def requirements_from_snapshot(
    payload: Any,
    expected_manifest_digests: dict[str, str] | None = None,
) -> Requirements:
    data = _require_object(payload, "requirements snapshot")
    if data.get("schema") != SCHEMA:
        raise ContractError("requirements snapshot schema is unsupported")
    digests = data.get("manifest_digests")
    content_digests = data.get("content_digests")
    if not isinstance(digests, dict):
        raise ContractError("requirements snapshot has no manifest digests")
    if not isinstance(content_digests, dict):
        raise ContractError("requirements snapshot has no content digests")
    artifacts = data.get("required_artifacts")
    oracles = data.get("required_oracles")
    scoring = data.get("expected_scoring_items")
    if not isinstance(artifacts, list) or not all(isinstance(x, str) and x for x in artifacts):
        raise ContractError("requirements snapshot required_artifacts is invalid")
    if not isinstance(oracles, list) or not all(isinstance(x, dict) for x in oracles):
        raise ContractError("requirements snapshot required_oracles is invalid")
    if not isinstance(scoring, list) or not all(isinstance(x, dict) for x in scoring):
        raise ContractError("requirements snapshot expected_scoring_items is invalid")
    actual_content = {
        "required_artifacts": stable_json_sha256(artifacts),
        "required_oracles": stable_json_sha256(oracles),
        "expected_scoring_items": stable_json_sha256(scoring),
    }
    if content_digests != actual_content:
        raise ContractError("requirements snapshot content digests do not match content")
    for key in ("required_artifacts", "required_oracles", "expected_scoring_items"):
        if not isinstance(digests.get(key), str) or not digests[key]:
            raise ContractError(f"requirements snapshot digest {key} is invalid")
    if expected_manifest_digests is not None and digests != expected_manifest_digests:
        raise ContractError("requirements snapshot manifest digests do not match run identity")
    oracle_ids: set[str] = set()
    for index, item in enumerate(oracles):
        oid, rel = item.get("id"), item.get("path")
        if not isinstance(oid, str) or not oid or oid in oracle_ids or not isinstance(rel, str) or not rel:
            raise ContractError(f"requirements snapshot oracle {index} is invalid")
        oracle_ids.add(oid)
    scoring_ids: set[str] = set()
    for index, item in enumerate(scoring):
        iid = item.get("id")
        if not isinstance(iid, str) or not iid or iid in scoring_ids:
            raise ContractError(f"requirements snapshot scoring item {index} is invalid")
        if not isinstance(item.get("measure"), str) or not item["measure"]:
            raise ContractError(f"requirements snapshot scoring item {iid} has no measure")
        if not isinstance(item.get("critical"), bool):
            raise ContractError(f"requirements snapshot scoring item {iid} critical is invalid")
        if not isinstance(item.get("branch"), str) or not item["branch"]:
            raise ContractError(f"requirements snapshot scoring item {iid} branch is invalid")
        allowed = item.get("allowed_dispositions")
        if not isinstance(allowed, list) or not allowed or not set(allowed) <= DISPOSITIONS:
            raise ContractError(f"requirements snapshot scoring item {iid} dispositions are invalid")
        scoring_ids.add(iid)
    return Requirements(
        artifacts=tuple(artifacts),
        oracles=tuple(dict(item) for item in oracles),
        scoring_items=tuple(dict(item) for item in scoring),
        artifact_manifest_digest=digests["required_artifacts"],
        oracle_manifest_digest=digests["required_oracles"],
        scoring_manifest_digest=digests["expected_scoring_items"],
    )


def _load_normalized_events(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"cannot read normalized events: {exc}"]
    for index, line in enumerate(lines):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"normalized event line {index} is invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"normalized event line {index} is not an object")
            continue
        events.append(value)
    return events, errors


def validate_complete_run(run: Path, identity: dict[str, Any], requirements: Requirements) -> list[str]:
    errors: list[str] = []
    try:
        prior = _require_object(load_json(run / "run-identity.json"), "run identity")
        summary = _require_object(load_json(run / "summary.json"), "run summary")
        snapshot_payload = load_json(run / "requirements-snapshot.json")
    except ContractError as exc:
        return [str(exc)]
    if prior != identity:
        errors.append("stored run identity does not match current identity")
    if summary.get("run_identity_sha256") != identity.get("identity_sha256"):
        errors.append("run summary identity does not match current identity")
    if summary.get("evidence_state") != "COMPLETE_ADMISSIBLE" or summary.get("execution_ok") is not True:
        errors.append("run summary is not COMPLETE_ADMISSIBLE with successful execution")
    identity_requirements = identity.get("requirements") if isinstance(identity.get("requirements"), dict) else {}
    expected_manifest_digests = {
        "required_artifacts": identity_requirements.get("required_artifacts_sha256"),
        "required_oracles": identity_requirements.get("required_oracles_sha256"),
        "expected_scoring_items": identity_requirements.get("expected_scoring_items_sha256"),
    }
    try:
        snap_requirements = requirements_from_snapshot(snapshot_payload, expected_manifest_digests)
    except ContractError as exc:
        errors.append(str(exc))
        snap_requirements = None
    if snap_requirements is not None and snap_requirements != requirements:
        errors.append("requirements snapshot does not match current frozen requirements")
    missing_artifacts = validate_required_artifacts(run, requirements)
    missing_oracles = validate_required_oracles(run, requirements)
    if missing_artifacts:
        errors.append(f"required artifacts are missing: {missing_artifacts}")
    if missing_oracles:
        errors.append(f"required oracles are missing/unexecuted/corrupt: {missing_oracles}")
    events, parse_errors = _load_normalized_events(run / "events.normalized.jsonl")
    errors.extend(parse_errors)
    if not parse_errors:
        errors.extend(validate_normalized_events(events, identity.get("identity_sha256")))
    try:
        completeness = _require_object(load_json(run / "normalization-map.json"), "normalization map")
        count = completeness.get("native_event_count")
        entries = completeness.get("entries")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0 or not isinstance(entries, list):
            errors.append("normalization map shape is invalid")
        elif not parse_errors:
            errors.extend(validate_completeness_map(count, entries, events))
    except ContractError as exc:
        errors.append(str(exc))
    errors.extend(validate_evidence_integrity(run, requirements))
    return errors


def cache_valid(target: Path, identity: dict[str, Any], requirements: Requirements) -> bool:
    return not validate_complete_run(target, identity, requirements)


def run_evidence_state(
    *,
    execution_ok: bool,
    profile_errors: list[str],
    event_errors: list[str],
    completeness_errors: list[str],
    catalog_ok: bool,
    terminal_exists: bool,
    final_result_exists: bool,
    missing_artifacts: list[str],
    missing_oracles: list[str],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not execution_ok:
        reasons.append("executor did not complete successfully")
        return "EXECUTION_ERROR", reasons
    if profile_errors:
        reasons.extend(profile_errors)
        return "INADMISSIBLE", reasons
    if event_errors or completeness_errors:
        reasons.extend(event_errors)
        reasons.extend(completeness_errors)
        return "MALFORMED_EVIDENCE_OR_ASSESSMENT", reasons
    if not catalog_ok:
        reasons.append("runtime catalog isolation failed")
        return "INADMISSIBLE", reasons
    if not terminal_exists:
        reasons.append("termination event is missing")
    if not final_result_exists:
        reasons.append("final-result event is missing")
    if missing_artifacts:
        reasons.append(f"required artifacts are missing: {missing_artifacts}")
    if missing_oracles:
        reasons.append(f"required oracles are missing/unexecuted: {missing_oracles}")
    if reasons:
        return "MISSING_REQUIRED_EVIDENCE", reasons
    return "COMPLETE_ADMISSIBLE", []
