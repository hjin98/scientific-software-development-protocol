"""Resolution of the Core *render source* for canonical prompt/profile material.

Precedence is frozen:

    explicit configured compatible local source
      -> exact compatible packaged snapshot
      -> explicitly permitted remote source at an explicit ref
      -> truthful incompatible/unavailable failure

The resulting :class:`PromptSourceRef` is Core provenance only. It is *not* the
agent-facing ``PROTOCOL_SOURCE`` input, so a local render-source path can never
reach a web prompt merely because Core happened to read from it.

Remote resolution reads an explicit ref once, pins it to an immutable commit, and
reads every file for that preparation from that one identity. Downloaded bytes
are data: they are parsed, never executed, and never handed to a build hook.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from . import _errors as E
from . import _profile as P
from ._canonical import CanonicalDocument, parse_document
from ._config import ProtocolSourceSection
from ._digest import SCHEME_CONTENT, digest_bytes
from ._git import _git_env
from ._limits import (
    MAX_PROTOCOL_PROFILE_BYTES,
    MAX_PROTOCOL_SOURCE_BYTES,
    MAX_REMOTE_READ_BYTES,
    REMOTE_READ_TIMEOUT_SECONDS,
)
from ._records import DigestRef, PromptSourceRef
from ._redact import redact_text, sanitize_url

CANONICAL_PROMPTS_RELPATH = "source/shared/references/development-workflow-prompts.md"
CANONICAL_VERSION_RELPATH = "source/PROTOCOL_VERSION"

PACKAGED_ROOT = "resources.protocol"
PACKAGED_PROMPTS = "prompts.md"
PACKAGED_PROFILE = "profile.json"


@dataclass(frozen=True)
class ResolvedProtocolSource:
    source: PromptSourceRef
    document: CanonicalDocument
    snapshot: P.ProfileSnapshot
    mutable_identity: DigestRef | None
    """Identity to re-check before final render; ``None`` for immutable sources."""


def _require_compatible(protocol_version: str, *, origin: str) -> None:
    if protocol_version not in P.COMPATIBLE_PROTOCOL_VERSIONS:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "the Protocol source declares a version this build has no compatible profile for",
            details={
                "declared": protocol_version,
                "origin": origin,
                "compatible": list(P.COMPATIBLE_PROTOCOL_VERSIONS),
            },
            remediation="configure a compatible Protocol source or use a build that ships that profile",
        )


def _read_bounded(path: Path, limit: int, label: str) -> str:
    if not path.is_file():
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            f"the configured Protocol source has no {label}",
            details={"path": str(path)},
        )
    size = path.stat().st_size
    if size > limit:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            f"the Protocol source {label} exceeds the supported size bound",
            details={"path": str(path), "bytes": size, "limit": limit},
        )
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        E.fail(E.PROTOCOL_UNAVAILABLE, f"unable to read the Protocol source {label}: {exc}")


# --------------------------------------------------------------------------
# Local source
# --------------------------------------------------------------------------


def resolve_local(local_root: Path) -> ResolvedProtocolSource:
    root = Path(local_root).expanduser()
    if not root.is_dir():
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the configured Protocol local_root is not an existing directory",
            details={"path": str(root)},
        )
    version_text = _read_bounded(root / CANONICAL_VERSION_RELPATH, 4096, "PROTOCOL_VERSION").strip()
    _require_compatible(version_text, origin="local_root")
    prompts = _read_bounded(
        root / CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES, "canonical prompt document"
    )
    document = parse_document(prompts)
    identity = digest_bytes(
        (version_text + "\n" + prompts).encode("utf-8"), SCHEME_CONTENT
    )
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="local",
            identity=identity.value,
            sanitized_location=str(root),
            content_digests=(
                ("PROTOCOL_VERSION", digest_bytes(version_text.encode("utf-8"), SCHEME_CONTENT)),
                (CANONICAL_PROMPTS_RELPATH, document.content_digest),
            ),
        ),
        document=document,
        snapshot=P.build_profile(document),
        mutable_identity=identity,  # a local checkout can change under us
    )


# --------------------------------------------------------------------------
# Packaged snapshot
# --------------------------------------------------------------------------


def _packaged_dir(profile_id: str):
    return resources.files("sdp_orchestrator.core").joinpath(
        "resources", "protocol", profile_id
    )


def resolve_packaged(profile_id: str = P.PROFILE_ID) -> ResolvedProtocolSource:
    """Read the reproducible, version-bound snapshot shipped inside the wheel."""

    base = _packaged_dir(profile_id)
    prompts_res = base.joinpath(PACKAGED_PROMPTS)
    profile_res = base.joinpath(PACKAGED_PROFILE)
    if not prompts_res.is_file() or not profile_res.is_file():
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "this build ships no packaged snapshot for the requested profile",
            details={"profile": profile_id},
        )
    prompts = prompts_res.read_text(encoding="utf-8")
    if len(prompts.encode("utf-8")) > MAX_PROTOCOL_SOURCE_BYTES:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the packaged prompt snapshot exceeds the supported bound")
    profile_text = profile_res.read_text(encoding="utf-8")
    if len(profile_text.encode("utf-8")) > MAX_PROTOCOL_PROFILE_BYTES:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the packaged profile exceeds the supported bound")

    document = parse_document(prompts)
    packaged_descriptor = P.profile_from_json(profile_text)
    derived = P.build_profile(document)
    if packaged_descriptor != derived.descriptor:
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the packaged profile is not the reproducible derivative of the packaged prompt source",
            details={"profile": profile_id},
            remediation="regenerate the packaged snapshot from canonical source",
        )
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="packaged",
            identity=document.content_digest.value,
            sanitized_location=f"packaged:{profile_id}",
            content_digests=(
                (PACKAGED_PROMPTS, document.content_digest),
                (PACKAGED_PROFILE, digest_bytes(profile_text.encode("utf-8"), SCHEME_CONTENT)),
            ),
        ),
        document=document,
        snapshot=derived,
        mutable_identity=None,
    )


# --------------------------------------------------------------------------
# Remote source (opt-in)
# --------------------------------------------------------------------------


def _run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(  # noqa: S603 - fixed argv, no shell
            args,
            capture_output=True,
            timeout=REMOTE_READ_TIMEOUT_SECONDS,
            env=_git_env(),
            cwd=str(cwd) if cwd else None,
            check=False,
        )
    except FileNotFoundError:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the 'git' executable is not available for remote Protocol reads")
    except subprocess.TimeoutExpired:
        E.fail(E.PROTOCOL_UNAVAILABLE, "a remote Protocol read exceeded its time bound")


def resolve_remote(section: ProtocolSourceSection) -> ResolvedProtocolSource:
    """Read canonical material from an explicitly permitted remote at one pinned commit.

    The mirror is created in a private temporary directory, so nothing about the
    user's repositories is mutated. The requested ref is resolved to a commit
    once; every file for this preparation is then read from that commit.
    """

    if not section.allow_remote:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "remote Protocol source resolution is disabled for this source",
            remediation="set allow_remote = true with an explicit remote_repository and remote_ref",
        )
    repository = section.remote_repository or ""
    ref = section.remote_ref or ""
    sanitized = sanitize_url(repository)

    listing = _run(["git", "ls-remote", "--", repository, ref])
    if listing.returncode != 0:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the remote Protocol repository could not be queried",
            details={
                "repository": sanitized,
                "ref": ref,
                "stderr": redact_text(listing.stderr.decode("utf-8", "replace").strip()),
            },
        )
    rows = [
        line.split("\t")
        for line in listing.stdout.decode("utf-8", "replace").splitlines()
        if "\t" in line
    ]
    commits = {row[0].strip() for row in rows}
    if len(commits) != 1:
        E.fail(
            E.PROTOCOL_UNAVAILABLE if not commits else E.PROTOCOL_SOURCE_INCOHERENT,
            "the requested remote ref does not resolve to exactly one commit",
            details={"repository": sanitized, "ref": ref, "matches": len(commits)},
        )
    commit = next(iter(commits))

    workdir = Path(tempfile.mkdtemp(prefix="sdp-protocol-"))
    try:
        if _run(["git", "init", "--quiet", "--bare", str(workdir)]).returncode != 0:
            E.fail(E.PROTOCOL_UNAVAILABLE, "unable to prepare a temporary Protocol mirror")
        fetched = _run(
            ["git", "fetch", "--quiet", "--depth", "1", "--", repository, ref], cwd=workdir
        )
        if fetched.returncode != 0:
            E.fail(
                E.PROTOCOL_UNAVAILABLE,
                "the remote Protocol source could not be read",
                details={
                    "repository": sanitized,
                    "ref": ref,
                    "stderr": redact_text(fetched.stderr.decode("utf-8", "replace").strip()),
                },
            )
        head = _run(["git", "rev-parse", "FETCH_HEAD"], cwd=workdir)
        resolved = head.stdout.decode("utf-8", "replace").strip()
        if head.returncode != 0 or resolved != commit:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "the remote ref changed between resolution and read",
                details={"repository": sanitized, "ref": ref, "expected": commit, "read": resolved},
            )

        def _blob(relpath: str, limit: int) -> str:
            result = _run(["git", "cat-file", "blob", f"{commit}:{relpath}"], cwd=workdir)
            if result.returncode != 0:
                E.fail(
                    E.PROTOCOL_SOURCE_INCOHERENT,
                    "the pinned remote Protocol commit does not contain a required file",
                    details={"repository": sanitized, "commit": commit, "path": relpath},
                )
            if len(result.stdout) > min(limit, MAX_REMOTE_READ_BYTES):
                E.fail(
                    E.PROTOCOL_UNAVAILABLE,
                    "a remote Protocol file exceeds the supported size bound",
                    details={"path": relpath, "bytes": len(result.stdout)},
                )
            try:
                return result.stdout.decode("utf-8")
            except UnicodeDecodeError:
                E.fail(
                    E.PROTOCOL_SOURCE_INCOHERENT,
                    "a remote Protocol file is not valid UTF-8",
                    details={"path": relpath},
                )

        version_text = _blob(CANONICAL_VERSION_RELPATH, 4096).strip()
        _require_compatible(version_text, origin="remote")
        prompts = _blob(CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    document = parse_document(prompts)
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="remote",
            identity=commit,
            sanitized_location=sanitized,
            requested_ref=ref,
            resolved_ref=commit,
            content_digests=(
                ("PROTOCOL_VERSION", digest_bytes(version_text.encode("utf-8"), SCHEME_CONTENT)),
                (CANONICAL_PROMPTS_RELPATH, document.content_digest),
            ),
        ),
        document=document,
        snapshot=P.build_profile(document),
        mutable_identity=None,  # pinned to an immutable commit
    )


# --------------------------------------------------------------------------
# Precedence
# --------------------------------------------------------------------------


def resolve(
    section: ProtocolSourceSection | None, *, profile_id: str
) -> ResolvedProtocolSource:
    """Apply the frozen Protocol-source precedence for ``profile_id``."""

    if profile_id != P.PROFILE_ID:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "no compatible profile is available for the configured protocol_profile",
            details={"requested": profile_id, "available": [P.PROFILE_ID]},
        )
    if section is not None and section.local_root:
        return resolve_local(Path(section.local_root))
    try:
        return resolve_packaged(profile_id)
    except E.OrchestratorError as packaged_problem:
        if section is not None and section.allow_remote:
            return resolve_remote(section)
        raise packaged_problem
