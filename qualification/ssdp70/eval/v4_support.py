"""Shared helpers for the Stage F v4 repair regression tests (test support, not runtime code).

The regression tests use the REAL Claude Code 2.1.284 traces retained under
`stage-f-runner-admission-v4-inputs-2026-09-29/`. The only transformation is retargeting the recorded
ephemeral run root to the test's temporary project so that the adapter can read the installed
`SKILL.md`; installed skill bytes come from the immutable Protocol 7 candidate commit, never from the
trace being tested.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
INPUTS = HERE.parent / "stage-f-runner-admission-v4-inputs-2026-09-29"
CANDIDATE_COMMIT = "db94a2dfb7fef480f37227eab5c45256e89901b8"
PACKAGE_SHA256 = "7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b"

RUNS = (
    "CHK-PING-p70-r0",
    "CHK-TURN-p70-r0",
    "N02-cat-custody-file-Bash-p70-r0",
    "N05-list-host-home-p70-r0",
    "N06-write-tmp-python-p70-r0",
    "N07-write-tmp-Write-tool-p70-r0",
    "N08-write-outside-project-relative-p70-r0",
    "N18-mcp-issue-create-p70-r0",
    "N19-mcp-delegate-p70-r0",
    "N20-ordinary-control-ls-p70-r0",
    "N21-grep-no-path-p70-r0",
    "N22-glob-no-path-p70-r0",
)


def installed_skill_bytes(skill: str, commit: str = CANDIDATE_COMMIT) -> bytes:
    """The installed SKILL.md of the immutable candidate package (generated dist)."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{commit}:dist/skills/{skill}/SKILL.md"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:  # never skip: a required check that cannot run is a failure
        raise AssertionError(
            f"candidate {commit} SKILL.md for {skill!r} is unavailable ({exc.stderr.decode(errors='replace').strip()}); "
            "the regression evidence requires the immutable candidate commit in this repository"
        ) from exc


def trace_text(run: str) -> str:
    return (INPUTS / run / "trace.jsonl").read_text(encoding="utf-8")


def recorded_project(run: str) -> str:
    """The ephemeral run project the real runtime recorded as its working directory."""
    for line in trace_text(run).splitlines():
        row = json.loads(line)
        if row.get("type") == "system" and row.get("subtype") == "init":
            return row["cwd"]
    raise AssertionError(f"{run}: no init event")


def retarget(run: str, project: Path) -> str:
    """Replace the recorded ephemeral project path with the test project path (nothing else)."""
    return trace_text(run).replace(recorded_project(run), str(project))


def package_context(project: Path) -> dict:
    return {
        "project": str(project),
        "skills_root": str(project / ".claude" / "skills"),
        "package_identity": {
            "arm": "p70",
            "commit": CANDIDATE_COMMIT,
            "version": "7.0.0",
            "package_sha256": PACKAGE_SHA256,
        },
    }


def install_real_skill(project: Path, skill: str = "software-implementation", data: bytes | None = None) -> Path:
    path = project / ".claude" / "skills" / skill / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(installed_skill_bytes(skill) if data is None else data)
    return path


def raw_rows(run: str) -> list[dict]:
    return [json.loads(line) for line in trace_text(run).splitlines() if line.strip()]
