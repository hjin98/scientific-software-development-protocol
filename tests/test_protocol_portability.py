from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
HIERARCHY = "product engineering fitness > minimum justified product/system complexity > development economy"
LINK_RE = re.compile(r"\[[^\]]+\]\((references/[A-Za-z0-9_.-]+\.md)\)")

ROLE_513 = {
    "convergence-and-cycle-economy.md",
    "tool-assisted-engineering.md",
    "tool-serena.md",
    "tool-semgrep.md",
    "tool-hypothesis.md",
    "tool-codeql.md",
}
ROLE_515 = {
    "language-profiles.md",
    "python-engineering.md",
    "cpp-engineering.md",
}
ROLE_516 = {"long-horizon-code-health.md"}

EXPECTED_REFERENCES = {
    "roles/software-design": {
        "workflow-and-workplans.md", "testing-and-validation.md", "protocol-versioning-and-compatibility.md",
        "architecture-and-design.md", "documentation-and-evidence.md", "specification-and-implementation.md",
        "release-and-distribution.md", "repository-intake.md",
        "configuration-and-policy.md", "concurrency-and-orchestration.md", "security-and-trust-boundaries.md",
        "performance-and-parallelism.md", "storage-and-io.md", "scientific-software.md",
    } | ROLE_513 | ROLE_515 | ROLE_516,
    "roles/software-implementation": {
        "workflow-and-workplans.md", "testing-and-validation.md", "protocol-versioning-and-compatibility.md",
        "architecture-and-design.md", "debugging-and-state-recovery.md", "documentation-and-evidence.md",
        "specification-and-implementation.md", "release-and-distribution.md", "repository-intake.md",
        "git-and-version-control.md", "configuration-and-policy.md",
        "concurrency-and-orchestration.md", "security-and-trust-boundaries.md", "performance-and-parallelism.md",
        "storage-and-io.md", "scientific-software.md",
    } | ROLE_513 | ROLE_515 | ROLE_516,
    "specialists/software-documentation": {
        "workflow-and-workplans.md", "testing-and-validation.md", "protocol-versioning-and-compatibility.md",
        "architecture-and-design.md", "documentation-and-evidence.md", "documentation-maintenance.md",
        "scientific-technical-writing.md", "specification-and-implementation.md", "release-and-distribution.md",
        "security-and-trust-boundaries.md", "performance-and-parallelism.md", "storage-and-io.md", "scientific-software.md",
    },
    "specialists/repository-hygiene": {
        "workflow-and-workplans.md", "testing-and-validation.md", "protocol-versioning-and-compatibility.md",
        "git-and-version-control.md", "documentation-and-evidence.md", "release-and-distribution.md",
        "repository-intake.md", "security-and-trust-boundaries.md", "storage-and-io.md",
    },
    "specialists/software-maintenance-audit": {
        "workflow-and-workplans.md", "testing-and-validation.md", "protocol-versioning-and-compatibility.md",
        "long-horizon-code-health.md", "architecture-and-design.md", "git-and-version-control.md",
        "repository-intake.md", "tool-assisted-engineering.md", "convergence-and-cycle-economy.md",
        "documentation-and-evidence.md", "scientific-software.md",
    },
}


class ProtocolPortabilityTests(unittest.TestCase):
    def test_doctrine_hierarchy_remains_verbatim_in_lifecycle_entrypoints(self) -> None:
        for rel in ("roles/software-design", "roles/software-implementation"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(HIERARCHY, text, rel)

    def test_reference_sets_are_preserved_and_directly_linked(self) -> None:
        for rel, expected in EXPECTED_REFERENCES.items():
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertEqual(expected, linked, rel)

    def test_protocol_513_direct_tool_refs_remain_lifecycle_only(self) -> None:
        for rel in ("roles/software-design", "roles/software-implementation"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertTrue(ROLE_513 <= linked)
        direct_tools = {"tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"}
        for rel in (
            "specialists/software-documentation",
            "specialists/repository-hygiene",
            "specialists/software-maintenance-audit",
        ):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertTrue(direct_tools.isdisjoint(linked))
        audit = (SOURCE / "specialists/software-maintenance-audit/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("](references/tool-assisted-engineering.md)", audit)

    def test_protocol_515_language_profiles_are_lifecycle_only(self) -> None:
        for rel in ("roles/software-design", "roles/software-implementation"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertTrue(ROLE_515 <= linked)
        for rel in (
            "specialists/software-documentation",
            "specialists/repository-hygiene",
            "specialists/software-maintenance-audit",
        ):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertTrue(ROLE_515.isdisjoint(linked))

    def test_protocol_516_long_horizon_reference_is_progressively_disclosed(self) -> None:
        for rel in ("roles/software-design", "roles/software-implementation", "specialists/software-maintenance-audit"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertIn("long-horizon-code-health.md", linked, rel)
        for rel in ("specialists/software-documentation", "specialists/repository-hygiene"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            linked = {Path(path).name for path in LINK_RE.findall(text)}
            self.assertNotIn("long-horizon-code-health.md", linked, rel)

    def test_language_profile_routes_are_mandatory_for_both_lifecycle_roles(self) -> None:
        for rel in ("roles/software-design", "roles/software-implementation"):
            text = (SOURCE / rel / "SKILL.md").read_text(encoding="utf-8")
            for path in (
                "references/language-profiles.md",
                "references/python-engineering.md",
                "references/cpp-engineering.md",
            ):
                line = next(line for line in text.splitlines() if f"]({path})" in line)
                self.assertIn("MUST read", line, (rel, path))

    def test_design_role_critical_routes_are_mandatory(self) -> None:
        text = (SOURCE / "roles/software-design/SKILL.md").read_text(encoding="utf-8")
        for path in (
            "references/workflow-and-workplans.md",
            "references/testing-and-validation.md",
            "references/architecture-and-design.md",
            "references/protocol-versioning-and-compatibility.md",
        ):
            line = next(line for line in text.splitlines() if f"]({path})" in line)
            self.assertIn("MUST read", line, path)

    def test_implementation_role_critical_routes_are_mandatory(self) -> None:
        text = (SOURCE / "roles/software-implementation/SKILL.md").read_text(encoding="utf-8")
        for path in (
            "references/workflow-and-workplans.md",
            "references/testing-and-validation.md",
            "references/architecture-and-design.md",
            "references/protocol-versioning-and-compatibility.md",
        ):
            line = next(line for line in text.splitlines() if f"]({path})" in line)
            self.assertIn("MUST read", line, path)

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
