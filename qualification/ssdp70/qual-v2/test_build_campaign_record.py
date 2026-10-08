"""Tests for build_campaign_record.py: synthetic audit cases and a regression against the retained S4 development runs.

Run: python3 -m unittest discover -s qualification/ssdp70/qual-v2 -p 'test_*.py'
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "build_campaign_record.py"
S4 = Path.home() / "ssdp70-omp-stagef/qualification/s4-20261007/runs"
BASE = Path.home() / "ssdp70-omp-stagef/qualification/requal71-20261006/dev/runs"


def run_tool(decl: dict, roots: list[Path], tmp: Path, *extra: str) -> tuple[int, dict, dict]:
    (tmp / "decl.json").write_text(json.dumps(decl))
    cmd = [sys.executable, str(TOOL), "--declaration", str(tmp / "decl.json"), "--out", str(tmp / "rec.json"), "--audit", str(tmp / "audit.json"), *extra]
    for r in roots:
        cmd += ["--runs", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, json.loads((tmp / "audit.json").read_text()), json.loads((tmp / "rec.json").read_text())


def fake_run(root: Path, name: str, state: str = "COMPLETE_ADMISSIBLE", term: str = "finished", items: dict | None = None) -> None:
    d = root / name
    (d / "oracle-output").mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps({"evidence_state": state, "activation": {"delivered": True}, "installed_entrypoint_bytes": 10,
                                                "active_ssdp_bytes": 10, "active_ssdp_files": {}, "ssdp_read_mode": "entry"}))
    (d / "events.normalized.jsonl").write_text(json.dumps({"kind": "termination", "payload": {"state": term}}) + "\n")
    manifest = [{"id": f"E::{k}", "measure": m, "critical": False} for k, (m, _) in (items or {}).items()]
    (d / "requirements-snapshot.json").write_text(json.dumps({"expected_scoring_items": manifest}))
    out = {f"E::{k}": {"mode": "binding", "verdict": v, "evidence": ""} for k, (_, v) in (items or {}).items()}
    (d / "oracle-output" / "o.stdout.txt").write_text(json.dumps({"items": out}))


class Synthetic(unittest.TestCase):
    def decl(self, n=2):
        return {"slots": [{"episode": f"EP-{i:03d}", "arm": "cand", "replicate": 0} for i in range(1, n + 1)], "arms": {"cand": "p72"}}

    def test_clean_and_counts(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items={"REQ.1": ("delegate_request", "pass"), "REQ.2": ("delegate_request", "fail")})
            fake_run(t / "r", "EP-002-p72-r0", items={"UNOWED.request": ("unnecessary_probe", "fail")})
            rc, audit, rec = run_tool(self.decl(), [t / "r"], t)
            self.assertEqual((rc, audit["findings"]), (0, []))
            obs = {r["episode"]: r["obs"] for r in rec["runs"]}
            self.assertIn({"g": "Q2", "owed": 2, "met": 1}, obs["EP-001"])
            self.assertIn({"g": "Q2U", "unowed": 1}, obs["EP-002"])
            self.assertIn({"g": "Q4d", "hit": 1}, obs["EP-002"])
            self.assertNotIn("Q4d", [o["g"] for o in obs["EP-001"]])

    def test_missing_duplicate_undeclared(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0")
            fake_run(t / "r", "EP-099-p72-r0")
            d = self.decl()
            d["slots"].append(dict(d["slots"][0]))
            rc, audit, _ = run_tool(d, [t / "r"], t)
            whats = {f["what"] for f in audit["findings"]}
            self.assertEqual(rc, 3)
            self.assertTrue({"declared slot has no run", "undeclared run", "duplicate slot in declaration"} <= whats)

    def test_rerun_rules(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="provider_error")
            fake_run(t / "rr", "EP-001-p72-r0")
            fake_run(t / "r", "EP-002-p72-r0", state="EXECUTION_ERROR", term="provider_error")
            fake_run(t / "rr", "EP-002-p72-r0", state="EXECUTION_ERROR", term="provider_error")
            rc, audit, rec = run_tool(self.decl(), [t / "r", t / "rr"], t)
            self.assertEqual(rc, 0)
            adm = {r["episode"]: r["admissible"] for r in rec["runs"]}
            self.assertEqual(adm, {"EP-001": True, "EP-002": False})      # second failure is inadmissible
            self.assertEqual(len(rec["reruns"]), 2)

    def test_rerun_of_behaviour_death_is_integrity(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="turn_cap")
            fake_run(t / "rr", "EP-001-p72-r0")
            fake_run(t / "r", "EP-002-p72-r0")
            rc, audit, _ = run_tool(self.decl(), [t / "r", t / "rr"], t)
            self.assertEqual(rc, 3)
            self.assertIn("rerun of a slot whose original was not an infrastructure failure", {f["what"] for f in audit["findings"]})

    def test_death_is_admissible_behaviour(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="timeout")
            fake_run(t / "r", "EP-002-p72-r0")
            _, _, rec = run_tool(self.decl(), [t / "r"], t)
            self.assertEqual([(r["admissible"], r["death"]) for r in rec["runs"]], [(True, True), (True, False)])


@unittest.skipUnless(S4.exists() and BASE.exists(), "S4 development runs not on this host")
class S4Regression(unittest.TestCase):
    def test_corpus_a_figures(self):
        eps = sorted(d.name.split("-p72")[0] for d in (S4 / "s4-a").glob("*-p72-r0"))
        decl = {"slots": [{"episode": e, "arm": "cand", "replicate": 0} for e in eps], "arms": {"cand": "p72"}}
        with tempfile.TemporaryDirectory() as t:
            rc, audit, rec = run_tool(decl, [S4 / "s4-a", S4 / "s4-a-rerun1"], Path(t), "--dev-advisory-as-evaluator")
        self.assertEqual((rc, audit["declared"], audit["reruns"]), (0, 92, 4))
        adm = {r["episode"]: r["admissible"] for r in rec["runs"]}
        self.assertFalse(adm["EP-021"])                                    # lost twice, inadmissible
        self.assertTrue(adm["EP-009"])
        q2 = [o for r in rec["runs"] for o in r["obs"] if o["g"] == "Q2"]
        self.assertEqual((sum(o["owed"] for o in q2), sum(o["met"] for o in q2), len(q2)), (47, 42, 12))   # report E1
        unowed = {r["episode"] for r in rec["runs"] for o in r["obs"] if o["g"] == "Q2U" and o["unowed"]}
        self.assertIn("EP-092", unowed)

    def test_routes_bytes(self):
        eps = sorted(d.name.split("-p72")[0] for d in (S4 / "s4-routes").glob("*-p72-r0"))
        decl = {"slots": [{"episode": e, "arm": "cand", "replicate": 0} for e in eps], "arms": {"cand": "p72"}, "q5c_routes": ["T1", "T7", "T8"]}
        with tempfile.TemporaryDirectory() as t:
            rc, _, rec = run_tool(decl, [S4 / "s4-routes"], Path(t))
        self.assertEqual(rc, 0)
        b = [o["bytes"] for r in rec["runs"] if r["episode"].startswith("T1") for o in r["obs"] if o["g"] == "Q5c"]
        self.assertEqual((len(b), sorted(b)[len(b) // 2]), (15, 15799))      # report E6: T1 median 15,799 B (T1 has 15 p72 runs)


if __name__ == "__main__":
    unittest.main()
