"""Regression tests for the Stage F runner-admission v4 repair (D-A..D-E, C-1).

D-A..D-E use the real Claude Code 2.1.284 traces retained in
`stage-f-runner-admission-v4-inputs-2026-09-29/` through the real adapter normalizer, core validators
and (for the end-to-end class) the real harness. C-1 is asserted at the settings/permission-rule level
only: offline tests cannot prove that the runtime honors the settings; that is verified live by
`live_verify_v4.py` and reported in the repair record.
"""
from __future__ import annotations

import ast
import copy
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import core70
import harness70
import v4_support
from adapters import claude

HERE = Path(__file__).resolve().parent
V4_ROOT = HERE.parent / "stage-f-runner-admission-v4-repair-2026-09-29"
FIXTURE_FILES = {"README.md", "data", "src", "tests"}


def normalize_run(run: str, root: Path, skill_data: bytes | None = None, context: dict | None = None):
    v4_support.install_real_skill(root, data=skill_data)
    trace = v4_support.retarget(run, root)
    ctx = v4_support.package_context(root) if context is None else context
    events, mapping, errors, count = claude.normalize(trace, f"run-{run}", ctx)
    return events, mapping, errors, count, trace


def all_errors(run: str, root: Path, **kwargs):
    events, mapping, errors, count, _ = normalize_run(run, root, **kwargs)
    return (
        errors
        + core70.validate_normalized_events(events, f"run-{run}")
        + core70.validate_completeness_map(count, mapping, events)
    ), events, mapping


class SkillInjectionBindingTests(unittest.TestCase):
    """D-A: injected skill body == installed SKILL.md minus its leading frontmatter block."""

    def test_rule_definition_is_precise(self):
        strip = claude.strip_skill_frontmatter
        self.assertEqual(strip("---\nname: a\n---\n\n# T\nbody\n"), "# T\nbody\n")
        self.assertEqual(strip("---\nname: a\n---\n# T\n"), "# T\n")
        self.assertEqual(strip("---\n---\n\n\n# T"), "# T")  # only leading newlines are removed
        self.assertEqual(strip("---\nk: v\n---\n  indented\n"), "  indented\n")  # spaces are not trimmed
        self.assertEqual(strip("---\nk: v\n---\nbody\n\n\n"), "body\n\n\n")  # no trailing trim
        self.assertEqual(strip("---\nk: ---\n---\nbody"), "body")  # `---` inside a value line is not a delimiter
        for broken in ("no frontmatter\n", "---\nk: v\nnever closed\n", "﻿---\nk: v\n---\nbody", "---\r\nk: v\r\n---\r\nbody"):
            with self.assertRaises(ValueError):
                strip(broken)

    def test_real_ping_trace_binds_exactly_and_maps_every_oracle_relevant_event(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            errors, events, mapping = all_errors("CHK-PING-p70-r0", root)
            self.assertEqual(errors, [])
            self.assertFalse([row for row in mapping if row["oracle_relevant"] and not row["mapped_event_ids"]])
            injected = [e for e in events if (e["payload"] or {}).get("operation") == "skill-injected-body"]
            self.assertEqual(len(injected), 1)
            payload = injected[0]["payload"]
            installed = (root / ".claude/skills/software-implementation/SKILL.md").read_bytes()
            self.assertEqual(payload["input"]["injected_body_rule"], claude.SKILL_BODY_RULE)
            self.assertEqual(payload["resource_bytes"], len(installed))
            self.assertEqual(payload["resource_bytes"] > len(payload["result_content"].encode()), True)
            self.assertEqual(payload["result_content"], claude.strip_skill_frontmatter(installed.decode()))
            self.assertEqual(core70.validate_claim_observability(events, ["t1", "t7", "t8"]), [])

    def test_real_turn_trace_no_longer_fails_on_skill_binding_or_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            errors, _, _ = all_errors("CHK-TURN-p70-r0", Path(td))
            self.assertEqual(errors, [])

    def mutated(self, transform):
        installed = v4_support.installed_skill_bytes("software-implementation").decode("utf-8")
        with tempfile.TemporaryDirectory() as td:
            errors, _, mapping = all_errors("CHK-PING-p70-r0", Path(td), skill_data=transform(installed).encode("utf-8"))
        return errors, mapping

    def assertRejected(self, transform, needle="does not equal the installed SKILL.md"):
        errors, mapping = self.mutated(transform)
        self.assertTrue(any(needle in error for error in errors), errors)
        # fail closed twice: the binding error and an unmapped oracle-relevant native event
        self.assertTrue(any("is unmapped" in error for error in errors), errors)

    def test_any_body_edit_fails(self):
        self.assertRejected(lambda text: text.replace("Software Implementation", "Software  Implementation", 1))
        self.assertRejected(lambda text: text.replace("D4", "D5", 1))
        self.assertRejected(lambda text: text[:-2])  # last body bytes removed

    def test_extra_text_fails(self):
        self.assertRejected(lambda text: text + "\nextra trailing line\n")
        self.assertRejected(lambda text: text.replace("\n---\n\n", "\n---\n\nInjected preamble.\n\n", 1))

    def test_missing_body_fails(self):
        def frontmatter_only(text):
            return text[: text.index("\n---\n", 4) + 5]
        self.assertRejected(frontmatter_only)

    def test_different_skill_fails(self):
        other = v4_support.installed_skill_bytes("software-design").decode("utf-8")
        self.assertRejected(lambda _text: other)

    def test_frontmatter_edits_do_not_change_the_body_binding_but_missing_frontmatter_fails(self):
        with tempfile.TemporaryDirectory() as td:
            errors, _, _ = all_errors(
                "CHK-PING-p70-r0", Path(td),
                skill_data=v4_support.installed_skill_bytes("software-implementation").replace(b"name: software-implementation", b"name: renamed", 1),
            )
            self.assertEqual(errors, [])
        errors, _ = self.mutated(lambda text: text[text.index("\n---\n", 4) + 5:])
        self.assertTrue(any("does not start with a frontmatter block" in error for error in errors), errors)

    def test_circular_v3_test_pattern_is_rejected(self):
        """The v3 test installed the injected body itself; that is not the installed file and must fail."""
        injected = claude.strip_skill_frontmatter(v4_support.installed_skill_bytes("software-implementation").decode())
        errors, _ = self.mutated(lambda _text: injected)
        self.assertTrue(any("does not start with a frontmatter block" in error for error in errors), errors)

    def test_prefix_and_substring_matching_is_not_accepted(self):
        installed = v4_support.installed_skill_bytes("software-implementation").decode("utf-8")
        body = claude.strip_skill_frontmatter(installed)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            v4_support.install_real_skill(root)
            trace = v4_support.retarget("CHK-PING-p70-r0", root)
            rows = [json.loads(line) for line in trace.splitlines()]
            synthetic = next(row for row in rows if row.get("isSynthetic") is True)
            block = synthetic["message"]["content"][0]
            prefix_line, real_body = block["text"].split("\n\n", 1)
            self.assertEqual(real_body, body)
            for label, altered in (
                ("truncated to a prefix", real_body[: len(real_body) // 2]),
                ("expected body embedded in longer text", "leading noise\n" + real_body),
                ("expected body followed by more text", real_body + "trailing noise"),
                ("empty body", ""),
            ):
                block["text"] = prefix_line + "\n\n" + altered
                text = "\n".join(json.dumps(row) for row in rows)
                events, mapping, errors, count = claude.normalize(text, "x", v4_support.package_context(root))
                self.assertTrue(errors, label)
                self.assertNotIn("skill-injected-body", [(e["payload"] or {}).get("operation") for e in events], label)

    def test_base_directory_binding_is_kept_and_names_the_selected_skill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            v4_support.install_real_skill(root)
            trace = v4_support.retarget("CHK-PING-p70-r0", root)
            wrong = trace.replace(
                f"Base directory for this skill: {root}/.claude/skills/software-implementation",
                f"Base directory for this skill: {root}/.claude/skills/software-design",
            )
            self.assertNotEqual(wrong, trace)
            _, _, errors, _ = claude.normalize(wrong, "x", v4_support.package_context(root))
            self.assertTrue(any("declares base directory" in error for error in errors), errors)
            missing = trace.replace("Base directory for this skill: ", "Working directory: ")
            _, _, errors, _ = claude.normalize(missing, "x", v4_support.package_context(root))
            self.assertTrue(any("lacks base-directory binding" in error for error in errors), errors)

    def test_non_simple_skill_name_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            v4_support.install_real_skill(root)
            trace = v4_support.retarget("CHK-PING-p70-r0", root)
            rows = [json.loads(line) for line in trace.splitlines()]
            for row in rows:
                if row.get("type") == "assistant":
                    for block in row["message"]["content"]:
                        if block.get("name") == "Skill":
                            block["input"]["skill"] = "../software-implementation"
            forged = "\n".join(json.dumps(row) for row in rows)
            self.assertNotEqual(forged, trace)
            _, _, errors, _ = claude.normalize(forged, "x", v4_support.package_context(root))
            self.assertTrue(any("non-simple skill name" in error for error in errors), errors)


class SearchToolIdentityTests(unittest.TestCase):
    """D-B: every resource_access has a complete identity plus the full query/action input."""

    def test_real_pathless_grep_and_glob_have_project_root_identity(self):
        for run, tool in (("N21-grep-no-path-p70-r0", "Grep"), ("N22-glob-no-path-p70-r0", "Glob")):
            project = v4_support.recorded_project(run)
            trace = v4_support.trace_text(run)
            native = [
                block["input"] for row in v4_support.raw_rows(run) if row.get("type") == "assistant"
                for block in row["message"]["content"] if block.get("type") == "tool_use" and block["name"] == tool
            ]
            self.assertTrue(native)
            self.assertNotIn("path", native[0])  # the real call carried no path
            events, mapping, errors, count = claude.normalize(trace, "r", v4_support.package_context(Path(project)))
            self.assertEqual(errors, [], run)
            self.assertEqual(core70.validate_normalized_events(events, "r"), [], run)
            self.assertEqual(core70.validate_completeness_map(count, mapping, events), [], run)
            reads = [e for e in events if e["kind"] == "resource_access"]
            self.assertEqual(len(reads), 2)  # start + result
            for event in reads:
                payload = event["payload"]
                self.assertEqual(payload["resource_identity"], project)
                self.assertEqual(payload["resource_identity_source"], "default-search-root-run-project")
                self.assertEqual(payload["search_root"], project)
                self.assertEqual(payload["input"], native[0])  # pattern/options kept verbatim
                self.assertEqual(payload["operation"], tool.lower())
            self.assertEqual(reads[1]["status"], "result")
            self.assertTrue(reads[1]["payload"]["result_reference"].startswith("trace:"))
            self.assertRegex(reads[1]["payload"]["result_sha256"], r"^[0-9a-f]{64}$")

    def test_real_turn_trace_search_tools_validate(self):
        with tempfile.TemporaryDirectory() as td:
            errors, events, _ = all_errors("CHK-TURN-p70-r0", Path(td))
            self.assertEqual(errors, [])
            searches = [e for e in events if e["kind"] == "resource_access" and e["payload"]["operation"] in {"grep", "glob"}]
            self.assertTrue(searches)
            self.assertTrue(all(isinstance(e["payload"]["resource_identity"], str) and e["payload"]["resource_identity"] for e in searches))

    def test_missing_identity_is_never_silent(self):
        run = "N21-grep-no-path-p70-r0"
        trace = v4_support.trace_text(run)
        # no project in the normalization context: the identity cannot be established
        events, mapping, errors, count = claude.normalize(trace, "r", {})
        self.assertTrue(any("has no resource identity" in error for error in errors), errors)
        self.assertTrue(any(e["kind"] == "resource_access" and e["payload"]["resource_identity"] is None for e in events))
        core = core70.validate_normalized_events(events, "r")
        self.assertTrue(any("resource_identity is invalid" in error for error in core), core)
        # a Read without a file path is equally refused
        forged = json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "t1", "name": "Read", "input": {}}]}})
        result = json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "x"}]}})
        _, _, errors, _ = claude.normalize(forged + "\n" + result, "r", v4_support.package_context(Path("/nonexistent-project")))
        self.assertTrue(any("has no resource identity" in error for error in errors), errors)
        # core validator alone: null, empty and non-string identities are all invalid
        for value in (None, "", 0, ["x"]):
            payload = {
                "operation": "grep", "resource_identity": value, "input": {}, "tool_use_id": "t", "result_status": "pending",
                "result_reference": None, "result_sha256": None, "resolved_package_identity": None,
                "resource_sha256": None, "resource_bytes": None,
            }
            self.assertTrue(core70._validate_event_payload("resource_access", "start", payload, 0))

    def test_explicit_paths_keep_their_identity(self):
        rows = []
        for tool, data in (("Grep", {"pattern": "x", "path": "src"}), ("Glob", {"pattern": "*.py", "path": "/abs/dir"}), ("Read", {"file_path": "/abs/f.py"})):
            rows.append(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t-{tool}", "name": tool, "input": data}]}}))
            rows.append(json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"t-{tool}", "content": "x"}]}}))
        events, _, errors, _ = claude.normalize("\n".join(rows), "r", {"project": "/tmp/p"})
        self.assertEqual(errors, [])
        starts = [e["payload"] for e in events if e["kind"] == "resource_access" and e["status"] == "start"]
        self.assertEqual([p["resource_identity"] for p in starts], ["src", "/abs/dir", "/abs/f.py"])
        self.assertEqual([p["search_root"] for p in starts], ["/tmp/p/src", "/abs/dir", None])


class BlockedAttemptTests(unittest.TestCase):
    """D-D: the native permission_denied system event is classified and retained as a blocked attempt."""

    def normalized(self, run):
        with tempfile.TemporaryDirectory() as td:
            return all_errors(run, Path(td))

    def test_real_permission_denied_traces_are_retained_as_blocked_attempts(self):
        for run in ("N02-cat-custody-file-Bash-p70-r0", "N05-list-host-home-p70-r0"):
            errors, events, mapping = self.normalized(run)
            self.assertEqual(errors, [], run)
            raw = [r for r in v4_support.raw_rows(run) if r.get("type") == "system" and r.get("subtype") == "permission_denied"]
            self.assertEqual(len(raw), 1)
            row = next(m for m in mapping if m["classification"] == "permission-decision:permission_denied")
            self.assertTrue(row["oracle_relevant"])
            actions = [e for e in events if e["kind"] == "tool_action"]
            start, result = actions[0], actions[-1]
            self.assertEqual((start["status"], result["status"]), ("start", "error"))
            self.assertEqual(row["mapped_event_ids"], [start["event_id"], result["event_id"]])
            payload = result["payload"]
            self.assertIs(payload["blocked"], True)
            self.assertEqual(payload["blocked_reason"], "runtime-permission-denied")
            self.assertEqual(payload["result_status"], "error")
            self.assertEqual(payload["permission_decision"]["message"], raw[0]["message"])
            self.assertEqual(payload["permission_decision"]["decision_reason_type"], raw[0]["decision_reason_type"])
            self.assertEqual(payload["permission_decision"]["tool_use_id"], raw[0]["tool_use_id"])
            self.assertEqual(payload["non_execution_kind"], "user-rejected")
            native_input = next(
                b["input"] for r in v4_support.raw_rows(run) if r.get("type") == "assistant"
                for b in r["message"]["content"] if b.get("type") == "tool_use"
            )
            self.assertEqual(payload["input"], native_input)  # complete action input retained
            self.assertEqual(start["payload"]["input"], native_input)
            self.assertNotEqual(result["status"], "result")  # never treated as success
            # the retained attempt reaches tool-calls exactly like any tool action
            self.assertIn(result["kind"], {"tool_action"})

    def test_permission_denied_for_unknown_or_mismatched_tool_use_fails_closed(self):
        run = "N02-cat-custody-file-Bash-p70-r0"
        rows = v4_support.raw_rows(run)
        index = next(i for i, r in enumerate(rows) if r.get("subtype") == "permission_denied")
        for label, change, needle in (
            ("unknown id", {"tool_use_id": "toolu_unknown"}, "no matching pending tool use"),
            ("wrong tool", {"tool_name": "Write"}, "names tool 'Write'"),
        ):
            forged = copy.deepcopy(rows)
            forged[index].update(change)
            text = "\n".join(json.dumps(r) for r in forged)
            with tempfile.TemporaryDirectory() as td:
                events, mapping, errors, count = claude.normalize(text, "r", v4_support.package_context(Path(td)))
            self.assertTrue(any(needle in e for e in errors), (label, errors))
            self.assertTrue(core70.validate_completeness_map(count, mapping, events) or errors)

    def test_denied_tool_that_reports_success_is_contradictory_evidence(self):
        run = "N02-cat-custody-file-Bash-p70-r0"
        rows = v4_support.raw_rows(run)
        forged = copy.deepcopy(rows)
        result_row = next(r for r in forged if r.get("type") == "user")
        result_row["message"]["content"][0]["is_error"] = False
        with tempfile.TemporaryDirectory() as td:
            _, _, errors, _ = claude.normalize("\n".join(json.dumps(r) for r in forged), "r", v4_support.package_context(Path(td)))
        self.assertTrue(any("denied by a runtime permission decision but reports a successful result" in e for e in errors), errors)

    def test_denied_tool_without_result_is_still_reported_missing(self):
        run = "N05-list-host-home-p70-r0"
        rows = [r for r in v4_support.raw_rows(run) if r.get("type") != "user"]
        with tempfile.TemporaryDirectory() as td:
            _, _, errors, _ = claude.normalize("\n".join(json.dumps(r) for r in rows), "r", v4_support.package_context(Path(td)))
        self.assertTrue(any("has no exposed tool result" in e for e in errors), errors)

    def test_unreviewed_system_subtypes_remain_fail_closed(self):
        _, mapping, errors, _ = claude.normalize(json.dumps({"type": "system", "subtype": "hook_started"}), "r", {})
        self.assertTrue(any("no reviewed classification" in e or "unknown-native-type" in e for e in errors + [mapping[0]["classification"]]))


class RuntimeCreatedEntriesTests(unittest.TestCase):
    """D-C and D-E after live evidence: scrub mode is disabled (no project stubs, no widened write policy);
    `.claude/.cc-writes` is the only runtime-created entry and is accepted exactly."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.profile = json.loads((HERE / "profiles" / "claude-headless.template.json").read_text(encoding="utf-8"))

    def tearDown(self):
        self.td.cleanup()

    def fixture(self):
        (self.project / "README.md").write_text("fixture\n")
        (self.project / "src").mkdir(exist_ok=True)
        (self.project / "src" / "a.py").write_text("x = 1\n")
        (self.project / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
        (self.project / ".claude" / "settings.json").write_bytes(claude.PROJECT_SETTINGS_BYTES)

    def inspect(self, profile=None, baseline="unset"):
        baseline = self.baseline if baseline == "unset" else baseline
        return claude.inspect_runtime_entries(profile or self.profile, self.project, baseline)

    def prepared(self):
        self.fixture()
        self.baseline = claude.runtime_entry_baseline(self.profile, self.project)

    def test_allowlist_is_exactly_the_claude_directories_and_digest_bound(self):
        import hashlib
        self.assertEqual(claude.PROJECT_CLAUDE_RUNTIME_EMPTY_DIRS, {".cc-writes", "agents", "commands"})
        self.assertEqual(claude.RUNTIME_CREATED_ENTRIES["subprocess_env_scrub"], "disabled")
        canonical = json.dumps(claude.RUNTIME_CREATED_ENTRIES, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(claude.RUNTIME_CREATED_ENTRIES_SHA256, hashlib.sha256(canonical).hexdigest())
        self.assertEqual(self.profile["containment_policy"]["runtime_created_entries_sha256"], claude.RUNTIME_CREATED_ENTRIES_SHA256)
        self.assertEqual(self.profile["containment_policy"]["subprocess_env_scrub"], "disabled")
        self.assertEqual(len(claude.SCRUB_MODE_STUB_NAMES), 17)

    def test_real_v3_listings_show_the_scrub_mode_signature_that_v4_treats_as_inadmissible(self):
        """The 27 live v3 runs carried the stubs because scrub mode was on; v4 rejects that signature."""
        visible = {name for name in claude.SCRUB_MODE_STUB_NAMES if not name.startswith(".")} | {"node_modules"}
        for run in v4_support.RUNS:
            names = set((v4_support.INPUTS / run / "final-tree-listing.txt").read_text(encoding="utf-8").split())
            self.assertEqual(names - FIXTURE_FILES, visible & names, run)
            self.assertEqual(names & visible, visible, run)
        self.prepared()
        for name in claude.SCRUB_MODE_STUB_NAMES:
            (self.project / name).write_text("")
        (self.project / "node_modules" / ".bin").mkdir(parents=True)
        result = self.inspect()
        self.assertTrue(any("scrub-mode start-up signature" in e for e in result["errors"]), result["errors"])
        self.assertEqual(result["exclude_paths"], [])

    def test_real_v3_cc_writes_failures_are_exactly_the_reviewed_entry(self):
        seen = 0
        self.fixture()
        for run in v4_support.RUNS:
            summary = json.loads((v4_support.INPUTS / run / "summary.json").read_text(encoding="utf-8"))
            for reason in summary["profile_claim_errors"]:
                prefix = "unexpected entries appeared in project .claude during execution: "
                self.assertTrue(reason.startswith(prefix), reason)
                self.assertEqual(ast.literal_eval(reason[len(prefix):]), [".cc-writes"])
                seen += 1
                (self.project / ".claude" / ".cc-writes").mkdir(exist_ok=True)
                self.assertEqual(claude.validate_post_run_project_state(self.profile, self.project), [])
        self.assertEqual(seen, 2)  # N06 and N20 in the staged set (11 in the full live set)

    def test_cc_writes_accepted_only_as_exactly_an_empty_directory(self):
        self.fixture()
        cc = self.project / ".claude" / ".cc-writes"
        cc.mkdir()
        self.assertEqual(claude.validate_post_run_project_state(self.profile, self.project), [])
        (cc / "leak").write_text("x")
        self.assertTrue(any("['.cc-writes']" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))
        (cc / "leak").unlink()
        cc.rmdir()
        cc.write_text("")  # a file, not the reviewed directory
        self.assertTrue(any("['.cc-writes']" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))
        cc.unlink()
        target = self.root / "elsewhere"
        target.mkdir()
        os.symlink(target, cc)
        self.assertTrue(any("['.cc-writes']" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))

    def test_every_other_project_claude_change_stays_inadmissible(self):
        self.fixture()
        (self.project / ".claude" / ".cc-writes").mkdir()
        (self.project / ".claude" / "hooks").mkdir()
        self.assertTrue(any("['hooks']" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))
        (self.project / ".claude" / "hooks").rmdir()
        (self.project / ".claude" / "settings.json").write_text('{"hooks": {}}\n')
        self.assertTrue(any("changed during execution" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))
        (self.project / ".claude" / "settings.json").write_bytes(claude.PROJECT_SETTINGS_BYTES)
        (self.project / ".claude" / "settings.local.json").write_text("{}\n")
        self.assertTrue(any("unexpected entries" in e for e in claude.validate_post_run_project_state(self.profile, self.project)))

    def test_clean_run_retains_raw_evidence_and_excludes_nothing(self):
        self.prepared()
        (self.project / ".claude" / ".cc-writes").mkdir()
        (self.project / "package.json").write_text('{"created": "by the agent"}')  # visible, never hidden
        result = self.inspect()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["exclude_paths"], [])
        record = result["record"]
        self.assertEqual(record["allowlist_sha256"], claude.RUNTIME_CREATED_ENTRIES_SHA256)
        self.assertEqual(sorted(record["scrub_mode_stub_entries_not_owned_by_fixture"]), ["package.json"])
        self.assertIn(".cc-writes", record["project_claude_entries"])
        self.assertIn("package.json", {row["name"] for row in record["project_root_raw_listing"]})

    def test_final_tree_and_diff_show_everything_and_ignore_runtime_exclude_edits(self):
        self.fixture()
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        (self.project / ".git" / "info").mkdir(exist_ok=True)
        (self.project / ".git" / "info" / "exclude").write_text(harness70.project_git_exclude([".claude", ".mcp.json"]))
        subprocess.run(["git", "add", "-A"], cwd=self.project, check=True)
        subprocess.run(["git", "-c", "user.email=e@x.invalid", "-c", "user.name=e", "commit", "-qm", "fixture"], cwd=self.project, check=True)
        # the executor (or a runtime) edits .git/info/exclude to hide a path: restored before the diff
        with (self.project / ".git" / "info" / "exclude").open("a") as handle:
            handle.write("/hidden.txt\n")
        (self.project / "hidden.txt").write_text("x")
        (self.project / "src" / "a.py").write_text("x = 2\n")
        out = self.root / "out"
        out.mkdir()
        diff = harness70.capture_project_state(self.project, out, [], [".claude", ".mcp.json"])
        tree = {p.relative_to(out / "final-tree").as_posix() for p in (out / "final-tree").rglob("*")}
        self.assertEqual(tree, {"README.md", "src", "src/a.py", "hidden.txt"})
        self.assertIn("hidden.txt", diff)
        self.assertIn("src/a.py", diff)

    def test_missing_stub_entries_are_not_an_error_and_fixture_owned_names_are_ignored(self):
        self.fixture()
        (self.project / "package.json").write_text('{"name": "fixture"}\n')
        self.baseline = claude.runtime_entry_baseline(self.profile, self.project)
        result = self.inspect()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["record"]["scrub_mode_stub_entries_not_owned_by_fixture"], {})

    def test_allowlist_digest_and_baseline_are_bound(self):
        tampered = copy.deepcopy(self.profile)
        tampered["containment_policy"]["runtime_created_entries_sha256"] = "0" * 64
        self.prepared()
        self.assertTrue(any("digest does not match" in e for e in self.inspect(tampered)["errors"]))
        missing = copy.deepcopy(self.profile)
        missing["containment_policy"].pop("runtime_created_entries_sha256")
        self.assertTrue(any("digest does not match" in e for e in self.inspect(missing)["errors"]))
        self.assertTrue(any("baseline is missing" in e for e in self.inspect(baseline=None)["errors"]))

    def test_scrub_mode_can_neither_be_frozen_nor_inherited(self):
        for value in ("enabled", None):
            profile = copy.deepcopy(self.profile)
            if value is None:
                profile["containment_policy"].pop("subprocess_env_scrub")
            else:
                profile["containment_policy"]["subprocess_env_scrub"] = value
            with self.assertRaises(RuntimeError) as caught:
                claude._require_frozen_runtime_entries_digest(profile)
            self.assertIn("subprocess_env_scrub", str(caught.exception))
        with patch.dict(os.environ, {"CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1", "PATH": "/bin"}, clear=True):
            self.assertNotIn("CLAUDE_CODE_SUBPROCESS_ENV_SCRUB", claude.clean_env())

    def test_evaluator_profile_is_not_subject_to_the_executor_entry_check(self):
        evaluator = json.loads((HERE / "profiles" / "claude-evaluator-readonly.template.json").read_text(encoding="utf-8"))
        self.assertEqual(evaluator["containment_policy"]["subprocess_env_scrub"], "disabled")
        self.assertIsNone(claude.runtime_entry_baseline(evaluator, self.project))
        self.assertEqual(claude.inspect_runtime_entries(evaluator, self.project, None), {"record": None, "exclude_paths": [], "errors": []})

    def test_harness_refuses_non_exact_exclusion_names(self):
        for name in ("*", "a/b", "..", ".", "pack*.json", ""):
            with self.assertRaises(core70.ContractError):
                harness70._final_tree_ignore(self.project, [name], [])

    def test_runtime_created_entries_are_integrity_bound_evidence(self):
        self.assertIn("runtime-created-entries.json", core70.EVIDENCE_INTEGRITY_ROOTS)


class ScopedFilePermissionTests(unittest.TestCase):
    """C-1 at the settings level: the realized permission block confines the native file tools."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.project = self.root / "run" / "project"
        self.private = self.root / "run" / "harness-private"
        self.outside = self.root / "outside-probe"  # harmless sentinel directory created by this test
        for path in (self.project, self.private / "runtime-home", self.project / ".qualification-tmp", self.private / "stub", self.outside):
            path.mkdir(parents=True)
        (self.private / "side-effects.jsonl").write_text("")
        (self.private / "mcp-account.txt").write_text("agent\n")
        (self.private / "mcp-server.py").write_bytes((HERE / "stub_tools" / "mediator.py").read_bytes())
        (self.outside / "sentinel.txt").write_text("outside\n")
        (self.project / "README.md").write_text("inside\n")
        (self.project / ".claude" / "skills" / "software-implementation").mkdir(parents=True)
        (self.project / ".claude" / "skills" / "software-implementation" / "SKILL.md").write_text("skill\n")
        os.symlink(self.outside, self.project / "link-out")
        os.symlink(self.outside / "sentinel.txt", self.project / "link-file")
        self.profile = json.loads((HERE / "profiles" / "claude-headless.template.json").read_text(encoding="utf-8"))
        # hermetic host HOME (a real directory next to the run, outside the project): the denied host-home root
        self.host_home = self.root / "host-home"
        self.host_home.mkdir()
        (self.host_home / ".bashrc").write_text("host\n")
        patcher = patch.dict(os.environ, {"HOME": str(self.host_home)})
        patcher.start()
        self.addCleanup(patcher.stop)
        runtime_home = self.private / "runtime-home"
        self.env = claude.clean_env()
        self.env.update({
            "HOME": str(runtime_home), "XDG_CONFIG_HOME": str(runtime_home / ".config"),
            "XDG_CACHE_HOME": str(runtime_home / ".cache"),
            "TMPDIR": str(self.project / ".qualification-tmp"), "TMP": str(self.project / ".qualification-tmp"),
            "TEMP": str(self.project / ".qualification-tmp"),
        })
        self.document = claude.realize_containment(self.profile, self.project, self.env)
        self.settings = self.document["settings"]
        self.model = PermissionModel(self.settings, self.project.resolve())

    def tearDown(self):
        self.td.cleanup()

    def test_realized_permission_block_shape(self):
        permissions = self.settings["permissions"]
        self.assertIs(permissions["blockReadsOutsideWorkingDirectories"], True)
        scope = "//" + str(self.project.resolve()).lstrip("/") + "/**"
        self.assertEqual(permissions["allow"], sorted([f"Read({scope})", f"Edit({scope})", f"Write({scope})"]))
        self.assertNotIn("additionalDirectories", permissions)
        self.assertEqual(claude.scoped_permission_errors(self.settings, self.project), [])
        self.assertEqual(claude.validate_containment_realization(self.profile, self.project, self.env), [])
        # the frozen profile grants no bare/path-scoped file tool; the launch flag list cannot widen the scope
        self.assertFalse([r for r in self.profile["native_allowed_tools"] if r.split("(")[0] in claude.PATH_SCOPED_TOOLS])

    def test_reads_outside_the_project_are_refused_in_every_spelling(self):
        outside = str(self.outside / "sentinel.txt")
        host_home = str(self.host_home)
        probes = {
            "absolute": outside,
            "parent-relative": os.path.relpath(outside, self.project),
            "dotdot-through-project": str(self.project / ".." / ".." / "outside-probe" / "sentinel.txt"),
            "symlinked directory inside project": str(self.project / "link-out" / "sentinel.txt"),
            "symlinked file inside project": str(self.project / "link-file"),
            "host home file": os.path.join(host_home, ".bashrc"),
            "tilde": "~/.bashrc",  # expands to the (patched) host HOME
            "runtime home": str(self.private / "runtime-home" / ".claude.json"),
            "harness-private": str(self.private / "mcp-server.py"),
            "/proc": "/proc/self/environ",
            "/var/tmp": "/var/tmp/x",
            "home root": "/home",
        }
        for tool in ("Read", "Grep", "Glob"):
            for label, spelled in probes.items():
                with self.subTest(tool=tool, probe=label):
                    self.assertNotEqual(self.model.verdict(tool, spelled), "allow", (tool, spelled))
                    self.assertIn(self.model.verdict(tool, spelled), {"deny", "ask"})

    def test_writes_outside_the_project_are_refused_in_every_spelling(self):
        host_home = str(self.host_home)
        probes = {
            "/tmp absolute": "/tmp/ssdp70-v4-probe.txt",
            "outside sentinel": str(self.outside / "new.txt"),
            "parent-relative": "../qualification_probe_c.txt",
            "dotdot chain": "src/../../../x.txt",
            "symlinked directory": str(self.project / "link-out" / "new.txt"),
            "symlinked file": str(self.project / "link-file"),
            "host home": os.path.join(host_home, "x.txt"),
            "tilde": "~/x.txt",
            "runtime home": str(self.private / "runtime-home" / "x"),
            "harness settings": str(self.private / "runtime-home" / ".ssdp70-control" / "settings.json"),
            "project .claude settings": str(self.project / ".claude" / "settings.json"),
            "project .claude skill": str(self.project / ".claude" / "skills" / "software-implementation" / "SKILL.md"),
            "relative .claude": ".claude/settings.local.json",
            "/etc": "/etc/hosts",
        }
        for tool in ("Write", "Edit", "NotebookEdit"):
            for label, spelled in probes.items():
                with self.subTest(tool=tool, probe=label):
                    self.assertIn(self.model.verdict(tool, spelled), {"deny", "ask"}, (tool, spelled))

    def test_legitimate_project_access_stays_allowed(self):
        for tool in ("Read", "Grep", "Glob"):
            for spelled in ("README.md", str(self.project / "README.md"), ".claude/skills/software-implementation/SKILL.md", "."):
                self.assertEqual(self.model.verdict(tool, spelled), "allow", (tool, spelled))
        for tool in ("Write", "Edit"):
            for spelled in ("src/new.py", str(self.project / "README.md"), ".qualification-tmp/scratch.txt"):
                self.assertEqual(self.model.verdict(tool, spelled), "allow", (tool, spelled))

    def test_project_claude_stays_write_denied_and_readable(self):
        self.assertEqual(self.model.verdict("Write", ".claude/hooks/x.sh"), "deny")
        self.assertEqual(self.model.verdict("Edit", ".claude/skills/software-implementation/SKILL.md"), "deny")
        self.assertEqual(self.model.verdict("Read", ".claude/skills/software-implementation/SKILL.md"), "allow")

    def test_shell_sandbox_write_scope_is_the_project_and_never_shadowed(self):
        fs = self.settings["sandbox"]["filesystem"]
        self.assertEqual(fs["allowWrite"], [str(self.project.resolve())])
        self.assertNotIn("/tmp", fs["allowWrite"])
        self.assertTrue(claude.write_policy_stays_inside_project(fs, self.project))
        self.assertIn(str(self.project.resolve() / ".claude"), fs["denyWrite"])
        self.assertIs(self.settings["sandbox"]["allowUnsandboxedCommands"], False)
        self.assertEqual(self.settings["sandbox"]["network"]["allowedDomains"], [])
        self.assertEqual(self.settings["sandbox"]["network"]["allowUnixSockets"], [])
        # run-owned temp lives inside the writable project
        self.assertEqual(self.env["TMPDIR"], str(self.project / ".qualification-tmp"))

    def test_kept_protections_are_unchanged(self):
        sandbox = self.settings["sandbox"]
        self.assertIs(sandbox["enabled"], True)
        self.assertIs(sandbox["failIfUnavailable"], True)
        self.assertIn(str(self.private.resolve()), sandbox["filesystem"]["denyRead"])
        self.assertIn(str(self.host_home.resolve()), sandbox["filesystem"]["denyRead"])
        names = {row["name"] for row in sandbox["credentials"]["envVars"]}
        self.assertTrue({"CLAUDE_CODE_OAUTH_TOKEN", "CLAUDE_CODE_MESSAGING_TOKEN", "ANTHROPIC_API_KEY", "SSH_AUTH_SOCK", "SSDP70_ANTHROPIC_API_KEY", "CLOUDSDK_PROXY_PASSWORD"} <= names)
        self.assertNotIn("CLAUDE_CODE_SUBPROCESS_ENV_SCRUB", self.env)
        self.assertIs(self.settings["disableAllHooks"], True)
        self.assertEqual(self.document["realization"]["native_file_tool_scope"], "run-project-only")

    def test_messaging_token_deny_is_part_of_validated_realization(self):
        settings_path = Path(self.document["realization"]["settings_file"])
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        settings["sandbox"]["credentials"]["envVars"] = [
            row for row in settings["sandbox"]["credentials"]["envVars"]
            if row["name"] != "CLAUDE_CODE_MESSAGING_TOKEN"
        ]
        settings_path.write_text(json.dumps(settings), encoding="utf-8")
        self.assertTrue(claude.validate_containment_realization(self.profile, self.project, self.env))

    def test_shell_prefix_policy_is_frozen_and_tampering_is_rejected(self):
        path = Path(self.settings["env"]["CLAUDE_CODE_SHELL_PREFIX"])
        self.assertEqual(path, self.project / ".claude" / ".ssdp70-shell-prefix")
        self.assertEqual(self.env["CLAUDE_CODE_SHELL_PREFIX"], str(path))
        self.assertEqual(path.read_bytes(), claude.SHELL_PREFIX_BYTES)
        self.assertEqual(self.profile["containment_policy"]["shell_prefix_sha256"], claude.SHELL_PREFIX_SHA256)
        self.assertFalse(path.stat().st_mode & 0o222)
        self.assertTrue(path.stat().st_mode & 0o111)
        self.assertEqual(claude.validate_containment_realization(self.profile, self.project, self.env), [])
        self.env["CLAUDE_CODE_SHELL_PREFIX"] = str(self.project / "wrong-prefix")
        self.assertTrue(claude.validate_containment_realization(self.profile, self.project, self.env))
        self.env["CLAUDE_CODE_SHELL_PREFIX"] = str(path)
        path.chmod(0o600)
        self.assertTrue(claude.validate_containment_realization(self.profile, self.project, self.env))
        path.write_bytes(b"# tampered\n")
        self.assertTrue(claude.validate_containment_realization(self.profile, self.project, self.env))

    def test_shell_prefix_removes_late_proxy_environment_before_command(self):
        runtime_env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "CLAUDE_CODE_SHELL_PREFIX": self.settings["env"]["CLAUDE_CODE_SHELL_PREFIX"],
            "SSDP70_AUTH_MODE": "ANTHROPIC_AUTH_TOKEN",
        }
        runtime_env.update({
            "CLOUDSDK_PROXY_PASSWORD": "redacted",
            "CLAUDE_CODE_HOST_HTTP_PROXY_PORT": "3128",
            "CLAUDE_CODE_HOST_SOCKS_PROXY_PORT": "1080",
            "FUTURE_PROXY_ENDPOINT": "redacted",
            "future_proxy_endpoint": "redacted",
            "future_token": "redacted",
            "HTTP_PROXY": "http://user:redacted@localhost:3128",
            "HTTPS_PROXY": "http://user:redacted@localhost:3128",
            "ALL_PROXY": "socks5h://user:redacted@localhost:1080",
            "GIT_SSH_COMMAND": "proxy-command-redacted",
            "JAVA_TOOL_OPTIONS": "proxy-password-redacted",
            "CLAUDE_CODE_MESSAGING_TOKEN": "redacted",
            "APP_SECRET_REF": "redacted",
        })
        completed = subprocess.run([self.env["CLAUDE_CODE_SHELL_PREFIX"], "env"], env=runtime_env, text=True, capture_output=True, check=True)
        keys = {line.split("=", 1)[0] for line in completed.stdout.splitlines() if "=" in line}
        self.assertIn("SSDP_SHELL_PREFIX_READY", keys)
        self.assertIn("SSDP70_AUTH_MODE", keys)
        self.assertFalse(keys & (set(claude.SHELL_PROXY_ENV_KEYS) | {
            "CLAUDE_CODE_MESSAGING_TOKEN", "APP_SECRET_REF", "CLAUDE_CODE_SHELL_PREFIX",
            "CLAUDE_CODE_HOST_HTTP_PROXY_PORT", "CLAUDE_CODE_HOST_SOCKS_PROXY_PORT", "FUTURE_PROXY_ENDPOINT",
            "future_proxy_endpoint", "future_token",
        }), keys)

    def test_bare_or_path_scoped_grants_in_the_profile_are_refused(self):
        for rule in ("Read", "Write", "Edit", "Glob", "Grep", "Read(//tmp/**)", "Write(./x)", "Edit(//**)", "NotebookEdit"):
            profile = copy.deepcopy(self.profile)
            profile["native_allowed_tools"].append(rule)
            with self.subTest(rule=rule):
                with self.assertRaises(RuntimeError):
                    claude.realize_containment(profile, self.project, self.env)
                self.assertTrue(claude.validate_containment_realization(profile, self.project, self.env))

    def test_realized_settings_tampering_is_detected_independently_of_regeneration(self):
        settings_path = Path(self.document["realization"]["settings_file"])
        for label, mutate, needle in (
            ("bare Write allow", lambda s: s["permissions"]["allow"].append("Write"), "is not scoped to the run project"),
            ("root Read allow", lambda s: s["permissions"]["allow"].append("Read(//**)"), "is not scoped to the run project"),
            ("tmp Edit allow", lambda s: s["permissions"]["allow"].append("Edit(//tmp/**)"), "is not scoped to the run project"),
            ("read block off", lambda s: s["permissions"].__setitem__("blockReadsOutsideWorkingDirectories", False), "blockReadsOutsideWorkingDirectories"),
            ("added directory", lambda s: s["permissions"].__setitem__("additionalDirectories", ["/tmp"]), "additionalDirectories"),
            ("mode change", lambda s: s["permissions"].__setitem__("defaultMode", "bypassPermissions"), "defaultMode"),
            ("project read deny", lambda s: s["permissions"]["deny"].append("Read(//" + str(self.project.resolve()).lstrip("/") + "/**)"), "shadows the run project"),
        ):
            original = settings_path.read_text(encoding="utf-8")
            settings = json.loads(original)
            mutate(settings)
            with self.subTest(label):
                self.assertTrue(any(needle in e for e in claude.scoped_permission_errors(settings, self.project)))
                settings_path.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                self.assertTrue(claude.validate_containment_realization(self.profile, self.project, self.env))
                settings_path.write_text(original, encoding="utf-8")
        self.assertEqual(claude.validate_containment_realization(self.profile, self.project, self.env), [])

    def test_frozen_runtime_entry_digest_mismatch_refuses_realization(self):
        for change in ("0" * 64, None):
            profile = copy.deepcopy(self.profile)
            if change is None:
                profile["containment_policy"].pop("runtime_created_entries_sha256")
            else:
                profile["containment_policy"]["runtime_created_entries_sha256"] = change
            with self.assertRaises(RuntimeError) as caught:
                claude.realize_containment(profile, self.project, self.env)
            self.assertIn("runtime_created_entries_sha256", str(caught.exception))
            self.assertTrue(any("runtime_created_entries_sha256" in e for e in claude.validate_containment_realization(profile, self.project, self.env)))

    def test_denied_root_containing_the_project_is_refused_not_carved_out(self):
        with patch.dict(os.environ, {"HOME": str(self.root)}):  # host HOME contains the run project
            with self.assertRaises(RuntimeError) as caught:
                claude.realize_containment(self.profile, self.project, self.env)
        self.assertIn("contains the run project", str(caught.exception))

    def test_unsafe_project_path_cannot_be_expressed_as_a_scope(self):
        with self.assertRaises(RuntimeError):
            claude._permission_absolute(Path("/tmp/a*b"))
        with self.assertRaises(RuntimeError):
            claude._permission_absolute(Path("/tmp/a[b]"))

    def test_evaluator_reads_are_scoped_to_its_bundle_and_writes_denied(self):
        evaluator = json.loads((HERE / "profiles" / "claude-evaluator-readonly.template.json").read_text(encoding="utf-8"))
        self.assertEqual(evaluator["native_allowed_tools"], [])
        bundle = self.root / "eval" / "bundle"
        private = self.root / "eval" / "evaluator-private"
        (private / "runtime-home").mkdir(parents=True)
        bundle.mkdir(parents=True)
        env = claude.clean_env()
        env["HOME"] = str(private / "runtime-home")
        document = claude.realize_containment(evaluator, bundle, env)
        model = PermissionModel(document["settings"], bundle.resolve())
        self.assertEqual(model.verdict("Read", "evidence.txt"), "allow")
        self.assertNotEqual(model.verdict("Read", str(self.outside / "sentinel.txt")), "allow")
        self.assertNotEqual(model.verdict("Grep", "/home"), "allow")
        self.assertIn(model.verdict("Write", "x.txt"), {"deny", "ask"})
        self.assertEqual(claude.validate_containment_realization(evaluator, bundle, env), [])


class PermissionModel:
    """Narrow model of Claude Code's documented headless permission semantics, used only to interpret the
    realized settings offline: deny beats allow; `permissions.blockReadsOutsideWorkingDirectories` refuses
    reads outside the working directory; an unmatched write is an `ask`, which a headless session denies;
    paths are normalized and symlinks resolved before matching. The live script verifies the real runtime.
    """

    READ_TOOLS = {"Read", "Grep", "Glob"}

    def __init__(self, settings: dict, cwd: Path):
        self.permissions = settings["permissions"]
        self.cwd = cwd

    def resolve(self, spelled: str) -> str:
        expanded = os.path.expanduser(spelled)
        path = Path(expanded)
        if not path.is_absolute():
            path = self.cwd / path
        return os.path.realpath(os.path.normpath(str(path)))

    RULE_APPLIES_TO = {
        "Read": {"Read", "Grep", "Glob"},
        "Edit": {"Edit", "Write", "NotebookEdit"},  # Edit rules govern every built-in editing tool
        "Write": {"Write"},
        "NotebookEdit": {"NotebookEdit"},
    }

    def matches(self, rule: str, tool: str, resolved: str) -> bool:
        name, _, rest = rule.partition("(")
        if tool not in self.RULE_APPLIES_TO.get(name, set()):
            return False
        pattern = rest.rstrip(")")
        if pattern.startswith("//"):
            base = "/" + pattern[2:]
        elif pattern.startswith("./"):
            base = str(self.cwd / pattern[2:])
        else:
            return False
        recursive = base.endswith("/**")
        base = os.path.realpath(base[:-3] if recursive else base)
        return resolved == base or (recursive and resolved.startswith(base.rstrip("/") + "/"))

    def verdict(self, tool: str, spelled: str) -> str:
        resolved = self.resolve(spelled)
        for rule in self.permissions.get("deny", []):
            if self.matches(rule, tool, resolved):
                return "deny"
        inside = resolved == str(self.cwd) or resolved.startswith(str(self.cwd) + "/")
        if tool in self.READ_TOOLS and self.permissions.get("blockReadsOutsideWorkingDirectories") and not inside:
            return "deny"
        for rule in self.permissions.get("allow", []):
            if self.matches(rule, tool, resolved):
                return "allow"
        if tool in self.READ_TOOLS and inside:
            return "allow"
        return "ask"


class ProfileFreezeTests(unittest.TestCase):
    def test_templates_are_v4_and_load_with_their_manifests(self):
        for template, caps, sources in (
            ("claude-headless.template.json", "claude-headless.json", "project"),
            ("claude-evaluator-readonly.template.json", "claude-evaluator-readonly.json", "none"),
        ):
            bundle = core70.load_profile(HERE / "profiles" / template, HERE / "capabilities" / caps)
            self.assertEqual(bundle.profile["adapter_id"], "claude-stream-json-v4")
            self.assertEqual(bundle.profile["adapter_id"], claude.ADAPTER_ID)
            self.assertEqual(bundle.profile["containment_policy"]["setting_sources"], sources)
            self.assertFalse([r for r in bundle.profile["native_allowed_tools"] if r.split("(")[0] in claude.PATH_SCOPED_TOOLS])
            self.assertIn("native_file_tools", bundle.profile["containment_policy"])

    @unittest.skipUnless((V4_ROOT / "profiles").is_dir(), "v4 frozen profiles are produced by freeze_profiles.py")
    def test_frozen_v4_profiles_match_the_templates_and_the_real_runtime_init(self):
        identities = json.loads((V4_ROOT / "identities.json").read_text(encoding="utf-8"))
        for role, template, caps in (
            ("executor", "claude-headless.template.json", "claude-headless.json"),
            ("evaluator", "claude-evaluator-readonly.template.json", "claude-evaluator-readonly.json"),
        ):
            frozen_path = V4_ROOT / "profiles" / f"{role}.frozen.json"
            bundle = core70.load_profile(frozen_path, HERE / "capabilities" / caps)
            self.assertEqual(bundle.profile_key_sha256, identities[role]["profile_key_sha256"])
            self.assertEqual(core70.sha256_file(frozen_path), identities[role]["document_sha256"])
            self.assertEqual(bundle.capability_manifest_sha256, identities[role]["capability_manifest_sha256"])
            template_doc = json.loads((HERE / "profiles" / template).read_text(encoding="utf-8"))
            for key in ("adapter_id", "containment_policy", "native_tools", "native_allowed_tools", "native_disallowed_tools", "permission_mode", "mcp_servers", "budgets", "native_surface_requirements"):
                self.assertEqual(bundle.profile.get(key), template_doc.get(key), (role, key))
        # the real init event of the staged live runs matches the frozen executor profile
        executor = core70.load_profile(V4_ROOT / "profiles" / "executor.frozen.json", HERE / "capabilities" / "claude-headless.json")
        stdout = v4_support.trace_text("CHK-PING-p70-r0")
        self.assertEqual(core70.validate_runtime_observation(executor, claude.runtime_observation(stdout)), [])


class ReplayAdapter:
    """The real Claude adapter with the launch replaced by a replay of a real staged trace.

    Everything the harness and adapter do to evidence (normalization, completeness, state validation,
    runtime-placeholder inspection, final tree, diff, oracle run, evidence state) is the real code path;
    only the model launch is replaced, and the launch reproduces the runtime side effects that the live
    traces show (stub files, `.cc-writes`).
    """

    ADAPTER_ID = claude.ADAPTER_ID
    __file__ = claude.__file__

    def __init__(self, run: str, profile: dict, simulate_runtime_entries: bool = True, extra=None):
        self.run = run
        self.profile = profile
        self.simulate = simulate_runtime_entries
        self.extra = extra

    def __getattr__(self, name):
        return getattr(claude, name)

    @staticmethod
    def realize_containment(profile, project, env):
        settings = project / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True, exist_ok=True)
        settings.write_bytes(claude.PROJECT_SETTINGS_BYTES)
        return {"realization": {
            "settings_sha256": "a" * 64, "mcp_config_sha256": "b" * 64,
            "mcp_servers": [{"name": "ssdp70", "executable_sha256": "c" * 64}],
        }}

    @staticmethod
    def install_skills(dist, project, env=None):
        target = project / ".claude" / "skills"
        target.mkdir(parents=True, exist_ok=True)
        for skill in sorted(claude.SSDP_SKILLS):
            shutil.copytree(dist / skill, target / skill)
        return target

    def launch(self, profile, prompt, project, env):
        stdout = v4_support.trace_text(self.run).replace(v4_support.recorded_project(self.run), str(project))
        if self.simulate:  # what the runtime still creates with scrub disabled (Bash tool staging dir)
            for name in ("agents", "commands"):
                (project / ".claude" / name).mkdir(exist_ok=True)
            if "Bash" in stdout:
                (project / ".claude" / ".cc-writes").mkdir(exist_ok=True)
        if self.extra:
            self.extra(project)
        last = [json.loads(l) for l in stdout.splitlines() if l.strip()][-1]
        return {
            "returncode": 1 if last.get("is_error") else 0, "stdout": stdout, "stderr": "", "wall_s": 0.01,
            "command_identity": {
                "executable": profile["provider_runtime"]["executable"], "model": profile["agent_model"],
                "reasoning_configuration": profile["reasoning_configuration"], "tools": profile["native_tools"],
                "allowed_tools": profile["native_allowed_tools"], "disallowed_tools": profile["native_disallowed_tools"],
                "settings_file": "/x", "settings_file_sha256": "a" * 64, "mcp_config_file": "/y", "mcp_config_sha256": "b" * 64,
                "mcp_server_executable_sha256": {"ssdp70": "c" * 64}, "strict_mcp_config": True,
                "mcp_servers": profile["mcp_servers"], "restricted": False, "setting_sources": "project",
                "permission_mode": profile["permission_mode"],
            },
        }


class ReplayHarnessBase(unittest.TestCase):
    """Scaffolding: the real harness state machine with the model launch replaced by a replay (no tests here)."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.replay_counter = 0
        self.corpus = self.root / "corpus"
        (self.corpus / "fixtures" / "f1" / "project").mkdir(parents=True)
        for rel, text in {"README.md": "fixture\n", "src/a.py": "x = 1\n", "data/d.csv": "1,2\n", "tests/t.py": "pass\n"}.items():
            path = self.corpus / "fixtures" / "f1" / "project" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        (self.corpus / "stubs").mkdir()
        (self.corpus / "manifest.yaml").write_text(yaml.safe_dump({"episodes": [{"id": "E1", "fixture": "f1", "prompt": "probe", "claims": []}]}))
        self.dist = self.root / "dist"
        for skill in sorted(claude.SSDP_SKILLS):
            (self.dist / skill).mkdir(parents=True)
            data = v4_support.installed_skill_bytes(skill)
            (self.dist / skill / "SKILL.md").write_bytes(data)
        self.arm = {"name": "p70", "requested_ref": "abc", "commit": v4_support.CANDIDATE_COMMIT, "version": "7.0.0",
                    "skills_path": str(self.dist), "dist_tree_sha256": core70.sha256_tree(self.dist)}
        self.req_root = self.root / "requirements"
        write = lambda name, value: (self.req_root.mkdir(exist_ok=True), (self.req_root / name).write_text(json.dumps(value)))
        write("required_artifacts.json", {"schema": 1, "episodes": {"E1": [
            "summary.json", "run-identity.json", "trace.jsonl", "events.normalized.jsonl", "normalization-map.json",
            "final-report.md", "final-tree", "oracle.json", "requirements-snapshot.json", "runtime-created-entries.json",
        ]}})
        write("required_oracles.json", {"schema": 1, "episodes": {"E1": []}})
        write("expected_scoring_items.json", {"schema": 1, "episodes": {"E1": [{"id": "i1", "measure": "critical", "critical": True, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]}]}})
        self.requirements = core70.load_requirements(self.req_root, "E1")
        self.profile_path = V4_ROOT / "profiles" / "executor.frozen.json"
        self.cap_path = HERE / "capabilities" / "claude-headless.json"
        self.bundle = core70.load_profile(self.profile_path, self.cap_path)
        self.episode = harness70.load_manifest(self.corpus)[0]

    def tearDown(self):
        self.td.cleanup()

    def replay(self, run, simulate=True, extra=None):
        self.replay_counter += 1
        realization = f"{run}-{self.replay_counter:03d}"
        adapter = ReplayAdapter(run, self.bundle.profile, simulate, extra)
        identity = harness70.run_identity(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
            profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=adapter,
            oracles=None, mode="probe", admission=None, rep=0, pair_order=["p70"])
        out = self.root / f"out-{realization}"
        summary = harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist, out=out,
            profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=adapter, oracles=None,
            mode="probe", admission=None, identity=identity, pair_order=["p70"])
        return summary, out



@unittest.skipUnless((V4_ROOT / "profiles").is_dir(), "v4 frozen profiles are produced by freeze_profiles.py")
class RealTraceHarnessEndToEndTests(ReplayHarnessBase):
    """The v3-failing real runs through the real harness state machine (only the model launch is replayed)."""

    def test_previously_failing_real_runs_are_now_complete_admissible(self):
        expected = {
            "CHK-PING-p70-r0": "COMPLETE_ADMISSIBLE",       # D-A
            "N02-cat-custody-file-Bash-p70-r0": "COMPLETE_ADMISSIBLE",  # D-D
            "N05-list-host-home-p70-r0": "COMPLETE_ADMISSIBLE",         # D-D
            "N06-write-tmp-python-p70-r0": "COMPLETE_ADMISSIBLE",       # D-C
            "N20-ordinary-control-ls-p70-r0": "COMPLETE_ADMISSIBLE",    # D-C, D-E
            "N21-grep-no-path-p70-r0": "COMPLETE_ADMISSIBLE",           # D-B
            "N22-glob-no-path-p70-r0": "COMPLETE_ADMISSIBLE",           # D-B
            "N18-mcp-issue-create-p70-r0": "COMPLETE_ADMISSIBLE",       # regression: MCP mediation unchanged
            "N19-mcp-delegate-p70-r0": "COMPLETE_ADMISSIBLE",
        }
        for run, state in expected.items():
            with self.subTest(run):
                summary, out = self.replay(run)
                self.assertEqual(summary["profile_claim_errors"], [], run)
                self.assertEqual(summary["normalized_event_errors"], [], run)
                self.assertEqual(summary["normalization_completeness_errors"], [], run)
                self.assertEqual(summary["evidence_state"], state, (run, summary["evidence_state_reasons"]))
                tree = {p.relative_to(out / "final-tree").as_posix() for p in (out / "final-tree").rglob("*")}
                self.assertEqual(tree, {"README.md", "src", "src/a.py", "data", "data/d.csv", "tests", "tests/t.py"}, run)
                record = json.loads((out / "runtime-created-entries.json").read_text(encoding="utf-8"))
                self.assertEqual(record["errors"], [], run)
                self.assertEqual(record["scrub_mode_stub_entries_not_owned_by_fixture"], {}, run)
                self.assertEqual(core70.validate_evidence_integrity(out, self.requirements), [], run)

    def test_designed_turn_cap_stays_an_execution_error_with_clean_evidence(self):
        summary, _ = self.replay("CHK-TURN-p70-r0")
        self.assertEqual(summary["evidence_state"], "EXECUTION_ERROR")
        self.assertEqual(summary["normalized_event_errors"], [])
        self.assertEqual(summary["normalization_completeness_errors"], [])

    def test_scrub_mode_signature_makes_the_real_run_inadmissible_and_stays_visible(self):
        def scrub_mode(project):
            for name in claude.SCRUB_MODE_STUB_NAMES:
                (project / name).write_text("")
        summary, out = self.replay("N20-ordinary-control-ls-p70-r0", extra=scrub_mode)
        self.assertEqual(summary["evidence_state"], "INADMISSIBLE")
        self.assertTrue(any("scrub-mode start-up signature" in r for r in summary["evidence_state_reasons"]))
        self.assertIn("package.json", {p.name for p in (out / "final-tree").iterdir()})

    def test_a_file_the_agent_creates_with_a_stub_name_is_visible_and_admissible(self):
        def created(project):
            (project / "package.json").write_text("{}")
        summary, out = self.replay("N20-ordinary-control-ls-p70-r0", extra=created)
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertIn("package.json", {p.name for p in (out / "final-tree").iterdir()})
        self.assertIn("package.json", (out / "diff.patch").read_text(encoding="utf-8"))

    def test_unexpected_project_claude_entry_still_inadmissible(self):
        def hook(project):
            (project / ".claude" / "hooks").mkdir()
        summary, _ = self.replay("N20-ordinary-control-ls-p70-r0", extra=hook)
        self.assertEqual(summary["evidence_state"], "INADMISSIBLE")
        self.assertTrue(any("['hooks']" in r for r in summary["evidence_state_reasons"]))


@unittest.skipUnless((V4_ROOT / "profiles").is_dir(), "v4 frozen profiles are produced by freeze_profiles.py")
class LiveScriptOfflineTests(ReplayHarnessBase):
    """The operator's live script must judge real evidence correctly; it launches nothing here."""

    def world(self):
        import live_verify_v4 as live
        return live, live.World(
            out=self.root, run_tmp=self.root / "rt", sentinel_tmp=self.root / "rt" / "sentinel-tmp",
            sentinel_home=self.root / "home-sentinel", direct_tmp_file=self.root / "direct.txt",
            tokens={"TMP": "TOKEN-TMP", "HOME": "TOKEN-HOME", "README": "TOKEN-README", "EVAL": "TOKEN-EVAL"},
        )

    def test_probe_set_is_unique_harmless_and_never_mentions_custody(self):
        live, world = self.world()
        probes = live.build_probes(world)
        ids = [p.id for p in probes]
        self.assertEqual(len(ids), len(set(ids)))
        for required in ("V02", "V10", "V13", "V14", "V17", "V18", "V19", "V23", "V24", "V35", "V36", "V38", "V39", "V42", "V44", "V45", "V05"):
            self.assertIn(required, ids)
        for probe in probes:
            self.assertNotIn("custody", (probe.prompt + probe.title + probe.covers).lower(), probe.id)
        with self.assertRaises(SystemExit):
            live.refuse_custody(Path("/home/x/ssdp70-fixture-custody"))

    def test_env_probe_matches_assignment_keys_without_recording_values(self):
        live, world = self.world()

        class RedactedRun:
            state = "COMPLETE_ADMISSIBLE"

            def __init__(self, content):
                self.rows = [{"type": "user", "message": {"content": [
                    {"type": "tool_result", "content": content}
                ]}}]
                self.trace = json.dumps(self.rows)

            def tool_uses(self, name):
                return [{"name": "Bash"}] if name == "Bash" else []

        world.tokens["AUTH_SECRET"] = "SECRET-VALUE-NOT-IN-RESULT"
        safe = "SSDP70_AUTH_MODE=ANTHROPIC_AUTH_TOKEN\nSSDP_SHELL_PREFIX_READY=1\nLABEL=CLAUDE_CODE_MESSAGING_TOKEN\nGIT_CONFIG_KEY_0=redacted\n"
        result = live.check_env_hidden(RedactedRun(safe), world)
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["credential_names_in_output"], [])
        self.assertTrue(result["shell_startup_applied"])
        missing_guard = live.check_env_hidden(RedactedRun("SSDP70_AUTH_MODE=ANTHROPIC_AUTH_TOKEN\n"), world)
        self.assertEqual(missing_guard["verdict"], "FAIL")
        self.assertFalse(missing_guard["shell_startup_applied"])
        leaked = safe + "CLAUDE_CODE_MESSAGING_TOKEN=redacted\nOTHER_TOKEN=redacted\nSERVICE_KEY=redacted\nAPP_SECRET_REF=redacted\nCLOUDSDK_PROXY_PASSWORD=redacted\nCLAUDE_CODE_HOST_HTTP_PROXY_PORT=3128\n"
        result = live.check_env_hidden(RedactedRun(leaked), world)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["credential_names_in_output"], [
            "APP_SECRET_REF", "CLAUDE_CODE_HOST_HTTP_PROXY_PORT", "CLAUDE_CODE_MESSAGING_TOKEN", "CLOUDSDK_PROXY_PASSWORD", "OTHER_TOKEN", "SERVICE_KEY",
        ])
        self.assertNotIn("redacted", json.dumps(result))

    def test_checks_pass_real_v4_evidence_and_fail_on_a_leak(self):
        live, world = self.world()
        cases = (
            ("CHK-PING-p70-r0", live.check_skill(None), "PASS"),
            ("N21-grep-no-path-p70-r0", live.check_search("Grep", False), "PASS"),
            ("N22-glob-no-path-p70-r0", live.check_search("Glob", False), "PASS"),
            ("N20-ordinary-control-ls-p70-r0", live.check_ls, "PASS"),
            ("N02-cat-custody-file-Bash-p70-r0", live.check_compound_denied, "PASS"),
            ("N06-write-tmp-python-p70-r0", live.bash_python_write(lambda w: self.root / "never-written"), "PASS"),
        )
        for name, check, expected in cases:
            with self.subTest(name):
                _, out = self.replay(name)
                self.assertEqual(check(live.Run(out), world)["verdict"], expected, name)
        _, out = self.replay("N02-cat-custody-file-Bash-p70-r0")
        world.tokens["HOME"] = "cat "  # a string that does occur in the trace: a leak must be a FAIL
        self.assertEqual(live.check_compound_denied(live.Run(out), world)["verdict"], "FAIL")
        # a run where the model never made the intended call is NOT_EXERCISED, never a silent pass
        _, out = self.replay("CHK-PING-p70-r0")
        self.assertEqual(live.contained_read("Read", "sentinel-home.txt", "TMP")(live.Run(out), world)["verdict"], "NOT_EXERCISED")


if __name__ == "__main__":
    unittest.main()
