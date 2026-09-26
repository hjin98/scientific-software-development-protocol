from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class EngineeringStewardshipContractTests(unittest.TestCase):
    """Preserve Protocol 5.7 stewardship at its Protocol 6.2 canonical owners."""

    def test_product_truth_is_owned_by_universal_kernel(self) -> None:
        kernel = read("source/shared/references/abstraction-and-concretization.md").lower()
        for phrase in (
            "steward",
            "durable product/outcome",
            "process artifacts",
            "self-authorizing",
            "protected purpose",
            "governed scope",
            "unrelated enhancement",
            "speculative future-proofing",
        ):
            self.assertIn(phrase, kernel)

    def test_d3_d4_entrypoints_load_the_stewardship_owner(self) -> None:
        # consumed entrypoints: the kernel route is generated into their entry contract
        for path in ("dist/skills/software-design/SKILL.md", "dist/skills/software-implementation/SKILL.md"):
            text = read(path).lower()
            self.assertIn("references/abstraction-and-concretization.md", text, path)
            self.assertIn("before substantive", text, path)

    def test_acceptance_integrity_details_live_in_testing_reference(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "instruments, not truth or product objectives",
            "deleting/weakening assertions",
            "removing known failing inputs",
            "copying defective production output into expected values",
            "converting required failure into success/warning",
            "making required checks optional",
            "widening tolerances/thresholds because they failed",
            "rewriting authority to bless unintended behavior",
            "test/fixture/threshold/specification changes are legitimate when governing authority genuinely changed",
        ):
            self.assertIn(phrase, testing)

    def test_owning_layer_repair_and_truthful_nonclosure_remain_direct(self) -> None:
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("direct owning-layer repair", implementation)
        self.assertIn("simplest admissible concretization", implementation)
        self.assertIn("remove/narrow/alter/consolidate/refactor", implementation)
        self.assertIn("a required check that did not execute is not a pass", implementation)
        self.assertIn("report unavailable/blocking rather than proxy-passing it", implementation)

    def test_independent_review_can_reject_literal_but_bad_outcome(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        testing = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("literal workplan compliance is insufficient", design)
        self.assertIn("too weak for the protected outcome", design)
        self.assertIn("independent evaluator of the same accepted outcome/engineering envelope", testing)

    def test_workplans_and_evidence_remain_subordinate(self) -> None:
        workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        kernel = read("source/shared/references/abstraction-and-concretization.md").lower()
        self.assertIn("workplans are coordination/authority for the bounded cycle, not terminal objectives", workflow)
        for phrase in ("workplans", "tests", "coordination state", "self-authorizing"):
            self.assertIn(phrase, kernel)

    def test_root_agents_is_compact_router_not_duplicate_manual(self) -> None:
        agents = read("AGENTS.md")
        implementation = read("source/roles/software-implementation/SKILL.md")
        lower = agents.lower()
        self.assertIn("engineering steward", lower)
        self.assertIn("stakeholder's durable product", lower)
        self.assertIn("role/specialist entrypoint owns root routing", lower)
        self.assertIn("lossless representation rule", lower)
        # AGENTS.md must stay a compact router rather than a duplicate manual: smaller than
        # the universal kernel it routes to and free of its section structure.
        kernel = read("source/shared/references/abstraction-and-concretization.md")
        self.assertLess(len(agents), len(kernel))
        self.assertNotIn("## lossless representation rule", lower)
        self.assertIn("## implementation contract", implementation.lower())
        self.assertNotIn("## governing doctrine", lower)

    def test_optional_specialists_remain_non_authoritative_and_product_safe(self) -> None:
        docs = read("source/specialists/software-documentation/SKILL.md").lower()
        hygiene = read("source/specialists/repository-hygiene/SKILL.md").lower()
        self.assertIn("optional editorial/publication specialist", docs)
        self.assertIn("do not create a fifth authority domain", docs)
        self.assertIn("cannot self-approve semantic changes", docs)
        self.assertIn("repository safety/recoverability outrank cosmetic cleanliness", hygiene)
        self.assertIn("do not interrupt active engineering merely to make a tree look tidy", hygiene)
        self.assertIn("never use hygiene to", hygiene)
        self.assertIn("change product/scientific semantics", hygiene)


if __name__ == "__main__":
    unittest.main()
