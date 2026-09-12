#!/usr/bin/env python3
"""Validate and render Protocol 6.3 Project Engineering Memory (PEM) schema 1.

Markdown remains the canonical project memory. This utility is deliberately a
small structural validator/derived-view renderer, not a database, authority
registry, history indexer, or background service.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

SCHEMA_VERSION = 1
FAMILY_KINDS = {"FAILURE_FAMILY", "SUCCESS_PATTERN", "DISCOVERY", "PRESERVATION_CAPABILITY"}
FAMILY_STATES = {"CURRENT", "REVIEW_REQUIRED", "STALE_OR_INAPPLICABLE", "RETIRED"}
MATURITIES = {"PROVISIONAL", "SUPPORTED", "PROVEN"}
TEMPERATURES = {"HOT", "WARM", "COLD", "UNASSESSED"}
AUTHORITY_BINDINGS = {"EVIDENCE_ONLY", "AUTHORITY_BOUND", "PROPOSED_FOR_PROMOTION"}
ASSESSMENT_STATES = {
    "ADMISSIBLE", "REVIEW_REQUIRED", "INCONCLUSIVE", "CHALLENGED",
    "REJECTED_OR_INVALID", "STALE_OR_INAPPLICABLE", "RETIRED",
}
APPLICATION_OUTCOMES = {"SUPPORTING", "NEUTRAL", "CONTRADICTING", "INCONCLUSIVE"}
GUIDANCE_LEVELS = {"OBSERVED", "RECOMMENDED", "PREFERRED", "DEFAULT", "BEST", "BETTER"}
COMPARATIVE_GUIDANCE = {"PREFERRED", "DEFAULT", "BEST", "BETTER"}
BINDING_HEALTH = {"HEALTHY", "REVIEW_REQUIRED", "UNAVAILABLE", "RETIRED"}
BINDING_SEVERITY = {"HEALTHY": 0, "REVIEW_REQUIRED": 1, "UNAVAILABLE": 2, "RETIRED": 3}
LINEAGE_RELATIONS = {"SUPERSEDES", "SPLIT_FROM", "MERGED_FROM", "REPLACES"}
RELATION_TYPES = LINEAGE_RELATIONS | {
    "LED_TO", "NARROWS", "GENERALIZES", "SUPPORTS_LEARNING_FROM", "CONFLICTS_WITH",
}
HAS_DISPOSITIONS = {"APPLICABLE", "NOT_APPLICABLE", "REVIEW_REQUIRED"}
HAS_BASIS_FIELDS = {"accepted_project_state", "accepted_pem", "candidate_overlay_semantic_candidate"}
TRIGGER_TYPES = {"deadline", "accepted_base_change", "owner_change", "binding_change", "manual_external"}
MATURITY_OBLIGATION_TYPES = {
    "claim_support", "applicability", "contradiction_resolution", "replication",
    "independent_replication", "comparator", "comparative_independence", "owner_priority",
}
ID_RE = re.compile(r"^(FF|SP|DS|PC)-[0-9]+$")
NOTICE_ID_RE = re.compile(r"^NT-[0-9]+$")
ROUTE_RE = re.compile(
    r"^(?P<source>[^@\s:]+(?:/[^@\s:]+)*)@(?P<revision>[^:\s]+):(?P<path>[^#\s]+)(?:#(?P<locator>.+))?$"
)
HEX_OBJECT_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")
FRONT_RE = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)
FAMILY_RE = re.compile(
    r"^###\s+(?P<heading_id>(?:FF|SP|DS|PC)-[0-9]+)\s+(?:—|-)\s+.*?\n"
    r"(?:(?!^###\s).)*?^```yaml pem-family\s*\n(?P<yaml>.*?)^```\s*$",
    re.MULTILINE | re.DOTALL,
)
NOTICE_RE = re.compile(
    r"^###\s+(?P<heading_id>NT-[0-9]+)\s+(?:—|-)\s+.*?\n"
    r"(?:(?!^###\s).)*?^```yaml pem-notice\s*\n(?P<yaml>.*?)^```\s*$",
    re.MULTILINE | re.DOTALL,
)
SUMMARY_RE = re.compile(
    r"(?P<start><!-- BEGIN DERIVED PEM SUMMARY -->\n)(?P<body>.*?)(?P<end><!-- END DERIVED PEM SUMMARY -->)",
    re.DOTALL,
)
REPAIR_ACCEPTANCE_RE = re.compile(
    r"^```yaml pem-repair-acceptance\s*\n(?P<yaml>.*?)^```\s*$",
    re.MULTILINE | re.DOTALL,
)


class PemError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class PemDocument:
    root: Path
    metadata: dict[str, Any]
    families: dict[str, dict[str, Any]]
    notices: dict[str, dict[str, Any]]
    sources: dict[str, Path]
    root_text: str


@dataclasses.dataclass(frozen=True)
class EvidenceRoute:
    raw: str
    source: str
    revision: str
    path: str
    locator: str | None = None


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PemError(f"{where} must be a mapping")
    return value


def _list(value: Any, where: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise PemError(f"{where} must be a list")
    return value


def _required_text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PemError(f"{where} must be non-empty text")
    return value.strip()


def _frontmatter(text: str, path: Path) -> dict[str, Any]:
    match = FRONT_RE.search(text)
    if not match:
        raise PemError(f"{path}: missing YAML front matter")
    try:
        data = yaml.safe_load(match.group("yaml")) or {}
    except yaml.YAMLError as exc:
        raise PemError(f"{path}: invalid front matter: {exc}") from exc
    return _mapping(data, f"{path}: front matter")


def _parse_blocks(text: str, path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    families: dict[str, dict[str, Any]] = {}
    notices: dict[str, dict[str, Any]] = {}
    for regex, target, label in ((FAMILY_RE, families, "family"), (NOTICE_RE, notices, "notice")):
        for match in regex.finditer(text):
            try:
                row = yaml.safe_load(match.group("yaml")) or {}
            except yaml.YAMLError as exc:
                raise PemError(f"{path}: invalid {label} YAML under {match.group('heading_id')}: {exc}") from exc
            row = _mapping(row, f"{path}:{match.group('heading_id')}")
            row_id = str(row.get("id", ""))
            if row_id != match.group("heading_id"):
                raise PemError(f"{path}: heading ID {match.group('heading_id')} != record ID {row_id!r}")
            if row_id in target:
                raise PemError(f"{path}: duplicate {label} ID {row_id}")
            target[row_id] = row
    return families, notices


def _validate_source_project(row: dict[str, Any], where: str) -> str:
    source_project = _required_text(row.get("source_project"), f"{where}:source_project")
    if source_project.lower() in {"external", "remote", "other", "unknown", "non-local", "nonlocal"}:
        raise PemError(
            f"{where}: non-local source_project must be an unambiguous project/repository identity, not {source_project!r}"
        )
    return source_project


def parse_evidence_route(value: Any, where: str = "evidence") -> EvidenceRoute:
    raw = _required_text(value, where)
    match = ROUTE_RE.fullmatch(raw)
    if not match:
        raise PemError(
            f"{where}: evidence route must be SOURCE@IMMUTABLE_ID:path[#stable-locator], got {raw!r}"
        )
    source = match.group("source")
    if source.lower() in {"external", "remote", "other", "unknown", "non-local", "nonlocal"}:
        raise PemError(f"{where}: evidence source identity is ambiguous: {source!r}")
    path = match.group("path")
    if path.startswith(("/", "~")) or ".." in Path(path).parts:
        raise PemError(f"{where}: evidence path must be repository-relative: {path!r}")
    locator = match.group("locator")
    if locator is not None and not locator.strip():
        raise PemError(f"{where}: evidence locator must be non-empty when present")
    return EvidenceRoute(raw, source, match.group("revision"), path, locator.strip() if locator else None)


def _git_root(path: Path) -> Path | None:
    start = path if path.is_dir() else path.parent
    try:
        proc = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            check=False, capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return Path(proc.stdout.strip()).resolve()


def _git_ok(root: Path, *args: str) -> bool:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args], check=False, capture_output=True, text=True, timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def _git_text(root: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args], check=False, capture_output=True, text=True, timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def _accepted_project_commit(doc: PemDocument, where: str) -> tuple[Path, str]:
    raw: Any = doc.metadata.get("accepted_base")
    if isinstance(raw, dict):
        raw = raw.get("project_state") or raw.get("identity")
    commit = _git_commit_from_identity(raw)
    if not commit:
        raise PemError(
            f"{where}: authority-bearing validation requires accepted_base.project_state to expose an exact immutable project commit"
        )
    root = _git_root(doc.root)
    if root is None or not _git_ok(root, "cat-file", "-e", f"{commit}^{{commit}}"):
        raise PemError(f"{where}: accepted project state {commit!r} is not a resolvable local commit")
    return root, commit


def _validate_accepted_project_route(
    route: EvidenceRoute, doc: PemDocument, where: str, *, target_revision: str | None = None,
    require_same_path_content: bool = False,
) -> tuple[Path, str]:
    health, reason = evidence_route_health(route, doc)
    if health != "HEALTHY":
        raise PemError(f"{where}: route is not mechanically healthy: {health}: {reason}")
    if not _route_is_local(route, doc):
        raise PemError(f"{where}: no source-specific resolver can establish this non-local owner as accepted project authority")
    root = _git_root(doc.root)
    if root is None:
        raise PemError(f"{where}: local Git repository is unavailable for accepted-project binding")
    if target_revision is None:
        _, target = _accepted_project_commit(doc, where)
    else:
        target = target_revision
        if not _git_ok(root, "cat-file", "-e", f"{target}^{{commit}}"):
            raise PemError(f"{where}: binding target revision {target!r} is not a resolvable commit")
    if not _git_ok(root, "merge-base", "--is-ancestor", route.revision, target):
        raise PemError(f"{where}: route revision is not contained by the governing accepted project state")
    if require_same_path_content:
        cited_blob = _git_text(root, "rev-parse", f"{route.revision}:{route.path}")
        target_blob = _git_text(root, "rev-parse", f"{target}:{route.path}")
        if target_blob is None:
            raise PemError(f"{where}: owner path is absent from the governing accepted project state")
        if cited_blob != target_blob:
            raise PemError(f"{where}: owner content changed before the governing accepted project state; binding requires review/remap")
    return root, target


def _validate_owner_binding(
    value: Any, doc: PemDocument, where: str, *, target_revision: str | None = None
) -> EvidenceRoute:
    route = parse_evidence_route(value, where)
    _validate_accepted_project_route(
        route, doc, where, target_revision=target_revision, require_same_path_content=True
    )
    return route


def _validate_accepted_authority_evidence(values: Any, doc: PemDocument, where: str) -> list[EvidenceRoute]:
    raw_routes = _list(values, where)
    if not raw_routes:
        raise PemError(f"{where}: accepted authority requires at least one explicit accepted-state authority-evidence route")
    routes: list[EvidenceRoute] = []
    for raw in raw_routes:
        route = parse_evidence_route(raw, where)
        _validate_accepted_project_route(route, doc, where)
        routes.append(route)
    return routes


def _validate_repair_acceptance_artifact(
    root: Path, route: EvidenceRoute, repair_identity: str, where: str, doc: PemDocument
) -> None:
    text = _git_text(root, "show", f"{route.revision}:{route.path}")
    if text is None:
        raise PemError(f"{where}: recurrence acceptance artifact cannot be read from immutable route")
    records: list[dict[str, Any]] = []
    for match in REPAIR_ACCEPTANCE_RE.finditer(text):
        try:
            record = yaml.safe_load(match.group("yaml")) or {}
        except yaml.YAMLError as exc:
            raise PemError(f"{where}: invalid typed repair-acceptance YAML: {exc}") from exc
        records.append(_mapping(record, f"{where}:repair acceptance record"))
    if not records:
        raise PemError(f"{where}: recurrence acceptance route does not contain a typed pem-repair-acceptance record")
    matches = [record for record in records if record.get("repair_identity") == repair_identity]
    if len(matches) != 1:
        raise PemError(f"{where}: recurrence acceptance artifact must contain exactly one typed record for repair {repair_identity!r}")
    record = matches[0]
    if record.get("state") != "ACCEPTED":
        raise PemError(f"{where}: repair acceptance record for the claimed repair is not ACCEPTED")
    owner = _required_text(record.get("owner"), f"{where}:repair acceptance owner")
    _validate_owner_binding(owner, doc, f"{where}:repair acceptance owner", target_revision=route.revision)


def _validate_repair_acceptance_routes(
    routes: list[EvidenceRoute], doc: PemDocument, root: Path, repair_identity: str, where: str
) -> list[str]:
    _, accepted_project = _accepted_project_commit(doc, f"{where}:repair acceptance")
    revisions: list[str] = []
    for route in routes:
        health, reason = evidence_route_health(route, doc)
        if health != "HEALTHY":
            raise PemError(f"{where}: recurrence acceptance route is not resolvable: {health}: {reason}")
        if not _route_is_local(route, doc):
            raise PemError(f"{where}: recurrence acceptance must be established by a resolvable project-local immutable artifact")
        if not _git_ok(root, "merge-base", "--is-ancestor", route.revision, accepted_project):
            raise PemError(f"{where}: repair acceptance artifact is not contained by accepted project state")
        _validate_repair_acceptance_artifact(root, route, repair_identity, where, doc)
        revisions.append(route.revision)
    return revisions


def _route_is_local(route: EvidenceRoute, doc: PemDocument) -> bool:
    repository = str(doc.metadata.get("repository", "")).strip().lower()
    source = route.source.lower()
    if repository and source == repository:
        return True
    return source in {"local", "repo", "repository"}


def evidence_route_health(route: EvidenceRoute, doc: PemDocument) -> tuple[str, str]:
    """Realize an evidence binding at the route's owning source when possible.

    Local repository routes are HEALTHY only when a commit/tree-ish publication and exact path
    resolve. A blob cannot masquerade as a publication revision. Non-local routes are never
    promoted to HEALTHY from syntax alone; absent a source-specific resolver in this validator
    they remain REVIEW_REQUIRED for an external/event-driven assessment.
    """
    if not _route_is_local(route, doc):
        return "REVIEW_REQUIRED", "non-local route has explicit source identity but no route-specific external realization"
    root = _git_root(doc.root)
    if root is None:
        return "REVIEW_REQUIRED", "local Git repository is unavailable for route realization"
    if not _git_ok(root, "cat-file", "-e", f"{route.revision}^{{commit}}"):
        if _git_ok(root, "cat-file", "-e", f"{route.revision}^{{blob}}"):
            return "UNAVAILABLE", "revision is a blob object, not a repository publication commit"
        return "UNAVAILABLE", "repository revision is not resolvable as a commit"
    if not _git_ok(root, "cat-file", "-e", f"{route.revision}:{route.path}"):
        return "UNAVAILABLE", "declared path is absent from the immutable repository revision"
    if route.locator:
        text = _git_text(root, "show", f"{route.revision}:{route.path}")
        if text is None:
            return "UNAVAILABLE", "declared path cannot be read for stable-locator realization"
        locator = route.locator.strip()
        if locator not in text:
            normalized = re.sub(r"[-_]+", " ", locator).strip().lower()
            normalized_text = re.sub(r"[-_]+", " ", text).lower()
            if normalized and normalized in normalized_text:
                return "HEALTHY", "commit, repository path, and normalized stable locator resolve"
            if re.fullmatch(r"[A-Za-z0-9_.:/ -]+", locator):
                return "UNAVAILABLE", "declared stable locator is absent from the immutable repository file"
            return "REVIEW_REQUIRED", "stable locator syntax is not mechanically interpretable by schema-1 text-anchor realization"
        return "HEALTHY", "commit, repository path, and stable locator resolve"
    return "HEALTHY", "commit and repository path resolve"


def _safe_detail_path(root: Path, raw: Any) -> tuple[Path, str | None]:
    expected_digest: str | None = None
    if isinstance(raw, dict):
        item = _mapping(raw, "detail_files entry")
        raw_path = item.get("path")
        expected_digest = _required_text(item.get("sha256"), "detail_files entry sha256")
        if not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
            raise PemError(f"detail_files entry sha256 must be a lowercase 64-hex digest: {expected_digest!r}")
    else:
        raw_path = raw
    if not isinstance(raw_path, str) or not raw_path or raw_path.startswith(("/", "~")):
        raise PemError(f"invalid detail_files entry: {raw!r}")
    candidate = (root.parent / raw_path).resolve()
    base = root.parent.resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise PemError(f"detail file escapes project memory root: {raw_path}") from exc
    if candidate.suffix.lower() != ".md":
        raise PemError(f"detail file must be Markdown: {raw_path}")
    return candidate, expected_digest


def _same_basis(a: Any, b: Any) -> bool:
    return yaml.safe_dump(a, sort_keys=True) == yaml.safe_dump(b, sort_keys=True)


def load_memory(root: Path | str) -> PemDocument:
    root = Path(root).resolve()
    text = root.read_text(encoding="utf-8")
    metadata = _frontmatter(text, root)
    if metadata.get("memory_schema_version") != SCHEMA_VERSION:
        raise PemError(
            f"{root}: unsupported memory_schema_version {metadata.get('memory_schema_version')!r}; supported={SCHEMA_VERSION}"
        )
    required_meta = {
        "maintained_under_protocol", "project_id", "repository", "scope", "coverage_state",
        "coverage_basis", "reconciled_through", "accepted_base", "candidate_overlay",
    }
    missing = sorted(k for k in required_meta if metadata.get(k) in (None, "", []))
    if missing:
        raise PemError(f"{root}: missing required metadata: {', '.join(missing)}")
    if metadata["coverage_state"] not in {"UNINITIALIZED", "PARTIAL", "RECONCILED_FOR_DECLARED_SCOPE"}:
        raise PemError(f"{root}: invalid coverage_state {metadata['coverage_state']!r}")

    families, notices = _parse_blocks(text, root)
    sources: dict[str, Path] = {**{k: root for k in families}, **{k: root for k in notices}}
    details = _list(metadata.get("detail_files", []), f"{root}:detail_files")
    for raw in details:
        detail, expected_digest = _safe_detail_path(root, raw)
        if not detail.is_file():
            raise PemError(f"declared detail file is missing: {raw!r}")
        detail_bytes = detail.read_bytes()
        if expected_digest is not None:
            actual_digest = hashlib.sha256(detail_bytes).hexdigest()
            if actual_digest != expected_digest:
                raise PemError(
                    f"{detail}: partition digest mismatch; expected {expected_digest}, observed {actual_digest}"
                )
        detail_text = detail_bytes.decode("utf-8")
        detail_meta = _frontmatter(detail_text, detail)
        if detail_meta.get("memory_schema_version") != SCHEMA_VERSION or detail_meta.get("pem_partition") is not True:
            raise PemError(f"{detail}: invalid PEM partition metadata")
        for key in ("project_id", "repository", "scope", "accepted_base", "candidate_overlay"):
            if not _same_basis(detail_meta.get(key), metadata.get(key)):
                raise PemError(f"{detail}: {key} differs from root publication basis")
        if SUMMARY_RE.search(detail_text):
            raise PemError(f"{detail}: only the PEM root may own the active summary")
        part_families, part_notices = _parse_blocks(detail_text, detail)
        for row_id in {**part_families, **part_notices}:
            if row_id in sources:
                raise PemError(f"duplicate canonical PEM ID {row_id} in {sources[row_id]} and {detail}")
            sources[row_id] = detail
        if expected_digest is None:
            raise PemError(
                f"{root}: partitioned schema-1 memory requires root-declared immutable sha256 for {detail.name}"
            )
        families.update(part_families)
        notices.update(part_notices)
    return PemDocument(root, metadata, families, notices, sources, text)


def _current_assessment(row: dict[str, Any], where: str) -> dict[str, Any] | None:
    assessments = _list(row.get("assessments", []), f"{where}:assessments")
    if not assessments:
        return None
    parsed: dict[str, dict[str, Any]] = {}
    for raw in assessments:
        item = _mapping(raw, f"{where}:assessment")
        aid = str(item.get("id", ""))
        if not aid or aid in parsed:
            raise PemError(f"{where}: assessment IDs must be non-empty and unique")
        if item.get("state") not in ASSESSMENT_STATES:
            raise PemError(f"{where}:{aid}: invalid assessment state {item.get('state')!r}")
        _required_text(item.get("conclusion"), f"{where}:{aid}:conclusion")
        evidence = _list(item.get("evidence"), f"{where}:{aid}:evidence")
        if not evidence:
            raise PemError(f"{where}:{aid}: assessment requires non-empty evidence route(s)")
        for route in evidence:
            parse_evidence_route(route, f"{where}:{aid}:evidence route")
        parsed[aid] = item
    graph: dict[str, set[str]] = {aid: set() for aid in parsed}
    superseded: set[str] = set()
    for aid, item in parsed.items():
        for raw_target in _list(item.get("supersedes", []), f"{where}:{aid}:supersedes"):
            target = _required_text(raw_target, f"{where}:{aid}:supersedes target")
            if target == aid:
                raise PemError(f"{where}:{aid}: assessment cannot supersede itself")
            if target not in parsed:
                raise PemError(f"{where}:{aid}: supersedes unknown assessment {target!r}")
            graph[aid].add(target)
            superseded.add(target)
    visiting: set[str] = set()
    done: set[str] = set()
    def visit(aid: str) -> None:
        if aid in done:
            return
        if aid in visiting:
            raise PemError(f"{where}: assessment supersession cycle includes {aid}")
        visiting.add(aid)
        for target in graph[aid]:
            visit(target)
        visiting.remove(aid)
        done.add(aid)
    for aid in graph:
        visit(aid)
    live = [item for aid, item in parsed.items() if aid not in superseded]
    if not live:
        raise PemError(f"{where}: assessment supersession leaves no current assessment")
    signatures = {(str(item.get("state")), str(item.get("conclusion"))) for item in live}
    if len(signatures) != 1:
        raise PemError(
            f"{where}: conflicting live assessments require explicit adjudication/supersession; serialized order, reviewer count, or latest-editor position cannot select current truth"
        )
    return live[0]


def _require_observation(row: dict[str, Any], where: str) -> None:
    current = _current_assessment(row, where)
    if current and current.get("state") == "ADMISSIBLE":
        _required_text(row.get("observation"), f"{where}:observation")


def _git_commit_from_identity(value: Any) -> str | None:
    text = str(value or "").strip()
    if text.startswith("commit:"):
        text = text.split(":", 1)[1]
    elif "@" in text:
        text = text.rsplit("@", 1)[1]
    return text if HEX_OBJECT_RE.fullmatch(text) else None


def _git_patch_id(root: Path, commit: str) -> str | None:
    try:
        show = subprocess.run(
            ["git", "-C", str(root), "show", "--pretty=format:", "--no-ext-diff", commit],
            check=False, capture_output=True, timeout=8,
        )
        if show.returncode != 0 or not show.stdout:
            return None
        patch = subprocess.run(
            ["git", "patch-id", "--stable"], input=show.stdout,
            check=False, capture_output=True, timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if patch.returncode != 0 or not patch.stdout.strip():
        return None
    return patch.stdout.decode("utf-8", errors="replace").split()[0]


def _validate_recurrence_structure(
    row: dict[str, Any], where: str, occurrence_ids: set[str], event_identity: str,
    *, prior_events: dict[str, str] | None = None, doc: PemDocument | None = None,
) -> bool:
    if row.get("recurrence_after_accepted_repair") is not True:
        return False
    basis = row.get("recurrence_basis")
    if not isinstance(basis, dict):
        raise PemError(f"{where}: recurrence requires prior_accepted_repair structured recurrence_basis")
    prior_id = _required_text(basis.get("prior_occurrence_id"), f"{where}:recurrence_basis:prior_occurrence_id")
    if prior_id not in occurrence_ids:
        raise PemError(f"{where}: recurrence prior occurrence {prior_id!r} must precede the current occurrence")
    repair_identity = _required_text(basis.get("repair_identity"), f"{where}:recurrence_basis:repair_identity")
    evidence = _list(basis.get("repair_acceptance_evidence"), f"{where}:recurrence_basis:repair_acceptance_evidence")
    if not evidence:
        raise PemError(f"{where}: recurrence requires actual repair-acceptance evidence")
    parsed_evidence = [parse_evidence_route(route, f"{where}:recurrence_basis:repair_acceptance_evidence") for route in evidence]
    later = _required_text(basis.get("later_event_identity"), f"{where}:recurrence_basis:later_event_identity")
    if later != event_identity:
        raise PemError(f"{where}: recurrence later_event_identity must equal the current independent event identity")
    _required_text(basis.get("independence_basis"), f"{where}:recurrence_basis:independence_basis")
    if basis.get("alias_of"):
        raise PemError(f"{where}: copied/rebased/cherry-picked alias cannot count as recurrence")

    prior_event = (prior_events or {}).get(prior_id)
    prior_commit = _git_commit_from_identity(prior_event)
    repair_commit = _git_commit_from_identity(repair_identity)
    later_commit = _git_commit_from_identity(later)
    if prior_commit and repair_commit and later_commit:
        if doc is None:
            raise PemError(f"{where}: Git-native recurrence requires repository context for accepted-repair chronology")
        root = _git_root(doc.root)
        if root is None:
            raise PemError(f"{where}: Git-native recurrence cannot resolve repository chronology")
        for label, commit in (("prior occurrence", prior_commit), ("repair", repair_commit), ("later event", later_commit)):
            if not _git_ok(root, "cat-file", "-e", f"{commit}^{{commit}}"):
                raise PemError(f"{where}: recurrence {label} identity is not a resolvable commit")
        acceptance_commits = _validate_repair_acceptance_routes(
            parsed_evidence, doc, root, repair_identity, where
        )
        if not _git_ok(root, "merge-base", "--is-ancestor", prior_commit, repair_commit):
            raise PemError(f"{where}: prior occurrence does not precede the claimed repair in project lineage")
        for accepted in acceptance_commits:
            if not _git_ok(root, "merge-base", "--is-ancestor", repair_commit, accepted):
                raise PemError(f"{where}: repair acceptance evidence does not contain/follow the claimed repair")
            if not _git_ok(root, "merge-base", "--is-ancestor", accepted, later_commit):
                raise PemError(f"{where}: accepted repair does not precede the later recurrence event")
        if prior_commit == later_commit or repair_commit == later_commit:
            raise PemError(f"{where}: same event/repair identity cannot count as independent recurrence")
        later_patch = _git_patch_id(root, later_commit)
        for earlier in (prior_commit, repair_commit):
            earlier_patch = _git_patch_id(root, earlier)
            if later_patch and earlier_patch and later_patch == earlier_patch:
                raise PemError(f"{where}: copied/rebased/cherry-picked patch-equivalent event cannot count as recurrence")
        return True

    if doc is None:
        raise PemError(f"{where}: non-Git recurrence requires document context to realize repair acceptance")
    root = _git_root(doc.root)
    if root is None:
        raise PemError(f"{where}: non-Git recurrence cannot realize durable repair-acceptance evidence")
    _validate_repair_acceptance_routes(parsed_evidence, doc, root, repair_identity, where)

    chronology = basis.get("chronology_assessment")
    if not isinstance(chronology, dict) or chronology.get("state") != "VERIFIED":
        raise PemError(
            f"{where}: non-Git recurrence requires explicit durable VERIFIED chronology_assessment; unresolved/self-attesting order cannot increment recurrence"
        )
    chronology_evidence = _list(chronology.get("evidence"), f"{where}:recurrence_basis:chronology_assessment:evidence")
    if not chronology_evidence:
        raise PemError(f"{where}: non-Git recurrence chronology assessment requires durable evidence")
    for raw in chronology_evidence:
        route = parse_evidence_route(raw, f"{where}:recurrence_basis:chronology_assessment:evidence")
        health, reason = evidence_route_health(route, doc)
        if health != "HEALTHY":
            raise PemError(f"{where}: non-Git recurrence chronology evidence is not resolvable: {health}: {reason}")
    return True


def derived_counts(family: dict[str, Any], doc: PemDocument | None = None) -> dict[str, int]:
    family_id = str(family.get("id", "?"))
    kind = family.get("kind")
    if kind == "FAILURE_FAMILY":
        occurrences = _list(family.get("occurrences", []), f"{family_id}:occurrences")
        confirmed = recurrence = 0
        surfaces: set[str] = set()
        occurrence_ids: set[str] = set()
        episode_ids: set[str] = set()
        prior_events: dict[str, str] = {}
        for row in occurrences:
            row = _mapping(row, f"{family_id}:occurrence")
            oid = str(row.get("id", ""))
            episode = str(row.get("event_identity", ""))
            if not oid or oid in occurrence_ids:
                raise PemError(f"{family_id}: occurrence IDs must be non-empty and unique within the family")
            if not episode or episode in episode_ids:
                raise PemError(f"{family_id}: occurrence event identities must be non-empty and unique within the family")
            _required_text(row.get("lifecycle_context"), f"{family_id}:{oid}:lifecycle_context")
            _validate_source_project(row, f"{family_id}:{oid}")
            surfaces.update(str(v) for v in _list(row.get("surfaces", []), f"{family_id}:{oid}:surfaces"))
            current = _current_assessment(row, f"{family_id}:{oid}")
            cause_claim = str(row.get("cause_claim", "")).strip()
            cause_evidence = row.get("cause_evidence", [])
            if cause_claim:
                if not isinstance(cause_evidence, list) or not cause_evidence:
                    raise PemError(f"{family_id}:{oid}: mechanism-specific cause_claim requires discriminating cause_evidence")
                for raw in cause_evidence:
                    parse_evidence_route(raw, f"{family_id}:{oid}:cause_evidence")
            if current and current.get("state") == "ADMISSIBLE" and current.get("conclusion") == "CONFIRMED":
                if _validate_recurrence_structure(
                    row, f"{family_id}:{oid}", occurrence_ids, episode,
                    prior_events=prior_events, doc=doc,
                ):
                    recurrence += 1
                confirmed += 1
            if current and current.get("state") == "ADMISSIBLE":
                _required_text(row.get("observation"), f"{family_id}:{oid}:observation")
            occurrence_ids.add(oid)
            episode_ids.add(episode)
            prior_events[oid] = episode
        return {"confirmed": confirmed, "affected_surfaces": len(surfaces), "recurrence": recurrence}
    if kind == "SUCCESS_PATTERN":
        applications = _list(family.get("applications", []), f"{family_id}:applications")
        counts = {"evaluated": len(applications), "supporting": 0, "neutral": 0, "contradicting": 0, "inconclusive": 0}
        surfaces: set[str] = set()
        application_ids: set[str] = set()
        episodes: set[str] = set()
        for row in applications:
            row = _mapping(row, f"{family_id}:application")
            aid = str(row.get("id", ""))
            episode = str(row.get("episode_identity", ""))
            if not aid or aid in application_ids:
                raise PemError(f"{family_id}: application IDs must be non-empty and unique within the family")
            if not episode or episode in episodes:
                raise PemError(f"{family_id}: application episode identities must be non-empty and unique within the family")
            application_ids.add(aid)
            episodes.add(episode)
            _required_text(row.get("lifecycle_context"), f"{family_id}:{aid}:lifecycle_context")
            _validate_source_project(row, f"{family_id}:{aid}")
            _required_text(row.get("provenance_cluster"), f"{family_id}:{aid}:provenance_cluster")
            surfaces.update(str(v) for v in _list(row.get("surfaces", []), f"{family_id}:{aid}:surfaces"))
            outcome = row.get("outcome")
            if outcome not in APPLICATION_OUTCOMES:
                raise PemError(f"{family_id}:{aid}: invalid outcome {outcome!r}")
            _require_observation(row, f"{family_id}:{aid}")
            current = _current_assessment(row, f"{family_id}:{aid}")
            if current and current.get("state") == "ADMISSIBLE":
                counts[outcome.lower()] += 1
        counts["affected_surfaces"] = len(surfaces)
        return counts
    evidence = _list(family.get("evidence", []), f"{family_id}:evidence")
    for route in evidence:
        parse_evidence_route(route, f"{family_id}:evidence route")
    return {"evidence": len(evidence)}


def base_temperature(family: dict[str, Any], counts: dict[str, int]) -> str:
    coverage = family.get("coverage_state")
    if family.get("kind") == "FAILURE_FAMILY":
        n = counts.get("confirmed", 0)
    elif family.get("kind") == "SUCCESS_PATTERN":
        n = counts.get("supporting", 0)
    else:
        return "UNASSESSED"
    if n >= 3:
        return "HOT"
    if n == 2:
        return "WARM"
    if n == 1:
        return "COLD" if coverage == "RECONCILED_FOR_DECLARED_SCOPE" else "UNASSESSED"
    return "UNASSESSED"


def _supporting_clusters(family: dict[str, Any]) -> set[str]:
    clusters: set[str] = set()
    for raw in _list(family.get("applications", []), f"{family.get('id', '?')}:applications"):
        row = _mapping(raw, f"{family.get('id', '?')}:application")
        current = _current_assessment(row, f"{family.get('id', '?')}:{row.get('id', '?')}")
        if current and current.get("state") == "ADMISSIBLE" and row.get("outcome") == "SUPPORTING":
            cluster = str(row.get("provenance_cluster", "")).strip()
            if cluster and cluster != "NONE":
                clusters.add(cluster)
    return clusters


def _required_maturity_obligations(family: dict[str, Any], basis: dict[str, Any]) -> set[str]:
    required = {"claim_support", "applicability", "contradiction_resolution"}
    if family.get("kind") == "SUCCESS_PATTERN":
        required.update({"replication", "independent_replication"})
    else:
        if basis.get("requires_replication"):
            required.add("replication")
        if basis.get("requires_independence") or family.get("provenance_independence_required"):
            required.add("independent_replication")
    if family.get("guidance_level") in COMPARATIVE_GUIDANCE:
        required.add("comparator")
        if not family.get("comparative_authority"):
            required.add("comparative_independence")
        else:
            required.add("owner_priority")
    return required


def _validate_maturity_basis(family: dict[str, Any], errors: list[str]) -> None:
    fid = str(family.get("id", ""))
    if family.get("maturity") != "PROVEN":
        return
    basis = family.get("maturity_basis")
    if not isinstance(basis, dict):
        errors.append(f"{fid}: PROVEN requires claim-relative structured maturity_basis")
        return
    claim = basis.get("claim")
    obligations = basis.get("obligations")
    if not isinstance(claim, str) or not claim.strip() or not isinstance(obligations, list) or not obligations:
        errors.append(f"{fid}: PROVEN requires claim-relative maturity_basis with explicit evidence obligations")
        return
    clusters = _supporting_clusters(family) if family.get("kind") == "SUCCESS_PATTERN" else set()
    seen: set[str] = set()
    for raw in obligations:
        if not isinstance(raw, dict):
            errors.append(f"{fid}: maturity obligation must be a mapping")
            continue
        otype = str(raw.get("type", ""))
        if otype not in MATURITY_OBLIGATION_TYPES:
            errors.append(f"{fid}: unknown PROVEN maturity obligation type {otype or '<unnamed>'!r}")
            continue
        if otype in seen:
            errors.append(f"{fid}: duplicate PROVEN maturity obligation type {otype!r}")
        seen.add(otype)
        if raw.get("status") != "CLOSED":
            errors.append(f"{fid}: PROVEN obligation {otype} is not CLOSED")
        evidence = raw.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{fid}: PROVEN obligation {otype} lacks evidence")
        else:
            for route in evidence:
                try:
                    parse_evidence_route(route, f"{fid}:maturity obligation evidence")
                except PemError as exc:
                    errors.append(str(exc))
        if otype in {"independent_replication", "replication", "comparative_independence"}:
            minimum = raw.get("minimum_independent_clusters")
            if otype == "replication":
                minimum = raw.get("minimum_independent_clusters", 1)
                min_allowed = 1
            else:
                min_allowed = 2
            if not isinstance(minimum, int) or minimum < min_allowed:
                errors.append(f"{fid}: {otype} obligation must declare minimum_independent_clusters >= {min_allowed}")
            elif family.get("kind") == "SUCCESS_PATTERN" and len(clusters) < minimum:
                errors.append(
                    f"{fid}: independence-sensitive PROVEN claim has {len(clusters)} supporting provenance cluster(s), requires {minimum}"
                )
    missing = _required_maturity_obligations(family, basis) - seen
    if missing:
        errors.append(f"{fid}: PROVEN maturity_basis omits required typed obligation(s): {', '.join(sorted(missing))}")


def _validate_comparative_basis(family: dict[str, Any], errors: list[str], doc: PemDocument | None = None) -> None:
    fid = str(family.get("id", ""))
    if family.get("guidance_level") not in COMPARATIVE_GUIDANCE:
        return
    authority = family.get("comparative_authority")
    if authority is not None:
        if not isinstance(authority, dict):
            errors.append(f"{fid}: comparative_authority must be a structured current-owner basis")
            return
        if not authority.get("owner") or not authority.get("decision"):
            errors.append(f"{fid}: comparative_authority requires current owner and explicit decision/tradeoff")
        elif doc is None:
            errors.append(f"{fid}: comparative owner priority cannot be established without accepted project context")
        else:
            try:
                _validate_owner_binding(authority.get("owner"), doc, f"{fid}:comparative authority owner")
            except PemError as exc:
                errors.append(str(exc))
        evidence = authority.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{fid}: comparative_authority requires applicable evidence")
        elif doc is None:
            errors.append(f"{fid}: comparative owner decision evidence cannot be established without accepted project context")
        else:
            for raw in evidence:
                try:
                    route = parse_evidence_route(raw, f"{fid}:comparative authority evidence")
                    _validate_accepted_project_route(route, doc, f"{fid}:comparative authority evidence")
                except PemError as exc:
                    errors.append(str(exc))
        return
    basis = family.get("comparative_basis")
    if not isinstance(basis, dict) or not basis:
        errors.append(f"{fid}: comparative/default/best guidance requires typed comparative_basis or current-owner authority")
        return
    comparison_set = basis.get("comparison_set")
    comparator = basis.get("comparator")
    objective = basis.get("objective")
    constraints = basis.get("constraints")
    evidence = basis.get("evidence")
    provenance_state = basis.get("provenance_state")
    if not isinstance(comparison_set, list) or len({str(v).strip() for v in comparison_set if str(v).strip()}) < 2:
        errors.append(f"{fid}: comparative_basis requires a viable comparison_set with at least two distinct alternatives")
    if not isinstance(comparator, str) or not comparator.strip():
        errors.append(f"{fid}: comparative_basis requires comparator identity")
    if not isinstance(objective, str) or not objective.strip():
        errors.append(f"{fid}: comparative_basis requires governing objective")
    if not isinstance(constraints, list) or not constraints or not all(str(v).strip() for v in constraints):
        errors.append(f"{fid}: comparative_basis requires material constraints/tradeoff bounds")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{fid}: comparative_basis requires applicable comparative evidence")
    else:
        for route in evidence:
            try: parse_evidence_route(route, f"{fid}:comparative evidence")
            except PemError as exc: errors.append(str(exc))
    if provenance_state not in {"INDEPENDENT", "COMMON_MODE_ACCOUNTED"}:
        errors.append(f"{fid}: comparative_basis requires explicit provenance/independence state")
    minimum = basis.get("minimum_independent_clusters")
    if provenance_state == "INDEPENDENT":
        if not isinstance(minimum, int) or minimum < 2:
            errors.append(f"{fid}: independent comparative_basis requires minimum_independent_clusters >= 2")
        elif len(_supporting_clusters(family)) < minimum:
            errors.append(f"{fid}: comparative/default/best guidance lacks required independent provenance clusters")


def _material_routes(family: dict[str, Any]) -> list[str]:
    routes: list[str] = []
    routes.extend(str(v) for v in family.get("evidence", []) if isinstance(v, str))
    for bucket in ("occurrences", "applications"):
        for raw in family.get(bucket, []) if isinstance(family.get(bucket, []), list) else []:
            if not isinstance(raw, dict):
                continue
            for assessment in raw.get("assessments", []) if isinstance(raw.get("assessments", []), list) else []:
                if isinstance(assessment, dict):
                    routes.extend(str(v) for v in assessment.get("evidence", []) if isinstance(v, str))
            routes.extend(str(v) for v in raw.get("cause_evidence", []) if isinstance(v, str))
            recurrence = raw.get("recurrence_basis")
            if isinstance(recurrence, dict):
                routes.extend(str(v) for v in recurrence.get("repair_acceptance_evidence", []) if isinstance(v, str))
                chronology = recurrence.get("chronology_assessment")
                if isinstance(chronology, dict):
                    routes.extend(str(v) for v in chronology.get("evidence", []) if isinstance(v, str))
    maturity = family.get("maturity_basis")
    if isinstance(maturity, dict):
        for obligation in maturity.get("obligations", []) if isinstance(maturity.get("obligations", []), list) else []:
            if isinstance(obligation, dict):
                routes.extend(str(v) for v in obligation.get("evidence", []) if isinstance(v, str))
    comparative = family.get("comparative_basis")
    if isinstance(comparative, dict):
        routes.extend(str(v) for v in comparative.get("evidence", []) if isinstance(v, str))
    authority = family.get("comparative_authority")
    if isinstance(authority, dict):
        if isinstance(authority.get("owner"), str): routes.append(str(authority["owner"]))
        routes.extend(str(v) for v in authority.get("evidence", []) if isinstance(v, str))
    if isinstance(family.get("authority_owner"), str): routes.append(str(family["authority_owner"]))
    routes.extend(str(v) for v in family.get("authority_evidence", []) if isinstance(v, str))
    override = family.get("temperature_override")
    if isinstance(override, dict):
        routes.extend(str(v) for v in override.get("evidence", []) if isinstance(v, str))
    counterevidence = family.get("counterevidence_search")
    if isinstance(counterevidence, dict):
        routes.extend(str(v) for v in counterevidence.get("evidence", []) if isinstance(v, str))
    reconciliation = family.get("semantic_reconciliation")
    if isinstance(reconciliation, dict):
        routes.extend(str(v) for v in reconciliation.get("evidence", []) if isinstance(v, str))
    return routes


def _family_requires_binding_health(family: dict[str, Any]) -> bool:
    if family.get("state") != "CURRENT":
        return False
    return (
        family.get("maturity") in {"SUPPORTED", "PROVEN"}
        or family.get("positive_guidance_eligible") is True
        or family.get("guidance_level") in {"RECOMMENDED", *COMPARATIVE_GUIDANCE}
        or family.get("authority_binding") == "AUTHORITY_BOUND"
    )


def _validate_family(family: dict[str, Any], doc: PemDocument | None = None) -> list[str]:
    errors: list[str] = []
    fid = str(family.get("id", ""))
    prefix = fid.split("-", 1)[0] if "-" in fid else ""
    expected = {"FF": "FAILURE_FAMILY", "SP": "SUCCESS_PATTERN", "DS": "DISCOVERY", "PC": "PRESERVATION_CAPABILITY"}.get(prefix)
    if not ID_RE.fullmatch(fid): errors.append(f"{fid or '<missing>'}: invalid family ID")
    if family.get("kind") not in FAMILY_KINDS or family.get("kind") != expected: errors.append(f"{fid}: kind does not match ID namespace")
    if family.get("state") not in FAMILY_STATES: errors.append(f"{fid}: invalid state {family.get('state')!r}")
    if family.get("maturity") not in MATURITIES: errors.append(f"{fid}: invalid maturity {family.get('maturity')!r}")
    if family.get("temperature") not in TEMPERATURES: errors.append(f"{fid}: invalid temperature {family.get('temperature')!r}")
    if family.get("authority_binding") not in AUTHORITY_BINDINGS: errors.append(f"{fid}: invalid authority_binding {family.get('authority_binding')!r}")
    binding_health = family.get("binding_health")
    if binding_health is not None and binding_health not in BINDING_HEALTH: errors.append(f"{fid}: invalid binding_health {binding_health!r}")
    if _family_requires_binding_health(family) and binding_health is None:
        errors.append(f"{fid}: material current warrant requires explicit binding_health")
    for field in ("summary", "aggregation_scope", "coverage_state", "coverage_basis", "applicability"):
        if field not in family: errors.append(f"{fid}: missing {field}")
    identity = family.get("semantic_identity")
    if not isinstance(identity, dict) or any(not identity.get(k) for k in ("invariant_or_claim", "owner_class", "mechanism_family", "applicability_dimensions")):
        errors.append(f"{fid}: incomplete semantic_identity envelope")
    if family.get("coverage_state") not in {"UNINITIALIZED", "PARTIAL", "RECONCILED_FOR_DECLARED_SCOPE"}: errors.append(f"{fid}: invalid coverage_state")
    try:
        counts = derived_counts(family, doc=doc)
    except PemError as exc:
        errors.append(str(exc)); counts = {}
    base = base_temperature(family, counts)
    declared = family.get("temperature")
    if declared != base:
        override = family.get("temperature_override")
        if not isinstance(override, dict) or override.get("final") != declared or not override.get("reason"):
            errors.append(f"{fid}: temperature {declared!r} differs from derived base {base!r} without evidence-bound override")
        else:
            override_evidence = override.get("evidence")
            if not isinstance(override_evidence, list) or not override_evidence:
                errors.append(f"{fid}: temperature override requires non-empty evidence route(s)")
            else:
                for raw in override_evidence:
                    try:
                        parse_evidence_route(raw, f"{fid}:temperature override evidence")
                    except PemError as exc:
                        errors.append(str(exc))
    if family.get("maturity") == "SUPPORTED":
        if family.get("kind") == "FAILURE_FAMILY" and counts.get("confirmed", 0) < 1: errors.append(f"{fid}: SUPPORTED failure family has no admissible confirmed occurrence")
        elif family.get("kind") == "SUCCESS_PATTERN" and counts.get("supporting", 0) < 1: errors.append(f"{fid}: SUPPORTED success pattern has no admissible supporting application")
        elif family.get("kind") in {"DISCOVERY", "PRESERVATION_CAPABILITY"} and counts.get("evidence", 0) < 1: errors.append(f"{fid}: SUPPORTED finding requires evidence")
    if family.get("maturity") == "PROVEN":
        _validate_maturity_basis(family, errors)
        if family.get("state") != "CURRENT": errors.append(f"{fid}: non-current family cannot remain PROVEN current guidance")
        if family.get("kind") == "SUCCESS_PATTERN" and counts.get("contradicting", 0): errors.append(f"{fid}: PROVEN success pattern has unresolved admissible contradiction")
    guidance = family.get("guidance_level", "OBSERVED")
    if guidance not in GUIDANCE_LEVELS: errors.append(f"{fid}: invalid guidance_level {guidance!r}")
    if family.get("kind") == "SUCCESS_PATTERN":
        eligible = family.get("positive_guidance_eligible", False)
        if eligible:
            if family.get("state") != "CURRENT" or family.get("maturity") not in {"SUPPORTED", "PROVEN"}: errors.append(f"{fid}: positive guidance eligibility requires CURRENT SUPPORTED/PROVEN state")
            if counts.get("supporting", 0) < 1: errors.append(f"{fid}: positive guidance eligibility requires admissible supporting evidence")
            if counts.get("contradicting", 0): errors.append(f"{fid}: positive guidance eligibility hides admissible contradiction")
            if binding_health != "HEALTHY": errors.append(f"{fid}: positive guidance eligibility requires explicit HEALTHY binding_health")
            search = family.get("counterevidence_search")
            if not isinstance(search, dict):
                errors.append(f"{fid}: positive guidance eligibility requires structured bounded counterevidence_search")
            else:
                if search.get("state") != "COMPLETE_FOR_DECLARED_SCOPE":
                    errors.append(f"{fid}: positive guidance counterevidence_search is not complete for the declared scope")
                for key in ("scope", "search_basis", "blind_spots"):
                    if key not in search or search.get(key) in (None, ""):
                        errors.append(f"{fid}: counterevidence_search requires {key}")
                outcomes = search.get("outcomes_reviewed")
                required_outcomes = {"SUPPORTING", "NEUTRAL", "CONTRADICTING", "INCONCLUSIVE"}
                if not isinstance(outcomes, list) or not required_outcomes.issubset({str(v) for v in outcomes}):
                    errors.append(f"{fid}: counterevidence_search must review supporting, neutral, contradicting, and inconclusive outcomes")
                evidence = search.get("evidence")
                if not isinstance(evidence, list) or not evidence:
                    errors.append(f"{fid}: counterevidence_search requires durable evidence")
                else:
                    for raw in evidence:
                        try:
                            parse_evidence_route(raw, f"{fid}:counterevidence search evidence")
                        except PemError as exc:
                            errors.append(str(exc))
        if guidance in ({"RECOMMENDED"} | COMPARATIVE_GUIDANCE) and not eligible: errors.append(f"{fid}: positive recommendation is not eligible")
        _validate_comparative_basis(family, errors, doc=doc)
    elif guidance != "OBSERVED": errors.append(f"{fid}: only SUCCESS_PATTERN may carry positive guidance levels")
    if family.get("authority_binding") == "AUTHORITY_BOUND":
        if not family.get("authority_owner"):
            errors.append(f"{fid}: AUTHORITY_BOUND requires authority_owner")
        elif doc is None:
            errors.append(f"{fid}: AUTHORITY_BOUND owner cannot be established without accepted project context")
        else:
            try:
                _validate_owner_binding(family.get("authority_owner"), doc, f"{fid}:authority_owner")
                _validate_accepted_authority_evidence(family.get("authority_evidence"), doc, f"{fid}:authority_evidence")
            except PemError as exc:
                errors.append(str(exc))
        if family.get("state") == "CURRENT" and binding_health != "HEALTHY": errors.append(f"{fid}: CURRENT AUTHORITY_BOUND family requires explicit HEALTHY binding_health")
    relations = family.get("relations", [])
    if not isinstance(relations, list): errors.append(f"{fid}: relations must be a list")
    else:
        for relation in relations:
            if not isinstance(relation, dict) or relation.get("type") not in RELATION_TYPES or not relation.get("target"): errors.append(f"{fid}: invalid typed relation {relation!r}")
            elif str(relation.get("target")) == fid: errors.append(f"{fid}: relation cannot target its own canonical family ID")
    return errors


def _validate_lineage(doc: PemDocument) -> list[str]:
    errors: list[str] = []
    graph: dict[str, set[str]] = {fid: set() for fid in doc.families}
    for fid, family in doc.families.items():
        for relation in family.get("relations", []) if isinstance(family.get("relations", []), list) else []:
            target = relation.get("target") if isinstance(relation, dict) else None
            if target not in doc.families:
                errors.append(f"{fid}: relation target {target!r} has no canonical family record"); continue
            if relation.get("type") in LINEAGE_RELATIONS:
                graph[fid].add(str(target))
                if doc.families[str(target)].get("state") == "CURRENT": errors.append(f"{fid}: lineage target {target} cannot remain CURRENT while superseded/replaced/split/merged lineage is active")
            if relation.get("type") == "CONFLICTS_WITH":
                other = doc.families[str(target)]
                active = family.get("guidance_level") in ({"RECOMMENDED"} | COMPARATIVE_GUIDANCE)
                other_active = other.get("guidance_level") in ({"RECOMMENDED"} | COMPARATIVE_GUIDANCE)
                if active and other_active and family.get("state") == other.get("state") == "CURRENT":
                    if not family.get("decision_boundary") and not other.get("decision_boundary"): errors.append(f"{fid}: current conflicting guidance with {target} lacks decision boundary/tradeoff")
    visiting: set[str] = set(); done: set[str] = set()
    def visit(node: str) -> None:
        if node in done: return
        if node in visiting: errors.append(f"lineage cycle includes {node}"); return
        visiting.add(node)
        for target in graph[node]: visit(target)
        visiting.remove(node); done.add(node)
    for node in graph: visit(node)
    return errors


def _accepted_base_identity(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("pem_identity", "project_state", "identity"):
            if value.get(key): return str(value[key])
    return str(value)


def _notice_trigger_state(notice: dict[str, Any], doc: PemDocument, today: dt.date | None = None) -> tuple[str, str]:
    trigger = notice.get("review_trigger")
    if not isinstance(trigger, dict):
        return "INDETERMINATE", "opaque, legacy, or missing typed review trigger"
    ttype = trigger.get("type")
    if ttype not in TRIGGER_TYPES:
        return "INDETERMINATE", f"unsupported trigger type {ttype!r}"
    if ttype == "deadline":
        raw = trigger.get("at")
        try: deadline = dt.date.fromisoformat(str(raw))
        except ValueError: return "INDETERMINATE", "deadline trigger is not an ISO date"
        return ("FIRED", "deadline reached") if (today or dt.date.today()) >= deadline else ("CLEAR", "deadline not reached")
    if ttype == "accepted_base_change":
        basis = trigger.get("basis")
        if basis in (None, ""): return "INDETERMINATE", "accepted-base trigger lacks admitted basis"
        current = _accepted_base_identity(doc.metadata.get("accepted_base"))
        return ("FIRED", "accepted base changed") if str(basis) != current else ("CLEAR", "accepted base unchanged")
    if ttype == "binding_change":
        basis = trigger.get("basis"); current = notice.get("binding_health")
        if basis not in BINDING_HEALTH: return "INDETERMINATE", "binding trigger lacks valid admitted basis"
        return ("FIRED", "binding health changed") if basis != current else ("CLEAR", "binding health unchanged")
    if ttype == "owner_change":
        basis = trigger.get("basis"); current = notice.get("owner")
        if not basis or not current: return "INDETERMINATE", "owner trigger requires admitted basis and current resolved owner"
        return ("FIRED", "owner changed") if str(basis) != str(current) else ("CLEAR", "owner unchanged")
    state = trigger.get("assessed_state")
    evidence = trigger.get("assessed_evidence")
    if state not in {"CLEAR", "FIRED", "INDETERMINATE"} or not isinstance(evidence, list) or not evidence:
        return "INDETERMINATE", "manual/external trigger lacks explicit current assessment and evidence"
    try:
        for route in evidence: parse_evidence_route(route, "manual/external trigger assessed_evidence")
    except PemError as exc:
        return "INDETERMINATE", str(exc)
    return str(state), "explicit external/manual assessment"


def _validate_notices(doc: PemDocument) -> list[str]:
    errors: list[str] = []
    for nid, notice in doc.notices.items():
        if not NOTICE_ID_RE.fullmatch(nid): errors.append(f"{nid}: invalid notice ID")
        if notice.get("state") not in FAMILY_STATES: errors.append(f"{nid}: invalid state")
        if notice.get("binding_health") not in BINDING_HEALTH: errors.append(f"{nid}: invalid binding_health")
        for key in ("summary", "applicability", "normative_status"):
            if not notice.get(key): errors.append(f"{nid}: missing {key}")
        if not isinstance(notice.get("review_trigger"), dict): errors.append(f"{nid}: missing typed review_trigger; legacy review_or_expiry text is not an evaluable current trigger")
        evidence = notice.get("evidence")
        if not isinstance(evidence, list) or not evidence: errors.append(f"{nid}: evidence must contain at least one non-empty route")
        else:
            for route in evidence:
                try: parse_evidence_route(route, f"{nid}:evidence route")
                except PemError as exc: errors.append(str(exc))
        if notice.get("normative_status") != "NON_AUTHORITATIVE":
            if notice.get("owner") in (None, "", "NONE"):
                errors.append(f"{nid}: normative notice requires governing owner")
            else:
                try:
                    _validate_owner_binding(notice.get("owner"), doc, f"{nid}:normative owner")
                    _validate_accepted_authority_evidence(notice.get("evidence"), doc, f"{nid}:normative evidence")
                except PemError as exc:
                    errors.append(str(exc))
        if notice.get("state") == "CURRENT" and notice.get("binding_health") != "HEALTHY": errors.append(f"{nid}: unhealthy notice cannot remain unqualified CURRENT")
        trigger_state, reason = _notice_trigger_state(notice, doc)
        if notice.get("state") == "CURRENT" and trigger_state != "CLEAR": errors.append(f"{nid}: current notice trigger is {trigger_state}: {reason}; route to REVIEW_REQUIRED/RETIRED reconciliation")
    return errors


def _actual_route_health(
    routes: list[str], doc: PemDocument, where: str, errors: list[str]
) -> tuple[str, list[tuple[str, str, str]]]:
    worst = "HEALTHY"
    realized: list[tuple[str, str, str]] = []
    if not routes:
        return "REVIEW_REQUIRED", realized
    for raw in routes:
        try:
            route = parse_evidence_route(raw, f"{where}:material evidence")
        except PemError as exc:
            errors.append(str(exc)); worst = "UNAVAILABLE"; continue
        health, reason = evidence_route_health(route, doc)
        realized.append((raw, health, reason))
        if BINDING_SEVERITY[health] > BINDING_SEVERITY[worst]:
            worst = health
    return worst, realized


def _validate_binding_health(doc: PemDocument) -> list[str]:
    errors: list[str] = []
    for fid, family in doc.families.items():
        routes = _material_routes(family)
        actual, realized = _actual_route_health(routes, doc, fid, errors)
        declared = family.get("binding_health")
        if _family_requires_binding_health(family) and declared is None:
            errors.append(f"{fid}: material current warrant omits family-level binding_health; current support/guidance is REVIEW_REQUIRED")
            continue
        if declared in BINDING_HEALTH and BINDING_SEVERITY[declared] < BINDING_SEVERITY[actual]:
            for raw, health, reason in realized:
                if BINDING_SEVERITY[health] > BINDING_SEVERITY[declared]:
                    errors.append(f"{fid}: binding_health {declared} is false for {raw!r}: {health}: {reason}")
            if not realized:
                errors.append(f"{fid}: declared binding_health {declared} overstates realized route health {actual}")
    for nid, notice in doc.notices.items():
        routes = [str(v) for v in notice.get("evidence", []) if isinstance(v, str)]
        if notice.get("normative_status") != "NON_AUTHORITATIVE" and isinstance(notice.get("owner"), str):
            routes.append(str(notice["owner"]))
        trigger = notice.get("review_trigger")
        if isinstance(trigger, dict):
            routes.extend(str(v) for v in trigger.get("assessed_evidence", []) if isinstance(v, str))
        actual, realized = _actual_route_health(routes, doc, nid, errors)
        declared = notice.get("binding_health")
        if declared in BINDING_HEALTH and BINDING_SEVERITY[declared] < BINDING_SEVERITY[actual]:
            for raw, health, reason in realized:
                if BINDING_SEVERITY[health] > BINDING_SEVERITY[declared]:
                    errors.append(f"{nid}: binding_health {declared} is false for {raw!r}: {health}: {reason}")
            if not realized:
                errors.append(f"{nid}: declared binding_health {declared} overstates realized route health {actual}")
    return errors


def _salience_key(family: dict[str, Any]) -> tuple[int, int, str]:
    binding_health = family.get("binding_health")
    unresolved = 0 if family.get("state") == "REVIEW_REQUIRED" or binding_health in {"REVIEW_REQUIRED", "UNAVAILABLE"} else 1
    temp = {"HOT": 0, "WARM": 1, "COLD": 2, "UNASSESSED": 3}.get(str(family.get("temperature")), 4)
    return unresolved, temp, str(family.get("id"))


def _notice_is_unresolved(notice: dict[str, Any], doc: PemDocument) -> bool:
    if notice.get("state") == "REVIEW_REQUIRED" or notice.get("binding_health") in {"REVIEW_REQUIRED", "UNAVAILABLE"}:
        return True
    trigger_state, _ = _notice_trigger_state(notice, doc)
    return notice.get("state") == "CURRENT" and trigger_state != "CLEAR"


def render_summary(doc: PemDocument) -> str:
    rows: list[str] = []
    for family in sorted(doc.families.values(), key=_salience_key):
        if family.get("state") not in {"CURRENT", "REVIEW_REQUIRED"}: continue
        counts = derived_counts(family, doc=doc)
        if family.get("kind") == "FAILURE_FAMILY": count_text = f"{counts.get('confirmed', 0)} confirmed"
        elif family.get("kind") == "SUCCESS_PATTERN": count_text = f"{counts.get('supporting', 0)} supporting / {counts.get('neutral', 0)} neutral / {counts.get('contradicting', 0)} contradicting / {counts.get('inconclusive', 0)} inconclusive"
        else: count_text = f"{counts.get('evidence', 0)} evidence route(s)"
        guidance = family.get("guidance_level", "OBSERVED"); authority_binding = family.get("authority_binding", "EVIDENCE_ONLY"); health = family.get("binding_health")
        binding = f"{authority_binding}/{health}" if health else str(authority_binding)
        rows.append("| {id} | {kind} | {temp} | {maturity}/{state} | {binding} | {guidance} | {count} | {summary} |".format(
            id=family["id"], kind=family["kind"], temp=family["temperature"], maturity=family["maturity"], state=family["state"], binding=binding, guidance=guidance, count=count_text, summary=str(family["summary"]).replace("|", "\\|")))
    active_notices = [n for n in doc.notices.values() if n.get("state") in {"CURRENT", "REVIEW_REQUIRED"}]
    unresolved_notices = [n for n in active_notices if _notice_is_unresolved(n, doc)]
    resolved_notices = [n for n in active_notices if n not in unresolved_notices]
    def notice_rows(items: list[dict[str, Any]]) -> list[str]:
        return [f"- **{n['id']}** [{n['state']}/{n['binding_health']}]: {n['summary']}" for n in sorted(items, key=lambda n: str(n.get("id")))]
    parts: list[str] = []
    if unresolved_notices:
        parts.extend(["High-impact unresolved notices:", "", *notice_rows(unresolved_notices), ""])
    if rows: parts.extend(["| ID | Kind | Temperature | Maturity/state | Binding | Guidance | Current evidence | Bounded lesson |", "| --- | --- | --- | --- | --- | --- | --- | --- |", *rows])
    else: parts.append("_No current learning families._")
    if resolved_notices: parts.extend(["", "Current notices:", "", *notice_rows(resolved_notices)])
    return "\n".join(parts).rstrip() + "\n"


def _all_event_rows(doc: PemDocument) -> dict[str, tuple[str, str, dict[str, Any]]]:
    rows: dict[str, tuple[str, str, dict[str, Any]]] = {}
    for fid, family in doc.families.items():
        for bucket, identity_field in (("occurrences", "event_identity"), ("applications", "episode_identity")):
            for raw in family.get(bucket, []) if isinstance(family.get(bucket, []), list) else []:
                if isinstance(raw, dict) and raw.get("id") and raw.get(identity_field):
                    identity = str(raw[identity_field])
                    # Multiple families may cite one historical event, but reconciliation must compare each
                    # accepted identity rather than family/local-row position. Keep the first canonical row;
                    # duplicate current rows are separately visible as representation ambiguity.
                    if identity not in rows:
                        rows[identity] = (fid, str(raw["id"]), raw)
    return rows


def _validate_observation_correction(identity: str, old: tuple[str, str, dict[str, Any]], new: tuple[str, str, dict[str, Any]]) -> str | None:
    old_fid, old_rowid, old_row = old; new_fid, new_rowid, new_row = new
    old_obs = old_row.get("observation"); new_obs = new_row.get("observation")
    if old_obs == new_obs: return None
    correction = new_row.get("observation_correction")
    if not isinstance(correction, dict):
        return f"{new_fid}:{new_rowid}: accepted event/application {identity!r} observation changed across representation identity without clerical-correction provenance"
    old_hash = hashlib.sha256(str(old_obs).encode("utf-8")).hexdigest()
    evidence = correction.get("evidence")
    if (
        correction.get("previous_sha256") != old_hash
        or correction.get("previous_observation") != old_obs
        or correction.get("corrected_observation") != new_obs
        or not correction.get("reason")
        or not isinstance(evidence, list) or not evidence
    ):
        return f"{new_fid}:{new_rowid}: observation correction does not preserve previous/corrected record, previous hash, reason, and evidence"
    try:
        for route in evidence: parse_evidence_route(route, f"{new_fid}:{new_rowid}:observation correction evidence")
    except PemError as exc:
        return str(exc)
    return None


def validate_memory(doc: PemDocument, *, check_summary: bool = True) -> list[str]:
    errors: list[str] = []
    for family in doc.families.values(): errors.extend(_validate_family(family, doc=doc))
    errors.extend(_validate_lineage(doc)); errors.extend(_validate_notices(doc)); errors.extend(_validate_binding_health(doc))
    if check_summary:
        match = SUMMARY_RE.search(doc.root_text)
        if not match: errors.append("PEM root is missing derived active-summary markers")
        elif match.group("body") != render_summary(doc): errors.append("derived active summary is stale; run --write-summary")
    return errors


def _semantic_identity_signature(family: dict[str, Any]) -> str:
    payload = {"kind": family.get("kind"), "semantic_identity": family.get("semantic_identity"), "applicability": family.get("applicability")}
    return hashlib.sha256(yaml.safe_dump(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _normalized_semantic_text(value: Any) -> str:
    """Normalize presentation-only text differences without inferring semantic equivalence."""
    if isinstance(value, str):
        return re.sub(r"[\W_]+", " ", value, flags=re.UNICODE).strip().casefold()
    return yaml.safe_dump(value, sort_keys=True).strip().casefold()


def _normalized_applicability(value: Any) -> set[str] | None:
    if not isinstance(value, list):
        return None
    normalized = {_normalized_semantic_text(item) for item in value}
    normalized.discard("")
    return normalized


def validate_reconciliation(previous: PemDocument, current: PemDocument) -> list[str]:
    """Reject silent accepted semantic drift and observation rewriting across representations."""
    errors: list[str] = []
    for fid in previous.families.keys() & current.families.keys():
        old_family = previous.families[fid]; new_family = current.families[fid]
        old_sig = _semantic_identity_signature(old_family); new_sig = _semantic_identity_signature(new_family)
        if old_sig != new_sig:
            old_semantic = old_family.get("semantic_identity") if isinstance(old_family.get("semantic_identity"), dict) else {}
            new_semantic = new_family.get("semantic_identity") if isinstance(new_family.get("semantic_identity"), dict) else {}
            mechanically_material: list[str] = []
            if old_family.get("kind") != new_family.get("kind"):
                mechanically_material.append("kind")
            for key in ("owner_class", "mechanism_family"):
                if old_semantic.get(key) != new_semantic.get(key):
                    mechanically_material.append(key)
            if _normalized_semantic_text(old_semantic.get("invariant_or_claim")) != _normalized_semantic_text(new_semantic.get("invariant_or_claim")):
                mechanically_material.append("invariant_or_claim")
            if _normalized_semantic_text(old_semantic.get("applicability_dimensions")) != _normalized_semantic_text(new_semantic.get("applicability_dimensions")):
                mechanically_material.append("applicability_dimensions")
            old_app = _normalized_applicability(old_family.get("applicability"))
            new_app = _normalized_applicability(new_family.get("applicability"))
            if old_app is None or new_app is None or not new_app or not new_app.issubset(old_app):
                mechanically_material.append("applicability")
            if mechanically_material:
                errors.append(
                    f"{fid}: accepted family changed mechanically material semantic identity field(s) under the same ID: "
                    + ", ".join(mechanically_material)
                    + "; use a new/successor/reclassified identity with lineage"
                )
                continue
            record = new_family.get("semantic_reconciliation")
            if not isinstance(record, dict):
                errors.append(f"{fid}: accepted family semantic identity/applicability changed under the same ID without explicit reconciliation or lineage")
            else:
                evidence = record.get("evidence")
                if (record.get("classification") != "WITHIN_ENVELOPE" or record.get("previous_identity_sha256") != old_sig or not record.get("reason") or not isinstance(evidence, list) or not evidence):
                    errors.append(f"{fid}: same-ID semantic reconciliation must bind the previous envelope, WITHIN_ENVELOPE classification, reason, and evidence")
                else:
                    for raw in evidence:
                        try:
                            route = parse_evidence_route(raw, f"{fid}:semantic reconciliation evidence")
                            health, reason = evidence_route_health(route, current)
                            if health != "HEALTHY":
                                errors.append(f"{fid}: same-ID semantic reconciliation evidence is not mechanically healthy: {health}: {reason}")
                        except PemError as exc:
                            errors.append(str(exc))
    old_rows = _all_event_rows(previous); new_rows = _all_event_rows(current)
    for identity in old_rows.keys() & new_rows.keys():
        error = _validate_observation_correction(identity, old_rows[identity], new_rows[identity])
        if error: errors.append(error)
    return errors


def validate_has(
    record: dict[str, Any], *, accepted_project_state: str, accepted_pem: str,
    candidate_overlay_identity: str, accepted_ids: Iterable[str], current_accepted_project_state: str | None = None,
) -> list[str]:
    """Validate the one documented Historical Applicability Set (HAS) workflow/PEM seam."""
    errors: list[str] = []
    basis = record.get("pem_basis"); rows = record.get("has")
    if not isinstance(basis, dict): return ["HAS pem_basis must be a mapping"]
    extra = set(basis) - HAS_BASIS_FIELDS
    missing = HAS_BASIS_FIELDS - set(basis)
    if extra: errors.append(f"HAS pem_basis contains non-canonical field(s): {', '.join(sorted(extra))}")
    if missing: errors.append(f"HAS pem_basis omits canonical field(s): {', '.join(sorted(missing))}")
    expected = {"accepted_project_state": accepted_project_state, "accepted_pem": accepted_pem, "candidate_overlay_semantic_candidate": candidate_overlay_identity}
    for key, value in expected.items():
        if basis.get(key) != value: errors.append(f"HAS basis {key} does not match the exact workflow-selected identity")
    if candidate_overlay_identity in {accepted_project_state, accepted_pem}: errors.append("candidate overlay cannot self-ratify as the accepted project/memory basis")
    if current_accepted_project_state and current_accepted_project_state != accepted_project_state: errors.append("accepted project-memory basis advanced; HAS is REVIEW_REQUIRED until reconciled")
    if not isinstance(rows, list): return errors + ["HAS has must be a list"]
    seen: set[str] = set()
    for raw in rows:
        if not isinstance(raw, dict): errors.append("HAS row must be a mapping"); continue
        item_id = str(raw.get("id", ""))
        if not item_id or item_id in seen: errors.append("HAS row IDs must be non-empty and unique"); continue
        seen.add(item_id)
        if raw.get("disposition") not in HAS_DISPOSITIONS: errors.append(f"HAS {item_id}: invalid disposition")
        if not raw.get("reason"): errors.append(f"HAS {item_id}: disposition requires reason")
    omitted = set(str(v) for v in accepted_ids) - seen
    if omitted: errors.append(f"candidate overlay/HAS cannot delete accepted entries by omission: {', '.join(sorted(omitted))}")
    return errors


def validate_overlay(base: PemDocument, candidate: PemDocument, *, overlay_identity: str, accepted_pem_identity: str) -> list[str]:
    errors: list[str] = []
    declared = candidate.metadata.get("candidate_overlay")
    if isinstance(declared, dict): identity = str(declared.get("identity", "")); based_on = str(declared.get("based_on_accepted_pem", ""))
    else: identity = str(declared); based_on = ""
    if identity != overlay_identity: errors.append("candidate overlay identity does not match the selected overlay")
    if based_on != accepted_pem_identity: errors.append("candidate overlay is not explicitly based on the exact workflow-selected accepted PEM publication")
    if identity == accepted_pem_identity: errors.append("candidate overlay cannot self-ratify as accepted memory")
    omitted = set(base.families) | set(base.notices); omitted -= set(candidate.families) | set(candidate.notices)
    if omitted: errors.append(f"candidate overlay cannot delete accepted entries by omission: {', '.join(sorted(omitted))}")
    errors.extend(validate_reconciliation(base, candidate))
    return errors


def select_applicable(doc: PemDocument, terms: Iterable[str]) -> list[str]:
    needles = {str(term).strip().lower() for term in terms if str(term).strip()}
    if not needles: return []
    hits: list[str] = []
    for fid, family in doc.families.items():
        if family.get("state") == "RETIRED": continue
        identity = family.get("semantic_identity", {}) if isinstance(family.get("semantic_identity"), dict) else {}
        fields = [fid, family.get("summary", ""), family.get("aggregation_scope", ""), *family.get("applicability", [])]; fields.extend(identity.values())
        if any(needle in " ".join(str(v).lower() for v in fields) for needle in needles): hits.append(fid)
    for nid, notice in doc.notices.items():
        if notice.get("state") == "RETIRED": continue
        haystack = " ".join(str(v).lower() for v in [nid, notice.get("summary", ""), *notice.get("applicability", [])])
        if any(needle in haystack for needle in needles): hits.append(nid)
    return sorted(hits)


def write_summary(doc: PemDocument) -> None:
    match = SUMMARY_RE.search(doc.root_text)
    if not match: raise PemError("PEM root is missing derived active-summary markers")
    replacement = match.group("start") + render_summary(doc) + match.group("end")
    doc.root.write_text(doc.root_text[:match.start()] + replacement + doc.root_text[match.end():], encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("path", nargs="?", default="PROJECT-ENGINEERING-MEMORY.md"); parser.add_argument("--write-summary", action="store_true"); args = parser.parse_args(argv)
    try:
        doc = load_memory(args.path)
        if args.write_summary: write_summary(doc); doc = load_memory(args.path)
        errors = validate_memory(doc)
    except (OSError, UnicodeDecodeError, PemError) as exc:
        print(f"PEM validation failed: {exc}", file=sys.stderr); return 1
    if errors:
        for error in errors: print(f"PEM validation failed: {error}", file=sys.stderr)
        return 1
    print(f"PEM schema {SCHEMA_VERSION} valid: {len(doc.families)} families, {len(doc.notices)} notices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
