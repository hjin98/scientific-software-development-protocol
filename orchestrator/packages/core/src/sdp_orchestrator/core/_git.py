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
import selectors
import stat as stat_module
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import _errors as E
from ._digest import SCHEME_GIT_WORKING_TREE, digest_bytes, digest_canonical
from ._limits import (
    GIT_REMOTE_TIMEOUT_SECONDS,
    GIT_TIMEOUT_SECONDS,
    MAX_DIRTY_CONTENT_BYTES,
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
_SAFE_ENVIRONMENT = frozenset(
    {
        "PATH",
        "HOME",
        "USER",
        "LOGNAME",
        "TMPDIR",
        "XDG_CONFIG_HOME",
        "XDG_CACHE_HOME",
        "XDG_DATA_HOME",
        "SSH_AUTH_SOCK",
        "SSH_AGENT_PID",
        "GIT_SSH",
        "GIT_SSH_COMMAND",
        "GIT_SSH_VARIANT",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "CURL_CA_BUNDLE",
    }
)


def _git_env() -> dict[str, str]:
    """A noninteractive, non-mutating, credential-quiet environment."""

    # Do not inherit ambient GIT_* variables that can redirect repository
    # discovery, configuration, objects, refs, or the index. HOME and the
    # established transport variables remain available for credential helpers.
    env = {name: value for name, value in os.environ.items() if name in _SAFE_ENVIRONMENT}
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
    return env


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: bytes
    stderr: str


class _BoundedRunError(Exception):
    def __init__(self, reason: str, stream: str | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.stream = stream


def run_bounded(
    command: list[str],
    *,
    cwd: Path | None = None,
    timeout: float,
    max_output_bytes: int,
    env: dict[str, str] | None = None,
) -> GitResult:
    """Run a fixed command while bounding both pipes during collection."""

    process = subprocess.Popen(  # noqa: S603 - callers provide fixed argv
        command,
        cwd=str(cwd) if cwd is not None else None,
        env=env if env is not None else _git_env(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    selector = selectors.DefaultSelector()
    streams: dict[int, tuple[str, bytearray]] = {}
    assert process.stdout is not None
    assert process.stderr is not None
    stdout_fd = process.stdout.fileno()
    stderr_fd = process.stderr.fileno()
    for name, pipe in (("stdout", process.stdout), ("stderr", process.stderr)):
        selector.register(pipe, selectors.EVENT_READ, name)
        streams[pipe.fileno()] = (name, bytearray())

    deadline = time.monotonic() + timeout
    total_bytes = 0
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                process.kill()
                process.wait()
                raise _BoundedRunError("timeout")
            for key, _ in selector.select(min(remaining, 0.1)):
                pipe = key.fileobj
                chunk = os.read(pipe.fileno(), 64 * 1024)
                if not chunk:
                    selector.unregister(pipe)
                    continue
                name, buffer = streams[pipe.fileno()]
                buffer.extend(chunk)
                total_bytes += len(chunk)
                if total_bytes > max_output_bytes:
                    process.kill()
                    process.wait()
                    raise _BoundedRunError("output", name)

        returncode = process.wait()
        stdout = bytes(streams[stdout_fd][1])
        stderr = redact_text(
            bytes(streams[stderr_fd][1]).decode("utf-8", "replace").strip()
        )
        return GitResult(returncode, stdout, stderr)
    finally:
        selector.close()
        for pipe in (process.stdout, process.stderr):
            if pipe is not None and not pipe.closed:
                pipe.close()
        if process.poll() is None:
            process.kill()
            process.wait()


def run_git(
    root: Path, args: list[str], *, timeout: float = GIT_TIMEOUT_SECONDS
) -> GitResult:
    """Run one bounded read-only Git command rooted at ``root``."""

    command = ["git", "--no-optional-locks", "-C", str(root), *args]
    try:
        return run_bounded(
            command,
            timeout=timeout,
            max_output_bytes=MAX_GIT_OUTPUT_BYTES,
            env=_git_env(),
        )
    except FileNotFoundError:
        E.fail(
            E.REPOSITORY_INVALID,
            "the 'git' executable is not available",
            remediation="install Git or make it available on PATH",
        )
    except _BoundedRunError as exc:
        if exc.reason == "output":
            E.fail(
                E.REPOSITORY_INVALID,
                "a Git command produced more output than the supported bound",
                details={"args": args, "stream": exc.stream, "limit": MAX_GIT_OUTPUT_BYTES},
            )
        E.fail(
            E.REPOSITORY_INVALID,
            "a Git command exceeded its time bound",
            details={"args": args, "timeout_seconds": timeout},
            retryable=True,
        )


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
            target = os.fsencode(os.readlink(path)).hex()
            return f"symlink:{mode:o}:{target}", True
        except OSError:
            return f"symlink:{mode:o}:unreadable", False
    if not stat_module.S_ISREG(mode):
        # FIFOs, sockets, devices: no safe bounded content identity exists.
        return f"special:{mode:o}", False
    if stat.st_size > MAX_DIRTY_FILE_BYTES:
        return f"oversize:{stat.st_size}", False
    try:
        digest_builder = hashlib.sha256()
        total = 0
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(min(64 * 1024, MAX_DIRTY_FILE_BYTES - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_DIRTY_FILE_BYTES:
                    return f"oversize:>{MAX_DIRTY_FILE_BYTES}", False
                digest_builder.update(chunk)
    except OSError:
        return "unreadable", False
    return f"file:{mode:o}:blob:{digest_builder.hexdigest()}", True


def _path_token(path: str) -> str:
    """Encode a Git path without placing surrogate escapes in JSON."""

    return "hex:" + os.fsencode(path).hex()


def _entry_metadata(path: Path) -> dict[str, int | str]:
    try:
        stat = path.lstat()
    except OSError:
        return {"state": "unreadable"}
    return {"mode": stat.st_mode, "size": stat.st_size}


def _staged_identity(toplevel: Path) -> DigestRef | None:
    """Digest the index patch, including staged blob ids and file modes."""

    result = run_git(
        toplevel,
        ["diff", "--cached", "--raw", "-z", "--no-renames", "--no-abbrev"],
    )
    if result.returncode != 0:
        E.fail(
            E.REPOSITORY_INVALID,
            "unable to inspect the Git index state",
            details={"stderr": result.stderr},
        )
    if not result.stdout:
        return None
    return digest_bytes(result.stdout, SCHEME_GIT_WORKING_TREE)


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
    staged = _staged_identity(toplevel)
    complete = True
    total_bytes = 0
    unique_entries = sorted(set(entries))
    for _, path in unique_entries:
        try:
            candidate = toplevel / path
            stat = candidate.lstat()
        except OSError:
            continue
        if stat_module.S_ISREG(stat.st_mode):
            total_bytes += stat.st_size
        if total_bytes > MAX_DIRTY_CONTENT_BYTES:
            return (
                digest_canonical(
                    {
                        "staged": staged.value if staged else None,
                        "overflow": [
                            {
                                "status": status,
                                "path": _path_token(item_path),
                                "metadata": _entry_metadata(toplevel / item_path),
                            }
                            for status, item_path in unique_entries
                        ],
                    },
                    SCHEME_GIT_WORKING_TREE,
                ),
                False,
            )
    records: list[dict[str, str]] = []
    for status, path in unique_entries:
        content, ok = _entry_content(toplevel / path)
        complete = complete and ok
        records.append({"status": status, "path": _path_token(path), "content": content})
    return digest_canonical(
        {"staged": staged.value if staged else None, "entries": records},
        SCHEME_GIT_WORKING_TREE,
    ), complete


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


def _upstream_parts(value: str | None) -> tuple[str, str] | None:
    if not value or "/" not in value:
        return None
    remote, branch = value.split("/", 1)
    return (remote, branch) if remote and branch else None


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
    max_remote_staleness_seconds: int | None = None,
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
    remote_observed_at: str | None = None
    observed_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")

    if max_remote_staleness_seconds is not None and max_remote_staleness_seconds < 0:
        E.fail(
            E.CONFIG_INVALID,
            "max_remote_staleness_seconds must be non-negative",
            details={"value": max_remote_staleness_seconds},
        )

    if remote_mode is not RemoteMode.LOCAL_ONLY:
        try:
            remote = select_remote(
                toplevel, configured_name=configured_remote_name, branch=branch
            )
        except E.OrchestratorError as exc:
            diagnostics.append(f"{exc.problem.code}: {exc.problem.message}")
        if remote is not None and not detached:
            upstream = _upstream_ref(toplevel)
            upstream_parts = _upstream_parts(upstream)
            target_branch = branch
            if upstream_parts and upstream_parts[0] == remote.remote_name:
                target_branch = upstream_parts[1]
            if target_branch:
                selected_tracking_ref = f"refs/remotes/{remote.remote_name}/{target_branch}"
                cached = _git_text(
                    toplevel,
                    ["rev-parse", "--verify", "--quiet", selected_tracking_ref],
                )
                if cached:
                    observed_remote_commit = cached
                    evidence = RemoteEvidence.CACHED
                elif upstream_parts and upstream_parts[0] == remote.remote_name:
                    diagnostics.append(
                        f"upstream {upstream} has no local remote-tracking commit"
                    )
            if remote_mode is RemoteMode.REFRESH_REMOTE and branch:
                refreshed = ls_remote_head(toplevel, remote.remote_name, target_branch)
                if refreshed is None:
                    diagnostics.append(
                        f"bounded remote query against {remote.remote_name} did not succeed"
                    )
                elif refreshed == "":
                    observed_remote_commit = None
                    evidence = RemoteEvidence.REFRESHED
                    remote_observed_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
                    diagnostics.append(
                        f"remote {remote.remote_name} has no branch {target_branch}"
                    )
                else:
                    observed_remote_commit = refreshed
                    evidence = RemoteEvidence.REFRESHED
                    remote_observed_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")

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
        remote_observed_at=remote_observed_at,
        observed_at=observed_at,
    )
    return Observation(candidate=candidate, remote=remote, diagnostics=tuple(diagnostics))
