# OMP Stage 7 Transcript-Consistency Repair and Campaign Closure Report

**Date:** 2026-10-02

**Governing protocol:** Scientific Software Development Protocol (SSDP) 6.6.0

**Disposition:** Candidate evidence closure; runner admission remains open for independent review (`CANDIDATE`).

---

## 1. Scope and Status Terms

This report records the D4 repair of the SSDP 7.0 OMP Stage 7 execution profile and transcript-consistency machinery: freezing native stale-result pruning controls, eliminating adapter-side pruning eligibility duplication, re-deriving the exact profile identity, executing a fresh append-only real-provider probe, running the complete positive exact-profile campaign across `p66` and `p70`, executing deterministic falsification, and recording executor admission and Section 6 proof artifacts.
- **OMP**: Headless runner identified by the qualification contract and frozen profile.
- **Arms**: `p66` (Protocol 6.6.0 comparison arm) and `p70` (candidate semantic subject).
- **`COMPLETE_ADMISSIBLE`**: A run has complete, untruncated, admissible realization evidence satisfying all contract constraints; does not denote runner admission.
- **`NOT_EVALUATED`**: Qualification scoring was not performed (probe mode).
- **`CANDIDATE`**: Profile evidence is complete and admissible for review; runner admission has not been self-authorized.

---

## 2. Commits, Candidate, and Execution Profile

- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Candidate starting head:** `b0af78352c8dfaf6c33a3d045d76d1c147306725`
- **Implementation commit:** `d4073e539aee86f62d31acb0a02950a62554ec03`
- **Immutable semantic subject:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p66 arm commit:** `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- **p66 package-tree SHA-256:** `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`
- **p70 arm commit:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p70 package-tree SHA-256:** `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`
- **Frozen OMP profile ID:** `omp-headless-deepinfra-glm53-flash-stage7-nopruning-d4073e539aee86f62d31acb0a02950a62554ec03`
- **Frozen OMP profile key:** `fbb23db56d427a9ce46ff1fc937098bb35b5232163ff9dac002b624332c31d09`
- **Frozen profile document SHA-256:** `249ee75c938199613991f1c5142fa897971fc474c184f6be2fb14f37dc75bb95`
- **Adapter (`adapters/omp.py`) SHA-256:** `a66be1da4fc43c8562885f777763d3b8afc3f43cfbbc37d32362b583d3ee8d66`
- **Subject Launcher (`subject_launcher.py`) SHA-256:** `e6a1c1487c0617908e73db887901b2a850ae2a5ee1b172cc0f7bf55d0936061d`
- **Build Inventory (`omp-build-inventory-18.0.11.json`) SHA-256:** `a770317cced12600ab8e3604a24af226ebc4c329b3043b2acb98662ec77fd428`
- **Campaign harness (`omp_stage7_campaign.py`) SHA-256:** `4e6cd557ec5eb7b6795d22a46835798caa17642c6c94697ac4c9b7e0aaf63bf8`
- **Admission harness (`omp_stage7_admission.py`) SHA-256:** `e5d5059f67c0bae6449f5d5c3ea3077b96716aac28ff631fc31c9143080ead77`
- **Host Execution Environment (bound in profile):**
  - OS Release: Ubuntu 22.04 (`id="ubuntu"`, `version_id="22.04"`, SHA-256: `594d5ddd35aedb47f00d9c34d140017907a5b9f93c975aba125fc924daac5c07`)
  - Kernel: `Linux 6.8.0-138-generic #138~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC x86_64`
  - Supervisor Python: CPython 3.10.12 (executable SHA-256: `a2f33a6e006989270f4340528eb61f8f97366e00a5d1b602ac8672ea44fc56ae`)

---

## 3. Repair of Pruning Controls and Exact Transcript Equality

### Blocking Finding B1: Native Stale-Result Pruning Controls
In OMP 18.0.11, stale-result pruning runs on every turn before the `compaction.enabled` gate is evaluated. The independently active controls that govern this behavior are:
- `compaction.supersedeReads`
- `compaction.dropUseless`

Previously, `omp-build-inventory-18.0.11.json` incorrectly classified these two settings as inert `sub-parameter-of-closed-feature` rows while their effective values remained default `true`. Consequently, OMP mutated `agent_end.messages` in memory by replacing earlier read contents with `"[Superseded by a newer read of this file]"` and injecting `prunedAt` timestamps.

**Repair Actions for B1:**
1. Both controls are explicitly frozen to `false` in `qualification/ssdp70/eval/adapters/omp.py`:
   - `FROZEN_SETTINGS["compaction"]["supersedeReads"] = False`
   - `FROZEN_SETTINGS["compaction"]["dropUseless"] = False`
2. `omp-build-inventory-18.0.11.json` is corrected:
   - `compaction.supersedeReads`: class updated from `sub-parameter-of-closed-feature` to `frozen-closed`, `effective_under_frozen_profile: false`, `frozen_value: false`.
   - `compaction.dropUseless`: class updated from `sub-parameter-of-closed-feature` to `frozen-closed`, `effective_under_frozen_profile: false`, `frozen_value: false`.
   - Row 462 mechanism updated to reflect explicit disabling of both controls.
3. In `qualification/ssdp70/eval/subject_launcher.py`, the pre-launch `effective-settings` probe explicitly parses the effective values of both controls. If either is not `False`, the launcher appends `launcher_refused` and exits immediately with code 98 before launching OMP.
4. The execution profile key and all dependent digests were re-derived, establishing replacement profile key `fbb23db56d42...`.

### Blocking Finding B2: Elimination of Adapter-Side Pruning Eligibility Duplication
Reimplementing OMP's pruning eligibility algorithm (`readToolSupersedeKey`, `splitReadSelector`, protected tool exclusions) inside the adapter created unnecessary duplicate authority and a fragile oracle. With `supersedeReads=false` and `dropUseless=false` verified, OMP preserves identical read tool results across both events.

**Repair Actions for B2:**
1. Removed `_is_valid_omp_tool_result_pruning` and related special-case constants (`OMP_PRUNED_TOOL_RESULT_NOTICES`, `OMP_SUPERSEDED_READ_NOTICE`).
2. Required exact transcript agreement between `message_end` and `agent_end.messages`:
   - Message count must match exactly.
   - Message identity (`role`, `name`, `toolCallId`) must match at every index.
   - Message content must match strictly without mutation.
3. Added fail-closed checks in `adapters/omp.py`:
   - Any message in `message_end` or `agent_end` bearing `prunedAt` is rejected as an unauthorized runtime profile violation.
   - Any message bearing `[Superseded by a newer read of this file]` or `[Uneventful result elided]` is rejected as an unauthorized pruning notice.

---

## 4. Counterfactual and Discriminating Test Coverage

Focused discriminating tests in `qualification/ssdp70/eval/test_omp_units.py` verify all required properties:

1. **`test_compaction_supersede_reads_true_rejected_as_frozen_profile_mismatch`:**
   Proves `compaction.supersedeReads=true` is rejected by `check_runtime_surface` as a frozen profile mismatch.
2. **`test_compaction_drop_useless_true_rejected_as_frozen_profile_mismatch`:**
   Proves `compaction.dropUseless=true` is rejected by `check_runtime_surface` as a frozen profile mismatch.
3. **`test_pruning_controls_verified_through_effective_settings_path_and_launcher_probe`:**
   Proves both controls evaluate to `False` through the real inventory and launcher probe path without generating runtime surface errors.
4. **`test_transcript_consistency_pruning_difference_fails_closed`:**
   Proves a content mismatch between `message_end` and `agent_end.messages` fails transcript consistency fail-closed.
5. **`test_transcript_consistency_pruned_at_bearing_message_fails_closed`:**
   Proves presence of `prunedAt` on either `agent_end` or `message_end` fails closed with an explicit unauthorized `prunedAt` error.
6. **`test_transcript_consistency_both_native_pruning_notices_fail_closed`:**
   Proves both `[Superseded by a newer read of this file]` and `[Uneventful result elided]` fail closed.
7. **`test_transcript_consistency_exact_unchanged_transcripts_pass`:**
   Proves legitimate multiple file reads with exact matching transcripts pass with zero transcript errors.
8. **`test_transcript_consistency_dropped_reordered_truncated_detection_fails_closed`:**
   Proves dropped message events, reordered events, and truncated traces continue to fail closed with precise diagnostics.

---

## 5. Stale Evidence Classification

The following prior campaign evidence is classified as stale and retained append-only:

1. **`OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix`:**
   - **Reason:** Adapter misdiagnosed native in-memory compaction on realization `S7-ORD-VARIANT-p66-r0` as dropped/reordered events. Profile key `5754fb5ec39a...` was superseded.
2. **`OMP-STAGE7-20261002T040939Z-c42206dace0c-transcriptfix`:**
   - **Reason:** While `S7-ORD-VARIANT-p66-r0` succeeded, the pruning admissibility predicate was underconstrained (`prunedAt` not strictly typed as positive int, metadata equality not fail-closed, unauthorized notices permitted, trajectory eligibility not enforced).
3. **`OMP-STAGE7-20261002T063352Z-cb8f358825b2-tightenedpruning` and Probe `OMP-STAGE7-REAL-PROVIDER-TIGHTENEDPRUNING-20261002T063600.692983Z-d79c4f8b230b`:**
   - **Reason:** Active OMP 18.0.11 pruning controls `compaction.supersedeReads` and `compaction.dropUseless` were default `true` rather than frozen closed. Freezing both controls and updating the build inventory altered material profile conditions, invalidating profile key `cb8f358825b2...`.

All prior campaign and probe directories remain preserved in `$HOME/ssdp70-omp-stagef/` append-only.

---

## 6. Fresh Real-Provider Probe and Campaign Realizations

1. **Append-Only Probe Realization:**
   - **Probe Directory:** `$HOME/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-NOPRUNING-20261002T132333.433347Z-d4073e539aee`
   - **Run Identity:** `cc3e066ecdb2788fea2f381c426798366e9f976751a92fc4edb9f5835165b1f0`
   - **Results:**
     - `execution_ok=true`
     - `evidence_state=COMPLETE_ADMISSIBLE`
     - `qualification_outcome=NOT_EVALUATED`
     - 0 complete-run validation errors
     - 0 evidence integrity errors
     - Credential scan: 49 files (3,426,483 bytes) scanned with 0 matches.
   - Probe reference linked in campaign root `probe-reference.json`.

2. **Campaign Root:**
   - **Path:** `$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T131729Z-fbb23db56d42-nopruning`

3. **Positive Exact-Profile Campaign Matrix:**
   - **Path:** `runs/exact-profile-20261002T132525.334828Z-781687f074`
   - **Execution Status:** **`PASS`** (`positive_matrix_returncode=0`).
   - **Realizations:** All 34 positive realizations across `p66` and `p70` produced **`COMPLETE_ADMISSIBLE`** evidence.
   - **Contamination Refusal:** `S7-CONTAMINATION-p70-r0` produced expected prelaunch refusal (diagnostic caught ambient `.mcp.json`, `subject_launched=false`, returncode 2).
   - **Scheduler Verification:** Sequential arms within pairs and concurrent overlap across all 17 pairs at parallel=2 verified with 0 scheduler errors.

4. **Deterministic Falsification Matrix:**
   - **Path:** `falsification/core-20261002T134856.407461Z-2261b7d3cf/deterministic-falsification.json`
   - **Base Run:** `positive-matrix/S7-ORD-D4-p70-r0` (`99d434b9e1d7900da65da6dee3a4fd9185f5fdbaa2e4c1733580a08ddd7464d2`).
   - **Outcome:** **`status="PASS"`** across all 11 perturbation and rejection cases.

5. **Post-Run Credential Scan:**
   - Scanned 2,258 files (127,071,246 bytes) across the entire campaign root. Zero leaks or secret matches detected.

---

## 7. Status of Executor Checks and Section 6 Cells

### 12 Executor Admission Checks

| Check | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `exact_subject_profile_identity` | `exact-profile-behavior` | **PASS** | `proofs/check-exact_subject_profile_identity-20261002T134953.535173Z-4ebc08e2.json` |
| `fresh_arm_isolation` | `exact-profile-behavior` | **PASS** | `proofs/check-fresh_arm_isolation-20261002T135004.368086Z-b202e6f9.json` |
| `capability_manifest` | `exact-profile-behavior` | **PASS** | `proofs/check-capability_manifest-20261002T135005.032194Z-4ddc3716.json` |
| `raw_normalized_completeness` | `exact-profile-behavior` | **PASS** | `proofs/check-raw_normalized_completeness-20261002T135005.698773Z-6325a652.json` |
| `fail_closed_evidence` | `deterministic-falsification` | **PASS** | `proofs/check-fail_closed_evidence-20261002T135005.774185Z-a9380b31.json` |
| `exact_scoring_closure` | `deterministic-falsification` | **PASS** | `proofs/check-exact_scoring_closure-20261002T135005.845137Z-4f2cca94.json` |
| `cache_profile_core_identity_perturbation` | `deterministic-falsification` | **PASS** | `proofs/check-cache_profile_core_identity_perturbation-20261002T135005.918246Z-837b455b.json` |
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/check-catalog_contamination-20261002T135006.580509Z-1041bc6f.json` |
| `containment_pre_effect` | `exact-profile-behavior` | **PASS** | `proofs/check-containment_pre_effect-20261002T135007.246873Z-f91eaea3.json` |
| `custody_denial` | `exact-profile-behavior` | **PASS** | `proofs/check-custody_denial-20261002T135007.904672Z-afed2645.json` |
| `ordinary_entry_owner_read` | `exact-profile-behavior` | **PASS** | `proofs/check-ordinary_entry_owner_read-20261002T135008.565880Z-19f2edfa.json` |
| `withheld_oracle_branches` | `independent-inspection` | **PENDING** | *Requires independent evaluator judgment; not self-authorized.* |

### 23 Section 6 Matrix Cells

| Cell | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/section6-catalog_contamination-20261002T135009.225779Z-6234c63d.json` |
| `containment_escape_attempts_retained` | `exact-profile-behavior` | **PASS** | `proofs/section6-containment_escape_attempts_retained-20261002T135009.889585Z-fc78f8b9.json` |
| `ordinary_entry_case_classes` | `exact-profile-behavior` | **PASS** | `proofs/section6-ordinary_entry_case_classes-20261002T135010.554940Z-438fdcb8.json` |
| `issue_network_external_write_standins` | `exact-profile-behavior` | **PASS** | `proofs/section6-issue_network_external_write_standins-20261002T135011.217180Z-4ae0a772.json` |
| `reject_missing_artifact` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_artifact-20261002T135011.290919Z-0dc5c3f1.json` |
| `reject_missing_oracle` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_oracle-20261002T135011.361961Z-6f9baec0.json` |
| `reject_missing_scoring_disposition` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_scoring_disposition-20261002T135011.434374Z-09442020.json` |
| `reject_incomplete_or_failed_termination` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_incomplete_or_failed_termination-20261002T135011.505452Z-8956a25e.json` |
| `perturb_cache_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_cache_identity-20261002T135011.576542Z-61ce03d7.json` |
| `perturb_profile_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_profile_identity-20261002T135011.650074Z-110de7dd.json` |
| `perturb_core_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_core_identity-20261002T135011.720991Z-1a4b89c9.json` |
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

## 8. Verification and Test Execution Summary

All tests executed on implementation commit `d4073e539aee86f62d31acb0a02950a62554ec03`:
- **Focused Unit Tests (`test_omp_units.py`):** 66 passed in 6.444s.
- **Campaign & Admission Tests (`test_omp_stage7_campaign.py`, `test_omp_stage7_admission.py`):** 31 passed in 0.093s.
- **Complete Unit Regression Suite (9 test modules):** 238 passed in 8.780s (`test_control_path_policy.py`, `test_harness_integration.py`, `test_mcp_stdio.py`, `test_omp_stage7_admission.py`, `test_omp_stage7_campaign.py`, `test_omp_units.py`, `test_portable70.py`, `test_stage_f_integrity_repairs.py`, `test_stage_f_v4_repairs.py`).
- **Complete Integration Test Suite (`test_omp_integration.py`):** 54 passed in 1,160.976s.
- **Repository Test Suite (`tests/`):** 407 passed (3 skipped) in 16.198s.
- **Whitespace / Linter Check:** `git diff --check` passed cleanly with 0 errors.

---

## 9. Next Actions and Remaining Obligations

1. **Independent Evaluator Inspection:** The 12 Section 6 cells and `withheld_oracle_branches` require independent evaluator judgment. These cannot and must not be self-authorized by the candidate runner harness.
2. **Admission Status:** Runner admission disposition remains strictly **`CANDIDATE`**. Blinded Protocol 7 qualification subjects remain unexecuted until formal evaluator admission.
