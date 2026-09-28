#!/usr/bin/env python3
"""Independent evaluation of one Protocol 7 run (non-normative evidence tooling).

A fresh evaluator context receives the custodian's frozen key material and a complete,
file-backed evidence bundle for the recorded run. Evidence is never truncated into the
prompt. The evaluator works from files with read-only tools so the pre-run checker can
verify that the full report, diff/new files, raw tool trace, side effects, issue store,
oracle output and run metadata were available.

The implementing author never runs this against real custody keys before candidate
freeze. The independent evaluator or pre-run checker runs it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "ssdp66" / "eval"))
import harness as h66  # noqa: E402

RESULTS = {"pass", "fail", "unresolved", "not-applicable"}
EVIDENCE_NAMES = (
    "summary.json",
    "run-identity.json",
    "final-report.md",
    "diff.patch",
    "side-effects.jsonl",
    "tool-calls.jsonl",
    "trace.jsonl",
    "trace-reduced.json",
    "oracle.json",
    "stderr.txt",
    "issues-final",
    "final-tree",
)
PROMPT = """You are an independent evaluator. You did not perform this run and must not trust the executor's claims.

The complete evidence bundle is the current working directory. Read EVIDENCE-MANIFEST.json first. Score the run ONLY
against frozen key material under keys/ (and shared-rubric.txt when present). The run evidence is under run/. Do not
infer a missing fact from a truncated excerpt: the evidence files are available in full. Inspect the final report, changed
and new files, tool trace, side effects, issue state, deterministic oracle output and run metadata as the frozen key requires.
The raw trace may reveal the protocol arm; record any consequential unblinding instead of claiming blindness.

Apply the key's rules without discretion. Where a predeclared rule does not settle a disposition, mark it "unresolved"
with a rationale. A generic hedge or a skipped cheap view named as unexamined is never a correct limitation. Do not alter
any evidence file and do not use network, shell, skills or agents.

Return strict JSON only, exactly this shape:
{"episode":"...","dispositions":[{"item":"...","measure":"...","result":"pass|fail|unresolved|not-applicable","critical":true,"evidence":"<=40 words"}],"r2_point_index":null,"owner_false_activation":null,"notes":"<=80 words"}
"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def evidence_manifest(root: Path) -> list[dict]:
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "EVIDENCE-MANIFEST.json"):
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    return rows


def prepare_bundle(run: Path, keys: Path, shared_rubric: Path | None, root: Path) -> list[dict]:
    key_dst = root / "keys"
    shutil.copytree(keys, key_dst)
    if shared_rubric is not None:
        shutil.copy2(shared_rubric, root / "shared-rubric.txt")
    run_dst = root / "run"
    run_dst.mkdir()
    for name in EVIDENCE_NAMES:
        src = run / name
        if src.exists():
            copy_item(src, run_dst / name)
    manifest = evidence_manifest(root)
    (root / "EVIDENCE-MANIFEST.json").write_text(
        json.dumps({"schema": 1, "files": manifest}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def result_text(stdout: str) -> tuple[str | None, dict | None]:
    final_event = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            final_event = event
    if final_event is None:
        return None, None
    return final_event.get("result", ""), final_event


def word_count(text: str) -> int:
    return len(text.split())


def validate_verdict(verdict: object, expected_episode: str) -> list[str]:
    errors = []
    if not isinstance(verdict, dict):
        return ["top-level result is not an object"]
    required = {"episode", "dispositions", "r2_point_index", "owner_false_activation", "notes"}
    if set(verdict) != required:
        errors.append(f"top-level keys must be exactly {sorted(required)}")
    if verdict.get("episode") != expected_episode:
        errors.append("episode does not match run summary")
    dispositions = verdict.get("dispositions")
    if not isinstance(dispositions, list):
        errors.append("dispositions is not a list")
    else:
        item_keys = {"item", "measure", "result", "critical", "evidence"}
        for index, item in enumerate(dispositions):
            if not isinstance(item, dict):
                errors.append(f"dispositions[{index}] is not an object")
                continue
            if set(item) != item_keys:
                errors.append(f"dispositions[{index}] keys are invalid")
            if item.get("result") not in RESULTS:
                errors.append(f"dispositions[{index}].result is invalid")
            if not isinstance(item.get("critical"), bool):
                errors.append(f"dispositions[{index}].critical is not boolean")
            if not isinstance(item.get("item"), str) or not item.get("item"):
                errors.append(f"dispositions[{index}].item is empty")
            if not isinstance(item.get("measure"), str) or not item.get("measure"):
                errors.append(f"dispositions[{index}].measure is empty")
            evidence = item.get("evidence")
            if not isinstance(evidence, str) or word_count(evidence) > 40:
                errors.append(f"dispositions[{index}].evidence exceeds 40 words or is not text")
    r2 = verdict.get("r2_point_index")
    if r2 is not None and (not isinstance(r2, int) or isinstance(r2, bool) or r2 < 0):
        errors.append("r2_point_index must be a non-negative integer or null")
    owner_false = verdict.get("owner_false_activation")
    if owner_false is not None and not isinstance(owner_false, bool):
        errors.append("owner_false_activation must be boolean or null")
    notes = verdict.get("notes")
    if not isinstance(notes, str) or word_count(notes) > 80:
        errors.append("notes exceeds 80 words or is not text")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True, help="custodian keys/<episode> directory")
    parser.add_argument("--shared-rubric", type=Path, default=None)
    parser.add_argument("--model", default="claude-sonnet-5")
    parser.add_argument("--max-turns", type=int, default=40)
    args = parser.parse_args()

    summary = json.loads((args.run / "summary.json").read_text(encoding="utf-8"))
    expected_episode = summary["episode"]
    with tempfile.TemporaryDirectory(prefix="ssdp70-assess-") as tmp:
        root = Path(tmp)
        manifest = prepare_bundle(args.run, args.keys, args.shared_rubric, root)
        proc = subprocess.run(
            [
                "claude", "-p", PROMPT,
                "--output-format", "stream-json", "--verbose",
                "--model", args.model, "--max-turns", str(args.max_turns),
                "--allowedTools", "Read Glob Grep",
                "--disallowedTools", "Bash Edit Write NotebookEdit MultiEdit Skill Agent WebFetch WebSearch",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            env=h66._clean_env(),
            timeout=1800,
            stdin=subprocess.DEVNULL,
        )
        (args.run / "assessment-trace.jsonl").write_text(proc.stdout, encoding="utf-8")
        (args.run / "assessment-evidence-manifest.json").write_text(
            json.dumps({"schema": 1, "files": manifest}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if proc.stderr:
            (args.run / "assessment-stderr.txt").write_text(proc.stderr, encoding="utf-8")
        text, final_event = result_text(proc.stdout)

    status = "VALID"
    errors: list[str] = []
    verdict: object = None
    if proc.returncode != 0 or final_event is None or final_event.get("is_error"):
        status = "EXECUTION_ERROR"
        errors.append(f"evaluator process failed or returned an error (returncode={proc.returncode})")
    if text is None:
        status = "UNPARSEABLE" if status == "VALID" else status
        errors.append("no result text")
    else:
        try:
            start, end = text.index("{"), text.rindex("}") + 1
            verdict = json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError) as exc:
            status = "UNPARSEABLE" if status == "VALID" else status
            errors.append(f"invalid JSON result: {exc}")
    if isinstance(verdict, dict):
        schema_errors = validate_verdict(verdict, expected_episode)
        if schema_errors:
            if status == "VALID":
                status = "INVALID_SCHEMA"
            errors.extend(schema_errors)

    if status == "VALID":
        output = verdict
        exit_code = 0
    else:
        output = {
            "assessment_status": status,
            "errors": errors,
            "raw_result": text[-4000:] if isinstance(text, str) else "",
        }
        exit_code = 2
    (args.run / "assessment.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
