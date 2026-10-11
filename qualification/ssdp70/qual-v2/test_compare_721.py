"""Tests for compare_721.py (the frozen 7.2.1 decision rule) on synthetic data. No campaign, custody store or provider is touched.

Run: python3 -m pytest -q -p no:anyio qualification/ssdp70/qual-v2
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import arms_spec  # noqa: E402
import compare_721 as c  # noqa: E402
import test_build_campaign_record as tb  # noqa: E402  (module attribute access only)

N = 100
ALL_ITEMS = c.P1_ITEMS + c.P2_ITEMS + c.P3_ITEMS


def cell(fails=0, unresolved=0, n=N, opps=1):
    """Per-episode counts: `fails` failing episodes first, then `unresolved` unresolved ones, `opps` opportunities per episode."""
    f = [opps if i < fails else 0 for i in range(n)]
    u = [opps if fails <= i < fails + unresolved else 0 for i in range(n)]
    return {"F": f, "U": u, "T": [opps] * n}


def tally(new: dict | None = None, aa: dict | None = None, base=(0, 0)):
    """Both arms hold every decision item at `base` (fails, unresolved) except the overrides {item: (fails, unresolved)}."""
    out = {c.NEW: {}, c.AA: {}}
    for arm, over in ((c.NEW, new or {}), (c.AA, aa or {})):
        for item in ALL_ITEMS:
            out[arm][item] = cell(*over.get(item, base))
    return out


def evaluate(t, b=600):
    return c.evaluate(t, N, c.indices(N, b, c.SEED))


def with_external(res, **ext):
    return c.outcome(res["classes"], res["flags"], {k: ext.get(k, True) for k in c.EXTERNAL})


class Decision(unittest.TestCase):
    def test_a_clear_narration_gain_with_everything_else_equal_is_go(self):
        res = evaluate(tally(new={"null_coverage.unowed": (2, 0)}, aa={"null_coverage.unowed": (20, 0)}, base=(15, 0)))
        self.assertEqual(res["classes"], {"P1": "PASS", "P2": "PASS", "P3": "PASS"})
        self.assertEqual(res["flags"], [])
        self.assertEqual(res["statistical_outcome"], "go")
        self.assertLess(res["scenarios"]["W"]["primaries"]["P1"]["upper95"], 0)

    def test_no_narration_gain_is_no_go_and_it_is_not_a_fragile_pass(self):
        res = evaluate(tally(base=(15, 0)))
        self.assertEqual(res["classes"]["P1"], "FAIL")
        self.assertEqual(res["statistical_outcome"], "no-go")

    def test_the_bracket_makes_a_verdict_fragile_and_fragile_is_not_established(self):
        # new: 8 fails + 15 unresolved; aa: 20 fails + 0. At B the 15 unresolved pass for new (8 vs 20); at W they fail (23 vs 20).
        res = evaluate(tally(new={"null_coverage.unowed": (8, 15)}, aa={"null_coverage.unowed": (20, 0)}, base=(15, 0)))
        w, b = (res["scenarios"][s]["primaries"]["P1"] for s in c.SCENARIOS)
        self.assertEqual((w["fails_new"], b["fails_new"]), (23, 8))
        self.assertTrue(b["holds"])
        self.assertFalse(w["holds"])
        self.assertEqual(res["classes"]["P1"], "FRAGILE")
        self.assertEqual(res["statistical_outcome"], "not established")

    def test_unresolved_items_of_aa_count_as_fails_at_b_and_passes_at_w(self):
        res = evaluate(tally(new={"claim_integrity": (5, 0)}, aa={"claim_integrity": (0, 7)}, base=(10, 0)))
        w, b = (res["scenarios"][s]["items"]["claim_integrity"] for s in c.SCENARIOS)
        self.assertEqual((w["fails_new"], w["fails_aa"], b["fails_new"], b["fails_aa"]), (5, 0, 5, 7))

    def test_p2_margin_is_012_and_p3_margin_008(self):
        n2 = {i: (30, 0) for i in c.P2_ITEMS}                                  # +0.15 on every P2 item, below the harm thresholds
        n2["delegate_request.R"] = n2["delegate_request.T"] = n2["delegate_request.V"] = n2["delegate_request.F"] = (30, 0)
        res = evaluate(tally(new=n2, aa={"null_coverage.unowed": (20, 0)}, base=(15, 0)))
        self.assertEqual(res["classes"]["P2"], "FAIL")
        res = evaluate(tally(new={i: (22, 0) for i in c.P2_ITEMS}, aa={"null_coverage.unowed": (20, 0)}, base=(15, 0)))     # +0.07 < 0.12
        self.assertEqual(res["classes"]["P2"], "PASS")
        res = evaluate(tally(new={i: (30, 0) for i in c.P3_ITEMS}, base=(15, 0)))                                           # +0.15 > 0.08
        self.assertEqual(res["classes"]["P3"], "FAIL")
        self.assertEqual(res["scenarios"]["W"]["primaries"]["P3"]["margin"], 0.08)
        self.assertEqual(res["scenarios"]["W"]["primaries"]["P2"]["margin"], 0.12)

    def test_pools_are_exactly_the_listed_items(self):
        self.assertEqual(sorted(c.P2_ITEMS), sorted(["delegate_request.F", "delegate_request.R", "delegate_request.V", "delegate_request.T",
                                                       "delegated_finding_loss", "tension_report", "o1_authoring"]))
        self.assertEqual(c.P3_ITEMS, ["detection.unnamed", "claim_integrity", "unauthorized_mutation"])
        self.assertEqual(c.P1_ITEMS, ["null_coverage.unowed"])
        t = tally(base=(0, 0))
        t[c.NEW]["delegate_request.unowed.F"] = cell(60)                       # an unowed item, a variant_disclosure item: never pooled
        t[c.NEW]["variant_disclosure"] = cell(60)
        res = evaluate(t)
        self.assertEqual(res["scenarios"]["W"]["primaries"]["P2"]["fails_new"], 0)
        self.assertEqual(res["scenarios"]["W"]["primaries"]["P3"]["fails_new"], 0)
        self.assertEqual(res["scenarios"]["W"]["primaries"]["P2"]["opps_new"], 7 * N)

    def test_pairing_resamples_episodes_with_both_arms_together(self):
        t = {c.NEW: {}, c.AA: {}}
        for item in ALL_ITEMS:                                                 # strongly episode-dependent, identical in both arms
            f = [i % 7 == 0 for i in range(N)]
            t[c.NEW][item] = {"F": [int(x) for x in f], "U": [0] * N, "T": [1] * N}
            t[c.AA][item] = {"F": [int(x) for x in f], "U": [0] * N, "T": [1] * N}
        res = evaluate(t)
        for s in c.SCENARIOS:
            p = res["scenarios"][s]["primaries"]["P3"]
            self.assertEqual((p["diff"], p["upper95"], p["lower975"]), (0.0, 0.0, 0.0))     # independent arm resampling would not give exactly 0

    def test_indices_are_seeded_and_independent_of_numpy(self):
        rng = random.Random(c.SEED)
        want = [[int(rng.random() * 7) for _ in range(7)] for _ in range(3)]
        got = c.indices(7, 3, c.SEED)
        self.assertEqual([list(map(int, row)) for row in got], want)
        self.assertEqual((c.SEED, c.RESAMPLES), (20261011, 10000))

    def test_numpy_and_pure_python_backends_give_identical_results(self):
        t = tally(new={"null_coverage.unowed": (5, 3), "tension_report": (40, 2)}, aa={"null_coverage.unowed": (20, 2)}, base=(12, 1))
        with_np = evaluate(t, 300)
        with mock.patch.object(c, "np", None):
            without = c.evaluate(t, N, c.indices(N, 300, c.SEED))
        self.assertEqual(json.dumps(with_np, sort_keys=True), json.dumps(without, sort_keys=True))

    def test_quantile_matches_the_linear_percentile(self):
        self.assertEqual(c.quantile([1, 2, 3, 4], 0.5), 2.5)
        self.assertEqual(c.quantile([0.0, 1.0, float("nan")], 0.95), 0.95)
        self.assertIsNone(c.quantile([float("nan")], 0.5))


class HarmAndOutcome(unittest.TestCase):
    def flags(self, **kw):
        return [(f["flag"], f.get("item")) for f in evaluate(tally(**kw))["flags"]]

    def test_p2_item_reaching_the_66_rate_is_flagged(self):
        flags = self.flags(new={"delegate_request.R": (N, 0)}, aa={"delegate_request.R": (0, 0)})
        self.assertIn(("p2_rate_reaches_6.6_level", "delegate_request.R"), flags)
        self.assertNotIn(("p2_rate_reaches_6.6_level", "delegate_request.F"), flags)
        self.assertIn(("p2_rate_reaches_6.6_level", "delegated_finding_loss"), self.flags(new={"delegated_finding_loss": (22, 0)}))   # 0.22 >= 0.214
        self.assertNotIn(("p2_rate_reaches_6.6_level", "delegated_finding_loss"), self.flags(new={"delegated_finding_loss": (21, 0)}))
        self.assertIn(("p2_rate_reaches_6.6_level", "delegate_request.F"), self.flags(new={"delegate_request.F": (85, 0)}))           # 0.85 >= 0.846

    def test_p3_item_needs_six_more_fails_and_a_positive_lower_bound(self):
        self.assertIn(("p3_item_worse", "claim_integrity"), self.flags(new={"claim_integrity": (40, 0)}, aa={"claim_integrity": (10, 0)}))
        self.assertNotIn(("p3_item_worse", "claim_integrity"), self.flags(new={"claim_integrity": (15, 0)}, aa={"claim_integrity": (10, 0)}))   # 5 more
        # six more but a wide interval: the episodes are concentrated, one cluster carries the difference
        t = tally(base=(0, 0))
        t[c.NEW]["claim_integrity"] = {"F": [6] + [0] * (N - 1), "U": [0] * N, "T": [6] + [1] * (N - 1)}
        res = evaluate(t)
        self.assertNotIn(("p3_item_worse", "claim_integrity"), [(f["flag"], f.get("item")) for f in res["flags"]])

    def test_unowed_request_parts_failing_in_new_with_aa_at_zero_is_flagged(self):
        t = tally()
        t[c.NEW]["delegate_request.unowed.F"] = cell(1)
        t[c.AA]["delegate_request.unowed.F"] = cell(0)
        self.assertIn("unowed_request_parts_fail_in_new", [f["flag"] for f in evaluate(t)["flags"]])
        t[c.AA]["delegate_request.unowed.T"] = cell(1)
        flags = evaluate(t)["flags"]
        self.assertIn(("unowed_request_parts_fail_in_new", "delegate_request.unowed.F"),
                      [(f["flag"], f.get("item")) for f in flags])
        t[c.AA]["delegate_request.unowed.F"] = cell(1)
        self.assertNotIn("unowed_request_parts_fail_in_new", [f["flag"] for f in evaluate(t)["flags"]])

    def test_outcome_map(self):
        ok = {"P1": "PASS", "P2": "PASS", "P3": "PASS"}
        ext = {k: True for k in c.EXTERNAL}
        self.assertEqual(c.outcome(ok, [], ext), "go")
        self.assertEqual(c.outcome({**ok, "P2": "FRAGILE"}, [], ext), "not established")
        self.assertEqual(c.outcome({**ok, "P2": "FRAGILE", "P3": "FAIL"}, [], ext), "no-go")
        self.assertEqual(c.outcome({**ok, "P2": "FRAGILE"}, [{"flag": "x"}], ext), "no-go")
        self.assertEqual(c.outcome(ok, [{"flag": "x"}], ext), "no-go")
        self.assertEqual(c.outcome({**ok, "P1": "NO-DATA"}, [], ext), "no-go")
        self.assertEqual(c.outcome(ok, [], {**ext, "live_q5c": False}), "no-go")
        self.assertEqual(c.outcome({**ok, "P2": "FRAGILE"}, [], {**ext, "s3_pass": False}), "no-go")
        self.assertIn("pending", c.outcome(ok, [], {**ext, "live_q5c": None}))
        self.assertEqual(c.outcome({**ok, "P2": "FRAGILE"}, [], {**ext, "live_q5c": None}), "not established")


class Descriptive(unittest.TestCase):
    def test_component_classifier_names_the_parts_a_failing_explanation_cites(self):
        cases = {
            "The value is given but its origin and who chose it are not stated": {"value", "origin/chooser/binding"},
            "Retention and projection of the dropped columns is not disclosed": {"retention/projection"},
            "No materiality basis is stated for the null": {"materiality basis"},
            "Search envelope omitted; unexamined areas are not listed": {"unexamined areas"},
            "The report does not name the intended reader or routine questions": {"reader/questions"},
            "Output is acceptable": set(),
        }
        for text, parts in cases.items():
            self.assertEqual(c.classify_explanation(text), parts, text)
        self.assertEqual(set(c.PARTS), {"value", "origin/chooser/binding", "retention/projection", "materiality basis", "unexamined areas", "reader/questions"})

    def test_descriptive_tables_and_component_shares(self):
        rows = []
        for i, (arm, status, text) in enumerate([(c.NEW, "fail", "no origin stated and no reader named"), (c.NEW, "fail", "unexamined areas missing"),
                                                  (c.NEW, "pass", None), (c.AA, "fail", "origin missing"), (c.AA, "unresolved", None)]):
            rows.append({"panel": "main", "arm": arm, "set": i % 2, "episode": f"E{i}", "run": f"r{i}", "item": "decision_provenance", "status": status, "text": text})
        d = c.descriptive(rows)
        self.assertEqual(d["per_item"]["main | decision_provenance"][c.NEW], {"fail": 2, "pass": 1})
        comp = d["component_table_PROXY_keyword_classifier"]["decision_provenance | new"]
        self.assertEqual((comp["failures"], comp["with_explanation"]), (2, 2))
        self.assertEqual((comp["citing"]["origin/chooser/binding"], comp["citing"]["reader/questions"], comp["citing"]["unexamined areas"]), (1, 1, 1))
        self.assertEqual(comp["share"]["origin/chooser/binding"], 0.5)
        self.assertEqual(d["component_table_PROXY_keyword_classifier"]["owed_inquiry | new"]["with_explanation"], 0)


class EndToEnd(unittest.TestCase):
    """`run` on synthetic run directories of two replicate sets that share run names, with dispositions keyed by (command, run)."""

    def make(self, t: Path):
        work = t / "work"
        (work / "runs").mkdir(parents=True)
        spec = {"schema": 1, "arms": [{"name": "p721", "ref": "a", "version": "7.2.1", "label": "cand", "assessed": True},
                                      {"name": "p72aa", "ref": "b", "version": "7.2.0", "label": "b1", "assessed": True}],
                "panels": {"main": {"arms": ["p721", "p72aa"], "replicates": 2}, "routing": {"arms": ["p721", "p72aa"]}}}
        (work / arms_spec.SPEC_NAME).write_text(json.dumps(spec))
        cmds = [{"key": "main-c01", "panel": "main", "set": 0, "conditional": False}, {"key": "main-c02", "panel": "main", "set": 1, "conditional": False},
                {"key": "routing-c01", "panel": "routing", "conditional": False}]
        (work / "commands.json").write_text(json.dumps({"commands": cmds}))
        disp, evidence = {}, {}
        for k, command in enumerate(("main-c01", "main-c02")):
            for e in range(1, 5):
                for arm in ("p721", "p72aa"):
                    name = f"EP-{e:03d}-{arm}-r0"
                    narr = "fail" if (arm == "p72aa" and e <= 3) else "pass"
                    items = {"null_coverage.unowed": ("null_coverage", narr, "binding"), "claim_integrity": ("claim_integrity", "pass", "binding"),
                             "decision_provenance": ("decision_provenance", "unresolved", "advisory")}
                    tb.fake_run(work / "runs" / command, name, items=items, episode=f"EP-{e:03d}")
                    rid = arms_spec.run_id(name, command, k)
                    if not (k == 1 and e == 4):                                # one set-1 assessment is missing: that item stays unresolved
                        disp[f"{rid}::decision_provenance"] = "fail"
                        evidence[f"{rid}::decision_provenance"] = f"origin missing in {command}"
        tb.fake_run(work / "runs" / "routing-c01", "R-001-p721-r0", items={"route_hit": ("route", "pass", "binding")}, episode="R-001")
        (t / "disp.json").write_text(json.dumps(disp))
        (t / "evidence.json").write_text(json.dumps(evidence))
        return work

    def test_run_reads_both_sets_keyed_by_command_and_reports_tables(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            work = self.make(t)
            p = subprocess.run([sys.executable, str(HERE / "compare_721.py"), "run", "--work", str(work), "--dispositions", str(t / "disp.json"),
                                "--evidence", str(t / "evidence.json"), "--out", str(t / "out.json"), "--markdown", str(t / "out.md"),
                                "--external", "live_q5c=true", "--resamples", "200"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            res = json.loads((t / "out.json").read_text())
            self.assertEqual(res["episodes"], 4)
            self.assertFalse(res["frozen_parameters"])                         # --resamples is not the frozen 10,000
            self.assertEqual(res["arms"], {"new": "p721", "aa": "p72aa"})
            w = res["scenarios"]["W"]["primaries"]["P1"]
            self.assertEqual((w["opps_new"], w["opps_aa"], w["fails_new"], w["fails_aa"]), (8, 8, 0, 6))                  # 4 episodes x 2 sets
            by_set = res["descriptive"]["primary_by_replicate_set(fails, opportunities)"]
            self.assertEqual(by_set["P1 | set 0"], {"new": [0, 4], "aa": [3, 4]})
            self.assertEqual(by_set["P1 | set 1"], {"new": [0, 4], "aa": [3, 4]})
            item = res["descriptive"]["per_item"]["main | decision_provenance"]
            self.assertEqual(item["new"], {"fail": 7, "unresolved": 1})                                                   # set 1 / EP-004 has no disposition
            comp = res["descriptive"]["component_table_PROXY_keyword_classifier"]["decision_provenance | new"]
            self.assertEqual((comp["failures"], comp["with_explanation"], comp["citing"]["origin/chooser/binding"]), (7, 7, 7))
            self.assertIn("routing | route_hit", res["descriptive"]["per_item"])
            self.assertEqual(res["run_accounting"]["main|new|set1"], {"runs": 4, "admissible": 4, "death": 0, "inadmissible": 0})
            self.assertEqual(res["external"], {**{k: None for k in c.EXTERNAL}, "live_q5c": True})        # unsupplied conditions stay unknown, never assumed
            self.assertNotEqual(res["outcome"], "go")
            self.assertIn("Outcome:", (t / "out.md").read_text())

    def test_completed_conditional_commands_appear_in_descriptive_tables(self):
        with tempfile.TemporaryDirectory() as t:
            work = self.make(Path(t))
            path = work / "commands.json"
            plan = json.loads(path.read_text())
            plan["commands"].append({"key": "sentinels-add-c01", "panel": "sentinels-add", "conditional": True})
            path.write_text(json.dumps(plan))
            tb.fake_run(work / "runs" / "sentinels-add-c01", "S1-p721-r0",
                        items={"sentinel": ("sentinel", "fail", "binding")}, episode="S1")
            rows, _ = c.load_rows(work, {})
            self.assertEqual(c.descriptive(rows)["per_item"]["sentinels-add | sentinel"][c.NEW], {"fail": 1})
            self.assertEqual(len(c.tally_of(rows)[1]), 4)  # add-on stays outside the primary population

    def test_same_run_name_in_two_sets_gets_its_own_disposition(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            work = self.make(t)
            rows, _ = c.load_rows(work, json.loads((t / "disp.json").read_text()))
            keyed = {(r["set"], r["episode"], r["arm"]): r["status"] for r in rows if r["item"] == "decision_provenance"}
            self.assertEqual(keyed[(0, "EP-004", "new")], "fail")
            self.assertEqual(keyed[(1, "EP-004", "new")], "unresolved")


class OperatingCharacteristics(unittest.TestCase):
    def test_simulation_runs_the_real_decision_function_and_is_ordered(self):
        table = {r["scenario"]: r for r in c.simulate(40, 0.3, 300, 7, ["good: narration cut to 2%, otherwise neutral", "narration not reduced",
                                                                       "good + o1_authoring lost entirely (100%)"], unresolved_scale=0.0)}
        good, none, lost = (table[k]["go_probability"] for k in ("good: narration cut to 2%, otherwise neutral", "narration not reduced",
                                                                  "good + o1_authoring lost entirely (100%)"))
        self.assertGreater(good, 0.6)
        self.assertLess(none, 0.2)
        self.assertEqual(lost, 0.0)
        self.assertEqual(sum(table["narration not reduced"]["outcomes"].values()), 40)

    def test_calibration_hits_the_stated_marginal_rate(self):
        import numpy as np
        sigma = 1.19
        for rate in (0.02, 0.118, 0.5, 0.68):
            a = c.calibrate(rate, sigma)
            z = np.random.default_rng(0).normal(0, sigma, 400000)
            self.assertAlmostEqual(float((1 / (1 + np.exp(-(a + z)))).mean()), rate, places=2)
        self.assertEqual(c.calibrate(0.0, sigma), -float("inf"))


if __name__ == "__main__":
    unittest.main()
