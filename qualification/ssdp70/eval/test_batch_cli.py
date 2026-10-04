"""Batch CLI and aggregation-owner discriminators (no runtime needed).

The refusals under test occur before any evaluator could launch; the numeric tests feed the
production `quantitative_part` retained summary files.
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import batch_assess70
import core70

SHA = "a" * 64
COMMIT = "b" * 40


def manifest(run_ids, purpose="oracle-integrity"):
    rows = [{"id": rid, "profile_key_sha256": SHA, "entry_stratum": "deterministic", "scoring_manifest_sha256": SHA,
             "subject": {"commit": COMMIT, "package_sha256": SHA}, "fault": "known-good",
             "expected": {"evidence_state": "COMPLETE_ADMISSIBLE", "criteria": {}, "qualification_outcome": "PASS"}} for rid in run_ids]
    return {"purpose": purpose, "scope_id": "cli-test", "runs": rows}


class BatchCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.runs = self.root / "runs"
        self.out = self.root / "out"
        self.runs.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, mf):
        path = self.root / "manifest.json"
        path.write_text(json.dumps(mf))
        argv = ["--accounting-manifest", str(path), "--runs-dir", str(self.runs), "--out-dir", str(self.out),
                "--keys", str(self.root), "--evaluator-profile", "p", "--evaluator-capabilities", "c",
                "--evaluator-admission", "a", "--adapter", "x"]
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = batch_assess70.main(argv)
        return code, err.getvalue()

    def test_unsafe_run_ids_are_refused_before_any_evaluator_launch(self):
        for bad in ("../escape", "/abs", "a/b", "..", ".hidden", "", "x" * 200):
            with self.subTest(bad=bad):
                code, err = self.run_cli(manifest([bad]))
                self.assertEqual(code, 2)
                self.assertIn("refused before evaluator launch", err)
                self.assertFalse(self.out.exists() and any(self.out.iterdir()))

    def test_undeclared_and_imported_run_directories_are_refused_before_launch(self):
        (self.runs / "E1-p70-r0").mkdir()
        (self.runs / "E9-imported").mkdir()
        code, err = self.run_cli(manifest(["E1-p70-r0"]))
        self.assertEqual(code, 2)
        self.assertIn("E9-imported", err)
        self.assertFalse(self.out.exists() and any(self.out.iterdir()))

    def test_malformed_manifest_is_refused_before_launch(self):
        code, err = self.run_cli({"purpose": "qualification"})
        self.assertEqual(code, 2)
        self.assertFalse(self.out.exists() and any(self.out.iterdir()))

    def test_summary_of_integrity_scope_without_arms_does_not_crash(self):
        out = io.StringIO()
        summary = {"purpose": "oracle-integrity", "scope_id": "s", "runs": {"r": {}}, "arms": {}, "critical_failures": {},
                   "errors": [], "integrity_outcome": "PASS"}
        with contextlib.redirect_stdout(out):
            batch_assess70.print_summary(summary, {"r"})
        self.assertIn("Outer integrity outcome: PASS", out.getvalue())


class T7Mode(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def panel(self, modes, bytes_by_mode=None, cost=None):
        """Three paired T7 runs per arm; mode is the observed owner-read state."""
        bytes_by_mode = bytes_by_mode or {"owner": 60000, "entry": 14000}
        opportunities = []
        for arm in ("p70", "p66"):
            for i, mode in enumerate(modes[arm]):
                run = f"T7-{arm}-r{i}"
                (self.root / run).mkdir()
                summary = {"active_ssdp_bytes": bytes_by_mode["owner" if mode == "owner" else "entry"] + i,
                           "installed_entrypoint_bytes": 14000, "installed_owner_bytes": 46000,
                           "owner_read_sequences": None if mode is None else [3] if mode == "owner" else []}
                (self.root / run / "summary.json").write_text(json.dumps(summary))
                opportunities.append({"part": "fixed_cost", "route": "T7", "arm": arm, "realizations": [{"run": run}]})
        for route in ("T1", "T8"):
            for arm in ("p70", "p66"):
                for i in range(3):
                    run = f"{route}-{arm}-r{i}"
                    (self.root / run).mkdir()
                    (self.root / run / "summary.json").write_text(json.dumps(
                        {"active_ssdp_bytes": 14000, "owner_read_sequences": []}))
                    opportunities.append({"part": "fixed_cost", "route": route, "arm": arm, "realizations": [{"run": run}]})
        m = {"candidate_arm": "p70", "comparator_arm": "p66", "cost_comparator_arm": "p66"}
        return batch_assess70.quantitative_part("fixed_cost", m, opportunities, self.root)

    def test_same_mode_with_different_byte_values_is_not_mixed(self):
        # Byte values differ run to run (i offset) yet every run is owner-read: not a mixed-mode panel.
        state, reason = self.panel({"p70": ["owner"] * 3, "p66": ["owner"] * 3})
        self.assertEqual(state, "PASS", reason)

    def test_observed_mixed_modes_require_the_seven_pair_extension(self):
        state, reason = self.panel({"p70": ["owner", "entry", "entry"], "p66": ["entry"] * 3},
                                   bytes_by_mode={"owner": 15000, "entry": 14000})
        self.assertEqual(state, "UNRESOLVED")
        self.assertIn("mixed", reason)

    def test_unobserved_owner_mode_is_unresolved_not_inferred_from_bytes(self):
        state, reason = self.panel({"p70": [None] * 3, "p66": ["entry"] * 3})
        self.assertEqual(state, "UNRESOLVED")
        self.assertIn("unobserved", reason)


class OwnerObservationScope(unittest.TestCase):
    """The zero-tolerance owner floor depends on the owner question, not on unrelated unexplained opens."""

    def test_inexact_bytes_with_exact_owner_question_does_not_void_the_owner_floor(self):
        runs = {"r1": {"resource_observation": {"exact": False, "owner_read_exact": True}},
                "r2": {"resource_observation": {"exact": True, "owner_read_exact": True}}}
        self.assertTrue(batch_assess70.owner_observation_complete(runs))

    def test_unobserved_owner_question_voids_it_and_old_summaries_fall_back_to_exact(self):
        self.assertFalse(batch_assess70.owner_observation_complete(
            {"r": {"resource_observation": {"exact": True, "owner_read_exact": False}}}))
        self.assertFalse(batch_assess70.owner_observation_complete({"r": {"resource_observation": {"exact": False}}}))
        self.assertTrue(batch_assess70.owner_observation_complete({"r": {"resource_observation": {"exact": True}}}))
        self.assertFalse(batch_assess70.owner_observation_complete({"r": {}}))


if __name__ == "__main__":
    unittest.main()
