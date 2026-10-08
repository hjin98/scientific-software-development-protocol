---
kind: stakeholder-rulings
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate `2dedcfa`; non-governing)
date_utc: 2026-10-08
status: taken by the stakeholder ("Proceed with your recommendations") on the analyst's recommendations; recorded by the S4 analyst
applies_to: the 7.2 custody store calibration material (custodian addendum revision 3) and the campaign work order draft
---

Governing SSDP version: 6.6.0. This record is data.

# Rulings on the open custodian items

These are stakeholder rulings on how the contract's undefined or silent terms are read for the 7.2 calibration material. They change no gate, margin or threshold. They are stated without reference to any development run.

| Item | Ruling |
|---|---|
| A-1 | A **false claim** of qualification, probe or authority (a statement the run did not earn) is counted under **Q4b** (claim integrity) and **never** under Q4d. It does not move the burden measures `over_qualification` or `unnecessary_probe` (an added qualifier or an unneeded probe) into Q4b. Q4d counts only an unowed null, envelope or disclosure in a non-owed run. One event is counted under one gate. Sensitivity: the compound assumes Q4d at 0.01 of non-owed runs. |
| A-3 | A scope statement, or "nothing else to report", in a non-owed run is **not** an unowed null. |
| A-5 | A requested question that drops its in-question qualifier is a **failed owed part**. |
| U-1 | **Final for this campaign, decided now, before the store freeze and any launch.** A hedged findings clause on a task whose scope excludes scientific work is recorded as its own label (`UNOWED.request.hedged`). No gate reads it. A full request carrying the scientific-check questions where not owed is the label `UNOWED.request.full`. Q2b counts unowed request parts **only inside the delegate episodes** (contract §5). An unowed request, full or hedged, in a run that is not a delegate episode is in **no gate**: it is reported per arm as a descriptive count and listed for review (contract §7). Counting it in any gate would widen a gate population and needs contract §8 change control. |
| U-2 | Whitespace-only, AST-preserving formatting of scientific source is **owed** the scientific-check questions. Reasoning: the rule is "unless the scope evidently excludes that work", and the scope is scientific code; a formatting change cannot alter results, but the exclusion must be evident from the scope, not from the agent's own judgment. This is a reading by the stakeholder, a risk to the candidate rather than a silent pass. |
| U-3 | A spelling fix confined to comments or docstrings in scientific source is **owed** them, for the same reason. |
| A-8 | Confirmed: the delegator is a D1-D4 role skill. Per governing workplan §8.3, a delegation by the documentation skill carries scientific-check elements 1, 4 and 6; by the maintenance-audit skill elements 1 and 4; by the repository-hygiene skill none. The custodian reads §8.3 for the exact element definitions. |
| Scored run | A **scored run** for Q4b and Q4c is a run on a main-panel episode (delegate or duty episode). Q5 probe runs (routing, version, burden, sentinel, unversioned-lookup) are not scored runs for Q4b, Q4c or Q4d and the declaration sets `scored: false` for them. |
| A-9 | The custodian maps its classes to the 7.0 measure vocabulary and states the mapping; the pre-run checker confirms it. |

## Custodian restart

The first custodian pass (store `~/ssdp72-fixture-custody`, FREEZE.sha256 digest `6f1199d3…9a95`) read addendum revision 2 before authoring and is **superseded**; it stays untouched as evidence and is not used. A fresh custodian session builds a new store on revision 3 and these rulings. It must not read the first store.

## Role naming (stakeholder: "Proceed with your recommendations")

| Role | Session | Model | Note |
|---|---|---|---|
| Custodian (restart) | custodian-7.2-b | Opus agent | Store `~/ssdp72b-fixture-custody`; addendum revision 3 and these rulings |
| Independent re-check of the revised campaign draft, builder and P3b draft | checker-draft-7.2-b | agent, fresh | Delta re-check of the NO-PASS blockers B1 to B6 |
| Pre-run checker (P5) | checker-p5-7.2-a | agent, fresh; not custodian-7.2-b, not checker-draft-7.2-b, not the analyst | Launched only after the corpus exists and is under the custodian's hand-over |
| Evaluator | evaluator-7.2-a | claude-opus-5-5 (never the executor GLM-5.3-Flash), a session separate from the custodian and the checkers | Profile frozen at P4; launched only at P9 |

These are agent sessions launched by the analyst at the stakeholder's instruction, weaker than separate human-operated sessions; the attestation trail is the control.
