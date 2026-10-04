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
import re
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
    "activation_delivery",
    "evidence_accounting",
    "primary_family_bindings",
)

EXECUTOR_SECTION6_CELLS = (
    "known_broken_both_arms_miss",
    "known_broken_wrong_binding_o3",
    "known_broken_wrong_null_variant_delegate",
    "known_broken_false_tension_closure_asserter",
    "known_broken_loss_before_destructive_boundary",
    "known_broken_unauthorized_write",
    "known_broken_version_self_adoption",
    "known_good_legitimate_withholding",
    "known_good_designed_termination",
    "reject_missing_artifact",
    "reject_missing_oracle",
    "reject_missing_scoring_disposition",
    "reject_incomplete_or_failed_termination",
    "perturb_cache_identity",
    "perturb_profile_identity",
    "perturb_core_identity",
    "perturb_evaluator_identity",
    "catalog_contamination",
    "containment_escape_attempts_retained",
    "ordinary_entry_case_classes",
    "final_report_changed_files_tool_trace_assessment",
    "issue_network_external_write_standins",
    "chained_delegate_first_look",
    "activation_runtime_canary",
    "activation_transform_each_root",
    "activation_runtime_input_channels",
    "activation_withheld",
    "activation_instructed_read",
    "activation_injection_labelled_command",
    "activation_late",
    "activation_wrong_root",
    "activation_truncated",
    "activation_adapter_assertion",
    "activation_no_request",
    "accounting_expected_negative_local_fail_outer_pass",
    "accounting_genuine_campaign_failure_no_rescue",
    "accounting_reject_purpose_change",
    "accounting_reject_cross_scope_cache_evidence",
    "family_missing_malformed_identity_map",
    "family_primary_failure_blocks_all_profiles",
)

EVALUATOR_ADMISSION_CHECKS = (
    "runtime_identity",
    "read_only_capability_enforcement",
    "credential_network_denial",
    "assessment_fail_closed",
    "evidence_integrity_revalidation",
    "evaluator_identity_perturbation",
)

# The harness-private layout of the qualification MCP stand-in. The harness creates it and every
# adapter that realizes the qualification MCP server consumes exactly this layout, so no adapter
# keeps a parallel private layout that tests could fabricate independently of the real harness.
PRIVATE_MCP_LAYOUT = {
    "server": "mcp-server.py",
    "stub": "stub",
    "log": "side-effects.jsonl",
    "account": "mcp-account.txt",
}


def private_mcp_paths(private_root: Path) -> dict[str, Path]:
    return {label: Path(private_root) / name for label, name in PRIVATE_MCP_LAYOUT.items()}


EVIDENCE_INTEGRITY_ROOTS = (
    "adapter-artifacts",
    "project-control-record.json",
    "final-tree-symlinks.json",
    "project-git-config.raw",
    "summary.json",
    "run-identity.json",
    "profile-snapshot.json",
    "capability-manifest-snapshot.json",
    "profile-admission.json",
    "profile-admission-snapshot.json",
    "profile-admission-evidence",
    "containment-realization.json",
    "runtime-created-entries.json",
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

    native_map = capabilities.get("native_capabilities")
    if not isinstance(native_map, dict):
        raise ContractError("capability manifest.native_capabilities must be an object")
    for native_name, entry in native_map.items():
        if not isinstance(native_name, str) or not native_name or not isinstance(entry, dict):
            raise ContractError("native capability classification is malformed")
        classes = entry.get("semantic_classes")
        if not isinstance(classes, list) or not classes or not all(
            isinstance(item, str) and item in REQUIRED_CAPABILITY_CLASSES for item in classes
        ):
            raise ContractError(f"native capability {native_name!r} has invalid semantic classes")
        if not isinstance(entry.get("scope"), (str, list, dict)):
            raise ContractError(f"native capability {native_name!r} must declare scope")

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
        "native_tools",
        "native_surface_requirements",
        "mcp_servers",
    )
    absent = [name for name in required_profile if name not in profile]
    if absent:
        raise ContractError(f"execution profile is missing fields: {absent}")
    native_tools = profile["native_tools"]
    if not isinstance(native_tools, list) or not all(isinstance(item, str) and item for item in native_tools):
        raise ContractError("native_tools must be a list of non-empty strings")
    if len(native_tools) != len(set(native_tools)):
        raise ContractError("native_tools contains duplicates")
    surface_requirements = profile["native_surface_requirements"]
    if not isinstance(surface_requirements, list) or not all(
        isinstance(item, str) and item for item in surface_requirements
    ):
        raise ContractError("native_surface_requirements must be a list of non-empty strings")
    if len(surface_requirements) != len(set(surface_requirements)):
        raise ContractError("native_surface_requirements contains duplicates")
    for tool in native_tools:
        if f"tool:{tool}" not in native_map:
            raise ContractError(f"native tool {tool!r} has no semantic capability classification")
    for surface in surface_requirements:
        if surface not in native_map:
            raise ContractError(f"native surface {surface!r} has no semantic capability classification")

    mcp_servers = profile["mcp_servers"]
    if not isinstance(mcp_servers, list):
        raise ContractError("mcp_servers must be a list")
    mcp_names: set[str] = set()
    declared_mcp_tools: list[str] = []
    for index, server in enumerate(mcp_servers):
        if not isinstance(server, dict):
            raise ContractError(f"mcp_servers[{index}] must be an object")
        name = server.get("name")
        transport = server.get("transport")
        server_id = server.get("server_id")
        entrypoint = server.get("entrypoint")
        tools = server.get("tools")
        if not isinstance(name, str) or not name or name in mcp_names:
            raise ContractError(f"mcp_servers[{index}] has invalid/duplicate name")
        mcp_names.add(name)
        if transport != "stdio":
            raise ContractError(f"MCP server {name!r} must use stdio transport")
        if not isinstance(server_id, str) or not server_id:
            raise ContractError(f"MCP server {name!r} has no frozen server_id")
        if not isinstance(entrypoint, str) or not entrypoint:
            raise ContractError(f"MCP server {name!r} has no frozen entrypoint")
        if not isinstance(tools, list) or not tools or not all(isinstance(tool, str) and tool for tool in tools):
            raise ContractError(f"MCP server {name!r} has invalid tool surface")
        if len(tools) != len(set(tools)):
            raise ContractError(f"MCP server {name!r} tool surface contains duplicates")
        if f"mcp_server:{name}" not in native_map:
            raise ContractError(f"MCP server {name!r} has no semantic capability classification")
        # The provider-native registered tool id is whatever the provider exposes for this
        # declared server; it is not derivable from the server name. Binding is established
        # by the frozen exact identity of the server plus the declared id list, never by a
        # naming convention. A provider-native id may belong to exactly one declared server.
        for tool in tools:
            if tool in declared_mcp_tools:
                raise ContractError(
                    f"provider-native MCP tool id {tool!r} is declared by more than one server"
                )
            if tool not in native_tools:
                raise ContractError(f"MCP tool {tool!r} is missing from the exact native tool surface")
            if f"tool:{tool}" not in native_map:
                raise ContractError(f"MCP tool {tool!r} has no semantic capability classification")
            declared_mcp_tools.append(tool)

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
        "native_tools": native_tools,
        "native_surface_requirements": surface_requirements,
        "mcp_servers": mcp_servers,
    }
    # Runtime mode, transform and mechanism are material execution-profile fields.
    for name in ("runtime_mode", "activation_mechanism", "delivery_transform", "runtime_input_template"):
        if name in profile:
            profile_key[name] = profile[name]
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
        native_return_state = payload.get("native_return_state")
        if not isinstance(native_return_state, dict):
            errors.append(f"normalized event {index} termination native_return_state is invalid")
        elif not isinstance(native_return_state.get("is_error"), bool):
            errors.append(
                f"normalized event {index} termination native_return_state.is_error is missing or invalid"
            )
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


def compute_admission_bundle_sha256(
    record: dict[str, Any],
    check_evidence: dict[str, str],
    *,
    role: str = "executor",
    section6_evidence: dict[str, str] | None = None,
) -> str:
    if not isinstance(record, dict):
        raise ContractError("profile admission record must be an object")
    expected_checks = set(_admission_checks_for_role(role))
    if set(check_evidence) != expected_checks:
        raise ContractError(f"{role} admission bundle check evidence does not match canonical check set")
    if role == "executor":
        if not isinstance(record.get("section6"), dict):
            raise ContractError("profile admission section6 matrix is missing")
        if not isinstance(section6_evidence, dict):
            raise ContractError("executor admission bundle requires section6 evidence mapping")
        expected_cells = set(EXECUTOR_SECTION6_CELLS)
        if set(section6_evidence) != expected_cells:
            raise ContractError("executor admission bundle section6 evidence does not match canonical cell set")
        evidence: Any = {"checks": check_evidence, "section6": section6_evidence}
    else:
        evidence = check_evidence
    return stable_json_sha256({"record": record, "evidence": evidence})


def admission_bundle_sha256(admission_path: Path | None, *, role: str = "executor") -> str | None:
    if admission_path is None:
        return None
    payload = _require_object(load_json(admission_path), "profile admission")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        raise ContractError("profile admission checks are malformed")
    check_evidence: dict[str, str] = {}
    for name in _admission_checks_for_role(role):
        row = checks.get(name)
        if not isinstance(row, dict):
            raise ContractError(f"profile admission check {name!r} is missing")
        path = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
        if path is None or not path.is_file():
            raise ContractError(f"profile admission check {name!r} evidence is unavailable")
        check_evidence[name] = sha256_file(path)
    s6_evidence: dict[str, str] | None = None
    if role == "executor":
        section6 = payload.get("section6")
        if not isinstance(section6, dict):
            raise ContractError("profile admission section6 matrix is missing")
        s6_evidence = {}
        for cell_name in EXECUTOR_SECTION6_CELLS:
            row = section6.get(cell_name)
            if not isinstance(row, dict):
                raise ContractError(f"profile admission section6 cell {cell_name!r} is missing")
            path = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
            if path is None or not path.is_file():
                raise ContractError(f"profile admission section6 cell {cell_name!r} evidence is unavailable")
            s6_evidence[cell_name] = sha256_file(path)
    return compute_admission_bundle_sha256(
        payload,
        check_evidence,
        role=role,
        section6_evidence=s6_evidence,
    )


def recompute_profile_admission_snapshot_bundle_sha256(
    run: Path,
    *,
    role: str = "executor",
    prefix: str = "profile-admission",
) -> str:
    snapshot_path = run / f"{prefix}-snapshot.json"
    record_path = run / f"{prefix}.json"
    if not snapshot_path.is_file() or not record_path.is_file():
        raise ContractError(f"{role} profile-admission snapshot is missing")
    snapshot = _require_object(load_json(snapshot_path), "profile admission snapshot")
    record = _require_object(load_json(record_path), f"{role} profile admission record")
    proofs = snapshot.get("proofs")
    if not isinstance(proofs, list):
        raise ContractError(f"{role} profile-admission proof list is malformed")
    expected_checks = set(_admission_checks_for_role(role))
    check_evidence: dict[str, str] = {}
    for row in proofs:
        if not isinstance(row, dict):
            continue
        name = row.get("check")
        if isinstance(name, str) and name in expected_checks and name not in check_evidence:
            proof = _safe_relative_file(run, row.get("path"))
            if proof is None or not proof.is_file():
                raise ContractError(f"{role} profile-admission proof {name!r} is unavailable")
            check_evidence[name] = sha256_file(proof)
    if set(check_evidence) != expected_checks:
        raise ContractError(f"{role} profile-admission snapshot does not contain the exact required check set")
    s6_evidence: dict[str, str] | None = None
    if role == "executor":
        s6_proofs = snapshot.get("section6_proofs")
        if not isinstance(s6_proofs, list):
            raise ContractError(f"{role} profile-admission section6 proof list is missing or malformed")
        expected_cells = set(EXECUTOR_SECTION6_CELLS)
        s6_evidence = {}
        for row in s6_proofs:
            if not isinstance(row, dict):
                continue
            cell_name = row.get("cell") or row.get("check")
            if isinstance(cell_name, str) and cell_name in expected_cells and cell_name not in s6_evidence:
                proof = _safe_relative_file(run, row.get("path"))
                if proof is None or not proof.is_file():
                    raise ContractError(f"{role} profile-admission section6 proof {cell_name!r} is unavailable")
                s6_evidence[cell_name] = sha256_file(proof)
        if set(s6_evidence) != expected_cells:
            raise ContractError(f"{role} profile-admission snapshot does not contain the exact required section6 cell set")
    return compute_admission_bundle_sha256(
        record,
        check_evidence,
        role=role,
        section6_evidence=s6_evidence,
    )


def snapshot_profile_admission(
    admission_path: Path,
    out: Path,
    *,
    role: str,
    prefix: str = "profile-admission",
) -> dict[str, Any]:
    payload = _require_object(load_json(admission_path), "profile admission")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        raise ContractError("profile admission checks are malformed")
    record_path = out / f"{prefix}.json"
    record_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    evidence_root = out / f"{prefix}-evidence"
    evidence_root.mkdir(exist_ok=True)
    rows: list[dict[str, Any]] = []
    for name in _admission_checks_for_role(role):
        row = checks.get(name)
        if not isinstance(row, dict):
            raise ContractError(f"profile admission check {name!r} is missing")
        source = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
        if source is None or not source.is_file():
            raise ContractError(f"profile admission check {name!r} evidence is unavailable")
        target = evidence_root / f"{name}.proof"
        target.write_bytes(source.read_bytes())
        rows.append({
            "check": name,
            "path": target.relative_to(out).as_posix(),
            "sha256": sha256_file(target),
            "bytes": target.stat().st_size,
        })
    snapshot: dict[str, Any] = {
        "schema": SCHEMA,
        "role": role,
        "admission_bundle_sha256": admission_bundle_sha256(admission_path, role=role),
        "record_sha256": sha256_file(record_path),
        "proofs": rows,
    }
    if role == "executor":
        section6 = payload.get("section6")
        if not isinstance(section6, dict):
            raise ContractError("profile admission section6 matrix is missing")
        s6_rows: list[dict[str, Any]] = []
        for cell_name in EXECUTOR_SECTION6_CELLS:
            row = section6.get(cell_name)
            if not isinstance(row, dict):
                raise ContractError(f"profile admission section6 cell {cell_name!r} is missing")
            source = _safe_relative_file(admission_path.parent, row.get("evidence_path"))
            if source is None or not source.is_file():
                raise ContractError(f"profile admission section6 cell {cell_name!r} evidence is unavailable")
            target = evidence_root / f"section6-{cell_name}.proof"
            target.write_bytes(source.read_bytes())
            s6_rows.append({
                "cell": cell_name,
                "path": target.relative_to(out).as_posix(),
                "sha256": sha256_file(target),
                "bytes": target.stat().st_size,
            })
        snapshot["section6_proofs"] = s6_rows
    (out / f"{prefix}-snapshot.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return snapshot


def validate_profile_admission_snapshot(
    run: Path,
    expected_bundle_sha256: str | None,
    *,
    role: str,
    prefix: str = "profile-admission",
) -> list[str]:
    if expected_bundle_sha256 is None:
        return [f"{role} admission bundle identity is missing"]
    snapshot_path = run / f"{prefix}-snapshot.json"
    record_path = run / f"{prefix}.json"
    if not snapshot_path.is_file() or not record_path.is_file():
        return [f"{role} profile-admission snapshot is missing"]
    try:
        snapshot = _require_object(load_json(snapshot_path), "profile admission snapshot")
        record = _require_object(load_json(record_path), f"{role} profile admission record")
    except ContractError as exc:
        return [str(exc)]
    errors: list[str] = []
    if snapshot.get("schema") != SCHEMA or snapshot.get("role") != role:
        errors.append(f"{role} profile-admission snapshot identity is invalid")
    if snapshot.get("admission_bundle_sha256") != expected_bundle_sha256:
        errors.append(f"{role} profile-admission bundle does not match run identity")
    if not _valid_sha256(snapshot.get("record_sha256")) or sha256_file(record_path) != snapshot.get("record_sha256"):
        errors.append(f"{role} profile-admission record hash changed")
    if record.get("status") != "ADMITTED":
        errors.append(f"{role} profile-admission record status is not ADMITTED")
    proofs = snapshot.get("proofs")
    if not isinstance(proofs, list):
        return errors + [f"{role} profile-admission proof list is malformed"]
    expected_checks = set(_admission_checks_for_role(role))
    seen: set[str] = set()
    record_checks = record.get("checks") if isinstance(record.get("checks"), dict) else {}
    check_evidence: dict[str, str] = {}
    for index, row in enumerate(proofs):
        if not isinstance(row, dict):
            errors.append(f"{role} profile-admission proof {index} is malformed")
            continue
        name = row.get("check")
        if not isinstance(name, str) or name not in expected_checks or name in seen:
            errors.append(f"{role} profile-admission proof {index} has invalid check {name!r}")
            continue
        seen.add(name)
        proof = _safe_relative_file(run, row.get("path"))
        if proof is None or not proof.is_file():
            errors.append(f"{role} profile-admission proof {name!r} is unavailable")
            continue
        actual_sha = sha256_file(proof)
        check_evidence[name] = actual_sha
        if row.get("bytes") != proof.stat().st_size:
            errors.append(f"{role} profile-admission proof {name!r} size changed")
        if not _valid_sha256(row.get("sha256")) or actual_sha != row.get("sha256"):
            errors.append(f"{role} profile-admission proof {name!r} hash changed")
        record_check_row = record_checks.get(name)
        if isinstance(record_check_row, dict) and record_check_row.get("evidence_sha256") != row.get("sha256"):
            errors.append(f"{role} profile-admission proof {name!r} hash does not match record")
    if seen != expected_checks:
        errors.append(f"{role} profile-admission snapshot does not contain the exact required check set")

    s6_evidence: dict[str, str] | None = None
    if role == "executor":
        if "section6" not in record or not isinstance(record.get("section6"), dict):
            errors.append(f"{role} profile-admission record section6 matrix is missing")
        s6_proofs = snapshot.get("section6_proofs")
        if not isinstance(s6_proofs, list):
            errors.append(f"{role} profile-admission section6 proof list is missing or malformed")
        else:
            expected_cells = set(EXECUTOR_SECTION6_CELLS)
            seen_cells: set[str] = set()
            record_s6 = record.get("section6") if isinstance(record.get("section6"), dict) else {}
            s6_evidence = {}
            for index, row in enumerate(s6_proofs):
                if not isinstance(row, dict):
                    errors.append(f"{role} profile-admission section6 proof {index} is malformed")
                    continue
                cell_name = row.get("cell") or row.get("check")
                if not isinstance(cell_name, str) or cell_name not in expected_cells or cell_name in seen_cells:
                    errors.append(f"{role} profile-admission section6 proof {index} has invalid cell {cell_name!r}")
                    continue
                seen_cells.add(cell_name)
                proof = _safe_relative_file(run, row.get("path"))
                if proof is None or not proof.is_file():
                    errors.append(f"{role} profile-admission section6 proof {cell_name!r} is unavailable")
                    continue
                actual_sha = sha256_file(proof)
                s6_evidence[cell_name] = actual_sha
                if row.get("bytes") != proof.stat().st_size:
                    errors.append(f"{role} profile-admission section6 proof {cell_name!r} size changed")
                if not _valid_sha256(row.get("sha256")) or actual_sha != row.get("sha256"):
                    errors.append(f"{role} profile-admission section6 proof {cell_name!r} hash changed")
                record_s6_row = record_s6.get(cell_name)
                if isinstance(record_s6_row, dict) and record_s6_row.get("evidence_sha256") != row.get("sha256"):
                    errors.append(f"{role} profile-admission section6 proof {cell_name!r} hash does not match record")
            if seen_cells != expected_cells:
                errors.append(f"{role} profile-admission snapshot does not contain the exact required section6 cell set")

    if len(check_evidence) == len(expected_checks) and (
        role != "executor" or (s6_evidence is not None and len(s6_evidence) == len(expected_cells))
    ):
        try:
            recomputed_bundle_sha = compute_admission_bundle_sha256(
                record,
                check_evidence,
                role=role,
                section6_evidence=s6_evidence,
            )
            if recomputed_bundle_sha != expected_bundle_sha256:
                errors.append(f"{role} profile-admission recomputed bundle does not match run identity")
            if snapshot.get("admission_bundle_sha256") != recomputed_bundle_sha:
                errors.append(f"{role} profile-admission snapshot bundle does not match recomputed digest")
        except ContractError as exc:
            errors.append(f"{role} profile-admission bundle recomputation failed: {exc}")
    else:
        errors.append(f"{role} profile-admission bundle cannot be recomputed: incomplete proof set")

    return errors


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

    if role == "executor":
        section6 = payload.get("section6")
        if not isinstance(section6, dict):
            errors.append("profile admission section6 matrix is missing")
        else:
            expected_cells = set(EXECUTOR_SECTION6_CELLS)
            actual_cells = set(section6)
            missing_cells = sorted(expected_cells - actual_cells)
            unknown_cells = sorted(actual_cells - expected_cells)
            if missing_cells:
                errors.append(f"profile admission section6 is missing required cells: {missing_cells}")
            if unknown_cells:
                errors.append(f"profile admission section6 has unknown cells: {unknown_cells}")
            for cell_name in sorted(expected_cells & actual_cells):
                cell_row = section6[cell_name]
                if not isinstance(cell_row, dict):
                    errors.append(f"profile admission section6 cell {cell_name!r} is not an object")
                    continue
                if cell_row.get("status") != "PASS":
                    errors.append(f"profile admission section6 cell {cell_name!r} did not PASS")
                cell_path = _safe_relative_file(admission_path.parent, cell_row.get("evidence_path"))
                expected_cell_sha = cell_row.get("evidence_sha256")
                if cell_path is None or not cell_path.is_file():
                    errors.append(f"profile admission section6 cell {cell_name!r} evidence is unavailable")
                    continue
                if not _valid_sha256(expected_cell_sha) or sha256_file(cell_path) != expected_cell_sha:
                    errors.append(f"profile admission section6 cell {cell_name!r} evidence hash does not match")
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
    if command_identity.get("tools") != profile.get("native_tools"):
        errors.append("launched exact native-tool surface does not match frozen execution profile")
    if command_identity.get("mcp_servers") != profile.get("mcp_servers"):
        errors.append("launched MCP server identity does not match frozen execution profile")
    expected_mcp_names = [
        server.get("name") for server in (profile.get("mcp_servers") or [])
        if isinstance(server, dict)
    ]
    executable_digests = command_identity.get("mcp_server_executable_sha256")
    if not isinstance(executable_digests, dict) or set(executable_digests) != set(expected_mcp_names):
        errors.append("launched MCP server executable digest set does not match frozen execution profile")
    elif any(not _valid_sha256(value) for value in executable_digests.values()):
        errors.append("launched MCP server executable digest is malformed")
    containment = profile.get("containment_policy")
    if isinstance(containment, dict) and containment.get("kind") == "claude-code-restricted-sandbox-v1":
        sources = containment.get("setting_sources")
        if command_identity.get("setting_sources") != sources:
            errors.append("Claude launch setting sources do not match the frozen containment policy")
        if command_identity.get("restricted") is not (sources == "none"):
            errors.append("Claude launch restricted mode does not match the frozen containment policy")
        if not isinstance(command_identity.get("settings_file"), str) or not command_identity.get("settings_file"):
            errors.append("Claude launch did not bind explicit run-owned settings")
        if not _valid_sha256(command_identity.get("settings_file_sha256")):
            errors.append("Claude launch did not bind the explicit settings bytes")
        if command_identity.get("strict_mcp_config") is not True:
            errors.append("Claude launch did not require strict MCP configuration")
        if not isinstance(command_identity.get("mcp_config_file"), str) or not command_identity.get("mcp_config_file"):
            errors.append("Claude launch did not bind an explicit run-owned MCP configuration")
        if not _valid_sha256(command_identity.get("mcp_config_sha256")):
            errors.append("Claude launch did not bind the MCP configuration bytes")
    if "permission_mode" in profile and command_identity.get("permission_mode") != profile.get("permission_mode"):
        errors.append("launched permission mode does not match frozen execution profile")
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

    expected_mode = bundle.profile.get("permission_mode")
    if expected_mode is not None and observation.get("permission_mode") != expected_mode:
        errors.append(
            f"runtime-observed permission mode {observation.get('permission_mode')!r} does not match "
            f"frozen execution profile {expected_mode!r}"
        )

    declared_tools = bundle.profile.get("native_tools")
    observed_tools = observation.get("tools")
    if not isinstance(observed_tools, list) or not all(isinstance(item, str) and item for item in observed_tools):
        errors.append("runtime init did not expose a valid native tools list")
        observed_tools = []
    elif len(observed_tools) != len(set(observed_tools)):
        errors.append("runtime init native tools list contains duplicates")
    if isinstance(declared_tools, list) and set(observed_tools) != set(declared_tools):
        errors.append(
            f"runtime native-tool surface differs from declared set: declared={sorted(declared_tools)}, "
            f"observed={sorted(observed_tools)}"
        )

    native_map = bundle.capabilities.get("native_capabilities")
    if not isinstance(native_map, dict):
        errors.append("native capability classification map is missing")
        native_map = {}
    for tool in observed_tools:
        if f"tool:{tool}" not in native_map:
            errors.append(f"runtime exposed unclassified native tool {tool!r}")
    observed_caps = observation.get("native_capabilities")
    if not isinstance(observed_caps, list) or not all(isinstance(item, str) and item for item in observed_caps):
        errors.append("runtime init native capabilities list is malformed")
        observed_caps = []
    for capability in observed_caps:
        name = f"runtime_capability:{capability}"
        if name not in native_map:
            errors.append(f"runtime exposed unclassified native capability {capability!r}")
    if observation.get("messaging_socket_path"):
        if "messaging_socket_path" not in native_map:
            errors.append("runtime exposed an unclassified messaging socket")
    memory_paths = observation.get("memory_paths")
    if isinstance(memory_paths, dict) and memory_paths.get("auto"):
        if "auto_memory_write" not in native_map:
            errors.append("runtime exposed unclassified auto-memory state")
    expected_servers = bundle.profile.get("mcp_servers") or []
    expected_names = [server.get("name") for server in expected_servers if isinstance(server, dict)]
    mcp_servers = observation.get("mcp_servers")
    if not isinstance(mcp_servers, list) or not all(isinstance(row, dict) for row in mcp_servers):
        errors.append("runtime init MCP server list is malformed")
        mcp_servers = []
    observed_names: list[str] = []
    for row in mcp_servers:
        name = row.get("name")
        status = row.get("status")
        if not isinstance(name, str) or not name:
            errors.append("runtime exposed MCP server without stable name")
            continue
        observed_names.append(name)
        if status != "connected":
            errors.append(f"runtime MCP server {name!r} is not connected")
        if f"mcp_server:{name}" not in native_map:
            errors.append(f"runtime exposed unclassified MCP server {name!r}")
    if len(observed_names) != len(set(observed_names)):
        errors.append("runtime init MCP server list contains duplicates")
    if set(observed_names) != set(expected_names):
        errors.append(
            f"runtime MCP server surface differs from declared set: declared={sorted(expected_names)}, "
            f"observed={sorted(observed_names)}"
        )

    exposed_surfaces = {f"tool:{tool}" for tool in observed_tools}
    exposed_surfaces.update(f"mcp_server:{name}" for name in observed_names)
    exposed_surfaces.update(f"runtime_capability:{capability}" for capability in observed_caps)
    if observation.get("messaging_socket_path"):
        exposed_surfaces.add("messaging_socket_path")
    if isinstance(memory_paths, dict) and memory_paths.get("auto"):
        exposed_surfaces.add("auto_memory_write")
    for required in bundle.profile.get("native_surface_requirements", []):
        if required not in exposed_surfaces:
            errors.append(f"runtime did not expose required classified native surface {required!r}")
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



PURPOSES = frozenset({"qualification", "oracle-integrity", "development"})


def validate_accounting_identity(identity: dict[str, Any]) -> list[str]:
    scope = identity.get("accounting")
    errors = []
    if not isinstance(scope, dict) or scope.get("purpose") not in PURPOSES:
        return ["missing or malformed frozen evidence-accounting scope"]
    for name in ("manifest_sha256", "scoring_manifest_sha256"):
        if not _valid_sha256(scope.get(name)):
            errors.append(f"accounting {name} is missing or malformed")
    if not isinstance(scope.get("scope_id"), str) or not scope["scope_id"]:
        errors.append("accounting campaign/suite identity is missing")
    req = identity.get("requirements") or {}
    if scope.get("scoring_manifest_sha256") != req.get("expected_scoring_items_sha256"):
        errors.append("accounting scoring manifest differs from frozen run requirements")
    if identity.get("execution_mode") == "qualification" and scope.get("purpose") != "qualification":
        errors.append("qualification execution cannot import integrity/development evidence")
    if scope.get("purpose") == "qualification":
        for name in ("campaign_record_sha256", "family_record_sha256", "primary_family_id"):
            if not _valid_sha256(scope.get(name)):
                errors.append(f"qualification {name} is missing or malformed")
        if identity.get("execution_mode") != "qualification":
            parent = scope.get("integrity_test_campaign")
            if not isinstance(parent, dict) or parent.get("purpose") != "oracle-integrity" or not _valid_sha256(parent.get("suite_sha256")):
                errors.append("qualification scope in probe mode requires a predeclared outer integrity test campaign")
    manifest = identity.get("accounting_manifest")
    if manifest is not None:
        errors.extend(campaign_manifest_errors(manifest))
        if stable_json_sha256(manifest) != scope.get("manifest_sha256") or manifest.get("purpose") != scope.get("purpose"):
            errors.append("launch manifest purpose/digest mismatch")
    elif scope.get("purpose") != "development":
        errors.append("non-development scope requires its frozen campaign/suite manifest")
    digest = identity.get("identity_sha256")
    if digest != stable_json_sha256({k: v for k, v in identity.items() if k != "identity_sha256"}):
        errors.append("launch identity digest differs from its frozen contents")
    return errors


def assessment_accounting(identity: dict[str, Any]) -> dict[str, Any]:
    errors = validate_accounting_identity(identity)
    if errors:
        raise ContractError("; ".join(errors))
    return {"accounting": identity["accounting"], "run_identity_sha256": identity["identity_sha256"]}


def local_criteria(summary: dict[str, Any], identity: dict[str, Any]) -> dict[str, str]:
    """An activation FAIL is independent of doctrine scoring on inadmissible evidence."""
    errors = validate_accounting_identity(identity)
    if summary.get("accounting") != identity.get("accounting"):
        errors.append("post-launch accounting change")
    result = {"harness/admissibility": "PASS" if not errors and summary.get("evidence_state") == "COMPLETE_ADMISSIBLE" else "FAIL"}
    if identity.get("entry_stratum") == "deterministic":
        result["deterministic activation"] = "PASS" if summary.get("activation", {}).get("delivered") is True and not errors else "FAIL"
    else:
        result["deterministic activation"] = "NOT_EVALUATED"
    return result


def integrity_assessment(actual: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    """Outer assessment compares the retained production result, without changing it."""
    keys = {"evidence_state", "criteria", "qualification_outcome"}
    if set(expected) != keys or not all(key in actual for key in keys):
        return {"integrity_outcome": "FAIL", "reason": "missing/malformed frozen expected or actual result", "actual": actual}
    passed = all(actual[key] == expected[key] for key in keys)
    return {"integrity_outcome": "PASS" if passed else "FAIL", "actual": json.loads(json.dumps(actual)), "expected": expected}

def validate_complete_run(run: Path, identity: dict[str, Any], requirements: Requirements) -> list[str]:
    errors: list[str] = []
    try:
        prior = _require_object(load_json(run / "run-identity.json"), "run identity")
        summary = _require_object(load_json(run / "summary.json"), "run summary")
        snapshot_payload = load_json(run / "requirements-snapshot.json")
    except ContractError as exc:
        return [str(exc)]
    errors.extend(validate_accounting_identity(identity))
    if summary.get("accounting") != identity.get("accounting"):
        errors.append("summary accounting purpose/bindings differ from frozen launch identity")
    if prior != identity:
        errors.append("stored run identity does not match current identity")
    if summary.get("run_identity_sha256") != identity.get("identity_sha256"):
        errors.append("run summary identity does not match current identity")
    if summary.get("evidence_state") != "COMPLETE_ADMISSIBLE" or summary.get("execution_ok") is not True:
        errors.append("run summary is not COMPLETE_ADMISSIBLE with successful execution")
    if identity.get("execution_mode") == "qualification":
        errors.extend(validate_profile_admission_snapshot(
            run,
            identity.get("profile_admission_sha256"),
            role="executor",
            prefix="profile-admission",
        ))
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

# Complete criterion parts, including report-only exposure, shared by freezing and aggregation.
# (criterion, panel, minimum independent opportunities per arm, maximum failed parts)
CAMPAIGN_PARTS = {
    "harness": ("harness/admissibility", "all", 1, 0),
    "activation": ("deterministic activation", "deterministic", 1, 0),
    "critical": ("no critical failure", "main", 12, 0),
    "noncritical_detection": ("absolute floors", "main", 20, None),
    "unnamed_detection": ("absolute floors", "main", 6, None),
    "null": ("absolute floors", "main", 6, 0),
    "variant": ("absolute floors", "main", 6, 0),
    "provenance": ("absolute floors", "main", 6, 0),
    "delegated_finding": ("absolute floors", "main", 6, 0),
    "delegate_request": ("absolute floors", "main", 12, 0),
    "claim_integrity": ("absolute floors", "main", 1, 0),
    "o3": ("absolute floors", "main", 6, 0),
    "unauthorized_mutation": ("absolute floors", "main", 6, 0),
    "false_surfacing": ("absolute floors", "main", 20, None),
    "r2_analysis": ("6.6 preservation", "r2", 6, None),
    "r2_authority": ("6.6 preservation", "r2", 6, None),
    "r2_gate": ("6.6 preservation", "r2", 6, None),
    "r2_authoring": ("6.6 preservation", "r2", 2, None),
    "r2_review": ("6.6 preservation", "r2", 2, None),
    "owner_false_activation": ("6.6 preservation", "all", 1, 0),
    "predicate_false_firing": ("6.6 preservation", "all", 12, 1),
    "selection_negative": ("6.6 preservation", "ordinary", 1, None),
    "near_negative": ("6.6 preservation", "ordinary", 8, None),
    "routing_hits": ("6.6 preservation", "routing", 38, None),
    "routing_violations": ("6.6 preservation", "routing", 38, None),
    "routing_case_extremes": ("6.6 preservation", "routing", 19, 0),
    "t2_t3": ("6.6 preservation", "sentinels", 4, 0),
    "t4_t6": ("6.6 preservation", "versioning", 8, None),
    "never_stated": ("6.6 preservation", "versioning", 8, None),
    "sentinel_regression": ("6.6 preservation", "sentinels", 1, 0),
    "fixed_cost": ("burden", "burden", 3, None),
    "no_lookup": ("burden", "burden", 3, 0),
    "panel_correctness": ("burden", "burden", 3, 0),
    "active_material": ("burden", "main", 1, None),
    "unowed_owner": ("burden", "main", 1, 0),
    "unauthorized_shared_probe": ("burden", "main", 1, 0),
    "unowed_delegate": ("burden", "main", 12, 1),
    "unowed_gap": ("burden", "main", 12, 1),
    "blanket_withholding": ("burden", "main", 1, 0),
    "report_length": ("burden", "main", 1, None),
    "elapsed_time": ("burden", "main", 1, None),
    "comparative": ("comparative benefit", "main", 1, None),
    "human_routine": ("human trial", "main", 20, None),
    "human_critical": ("human trial", "main", 4, 0),
    "human_time": ("human trial", "main", 20, None),
    "selection_correct_reporting": ("report-only", "ordinary", 32, None),
    **{f"ordinary_{kind}": ("report-only", "ordinary", 3, None)
       for kind in ("run", "adhoc", "review", "gate", "copy_relay", "delegate")},
}
CRITERION_ORDER = ("harness/admissibility", "deterministic activation", "no critical failure", "absolute floors",
                   "6.6 preservation", "burden", "comparative benefit", "human trial")
FAMILY_SERIALIZATION = "json-sort-keys-compact-utf8"


def family_id(record: dict[str, Any]) -> str:
    return stable_json_sha256({"ordered_keys": record["ordered_keys"], "criterion_to_keys": record["criterion_to_keys"]})


def validate_family(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["missing primary family record"]
    errors = []
    try:
        if record["serialization"] != FAMILY_SERIALIZATION or record["hash_algorithm"] != "sha256":
            errors.append("family serialization/hash algorithm is unsupported")
        keys, profiles, mapping, panels = record["ordered_keys"], record["profile_keys"], record["criterion_to_keys"], record["panels"]
        if not isinstance(keys, list) or len(keys) < 2 or len(set(keys)) != len(keys) or set(keys) != set(profiles):
            return errors + ["family ordered key set is missing, duplicated or mismatched"]
        if any(not _valid_sha256(key) or stable_json_sha256(profiles[key]) != key for key in keys):
            errors.append("family execution-profile key digest mismatch")
        if set(mapping) != set(CAMPAIGN_PARTS):
            errors.append("family criterion-part map is incomplete or has unknown parts")
        if record.get("family_id") != family_id(record):
            errors.append("family id does not bind ordered keys and complete criterion-part map")
        if set(panels) != {"main", "burden", "ordinary", "routing", "sentinels", "versioning", "r2"}:
            return errors + ["family panel budget schedule is incomplete"]
        main = profiles[panels["main"]["key"]]
        shared_fields = ("agent_model", "provider_runtime", "runtime_mode", "reasoning_configuration", "adapter_id",
                         "containment_policy", "network_external_write_policy", "credential_service_account_policy",
                         "workspace_realization", "install_mechanism", "provider_managed_unknowns")
        if main["agent_model"] != "deepinfra/zai-org/GLM-5.3-Flash":
            errors.append("primary family model needs a separately resolved written stakeholder designation")
        for key in keys:
            if any(profiles[key].get(field) != main.get(field) for field in shared_fields):
                errors.append("family shared fields differ across execution keys")
        ordinary_key = panels["ordinary"]["key"]
        deterministic = [key for key in keys if key != ordinary_key]
        if profiles[ordinary_key].get("activation_mechanism") != "ordinary-read":
            errors.append("ordinary-entry key mechanism is missing or wrong")
        for key in deterministic:
            if profiles[key].get("runtime_mode") != "rpc" or profiles[key].get("activation_mechanism") != "runtime-command":
                errors.append("primary deterministic keys require real runtime-command in RPC mode")
        for panel, row in panels.items():
            key = row["key"]
            expected = 3 if panel == "ordinary" else 8 if panel == "routing" else 60
            if key not in keys or row["max_turns"] != expected or profiles[key]["budgets"]["max_turns"] != expected:
                errors.append(f"panel {panel} budget/key schedule differs from frozen contract")
        burden = profiles[panels["burden"]["key"]]
        if any("delegate" in name for name in burden.get("native_tools", [])):
            errors.append("T1/T7/T8 key exposes delegated-agent capability")
        for part, (_, panel, _, _) in CAMPAIGN_PARTS.items():
            assigned = mapping.get(part)
            expected = keys if panel == "all" else deterministic if panel == "deterministic" else [panels[panel]["key"]]
            if assigned != expected:
                errors.append(f"criterion part {part} has wrong or missing ordered key assignments")
        if record.get("aggregation") != {"owner_false_activation": "pool-all-keys", "predicate_false_firing": "pool-all-keys", "failures": "never-remove"}:
            errors.append("family aggregation rules are missing or weakened")
    except (KeyError, TypeError, ValueError):
        errors.append("family record is malformed")
    return errors


def campaign_manifest_errors(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["campaign/suite manifest is not an object"]
    if manifest.get("purpose") not in PURPOSES or not isinstance(manifest.get("scope_id"), str):
        return ["campaign/suite purpose or identity is missing"]
    errors = []
    runs = manifest.get("runs")
    if not isinstance(runs, list) or not runs:
        return ["campaign/suite must enumerate every declared realization before launch"]
    seen = set()
    for row in runs:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or row["id"] in seen:
            errors.append("declared realization identity is malformed or duplicated")
            continue
        seen.add(row["id"])
        if row.get("entry_stratum") not in ("deterministic", "ordinary"):
            errors.append("declared entry stratum is missing")
        if not _valid_sha256(row.get("profile_key_sha256")) or not _valid_sha256(row.get("scoring_manifest_sha256")):
            errors.append("declared profile/scoring identity is missing")
        if not isinstance(row.get("subject"), dict) or not _valid_sha256(row["subject"].get("package_sha256")) or not re.fullmatch(r"[a-f0-9]{40}", str(row["subject"].get("commit", ""))):
            errors.append("declared immutable subject identity is missing")
        if manifest["purpose"] == "oracle-integrity":
            expected = row.get("expected")
            if not isinstance(expected, dict) or set(expected) != {"evidence_state", "criteria", "qualification_outcome"} or not isinstance(row.get("fault"), str):
                errors.append("integrity fault/expected assessment is not frozen")
    if manifest["purpose"] == "qualification":
        family = manifest.get("family")
        errors.extend(validate_family(family))
        if manifest.get("family_record_sha256") != stable_json_sha256(family):
            errors.append("campaign family digest mismatch")
        offered = manifest.get("offered_profiles")
        if not isinstance(offered, list) or not offered or len(set(offered)) != len(offered):
            errors.append("offered profile set is missing or duplicated")
        elif isinstance(family, dict) and not set(family.get("ordered_keys", [])) <= set(offered):
            errors.append("offered profile set omits a primary family key")
        if any(row.get("profile_key_sha256") not in (offered or []) for row in runs):
            errors.append("campaign realization is outside the frozen offered set")
        if not isinstance(manifest.get("prior_campaigns"), list):
            errors.append("prior campaign lineage disclosure is missing")
    return errors


def production_assessment(summary: dict[str, Any], identity: dict[str, Any], requirements: Requirements,
                          dispositions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    result = {**assessment_accounting(identity), "evidence_state": summary.get("evidence_state"),
              "criteria": local_criteria(summary, identity), "qualification_outcome": "NOT_EVALUATED",
              "resource_observation": summary.get("resource_observation", {"exact": False})}
    if summary.get("accounting") != identity["accounting"]:
        raise ContractError("post-launch purpose/campaign/scoring change")
    if summary.get("evidence_state") == "COMPLETE_ADMISSIBLE" and dispositions is not None:
        result["qualification_outcome"] = outcome_from_dispositions(dispositions, requirements)
        result["dispositions"] = dispositions
    return result
