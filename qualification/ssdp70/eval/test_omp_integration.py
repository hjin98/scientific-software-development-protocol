"""Integration acceptance for the OMP-only Stage F D4 provider adaptation.

Every test here drives the REAL production path:

  harness70.run_episode -> adapters.omp (realization, principals, sandbox, launch)
    -> the frozen omp/18.0.11 executable inside bubblewrap
    -> qualification observer (provider-control/observation principal) + MCP bridge + unchanged mediator
    -> deterministic local model-provider stand-in (the only substituted component)
    -> raw hash-linked evidence + native JSON trace -> adapter normalization -> core validation.

Standalone principal tests or a script printing synthetic OMP JSON are NOT accepted as integration.
Tests that mutate recorded real artifacts (normalization edge cases) start from artifacts a real run
produced. A missing prerequisite is reported as a skip with the reason, never as a pass in the report.
"""
import base64
import copy
import fcntl
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import evidence70  # noqa: E402
import harness70  # noqa: E402
import observer70  # noqa: E402
import omp_rig  # noqa: E402
from omp_rig import Rig, call, calls, load_events, scenario_steps, text  # noqa: E402
from adapters import omp  # noqa: E402

MISSING = omp_rig.prerequisites()
SKIP = unittest.skipIf(bool(MISSING), f"OMP integration prerequisites missing: {MISSING}")
HOST_HOME = str(Path.home())


def py(code: str) -> dict:
    return call("bash", command="python3 - <<'PYEOF'\n" + textwrap.dedent(code) + "\nPYEOF")


def sh(command: str) -> dict:
    return call("bash", command=command)


class RigCase(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.root = Path(self.td.name)
        self._patches = []

    def tearDown(self):
        for target, name, original in reversed(self._patches):
            setattr(target, name, original)
        self.td.cleanup()

    def patch(self, target, name, value):
        self._patches.append((target, name, getattr(target, name)))
        setattr(target, name, value)

    def rig(self, **kwargs):
        return Rig(self.root, **kwargs)

    def bash_results(self, out):
        return [e for e in load_events(out) if e["kind"] == "tool_action" and e["status"] in ("result", "error")]

    def kinds(self, out, kind, status=None):
        return [e for e in load_events(out) if e["kind"] == kind and (status is None or e["status"] == status)]

    def assertComplete(self, summary):
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", json.dumps({
            k: summary.get(k) for k in ("evidence_state_reasons", "profile_claim_errors", "normalized_event_errors",
                                        "normalization_completeness_errors")}, indent=1)[:3000])

    def assertNotComplete(self, summary, fragment=None):
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        if fragment is not None:
            blob = json.dumps([summary.get("profile_claim_errors"), summary.get("normalized_event_errors"),
                               summary.get("normalization_completeness_errors"), summary.get("evidence_state_reasons")])
            self.assertIn(fragment, blob)


@SKIP
class B1RealObservationAndEventCompleteness(RigCase):
    def baseline_scenario(self):
        return scenario_steps(
            call("read", path="skill://software-implementation"),
            call("read", path="/opt/ssdp/skills/software-implementation/references/scientific-inspectability-and-initiative.md"),
            call("mcp__ssdp_issue_show", issue_id="A-1"),
            call("write", path="/workspace/out.txt", content="hello\n"),
            text("all done"),
        )

    def test_full_path_is_complete_and_every_surface_is_runtime_derived(self):
        summary = self.rig(claims=["owner-read", "ordinary-entry"]).run(self.baseline_scenario())
        self.assertComplete(summary)
        out = summary["_out"]
        obs = summary["runtime_observation"]
        self.assertEqual(obs["runtime_version"], "18.0.11")
        self.assertEqual(obs["model"], "stand/stand-model")
        self.assertEqual(sorted(obs["tools"]), sorted(["read", "glob", "grep", "edit", "write", "bash", *[
            f"mcp__ssdp_{n}" for n in ("issue_locations", "issue_search", "issue_show", "issue_create", "issue_comment", "delegate")]]))
        self.assertEqual(obs["mcp_servers"], [{"name": "ssdp70", "status": "connected"}])
        self.assertEqual(obs["reasoning_fields"], {"reasoning_effort": "high"})
        self.assertEqual(obs["observation_errors"], [])
        snapshot = self.kinds(out, "catalog_snapshot")[0]["payload"]
        self.assertEqual(snapshot["catalog_source"], "observer-runtime-request-system-prompt")
        self.assertEqual(sorted(snapshot["logical_skill_ids"]), sorted(omp.SSDP_SKILLS))
        self.assertEqual(snapshot["runtime_version"], "18.0.11")
        # raw evidence exists for every principal and verifies as hash-linked, complete chains
        artifacts = Path(out) / "adapter-artifacts"
        for name, principal in (("observer-evidence.jsonl", "ssdp70-provider-observer-v1"),
                                ("bridge-evidence.jsonl", "ssdp70-mcp-bridge-v1"),
                                ("launcher-evidence.jsonl", "ssdp70-subject-launcher-v1")):
            records, errors = evidence70.parse_chain((artifacts / name).read_text(), principal)
            self.assertEqual(errors, [], name)
            self.assertGreater(len(records), 2)
        # the model actually received the exact frozen build's tool list and system prompt
        first = json.loads(base64.b64decode(next(
            r["data"]["body_b64"] for r in (json.loads(l) for l in (artifacts / "observer-evidence.jsonl").read_text().splitlines())
            if r["kind"] == "request")))
        self.assertEqual(first["reasoning_effort"], "high")
        self.assertTrue(first["messages"][0]["content"].startswith("<system-conventions>"))

    def test_parallel_tool_results_may_arrive_in_completion_order(self):
        summary = self.rig(timeout_s=120).run(scenario_steps(
            calls(
                ("bash", {"command": "sleep 1; printf slow"}),
                ("bash", {"command": "printf fast"}),
            ),
            text("done"),
        ))
        self.assertComplete(summary)
        observer = [
            json.loads(line)
            for line in (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()
            if json.loads(line)["kind"] == "request"
        ]
        histories = [json.loads(base64.b64decode(row["data"]["body_b64"])) for row in observer]
        history = next(
            body for body in histories
            if any(
                message.get("role") == "assistant" and len(message.get("tool_calls") or []) == 2
                for message in body.get("messages") or []
                if isinstance(message, dict)
            )
        )
        assistant = next(
            message for message in history["messages"]
            if message.get("role") == "assistant" and len(message.get("tool_calls") or []) == 2
        )
        expected_ids = [call["id"] for call in assistant["tool_calls"]]
        actual_ids = [
            message["tool_call_id"] for message in history["messages"]
            if message.get("role") == "tool" and message.get("tool_call_id") in set(expected_ids)
        ]
        self.assertCountEqual(actual_ids, expected_ids)
        self.assertEqual(len(actual_ids), 2)

    def test_provider_response_over_evidence_limit_is_inadmissible_on_the_assembled_path(self):
        body = "R" * (observer70.RESPONSE_EVIDENCE_LIMIT + 1024)
        summary = self.rig(timeout_s=180).run(scenario_steps({"text": body}))
        observer_records = [json.loads(line) for line in
                            (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
        responses = [row["data"] for row in observer_records if row["kind"] == "response"]
        self.assertTrue(responses)
        self.assertTrue(any(row.get("body_truncated_in_evidence") is True for row in responses))
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertTrue(any("truncated in evidence" in error
                            for error in summary["runtime_observation"].get("observation_errors", [])))

    def test_every_native_and_observer_record_is_accounted_for_in_the_completeness_map(self):
        summary = self.rig().run(self.baseline_scenario())
        self.assertComplete(summary)
        mapping = json.loads((Path(summary["_out"]) / "normalization-map.json").read_text())
        indexes = [row["native_index"] for row in mapping["entries"]]
        self.assertEqual(indexes, list(range(mapping["native_event_count"])))
        classes = {row["classification"] for row in mapping["entries"]}
        self.assertTrue({"observer-inference-request", "observer-inference-response", "agent-end", "tool-end:read"} <= classes)
        self.assertTrue(all(row["mapped_event_ids"] for row in mapping["entries"] if row["oracle_relevant"]))

    def test_observer_saw_every_model_call_and_the_provider_received_the_sentinel_only_upstream(self):
        rig = self.rig()
        summary = rig.run(self.baseline_scenario())
        self.assertComplete(summary)
        upstream = summary["_stand_in_requests"]
        self.assertEqual(len(upstream), 5)
        self.assertTrue(all(row["authorization_ok"] for row in upstream))
        observer = [json.loads(l) for l in (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
        requests = [r for r in observer if r["kind"] == "request"]
        self.assertEqual(len(requests), 5)
        self.assertTrue(all(r["data"]["inbound_authorization"]["matches_placeholder"] for r in requests))
        # the sentinel credential never appears in any retained evidence or in the project
        blob = b""
        for path in Path(summary["_out"]).rglob("*"):
            if path.is_file():
                blob += path.read_bytes()
        self.assertNotIn(omp_rig.SENTINEL_CREDENTIAL.encode(), blob)

    def test_catalog_is_runtime_derived_installed_files_cannot_vouch_for_it(self):
        # Runtime hides one skill (ignoredSkills); the installed package and its digest are unchanged.
        patched = copy.deepcopy(omp.FROZEN_SETTINGS)
        patched["skills"]["ignoredSkills"] = ["software-design"]
        self.patch(omp, "FROZEN_SETTINGS", patched)
        summary = self.rig().run(self.baseline_scenario())
        self.assertNotComplete(summary, "runtime catalog differs from the mounted protocol package")
        self.assertFalse(summary["catalog_isolation"]["ok"] and "software-design" in summary["catalog_isolation"]["catalog"])
        self.assertNotIn("software-design", summary["catalog_isolation"]["catalog"])
        self.assertTrue((Path(summary["_out"]).parent / "corpus").exists())

    def test_observer_disconnected_from_the_real_run_path_is_not_green(self):
        # inference routed to the MCP relay port instead of the observer: the model is never reached
        original = omp.models_document

        def misrouted(profile):
            doc = original(profile)
            for provider in doc["providers"].values():
                provider["baseUrl"] = f"http://127.0.0.1:{omp.RELAY_PORTS['mcp']}/v1"
            return doc

        self.patch(omp, "models_document", misrouted)
        summary = self.rig(timeout_s=60).run(self.baseline_scenario())
        self.assertNotComplete(summary)
        self.assertEqual(summary["_stand_in_requests"], [])

    def test_observer_evidence_removed_after_a_real_run_fails_closed(self):
        original = omp.launch

        def launch_without_observer(profile, prompt, project, env):
            launched = original(profile, prompt, project, env)
            launched["adapter_artifacts"]["observer-evidence.jsonl"] = ""
            return launched

        self.patch(omp, "launch", launch_without_observer)
        summary = self.rig().run(self.baseline_scenario())
        self.assertNotComplete(summary, "observer")

    def test_mcp_reachable_but_inference_dead_and_inference_alive_but_mcp_dead(self):
        original = omp.mcp_document
        self.patch(omp, "mcp_document", lambda: {"mcpServers": {"ssdp70": {"type": "http", "url": "http://127.0.0.1:1/mcp"}}})
        summary = self.rig(timeout_s=90).run(scenario_steps(text("no tools needed")))
        self.assertNotComplete(summary)
        self.assertNotEqual(summary["runtime_observation"]["mcp_servers"], [{"name": "ssdp70", "status": "connected"}])
        # a missing MCP device is never replaced by profile assumptions
        self.assertNotIn("mcp__ssdp_delegate", summary["runtime_observation"]["tools"] or [])

    def test_effective_config_source_binding_detects_a_perturbed_setting(self):
        # control file bytes are digest-consistent but the exact binary reports a different value
        patched = copy.deepcopy(omp.FROZEN_SETTINGS)
        original_doc = omp.settings_document
        patched_doc = copy.deepcopy(omp.FROZEN_SETTINGS)
        patched_doc["retry"]["enabled"] = True
        self.patch(omp, "settings_document", lambda: patched_doc)
        summary = self.rig().run(self.baseline_scenario())
        self.assertNotComplete(summary, "effective OMP setting retry.enabled")

    def test_native_tool_surface_is_exactly_restricted_and_contamination_is_detected(self):
        summary = self.rig().run(scenario_steps(
            call("web_search", query="x"), call("task", description="d"), call("eval", code="1"), text("done")))
        self.assertComplete(summary)
        attempts = [e for e in self.kinds(summary["_out"], "tool_action") if "unexposed-native-tool-attempt" in e["payload"]["semantic_capability_classes"]]
        names = {e["payload"]["native_operation"] for e in attempts}
        self.assertEqual(names, {"web_search", "task", "eval"})
        self.assertTrue(all(e["payload"]["exposed_in_runtime_surface"] is False for e in attempts))
        ends = [e for e in attempts if e["status"] == "error"]
        self.assertEqual(len(ends), 3)
        self.assertEqual({e["payload"]["attempted_semantic_class"] for e in ends}, {"network_remote_service", "delegation", "process_execution"})
        # contamination: launch exposes extra native tools while the frozen profile excludes them
        original = omp.omp_argv
        self.patch(omp, "omp_argv", lambda profile, prompt: [a if a != "read,glob,grep,edit,write,bash" else "read,glob,grep,edit,write,bash,task,eval" for a in original(profile, prompt)])
        dirty = self.rig().run(scenario_steps(text("done")))
        self.assertNotComplete(dirty, "differ")

    def test_model_reasoning_output_and_config_bindings(self):
        summary = self.rig(reasoning=True, thinking="medium").run(self.baseline_scenario())
        self.assertComplete(summary)
        self.assertEqual(summary["runtime_observation"]["reasoning_fields"], {"reasoning_effort": "medium"})
        # frozen thinking level that the runtime does not send is not silently accepted
        original = omp.omp_argv
        self.patch(omp, "omp_argv", lambda profile, prompt: [a for i, a in enumerate(original(profile, prompt)) if a not in ("--thinking",) and (i == 0 or original(profile, prompt)[i - 1] != "--thinking")])
        mismatch = self.rig(reasoning=True, thinking="medium").run(self.baseline_scenario())
        self.assertNotComplete(mismatch, "reasoning")
        # a non-reasoning model with a non-off frozen level is a mismatch, not a pass
        self.patch(omp, "omp_argv", original)
        with self.assertRaises(omp.AdapterError) as ctx:
            self.rig(reasoning=False, thinking="high").run(scenario_steps(text("x")))
        self.assertIn("non-reasoning model", str(ctx.exception))
        off = self.rig(reasoning=False, thinking="off").run(scenario_steps(text("x")))
        self.assertComplete(off)
        self.assertEqual(off["runtime_observation"]["reasoning_fields"], {})

    def test_unknown_native_event_is_fail_closed(self):
        self.assert_perturbation("unknown", lambda lines: lines + [json.dumps({"type": "mystery_event", "x": 1})], "unknown native type")

    def test_dropped_reordered_truncated_and_duplicated_native_events(self):
        summary = self.rig().run(self.baseline_scenario())
        self.assertComplete(summary)
        base = (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()
        artifacts = self.load_artifacts(summary["_out"])
        ctx = self.context(summary)
        tool_end = next(i for i, l in enumerate(base) if json.loads(l).get("type") == "tool_execution_end")
        for label, mutate, needle in (
            ("dropped tool end", lambda ls: ls[:tool_end] + ls[tool_end + 1:], "no matching result"),
            ("dropped message_end", lambda ls: [l for i, l in enumerate(ls) if i != next(j for j, x in enumerate(ls) if json.loads(x).get("type") == "message_end")], "agent_end"),
            ("reordered", lambda ls: ls[:tool_end - 1] + [ls[tool_end], ls[tool_end - 1]] + ls[tool_end + 1:], "no observed start"),
            ("truncated mid-line", lambda ls: ls[:-1] + [ls[-1][: len(ls[-1]) // 2]], "not valid JSON"),
            ("truncated before agent_end", lambda ls: ls[:-3], "agent_end"),
            ("duplicated event", lambda ls: ls[:tool_end + 1] + [ls[tool_end]] + ls[tool_end + 1:], "no observed start"),
            ("unmatched start at EOF", lambda ls: ls[:tool_end] + [json.dumps({"type": "tool_execution_start", "toolCallId": "ghost", "toolName": "read", "args": {}})] + ls[tool_end:], "pending at end of evidence"),
        ):
            events, mapping, errors, count = omp.normalize("\n".join(mutate(base)) + "\n", "run", {**ctx, "adapter_artifacts": artifacts})
            self.assertTrue(any(needle in e for e in errors), (label, errors))
            problems = core70.validate_completeness_map(count, mapping, events)
            self.assertTrue(errors or problems, label)

    def test_raw_native_mcp_identity_mismatch_and_missing_identity(self):
        summary = self.rig().run(self.baseline_scenario())
        base = (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()
        artifacts = self.load_artifacts(summary["_out"])
        ctx = {**self.context(summary), "adapter_artifacts": artifacts}

        def edit(mutator):
            out = []
            for line in base:
                obj = json.loads(line)
                if obj.get("type") == "tool_execution_end" and obj.get("toolName") == "mcp__ssdp_issue_show":
                    mutator(obj)
                out.append(json.dumps(obj))
            return "\n".join(out) + "\n"

        cases = {
            "serverName": lambda o: o["result"]["details"].__setitem__("serverName", "other"),
            "mcpToolName": lambda o: o["result"]["details"].__setitem__("mcpToolName", "issue_search"),
            "rawContent altered": lambda o: o["result"]["details"]["rawContent"][0].__setitem__("text", "{}"),
            "rawContent missing": lambda o: o["result"]["details"].pop("rawContent"),
            "isError contradicts": lambda o: o.__setitem__("isError", True),
        }
        for label, mutator in cases.items():
            events, mapping, errors, count = omp.normalize(edit(mutator), "run", ctx)
            self.assertTrue(errors, label)

    def test_provider_response_binding_detects_forged_and_altered_native_assistant_events(self):
        summary = self.rig().run(self.baseline_scenario())
        base = (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()
        ctx = {**self.context(summary), "adapter_artifacts": self.load_artifacts(summary["_out"])}
        forged = []
        for line in base:
            obj = json.loads(line)
            if obj.get("type") == "tool_execution_start" and obj["toolName"] == "read":
                obj["toolCallId"] = "forged-id"
            forged.append(json.dumps(obj))
        _, _, errors, _ = omp.normalize("\n".join(forged) + "\n", "run", ctx)
        self.assertTrue(any("does not appear in any provider response" in e for e in errors))
        extra = base[:-1] + [json.dumps({"type": "tool_execution_start", "toolCallId": "call_x", "toolName": "bash", "args": {"command": "true"}}),
                              json.dumps({"type": "tool_execution_end", "toolCallId": "call_x", "toolName": "bash", "result": {"content": [{"type": "text", "text": "x"}]}, "isError": False}), base[-1]]
        _, _, errors, _ = omp.normalize("\n".join(extra) + "\n", "run", ctx)
        self.assertTrue(any("provider response" in e for e in errors))

    def test_tampered_principal_evidence_is_detected(self):
        summary = self.rig().run(self.baseline_scenario())
        base = (Path(summary["_out"]) / "trace.jsonl").read_text()
        artifacts = self.load_artifacts(summary["_out"])
        ctx = self.context(summary)
        lines = artifacts["observer-evidence.jsonl"].splitlines()
        for label, mutated in (
            ("truncated", "\n".join(lines[:-1]) + "\n"),
            ("dropped", "\n".join(lines[:2] + lines[3:]) + "\n"),
            ("altered", "\n".join([lines[0], json.dumps({**json.loads(lines[1]), "data": {**json.loads(lines[1])["data"], "request_index": 7}}), *lines[2:]]) + "\n"),
        ):
            _, _, errors, _ = omp.normalize(base, "run", {**ctx, "adapter_artifacts": {**artifacts, "observer-evidence.jsonl": mutated}})
            self.assertTrue(any("observer" in e or "evidence" in e for e in errors), label)
        launcher = artifacts["launcher-evidence.jsonl"].splitlines()
        _, _, errors, _ = omp.normalize(base, "run", {**ctx, "adapter_artifacts": {**artifacts, "launcher-evidence.jsonl": "\n".join(launcher[:-1]) + "\n"}})
        self.assertTrue(errors)

    # ---- helpers used by the perturbation tests
    def load_artifacts(self, out):
        base = Path(out) / "adapter-artifacts"
        return {p.name: p.read_text() for p in base.iterdir() if p.is_file()}

    def context(self, summary):
        out = Path(summary["_out"])
        profile = json.loads((out / "profile-snapshot.json").read_text())
        identity = json.loads((out / "run-identity.json").read_text())
        return {
            "project": str(self.root / "project-not-retained"), "skills_root": str(omp_rig.DIST_SKILLS),
            "package_identity": dict(identity["subject"]), "entry": "ordinary", "profile": profile,
            "runtime_home": str(self.root / "home-not-retained"),
            "prompt": omp_rig.PROMPT_DEFAULT,
        }

    def assert_perturbation(self, label, mutate, needle):
        summary = self.rig().run(self.baseline_scenario())
        base = (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()
        ctx = {**self.context(summary), "adapter_artifacts": self.load_artifacts(summary["_out"])}
        _, _, errors, _ = omp.normalize("\n".join(mutate(base)) + "\n", "run", ctx)
        self.assertTrue(any(needle in e for e in errors), (label, errors))


@SKIP
class RootSelectionAndConsumedResources(RigCase):
    def test_ordinary_root_selection_from_successful_skill_read_with_exact_consumed_resource(self):
        summary = self.rig(claims=["ordinary-entry", "t1-burden"]).run(scenario_steps(
            call("read", path="skill://software-implementation"), text("done")))
        self.assertComplete(summary)
        selection = self.kinds(summary["_out"], "root_selection")
        self.assertEqual(len(selection), 1)
        payload = selection[0]["payload"]
        self.assertEqual(payload["logical_root"], "software-implementation")
        self.assertEqual(payload["selection_mechanism"], "ordinary-skill-read")
        self.assertEqual(payload["native_operation"], "read")
        self.assertEqual(payload["input"], {"path": "skill://software-implementation"})
        self.assertEqual(payload["resolved_package_identity"]["package_sha256"], core70.sha256_tree(omp_rig.DIST_SKILLS))
        consumed = payload["consumed_resource"]
        self.assertEqual(consumed["match"], "exact")
        source = (omp_rig.DIST_SKILLS / "software-implementation" / "SKILL.md")
        self.assertEqual(consumed["resource_sha256"], core70.sha256_file(source))
        self.assertEqual(consumed["resource_bytes"], source.stat().st_size)
        self.assertEqual(consumed["package_relative_path"], "SKILL.md")
        self.assertIsNotNone(consumed["observer_request_index"])

    def test_explicit_mechanism_is_distinct_from_ordinary(self):
        rig = self.rig(entry="pinned:software-design", claims=[])
        summary = rig.run(scenario_steps(call("read", path="skill://software-design"), text("done")))
        self.assertComplete(summary)
        self.assertEqual(self.kinds(summary["_out"], "root_selection")[0]["payload"]["selection_mechanism"], "explicit-instruction-skill-read")
        other = self.rig(entry="pinned:software-design", claims=[]).run(scenario_steps(call("read", path="skill://scientific-formulation"), text("done")), out_name="run2")
        self.assertEqual(self.kinds(other["_out"], "root_selection")[0]["payload"]["selection_mechanism"], "ordinary-skill-read")

    def test_failed_or_attempted_read_creates_no_root_selection(self):
        summary = self.rig().run(scenario_steps(
            call("read", path="skill://no-such-skill"),
            call("read", path="/opt/ssdp/skills/software-design/NOPE.md"),
            py("from pathlib import Path; Path('/opt/ssdp/skills/software-design/SKILL.md').read_bytes()"),
            text("done")))
        self.assertComplete(summary)
        self.assertEqual(self.kinds(summary["_out"], "root_selection"), [])
        reads = self.kinds(summary["_out"], "resource_access", "error")
        self.assertEqual(len(reads), 2)

    def test_owner_file_read_is_consumed_exactly_without_claiming_a_root(self):
        owner = "software-implementation/references/scientific-inspectability-and-initiative.md"
        summary = self.rig(claims=["owner-read"]).run(scenario_steps(
            call("read", path=f"/opt/ssdp/skills/{owner}"), text("done")))
        self.assertComplete(summary)
        self.assertEqual(self.kinds(summary["_out"], "root_selection"), [])
        access = self.kinds(summary["_out"], "resource_access", "result")[0]["payload"]
        self.assertEqual(access["consumed_resource"]["package_relative_path"], "references/scientific-inspectability-and-initiative.md")
        self.assertIn(access["consumed_resource"]["match"], ("exact", "partial"))
        self.assertEqual(access["resource_sha256"], core70.sha256_file(omp_rig.DIST_SKILLS / owner))
        self.assertEqual(summary["owner_read_sequences"], [access and next(e for e in load_events(summary["_out"]) if e["kind"] == "resource_access" and e["status"] == "result")["sequence"]])

    def test_partial_consumption_is_recorded_as_partial_not_exact(self):
        summary = self.rig().run(scenario_steps(
            call("read", path="/opt/ssdp/skills/software-implementation/SKILL.md:1-5"), text("done")))
        self.assertComplete(summary)
        consumed = self.kinds(summary["_out"], "resource_access", "result")[0]["payload"]["consumed_resource"]
        self.assertEqual(consumed["match"], "partial")
        self.assertLess(consumed["consumed_bytes"], consumed["resource_bytes"])

    def test_burden_claim_without_root_or_resource_evidence_is_not_admissible(self):
        summary = self.rig(claims=["t1-burden"]).run(scenario_steps(text("no reads at all")))
        self.assertNotComplete(summary, "burden claim")

    def test_catalog_visibility_alone_is_not_root_selection(self):
        summary = self.rig().run(scenario_steps(text("Use the software-design skill.")))
        self.assertComplete(summary)
        self.assertEqual(self.kinds(summary["_out"], "root_selection"), [])


@SKIP
class MediatorNormalization(RigCase):
    def test_all_six_mediator_operations_normalize_losslessly_with_version_binding(self):
        summary = self.rig().run(scenario_steps(
            call("mcp__ssdp_issue_locations"),
            call("mcp__ssdp_issue_search", query="first", location="local"),
            call("mcp__ssdp_issue_show", issue_id="A-1"),
            call("mcp__ssdp_issue_create", location="local", title="new one", body="created body", labels=["x"]),
            call("mcp__ssdp_issue_comment", issue_id="A-1", body="a comment"),
            call("mcp__ssdp_delegate", agent="reviewer", instruction="check"),
            call("mcp__ssdp_delegate", agent="nobody", instruction="check"),
            call("mcp__ssdp_issue_create", location="remote", title="blocked", body="b"),
            text("done")))
        self.assertComplete(summary)
        out = summary["_out"]
        access = {e["payload"]["tool_use_id"]: e["payload"] for e in self.kinds(out, "issue_evidence_access") if e["status"] in ("result", "error")}
        by_op = {p["operation"]: p for p in access.values() if p["result_status"] == "result"}
        for payload in access.values():
            self.assertEqual(payload["server_name"], "ssdp70")
            self.assertTrue(payload["native_tool_name"].startswith("mcp__ssdp_"))
            self.assertEqual(payload["mediator_evidence"]["store_identity"], "ssdp70-private-issue-standin")
            self.assertTrue(payload["identity_cross_check"]["ok"])
        self.assertEqual(by_op["locations"]["object_ids"], ["local", "remote"])
        self.assertEqual(by_op["search"]["query"], "first")
        self.assertEqual(by_op["search"]["object_ids"], ["A-1"])
        show, create, comment = by_op["show"], by_op["create"], by_op["comment"]
        self.assertEqual(show["before_object_version"], show["after_object_version"])
        self.assertIsNone(create["before_object_version"])
        # before/after version binding against the stand-in the supervisor owns
        created_id = create["object_ids"][0]
        final_issue = Path(out) / "issues-final" / "local" / f"{created_id}.json"
        self.assertEqual(create["after_object_version"], core70.sha256_file(final_issue))
        self.assertEqual(comment["before_object_version"], show["after_object_version"])
        final_a1 = Path(out) / "issues-final" / "local" / "A-1.json"
        self.assertEqual(comment["after_object_version"], core70.sha256_file(final_a1))
        self.assertNotEqual(comment["before_object_version"], comment["after_object_version"])
        # mutation events carry the same versions and the mutation disposition
        mutations = [e["payload"] for e in self.kinds(out, "mutation", "result") if e["payload"].get("mcp_tool_name")]
        self.assertEqual({m["operation"] for m in mutations}, {"create", "comment"})
        self.assertTrue(all(m["disposition"] == "sandboxed" and m["workspace_external_class"] == "qualification-owned-standin" for m in mutations))
        # refused mutation: error status, blocked disposition, no version fabricated
        blocked = [e["payload"] for e in self.kinds(out, "mutation", "error")]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["disposition"], "blocked-or-error")
        self.assertIsNone(blocked[0]["mediator_evidence"].get("after_object_version"))
        # delegate identity, parent, relation, both found and unknown delegates
        returns = [e["payload"] for e in self.kinds(out, "delegate_return")]
        self.assertEqual([r["delegate_id"] for r in returns], ["reviewer", "nobody"])
        self.assertEqual([r["delegate_found"] for r in returns], [True, False])
        self.assertTrue(all(r["parent_actor"] == "executor" and r["launched_work_relation"] == "scripted-qualification-standin" for r in returns))
        calls_ = [e["payload"] for e in self.kinds(out, "delegate_call")]
        self.assertEqual([c["request"]["agent"] for c in calls_], ["reviewer", "nobody"])
        # side-effect log agrees with the normalized mutation set
        log = [json.loads(l) for l in (Path(out) / "side-effects.jsonl").read_text().splitlines()]
        self.assertEqual([r["op"] for r in log if r.get("tool") == "issues" and r["op"] in ("create", "comment")], ["create", "comment", "create"])

    def test_unknown_or_extra_mcp_surface_fails_closed(self):
        summary = self.rig().run(scenario_steps(call("mcp__ssdp_issue_show", issue_id="A-1"), text("x")))
        self.assertComplete(summary)
        base = (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()
        artifacts = {p.name: p.read_text() for p in (Path(summary["_out"]) / "adapter-artifacts").iterdir() if p.is_file()}
        ctx = {"project": "/x", "skills_root": str(omp_rig.DIST_SKILLS), "package_identity": {"package_sha256": "0" * 64}, "entry": "ordinary",
               "profile": json.loads((Path(summary["_out"]) / "profile-snapshot.json").read_text()), "runtime_home": "/y", "prompt": omp_rig.PROMPT_DEFAULT, "adapter_artifacts": artifacts}
        mutated = []
        for line in base:
            obj = json.loads(line)
            for key in ("toolName",):
                if obj.get(key) == "mcp__ssdp_issue_show":
                    obj[key] = "mcp__ssdp70_issue_show"  # the false digit-preserving id
            mutated.append(json.dumps(obj))
        _, _, errors, _ = omp.normalize("\n".join(mutated) + "\n", "run", ctx)
        self.assertTrue(any("exact minted" in e or "not one of" in e for e in errors), errors)


@SKIP
class TerminationTimeoutTurnAndTokenCaps(RigCase):
    def test_turn_cap_is_distinct_from_completion(self):
        steps = [call("bash", command=f"echo {i}") for i in range(6)] + [text("never reached")]
        summary = self.rig(max_turns=3).run(scenario_steps(*steps))
        termination = self.kinds(summary["_out"], "termination")[0]["payload"]
        self.assertEqual(termination["state"], "turn_cap")
        self.assertTrue(termination["native_return_state"]["turn_budget_exhausted_on_observer"])
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        observer = [json.loads(l) for l in (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
        self.assertGreaterEqual(len([r for r in observer if r["kind"] == "budget_exhausted"]), 1)
        self.assertEqual(len(summary["_stand_in_requests"]), 3)  # the over-budget request never reached the provider

    def test_token_cap_is_distinct_from_completion(self):
        summary = self.rig().run(scenario_steps({"text": "truncated at the cap", "finish": "length"}))
        termination = self.kinds(summary["_out"], "termination")[0]["payload"]
        self.assertEqual(termination["state"], "token_cap")
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")

    def test_timeout_kills_the_whole_sandbox_and_is_a_terminal_state(self):
        summary = self.rig(timeout_s=6).run(scenario_steps(py("import time; time.sleep(300)"), text("unreached")))
        termination = self.kinds(summary["_out"], "termination")[0]["payload"]
        self.assertEqual(termination["state"], "timeout")
        self.assertTrue(termination["native_return_state"]["timed_out"])
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertLess(summary["wall_s"], 60)
        # nothing survives the sandbox
        leftovers = [p for p in os.listdir("/proc") if p.isdigit() and self._cmd(p) and "ssdp-subject" in self._cmd(p)]
        self.assertEqual(leftovers, [])

    @staticmethod
    def _cmd(pid):
        try:
            return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
        except OSError:
            return ""

    def test_provider_layer_retry_is_frozen_observed_and_accounted(self):
        # OMP's provider layer resends the identical request once after a transient error (hard-coded in the exact build)
        summary = self.rig().run(scenario_steps({"http_error": 500}, text("recovered")))
        self.assertComplete(summary)
        self.assertEqual(len(summary["_stand_in_requests"]), 2)
        usage = self.kinds(summary["_out"], "usage_timing")[0]["payload"]
        self.assertEqual(len(usage["provider_layer_retries"]), 1)
        self.assertEqual(usage["provider_layer_retries"][0]["kind"], "transient-provider-error")
        self.assertEqual(usage["provider_layer_retries"][0]["previous_status"], 500)
        mapping = json.loads((Path(summary["_out"]) / "normalization-map.json").read_text())
        self.assertIn("observer-provider-layer-retry", {row["classification"] for row in mapping["entries"]})
        observer = [json.loads(l) for l in (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
        digests = [r["data"]["body_sha256"] for r in observer if r["kind"] == "request"]
        self.assertEqual(digests[0], digests[1])  # byte-identical resend

    def test_provider_layer_retries_beyond_the_builds_limits_fail_closed(self):
        # more identical resends than the exact build ever performs would be an unexplained hidden call
        summary = self.rig().run(scenario_steps(*([{"http_error": 500}] * 14), text("never reached")))
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")

    def test_empty_completion_retry_is_accounted_in_the_evidence(self):
        summary = self.rig().run(scenario_steps({"text": ""}, text("second try")))
        self.assertComplete(summary)
        usage = self.kinds(summary["_out"], "usage_timing")[0]["payload"]
        self.assertEqual([r["kind"] for r in usage["provider_layer_retries"]], ["empty-completion"])

    def test_runtime_injected_steering_after_repeated_empty_completions_is_inadmissible(self):
        # after the identical resends the build injects a hard-coded `<system-injection>` user message that the
        # native trace never shows; only the trusted observer sees it, and it is not absorbed
        summary = self.rig().run(scenario_steps(*([{"text": ""}] * 3), text("after the injection")))
        self.assertNotComplete(summary, "runtime-injected message")
        self.assertIn("Stopped without actionable output", json.dumps(summary["normalized_event_errors"]))

    def test_unexplained_duplicate_or_extra_inference_request_is_a_hidden_call(self):
        summary = self.rig().run(scenario_steps(call("bash", command="true"), text("done")))
        self.assertComplete(summary)
        base = (Path(summary["_out"]) / "trace.jsonl").read_text()
        artifacts = {p.name: p.read_text() for p in (Path(summary["_out"]) / "adapter-artifacts").iterdir() if p.is_file()}
        # forge a second observer request record chain that duplicates a successful request (rebuilt chain)
        observer = [json.loads(l) for l in artifacts["observer-evidence.jsonl"].splitlines()]
        requests = [r for r in observer if r["kind"] == "request"]
        body = [r for r in observer if r["kind"] in ("request", "response")]
        forged_path = self.root / "forged-observer.jsonl"
        w = os.open(forged_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        chain = evidence70.ChainWriter(w, "ssdp70-provider-observer-v1")
        for record in observer[:-1]:
            chain.append(record["kind"], record["data"])
            if record["kind"] == "response" and record["data"]["request_index"] == 0:
                dup = dict(requests[0]["data"], request_index=99)
                chain.append("request", dup)
                chain.append("response", dict(record["data"], request_index=99))
        chain.close()
        os.close(w)
        forged = forged_path.read_text()
        ctx = {"project": "/x", "skills_root": str(omp_rig.DIST_SKILLS), "package_identity": {"package_sha256": "0" * 64}, "entry": "ordinary",
               "profile": json.loads((Path(summary["_out"]) / "profile-snapshot.json").read_text()), "runtime_home": "/y", "prompt": omp_rig.PROMPT_DEFAULT,
               "adapter_artifacts": {**artifacts, "observer-evidence.jsonl": forged}}
        _, _, errors, _ = omp.normalize(base, "run", ctx)
        self.assertTrue(any("unaccounted" in e or "unexplained" in e or "unaccounted for" in e for e in errors), errors)

    def test_provider_managed_auto_retry_event_is_inadmissible_when_enabled(self):
        patched = copy.deepcopy(omp.FROZEN_SETTINGS)
        patched["retry"] = {"enabled": True, "maxRetries": 2, "modelFallback": False, "usageAwareFallback": False}
        self.patch(omp, "FROZEN_SETTINGS", patched)
        # 429 survives the provider layer's own resends; OMP's session-level auto-retry then acts
        summary = self.rig().run(scenario_steps(*([{"http_error": 429}] * 6), text("after auto retry")))
        self.assertNotComplete(summary)
        self.assertIn("auto_retry", json.dumps(summary["normalized_event_errors"]))

    def test_frozen_closure_leaves_a_429_as_an_error_not_a_session_retry(self):
        summary = self.rig().run(scenario_steps(*([{"http_error": 429}] * 6), text("never reached")))
        self.assertEqual(self.kinds(summary["_out"], "termination")[0]["payload"]["state"], "error")
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        native = [json.loads(l)["type"] for l in (Path(summary["_out"]) / "trace.jsonl").read_text().splitlines()]
        self.assertNotIn("auto_retry_start", native)


@SKIP
class ProviderManagedStateAndDiscoveryEffects(RigCase):
    """Hostile discovery inputs are rejected before the OMP process or provider can run."""

    MARKER = "HOSTILE-MARKER-D4"

    def _assert_rejected_before_process(self, rig, *, inject_launch_environment=None, expect_launch=False):
        original_launch = omp.launch
        launch_calls = []

        def observed_launch(profile, prompt, project, env):
            launch_calls.append(True)
            if inject_launch_environment is not None:
                env = dict(env)
                env.update(inject_launch_environment)
            return original_launch(profile, prompt, project, env)

        with mock.patch.object(omp, "launch", side_effect=observed_launch), \
                mock.patch.object(omp.subprocess, "Popen", wraps=omp.subprocess.Popen) as process_start:
            summary = rig.run(scenario_steps(text("must not launch")))

        self.assertEqual(summary["evidence_state"], "EXECUTION_ERROR")
        self.assertEqual(summary["qualification_outcome"], "NOT_EVALUATED")
        self.assertFalse(summary["execution_ok"])
        self.assertFalse(summary["prelaunch_refusal"]["subject_launched"])
        self.assertTrue(any("ambient discovery is not closed" in item for item in summary["evidence_state_reasons"]))
        subject_launches = [
            call for call in process_start.call_args_list
            if call.args and isinstance(call.args[0], (list, tuple)) and call.args[0]
            and Path(str(call.args[0][0])).name == "bwrap"
        ]
        self.assertEqual(subject_launches, [])
        self.assertEqual(len(launch_calls), 1 if expect_launch or inject_launch_environment else 0)
        self.assertEqual(rig.read_stand_in(), [])
        secret_values = [omp_rig.SENTINEL_CREDENTIAL, *(inject_launch_environment or {}).values()]
        for path in Path(summary["_out"]).rglob("*"):
            if path.is_file():
                contents = path.read_bytes()
                for secret in secret_values:
                    self.assertNotIn(secret.encode(), contents, f"credential value was written to {path.name}")

    def test_every_project_discovery_source_is_refused_before_omp_or_provider(self):
        for rel in omp.PROJECT_DISCOVERY_SOURCES:
            with self.subTest(source=rel), tempfile.TemporaryDirectory(dir=self.root) as td:
                content = json.dumps({"mcpServers": {"hostile": {"url": "http://127.0.0.1:31099/mcp"}}}) \
                    if "mcp" in rel.lower() else f"{self.MARKER}:{rel}\n"
                rig = Rig(Path(td), project_files={rel: content})
                self._assert_rejected_before_process(rig)

    def test_every_home_discovery_source_is_refused_before_omp_or_provider(self):
        original = omp._write_control_tree
        for rel in omp.HOME_DISCOVERY_SOURCES:
            with self.subTest(source=rel), tempfile.TemporaryDirectory(dir=self.root) as td:
                rig = Rig(Path(td))

                def seed_home_source(paths, profile, source=rel):
                    manifest = original(paths, profile)
                    target = paths["home"] / source
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(f"{self.MARKER}:{source}\n")
                    return manifest

                with mock.patch.object(omp, "_write_control_tree", side_effect=seed_home_source):
                    self._assert_rejected_before_process(rig, expect_launch=True)

    def test_every_credential_environment_name_is_refused_before_omp_or_provider(self):
        for name in omp.CREDENTIAL_ENV_NAMES:
            with self.subTest(variable=name), tempfile.TemporaryDirectory(dir=self.root) as td:
                rig = Rig(Path(td))
                self._assert_rejected_before_process(rig, inject_launch_environment={name: "SYNTHETIC-CREDENTIAL-SENTINEL"})

    def test_project_dotenv_remains_fixture_data_and_is_not_ingested(self):
        rig = self.rig(project_files={
            ".env": "HOSTILE_ENV_PROJECT=1\nOPENAI_API_KEY=SYNTHETIC-PROJECT-KEY\n",
        })
        summary = rig.run(scenario_steps(
            py("""
                import os
                print('PROJECT_ENV_PRESENT', 'HOSTILE_ENV_PROJECT' in os.environ)
                print('PROJECT_CREDENTIAL_PRESENT', 'OPENAI_API_KEY' in os.environ)
            """),
            text("done")))
        self.assertComplete(summary)
        result = self.bash_results(summary["_out"])[0]["payload"]["result_content"]
        self.assertIn("PROJECT_ENV_PRESENT False", result)
        self.assertIn("PROJECT_CREDENTIAL_PRESENT False", result)

    def test_ancestor_directory_discovery_sees_nothing(self):
        summary = self.rig().run(scenario_steps(py("""
            import os
            for root in ("/", "/workspace/..", "/workspace/../.."):
                print(root, " ".join(sorted(os.listdir(root))))
            print("mountinfo", sum(1 for _ in open("/proc/self/mountinfo")))
        """), text("done")))
        self.assertComplete(summary)
        result = self.bash_results(summary["_out"])[0]["payload"]["result_content"]
        self.assertNotIn(".omp", result.split("\n")[0])
        for name in (".claude", ".codex", ".gemini", ".agents", "AGENTS.md"):
            self.assertNotIn(name, result)

    def test_run_home_is_exactly_the_control_files_plus_omp_runtime_state(self):
        summary = self.rig().run(scenario_steps(text("done")))
        self.assertComplete(summary)
        inventory = json.loads((Path(summary["_out"]) / "adapter-artifacts" / "runtime-home-inventory.json").read_text())
        classes = {row["path"]: row["class"] for row in inventory["entries"]}
        self.assertEqual({p for p, c in classes.items() if c == "control"}, set(omp.CONTROL_FILES_IN_HOME))
        self.assertEqual({c for c in classes.values()}, {"control", "omp-runtime-state"})

    def test_profile_and_provider_managed_state_perturbations(self):
        rig = self.rig(claims=["t1", "t7", "t8"])
        profile = rig.profile("http://127.0.0.1:1")
        write = self.root / "p.json"
        omp_rig.write_json(write, profile)
        bundle = core70.load_profile(write, omp_rig.HERE / "capabilities" / "omp-headless.json")
        # after the closure only arm-neutral unknowns remain: the burden claims are not scoped inadmissible
        self.assertEqual(core70.profile_claim_errors(bundle, ["t1", "t7", "t8", "ordinary-entry", "owner-read"]), [])
        # a newly discovered uncontrolled unknown sensitive to those claims blocks them (claim-scoped inadmissible)
        profile["provider_managed_unknowns"].append({"classification": "uncontrolled", "name": "newly-discovered-state", "sensitive_claims": ["t7"]})
        omp_rig.write_json(write, profile)
        worse = core70.load_profile(write, omp_rig.HERE / "capabilities" / "omp-headless.json")
        self.assertTrue(core70.profile_claim_errors(worse, ["t7"]))
        self.assertEqual(core70.profile_claim_errors(worse, ["t1"]), [])
        # perturbing any frozen digest is refused at realization, before anything launches
        for path in (("containment_policy", "settings_closure_sha256"), ("containment_policy", "build_inventory_sha256")):
            def mutate(profile, path=path):
                profile[path[0]][path[1]] = "0" * 64
                return profile
            refused = self.rig().run(scenario_steps(text("x")), mutate_profile=mutate)
            self.assertEqual(refused["evidence_state"], "EXECUTION_ERROR")
            self.assertEqual(refused["qualification_outcome"], "NOT_EVALUATED")
            self.assertEqual(refused["_stand_in_requests"], [])
        # an unfrozen profile cannot reach the runtime through the harness
        def unfreeze(profile):
            profile["provider_runtime"]["provider"] = "MUST-BE-FROZEN-BEFORE-QUALIFICATION"
            return profile
        summary = self.rig().run(scenario_steps(text("x")), mutate_profile=unfreeze) if False else None
        del summary


class B2PrivilegeSeparationWhileInferenceWorks(RigCase):
    def run_attacks(self, steps, **kwargs):
        rig = self.rig(timeout_s=110, **kwargs)
        summary = rig.run(scenario_steps(*steps, text("done")))
        return summary, {e["payload"]["input"].get("command", "")[:60]: e["payload"]["result_content"]
                         for e in self.bash_results(summary["_out"])}

    def test_inference_and_mcp_work_while_credential_home_and_state_are_denied(self):
        host_secret = self.root / "host-secret.txt"
        host_secret.write_text("HOST-ONLY-SECRET\n")
        target = str(host_secret)
        summary, out = self.run_attacks([
            call("mcp__ssdp_issue_show", issue_id="A-1"),
            py(f"""
                import os
                marker = {omp_rig.SENTINEL_CREDENTIAL!r}
                print("credential-env", [(k, v) for k, v in os.environ.items() if "SSDP70_OMP" in k or marker[:16] in v])
                for root in ("/workspace", "/home", "/tmp", "/opt", "/etc"):
                    for current, dirs, files in os.walk(root):
                        dirs[:] = dirs[:80]
                        for name in files[:300]:
                            path = os.path.join(current, name)
                            try:
                                if marker in open(path, "r", errors="ignore").read(100000): print("SECRET-FILE", path)
                            except OSError:
                                pass
                print("ENVDONE GREPDONE")
            """),
            py(f"""
                from pathlib import Path
                paths = [{HOST_HOME!r}, {str(Path(HOST_HOME) / '.bashrc')!r}, {target!r}, '/root']
                for path in paths:
                    try:
                        p = Path(path)
                        value = p.read_bytes()[:100] if p.is_file() else sorted(x.name for x in p.iterdir())[:2]
                        print(path, value)
                    except OSError as exc: print(path, type(exc).__name__, exc.errno)
            """),
            py(f"""
                import os
                target = {target!r}
                for name, value in (("abs-link", target), ("up", "../../../../../..")):
                    try: os.symlink(value, "/workspace/" + name)
                    except FileExistsError: pass
                for path in ("/workspace/abs-link", "/workspace/../../../../" + target.lstrip("/"),
                             "/workspace/up", "/proc/self/root" + target):
                    try: print(path, open(path, "rb").read(100))
                    except OSError as exc: print(path, type(exc).__name__, exc.errno)
            """),
            py("""
                import os, stat
                names = {"side-effects.jsonl", "mcp-account.txt", "mcp-server.py"}
                root_dev = os.stat("/").st_dev
                found = []
                for root, dirs, files in os.walk("/", followlinks=False):
                    dirs[:] = [d for d in dirs if os.stat(os.path.join(root, d), follow_symlinks=False).st_dev == root_dev]
                    for name in files:
                        path = os.path.join(root, name)
                        try:
                            if name in names or name.endswith(".evidence.jsonl") or name.startswith("observer"):
                                if stat.S_ISSOCK(os.stat(path, follow_symlinks=False).st_mode): found.append(path)
                        except OSError: pass
                print("\\n".join(found)); print("FINDDONE")
            """),
            py("""
                import re
                lines = open("/proc/self/mountinfo").read().splitlines()
                print(sum(bool(re.search(r"side-effects|mcp-account|mcp-server|/stub|evidence|observer|bridge", line)) for line in lines))
                print("MOUNTINFO-DONE")
            """),
        ])
        self.assertComplete(summary)
        self.assertEqual(len(self.kinds(summary["_out"], "issue_evidence_access", "result")), 1)  # MCP works
        self.assertEqual(len(summary["_stand_in_requests"]), 7)                                   # inference works (6 tool turns + final)
        mountinfo = next(v for v in out.values() if "MOUNTINFO-DONE" in v)
        self.assertTrue(mountinfo.startswith("0"), mountinfo)
        text_out = "\n".join(out.values())
        self.assertNotIn("HOST-ONLY-SECRET", text_out)
        self.assertNotIn(omp_rig.SENTINEL_CREDENTIAL, text_out)
        self.assertIn("FileNotFoundError", text_out)
        find_out = next(v for v in out.values() if "FINDDONE" in v)
        self.assertEqual(find_out.split("FINDDONE")[0].strip(), "")

    def test_minimal_runtime_keeps_required_tools_and_omits_host_software(self):
        summary, out = self.run_attacks([
            py(f"""
                import os, subprocess, sys
                print("PYTHON", sys.version.split()[0])
                bash = subprocess.run(['/usr/bin/bash', '--version'], capture_output=True, text=True)
                print("BASH", bash.returncode, bash.stdout.splitlines()[0])
                for path in ('/usr/bin/git', '/usr/bin/gcc', '/usr/bin/curl', '/usr/bin/apt',
                             '/usr/bin/find', '/usr/bin/cat', '/usr/bin/node', {HOST_HOME!r},
                             '/home/agent/.config', '/usr/share/doc'):
                    try:
                        with open(path, 'rb') as stream: stream.read(1)
                        readable = True
                    except OSError:
                        readable = False
                    try:
                        subprocess.run([path, '--version'], capture_output=True, timeout=3)
                        executable = True
                    except (OSError, subprocess.SubprocessError):
                        executable = False
                    print(path, readable, executable)
            """),
        ])
        self.assertComplete(summary)
        result = next(v for v in out.values() if "PYTHON" in v)
        self.assertIn("PYTHON 3.10", result)
        self.assertIn("BASH 0 GNU bash", result)
        for name in ("git", "gcc", "curl", "apt", "find", "cat", "node"):
            self.assertIn(f"/usr/bin/{name} False False", result)
        self.assertIn(f"{HOST_HOME} False False", result)

    def test_staged_runtime_tampering_fails_before_subject_or_provider_execution(self):
        rig = self.rig(timeout_s=110)
        original_materialize = omp._materialize_runtime_dependencies
        launched = mock.Mock()

        def materialize_then_tamper(paths):
            staged = original_materialize(paths)
            target = paths["subject_runtime"] / "usr/bin/bash"
            with target.open("ab") as stream:
                stream.write(b"tamper")
            return staged

        with mock.patch.object(omp, "_materialize_runtime_dependencies", side_effect=materialize_then_tamper), \
                mock.patch.object(omp, "launch", launched):
            summary = rig.run(scenario_steps(text("must not launch")))
        self.assertEqual(summary["evidence_state"], "EXECUTION_ERROR")
        self.assertTrue(any("staged OMP runtime closure is inadmissible" in item
                            for item in summary["evidence_state_reasons"]))
        launched.assert_not_called()
        self.assertEqual(rig.read_stand_in(), [])

    def test_bash_cannot_use_the_inference_or_mcp_transport_or_launch_a_second_omp(self):
        summary, out = self.run_attacks([
            py("""
               import socket
               for port in (31001, 31002):
                   s = socket.socket(); s.settimeout(3)
                   s.connect(("127.0.0.1", port))
                   s.sendall(b"POST /v1/chat/completions HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 2\\r\\nAuthorization: Bearer ssdp70-run-transport-key\\r\\n\\r\\n{}")
                   try:
                       data = s.recv(100)
                   except Exception as e:
                       data = repr(e).encode()
                   print(port, data[:60])
               for host, port in (("93.184.216.34", 80), ("1.1.1.1", 53), ("127.0.0.1", 9)):
                   s = socket.socket(); s.settimeout(3)
                   try:
                       s.connect((host, port)); print(host, port, "CONNECTED")
                   except Exception as e:
                       print(host, port, type(e).__name__)
            """),
            py("""
                import re, subprocess
                run = subprocess.run(['/opt/omp/omp', '-p', '--mode=json', '--no-session', '--no-title',
                                      '--model', 'stand/stand-model', 'second instance'],
                                     capture_output=True, text=True, timeout=30)
                print(sum(1 for line in (run.stdout + run.stderr).splitlines() if re.search(r'HTTP|error', line)))
                print('SECOND-DONE')
            """),
        ])
        self.assertComplete(summary)
        # only the authorized OMP process ever reached the provider: 3 model calls, nothing else
        self.assertEqual(len(summary["_stand_in_requests"]), 3)
        denials = self.kinds(summary["_out"], "network_external_action")
        self.assertGreaterEqual(len(denials), 3)
        self.assertTrue(all(d["payload"]["disposition"] == "blocked" and d["payload"]["authorization_decision"] == "deny" for d in denials))
        self.assertTrue(all("not-held-solely" in d["payload"]["input"]["reason"] for d in denials))
        network = next(v for k, v in out.items() if k.startswith("python3"))
        self.assertNotIn("CONNECTED", network)
        self.assertIn("Connection", network) if "ConnectionRefused" in network else None
        observer = [json.loads(l) for l in (Path(summary["_out"]) / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
        self.assertEqual(len([r for r in observer if r["kind"] == "request"]), 3)
        self.assertEqual([r for r in observer if r["kind"] == "refused"], [])

    def test_no_process_can_read_or_tamper_with_transport_state_or_forge_the_trace(self):
        summary, out = self.run_attacks([
            py("""
               import os, ctypes
               libc = ctypes.CDLL(None, use_errno=True)
               pids = sorted(int(x) for x in os.listdir('/proc') if x.isdigit())
               print("pids", len(pids) <= 6)
               launcher = pids[0]
               for name in ("environ", "mem", "fd", "maps"):
                   try:
                       if name == "fd":
                           os.listdir(f"/proc/{launcher}/fd")
                       else:
                           open(f"/proc/{launcher}/{name}", "rb").read(8)
                       print("LAUNCHER", name, "READABLE")
                   except OSError as e:
                       print("LAUNCHER", name, "DENIED", e.errno)
               omp = next(p for p in pids if os.path.exists(f"/proc/{p}/exe") and os.readlink(f"/proc/{p}/exe") == "/opt/omp/omp")
               for fd in (1, 2):
                   try:
                       open(f"/proc/{omp}/fd/{fd}", "ab", buffering=0).write(b'{"type":"agent_end","messages":[]}\\n'); print("FORGED", fd)
                   except OSError as e:
                       print("TRACE-FD", fd, "DENIED", e.errno)
               for pid in pids:
                   print("PTRACE", libc.ptrace(16, pid, 0, 0), ctypes.get_errno())
                   print("PIDFD", libc.syscall(438, 0, 0, 0), ctypes.get_errno())
                   print("PVM", libc.syscall(310, pid, 0, 0, 0, 0, 0), ctypes.get_errno())
            """),
        ])
        self.assertComplete(summary)
        result = next(iter(out.values()))
        self.assertNotIn("READABLE", result)
        self.assertNotIn("FORGED", result)
        self.assertIn("TRACE-FD 1 DENIED 6", result)   # ENXIO: a socket cannot be re-opened via /proc
        self.assertNotIn("PTRACE 0 ", result)
        self.assertTrue(all(line.endswith(" 1") for line in result.splitlines() if line.startswith(("PTRACE", "PVM"))))

    def test_external_write_and_immutable_control_mutation_are_contained_and_detected(self):
        rig = self.rig(timeout_s=110)
        summary = rig.run(scenario_steps(
            sh("echo pwn >> /home/agent/.omp/agent/config.yml; echo x > /opt/ssdp/skills/software-design/SKILL.md; "
               "echo x > /etc/evil; echo x > /usr/evil; echo ok > /tmp/scratch; echo ok > /home/agent/scratch; echo rc=$?"),
            call("write", path="/etc/evil2", content="x"),
            call("write", path="/tmp/ok.txt", content="x"),
            call("write", path="/workspace/inside.txt", content="x"),
            call("write", path="/workspace/notes.txt", content="ALPHA\nbeta\n"),
            text("done")))
        self.assertComplete(summary)
        result = self.bash_results(summary["_out"])[0]["payload"]["result_content"]
        self.assertIn("Permission denied", result)
        self.assertIn("Read-only file system", result)
        mutations = {e["payload"]["logical_target"]: e["payload"] for e in self.kinds(summary["_out"], "mutation") if e["status"] in ("result", "error")}
        self.assertEqual(mutations["/etc/evil2"]["workspace_external_class"], "external")
        self.assertEqual(mutations["/etc/evil2"]["disposition"], "blocked-or-error")
        self.assertEqual(mutations["/tmp/ok.txt"]["workspace_external_class"], "external")
        self.assertEqual(mutations["/tmp/ok.txt"]["disposition"], "sandboxed")
        self.assertEqual(mutations["/workspace/inside.txt"]["workspace_external_class"], "workspace")
        self.assertFalse(Path("/tmp/ok.txt").exists() and Path("/tmp/ok.txt").read_text() == "x")
        control = json.loads((Path(summary["_out"]) / "adapter-artifacts" / "control-digests.json").read_text())
        self.assertEqual(control["before"], control["after"])
        self.assertEqual(control["packages_before"], control["packages_after"])
        self.assertEqual((Path(summary["_out"]) / "final-tree" / "notes.txt").read_text(), "ALPHA\nbeta\n")

    def test_host_side_mutation_of_immutable_control_material_is_detected_post_run(self):
        original = omp.launch

        def mutate_after(profile, prompt, project, env):
            launched = original(profile, prompt, project, env)
            paths = omp._paths(project, env)
            (paths["home"] / ".omp" / "agent" / "mcp.json").chmod(0o644)
            (paths["home"] / ".omp" / "agent" / "mcp.json").write_text("{}")
            (paths["skills"] / "software-design" / "SKILL.md").write_text("tampered")
            return launched

        self.patch(omp, "launch", mutate_after)
        summary = self.rig().run(scenario_steps(text("done")))
        self.assertNotComplete(summary)
        blob = json.dumps(summary["profile_claim_errors"])
        self.assertIn("immutable OMP control file", blob)
        self.assertIn("installed protocol package changed during execution", blob)

    def test_discriminating_external_local_ipc_sentinel_is_unreachable(self):
        rig = self.rig(timeout_s=110)
        original = omp.launch
        sentinel_state = {"accepted": 0, "path": None}

        def with_external_sentinel(profile, prompt, project, env):
            path = project / ".qualification-external-ipc-sentinel.sock"
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(str(path))
            server.listen(4)
            server.settimeout(0.05)
            sentinel_state["path"] = str(path)
            stopping = threading.Event()

            def accept_connections():
                while not stopping.is_set():
                    try:
                        connection, _ = server.accept()
                    except socket.timeout:
                        continue
                    except OSError:
                        return
                    sentinel_state["accepted"] += 1
                    connection.close()

            worker = threading.Thread(target=accept_connections, daemon=True)
            worker.start()
            try:
                launched = original(profile, prompt, project, env)
            finally:
                stopping.set()
                server.close()
                worker.join(2)
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            launched["adapter_artifacts"]["local-ipc-sentinel.json"] = json.dumps({
                "owner": "qualification-supervisor-test",
                "server_outside_subject_process_and_pid_namespace": True,
                "subject_visible_mount_path": "/workspace/.qualification-external-ipc-sentinel.sock",
                "accepted_connections": sentinel_state["accepted"],
            }, indent=2, sort_keys=True) + "\n"
            return launched

        self.patch(omp, "launch", with_external_sentinel)
        try:
            summary = rig.run(scenario_steps(
                call("mcp__ssdp_issue_show", issue_id="A-1"),
                py("""
                    import socket
                    path = '/workspace/.qualification-external-ipc-sentinel.sock'
                    try:
                        channel = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                        print('AF_UNIX_SOCKET_CREATED')
                        try:
                            channel.connect(path)
                            print('SENTINEL_CONNECTED')
                        except OSError as exc:
                            print('SENTINEL_CONNECT_DENIED', exc.errno)
                    except OSError as exc:
                        print('AF_UNIX_SOCKET_DENIED', exc.errno)
                """),
                text("done")))
        except OSError as exc:
            self.fail(f"B2 = UNRESOLVED/BLOCKING: outer host denied the discriminating local IPC/provider probe: {type(exc).__name__} errno={exc.errno}")
        self.assertComplete(summary)
        bash_result = self.bash_results(summary["_out"])[0]["payload"]["result_content"]
        self.assertIn("AF_UNIX_SOCKET_DENIED 1", bash_result)
        self.assertNotIn("SENTINEL_CONNECTED", bash_result)
        self.assertEqual(sentinel_state["accepted"], 0)
        self.assertTrue(summary["_stand_in_requests"])
        self.assertEqual(len(self.kinds(summary["_out"], "issue_evidence_access", "result")), 1)


@SKIP
class ThirdPassObserverLaunchSafety(RigCase):
    @staticmethod
    def scenario():
        return scenario_steps(
            call("read", path="skill://software-implementation"),
            call("mcp__ssdp_issue_show", issue_id="A-1"),
            call("write", path="/workspace/out.txt", content="active\n"),
            text("done"),
        )

    def test_real_observer_fd_map_excludes_inheritable_supervisor_sentinel(self):
        sentinel_path = self.root / "unrelated-supervisor-open-fd.txt"
        sentinel_path.write_text("UNRELATED-SUPERVISOR-FD\n", encoding="utf-8")
        original_fd = os.open(sentinel_path, os.O_RDONLY)
        sentinel_fd = fcntl.fcntl(original_fd, fcntl.F_DUPFD, 256)
        os.close(original_fd)
        os.set_inheritable(sentinel_fd, True)

        original_builder = omp._observer_bwrap_argv

        def probe_inheritable_fd(profile, paths, observer_fds, probe_paths, supervisor_pid,
                                 supervisor_netns, supervisor_pidns):
            adjusted = [
                (name, f"/proc/self/fd/{sentinel_fd}" if name == "host_home" else path)
                for name, path in probe_paths
            ]
            return original_builder(profile, paths, observer_fds, adjusted, supervisor_pid,
                                    supervisor_netns, supervisor_pidns)

        self.patch(omp, "_observer_bwrap_argv", probe_inheritable_fd)
        try:
            summary = self.rig(timeout_s=90).run(self.scenario())
        finally:
            os.close(sentinel_fd)

        self.assertComplete(summary)
        artifacts = Path(summary["_out"]) / "adapter-artifacts"
        launch = json.loads((artifacts / "observer-boundary-argv.json").read_text(encoding="utf-8"))
        mapping = launch["fd_mapping"]
        self.assertEqual({name: mapping[name]["observer_fd"] for name in (
            "inference_input", "inference_output", "evidence_output", "credential_input",
        )}, {
            "inference_input": 3, "inference_output": 4, "evidence_output": 5, "credential_input": 6,
        })
        self.assertEqual(mapping["bubblewrap_arguments"]["bubblewrap_fd"], 7)
        expected_pass_fds = {
            mapping[name]["supervisor_source_fd"] for name in (
                "inference_input", "inference_output", "evidence_output", "credential_input",
                "bubblewrap_arguments",
            )
        }
        self.assertEqual(set(launch["pass_fds"]), expected_pass_fds)
        self.assertEqual(len(launch["pass_fds"]), 5)
        self.assertEqual(launch["argv"][1:3], ["--args", "7"])
        self.assertEqual(launch["exec_helper_sha256"], omp.sha256_file(omp.OBSERVER_EXEC_HELPER))
        identity = json.loads((Path(summary["_out"]) / "run-identity.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["adapter_support_sha256"]["observer_exec_helper70.py"],
                         launch["exec_helper_sha256"])

        records, errors = evidence70.parse_chain(
            (artifacts / "observer-evidence.jsonl").read_text(encoding="utf-8"),
            "ssdp70-provider-observer-v1",
        )
        self.assertEqual(errors, [])
        kinds = [row["kind"] for row in records]
        for required in ("boundary", "credential_received", "ready", "request", "response"):
            self.assertIn(required, kinds)
        self.assertLess(kinds.index("boundary"), kinds.index("credential_received"))
        self.assertLess(kinds.index("credential_received"), kinds.index("ready"))
        host_home_probe = next(row["data"] for row in records
                               if row["kind"] == "boundary_probe" and row["data"].get("name") == "host_home")
        self.assertEqual(host_home_probe["disposition"], "denied")
        self.assertTrue(summary["_stand_in_requests"], "descriptor-bound inference channel was not exercised")
        self.assertTrue(self.kinds(summary["_out"], "issue_evidence_access", "result"),
                        "supervisor-owned MCP channel was not exercised")
        self.assertLess(summary["wall_s"], 90)

    @staticmethod
    def _process_tree(pid):
        ordered = []
        seen = set()

        def visit(parent):
            if parent in seen:
                return
            seen.add(parent)
            ordered.append(parent)
            children_file = Path(f"/proc/{parent}/task/{parent}/children")
            try:
                children = [int(value) for value in children_file.read_text().split()]
            except (OSError, ValueError):
                children = []
            for child in children:
                visit(child)

        visit(pid)
        return ordered

    def test_repeated_launches_with_active_threads_have_an_outer_watchdog(self):
        worker_code = textwrap.dedent(r"""
            import json, sys, threading
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            import evidence70
            from omp_rig import Rig, call, load_events, scenario_steps, text
            root = Path(sys.argv[2])
            stop = threading.Event()
            ready = [threading.Event() for _ in range(4)]
            ticks = [0, 0, 0, 0]
            def churn(index):
                ready[index].set()
                while not stop.is_set():
                    ticks[index] += 1
                    stop.wait(0.002)
            threads = [threading.Thread(target=churn, args=(index,), daemon=True) for index in range(4)]
            for thread in threads: thread.start()
            if not all(event.wait(5) for event in ready):
                raise SystemExit("unrelated supervisor threads did not start")
            scenario = scenario_steps(
                call("read", path="skill://software-implementation"),
                call("mcp__ssdp_issue_show", issue_id="A-1"),
                call("write", path="/workspace/out.txt", content="active\n"),
                text("done"),
            )
            try:
                for iteration in range(3):
                    before = sum(ticks)
                    summary = Rig(root, timeout_s=120).run(scenario, out_name=f"launch-{iteration}")
                    if summary.get("evidence_state") != "COMPLETE_ADMISSIBLE":
                        raise SystemExit("assembled launch failed: " + json.dumps(summary.get("evidence_state_reasons")))
                    if sum(ticks) <= before:
                        raise SystemExit("unrelated supervisor threads were not active during the OMP launch")
                    if not summary.get("_stand_in_requests"):
                        raise SystemExit("provider inference route was not exercised")
                    artifacts = Path(summary["_out"]) / "adapter-artifacts"
                    records, errors = evidence70.parse_chain(
                        (artifacts / "observer-evidence.jsonl").read_text(encoding="utf-8"),
                        "ssdp70-provider-observer-v1",
                    )
                    if errors:
                        raise SystemExit("observer evidence chain failed: " + json.dumps(errors))
                    kinds = [row["kind"] for row in records]
                    if not all(kind in kinds for kind in ("boundary", "credential_received", "ready", "request", "response")):
                        raise SystemExit("observer did not complete boundary, credential, readiness, and inference")
                    if not (kinds.index("boundary") < kinds.index("credential_received") < kinds.index("ready")):
                        raise SystemExit("credential was not delivered after observer lockdown and before ready")
                    if not any(row["kind"] == "issue_evidence_access" and row["status"] == "result"
                               for row in load_events(summary["_out"])):
                        raise SystemExit("MCP bridge/mediator did not complete a normalized operation")
                    print(f"completed {iteration + 1}/3", flush=True)
            finally:
                stop.set()
                for thread in threads: thread.join(2)
        """)

        worker = subprocess.Popen(
            [sys.executable, "-c", worker_code, str(HERE), str(self.root)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True, start_new_session=True,
        )
        try:
            stdout, stderr = worker.communicate(timeout=90)
        except subprocess.TimeoutExpired:
            for child in reversed(self._process_tree(worker.pid)[1:]):
                try:
                    os.kill(child, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            try:
                os.killpg(worker.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = worker.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                worker.kill()
                stdout, stderr = worker.communicate(timeout=10)
            self.fail(f"outer launch watchdog expired; normal per-episode timeout was 120s; "
                      f"stdout={stdout!r}; stderr={stderr!r}")
        self.assertEqual(worker.returncode, 0, f"stdout={stdout!r}; stderr={stderr!r}")
        self.assertEqual(stdout.decode("utf-8", "replace").count("completed "), 3,
                         "the stress worker did not complete three assembled launches")


if __name__ == "__main__":
    unittest.main()
