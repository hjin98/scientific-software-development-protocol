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
    def _reconciliation_route(self, locator="def validate_reconciliation"):
        rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        return f"hjin98/scientific-software-development-protocol@{rev}:source/project_engineering_memory.py#{locator}"

    def _within_envelope(self, previous, current, *, evidence=None, reason="bounded same-ID reconciliation"):
        current["semantic_reconciliation"] = {
            "classification": "WITHIN_ENVELOPE",
            "previous_identity_sha256": pem._semantic_identity_signature(previous),
            "reason": reason,
            "evidence": evidence or [self._reconciliation_route()],
        }
        return current

    def test_d8_01_same_id_semantic_drift_rejected(self):
        old = success()
        mechanism = copy.deepcopy(old); mechanism["semantic_identity"]["mechanism_family"] = "different"
        self.assertTrue(any("mechanically material semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([mechanism]))))
        laundering = self._within_envelope(old, copy.deepcopy(mechanism), reason="claim changed mechanism is editorial")
        self.assertTrue(any("mechanically material semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([laundering]))))

        claim = copy.deepcopy(old); claim["semantic_identity"]["invariant_or_claim"] = "different governing claim"
        claim = self._within_envelope(old, claim, reason="claim replacement asserted within envelope")
        self.assertTrue(any("invariant_or_claim" in e and "mechanically material" in e for e in pem.validate_reconciliation(doc([old]), doc([claim]))))

        broad = copy.deepcopy(old); broad["applicability"] = ["x", "y"]
        broad = self._within_envelope(old, broad, reason="broadened applicability asserted within envelope")
        self.assertTrue(any("applicability" in e and "mechanically material" in e for e in pem.validate_reconciliation(doc([old]), doc([broad]))))

        dimensions = copy.deepcopy(old); dimensions["semantic_identity"]["applicability_dimensions"] = "different regime"
        dimensions = self._within_envelope(old, dimensions, reason="changed regime asserted within envelope")
        self.assertTrue(any("applicability_dimensions" in e and "mechanically material" in e for e in pem.validate_reconciliation(doc([old]), doc([dimensions]))))

        old_narrow = success(); old_narrow["applicability"] = ["x", "y"]
        narrow = copy.deepcopy(old_narrow); narrow["applicability"] = ["x"]
        narrow = self._within_envelope(old_narrow, narrow)
        self.assertEqual(pem.validate_reconciliation(doc([old_narrow]), doc([narrow])), [])
        self.assertIn(narrow["semantic_reconciliation"]["evidence"][0], pem._material_routes(narrow))

        broken = copy.deepcopy(narrow)
        broken["semantic_reconciliation"]["evidence"] = [self._reconciliation_route("THIS-RECONCILIATION-LOCATOR-DOES-NOT-EXIST")]
        self.assertTrue(any("not mechanically healthy" in e for e in pem.validate_reconciliation(doc([old_narrow]), doc([broken]))))

        editorial = copy.deepcopy(old); editorial["semantic_identity"]["invariant_or_claim"] = "Claim."
        editorial = self._within_envelope(old, editorial)
        self.assertEqual(pem.validate_reconciliation(doc([old]), doc([editorial])), [])
        self.assertEqual(pem.validate_reconciliation(doc([old]), doc([copy.deepcopy(old)])), [])
    def test_d8_02_overlay_uses_exact_accepted_pem_publication(self):
        base = success(); good = doc([copy.deepcopy(base)], overlay={"identity": "C", "based_on_accepted_pem": "M"}, accepted_base="P"); bad = doc([copy.deepcopy(base)], overlay={"identity": "C", "based_on_accepted_pem": "P"}, accepted_base="P"); self_ratifying = doc([copy.deepcopy(base)], overlay={"identity": "M", "based_on_accepted_pem": "M"}, accepted_base="P")
        self.assertEqual(pem.validate_overlay(doc([base]), good, overlay_identity="C", accepted_pem_identity="M"), [])
        self.assertTrue(any("accepted PEM publication" in e for e in pem.validate_overlay(doc([base]), bad, overlay_identity="C", accepted_pem_identity="M")))
        self.assertTrue(any("self-ratify" in e for e in pem.validate_overlay(doc([base]), self_ratifying, overlay_identity="M", accepted_pem_identity="M")))
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
