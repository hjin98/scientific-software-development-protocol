---
kind: ssdp63-f4-independent-review-repair-result
protocol_version: 6.3.0
candidate_under_test: 42eb89388dc96879157ba92db9e7f3c59f2c0b36
accepted_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
public_source_bootstrap: 42eb89388dc96879157ba92db9e7f3c59f2c0b36
replaces_public_source_bootstrap: dc22f09fd38dbbfeaeb0160152da9b284654f66e
prior_f3_candidate: 026eecf6ce382c3445ed218aeca80dcf2fb9a426
independent_review: pending
authority: non-normative-qualification-evidence
stage_g: blocked
---

# Protocol 6.3 F4 Independent-Review Repair Qualification

## Disposition

**IMPLEMENTATION-CONTEXT REPAIR QUALIFICATION PASS** for immutable semantic candidate `42eb89388dc96879157ba92db9e7f3c59f2c0b36`.

This result does not establish independent Protocol/D3 Review PASS, Protocol 6.3 recovery, accepted-current status, workplan closure, or `main` cutover. Accepted current remains Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`; Stage G remains blocked.

## Replacement public bootstrap

The previous Protocol 6.3 public source bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` is retained as historical evidence but is no longer the current 6.3 fallback because the independent-review repair changed canonical source semantics. This later descendant publishes the already-existing repaired source snapshot `42eb89388dc96879157ba92db9e7f3c59f2c0b36` as the replacement self-reference-safe public source bootstrap. The bootstrap identity is therefore the immutable semantic candidate itself; publication occurs only here, after that candidate already exists.

The repaired candidate was assembled and validated before this publication. It does not self-name this later publication record and remains distinct from Protocol 6.3 recovery/accepted-current state.

## Fresh mechanical discriminators

`tests/test_protocol_63_independent_review_repairs.py` supplies executable valid/counterfactual discrimination for the seven independent-review blockers:

| Case | Repaired claim | Executable discriminator |
| --- | --- | --- |
| D8-01 | accepted family IDs cannot silently change semantic identity; mechanically material kind/owner/mechanism changes require new/reclassified identity and lineage | `test_d8_01_same_id_semantic_drift_rejected` |
| D8-02 | overlay binds exact workflow-selected accepted PEM publication, separate from accepted project state | `test_d8_02_overlay_uses_exact_accepted_pem_publication` |
| D8-03 | declared stable locator participates in evidence/authority binding health | `test_d8_03_missing_stable_locator_is_not_healthy` |
| D8-04 | mechanism-specific cause claim requires discriminating cause evidence | `test_d8_04_mechanism_cause_requires_cause_evidence` |
| D8-05 | unqualified positive guidance requires bounded counterevidence-search disposition | `test_d8_05_wins_only_positive_guidance_rejected` |
| D8-06 | unresolved high-impact notice precedes lower-consequence optional positive guidance | `test_d8_06_unresolved_notice_precedes_positive_guidance` |
| D8-07 | temperature-override evidence is parsed and participates in material route health | `test_d8_07_temperature_override_evidence_is_material` |

The formerly non-discriminating/mis-bound qualification mappings are superseded for the repaired candidate as follows:

- Q63-06 -> D8-03
- Q63-13 -> D8-07
- Q63-42 -> D8-05
- Q63-64 -> D8-02
- Q63-66 -> D8-04
- Q63-69 -> D8-06
- Q63-71 -> D8-01
- F63-Y -> D8-05
- F63-AU -> D8-02
- F63-AW -> D8-04
- F63-AZ -> D8-06
- F63-BB -> D8-01

F2/F3 records remain immutable historical evidence. They are not relabelled as current proof. Unaffected prior semantic assessments are reusable only where the F4 repair cannot plausibly alter their claim, oracle, candidate-facing behavior, or frozen resource; shared executable surfaces received fresh candidate-bound regression evidence.

## Fresh assembled-candidate execution

GitHub Actions run `34689279877` assembled the repaired candidate from the reopened workplan and completed successfully. Before committing the semantic candidate it executed, in order:

1. all seven D8 independent-review repair discriminators — PASS;
2. the Protocol 6.3 PEM/reopened/repair regression — PASS;
3. full repository unittest discovery — PASS;
4. self-hosted `PROJECT-ENGINEERING-MEMORY.md` validation — PASS;
5. canonical skill distribution regeneration, independent package validation, and committed distribution parity — PASS;
6. removal of temporary execution-only repair machinery from the Git tracked-file view before containment checks — PASS;
7. current Protocol 6.3 profile regeneration/check and frozen Protocol 5.16/6.0/6.1/6.2 snapshot coherence — PASS;
8. Orchestrator Core acceptance — PASS;
9. final whitespace, D8, and self-hosted PEM checks — PASS;
10. semantic candidate commit `42eb89388dc96879157ba92db9e7f3c59f2c0b36` — PASS.

The temporary repair scripts/workflow and interim diagnostics were removed before the semantic candidate commit and are not part of `42eb89388dc96879157ba92db9e7f3c59f2c0b36`.

## Repair realization

The repair stays at existing owners rather than adding a second compliance layer:

- `source/project_engineering_memory.py` now realizes locator health, material temperature/counterevidence routes, causal-warrant checks, structured positive-guidance admission, unresolved-notice salience, semantic reconciliation, and exact accepted-PEM overlay binding;
- `source/shared/references/project-engineering-memory.md` records the strengthened canonical semantics;
- `source/shared/templates/project_engineering_memory_template.md` exposes the structured counterevidence-search and bounded same-ID reconciliation forms;
- Protocol 6.3 tests contain the executable counterfactuals and the prior positive-guidance fixture was brought into the strengthened contract;
- generated distribution/profile artifacts were regenerated from canonical source and validated.

## Remaining lifecycle gate

A fresh independent assembled-candidate Review of exact candidate `42eb89388dc96879157ba92db9e7f3c59f2c0b36` is still required. The reviewer must independently reconstruct accepted Protocol 6.2, the active Protocol 6.3 workplan, the seven repaired obligations, evidence applicability, bootstrap lifecycle, package/profile/frozen integrity, and all four inherited Challenge dimensions rather than inheriting this implementation-context PASS.

Until that independent Review passes and Stage G separately establishes recovery:

```text
independent Review: PENDING
Protocol 6.3 recovery: UNAVAILABLE
Stage G: BLOCKED
accepted current: Protocol 6.2
workplan: ACTIVE
main cutover: NOT AUTHORIZED
```
