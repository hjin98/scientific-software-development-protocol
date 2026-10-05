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

    def panel(self, modes, bytes_by_mode=None, cost=None, unknown=False):
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
                if unknown and mode is None:
                    summary["active_ssdp_bytes"] = None
                    summary["resource_observation"] = {"exact":False}
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
        runs = {"r1": {"resource_observation": {"exact": False, "owner_floor_exact": True}},
                "r2": {"resource_observation": {"exact": True, "owner_floor_exact": True}}}
        self.assertTrue(batch_assess70.owner_observation_complete(runs))

    def test_unobserved_owner_question_voids_it_and_old_summaries_fall_back_to_exact(self):
        self.assertFalse(batch_assess70.owner_observation_complete(
            {"r": {"resource_observation": {"exact": True, "owner_floor_exact": False}}}))
        self.assertFalse(batch_assess70.owner_observation_complete({"r": {"resource_observation": {"exact": False}}}))
        self.assertTrue(batch_assess70.owner_observation_complete({"r": {"resource_observation": {"exact": True}}}))
        self.assertFalse(batch_assess70.owner_observation_complete({"r": {}}))


if __name__ == "__main__":
    unittest.main()


class T7Unknown(T7Mode):
    def test_v_unknown_original_triggers_pair_addition_at_three_and_five(self):
        state,reason=self.panel({"p70":[None]*3,"p66":["entry"]*3},unknown=True)
        self.assertEqual(state,"UNRESOLVED");self.assertIn("3 -> 5",reason)

    def test_v_unknown_minority_at_seven_is_adversarial_interval_not_lower_bound(self):
        state,reason=self.panel({"p70":[None]+["entry"]*6,"p66":[None]+["entry"]*6},unknown=True)
        self.assertEqual(state,"PASS",reason)
        self.assertIn("median upper",reason);self.assertIn("median lower",reason)
        self.assertIsNone(json.loads((self.root/"T7-p70-r0/summary.json").read_text())["active_ssdp_bytes"])

    def test_v_majority_unknown_candidate_or_comparator_never_manufactures_pass(self):
        state,reason=self.panel({"p70":[None]*4+["entry"]*3,"p66":["entry"]*7},unknown=True)
        self.assertEqual(state,"UNRESOLVED");self.assertIn("unbounded above",reason)


class ReplacementBookkeeping(unittest.TestCase):
    def setup_case(self,route="T1",question="bytes",bound=True):
        mf=manifest(["original","replacement"])
        for d in mf["runs"]:d["replacement_case"]="affected-case"
        mf["opportunities"]=[{"part":"active_material","route":route,"arm":"p70",
            "realizations":[{"run":"original"}]}]
        mf["package_access_replacements"]=[{"original":"original","replacement":"replacement","question":question}]
        if bound:mf["package_access_policy"]={"byte_inexact_disparity_bound":{"value":1,"stakeholder_confirmation":"frozen stakeholder record"}}
        original={"arm":"p70","evidence_state":"INADMISSIBLE","qualification_outcome":"NOT_EVALUATED",
            "criteria":{"deterministic activation":"PASS"},"observation_only_inadmissibility":True,
            "resource_observation":{"exact":False,"accounting":{"reasons":[]}},"owner_floor_state":"UNRESOLVED",
            "owner_floor_adjudication":{"adjudicated":True,"r2_sequence":3,"consequential_sequence":9},
            "replacement_review":{"other_criteria_adjudicated":True,"observation_only":True,"overflow_cause":None},
            "original_dispositions":[{"result":"pass"}],"owner_load_hit":True}
        replacement={"arm":"p70","evidence_state":"COMPLETE_ADMISSIBLE","qualification_outcome":"PASS",
            "criteria":{"deterministic activation":"PASS"},"resource_observation":{"exact":True},"owner_floor_state":"PASS"}
        return mf,{"original":original,"replacement":replacement}

    def test_v_original_retained_replacement_scored_all_and_post_r2_hit_does_not_bar(self):
        mf,runs=self.setup_case();slots,report=batch_assess70.replacement_slots(mf,runs)
        self.assertEqual(slots,{"original":"replacement"})
        self.assertEqual(report["byte_slots"],slots);self.assertEqual(report["owner_slots"],slots)
        self.assertTrue(runs["original"]["owner_load_hit"])
        self.assertEqual(report["per_arm"]["p70"],{"runs":1,"inexact":1,"replacements":1})
        self.assertEqual(report["required"],[])

    def test_l_u_v_pre_r2_positive_other_unresolved_and_undisclosed_overflow_bar(self):
        for change in ("positive","other","overflow","r2"):
            mf,runs=self.setup_case();o=runs["original"]
            if change=="positive":o["owner_floor_state"]="FAIL"
            elif change=="other":o["original_dispositions"]=[{"result":"unresolved"}]
            elif change=="overflow":o["resource_observation"]["accounting"]["reasons"]=["ledger overflowed"]
            else:o["owner_floor_adjudication"]["adjudicated"]=False
            slots,report=batch_assess70.replacement_slots(mf,runs)
            self.assertEqual(slots["original"],"original",change)
            self.assertFalse(report["records"][0]["scored"])
        o["owner_floor_adjudication"]["adjudicated"]=True
        o["resource_observation"]["accounting"]["reasons"]=["ledger overflowed"]
        o["replacement_review"]["overflow_cause"]="disclosed volume of distinct interval rows"
        self.assertEqual(batch_assess70.replacement_slots(mf,runs)[0]["original"],"replacement")

    def test_v_missing_byte_bound_keeps_byte_question_pending_but_owner_has_no_campaign_cap(self):
        mf,runs=self.setup_case(bound=False)
        self.assertEqual(batch_assess70.replacement_slots(mf,runs)[0]["original"],"original")
        mf["package_access_replacements"][0]["question"]="owner-floor"
        slots,report=batch_assess70.replacement_slots(mf,runs)
        self.assertEqual(slots["original"],"replacement")
        self.assertEqual(report["owner_slots"]["original"],"replacement")
        self.assertEqual(report["byte_slots"]["original"],"original")

    def test_v_t7_owner_only_is_outside_median_and_cap_is_per_affected_original(self):
        mf,runs=self.setup_case(route="T7",question="t7-owner-floor")
        slots,report=batch_assess70.replacement_slots(mf,runs)
        self.assertEqual(slots["original"],"original")
        self.assertEqual(report["byte_slots"]["original"],"original")
        self.assertEqual(report["owner_slots"]["original"],"replacement")
        mf["package_access_replacements"][0]["question"]="bytes"
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)

    def test_v_cap_disallows_third_independent_rerun_and_reuse_of_one_identity(self):
        mf,runs=self.setup_case()
        requests=mf["package_access_replacements"]
        for i in range(2):
            rid=f"replacement-{i}";mf["runs"].append({**mf["runs"][1],"id":rid})
            runs[rid]={**runs["replacement"],"resource_observation":{"exact":False}}
            requests.append({"original":"original","replacement":rid,"question":"bytes"})
        runs["replacement"]["resource_observation"]["exact"]=False
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)


class PositiveIdentity(unittest.TestCase):
 def test_positive_owner_and_hit_still_require_frozen_profile_identity(self):
  for part in ('owner_false_activation','r2_analysis'):
   manifest={'candidate_arm':'p70','comparator_arm':'p66','family':{'criterion_to_keys':{part:['wanted']}},'runs':[{'id':'r','profile_key_sha256':'wrong','entry_stratum':'deterministic'}], 'opportunities':[{'id':'o','part':part,'arm':'p70','fixture':'f','profile_key_sha256':'wanted','realizations':[{'run':'r','item':'i'}]}]}
   with self.subTest(part=part),self.assertRaises(core70.ContractError):
    batch_assess70.aggregate_parts(manifest,{'r':{'owner_floor_state':'PASS','owner_load_hit':True}},Path('/tmp'))
