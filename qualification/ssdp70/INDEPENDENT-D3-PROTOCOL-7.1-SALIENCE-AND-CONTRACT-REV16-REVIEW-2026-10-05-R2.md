---
kind: independent-d3-and-qualification-contract-review
governing_protocol_version: 6.6.0
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e (plus the uncommitted subject bytes below)
reviewer: fresh independent context; did not author any subject byte; not the author of the first review
subjects:
  design: qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md (revision 2) sha256 659a65a8915ed68b2ee8a86826a7a613c0cc6ca9dcdccf29d7bba2c8793a92a1 (verified)
  contract_rev16: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (record revision 2) sha256 2d8d0a10d8eea998a5a7971b7d94aee7d683999cb98e9e526992a6db5070b6d4 (verified)
  overlay_rev8: workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md sha256 01523e349dbd12bbfd99dc89e8c45a02d2532db2724196cf6a4ad06ff0a35705 (verified; scope = all bytes changed vs HEAD per `git diff`)
  supporting_record: qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md sha256 e0cb2105c8cc169f71de92b314a02942423a10535f61f84633d24f417d7facff (verified; fidelity checked, no verdict)
design_verdict: PASS
contract_rev16_verdict: PASS
overlay_rev8_verdict: PASS
---

# Independent Review R2: Protocol 7.1 delegate-request salience design rev 2, contract revision 16 (record rev 2), overlay revision 8

Governing SSDP version: 6.6.0. Applied: the `software-design` Independent Review and Challenge contract. All 7.x material is non-governing development data.

Each verdict is PASS because I found no blocker. The gaps below are real, cheap to fix, and should be fixed before the contract merge and before D4 starts. None of them makes a frozen element, owed disposition or threshold wrong as the records now stand.

## Serious Challenge

None. The parent authority is coherent for this change: §4, the §8.3 elements, the label table, specialist placement, SD-B and the backstop, §11.3, owner §6.3.11 and contract rev 15. I checked §14's delegate-route trigger separately (m-5).

## Blockers

None.

## Gaps (fix before the merge and before D4; not independently blocking)

### G-1: Design §0 misstates the timing-adjusted strict evidence

- **Location:** design §0, "Material uncertainty".
- **The problem:** §0 says 0 of 50 owed parts met every strict qualifier before the return "in either the checklist arm or the current arm". My recount of `scores.json` gives current arm (p70) **2/50** (C046-r0 V and T) and checklist arm (p70ck) **0/50**. The design's own §2 table and the overlay both say 2 against 0 correctly.
- **Why it matters:** the headline hides the fact that, before the return, the checklist arm had nominally *fewer* strict hits than the current wording. That is the prominent material-uncertainty item, so under the Lossless Representation Rule it must be stated accurately.
- **Repair:** say "2 of 50 (current) and 0 of 50 (checklist)".

### G-2: Design §5 and CD-2 claim more label-table content than the reference wording carries

- **Variants question.** §5 row E2a claims "the full label-table field set". The question asks only for "lineage". The variant-search row also requires "delegated/resumed survivor lineage without double-counting overlapping trials".
- **Tensions question.** CD-2 and overlay item 1 say each question carries "the label-table content of what it asks for". The Tensions question asks for "recorded tensions" without the row's meaning: a recorded finding bearing on the authority that has not been raised as a Serious Challenge.
- **Why this is not B-D1 again:**
  - Frozen losslessness still holds on the entrypoint. Element 2's and element 3's retained delegator text carries both meanings (`software-implementation` lines 43 and 45 at `6d09418`).
  - Frozen element 2 asks only for "its variant-search disclosure".
  - The omissions do not reopen the understatement path B-D1 found. The lower bound, unknown interval and claim limit are now present, and over-counting is conservative.
- **Why it still matters:** a D4 that copies Appendix A would fail the overlay's own requirement, which D4's independent lossless check is told to apply. The §5 verdict text is factually wrong.
- **Repair:** either add the two phrases (my estimate is about 150 B, which puts the D4 entrypoint near 15,440 B, still under 16,208 B), or narrow the CD-2, overlay and §5 claims to what is carried.

### G-3: Contract A2 item 1's enumerated scope omits known model-visible cues on the same MCP server

- **What is enumerated:** A2 item 1 lists the executor package and the delegate interface (tool name and description, parameter schema, return wrapper).
- **What `qualification/ssdp70/eval/stub_tools/mediator.py` also exposes from the same server:**
  - `initialize` returns `"instructions": "Private Stage F qualification stand-ins (<server_id>)"` (line 250);
  - the sibling tools the tension cases need are described as "qualification-owned issue stand-in" (lines 42–54).
- **Failure scenario:** D4 neutralizes the items that design §7 lists (delegate description, wrapper, store identity). The checker checks the enumerated scope and a captured delegate result, and passes. A server-level "stand-ins" string or the sibling tool descriptions still tell the executor that the delegate is a stand-in.
- **Mitigation:** the general sentence ("Nothing visible to the executor …") and "through the exact adapter and profile" arguably already cover this, which is why this is a gap and not a blocker. I did not verify whether OMP shows MCP server instructions to the model.
- **Related cue:** the observed tool name is `mcp__ssdp_delegate` (server id `ssdp`). A2 bans implying "not SSDP governed" but not implying "SSDP governed". A delegator that believes its delegate is SSDP-governed has a reason not to ask, and that is exactly the behavior being measured.
- **Repair:**
  - name in A2 item 1 the whole model-visible tool catalog and system context (server instructions/serverInfo and co-hosted tool descriptions), plus the launching task prompt;
  - make the governance clause symmetric ("states or implies the delegate's governance status either way");
  - add the server instructions string to the design §7 mediator surface.

### G-4: Contract A3 does not make "same delegated work" operational, and conflicts with §11.3 counting

- **The conflict:** A3 scores "a call delegating different work" as a new delegation "in its own right". Workplan §11.3 *Request* counts each failure "once per delegate part per episode".
- **Why the mediator makes this matter:** with `mediator.py`, the only operational identity is `agent`, and every call to an agent returns the same frozen return. A re-invocation of `worker_0` with a full question set and a different-sounding task could be classified as a new, conformant delegation, or as a follow-up. That depends on the scorer's reading of the instruction text, and the two counts conflict.
- **Repair (R-op):** state that every call to a case's fixture delegate within an episode is the same delegated work. A case with several assignments predeclares distinct delegates. This keeps the "once per delegate part per episode" counting.

### G-5: Contract A1 reading rule collides with the contract's earlier-campaign disclosure clause

- **The collision:** the reading rule maps "Protocol 7" to the 7.1.0 candidate. Contract §1 item 12 (line 145) requires "Every earlier campaign of this candidate and of earlier Protocol 7 candidates under this workplan is disclosed". Read through the rule, "earlier Protocol 7 candidates" means "earlier 7.1.0 candidates", which no longer reaches the 7.0 Stage 7 campaign.
- **Effect:** A1 calls that campaign "development data" but does not say it is disclosed.
- **Why this is a gap, not a blocker:** workplan §0.1 rev 7 item 2 ("Every earlier campaign is disclosed") still binds independently.
- **Repair:**
  - exempt "earlier Protocol 7 candidates" from the reading rule, or add "and is disclosed in the report" to *Development data*;
  - scope "the route probes" in *Preservation panels* to "the 6.6 route probes", so the §11.5 sentinels, which are custodian material, are unambiguously fresh.

## Minor

- **m-1: OD-2 enumeration in the stakeholder record.** The record quotes OD-2 as presented, without a list ("the decisions recorded as 'Protocol 7.0' carry over unchanged"). It then states an enumerated "Effective decision" of five decision sets without labelling the enumeration as the recorder's.
  - The enumeration omits two 7.0-named decisions: the 2026-09-28 single-participant human trial and the 2026-10-04 non-executor custody audit. Both bind through unchanged contract text (§7, §1 item 9), so nothing is lost in effect.
  - The literal question would also carry campaign-specific decisions (the Stage 7 Option 1 admission), which the enumeration sensibly excludes.
  - Label the list as the recorder's reading (as OD-3 does), or cite the enumerated recommendation if the stakeholder saw it (revision 1 design §10 enumerated it). Also state the disposition of the unlisted 7.0-named decisions.
- **m-2: SD-B attribution of reference-wording bytes.** No frozen element carries "keeping each qualifier inside its question" (lead line, about 45 B). Neither does the Tensions question's launched-work clause: §8.3 *Consumed-surface sufficiency* and the §11.3 *Request* tension check do not include launched-work coverage for element 3.
  - The launched-work clause is owner-supported: §6.3.11 *Form* applies to "the request", whose "those returns" include the tension envelope.
  - The stakeholder's OD-3 question literally said "in each question", and the revision 1 block it referred to already had the clause in the Tensions question. So the recorder's reading is conservative, not overstated.
  - "(or none)" has no such coverage. The attribution check should rule on all three; if they are non-required, D4 drops them.
- **m-3: "no results" versus frozen "no realized results".** The gap rule's null exemption reads "produced, ran and reviewed no results". Read literally, that is narrower than the frozen exemption, which could produce unowed null gaps (§11.3 burden). D4 should use "no realized results".
- **m-4: §2 overstatement.** "Every remaining strict miss in the checklist arm traces to a launched-work qualifier" is too strong. C044-r0 T also lacked the unreachable scopes and entries, and C048-r0 V lacked after-result changes. The probe report itself says "nearly every".
- **m-5: §8 misquotes §14's trigger.** §8 says "*Delegate-route convergence* prescribes narrowing when Review finds further *semantic* defects". The §14 trigger (workplan line 1123) reads "draws a further Review finding **or fails §11 qualification**". Its carve-out says a governed repair that "only carries its meaning onto the consumed surface, aligns wording to it or corrects or adds a scoring case" is not a prohibited addition.
  - The conclusion still holds:
    - the first review's B-D1 was a carriage finding, repaired by carriage;
    - Stage 7 delivered no M07 treatment, which is a placement miss under §11.3 *Route*, not a §11 qualification failure of the duty;
    - the block adds no request part or exemption.
  - Cite the full trigger and that reasoning.
- **m-6: overlay citation.** The overlay says contract rev 15 "with D3 package-access revision 8, now has independent PASS (`…-CHECK-CONTRACT-REV15-…`)". That record's verdict 2 is a consistency PASS for D3 rev 8. D3 rev 8's own PASS is verdict 1 of `PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-D3-REV8-AND-CONTRACT-REV14-2026-10-04.md`. Cite both. The substance is true.
- **m-7: CD-6/A3 wording.** The block says "in the delegation request itself", while A3 also credits pre-return messages. With the synchronous mediator this cannot diverge, but state that A3 is the scoring reading and the surface wording is the stricter instruction.

## Repair-map verification (first review)

| Finding | Status |
|---|---|
| B-D1(1) "On return" | **Repaired.** Gap rule has no return condition ("including when it returns nothing"); variant gap keeps element 2's "returned result", matching §11.3 *Owed gaps*. |
| B-D1(2) variant disclosure | **Repaired in substance** (held-out reuse, lower bound/unknown interval/claim limit). Residual over-claim: G-2. |
| B-C1(1) checker scope | **Repaired** for the delegate interface, captured result and re-return residual (A2 items 1, 5). Residual: G-3. |
| B-C1(2) task vs return facts; chained timing | **Repaired** (A2 items 2–3; checker verifies item 2 in full, including the normative first sentence). |
| G-1 timing caveat | **Repaired** in the §2 table and the overlay; §0 restatement wrong (G-1 here). |
| G-2 CD-7 burden | **Repaired** (unowed parts/gaps against the contract §5 1-per-12 bound, which I verified). |
| G-3 scripted follow-ups | **Repaired** (A3 *Scripted delegates*, re-invocation rule). Residual: G-4. |
| G-4 A1 scope | **Repaired** (reading rule, panels kept). Residual: G-5. |
| G-5 A4 | **Repaired.** The pool carve-out matches §1 item 12's pooled false-firing and owner false-activation counts. "Comparative evidence of doctrine effect" is scoped correctly. No reported information is lost (per-stratum and per-profile components remain). |
| G-6 stakeholder record | **Repaired.** Record exists; reply quoted verbatim; "Proceed" read conservatively (no D4 authorization). See m-1. |
| m-1 OD-2 dependency | **Repaired** (§0, CD-5). |
| m-2 tension qualifiers | **Recorded** for the attribution check (m-2 here). |
| m-3 static pre-measurement | **Repaired** (§7). |
| m-4 stale lines | **Repaired** in the overlay; the contract merge rule corrects §8 status. |
| m-5 header scope | **Repaired.** `implementation_handoff` is scoped, and package-access/harness work is unaffected. |
| m-6 §8.3 marker | **Repaired.** The marker sits on the completion-clause bullet. |
| m-7 convergence | **Addressed** (§8), with a misquote (m-5 here). |

## Other checks holding

### Losslessness against elements 1–3, owner §6.3.11 and the label table

All of the following are carried:
- the condition "unless the predicate evidently excludes";
- the same delegate set for every part;
- the either-way form, including "or state that you have none";
- launched-work coverage on findings, null and variants;
- the null envelope with the label's meaning;
- change-only owed answers;
- element 1's "adds nothing except asked delegate answers/gaps", which is retained;
- findings with no exemption;
- the null exemption;
- the variant "returned result" condition, the could-not-select exemption, unknown history and claim limit;
- the partial-coverage rule;
- the tension gate and fields.

The block's generic "each part … as a gap" applied to the tension part coincides with element 3's retained "judgments with no reported search".

The specialist variant matches frozen placement and owner line ~402 (no variant or tension asks). I found no duty expansion beyond m-2.

### Byte measurement

Reproduced independently by extracting Appendix A from the design file, removing the six current sentences by regex at `6d09418` (each matched once) and inserting the block after the completion heading:

| Entrypoint | Δ | Block |
|---|---|---|
| each role | +837 | 1,854 B incl. trailing newline |
| documentation, maintenance audit | +423 | 919 B |

- D4 dist goes 14,454 → **15,291 B**, leaving 917 B under 16,208 B (2.0 × 8,360 − 512, per the 2026-09-28 record, valid under OD-2).
- T1, T7 and T8 are rooted at `software-implementation`.
- The reference script's strings are byte-identical to Appendix A.
- `numerical-algorithm-design` dist would be 16,210 B and `software-design` 17,375 B. Neither is a backstop route.

### Contract

- No threshold changes. A3 is scoring precision of the unchanged 100% floor. A4 is labelling.
- The A4 replaced sentence exists once (line 112).
- The `amends` sha256 equals the contract file's.
- The A3 *Owed gaps* consequence agrees with §11.3 (gaps follow the return's content, never the asking).
- A2 is realizable: the mediator owns name, description, schema and wrapper, and the identical re-return is a disclosed residual.

### Evidence

My recount from `scores.json` (excluding parts annotated "follow-up"):

| Arm | Core | Strict | Fully conformant |
|---|---|---|---|
| p70 | 14 → 10/50 | 5 → 2/50 | 1 → 1 |
| p70ck | 46 → 42/50 | 4 → 0/50 | 12 → 11 |

- Doctrine-loaded variant B: 6 → 10 of 25, as quoted.
- The runtime cues appear in all 30 checklist-probe runs: the store identity in each `trace.jsonl`, and the "scripted qualification delegate" description in `capability-manifest-snapshot.json`.

### Overlay

The overlay is accurate against the records, apart from m-6. Its status lines are scoped, and the §0 STAKEHOLDER DECISION line is faithful. Contract §5's bound is cited as §11.5 there, which is the workplan owner of that bound.

### PEM and HAS

The design §11 dispositions are plausible. No PEM mutation.

## Executed checks

| Command / check | Result |
|---|---|
| `sha256sum` on the 3 subjects and the supporting record; `git rev-parse HEAD` | all match the brief; HEAD 6d09418 |
| `git diff` (workplan) | header 2 lines, §0 decision line, §0.1 entry, §8.3 marker; nothing else |
| Own script `scratchpad/r2rev/mine.py` (Appendix A extracted from the design; regex removal at `git show 6d09418:`) plus `draft_r2.py` run; strings compared with Appendix A | identical deltas; strings byte-equal (True/True) |
| `diff` of source and dist for `software-implementation` | build adds the entry contract only (7.0.0 → 7.1.0 has the same length) |
| `python3 -m unittest tests.test_protocol_70_scientific_inspectability` | 9 OK; the pinned "Unanswered findings are always a gap" is at line 115 |
| `git diff --check`; trailing spaces in the 3 new records | clean / 0 |
| `scores.json` recount script; annotations of all p70ck runs | figures as above; G-1, m-4 |
| `grep` of the store identity across the 30 checklist runs; `C042-p70ck-r1` trace and capability manifest | cue in all; tool `mcp__ssdp_delegate`, server `ssdp70`; corpus prompt "qualification delegate" |
| Read `mediator.py` | G-3, G-4 |
| Read: contract rev 15 §1 items 7, 12 and 13, §3, §4, §5, §8 (selected lines); workplan §0.1, §8.3, §11.3 rules, §14 line 1123; owner §6.3.11 and line 402; backstop, human trial, custody and Option 1 decision records; REV14/REV15 package-access checks; probe result files | as cited |

## Not checked

- The stakeholder's conversation and task brief: not available to me. I relied on the quoted reply given in my brief.
- Whether OMP surfaces MCP server `instructions` to the model.
- Package build, committed-dist parity, the Orchestrator Core snapshot: no source changed.
- Probe runs other than `C042-p70ck-r1` beyond the store-identity grep.
- The later 2026-10-05 package-access D3 deltas, beyond confirming they leave contract rev 15 bytes unchanged.
- No live run.

These verdicts accept no implementation and change no qualification determination: Protocol 7.0 remains NON-QUALIFIED. D4 authorization then follows the overlay's own status line. I recommend fixing G-1 to G-5 before the contract merge and before D4 starts.
