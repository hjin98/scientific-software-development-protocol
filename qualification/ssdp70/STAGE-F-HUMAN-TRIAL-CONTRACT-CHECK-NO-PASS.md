---
kind: independent-pre-run-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: NO-PASS
---

# Independent pre-run check: single-participant human legibility trial (contract §7) — NO-PASS

**Independence and custody.** This checker authored neither the Protocol 7 candidate, the contract, the stakeholder decision nor any fixture. It read nothing under `/home/samjin/ssdp70-fixture-custody/`, and no concrete fixture, key, expected answer or human-trial material. The only file it wrote is this record. The check binds only the exact subjects below.

| Subject | SHA-256 verified |
| --- | --- |
| Revised contract (uncommitted working tree) | `c40598ab2ff2f2a213fee5e7ab94c3e64f11efe953d1c5bb615936944ebf7f36` |
| Contract at HEAD (the previously PASSed revision) | `02dd12dbf2468c5134119146bd04b8ae9d46551a505e498aa0e2b885030ce077` |
| Stakeholder decision 2026-09-28, single participant | `c6f88cefbe970e1b90fb5830980d5db519cbf745f808821e34d9ea701151a04a` |
| Governing workplan | `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` |

**Scope of change.** `git diff HEAD` shows changes only to §7, which is rewritten, and one added sentence in §8. No other contract text changed. The committed `STAGE-A-CLOSURE-2026-09-28.md` still describes the four-participant design, as a historical record bound to `02dd12db…`.

## Serious Challenge

None. Workplan §11.6 names "the stakeholder, or a designated scientist representing the declared reader". It requires "at least one fixture from each arm" and counterbalancing only "where more than one participant exists". The four-participant design was a Stage A contract choice, not a workplan floor. Returning to the workplan minimum before any exposure (Stage F entry stop: no run, no trial) is therefore a governed contract change. It is not the workplan relaxation that §11.6 reserves for a workplan change, and §13 items 5, 8, 10 and 14 still require a passed trial. No workplan change is needed.

## Material gap (blocks)

1. **An observed failure can be reclassified as missing evidence.** §7 scores "Unanswered questions … as wrong". The new underexposure clause makes the trial non-discriminating if either arm "falls below 20 routine or 4 critical **answered** opportunities" or the stakeholder "does not complete both arms". The superseded text counted presented opportunities.
   - As written, one unanswered question in a 20-question arm triggers both a scored failure and a non-discriminating result.
   - Stopping early after a materially wrong critical answer has been recorded also turns that failure into missing evidence.
   - Workplan §11.5 requires the contract to distinguish missing evidence from demonstrated failure and forbids recategorizing an observed material failure to evade a floor. With one participant, the "non-discriminating" route is also the route to a rerun.
   - **Repair.** Count exposure by presented frozen opportunities. State that any floor failure already observed (a wrong critical answer, or routine errors already exceeding 4 per arm) stands as a failure whether or not the trial completes. Classify non-completion as non-discriminating only for a recorded reason unrelated to the material, and score its unanswered questions as wrong otherwise.

## Retained protections (verified)

- Per-arm exposure is fixed at ≥20 routine and ≥4 critical questions, and the same single reader serves both arms, so no arm can be under-exposed relative to the other. The prior gap-3 protection holds, subject to the material gap above.
- These rules are unchanged: zero materially wrong critical answers per arm, ≥16/20 routine answers per arm, and candidate median time ≤2.0 × the baseline (6.6) arm's median.
- The stakeholder never sees the same fixture in both arms or the other arm's output. Custodian freeze and author/executor exclusion are unchanged, as are "no machine proxy" and blocked release acceptance.
- The added controls are adequate and honestly bounded: a recorded random pre-draw of fixture-to-arm and arm order, matched question templates, blinded independent scoring against frozen answers, and recorded unblinding. The stakeholder-only limit and the fixture/arm confound are stated.

## Minor findings (non-blocking)

- **Stakeholder access to custody.** The custody directory lives under the stakeholder's home directory, and "does not read them" is only a behavioral rule. Workplan §11 says "record what each … could access", so the trial record should state the stakeholder's access and include an attestation.
- **Stated limit is incomplete.** The limit should also say that the result covers one drawn fixture per arm and one drawn order, with order and learning effects unremovable. The time ratio compares different fixtures. "Intended-reader legibility" should not be read as holding across fixture classes.
- **Permitted assistance not in the freeze list.** Workplan §11.6 requires the custodian to freeze permitted assistance. §7's freeze list still omits it, a carry-over from `02dd12db…`.
- **Participant is also the ratifier.** The stakeholder has deep familiarity with Protocol 7 doctrine, so arm unblinding is near-certain. The ratification package should state this dual role.
- **Wording.** "Floors, per arm" includes the time bound, which is a cross-arm ratio.

## Pending pre-run checks (not passed)

These need withheld material. Re-plan the custodian's human-trial material for one participant, then check: the random-draw record, matched templates, frozen questions and answers, the per-question time protocol and permitted assistance. All earlier pending withheld-instance and actual-harness checks from `STAGE-A-INDEPENDENT-CONTRACT-RECHECK-PASS.md` also remain open.

## Disposition

**NO-PASS** for contract `c40598ab…`, on material gap 1 only. The single-participant design is admissible under workplan §11.6, with no Serious Challenge. After a wording repair of material gap 1, a fresh applicability check of the exact new bytes is required before any candidate run.
