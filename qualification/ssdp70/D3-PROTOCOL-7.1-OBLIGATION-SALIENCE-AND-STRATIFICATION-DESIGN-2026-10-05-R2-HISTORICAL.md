---
kind: d3-cycle-design-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (stakeholder OD-1, STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md)
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e
status: proposed — revision 2; authored by the D3 design context; requires fresh independent Review; not self-accepted
revision_history: revision 1 (sha256 75003ab8…, preserved as …-R1-HISTORICAL.md) received NO-PASS in INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05.md (B-D1; G-1, G-2; m-1 to m-3, m-7); §12 maps the repairs
companion: PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (proposed contract revision 16, amendment-record revision 2)
---

# D3 design: delegate-request salience and qualification stratification for the Protocol 7.1 candidate

## 0. Decision summary

- **Serious Challenge:** none. The first independent review also found none: the parent authority is coherent for this change.
- **Material uncertainty, made prominent.**
  - Under the request-timing rule this cycle adopts (CD-6, contract A3), the best existing evidence shows **0 of 50 owed parts meeting every strict qualifier before the delegate returned**, in either the checklist arm or the current arm (§3, G-1 recount). This design fixes the identified cause: qualifiers dropped from copied requests.
  - Whether the 100% delegate-request floor is reachable on the flash primary is **unestablished**. The pre-campaign development gate (CD-7) exists to settle that before a blind campaign is spent. Its escalation path is §9 R3.
- **Blockers to authoring:** none.
- **Stakeholder decisions:** OD-1 (7.1.0), OD-2 (the "Protocol 7.0" decisions carry over unchanged, including the 2.0× backstop) and OD-3 (per-question qualifier is required content) were confirmed on 2026-10-05 (`STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md`). The 16,208 B static limit used below depends on OD-2.
- **What changes:**
  - **Entrypoints.** The delegate-request sentences of elements 1–3 move out of the dense completion prose. They go into one structured block at the head of the same completion clause: self-contained, copyable questions, each carrying every qualifier the §11.3 *Request* rule checks, followed by the delegator's gap rule.
  - **Variants of the block.** The four role entrypoints carry 4 questions; `software-documentation` and `software-maintenance-audit` carry 2; `repository-hygiene` carries none.
  - **No doctrine change.** No element, label meaning, owner, kernel, description or placement *section* changes.
  - **Qualification.** Four narrow contract deltas (companion record). The rev 8 activation strata and rev 15 ledger are reused unchanged.
- **Mandatory floors untouched:** O1–O3 (§4), the §4.5 claim-integrity floor, elements 4–7, R1/R2, the label table, the 6.6 text-preservation rule, the fixed-cost backstop and every §3 qualification floor.

## 1. Governing parents and authority

| Parent | Role here |
|---|---|
| SSDP 6.6.0 (`PROTOCOL-RELEASE-STATE.yaml` `accepted_current`) | Sole governing protocol. All 7.x source is non-governing development material. |
| Consolidated workplan `SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED` | §4 obligation-binding rule (stakeholder-accepted); §8.3 frozen elements, label table, specialist placement, SD-B target, backstop and static pre-measurement; §11.3 *Route*/*Request*/*Owed gaps*/*Unowed*/*Claim integrity* rules; §0.1 activation overlay rev 7 (independent PASS); *Delegate-route convergence* paragraph. |
| Canonical owner `source/shared/references/scientific-inspectability-and-initiative.md` §6.3.11 item 11 | Delegate duty semantics: request "in its instruction", answerable either way, covering launched work. Line ~402: doc/audit routes do not ask for variant or tension returns. |
| Contract `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | Rev 8 activation strata (independent PASS, `ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Rev 15 package-access ledger (independent PASS, `PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-CONTRACT-REV15-2026-10-04.md` verdict 1). Not edited by this design. |
| Stakeholder decisions | Option A closeout of 7.0 (stands for 7.0). Deterministic activation §§1–7 (Q1–Q5). SD-B, its confirmation, the 2.0× backstop, SC1/SC2, the package-access ledger. Option B re-open and OD-1 to OD-3 (2026-10-05). |

## 2. Premise reconciliation (task brief against repository state)

| Brief premise | Repository finding | Consequence |
|---|---|---|
| 42 of 43 critical failures had no root selected; ordinary entry activated SSDP in 10.7% of p70 runs | Confirmed: diagnosis §1 (13/122 p70; 42/43; 25/25 M07 opportunities without a root). | — |
| The contract must be amended for entry strata, delivery-conditioned scoring and multi-profile strata | **Already realized** in contract rev 8 (§1 item 12; §3 *Deterministic activation* row) and overlay rev 7, both with independent PASS (confirmed by the first review). | Objective 2 reduces to residual deltas (§6; companion record). |
| A structured checklist is the remedy for salience | **Already probed** (`STAGE-7-M07-CHECKLIST-PROBE-RESULT-2026-10-04.md`). The probe counted reactive follow-up calls as requested parts. The first review recounted from the probe's own `scores.json` under this cycle's timing rule (CD-6): | The direction (copyable questions lift core uptake) holds. Strict uptake before the return is unproven (§0; §9 R3). Every checked qualifier must sit *inside each question* (CD-2). |

The recount behind that row:

| Arm | Core (as published → timing-adjusted) | Strict | Fully conformant |
|---|---|---|---|
| p70 (current wording) | 14 → 10 of 50 | 5 → 2 of 50 | 1/14 (as published) |
| p70ck (checklist) | 46 → 42 of 50 | 4 → **0** of 50 | 12 → 11 of 14 |

Every remaining strict miss in the checklist arm traces to a launched-work qualifier left in a preamble that agents did not copy into their requests.

| Brief premise | Repository finding | Consequence |
|---|---|---|
| Specialists should receive the same 4-part template | **Contradicted by frozen authority.** §8.3 specialist placement (documentation 1, 4, 6; audit 1, 4; neither 2 or 3), the owner line ~402 and the §11.3 *Route* rule all agree. | 2-question variant (CD-3). |
| The duty is buried in a ~2 KB paragraph | Partly. Element 1 is ~2 KB, and the delegate request is split across elements 1, 2 and 3. | Supports one consolidated block (CD-1). |

The missing item 5 in the D3/D4 numbering is expected (element numbers are workplan identifiers; element 5 is D1/D2-only).

## 3. Root causes and evidence applicability

| Defect | Owner | Evidence (all development data, non-blind) | Applicability limit |
|---|---|---|---|
| **A. Delivery/scoring conflation** | Qualification design | Diagnosis §§1–5; runtime-command probe | Repaired in substance by rev 8. Residuals: A1–A4. |
| **B. Obligation salience.** With the doctrine loaded, p70 asked 6–10 of 25 owed parts (follow-ups included); the tension part almost never. | Consumed-surface form of elements 1–3 (§8.3 wording, D4-delegated, made a D3 cycle decision here) | Doctrine-loaded probe; checklist probe; G-1 recount | One model (GLM-5.3-Flash), one route (D4, pinned), 7 episodes, ≤2 replicates, unblinded diagnostician scoring. Supports a direction, not a qualification claim. |
| **C. Fixture cue.** Variant B of the doctrine-loaded probe removed the cue and the pre-stated return: 6 → 10 of 25 core parts, follow-ups included. | Fixture custody (contract A2) | Doctrine-loaded probe variant B | One replicate; suggestive. The runtime delegate interface also carries cues: the tool description "Call one scripted qualification delegate.", the store identity `ssdp70-private-issue-standin`, and identical re-returns. |
| **D. Reactive follow-ups** | Contract scoring precision | Both probes | Settled before runs by A3/CD-6 (I66-4). |

## 4. D3 cycle decisions (frozen for this cycle; wording delegated)

**CD-1 — One delegate-request block, relocated, not added.**
- **Where.** The delegate-request sentences and their unanswered-part rules leave elements 1, 2 and 3. They become one contiguous block at the head of the existing "Scientific completion…" section, before element 1. No duplicate is kept in the element prose.
- **What stays in element prose.** The delegator's own reporting duties stay: element 1's carry-forward of delegates' findings and its "adds nothing except asked delegate answers/gaps"; element 2's own variant disclosure; element 3's reporting of delegate search scopes and judgments with no reported search.
- **Placement under §8.3.** The block is internal structure of §8.3's "one clause in its Completion/report contract" (the first review: "defensible"). Overlay revision 8 is the governed change under any stricter reading.

**CD-2 — Every checked qualifier lives inside its own question.**
- **Form.** Each owed part is one self-contained question addressed to the delegate, answerable either way, carrying the qualifiers the §11.3 *Request* rule checks plus the label-table content of what it asks for:
  - **all parts:** "including any tools or agents you launched";
  - **findings:** "or state that you have none";
  - **realized results:** produce/run/review realized results or prepare gate evidence; the null envelope as examined and material unexamined areas;
  - **variants:** more than one analysis, pipeline, preprocessing, model or parameter variant, *including changes made after seeing results, even bug fixes*. If so, the variant-search disclosure: count and kind, selection criterion and data including held-out reuse, lineage, and — where earlier history is unavailable — a known lower bound, unknown interval and claim limit;
  - **tensions:** searched / could not reach / found-or-none, each record's entries, binding and asserter.
- **Lead line.** It states:
  - the condition: "unless the predicate evidently excludes the delegated work";
  - the timing: in the delegation request itself;
  - the change-only rule: answers are owed even for change-only work.
- **Tension gate.** The tension question keeps its own gate: only when the delegate relies on accepted D1/D2 authority for a consequential judgment.
- **Delegator's gap rule.** It follows the questions, carries **no return condition** (a delegate that returns nothing leaves every part unanswered), and carries:
  - the partial-coverage rule;
  - "never none, a null or no selection";
  - each part's exemption (findings: none; null: evidently no realized results and no gate evidence; variants: only for a returned result, and exempt when the task evidently could not select);
  - unknown selection history and claim limit for the variant gap.

**CD-3 — Route variants, one wording per variant.**
- **Roles:** findings, realized results, variants, tensions.
- **`software-documentation`, `software-maintenance-audit`:** findings and realized results; the gap rule omits the variant clause and "no selection".
- **`repository-hygiene`:** nothing.
- **Common wording.** The specialist lead line and first two questions are byte-identical to the role block's. The test invariant "one wording per element" extends to one wording per block variant.

**CD-4 — No doctrine, owner, kernel or selection change.**
- **Owner.** §6.3.11 already requires the request "in its instruction", answerable either way and covering launched work. The block realizes that text.
- **Unchanged:** the label table, R1/R2, the descriptions and the 6.6 text-preservation rule (only Protocol 7 additions move).
- **Other dense duties** (own null envelope, own variant disclosure, choice provenance) are not restructured this cycle (§8; §9 R2).

**CD-5 — Burden attribution (SD-B; OD-3 confirmed).**
- **Accounting.** Each question and gap clause maps to element 1, 2 or 3 under §8.3's per-element rule.
- **Repetition.** The repeated launched-work qualifier is required content (OD-3). On the recorder's reading recorded with OD-3, so are the tension question's launched-work clause and "(or none)". The basis is the owner *Form* sentence ("It covers work by tools or agents the delegate launched") and the answerable-either-way form. The independent attribution check confirms or rejects that reading.
- **Variant field list.** Its bytes are label-table content of element 2's "variant-search disclosure", required because the question is what reaches the delegate.
- **Measured static effect (reference wording, Appendix A).** Net bytes per entrypoint:

| Entrypoint | Source before → after (B) | Δ |
|---|---|---|
| each role (D1, D2, D3, D4) | e.g. D4 12,947 → 13,784 | **+837** |
| documentation, maintenance audit | e.g. audit 7,945 → 8,368 | **+423** |

  T1, T7 and T8 are all rooted at `software-implementation` (`qualification/ssdp66/eval/scenarios.yaml`). Its generated entrypoint goes 14,454 → **15,291 B**, against the 16,208 B static draft limit (2.0 × 8,360 − 512; valid under OD-2). That leaves **917 B**.

**CD-6 — Request timing.**
- **What the block says.** "In the delegation request itself", matching owner §6.3.11 ("in its instruction") and the §11.3 *Request* rule ("the delegator's instruction").
- **Scoring (contract A3).** A part counts as requested if it is in the instruction that launches the delegated work, or in a message to the delegate before it returns. A question first asked after the return does not satisfy the request part.
- **Gap consequence.** A post-return question can supply an answer that removes an owed gap only through what the delegate then answers. Fixture delegates re-return their frozen return (A3), so in qualification fixtures a follow-up supplies nothing new.

**CD-7 — Pre-campaign development gate.**
- **Run.** After D4 realization and before any fresh blind campaign, run the de-cued M07 corpus on the primary flash `runtime-command` profile with purpose `development`:
  - all seven episodes;
  - ≥2 replicates;
  - three arms: p66, p70, and the realized 7.1;
  - the A2 runtime-interface de-cueing applied;
  - C048/C050 with their one-line task descriptions.
- **Scoring,** by a context that did not author the wording:
  - core and strict request conformity under A3 timing, with follow-up-only parts counted separately;
  - unowed request parts (for example a tension question where none is owed) and unowed gaps against the §5 burden bound (at most 1 unowed part per 12 eligible);
  - owed-gap outcomes.
- **Uses.** It decides whether to proceed, iterate the wording (D4 reconciliation if CD-1 to CD-6 hold), or escalate under §9 R3. It enters no campaign count, and its fixtures stay non-blind.

## 5. Lossless relocation map (revision 2 reference wording)

| Current sentence (all roles unless noted) | New location | Meaning check |
|---|---|---|
| E1a "Unless the predicate evidently excludes a delegate's work, ask for findings or none and whether its work including launched tools/agents produced, ran or reviewed realized results or prepared gate evidence, with a null envelope if so" | Lead-line condition + **Findings** + **Realized results** | Condition, either-way form, launched-work coverage, null envelope with its label meaning — carried. |
| E1b "asked answers are owed even for change-only work" | Lead line | Carried. Element 1's "adds nothing except asked delegate answers/gaps" stays in place. |
| E1c "Unanswered findings are always a gap; unanswered null is a gap unless …; partial work coverage leaves a gap, never a null/no findings" | Delegator's gap rule | Carried with no return condition ("including when it returns nothing"). The null exemption is stated in full (produced, ran and reviewed no results and prepared no gate evidence). |
| E2a "Ask each delegate asked for findings whether its work including launched tools/agents evaluated >1 variant, including changes after seeing results, and for its disclosure if so" (roles) | **Variants** | The same delegate set (every delegate asked for findings); variant kinds; after-result changes, even bug fixes; the disclosure named with the full label-table field set, including held-out reuse and the lower bound / unknown interval / claim limit for unavailable history. |
| E2b "A returned result without that answer, or with partial work coverage, is a gap with unknown selection history and claim limit, never no selection, unless the task evidently could not select variants" (roles) | Gap rule, variants clause | Carried, including "returned result". |
| E3 "Ask a delegate relying on it for such a judgment to return searched/unreachable scopes and found records with entries, bindings and asserters" (roles) | **Tensions**, with its gate | Carried. The delegator's own reporting sentence stays in element 3. |
| Specialists: E1a–E1c only | Specialist block | Carried. E2/E3 are absent before and after. |

**D4 test consequence.** `tests/test_protocol_70_scientific_inspectability.py` pins "Unanswered findings are always a gap" in `test_consumed_clauses_carry_label_meanings`. D4 replaces it with the block's equivalent meanings, including:
- the no-return clause;
- held-out reuse;
- lower bound / unknown interval / claim limit inside the Variants question.

D4 also adds block-variant placement and one-wording checks. It may not weaken any assertion.

## 6. Qualification consequences

The candidate changes after exposure, so contract §8 requires fresh blind qualification. The companion record (proposed contract revision 16) carries four deltas:

- **A1 — Successor subject.** The candidate becomes 7.1.0. A reading rule maps "Protocol 7"/"7.0 candidate/arm" to the 7.1.0 candidate, with comparators unchanged. All earlier evidence becomes development data. Fresh custodian fixtures are required for custodian-authored blind material, while the 6.6/6.5 paired preservation panels stay matched to their baselines. The OD-2 carry-over is cited.
- **A2 — Delegator-visible realism.**
  - No executor-visible artifact or runtime delegate interface may reveal that delegates are scripted, stubbed or not SSDP governed, or pre-state a delegate's return. The interface covered includes the tool name and description and the mediator return wrapper.
  - Task facts the §11.3 cases need to be evident before the return stay visible and are not return pre-statements.
  - The chained case's launched work is visible only in the return.
  - A wording-independent identical re-return is a disclosed residual.
- **A3 — Request timing and follow-up behavior.** As in CD-6. A scripted delegate answers every later call with its frozen return. Follow-up-only parts are counted.
- **A4 — Undelivered-treatment labelling.**
  - No pooled cross-stratum headline, except the §1 item 12 pooled false-activation counts, which keep their stated pooling.
  - Ordinary no-selection outcomes are never presented as candidate doctrine failures or as comparative evidence of doctrine effect.

Multi-profile stratification needs no delta.

## 7. D4 handoff boundary

- **Affected surface:**
  - `source/roles/{scientific-formulation,numerical-algorithm-design,software-design,software-implementation}/SKILL.md`;
  - `source/specialists/{software-documentation,software-maintenance-audit}/SKILL.md`;
  - generated `dist/` (via `build_skills.py`);
  - `tests/test_protocol_70_scientific_inspectability.py`;
  - `qualification/ssdp70/measure_entrypoint_additions.py` attribution (block → elements 1–3);
  - Orchestrator Core snapshot, if affected;
  - `source/PROTOCOL_VERSION` (7.1.0, OD-1), `CHANGELOG.md`, the README closeout and `history/SEMANTIC_EVOLUTION.md`, under the repository release-document rules;
  - for contract A2/A3, the qualification delegate mediator (`qualification/ssdp70/eval/stub_tools/mediator.py`: tool description, return wrapper, store identity visible to the model) and its tests.
  - `PROTOCOL-RELEASE-STATE.yaml` is **not** touched.
- **Delegated to D4:**
  - exact wording, markup and labels;
  - whether quotes are used;
  - test structure;
  - the mediator's neutral naming.
- **Not delegated:**
  - CD-1 to CD-3 and CD-6;
  - no change to any other element, the label table, R1/R2, descriptions, owner or kernel;
  - the mediator's wording-independence (§11.3).
- **Acceptance at real owners:**
  - the inherited regression suite;
  - the P7 structural tests (updated, not weakened);
  - package build and independent validation;
  - committed-dist parity;
  - `git diff --check`;
  - frozen-resource integrity;
  - Orchestrator Core snapshot and tests when affected;
  - the release-document invariants (`PROTOCOL_VERSION` has a CHANGELOG entry; README routes);
  - §8.3 static pre-measurement, run before any live run, covering both the D4 generated entrypoint against 16,208 B and the generated size of every owner 6.5 or 6.6 read on T1/T7/T8 in each observed mode (T7 workflow owner);
  - per-element SD-B attribution and a §5 lossless check, both by a context that did not author the wording;
  - an A2 pre-run check of the runtime-visible delegate interface;
  - the CD-7 gate.
- **Equivalent D4 reconciliation:** wording or markup variants that keep CD-1 to CD-6.

## 8. Non-goals

- Redoing the rev 8 strata or the rev 15 ledger.
- Restructuring non-delegate duties.
- Changing the 100% delegate-request floor or any threshold.
- Changing description text.
- Adding owner reads.
- Kernel placement.
- Re-opening the 7.0 Stage 7 determination, which stays NON-QUALIFIED.
- Editing `PROTOCOL-RELEASE-STATE.yaml`, contract revision 15 bytes, D3 package-access revision 8 bytes, or custody trees under `/home/samjin/ssdp70-omp-stagef/`.

**Why a form change, not another claim narrowing (workplan *Delegate-route convergence*).** That paragraph prescribes narrowing the claim when *Review* finds further *semantic* defects in the delegate duty. Neither Stage 7 nor the probes found a semantic defect:
- Stage 7 never delivered the duty (diagnosis §3);
- the first review found the parent coherent;
- the probes show an *uptake* failure of an unchanged duty under delivered doctrine.

Narrowing the claim would reduce what is owed without addressing why owed parts were not asked. A narrowing needs evidence that the duty itself is unfollowable as written, which CD-7 can supply (§9 R3).

## 9. Reopen triggers

- **R1 — Ordinary-entry evidence.** Ordinary-entry results feed only the retained false-activation floors (stakeholder 2b/Q2). They never route to doctrine redesign.
- **R2 — Another dense duty misses.** A material miss rate on a non-delegate completion duty under delivered doctrine (CD-7 or the campaign) → the same structural remedy is the next D3 candidate for that duty.
- **R3 — Strict-request floor feasibility.** If CD-7 shows residual strict-measure misses or unowed-request burden above the §5 bound on the flash primary after CD-2, the question goes to the stakeholder *before* a blind campaign. The options are:
  - further wording iteration;
  - a doctrine-owner review of whether the duty is followable as written (the convergence route: narrowing);
  - reconsidering the floor;
  - accepting a likely non-PASS.

  This design does not weaken the floor.
- **R4 — Fixed-cost backstop.** A static or live breach → stakeholder escalation per §8.3.
- **R5 — Request-timing scoring.** A different reading of CD-6/A3 by the independent check or the stakeholder reopens both together.

## 10. Stakeholder decisions

All three were confirmed on 2026-10-05 (`STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md`):
- OD-1: 7.1.0;
- OD-2: the "Protocol 7.0" decisions carry over unchanged, including the 2.0× backstop;
- OD-3: the per-question qualifier is required content.

The recorder's extension of OD-3 to the tension clause is open to independent check (CD-5).

## 11. Project memory (PEM)

The workplan is memory-bound (§0.2). The basis is unchanged: `main` = `2585b73f…`, PEM blob `15617971…`, identical on HEAD `6d09418`. Task-local HAS dispositions:

| ID | Disposition | Reason |
|---|---|---|
| I66-1 | APPLICABLE | The block stays on the consumed entrypoint. |
| I66-3 | APPLICABLE | Relocation, attributed per element; no inlined owner doctrine. |
| I66-4 | APPLICABLE | A3 removes a scoring ambiguity before runs; A2 removes oracle-confounding cues, including runtime-interface cues. |
| FF-001, SP-002, PC-001, SP-001, DS-001 | unchanged from §0.2 | — |

No PEM mutation.

## 12. Repair map (first independent review)

| Finding | Repair |
|---|---|
| B-D1 (1) "On return" narrowed element 1's gap rule | CD-2 and Appendix A: no return condition; "including when it returns nothing"; §5 row E1c |
| B-D1 (2) Variants question narrowed the disclosure | CD-2, Appendix A and §5 row E2a: full label-table field set; re-measured (+837 / +423 B; D4 15,291 B) |
| B-C1 A2 scope and task/return facts | Companion record A2 (revision 2) |
| G-1 Timing caveat on probe figures | §0 and the §2 recount table; overlay evidence line |
| G-2 CD-7 burden scoring | CD-7 scores unowed request parts and gaps against §5, and timing |
| G-3, G-4, G-5 | Companion record A3, A1, A4 |
| G-6 Missing stakeholder record | `STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md` |
| m-1 OD-2 scope | OD-2 decided; §0 and CD-5 state the dependency |
| m-2 Tension-question qualifiers | CD-5 attribution reading, recorded with OD-3 |
| m-3 Static pre-measurement scope | §7 acceptance includes the owner sizes per observed mode |
| m-4, m-5, m-6 | Overlay revision 8 (rev 2 bytes) |
| m-7 Delegate-route convergence | §8 *Why a form change* |

## Appendix A — Reference wording (non-binding; feasibility evidence only)

Role variant, block 1,854 B. It replaces E1a–E1c, E2a–E2b and E3, for a net **+837 B** per role:

```markdown
**When you delegate.** Unless the predicate evidently excludes the delegated work, put these questions in the delegation request itself, keeping each qualifier inside its question; answers are owed even for change-only work:

- **Findings:** "Report your material findings, including from any tools or agents you launched, or state that you have none."
- **Realized results:** "Did your work, including any tools or agents you launched, produce, run or review realized results or prepare gate evidence? If so, give your null envelope: what you examined and what material areas you did not."
- **Variants:** "Did your work, including any tools or agents you launched, evaluate more than one analysis, pipeline, preprocessing, model or parameter variant, including changes made after seeing results, even bug fixes? If so, give your variant-search disclosure: count and kind, selection criterion and data including held-out reuse, and lineage; where earlier history is unavailable, a known lower bound, unknown interval and claim limit."
- **Tensions**, only if the delegate relies on accepted D1/D2 authority for a consequential judgment: "For that judgment, including any tools or agents you launched, what did you search for recorded tensions against that authority, what could you not reach, and what did you find (or none), with each record's entries, binding and asserter?"

Report each part the delegate leaves unanswered, including when it returns nothing, and the uncovered rest of an answer covering only part of the work, as a gap, never as none, a null or no selection: findings always; realized results unless the delegated task evidently produced, ran and reviewed no results and prepared no gate evidence; variants, for a returned result, with unknown selection history and claim limit, unless the task evidently could not select variants.
```

Specialist variant, block 918 B, net **+423 B**: the same lead line and first two questions, then:

```markdown
Report each part the delegate leaves unanswered, including when it returns nothing, and the uncovered rest of an answer covering only part of the work, as a gap, never as none or a null: findings always; realized results unless the delegated task evidently produced, ran and reviewed no results and prepared no gate evidence.
```

**Measurement method.** The current exact sentences E1 (all six), E2 and E3 (roles) were removed from copies of `source/*/SKILL.md` at `6d09418`. Each matched exactly once. The block was inserted after the completion heading, and source bytes were compared. Generated sizes are the committed `dist/skills/*/SKILL.md` plus the same delta. The first review independently reproduced this method for revision 1's wording.
