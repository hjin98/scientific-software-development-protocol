from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class ConvergenceDurableSemanticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.convergence = read("source/shared/references/convergence-and-cycle-economy.md")
        self.architecture = read("source/shared/references/architecture-and-design.md")
        self.intake = read("source/shared/references/repository-intake.md")

    def test_local_defect_and_recurrence_semantics_survive(self) -> None:
        self.assertIn("first clean local defect remains local", self.convergence)
        self.assertIn("material sibling recurrence", self.convergence)
        self.assertIn("shared owner/mechanism", self.convergence)
        self.assertIn("convergence-and-cycle-economy.md", self.workflow)

    def test_complexity_triggers_simplification_before_addition(self) -> None:
        self.assertIn("structural complexity accumulation", self.convergence)
        self.assertIn("re-derive and simplify", self.convergence)
        self.assertIn("before another additive durable repair", self.convergence)
        self.assertIn("simplification", self.workflow)

    def test_census_is_bounded_by_a_real_completeness_claim(self) -> None:
        self.assertIn("finite/exhaustive", self.convergence)
        self.assertIn("bounded sibling discovery", self.convergence)
        self.assertIn("governing correctness claim itself is finite/exhaustive", self.intake)
        self.assertIn("recurrence by itself does not justify preserving the current mechanism", self.intake)

    def test_recurrence_can_route_to_earliest_affected_owner(self) -> None:
        self.assertIn("post-simplification recurrence", self.convergence)
        self.assertIn("earliest", self.convergence)
        self.assertIn("d1", self.convergence)
        self.assertIn("d3", self.convergence)
        self.assertIn("earliest affected", self.workflow)

    def test_revision_economy_remains_non_numeric(self) -> None:
        self.assertIn("ordinary implementation attempts and review cycles do not require a numbered authority revision", self.convergence)
        self.assertIn("no recurrence count, review count", self.convergence)
        self.assertIn("acceptance", self.convergence)

    def test_current_control_plane_uses_concretization_vocabulary(self) -> None:
        self.assertIn("delegated concretization", self.convergence)
        self.assertIn("accepted-current", self.workflow)
        self.assertIn("recurrence", self.architecture)


if __name__ == "__main__":
    unittest.main()
