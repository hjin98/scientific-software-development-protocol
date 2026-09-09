"""Protocol 6 profile/schema routing and Protocol 5.16 coexistence."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from sdp_orchestrator.core import profile as P
from sdp_orchestrator.core import protocol_source as PS
from sdp_orchestrator.core.canonical import CANONICAL_STAGES, SSDP6_STAGES, parse_document
from sdp_orchestrator.core.records import WorkplanPolicy

from ._support import CURRENT_CANONICAL_PROMPTS, REPO_ROOT


class SSDP6CanonicalProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        text = CURRENT_CANONICAL_PROMPTS.read_text(encoding="utf-8")
        cls.document = parse_document(text, profile_id=P.DEFAULT_PROFILE_ID)
        cls.snapshot = P.build_profile(cls.document, P.DEFAULT_PROFILE_ID)
        cls.descriptor = cls.snapshot.descriptor

    def test_current_profile_is_schema_v2_protocol_6(self) -> None:
        self.assertEqual(P.DEFAULT_PROFILE_ID, "ssdp-protocol-6.0")
        self.assertEqual(self.descriptor.profile.profile_id, P.DEFAULT_PROFILE_ID)
        self.assertEqual(self.descriptor.profile.protocol_version, "6.0.0")
        self.assertEqual(self.descriptor.profile.profile_schema_version, 2)
        self.assertEqual(self.descriptor.schema_version, 2)

    def test_current_canonical_source_has_exact_domain_stage_set(self) -> None:
        self.assertEqual(
            [stage.stage.stage_key for stage in self.descriptor.stages],
            [key for _, key, _ in SSDP6_STAGES],
        )
        self.assertEqual(len(self.descriptor.stages), 11)

    def test_profile_version_mapping_is_unambiguous(self) -> None:
        self.assertEqual(P.profile_id_for_version("5.16.0"), P.PROFILE_ID)
        self.assertEqual(P.profile_id_for_version("5.16"), P.PROFILE_ID)
        self.assertEqual(P.profile_id_for_version("6.0.0"), P.DEFAULT_PROFILE_ID)
        self.assertEqual(P.profile_id_for_version("6.0"), P.DEFAULT_PROFILE_ID)

    def test_every_current_input_is_classified(self) -> None:
        for stage in self.descriptor.stages:
            declared = {binding.name for binding in stage.inputs}
            self.assertEqual(declared, set(self.document.stages[stage.stage.stage_key].input_names))

    def test_current_profile_uses_protocol6_native_parent_authority_input(self) -> None:
        by_key = {stage.stage.stage_key: stage for stage in self.descriptor.stages}
        alignment_inputs = {item.name for item in by_key["alignment"].inputs}
        self.assertIn("GOVERNING_AUTHORITY", alignment_inputs)
        self.assertNotIn("FROZEN_PARENT_AUTHORITY", alignment_inputs)

    def test_task_is_not_re_requested_by_downstream_governed_stages(self) -> None:
        by_key = {stage.stage.stage_key: stage for stage in self.descriptor.stages}
        for key in ("software-implementation", "review", "verification", "stabilization", "alignment", "health-audit", "closeout"):
            self.assertNotIn("TASK", {item.name for item in by_key[key].inputs}, key)
        for key in ("intake", "scientific-formulation", "numerical-algorithm-design", "software-design"):
            self.assertIn("TASK", {item.name for item in by_key[key].inputs}, key)

    def test_implementation_and_review_require_governing_workplan(self) -> None:
        policies = {stage.stage.stage_key: stage.workplan_policy for stage in self.descriptor.stages}
        self.assertIs(policies["software-implementation"], WorkplanPolicy.REQUIRED)
        self.assertIs(policies["review"], WorkplanPolicy.REQUIRED)

    def test_reduced_routes_skip_unaffected_intermediate_domains(self) -> None:
        def destinations(stage_key: str, trigger: str) -> set[str]:
            return {
                t.to_stage.stage_key
                for t in self.descriptor.transitions
                if t.from_stage.stage_key == stage_key
                and t.trigger_key == trigger
                and t.to_stage is not None
            }

        self.assertIn("software-implementation", destinations("numerical-algorithm-design", "accepted"))
        self.assertIn("software-design", destinations("scientific-formulation", "accepted"))
        self.assertIn("software-implementation", destinations("scientific-formulation", "accepted"))

    def test_alignment_pass_routes_by_downstream_domain_owner(self) -> None:
        destinations = {
            t.to_stage.stage_key
            for t in self.descriptor.transitions
            if t.from_stage.stage_key == "alignment"
            and t.trigger_key == "pass"
            and t.to_stage is not None
        }
        self.assertEqual(
            destinations,
            {"numerical-algorithm-design", "software-design", "software-implementation"},
        )

    def test_serious_challenge_stops_automatic_routing(self) -> None:
        for stage_key in ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation", "review", "verification", "stabilization", "alignment", "health-audit", "closeout"):
            matches = [t for t in self.descriptor.transitions if t.from_stage.stage_key == stage_key and t.trigger_key == "serious_challenge"]
            self.assertTrue(matches, stage_key)
            self.assertTrue(all(t.terminal and t.to_stage is None for t in matches), stage_key)

    def test_every_transition_trigger_is_recognized(self) -> None:
        outcomes = {stage.stage.stage_key: set(stage.recognized_outcomes) for stage in self.descriptor.stages}
        for transition in self.descriptor.transitions:
            self.assertIn(transition.trigger_key, outcomes[transition.from_stage.stage_key])

    def test_profile_json_round_trips(self) -> None:
        self.assertEqual(P.profile_from_json(P.profile_to_json(self.descriptor)), self.descriptor)


class FrozenLegacyProfileTests(unittest.TestCase):
    def test_legacy_definition_stays_schema_v1_with_nine_stages(self) -> None:
        legacy = PS.resolve_packaged(P.PROFILE_ID).snapshot.descriptor
        self.assertEqual(legacy.profile.profile_id, "sdp-protocol-5.16")
        self.assertEqual(legacy.profile.protocol_version, "5.16.0")
        self.assertEqual(legacy.profile.profile_schema_version, 1)
        self.assertEqual(legacy.schema_version, 1)
        self.assertEqual([s.stage.stage_key for s in legacy.stages], [key for _, key, _ in CANONICAL_STAGES])

    def test_legacy_packaged_bytes_keep_pre_transition_git_blob_identity(self) -> None:
        import hashlib

        root = REPO_ROOT / "orchestrator/src/sdp_orchestrator/core/resources/protocol/sdp-protocol-5.16"
        expected = {
            "prompts.md": "3730b06393843e9c24406a324f981ab4481858da",
            "profile.json": "b3d4257fcd18af7bdb1799b2db742659bb2403fc",
        }
        for name, sha in expected.items():
            data = (root / name).read_bytes()
            actual = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324
            self.assertEqual(actual, sha, name)

    def test_legacy_alignment_retains_frozen_parent_input(self) -> None:
        legacy = PS.resolve_packaged(P.PROFILE_ID).snapshot.descriptor
        by_key = {stage.stage.stage_key: stage for stage in legacy.stages}
        alignment_inputs = {item.name for item in by_key["alignment"].inputs}
        self.assertIn("FROZEN_PARENT_AUTHORITY", alignment_inputs)

    def test_legacy_profile_is_still_derived_from_legacy_prompts(self) -> None:
        root = REPO_ROOT / "orchestrator/src/sdp_orchestrator/core/resources/protocol/sdp-protocol-5.16"
        text = (root / "prompts.md").read_text(encoding="utf-8")
        document = parse_document(text, profile_id=P.PROFILE_ID)
        expected = P.profile_to_json(P.build_profile(document, P.PROFILE_ID).descriptor)
        self.assertEqual((root / "profile.json").read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
