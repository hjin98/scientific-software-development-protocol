# Stage 7 OMP Independent Runner-Admission Review — NO-PASS — 2026-10-02

## Disposition

**NO-PASS**

**Serious Challenge:** none.

The governing architecture/qualification contract is coherent. The blocking defect is D4 admission enforcement: the qualification-mode profile-admission validator does not require the complete contract §6 matrix before accepting an `ADMITTED` executor record. A second review-closure limitation is that the persistent exact-profile campaign and its proof tree are host-local under `$HOME/ssdp70-omp-stagef/admission/` and were not available to this reviewer environment; repository summaries are not a substitute for the retained evidence the review contract requires.

Blinded Protocol 7 qualification remains **unauthorized**. No ADMITTED executor record was created or mutated, and no synthetic post-admission qualification-mode episode was run.

## Governing identities

- Governing SSDP: `6.6.0`
- Repository: `hjin98/scientific-software-development-protocol`
- Branch reviewed: `ssdp-7.0-scientific-epistemic-closure`
- Exact reviewed HEAD: `1bc0b5eb806216b092a3cc95e5f6074f2c787000`
- Expected HEAD: `1bc0b5eb806216b092a3cc95e5f6074f2c787000`
- HEAD comparison result: identical; no intervening commits.
- OMP executable implementation commit: `1715a8f0ddd6360d68c54afd650f32b037bcc2de`
- OMP adapter SHA-256 claimed by retained implementation records: `9ede18e4b69a1734637f77e3a99aec697fa5ab2c15772c5304defd1b3a192107`
- Frozen profile key: `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`
- Protocol 7 semantic subject p70: `db94a2dfb7fef480f37227eab5c45256e89901b8`
- Protocol 6.6 comparison arm p66: `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- Reported campaign root: `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/`

Comparison of executable implementation commit `1715a8f...` to reviewed HEAD `1bc0b5e...` shows four later commits changing only the Stage 7 OMP report/evidence Markdown records. The following executable/admission/profile-template/capability files are blob-identical between the implementation commit and reviewed HEAD: `adapters/omp.py`, `core70.py`, `harness70.py`, `omp_stage7_campaign.py`, `omp_stage7_admission.py`, `capabilities/omp-headless.json`, and `profiles/omp-headless.template.json`.

## Authority reconstructed

The review used the current `AGENTS.md`, the active SSDP 7.0 consolidated workplan, the Protocol 7.0 evaluation/qualification contract, and the current Stage 7 core/harness/OMP campaign/admission implementation.

The controlling admission rule is unambiguous:

1. all portable runner-admission requirements in contract §1 items 1–11 must pass;
2. the complete §6 runner/harness oracle-integrity matrix must pass through the exact adapter/profile;
3. a required cell not executed is blocking;
4. the implementer may only produce candidate evidence;
5. only a fresh independent checker may finalize the hash-bound `ADMITTED` executor bundle after deciding every §1 and §6 obligation;
6. only then may a harmless synthetic qualification-mode episode verify admission validation/snapshot/run-identity binding.

## Blocking finding B1 — qualification-mode admission does not enforce complete §6 closure

**Owner:** D4, `qualification/ssdp70/eval/core70.py` profile-admission validation/snapshot machinery.

**Consequence:** blocking.

`core70.validate_profile_admission()` validates:

- schema;
- `status == "ADMITTED"`;
- role;
- profile, adapter, core and capability identities; and
- the exact set of `_admission_checks_for_role("executor")`, which resolves to `EXECUTOR_ADMISSION_CHECKS`.

It does **not** require a `section6` field, does not require the exact `omp_stage7_admission.SECTION6_CELLS` set, and does not verify that every §6 cell is PASS with hash-bound evidence.

The same omission exists at the run snapshot boundary: `snapshot_profile_admission()` and `validate_profile_admission_snapshot()` copy/validate proof artifacts only for `_admission_checks_for_role(role)`. Even when a record happens to contain `section6`, the §6 proof artifacts are not part of the required snapshotted proof set.

### Local-compliance/global-failure falsification

A concrete counterexample is already encoded in `qualification/ssdp70/eval/test_portable70.py`:

- `write_admission()` creates an `ADMITTED` executor record containing only `EXECUTOR_ADMISSION_CHECKS` and no `section6` matrix.
- `test_admission_requires_exact_check_set_and_hashed_evidence` expects `core70.validate_profile_admission(..., role="executor") == []` for that record.

Therefore the assembled qualification gate can accept an ADMITTED executor whose §6 cells are absent, PENDING, FAIL, or otherwise never independently closed, provided the 12 executor checks are valid. This violates the workplan requirement that every §6 requirement be decided before admission and the qualification contract requirement that the §6 oracle-integrity suite gate qualification subjects.

This is not cured by `omp_stage7_admission.emit_candidate_bundle()` including a `section6` table. The final qualification-mode owner does not enforce that table.

### Minimum repair

Do not change OMP semantics, thresholds, fixtures, or scoring. Repair the generic executor admission mechanism so that an ADMITTED executor bundle and its run snapshot fail closed unless the complete governed §6 cell set is present, contains no unknown/missing cells, every cell is PASS, and every cited proof is hash-bound and available. Add counterfactual tests for at least:

- missing `section6`;
- one missing §6 cell;
- unknown §6 cell;
- PENDING/FAIL/UNRESOLVED §6 status;
- missing/tampered §6 proof;
- admitted-record snapshot omitting a §6 proof;
- candidate-to-admitted promotion while any §6 cell is not PASS.

The implementation should preserve the existing separation between the 12 canonical executor admission checks and the §6 oracle-integrity matrix; it need not collapse them into one namespace. It must, however, make complete §6 closure a mechanically enforced prerequisite of qualification mode.

## Review-evidence limitation E1 — retained campaign not available to this reviewer

The exact campaign/probe realizations and proof artifacts are retained only in the target-host persistent workspace. The repository contains detailed summaries and proof-path/hash claims, but the review instructions explicitly forbid promoting summary claims into PASS without inspecting the retained evidence and, where required, reproducing behavior.

This reviewer could inspect repository source and committed summaries, but could not access `/home/samjin/ssdp70-omp-stagef/admission/...` or re-execute the exact OMP/DeepInfra profile in the target host environment. Consequently the 13 checker-owned semantic/evaluator cells remain **UNRESOLVED in this review**, regardless of the implementation reports' candidate-evidence claims.

This limitation is independently blocking for this review, but it is not by itself evidence of an OMP semantic defect. A target-host independent checker may close these cells after B1 is repaired, using the preserved campaign.

## §1 items 1–11

| Item | Disposition | Independent review reason |
|---|---|---|
| 1. Exact subject/profile identity | UNRESOLVED | Repository/candidate identities were checked and executable sources are unchanged, but the frozen profile snapshot, host/runtime realization and retained exact-profile proof are host-local and were not independently inspected. |
| 2. Fresh arm isolation | UNRESOLVED | Source and summaries describe sequential arms and concurrent-pair isolation, but scheduler traces/private roots and retained run realizations were unavailable. |
| 3. Capability manifest completeness/enforcement | UNRESOLVED | Committed manifest/adapter machinery is inspectable, but exact frozen capability snapshot and real-boundary behavioral evidence were unavailable. |
| 4. Complete raw/equivalent trajectory and normalized stream | UNRESOLVED | Repository summaries report completeness; raw trajectories and normalized streams were not available for independent inspection. |
| 5. Raw-to-normalized completeness | UNRESOLVED | Completeness-map and native-event realizations were not independently inspected. |
| 6. Required evidence/scoring manifests | UNRESOLVED | Core ownership is present, but exact run-bound snapshots and retained oracle/scoring artifacts were unavailable. |
| 7. Fail-closed evidence/qualification states | UNRESOLVED | Source-level state separation is present; exact retained negative realizations were not independently reproduced here. |
| 8. Containment before effect | UNRESOLVED | Source/profile descriptions are coherent, but exact-profile hostile attempts and side-effect traces were unavailable. |
| 9. Custody/credential restrictions | UNRESOLVED | Exact target-host access/custody audit and attempt evidence were unavailable. |
| 10. Pair scheduling/concurrent isolation | UNRESOLVED | Driver source enforces the intended structure, but exact scheduler evidence was unavailable. |
| 11. Evidence/cache provenance | UNRESOLVED | Source binds extensive identities, but the retained proof/cache artifacts were unavailable for independent verification. |

No §1 item is promoted to PASS from a repository summary alone.

## §6 oracle-integrity matrix

The complete §6 gate is **FAIL at the assembled admission boundary** because qualification-mode admission does not require §6 closure (B1). Individual cell evidence dispositions in this reviewer environment are:

| §6 cell | Disposition | Reason |
|---|---|---|
| known_broken_both_arms_miss | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_wrong_binding_o3 | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_wrong_null_variant_delegate | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_false_tension_closure_asserter | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_loss_before_destructive_boundary | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_unauthorized_write | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_broken_version_self_adoption | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_good_legitimate_withholding | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| known_good_designed_termination | UNRESOLVED | checker-owned retained semantic evidence unavailable |
| reject_missing_artifact | UNRESOLVED | deterministic result is summarized in-repo, but retained falsification artifact was not independently inspected/re-executed |
| reject_missing_oracle | UNRESOLVED | same |
| reject_missing_scoring_disposition | UNRESOLVED | same |
| reject_incomplete_or_failed_termination | UNRESOLVED | same |
| perturb_cache_identity | UNRESOLVED | same |
| perturb_profile_identity | UNRESOLVED | same |
| perturb_core_identity | UNRESOLVED | same |
| perturb_evaluator_identity | UNRESOLVED | checker-owned retained evaluator evidence unavailable |
| catalog_contamination | UNRESOLVED | exact-profile prelaunch-refusal realization unavailable |
| containment_escape_attempts_retained | UNRESOLVED | exact-profile hostile-attempt realization unavailable |
| ordinary_entry_case_classes | UNRESOLVED | exact ordinary-entry trajectories unavailable |
| final_report_changed_files_tool_trace_assessment | UNRESOLVED | checker-owned retained assessment-input evidence unavailable |
| issue_network_external_write_standins | UNRESOLVED | exact-profile stand-in traces unavailable |
| chained_delegate_first_look | UNRESOLVED | checker-owned first-look evidence unavailable |

### Explicit 13 previously PENDING checker-owned obligations

| Obligation | Disposition | Concrete reason |
|---|---|---|
| withheld_oracle_branches | UNRESOLVED | Requires independent reconstruction of withheld classification/opportunity predicates and retained evidence; campaign not accessible. |
| known_broken_both_arms_miss | UNRESOLVED | No retained branch realization available to verify that aggregate gain cannot bypass the critical oracle. |
| known_broken_wrong_binding_o3 | UNRESOLVED | No retained branch realization available to inspect the real binding/O3 owner path. |
| known_broken_wrong_null_variant_delegate | UNRESOLVED | No retained branch realization available to distinguish correct gap/null/variant/delegate handling. |
| known_broken_false_tension_closure_asserter | UNRESOLVED | No retained semantic trajectory available to inspect closure/asserter handling. |
| known_broken_loss_before_destructive_boundary | UNRESOLVED | No retained trajectory available to verify loss is caught before the destructive boundary. |
| known_broken_unauthorized_write | UNRESOLVED | No retained hostile write trace/stand-in evidence available. |
| known_broken_version_self_adoption | UNRESOLVED | No retained semantic trajectory available to adjudicate version-bound self-adoption. |
| known_good_legitimate_withholding | UNRESOLVED | No retained known-good output available to verify legitimate withholding is accepted rather than over-rejected. |
| known_good_designed_termination | UNRESOLVED | No retained designed-termination trajectory available. |
| perturb_evaluator_identity | UNRESOLVED | No evaluator-admission/cache realization available to verify affected assessment reuse invalidation. |
| final_report_changed_files_tool_trace_assessment | UNRESOLVED | No retained evaluator input package available to verify final report, changed/new files and tool trace all reach assessment. |
| chained_delegate_first_look | UNRESOLVED | No retained first-look evidence available to verify the hidden anomaly is inaccessible from the cheap at-hand view. |

## Oracle-strength challenge

The smallest semantically wrong assembled behavior found is not inside one OMP trajectory; it is at admission composition:

> Every currently defined executor admission proof can be valid while the complete §6 matrix is missing, yet the qualification-mode validator can still accept an `ADMITTED` executor record.

This defeats the global invariant while leaving the locally validated executor-check set green. It is therefore a genuine compositional failure, not a manufactured defect.

Other oracle-strength questions remain open until the target-host campaign is inspected: transcript completeness, tool/catalog bijection, containment-before-effect, evaluator identity, final-report/changed-file/tool-trace delivery, pair isolation and append-only provenance cannot be independently strengthened or weakened from summaries alone.

## Checks performed

Performed:

- exact branch-head comparison against the requested HEAD: identical;
- implementation-commit to reviewed-HEAD comparison: four later changes, all report/evidence Markdown only;
- blob-identity comparison between implementation commit and reviewed HEAD for OMP adapter, core, harness, campaign, admission owner, OMP capability manifest and OMP profile template: all identical;
- independent reconstruction of §1 and §6 requirements from the current qualification contract/workplan;
- source inspection of `EXECUTOR_ADMISSION_CHECKS`, §6 cell classification/evidence classes, candidate-bundle emission, ADMITTED validation, admission hashing/snapshotting and current admission tests;
- local-compliance/global-failure falsification by source-level counterexample using the existing portable admission test construction.

Not performed / unavailable:

- target-host persistent campaign inspection;
- direct reading/hash verification of campaign proofs, raw traces, scheduler traces or synthetic/evaluator outputs;
- exact OMP/DeepInfra re-execution;
- post-admission synthetic qualification-mode run, because admission is not authorized.

## Evidence reuse and staleness

Repository summaries for the 34-run exact-profile campaign, real-provider probe, deterministic falsification, credential scan and test regressions were treated as navigation/evidence claims only. They were **not** promoted to independent PASS because their retained source artifacts were not available.

Earlier campaign/profile realizations identified by the implementation records as superseded were not reused.

The current executable candidate remains byte-stable relative to implementation commit `1715a8f...` for the inspected source/profile-template/capability surfaces.

## Earliest owning blocker and bounded repair

**Earliest blocker:** D4 generic profile-admission validation/snapshot contract in `core70.py`, not OMP-specific semantics and not D3 authority.

Minimum repair:

1. make the complete governed §6 matrix mandatory for executor `ADMITTED` validation;
2. hash-bind and snapshot every §6 proof needed to validate the admitted record;
3. fail closed on missing/unknown/non-PASS/tampered §6 cells/proofs;
4. add direct counterfactual regression tests for those failures;
5. rerun the affected admission/campaign regression;
6. run a fresh independent Stage 7 review on the target host with direct access to the preserved exact campaign;
7. only if every §1 and §6 obligation then passes, finalize ADMITTED and execute the harmless synthetic qualification-mode gate.

No OMP-specific scoring exception, contract relaxation, fixture change, threshold change or transfer of another runner's evidence is warranted.

## Final authorization state

**NO-PASS.**

The OMP runner remains **CANDIDATE / UNADMITTED** for Protocol 7 qualification. Blinded Protocol 7 qualification remains unauthorized by this review.

No admission bundle identity or synthetic post-admission result exists because admission did not occur.
