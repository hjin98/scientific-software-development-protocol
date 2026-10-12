"""Once-only format rerun of format-invalid evaluator assessments (campaign_assess): selection, binding, once-only, collection, reporting."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import campaign_assess as ca


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


ENV = {"SSDP70_OMP_PROVIDER_CREDENTIAL": "x"}


class FormatRerun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.w = Path(self.tmp.name)
        self.profile = self.w / "profile.json"; self.profile.write_text("{}")
        self.caps = self.w / "caps.json"; self.caps.write_text("{}")
        self.keys = self.w / "keys-root"
        (self.w / "authorizations").mkdir(); (self.w / "authorizations/evaluator-full.ok").write_text("ok")
        self.made = set()
        self.slots = {"A": "main-c01/E1-p72-r0", "B": "main-c01/E2-p66-r0", "C": "main-c02/E3-p66b-r0", "D": "main-c02/E4-p72-r0"}
        self.primary = self.w / "evaluations/mimo-1"
        self.rerun = self.w / "evaluations/mimo-1-format-rerun-1"
        errors = {"A": ["item unauthorized_mutation critical does not match manifest"], "D": ["no result text"]}
        for k, status in (("A", "INVALID_SCHEMA"), ("B", "VALID"), ("C", "EXECUTION_ERROR"), ("D", "UNPARSEABLE")):
            self.make_run(k, status, errors.get(k, []))

    def make_run(self, key, status, errors=()):
        slot = self.slots[key]
        d = self.w / "runs" / slot
        d.mkdir(parents=True)
        (d / "summary.json").write_text(json.dumps({"evidence_state": "COMPLETE_ADMISSIBLE", "episode": key}))
        (self.keys / key).mkdir(parents=True, exist_ok=True)
        out = self.primary / slot
        out.mkdir(parents=True)
        body = {"assessment_status": status, "errors": list(errors)}
        if status == "VALID":
            body["dispositions"] = [{"item": f"{key}::i", "result": "pass"}]
        (out / "assessment.json").write_text(json.dumps(body))
        (out / "assessment-identity.json").write_text(json.dumps({"identity_sha256": f"id-{key}"}))

    def authorize(self, phase="format-rerun", runs=None, **over):
        self.rerun.mkdir(parents=True, exist_ok=True)
        if runs is None:
            runs = {self.slots[k]: sha(self.primary / self.slots[k] / "assessment.json") for k in ("A", "D")}
        eval_dir = Path(ca.__file__).resolve().parent.parent / "eval"
        auth = {"phase": phase, "source_root": "mimo-1", "runs": runs, "panels": ["main"],
                "assess_sha256": sha(eval_dir / "assess70.py"), "core_sha256": sha(eval_dir / "core70.py"),
                "assessment_evidence_sha256": sha(eval_dir / "assessment_evidence.py"),
                "driver_sha256": sha(Path(ca.__file__)), "profile_sha256": sha(self.profile)}
        auth.update(over)
        (self.rerun / "PASS-AUTHORIZATION.json").write_text(json.dumps(auth))

    def args(self, **over):
        a = argparse.Namespace(work=self.w, panels=["main"], assessment_root=self.rerun, format_rerun_of=self.primary, limit=None,
                               parallel=2, evaluator_profile=self.profile, evaluator_capabilities=self.caps, keys_root=self.keys, shared_rubric=None,
                               rerun_root=None, out=self.w / "disp.json")
        for k, v in over.items():
            setattr(a, k, v)
        return a

    def fake_one(self, calls, result="VALID", ident=True):
        def one(d, a):
            calls.append(slot := d.relative_to(self.w / "runs").as_posix())
            out = ca.assessment_dir(d, a)
            out.mkdir(parents=True)
            body = {"assessment_status": result, "errors": ["no result text"] if result != "VALID" else []}
            if result == "VALID":
                body["dispositions"] = [{"item": f"{d.name}::i", "result": "fail"}]
            (out / "assessment.json").write_text(json.dumps(body))
            (out / "assessment-identity.json").write_text(json.dumps({"identity_sha256": ("id-" + d.name.split("-")[0].replace("E1", "A").replace("E4", "D").replace("E3", "C").replace("E5", "E")) if ident else "other"}))
            return d.name, 1
        return one

    def go(self, calls=None, **kw):
        calls = [] if calls is None else calls
        with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", self.fake_one(calls, **kw)):
            return ca.cmd_run(self.args()), calls

    def test_reruns_only_the_frozen_format_invalid_runs_once(self):
        self.authorize()
        rc, calls = self.go()
        self.assertEqual(rc, 0)
        self.assertEqual(sorted(calls), sorted([self.slots["A"], self.slots["D"]]))
        self.assertTrue((self.rerun / "FORMAT-RERUN-STARTED.json").is_file())
        for slot in calls:                                          # remove the outputs: the marker alone still refuses a repeat
            out = ca.assessment_dir(self.w / "runs" / slot, self.args())
            (out / "assessment.json").unlink(); (out / "assessment-identity.json").unlink(); out.rmdir()
        rc2, calls2 = self.go()
        self.assertEqual((rc2, calls2), (2, []))

    def test_refusals_before_any_call_and_before_the_marker(self):
        def refused(reason):
            rc, calls = self.go()
            self.assertEqual((rc, calls), (2, []), reason)
            self.assertFalse((self.rerun / "FORMAT-RERUN-STARTED.json").exists(), reason)
        refused("no authorization")
        self.authorize(phase="pilot"); refused("wrong phase")
        self.authorize(driver_sha256="0" * 64); refused("identity differs")
        self.authorize(runs={self.slots["B"]: sha(self.primary / self.slots["B"] / "assessment.json")}); refused("VALID primary")
        self.authorize(runs={self.slots["C"]: sha(self.primary / self.slots["C"] / "assessment.json")}); refused("EXECUTION_ERROR primary")
        self.authorize(runs={self.slots["A"]: sha(self.primary / self.slots["A"] / "assessment.json")}); refused("partial set (hand-picked subset)")
        self.authorize(runs={self.slots["A"]: "0" * 64, self.slots["D"]: sha(self.primary / self.slots["D"] / "assessment.json")}); refused("primary changed since freeze")
        self.authorize(runs={"../../x/E1-p72-r0": "0" * 64, self.slots["D"]: "0" * 64}); refused("traversing slot")
        self.authorize(source_root="other"); refused("source root")
        self.authorize()
        (self.w / "authorizations/evaluator-full.ok").unlink(); refused("primary pass not released")
        (self.w / "authorizations/evaluator-full.ok").write_text("ok")
        (self.primary / self.slots["B"] / "assessment.json").unlink(); refused("primary pass incomplete")
        (self.primary / self.slots["B"] / "assessment.json").write_text(json.dumps({"assessment_status": "VALID", "dispositions": []}))
        with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", self.fake_one([])):
            self.assertEqual(ca.cmd_run(self.args(limit=5)), 2)
            self.assertEqual(ca.cmd_run(self.args(format_rerun_of=self.rerun)), 2)       # primary must differ from rerun root
            nested = self.rerun / "nested"; nested.mkdir()
            self.assertEqual(ca.cmd_run(self.args(format_rerun_of=nested)), 2)
            self.assertEqual(ca.cmd_run(self.args(keys_root=self.w / "missing")), 2)     # not viable: marker not consumed
            self.assertEqual(ca.cmd_run(self.args(evaluator_capabilities=self.w / "nope")), 2)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(ca, "one", self.fake_one([])):
            self.assertEqual(ca.cmd_run(self.args()), 2)                                  # no credential
        self.assertFalse((self.rerun / "FORMAT-RERUN-STARTED.json").exists())

    def test_exception_after_the_marker_is_not_retried_and_exits_3(self):
        self.authorize()
        def boom(d, a): raise RuntimeError("provider")
        with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", boom):
            self.assertEqual(ca.cmd_run(self.args()), 3)
        self.assertTrue((self.rerun / "FORMAT-RERUN-STARTED.json").is_file())
        rc, calls = self.go()
        self.assertEqual((rc, calls), (2, []))

    def test_bad_assess_exit_gives_driver_exit_3(self):
        self.authorize()
        def one(d, a):
            ca.assessment_dir(d, a).mkdir(parents=True); return d.name, 7
        with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", one):
            self.assertEqual(ca.cmd_run(self.args()), 3)

    def test_collect_substitution_marker_identity_and_report(self):
        self.authorize()
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        self.assertEqual(ca.cmd_collect(a), 4)                                            # no marker, no reruns
        self.assertNotIn("E1-p72-r0::i", json.loads(a.out.read_text()))
        rc, _ = self.go(); self.assertEqual(rc, 0)
        self.assertEqual(ca.cmd_collect(a), 4)                                            # C (EXECUTION_ERROR) still blocks
        out = json.loads(a.out.read_text())
        self.assertEqual(out, {"E1-p72-r0::i": "fail", "E2-p66-r0::i": "pass", "E4-p72-r0::i": "fail"})
        # marker no longer matches an edited authorization
        auth = json.loads((self.rerun / "PASS-AUTHORIZATION.json").read_text()); auth["note"] = "edited"
        (self.rerun / "PASS-AUTHORIZATION.json").write_text(json.dumps(auth))
        self.assertEqual(ca.cmd_collect(a), 4); self.assertNotIn("E1-p72-r0::i", json.loads(a.out.read_text()))
        self.authorize(); (self.rerun / "FORMAT-RERUN-STARTED.json").write_text(json.dumps({"runs": sorted([self.slots["A"], self.slots["D"]]), "authorization_sha256": sha(self.rerun / "PASS-AUTHORIZATION.json")}))
        self.assertEqual(ca.cmd_collect(a), 4); self.assertIn("E1-p72-r0::i", json.loads(a.out.read_text()))
        # a rerun whose identity differs from the primary's is not accepted
        (self.rerun / self.slots["A"] / "assessment-identity.json").write_text(json.dumps({"identity_sha256": "other"}))
        self.assertEqual(ca.cmd_collect(a), 4); self.assertNotIn("E1-p72-r0::i", json.loads(a.out.read_text()))

    def test_second_invalid_stays_unresolved_and_is_reported_per_arm(self):
        self.authorize()
        rc, _ = self.go(result="INVALID_SCHEMA"); self.assertEqual(rc, 0)
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 4)
        report = json.loads(pr.call_args_list[-1].args[0])["format_failure_report"]
        self.assertEqual((report["first_draw_format_failures"], report["reruns_attempted"], report["reruns_valid"], report["reruns_second_invalid"]), (2, 2, 0, 2))
        self.assertEqual(report["by_arm"], {"p72": 2}); self.assertEqual(report["by_class"], {"no-result-text": 1, "schema": 1})
        self.assertEqual(report["items_named_in_errors"], {"unauthorized_mutation": 1})
        self.assertEqual(report["second_invalid_same_class_as_first"], 1)                   # D: no-result-text -> no-result-text
        self.assertNotIn("E1-p72-r0::i", json.loads(a.out.read_text()))

    def test_execution_error_rerun_is_not_counted_as_a_same_class_format_failure(self):
        self.authorize()
        rc, _ = self.go(result="EXECUTION_ERROR"); self.assertEqual(rc, 0)
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 4)
        report = json.loads(pr.call_args_list[-1].args[0])["format_failure_report"]
        self.assertEqual((report["reruns_attempted"], report["reruns_second_invalid"], report["second_invalid_same_class_as_first"], report["reruns_second_not_format_invalid"]), (2, 2, 0, 2))
        self.assertEqual({r["rerun_class"] for r in report["rows"]}, {"EXECUTION_ERROR"})

    def test_missing_rerun_is_counted_and_panels_are_bound(self):
        self.authorize()
        rc, _ = self.go(); self.assertEqual(rc, 0)
        (self.rerun / self.slots["D"] / "assessment.json").unlink()
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 4)
        self.assertEqual(json.loads(pr.call_args_list[-1].args[0])["format_failure_report"]["reruns_missing_or_rejected"], 1)
        self.assertEqual(ca.cmd_collect(self.args(assessment_root=self.primary, rerun_root=self.rerun, panels=["main", "versioning"])), 2)
        self.authorize(panels=["versioning"])
        with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", self.fake_one([])):
            self.assertEqual(ca.cmd_run(self.args()), 2)                                  # authorization panels differ from --panels

    def test_collect_never_lets_a_stray_rerun_rescue_a_valid_or_execution_error_primary(self):
        self.authorize()
        rc, _ = self.go(); self.assertEqual(rc, 0)
        for key in ("B", "C"):                                                              # stray reruns beside non-format-invalid primaries
            out = self.rerun / self.slots[key]; out.mkdir(parents=True)
            (out / "assessment.json").write_text(json.dumps({"assessment_status": "VALID", "dispositions": [{"item": f"{key}::i", "result": "fail"}]}))
            (out / "assessment-identity.json").write_text(json.dumps({"identity_sha256": f"id-{key}"}))
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        self.assertEqual(ca.cmd_collect(a), 4)
        out = json.loads(a.out.read_text())
        self.assertEqual(out["E2-p66-r0::i"], "pass"); self.assertNotIn("E3-p66b-r0::i", out)
        (self.rerun / "PASS-AUTHORIZATION.json").write_text(json.dumps({"phase": "pilot", "source_root": "mimo-1"}))
        self.assertEqual(ca.cmd_collect(a), 2)
        self.assertEqual(ca.cmd_collect(self.args(assessment_root=self.primary, rerun_root=None)), 4)   # no rerun root: reruns unused
        for slot in self.slots.values():
            self.assertTrue((self.primary / slot / "assessment.json").is_file())

    # ---- provider-transport EXECUTION_ERROR primaries (contract section 3), rerun with the format-invalid ones ----
    def trace(self, key, **last):
        out = self.primary / self.slots[key]
        rows = [{"type": "message_end", "message": {"role": "assistant", "stopReason": "stop"}}, {"type": "message_update"}]
        if last:
            rows.append({"type": "message_end", "message": {"role": "assistant", "content": [{"type": "thinking", "thinking": "x"}], **last}})
        (out / "assessment-trace.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        return out

    def authorize_with_transport(self, **over):
        runs = {self.slots[k]: sha(self.primary / self.slots[k] / "assessment.json") for k in ("A", "C", "D")}
        trace = ca.trace_digest(self.primary / self.slots["C"])
        self.authorize(runs=runs, transport_runs={self.slots["C"]: trace}, **over)

    def test_transport_failure_classification_is_mechanical(self):
        closed = {"stopReason": "error", "errorMessage": "OpenAI completions stream closed before a finish_reason was received"}
        cases = [(closed, True), ({"stopReason": "error", "errorStatus": 502, "errorMessage": "bad gateway"}, True),
                 ({"stopReason": "error", "errorStatus": 429, "errorMessage": "429 rate limit exceeded"}, True),
                 ({"stopReason": "error", "errorStatus": 403, "errorMessage": "403 qualification turn budget exhausted"}, False),
                 ({"stopReason": "error", "errorStatus": 408, "errorMessage": "request timeout"}, False),
                 ({"stopReason": "error", "errorMessage": "something else"}, False), ({"stopReason": "stop"}, False)]
        for last, expected in cases:
            self.assertEqual(ca.transport_failure(self.trace("C", **last)), expected, last)
        # an evaluator decision at the failure point (streamed answer, partial answer or tool call) is not transport, nor is a timeout or any result text
        for content in ([{"type": "text", "text": "{\"episode\": \"E3\"}"}], [{"type": "thinking"}, {"type": "text", "text": "partial"}], [{"type": "toolCall", "name": "read"}]):
            self.assertFalse(ca.transport_failure(self.trace("C", content=content, **closed)), content)
        self.assertTrue(ca.transport_failure(self.trace("C", content=[{"type": "thinking"}, {"type": "text", "text": "  "}], **closed)))
        body = json.loads((self.primary / self.slots["C"] / "assessment.json").read_text())
        for patch in ({"errors": ["evaluator process failed or returned an error (returncode=124)"]}, {"raw_result": "some text"}, {"assessment_status": "INVALID_SCHEMA"}):
            (self.primary / self.slots["C"] / "assessment.json").write_text(json.dumps({**body, **patch}))
            self.assertFalse(ca.transport_failure(self.trace("C", **closed)), patch)
        (self.primary / self.slots["C"] / "assessment.json").write_text(json.dumps(body))
        (self.primary / self.slots["C"] / "assessment-trace.jsonl").unlink()
        self.assertFalse(ca.transport_failure(self.primary / self.slots["C"]))                 # no trace: not transport (timeout, harness)
        self.assertFalse(ca.transport_failure(self.trace("B", **closed)))                      # a VALID assessment is never transport

    def test_transport_primary_is_rerun_once_with_the_format_invalid_runs(self):
        self.trace("C", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        self.authorize_with_transport()
        rc, calls = self.go()
        self.assertEqual((rc, sorted(calls)), (0, sorted(self.slots[k] for k in "ACD")))
        self.assertEqual(self.go()[0], 2)                                                      # the marker makes it once-only

    def test_transport_set_must_match_exactly(self):
        self.trace("C", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        self.authorize(); rc, calls = self.go(); self.assertEqual((rc, calls), (2, []))        # transport slot left out of the frozen set
        self.authorize(runs={self.slots[k]: sha(self.primary / self.slots[k] / "assessment.json") for k in "ACD"}); rc, calls = self.go()
        self.assertEqual((rc, calls), (2, []))                                                 # included but not declared as transport
        self.trace("C", stopReason="error", errorStatus=403, errorMessage="qualification turn budget exhausted")
        self.authorize_with_transport(); rc, calls = self.go(); self.assertEqual((rc, calls), (2, []))   # declared but not a transport failure
        self.trace("C", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        runs = {self.slots[k]: sha(self.primary / self.slots[k] / "assessment.json") for k in "ACD"}
        for bad in ([self.slots["C"]], {self.slots["C"]: 5}, {self.slots["C"]: "0" * 64}):   # malformed / wrong trace digest: a refusal, never a crash or a call
            self.authorize(runs=runs, transport_runs=bad); rc, calls = self.go(); self.assertEqual((rc, calls), (2, []), bad)
        self.assertFalse((self.rerun / "FORMAT-RERUN-STARTED.json").exists())

    def test_collect_uses_a_transport_rerun_only_when_valid_and_reports_it(self):
        self.trace("C", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        self.authorize_with_transport()
        rc, _ = self.go(); self.assertEqual(rc, 0)
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        t = self.primary / self.slots["C"] / "assessment-trace.jsonl"; original = t.read_text()
        t.write_text(original + "\n")                                                          # a primary trace changed since the freeze is not accepted
        self.assertEqual(ca.cmd_collect(a), 4); self.assertNotIn("E3-p66b-r0::i", json.loads(a.out.read_text()))
        t.write_text(original)
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 0)
        out = json.loads(a.out.read_text())
        self.assertIn("E3-p66b-r0::i", out)
        report = json.loads(pr.call_args[0][0])["format_failure_report"]
        self.assertEqual((report["first_draw_format_failures"], report["first_draw_transport_failures"], report["by_class"]),
                         (2, 1, {"no-result-text": 1, "schema": 1, "transport": 1}))
        # a second transport failure stays unresolved and is reported as the same class
        c_out = self.rerun / self.slots["C"]
        (c_out / "assessment.json").write_text(json.dumps({"assessment_status": "EXECUTION_ERROR", "errors": ["returncode=0"]}))
        (c_out / "assessment-trace.jsonl").write_text(json.dumps({"type": "message_end", "message": {"role": "assistant", "stopReason": "error", "content": [{"type": "thinking"}],
                                                       "errorMessage": "stream closed before a finish_reason was received"}}) + "\n")
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 4)
        report = json.loads(pr.call_args[0][0])["format_failure_report"]
        self.assertEqual((report["reruns_second_invalid"], report["second_invalid_same_class_as_first"]), (1, 1))
        self.assertNotIn("E3-p66b-r0::i", json.loads(a.out.read_text()))

    # ---- evaluator-limit EXECUTION_ERROR primaries (eighth ruling): wall-clock limit (returncode 124) or turn budget (403) ----
    made = set()

    def add_limit_slot(self, kind):
        self.slots["E"] = "main-c03/E5-p66-r0"
        body = {"errors": ["evaluator process failed or returned an error (returncode=124)", "invalid JSON result: substring not found"]} if kind == "timeout" else {"errors": ["evaluator process failed or returned an error (returncode=0)"]}
        if "E" not in self.made:
            self.make_run("E", "EXECUTION_ERROR", body["errors"]); self.made.add("E")
        else:
            (self.primary / self.slots["E"] / "assessment.json").write_text(json.dumps({"assessment_status": "EXECUTION_ERROR", "errors": body["errors"]}))
        if kind == "budget":
            self.trace("E", stopReason="error", errorStatus=403, errorMessage="403 qualification turn budget exhausted\nqualification turn budget exhausted (type=turn_budget)")

    def test_limit_failure_classification_is_mechanical_and_disjoint_from_transport(self):
        self.add_limit_slot("timeout"); out = self.primary / self.slots["E"]
        self.assertTrue(ca.limit_failure(out)); self.assertFalse(ca.transport_failure(out)); self.assertEqual(ca.exec_class(out), "limit")
        self.add_limit_slot("budget"); self.assertTrue(ca.limit_failure(out)); self.assertEqual(ca.exec_class(out), "limit")
        self.trace("E", stopReason="error", errorStatus=403, errorMessage="forbidden for another reason")
        self.assertFalse(ca.limit_failure(out))
        self.trace("E", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        self.assertEqual(ca.exec_class(out), "transport")
        body = json.loads((out / "assessment.json").read_text())
        for patch in ({"raw_result": "text"}, {"assessment_status": "VALID"}):
            (out / "assessment.json").write_text(json.dumps({**body, **patch}))
            self.assertFalse(ca.limit_failure(out), patch)
        (out / "assessment.json").write_text(json.dumps({"assessment_status": "EXECUTION_ERROR", "raw_result": "partial", "errors": ["returncode=124"]}))
        self.assertFalse(ca.limit_failure(out))                                                  # a timeout that left result text is not a limit slot
        (out / "assessment.json").write_text(json.dumps(body))
        (out / "assessment-trace.jsonl").unlink()
        (out / "assessment.json").write_text(json.dumps({"assessment_status": "EXECUTION_ERROR", "errors": ["returncode=0"]}))     # clean exit, no trace
        self.assertIsNone(ca.exec_class(out))

    def test_limit_primary_is_rerun_with_the_others_and_the_set_must_match(self):
        self.trace("C", stopReason="error", errorMessage="stream closed before a finish_reason was received")
        self.add_limit_slot("budget")
        runs = {self.slots[k]: sha(self.primary / self.slots[k] / "assessment.json") for k in "ACDE"}
        tr, li = {self.slots["C"]: ca.trace_digest(self.primary / self.slots["C"])}, {self.slots["E"]: ca.trace_digest(self.primary / self.slots["E"])}
        self.authorize(runs=runs, transport_runs=tr); self.assertEqual(self.go(), (2, []))                          # limit slot not declared
        self.authorize(runs=runs, transport_runs={**tr, **li}, limit_runs={}); self.assertEqual(self.go(), (2, []))  # declared in the wrong class
        self.authorize(runs=runs, transport_runs=tr, limit_runs={self.slots["E"]: "0" * 64}); self.assertEqual(self.go(), (2, []))   # wrong trace digest
        self.authorize(runs=runs, transport_runs=tr, limit_runs=[self.slots["E"]]); self.assertEqual(self.go(), (2, []))             # malformed
        self.assertFalse((self.rerun / "FORMAT-RERUN-STARTED.json").exists())
        self.authorize(runs=runs, transport_runs=tr, limit_runs=li)
        rc, calls = self.go(); self.assertEqual((rc, sorted(calls)), (0, sorted(self.slots[k] for k in "ACDE")))
        a = self.args(assessment_root=self.primary, rerun_root=self.rerun)
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 0)
        report = json.loads(pr.call_args[0][0])["format_failure_report"]
        self.assertEqual((report["first_draw_format_failures"], report["first_draw_transport_failures"], report["first_draw_limit_failures"]), (2, 1, 1))
        e_out = self.rerun / self.slots["E"]                                                       # a limit rerun that fails again stays unresolved, same class
        (e_out / "assessment.json").write_text(json.dumps({"assessment_status": "EXECUTION_ERROR", "errors": ["returncode=124"]}))
        with mock.patch("builtins.print") as pr:
            self.assertEqual(ca.cmd_collect(a), 4)
        report = json.loads(pr.call_args[0][0])["format_failure_report"]
        self.assertEqual((report["reruns_second_invalid"], report["second_invalid_same_class_as_first"]), (1, 1))
        t = self.primary / self.slots["E"] / "assessment-trace.jsonl"; original = t.read_text()
        t.write_text(original + "\n")
        self.assertEqual(ca.cmd_collect(a), 4)                                                                    # primary trace changed since the freeze
        t.write_text(original)


class ExecutorReruns(unittest.TestCase):
    def test_run_dirs_take_a_substituting_rerun_and_never_a_sibling(self):
        with tempfile.TemporaryDirectory() as t:
            w = Path(t)
            def run(rel, state, err=""):
                d = w / "runs" / rel
                d.mkdir(parents=True)
                (d / "summary.json").write_text(json.dumps({"evidence_state": state, "evidence_state_reasons": [], "episode": "E1"}))
                term = {"state": "error" if err else "completed", "native_return_state": {"errorMessage": err}}
                (d / "events.normalized.jsonl").write_text(json.dumps({"kind": "termination", "payload": term}) + "\n")
            run("main-c01/E1-p72-r0", "EXECUTION_ERROR", "429 Model busy, retry later")
            run("main-c01/E1-p72-r1", "COMPLETE_ADMISSIBLE")
            run("rerun-s1-p72/main-c01/E1-p72-r0", "COMPLETE_ADMISSIBLE")
            run("rerun-s1-p72/main-c01/E1-p72-r1", "COMPLETE_ADMISSIBLE")
            got = [ca.slot_of(d, w) for d in ca.run_dirs(w, ["main"])]
            self.assertEqual(got, ["main-c01/E1-p72-r0", "main-c01/E1-p72-r1", "rerun-s1-p72/main-c01/E1-p72-r0"])
            self.assertTrue(all(ca.SLOT.fullmatch(s) for s in got))


class OrdinaryPathUnchanged(unittest.TestCase):
    def test_full_pass_still_needs_evaluator_full_ok_and_pilot_still_needs_limit_5(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = Path(tmp); prof = w / "p.json"; prof.write_text("{}")
            root = w / "evaluations/mimo-x"; root.mkdir(parents=True)
            eval_dir = Path(ca.__file__).resolve().parent.parent / "eval"
            auth = {"phase": "full", "assess_sha256": sha(eval_dir / "assess70.py"), "core_sha256": sha(eval_dir / "core70.py"),
                    "assessment_evidence_sha256": sha(eval_dir / "assessment_evidence.py"), "driver_sha256": sha(Path(ca.__file__)), "profile_sha256": sha(prof)}
            (root / "PASS-AUTHORIZATION.json").write_text(json.dumps(auth))
            a = argparse.Namespace(work=w, panels=["main"], assessment_root=root, limit=None, parallel=1, evaluator_profile=prof, evaluator_capabilities=prof,
                                   keys_root=w, shared_rubric=None, format_rerun_of=None)
            with mock.patch.dict(os.environ, ENV), mock.patch.object(ca, "one", side_effect=AssertionError("no call expected")):
                self.assertEqual(ca.cmd_run(a), 2)                                          # no evaluator-full.ok
                auth["phase"] = "pilot"; (root / "PASS-AUTHORIZATION.json").write_text(json.dumps(auth))
                self.assertEqual(ca.cmd_run(a), 2)                                          # pilot needs --limit 5
                auth["phase"] = "format-rerun"; (root / "PASS-AUTHORIZATION.json").write_text(json.dumps(auth))
                self.assertEqual(ca.cmd_run(a), 2)                                          # not a primary phase


if __name__ == "__main__":
    unittest.main()
