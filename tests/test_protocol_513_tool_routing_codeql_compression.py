from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def lower(path: str) -> str:
    return read(path).lower()


class Protocol513RoutingPreservationTests(unittest.TestCase):
    """Preserve Protocol 5.13 tool-routing capability without freezing its old representation."""

    def setUp(self) -> None:
        self.design = lower("source/roles/software-design/SKILL.md")
        self.implementation = lower("source/roles/software-implementation/SKILL.md")
        self.common = lower("source/shared/references/tool-assisted-engineering.md")
        self.codeql = lower("source/shared/references/tool-codeql.md")
        self.workflow = lower("source/shared/references/workflow-and-workplans.md")
        self.convergence = lower("source/shared/references/convergence-and-cycle-economy.md")

    def test_513_history_is_preserved_without_owning_current_version(self) -> None:
        versioning = lower("source/shared/references/protocol-versioning-and-compatibility.md")
        self.assertIn("5.13 deterministic tool entry/codeql/progressive disclosure", versioning)
        self.assertIn("5.14 solution-boundary/active simplicity", versioning)

    def test_dispatch_remains_per_question_relation_first_via_concern_router(self) -> None:
        for text in (self.design, self.implementation):
            self.assertIn("references/tool-assisted-engineering.md", text)
            self.assertIn("relation", text)
            for ref in ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md"):
                self.assertNotIn(f"references/{ref}", text)

        for phrase in (
            "relation under the current material claim",
            "literal/path/text relation -> ordinary repository search/read",
            "symbol owner/definition/reference/caller relation -> serena",
            "ast/syntax/structural relation -> semgrep",
            "broad python input/state invariant -> hypothesis",
            "interprocedural flow/taint/source-to-sink relation -> codeql",
        ):
            self.assertIn(phrase, self.common)

    def test_specialized_trigger_keeps_non_silent_disposition(self) -> None:
        self.assertIn("cheap read-only/non-mutating capability probe", self.common)
        self.assertIn("available, current, supported, and directly models the claim", self.common)
        self.assertIn("presumptively use it", self.common)
        self.assertIn("fall back for a concrete reason", self.common)
        self.assertIn("familiarity with grep/read/shell/tests is not itself a fallback reason", self.common)

    def test_relation_first_common_router_and_optional_tools_remain(self) -> None:
        for phrase in (
            "relation under the current material claim",
            "security task is not automatically a codeql task",
            "forbidden-call pattern is structural",
            "decompose a multi-relation claim",
            "minimum set of capabilities",
        ):
            self.assertIn(phrase, self.common)
        self.assertIn("without becoming a **mandatory three-tool pipeline**", read("source/shared/references/tool-assisted-engineering.md"))

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

    def test_convergence_remains_conditionally_loaded_and_canonically_owned(self) -> None:
        self.assertIn("first clean local defect remains local", self.workflow)
        self.assertIn("material sibling recurrence", self.workflow)
        self.assertIn("convergence-and-cycle-economy.md", self.workflow)
        self.assertIn("semantic defect families", self.convergence)
        self.assertIn("active simplification trigger", self.convergence)
        self.assertIn("revision economy", self.convergence)
        self.assertIn("no recurrence count, review count, cycle budget, or convergence target can force acceptance", self.convergence)


if __name__ == "__main__":
    unittest.main()
