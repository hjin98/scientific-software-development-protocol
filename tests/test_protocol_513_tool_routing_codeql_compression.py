from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def lower(path: str) -> str:
    return read(path).lower()


class Protocol513RoutingPreservationTests(unittest.TestCase):
    """Protocol 5.13 relation-first routing remains a capability under 6.2 hierarchical disclosure."""

    def setUp(self) -> None:
        self.design = lower("source/roles/software-design/SKILL.md")
        self.implementation = lower("source/roles/software-implementation/SKILL.md")
        self.common = lower("source/shared/references/tool-assisted-engineering.md")
        self.codeql = lower("source/shared/references/tool-codeql.md")
        self.workflow = lower("source/shared/references/workflow-and-workplans.md")
        self.convergence = lower("source/shared/references/convergence-and-cycle-economy.md")

    def test_513_514_history_is_preserved_as_capability_lineage(self) -> None:
        versioning = lower("source/shared/references/protocol-versioning-and-compatibility.md")
        self.assertIn("5.13", versioning)
        self.assertIn("relation-first tool routing", versioning)
        self.assertIn("5.14", versioning)
        self.assertIn("active simplicity", versioning)

    def test_dispatch_remains_per_question_relation_first_via_one_common_router(self) -> None:
        for text in (self.design, self.implementation):
            self.assertIn("tool-assisted-engineering.md", text)
            self.assertIn("relation", text)
            for ref in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
                self.assertNotIn(f"references/{ref}", text)
        for phrase in (
            "relation under the current material claim",
            "literal/path/text",
            "minimum set of capabilities",
            "cheap",
            "fallback",
        ):
            self.assertIn(phrase, self.common)
        for ref in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
            self.assertIn(ref, self.common)

    def test_specialized_trigger_keeps_non_silent_disposition(self) -> None:
        for phrase in ("capability", "available", "supported", "fallback", "built-in"):
            self.assertIn(phrase, self.common)
        self.assertIn("tool absence", self.common)
        self.assertIn("does not weaken", self.common)

    def test_relation_first_common_router_and_optional_tools_remain(self) -> None:
        for phrase in (
            "relation under the current material claim",
            "security task is not automatically a codeql task",
            "forbidden-call pattern is structural",
            "decompose",
            "minimum set of capabilities",
        ):
            self.assertIn(phrase, self.common)
        self.assertIn("mandatory three-tool pipeline", self.common)

    def test_codeql_provenance_and_optional_status_remain(self) -> None:
        for phrase in (
            "optional specialist analyzer, not a generic security gate",
            "local/external codeql execution",
            "github-managed codeql execution",
            "github code-scanning result/alert surface",
            "not automatically independent execution evidence",
            "zero findings are not proof of absence outside that contract",
        ):
            self.assertIn(phrase, self.codeql)

    def test_recurrence_and_convergence_remain_conditional_owned_doctrine(self) -> None:
        self.assertIn("convergence-and-cycle-economy.md", self.workflow)
        self.assertIn("recurrence", self.workflow)
        self.assertIn("semantic defect families", self.convergence)
        self.assertIn("active simplification trigger", self.convergence)
        self.assertIn("revision economy", self.convergence)
        self.assertIn("acceptance", self.convergence)


if __name__ == "__main__":
    unittest.main()
