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
    """Preserve Protocol 5.16 long-horizon quality capabilities under Protocol 6.2 ownership."""

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

    def test_protocol62_identity_preserves_516_quality_lineage(self) -> None:
        self.assertEqual("6.2.0", read("source/PROTOCOL_VERSION").strip())
        versioning = read("source/shared/references/protocol-versioning-and-compatibility.md")
        self.assertIn("protocol 6.2 is a backward-compatible representation/progressive-disclosure strengthening", versioning)
        self.assertIn("5.16 long-horizon health/verification/stabilization/maintenance audit/workflow prompts/public fallback", versioning)
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", versioning)
        self.assertIn("d1 scientific formulation -> d2 numerical method -> d3 architecture -> d4 specification/implementation", self.workflow)
        self.assertIn("supporting specialists", self.workflow)
        self.assertIn("non-authoritative capabilities, not approval stages", self.workflow)

    def test_final_acceptance_precedes_independent_review(self) -> None:
        self.assertIn("required stage-local affected regression cannot be deferred merely because a later full suite exists", self.workflow)
        self.assertIn("final assembled acceptance still reflects the candidate after all material executable edits", self.workflow)
        self.assertIn("missing required pre-review acceptance remains a blocker", self.workflow)
        self.assertIn("review readiness normally follows this acceptance", self.testing)
        self.assertIn("run complete affected regression after all material executable edits", self.testing)

    def test_quality_metrics_are_sensors_not_authority(self) -> None:
        self.assertIn("sensors, not verdicts", self.health)
        self.assertIn("no universal threshold is normative", self.health)
        self.assertIn("metrics are sensors, not architecture truth", self.arch)
        self.assertIn("quality ratchet", self.health)
        self.assertIn("change frequency", self.health)
        self.assertIn("architectural centrality", self.health)
        self.assertIn("mutation survival is investigation evidence, not a required score", self.health)

    def test_test_effectiveness_routes_are_conditional(self) -> None:
        for token in ("mutation", "differential", "metamorphic", "counterfactual"):
            self.assertIn(token, self.testing)
        self.assertIn("test effectiveness / oracle-strength relation", self.tools)
        self.assertIn("changed-code behavioral-protection relation", self.tools)
        self.assertIn("objective dependency/architecture-invariant relation", self.tools)
        self.assertIn("longitudinal maintenance-risk relation", self.tools)
        self.assertIn("these capability classes remain conditional and relation-first", self.tools)

    def test_scientific_evidence_names_differential_and_metamorphic_relations(self) -> None:
        self.assertIn("differential testing", self.science)
        self.assertIn("metamorphic testing", self.science)
        for token in ("restart/continuation", "permutation", "symmetry", "backend equivalence"):
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
        self.assertIn("bounded deterministic failure injection", self.testing)
        self.assertIn("keep the real recovery owner executing", self.testing)
        self.assertIn("prefer bounded simulation over resource exhaustion", self.testing)
        self.assertIn("bounded deterministic fault injection", self.health)
        self.assertIn("real owner remains live", self.health)
        self.assertIn("stateful restart", self.scenarios)

    def test_stabilization_is_non_mutating_and_risk_triggered(self) -> None:
        self.assertIn("at a material convergence boundary after ordinary review otherwise passes", self.health)
        self.assertIn("stabilization is non-mutating", self.health)
        self.assertIn("required changes return through the normal owner", self.health)
        self.assertIn("deeper optional risk-triggered falsification mode", self.health)

    def test_maintenance_audit_is_non_authoritative_and_truthful_about_history(self) -> None:
        for token in ("longitudinal sensing", "churn", "change coupling", "history", "healthy", "watch", "action required"):
            self.assertIn(token, self.audit)
        self.assertIn("if history is unavailable, do not infer trends from a static snapshot", self.audit)
        self.assertIn("do not redesign or broadly refactor inside the audit", self.audit)
        for owner in ("software-design", "software-implementation", "repository-hygiene", "software-documentation"):
            self.assertIn(owner, self.audit)

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
