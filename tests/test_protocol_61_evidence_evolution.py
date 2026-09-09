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

if __name__ == "__main__":
    unittest.main()
