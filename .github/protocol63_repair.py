from pathlib import Path

p = Path('source/project_engineering_memory.py')
s = p.read_text(encoding='utf-8')

def replace(old: str, new: str, name: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f'{name} patch anchor missing')
    s = s.replace(old, new, 1)

replace(
'''    if not _git_ok(root, "cat-file", "-e", f"{route.revision}:{route.path}"):
        return "UNAVAILABLE", "declared path is absent from the immutable repository revision"
    return "HEALTHY", "commit and repository path resolve"
''',
'''    if not _git_ok(root, "cat-file", "-e", f"{route.revision}:{route.path}"):
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
''', 'locator')

replace(
'''    routes.extend(str(v) for v in family.get("authority_evidence", []) if isinstance(v, str))
    return routes
''',
'''    routes.extend(str(v) for v in family.get("authority_evidence", []) if isinstance(v, str))
    override = family.get("temperature_override")
    if isinstance(override, dict):
        routes.extend(str(v) for v in override.get("evidence", []) if isinstance(v, str))
    counterevidence = family.get("counterevidence_search")
    if isinstance(counterevidence, dict):
        routes.extend(str(v) for v in counterevidence.get("evidence", []) if isinstance(v, str))
    return routes
''', 'material-routes')

replace(
'''    if declared != base:
        override = family.get("temperature_override")
        if not isinstance(override, dict) or override.get("final") != declared or not override.get("reason") or not override.get("evidence"):
            errors.append(f"{fid}: temperature {declared!r} differs from derived base {base!r} without evidence-bound override")
''',
'''    if declared != base:
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
''', 'temperature')

replace(
'''            current = _current_assessment(row, f"{family_id}:{oid}")
            if current and current.get("state") == "ADMISSIBLE" and current.get("conclusion") == "CONFIRMED":
''',
'''            current = _current_assessment(row, f"{family_id}:{oid}")
            cause_claim = str(row.get("cause_claim", "")).strip()
            cause_evidence = row.get("cause_evidence", [])
            if cause_claim:
                if not isinstance(cause_evidence, list) or not cause_evidence:
                    raise PemError(f"{family_id}:{oid}: mechanism-specific cause_claim requires discriminating cause_evidence")
                for raw in cause_evidence:
                    parse_evidence_route(raw, f"{family_id}:{oid}:cause_evidence")
            if current and current.get("state") == "ADMISSIBLE" and current.get("conclusion") == "CONFIRMED":
''', 'causal')

replace(
'''        if eligible:
            if family.get("state") != "CURRENT" or family.get("maturity") not in {"SUPPORTED", "PROVEN"}: errors.append(f"{fid}: positive guidance eligibility requires CURRENT SUPPORTED/PROVEN state")
            if counts.get("supporting", 0) < 1: errors.append(f"{fid}: positive guidance eligibility requires admissible supporting evidence")
            if counts.get("contradicting", 0): errors.append(f"{fid}: positive guidance eligibility hides admissible contradiction")
            if binding_health != "HEALTHY": errors.append(f"{fid}: positive guidance eligibility requires explicit HEALTHY binding_health")
''',
'''        if eligible:
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
''', 'counterevidence')

replace(
'''def render_summary(doc: PemDocument) -> str:
    rows: list[str] = []
''',
'''def _notice_is_unresolved(notice: dict[str, Any], doc: PemDocument) -> bool:
    if notice.get("state") == "REVIEW_REQUIRED" or notice.get("binding_health") in {"REVIEW_REQUIRED", "UNAVAILABLE"}:
        return True
    trigger_state, _ = _notice_trigger_state(notice, doc)
    return notice.get("state") == "CURRENT" and trigger_state != "CLEAR"


def render_summary(doc: PemDocument) -> str:
    rows: list[str] = []
''', 'notice-helper')

replace(
'''    notice_rows = [f"- **{n['id']}** [{n['state']}/{n['binding_health']}]: {n['summary']}" for n in sorted(doc.notices.values(), key=lambda n: (0 if n.get("state") == "REVIEW_REQUIRED" else 1, str(n.get("id")))) if n.get("state") in {"CURRENT", "REVIEW_REQUIRED"}]
    parts: list[str] = []
    if rows: parts.extend(["| ID | Kind | Temperature | Maturity/state | Binding | Guidance | Current evidence | Bounded lesson |", "| --- | --- | --- | --- | --- | --- | --- | --- |", *rows])
    else: parts.append("_No current learning families._")
    if notice_rows: parts.extend(["", "Current notices:", "", *notice_rows])
''',
'''    active_notices = [n for n in doc.notices.values() if n.get("state") in {"CURRENT", "REVIEW_REQUIRED"}]
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
''', 'summary-order')

replace(
'''def validate_reconciliation(previous: PemDocument, current: PemDocument) -> list[str]:
    """Reject silent observation rewriting across family moves, row re-IDs, splits, and merges."""
    errors: list[str] = []
    old_rows = _all_event_rows(previous); new_rows = _all_event_rows(current)
    for identity in old_rows.keys() & new_rows.keys():
        error = _validate_observation_correction(identity, old_rows[identity], new_rows[identity])
        if error: errors.append(error)
    return errors
''',
'''def _semantic_identity_signature(family: dict[str, Any]) -> str:
    payload = {"kind": family.get("kind"), "semantic_identity": family.get("semantic_identity"), "applicability": family.get("applicability")}
    return hashlib.sha256(yaml.safe_dump(payload, sort_keys=True).encode("utf-8")).hexdigest()


def validate_reconciliation(previous: PemDocument, current: PemDocument) -> list[str]:
    """Reject silent accepted semantic drift and observation rewriting across representations."""
    errors: list[str] = []
    for fid in previous.families.keys() & current.families.keys():
        old_family = previous.families[fid]; new_family = current.families[fid]
        old_sig = _semantic_identity_signature(old_family); new_sig = _semantic_identity_signature(new_family)
        if old_sig != new_sig:
            record = new_family.get("semantic_reconciliation")
            if not isinstance(record, dict):
                errors.append(f"{fid}: accepted family semantic identity/applicability changed under the same ID without explicit reconciliation or lineage")
            else:
                evidence = record.get("evidence")
                if (record.get("classification") != "WITHIN_ENVELOPE" or record.get("previous_identity_sha256") != old_sig or not record.get("reason") or not isinstance(evidence, list) or not evidence):
                    errors.append(f"{fid}: same-ID semantic reconciliation must bind the previous envelope, WITHIN_ENVELOPE classification, reason, and evidence")
                else:
                    for raw in evidence:
                        try: parse_evidence_route(raw, f"{fid}:semantic reconciliation evidence")
                        except PemError as exc: errors.append(str(exc))
    old_rows = _all_event_rows(previous); new_rows = _all_event_rows(current)
    for identity in old_rows.keys() & new_rows.keys():
        error = _validate_observation_correction(identity, old_rows[identity], new_rows[identity])
        if error: errors.append(error)
    return errors
''', 'reconciliation')

replace(
'''def validate_overlay(base: PemDocument, candidate: PemDocument, *, overlay_identity: str) -> list[str]:
    errors: list[str] = []
    declared = candidate.metadata.get("candidate_overlay")
    if isinstance(declared, dict): identity = str(declared.get("identity", "")); based_on = str(declared.get("based_on_accepted_pem", ""))
    else: identity = str(declared); based_on = ""
    if identity != overlay_identity: errors.append("candidate overlay identity does not match the selected overlay")
    base_identity = _accepted_base_identity(base.metadata.get("accepted_base"))
    if based_on != base_identity: errors.append("candidate overlay is not explicitly based on the declared accepted memory state")
    if identity == base_identity: errors.append("candidate overlay cannot self-ratify as accepted memory")
    omitted = set(base.families) | set(base.notices); omitted -= set(candidate.families) | set(candidate.notices)
    if omitted: errors.append(f"candidate overlay cannot delete accepted entries by omission: {', '.join(sorted(omitted))}")
    return errors
''',
'''def validate_overlay(base: PemDocument, candidate: PemDocument, *, overlay_identity: str, accepted_pem_identity: str) -> list[str]:
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
''', 'overlay')

p.write_text(s, encoding='utf-8')

p = Path('source/shared/references/project-engineering-memory.md')
d = p.read_text(encoding='utf-8')
if '## Independent-review repair clarifications' not in d:
    d += '''\n\n## Independent-review repair clarifications\n\n- Stable evidence locators participate in binding health; path-only realization cannot make a missing locator healthy.\n- Mechanism-specific failure cause claims require durable discriminating cause evidence; observation-only rows need not invent a cause.\n- Current positive guidance requires a bounded counterevidence-search disposition covering supporting, neutral, contradicting, and inconclusive outcomes plus blind spots and durable search evidence.\n- Candidate overlays bind the exact workflow-selected accepted PEM publication separately from accepted project state.\n- Same accepted family IDs cannot silently change kind, semantic identity envelope, or applicability meaning; within-envelope reconciliation is explicit and evidence-bound, while material change uses lineage/new identity.\n- Temperature override evidence uses ordinary evidence-route health.\n- High-impact unresolved notices precede optional positive guidance in the active summary.\n'''
p.write_text(d, encoding='utf-8')

Path('tests/test_protocol_63_independent_review_repairs.py').write_text(r'''from __future__ import annotations
import copy, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
import project_engineering_memory as pem

def doc(families=None, notices=None, *, overlay="NONE", accepted_base="P"):
    return pem.PemDocument(root=ROOT / "PROJECT-ENGINEERING-MEMORY.md", metadata={"repository": "hjin98/scientific-software-development-protocol", "accepted_base": accepted_base, "candidate_overlay": overlay}, families={f["id"]: f for f in (families or [])}, notices={n["id"]: n for n in (notices or [])}, sources={}, root_text="")

def success(fid="SP-001"):
    return {"id": fid, "kind": "SUCCESS_PATTERN", "state": "CURRENT", "maturity": "SUPPORTED", "temperature": "UNASSESSED", "summary": "bounded success", "semantic_identity": {"invariant_or_claim": "claim", "owner_class": "D3/D4", "mechanism_family": "mechanism", "applicability_dimensions": "regime"}, "aggregation_scope": "scope", "coverage_state": "PARTIAL", "coverage_basis": "bounded", "applicability": ["x"], "authority_binding": "EVIDENCE_ONLY", "binding_health": "HEALTHY", "guidance_level": "OBSERVED", "positive_guidance_eligible": False, "relations": [], "applications": [{"id": "A01", "episode_identity": "episode-1", "lifecycle_context": "qualification", "source_project": "local", "surfaces": ["x"], "provenance_cluster": "cluster-1", "outcome": "SUPPORTING", "observation": "worked", "assessments": [{"id": "AS01", "state": "ADMISSIBLE", "conclusion": "SUPPORTS_BOUNDED_CLAIM", "evidence": ["repo@1111111:path#finding"]}]}]}

class IndependentReviewRepairTests(unittest.TestCase):
    def test_d8_01_same_id_semantic_drift_rejected(self):
        old = success(); new = copy.deepcopy(old); new["semantic_identity"]["mechanism_family"] = "different"
        self.assertTrue(any("semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([new]))))
        self.assertEqual(pem.validate_reconciliation(doc([old]), doc([copy.deepcopy(old)])), [])
    def test_d8_02_overlay_uses_exact_accepted_pem_publication(self):
        base = success(); good = doc([copy.deepcopy(base)], overlay={"identity": "C", "based_on_accepted_pem": "M"}, accepted_base="P"); bad = doc([copy.deepcopy(base)], overlay={"identity": "C", "based_on_accepted_pem": "P"}, accepted_base="P")
        self.assertEqual(pem.validate_overlay(doc([base]), good, overlay_identity="C", accepted_pem_identity="M"), [])
        self.assertTrue(any("accepted PEM publication" in e for e in pem.validate_overlay(doc([base]), bad, overlay_identity="C", accepted_pem_identity="M")))
    def test_d8_03_missing_stable_locator_is_not_healthy(self):
        rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(); route = pem.parse_evidence_route(f"hjin98/scientific-software-development-protocol@{rev}:source/project_engineering_memory.py#THIS-LOCATOR-DOES-NOT-EXIST")
        self.assertEqual(pem.evidence_route_health(route, doc())[0], "UNAVAILABLE")
    def test_d8_04_mechanism_cause_requires_cause_evidence(self):
        f = {"id": "FF-001", "kind": "FAILURE_FAMILY", "state": "CURRENT", "maturity": "SUPPORTED", "temperature": "UNASSESSED", "summary": "failure", "semantic_identity": {"invariant_or_claim": "inv", "owner_class": "D4", "mechanism_family": "m", "applicability_dimensions": "r"}, "aggregation_scope": "s", "coverage_state": "PARTIAL", "coverage_basis": "b", "applicability": ["x"], "authority_binding": "EVIDENCE_ONLY", "binding_health": "REVIEW_REQUIRED", "guidance_level": "OBSERVED", "relations": [], "occurrences": [{"id": "O01", "event_identity": "e1", "lifecycle_context": "qualification", "source_project": "local", "surfaces": ["x"], "observation": "failed", "cause_claim": "specific mechanism", "assessments": [{"id": "AS01", "state": "ADMISSIBLE", "conclusion": "CONFIRMED", "evidence": ["repo@1111111:path#finding"]}]}]}
        self.assertTrue(any("cause_claim requires" in e for e in pem._validate_family(f))); del f["occurrences"][0]["cause_claim"]; self.assertFalse(any("cause_claim requires" in e for e in pem._validate_family(f)))
    def test_d8_05_wins_only_positive_guidance_rejected(self):
        f = success(); f.update(guidance_level="RECOMMENDED", positive_guidance_eligible=True)
        self.assertTrue(any("counterevidence_search" in e for e in pem._validate_family(f)))
        f["counterevidence_search"] = {"state": "COMPLETE_FOR_DECLARED_SCOPE", "scope": "scope", "search_basis": "bounded history", "blind_spots": "broader history not claimed", "outcomes_reviewed": ["SUPPORTING", "NEUTRAL", "CONTRADICTING", "INCONCLUSIVE"], "evidence": ["repo@1111111:path#search"]}
        self.assertFalse(any("counterevidence_search" in e for e in pem._validate_family(f)))
    def test_d8_06_unresolved_notice_precedes_positive_guidance(self):
        f = success(); n = {"id": "NT-001", "state": "REVIEW_REQUIRED", "binding_health": "REVIEW_REQUIRED", "summary": "unresolved risk", "applicability": ["x"], "normative_status": "NON_AUTHORITATIVE", "review_trigger": {"type": "manual_external", "assessed_state": "INDETERMINATE", "assessed_evidence": ["repo@1111111:path#notice"]}, "evidence": ["repo@1111111:path#notice"]}
        text = pem.render_summary(doc([f], [n])); self.assertLess(text.index("NT-001"), text.index("SP-001"))
    def test_d8_07_temperature_override_evidence_is_material(self):
        f = success(); f["temperature"] = "HOT"; f["temperature_override"] = {"final": "HOT", "reason": "impact", "evidence": "not-a-list"}
        self.assertTrue(any("temperature override requires" in e for e in pem._validate_family(f))); f["temperature_override"]["evidence"] = ["repo@1111111:path#impact"]; self.assertIn("repo@1111111:path#impact", pem._material_routes(f))

if __name__ == '__main__': unittest.main()
''', encoding='utf-8')
