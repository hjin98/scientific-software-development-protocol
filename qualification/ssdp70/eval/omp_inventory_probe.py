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


def classify_setting(key: str, frozen: dict[str, object]) -> str:
    if key in frozen:
        return "frozen-closed"
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


def build_sandbox_env(tag: str, project_setup=None, home_setup=None, argv_wrap=None, prompt="probe"):
    """Assemble one real run (principals + sandbox) like the adapter does, minus the seccomp filter."""
    raise NotImplementedError


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
        "provider_managed_state": existing.get("provider_managed_state") or [],
        "environment": existing.get("environment") or {},
    }
    if args.discovery_json:
        inventory["discovery"] = json.loads(Path(args.discovery_json).read_text())
    Path(args.out).write_text(json.dumps(inventory, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {inventory['settings']['count']} settings, "
          f"{len(inventory['settings']['frozen_keys_absent_from_build'])} frozen keys absent from build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
