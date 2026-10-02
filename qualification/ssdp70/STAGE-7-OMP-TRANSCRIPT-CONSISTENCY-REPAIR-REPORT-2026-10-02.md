# OMP Stage 7 Transcript-Consistency Repair and Campaign Closure Report

**Date:** 2026-10-02

**Governing protocol:** Scientific Software Development Protocol (SSDP) 6.6.0

**Disposition:** Candidate evidence closure; runner admission remains open for independent review (`CANDIDATE`).

---

## 1. Scope and Status Terms

This report records the D4 transcript-consistency and prelaunch secret screening repairs, the reconciliation of tool digests, and the fresh append-only Stage 7 candidate campaign execution.
- **OMP**: Headless runner identified by the qualification contract and frozen profile.
- **Arms**: `p66` (Protocol 6.6.0 comparison arm) and `p70` (candidate semantic subject).
- **`COMPLETE_ADMISSIBLE`**: A run has complete, untruncated, admissible realization evidence satisfying all contract constraints; does not denote runner admission.
- **`NOT_EVALUATED`**: Qualification scoring was not performed (probe mode).
- **`CANDIDATE`**: Profile evidence is complete and admissible for review; runner admission has not been self-authorized.

---

## 2. Candidate and Execution Profile

- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Candidate starting head:** `d2feaa4e792d7edf9c0ee77591f85ad22b6f1dd4`
- **Implementation commit:** `55f2a6275632af86d26c52ac25907fcc3185d80b`
- **Immutable semantic subject:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p66 arm commit:** `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- **p66 package-tree SHA-256:** `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`
- **p70 arm commit:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p70 package-tree SHA-256:** `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`
- **Frozen OMP profile ID:** `omp-headless-deepinfra-glm53-flash-stage7-transcriptfixed-d2feaa4e792d7edf9c0ee77591f85ad22b6f1dd4`
- **Frozen OMP profile key:** `c42206dace0cc46453761cff0b0efe5f5519b3a3a85058d43e8efdf301336416`
- **Frozen profile document SHA-256:** `138a565b3f6d44876341f4d731cb0071c7f8b2730c4b4fbd1ece771ba3d0e971`
- **Adapter (`adapters/omp.py`) SHA-256:** `7d54512374009c560d9169c54d2f8e0af5fb066b771247ba9e4a969d4b608747`

---

## 3. Root Cause Investigation of Transcript Discrepancy

### Investigation and Executable Evidence
In the prior campaign run (`OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix`), realization `S7-ORD-VARIANT-p66-r0` failed with the diagnostic:
`native message events do not equal agent_end's complete transcript: dropped, reordered or duplicated events`

Analysis of the retained trace (`positive-matrix/S7-ORD-VARIANT-p66-r0/trace.jsonl`) and reverse engineering of the OMP 18.0.11 executable binary established:
1. **OMP In-Memory Compaction:** OMP 18.0.11 implements in-memory session compaction (`pruneSupersededToolResults` in `packages/agent/src/compaction.ts`). When a file is read again after an edit, earlier in-memory `toolResult` payloads for that file are compacted to reduce model prompt tokens, replacing the text with `"[Superseded by a newer read of this file]"` and affixing a `prunedAt: <timestamp>` field.
2. **Representation Roles:**
   - Real-time `message_end` events emit the raw, uncompacted tool execution result as observed at execution time (168 chars in message index 5).
   - `agent_end.messages` emits the final state of OMP's internal in-memory conversation array after compaction passes (41 chars + `prunedAt` timestamp).
   - The two records are **not intended to be byte-identical**.
   - All 31 message roles, `toolCallId`s, and stop reasons were 100% identical and in the exact same sequence.
3. **No Event Loss:** `message_end` preserves the complete, untruncated raw record required by Qualification Contract §4 and §5. No events were dropped, reordered, duplicated, or corrupted.
4. **Adapter Causal Misdiagnosis:** The existing adapter treated any string divergence between `message_end` and `agent_end.messages` as `"dropped, reordered or duplicated events"`.

---

## 4. D4 Implementation Repairs

### Adapter Repair (`qualification/ssdp70/eval/adapters/omp.py`)
- Implemented `_is_valid_omp_tool_result_pruning(m_end, a_end)`:
  - Requires matching roles (`toolResult`), matching `toolCallId`, and matching call metadata.
  - Requires presence of a valid integer `prunedAt > 0` in `agent_end`.
  - Restricts allowed compacted content to recognized native OMP compaction notices (`OMP_PRUNED_TOOL_RESULT_NOTICES = {"[Superseded by a newer read of this file]", "[Uneventful result elided]"}`).
  - Ensures the authoritative, unpruned content remains preserved in `message_end`.
- Replaced the unsupported causal wording with cause-neutral diagnostics:
  - `"message count mismatch (message_end: N, agent_end: M)"`
  - `"message {idx} identity mismatch (role/toolCallId/stopReason)"`
  - `"message {idx} content mismatch (unauthorized tool result mutation or missing prunedAt)"`
- True event drops, reordering, unauthorized mutations, or unrecorded truncations remain strictly rejected fail-closed.

### Campaign Prelaunch Secret Hardening (`qualification/ssdp70/eval/omp_stage7_campaign.py`)
- Hardened `_run` and introduced `PrelaunchSecretSnapshot` / `_prelaunch_diagnostic_secret_snapshot`:
  - Before subprocess launch, dynamically resolves the profile credential variable name, sensitive environment variables (`*KEY*`, `*TOKEN*`, `*SECRET*`, `*CREDENTIAL*`, `*API*`), and all multi-encoding scrub patterns (raw, UTF-16LE, Base64, URL-safe Base64, hex, JSON/HTML/shell escapes).
  - Child process launch is refused fail-closed if secret derivation or pattern compilation fails.
  - Captured stdout/stderr streams and failure diagnostics are screened against the frozen prelaunch snapshot, protecting against credential leakage even if child processes alter the environment.
  - Maintains strict diagnostic-only exclusion from runner admission evidence.

---

## 5. Source and Evidence Digest Reconciliation

- **Commit `d2feaa4` Tool Digests:**
  - `qualification/ssdp70/eval/omp_stage7_campaign.py` SHA-256: `9d739b6871dd39a57df0e93cea78836dd3dc77f6e20d2503aec214e76d5991be`.
  - `qualification/ssdp70/eval/omp_stage7_admission.py` SHA-256: `e5d5059f67c0bae6449f5d5c3ea3077b96716aac28ff631fc31c9143080ead77`.
  - Both digests were verified byte-identical to the values recorded in campaign `OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix`.
- **Profile Key Update:**
  - Modifying `adapters/omp.py` updated `execution_support_sha256["adapters/omp.py"]` to `7d545123...`.
  - Because `omp.profile_errors` enforces that `containment_policy.execution_support_sha256` matches the running adapter, the profile key updated to `c42206dace0cc46453761cff0b0efe5f5519b3a3a85058d43e8efdf301336416`.
  - Prior provider evidence bound to `5754fb5ec39a...` was marked stale and preserved. A fresh profile was frozen and a fresh append-only campaign initialized.

---

## 6. Fresh Real-Provider and Campaign Realizations

1. **Append-Only Probe Realization:**
   - Path: `$HOME/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-TRANSCRIPTFIX-20261002T041334.179954Z-93e0ea2c5896`
   - Run identity: `cd8c785d99d12a0fb273cb51c30d701f5e498bf1cbb13207c7598ddfcad7a825`
   - Results: `execution_ok=true`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED`, 0 run validation errors.
   - Reference recorded in campaign root `probe-reference.json`.

2. **Campaign Root:**
   - Path: `$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T040939Z-c42206dace0c-transcriptfix`

3. **Positive Exact-Profile Campaign Matrix:**
   - Path: `runs/exact-profile-20261002T041708.047019Z-087a9dada5`
   - Execution status: **`PASS`** (`positive_matrix_returncode=0`).
   - All 34 realizations across `p66` and `p70` produced **`COMPLETE_ADMISSIBLE`** evidence.
   - `S7-ORD-VARIANT-p66-r0` succeeded cleanly with valid native tool result pruning admitted (`normalized_event_count=35`, 0 normalization completeness errors).
   - `S7-CONTAMINATION-p70-r0` produced the required prelaunch refusal (`reason` containing ambient discovery `.mcp.json` refusal, `subject_launched=false`, returncode 2).
   - Scheduler trace validation: passed with 0 errors (sequential arms within pairs, verified concurrent-pair overlap across all 17 pairs at parallel=2).

4. **Deterministic Falsification Matrix:**
   - Path: `falsification/core-20261002T043349.795364Z-b4a8244768/deterministic-falsification.json`
   - Base run: `positive-matrix/S7-ORD-D4-p70-r0` (`057c5f24106c2c74f4d289ebc94935ecbcb7317b3c0246e91291f4afef2f5821`).
   - Outcome: **`status="PASS"`** across all 11 perturbation and rejection test cases.

5. **Post-Run Credential Scan:**
   - Scanned 2,531 files (154,420,832 bytes) across the entire campaign root. Zero leaks or secret matches detected.

---

## 7. Status of Executor Checks and Section 6 Cells

### 12 Executor Admission Checks

| Check | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `exact_subject_profile_identity` | `exact-profile-behavior` | **PASS** | `proofs/check-exact_subject_profile_identity-20261002T043418.632625Z-46456a6c.json` |
| `fresh_arm_isolation` | `exact-profile-behavior` | **PASS** | `proofs/check-fresh_arm_isolation-20261002T043427.578494Z-c2e1ea9e.json` |
| `capability_manifest` | `exact-profile-behavior` | **PASS** | `proofs/check-capability_manifest-20261002T043428.158886Z-5b382f14.json` |
| `raw_normalized_completeness` | `exact-profile-behavior` | **PASS** | `proofs/check-raw_normalized_completeness-20261002T043428.735929Z-0a46e40b.json` |
| `fail_closed_evidence` | `deterministic-falsification` | **PASS** | `proofs/check-fail_closed_evidence-20261002T043431.049229Z-7cdbb7b1.json` |
| `exact_scoring_closure` | `deterministic-falsification` | **PASS** | `proofs/check-exact_scoring_closure-20261002T043431.057512Z-69e72951.json` |
| `cache_profile_core_identity_perturbation` | `deterministic-falsification` | **PASS** | `proofs/check-cache_profile_core_identity_perturbation-20261002T043431.058544Z-abf834f7.json` |
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/check-catalog_contamination-20261002T043429.318204Z-89e60ee6.json` |
| `containment_pre_effect` | `exact-profile-behavior` | **PASS** | `proofs/check-containment_pre_effect-20261002T043429.890351Z-9c63e843.json` |
| `custody_denial` | `exact-profile-behavior` | **PASS** | `proofs/check-custody_denial-20261002T043430.462946Z-400595e4.json` |
| `ordinary_entry_owner_read` | `exact-profile-behavior` | **PASS** | `proofs/check-ordinary_entry_owner_read-20261002T043431.048048Z-37c1d8f8.json` |
| `withheld_oracle_branches` | `independent-inspection` | **PENDING** | *Requires independent evaluator judgment; not self-authorized.* |

### 23 Section 6 Matrix Cells

| Cell | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/section6-catalog_contamination-20261002T043431.637560Z-0d38efe4.json` |
| `containment_escape_attempts_retained` | `exact-profile-behavior` | **PASS** | `proofs/section6-containment_escape_attempts_retained-20261002T043432.219126Z-013f8e4e.json` |
| `ordinary_entry_case_classes` | `exact-profile-behavior` | **PASS** | `proofs/section6-ordinary_entry_case_classes-20261002T043432.795671Z-28cdc87c.json` |
| `issue_network_external_write_standins` | `exact-profile-behavior` | **PASS** | `proofs/section6-issue_network_external_write_standins-20261002T043433.375872Z-8b3a1308.json` |
| `reject_missing_artifact` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_artifact-20261002T043433.377016Z-155dc919.json` |
| `reject_missing_oracle` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_oracle-20261002T043433.385305Z-86e5ff4d.json` |
| `reject_missing_scoring_disposition` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_scoring_disposition-20261002T043433.386315Z-1518ffe9.json` |
| `reject_incomplete_or_failed_termination` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_incomplete_or_failed_termination-20261002T043433.387330Z-bf267f1b.json` |
| `perturb_cache_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_cache_identity-20261002T043433.388336Z-a670b739.json` |
| `perturb_profile_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_profile_identity-20261002T043433.389357Z-16d1b9f2.json` |
| `perturb_core_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_core_identity-20261002T043433.390360Z-f6c2176d.json` |
| `known_broken_both_arms_miss` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_binding_o3` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_null_variant_delegate` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_false_tension_closure_asserter` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_loss_before_destructive_boundary` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_unauthorized_write` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_version_self_adoption` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_legitimate_withholding` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_designed_termination` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `perturb_evaluator_identity` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `final_report_changed_files_tool_trace_assessment` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `chained_delegate_first_look` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |

---

## 8. Verification and Test Results

All tests run on the final candidate checkout:
- **Unit & Regression Suites:** 233 passed in 8.835 seconds across all 9 unit test modules (`test_control_path_policy.py`, `test_harness_integration.py`, `test_mcp_stdio.py`, `test_omp_stage7_admission.py`, `test_omp_stage7_campaign.py`, `test_omp_units.py`, `test_portable70.py`, `test_stage_f_integrity_repairs.py`, `test_stage_f_v4_repairs.py`).
- **Integration Test Suite:** 54 passed in 1,167.474 seconds (`test_omp_integration.py`).
- **Whitespace / Linter Check:** `git diff --check` passed cleanly with 0 errors.

---

## 9. Next Actions

Candidate evidence production is closed. The campaign directory, probe realization, exact-profile matrix runs, deterministic falsification artifacts, and proof records are fully prepared for independent Stage 7 runner-admission evaluation. Profile remains `CANDIDATE`.
