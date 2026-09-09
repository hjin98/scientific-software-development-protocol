from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class EngineeringStewardshipContractTests(unittest.TestCase):
    def test_product_truth_is_salient_in_both_entrypoints(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        for text in (design, implementation):
            self.assertIn("stakeholder", text)
            self.assertIn("durable software product", text)
            self.assertIn("tests", text)
            self.assertIn("not the objective", text)
            self.assertIn("truthful non-closure", text)

    def test_acceptance_integrity_details_live_in_testing_reference(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "measurement instruments",
            "deleting/weakening",
            "removing known failing inputs",
            "buggy implementation output",
            "warning/success",
            "making a required check optional",
            "relaxing a material threshold",
            "rewriting specification/documentation",
            "test, fixture, threshold, and specification changes remain legitimate",
        ):
            self.assertIn(phrase, testing)

    def test_non_adversarial_interpretation_and_owning_layer_repair_remain_direct(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("non-adversarially", design)
        self.assertIn("protected engineering purpose", implementation)
        self.assertIn("fix a clear local defect at the owning layer", implementation)

    def test_self_correction_and_truthful_nonclosure_are_preserved(self) -> None:
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("invalidate it and repair/retest", implementation)
        self.assertIn("reasonable in-scope engineering path remains", implementation)
        self.assertIn("counterfeit completion", implementation)

    def test_long_horizon_stewardship_remains_bounded(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        architecture = read("source/shared/references/architecture-and-design.md").lower()
        self.assertIn("stewardship remains bounded", design)
        self.assertIn("task/contracts/affected surfaces", design)
        self.assertIn("does not authorize unrelated", design)
        self.assertIn("speculative future-proofing", design)
        self.assertIn("bounded by explicit stakeholder requirements", workflow)
        self.assertIn("accepted scope", architecture)

    def test_independent_review_can_reject_literal_but_bad_outcome(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        testing = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("literal compliance actually concretizes the protected stakeholder outcome", design)
        self.assertIn("workplan/design deficiency", design)
        self.assertIn("independent-evaluator counterfactual", testing)

    def test_workplans_and_gates_remain_subordinate(self) -> None:
        workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        template = read("source/shared/templates/implementation_workplan_template.md").lower()
        self.assertIn("not terminal objectives", workflow)
        self.assertIn("must never create pressure to manufacture a pass", workflow)
        self.assertIn("anti-shortcut/integrity constraint", template)
        self.assertIn("attach only when material", template)

    def test_root_agents_is_compact_router_not_duplicate_manual(self) -> None:
        agents = read("AGENTS.md")
        implementation = read("source/roles/software-implementation/SKILL.md")
        lower = agents.lower()
        self.assertIn("engineering steward", lower)
        self.assertIn("durable software product", lower)
        self.assertIn("load detailed references only when", lower)
        self.assertIn("semantic owner", lower)
        self.assertLess(len(agents), len(implementation) // 2)
        self.assertNotIn("## governing doctrine", lower)
        self.assertNotIn("## product design", lower)

    def test_optional_specialists_share_product_truth_without_new_gate(self) -> None:
        docs = read("source/specialists/software-documentation/SKILL.md").lower()
        hygiene = read("source/specialists/repository-hygiene/SKILL.md").lower()
        self.assertIn("truthful stakeholder", docs)
        self.assertIn("never rewrite product truth", docs)
        self.assertIn("long-term repository safety", hygiene)
        self.assertIn("not cosmetic closure", hygiene)
        self.assertIn("not a lifecycle role", hygiene)


if __name__ == "__main__":
    unittest.main()
