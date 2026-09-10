from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    body = text[start + len(heading):]
    pos = body.find("\n## ")
    return body if pos < 0 else body[:pos]


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

    def test_protocol61_identity_preserves_516_quality_lineage(self) -> None:
        self.assertEqual("6.1.0", read("source/PROTOCOL_VERSION").strip())
        versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.assertIn("protocol 5.16 is a backward-compatible", versioning)
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", versioning)
        self.assertIn("d1 scientific-formulation", self.workflow)
        self.assertIn("d2 numerical-algorithm-design", self.workflow)
        self.assertIn("software-design -> software-implementation", self.workflow)
        self.assertIn("not a third lifecycle role", self.workflow)

    def test_final_acceptance_precedes_independent_review(self) -> None:
        typical = self.workflow[self.workflow.index("## typical workflows"):self.workflow.index("## workplans as bounded implementation contracts")]
        final_accept = typical.index("final affected regression + integration")
        review = typical.index("independent review")
        self.assertLess(final_accept, review)
        self.assertIn("review readiness", self.testing)
        self.assertIn("final complete affected-surface regression", self.testing)

    def test_quality_metrics_are_sensors_not_authority(self) -> None:
        for text in (self.health, self.arch):
            self.assertIn("sensor", text)
        combined = "\n".join((self.health, self.arch, self.testing, self.tools))
        self.assertIn("metrics are sensors", self.health)
        self.assertIn("do not require 100% mutation", combined)
        self.assertIn("quality ratchet", self.health)
        self.assertIn("change frequency", self.health)
        self.assertIn("architectural centrality", self.health)

    def test_test_effectiveness_routes_are_conditional(self) -> None:
        for token in ("mutation", "differential", "metamorphic", "counterfactual"):
            self.assertIn(token, self.testing)
        self.assertIn("test effectiveness", self.tools)
        self.assertIn("changed-code", self.tools)
        self.assertIn("architecture", self.tools)
        self.assertIn("longitudinal", self.tools)
        self.assertIn("not a universal test stage", self.testing)

    def test_scientific_evidence_names_differential_and_metamorphic_relations(self) -> None:
        self.assertIn("differential", self.science)
        self.assertIn("metamorphic", self.science)
        for token in ("restart", "permutation", "symmetry", "backend"):
            self.assertIn(token, self.science)

    def test_python_static_correctness_has_first_class_vendor_neutral_route(self) -> None:
        block = section(self.python, "## fast static correctness")

        def assert_semantics(candidate: str) -> None:
            self.assertIn("project's configured fast lint/type/static checks", candidate)
            self.assertIn("high-information evidence", candidate)
            self.assertIn("not product truth", candidate)
            self.assertIn("do not introduce a second type/schema system", candidate)

        assert_semantics(block)
        vendor_substituted = (
            block.replace("ruff", "lint-tool-example")
            .replace("pyright", "type-tool-example-a")
            .replace("mypy", "type-tool-example-b")
        )
        assert_semantics(vendor_substituted)

        route_removed = block.replace("project's configured fast lint/type/static checks", "project checks")
        with self.assertRaises(AssertionError):
            assert_semantics(route_removed)

    def test_failure_injection_is_bounded_and_real_owner_preserving(self) -> None:
        self.assertIn("bounded failure", self.testing)
        self.assertIn("real semantic owner", self.testing)
        self.assertIn("resource exhaustion", self.testing)
        self.assertIn("stateful restart", self.scenarios)

    def test_stabilization_is_non_mutating_and_risk_triggered(self) -> None:
        self.assertIn("stabilization", self.health)
        self.assertIn("non-mutating", self.health)
        self.assertIn("normal design", self.health)
        self.assertIn("verification", self.health)
        self.assertIn("risk-triggered", self.health)

    def test_maintenance_audit_is_non_authoritative_and_truthful_about_history(self) -> None:
        for token in ("health audit", "churn", "change coupling", "history", "healthy", "watch", "action required"):
            self.assertIn(token, self.audit)
        self.assertIn("do not fabricate", self.audit)
        self.assertIn("do not define new product requirements", self.audit)
        self.assertIn("software-design", self.audit)
        self.assertIn("software-implementation", self.audit)
        self.assertIn("repository-hygiene", self.audit)
        self.assertIn("software-documentation", self.audit)

    def test_behavioral_scenarios_cover_anti_entropy_counterfactuals(self) -> None:
        for heading in (
            "duplicate authoritative representations",
            "fallback accumulation",
            "high coverage, weak oracle",
            "objective dependency invariant",
            "static complexity versus change-sensitive risk",
            "trivial local change",
            "stateful restart or recovery defect",
            "missing repository history",
            "execution stage performs work instead of returning instructions",
            "mixed-stage request preserves mutation boundaries",
        ):
            self.assertIn(heading, self.scenarios)


if __name__ == "__main__":
    unittest.main()
