import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import core70
import harness70
from adapters import claude

SKILLS = sorted(claude.SSDP_SKILLS)


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
            },
        }

    @staticmethod
    def install_skills(dist, project):
        target = project / ".claude" / "skills"
        target.mkdir(parents=True)
        for name in SKILLS:
            shutil.copytree(dist / name, target / name)

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
            },
        }

    @staticmethod
    def runtime_observation(stdout):
        return {"model": "fake", "runtime_version": "1", "tools": ["Read"], "native_capabilities": [], "memory_paths": {}, "mcp_servers": []}

    normalize = staticmethod(claude.normalize)
    final_result = staticmethod(claude.final_result)
    catalog_isolation = staticmethod(claude.catalog_isolation)
    owner_reads = staticmethod(claude.owner_reads)


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
            "r2_point_index": None,
            "owner_false_activation": None,
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
            "native_tools": ["Read"], "native_mcp_servers": [], "native_surface_requirements": [],
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
            oracles=self.oracles.parent, mode="probe", admission=None, rep=0, pair_order=["p70"])


    def complete_run(self, name="run-assess"):
        out = self.root / name
        identity = self.identity()
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe", admission=None,
            identity=identity, pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        return out

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
            "native_mcp_servers": [],
            "native_surface_requirements": [],
        }
        write_json(profile_path, profile)
        capabilities = json.loads(self.cap_path.read_text(encoding="utf-8"))
        write_json(capability_path, capabilities)
        bundle = core70.load_profile(profile_path, capability_path)
        admission_root = self.root / f"eval-{version}-admission"
        evidence = admission_root / "evidence"
        evidence.mkdir(parents=True)
        checks = {}
        for name in core70.EVALUATOR_ADMISSION_CHECKS:
            proof = evidence / f"{name}.json"
            proof.write_text(json.dumps({"check": name, "pass": True}), encoding="utf-8")
            checks[name] = {
                "status": "PASS",
                "evidence_path": f"evidence/{name}.json",
                "evidence_sha256": core70.sha256_file(proof),
            }
        admission = admission_root / "admission.json"
        write_json(admission, {
            "schema": 1, "status": "ADMITTED", "role": "evaluator",
            "profile_key_sha256": bundle.profile_key_sha256,
            "adapter_sha256": core70.sha256_file(Path(FakeEvaluator.__file__).resolve()),
            "core_sha256": core70.sha256_file(Path(core70.__file__).resolve()),
            "capability_manifest_sha256": bundle.capability_manifest_sha256,
            "checks": checks,
        })
        return profile_path, capability_path, admission

    def test_assessor_requires_admitted_runtime_and_accepts_matching_runtime(self):
        import assess70
        out = self.complete_run()
        keys = self.root / "keys"
        keys.mkdir()
        (keys / "key.txt").write_text("custodian", encoding="utf-8")
        profile, capabilities, admission = self.evaluator_material("1")
        with patch.object(assess70, "load_adapter", return_value=FakeEvaluator):
            code = assess70.main([
                "--run", str(out), "--keys", str(keys),
                "--evaluator-profile", str(profile),
                "--evaluator-capabilities", str(capabilities),
                "--evaluator-admission", str(admission),
                "--adapter", "fake",
            ])
        self.assertEqual(code, 0)
        assessment = json.loads((out / "assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(assessment["qualification_outcome"], "PASS")
        self.assertTrue((out / "assessment-profile-admission-snapshot.json").is_file())

    def test_assessor_runtime_mismatch_is_inadmissible(self):
        import assess70
        out = self.complete_run("run-assess-mismatch")
        keys = self.root / "keys-mismatch"
        keys.mkdir()
        (keys / "key.txt").write_text("custodian", encoding="utf-8")
        profile, capabilities, admission = self.evaluator_material("2")
        with patch.object(assess70, "load_adapter", return_value=FakeEvaluator):
            code = assess70.main([
                "--run", str(out), "--keys", str(keys),
                "--evaluator-profile", str(profile),
                "--evaluator-capabilities", str(capabilities),
                "--evaluator-admission", str(admission),
                "--adapter", "fake",
            ])
        self.assertEqual(code, 2)
        assessment = json.loads((out / "assessment.json").read_text(encoding="utf-8"))
        self.assertEqual(assessment["evidence_state"], "INADMISSIBLE")
        self.assertEqual(assessment["qualification_outcome"], "NOT_EVALUATED")

    def test_probe_run_produces_complete_admissible_integrity_bound_evidence(self):
        out = self.root / "run"
        identity = self.identity()
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe", admission=None,
            identity=identity, pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertTrue(summary["owner_read_sequences"])
        self.assertTrue((out / "evidence-integrity.json").is_file())
        self.assertEqual(core70.validate_complete_run(out, identity, self.requirements), [])
        self.assertTrue(core70.cache_valid(out, identity, self.requirements))

    def test_cache_rejects_deleted_or_tampered_evidence(self):
        out = self.root / "run2"
        identity = self.identity()
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=self.oracles.parent, mode="probe", admission=None,
            identity=identity, pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        (out / "trace.jsonl").write_text("tampered", encoding="utf-8")
        self.assertFalse(core70.cache_valid(out, identity, self.requirements))

    def test_missing_oracle_is_non_pass(self):
        out = self.root / "run3"
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms",
            dist=self.dist, out=out, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=FakeAdapter, oracles=None, mode="probe", admission=None,
            identity=self.identity(), pair_order=["p70"])
        self.assertEqual(summary["evidence_state"], "MISSING_REQUIRED_EVIDENCE")
        self.assertEqual(summary["missing_required_oracles"], ["o1"])


class AssessmentValidation(unittest.TestCase):
    def test_assessment_rejects_missing_expected_items(self):
        import assess70
        req = core70.Requirements(
            artifacts=(), oracles=(),
            scoring_items=({"id": "i1", "measure": "m", "critical": True, "branch": "b", "allowed_dispositions": ["pass", "fail", "unresolved"]},),
            artifact_manifest_digest="a", oracle_manifest_digest="o", scoring_manifest_digest="s")
        verdict = {"episode": "E1", "dispositions": [], "r2_point_index": None, "owner_false_activation": None, "notes": ""}
        errors = assess70.validate_verdict(verdict, "E1", req)
        self.assertTrue(any("missing dispositions" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
