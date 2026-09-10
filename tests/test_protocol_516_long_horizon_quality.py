from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class Protocol6LongHorizonQualityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = read("source/shared/references/workflow-and-workplans.md")
        self.testing = read("source/shared/references/testing-and-validation.md")
        self.arch = read("source/shared/references/architecture-and-design.md")
        self.health = read("source/shared/references/long-horizon-code-health.md")
        self.tools = read("source/shared/references/tool-assisted-engineering.md")
        self.python = read("source/shared/references/python-engineering.md")
        self.science = read("source/shared/references/scientific-software.md")
        self.audit = read("source/specialists/software-maintenance-audit/SKILL.md")
        self.scenarios = read("qualification/long-horizon/SCENARIOS.md")

    def test_516_lineage_survives_under_protocol62(self) -> None:
        self.assertEqual("6.2.0", read("source/PROTOCOL_VERSION").strip())
        versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.assertIn("5.16", versioning)
        self.assertIn("long-horizon", versioning)
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", versioning)
        self.assertIn("d1", self.workflow)
        self.assertIn("d2", self.workflow)
        self.assertIn("d3", self.workflow)
        self.assertIn("d4", self.workflow)

    def test_final_acceptance_precedes_independent_review(self) -> None:
        self.assertIn("review readiness", self.testing)
        self.assertIn("final assembled acceptance", self.testing)
        self.assertIn("complete affected regression", self.testing)
        self.assertIn("independent review", self.workflow)

    def test_quality_metrics_are_sensors_not_authority(self) -> None:
        for text in (self.health, self.arch):
            self.assertIn("sensor", text)
        self.assertIn("metrics are sensors", self.health)
        self.assertIn("quality ratchet", self.health)
        self.assertIn("change frequency", self.health)
        self.assertIn("architectural centrality", self.health)
        self.assertIn("mutation", self.testing)

    def test_test_effectiveness_routes_are_conditional(self) -> None:
        for token in ("mutation", "differential", "metamorphic", "counterfactual"):
            self.assertIn(token, self.testing)
        self.assertIn("test effectiveness", self.tools)
        self.assertIn("not a universal", self.testing)

    def test_scientific_evidence_retains_differential_and_metamorphic_relations(self) -> None:
        self.assertIn("differential", self.science)
        self.assertIn("metamorphic", self.science)
        for token in ("restart", "permutation", "symmetry", "backend"):
            self.assertIn(token, self.science)

    def test_python_static_correctness_remains_vendor_neutral(self) -> None:
        for token in ("configured fast lint/type/static checks", "high-information evidence", "not product truth", "do not introduce a second type/schema system"):
            self.assertIn(token, self.python)

    def test_failure_injection_is_bounded_and_real_owner_preserving(self) -> None:
        self.assertIn("bounded deterministic failure injection", self.testing)
        self.assertIn("real recovery owner", self.testing)
        self.assertIn("resource exhaustion", self.testing)
        self.assertIn("stateful restart", self.scenarios)

    def test_stabilization_and_verification_remain_distinct_non_mutating_modes(self) -> None:
        self.assertIn("stabilization", self.health)
        self.assertIn("non-mutating", self.health)
        self.assertIn("verification", self.health)
        self.assertIn("risk-triggered", self.health)
        self.assertIn("normal design", self.health)

    def test_maintenance_audit_is_non_authoritative_and_truthful_about_history(self) -> None:
        for token in ("health audit", "churn", "change coupling", "history", "action required"):
            self.assertIn(token, self.audit)
        self.assertIn("do not fabricate", self.audit)
        self.assertIn("does not own", self.audit)
        for owner in ("software-design", "software-implementation", "repository-hygiene", "software-documentation"):
            self.assertIn(owner, self.audit)

    def test_behavioral_scenarios_still_cover_anti_entropy_counterfactuals(self) -> None:
        for heading in ("duplicate authoritative representations", "fallback accumulation", "high coverage, weak oracle", "objective dependency invariant", "static complexity versus change-sensitive risk", "trivial local change", "stateful restart or recovery defect", "missing repository history", "execution stage performs work instead of returning instructions", "mixed-stage request preserves mutation boundaries"):
            self.assertIn(heading, self.scenarios)


if __name__ == "__main__":
    unittest.main()
