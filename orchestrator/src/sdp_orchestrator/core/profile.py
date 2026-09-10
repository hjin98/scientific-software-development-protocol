"""Versioned Protocol workflow profiles.

Profile metadata is control-plane data only.  Canonical prompt prose remains in
its version-bound prompt document.  Protocol 5.16 schema-v1 is preserved as a
frozen compatibility definition while Protocol 6.0 and 6.1 use independent
schema-v2 profiles selected by declared protocol/profile identity.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from . import errors as E
from .canonical import (
    CANONICAL_STAGES,
    LEGACY_PROFILE_ID,
    SSDP6_PROFILE_ID,
    SSDP61_PROFILE_ID,
    SSDP6_STAGES,
    CanonicalDocument,
    stages_for_profile,
)
from .records import (
    DigestRef,
    InputBinding,
    InputOwnership,
    ProtocolProfileRef,
    StageDescriptor,
    StageRef,
    StageTransitionDescriptor,
    WorkflowProfileDescriptor,
    WorkplanPolicy,
)

# Legacy names remain import-compatible for Core v1 consumers/tests.
PROFILE_ID = LEGACY_PROFILE_ID
PROFILE_SCHEMA_VERSION = 1
PROFILE_PROTOCOL_VERSION = "5.16.0"
COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("5.16.0", "5.16")

SSDP6_PROFILE_SCHEMA_VERSION = 2
SSDP6_PROTOCOL_VERSION = "6.0.0"
SSDP6_COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("6.0.0", "6.0")

SSDP61_PROFILE_SCHEMA_VERSION = 2
SSDP61_PROTOCOL_VERSION = "6.1.0"
SSDP61_COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("6.1.0", "6.1")
DEFAULT_PROFILE_ID = SSDP61_PROFILE_ID
RESULT_SCHEMA_ID = "sdp.stage-result-envelope"
RESULT_SCHEMA_VERSION = 1

_MECHANICAL = InputOwnership.MECHANICAL
_DEFAULT = InputOwnership.CANONICAL_DEFAULT
_USER = InputOwnership.REQUIRED_USER

# name -> (ownership, default, override_allowed, mode_dependent, first_class_source)
_INPUT_TABLE: dict[str, tuple[InputOwnership, str | None, bool, bool, str | None]] = {
    "REPOSITORY_TARGET": (_MECHANICAL, None, False, True, "observation"),
    "IMPLEMENTATION_TARGET": (_MECHANICAL, None, False, True, "observation"),
    "PROTOCOL_REF": (_MECHANICAL, None, False, False, "governing_protocol_contract"),
    "WORKPLAN": (_MECHANICAL, None, False, False, "workplan_selector"),
    "CHANGE_PLAN": (_DEFAULT, "NONE", False, False, "workplan_selector_optional_path"),
    "DOWNSTREAM_WORKPLAN": (_MECHANICAL, None, False, False, "workplan_selector"),
    "TASK": (_USER, None, False, False, "first_task"),
    "PROTOCOL_SOURCE": (_DEFAULT, "AUTO_LOCAL_FIRST", True, False, None),
    "EXECUTION_MODE": (_DEFAULT, "AUTO_EXECUTE", True, False, None),
    "ADDITIONAL_CONSTRAINTS": (_DEFAULT, "NONE", True, False, None),
    "GOVERNING_AUTHORITY": (_DEFAULT, "AUTO", True, False, None),
    "AFFECTED_DOMAIN": (_DEFAULT, "AUTO", True, False, None),
    "CURRENT_AUTHORITY": (_DEFAULT, "AUTO", True, False, None),
    "HUMAN_RATIFICATION": (_DEFAULT, "AUTO", True, False, None),
    "EXISTING_AUTHORITIES": (_DEFAULT, "AUTO", True, False, None),
    "WORKPLAN_DESTINATION": (_DEFAULT, "AUTO", True, False, None),
    "RELATED_AUTHORITIES": (_DEFAULT, "AUTO", True, False, None),
    "GOVERNING_DESIGN": (_DEFAULT, "AUTO", True, False, None),
    "SCIENTIFIC_AUTHORITIES": (_DEFAULT, "AUTO", True, False, None),
    "FROZEN_PARENT_AUTHORITY": (_DEFAULT, "AUTO", True, False, None),
    "HISTORY_WINDOW": (_DEFAULT, "AUTO", True, False, None),
    "GOVERNING_ARCHITECTURE": (_DEFAULT, "AUTO", True, False, None),
    "AFFECTED_DOCUMENTATION": (_DEFAULT, "AUTO", True, False, None),
    "EXCLUSIONS": (_DEFAULT, "NONE", True, False, None),
    "BASELINE_SCOPE": (_USER, None, True, False, None),
    "VERIFICATION_SCOPE": (_USER, None, True, False, None),
    "STABILIZATION_SCOPE": (_USER, None, True, False, None),
    "AUDIT_SCOPE": (_USER, None, True, False, None),
    "UPSTREAM_ACCEPTED_WORK": (_USER, None, True, False, None),
    "COMPLETED_WORK": (_USER, None, True, False, "workplan_selector_optional"),
}

StageRow = tuple[str, str, str, str, tuple[str, ...], WorkplanPolicy, tuple[str, ...]]
TransitionRow = tuple[str, str, str | None, str]

_LEGACY_STAGE_TABLE: dict[str, StageRow] = {
    "baseline": ("Baseline / Change-Health Intake", "software-design", "task_local_evidence", "conditional", ("captured",), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "design": ("Design / Workplan", "software-design", "design_artifacts", "required", ("pass", "no_pass"), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "implementation": ("Implementation", "software-implementation", "product", "required", ("complete", "blocked"), WorkplanPolicy.REQUIRED, ()),
    "review": ("Review & Update", "software-design", "planning_artifacts", "required", ("pass", "no_pass"), WorkplanPolicy.REQUIRED, ()),
    "verification": ("Verification", "software-design", "none", "conditional", ("pass", "no_pass"), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "stabilization": ("Stabilization / Architecture GC", "software-design", "none", "conditional", ("stable", "tier2_simplification", "frozen_concern"), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "alignment": ("Alignment of a Downstream Workplan", "software-design", "downstream_workplan", "conditional", ("pass", "no_pass"), WorkplanPolicy.EXPLICIT_REQUIRED, ()),
    "health-audit": ("Health Audit", "software-maintenance-audit", "none", "periodic", ("healthy", "watch", "action_required"), WorkplanPolicy.DISALLOWED, ("health_audit",)),
    "closeout": ("Closeout", "software-documentation,repository-hygiene", "documentation_and_lifecycle", "required", ("complete", "blocked"), WorkplanPolicy.EXPLICIT_ONLY, ()),
}

_LEGACY_TRANSITIONS: tuple[TransitionRow, ...] = (
    ("baseline", "captured", "design", "baseline evidence is carried into the following Design stage"),
    ("design", "pass", "implementation", "an accepted workplan is ready for Implementation"),
    ("design", "no_pass", "design", "a workplan that is not snapshot-complete stays in Design"),
    ("implementation", "complete", "review", "an assembled candidate is reviewed"),
    ("implementation", "blocked", "implementation", "a bounded implementation blocker stays with the owning Implementation surface"),
    ("implementation", "blocked", "design", "a blocker that invalidates the implementation contract routes the affected design surface back to Design"),
    ("review", "no_pass", "implementation", "Review blockers are repaired by Implementation"),
    ("review", "no_pass", "design", "a Review finding that invalidates the accepted contract routes to Design"),
    ("review", "pass", "verification", "Verification when scientific/architectural/high-risk claims warrant it"),
    ("review", "pass", "stabilization", "Stabilization at substantial milestone boundaries"),
    ("review", "pass", "closeout", "Closeout when no further stage is warranted"),
    ("verification", "no_pass", "implementation", "Verification blockers route to the owning Implementation path"),
    ("verification", "no_pass", "design", "Verification blockers route to the owning Design path"),
    ("verification", "pass", "stabilization", "Stabilization at substantial milestone boundaries"),
    ("verification", "pass", "closeout", "Closeout when no further stage is warranted"),
    ("stabilization", "stable", "closeout", "a stable scope is ready for Closeout"),
    ("stabilization", "tier2_simplification", "design", "Tier-2 simplification routes through a bounded workplan"),
    ("stabilization", "tier2_simplification", "implementation", "Tier-2 simplification under sufficient existing authority"),
    ("stabilization", "frozen_concern", "design", "a Frozen-architecture concern reopens only the affected Design surface"),
    ("alignment", "pass", "implementation", "a realigned downstream workplan is ready for Implementation"),
    ("alignment", "no_pass", "alignment", "an incomplete realignment stays in Alignment"),
    ("alignment", "no_pass", "design", "a realignment finding that invalidates the downstream contract routes to Design"),
    ("health-audit", "healthy", None, "no action is required"),
    ("health-audit", "watch", None, "findings are retained as watch items"),
    ("health-audit", "action_required", "design", "substantial maintenance needs an accepted contract first"),
    ("health-audit", "action_required", "implementation", "local Tier-2 repair under already-sufficient authority"),
    ("closeout", "complete", None, "the lifecycle scope is closed"),
    ("closeout", "blocked", "implementation", "a closeout blocker owned by the accepted implementation routes to Implementation"),
    ("closeout", "blocked", "design", "a closeout blocker that reopens the contract routes to Design"),
)

_SSDP6_STAGE_TABLE: dict[str, StageRow] = {
    "intake": ("Authority / Affected-Domain Intake", "scientific-formulation,numerical-algorithm-design,software-design,software-implementation", "routing_evidence", "conditional", ("classified",), WorkplanPolicy.EXPLICIT_ONLY, ("domain-intake",)),
    "scientific-formulation": ("D1 Scientific & Mathematical Formulation", "scientific-formulation", "d1_authority", "conditional", ("accepted", "no_pass", "serious_challenge", "human_pending", "risk_override"), WorkplanPolicy.EXPLICIT_ONLY, ("d1", "science")),
    "numerical-algorithm-design": ("D2 Algorithm & Numerical Method Design", "numerical-algorithm-design", "d2_authority", "conditional", ("accepted", "no_pass", "serious_challenge", "human_pending", "risk_override"), WorkplanPolicy.EXPLICIT_ONLY, ("d2", "numerics")),
    "software-design": ("D3 Software Architecture / Workplan", "software-design", "d3_authority_and_workplan", "conditional", ("accepted", "no_pass", "serious_challenge"), WorkplanPolicy.EXPLICIT_ONLY, ("d3", "design")),
    "software-implementation": ("D4 Software Implementation", "software-implementation", "d4_product", "conditional", ("complete", "blocked", "serious_challenge"), WorkplanPolicy.EXPLICIT_ONLY, ("d4", "implementation")),
    "review": ("Review & Challenge Pass", "domain-parent-owner", "planning_and_authority_state", "required", ("pass", "no_pass", "serious_challenge", "human_pending", "risk_override"), WorkplanPolicy.REQUIRED, ()),
    "verification": ("Verification", "domain-parent-owner", "none", "conditional", ("pass", "no_pass", "serious_challenge", "human_pending", "risk_override"), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "stabilization": ("Stabilization / Architecture GC", "software-design", "none", "conditional", ("stable", "d4_simplification", "d3_concern", "upstream_concern", "serious_challenge"), WorkplanPolicy.EXPLICIT_ONLY, ()),
    "alignment": ("Downstream Authority Alignment", "domain-owner", "downstream_authority_or_plan", "conditional", ("pass", "no_pass", "serious_challenge"), WorkplanPolicy.EXPLICIT_REQUIRED, ()),
    "health-audit": ("Health Audit", "software-maintenance-audit", "none", "periodic", ("healthy", "watch", "action_required", "serious_challenge"), WorkplanPolicy.DISALLOWED, ("health_audit",)),
    "closeout": ("Closeout", "software-documentation,repository-hygiene", "documentation_and_lifecycle", "required", ("complete", "blocked", "serious_challenge"), WorkplanPolicy.EXPLICIT_ONLY, ()),
}

_SSDP6_TRANSITIONS: tuple[TransitionRow, ...] = (
    ("intake", "classified", "scientific-formulation", "route when D1 is the highest potentially affected domain"),
    ("intake", "classified", "numerical-algorithm-design", "route when D2 is the highest potentially affected domain"),
    ("intake", "classified", "software-design", "route when D3 is the highest potentially affected domain"),
    ("intake", "classified", "software-implementation", "route when only D4 realization is affected"),
    ("scientific-formulation", "accepted", "numerical-algorithm-design", "realize accepted D1 changes downward when D2 is affected"),
    ("scientific-formulation", "accepted", "software-design", "realize accepted D1 changes through affected architecture when D2 authority remains unchanged"),
    ("scientific-formulation", "accepted", "software-implementation", "realize accepted D1 changes directly in D4 when D2 and D3 authority remain unchanged"),
    ("scientific-formulation", "accepted", "review", "review a D1-only authority change when no lower realization is affected"),
    ("scientific-formulation", "accepted", "closeout", "close an accepted D1-only scope when no further realization/review is required"),
    ("scientific-formulation", "no_pass", "scientific-formulation", "unaccepted D1 work remains with its owner"),
    ("scientific-formulation", "serious_challenge", None, "human adjudication is required before dependent routing"),
    ("scientific-formulation", "human_pending", None, "required human ratification is pending"),
    ("scientific-formulation", "risk_override", "numerical-algorithm-design", "bounded downstream work may proceed under visible unresolved risk where policy permits"),
    ("scientific-formulation", "risk_override", "software-design", "bounded D3 work may proceed under visible unresolved D1 risk when D2 authority is unaffected"),
    ("scientific-formulation", "risk_override", "software-implementation", "bounded D4 work may proceed under visible unresolved D1 risk when D2 and D3 authority are unaffected"),
    ("numerical-algorithm-design", "accepted", "software-design", "realize accepted D2 changes through affected architecture"),
    ("numerical-algorithm-design", "accepted", "software-implementation", "realize accepted D2 changes directly in D4 when D3 authority remains unchanged"),
    ("numerical-algorithm-design", "accepted", "review", "review a D2-only authority change when no architecture realization is affected"),
    ("numerical-algorithm-design", "accepted", "closeout", "close an accepted D2-only scope when no lower realization is required"),
    ("numerical-algorithm-design", "no_pass", "numerical-algorithm-design", "unaccepted D2 work remains with its owner"),
    ("numerical-algorithm-design", "serious_challenge", None, "human adjudication is required before dependent routing"),
    ("numerical-algorithm-design", "human_pending", None, "required human ratification is pending"),
    ("numerical-algorithm-design", "risk_override", "software-design", "bounded downstream work may proceed under visible unresolved risk where policy permits"),
    ("numerical-algorithm-design", "risk_override", "software-implementation", "bounded D4 work may proceed under visible unresolved D2 risk when D3 authority is unaffected"),
    ("software-design", "accepted", "software-implementation", "an accepted D3->D4 workplan is ready for implementation"),
    ("software-design", "accepted", "review", "review an accepted D3-only authority change when no D4 realization is affected"),
    ("software-design", "accepted", "closeout", "close an accepted D3-only scope when existing D4 already conforms and no further review is required"),
    ("software-design", "no_pass", "software-design", "incomplete D3 authority/workplan stays with Software Design"),
    ("software-design", "serious_challenge", None, "human adjudication is required before dependent routing"),
    ("software-implementation", "complete", "review", "an assembled D4 candidate is reviewed"),
    ("software-implementation", "blocked", "software-implementation", "a D4-local blocker remains with implementation"),
    ("software-implementation", "blocked", "software-design", "a blocker invalidating D3 routes to Software Design"),
    ("software-implementation", "blocked", "numerical-algorithm-design", "a blocker invalidating D2 routes to Numerical Algorithm Design"),
    ("software-implementation", "blocked", "scientific-formulation", "a blocker invalidating D1 routes to Scientific Formulation"),
    ("software-implementation", "serious_challenge", None, "dependent closure stops for human adjudication"),
    ("review", "pass", "numerical-algorithm-design", "a passed D1-boundary review may continue into dependent D2 realization"),
    ("review", "pass", "software-design", "a passed D1/D2-boundary review may continue into dependent D3 realization"),
    ("review", "pass", "software-implementation", "a passed D1/D2/D3-boundary review may continue into dependent D4 realization"),
    ("review", "pass", "verification", "deeper verification is optional for materially high-risk claims"),
    ("review", "pass", "stabilization", "stabilization is optional at material convergence boundaries"),
    ("review", "pass", "closeout", "closeout follows when no further stage is warranted"),
    ("review", "no_pass", "software-implementation", "D4 nonconformance returns to implementation"),
    ("review", "no_pass", "software-design", "D3 deficiency reopens Software Design"),
    ("review", "no_pass", "numerical-algorithm-design", "D2 deficiency reopens Numerical Algorithm Design"),
    ("review", "no_pass", "scientific-formulation", "D1 deficiency reopens Scientific Formulation"),
    ("review", "serious_challenge", None, "human adjudication is required before normal Pass"),
    ("review", "human_pending", None, "required human adjudication/ratification is pending"),
    ("review", "risk_override", "numerical-algorithm-design", "bounded D2 realization may proceed under visible accepted risk where policy permits"),
    ("review", "risk_override", "software-design", "bounded D3 realization may proceed under visible accepted risk where policy permits"),
    ("review", "risk_override", "software-implementation", "bounded D4 realization may proceed under visible accepted risk where policy permits"),
    ("review", "risk_override", "verification", "bounded verification may proceed under visible accepted risk where policy permits"),
    ("review", "risk_override", "closeout", "non-protocol product closeout may proceed only under policy-permitted visible risk"),
    ("verification", "pass", "stabilization", "stabilization may follow a verified material milestone"),
    ("verification", "pass", "closeout", "verified work may close when no stabilization is warranted"),
    ("verification", "no_pass", "software-implementation", "D4 verification failure routes to implementation"),
    ("verification", "no_pass", "software-design", "D3 verification failure routes to Software Design"),
    ("verification", "no_pass", "numerical-algorithm-design", "D2 verification failure routes to Numerical Algorithm Design"),
    ("verification", "no_pass", "scientific-formulation", "D1 verification failure routes to Scientific Formulation"),
    ("verification", "serious_challenge", None, "human adjudication is required before dependent closure"),
    ("verification", "human_pending", None, "required human adjudication is pending"),
    ("verification", "risk_override", "closeout", "bounded product closeout may proceed under visible accepted risk where policy permits"),
    ("stabilization", "stable", "closeout", "a stable scope is ready for closeout"),
    ("stabilization", "d4_simplification", "software-implementation", "D4 simplification under sufficient D3 authority"),
    ("stabilization", "d3_concern", "software-design", "architecture concern reopens D3"),
    ("stabilization", "upstream_concern", "numerical-algorithm-design", "numerical concern routes to D2"),
    ("stabilization", "upstream_concern", "scientific-formulation", "scientific concern routes to D1"),
    ("stabilization", "serious_challenge", None, "authority challenge requires adjudication"),
    ("alignment", "pass", "numerical-algorithm-design", "an aligned downstream D2 plan is ready for numerical-method realization"),
    ("alignment", "pass", "software-design", "an aligned downstream D3 plan is ready for architecture/workplan realization"),
    ("alignment", "pass", "software-implementation", "an aligned downstream D3->D4 plan is ready for implementation"),
    ("alignment", "no_pass", "alignment", "incomplete alignment stays in the alignment stage"),
    ("alignment", "serious_challenge", None, "authority conflict requires adjudication"),
    ("health-audit", "healthy", None, "no action is required"),
    ("health-audit", "watch", None, "findings remain watch items"),
    ("health-audit", "action_required", "software-implementation", "local D4 repair under sufficient authority"),
    ("health-audit", "action_required", "software-design", "D3 maintenance concern requires architecture/workplan action"),
    ("health-audit", "action_required", "numerical-algorithm-design", "D2 maintenance concern routes to numerical authority"),
    ("health-audit", "action_required", "scientific-formulation", "D1 maintenance concern routes to scientific authority"),
    ("health-audit", "serious_challenge", None, "material authority contradiction requires adjudication"),
    ("closeout", "complete", None, "the lifecycle scope is closed"),
    ("closeout", "blocked", "software-implementation", "D4 closeout blocker returns to implementation"),
    ("closeout", "blocked", "software-design", "D3 closeout blocker reopens Software Design"),
    ("closeout", "blocked", "numerical-algorithm-design", "D2 closeout blocker reopens Numerical Algorithm Design"),
    ("closeout", "blocked", "scientific-formulation", "D1 closeout blocker reopens Scientific Formulation"),
    ("closeout", "serious_challenge", None, "Protocol 6 release cannot close under unresolved governing challenge"),
)


def _protocol61_term(text: str) -> str:
    return text.replace("realization", "concretization").replace("realize", "concretize")


_SSDP61_STAGE_TABLE: dict[str, StageRow] = dict(_SSDP6_STAGE_TABLE)
_SSDP61_TRANSITIONS: tuple[TransitionRow, ...] = tuple(
    (source, trigger, target, _protocol61_term(explanation))
    for source, trigger, target, explanation in _SSDP6_TRANSITIONS
)


@dataclass(frozen=True)
class ProfileDefinition:
    profile_id: str
    schema_version: int
    protocol_version: str
    compatible_versions: tuple[str, ...]
    stage_table: dict[str, StageRow]
    transitions: tuple[TransitionRow, ...]


_DEFINITIONS = {
    LEGACY_PROFILE_ID: ProfileDefinition(LEGACY_PROFILE_ID, 1, PROFILE_PROTOCOL_VERSION, COMPATIBLE_PROTOCOL_VERSIONS, _LEGACY_STAGE_TABLE, _LEGACY_TRANSITIONS),
    SSDP6_PROFILE_ID: ProfileDefinition(SSDP6_PROFILE_ID, SSDP6_PROFILE_SCHEMA_VERSION, SSDP6_PROTOCOL_VERSION, SSDP6_COMPATIBLE_PROTOCOL_VERSIONS, _SSDP6_STAGE_TABLE, _SSDP6_TRANSITIONS),
    SSDP61_PROFILE_ID: ProfileDefinition(SSDP61_PROFILE_ID, SSDP61_PROFILE_SCHEMA_VERSION, SSDP61_PROTOCOL_VERSION, SSDP61_COMPATIBLE_PROTOCOL_VERSIONS, _SSDP61_STAGE_TABLE, _SSDP61_TRANSITIONS),
}


@dataclass(frozen=True)
class ProfileSnapshot:
    descriptor: WorkflowProfileDescriptor
    bodies: dict[str, str]


def definition(profile_id: str) -> ProfileDefinition:
    try:
        return _DEFINITIONS[profile_id]
    except KeyError:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "no compatible workflow profile is available",
            details={"requested": profile_id, "available": sorted(_DEFINITIONS)},
        )


def available_profile_ids() -> tuple[str, ...]:
    return tuple(_DEFINITIONS)


def profile_id_for_version(protocol_version: str) -> str:
    matches = [item.profile_id for item in _DEFINITIONS.values() if protocol_version in item.compatible_versions]
    if len(matches) != 1:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "the declared protocol version does not map to exactly one supported profile",
            details={"declared": protocol_version, "supported": sorted(v for d in _DEFINITIONS.values() for v in d.compatible_versions)},
        )
    return matches[0]


def compatible_versions(profile_id: str) -> tuple[str, ...]:
    return definition(profile_id).compatible_versions


def _stage_ref(defn: ProfileDefinition, stage_key: str) -> StageRef:
    return StageRef(profile_id=defn.profile_id, protocol_version=defn.protocol_version, stage_key=stage_key)


def _binding(name: str) -> InputBinding:
    try:
        ownership, default, override, mode_dependent, source = _INPUT_TABLE[name]
    except KeyError:
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the canonical source declares an INPUT with no profile classification",
            details={"input": name},
            remediation="the profile must classify every canonical INPUT before it can be rendered",
        )
    return InputBinding(
        name=name,
        ownership=ownership,
        default_value=default,
        override_allowed=override,
        mode_dependent=mode_dependent,
        first_class_source=source,
    )


def profile_ref(profile_id: str, source_digest: DigestRef | None) -> ProtocolProfileRef:
    defn = definition(profile_id)
    return ProtocolProfileRef(
        profile_id=defn.profile_id,
        profile_schema_version=defn.schema_version,
        protocol_version=defn.protocol_version,
        compatible_protocol_versions=defn.compatible_versions,
        source_digest=source_digest,
    )


def build_profile(document: CanonicalDocument, profile_id: str | None = None) -> ProfileSnapshot:
    selected = profile_id or document.profile_id
    defn = definition(selected)
    if document.profile_id != selected:
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the parsed canonical document is bound to a different profile",
            details={"document": document.profile_id, "requested": selected},
        )
    canonical_spec = stages_for_profile(selected)
    canonical_keys = [key for _, key, _ in canonical_spec]
    if sorted(canonical_keys) != sorted(defn.stage_table) or set(document.stages) != set(canonical_keys):
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the profile stage set does not match the canonical stage set",
            details={"canonical": sorted(canonical_keys), "document": sorted(document.stages), "profile": sorted(defn.stage_table)},
        )

    stages: list[StageDescriptor] = []
    bodies: dict[str, str] = {}
    for stage_key in canonical_keys:
        canonical = document.stages[stage_key]
        title, role, mutation, optionality, outcomes, policy, aliases = defn.stage_table[stage_key]
        if canonical.title != title:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "a canonical stage title does not match the compatible profile",
                details={"stage": stage_key, "canonical": canonical.title, "profile": title},
            )
        stages.append(
            StageDescriptor(
                stage=_stage_ref(defn, stage_key),
                aliases=aliases,
                title=title,
                role_owner=role,
                mutation_class=mutation,
                optionality=optionality,
                recognized_outcomes=outcomes,
                workplan_policy=policy,
                inputs=tuple(_binding(name) for name in canonical.input_names),
            )
        )
        bodies[stage_key] = canonical.body

    known_stages = set(canonical_keys)
    transitions: list[StageTransitionDescriptor] = []
    for source, trigger, target, explanation in defn.transitions:
        if source not in known_stages or (target is not None and target not in known_stages):
            E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "a profile transition references an unknown stage", details={"from": source, "to": target})
        if trigger not in defn.stage_table[source][4]:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "a profile transition uses an unrecognized outcome",
                details={"from": source, "trigger": trigger, "recognized": list(defn.stage_table[source][4])},
            )
        transitions.append(
            StageTransitionDescriptor(
                from_stage=_stage_ref(defn, source),
                trigger_key=trigger,
                to_stage=_stage_ref(defn, target) if target else None,
                terminal=target is None,
                priority_hint=None,
                explanation=explanation,
            )
        )

    return ProfileSnapshot(
        descriptor=WorkflowProfileDescriptor(
            profile=profile_ref(selected, document.content_digest),
            schema_version=defn.schema_version,
            stages=tuple(stages),
            transitions=tuple(transitions),
            result_schema_id=RESULT_SCHEMA_ID,
            result_schema_version=RESULT_SCHEMA_VERSION,
        ),
        bodies=bodies,
    )


def resolve_stage_key(descriptor: WorkflowProfileDescriptor, selector: str) -> StageRef:
    normalized = selector.strip().lower()
    for stage in descriptor.stages:
        if normalized == stage.stage.stage_key or normalized in stage.aliases:
            return stage.stage
    E.fail(
        E.STAGE_UNKNOWN,
        f"stage {selector!r} is not defined by the compatible profile",
        details={"profile": descriptor.profile.profile_id, "available": [stage.stage.stage_key for stage in descriptor.stages]},
    )


def stage_descriptor(descriptor: WorkflowProfileDescriptor, stage: StageRef) -> StageDescriptor:
    for candidate in descriptor.stages:
        if candidate.stage == stage:
            return candidate
    E.fail(E.STAGE_UNKNOWN, f"stage {stage.stage_key!r} is not defined by the compatible profile", details={"profile": descriptor.profile.profile_id})


def profile_to_json(descriptor: WorkflowProfileDescriptor) -> str:
    payload: dict[str, Any] = descriptor.model_dump(mode="json")
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def profile_from_json(text: str) -> WorkflowProfileDescriptor:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        E.fail(E.PROTOCOL_UNAVAILABLE, f"the packaged workflow profile is not valid JSON: {exc}")
    try:
        descriptor = WorkflowProfileDescriptor(**payload)
    except Exception as exc:  # noqa: BLE001 - schema mismatch is a data problem
        E.fail(E.PROTOCOL_INCOMPATIBLE, f"the packaged workflow profile does not match the supported record schema: {exc}")
    defn = definition(descriptor.profile.profile_id)
    if descriptor.profile.profile_schema_version != defn.schema_version or descriptor.schema_version != defn.schema_version:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "the packaged workflow profile uses an unsupported profile schema version",
            details={"profile": defn.profile_id, "declared": descriptor.schema_version, "supported": defn.schema_version},
        )
    return descriptor
