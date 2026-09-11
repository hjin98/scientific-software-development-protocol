#!/usr/bin/env python3
"""Validate and render Protocol 6.3 Project Engineering Memory (PEM) schema 1.

Markdown remains the canonical project memory. This utility is deliberately a
small structural validator/derived-view renderer, not a database, authority
registry, history indexer, or background service.
"""
from __future__ import annotations

import argparse
import dataclasses
import re
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
    "ADMISSIBLE",
    "REVIEW_REQUIRED",
    "INCONCLUSIVE",
    "CHALLENGED",
    "REJECTED_OR_INVALID",
    "STALE_OR_INAPPLICABLE",
    "RETIRED",
}
APPLICATION_OUTCOMES = {"SUPPORTING", "NEUTRAL", "CONTRADICTING", "INCONCLUSIVE"}
GUIDANCE_LEVELS = {"OBSERVED", "RECOMMENDED", "PREFERRED", "DEFAULT", "BEST"}
BINDING_HEALTH = {"HEALTHY", "REVIEW_REQUIRED", "UNAVAILABLE", "RETIRED"}
LINEAGE_RELATIONS = {"SUPERSEDES", "SPLIT_FROM", "MERGED_FROM", "REPLACES"}
RELATION_TYPES = LINEAGE_RELATIONS | {
    "LED_TO",
    "NARROWS",
    "GENERALIZES",
    "SUPPORTS_LEARNING_FROM",
    "CONFLICTS_WITH",
}
ID_RE = re.compile(r"^(FF|SP|DS|PC)-[0-9]+$")
NOTICE_ID_RE = re.compile(r"^NT-[0-9]+$")
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


def _safe_detail_path(root: Path, raw: Any) -> Path:
    if not isinstance(raw, str) or not raw or raw.startswith(("/", "~")):
        raise PemError(f"invalid detail_files entry: {raw!r}")
    candidate = (root.parent / raw).resolve()
    base = root.parent.resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise PemError(f"detail file escapes project memory root: {raw}") from exc
    if candidate.suffix.lower() != ".md":
        raise PemError(f"detail file must be Markdown: {raw}")
    return candidate


def load_memory(root: Path | str) -> PemDocument:
    root = Path(root).resolve()
    text = root.read_text(encoding="utf-8")
    metadata = _frontmatter(text, root)
    if metadata.get("memory_schema_version") != SCHEMA_VERSION:
        raise PemError(
            f"{root}: unsupported memory_schema_version {metadata.get('memory_schema_version')!r}; "
            f"supported={SCHEMA_VERSION}"
        )
    required_meta = {
        "maintained_under_protocol",
        "project_id",
        "repository",
        "scope",
        "coverage_state",
        "coverage_basis",
        "reconciled_through",
        "accepted_base",
        "candidate_overlay",
    }
    missing = sorted(k for k in required_meta if not metadata.get(k))
    if missing:
        raise PemError(f"{root}: missing required metadata: {', '.join(missing)}")
    if metadata["coverage_state"] not in {"UNINITIALIZED", "PARTIAL", "RECONCILED_FOR_DECLARED_SCOPE"}:
        raise PemError(f"{root}: invalid coverage_state {metadata['coverage_state']!r}")

    families, notices = _parse_blocks(text, root)
    sources: dict[str, Path] = {**{k: root for k in families}, **{k: root for k in notices}}
    for raw in _list(metadata.get("detail_files", []), f"{root}:detail_files"):
        detail = _safe_detail_path(root, raw)
        if not detail.is_file():
            raise PemError(f"declared detail file is missing: {raw}")
        detail_text = detail.read_text(encoding="utf-8")
        detail_meta = _frontmatter(detail_text, detail)
        if detail_meta.get("memory_schema_version") != SCHEMA_VERSION or detail_meta.get("pem_partition") is not True:
            raise PemError(f"{detail}: invalid PEM partition metadata")
        if detail_meta.get("project_id") != metadata["project_id"]:
            raise PemError(f"{detail}: project_id differs from root")
        if SUMMARY_RE.search(detail_text):
            raise PemError(f"{detail}: only the PEM root may own the active summary")
        part_families, part_notices = _parse_blocks(detail_text, detail)
        for row_id, row in {**part_families, **part_notices}.items():
            if row_id in sources:
                raise PemError(f"duplicate canonical PEM ID {row_id} in {sources[row_id]} and {detail}")
            sources[row_id] = detail
        families.update(part_families)
        notices.update(part_notices)
    return PemDocument(root, metadata, families, notices, sources, text)


def _latest_assessment(row: dict[str, Any], where: str) -> dict[str, Any] | None:
    assessments = _list(row.get("assessments", []), f"{where}:assessments")
    if not assessments:
        return None
    ids: set[str] = set()
    for item in assessments:
        item = _mapping(item, f"{where}:assessment")
        aid = str(item.get("id", ""))
        if not aid or aid in ids:
            raise PemError(f"{where}: assessment IDs must be non-empty and unique")
        ids.add(aid)
        if item.get("state") not in ASSESSMENT_STATES:
            raise PemError(f"{where}:{aid}: invalid assessment state {item.get('state')!r}")
        if "evidence" not in item:
            raise PemError(f"{where}:{aid}: assessment requires evidence route(s)")
    return _mapping(assessments[-1], f"{where}:latest-assessment")


def _admissible(row: dict[str, Any], where: str) -> bool:
    latest = _latest_assessment(row, where)
    return bool(latest and latest.get("state") == "ADMISSIBLE")


def derived_counts(family: dict[str, Any]) -> dict[str, int]:
    family_id = str(family.get("id", "?"))
    kind = family.get("kind")
    if kind == "FAILURE_FAMILY":
        occurrences = _list(family.get("occurrences", []), f"{family_id}:occurrences")
        confirmed = 0
        recurrence = 0
        surfaces: set[str] = set()
        episode_ids: set[str] = set()
        for row in occurrences:
            row = _mapping(row, f"{family_id}:occurrence")
            oid = str(row.get("id", ""))
            episode = str(row.get("event_identity", ""))
            if not oid or not episode or episode in episode_ids:
                raise PemError(f"{family_id}: occurrence IDs/event identities must be non-empty and event identities unique")
            episode_ids.add(episode)
            surfaces.update(str(v) for v in _list(row.get("surfaces", []), f"{family_id}:{oid}:surfaces"))
            latest = _latest_assessment(row, f"{family_id}:{oid}")
            if latest and latest.get("state") == "ADMISSIBLE" and latest.get("conclusion") == "CONFIRMED":
                confirmed += 1
                if row.get("recurrence_after_accepted_repair") is True:
                    if not row.get("prior_accepted_repair"):
                        raise PemError(f"{family_id}:{oid}: recurrence requires prior_accepted_repair identity")
                    recurrence += 1
        return {"confirmed": confirmed, "affected_surfaces": len(surfaces), "recurrence": recurrence}
    if kind == "SUCCESS_PATTERN":
        applications = _list(family.get("applications", []), f"{family_id}:applications")
        counts = {"evaluated": len(applications), "supporting": 0, "neutral": 0, "contradicting": 0, "inconclusive": 0}
        surfaces: set[str] = set()
        episodes: set[str] = set()
        for row in applications:
            row = _mapping(row, f"{family_id}:application")
            aid = str(row.get("id", ""))
            episode = str(row.get("episode_identity", ""))
            if not aid or not episode or episode in episodes:
                raise PemError(f"{family_id}: application IDs/episode identities must be non-empty and episode identities unique")
            episodes.add(episode)
            surfaces.update(str(v) for v in _list(row.get("surfaces", []), f"{family_id}:{aid}:surfaces"))
            outcome = row.get("outcome")
            if outcome not in APPLICATION_OUTCOMES:
                raise PemError(f"{family_id}:{aid}: invalid outcome {outcome!r}")
            latest = _latest_assessment(row, f"{family_id}:{aid}")
            if latest and latest.get("state") == "ADMISSIBLE":
                counts[outcome.lower()] += 1
        counts["affected_surfaces"] = len(surfaces)
        return counts
    return {"evidence": len(_list(family.get("evidence", []), f"{family_id}:evidence"))}


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


def _validate_family(family: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fid = str(family.get("id", ""))
    prefix = fid.split("-", 1)[0] if "-" in fid else ""
    expected = {"FF": "FAILURE_FAMILY", "SP": "SUCCESS_PATTERN", "DS": "DISCOVERY", "PC": "PRESERVATION_CAPABILITY"}.get(prefix)
    if not ID_RE.fullmatch(fid):
        errors.append(f"{fid or '<missing>'}: invalid family ID")
    if family.get("kind") not in FAMILY_KINDS or family.get("kind") != expected:
        errors.append(f"{fid}: kind does not match ID namespace")
    if family.get("state") not in FAMILY_STATES:
        errors.append(f"{fid}: invalid state {family.get('state')!r}")
    if family.get("maturity") not in MATURITIES:
        errors.append(f"{fid}: invalid maturity {family.get('maturity')!r}")
    if family.get("temperature") not in TEMPERATURES:
        errors.append(f"{fid}: invalid temperature {family.get('temperature')!r}")
    if family.get("authority_binding") not in AUTHORITY_BINDINGS:
        errors.append(f"{fid}: invalid authority_binding {family.get('authority_binding')!r}")
    for field in ("summary", "aggregation_scope", "coverage_state", "coverage_basis", "applicability"):
        if field not in family:
            errors.append(f"{fid}: missing {field}")
    identity = family.get("semantic_identity")
    if not isinstance(identity, dict) or any(not identity.get(k) for k in ("invariant_or_claim", "owner_class", "mechanism_family", "applicability_dimensions")):
        errors.append(f"{fid}: incomplete semantic_identity envelope")
    if family.get("coverage_state") not in {"UNINITIALIZED", "PARTIAL", "RECONCILED_FOR_DECLARED_SCOPE"}:
        errors.append(f"{fid}: invalid coverage_state")
    try:
        counts = derived_counts(family)
    except PemError as exc:
        errors.append(str(exc))
        counts = {}
    base = base_temperature(family, counts)
    declared = family.get("temperature")
    if declared != base:
        override = family.get("temperature_override")
        if not isinstance(override, dict) or override.get("final") != declared or not override.get("reason") or not override.get("evidence"):
            errors.append(f"{fid}: temperature {declared!r} differs from derived base {base!r} without evidence-bound override")

    if family.get("maturity") == "SUPPORTED":
        if family.get("kind") == "FAILURE_FAMILY" and counts.get("confirmed", 0) < 1:
            errors.append(f"{fid}: SUPPORTED failure family has no admissible confirmed occurrence")
        elif family.get("kind") == "SUCCESS_PATTERN" and counts.get("supporting", 0) < 1:
            errors.append(f"{fid}: SUPPORTED success pattern has no admissible supporting application")
        elif family.get("kind") in {"DISCOVERY", "PRESERVATION_CAPABILITY"} and counts.get("evidence", 0) < 1:
            errors.append(f"{fid}: SUPPORTED finding requires evidence")
    if family.get("maturity") == "PROVEN":
        basis = family.get("maturity_basis")
        if not isinstance(basis, dict) or basis.get("all_obligations_closed") is not True or not basis.get("evidence"):
            errors.append(f"{fid}: PROVEN requires claim-relative maturity_basis with all obligations closed and evidence")
        if family.get("state") != "CURRENT":
            errors.append(f"{fid}: non-current family cannot remain PROVEN current guidance")
        if family.get("kind") == "SUCCESS_PATTERN" and counts.get("contradicting", 0):
            errors.append(f"{fid}: PROVEN success pattern has unresolved admissible contradiction")

    guidance = family.get("guidance_level", "OBSERVED")
    if guidance not in GUIDANCE_LEVELS:
        errors.append(f"{fid}: invalid guidance_level {guidance!r}")
    if family.get("kind") == "SUCCESS_PATTERN":
        eligible = family.get("positive_guidance_eligible", False)
        if guidance in {"RECOMMENDED", "PREFERRED", "DEFAULT", "BEST"}:
            if not eligible or family.get("state") != "CURRENT" or family.get("maturity") not in {"SUPPORTED", "PROVEN"}:
                errors.append(f"{fid}: positive recommendation is not eligible/current/sufficiently mature")
            if counts.get("contradicting", 0):
                errors.append(f"{fid}: positive recommendation hides admissible contradiction")
            if family.get("binding_health", "HEALTHY") != "HEALTHY":
                errors.append(f"{fid}: positive recommendation has unhealthy material binding")
        if guidance in {"PREFERRED", "DEFAULT", "BEST"}:
            comparative = family.get("comparative_basis")
            authority_basis = family.get("comparative_authority")
            if comparative in (None, "", "NONE") and not authority_basis:
                errors.append(f"{fid}: comparative/default/best guidance lacks comparative evidence or current-owner priority")
    elif guidance != "OBSERVED":
        errors.append(f"{fid}: only SUCCESS_PATTERN may carry positive guidance levels")

    if family.get("authority_binding") == "AUTHORITY_BOUND" and not family.get("authority_owner"):
        errors.append(f"{fid}: AUTHORITY_BOUND requires authority_owner")

    relations = family.get("relations", [])
    if not isinstance(relations, list):
        errors.append(f"{fid}: relations must be a list")
    else:
        for relation in relations:
            if not isinstance(relation, dict) or relation.get("type") not in RELATION_TYPES or not relation.get("target"):
                errors.append(f"{fid}: invalid typed relation {relation!r}")
    return errors


def _validate_lineage(doc: PemDocument) -> list[str]:
    errors: list[str] = []
    graph: dict[str, set[str]] = {fid: set() for fid in doc.families}
    for fid, family in doc.families.items():
        for relation in family.get("relations", []) if isinstance(family.get("relations", []), list) else []:
            target = relation.get("target") if isinstance(relation, dict) else None
            if target not in doc.families:
                errors.append(f"{fid}: relation target {target!r} has no canonical family record")
                continue
            if relation.get("type") in LINEAGE_RELATIONS:
                graph[fid].add(str(target))
            if relation.get("type") == "CONFLICTS_WITH":
                other = doc.families[str(target)]
                active_guidance = family.get("guidance_level") in {"RECOMMENDED", "PREFERRED", "DEFAULT", "BEST"}
                other_guidance = other.get("guidance_level") in {"RECOMMENDED", "PREFERRED", "DEFAULT", "BEST"}
                if active_guidance and other_guidance and family.get("state") == other.get("state") == "CURRENT":
                    if not family.get("decision_boundary") and not other.get("decision_boundary"):
                        errors.append(f"{fid}: current conflicting guidance with {target} lacks decision boundary/tradeoff")
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        if node in done:
            return
        if node in visiting:
            errors.append(f"lineage cycle includes {node}")
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        done.add(node)

    for node in graph:
        visit(node)
    return errors


def _validate_notices(doc: PemDocument) -> list[str]:
    errors: list[str] = []
    for nid, notice in doc.notices.items():
        if not NOTICE_ID_RE.fullmatch(nid):
            errors.append(f"{nid}: invalid notice ID")
        if notice.get("state") not in FAMILY_STATES:
            errors.append(f"{nid}: invalid state")
        if notice.get("binding_health") not in BINDING_HEALTH:
            errors.append(f"{nid}: invalid binding_health")
        for key in ("summary", "applicability", "evidence", "review_or_expiry", "normative_status"):
            if not notice.get(key):
                errors.append(f"{nid}: missing {key}")
        if notice.get("state") == "CURRENT" and notice.get("binding_health") != "HEALTHY":
            errors.append(f"{nid}: unhealthy notice cannot remain unqualified CURRENT")
    return errors


def _salience_key(family: dict[str, Any]) -> tuple[int, int, str]:
    unresolved = 0 if family.get("state") == "REVIEW_REQUIRED" else 1
    temp = {"HOT": 0, "WARM": 1, "COLD": 2, "UNASSESSED": 3}.get(str(family.get("temperature")), 4)
    return unresolved, temp, str(family.get("id"))


def render_summary(doc: PemDocument) -> str:
    rows: list[str] = []
    for family in sorted(doc.families.values(), key=_salience_key):
        if family.get("state") not in {"CURRENT", "REVIEW_REQUIRED"}:
            continue
        counts = derived_counts(family)
        if family.get("kind") == "FAILURE_FAMILY":
            count_text = f"{counts.get('confirmed', 0)} confirmed"
        elif family.get("kind") == "SUCCESS_PATTERN":
            count_text = (
                f"{counts.get('supporting', 0)} supporting / {counts.get('neutral', 0)} neutral / "
                f"{counts.get('contradicting', 0)} contradicting / {counts.get('inconclusive', 0)} inconclusive"
            )
        else:
            count_text = f"{counts.get('evidence', 0)} evidence route(s)"
        guidance = family.get("guidance_level", "OBSERVED")
        rows.append(
            "| {id} | {kind} | {temp} | {maturity}/{state} | {guidance} | {count} | {summary} |".format(
                id=family["id"], kind=family["kind"], temp=family["temperature"], maturity=family["maturity"],
                state=family["state"], guidance=guidance, count=count_text, summary=str(family["summary"]).replace("|", "\\|"),
            )
        )
    notice_rows: list[str] = []
    for notice in sorted(doc.notices.values(), key=lambda n: (0 if n.get("state") == "REVIEW_REQUIRED" else 1, str(n.get("id")))):
        if notice.get("state") in {"CURRENT", "REVIEW_REQUIRED"}:
            notice_rows.append(f"- **{notice['id']}** [{notice['state']}/{notice['binding_health']}]: {notice['summary']}")
    parts: list[str] = []
    if rows:
        parts.extend([
            "| ID | Kind | Temperature | Maturity/state | Guidance | Current evidence | Bounded lesson |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
        ])
    else:
        parts.append("_No current learning families._")
    if notice_rows:
        parts.extend(["", "Current notices:", "", *notice_rows])
    return "\n".join(parts).rstrip() + "\n"


def validate_memory(doc: PemDocument, *, check_summary: bool = True) -> list[str]:
    errors: list[str] = []
    for family in doc.families.values():
        errors.extend(_validate_family(family))
    errors.extend(_validate_lineage(doc))
    errors.extend(_validate_notices(doc))
    if check_summary:
        match = SUMMARY_RE.search(doc.root_text)
        if not match:
            errors.append("PEM root is missing derived active-summary markers")
        else:
            actual = match.group("body")
            expected = render_summary(doc)
            if actual != expected:
                errors.append("derived active summary is stale; run --write-summary")
    return errors


def select_applicable(doc: PemDocument, terms: Iterable[str]) -> list[str]:
    """Return canonical candidate IDs; never use active-summary/index presence as the search boundary."""
    needles = {str(term).strip().lower() for term in terms if str(term).strip()}
    if not needles:
        return []
    hits: list[str] = []
    for fid, family in doc.families.items():
        if family.get("state") == "RETIRED":
            continue
        identity = family.get("semantic_identity", {}) if isinstance(family.get("semantic_identity"), dict) else {}
        fields = [fid, family.get("summary", ""), family.get("aggregation_scope", ""), *family.get("applicability", [])]
        fields.extend(identity.values())
        haystack = " ".join(str(value).lower() for value in fields)
        if any(needle in haystack for needle in needles):
            hits.append(fid)
    for nid, notice in doc.notices.items():
        if notice.get("state") == "RETIRED":
            continue
        haystack = " ".join(str(v).lower() for v in [nid, notice.get("summary", ""), *notice.get("applicability", [])])
        if any(needle in haystack for needle in needles):
            hits.append(nid)
    return sorted(hits)


def write_summary(doc: PemDocument) -> None:
    match = SUMMARY_RE.search(doc.root_text)
    if not match:
        raise PemError("PEM root is missing derived active-summary markers")
    replacement = match.group("start") + render_summary(doc) + match.group("end")
    updated = doc.root_text[: match.start()] + replacement + doc.root_text[match.end() :]
    doc.root.write_text(updated, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="PROJECT-ENGINEERING-MEMORY.md")
    parser.add_argument("--write-summary", action="store_true")
    args = parser.parse_args(argv)
    try:
        doc = load_memory(args.path)
        if args.write_summary:
            write_summary(doc)
            doc = load_memory(args.path)
        errors = validate_memory(doc)
    except (OSError, UnicodeDecodeError, PemError) as exc:
        print(f"PEM validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"PEM validation failed: {error}", file=sys.stderr)
        return 1
    print(f"PEM schema {SCHEMA_VERSION} valid: {len(doc.families)} families, {len(doc.notices)} notices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
