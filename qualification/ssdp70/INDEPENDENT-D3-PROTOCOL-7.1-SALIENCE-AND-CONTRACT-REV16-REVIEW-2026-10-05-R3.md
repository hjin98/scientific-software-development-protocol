---
kind: independent-d3-and-qualification-contract-delta-review
governing_protocol_version: 6.6.0
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e (plus the uncommitted subject bytes below)
reviewer: fresh independent context; did not author any subject byte; not the author of the first or second review
scope: delta check of revision 3 against the R2-reviewed copies (changed bytes, their consistency with the R2-passed text, collateral)
subjects:
  design: qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md (revision 3) sha256 4e0f9de5ad619fd91a5d384524206ec2530b1d7e53642042ba2f915deae17f20 (verified; R2 copy 659a65a8… verified)
  contract_rev16: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (record revision 3) sha256 138b7262bf7ca57f80fc926ad67593dde99b6eb2a1051a572d641bc3d284b9f2 (verified; R2 copy 2d8d0a10… verified)
  overlay_rev8: workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md sha256 719ccc571aa50aecd55d28f55e258efa36460ab480896d37b896d081e02cabe8 (verified; scope = bytes changed versus the preserved R2-reviewed diff)
  supporting_record: qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md sha256 1dfd4e54cb484ac42ab8ea80303ecbe61c85672a8052fd35ae11dd86b9b6e004 (verified; fidelity checked, no verdict)
  unchanged_reference: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md revision 15 sha256 c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920 (verified unchanged, not modified in git status)
design_verdict: PASS
contract_rev16_verdict: PASS
overlay_rev8_verdict: PASS
stakeholder_record_fidelity: quoted words unaltered (only an appended section 3); two statements in the note need correction (m-R3-4)
---

# Independent Delta Review R3: design rev 3, amendment record rev 3 (proposed contract revision 16), overlay rev 8

Governing SSDP version: 6.6.0. Applied: the `software-design` Independent Review and Challenge contract. All 7.x material is non-governing development data. This is a delta check: I reviewed the changed bytes (by `diff` against the `*-R2-HISTORICAL` copies and the preserved overlay diff), their consistency with the R2-passed text, and collateral.

Each verdict is PASS because I found no blocker. All eleven R2 findings (G-1 to G-5, m-1 to m-7) are repaired in substance. The repairs introduce **three new gaps** (G-R3-1 to G-R3-3), two of them in the same G-5 and G-3 repairs, that should be fixed before the contract merge and before D4 starts. None changes a threshold, a frozen element or an owed disposition.

## Serious Challenge

None.

## Blockers

None.

## Gaps introduced or left by the repairs (fix before the merge and before D4; not independently blocking)

### G-R3-1: A1 now says the §11.5 sentinels are fresh, which contradicts the paragraph next to it and the workplan

- **Changed bytes:** A1 *Preservation panels*, new last sentence: "The §11.5 sentinels are custodian material and are fresh under the *Fresh fixtures* rule."
- **Contradiction 1, inside A1.** The same paragraph keeps "T1–T8" as panels that "stay matched to their accepted baselines and are not replaced". The 6.6 corpus's T2 and T3 (`qualification/ssdp66/eval/scenarios.yaml`, `T2-tolerance-within-envelope`, `T3-d2-owned-default`) are the "T2/T3 sentinels" the contract names (contract §1 item 12, line 100). They are both in T1–T8 (kept) and in "§11.5 sentinels" (fresh).
- **Contradiction 2, with the workplan.** Workplan line 952 lists "preservation sentinels reused from the 6.6 corpus where Protocol 7 touches their owners, including the 6.6 authority sentinels", and line 958 speaks of "a matched sentinel that 6.6 closes". Those are reused, not custodian-authored. Only sentinels Stage A newly adds (for example the costly/non-deterministic hygiene sentinel, workplan line 623) are custodian material.
- **Origin.** The phrase follows R2's own repair suggestion ("the §11.5 sentinels, which are custodian material"). R2 did not verify that claim. I did, and it is only partly true.
- **Failure scenario:** a custodian or D4 reads the sentence literally, replaces T2/T3 or the reused authority sentinels, and breaks the matched-baseline preservation comparison; or the pre-run checker flags either choice.
- **Repair:** scope the sentence to sentinels the Stage A map newly authors, for example "Sentinels newly authored by the custodian for this campaign (for example the §11.5 hygiene sentinel) are fresh under the *Fresh fixtures* rule; sentinels reused from the 6.6 corpus stay matched." Or delete the sentence: the "6.6 route probes" scoping already settled the ambiguity R2 found.

### G-R3-2: A2's server-identity requirement is not realizable by the surface D4 §7 lists, and some wording still describes the old, narrower check

- **What the repair requires:** A2 item 1 and design §7 say the server name and identifier, including the tool-name prefix, must imply neither governance status ("`mcp__<server>_delegate` currently implies governance").
- **What pins that identity.**
  - `qualification/ssdp70/eval/adapters/omp.py` line 136-137: `OMP_MCP_SERVER_NAME = "ssdp70"` and `OMP_MCP_SERVER_ID = "ssdp70-qualification-stdio-v1"`. `verify_mcp_binding` (lines ~405-407) rejects any other declared name or id.
  - `mint_mcp_tool_name` derives `mcp__ssdp_delegate` from the name (digits become `_`, then trimmed).
  - The mediator's `--server-id` check (line 281) must equal its `SERVER_ID`.
  - Hard-coded `mcp__ssdp_*` names in `eval/test_omp_integration.py`, and 26 references to these constants across `omp.py`, `test_omp_integration.py` and `test_omp_units.py`.
  - Frozen profile snapshots and capability manifests bind the same name.
- **The gap:** design §7 lists only "the qualification delegate mediator … and its tests". Renaming the server therefore needs the reviewed OMP adapter, its tests and the frozen profile keys, and re-establishing the adapter/profile admission. The design and overlay status text still say "separately governed package-access and harness work is unaffected". That is no longer accurate for the server-name part of A2. The tool description, the sibling tool descriptions, the `instructions` string and the return wrapper are mediator-local, so those parts are realizable as written.
- **Stale narrower wording left in the design:** §7 acceptance still says "an A2 pre-run check of the runtime-visible delegate interface" (line 209), and CD-3's list says "the A2 runtime-interface de-cueing applied" (line 132). The amendment's checker clause is the whole-surface one.
- **Repair:**
  - add the adapter constants, the adapter/integration tests and the profile identity to §7's affected surface;
  - say that renaming the server re-opens the adapter/profile admission, and mark that cost for the stakeholder;
  - correct "harness work is unaffected";
  - align the two stale phrases to "the whole model-visible surface".
  - The alternative is to state that a name change needs a separate governed harness change and that A2 then accepts the `ssdp` tool-name cue as a disclosed residual. That must be an explicit choice, not a silent one.

### G-R3-3: A2 item 1 read literally collides with the frozen owner text in the executor package

- **Changed bytes:** A2 item 1 now bans anything visible to the executor, listing "the executor package", that states or implies "that it is, or is not, SSDP governed".
- **The text in the package:** owner §6.3.11 (shipped in every `dist/skills/*/references/scientific-inspectability-and-initiative.md`) says "A delegate may not be governed by SSDP, so a delegating agent … asks each delegate …".
- **Reading:** that is a generic statement about delegates, not the status of a case's fixture delegate. The R2-passed wording ("not SSDP governed") had the same latent ambiguity. The new, broader and symmetric wording plus a mechanical pre-run checker makes it concrete.
- **Repair:** one clause: the clause concerns the case's fixture delegate; generic doctrine in the package, including owner §6.3.11's "may not be governed", is not a status statement about it.

## Minor

- **m-R3-1: "cannot diverge" is slightly too strong (m-7 repair; design CD-6, A3 *Basis*).** With a synchronous mediator, a same-turn second call to the same delegate carrying the questions is "a message … before it returns" under A3 timing. It is not "in the delegation request itself" in the block's wording. The two readings can diverge in that edge. Say "diverge only for same-turn parallel calls". A3's timing and *Same delegated work* clauses are otherwise consistent: call before the return is timing (ii), call after the return is a follow-up, and every call to the fixture delegate is one delegated work.
- **m-R3-2: stale label and one imprecise figure in the design.**
  - §5's heading still reads "revision 2 reference wording", while rows E1c, E2a and E3 now carry revision 3 wording.
  - CD-5 says "the 172 B of revision 3 content is the G-2 phrases". The G-2 phrases are 163 B (80 B Variants, 83 B Tensions); the other 9 B are "realized " from m-3.
- **m-R3-3: §8 re-justification (m-5 repair) is sound, with three wording points.**
  - The §14 trigger quote is verbatim with honest ellipses (workplan line 1123): the omitted parenthetical "(for example to reporting answers as given…)" and the omitted clause "a case that requires or forbids behavior those elements do not is an obligation or exemption change". The bold on "or fails §11 qualification" is the author's emphasis, not marked as added.
  - "A narrowing needs evidence that the duty itself is unfollowable as written" is the author's gloss. §14 states no such precondition.
  - "adds no … label meaning" is now ambiguous. The block carries two label-table meanings it did not carry in revision 2 (G-2), though it adds none to the table.
- **m-R3-4: stakeholder-record note (m-1 repair).** Two accuracy points:
  - "The same list appears as the recommended answer in revision 1 of the design (§10, OD-2)". In the R1 copy the list is in the *Question* column ("These are SD-B, SD-B confirmation, …"), not the recommended-answer column. That is stronger evidence that the question presented to the stakeholder enumerated the list, so the note understates rather than overstates.
  - The note says the literal OD-2 wording would carry the human-trial and custody-audit decisions too, but excludes the Option 1 admission and the Option A closeout "as such". That is a recorder's reading, and it is flagged as such with an open point. I judge it conservative and correct.
- **m-R3-5: A1 *Development data* sentence adds a small reporting statement.** "The probes and the gate are reported as development data" is a new disclosure duty for probes and the gate. It is harmless and consistent with CD-7's "enters no campaign count". It does not over-claim the item 12 clause (the Stage 7 campaign is "under this workplan"). It is the only sentence that could be read as new scope.

## Verification of each R2 finding

| R2 item | Verdict on the repair | Evidence |
|---|---|---|
| G-1 §0 strict figure | **Repaired, accurate.** | Recount of `scores.json` excluding "follow-up" parts: p70 strict 5 → 2/50 (C046-r0 V, T); p70ck 4 → 0/50 (all four are C042-r1 follow-ups). Core 14 → 10 and 46 → 42. The "nominally no better (0 against 2)" statement is correct. |
| m-4 "nearly every" | **Repaired, accurate.** | p70ck annotations: C044-r0 T "no unreachable/entries"; C048-r0 V "no after-results". Other misses: "no launched coverage". |
| G-2 Variants/Tensions content | **Repaired by adding content; lossless; no duty expansion.** | Variants: "lineage including delegated or resumed work, without double-counting overlapping trials" is the label-table "variant search" row (workplan line 606). Tensions: "a recorded finding bearing on it that has not been raised as a Serious Challenge" is the "tension" row (verbatim meaning). The label-table rule says the entrypoint carries "at least this meaning". It adds no request part and no exemption. §5 row E2a's "label-table variant-search field set" is now true. |
| Byte figures | **Reproduced.** | Author's `draft_r3.py` run: +1,009 per role, +432 per specialist; blocks 2,026 B and 928 B. Appendix A extracted by my own regex is byte-identical to the script's strings (role block and specialist block both True). D4 generated entrypoint 14,454 + 1,009 = 15,463 B, 745 B under 16,208 B. T1/T7/T8 roots are `software-implementation`. Other roles' dist would be 16,382 B (`numerical-algorithm-design`) and 17,547 B (`software-design`), not backstop routes. |
| m-3 "no realized results" | **Repaired, no drift.** | Frozen exemption wording (workplan lines 511, 627, 919): "evidently produced, ran and reviewed no realized results and prepared no gate evidence". Block (role and specialist), CD-2 and §5 row E1c use it. CD-2's paraphrase "no realized results produced, run or reviewed" is equivalent. No residual "no results" in the four subjects. |
| G-3 A2 scope and symmetry | **Repaired in text; realizability gaps G-R3-2, G-R3-3.** | See below. |
| G-4 "Same delegated work" | **Repaired; consistent.** | See below. |
| G-5 reading-rule exclusion | **Repaired in part; new gap G-R3-1.** | See below. |
| m-1 stakeholder note | **Repaired; two accuracy points (m-R3-4).** | See below. |
| m-2 CD-5 | **Repaired, accurate.** | See below. |
| m-5 §8 | **Repaired; sound; wording points (m-R3-3).** | See below. |
| m-6 overlay citation | **Repaired, accurate.** | See below. |
| m-7 scoring reading | **Repaired; one overclaim (m-R3-1).** | See below. |

### G-3 detail

- **OMP shows the server `instructions` to the model: confirmed from code.** `adapters/omp.py` line 2743-2748 reads `instructions` from the MCP initialize result and records an error ("runtime system prompt does not end with the connected MCP server's instructions") unless the first-request system prompt ends with it. A missing string is also an error ("no MCP initialize instructions were observed on the bridge"). The probe run `C042-p70ck-r1` has `observation_errors: []`, so in an admitted run the system prompt did end with it. The probe artifacts do not retain the literal prompt text (hash-only), so the visibility rests on the adapter's pass condition, not on a captured string.
- **"Present but neutral" is correct.** An absent string fails the adapter. An empty string would technically pass `endswith("")`, but it would make the append-contamination check vacuous. A non-empty neutral string is the right rule. I did not run OMP to see whether OMP appends an empty string at all.
- **Symmetric clause, sibling descriptions, tool-name prefix, launching prompt:** all in A2 item 1 and in design §6/§7. The mediator's descriptions ("qualification-owned issue stand-in" at lines 43-53) and the `instructions` f-string (line 250) are mediator-local and fixable in D4.
- **Tool-name prefix:** `mcp__ssdp_delegate` comes from the pinned name `ssdp70` (digits dropped by `_mint_component`). See G-R3-2 for what pins it.

### G-4 detail

- **A3 ordering.** Timing (launching instruction, or a message before the return), then *Same delegated work* (every call to a case's fixture delegate within an episode, whatever its instruction; several assignments predeclare distinct delegates), then *Follow-ups* (after the return, "that includes re-invoking it with a new instruction"), then *Scripted delegates*. The "different work = new delegation" sentence is gone and nothing else in the four subjects still says it.
- **Agreement with workplan §11.3.** *Request* counts "once per delegate part per episode", and the measure is "on any delegation in a §11.3 case" (line 948). With one delegated work per delegate, the counting is unchanged. *Owed gaps* ("including a part the instruction never asked") agrees. The probe's chained C042-r1 pattern (bare relay, then all four parts after the return) scores as follow-up-only, as the design counts.
- **Chained variant.** The workplan's chained delegated-judgment variant passes the conclusion through a second delegate inside the first delegate's frozen return, not through a second tool call. A2 item 3 agrees. The existing corpus has one fixture delegate per case, so no existing case is affected.
- **Residual.** The timing clause "a message … sent before it returns" has a same-turn parallel-call edge (m-R3-1).

### G-5 detail

- The quoted clause is verbatim at contract line 145: "Every earlier campaign of this candidate and of earlier Protocol 7 candidates under this workplan is disclosed, whatever its outcome." The contract file's sha256 is unchanged (c08a3e65…) and git shows no modification.
- Other contract uses of "Protocol 7" / "Protocol 7 candidate" are lines 10, 17, 173, 199-203. Under the reading rule they mean 7.1.0, which is the intended reading for run-before, fixture-blindness and byte-reporting clauses. The exclusion touches only item 12's clause. Line 84 ("every earlier failed campaign of the profile lineage") does not use the phrase and is unaffected.
- The *Development data* sentence ("The 7.0 Stage 7 campaign is disclosed in the report … whatever its outcome; the probes and the gate are reported as development data") does not over-claim: the Stage 7 campaign is a campaign "under this workplan". It does not under-claim the clause: the gate "enters no campaign count" (amendment §3) yet is still reported. See m-R3-5.
- "The 6.6 route probes" is correct (workplan line 962). The sentinel sentence is G-R3-1.

### m-1 detail

- `diff` against the R2 copy shows only one appended section (`41a42,51`). No quoted stakeholder word changed.
- Contract §7 cites `STAKEHOLDER-DECISION-2026-09-28-PROTOCOL-7.0-SINGLE-PARTICIPANT-HUMAN-TRIAL.md` (line 242). Contract §1 item 9 cites `…NON-EXECUTOR-CUSTODY-AUDIT.md` (line 48). Both are named "Protocol 7.0" and bind through unchanged text, as the note says.
- The Option 1 admission (2026-10-04) concerns the 7.0 Stage 7 campaign's claim-scoped inadmissibility and blind scoring authorization, and the Option A closeout is the 7.0 NON-QUALIFIED determination (Candidate 7.0 FAIL). The note's "campaign-specific" characterization is accurate. See m-R3-4 for the two accuracy points.

### m-2 detail

- (a) "keeping each qualifier inside its question" is 44 B (the note says "about 45 B"), and it rests only on OD-3's "in each question".
- (b) Element 3 (workplan line 586) and §11.3 *Request* ask for "what it searched, could not reach and found" without launched-work coverage. Owner §6.3.11 *Form* supports it for "those returns". The statement is accurate.
- (c) "(or none)": element 3 has "found" only. Accurate.
- The new Tensions parenthetical and the Variants lineage phrase are label-table content and therefore not in the (a)-(c) list. That is correct.

### m-6 detail

- `PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-D3-REV8-AND-CONTRACT-REV14-2026-10-04.md` verdict 1: "D3 revision 8 as D3: PASS". Verdict 2 there is a NO-PASS on contract revision 14, which the overlay does not cite.
- `…-CONTRACT-REV15-2026-10-04.md` verdict 1 is contract revision 15 PASS and verdict 2 is the D3 revision 8 consistency PASS. The overlay's numbering is right. The design and amendment headers also cite "verdict 1" for the contract's own PASS, which is right.

### m-7 detail

The three places (design CD-6, A3 *Basis*, overlay §0.1) agree that A3 is the scoring reading and the block wording is the stricter instruction. The one overclaim is "cannot diverge" (m-R3-1).

## Collateral

- **Stale figures.** In the four subject files, 837, 423, 15,291, 917, 1,854 and "revision 2" appear only inside explicitly historical contexts: the §12 map (flagged as revision 2 in §13), the "(revision 2: …)" parentheticals in Appendix A and CD-5, and revision-history headers. The overlay has no stale figure (+1,009 / +432 / 15,463 / 745). Stale labels: §5 heading (m-R3-2) and the two narrow A2 phrases (G-R3-2).
- **Revision labels.** The design is rev 3, the amendment record rev 3, and the overlay says design rev 3 and record rev 3 throughout. The overlay header `design_review_state` and `implementation_handoff` say "delta check" and "not authorized". Consistent.
- **Repair maps.** Design §13 maps G-1 to G-5 and m-1 to m-7 completely and accurately, apart from the "172 B is the G-2 phrases" point in CD-5 (m-R3-2). Amendment §5.1 correctly lists only the findings against that record (G-3, G-4, G-5, m-7).
- **Thresholds and scope.** No threshold changed (the 100% delegate-request floor, 16,208 B limit, 1-per-12 bound are untouched). The A4 text and the merge rule are unchanged. The only scope movement is the A2 server-identity reach (G-R3-2) and the A1 reporting sentence (m-R3-5).
- **Whitespace.** `git diff --check` clean (exit 0). In the three new records, trailing spaces 0, tabs 0, files end in a single newline.

## Executed checks

| Command / check | Result |
|---|---|
| `git rev-parse HEAD`; `sha256sum` on the R2 record, 3 subjects, 3 R2 copies, supporting record, contract rev 15; `git status --short` | HEAD 6d09418; all hashes match the brief; contract file unmodified |
| `diff` of design, amendment record and stakeholder record against the `*-R2-HISTORICAL.md` copies | changed bytes enumerated; stakeholder record is one appended section only |
| `git diff` of the workplan versus the preserved R2 diff | changed lines only in the two header state fields, the 0.1 intro, records, second-review sentence, A1-A3 summaries, m-6 citation, strict-evidence line, reference measurement and status; nothing else |
| Recount of `scores.json` from `M07-CHECKLIST-20261004T151913Z` (strict and core, "follow-up" parts excluded); read of all p70ck annotations | 2/50 and 0/50 strict, 10 and 42 of 50 core; m-4 exceptions C044-r0 T, C048-r0 V confirmed |
| `python3 draft_r3.py` (my own output directory); own regex extraction of Appendix A from the design and comparison with the script's output files | +1,009 per role, +432 per specialist, blocks 2,026 B / 928 B; role and specialist Appendix A blocks byte-identical; dist 14,454 → 15,463 B, 745 B left |
| Read of workplan label table (lines 596-622), element 2/3 (585-586), §11.3 *Request*/*Owed gaps* (918-919), §14 (1123), 952/958, 171/185 | label rows, exemption wording, trigger quote and counting rule checked as cited |
| Read of `eval/adapters/omp.py` (lines 136-140, 360-415, 2595-2760) and `eval/stub_tools/mediator.py` (28-62, 236-262); grep of constants and `mcp__ssdp_` across `*.py` | system-prompt/`instructions` check; name minting; name/id pinning; 26 constant references; G-3, G-R3-2 |
| `summary.json` of `C042-p70ck-r1` (`observation_errors`, tools) and grep of its artifacts for the instruction string | `observation_errors: []`; string not retained in artifacts (hash-only) |
| Read of contract rev 15 lines 10, 17, 48, 84, 98-102, 145, 189, 242; grep of "Protocol 7"/"7.0 candidate"/"earlier" | clause verbatim; other uses unaffected; T2/T3 sentinel naming for G-R3-1 |
| Read of the stakeholder decision files (human trial, custody audit, Option 1, Option A) and of R1 design §10 | note statements checked (m-R3-4) |
| Read of the REV14 and REV15 package-access check verdicts | m-6 numbering correct |
| Read of `STAGE-7-M07-DELEGATE-REQUEST-AND-TREATMENT-DELIVERY-DIAGNOSIS-2026-10-04.md` §3 | "zero effective exposure" supports the m-5 reasoning |
| `git diff --check`; trailing-space/tab/EOF check of the three new records | clean |
| `python3 -m unittest discover -s tests -t .` (system Python 3.10) | **Ran 407 tests, OK (skipped=3)** |

## Not checked

- Whether OMP would append an empty `instructions` string, and whether renaming the MCP server changes any other adapter, profile or admission artifact beyond the references I listed. I counted references, not re-ran the adapter suites.
- The literal system prompt text from a real run (the probe artifacts keep only its hash).
- The Orchestrator Core snapshot, package build, committed-dist parity and frozen-resource integrity: no `source/` or `dist/` byte changed in this delta.
- Same-turn parallel tool-call behavior of OMP with GLM-5.3-Flash (the edge in m-R3-1) and OMP's actual handling of two calls to one delegate.
- Whether the per-element SD-B attribution of the 172 B revision 3 content passes the independent attribution check (CD-5 routes it to D4's independent check).
- Package builds for the D4 wording itself (the reference wording is non-binding; D4 does not yet exist).
- Stage 7 data and custody trees beyond the probe artifacts named above. I did not read, write or modify `/home/samjin/ssdp70-omp-stagef/` beyond read-only access to the checklist probe. No live run.

These verdicts accept no implementation and change no qualification determination: Protocol 7.0 remains NON-QUALIFIED. D4 authorization follows the overlay's status line. I recommend fixing G-R3-1 to G-R3-3 (a few lines each) before the contract merge and before D4 starts. A further full review is not needed; a reader of the merged contract text and design §7 can confirm those edits mechanically.
