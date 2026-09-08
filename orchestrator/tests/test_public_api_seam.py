"""O6 -- public API completeness and the route-admission seam between the phases.

The decisive test here is ``AdapterShapedSeamTests``: an external admission step
runs *between* ``prepare()`` and ``render()`` using only public records, and no
provisional prompt or event exists while it runs. That is the property WP-2..WP-4
depend on.
"""

from __future__ import annotations

import inspect
import json
import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import errors as E
from sdp_orchestrator.core.api import v1 as api
from sdp_orchestrator.core.spi import v1 as spi

from ._support import commit_all, config_text, init_repo, write_workplan


class SeamBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")
        write_workplan(self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main")
        write_workplan(
            self.repo, "workplans/archive/OLD.md", workplan_id="OLD", status="completed",
            protocol_version="5.9.0",
        )
        commit_all(self.repo, "workplans")
        self.config = self.root / "config.toml"
        self.config.write_text(config_text(self.repo), encoding="utf-8")

    def app(self):
        return api.create_application(api.ApplicationRequest(config_path=str(self.config)))

    def core(self):
        return self.app().core()

    def prepare(self, core, stage="implementation", **kwargs):
        return core.prepare(
            api.PromptPreparationRequest(
                project=api.ProjectKey("demo"),
                stage=api.StageSelector(stage),
                policy=api.ObservationPolicy(remote_mode=api.RemoteMode.LOCAL_ONLY),
                **kwargs,
            )
        )


class SurfaceCompletenessTests(SeamBase):
    def test_core_api_protocol_is_satisfied_by_the_implementation(self) -> None:
        core = self.core()
        for name in (
            "allocate_run_id", "projects", "get_project", "observe", "workplans",
            "resolve_workplan", "workflow", "list_stages", "prepare", "render",
        ):
            self.assertTrue(callable(getattr(core, name)), name)

    def test_application_api_protocol_is_satisfied(self) -> None:
        application = self.app()
        for name in ("capabilities", "has", "service", "services", "core"):
            self.assertTrue(callable(getattr(application, name)), name)

    def test_core_capabilities_are_provisioned(self) -> None:
        application = self.app()
        for key in ("prompt.render", "project.observe", "workplan.catalog", "workflow.profile"):
            self.assertTrue(
                application.has(api.CapabilityRequirement(key=api.CapabilityKey(key))), key
            )

    def test_all_documented_error_codes_exist(self) -> None:
        for code in (
            "core.config.invalid", "core.project.not_found", "core.project.ambiguous",
            "core.repository.invalid", "core.context.stale", "core.workplan.required",
            "core.workplan.not_found", "core.workplan.ambiguous", "core.workplan.disallowed",
            "core.protocol.incompatible", "core.protocol.unavailable",
            "core.protocol.source_incoherent", "core.stage.unknown", "core.remote.unavailable",
            "core.remote.ambiguous", "core.remote.local_only", "core.remote.stale",
            "core.remote.target_unavailable", "core.prompt.mode_invalid",
            "core.prompt.input_required", "core.prompt.input_unknown",
            "core.prompt.input_conflict", "core.prompt.input_invalid",
            "core.extension.incompatible", "core.extension.activation_failed",
            "core.extension.dependency_cycle", "core.clipboard.unavailable",
        ):
            self.assertIn(code, api.ERROR_CODES, code)

    def test_there_is_one_error_type_not_a_hierarchy(self) -> None:
        subclasses = api.OrchestratorError.__subclasses__()
        self.assertEqual(subclasses, [])

    def test_problem_is_json_safe(self) -> None:
        try:
            self.core().get_project(api.ProjectKey("absent"))
        except api.OrchestratorError as exc:
            json.dumps(exc.problem.to_dict())
        else:  # pragma: no cover
            self.fail("expected a problem")

    def test_problem_retryable_is_structured_advisory_data(self) -> None:
        problem = api.Problem("core.context.stale", "retry", retryable=True)
        payload = problem.to_dict()
        self.assertIs(payload["retryable"], True)
        self.assertIsNone(api.Problem("core.context.stale", "unknown").to_dict()["retryable"])

    def test_no_private_object_leaks_through_public_records(self) -> None:
        """A public record must never carry a live implementation object."""

        core = self.core()
        prepared = self.prepare(core)
        rendered = core.render(
            api.PromptRenderRequest(
                prepared=prepared, prompt_execution_mode=api.PromptExecutionMode.LOCAL
            )
        )
        for record in (prepared, rendered, core.get_project(api.ProjectKey("demo"))):
            payload = record.model_dump(mode="json")
            json.dumps(payload)  # must be plain JSON data

    def test_public_modules_export_no_private_names(self) -> None:
        for module in (api, spi):
            for name in module.__all__:
                self.assertFalse(name.startswith("_"), f"{module.__name__}.{name}")
                self.assertTrue(hasattr(module, name), f"{module.__name__}.{name}")

    def test_public_signatures_do_not_mention_implementation_types(self) -> None:
        forbidden = ("subprocess", "Popen", "sqlite", "Lock", "socket", "asyncio")
        for name in dir(api.CoreAPI):
            if name.startswith("_"):
                continue
            signature = str(inspect.signature(getattr(api.CoreAPI, name)))
            for token in forbidden:
                self.assertNotIn(token, signature, f"{name}: {signature}")

    def test_pagination_uses_opaque_cursors(self) -> None:
        page = self.core().workplans(api.WorkplanQuery(project=api.ProjectKey("demo"), limit=1))
        self.assertEqual(len(page.items), 1)
        self.assertIsNotNone(page.next_cursor)
        second = self.core().workplans(
            api.WorkplanQuery(project=api.ProjectKey("demo"), limit=1, cursor=page.next_cursor)
        )
        self.assertNotEqual(second.items[0].ref.path, page.items[0].ref.path)


class StageIdentityTests(SeamBase):
    def test_stage_selector_resolves_only_through_a_compatible_profile(self) -> None:
        prepared = self.prepare(self.core())
        self.assertEqual(prepared.stage.profile_id, prepared.profile.profile_id)
        self.assertEqual(prepared.stage.protocol_version, prepared.profile.protocol_version)

    def test_stage_selector_is_a_plain_string_and_stage_ref_is_a_record(self) -> None:
        self.assertIsInstance(api.StageSelector("implementation"), str)
        self.assertTrue(hasattr(api.StageRef, "model_fields"))

    def test_unknown_stage_is_rejected(self) -> None:
        with self.assertRaises(api.OrchestratorError) as caught:
            self.prepare(self.core(), stage="deploy")
        self.assertEqual(caught.exception.code, E.STAGE_UNKNOWN)


class WorkplanOwnershipTests(SeamBase):
    def test_resolve_workplan_is_the_public_selection_owner(self) -> None:
        core = self.core()
        stage = core.list_stages(api.WorkflowRequest(project=api.ProjectKey("demo")))[2].stage
        resolution = core.resolve_workplan(
            api.WorkplanResolutionRequest(
                project=api.ProjectKey("demo"), stage=stage, branch="main"
            )
        )
        self.assertEqual(resolution.workplan.workplan_id, "WP")
        self.assertTrue(resolution.selection_basis)
        self.assertIn("workplans/active/WP.md", resolution.considered)

    def test_workflow_follows_the_governing_workplan_protocol(self) -> None:
        """A governing plan on an unsupported protocol fails; it is never coerced to 5.16."""

        core = self.core()
        old = next(
            item.ref
            for item in core.workplans(api.WorkplanQuery(project=api.ProjectKey("demo"))).items
            if item.ref.workplan_id == "OLD"
        )
        with self.assertRaises(api.OrchestratorError) as caught:
            core.workflow(api.WorkflowRequest(project=api.ProjectKey("demo"), workplan=old))
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_governing_workplan_without_protocol_version_fails_for_required_stages(self) -> None:
        write_workplan(
            self.repo, "workplans/active/NOVER.md", workplan_id="NOVER", protocol_version=None,
        )
        commit_all(self.repo, "no version")
        with self.assertRaises(api.OrchestratorError) as caught:
            self.prepare(self.core(), workplan_selector="NOVER")
        self.assertEqual(caught.exception.code, E.PROTOCOL_UNAVAILABLE)

    def test_governing_workplan_precedes_an_explicit_profile(self) -> None:
        core = self.core()
        old = next(
            item.ref
            for item in core.workplans(api.WorkplanQuery(project=api.ProjectKey("demo"))).items
            if item.ref.workplan_id == "OLD"
        )
        profile = core.workflow(api.WorkflowRequest(project=api.ProjectKey("demo"))).profile
        with self.assertRaises(api.OrchestratorError) as caught:
            core.workflow(api.WorkflowRequest(workplan=old, profile=profile))
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_explicit_profile_identity_fields_are_not_silently_rewritten(self) -> None:
        core = self.core()
        profile = core.workflow(api.WorkflowRequest(project=api.ProjectKey("demo"))).profile
        mismatched = profile.model_copy(update={"profile_schema_version": 99})
        with self.assertRaises(api.OrchestratorError) as caught:
            core.workflow(api.WorkflowRequest(profile=mismatched))
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_explicit_only_stage_tolerates_incomplete_protocol_metadata(self) -> None:
        """An optional authority is evidence; it does not decide the governing contract."""

        write_workplan(
            self.repo, "workplans/active/NOVER.md", workplan_id="NOVER", protocol_version=None,
        )
        commit_all(self.repo, "no version")
        prepared = self.prepare(
            self.core(), stage="verification", workplan_selector="NOVER",
            input_overrides=(("VERIFICATION_SCOPE", "scope"),),
        )
        self.assertEqual(prepared.workplan_resolution.workplan.workplan_id, "NOVER")
        self.assertEqual(prepared.profile.protocol_version, "5.16.0")

    def test_explicit_only_stage_rejects_an_explicit_unsupported_protocol_version(self) -> None:
        write_workplan(
            self.repo,
            "workplans/active/OLD_ACTIVE.md",
            workplan_id="OLD_ACTIVE",
            protocol_version="5.9.0",
        )
        commit_all(self.repo, "unsupported optional authority")
        with self.assertRaises(api.OrchestratorError) as caught:
            self.prepare(
                self.core(),
                stage="verification",
                workplan_selector="OLD_ACTIVE",
                input_overrides=(("VERIFICATION_SCOPE", "scope"),),
            )
        self.assertEqual(caught.exception.code, E.PROTOCOL_INCOMPATIBLE)

    def test_list_stages_is_a_view_of_the_same_descriptor(self) -> None:
        core = self.core()
        request = api.WorkflowRequest(project=api.ProjectKey("demo"))
        self.assertEqual(core.list_stages(request), core.workflow(request).stages)


class AdapterShapedSeamTests(SeamBase):
    """A route is admitted between the phases, exactly as WP-3 will do it."""

    def test_external_admission_sees_a_complete_preparation_and_no_prompt(self) -> None:
        application = self.app()
        core = application.core()
        received: list[object] = []
        application.events().subscribe(
            (api.PROMPT_RENDERED_EVENT,), received.append, "seam.sink"
        )

        prepared = self.prepare(core)

        # No prompt artifact and no event may exist yet.
        self.assertFalse(hasattr(prepared, "prompt_text"))
        self.assertEqual(received, [])

        def admit(candidate: api.PreparedPrompt) -> api.PromptExecutionMode:
            """A no-op admission using only public preparation records."""

            assert candidate.stage.stage_key == "implementation"
            assert candidate.workplan_resolution.workplan is not None
            assert candidate.profile.protocol_version == "5.16.0"
            assert candidate.preparation_fingerprint.canonicalization_scheme == (
                "sdp.prompt-preparation.v1"
            )
            assert candidate.observation.candidate.head_commit
            return api.PromptExecutionMode.LOCAL

        rendered = core.render(
            api.PromptRenderRequest(prepared=prepared, prompt_execution_mode=admit(prepared))
        )
        self.assertTrue(rendered.prompt_text)
        self.assertEqual(len(received), 1)

    def test_one_preparation_can_render_either_mode_subject_to_feasibility(self) -> None:
        core = self.core()
        prepared = self.prepare(core)
        local = core.render(
            api.PromptRenderRequest(
                prepared=prepared, prompt_execution_mode=api.PromptExecutionMode.LOCAL
            )
        )
        self.assertEqual(local.preparation_fingerprint, prepared.preparation_fingerprint)
        with self.assertRaises(api.OrchestratorError):
            # No remote evidence was gathered, so web mode refuses truthfully.
            core.render(
                api.PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=api.PromptExecutionMode.WEB
                )
            )

    def test_preparation_carries_no_prompt_execution_mode(self) -> None:
        self.assertNotIn("prompt_execution_mode", api.PromptPreparationRequest.model_fields)
        self.assertIn("prompt_execution_mode", api.PromptRenderRequest.model_fields)

    def test_prepared_prompt_survives_serialization_across_a_process_boundary(self) -> None:
        core = self.core()
        prepared = self.prepare(core)
        wire = json.dumps(prepared.model_dump(mode="json"))
        restored = api.PreparedPrompt(**json.loads(wire))
        rendered = core.render(
            api.PromptRenderRequest(
                prepared=restored, prompt_execution_mode=api.PromptExecutionMode.LOCAL
            )
        )
        self.assertTrue(rendered.prompt_text)


if __name__ == "__main__":
    unittest.main()
