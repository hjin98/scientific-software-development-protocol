from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))
import release_state  # noqa: E402
P0_KERNEL_WORDS = 2642
HOT_CURRENT_SURFACES = (
    "README.md",
    "AGENTS.md",
    "PORTABILITY.md",
    "source/README.md",
    "source/SEMANTIC_DEPENDENCIES.md",
    "source/shared/references/development-workflow-prompts.md",
    "source/shared/references/protocol-versioning-and-compatibility.md",
    str(Path("orchestrator", "src", "sdp_" + "orchestrator", "core", "resources", "protocol", "ssdp-protocol-6.5", "prompts.md")),
)


class Protocol65CurrentStateOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.state = release_state.load(ROOT / "PROTOCOL-RELEASE-STATE.yaml")

    def test_mutable_release_refs_have_one_hot_owner(self) -> None:
        values = (
            self.state["accepted_current"]["public_source_ref"],
            self.state["accepted_current"]["recovery_ref"],
        )
        for rel in HOT_CURRENT_SURFACES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for value in values:
                self.assertNotIn(value, text, f"{rel} duplicates mutable release-state value {value}")

    def test_current_prompt_semantics_do_not_embed_release_state_variables(self) -> None:
        canonical = (ROOT / "source/shared/references/development-workflow-prompts.md").read_text(encoding="utf-8")
        generated_path = ROOT / "orchestrator" / "src" / ("sdp_" + "orchestrator") / "core" / "resources" / "protocol" / "ssdp-protocol-6.5" / "prompts.md"
        generated = generated_path.read_text(encoding="utf-8")
        self.assertEqual(canonical, generated)
        for token in ("CURRENT_PROTOCOL =", "CURRENT_PUBLIC_REF =", "ACCEPTED_6_3_PUBLIC_REF ="):
            self.assertNotIn(token, canonical)

    def test_current_workflow_prompt_has_no_predecessor_version_gate(self) -> None:
        canonical = (ROOT / "source/shared/references/development-workflow-prompts.md").read_text(encoding="utf-8")
        self.assertNotIn("Protocol 6.4", canonical)

    def test_stale_current_version_labels_are_absent_from_current_entrypoints(self) -> None:
        for path in sorted((ROOT / "source/roles").glob("*/SKILL.md")) + sorted((ROOT / "source/specialists").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"under Protocol 6\.[1234]\b", text), str(path.relative_to(ROOT)))
        self.assertNotIn(
            "Canonical D1 document-family template for Protocol 6.1",
            (ROOT / "source/shared/templates/scientific_method_paper_template.md").read_text(encoding="utf-8"),
        )
        self.assertNotIn(
            "Canonical D2 document-family template for Protocol 6.1",
            (ROOT / "source/shared/templates/numerical_algorithmic_method_paper_template.md").read_text(encoding="utf-8"),
        )
        self.assertNotIn(
            "Current Protocol 6.2 shared domain doctrine is authoritative",
            (ROOT / "source/shared/references/language-profiles.md").read_text(encoding="utf-8"),
        )

    def test_release_documentation_persistence(self) -> None:
        version = (ROOT / "source/PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertRegex(changelog, rf"(?m)^###\\s+{re.escape(version)}\\b")
        self.assertIn("[CHANGELOG.md](CHANGELOG.md)", readme)
        self.assertIn("[PROTOCOL-RELEASE-STATE.yaml](PROTOCOL-RELEASE-STATE.yaml)", readme)

    def test_proportional_rigor_keeps_acceptance_and_priority_distinct(self) -> None:
        kernel = (ROOT / "source/shared/references/abstraction-and-concretization.md").read_text(encoding="utf-8")
        convergence = (ROOT / "source/shared/references/convergence-and-cycle-economy.md").read_text(encoding="utf-8")
        evidence = (ROOT / "source/shared/references/evidence-evolution-and-dependencies.md").read_text(encoding="utf-8")
        self.assertIn("Mandatory obligations stay mandatory; priority only schedules them.", kernel)
        self.assertIn("child issues inherit no parent importance without credible causal linkage", kernel)
        self.assertIn("Distinguish problem importance from **next-action priority**", convergence)
        self.assertIn("Applicability is a feasibility condition, not an economy variable.", evidence)

    def test_universal_kernel_does_not_exceed_frozen_p0_word_count(self) -> None:
        text = (ROOT / "source/shared/references/abstraction-and-concretization.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(re.findall(r"\S+", text)), P0_KERNEL_WORDS)


if __name__ == "__main__":
    unittest.main()
