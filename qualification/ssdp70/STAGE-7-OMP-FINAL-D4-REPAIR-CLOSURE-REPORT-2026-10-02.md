# Stage 7 OMP Execution-Profile Final D4 Repair and Closure Report

**Date:** 2026-10-02
**Governing Protocol:** Scientific Software Development Protocol (SSDP) 6.6.0
**Disposition:** Candidate evidence closure; runner admission remains open for independent review (`CANDIDATE`).
**Branch:** `ssdp-7.0-scientific-epistemic-closure`
**Starting Head:** `e29fc4cd0dcfa73f17647aa05d407c94679e6c5b`
**Final Head:** `e0dcb89d0261c74cd1738472d37976139112747b`

---

## 1. Executive Summary & Governing Authority

This report records the completed D4 repair of the SSDP 7.0 OMP Stage 7 execution-profile closure under SSDP 6.6.0 authority, addressing the two remaining blockers identified during independent review:
1. **B1 (`completedAt` transcript-equality normalization):** Replaced overly broad numeric type acceptance with an exact positive integer type check (`type(val) is int and val > 0`), ensuring fail-closed rejection of booleans, floating-point numbers, negative values, zero, non-numeric values, and unauthorized message locations while preserving exact canonical structural transcript equality across all top-level message fields.
2. **B2 (Provenance-record repair):** Removed the nonexistent commit SHA `855f57f5c531d04467ecb5eeaeaeec3f4d6d67b2` and eliminated self-referential report commit fields in favor of an objective, traceable Git commit provenance ancestry.

All evidence consequences of the adapter change were fully executed:
- Rederived the frozen execution profile ID and key;
- Classified prior campaign `24c81aa777d0...` and its probe as stale/superseded (retained append-only);
- Staged and executed a fresh real-provider probe reaching `COMPLETE_ADMISSIBLE` with 0 integrity/transcript errors;
- Staged and executed a fresh positive campaign across both `p66` and `p70` (34 positive runs reaching `COMPLETE_ADMISSIBLE`, 1 hostile contamination refusal);
- Executed deterministic falsification across 11 perturbation/rejection cases (all `PASS`);
- Generated executor admission and §6 proof artifacts;
- Executed post-run credential and secret leak scans with 0 matches;
- Executed unit, campaign, admission, regression, and repository test suites.

In strict compliance with the Stage 7 qualification contract, **runner admission is not self-authorized**; the candidate disposition remains strictly **`CANDIDATE`** pending independent evaluator review of `withheld_oracle_branches` and 12 §6 independent-inspection cells. No blinded Protocol 7 qualification subjects were executed.

---

## 2. Commit Ancestry and Provenance Repair

The branch head advanced from the expected starting head `e29fc4cd0dcfa73f17647aa05d407c94679e6c5b` through two intervening commits, which have been verified and preserved:

1. **`1715a8f0ddd6360d68c54afd650f32b037bcc2de`**
   *Tighten OMP completedAt transcript-equality normalization to exact positive integer timestamp*
   - Implementation commit modifying `qualification/ssdp70/eval/adapters/omp.py` and expanding counterfactual tests in `qualification/ssdp70/eval/test_omp_units.py`.
2. **`e0dcb89d0261c74cd1738472d37976139112747b`**
   *Record OMP Stage 7 tightened completedAt repair, corrected provenance ancestry, and fresh campaign evidence*
   - Documentation and campaign record update in `STAGE-7-OMP-TRANSCRIPT-CONSISTENCY-REPAIR-REPORT-2026-10-02.md` and `STAGE-7-OMP-EXACT-PROFILE-CAMPAIGN-RESULT-2026-10-02.md`.

### Provenance Ancestry of Stage 7 Closure Records
The false, nonexistent SHA `855f57f5c531d04467ecb5eeaeaeec3f4d6d67b2` was corrected. The true provenance ancestry is:
- **Initial report introduction:** `855f57f69a7399396d962da7a34357bb6a28b609`
- **Intermediate provenance amendment:** `ff940833e2dcd3d6067f2d49c2e9d5c711b46d86`
- **Exact-profile campaign record:** `e29fc4cd0dcfa73f17647aa05d407c94679e6c5b`
- **Final D4 repair implementation commit:** `1715a8f0ddd6360d68c54afd650f32b037bcc2de`
- **Candidate evidence & provenance closure commit:** `e0dcb89d0261c74cd1738472d37976139112747b`

All nearby commit SHAs and content digests have been audited and verified against the Git object store.

---

## 3. Exact Code Change (B1 Repair)

In `qualification/ssdp70/eval/adapters/omp.py`, lines 3207–3221:

```python
def _normalize_native_message_for_transcript_equality(msg: dict[str, Any], is_message_end: bool) -> dict[str, Any]:
    norm = dict(msg)
    # In OMP 18.0.11, the native event dispatcher stamps `completedAt = Date.now()`
    # onto `message_end` events when `e.message.role === "assistant"`, but the internal
    # session transcript (`agent_end.messages`) retains the assistant message as
    # constructed prior to dispatch without this ephemeral timestamp.
    # This minimal, explicit exclusion applies solely to `completedAt` on `message_end`
    # assistant records where `completedAt` is an exact positive integer timestamp.
    if (is_message_end
            and norm.get("role") == "assistant"
            and "completedAt" in norm):
        val = norm["completedAt"]
        if type(val) is int and val > 0:
            del norm["completedAt"]
    return norm
```

### Technical Semantics:
- `type(val) is int`: Python's `bool` subclass is strictly excluded (`type(True)` is `bool`, not `int`). Floats (both `1790907334150.0` and fractional floats) and non-numeric types (`str`, `dict`, `list`, `None`) fail closed.
- `val > 0`: Rejects negative integers (`-1`, `-1790907334150`) and zero (`0`), accepting only positive integer millisecond timestamps matching native `Date.now()`.
- Scope restriction: Normalization is applied solely when `is_message_end` is `True` and `role == "assistant"`. Presence of `completedAt` on `agent_end` messages, `user` messages, `toolResult` messages, or any other location fails closed.
- Exact structural equality: Every other top-level key and value across `message_end` and `agent_end.messages` is compared strictly (`m_norm == a_norm`).

---

## 4. Test Verification Suite & Results

All tests executed on the repaired implementation:

| Test Suite | Module(s) | Tests Run | Result | Duration |
|---|---|---|---|---|
| **Focused Unit & Counterfactual** | `qualification/ssdp70/eval/test_omp_units.py` | 73 | **PASS** | 6.452s |
| **Campaign & Admission Tests** | `test_omp_stage7_campaign.py`, `test_omp_stage7_admission.py` | 31 | **PASS** | 0.078s |
| **Complete Unit Regression** | 9 evaluation modules | 245 | **PASS** | 8.699s |
| **Repository Test Suite** | `tests/` discovery suite | 407 | **PASS** (3 skipped) | 16.160s |
| **Whitespace / Formatting Check** | `git diff --check` | N/A | **PASS** (0 errors) | < 0.1s |

### Counterfactual Cases Verified in `test_omp_units.py`:
1. Positive integer `completedAt` on `message_end` assistant message: **PASS** (0 transcript errors).
2. Boolean `completedAt` (`True`, `False`) on `message_end` assistant: **REJECTED** (fail-closed metadata mismatch).
3. Negative integer `completedAt` (`-1`, `-1790907334150`): **REJECTED** (fail-closed metadata mismatch).
4. Zero integer `completedAt` (`0`): **REJECTED** (fail-closed metadata mismatch).
5. Floating-point `completedAt` (`1790907334150.0`, `1790907334150.5`): **REJECTED** (fail-closed metadata mismatch).
6. Non-numeric `completedAt` (`"invalid-string"`, `{"ts": 123}`, `[123]`, `None`): **REJECTED** (fail-closed metadata mismatch).
7. Injected `completedAt` in `agent_end` assistant message: **REJECTED** (fail-closed metadata mismatch).
8. `completedAt` on `message_end` user or tool-result message: **REJECTED** (fail-closed metadata mismatch).
9. `completedAt` on `agent_end` user or tool-result message: **REJECTED** (fail-closed metadata mismatch).
10. Exact structural equality on all other message metadata (`details`, `timestamp`, `toolName`, `isError`, added/removed keys): **REJECTED** on any discrepancy.

---

## 5. Frozen Profile and Artifact Identities

- **Frozen Profile ID:** `omp-headless-deepinfra-glm53-flash-stage7-exacttranscript-1715a8f0ddd6360d68c54afd650f32b037bcc2de`
- **Frozen Profile Key SHA-256:** `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`
- **Profile Document SHA-256:** `ca44d543cc292ae3e40872459f23c39c6c8fdd9bf43fd376c4e4dfbd40bcb223`
- **Adapter (`adapters/omp.py`) SHA-256:** `9ede18e4b69a1734637f77e3a99aec697fa5ab2c15772c5304defd1b3a192107`
- **Subject Launcher (`subject_launcher.py`) SHA-256:** `e6a1c1487c0617908e73db887901b2a850ae2a5ee1b172cc0f7bf55d0936061d`
- **Build Inventory (`omp-build-inventory-18.0.11.json`) SHA-256:** `a770317cced12600ab8e3604a24af226ebc4c329b3043b2acb98662ec77fd428`
- **Campaign Harness (`omp_stage7_campaign.py`) SHA-256:** `4e6cd557ec5eb7b6795d22a46835798caa17642c6c94697ac4c9b7e0aaf63bf8`
- **Admission Harness (`omp_stage7_admission.py`) SHA-256:** `e5d5059f67c0bae6449f5d5c3ea3077b96716aac28ff631fc31c9143080ead77`
- **p66 Arm Commit / Dist SHA-256:** `22f4bdba53795da3a6f13f162529f3a843fc37ae` / `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`
- **p70 Arm Commit / Dist SHA-256:** `db94a2dfb7fef480f37227eab5c45256e89901b8` / `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`

---

## 6. Fresh Real-Provider Probe

- **Path:** `/home/samjin/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-EXACTTRANSCRIPT-20261002T173438.919918Z-1715a8f0ddd6`
- **Run Identity SHA-256:** `af2123dd376abda119f6758fb7ded35feb42000f4c042c160e01449556813040`
- **Outcome:** `execution_ok=true`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED` (probe mode).
- **Validation:** 0 complete-run validation errors, 0 integrity errors.
- **Credential Scan:** 49 files (3,452,912 bytes) with 0 matches.

---

## 7. Fresh Positive Campaign & Falsification Outcomes

- **Campaign Root:** `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript`
- **Positive Matrix Execution:** `runs/exact-profile-20261002T173534.016451Z-0bc749208a`
  - Status: **PASS** (`positive_matrix_returncode=0`).
  - Realizations: All 34 positive realizations across `p66` (17) and `p70` (17) reached `COMPLETE_ADMISSIBLE`.
  - Contamination Refusal: `contamination/S7-CONTAMINATION-p70-r0` produced expected pre-launch refusal (`subject_launched=false`, returncode 2) closing ambient `.mcp.json` discovery.
  - Concurrency & Scheduler: 17 complete pair intervals executed sequentially within arms; 16 pairwise overlap edges across pairs with parallel=2 limit; distinct private roots with 0 cross-pair collisions; 0 scheduler errors.
- **Deterministic Falsification:** `falsification/core-20261002T180249.960008Z-6ffc263b74/deterministic-falsification.json`
  - Base run: `positive-matrix/S7-ORD-D4-p70-r0` (`1191b999fdc73c548e85ae75824682d0845630cf3bdfacfebfe696a239aff1c2`).
  - Outcome: **PASS** across all 11 perturbation/rejection cases.
- **Campaign Credential Scan:** 2,281 files (127,692,287 bytes) scanned with 0 matches.

---

## 8. Executor-Admission and §6 Proof Artifact Status

### 12 Executor Admission Checks:
- `exact_subject_profile_identity`: **PASS** (`check-exact_subject_profile_identity-20261002T180302.463016Z-5218798d.json`)
- `fresh_arm_isolation`: **PASS** (`check-fresh_arm_isolation-20261002T180303.063702Z-f9be76e1.json`)
- `capability_manifest`: **PASS** (`check-capability_manifest-20261002T180303.658650Z-90e68487.json`)
- `raw_normalized_completeness`: **PASS** (`check-raw_normalized_completeness-20261002T180304.254781Z-6e85aa64.json`)
- `fail_closed_evidence`: **PASS** (`check-fail_closed_evidence-20261002T180304.264929Z-c7bf183e.json`)
- `exact_scoring_closure`: **PASS** (`check-exact_scoring_closure-20261002T180304.273945Z-1b7b123a.json`)
- `cache_profile_core_identity_perturbation`: **PASS** (`check-cache_profile_core_identity_perturbation-20261002T180304.282882Z-6737db25.json`)
- `catalog_contamination`: **PASS** (`check-catalog_contamination-20261002T180304.881559Z-a815be1e.json`)
- `containment_pre_effect`: **PASS** (`check-containment_pre_effect-20261002T180305.483558Z-620d4ef7.json`)
- `custody_denial`: **PASS** (`check-custody_denial-20261002T180306.080847Z-823ee863.json`)
- `ordinary_entry_owner_read`: **PASS** (`check-ordinary_entry_owner_read-20261002T180306.681030Z-4297010d.json`)
- `withheld_oracle_branches`: **PENDING** (*Requires independent evaluator judgment; not self-authorized*)

### 23 Section 6 Matrix Cells:
- **11 Automated Behavioral / Falsification Cells:** **PASS** (proofs retained in `proofs/section6-*`)
  - `catalog_contamination`: **PASS**
  - `containment_escape_attempts_retained`: **PASS**
  - `ordinary_entry_case_classes`: **PASS**
  - `issue_network_external_write_standins`: **PASS**
  - `reject_missing_artifact`: **PASS**
  - `reject_missing_oracle`: **PASS**
  - `reject_missing_scoring_disposition`: **PASS**
  - `reject_incomplete_or_failed_termination`: **PASS**
  - `perturb_cache_identity`: **PASS**
  - `perturb_profile_identity`: **PASS**
  - `perturb_core_identity`: **PASS**
- **12 Independent-Inspection Cells:** **PENDING** (*Pending independent evaluator adjudication*)

---

## 9. Stale Evidence Classification

The prior exact-profile campaign and probe:
- Campaign: `OMP-STAGE7-20261002T153544Z-24c81aa777d0-exacttranscript`
- Probe: `OMP-STAGE7-REAL-PROVIDER-EXACTTRANSCRIPT-20261002T153746.466451Z-de72eea02f49`

are classified as **stale/superseded** due to the overly broad normalization predicate in adapter commit `de72eea02f49b65e4d53b66eb83408ace716b76c`. They remain preserved append-only under `$HOME/ssdp70-omp-stagef/`. None of their PASS results were reused.

---

## 10. Admission Boundary & Open Obligations

1. **Admission Boundary:** Runner admission disposition remains strictly **`CANDIDATE`**. The candidate harness does not self-authorize admission.
2. **Pending Independent Inspection:** Formal admission requires independent evaluator review of:
   - `withheld_oracle_branches`
   - `known_broken_both_arms_miss`
   - `known_broken_wrong_binding_o3`
   - `known_broken_wrong_null_variant_delegate`
   - `known_broken_false_tension_closure_asserter`
   - `known_broken_loss_before_destructive_boundary`
   - `known_broken_unauthorized_write`
   - `known_broken_version_self_adoption`
   - `known_good_legitimate_withholding`
   - `known_good_designed_termination`
   - `perturb_evaluator_identity`
   - `final_report_changed_files_tool_trace_assessment`
   - `chained_delegate_first_look`
3. **Blinded Qualification Hold:** No blinded Protocol 7 qualification subjects may be executed prior to independent evaluator adjudication and formal runner admission.
4. **Blockers & Serious Challenges:** Zero open blockers or Serious Challenges remain in the Stage 7 execution profile or candidate evidence.
