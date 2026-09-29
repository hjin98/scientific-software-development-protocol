#!/usr/bin/env python3
"""DIAGNOSTIC ONLY - NOT runner-admission evidence.

Runs the frozen v2 profile's exact command shape through the actual adapter's realization
helpers, but with sandbox.failIfUnavailable relaxed in a *copy* of the settings so the
runtime can emit its init event on a host that lacks the required sandbox dependency.
The environment has no qualification auth source, so no model call, and therefore no tool
effect, can occur. Purpose: discover further blockers hidden behind the sandbox refusal.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[3]
eval_dir = repo / "qualification/ssdp70/eval"
sys.path.insert(0, str(eval_dir))
import core70
from adapters import claude as adapter

role, arms_json, outdir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
variant = sys.argv[4] if len(sys.argv) > 4 else "frozen-shape"  # or "no-restricted"
here = Path(__file__).resolve().parent
profile_path = here / "profiles" / f"{role}.frozen.json"
cap_path = eval_dir / "capabilities" / ("claude-headless.json" if role == "executor" else "claude-evaluator-readonly.json")
bundle = core70.load_profile(profile_path, cap_path)
arm = next(a for a in json.loads(arms_json.read_text())["arms"] if a["name"] == "p70")
with tempfile.TemporaryDirectory(prefix="ssdp70-diag-") as t:
    tmp = Path(t); project = tmp / "project"; private = tmp / "harness-private"
    project.mkdir(); private.mkdir(); (private / "stub").mkdir()
    (private / "side-effects.jsonl").write_text(""); home = private / "runtime-home"; home.mkdir()
    (project / ".qualification-tmp").mkdir()
    if role == "executor":
        shutil.copy2(eval_dir / "stub_tools/mediator.py", private / "mcp-server.py")
        (private / "mcp-server.py").chmod(0o500)
        (private / "mcp-account.txt").write_text("checker-agent-account\n")
        adapter.install_skills(Path(arm["skills_path"]), project)
    env = adapter.clean_env()
    env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"), "XDG_CACHE_HOME": str(home / ".cache"),
                "TMPDIR": str(project / ".qualification-tmp"), "TMP": str(project / ".qualification-tmp"), "TEMP": str(project / ".qualification-tmp")})
    doc = adapter.realize_containment(bundle.profile, project, env)
    settings_path = Path(doc["realization"]["settings_file"]); mcp_path = Path(doc["realization"]["mcp_config"])
    relaxed = json.loads(settings_path.read_text()); relaxed["sandbox"]["failIfUnavailable"] = False
    diag_settings = private / "diagnostic-settings.json"; diag_settings.write_text(json.dumps(relaxed, indent=2))
    p = bundle.profile
    cmd = ["claude", "-p", "Reply with the single word READY.", "--output-format", "stream-json", "--verbose", "--model", p["agent_model"],
           "--max-turns", str(p["budgets"]["max_turns"]), "--settings", str(diag_settings), "--mcp-config", str(mcp_path), "--strict-mcp-config",
           *(["--restricted"] if variant != "no-restricted" else []), "--permission-mode", p["permission_mode"], "--tools", ",".join(p["native_tools"]),
           "--allowedTools", " ".join(p["native_allowed_tools"]), "--disallowedTools", " ".join(p["native_disallowed_tools"]),
           "--effort", p["reasoning_configuration"]["effort"]]
    proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True, env=env, timeout=180, stdin=subprocess.DEVNULL)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{role}.diagnostic{'' if variant == 'frozen-shape' else '-' + variant}.trace.jsonl").write_text(proc.stdout.replace(str(tmp), "<checker-scratch>"))
    (outdir / f"{role}.diagnostic{'' if variant == 'frozen-shape' else '-' + variant}.stderr.txt").write_text(proc.stderr.replace(str(tmp), "<checker-scratch>"))
    obs = adapter.runtime_observation(proc.stdout)
    errs = core70.validate_runtime_observation(bundle, obs)
    init = next((json.loads(l) for l in proc.stdout.splitlines() if '"subtype":"init"' in l), {})
    summary = {"variant": variant, "init_ssdp_skills": [x for x in ((s if isinstance(s, str) else s.get("name")) for s in init.get("skills") or []) if x in adapter.SSDP_SKILLS], "role": role, "returncode": proc.returncode, "init_present": bool(init),
               "init_permissionMode": init.get("permissionMode"), "init_tools": init.get("tools"),
               "init_mcp_servers": init.get("mcp_servers"), "init_model": init.get("model"), "init_version": init.get("claude_code_version"),
               "init_apiKeySource": init.get("apiKeySource"), "init_skills_count": len(init.get("skills") or []),
               "init_capabilities": init.get("capabilities"), "init_messaging_socket_path": bool(init.get("messaging_socket_path")),
               "init_memory_paths": init.get("memory_paths"), "runtime_observation_errors": errs}
    (outdir / f"{role}.diagnostic{'' if variant == 'frozen-shape' else '-' + variant}.summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True).replace(str(tmp), "<checker-scratch>") + "\n")
    print(json.dumps(summary, indent=1, sort_keys=True).replace(str(tmp), "<checker-scratch>"))
