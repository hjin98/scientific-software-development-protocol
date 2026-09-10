from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProxyProofAcceptanceContractTests(unittest.TestCase):
    """Preserve Protocol 5.6 proxy-proof acceptance through Protocol 6.2 canonical ownership."""

    def test_testing_reference_is_canonical_proxy_proof_owner(self) -> None:
        text = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "proxy-proof real-owner evidence",
            "real semantic owner/path",
            "allowed test-double boundary below/outside it",
            "ask whether evidence could remain green while that owner is materially broken",
            "it cannot close that owner claim",
            "this is not a blanket mock ban",
        ):
            self.assertIn(phrase, text)

    def test_historical_proxy_substitutions_remain_rejected_semantically(self) -> None:
        text = read("source/shared/references/testing-and-validation.md").lower()
        for phrase in (
            "mocking/reimplementing the owner",
            "calling a downstream helper when production routing is part of the claim",
            "seeding post-decision state when the decision is under test",
            "replacing durable persistence when restart/persistence is the claim",
            "helper-generated results when production construction/routing is the behavior being verified",
        ):
            self.assertIn(phrase, text)

    def test_bounded_fakes_below_real_owner_remain_valid(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("bounded deterministic doubles remain valid below/outside the owner", testing)
        self.assertIn("external services, hardware, expensive data/training, or nondeterminism", testing)
        self.assertIn("test doubles may control dependencies below/outside the owner", implementation)
        self.assertIn("production scale is needed only when production-scale behavior/resource qualification is itself the claim", testing)

    def test_unavailable_required_owner_boundary_is_not_proxy_passed(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("mark the claim unavailable/blocking", testing)
        self.assertIn("report unavailable/blocking rather than proxy-passing it", implementation)

    def test_entrypoints_route_proxy_proof_to_testing_owner(self) -> None:
        design = read("source/roles/software-design/SKILL.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        for text in (design, implementation):
            self.assertIn("references/testing-and-validation.md", text)
            self.assertIn("proxy-proof", text)
        self.assertIn("real semantic-owner/consumer boundaries", design)
        self.assertIn("real semantic owner/path", implementation)
        self.assertIn("could remain green while that owner is broken", implementation)

    def test_workplan_records_real_owner_boundary_only_when_material(self) -> None:
        template = read("source/shared/templates/implementation_workplan_template.md").lower()
        self.assertIn("real semantic-owner/consumer boundary, allowed doubles and forbidden proxy substitutions when material", template)
        self.assertIn("integration/end-to-end through real owner/consumer boundaries", template)
        self.assertIn("known shortcut that could appear green while defeating the outcome", template)

    def test_delegated_owner_replacement_remaps_evidence_without_freezing_old_owner(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        implementation = read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("if delegated owner identity changes under equivalent semantics, remap/rerun owner-specific evidence rather than preserving the old owner", testing)
        self.assertIn("remap/rerun still-valid evidence specifications after owner replacement rather than preserving obsolete product machinery for the test", implementation)

    def test_structural_guardrails_are_claim_triggered_not_global_frameworks(self) -> None:
        testing = read("source/shared/references/testing-and-validation.md").lower()
        self.assertIn("for removal/uniqueness/ownership/no-legacy-path claims", testing)
        self.assertIn("use source/structural negative assertions", testing)
        self.assertIn("do not build a universal architecture manifest solely for compliance", testing)


if __name__ == "__main__":
    unittest.main()
