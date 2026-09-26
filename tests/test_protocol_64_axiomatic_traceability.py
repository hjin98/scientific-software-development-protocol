from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import release_state  # noqa: E402


class Protocol64PreservationAndStructureTests(unittest.TestCase):
    """Preserve real Protocol 6.4 structural contracts without proxying prose semantics."""

    def test_historical_64_release_identity_is_owned_by_release_state(self) -> None:
        state = release_state.load(ROOT / "PROTOCOL-RELEASE-STATE.yaml")
        if state["accepted_current"]["version"] == "6.4.0":
            p64 = state["accepted_current"]
        else:
            p64 = state["historical"]["6.4.0"]
        self.assertEqual(p64["public_source_ref"], "e09a9d1480211eea2d16d722182bb5c6de1bee12")
        self.assertEqual(p64["recovery_ref"], "74bc572ef516cae417437a2027eeff52a2e25c15")
        self.assertNotEqual(p64["public_source_ref"], p64["recovery_ref"])

    def test_64_consolidated_authority_is_archived_and_recoverable(self) -> None:
        active = sorted((ROOT / "workplans/active").glob("SSDP-6.4*.md"))
        archived = ROOT / "workplans/archive/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md"
        self.assertEqual(active, [])
        self.assertTrue(archived.is_file())
        self.assertIn("STAGE F: PASS", archived.read_text(encoding="utf-8"))

    def test_current_roles_route_to_real_definition_owners(self) -> None:
        expected = {
            "scientific-formulation": "references/scientific-formulation.md",
            "numerical-algorithm-design": "references/numerical-algorithm-design.md",
            "software-design": "references/architecture-and-design.md",
            "software-implementation": "references/specification-and-implementation.md",
        }
        for role, owner in expected.items():
            # consumed entrypoint: the kernel route is generated into its entry contract
            text = (ROOT / "dist" / "skills" / role / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("references/abstraction-and-concretization.md", text, role)
            self.assertIn(owner, text, role)

    def test_current_markdown_owner_surfaces_have_balanced_fences(self) -> None:
        surfaces = [
            SOURCE / "shared/references/abstraction-and-concretization.md",
            SOURCE / "shared/references/evidence-evolution-and-dependencies.md",
            SOURCE / "shared/references/scientific-technical-writing.md",
            SOURCE / "shared/references/protocol-versioning-and-compatibility.md",
            SOURCE / "shared/references/development-workflow-prompts.md",
            SOURCE / "SEMANTIC_DEPENDENCIES.md",
        ]
        for path in surfaces:
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("```") % 2, 0, str(path.relative_to(ROOT)))

if __name__ == "__main__":
    unittest.main()
