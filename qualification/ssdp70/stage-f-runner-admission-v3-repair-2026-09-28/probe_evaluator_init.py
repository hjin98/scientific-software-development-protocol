#!/usr/bin/env python3
"""Unauthenticated live init probe of the frozen v3 evaluator profile through the real adapter launch path.

Mirrors assess70.py's bundle/private/HOME layout (checker-owned harmless bundle, no custody material).
No qualification auth source is present, so no model call and no tool effect can occur.
"""
import json, sys, tempfile
from pathlib import Path

repo = Path(__file__).resolve().parents[3]
ev = repo / "qualification/ssdp70/eval"
sys.path.insert(0, str(ev))
import core70
from adapters import claude as adapter

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
here = Path(__file__).resolve().parent
bundle = core70.load_profile(here / "profiles/evaluator.frozen.json", ev / "capabilities/claude-evaluator-readonly.json")
with tempfile.TemporaryDirectory(prefix="ssdp70-assess-") as t:
    root = Path(t); bundle_root = root / "bundle"; private = root / "evaluator-private"; home = private / "runtime-home"
    bundle_root.mkdir(); private.mkdir(); home.mkdir(); (bundle_root / ".qualification-tmp").mkdir()
    (bundle_root / "EVIDENCE-MANIFEST.json").write_text('{"schema": 1, "files": []}\n')
    env = adapter.clean_env()
    env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"), "XDG_CACHE_HOME": str(home / ".cache"),
                "TMPDIR": str(bundle_root / ".qualification-tmp"), "TMP": str(bundle_root / ".qualification-tmp"), "TEMP": str(bundle_root / ".qualification-tmp")})
    containment = adapter.realize_containment(bundle.profile, bundle_root, env)
    launched = adapter.launch(bundle.profile, "Reply with the single word READY.", bundle_root, env)
    obs = adapter.runtime_observation(launched["stdout"])
    errors = core70.validate_launch_identity(bundle.profile, launched["command_identity"]) + core70.validate_runtime_observation(bundle, obs)
    clean = lambda x: x.replace(str(root), "<checker-scratch>")
    (out / "evaluator-init.jsonl").write_text(clean(launched["stdout"]))
    (out / "evaluator-stderr.txt").write_text(clean(launched["stderr"]).rstrip("\n") + "\n")
    summary = {"returncode": launched["returncode"], "runtime_observation": obs, "launch_and_runtime_validation_errors": errors,
               "command_identity": launched["command_identity"]}
    (out / "evaluator-probe-summary.json").write_text(clean(json.dumps(summary, indent=2, sort_keys=True, default=str)) + "\n")
    print(json.dumps({k: summary[k] for k in ("returncode", "launch_and_runtime_validation_errors")}, indent=1))
    print("tools", obs["tools"], "mcp", obs["mcp_servers"], "permission_mode", obs["permission_mode"])
