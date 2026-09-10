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

    def test_prompt_reference_keeps_all_parameterized_stages(self) -> None:
        for stage in (
            "0. Authority / Affected-Domain Intake", "1. D1 Scientific & Mathematical Formulation",
            "2. D2 Algorithm & Numerical Method Design", "3. D3 Software Architecture / Workplan",
            "4. D4 Software Implementation", "5. Review & Challenge Pass", "6. Verification",
            "7. Stabilization / Architecture GC", "8. Downstream Authority Alignment",
            "9. Health Audit", "10. Closeout",
        ):
            self.assertIn(stage.lower(), self.lower)
        self.assertEqual(self.prompt.count("INPUTS"), 11)
        self.assertEqual(self.prompt.count("EXECUTION_MODE"), 11)
        self.assertIn("AUTO_EXECUTE", self.prompt)
        self.assertIn("REPORT_ONLY", self.prompt)

    def test_portable_resolution_is_shared_once_and_version_bound(self) -> None:
        for token in (
            "auto_local_first", "https://github.com/hjin98/scientific-software-development-protocol",
            "governing protocol version", "never guess that a semantic version is a git ref",
            "truthful non-closure", "repository-default bytes are never a substitute",
        ):
            self.assertIn(token, self.lower)
        self.assertIn("automatic current-6.2 public fallback is unavailable", self.lower)

    def test_execution_contract_prefers_action_when_context_is_discoverable(self) -> None:
        self.assertIn("execution prompts", self.lower)
        self.assertIn("rather than stopping at commands/snippets/next steps", self.lower)
        self.assertIn("prefer action over clarification when context is discoverable", self.lower)

    def test_material_authority_acceptance_requires_independent_falsification(self) -> None:
        shared = self.lower
        self.assertIn("independent falsification", shared)
        self.assertIn("did not author the proposal", shared)
        for heading in ("1. D1 Scientific & Mathematical Formulation", "2. D2 Algorithm & Numerical Method Design", "3. D3 Software Architecture / Workplan"):
            block = self.stage_block(heading).lower()
            self.assertIn("accepted-current", block)
            self.assertIn("independent", block)

    def test_stage_routes_preserve_domain_ownership(self) -> None:
        expected = {
            "1. D1 Scientific & Mathematical Formulation": "scientific-formulation",
            "2. D2 Algorithm & Numerical Method Design": "numerical-algorithm-design",
            "3. D3 Software Architecture / Workplan": "software-design",
            "4. D4 Software Implementation": "software-implementation",
            "9. Health Audit": "software-maintenance-audit",
        }
        for heading, skill in expected.items():
            self.assertIn(skill, self.stage_block(heading).lower(), heading)

    def test_reduced_routes_and_upstream_impact_exclusion_are_explicit(self) -> None:
        intake = self.stage_block("0. Authority / Affected-Domain Intake").lower()
        self.assertIn("proportionate upstream-impact exclusion", intake)
        self.assertIn("do not invent missing d1/d2 artifacts", intake)
        self.assertIn("reduced d4-only", self.lower)
        self.assertIn("d2->d4", self.lower)

    def test_mutation_boundaries_remain_explicit(self) -> None:
        d3 = self.stage_block("3. D3 Software Architecture / Workplan").lower()
        d4 = self.stage_block("4. D4 Software Implementation").lower()
        review = self.stage_block("5. Review & Challenge Pass").lower()
        verify = self.stage_block("6. Verification").lower()
        stabilize = self.stage_block("7. Stabilization / Architecture GC").lower()
        align = self.stage_block("8. Downstream Authority Alignment").lower()
        health = self.stage_block("9. Health Audit").lower()
        closeout = self.stage_block("10. Closeout").lower()
        self.assertIn("create/update", d3)
        self.assertIn("modify/test the real target", d4)
        self.assertIn("does not modify product implementation", review)
        self.assertIn("neither replaces ordinary review nor mutates production implementation", verify)
        self.assertIn("non-mutating", stabilize)
        self.assertIn("never production implementation", align)
        self.assertIn("neither accepts architecture nor implements repairs", health)
        self.assertIn("closeout cannot change product semantics", closeout)

    def test_review_verification_stabilization_and_health_audit_are_distinct(self) -> None:
        self.assertIn("independent review mode", self.stage_block("5. Review & Challenge Pass").lower())
        self.assertIn("deeper non-mutating risk-triggered falsification", self.stage_block("6. Verification").lower())
        self.assertIn("minimum justified system", self.stage_block("7. Stabilization / Architecture GC").lower())
        self.assertIn("longitudinal sensing", self.stage_block("9. Health Audit").lower())

    def test_mixed_review_and_fix_preserves_mutation_boundary(self) -> None:
        self.assertIn("mixed \"review and fix\" preserves the boundary", self.lower)
        self.assertIn("review identifies/routes findings", self.lower)
        self.assertIn("owning mutation stage performs repair", self.lower)

    def test_serious_challenge_and_risk_override_state_are_preserved(self) -> None:
        self.assertIn("serious challenge", self.lower)
        self.assertIn("before ordinary findings", self.lower)
        self.assertIn("risk-accepted/provisional", self.lower)
        self.assertIn("authority_state = risk_accepted_provisional", self.lower)
        self.assertIn("json key `authority_state`", self.lower)


if __name__ == "__main__":
    unittest.main()
