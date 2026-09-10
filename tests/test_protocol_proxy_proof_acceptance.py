from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class ProxyProofAcceptanceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.testing = read("source/shared/references/testing-and-validation.md")
        self.design = read("source/roles/software-design/SKILL.md")
        self.implementation = read("source/roles/software-implementation/SKILL.md")
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.template = read("source/shared/templates/implementation_workplan_template.md")

    def test_testing_reference_is_canonical_proxy_proof_owner(self) -> None:
        for phrase in ("proxy-proof real-owner evidence", "real semantic owner/path", "allowed test-double boundary", "could the evidence remain green", "cannot close that owner claim"):
            self.assertIn(phrase, self.testing)

    def test_historical_proxy_substitution_classes_remain_rejected(self) -> None:
        for phrase in ("mocking/reimplementing the owner", "calling a downstream helper", "seeding post-decision state", "replacing durable persistence", "helper-generated results"):
            self.assertIn(phrase, self.testing)

    def test_bounded_doubles_below_real_owner_remain_valid(self) -> None:
        self.assertIn("not a blanket mock ban", self.testing)
        self.assertIn("bounded deterministic doubles remain valid below/outside the owner", self.testing)
        self.assertIn("expensive data/training", self.testing)
        self.assertIn("production scale", self.testing)

    def test_unavailable_required_owner_boundary_is_not_proxy_passed(self) -> None:
        self.assertIn("unavailable/blocking", self.testing)
        self.assertIn("required evidence", self.implementation)
        self.assertIn("blocking", self.implementation)

    def test_entrypoints_keep_salient_owner_trigger_not_full_duplicate_manual(self) -> None:
        for text in (self.design, self.implementation):
            self.assertIn("references/testing-and-validation.md", text)
            self.assertIn("owner", text)
            self.assertNotIn("mocking/reimplementing the owner", text)

    def test_workplan_boundary_is_conditional_not_ceremonial(self) -> None:
        self.assertIn("acceptance boundary", self.template)
        self.assertIn("when proxy acceptance is a material risk", self.template)
        self.assertIn("when material", self.template)
        self.assertIn("real-owner", self.workflow)

    def test_delegated_owner_replacement_remaps_without_freezing_old_owner(self) -> None:
        self.assertIn("if delegated owner identity changes under equivalent semantics", self.testing)
        self.assertIn("remap/rerun owner-specific evidence", self.testing)
        self.assertIn("delegated", self.template)
        self.assertIn("replaceable", self.implementation)

    def test_targeted_structural_guardrails_do_not_create_global_mock_policy(self) -> None:
        self.assertIn("source/structural negative assertions", self.testing)
        self.assertIn("not a blanket mock ban", self.testing)


if __name__ == "__main__":
    unittest.main()
