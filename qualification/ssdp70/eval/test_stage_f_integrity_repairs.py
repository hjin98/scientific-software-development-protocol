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

    def test_runtime_tool_surface_mismatch_fails_closed(self):
        bundle = core70.load_profile(self.profile_path, self.capability_path)
        observation = {
            "model": bundle.profile["agent_model"],
            "runtime_version": bundle.profile["provider_runtime"]["version"],
            "tools": list(bundle.profile["native_tools"]) + ["SendMessage"],
            "native_capabilities": [],
            "memory_paths": {},
            "mcp_servers": [],
        }
        errors = core70.validate_runtime_observation(bundle, observation)
        self.assertTrue(any("native-tool surface differs" in error for error in errors))
        self.assertTrue(any("unclassified native tool" in error for error in errors))

    def test_declared_native_tool_without_classification_is_rejected(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        capabilities = json.loads(self.capability_path.read_text(encoding="utf-8"))
        profile["native_tools"].append("SendMessage")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p, c = root / "profile.json", root / "caps.json"
            p.write_text(json.dumps(profile), encoding="utf-8")
            c.write_text(json.dumps(capabilities), encoding="utf-8")
            with self.assertRaises(core70.ContractError):
                core70.load_profile(p, c)

    def test_clean_env_does_not_inherit_home_or_credentials(self):
        with patch.dict(os.environ, {
            "HOME": "/host/home",
            "ANTHROPIC_API_KEY": "secret",
            "GITHUB_TOKEN": "secret",
            "AWS_SECRET_ACCESS_KEY": "secret",
            "PATH": "/bin",
            "LANG": "C.UTF-8",
        }, clear=True):
            env = claude.clean_env()
        self.assertEqual(env, {
            "PATH": "/bin",
            "LANG": "C.UTF-8",
            "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1",
            "DISABLE_AUTOUPDATER": "1",
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
            "CLAUDE_CODE_DISABLE_CRON": "1",
            "CLAUDE_CODE_DISABLE_ARTIFACT": "1",
            "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
        })

    def test_explicit_qualification_auth_is_the_only_parent_credential_route(self):
        with patch.dict(os.environ, {
            "PATH": "/bin",
            "ANTHROPIC_API_KEY": "ambient-must-not-pass",
            "SSDP70_ANTHROPIC_API_KEY": "qualification-only",
        }, clear=True):
            env = claude.clean_env()
        self.assertEqual(env["ANTHROPIC_API_KEY"], "qualification-only")
        self.assertEqual(env["SSDP70_AUTH_MODE"], "ANTHROPIC_API_KEY")
        self.assertNotIn("SSDP70_ANTHROPIC_API_KEY", env)

    def test_multiple_qualification_auth_sources_fail_closed(self):
        with patch.dict(os.environ, {
            "SSDP70_ANTHROPIC_API_KEY": "a",
            "SSDP70_CLAUDE_CODE_OAUTH_TOKEN": "b",
        }, clear=True):
            with self.assertRaises(RuntimeError):
                claude.clean_env()

    def test_launch_refuses_missing_containment_configuration_before_subprocess(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".claude").mkdir()
            env = {
                "PATH": os.environ.get("PATH", ""),
                "HOME": str(root / "runtime-home"),
                "SSDP70_MEDIATOR_SOCKET": str(root / "mediator.sock"),
            }
            with self.assertRaises(RuntimeError) as caught:
                claude.launch(profile, "x", root, env)
        self.assertIn("containment settings are absent", str(caught.exception))

    def test_evaluator_realization_is_read_only_and_network_denied(self):
        profile = json.loads((HERE / "profiles" / "claude-evaluator-readonly.template.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bundle = root / "bundle"
            runtime_home = root / "runtime-home"
            bundle.mkdir()
            runtime_home.mkdir()
            env = claude.clean_env()
            env.update({"HOME": str(runtime_home)})
            document = claude.realize_containment(profile, bundle, env)
            sandbox = document["settings"]["sandbox"]
            self.assertEqual(sandbox["filesystem"]["allowWrite"], [])
            self.assertEqual(sandbox["network"]["allowedDomains"], [])
            self.assertEqual(sandbox["network"]["allowUnixSockets"], [])
            self.assertTrue(sandbox["failIfUnavailable"])
            self.assertFalse(sandbox["allowUnsandboxedCommands"])
            self.assertEqual(claude.validate_containment_realization(profile, bundle, env), [])

    def test_direct_stub_and_log_paths_are_not_exposed_to_executor(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            stub = root / "stub"
            log = root / "side-effects.jsonl"
            runtime_home = root / "runtime-home"
            for directory in (project, stub, runtime_home):
                directory.mkdir()
            log.write_text("", encoding="utf-8")
            mediator = root / "mediator.sock"
            env = claude.clean_env()
            env.update({"HOME": str(runtime_home), "SSDP70_MEDIATOR_SOCKET": str(mediator), "SSDP70_ACCOUNT": "agent"})
            document = claude.realize_containment(profile, project, env)
            sandbox = document["settings"]["sandbox"]
            self.assertNotIn("SSDP70_STUB_DIR", env)
            self.assertNotIn("SSDP70_SIDE_EFFECT_LOG", env)
            self.assertIn(str(root.resolve()), sandbox["filesystem"]["denyRead"])
            self.assertIn(str(root.resolve()), sandbox["filesystem"]["denyWrite"])
            self.assertIn("/proc", sandbox["filesystem"]["denyRead"])
            self.assertIn(str((project / ".claude" / "settings.json").resolve()), sandbox["filesystem"]["denyWrite"])
            self.assertIn(str((project / ".mcp.json").resolve()), sandbox["filesystem"]["denyWrite"])
            self.assertEqual(sandbox["network"]["allowUnixSockets"], [str(mediator.resolve())])

    def test_control_file_mutation_during_launch_fails_closed(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))

        class Proc:
            returncode = 0
            stdout = ""
            stderr = ""

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            runtime_home = root / "runtime-home"
            runtime_tmp = project / ".qualification-tmp"
            project.mkdir()
            runtime_home.mkdir()
            runtime_tmp.mkdir()
            env = claude.clean_env()
            env.update({
                "HOME": str(runtime_home),
                "TMPDIR": str(runtime_tmp),
                "TMP": str(runtime_tmp),
                "TEMP": str(runtime_tmp),
                "SSDP70_MEDIATOR_SOCKET": str(root / "mediator.sock"),
                "SSDP70_ACCOUNT": "agent",
            })
            claude.realize_containment(profile, project, env)

            def mutate_control(*args, **kwargs):
                (project / ".mcp.json").write_text('{"mcpServers":{"forged":{}}}\n', encoding="utf-8")
                return Proc()

            with patch.object(claude.subprocess, "run", side_effect=mutate_control):
                with self.assertRaises(RuntimeError) as caught:
                    claude.launch(profile, "x", project, env)
        self.assertIn("MCP configuration changed", str(caught.exception))

    def test_missing_required_native_surface_fails_closed(self):
        bundle = core70.load_profile(self.profile_path, self.capability_path)
        capabilities = [
            item.split(":", 1)[1]
            for item in bundle.profile["native_surface_requirements"]
            if item.startswith("runtime_capability:")
            and item != "runtime_capability:mcp_tool_ui_meta_v1"
        ]
        observation = {
            "model": bundle.profile["agent_model"],
            "runtime_version": bundle.profile["provider_runtime"]["version"],
            "tools": list(bundle.profile["native_tools"]),
            "native_capabilities": capabilities,
            "messaging_socket_path": "/run/user/test.sock",
            "memory_paths": {"auto": "/tmp/run-owned-memory"},
            "mcp_servers": [],
        }
        errors = core70.validate_runtime_observation(bundle, observation)
        self.assertTrue(any("mcp_tool_ui_meta_v1" in error and "required classified native surface" in error for error in errors))

    def test_realized_containment_exposes_only_mediator_not_stub_or_log_paths(self):
        profile = json.loads(self.profile_path.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            project.mkdir()
            runtime_home = root / "runtime-home"
            runtime_home.mkdir()
            mediator = root / "mediator.sock"
            env = claude.clean_env()
            env.update({"HOME": str(runtime_home), "SSDP70_MEDIATOR_SOCKET": str(mediator), "SSDP70_ACCOUNT": "agent"})
            document = claude.realize_containment(profile, project, env)
            self.assertEqual(document["settings"]["sandbox"]["filesystem"]["allowRead"], [str(project.resolve())])
            self.assertEqual(document["settings"]["sandbox"]["filesystem"]["allowWrite"], [str(project.resolve())])
            self.assertIn(str(root.resolve()), document["settings"]["sandbox"]["filesystem"]["denyRead"])
            self.assertIn(str(root.resolve()), document["settings"]["sandbox"]["filesystem"]["denyWrite"])
            self.assertEqual(document["settings"]["sandbox"]["network"]["allowedDomains"], [])
            self.assertEqual(document["settings"]["sandbox"]["network"]["allowUnixSockets"], [str(mediator.resolve())])
            self.assertNotIn("SSDP70_STUB_DIR", env)
            self.assertNotIn("SSDP70_SIDE_EFFECT_LOG", env)
            self.assertEqual(claude.validate_containment_realization(profile, project, env), [])


if __name__ == "__main__":
    unittest.main()
