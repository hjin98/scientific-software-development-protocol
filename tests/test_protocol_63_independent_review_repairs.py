from __future__ import annotations
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
        errors = pem.validate_reconciliation(doc([old]), doc([new]))
        self.assertTrue(any("mechanically material semantic identity" in e for e in errors))
        laundering = copy.deepcopy(new)
        laundering["semantic_reconciliation"] = {
            "classification": "WITHIN_ENVELOPE",
            "previous_identity_sha256": pem._semantic_identity_signature(old),
            "reason": "claim that the changed mechanism is merely editorial",
            "evidence": ["repo@1111111:path#review"],
        }
        self.assertTrue(any("mechanically material semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([laundering]))))
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
