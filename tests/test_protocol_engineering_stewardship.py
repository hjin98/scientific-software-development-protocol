from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class EngineeringStewardshipContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = read("source/shared/references/abstraction-and-concretization.md")
        self.design = read("source/roles/software-design/SKILL.md")
        self.implementation = read("source/roles/software-implementation/SKILL.md")
        self.testing = read("source/shared/references/testing-and-validation.md")
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.architecture = read("source/shared/references/architecture-and-design.md")

    def test_engineering_fitness_and_truth_remain_above_development_economy(self) -> None:
        self.assertIn("domain engineering fitness", self.foundation)
        self.assertIn("minimum justified concretization complexity", self.foundation)
        self.assertIn("development economy", self.foundation)
        self.assertIn("truth", self.foundation)
        self.assertIn("counterfeit", self.testing)

    def test_acceptance_integrity_details_live_in_testing_reference(self) -> None:
        for phrase in ("instruments, not truth", "deleting/weakening assertions", "removing known failing inputs", "defective production output", "required failure", "required checks optional", "widening tolerances", "rewriting authority", "legitimate when governing authority genuinely changed"):
            self.assertIn(phrase, self.testing)

    def test_owning_layer_repair_and_non_additive_preference_survive(self) -> None:
        self.assertIn("smallest owning-layer repair", self.implementation)
        self.assertIn("remove/narrow/alter/consolidate", self.implementation)
        self.assertIn("minimum justified", self.design)
        self.assertIn("removal/consolidation", self.design)

    def test_truthful_nonclosure_is_preserved(self) -> None:
        self.assertIn("required check", self.implementation)
        self.assertIn("blocking", self.implementation)
        self.assertIn("required check that did not execute is not a pass", self.testing)
        self.assertIn("serious challenge", self.foundation)

    def test_stewardship_scope_remains_bounded(self) -> None:
        self.assertIn("requested/accepted scope", self.design)
        self.assertIn("does not authorize unrelated enhancement", self.design)
        self.assertIn("accepted scope", self.architecture)
        self.assertIn("side constraints", self.workflow)

    def test_independent_review_can_reject_literal_but_bad_outcome(self) -> None:
        self.assertIn("independent evaluator", self.testing)
        self.assertIn("same accepted outcome", self.testing)
        self.assertIn("challenge", self.design)

    def test_workplans_and_gates_remain_subordinate(self) -> None:
        template = read("source/shared/templates/implementation_workplan_template.md")
        self.assertIn("green tests", template)
        self.assertIn("anti-shortcut", template)
        self.assertIn("when material", template)
        self.assertIn("cycle-scoped", self.workflow)

    def test_root_agents_is_compact_router_not_duplicate_manual(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        lower = agents.lower()
        self.assertIn("router", lower)
        self.assertIn("semantic owner", lower)
        self.assertIn("lossless", lower)
        self.assertLess(len(agents), len((ROOT / "source/roles/software-implementation/SKILL.md").read_text(encoding="utf-8")))

    def test_optional_specialists_do_not_create_new_authority_domains(self) -> None:
        docs = read("source/specialists/software-documentation/SKILL.md")
        hygiene = read("source/specialists/repository-hygiene/SKILL.md")
        audit = read("source/specialists/software-maintenance-audit/SKILL.md")
        self.assertIn("does not own", docs)
        self.assertIn("does not own", audit)
        self.assertIn("not a lifecycle role", hygiene)


if __name__ == "__main__":
    unittest.main()
