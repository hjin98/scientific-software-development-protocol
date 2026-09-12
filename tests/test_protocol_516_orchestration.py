from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "source/shared/references/development-workflow-prompts.md"


class Protocol6OrchestrationTests(unittest.TestCase):
    """Preserve Protocol 5.16 orchestration capability under the Protocol 6.2 prompt representation."""

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
            "auto_local_first",
            "governing-version-compatible installed skill/exposed skill root",
            "https://github.com/hjin98/scientific-software-development-protocol",
            "immutable public-source ref mapped for that version",
            "truthful non-closure",
            "silently substitute latest/default-branch doctrine",
            "never guess that a semantic version is a git ref",
            "repository-default bytes are never a substitute",
        ):
            self.assertIn(token, self.lower)

        current_version = (ROOT / "source/PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        if current_version == "6.2.0":
            published = re.search(r"public_ref = ([0-9a-f]{40})", self.lower)
            if published is None:
                self.assertIn("bootstrap self-reference rule", self.lower)
                self.assertIn("automatic current-6.2 public fallback is unavailable", self.lower)
                self.assertNotIn("current 6.2 may fall back", self.lower)
            else:
                self.assertNotEqual(published.group(1), "1181c2031710c5d343194d87d08543290fded0ab")
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", self.lower)
        else:
            self.assertIn("current_protocol = 6.3.0", self.lower)
            current = re.search(r"current_public_ref = ([^\s]+)", self.lower)
            self.assertIsNotNone(current)
            current_ref = current.group(1)
            self.assertNotEqual(current_ref, "1484c1d3caa49d87cc15bc52a5e775399c1dae1b")
            self.assertTrue(current_ref == "unavailable_pending_6.3_bootstrap_qualification" or re.fullmatch(r"[0-9a-f]{40}", current_ref))
            self.assertIn("accepted_6_2_public_ref = 5a062ebc472755607b9dc66d33a5ebbc4b7429aa", self.lower)
            self.assertIn("self-reference-safe source snapshot", self.lower)

    def test_execution_contract_prefers_action_and_resolves_inferable_context(self) -> None:
        self.assertIn("these are execution prompts", self.lower)
        self.assertIn("perform every authorized action rather than stopping at commands/snippets/next steps", self.lower)
        self.assertIn("prefer action over clarification when context is discoverable", self.lower)
        self.assertIn("ask only when proceeding would require guessing consequential authority", self.lower)

    def test_material_authority_acceptance_requires_independent_falsification_first(self) -> None:
        self.assertIn("material d1/d2/durable-d3 authority mutation becomes accepted-current only after", self.lower)
        self.assertIn("independent falsification by a context/reviewer that did not author the proposal", self.lower)
        self.assertIn("required human ratification", self.lower)
        for heading in (
            "1. D1 Scientific & Mathematical Formulation",
            "2. D2 Algorithm & Numerical Method Design",
            "3. D3 Software Architecture / Workplan",
        ):
            block = self.stage_block(heading).lower()
            self.assertIn("independent falsification", block, heading)
            self.assertIn("otherwise remain", block, heading)

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
        self.assertIn("d3/d4-only classification", intake)
        self.assertIn("proportionate upstream-impact exclusion", intake)
        self.assertIn("do not invent missing d1/d2 artifacts", intake)
        self.assertIn("reduced d4-only, d3->d4, d2->d4 or d1->d3/d4 paths are normal", self.lower)

    def test_mutation_boundaries_are_explicit(self) -> None:
        d3 = self.stage_block("3. D3 Software Architecture / Workplan").lower()
        d4 = self.stage_block("4. D4 Software Implementation").lower()
        review = self.stage_block("5. Review & Challenge Pass").lower()
        verify = self.stage_block("6. Verification").lower()
        stabilize = self.stage_block("7. Stabilization / Architecture GC").lower()
        align = self.stage_block("8. Downstream Authority Alignment").lower()
        health = self.stage_block("9. Health Audit").lower()
        closeout = self.stage_block("10. Closeout").lower()

        self.assertIn("create/update the governing d3->d4 plan", d3)
        self.assertIn("under auto_execute modify/test the real target", d4)
        self.assertIn("review does not modify product implementation", review)
        self.assertIn("deeper non-mutating risk-triggered falsification", verify)
        self.assertIn("non-mutatingly ask whether", stabilize)
        self.assertIn("update the downstream plan/authority when warranted, never production implementation", align)
        self.assertIn("the audit itself neither accepts architecture nor implements repairs", health)
        self.assertIn("under auto_execute reconcile affected current d1-d4 authority", closeout)
        self.assertIn("closeout cannot change product semantics", closeout)

    def test_review_verification_stabilization_and_audit_are_not_collapsed(self) -> None:
        review = self.stage_block("5. Review & Challenge Pass").lower()
        verify = self.stage_block("6. Verification").lower()
        stabilize = self.stage_block("7. Stabilization / Architecture GC").lower()
        health = self.stage_block("9. Health Audit").lower()
        self.assertIn("independent review mode", review)
        self.assertIn("deeper non-mutating risk-triggered falsification", verify)
        self.assertIn("after ordinary review otherwise passes", stabilize)
        self.assertIn("longitudinal sensing", health)
        self.assertIn("metrics are sensors", health)

    def test_stage_selection_covers_mixed_review_and_fix_routing(self) -> None:
        selection = self.stage_block("Stage selection").lower()
        self.assertIn("semantic/mutation boundary", selection)
        self.assertIn("mixed `review and fix` preserves the boundary", selection)
        self.assertIn("review identifies/routes findings", selection)
        self.assertIn("the owning mutation stage performs repair", selection)

    def test_serious_challenge_blocks_normal_release_semantics(self) -> None:
        self.assertIn("serious challenge", self.lower)
        self.assertIn("emit `serious challenge` before ordinary findings", self.lower)
        self.assertIn("stop unqualified closure", self.lower)
        closeout = self.stage_block("10. Closeout").lower()
        self.assertIn("unresolved acceptance/serious challenge", closeout)
        self.assertIn("cannot", closeout)
        self.assertIn("completion", closeout)


if __name__ == "__main__":
    unittest.main()
