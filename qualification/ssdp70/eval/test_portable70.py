import json
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

import core70
import harness70



def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


class ProjectStagingTests(unittest.TestCase):
    def test_history_hard_links_are_refused_before_copy_or_chmod(self):
        for copied_collision in (False, True):
            with self.subTest(copied_collision=copied_collision), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                fixture = root / "corpus/fixtures/frozen"
                source = fixture / "project"
                source.mkdir(parents=True)
                outside = root / "outside.txt"
                outside.write_text("protected\n")
                outside.chmod(0o400)
                if copied_collision:
                    (source / "history-data").write_text("overlay\n")
                (fixture / "build_history.sh").write_text(
                    f'ln "{outside}" history-data\n'
                )
                project = root / "working"
                with self.assertRaisesRegex(core70.ContractError, "hard-linked file: history-data"):
                    harness70.build_project(
                        root / "corpus", {"id": "E1", "fixture": "frozen"}, project, []
                    )
                self.assertEqual(stat.S_IMODE(outside.stat().st_mode), 0o400)
                self.assertEqual(outside.read_text(), "protected\n")
                self.assertFalse((project / ".git").exists())

    def test_history_git_commits_and_restricted_modes_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "corpus/fixtures/frozen"
            source = fixture / "project"
            nested = source / "nested"
            nested.mkdir(parents=True)
            data = nested / "data.txt"
            data.write_text("frozen\n")
            executable = source / "run.sh"
            executable.write_text("#!/bin/sh\nprintf staged\n")
            data.chmod(0o440)
            executable.chmod(0o551)
            nested.chmod(0o550)
            source.chmod(0o550)
            (fixture / "build_history.sh").write_text(
                "git init -q\nprintf history > historical.txt\ngit add historical.txt\n"
                "git -c user.email=eval@example.invalid -c user.name=eval commit -qm history\n"
            )
            project = root / "working"
            try:
                harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, project, [".omp"])
                self.assertEqual(subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=project), b"2\n")
                self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=project), b"")
                self.assertEqual((project / ".git/info/exclude").read_text(), harness70.project_git_exclude([".omp"]))
                self.assertEqual(stat.S_IMODE((project / "nested").stat().st_mode), 0o750)
                self.assertEqual(stat.S_IMODE((project / "nested/data.txt").stat().st_mode), 0o640)
                self.assertEqual(stat.S_IMODE((project / "run.sh").stat().st_mode), 0o751)
                self.assertEqual(subprocess.check_output([str(project / "run.sh")]), b"staged")
                (project / "nested/data.txt").write_text("edited\n")
                self.assertEqual(data.read_text(), "frozen\n")
                self.assertEqual(stat.S_IMODE(data.stat().st_mode), 0o440)
                self.assertEqual(stat.S_IMODE(executable.stat().st_mode), 0o551)
                self.assertEqual(stat.S_IMODE(nested.stat().st_mode), 0o550)
                self.assertEqual(stat.S_IMODE(source.stat().st_mode), 0o550)
            finally:
                source.chmod(0o700)
                nested.chmod(0o700)

    def test_frozen_fixture_becomes_writable_without_changing_custody(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "corpus" / "fixtures" / "frozen" / "project"
            nested = source / "nested"
            nested.mkdir(parents=True)
            data = nested / "data.txt"
            data.write_text("frozen data\n")
            executable = source / "run.sh"
            executable.write_text("#!/bin/sh\nprintf staged\n")
            data.chmod(0o400)
            executable.chmod(0o500)
            nested.chmod(0o500)
            source.chmod(0o500)
            before = {p: (stat.S_IMODE(p.stat().st_mode), p.read_bytes() if p.is_file() else None)
                      for p in (source, nested, data, executable)}
            project = root / "working"
            try:
                harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, project, [])
                self.assertEqual(stat.S_IMODE(project.stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE((project / "nested").stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE((project / "nested/data.txt").stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE((project / "run.sh").stat().st_mode), 0o700)
                self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=project), b"")
                self.assertEqual(subprocess.check_output([str(project / "run.sh")], cwd=project), b"staged")
                (project / "nested/data.txt").write_text("edited\n")
                (project / "nested/new.txt").write_text("created\n")
                self.assertTrue(subprocess.check_output(["git", "diff", "--", "nested/data.txt"], cwd=project))
                for path, expected in before.items():
                    self.assertEqual((stat.S_IMODE(path.stat().st_mode), path.read_bytes() if path.is_file() else None), expected)
            finally:
                # Only the synthetic fixture needs thawing for temporary cleanup.
                source.chmod(0o700)
                nested.chmod(0o700)

    def test_staging_does_not_chmod_history_script_symlink_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "corpus/fixtures/frozen"
            (fixture / "project").mkdir(parents=True)
            outside = root / "outside.txt"
            outside.write_text("protected\n")
            outside.chmod(0o400)
            outside_dir = root / "outside-dir"
            outside_dir.mkdir()
            (outside_dir / "data.txt").write_text("protected\n")
            (outside_dir / "data.txt").chmod(0o400)
            (fixture / "build_history.sh").write_text(
                f'ln -s "{outside}" file-link\nln -s "{outside_dir}" dir-link\n'
            )
            harness70.build_project(root / "corpus", {"id": "E1", "fixture": "frozen"}, root / "working", [])
            self.assertEqual(stat.S_IMODE(outside.stat().st_mode), 0o400)
            self.assertEqual(stat.S_IMODE((outside_dir / "data.txt").stat().st_mode), 0o400)


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
            "adapter_id": "omp-json-v2",
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

    def test_termination_requires_portable_boolean_is_error(self):
        missing_flag = [{
            "schema_version": 1, "run_id": "r", "event_id": "e000001", "sequence": 1,
            "actor_id": "executor", "kind": "termination",
            "native_source": {"native_index": 0, "native_sha256": "a" * 64},
            "status": "observed", "timing": None,
            "payload": {"state": "error", "native_return_state": {"isError": True}, "terminal_result_exists": False},
        }]
        errors = core70.validate_normalized_events(missing_flag, "r")
        self.assertTrue(any("native_return_state.is_error" in error for error in errors), errors)
        self.assertEqual(harness70._termination_state(missing_flag), (True, False))

        success = [{
            "kind": "termination",
            "payload": {"state": "completed", "native_return_state": {"is_error": False}, "terminal_result_exists": True},
        }]
        failure = [{
            "kind": "termination",
            "payload": {"state": "error", "native_return_state": {"is_error": True}, "terminal_result_exists": False},
        }]
        self.assertEqual(harness70._termination_state(success), (True, True))
        self.assertEqual(harness70._termination_state(failure), (True, False))

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
