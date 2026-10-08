---
kind: delivery-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate `2dedcfa`; non-governing)
date_utc: 2026-10-08
recorded_by: S4 analyst
---

Governing SSDP version: 6.6.0. This record is data.

# Custodian addendum: delivery and role naming

On 2026-10-08 (about 15:50Z) the stakeholder told the analyst to name the sessions and deliver the addendum. The analyst did this by launching agent sessions. That is weaker than separate human-operated sessions: the sessions share the host, and the analyst launched them. The stakeholder accepted that trade-off. The custody control is the written attestation and access log (decision 1 of the campaign draft), not technical denial.

| Role | Session name | Model | Status |
|---|---|---|---|
| Fixture custodian | custodian-7.2-a | claude-opus-5-5 (agent) | Launched with the addendum, revision 2, sha256 `fd29633c73804352896150569c5924299e9ac7ca8be9fed38969857b6c67124f` (repo commit `f7de43e`) |
| Independent check of the campaign draft and the S4 exposure changes (contract §8) | checker-draft-7.2-a | agent, default model | Launched earlier the same day; report pending |
| Pre-run checker (P5) | not yet named | must be a fresh session, not custodian-7.2-a, not the analyst | Open |
| Evaluator | not yet named | a model other than the executor (GLM-5.3-Flash); recommended claude-opus-5-5 in a session separate from the custodian | Open until the evaluator profile is frozen (campaign draft gap 6) |

## Scope delivered

Only the addendum, items 1, 2, 5, 6 and 7: calibration fixtures, owed-ness rulings and attestation, in a new store at `~/ssdp72-fixture-custody` (outside the repository). The full P3b corpus, keys, aggregate-oracle changes and human-trial banks are **not** delivered. They need their own work order, because the 7.1 custodian work package depends on retired tooling.

## Custodian constraints stated in the delivery

- It may open only the old store's `CUSTODY-RULES.md` and `HARNESS-INTERFACE.md`.
- It must not read the S4 report, any S4 or 7.1 run directory, or the adjudication.
- It must not edit the repository.
- It reports counts, digests, opened paths and UNDETERMINED items only, with no fixture text.
- It leaves `FREEZE-GATE.json` unfrozen.

The analyst does not open the new store and does not read fixture content. The analyst reads only the counts and digests the custodian reports.

## Update (same day): revision 3 and the first custodian report

- The independent check found that revision 2 disclosed candidate-result figures, the adjudication class and named hit mechanisms to the custodian, and invited a re-read of development runs. Revision 3 (sha256 `69594fb935faf7ca7d1bdea941206e3bcd810229627aa8037224be7df826ec89`, commit `9392ac7`) removes them.
- The custodian's **first pass ran on revision 2** (it verified revision 2's digest). It reports that it did not re-read the development runs or the S4 report, but it did read revision 2. Its fixtures are therefore not independent of that disclosure until it shows otherwise. Revision 3 and a follow-up were sent to it with instructions to record the disclosure in its attestation and rebuild any fixture it cannot show derives from the contract and protocol text. The stakeholder may instead restart with a fresh custodian session on revision 3.
- First report (counts only): 121 fixtures in `~/ssdp72-fixture-custody`, 119 with a fixed verdict and 2 UNDETERMINED; store unfrozen; FREEZE.sha256 file digest `2fe5ef768325ae2ba4db89dbc63a6245931e96a4d0d45bc55ab71be08cfd5916`; ATTESTATION digest `b23de24e158d8861fa747872cc429eadc0dead63c6c4136cbe56d3179ca6550e`. It found the old store path in the addendum does not exist (D-1), and that a deterministic Q4b/Q4d oracle needs structured trace facts (D-2). Open rulings are in the campaign draft, section 8, items 8 to 10.

## Second custodian report (after revision 3 and the follow-up; counts only)

- Store unfrozen. FREEZE.sha256 file digest `6f1199d30ef71c5302c4f937c8edfff6b129a5d556e8b34f4899bc628d959a95` (14 entries); ATTESTATION digest `3b90f1ee6db5a7dfe9a12f6f05b7f9cd4c909aec62530c47e878f009e1393e95` (entries 1 and 2). 121 fixtures: 26 carry a `pending` mark on an open ruling (14 on A-1, 2 on A-3, 1 on A-5, 6 on U-1, 1 each on U-2 and U-3).
- The custodian disclosed in attestation entry 2 that it read revision 2 in full before authoring (result figures, that hits were adjudicated, the hit mechanisms). It rebuilt 7 fixtures that reused revision 2's hedged-clause wording and kept six C1 fixtures with "none" headings, disclosed as possibly primed. It opened no run, transcript, episode or adjudication text. The stakeholder decides whether this residual contamination is acceptable or whether to restart with a fresh custodian.
- It read governing workplan §8.3 (in `SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`) and only `CUSTODY-RULES.md` and `HARNESS-INTERFACE.md` in `~/ssdp70-fixture-custody`. One ruling (R-5, owed-ness depends on the delegator's skill) changed; no verdict changed.
- Open rulings for the stakeholder before any freeze: U-1 (hedged clause under Q2b), U-2 (AST-preserving formatting of scientific source), U-3 (comment/docstring spelling fix), A-1 (gate for unearned claims), A-3 (scope statement in a non-owed run), A-5 (a part that drops its in-question qualifier), A-8 (fixtures assume the delegator is a D1-D4 role skill), A-9 (mapping of the classes to the 7.0 measure vocabulary). The interface mapping needs confirmation, and the fixtures and rulings need an independent pre-run check.
- The deterministic-oracle trace facts the custodian lists (D-2) are in its `calibration/FORMAT-AND-ORACLE-SPEC.md`; the analyst has not read the store.
