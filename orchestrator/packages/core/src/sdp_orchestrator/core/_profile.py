"""The compatible Protocol 5.16 workflow profile.

The profile is *control metadata only*: stage identity, ownership, mutation
class, workplan policy, input classification, recognized outcomes, and
authority-backed routing relations. It deliberately contains no prompt prose --
prose has exactly one authority, the canonical document parsed by
:mod:`._canonical` -- and it is not a general workflow DSL.

Routing is conservative by construction. Where Protocol 5.16 leaves the next
stage optional or context-dependent, this profile emits *several* transitions
under one trigger key so a consumer must treat the relation as ambiguous. It
never invents a deterministic edge the authority does not state.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from . import _errors as E
from ._canonical import CANONICAL_STAGES, CanonicalDocument
from ._records import (
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

PROFILE_ID = "sdp-protocol-5.16"
PROFILE_SCHEMA_VERSION = 1
PROFILE_PROTOCOL_VERSION = "5.16.0"
COMPATIBLE_PROTOCOL_VERSIONS: tuple[str, ...] = ("5.16.0", "5.16")
RESULT_SCHEMA_ID = "sdp.stage-result-envelope"
RESULT_SCHEMA_VERSION = 1

_MECHANICAL = InputOwnership.MECHANICAL
_DEFAULT = InputOwnership.CANONICAL_DEFAULT
_USER = InputOwnership.REQUIRED_USER

#: name -> (ownership, default_value, override_allowed, mode_dependent, first_class_source)
_INPUT_TABLE: dict[str, tuple[InputOwnership, str | None, bool, bool, str | None]] = {
    # Mechanical, mode-dependent repository context produced during final render.
    "REPOSITORY_TARGET": (_MECHANICAL, None, False, True, "observation"),
    "IMPLEMENTATION_TARGET": (_MECHANICAL, None, False, True, "observation"),
    # Mechanical governing-contract bindings.
    "PROTOCOL_REF": (_MECHANICAL, None, False, False, "governing_protocol_contract"),
    "WORKPLAN": (_MECHANICAL, None, False, False, "workplan_selector"),
    "DOWNSTREAM_WORKPLAN": (_MECHANICAL, None, False, False, "workplan_selector"),
    # First-class user input with its own CLI/API binding.
    "TASK": (_USER, None, False, False, "first_task"),
    # Canonical defaults, overridable through a declared input.
    "PROTOCOL_SOURCE": (_DEFAULT, "AUTO_LOCAL_FIRST", True, False, None),
    "EXECUTION_MODE": (_DEFAULT, "AUTO_EXECUTE", True, False, None),
    "ADDITIONAL_CONSTRAINTS": (_DEFAULT, "NONE", True, False, None),
    "GOVERNING_AUTHORITY": (_DEFAULT, "AUTO", True, False, None),
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
    # Required user decisions bound through --input.
    "BASELINE_SCOPE": (_USER, None, True, False, None),
    "VERIFICATION_SCOPE": (_USER, None, True, False, None),
    "STABILIZATION_SCOPE": (_USER, None, True, False, None),
    "AUDIT_SCOPE": (_USER, None, True, False, None),
    "UPSTREAM_ACCEPTED_WORK": (_USER, None, True, False, None),
    #: Satisfiable either by --input or by an exact selected completed workplan.
    "COMPLETED_WORK": (_USER, None, True, False, "workplan_selector_optional"),
}

#: stage_key -> (title, role_owner, mutation_class, optionality, outcomes, workplan policy, aliases)
_STAGE_TABLE: dict[str, tuple[str, str, str, str, tuple[str, ...], WorkplanPolicy, tuple[str, ...]]] = {
    "baseline": (
        "Baseline / Change-Health Intake",
        "software-design",
        "task_local_evidence",
        "conditional",
        ("captured",),
        WorkplanPolicy.EXPLICIT_ONLY,
        (),
    ),
    "design": (
        "Design / Workplan",
        "software-design",
        "design_artifacts",
        "required",
        ("pass", "no_pass"),
        WorkplanPolicy.EXPLICIT_ONLY,
        (),
    ),
    "implementation": (
        "Implementation",
        "software-implementation",
        "product",
        "required",
        ("complete", "blocked"),
        WorkplanPolicy.REQUIRED,
        (),
    ),
    "review": (
        "Review & Update",
        "software-design",
        "planning_artifacts",
        "required",
        ("pass", "no_pass"),
        WorkplanPolicy.REQUIRED,
        (),
    ),
    "verification": (
        "Verification",
        "software-design",
        "none",
        "conditional",
        ("pass", "no_pass"),
        WorkplanPolicy.EXPLICIT_ONLY,
        (),
    ),
    "stabilization": (
        "Stabilization / Architecture GC",
        "software-design",
        "none",
        "conditional",
        ("stable", "tier2_simplification", "frozen_concern"),
        WorkplanPolicy.EXPLICIT_ONLY,
        (),
    ),
    "alignment": (
        "Alignment of a Downstream Workplan",
        "software-design",
        "downstream_workplan",
        "conditional",
        ("pass", "no_pass"),
        WorkplanPolicy.EXPLICIT_REQUIRED,
        (),
    ),
    "health-audit": (
        "Health Audit",
        "software-maintenance-audit",
        "none",
        "periodic",
        ("healthy", "watch", "action_required"),
        WorkplanPolicy.DISALLOWED,
        ("health_audit",),
    ),
    "closeout": (
        "Closeout",
        "software-documentation,repository-hygiene",
        "documentation_and_lifecycle",
        "required",
        ("complete", "blocked"),
        WorkplanPolicy.EXPLICIT_ONLY,
        (),
    ),
}

#: (from, trigger, to | None, explanation). Several rows sharing a (from, trigger)
#: pair state a genuinely optional relation and must be read as ambiguous.
_TRANSITIONS: tuple[tuple[str, str, str | None, str], ...] = (
    ("baseline", "captured", "design", "baseline evidence is carried into the following Design stage"),
    ("design", "pass", "implementation", "an accepted workplan is ready for Implementation"),
    ("design", "no_pass", "design", "a workplan that is not snapshot-complete stays in Design"),
    ("implementation", "complete", "review", "an assembled candidate is reviewed"),
    ("implementation", "blocked", "design", "a blocked implementation routes the affected design surface back to Design"),
    ("review", "no_pass", "implementation", "Review blockers are repaired by Implementation"),
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
    ("health-audit", "healthy", None, "no action is required"),
    ("health-audit", "watch", None, "findings are retained as watch items"),
    ("health-audit", "action_required", "design", "substantial maintenance needs an accepted contract first"),
    ("health-audit", "action_required", "implementation", "local Tier-2 repair under already-sufficient authority"),
    ("closeout", "complete", None, "the lifecycle scope is closed"),
    ("closeout", "blocked", "implementation", "a semantic defect routes back to the owning Implementation stage"),
)


@dataclass(frozen=True)
class ProfileSnapshot:
    """A compatible profile plus the canonical prompt bodies it interprets."""

    descriptor: WorkflowProfileDescriptor
    bodies: dict[str, str]


def _stage_ref(stage_key: str) -> StageRef:
    return StageRef(
        profile_id=PROFILE_ID,
        protocol_version=PROFILE_PROTOCOL_VERSION,
        stage_key=stage_key,
    )


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


def profile_ref(source_digest: DigestRef | None) -> ProtocolProfileRef:
    return ProtocolProfileRef(
        profile_id=PROFILE_ID,
        profile_schema_version=PROFILE_SCHEMA_VERSION,
        protocol_version=PROFILE_PROTOCOL_VERSION,
        compatible_protocol_versions=COMPATIBLE_PROTOCOL_VERSIONS,
        source_digest=source_digest,
    )


def build_profile(document: CanonicalDocument) -> ProfileSnapshot:
    """Derive the profile descriptor from authored control metadata + canonical source.

    Reconciliation is bidirectional: every canonical INPUT must be classified, and
    the stage set must match the canonical stage set exactly. Source drift becomes
    a loud failure instead of a silently partial prompt.
    """

    canonical_keys = [key for _, key, _ in CANONICAL_STAGES]
    if sorted(canonical_keys) != sorted(_STAGE_TABLE):
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the profile stage set does not match the canonical stage set",
            details={"canonical": sorted(canonical_keys), "profile": sorted(_STAGE_TABLE)},
        )

    stages: list[StageDescriptor] = []
    bodies: dict[str, str] = {}
    for stage_key in canonical_keys:
        canonical = document.stages[stage_key]
        title, role, mutation, optionality, outcomes, policy, aliases = _STAGE_TABLE[stage_key]
        if canonical.title != title:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "a canonical stage title does not match the compatible profile",
                details={"stage": stage_key, "canonical": canonical.title, "profile": title},
            )
        stages.append(
            StageDescriptor(
                stage=_stage_ref(stage_key),
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
    for source, trigger, target, explanation in _TRANSITIONS:
        if source not in known_stages or (target is not None and target not in known_stages):
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "a profile transition references an unknown stage",
                details={"from": source, "to": target},
            )
        stage_outcomes = _STAGE_TABLE[source][4]
        if trigger not in stage_outcomes:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "a profile transition uses a trigger that is not a recognized outcome",
                details={"from": source, "trigger": trigger, "recognized": list(stage_outcomes)},
            )
        transitions.append(
            StageTransitionDescriptor(
                from_stage=_stage_ref(source),
                trigger_key=trigger,
                to_stage=_stage_ref(target) if target else None,
                terminal=target is None,
                priority_hint=None,
                explanation=explanation,
            )
        )

    descriptor = WorkflowProfileDescriptor(
        profile=profile_ref(document.content_digest),
        schema_version=PROFILE_SCHEMA_VERSION,
        stages=tuple(stages),
        transitions=tuple(transitions),
        result_schema_id=RESULT_SCHEMA_ID,
        result_schema_version=RESULT_SCHEMA_VERSION,
    )
    return ProfileSnapshot(descriptor=descriptor, bodies=bodies)


def resolve_stage_key(descriptor: WorkflowProfileDescriptor, selector: str) -> StageRef:
    """Resolve a profile-neutral selector to a profile-bound :class:`StageRef`."""

    normalized = selector.strip().lower()
    for stage in descriptor.stages:
        if normalized == stage.stage.stage_key or normalized in stage.aliases:
            return stage.stage
    E.fail(
        E.STAGE_UNKNOWN,
        f"stage {selector!r} is not defined by the compatible profile",
        details={
            "profile": descriptor.profile.profile_id,
            "available": [stage.stage.stage_key for stage in descriptor.stages],
        },
    )


def stage_descriptor(
    descriptor: WorkflowProfileDescriptor, stage: StageRef
) -> StageDescriptor:
    for candidate in descriptor.stages:
        if candidate.stage == stage:
            return candidate
    E.fail(
        E.STAGE_UNKNOWN,
        f"stage {stage.stage_key!r} is not defined by the compatible profile",
        details={"profile": descriptor.profile.profile_id},
    )


# --------------------------------------------------------------------------
# Serialization of the packaged snapshot
# --------------------------------------------------------------------------


def profile_to_json(descriptor: WorkflowProfileDescriptor) -> str:
    """Serialize the descriptor as the packaged, reproducible profile document."""

    payload: dict[str, Any] = descriptor.model_dump(mode="json")
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def profile_from_json(text: str) -> WorkflowProfileDescriptor:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        E.fail(E.PROTOCOL_UNAVAILABLE, f"the packaged workflow profile is not valid JSON: {exc}")
    try:
        return WorkflowProfileDescriptor(**payload)
    except Exception as exc:  # noqa: BLE001 - schema mismatch is a data problem
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            f"the packaged workflow profile does not match the supported schema: {exc}",
        )
