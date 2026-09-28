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
    return {
        "schema": SCHEMA,
        "required_artifacts": list(requirements.artifacts),
        "required_oracles": list(requirements.oracles),
        "expected_scoring_items": list(requirements.scoring_items),
        "manifest_digests": {
            "required_artifacts": requirements.artifact_manifest_digest,
            "required_oracles": requirements.oracle_manifest_digest,
            "expected_scoring_items": requirements.scoring_manifest_digest,
        },
    }


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
        if event.get("kind") not in NORMALIZED_EVENT_KINDS:
            errors.append(f"normalized event {index} has unknown kind")
        native_source = event.get("native_source")
        if not isinstance(native_source, dict):
            errors.append(f"normalized event {index} native_source is not an object")
        else:
            native_index = native_source.get("native_index")
            native_sha = native_source.get("native_sha256")
            if not isinstance(native_index, int) or isinstance(native_index, bool) or native_index < 0:
                errors.append(f"normalized event {index} native_index is invalid")
            if not isinstance(native_sha, str) or len(native_sha) != 64:
                errors.append(f"normalized event {index} native_sha256 is invalid")
        if not isinstance(event.get("payload"), dict):
            errors.append(f"normalized event {index} payload is not an object")
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
        if not isinstance(native_sha, str) or len(native_sha) != 64:
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
        if not isinstance(stdout_ref, str) or not (run / stdout_ref).is_file():
            missing.append(item["id"])
            continue
        if not isinstance(stderr_ref, str) or not (run / stderr_ref).is_file():
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


def validate_profile_admission(
    admission_path: Path | None,
    *,
    mode: str,
    profile_key_sha256: str,
    adapter_sha256: str,
    core_sha256: str,
    capability_manifest_sha256: str,
) -> list[str]:
    if mode == "probe":
        return []
    if mode != "qualification":
        return [f"unknown execution mode {mode!r}"]
    if admission_path is None:
        return ["qualification mode requires a profile-admission record"]
    try:
        payload = _require_object(load_json(admission_path), "profile admission")
    except ContractError as exc:
        return [str(exc)]
    required = {
        "schema": SCHEMA,
        "status": "ADMITTED",
        "profile_key_sha256": profile_key_sha256,
        "adapter_sha256": adapter_sha256,
        "core_sha256": core_sha256,
        "capability_manifest_sha256": capability_manifest_sha256,
    }
    errors = []
    for key, expected in required.items():
        if payload.get(key) != expected:
            errors.append(f"profile admission {key} does not match current realization")
    checks = payload.get("checks")
    if not isinstance(checks, dict) or not checks or any(value is not True for value in checks.values()):
        errors.append("profile admission checks are missing or not all true")
    return errors


def cache_valid(target: Path, identity: dict[str, Any]) -> bool:
    try:
        prior = json.loads((target / "run-identity.json").read_text(encoding="utf-8"))
        summary = json.loads((target / "summary.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        prior == identity
        and summary.get("evidence_state") == "COMPLETE_ADMISSIBLE"
        and summary.get("execution_ok") is True
    )


def requirements_from_snapshot(payload: Any) -> Requirements:
    data = _require_object(payload, "requirements snapshot")
    if data.get("schema") != SCHEMA:
        raise ContractError("requirements snapshot schema is unsupported")
    digests = data.get("manifest_digests")
    if not isinstance(digests, dict):
        raise ContractError("requirements snapshot has no manifest digests")
    artifacts = data.get("required_artifacts")
    oracles = data.get("required_oracles")
    scoring = data.get("expected_scoring_items")
    if not isinstance(artifacts, list) or not all(isinstance(x, str) and x for x in artifacts):
        raise ContractError("requirements snapshot required_artifacts is invalid")
    if not isinstance(oracles, list) or not all(isinstance(x, dict) for x in oracles):
        raise ContractError("requirements snapshot required_oracles is invalid")
    if not isinstance(scoring, list) or not all(isinstance(x, dict) for x in scoring):
        raise ContractError("requirements snapshot expected_scoring_items is invalid")
    # Reuse the exact validators by reconstructing a checked object in memory.
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
    for key in ("required_artifacts", "required_oracles", "expected_scoring_items"):
        if not isinstance(digests.get(key), str) or not digests[key]:
            raise ContractError(f"requirements snapshot digest {key} is invalid")
    return Requirements(
        artifacts=tuple(artifacts),
        oracles=tuple(dict(item) for item in oracles),
        scoring_items=tuple(dict(item) for item in scoring),
        artifact_manifest_digest=digests["required_artifacts"],
        oracle_manifest_digest=digests["required_oracles"],
        scoring_manifest_digest=digests["expected_scoring_items"],
    )


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
