import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "workplans/active"
ARCHIVE = ROOT / "workplans/archive"
CONSOLIDATED = "SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED.md"
PREFIX = "SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION"
SUPERSEDED = [
    f"{PREFIX}.md",
    f"{PREFIX}-REVISION-1-SECOND-REVIEW-CLOSURE.md",
    f"{PREFIX}-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md",
    f"{PREFIX}-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md",
    f"{PREFIX}-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md",
    f"{PREFIX}-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION.md",
    f"{PREFIX}-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION.md",
    f"{PREFIX}-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT.md",
    "SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md",
]


class Protocol80OrchestratorConsolidationTests(unittest.TestCase):
    def test_single_proposed_protocol8_handoff(self) -> None:
        text = (ACTIVE / CONSOLIDATED).read_text(encoding="utf-8")
        self.assertIn("target_protocol_version: 8.0.0", text)
        self.assertIn("status: proposed", text)
        self.assertIn("PROTOCOL 8 D4 IMPLEMENTATION: NOT AUTHORIZED", text)
        for name in SUPERSEDED:
            self.assertIn(Path(name).stem, text, name)

    def test_superseded_family_is_archived_not_active(self) -> None:
        for name in SUPERSEDED:
            self.assertFalse((ACTIVE / name).exists(), name)
            self.assertTrue((ARCHIVE / name).is_file(), name)

    def test_index_routes_to_consolidated_handoff(self) -> None:
        index = (ACTIVE / "SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md").read_text(encoding="utf-8")
        self.assertIn(f"workplans/active/{CONSOLIDATED}", index)
        self.assertNotIn(f"workplans/active/{PREFIX}", index)


if __name__ == "__main__":
    unittest.main()
