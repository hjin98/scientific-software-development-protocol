from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "source/shared/references/development-workflow-prompts.md"


class Protocol516OrchestrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prompt = PROMPT.read_text(encoding="utf-8")
        self.lower = self.prompt.lower()

    def stage_block(self, heading: str) -> str:
        marker = f"## {heading}"
        pos = self.prompt.index(marker)
        next_pos = self.prompt.find("\n## ", pos + len(marker))
        return self.prompt[pos:] if next_pos < 0 else self.prompt[pos:next_pos]

    def assert_portable_resolution_contract(self, block: str) -> None:
        lower = block.lower()
        self.assertIn("exposed", lower)
        self.assertIn("installed-skill root", lower)
        self.assertIn("https://github.com/hjin98/software-development-protocol", block)
        self.assertIn("not shell commands", lower)
        self.assertIn("truthful non-closure", lower)
        self.assertIn("do not claim protocol execution from memory", lower)
        self.assertIn("do not silently substitute a different protocol version", lower)

    def test_prompt_reference_has_parameterized_stage_entrypoints(self) -> None:
        for stage in (
            "0. Baseline / Change-Health Intake",
            "1. Design / Workplan",
            "2. Implementation",
            "3. Review & Update",
            "4. Verification",
            "5. Stabilization / Architecture GC",
            "6. Alignment of a Downstream Workplan",
            "7. Health Audit",
            "8. Closeout",
        ):
            self.assertIn(stage.lower(), self.lower)
        self.assertGreaterEqual(self.prompt.count("INPUTS"), 9)
        self.assertIn("AUTO_LOCAL_FIRST", self.prompt)
        self.assertIn("PROTOCOL_REF", self.prompt)

    def test_baseline_is_user_discoverable_and_conditional(self) -> None:
        block = self.stage_block("0. Baseline / Change-Health Intake").lower()
        self.assertIn("substantial or structurally risky", block)
        self.assertIn("not a mandatory per-change gate", block)
        self.assertIn("task-local evidence", block)
        self.assertIn("do not create a permanent health ledger", block)
        lifecycle = self.prompt[self.prompt.index("For substantial work"): self.prompt.index("Testing, verification")].lower()
        self.assertIn("baseline / change-health intake when material", lifecycle)
        design = self.stage_block("1. Design / Workplan").lower()
        self.assertIn("if task is substantial or structurally risky and no useful baseline was supplied", design)

    def test_every_copied_stage_preserves_portable_resolution_terminal(self) -> None:
        for heading in (
            "0. Baseline / Change-Health Intake",
            "1. Design / Workplan",
            "2. Implementation",
            "3. Review & Update",
            "4. Verification",
            "5. Stabilization / Architecture GC",
            "6. Alignment of a Downstream Workplan",
            "7. Health Audit",
            "8. Closeout",
        ):
            self.assert_portable_resolution_contract(self.stage_block(heading))

    def test_local_first_public_fallback_is_explicit(self) -> None:
        self.assertIn("local first, public repository second", self.lower)
        self.assertIn("documented exposed installed-skill root", self.lower)
        self.assertIn("source/roles/<skill-name>/skill.md", self.lower)
        self.assertIn("source/specialists/<skill-name>/skill.md", self.lower)
        self.assertIn("do not guess that a semantic version is a git ref", self.lower)

    def test_stage_skill_routes_are_correct(self) -> None:
        expected = {
            "0. Baseline / Change-Health Intake": "software-design",
            "1. Design / Workplan": "software-design",
            "2. Implementation": "software-implementation",
            "3. Review & Update": "software-design",
            "4. Verification": "software-design",
            "5. Stabilization / Architecture GC": "software-design",
            "6. Alignment of a Downstream Workplan": "software-design",
            "7. Health Audit": "software-maintenance-audit",
            "8. Closeout": "software-documentation",
        }
        for heading, skill in expected.items():
            self.assertIn(skill, self.stage_block(heading).lower(), heading)

    def test_health_audit_routing_preserves_authority(self) -> None:
        block = self.stage_block("7. Health Audit").lower()
        self.assertIn("local tier-2 repair/simplification under already-sufficient existing authority", block)
        self.assertIn("substantial maintenance that needs a new or revised workplan/implementation contract", block)
        self.assertIn("software-design` first", block)
        self.assertIn("frozen-architecture concern -> `software-design`", block)
        self.assertNotIn("tier-2 simplification candidate -> bounded workplan and `software-implementation`", block)

    def test_review_verification_stabilization_health_are_not_collapsed(self) -> None:
        review = self.stage_block("3. Review & Update").lower()
        verify = self.stage_block("4. Verification").lower()
        stabilize = self.stage_block("5. Stabilization / Architecture GC").lower()
        health = self.stage_block("7. Health Audit").lower()
        self.assertIn("independent implementation-review mode", review)
        self.assertIn("adversarial-verification mode", verify)
        self.assertIn("stabilization is non-mutating", stabilize)
        self.assertIn("periodic long-horizon repository audit", health)
        self.assertIn("not a feature review or approval gate", health)

    def test_no_source_means_truthful_nonclosure_in_each_stage(self) -> None:
        for heading in (
            "0. Baseline / Change-Health Intake",
            "1. Design / Workplan",
            "2. Implementation",
            "3. Review & Update",
            "4. Verification",
            "5. Stabilization / Architecture GC",
            "6. Alignment of a Downstream Workplan",
            "7. Health Audit",
            "8. Closeout",
        ):
            lower = self.stage_block(heading).lower()
            self.assertIn("truthful non-closure", lower, heading)
            self.assertIn("do not claim protocol execution from memory", lower, heading)


if __name__ == "__main__":
    unittest.main()
