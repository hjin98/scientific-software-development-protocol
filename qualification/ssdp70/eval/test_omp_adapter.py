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
import harness70
import observer70
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
        paths = omp._private_mcp_paths(self.private)
        shutil.copy2(EVAL / "stub_tools" / "mediator.py", paths["server"])
        paths["stub"].mkdir(parents=True)
        paths["log"].write_text("")
        paths["account"].write_text("agent-account\n")
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


class B1B2ObserverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-obs-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.evidence = self.tmp / "obs-evidence.jsonl"

    def test_observer_captures_catalog_mcp_and_tools(self):
        prompt = (
            "<skills>\n"
            "<skill><name>scientific-formulation</name></skill>\n"
            "<skill><name>software-design</name></skill>\n"
            "</skills>\n"
            "# xd:// Tool Devices\n"
            "* xd://mcp__ssdp_issue_search: search\n"
            "* xd://mcp__ssdp_delegate: delegate\n"
            "## read\nread tool\n"
            "## bash\nbash tool\n"
        )
        self.assertEqual(
            observer70.parse_system_prompt_catalog(prompt),
            ["scientific-formulation", "software-design"],
        )
        self.assertEqual(
            observer70.parse_system_prompt_mcp_devices(prompt),
            ["mcp__ssdp_delegate", "mcp__ssdp_issue_search"],
        )
        self.assertEqual(
            observer70.parse_system_prompt_native_tools(prompt),
            ["bash", "read"],
        )

        with observer70.TrustedObserver(evidence_path=self.evidence, verify_peer=False) as obs:
            import urllib.request
            req = urllib.request.Request(
                obs.base_url + "/chat/completions",
                data=json.dumps({
                    "model": "local/test-model",
                    "messages": [{"role": "system", "content": prompt}],
                }).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req) as resp:
                data = resp.read().decode("utf-8")
                self.assertIn("data: ", data)
                self.assertIn("[DONE]", data)

            info = obs.get_observation()
            self.assertIsNotNone(info)
            self.assertEqual(info["model"], "local/test-model")
            self.assertEqual(info["skills"], ["scientific-formulation", "software-design"])
            self.assertEqual(info["mcp_devices"], ["mcp__ssdp_delegate", "mcp__ssdp_issue_search"])
            self.assertEqual(info["tools"], ["bash", "read"])

            ok, errors, records = observer70.validate_observer_log(self.evidence)
            self.assertTrue(ok, errors)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["request_model"], "local/test-model")
            self.assertEqual(records[0]["observed_skills"], ["scientific-formulation", "software-design"])

    def test_observer_peer_verification_rejects_unauthorized(self):
        with observer70.TrustedObserver(evidence_path=self.evidence, verify_peer=True) as obs:
            import urllib.error
            import urllib.request
            req = urllib.request.Request(
                obs.base_url + "/chat/completions",
                data=json.dumps({"model": "m", "messages": []}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(req)
            self.assertEqual(caught.exception.code, 403)

    def test_observer_rejects_non_completions_endpoints(self):
        with observer70.TrustedObserver(evidence_path=self.evidence, verify_peer=False) as obs:
            import urllib.error
            import urllib.request
            for bad_path, expected_code in [("/v1/models", 404), ("/", 404)]:
                req = urllib.request.Request(
                    f"http://127.0.0.1:{obs.port}{bad_path}",
                    data=b"{}",
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    urllib.request.urlopen(req)
                self.assertEqual(caught.exception.code, expected_code)

    def test_runtime_observation_with_observer_evidence(self):
        evidence_record = {
            "model": "probe/observed-model",
            "runtime_version": "omp/18.0.11",
            "runtime_version_source": "trusted-observer-verified-executable-build",
            "tools": ["read", "bash", "edit", "glob", "grep", "write"],
            "mcp_servers": [{"name": "ssdp70", "status": "connected"}],
            "evidence_sha256": "f" * 64,
        }
        obs = omp.runtime_observation("", observer_record=evidence_record)
        self.assertEqual(obs["model"], "probe/observed-model")
        self.assertEqual(obs["runtime_version"], "omp/18.0.11")
        self.assertEqual(obs["runtime_version_source"], "trusted-observer-verified-executable-build")
        self.assertEqual(obs["tools"], ["read", "bash", "edit", "glob", "grep", "write"])
        self.assertEqual(len(obs["mcp_servers"]), 1)
        self.assertEqual(obs["observer_evidence_sha256"], "f" * 64)


class NameMintingAuthorityTests(unittest.TestCase):
    def test_sanitize_component_rules(self):
        self.assertEqual(omp._sanitize_component("SSDP70"), "ssdp")
        self.assertEqual(omp._sanitize_component("Tool-A1!_B"), "tool_a_b")
        self.assertEqual(omp._sanitize_component("___alpha___"), "alpha")
        self.assertEqual(omp._sanitize_component(""), "")

    def test_mcp_native_id_prefix_deduplication(self):
        # In OMP v18.0.11 hft: if tool starts with server + "_", prefix is stripped
        self.assertEqual(omp.mcp_native_id("server", "server_tool"), "mcp__server_tool")
        self.assertEqual(omp.mcp_native_id("ssdp70", "issue_search"), "mcp__ssdp_issue_search")
        self.assertEqual(omp.mcp_native_id("alpha", "tool_a1"), "mcp__alpha_tool_a")

    def test_mcp_native_id_length_cap_64(self):
        long_tool = "a" * 70
        device = omp.mcp_native_id("server", long_tool)
        self.assertEqual(len(device), 64)
        self.assertTrue(device.startswith("mcp__server_"))
        self.assertEqual(device[55], "_")


class D4RepairsNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-d4-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.skills = self.tmp / "skills"
        for s in omp.SSDP_SKILLS:
            (self.skills / s).mkdir(parents=True)
            (self.skills / s / "SKILL.md").write_text(f"---\nname: {s}\n---\n# {s}\n")

    def _ctx(self):
        return {"project": str(self.project), "skills_root": str(self.skills), "package_identity": _pkg()}

    def test_root_selection_on_skill_url_read(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "c1", "toolName": "read",
                        "args": {"path": "skill://scientific-formulation"}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "c1", "toolName": "read",
                        "result": {"content": [{"type": "text", "text": "body"}]}, "isError": False}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "ok"}]}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r1", self._ctx())
        self.assertEqual(errors, [])
        roots = [e for e in events if e.get("kind") == "root_selection"]
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0]["payload"]["logical_root"], "scientific-formulation")
        self.assertEqual(roots[0]["payload"]["selection_mechanism"], "ordinary-resource-read")
        self.assertIsNotNone(roots[0]["payload"]["resolved_package_identity"])

    def test_root_selection_on_skill_file_read(self):
        skill_file = self.skills / "software-design" / "SKILL.md"
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "c2", "toolName": "read",
                        "args": {"path": str(skill_file)}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "c2", "toolName": "read",
                        "result": {"content": [{"type": "text", "text": "body"}]}, "isError": False}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "ok"}]}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r2", self._ctx())
        self.assertEqual(errors, [])
        roots = [e for e in events if e.get("kind") == "root_selection"]
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0]["payload"]["logical_root"], "software-design")

    def test_mcp_issue_create_and_comment_emit_mutation_and_access(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "c_create", "toolName": "write",
                        "args": {"path": "xd://mcp__ssdp_issue_create", "title": "new issue"}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "c_create", "toolName": "write",
                        "result": {"content": [{"type": "text", "text": "created"}],
                                   "details": {"xdev": {"serverName": "ssdp70", "mcpToolName": "issue_create"}}},
                        "isError": False}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "ok"}]}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r3", self._ctx())
        self.assertEqual(errors, [])
        mutations = [e for e in events if e.get("kind") == "mutation"]
        accesses = [e for e in events if e.get("kind") == "issue_evidence_access"]
        self.assertTrue(len(mutations) >= 2)  # start + end
        self.assertTrue(len(accesses) >= 2)   # start + end
        self.assertEqual(mutations[-1]["payload"]["workspace_external_class"], "qualification-owned-standin")
        self.assertEqual(mutations[-1]["payload"]["authorization_decision"], "sandbox-mediate")

    def test_mcp_delegate_call_and_return(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "d1", "toolName": "write",
                        "args": {"path": "xd://mcp__ssdp_delegate", "task": "analyze"}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "d1", "toolName": "write",
                        "result": {"content": [{"type": "text", "text": "done"}],
                                   "details": {"xdev": {"serverName": "ssdp70", "mcpToolName": "delegate"}}},
                        "isError": False}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop", "content": [{"type": "text", "text": "ok"}]}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r4", self._ctx())
        self.assertEqual(errors, [])
        kinds = [e["kind"] for e in events]
        self.assertIn("delegate_call", kinds)
        self.assertIn("delegate_return", kinds)

    def test_mcp_server_and_tool_name_mismatch_fails_closed(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "d2", "toolName": "write",
                        "args": {"path": "xd://mcp__ssdp_delegate"}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "d2", "toolName": "write",
                        "result": {"content": [],
                                   "details": {"xdev": {"serverName": "rogue-server", "mcpToolName": "delegate"}}},
                        "isError": False}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop"}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r5", self._ctx())
        self.assertTrue(any("serverName mismatch" in err for err in errors), errors)

    def test_unclosed_pending_calls_at_eof_fails_closed(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "unclosed_1", "toolName": "read",
                        "args": {"path": "file.txt"}}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r6", self._ctx())
        self.assertTrue(any("unclosed pending tool execution" in err for err in errors), errors)

    def test_external_path_write_classification(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "message_end", "message": {"role": "assistant", "provider": "p", "model": "m"}}),
            json.dumps({"type": "tool_execution_start", "toolCallId": "w1", "toolName": "write",
                        "args": {"path": "/etc/shadow", "content": "hacked"}}),
            json.dumps({"type": "tool_execution_end", "toolCallId": "w1", "toolName": "write",
                        "result": "Permission denied", "isError": True}),
            json.dumps({"type": "agent_end", "messages": [{"role": "assistant", "stopReason": "stop"}]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r7", self._ctx())
        self.assertEqual(errors, [])
        mutations = [e for e in events if e.get("kind") == "mutation"]
        self.assertEqual(mutations[-1]["payload"]["workspace_external_class"], "external")
        self.assertEqual(mutations[-1]["payload"]["disposition"], "blocked-or-error")

    def test_token_cap_termination_distinction(self):
        trace = "\n".join([
            json.dumps({"type": "session", "version": 3}),
            json.dumps({"type": "agent_end", "messages": [
                {"role": "assistant", "provider": "p", "model": "m", "stopReason": "length",
                 "content": [{"type": "text", "text": "partial"}]}
            ]}),
        ])
        events, _, errors, _ = omp.normalize(trace, "r8", self._ctx())
        self.assertEqual(errors, [])
        term = [e for e in events if e.get("kind") == "termination"][0]
        self.assertEqual(term["payload"]["state"], "length_capped")
        self.assertTrue(term["payload"]["native_return_state"]["lengthCapped"])


class HarnessControlExclusionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-harn-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.corpus = self.tmp / "corpus"
        self.fixture = self.corpus / "fixtures" / "f1"
        self.fixture.mkdir(parents=True)
        self.project = self.tmp / "project"

    def test_build_project_rejects_reserved_control_paths(self):
        # Place a reserved control path inside fixture
        (self.fixture / "project").mkdir(parents=True)
        (self.fixture / "project" / ".claude").mkdir()
        episode = {"id": "ep1", "fixture": "f1"}
        with self.assertRaises(core70.ContractError) as caught:
            harness70.build_project(self.corpus, episode, self.project, [".claude"])
        self.assertIn("fixture baseline contains reserved provider control path", str(caught.exception))

    def test_unified_private_mcp_paths(self):
        private = self.tmp / "private"
        h_paths = harness70.private_mcp_paths(private)
        o_paths = omp._private_mcp_paths(private)
        self.assertEqual(h_paths, o_paths)
        self.assertEqual(h_paths["server"].name, "mcp-server.py")
        self.assertEqual(h_paths["stub"].name, "stub")
        self.assertEqual(h_paths["log"].name, "side-effects.jsonl")
        self.assertEqual(h_paths["account"].name, "mcp-account.txt")


class ContainmentAndLaunchRepairsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="omp-cont-launch-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.project = self.tmp / "project"
        self.project.mkdir()
        self.home = self.tmp / "runtime-home"
        (self.home / omp.OMP_AGENT_RELATIVE).mkdir(parents=True)
        self.env = {"HOME": str(self.home)}
        self.private = self.home.parent
        paths = omp._private_mcp_paths(self.private)
        shutil.copy2(EVAL / "stub_tools" / "mediator.py", paths["server"])
        paths["stub"].mkdir(parents=True)
        paths["log"].write_text("")
        paths["account"].write_text("agent-account\n")
        self.substrate = self.tmp / "fake-substrate"
        self.substrate.write_text("#!/bin/sh\nexit 0\n")
        self.substrate.chmod(0o755)
        self.substrate_sha = hashlib.sha256(self.substrate.read_bytes()).hexdigest()
        self.profile = json.loads(TEMPLATE_PROFILE.read_text())
        policy = self.profile["containment_policy"]
        policy["substrate"].update({
            "status": "frozen", "executable": str(self.substrate),
            "executable_sha256": self.substrate_sha,
        })
        policy["credential_isolation"] = {"kind": "external-broker-outside-sandbox", "broker": "/run/broker.sock"}
        policy["provider_config_status"] = "frozen"
        policy["provider_config"] = {"modelRoles": {"default": "probe/local"}}

    def test_minimal_substrate_binds_exclude_host_home(self):
        omp.realize_containment(self.profile, self.project, self.env)
        cmd = omp._substrate_command(self.profile["containment_policy"]["substrate"], self.project, self.env)
        # Verify --ro-bind / / is completely absent
        self.assertNotIn(["--ro-bind", "/", "/"], [cmd[i:i+3] for i in range(len(cmd)-2)])
        # Verify minimal explicit binds
        self.assertIn("--proc", cmd)
        self.assertIn("--dev", cmd)
        self.assertIn("--tmpfs", cmd)
        self.assertIn("/usr", cmd)
        # Verify project and home are bound
        self.assertIn(str(self.project.resolve()), cmd)
        self.assertIn(str(self.home.resolve()), cmd)

    def test_launch_executes_and_reports_real_identity(self):
        omp.realize_containment(self.profile, self.project, self.env)
        launched = omp.launch(self.profile, "hello", self.project, self.env)
        self.assertIn("returncode", launched)
        self.assertIn("wall_s", launched)
        self.assertEqual(launched["returncode"], 0)
        cmd_id = launched["command_identity"]
        self.assertEqual(cmd_id["adapter_id"], "omp-json-v1")
        self.assertTrue(cmd_id["strict_mcp_config"])

    def test_launch_detects_control_file_tampering(self):
        omp.realize_containment(self.profile, self.project, self.env)
        config_path, _ = omp._control_paths(self.project, self.env)
        # Substrate that mutates config.yml
        mutator = self.tmp / "mutator-substrate"
        mutator.write_text(f"#!/bin/sh\necho 'tampered: true' >> {config_path}\nexit 0\n")
        mutator.chmod(0o755)
        self.profile["containment_policy"]["substrate"]["executable"] = str(mutator)
        self.profile["containment_policy"]["substrate"]["executable_sha256"] = hashlib.sha256(mutator.read_bytes()).hexdigest()
        with self.assertRaises(RuntimeError) as caught:
            omp.launch(self.profile, "hello", self.project, self.env)
        self.assertIn("containment settings changed", str(caught.exception))

    def test_harness_run_episode_with_omp_adapter(self):
        corpus = self.tmp / "harness-corpus"
        fixture = corpus / "fixtures" / "f1"
        (fixture / "project").mkdir(parents=True)
        (fixture / "project" / "hello.py").write_text("print('hi')\n")
        episode = {
            "id": "E_OMP",
            "fixture": "f1",
            "prompt": "solve problem",
            "claims": [],
        }
        dist = self.tmp / "harness-dist"
        for s in omp.SSDP_SKILLS:
            (dist / s).mkdir(parents=True)
            (dist / s / "SKILL.md").write_text(f"---\nname: {s}\n---\n# {s}\n")
        dist_tree_sha = core70.sha256_tree(dist)
        arm = {
            "name": "candidate",
            "requested_ref": "candidate",
            "commit": "c" * 40,
            "version": "7.0.0",
            "skills_path": str(dist),
            "dist_tree_sha256": dist_tree_sha,
        }
        trace_script = self.tmp / "trace-substrate"
        trace_content = _synthetic_trace()
        trace_script.write_text(f"#!/bin/sh\ncat << 'EOF'\n{trace_content}\nEOF\n")
        trace_script.chmod(0o755)
        self.profile["containment_policy"]["substrate"]["executable"] = str(trace_script)
        self.profile["containment_policy"]["substrate"]["executable_sha256"] = hashlib.sha256(trace_script.read_bytes()).hexdigest()

        bundle = core70.ProfileBundle(
            profile=self.profile,
            capabilities=json.loads(TEMPLATE_MANIFEST.read_text()),
            profile_key="omp-key",
            profile_key_sha256="k" * 64,
            capability_manifest_sha256="m" * 64,
        )
        requirements = core70.Requirements(
            artifacts=(), oracles=(), scoring_items=(),
            artifact_manifest_digest="a" * 64,
            oracle_manifest_digest="o" * 64,
            scoring_manifest_digest="s" * 64,
        )
        identity = {
            "schema": 2, "identity_sha256": "id" + "0" * 62, "subject": arm,
            "episode": "E_OMP", "arm": "candidate",
        }
        out = self.tmp / "out-episode"
        result = harness70.run_episode(
            corpus=corpus,
            episode=episode,
            arm=arm,
            arms_manifest_sha256="m" * 64,
            dist=dist,
            out=out,
            profile_bundle=bundle,
            profile_path=TEMPLATE_PROFILE,
            capability_path=TEMPLATE_MANIFEST,
            requirements=requirements,
            requirements_root=self.tmp,
            adapter_module=omp,
            oracles=None,
            mode="probe",
            admission=None,
            identity=identity,
            pair_order=["E_OMP"],
        )
        self.assertEqual(result["episode"], "E_OMP")
        self.assertEqual(result["execution_returncode"], 0)
        self.assertTrue((out / "trace.jsonl").is_file())
        self.assertTrue((out / "events.normalized.jsonl").is_file())
        self.assertTrue((out / "final-report.md").is_file())


if __name__ == "__main__":
    unittest.main()
