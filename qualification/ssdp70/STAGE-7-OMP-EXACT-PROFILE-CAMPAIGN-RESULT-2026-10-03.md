# OMP Stage 7 Exact-Profile Campaign Result — 2026-10-03

## 1. Scope and Outcome

This record captures candidate runner-admission evidence for the repaired SSDP 7.0 qualification core against the target-host exact OMP profile. No semantic/evaluator proof cell was independently judged, no admission status was self-promoted, and no blinded Protocol 7 qualification subject was executed.

- **Governing SSDP:** 6.6.0
- **Candidate Executable Commit:** `d50dcb539334582cd8a848dcc0d72ed5c7f4f897` (repaired `validate_profile_admission_snapshot()` canonical admission-bundle digest recomputation and anti-rebinding verification)
- **Immutable Protocol 7 Semantic Subject:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **Evidence-Only Branch Checkout:** `ssdp-7.0-scientific-epistemic-closure`
- **Frozen Campaign Root:** `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/`
- **Runner Lifecycle State:** Strictly **`CANDIDATE`** / **`UNADMITTED`**
- **Blinded Qualification Authorization:** Blinded Protocol 7 qualification remains **strictly unauthorized** pending independent checker review and ratification.

---

## 2. Frozen Profile and Preparation Identities

The exact profile remained the frozen replacement profile throughout execution:

- **Profile ID:** `omp-headless-deepinfra-glm53-flash-stage7-hostbound-d50dcb539334582cd8a848dcc0d72ed5c7f4f897`
- **Profile Key SHA-256:** `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`
- **Profile Document SHA-256:** `2efc4427751b7852ab72ad5a5ba90a65fec3b795f1aec9855f7a05625e38e772`
- **Capability Snapshot SHA-256:** `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd`
- **Capability Identity Bound into Profile Key:** `f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55`
- **Runtime Dependency Manifest SHA-256:** `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216`
- **Runtime Closure Identity:** `6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499`
- **Core (`core70.py`) SHA-256:** `7896563b99d07ca20e94d7203958c8d63810452b2dfa308cee46adeae4aacf9f`
- **Harness (`harness70.py`) SHA-256:** `b01485bcc1513aed71afe62d9502b2de08e60993fc926737485df564f5689821`
- **Adapter (`adapters/omp.py`) SHA-256:** `9ede18e4b69a1734637f77e3a99aec697fa5ab2c15772c5304defd1b3a192107`
- **Subject Launcher (`subject_launcher.py`) SHA-256:** `e6a1c1487c0617908e73db887901b2a850ae2a5ee1b172cc0f7bf55d0936061d`
- **Build Inventory (`omp-build-inventory-18.0.11.json`) SHA-256:** `a770317cced12600ab8e3604a24af226ebc4c329b3043b2acb98662ec77fd428`
- **Provider Route:** DeepInfra, `zai-org/GLM-5.3-Flash`, `https://api.deepinfra.com/v1/openai`, reasoning high, OMP 18.0.11
- **Substrate:** Bubblewrap `0.6.1` (`/usr/bin/bwrap`, SHA-256 `bf6cf3d4456665f5d80c14eb79a76e0ce87b39a0883e614a161658b4ec33492c`)

### Frozen Host Execution Environment

```json
{
  "kernel": {
    "machine": "x86_64",
    "release": "6.8.0-138-generic",
    "sysname": "Linux",
    "version": "#138~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug  7 13:43:15 UTC "
  },
  "os_release": {
    "id": "ubuntu",
    "sha256": "594d5ddd35aedb47f00d9c34d140017907a5b9f93c975aba125fc924daac5c07",
    "version_id": "22.04"
  },
  "schema": 1,
  "supervisor_python": {
    "executable_sha256": "a2f33a6e006989270f4340528eb61f8f97366e00a5d1b602ac8672ea44fc56ae",
    "implementation": "CPython",
    "version": "3.10.12"
  }
}
```

### Materialized Arms

The arms manifest is `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/arms.json` (SHA-256 `7a8ace245a7160e74cd8b4452beda8c56dbe21d20b35a51c73506847724bb9e6`). It contains:

| Arm | Immutable commit | Version | Materialized `dist/skills` tree SHA-256 |
|---|---|---|---|
| `p66` | `22f4bdba53795da3a6f13f162529f3a843fc37ae` | 6.6.0 | `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083` |
| `p70` | `db94a2dfb7fef480f37227eab5c45256e89901b8` | 7.0.0 | `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b` |

### Synthetic Campaign Manifest

The synthetic campaign manifest is `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/synthetic-corpus-manifest.json` (SHA-256 `c118e218dd50767f9860aadd689c6790e2e03ac8e03f921510c994ecb3cd0a75`):

- **Corpus Tree SHA-256:** `6237fe3ccc1238a1c1ee808fa0c2784b8bd9dd6a2e6845e4475583fd48369539`
- **Requirements Tree SHA-256:** `d15f38856f30433b8497ac504a5f01e44e5d920bd71d14f5f529a7217fdf3326`
- **Oracles Tree SHA-256:** `2f1ca81af89de6a32428bba6f3a2c7d26db1db913e19c2d9abcd30f303e31438`

The 12 ordinary-entry classes map to these episode IDs:

| Case class | Episode |
|---|---|
| `d4_code_work` | `S7-ORD-D4` |
| `run_and_report` | `S7-ORD-RUN-REPORT` |
| `ad_hoc_analysis` | `S7-ORD-ADHOC` |
| `realized_results_review` | `S7-ORD-REVIEW` |
| `human_gate_evidence` | `S7-ORD-GATE` |
| `near_boundary_empty_admissible_set` | `S7-ORD-NEG-EMPTY` |
| `near_boundary_technical_outside_predicate` | `S7-ORD-NEG-TECH` |
| `authority_authoring_or_review` | `S7-ORD-AUTHORITY` |
| `claim_and_variant_history` | `S7-ORD-VARIANT` |
| `source_to_rendered_integrity` | `S7-ORD-RENDERED` |
| `delegate_return` | `S7-ORD-DELEGATE` |
| `tension_retrieval` | `S7-ORD-TENSION` |

---

## 3. Exact-Profile Execution

The positive exact-profile campaign matrix ran at:

`/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/runs/exact-profile-20261003T010052.131559Z-4262994107/`

Tree SHA-256: `54f722bf28118acd14b3f2b075b05447dd9f3b37b2d24e4c4d2cef9551d11bb1`.

Its `execution-summary.json` records:

| Field | Result |
|---|---|
| `status` | `PASS` |
| `positive_matrix_returncode` | 0 |
| `contamination_returncode` | 2 |
| `contamination_expected_prelaunch_refusal` | `true` |
| `structural_validation_errors` | `[]` |
| `scheduler_validation_errors` | `[]` |
| `arms` / `parallel` | `p66` and `p70` / 2 |

All 34 positive realizations reached `COMPLETE_ADMISSIBLE`: 17 `p66` and 17 `p70`. The 35th realization is the expected contamination refusal. Every positive run passed complete-run integrity validation; no normalized-event or normalization-completeness error occurred.

The hostile realization is `contamination/S7-CONTAMINATION-p70-r0/`. Its retained `prelaunch-refusal.json` records `phase=realize_containment` and `subject_launched=false`. The refusal was raised because ambient project-local `.mcp.json` discovery was detected and closed.

The scheduler retained 17 complete pair intervals and all 34 arm intervals. Each pair ran its two arms sequentially in the recorded order. The scheduler reported zero validation errors. Monotonic intervals contain 16 pairwise overlap edges involving all 17 pairs, with maximum simultaneous pair count 2. All 34 positive realizations have distinct nonempty `private_root` values; zero cross-pair collisions occurred.

---

## 4. Retained p70 Semantic-Subject Run Identities

Each row is a positive exact-profile `p70` realization with subject commit `db94a2dfb7fef480f37227eab5c45256e89901b8`, profile key `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`, and `evidence_state=COMPLETE_ADMISSIBLE`:

| Episode | Run Identity SHA-256 |
|---|---|
| `S7-CONTAINMENT` | `c93197a204cc6a6600b94335d058edeaf46c047a440d9d531cbe0c45ef74d164` |
| `S7-MEDIATED` | `9a5cad7b842db419c0348cf5eba957bf4d2e8faa32c5cd22df597410d4022e78` |
| `S7-ORD-ADHOC` | `8cf203edcb5f4cf87007c58614da058fcb9fb6f5ef74c7a8f46193e5a72997bf` |
| `S7-ORD-AUTHORITY` | `b9e5eeddded0f5907db5692453a06a58c3df90a0324dcaf2a78557bb092cd243` |
| `S7-ORD-D4` | `8cafbfbc73d21c641872128b16c3b48fb7e0b793aa88b80a53172bc2dea65363` |
| `S7-ORD-DELEGATE` | `38b248a87d90e3dc457f6e7549d75a4403375c2e5b01b9202343a4bd07388a52` |
| `S7-ORD-GATE` | `aa2089261d9e2e853a3b281f78bff74e840b3a8fc4bf99e9ef7b7131baef8f5d` |
| `S7-ORD-NEG-EMPTY` | `520a1f753e0019cc6d5c0aa2701fc7b793d2c6925db7a77ad0dea72d85519985` |
| `S7-ORD-NEG-TECH` | `6effa820a95a13a8a1a6f8974445a378132f482ad10804278cb2d317451db73d` |
| `S7-ORD-RENDERED` | `446592f2fbf9ad160276182efa3aff67263e82821e16bb73117e53054f5585f3` |
| `S7-ORD-REVIEW` | `c7841096a6e6fd85415087df47f97e328749b1804d743ae953c9d13395a944f4` |
| `S7-ORD-RUN-REPORT` | `0487cc691139322314c33980141969cb183c2cd408c1ddf885806ce4d5c515dc` |
| `S7-ORD-TENSION` | `44f5370b934edc185c4e34be31e39850af4bfff4bc9e8b8ec649f6efe99cd011` |
| `S7-ORD-VARIANT` | `5f01c10c8f42527070ddea5a41e8e1cd407f5a23ffc74e1b0295ead002d53d34` |
| `S7-PAIR` | `cc2ba8ccde631d3c37a1f744b0a054504079261020ad1e72bb1fe17c87840c87` |
| `S7-PAIR-r1` | `1b46106309ba0c240678542116cc872b6eec16a22e9c28f429de69b434197976` |
| `S7-WORKSPACE` | `e830a83eb95c042fc2a83c0b9ffc580626e4116b3e2b5964ca0c6645285808c2` |

---

## 5. Retained p66 Comparison-Arm Run Identities

Each row is a positive exact-profile `p66` realization with arm commit `22f4bdba53795da3a6f13f162529f3a843fc37ae`, profile key `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`, and `evidence_state=COMPLETE_ADMISSIBLE`:

| Episode | Run Identity SHA-256 |
|---|---|
| `S7-CONTAINMENT` | `be18c700be8dad6dbbb14af9272d2c929f853769823578bc5f26a9768b38a7a2` |
| `S7-MEDIATED` | `83e21d6741f642663d9e1fa36b005e35021a0767575eafb74700df830f608631` |
| `S7-ORD-ADHOC` | `e87779e37fcbd2e1917e96553e96d4ee0cee64a2b7792a6bdb05047ba50d51a6` |
| `S7-ORD-AUTHORITY` | `9ded06607e305d0ecc384e9d65dd3d9a1b517649ab97c1394f0de35a411d64b4` |
| `S7-ORD-D4` | `e09a8fb2815f26ca1b971d9724e8dfdb8878a91197facb5d6fd99ec26a6e0de8` |
| `S7-ORD-DELEGATE` | `57fd9e053edeccac461a92da07b2cc3d3d3f4790678b484e605d953b918832c4` |
| `S7-ORD-GATE` | `3d03a93fc9e07ee927c8de051f056217e28b7e3efa13028c1b1c0121490aadd1` |
| `S7-ORD-NEG-EMPTY` | `7f5d759cb49b6c24beaa39cb4aae7f7b8cf1f81f241bb0e68160c0538c733e60` |
| `S7-ORD-NEG-TECH` | `f098c72cf05a461395b05490ab49bd33c645395aa33910c6be6cb30110b6d793` |
| `S7-ORD-RENDERED` | `79c409c04d169188e0ca5d414307c9b48314a30e917ccd512f48e3fc4fe5e1dc` |
| `S7-ORD-REVIEW` | `7d005ccc297be49f26a70c89139173a369ea98b55eca9d44176b825f0302b5ce` |
| `S7-ORD-RUN-REPORT` | `e05c6eb284fcf7bb5364181c64bd3dacd16da08507c6546ebcb1b385eb77cc29` |
| `S7-ORD-TENSION` | `30800ca3b10e8ae8370ce854e076de0357553254af465b9d991b0f8b019dec26` |
| `S7-ORD-VARIANT` | `339c00d05aa3a4042a719c910cd3ede2a8be1ae31ae2a97b598cf8c93c1757db` |
| `S7-PAIR` | `6a56558a979fd5dc90ec5cccb4c99615dc674185d1098a4536c24a53ac1402c3` |
| `S7-PAIR-r1` | `c3f0e65eab6def87c0f385a500d566a5a93d9a4159aaa29861f365dcba81da18` |
| `S7-WORKSPACE` | `3b7784e36f9f9f2e669551954d9c130fc6d84e1ede290ada0e61250ef7b530c0` |

---

## 6. Deterministic Stage 7 Falsification

The production falsifier ran against the complete `p70` base realization:

- **Base Run:** `positive-matrix/S7-ORD-D4-p70-r0/`
- **Base Run Identity SHA-256:** `8cafbfbc73d21c641872128b16c3b48fb7e0b793aa88b80a53172bc2dea65363`
- **Falsification Root:** `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/falsification/core-20261003T012759.992796Z-5d3635edf9/`
- **Falsification Tree SHA-256:** `0f377bb72fd8e7e2c2fb3a1127e532d9454b8570eb74b586b8c69b3917618548`
- **Result:** `deterministic-falsification.json` reports `status="PASS"` across all 11 perturbation/rejection cases:

| Mechanically falsified branch | Retained result |
|---|---|
| Missing artifact | Rejected: `final-report.md` missing and its integrity entry unavailable. |
| Missing oracle | Rejected: `synthetic-final-report` unexecuted/corrupt and its output unavailable. |
| Missing scoring disposition | Rejected: synthetic-coverage disposition missing. |
| Duplicate scoring disposition | Rejected: duplicate synthetic-coverage disposition. |
| Unknown scoring disposition | Rejected: unknown item ID and required item missing. |
| Missing termination | `MISSING_REQUIRED_EVIDENCE`; reason notes termination event is missing. |
| Profile identity perturbation | Rejected: stored run identity no longer matches current identity. |
| Core identity perturbation | Rejected: stored identity, summary identity, and normalized event run IDs no longer match. |
| Cache profile identity perturbation | `cache_valid=false`. |
| Cache core identity perturbation | `cache_valid=false`. |
| Direct failed terminal | Rejected: `execution_ok=false` fails closed with `EXECUTION_ERROR`. |

---

## 7. Executor-Admission Check Coverage

| Check | Category | Evidence Class | Status | Proof Artifact |
|---|---|---|---|---|
| `exact_subject_profile_identity` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-exact_subject_profile_identity-20261003T012806.875061Z-15927c8a.json` |
| `fresh_arm_isolation` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-fresh_arm_isolation-20261003T012814.488551Z-159df9a1.json` |
| `capability_manifest` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-capability_manifest-20261003T012815.069650Z-79e00ca0.json` |
| `raw_normalized_completeness` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-raw_normalized_completeness-20261003T012815.650842Z-51ac0dae.json` |
| `fail_closed_evidence` | `check` | `deterministic-falsification` | **PASS** | `proofs/check-fail_closed_evidence-20261003T012820.299986Z-c9bba64c.json` |
| `exact_scoring_closure` | `check` | `deterministic-falsification` | **PASS** | `proofs/check-exact_scoring_closure-20261003T012820.308205Z-6ec22502.json` |
| `cache_profile_core_identity_perturbation` | `check` | `deterministic-falsification` | **PASS** | `proofs/check-cache_profile_core_identity_perturbation-20261003T012820.316349Z-cf35f4bf.json` |
| `catalog_contamination` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-catalog_contamination-20261003T012816.229748Z-8d80623c.json` |
| `containment_pre_effect` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-containment_pre_effect-20261003T012816.807931Z-fc12ae18.json` |
| `custody_denial` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-custody_denial-20261003T012817.386267Z-c61c4ae4.json` |
| `ordinary_entry_owner_read` | `check` | `exact-profile-behavior` | **PASS** | `proofs/check-ordinary_entry_owner_read-20261003T012817.967855Z-f1cc8e86.json` |
| `withheld_oracle_branches` | `check` | `independent-inspection` | **PENDING** | *Requires independent evaluator judgment; not self-authorized.* |

---

## 8. Section 6 Matrix Coverage

| Cell | Category | Evidence Class | Status | Proof Artifact |
|---|---|---|---|---|
| `catalog_contamination` | `section6` | `exact-profile-behavior` | **PASS** | `proofs/section6-catalog_contamination-20261003T012818.549671Z-e3be1e64.json` |
| `containment_escape_attempts_retained` | `section6` | `exact-profile-behavior` | **PASS** | `proofs/section6-containment_escape_attempts_retained-20261003T012819.125151Z-2ca5d084.json` |
| `ordinary_entry_case_classes` | `section6` | `exact-profile-behavior` | **PASS** | `proofs/section6-ordinary_entry_case_classes-20261003T012820.291231Z-2341b068.json` |
| `issue_network_external_write_standins` | `section6` | `exact-profile-behavior` | **PASS** | `proofs/section6-issue_network_external_write_standins-20261003T012819.701591Z-c39aea56.json` |
| `reject_missing_artifact` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_artifact-20261003T012820.324542Z-f87c2ef6.json` |
| `reject_missing_oracle` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_oracle-20261003T012820.332776Z-d58428f7.json` |
| `reject_missing_scoring_disposition` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_scoring_disposition-20261003T012820.341035Z-94d0a4f9.json` |
| `reject_incomplete_or_failed_termination` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_incomplete_or_failed_termination-20261003T012820.349253Z-3216cb6c.json` |
| `perturb_cache_identity` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_cache_identity-20261003T012820.357556Z-1c0600a5.json` |
| `perturb_profile_identity` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_profile_identity-20261003T012820.365789Z-aa9da3b5.json` |
| `perturb_core_identity` | `section6` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_core_identity-20261003T012820.374090Z-39b4e682.json` |
| `known_broken_both_arms_miss` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_binding_o3` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_null_variant_delegate` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_false_tension_closure_asserter` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_loss_before_destructive_boundary` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_unauthorized_write` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_version_self_adoption` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_legitimate_withholding` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_designed_termination` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `perturb_evaluator_identity` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `final_report_changed_files_tool_trace_assessment` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `chained_delegate_first_look` | `section6` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |

---

## 9. Integrity, Credential, and Disposition Closure

1. **Campaign Verification:**
   - The 22 recorded implementer-owned PASS proof artifacts satisfy the tooling's structural/hash checks. Whole-campaign `omp_stage7_admission.campaign_errors()` verification is **not clean**: it reports a non-PASS error for each of the 13 mandatory independent-inspection slots. The earlier zero-errors wording did not describe a successful whole-campaign verification. The historical command transcript for a separate successful proof-only check is not retained in this campaign.
   - Profile key, core hash, adapter hash, harness hash, build inventory, runtime closure, and host execution environment match across campaign, runs, and proofs.
   - Exactly the 13 designated independent-inspection obligations remain `PENDING` / `UNRESOLVED` (1 check + 12 Section 6 cells).

2. **Credential Leakage Screening:**
   - The credential scan checked 2,280 files and 124,038,609 bytes across the fresh campaign root using UTF-8 and UTF-16LE encodings for sensitive environment secrets.
   - Zero leaks or secret matches were found (0 matches).

3. **Final Lifecycle State:**
   - Runner admission disposition remains strictly **`CANDIDATE`** / **`UNADMITTED`**.
   - No code path created or mutated `status="ADMITTED"`.
   - Blinded Protocol 7 qualification subjects remain **strictly unauthorized** pending independent evaluator review, inspection of the 13 pending obligations, and formal runner admission.
