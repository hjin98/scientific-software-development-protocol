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
