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

    def test_current_516_workplan_remains_active_until_independent_review(self) -> None:
        name = "PROTOCOL-5.16-LONG-HORIZON-CODE-HEALTH-AND-AUTONOMOUS-QUALITY.md"
        self.assertTrue((ACTIVE / name).is_file())
        self.assertFalse((ARCHIVE / name).exists())


if __name__ == "__main__":
    unittest.main()
