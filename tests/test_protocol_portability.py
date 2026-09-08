from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402

LINK_RE = re.compile(r"\[[^\]]+\]\(((?:references|templates)/[A-Za-z0-9_.-]+\.md)\)")
DIRECT_TOOLS = {"tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"}
LANGUAGE_PROFILES = {"language-profiles.md", "python-engineering.md", "cpp-engineering.md"}


def links_for(kind: str, name: str) -> set[str]:
    parent = "roles" if kind == "role" else "specialists"
    text = (SOURCE / parent / name / "SKILL.md").read_text(encoding="utf-8")
    return set(LINK_RE.findall(text))


class ProtocolPortabilityTests(unittest.TestCase):
    def test_current_protocol_uses_abstraction_realization_hierarchy(self) -> None:
        foundation = (SOURCE / "shared/references/abstraction-and-realization.md").read_text(encoding="utf-8").lower()
        self.assertIn("domain engineering fitness", foundation)
        self.assertIn("minimum justified realization complexity", foundation)
        self.assertIn("development economy", foundation)
        self.assertIn("fidelity is a feasibility condition", foundation)

    def test_registry_resources_are_exactly_directly_linked(self) -> None:
        for name, spec in build_skills.ROLE_SPECS.items():
            expected = {f"references/{ref}" for ref in spec["references"]} | {
                f"templates/{template}" for template in spec["templates"]
            }
            self.assertEqual(expected, links_for("role", name), name)
        for name, spec in build_skills.SPECIALIST_SPECS.items():
            expected = {f"references/{ref}" for ref in spec["references"]} | {
                f"templates/{template}" for template in spec["templates"]
            }
            self.assertEqual(expected, links_for("specialist", name), name)

    def test_direct_software_tool_routes_remain_d3_d4_only(self) -> None:
        for role in ("software-design", "software-implementation"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(DIRECT_TOOLS <= linked, role)
            self.assertIn("tool-assisted-engineering.md", linked, role)

        for role in ("scientific-formulation", "numerical-algorithm-design"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(DIRECT_TOOLS.isdisjoint(linked), role)

        for specialist in ("software-documentation", "repository-hygiene", "software-maintenance-audit"):
            linked = {Path(path).name for path in links_for("specialist", specialist)}
            self.assertTrue(DIRECT_TOOLS.isdisjoint(linked), specialist)
        self.assertIn(
            "references/tool-assisted-engineering.md",
            links_for("specialist", "software-maintenance-audit"),
        )

    def test_language_profiles_remain_d3_d4_execution_routes(self) -> None:
        for role in ("software-design", "software-implementation"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(LANGUAGE_PROFILES <= linked, role)
        for role in ("scientific-formulation", "numerical-algorithm-design"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(LANGUAGE_PROFILES.isdisjoint(linked), role)
        for specialist in build_skills.SPECIALIST_SPECS:
            linked = {Path(path).name for path in links_for("specialist", specialist)}
            self.assertTrue(LANGUAGE_PROFILES.isdisjoint(linked), specialist)

    def test_language_profile_routes_are_mandatory_for_d3_d4(self) -> None:
        for role in ("software-design", "software-implementation"):
            text = (SOURCE / "roles" / role / "SKILL.md").read_text(encoding="utf-8")
            for path in (
                "references/language-profiles.md",
                "references/python-engineering.md",
                "references/cpp-engineering.md",
            ):
                line = next(line for line in text.splitlines() if f"]({path})" in line)
                self.assertIn("MUST read", line, (role, path))

    def test_role_critical_routes_are_mandatory_for_d3_d4(self) -> None:
        for role in ("software-design", "software-implementation"):
            text = (SOURCE / "roles" / role / "SKILL.md").read_text(encoding="utf-8")
            for path in (
                "references/abstraction-and-realization.md",
                "references/workflow-and-workplans.md",
                "references/testing-and-validation.md",
                "references/architecture-and-design.md",
                "references/protocol-versioning-and-compatibility.md",
            ):
                line = next(line for line in text.splitlines() if f"]({path})" in line)
                self.assertIn("MUST read", line, (role, path))

    def test_new_authority_roles_package_their_domain_documents(self) -> None:
        d1 = links_for("role", "scientific-formulation")
        d2 = links_for("role", "numerical-algorithm-design")
        self.assertIn("references/scientific-formulation.md", d1)
        self.assertIn("templates/scientific_method_paper_template.md", d1)
        self.assertIn("references/numerical-algorithm-design.md", d2)
        self.assertIn("templates/numerical_algorithmic_method_paper_template.md", d2)
        self.assertIn("templates/abstraction_realization_change_plan_template.md", d1)
        self.assertIn("templates/abstraction_realization_change_plan_template.md", d2)
        self.assertNotIn("templates/abstraction_realization_change_plan_template.md", links_for("role", "software-design"))

    def test_historical_516_resolution_is_explicit(self) -> None:
        versioning = (SOURCE / "shared/references/protocol-versioning-and-compatibility.md").read_text(encoding="utf-8").lower()
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", versioning)
        self.assertIn("sdp-protocol-5.16", versioning)
        self.assertIn("profile schema v1", versioning)

    def test_sentinel_value_is_reference_only(self) -> None:
        root = ROOT / "qualification/reference-routing/protocol-routing-sentinel"
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        reference = (root / "references/sentinel.md").read_text(encoding="utf-8")
        token = re.search(r"`(PROTOCOL_ROUTING_REFERENCE_[0-9]+)`", reference)
        self.assertIsNotNone(token)
        self.assertNotIn(token.group(1), skill)
        self.assertIn("](references/sentinel.md)", skill)
        self.assertIn("MUST read", skill)


if __name__ == "__main__":
    unittest.main()
