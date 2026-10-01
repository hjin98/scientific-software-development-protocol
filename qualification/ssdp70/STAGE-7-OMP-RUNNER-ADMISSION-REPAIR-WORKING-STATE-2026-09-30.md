# OMP-only Stage F — Stage 7 runner-admission repair working state

- **Date:** 2026-09-30 (America/Chicago; 2026-10-01 UTC)
- **Governing SSDP:** 6.6.0
- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Starting independent NO-PASS:** `5fc2051d97e670a289b93eaddebc4297170b83cd`
- **Current implementation head at this record:** `c13a90703437897e870584e02378a8e537c5d8de`
- **State:** **SOURCE REPAIR IMPLEMENTED; TARGET-HOST ACCEPTANCE AND STAGE 7 ADMISSION EVIDENCE NOT YET EXECUTED. OMP REMAINS UNADMITTED.**

This record is resumability/evidence state only. It does not admit OMP, qualify Protocol 7, or replace the independent Stage 7 review.

## Implemented bounded repair

1. The active SSDP 7.0 workplan now contains the Stage 7 repair tranche separating the concrete host-identity defect from the missing exact-profile admission campaign.
2. The OMP containment policy now freezes a canonical `host_execution_environment` containing:
   - kernel sysname/release/version/machine;
   - canonical OS-release digest plus ID/VERSION_ID;
   - qualification-supervisor Python implementation/version/executable digest.
3. `freeze_profile()` captures that host identity. `profile_errors()` independently re-observes it and rejects a migrated host before realization/launch. The actual observed host object is retained in containment realization evidence.
4. The host object is inside the existing containment policy and therefore inside the existing profile key. The prior profile key `86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10` and live probe `509d8459969962f9fc793c6aecd717894408b3ee1a4e7feb4db4f6bc4f362e1f` are historical evidence only after this change.
5. Focused unit coverage was added for profile-key binding and migration refusal.
6. `qualification/ssdp70/eval/omp_stage7_admission.py` now owns persistent candidate campaign evidence under `$HOME/ssdp70-omp-stagef/admission/`. It binds one exact profile, retains hash-addressed proof attempts for the exact `core70.EXECUTOR_ADMISSION_CHECKS` set and the required §6 matrix, rejects evidence-class substitution where exact-profile behavior is required, and emits only `status=CANDIDATE`.
7. The campaign code has no `status=ADMITTED` emission path. A fresh independent checker remains the only context allowed to finalize an executor admission record.
8. OMP harness realizations are now authorized under the persistent `admission/` root in addition to `probes/` and `qualification/`, so exact-profile Stage 7 evidence can be produced through the real harness without relocating it into the source repository.

## Evidence applicability

The source changes modify the OMP adapter and profile template, so all previous OMP profile-bound live evidence is stale for the replacement profile. Historical records remain immutable. Stage 6 regression evidence remains useful only as regression design/evidence for unaffected properties and must not be relabeled as exact-profile Stage 7 admission evidence.

PEM basis remains the workplan-bound accepted memory `PROJECT-ENGINEERING-MEMORY.md@23e46543c174a8451bbadc402df63538105eab10`: `DS-001=APPLICABLE` for proxy/evidence-scope discipline and `PC-001=APPLICABLE` for immutable historical profile/evidence preservation.

## Unexecuted mandatory acceptance

This implementation context could modify and inspect the connected repository but did not have the operator's target-host OMP executable/runtime-closure workspace or a configured repository CI workflow. Therefore the following remain **UNEXECUTED/BLOCKING**, not PASS:

1. focused new Stage 7 tests;
2. the complete affected portable/Claude/MCP/Stage-F/OMP suite on the exact repaired head, with zero required skips;
3. replacement exact-profile freeze on the actual qualification host;
4. a fresh real-provider OMP probe for that replacement profile;
5. the exact-profile Stage 7 executor-admission campaign and complete §6 branch matrix under `$HOME/ssdp70-omp-stagef/admission/`;
6. independent inspection/re-execution and finalization of the hash-bound `ADMITTED` executor bundle;
7. the harmless qualification-mode dry run using that independently admitted bundle.

No Protocol 7 qualification subject may run before all seven close.

## Resume sequence on the authorized target host

1. Update the local branch to this record's descendant head and verify there are no intervening unreviewed executable changes.
2. Ensure `$HOME/ssdp70-omp-stagef/{runtime-closures,probes,admission,qualification,logs}` remain writable persistent workspace roots.
3. Run the focused Stage 7 unit tests, then the full affected exact-head suite. Any required skip/failure is blocking.
4. Freeze a **new** OMP profile from the repaired template on that host. Record the new profile key and host-execution object; do not mutate the prior profile.
5. Run a fresh append-only real-provider probe for the new profile. Required successful semantics remain `execution_mode=probe`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED`.
6. Initialize the candidate Stage 7 campaign with `omp_stage7_admission.py init`, execute the exact-profile and deterministic-falsification evidence matrix required by the workplan, and record every proof under that campaign. `verify` must be clean before `emit-candidate`.
7. Hand the resulting `profile-admission-candidate.json`, campaign evidence and fresh probe to a fresh independent Stage 7 checker. The implementer must not change its status to `ADMITTED`.
8. After independent PASS/finalization, run one harmless synthetic qualification-mode episode proving admission-bundle validation/snapshot/run-identity binding. Only then may blinded Protocol 7 qualification subjects begin.
