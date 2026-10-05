---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.1.0
decision_date_utc: 2026-10-05
status: stakeholder-stated (recorded by the D3 design context; wording quoted verbatim)
---

# Option B re-open and the successor-candidate decisions OD-1 to OD-4

## 1. Option B direction

The 2026-10-05 D3 task brief that the stakeholder issued to the design context states:

> "Following the completion of the D4 package-access ledger implementation, the 25-scenario executor rehearsal matrix, and empirical target instantiation (…), the stakeholder reviewed the Stage 7 qualification failure and formally directed **Option B: Re-open Design**."

The brief names:
- the governing protocol: "SSDP **6.6.0**";
- the target: "Protocol 7.1 Candidate (Protocol 7.0 remains **NON-QUALIFIED** under Option A)".

Option A's determination for the 7.0 candidate (`STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-QUALIFICATION-CLOSEOUT.md`) is unchanged.

## 2. Answers to OD-1 to OD-3

The design context presented three decisions, each with a recommended answer, after the first independent review (`INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05.md`). The questions as presented:

- "OD-1: confirm "7.1.0" as the successor's version label."
- "OD-2: confirm that the decisions recorded as "Protocol 7.0" carry over unchanged. This includes the 2.0× size backstop, which is worded "for Protocol 7.0 only"."
- "OD-3: confirm that repeating "including any tools or agents you launched" in each question counts as required content under the 1,000 B size target, not as redundancy."

The stakeholder answered: **"Decisions confirmed. Proceed."**

**Effective decisions.**

| ID | Decision |
|---|---|
| OD-1 | The successor candidate's version label is **7.1.0**. |
| OD-2 | These decisions bind the 7.1.0 candidate unchanged, and "Protocol 7.0" in them reads as this workplan's target candidate: SD-B and its confirmation, the 2.0× fixed-cost backstop relaxation (its "for Protocol 7.0 only" scope included), SC1/SC2, activation Q1–Q5 and the package-access ledger decisions. |
| OD-3 | Under the SD-B per-element attribution, the launched-work qualifier repeated inside each delegate question is required content, not redundancy. **Recorder's reading, open to independent check:** the same applies to the tension question's launched-work clause and its "(or none)". The basis is the owner §6.3.11 *Form* sentence ("It covers work by tools or agents the delegate launched") and the answerable-either-way form. |

"Proceed" authorizes the design context to repair the first review's findings and resubmit for fresh independent Review. It does not authorize D4 implementation, which still requires independent PASS.

## 3. Recorder's note on the OD-2 enumeration (added after the second independent review; R2 m-1)

This note changes none of the quoted words above and none of the stakeholder's answer.

- **The enumeration is the recorder's reading.** The OD-2 question, as quoted in §2, names only "the decisions recorded as \"Protocol 7.0\"" and the 2.0× backstop. The five-part list in the OD-2 row of the effective-decisions table (SD-B and its confirmation, the backstop, SC1/SC2, activation Q1–Q5, the package-access ledger decisions) is the recorder's enumeration. The same list appears in the Question column of revision 1 of the design's decision table (`D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05-R1-HISTORICAL.md`, §10, OD-2). The quoted brief does not record whether the stakeholder saw that table, so the enumeration stays the recorder's reading.
- **Other "Protocol 7.0" decisions the list does not name.**
  - The 2026-09-28 single-participant human trial decision (`STAKEHOLDER-DECISION-2026-09-28-PROTOCOL-7.0-SINGLE-PARTICIPANT-HUMAN-TRIAL.md`) and the 2026-10-04 non-executor custody audit decision (`STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-EXECUTOR-CUSTODY-AUDIT.md`) are recorded for "Protocol 7.0". They bind the 7.1.0 candidate through the unchanged contract text (§7 and §1 item 9), and the literal OD-2 wording would carry them too. Nothing is lost by their absence from the list.
  - Campaign-specific decisions are not carried as such: the Stage 7 Option 1 claim-scoped admission (`STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-STAGE7-OPTION1-CLAIM-SCOPED-ADMISSION.md`) and the Option A closeout (`…-NON-QUALIFICATION-CLOSEOUT.md`) concern the 7.0 campaign and the 7.0 determination, which stays NON-QUALIFIED. A successor campaign needs its own admission.
- **Open point.** If the stakeholder intended a narrower or wider carry-over than the enumeration and the unchanged contract text give, the stakeholder states it; no other record relies on a reading beyond them.

## 4. OD-4: MCP server identity (decided after the R3 review)

The R3 review (`INDEPENDENT-D3-PROTOCOL-7.1-SALIENCE-AND-CONTRACT-REV16-REVIEW-2026-10-05-R3.md`, G-R3-2) found that the tool name the executor sees, `mcp__ssdp_delegate`, derives from the adapter-pinned MCP server name `ssdp70` and implies a governed delegate, which contract amendment A2 item 1 bans. The design context presented two options, with a recommendation for (a). The text presented, verbatim:

- "**(a) Rename the server to a neutral name.** This meets A2 in full, but it re-opens the OMP adapter and profile admission that the package-access work had closed (about 26 references)."
- "**(b) Keep the name** and disclose the `mcp__ssdp_` prefix as a residual cue present in every run of both arms. The alternative A2 text is already written in the amendment. Concealment stays partial, and the cue that the delegate may be governed remains."
- "I'd choose (a) if the re-admission cost is acceptable. The cue bears on the behavior being measured, namely whether delegators ask the questions."

**Correction of the presented cost (recorder, after the R4 review).** "About 26 references" counted three files and understated the rename. By grep over `qualification/ssdp70/eval/` for the server name, server id, `mcp__ssdp_` prefix and store identity, the scope is 14 files and over 100 matching lines, including the Claude adapter, the frozen profile templates and capability files, and four further test and probe files, and the store identity returned in every tool result is renamed too (design §7 *Server identity*). The stakeholder's answer below was given on the lower figure. It stays recorded as given; if the corrected scope changes the stakeholder's choice, the stakeholder says so before D4 starts the rename.

The stakeholder answered: **"Proceed with OD-4.a."**

**Effective decision.**

| ID | Decision |
|---|---|
| OD-4 | Option (a): the MCP server name and identifier, and the tool-name prefix derived from them, are renamed to values that imply neither governance status (neither SSDP governed nor not governed). **Recorder's extension:** also no scripted, stub, stand-in or qualification cue, which is the wording of A2 item 1; the store identity in tool results is renamed under the same rule. Contract amendment A2 item 1 stands as written. The cost accepted with it, as itemized by the recorder and corrected above: the reviewed OMP adapter constants, its tests, the mediator's server id and the frozen profile snapshots and capability manifests are re-derived and re-checked in D4, and the adapter/profile admission is re-established. |

**Recorder's reading, open to independent check.** "Proceed" authorizes the design context to record this decision in the design (§7, §10) and the amendment, and to continue to the contract merge once the revised bytes pass an independent check. It does not authorize the D4 rename itself, which is part of D4 and follows the same independent-PASS gate as the rest of D4. The exact neutral names are delegated to D4.
