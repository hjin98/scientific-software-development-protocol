"""Resolution of version-selected canonical Protocol prompt/profile material.

Precedence for one explicit profile remains:

    configured compatible local source
      -> exact compatible packaged snapshot
      -> explicitly permitted remote source at an explicit ref
      -> truthful incompatible/unavailable failure

Protocol 5.16 and Protocol 6.0 are separate profile/source contracts.  A source
for one is never silently interpreted under the other.
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
PACKAGED_PROMPTS = "prompts.md"
PACKAGED_PROFILE = "profile.json"


@dataclass(frozen=True)
class ResolvedProtocolSource:
    source: PromptSourceRef
    document: CanonicalDocument
    snapshot: P.ProfileSnapshot
    mutable_identity: DigestRef | None


def _require_compatible(protocol_version: str, *, profile_id: str, origin: str) -> None:
    compatible = P.compatible_versions(profile_id)
    if protocol_version not in compatible:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "the Protocol source declares a version incompatible with the requested profile",
            details={"declared": protocol_version, "profile": profile_id, "origin": origin, "compatible": list(compatible)},
            remediation="configure the profile/source matching the governing workplan protocol version",
        )


def _read_bounded(path: Path, limit: int, label: str) -> str:
    if not path.is_file():
        E.fail(E.PROTOCOL_UNAVAILABLE, f"the configured Protocol source has no {label}", details={"path": str(path)})
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
                    E.fail(E.PROTOCOL_UNAVAILABLE, f"the Protocol source {label} exceeds the supported size bound", details={"path": str(path), "limit": limit})
        return b"".join(chunks).decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        E.fail(E.PROTOCOL_UNAVAILABLE, f"unable to read the Protocol source {label}: {exc}")


def resolve_local(local_root: Path, *, profile_id: str = P.PROFILE_ID) -> ResolvedProtocolSource:
    P.definition(profile_id)
    root = Path(local_root).expanduser()
    if not root.is_dir():
        E.fail(E.PROTOCOL_UNAVAILABLE, "the configured Protocol local_root is not an existing directory", details={"path": str(root)})
    first_version = _read_bounded(root / CANONICAL_VERSION_RELPATH, 4096, "PROTOCOL_VERSION")
    first_prompts = _read_bounded(root / CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES, "canonical prompt document")
    second_version = _read_bounded(root / CANONICAL_VERSION_RELPATH, 4096, "PROTOCOL_VERSION")
    second_prompts = _read_bounded(root / CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES, "canonical prompt document")
    if (first_version, first_prompts) != (second_version, second_prompts):
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the local Protocol source changed while it was being read", details={"root": str(root)}, remediation="retry after the local Protocol checkout is stable")
    version_text = first_version.strip()
    _require_compatible(version_text, profile_id=profile_id, origin="local_root")
    document = parse_document(first_prompts, profile_id=profile_id)
    identity = digest_bytes((version_text + "\n" + first_prompts).encode("utf-8"), SCHEME_CONTENT)
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="local",
            identity=identity.value,
            sanitized_location=str(root),
            content_digests=(("PROTOCOL_VERSION", digest_bytes(version_text.encode("utf-8"), SCHEME_CONTENT)), (CANONICAL_PROMPTS_RELPATH, document.content_digest)),
        ),
        document=document,
        snapshot=P.build_profile(document, profile_id),
        mutable_identity=identity,
    )


def _packaged_dir(profile_id: str):
    return resources.files("sdp_orchestrator.core").joinpath("resources", "protocol", profile_id)


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
                    E.fail(E.PROTOCOL_UNAVAILABLE, f"the packaged Protocol {label} exceeds the supported size bound", details={"limit": limit})
        return b"".join(chunks).decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        E.fail(E.PROTOCOL_UNAVAILABLE, f"the packaged Protocol {label} could not be read: {type(exc).__name__}")


def resolve_packaged(profile_id: str = P.PROFILE_ID) -> ResolvedProtocolSource:
    """Read a reproducible profile/version-bound snapshot shipped in the wheel."""

    defn = P.definition(profile_id)
    base = _packaged_dir(profile_id)
    prompts_res = base.joinpath(PACKAGED_PROMPTS)
    profile_res = base.joinpath(PACKAGED_PROFILE)
    if not prompts_res.is_file() or not profile_res.is_file():
        E.fail(E.PROTOCOL_UNAVAILABLE, "this build ships no packaged snapshot for the requested profile", details={"profile": profile_id})
    prompts = _read_resource_bounded(prompts_res, MAX_PROTOCOL_SOURCE_BYTES, "prompt snapshot")
    profile_text = _read_resource_bounded(profile_res, MAX_PROTOCOL_PROFILE_BYTES, "profile")
    document = parse_document(prompts, profile_id=profile_id)
    packaged_descriptor = P.profile_from_json(profile_text)
    derived = P.build_profile(document, profile_id)
    if packaged_descriptor != derived.descriptor:
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the packaged profile is not the reproducible derivative of its packaged prompt source", details={"profile": profile_id}, remediation="regenerate the packaged snapshot from its canonical version-bound source")
    if packaged_descriptor.profile.protocol_version != defn.protocol_version:
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the packaged profile protocol version does not match its registered profile definition", details={"profile": profile_id})
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="packaged",
            identity=document.content_digest.value,
            sanitized_location=f"packaged:{profile_id}",
            content_digests=((PACKAGED_PROMPTS, document.content_digest), (PACKAGED_PROFILE, digest_bytes(profile_text.encode("utf-8"), SCHEME_CONTENT))),
        ),
        document=document,
        snapshot=derived,
        mutable_identity=None,
    )


def _run(args: list[str], *, cwd: Path | None = None) -> GitResult:
    try:
        return run_bounded(args, timeout=REMOTE_READ_TIMEOUT_SECONDS, max_output_bytes=MAX_REMOTE_READ_BYTES, env=_git_env(), cwd=cwd)
    except FileNotFoundError:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the 'git' executable is not available for remote Protocol reads")
    except _BoundedRunError as exc:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "a remote Protocol read exceeded its time bound" if exc.reason == "timeout" else "a remote Protocol read exceeded the supported transfer bound",
            retryable=exc.reason == "timeout",
            details={"stream": exc.stream} if exc.stream else None,
        )


def resolve_remote(section: ProtocolSourceSection, *, profile_id: str = P.PROFILE_ID) -> ResolvedProtocolSource:
    """Read one explicit profile from one pinned remote ref without executing it."""

    P.definition(profile_id)
    if not section.allow_remote:
        E.fail(E.PROTOCOL_UNAVAILABLE, "remote Protocol source resolution is disabled for this source", remediation="set allow_remote = true with an explicit remote_repository and remote_ref")
    repository = section.remote_repository or ""
    ref = section.remote_ref or ""
    sanitized = sanitize_url(repository)

    listing = _run(["git", "ls-remote", "--", repository, ref])
    if listing.returncode != 0:
        E.fail(E.PROTOCOL_UNAVAILABLE, "the remote Protocol repository could not be queried", details={"repository": sanitized, "ref": ref, "stderr": listing.stderr})
    rows = [line.split("\t") for line in listing.stdout.decode("utf-8", "replace").splitlines() if "\t" in line]
    commits = {row[0].strip() for row in rows}
    if len(commits) != 1:
        E.fail(E.PROTOCOL_UNAVAILABLE if not commits else E.PROTOCOL_SOURCE_INCOHERENT, "the requested remote ref does not resolve to exactly one commit", details={"repository": sanitized, "ref": ref, "matches": len(commits)})
    commit = next(iter(commits))

    archive = _run(["git", "archive", "--remote", repository, ref, "--", CANONICAL_VERSION_RELPATH, CANONICAL_PROMPTS_RELPATH])
    if archive.returncode != 0:
        stderr = archive.stderr
        lowered = stderr.lower()
        missing_required_path = any(
            marker in lowered
            for marker in (
                "pathspec",
                "did not match any files",
                "path not found",
            )
        )
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT if missing_required_path else E.PROTOCOL_UNAVAILABLE,
            (
                "the pinned remote Protocol commit does not contain every required canonical file"
                if missing_required_path
                else "the remote Protocol source could not be read"
            ),
            details={"repository": sanitized, "ref": ref, "commit": commit, "stderr": stderr},
        )

    confirmation = _run(["git", "ls-remote", "--", repository, ref])
    confirmed_commits = {line.split("\t", 1)[0].strip() for line in confirmation.stdout.decode("utf-8", "replace").splitlines() if "\t" in line} if confirmation.returncode == 0 else set()
    if confirmed_commits != {commit}:
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT if confirmed_commits else E.PROTOCOL_UNAVAILABLE, "the remote Protocol ref could not be immutably revalidated after its bounded read", details={"repository": sanitized, "ref": ref})

    try:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:*") as bundle:
            members = {member.name: member for member in bundle.getmembers()}

            def archive_file(relpath: str, limit: int) -> str:
                member = members.get(relpath)
                if member is None or not member.isfile():
                    E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the pinned remote Protocol commit does not contain a required file", details={"repository": sanitized, "commit": commit, "path": relpath})
                handle = bundle.extractfile(member)
                if handle is None:
                    E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the pinned remote Protocol file could not be materialized", details={"path": relpath})
                content = handle.read(limit + 1)
                if len(content) > limit:
                    E.fail(E.PROTOCOL_UNAVAILABLE, "a remote Protocol file exceeds the supported size bound", details={"path": relpath, "limit": limit})
                try:
                    return content.decode("utf-8")
                except UnicodeDecodeError:
                    E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "a remote Protocol file is not valid UTF-8", details={"path": relpath})

            version_text = archive_file(CANONICAL_VERSION_RELPATH, 4096).strip()
            prompts = archive_file(CANONICAL_PROMPTS_RELPATH, MAX_PROTOCOL_SOURCE_BYTES)
    except (tarfile.TarError, OSError) as exc:
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the remote Protocol archive is not a valid bounded source bundle", details={"repository": sanitized, "error": type(exc).__name__})

    _require_compatible(version_text, profile_id=profile_id, origin="remote")
    document = parse_document(prompts, profile_id=profile_id)
    return ResolvedProtocolSource(
        source=PromptSourceRef(
            kind="remote",
            identity=commit,
            sanitized_location=sanitized,
            requested_ref=ref,
            resolved_ref=commit,
            content_digests=(("PROTOCOL_VERSION", digest_bytes(version_text.encode("utf-8"), SCHEME_CONTENT)), (CANONICAL_PROMPTS_RELPATH, document.content_digest)),
        ),
        document=document,
        snapshot=P.build_profile(document, profile_id),
        mutable_identity=None,
    )


def resolve(section: ProtocolSourceSection | None, *, profile_id: str) -> ResolvedProtocolSource:
    """Apply frozen source precedence for one explicitly selected profile."""

    P.definition(profile_id)
    if section is not None and section.local_root:
        return resolve_local(Path(section.local_root), profile_id=profile_id)
    try:
        return resolve_packaged(profile_id)
    except E.OrchestratorError as packaged_problem:
        if section is not None and section.allow_remote:
            return resolve_remote(section, profile_id=profile_id)
        raise packaged_problem
