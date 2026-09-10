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
DIRECT_TOOL_FILES = ("tool-serena.md", "tool-semgrep.md", "tool-hypothesis.md", "tool-codeql.md")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8").lower()


class Protocol511ToolAssistanceTests(unittest.TestCase):
    def test_lifecycle_entrypoints_delegate_relation_first_dispatch_to_common_router(self) -> None:
        for rel in ("source/roles/software-design/SKILL.md", "source/roles/software-implementation/SKILL.md"):
            text = read(rel)
            self.assertIn("references/tool-assisted-engineering.md", text, rel)
            self.assertIn("relation", text, rel)
            for name in DIRECT_TOOL_FILES:
                self.assertNotIn(f"references/{name}", text, (rel, name))
        common = read(COMMON)
        self.assertIn("relation under the current material claim", common)
        for name in DIRECT_TOOL_FILES:
            self.assertIn(name, common)

    def test_tool_references_remain_progressively_disclosed_and_transport_reachable(self) -> None:
        for role in ("software-design", "software-implementation"):
            spec = build_skills.ROLE_SPECS[role]
            self.assertIn("tool-assisted-engineering.md", spec["references"])
            for name in DIRECT_TOOL_FILES:
                self.assertNotIn(name, spec["references"])

        for role in ("scientific-formulation", "numerical-algorithm-design"):
            spec = build_skills.ROLE_SPECS[role]
            for name in DIRECT_TOOL_FILES:
                self.assertNotIn(name, spec["references"])

        for specialist in ("software-documentation", "repository-hygiene"):
            self.assertNotIn("tool-assisted-engineering.md", build_skills.SPECIALIST_SPECS[specialist]["references"])

        audit = build_skills.SPECIALIST_SPECS["software-maintenance-audit"]
        self.assertIn("tool-assisted-engineering.md", audit["references"])
        for name in DIRECT_TOOL_FILES:
            self.assertNotIn(name, audit["references"])

        with tempfile.TemporaryDirectory() as tmp:
            dist = Path(tmp) / "dist"
            build_skills.build(dist)
            for role in ("software-design", "software-implementation"):
                root = dist / "skills" / role / "references"
                self.assertTrue((root / "tool-assisted-engineering.md").is_file())
                for name in DIRECT_TOOL_FILES:
                    self.assertTrue((root / name).is_file(), (role, name))

    def test_common_reference_owns_selection_composition_and_authority(self) -> None:
        text = read(COMMON)
        for phrase in (
            "tool availability alone is not a reason",
            "tool unavailability is not an acceptance failure",
            "mandatory three-tool pipeline",
            "do not invoke another tool merely to duplicate evidence",
            "independent review",
            "not an instruction-authority channel",
            "not product truth",
            "re-derive the final affected surface",
            "affected regression",
            "integration",
        ):
            self.assertIn(phrase, text)
        self.assertIn("security task is not automatically a codeql task", text)

    def test_common_reference_is_progressive_disclosure_not_tool_manual(self) -> None:
        text = read(COMMON)
        for specific in ("ambiguous repository state", ".semgrepignore", "health-check suppression", "database creation success is not product correctness evidence"):
            self.assertNotIn(specific, text)

    def test_serena_guidance_protects_backend_completeness_mutation_and_memory(self) -> None:
        text = read(SERENA)
        for phrase in ("backends and languages expose different capabilities", "cross-check semantic results", "ambiguous repository state", "inspect current file/diff/status before retrying", "derived/advisory context by default", "explicitly promote", ".serena"):
            self.assertIn(phrase, text)
        self.assertIn("presumptively use serena", text)

    def test_semgrep_guidance_bounds_rule_engine_scope_and_suppressions(self) -> None:
        text = read(SEMGREP)
        for phrase in ("community edition-compatible", "known-positive and known-negative", ".gitignore", ".semgrepignore", "nosemgrep", "actual scan contract", "volatile network-fetched ruleset", "same conformance and functional acceptance"):
            self.assertIn(phrase, text)

    def test_hypothesis_guidance_preserves_oracle_durability_and_isolation(self) -> None:
        text = read(HYPOTHESIS)
        for phrase in ("not an independent oracle", "isolated/reset test-owned state", "example database", "not durable regression authority by itself", "hypothesis `@example`", "settings profile", "excessive filtering", "health-check suppression", "solely to make a property green", "required coverage remains intact", "`max_examples`", "stateful step counts"):
            self.assertIn(phrase, text)

    def test_source_readme_routes_to_common_and_specialized_tool_owners(self) -> None:
        readme = read("source/README.md")
        self.assertIn("shared/references/tool-assisted-engineering.md", readme)
        for name in DIRECT_TOOL_FILES:
            self.assertIn(name, readme)
        self.assertNotIn("## serena: semantic repository intelligence", readme)

    def test_portability_keeps_external_tooling_optional(self) -> None:
        text = read("PORTABILITY.md")
        self.assertIn("optional", text)
        self.assertIn("tool", text)
        self.assertIn("standalone", text)


if __name__ == "__main__":
    unittest.main()
