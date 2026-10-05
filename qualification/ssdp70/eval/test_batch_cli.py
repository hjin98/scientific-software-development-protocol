"""Batch CLI and aggregation-owner discriminators (no runtime needed).

The refusals under test occur before any evaluator could launch; the numeric tests feed the
production `quantitative_part` retained summary files.
"""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from unittest.mock import patch
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
        self.assertEqual(report["per_arm"]["p70"],{"runs":1,"inexact":1,"replacements":1,"scored_replacements":1})
        self.assertEqual(report["required"],[])

    def test_l_u_v_pre_r2_positive_other_unresolved_and_undisclosed_overflow_bar(self):
        mf,runs=self.setup_case();runs["original"]["owner_floor_state"]="FAIL"
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)   # a positive pre-R2 original is never replaced
        for change in ("other","overflow","r2"):
            mf,runs=self.setup_case();o=runs["original"]
            if change=="other":o["original_dispositions"]=[{"result":"unresolved"}]
            elif change=="overflow":o["resource_observation"]["accounting"]["reasons"]=["ledger overflowed"]
            else:o["owner_floor_adjudication"]["adjudicated"]=False
            slots,report=batch_assess70.replacement_slots(mf,runs)
            self.assertEqual(slots["original"],"original",change)
            self.assertFalse(report["records"][0]["scored"])
        o["owner_floor_adjudication"]["adjudicated"]=True
        o["resource_observation"]["accounting"]["reasons"]=["ledger overflowed"]
        o["replacement_review"]["overflow_cause"]="disclosed volume of distinct interval rows"
        self.assertEqual(batch_assess70.replacement_slots(mf,runs)[0]["original"],"replacement")

    def test_v_not_applicable_items_do_not_bar_but_fail_and_unresolved_do(self):
        for result,expected in (("not-applicable","replacement"),("pass","replacement"),("unresolved","original")):
            mf,runs=self.setup_case();runs["original"]["original_dispositions"]=[{"result":"pass"},{"result":result}]
            self.assertEqual(batch_assess70.replacement_slots(mf,runs)[0]["original"],expected,result)
        mf,runs=self.setup_case();runs["original"]["original_dispositions"]=[{"result":"pass"},{"result":"fail"}]
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)   # a failing original is never replaced

    def test_observation_adjudicated_needs_every_independent_attestation(self):
        mf,runs=self.setup_case();row=runs["original"]
        self.assertTrue(batch_assess70.observation_adjudicated(row))
        for path,value in ((("owner_floor_adjudication","adjudicated"),False),(("replacement_review","other_criteria_adjudicated"),False),
                           (("replacement_review","observation_only"),False),(("original_dispositions",),[]),(("original_dispositions",),[{"result":"fail"}])):
            broken=copy.deepcopy(row)
            if len(path)==2:broken[path[0]][path[1]]=value
            else:broken[path[0]]=value
            self.assertFalse(batch_assess70.observation_adjudicated(broken),path)

    def add_replacement(self,mf,runs,rid,question,**record):
        mf["runs"].append({**mf["runs"][1],"id":rid})
        runs[rid]={**runs["replacement"],**record}
        mf["package_access_replacements"].append({"original":"original","replacement":rid,"question":question})

    def test_one_slot_one_scored_run_partial_replacement_is_disclosed_and_the_rerun_must_resolve_all(self):
        mf,runs=self.setup_case()
        runs["replacement"]["owner_floor_state"]="UNRESOLVED"        # byte-exact, owner floor still open
        self.add_replacement(mf,runs,"replacement-2","bytes",owner_floor_state="PASS")
        slots,report=batch_assess70.replacement_slots(mf,runs)
        first,second=report["records"]
        self.assertFalse(first["scored"]);self.assertIn("does not resolve every available open question",first["reason"])
        self.assertTrue(second["scored"])
        self.assertEqual(slots["original"],"replacement-2")
        self.assertEqual(report["byte_slots"]["original"],"replacement-2");self.assertEqual(report["owner_slots"]["original"],"replacement-2")
        self.assertEqual(report["required"],[])
        self.assertEqual((report["per_arm"]["p70"]["replacements"],report["per_arm"]["p70"]["scored_replacements"]),(2,1))   # attempts vs scored
        self.add_replacement(mf,runs,"replacement-3","bytes",owner_floor_state="PASS")
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)    # cap of two independent reruns

    def test_a_resolved_slot_cannot_be_rerun_for_any_question(self):
        for question in ("bytes","owner-floor"):
            mf,runs=self.setup_case()
            self.add_replacement(mf,runs,"replacement-2",question)
            with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)

    def test_without_a_byte_bound_the_owner_floor_alone_decides_scoring_and_bytes_stay_pending(self):
        mf,runs=self.setup_case(bound=False)
        mf["package_access_replacements"][0]["question"]="owner-floor"
        runs["replacement"]["resource_observation"]={"exact":False}   # bytes not resolved, owner floor resolved
        slots,report=batch_assess70.replacement_slots(mf,runs)
        self.assertEqual(slots["original"],"replacement");self.assertEqual(report["owner_slots"]["original"],"replacement")
        self.assertEqual(report["byte_slots"]["original"],"original")
        self.assertTrue(any(v["original"]=="original" and v["questions"]==["bytes"] for v in report["required"]))

    def test_bn1_a_replacement_must_resolve_its_own_owner_floor_even_when_only_bytes_were_open(self):
        for owner_state, scored in (("UNRESOLVED", False), ("PASS", True)):
            mf, runs = self.setup_case(route="T1", question="bytes")
            runs["original"]["owner_floor_state"] = "PASS"             # only the byte question is open on the original
            runs["replacement"]["owner_floor_state"] = owner_state
            slots, report = batch_assess70.replacement_slots(mf, runs)
            self.assertEqual(report["records"][0]["scored"], scored, owner_state)
            self.assertEqual(slots["original"], "replacement" if scored else "original")

    def test_cr2_b1_a_declared_reserve_cannot_override_an_original_that_needed_no_replacement(self):
        for question in ("bytes","owner-floor"):                      # exact original, owner floor PASS: nothing is open
            mf,runs=self.setup_case(question=question);o=runs["original"]
            o.update(evidence_state="COMPLETE_ADMISSIBLE",owner_floor_state="PASS",resource_observation={"exact":True},
                     observation_only_inadmissibility=False)
            with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)
        mf,runs=self.setup_case(question="owner-floor",bound=False)    # only the byte question is open: an owner-floor reserve answers nothing
        runs["original"]["owner_floor_state"]="PASS"
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)
        mf,runs=self.setup_case(route="T7",question="t7-owner-floor")  # T7 owner floor already resolved: nothing for an owner-only rerun
        runs["original"]["owner_floor_state"]="PASS"
        with self.assertRaises(core70.ContractError):batch_assess70.replacement_slots(mf,runs)

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


class SlotScoringComposition(unittest.TestCase):
    """Independent-review B-2 (M36-M38): the production slot scorer must apply replacement byte slots,
    the T7 owner-floor-only override and the frozen disparity bound to the parts it computes."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def good(self, arm):
        return {"arm": arm, "evidence_state": "COMPLETE_ADMISSIBLE", "qualification_outcome": "PASS",
                "criteria": {"deterministic activation": "PASS", "harness/admissibility": "PASS"},
                "dispositions": [{"item": "i1", "measure": "m", "critical": False, "result": "pass"}],
                "owner_floor_state": "PASS", "resource_observation": {"exact": True}}

    def inexact(self, arm):
        row = {**self.good(arm), "evidence_state": "INADMISSIBLE", "qualification_outcome": "NOT_EVALUATED",
                "criteria": {"deterministic activation": "PASS", "harness/admissibility": "FAIL"},
                "observation_only_inadmissibility": True, "owner_floor_state": "UNRESOLVED",
                "resource_observation": {"exact": False, "accounting": {"reasons": []}},
                "owner_floor_adjudication": {"adjudicated": True, "r2_sequence": 3, "consequential_sequence": 9},
                "replacement_review": {"other_criteria_adjudicated": True, "observation_only": True, "overflow_cause": None},
                "original_dispositions": [{"item": "i1", "result": "pass"}]}
        row.pop("dispositions")      # production publishes dispositions only for COMPLETE_ADMISSIBLE runs
        return row

    def write(self, rid, **summary):
        (self.root / rid).mkdir(exist_ok=True)
        (self.root / rid / "summary.json").write_text(json.dumps(
            {"active_ssdp_bytes": 14000, "installed_entrypoint_bytes": 14000, "installed_owner_bytes": 46000,
             "owner_read_sequences": [], **summary}))

    def build(self, *, replaced, question, bound=1, owner_replacement=None, extra=(), original_overrides=None):
        """Three paired T1/T7/T8 fixed-cost opportunities per arm; one affected p70 run with a declared replacement."""
        runs, declared, opportunities = {}, [], []
        subject = {"commit": COMMIT, "package_sha256": SHA}
        for route in ("T1", "T7", "T8"):
            for arm in ("p70", "p66"):
                for i in range(3):
                    rid = f"{route}-{arm}-r{i}"
                    runs[rid] = self.good(arm); self.write(rid)
                    declared.append({"id": rid, "profile_key_sha256": SHA, "entry_stratum": "deterministic", "subject": subject,
                                     "replacement_case": "case-" + rid})
                    opportunities.append({"id": rid, "part": "fixed_cost", "route": route, "arm": arm, "fixture": "f",
                                          "profile_key_sha256": SHA, "realizations": [{"run": rid, "item": "i1"}]})
        for arm in ("p70", "p66"):
            rid = f"T7-{arm}-r0"
            opportunities.append({"id": "own-" + arm, "part": "owner_false_activation", "route": "T7", "arm": arm, "fixture": "f",
                                  "profile_key_sha256": SHA, "realizations": [{"run": rid, "item": "i1"}]})
        original = replaced
        opportunities.append({"id": "own-slot", "part": "owner_false_activation", "route": "T7" if original.startswith("T7") else "T1",
                              "arm": "p70", "fixture": "f", "profile_key_sha256": SHA, "realizations": [{"run": original, "item": "i1"}]})
        runs[original] = {**self.inexact("p70"), **(original_overrides or {})}
        self.write(original, active_ssdp_bytes=None, owner_read_sequences=None, resource_observation={"exact": False})
        replacement = original + "-repl"
        runs[replacement] = {**self.good("p70"), **(owner_replacement or {})}
        self.write(replacement)
        declared.append({"id": replacement, "profile_key_sha256": SHA, "entry_stratum": "deterministic", "subject": subject,
                         "replacement_case": "case-" + original})
        replacements = [{"original": original, "replacement": replacement, "question": question}]
        for rid, q, overrides in extra:      # further declared attempts at the same slot, in order
            runs[rid] = {**self.good("p70"), **overrides}; self.write(rid)
            declared.append({"id": rid, "profile_key_sha256": SHA, "entry_stratum": "deterministic", "subject": subject,
                             "replacement_case": "case-" + original})
            replacements.append({"original": original, "replacement": rid, "question": q})
        manifest = {"candidate_arm": "p70", "comparator_arm": "p66", "cost_comparator_arm": "p66", "runs": declared,
                    "family": {"criterion_to_keys": {part: [SHA] for part in core70.CAMPAIGN_PARTS}}, "offered_profiles": [SHA],
                    "opportunities": opportunities,
                    "package_access_replacements": replacements}
        if bound is not None:
            manifest["package_access_policy"] = {"byte_inexact_disparity_bound": {"value": bound, "stakeholder_confirmation": "frozen record"}}
        result = {"runs": runs, "errors": []}
        batch_assess70.score_slots(result, manifest, {r["id"]: r for r in declared}, self.root, {SHA: {}})
        return result

    def test_m36_replacement_byte_summary_resolves_fixed_cost_only_through_the_byte_slot(self):
        result = self.build(replaced="T1-p70-r0", question="bytes")
        self.assertEqual(result["package_access_replacements"]["byte_slots"]["T1-p70-r0"], "T1-p70-r0-repl")
        self.assertEqual(result["parts"]["fixed_cost"]["state"], "PASS", result["parts"]["fixed_cost"])
        unbounded = self.build(replaced="T1-p70-r0", question="bytes", bound=None)   # no frozen bound: byte replacement unavailable
        self.assertEqual(unbounded["package_access_replacements"]["byte_slots"]["T1-p70-r0"], "T1-p70-r0")
        self.assertEqual(unbounded["parts"]["fixed_cost"]["state"], "UNRESOLVED")

    def test_m38_frozen_disparity_bound_makes_every_byte_comparison_unresolved(self):
        for part in ("fixed_cost", "active_material", "comparative"):
            self.assertNotEqual(self.build(replaced="T1-p70-r0", question="bytes", bound=1)["parts"][part].get("reason"),
                                "byte inexact-run disparity exceeds frozen bound")
        result = self.build(replaced="T1-p70-r0", question="bytes", bound=0)
        self.assertTrue(result["package_access_replacements"]["byte_disparity_exceeded"])
        for part in ("fixed_cost", "active_material", "comparative"):
            self.assertEqual(result["parts"][part]["state"], "UNRESOLVED", part)
            self.assertEqual(result["parts"][part]["reason"], "byte inexact-run disparity exceeds frozen bound")

    def test_m37_t7_owner_floor_only_replacement_decides_the_owner_floor_but_not_the_burden_slot(self):
        result = self.build(replaced="T7-p70-r0", question="t7-owner-floor", owner_replacement={"owner_floor_state": "FAIL"})
        bookkeeping = result["package_access_replacements"]
        self.assertEqual(bookkeeping["owner_slots"]["T7-p70-r0"], "T7-p70-r0-repl")
        self.assertEqual(bookkeeping["byte_slots"]["T7-p70-r0"], "T7-p70-r0")
        self.assertEqual(result["parts"]["owner_false_activation"]["state"], "FAIL")
        clean = self.build(replaced="T7-p70-r0", question="t7-owner-floor")
        self.assertNotEqual(clean["parts"]["owner_false_activation"]["state"], "FAIL")


    def test_b1_a_partial_replacement_that_carries_a_positive_pre_r2_read_stands_and_bars_the_slot(self):
        """Independent text review B-1: outcome selection must not discard a definite failure seen in a replacement."""
        failing_partial = {"resource_observation": {"exact": False}, "owner_floor_state": "FAIL"}
        result = self.build(replaced="T1-p70-r0", question="bytes", owner_replacement=failing_partial)
        self.assertEqual(result["parts"]["owner_false_activation"]["state"], "FAIL")            # a single failing attempt stands
        record = result["package_access_replacements"]["records"][0]
        self.assertTrue(record["scored"] and record["standing_failure"])
        self.assertEqual(result["package_access_replacements"]["owner_slots"]["T1-p70-r0"], "T1-p70-r0-repl")
        with self.assertRaises(core70.ContractError):         # a cleaner second rerun of the barred slot is refused outright
            self.build(replaced="T1-p70-r0", question="bytes", owner_replacement=failing_partial,
                       extra=[("T1-p70-r0-repl2", "bytes", {})])

    def test_b1_a_deterministic_activation_failure_in_a_replacement_also_stands(self):
        failing = {"criteria": {"deterministic activation": "FAIL", "harness/admissibility": "PASS"}}
        result = self.build(replaced="T1-p70-r0", question="bytes", owner_replacement=failing)
        record = result["package_access_replacements"]["records"][0]
        self.assertTrue(record["scored"] and record["standing_failure"])
        self.assertEqual(result["package_access_replacements"]["owner_slots"]["T1-p70-r0"], "T1-p70-r0-repl")


    def test_r2_1_no_declared_run_loses_a_definite_failure_whatever_the_original_or_the_evidence_state(self):
        """Independent text review R2-1, each case executed through score_slots."""
        owner_fail = {"owner_floor_state": "FAIL"}
        cases = {
            "original unresolved on another criterion": dict(original_overrides={"original_dispositions": [{"item": "i1", "result": "unresolved"}]}, owner_replacement=owner_fail),
            "original not yet adjudicated": dict(original_overrides={"owner_floor_adjudication": {"adjudicated": False, "r2_sequence": None, "consequential_sequence": None}}, owner_replacement=owner_fail),
            "original with undisclosed overflow": dict(original_overrides={"resource_observation": {"exact": False, "accounting": {"reasons": ["ledger overflowed"]}}}, owner_replacement=owner_fail),
            "unusable replacement evidence": dict(owner_replacement={**owner_fail, "evidence_state": "EXECUTION_ERROR"}),
            "partial replacement": dict(owner_replacement={"resource_observation": {"exact": False}, **owner_fail}),
        }
        for name, kwargs in cases.items():
            result = self.build(replaced="T1-p70-r0", question="bytes", **kwargs)
            self.assertEqual(result["parts"]["owner_false_activation"]["state"], "FAIL", name)
            self.assertTrue(result["package_access_replacements"]["records"][0].get("standing_failure"), name)

    def test_r2_1_failing_or_unresolved_dispositions_in_a_replacement_stand_and_bar_the_rerun(self):
        for disposition in ({"item": "i1", "measure": "m", "critical": True, "result": "fail"},
                            {"item": "i1", "measure": "m", "critical": False, "result": "unresolved"}):
            kwargs = dict(replaced="T1-p70-r0", question="bytes", owner_replacement={"dispositions": [disposition]})
            result = self.build(**kwargs)
            self.assertTrue(result["package_access_replacements"]["records"][0]["standing_failure"], disposition)
            with self.assertRaises(core70.ContractError):          # no rerun-until-clean
                self.build(**kwargs, extra=[("T1-p70-r0-repl2", "bytes", {})])

    def test_r2_1_t7_owner_only_rerun_with_an_activation_failure_fails_the_activation_criterion(self):
        failing = {"criteria": {"deterministic activation": "FAIL", "harness/admissibility": "PASS"}}
        result = self.build(replaced="T7-p70-r0", question="t7-owner-floor", owner_replacement=failing)
        self.assertTrue(result["package_access_replacements"]["records"][0]["standing_failure"])
        self.assertEqual(result["profiles"][SHA]["deterministic activation"], "FAIL")
        self.assertEqual(result["package_access_replacements"]["byte_slots"]["T7-p70-r0"], "T7-p70-r0")     # median value unchanged
        clean = self.build(replaced="T7-p70-r0", question="t7-owner-floor")
        self.assertEqual(clean["profiles"][SHA]["deterministic activation"], "PASS")


    def test_r3_1_a_replacement_declared_for_an_original_with_a_definite_failure_is_refused_not_dropped(self):
        tolerated = [{"item": "i1", "measure": "m", "critical": False, "result": "fail"}]       # a campaign may tolerate this one
        for original_overrides in ({"original_dispositions": tolerated},
                                   {"criteria": {"deterministic activation": "FAIL", "harness/admissibility": "FAIL"}},
                                   {"owner_floor_state": "FAIL"}):
            with self.assertRaises(core70.ContractError):
                self.build(replaced="T1-p70-r0", question="bytes", original_overrides=original_overrides,
                           owner_replacement={"owner_floor_state": "FAIL"})

    def test_r3_n2_t7_owner_only_rerun_with_a_critical_fail_disposition_counts_as_a_critical_failure(self):
        failing = {"dispositions": [{"item": "i1", "measure": "m", "critical": True, "result": "fail"}]}
        result = self.build(replaced="T7-p70-r0", question="t7-owner-floor", owner_replacement=failing)
        self.assertEqual(result["critical_failures"].get("p70"), 1)
        self.assertEqual(result["arms"]["p70"]["dispositions"]["fail"], 1)
        clean = self.build(replaced="T7-p70-r0", question="t7-owner-floor")
        self.assertEqual(clean["critical_failures"].get("p70", 0), 0)

    def test_inadmissible_standing_failure_counts_failures_and_blocks_without_scoring_retained_passes(self):
        retained = [{"item": "i1", "measure": "m", "critical": True, "result": "fail"},
                    {"item": "i2", "measure": "m", "critical": False, "result": "pass"},
                    {"item": "i3", "measure": "m", "critical": True, "result": "unresolved"}]
        for route, question in (("T1", "bytes"), ("T7", "t7-owner-floor")):
            with self.subTest(route=route):
                failure = {"evidence_state": "INADMISSIBLE", "qualification_outcome": "NOT_EVALUATED",
                           "dispositions": [], "original_dispositions": retained}
                result = self.build(replaced=route + "-p70-r0", question=question, owner_replacement=failure)
                self.assertTrue(result["package_access_replacements"]["records"][0]["standing_failure"])
                self.assertEqual(result["critical_failures"].get("p70"), 1)
                tallies = result["arms"]["p70"]["dispositions"]
                self.assertEqual(tallies["fail"], 1)
                self.assertEqual(tallies["unresolved"], 1)
                self.assertEqual(tallies["pass"], 8)

    def test_t7_unresolved_critical_block_reaches_the_final_aggregation_criterion(self):
        """Real slot/part/final criterion owners; validated assessment loading is controlled below them."""
        captured = {}
        score = batch_assess70.score_slots
        def capture(result, mf, expected, out, keys):
            for arm in ("p70", "p66"):
                base = next(d for d in mf["runs"] if d["id"] == "T1-" + arm + "-r0")
                for i in range(3):
                    rid = "critical-" + arm + "-" + str(i)
                    declaration = {**base, "id": rid}
                    mf["runs"].append(declaration); expected[rid] = declaration
                    result["runs"][rid] = self.good(arm); self.write(rid)
                ids = [d["id"] for d in mf["runs"] if result["runs"][d["id"]]["arm"] == arm
                       and not d["id"].endswith("-repl")]
                for i, rid in enumerate(ids):
                    mf["opportunities"].append({"id": "critical-" + arm + "-" + str(i), "part": "critical",
                        "arm": arm, "fixture": "f", "profile_key_sha256": SHA, "realizations": [{"run": rid, "item": "i1"}]})
            self.write("T7-p70-r0", active_ssdp_bytes=14000, owner_read_sequences=[])
            captured.update(manifest=copy.deepcopy(mf), runs=copy.deepcopy(result["runs"]))
            return score(result, mf, expected, out, keys)
        with patch.object(batch_assess70, "score_slots", side_effect=capture):
            self.build(replaced="T7-p70-r0", question="t7-owner-floor",
                owner_replacement={"dispositions": [{"item": "i1", "measure": "m", "critical": True, "result": "unresolved"}]},
                original_overrides={"evidence_state": "COMPLETE_ADMISSIBLE", "qualification_outcome": "PASS",
                    "criteria": {"harness/admissibility": "PASS", "deterministic activation": "PASS"},
                    "resource_observation": {"exact": True},
                    "dispositions": [{"item": "i1", "measure": "m", "critical": True, "result": "pass"}]})
        mf, runs = captured["manifest"], captured["runs"]
        mf.update(purpose="qualification", scope_id="synthetic-aggregation-test", family_record_sha256=SHA)
        mf["family"].update(ordered_keys=[SHA], family_id="synthetic-family", panels={"ordinary": {"key": "ordinary"}})
        digest = core70.stable_json_sha256(mf)
        for declaration in mf["runs"]:
            rid = declaration["id"]
            scope = {"purpose": mf["purpose"], "scope_id": mf["scope_id"], "manifest_sha256": digest,
                "campaign_record_sha256": digest, "family_record_sha256": SHA, "primary_family_id": mf["family"]["family_id"],
                "scoring_manifest_sha256": declaration.get("scoring_manifest_sha256")}
            identity = {**declaration, "accounting": scope, "identity_sha256": SHA, "arm": runs[rid]["arm"], "episode": "E1",
                "requirements": {"required_artifacts_sha256": SHA, "required_oracles_sha256": SHA}}
            directory = self.root / rid
            summary = json.loads((directory / "summary.json").read_text())
            summary.update(accounting=scope, run_identity_sha256=SHA, fixture_run_id=rid)
            for name, value in (("run-identity.json", identity), ("summary.json", summary),
                    ("requirements-snapshot.json", {}), ("assessment.json", {"accounting": scope, "run_identity_sha256": SHA})):
                (directory / name).write_text(json.dumps(value))
        # This test does not claim fixture admission: only the aggregation
        # consumers execute; raw-run validation/assessment is the controlled boundary.
        with patch.object(core70, "campaign_manifest_errors", return_value=[]), \
             patch.object(core70, "validate_accounting_identity", return_value=[]), \
             patch.object(core70, "requirements_from_snapshot", return_value=None), \
             patch.object(core70, "validate_complete_run", return_value=[]), \
             patch.object(core70, "production_assessment", side_effect=lambda summary, *a, **k: copy.deepcopy(runs[summary["fixture_run_id"]])):
            result = batch_assess70.aggregate_assessments(self.root, mf)
            runs["T7-p70-r0-repl"]["dispositions"].append(
                {"item": "i2", "measure": "m", "critical": True, "result": "fail"})
            failed = batch_assess70.aggregate_assessments(self.root, mf)
        self.assertEqual(result["criteria"]["no critical failure"], "UNRESOLVED")
        self.assertEqual(failed["criteria"]["no critical failure"], "FAIL")
        self.assertEqual(result["critical_unresolved"], {"p70": 1})
        self.assertEqual(result["arms"]["p70"]["dispositions"]["unresolved"], 1)
        self.assertEqual(result["parts"]["owner_false_activation"]["state"], "PASS")
        self.assertEqual(result["parts"]["fixed_cost"]["state"], "PASS")
        self.assertEqual(result["package_access_replacements"]["byte_slots"]["T7-p70-r0"], "T7-p70-r0")
        self.assertNotEqual(result["qualification_outcome"], "PASS")

    def test_t7_noncritical_block_uses_its_binding_and_unmapped_blocks_are_refused(self):
        for item, raises in (("i1", False), ("unbound", True)):
            kwargs = dict(replaced="T7-p70-r0", question="t7-owner-floor", owner_replacement={
                "dispositions": [{"item": item, "measure": "m", "critical": False, "result": "unresolved"}]})
            if raises:
                with self.assertRaisesRegex(core70.ContractError, "no qualification criterion binding"):
                    self.build(**kwargs)
            else:
                result = self.build(**kwargs)
                self.assertEqual(result["parts"]["owner_false_activation"]["state"], "UNRESOLVED")
                self.assertEqual(result["runs"]["T7-p70-r0-repl"]["owner_floor_state"], "PASS")
                self.assertEqual(result["critical_unresolved"], {})
                self.assertEqual(result["arms"]["p70"]["dispositions"]["unresolved"], 1)


    def test_cr2_b2_activation_counts_every_declared_deterministic_run_not_only_the_scored_slots(self):
        undetermined = {"resource_observation": {"exact": True}, "owner_floor_state": "UNRESOLVED",
                        "criteria": {"deterministic activation": "NOT_EVALUATED", "harness/admissibility": "PASS"}}
        result = self.build(replaced="T1-p70-r0", question="bytes", owner_replacement=undetermined,
                            extra=[("T1-p70-r0-repl2", "bytes", {})])
        first, second = result["package_access_replacements"]["records"]
        self.assertFalse(first["scored"]);self.assertTrue(second["scored"])
        self.assertEqual(result["profiles"][SHA]["deterministic activation"], "NOT_EVALUATED")     # an unscored launched run still counts
        clean = self.build(replaced="T1-p70-r0", question="bytes")
        self.assertEqual(clean["profiles"][SHA]["deterministic activation"], "PASS")
