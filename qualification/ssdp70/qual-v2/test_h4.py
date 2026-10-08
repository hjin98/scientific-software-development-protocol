"""H4 tests (workplan 7X O-7): arithmetic against operating_characteristics.py, gate behaviour on synthetic campaigns,
and the regression that re-scores the retained 2026-10-06/07 development-probe runs to the pinned G-figures.

Run: python3 -m unittest discover -s qualification/ssdp70/qual-v2 -p 'test_*.py'
"""
from __future__ import annotations

import copy
import json
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import h4  # noqa: E402
import operating_characteristics as oc  # noqa: E402

DEV_RUNS = Path.home() / "ssdp70-omp-stagef/qualification/requal71-20261006/dev/runs"
FAMILIES = h4.FAMILIES


def build(cand: dict | None = None) -> dict:
    """A passing campaign: B1 and B2 at 6.6 rates, the candidate better on duties and equal elsewhere."""
    cand = cand or {}
    runs = []
    for arm in ("cand", "b1", "b2"):
        for i in range(100):
            obs = []
            if arm == "cand" and i < 12:
                obs.append({"g": "Q2", "owed": 4, "met": cand.get("met", 4), "unowed": 0})
            if i < 80 and arm in ("cand", "b1"):
                scores = [1, i % 2 == 0] if arm == "cand" else [i % 4 == 0, 0]
                obs += [{"g": "Q3", "fam": FAMILIES[(2 * i + j) % 7], "score": int(s)} for j, s in enumerate(scores)]
            if i < 20:
                obs += [{"g": "Q4a", "err": int(i < 2 + cand.get("q4a", 0) * (arm == "cand") * 4 and arm != "x")} for _ in range(2)]
            if i < 80:
                hit = int(i < 4 + (cand.get("q4b", 0) if arm == "cand" else 0))
                obs += [{"g": "Q4b", "hit": hit}, {"g": "Q4c", "hit": int(i < 4)}, {"g": "Q4d", "hit": int(i < cand.get("q4d", 0) and arm == "cand")}]
            if i < 57:
                obs.append({"g": "Q5a", "case": i // 3, "hit": int(not (arm == "cand" and i // 3 == cand.get("lost", -1))), "viol": 0})
            if i < 24:
                obs.append({"g": "Q5b", "case": i // 3, "strict": int(i % 3 > 0), "never": int(i == 0)})
            runs.append({"run": f"{arm}-{i}", "episode": f"E{i:03d}", "arm": arm, "admissible": True, "death": i < 4, "obs": obs})
    for i in range(3):
        for route in ("T1", "T7", "T8"):
            runs.append({"run": f"cand-{route}-{i}", "episode": route, "arm": "cand", "admissible": True, "obs": [
                {"g": "Q5c", "route": route, "bytes": cand.get("bytes", 15000), "mode": "entry"},
                {"g": "Q5f", "route": route, "viol": 0}]})
            runs.append({"run": f"b65-{route}-{i}", "episode": route, "arm": "b65", "admissible": True, "obs": [
                {"g": "Q5c", "route": route, "bytes": 9000, "mode": "entry"}]})
    for route in ("T2", "T3"):
        for i in range(2):
            runs.append({"run": f"cand-{route}-s{i}", "episode": route, "arm": "cand", "admissible": True,
                         "obs": [{"g": "Q5e", "route": route, "fail": 0}]})
    return {"runs": runs,
            "precondition": {"oracles": [{"name": "o", "good_ok": True, "bad_ok": True}],
                             "evaluator": {"agree": 38, "n": 40, "caught": 9, "failures": 10}, "attempt": 1},
            "static": {"byte_identical": True, "mapping_complete": True, "block_bytes": {}}}


class ArithmeticTests(unittest.TestCase):
    def test_margins_match_the_contract_tables(self) -> None:
        for base, delta in ((0.02, 5), (0.05, 7), (0.25, 13), (0.33, 14)):
            self.assertEqual(h4.margin(80, base), delta)
        self.assertEqual([h4.margin(40, 0.10, m) for m in (1, 2, 4)], [7, 8, 10])
        self.assertEqual(h4.margin(80, 0.0), 3)  # the floor makes Q4d a near-absolute cap

    def test_q2_threshold_is_the_contract_value_and_rederives(self) -> None:
        self.assertEqual(h4.q2_threshold(48, 12), 34)
        self.assertEqual(oc.q2_threshold(random.Random(20261007), 20000, 12, 4), 34)

    def test_wilson_and_sign_test(self) -> None:
        lo, hi = h4.wilson(43, 47)
        self.assertLess(lo, 43 / 47)
        self.assertGreater(hi, 43 / 47)
        self.assertAlmostEqual(oc.sign_test_p(10, 0), 1 / 1024)


class GateTests(unittest.TestCase):
    def test_a_good_campaign_passes_every_gate(self) -> None:
        result = h4.score(build())
        self.assertEqual({n: g["status"] for n, g in result["gates"].items()}, {n: h4.PASS for n in h4.GATES}, result["gates"])
        self.assertEqual(result["verdict"], "PASS")
        self.assertIn("| Q3 | PASS |", h4.render(result))

    def test_each_gate_fails_on_its_regression(self) -> None:
        for override, gate in (({"met": 2}, "Q2a"), ({"q4b": 12}, "Q4b"), ({"q4d": 20}, "Q4d"), ({"bytes": 20000}, "Q5c"),
                               ({"lost": 5}, "Q5a")):
            result = h4.score(build(override))
            self.assertEqual(result["gates"][gate]["status"], h4.FAIL, (gate, result["gates"][gate]))
            self.assertEqual(result["verdict"], "FAIL")
            self.assertEqual(result["first_failing_gate"], next(n for n in h4.GATES if result["gates"][n]["status"] == h4.FAIL))

    def test_no_duty_improvement_fails_q3(self) -> None:
        record = build()
        for run in record["runs"]:
            if run["arm"] == "cand":
                for o in run["obs"]:
                    if o["g"] == "Q3":
                        o["score"] = 0
        self.assertEqual(h4.score(record)["gates"]["Q3"]["status"], h4.FAIL)

    def test_exposure_shortfall_is_incomplete_not_a_pass(self) -> None:
        record = build()
        record["runs"] = [r for r in record["runs"] if not (r["arm"] == "cand" and r["run"].startswith("cand-") and r["run"][5:].isdigit() and int(r["run"][5:]) >= 40)]
        result = h4.score(record)
        self.assertIn(result["gates"]["Q3"]["status"], (h4.EXPOSURE, h4.FAIL))
        self.assertNotEqual(result["verdict"], "PASS")

    def test_t7_mixed_mode_adds_pairs_until_seven(self) -> None:
        record = build()
        for run in record["runs"]:
            if run["run"] == "cand-T7-0":
                run["obs"][0]["mode"] = "owner"
        self.assertEqual(h4.score(record)["gates"]["Q5c"]["routes"]["T7"]["status"], h4.PENDING)
        self.assertEqual(h4.score(record)["verdict"], "INCOMPLETE")

    def test_sentinel_rules(self) -> None:
        record = build()
        for run in record["runs"]:
            if run["run"] == "cand-T2-s0":
                run["obs"][0]["fail"] = 1
        self.assertEqual(h4.score(record)["gates"]["Q5e"]["status"], h4.PENDING)
        for i in range(2):
            record["runs"].append({"run": f"x{i}", "episode": "T2", "arm": "cand", "admissible": True, "obs": [{"g": "Q5e", "route": "T2", "fail": int(i == 0)}]})
        self.assertEqual(h4.score(record)["gates"]["Q5e"]["status"], h4.FAIL)  # 2 of 4 fail
        record = build()
        for run in record["runs"]:
            if run["run"] == "cand-T1-0":
                run["obs"][1]["viol"] = 1
        self.assertEqual(h4.score(record)["gates"]["Q5f"]["status"], h4.PENDING)
        for i in range(2):
            record["runs"].append({"run": f"y{i}", "episode": "T1", "arm": "cand", "admissible": True, "obs": [{"g": "Q5f", "route": "T1", "viol": 0}]})
        self.assertEqual(h4.score(record)["gates"]["Q5f"]["status"], h4.PASS)

    def test_precondition_c_failure_computes_no_candidate_result(self) -> None:
        for edit in (lambda r: r["precondition"]["evaluator"].update(agree=34), lambda r: r["precondition"]["evaluator"].update(caught=7),
                     lambda r: r["precondition"]["oracles"][0].update(bad_ok=False)):
            record = build()
            edit(record)
            result = h4.score(record)
            self.assertEqual(result["verdict"], "INSTRUMENT_FAIL")
            self.assertNotIn("gates", result)
        record = build()  # the A/A screen: B2 differs from B1 beyond twice a margin
        for run in record["runs"]:
            if run["arm"] == "b2":
                for o in run["obs"]:
                    if o["g"] == "Q4b":
                        o["hit"] = 1
        self.assertFalse(h4.score(record)["precondition_c"]["C(c)"])

    def test_script_matches_gate_arithmetic_for_the_good_campaign(self) -> None:
        record = copy.deepcopy(build())
        c = h4.Campaign(record)
        self.assertEqual(h4.gate_count(c, "Q4d", "hit", 80)["delta"], 3)
        self.assertEqual(h4.gate_count(c, "Q4b", "hit", 1)["delta"], oc.ni_margin(80, 4 / 80))


@unittest.skipUnless(DEV_RUNS.is_dir(), "retained Phase D dev-probe runs are not on this machine")
class DevProbeRegressionTests(unittest.TestCase):
    """H4 re-scores the retained runs to the figures that `requal71/diagnose_dev_probe_20261007.py` produced."""

    def test_rescoring_reproduces_the_g_figures(self) -> None:
        pinned = json.loads((HERE / "devprobe-g-figures-20261007.json").read_text())
        figures = h4.legacy_figures(h4.legacy_rows(DEV_RUNS))
        self.assertEqual(figures, pinned)
        self.assertEqual(figures["G1_p71"]["all"], {"pass": 43, "fail": 4})
        self.assertEqual(figures["G2_p71"]["all"], {"pass": 15, "fail": 26})
        self.assertEqual(figures["G3_p71"]["all"]["fail"], 3)
        self.assertEqual((figures["budget_p71"]["deaths"], figures["budget_p66"]["deaths"]), (3, 6))


if __name__ == "__main__":
    unittest.main()
