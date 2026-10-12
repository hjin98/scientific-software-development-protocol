---
kind: independent-pre-run-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: PASS
---

# Independent pre-run recheck of the single-participant human legibility trial (contract §7): PASS

**Independence and custody.** The same independent checker ran this recheck as the prior check. It authored none of the Protocol 7 candidate, the contract, the stakeholder decision or any fixture. It read nothing under `/home/samjin/ssdp70-fixture-custody/` and no concrete fixture, key, expected answer or human-trial material. The only file it wrote is this record, and the result binds only the exact subjects below.

| Subject | SHA-256 verified |
| --- | --- |
| Revised contract (uncommitted working tree) | `0ad41af6ec5aee36f50666e92238f4fb74298d331642164426316c34449ca35d` |
| Contract at HEAD (Stage A PASS revision) | `02dd12dbf2468c5134119146bd04b8ae9d46551a505e498aa0e2b885030ce077` |
| Stakeholder decision 2026-09-28, single participant | `c6f88cefbe970e1b90fb5830980d5db519cbf745f808821e34d9ea701151a04a` |
| Governing workplan | `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` |
| Prior check (NO-PASS on `c40598ab…`) | `11ef561c372e3f02627c728e5c82261ef01efac21f3a69d2398c9e270143ba33` |

**Scope of change.** `git diff HEAD` has two hunks. The first rewrites §7. The second is §8, and its text matches the `c40598ab…` text checked earlier byte for byte. So the only change since `c40598ab…` is in §7. No other contract text differs from `02dd12db…`.

## Serious Challenge

None. The admissibility finding from the prior check still holds. A single stakeholder participant with one fixture per arm is within workplan §11.6. No counterbalancing is required with one participant. This is a governed contract change made before any exposure; it needs no workplan change. §13 items 5, 8, 10 and 14 still require a passed trial.

## Prior material gap: CLOSED

The earlier gap was that a failure could be reclassified as missing evidence. The revised §7 closes it:

- Exposure is counted by questions presented, and underexposure refers to presented questions.
- An observed floor failure stands whether or not the trial is completed.
- Non-completion is non-discriminating only for a recorded reason unrelated to the material. Otherwise every presented question left unanswered is scored wrong.
- A repeat is allowed only after a non-discriminating result, on unseen fixtures and under a fresh custodian draw, with the earlier observations kept.

This satisfies the workplan §11.5 rule that distinguishes missing evidence from demonstrated failure and forbids recategorizing an observed failure.

## Prior minors: all addressed

- The trial record carries a custody-access attestation.
- Permitted assistance is in the freeze list.
- The contract states that unblinding is near-certain because the participant is also the ratifier.
- The stated limit covers the stakeholder only, one drawn fixture per arm, one drawn order, and the fixture/arm confound, including in the time ratio.
- The time bound now sits under "Across arms".

## Retained protections (verified)

These are unchanged from the prior check:

- at least 20 routine and at least 4 critical questions presented per arm;
- zero materially wrong critical answers per arm;
- at least 16/20 correct routine answers per arm;
- candidate-arm median time at most 2.0 × the 6.6 arm's median;
- no fixture is seen in both arms;
- the custodian freeze, and the author/executor exclusion from custody material;
- blinded independent scoring;
- no machine proxy, and release blocked if the trial cannot run.

## Minor findings (non-blocking)

- **Who judges non-completion.** The contract does not say who decides whether a non-completion reason is "unrelated to the material". The participant is also the ratifier and has a stake in the outcome. The reason should be recorded when it occurs and assessed by the custodian or evaluator, not by the participant alone.
- **Repeat feasibility.** The workplan provides 2–3 composite fixtures, so a repeat will likely need newly authored custodian fixtures. That is permitted by this pre-declared rule and is not a contract gap.

## Pending pre-run checks (not passed)

- The custodian's human-trial material must be re-planned for one participant. This check needs the withheld material and covers the random-draw record, matched templates, frozen questions and answers, the time protocol and permitted assistance.
- All withheld-instance and actual-harness checks listed in `STAGE-A-INDEPENDENT-CONTRACT-RECHECK-PASS.md` remain open.

## Disposition

**PASS** for contract §7 at SHA-256 `0ad41af6…`, as a framework only. It passes none of the pending checks above, each of which must pass before any candidate run. Any later edit to the contract requires a new applicability check.
