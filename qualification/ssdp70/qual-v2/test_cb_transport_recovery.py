import hashlib
import json
import tempfile
import shutil
import types
import unittest
from pathlib import Path
import campaign_cb


class TransportRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = self.root / "work"
        (self.work / "keys").mkdir(parents=True)
        (self.work / "keys/omp-evaluator-readonly.json").write_text("profile")
        (self.work / "campaign-identity.json").write_text("identity")
        old = self.root / "old"
        (old / "cb-traces").mkdir(parents=True)
        self.source = old / "cb-results.json"
        results = {f"cb-{i}": {"result": "fail", "evidence": "original"} for i in range(40)}
        results["cb-0"] = {"result": "invalid", "evidence": "process error"}
        self.source.write_text(json.dumps(results))
        self.trace = old / "cb-traces/cb-0.jsonl"
        self.events = [{"type": "message_end", "message": {"errorMessage": "OpenAI completions stream closed before a finish_reason was received"}}, {"type": "result", "is_error": True}]
        self.trace.write_text("\n".join(map(json.dumps, self.events)))
        new = self.root / "new"
        new.mkdir()
        self.auth = new / "AUTH.json"
        self.a = types.SimpleNamespace(work=self.work, recover_from=self.source, recovery_authorization=self.auth, out=new / "cb-results.json", limit=None)
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        self.authorization = {"scope": "cb-transport-recovery-once", "source": str(self.source), "out": str(self.a.out), "source_sha256": digest(self.source), "profile_sha256": digest(self.work / "keys/omp-evaluator-readonly.json"), "campaign_identity_sha256": digest(self.work / "campaign-identity.json"), "items": ["cb-0"], "trace_sha256": {"cb-0": digest(self.trace)}}
        self.auth.write_text(json.dumps(self.authorization))

    def test_transport_only_preserves_completed_judgments(self):
        prior, ids = campaign_cb.recovery_inputs(self.a)
        self.assertEqual(ids, {"cb-0"})
        self.assertEqual(len(prior), 40)
        self.assertEqual(prior["cb-1"], {"result": "fail", "evidence": "original"})

    def test_changed_source_profile_identity_or_trace_refused(self):
        for p in [self.source, self.trace, self.work / "keys/omp-evaluator-readonly.json", self.work / "campaign-identity.json"]:
            original = p.read_bytes()
            p.write_bytes(original + b" ")
            with self.assertRaises(ValueError):
                campaign_cb.recovery_inputs(self.a)
            p.write_bytes(original)

    def test_behavior_failure_refused_even_with_matching_digest(self):
        self.events[0]["message"]["errorMessage"] = "thinking loop detected"
        self.trace.write_text("\n".join(map(json.dumps, self.events)))
        self.authorization["trace_sha256"]["cb-0"] = hashlib.sha256(self.trace.read_bytes()).hexdigest()
        self.auth.write_text(json.dumps(self.authorization))
        with self.assertRaisesRegex(ValueError, "eligible"):
            campaign_cb.recovery_inputs(self.a)

    def test_completed_judgment_selection_and_output_redirection_refused(self):
        self.authorization["items"] = ["cb-1"]
        self.auth.write_text(json.dumps(self.authorization))
        with self.assertRaisesRegex(ValueError, "exactly"):
            campaign_cb.recovery_inputs(self.a)
        self.a.out = self.root / "elsewhere.json"
        with self.assertRaisesRegex(ValueError, "authorization"):
            campaign_cb.recovery_inputs(self.a)

    def test_real_run_merges_once_and_refuses_second_launch(self):
        key_root = Path("/home/samjin/ssdp70-omp-stagef/qualification/campaign-72-20261008/keys")
        for name in ["omp-evaluator-readonly.json", "omp-evaluator-readonly.capabilities.json"]:
            shutil.copy2(key_root / name, self.work / "keys" / name)
        self.authorization["profile_sha256"] = hashlib.sha256((self.work / "keys/omp-evaluator-readonly.json").read_bytes()).hexdigest()
        self.auth.write_text(json.dumps(self.authorization))
        original_results = json.loads(self.source.read_text())
        original_results["cb-2"] = {"result": "invalid", "evidence": "process error"}
        self.source.write_text(json.dumps(original_results))
        second_trace = self.trace.with_name("cb-2.jsonl")
        second_trace.write_bytes(self.trace.read_bytes())
        self.authorization["source_sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.authorization["items"] = ["cb-0", "cb-2"]
        self.authorization["trace_sha256"]["cb-2"] = hashlib.sha256(second_trace.read_bytes()).hexdigest()
        self.auth.write_text(json.dumps(self.authorization))
        original_traces = {p.name: p.read_bytes() for p in self.trace.parent.iterdir()}
        view = self.root / "view"
        view.mkdir()
        (view / "cb-0.json").write_text(json.dumps({"item": "cb-0"}))
        (view / "cb-2.json").write_text(json.dumps({"item": "cb-2"}))
        rubric = self.root / "rubric"
        rubric.write_text("synthetic rubric")
        self.a.view_dir, self.a.rubric, self.a.parallel = view, rubric, 1
        launches = []
        def launch(profile, prompt, bundle, env):
            item = json.loads((bundle / "item.json").read_text())["id"]
            launches.append(item)
            out = json.dumps({"type": "result", "result": json.dumps({"item": item, "result": "fail", "evidence": "recovered"})})
            return {"stdout": out, "returncode": 0}
        adapter = types.SimpleNamespace(clean_env=lambda: {}, realize_containment=lambda *a: {}, launch=launch)
        original = self.source.read_bytes()
        self.assertEqual(campaign_cb.cmd_run(self.a, adapter), 0)
        merged = json.loads(self.a.out.read_text())
        self.assertEqual(len(merged), 40)
        self.assertEqual(merged["cb-0"]["evidence"], "recovered")
        self.assertEqual(merged["cb-1"]["evidence"], "original")
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual({p.name: p.read_bytes() for p in self.trace.parent.iterdir()}, original_traces)
        self.assertEqual({p.stem for p in (self.a.out.parent / "cb-traces").iterdir()}, {"cb-0", "cb-2"})
        for key, value in original_results.items():
            if key not in {"cb-0", "cb-2"}:
                self.assertEqual(merged[key], value)
        self.assertEqual(campaign_cb.cmd_run(self.a, adapter), 2)
        self.assertEqual(len(launches), 2)
        self.a.out.unlink()
        shutil.rmtree(self.a.out.parent / "cb-traces")
        self.assertEqual(campaign_cb.cmd_run(self.a, adapter), 2)
        self.assertEqual(len(launches), 2)
