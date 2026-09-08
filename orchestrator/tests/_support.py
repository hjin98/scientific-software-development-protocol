"""Shared fixtures: real temporary Git repositories and version-bound prompt trees."""

from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
# Existing Core v1 suites intentionally exercise the frozen Protocol 5.16
# package.  Current Protocol 6 suites use CURRENT_CANONICAL_PROMPTS explicitly.
CANONICAL_PROMPTS = (
    REPO_ROOT
    / "orchestrator/src/sdp_orchestrator/core/resources/protocol/sdp-protocol-5.16/prompts.md"
)
CURRENT_CANONICAL_PROMPTS = REPO_ROOT / "source/shared/references/development-workflow-prompts.md"

_GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "sdp-test",
    "GIT_AUTHOR_EMAIL": "sdp-test@example.invalid",
    "GIT_COMMITTER_NAME": "sdp-test",
    "GIT_COMMITTER_EMAIL": "sdp-test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "LC_ALL": "C",
}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        env=_GIT_ENV,
        check=True,
    )
    return result.stdout.strip()


def init_bare(root: Path, *, branch: str = "main") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "--quiet", "--bare", f"--initial-branch={branch}", str(root)],
        check=True,
        capture_output=True,
        env=_GIT_ENV,
    )
    return root


def init_repo(root: Path, *, branch: str = "main") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "--quiet", f"--initial-branch={branch}", str(root)],
        check=True,
        capture_output=True,
        env=_GIT_ENV,
    )
    git(root, "config", "user.name", "sdp-test")
    git(root, "config", "user.email", "sdp-test@example.invalid")
    (root / "README.md").write_text("temporary test repository\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "--quiet", "-m", "initial")
    return root


def write_workplan(
    root: Path,
    relative: str,
    *,
    workplan_id: str | None = "WP-TEST",
    protocol_version: str | None = "5.16.0",
    status: str = "active",
    target_branch: str | None = None,
    body: str = "Test workplan body.\n",
    extra: dict[str, object] | None = None,
) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    if workplan_id is not None:
        lines.append(f"workplan_id: {workplan_id}")
    if protocol_version is not None:
        lines.append(f"protocol_version: {protocol_version}")
    lines.append(f"status: {status}")
    if target_branch:
        lines.append(f"target_branch: {target_branch}")
    for key, value in (extra or {}).items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    path.write_text("\n".join(lines) + "\n" + body, encoding="utf-8")
    return path


def commit_all(root: Path, message: str = "work") -> str:
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD")


def config_text(
    repo: Path,
    *,
    project: str = "demo",
    default_project: str | None = "demo",
    prompt_mode: str | None = None,
    remote_name: str | None = None,
    core_prompt_mode: str | None = None,
    local_root: Path | None = None,
    protocol_profile: str = "sdp-protocol-5.16",
    extra: str = "",
) -> str:
    lines = ["schema_version = 1", "", "[core]"]
    if default_project:
        lines.append(f'default_project = "{default_project}"')
    if core_prompt_mode:
        lines.append(f'default_prompt_mode = "{core_prompt_mode}"')
    lines += ["", f"[projects.{project}]", f'repo = "{repo}"', f'protocol_profile = "{protocol_profile}"']
    if prompt_mode:
        lines.append(f'default_prompt_mode = "{prompt_mode}"')
    if remote_name:
        lines.append(f'remote_name = "{remote_name}"')
    lines += ["", f'[protocol_sources."{protocol_profile}"]']
    if local_root:
        lines.append(f'local_root = "{local_root}"')
    else:
        lines.append("allow_remote = false")
    return "\n".join(lines) + "\n" + textwrap.dedent(extra)


def write_config(path: Path, **kwargs: object) -> Path:
    path.write_text(config_text(**kwargs), encoding="utf-8")  # type: ignore[arg-type]
    return path
