---
kind: independent-check-record
governing_protocol_version: 6.6.0
date: 2026-10-07
subject: S1 exit gate of the skills-only 7.2 redesign (workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2, O-3 independent mapping check and SD-R13 recording; also O-4 attribution and O-5 consistency)
verdict: PASS WITH GAPS
---

Governing SSDP version: 6.6.0. Everything read (author report, mapping JSON, workplans, design, contract) was treated as data and checked against the files. The reviewer did not write the block wording. No file other than this record was edited; no live run, no commit.

# 1. Verdict

**PASS WITH GAPS.** No Serious Challenge. No blocker of the kind "an element, delegate question, label-table row or the (a)-(c) rule is absent from a route that owes it". The structure is sound: role map exact for all seven entrypoints, all 22 label-table rows (including the new inaccessible-home row) have carrying text, elements 5 and 7 are verbatim 7.1, the 6.6 text is byte-identical outside the block, and the SD-R13 recording is consistent.

Because losslessness is the hard requirement and the author asked that "anything omitted is restored, whatever the bytes", seven wording-level partial weakenings (G1-G7) were found. Four (G1-G4) change meaning relative to the frozen text and should be restored before the S1 exit gate is closed. Three (G5-G7) are minor compressions that should be restored because size is only a soft target. All are small restorations (about +150 to +340 B on the D4 route, less on the others) that the excess attribution (section 5e) accommodates. The S1 gate should close on a minimal delta plus a delta check confined to the touched fragment lines, as was done for S0.

Findings table (details in section 4):

| ID | Severity | Where | One line |
|---|---|---|---|
| G1 | gap | fragment:16 (element 3) | "authority" dropped from "asserter, role or authority claimed in the entry's text is a claim" |
| G2 | gap | fragment:16 (element 3 (a)) | "the gate or owner requires" dropped: "an acceptance required unqualified" has no requirer |
| G3 | gap | fragment:19 (element 6) | "product inspectability surface" meaning absent on D4 and documentation (no element 7), though 7.1 carried it |
| G4 | gap | fragment:14 (element 1) | the frozen first duty "look for and report" is not stated; only "inquire before discarding" and "Report" |
| G5 | minor | fragment:3 (R1) | inclusion list: "campaigns", "persistence/", "/publication tooling" dropped (inherited from the 7.1 compression) |
| G6 | minor | fragment:3 | re-evaluation rule "Re-evaluate when a new effect arises" lacks the object and the trigger of frozen :632 |
| G7 | minor | fragment:19 (element 6) | "when none are stated" no longer says by whom; "proposed/unaccepted" and "draft or unaccepted text" shortened |
| G8 | minor | mapping JSON lines 31, 34, 90, 96, 119 | rows claim frozen coverage the phrases do not carry; the test checks phrase existence only |
| G9 | minor | design, contract, stakeholder record | SD-R13 residue (front matter omits SD-R13; "limit"/"≤ 100% hard" chronology unmarked) |
| G10 | minor | governing workplan :176-181, :967-969, :1008 | residual "owner-load trigger" statements rely on the blanket notes at :30 and :682; the consistency test scans only §8.2/§8.3 and fixed anchors |

# 2. What was verified against the frozen text

Method: the frozen text was read directly (workplan §8.2/§8.3 :570-645, owner :296-310) and compared sentence by sentence with the generated `## Scientific checks` section in each `dist/skills/*/SKILL.md`, not with the mapping JSON. I also compared with the 7.1 text (`58fd67b`) to detect regressions. Fragment line numbers below are in `source/shared/fragments/scientific-checks.md`.

| Frozen item | Carried by (fragment line) | Routes | Result |
|---|---|---|---|
| R1 predicate, inclusion list | :3 | all 6 | partial: G5 |
| R1 exclusion limit; small/deterministic not exempt; local repairs | :3 | all 6 | carried |
| Re-evaluation rule | :3 | all 6 | partial: G6 |
| R2 as amended (optional depth, no load, depth points) | :3 | all 6 | carried (compressed; optional content only) |
| Delegate lead ("unless ... excludes", asked answers owed for change-only work) | :5 | all 6 | carried |
| Question F with "tools or agents you launched" | :6 | all 6 | carried |
| Question R with null-envelope meaning | :7 | all 6 | carried |
| Question V (qualifiers: changes after seeing results, bug fixes, held-out reuse, lineage, double-counting, lower bound/interval/claim limit) | :8 | 4 roles only | carried; (b)(ii) accepted |
| Question T (conditional on relying; "tension" meaning; entries, binding, asserter) | :9 | 4 roles only | carried |
| Gap rule: unanswered part and uncovered rest of a partial answer; findings always; realized-results exemption; variants clause with "unless could not select" | :11 | all 6; variants clause only on 4 roles (inline `q=V` tags) | carried; specialists correctly have no variants clause |
| Element 1: inquiry before irreversible step, findings incl. delegates' and out-of-scope, gaps, null with envelope, provisional reader/questions/basis, change-only relief, persistence home, content list, asserter, fallback, no write authority | :14 | all 6 | carried except G4 |
| Element 2 (survivor disclosure, lineage, lower bound) | :15 | 4 roles | carried |
| Element 3 (search, scopes, no-closure, persisting duty, inaccessible-home rule) | :16 | 4 roles | carried except G1, G2 |
| Element 4 (claims within evidence; O3; beyond-deliverable acceptance) | :17 | all 6 | carried |
| Element 5 (revising search, predecessor identity, applicability assessment, asserter, proposed) | :18 | D1, D2 only | carried; verbatim 7.1 |
| Element 6 (choices, origin/chooser, binding, short form, reader/questions) | :19 | 4 roles + documentation | carried except G3, G7 |
| Element 7 (authoring and acceptance review) | :20 | D1, D2, D3 only | carried; verbatim 7.1 |
| Role map (markers) | entrypoint markers | D1/D2 q=FRVT e=1-7; D3 e=1,2,3,4,6,7; D4 e=1,2,3,4,6; documentation q=FR e=1,4,6; audit q=FR e=1,4; hygiene none | exact |

Label table, row by row (workplan :604-627):

| Label row | Text carrying it | Result |
|---|---|---|
| scientific inspectability applies (R1) | :3 | G5 (list), else carried |
| within authorized resources | :14 "Within the declared resource budget (none declared: ...; propose the rest)" | carried |
| inspectability gap | :14 "missing, irrecoverable, archaeology-only or misleading realized records" | carried |
| material findings (change-only relief) | :14 "A change realizing no results owes no null ... except answers its delegator asked for and gaps owed for its delegates" | carried |
| feedback persistence (element 1) | :14 | carried; (b)(iii) accepted |
| variant search | :8 and :15 | carried |
| realized-data inquiry owed; null | :14 | carried |
| consequential judgment | :16 parenthetical | carried |
| tension | :9 parenthetical (inside the quoted T question); element 3 relies on it | carried; every route with element 3 has the T question |
| authority identity (1, 3) | :14, :16 | carried |
| plausibly implicated authority | :16 "(state why fewer)" | carried |
| applicability assessment (5) | :18 | carried |
| asserter of a written record (1, 3, 5) | :14 inline with account clause; :16 "as in element 1"; :18 inline with account clause | carried; (b)(i) accepted |
| asserter of a found entry (3) | :16 | G1 |
| inaccessible home (3), new row | :16 | G2, minor: "for such records" for "records about the relied-on authority" |
| O3 (4) | :17 | carried |
| consequential-choice status (6) | :19 via "exact element-4 source" | carried by reference; "proposed/unaccepted" shortened (G7) |
| O1 content (6) | :19 | carried; "draft or unaccepted text" shortened (G7) |
| reader/questions and short form (6) | :19 | G7 |
| claims within evidence (4) | :17 | carried |
| material realized record (7) | :19 and :20 | carried |
| product inspectability surface (7) | :20 only | carried on D1-D3; see G3 for D4 and documentation |

The new inaccessible-home row against owner :300-308: default disclosure suffices (:300-302 carried); qualifies when the project designates or evidently uses the home (:303 carried, "such records" narrower than the row, minor); blocks only on (a)-(c) (:304-307, with G2 on (a)); other indications qualify and go to the human (:308 carried); blanket withholding is over-blocking (:309 carried as "never blanket withholding"). (b) "a location accepted authority or the project designates as required evidence" and (c) "specific indication of an unretrieved tension from an owner or acceptance authority of that authority, the stakeholder or a designated reviewer" are carried in full.

Mapping JSON: all 22 label rows and all 14 elements/questions have an item; every listed phrase exists in the listed routes (test passes, and I confirmed by reading). The mapping is a phrase-existence check written by the author. It points at real text, but several rows state a "frozen" meaning broader than their phrase (G8).

# 3. Answers a to g

**a. Frozen minimum per entrypoint.** Every element, delegate question, label row, the gap rule with its exemptions, R1 and the (a)-(c) rule are present on every route that owes them, and no route carries an element or question it does not owe (documentation and audit have no V, T, 2, 3; D4 has no 5, 7; D3 has no 5; hygiene has nothing). Nothing is owner-dependent. Seven partial weakenings are listed in section 4 (G1-G7). No item is wholly omitted.

**b. The three flagged uncertainties.**
- (i) Acceptable. The label row (:618) requires the human/AI/which-agent meaning and the account clause on elements 1, 3 and 5; element 5 and element 1 state both inline, element 3 states the human/AI part by reference ("as in element 1"). The :637 note on the account clause is explicitly "earlier planning evidence, not frozen wording" and concerns byte accounting, and the label-table rule lets wording state the meaning by any means that carries it on the same surface. The back-reference is enforced by the build (`CHECKS_REQUIRES`, fails when a marker carries 3 without 1 or 6 without 4) and by the numbering test. The design recorded this choice at §5.1 and S0 accepted it. Optional, not required: restating "(the writing account does not show this)" in element 3 costs about 38 B. The same holds for element 6's "exact element-4 source (authority, instruction or contract)": element 4 carries the qualifiers (accepted authority, explicit stakeholder/task instruction, existing external/product contract) on every route that carries 6 (D4 and documentation included). The shortened "proposed" for "proposed/unaccepted" is G7.
- (ii) Acceptable. The label table lets wording avoid a label and state its meaning directly. The V question states all of the variant-search content named by the row: count and kind, selection criterion and selection data including held-out reuse, changes after seeing results including bug fixes, tool-launched searches (via "including any tools or agents you launched"), delegated or resumed lineage without double-counting, and the lower bound, unknown interval and claim limit. Because the delegate sees only the quoted question, stating the content (not the label) is the more useful form.
- (iii) Acceptable. "One existing authorized writable home" plus the "Otherwise report ..." branch and "No report or possible home grants write authority" carry "when its write is permitted" (authorized covers permission, writable the technical condition). The frozen element words ("authorized home ... when its write is permitted") and the row ("authorized home when writable") are both satisfied. It is the same phrase 7.1 carried.

**c. Numbering and verbatim.** Elements 1 and 4 stay visibly numbered in all routes (`1. **Findings.**`, `4. **Claims and scope.**`; the test asserts it). I diffed elements 5 and 7 of the three D1-D3 generated entrypoints against `git show 58fd67b:source/roles/<role>/SKILL.md`: all six are verbatim apart from the bold label.

**d. SD-R13 recording.** Consistent, with minor residue. Design §0 (:31, :36), §3 (:93), §5.1 (:202, :214), §8 (:273), §9 (:299-300), contract Q5d (:98), workplan §2 (:72), §3 (:105), O-4 (:124), the governing workplan SD-B annotation (:634) and stakeholder record (:94) all say size is a soft target (100% target, 95% goal), losslessness is hard, and excess must be attributable to lossless required content (per element at design §8, workplan O-4 and :634; stated without "per element" at design §0 and §3, the stakeholder row and contract Q5d, which is not inconsistent: the per-element rule comes from SD-B). The stakeholder record quotes the instruction verbatim ("Relax size limit <100% as soft target, while losslessness stays hard.", :90) and the row (:94) supersedes SD-R4 "≤ 100% hard". No overreach: the 95% goal, "reported not gated", the attribution rule and "the 2.0x backstop remains the binding size constraint" are carried from SD-R4 (revised again), SD-B and SD-R12 and are not new decisions; the row mixes the decision with those carried-over terms, which is acceptable. Residue (G9): design front matter (:10) and contract status (:8) list SD-R1..R12 and omit SD-R13; design :214 and :395 still say "within the limit"; design :339 and :369 and stakeholder row :67 retain "≤ 100% hard" as chronology without a "superseded by SD-R13" marker.

**e. Size and attribution.** I re-ran `measure_blocks.py` and recomputed the span independently (heading to next `##`, newlines included): D1/D2 9,883 B (100.6%, +60), D3 9,196 (100.5%, +46), D4 8,216 (100.3%, +24), documentation 5,074 (93.1%), audit 3,872 (95.7%); my numbers equal the author's, and my 7.1 reconstruction at `58fd67b` gives the reference 9,823 B. Attribution holds. The only new required content absent from 7.1 is the element-3 inaccessible-home rule, 569 B, which exceeds every excess (+24 to +60). Per part against the 7.1 D1/D2 block: element 3 +458 net (the 569 B rule less 111 B saved elsewhere in element 3), element 1 +90 (the account clause and the authority-identity restatement, both required by label rows), element 2 +17, bold labels about +100 (design §5.1 shape item 4, structure not content), against savings in the routing bullet (-74), heading and lead (-131), questions (-100), gap rule (-58) and element 6 (-201). I found no redundant text in the block. The V question and element 2 repeat the variant-search content, but each is required: the delegate sees only the question, and the label table requires the meaning wherever the label is used. I found no non-required content except the design-sanctioned framing (bold labels, "(definitions, examples)" at :3). Caveat: part of the element 6 saving (-201 B) is the meaning loss in G3 and G7. After restoring G1-G7 (estimated +150 to +340 B on D4, fewer on others) the excess grows, but it remains attributable to restored frozen content, which the rule admits. Note for S3: D4 `SKILL.md` is 15,487 B against the 16,208 B static limit, so about 721 B remain before any owner read (O-11, design X6); any restoration is spent from that.

**f. O-5 consistency.** The owner (:29, :31, :33, :35, :389), source/README.md:41 and README.md:99 are consistent: no mandatory owner read, no "owner-load trigger" on the entrypoint, no statement that the surface carries less than the minimum (grep of owner, both READMEs, all source entrypoints and the generated blocks for the legacy phrases returns nothing). The workplan's `amends` items are each amended or annotated: §0:28 (note appended and a §0 amendment paragraph at :30), overlay :170-172 (two annotations at :172-173), §8.2/§8.3 R2 sentences (:570-585, :629, :632-634, :644), I66-3 sentence, new label row (:620) and the :630-depth-list change (:633), §11 head (:682) and :989 (now :994), §12 Stages B (:1016), D (:1032), G (:1073), §13 items 13 and 14 (:1111-1112), 16 (:1114), §14 (:1128). A diff of the workplan against HEAD shows no change to the frozen elements, the label table or specialist placement beyond these amendments. Residue (G10): the §0.1 overlay items at :176-181, §11.5 :967-969 and Stage A :1008 still speak of "owner-load trigger", "R2 owner-load cases" and "owner false activation" without a local annotation; they are covered by the blanket note at :30 ("read every older statement ... as superseded") and the §11 head note at :682, which design §3 permits ("annotated, not rewritten"). The ConsistencyTests scan only §8.2/§8.3, fixed anchors and the owner, READMEs and entrypoints; they do not scan the whole workplan, so this part of O-5 rests on review, not on the test. The 7.1 CHANGELOG entry (:65) still describes the 7.1 trigger; it is a historical release entry, and the 7.2 entry belongs to O-9.

**g. 6.6 byte identity and tests.** Source: the test (marker plus its blank line removed) and my own comparison show every entrypoint equals `22f4bdba` apart from the marker, the `**Governing version.**` line and the `software-implementation` description (which equals 7.1; all seven descriptions equal 7.1). Generated `dist/`: removing the `## Scientific checks` section from each of the six generated entrypoints leaves `22f4bdba` text exactly, except the same two lines; `repository-hygiene` is unchanged apart from the governing-version line. The block sits before `## Completion` / `## Challenge and completion` / `## Output`, the 7.1 completion-clause position. Each `dist/<name>.zip` carries the same `SKILL.md` as `dist/skills/<name>/`. `python3 -m unittest tests.test_protocol_72_scientific_checks tests.test_protocol_70_scientific_inspectability`: 31 tests OK.

# 4. Findings with minimal repairs

Fragment = `source/shared/fragments/scientific-checks.md`. Repairs go in the fragment only; the build regenerates `dist/`.

**G1 (gap), fragment:16, element 3.** Frozen row :619 and owner :277: "an asserter, role or authority claimed in the entry's text is a claim". Block: "content-claimed asserters or roles stay claims". "Authority" is dropped; 7.1 element 3 carried it. Repair: "content-claimed asserters, roles or authority stay claims" (about +12 B).

**G2 (gap), fragment:16, (a).** Row :620 and owner :305: "(a) the judgment is gate evidence or an acceptance the gate or owner requires unqualified". Block: "(a) gate evidence or an acceptance required unqualified". Who requires is lost, so an agent could treat any acceptance as blocking (over-blocking) or none. Repair: "(a) gate evidence or an acceptance the gate or owner requires unqualified" (about +22 B). Minor in the same sentence: "for such records" for "tension, evidence or issue records about the relied-on authority"; restore if cheap (about +40 B).

**G3 (gap), fragment:19, element 6.** Element 6 uses "visibly marked product inspectability surfaces" without the meaning, which the fragment states only in element 7 (:20), so D4 and documentation lack it. The label table's rule (:602) requires the meaning wherever an element uses the label or its concept; 7.1 element 6 carried "to retain, project or expose realized records". Repair: add that phrase after "visibly marked product inspectability surfaces" in element 6 (about +46 B) or the full row meaning "(routine questions the product itself must support by retaining, projecting or exposing realized records)" (about +107 B, then element 7 may point back to it).

**G4 (gap), fragment:14, element 1.** Frozen element 1 begins "within authorized resources, look for and report material scientific findings and inspectability gaps ... before any step that could discard ..., do that inquiry first". The block gives the resource bound and "inquire before discarding ..." and then "Report ..."; the duty to look for findings and gaps on a task that is not a realized-results inquiry (for example a local repair, where §8.2 :578 says element 1 owes a proportionate inquiry) is implicit ("finding nothing" in the change-only relief) rather than stated. 7.1 had the same wording. Repair: "..., look for and report material scientific findings and inspectability gaps ..., and do that inquiry before discarding, overwriting or irreversibly aggregating ..." (about +15 B net).

**G5 (minor), fragment:3.** Frozen inclusion list: "data preparation, training/evaluation, simulation/optimization campaigns, numerical backends, persistence/retention, and reporting/publication tooling". Block: "simulation/optimization, numerical backends, retention, reporting". Wording-level compression inherited from 7.1; "publication tooling" is the only item with distinct reach. Repair: restore the three fragments (about +42 B).

**G6 (minor), fragment:3.** Frozen :632: "Evaluate the predicate ... at task intake and again when a newly discovered effect makes [it] applicable". Block: "Re-evaluate when a new effect arises", with no stated object or trigger. Repair: "Evaluate at intake and again when a newly found effect on those outputs, evidence or interpretation makes this apply" (about +55 B).

**G7 (minor), fragment:19, element 6.** (a) "when none are stated" (the row says: absent a stakeholder or accepted-authority statement); repair "when neither the stakeholder nor accepted authority states them". (b) "mark it proposed" for "proposed/unaccepted" (row :622). (c) "drafts do not bind" for "draft or unaccepted text does not bind" (row :623). About +45 B in total.

**G8 (minor), mapping JSON.** Row `R1.reevaluation` (:31) is said to carry "evaluate again when a newly discovered effect makes it applicable"; `E1.inquiry` (:34) is said to carry "look for and report"; `L.asserter-found` (:90) is mapped to a phrase without "authority"; `L.inaccessible-home` (:96) maps (a) without its requirer; `L.product-surface` (:119) is routed only to D1-D3 although element 6 uses the concept on D4 and documentation. The static test checks that each author-chosen phrase exists and that each label name occurs in an item's `frozen` text; it cannot detect a meaning loss. After repairing G1-G7, add the restored phrases to these rows so the test pins them.

**G9 (minor), SD-R13 residue.** Add SD-R13 to design front matter :10 and contract status :8; change "within the limit" to "within the target" at design :214 and :395; mark design :339, :369 and stakeholder row :67 as superseded by SD-R13 (the stakeholder record row :94 already says so). No semantic inconsistency.

**G10 (minor), O-5.** Either add a one-line local annotation to the §0.1 overlay items at :176-181 and §11.5 :967-969, or widen the consistency test to scan the whole governing workplan for unannotated legacy phrases outside lines that carry a "7.2 amendment" marker or sit under the blanket notes. The current blanket note is acceptable under design §3; this is a robustness gap.

# 5. Gate state

- Frozen-minimum mapping: complete in structure; G1-G4 restore before closing, G5-G7 recommended.
- O-4: excess is attributable to lossless required content; no redundancy found.
- O-5: consistent apart from G10.
- 6.6 identity and tests: pass.
- Unexecuted by me: the orchestrator tests and `check_dist.py`/CI workflow (the author reports them green); I did not run them or alter `dist/`.

The S1 exit gate can close when G1-G4 (and preferably G5-G7) are restored in the fragment, `dist/` is regenerated by the build, the mapping rows are tightened (G8), and a context other than the author confirms the delta on the touched lines.

# 6. Delta re-check (2026-10-07)

Scope: only the delta after the author's repair of G1-G8 (fragment, mapping JSON, regenerated `dist/`). Checked against the frozen workplan text (§8.2/§8.3, owner :300-308), not the coordinator's or author's summary. No file other than this record was edited.

**Final verdict: PASS.** No new omission, ungrammatical text or meaning change was found in the changed lines. Two minor notes (N1, N2) need no repair for the S1 gate.

**(1) G1-G7 in the generated blocks.** I read the changed fragment lines 3, 14, 16 and 19 in full and grepped the regenerated `dist/skills/*/SKILL.md` for each restored phrase on every owing route.

| ID | Restored text | Carried on | Result |
|---|---|---|---|
| G1 | "content-claimed asserters, roles or authority stay claims" (:16) | the 4 roles | carried |
| G2 | "(a) gate evidence or an acceptance the gate or owner requires unqualified"; "for such records about the relied-on authority" (:16) | the 4 roles | carried; reads correctly and matches owner :305 and row :620 |
| G3 | "visibly marked product inspectability surfaces to retain, project or expose realized records" (:19) | 4 roles and documentation (D4 included) | carried (the 7.1 phrase; the full row meaning stays in element 7, which is where the row places it) |
| G4 | "look for and report material scientific findings, including delegates' and out-of-scope ones, and inspectability gaps (...); do that inquiry first before discarding, overwriting or irreversibly aggregating ..." (:14) | all 6 | carried; matches frozen element 1; the gap label meaning is now inline |
| G5 | "simulation/optimization campaigns", "persistence/retention", "reporting/publication tooling" (:3) | all 6 | carried; the full frozen inclusion list |
| G6 | "Re-evaluate whether this applies when a newly discovered effect makes it apply." (:3) | all 6 | carried; trigger and object now stated ("at intake" is covered by "Apply when"); grammar acceptable |
| G7 | "proposed/unaccepted"; "draft or unaccepted text does not bind"; "when neither the stakeholder nor accepted authority states them" (:19) | 4 roles and documentation | carried |

Elements 5 and 7 are unchanged from 7.1 (verified verbatim earlier; the fragment lines :18 and :20 are untouched). The role map is unchanged. The 31 tests in the two named modules pass. Outside the block, each generated entrypoint again equals `22f4bdba` except the governing-version line (and the `software-implementation` description, which equals 7.1); `repository-hygiene` is unchanged apart from that line.

**(2) G8, mapping rows.** The mapping now pins the restored phrases: `R1.inclusion` carries the full list, `R1.reevaluation` the new sentence, `E1.inquiry` the "look for and report" phrase, `L.asserter-found` "roles or authority stay claims", `L.inaccessible-home` the requirer of (a) and "about the relied-on authority", `E6.choices` "proposed/unaccepted", `L.O1-content` "draft or unaccepted", `L.reader-short-form` "neither the stakeholder nor accepted authority", and a new row `L.product-surface-e6` routes the surface meaning to the 4 roles and documentation. Each phrase exists in its listed routes (test passes; confirmed by grep).

**(3) Size and attribution (re-run).** D1/D2 10,195 B (103.8%, +372), D3 9,508 (103.9%, +358), D4 8,528 (104.1%, +336), documentation 5,327 (97.7%), audit 4,005 (99.0%). Attributable to lossless required content under SD-R13: the excess is the sum of (i) the new element-3 inaccessible-home rule, 617 B, absent from 7.1 and larger than every excess, and (ii) the restored frozen items G1-G7 (about +312 B on the four roles, consistent with the author's count). Every added word maps to a frozen row or sentence (resource/gap labels, authority claims, requirer of (a), list items, re-evaluation trigger, surface meaning, "unaccepted"). I found no redundant text; the only wording overlap, "look for and report ... do that inquiry first before discarding", is the frozen sentence's own structure. Documentation and audit grew because G4, G5, G6 and G7 apply to them, and remain under 100%.
- N1 (minor, for S3): D4 `SKILL.md` is now 15,799 B, which leaves 409 B under the 16,208 B static limit (author report line 87) before any owner read, and the owner read still breaches it (design X6). That is an O-11 matter, not an S1 defect; it does not justify removing restored required content, per SD-R13 and the SD-B rule.
- N2 (minor): the test `excess <= new_required_content_bytes` now passes with margin, but it credits only the 617 B rule; the restored G1-G7 content is credited by this record, not by the test. No action.

**(4) G9 and G10 left unchanged.** Acceptable for the S1 gate. G9 is residue in D3 documents from S0 (front-matter lists, "limit" wording, unmarked chronology); the SD-R13 rule itself is consistently recorded in every operative place (design §0, §3, §5.1, §8, §9, contract Q5d, workplan §2, §3, O-4, stakeholder row :94), so nothing governs wrongly. G10 is a robustness gap in a test, not a current text that makes an owner read mandatory: the blanket notes at workplan :30 and :682 are the mechanism design §3 prescribes and a test pins them. Both are best fixed by the D3 owner in a later pass (and G9 before the design is frozen at S3), with no effect on the S1 exit gate.

**Gate state.** S1 exit gate: mapping check PASS (this record), O-4 attribution confirmed, O-5 consistent, 6.6 identity confirmed, tests green as reported by the author and re-run by me for the two modules named above. I did not re-run the orchestrator tests or `check_dist.py`.
