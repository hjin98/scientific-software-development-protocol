"""Workplan catalog, current-authority deduplication, and stage-specific resolution.

Two rules do most of the work here:

1. **No fuzzy selection.** Filename similarity, modification time, and directory
   ordering are never evidence. A plan is chosen by an exact selector, by an
   explicit ``target_branch`` binding, or because it is the only active plan.
2. **Supersession must be declared.** Documents sharing a ``workplan_id`` are
   collapsed only through explicit ``parent_workplan``/``supersedes_revision``
   evidence. Where that evidence does not single one out, the group is ambiguous
   and says so instead of picking a winner.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import frontmatter

from . import _errors as E
from ._digest import (
    SCHEME_WORKPLAN_ARTIFACT,
    SCHEME_WORKPLAN_SEMANTIC,
    digest_bytes,
    digest_canonical,
)
from ._limits import (
    MAX_WORKPLAN_BYTES,
    MAX_WORKPLAN_DEPTH,
    MAX_WORKPLAN_FILES,
    WORKPLAN_SUFFIXES,
)
from ._records import (
    LifecycleState,
    StageRef,
    WorkplanDescriptor,
    WorkplanPolicy,
    WorkplanRef,
    WorkplanResolution,
)

WORKPLAN_ROOTS: tuple[tuple[str, LifecycleState], ...] = (
    ("workplans/active", LifecycleState.ACTIVE),
    ("workplans/archive", LifecycleState.ARCHIVE),
)

#: Finite, tested, lifecycle-only exclusion list for ``sdp.workplan-semantic.v1``.
#: Every other frontmatter key -- including unknown future keys -- participates in
#: semantic identity, because an unrecognized key may carry binding authority.
SEMANTIC_EXCLUDED_KEYS: frozenset[str] = frozenset(
    {
        "status",
        "created_date",
        "frozen_date",
        "reviewed_date",
        "completed_date",
        "archived_date",
        "reopened_date",
        "refrozen_date",
        "reopened_again_date",
        "refrozen_again_date",
        "review_verdict",
        "reviewed_candidate",
        "revision",
        "supersedes_revision",
    }
)

_ACTIVE_STATUSES = frozenset({"active", "frozen", "in_progress", "draft", "reopened"})
_ARCHIVE_STATUSES = frozenset({"completed", "superseded", "archived", "abandoned"})


@dataclass(frozen=True)
class CatalogEntry:
    descriptor: WorkplanDescriptor
    relative_path: str
    declared_id: bool


def _is_scalar_tree(value: Any, depth: int = 0) -> bool:
    if depth > 12:
        return False
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, Mapping):
        return all(isinstance(k, str) and _is_scalar_tree(v, depth + 1) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(_is_scalar_tree(item, depth + 1) for item in value)
    return False


def _read_document(path: Path) -> tuple[dict[str, Any], str, bytes, tuple[str, ...]]:
    """Read one bounded workplan document as data.

    Returns ``(metadata, body, raw_bytes, diagnostics)``. Parsing is
    ``yaml.safe_load`` based: no arbitrary object construction, no repository code
    execution.
    """

    diagnostics: list[str] = []
    size = path.stat().st_size
    if size > MAX_WORKPLAN_BYTES:
        return {}, "", b"", (f"exceeds the {MAX_WORKPLAN_BYTES}-byte workplan bound",)
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return {}, "", raw, ("is not valid UTF-8",)
    try:
        document = frontmatter.loads(text)
    except Exception as exc:  # noqa: BLE001 - any parser failure is data-level
        return {}, text, raw, (f"frontmatter could not be parsed: {type(exc).__name__}",)
    metadata = dict(document.metadata or {})
    if not _is_scalar_tree(metadata):
        diagnostics.append("frontmatter contains non-scalar data and is treated as incomplete")
        metadata = {}
    return metadata, document.content, raw, tuple(diagnostics)


def _semantic_digest(metadata: Mapping[str, Any], body: str) -> Any:
    payload = {
        "frontmatter": {
            key: metadata[key] for key in sorted(metadata) if key not in SEMANTIC_EXCLUDED_KEYS
        },
        "body": body,
    }
    return digest_canonical(payload, SCHEME_WORKPLAN_SEMANTIC)


def _iter_files(root: Path, base: Path) -> Iterable[Path]:
    """Yield regular workplan files under ``root`` without escaping ``base``."""

    stack = [(root, 0)]
    seen = 0
    while stack:
        directory, depth = stack.pop()
        if depth > MAX_WORKPLAN_DEPTH:
            continue
        try:
            children = sorted(directory.iterdir())
        except OSError:
            continue
        for child in children:
            if child.is_symlink():
                # A symlink may point outside the repository; resolving and
                # re-checking containment is cheaper than trusting it.
                try:
                    target = child.resolve(strict=True)
                except OSError:
                    continue
                if not target.is_relative_to(base):
                    continue
            if child.is_dir():
                stack.append((child, depth + 1))
                continue
            if not child.is_file():
                continue
            if child.suffix.lower() not in WORKPLAN_SUFFIXES:
                continue
            seen += 1
            if seen > MAX_WORKPLAN_FILES:
                E.fail(
                    E.CONFIG_INVALID,
                    "the workplan tree contains more files than the supported bound",
                    details={"limit": MAX_WORKPLAN_FILES},
                )
            yield child


def _lifecycle_consistent(state: LifecycleState, status: str | None) -> bool:
    if status is None:
        return True
    normalized = str(status).strip().lower()
    if state is LifecycleState.ACTIVE:
        return normalized in _ACTIVE_STATUSES
    return normalized in _ARCHIVE_STATUSES


def build_catalog(repo_root: Path) -> tuple[CatalogEntry, ...]:
    """Catalog every bounded repository-owned workplan document."""

    base = repo_root.resolve()
    raw_entries: list[dict[str, Any]] = []
    for relative_root, state in WORKPLAN_ROOTS:
        root = base / relative_root
        if not root.is_dir():
            continue
        for path in _iter_files(root, base):
            resolved = path.resolve()
            if not resolved.is_relative_to(base):
                continue
            metadata, body, raw, diagnostics = _read_document(path)
            declared_id = isinstance(metadata.get("workplan_id"), str) and bool(
                metadata["workplan_id"]
            )
            relative = str(path.relative_to(base)).replace("\\", "/")
            raw_entries.append(
                {
                    "path": relative,
                    "abs": path,
                    "state": state,
                    "metadata": metadata,
                    "body": body,
                    "raw": raw,
                    "diagnostics": list(diagnostics),
                    "declared_id": declared_id,
                    "workplan_id": (
                        str(metadata["workplan_id"]) if declared_id else path.stem
                    ),
                }
            )

    _mark_supersession(raw_entries)

    catalog: list[CatalogEntry] = []
    for entry in raw_entries:
        metadata = entry["metadata"]
        status = metadata.get("status")
        status_text = str(status) if status is not None else None
        superseded = entry.get("superseded_by")
        consistent = True if superseded else _lifecycle_consistent(entry["state"], status_text)
        if not consistent:
            entry["diagnostics"].append(
                f"declared status {status_text!r} is inconsistent with the {entry['state'].value} lifecycle directory"
            )
        protocol_version = metadata.get("protocol_version")
        ref = WorkplanRef(
            workplan_id=entry["workplan_id"],
            protocol_version=str(protocol_version) if protocol_version is not None else None,
            path=entry["path"],
            artifact_digest=digest_bytes(entry["raw"], SCHEME_WORKPLAN_ARTIFACT),
            semantic_digest=_semantic_digest(metadata, entry["body"]) if metadata else None,
            semantic_identity_complete=bool(metadata) and entry["declared_id"],
            lifecycle_state=entry["state"],
            lifecycle_consistent=consistent,
            declared_status=status_text,
        )
        target_branch = metadata.get("target_branch")
        catalog.append(
            CatalogEntry(
                descriptor=WorkplanDescriptor(
                    ref=ref,
                    kind=str(metadata["kind"]) if isinstance(metadata.get("kind"), str) else None,
                    target_branch=str(target_branch) if isinstance(target_branch, str) else None,
                    is_current_authority=bool(entry.get("is_current_authority", True)),
                    superseded_by=entry.get("superseded_by"),
                    diagnostics=tuple(entry["diagnostics"]),
                ),
                relative_path=entry["path"],
                declared_id=entry["declared_id"],
            )
        )
    return tuple(sorted(catalog, key=lambda item: item.relative_path))


def _mark_supersession(entries: list[dict[str, Any]]) -> None:
    """Resolve current authority within each declared ``workplan_id`` group."""

    by_path = {entry["path"]: entry for entry in entries}
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        if entry["declared_id"]:
            groups.setdefault(entry["workplan_id"], []).append(entry)

    for group in groups.values():
        if len(group) == 1:
            group[0]["is_current_authority"] = True
            continue
        by_revision: dict[Any, dict[str, Any]] = {}
        for member in group:
            revision = member["metadata"].get("revision")
            if revision is not None:
                by_revision.setdefault(revision, member)
        superseded: dict[str, str] = {}
        for member in group:
            parent = member["metadata"].get("parent_workplan")
            if isinstance(parent, str):
                candidate = (Path(member["path"]).parent / parent).as_posix()
                normalized = _normalize_relative(candidate)
                target = by_path.get(normalized)
                if target is not None and target in group:
                    superseded[target["path"]] = member["path"]
            replaced = member["metadata"].get("supersedes_revision")
            if replaced is not None and replaced in by_revision:
                target = by_revision[replaced]
                if target is not member:
                    superseded[target["path"]] = member["path"]
        remaining = [member for member in group if member["path"] not in superseded]
        for member in group:
            member["superseded_by"] = superseded.get(member["path"])
        if len(remaining) == 1:
            for member in group:
                member["is_current_authority"] = member is remaining[0]
        else:
            for member in group:
                member["is_current_authority"] = False
                member["diagnostics"].append(
                    "current authority for this workplan_id cannot be determined from explicit evidence"
                )


def _normalize_relative(path_text: str) -> str:
    parts: list[str] = []
    for part in path_text.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


# --------------------------------------------------------------------------
# Stage-specific resolution -- the single public owner of plan selection
# --------------------------------------------------------------------------


def _lookup_exact(catalog: tuple[CatalogEntry, ...], selector: str) -> WorkplanRef:
    """Resolve an exact workplan ID or exact repository-relative path."""

    normalized_path = _normalize_relative(selector.replace("\\", "/"))
    by_path = [entry for entry in catalog if entry.relative_path == normalized_path]
    if len(by_path) == 1:
        return by_path[0].descriptor.ref

    by_id = [
        entry
        for entry in catalog
        if entry.declared_id and entry.descriptor.ref.workplan_id == selector
    ]
    if not by_id:
        E.fail(
            E.WORKPLAN_NOT_FOUND,
            "no workplan matches the supplied selector",
            details={"selector": selector},
            remediation="pass an exact workplan_id or an exact repository-relative path",
        )
    current = [entry for entry in by_id if entry.descriptor.is_current_authority]
    if len(current) == 1:
        return current[0].descriptor.ref
    if not current:
        E.fail(
            E.WORKPLAN_AMBIGUOUS,
            "the workplan_id has no single current authority",
            details={
                "selector": selector,
                "candidates": [entry.relative_path for entry in by_id],
            },
            remediation="select the intended document by exact repository-relative path",
        )
    E.fail(
        E.WORKPLAN_AMBIGUOUS,
        "the workplan_id resolves to multiple current-authority documents",
        details={"selector": selector, "candidates": [entry.relative_path for entry in current]},
    )


def _active_authorities(catalog: tuple[CatalogEntry, ...]) -> list[CatalogEntry]:
    return [
        entry
        for entry in catalog
        if entry.descriptor.ref.lifecycle_state is LifecycleState.ACTIVE
        and entry.descriptor.is_current_authority
        and entry.descriptor.superseded_by is None
    ]


def resolve(
    catalog: tuple[CatalogEntry, ...],
    *,
    stage: StageRef,
    policy: WorkplanPolicy,
    selector: str | None,
    branch: str | None,
) -> WorkplanResolution:
    """Apply the stage's workplan policy to the catalog.

    A stage that disallows a workplan *fails* on an explicit selector rather than
    ignoring it: silently dropping user intent is how a prompt ends up governed by
    an authority the user never chose.
    """

    considered = tuple(entry.relative_path for entry in _active_authorities(catalog))

    if policy is WorkplanPolicy.DISALLOWED:
        if selector:
            E.fail(
                E.WORKPLAN_DISALLOWED,
                f"stage {stage.stage_key!r} does not select a governing workplan",
                details={"selector": selector, "stage": stage.stage_key},
            )
        return WorkplanResolution(
            stage=stage,
            policy=policy,
            workplan=None,
            selection_basis="stage_disallows_workplan",
            considered=(),
        )

    if selector:
        return WorkplanResolution(
            stage=stage,
            policy=policy,
            workplan=_lookup_exact(catalog, selector),
            selection_basis="explicit_selector",
            considered=considered,
        )

    if policy is WorkplanPolicy.EXPLICIT_REQUIRED:
        E.fail(
            E.WORKPLAN_REQUIRED,
            f"stage {stage.stage_key!r} requires an exact workplan selector",
            details={"stage": stage.stage_key},
            remediation="pass --workplan <workplan_id-or-path>",
        )

    if policy is WorkplanPolicy.EXPLICIT_ONLY:
        # Explicit-only stages never capture an unrelated sole active plan.
        return WorkplanResolution(
            stage=stage,
            policy=policy,
            workplan=None,
            selection_basis="no_explicit_authority_supplied",
            considered=considered,
        )

    active = _active_authorities(catalog)
    if branch:
        bound = [entry for entry in active if entry.descriptor.target_branch == branch]
        if len(bound) == 1:
            return WorkplanResolution(
                stage=stage,
                policy=policy,
                workplan=bound[0].descriptor.ref,
                selection_basis="current_branch_target_branch_binding",
                considered=considered,
            )
        if len(bound) > 1:
            E.fail(
                E.WORKPLAN_AMBIGUOUS,
                "multiple active workplans declare the current branch as target_branch",
                details={
                    "branch": branch,
                    "candidates": [entry.relative_path for entry in bound],
                },
                remediation="pass --workplan to select the governing plan explicitly",
            )

    if len(active) == 1:
        return WorkplanResolution(
            stage=stage,
            policy=policy,
            workplan=active[0].descriptor.ref,
            selection_basis="sole_active_workplan",
            considered=considered,
        )
    if not active:
        E.fail(
            E.WORKPLAN_NOT_FOUND,
            f"stage {stage.stage_key!r} requires a governing workplan but none is active",
            details={"stage": stage.stage_key},
            remediation="pass --workplan or add an active workplan",
        )
    E.fail(
        E.WORKPLAN_AMBIGUOUS,
        f"stage {stage.stage_key!r} requires a governing workplan and several are active",
        details={"stage": stage.stage_key, "candidates": list(considered)},
        remediation="pass --workplan <workplan_id-or-path>",
    )
