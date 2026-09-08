"""Public v1 records.

Everything reachable from ``api.v1``/``spi.v1`` is defined here or is a standard
immutable scalar/container. Records are frozen, JSON-compatible, and never carry
a live Git handle, subprocess, file object, or other implementation object.

Pydantic is the initial technology, not the semantic authority: the field names
and their meanings are the contract.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, NewType, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# --------------------------------------------------------------------------
# Opaque identities
# --------------------------------------------------------------------------

ProjectKey = NewType("ProjectKey", str)
WorktreeKey = NewType("WorktreeKey", str)
RunId = NewType("RunId", str)
EventId = NewType("EventId", str)
StageSelector = NewType("StageSelector", str)
CapabilityKey = NewType("CapabilityKey", str)
ExtensionId = NewType("ExtensionId", str)


class _Record(BaseModel):
    """Base for every public record: frozen, closed, JSON-compatible."""

    model_config = ConfigDict(frozen=True, extra="forbid")


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """A bounded slice of an unbounded collection.

    ``next_cursor`` is opaque and scoped to the originating query; callers must
    not construct or reinterpret it.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    items: tuple[T, ...] = ()
    next_cursor: str | None = None
    total_known: int | None = None


# --------------------------------------------------------------------------
# Enumerations
# --------------------------------------------------------------------------


class PromptExecutionMode(str, Enum):
    """Where/how the rendered prompt will be consumed.

    Deliberately distinct from the canonical SDP prompt INPUT ``EXECUTION_MODE``
    (``AUTO_EXECUTE``/``REPORT_ONLY``), which governs what the receiving agent
    may do. Changing one never changes the other.
    """

    LOCAL = "local"
    WEB = "web"


class RemoteMode(str, Enum):
    LOCAL_ONLY = "local_only"
    USE_CACHED_REMOTE = "use_cached_remote"
    REFRESH_REMOTE = "refresh_remote"


class ActivationPolicy(str, Enum):
    NORMAL = "normal"
    DISCOVERY_ONLY = "discovery_only"


class InputOwnership(str, Enum):
    MECHANICAL = "mechanical"
    CANONICAL_DEFAULT = "canonical_default"
    REQUIRED_USER = "required_user"


class WorkplanPolicy(str, Enum):
    REQUIRED = "required"
    EXPLICIT_ONLY = "explicit_only"
    EXPLICIT_REQUIRED = "explicit_required"
    DISALLOWED = "disallowed"


class LifecycleState(str, Enum):
    ACTIVE = "active"
    ARCHIVE = "archive"


class Multiplicity(str, Enum):
    SINGULAR = "singular"
    MANY = "many"


class RemoteEvidence(str, Enum):
    """Provenance of whatever is known about the remote side."""

    NONE = "none"
    CACHED = "cached"
    REFRESHED = "refreshed"


# --------------------------------------------------------------------------
# Identity records
# --------------------------------------------------------------------------


class DigestRef(_Record):
    algorithm: str
    canonicalization_scheme: str | None = None
    value: str

    def as_text(self) -> str:
        return f"{self.algorithm}:{self.value}"


class StageRef(_Record):
    """Resolved, profile-bound stage identity.

    Never fabricated from user input alone: it exists only after a compatible
    protocol profile has been resolved, so a stage key always means what the
    governing profile says it means.
    """

    profile_id: str
    protocol_version: str
    stage_key: str


class ProtocolProfileRef(_Record):
    profile_id: str
    profile_schema_version: int
    protocol_version: str
    compatible_protocol_versions: tuple[str, ...]
    source_digest: DigestRef | None = None


class PromptSourceRef(_Record):
    """Where Core read canonical prompt/profile material.

    This is Core provenance and is *not* the agent-facing ``PROTOCOL_SOURCE``
    input. A local render source therefore never becomes prompt content.
    """

    kind: str  # packaged | local | remote
    identity: str
    sanitized_location: str | None = None
    requested_ref: str | None = None
    resolved_ref: str | None = None
    content_digests: tuple[tuple[str, DigestRef], ...] = ()


class RemoteRepositoryRef(_Record):
    remote_name: str
    sanitized_repository: str
    scheme: str
    web_addressable: bool


class WorkplanRef(_Record):
    workplan_id: str
    protocol_version: str | None
    path: str
    artifact_digest: DigestRef
    semantic_digest: DigestRef | None = None
    semantic_identity_complete: bool = False
    lifecycle_state: LifecycleState = LifecycleState.ACTIVE
    lifecycle_consistent: bool = True
    declared_status: str | None = None


class CandidateRef(_Record):
    repository_id: str
    branch: str | None
    detached: bool
    head_commit: str | None
    working_tree_digest: DigestRef | None = None
    identity_complete: bool = True
    upstream_ref: str | None = None
    observed_remote_commit: str | None = None
    remote_evidence: RemoteEvidence = RemoteEvidence.NONE
    remote_observed_at: str | None = None
    observed_at: str | None = None


# --------------------------------------------------------------------------
# Project / observation
# --------------------------------------------------------------------------


class ProjectDescriptor(_Record):
    """Trusted local-process project data.

    ``local_repo_root`` is never auto-embedded into a web prompt; only
    :class:`PromptProjectSnapshot` reaches prompt content.
    """

    project_key: ProjectKey
    worktree_key: WorktreeKey | None = None
    local_repo_root: str | None = None
    sanitized_remote_repository: str | None = None
    configured_prompt_mode: PromptExecutionMode | None = None
    protocol_profile: str | None = None
    configuration_identity: DigestRef


class ObservationPolicy(_Record):
    remote_mode: RemoteMode = RemoteMode.LOCAL_ONLY
    max_remote_staleness_seconds: int | None = None


class ProjectQuery(_Record):
    limit: int = 100
    cursor: str | None = None


class ProjectObservationRequest(_Record):
    project: ProjectKey
    policy: ObservationPolicy = ObservationPolicy()


class ProjectObservation(_Record):
    project_key: ProjectKey
    worktree_key: WorktreeKey
    candidate: CandidateRef
    selected_remote: RemoteRepositoryRef | None = None
    remote_diagnostics: tuple[str, ...] = ()
    policy: ObservationPolicy = ObservationPolicy()
    local_repo_root: str | None = None


class PromptProjectSnapshot(_Record):
    """Prompt-mode-safe context actually eligible to enter prompt text."""

    prompt_execution_mode: PromptExecutionMode
    repository_target: str
    candidate_commit: str | None = None
    target_ref: str | None = None
    remote_evidence: RemoteEvidence = RemoteEvidence.NONE
    notes: tuple[str, ...] = ()


# --------------------------------------------------------------------------
# Workplans
# --------------------------------------------------------------------------


class WorkplanDescriptor(_Record):
    ref: WorkplanRef
    kind: str | None = None
    target_branch: str | None = None
    is_current_authority: bool = True
    superseded_by: str | None = None
    diagnostics: tuple[str, ...] = ()


class WorkplanQuery(_Record):
    project: ProjectKey
    lifecycle_states: tuple[LifecycleState, ...] = (
        LifecycleState.ACTIVE,
        LifecycleState.ARCHIVE,
    )
    limit: int = 200
    cursor: str | None = None
    include_historical_revisions: bool = False


class WorkplanResolutionRequest(_Record):
    project: ProjectKey
    stage: StageRef
    selector: str | None = None
    branch: str | None = None


class WorkplanResolution(_Record):
    """Outcome of stage-specific governing-workplan selection.

    ``selection_basis`` is the evidence that produced ``workplan``: it exists so
    consumers can audit the choice instead of re-deriving it.
    """

    stage: StageRef
    policy: WorkplanPolicy
    workplan: WorkplanRef | None = None
    selection_basis: str
    considered: tuple[str, ...] = ()


# --------------------------------------------------------------------------
# Workflow profile
# --------------------------------------------------------------------------


class InputBinding(_Record):
    name: str
    ownership: InputOwnership
    default_value: str | None = None
    override_allowed: bool = True
    mode_dependent: bool = False
    first_class_source: str | None = None
    description: str | None = None


class StageDescriptor(_Record):
    stage: StageRef
    aliases: tuple[str, ...] = ()
    title: str
    role_owner: str
    mutation_class: str
    optionality: str
    recognized_outcomes: tuple[str, ...] = ()
    workplan_policy: WorkplanPolicy = WorkplanPolicy.EXPLICIT_ONLY
    inputs: tuple[InputBinding, ...] = ()


class StageTransitionDescriptor(_Record):
    from_stage: StageRef
    trigger_key: str
    to_stage: StageRef | None = None
    terminal: bool = False
    priority_hint: int | None = None
    explanation: str = ""


class WorkflowProfileDescriptor(_Record):
    profile: ProtocolProfileRef
    schema_version: int
    stages: tuple[StageDescriptor, ...] = ()
    transitions: tuple[StageTransitionDescriptor, ...] = ()
    result_schema_id: str = ""
    result_schema_version: int = 1


class WorkflowRequest(_Record):
    project: ProjectKey | None = None
    profile: ProtocolProfileRef | None = None
    workplan: WorkplanRef | None = None


# --------------------------------------------------------------------------
# Prompt preparation / rendering
# --------------------------------------------------------------------------


class ResolvedInput(_Record):
    name: str
    ownership: InputOwnership
    value: str | None = None
    provenance: str = ""
    mode_dependent: bool = False


class PromptPreparationRequest(_Record):
    """Route-independent preparation request. Carries no local/web prompt mode."""

    project: ProjectKey
    stage: StageSelector
    run_id: RunId | None = None
    workplan_selector: str | None = None
    first_task: str | None = None
    input_overrides: tuple[tuple[str, str], ...] = ()
    policy: ObservationPolicy = ObservationPolicy()


class PreparedPrompt(_Record):
    run_id: RunId
    preparation_fingerprint: DigestRef
    stage: StageRef
    observation: ProjectObservation
    workplan_resolution: WorkplanResolution
    profile: ProtocolProfileRef
    workflow: WorkflowProfileDescriptor
    prompt_source: PromptSourceRef
    inputs: tuple[ResolvedInput, ...] = ()
    result_schema_id: str = ""
    result_schema_version: int = 1


class PromptRenderRequest(_Record):
    prepared: PreparedPrompt
    prompt_execution_mode: PromptExecutionMode


class RenderedPrompt(_Record):
    run_id: RunId
    stage: StageRef
    prompt_execution_mode: PromptExecutionMode
    prompt_text: str
    prompt_fingerprint: DigestRef
    preparation_fingerprint: DigestRef
    snapshot: PromptProjectSnapshot
    inputs: tuple[ResolvedInput, ...] = ()
    result_schema_id: str = ""
    result_schema_version: int = 1


# --------------------------------------------------------------------------
# Result envelope (requested, never parsed by Core in WP-1)
# --------------------------------------------------------------------------


class BlockerRecord(_Record):
    summary: str
    blocker_id: str | None = None
    classification: str | None = None
    authority_class: str | None = None


class StageResultEnvelope(_Record):
    """Schema Core *requests* in every prompt footer.

    Core does not parse or persist it in WP-1; the type exists so the contract is
    executable and frozen for Tracker.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    schema_version: int
    run_id: str
    prompt_fingerprint: str
    stage: str
    outcome: str
    recommended_next_stage: str | None = None
    blockers: tuple[BlockerRecord, ...] = ()
    completed_obligations: tuple[str, ...] = ()
    pending_obligations: tuple[str, ...] = ()
    checks_executed: tuple[str, ...] = ()
    checks_unavailable: tuple[str, ...] = ()
    candidate: str | None = None
    summary: str | None = None


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------


class EventEnvelope(_Record):
    event_id: EventId
    event_type: str
    schema_version: int
    occurred_at: str
    project_key: ProjectKey | None = None
    run_id: RunId | None = None
    producer_extension: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class EventSubscription(_Record):
    event_types: tuple[str, ...]


# --------------------------------------------------------------------------
# Capabilities / composition
# --------------------------------------------------------------------------


class CapabilityRequirement(_Record):
    key: CapabilityKey
    api_spec: str = ""
    multiplicity: Multiplicity = Multiplicity.SINGULAR


class CapabilityProvision(_Record):
    key: CapabilityKey
    api_major: int
    multiplicity: Multiplicity = Multiplicity.SINGULAR


class CapabilityStatus(_Record):
    key: CapabilityKey
    state: str  # active | discovered | disabled | unavailable
    api_major: int | None = None
    providers: tuple[str, ...] = ()
    detail: str | None = None


class ExtensionManifest(_Record):
    extension_id: ExtensionId
    extension_version: str
    core_spi_spec: str = ""
    requires_extensions: tuple[str, ...] = ()
    requires_capabilities: tuple[CapabilityRequirement, ...] = ()
    provides_capabilities: tuple[CapabilityProvision, ...] = ()


class ExtensionRegistration(_Record):
    services: tuple[tuple[CapabilityKey, int], ...] = ()
    subscriptions: tuple[EventSubscription, ...] = ()
    detail: str | None = None


class ExtensionStatus(_Record):
    extension_id: ExtensionId
    state: str  # discovered | active | disabled | failed
    distribution: str | None = None
    entry_point: str | None = None
    version: str | None = None
    detail: str | None = None


class ApplicationRequest(_Record):
    config_path: str | None = None
    activation_policy: ActivationPolicy = ActivationPolicy.DISCOVERY_ONLY
