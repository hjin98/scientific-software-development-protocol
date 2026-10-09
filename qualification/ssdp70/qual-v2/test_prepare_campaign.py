"""Tests for prepare_campaign.py and campaign_run.py on a synthetic plan built from the retained S4 route corpus (no provider, no run).

Run: python3 -m unittest discover -s qualification/ssdp70/qual-v2 -p 'test_*.py'
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CAMPAIGN = Path.home() / "ssdp70-omp-stagef/qualification/campaign-72-20261008"
S4 = Path.home() / "ssdp70-omp-stagef/qualification/s4-20261007"


def run(*args, **kw):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, **kw)


@unittest.skipUnless((CAMPAIGN / "campaign-identity.json").exists() and (S4 / "routes").exists(), "campaign directory not on this host")
class Plan(unittest.TestCase):
    def setUp(self):
        self.t = Path(tempfile.mkdtemp())
        self.work = self.t / "work"
        self.work.mkdir()
        shutil.copytree(CAMPAIGN / "keys", self.work / "keys")
        (self.work / "arms").symlink_to(CAMPAIGN / "arms")
        manifest = yaml.safe_load((S4 / "routes/corpus/manifest.yaml").read_text())
        eps = manifest["episodes"]
        for e in eps:
            e["panel"] = "burden"
        for e in eps:
            if e["id"] in ("T1-r01", "T1-r02", "T1-r03"):
                e["panel"] = "main"
            if e["id"] == "T7-r05":
                e["panel"] = "burden-add"
            if e["id"] == "T8-r01":
                e["panel"] = "sentinels"
        self.corpus = self.t / "corpus"
        shutil.copytree(S4 / "routes/corpus", self.corpus)
        (self.corpus / "manifest.yaml").write_text(yaml.safe_dump(manifest))
        self.flags = self.t / "flags.json"
        self.flags.write_text(json.dumps({"T1-r01": {"delegate": True, "non_owed": False, "scored": True},
                                          "T1-r02": {"delegate": False, "non_owed": True, "scored": True},
                                          "T1-r03": {"delegate": False, "non_owed": True, "scored": True}}))
        self.args = ["--work", self.work, "--corpus", self.corpus, "--requirements", S4 / "routes/requirements",
                     "--oracles", S4 / "routes/oracles", "--slot-flags", self.flags]

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def test_check_plan_and_conditional_hold(self):
        p = run(HERE / "prepare_campaign.py", "check-corpus", *self.args)
        self.assertEqual(p.returncode, 0, p.stdout)
        p = run(HERE / "prepare_campaign.py", "plan", *self.args)
        self.assertEqual(p.returncode, 0, p.stderr)
        plan = json.loads((self.work / "commands.json").read_text())["commands"]
        arms = {c["panel"]: c["arms"] for c in plan}
        self.assertEqual(arms["main"], ["p72", "p66", "p66b"])
        self.assertEqual(arms["burden"], ["p72", "p65"])
        self.assertEqual(arms["sentinels"], ["p72"])
        self.assertTrue(next(c for c in plan if c["panel"] == "burden-add")["conditional"])
        self.assertTrue(all(int(c["argv"][c["argv"].index("--parallel") + 1]) <= 8 for c in plan))
        decl = json.loads((self.work / "declaration.json").read_text())
        self.assertEqual(len(decl["conditional_slots"]), 2)
        self.assertEqual(decl["arms"], {"cand": "p72", "b1": "p66", "b2": "p66b", "b65": "p65"})
        p = run(HERE / "prepare_campaign.py", "check-plan", "--work", self.work)
        self.assertEqual(p.returncode, 0, p.stdout)
        # a plan cannot be overwritten
        self.assertNotEqual(run(HERE / "prepare_campaign.py", "plan", *self.args).returncode, 0)

    def test_check_corpus_flags_missing_slot_flags(self):
        self.flags.write_text(json.dumps({"T1-r01": {"delegate": True}}))
        p = run(HERE / "prepare_campaign.py", "check-corpus", *self.args)
        self.assertEqual(p.returncode, 2)
        self.assertIn("slot flags", p.stdout)

    def test_runner_refuses_without_credential_and_conditional_without_authorization(self):
        run(HERE / "prepare_campaign.py", "plan", *self.args)
        env = {"PATH": "/usr/bin:/bin"}
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "start"], capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("CREDENTIAL", p.stderr)
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "start", "1"], capture_output=True, text=True,
                           env={**env, "SSDP70_OMP_PROVIDER_CREDENTIAL": "x"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("READY does not say", p.stderr)
        self.assertFalse((self.work / "launch").exists() and any((self.work / "launch").iterdir()))
        key = next(c["key"] for c in json.loads((self.work / "commands.json").read_text())["commands"] if c["conditional"])
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "run-conditional", key], capture_output=True, text=True,
                           env={**env, "SSDP70_OMP_PROVIDER_CREDENTIAL": "x"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("not authorized", p.stderr)

    def test_stages_follow_gate_order_and_stage2_needs_authorization(self):
        run(HERE / "prepare_campaign.py", "plan", *self.args)
        plan = json.loads((self.work / "commands.json").read_text())["commands"]
        self.assertEqual({c["panel"]: c["stage"] for c in plan}, {"main": 1, "burden": 2, "burden-add": 2, "sentinels": 2})
        env = {"PATH": "/usr/bin:/bin", "SSDP70_OMP_PROVIDER_CREDENTIAL": "x"}
        (self.work / "READY").write_text("STAGE 2 MAY START\n")
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "start", "2"], capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("not authorized", p.stderr)
        (self.work / "authorizations").mkdir()
        (self.work / "authorizations" / "stage2.ok").write_text("ok")
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "start", "2"], capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("has not finished", p.stderr)

    def test_conditional_commands_are_two_episodes_and_slots_carry_their_command(self):
        run(HERE / "prepare_campaign.py", "plan", *self.args)
        plan = json.loads((self.work / "commands.json").read_text())["commands"]
        cond = [c for c in plan if c["conditional"]]
        self.assertTrue(cond and all(c["episodes"] <= 2 for c in cond))
        decl = json.loads((self.work / "declaration.json").read_text())
        self.assertTrue(all(x["command"] in {c["key"] for c in cond} for x in decl["conditional_slots"]))

    def test_evaluator_profile_has_the_turn_cap(self):
        sys.path.insert(0, str(HERE))
        import prepare_campaign
        prepare_campaign.build_evaluator_key(self.work, "deepseek-ai/DeepSeek-V4.1-Flash")
        prof = json.loads((self.work / "keys" / "omp-evaluator-readonly.json").read_text())
        self.assertEqual(prof["budgets"]["max_turns"], 20)
        self.assertEqual(prof["agent_model"], "deepinfra/deepseek-ai/DeepSeek-V4.1-Flash")

    def test_evaluator_must_not_be_the_executor(self):
        # the evaluator key builder refuses the executor model (calls the module function on a scratch copy)
        sys.path.insert(0, str(HERE))
        import prepare_campaign
        with self.assertRaises(SystemExit) as ctx:
            prepare_campaign.build_evaluator_key(self.work, "zai-org/GLM-5.3-Flash")
        self.assertIn("must not be the executor model", str(ctx.exception))


class CB(unittest.TestCase):
    def test_bundle_has_only_item_rubric_and_task_and_parse_is_strict(self):
        sys.path.insert(0, str(HERE))
        import campaign_cb
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            item = tmp / "cb-aaa.json"
            item.write_text(json.dumps({"item": "cb-aaa", "report": "SSDP 7.2.0 said so"}))
            rub = tmp / "rubric.txt"
            rub.write_text("Rubric for Protocol 7.2.0")
            b = tmp / "b"
            b.mkdir()
            campaign_cb.build_bundle(item, rub, b)
            self.assertEqual(sorted(p.name for p in b.iterdir() if p.is_file()), ["EVIDENCE-MANIFEST.json", "item.json", "shared-rubric.txt", "task.md"])
            self.assertEqual(json.loads((b / "item.json").read_text())["id"], "cb-aaa")
            self.assertNotIn("7.2.0", (b / "shared-rubric.txt").read_text())          # version identifiers are redacted from the rubric
        p = campaign_cb.parse
        self.assertEqual(p('{"item":"cb-1","result":"fail","evidence":"x"}', "cb-1")["result"], "fail")
        self.assertEqual(p('{"item":"cb-2","result":"fail","evidence":"x"}', "cb-1")["result"], "invalid")
        self.assertEqual(p('{"item":"cb-1","result":"maybe","evidence":"x"}', "cb-1")["result"], "invalid")
        self.assertEqual(p("no json", "cb-1")["result"], "invalid")
        self.assertEqual(p(None, "cb-1")["result"], "invalid")

    def test_run_with_a_fake_adapter_writes_results_and_traces(self):
        sys.path.insert(0, str(HERE))
        import types
        import campaign_cb
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            work = tmp / "work"
            shutil.copytree(CAMPAIGN / "keys", work / "keys")
            sys.path.insert(0, str(HERE))
            import prepare_campaign
            prepare_campaign.build_evaluator_key(work, "deepseek-ai/DeepSeek-V4.1-Flash")
            view = tmp / "view"
            view.mkdir()
            for i in ("cb-a", "cb-b"):
                (view / f"{i}.json").write_text(json.dumps({"item": i}))
            rub = tmp / "r.txt"
            rub.write_text("rubric")

            def launch(profile, prompt, bundle, env):
                item = json.loads((bundle / "item.json").read_text())["id"]
                out = json.dumps({"type": "result", "result": json.dumps({"item": item, "result": "pass", "evidence": "ok"})})
                return {"stdout": out + "\n", "stderr": "", "returncode": 0, "command_identity": {}}
            fake = types.SimpleNamespace(clean_env=lambda: {}, realize_containment=lambda *a, **k: {}, launch=launch)
            ns = types.SimpleNamespace(work=work, view_dir=view, rubric=rub, out=tmp / "cb-results.json", limit=None, parallel=2)
            self.assertEqual(campaign_cb.cmd_run(ns, adapter=fake), 0)
            res = json.loads((tmp / "cb-results.json").read_text())
            self.assertEqual(res, {"cb-a": {"result": "pass", "evidence": "ok"}, "cb-b": {"result": "pass", "evidence": "ok"}})
            self.assertTrue((tmp / "cb-traces" / "cb-a.jsonl").exists())


class Assess(unittest.TestCase):
    def test_panel_filter_and_cost_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "commands.json").write_text(json.dumps({"commands": [
                {"key": "main-c01", "panel": "main", "runs": 6}, {"key": "routing-c01", "panel": "routing", "runs": 9}]}))
            for key, name in (("main-c01", "EP-001-p72-r0"), ("main-c01", "EP-001-p66-r0"), ("routing-c01", "P01-p72-r0")):
                d = work / "runs" / key / name
                d.mkdir(parents=True)
                (d / "summary.json").write_text(json.dumps({"evidence_state": "COMPLETE_ADMISSIBLE", "episode": name[:6]}))
                msg = {"type": "message_end", "message": {"role": "assistant", "usage": {"input": 10000, "cacheRead": 40000, "output": 1000}}}
                (d / "assessment-trace.jsonl").write_text(json.dumps(msg) + "\n" + json.dumps(msg) + "\n")
            p = run(HERE / "campaign_assess.py", "run", work, "--keys-root", work, "--evaluator-profile", work, "--evaluator-capabilities", work)
            self.assertEqual(p.returncode, 2)                                   # no credential in this test environment
            p = run(HERE / "campaign_assess.py", "cost", work, "--price-in", "0.2", "--price-cached", "0.006", "--price-out", "0.6")
            out = json.loads(p.stdout)
            self.assertEqual(out["assessed_runs"], 2)                       # the routing run is outside the default panels
            self.assertEqual(out["mean_turns"], 2.0)
            self.assertEqual(out["cache_hit_rate"], 0.8)
            self.assertEqual(out["planned_evaluable_runs"], 6)
            self.assertAlmostEqual(out["mean_usd_per_run"], (2 * (10000 * 0.2 + 40000 * 0.006 + 1000 * 0.6)) / 1e6, places=4)
            self.assertAlmostEqual(out["projected_usd"], round(out["mean_usd_per_run"] * 6, 2), places=2)

    def test_collect_reads_valid_assessments_and_lists_the_rest(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            for name, status in (("EP-001-p72-r0", "VALID"), ("EP-002-p72-r0", "INVALID_SCHEMA"), ("EP-003-p72-r0", None)):
                d = work / "runs" / "main-c01" / name
                d.mkdir(parents=True)
                (d / "summary.json").write_text(json.dumps({"evidence_state": "COMPLETE_ADMISSIBLE", "episode": name[:6]}))
                if status:
                    rows = [{"item": f"{name[:6]}::CLM.1", "result": "fail"}] if status == "VALID" else []
                    (d / "assessment.json").write_text(json.dumps({"assessment_status": status, "dispositions": rows}))
            out = work / "d.json"
            p = run(HERE / "campaign_assess.py", "collect", work, "--out", out)
            self.assertEqual(p.returncode, 4)
            self.assertEqual(json.loads(out.read_text()), {"EP-001-p72-r0::CLM.1": "fail"})
            self.assertIn("no assessment", p.stdout)
            self.assertIn("INVALID_SCHEMA", p.stdout)


if __name__ == "__main__":
    unittest.main()
