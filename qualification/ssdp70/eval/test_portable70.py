import json
import tempfile
import unittest
from pathlib import Path

import core70
from adapters import claude


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


class PortableCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = self.root / "profile.json"
        self.capabilities = self.root / "capabilities.json"
        write_json(self.capabilities, {
            "schema": 1,
            "capabilities": {
                name: {"decision": "ALLOW" if name not in {"delegation", "network_remote_service"} else "DENY", "scope": "*"}
                for name in core70.REQUIRED_CAPABILITY_CLASSES
            },
            "native_capabilities": {
                "tool:Read": {"semantic_classes": ["workspace_read_search_list"], "scope": "test read"}
            },
        })
        write_json(self.profile, {
            "schema": 1,
            "profile_id": "test-profile",
            "adapter_id": claude.ADAPTER_ID,
            "agent_model": "test-model",
            "provider_runtime": {"provider": "test", "runtime": "claude-code", "executable": "claude", "version": "exposed-v1"},
            "reasoning_configuration": {"effort": "high"},
            "workspace_realization": {"kind": "tempdir"},
            "install_mechanism": "project-skills",
            "budgets": {"max_turns": 60, "timeout_s": 3600},
            "containment_policy": {"kind": "external-pre-effect"},
            "network_external_write_policy": {"network": "deny", "external_write": "sandbox"},
            "credential_service_account_policy": {"ambient_credentials": "deny"},
            "provider_managed_unknowns": [
                {"name": "backend-shard", "classification": "arm-neutral", "sensitive_claims": ["*"]}
            ],
            "native_tools": ["Read"],
            "native_surface_requirements": [],
            "mcp_servers": [],
        })

    def tearDown(self):
        self.tmp.cleanup()

    def requirements(self):
        req = self.root / "req"
        req.mkdir(exist_ok=True)
        write_json(req / "required_artifacts.json", {"schema": 1, "episodes": {"E1": ["final-report.md", "trace.jsonl"]}})
        write_json(req / "required_oracles.json", {"schema": 1, "episodes": {"E1": [{"id": "o1", "path": "check_o1.py"}]}})
        write_json(req / "expected_scoring_items.json", {"schema": 1, "episodes": {"E1": [
            {"id": "i1", "measure": "critical-judgment", "critical": True, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]},
            {"id": "i2", "measure": "null-coverage", "critical": False, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved", "not-applicable"]},
        ]}})
        return core70.load_requirements(req, "E1")

    def write_admission(self, role="executor", omit=None):
        bundle = core70.load_profile(self.profile, self.capabilities)
        root = self.root / f"{role}-admission"
        evidence = root / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        names = core70.EXECUTOR_ADMISSION_CHECKS if role == "executor" else core70.EVALUATOR_ADMISSION_CHECKS
        checks = {}
        for name in names:
            if name == omit:
                continue
            artifact = evidence / f"{name}.json"
            artifact.write_text(json.dumps({"check": name, "pass": True}), encoding="utf-8")
            checks[name] = {
                "status": "PASS",
                "evidence_path": f"evidence/{name}.json",
                "evidence_sha256": core70.sha256_file(artifact),
            }
        admission = root / "admission.json"
        write_json(admission, {
            "schema": 1,
            "status": "ADMITTED",
            "role": role,
            "profile_key_sha256": bundle.profile_key_sha256,
            "adapter_sha256": "adapter-a",
            "core_sha256": "core-a",
            "capability_manifest_sha256": bundle.capability_manifest_sha256,
            "checks": checks,
        })
        return admission, bundle

    def test_profile_key_changes_with_material_capability_change(self):
        a = core70.load_profile(self.profile, self.capabilities)
        caps = json.loads(self.capabilities.read_text())
        caps["capabilities"]["process_execution"]["decision"] = "DENY"
        write_json(self.capabilities, caps)
        b = core70.load_profile(self.profile, self.capabilities)
        self.assertNotEqual(a.profile_key_sha256, b.profile_key_sha256)

    def test_uncontrolled_provider_unknown_fails_sensitive_claim(self):
        profile = json.loads(self.profile.read_text())
        profile["provider_managed_unknowns"] = [
            {"name": "hidden-system-prompt", "classification": "uncontrolled", "sensitive_claims": ["owner-read"]}
        ]
        write_json(self.profile, profile)
        bundle = core70.load_profile(self.profile, self.capabilities)
        self.assertTrue(core70.profile_claim_errors(bundle, ["owner-read"]))
        self.assertFalse(core70.profile_claim_errors(bundle, ["timing"]))

    def test_admission_requires_exact_check_set_and_hashed_evidence(self):
        admission, bundle = self.write_admission()
        self.assertEqual(core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        ), [])
        incomplete, bundle = self.write_admission(omit=core70.EXECUTOR_ADMISSION_CHECKS[-1])
        errors = core70.validate_profile_admission(
            incomplete, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("missing required checks" in error for error in errors))

    def test_admission_rejects_tampered_proof_artifact(self):
        admission, bundle = self.write_admission()
        proof = admission.parent / "evidence" / f"{core70.EXECUTOR_ADMISSION_CHECKS[0]}.json"
        proof.write_text("tampered", encoding="utf-8")
        errors = core70.validate_profile_admission(
            admission, mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256="adapter-a", core_sha256="core-a",
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor",
        )
        self.assertTrue(any("hash does not match" in error for error in errors))

    def test_admission_snapshot_preserves_and_validates_all_proofs(self):
        admission, _ = self.write_admission()
        out = self.root / "run-admission"
        out.mkdir()
        bundle_sha = core70.admission_bundle_sha256(admission, role="executor")
        core70.snapshot_profile_admission(admission, out, role="executor")
        self.assertEqual(core70.validate_profile_admission_snapshot(
            out, bundle_sha, role="executor"), [])
        proof = out / "profile-admission-evidence" / f"{core70.EXECUTOR_ADMISSION_CHECKS[0]}.proof"
        proof.write_text("tampered", encoding="utf-8")
        self.assertTrue(core70.validate_profile_admission_snapshot(
            out, bundle_sha, role="executor"))

    def test_runtime_observation_rejects_unfrozen_or_mismatched_runtime(self):
        bundle = core70.load_profile(self.profile, self.capabilities)
        self.assertEqual(core70.validate_runtime_observation(
            bundle, {"model": "test-model", "runtime_version": "exposed-v1", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}), [])
        self.assertTrue(core70.validate_runtime_observation(
            bundle, {"model": "test-model", "runtime_version": "other", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}))
        profile = json.loads(self.profile.read_text())
        profile["provider_runtime"]["version"] = "MUST-BE-FROZEN-BEFORE-QUALIFICATION"
        write_json(self.profile, profile)
        frozen = core70.load_profile(self.profile, self.capabilities)
        self.assertTrue(core70.validate_runtime_observation(
            frozen, {"model": "test-model", "runtime_version": "x", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}))

    def test_scoring_exact_closure_rejects_empty_and_duplicates(self):
        req = self.requirements()
        self.assertTrue(core70.validate_dispositions([], req))
        valid = [
            {"item": "i1", "measure": "critical-judgment", "critical": True, "result": "pass"},
            {"item": "i2", "measure": "null-coverage", "critical": False, "result": "not-applicable"},
        ]
        self.assertEqual(core70.validate_dispositions(valid, req), [])
        self.assertTrue(core70.validate_dispositions(valid + [dict(valid[0])], req))

    def test_required_oracle_hashes_are_enforced(self):
        req = self.requirements()
        run = self.root / "run"
        run.mkdir()
        (run / "final-report.md").write_text("x")
        (run / "trace.jsonl").write_text("{}\n")
        (run / "o1.out").write_text("ok")
        (run / "o1.err").write_text("")
        write_json(run / "oracle.json", {"schema": 1, "results": {"o1": {
            "executed": True,
            "stdout_artifact": "o1.out",
            "stderr_artifact": "o1.err",
            "stdout_sha256": core70.sha256_file(run / "o1.out"),
            "stderr_sha256": core70.sha256_file(run / "o1.err"),
        }}})
        self.assertEqual(core70.validate_required_oracles(run, req), [])
        (run / "o1.out").write_text("changed")
        self.assertEqual(core70.validate_required_oracles(run, req), ["o1"])

    def test_requirements_snapshot_is_content_bound(self):
        req = self.requirements()
        snapshot = core70.requirements_snapshot(req)
        parsed = core70.requirements_from_snapshot(snapshot, snapshot["manifest_digests"])
        self.assertEqual(parsed, req)
        snapshot["expected_scoring_items"][0]["measure"] = "tampered"
        with self.assertRaises(core70.ContractError):
            core70.requirements_from_snapshot(snapshot, snapshot["manifest_digests"])

    def test_event_payload_schema_rejects_missing_result_evidence(self):
        event = {
            "schema_version": 1, "run_id": "r", "event_id": "e1", "sequence": 1,
            "actor_id": "executor", "kind": "resource_access",
            "native_source": {"native_index": 0, "native_sha256": "a" * 64},
            "status": "result", "timing": None,
            "payload": {
                "operation": "read", "resource_identity": "/x", "input": {}, "tool_use_id": "t1",
                "result_status": "result", "result_reference": None, "result_sha256": None,
                "resolved_package_identity": None, "resource_sha256": None, "resource_bytes": None,
            },
        }
        errors = core70.validate_normalized_events([event], "r")
        self.assertTrue(any("result_reference" in error for error in errors))

    def test_normalization_completeness_rejects_dropped_event(self):
        events = [{
            "schema_version": 1, "run_id": "r", "event_id": "e000001", "sequence": 1,
            "actor_id": "executor", "kind": "termination",
            "native_source": {"native_index": 1, "native_sha256": "a" * 64},
            "status": "observed", "timing": None,
            "payload": {"state": "completed", "native_return_state": {"is_error": False}, "terminal_result_exists": True},
        }]
        mapping = [{"native_index": 1, "native_sha256": "a" * 64, "mapped_event_ids": ["e000001"], "classification": "terminal", "oracle_relevant": True}]
        errors = core70.validate_completeness_map(2, mapping, events)
        self.assertTrue(any("missing from completeness map" in error for error in errors))


class ClaudeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.skills = self.root / ".claude" / "skills"
        owner = self.skills / "software-implementation" / "references" / "scientific-inspectability-and-initiative.md"
        owner.parent.mkdir(parents=True)
        owner.write_text("owner bytes", encoding="utf-8")
        skill = self.skills / "software-implementation" / "SKILL.md"
        skill.write_text("# root", encoding="utf-8")
        self.context = {
            "project": str(self.root),
            "skills_root": str(self.skills),
            "package_identity": {
                "arm": "p70", "commit": "abc", "version": "7.0.0",
                "package_sha256": "b" * 64,
            },
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_owner_read_has_success_result_and_exact_resource_bytes(self):
        owner = self.skills / "software-implementation" / "references" / "scientific-inspectability-and-initiative.md"
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(owner)}}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "u1", "content": "owner bytes", "is_error": False}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        events, mapping, errors, native_count = claude.normalize(stdout, "run-1", self.context)
        self.assertEqual(errors, [])
        self.assertEqual(core70.validate_normalized_events(events, "run-1"), [])
        self.assertEqual(core70.validate_completeness_map(native_count, mapping, events), [])
        self.assertTrue(claude.owner_reads(events, "scientific-inspectability-and-initiative.md"))
        result = [e for e in events if e["kind"] == "resource_access" and e["status"] == "result"][0]
        self.assertEqual(result["payload"]["resource_bytes"], len(b"owner bytes"))
        self.assertIsNotNone(result["payload"]["resource_sha256"])

    def test_ordinary_entry_root_is_observed_from_skill_read(self):
        skill = self.skills / "software-implementation" / "SKILL.md"
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(skill)}}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "u1", "content": "# root", "is_error": False}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        events, _, errors, _ = claude.normalize(stdout, "run-2", self.context)
        self.assertEqual(errors, [])
        roots = [e for e in events if e["kind"] == "root_selection"]
        self.assertTrue(any(e["payload"]["selection_mechanism"] == "ordinary-resource-read" for e in roots))

    def test_missing_tool_result_is_fail_closed(self):
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": sorted(claude.SSDP_SKILLS), "model": "m", "claude_code_version": "v1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(self.skills / "software-implementation" / "SKILL.md")}}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done", "duration_ms": 1, "usage": {}}),
        ])
        _, _, errors, _ = claude.normalize(stdout, "run-3", self.context)
        self.assertTrue(any("no exposed tool result" in error for error in errors))

    def test_unknown_native_event_type_is_fail_closed(self):
        stdout = json.dumps({"type": "mystery", "payload": {"x": 1}})
        _, mapping, errors, native_count = claude.normalize(stdout, "run-4", self.context)
        self.assertTrue(errors)
        self.assertEqual(native_count, 1)
        self.assertTrue(mapping[0]["oracle_relevant"])


class EvidenceStateTests(unittest.TestCase):
    def test_incomplete_terminal_cannot_be_complete(self):
        state, reasons = core70.run_evidence_state(
            execution_ok=True, profile_errors=[], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=False, final_result_exists=False,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, "MISSING_REQUIRED_EVIDENCE")
        self.assertTrue(reasons)

    def test_execution_transport_success_does_not_override_inadmissible_profile(self):
        state, _ = core70.run_evidence_state(
            execution_ok=True, profile_errors=["uncontrolled hidden state"], event_errors=[], completeness_errors=[],
            catalog_ok=True, terminal_exists=True, final_result_exists=True,
            missing_artifacts=[], missing_oracles=[])
        self.assertEqual(state, "INADMISSIBLE")


if __name__ == "__main__":
    unittest.main()
