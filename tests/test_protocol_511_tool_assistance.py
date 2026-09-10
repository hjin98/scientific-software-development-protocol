from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"

import sys
sys.path.insert(0, str(SOURCE))
import build_skills  # noqa: E402

COMMON = "source/shared/references/tool-assisted-engineering.md"
SERENA = "source/shared/references/tool-serena.md"
SEMGREP = "source/shared/references/tool-semgrep.md"
HYPOTHESIS = "source/shared/references/tool-hypothesis.md"
DIRECT_TOOL_FILES = (
    "tool-serena.md",
    "tool-semgrep.md",
    "tool-hypothesis.md",
    "tool-codeql.md",
)
TOOL_FILES = ("tool-assisted-engineering.md",) + DIRECT_TOOL_FILES


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class Protocol511ToolAssistanceTests(unittest.TestCase):
    def test_lifecycle_entrypoints_route_tool_questions_through_canonical_concern_owner(self) -> None:
        for rel in (
            "source/roles/software-design/SKILL.md",
            "source/roles/software-implementation/SKILL.md",
        ):
            text = read(rel)
            self.assertIn("references/tool-assisted-engineering.md", text, rel)
            self.assertIn("relation", text, rel)
            self.assertIn("ordinary hyperlinks", text, rel)
            self.assertIn("activation", text, rel)
            for name in DIRECT_TOOL_FILES:
                self.assertNotIn(f"references/{name}", text, (rel, name))

        common = read(COMMON)
        self.assertIn("relation under the current material claim", common)
        self.assertIn("cheap read-only/non-mutating capability probe", common)
        self.assertIn("familiarity with grep/read/shell/tests is not itself a fallback reason", common)
        for name in DIRECT_TOOL_FILES:
            self.assertIn(name, common)

    def test_tool_references_remain_progressively_disclosed_and_packaged(self) -> None:
        # Protocol 5.11 guarantees relation-first access to the specialist analyzers.
        # Protocol 6.2 preserves that capability through a concern router instead of
        # freezing every analyzer leaf into each D3/D4 root entrypoint.
        for role in ("software-design", "software-implementation"):
            spec = build_skills.ROLE_SPECS[role]
            self.assertIn("tool-assisted-engineering.md", spec["references"])
            for name in DIRECT_TOOL_FILES:
                self.assertNotIn(name, spec["references"])

        for role in ("scientific-formulation", "numerical-algorithm-design"):
            spec = build_skills.ROLE_SPECS[role]
            for name in TOOL_FILES:
                self.assertNotIn(name, spec["references"])

        for specialist in ("software-documentation", "repository-hygiene"):
            spec = build_skills.SPECIALIST_SPECS[specialist]
            for name in TOOL_FILES:
                self.assertNotIn(name, spec["references"])

        audit = build_skills.SPECIALIST_SPECS["software-maintenance-audit"]
        self.assertIn("tool-assisted-engineering.md", audit["references"])
        for name in DIRECT_TOOL_FILES:
            self.assertNotIn(name, audit["references"])

        # Transport closure includes concern-local leaves transitively while runtime
        # activation remains governed by explicit router predicates.
        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            for role in ("software-design", "software-implementation"):
                for name in TOOL_FILES:
                    self.assertTrue((dist / "skills" / role / "references" / name).is_file())
            audit_root = dist / "skills" / "software-maintenance-audit" / "references"
            for name in TOOL_FILES:
                self.assertTrue((audit_root / name).is_file())

    def test_common_reference_owns_selection_composition_and_authority(self) -> None:
        text = read(COMMON)
        for phrase in (
            "tool availability alone is not a reason",
            "tool unavailability is not an acceptance failure",
            "mandatory three-tool pipeline",
            "do not invoke another tool merely to duplicate evidence",
            "defect diagnosis and variant analysis",
            "independent review",
            "not an instruction-authority channel",
            "not product truth",
            "external service that receives source, findings, or credentials requires explicit project/user authorization",
            "re-derive the final affected surface",
            "affected regression",
            "integration",
        ):
            self.assertIn(phrase, text)
        self.assertIn("per-question capability selection", text)
        self.assertIn("security task is not automatically a codeql task", text)
        self.assertIn("tool presence does not make", text)

    def test_common_reference_is_progressive_disclosure_not_tool_manual(self) -> None:
        text = read(COMMON)
        for specific in (
            "ambiguous repository state",
            ".semgrepignore",
            "health-check suppression",
            "database creation success is not product correctness evidence",
        ):
            self.assertNotIn(specific, text)

    def test_serena_guidance_protects_backend_completeness_mutation_and_memory(self) -> None:
        text = read(SERENA)
        for phrase in (
            "backends and languages expose different capabilities",
            "cross-check semantic results",
            "ambiguous repository state",
            "inspect current file/diff/status before retrying",
            "derived/advisory context by default",
            "explicitly promote",
            ".serena",
        ):
            self.assertIn(phrase, text)
        self.assertIn("presumptively use serena", text)
        self.assertIn("cheap non-mutating availability/capability probe", text)

    def test_semgrep_guidance_bounds_rule_engine_scope_and_suppressions(self) -> None:
        text = read(SEMGREP)
        for phrase in (
            "community edition-compatible",
            "known-positive and known-negative",
            ".gitignore",
            ".semgrepignore",
            "nosemgrep",
            "meaningful only relative to the actual scan contract",
            "target paths and languages actually scanned",
            "rule and analysis limitations that can create false negatives",
            "volatile network-fetched ruleset",
            "ordinary implementation output",
            "same conformance and functional acceptance",
        ):
            self.assertIn(phrase, text)

    def test_hypothesis_guidance_preserves_oracle_durability_and_isolation(self) -> None:
        text = read(HYPOTHESIS)
        for phrase in (
            "not an independent oracle",
            "isolated/reset test-owned state",
            "example database",
            "not durable regression authority by itself",
            "hypothesis `@example`",
            "settings profile",
            "seeds and failure-replay mechanisms are debugging aids",
            "excessive filtering",
            "health-check suppression",
            "solely to make a property green",
            "required coverage remains intact",
            "`max_examples`",
            "stateful step counts",
            "preserving representative coverage",
        ):
            self.assertIn(phrase, text)

    def test_source_readme_routes_to_split_tool_owners_without_copying_manuals(self) -> None:
        readme = read("source/README.md")
        common = read(COMMON)
        self.assertIn("shared/references/tool-assisted-engineering.md", readme)
        for name in DIRECT_TOOL_FILES:
            self.assertIn(name, common)
            self.assertNotIn(f"shared/references/{name}", readme)
        self.assertNotIn("## serena: semantic repository intelligence", readme)

    def test_portability_keeps_external_tooling_optional(self) -> None:
        text = read("PORTABILITY.md")
        self.assertIn("optional environment capabilities", text)
        self.assertIn("not generic agent skill validity requirements", text)
        self.assertIn("install a skill as a direct child", text)
        self.assertIn("named harness/model/tool evidence", text)


if __name__ == "__main__":
    unittest.main()
