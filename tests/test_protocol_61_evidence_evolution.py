from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Protocol61EvidenceEvolutionTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_current_version_and_concretization_vocabulary(self) -> None:
        version = tuple(int(part) for part in self.read("source/PROTOCOL_VERSION").strip().split("."))
        self.assertEqual(version[0], 6)
        self.assertGreaterEqual(version, (6, 2, 0))
        authority = self.read("source/shared/references/abstraction-and-concretization.md")
        self.assertIn("A **concretization** is a lower-level choice", authority)
        self.assertIn("**Realization** is reserved for concrete evidence execution", authority)

    def test_evidence_model_and_stale_evidence_are_explicit(self) -> None:
        evidence = self.read("source/shared/references/evidence-evolution-and-dependencies.md")
        testing = self.read("source/shared/references/testing-and-validation.md")
        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "EXECUTION_DEPENDS_ON"):
            self.assertIn(phrase, evidence)
        self.assertIn("stale pass", testing.lower())
        self.assertIn("stale fail", testing.lower())

    def test_role_skills_keep_evidence_target_separate_from_execution_machinery(self) -> None:
        for role in ("software-design", "software-implementation"):
            text = self.read(f"source/roles/{role}/SKILL.md").lower()
            self.assertNotIn("evidence specifications/concretizations", text, role)
            self.assertNotIn("evidence specification, concretization", text, role)
        implementation = self.read("source/roles/software-implementation/SKILL.md").lower()
        evidence = self.read("source/shared/references/evidence-evolution-and-dependencies.md")
        self.assertIn("evidence target separately from harness/fixture/backend/implementation dependencies", implementation)
        self.assertIn("EXECUTION_DEPENDS_ON", evidence)

    def test_source_readme_canonical_routes_exist(self) -> None:
        readme = self.read("source/README.md")
        self.assertIn("shared/references/abstraction-and-concretization.md", readme)
        self.assertNotIn("shared/references/abstraction-and-realization.md", readme)
        for raw in readme.split("`"):
            if raw.startswith("shared/references/") and raw.endswith(".md"):
                self.assertTrue((ROOT / "source" / raw).is_file(), raw)

    def test_bounded_dependency_and_history_surfaces_exist(self) -> None:
        dep = self.read("source/SEMANTIC_DEPENDENCIES.md")
        hist = self.read("history/SEMANTIC_EVOLUTION.md")
        self.assertIn("Absence", dep)
        self.assertIn("independence", dep)
        self.assertIn("Semantic Evolution", hist)

    def test_human_facing_background_and_abbreviation_contract(self) -> None:
        writing = self.read("source/shared/references/scientific-technical-writing.md")
        self.assertIn("intended competent reader", writing)
        self.assertIn("full term (ABC)", writing)
        d1 = self.read("source/shared/templates/scientific_method_paper_template.md")
        d2 = self.read("source/shared/templates/numerical_algorithmic_method_paper_template.md")
        self.assertLess(d1.index("## Background and terminology"), d1.index("## Normative scientific / mathematical formulation"))
        self.assertLess(d2.index("## Background and terminology"), d2.index("## Governing numerical / algorithmic formulation"))

    def test_current_prompt_preserves_public_source_discipline_during_and_after_62_bootstrap(self) -> None:
        invalidated = "1181c2031710c5d343194d87d08543290fded0ab"
        prompts = self.read("source/shared/references/development-workflow-prompts.md")
        lower = prompts.lower()
        versioning = self.read("source/shared/references/protocol-versioning-and-compatibility.md")
        published = re.search(r"6\.2\.0 public-source bootstrap -> ([0-9a-f]{40})", versioning)

        self.assertIn("https://github.com/hjin98/scientific-software-development-protocol", prompts)
        self.assertNotIn("https://github.com/hjin98/software-development-protocol", prompts)
        self.assertIn("repository-default bytes are never a substitute", lower)
        self.assertNotIn(f"PUBLIC_REF = {invalidated}", prompts)

        if published is None:
            self.assertIn("bootstrap self-reference rule", lower)
            self.assertIn("automatic current-6.2 public fallback is unavailable", lower)
            self.assertNotIn("current 6.2 may fall back", lower)
        else:
            bootstrap = published.group(1)
            self.assertNotEqual(bootstrap, invalidated)
            current_version = self.read("source/PROTOCOL_VERSION").strip()
            if current_version == "6.2.0":
                self.assertIn(f"PUBLIC_REF = {bootstrap}", prompts)
                self.assertIn("current 6.2 may fall back", lower)
                self.assertNotIn("automatic current-6.2 public fallback is unavailable", lower)
            else:
                self.assertIn(f"ACCEPTED_6_2_PUBLIC_REF = {bootstrap}", prompts)
                current = re.search(r"^CURRENT_PUBLIC_REF = (\S+)$", prompts, re.MULTILINE)
                self.assertIsNotNone(current)
                current_ref = current.group(1)
                self.assertNotEqual(current_ref, "1484c1d3caa49d87cc15bc52a5e775399c1dae1b")
                self.assertTrue(current_ref == "UNAVAILABLE_PENDING_6.3_BOOTSTRAP_QUALIFICATION" or re.fullmatch(r"[0-9a-f]{40}", current_ref))
                self.assertIn("version-bound 6.2 work continues to use exactly", lower)

    def test_accepted_61_recovery_and_bootstrap_remain_immutable(self) -> None:
        recovery = "802e75af261efb4f70d71284d860613a2197b639"
        bootstrap = "47e9155632c44493644b0b02fa1fa625703cf480"
        versioning = self.read("source/shared/references/protocol-versioning-and-compatibility.md")
        portability = self.read("PORTABILITY.md")
        self.assertIn(f"6.1.0  -> {recovery}", versioning)
        self.assertIn(recovery, portability)
        self.assertIn(f"6.1.0 public-source bootstrap -> {bootstrap}", versioning)
        self.assertIn(bootstrap, portability)
        self.assertNotEqual(recovery, bootstrap)
        self.assertIn("historical", versioning.lower())


if __name__ == "__main__":
    unittest.main()
