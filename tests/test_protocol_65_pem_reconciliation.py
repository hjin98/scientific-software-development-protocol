from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
P0 = "55c085261eb827e3047637d045a8e6917ea6b962"
sys.path.insert(0, str(SOURCE))

import project_engineering_memory as pem  # noqa: E402


class Protocol65PemReconciliationTests(unittest.TestCase):
    def test_current_overlay_reconciles_without_silent_accepted_family_drift(self) -> None:
        previous_text = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{P0}:PROJECT-ENGINEERING-MEMORY.md"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        with tempfile.TemporaryDirectory(dir=ROOT) as td:
            prior_path = Path(td) / "previous-project-engineering-memory.md"
            prior_path.write_text(previous_text, encoding="utf-8")
            previous = pem.load_memory(prior_path)
            current = pem.load_memory(ROOT / "PROJECT-ENGINEERING-MEMORY.md")
            self.assertEqual(pem.validate_reconciliation(previous, current), [])


if __name__ == "__main__":
    unittest.main()
