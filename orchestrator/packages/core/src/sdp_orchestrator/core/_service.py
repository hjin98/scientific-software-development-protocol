"""The Core service: the single implementation of ``CoreAPI`` v1.

Preparation and rendering are deliberately separate phases.

``prepare()`` resolves everything a route cannot influence -- stage identity under
a compatible profile, the candidate, the governing workplan, the workflow profile,
the render source, and mode-independent inputs -- and returns a
:class:`PreparedPrompt` with a versioned fingerprint. It renders nothing and emits
no event, so a later Adapter/Scheduler can admit a route *between* the phases
without Core ever producing a provisional prompt.

``render()`` adds the one route-sensitive fact (local vs web), re-checks that the
material preparation state has not moved underneath it, and only then assembles
the artifact. A mixed snapshot -- prompt text describing two different repository
states -- is the failure this revalidation exists to prevent.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from . import _errors as E
from . import _profile as P
from . import _protocolsrc as PS
from . import _render as R
from . import _workplans as W
from ._config import CoreConfig, ProjectSection
from ._digest import SCHEME_PROMPT_PREPARATION, digest_canonical
from ._events import EventBus
from ._git import Observation, WorktreeIdentity, identify_worktree, observe
from ._inputs import normalize_overrides, resolve_inputs
from ._records import (
    CandidateRef,
    DigestRef,
    Page,
    PreparedPrompt,
    ProjectDescriptor,
    ProjectKey,
    ProjectObservation,
    ProjectObservationRequest,
    ProjectQuery,
    PromptPreparationRequest,
    PromptRenderRequest,
    PromptSourceRef,
    RenderedPrompt,
    RunId,
    StageDescriptor,
    WorkflowProfileDescriptor,
    WorkflowRequest,
    WorkplanDescriptor,
    WorkplanQuery,
    WorkplanRef,
    WorkplanResolution,
    WorkplanResolutionRequest,
)


@dataclass(frozen=True)
class _ProjectContext:
    key: ProjectKey
    section: ProjectSection
    identity: WorktreeIdentity


class CoreService:
    """Read-only with respect to every target repository."""

    def __init__(self, config: CoreConfig, events: EventBus | None = None) -> None:
        self._config = config
        self._events = events or EventBus()

    # -- identity ---------------------------------------------------------

    def allocate_run_id(self) -> RunId:
        return RunId(f"run-{uuid.uuid4().hex}")

    # -- projects ---------------------------------------------------------

    def _context(self, project: ProjectKey) -> _ProjectContext:
        section = self._config.project(str(project))
        return _ProjectContext(
            key=project, section=section, identity=identify_worktree(Path(section.repo))
        )

    def _descriptor(self, key: str, section: ProjectSection) -> ProjectDescriptor:
        try:
            identity = identify_worktree(Path(section.repo))
            root: str | None = str(identity.toplevel)
            worktree_key = identity.worktree_key
        except E.OrchestratorError:
            root, worktree_key = None, None
        return ProjectDescriptor(
            project_key=ProjectKey(key),
            worktree_key=worktree_key,
            local_repo_root=root,
            sanitized_remote_repository=None,
            configured_prompt_mode=section.default_prompt_mode,
            protocol_profile=section.protocol_profile,
            configuration_identity=self._config.identity,
        )

    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]:
        request = query or ProjectQuery()
        keys = sorted(self._config.projects)
        start = keys.index(request.cursor) + 1 if request.cursor in keys else 0
        window = keys[start : start + max(1, request.limit)]
        items = tuple(self._descriptor(key, self._config.projects[key]) for key in window)
        end = start + len(window)
        return Page[ProjectDescriptor](
            items=items,
            next_cursor=window[-1] if end < len(keys) and window else None,
            total_known=len(keys),
        )

    def get_project(self, project: ProjectKey) -> ProjectDescriptor:
        return self._descriptor(str(project), self._config.project(str(project)))

    def resolve_project_key(self, explicit: str | None, cwd: Path | None = None) -> ProjectKey:
        """CLI convenience resolution. Public API requests always name a project.

        Precedence: explicit -> unique project containing cwd -> [core].default_project
        -> sole configured project -> explicit ambiguity.
        """

        if explicit:
            self._config.project(explicit)
            return ProjectKey(explicit)
        if not self._config.projects:
            E.fail(
                E.PROJECT_NOT_FOUND,
                "no projects are configured",
                details={"config_path": str(self._config.path) if self._config.path else None},
                remediation="add a [projects.<key>] section to the configuration",
            )
        here = (cwd or Path(os.getcwd())).resolve()
        containing: list[str] = []
        for key, section in self._config.projects.items():
            try:
                root = identify_worktree(Path(section.repo)).toplevel
            except E.OrchestratorError:
                continue
            if here == root or here.is_relative_to(root):
                containing.append(key)
        if len(containing) == 1:
            return ProjectKey(containing[0])
        if len(containing) > 1:
            E.fail(
                E.PROJECT_AMBIGUOUS,
                "the current directory lies inside several configured projects",
                details={"candidates": sorted(containing)},
                remediation="pass --project <key>",
            )
        if self._config.core.default_project:
            return ProjectKey(self._config.core.default_project)
        if len(self._config.projects) == 1:
            return ProjectKey(next(iter(self._config.projects)))
        E.fail(
            E.PROJECT_AMBIGUOUS,
            "several projects are configured and none is selected",
            details={"configured": sorted(self._config.projects)},
            remediation="pass --project <key> or set [core].default_project",
        )

    # -- observation ------------------------------------------------------

    def _observe(self, context: _ProjectContext, request: ProjectObservationRequest) -> Observation:
        return observe(
            context.identity,
            remote_mode=request.policy.remote_mode,
            configured_remote_name=context.section.remote_name,
        )

    def observe(self, request: ProjectObservationRequest) -> ProjectObservation:
        context = self._context(request.project)
        result = self._observe(context, request)
        return ProjectObservation(
            project_key=request.project,
            worktree_key=context.identity.worktree_key,
            candidate=result.candidate,
            selected_remote=result.remote,
            remote_diagnostics=result.diagnostics,
            policy=request.policy,
            local_repo_root=str(context.identity.toplevel),
        )

    # -- workplans --------------------------------------------------------

    def _catalog(self, context: _ProjectContext) -> tuple[W.CatalogEntry, ...]:
        return W.build_catalog(context.identity.toplevel)

    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]:
        context = self._context(request.project)
        states = set(request.lifecycle_states)
        entries = [
            entry
            for entry in self._catalog(context)
            if entry.descriptor.ref.lifecycle_state in states
            and (request.include_historical_revisions or entry.descriptor.superseded_by is None)
        ]
        paths = [entry.relative_path for entry in entries]
        start = paths.index(request.cursor) + 1 if request.cursor in paths else 0
        window = entries[start : start + max(1, request.limit)]
        end = start + len(window)
        return Page[WorkplanDescriptor](
            items=tuple(entry.descriptor for entry in window),
            next_cursor=window[-1].relative_path if end < len(entries) and window else None,
            total_known=len(entries),
        )

    def resolve_workplan(self, request: WorkplanResolutionRequest) -> WorkplanResolution:
        context = self._context(request.project)
        descriptor = self._workflow_descriptor_for_project(context)
        stage = P.stage_descriptor(descriptor, request.stage)
        return W.resolve(
            self._catalog(context),
            stage=request.stage,
            policy=stage.workplan_policy,
            selector=request.selector,
            branch=request.branch,
        )

    # -- workflow profile -------------------------------------------------

    def _protocol_source(self, profile_id: str) -> PS.ResolvedProtocolSource:
        section = self._config.protocol_sources.get(profile_id)
        return PS.resolve(section, profile_id=profile_id)

    def _profile_id_for(self, context: _ProjectContext, workplan: WorkplanRef | None) -> str:
        """Governing workplan protocol version wins over the project default."""

        if workplan is not None:
            declared = workplan.protocol_version
            if declared is None:
                E.fail(
                    E.PROTOCOL_UNAVAILABLE,
                    "the governing workplan declares no protocol_version",
                    details={"workplan": workplan.path},
                    remediation="add protocol_version to the workplan frontmatter",
                )
            if declared not in P.COMPATIBLE_PROTOCOL_VERSIONS:
                E.fail(
                    E.PROTOCOL_INCOMPATIBLE,
                    "the governing workplan declares a protocol version with no compatible profile",
                    details={
                        "workplan": workplan.path,
                        "declared": declared,
                        "compatible": list(P.COMPATIBLE_PROTOCOL_VERSIONS),
                    },
                )
            return P.PROFILE_ID
        return context.section.protocol_profile or P.PROFILE_ID

    def _workflow_descriptor_for_project(
        self, context: _ProjectContext
    ) -> WorkflowProfileDescriptor:
        profile_id = context.section.protocol_profile or P.PROFILE_ID
        return self._protocol_source(profile_id).snapshot.descriptor

    def workflow(self, request: WorkflowRequest) -> WorkflowProfileDescriptor:
        if request.profile is not None:
            return self._protocol_source(request.profile.profile_id).snapshot.descriptor
        if request.project is None:
            E.fail(
                E.PROTOCOL_UNAVAILABLE,
                "a workflow request needs an explicit profile or a project context",
            )
        context = self._context(request.project)
        profile_id = self._profile_id_for(context, request.workplan)
        return self._protocol_source(profile_id).snapshot.descriptor

    def list_stages(self, request: WorkflowRequest) -> tuple[StageDescriptor, ...]:
        return self.workflow(request).stages

    # -- preparation ------------------------------------------------------

    def prepare(self, request: PromptPreparationRequest) -> PreparedPrompt:
        context = self._context(request.project)
        run_id = request.run_id or self.allocate_run_id()

        observation = self.observe(
            ProjectObservationRequest(project=request.project, policy=request.policy)
        )

        # Stage identity requires a profile, and the governing profile may come
        # from the selected workplan -- so resolve the project-default profile
        # first only to interpret the selector, then rebind if the plan disagrees.
        bootstrap = self._protocol_source(context.section.protocol_profile or P.PROFILE_ID)
        stage_ref = P.resolve_stage_key(bootstrap.snapshot.descriptor, str(request.stage))
        stage_descriptor = P.stage_descriptor(bootstrap.snapshot.descriptor, stage_ref)

        resolution = W.resolve(
            self._catalog(context),
            stage=stage_ref,
            policy=stage_descriptor.workplan_policy,
            selector=request.workplan_selector,
            branch=observation.candidate.branch,
        )

        governing_workplan = (
            resolution.workplan
            if resolution.policy
            in (W.WorkplanPolicy.REQUIRED, W.WorkplanPolicy.EXPLICIT_REQUIRED)
            else None
        )
        profile_id = self._profile_id_for(context, governing_workplan)
        source = (
            bootstrap
            if profile_id == bootstrap.snapshot.descriptor.profile.profile_id
            else self._protocol_source(profile_id)
        )
        descriptor = source.snapshot.descriptor
        stage_ref = P.resolve_stage_key(descriptor, str(request.stage))
        stage_descriptor = P.stage_descriptor(descriptor, stage_ref)

        governing_version = (
            governing_workplan.protocol_version
            if governing_workplan is not None and governing_workplan.protocol_version
            else descriptor.profile.protocol_version
        )

        inputs = resolve_inputs(
            stage_descriptor,
            workplan=resolution.workplan,
            first_task=request.first_task,
            overrides=normalize_overrides(request.input_overrides),
            governing_protocol_version=governing_version,
        )

        prepared = PreparedPrompt(
            run_id=run_id,
            preparation_fingerprint=DigestRef(algorithm="sha256", value="0" * 64),
            stage=stage_ref,
            observation=observation,
            workplan_resolution=resolution,
            profile=descriptor.profile,
            workflow=descriptor,
            prompt_source=source.source,
            inputs=inputs,
            result_schema_id=descriptor.result_schema_id,
            result_schema_version=descriptor.result_schema_version,
        )
        return prepared.model_copy(
            update={"preparation_fingerprint": preparation_fingerprint(prepared)}
        )

    # -- render -----------------------------------------------------------

    def render(self, request: PromptRenderRequest) -> RenderedPrompt:
        prepared = request.prepared
        context = self._context(prepared.observation.project_key)
        self._revalidate(context, prepared)

        snapshot = R.build_snapshot(prepared.observation, request.prompt_execution_mode)
        source = self._protocol_source(prepared.profile.profile_id)
        body = source.snapshot.bodies[prepared.stage.stage_key]

        text, fingerprint = R.assemble(
            body=body,
            run_id=str(prepared.run_id),
            stage=prepared.stage,
            inputs=prepared.inputs,
            snapshot=snapshot,
            result_schema_id=prepared.result_schema_id,
            result_schema_version=prepared.result_schema_version,
        )

        rendered = RenderedPrompt(
            run_id=prepared.run_id,
            stage=prepared.stage,
            prompt_execution_mode=request.prompt_execution_mode,
            prompt_text=text,
            prompt_fingerprint=fingerprint,
            preparation_fingerprint=prepared.preparation_fingerprint,
            snapshot=snapshot,
            inputs=prepared.inputs,
            result_schema_id=prepared.result_schema_id,
            result_schema_version=prepared.result_schema_version,
        )
        # Only a fully constructed artifact produces an event.
        self._events.publish(
            self._events.build_prompt_event(
                project_key=prepared.observation.project_key,
                run_id=prepared.run_id,
                prompt_fingerprint=fingerprint.value,
                payload={
                    "stage": prepared.stage.stage_key,
                    "prompt_execution_mode": request.prompt_execution_mode.value,
                    "prompt_text": text,
                    "preparation_fingerprint": prepared.preparation_fingerprint.value,
                },
            )
        )
        return rendered

    def _revalidate(self, context: _ProjectContext, prepared: PreparedPrompt) -> None:
        """Refuse to render a prompt assembled from a state that has since moved."""

        current = observe(
            context.identity,
            remote_mode=prepared.observation.policy.remote_mode,
            configured_remote_name=context.section.remote_name,
        )
        if _candidate_identity(current.candidate) != _candidate_identity(
            prepared.observation.candidate
        ):
            E.fail(
                E.CONTEXT_STALE,
                "the candidate changed between preparation and final render",
                remediation="re-run the command to prepare and render one coherent snapshot",
            )

        selected = prepared.workplan_resolution.workplan
        if selected is not None:
            catalog = {
                entry.relative_path: entry.descriptor.ref for entry in self._catalog(context)
            }
            now = catalog.get(selected.path)
            if now is None:
                E.fail(
                    E.CONTEXT_STALE,
                    "the selected workplan disappeared between preparation and final render",
                    details={"workplan": selected.path},
                )
            if _workplan_identity(now) != _workplan_identity(selected):
                E.fail(
                    E.CONTEXT_STALE,
                    "the selected workplan changed between preparation and final render",
                    details={"workplan": selected.path},
                )

        source = self._protocol_source(prepared.profile.profile_id)
        if source.mutable_identity is not None and (
            source.source.identity != prepared.prompt_source.identity
        ):
            E.fail(
                E.CONTEXT_STALE,
                "the local Protocol render source changed between preparation and final render",
                details={"source": prepared.prompt_source.kind},
            )


# --------------------------------------------------------------------------
# sdp.prompt-preparation.v1
# --------------------------------------------------------------------------


def _candidate_identity(candidate: CandidateRef) -> dict[str, object]:
    """Material candidate identity. ``observed_at`` is excluded: it is wall clock."""

    return {
        "repository_id": candidate.repository_id,
        "branch": candidate.branch,
        "detached": candidate.detached,
        "head_commit": candidate.head_commit,
        "working_tree_digest": (
            candidate.working_tree_digest.value if candidate.working_tree_digest else None
        ),
        "identity_complete": candidate.identity_complete,
        "upstream_ref": candidate.upstream_ref,
        "observed_remote_commit": candidate.observed_remote_commit,
        "remote_evidence": candidate.remote_evidence.value,
    }


def _workplan_identity(ref: WorkplanRef) -> dict[str, object]:
    return {
        "workplan_id": ref.workplan_id,
        "protocol_version": ref.protocol_version,
        "path": ref.path,
        "artifact_digest": ref.artifact_digest.value,
        "semantic_digest": ref.semantic_digest.value if ref.semantic_digest else None,
        "semantic_identity_complete": ref.semantic_identity_complete,
        "lifecycle_state": ref.lifecycle_state.value,
        "lifecycle_consistent": ref.lifecycle_consistent,
    }


def _source_identity(source: PromptSourceRef) -> dict[str, object]:
    """Content identity of the render source.

    ``sanitized_location`` is excluded on purpose: two checkouts with identical
    content produce identical prompts, so moving a local root must not change
    preparation identity.
    """

    return {
        "kind": source.kind,
        "identity": source.identity,
        "requested_ref": source.requested_ref,
        "resolved_ref": source.resolved_ref,
        "content_digests": [
            [name, digest.value] for name, digest in source.content_digests
        ],
    }


def preparation_fingerprint(prepared: PreparedPrompt) -> DigestRef:
    """Compute ``sdp.prompt-preparation.v1`` over the mode-independent identity.

    Excluded by design: observation timestamps, remote/Git diagnostics, unrelated
    extension configuration, and every mode-dependent input value. Included:
    everything that would change what the final prompt means.
    """

    observation = prepared.observation
    remote = observation.selected_remote
    payload = {
        "scheme": SCHEME_PROMPT_PREPARATION,
        "run_id": str(prepared.run_id),
        "project_key": str(observation.project_key),
        "worktree_key": str(observation.worktree_key),
        "stage": {
            "profile_id": prepared.stage.profile_id,
            "protocol_version": prepared.stage.protocol_version,
            "stage_key": prepared.stage.stage_key,
        },
        "candidate": _candidate_identity(observation.candidate),
        "selected_remote": (
            None
            if remote is None
            else {
                "remote_name": remote.remote_name,
                "sanitized_repository": remote.sanitized_repository,
                "scheme": remote.scheme,
                "web_addressable": remote.web_addressable,
            }
        ),
        "observation_policy": {
            "remote_mode": observation.policy.remote_mode.value,
            "max_remote_staleness_seconds": observation.policy.max_remote_staleness_seconds,
        },
        "workplan": {
            "policy": prepared.workplan_resolution.policy.value,
            "selection_basis": prepared.workplan_resolution.selection_basis,
            "selected": (
                None
                if prepared.workplan_resolution.workplan is None
                else _workplan_identity(prepared.workplan_resolution.workplan)
            ),
        },
        "profile": {
            "profile_id": prepared.profile.profile_id,
            "profile_schema_version": prepared.profile.profile_schema_version,
            "protocol_version": prepared.profile.protocol_version,
            "compatible_protocol_versions": list(prepared.profile.compatible_protocol_versions),
            "source_digest": (
                prepared.profile.source_digest.value if prepared.profile.source_digest else None
            ),
        },
        "prompt_source": _source_identity(prepared.prompt_source),
        "inputs": [
            {
                "name": item.name,
                "ownership": item.ownership.value,
                "value": item.value,
                "provenance": item.provenance,
            }
            for item in prepared.inputs
            if not item.mode_dependent
        ],
        "mode_dependent_inputs": [
            item.name for item in prepared.inputs if item.mode_dependent
        ],
        "result_schema": {
            "id": prepared.result_schema_id,
            "version": prepared.result_schema_version,
        },
    }
    return digest_canonical(payload, SCHEME_PROMPT_PREPARATION)


__all__ = ["CoreService", "preparation_fingerprint"]
