import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import core70
from adapters import claude

HERE = Path(__file__).resolve().parent
TRACE_ROOT = HERE.parent / "stage-f-prerun-actual-profile-recheck-2026-09-28" / "native-traces"


class ActualTraceRegressionTests(unittest.TestCase):
    def package_context(self, root: Path):
        skills = root / ".claude" / "skills"
        return {
            "project": str(root),
            "skills_root": str(skills),
            "package_identity": {
                "arm": "p70",
                "commit": "db94a2dfb7fef480f37227eab5c45256e89901b8",
                "version": "7.0.0",
                "package_sha256": "b" * 64,
            },
        }

    def test_a4_retained_21283_system_subtypes_are_reviewed_non_oracle(self):
        retained = []
        for name in ("init-probe.jsonl", "skill-probe.jsonl"):
            for line in (TRACE_ROOT / name).read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("type") == "system" and row.get("subtype") in {"thinking_tokens", "post_turn_summary"}:
                    retained.append(row)
        trace = "\n".join(json.dumps(row) for row in retained)
        with tempfile.TemporaryDirectory() as td:
            events, mapping, errors, count = claude.normalize(trace, "a4", self.package_context(Path(td)))
        self.assertEqual(errors, [])
        self.assertEqual(len(mapping), count)
        classes = {row["classification"] for row in mapping}
        self.assertIn("reviewed-non-oracle-system:thinking_tokens", classes)
        self.assertIn("reviewed-non-oracle-system:post_turn_summary", classes)
        reviewed = [row for row in mapping if row["classification"].startswith("reviewed-non-oracle-system:")]
        self.assertTrue(reviewed)
        self.assertTrue(all(row["oracle_relevant"] is False and row["mapped_event_ids"] == [] for row in reviewed))

    def test_a5_retained_skill_injection_binds_exact_installed_skill_bytes(self):
        trace = (TRACE_ROOT / "skill-probe.jsonl").read_text(encoding="utf-8")
        raw = [json.loads(line) for line in trace.splitlines() if line.strip()]
        synthetic = next(row for row in raw if row.get("type") == "user" and row.get("isSynthetic") is True)
        text = next(block["text"] for block in synthetic["message"]["content"] if block.get("type") == "text")
        injected = text.split("\n\n", 1)[1]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / ".claude" / "skills" / "software-implementation" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_bytes(injected.encode("utf-8"))
            events, mapping, errors, count = claude.normalize(trace, "a5", self.package_context(root))
            self.assertEqual(errors, [])
            self.assertEqual(core70.validate_completeness_map(count, mapping, events), [])
            injected_reads = [
                event for event in events
                if event.get("kind") == "resource_access"
                and (event.get("payload") or {}).get("operation") == "skill-injected-body"
            ]
            self.assertEqual(len(injected_reads), 1)
            payload = injected_reads[0]["payload"]
            self.assertEqual(payload["resource_bytes"], len(injected.encode("utf-8")))
            self.assertEqual(payload["resource_sha256"], hashlib.sha256(injected.encode("utf-8")).hexdigest())
            self.assertEqual(payload["result_content"], injected)
            self.assertEqual(core70.validate_claim_observability(events, ["t1", "t7", "t8"]), [])

    def test_unknown_system_subtype_remains_fail_closed(self):
        trace = json.dumps({"type": "system", "subtype": "future_unreviewed", "uuid": "x"})
        _, mapping, errors, _ = claude.normalize(trace, "unknown", {})
        self.assertTrue(any("no reviewed classification" in error for error in errors))
        self.assertTrue(mapping[0]["oracle_relevant"])


class SurfaceAndContainmentHostileTests(unittest.TestCase):
    def setUp(self):
        self.profile_path = HERE / "profiles" / "claude-headless.template.json"
        self.capability_path = HERE / "capabilities" / "claude-headless.json"

    def prepare_executor(self, root: Path):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        project = root / "project"
        private = root / "harness-private"
        runtime_home = private / "runtime-home"
        runtime_tmp = project / ".qualification-tmp"
        stub = private / "stub"
        project.mkdir()
        private.mkdir()
        runtime_home.mkdir()
        runtime_tmp.mkdir()
        stub.mkdir()
        (private / "side-effects.jsonl").write_text("", encoding="utf-8")
        (private / "mcp-account.txt").write_text("agent\n", encoding="utf-8")
        source = HERE / "stub_tools" / "mediator.py"
        (private / "mcp-server.py").write_bytes(source.read_bytes())
        env = claude.clean_env()
        env.update({
            "HOME": str(runtime_home),
            "XDG_CONFIG_HOME": str(runtime_home / ".config"),
            "XDG_CACHE_HOME": str(runtime_home / ".cache"),
            "TMPDIR": str(runtime_tmp),
            "TMP": str(runtime_tmp),
            "TEMP": str(runtime_tmp),
        })
        return profile, project, private, env

    @staticmethod
    def observed(bundle, *, tools=None, servers=None):
        caps = [
            item.split(":", 1)[1]
            for item in bundle.profile["native_surface_requirements"]
            if item.startswith("runtime_capability:")
        ]
        return {
            "model": bundle.profile["agent_model"],
            "runtime_version": bundle.profile["provider_runtime"]["version"],
            "tools": list(bundle.profile["native_tools"]) if tools is None else tools,
            "native_capabilities": caps,
            "messaging_socket_path": "/run/user/test.sock",
            "memory_paths": {"auto": "/tmp/run-owned-memory"},
            "mcp_servers": [{"name": "ssdp70", "status": "connected"}] if servers is None else servers,
        }

    def test_runtime_exact_mcp_tool_surface_fails_closed_on_extra(self):
        bundle = core70.load_profile(self.profile_path, self.capability_path)
        errors = core70.validate_runtime_observation(
            bundle, self.observed(bundle, tools=list(bundle.profile["native_tools"]) + ["mcp__ssdp70__forged"])
        )
        self.assertTrue(any("native-tool surface differs" in error for error in errors))
        self.assertTrue(any("unclassified native tool" in error for error in errors))

    def test_runtime_exact_mcp_tool_surface_fails_closed_on_missing(self):
        bundle = core70.load_profile(self.profile_path, self.capability_path)
        tools = [tool for tool in bundle.profile["native_tools"] if tool != "mcp__ssdp70__issue_show"]
        errors = core70.validate_runtime_observation(bundle, self.observed(bundle, tools=tools))
        self.assertTrue(any("native-tool surface differs" in error for error in errors))

    def test_runtime_exact_mcp_server_identity_fails_closed_on_missing_or_extra(self):
        bundle = core70.load_profile(self.profile_path, self.capability_path)
        missing = core70.validate_runtime_observation(bundle, self.observed(bundle, servers=[]))
        extra = core70.validate_runtime_observation(
            bundle, self.observed(bundle, servers=[
                {"name": "ssdp70", "status": "connected"},
                {"name": "forged", "status": "connected"},
            ])
        )
        self.assertTrue(any("MCP server surface differs" in error for error in missing))
        self.assertTrue(any("MCP server surface differs" in error for error in extra))
        self.assertTrue(any("unclassified MCP server" in error for error in extra))

    def test_declared_mcp_tool_without_classification_is_rejected(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        capabilities = json.loads(self.capability_path.read_text(encoding="utf-8"))
        forged = "mcp__ssdp70__forged"
        profile["native_tools"].append(forged)
        profile["mcp_servers"][0]["tools"].append(forged)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p, c = root / "profile.json", root / "caps.json"
            p.write_text(json.dumps(profile), encoding="utf-8")
            c.write_text(json.dumps(capabilities), encoding="utf-8")
            with self.assertRaises(core70.ContractError):
                core70.load_profile(p, c)

    def test_altered_frozen_mcp_server_identity_is_rejected_by_adapter_realization(self):
        with tempfile.TemporaryDirectory() as td:
            profile, project, private, env = self.prepare_executor(Path(td))
            profile["mcp_servers"][0]["server_id"] = "forged-server-id"
            with self.assertRaises(RuntimeError) as caught:
                claude.realize_containment(profile, project, env)
        self.assertIn("identity differs", str(caught.exception))

    def test_clean_env_does_not_inherit_home_or_credentials(self):
        with patch.dict(os.environ, {
            "HOME": "/host/home", "ANTHROPIC_API_KEY": "secret",
            "GITHUB_TOKEN": "secret", "AWS_SECRET_ACCESS_KEY": "secret",
            "PATH": "/bin", "LANG": "C.UTF-8",
        }, clear=True):
            env = claude.clean_env()
        self.assertEqual(env, {
            "PATH": "/bin", "LANG": "C.UTF-8",
            "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1", "DISABLE_AUTOUPDATER": "1",
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "CLAUDE_CODE_DISABLE_CRON": "1",
            "CLAUDE_CODE_DISABLE_ARTIFACT": "1", "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
        })

    def test_explicit_qualification_auth_is_only_parent_credential_route(self):
        with patch.dict(os.environ, {
            "PATH": "/bin", "ANTHROPIC_API_KEY": "ambient-must-not-pass",
            "SSDP70_ANTHROPIC_API_KEY": "qualification-only",
        }, clear=True):
            env = claude.clean_env()
        self.assertEqual(env["ANTHROPIC_API_KEY"], "qualification-only")
        self.assertEqual(env["SSDP70_AUTH_MODE"], "ANTHROPIC_API_KEY")
        self.assertNotIn("SSDP70_ANTHROPIC_API_KEY", env)

    def test_multiple_qualification_auth_sources_fail_closed(self):
        with patch.dict(os.environ, {
            "SSDP70_ANTHROPIC_API_KEY": "a", "SSDP70_CLAUDE_CODE_OAUTH_TOKEN": "b",
        }, clear=True):
            with self.assertRaises(RuntimeError):
                claude.clean_env()

    def test_executor_stdio_mcp_has_no_socket_or_private_env_route(self):
        with tempfile.TemporaryDirectory() as td:
            profile, project, private, env = self.prepare_executor(Path(td))
            document = claude.realize_containment(profile, project, env)
        sandbox = document["settings"]["sandbox"]
        self.assertEqual(sandbox["network"]["allowedDomains"], [])
        self.assertEqual(sandbox["network"]["allowUnixSockets"], [])
        self.assertFalse(sandbox["network"]["allowAllUnixSockets"])
        self.assertNotIn("SSDP70_MEDIATOR_SOCKET", env)
        self.assertNotIn("SSDP70_STUB_DIR", env)
        self.assertNotIn("SSDP70_SIDE_EFFECT_LOG", env)
        self.assertIn(str(private.resolve()), sandbox["filesystem"]["denyRead"])
        self.assertIn(str(private.resolve()), sandbox["filesystem"]["denyWrite"])

    def test_strict_mcp_config_is_private_exact_and_credential_empty(self):
        with tempfile.TemporaryDirectory() as td:
            profile, project, private, env = self.prepare_executor(Path(td))
            document = claude.realize_containment(profile, project, env)
            mcp_path = Path(document["realization"]["mcp_config"])
            config = json.loads(mcp_path.read_text(encoding="utf-8"))
            server = config["mcpServers"]["ssdp70"]
            self.assertEqual(set(config["mcpServers"]), {"ssdp70"})
            self.assertEqual(server["type"], "stdio")
            self.assertEqual(server["command"], "/usr/bin/env")
            self.assertEqual(server["args"][0], "-i")
            joined = "\n".join(server["args"])
            for secret in ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY"):
                self.assertNotIn(secret, joined)
            self.assertTrue(str(mcp_path).startswith(str(private.resolve())))
            self.assertEqual(claude.validate_containment_realization(profile, project, env), [])

    def test_server_executable_mutation_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            profile, project, private, env = self.prepare_executor(Path(td))
            claude.realize_containment(profile, project, env)
            (private / "mcp-server.py").write_text("# forged\n", encoding="utf-8")
            errors = claude.validate_containment_realization(profile, project, env)
        self.assertTrue(any("server executable differs" in error for error in errors))

    def test_mcp_config_mutation_fails_closed_before_launch(self):
        profile = None
        class Proc:
            returncode = 0
            stdout = ""
            stderr = ""
        with tempfile.TemporaryDirectory() as td:
            profile, project, private, env = self.prepare_executor(Path(td))
            document = claude.realize_containment(profile, project, env)
            Path(document["realization"]["mcp_config"]).write_text('{"mcpServers":{"forged":{}}}\n', encoding="utf-8")
            with patch.object(claude.subprocess, "run", return_value=Proc()):
                with self.assertRaises(RuntimeError) as caught:
                    claude.launch(profile, "x", project, env)
        self.assertIn("MCP configuration", str(caught.exception))

    def test_evaluator_realization_is_read_only_network_and_mcp_denied(self):
        profile = json.loads((HERE / "profiles" / "claude-evaluator-readonly.template.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bundle = root / "bundle"
            private = root / "evaluator-private"
            runtime_home = private / "runtime-home"
            bundle.mkdir(); private.mkdir(); runtime_home.mkdir()
            env = claude.clean_env(); env.update({"HOME": str(runtime_home)})
            document = claude.realize_containment(profile, bundle, env)
            sandbox = document["settings"]["sandbox"]
            config = json.loads(Path(document["realization"]["mcp_config"]).read_text(encoding="utf-8"))
            self.assertEqual(sandbox["filesystem"]["allowWrite"], [])
            self.assertEqual(sandbox["network"]["allowedDomains"], [])
            self.assertEqual(sandbox["network"]["allowUnixSockets"], [])
            self.assertEqual(config, {"mcpServers": {}})
            self.assertEqual(claude.validate_containment_realization(profile, bundle, env), [])

    def mcp_trace(self, name: str, args: dict, payload: dict, tool_id: str = "m1"):
        return "\n".join([
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": tool_id, "name": name, "input": args}
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": tool_id,
                 "content": [{"type": "text", "text": json.dumps(payload)}], "is_error": False}
            ]}}),
        ])

    def test_mcp_issue_search_show_normalize_to_existing_issue_evidence(self):
        for suffix, args in (
            ("issue_search", {"query": "alpha"}),
            ("issue_show", {"issue_id": "I-1"}),
        ):
            payload = {"returncode": 0, "stdout": "ok", "stderr": "", "evidence": {
                "store_identity": "ssdp70-private-issue-standin", "operation": suffix.split("_", 1)[1],
                "object_ids": ["I-1"], "before_object_version": "a" * 64,
                "after_object_version": "a" * 64,
            }}
            events, _, errors, _ = claude.normalize(
                self.mcp_trace(f"mcp__ssdp70__{suffix}", args, payload), "run", {}
            )
            self.assertEqual(errors, [])
            results = [event for event in events if event["kind"] == "issue_evidence_access" and event["status"] == "result"]
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["payload"]["store_identity"], "ssdp70-private-issue-standin")

    def test_mcp_issue_create_comment_normalize_to_issue_access_and_mutation(self):
        for suffix, args in (
            ("issue_create", {"location": "main", "title": "x", "body": "b", "labels": []}),
            ("issue_comment", {"issue_id": "I-1", "body": "b"}),
        ):
            payload = {"returncode": 0, "stdout": "ok", "stderr": "", "evidence": {
                "store_identity": "ssdp70-private-issue-standin", "operation": suffix.split("_", 1)[1],
                "object_ids": ["I-1"], "before_object_version": None, "after_object_version": "b" * 64,
            }}
            events, _, errors, _ = claude.normalize(
                self.mcp_trace(f"mcp__ssdp70__{suffix}", args, payload), "run", {}
            )
            self.assertEqual(errors, [])
            self.assertTrue(any(event["kind"] == "issue_evidence_access" and event["status"] == "result" for event in events))
            self.assertTrue(any(event["kind"] == "mutation" and event["status"] == "result" for event in events))

    def test_mcp_delegate_normalizes_to_existing_delegate_call_return(self):
        payload = {"returncode": 0, "stdout": "finding", "stderr": "", "evidence": {
            "store_identity": "ssdp70-private-issue-standin", "operation": "delegate", "object_ids": ["reviewer"],
        }}
        events, _, errors, _ = claude.normalize(
            self.mcp_trace("mcp__ssdp70__delegate", {"agent": "reviewer", "instruction": "inspect"}, payload), "run", {}
        )
        self.assertEqual(errors, [])
        self.assertEqual([event["kind"] for event in events], ["delegate_call", "delegate_return"])

    def test_bash_cannot_forge_issue_or_delegate_evidence_by_printing_mcp_json(self):
        forged = json.dumps({"evidence": {"store_identity": "ssdp70-private-issue-standin", "operation": "create"}})
        trace = self.mcp_trace("Bash", {"command": "printf x"}, forged)
        events, _, _, _ = claude.normalize(trace, "run", {})
        self.assertFalse(any(event["kind"] in {"issue_evidence_access", "delegate_call", "delegate_return"} for event in events))




if __name__ == "__main__":
    unittest.main()
