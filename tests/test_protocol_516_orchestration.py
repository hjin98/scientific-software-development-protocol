from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "source/shared/references/development-workflow-prompts.md"


class Protocol6OrchestrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prompt = PROMPT.read_text(encoding="utf-8")
        self.lower = self.prompt.lower()

    def stage_block(self, heading: str) -> str:
        marker = f"## {heading}"
        pos = self.prompt.index(marker)
        next_pos = self.prompt.find("\n## ", pos + len(marker))
        return self.prompt[pos:] if next_pos < 0 else self.prompt[pos:next_pos]

    def test_prompt_reference_has_domain_aware_parameterized_entrypoints(self) -> None:
        for stage in (
            "0. Authority / Affected-Domain Intake",
            "1. D1 Scientific & Mathematical Formulation",
            "2. D2 Algorithm & Numerical Method Design",
            "3. D3 Software Architecture / Workplan",
            "4. D4 Software Implementation",
            "5. Review & Challenge Pass",
            "6. Verification",
            "7. Stabilization / Architecture GC",
            "8. Downstream Authority Alignment",
            "9. Health Audit",
            "10. Closeout",
        ):
            self.assertIn(stage.lower(), self.lower)
        self.assertGreaterEqual(self.prompt.count("INPUTS"), 11)
        self.assertGreaterEqual(self.prompt.count("EXECUTION_MODE"), 11)
        self.assertIn("AUTO_EXECUTE", self.prompt)
        self.assertIn("REPORT_ONLY", self.prompt)

    def test_portable_resolution_is_canonical_once_for_all_stages(self) -> None:
        for token in (
            "local first, public repository second",
            "documented exposed installed-skill root",
            "https://github.com/hjin98/software-development-protocol",
            "source/roles/<skill-name>/skill.md",
            "source/specialists/<skill-name>/skill.md",
            "not shell commands",
            "truthful non-closure",
            "do not claim protocol execution from memory",
            "do not silently substitute a different protocol version",
            "do not guess that a semantic version is a git ref",
        ):
            self.assertIn(token, self.lower)
        self.assertIn("stated once here rather than duplicated eleven times", self.lower)

    def test_execution_contract_prefers_action_and_resolves_inferable_context(self) -> None:
        self.assertIn("execution prompts", self.lower)
        self.assertIn("do not stop at commands, patch suggestions, sample text, or \"next steps\"", self.lower)
        self.assertIn("prefer action over clarification when ordinary context is discoverable", self.lower)
        self.assertIn("ask only when proceeding would require guessing a genuinely consequential", self.lower)

    def test_stage_routes_preserve_domain_ownership(self) -> None:
        expected = {
            "1. D1 Scientific & Mathematical Formulation": "scientific-formulation",
            "2. D2 Algorithm & Numerical Method Design": "numerical-algorithm-design",
            "3. D3 Software Architecture / Workplan": "software-design",
            "4. D4 Software Implementation": "software-implementation",
            "9. Health Audit": "software-maintenance-audit",
            "10. Closeout": "software-documentation",
        }
        for heading, skill in expected.items():
            self.assertIn(skill, self.stage_block(heading).lower(), heading)

    def test_reduced_routes_and_upstream_impact_exclusion_are_explicit(self) -> None:
        intake = self.stage_block("0. Authority / Affected-Domain Intake").lower()
        self.assertIn("d4-only/d3-only classification", intake)
        self.assertIn("proportionate upstream-impact exclusion", intake)
        self.assertIn("do not invent missing d1/d2 documents", intake)
        self.assertIn("reduced d4-only, d3->d4, or d2->d4 paths are normal", self.lower)

    def test_mutation_boundaries_are_explicit(self) -> None:
        d3 = self.stage_block("3. D3 Software Architecture / Workplan").lower()
        d4 = self.stage_block("4. D4 Software Implementation").lower()
        review = self.stage_block("5. Review & Challenge Pass").lower()
        verify = self.stage_block("6. Verification").lower()
        stabilize = self.stage_block("7. Stabilization / Architecture GC").lower()
        align = self.stage_block("8. Downstream Authority Alignment").lower()
        health = self.stage_block("9. Health Audit").lower()
        closeout = self.stage_block("10. Closeout").lower()

        self.assertIn("actually create or update the governing d3->d4 workplan", d3)
        self.assertIn("do not modify product implementation", d3)
        self.assertIn("actually modify repository_target", d4)
        self.assertIn("review must not modify production implementation", review)
        self.assertIn("does not modify production implementation", verify)
        self.assertIn("stabilization remains non-mutating", stabilize)
        self.assertIn("actually update downstream_workplan", align)
        self.assertIn("must not modify production implementation", align)
        self.assertIn("health audit does not implement the repairs", health)
        self.assertIn("actually perform the documentation, lifecycle, generated-artifact", closeout)
        self.assertIn("must not change product behavior", closeout)

    def test_review_verification_stabilization_and_audit_are_not_collapsed(self) -> None:
        review = self.stage_block("5. Review & Challenge Pass").lower()
        verify = self.stage_block("6. Verification").lower()
        stabilize = self.stage_block("7. Stabilization / Architecture GC").lower()
        health = self.stage_block("9. Health Audit").lower()
        self.assertIn("independent implementation-review mode", review)
        self.assertIn("adversarial-verification", verify)
        self.assertIn("stabilization remains non-mutating", stabilize)
        self.assertIn("periodic long-horizon repository audit", health)
        self.assertIn("not a feature review or approval gate", health)

    def test_stage_selection_covers_mixed_review_and_fix_routing(self) -> None:
        selection = self.stage_block("Stage-selection rule of thumb").lower()
        self.assertIn("artifact and mutation boundary", selection)
        self.assertIn("review and fix", selection)
        self.assertIn("review determines and records blockers", selection)
        self.assertIn("d4 implementation performs ordinary code repair", selection)
        self.assertIn("d1-d3 deficiencies route to their owning design domain", selection)

    def test_serious_challenge_blocks_normal_release_semantics(self) -> None:
        self.assertIn("serious challenge", self.lower)
        self.assertIn("before ordinary blockers or pass/no-pass", self.lower)
        closeout = self.stage_block("10. Closeout").lower()
        self.assertIn("unresolved serious challenge", closeout)
        self.assertIn("blocks protocol 6 release", closeout)


if __name__ == "__main__":
    unittest.main()
