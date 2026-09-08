"""O8 -- renderer, prompt/preparation fingerprints, result footer, and events.

The event assertions matter as much as the byte assertions: an event carrying the
complete prompt must reach only sinks that explicitly asked for it, and only
after a fully constructed artifact exists.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import errors as E
from sdp_orchestrator.core import render as R
from sdp_orchestrator.core.application import create_application
from sdp_orchestrator.core.canonical import CANONICAL_STAGES
from sdp_orchestrator.core.events import PROMPT_RENDERED_EVENT, logical_event_id
from sdp_orchestrator.core.records import (
    ApplicationRequest,
    EventEnvelope,
    ObservationPolicy,
    ProjectKey,
    PromptExecutionMode,
    PromptPreparationRequest,
    PromptRenderRequest,
    RemoteMode,
    StageResultEnvelope,
    StageSelector,
)
from sdp_orchestrator.core.service import preparation_fingerprint
from pydantic import ValidationError

from ._support import commit_all, config_text, git, init_repo, write_workplan

REQUIRED_INPUT = {
    "baseline": [("BASELINE_SCOPE", "the storage subsystem")],
    "design": [],
    "implementation": [],
    "review": [],
    "verification": [("VERIFICATION_SCOPE", "the release claims")],
    "stabilization": [("STABILIZATION_SCOPE", "the migration")],
    "alignment": [("UPSTREAM_ACCEPTED_WORK", "WP-0")],
    "health-audit": [("AUDIT_SCOPE", "the repository")],
    "closeout": [],
}


class RenderBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")
        write_workplan(
            self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main"
        )
        commit_all(self.repo, "add workplan")
        self.config = self.root / "config.toml"
        self.config.write_text(config_text(self.repo), encoding="utf-8")

    def core(self):
        return create_application(ApplicationRequest(config_path=str(self.config)))

    def application(self):
        return create_application(ApplicationRequest(config_path=str(self.config)))

    def prepare(self, stage: str, *, app=None, **kwargs):
        application = app or self.application()
        overrides = tuple(REQUIRED_INPUT[stage]) + tuple(kwargs.pop("overrides", ()))
        return application.core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector(stage),
                workplan_selector=kwargs.pop(
                    "workplan_selector",
                    "WP" if stage in {"alignment", "closeout"} else None,
                ),
                first_task=kwargs.pop("first_task", "do the thing" if stage == "design" else None),
                input_overrides=overrides,
                policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
                **kwargs,
            )
        )

    def render(self, stage: str, *, mode=PromptExecutionMode.LOCAL, app=None, **kwargs):
        application = app or self.application()
        prepared = self.prepare(stage, app=application, **kwargs)
        return application.core().render(
            PromptRenderRequest(prepared=prepared, prompt_execution_mode=mode)
        )


class BodyFidelityTests(RenderBase):
    def test_every_stage_renders_its_own_canonical_body(self) -> None:
        seen: dict[str, str] = {}
        for _, key, title in CANONICAL_STAGES:
            rendered = self.render(key)
            self.assertIn("INPUTS", rendered.prompt_text)
            seen[key] = rendered.prompt_text
        self.assertEqual(len(set(seen.values())), len(seen), "stages must not share a body")

    def test_only_declared_input_lines_are_substituted(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        source_body = application.core()._protocol_source(  # noqa: SLF001 - white-box body check
            prepared.profile.profile_id
        ).snapshot.bodies["implementation"]
        rendered = application.core().render(
            PromptRenderRequest(prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL)
        )
        body_lines = source_body.splitlines()
        prompt_lines = rendered.prompt_text.splitlines()
        declared = {b.name for b in prepared.workflow.stages[0].inputs} | {
            i.name for i in prepared.inputs
        }
        for index, original in enumerate(body_lines):
            if original.split("=", 1)[0].strip() in declared and "=" in original:
                continue
            self.assertEqual(prompt_lines[index], original, f"line {index} must be preserved")

    def test_no_hidden_reasoning_is_requested(self) -> None:
        text = self.render("implementation").prompt_text.lower()
        for phrase in ("chain of thought", "chain-of-thought", "internal reasoning", "scratchpad"):
            self.assertNotIn(phrase, text)
        self.assertIn("do not reveal hidden reasoning", text)

    def test_footer_is_appended_after_the_canonical_body(self) -> None:
        text = self.render("implementation").prompt_text
        self.assertLess(text.index("INPUTS"), text.index(R.FOOTER_BEGIN))

    def test_artifact_ends_with_exactly_one_trailing_newline(self) -> None:
        text = self.render("implementation").prompt_text
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))
        self.assertNotIn("\r", text)


class FingerprintTests(RenderBase):
    def test_same_semantic_state_and_run_id_gives_byte_identical_output(self) -> None:
        first = self.prepare("implementation")
        application = self.application()
        second = application.core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector("implementation"),
                run_id=first.run_id,
                policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
            )
        )
        self.assertEqual(first.preparation_fingerprint, second.preparation_fingerprint)
        a = self.application().core().render(
            PromptRenderRequest(prepared=first, prompt_execution_mode=PromptExecutionMode.LOCAL)
        )
        b = application.core().render(
            PromptRenderRequest(prepared=second, prompt_execution_mode=PromptExecutionMode.LOCAL)
        )
        self.assertEqual(a.prompt_text, b.prompt_text)
        self.assertEqual(a.prompt_fingerprint, b.prompt_fingerprint)

    def test_schemes_are_versioned(self) -> None:
        rendered = self.render("implementation")
        self.assertEqual(
            rendered.preparation_fingerprint.canonicalization_scheme, "sdp.prompt-preparation.v1"
        )
        self.assertEqual(
            rendered.prompt_fingerprint.canonicalization_scheme, "sdp.prompt-fingerprint.v1"
        )

    def test_preparation_identity_is_insensitive_to_unrelated_extension_config(self) -> None:
        base = self.prepare("implementation")
        self.config.write_text(
            config_text(self.repo, extra='\n[extensions."vendor.x"]\nnoise = 42\n'),
            encoding="utf-8",
        )
        again = self.application().core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector("implementation"),
                run_id=base.run_id,
                policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
            )
        )
        self.assertEqual(base.preparation_fingerprint, again.preparation_fingerprint)

    def test_preparation_identity_is_insensitive_to_observation_timestamps(self) -> None:
        first = self.prepare("implementation")
        second = self.application().core().prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector("implementation"),
                run_id=first.run_id,
                policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
            )
        )
        self.assertNotEqual(
            first.observation.candidate.observed_at, None
        )
        self.assertEqual(first.preparation_fingerprint, second.preparation_fingerprint)

    def test_material_changes_change_the_preparation_identity(self) -> None:
        base = self.prepare("implementation")
        run = base.run_id

        def again(**kwargs):
            return self.application().core().prepare(
                PromptPreparationRequest(
                    project=ProjectKey("demo"),
                    stage=StageSelector(kwargs.pop("stage", "implementation")),
                    run_id=run,
                    policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
                    **kwargs,
                )
            )

        self.assertNotEqual(
            base.preparation_fingerprint, again(stage="review").preparation_fingerprint
        )
        self.assertNotEqual(
            base.preparation_fingerprint,
            again(input_overrides=(("EXECUTION_MODE", "REPORT_ONLY"),)).preparation_fingerprint,
        )
        # A material candidate change.
        (self.repo / "new.txt").write_text("x\n", encoding="utf-8")
        self.assertNotEqual(base.preparation_fingerprint, again().preparation_fingerprint)

        # A material workplan change.
        commit_all(self.repo, "dirty")
        write_workplan(
            self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main",
            body="changed body\n",
        )
        commit_all(self.repo, "edit workplan")
        self.assertNotEqual(base.preparation_fingerprint, again().preparation_fingerprint)

    def test_digest_metadata_is_part_of_preparation_identity(self) -> None:
        prepared = self.prepare("implementation")
        name, digest = prepared.prompt_source.content_digests[0]
        changed = digest.model_copy(update={"canonicalization_scheme": "other.scheme.v1"})
        source = prepared.prompt_source.model_copy(
            update={
                "content_digests": ((name, changed),)
                + prepared.prompt_source.content_digests[1:]
            }
        )
        tampered = prepared.model_copy(update={"prompt_source": source})
        self.assertNotEqual(
            preparation_fingerprint(prepared), preparation_fingerprint(tampered)
        )

    def test_different_run_ids_change_identity(self) -> None:
        a = self.prepare("implementation")
        b = self.prepare("implementation")
        self.assertNotEqual(a.run_id, b.run_id)
        self.assertNotEqual(a.preparation_fingerprint, b.preparation_fingerprint)

    def test_prompt_mode_changes_the_prompt_but_not_the_preparation(self) -> None:
        prepared = self.prepare("implementation")
        application = self.application()
        local = application.core().render(
            PromptRenderRequest(prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL)
        )
        self.assertEqual(local.preparation_fingerprint, prepared.preparation_fingerprint)

    def test_prepared_prompt_round_trips_through_json(self) -> None:
        from sdp_orchestrator.core.records import PreparedPrompt

        prepared = self.prepare("implementation")
        payload = prepared.model_dump(mode="json")
        restored = PreparedPrompt(**json.loads(json.dumps(payload)))
        self.assertEqual(restored, prepared)

    def test_workflow_tampering_cannot_reuse_the_old_preparation_fingerprint(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        tampered_workflow = prepared.workflow.model_copy(update={"transitions": ()})
        tampered = prepared.model_copy(update={"workflow": tampered_workflow})

        with self.assertRaises(E.OrchestratorError) as caught:
            application.core().render(
                PromptRenderRequest(
                    prepared=tampered, prompt_execution_mode=PromptExecutionMode.LOCAL
                )
            )
        self.assertEqual(caught.exception.code, E.CONTEXT_STALE)


class ResultFooterTests(RenderBase):
    def _footer(self, text: str) -> dict:
        extracted = R.extract_result_footer(text)
        self.assertIsNotNone(extracted)
        return json.loads(extracted)

    def test_footer_is_terminal_and_uniquely_marked(self) -> None:
        text = self.render("implementation").prompt_text
        self.assertEqual(text.count(R.FOOTER_BEGIN), 1)
        self.assertEqual(text.count(R.FOOTER_END), 1)

    def test_footer_template_is_valid_json_with_required_identity(self) -> None:
        rendered = self.render("implementation")
        payload = self._footer(rendered.prompt_text)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["run_id"], str(rendered.run_id))
        self.assertEqual(payload["stage"], "implementation")
        self.assertEqual(
            payload["prompt_fingerprint"], f"sha256:{rendered.prompt_fingerprint.value}"
        )

    def test_extraction_ignores_surrounding_prose(self) -> None:
        rendered = self.render("implementation")
        response = (
            "Here is my ordinary report.\n\nI ran the tests.\n\n"
            + R.FOOTER_BEGIN
            + '\n{"schema_version": 1, "run_id": "r", "prompt_fingerprint": "f",'
            ' "stage": "implementation", "outcome": "complete"}\n'
            + R.FOOTER_END
            + "\n"
        )
        payload = json.loads(R.extract_result_footer(response))
        self.assertEqual(payload["outcome"], "complete")
        del rendered

    def test_extraction_rejects_duplicate_marked_blocks(self) -> None:
        response = (
            f"{R.FOOTER_BEGIN}\n{{\"outcome\": \"earlier\"}}\n{R.FOOTER_END}\n"
            "some intervening prose\n"
            f"{R.FOOTER_BEGIN}\n{{\"outcome\": \"final\"}}\n{R.FOOTER_END}\n"
        )
        self.assertIsNone(R.extract_result_footer(response))

    def test_indented_markers_and_trailing_prose_are_not_terminal_footers(self) -> None:
        indented = f"  {R.FOOTER_BEGIN}\n{{}}\n{R.FOOTER_END}\n"
        self.assertIsNone(R.extract_result_footer(indented))
        trailing = f"{R.FOOTER_BEGIN}\n{{}}\n{R.FOOTER_END}\ntrailing prose\n"
        self.assertIsNone(R.extract_result_footer(trailing))

    def test_opaque_run_id_is_json_serialized_coherently(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        snapshot = R.build_snapshot(prepared.observation, PromptExecutionMode.LOCAL)
        run_id = 'opaque "run"\\id\n'
        source_body = application.core()._protocol_source(  # noqa: SLF001
            prepared.profile.profile_id
        ).snapshot.bodies["implementation"]
        text, _ = R.assemble(
            body=source_body,
            run_id=run_id,
            stage=prepared.stage,
            inputs=prepared.inputs,
            snapshot=snapshot,
            result_schema_id=prepared.result_schema_id,
            result_schema_version=prepared.result_schema_version,
        )
        payload = json.loads(R.extract_result_footer(text))
        self.assertEqual(payload["run_id"], run_id)

    def test_fingerprint_placeholder_in_body_is_not_rewritten(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        snapshot = R.build_snapshot(prepared.observation, PromptExecutionMode.LOCAL)
        literal = R.FINGERPRINT_PLACEHOLDER
        source_body = application.core()._protocol_source(  # noqa: SLF001
            prepared.profile.profile_id
        ).snapshot.bodies["implementation"]
        text, _ = R.assemble(
            body=source_body + f"\nLiteral placeholder: {literal}\n",
            run_id=str(prepared.run_id),
            stage=prepared.stage,
            inputs=prepared.inputs,
            snapshot=snapshot,
            result_schema_id=prepared.result_schema_id,
            result_schema_version=prepared.result_schema_version,
        )
        self.assertIn(f"Literal placeholder: {literal}", text)

    def test_absent_footer_returns_none(self) -> None:
        self.assertIsNone(R.extract_result_footer("just prose\n"))

    def test_schema_tolerates_additive_fields(self) -> None:
        envelope = StageResultEnvelope(
            schema_version=1,
            run_id="r",
            prompt_fingerprint="sha256:" + "0" * 64,
            stage="implementation",
            outcome="complete",
            future_field={"anything": True},
        )
        self.assertEqual(envelope.outcome, "complete")

    def test_additive_fields_and_timestamps_stay_wire_safe(self) -> None:
        with self.assertRaises(ValidationError):
            StageResultEnvelope(
                schema_version=1,
                run_id="r",
                prompt_fingerprint="sha256:" + "0" * 64,
                stage="implementation",
                outcome="complete",
                future_field=object(),
            )
        with self.assertRaises(ValidationError):
            EventEnvelope(
                event_id="event",
                event_type="future.event",
                schema_version=1,
                occurred_at="2026-09-08T00:00:00+02:00",
            )
        with self.assertRaises(ValidationError):
            EventEnvelope(
                event_id="event",
                event_type="future.event",
                schema_version=1,
                occurred_at="2026-09-08T00:00:00Z",
                payload={"future": object()},
            )

    def test_schema_identity_is_reported(self) -> None:
        rendered = self.render("implementation")
        self.assertEqual(rendered.result_schema_id, "sdp.stage-result-envelope")
        self.assertEqual(rendered.result_schema_version, 1)
        self.assertIn("sdp.stage-result-envelope v1", rendered.prompt_text)


class EventTests(RenderBase):
    def _subscribe(self, application, event_types):
        received = []
        application.events().subscribe(tuple(event_types), received.append, "test.sink")
        return received

    def test_successful_render_notifies_a_subscribed_sink(self) -> None:
        application = self.application()
        received = self._subscribe(application, [PROMPT_RENDERED_EVENT])
        rendered = self.render("implementation", app=application)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].payload["prompt_text"], rendered.prompt_text)
        self.assertEqual(received[0].run_id, rendered.run_id)

    def test_unsubscribed_sink_never_sees_the_prompt(self) -> None:
        application = self.application()
        received = self._subscribe(application, ["some.other.event.v1"])
        self.render("implementation", app=application)
        self.assertEqual(received, [])

    def test_failed_render_emits_no_event(self) -> None:
        application = self.application()
        received = self._subscribe(application, [PROMPT_RENDERED_EVENT])
        (self.repo / "dirty.txt").write_text("d\n", encoding="utf-8")
        with self.assertRaises(E.OrchestratorError):
            self.render("implementation", mode=PromptExecutionMode.WEB, app=application)
        self.assertEqual(received, [])

    def test_event_id_is_stable_for_the_same_run_and_prompt(self) -> None:
        first = logical_event_id(PROMPT_RENDERED_EVENT, "run-1", "abc")
        second = logical_event_id(PROMPT_RENDERED_EVENT, "run-1", "abc")
        self.assertEqual(first, second)
        self.assertNotEqual(first, logical_event_id(PROMPT_RENDERED_EVENT, "run-2", "abc"))

    def test_sink_failure_does_not_invalidate_the_primary_render(self) -> None:
        application = self.application()

        def explode(event):
            raise RuntimeError("sink is broken")

        application.events().subscribe((PROMPT_RENDERED_EVENT,), explode, "broken.sink")
        rendered = self.render("implementation", app=application)
        self.assertTrue(rendered.prompt_text)
        self.assertTrue(application.events().failures)


class StaleContextTests(RenderBase):
    def test_candidate_drift_between_phases_is_refused(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        (self.repo / "drift.txt").write_text("x\n", encoding="utf-8")
        with self.assertRaises(E.OrchestratorError) as caught:
            application.core().render(
                PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL
                )
            )
        self.assertEqual(caught.exception.code, E.CONTEXT_STALE)

    def test_staged_index_drift_between_phases_is_refused_without_event(self) -> None:
        target = self.repo / "staged.txt"
        target.write_text("base\n", encoding="utf-8")
        commit_all(self.repo, "add staged file")

        application = self.application()
        received = []
        application.events().subscribe((PROMPT_RENDERED_EVENT,), received.append, "sink")
        prepared = self.prepare("implementation", app=application)

        alternate = self.root / "alternate.txt"
        alternate.write_text("index-only\n", encoding="utf-8")
        blob = git(self.repo, "hash-object", "-w", str(alternate))
        alternate.unlink()
        git(self.repo, "update-index", "--cacheinfo", f"100644,{blob},staged.txt")

        with self.assertRaises(E.OrchestratorError) as caught:
            application.core().render(
                PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL
                )
            )
        self.assertEqual(caught.exception.code, E.CONTEXT_STALE)
        self.assertEqual(received, [])

    def test_workplan_drift_between_phases_is_refused(self) -> None:
        application = self.application()
        prepared = self.prepare("implementation", app=application)
        write_workplan(
            self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main",
            body="edited after preparation\n",
        )
        commit_all(self.repo, "edit")
        with self.assertRaises(E.OrchestratorError) as caught:
            application.core().render(
                PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL
                )
            )
        self.assertEqual(caught.exception.code, E.CONTEXT_STALE)

    def test_stale_context_emits_no_event_and_no_prompt(self) -> None:
        application = self.application()
        received = []
        application.events().subscribe((PROMPT_RENDERED_EVENT,), received.append, "sink")
        prepared = self.prepare("implementation", app=application)
        (self.repo / "drift.txt").write_text("x\n", encoding="utf-8")
        with self.assertRaises(E.OrchestratorError):
            application.core().render(
                PromptRenderRequest(
                    prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL
                )
            )
        self.assertEqual(received, [])


if __name__ == "__main__":
    unittest.main()
