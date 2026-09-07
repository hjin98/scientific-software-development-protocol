"""O7 -- canonical input classification, ownership enforcement, and safe encoding.

This suite exercises every canonical stage and every declared INPUT line, and it
pins the naming separation the architecture insists on: the Core prompt mode
(``local``/``web``) and the canonical ``EXECUTION_MODE`` input are independent.
"""

from __future__ import annotations

import unittest

from sdp_orchestrator.core import _errors as E
from sdp_orchestrator.core import _profile as P
from sdp_orchestrator.core._canonical import CANONICAL_STAGES, parse_document
from sdp_orchestrator.core._inputs import (
    decode_scalar,
    encode_scalar,
    normalize_overrides,
    resolve_inputs,
)
from sdp_orchestrator.core._limits import MAX_INPUT_VALUE_BYTES
from sdp_orchestrator.core._records import (
    DigestRef,
    InputOwnership,
    LifecycleState,
    WorkplanRef,
)

from ._support import CANONICAL_PROMPTS

DESCRIPTOR = P.build_profile(parse_document(CANONICAL_PROMPTS.read_text(encoding="utf-8"))).descriptor

WORKPLAN = WorkplanRef(
    workplan_id="WP-TEST",
    protocol_version="5.16.0",
    path="workplans/active/WP-TEST.md",
    artifact_digest=DigestRef(algorithm="sha256", value="a" * 64),
    semantic_digest=DigestRef(algorithm="sha256", value="b" * 64),
    semantic_identity_complete=True,
    lifecycle_state=LifecycleState.ACTIVE,
)

#: The required user input for each stage, per the frozen workplan table.
REQUIRED_USER = {
    "baseline": {"BASELINE_SCOPE"},
    "design": {"TASK"},
    "implementation": set(),
    "review": set(),
    "verification": {"VERIFICATION_SCOPE"},
    "stabilization": {"STABILIZATION_SCOPE"},
    "alignment": {"UPSTREAM_ACCEPTED_WORK"},
    "health-audit": {"AUDIT_SCOPE"},
    "closeout": {"COMPLETED_WORK"},
}


def stage(key: str):
    return P.stage_descriptor(DESCRIPTOR, P.resolve_stage_key(DESCRIPTOR, key))


def resolve(key: str, *, workplan=WORKPLAN, first_task=None, overrides=None, version="5.16.0"):
    return resolve_inputs(
        stage(key),
        workplan=workplan,
        first_task=first_task,
        overrides=dict(overrides or {}),
        governing_protocol_version=version,
    )


def defaults_for(key: str) -> dict[str, str]:
    """Minimum inputs that make ``key`` renderable."""

    overrides = {name: "supplied scope" for name in REQUIRED_USER[key] if name != "TASK"}
    return overrides


class ClassificationTests(unittest.TestCase):
    def test_every_canonical_input_is_classified(self) -> None:
        document = parse_document(CANONICAL_PROMPTS.read_text(encoding="utf-8"))
        for _, key, _ in CANONICAL_STAGES:
            declared = {binding.name for binding in stage(key).inputs}
            self.assertEqual(declared, set(document.stages[key].input_names), key)

    def test_required_user_table_matches_the_frozen_contract(self) -> None:
        for _, key, _ in CANONICAL_STAGES:
            actual = {
                binding.name
                for binding in stage(key).inputs
                if binding.ownership is InputOwnership.REQUIRED_USER
            }
            self.assertEqual(actual, REQUIRED_USER[key], key)

    def test_repository_targets_are_mode_dependent_and_unvalued_in_preparation(self) -> None:
        for _, key, _ in CANONICAL_STAGES:
            for item in resolve(
                key, first_task="t" if key == "design" else None, overrides=defaults_for(key)
            ):
                if item.name in {"REPOSITORY_TARGET", "IMPLEMENTATION_TARGET"}:
                    self.assertTrue(item.mode_dependent, key)
                    self.assertIsNone(item.value, key)

    def test_canonical_defaults_are_applied(self) -> None:
        values = {i.name: i.value for i in resolve("implementation")}
        self.assertEqual(values["PROTOCOL_SOURCE"], "AUTO_LOCAL_FIRST")
        self.assertEqual(values["EXECUTION_MODE"], "AUTO_EXECUTE")
        self.assertEqual(values["ADDITIONAL_CONSTRAINTS"], "NONE")

    def test_auto_and_none_sentinels_stay_canonical(self) -> None:
        values = {i.name: i.value for i in resolve("health-audit", overrides={"AUDIT_SCOPE": "repo"})}
        self.assertEqual(values["HISTORY_WINDOW"], "AUTO")
        self.assertEqual(values["GOVERNING_ARCHITECTURE"], "AUTO")
        self.assertEqual(values["EXCLUSIONS"], "NONE")

    def test_protocol_ref_follows_the_governing_contract(self) -> None:
        values = {i.name: i.value for i in resolve("implementation", version="5.16.0")}
        self.assertEqual(values["PROTOCOL_REF"], "5.16.0")

    def test_workplan_input_is_bound_mechanically_from_the_resolver(self) -> None:
        self.assertEqual(
            {i.name: i.value for i in resolve("implementation")}["WORKPLAN"], WORKPLAN.path
        )
        self.assertEqual(
            {i.name: i.value for i in resolve("alignment", overrides={"UPSTREAM_ACCEPTED_WORK": "u"})}[
                "DOWNSTREAM_WORKPLAN"
            ],
            WORKPLAN.path,
        )

    def test_closeout_completed_work_may_come_from_an_exact_workplan(self) -> None:
        values = {i.name: i.value for i in resolve("closeout")}
        self.assertEqual(values["COMPLETED_WORK"], WORKPLAN.workplan_id)

    def test_closeout_requires_completed_work_without_a_workplan(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("closeout", workplan=None)
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_REQUIRED)

    def test_no_successful_resolution_leaves_a_placeholder(self) -> None:
        for _, key, _ in CANONICAL_STAGES:
            for item in resolve(
                key, first_task="t" if key == "design" else None, overrides=defaults_for(key)
            ):
                if item.value is not None:
                    self.assertNotIn("[", item.value, f"{key}:{item.name}")


class OwnershipEnforcementTests(unittest.TestCase):
    def test_unknown_input_is_rejected(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("implementation", overrides={"NOT_AN_INPUT": "x"})
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_UNKNOWN)

    def test_input_declared_by_another_stage_is_unknown_here(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("implementation", overrides={"AUDIT_SCOPE": "x"})
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_UNKNOWN)

    def test_mechanical_bindings_cannot_be_overridden(self) -> None:
        for name in ("PROTOCOL_REF", "REPOSITORY_TARGET", "WORKPLAN"):
            with self.assertRaises(E.OrchestratorError) as caught:
                resolve("implementation", overrides={name: "x"})
            self.assertEqual(caught.exception.code, E.PROMPT_INPUT_CONFLICT, name)

    def test_task_cannot_be_set_through_a_generic_override(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("design", overrides={"TASK": "x"})
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_CONFLICT)

    def test_task_outside_design_is_a_conflict(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("implementation", first_task="something")
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_CONFLICT)

    def test_missing_required_user_input_fails_atomically(self) -> None:
        for key, required in REQUIRED_USER.items():
            if not required or key in {"design", "closeout"}:
                continue
            with self.assertRaises(E.OrchestratorError) as caught:
                resolve(key)
            self.assertEqual(caught.exception.code, E.PROMPT_INPUT_REQUIRED, key)

    def test_empty_override_value_is_invalid(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("verification", overrides={"VERIFICATION_SCOPE": "   "})
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_INVALID)

    def test_oversized_value_is_invalid(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            resolve("verification", overrides={"VERIFICATION_SCOPE": "x" * (MAX_INPUT_VALUE_BYTES + 1)})
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_INVALID)

    def test_malformed_input_name_is_invalid(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            normalize_overrides((("lower case", "x"),))
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_INVALID)

    def test_repeated_conflicting_override_is_a_conflict(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            normalize_overrides((("AUDIT_SCOPE", "a"), ("AUDIT_SCOPE", "b")))
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_CONFLICT)

    def test_too_many_overrides_are_rejected(self) -> None:
        from sdp_orchestrator.core._limits import MAX_INPUT_OVERRIDES

        pairs = tuple((f"NAME_{i}", "v") for i in range(MAX_INPUT_OVERRIDES + 1))
        with self.assertRaises(E.OrchestratorError) as caught:
            normalize_overrides(pairs)
        self.assertEqual(caught.exception.code, E.PROMPT_INPUT_INVALID)


class NamingSeparationTests(unittest.TestCase):
    """Prompt mode and canonical EXECUTION_MODE are independent knobs."""

    def test_execution_mode_override_is_accepted(self) -> None:
        values = {
            i.name: i.value
            for i in resolve("implementation", overrides={"EXECUTION_MODE": "REPORT_ONLY"})
        }
        self.assertEqual(values["EXECUTION_MODE"], "REPORT_ONLY")

    def test_execution_mode_is_not_a_prompt_mode_value(self) -> None:
        from sdp_orchestrator.core._records import PromptExecutionMode

        self.assertEqual({m.value for m in PromptExecutionMode}, {"local", "web"})
        self.assertNotIn("AUTO_EXECUTE", {m.value for m in PromptExecutionMode})

    def test_protocol_source_default_is_agent_facing_not_a_render_path(self) -> None:
        binding = next(b for b in stage("implementation").inputs if b.name == "PROTOCOL_SOURCE")
        self.assertEqual(binding.default_value, "AUTO_LOCAL_FIRST")
        self.assertTrue(binding.override_allowed)


class ScalarEncodingTests(unittest.TestCase):
    def test_newlines_cannot_break_the_input_grammar(self) -> None:
        encoded = encode_scalar("first\nEXECUTION_MODE = REPORT_ONLY")
        self.assertNotIn("\n", encoded)
        self.assertEqual(decode_scalar(encoded), "first\nEXECUTION_MODE = REPORT_ONLY")

    def test_nul_and_carriage_return_are_escaped(self) -> None:
        encoded = encode_scalar("a\x00b\rc")
        self.assertNotIn("\x00", encoded)
        self.assertNotIn("\r", encoded)
        self.assertEqual(decode_scalar(encoded), "a\x00b\rc")

    def test_canonical_sentinels_pass_through_unchanged(self) -> None:
        for sentinel in ("AUTO", "NONE", "AUTO_EXECUTE", "AUTO_LOCAL_FIRST", "REPORT_ONLY"):
            self.assertEqual(encode_scalar(sentinel), sentinel)

    def test_ordinary_text_including_unicode_is_unchanged(self) -> None:
        for text in ("a simple task", "chemin/à/tester", "数値解析", "a = b; c[0]"):
            self.assertEqual(encode_scalar(text), text)

    def test_backslash_is_escaped_reversibly(self) -> None:
        self.assertEqual(encode_scalar("a\\nb"), "a\\\\nb")
        self.assertEqual(decode_scalar(encode_scalar("a\\nb")), "a\\nb")


try:  # pragma: no cover - the property test is skipped when hypothesis is absent
    from hypothesis import given, settings
    from hypothesis import strategies as st
except ImportError:  # pragma: no cover
    HYPOTHESIS = False
else:
    HYPOTHESIS = True


@unittest.skipUnless(HYPOTHESIS, "hypothesis is not installed")
class ScalarEncodingPropertyTests(unittest.TestCase):
    """The encoding must be single-line and reversible for *arbitrary* input.

    Example-based tests can only cover the control characters someone thought of.
    The safety claim here is universal, so it is stated as a property.
    """

    @settings(max_examples=400, deadline=None)
    @given(st.text(max_size=512))
    def test_encoding_is_single_line_and_reversible(self, value: str) -> None:
        encoded = encode_scalar(value)
        self.assertNotIn("\n", encoded)
        self.assertNotIn("\r", encoded)
        self.assertNotIn("\x00", encoded)
        self.assertEqual(decode_scalar(encoded), value)

    @settings(max_examples=200, deadline=None)
    @given(st.text(max_size=256), st.text(max_size=256))
    def test_distinct_values_encode_distinctly(self, left: str, right: str) -> None:
        if left != right:
            self.assertNotEqual(encode_scalar(left), encode_scalar(right))


if __name__ == "__main__":
    unittest.main()
