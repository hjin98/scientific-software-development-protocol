# OMP Stage 7 Transcript-Consistency Repair and Campaign Closure Report

**Date:** 2026-10-02

**Governing protocol:** Scientific Software Development Protocol (SSDP) 6.6.0

**Disposition:** Candidate evidence closure; runner admission remains open for independent review (`CANDIDATE`).

---

## 1. Scope and Status Terms

This report records the D4 transcript-consistency repair tightening the native OMP tool result pruning predicate, the reconciliation of tool digests, the re-frozen execution profile, the fresh append-only real-provider probe, and the fresh Stage 7 candidate campaign execution.
- **OMP**: Headless runner identified by the qualification contract and frozen profile.
- **Arms**: `p66` (Protocol 6.6.0 comparison arm) and `p70` (candidate semantic subject).
- **`COMPLETE_ADMISSIBLE`**: A run has complete, untruncated, admissible realization evidence satisfying all contract constraints; does not denote runner admission.
- **`NOT_EVALUATED`**: Qualification scoring was not performed (probe mode).
- **`CANDIDATE`**: Profile evidence is complete and admissible for review; runner admission has not been self-authorized.

---

## 2. Commits, Candidate, and Execution Profile

- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Candidate starting head:** `800de808e5f3f435c904b49e07f64fc5c80a4994`
- **Implementation commit:** `110c47de0da303df0c21eb9f0d1f22d6670da1c0`
- **Final closure report commit:** `00675475819a0993aae0ace918573a75111a8e93`
- **Immutable semantic subject:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p66 arm commit:** `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- **p66 package-tree SHA-256:** `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`
- **p70 arm commit:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **p70 package-tree SHA-256:** `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`
- **Frozen OMP profile ID:** `omp-headless-deepinfra-glm53-flash-stage7-transcriptfixed-110c47de0da303df0c21eb9f0d1f22d6670da1c0`
- **Frozen OMP profile key:** `cb8f358825b22a5c1b76723d6bd6144c90824a3f4874de607a75eb727619cb18`
- **Frozen profile document SHA-256:** `62a6c4529abb72a8890d32e2dc598fa5f1662ab6df24058cd4df52b6e7955c77`
- **Adapter (`adapters/omp.py`) SHA-256:** `2009c56f2ecb99cf16d02e720fc7d4fd5c14720d6379d2cf6d51a9e156903907`
- **Campaign harness (`omp_stage7_campaign.py`) SHA-256:** `9d739b6871dd39a57df0e93cea78836dd3dc77f6e20d2503aec214e76d5991be`
- **Admission harness (`omp_stage7_admission.py`) SHA-256:** `e5d5059f67c0bae6449f5d5c3ea3077b96716aac28ff631fc31c9143080ead77`
- **Host Execution Environment (bound in profile):**
  - OS Release: Ubuntu 22.04 (`id="ubuntu"`, `version_id="22.04"`, SHA-256: `594d5ddd35aedb47f00d9c34d140017907a5b9f93c975aba125fc924daac5c07`)
  - Kernel: `Linux 6.8.0-138-generic #138~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC x86_64`
  - Supervisor Python: CPython 3.10.12 (executable SHA-256: `a2f33a6e006989270f4340528eb61f8f97366e00a5d1b602ac8672ea44fc56ae`)

---

## 3. Transcript-Consistency Pruning Repair Details

### Prior Defect and Motivation
The previous implementation commit (`55f2a6275632af86d26c52ac25907fcc3185d80b`) identified that OMP 18.0.11 performs in-memory compaction (`pruneSupersededToolResults`) on earlier reads of a re-read file, emitting the raw execution result in real-time `message_end` and the compacted record in `agent_end.messages`. However, review revealed that the pruning admissibility predicate was underconstrained:
1. `prunedAt` was accepted as any non-None object.
2. Metadata equality was not enforced fail-closed across all non-pruning fields (keys could be added, deleted, or mutated).
3. The predicate authorized `"[Uneventful result elided]"` without establishing native runtime eligibility or evidence.
4. Trajectory eligibility was not verified: a pruned `toolResult` was admitted even if the corresponding tool call was not a `read` or the file was never subsequently read.

### The Precise Executable Pruning Predicate
The helper `_is_valid_omp_tool_result_pruning(m_end, a_end, trajectory)` in `qualification/ssdp70/eval/adapters/omp.py` now enforces a 9-condition structurally fail-closed relation:
1. **Role Match:** `m_end.get("role") == "toolResult"` and `a_end.get("role") == "toolResult"`.
2. **Tool Call ID Match:** `m_end.get("toolCallId") == a_end.get("toolCallId")` and `bool(m_end.get("toolCallId"))`.
3. **Structural Field Set Parity:** `set(a_end.keys()) == set(m_end.keys()) | {"prunedAt"}`. No arbitrary fields may be added, removed, or renamed.
4. **Fail-Closed Non-Pruning Metadata Equality:** For every key `k` in `m_end` except `"content"`, `a_end[k] == m_end[k]`. This verifies `toolName`, `isError`, selector metadata, and all other metadata attributes remain strictly identical.
5. **Strict `prunedAt` Validation:** `type(pruned_at) is int and pruned_at > 0`. Python booleans (`bool` is a subclass of `int`) are explicitly rejected (`type(True) is bool`). Non-ints, strings, lists, 0, and negative numbers are rejected fail-closed.
6. **Narrow Authorized Notice:** `a_end.get("content")` must be exactly `[{"type": "text", "text": "[Superseded by a newer read of this file]"}]`. The unauthorized notice `"[Uneventful result elided]"` has been eliminated.
7. **Intact Raw Result:** `m_end.get("content") != a_end.get("content")` (the raw execution result in `message_end` must remain preserved and not pre-mutated).
8. **Trajectory Grounding:** The `toolCallId` must match an earlier `role == "toolUse"` event in the preceding trajectory.
9. **Trajectory Native Eligibility:** The grounded `toolUse` call must invoke a read tool (`toolName` in `{"read_file", "read"}` or ending with `.read_file`/`.read`), extract a valid target path, and there must exist a strictly subsequent read tool call targeting the exact same path prior to `m_end`.

---

## 4. Counterfactual and Discriminating Test Coverage

Focused negative and counterfactual tests were added in `qualification/ssdp70/eval/test_omp_units.py`:

1. **Strict `prunedAt` Validation (`test_omp_tool_result_pruning_strict_pruned_at`):**
   - Verified rejection of: `None`, `0`, `-1`, `-100`, `True` (bool), `False` (bool), `"12345"` (string), `[12345]` (list), `{"val": 12345}` (dict), and omitted `prunedAt`.
   - Verified acceptance of genuine positive integer `1727850000000`.

2. **Fail-Closed Metadata Parity (`test_omp_tool_result_pruning_structurally_fail_closed_metadata`):**
   - Verified rejection of metadata mutations: `isError: False -> True`, `toolName: "read" -> "read_v2"`, selector metadata alteration.
   - Verified rejection of added keys (e.g. `extra: "data"`).
   - Verified rejection of removed keys (e.g. omitting non-content fields present in `message_end`).

3. **Narrow Class and Trajectory Eligibility (`test_omp_tool_result_pruning_narrow_class_and_trajectory_eligibility`):**
   - Verified rejection of unauthorized notice `"[Uneventful result elided]"`.
   - Verified rejection of arbitrary pruning notice strings.
   - Verified rejection of pruning applied to non-read tools (e.g. `write_file`).
   - Verified rejection of ungrounded `toolCallId` (not present in preceding trajectory).
   - Verified rejection of single-read files (file read only once, never superseded).
   - Verified acceptance of legitimate superseded file read trajectory.

---

## 5. Stale Evidence Classification

The following prior campaign evidence is classified as stale and retained append-only:
1. **`OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix`:**
   - **Reason:** Adapter misdiagnosed native in-memory compaction on realization `S7-ORD-VARIANT-p66-r0` as dropped/reordered events. Profile key `5754fb5ec39a...` was superseded.
2. **`OMP-STAGE7-20261002T040939Z-c42206dace0c-transcriptfix`:**
   - **Reason:** While `S7-ORD-VARIANT-p66-r0` succeeded, the pruning admissibility predicate was underconstrained (`prunedAt` not strictly typed as positive int, metadata equality not fail-closed, unauthorized notices permitted, trajectory eligibility not enforced). Modifying `adapters/omp.py` updated `execution_support_sha256` and invalidated profile key `c42206dace0c...`.

Both prior campaign directories remain preserved in `$HOME/ssdp70-omp-stagef/admission/` and are not reused as candidate admission evidence.

---

## 6. Fresh Real-Provider Probe and Campaign Realizations

1. **Append-Only Probe Realization:**
   - **Probe Directory:** `$HOME/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-TIGHTENEDPRUNING-20261002T063600.692983Z-d79c4f8b230b`
   - **Run Identity:** `22f859c87e1e953a490f8eeb1da5fa647077e9b7639e9f7186db7ee473b87269`
   - **Results:**
     - `execution_ok=true`
     - `evidence_state=COMPLETE_ADMISSIBLE`
     - `qualification_outcome=NOT_EVALUATED`
     - 0 run validation errors
     - 0 integrity errors
     - 0 credential matches detected
   - Probe reference linked in campaign root `probe-reference.json`.

2. **Campaign Root:**
   - **Path:** `$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T063352Z-cb8f358825b2-tightenedpruning`

3. **Positive Exact-Profile Campaign Matrix:**
   - **Path:** `runs/exact-profile-20261002T063752.706611Z-f86dad5d14`
   - **Execution Status:** **`PASS`** (`positive_matrix_returncode=0`).
   - **Realizations:** All 34 positive realizations across `p66` and `p70` produced **`COMPLETE_ADMISSIBLE`** evidence.
   - **Contamination Refusal:** `S7-CONTAMINATION-p70-r0` produced expected prelaunch refusal (diagnostic caught ambient `.mcp.json`, `subject_launched=false`, returncode 2).
   - **Scheduler Verification:** Sequential arms within pairs and concurrent overlap across all 17 pairs at parallel=2 verified with 0 scheduler errors.
   - **Historical S7-ORD-VARIANT-p66-r0 Trace Verification:** The real OMP trace from campaign `5754fb5ec39a` was re-verified against the tightened adapter. It passed with 0 transcript errors and 46 normalized events, demonstrating that legitimate native compaction succeeds through the tightened fail-closed predicate.

4. **Deterministic Falsification Matrix:**
   - **Path:** `falsification/core-20261002T065740.179476Z-171fc0b62b/deterministic-falsification.json`
   - **Base Run:** `positive-matrix/S7-ORD-D4-p70-r0` (`ec357045bfccff574360f953042501af81ffb45b722273cbbb5f42cb0b49ba95`).
   - **Outcome:** **`status="PASS"`** across all 11 perturbation and rejection cases.

5. **Post-Run Credential Scan:**
   - Scanned 2,281 files (123,608,293 bytes) across the entire campaign root. Zero leaks or secret matches detected.

---

## 7. Status of Executor Checks and Section 6 Cells

### 12 Executor Admission Checks

| Check | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `exact_subject_profile_identity` | `exact-profile-behavior` | **PASS** | `proofs/check-exact_subject_profile_identity-20261002T065809.845009Z-d5b7617b.json` |
| `fresh_arm_isolation` | `exact-profile-behavior` | **PASS** | `proofs/check-fresh_arm_isolation-20261002T065818.571439Z-41cfb691.json` |
| `capability_manifest` | `exact-profile-behavior` | **PASS** | `proofs/check-capability_manifest-20261002T065819.141671Z-570a25fa.json` |
| `raw_normalized_completeness` | `exact-profile-behavior` | **PASS** | `proofs/check-raw_normalized_completeness-20261002T065819.709322Z-e1371569.json` |
| `fail_closed_evidence` | `deterministic-falsification` | **PASS** | `proofs/check-fail_closed_evidence-20261002T065821.990264Z-2d887a02.json` |
| `exact_scoring_closure` | `deterministic-falsification` | **PASS** | `proofs/check-exact_scoring_closure-20261002T065821.998462Z-754641e7.json` |
| `cache_profile_core_identity_perturbation` | `deterministic-falsification` | **PASS** | `proofs/check-cache_profile_core_identity_perturbation-20261002T065821.999479Z-f0bb5043.json` |
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/check-catalog_contamination-20261002T065820.279860Z-1faee5b1.json` |
| `containment_pre_effect` | `exact-profile-behavior` | **PASS** | `proofs/check-containment_pre_effect-20261002T065820.852431Z-ebf5fdb8.json` |
| `custody_denial` | `exact-profile-behavior` | **PASS** | `proofs/check-custody_denial-20261002T065821.417256Z-3f309a63.json` |
| `ordinary_entry_owner_read` | `exact-profile-behavior` | **PASS** | `proofs/check-ordinary_entry_owner_read-20261002T065821.989069Z-e945c7eb.json` |
| `withheld_oracle_branches` | `independent-inspection` | **PENDING** | *Requires independent evaluator judgment; not self-authorized.* |

### 23 Section 6 Matrix Cells

| Cell | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/section6-catalog_contamination-20261002T065822.571434Z-2c8cff41.json` |
| `containment_escape_attempts_retained` | `exact-profile-behavior` | **PASS** | `proofs/section6-containment_escape_attempts_retained-20261002T065823.140880Z-da50f4be.json` |
| `ordinary_entry_case_classes` | `exact-profile-behavior` | **PASS** | `proofs/section6-ordinary_entry_case_classes-20261002T065823.708899Z-0c8da973.json` |
| `issue_network_external_write_standins` | `exact-profile-behavior` | **PASS** | `proofs/section6-issue_network_external_write_standins-20261002T065824.281488Z-b64cb890.json` |
| `reject_missing_artifact` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_artifact-20261002T065824.282670Z-a0f5cb05.json` |
| `reject_missing_oracle` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_oracle-20261002T065824.290740Z-c2f6d2f3.json` |
| `reject_missing_scoring_disposition` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_scoring_disposition-20261002T065824.291738Z-f2eb8b75.json` |
| `reject_incomplete_or_failed_termination` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_incomplete_or_failed_termination-20261002T065824.292737Z-9e6b36cb.json` |
| `perturb_cache_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_cache_identity-20261002T065824.293739Z-e18e8748.json` |
| `perturb_profile_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_profile_identity-20261002T065824.294747Z-7ecf8ff9.json` |
| `perturb_core_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_core_identity-20261002T065824.295742Z-a35dc8c0.json` |
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

All tests executed on checkout `110c47de0da303df0c21eb9f0d1f22d6670da1c0`:
- **Focused Unit Tests (`test_omp_units.py`):** 64 passed in 0.26s.
- **Campaign & Admission Tests (`test_omp_stage7_campaign.py`, `test_omp_stage7_admission.py`):** 31 passed in 0.64s.
- **Complete Unit Regression Suite (9 test modules):** 236 passed in 8.721s (`test_control_path_policy.py`, `test_harness_integration.py`, `test_mcp_stdio.py`, `test_omp_stage7_admission.py`, `test_omp_stage7_campaign.py`, `test_omp_units.py`, `test_portable70.py`, `test_stage_f_integrity_repairs.py`, `test_stage_f_v4_repairs.py`).
- **Complete Integration Test Suite (`test_omp_integration.py`):** 54 passed in 1,162.451s.
- **Whitespace / Linter Check:** `git diff --check` passed cleanly with 0 errors.

---

## 9. Next Actions and Remaining Obligations

1. **Independent Evaluator Inspection:** The 12 Section 6 cells and `withheld_oracle_branches` require independent evaluator judgment. These cannot and must not be self-authorized by the candidate runner harness.
2. **Admission Status:** Runner admission disposition remains strictly **`CANDIDATE`**. Blinded Protocol 7 qualification subjects remain unexecuted until formal evaluator admission.
