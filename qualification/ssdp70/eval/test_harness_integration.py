import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import core70
import harness70

SKILLS = ["numerical-algorithm-design", "repository-hygiene", "scientific-formulation", "software-design",
          "software-documentation", "software-implementation", "software-maintenance-audit"]
OWNER_NAME = "scientific-inspectability-and-initiative.md"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


class FakeAdapter:
    ADAPTER_ID = "fake-stream-v1"
    __file__ = __file__

    @staticmethod
    def clean_env():
        return {}

    @staticmethod
    def realize_containment(profile, project, env):
        return {
            "fake": True,
            "realization": {
                "settings_sha256": "a" * 64,
                "mcp_config_sha256": "b" * 64,
                "mcp_servers": [],
                "mcp_server_executable_sha256": {},
            },
        }

    @staticmethod
    def install_skills(dist, project, env=None):
        target = project / ".claude" / "skills"
        target.mkdir(parents=True)
        for name in SKILLS:
            shutil.copytree(dist / name, target / name)
        return target

    @staticmethod
    def project_control_paths(profile):
        return [".claude", ".mcp.json"]

    @staticmethod
    def prepare_prompt(profile, entry, prompt):
        return prompt

    @staticmethod
    def launch(profile, prompt, project, env):
        owner = project / ".claude" / "skills" / "software-implementation" / "references" / "scientific-inspectability-and-initiative.md"
        stdout = "\n".join([
            json.dumps({"type": "system", "subtype": "init", "skills": SKILLS, "model": "fake", "claude_code_version": "1"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "u1", "name": "Read", "input": {"file_path": str(owner)}}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "u1", "content": "owner", "is_error": False}
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "final report", "duration_ms": 1, "usage": {}}),
        ]) + "\n"
        return {
            "returncode": 0, "stdout": stdout, "stderr": "", "wall_s": 0.01,
            "command_identity": {
                "executable": None,
                "model": "fake",
                "reasoning_configuration": {"effort": "fixed"},
                "tools": ["Read"],
                "allowed_tools": None,
                "disallowed_tools": None,
                "settings_file_sha256": "a" * 64,
                "mcp_config_sha256": "b" * 64,
                "mcp_servers": [],
                "mcp_server_executable_sha256": {},
            },
        }

    @staticmethod
    def runtime_observation(stdout):
        return {"model": "fake", "runtime_version": "1", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}

    @staticmethod
    def normalize(stdout, run_id, context):
        lines = [line for line in stdout.splitlines() if line.strip()]
        package = {**{k: context["package_identity"][k] for k in ("commit", "package_sha256")}, "identity_source": "verified-install"}
        owner = str(Path(context["skills_root"]) / "software-implementation" / "references" / OWNER_NAME)
        read = {"input": {"file_path": owner}, "operation": "read", "resolved_package_identity": package, "resolved_resource_path": owner,
                "resource_bytes": 5, "resource_identity": owner, "resource_identity_source": "input-path",
                "resource_sha256": hashlib.sha256(b"owner").hexdigest(), "search_root": None, "tool_use_id": "u1"}
        rows = [
            (0, "catalog_snapshot", "observed", {"logical_skill_ids": SKILLS, "model": "fake", "native_tools": [], "resolved_package_identity": package, "runtime_version": "1"}),
            (1, "resource_access", "start", {**read, "result_reference": None, "result_sha256": None, "result_status": "pending"}),
            (2, "resource_access", "result", {**read, "result_content": "owner", "result_reference": "trace:2:block:0",
                                              "result_sha256": hashlib.sha256(b"owner").hexdigest(), "result_status": "result"}),
            (3, "termination", "observed", {"native_return_state": {"is_error": False}, "state": "success", "terminal_result_exists": True}),
            (3, "final_result", "observed", {"artifact_reference": "final-report.md", "result_text": "final report"}),
            (3, "usage_timing", "observed", {"duration_ms": 1, "duration_unit": "ms", "usage": {}, "usage_source": "provider-result-event"}),
        ]
        events, mapped = [], {}
        for number, (index, kind, status, payload) in enumerate(rows, 1):
            digest = hashlib.sha256(lines[index].encode()).hexdigest()
            events.append({"actor_id": "executor", "event_id": f"e{number:06d}", "kind": kind, "payload": payload, "run_id": run_id,
                           "native_source": {"native_index": index, "native_sha256": digest, "stream": "stdout"},
                           "schema_version": 1, "sequence": number, "status": status, "timing": None})
            mapped.setdefault(index, []).append(f"e{number:06d}")
        kinds = {0: "catalog", 1: "assistant-message", 2: "user-message", 3: "terminal-result"}
        mapping = [{"native_index": i, "native_sha256": hashlib.sha256(lines[i].encode()).hexdigest(), "mapped_event_ids": ids,
                    "classification": kinds[i], "oracle_relevant": True} for i, ids in sorted(mapped.items())]
        return events, mapping, [], len(lines)

    @staticmethod
    def final_result(events):
        return next(e["payload"]["result_text"] for e in events if e["kind"] == "final_result")

    @staticmethod
    def catalog_isolation(events):
        return {"ok": True}

    @staticmethod
    def owner_reads(events, owner_name):
        return [e["sequence"] for e in events if e["kind"] == "resource_access" and e["status"] == "result"
                and e["payload"]["resource_identity"].endswith(owner_name)]


class FakeEvaluator:
    ADAPTER_ID = "fake-evaluator-v1"
    __file__ = __file__

    @staticmethod
    def clean_env():
        return {}

    @staticmethod
    def realize_containment(profile, project, env):
        return {
            "fake": True,
            "realization": {
                "settings_sha256": "a" * 64,
                "mcp_config_sha256": "b" * 64,
                "mcp_servers": [],
                "mcp_server_executable_sha256": {},
            },
        }

    @staticmethod
    def launch(profile, prompt, project, env):
        verdict = {
            "episode": "E1",
            "dispositions": [{
                "item": "i1", "measure": "critical", "result": "pass",
                "critical": True, "evidence": "complete evidence",
            }],
            "notes": "",
        }
        stdout = json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "result": json.dumps(verdict),
        }) + "\n"
        return {
            "returncode": 0, "stdout": stdout, "stderr": "",
            "command_identity": {
                "executable": None,
                "model": "eval",
                "reasoning_configuration": {"effort": "fixed"},
                "tools": ["Read"],
                "settings_file_sha256": "a" * 64,
                "mcp_config_sha256": "b" * 64,
                "mcp_servers": [],
                "mcp_server_executable_sha256": {},
            },
        }

    @staticmethod
    def runtime_observation(stdout):
        return {"model": "eval", "runtime_version": "1", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}


class HarnessIntegration(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.corpus = self.root / "corpus"
        (self.corpus / "fixtures" / "f1" / "project").mkdir(parents=True)
        (self.corpus / "fixtures" / "f1" / "project" / "README.txt").write_text("fixture")
        (self.corpus / "stubs").mkdir()
        (self.corpus / "manifest.yaml").write_text(yaml.safe_dump({"episodes": [{
            "id": "E1", "fixture": "f1", "prompt": "do task", "claims": ["owner-read"]
        }]}))
        self.dist = self.root / "dist"
        for name in SKILLS:
            (self.dist / name / "references").mkdir(parents=True)
            (self.dist / name / "SKILL.md").write_text(f"# {name}\n")
            (self.dist / name / "references" / "scientific-inspectability-and-initiative.md").write_text("owner")
        self.profile_path = self.root / "profile.json"
        self.cap_path = self.root / "cap.json"
        profile = {
            "schema": 1, "profile_id": "fake", "adapter_id": "fake-stream-v1", "agent_model": "fake",
            "provider_runtime": {"provider": "fake", "runtime": "fake", "version": "1"},
            "reasoning_configuration": {"effort": "fixed"}, "workspace_realization": {"kind": "temp"},
            "install_mechanism": "project-skills", "budgets": {"max_turns": 2, "timeout_s": 10},
            "containment_policy": {"kind": "fake-pre-effect"},
            "network_external_write_policy": {"network": "deny", "external_write": "sandbox"},
            "credential_service_account_policy": {"ambient": "deny"}, "provider_managed_unknowns": [],
            "native_tools": ["Read"], "native_surface_requirements": [], "mcp_servers": [],
        }
        write_json(self.profile_path, profile)
        write_json(self.cap_path, {"schema": 1, "capabilities": {
            name: {"decision": "DENY" if name in {"delegation", "network_remote_service"} else "ALLOW", "scope": "*"}
            for name in core70.REQUIRED_CAPABILITY_CLASSES
        }, "native_capabilities": {
            "tool:Read": {"semantic_classes": ["workspace_read_search_list"], "scope": "test read"}
        }})
        self.bundle = core70.load_profile(self.profile_path, self.cap_path)
        self.req_root = self.root / "requirements"
        write_json(self.req_root / "required_artifacts.json", {"schema": 1, "episodes": {"E1": [
            "summary.json", "run-identity.json", "trace.jsonl", "events.normalized.jsonl", "normalization-map.json",
            "final-report.md", "final-tree", "oracle.json", "requirements-snapshot.json"
        ]}})
        write_json(self.req_root / "required_oracles.json", {"schema": 1, "episodes": {"E1": [
            {"id": "o1", "path": "check_o1.py"}
        ]}})
        write_json(self.req_root / "expected_scoring_items.json", {"schema": 1, "episodes": {"E1": [
            {"id": "i1", "measure": "critical", "critical": True, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]}
        ]}})
        self.oracles = self.root / "oracles" / "E1"
        self.oracles.mkdir(parents=True)
        (self.oracles / "check_o1.py").write_text("import sys\nsys.exit(0)\n")
        self.requirements = core70.load_requirements(self.req_root, "E1")
        self.arm = {
            "name": "p70", "requested_ref": "abc", "commit": "abc", "version": "7.0.0",
            "skills_path": str(self.dist), "dist_tree_sha256": core70.sha256_tree(self.dist),
        }
        self.episode = harness70.load_manifest(self.corpus)[0]

    def tearDown(self):
        self.td.cleanup()

    def identity(self):
        return harness70.run_identity(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=FakeAdapter,
            oracles=self.oracles.parent, mode="probe", rep=0, pair_order=["p70"])

    def invoke(self, out):
        return harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe",
            identity=self.identity(), pair_order=["p70"])

    @staticmethod
    def snapshot_realization(root):
        root = Path(root)
        snapshot = {}
        for path in [root, *sorted(root.rglob("*"))]:
            info = path.lstat()
            if path.is_symlink():
                kind, content = "symlink", os.readlink(path)
            elif path.is_file():
                kind, content = "file", path.read_bytes()
            else:
                kind, content = "directory", None
            snapshot[path.relative_to(root).as_posix()] = {
                "kind": kind, "content": content, "mode": info.st_mode & 0o7777,
                "inode": info.st_ino, "mtime_ns": info.st_mtime_ns, "ctime_ns": info.st_ctime_ns,
            }
        return snapshot


    def complete_run(self, name="run-assess"):
        out = self.root / name
        summary = self.invoke(out)
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        return out

    def assert_collision_preserves(self, out):
        before = self.snapshot_realization(out)
        with self.assertRaisesRegex(core70.ContractError, "realization collision"):
            self.invoke(out)
        self.assertEqual(self.snapshot_realization(out), before)

    def test_completed_realization_collision_is_byte_and_metadata_preserving(self):
        out = self.complete_run("completed-collision")
        self.assertTrue((out / "run-identity.json").is_file())
        self.assertTrue((out / "summary.json").is_file())
        self.assert_collision_preserves(out)

    def test_interrupted_partial_realization_collision_is_byte_and_metadata_preserving(self):
        out = self.root / "interrupted-collision"
        out.mkdir()
        (out / "run-identity.json").write_bytes(b'{"schema":2,"interrupted":true')
        (out / "trace.jsonl").write_bytes(b'{"partial":"native event prefix"')
        self.assert_collision_preserves(out)

    def test_terminal_integrity_artifacts_survive_realization_collision(self):
        out = self.root / "terminal-collision"
        out.mkdir()
        (out / "run-identity.json").write_bytes(b'{"identity_sha256":"prior-run"}\n')
        (out / "trace.jsonl").write_bytes(b'{"kind":"termination","complete":true}\n')
        (out / "summary.json").write_bytes(b'{"evidence_state":"COMPLETE_ADMISSIBLE","qualification_outcome":"NOT_EVALUATED"}\n')
        (out / "evidence-integrity.json").write_bytes(b'{"schema":1,"files":[{"path":"trace.jsonl","sha256":"prior"}]}\n')
        self.assert_collision_preserves(out)

    def evaluator_material(self, version="1"):
        profile_path = self.root / f"evaluator-{version}.json"
        capability_path = self.root / f"evaluator-{version}-cap.json"
        profile = {
            "schema": 1, "profile_id": f"eval-{version}", "adapter_id": FakeEvaluator.ADAPTER_ID,
            "agent_model": "eval",
            "provider_runtime": {"provider": "fake", "runtime": "fake", "version": version},
            "reasoning_configuration": {"effort": "fixed"},
            "workspace_realization": {"kind": "temporary-read-only-evidence-bundle"},
            "install_mechanism": "none",
            "budgets": {"max_turns": 2, "timeout_s": 10},
            "containment_policy": {"kind": "read-only-evaluator"},
            "network_external_write_policy": {"network": "deny", "external_write": "deny"},
            "credential_service_account_policy": {"ambient": "deny"},
            "provider_managed_unknowns": [],
            "native_tools": ["Read"],
            "native_surface_requirements": [], "mcp_servers": [],
        }
        write_json(profile_path, profile)
        capabilities = json.loads(self.cap_path.read_text(encoding="utf-8"))
        write_json(capability_path, capabilities)
        return profile_path, capability_path

    def test_assessor_accepts_matching_runtime_and_blinds_the_arm(self):
        import assess70
        out = self.complete_run()
        keys = self.root / "keys"
        keys.mkdir()
        (keys / "key.txt").write_text("custodian", encoding="utf-8")
        profile, capabilities = self.evaluator_material("1")
        with patch.object(assess70, "load_adapter", return_value=FakeEvaluator):
            code = assess70.main([
                "--run", str(out), "--keys", str(keys),
                "--evaluator-profile", str(profile),
                "--evaluator-capabilities", str(capabilities),
                "--adapter", "fake",
            ])
        self.assertEqual(code, 0)
        assessment = json.loads((out / "assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(assessment["qualification_outcome"], "PASS")
        bundle_listing = json.loads((out / "assessment-identity.json").read_text(encoding="utf-8"))
        self.assertEqual(bundle_listing["redaction_version"], assess70.REDACTION_VERSION)

    def test_assessor_runtime_mismatch_is_inadmissible(self):
        import assess70
        out = self.complete_run("run-assess-mismatch")
        keys = self.root / "keys-mismatch"
        keys.mkdir()
        (keys / "key.txt").write_text("custodian", encoding="utf-8")
        profile, capabilities = self.evaluator_material("2")
        with patch.object(assess70, "load_adapter", return_value=FakeEvaluator):
            code = assess70.main([
                "--run", str(out), "--keys", str(keys),
                "--evaluator-profile", str(profile),
                "--evaluator-capabilities", str(capabilities),
                "--adapter", "fake",
            ])
        self.assertEqual(code, 2)
        assessment = json.loads((out / "assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(assessment["assessment_status"], "INADMISSIBLE")
        self.assertEqual(assessment["qualification_outcome"], "NOT_EVALUATED")

    def test_probe_run_produces_complete_admissible_integrity_bound_evidence(self):
        out = self.root / "run"
        identity = self.identity()
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe",
            identity=identity, pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertTrue(summary["owner_read_sequences"])
        self.assertTrue((out / "evidence-integrity.json").is_file())
        self.assertEqual(core70.validate_complete_run(out, identity, self.requirements), [])
        self.assertEqual(core70.validate_complete_run(out, identity, self.requirements), [])

    def test_cache_rejects_deleted_or_tampered_evidence(self):
        out = self.root / "run2"
        identity = self.identity()
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe",
            identity=identity, pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        (out / "trace.jsonl").write_text("tampered", encoding="utf-8")
        self.assertTrue(core70.validate_complete_run(out, identity, self.requirements))

    def test_pin_mismatches_refuse_the_run_and_every_pinned_input_changes_run_identity(self):
        baseline = self.identity()["identity_sha256"]
        # package pin: the installed tree must equal the prepared arm digest, before anything launches
        (self.dist / "software-design" / "SKILL.md").write_text("# tampered\n")
        with self.assertRaisesRegex(core70.ContractError, "installed protocol package digest mismatch"):
            self.invoke(self.root / "run-pin")
        (self.dist / "software-design" / "SKILL.md").write_text("# software-design\n")
        self.assertEqual(self.identity()["identity_sha256"], baseline)
        # fixture, oracle, requirements and profile pins each move the identity
        (self.corpus / "fixtures" / "f1" / "project" / "README.txt").write_text("changed fixture")
        self.assertNotEqual(self.identity()["identity_sha256"], baseline)
        (self.corpus / "fixtures" / "f1" / "project" / "README.txt").write_text("fixture")
        (self.oracles / "check_o1.py").write_text("import sys\nsys.exit(1)\n")
        self.assertNotEqual(self.identity()["identity_sha256"], baseline)
        (self.oracles / "check_o1.py").write_text("import sys\nsys.exit(0)\n")
        write_json(self.profile_path, {**json.loads(self.profile_path.read_text()), "agent_model": "other"})
        self.assertNotEqual(self.identity()["identity_sha256"], baseline)

    def test_missing_oracle_is_non_pass(self):
        out = self.root / "run3"
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=None, mode="probe",
            identity=self.identity(), pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "MISSING_REQUIRED_EVIDENCE")
        self.assertEqual(summary["missing_required_oracles"], ["o1"])

    def test_evaluator_bundle_blinds_arm_and_redacts_identifiers_but_not_numbers(self):
        import assess70
        out = self.complete_run("run-blind")
        (out / "final-report.md").write_text("Under Protocol 7.1 (SSDP 6.6.0, arm p71) the mean was 6.5 and 7.25 on 127.0.0.1", encoding="utf-8")
        keys = self.root / "keys-blind"
        keys.mkdir()
        (keys / "key.txt").write_text("custodian", encoding="utf-8")
        bundle = self.root / "bundle-blind"
        bundle.mkdir()
        assess70.prepare_bundle(out, keys, None, self.requirements, bundle)
        run = bundle / "run"
        for withheld in ("run-identity.json", "profile-snapshot.json", "installed-package", "adapter-artifacts"):
            self.assertFalse((run / withheld).exists(), withheld)
        self.assertNotIn("arm", json.loads((run / "summary.json").read_text(encoding="utf-8")))
        report = (run / "final-report.md").read_text(encoding="utf-8")
        self.assertNotIn("7.1", report)
        self.assertNotIn("p71", report)
        self.assertIn("mean was 6.5 and 7.25 on 127.0.0.1", report)


class AssessmentValidation(unittest.TestCase):
    def test_assessment_rejects_missing_expected_items(self):
        import assess70
        req = core70.Requirements(
            artifacts=(), oracles=(),
            scoring_items=({"id": "i1", "measure": "m", "critical": True, "branch": "b", "allowed_dispositions": ["pass", "fail", "unresolved"]},),
            artifact_manifest_digest="a", oracle_manifest_digest="o", scoring_manifest_digest="s")
        verdict = {"episode": "E1", "dispositions": [], "notes": ""}
        errors = assess70.validate_verdict(verdict, "E1", req)
        self.assertTrue(any("missing dispositions" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
