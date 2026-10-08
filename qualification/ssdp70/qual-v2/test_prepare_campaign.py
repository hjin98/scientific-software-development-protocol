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
        self.assertFalse((self.work / "launch").exists() and any((self.work / "launch").iterdir()))
        key = next(c["key"] for c in json.loads((self.work / "commands.json").read_text())["commands"] if c["conditional"])
        p = subprocess.run([sys.executable, HERE / "campaign_run.py", str(self.work), "run-conditional", key], capture_output=True, text=True,
                           env={**env, "SSDP70_OMP_PROVIDER_CREDENTIAL": "x"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("not authorized", p.stderr)

    def test_evaluator_must_not_be_the_executor(self):
        # the evaluator key builder refuses the executor model (calls the module function on a scratch copy)
        sys.path.insert(0, str(HERE))
        import prepare_campaign
        with self.assertRaises(SystemExit) as ctx:
            prepare_campaign.build_evaluator_key(self.work, "zai-org/GLM-5.3-Flash")
        self.assertIn("must not be the executor model", str(ctx.exception))


class Assess(unittest.TestCase):
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
