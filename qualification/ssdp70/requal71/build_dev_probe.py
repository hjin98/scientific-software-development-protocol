#!/usr/bin/env python3
"""Analyst tool: build the SD-5 development-probe inputs (runbook Phase D).

Writes, under --work/dev: a deterministic-entry overlay of the disclosed 2026-09-28 corpus (roots from
dev-probe-roots.json, 60-turn main panel) and commands.json (harness matrix in probe mode, p66 vs p71,
one command per fixture family). Development purpose only (contract §1 item 7). Opens no custody key.
"""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent / "eval"
sys.path.insert(0, str(EVAL))
from adapters import omp  # noqa: E402

CHUNKS = {"dev-s": ("fx-s",), "dev-p": ("fx-p",), "dev-a": ("fx-a", "fx-inv")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=Path, required=True, help="disclosed corpus root (2026-09-28 store corpus/)")
    ap.add_argument("--requirements", type=Path, required=True)
    ap.add_argument("--oracles", type=Path, required=True)
    ap.add_argument("--roots", type=Path, default=HERE / "dev-probe-roots.json")
    ap.add_argument("--profile", type=Path, required=True, help="derived 60-turn main key profile")
    ap.add_argument("--capabilities", type=Path, required=True)
    ap.add_argument("--arms-manifest", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    dev = a.work / "dev"
    if (dev / "corpus").exists() or (dev / "commands.json").exists():
        sys.exit(f"refusing to overwrite {dev}")
    roots = json.loads(a.roots.read_text())
    root_of = {ep: root for root, row in roots["overrides"].items() for ep in row["episodes"]}
    episodes = yaml.safe_load((a.corpus / "manifest.yaml").read_text())["episodes"]
    kept = []
    for ep in episodes:
        if ep["id"] in roots["excluded"]["episodes"]:
            continue
        kept.append({**ep, "entry": f"pinned:{root_of.get(ep['id'], roots['default_root'])}", "max_turns": 60, "replicates": 1, "panel": "main"})
    (dev / "corpus").mkdir(parents=True)
    for sub, field in (("fixtures", "fixture"), ("stubs", "stub")):
        for name in sorted({ep[field] for ep in kept if ep.get(field)}):
            shutil.copytree(a.corpus / sub / name, dev / "corpus" / sub / name, symlinks=True)
    (dev / "corpus" / "manifest.yaml").write_text(yaml.safe_dump({"schema": "ssdp70-corpus-manifest/1", "note": "SD-5 development overlay of the disclosed 2026-09-28 corpus; deterministic entry", "episodes": kept}, sort_keys=False))
    out_root = dev / "runs"
    if not any(r.resolve() in out_root.resolve().parents for r in omp.RUN_REALIZATION_ROOTS):
        sys.exit(f"{out_root} is not beneath an approved OMP realization root")
    commands = []
    for key, prefixes in CHUNKS.items():
        ids = [ep["id"] for ep in kept if ep["fixture"].startswith(prefixes)]
        argv = ["/usr/bin/python3", str(EVAL / "harness70.py"), "matrix", "--corpus", str(dev / "corpus"), "--arms-manifest", str(a.arms_manifest),
                "--arm", "p66", "--arm", "p71", "--out", str(out_root / key), "--profile", str(a.profile), "--capabilities", str(a.capabilities),
                "--requirements", str(a.requirements), "--oracles", str(a.oracles), "--adapter", "omp", "--mode", "probe", "--parallel", str(a.parallel)]
        for i in ids:
            argv += ["--only", i]
        commands.append({"key": key, "episodes": len(ids), "argv": argv, "shell": shlex.join(argv)})
    (dev / "commands.json").write_text(json.dumps({"schema": 1, "purpose": "development", "commands": commands}, indent=2) + "\n")
    print(json.dumps({"episodes": len(kept), "runs": 2 * len(kept), "chunks": {c["key"]: c["episodes"] for c in commands},
                      "roots": {r: sum(1 for e in kept if e["entry"] == f"pinned:{r}") for r in sorted({e["entry"][7:] for e in kept})}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
