import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import core70
from adapters import omp

EVAL = Path(__file__).resolve().parent
TEMPLATE_PROFILE = EVAL / "profiles" / "omp-headless.template.json"
TEMPLATE_MANIFEST = EVAL / "capabilities" / "omp-headless.json"


def _pkg(sha="a" * 64):
    return {"package_sha256": sha}


def _context(project, skills_root):
    return {"project": str(project), "skills_root": str(skills_root), "package_identity": _pkg()}


def _normalize(trace, run_id="run-omp", project="/tmp/p", skills_root="/tmp/skills"):
    return omp.normalize(trace, run_id, _context(project, skills_root))


def _synthetic_trace(model_event=True):
    lines = [json.dumps({"type": "session", "version": 3})]
    if model_event:
        lines.append(json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "probe", "model": "local"}}))
    lines.extend([
        json.dumps({"type": "tool_execution_start", "toolCallId": "c1", "toolName": "read", "args": {"path": "a.py"}}),
        json.dumps({"type": "tool_execution_end", "toolCallId": "c1", "toolName": "read",
                    "result": {"content": [{"type": "text", "text": "x = 1"}], "details": {}}, "isError": False}),
        json.dumps({"type": "tool_execution_start", "toolCallId": "m1", "toolName": "write",
                    "args": {"path": "xd://mcp__ssdp_issue_search"}}),
        json.dumps({"type": "tool_execution_end", "toolCallId": "m1", "toolName": "write",
                    "result": {"content": [{"type": "text", "text": "[]"}],
                               "details": {"xdev": {"serverName": "ssdp70", "mcpToolName": "issue_search"}}},
                    "isError": False}),
        json.dumps({"type": "agent_end", "messages": [
            {"role": "assistant", "provider": "probe", "model": "local", "stopReason": "stop",
             "usage": {"input": 3, "output": 4}, "duration": 12.5,
             "content": [{"type": "text", "text": "done"}]},
        ]}),
    ])
    return "\n".join(lines)


class McpBindingTests(unittest.TestCase):
    def test_sanitize_component_removes_digits(self):
        self.assertEqual(omp._sanitize_component("ssdp70"), "ssdp")
        self.assertEqual(omp.mcp_native_id("ssdp70", "issue_search"), "mcp__ssdp_issue_search")
        self.assertEqual(omp.mcp_native_id("alpha", "tool_a1"), "mcp__alpha_tool_a")

    def test_template_binding_is_admissible(self):
        profile = json.loads(TEMPLATE_PROFILE.read_text())
        ok, errors, mapping = omp.verify_mcp_binding(profile)
        self.assertTrue(ok, errors)
        self.assertEqual(mapping["delegate"], "mcp__ssdp_delegate")

    def test_foreign_tool_surface_is_rejected(self):
        profile = json.loads(TEMPLATE_PROFILE.read_text())
        profile["mcp_servers"][0]["tools"] = ["mcp__other_issue_search"]
        ok, errors, _ = omp.verify_mcp_binding(profile)
        self.assertFalse(ok)
        self.assertTrue(any("raw->native binding" in error for error in errors))

    def test_raw_tool_from_device_id(self):
        self.assertEqual(omp._raw_tool_from_device_id("mcp__ssdp_issue_show"), "issue_show")
        self.assertIsNone(omp._raw_tool_from_device_id("mcp__unknown_tool"))


class CoreProviderNeutralBindingTests(unittest.TestCase):
    """The portable core must bind MCP tools by declared identity, not by a naming convention."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-core-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.manifest = json.loads(TEMPLATE_MANIFEST.read_text())
        self.profile = json.loads(TEMPLATE_PROFILE.read_text())
        self.profile["provider_managed_unknowns"] = []
        self.manifest["native_capabilities"]["tool:provider_native_alpha"] = {
            "semantic_classes": ["issue_evidence_store"], "scope": "test"}
        self.manifest["native_capabilities"]["tool:provider_native_beta"] = {
            "semantic_classes": ["issue_evidence_store"], "scope": "test"}
        self.manifest["native_capabilities"]["mcp_server:other"] = {
            "semantic_classes": ["issue_evidence_store"], "scope": "test"}

    def _load(self):
        profile_path = self.tmp / "profile.json"
        manifest_path = self.tmp / "manifest.json"
        profile_path.write_text(json.dumps(self.profile))
        manifest_path.write_text(json.dumps(self.manifest))
        return core70.load_profile(profile_path, manifest_path)

    def _servers(self, tools_a, tools_b):
        self.profile["native_tools"] = ["provider_native_alpha", "provider_native_beta"]
        self.profile["native_surface_requirements"] = ["mcp_server:ssdp70", "mcp_server:other"]
        self.profile["mcp_servers"] = [
            {"name": "ssdp70", "transport": "stdio", "server_id": "s1", "entrypoint": "e.py", "tools": tools_a},
            {"name": "other", "transport": "stdio", "server_id": "s2", "entrypoint": "e.py", "tools": tools_b},
        ]

    def test_non_convention_native_ids_are_accepted(self):
        self._servers(["provider_native_alpha"], ["provider_native_beta"])
        bundle = self._load()
        self.assertEqual(len(bundle.profile["mcp_servers"]), 2)

    def test_cross_server_duplicate_native_id_is_rejected(self):
        self._servers(["provider_native_alpha"], ["provider_native_alpha"])
        with self.assertRaises(core70.ContractError) as caught:
            self._load()
        self.assertIn("declared by more than one server", str(caught.exception))

    def test_mcp_tool_must_be_in_native_tools(self):
        self._servers(["provider_native_alpha"], ["provider_native_beta"])
        self.profile["native_tools"] = ["provider_native_alpha"]
        with self.assertRaises(core70.ContractError) as caught:
            self._load()
        self.assertIn("missing from the exact native tool surface", str(caught.exception))


class NormalizeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-norm-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.project = self.tmp / "project"
        self.project.mkdir()
        (self.project / "a.py").write_text("x = 1\n")
        self.skills = self.tmp / "skills"
        for skill in sorted(omp.SSDP_SKILLS):
            (self.skills / skill).mkdir(parents=True)

    def _ctx(self):
        return _context(self.project, self.skills)

    def test_trace_normalizes_and_is_schema_valid(self):
        trace = _synthetic_trace()
        events, completeness, errors, native = _normalize(trace, project=self.project, skills_root=self.skills)
        self.assertEqual(errors, [])
        self.assertEqual(native, 7)
        self.assertEqual(core70.validate_normalized_events(events, "run-omp"), [])
        self.assertEqual(core70.validate_completeness_map(native, completeness, events), [])
        kinds = [event["kind"] for event in events]
        self.assertEqual(kinds.count("catalog_snapshot"), 1)
        self.assertIn("resource_access", kinds)
        self.assertIn("issue_evidence_access", kinds)
        self.assertIn("termination", kinds)
        self.assertIn("final_result", kinds)
        self.assertEqual(omp.final_result(events), "done")
        catalog = omp.catalog_isolation(events)
        self.assertTrue(catalog["ok"], catalog)
        self.assertEqual(sorted(catalog["catalog"]), sorted(omp.SSDP_SKILLS))

    def test_mcp_write_binds_native_and_raw_tool(self):
        trace = _synthetic_trace()
        events, _, errors, _ = _normalize(trace, project=self.project, skills_root=self.skills)
        self.assertEqual(errors, [])
        mcp = [event for event in events if event["kind"] == "issue_evidence_access"]
        self.assertTrue(mcp)
        self.assertEqual(mcp[0]["payload"]["resource_identity"], "issue_search")

    def test_unknown_event_fails_closed(self):
        trace = _synthetic_trace() + "\n" + json.dumps({"type": "brand_new_event"})
        events, completeness, errors, native = _normalize(trace, project=self.project, skills_root=self.skills)
        self.assertTrue(any("unknown native type" in error for error in errors))
        last = completeness[-1]
        self.assertTrue(last["oracle_relevant"])
        self.assertEqual(last["mapped_event_ids"], [])

    def test_malformed_line_is_oracle_relevant(self):
        trace = _synthetic_trace() + "\nnot-json"
        _, completeness, errors, native = _normalize(trace, project=self.project, skills_root=self.skills)
        self.assertTrue(any("not valid JSON" in error for error in errors))
        self.assertTrue(completeness[-1]["oracle_relevant"])

    def test_observation_reports_catalog_unobserved(self):
        observation = omp.runtime_observation(_synthetic_trace())
        self.assertEqual(observation["model"], "probe/local")
        self.assertIsNone(observation["tools"])
        self.assertIsNone(observation["runtime_version"])


class DiscoveryClosureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-disc-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.home = self.tmp / "runtime-home"
        (self.home / omp.OMP_AGENT_RELATIVE).mkdir(parents=True)
        self.env = {"HOME": str(self.home)}

    def test_clean_project_and_run_home_close_discovery(self):
        self.assertEqual(omp.validate_ambient_discovery_closure(self.project, self.env), [])

    def test_project_local_discovery_is_refused(self):
        (self.project / ".mcp.json").write_text("{}")
        errors = omp.validate_ambient_discovery_closure(self.project, self.env)
        self.assertTrue(any(".mcp.json" in error for error in errors))

    def test_ambient_home_is_refused(self):
        env = {"HOME": str(Path(os.path.expanduser("~")))}
        errors = omp.validate_ambient_discovery_closure(self.project, env)
        self.assertTrue(any("ambient user home" in error for error in errors))


class ContainmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-cont-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.home = self.tmp / "runtime-home"
        (self.home / omp.OMP_AGENT_RELATIVE).mkdir(parents=True)
        self.env = {"HOME": str(self.home)}
        self.private = self.home.parent
        (self.private / "mcp").mkdir(parents=True)
        shutil.copy2(EVAL / "stub_tools" / "mediator.py", self.private / "mcp" / "mediator.py")
        (self.private / "stub-root").mkdir()
        (self.private / "side-effect-log.jsonl").write_text("")
        (self.private / "account.json").write_text("{}")
        self.substrate = self.tmp / "fake-substrate"
        self.substrate.write_text("#!/bin/sh\n")
        self.substrate.chmod(0o755)
        self.substrate_sha = hashlib.sha256(self.substrate.read_bytes()).hexdigest()
        self.profile = json.loads(TEMPLATE_PROFILE.read_text())

    def _freeze(self):
        policy = self.profile["containment_policy"]
        policy["substrate"].update({"status": "frozen", "executable": str(self.substrate),
                                    "executable_sha256": self.substrate_sha})
        policy["credential_isolation"] = {"kind": "external-broker-outside-sandbox", "broker": "/run/broker.sock"}
        policy["provider_config_status"] = "frozen"
        policy["provider_config"] = {"modelRoles": {"default": "probe/local"}}

    def test_unfrozen_template_fails_closed(self):
        with self.assertRaises(RuntimeError) as caught:
            omp.realize_containment(self.profile, self.project, self.env)
        self.assertIn("not operator-frozen", str(caught.exception))

    def test_missing_credential_isolation_fails_closed(self):
        self._freeze()
        self.profile["containment_policy"]["credential_isolation"] = {"kind": "none"}
        with self.assertRaises(RuntimeError) as caught:
            omp.realize_containment(self.profile, self.project, self.env)
        self.assertIn("credentials outside the sandbox", str(caught.exception))

    def test_frozen_substrate_realizes_namespace_boundaries(self):
        self._freeze()
        document = omp.realize_containment(self.profile, self.project, self.env)
        command = document["realization"]["substrate_command"]
        for flag in ("--unshare-net", "--unshare-pid", "--unshare-ipc", "--unshare-user"):
            self.assertIn(flag, command)
        self.assertEqual(document["realization"]["native_network"], "unshared-no-egress")
        self.assertEqual(omp.validate_containment_realization(self.profile, self.project, self.env), [])

    def test_launch_refuses_project_discovery(self):
        self._freeze()
        (self.project / ".omp").mkdir()
        with self.assertRaises(RuntimeError) as caught:
            omp.launch(self.profile, "hi", self.project, self.env)
        self.assertIn("ambient discovery", str(caught.exception))


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-inst-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.dist = self.tmp / "dist"
        for skill in sorted(omp.SSDP_SKILLS):
            (self.dist / skill).mkdir(parents=True)
            (self.dist / skill / "SKILL.md").write_text("body\n")
        self.home = self.tmp / "runtime-home"
        self.home.mkdir()
        self.env = {"HOME": str(self.home)}

    def test_install_returns_run_owned_root(self):
        root = omp.install_skills(self.dist, self.tmp / "project", self.env)
        self.assertEqual(root, self.home / omp.OMP_AGENT_RELATIVE / "skills")
        self.assertEqual(sorted(p.name for p in root.iterdir()), sorted(omp.SSDP_SKILLS))

    def test_install_requires_run_owned_home(self):
        with self.assertRaises(RuntimeError):
            omp.install_skills(self.dist, self.tmp / "project", {"HOME": str(Path(os.path.expanduser("~")))})


class ProfileTemplateTests(unittest.TestCase):
    def test_template_loads_but_fails_closed(self):
        bundle = core70.load_profile(TEMPLATE_PROFILE, TEMPLATE_MANIFEST)
        self.assertEqual(bundle.profile["adapter_id"], "omp-json-v1")
        errors = core70.validate_runtime_observation(bundle, omp.runtime_observation(""))
        self.assertTrue(any("unfrozen runtime/reasoning marker" in error for error in errors))
        self.assertTrue(any("did not expose a valid native tools list" in error for error in errors))

    def test_adapter_is_discoverable(self):
        import assess70
        module = assess70.load_adapter("omp")
        self.assertEqual(module.ADAPTER_ID, "omp-json-v1")


if __name__ == "__main__":
    unittest.main()
