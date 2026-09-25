from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.path.insert(0, str(SOURCE))

import project_engineering_memory as pem  # noqa: E402


class Protocol65PemParserStrictnessTests(unittest.TestCase):
    def _front(self) -> str:
        return """---
memory_schema_version: 1
maintained_under_protocol: 6.5.0
project_id: test
repository: local
scope: repository
coverage_state: UNINITIALIZED
coverage_basis: none
reconciled_through: accepted
accepted_base:
  project_state: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  basis: test
candidate_overlay: NONE
detail_files: []
---
"""

    def _summary(self) -> str:
        return """# Project Engineering Memory

<!-- BEGIN DERIVED PEM SUMMARY -->
_No current learning families._
<!-- END DERIVED PEM SUMMARY -->
"""

    def _init(self, root: Path) -> None:
        subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "PEM Strictness Test"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "pem-strict@example.invalid"], check=True)

    def _commit(self, root: Path, message: str) -> str:
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", message], check=True)
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def test_root_frontmatter_rejects_duplicate_mapping_keys(self) -> None:
        text = self._front().replace(
            "repository: local\n",
            "repository: local\nrepository: forged\n",
        ) + self._summary()
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(pem.PemError, "duplicate key"):
                pem.load_memory(path)

    def test_family_block_rejects_duplicate_mapping_keys(self) -> None:
        family = """
### DS-001 — duplicate key

```yaml pem-family
id: DS-001
kind: DISCOVERY
kind: SUCCESS_PATTERN
```
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"
            path.write_text(self._front() + self._summary() + family, encoding="utf-8")
            with self.assertRaisesRegex(pem.PemError, "duplicate key"):
                pem.load_memory(path)

    def test_orphan_canonical_family_block_is_rejected(self) -> None:
        orphan = """
```yaml pem-family
id: DS-001
kind: DISCOVERY
```
"""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"
            path.write_text(self._front() + self._summary() + orphan, encoding="utf-8")
            with self.assertRaisesRegex(pem.PemError, "every yaml pem-family block"):
                pem.load_memory(path)

    def test_root_requires_exactly_one_active_summary_pair(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"
            path.write_text(
                self._front() + self._summary() + self._summary(),
                encoding="utf-8",
            )
            doc = pem.load_memory(path)
            errors = pem.validate_memory(doc)
            self.assertTrue(any("exactly one derived active-summary" in error for error in errors))

    def test_repair_acceptance_rejects_duplicate_mapping_keys(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._init(root)
            (root / "acceptance.md").write_text(
                """```yaml pem-repair-acceptance
repair_identity: commit:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
repair_identity: commit:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
state: ACCEPTED
owner: local@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:owner.md
```
""",
                encoding="utf-8",
            )
            (root / "owner.md").write_text("owner\n", encoding="utf-8")
            commit = self._commit(root, "duplicate repair acceptance")
            doc = pem.PemDocument(
                root=root / "PROJECT-ENGINEERING-MEMORY.md",
                metadata={"repository": "local", "accepted_base": {"project_state": commit}},
                families={},
                notices={},
                sources={},
                root_text="",
            )
            route = pem.parse_evidence_route(f"local@{commit}:acceptance.md")
            with self.assertRaisesRegex(pem.PemError, "invalid typed repair-acceptance YAML"):
                pem._validate_repair_acceptance_artifact(
                    root,
                    route,
                    "commit:" + ("a" * 40),
                    "recurrence",
                    doc,
                )


if __name__ == "__main__":
    unittest.main()
