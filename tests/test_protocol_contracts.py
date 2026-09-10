from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Protocol6ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = read("source/shared/references/abstraction-and-concretization.md").lower()
        self.workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        self.testing = read("source/shared/references/testing-and-validation.md").lower()
        self.d1 = read("source/shared/references/scientific-formulation.md").lower()
        self.d2 = read("source/shared/references/numerical-algorithm-design.md").lower()
        self.d3 = read("source/shared/references/architecture-and-design.md").lower()
        self.d4 = read("source/shared/references/specification-and-implementation.md").lower()
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()
        self.evolution = read("source/shared/references/evidence-evolution-and-dependencies.md").lower()

    def test_protocol_62_identity_and_four_domain_roles(self) -> None:
        self.assertEqual("6.2.0", read("source/PROTOCOL_VERSION").strip())
        self.assertIn("protocol 6.2", read("README.md").lower())
        for skill in ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation"):
            self.assertTrue((ROOT / f"source/roles/{skill}/SKILL.md").is_file(), skill)

    def test_recursive_concretization_feasibility_and_delegation_are_canonical(self) -> None:
        for phrase in (
            "fidelity is a feasibility condition",
            "domain engineering fitness",
            "minimum justified concretization complexity",
            "development economy",
            "layered directed acyclic graph",
            "does not acquire authority because it exists",
        ):
            self.assertIn(phrase, self.foundation)

    def test_protocol61_evidence_evolution_capabilities_remain_first_class(self) -> None:
        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "execution_depends_on"):
            self.assertIn(phrase, self.evolution)
        self.assertIn("absence of an edge", self.evolution)
        self.assertIn("stale", self.evolution)
        self.assertIn("common-mode", self.evolution)

    def test_authority_provenance_and_multiple_constraints_survive(self) -> None:
        self.assertIn("semantic level and authority provenance are independent", self.foundation)
        self.assertIn("safety", self.foundation)
        self.assertIn("stakeholder", self.foundation)
        self.assertIn("external contracts", self.foundation)
        self.assertIn("one current semantic owner", self.foundation)
        self.assertIn("several parents/side constraints", self.foundation)

    def test_d1_d2_d3_d4_ownership_is_separated(self) -> None:
        self.assertIn("scientific method paper", self.d1)
        self.assertIn("numerical & algorithmic method paper", self.d2)
        self.assertIn("architecture manual", self.d3)
        self.assertIn("accepted d4 specification", self.d4)
        self.assertIn("code/executable behavior", self.d4)

    def test_verification_is_reverse_semantic_and_checks_adequacy(self) -> None:
        self.assertIn("verification therefore is opposite-direction semantic reconstruction", self.foundation)
        self.assertIn("concretization fidelity", self.foundation)
        self.assertIn("abstraction adequacy", self.foundation)
        self.assertIn("composed scientific closure", self.testing)

    def test_authority_states_bounded_impact_and_challenge_survive(self) -> None:
        for phrase in ("proposed", "accepted-current", "challenged", "risk-accepted/provisional", "stale-dependent", "superseded/historical", "release-pinned/publication"):
            self.assertIn(phrase, self.foundation)
        self.assertIn("review only materially dependent descendants/evidence", self.foundation)
        self.assertIn("challenge pass", self.foundation)
        self.assertIn("serious challenge", self.foundation)
        self.assertIn("human adjudication", self.foundation)

    def test_lossless_representation_is_a_hard_current_contract(self) -> None:
        for phrase in (
            "lossless representation rule",
            "governed scope",
            "one detailed owner per generic rule",
            "use progressive disclosure",
            "keep cold paths discoverable",
            "weight attention without weakening acceptance",
            "do not deduplicate by adjudicating semantics",
            "keep derivatives subordinate",
        ):
            self.assertIn(phrase, self.foundation)

    def test_tests_and_code_cannot_counterfeit_authority(self) -> None:
        self.assertIn("evidence integrity", self.testing)
        self.assertIn("required check that did not execute is not a pass", self.testing)
        self.assertIn("rewrite", self.testing)
        self.assertIn("code does not become intended contract", self.d4)

    def test_stage_local_final_regression_and_proxy_proof_survive(self) -> None:
        self.assertIn("stage-local affected regression", self.testing)
        self.assertIn("final assembled acceptance", self.testing)
        self.assertIn("proxy-proof real-owner evidence", self.testing)
        self.assertIn("could the evidence remain green while the owner", self.testing)

    def test_active_simplicity_survives_without_machinery_preservation(self) -> None:
        for text in (self.d3, read("source/roles/software-implementation/SKILL.md").lower()):
            self.assertIn("remove", text)
            self.assertIn("consolidat", text)
        self.assertIn("before another additive durable repair", self.d3)

    def test_workflow_is_proportional_and_preserves_risk_and_impact(self) -> None:
        prompts = read("source/shared/references/development-workflow-prompts.md").lower()
        self.assertIn("change_plan may be none", prompts)
        self.assertIn("risk-accepted/provisional", prompts)
        self.assertIn("bounded impact closure", prompts)
        self.assertIn("reduced d4-only", prompts)
        self.assertIn("dependent descendants", self.workflow)
        self.assertIn("cannot close", self.workflow)

    def test_historical_recovery_is_immutable_and_not_silently_upgraded(self) -> None:
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", self.versioning)
        self.assertIn("6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2", self.versioning)
        self.assertIn("6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639", self.versioning)
        self.assertIn("never silently reinterprets older work", self.versioning)

    def test_build_registry_contains_four_roles_and_three_specialists(self) -> None:
        build = read("source/build_skills.py")
        for name in ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation", "software-documentation", "software-maintenance-audit", "repository-hygiene"):
            self.assertIn(f'"{name}"', build)


if __name__ == "__main__":
    unittest.main()
