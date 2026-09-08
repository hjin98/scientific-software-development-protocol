from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Protocol6ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = read("source/shared/references/abstraction-and-realization.md").lower()
        self.workflow = read("source/shared/references/workflow-and-workplans.md").lower()
        self.testing = read("source/shared/references/testing-and-validation.md").lower()
        self.d1 = read("source/shared/references/scientific-formulation.md").lower()
        self.d2 = read("source/shared/references/numerical-algorithm-design.md").lower()
        self.d3 = read("source/shared/references/architecture-and-design.md").lower()
        self.d4 = read("source/shared/references/specification-and-implementation.md").lower()
        self.versioning = read("source/shared/references/protocol-versioning-and-compatibility.md").lower()

    def test_protocol_60_identity_and_four_domain_roles(self) -> None:
        self.assertEqual("6.0.0", read("source/PROTOCOL_VERSION").strip())
        self.assertIn("current protocol version: **6.0**", read("README.md").lower())
        for skill in ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation"):
            self.assertTrue((ROOT / f"source/roles/{skill}/SKILL.md").is_file(), skill)

    def test_recursive_abstraction_realization_and_feasibility_are_canonical(self) -> None:
        self.assertIn("abstraction  --design / constrain-->  realization", self.foundation)
        self.assertIn("fidelity is a feasibility condition", self.foundation)
        self.assertIn("domain engineering fitness", self.foundation)
        self.assertIn("minimum justified realization complexity", self.foundation)

    def test_authority_provenance_is_orthogonal_to_domain_level(self) -> None:
        self.assertIn("authority source is orthogonal to abstraction level", self.foundation)
        self.assertIn("safety / explicit stakeholder and project authority / governed external contracts", self.foundation)
        self.assertIn("do not force every external requirement through d1", self.foundation)

    def test_d1_d2_d3_d4_ownership_is_separated(self) -> None:
        self.assertIn("scientific method paper", self.d1)
        self.assertIn("numerical & algorithmic method paper", self.d2)
        self.assertIn("d3 boundary", self.d3)
        self.assertIn("accepted d4 specification", self.d4)
        self.assertIn("code/executable behavior is the realization", self.d4)

    def test_verification_is_reverse_semantic_not_bijective_inverse(self) -> None:
        self.assertIn("verification therefore is not a mathematical inverse", self.foundation)
        self.assertIn("realization fidelity", self.foundation)
        self.assertIn("abstraction adequacy", self.foundation)
        self.assertIn("composed end-to-end scientific closure", self.testing)

    def test_authority_states_and_bounded_invalidation_exist(self) -> None:
        for phrase in ("proposed", "accepted current", "challenged", "stale dependent", "superseded/historical", "release-pinned/publication"):
            self.assertIn(phrase, self.foundation)
        self.assertIn("invalidates only descendants/evidence whose claim could materially change", self.foundation)

    def test_serious_challenge_is_mandatory_material_review_semantics(self) -> None:
        self.assertIn("mandatory bounded challenge pass", self.foundation)
        self.assertIn("serious challenge", self.foundation)
        self.assertIn("human adjudication", self.foundation)
        self.assertIn("serious challenge", self.workflow)
        self.assertIn("truth", self.foundation)

    def test_tests_and_code_cannot_counterfeit_authority(self) -> None:
        self.assertIn("evidence integrity", self.testing)
        self.assertIn("rewriting specification", self.testing)
        self.assertIn("required check that did not execute is not a pass", self.testing)
        self.assertIn("code does not become the intended contract", self.d4)

    def test_stage_local_final_regression_and_proxy_proof_survive(self) -> None:
        self.assertIn("stage-local regression", self.testing)
        self.assertIn("final assembled acceptance", self.testing)
        self.assertIn("proxy-proof semantic-owner evidence", self.testing)
        self.assertIn("real semantic owner", self.testing)

    def test_active_simplicity_survives_without_machinery_preservation(self) -> None:
        for text in (self.d3, read("source/roles/software-implementation/SKILL.md").lower()):
            self.assertIn("remove", text)
            self.assertIn("consolidat", text)
        self.assertIn("before another additive durable repair", self.d3)

    def test_historical_516_is_immutable_and_not_silently_upgraded(self) -> None:
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", self.versioning)
        self.assertIn("do not reinterpret active or completed 5.x work using protocol 6", self.versioning)

    def test_build_registry_contains_four_roles_and_three_specialists(self) -> None:
        build = read("source/build_skills.py")
        for name in ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation", "software-documentation", "software-maintenance-audit", "repository-hygiene"):
            self.assertIn(f'"{name}"', build)


if __name__ == "__main__":
    unittest.main()
