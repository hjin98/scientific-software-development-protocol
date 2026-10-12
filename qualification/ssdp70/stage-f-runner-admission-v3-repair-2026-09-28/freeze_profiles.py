#!/usr/bin/env python3
"""Freeze fresh v3 executor/evaluator profiles from the current templates (checker-owned).

Only runtime version/build, reasoning configuration, profile id and provider-managed
unknown classifications are bound here; every other field is copied unchanged from the
reviewed template. The historical v1 frozen profiles are never read or modified.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

repo = Path(__file__).resolve().parents[3]
eval_dir = repo / "qualification/ssdp70/eval"
out = Path(__file__).resolve().parent / "profiles"
claude = Path(subprocess.check_output(["readlink", "-f", subprocess.check_output(["which", "claude"], text=True).strip()], text=True).strip())
version = subprocess.check_output(["claude", "--version"], text=True).split()[0]
binary_sha = hashlib.sha256(claude.read_bytes()).hexdigest()
UNKNOWNS = [
    {"classification": "arm-neutral", "name": "provider-backend-shard", "sensitive_claims": ["*"]},
    {"classification": "arm-neutral", "name": "provider-model-serving-revision-behind-alias", "sensitive_claims": ["*"]},
]
for role, tpl in (("executor", "claude-headless.template.json"), ("evaluator", "claude-evaluator-readonly.template.json")):
    profile = json.loads((eval_dir / "profiles" / tpl).read_text())
    profile["profile_id"] = f"claude-code-{version}-sonnet5-high-local-samjin-{role}-v3"
    profile["provider_runtime"] = {**profile["provider_runtime"], "version": version, "binary_sha256": binary_sha}
    profile["reasoning_configuration"] = {"effort": "high", "source": "checker-frozen-2026-09-28"}
    profile["provider_managed_unknowns"] = UNKNOWNS
    (out / f"{role}.frozen.json").write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(role, profile["profile_id"], version, binary_sha)
