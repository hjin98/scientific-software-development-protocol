import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = "9f353097fab36e325a325f1c2f9d9cec32e86177"
BOOTSTRAP = "86c13cab6bdd1991dffa94e277db8eacf87e2e11"


class Protocol63CloseoutTests(unittest.TestCase):
    def test_historical_identity_survives_current_successor_work(self) -> None:
        state = yaml.safe_load((ROOT / "PROTOCOL-RELEASE-STATE.yaml").read_text())
        self.assertEqual(state["historical"]["6.3.0"]["public_source_ref"], BOOTSTRAP)
        self.assertEqual(state["historical"]["6.3.0"]["recovery_ref"], RECOVERY)
        self.assertNotEqual(RECOVERY, BOOTSTRAP)

    def test_workplan_archived_and_protocol7_inheritance_reconciled(self) -> None:
        self.assertFalse((ROOT / "workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md").exists())
        self.assertTrue((ROOT / "workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md").is_file())
        rev4 = (ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md").read_text()
        self.assertIn("d3_architecture_mutation: none", rev4)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", rev4)

    def test_historical_closeout_evidence_remains(self) -> None:
        state = (ROOT / "qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md").read_text()
        closeout = (ROOT / "qualification/ssdp6/STAGE-G-CLOSEOUT-PROTOCOL-6.3.md").read_text()
        self.assertIn("accepted_current_protocol: 6.3.0", state)
        self.assertIn(f"protocol_63_recovery: {RECOVERY}", state)
        self.assertIn("**STAGE G: PASS.**", closeout)


if __name__ == "__main__":
    unittest.main()
