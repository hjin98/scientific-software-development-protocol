from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "workplans/active"
ARCHIVE = ROOT / "workplans/archive"


class Protocol516LifecycleCloseoutTests(unittest.TestCase):
    def test_completed_514_and_515_workplans_are_archived_with_truthful_status(self) -> None:
        for name in (
            "PROTOCOL-5.14-SOLUTION-BOUNDARY-AND-ACTIVE-SIMPLICITY.md",
            "PROTOCOL-5.15-LANGUAGE-PROFILES-CPP-PERFORMANCE.md",
        ):
            self.assertFalse((ACTIVE / name).exists(), name)
            archived = ARCHIVE / name
            self.assertTrue(archived.is_file(), name)
            header = archived.read_text(encoding="utf-8").split("---", 2)[1]
            self.assertIn("status: completed", header, name)
            self.assertIn("completed_date: 2026-09-04", header, name)

    def test_516_workplan_is_archived_after_passing_independent_review(self) -> None:
        name = "PROTOCOL-5.16-LONG-HORIZON-CODE-HEALTH-AND-AUTONOMOUS-QUALITY.md"
        self.assertFalse((ACTIVE / name).exists())
        archived = ARCHIVE / name
        self.assertTrue(archived.is_file())
        text = archived.read_text(encoding="utf-8")
        header = text.split("---", 2)[1]
        self.assertIn("status: completed", header)
        self.assertIn("completed_date: 2026-09-06", header)
        self.assertIn("Final Design verdict: PASS", text)

    def test_ssdp6_transition_authority_is_archived_after_final_pass(self) -> None:
        names = (
            "SSDP-6-AUTHORITY.md",
            "SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL.md",
            "SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL-AUTHORITY-REVISION-1-SERIOUS-CHALLENGE-AND-ADVERSARIAL-REVIEW.md",
            "SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL-AUTHORITY-REVISION-2-PROTOCOL-5-INHERITANCE-AND-CONSOLIDATION.md",
        )
        for name in names:
            self.assertFalse((ACTIVE / name).exists(), name)
            archived = ARCHIVE / name
            self.assertTrue(archived.is_file(), name)
            header = archived.read_text(encoding="utf-8").split("---", 2)[1]
            self.assertIn("status: completed", header, name)
            self.assertIn("completed_date: 2026-09-09", header, name)
            self.assertIn("final_review: pass", header, name)
            self.assertIn("active_serious_challenge: none", header, name)
        authority = (ARCHIVE / "SSDP-6-AUTHORITY.md").read_text(encoding="utf-8")
        self.assertIn("FINAL INDEPENDENT REVIEW / CHALLENGE PASS: PASS", authority)
        self.assertIn("no longer a parallel current authority layer", authority)


if __name__ == "__main__":
    unittest.main()
