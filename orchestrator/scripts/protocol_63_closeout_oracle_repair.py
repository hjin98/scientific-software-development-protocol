#!/usr/bin/env python3
"""Reconcile successor-sensitive closeout oracles for Protocol 6.3 cutover."""
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


ROOT = Path(__file__).resolve().parents[2]

versioning = ROOT / "source/shared/references/protocol-versioning-and-compatibility.md"
replace_once(
    versioning,
    "so replacement self-reference-safe source snapshot `86c13cab6bdd1991dffa94e277db8eacf87e2e11`",
    "so Replacement self-reference-safe source snapshot `86c13cab6bdd1991dffa94e277db8eacf87e2e11`",
)
replace_once(
    versioning,
    "sole 6.3 public-source fallback",
    "sole current 6.3 public-source fallback",
)

protocol62_test = ROOT / "tests/test_protocol_62_closeout.py"
replace_once(
    protocol62_test,
    '''    def test_current_and_historical_profile_state_is_explicit(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", portability)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", portability)
''',
    '''    def test_current_and_historical_profile_state_is_explicit(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn("| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", portability)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |", portability)
        self.assertIn("| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |", portability)
''',
)
replace_once(
    protocol62_test,
    '''    def test_current_dependency_view_names_62_as_current(self):
        dependencies = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        self.assertIn("ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics", dependencies)
        self.assertIn("ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics", dependencies)
''',
    '''    def test_current_dependency_view_advances_without_losing_62_history(self):
        dependencies = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        self.assertIn("ssdp-protocol-6.3 CONSTRAINED_BY -> accepted-current Protocol 6.3 semantics", dependencies)
        self.assertIn("ssdp-protocol-6.2 CONSTRAINED_BY -> immutable historical Protocol 6.2 rollback semantics", dependencies)
        self.assertIn("ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics", dependencies)
''',
)
