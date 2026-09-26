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


def consumed_skill(tree: "Tree", name: str, kind: str) -> str:
    """The entrypoint as a runtime consumes it: a build-inlined entry contract is expanded."""
    text = tree.read(skill_path(name, kind)) or ""
    placeholder = "<!-- SSDP-ENTRY-CONTRACT -->"
    if placeholder in text:
        sys.path.insert(0, str(REPO / "source"))
        import build_skills  # current build owner; only refs carrying the placeholder reach here

        text = text.replace(placeholder, build_skills.entry_contract(
            tree.read("source/shared/references/abstraction-and-concretization.md") or "",
            tree.read("source/shared/references/protocol-versioning-and-compatibility.md") or "",
        ))
    return text


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
            skill_text = consumed_skill(tree, root, kinds[root])
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


MUTATING_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
LOOKUP_RE = re.compile(r"git (?:fetch|clone|ls-remote|pull)|curl |wget |pip (?:download|install)")
SSDP_SKILLS = {name for name, _ in SKILLS}
# Implementation Review R2 (workplan section 16.9, B3) ordering-oracle correction; frozen
# before any authenticated post-R1 run. Conservative by construction:
#   knowable   - first Read/Grep/Bash that can expose the governing workplan (input names a
#                workplan, or a repository-wide Grep/recursive shell search); 0 if never seen.
#   protocol   - after knowable: any read/search/shell touching installed SSDP material or a
#                further SSDP Skill invocation. Exempt: the single entry Skill invocation that
#                loads the entry contract, and calls whose every installed-SSDP path is a
#                version-identity file (PROTOCOL_VERSION, protocol-manifest.json, the
#                versioning owner, the version helper): workplan 16.11.1 item 7 makes those
#                reads part of the version decision itself. Frozen for the final
#                simplification before any run of it; a call that also touches any other
#                SSDP file is still protocol action.
#   mutation   - Edit/Write/NotebookEdit/MultiEdit or a mutating shell command, anywhere.
BASH_MUTATION_RE = re.compile(
    r"\bsed\s+-i|\btee\b|(?<![0-9&])>>?\s*(?!&|/dev/null)[\w./~\"'$-]|\b(?:mv|rm|cp|touch|mkdir)\s"
    r"|git\s+(?:add|commit|apply|am|checkout|reset|restore|mv|rm|stash|merge|rebase)\b"
    r"|\.write_text\(|\.write\(|open\([^)]*[\"'][wa]")
KNOWABLE_SEARCH_RE = re.compile(r"grep\s+-\w*[rR]|\brg\s|git\s+grep")
SSDP_PATH_RE = re.compile(r"\.claude/skills/[^\s\"'\\;|&)]*")
VERSION_IDENTITY_RE = re.compile(r"(?:PROTOCOL_VERSION|protocol-manifest\.json|protocol-versioning-and-compatibility(?:\.md)?|version_preflight(?:\.py)?)$")


def version_decision_only(raw: str) -> bool:
    paths = SSDP_PATH_RE.findall(raw)
    return bool(paths) and all(VERSION_IDENTITY_RE.search(path) for path in paths)


def _shell(raw: str) -> str:
    try:
        return json.loads(raw).get("command", "") if raw.startswith("{") else raw
    except json.JSONDecodeError:
        return raw


def ordering_events(reduced: list[dict]) -> dict:
    """Indices (into ``reduced``) for the B3 ordering oracle; see the block comment above."""
    knowable = first_protocol = first_mutation = None
    protocol_detail = mutation_detail = None
    entry_skill_seen = False
    for i, e in enumerate(reduced):
        tool, raw = e.get("tool"), e.get("input", "")
        if tool is None:
            continue
        command = _shell(raw) if tool == "Bash" else ""
        if knowable is None and tool in {"Read", "Grep", "Bash"} and (
            "workplan" in raw.lower()
            or (tool == "Grep" and '"path"' not in raw)
            or (tool == "Bash" and KNOWABLE_SEARCH_RE.search(command))
        ):
            knowable = i
        if first_mutation is None and (tool in MUTATING_TOOLS or (tool == "Bash" and BASH_MUTATION_RE.search(command))):
            first_mutation, mutation_detail = i, raw[:160]
        protocol = False
        if tool == "Skill":
            try:
                name = json.loads(raw).get("skill") if raw.startswith("{") else None
            except json.JSONDecodeError:
                name = None
            if name in SSDP_SKILLS:
                protocol = entry_skill_seen
                entry_skill_seen = True
        elif ".claude/skills/" in raw and not version_decision_only(raw):
            protocol = True
        if protocol and knowable is not None and i > knowable and first_protocol is None:
            first_protocol, protocol_detail = i, raw[:160]
    return {"knowable": knowable, "first_protocol": first_protocol, "protocol_detail": protocol_detail,
            "first_mutation": first_mutation, "mutation_detail": mutation_detail}


def entry_and_burden(reduced: list[dict], governing: str | None, dist: Path | None) -> dict:
    """Rework R0 deterministic trace checks (frozen before the R1 repair; the ordering
    oracle was strengthened by Review R2 / section 16.9 before any valid post-R1 run).

    entry: for a version-bound task, does an assistant text naming the governing version
    precede (a) the first file mutation and (b) the first substantive SSDP/protocol-dependent
    action after the governing version becomes knowable (``ordering_events``)? For any task,
    did the run perform a remote/source lookup or open the versioning owner?
    burden: observed active SSDP material = bytes of every invoked SSDP entrypoint as
    installed + bytes of SSDP files actually read, plus the count of protocol-file reads.
    """
    order = ordering_events(reduced)
    first_mutation = order["first_mutation"]
    stated_at = None
    if governing:
        pattern = re.compile(r"(?<![\d.])" + re.escape(governing.rsplit(".0", 1)[0] if governing.endswith(".0") else governing) + r"(?:\.0)?(?!\d|\.\d)")
        stated_at = next((i for i, e in enumerate(reduced) if "text" in e and pattern.search(e["text"])), None)
    gate = min((i for i in (first_mutation, order["first_protocol"]) if i is not None), default=None)
    lookups, versioning_reads, protocol_reads, protocol_bytes, skills = [], 0, 0, 0, []
    for e in reduced:
        tool, raw = e.get("tool"), e.get("input", "")
        if tool in {"WebFetch", "WebSearch"} or (tool == "Bash" and LOOKUP_RE.search(raw)):
            lookups.append(raw[:120])
        if tool == "Skill":
            name = json.loads(raw).get("skill") if raw.startswith("{") else None
            if name in SSDP_SKILLS:
                skills.append(name)
        if tool in {"Read", "Grep", "Glob", "Bash"} and ".claude/skills/" in raw:
            protocol_reads += 1
            if "protocol-versioning-and-compatibility" in raw:
                versioning_reads += 1
            if tool == "Read":
                try:
                    rel = json.loads(raw)["file_path"].split(".claude/skills/", 1)[1]
                    protocol_bytes += (dist / rel).stat().st_size if dist else 0
                except (ValueError, KeyError, IndexError, OSError):
                    pass
    entry_bytes = sum((dist / name / "SKILL.md").stat().st_size for name in skills) if dist else 0
    return {
        "governing_version": governing,
        "first_mutation_index": first_mutation,
        "first_mutation_detail": order["mutation_detail"],
        "governing_knowable_index": order["knowable"],
        "first_protocol_action_index": order["first_protocol"],
        "first_protocol_action_detail": order["protocol_detail"],
        "governing_stated_index": stated_at,
        # Frozen R0 field, retained for audit continuity; superseded as the R1 gate by the
        # stronger field below.
        "governing_stated_before_mutation": None if not governing else (
            stated_at is not None and (first_mutation is None or stated_at < first_mutation)),
        "governing_stated_before_protocol_action_or_mutation": None if not governing else (
            stated_at is not None and (gate is None or stated_at < gate)),
        "remote_or_source_lookups": lookups,
        "versioning_owner_reads": versioning_reads,
        "ssdp_entrypoint_bytes": entry_bytes,
        "ssdp_reference_read_bytes": protocol_bytes,
        "observed_active_ssdp_bytes": entry_bytes + protocol_bytes,
        "protocol_file_reads": protocol_reads,
    }


def run_live(dist: Path, prompt: str, fixture: Path | None, out: Path, model: str, max_turns: int, mode: str, governing: str | None = None) -> dict:
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
        # Load only project/local settings so user-level installed skills (for example an
        # accepted SSDP package under ~/.claude/skills) cannot shadow the variant under test.
        cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model,
               "--max-turns", str(max_turns), "--setting-sources", "project,local"]
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
        reduced = reduce_trace(proc.stdout.splitlines())
        (out / "trace-reduced.json").write_text(json.dumps(reduced, indent=1) + "\n", encoding="utf-8")
        if proc.stderr:
            (out / "stderr.txt").write_text(proc.stderr, encoding="utf-8")
        summary = parse_trace(proc.stdout.splitlines())
        summary["wall_s"] = round(time.time() - started, 1)
        summary["entry_and_burden"] = entry_and_burden(reduced, governing, dist)
        if fixture is not None:
            untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True, text=True).stdout
            # Intent-to-add new files so the assessor sees their content, not only their names.
            subprocess.run(["git", "add", "-A", "-N", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True)
            diff = subprocess.run(["git", "diff", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True, text=True).stdout
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
        # The copy must match unittest's default ``test*.py`` discovery pattern. Before the D3
        # reopen it was named ``zz_test_*.py`` and was never collected, so earlier
        # ``tests_pass`` values reflect only the fixture's visible tests (see
        # D3-REOPEN-QUALIFICATION-FREEZE.md).
        target = project / "tests" / f"test_zz_oracle_{hidden.name}"
        shutil.copy(hidden, target)
        proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=project, capture_output=True, text=True)
        results["tests_pass"] = proc.returncode == 0
        results["tests_tail"] = proc.stderr.strip().splitlines()[-1:] if proc.stderr else []
        results["hidden_collected"] = target.stem in proc.stderr
        target.unlink()
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
        final=final[:6000], oracle=json.dumps({**(summary.get("oracle") or {}), **{
            k: v for k, v in (summary.get("entry_and_burden") or {}).items()
            if k in {"governing_version", "governing_stated_before_protocol_action_or_mutation", "remote_or_source_lookups"}}}),
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
    lv.add_argument("--governing-version", default=None, help="version declared by the task/workplan (rework R0 entry check)")
    asx = sub.add_parser("assess")
    asx.add_argument("--run", type=Path, required=True)
    asx.add_argument("--fixture", type=Path, required=True)
    asx.add_argument("--rubric", required=True)
    asx.add_argument("--model", default="claude-sonnet-5")
    args = parser.parse_args(argv)
    if args.cmd == "static":
        print(json.dumps(static_report(args.ref), indent=2, sort_keys=True))
    elif args.cmd == "live":
        print(json.dumps(run_live(args.dist, args.prompt, args.fixture, args.out, args.model, args.max_turns, args.mode, args.governing_version), indent=2, sort_keys=True))
    else:
        print(json.dumps(assess(args.run, args.fixture, args.rubric, args.model), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
