from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class Protocol62CloseoutTests(unittest.TestCase):
    def test_historical_profile_and_release_state_are_preserved(self):
        portability = (ROOT / "PORTABILITY.md").read_text()
        state = yaml.safe_load((ROOT / "PROTOCOL-RELEASE-STATE.yaml").read_text())
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical |", portability)
        self.assertEqual(state["historical"]["6.2.0"]["public_source_ref"], "5a062ebc472755607b9dc66d33a5ebbc4b7429aa")
        self.assertEqual(state["historical"]["6.2.0"]["recovery_ref"], "b59adc77efe6951912cfd705cc43830c58ca27d0")

    def test_archive_closeout_survives(self):
        self.assertFalse((ROOT / "workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").exists())
        self.assertTrue((ROOT / "workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md").is_file())

    def test_protocol7_is_reconciled_but_d4_stays_blocked(self):
        rev3 = (ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md").read_text()
        index = (ROOT / "workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md").read_text()
        self.assertIn("d3_architecture_mutation: none", rev3)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev3)
        self.assertIn("PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED", index)


if __name__ == "__main__":
    unittest.main()
