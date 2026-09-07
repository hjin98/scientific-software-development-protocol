"""Read-only Git worktree/remote observation.

Every command here is chosen to leave the target untouched: no fetch, no pull, no
checkout, no ref write. ``--no-optional-locks`` plus ``GIT_OPTIONAL_LOCKS=0``
additionally stops ``git status`` from opportunistically rewriting the index,
which would otherwise violate the non-mutating invariant for an inspection.

Remote knowledge is graded rather than assumed:

* ``local_only``      -- repository configuration only; nothing about the remote side.
* ``use_cached_remote`` -- existing local remote-tracking refs, read but never updated.
* ``refresh_remote``  -- one bounded, noninteractive ``git ls-remote`` query.

The distinction is load-bearing: web prompt rendering must be able to say *how*
it knows a target exists, and "unknown" must stay distinguishable from "absent".
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import _errors as E
from ._digest import SCHEME_GIT_WORKING_TREE, digest_canonical
from ._limits import (
    GIT_REMOTE_TIMEOUT_SECONDS,
    GIT_TIMEOUT_SECONDS,
    MAX_DIRTY_FILE_BYTES,
    MAX_DIRTY_PATHS,
    MAX_GIT_OUTPUT_BYTES,
)
from ._records import (
    CandidateRef,
    DigestRef,
    RemoteEvidence,
    RemoteMode,
    RemoteRepositoryRef,
    WorktreeKey,
)
from ._redact import redact_text, sanitize_url

_SCP_LIKE = re.compile(r"^(?:[^@/\s]+@)?(?P<host>[^:/\s]+):(?!//)(?P<path>.+)$")
_WEB_SCHEMES = frozenset({"https", "http", "ssh", "git"})


def _git_env() -> dict[str, str]:
    """A noninteractive, non-mutating, credential-quiet environment."""

    env = dict(os.environ)
    env.update(
        {
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ASKPASS": "",
            "SSH_ASKPASS": "",
            "GIT_PAGER": "cat",
            "GIT_CONFIG_PARAMETERS": "",
            "LC_ALL": "C",
        }
    )
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: bytes
    stderr: str


def run_git(
    root: Path, args: list[str], *, timeout: float = GIT_TIMEOUT_SECONDS
) -> GitResult:
    """Run one bounded read-only Git command rooted at ``root``."""

    command = ["git", "--no-optional-locks", "-C", str(root), *args]
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
            command,
            capture_output=True,
            timeout=timeout,
            env=_git_env(),
            check=False,
        )
    except FileNotFoundError:
        E.fail(
            E.REPOSITORY_INVALID,
            "the 'git' executable is not available",
            remediation="install Git or make it available on PATH",
        )
    except subprocess.TimeoutExpired:
        E.fail(
            E.REPOSITORY_INVALID,
            "a Git command exceeded its time bound",
            details={"args": args, "timeout_seconds": timeout},
        )
    if len(completed.stdout) > MAX_GIT_OUTPUT_BYTES:
        E.fail(
            E.REPOSITORY_INVALID,
            "a Git command produced more output than the supported bound",
            details={"args": args, "limit": MAX_GIT_OUTPUT_BYTES},
        )
    stderr = redact_text(completed.stderr.decode("utf-8", "replace").strip())
    return GitResult(completed.returncode, completed.stdout, stderr)


def _git_text(root: Path, args: list[str], *, timeout: float = GIT_TIMEOUT_SECONDS) -> str | None:
    result = run_git(root, args, timeout=timeout)
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", "replace").strip()


def _opaque(prefix: str, material: str) -> str:
    return f"{prefix}-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:32]}"


@dataclass(frozen=True)
class WorktreeIdentity:
    toplevel: Path
    worktree_key: WorktreeKey
    repository_id: str


def identify_worktree(repo_path: Path) -> WorktreeIdentity:
    """Resolve a configured path to one physical worktree identity.

    Symlinked or otherwise aliased paths to the same checkout collapse to one
    key; a linked ``git worktree`` gets a distinct key while sharing the
    repository id.
    """

    candidate = Path(repo_path).expanduser()
    if not candidate.is_dir():
        E.fail(
            E.REPOSITORY_INVALID,
            "configured repository path is not an existing directory",
            details={"path": str(candidate)},
        )
    toplevel_text = _git_text(candidate, ["rev-parse", "--show-toplevel"])
    if not toplevel_text:
        E.fail(
            E.REPOSITORY_INVALID,
            "configured repository path is not inside a Git worktree",
            details={"path": str(candidate)},
        )
    common_text = _git_text(candidate, ["rev-parse", "--path-format=absolute", "--git-common-dir"])
    if not common_text:
        E.fail(
            E.REPOSITORY_INVALID,
            "unable to resolve the Git common directory",
            details={"path": str(candidate)},
        )
    toplevel = Path(toplevel_text).resolve()
    common = Path(common_text).resolve()
    return WorktreeIdentity(
        toplevel=toplevel,
        worktree_key=WorktreeKey(_opaque("wt", str(toplevel))),
        repository_id=_opaque("repo", str(common)),
    )


# --------------------------------------------------------------------------
# Working-tree content identity
# --------------------------------------------------------------------------


def _entry_content(path: Path) -> tuple[str, bool]:
    """Return a stable content token for one dirty path plus completeness."""

    try:
        stat = path.lstat()
    except OSError:
        return "absent", True
    mode = stat.st_mode
    if os.path.islink(path):
        try:
            return "symlink:" + os.readlink(path), True
        except OSError:
            return "symlink:unreadable", False
    if not os.path.isfile(path):
        # FIFOs, sockets, devices: no safe bounded content identity exists.
        return f"special:{mode:o}", False
    if stat.st_size > MAX_DIRTY_FILE_BYTES:
        return f"oversize:{stat.st_size}", False
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return "unreadable", False
    return f"blob:{digest}", True


def _parse_porcelain(payload: bytes) -> list[tuple[str, str]]:
    """Parse ``git status --porcelain=v1 -z`` into (status, path) pairs."""

    fields = payload.split(b"\x00")
    entries: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        text = field.decode("utf-8", "surrogateescape")
        if len(text) < 4:
            continue
        status, path = text[:2], text[3:]
        entries.append((status, path))
        if status[0] in {"R", "C"}:
            # Rename/copy records carry the original path in the next field.
            if index < len(fields):
                origin = fields[index].decode("utf-8", "surrogateescape")
                index += 1
                entries.append((status[0] + "<", origin))
    return entries


def working_tree_identity(toplevel: Path) -> tuple[DigestRef | None, bool]:
    """Digest materially different working-tree content, if any.

    Returns ``(None, True)`` for a clean tree. A dirty tree yields a versioned
    digest under ``sdp.git-working-tree.v1``; completeness is ``False`` whenever
    any path could not be bounded-fingerprinted safely.
    """

    result = run_git(
        toplevel,
        ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none"],
    )
    if result.returncode != 0:
        E.fail(
            E.REPOSITORY_INVALID,
            "unable to inspect Git working-tree status",
            details={"stderr": result.stderr},
        )
    entries = _parse_porcelain(result.stdout)
    if not entries:
        return None, True
    if len(entries) > MAX_DIRTY_PATHS:
        return (
            digest_canonical(
                {"overflow": True, "count": len(entries)}, SCHEME_GIT_WORKING_TREE
            ),
            False,
        )
    complete = True
    records: list[dict[str, str]] = []
    for status, path in sorted(set(entries)):
        content, ok = _entry_content(toplevel / path)
        complete = complete and ok
        records.append({"status": status, "path": path, "content": content})
    return digest_canonical({"entries": records}, SCHEME_GIT_WORKING_TREE), complete


# --------------------------------------------------------------------------
# Remotes
# --------------------------------------------------------------------------


def _classify_remote_url(url: str) -> tuple[str, bool]:
    """Return ``(scheme, web_addressable)`` for a configured remote URL."""

    lowered = url.strip()
    if "://" in lowered:
        scheme = lowered.split("://", 1)[0].lower()
        return scheme, scheme in _WEB_SCHEMES
    if _SCP_LIKE.match(lowered):
        return "ssh", True
    return "path", False


def list_remotes(toplevel: Path) -> dict[str, str]:
    text = _git_text(toplevel, ["remote"])
    names = [line.strip() for line in (text or "").splitlines() if line.strip()]
    remotes: dict[str, str] = {}
    for name in names:
        url = _git_text(toplevel, ["remote", "get-url", name])
        if url:
            remotes[name] = url.strip()
    return remotes


def select_remote(
    toplevel: Path, *, configured_name: str | None, branch: str | None
) -> RemoteRepositoryRef:
    """Apply the frozen remote-selection precedence.

    configured name -> current-branch upstream remote -> ``origin`` -> sole remote.
    Anything less determinate is an explicit ambiguity, never a guess.
    """

    remotes = list_remotes(toplevel)
    if not remotes:
        E.fail(
            E.REMOTE_UNAVAILABLE,
            "the repository has no configured Git remote",
            remediation="configure a remote or render with --prompt-mode local",
        )

    chosen: str | None = None
    if configured_name:
        if configured_name not in remotes:
            E.fail(
                E.REMOTE_UNAVAILABLE,
                "the configured remote_name is not defined in the repository",
                details={"remote_name": configured_name, "available": sorted(remotes)},
            )
        chosen = configured_name
    if chosen is None and branch:
        upstream_remote = _git_text(toplevel, ["config", "--get", f"branch.{branch}.remote"])
        if upstream_remote and upstream_remote in remotes:
            chosen = upstream_remote
    if chosen is None and "origin" in remotes:
        chosen = "origin"
    if chosen is None and len(remotes) == 1:
        chosen = next(iter(remotes))
    if chosen is None:
        E.fail(
            E.REMOTE_AMBIGUOUS,
            "multiple Git remotes exist and none is uniquely selected",
            details={"available": sorted(remotes)},
            remediation="set projects.<key>.remote_name to the intended remote",
        )

    url = remotes[chosen]
    scheme, web_addressable = _classify_remote_url(url)
    return RemoteRepositoryRef(
        remote_name=chosen,
        sanitized_repository=sanitize_url(url),
        scheme=scheme,
        web_addressable=web_addressable,
    )


def _upstream_ref(toplevel: Path) -> str | None:
    return _git_text(toplevel, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])


def ls_remote_head(toplevel: Path, remote: str, branch: str) -> str | None:
    """One bounded, noninteractive, read-only remote query.

    ``ls-remote`` never writes refs, the working tree, or the index. A failure is
    reported as unknown rather than raised, so callers can distinguish "target
    absent" from "query impossible" at the policy layer.
    """

    result = run_git(
        toplevel,
        ["ls-remote", "--heads", "--", remote, f"refs/heads/{branch}"],
        timeout=GIT_REMOTE_TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        return None
    text = result.stdout.decode("utf-8", "replace").strip()
    if not text:
        return ""
    first = text.splitlines()[0].split("\t")[0].strip()
    return first or ""


# --------------------------------------------------------------------------
# Candidate observation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Observation:
    candidate: CandidateRef
    remote: RemoteRepositoryRef | None
    diagnostics: tuple[str, ...]


def observe(
    identity: WorktreeIdentity,
    *,
    remote_mode: RemoteMode,
    configured_remote_name: str | None,
) -> Observation:
    """Observe the candidate without mutating anything in the target."""

    toplevel = identity.toplevel
    head = _git_text(toplevel, ["rev-parse", "HEAD"])
    branch = _git_text(toplevel, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    detached = branch is None
    tree_digest, complete = working_tree_identity(toplevel)

    diagnostics: list[str] = []
    remote: RemoteRepositoryRef | None = None
    upstream: str | None = None
    observed_remote_commit: str | None = None
    evidence = RemoteEvidence.NONE

    if remote_mode is not RemoteMode.LOCAL_ONLY:
        try:
            remote = select_remote(
                toplevel, configured_name=configured_remote_name, branch=branch
            )
        except E.OrchestratorError as exc:
            diagnostics.append(f"{exc.problem.code}: {exc.problem.message}")
        if remote is not None and not detached:
            upstream = _upstream_ref(toplevel)
            if upstream:
                cached = _git_text(toplevel, ["rev-parse", "--verify", "--quiet", upstream])
                if cached:
                    observed_remote_commit = cached
                    evidence = RemoteEvidence.CACHED
                else:
                    diagnostics.append(
                        f"upstream {upstream} has no local remote-tracking commit"
                    )
            if remote_mode is RemoteMode.REFRESH_REMOTE and branch:
                target_branch = upstream.split("/", 1)[1] if upstream else branch
                refreshed = ls_remote_head(toplevel, remote.remote_name, target_branch)
                if refreshed is None:
                    diagnostics.append(
                        f"bounded remote query against {remote.remote_name} did not succeed"
                    )
                elif refreshed == "":
                    observed_remote_commit = None
                    evidence = RemoteEvidence.REFRESHED
                    diagnostics.append(
                        f"remote {remote.remote_name} has no branch {target_branch}"
                    )
                else:
                    observed_remote_commit = refreshed
                    evidence = RemoteEvidence.REFRESHED

    candidate = CandidateRef(
        repository_id=identity.repository_id,
        branch=branch,
        detached=detached,
        head_commit=head,
        working_tree_digest=tree_digest,
        identity_complete=bool(head) and complete,
        upstream_ref=upstream,
        observed_remote_commit=observed_remote_commit,
        remote_evidence=evidence,
        observed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    return Observation(candidate=candidate, remote=remote, diagnostics=tuple(diagnostics))
