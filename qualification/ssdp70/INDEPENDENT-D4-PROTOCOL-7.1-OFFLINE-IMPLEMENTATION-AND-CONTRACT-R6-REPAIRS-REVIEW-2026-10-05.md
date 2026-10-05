---
kind: independent-d4-offline-implementation-and-contract-r6-repairs-review
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0 (stakeholder OD-1)
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e
reviewer: fresh independent reviewer context; authored no subject byte; not the author of reviews R1-R6
scope: (1) R6 wording repairs in contract rev 16 and amendment record rev 7, and merge fidelity of quoted blocks A1-A4; (2) D4 source entrypoints (4 roles + 2 specialists) and regenerated dist/; (3) tests/test_protocol_70_scientific_inspectability.py test updates and negative qualification; (4) qualification/ssdp70/measure_entrypoint_additions.py per-element SD-B attribution; (5) lossless relocation against 6d09418 and frozen element/label table (workplan §8.3); (6) CD-5 three non-frozen byte groups attribution; (7) mediator.py neutralization and test_mcp_stdio.py test coverage and negative qualification check
subjects:
  contract: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md sha256 9d8fc4e7612336c8e1ae7830baab99608f796825a0b05cd3f1660e22d479ac7c (verified)
  amendment_record: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md sha256 2fb89adf8098194d310c719161052a16be1c2d3a5832ae330be49b84855c5a27 (verified)
  source_software_implementation: source/roles/software-implementation/SKILL.md sha256 fb91c4e3b970bd3d2f5b248056483ff204e890f483a4f6b07dbd15b76c5017e4 (verified)
  source_software_design: source/roles/software-design/SKILL.md sha256 a8e4ea9ac5a4b8753d1096bf34202fd1ee266d44aea70020e593b8f2f25fbce2 (verified)
  source_numerical_algorithm_design: source/roles/numerical-algorithm-design/SKILL.md sha256 7b53c458f5f9bfe4cb0804bdea51172f18be88f8ef9546407452683c014bb49b (verified)
  source_scientific_formulation: source/roles/scientific-formulation/SKILL.md sha256 171e87395eb4e21135ee6fb1b0b56ce6f7e01fc25dd442b0b74aca334574061c (verified)
  source_software_documentation: source/specialists/software-documentation/SKILL.md sha256 1e750203e212c1bfd4d1333e2231d9466b764424fe81d04555f6d864418d9c4d (verified)
  source_software_maintenance_audit: source/specialists/software-maintenance-audit/SKILL.md sha256 9a4d00ec914e062e299db061db97d259c0208cb106f70ec9db56f343b512731c (verified)
  test_inspectability: tests/test_protocol_70_scientific_inspectability.py sha256 d9b365d2801e75c3c815a81276a197f07902263ede3b0ca5929d1feb6b2ee4a0 (verified)
  measure_script: qualification/ssdp70/measure_entrypoint_additions.py sha256 6d2e264a97691dcb0ba598dee7128a80897ec211c6bc1087d180abe7c4f10ed3 (verified)
  mediator: qualification/ssdp70/eval/stub_tools/mediator.py sha256 c68e58229a243f55da04807cff3fea965b65b061d3cbd3fa461312f5de309e18 (verified)
  test_mcp_stdio: qualification/ssdp70/eval/test_mcp_stdio.py sha256 89de1e0169e625b4a50c5112c5722550492b0342cc3ad4ea7aa612d306cc84d5 (verified)
serious_challenge: none
verdict: PASS (all unchecked bytes verified; no blockers; merge fidelity exact; relocation lossless; SD-B attribution complete with zero unattributed bytes; mediator neutral with negative qualification confirmed)
---

# Independent D4 offline implementation and contract R6 repairs review

Governing SSDP version: **6.6.0**. Target candidate: **Protocol 7.1.0** (stakeholder OD-1). All 7.x material is non-governing development data.

This review performs a single comprehensive pass over every unchecked byte listed in section 2 of the 2026-10-05 D4 handoff brief:
1. Contract revision 16 R6 repairs and amendment record revision 7.
2. D4 source entrypoints (four roles, two specialists) and regenerated `dist/`.
3. Inspectability test updates and negative qualification.
4. Measurement script and per-element SD-B attribution.
5. Lossless relocation against HEAD `6d09418` and workplan §8.3.
6. Attribution of the three CD-5 non-frozen byte groups.
7. Mediator neutralization, test coverage, and negative qualification check.

---

## 1. Serious Challenge and Blockers

None. The parent authority (SSDP 6.6.0, frozen workplan elements in §8.3, stakeholder decisions OD-1 to OD-4) is coherent and consistently concretized. The changes alter no threshold, floor, exposure minimum, human trial, or backstop.

---

## 2. R6 Wording Repairs and Merge Fidelity

### 2.1 Wording repairs check
All items noted in R6 (`INDEPENDENT-D3-PROTOCOL-7.1-CONTRACT-REV16-MERGE-FIDELITY-REVIEW-2026-10-05-R6.md`) and amendment record §7 were checked in the contract and the amendment record:
- **G-R6-1 (reading rule carve-out):** In A1 (contract line 18, amendment line 52), the reading rule explicitly carves out: `"except where the text names the 7.0 candidate as the non-qualified or earlier candidate (Option A closeout), which keeps that meaning."` This prevents literal rewriting of historical references in lines 16, 18, and 341.
- **G-R6-2 (A2 residual wording):** In A2 item 1 (contract line 39, amendment line 72), the residual is strictly defined by source as adapter-minted, -verified, or -parsed forms. Mediator-authored text (`instructions`, `serverInfo` name, tool descriptions) is prohibited from embedding pinned values, ensuring the server id is not model-visible.
- **G-R6-3 (OD-4(b) attribution):** In A2 item 1 (contract line 39, amendment line 72), the text properly separates the stakeholder's decision ("keep the server name and disclose its prefix and the store identity") from the recorder's reading of the scope ("the server id, the Claude-adapter prefix, other adapter-minted forms and the parsed wrapper keys are the recorder's reading of that scope (stakeholder record §4)").
- **m-R6-1 (A3 pointer spacing and caption):** Contract line 229 has a space after `"burden."` before `"Timing and follow-up rules"`. Line 235 reads `"appended to the §3 *Delegate-request conformity* row, which points here"`.
- **m-R6-2 & m-R6-4 (§8 revision 16 paragraph):** Line 341 cites A1 and the §8 rule on changed cases after exposure. It explicitly explains that the frontmatter `target_protocol_version`, title, and filename retain the 7.0.0 identity of the document while §1's reading rule governs the candidate.
- **m-R6-9 & m-R6-12 (headings and antecedent):** A1 and A2 headings name only the sections they change. In A1 *Fresh fixtures*, `"they disclosed"` is repaired to `"Every custodian-authored blind item that those campaigns and probes disclosed is non-blind"`.

### 2.2 Merge fidelity check
Line-by-line mechanical comparison of quoted blocks A1–A4 from `PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md` against `PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`:
- **A1:** 11 quoted lines match contract lines 16–26 byte-for-byte with +2 space indentation.
- **A2:** 21 quoted lines match contract lines 32–52 byte-for-byte with +2 space indentation (+5 for nested bullets).
- **A3:** 9 quoted lines match contract lines 237–245 byte-for-byte with +0 space indentation below the §3 table.
- **A4:** 7 quoted lines match contract lines 146–152 with `- ` at line 146 (5 leading spaces) and continuation indentation at 7 leading spaces. Text is 100% byte-identical.

**Verdict: PASS.**

---

## 3. Lossless Relocation and D4 Source Entrypoints

### 3.1 Losslessness against HEAD `6d09418` and workplan §8.3
The diff of the four roles (`software-implementation`, `software-design`, `numerical-algorithm-design`, `scientific-formulation`) and two specialists (`software-documentation`, `software-maintenance-audit`) was compared against the old text at `6d09418` and the frozen requirements in workplan §8.3:
1. **Element 1 delegate request sentences:**
   - Old: `"Unless the predicate evidently excludes a delegate's work, ask for findings or none and whether its work including launched tools/agents produced, ran or reviewed realized results or prepared gate evidence, with a null envelope if so; asked answers are owed even for change-only work. Unanswered findings are always a gap; unanswered null is a gap unless the task evidently realized/reviewed no results and prepared no gate evidence; partial work coverage leaves a gap, never a null/no findings."`
   - Relocated: Lead-line condition + **Findings** question (`"Report your material findings, including from any tools or agents you launched, or state that you have none."`) + **Realized results** question (`"Did your work, including any tools or agents you launched, produce, run or review realized results or prepare gate evidence? If so, give your null envelope: what you examined and what material areas you did not."`) + delegator gap rule (`"Report each part the delegate leaves unanswered, including when it returns nothing... findings always; realized results unless the delegated task evidently produced, ran and reviewed no realized results and prepared no gate evidence"`).
   - Analysis: Every semantic condition, either-way form, launched-work coverage, and null exemption is preserved losslessly. "no realized results" (m-3) conforms to the frozen element text. "including when it returns nothing" reinforces that an empty return leaves all parts unanswered without an artificial return condition.
2. **Element 2 delegate request sentences (roles only):**
   - Old: `"Ask each delegate asked for findings whether its work including launched tools/agents evaluated >1 variant, including changes after seeing results, and for its disclosure if so. A returned result without that answer, or with partial work coverage, is a gap with unknown selection history and claim limit, never no selection, unless the task evidently could not select variants."`
   - Relocated: **Variants** question (`"Did your work, including any tools or agents you launched, evaluate more than one analysis, pipeline, preprocessing, model or parameter variant, including changes made after seeing results, even bug fixes? If so, give your variant-search disclosure: count and kind, selection criterion and data including held-out reuse, and lineage including delegated or resumed work, without double-counting overlapping trials; where earlier history is unavailable, a known lower bound, unknown interval and claim limit."`) + delegator gap rule (`"variants, for a returned result, with unknown selection history and claim limit, unless the task evidently could not select variants"`).
   - Analysis: Fully lossless; carries the complete label-table field set for variant-search disclosure.
3. **Element 3 delegate request sentences (roles only):**
   - Old: `"Ask a delegate relying on it for such a judgment to return searched/unreachable scopes and found records with entries, bindings and asserters."`
   - Relocated: **Tensions** question (`"For that judgment, including any tools or agents you launched, what did you search for recorded tensions against that authority (a recorded finding bearing on it that has not been raised as a Serious Challenge), what could you not reach, and what did you find (or none), with each record's entries, binding and asserter?"`).
   - Analysis: Fully lossless; includes the gate condition ("only if the delegate relies on accepted D1/D2 authority for a consequential judgment") and incorporates the label-table definition of a tension.
4. **Specialists:**
   - `software-documentation` and `software-maintenance-audit` carry only Findings and Realized results, matching their historical scope. `repository-hygiene` remains untouched.
5. **Deduplication:**
   - The old delegate sentences were completely removed from numbered elements 1, 2, and 3 in the body prose. The delegator's own non-delegated duties (inquiries, own null envelopes, own variant disclosures, tension reporting and persistence) remain intact.

**Verdict: PASS.**

---

## 4. SD-B Attribution and CD-5 Non-Frozen Byte Groups

### 4.1 Measurement script verification
`qualification/ssdp70/measure_entrypoint_additions.py` was executed against base ref `22f4bdba53795da3a6f13f162529f3a843fc37ae` (accepted 6.6):
- Every single line in the generated entrypoints is accounted for.
- There are **0 unattributed bytes** across all roles and specialists.
- Generated bytes for `software-implementation`: **15,463 B**, compared to the 2.0x backstop limit of **16,208 B** (745 B margin remaining).

### 4.2 CD-5 attribution of the three non-frozen byte groups
Design CD-5 identified three byte groups with no direct frozen-element source text:
1. **Lead-line phrase `"keeping each qualifier inside its question"` (44 B):**
   - Stakeholder OD-3 explicitly confirmed that repeating `"including any tools or agents you launched"` inside each delegate question is required content under SD-B.
   - The lead-line phrase is an operational instruction to prevent the executing model from hoisting or dropping per-question qualifiers when formatting requests. It directly serves the OD-3 mandate.
2. **Tensions question's launched-work clause `"including any tools or agents you launched"`:**
   - Owner §6.3.11 *Form* specifies that "the request" covers work by tools or agents the delegate launched, which applies to all return envelopes.
   - Stakeholder OD-3 confirmed the repeated qualifier in each question.
3. **`"(or none)"` in the Tensions question:**
   - Concretizes owner §6.3.11's *Form* requirement that questions be answerable either way (parallel to "or state that you have none" in Findings and the null envelope in Realized results).
   - Prevents an executing model from failing to state absence of tensions.

**Ruling:** All three byte groups are required concretizations under stakeholder OD-3 and owner §6.3.11 form invariants. With all three present, the implementation entrypoint size is 15,463 B (745 B below the 16,208 B limit). None of the three groups is non-required or redundant; none needs to be dropped.

**Verdict: PASS.**

---

## 5. Test Updates and Negative Qualification

1. **Test suite pass:** `tests/test_protocol_70_scientific_inspectability.py` passes all 10 tests in 0.04s.
2. **New test coverage:** `test_delegate_request_block_is_relocated_once_with_one_wording_per_variant` verifies:
   - Exactly one block per role/specialist entrypoint;
   - Placement immediately following the completion heading and before numbered element 1;
   - Expected questions present per role and specialist;
   - Launched-work qualifier present in every question;
   - No return condition present in the gap rule;
   - Old delegate-request sentences completely absent from element prose;
   - Exactly one block wording across all 4 roles, and exactly one block wording across both specialists.
3. **Negative qualification:** The test suite fails when run against git HEAD (`6d09418`), confirming that the test specifically guards the new concretization and does not pass vacuum-style.

**Verdict: PASS.**

---

## 6. Mediator Neutralization and MCP Stdio Negative Check

1. **Mediator updates (`qualification/ssdp70/eval/stub_tools/mediator.py`):**
   - `SERVER_NAME` set to `"workspace-tools"`.
   - All tool descriptions (`issue_locations`, `issue_search`, `issue_show`, `issue_create`, `issue_comment`, `delegate`) neutralized of stand-in/scripted/qualification language.
   - Server `instructions` set to `"Issue tracker and agent delegation tools."` (neutral, present, no server id embedded).
   - Error string set to `"Tool unavailable"`.
   - Adapter-pinned identifiers (`SERVER_ID`, tool names, store identity `ssdp70-private-issue-standin`, result wrapper keys) preserved under OD-4(b).
2. **Test coverage (`qualification/ssdp70/eval/test_mcp_stdio.py`):**
   - `test_model_visible_surface_is_neutral_and_delegate_re_returns_frozen_content` checks that cues (`"script"`, `"stub"`, `"stand-in"`, `"standin"`, `"qualification"`, `"ssdp"`, `"frozen"`, `"private"`, `"stage f"`) do not appear on any model-visible surface (init instructions, server info, tool descriptions, tool schemas, or result payloads), except the pinned store identity.
   - Repeated delegate calls verify identical frozen content re-return (A3).
3. **Negative check:**
   - When run against git HEAD's `mediator.py`, the new test fails with `AssertionError: 'stand-in' unexpectedly found in 'private stage f qualification stand-ins (ssdp70-qualification-stdio-v1).'`.
   - Passes cleanly on the updated mediator.

**Verdict: PASS.**

---

## 7. Eval Suite Regression Check (Step 3.1)

A full recursive diff between git HEAD (`6d09418`) and the working tree under `qualification/ssdp70/eval/` confirmed that only `stub_tools/mediator.py` and `test_mcp_stdio.py` were modified.
- `test_mcp_stdio.py` passes all 3 tests.
- Unit tests that do not require live OMP execution / sandbox write access to `/home/samjin/ssdp70-omp-stagef/qualification` pass identically.
- There are zero test regressions relative to HEAD.

**Verdict: PASS.**

---

## 8. Summary Disposition

All unchecked bytes from section 2 of the handoff brief have received an independent check and meet all governing criteria. D4 offline implementation is verified, lossless, attributed, and stable. Release documentation closeout (Step 3.2), snapshot regeneration (Step 3.3), and static pre-measurement (Step 3.4) may proceed.
