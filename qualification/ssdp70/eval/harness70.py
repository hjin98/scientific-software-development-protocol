#!/usr/bin/env python3
"""Protocol 7.0 composite-episode harness (non-normative evidence tooling).

Runs custodian-authored episodes through Claude Code headless with one protocol arm
installed as project skills. It captures what the frozen qualification contract requires:
complete raw and reduced traces, full tool-call inputs, final report/diff/tree, scripted
stand-in side effects, issue state, selection/owner-read evidence, catalog isolation and
an exact run identity binding the corpus, protocol package and harness bytes.

The harness never reads keys or expected answers. Deterministic custodian oracles, when
given, run only after the agent finishes against a copy of the final tree.

Subcommands:
  episode  run one manifest episode for one arm
  matrix   run every manifest episode for all arms; arm order is sequential within each
           episode/replicate pair and counterbalanced across pairs, while pairs may run
           concurrently.
"""
from __future__ import annotations

import argparse
import hashlib
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
import harness as h66  # noqa: E402

OWNER = "scientific-inspectability-and-initiative.md"
SSDP = [name for name, _ in h66.SKILLS]
NETWORK_RE = re.compile(
    r"\b(?:curl|wget|nc|ssh|scp|ftp|telnet)\b|"
    r"\bgit\s+(?:push|fetch|pull|clone|ls-remote)\b|"
    r"urllib|requests\.|http\.client|socket\.|https?://"
)
ABS_WRITE_RE = re.compile(
    r"(?:>>?|\btee\s+(?:-a\s+)?|\b(?:cp|mv|touch|mkdir)\s+(?:-\w+\s+)*)"
    r"\s*(/(?!dev/null)[^\s\"';|&)]+)"
)
PY_ABS_WRITE_RE = re.compile(
    r"(?:open|Path)\(\s*[\"'](/(?!dev/null)[^\"']+)[\"']"
)
ALLOWED = (
    "Skill Read Glob Grep Edit Write TodoWrite "
    "Bash(python:*) Bash(python3:*) Bash(git:*) Bash(ls:*) Bash(cat:*) Bash(grep:*) "
    "Bash(find:*) Bash(head:*) Bash(tail:*) Bash(wc:*) Bash(sed -n:*)"
)
DISALLOWED = "Agent WebFetch WebSearch"


def load_manifest(corpus: Path) -> list[dict]:
    data = yaml.safe_load((corpus / "manifest.yaml").read_text(encoding="utf-8"))
    return data["episodes"] if isinstance(data, dict) else data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path | None) -> str | None:
    if root is None or not root.exists():
        return None
    digest = hashlib.sha256()
    if root.is_file():
        digest.update(root.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(root.read_bytes())
        return digest.hexdigest()
    files = sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def stable_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run_identity(corpus: Path, episode: dict, arm: str, dist: Path, model: str, oracles: Path | None) -> dict:
    fixture = corpus / "fixtures" / episode["fixture"]
    stub = corpus / "stubs" / episode["stub"] if episode.get("stub") else None
    episode_oracles = oracles / episode["id"] if oracles is not None else None
    identity = {
        "schema": 1,
        "episode": episode["id"],
        "arm": arm,
        "model": model,
        "episode_config_sha256": stable_json_sha256(episode),
        "manifest_sha256": sha256_file(corpus / "manifest.yaml"),
        "fixture_tree_sha256": sha256_tree(fixture),
        "stub_tree_sha256": sha256_tree(stub),
        "dist_tree_sha256": sha256_tree(dist),
        "oracles_tree_sha256": sha256_tree(episode_oracles),
        "harness70_sha256": sha256_file(Path(__file__).resolve()),
        "harness66_sha256": sha256_file(Path(h66.__file__).resolve()),
        "stub_tools_sha256": sha256_tree(HERE / "stub_tools"),
        "allowed_tools": ALLOWED,
        "disallowed_tools": DISALLOWED,
    }
    identity["identity_sha256"] = stable_json_sha256(identity)
    return identity


def cache_valid(target: Path, identity: dict) -> bool:
    try:
        prior = json.loads((target / "run-identity.json").read_text(encoding="utf-8"))
        summary = json.loads((target / "summary.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return prior == identity and bool(summary.get("execution_ok")) and bool(summary.get("admissible"))


def _yaml_tree_to_json(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if path.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)
        elif path.suffix in {".yaml", ".yml"}:
            target = dst / rel.with_suffix(".json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(yaml.safe_load(path.read_text(encoding="utf-8")), default=str),
                encoding="utf-8",
            )
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
        shutil.copytree(
            fixture / "project", project, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    tools = project / "tools"
    tools.mkdir(exist_ok=True)
    for name in ("delegate.py", "issues.py"):
        shutil.copy(HERE / "stub_tools" / name, tools / name)
    if not (project / ".git").is_dir():
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    (project / ".git" / "info" / "exclude").write_text(
        "__pycache__/\n*.pyc\n.claude/\n", encoding="utf-8"
    )
    subprocess.run(["git", "add", "-A"], cwd=project, check=True)
    subprocess.run(
        [
            "git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval",
            "commit", "-qm", "fixture", "--allow-empty",
        ],
        cwd=project,
        check=True,
    )


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


def full_tool_calls(lines: list[str]) -> list[dict]:
    calls = []
    ordinal = 0
    for event_index, line in enumerate(lines):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant":
            continue
        for block_index, block in enumerate(event.get("message", {}).get("content", [])):
            if block.get("type") != "tool_use":
                continue
            calls.append({
                "ordinal": ordinal,
                "event_index": event_index,
                "block_index": block_index,
                "name": block.get("name"),
                "input": block.get("input") or {},
            })
            ordinal += 1
    return calls


def owner_reads(reduced: list[dict]) -> list[int]:
    return [
        i for i, event in enumerate(reduced)
        if event.get("tool") in {"Read", "Grep", "Bash", "Glob"}
        and OWNER in event.get("input", "")
    ]


def outside_project(value: str, project: Path) -> bool:
    try:
        path = Path(value)
        target = path if path.is_absolute() else project / path
        target = target.resolve(strict=False)
        root = project.resolve(strict=False)
        return target != root and root not in target.parents
    except (OSError, RuntimeError, TypeError, ValueError):
        return True


def outside_actions(calls: list[dict], project: Path) -> dict:
    network, writes = [], []
    for call in calls:
        name, data, ordinal = call.get("name"), call.get("input") or {}, call.get("ordinal")
        if name in {"Write", "Edit", "NotebookEdit", "MultiEdit"}:
            for key in ("file_path", "path", "notebook_path"):
                target = data.get(key)
                if isinstance(target, str) and outside_project(target, project):
                    writes.append({"tool_index": ordinal, "tool": name, "target": target})
        if name != "Bash":
            continue
        command = data.get("command", "") if isinstance(data, dict) else ""
        if NETWORK_RE.search(command):
            network.append({"tool_index": ordinal, "command": command[:500]})
        for pattern in (ABS_WRITE_RE, PY_ABS_WRITE_RE):
            for match in pattern.finditer(command):
                target = match.group(1)
                if outside_project(target, project):
                    writes.append({"tool_index": ordinal, "tool": "Bash", "target": target, "command": command[:500]})
    return {"network_attempts": network, "out_of_tree_write_attempts": writes}


def run_episode(
    corpus: Path,
    episode: dict,
    arm: str,
    dist: Path,
    out: Path,
    model: str,
    oracles: Path | None,
    identity: dict | None = None,
    pair_order: list[str] | None = None,
) -> dict:
    identity = identity or run_identity(corpus, episode, arm, dist, model, oracles)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "run-identity.json").write_text(
        json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with tempfile.TemporaryDirectory(prefix="ssdp70-") as tmp_name:
        tmp = Path(tmp_name)
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
        env.update({
            "SSDP70_STUB_DIR": str(stub),
            "SSDP70_SIDE_EFFECT_LOG": str(log),
            "SSDP70_ACCOUNT": episode.get("account") or "agent-account",
        })
        cmd = [
            "claude", "-p", prompt,
            "--output-format", "stream-json", "--verbose", "--model", model,
            "--max-turns", str(episode.get("max_turns", 60)),
            "--setting-sources", "project,local",
            "--permission-mode", "acceptEdits",
            "--allowedTools", ALLOWED,
            "--disallowedTools", DISALLOWED,
        ]
        started = time.time()
        proc = subprocess.run(
            cmd,
            cwd=project,
            capture_output=True,
            text=True,
            env=env,
            timeout=3600,
            stdin=subprocess.DEVNULL,
        )
        lines = proc.stdout.splitlines()
        (out / "trace.jsonl").write_text(proc.stdout, encoding="utf-8")
        calls = full_tool_calls(lines)
        (out / "tool-calls.jsonl").write_text(
            "".join(json.dumps(call, sort_keys=True, default=str) + "\n" for call in calls),
            encoding="utf-8",
        )
        reduced = h66.reduce_trace(lines)
        (out / "trace-reduced.json").write_text(
            json.dumps(reduced, indent=1) + "\n", encoding="utf-8"
        )
        if proc.stderr:
            (out / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        summary = h66.parse_trace(lines)
        execution_ok = proc.returncode == 0 and not bool(summary.get("is_error"))
        summary.update({
            "episode": episode["id"],
            "arm": arm,
            "model": model,
            "wall_s": round(time.time() - started, 1),
            "execution_returncode": proc.returncode,
            "execution_ok": execution_ok,
            "pair_order": pair_order or [arm],
            "run_identity_sha256": identity["identity_sha256"],
            "catalog_isolation": catalog_isolation(lines),
            "entry_and_burden": h66.entry_and_burden(reduced, None, dist),
            "new_owner_read_indices": owner_reads(reduced),
            "outside_actions": outside_actions(calls, project),
            "tool_call_count": len(calls),
        })
        summary["admissible"] = bool(summary["catalog_isolation"]["ok"] and execution_ok)
        shutil.copy(log, out / "side-effects.jsonl")
        if (stub / "issues").is_dir():
            shutil.copytree(stub / "issues", out / "issues-final")
        subprocess.run(
            ["git", "add", "-A", "-N", "--", ".", ":(exclude).claude"],
            cwd=project,
            capture_output=True,
        )
        (out / "diff.patch").write_text(
            subprocess.run(
                ["git", "diff", "--", ".", ":(exclude).claude"],
                cwd=project,
                capture_output=True,
                text=True,
            ).stdout,
            encoding="utf-8",
        )
        (out / "final-report.md").write_text(summary.get("final") or "", encoding="utf-8")
        shutil.copytree(
            project,
            out / "final-tree",
            ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"),
        )
        oracle_collection = []
        if oracles is not None and (oracles / episode["id"]).is_dir():
            results = {}
            for check in sorted((oracles / episode["id"]).glob("check_*.py")):
                result = subprocess.run(
                    [sys.executable, str(check), str(out / "final-tree"), str(out)],
                    capture_output=True,
                    text=True,
                )
                oracle_collection.append(check.name)
                results[check.stem] = {
                    "pass": result.returncode == 0,
                    "returncode": result.returncode,
                    "detail": result.stdout.strip()[-2000:],
                    "stderr": result.stderr.strip()[-1000:],
                }
            (out / "oracle.json").write_text(
                json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        summary["oracle_collection"] = oracle_collection
        (out / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8"
        )
    return summary


def matrix_plan(episodes: dict[str, dict], arm_names: list[str], only: list[str]) -> list[dict]:
    plan = []
    for episode_index, (episode_id, episode) in enumerate(episodes.items()):
        if only and episode_id not in only:
            continue
        for rep in range(int(episode.get("replicates", 1))):
            order = list(arm_names) if (episode_index + rep) % 2 == 0 else list(reversed(arm_names))
            plan.append({"episode_id": episode_id, "rep": rep, "order": order})
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("episode", "matrix"):
        command = sub.add_parser(name)
        command.add_argument("--corpus", type=Path, required=True)
        command.add_argument("--arm", action="append", required=True, help="name=path/to/dist/skills")
        command.add_argument("--out", type=Path, required=True)
        command.add_argument("--model", default="claude-sonnet-5")
        command.add_argument("--oracles", type=Path, default=None, help="custodian oracle dir (post-run only)")
        if name == "episode":
            command.add_argument("--id", required=True)
            command.add_argument("--rep", type=int, default=0)
        else:
            command.add_argument("--parallel", type=int, default=4, help="number of episode/replicate pairs in flight")
            command.add_argument("--only", action="append", default=[])
    args = parser.parse_args(argv)
    arms = {key: Path(value) for key, value in (arg.split("=", 1) for arg in args.arm)}
    episodes = {episode["id"]: episode for episode in load_manifest(args.corpus)}

    if args.cmd == "episode":
        (arm, dist), = arms.items()
        episode = episodes[args.id]
        identity = run_identity(args.corpus, episode, arm, dist, args.model, args.oracles)
        summary = run_episode(
            args.corpus,
            episode,
            arm,
            dist,
            args.out / f"{args.id}-{arm}-r{args.rep}",
            args.model,
            args.oracles,
            identity=identity,
            pair_order=[arm],
        )
        print(json.dumps({
            key: summary[key]
            for key in ("episode", "arm", "admissible", "new_owner_read_indices", "wall_s", "run_identity_sha256")
        }))
        return 0

    plan = matrix_plan(episodes, list(arms), args.only)
    args.out.mkdir(parents=True, exist_ok=True)
    plan_record = {
        "schema": 1,
        "model": args.model,
        "parallel_pairs": args.parallel,
        "pairs": plan,
    }
    (args.out / "matrix-plan.json").write_text(
        json.dumps(plan_record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    def run_pair(item: dict) -> list[tuple[str, str]]:
        episode = episodes[item["episode_id"]]
        rep = item["rep"]
        results = []
        # Sequential by construction: the next arm starts only after the prior arm completes.
        for arm in item["order"]:
            target = args.out / f"{episode['id']}-{arm}-r{rep}"
            identity = run_identity(args.corpus, episode, arm, arms[arm], args.model, args.oracles)
            if cache_valid(target, identity):
                results.append((target.name, "cached-exact"))
                continue
            try:
                run_episode(
                    args.corpus,
                    episode,
                    arm,
                    arms[arm],
                    target,
                    args.model,
                    args.oracles,
                    identity=identity,
                    pair_order=item["order"],
                )
                results.append((target.name, "ok"))
            except Exception as exc:  # recorded, never silently dropped
                args.out.mkdir(parents=True, exist_ok=True)
                (args.out / f"{target.name}.error.txt").write_text(repr(exc), encoding="utf-8")
                results.append((target.name, "error"))
        return results

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for pair_results in pool.map(run_pair, plan):
            for name, status in pair_results:
                print(json.dumps({"run": name, "status": status}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
