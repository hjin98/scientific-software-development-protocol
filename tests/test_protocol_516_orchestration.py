from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "source/shared/references/development-workflow-prompts.md"


class Protocol516OrchestrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prompt = PROMPT.read_text(encoding="utf-8")
        self.lower = self.prompt.lower()

    def test_prompt_reference_has_parameterized_stage_entrypoints(self) -> None:
        for stage in (
            "Design / Workplan",
            "Implementation",
            "Review & Update",
            "Verification",
            "Stabilization / Architecture GC",
            "Alignment of a Downstream Workplan",
            "Health Audit",
            "Closeout",
        ):
            self.assertIn(stage.lower(), self.lower)
        self.assertGreaterEqual(self.prompt.count("INPUTS"), 8)
        self.assertIn("AUTO_LOCAL_FIRST", self.prompt)
        self.assertIn("PROTOCOL_REF", self.prompt)
        workflow = (ROOT / "source/shared/references/workflow-and-workplans.md").read_text(encoding="utf-8").lower()
        self.assertIn("baseline / change-health intake", workflow)
        self.assertIn("explicit stage or a design preamble", workflow)

    def test_local_first_public_fallback_is_explicit(self) -> None:
        self.assertRegex(self.lower, r"fall back to the canonical public repository(?: only)? when local resolution fails")
        self.assertIn("https://github.com/hjin98/software-development-protocol", self.prompt)
        self.assertRegex(self.lower, r"source/roles/<skill(?:-name)?>/skill\.md")
        self.assertRegex(self.lower, r"source/specialists/<skill(?:-name)?>/skill\.md")
        self.assertIn("skill root", self.lower)

    def test_selector_examples_are_not_shell_commands(self) -> None:
        self.assertIn("@software-design", self.prompt)
        self.assertIn("/software-implementation", self.prompt)
        self.assertIn("not shell commands", self.lower)
        self.assertNotRegex(self.prompt, r"(?:bash|sh)\s+@software-design")
        self.assertNotRegex(self.prompt, r"(?:bash|sh)\s+/software-implementation")

    def test_version_binding_forbids_silent_latest_upgrade(self) -> None:
        self.assertIn("do not silently", self.lower)
        self.assertIn("older", self.lower)
        self.assertIn("compatible", self.lower)
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text(encoding="utf-8").lower()
        self.assertIn("do not reinterpret", versioning)

    def test_stage_skill_routes_are_correct(self) -> None:
        expected = {
            "1. Design / Workplan": "software-design",
            "2. Implementation": "software-implementation",
            "3. Review & Update": "software-design",
            "4. Verification": "software-design",
            "5. Stabilization / Architecture GC": "software-design",
            "6. Alignment of a Downstream Workplan": "software-design",
            "7. Health Audit": "software-maintenance-audit",
        }
        for heading, skill in expected.items():
            pos = self.prompt.index(f"## {heading}")
            next_pos = self.prompt.find("\n## ", pos + 4)
            block = self.prompt[pos:] if next_pos < 0 else self.prompt[pos:next_pos]
            self.assertIn(skill, block.lower(), heading)

    def test_review_verification_stabilization_health_are_not_collapsed(self) -> None:
        self.assertIn("review & update", self.lower)
        self.assertIn("verification", self.lower)
        self.assertIn("high-risk", self.lower)
        self.assertIn("stabilization", self.lower)
        self.assertIn("non-mutating", self.lower)
        self.assertIn("health audit", self.lower)
        self.assertIn("periodic", self.lower)

    def test_no_source_means_truthful_limitation(self) -> None:
        self.assertRegex(self.lower, r"neither.{0,220}(?:source|installation).{0,220}(?:report|limitation)")
        self.assertIn("do not claim", self.lower)


if __name__ == "__main__":
    unittest.main()
