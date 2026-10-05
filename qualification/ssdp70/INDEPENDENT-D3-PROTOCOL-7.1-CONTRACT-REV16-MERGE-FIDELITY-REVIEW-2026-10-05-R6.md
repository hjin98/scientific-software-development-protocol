---
kind: independent-contract-merge-fidelity-and-post-r5-delta-review
governing_protocol_version: 6.6.0
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e (plus the uncommitted subject bytes below)
reviewer: fresh independent context; authored no subject byte; not the author of reviews R1-R5
scope: (1) merge fidelity of contract revision 16 against the quoted blocks A1-A4 of amendment record revision 6; (2) the post-R5 repairs (G-R5-1, G-R5-2, m-R5-1..7) in design rev 6, the record, the stakeholder record and the overlay; (3) contract self-consistency after the merge
subjects:
  merged_contract: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md sha256 abc97a3e8eb0555ca933835b37f195825af40f68c83cd8ef9092d7ff96505cb9 (verified); HEAD blob (revision 15) sha256 c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920 (verified)
  amendment_record: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (record revision 6) sha256 6649e5ccd4957f34fd6d5228c9c068879fcbe8cb937da007589191a84cf46d29 (verified; the -PRE-R6-HISTORICAL copy has the identical hash)
  design: qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md (revision 6) sha256 5e827c5ce42104e5db4a4074b291a534ccdcb81bae91b6ca90a3996ab2823347 (verified; the -PRE-R6-HISTORICAL copy has the identical hash)
  stakeholder_record: qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md sha256 82cf623a190a36b0b678fde7d9e199972e08c700124eeb5d3626dc7d97dc5528 (verified; the -PRE-R6-HISTORICAL copy has the identical hash)
  overlay: workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md sha256 d4fefb3085eaa66bab1216f2a6266b19294d4e9183e92105051b0afae28b2058 (verified)
serious_challenge: none
merge_fidelity_verdict: PASS (A1, A2, A3, A4 are byte-identical to the record's quoted blocks after prefix removal and the stated re-indentation; the diff has exactly the seven expected hunks; placement and Markdown nesting are faithful; two cosmetic defects in the A3 pointer to fix before the commit, m-R6-1)
post_r5_record_deltas_verdict: PASS (G-R5-1, G-R5-2 and m-R5-1..7 are repaired in substance and every adapter fact checked is true; residual gaps G-R6-1 to G-R6-3 and minors below, none changes a threshold, frozen element or the A1-A4 byte content except as an optional new record revision)
stakeholder_record_fidelity: faithful. The effective-decision rows carry only the quoted choices; recorder content is labelled as the recorder's. Not verifiable by me: the dialogue itself (the first-exchange option text and the follow-up question), which the record now says it quotes from the session. Two attribution points remain (G-R6-3 and m-R6-6). The record authorizes neither the merge nor D4 and does not claim to.
authorization: this review authorizes neither a commit of the merged contract nor D4
---

# Independent merge-fidelity review R6: contract revision 16 and the post-R5 deltas

Governing SSDP version: 6.6.0. Applied: the `software-design` Independent Review and Challenge contract. All 7.x material is non-governing development data. The only stakeholder statements I credit are the words quoted in the stakeholder record (user answers "Decisions confirmed. Proceed.", "Proceed with OD-4.a.", "Switch to (b)", and the quoted option text). I read R5 in full first.

## Serious Challenge

None. The parent authority (SSDP 6.6.0, frozen workplan elements, contract revision 15) is coherent for this change. The merge changes no threshold, floor, exposure minimum, human trial, backstop or custody role.

## Blockers

None.

## Required edits before the contract is committed (cosmetic, no fidelity effect)

- **m-R6-1: the A3 pointer in the §3 row.** Contract line 229 now reads "…is separately counted as burden.Timing and follow-up rules (revision 16): see the paragraph below this table. |". There is no space after "burden." (the record's row text ended with "burden." and the pointer was concatenated). It renders as "burden.Timing". Also the caption at line 235 says the A3 text was "appended to the table row above", but the row is not above: it is the "Delegate-request conformity" row, six rows earlier. Say "appended to the §3 *Delegate-request conformity* row, which points here". Neither defect changes meaning.
- **Status line** (frontmatter) must be updated by whoever commits, once this review is accepted.

## Gaps (fix, or record a decision to accept, before D4; none blocks the commit of the merge)

### G-R6-1: the A1 reading rule, applied literally, rewrites two historical references to the non-qualified 7.0 candidate

The A1 reading rule says "7.0 candidate" (and "Protocol 7", "p70", "the candidate arm") denote the 7.1.0 candidate. Its only carve-out is the §1 item 12 earlier-campaign clause. Literal applications that read absurdly:

- Contract line 16 (A1's own first paragraph): "successor to the non-qualified 7.0 candidate (Option A closeout)" becomes "successor to the non-qualified 7.1.0 candidate".
- Contract line 18 (the rule's own exclusion sentence): "which includes the 7.0 candidate".
- Contract line 341 (§8 revision 16 paragraph): "The Protocol 7.0 candidate stays NON-QUALIFIED under the stakeholder's Option A closeout" contains the substring "7.0 candidate" and would assert that the 7.1.0 candidate is non-qualified.
- Contract line 257 (§4): "applies identically to the 6.5, 6.6 and 7.0 arms": "7.0 arms" is not in the rule's list, so it keeps "7.0", while the arm under test is the 7.1.0 candidate. Harmless.

The §8 historical paragraphs for revisions 1-15 contain none of the listed strings (grep over lines 326-338 and the revision 15 paragraph: no "7.0 candidate", "p70", "the Protocol 7 candidate"), so the rule does not rewrite them. The only literal hazards are lines 16, 18 and 341. Context makes each reading unambiguous to a human reader, so I judge them harmless in practice, but a contract's reading rule should not contradict its own text. Recommended repair (one clause in A1, then the merge text): "unless the text names it as the non-qualified or earlier candidate (Option A closeout)". Alternatively rewrite lines 16 and 341 as "non-qualified Protocol 7.0 candidate (Option A closeout)" with the rule scoped to the quoted tokens only. Either is a new record revision and a re-check of that clause only. If the author keeps the text, record the decision.

### G-R6-2: A2's residual wording has two small interpretive holes

- "every model-visible form of those pinned values" (item 1) is literal enough to cover mediator-authored text that embeds the server name or id (for example a tool description reading "the ssdp70 delegate"), while the same item says every tool description is neutral. The "other" in "every other model-visible identifier and text" resolves most cases, and the checker lists the observed set, but a case that sits in both lists has no stated winner. A clause such as "forms the adapter itself mints, verifies or parses; mediator-authored text may not embed the pinned values" would close it.
- The server id is a pinned value, and the `instructions` string is the only place the mediator embeds it (`mediator.py` line 250). Item 1 says the `instructions` "must not embed the server id", so the id is not model-visible after D4. That is consistent (specific over general), but the item still lists the server id among the residual's "pinned values". Harmless; one clarifying clause would remove the apparent overlap.

### G-R6-3: attribution of the whole A2 list to OD-4(b)

Contract A2 item 1 says "The following are not renamed or changed (stakeholder decision OD-4(b))" and then lists the server name, server id and store identity forms, the Claude-adapter prefix, any other observed form and the adapter-parsed wrapper keys. The stakeholder's words (record §4) are: keep the server name and disclose the `mcp__ssdp_` prefix "(and store identity)". The server id, the Claude prefix, "any other form the checker observes" and the wrapper keys are the recorder's reading (stakeholder record §4, first *Recorder's reading* bullet, labelled as such there). In the contract text the parenthetical attributes the full list to the stakeholder decision. The amendment §1 OD-4 line ("keep the adapter-pinned server identity") and design §0 use the same wider noun. This is the m-R5-3 issue in a new place; because the contract quote is byte-bound to the record, the fix is a record edit ("stakeholder decision OD-4(b), as read in stakeholder record §4") and a re-merge of that one parenthetical. Not an authority overstatement in effect (the reading is conservative, R5 judged it faithful), but it should say whose reading it is.

## Minor

- **m-R6-2: §8 cites a rule §8 does not state.** Contract line 341: "the changed candidate needs fresh blind qualification (this section's rule on candidate changes after exposure)". §8 states: "Any changed threshold or case after exposure is a governed contract change with affected requalification; a tuned holdout becomes development data" (line 328). That is about thresholds and cases, not candidate changes. The requirement itself is real (A1 *Successor subject*, *Fresh fixtures*, *Pre-run check*; item 12 *Requalifying the profile*), so reword to cite A1 and the §8 rule on changed cases.
- **m-R6-3: the revision 15 status correction is true but compresses.** Verified (below): revision 15 PASS is verdict 1 of the REV15 check; D3 revision 8 PASS is verdict 1 of the REV8 check; consistency is verdict 2 of the REV15 check; the bytes the REV15 check examined (commit `b8c706f`, file blob sha256 `c08a3e65…`) are the revision 15 bytes. "B-1 to B-9 are D4-stage conditions or tidy-ups" repeats the check's own sentence, but that check also lists B-2, B-3 and B-4 under "To confirm with the stakeholder"; the paragraph's declared effect (d) still says "neutral on outcome", which B-2 asks to reword. None of this is made worse by revision 16; say "B-2 to B-4 await stakeholder confirmation" if the paragraph is touched again.
- **m-R6-4: frontmatter `target_protocol_version: 7.0.0` (left deliberately).** Not a defect in itself: the reading rule governs "in this contract", and the file name and title keep the 7.0 identity. But a tool or reader that reads only the frontmatter gets 7.0.0, and nothing in the merged text says the value was deliberately left. One sentence in the §8 revision 16 paragraph ("the front-matter `target_protocol_version`, the title and the file name keep the 7.0.0 identity of the file; §1's reading rule governs the candidate") makes the choice explicit. Judged a minor gap, not a blocker.
- **m-R6-5: stakeholder record §4 last sentence of the *Correction* paragraph is stale.** "…if the corrected scope changes the stakeholder's choice, the stakeholder says so before D4 begins." The stakeholder did change the choice (the next paragraphs record it). Make it past tense or delete (R5 m-R5-1 asked for the "renamed" and "rename" repairs, which are done; this sentence is the remainder).
- **m-R6-6: design §1 parent table** still lists "Option B re-open and OD-1 to OD-3"; design §6 A2 bullet (line 167) still says "Two adapter-pinned identifiers, the tool prefix and the store identity" although §7, the record and the contract now define the residual by source (G-R5-2). Align both (no effect on the contract text).
- **m-R6-7: the `-PRE-R6-HISTORICAL` copies are byte-identical to the current files** (verified by hash), so they preserve nothing that differs. The R5-reviewed bytes (record `8174c3c3…`, design `5098dc0e…`, stakeholder record `6fcc77bb…`, overlay `d610aa14…`) were not preserved, so the post-R5 delta cannot be diffed exactly. I reconstructed it from R5's descriptions, the REV5 copies and fact checks. The label "PRE-R6" is misleading; either delete these copies or note that they equal revision 6. This weakens, but does not defeat, the post-R5 check.
- **m-R6-8: the merge record is not self-describing about placement and indentation.** The record's merge rule says only "byte-checked against this record". The A3 split (pointer in the row, text in the paragraph below the table) is documented only in the contract (caption at line 235 and the §8 paragraph). Add one sentence to the record's merge rule.
- **m-R6-9: titles name sections that carry no text delta.** The A1 heading names "§1 *Custody*/*Scope*, §8"; the A2 heading names "§6". No text is merged under those; A2's checker duty lives in A2 itself. No effect; mention for the next record revision.
- **m-R6-10: count provenance.** Design §7 gives the R4 count (103 hits, 11 Python files) and the author's and R5's (136, 138 across 14 files). My grep of the same kind of pattern over `eval/` gives 139 lines in 15 files (the extra file is `adapters/omp_eval.py`, one hit). The claim "14 files and over 100 references" is true as a lower bound; the exact figure depends on the pattern.
- **m-R6-11: overlay lacks the R5 outcome.** The overlay `design_review_state` and §0.1 record the R4 pass and "pending independent merge-fidelity check" but not the R5 PASS with gaps. Design §16 has it. A clause would make the overlay's review chain complete. Not a blocker.
- **m-R6-12: A1 "Fresh fixtures" sentence.** "Every custodian-authored blind item they disclosed is non-blind." "They" has no clear antecedent. Meaning is recoverable from the next sentence. Optional wording repair at the next record revision.
- **Process observation.** The stakeholder's option (b) text promised "an independent check before any merge". R5 passed the text, but the merged A2 contains the G-R5-2 repair that R5 did not see; this review is the check of the merged bytes. The merge is uncommitted, so the gate holds if the commit waits for this verdict.

## Verification by brief item

### A. Merge fidelity (primary)

Method. A script (scratchpad `fid.py`) extracts each quoted block from the record (contiguous lines starting with ">", prefix "> " or ">" removed), locates its first line in the contract, and compares line by line against the contract with the expected indentation added (A1, A2 +2 spaces, A3 +0, A4 +7 spaces for continuation lines; the first A4 line must be "- " plus the record's first line). Blank lines must be blank.

| Block | Record lines | Contract lines | Result |
|---|---|---|---|
| A1 (*Candidate*) | 50-60 (11 lines) | 16-26 | 0 mismatches; indentation exactly +2 |
| A2 (*Scope*) | 66-86 (21 lines) | 32-52 | 0 mismatches; item 1 text, sub-bullets and the closing checker sentence identical; indentation exactly +2 (list at +2, nested bullets at +5) |
| A3 | 99-107 (9 lines) | 237-245 | 0 mismatches; indentation +0 |
| A4 | 115-121 (7 lines) | 146-152 | 0 mismatches; first line "- Ordinary runs enter no other floor. Every critical-oracle outcome in them is listed in the report, by group:" |

- **Placement.**
  - A1: inside the *Candidate* bullet, after its first paragraph, before the *Comparator* bullet. As the record says ("Add to §1 *Candidate*").
  - A2: inside the *Scope* bullet, after its first paragraph, before "**Portable runner-admission contract.**". As the record says ("Add to §1 *Scope*").
  - A3: the record says "Append to the §3 *Delegate-request conformity* row". A table cell cannot hold the multi-paragraph text with a nested list. The merge puts a pointer sentence at the end of the row and the A3 text byte-identical in the paragraph directly below the table (line 235 caption, lines 237-245). I judge this faithful and unambiguous in substance: the row carries the pointer, the caption names the row, and §8 says "through the paragraph below the §3 table". The row's earlier text is preserved byte for byte up to its last sentence (checked: the new row begins with the old row minus the closing " |"). Defects: m-R6-1 (missing space; "row above").
  - A4: replaces exactly the old line 112 sentence ("Ordinary runs enter no other floor. Every critical failure in them is listed in the report, by group."); the removed line in the diff is that single line.
- **Markdown nesting** (rendered with `markdown_it`, CommonMark + tables, to a token tree).
  - A4: *Scoring scope* keeps its three bullets; the third bullet ("Ordinary runs…") owns a nested two-bullet list, then two paragraphs (the "Selection and activation…" sentence and the "No report total…" paragraph) at the same item level. The next sibling, "**Primary flash profile family…**", is intact at its original level; the *Scoring scope* list item structure (siblings: Run-type strata, Scoring scope, Primary flash profile family) is unchanged.
  - A2: ordered list 1-5 with nested bullet lists and continuation paragraphs, then the closing checker paragraph as part of the *Scope* item. A1: six paragraphs inside the *Candidate* item.
  - A3: a table, then paragraphs and a two-bullet list, then "**Comparative improvement.**" at top level.

### B. Nothing else changed

`git diff` has seven hunk groups (numstat +58/-4): (i) frontmatter `status` (line 5); (ii) A1 insertion after line 14; (iii) A2 insertion after line 19 of the old file; (iv) A4 line replacement (old line 112); (v) the A3 row edit (old line 189); (vi) the A3 paragraph insertion (after old line 194); (vii) the §8 changes: the revision 15 paragraph (a word diff shows only its final sentence "No independent check accepts the revision 15 bytes yet; a fresh check, together with fresh acceptance of the governing D3 decision and a Review of the workplan §0.1 entry, is required before any harness change, admission or run relies on them." replaced by the "Status corrected in revision 16: …" sentence, with the rest of the paragraph byte-identical) and the new revision 16 paragraph. The four removed lines are exactly: the old status line, the old A4 sentence line, the old table row, and the old revision 15 paragraph. No other hunk. Nothing else is modified among tracked files except the overlay; `PROTOCOL-RELEASE-STATE.yaml`, `source/`, `dist/`, `eval/` untouched.

The frontmatter `target_protocol_version: 7.0.0` left in place: see m-R6-4 (minor gap; not a blocker).

### C. §8 accuracy

- **Revision 15 correction: true.**
  - REV15 check (`PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-CONTRACT-REV15-2026-10-04.md`, "Verdicts"): "1. Contract revision 15, with the amendment record and the decision record: PASS. There are no blockers. B-1 to B-9 are conditions for the D4 stage or tidy-ups at the next touch." "2. Governing D3 revision 8 and the workplan §0.1 entry remain consistent with revision 15: PASS."
  - REV8 check (`…-D3-REV8-AND-CONTRACT-REV14-2026-10-04.md`, "Verdicts"): "1. D3 revision 8 as D3: PASS, with conditions B-3 to B-9 and the rehearsal-form additions for the D4 stage."
  - The REV15 check's subject is commit `b8c706f`; `git show b8c706f:…CONTRACT.md | sha256sum` = `c08a3e65…`, equal to the HEAD blob; the file's history shows `b8c706f` as the last commit touching it. So the bytes it passed are the revision 15 bytes.
  - Caveats: m-R6-3.
- **Revision 16 paragraph: accurate, no overclaim.**
  - It names the record revision 6 and deltas A1-A4; states that it follows Option B and OD-1 to OD-4; lists the four sections changed (matches the diff); says no floor/threshold/exposure/human-trial/backstop/custody change (confirmed: the diff touches none).
  - All five review files it names exist: `INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05.md` (design NO-PASS, contract NO-PASS), `-R2`, `-R3`, `-R4`, `-R5` (PASS each, with gaps), per their front matter.
  - It says "No independent check accepts these merged revision 16 bytes yet", which is true until this record.
  - "The Protocol 7.0 candidate stays NON-QUALIFIED under the stakeholder's Option A closeout" is faithful to `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-QUALIFICATION-CLOSEOUT.md` ("Go with Option A…", formal NON-QUALIFIED determination; Stage 7 closed NON-QUALIFIED). Literal-reading hazard: G-R6-1. The parenthetical rule citation: m-R6-2.

### D. Contract self-consistency after the merge

Searched the full contract (read §1 items 1-13, §3, §4, §6, §8; grepped "Protocol 7", "7.0", "p70", "earlier", "scripted", "stand-in", "panel", "pool", "T1", "route", "§11.5").

| Clause | Result |
|---|---|
| §1 item 12 earlier-campaign disclosure (line 185) | Consistent: A1's carve-out preserves its literal reach; the 7.0 Stage 7 campaign stays disclosed. |
| §1 item 12 deterministic stratum list ("T2/T3 sentinels, T4–T6, T1/T7/T8 and P01–P19 routing probes") and ordinary list (S01–S11/H01–H05) | Consistent with A1 *Preservation panels* (matched to baselines). A1's "6.6 route probes" is not a term the contract uses: closest are "P01–P19 routing probes" and "selection routes". Harmless (R2 G-5 already examined). |
| §3 *Delegate-request conformity* row ("a scripted compliant response cannot excuse an omitted request") | Consistent with A3: a follow-up supplies an answer (an owed gap) but does not satisfy a request part. |
| §3 "12 owed delegate request parts across the frozen silent/compliant/rename/compaction/chained/review cases" (line 213) | Consistent with A3 *Same delegated work* (a case needing several assignments predeclares a distinct delegate per assignment, so the count per delegate part stands). |
| §1 *Custody*, §8 ("This framework contains no concrete fixture/answer data") | A2 quotes case-class facts (a rename or compaction "with no run", "no accepted D1/D2 authority governs that dataset") that appear in workplan §11.3 (lines 913, 917, which the candidate author already authors) and the example `launches_work: false`, which I could not locate in the repository (it is custodian-held Stage 7 material). These are case-class descriptions, not keys or planted properties. Judged harmless. |
| §6 pre-run checker scope | No conflict. §6's list of what the checker "records" is not exhaustive; A2 adds its own checker duty ("items 1 to 4 through the exact adapter and profile, over the full item 1 scope"), and §6's "A missing branch… blocks runs" is compatible with A2's "voids the affected case". A2 is not mirrored in §6 (m-R6-9), which is a navigation gap only. |
| §1 item 8 / §6 "qualification-owned stand-in" | Not executor-visible, so not governed by A2's concealment clause. |
| §4 "6.5, 6.6 and 7.0 arms" | Literal "7.0" remains for the arm under test: G-R6-1 (harmless). |
| §1 item 12 *Scoring scope* vs A4 | Consistent; A4 broadens "critical failure" to "critical-oracle outcome" (stricter on reporting, no information removed) and its pooled-count carve-out names the pools §1 item 12 specifies (line 203 and the *Retained false-activation floors* bullet). |
| A1 reading rule against §8 history (revisions 1-15) | The history contains none of the rule's tokens; no absurd reading there. The literal hazards are lines 16, 18, 341 (G-R6-1). |

I found no clause that contradicts the merged text, and no instance where the merged A2 conflicts with §6.

### E. Post-R5 repairs

**E1. A2 item 1 "adapter-pinned residual" and item 5.**
- Self-consistent and honest: item 1's first sentence, the surface list, the pinned paragraph, the neutral list and the checker sentence agree with item 5's second paragraph (residual present in every delegate-case run of both arms; the observed set is disclosed; the uptake-claim caveat). Nothing is excused beyond the residual except the two interpretive holes in G-R6-2.
- Adapter facts verified by reading `qualification/ssdp70/eval/` (all true):
  - `OMP_MCP_SERVER_NAME = "ssdp70"`, `OMP_MCP_SERVER_ID` and `MCP_STORE_IDENTITY` constants at `adapters/omp.py` 134-148; `verify_mcp_binding` rejects another name, id and entrypoint (about 405-409).
  - `mint_mcp_tool_name` (366-380) derives `mcp__ssdp_<tool>` from `ssdp70`; `adapters/claude.py` 39-41 builds `mcp__ssdp70__`; the Claude adapter hard-codes the store identity (1351, 1366).
  - The adapter parses `details.serverName` of every MCP result (3730-3735), so a server name in result details is adapter-pinned: the item's "for example a server name in result details" is correct and covers R5's unestablished third form.
  - The adapter parses `returncode`, `evidence.store_identity`, `evidence.operation`, `evidence.object_ids`, `evidence.query` and the two `*_object_version` fields (3770-3835); item 1's "`returncode` and `evidence.*`" is a fair summary. The adapter also retains `stdout` and `stderr` as the return content, so "the other return-wrapper fields" is, in practice, close to an empty set; D4 enumerates it (design §7).
  - The system prompt must end with the connected server's `initialize` `instructions`, which must be a string (2735-2748): the "must stay present as a neutral string" statement is accurate; an empty string would satisfy the check.
  - The adapter compares each native tool's description and schema against the raw mediator tool live (2853-2854), not against a pinned constant, so neutral descriptions are realizable without an adapter constant change. `serverInfo.name` is read by no adapter (only `eval/test_mcp_stdio.py` line 70 asserts it).
  - The mediator embeds the server id only in `instructions` (line 250), so "the `instructions` must not embed the server id" is realizable.
- Realizable: yes, with the adapter-parsed keys and pinned forms excused, the mediator-local surface is neutralizable by D4 alone.
- Not established: whether OMP shows the model anything beyond the system prompt, tool catalog and tool results (for example `details.serverName`); A2 deliberately covers it by "any other form… that the checker observes". R5 recorded the same gap.

**E2. G-R5-1 (mediator digest bound into frozen OMP profiles).** Verified:
- `principal_files()` includes `"stub_tools/mediator.py"` (`omp.py` 440-451); `principal_files_sha256()` (460); `freeze_profile` writes it to `containment_policy.principal_files_sha256` (1058); `profile_errors` refuses a mismatching profile (937-938); each run records it (1520); `adapters/omp_eval.py` lines 261 and 712 do the same for the evaluator.
- `eval/profiles/omp-evaluator-readonly.json` lines 45-52 record `stub_tools/mediator.py` as `e51f0641…`; the committed mediator is `bf0070c0…`, so that profile is already stale (design §7 says this).
- The Claude adapter computes the mediator digest per run only (`claude.py` 188-232: `--expected-self-sha256`, `executable_sha256`) and no `principal_files_sha256` appears in it or in its profile template.
- Statements about "no adapter constant / profile / snapshot changes" (grep and read of design, record, stakeholder record, overlay for "no adapter", "adapter constant", "profile identity", "snapshot", "unaffected", "unchanged", "re-open", "re-freez", "renam"): every remaining occurrence is accurate: design §7 *Server identity* ("change no adapter source constant, **but they do change a bound digest**… re-frozen… evidence re-derived"), design §7 acceptance, §16; amendment OD-4(b) paragraph; stakeholder record §4 cost bullet; overlay header lines, §0.1 *Authority* bullet, *Status*, and the workplan line 723 marker. The remaining "re-open" hits are the option (a) description quoted from the dialogue, the overlay's description of option (a), design §9 triggers and §8 non-goals. Nothing is stale on this point.

**E3. m-R5-1..7.**
- m-R5-1: the "is renamed too" and "starts the rename" sentences are gone (grep "renam" over the four records: only option-(a) history, the quoted question, "not renamed", and "Renaming would change…" remain). Remainder: m-R6-5.
- m-R5-2: overlay line 723 says OD-4(b) and "because `principal_files()` binds the mediator digest into the frozen OMP profiles, those profiles are re-frozen".
- m-R5-3: the stakeholder record's effective-decision row for OD-4 now says only "Option (b) as presented: keep the server name and disclose the `mcp__ssdp_` prefix (and store identity) as a residual cue." The Claude prefix, the server id and the neutralization sit in a block titled "Recorder's reading and consequences, open to independent check (not stakeholder words)". The overlay header says "Recorder's consequences, not stakeholder words". Design §7 and the amendment say "chose not to rename", not "declined". Remainder: G-R6-3 (the contract parenthetical) and the amendment §1 noun.
- m-R5-4: count provenance now stated (R4: 103 hits in 11 Python files; author 136; R5 138); m-R6-10 for the pattern dependence.
- m-R5-5: amendment header `stakeholder_basis` and §1 include OD-3 and OD-4 (OD-4 states (b), first answered (a)). Design §1 parent table still says OD-1 to OD-3 (m-R6-6).
- m-R5-6: design §15 is collapsed to a heading and two sentences saying revision 5's text binds nothing.
- m-R5-7: the quoted-exchange source sentence is present (stakeholder record §4, last bullet).

**E4. Stakeholder fidelity.**
- Exact quotes present: "Proceed with OD-4.a." and the "Switch to (b)" description (one hit each in record §4; design §10 and the overlay header quote the first answer).
- The effective-decision row states only what the presented option (b) states. Recorder content is labelled as the recorder's reading, including the reading of "(and store identity)".
- The record's *Authority* bullet says "Switch to (b)" does not authorize the merge or D4, consistent with the presented option text ("then re-run an independent check before any merge").
- Nothing attributes to the stakeholder more than the quoted words, except G-R6-3 (contract parenthetical and the amendment's noun "server identity") which are scope extensions that the record itself labels as the recorder's reading.
- I cannot verify the dialogue beyond what it quotes.

### F. R5 invariants

- `git diff --check`: clean (exit 0). In the five subject files: 0 trailing-space lines, 0 tabs, each ends with exactly one newline.
- Design Appendix A is byte-identical to the R3 copy's Appendix A (also to the REV5 copy): 3,289 characters, identical.
- Measurement figures unchanged: "+1,009" and "+432" B, "15,463" and "16,208" B, "745 B", "14,454" appear in the current design as in the R3 copy (the extra counts are the revision 6 text restating them). CD-1 to CD-7 differ from the R3 copy only by the R3 repairs (m-R3-1 divergence wording, 163 B + 9 B attribution, the A2 de-cueing line).
- `python3 -m unittest discover -s tests -t .` (system Python 3.10): Ran 407 tests, OK (skipped=3).
- No threshold, frozen element, block wording or measurement changed in this delta.

## Executed checks

| Command / check | Result |
|---|---|
| `git rev-parse HEAD`; `sha256sum` of the five subjects and the HEAD contract blob; `git status --short`; `sha256sum` of the three `-PRE-R6-HISTORICAL` copies | HEAD 6d09418; all hashes match the brief; the three PRE-R6 copies equal the current files; only the contract and the overlay are modified among tracked files |
| Read R5 in full; read the amendment record, stakeholder record, design (header, §1, §6, §7, §10, §14-16, grep elsewhere), overlay delta | as above |
| `fid.py` (scratchpad): extract A1-A4 quoted blocks, compare to the contract with indentation | 0 mismatches in all four |
| `git diff -U0` hunks; `git diff --numstat`; word diff of the §8 revision 15 paragraph; row-prefix and paragraph-prefix checks | seven hunk groups, +58/-4; only the expected removed lines |
| `markdown_it` token trees of lines 14-56, 130-154, 215-247 | nesting correct in A1, A2, A4 and the A3 paragraph; surrounding *Scoring scope* bullets intact |
| Read REV15 check "Verdicts", REV8 check "Verdicts"; `git show b8c706f:…CONTRACT.md \| sha256sum`; `git log` of the contract | claims in the §8 correction true; bytes examined = c08a3e65… |
| Front-matter verdict grep of R1-R5; read the Option A closeout record | review file names and verdicts as stated; NON-QUALIFIED faithful |
| Grep and read of `eval/adapters/omp.py` (134-150, 360-415, 436-470, 930-940, 1058, 1520, 2735-2750, 2853, 3730-3835), `adapters/claude.py` (36-46, 177-232, 1351), `stub_tools/mediator.py` (13-17, 42-60, 85-110, 195-215, 245-252, 281), `profiles/omp-evaluator-readonly.json`, `profiles/*headless.template.json`, `omp_eval.py` grep | adapter facts in A2 and G-R5-1 true; descriptions compared live; `serverInfo` unused by adapters |
| Grep counts over `eval/` for the pinned strings | 139 lines in 15 files (pattern-dependent; ≥14 files and >100 lines is true) |
| Grep of "no adapter / unchanged / snapshot / unaffected / re-open / renam / declined / stakeholder chose" over design, record, stakeholder record, overlay delta, contract | no stale or overstated statement; remaining hits explained |
| Diff of the design against the R3 and REV5 copies; Appendix A comparison; figure counts | only the repairs described; Appendix A identical |
| `git diff --check`; whitespace/EOF script; `python3 -m unittest discover -s tests -t .` | clean; 407 tests OK, 3 skipped |

## Not checked

- What OMP shows the model beyond the system prompt, the tool catalog and tool results (whether `details.serverName` or any banner reaches the provider request); no OMP in the sandbox, no live run. A2's "any other form the checker observes" rests on this.
- The `eval/` unit, integration, rehearsal and admission suites (not run); whether any `eval/` test pins mediator text, descriptions or digests beyond the cases named above (`test_mcp_stdio.py` line 70).
- Whether the 2026-10-05 D3 addenda (`D3-PACKAGE-ACCESS-WINDOW-AND-REPLACEMENT-CLARIFICATION-2026-10-05.md`, `D3-PACKAGE-ACCESS-UNVERIFIED-PAIRING-FAIL-CLOSURE-2026-10-05.md`) or later D4 commits change the reading of contract revision 15; the §8 correction speaks only of the recorded 2026-10-04 PASS verdicts.
- The R5-reviewed bytes of the record, design, stakeholder record and overlay (not preserved); the post-R5 delta was reconstructed, not diffed (m-R6-7).
- The stakeholder dialogue itself; the exact text the user saw; whether the user saw the design file or a chat version.
- Whether the example `launches_work: false` matches a custodian-held Stage 7 fixture (custody trees not read).
- Orchestrator Core snapshot, package build, committed-dist parity and frozen-resource integrity (no `source/`, `dist/` or `eval/` byte changed).
- A real executor package and a captured delegate result against the A2 checker clause (the checker does not exist yet).
- Custody trees under `/home/samjin/ssdp70-omp-stagef/` (not read or modified).

## Verdict statement and what must change

- **Is the merged contract revision 16 faithful to the record?** PASS. The text of A1-A4 is byte-identical to the record's quoted blocks; the only deviation from "append to the row" for A3 is the documented, faithful pointer-plus-paragraph form; the diff contains nothing else.
- **Are the post-R5 record deltas acceptable?** PASS, with the gaps above.
- **Before the contract is committed:** fix m-R6-1 (space and caption) and update the front-matter status after this verdict is accepted. Recommended in the same pass because they touch the same bytes: G-R6-1 (reading-rule carve-out; needs a new record revision and a re-check of that clause only), G-R6-3 (attribution parenthetical), m-R6-2 (§8 rule citation), m-R6-4 (frontmatter sentence).
- **Before D4 begins:** decide G-R6-2 (residual wording holes) or record the acceptance; align design §1 and §6 (m-R6-6); remove or relabel the PRE-R6 copies (m-R6-7). D4 is not authorized by this review.

These verdicts accept no implementation and change no qualification determination: Protocol 7.0 remains NON-QUALIFIED. This review authorizes neither a commit of the merged contract nor D4.
