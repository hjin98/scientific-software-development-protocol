# Stage 7 OMP Snapshot Rebinding Repair Report — 2026-10-02

## 1. Executive Summary & Disposition

- **Governing Protocol:** Scientific Software Development Protocol (SSDP) `6.6.0`
- **Starting HEAD:** `13a61f6b7cd60a440b0dce4d6968228727cd2acf` (Record Stage 7 OMP Section 6 admission repair and counterfactual verification report)
- **Repository:** `hjin98/scientific-software-development-protocol`
- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Repair Domain:** D4 executable concretization (canonical admission bundle digest recomputation from snapshot material)
- **Defect Closed:** Coherent-rebinding vulnerability in `validate_profile_admission_snapshot()`, which previously trusted `snapshot["admission_bundle_sha256"]` against run identity without independently recomputing the canonical bundle digest from archived record payload and archived proof file bytes.
- **Runner Lifecycle State:** Strictly **`CANDIDATE`** / **`UNADMITTED`**
- **Blinded Qualification Authorization:** Blinded Protocol 7 qualification remains **strictly unauthorized** pending fresh independent runner-admission PASS.
- **Serious Challenges:** **NONE**. Governing architecture and qualification contracts are coherent; defect was confined to D4 snapshot validation in `core70.py`.

---

## 2. Commit Ancestry

- **Starting HEAD:** `13a61f6b7cd60a440b0dce4d6968228727cd2acf`
  - Verified clean working tree and matching git rev-parse HEAD before implementation.
- **Intervening Commit Review:**
  - `13a61f6b7cd60a440b0dce4d6968228727cd2acf`: Recorded Stage 7 OMP Section 6 admission repair report and counterfactual verification.
  - `1ce2db1b3d92d01c4ab2cafd7767db116d51274c`: Enforced mandatory Section 6 oracle-integrity closure in executor admission.
- **D4 Executable Implementation Commit:** `ba11ad846a669ff9e34fb726a9c9a753d412d756`

---

## 3. Files Changed and Architectural Reason

1. `qualification/ssdp70/eval/core70.py`:
   - **Architectural Reason:** D4 generic profile-admission and evidence-validation owner.
   - Factored canonical admission-bundle digest computation into `compute_admission_bundle_sha256(record, check_evidence, *, role="executor", section6_evidence=None)`:
     - Enforces exact required check set in `check_evidence`;
     - For `role="executor"`, enforces presence of `section6` in `record` and exact 23-cell `EXECUTOR_SECTION6_CELLS` set in `section6_evidence`;
     - Returns `stable_json_sha256({"record": record, "evidence": evidence})` with unified digest semantics across all callers.
   - Refactored `admission_bundle_sha256(admission_path, role=role)` to reuse `compute_admission_bundle_sha256()`.
   - Added `recompute_profile_admission_snapshot_bundle_sha256(run, *, role="executor", prefix="profile-admission")` to recompute the canonical bundle digest directly from snapshotted material on disk.
   - Updated `validate_profile_admission_snapshot()` to:
     - Hash each snapshotted proof file directly from disk;
     - Validate individual proof size, hash against snapshot row, and hash against record row;
     - Recompute the canonical admission bundle digest using `compute_admission_bundle_sha256()` from the archived `record` and actual proof bytes on disk;
     - Fail closed if the recomputed bundle digest does not match the `expected_bundle_sha256` frozen into run identity (`f"{role} profile-admission recomputed bundle does not match run identity"`);
     - Fail closed if `snapshot["admission_bundle_sha256"]` does not match the recomputed digest (`f"{role} profile-admission snapshot bundle does not match recomputed digest"`);
     - Fail closed if proof set is incomplete (`f"{role} profile-admission bundle cannot be recomputed: incomplete proof set"`).

2. `qualification/ssdp70/eval/test_portable70.py`:
   - **Architectural Reason:** Portable qualification harness test suite.
   - Added focused counterfactual test `test_snapshot_rejects_coherent_rebinding_tamper_of_section6_proof`:
     - Creates valid admitted executor snapshot;
     - Captures original admission bundle digest;
     - Alters an archived Section 6 proof file on disk;
     - Updates `evidence_sha256` in the archived `profile-admission.json` record;
     - Updates `sha256` and `bytes` in `profile-admission-snapshot.json` `section6_proofs`;
     - Updates `record_sha256` in `profile-admission-snapshot.json`;
     - Leaves `snapshot["admission_bundle_sha256"]` untouched (equal to run identity);
     - Proves `validate_profile_admission_snapshot()` rejects the coherently rewritten archive because the recomputed digest differs from run identity.
   - Added equivalent coverage for ordinary executor check proof in `test_snapshot_rejects_coherent_rebinding_tamper_of_ordinary_check_proof`.
   - Added equivalent coverage for evaluator admission in `test_snapshot_rejects_coherent_rebinding_tamper_for_evaluator_role`.

3. `qualification/ssdp70/STAGE-7-OMP-SNAPSHOT-REBINDING-REPAIR-REPORT-2026-10-02.md`:
   - **Architectural Reason:** Durable audit and repair record.

---

## 4. Repaired Invariants

| Invariant | Scope | Enforcement Point | Behavior |
|---|---|---|---|
| **I1: Single Canonical Bundle Digest** | Protocol-wide | `core70.compute_admission_bundle_sha256()` | One shared digest function for pre-launch, snapshotting, and post-run validation; zero parallel digest semantics. |
| **I2: Byte-Reproducible Bundle Digest** | Architecture | `core70.py` | Digest binds complete record payload + SHA-256 of every required ordinary check proof + (for executor) every required 23 Section 6 cell proof. |
| **I3: Snapshot Recomputation & Verification** | Run Archive | `core70.validate_profile_admission_snapshot()` | Independently recomputes bundle digest from archived record and actual proof bytes on disk, comparing directly against run identity. |
| **I4: Coherent Rebinding Fail-Closed** | Attack Mitigation | `core70.validate_profile_admission_snapshot()` | Even when proof metadata, record metadata, and snapshot hashes are consistently updated, snapshot validation rejects if the recomputed bundle does not match run identity. |
| **I5: Evaluator & Executor Generic Support** | Roles | `core70.py` | Both executor (12 checks + 23 §6 cells) and evaluator (6 checks) benefit from identical recomputation and anti-rebinding guarantees. |

---

## 5. Counterfactual Tests Added

1. **`test_snapshot_rejects_coherent_rebinding_tamper_of_section6_proof`:**
   - Alters one archived Section 6 proof file on disk (`section6-known_broken_both_arms_miss.proof`).
   - Coherently updates `record["section6"][target]["evidence_sha256"]`.
   - Coherently updates snapshot `section6_proofs` row `sha256` and `bytes`.
   - Coherently updates `snapshot["record_sha256"]`.
   - Leaves `snapshot["admission_bundle_sha256"]` untouched.
   - Verifies all isolated metadata checks pass.
   - Proves `validate_profile_admission_snapshot()` fails closed with:
     - `"executor profile-admission recomputed bundle does not match run identity"`
     - `"executor profile-admission snapshot bundle does not match recomputed digest"`

2. **`test_snapshot_rejects_coherent_rebinding_tamper_of_ordinary_check_proof`:**
   - Applies the coherent rebinding attack to an ordinary executor check proof (`schema_and_profile_identity.proof`).
   - Proves `validate_profile_admission_snapshot()` fails closed with recomputed bundle mismatch.

3. **`test_snapshot_rejects_coherent_rebinding_tamper_for_evaluator_role`:**
   - Applies the coherent rebinding attack to an evaluator admission proof (`evaluator_schema_and_profile_identity.proof`).
   - Proves `validate_profile_admission_snapshot()` fails closed with recomputed bundle mismatch for `role="evaluator"`.

---

## 6. Commands and Tests Actually Executed

| Command | Tests | Result | Duration | Notes |
|---|---|---|---|---|
| `PYTHONPATH=qualification/ssdp70/eval python3 -m unittest qualification/ssdp70/eval/test_portable70.py` | 30 | **PASS** | 0.306s | Includes all 3 new counterfactual tests |
| `PYTHONPATH=qualification/ssdp70/eval python3 -m unittest qualification/ssdp70/eval/test_omp_stage7_admission.py qualification/ssdp70/eval/test_omp_stage7_campaign.py` | 31 | **PASS** | 0.110s | Campaign driver and admission lifecycle suites |
| `PYTHONPATH=qualification/ssdp70/eval python3 -m unittest qualification/ssdp70/eval/test_harness_integration.py` | 9 | **PASS** | 0.474s | Harness integration and mock evaluator validation |
| `PYTHONPATH=qualification/ssdp70/eval python3 -m unittest qualification/ssdp70/eval/test_omp_units.py` | 73 | **PASS** | 6.420s | Full OMP unit regression |
| `PYTHONPATH=qualification/ssdp70/eval python3 -m unittest qualification/ssdp70/eval/test_control_path_policy.py test_mcp_stdio.py test_stage_f_integrity_repairs.py test_stage_f_v4_repairs.py` | 114 | **PASS** | 2.800s | Stage F regression suite |
| `python3 -m unittest discover -s tests` | 407 | **PASS** (3 skipped) | 16.555s | Repository-wide test suite |
| `python3 source/release_state.py` | N/A | **PASS** | < 0.1s | `release state is coherent` |
| `python3 source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` | N/A | **PASS** | < 0.1s | `PEM schema 1 valid: 5 families, 0 notices` |
| `python3 source/build_skills.py --output /tmp/protocol-dist` | N/A | **PASS** | < 0.1s | Built all 7 canonical skills |
| `python3 source/validate_packages.py --dist /tmp/protocol-dist` | N/A | **PASS** | 0.6s | `all generated Protocol skill directory bundles and ZIPs are structurally valid` |
| `python3 source/check_dist.py --expected /tmp/protocol-dist --committed dist` | N/A | **PASS** | 0.4s | `committed dist matches the fresh canonical build semantically` |
| `git diff --check` | N/A | **PASS** | < 0.1s | Zero whitespace or formatting errors |

---

## 7. Resulting Identities & Evidence Applicability

- **`core70.py` SHA-256:** `7896563b99d07ca20e94d7203958c8d63810452b2dfa308cee46adeae4aacf9f`
- **`adapters/omp.py` SHA-256:** `9ede18e4b69a1734637f77e3a99aec697fa5ab2c15772c5304defd1b3a192107`
- **`omp_stage7_admission.py` SHA-256:** `e600e94a78825b038ead7007e0ed56b502ed2fac0feed9e7854cc194ea85d516`
- **`omp_stage7_campaign.py` SHA-256:** `4e6cd557ec5eb7b6795d22a46835798caa17642c6c94697ac4c9b7e0aaf63bf8`
- **`capabilities/omp-headless.json` File SHA-256:** `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd`
- **`capabilities/omp-headless.json` Canonical Stable JSON SHA-256:** `f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55`
- **Frozen Profile Key SHA-256:** `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`
- **Protocol 7 Semantic Subject `p70`:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **Protocol 6.6 Comparison Arm `p66`:** `22f4bdba53795da3a6f13f162529f3a843fc37ae`

### Fresh Campaign Execution Status

- **Real Provider Access:** Provisioned via environment variable `SSDP70_DEEPINFRA_API` mapped to `SSDP70_OMP_PROVIDER_CREDENTIAL`.
- **Evidence Applicability Rule Enforced:** Per workplan instructions and PEM `PC-001`, modifying `core70.py` changed the qualification core identity (`7896563b...`). Prior campaign evidence bound to earlier core versions was superseded. Historical evidence was preserved intact under `$HOME/ssdp70-omp-stagef/admission/` and not rewritten.
- **Fresh Campaign Executed:** A complete fresh exact-profile campaign was executed and bound to committed candidate HEAD `d50dcb539334582cd8a848dcc0d72ed5c7f4f897` and profile key `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`:
  - Campaign root: `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound/`
  - All 34 positive realizations reached `COMPLETE_ADMISSIBLE`; contamination case cleanly refused at prelaunch.
  - Deterministic falsification passed across all 11 perturbation/rejection cases.
  - All 22 implementer-provable proofs recorded and verified with zero errors.
  - Full campaign result documented in `qualification/ssdp70/STAGE-7-OMP-EXACT-PROFILE-CAMPAIGN-RESULT-2026-10-03.md`.

---

## 8. Fresh Exact-Profile Stage 7 Campaign Execution Record

The complete fresh campaign was executed via:

```bash
# 1. Freeze replacement profile and initialize campaign
CANDIDATE_HEAD=$(git rev-parse HEAD)
CAMPAIGN=$(PYTHONPATH=qualification/ssdp70/eval python3 qualification/ssdp70/eval/omp_stage7_campaign.py freeze-inherit \
  --source-profile "$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/profile-snapshot.json" \
  --source-capabilities "$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/capability-manifest-snapshot.json" \
  --executable "$HOME/.local/bin/omp" \
  --capabilities qualification/ssdp70/eval/capabilities/omp-headless.json \
  --candidate-head "$CANDIDATE_HEAD" \
  --semantic-subject db94a2dfb7fef480f37227eab5c45256e89901b8 \
  --profile-id "omp-headless-deepinfra-glm53-flash-stage7-hostbound-$CANDIDATE_HEAD" \
  --expect-provider-id deepinfra \
  --expect-model-id zai-org/GLM-5.3-Flash \
  --expect-upstream https://api.deepinfra.com/v1/openai \
  --expect-source-profile-key 86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10 \
  --label hostbound)

# 2. Materialize arms and prepare synthetic corpus
ARMS=$(PYTHONPATH=qualification/ssdp70/eval python3 qualification/ssdp70/eval/omp_stage7_campaign.py prepare-arms --campaign "$CAMPAIGN" --repo .)
PYTHONPATH=qualification/ssdp70/eval python3 qualification/ssdp70/eval/omp_stage7_campaign.py prepare --campaign "$CAMPAIGN"

# 3. Execute positive exact-profile matrix and contamination test
export SSDP70_OMP_PROVIDER_CREDENTIAL="$SSDP70_DEEPINFRA_API"
unset SSH_AUTH_SOCK
EXECUTION_ROOT=$(PYTHONPATH=qualification/ssdp70/eval python3 qualification/ssdp70/eval/omp_stage7_campaign.py run-exact \
  --campaign "$CAMPAIGN" --arms-manifest "$ARMS" --arm p66 --arm p70 --parallel 2)

# 4. Execute deterministic falsification
PYTHONPATH=qualification/ssdp70/eval python3 qualification/ssdp70/eval/omp_stage7_campaign.py falsify \
  --campaign "$CAMPAIGN" --base-run "$EXECUTION_ROOT/positive-matrix/S7-ORD-D4-p70-r0"

# 5. Record proofs and verify campaign
# (Recorded 22 proofs across checks and §6 cells; verified via omp_stage7_admission.campaign_errors)
```

---

## 9. Open Independent-Inspection Obligations

The 13 independent-inspection obligations remain strictly **`PENDING`** / **`UNRESOLVED`**:

1. `withheld_oracle_branches`
2. `known_broken_both_arms_miss`
3. `known_broken_wrong_binding_o3`
4. `known_broken_wrong_null_variant_delegate`
5. `known_broken_false_tension_closure_asserter`
6. `known_broken_loss_before_destructive_boundary`
7. `known_broken_unauthorized_write`
8. `known_broken_version_self_adoption`
9. `known_good_legitimate_withholding`
10. `known_good_designed_termination`
11. `perturb_evaluator_identity`
12. `final_report_changed_files_tool_trace_assessment`
13. `chained_delegate_first_look`

Admission tooling (`omp_stage7_admission.py`) fails closed whenever any §6 cell is pending or non-PASS.

---

## 10. Final Lifecycle State & Authorization

- **Runner Lifecycle State:** **`CANDIDATE`** / **`UNADMITTED`**
- **No Self-Authorization:** No code path created or mutated `status="ADMITTED"`.
- **Synthetic Qualification Mode Episode:** Not executed, because admission did not occur.
- **Blinded Qualification Hold:** Execution of blinded Protocol 7 qualification subjects remains strictly **unauthorized** pending fresh independent runner-admission PASS.
