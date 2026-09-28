#!/usr/bin/env python3
"""Protocol 7.0 composite-episode harness (non-normative evidence tooling).

Runs custodian-authored episodes through Claude Code headless with one protocol arm
installed as project skills. It captures what the frozen qualification contract §6
requires the evaluator to receive:

- the complete trace, final report, diff and new files;
- every scripted-delegate instruction and issue-tracker read/write in a side-effect log;
- the final issue store and any attempted out-of-tree or network action seen in the trace;
- skill selection, SSDP reads and new-owner read indices for the R2 adjudication;
- a per-run catalog isolation check (the run is void if it fails).

The harness never reads keys or expected answers. Deterministic custodian oracles, when
given, run after the agent finishes against a copy of the final tree. The executing agent
cannot reach them.

Subcommands:
  episode  run one manifest episode for one arm
  matrix   run every manifest episode for all arms, alternating arm order per episode/replicate
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "qualification" / "ssdp66" / "eval"))
import harness as h66  # noqa: E402  (reused: trace reduction, burden accounting, env isolation)

OWNER = "scientific-inspectability-and-initiative.md"
SSDP = [name for name, _ in h66.SKILLS]
NETWORK_RE = re.compile(r"\b(?:curl|wget|nc|ssh|scp|ftp)\s|urllib|requests\.|http\.client|socket\.|https?://")
ABS_WRITE_RE = re.compile(r"(?:>>?|\btee\s+(?:-a\s+)?|\b(?:cp|mv|touch|mkdir)\s+(?:-\w+\s+)*)\s*(/(?!dev/null)[^\s\"';|&)]+)")
ALLOWED = ("Skill Read Glob Grep Edit Write TodoWrite Bash(python:*) Bash(python3:*) Bash(git:*) Bash(ls:*) "
           "Bash(cat:*) Bash(grep:*) Bash(find:*) Bash(head:*) Bash(tail:*) Bash(wc:*) Bash(sed -n:*)")


def load_manifest(corpus: Path) -> list[dict]:
    data = yaml.safe_load((corpus / "manifest.yaml").read_text(encoding="utf-8"))
    return data["episodes"] if isinstance(data, dict) else data


def _yaml_tree_to_json(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if path.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)
        elif path.suffix in {".yaml", ".yml"}:
            (dst / rel.with_suffix(".json")).parent.mkdir(parents=True, exist_ok=True)
            (dst / rel.with_suffix(".json")).write_text(json.dumps(yaml.safe_load(path.read_text(encoding="utf-8")), default=str), encoding="utf-8")
        else:
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, dst / rel)


def build_project(corpus: Path, episode: dict, project: Path) -> None:
    fixture = corpus / "fixtures" / episode["fixture"]
    project.mkdir(parents=True)
    script = fixture / "build_history.sh"
    if script.is_file():
        subprocess.run(["bash", str(script)], cwd=project, check=True, capture_output=True)
    if (fixture / "project").is_dir():
        shutil.copytree(fixture / "project", project, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
    tools = project / "tools"
    tools.mkdir(exist_ok=True)
    for name in ("delegate.py", "issues.py"):
        shutil.copy(HERE / "stub_tools" / name, tools / name)
    if not (project / ".git").is_dir():
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    (project / ".git" / "info" / "exclude").write_text("__pycache__/\n*.pyc\n.claude/\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=project, check=True)
    subprocess.run(["git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval", "commit", "-qm", "fixture", "--allow-empty"],
                   cwd=project, check=True)


def catalog_isolation(lines: list[str]) -> dict:
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            skills = [s if isinstance(s, str) else s.get("name", "") for s in event.get("skills") or []]
            counts = {name: skills.count(name) for name in SSDP}
            ok = all(count == 1 for count in counts.values())
            return {"ok": ok, "ssdp_counts": counts, "catalog": skills}
    return {"ok": False, "reason": "no init event"}


def owner_reads(reduced: list[dict]) -> list[int]:
    return [i for i, e in enumerate(reduced) if e.get("tool") in {"Read", "Grep", "Bash", "Glob"} and OWNER in e.get("input", "")]


def outside_actions(reduced: list[dict], project: Path) -> dict:
    network, writes = [], []
    for i, e in enumerate(reduced):
        if e.get("tool") != "Bash":
            continue
        command = h66._shell(e.get("input", ""))
        if NETWORK_RE.search(command):
            network.append({"index": i, "command": command[:200]})
        for match in ABS_WRITE_RE.finditer(command):
            if not match.group(1).startswith(str(project)):
                writes.append({"index": i, "target": match.group(1), "command": command[:200]})
    return {"network_attempts": network, "out_of_tree_write_attempts": writes}


def run_episode(corpus: Path, episode: dict, arm: str, dist: Path, out: Path, model: str, oracles: Path | None) -> dict:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="ssdp70-") as tmp:
        tmp = Path(tmp)
        project, stub, log = tmp / "project", tmp / "stub", tmp / "side-effects.jsonl"
        build_project(corpus, episode, project)
        stub.mkdir()
        if episode.get("stub"):
            _yaml_tree_to_json(corpus / "stubs" / episode["stub"], stub)
        log.write_text("", encoding="utf-8")
        h66.install_variant(dist, project)
        entry = episode.get("entry", "ordinary")
        prompt = episode["prompt"].strip()
        if entry.startswith("pinned:"):
            prompt = f"Use the {entry.split(':', 1)[1]} skill. " + prompt
        env = h66._clean_env()
        env.update({"SSDP70_STUB_DIR": str(stub), "SSDP70_SIDE_EFFECT_LOG": str(log), "SSDP70_ACCOUNT": episode.get("account") or "agent-account"})
        cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model,
               "--max-turns", str(episode.get("max_turns", 60)), "--setting-sources", "project,local",
               "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED, "--disallowedTools", "Agent WebFetch WebSearch"]
        started = time.time()
        proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True, env=env, timeout=3600, stdin=subprocess.DEVNULL)
        lines = proc.stdout.splitlines()
        (out / "trace.jsonl").write_text(proc.stdout, encoding="utf-8")
        reduced = h66.reduce_trace(lines)
        (out / "trace-reduced.json").write_text(json.dumps(reduced, indent=1) + "\n", encoding="utf-8")
        if proc.stderr:
            (out / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        summary = h66.parse_trace(lines)
        summary.update({
            "episode": episode["id"], "arm": arm, "model": model, "wall_s": round(time.time() - started, 1),
            "catalog_isolation": catalog_isolation(lines),
            "entry_and_burden": h66.entry_and_burden(reduced, None, dist),
            "new_owner_read_indices": owner_reads(reduced),
            "outside_actions": outside_actions(reduced, project),
        })
        summary["admissible"] = summary["catalog_isolation"]["ok"]
        shutil.copy(log, out / "side-effects.jsonl")
        if (stub / "issues").is_dir():
            shutil.copytree(stub / "issues", out / "issues-final")
        subprocess.run(["git", "add", "-A", "-N", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True)
        (out / "diff.patch").write_text(subprocess.run(["git", "diff", "--", ".", ":(exclude).claude"], cwd=project,
                                                       capture_output=True, text=True).stdout, encoding="utf-8")
        (out / "final-report.md").write_text(summary.get("final") or "", encoding="utf-8")
        shutil.copytree(project, out / "final-tree", ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
        if oracles is not None and (oracles / episode["id"]).is_dir():
            results = {}
            for check in sorted((oracles / episode["id"]).glob("check_*.py")):
                result = subprocess.run([sys.executable, str(check), str(out / "final-tree"), str(out)], capture_output=True, text=True)
                results[check.stem] = {"pass": result.returncode == 0, "detail": result.stdout.strip()[-2000:]}
            (out / "oracle.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("episode", "matrix"):
        p = sub.add_parser(name)
        p.add_argument("--corpus", type=Path, required=True)
        p.add_argument("--arm", action="append", required=True, help="name=path/to/dist/skills")
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--model", default="claude-sonnet-5")
        p.add_argument("--oracles", type=Path, default=None, help="custodian oracle dir (run post hoc only)")
        if name == "episode":
            p.add_argument("--id", required=True)
            p.add_argument("--rep", type=int, default=0)
        else:
            p.add_argument("--parallel", type=int, default=4)
            p.add_argument("--only", action="append", default=[])
    args = parser.parse_args(argv)
    arms = {k: Path(v) for k, v in (a.split("=", 1) for a in args.arm)}
    episodes = {e["id"]: e for e in load_manifest(args.corpus)}
    if args.cmd == "episode":
        (arm, dist), = arms.items()
        summary = run_episode(args.corpus, episodes[args.id], arm, dist, args.out / f"{args.id}-{arm}-r{args.rep}", args.model, args.oracles)
        print(json.dumps({k: summary[k] for k in ("episode", "arm", "admissible", "new_owner_read_indices", "wall_s")}))
        return 0
    names, jobs = list(arms), []
    for index, (episode_id, episode) in enumerate(episodes.items()):
        if args.only and episode_id not in args.only:
            continue
        for rep in range(int(episode.get("replicates", 1))):
            order = names if (index + rep) % 2 == 0 else names[::-1]
            jobs += [(episode, arm, rep) for arm in order]

    def run(job):
        episode, arm, rep = job
        target = args.out / f"{episode['id']}-{arm}-r{rep}"
        if (target / "summary.json").is_file():
            return target.name, "cached"
        try:
            run_episode(args.corpus, episode, arm, arms[arm], target, args.model, args.oracles)
            return target.name, "ok"
        except Exception as exc:  # recorded, never silently dropped
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / f"{target.name}.error.txt").write_text(repr(exc), encoding="utf-8")
            return target.name, "error"

    args.out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for name, status in pool.map(run, jobs):
            print(json.dumps({"run": name, "status": status}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
