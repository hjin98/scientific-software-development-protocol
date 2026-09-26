#!/usr/bin/env python3
"""Run the frozen Stage F live matrix for two variants with counterbalanced order.

Evidence tooling only (see harness.py). Each (scenario, repetition) pair runs both
variants back to back, alternating which variant goes first, so slow service/model
drift does not systematically favor one variant.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent


def jobs(scenarios: dict, layer: str, reps: int, variants: dict[str, Path], only: set[str] | None = None) -> list[tuple[str, list[str]]]:
    out = []
    names = list(variants)
    if layer == "selection":
        items = [(s, split) for split in ("development", "holdout") for s in scenarios["selection"][split]]
        for index, (item, split) in enumerate(items):
            for rep in range(reps):
                order = names if (index + rep) % 2 == 0 else names[::-1]
                for variant in order:
                    run_id = f"{item['id']}-{variant}-r{rep}"
                    out.append((run_id, ["live", "--dist", str(variants[variant]), "--prompt", item["task"], "--max-turns", "3", "--mode", "select"]))
    elif layer == "route":
        probes = scenarios["final"]["route_probes"]
        for index, item in enumerate(probes["cases"]):
            if only and item["id"] not in only:
                continue
            prompt = probes["prompt"].format(root=item["root"], task=item["task"])
            for rep in range(reps):
                order = names if (index + rep) % 2 == 0 else names[::-1]
                for variant in order:
                    run_id = f"{item['id']}-{variant}-r{rep}"
                    out.append((run_id, ["live", "--dist", str(variants[variant]), "--prompt", prompt, "--max-turns", str(probes["max_turns"]), "--mode", "select"]))
    else:
        items = [(s, split) for split in ("development", "holdout", "rework_holdout", "redesign_challenge") for s in scenarios["trajectories"].get(split, [])]
        items = [(s, split) for s, split in items if not only or s["id"] in only]
        for index, (item, split) in enumerate(items):
            fixture = HERE / "fixtures" / item["fixture"]
            prompt = f"Use the {item['root']} skill. " + (fixture / "TASK.md").read_text(encoding="utf-8").strip()
            for rep in range(reps):
                order = names if (index + rep) % 2 == 0 else names[::-1]
                for variant in order:
                    run_id = f"{item['id']}-{variant}-r{rep}"
                    cmd = ["live", "--dist", str(variants[variant]), "--fixture", str(fixture), "--prompt", prompt, "--max-turns", "60", "--mode", "trajectory"]
                    if item.get("governing_version"):
                        cmd += ["--governing-version", str(item["governing_version"])]
                    out.append((run_id, cmd))
    return out


def summarize(out: Path, layer: str) -> dict:
    """Aggregate per-run summaries; selection runs are scored against admissible sets."""
    scenarios = yaml.safe_load((HERE / "scenarios.yaml").read_text(encoding="utf-8"))
    admissible = {s["id"]: set(s["admissible"]) for split in ("development", "holdout") for s in scenarios["selection"][split]}
    rows = {}
    for summary_path in sorted(out.glob("*/summary.json")):
        run_id = summary_path.parent.name
        scenario, variant, rep = run_id.rsplit("-", 2)
        data = json.loads(summary_path.read_text(encoding="utf-8"))
        ssdp = [s for s in data.get("skills_invoked", []) if s in {n for names in admissible.values() for n in names} or s in {
            "scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation",
            "software-documentation", "software-maintenance-audit", "repository-hygiene"}]
        row = {"scenario": scenario, "variant": variant, "rep": rep, "ssdp_skills": ssdp,
               "protocol_reads": data.get("protocol_reads", []), "protocol_read_bytes": data.get("protocol_read_bytes_on_disk", 0),
               "num_turns": data.get("num_turns"), "cost_usd": data.get("total_cost_usd"), "input_tokens": data.get("input_tokens_total"),
               "output_tokens": data.get("output_tokens"), "oracle": data.get("oracle"),
               "entry_and_burden": data.get("entry_and_burden")}
        if layer == "selection":
            allowed = admissible[scenario]
            row["outcome"] = (
                "correct-none" if not allowed and not ssdp else
                "false-activation" if not allowed and ssdp else
                "missed" if allowed and not ssdp else
                "admissible" if ssdp[0] in allowed and set(ssdp) <= allowed else
                "wrong-or-extra"
            )
        assessment = summary_path.parent / "assessment.json"
        if assessment.is_file():
            row["assessment"] = json.loads(assessment.read_text(encoding="utf-8")).get("verdict")
        rows[run_id] = row
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summarize", action="store_true", help="aggregate existing runs instead of executing")
    parser.add_argument("--layer", choices=("selection", "route", "trajectory"), required=True)
    parser.add_argument("--variant", action="append", default=[], help="name=path/to/dist/skills")
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--model", default="claude-sonnet-5")
    parser.add_argument("--only", action="append", default=[], help="restrict to these scenario ids")
    args = parser.parse_args()
    if args.summarize:
        print(json.dumps(summarize(args.out, "selection" if args.layer == "selection" else "trajectory"), indent=1, sort_keys=True))
        return 0
    variants = dict(v.split("=", 1) for v in args.variant)
    variants = {k: Path(v) for k, v in variants.items()}
    scenarios = yaml.safe_load((HERE / "scenarios.yaml").read_text(encoding="utf-8"))
    todo = jobs(scenarios, args.layer, args.reps, variants, set(args.only))

    def run(job: tuple[str, list[str]]) -> tuple[str, int]:
        run_id, cmd = job
        target = args.out / run_id
        if (target / "summary.json").is_file():
            return run_id, 0
        proc = subprocess.run([sys.executable, str(HERE / "harness.py"), *cmd, "--out", str(target), "--model", args.model], capture_output=True, text=True)
        if proc.returncode:
            (args.out / f"{run_id}.error.txt").write_text(proc.stderr[-4000:], encoding="utf-8")
        return run_id, proc.returncode

    args.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for run_id, code in pool.map(run, todo):
            print(json.dumps({"run": run_id, "exit": code}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
