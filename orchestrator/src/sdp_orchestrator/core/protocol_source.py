"""Resolution of the Core *render source* for canonical prompt/profile material.

Precedence is frozen:

    explicit configured compatible local source
      -> exact compatible packaged snapshot
      -> explicitly permitted remote source at an explicit ref
      -> truthful incompatible/unavailable failure

The resulting :class:`PromptSourceRef` is Core provenance only. It is *not* the
agent-facing ``PROTOCOL_SOURCE`` input, so a local render-source path can never
reach a web prompt merely because Core happened to read from it.

Remote resolution resolves an explicit ref, reads a bounded archive, and
revalidates the ref so every file for that preparation is tied to one commit.
Downloaded bytes are data: they are parsed, never executed, and never handed to
a build hook.
"""

from __future__ import annotations

import io
import tarfile
from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from . import errors as E
from . import profile as P
from .canonical import CanonicalDocument, parse_document
from .config import ProtocolSourceSection
from .digest import SCHEME_CONTENT, digest_bytes
from .git import GitResult, _BoundedRunError, _git_env, run_bounded
from .limits import (
    MAX_PROTOCOL_PROFILE_BYTES,
    MAX_PROTOCOL_SOURCE_BYTES,
    MAX_REMOTE_READ_BYTES,
    REMOTE_READ_TIMEOUT_SECONDS,
)
from .records import DigestRef, PromptSourceRef
from .redaction import sanitize_url

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
    try:
        chunks: list[bytes] = []
        total = 0
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(min(64 * 1024, limit - total + 1))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > limit:
                    E.fail(
                        E.PROTOCOL_UNAVAILABLE,
                        f"the Protocol source {label} exceeds the supported size bound",
                        details={"path": str(path), "limit": limit},
                    )
        return b"".join(chunks).decode("utf-8")
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
    first_version = _read_bounded(
        root / CANONICAL_VERSION_RELPATH, 4096, "PROTOCOL_VERSION"
    )
    first_prompts = _read_bounded(
        root / CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES, "canonical prompt document"
    )
    second_version = _read_bounded(
        root / CANONICAL_VERSION_RELPATH, 4096, "PROTOCOL_VERSION"
    )
    second_prompts = _read_bounded(
        root / CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES, "canonical prompt document"
    )
    if (first_version, first_prompts) != (second_version, second_prompts):
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the local Protocol source changed while it was being read",
            details={"root": str(root)},
            remediation="retry after the local Protocol checkout is stable",
        )
    version_text = first_version.strip()
    _require_compatible(version_text, origin="local_root")
    prompts = first_prompts
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


def _read_resource_bounded(resource: Traversable, limit: int, label: str) -> str:
    try:
        chunks: list[bytes] = []
        total = 0
        with resource.open("rb") as handle:
            while True:
                chunk = handle.read(min(64 * 1024, limit - total + 1))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > limit:
                    E.fail(
                        E.PROTOCOL_UNAVAILABLE,
                        f"the packaged Protocol {label} exceeds the supported size bound",
                        details={"limit": limit},
                    )
        return b"".join(chunks).decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            f"the packaged Protocol {label} could not be read: {type(exc).__name__}",
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
    prompts = _read_resource_bounded(
        prompts_res, MAX_PROTOCOL_SOURCE_BYTES, "prompt snapshot"
    )
    profile_text = _read_resource_bounded(profile_res, MAX_PROTOCOL_PROFILE_BYTES, "profile")

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


def _run(args: list[str], *, cwd: Path | None = None) -> GitResult:
    try:
        return run_bounded(
            args,
            timeout=REMOTE_READ_TIMEOUT_SECONDS,
            max_output_bytes=MAX_REMOTE_READ_BYTES,
            env=_git_env(),
            cwd=cwd,
        )
    except FileNotFoundError:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the 'git' executable is not available for remote Protocol reads")
    except _BoundedRunError as exc:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            (
                "a remote Protocol read exceeded its time bound"
                if exc.reason == "timeout"
                else "a remote Protocol read exceeded the supported transfer bound"
            ),
            retryable=exc.reason == "timeout",
            details={"stream": exc.stream} if exc.stream else None,
        )


def resolve_remote(section: ProtocolSourceSection) -> ResolvedProtocolSource:
    """Read canonical material from an explicitly permitted remote at one pinned commit.

    The required files are streamed from a bounded ``git archive`` response;
    Core does not fetch or mirror unrelated repository content. The requested
    ref is resolved and revalidated so every file for this preparation is tied
    to one commit.
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
                "stderr": listing.stderr,
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

    archive = _run(
        [
            "git",
            "archive",
            "--remote",
            repository,
            ref,
            "--",
            CANONICAL_VERSION_RELPATH,
            CANONICAL_PROMPTS_RELPATH,
        ]
    )
    if archive.returncode != 0:
        if "pathspec" in archive.stderr and "did not match any files" in archive.stderr:
            E.fail(
                E.PROTOCOL_SOURCE_INCOHERENT,
                "the pinned remote Protocol ref does not contain a required file",
                details={"repository": sanitized, "commit": commit},
            )
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the remote Protocol source could not be read",
            details={"repository": sanitized, "ref": ref, "stderr": archive.stderr},
        )

    confirmation = _run(["git", "ls-remote", "--", repository, ref])
    if confirmation.returncode != 0:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the remote Protocol ref could not be revalidated after its bounded read",
            details={"repository": sanitized, "ref": ref, "stderr": confirmation.stderr},
        )
    confirmed_commits = {
        line.split("\t", 1)[0].strip()
        for line in confirmation.stdout.decode("utf-8", "replace").splitlines()
        if "\t" in line
    }
    if confirmed_commits != {commit}:
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the remote ref changed while the Protocol source was being read",
            details={"repository": sanitized, "ref": ref},
        )

    try:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:*") as bundle:
            members = {member.name: member for member in bundle.getmembers()}

            def _archive_file(relpath: str, limit: int) -> str:
                member = members.get(relpath)
                if member is None or not member.isfile():
                    E.fail(
                        E.PROTOCOL_SOURCE_INCOHERENT,
                        "the pinned remote Protocol commit does not contain a required file",
                        details={"repository": sanitized, "commit": commit, "path": relpath},
                    )
                handle = bundle.extractfile(member)
                if handle is None:
                    E.fail(
                        E.PROTOCOL_SOURCE_INCOHERENT,
                        "the pinned remote Protocol file could not be materialized",
                        details={"path": relpath},
                    )
                content = handle.read(limit + 1)
                if len(content) > limit:
                    E.fail(
                        E.PROTOCOL_UNAVAILABLE,
                        "a remote Protocol file exceeds the supported size bound",
                        details={"path": relpath, "limit": limit},
                    )
                try:
                    return content.decode("utf-8")
                except UnicodeDecodeError:
                    E.fail(
                        E.PROTOCOL_SOURCE_INCOHERENT,
                        "a remote Protocol file is not valid UTF-8",
                        details={"path": relpath},
                    )

            version_text = _archive_file(CANONICAL_VERSION_RELPATH, 4096).strip()
            prompts = _archive_file(CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES)
    except (tarfile.TarError, OSError) as exc:
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the remote Protocol archive is not a valid bounded source bundle",
            details={"repository": sanitized, "error": type(exc).__name__},
        )

    _require_compatible(version_text, origin="remote")
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
