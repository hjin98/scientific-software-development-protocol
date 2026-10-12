#!/usr/bin/env python3
"""Freeze the v4 executor/evaluator profiles from the current templates (implementer-produced; the fresh
independent checker must re-freeze independently and compare digests).

Only runtime version/build, reasoning configuration, profile id and provider-managed unknown
classifications are bound here; every other field is copied unchanged from the reviewed template. The
historical v1/v2/v3 frozen profiles are never read or modified. Writes profiles/*.frozen.json and
identities.json (document, key, capability-manifest and tooling digests).
"""
import hashlib, json, subprocess, sys
from pathlib import Path

repo = Path(__file__).resolve().parents[3]
eval_dir = repo / "qualification/ssdp70/eval"
sys.path.insert(0, str(eval_dir))
import core70  # noqa: E402

here = Path(__file__).resolve().parent
out = here / "profiles"
out.mkdir(exist_ok=True)
claude = Path(subprocess.check_output(["readlink", "-f", subprocess.check_output(["which", "claude"], text=True).strip()], text=True).strip())
version = subprocess.check_output(["claude", "--version"], text=True).split()[0]
binary_sha = hashlib.sha256(claude.read_bytes()).hexdigest()
UNKNOWNS = [
    {"classification": "arm-neutral", "name": "provider-backend-shard", "sensitive_claims": ["*"]},
    {"classification": "arm-neutral", "name": "provider-model-serving-revision-behind-alias", "sensitive_claims": ["*"]},
]
identities = {}
for role, tpl, caps in (
    ("executor", "claude-headless.template.json", "claude-headless.json"),
    ("evaluator", "claude-evaluator-readonly.template.json", "claude-evaluator-readonly.json"),
):
    profile = json.loads((eval_dir / "profiles" / tpl).read_text())
    profile["profile_id"] = f"claude-code-{version}-sonnet5-high-local-samjin-{role}-v4"
    profile["provider_runtime"] = {**profile["provider_runtime"], "version": version, "binary_sha256": binary_sha}
    profile["reasoning_configuration"] = {"effort": "high", "source": "implementer-frozen-2026-09-29"}
    profile["provider_managed_unknowns"] = UNKNOWNS
    path = out / f"{role}.frozen.json"
    path.write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    bundle = core70.load_profile(path, eval_dir / "capabilities" / caps)
    identities[role] = {
        "capability_manifest_sha256": bundle.capability_manifest_sha256,
        "document_sha256": core70.sha256_file(path),
        "profile_id": profile["profile_id"],
        "profile_key_sha256": bundle.profile_key_sha256,
    }
    print(role, profile["profile_id"], version, binary_sha)
tracked = [
    "adapters/claude.py", "assess70.py", "capabilities/claude-evaluator-readonly.json",
    "capabilities/claude-headless.json", "core70.py", "harness70.py",
    "profiles/claude-evaluator-readonly.template.json", "profiles/claude-headless.template.json",
    "stub_tools/mediator.py",
]
identities["files"] = {name: core70.sha256_file(eval_dir / name) for name in tracked}
identities["runtime"] = {"version": version, "binary_sha256": binary_sha}
(here / "identities.json").write_text(json.dumps(identities, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(identities, indent=2, sort_keys=True))
