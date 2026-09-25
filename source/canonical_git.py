#!/usr/bin/env python3
"""Canonical local-Git topology helpers for self-governance validators."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

OBJECT_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")


class CanonicalGitError(RuntimeError):
    """Canonical Git topology could not be established from raw commit objects."""

    def __init__(
        self,
        kind: str,
        subject: str,
        *,
        commit: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.kind = kind
        self.subject = subject
        self.commit = commit
        self.detail = detail
        super().__init__(self._message())

    def _message(self) -> str:
        if self.kind == "resolve":
            return f"cannot resolve canonical commit at {self.subject}"
        if self.kind == "read":
            return f"cannot read canonical commit object {self.commit or self.subject}"
        if self.kind == "parent":
            return (
                f"canonical commit {self.commit or self.subject} has invalid parent "
                f"{self.detail!r}"
            )
        return f"cannot establish canonical Git topology at {self.subject}"


def run_canonical_git(
    root: Path,
    *args: str,
    timeout: int = 10,
) -> tuple[int, str]:
    """Run one text Git command with replacement objects disabled."""
    result = subprocess.run(
        ["git", "-C", str(root), "--no-replace-objects", *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout.strip()


def commit_and_parents(root: Path, ref: str) -> tuple[str, list[str]]:
    """Resolve one commit and parse only its raw canonical parent headers."""
    code, commit = run_canonical_git(
        root,
        "rev-parse",
        "--verify",
        f"{ref}^{{commit}}",
    )
    if code or not OBJECT_RE.fullmatch(commit):
        raise CanonicalGitError("resolve", ref)

    code, raw = run_canonical_git(root, "cat-file", "-p", commit)
    if code or not raw:
        raise CanonicalGitError("read", ref, commit=commit)

    header = raw.split("\n\n", 1)[0]
    parents: list[str] = []
    for line in header.splitlines():
        if not line.startswith("parent "):
            continue
        parent = line.removeprefix("parent ").strip()
        if not OBJECT_RE.fullmatch(parent):
            raise CanonicalGitError(
                "parent",
                ref,
                commit=commit,
                detail=parent,
            )
        parents.append(parent)
    return commit, parents


def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    """Resolve ancestry from raw canonical commit parents, not revision overlays."""
    target, _ = commit_and_parents(root, ancestor)
    descendant_commit, descendant_parents = commit_and_parents(root, descendant)
    if descendant_commit == target:
        return True

    visited = {descendant_commit}
    stack = list(descendant_parents)
    while stack:
        commit, parents = commit_and_parents(root, stack.pop())
        if commit in visited:
            continue
        if commit == target:
            return True
        visited.add(commit)
        stack.extend(parents)
    return False
