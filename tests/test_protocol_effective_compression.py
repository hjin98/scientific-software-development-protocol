from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def current_operational_documents() -> tuple[Path, ...]:
    roots = (
        ROOT / "source" / "roles",
        ROOT / "source" / "specialists",
        ROOT / "source" / "shared" / "references",
        ROOT / "source" / "shared" / "templates",
    )
    historical_compatibility_owner = (
        ROOT / "source" / "shared" / "references" / "protocol-versioning-and-compatibility.md"
    )
    return tuple(
        sorted(
            path
            for root in roots
            for path in root.rglob("*.md")
            if path != historical_compatibility_owner
        )
    )


class HistoricalFailureModeScenarios(unittest.TestCase):
    """Preserve historical safeguards while allowing Protocol 6.2 canonical ownership."""

    def setUp(self) -> None:
        self.design = read("source/roles/software-design/SKILL.md")
        self.implementation = read("source/roles/software-implementation/SKILL.md")
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.testing = read("source/shared/references/testing-and-validation.md")
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.concurrency = read("source/shared/references/concurrency-and-orchestration.md")
        self.debugging = read("source/shared/references/debugging-and-state-recovery.md")

    def test_green_tests_plus_omitted_obligation_is_incomplete(self) -> None:
        self.assertIn("green tests do not establish omitted workplan/conformance obligations", self.testing)
        self.assertIn("green tests do not prove omitted workplan obligations", self.implementation)

    def test_downstream_helper_cannot_replace_required_production_caller(self) -> None:
        self.assertIn("calling a downstream helper when production routing is part of the claim", self.testing)
        self.assertIn("if yes, it cannot close that owner claim", self.testing)

    def test_expensive_dependency_can_be_faked_below_real_owner(self) -> None:
        self.assertIn("bounded deterministic doubles remain valid below/outside the owner", self.testing)
        self.assertIn("expensive data/training", self.testing)

    def test_equivalent_local_concretization_is_reconciliation_not_redesign(self) -> None:
        self.assertIn("equivalent local concretization is d4 reconciliation, not redesign", self.implementation)
        self.assertIn("removing/consolidating/replacing expected lower machinery with an equivalent concretization is local reconciliation, not redesign", self.workflow)
        self.assertIn("suggested mechanisms remain delegated unless explicitly frozen", self.workflow)

    def test_invalidated_accepted_premise_routes_to_earliest_owner(self) -> None:
        self.assertIn("challenge upward when admissible evidence indicates accepted authority may itself be materially false", self.implementation)
        self.assertIn("reopen d3/d2/d1 only when the governing abstraction/cycle decision must change", self.implementation)
        self.assertIn("earliest affected semantic owner", self.workflow)

    def test_acceptance_signal_cannot_be_repaired_by_weakening_fixture_or_spec(self) -> None:
        self.assertIn("deleting/weakening assertions", self.testing)
        self.assertIn("removing known failing inputs", self.testing)
        self.assertIn("rewriting authority to bless unintended behavior", self.testing)

    def test_self_correction_cannot_manufacture_closure(self) -> None:
        self.assertIn("a required check that did not execute is not a pass", self.implementation)
        self.assertIn("report unavailable/blocking rather than proxy-passing it", self.implementation)

    def test_small_local_change_does_not_require_micro_gating(self) -> None:
        self.assertIn("a coherent material behavior/risk boundary is normally one implementation stage", self.workflow)
        self.assertIn("tightly coupled edits may form one stage", self.implementation)
        self.assertIn("file count does not define stage count", self.implementation)

    def test_newly_discovered_affected_surface_is_incorporated_without_unrelated_redesign(self) -> None:
        self.assertIn("the accepted plan is the minimum known contract, not a ceiling on newly discovered affected behavior", self.workflow)
        self.assertIn("affected-surface expansion is not requirement expansion", self.workflow)
        self.assertIn("re-derive the complete final affected semantic/behavioral/evidence/documentation surface", self.implementation)

    def test_removal_or_unique_authority_claim_needs_structural_evidence(self) -> None:
        self.assertIn("removal/uniqueness/ownership/no-legacy-path claims", self.testing)
        self.assertIn("source/structural negative assertions", self.testing)

    def test_literal_contract_pass_that_defeats_stakeholder_outcome_is_rejected(self) -> None:
        self.assertIn("literal workplan compliance is insufficient", self.design)
        self.assertIn("too weak for the protected outcome", self.design)
        self.assertIn("independent evaluator of the same accepted outcome/engineering envelope", self.testing)

    def test_protocol5_is_functionally_inherited_as_protocol6_generalization(self) -> None:
        self.assertIn("protocol 6 generalizes protocol 5", self.versioning)
        self.assertIn("capability, not obsolete wording, is the compatibility oracle", self.versioning)
        self.assertIn("compression that loses behavior is a defect", self.versioning)
        self.assertIn("recovers the former software-local design->implementation specialization", self.versioning)

    def test_urgent_mitigation_preserves_simplification_debt(self) -> None:
        self.assertIn("bounded reversible or safely replaceable mitigation", self.workflow)
        self.assertIn("keep unresolved debt explicit", self.workflow)
        self.assertIn("emergency use never promotes the mitigation into durable authority", self.workflow)

    def test_long_work_has_compact_non_authoritative_resumable_state(self) -> None:
        self.assertIn("compact temporary working state", self.workflow)
        self.assertIn("governing snapshot identity", self.workflow)
        self.assertIn("derived coordination state, not authority", self.workflow)
        self.assertIn("should disappear when no longer useful", self.workflow)

    def test_current_operational_control_plane_uses_protocol6_semantics(self) -> None:
        forbidden = (
            "product/frozen",
            "frozen_parent_authority",
            "tier-2",
            "tier 1a",
            "tier 1b",
            "shared protocol 5 doctrine remains authoritative",
        )
        for path in current_operational_documents():
            text = path.read_text(encoding="utf-8").lower()
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                for legacy_token in forbidden:
                    self.assertNotIn(legacy_token, text)
        self.assertIn("accepted d3 architecture", self.concurrency)
        self.assertIn("cycle-scoped design assumption", self.debugging)


if __name__ == "__main__":
    unittest.main()
