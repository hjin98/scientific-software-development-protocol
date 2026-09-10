from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class ConvergenceDurableSemanticsTests(unittest.TestCase):
    """Retain Protocol 5.12 convergence capability through Protocol 6.2 canonical ownership."""

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
        self.assertIn("does not answer whether the current concretization should survive", self.convergence)
        self.assertIn("material sibling recurrence", self.architecture)
        self.assertIn("shared mechanism", self.architecture)
        self.assertIn("simplify/re-derive delegated concretization", self.architecture)

    def test_complexity_evidence_triggers_simplification_before_addition(self) -> None:
        self.assertIn("structural complexity accumulation", self.convergence)
        self.assertIn("re-derive and simplify the delegated concretization", self.convergence)
        self.assertIn("mandatory before another additive durable repair", self.convergence)
        self.assertIn("simplify/re-derive delegated machinery before another additive durable repair", self.workflow)

    def test_census_is_for_real_completeness_or_safe_simplification(self) -> None:
        self.assertIn("governing parent/external correctness claim is finite/exhaustive", self.convergence)
        self.assertIn("bounded sibling discovery is needed", self.convergence)
        self.assertIn("governing correctness claim is itself finite/exhaustive", self.intake)
        self.assertIn("bounded sibling discovery is needed for safe consolidation/removal/family closure", self.intake)

    def test_post_simplification_recurrence_routes_to_earliest_domain(self) -> None:
        self.assertIn("post-simplification recurrence", self.convergence)
        self.assertIn("bounded software design reconsideration", self.convergence)
        self.assertIn("accepted parent abstraction or cycle-scoped decision", self.convergence)
        self.assertIn("earliest affected abstraction", self.convergence)
        self.assertIn("reopen the parent only when its accepted abstraction or material cycle decision must change", self.workflow)

    def test_revision_economy_and_nonrefusal_survive(self) -> None:
        self.assertIn("explicitly requested review still proceeds", self.convergence)
        self.assertIn("ordinary implementation attempts and review cycles do not require a numbered authority revision", self.convergence)
        self.assertIn("no recurrence count, review count", self.convergence)
        self.assertIn("not the pass threshold", self.convergence)

    def test_current_convergence_control_plane_is_protocol6_native(self) -> None:
        for text in (self.workflow, self.convergence, self.intake):
            self.assertNotIn("tier-2", text)
            self.assertNotIn("tier 1", text)
            self.assertNotIn("product/frozen", text)
        self.assertIn("delegated concretization", self.convergence)
        self.assertIn("accepted-current d1-d4 authority", self.workflow)


if __name__ == "__main__":
    unittest.main()
