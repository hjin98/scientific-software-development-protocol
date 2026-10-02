import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "workplans/active"
ARCHIVE = ROOT / "workplans/archive"
INDEX = ACTIVE / "SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md"
SSDS8 = "SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE.md"
SSDS8_HYPOTHESIS = "SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE-BEFE678-HYPOTHESIS.md"
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
LINEAGE = [CONSOLIDATED, SSDS8_HYPOTHESIS, *SUPERSEDED]


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} has no frontmatter")
    return yaml.safe_load(text[4:text.index("\n---\n", 4)])


class Protocol80OrchestratorConsolidationTests(unittest.TestCase):
    """The deterministic-orchestrator line has one current, unauthorized handoff.

    These checks read frontmatter and file placement only. Whether the handoff
    or the index is semantically adequate is owned by independent Review.
    """

    def test_single_proposed_unauthorized_ssds8_handoff(self) -> None:
        meta = frontmatter(ACTIVE / SSDS8)
        self.assertEqual(meta["workplan_id"], Path(SSDS8).stem)
        self.assertEqual(meta["protocol_version"], "6.6.0")
        self.assertEqual(meta["target_system_version"], "8.0.0")
        self.assertEqual(meta["status"], "proposed")
        self.assertEqual(meta["d3_architecture_state"], "proposed")
        self.assertEqual(meta["implementation_handoff"], "not-authorized")

    def test_superseded_lineage_is_closed_and_archived(self) -> None:
        meta = frontmatter(ACTIVE / SSDS8)
        self.assertEqual(set(meta["supersedes"]), {Path(CONSOLIDATED).stem, Path(SSDS8_HYPOTHESIS).stem})
        consolidated = frontmatter(ARCHIVE / CONSOLIDATED)
        self.assertEqual(consolidated["implementation_handoff"], "not-authorized")
        self.assertEqual(set(consolidated["supersedes"]), {Path(name).stem for name in SUPERSEDED})
        for name in LINEAGE:
            self.assertFalse((ACTIVE / name).exists(), name)
            self.assertTrue((ARCHIVE / name).is_file(), name)

    def test_index_routes_to_current_handoffs(self) -> None:
        routes = frontmatter(INDEX)["current_handoffs"]
        self.assertEqual(routes["ssds-8.0"], f"workplans/active/{SSDS8}")
        superseded = {Path(name).stem for name in LINEAGE}
        for line, relative in routes.items():
            target = ROOT / relative
            self.assertTrue(target.is_file(), line)
            self.assertEqual(target.parent, ACTIVE, line)
            self.assertEqual(frontmatter(target)["workplan_id"], target.stem, line)
            self.assertNotIn(target.stem, superseded, line)

    def test_index_keeps_archived_lineage_routes(self) -> None:
        # Representation guard against the befe678 regression that dropped
        # lineage routes from the index; it does not establish routing truth.
        index = INDEX.read_text(encoding="utf-8")
        for name in LINEAGE:
            self.assertIn(f"workplans/archive/{name}", index, name)
            self.assertNotIn(f"workplans/active/{name}", index, name)


if __name__ == "__main__":
    unittest.main()
