import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = "9f353097fab36e325a325f1c2f9d9cec32e86177"
BOOTSTRAP = "86c13cab6bdd1991dffa94e277db8eacf87e2e11"
BASE62 = "b59adc77efe6951912cfd705cc43830c58ca27d0"


class Protocol63CloseoutTests(unittest.TestCase):
    def test_accepted_current_and_identity_distinction(self) -> None:
        versioning = (ROOT / "source/shared/references/protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn("| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |", versioning)
        self.assertIn("| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |", versioning)
        self.assertIn(f"6.3.0  -> {RECOVERY}", versioning)
        self.assertIn(f"6.3.0 public bootstrap -> {BOOTSTRAP}", portability)
        self.assertIn(f"6.3.0 recovery -> {RECOVERY}", portability)
        self.assertNotEqual(RECOVERY, BOOTSTRAP)
        self.assertIn("Current accepted document-controlled release: **Protocol 6.3**", readme)
        self.assertIn(BASE62, readme)

    def test_workplan_archived_and_protocol7_inheritance_reconciled(self) -> None:
        active = ROOT / "workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
        archived = ROOT / "workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
        rev4 = ROOT / "workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md"
        self.assertFalse(active.exists())
        self.assertTrue(archived.is_file())
        text = rev4.read_text()
        self.assertIn("d3_architecture_mutation: none", text)
        self.assertIn("PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED", text)
        self.assertIn(f"Protocol 6.3 recovery           -> {RECOVERY}", text)

    def test_current_dependency_and_closeout_evidence(self) -> None:
        deps = (ROOT / "source/SEMANTIC_DEPENDENCIES.md").read_text()
        state = (ROOT / "qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md").read_text()
        closeout = (ROOT / "qualification/ssdp6/STAGE-G-CLOSEOUT-PROTOCOL-6.3.md").read_text()
        self.assertIn("ssdp-protocol-6.3 CONSTRAINED_BY -> accepted-current Protocol 6.3 semantics", deps)
        self.assertIn("accepted_current_protocol: 6.3.0", state)
        self.assertIn(f"protocol_63_recovery: {RECOVERY}", state)
        self.assertIn("**STAGE G: PASS.**", closeout)


if __name__ == "__main__":
    unittest.main()
