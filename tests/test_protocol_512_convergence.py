from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class ConvergenceDurableSemanticsTests(unittest.TestCase):
    """Retain the useful Protocol 5.12 convergence lesson without ossifying its old control plane."""

    def setUp(self) -> None:
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.convergence = read("source/shared/references/convergence-and-cycle-economy.md")
        self.architecture = read("source/shared/references/architecture-and-design.md")
        self.intake = read("source/shared/references/repository-intake.md")

    def test_first_clean_local_defect_remains_lightweight(self) -> None:
        self.assertIn("first clean local defect remains local", self.convergence)
        self.assertIn("does not require a census", self.convergence)
        self.assertIn("first clean local defect remains local", self.workflow)

    def test_recurrence_changes_reasoning_unit_without_freezing_mechanism(self) -> None:
        self.assertIn("material sibling recurrence", self.convergence)
        self.assertIn("shared owner/mechanism", self.convergence)
        self.assertIn("does not answer whether the current realization should survive", self.convergence)
        self.assertIn("recurrence is evidence about the shared owner/mechanism", self.architecture)

    def test_complexity_evidence_triggers_simplification_before_addition(self) -> None:
        self.assertIn("structural complexity accumulation", self.convergence)
        self.assertIn("re-derive and simplify the tier-2 realization", self.convergence)
        self.assertIn("mandatory before another additive durable repair", self.convergence)
        self.assertIn("active tier-2 simplification/re-derivation is required", self.workflow)

    def test_census_is_for_real_completeness_or_safe_simplification(self) -> None:
        self.assertIn("tier-1 correctness claim is finite/exhaustive", self.convergence)
        self.assertIn("bounded sibling discovery is needed", self.convergence)
        self.assertIn("tier-1 correctness claim itself is finite/exhaustive", self.intake)
        self.assertIn("recurrence by itself does not justify preserving the current mechanism", self.intake)

    def test_post_simplification_recurrence_routes_to_earliest_domain(self) -> None:
        self.assertIn("post-simplification recurrence", self.convergence)
        self.assertIn("bounded software design reconsideration", self.convergence)
        self.assertIn("frozen/accepted parent abstraction is wrong", self.workflow)
        self.assertIn("earliest affected d1-d3 owner", self.workflow)

    def test_revision_economy_and_nonrefusal_survive(self) -> None:
        self.assertIn("explicitly requested review still proceeds", self.convergence)
        self.assertIn("ordinary implementation attempts and review cycles do not require a numbered authority revision", self.convergence)
        self.assertIn("no recurrence count, review count", self.convergence)
        self.assertIn("not the pass threshold", self.convergence)


if __name__ == "__main__":
    unittest.main()
