import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import core70
from adapters import claude


HERE = Path(__file__).resolve().parent
TRACE_ROOT = HERE.parent / "stage-f-prerun-actual-profile-recheck-2026-09-28" / "native-traces"


class RetainedTraceRepairTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.skills = self.root / ".claude" / "skills"
        self.skill = self.skills / "software-implementation" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)

    def tearDown(self):
        self.td.cleanup()

    def _skill_trace_and_context(self):
        trace = (TRACE_ROOT / "skill-probe.jsonl").read_text(encoding="utf-8")
        synthetic = None
        for line in trace.splitlines():
            row = json.loads(line)
            if row.get("type") == "user" and row.get("isSynthetic") is True:
                synthetic = row
                break
        self.assertIsNotNone(synthetic)
        text = synthetic["message"]["content"][0]["text"]
        prefix, body = text.split("\n\n", 1)
        self.assertTrue(prefix.startswith("Base directory for this skill: "))
        self.skill.write_text(body, encoding="utf-8")
        context = {
            "project": str(self.root),
            "skills_root": str(self.skills),
            "package_identity": {
                "arm": "p70",
                "commit": "db94a2dfb7fef480f37227eab5c45256e89901b8",
                "version": "7.0.0",
                "package_sha256": "b" * 64,
            },
        }
        return trace, context, body

    def test_retained_21283_system_subtypes_have_reviewed_non_oracle_classification(self):
        trace, context, _ = self._skill_trace_and_context()
        events, mapping, errors, count = claude.normalize(trace, "retained-skill", context)
        self.assertEqual(errors, [])
        self.assertEqual(core70.validate_completeness_map(count, mapping, events), [])
        classifications = {row["classification"] for row in mapping}
        self.assertIn("reviewed-non-oracle-system:thinking_tokens", classifications)
        self.assertIn("reviewed-non-oracle-system:post_turn_summary", classifications)
        reviewed = [
            row for row in mapping
            if row["classification"].startswith("reviewed-non-oracle-system:")
        ]
        self.assertTrue(reviewed)
        self.assertTrue(all(row["oracle_relevant"] is False for row in reviewed))

    def test_retained_skill_injection_binds_exact_installed_bytes_for_burden_claims(self):
        trace, context, body = self._skill_trace_and_context()
        events, _, errors, _ = claude.normalize(trace, "retained-skill-bytes", context)
        self.assertEqual(errors, [])
        injected = [
            event for event in events
            if event.get("kind") == "resource_access"
            and (event.get("payload") or {}).get("operation") == "skill-injected-body"
        ]
        self.assertEqual(len(injected), 1)
        payload = injected[0]["payload"]
        exact = self.skill.read_bytes()
        self.assertEqual(payload["resource_bytes"], len(exact))
        self.assertEqual(payload["resource_sha256"], hashlib.sha256(exact).hexdigest())
        self.assertEqual(payload["result_content"].replace("\r\n", "\n").rstrip("\n"),
                         body.replace("\r\n", "\n").rstrip("\n"))
        self.assertEqual(core70.validate_claim_observability(events, ["T1-active-byte"]), [])

    def test_unknown_system_subtype_remains_fail_closed(self):
        trace = json.dumps({"type": "system", "subtype": "future-unknown"})
        _, mapping, errors, count = claude.normalize(trace, "unknown-system", {
            "project": str(self.root), "skills_root": str(self.skills),
            "package_identity": {"package_sha256": "c" * 64},
        })
        self.assertEqual(count, 1)
        self.assertTrue(errors)
        self.assertTrue(mapping[0]["oracle_relevant"])


class ContainmentHostileTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.runtime = self.root / "runtime-copy"
        self.runtime.write_text("runtime", encoding="utf-8")
        self.profile = {
            "containment_policy": {
                "kind": "bwrap-plus-claude-sandbox-v1",
                "workspace_mode": "read-write",
                "mediator_required": True,
            },
            "provider_runtime": {"executable": "claude"},
        }
        self.socket = self.root / "mediator.sock"
        self.socket.touch()
        self.env = {
            "SSDP70_MEDIATOR_SOCKET": str(self.socket),
            "SSDP70_ACCOUNT": "agent-account",
            "_SSDP70_RUNTIME_COPY": str(self.runtime),
        }

    def tearDown(self):
        self.td.cleanup()

    def test_containment_config_absence_is_blocking(self):
        def which(name):
            return "/usr/bin/bwrap" if name == "bwrap" else "/usr/bin/claude"
        with patch.object(claude.shutil, "which", side_effect=which):
            errors = claude.validate_containment_realization(self.profile, self.project, self.env)
        self.assertTrue(any("settings are absent" in error for error in errors))

    def test_containment_settings_fail_closed_and_strict_network(self):
        document = claude._containment_document(self.profile, self.project, self.env)
        sandbox = document["sandbox"]
        network = sandbox["network"]
        self.assertIs(sandbox["failIfUnavailable"], True)
        self.assertIs(sandbox["allowUnsandboxedCommands"], False)
        self.assertEqual(sandbox["excludedCommands"], [])
        self.assertIs(network["strictAllowlist"], True)
        self.assertEqual(network["allowedDomains"], [])
        self.assertIs(network["allowAllUnixSockets"], True)
        self.assertEqual(network["allowUnixSockets"], [])
        self.assertIn("only qualification mediator", document["ssdp70Containment"]["unix_socket_policy"])

    def test_env_leakage_is_blocking(self):
        def which(name):
            return "/usr/bin/bwrap" if name == "bwrap" else "/usr/bin/claude"
        claude_dir = self.project / ".claude"
        claude_dir.mkdir()
        expected = claude._containment_document(self.profile, self.project, self.env)
        (claude_dir / "settings.json").write_text(json.dumps(expected), encoding="utf-8")
        leaked = dict(self.env)
        leaked["AWS_SECRET_ACCESS_KEY"] = "not-a-real-secret"
        with patch.object(claude.shutil, "which", side_effect=which):
            errors = claude.validate_containment_realization(self.profile, self.project, leaked)
        self.assertTrue(any("AWS_SECRET_ACCESS_KEY" in error for error in errors))

    def test_executor_has_no_direct_stub_or_log_path_contract(self):
        issues = (HERE / "stub_tools" / "issues.py").read_text(encoding="utf-8")
        delegate = (HERE / "stub_tools" / "delegate.py").read_text(encoding="utf-8")
        self.assertNotIn("SSDP70_STUB_DIR", issues + delegate)
        self.assertNotIn("SSDP70_SIDE_EFFECT_LOG", issues + delegate)
        self.assertIn("SSDP70_MEDIATOR_SOCKET", issues + delegate)

    def test_bwrap_surface_mounts_only_mediator_socket_not_backing_state(self):
        def which(name):
            return "/usr/bin/bwrap" if name == "bwrap" else "/usr/bin/claude"
        with patch.object(claude.shutil, "which", side_effect=which):
            cmd = claude._bwrap_prefix(self.profile, self.project, self.env, self.runtime)
        joined = " ".join(cmd)
        self.assertIn("/run/ssdp70/mediator.sock", joined)
        self.assertNotIn("SSDP70_STUB_DIR", joined)
        self.assertNotIn("side-effects.jsonl", joined)


class ProfileSurfaceTests(unittest.TestCase):
    def test_evaluator_profile_is_read_only_and_exact_surface(self):
        profile = json.loads((HERE / "profiles" / "claude-evaluator-readonly.template.json").read_text(encoding="utf-8"))
        caps = json.loads((HERE / "capabilities" / "claude-evaluator-readonly.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["native_tools"], ["Read", "Glob", "Grep"])
        self.assertEqual(profile["containment_policy"]["workspace_mode"], "read-only")
        self.assertEqual(caps["capabilities"]["workspace_mutation"]["decision"], "DENY")
        self.assertEqual(caps["capabilities"]["process_execution"]["decision"], "DENY")
        self.assertEqual(caps["capabilities"]["network_remote_service"]["decision"], "DENY")
        self.assertEqual(caps["capabilities"]["credential_secret_service_account"]["decision"], "DENY")


if __name__ == "__main__":
    unittest.main()
