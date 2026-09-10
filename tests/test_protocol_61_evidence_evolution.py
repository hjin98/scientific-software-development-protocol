from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Protocol61EvidenceEvolutionTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_current_version_and_concretization_vocabulary(self) -> None:
        self.assertEqual(self.read("source/PROTOCOL_VERSION").strip(), "6.1.0")
        authority = self.read("source/shared/references/abstraction-and-realization.md")
        self.assertIn("ABSTRACTION  --design / constrain-->  CONCRETIZATION", authority)
        self.assertIn("**realization** is reserved for concrete evidence execution", authority)

    def test_evidence_model_and_stale_evidence_are_explicit(self) -> None:
        evidence = self.read("source/shared/references/evidence-evolution-and-dependencies.md")
        testing = self.read("source/shared/references/testing-and-validation.md")
        for phrase in ("evidence specification", "evidence realization", "observation", "evidence assessment", "EXECUTION_DEPENDS_ON"):
            self.assertIn(phrase, evidence)
        self.assertIn("stale passing", testing.lower())
        self.assertIn("stale failing", testing.lower())

    def test_role_skills_do_not_call_evidence_realizations_concretizations(self) -> None:
        for role in ("software-design", "software-implementation"):
            text = self.read(f"source/roles/{role}/SKILL.md").lower()
            self.assertNotIn("evidence specifications/concretizations", text, role)
            self.assertNotIn("evidence specification, concretization", text, role)
        implementation = self.read("source/roles/software-implementation/SKILL.md").lower()
        self.assertIn("evidence specification, realization, and applicability", implementation)
        self.assertIn("evidence specifications/realizations", implementation)

    def test_source_readme_canonical_routes_exist(self) -> None:
        readme = self.read("source/README.md")
        self.assertIn("shared/references/abstraction-and-realization.md", readme)
        self.assertNotIn("shared/references/abstraction-and-concretization.md", readme)
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
        self.assertIn("alpha beta gamma (ABG)", writing)
        d1 = self.read("source/shared/templates/scientific_method_paper_template.md")
        d2 = self.read("source/shared/templates/numerical_algorithmic_method_paper_template.md")
        self.assertLess(d1.index("## Background and terminology"), d1.index("## Normative scientific / mathematical formulation"))
        self.assertLess(d2.index("## Background and terminology"), d2.index("## Governing numerical / algorithmic formulation"))

    def test_current_prompt_uses_canonical_public_repository(self) -> None:
        prompts = self.read("source/shared/references/development-workflow-prompts.md")
        self.assertIn("https://github.com/hjin98/scientific-software-development-protocol", prompts)
        self.assertNotIn("https://github.com/hjin98/software-development-protocol", prompts)
        self.assertIn("47e9155632c44493644b0b02fa1fa625703cf480", prompts)
        self.assertIn("repository default branch", prompts.lower())

    def test_current_recovery_mapping_is_immutable_and_coherent(self) -> None:
        recovery = "802e75af261efb4f70d71284d860613a2197b639"
        bootstrap = "47e9155632c44493644b0b02fa1fa625703cf480"
        versioning = self.read("source/shared/references/protocol-versioning-and-compatibility.md")
        portability = self.read("PORTABILITY.md")
        self.assertIn(f"6.1.0 -> {recovery}", versioning)
        self.assertIn(f"| 6.1.0 | `{recovery}` |", portability)
        self.assertIn(f"6.1.0 public-source bootstrap -> {bootstrap}", versioning)
        self.assertIn(f"public-source bootstrap: `{bootstrap}`", portability)
        self.assertNotEqual(recovery, bootstrap)
        self.assertIn("0c90fda19bf6ed9cb0c4511beb3da80ace6584ed", versioning)
        self.assertIn("historical", versioning.lower())

if __name__ == "__main__":
    unittest.main()
