# OMP-only Stage F — Stage 7 runner-admission repair working state

- **Date:** 2026-09-30 (America/Chicago; 2026-10-01 UTC)
- **Governing SSDP:** 6.6.0
- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Starting independent NO-PASS:** `5fc2051d97e670a289b93eaddebc4297170b83cd`
- **Executable repair head before this coordination-only record:** `98a710a906804d39d8709271fed6e2caae33721b`
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
9. `omp_stage7_campaign.py` now provides the target-host driver: it can inherit the approved Stage 6 provider/model/reasoning/budget route into a newly frozen host-bound profile, materialize the exact frozen Protocol 6.6 and Protocol 7 arm packages from immutable Git commits, build the bounded non-custody Stage 7 corpus, execute the exact-profile matrix, retain pair-scheduler evidence, and run deterministic core/harness falsification.
10. Campaign creation is bound to the exact executing checkout: the supplied `candidate_head` must equal `git rev-parse HEAD`. `freeze-inherit` additionally requires the exact historical source-profile key and matching source capability snapshot; route inheritance fails closed on provider/model/upstream/API drift.
11. Exact-profile proof records must point to real harness realizations whose retained profile/capability/core/harness/adapter/support identities match the campaign. Positive exact-profile claims require at least one `COMPLETE_ADMISSIBLE` realization. The catalog-contamination claim instead requires a structurally valid retained prelaunch refusal; an unrelated execution failure cannot serve as behavioral proof.
12. Pair scheduling is now retained as `matrix-scheduler.jsonl`. The Stage 7 driver validates sequential arms within each pair, complete pair realization, and actual monotonic-time overlap of at least two independent pairs.
13. Evidence classes are now aligned to their semantic owners. Exact runtime/containment cells accept only `exact-profile-behavior`; mechanically decidable missing-evidence/cache/profile/core cells accept only `deterministic-falsification`; semantic known-good/known-broken branches, evaluator-identity perturbation, assessment-input completeness, chained-delegate first-look, and the executor `withheld_oracle_branches` check accept `independent-inspection`. This prevents the implementer from closing semantic checker obligations with a structural proxy.
14. The campaign remains candidate evidence only. No source path emits `status=ADMITTED`; the independent checker must supply the independent semantic/evaluator proof cells and finalize admission separately.

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

The approved Stage 6 route source is the successful historical realization:

- profile: `$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/profile-snapshot.json`
- capability snapshot: `$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/capability-manifest-snapshot.json`
- historical source-profile key: `86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10`

These are route/configuration inputs only; their prior profile/probe evidence remains stale for the replacement profile.

1. Sync this branch to the exact current descendant, require a clean worktree, and set `CANDIDATE_HEAD=$(git rev-parse HEAD)`. Do not freeze against one commit and execute another.
2. Ensure `$HOME/ssdp70-omp-stagef/{runtime-closures,probes,admission,qualification,logs}` remain persistent writable roots and inject the approved provider credential only through the reviewed secret/environment path.
3. Execute focused Stage 7 tests followed by the complete affected exact-head suite. Any required failure/skip is blocking:

   `python3 -m unittest qualification.ssdp70.eval.test_omp_stage7_admission qualification.ssdp70.eval.test_omp_stage7_campaign qualification.ssdp70.eval.test_omp_units -v`

   `python3 -W ignore -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -q`

4. Freeze the replacement host-bound profile and create the candidate campaign through the approved route:

   `CAMPAIGN=$(python3 qualification/ssdp70/eval/omp_stage7_campaign.py freeze-inherit --source-profile "$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/profile-snapshot.json" --source-capabilities "$HOME/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/out/E1-p70-r0/capability-manifest-snapshot.json" --executable "$HOME/.local/bin/omp" --capabilities qualification/ssdp70/eval/capabilities/omp-headless.json --candidate-head "$CANDIDATE_HEAD" --semantic-subject db94a2dfb7fef480f37227eab5c45256e89901b8 --profile-id "omp-headless-deepinfra-glm53-flash-stage7-hostbound-$CANDIDATE_HEAD" --expect-provider-id deepinfra --expect-model-id zai-org/GLM-5.3-Flash --expect-upstream https://api.deepinfra.com/v1/openai --expect-source-profile-key 86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10 --label hostbound)`

   Retain the new profile key and `host_execution_environment`. The key must not be relabeled as the historical `86da2241…` profile.

5. Materialize the immutable arms and prepare the bounded Stage 7 corpus:

   `ARMS=$(python3 qualification/ssdp70/eval/omp_stage7_campaign.py prepare-arms --campaign "$CAMPAIGN" --repo .)`

   `python3 qualification/ssdp70/eval/omp_stage7_campaign.py prepare --campaign "$CAMPAIGN"`

6. Execute the exact-profile campaign:

   `EXECUTION_ROOT=$(python3 qualification/ssdp70/eval/omp_stage7_campaign.py run-exact --campaign "$CAMPAIGN" --arms-manifest "$ARMS" --arm p66 --arm p70 --parallel 2)`

   Its execution summary must PASS; positive runs must be `COMPLETE_ADMISSIBLE`; the contamination case must be a validated prelaunch refusal; scheduler validation must prove sequential arms plus overlapping independent pairs.

7. Select a complete positive Protocol 7 realization under `$EXECUTION_ROOT` and run deterministic falsification:

   `python3 qualification/ssdp70/eval/omp_stage7_campaign.py falsify --campaign "$CAMPAIGN" --base-run "<complete-p70-run-directory>"`

   This can close only the mechanically discriminated core/harness cells. It must not be used as semantic §6 evidence.

8. Run a fresh append-only real-provider probe for the replacement profile under `$HOME/ssdp70-omp-stagef/probes/`. Required successful semantics remain `execution_mode=probe`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED`.

9. A fresh independent custody/evaluator checker must then produce the remaining `independent-inspection` proof cells: the §11.3 known-broken/known-good semantic branches, evaluator-identity perturbation, final-report/changed-file/tool-trace assessment-input completeness, chained-delegate first-look, and the aggregate `withheld_oracle_branches` executor check. Exact-profile and deterministic proof classes cannot substitute for these cells.

10. After every campaign slot is independently supportable, the independent checker may verify the candidate campaign and finalize the hash-bound executor admission record as `ADMITTED`. The implementation context must not perform that promotion.

11. After independent PASS/finalization, run one harmless synthetic qualification-mode episode proving admission validation, snapshotting and run-identity binding. Only after that dry run passes may blinded Protocol 7 qualification subjects execute.
