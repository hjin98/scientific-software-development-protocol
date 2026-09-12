from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QDIR = ROOT / "qualification" / "ssdp6"
BRANCH = "ssdp-6.3-engineering-memory"
BASELINE = "b59adc77efe6951912cfd705cc43830c58ca27d0"
OLD_CANDIDATE = "42eb89388dc96879157ba92db9e7f3c59f2c0b36"


def run(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def out(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing expected {label}: {old!r}")
    return text.replace(old, new, 1)


run("git", "config", "user.name", "Protocol 6.3 D9 repair automation")
run("git", "config", "user.email", "protocol63-d9-repair@users.noreply.github.com")

# 1. Reopen the active workplan at the exact two owning surfaces.
wp = ROOT / "workplans" / "active" / "PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md"
w = wp.read_text()
w = replace_once(w, "implementation_review_state: reopened-after-independent-no-pass\n", "implementation_review_state: reopened-after-independent-no-pass-4\n", "review state")
w = replace_once(w, "reviewed_candidate_no_pass_3: 026eecf6ce382c3445ed218aeca80dcf2fb9a426\n", "reviewed_candidate_no_pass_3: 026eecf6ce382c3445ed218aeca80dcf2fb9a426\nreviewed_candidate_no_pass_4: 42eb89388dc96879157ba92db9e7f3c59f2c0b36\n", "fourth no-pass")
w = replace_once(w, "prior_public_bootstrap: dc22f09fd38dbbfeaeb0160152da9b284654f66e\n", "prior_public_bootstrap: 42eb89388dc96879157ba92db9e7f3c59f2c0b36\n", "prior bootstrap")
w = replace_once(w, "prior_semantic_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426\n", "prior_semantic_candidate: 42eb89388dc96879157ba92db9e7f3c59f2c0b36\n", "prior semantic candidate")
w = replace_once(
    w,
    "prior_f3_qualification_commit: 5362f39107aa3f5760f501c02c66e3d25434cac7\nprior_f3_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F3.md\n",
    "prior_f3_qualification_commit: 5362f39107aa3f5760f501c02c66e3d25434cac7\nprior_f3_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F3.md\nprior_f4_qualification_commit: a2ac5de1928bbfc8e7bf5fb6e1f285ac2b13f3ae\nprior_f4_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F4.md\n",
    "F4 provenance",
)
old_disp = "The independent assembled-candidate review of semantic candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` found seven genuine D4/schema-validation and Stage-F oracle blockers and **no Serious Challenge** to accepted Protocol 6.2 or to the established Protocol 6.3 design. This workplan therefore reopens only Stages B, D, and F at the owning surfaces identified below."
new_disp = "Independent review subsequently falsified candidates `026eecf6ce382c3445ed218aeca80dcf2fb9a426` and `42eb89388dc96879157ba92db9e7f3c59f2c0b36`. The latest review of `42eb89388dc96879157ba92db9e7f3c59f2c0b36` found two remaining blockers: D8-01 still permits same-ID governing-claim/applicability laundering under claimant-authored `WITHIN_ENVELOPE` reconciliation, and current-facing Stage-F preservation/static-sensor evidence is not bound to the exact reviewed candidate. There is **no Serious Challenge** to accepted Protocol 6.2 or to the established Protocol 6.3 design. Stages B, D, and F remain reopened only at these owning surfaces."
w = replace_once(w, old_disp, new_disp, "current disposition")
section = '''## D9 independent-review repair delta — candidate `42eb8938...`

The D8 repair is retained except where this section strengthens D8-01 and Stage-F candidate binding. F2/F3/F4 records remain immutable historical evidence; none may be treated as current acceptance after the semantic candidate changes.

### B4.8 Same-ID reconciliation must be mechanically bounded and health-realized

Owner: the existing `source/project_engineering_memory.py` semantic-reconciliation and material-route path. Do not add a second registry/resolver/compliance layer.

A claimant-authored `classification: WITHIN_ENVELOPE` is not evidence that a materially changed family retained identity. Schema-1 same-ID continuation is mechanically admissible only for changes that are demonstrably non-material at the supported representation boundary: editorial normalization of the governing claim that preserves normalized meaning, or applicability narrowing whose normalized new applicability set is a subset of the previous set. Changes to kind, owner class, mechanism family, normalized governing claim, applicability dimensions, or applicability broadening/change-of-regime are mechanically material and require a new/successor/split/merge/reclassified identity with lineage.

Even mechanically admissible editorial/narrowing continuation still requires `semantic_reconciliation` to bind the previous semantic signature, `WITHIN_ENVELOPE`, a reason, and durable evidence. Reconciliation evidence is a material family warrant: it SHALL use the ordinary evidence-route realization path, SHALL be `HEALTHY` for a passing same-ID reconciliation, and SHALL participate in family-level binding-health realization through the existing material-route set. Syntax-only evidence is insufficient.

**Required discriminators:** same-ID mechanism/owner/kind changes fail; governing-claim replacement fails even with a self-authored `WITHIN_ENVELOPE` record; applicability broadening fails even with that record; normalized editorial-only claim change with healthy evidence may pass; true applicability narrowing with healthy evidence may pass; allowed narrowing/editorial reconciliation with an absent/unhealthy locator fails; reconciliation evidence appears in ordinary material-route/binding-health evaluation.

Owning rows: Q63-71, F63-BB, T112, plus Q63-06/T86 where reconciliation warrant health is material.

### D9.1 Repair the false-positive D8-01 qualification oracle

Expand the existing independent-review repair test rather than adding parallel qualification machinery. The executable D8-01 discriminator SHALL directly exercise governing-claim replacement, applicability broadening, valid narrowing/editorial continuation, and unhealthy reconciliation evidence in addition to the already-covered kind/owner/mechanism class. Q63-71/F63-BB cannot inherit F4 PASS unless these counterfactuals discriminate against the exact repaired candidate.

### F4.8 Exact candidate binding for current-facing Stage-F evidence

After the repaired semantic candidate is committed, refresh the current-facing Protocol 6.3 preservation census, static activation sensor record, implementation-state record, F5 qualification result, and independent-review handoff to that exact immutable candidate. Recompute or mechanically recheck static active-set bytes against the exact candidate; do not merely relabel old measurements. Prior candidate identities remain historical provenance only. The qualification publication must distinguish semantic candidate, replacement public bootstrap, later publication/qualification descendant, and unavailable Protocol 6.3 recovery.

Because this D9 repair changes canonical validator semantics after bootstrap `42eb89388dc96879157ba92db9e7f3c59f2c0b36`, that bootstrap becomes historical. Apply the existing self-reference-safe replacement rule: first create and validate the new immutable candidate, then publish that exact already-existing snapshot only from a later descendant. Recovery, accepted-current promotion, workplan archive, and `main` cutover remain Stage-G-blocked.

**Gate D9/F5:** focused D9 discriminators pass; full repository regression, self-hosted PEM validation, source/package/dist checks, Protocol 6.3 profile/snapshot parity, Orchestrator Core acceptance, frozen prior-resource checks, and candidate-bound static sensor verification pass; current-facing evidence names one exact candidate; fresh independent assembled-candidate Review remains the next gate.

'''
w = replace_once(w, "## Current next action\n", section + "## Current next action\n", "D9 insertion marker")
w = replace_once(
    w,
    "Implement B4.1-B4.7 in the existing PEM validator/reconciliation/renderer, add D8.1-D8.7 executable discriminators, run the affected/full acceptance surface, then bind a repaired immutable candidate. Stage G remains blocked until the resulting candidate passes fresh independent Review.",
    "Implement B4.8/D9.1 in the existing reconciliation/material-route path, rerun the affected/full acceptance surface, bind a new immutable candidate, publish candidate-bound F5 evidence from a later descendant, and hand that exact candidate to fresh independent Review. Stage G remains blocked until that Review passes.",
    "current next action",
)
wp.write_text(w)
run("git", "diff", "--check")
run("git", "add", str(wp.relative_to(ROOT)))
run("git", "commit", "-m", "Reopen Protocol 6.3 for D9 reconciliation repair")

# 2. Repair the existing validator/material-route owner and the falsified D8-01 oracle.
src = ROOT / "source" / "project_engineering_memory.py"
s = src.read_text()
old_routes = '''    counterevidence = family.get("counterevidence_search")
    if isinstance(counterevidence, dict):
        routes.extend(str(v) for v in counterevidence.get("evidence", []) if isinstance(v, str))
    return routes
'''
new_routes = '''    counterevidence = family.get("counterevidence_search")
    if isinstance(counterevidence, dict):
        routes.extend(str(v) for v in counterevidence.get("evidence", []) if isinstance(v, str))
    reconciliation = family.get("semantic_reconciliation")
    if isinstance(reconciliation, dict):
        routes.extend(str(v) for v in reconciliation.get("evidence", []) if isinstance(v, str))
    return routes
'''
s = replace_once(s, old_routes, new_routes, "material routes")
old_recon = '''def _semantic_identity_signature(family: dict[str, Any]) -> str:
    payload = {"kind": family.get("kind"), "semantic_identity": family.get("semantic_identity"), "applicability": family.get("applicability")}
    return hashlib.sha256(yaml.safe_dump(payload, sort_keys=True).encode("utf-8")).hexdigest()


def validate_reconciliation(previous: PemDocument, current: PemDocument) -> list[str]:
    """Reject silent accepted semantic drift and observation rewriting across representations."""
    errors: list[str] = []
    for fid in previous.families.keys() & current.families.keys():
        old_family = previous.families[fid]; new_family = current.families[fid]
        old_sig = _semantic_identity_signature(old_family); new_sig = _semantic_identity_signature(new_family)
        if old_sig != new_sig:
            old_semantic = old_family.get("semantic_identity") if isinstance(old_family.get("semantic_identity"), dict) else {}
            new_semantic = new_family.get("semantic_identity") if isinstance(new_family.get("semantic_identity"), dict) else {}
            mechanically_material = []
            if old_family.get("kind") != new_family.get("kind"):
                mechanically_material.append("kind")
            for key in ("owner_class", "mechanism_family"):
                if old_semantic.get(key) != new_semantic.get(key):
                    mechanically_material.append(key)
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
                        try: parse_evidence_route(raw, f"{fid}:semantic reconciliation evidence")
                        except PemError as exc: errors.append(str(exc))
    old_rows = _all_event_rows(previous); new_rows = _all_event_rows(current)
'''
new_recon = '''def _semantic_identity_signature(family: dict[str, Any]) -> str:
    payload = {"kind": family.get("kind"), "semantic_identity": family.get("semantic_identity"), "applicability": family.get("applicability")}
    return hashlib.sha256(yaml.safe_dump(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _normalized_semantic_text(value: Any) -> str:
    """Normalize presentation-only text differences without inferring semantic equivalence."""
    if isinstance(value, str):
        return re.sub(r"[\\W_]+", " ", value, flags=re.UNICODE).strip().casefold()
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
'''
s = replace_once(s, old_recon, new_recon, "reconciliation validator")
src.write_text(s)

tp = ROOT / "tests" / "test_protocol_63_independent_review_repairs.py"
t = tp.read_text()
old_test = '''    def test_d8_01_same_id_semantic_drift_rejected(self):
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
'''
new_test = '''    def _reconciliation_route(self, locator="def validate_reconciliation"):
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
'''
t = replace_once(t, old_test, new_test, "D8-01 discriminator")
tp.write_text(t)

run("git", "diff", "--check")
run("git", "rm", ".github/workflows/temporary-protocol63-d9-repair.yml", "qualification/ssdp6/temporary_d9_repair.py")
run("git", "add", "source/project_engineering_memory.py", "tests/test_protocol_63_independent_review_repairs.py")
run("git", "commit", "-m", "Repair Protocol 6.3 same-ID reconciliation validation")
candidate = out("git", "rev-parse", "HEAD")

# 3. Qualify the immutable candidate before publication.
run("python", "-m", "unittest", "tests.test_protocol_63_independent_review_repairs", "-v")
run("python", "-m", "unittest", "discover", "-s", "tests", "-v")
run("python", "source/project_engineering_memory.py", "PROJECT-ENGINEERING-MEMORY.md")
run("python", "source/build_skills.py", "--output", "/tmp/protocol-dist")
run("python", "source/validate_packages.py", "--dist", "/tmp/protocol-dist")
run("python", "source/check_dist.py", "--expected", "/tmp/protocol-dist", "--committed", "dist")
run("python", "-m", "pip", "install", "./orchestrator", "-r", "orchestrator/requirements-dev.txt")
run("python", "orchestrator/scripts/generate_protocol_snapshot.py", "--check")
run("python", "orchestrator/scripts/run_core_tests.py")
run("git", "diff", "--check", f"{candidate}^", candidate)
if out("git", "status", "--porcelain"):
    raise SystemExit("candidate qualification dirtied the worktree")

sensor = QDIR / "SSDP-6.3-STATIC-ACTIVATION-SENSORS.md"
sensor_text = sensor.read_text()
tail = sensor_text.split("## 6.3 active sets", 1)[1]
sections = re.split(r"(?m)^### ", tail)[1:]
checked = 0
for block in sections:
    heading = block.splitlines()[0]
    m_expected = re.search(r"- active bytes: ([0-9,]+);", block)
    m_paths = re.search(r"(?m)^- active: (.+)$", block)
    if not m_expected or not m_paths:
        continue
    paths = re.findall(r"`([^`]+)`", m_paths.group(1))
    actual = sum((ROOT / path).stat().st_size for path in paths)
    expected = int(m_expected.group(1).replace(",", ""))
    if actual != expected:
        raise SystemExit(f"{heading}: documented active bytes {expected}, exact-candidate bytes {actual}")
    checked += 1
if checked != 11:
    raise SystemExit(f"expected 11 static active-set traces, checked {checked}")
print(f"verified {checked} exact-candidate static active-set byte totals")

# 4. Publish current-facing F5 evidence from a later descendant.
sensor_text = replace_once(sensor_text, "semantic_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426", f"semantic_candidate: {candidate}", "sensor candidate")
sensor_text = replace_once(sensor_text, "F3 owner-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` and remain unchanged. Every 6.3 byte total below was recomputed from the exact candidate files named by that fixed active set; no F2 candidate-side byte total is carried forward as current evidence.", f"F5/D9 candidate-binding refresh: the active-set predicates/topology were rechecked against repaired semantic candidate `{candidate}` and remain unchanged. Every 6.3 byte total below was mechanically remeasured from the exact candidate files named by that fixed active set; all eleven totals match the table. No F2/F3/F4 candidate-side identity is carried forward as current evidence.", "sensor refresh paragraph")
sensor.write_text(sensor_text)

census = QDIR / "SSDP-6.3-PRESERVATION-CENSUS.md"
c = census.read_text()
c = replace_once(c, "semantic_candidate: 3bbbdfa8120646d76336c7b916e6a891c9ed38f2", f"semantic_candidate: {candidate}", "census candidate")
if "status: f2-qualified-independent-review-pending" in c:
    c = c.replace("status: f2-qualified-independent-review-pending", "status: f5-qualified-independent-review-pending", 1)
c += f"\n\n## F5 / D9 preservation refresh\n\nExact repaired semantic candidate: `{candidate}`. D9 narrows same-ID reconciliation validation and adds reconciliation evidence to the existing material-route health path; it does not alter D1-D3 authority, accepted Protocol 6.2 T01-T39 semantics, cold-route activation topology, frozen 5.16/6.0/6.1/6.2 resources, or package/profile ownership. F2/F3/F4 candidate identities remain historical evidence only. Static activation active sets were mechanically rechecked against this exact candidate with all documented candidate-side byte totals unchanged. Stage G and Protocol 6.3 recovery remain blocked pending fresh independent Review.\n"
census.write_text(c)

state = QDIR / "IMPLEMENTATION-STATE-PROTOCOL-6.3.md"
state.write_text(f'''---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: f5-implementation-qualification-complete-independent-review-pending
accepted_current_protocol: 6.2.0
accepted_rollback_commit: {BASELINE}
semantic_candidate: {candidate}
protocol_63_public_bootstrap: {candidate}
protocol_63_public_bootstrap_mapping: PENDING_F5_PUBLICATION_BINDING
stage_f_static_sensor_commit: PENDING_F5_PUBLICATION_BINDING
stage_f_qualification_commit: PENDING_F5_PUBLICATION_BINDING
stage_f_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md
independent_review: pending_fresh_context
protocol_63_recovery: unavailable_pending_independent_review
---

# Protocol 6.3 Implementation State

## Current disposition

Protocol 6.3 D9 implementation-context repair is complete for immutable semantic candidate `{candidate}`. Protocol 6.2 remains accepted-current at recovery `{BASELINE}`. This record does not claim independent Review PASS, Protocol 6.3 recovery, lifecycle acceptance, workplan closure, or `main` cutover.

The F2/F3/F4 candidates and qualification records remain immutable historical evidence. Independent Review of F4 candidate `{OLD_CANDIDATE}` falsified the D8-01 oracle and found stale current-facing candidate bindings; those PASS labels do not establish current acceptance.

## D9 repair closure

The existing reconciliation path now treats changed kind, owner class, mechanism family, normalized governing claim, applicability dimensions, and applicability broadening/change as mechanically material same-ID drift requiring lineage. Only mechanically demonstrable presentation normalization or true applicability narrowing may reach `WITHIN_ENVELOPE` reconciliation, and those cases still require durable `HEALTHY` evidence. Reconciliation evidence is included in ordinary material-route/binding-health realization. The focused D8-01 test now falsifies governing-claim laundering, applicability broadening, applicability-dimension replacement, unhealthy reconciliation evidence, and confirms valid narrowing/editorial continuation.

## F5 qualification

The exact candidate passed the focused D9 repair tests, full repository unittest discovery, self-hosted PEM validation, canonical build/package/dist validation, Protocol 6.3 snapshot check, Orchestrator Core acceptance, whitespace checks, and exact-candidate remeasurement of all eleven static activation active sets. Frozen prior-version/resource invariants remain covered by the full repository and Orchestrator acceptance surfaces.

The D9 source mutation makes prior public bootstrap `{OLD_CANDIDATE}` historical. The exact already-existing candidate `{candidate}` is published as the replacement 6.3 source fallback only by the later F5 evidence descendant; it remains distinct from unavailable Protocol 6.3 recovery.

## Remaining gate

Fresh independent assembled-candidate Protocol/D3 Review of `{candidate}` is required. Stage G, recovery, accepted-current promotion, workplan archive, and `main` cutover remain blocked until that Review passes.
''')

run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
result = QDIR / "RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md"
result.write_text(f'''---
kind: ssdp63-f5-d9-repair-qualification-result
protocol_version: 6.3.0
candidate_under_test: {candidate}
accepted_protocol_62_recovery: {BASELINE}
public_source_bootstrap: {candidate}
replaces_public_source_bootstrap: {OLD_CANDIDATE}
prior_f4_candidate: {OLD_CANDIDATE}
independent_review: pending
authority: non-normative-qualification-evidence
stage_g: blocked
---

# Protocol 6.3 F5 D9 Repair Qualification

## Disposition

**IMPLEMENTATION-CONTEXT REPAIR QUALIFICATION PASS** for immutable semantic candidate `{candidate}`. This is not independent Review PASS, recovery, accepted-current promotion, workplan closure, or `main` cutover.

## D9 repaired blockers

1. **D9-01 / D8-01 oracle and validator:** same-ID governing-claim replacement, applicability-dimension replacement, or applicability broadening/change is mechanically material and cannot be laundered by claimant-authored `WITHIN_ENVELOPE`. Mechanically admissible editorial normalization or true applicability narrowing still requires previous-signature binding, reason, and durable `HEALTHY` evidence. Reconciliation evidence participates in the ordinary family material-route/binding-health path.
2. **D9-02 / Stage-F exact binding:** preservation census, static activation sensors, implementation state, this F5 record, and the following independent-review handoff are rebound to `{candidate}`. F2/F3/F4 remain historical evidence.

## Executed evidence

GitHub Actions run `{run_id}` executed the focused D9 tests, complete repository regression, self-hosted PEM validation, canonical build/package/dist checks, Protocol 6.3 snapshot check, Orchestrator Core acceptance, whitespace checks, and mechanical remeasurement of all eleven Protocol 6.3 static activation active sets against the exact candidate. The temporary execution workflow and repair script are absent from the candidate tree.

## Bootstrap lifecycle

Candidate `{candidate}` existed and passed the assembled acceptance surface before this descendant publication. This F5 descendant publishes that exact immutable snapshot as the replacement public-source bootstrap. The previous `{OLD_CANDIDATE}` bootstrap is historical because canonical validator semantics changed. The source bootstrap remains fallback-only and is not Protocol 6.3 recovery.

## Remaining lifecycle gate

Fresh independent assembled-candidate Review is required. Accepted current remains Protocol 6.2 recovery `{BASELINE}`; Stage G and Protocol 6.3 recovery remain blocked.
''')

run("git", "diff", "--check")
run("git", "add", str(sensor.relative_to(ROOT)), str(census.relative_to(ROOT)), str(state.relative_to(ROOT)), str(result.relative_to(ROOT)))
run("git", "commit", "-m", "Qualify Protocol 6.3 D9 repaired candidate")
qualification = out("git", "rev-parse", "HEAD")

# 5. Bind the publication descendant into current state/workplan and issue the fresh handoff.
st = state.read_text().replace("PENDING_F5_PUBLICATION_BINDING", qualification)
state.write_text(st)

c = census.read_text()
for old, new in [
    ("public_source_bootstrap: e12572c021087308570abfa41657a910c6896457", f"public_source_bootstrap: {candidate}"),
    ("public_source_mapping_commit: e6a8c12f065c3d25a41da804c129d6bc0a4f7b50", f"public_source_mapping_commit: {qualification}"),
    ("stage_f_static_sensor_commit: 6fc26ce374b5346495782871d5d7241de5b90071", f"stage_f_static_sensor_commit: {qualification}"),
    ("stage_f_qualification_commit: 6fc26ce374b5346495782871d5d7241de5b90071", f"stage_f_qualification_commit: {qualification}"),
]:
    if old in c:
        c = c.replace(old, new, 1)
census.write_text(c)

w = wp.read_text()
anchor = "prior_f4_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F4.md\n"
w = replace_once(w, anchor, anchor + f"current_f5_semantic_candidate: {candidate}\ncurrent_f5_qualification_commit: {qualification}\ncurrent_f5_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md\n", "workplan F5 metadata")
w = replace_once(
    w,
    "Implement B4.8/D9.1 in the existing reconciliation/material-route path, rerun the affected/full acceptance surface, bind a new immutable candidate, publish candidate-bound F5 evidence from a later descendant, and hand that exact candidate to fresh independent Review. Stage G remains blocked until that Review passes.",
    f"D9 implementation and F5 qualification are complete for immutable candidate `{candidate}` with publication evidence at `{qualification}`. Perform a fresh independent assembled-candidate Review of that exact candidate against accepted Protocol 6.2 and this active workplan. Stage G remains blocked until Review PASS.",
    "completed current next action",
)
wp.write_text(w)

handoff = QDIR / "INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md"
handoff.write_text(f'''---
kind: ssdp63-independent-review-handoff
protocol_version: 6.3.0
authority: non-normative-review-handoff
semantic_candidate: {candidate}
qualification_result_commit: {qualification}
qualification_result: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md
public_source_bootstrap: {candidate}
public_source_mapping_commit: {qualification}
replaced_public_source_bootstrap: {OLD_CANDIDATE}
accepted_protocol_62_recovery: {BASELINE}
accepted_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
accepted_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
independent_review: required_fresh_context
protocol_63_recovery: unavailable_pending_review
accepted_current_protocol: 6.2.0
stage_g: blocked
---

# Independent Protocol/D3 Review Handoff — Protocol 6.3 D9 Candidate

## Reviewer mandate

Perform a fresh independent assembled-candidate Protocol/D3 Review of immutable semantic candidate `{candidate}` against accepted Protocol 6.2 recovery `{BASELINE}` and the active Protocol 6.3 workplan. Do not inherit F5, this handoff, green CI, or prior Review conclusions as authority.

The immediately preceding Review of candidate `{OLD_CANDIDATE}` returned NO-PASS with two blockers and no Serious Challenge: a D8-01 false-pass for governing-claim/applicability same-ID laundering, and stale current-facing Stage-F candidate bindings. Candidate `{candidate}` is intended to close exactly those blockers without broadening architecture.

## D9 repairs to re-falsify

### D9-01 — same-ID semantic reconciliation

Attempt same-ID changes to kind, owner class, mechanism family, governing claim, applicability dimensions, and applicability. Claim replacement and applicability broadening/change-of-regime must require new/reclassified identity with lineage and must not be launderable by `WITHIN_ENVELOPE`. Mechanically demonstrable editorial-only normalization or true applicability narrowing may retain the ID only with the previous signature, reason, and durable `HEALTHY` reconciliation evidence. Break that evidence locator and confirm reconciliation/binding health cannot pass.

### D9-02 — exact candidate-bound qualification evidence

Confirm preservation census, static activation sensors, implementation state, F5 qualification, and this handoff all bind `{candidate}` as the current semantic candidate. F2/F3/F4 identities must remain historical only. Confirm all eleven static activation active-set byte totals match exact candidate files and frozen 5.16/6.0/6.1/6.2 resources remain unchanged.

## Evidence to challenge

F5 publication commit is `{qualification}`. It reports focused D9 tests, full repository regression, self-hosted PEM validation, package/dist parity, Protocol 6.3 snapshot parity, Orchestrator Core acceptance, whitespace, and exact-candidate static active-set remeasurement. Treat it as evidence, not Review authority.

Reconstruct the still-binding complete design through the active workplan's immutable reference to `5de67c6a9509c1ede9104badc3ddae468c988311`, including T01-T120, D1-D9, Q63/F63, bootstrap/recovery separation, cold-route/progressive-disclosure behavior, source/generated/package/profile parity, frozen prior-version resources, and all four inherited Challenge dimensions: Loss, scope/materiality laundering, priority inversion, and false compaction.

## Lifecycle boundary

The new public source bootstrap is the already-existing candidate `{candidate}`, published only by later descendant `{qualification}`. It is not Protocol 6.3 recovery. Until fresh independent Review PASS and separate Stage G recovery lifecycle complete, accepted current remains Protocol 6.2; recovery is unavailable; the workplan stays active; `main` cutover is not authorized.
''')

run("git", "diff", "--check")
run("git", "add", str(state.relative_to(ROOT)), str(census.relative_to(ROOT)), str(handoff.relative_to(ROOT)), str(wp.relative_to(ROOT)))
run("git", "commit", "-m", "Hand off Protocol 6.3 D9 candidate for independent review")
run("git", "push", "origin", f"HEAD:{BRANCH}")
print(f"semantic candidate: {candidate}")
print(f"F5 qualification publication: {qualification}")
print(f"final handoff head: {out('git', 'rev-parse', 'HEAD')}")
