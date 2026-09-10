from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402

LINK_RE = re.compile(r"\[[^\]]+\]\(((?:references|templates)/[A-Za-z0-9_.-]+\.md)\)")
TOOL_LEAVES = {"tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"}
LANGUAGE_LEAVES = {"python-engineering.md", "cpp-engineering.md"}


def links_for(kind: str, name: str) -> set[str]:
    parent = "roles" if kind == "role" else "specialists"
    text = (SOURCE / parent / name / "SKILL.md").read_text(encoding="utf-8")
    return set(LINK_RE.findall(text))


class ProtocolPortabilityTests(unittest.TestCase):
    def test_current_protocol_uses_abstraction_concretization_hierarchy(self) -> None:
        foundation = (SOURCE / "shared/references/abstraction-and-concretization.md").read_text(encoding="utf-8").lower()
        self.assertIn("domain engineering fitness", foundation)
        self.assertIn("minimum justified concretization complexity", foundation)
        self.assertIn("development economy", foundation)
        self.assertIn("fidelity is a feasibility condition", foundation)
        self.assertIn("lossless representation rule", foundation)

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

    def test_tool_leaf_routing_is_hierarchical(self) -> None:
        for role in ("software-design", "software-implementation"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertIn("tool-assisted-engineering.md", linked, role)
            self.assertTrue(TOOL_LEAVES.isdisjoint(linked), role)

        router = (SOURCE / "shared/references/tool-assisted-engineering.md").read_text(encoding="utf-8")
        for leaf in TOOL_LEAVES:
            self.assertIn(leaf, router)

        for role in ("scientific-formulation", "numerical-algorithm-design"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(TOOL_LEAVES.isdisjoint(linked), role)
        for specialist in ("software-documentation", "repository-hygiene"):
            linked = {Path(path).name for path in links_for("specialist", specialist)}
            self.assertTrue(TOOL_LEAVES.isdisjoint(linked), specialist)
        self.assertIn("references/tool-assisted-engineering.md", links_for("specialist", "software-maintenance-audit"))

    def test_language_leaf_routing_is_hierarchical(self) -> None:
        for role in ("software-design", "software-implementation"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertIn("language-profiles.md", linked, role)
            self.assertTrue(LANGUAGE_LEAVES.isdisjoint(linked), role)

        router = (SOURCE / "shared/references/language-profiles.md").read_text(encoding="utf-8")
        for leaf in LANGUAGE_LEAVES:
            self.assertIn(leaf, router)
        self.assertIn("python-only", router.lower())
        self.assertIn("c++-only", router.lower())

        for role in ("scientific-formulation", "numerical-algorithm-design"):
            linked = {Path(path).name for path in links_for("role", role)}
            self.assertTrue(LANGUAGE_LEAVES.isdisjoint(linked), role)
        for specialist in build_skills.SPECIALIST_SPECS:
            linked = {Path(path).name for path in links_for("specialist", specialist)}
            self.assertTrue(LANGUAGE_LEAVES.isdisjoint(linked), specialist)

    def test_root_role_baseline_and_concern_routes_are_explicit(self) -> None:
        for role, owner in (
            ("software-design", "references/architecture-and-design.md"),
            ("software-implementation", "references/specification-and-implementation.md"),
        ):
            text = (SOURCE / "roles" / role / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("references/abstraction-and-concretization.md", text)
            self.assertIn(owner, text)
            self.assertIn("references/workflow-and-workplans.md", text)
            self.assertIn("references/testing-and-validation.md", text)
            self.assertIn("load only", text.lower())
            self.assertIn("package membership", text.lower())

    def test_new_authority_roles_package_their_domain_documents(self) -> None:
        d1 = links_for("role", "scientific-formulation")
        d2 = links_for("role", "numerical-algorithm-design")
        self.assertIn("references/scientific-formulation.md", d1)
        self.assertIn("templates/scientific_method_paper_template.md", d1)
        self.assertIn("references/numerical-algorithm-design.md", d2)
        self.assertIn("templates/numerical_algorithmic_method_paper_template.md", d2)
        self.assertIn("templates/abstraction_concretization_change_plan_template.md", d1)
        self.assertIn("templates/abstraction_concretization_change_plan_template.md", d2)
        self.assertNotIn("templates/abstraction_concretization_change_plan_template.md", links_for("role", "software-design"))

    def test_transitive_transport_keeps_conditional_leaves_reachable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "dist"
            subprocess.run(
                [sys.executable, str(SOURCE / "build_skills.py"), "--output", str(out)],
                cwd=ROOT,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for role in ("software-design", "software-implementation"):
                refs = {p.name for p in (out / "skills" / role / "references").iterdir() if p.is_file()}
                self.assertTrue(LANGUAGE_LEAVES <= refs, (role, sorted(LANGUAGE_LEAVES - refs)))
                self.assertTrue(TOOL_LEAVES <= refs, (role, sorted(TOOL_LEAVES - refs)))

    def test_historical_516_resolution_is_explicit(self) -> None:
        versioning = (SOURCE / "shared/references/protocol-versioning-and-compatibility.md").read_text(encoding="utf-8").lower()
        self.assertIn("5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3", versioning)
        self.assertIn("sdp-protocol-5.16", versioning)
        self.assertIn("schema", versioning)

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
