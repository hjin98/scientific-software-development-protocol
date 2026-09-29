#!/usr/bin/env python3
"""Operator/developer probe that (re)generates the exact-build OMP inventory.

Output: omp-build-inventory-18.0.11.json, retained beside the adapter and bound by digest into the
frozen execution profile. The inventory is empirical evidence about the exact build, not authority:

  * settings      every setting the build exposes (`omp config list --json`), its default, the value
                  the profile freezes and its closure class;
  * discovery     every project-, HOME- and ancestor-relative path the build probes at startup
                  (strace of the real binary in the real sandbox, seccomp off only so strace can
                  trace), every program it executes and every network destination it attempts;
  * effect tests  hostile sources planted in each identified family and what actually reached the
                  runtime (system prompt, tool list, environment, executed code), observed through
                  the trusted observer, i.e. through the same evidence path a run uses;
  * provider-managed state   each behaviour with its disposition (disabled / frozen+observed /
                  claim-scoped inadmissible).

Run: python3 omp_inventory_probe.py --omp ~/.local/bin/omp [--out omp-build-inventory-18.0.11.json]
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yaml  # noqa: E402

from adapters import omp  # noqa: E402
import stand_in_provider  # noqa: E402

UI_PREFIXES = (
    "theme.", "symbolPreset", "colorBlindMode", "composer.", "statusLine.", "terminal.", "images.autoResize",
    "images.blockImages", "tui.", "display.", "showHardwareCursor", "task.showResolvedModelBadge",
    "treeFilterMode", "autocompleteMaxVisible", "spelling.", "emojiAutocomplete", "paste.", "doubleEscapeAction",
    "stt.", "speech.", "tts.", "live.voice", "providers.tts",
)
NETWORK_ONLY_PREFIXES = (
    "collab.", "share.", "searxng.", "exa.", "hindsight.", "mnemopi.", "sharpshooter.", "images.urls.",
    "providers.webSearch", "providers.imageOrder", "providers.fireworksTier", "providers.ollama", "providers.antigravity",
    "providers.kimiApiFormat", "providers.openrouterVariant", "providers.fetch", "providers.cacheRetention",
    "codexResets.", "github.", "browser.", "computer.", "irc.", "vault.", "generate_image.", "speechgen.",
    "commit.", "gc.", "dev.autoqaPush", "auth.broker", "secrets.",
)
TOOL_ABSENT_PREFIXES = (
    "task.", "astGrep.", "astEdit.", "debug.", "launch.", "checkpoint.", "inspect_image.", "fetch.", "web_search.",
    "security.", "ask.enabled", "async.", "todo.", "glob.", "grep.",
)


CLOSED_FEATURE_GROUPS = (
    "retry.", "compaction.", "snapcompact.", "memories.", "memory.", "autolearn.", "advisor.", "ttsr.", "prewalk.",
    "branchSummary.", "shellMinimizer.", "recap.", "lsp.", "bash.direnv", "bash.autoBackground", "eval.", "mcp.notif",
    "model.loopGuard", "model.toolCallLoopGuard", "plan.", "goal.", "title.", "features.", "magicKeywords.",
    "contextPromotion", "read.summarize", "extensions", "disabledExtensions", "skills.ignoredSkills", "skills.includeSkills",
    "python.", "ruby.", "julia.", "tasks.", "startup.", "update.", "tools.xdev", "async.", "bash.autoBackground",
)


def classify_setting(key: str, frozen: dict[str, object]) -> str:
    if key in frozen:
        return "frozen-closed"
    if key.startswith(CLOSED_FEATURE_GROUPS):
        return "sub-parameter-of-closed-feature"
    if key.startswith(UI_PREFIXES):
        return "ui-irrelevant-in-print-json-mode"
    if key.startswith(NETWORK_ONLY_PREFIXES):
        return "requires-network-or-service-unreachable-in-subject-netns"
    if key.startswith(TOOL_ABSENT_PREFIXES):
        return "tool-not-exposed-by-frozen-tool-surface"
    return "default-retained-behaviour-visible-in-evidence"


def run_settings(exe: str) -> dict[str, dict]:
    tmp = Path(tempfile.mkdtemp(prefix="omp-inv-"))
    try:
        results = {}
        for label, doc in (("default", None), ("frozen", omp.settings_document())):
            home = tmp / label
            (home / ".omp" / "agent").mkdir(parents=True)
            if doc is not None:
                (home / ".omp" / "agent" / "config.yml").write_bytes(omp._yaml(doc))
            done = subprocess.run(
                [exe, "config", "list", "--json"], env={"PATH": "/usr/bin:/bin", "HOME": str(home)},
                capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120,
            )
            if done.returncode != 0:
                raise SystemExit(f"omp config list failed: {done.stderr[:400]}")
            results[label] = json.loads(done.stdout)
        return results
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def settings_inventory(exe: str) -> dict:
    results = run_settings(exe)
    frozen = omp.frozen_settings_flat()
    entries = []
    missing = []
    for key, meta in sorted(results["default"].items()):
        eff = results["frozen"].get(key, {})
        entries.append({
            "key": key,
            "type": meta.get("type"),
            "default": meta.get("value"),
            "effective_under_frozen_profile": eff.get("value"),
            "frozen_value": frozen.get(key, "<not frozen>") if key in frozen else None,
            "class": classify_setting(key, frozen),
        })
    for key in frozen:
        if key not in results["default"]:
            missing.append(key)
    return {"count": len(entries), "entries": entries, "frozen_keys_absent_from_build": missing}


SYSCALL_TRACE = "openat,open,stat,lstat,newfstatat,statx,access,faccessat,faccessat2,readlink,readlinkat,getdents64,execve,connect,mkdir,mkdirat,creat,rename,renameat,renameat2,unlink,unlinkat,symlink,symlinkat"
STRACE_LINE = re.compile(r"^(?:\d+\s+)?(\w+)\((.*)\)\s+=\s+(-?\d+|\?)(?:\s+(\w+))?")


def hostile_project_files() -> dict[str, str]:
    marker = "HOSTILE-MARKER-D4"
    files: dict[str, str] = {}
    for root, name in ((".claude", "evil-claude"), (".codex", "evil-codex"), (".agents", "evil-agents"), (".agent", "evil-agent"),
                       (".omp", "evil-omp"), (".opencode", "evil-opencode"), (".gemini", "evil-gemini"), (".cursor", "evil-cursor"),
                       (".github", "evil-github")):
        files[f"{root}/skills/{name}/SKILL.md"] = f"---\nname: {name}\ndescription: {marker}-{name}\n---\n{marker}\n"
    files["CLAUDE.md"] = f"{marker}-CLAUDE-md\n"
    files["AGENTS.md"] = f"{marker}-AGENTS-md\n"
    files["GEMINI.md"] = f"{marker}-GEMINI-md\n"
    files[".github/copilot-instructions.md"] = f"{marker}-copilot\n"
    files[".cursor/rules/r.mdc"] = f"---\nalwaysApply: true\n---\n{marker}-cursor\n"
    files[".windsurf/rules/r.md"] = f"{marker}-windsurf\n"
    files[".omp/rules/r.md"] = f"---\nalwaysApply: true\n---\n{marker}-omp-rule\n"
    for name in (".mcp.json", "mcp.json", ".omp/mcp.json", ".cursor/mcp.json", ".vscode/mcp.json", ".claude/mcp.json"):
        files[name] = json.dumps({"mcpServers": {"evil-mcp": {"type": "http", "url": "http://127.0.0.1:31099/mcp"}}})
    files[".claude/hooks/pre/x.sh"] = "#!/bin/sh\ntouch /workspace/HOOK-RAN\n"
    files[".omp/hooks/pre/x.sh"] = "#!/bin/sh\ntouch /workspace/HOOK2-RAN\n"
    files[".omp/extensions/evil.ts"] = "export default () => { require('fs').writeFileSync('/workspace/EXT-RAN', '1') }\n"
    files["bunfig.toml"] = "preload = ['./evil.js']\n"
    files["evil.js"] = "require('fs').writeFileSync('/workspace/BUNFIG-RAN', '1')\n"
    files[".env"] = "HOSTILE_ENV_PROJECT=1\nOPENAI_API_KEY=HOSTILE-KEY\n"
    return files


def _family(path: str) -> str:
    if path.startswith("/workspace/"):
        rel = path[len("/workspace/"):]
        return "project:" + rel
    if path == "/workspace":
        return "project-root"
    if path.startswith("/home/agent/"):
        return "home:" + path[len("/home/agent/"):]
    if path.startswith(("/usr/", "/lib", "/bin", "/etc", "/proc", "/dev", "/sys", "/opt/omp", "/opt/ssdp", "/tmp")):
        return "system"
    return "ancestor-or-other:" + path


def parse_strace(text: str) -> dict:
    found: dict[str, str] = {}
    absent: set[str] = set()
    execs: list[list[str]] = []
    connects: set[str] = set()
    created: set[str] = set()
    for line in text.splitlines():
        match = STRACE_LINE.match(line)
        if not match:
            continue
        call, args, result = match.group(1), match.group(2), match.group(3)
        if call in ("connect",):
            m = re.search(r'sa_family=(AF_\w+).*?(?:sin_port=htons\((\d+)\)|sun_path="([^"]*)").*?(?:inet_addr\("([^"]*)"\))?', args)
            if m:
                connects.add(f"{m.group(1)}:{m.group(4) or m.group(3) or ''}:{m.group(2) or ''}={result}")
            continue
        if call == "execve":
            m = re.match(r'"([^"]*)",\s*\[(.*?)\]', args)
            if m:
                execs.append([m.group(1), m.group(2)[:200]])
            continue
        paths = re.findall(r'"(/[^"]*)"', args)
        for path in paths[:2]:
            if call in ("mkdir", "mkdirat", "creat", "rename", "renameat", "renameat2", "symlink", "symlinkat", "unlink", "unlinkat"):
                created.add(path)
            elif result.startswith("-"):
                absent.add(path)
            else:
                found.setdefault(path, call)
    return {"found": found, "absent": sorted(absent), "execs": execs, "connects": sorted(connects), "mutations": sorted(created)}


def _plant_home(adapter, original_wct):
    marker = "HOSTILE-MARKER-D4"

    def plant(paths, profile):
        manifest = original_wct(paths, profile)
        home = paths["home"]
        for rel, body in {
            ".claude/skills/hc/SKILL.md": f"---\nname: hc\ndescription: {marker}-home-claude\n---\n{marker}\n",
            ".codex/skills/hx/SKILL.md": f"---\nname: hx\ndescription: {marker}-home-codex\n---\n{marker}\n",
            ".agents/skills/ha/SKILL.md": f"---\nname: ha\ndescription: {marker}-home-agents\n---\n{marker}\n",
            ".omp/agent/skills/ho/SKILL.md": f"---\nname: ho\ndescription: {marker}-home-omp\n---\n{marker}\n",
            ".cursor/mcp.json": json.dumps({"mcpServers": {"evil-home-mcp": {"type": "http", "url": "http://127.0.0.1:31098/mcp"}}}),
            ".claude.json": json.dumps({"mcpServers": {"evil-claude-json": {"type": "http", "url": "http://127.0.0.1:31097/mcp"}}}),
            ".codeium/windsurf/mcp_config.json": json.dumps({"mcpServers": {"evil-ws": {"type": "http", "url": "http://127.0.0.1:31096/mcp"}}}),
            ".omp/agent/AGENTS.md": f"{marker}-home-agents-md\n",
            ".claude/CLAUDE.md": f"{marker}-home-claude-md\n",
            ".env": "HOSTILE_ENV_HOME=1\n",
            ".omp/agent/.env": "HOSTILE_ENV_AGENT=1\n",
        }.items():
            target = home / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body)
        return manifest

    return plant


def discovery_probe(exe: str) -> dict:
    """Real binary, real sandbox, hostile project + hostile HOME, pre-launch refusal bypassed.

    Run 1 traces every path/program/connection with strace (the seccomp filter is allow-all only so strace
    can trace; inference is not served because the relay authorizes the launcher-started process, not strace).
    Run 2 is a normal run (real filter, real relay) whose effects are read from the trusted observer evidence.
    """
    import omp_rig  # noqa: WPS433
    from adapters import omp as adapter

    marker = "HOSTILE-MARKER-D4"
    result: dict = {"method": (
        "run 1: strace -f of the real omp/18.0.11 in the real sandbox (allow-all seccomp so strace can trace), hostile project and HOME planted, "
        "pre-launch refusal bypassed; run 2: normal run with the same hostile sources, effects read from the trusted observer evidence")}
    original_argv, original_filter = adapter.omp_argv, adapter.seccomp70.build_deny_filter
    original_pd, original_hd, original_wct = adapter.PROJECT_DISCOVERY_SOURCES, adapter.HOME_DISCOVERY_SOURCES, adapter._write_control_tree
    original_vc = adapter.validate_ambient_discovery_closure

    def run(traced: bool) -> tuple[dict, Path]:
        work = Path(tempfile.mkdtemp(prefix="omp-discovery-"))
        try:
            def traced_argv(profile, prompt):
                return ["/usr/bin/strace", "-f", "-qq", "-s", "200", "-e", f"trace={SYSCALL_TRACE}", "-o",
                        "/workspace/.omp-strace.txt", *original_argv(profile, prompt)]

            adapter._write_control_tree = _plant_home(adapter, original_wct)
            adapter.PROJECT_DISCOVERY_SOURCES = ()
            adapter.HOME_DISCOVERY_SOURCES = ()
            adapter.validate_ambient_discovery_closure = lambda project, env: []
            if traced:
                adapter.omp_argv = traced_argv
                adapter.seccomp70.build_deny_filter = lambda names=None: b"\x06\x00\x00\x00\x00\x00\xff\x7f"
            rig = omp_rig.Rig(work, project_files=hostile_project_files(), timeout_s=120)
            summary = rig.run(omp_rig.scenario_steps(
                omp_rig.call("bash", command="printenv | grep -c HOSTILE; ls -a /workspace | tr '\\n' ' '"),
                omp_rig.text("done")), out_name="probe")
            out = Path(summary["_out"])
            keep = Path(tempfile.mkdtemp(prefix="omp-discovery-keep-"))
            shutil.copytree(out, keep / "out", symlinks=True)
            return summary, keep / "out"
        finally:
            adapter.omp_argv, adapter.seccomp70.build_deny_filter = original_argv, original_filter
            adapter.PROJECT_DISCOVERY_SOURCES, adapter.HOME_DISCOVERY_SOURCES, adapter._write_control_tree = original_pd, original_hd, original_wct
            adapter.validate_ambient_discovery_closure = original_vc
            shutil.rmtree(work, ignore_errors=True)

    summary1, out1 = run(True)
    trace_file = out1 / "final-tree" / ".omp-strace.txt"
    parsed = parse_strace(trace_file.read_text(errors="replace")) if trace_file.exists() else parse_strace("")
    probed = sorted({p for p in list(parsed["found"]) + parsed["absent"]})
    result.update({
        "paths_probed_project": sorted(p for p in probed if p.startswith("/workspace/")),
        "paths_probed_home": sorted(p for p in probed if p.startswith("/home/agent/")),
        "paths_probed_ancestors_and_other": sorted(p for p in probed if not p.startswith(("/workspace/", "/home/agent/", "/usr", "/lib", "/proc", "/dev", "/sys", "/etc", "/tmp", "/opt/", "/bin", "/sbin")) and p != "/"),
        "programs_executed": parsed["execs"],
        "network_connect_attempts": parsed["connects"],
        "paths_created_or_removed": [p for p in parsed["mutations"] if p.startswith(("/workspace/", "/home/agent/", "/tmp"))][:200],
    })
    summary2, out2 = run(False)
    observer = [json.loads(l) for l in (out2 / "adapter-artifacts" / "observer-evidence.jsonl").read_text().splitlines()]
    requests = [json.loads(base64.b64decode(r["data"]["body_b64"])) for r in observer if r["kind"] == "request"]
    prompt = requests[0]["messages"][0]["content"] if requests else ""
    events = [json.loads(l) for l in (out2 / "events.normalized.jsonl").read_text().splitlines()]
    env_result = next((e["payload"]["result_content"] for e in events if e["kind"] == "tool_action" and e["status"] == "result"), "")
    result["effects_observed_through_the_trusted_observer"] = {
        "hostile_markers_that_reached_the_system_prompt": sorted(set(re.findall(r"HOSTILE-MARKER-D4-[A-Za-z0-9-]+", prompt))),
        "skills_in_runtime_catalog": sorted(adapter.parse_catalog(prompt)[0] and [row["name"] for row in adapter.parse_catalog(prompt)[0]]),
        "native_tools_in_request": [t["function"]["name"] for t in requests[0].get("tools", [])] if requests else [],
        "printenv_HOSTILE_count_and_workspace_listing_seen_by_the_agent": env_result[:400],
        "hook_or_extension_or_bunfig_code_ran": [n for n in ("HOOK-RAN", "HOOK2-RAN", "EXT-RAN", "BUNFIG-RAN") if (out2 / "final-tree" / n).exists()],
        "evidence_state": summary2["evidence_state"],
        "adapter_detected": (summary2.get("profile_claim_errors") or [])[:8],
    }
    for keep in (out1.parent, out2.parent):
        shutil.rmtree(keep, ignore_errors=True)
    return result


PROVIDER_MANAGED_STATE = [
    {"name": "auto-retry / model fallback", "disposition": "disabled", "mechanism": "retry.enabled=false, retry.maxRetries=0, retry.modelFallback=false",
     "evidence": "one accounted inference request per assistant message; auto_retry_* events are inadmissible; test_provider_error_is_a_single_accounted_request_never_a_hidden_retry and test_provider_managed_retry_appears_in_evidence_and_is_inadmissible_when_enabled"},
    {"name": "provider-layer retry of transient errors and empty completions (openai-completions)", "disposition": "frozen+observed (cannot be disabled)",
     "mechanism": "hard-coded in the exact build below OMP's retry setting: one resend after a transient provider error, up to two after an empty completion, always the byte-identical request, only before any content reached the agent",
     "evidence": "the observer records every resend; the adapter accepts it only when identical to its predecessor after a transient/empty response, within those limits, and retains the ledger in usage_timing.provider_layer_retries; profile unknown provider-layer-retry-of-transient-errors-and-empty-completions is arm-neutral"},
    {"name": "compaction / context promotion / branch summary", "disposition": "disabled", "mechanism": "compaction.enabled/midTurnEnabled/asyncEnabled/idleEnabled=false, contextPromotion.enabled=false, branchSummary.enabled=false",
     "evidence": "auto_compaction_* events inadmissible; any extra model call is an unaccounted observer request"},
    {"name": "title / recap / background summaries", "disposition": "disabled", "mechanism": "--no-title, PI_NO_TITLE=1, title.refreshOnReplan via recap.enabled=false, features.unexpectedStopDetection=none",
     "evidence": "extra observer request without a native assistant message fails the request/assistant-message accounting"},
    {"name": "advisor / prewalk / plan / goal", "disposition": "disabled", "mechanism": "advisor.enabled, prewalk.enabled, task.prewalk, plan.enabled, goal.enabled = false; task/hub tools not exposed",
     "evidence": "model_changed / goal_updated events inadmissible; observer request accounting"},
    {"name": "memory / auto-learning / hindsight / mnemopi / sharpshooter", "disposition": "disabled", "mechanism": "memory.backend=off, memories.enabled=false, autolearn.enabled=false; memory tools not exposed; network unreachable",
     "evidence": "effective-settings probe equals the inventory for every key; observer request accounting"},
    {"name": "TTSR rule injection / todo reminders / loop guards / magic keywords", "disposition": "disabled", "mechanism": "ttsr.enabled=false, todo.reminders=false, model.loopGuard/toolCallLoopGuard.enabled=false, magicKeywords.enabled=false",
     "evidence": "ttsr_triggered/todo_reminder events inadmissible; effective-settings probe"},
    {"name": "session state / artifacts", "disposition": "frozen+observed", "mechanism": "--no-session; runtime state is confined to the run-owned HOME and inventoried after the run (runtime-home-inventory.json)",
     "evidence": "runtime-home inventory classes are exactly control + omp-runtime-state in a normal run"},
    {"name": "extension / plugin / hook discovery", "disposition": "disabled", "mechanism": "--no-extensions, --no-rules, --no-lsp, skills/commands enable* flags false, mcp.enableProjectConfig=false, run-owned HOME holds no plugin/extension/hook path (pre-launch refusal)",
     "evidence": "hostile project/HOME effect test: no hook/extension/bunfig code ran; unit tests refuse every identified source"},
    {"name": "OMP / Claude / Codex / Gemini / OpenCode / Cursor / Windsurf / VS Code / GitHub-agents / standalone-MCP discovery", "disposition": "disabled or refused",
     "mechanism": "skills.enable{Codex,Claude,Pi,Agents}{User,Project}=false plus skills.customDirectories=[/opt/ssdp/skills]; commands.enable*=false; mcp.enableProjectConfig=false; pre-launch refusal of every identified project/HOME source; system-prompt structure checks for context/override/append",
     "evidence": "discovery.effects_observed_through_the_trusted_observer; the only source that reached the runtime in the hostile probe (.github/copilot-instructions.md, HOME SYSTEM/APPEND/AGENTS.md) is detected from the observed prompt"},
    {"name": "ancestor-directory discovery", "disposition": "closed by substrate", "mechanism": "the sandbox root holds only /workspace, /home/agent, /usr, /etc, /opt, /tmp, /proc, /dev; the project has no host ancestors",
     "evidence": "test_ancestor_directory_discovery_sees_nothing"},
    {"name": "dotenv autoload (HOME .env, ~/.omp/.env, ~/.omp/agent/.env)", "disposition": "refused pre-launch", "mechanism": "run-owned HOME is created empty; any .env is refused; process cwd is `/` and project .env/bunfig.toml are not read (observed)",
     "evidence": "hostile probe: HOME .env variables entered OMP's environment, project .env did not; HOME sources are refused before launch"},
    {"name": "startup network activity (model catalog refresh, update check, telemetry, autoqa push)", "disposition": "unreachable + disabled", "mechanism": "empty network namespace; startup.checkUpdate=false, dev.autoqa=false, marketplace.autoUpdate=off",
     "evidence": "network_connect_attempts in the strace inventory all fail with the empty netns; no effect on runtime state"},
    {"name": "hardware/host fingerprint in the system prompt (`<workstation>` block)", "disposition": "claim-scoped: arm-neutral provider-managed", "mechanism": "host-derived OS/kernel/CPU/GPU lines are recorded by the observer; identical for both arms on one host",
     "evidence": "profile provider_managed_unknowns entry host-derived-system-prompt-workstation-block (arm-neutral)"},
    {"name": "exact consumed SSDP material (T1/T7/T8)", "disposition": "observable", "mechanism": "tool results the model received are compared, line-numbered, with the exact mounted package files (consumed_resource)",
     "evidence": "test_ordinary_root_selection_from_successful_skill_read_with_exact_consumed_resource; read truncation (300-line default) is recorded as partial with line ranges, not as exact"},
]

ENVIRONMENT = {
    "subject_environment": "cleared; only PATH, HOME, XDG_CONFIG_HOME, XDG_CACHE_HOME, TMPDIR/TMP/TEMP, TERM, NO_COLOR, LANG, TZ, PI_NO_TITLE are set",
    "provider_credential_variables_absent_by_construction": list(sorted(__import__("adapters.omp", fromlist=["x"]).CREDENTIAL_ENV_NAMES)),
    "omp_environment_variables_found_in_the_binary": "PI_* and OMP_* names (for example PI_CODING_AGENT_DIR, PI_DATA_DIR, PI_SMOL_MODEL, PI_SLOW_MODEL, PI_PLAN_MODEL, PI_NO_TITLE, PI_AUTO_QA_PUSH, PI_NO_PTY, PI_DISABLE_UUTILS_BUILTINS, PI_SHELL_PREFIX, PI_BASH_NO_CI, OMP_AUTH_BROKER_*, OMP_DAEMON_*, OMP_LSP_MUX_*); none is set by the profile beyond PI_NO_TITLE, and the environment is cleared so none can enter from the host",
    "embedded_shell_note": "the bash tool runs OMP's embedded shell (in-process builtins, external commands as children of OMP); shellPath is not used by that path, so the sandbox, not a shell wrapper, is the process boundary",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--omp", default=os.path.expanduser("~/.local/bin/omp"))
    parser.add_argument("--out", default=str(HERE / "omp-build-inventory-18.0.11.json"))
    parser.add_argument("--settings-only", action="store_true", help="skip the sandboxed discovery probes")
    parser.add_argument("--discovery-json", default=None, help="merge a previously captured discovery section")
    args = parser.parse_args()
    exe = args.omp
    if hashlib.sha256(Path(exe).read_bytes()).hexdigest() != omp.OMP_BUILD["sha256"]:
        raise SystemExit("executable is not the exact frozen OMP build")
    existing = {}
    if Path(args.out).is_file():
        existing = json.loads(Path(args.out).read_text())
    inventory = {
        "schema": 1,
        "purpose": "empirical exact-build inventory of OMP configuration, discovery and provider-managed state; evidence, not authority",
        "build": omp.OMP_BUILD,
        "settings": settings_inventory(exe),
        "discovery": existing.get("discovery") or {},
        "provider_managed_state": PROVIDER_MANAGED_STATE,
        "environment": ENVIRONMENT,
    }
    if args.discovery_json:
        inventory["discovery"] = json.loads(Path(args.discovery_json).read_text())
    elif not args.settings_only:
        inventory["discovery"] = discovery_probe(exe)
    Path(args.out).write_text(json.dumps(inventory, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {inventory['settings']['count']} settings, "
          f"{len(inventory['settings']['frozen_keys_absent_from_build'])} frozen keys absent from build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
