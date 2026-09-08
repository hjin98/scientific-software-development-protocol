"""The Core service: one implementation of the public CoreAPI v1 records.

Preparation and rendering remain separate.  Protocol 6 changes profile/source
selection, not the public record seam: a declared workplan protocol version is
resolved to its compatible profile before stage semantics are interpreted.
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from . import errors as E
from . import profile as P
from . import protocol_source as PS
from . import render as R
from . import workplans as W
from .config import CoreConfig, ProjectSection
from .digest import SCHEME_PROMPT_PREPARATION, digest_canonical
from .events import EventBus
from .git import Observation, WorktreeIdentity, identify_worktree, observe
from .inputs import normalize_overrides, resolve_inputs
from .records import (
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
    ProtocolProfileRef,
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

    def allocate_run_id(self) -> RunId:
        return RunId(f"run-{uuid.uuid4().hex}")

    def _context(self, project: ProjectKey) -> _ProjectContext:
        section = self._config.project(str(project))
        return _ProjectContext(key=project, section=section, identity=identify_worktree(Path(section.repo)))

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
        return Page(items=items, next_cursor=window[-1] if end < len(keys) and window else None, total_known=len(keys))

    def get_project(self, project: ProjectKey) -> ProjectDescriptor:
        return self._descriptor(str(project), self._config.project(str(project)))

    def resolve_project_key(self, explicit: str | None, cwd: Path | None = None) -> ProjectKey:
        if explicit:
            self._config.project(explicit)
            return ProjectKey(explicit)
        if not self._config.projects:
            E.fail(E.PROJECT_NOT_FOUND, "no projects are configured", details={"config_path": str(self._config.path) if self._config.path else None}, remediation="add a [projects.<key>] section to the configuration")
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
            E.fail(E.PROJECT_AMBIGUOUS, "the current directory lies inside several configured projects", details={"candidates": sorted(containing)}, remediation="pass --project <key>")
        if self._config.core.default_project:
            return ProjectKey(self._config.core.default_project)
        if len(self._config.projects) == 1:
            return ProjectKey(next(iter(self._config.projects)))
        E.fail(E.PROJECT_AMBIGUOUS, "several projects are configured and none is selected", details={"configured": sorted(self._config.projects)}, remediation="pass --project <key> or set [core].default_project")

    def _observe(self, context: _ProjectContext, request: ProjectObservationRequest) -> Observation:
        return observe(
            context.identity,
            remote_mode=request.policy.remote_mode,
            configured_remote_name=context.section.remote_name,
            max_remote_staleness_seconds=request.policy.max_remote_staleness_seconds,
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

    def _catalog(self, context: _ProjectContext) -> tuple[W.CatalogEntry, ...]:
        return W.build_catalog(context.identity.toplevel)

    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]:
        context = self._context(request.project)
        states = set(request.lifecycle_states)
        entries = [entry for entry in self._catalog(context) if entry.descriptor.ref.lifecycle_state in states and (request.include_historical_revisions or entry.descriptor.superseded_by is None)]
        paths = [entry.relative_path for entry in entries]
        start = paths.index(request.cursor) + 1 if request.cursor in paths else 0
        window = entries[start : start + max(1, request.limit)]
        end = start + len(window)
        return Page(items=tuple(entry.descriptor for entry in window), next_cursor=window[-1].relative_path if end < len(entries) and window else None, total_known=len(entries))

    def resolve_workplan(self, request: WorkplanResolutionRequest) -> WorkplanResolution:
        context = self._context(request.project)
        descriptor = self._protocol_source(request.stage.profile_id).snapshot.descriptor
        stage = P.stage_descriptor(descriptor, request.stage)
        return W.resolve(self._catalog(context), stage=request.stage, policy=stage.workplan_policy, selector=request.selector, branch=request.branch)

    def _protocol_source(self, profile_id: str) -> PS.ResolvedProtocolSource:
        section = self._config.protocol_sources.get(profile_id)
        return PS.resolve(section, profile_id=profile_id)

    def _profile_id_for(
        self,
        context: _ProjectContext | None,
        workplan: WorkplanRef | None,
        *,
        require_version: bool = False,
    ) -> str:
        """Bind a workplan to its declared protocol before interpreting stages.

        An exact workplan declaration outranks a project-default profile.  This is
        what prevents a Protocol 5.16 workplan from being interpreted by the
        current Protocol 6 profile (and vice versa).
        """

        if workplan is not None:
            declared = workplan.protocol_version
            if declared is None:
                if require_version:
                    E.fail(
                        E.PROTOCOL_UNAVAILABLE,
                        "the governing workplan declares no protocol_version",
                        details={"workplan": workplan.path},
                        remediation="add protocol_version to the workplan frontmatter",
                    )
                configured = context.section.protocol_profile if context is not None else None
                selected = configured or P.DEFAULT_PROFILE_ID
                P.definition(selected)
                return selected
            return P.profile_id_for_version(declared)

        configured = context.section.protocol_profile if context is not None else None
        selected = configured or P.DEFAULT_PROFILE_ID
        P.definition(selected)
        return selected

    def _validate_profile_ref(self, requested: ProtocolProfileRef, descriptor: WorkflowProfileDescriptor) -> None:
        expected = descriptor.profile
        if (
            requested.profile_id != expected.profile_id
            or requested.profile_schema_version != expected.profile_schema_version
            or requested.protocol_version != expected.protocol_version
            or requested.compatible_protocol_versions != expected.compatible_protocol_versions
            or (requested.source_digest is not None and requested.source_digest != expected.source_digest)
        ):
            E.fail(
                E.PROTOCOL_INCOMPATIBLE,
                "the supplied Protocol profile identity does not match the resolved source",
                details={"requested_profile": requested.profile_id, "resolved_profile": expected.profile_id},
                remediation="use the profile identity returned by Core for the selected source",
            )

    def workflow(self, request: WorkflowRequest) -> WorkflowProfileDescriptor:
        if request.workplan is not None:
            profile_id = self._profile_id_for(None, request.workplan, require_version=True)
        elif request.profile is not None:
            profile_id = request.profile.profile_id
        elif request.project is not None:
            profile_id = self._profile_id_for(self._context(request.project), None)
        else:
            E.fail(E.PROTOCOL_UNAVAILABLE, "a workflow request needs an explicit profile or a project context")
        descriptor = self._protocol_source(profile_id).snapshot.descriptor
        if request.profile is not None:
            self._validate_profile_ref(request.profile, descriptor)
        return descriptor

    def list_stages(self, request: WorkflowRequest) -> tuple[StageDescriptor, ...]:
        return self.workflow(request).stages

    def prepare(self, request: PromptPreparationRequest) -> PreparedPrompt:
        context = self._context(request.project)
        run_id = request.run_id or self.allocate_run_id()
        observation = self.observe(ProjectObservationRequest(project=request.project, policy=request.policy))

        catalog = self._catalog(context)
        explicit_workplan = W.lookup_exact(catalog, request.workplan_selector) if request.workplan_selector else None
        bootstrap = self._protocol_source(self._profile_id_for(context, explicit_workplan))
        stage_ref = P.resolve_stage_key(bootstrap.snapshot.descriptor, str(request.stage))
        stage_descriptor = P.stage_descriptor(bootstrap.snapshot.descriptor, stage_ref)

        resolution = W.resolve(
            catalog,
            stage=stage_ref,
            policy=stage_descriptor.workplan_policy,
            selector=request.workplan_selector,
            branch=observation.candidate.branch,
        )

        selected_workplan = resolution.workplan
        governing_workplan = selected_workplan if resolution.policy in (W.WorkplanPolicy.REQUIRED, W.WorkplanPolicy.EXPLICIT_REQUIRED) else None
        profile_binding = selected_workplan if selected_workplan is not None and (governing_workplan is not None or selected_workplan.protocol_version is not None) else None
        profile_id = self._profile_id_for(context, profile_binding, require_version=governing_workplan is not None)
        source = bootstrap if profile_id == bootstrap.snapshot.descriptor.profile.profile_id else self._protocol_source(profile_id)
        descriptor = source.snapshot.descriptor
        stage_ref = P.resolve_stage_key(descriptor, str(request.stage))
        stage_descriptor = P.stage_descriptor(descriptor, stage_ref)

        governing_version = selected_workplan.protocol_version if selected_workplan is not None and selected_workplan.protocol_version else descriptor.profile.protocol_version
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
        return prepared.model_copy(update={"preparation_fingerprint": preparation_fingerprint(prepared)})

    def render(self, request: PromptRenderRequest) -> RenderedPrompt:
        prepared = request.prepared
        context = self._context(prepared.observation.project_key)
        if preparation_fingerprint(prepared) != prepared.preparation_fingerprint:
            E.fail(E.CONTEXT_STALE, "the prepared prompt fingerprint does not match its material contents", remediation="use the unmodified preparation returned by Core")
        current, source = self._revalidate(context, prepared)
        current_observation = ProjectObservation(
            project_key=prepared.observation.project_key,
            worktree_key=context.identity.worktree_key,
            candidate=current.candidate,
            selected_remote=current.remote,
            remote_diagnostics=current.diagnostics,
            policy=prepared.observation.policy,
            local_repo_root=str(context.identity.toplevel),
        )
        snapshot = R.build_snapshot(current_observation, request.prompt_execution_mode)
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
        self._revalidate(context, prepared)
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
        self._events.publish(
            self._events.build_prompt_event(
                project_key=prepared.observation.project_key,
                run_id=prepared.run_id,
                prompt_fingerprint=fingerprint.value,
                payload={"stage": prepared.stage.stage_key, "prompt_execution_mode": request.prompt_execution_mode.value, "prompt_text": text, "preparation_fingerprint": prepared.preparation_fingerprint.value},
            )
        )
        return rendered

    def _revalidate(self, context: _ProjectContext, prepared: PreparedPrompt) -> tuple[Observation, PS.ResolvedProtocolSource]:
        current = observe(
            context.identity,
            remote_mode=prepared.observation.policy.remote_mode,
            configured_remote_name=context.section.remote_name,
            max_remote_staleness_seconds=prepared.observation.policy.max_remote_staleness_seconds,
        )
        if current.candidate.repository_id != prepared.observation.candidate.repository_id:
            E.fail(E.CONTEXT_STALE, "the repository identity changed between preparation and final render")
        if context.identity.worktree_key != prepared.observation.worktree_key:
            E.fail(E.CONTEXT_STALE, "the Git worktree identity changed between preparation and final render")
        if current.remote != prepared.observation.selected_remote:
            E.fail(E.CONTEXT_STALE, "the selected remote changed between preparation and final render")
        if _candidate_identity(current.candidate) != _candidate_identity(prepared.observation.candidate):
            E.fail(E.CONTEXT_STALE, "the candidate changed between preparation and final render", remediation="re-run the command to prepare and render one coherent snapshot")

        try:
            source = self._protocol_source(prepared.profile.profile_id)
            current_stage = P.stage_descriptor(source.snapshot.descriptor, prepared.stage)
        except E.OrchestratorError as exc:
            E.fail(E.CONTEXT_STALE, "the prepared stage is not defined by the current Protocol source", details={"code": exc.problem.code})
        if source.snapshot.descriptor.model_dump(mode="json") != prepared.workflow.model_dump(mode="json"):
            E.fail(E.CONTEXT_STALE, "the workflow profile changed between preparation and final render")
        if source.snapshot.descriptor.profile != prepared.profile:
            E.fail(E.CONTEXT_STALE, "the prepared Protocol profile is not the current source profile")
        if current_stage.workplan_policy is not prepared.workplan_resolution.policy:
            E.fail(E.CONTEXT_STALE, "the prepared stage policy changed between preparation and final render")
        if _source_identity(source.source) != _source_identity(prepared.prompt_source):
            E.fail(E.CONTEXT_STALE, "the Protocol render source changed between preparation and final render", details={"source": prepared.prompt_source.kind})

        original = prepared.workplan_resolution
        selector = original.workplan.path if original.selection_basis == "explicit_selector" and original.workplan else None
        try:
            current_resolution = W.resolve(self._catalog(context), stage=prepared.stage, policy=original.policy, selector=selector, branch=current.candidate.branch)
        except E.OrchestratorError as exc:
            E.fail(E.CONTEXT_STALE, "the governing workplan resolution changed between preparation and final render", details={"code": exc.problem.code})
        if current_resolution.model_dump(mode="json") != original.model_dump(mode="json"):
            E.fail(E.CONTEXT_STALE, "the governing workplan resolution changed between preparation and final render")
        return current, source


def _digest_identity(digest: DigestRef | None) -> dict[str, object] | None:
    if digest is None:
        return None
    return {"algorithm": digest.algorithm, "canonicalization_scheme": digest.canonicalization_scheme, "value": digest.value}


def _candidate_identity(candidate: CandidateRef) -> dict[str, object]:
    return {
        "repository_id": candidate.repository_id,
        "branch": candidate.branch,
        "detached": candidate.detached,
        "head_commit": candidate.head_commit,
        "working_tree_digest": _digest_identity(candidate.working_tree_digest),
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
        "artifact_digest": _digest_identity(ref.artifact_digest),
        "semantic_digest": _digest_identity(ref.semantic_digest),
        "semantic_identity_complete": ref.semantic_identity_complete,
        "lifecycle_state": ref.lifecycle_state.value,
        "lifecycle_consistent": ref.lifecycle_consistent,
    }


def _source_identity(source: PromptSourceRef) -> dict[str, object]:
    return {
        "kind": source.kind,
        "identity": source.identity,
        "sanitized_location": source.sanitized_location,
        "requested_ref": source.requested_ref,
        "resolved_ref": source.resolved_ref,
        "content_digests": [[name, _digest_identity(digest)] for name, digest in source.content_digests],
    }


def preparation_fingerprint(prepared: PreparedPrompt) -> DigestRef:
    observation = prepared.observation
    remote = observation.selected_remote
    payload = {
        "scheme": SCHEME_PROMPT_PREPARATION,
        "run_id": str(prepared.run_id),
        "project_key": str(observation.project_key),
        "worktree_key": str(observation.worktree_key),
        "stage": {"profile_id": prepared.stage.profile_id, "protocol_version": prepared.stage.protocol_version, "stage_key": prepared.stage.stage_key},
        "candidate": _candidate_identity(observation.candidate),
        "selected_remote": None if remote is None else {"remote_name": remote.remote_name, "sanitized_repository": remote.sanitized_repository, "scheme": remote.scheme, "web_addressable": remote.web_addressable},
        "observation_policy": {"remote_mode": observation.policy.remote_mode.value, "max_remote_staleness_seconds": observation.policy.max_remote_staleness_seconds},
        "workplan": {
            "policy": prepared.workplan_resolution.policy.value,
            "selection_basis": prepared.workplan_resolution.selection_basis,
            "selected": None if prepared.workplan_resolution.workplan is None else _workplan_identity(prepared.workplan_resolution.workplan),
        },
        "profile": {
            "profile_id": prepared.profile.profile_id,
            "profile_schema_version": prepared.profile.profile_schema_version,
            "protocol_version": prepared.profile.protocol_version,
            "compatible_protocol_versions": list(prepared.profile.compatible_protocol_versions),
            "source_digest": _digest_identity(prepared.profile.source_digest),
        },
        "prompt_source": _source_identity(prepared.prompt_source),
        "workflow": prepared.workflow.model_dump(mode="json"),
        "inputs": [{"name": item.name, "ownership": item.ownership.value, "value": item.value, "provenance": item.provenance} for item in prepared.inputs if not item.mode_dependent],
        "mode_dependent_inputs": [item.name for item in prepared.inputs if item.mode_dependent],
        "result_schema": {"id": prepared.result_schema_id, "version": prepared.result_schema_version},
    }
    return digest_canonical(payload, SCHEME_PROMPT_PREPARATION)


__all__ = ["CoreService", "preparation_fingerprint"]
