---
kind: independent-d3-and-qualification-contract-cumulative-delta-review
governing_protocol_version: 6.6.0
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e (plus the uncommitted subject bytes below)
reviewer: fresh independent context; did not author any subject byte; not the author of reviews R1-R4
scope: cumulative delta of design rev 6 / amendment record rev 6 / stakeholder record (§3 revised, §4 added) / overlay rev 8 against the R3-reviewed copies (`*-R3-HISTORICAL.md`, preserved overlay diff); the R3 and R4 repairs and the OD-4(b) rewrite
subjects:
  design: qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md (revision 6) sha256 5098dc0e378c7d448f3b606a9a9461f32d596c5b0df53687149415cfa578ffa4 (verified)
  contract_rev16: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md (record revision 6) sha256 8174c3c3dad16b385a4bb9d8bd8f887c87b2041fc5b3bbbf95737ddb9a546f54 (verified)
  overlay_rev8: workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md sha256 d610aa146e2ccb1f13ddd3446eac6ba8c64f94a0e2ac5980ef7688d311e007d9 (verified; scope = bytes differing from the R3-reviewed diff)
  supporting_record: qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-05-PROTOCOL-7.1-OPTION-B-REOPEN.md sha256 6fcc77bba3f822d50c66b05e1723f44b03a4b473486ed014e27767c649a9e211 (verified; fidelity checked, no verdict)
  unchanged_reference: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md revision 15 sha256 c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920 (verified unchanged; `git status`: only the workplan is modified among tracked files)
design_verdict: PASS (with gaps G-R5-1, G-R5-2 to fix before D4)
contract_rev16_verdict: PASS (A1, A3, A4 merge-ready as quoted; A2 merge-ready after one recommended sentence edit, G-R5-2; fix the record-side G-R5-1 in the same pass)
overlay_rev8_verdict: PASS (with G-R5-1 and m-R5-2 to correct)
stakeholder_record_fidelity: both quoted user answers ("Proceed with OD-4.a.", "Switch to (b)") and the quoted "Switch to (b)" option description are exact; the record does not authorize the contract merge or D4, and its readings are labelled as the recorder's. Not verifiable by me: the first-exchange option text and the follow-up question text (the brief does not quote them). Four labelling or staleness points (m-R5-1, m-R5-3, m-R5-7). No overstatement of the stakeholder's authority found.
---

# Independent Cumulative Delta Review R5: design rev 6, amendment record rev 6 (proposed contract revision 16), stakeholder record, overlay rev 8

Governing SSDP version: 6.6.0. Applied: the `software-design` Independent Review and Challenge contract. All 7.x material is non-governing development data. The only stakeholder statements I credit are the user's words as quoted in my brief: "Proceed with OD-4.a." and the selection of "Switch to (b)" with the option description quoted there. I judged every record's statement about the stakeholder against those words, not against what the records say about themselves.

Scope: the cumulative delta against the R3-reviewed copies (`diff` of each subject against its `*-R3-HISTORICAL.md` copy; the current overlay diff against the preserved R3 overlay diff), plus the author's intermediate copies (rev 4, rev 5) to see what the (b) rewrite changed.

## Serious Challenge

None. The parent authority (SSDP 6.6.0, the frozen workplan elements, contract rev 15) is coherent for this change, and the OD-4(b) rewrite does not touch any threshold, frozen element, block wording or measurement.

## Blockers

None.

## Gaps (fix before the contract merge and D4; not independently blocking)

### G-R5-1: the claim "no adapter constant, profile identity or snapshot changes" is wrong for frozen profiles and their snapshots

- **Where the claim appears.**
  - Design §7 *Server identity* ("so these edits change no adapter constant, profile identity or snapshot") and the §7 acceptance bullet ("adapter constants, profile identity and snapshots unchanged"); §16.
  - Amendment OD-4(b) paragraph ("no adapter constant, profile identity or snapshot changes").
  - Overlay §0.1 (the third-review bullet and the *Status* bullet).
- **What the code does.**
  - `eval/adapters/omp.py` lines 440-463: `principal_files()` includes `"stub_tools/mediator.py"`, and `principal_files_sha256()` hashes it.
  - `freeze_profile` (line 1058) writes that digest into the frozen profile's `containment_policy.principal_files_sha256`. `profile_errors` (line 937) refuses to run a profile whose frozen digest differs from the current mediator ("frozen principal-file digests do not match the adapter's principal code").
  - Line 1520 and 1534: each run's containment realization records `principal_files_sha256` and `mediator_executable_sha256`.
  - Custody evidence: `~/ssdp70-omp-stagef/probes/DETERMINISTIC-ACTIVATION-20261004T140929Z/runs/C042-p70-r0/profile-snapshot.json` line 51 records `"stub_tools/mediator.py": "e51f0641…"`. The repository's `eval/profiles/omp-evaluator-readonly.json` line 52 records the same digest.
  - The workplan itself says so (workplan line 724): "The mediator executable digest, server id, OMP runtime/build, adapter/normalizer digest and exact native tool set make this binding part of the execution-profile evidence."
- **What is true, and what is not.**
  - True: no adapter *source constant* changes (OMP_MCP_SERVER_NAME/ID, MCP_STORE_IDENTITY stay), and `execution_support_sha256` (adapter, template, core, harness, ledger, premise) is unaffected. The per-run `--expected-self-sha256` and `mediator_executable_sha256` are computed per run (`omp.py` 1534, 1805, 2057), as the design says.
  - False: a frozen profile and its snapshot record the mediator's digest. Editing `mediator.py` makes every previously frozen OMP profile fail `profile_errors` until it is re-frozen, and the new profile snapshot differs. The Claude adapter is different: `claude-headless.template.json` records no mediator digest, and `adapters/claude.py` 191-232 computes it per run.
- **Pre-existing observation.** The committed mediator (`bf0070c0…`, commit 46ea4a0, which added `--disabled-tool`) already differs from the digest in the committed evaluator profile and in every Stage F and Stage 7 record (`e51f0641…`, commit 303ead0). The `profiles/omp-evaluator-readonly.json` in the repository is therefore already stale against HEAD, independent of this change.
- **Consequence.** The (b) cost is slightly larger than the records say: OMP profiles are re-frozen with the new mediator digest, and admission and rehearsal evidence is re-derived for it. A new campaign needs fresh frozen profile keys anyway (A1 *Pre-run check*), so the added cost is small, and (b) is still far cheaper than the rename. The design's other statement stands and is accurate: admission and rehearsal evidence recorded against old mediator bytes is not reused.
- **Repair.** Replace the sentence with: "no adapter source constant changes; each OMP profile is re-frozen with the new mediator digest (`containment_policy.principal_files_sha256`), and admission and rehearsal evidence is re-derived for the changed bytes." Apply it in design §7 (both places) and §16, the amendment OD-4(b) paragraph, and overlay §0.1 and *Status*.
- **Severity.** The A1-A4 contract text does not contain the claim, and no decision depends on it. It is a factual misstatement in four records, one of them the governing workplan overlay. I treat it as a gap, not a blocker.

### G-R5-2: A2's exception names two forms; realizability of "exactly two pinned identifiers" is asserted, not established

- **The text.** A2 item 1: "Except for the two adapter-pinned identifiers named at the end of this item … The reviewed adapter and frozen profile pin two model-visible identifiers: the tool-name prefix … and the store identity …". The checker "confirms that nothing outside them states or implies a delegate's status".
- **What the adapter pins beyond those two forms.**
  - The server name `ssdp70` itself, in forms other than the tool-name prefix. The retained trace of run `C068-p70-r0` carries `details.serverName: "ssdp70"` in every MCP tool-result event (`trace.jsonl`). Provider request bodies are not retained (hash-only), so I could not establish whether OMP shows that field to the model. If it does, the name appears outside the two named forms, is adapter-pinned (`omp.py` 3735), and A2 as written has no exemption for it.
  - The return-wrapper structure. `omp.py` 3760-3800 requires `returncode`, `evidence` and its keys `store_identity`, `operation`, `object_ids`, `query` and the two `*_object_version` fields. These are model-visible (the full JSON is the tool-result text, confirmed in the trace). A2 item 1 and design §7 say "return-wrapper fields other than the store identity" are neutralized, and overlay line 723 says the mediator's "return-wrapper fields" change in D4; the adapter forbids changing the keys the adapter parses. In substance these keys state no governance status, so nothing needs changing, but the text tells D4 to neutralize something it cannot change, and a strict checker could treat `evidence` and `operation` as qualification cues.
- **Failure scenario.** After the merge, the D4 pre-run check observes a third pinned form (or a wrapper key the checker judges to be a cue). The contract excuses only two forms, the case is voided, and the adapter-pinned form cannot be repaired without the re-opening that the stakeholder declined. The contract would then need another amendment.
- **Repair (one sentence, in A2 item 1 and item 5, and the matching lines in design §6/§7):** define the exception by source rather than by an enumerated pair of forms: "the adapter-pinned server name, server id and store identity and every model-visible form derived from them (including the tool-name prefix), as listed by the checker; the wrapper keys the adapter parses stay and are not status cues". The disclosure in item 5 then names "the observed set". The checker still lists and bounds the set. Keeping the exact two forms is acceptable only if the author accepts the rework scenario above.

## Minor

- **m-R5-1: stale text in stakeholder record §4.**
  - The *Correction of the presented cost* paragraph still says "the store identity returned in every tool result is renamed too (design §7 *Server identity*)". Design §7 now says it is not renamed. The sentence describes the scope of option (a), but its cross-reference is wrong. Say "would be renamed".
  - The same paragraph ends "…the stakeholder says so before D4 starts the rename". No rename is planned after (b). Delete it or reword it ("before D4 starts").
  - The paragraph also sits before the "first answered" line it says is "below". Reordering is optional.
- **m-R5-2: overlay line 723 marker carries a stale label (R4 m-R4-4 repair).** It reads "contract A2 and stakeholder decision OD-4(a) change the mediator's … (the adapter-pinned … are kept and disclosed, OD-4(b))". It should say OD-4(b) or "OD-4". See also G-R5-2 on "return-wrapper fields".
- **m-R5-3: recorder content not labelled as such, and a motive attributed to the stakeholder.**
  - The stakeholder record's effective-decision row states, unflagged, the Claude-adapter prefix (`mcp__ssdp70__`), the server id as part of what is "not renamed", and "Every other model-visible identifier and text … is neutralized in D4". The user's presented words named only the `mcp__ssdp_` prefix, the "server name" and "(and store identity)". The extensions are natural (the follow-up question's own scope list included the Claude adapter, and both adapters pin `ssdp70`) and the *Recorder's reading* bullets do flag the neutralization reading, but the row itself reads as the stakeholder's decision. Mark those three items as the recorder's reading, or say "per the recorder's reading below".
  - Likewise the overlay header's "STAKEHOLDER DECISION (2026-10-05, OD-4)" line ends with "mediator-local text is neutralized in D4", attributing the neutralization to the stakeholder.
  - Design §7 and amendment rationale say the prefix and store identity cannot be neutralized without re-opening admission, "which the stakeholder declined". The user selected (b); a motive of declining the cost is the recorder's inference. Say "chose not to rename (b)".
- **m-R5-4: attribution of the scope figure.** Design §7 says the 14 files and over 100 references were "measured at the R4 review". R4 reported 103 hits in 11 files and called its figure an order-of-magnitude statement. The 14-file figure is correct by my grep (below), but it is not R4's. Say "measured after the R4 review, by grep over `eval/`", or cite the pattern.
- **m-R5-5: amendment header and §1 do not mention OD-3 and OD-4.** `stakeholder_basis` says "(Option B; OD-1 to OD-3 confirmed)" and §1 lists OD-1 and OD-2 only, although A2 now cites OD-4(b). The OD-4(b) paragraph carries it. One clause in the header closes it.
- **m-R5-6: design §15 is kept as history and says the rename "is in scope".** The heading says "superseded by §16", which is enough for a careful reader, and §16 and §14 say so. A D4 implementer reading §15 alone would get the wrong scope. I would collapse §15 to its heading plus one line. Not a merge or D4 blocker.
- **m-R5-7: "verbatim" for the first exchange.** The record's header says wording is "quoted verbatim", and §4 gives the first presented options (a) and (b) and the follow-up question as verbatim. I could verify only what my brief quotes. Those texts are not in the preserved rev 4 design §10 (which words the options differently and does not contain "about 26 references"), so they come from the session's question dialogue. Say so in the record (source: the session's question tool), so a reader knows where the quotation comes from. This is a provenance statement, not a correction.
- **m-R5-8 (observation, no action needed in this delta): no checker for the "pinned set".** Design §7 acceptance asks for an independent check that the observed pinned set is exactly the residual. Nothing exists yet to run; G-R5-2 is the realizability risk of that check.

## Verification by brief item

### 1. Stakeholder fidelity (most important)

- **Quotes.**
  - "Proceed with OD-4.a." appears exactly in record §4 (once), design §10, overlay header and §0.1.
  - The option description for "Switch to (b)" in record §4 is byte-identical to the brief (grep of the full sentence: 1 hit): "Keep the server name and disclose the mcp__ssdp_ prefix (and store identity) as a residual cue. I rewrite A2 item 1, design §7 and §10 and the stakeholder record accordingly, then re-run an independent check before any merge."
  - The other two option labels ("Keep (a); merge the contract", "Hold; decide later") match the brief.
  - The follow-up question text and the first-exchange option text: not verifiable by me (m-R5-7). The figures in the follow-up (14 files, 100+ references; Claude adapter, profile templates and capability files, test/probe files, store identity) agree with the brief's summary and with my grep.
- **Correction of the presented cost.** Accurate: "about 26" was a three-file count (R3 and the rev 4 design); by my grep the real scope is 14 files and 138 lines (below). It says the answer "was given on the lower figure" and "stays recorded as given". The two stale sentences are m-R5-1.
- **Effective-decision table versus option (b) as presented.** Consistent: not renamed; prefix and store identity disclosed as residual; present in every delegate-case run of both arms. Three recorder extensions are in the row without a label (m-R5-3).
- **Recorder's readings.** Labelled "Recorder's reading, open to independent check". Bullet 2 states that "Switch to (b)" "does not authorize the contract merge or D4", which is consistent with the presented option ("re-run an independent check before any merge"). The overlay says "D4 itself still not authorized"; design §7 and §10 say the same.
- **"(and store identity)".** The record reads it as the store identity that the adapter pins and the mediator returns in every tool result (`omp.py` 3773, `mediator.py` `STORE_IDENTITY`), not as a license for other cues. I judge this a faithful and conservative reading, and not an overreach.
  - It matches the follow-up question, whose own scope list named "the store identity returned in every tool result" as part of what the rename would have touched, so the residual that (b) keeps is exactly that string.
  - It excuses the least that the presented words allow. The only alternative reading that conflicts with the presented words is a wider excuse ("keep the whole server name, including mediator-local `serverInfo.name`"). The record's narrower reading costs D4 a small mediator edit, which A2 already required before OD-4.
  - One point for the reader: "the server name" in the presented option is read as the adapter-pinned `ssdp70`; the mediator-local `serverInfo.name` (`ssdp70-qualification`) is a different string that D4 neutralizes. The record says this only implicitly (its list names the `serverInfo` name). One clause would make it explicit; not required.
- **Verdict:** no statement goes beyond the quoted words except as labelled recorder reading (m-R5-3 asks for the three unlabelled items).

### 2. Cost-scope facts (own grep over `qualification/ssdp70/eval/`, `__pycache__` excluded)

Pattern: `ssdp70-qualification-stdio-v1|ssdp70-private-issue-standin|mcp__ssdp|OMP_MCP_SERVER_NAME|OMP_MCP_SERVER_ID|MCP_STORE_IDENTITY|"ssdp70"`, plus the Claude adapter's `MCP_SERVER_*`.

| File | Hits |
|---|---|
| `adapters/omp.py` | 25 |
| `adapters/claude.py` | 4 (plus 6 with the `MCP_SERVER_*` names) |
| `stub_tools/mediator.py` | 2 (plus `SERVER_NAME`, `SERVER_ID`, `STORE_IDENTITY`: 6 with names) |
| `test_omp_integration.py` | 26 |
| `test_omp_units.py` | 8 |
| `test_stage_f_integrity_repairs.py` | 15 |
| `test_mcp_stdio.py` | 2 |
| `test_stage_f_v4_repairs.py` | 2 |
| `live_verify_v4.py` | 2 |
| `profiles/omp-headless.template.json` | 14 |
| `profiles/claude-headless.template.json` | 20 |
| `capabilities/omp-headless.json` | 6 |
| `capabilities/claude-headless.json` | 6 |
| `omp-build-inventory-18.0.11.json` | 6 |

That is 14 files and 138 lines (155 with the constant names and the observer id, which is not the server id and is excluded). The claim "14 files, over 100 references" is fair. The four "more test/probe files" are `test_mcp_stdio.py`, `test_stage_f_integrity_repairs.py`, `test_stage_f_v4_repairs.py` and `live_verify_v4.py`. "Frozen profile templates and capability files" are committed templates and manifests; the truly frozen snapshots are the per-run custody copies.

What the adapter pins and what is mediator-local:
- **(a) Store identity.** `omp.py` 3773-3774 rejects any `evidence.store_identity` other than `MCP_STORE_IDENTITY`, while `mediator.py` 17 and 101 hold and return it. The Claude adapter hard-codes the same string (`claude.py` 1351, 1366). Pinned by the adapter, and returned in every tool result (confirmed in a retained trace: 140 occurrences in one run).
- **(b) `serverInfo` name.** `mediator.py` 13 and 249 (`SERVER_NAME = "ssdp70-qualification"`). No adapter reads it. The only consumer is the literal asserted in `test_mcp_stdio.py` 70, which D4 would update. Mediator-local, as the design says.
- **(c) `instructions` f-string.** `mediator.py` 250 embeds `self.server_id`. Mediator-local; the adapter requires only that the system prompt end with the string (`omp.py` 2743-2748). Removing the id from it is possible.
- **(d) Mediator digest.** Computed per run and passed as `--expected-self-sha256` (`omp.py` 1805, `claude.py` 215); `mediator_executable_sha256` recorded per run (1534, 2057). That is as the design says. **But the digest is also frozen in the profile** (`principal_files_sha256`; G-R5-1). The Claude adapter, by contrast, records it per run only.
- **Server id.** `OMP_MCP_SERVER_ID` is pinned by `verify_mcp_binding` (`omp.py` 407) and by the mediator's `--server-id` check (`mediator.py` 281). Where it is model-visible is only the `instructions` f-string (c).
- **Tool prefix.** `mint_mcp_tool_name` (`omp.py` 366-380) derives `mcp__ssdp_<tool>` from the pinned name; `claude.py` 41 builds `mcp__ssdp70__`. A retained model trace (`C068-p70-r0`) shows the model reading the tool description "Call one scripted qualification delegate." and reasoning about a scripted delegate, which supports the design's account of the cue.

### 3. Amendment A2 items 1 and 5 as they would merge

- **Self-consistency.** Item 1's first sentence, the surface list, the pinned-identifier paragraph and item 5's second paragraph agree: the two named identifiers are excused from the status ban only; "Nothing may pre-state or summarize a delegate's return" is not excused; every other identifier and text, including the `instructions` (without the server id), `serverInfo` name, tool descriptions and other wrapper fields, is neutral. Nothing else is excused. Items 2-4 are unchanged and still hold.
- **Verbatim owner quote.** `source/shared/references/scientific-inspectability-and-initiative.md` line 224: "**Request.** Delegates may not be governed by SSDP." The amendment now reads "Delegates may not be governed by SSDP" (R4 G-R4-1 repaired). The same sentence is in the committed `dist/skills/*/references/` copies the executor package ships.
- **Fixture-delegate clause.** "The clause concerns the case's fixture delegate: generic doctrine in the executor package … is not a status statement about it." It narrows no enumerated surface item; every case-specific cue stays banned.
- **Symmetric clause.** Kept ("either way", "is, or is not, SSDP governed").
- **Checker clause.** Realizable through the exact adapter for the system prompt, tool catalog and a captured tool result (the adapter observes the first-request system prompt and `initialize` instructions; the trace retains tool results). The realizability of "exactly two pinned identifiers" is G-R5-2.
- **Honest disclosure.** Item 5 says the prefix can imply a governed delegate and the store identity can imply a stand-in store, that both are present in every delegate-case run of both arms, that the report discloses the observed set, and that comparative uptake claims carry the caveat. I judge that honest and sufficient.
- **Conditional, alternative or rename-as-decided text.** Grep of "OD-4", "rename", "alternative", "open decision", "26 references", "if the stakeholder" over the four subjects: no conditional or alternative text remains. Remaining hits are intentional: historical labels (`REV5-OD4A-HISTORICAL`, record revision history), the quoted first-exchange options in the stakeholder record, the design §10 and §15/§16 history, and the corrected "about 26" figure (stakeholder record §4, design §7 and §10, overlay §0.1), each as the corrected figure only. The overlay line 723 marker's "OD-4(a)" is m-R5-2. Design §15 as history: m-R5-6.

### 4. Design consistency and the R4 repairs

| R4 item | Result |
|---|---|
| G-R4-1 owner quote | Repaired (amendment A2 item 1, verified against line 224 and dist) |
| G-R4-2 §7 scope, store identity, Claude adapter | Repaired in substance (design §7 names the Claude adapter prefix, `MCP_STORE_IDENTITY`, `verify_mcp_binding`, `--server-id`). The scope is a count, not a grep-defined list; for (b) that is sufficient. "Measured at the R4 review" misattributes the figure (m-R5-4). |
| m-R4-1 companion line | Repaired ("amendment-record revision 6") |
| m-R4-2 §0 line; stakeholder title | Repaired (design §0 lists OD-4(b); title "OD-1 to OD-4") |
| m-R4-3 quotes honest; recorder extensions flagged | Partly: readings are flagged below the table; three extensions in the row are not (m-R5-3); provenance of the first-exchange quotes is not stated (m-R5-7) |
| m-R4-4 line-723 marker | Present and accurate except the stale "OD-4(a)" label (m-R5-2) |
| m-R4-5 hygiene sentinel label | Repaired and matches workplan line 1002 ("a repository-hygiene sentinel with costly or non-deterministic realized results") |

Other design checks: §6 A2 summary, §7 mediator bullet and *Server identity*, §7 acceptance, §10, §14 row, §15/§16 and CD-7 agree with the amendment and overlay except for G-R5-1 and the "return-wrapper fields" point (G-R5-2). The overlay header lines, §0.1 text and *Status* carry revision 6 for both design and record.

### 5. R3 items and invariants

- **G-R3-1 sentinel text, G-R3-3 fixture-delegate clause, m-R3-1..5:** all still present as repaired by R4.
- **Unchanged:** Appendix A is byte-identical to the R3-reviewed design (`diff` of the section: identical); CD-1 to CD-7 differ from R3 only by the m-R3-1 wording and the CD-7 de-cueing line; the +1,009 B per role and +432 B per specialist figures, 15,463 B against 16,208 B (745 B left) and the committed `dist/skills/software-implementation/SKILL.md` at 14,454 B all agree. No threshold, frozen element, block wording or measurement changed.
- **Revision labels:** design rev 6, amendment record rev 6, overlay "revision 6" for both throughout; the preserved sha256 prefixes in the headers (design rev 3 `4e0f9de5`, rev 4 `2e217cd4`, rev 5 `dc018e1b`; amendment rev 3 `138b7262`, rev 4 `c6e14dba`, rev 5 `43ed340d`) match the preserved files.
- **"26 references":** appears only as the corrected figure.

### 6. Collateral

`git diff --check` clean (exit 0). In the three subject records: 0 trailing spaces, 0 tabs, each file ends with a single newline. Only the workplan is modified among tracked files; nothing under `PROTOCOL-RELEASE-STATE.yaml`, `source/`, `dist/` or `eval/` changed; contract rev 15 hash unchanged. `python3 -m unittest discover -s tests -t .` (system Python 3.10): Ran 407 tests, OK (skipped=3).

### 7. Merge readiness of A1-A4 as contract revision 16

- **A1, A3, A4** (quoted blocks of record rev 6): merge-ready as quoted.
- **A2:** merge-ready after one recommended edit, G-R5-2 (define the exception by source, not by two enumerated forms). If the author keeps the two forms, record that decision and the rework scenario.
- **Same pass, record side (not contract text):** fix G-R5-1 in the amendment OD-4(b) paragraph, design §7/§16 and overlay §0.1/*Status*; m-R5-1, m-R5-2, m-R5-3 and m-R5-5 are one-clause edits. None changes A1-A4.
- The merge itself, its byte-fidelity check against the record, and D4 remain unauthorized by this review.

## Executed checks

| Command / check | Result |
|---|---|
| `git rev-parse HEAD`; `sha256sum` on the three subjects, overlay, contract rev 15 and all `*-HISTORICAL` copies; `git status --short` | HEAD 6d09418; every hash matches the brief; preserved-copy prefixes match the header claims; only the workplan modified among tracked files |
| `diff` of design, amendment and stakeholder record against the R3 and rev 4/rev 5 copies; current overlay `git diff` against the preserved R3 overlay diff | changed bytes enumerated; overlay changes confined to header state fields, the OD-4 decision line, §0.1 labels, authority bullet's review chain, evidence/status lines and the line-723 marker |
| `diff` of design Appendix A against the R3 copy | identical |
| `grep -c` of the quoted "Switch to (b)" description, labels and "Proceed with OD-4.a." in the stakeholder record | 1 hit each, exact |
| `grep` of "OD-4", "rename", "alternative", "open decision", "26 references" over the four subjects | no conditional/alternative text; hits explained above |
| `grep -rIc` over `eval/` for the server name, id, `mcp__ssdp`, store identity and constants; read of the match lines | 14 files, 138 lines (scope claim fair) |
| Read of `adapters/omp.py` 130-150, 360-415, 440-475, 895-945, 1026-1064, 1270-1280, 1485-1540, 2043-2060, 2740-2750, 3735-3800; `adapters/claude.py` grep; `stub_tools/mediator.py` whole file | pinning facts (a)-(d), principal-file digest binding, wrapper keys parsed by the adapter |
| Read of `eval/profiles/omp-evaluator-readonly.json` and a custody `profile-snapshot.json` (read-only); `git log`/`git show` of the mediator at its four commits | mediator digest frozen in profiles; `e51f0641…` (303ead0) versus HEAD `bf0070c0…` (46ea4a0) |
| Read of a retained trace (`C068-p70-r0/trace.jsonl`): `grep -o` for `ssdp*` and `mcp__*` strings | model reads the delegate tool description; `details.serverName`, store identity in every result |
| `grep` of owner source, `dist/skills/*/references`, workplan for "may not be governed"; workplan lines 584, 722-724, 1002 | owner quote verbatim and in dist; hygiene sentinel label; line-724 digest sentence |
| Trailing-space, tab, EOF check of the three records; `git diff --check` | clean |
| `python3 -m unittest discover -s tests -t .` | Ran 407 tests, OK (skipped=3) |

## Not checked

- What OMP shows the model beyond the `instructions` string, the tool catalog and the tool-result content: whether `details.serverName`, the server name or any runtime banner reaches the provider request. Provider request bodies are not retained (hash-only), I ran no OMP (none in the sandbox) and made no live run. G-R5-2 rests on this gap.
- The `eval/` unit, integration, rehearsal and admission suites: I counted references by grep and did not run them. I did not check whether any `eval/` test pins the mediator digest or the stale evaluator profile.
- The exact text of the first-exchange options and the follow-up question as the user saw them (m-R5-7), and whether the user saw the design file or a chat version.
- The generic-versus-case-specific boundary of the fixture-delegate clause against a real executor package (the checker does not exist yet).
- Same-turn parallel-call behavior of OMP (m-R3-1 edge), whether OMP appends an empty `instructions` string, and the SD-B per-element attribution of the 172 B (routed to D4's independent check).
- Orchestrator Core snapshot, package build, committed-dist parity and frozen-resource integrity: no `source/` or `dist/` byte changed in this delta.
- Custody trees beyond the read-only greps named above; I read, wrote or modified nothing there.

These verdicts accept no implementation and change no qualification determination: Protocol 7.0 remains NON-QUALIFIED. The OD-4(b) decision is recorded; this review authorizes neither the contract merge nor D4.
