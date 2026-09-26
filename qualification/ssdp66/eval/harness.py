#!/usr/bin/env python3
"""Minimal, removable Protocol 6.6 evaluation harness (non-normative evidence tooling).

Subcommands:
  static      layer-0 catalog metadata footprint and layer-1 declared mandatory-read
              closure for the frozen routes, read from an exact Git ref or the worktree.
  live        layer-0/2/3 runs through a real agent harness (Claude Code headless CLI)
              with one protocol variant installed as project skills; records raw
              stream-json traces plus oracle results.
  assess      blinded independent assessment of a recorded trajectory by a fresh
              agent context that did not execute it.

This harness is evidence coordination only. It owns no protocol semantics, and a
result can never waive a correctness/authority blocker (qualification contract).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SKILLS = (
    ("scientific-formulation", "roles"),
    ("numerical-algorithm-design", "roles"),
    ("software-design", "roles"),
    ("software-implementation", "roles"),
    ("software-documentation", "specialists"),
    ("software-maintenance-audit", "specialists"),
    ("repository-hygiene", "specialists"),
)
# Concern key -> candidate owner files (first existing wins). ``None`` means the
# concern is carried inside an always-read file for that variant.
CONCERN_FILES = {
    "workflow": ["workflow-and-workplans.md"],
    "testing": ["testing-and-validation.md"],
    "convergence": ["convergence-and-cycle-economy.md"],
    "pem": ["project-engineering-memory.md"],
    "pem_schema": ["project-engineering-memory-schema.md", "project-engineering-memory.md"],
    "semantic_definition": ["semantic-definition-and-traceability.md", None],
    "prompts": ["development-workflow-prompts.md"],
    "history": [],
}
TOKEN_RE = re.compile(r"\w+|[^\w\s]")
LINK_RE = re.compile(r"\]\((references|templates)/([A-Za-z0-9_.-]+\.md)\)")
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


class Tree:
    """Read canonical source from an exact Git ref or the working tree."""

    def __init__(self, ref: str | None) -> None:
        self.ref = ref

    def read(self, rel: str) -> str | None:
        if self.ref is None:
            path = REPO / rel
            return path.read_text(encoding="utf-8") if path.is_file() else None
        proc = subprocess.run(["git", "-C", str(REPO), "show", f"{self.ref}:{rel}"], capture_output=True)
        return proc.stdout.decode("utf-8") if proc.returncode == 0 else None


def measure(text: str) -> dict[str, int]:
    return {"bytes": len(text.encode("utf-8")), "tokens_proxy": len(TOKEN_RE.findall(text))}


def skill_path(name: str, kind: str) -> str:
    return f"source/{kind}/{name}/SKILL.md"


def mandatory_refs(skill_text: str) -> list[str]:
    """Links in the entrypoint's unconditional pre-reasoning read sentence."""
    for para in skill_text.split("\n\n"):
        flat = " ".join(para.split())
        if flat.startswith("Before substantive") or flat.startswith("Read "):
            return [m.group(2) for m in LINK_RE.finditer(para) if m.group(1) == "references"]
    return []


def static_report(ref: str | None) -> dict:
    tree = Tree(ref)
    scenarios = yaml.safe_load((HERE / "scenarios.yaml").read_text(encoding="utf-8"))
    catalog = {}
    for name, kind in SKILLS:
        text = tree.read(skill_path(name, kind)) or ""
        front = FRONT_RE.match(text)
        adapter = tree.read(f"source/{kind}/{name}/agents/openai.yaml") or ""
        catalog[name] = {"frontmatter": measure(front.group(1) if front else ""), "openai_adapter": measure(adapter)}
    totals = {
        "frontmatter_bytes": sum(v["frontmatter"]["bytes"] for v in catalog.values()),
        "frontmatter_tokens_proxy": sum(v["frontmatter"]["tokens_proxy"] for v in catalog.values()),
        "adapter_bytes": sum(v["openai_adapter"]["bytes"] for v in catalog.values()),
    }
    kinds = dict(SKILLS)
    routes = {}
    for split in ("development", "holdout"):
        for route in scenarios["routes"][split]:
            root = route["root"]
            skill_text = tree.read(skill_path(root, kinds[root])) or ""
            mandatory = mandatory_refs(skill_text)
            direct = {m.group(2) for m in LINK_RE.finditer(skill_text)}
            hot = ["SKILL.md", *mandatory]
            unreachable = []
            for concern in route["fires"]:
                for candidate in CONCERN_FILES[concern]:
                    if candidate is None:
                        break
                    if tree.read(f"source/shared/references/{candidate}") is None:
                        continue
                    reachable = candidate in direct or any(
                        candidate in (tree.read(f"source/shared/references/{m}") or "") for m in [*mandatory, *direct]
                    )
                    if not reachable:
                        unreachable.append(candidate)
                    if candidate not in hot:
                        hot.append(candidate)
                    break
            eager_forbidden = []
            for concern in route["forbid"]:
                for candidate in CONCERN_FILES[concern]:
                    if candidate and candidate in mandatory:
                        eager_forbidden.append(candidate)
            size = {"bytes": 0, "tokens_proxy": 0}
            for rel in hot:
                text = skill_text if rel == "SKILL.md" else (tree.read(f"source/shared/references/{rel}") or "")
                m = measure(text)
                size["bytes"] += m["bytes"]
                size["tokens_proxy"] += m["tokens_proxy"]
            mand = {"bytes": 0, "tokens_proxy": 0}
            for rel in ["SKILL.md", *mandatory]:
                text = skill_text if rel == "SKILL.md" else (tree.read(f"source/shared/references/{rel}") or "")
                m = measure(text)
                mand["bytes"] += m["bytes"]
                mand["tokens_proxy"] += m["tokens_proxy"]
            routes[route["id"]] = {
                "split": split,
                "mandatory_files": ["SKILL.md", *mandatory],
                "mandatory_closure": mand,
                "route_files": hot,
                "route_closure": size,
                "unreachable_fired_concerns": unreachable,
                "eager_forbidden_concerns": eager_forbidden,
            }
    return {"ref": ref or "WORKTREE", "catalog": catalog, "catalog_totals": totals, "routes": routes}


# ---------------------------------------------------------------- live harness

def _clean_env() -> dict[str, str]:
    env = dict(os.environ)
    # Isolate evaluation runs from the invoking agent session (no shared session id,
    # remote ingress, or additional instruction directories).
    for key in list(env):
        if "SESSION" in key or key in {"CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_PID"}:
            env.pop(key)
    return env


def install_variant(dist: Path, project: Path) -> None:
    target = project / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    for name, _ in SKILLS:
        shutil.copytree(dist / name, target / name)


def reduce_trace(lines: list[str]) -> list[dict]:
    """Committed provenance: ordered tool calls, assistant text and the result usage."""
    reduced = []
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            reduced.append({"init": {"model": event.get("model"), "claude_code_version": event.get("claude_code_version"), "skills": event.get("skills")}})
        elif event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    reduced.append({"tool": block.get("name"), "input": json.dumps(block.get("input"))[:400]})
                elif block.get("type") == "text":
                    reduced.append({"text": block.get("text", "")[:4000]})
        elif event.get("type") == "result":
            reduced.append({"result": {k: event.get(k) for k in ("subtype", "num_turns", "total_cost_usd", "duration_ms", "usage", "is_error")}})
    return reduced


def parse_trace(lines: list[str]) -> dict:
    skills, reads, result = [], [], {}
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") != "tool_use":
                    continue
                if block.get("name") == "Skill":
                    skills.append(block.get("input", {}).get("skill") or block.get("input", {}).get("command"))
                elif block.get("name") == "Read":
                    reads.append(block.get("input", {}).get("file_path", ""))
        elif event.get("type") == "result":
            result = event
    protocol_reads = [r for r in reads if "/.claude/skills/" in r]
    protocol_bytes = 0
    for r in protocol_reads:
        try:
            protocol_bytes += Path(r).stat().st_size
        except OSError:
            pass
    usage = result.get("usage", {})
    return {
        "skills_invoked": skills,
        "protocol_reads": [r.split("/.claude/skills/", 1)[1] for r in protocol_reads],
        "protocol_read_bytes_on_disk": protocol_bytes,
        "num_turns": result.get("num_turns"),
        "total_cost_usd": result.get("total_cost_usd"),
        "duration_ms": result.get("duration_ms"),
        "input_tokens_total": sum(usage.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")),
        "output_tokens": usage.get("output_tokens"),
        "is_error": result.get("is_error"),
        "final": result.get("result", ""),
        "models": sorted(result.get("modelUsage", {}).keys()),
    }


def run_live(dist: Path, prompt: str, fixture: Path | None, out: Path, model: str, max_turns: int, mode: str) -> dict:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="ssdp66-") as tmp:
        project = Path(tmp) / "project"
        if fixture is not None:
            shutil.copytree(fixture, project, ignore=shutil.ignore_patterns("__pycache__"))
            (project / "TASK.md").unlink(missing_ok=True)
        else:
            project.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
        (project / ".git" / "info" / "exclude").write_text("__pycache__/\n*.pyc\n.claude/\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=project, check=True)
        subprocess.run(["git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval", "commit", "-qm", "fixture", "--allow-empty"], cwd=project, check=True)
        install_variant(dist, project)
        cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model, "--max-turns", str(max_turns)]
        if mode == "select":
            cmd += ["--allowedTools", "Skill Read Glob Grep", "--disallowedTools", "Edit Write Bash NotebookEdit Agent WebFetch WebSearch"]
        else:
            cmd += [
                "--permission-mode", "acceptEdits",
                "--allowedTools", "Skill Read Glob Grep Edit Write TodoWrite Bash(python:*) Bash(python3:*) Bash(git:*) Bash(ls:*) Bash(cat:*) Bash(grep:*) Bash(find:*) Bash(head:*) Bash(sed -n:*) WebFetch",
                "--disallowedTools", "Agent WebSearch",
            ]
        started = time.time()
        proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True, env=_clean_env(), timeout=1800, stdin=subprocess.DEVNULL)
        (out / "trace.jsonl").write_text(proc.stdout, encoding="utf-8")
        (out / "trace-reduced.json").write_text(json.dumps(reduce_trace(proc.stdout.splitlines()), indent=1) + "\n", encoding="utf-8")
        if proc.stderr:
            (out / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        summary = parse_trace(proc.stdout.splitlines())
        summary["wall_s"] = round(time.time() - started, 1)
        if fixture is not None:
            diff = subprocess.run(["git", "diff", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True, text=True).stdout
            untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True, text=True).stdout
            (out / "diff.patch").write_text(diff, encoding="utf-8")
            summary["untracked"] = [p for p in untracked.splitlines() if not p.startswith(".claude/")]
            summary["oracle"] = run_oracle(fixture.name, project)
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if fixture is not None:
            shutil.copytree(project, out / "final-tree", ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))
    return summary


def run_oracle(fixture_id: str, project: Path) -> dict:
    oracle_dir = HERE / "oracles" / fixture_id
    results = {}
    for hidden in sorted(oracle_dir.glob("test_*.py")):
        shutil.copy(hidden, project / "tests" / f"zz_{hidden.name}")
        proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=project, capture_output=True, text=True)
        results["tests_pass"] = proc.returncode == 0
        results["tests_tail"] = proc.stderr.strip().splitlines()[-1:] if proc.stderr else []
        (project / "tests" / f"zz_{hidden.name}").unlink()
    for check in sorted(oracle_dir.glob("check_*.py")):
        proc = subprocess.run([sys.executable, str(check), str(project)], capture_output=True, text=True)
        results[check.stem] = {"pass": proc.returncode == 0, "detail": proc.stdout.strip()}
    return results


ASSESS_PROMPT = """You are an independent evaluator. You did not perform the task below and must not assume the executor's claims are true.
Grade ONLY against the rubric using the evidence provided (task, repository documents, final diff, executor final message, deterministic oracle output).
Return strict JSON: {{"verdict": "PASS"|"FAIL", "rubric_items": {{...}}, "notes": "<=80 words"}}.

RUBRIC: {rubric}

TASK:
{task}

REPOSITORY DOCUMENTS (pre-task):
{docs}

FINAL DIFF:
{diff}

UNTRACKED NEW FILES: {untracked}

EXECUTOR FINAL MESSAGE (variant identifiers redacted):
{final}

DETERMINISTIC ORACLE OUTPUT:
{oracle}
"""


def assess(run_dir: Path, fixture: Path, rubric: str, model: str) -> dict:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    docs = []
    for path in sorted(fixture.rglob("*.md")):
        if path.name != "TASK.md":
            docs.append(f"--- {path.relative_to(fixture)}\n{path.read_text(encoding='utf-8')}")
    # Blind the evaluator to the protocol variant: redact only the two compared package
    # versions, keeping other versions (e.g. a workplan's own binding) visible.
    redact = lambda s: re.sub(r"\b6\.[56](?:\.0)?\b", "<installed-version>", s)  # noqa: E731
    final = redact(summary.get("final", ""))
    # Keep the governing workplan's own declared version visible; only executor text is redacted.
    prompt = ASSESS_PROMPT.format(
        rubric=rubric, task=(fixture / "TASK.md").read_text(encoding="utf-8"), docs="\n".join(docs) or "NONE",
        diff=redact((run_dir / "diff.patch").read_text(encoding="utf-8"))[:20000], untracked=summary.get("untracked"),
        final=final[:6000], oracle=json.dumps(summary.get("oracle")),
    )
    with tempfile.TemporaryDirectory(prefix="ssdp66-assess-") as tmp:
        proc = subprocess.run(["claude", "-p", prompt, "--output-format", "json", "--model", model, "--max-turns", "1", "--disallowedTools", "Bash Edit Write Read Glob Grep Skill Agent"], cwd=tmp, capture_output=True, text=True, env=_clean_env(), timeout=600, stdin=subprocess.DEVNULL)
    try:
        text = json.loads(proc.stdout).get("result", "")
        verdict = json.loads(text[text.index("{"): text.rindex("}") + 1])
    except (ValueError, json.JSONDecodeError):
        verdict = {"verdict": "UNPARSEABLE", "raw": proc.stdout[-2000:]}
    (run_dir / "assessment.json").write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("static")
    st.add_argument("--ref", default=None, help="exact Git ref; omit for the working tree")
    lv = sub.add_parser("live")
    lv.add_argument("--dist", type=Path, required=True, help="generated skills root (dist/skills) of one variant")
    lv.add_argument("--prompt", required=True)
    lv.add_argument("--fixture", type=Path)
    lv.add_argument("--out", type=Path, required=True)
    lv.add_argument("--model", default="claude-sonnet-5")
    lv.add_argument("--max-turns", type=int, default=4)
    lv.add_argument("--mode", choices=("select", "trajectory"), default="select")
    asx = sub.add_parser("assess")
    asx.add_argument("--run", type=Path, required=True)
    asx.add_argument("--fixture", type=Path, required=True)
    asx.add_argument("--rubric", required=True)
    asx.add_argument("--model", default="claude-sonnet-5")
    args = parser.parse_args(argv)
    if args.cmd == "static":
        print(json.dumps(static_report(args.ref), indent=2, sort_keys=True))
    elif args.cmd == "live":
        print(json.dumps(run_live(args.dist, args.prompt, args.fixture, args.out, args.model, args.max_turns, args.mode), indent=2, sort_keys=True))
    else:
        print(json.dumps(assess(args.run, args.fixture, args.rubric, args.model), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
