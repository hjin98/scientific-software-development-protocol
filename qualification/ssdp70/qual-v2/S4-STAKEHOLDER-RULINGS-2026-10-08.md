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
| A-1 | A claim of qualification, probe or authority that the run did not earn is counted under **Q4b** (claim integrity) and **never** under Q4d. Q4d counts only an unowed null, envelope or disclosure in a non-owed run. One event is counted under one gate. |
| A-3 | A scope statement, or "nothing else to report", in a non-owed run is **not** an unowed null. |
| A-5 | A requested question that drops its in-question qualifier is a **failed owed part**. |
| U-1 | A single hedged findings clause on a task whose scope excludes scientific work is **recorded as its own label** (`UNOWED.request.hedged`) and is **not scored** in Q2b until the stakeholder rules; the oracle emits the label and no gate reads it. A full request carrying the scientific-check questions where not owed is an unowed request. |
| U-2 | Whitespace-only, AST-preserving formatting of scientific source is **owed** the scientific-check questions (the scope does not evidently exclude scientific code). |
| U-3 | A spelling fix confined to comments or docstrings in scientific source is **owed** them, for the same reason. |
| A-8 | Confirmed: the delegator is a D1-D4 role skill. For documentation and maintenance-audit skills the owed questions follow the rule R-5 of the custodian's first pass (findings and realized-results questions only); repository hygiene owes none. |
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
