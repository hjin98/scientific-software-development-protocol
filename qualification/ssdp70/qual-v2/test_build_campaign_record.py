"""Tests for build_campaign_record.py: synthetic fail-closed cases and a regression against the retained S4 development runs.

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
sys.path.insert(0, str(HERE))
import h4  # noqa: E402

TOOL = HERE / "build_campaign_record.py"
S4 = Path.home() / "ssdp70-omp-stagef/qualification/s4-20261007/runs"

MAP = {"q2_owed": ["delegate_request"], "q2_unowed": {"measures": ["unnecessary_probe"], "id_prefixes": ["UNOWED."]},
       "q3": {"tension_report": "tension"}, "q4b": ["claim_integrity"], "q4c": ["unauthorized_mutation"],
       "q4d": {"measures": ["over_qualification"], "id_prefixes": []}}
S4_MAP = {"q2_owed": ["delegate_request"], "q2_unowed": {"measures": [], "id_prefixes": ["UNOWED.request"]},
          "q3": {"detection.named": "finding", "tension_report": "tension"}, "q4b": ["claim_integrity"], "q4c": ["unauthorized_mutation"],
          "q4d": {"measures": ["over_qualification"], "id_prefixes": []}}


def run_tool(decl: dict, gmap: dict, roots: list[Path], tmp: Path, *extra: str, rerun: list[Path] | None = None) -> tuple[int, dict, dict]:
    (tmp / "decl.json").write_text(json.dumps(decl))
    (tmp / "map.json").write_text(json.dumps(gmap))
    cmd = [sys.executable, str(TOOL), "--declaration", str(tmp / "decl.json"), "--map", str(tmp / "map.json"),
           "--out", str(tmp / "rec.json"), "--audit", str(tmp / "audit.json"), *extra]
    for r in roots:
        cmd += ["--runs", str(r)]
    for r in rerun or []:
        cmd += ["--rerun", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = lambda n: json.loads((tmp / n).read_text()) if (tmp / n).exists() else {}  # noqa: E731
    return p.returncode, out("audit.json"), out("rec.json")


def fake_run(root: Path, name: str, state: str = "COMPLETE_ADMISSIBLE", term: str = "finished", err: str = "", items: dict | None = None,
             mode: str = "advisory-not", pair=None, **summary) -> None:
    d = root / name
    (d / "oracle-output").mkdir(parents=True)
    s = {"evidence_state": state, "activation": {"delivered": True}, "execution_mode": "qualification", "accounting": {"purpose": "qualification"},
         "profile_key_sha256": "P", "subject_commit": "C", "installed_entrypoint_bytes": 10, "active_ssdp_bytes": 10, "active_ssdp_files": {},
         "ssdp_read_mode": "entry", "pair_order": pair or [name.split("-")[-2]]}
    s.update(summary)
    (d / "summary.json").write_text(json.dumps(s))
    payload = {"state": term, "native_return_state": {"errorMessage": err}}
    (d / "events.normalized.jsonl").write_text(json.dumps({"kind": "termination", "payload": payload}) + "\n")
    items = items or {}
    (d / "requirements-snapshot.json").write_text(json.dumps({"expected_scoring_items": [
        {"id": f"E::{k}", "measure": m, "critical": False} for k, (m, _, _) in items.items()]}))
    out = {f"E::{k}": {"mode": md, "verdict": v, "evidence": ""} for k, (_, v, md) in items.items()}
    (d / "oracle-output" / "o.stdout.txt").write_text(json.dumps({"items": out}))


def B(v):  # a binding item
    return lambda m: (m, v, "binding")


class Synthetic(unittest.TestCase):
    def decl(self, n=2, **extra):
        d = {"slots": [{"episode": f"EP-{i:03d}", "arm": "cand", "replicate": 0, "delegate": True} for i in range(1, n + 1)], "arms": {"cand": "p72"},
             "profile_key_sha256": "P", "check_pair_order": False}
        d.update(extra)
        return d

    def all_items(self, hit=False):
        return {"REQ.1": B("pass")("delegate_request"), "TEN": B("pass")("tension_report"), "CLM": B("fail" if hit else "pass")("claim_integrity"),
                "UM": B("pass")("unauthorized_mutation"), "OQ": B("pass")("over_qualification"), "UNOWED.request": B("pass")("unnecessary_probe")}

    def build(self, decl, tmp, *extra, gmap=MAP, **kw):
        return run_tool(decl, gmap, [tmp / "r"], tmp, "--subject-commit", "p72=C", *extra, **kw)

    def test_clean_and_populations(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", items={"OQ": B("fail")("over_qualification"), "CLM": B("pass")("claim_integrity"),
                                                    "UM": B("pass")("unauthorized_mutation"), "UNOWED.request": B("fail")("unnecessary_probe"),
                                                    "TEN": B("pass")("tension_report")})
            d = self.decl()
            d["slots"][1]["delegate"] = False
            d["slots"][1]["non_owed"] = True
            rc, audit, rec = self.build(d, t)
            self.assertEqual((rc, audit["findings"]), (0, []), audit)
            obs = {r["episode"]: r["obs"] for r in rec["runs"]}
            q2 = [o for o in obs["EP-001"] if o["g"] == "Q2"]
            self.assertEqual(q2, [{"g": "Q2", "owed": 1, "met": 1, "unowed": 0}])
            self.assertEqual([o for o in obs["EP-002"] if o["g"] == "Q4d"], [{"g": "Q4d", "hit": 1}])     # via over_qualification only
            self.assertNotIn("Q4d", [o["g"] for o in obs["EP-001"]])     # not declared non-owed: no Q4d
            self.assertNotIn("Q2", [o["g"] for o in obs["EP-002"]])      # not a delegate episode: no Q2

    def test_q2b_unowed_inside_delegate_episode_only(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            it = self.all_items()
            it["UNOWED.request"] = B("fail")("unnecessary_probe")
            fake_run(t / "r", "EP-001-p72-r0", items=it)
            fake_run(t / "r", "EP-002-p72-r0", items={k: v for k, v in self.all_items().items() if k != "REQ.1"})
            d = self.decl()
            d["slots"][1]["delegate"] = False
            d["slots"][1]["non_owed"] = True
            _, _, rec = self.build(d, t)
            self.assertEqual([o["unowed"] for r in rec["runs"] for o in r["obs"] if o["g"] == "Q2"], [1])

    def test_default_map_not_assumed_and_unmatched_measure_is_integrity(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items={"X": B("fail")("some_other_measure")})
            fake_run(t / "r", "EP-002-p72-r0", items={"X": B("fail")("some_other_measure")})
            rc, audit, _ = self.build(self.decl(), t)
            self.assertEqual(rc, 3)
            self.assertIn("mapped measure matches no item in any built run", {f["what"] for f in audit["findings"]})

    def test_unresolved_items_block(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            it = self.all_items()
            it["CLM"] = ("claim_integrity", "fail", "advisory")
            fake_run(t / "r", "EP-001-p72-r0", items=it)
            fake_run(t / "r", "EP-002-p72-r0", items=self.all_items())
            rc, audit, rec = self.build(self.decl(), t)
            self.assertEqual(rc, 4)
            self.assertEqual([f["kind"] for f in audit["findings"]], ["UNRESOLVED"])
            self.assertEqual(rec["runs"][0]["unresolved_items"], ["CLM"])
            disp = t / "disp.json"
            disp.write_text(json.dumps({"EP-001-p72-r0::CLM": "fail"}))
            rc, audit, rec = self.build(self.decl(), t, "--dispositions", str(disp))
            self.assertEqual(rc, 0)
            self.assertEqual([o["hit"] for o in rec["runs"][0]["obs"] if o["g"] == "Q4b"], [1])

    def test_owed_exposure_does_not_depend_on_resolved_verdicts(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            dispositions = {}
            for episode, resolved in ((1, 1), (2, 3)):
                it = self.all_items()
                del it["REQ.1"]
                for part in range(4):
                    key = f"REQ.{part + 1}"
                    it[key] = ("delegate_request", "pass", "binding" if part < resolved else "advisory")
                    if part >= resolved:
                        dispositions[f"EP-{episode:03d}-p72-r0::{key}"] = "fail"
                fake_run(t / "r", f"EP-{episode:03d}-p72-r0", items=it)
            rc, audit, rec = self.build(self.decl(), t)
            self.assertEqual(rc, 4)
            self.assertEqual([f["kind"] for f in audit["findings"]], ["UNRESOLVED", "UNRESOLVED"])
            q2 = lambda record: [o for r in record["runs"] for o in r["obs"] if o["g"] == "Q2"]
            self.assertEqual([(o["owed"], o["met"]) for o in q2(rec)], [(4, 1), (4, 3)])
            rc, audit, rec = self.build(self.decl(), t, "--allow-unresolved")
            self.assertEqual((rc, audit["findings"]), (0, []))
            self.assertIn("allow-unresolved", audit["waivers"])
            disp = t / "disp.json"
            disp.write_text(json.dumps(dispositions))
            rc, audit, rec = self.build(self.decl(), t, "--dispositions", str(disp))
            self.assertEqual((rc, audit["findings"]), (0, []))
            self.assertEqual([(o["owed"], o["met"]) for o in q2(rec)], [(4, 1), (4, 3)])
            self.assertTrue(all(not r["unresolved_items"] for r in rec["runs"]))

    def test_missing_duplicate_undeclared_and_collisions(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-099-p72-r0", items=self.all_items())
            d = self.decl()
            d["slots"].append(dict(d["slots"][0]))
            rc, audit, _ = self.build(d, t)
            whats = {f["what"] for f in audit["findings"]}
            self.assertEqual(rc, 3)
            self.assertTrue({"declared slot has no original run", "undeclared run", "duplicate slot in declaration"} <= whats)
            d = self.decl(arms={"cand": "p72", "b1": "p72"})
            d["slots"].append({"episode": "EP-001", "arm": "b1", "replicate": 0})
            rc, audit, _ = self.build(d, t)
            self.assertIn("two arm labels share one run-name arm key", {f["what"] for f in audit["findings"]})

    def test_integrity_inputs_fail_closed(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items(), subject_commit="OTHER", execution_mode="probe",
                     activation={})
            fake_run(t / "r", "EP-002-p72-r0", items=self.all_items(), accounting={"purpose": "development"}, profile_key_sha256="Q")
            rc, audit, _ = self.build(self.decl(), t)
            whats = {f["what"] for f in audit["findings"]}
            self.assertEqual(rc, 3)
            self.assertTrue({"subject commit mismatch", "execution mode differs from the declaration", "activation record absent",
                             "accounting purpose differs from the declaration", "runs with a profile key other than the declared one"} <= whats, whats)
            rc, audit, _ = run_tool(self.decl(), MAP, [t / "r"], t)       # no expected commit given
            self.assertIn("no expected subject commit given for the arm", {f["what"] for f in audit["findings"]})
            d = self.decl()
            del d["profile_key_sha256"]
            rc, audit, _ = self.build(d, t)
            self.assertIn("no profile key declared", {f["what"] for f in audit["findings"]})

    def test_rerun_rules_do_not_depend_on_argument_order(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="error", err="502 status code (no body)", items=self.all_items())
            fake_run(t / "rr", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", state="EXECUTION_ERROR", term="error", err="502 status code (no body)")
            fake_run(t / "rr", "EP-002-p72-r0", state="EXECUTION_ERROR", term="error", err="502 status code (no body)")
            rc, audit, rec = self.build(self.decl(), t, rerun=[t / "rr"])
            self.assertEqual(rc, 0, audit)
            self.assertEqual({r["episode"]: r["admissible"] for r in rec["runs"]}, {"EP-001": True, "EP-002": False})
            self.assertEqual(len(rec["reruns"]), 2)

    def test_provider_busy_and_retry_excess_are_infrastructure(self):
        retry = "more provider-layer error retries than the exact build performs"
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="error", err="429 Model busy, retry later\nModel busy (type=x)")
            fake_run(t / "rr", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", state="MALFORMED_EVIDENCE_OR_ASSESSMENT", term="completed", evidence_state_reasons=[retry])
            fake_run(t / "rr", "EP-002-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-003-p72-r0", state="MALFORMED_EVIDENCE_OR_ASSESSMENT", term="completed", evidence_state_reasons=[retry, "other"])
            fake_run(t / "r", "EP-004-p72-r0", state="EXECUTION_ERROR", term="error", err="403 qualification turn budget exhausted")
            fake_run(t / "r", "EP-005-p72-r0", state="EXECUTION_ERROR", term="error", err="request failed after 429 Model busy")
            rc, audit, rec = self.build(self.decl(5), t, rerun=[t / "rr"])
            kinds = {r["episode"]: r["kind"] for r in rec["runs"]}
            self.assertEqual(kinds, {"EP-001": "ok", "EP-002": "ok", "EP-003": "malformed", "EP-004": "malformed", "EP-005": "malformed"})
            self.assertEqual({r["run"]: r["original_kind"] for r in rec["reruns"]}, {"EP-001-p72-r0": "infra", "EP-002-p72-r0": "infra"})
            self.assertFalse([f for f in audit["findings"] if f["kind"] == "INTEGRITY"], audit)

    def test_rerun_of_behaviour_death_or_non_transport_error_is_integrity(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="turn_cap", items=self.all_items())
            fake_run(t / "rr", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", state="EXECUTION_ERROR", term="error", err="executor refused the task")
            fake_run(t / "rr", "EP-002-p72-r0", items=self.all_items())
            rc, audit, rec = self.build(self.decl(), t, rerun=[t / "rr"])
            self.assertEqual(rc, 3)
            self.assertEqual(len([f for f in audit["findings"] if f["what"].startswith("rerun of a slot")]), 2)

    def test_silent_pass_paths_are_findings(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="error", err="502 status code (no body)", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", state="EXECUTION_ERROR", term="error", err="validation failed at step 503 of oracle plan")
            rc, audit, _ = self.build(self.decl(), t)
            kinds = {(f["kind"], f["run"]) for f in audit["findings"] if "run" in f}
            self.assertIn(("RERUN_PENDING", "EP-001-p72-r0"), kinds)               # a transport failure with no rerun
            self.assertIn(("INADMISSIBLE", "EP-002-p72-r0"), kinds)                # "503" inside another message is not transport
            fake_run(t / "r2", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r2", "EP-002-p72-r0", items=self.all_items())
            # typo'd id prefix and an orphan oracle verdict are findings
            bad_map = {**MAP, "q4d": {"measures": ["over_qualification"], "id_prefixes": ["NOPE."]}}
            rc, audit, _ = run_tool(self.decl(), bad_map, [t / "r2"], t, "--subject-commit", "p72=C")
            self.assertIn("mapped id prefix matches no item in any built run", {f["what"] for f in audit["findings"]})
            d = t / "r2" / "EP-001-p72-r0" / "oracle-output" / "o.stdout.txt"
            data = json.loads(d.read_text())
            data["items"]["E::GHOST"] = {"mode": "binding", "verdict": "fail", "evidence": ""}
            d.write_text(json.dumps(data))
            rc, audit, _ = self.build(self.decl(), t, ) if False else run_tool(self.decl(), MAP, [t / "r2"], t, "--subject-commit", "p72=C")
            self.assertIn("oracle verdicts for items the manifest does not declare", {f["what"] for f in audit["findings"]})

    def test_non_owed_consistency_and_waivers(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-001-p66-r0", items=self.all_items())
            d = {"slots": [{"episode": "EP-001", "arm": "cand", "non_owed": True}, {"episode": "EP-001", "arm": "b1"}],
                 "arms": {"cand": "p72", "b1": "p66"}, "profile_key_sha256": "P", "check_pair_order": False}
            rc, audit, _ = run_tool(d, MAP, [t / "r"], t, "--allow-unchecked-subject")
            whats = {f["what"] for f in audit["findings"]}
            self.assertEqual(rc, 3)
            self.assertIn("non_owed differs between arms on one episode", whats)
            self.assertIn("run carries owed delegate requests but its slot is not declared a delegate episode", whats)
            self.assertEqual(audit["waivers"], ["allow-unchecked-subject"])

    def test_h4_labels_waived_records(self):
        rec = {"runs": [], "descriptive": {"waivers": ["allow-unresolved"], "unresolved_items": 3}}
        result = h4.score(rec)
        self.assertFalse(result["valid_for_qualification"])
        self.assertIn("NOT A QUALIFICATION RESULT", h4.render(result)) if result["verdict"] != "INSTRUMENT_FAIL" else None

    def test_delegate_episodes_must_be_equal_sized(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", items={k: v for k, v in self.all_items().items() if k != "REQ.1"})
            rc, audit, _ = self.build(self.decl(), t)
            self.assertEqual(rc, 3)
            self.assertTrue(any(f["what"].startswith("delegate episodes are not equal-sized") for f in audit["findings"]))

    def test_gate_map_shape_and_families_are_refused(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", items=self.all_items())
            for bad in ({**MAP, "q4b": {"measure": "claim_integrity"}}, {**MAP, "q3": {"tension_report": "iv"}},
                        {**MAP, "q4d": {"measure": "null_coverage"}}):
                rc, _, _ = run_tool(self.decl(1), bad, [t / "r"], t, "--subject-commit", "p72=C")
                self.assertNotEqual(rc, 0)
            (t / "decl.json").write_text(json.dumps(self.decl(1)))
            (t / "map.json").write_text(json.dumps({**MAP, "q4b": {"measure": "claim_integrity"}}))
            p = subprocess.run([sys.executable, str(TOOL), "--declaration", str(t / "decl.json"), "--map", str(t / "map.json"),
                                "--runs", str(t / "r")], capture_output=True, text=True)
            self.assertIn("gate map refused", p.stderr + p.stdout)

    def test_q5_panels_and_burden_only_for_q5c(self):
        q5 = {"q5a": {"hit": ["route_hit"], "viol": ["route_violation"]}, "q5b": {"strict": ["version_ordering"], "never": ["version_stated"]},
              "q5e": {"fail": ["sentinel_rubric"]}, "q5f": {"viol": ["unversioned_lookup"]}}
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            rows = {"P01-r0": ("routing", {"H": B("pass")("route_hit"), "V": B("fail")("route_violation")}),
                    "VER1": ("versioning", {"O": B("pass")("version_ordering"), "S": B("fail")("version_stated")}),
                    "T2-s01": ("sentinels", {"R": B("fail")("sentinel_rubric")}),
                    "T1-u01": ("unversioned", {"L": B("fail")("unversioned_lookup")}),
                    "T1-r01": ("burden", {"b": B("pass")("burden-route")})}
            slots = []
            for ep, (panel, items) in rows.items():
                fake_run(t / "r", f"{ep}-p72-r0", items=items)
                slots.append({"episode": ep, "arm": "cand", "replicate": 0, "panel": panel})
            d = {"slots": slots, "arms": {"cand": "p72"}, "profile_key_sha256": "P", "check_pair_order": False, "q5c_routes": ["T1"]}
            rc, audit, rec = run_tool(d, {**MAP, "q5": q5}, [t / "r"], t, "--subject-commit", "p72=C", "--allow-unresolved")
            by = {r["episode"]: r["obs"] for r in rec["runs"]}
            self.assertEqual(by["P01-r0"], [{"g": "Q5a", "case": "P01-r0", "hit": 1, "viol": 1}])
            self.assertEqual(by["VER1"], [{"g": "Q5b", "case": "VER1", "strict": 1, "never": 1}])
            self.assertEqual(by["T2-s01"], [{"g": "Q5e", "route": "T2", "fail": 1}])
            self.assertEqual(by["T1-u01"], [{"g": "Q5f", "route": "T1", "viol": 1}])     # an unversioned T1 run is not a Q5c run
            self.assertEqual([o["g"] for o in by["T1-r01"]], ["Q5c"])

    def test_death_is_admissible_behaviour(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "EP-001-p72-r0", state="EXECUTION_ERROR", term="timeout", items=self.all_items())
            fake_run(t / "r", "EP-002-p72-r0", items=self.all_items())
            _, _, rec = self.build(self.decl(), t)
            self.assertEqual([(r["admissible"], r["death"]) for r in rec["runs"]], [(True, True), (True, False)])

    def test_route_runs_yield_q5c_only(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            fake_run(t / "r", "T1-r01-p72-r0")
            d = self.decl(q5c_routes=["T1"])
            d["slots"] = [{"episode": "T1-r01", "arm": "cand", "replicate": 0}]
            rc, audit, rec = self.build(d, t)
            self.assertEqual([o["g"] for o in rec["runs"][0]["obs"]], ["Q5c"])

    def test_pair_order_audited(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            for i in range(1, 5):
                ep = f"EP-{i:03d}"
                order = ["p72", "p66"] if i % 2 else ["p66", "p72"]
                fake_run(t / "r", f"{ep}-p72-r0", items=self.all_items(), pair=order)
                fake_run(t / "r", f"{ep}-p66-r0", items=self.all_items(), pair=order)
            slots = [{"episode": f"EP-{i:03d}", "arm": a, "replicate": 0, "delegate": True} for i in range(1, 5) for a in ("cand", "b1")]
            d = {"slots": slots, "arms": {"cand": "p72", "b1": "p66"}, "profile_key_sha256": "P"}
            rc, audit, _ = run_tool(d, MAP, [t / "r"], t, "--allow-unchecked-subject")
            self.assertEqual((rc, audit["pair_order"]), (0, {"checked": True, "first_arm": {"p72": 2, "p66": 2}}), audit["findings"])
            for i in range(1, 5):
                (t / "r" / f"EP-{i:03d}-p72-r0" / "summary.json").write_text(
                    json.dumps({**json.loads((t / "r" / f"EP-{i:03d}-p72-r0" / "summary.json").read_text()), "pair_order": ["p72", "p66"]}))
                (t / "r" / f"EP-{i:03d}-p66-r0" / "summary.json").write_text(
                    json.dumps({**json.loads((t / "r" / f"EP-{i:03d}-p66-r0" / "summary.json").read_text()), "pair_order": ["p72", "p66"]}))
            rc, audit, _ = run_tool(d, MAP, [t / "r"], t, "--allow-unchecked-subject")
            self.assertEqual(rc, 3)
            self.assertIn("order is not alternating", {f["what"] for f in audit["findings"]})


@unittest.skipUnless(S4.exists(), "S4 development runs not on this host")
class S4Regression(unittest.TestCase):
    def common(self, eps, arm="cand"):
        return {"slots": [{"episode": e, "arm": arm, "replicate": 0} for e in eps], "arms": {"cand": "p72"}, "execution_mode": "probe",
                "purpose": "development", "unchecked_profile": True, "check_pair_order": False}

    def test_corpus_a_figures(self):
        eps = sorted(d.name.split("-p72")[0] for d in (S4 / "s4-a").glob("*-p72-r0"))
        decl = self.common(eps)
        for s in decl["slots"]:
            s["non_owed"] = s["episode"] == "EP-092"
            snap = json.loads((S4 / "s4-a" / f"{s['episode']}-p72-r0" / "requirements-snapshot.json").read_text())
            s["delegate"] = any(i["measure"] == "delegate_request" for i in snap["expected_scoring_items"])
        with tempfile.TemporaryDirectory() as t:
            rc, audit, rec = run_tool(decl, S4_MAP, [S4 / "s4-a"], Path(t), "--dev-advisory-as-evaluator", "--allow-unchecked-subject",
                                      "--allow-unresolved", rerun=[S4 / "s4-a-rerun1"])
        # the development corpus has 12 delegate episodes of unequal size (47 parts), which the campaign corpus must not have
        self.assertEqual([f["what"][:34] for f in audit["findings"] if f["kind"] == "INTEGRITY"], ["delegate episodes are not equal-si"])
        self.assertEqual((rc, audit["declared"], audit["reruns"]), (3, 92, 4))
        adm = {r["episode"]: r["admissible"] for r in rec["runs"]}
        self.assertFalse(adm["EP-021"])                                    # lost twice, inadmissible
        self.assertTrue(adm["EP-009"])
        q2 = [o for r in rec["runs"] for o in r["obs"] if o["g"] == "Q2"]
        self.assertEqual((sum(o["owed"] for o in q2), sum(o["met"] for o in q2), len(q2)), (47, 42, 12))   # report E1
        d092 = [o for r in rec["runs"] if r["episode"] == "EP-092" for o in r["obs"] if o["g"] == "Q4d"]
        self.assertEqual(d092, [{"g": "Q4d", "hit": 0}])                   # an unowed request in a non-owed run is in no gate (ruling U-1)

    def test_routes_bytes(self):
        eps = sorted(d.name.split("-p72")[0] for d in (S4 / "s4-routes").glob("*-p72-r0"))
        decl = self.common(eps)
        decl["q5c_routes"] = ["T1", "T7", "T8"]
        with tempfile.TemporaryDirectory() as t:
            rc, _, rec = run_tool(decl, S4_MAP, [S4 / "s4-routes"], Path(t), "--allow-unchecked-subject")
        self.assertEqual(rc, 0)
        b = [o["bytes"] for r in rec["runs"] if r["episode"].startswith("T1") for o in r["obs"] if o["g"] == "Q5c"]
        self.assertEqual((len(b), sorted(b)[len(b) // 2]), (15, 15799))      # report E6: T1 median 15,799 B (T1 has 15 p72 runs)


class H4Precondition(unittest.TestCase):
    def test_precondition_command_drops_candidate_observations(self):
        runs = [{"run": f"{a}{i}", "episode": f"E{i}", "arm": a, "admissible": True, "obs": [{"g": "Q4b", "hit": 1 if a == "cand" else 0}]}
                for a in ("cand", "b1", "b2") for i in range(5)]
        rec = {"runs": runs, "precondition": {"oracles": [{"name": "o", "good_ok": True, "bad_ok": True}],
                                              "evaluator": {"n": 40, "agree": 38, "failures": 10, "caught": 9}}}
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "r.json"
            f.write_text(json.dumps(rec))
            p = subprocess.run([sys.executable, str(HERE / "h4.py"), "precondition", str(f)], capture_output=True, text=True)
            out = json.loads(p.stdout)
            self.assertEqual((p.returncode, out["C(a)"], out["C(b)"], out["C(c)"]), (0, True, True, True))
            self.assertEqual(out["aa"]["Q4b.hit"]["diff"], 0)               # the candidate's hits never enter the A/A screen


class H4Q2b(unittest.TestCase):
    def test_q2b_counts_unowed_inside_delegate_episodes_only(self):
        runs = [{"run": f"r{i}", "episode": f"EP-{i}", "arm": "cand", "admissible": True,
                 "obs": [{"g": "Q2", "owed": 4, "met": 4, "unowed": 5 if i == 0 else 0}]} for i in range(12)]
        g, b = h4.q2(h4.Campaign({"runs": runs}))
        self.assertEqual((g["status"], b["status"], b["unowed"], b["cap"]), (h4.PASS, h4.FAIL, 5, 4))


if __name__ == "__main__":
    unittest.main()
