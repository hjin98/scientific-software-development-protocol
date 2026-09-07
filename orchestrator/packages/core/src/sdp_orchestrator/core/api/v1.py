"""``sdp_orchestrator.core.api.v1`` -- the public Core consumer API.

Everything re-exported here is a public v1 record, protocol, enumeration, or
factory. Nothing in this module exposes a Git handle, subprocess, file object,
lock, or other implementation type, and higher modules must import from here (or
from :mod:`sdp_orchestrator.core.spi.v1`) rather than from private modules.

Compatibility: additive optional fields and new methods may appear within v1;
anything that changes existing request/response semantics requires a new major.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .._app import CORE_CAPABILITIES, create_application
from .._errors import ERROR_CODES, OrchestratorError, Problem
from .._events import PROMPT_RENDERED_EVENT, PROMPT_RENDERED_SCHEMA_VERSION, logical_event_id
from .._profile import RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION
from .._records import (
    ActivationPolicy,
    ApplicationRequest,
    BlockerRecord,
    CandidateRef,
    CapabilityKey,
    CapabilityProvision,
    CapabilityRequirement,
    CapabilityStatus,
    DigestRef,
    EventEnvelope,
    EventId,
    EventSubscription,
    ExtensionId,
    ExtensionManifest,
    ExtensionRegistration,
    ExtensionStatus,
    InputBinding,
    InputOwnership,
    LifecycleState,
    Multiplicity,
    Page,
    PreparedPrompt,
    ProjectDescriptor,
    ProjectKey,
    ProjectObservation,
    ProjectObservationRequest,
    ProjectQuery,
    PromptExecutionMode,
    PromptPreparationRequest,
    PromptProjectSnapshot,
    PromptRenderRequest,
    PromptSourceRef,
    ProtocolProfileRef,
    ObservationPolicy,
    RemoteEvidence,
    RemoteMode,
    RemoteRepositoryRef,
    RenderedPrompt,
    ResolvedInput,
    RunId,
    StageDescriptor,
    StageRef,
    StageResultEnvelope,
    StageSelector,
    StageTransitionDescriptor,
    WorkflowProfileDescriptor,
    WorkflowRequest,
    WorkplanDescriptor,
    WorkplanPolicy,
    WorkplanQuery,
    WorkplanRef,
    WorkplanResolution,
    WorkplanResolutionRequest,
    WorktreeKey,
)
from .._render import FOOTER_BEGIN, FOOTER_END, extract_result_footer

API_MAJOR = 1


@runtime_checkable
class CoreAPI(Protocol):
    """Read-only with respect to every target repository."""

    def allocate_run_id(self) -> RunId: ...

    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]: ...

    def get_project(self, project: ProjectKey) -> ProjectDescriptor: ...

    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...

    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]: ...

    def resolve_workplan(self, request: WorkplanResolutionRequest) -> WorkplanResolution: ...

    def workflow(self, request: WorkflowRequest) -> WorkflowProfileDescriptor: ...

    def list_stages(self, request: WorkflowRequest) -> tuple[StageDescriptor, ...]: ...

    def prepare(self, request: PromptPreparationRequest) -> PreparedPrompt: ...

    def render(self, request: PromptRenderRequest) -> RenderedPrompt: ...


@runtime_checkable
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...

    def has(self, requirement: CapabilityRequirement) -> bool: ...

    def service(self, requirement: CapabilityRequirement) -> object: ...

    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...

    def core(self) -> CoreAPI: ...


__all__ = [
    "API_MAJOR",
    "ActivationPolicy",
    "ApplicationAPI",
    "ApplicationRequest",
    "BlockerRecord",
    "CORE_CAPABILITIES",
    "CandidateRef",
    "CapabilityKey",
    "CapabilityProvision",
    "CapabilityRequirement",
    "CapabilityStatus",
    "CoreAPI",
    "DigestRef",
    "ERROR_CODES",
    "EventEnvelope",
    "EventId",
    "EventSubscription",
    "ExtensionId",
    "ExtensionManifest",
    "ExtensionRegistration",
    "ExtensionStatus",
    "FOOTER_BEGIN",
    "FOOTER_END",
    "InputBinding",
    "InputOwnership",
    "LifecycleState",
    "Multiplicity",
    "ObservationPolicy",
    "OrchestratorError",
    "PROMPT_RENDERED_EVENT",
    "PROMPT_RENDERED_SCHEMA_VERSION",
    "Page",
    "PreparedPrompt",
    "Problem",
    "ProjectDescriptor",
    "ProjectKey",
    "ProjectObservation",
    "ProjectObservationRequest",
    "ProjectQuery",
    "PromptExecutionMode",
    "PromptPreparationRequest",
    "PromptProjectSnapshot",
    "PromptRenderRequest",
    "PromptSourceRef",
    "ProtocolProfileRef",
    "RESULT_SCHEMA_ID",
    "RESULT_SCHEMA_VERSION",
    "RemoteEvidence",
    "RemoteMode",
    "RemoteRepositoryRef",
    "RenderedPrompt",
    "ResolvedInput",
    "RunId",
    "StageDescriptor",
    "StageRef",
    "StageResultEnvelope",
    "StageSelector",
    "StageTransitionDescriptor",
    "WorkflowProfileDescriptor",
    "WorkflowRequest",
    "WorkplanDescriptor",
    "WorkplanPolicy",
    "WorkplanQuery",
    "WorkplanRef",
    "WorkplanResolution",
    "WorkplanResolutionRequest",
    "WorktreeKey",
    "create_application",
    "extract_result_footer",
    "logical_event_id",
]
