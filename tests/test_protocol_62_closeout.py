from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Protocol62CloseoutTests(unittest.TestCase):
    def test_current_and_historical_profile_state_is_explicit(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |", portability)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | accepted current |", portability)

    def test_recovery_bootstrap_and_archive_closeout(self):
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        self.assertIn("6.2.0  -> b59adc77efe6951912cfd705cc43830c58ca27d0", versioning)
        self.assertIn("6.2.0 public-source bootstrap -> 5a062ebc472755607b9dc66d33a5ebbc4b7429aa", versioning)
        self.assertNotEqual("b59adc77efe6951912cfd705cc43830c58ca27d0", "5a062ebc472755607b9dc66d33a5ebbc4b7429aa")
        self.assertFalse((ROOT / "workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").exists())
        self.assertTrue((ROOT / "workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").is_file())

    def test_protocol7_is_reconciled_but_d4_stays_blocked(self):
        rev3 = (ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md").read_text()
        index = (ROOT / "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md").read_text()
        self.assertIn("d3_architecture_mutation: none", rev3)
        self.assertIn("PROTOCOL 7 DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN / SUPERSESSION: STILL REQUIRED", rev3)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev3)
        self.assertIn("PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED", index)
        self.assertIn("PROTOCOL 7 D4: NOT AUTHORIZED", index)

    def test_current_dependency_view_names_62_as_current(self):
        dependencies = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        self.assertIn("ssdp-protocol-6.2 CONSTRAINED_BY -> accepted-current Protocol 6.2 semantics", dependencies)
        self.assertIn("ssdp-protocol-6.1 CONSTRAINED_BY -> immutable historical Protocol 6.1 rollback semantics", dependencies)


if __name__ == "__main__":
    unittest.main()
