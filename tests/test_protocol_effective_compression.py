from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class HistoricalFailureModeScenarios(unittest.TestCase):
    """Historical engineering capabilities expressed through Protocol 6.2 owners."""

    def setUp(self) -> None:
        self.foundation = read("source/shared/references/abstraction-and-concretization.md")
        self.design = read("source/roles/software-design/SKILL.md")
        self.implementation = read("source/roles/software-implementation/SKILL.md")
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.testing = read("source/shared/references/testing-and-validation.md")
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.convergence = read("source/shared/references/convergence-and-cycle-economy.md")

    def test_green_tests_plus_omitted_obligation_is_incomplete(self) -> None:
        self.assertIn("green tests do not establish omitted", self.testing)
        self.assertIn("required check that did not execute is not a pass", self.testing)

    def test_downstream_helper_cannot_replace_required_owner(self) -> None:
        self.assertIn("calling a downstream helper", self.testing)
        self.assertIn("cannot close that owner claim", self.testing)

    def test_expensive_dependency_can_be_controlled_below_real_owner(self) -> None:
        self.assertIn("bounded deterministic doubles", self.testing)
        self.assertIn("expensive data/training", self.testing)
        self.assertIn("not a blanket mock ban", self.testing)

    def test_equivalent_local_concretization_does_not_gain_authority(self) -> None:
        self.assertIn("treat lower machinery as replaceable", self.implementation)
        self.assertIn("does not acquire authority because it exists", self.foundation)
        self.assertIn("cycle-scoped", self.workflow)

    def test_invalidated_premise_routes_to_earliest_owner(self) -> None:
        self.assertIn("if governing authority may be wrong", self.implementation)
        self.assertIn("route", self.implementation)
        self.assertIn("earliest affected", self.workflow)

    def test_acceptance_signal_cannot_be_repaired_by_weakening_oracle_or_authority(self) -> None:
        for phrase in ("deleting/weakening assertions", "removing known failing inputs", "rewriting authority"):
            self.assertIn(phrase, self.testing)

    def test_small_work_does_not_require_invented_lifecycle_machinery(self) -> None:
        self.assertIn("local d4 repair", self.workflow)
        self.assertIn("need not invent a workplan", self.implementation)
        self.assertIn("coherent", self.workflow)

    def test_new_affected_surface_is_incorporated_without_requirement_expansion(self) -> None:
        self.assertIn("affected surface", self.implementation)
        self.assertIn("re-derive", self.testing)
        self.assertIn("requirement", self.foundation)

    def test_removal_or_unique_owner_claim_uses_structural_evidence(self) -> None:
        self.assertIn("removal/uniqueness/ownership/no-legacy-path", self.testing)
        self.assertIn("structural", self.testing)

    def test_protocol5_capabilities_are_inherited_without_parallel_vocabulary(self) -> None:
        self.assertIn("protocol 5", self.versioning)
        self.assertIn("capability", self.versioning)
        self.assertIn("minimum justified complexity", self.versioning)
        self.assertIn("snapshot-complete", self.versioning)
        self.assertIn("proxy-proof", self.versioning)

    def test_urgent_mitigation_preserves_debt_and_normal_path(self) -> None:
        self.assertIn("urgent", self.workflow)
        self.assertIn("mitigation", self.workflow)
        self.assertIn("debt", self.workflow)
        self.assertIn("simplification", self.convergence)

    def test_long_work_has_compact_non_authoritative_resumable_state(self) -> None:
        self.assertIn("resumable", self.workflow)
        self.assertIn("non-authoritative", self.workflow)
        self.assertIn("lossless representation", self.foundation)

    def test_current_control_plane_uses_one_owner_and_progressive_disclosure(self) -> None:
        self.assertIn("one detailed owner per generic rule", self.foundation)
        self.assertIn("progressive disclosure", self.foundation)
        self.assertIn("package membership", self.foundation)
        self.assertIn("does not imply activation", self.foundation)


if __name__ == "__main__":
    unittest.main()
