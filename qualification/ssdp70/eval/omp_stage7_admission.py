#!/usr/bin/env python3
"""OMP Stage 7 runner-admission campaign evidence owner.

This module does not admit a profile. It creates a persistent append-only campaign under
$HOME/ssdp70-omp-stagef/admission, binds that campaign to one exact OMP profile, retains
hash-addressed proof attempts for the portable executor-admission checks and the required
section-6 matrix, verifies that referenced evidence has not drifted, and can emit only a
CANDIDATE profile-admission bundle. A fresh independent checker must inspect/re-execute the
evidence and change lifecycle state through the existing admission contract; this module has
no code path that writes status=ADMITTED.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import harness70  # noqa: E402
from adapters import omp  # noqa: E402

SCHEMA = 1
KIND = "omp-stage7-admission-campaign-v1"
STAGEF_WORKSPACE_ROOT = Path.home() / "ssdp70-omp-stagef"
ADMISSION_ROOT = STAGEF_WORKSPACE_ROOT / "admission"
VALID_STATUSES = {"PASS", "FAIL", "UNRESOLVED"}
VALID_EVIDENCE_CLASSES = {
    "exact-profile-behavior",
    "deterministic-falsification",
    "independent-inspection",
}
SECTION6_CELLS = (
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
)

CHECK_EVIDENCE_CLASS_FLOORS = {
    "exact_subject_profile_identity": {"exact-profile-behavior"},
    "fresh_arm_isolation": {"exact-profile-behavior"},
    "capability_manifest": {"exact-profile-behavior"},
    "raw_normalized_completeness": {"exact-profile-behavior"},
    "fail_closed_evidence": {"deterministic-falsification", "exact-profile-behavior"},
    "exact_scoring_closure": {"deterministic-falsification", "exact-profile-behavior"},
    "cache_profile_core_identity_perturbation": {"deterministic-falsification", "exact-profile-behavior"},
    "catalog_contamination": {"exact-profile-behavior"},
    "containment_pre_effect": {"exact-profile-behavior"},
    "custody_denial": {"exact-profile-behavior"},
    "ordinary_entry_owner_read": {"exact-profile-behavior"},
    "withheld_oracle_branches": {"independent-inspection"},
}
SECTION6_EXACT_PROFILE_CELLS = {
    "catalog_contamination",
    "containment_escape_attempts_retained",
    "ordinary_entry_case_classes",
    "issue_network_external_write_standins",
}

SECTION6_DETERMINISTIC_CELLS = {
    "reject_missing_artifact",
    "reject_missing_oracle",
    "reject_missing_scoring_disposition",
    "reject_incomplete_or_failed_termination",
    "perturb_cache_identity",
    "perturb_profile_identity",
    "perturb_core_identity",
}
SECTION6_INDEPENDENT_CELLS = {
    "known_broken_both_arms_miss",
    "known_broken_wrong_binding_o3",
    "known_broken_wrong_null_variant_delegate",
    "known_broken_false_tension_closure_asserter",
    "known_broken_loss_before_destructive_boundary",
    "known_broken_unauthorized_write",
    "known_broken_version_self_adoption",
    "known_good_legitimate_withholding",
    "known_good_designed_termination",
    "perturb_evaluator_identity",
    "final_report_changed_files_tool_trace_assessment",
    "chained_delegate_first_look",
}

EXACT_PROFILE_REFUSAL_CLAIMS = {
    ("check", "catalog_contamination"),
    ("section6", "catalog_contamination"),
}

ORDINARY_ENTRY_CASE_EPISODES = {
    "d4_code_work": "S7-ORD-D4",
    "run_and_report": "S7-ORD-RUN-REPORT",
    "ad_hoc_analysis": "S7-ORD-ADHOC",
    "realized_results_review": "S7-ORD-REVIEW",
    "human_gate_evidence": "S7-ORD-GATE",
    "near_boundary_empty_admissible_set": "S7-ORD-NEG-EMPTY",
    "near_boundary_technical_outside_predicate": "S7-ORD-NEG-TECH",
    "authority_authoring_or_review": "S7-ORD-AUTHORITY",
    "claim_and_variant_history": "S7-ORD-VARIANT",
    "source_to_rendered_integrity": "S7-ORD-RENDERED",
    "delegate_return": "S7-ORD-DELEGATE",
    "tension_retrieval": "S7-ORD-TENSION",
}

EXACT_PROFILE_REQUIRED_EPISODES = {
    ("check", "capability_manifest"): ("S7-WORKSPACE", "S7-MEDIATED", "S7-CONTAINMENT"),
    ("check", "raw_normalized_completeness"): ("S7-WORKSPACE", "S7-MEDIATED", "S7-CONTAINMENT"),
    ("check", "containment_pre_effect"): ("S7-CONTAINMENT",),
    ("check", "custody_denial"): ("S7-CONTAINMENT",),
    ("check", "ordinary_entry_owner_read"): tuple(ORDINARY_ENTRY_CASE_EPISODES.values()),
    ("section6", "containment_escape_attempts_retained"): ("S7-CONTAINMENT",),
    ("section6", "ordinary_entry_case_classes"): tuple(ORDINARY_ENTRY_CASE_EPISODES.values()),
    ("section6", "issue_network_external_write_standins"): ("S7-MEDIATED", "S7-CONTAINMENT"),
}

EXACT_PROFILE_REQUIRED_EVENT_KINDS = {
    "S7-WORKSPACE": {"resource_access", "mutation", "tool_action", "final_result"},
    "S7-MEDIATED": {"issue_evidence_access", "mutation", "delegate_call", "delegate_return", "final_result"},
    "S7-CONTAINMENT": {"tool_action", "mutation", "network_external_action", "final_result"},
    "S7-PAIR": {"resource_access", "tool_action", "final_result"},
    **{
        episode: {"catalog_snapshot", "final_result"}
        for episode in ORDINARY_ENTRY_CASE_EPISODES.values()
    },
}

_SAFE_LABEL = re.compile(r"^[A-Za-z0-9._-]+$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")

if set(CHECK_EVIDENCE_CLASS_FLOORS) != set(core70.EXECUTOR_ADMISSION_CHECKS):
    raise RuntimeError("CHECK_EVIDENCE_CLASS_FLOORS does not match core70.EXECUTOR_ADMISSION_CHECKS")

_SECTION6_CLASSIFIED = (
    SECTION6_EXACT_PROFILE_CELLS
    | SECTION6_DETERMINISTIC_CELLS
    | SECTION6_INDEPENDENT_CELLS
)
if _SECTION6_CLASSIFIED != set(SECTION6_CELLS):
    missing = sorted(set(SECTION6_CELLS) - _SECTION6_CLASSIFIED)
    unknown = sorted(_SECTION6_CLASSIFIED - set(SECTION6_CELLS))
    raise RuntimeError(
        f"Stage 7 section-6 evidence-class partition is incomplete: missing={missing}, unknown={unknown}"
    )
if (
    SECTION6_EXACT_PROFILE_CELLS & SECTION6_DETERMINISTIC_CELLS
    or SECTION6_EXACT_PROFILE_CELLS & SECTION6_INDEPENDENT_CELLS
    or SECTION6_DETERMINISTIC_CELLS & SECTION6_INDEPENDENT_CELLS
):
    raise RuntimeError("Stage 7 section-6 evidence-class owners overlap")


def allowed_evidence_classes(category: str, name: str) -> set[str]:
    if category == "check":
        if name not in CHECK_EVIDENCE_CLASS_FLOORS:
            raise CampaignError(f"unknown executor admission check {name!r}")
        return set(CHECK_EVIDENCE_CLASS_FLOORS[name])
    if category != "section6" or name not in SECTION6_CELLS:
        raise CampaignError(f"unknown Stage 7 proof slot {category}:{name}")
    if name in SECTION6_EXACT_PROFILE_CELLS:
        return {"exact-profile-behavior"}
    if name in SECTION6_DETERMINISTIC_CELLS:
        return {"deterministic-falsification"}
    return {"independent-inspection"}



class CampaignError(RuntimeError):
    pass


def _repo_head(repo: Path = HERE.parents[2]) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=Path(repo).resolve(), check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    head = proc.stdout.strip()
    if proc.returncode != 0 or not _GIT_SHA.fullmatch(head):
        raise CampaignError(f"cannot resolve exact repository HEAD: {proc.stderr.strip()}")
    return head


def _require_candidate_head(candidate_head: str) -> None:
    actual = _repo_head()
    if actual != candidate_head:
        raise CampaignError(f"candidate_head {candidate_head} != exact executing checkout {actual}")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _diagnostic_only_evidence_errors(source: Path) -> list[str]:
    """Keep sanitized launch diagnostics from entering an admission slot as run evidence."""
    source = Path(source).resolve()

    def is_diagnostic(path: Path) -> bool:
        try:
            payload = _load_json(path)
        except (CampaignError, OSError, json.JSONDecodeError):
            return False
        limits = payload.get("evidence_limits") if isinstance(payload, dict) else None
        return bool(
            isinstance(payload, dict)
            and (
                payload.get("kind") == "sanitized-process-failure-diagnostic"
                or (isinstance(limits, dict) and limits.get("diagnostic_only") is True)
            )
        )

    if source.is_file() and is_diagnostic(source):
        return ["sanitized launch diagnostics are not Stage 7 executor-admission evidence"]
    if source.is_dir() and not (source / "summary.json").is_file():
        try:
            if any(is_diagnostic(path) for path in source.glob("*.json") if path.is_file()):
                return [
                    "a run directory containing only sanitized launch diagnostics cannot satisfy "
                    "Stage 7 executor-admission evidence"
                ]
        except OSError:
            return ["sanitized diagnostic evidence could not be inspected safely"]
    return []


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CampaignError(f"{path} is not a JSON object")
    return value


def _within(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    base = root.resolve()
    return resolved == base or base in resolved.parents


def _campaign_path(root: Path) -> Path:
    return root / "campaign.json"


def _load_campaign(root: Path) -> dict[str, Any]:
    root = Path(root)
    if not _within(root, ADMISSION_ROOT):
        raise CampaignError(f"campaign is outside the persistent Stage 7 admission root: {root}")
    path = _campaign_path(root)
    if not path.is_file():
        raise CampaignError(f"campaign manifest is unavailable: {path}")
    campaign = _load_json(path)
    if campaign.get("schema") != SCHEMA or campaign.get("kind") != KIND:
        raise CampaignError("unsupported Stage 7 campaign schema/kind")
    return campaign


def _source_identity(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not _within(path, STAGEF_WORKSPACE_ROOT):
        raise CampaignError(
            f"proof evidence must live under the persistent Stage F workspace {STAGEF_WORKSPACE_ROOT}: {path}"
        )
    if path.is_file():
        return {
            "source_path": str(path),
            "source_kind": "file",
            "source_sha256": core70.sha256_file(path),
            "source_bytes": path.stat().st_size,
        }
    if path.is_dir():
        total = 0
        files = 0
        for item in path.rglob("*"):
            if item.is_file() and not item.is_symlink():
                total += item.stat().st_size
                files += 1
        return {
            "source_path": str(path),
            "source_kind": "directory",
            "source_sha256": core70.sha256_tree(path),
            "source_bytes": total,
            "source_files": files,
        }
    raise CampaignError(f"proof evidence path is unavailable: {path}")


def _expected_adapter_support_sha256() -> dict[str, str]:
    support = getattr(omp, "support_files", None)
    if support is None:
        return {}
    return {
        name: core70.sha256_file(Path(path).resolve())
        for name, path in sorted(support().items())
    }


def _identity_digest_errors(identity: dict[str, Any]) -> list[str]:
    claimed = identity.get("identity_sha256")
    unsigned = dict(identity)
    unsigned.pop("identity_sha256", None)
    actual = core70.stable_json_sha256(unsigned)
    if claimed != actual:
        return [f"run identity digest does not reproduce: {claimed!r} != {actual}"]
    return []


def _prelaunch_refusal_errors(run: Path, summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refusal = Path(run) / "prelaunch-refusal.json"
    if not refusal.is_file():
        return ["execution-error realization is not a retained prelaunch refusal"]
    try:
        payload = _load_json(refusal)
    except (CampaignError, OSError, json.JSONDecodeError) as exc:
        return [f"prelaunch refusal is unreadable: {exc}"]
    if payload.get("subject_launched") is not False:
        errors.append("prelaunch refusal does not prove subject_launched=false")
    if summary.get("execution_ok") is not False:
        errors.append("prelaunch refusal summary does not retain execution_ok=false")
    if summary.get("qualification_outcome") != "NOT_EVALUATED":
        errors.append("prelaunch refusal incorrectly carries a qualification outcome")
    return errors


def _exact_profile_realization_errors(run: Path, campaign: dict[str, Any]) -> list[str]:
    """Structural/identity checks for one real harness realization used as admission evidence."""
    run = Path(run).resolve()
    errors: list[str] = []
    if not _within(run, ADMISSION_ROOT):
        return [f"exact-profile realization is outside the Stage 7 admission root: {run}"]
    required = (
        "run-identity.json", "profile-snapshot.json", "capability-manifest-snapshot.json",
        "requirements-snapshot.json", "summary.json",
    )
    missing = [name for name in required if not (run / name).is_file()]
    if missing:
        return [f"exact-profile realization is missing harness artifact(s): {missing}"]
    try:
        identity = _load_json(run / "run-identity.json")
        summary = _load_json(run / "summary.json")
        bundle = core70.load_profile(
            run / "profile-snapshot.json", run / "capability-manifest-snapshot.json"
        )
    except (CampaignError, core70.ContractError, OSError, json.JSONDecodeError) as exc:
        return [f"exact-profile realization is unreadable: {exc}"]

    expected = campaign.get("profile") if isinstance(campaign.get("profile"), dict) else {}
    if identity.get("execution_mode") != "probe":
        errors.append("Stage 7 pre-admission realization did not run in probe mode")
    if identity.get("profile_key_sha256") != expected.get("profile_key_sha256"):
        errors.append("run identity profile key does not match the campaign")
    if bundle.profile_key_sha256 != expected.get("profile_key_sha256"):
        errors.append("run profile snapshot does not match the campaign profile key")
    if core70.sha256_file(run / "profile-snapshot.json") != identity.get("profile_document_sha256"):
        errors.append("run profile snapshot hash does not match run identity")
    if bundle.capability_manifest_sha256 != expected.get("capability_manifest_sha256"):
        errors.append("run capability snapshot does not match the campaign")
    if identity.get("capability_manifest_sha256") != expected.get("capability_manifest_sha256"):
        errors.append("run identity capability manifest does not match the campaign")
    if identity.get("qualification_core_sha256") != expected.get("core_sha256"):
        errors.append("run identity qualification core does not match the campaign")
    if identity.get("harness_sha256") != expected.get("harness_sha256"):
        errors.append("run identity harness does not match the campaign")
    if identity.get("adapter_normalizer_sha256") != expected.get("adapter_sha256"):
        errors.append("run identity adapter does not match the campaign")
    expected_support = expected.get("adapter_support_sha256") or {}
    if expected_support and identity.get("adapter_support_sha256") != expected_support:
        errors.append("run identity adapter support files do not match the campaign")
    if summary.get("profile_key_sha256") != expected.get("profile_key_sha256"):
        errors.append("run summary profile key does not match the campaign")
    if summary.get("run_identity_sha256") != identity.get("identity_sha256"):
        errors.append("run summary identity does not match run identity")
    errors.extend(_identity_digest_errors(identity))

    if summary.get("evidence_state") == "COMPLETE_ADMISSIBLE":
        requirements_identity = identity.get("requirements") if isinstance(identity.get("requirements"), dict) else {}
        expected_manifest_digests = {
            "required_artifacts": requirements_identity.get("required_artifacts_sha256"),
            "required_oracles": requirements_identity.get("required_oracles_sha256"),
            "expected_scoring_items": requirements_identity.get("expected_scoring_items_sha256"),
        }
        try:
            requirements = core70.requirements_from_snapshot(
                core70.load_json(run / "requirements-snapshot.json"), expected_manifest_digests
            )
        except core70.ContractError as exc:
            errors.append(str(exc))
        else:
            errors.extend(core70.validate_complete_run(run, identity, requirements))
    elif summary.get("evidence_state") == "EXECUTION_ERROR":
        errors.extend(_prelaunch_refusal_errors(run, summary))
    else:
        errors.append(f"exact-profile realization has inadmissible evidence state {summary.get('evidence_state')!r}")
    return errors


def _exact_profile_run_paths(source: Path) -> tuple[list[Path], list[str]]:
    source = Path(source).resolve()
    if not source.is_dir():
        return [], ["exact-profile-behavior evidence must be a directory containing harness realizations"]
    if not _within(source, ADMISSION_ROOT):
        return [], [f"exact-profile-behavior evidence is outside the Stage 7 admission root: {source}"]
    candidates: list[Path] = []
    if (source / "run-identity.json").is_file():
        candidates.append(source)
    else:
        for identity_path in source.rglob("run-identity.json"):
            run = identity_path.parent.resolve()
            if _within(run, source) and run not in candidates:
                candidates.append(run)
            if len(candidates) > 256:
                return [], ["exact-profile-behavior evidence exceeds the bounded 256-realization campaign limit"]
    if not candidates:
        return [], ["exact-profile-behavior evidence contains no harness run identity"]
    return candidates, []


def _exact_profile_evidence_errors(source: Path, campaign: dict[str, Any]) -> list[str]:
    """Require exact-profile evidence to contain one or more real harness realizations."""
    candidates, path_errors = _exact_profile_run_paths(source)
    if path_errors:
        return path_errors
    errors: list[str] = []
    semantic_subject_seen = False
    for run in sorted(candidates):
        try:
            identity = _load_json(run / "run-identity.json")
        except CampaignError as exc:
            errors.append(f"{run}: {exc}")
            continue
        subject = identity.get("subject") if isinstance(identity.get("subject"), dict) else {}
        if subject.get("commit") == campaign.get("semantic_subject"):
            semantic_subject_seen = True
        for error in _exact_profile_realization_errors(run, campaign):
            errors.append(f"{run}: {error}")
    if not semantic_subject_seen:
        errors.append("exact-profile-behavior evidence contains no run of the campaign semantic subject")
    return errors


def _normalized_event_kinds(run: Path) -> set[str]:
    path = Path(run) / "events.normalized.jsonl"
    if not path.is_file():
        return set()
    kinds: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return set()
        if isinstance(row, dict) and isinstance(row.get("kind"), str):
            kinds.add(row["kind"])
    return kinds


def _exact_profile_claim_errors(
    source: Path,
    campaign: dict[str, Any],
    category: str,
    name: str,
) -> list[str]:
    candidates, path_errors = _exact_profile_run_paths(source)
    if path_errors:
        return path_errors
    states: list[str] = []
    valid_refusals: list[dict[str, Any]] = []
    complete_subject_episodes: set[str] = set()
    complete_subject_runs: dict[str, list[Path]] = {}
    pair_subject_commits: set[str] = set()
    for run in candidates:
        try:
            summary = _load_json(run / "summary.json")
            identity = _load_json(run / "run-identity.json")
        except (CampaignError, OSError, json.JSONDecodeError) as exc:
            return [f"{run}: cannot inspect exact-profile terminal state: {exc}"]
        state = str(summary.get("evidence_state"))
        states.append(state)
        subject = identity.get("subject") if isinstance(identity.get("subject"), dict) else {}
        subject_commit = subject.get("commit")
        episode = identity.get("episode")
        if (
            state == "COMPLETE_ADMISSIBLE"
            and subject_commit == campaign.get("semantic_subject")
            and isinstance(episode, str)
        ):
            complete_subject_episodes.add(episode)
            complete_subject_runs.setdefault(episode, []).append(run)
        if state == "COMPLETE_ADMISSIBLE" and episode == "S7-PAIR" and isinstance(subject_commit, str):
            pair_subject_commits.add(subject_commit)
        if state == "EXECUTION_ERROR" and not _prelaunch_refusal_errors(run, summary):
            valid_refusals.append({
                "episode": episode,
                "subject_commit": subject_commit,
                "run": str(run),
            })

    if (category, name) in EXACT_PROFILE_REFUSAL_CLAIMS:
        matched = [
            row for row in valid_refusals
            if row["episode"] == "S7-CONTAMINATION"
            and row["subject_commit"] == campaign.get("semantic_subject")
        ]
        if not matched:
            return [
                f"{category} {name} requires a valid S7-CONTAMINATION prelaunch refusal "
                "for the campaign semantic subject"
            ]
        return []

    if "COMPLETE_ADMISSIBLE" not in states:
        return [f"{category} {name} requires at least one COMPLETE_ADMISSIBLE exact-profile realization"]

    required_episodes = EXACT_PROFILE_REQUIRED_EPISODES.get((category, name), ())
    missing = sorted(set(required_episodes) - complete_subject_episodes)
    if missing:
        return [f"{category} {name} lacks COMPLETE_ADMISSIBLE semantic-subject episode(s): {missing}"]

    event_errors: list[str] = []
    for episode in required_episodes:
        required_kinds = EXACT_PROFILE_REQUIRED_EVENT_KINDS.get(episode, set())
        if not required_kinds:
            continue
        runs = complete_subject_runs.get(episode, [])
        observed_sets = [_normalized_event_kinds(run) for run in runs]
        if not any(required_kinds.issubset(observed) for observed in observed_sets):
            observed_union = sorted(set().union(*observed_sets)) if observed_sets else []
            event_errors.append(
                f"{episode} lacks required normalized event kinds {sorted(required_kinds)}; "
                f"observed={observed_union}"
            )
    if event_errors:
        return [f"{category} {name}: {item}" for item in event_errors]

    if (category, name) == ("check", "fresh_arm_isolation"):
        if len(pair_subject_commits) < 2:
            return ["fresh_arm_isolation requires COMPLETE_ADMISSIBLE S7-PAIR runs from at least two distinct arms"]
        summaries = list(Path(source).resolve().rglob("execution-summary.json"))
        if not summaries:
            return ["fresh_arm_isolation requires the retained exact-profile execution summary"]
        passed = False
        for summary_path in summaries:
            try:
                payload = _load_json(summary_path)
            except (CampaignError, OSError, json.JSONDecodeError):
                continue
            if (
                payload.get("status") == "PASS"
                and isinstance(payload.get("arms"), list)
                and len(set(payload["arms"])) >= 2
                and isinstance(payload.get("parallel"), int)
                and payload["parallel"] >= 2
                and not payload.get("scheduler_validation_errors")
            ):
                passed = True
                break
        if not passed:
            return ["fresh_arm_isolation lacks a PASS execution summary proving sequential arms and concurrent independent pairs"]
    return []

def init_campaign(
    profile_path: Path,
    capability_path: Path,
    *,
    candidate_head: str,
    semantic_subject: str,
    label: str | None = None,
) -> Path:
    profile_path = Path(profile_path).resolve()
    capability_path = Path(capability_path).resolve()
    if not _GIT_SHA.fullmatch(candidate_head):
        raise CampaignError("candidate_head must be a full 40-hex Git commit")
    if not _GIT_SHA.fullmatch(semantic_subject):
        raise CampaignError("semantic_subject must be a full 40-hex Git commit")
    _require_candidate_head(candidate_head)
    bundle = core70.load_profile(profile_path, capability_path)
    if bundle.profile.get("adapter_id") != omp.ADAPTER_ID:
        raise CampaignError("Stage 7 OMP campaign requires the exact OMP adapter profile")
    profile_errors = omp.profile_errors(bundle.profile)
    if profile_errors:
        raise CampaignError("OMP profile is not admissible for campaign initialization: " + "; ".join(profile_errors))
    if label is not None and not _SAFE_LABEL.fullmatch(label):
        raise CampaignError("campaign label must contain only letters, digits, dot, underscore or hyphen")

    ADMISSION_ROOT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = label or uuid.uuid4().hex[:12]
    root = ADMISSION_ROOT / f"OMP-STAGE7-{stamp}-{bundle.profile_key_sha256[:12]}-{suffix}"
    root.mkdir()
    (root / "proofs").mkdir()

    profile_snapshot = root / "profile.json"
    capability_snapshot = root / "capabilities.json"
    profile_snapshot.write_bytes(profile_path.read_bytes())
    capability_snapshot.write_bytes(capability_path.read_bytes())

    campaign = {
        "schema": SCHEMA,
        "kind": KIND,
        "state": "CANDIDATE_EVIDENCE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_head": candidate_head,
        "semantic_subject": semantic_subject,
        "profile": {
            "profile_id": bundle.profile.get("profile_id"),
            "profile_key_sha256": bundle.profile_key_sha256,
            "profile_document_sha256": core70.sha256_file(profile_snapshot),
            "capability_manifest_sha256": bundle.capability_manifest_sha256,
            "adapter_sha256": core70.sha256_file(Path(omp.__file__).resolve()),
            "core_sha256": core70.sha256_file(Path(core70.__file__).resolve()),
            "harness_sha256": core70.sha256_file(Path(harness70.__file__).resolve()),
            "admission_tool_sha256": core70.sha256_file(Path(__file__).resolve()),
            "campaign_driver_sha256": (
                core70.sha256_file(HERE / "omp_stage7_campaign.py")
                if (HERE / "omp_stage7_campaign.py").is_file() else None
            ),
            "adapter_support_sha256": _expected_adapter_support_sha256(),
            "host_execution_environment": bundle.profile.get("containment_policy", {}).get(
                "host_execution_environment"
            ),
        },
        "snapshots": {
            "profile": profile_snapshot.name,
            "capabilities": capability_snapshot.name,
        },
        "checks": {
            name: {"status": "PENDING", "attempts": []}
            for name in core70.EXECUTOR_ADMISSION_CHECKS
        },
        "section6": {
            name: {"status": "PENDING", "attempts": []}
            for name in SECTION6_CELLS
        },
    }
    _write_json(_campaign_path(root), campaign)
    return root


def _target(campaign: dict[str, Any], category: str, name: str) -> dict[str, Any]:
    if category == "check":
        if name not in core70.EXECUTOR_ADMISSION_CHECKS:
            raise CampaignError(f"unknown executor admission check {name!r}")
        return campaign["checks"][name]
    if category == "section6":
        if name not in SECTION6_CELLS:
            raise CampaignError(f"unknown section-6 matrix cell {name!r}")
        return campaign["section6"][name]
    raise CampaignError(f"unknown proof category {category!r}")


def record_proof(
    campaign_root: Path,
    *,
    category: str,
    name: str,
    evidence_path: Path,
    evidence_class: str,
    status: str,
    note: str = "",
) -> Path:
    if evidence_class not in VALID_EVIDENCE_CLASSES:
        raise CampaignError(f"unsupported evidence class {evidence_class!r}")
    allowed_classes = allowed_evidence_classes(category, name)
    if evidence_class not in allowed_classes:
        raise CampaignError(
            f"{category} {name} requires evidence class in {sorted(allowed_classes)}, got {evidence_class!r}"
        )
    if status not in VALID_STATUSES:
        raise CampaignError(f"unsupported proof status {status!r}")
    root = Path(campaign_root).resolve()
    campaign = _load_campaign(root)
    row = _target(campaign, category, name)
    evidence_path = Path(evidence_path).resolve()
    if not _within(evidence_path, root):
        raise CampaignError("proof evidence must remain inside its Stage 7 campaign realization")
    diagnostic_errors = _diagnostic_only_evidence_errors(evidence_path)
    if diagnostic_errors:
        raise CampaignError("inadmissible diagnostic evidence: " + "; ".join(diagnostic_errors))
    if evidence_class == "exact-profile-behavior":
        evidence_errors = _exact_profile_evidence_errors(evidence_path, campaign)
        evidence_errors.extend(_exact_profile_claim_errors(evidence_path, campaign, category, name))
        if evidence_errors:
            raise CampaignError("exact-profile evidence is inadmissible: " + "; ".join(evidence_errors))
    source = _source_identity(evidence_path)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    proof_name = f"{category}-{name}-{stamp}-{uuid.uuid4().hex[:8]}.json"
    proof_path = root / "proofs" / proof_name
    proof = {
        "schema": SCHEMA,
        "kind": "omp-stage7-proof-v1",
        "category": category,
        "name": name,
        "status": status,
        "evidence_class": evidence_class,
        "note": note,
        "profile_key_sha256": campaign["profile"]["profile_key_sha256"],
        "candidate_head": campaign["candidate_head"],
        **source,
    }
    _write_json(proof_path, proof)
    attempt = {
        "proof_path": proof_path.relative_to(root).as_posix(),
        "proof_sha256": core70.sha256_file(proof_path),
        "status": status,
        "evidence_class": evidence_class,
    }
    row["attempts"].append(attempt)
    row["status"] = status
    row["proof_path"] = attempt["proof_path"]
    row["proof_sha256"] = attempt["proof_sha256"]
    _write_json(_campaign_path(root), campaign)
    return proof_path


def campaign_errors(campaign_root: Path) -> list[str]:
    root = Path(campaign_root).resolve()
    campaign = _load_campaign(root)
    errors: list[str] = []
    snapshots = campaign.get("snapshots") if isinstance(campaign.get("snapshots"), dict) else {}
    profile_rel = snapshots.get("profile")
    capability_rel = snapshots.get("capabilities")
    profile_path = (root / profile_rel).resolve() if isinstance(profile_rel, str) else None
    capability_path = (root / capability_rel).resolve() if isinstance(capability_rel, str) else None
    if profile_path is None or not _within(profile_path, root) or not profile_path.is_file():
        errors.append("profile snapshot is unavailable or changed")
    if capability_path is None or not _within(capability_path, root) or not capability_path.is_file():
        errors.append("capability snapshot is unavailable or changed")
    if profile_path is not None and profile_path.is_file() and capability_path is not None and capability_path.is_file():
        try:
            bundle = core70.load_profile(profile_path, capability_path)
        except Exception as exc:
            errors.append(f"campaign profile snapshots are invalid: {exc}")
        else:
            expected_profile = campaign.get("profile") if isinstance(campaign.get("profile"), dict) else {}
            if bundle.profile_key_sha256 != expected_profile.get("profile_key_sha256"):
                errors.append("campaign profile key changed")
            if core70.sha256_file(profile_path) != expected_profile.get("profile_document_sha256"):
                errors.append("campaign profile snapshot hash changed")
            if bundle.capability_manifest_sha256 != expected_profile.get("capability_manifest_sha256"):
                errors.append("campaign capability manifest changed")
            if core70.sha256_file(Path(omp.__file__).resolve()) != expected_profile.get("adapter_sha256"):
                errors.append("campaign adapter implementation changed")
            if core70.sha256_file(Path(core70.__file__).resolve()) != expected_profile.get("core_sha256"):
                errors.append("campaign qualification core changed")
            if core70.sha256_file(Path(harness70.__file__).resolve()) != expected_profile.get("harness_sha256"):
                errors.append("campaign harness changed")
            if core70.sha256_file(Path(__file__).resolve()) != expected_profile.get("admission_tool_sha256"):
                errors.append("campaign admission tool changed")
            frozen_driver = expected_profile.get("campaign_driver_sha256")
            current_driver_path = HERE / "omp_stage7_campaign.py"
            current_driver = core70.sha256_file(current_driver_path) if current_driver_path.is_file() else None
            if current_driver != frozen_driver:
                errors.append("campaign execution driver changed")
            if _expected_adapter_support_sha256() != (expected_profile.get("adapter_support_sha256") or {}):
                errors.append("campaign adapter support files changed")
            host_errors = omp.profile_errors(bundle.profile)
            if host_errors:
                errors.append("campaign exact profile is no longer admissible on this host: " + "; ".join(host_errors))
    if set(campaign.get("checks", {})) != set(core70.EXECUTOR_ADMISSION_CHECKS):
        errors.append("campaign does not contain the exact executor admission check set")
    if set(campaign.get("section6", {})) != set(SECTION6_CELLS):
        errors.append("campaign does not contain the exact section-6 matrix")

    for category, names in (("check", core70.EXECUTOR_ADMISSION_CHECKS), ("section6", SECTION6_CELLS)):
        table = campaign["checks"] if category == "check" else campaign["section6"]
        for name in names:
            row = table.get(name)
            if not isinstance(row, dict):
                errors.append(f"{category} {name} is missing")
                continue
            if row.get("status") != "PASS":
                errors.append(f"{category} {name} is not PASS")
                continue
            rel = row.get("proof_path")
            if not isinstance(rel, str) or not rel:
                errors.append(f"{category} {name} has no proof path")
                continue
            proof_path = (root / rel).resolve()
            if not _within(proof_path, root) or not proof_path.is_file():
                errors.append(f"{category} {name} proof is unavailable")
                continue
            if core70.sha256_file(proof_path) != row.get("proof_sha256"):
                errors.append(f"{category} {name} proof hash changed")
                continue
            proof = _load_json(proof_path)
            if proof.get("category") != category or proof.get("name") != name or proof.get("status") != "PASS":
                errors.append(f"{category} {name} proof metadata does not match its campaign slot")
                continue
            if proof.get("profile_key_sha256") != campaign["profile"]["profile_key_sha256"]:
                errors.append(f"{category} {name} proof profile identity changed")
                continue
            if proof.get("candidate_head") != campaign["candidate_head"]:
                errors.append(f"{category} {name} proof candidate identity changed")
                continue
            evidence_class = proof.get("evidence_class")
            allowed_classes = allowed_evidence_classes(category, name)
            if evidence_class not in allowed_classes:
                errors.append(
                    f"{category} {name} proof class {evidence_class!r} cannot establish this admission claim"
                )
                continue
            source_path = Path(proof.get("source_path", "")).resolve()
            if not _within(source_path, root):
                errors.append(f"{category} {name} proof source escaped its Stage 7 campaign")
                continue
            diagnostic_errors = _diagnostic_only_evidence_errors(source_path)
            if diagnostic_errors:
                errors.extend(f"{category} {name}: {item}" for item in diagnostic_errors)
                continue
            if evidence_class == "exact-profile-behavior":
                exact_errors = _exact_profile_evidence_errors(source_path, campaign)
                exact_errors.extend(_exact_profile_claim_errors(source_path, campaign, category, name))
                if exact_errors:
                    errors.extend(f"{category} {name}: {item}" for item in exact_errors)
                    continue
            try:
                source = _source_identity(source_path)
            except CampaignError as exc:
                errors.append(f"{category} {name} source evidence is unavailable: {exc}")
                continue
            if source.get("source_kind") != proof.get("source_kind"):
                errors.append(f"{category} {name} source kind changed")
            if source.get("source_sha256") != proof.get("source_sha256"):
                errors.append(f"{category} {name} source evidence hash changed")
            if source.get("source_bytes") != proof.get("source_bytes"):
                errors.append(f"{category} {name} source evidence size changed")
            if source.get("source_kind") == "directory" and source.get("source_files") != proof.get("source_files"):
                errors.append(f"{category} {name} source evidence file count changed")
    return errors


def emit_candidate_bundle(campaign_root: Path) -> Path:
    root = Path(campaign_root).resolve()
    errors = campaign_errors(root)
    if errors:
        raise CampaignError("campaign is incomplete: " + "; ".join(errors))
    campaign = _load_campaign(root)
    target = root / "profile-admission-candidate.json"
    if target.exists():
        raise CampaignError(f"candidate admission bundle already exists: {target}")
    checks = {}
    for name in core70.EXECUTOR_ADMISSION_CHECKS:
        row = campaign["checks"][name]
        checks[name] = {
            "status": "PASS",
            "evidence_path": row["proof_path"],
            "evidence_sha256": row["proof_sha256"],
        }
    payload = {
        "schema": core70.SCHEMA,
        "status": "CANDIDATE",
        "role": "executor",
        "profile_key_sha256": campaign["profile"]["profile_key_sha256"],
        "adapter_sha256": campaign["profile"]["adapter_sha256"],
        "core_sha256": campaign["profile"]["core_sha256"],
        "capability_manifest_sha256": campaign["profile"]["capability_manifest_sha256"],
        "checks": checks,
        "section6": {
            name: {
                "status": campaign["section6"][name]["status"],
                "evidence_path": campaign["section6"][name]["proof_path"],
                "evidence_sha256": campaign["section6"][name]["proof_sha256"],
            }
            for name in SECTION6_CELLS
        },
        "lifecycle_note": (
            "CANDIDATE evidence only. A fresh independent Stage 7 checker must inspect/re-execute "
            "the exact-profile evidence and separately finalize an ADMITTED executor bundle."
        ),
    }
    _write_json(target, payload)
    return target


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--profile", type=Path, required=True)
    init.add_argument("--capabilities", type=Path, required=True)
    init.add_argument("--candidate-head", required=True)
    init.add_argument("--semantic-subject", required=True)
    init.add_argument("--label")

    record = sub.add_parser("record")
    record.add_argument("--campaign", type=Path, required=True)
    group = record.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", choices=core70.EXECUTOR_ADMISSION_CHECKS)
    group.add_argument("--section6", choices=SECTION6_CELLS)
    record.add_argument("--evidence", type=Path, required=True)
    record.add_argument("--evidence-class", choices=sorted(VALID_EVIDENCE_CLASSES), required=True)
    record.add_argument("--status", choices=sorted(VALID_STATUSES), required=True)
    record.add_argument("--note", default="")

    verify = sub.add_parser("verify")
    verify.add_argument("--campaign", type=Path, required=True)

    emit = sub.add_parser("emit-candidate")
    emit.add_argument("--campaign", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        root = init_campaign(
            args.profile,
            args.capabilities,
            candidate_head=args.candidate_head,
            semantic_subject=args.semantic_subject,
            label=args.label,
        )
        print(root)
        return 0
    if args.command == "record":
        category, name = ("check", args.check) if args.check else ("section6", args.section6)
        proof = record_proof(
            args.campaign,
            category=category,
            name=name,
            evidence_path=args.evidence,
            evidence_class=args.evidence_class,
            status=args.status,
            note=args.note,
        )
        print(proof)
        return 0
    if args.command == "verify":
        errors = campaign_errors(args.campaign)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 2
        print("PASS: candidate Stage 7 evidence matrix is complete and unchanged")
        return 0
    if args.command == "emit-candidate":
        print(emit_candidate_bundle(args.campaign))
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
