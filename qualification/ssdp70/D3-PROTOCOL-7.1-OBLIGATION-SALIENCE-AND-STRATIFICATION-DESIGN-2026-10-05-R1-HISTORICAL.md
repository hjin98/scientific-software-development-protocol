---
kind: d3-cycle-design-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (task-stated successor to the non-qualified 7.0 candidate; label confirmation is open decision OD-1)
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e
status: proposed — revision 1; authored by the D3 design context; requires fresh independent Review; not self-accepted
companion: PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (proposed contract revision 16)
---

# D3 design: delegate-request salience and qualification stratification for the Protocol 7.1 candidate

## 0. Decision summary

- **Serious Challenge:** none raised. One floor-feasibility risk is surfaced as a reopen trigger (§9 R3), not as a challenge. The evidence does not show that the 100% delegate-request floor is unrealizable.
- **Blockers to authoring this design:** none.
- **Open stakeholder decisions:** three (§10: OD-1 version label, OD-2 carrying over the 7.0-scoped decisions, OD-3 the SD-B reading of the repeated qualifier). OD-1 and OD-2 bound the contract amendment, not the entrypoint design.
- **What changes:**
  - **Entrypoints.** The delegate-request sentences of elements 1–3 move out of the dense completion prose. They go into one structured block at the head of the same completion clause: self-contained, copyable questions, each carrying every qualifier the §11.3 *Request* rule checks, followed by the receiving-side gap rule.
  - **Variants of the block.** The four role entrypoints carry 4 questions; `software-documentation` and `software-maintenance-audit` carry 2; `repository-hygiene` carries none.
  - **No doctrine change.** No element, label meaning, owner, kernel, description or placement *section* changes.
  - **Qualification.** Four narrow contract deltas (companion amendment). They add to the activation strata already accepted, which are reused unchanged.
- **Mandatory floors untouched:** O1–O3 (§4), the §4.5 claim-integrity floor, elements 4–7, R1/R2, the label table, the 6.6 text-preservation rule, the fixed-cost backstop and every §3 qualification floor.

## 1. Governing parents and authority

| Parent | Role here |
|---|---|
| SSDP 6.6.0 (`PROTOCOL-RELEASE-STATE.yaml` `accepted_current`) | Sole governing protocol. All 7.x source is non-governing development material. |
| Consolidated workplan `SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED` | §4 obligation-binding rule (stakeholder-accepted); §8.3 frozen elements, label table, specialist placement, SD-B target and backstop; §11.3 *Route*/*Request*/*Owed gaps* rules; §0.1 activation overlay rev 7 (independent PASS). |
| Canonical owner `source/shared/references/scientific-inspectability-and-initiative.md` §6.3.11 item 11 | Delegate duty semantics: request "in its instruction", answerable either way, covering launched work. Line 402 says doc/audit routes do not ask for variant or tension returns. |
| Contract `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | Rev 8 activation strata (independent PASS, `ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Rev 15 package-access ledger (`PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-CONTRACT-REV15-2026-10-04.md`). Not edited by this design. |
| Stakeholder decisions | Option A closeout of 7.0 (stands for 7.0). Deterministic-activation decision §§1–7 (Q1–Q5). SD-B, SD-B confirmation, 2.0× backstop relaxation, SC1/SC2, package-access ledger. |
| Task authority (2026-10-05 D3 task) | Stakeholder direction **Option B: re-open design** for a successor candidate, relayed in the task. No separate stakeholder record exists; this design cites the task as the source. |

## 2. Premise reconciliation (task brief against repository state)

The task brief is data. Each claim was checked against the files.

| Brief premise | Repository finding | Consequence |
|---|---|---|
| 42 of 43 critical failures had no root selected; ordinary entry activated SSDP in 10.7% of p70 runs | Confirmed: diagnosis §1 (13/122 p70; 42/43 critical failures; 25/25 M07 opportunities without a root). | — |
| The contract must be amended for entry strata, delivery-conditioned scoring and multi-profile strata | **Already realized.** Contract §1 item 12 (deterministic vs ordinary strata, `runtime-command`/`harness-injection`, undelivered run → inadmissible plus activation failure, ordinary runs enter no floor except retained false-activation floors) and the §3 *Deterministic activation* row. Workplan §0.1 items 1–7. Primary flash family; other profiles are non-rescuing strata. Contract rev 8 and overlay rev 7 received independent PASS. | Objective 2 shrinks to residual deltas (§7; companion amendment). Re-authoring the strata would duplicate an accepted owner. |
| A structured checklist is the remedy for salience | **Already probed.** `STAGE-7-M07-CHECKLIST-PROBE-RESULT-2026-10-04.md`: core 14/50 → 46/50; fully conformant 1/14 → 12/14; strict 5/50 → **4/50**. Cause of the strict misses: agents copy the questions and drop the preamble that carried "including tools or agents it launched". | The design must put every checked qualifier *inside each question* (CD-2), not only add a checklist. |
| Specialists should receive the same 4-part template | **Contradicted by frozen authority.** §8.3 specialist placement: documentation carries elements 1, 4, 6 and audit carries 1, 4; neither carries element 2 or 3. Owner line 402 and the §11.3 *Route* rule (variant part not scored on these routes) agree. | Specialists get the 2-question variant (CD-3). A 4-part template there would be an unauthorized duty expansion. |
| The duty is buried in a ~2 KB paragraph | Partly. Element 1 is ~2 KB. The delegate request is actually split across elements 1, 2 and 3 (three sentences in three items, each with its own gap rule). | Strengthens the case for one consolidated block (CD-1). |
| Brief lists 4 core parts as F/N/V/T | Matches the §11.3 *Request* parts (findings, null, variant, tension-search). | — |

The missing item 5 in the D3/D4 entrypoint numbering is expected: element numbers are workplan identifiers (§8.3), and element 5 is D1/D2-only. It is not a defect.

## 3. Root causes and evidence applicability

| Defect | Owner | Evidence (all development data, non-blind) | Applicability limit |
|---|---|---|---|
| **A. Delivery/scoring conflation.** Stage 7 scored doctrine on runs where no doctrine was delivered. | Qualification design (contract/workplan §11) | Diagnosis §§1–5; runtime-command probe | Repaired in substance by rev 8 strata. Residual: report labelling, fixture cue, request timing, subject retarget (§7). |
| **B. Obligation salience.** With the doctrine loaded, p70 asked 6–10 of 25 owed parts; the tension part almost never. | Consumed-surface form of elements 1–3 (§8.3 wording, D4-delegated, made a D3 cycle decision here) | Doctrine-loaded probe; checklist probe | One model (GLM-5.3-Flash), one route (D4, pinned), 7 episodes, ≤2 replicates, scored by an unblinded diagnostician. Supports a direction, not a qualification claim. |
| **C. Fixture cue.** "Delegate is scripted, not SSDP governed" plus a pre-stated return depressed requests (6→10 of 25). | Fixture custody (contract) | Doctrine-loaded probe variant B | One replicate; suggestive. |
| **D. Reactive follow-ups.** Owed questions asked only after the bare return. | Contract scoring precision | Both probes flag it; neither resolves it | A scoring ambiguity that changes M07 dispositions. It must be fixed before runs (I66-4). |

## 4. D3 cycle decisions (frozen for this cycle; wording delegated)

**CD-1 — One delegate-request block, relocated, not added.**
- **Where.** The delegate-request sentences and their unanswered-part rules leave elements 1, 2 and 3. They become one contiguous block at the head of the existing "Scientific completion…" section, before element 1.
- **Why there.** That is where the entrypoint discusses delegation. The probe evidence placed the checklist immediately before element 1.
- **Single representation.** No sentence keeps a duplicate in the element prose.
- **What stays in element prose.** The delegator's *own* reporting duties stay where they are: element 1's carry-forward of delegates' findings, element 2's own variant disclosure, and element 3's reporting of delegate search scopes and judgments with no reported search.
- **Placement under §8.3.** The block stays inside the "one clause in its Completion/report contract" that §8.3 places. It is internal structure of that clause, not a new section or routing line.
- **If a reviewer reads it as a placement change.** The workplan overlay records it as a governed §8.3 form change, so it is covered under either reading.

**CD-2 — Every checked qualifier lives inside its own question.**
- **Form.** Each owed part is one self-contained question addressed to the delegate, answerable either way. Each carries the qualifiers the §11.3 *Request* rule checks for that part:
  - **all parts:** "including any tools or agents you launched";
  - **findings:** "or state that you have none";
  - **realized results:** produce/run/review realized results or prepare gate evidence; the null envelope as examined and material unexamined areas;
  - **variants:** more than one variant, *including changes made after seeing results*, with the disclosure;
  - **tensions:** searched / could not reach / found-or-none, each record's entries, binding and asserter.
- **Lead line.** It states:
  - the condition: "unless the predicate evidently excludes the delegated work";
  - the timing: in the delegation request itself;
  - the change-only rule: answers are owed even for change-only work.
- **Tension gate.** The tension question keeps its own gate: only when the delegate relies on accepted D1/D2 authority for a consequential judgment. This minimizes the unowed-probe burden that the checklist probe observed.
- **Receiving-side rule.** It follows the questions, carrying:
  - the gap rule;
  - the partial-coverage rule;
  - "never none, a null or no selection";
  - each part's exemption (findings: none; null: evidently no realized results and no gate evidence; variants: only for a returned result, and exempt when the task evidently could not select);
  - unknown selection history and claim limit for the variant gap.

**CD-3 — Route variants, one wording per variant.**
- **Roles** (D1, D2, D3, D4): findings, realized results, variants, tensions.
- **`software-documentation`, `software-maintenance-audit`:** findings and realized results only. The receiving rule omits the variant clause and "no selection".
- **`repository-hygiene`:** nothing (outside the predicate; §8.3).
- **Common wording.** The specialist block's lead line and two questions are byte-identical to the role block's. The test invariant "one wording per element across entrypoints" extends to one wording per block variant.

**CD-4 — No doctrine, owner, kernel or selection change.**
- **Owner.** §6.3.11 already says the request is made "in its instruction", answerable either way and covering launched work. The block realizes that text and adds no meaning.
- **Unchanged:**
  - the label table;
  - the R1/R2 routing line;
  - the descriptions;
  - the 6.6 text-preservation rule ("no 6.6 entrypoint text is removed or reworded"), since only Protocol 7 additions move.
- **Other dense duties.** Null envelope (own), variant disclosure (own) and choice provenance are named by the checklist probe as candidates for the same treatment. They are **not** restructured this cycle: no doctrine-loaded evidence shows their uptake failing (§8 non-goals; §9 R2).

**CD-5 — Burden attribution (SD-B).**
- **Accounting.** The block's bytes are attributed to elements 1, 2 and 3 under the §8.3 per-element rule: each question and gap clause maps to its element.
- **Repetition.** The qualifier "including any tools or agents you launched" is repeated once per question. That is a deliberate per-emitted-unit carriage requirement, evidenced by the checklist probe's strict-miss cause, not redundancy in the SD-B sense.
- **Whether that reading holds** is OD-3. If the reviewer or stakeholder rejects it, the fallback (see the sketch below) is a single shared closing line in the request rather than a preamble the delegator does not copy. It is weaker on evidence.
- **Measured static effect** (reference wording, Appendix A):

| Entrypoint | Source before → after (B) | Δ |
|---|---|---|
| each role (D1, D2, D3, D4) | e.g. D4 12,947 → 13,520 | **+573** |
| documentation, maintenance audit | e.g. audit 7,945 → 8,324 | **+379** |

  Backstop routes T1/T7/T8 are all `software-implementation` (`qualification/ssdp66/eval/scenarios.yaml`). Its generated `dist` entrypoint goes 14,454 → **15,027 B**, against the 16,208 B static draft limit (2.0 × 8,360 B minus the 512 B margin). That leaves 1,181 B. Live paired medians remain a qualification measurement, not a static claim.

  Fallback sketch for OD-3, not recommended: a final quoted line "Each answer covers your own work and any tools or agents you launched."

**CD-6 — Request timing.** The block says "in the delegation request itself". It matches owner §6.3.11 ("in its instruction") and the §11.3 *Request* rule ("the delegator's instruction"). The scoring consequence is fixed in the contract (amendment A3). A follow-up question after the delegate returns can still remove an owed *gap* (outcome), but it does not satisfy the request part.

**CD-7 — Pre-campaign development gate (cheap discriminator before a blind campaign).**
- **Run.** After D4 realization and before any fresh blind campaign, re-run the de-cued M07 corpus on the primary flash `runtime-command` profile, as **development data**:
  - all seven episodes;
  - ≥2 replicates;
  - the three arms p66, p70 and the realized 7.1 candidate;
  - for C048/C050, the restored one-line task description from the checklist probe.
- **Scoring.** Core and strict, by a context that did not author the wording.
- **Uses.** It decides only whether to proceed, iterate the wording, or escalate (§9 R3). It enters no campaign count (contract §1 item 7 purpose accounting), and its fixtures stay non-blind.

## 5. Lossless relocation map

| Current sentence (source, all roles unless noted) | New location | Meaning check |
|---|---|---|
| E1a "Unless the predicate evidently excludes a delegate's work, ask for findings or none and whether its work including launched tools/agents produced, ran or reviewed realized results or prepared gate evidence, with a null envelope if so" | Lead line condition + **Findings** + **Realized results** questions | Condition, either-way form, launched-work coverage, null envelope (now also defined in-question) — carried. |
| E1b "asked answers are owed even for change-only work" | Lead line | Carried. Element 1's "adds nothing except asked delegate answers/gaps" stays in place. |
| E1c "Unanswered findings are always a gap; unanswered null is a gap unless …; partial work coverage leaves a gap, never a null/no findings" | Receiving-side rule | All three conditions and exemptions carried. |
| E2a "Ask each delegate asked for findings whether its work including launched tools/agents evaluated >1 variant, including changes after seeing results, and for its disclosure if so" (roles only) | **Variants** question | Same delegate set (every one asked for findings); after-result changes inside the question; disclosure fields named. |
| E2b "A returned result without that answer, or with partial work coverage, is a gap with unknown selection history and claim limit, never no selection, unless the task evidently could not select variants" (roles only) | Receiving-side rule, variants clause | Carried, including "returned result". |
| E3 "Ask a delegate relying on it for such a judgment to return searched/unreachable scopes and found records with entries, bindings and asserters" (roles only) | **Tensions** question with its gate | Carried. The delegator's own reporting sentence stays in element 3. |
| Specialists: E1a–E1c only | Specialist block | Carried. E2/E3 are absent before and after. |

Required D4 test consequence: `tests/test_protocol_70_scientific_inspectability.py` currently pins "Unanswered findings are always a gap" in `test_consumed_clauses_carry_label_meanings`. D4 replaces it with the block's equivalent meanings and adds block-variant placement and one-wording checks. Weakening the assertion is not allowed.

## 6. Qualification consequences

The candidate changes after exposure, so contract §8 requires fresh blind qualification. The companion amendment (proposed contract revision 16) makes four deltas and otherwise reuses revisions 8 and 15 unchanged:

- **A1 — Subject retarget.** The candidate becomes the 7.1 successor. The 7.0 Stage 7 runs and all probe evidence are development data. All current fixtures are non-blind, so fresh custodian fixtures are required. The precondition is OD-2.
- **A2 — Delegator-visible fixture realism.** Delegates stay scripted (§11.3), but delegator-visible artifacts do not state that, do not pre-state returns, and keep a self-contained task description.
- **A3 — Request timing.** Request conformity is scored on the instruction that launches the delegated work. Follow-up-only asks are counted descriptively and may resolve outcome gaps.
- **A4 — Undelivered-treatment labelling.** No pooled cross-stratum headline. Oracle outcomes on ordinary no-selection runs are reported as *undelivered-treatment outcomes* under the §11.3 placement-miss rule, never as candidate doctrine failures or arm doctrine effects.

Multi-profile stratification needs no delta. The primary flash `runtime-command` family must pass every floor; a reasoning-class profile may be offered in the campaign record as a non-rescuing additional stratum (contract §1 item 12).

## 7. D4 handoff boundary

- **Affected surface:**
  - `source/roles/{scientific-formulation,numerical-algorithm-design,software-design,software-implementation}/SKILL.md`;
  - `source/specialists/{software-documentation,software-maintenance-audit}/SKILL.md`;
  - generated `dist/` (via `build_skills.py`, never hand-edited);
  - `tests/test_protocol_70_scientific_inspectability.py`;
  - `qualification/ssdp70/measure_entrypoint_additions.py` attribution (block → elements 1–3);
  - Orchestrator Core snapshot, if it embeds entrypoints;
  - `source/PROTOCOL_VERSION`, `CHANGELOG.md`, README closeout and `history/SEMANTIC_EVOLUTION.md`, only after OD-1, under the repository release-document rules.
  - `PROTOCOL-RELEASE-STATE.yaml` is **not** touched.
- **Delegated to D4:**
  - exact wording, bold/list markup and question labels;
  - whether quotes are used;
  - test structure.
- **Not delegated:**
  - CD-1 single relocated block inside the completion clause;
  - CD-2 per-question qualifiers;
  - CD-3 route variants;
  - CD-6 request-timing phrase;
  - no change to any other element, the label table, R1/R2, descriptions, owner or kernel.
- **Acceptance at real owners:**
  - the inherited regression suite;
  - the P7 structural tests (updated, not weakened);
  - package build and independent validation;
  - committed-dist parity;
  - `git diff --check`;
  - frozen-resource integrity;
  - Orchestrator Core snapshot and tests when affected;
  - static re-measurement of the D4 generated entrypoint against 16,208 B;
  - per-element SD-B attribution checked by a context that did not author the wording;
  - a lossless check of §5 by that context;
  - CD-7 gate results.
- **Equivalent D4 reconciliation (no D3 reopen):** wording or markup variants that keep CD-1–CD-6.
- **Reopens D3:** see §9.

## 8. Non-goals

- Redoing or re-reviewing the rev 8 activation strata or rev 15 ledger.
- Restructuring non-delegate duties (null envelope, own variant disclosure, choice provenance).
- Changing the 100% delegate-request floor.
- Changing description text.
- Adding owner reads.
- Kernel placement.
- Re-scoring or re-opening the 7.0 Stage 7 determination, which stays NON-QUALIFIED.
- Editing `PROTOCOL-RELEASE-STATE.yaml`, contract revision 15 bytes, D3 package-access revision 8 bytes, or custody trees under `/home/samjin/ssdp70-omp-stagef/`.

## 9. Reopen triggers

- **R1 — Ordinary-entry evidence.** Ordinary-entry results return no route to doctrine redesign (stakeholder 2b/Q2). They feed only the retained false-activation floors.
- **R2 — Another dense duty misses.** If CD-7 or the campaign shows a material miss rate on a non-delegate completion duty under delivered doctrine, the same structural remedy is the next D3 candidate for that duty.
- **R3 — Strict-request floor feasibility.** If CD-7 shows residual strict-measure misses on the flash primary after CD-2, the question goes to the stakeholder *before* a blind campaign: further wording iteration, floor reconsideration, or accepting a likely non-PASS. The 100% process floor is §3 authority. This design does not weaken it.
- **R4 — Fixed-cost backstop.** A static or live breach of the backstop → stakeholder escalation per §8.3 (unchanged).
- **R5 — Request-timing scoring.** If the independent check or stakeholder reads CD-6/A3 differently (for example, that follow-ups satisfy the request), CD-6 and A3 reopen together.

## 10. Open stakeholder decisions

| ID | Question | Recommended answer | Blocks |
|---|---|---|---|
| OD-1 | Version label of the successor candidate | **7.1.0**, as task-stated. It keeps the exposed, non-qualified 7.0 candidate identity distinct (Option A says 7.0 "SHALL NOT be ratified"). | Release-document and `PROTOCOL_VERSION` work; contract subject text (A1) |
| OD-2 | Do the decisions recorded as "Protocol 7.0" decisions carry to the successor unchanged? These are SD-B, SD-B confirmation, the 2.0× backstop ("for Protocol 7.0 only"), SC1/SC2, activation Q1–Q5 and the package-access ledger. | **Yes**, all unchanged. They govern the same workplan target; this cycle changes no premise they rest on. | Contract A1; the backstop numeric value |
| OD-3 | Is the per-question repetition of the launched-work qualifier required content under SD-B attribution? | **Yes** (CD-5 evidence) | SD-B attribution check; fallback wording |

## 11. Project memory (PEM)

The workplan is memory-bound (§0.2). The basis is unchanged: `main` = `2585b73f…`, PEM blob `15617971…`, identical on HEAD `6d09418`. Task-local HAS dispositions:

| ID | Disposition | Reason |
|---|---|---|
| I66-1 | APPLICABLE | The block stays on the consumed entrypoint. No owner-only reliance is introduced. |
| I66-3 | APPLICABLE | Relocation (net +573/+379 B), not inlined owner doctrine. Bytes are attributed per element (CD-5). |
| I66-4 | APPLICABLE | A3 removes a scoring ambiguity before runs. A2 removes a fixture artefact that confounds the oracle. |
| FF-001, SP-002, PC-001, SP-001, DS-001 | unchanged from §0.2 | No release, publication or frozen-resource surface changes in this design. |

No PEM mutation.

## Appendix A — Reference wording (non-binding; feasibility evidence only)

Role variant, measured 1,590 B as a block. It replaces E1a–E1c, E2a–E2b and E3, for a net +573 B per role:

```markdown
**When you delegate.** Unless the predicate evidently excludes the delegated work, put these questions in the delegation request itself, keeping each qualifier inside its question; answers are owed even for change-only work:

- **Findings:** "Report your material findings, including from any tools or agents you launched, or state that you have none."
- **Realized results:** "Did your work, including any tools or agents you launched, produce, run or review realized results or prepare gate evidence? If so, give your null envelope: what you examined and what material areas you did not."
- **Variants:** "Did your work, including any tools or agents you launched, evaluate more than one variant, including changes made after seeing results? If so, give count and kind, selection criterion and data, and lineage."
- **Tensions**, only if the delegate relies on accepted D1/D2 authority for a consequential judgment: "For that judgment, including any tools or agents you launched, what did you search for recorded tensions against that authority, what could you not reach, and what did you find (or none), with each record's entries, binding and asserter?"

On return, report each unanswered part, and the uncovered rest of an answer covering only part of the work, as a gap, never as none, a null or no selection: findings always; realized results unless the delegated task evidently produced, ran and reviewed no results and prepared no gate evidence; variants, for a returned result, with unknown selection history and claim limit, unless the task evidently could not select variants.
```

Specialist variant, 874 B, net +379 B: the same lead line and first two questions, then:

```markdown
On return, report each unanswered part, and the uncovered rest of an answer covering only part of the work, as a gap, never as none or a null: findings always; realized results unless the delegated task evidently produced, ran and reviewed no results and prepared no gate evidence.
```

**Measurement method.** The current exact sentences E1 (all six), E2 and E3 (roles) were removed from copies of `source/*/SKILL.md` at `6d09418`. The block was inserted after the completion heading, and source byte counts were compared. Every removed string matched exactly once. Generated sizes are the committed `dist/skills/*/SKILL.md` plus the same delta. The build inserts the entry contract only at the separate placeholder.
