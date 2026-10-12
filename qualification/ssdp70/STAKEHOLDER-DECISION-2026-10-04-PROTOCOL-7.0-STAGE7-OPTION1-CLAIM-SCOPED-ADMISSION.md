---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date_utc: 2026-10-04
status: stakeholder-adopted
---

# Stage 7 — Adoption of Option 1: Proceed under Claim-Scoped Inadmissibility

The stakeholder formally adopted **Option 1** upon review of the Comprehensive Stage 7 Independent Inspection and Admission Report: **“Option 1.”**

This decision authorizes proceeding with blind evaluator assessment (`assess70.py`) of the frozen 244-run realizations under the claim-scoped qualification boundary, retaining `check custody_denial` as `UNRESOLVED` under fail-closed SSDP 6.6.0 semantics.

---

## 1. Adopted Scope & Governance

1. **Acceptance of Campaign Status (34 PASS / 1 UNRESOLVED):**
   - The Stage 7 admission campaign at `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261004T002409Z-d4572470db98-staging-repair-411510ed96c0` is accepted in its verified, sealed state.
   - All 34 passing cells (10 exact-profile checks, 11 deterministic falsifications, and 13 independent inspections) stand as cryptographically verified and bound.
   - `check custody_denial` remains formally **UNRESOLVED / NO-PASS**.

2. **Mandatory Disclosure of Unauditable Reads (Contract §1 Item 9 Condition (d)):**
   - On this local execution host, all operations execute under a single user identity (`samjin`, UID 1000). The host kernel provides no mechanical read-auditing facility (such as IMA/auditd or hardware memory tagging) to verify whether non-executor processes opened withheld custody holdouts.
   - Filesystem `atime` metadata was updated by prior hash verifications (`sha256sum`), permanently precluding retrospective read reconstruction.
   - In accordance with qualification contract §1 item 9 condition (d), this unauditable-read residual is acknowledged and must be explicitly stated in all dependent admission and qualification reports.

3. **Claim-Scoped Inadmissibility Boundary:**
   - Under qualification contract §1, the candidate execution profile (`d4572470db98e704c05c5eb111a8e9916cb77c3da85e5252e9b981d490e80b76`) is **claim-scoped inadmissible** for qualification claims that strictly depend upon a mechanically audited custody holdout.
   - The profile remains admissible for executor containment, tool tracing, and comparative semantic performance within the demonstrated boundaries.
   - Automated candidate admission bundle emission (`emit-candidate`) remains blocked fail-closed; no artificial PASS is manufactured.

4. **Authorization of Blind Evaluator Scoring:**
   - Evaluator assessment via `qualification/ssdp70/eval/assess70.py` is authorized across the frozen 244-run realizations (`semantic-runs/20261004T050108Z/`).
   - All assessments must be executed on isolated copies of run directories, preserving the frozen realization tree unmodified and sealed under `FREEZE.sha256`.
   - The evaluator must operate strictly through the admitted read-only adapter `omp_eval` (`profile-admission.json`, status `ADMITTED`) with network and credential denial enforced.

---

## 2. Preserved Baselines & Invariants

- **Baseline Custody Tree:** `/home/samjin/ssdp70-omp-stagef/semantic-custody-20261003T161129.024432Z/` remains frozen and unmodified (verified 423/423 entries OK).
- **Gate A Record:** Fixture custodian F-12 classification in `custody-successors/OMP-STAGE7-F12-CLASSIFICATION-20261004T041512.937091Z/` (MANIFEST digest `5d7c120ad503107810311af23cd666ce71ca24652edd1c086e41b314dbc01c5e`) remains binding. F-12 is treated as non-blind development data.
- **Gate B Record:** Evaluator admission in `admission/evaluator-omp-admission-20261004T000000Z/profile-admission.json` remains binding.
- **C1 Binding:** Write and unauthorized-write oracles derive target paths strictly from retained input/result headers and host `diff.patch`, never from normalizer `workspace_external_class` or `disposition`.
- **Project Engineering Memory (PEM):** Base `main` at `2585b73f00420daca185a4fbb9ac42a79473eda1`, PEM blob `1561797125622f355f84eb27319f87e8fa4227d9`. Schema 1 valid (5 families, 0 notices). Task HAS: `PC-001` APPLICABLE, `DS-001` APPLICABLE, `FF-001`/`SP-001`/`SP-002` NOT_APPLICABLE.
