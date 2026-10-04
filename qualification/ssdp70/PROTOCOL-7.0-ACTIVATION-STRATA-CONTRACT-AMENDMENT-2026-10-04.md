---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 3
status: revision 3 drafted; fresh independent check required (contract) together with fresh independent workplan Review (overlay revision 2)
---

# Activation-strata amendment to the Protocol 7.0 qualification contract (revision 3)

## 1. Authority and status

- **Authority.** `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-DETERMINISTIC-ACTIVATION-AND-ACTIVATION-QUALIFICATION.md`:
  - §5: the stakeholder's verbatim refinement, with 2b recorded as conditional;
  - §6: the stakeholder's verbatim answers Q1–Q4 to the second independent check.

  Recorder derivations D1, D2 and D4 are labelled where used. D3 is superseded by Q3.
- **Workplan.** The active workplan's §0.1 overlay, revision 2, with a header decision entry and markers at every affected location.
- **History.**
  - Revision 1 (`d370193`): NO-PASS, recorded in `ACTIVATION-STRATA-AMENDMENT-INDEPENDENT-CHECK-2026-10-04.md`.
  - Revision 2 (`0c5372d`): NO-PASS, recorded in `ACTIVATION-OVERLAY-AND-CONTRACT-REV2-INDEPENDENT-CHECK-2026-10-04.md`.
- **Authorship.** The same context authored all three revisions, so it cannot accept this one.

## 2. Evidence

The evidence is unchanged from revision 2:
- the treatment-delivery diagnosis;
- the doctrine-loaded M07 probe;
- the stronger-executor selection probe;
- the runtime command-activation probe (`STAGE-7-*-2026-10-04.md`).

## 3. Contract changes in revision 3

| Section | Change |
|---|---|
| §1 item 4 | The deterministic delivery record holds:<br>• the installed `SKILL.md` hash;<br>• the delivery-transform identity;<br>• the delivered-text hash;<br>• the hash-linked observer record of the first provider request;<br>• the byte offset of the delivered text within that request. |
| §1 item 12 | Rewritten.<br>• **`runtime-command`** is admissible only where expansion is demonstrated for that runtime and mode.<br>• **`harness-injection`** must reproduce the same runtime's demonstrated `runtime-command` request 0. A runtime with no demonstrated command delivery (Codex `exec`) has no deterministic stratum.<br>• **Proof.** A per-runtime *delivery transform* is frozen, and proof is **observer request 0**. Adapter or runtime records only corroborate. A runtime without an observer is claim-scoped inadmissible.<br>• **Activation failure.** The run is inadmissible for every floor and fails the profile's criterion, with no rerun rescue. Requalification needs a new profile key, a fresh pre-run check and a fresh campaign.<br>• **Ordinary reporting.** Four groups, plus at least 3 episodes per arm per new class (D2).<br>• **Retained false-activation floors (Q4).** Predicate false-firing is measured on deterministic runs.<br>• **Run-type strata** are revised accordingly.<br>• **Profile coverage (Q1).** At least one flash-class profile uses `runtime-command`. Injection is never the only evidence. Each profile stands alone (D1). |
| §3 | The activation row counts **every declared deterministic run**, including inadmissible ones. It states the Q1 requirement and points to the §4 floors that remain binding. |
| §4 | Only the 6.6 correct-selection bound is report-only (Q3). The 6.6 negative and near-boundary false-activation bounds and predicate false-firing stay floors (Q4). The routing probes and sentinels are deterministic, with their floors intact. The T1/T7/T8 byte metric is **unchanged** (whole installed `SKILL.md` plus SSDP files read, each counted once, identical across arms); delivered and wrapper bytes are descriptive only. The "Composite ordinary-entry" residue is removed. |
| §6 | Expansion is demonstrated with a canary at the provider-request layer. The transform is frozen and reproduced byte-for-byte for the canary and each SSDP root. Injection is checked against `runtime-command` request 0. Six known-broken probes count against the activation criterion. The composite-ordinary residue is replaced by per-stratum recording. |
| §8 | Records revision 3. |

## 4. Response to the second independent check

| Finding | Disposition |
|---|---|
| **SC-A** — 2b recorded unconditionally; injection could satisfy 2a | The stakeholder answered Q1 and Q2 (decision record §6). 2b is now recorded as conditional on runtime-command evidence. Item 12 and the §3 row require `runtime-command` on at least one flash-class profile, and injection is never the only evidence. |
| **B1** — PASS possible with no `runtime-command` | Closed by the Q1 requirement in item 12 *Profile coverage* and in the §3 row. |
| **B2** — D3 not non-binding; scope ambiguous | Q3 confirms D3, narrowed to the 6.6 correct-selection bound only. The §4 text names that bound alone. The routing probes and T2/T3 sentinels keep their floors on deterministic entry. Criterion 16 gets its explicit supersession (decision record §6; workplan marker). |
| **B3** — false-activation and predicate-false-firing floors dropped | Q4 retains them. They are stated as floors in item 12, §3 and §4, and in overlay item 5. Predicate false-firing is measured on deterministic entry. Criterion 13's false-activation clause is restated in overlay item 4. |
| **B4** — delivery record ill-defined, not tamper-evident | Proof is the observer's hash-linked request 0, checked under a per-runtime frozen delivery transform. This handles OMP's frontmatter stripping and embedded prompt. Runtime and adapter records only corroborate. A runtime without the observer is claim-scoped inadmissible for this stratum, which covers the Claude Code case where there is no expansion event. |
| **B5** — contradictory byte accounting | There is one metric, the unchanged 6.6 metric, applied identically to all arms. Delivered and wrapper bytes are descriptive only. |
| **B6** — ordinary new-class measurement unrealized | Item 12 requires at least 3 ordinary episodes per arm per new class, report-only (D2). |
| **G1** — tautological activation row | The denominator is now every declared deterministic run, including inadmissible ones. |
| **G2** — injection undefined across layers; Codex | Injection is defined at the provider-request layer against the same runtime's demonstrated `runtime-command` request 0. A runtime with no demonstrated command delivery cannot use injection. |
| **G3** — Stage A static-margin basis | Unchanged, because the byte metric is unchanged. The workplan *Static pre-measurement* bullet carries a marker. |
| **G4** — attribution and labelling | Every attribution is now stakeholder-quoted: the quote is restored verbatim ("alwasy [sic]"); 2b keeps "If that works"; "approved the plan" is replaced by the verbatim instruction; Q1–Q4 are quoted. The derivations are labelled at each use: D1 in item 12, D2 in item 12 and the overlay, and D4 is reflected in the retained floors. |
| **G5** — D4 vs scope; wrong-root grouping | Owner false activation and the Q4 floors apply across strata. Doctrine floors are deterministic-only. Ordinary runs are reported in four groups (no selection, wrong root, admissible root, prose-instructed), with every critical failure listed by group. |
| **G6** — unmarked workplan locations; header | Markers are added at: the I66-2 map row, §11.3 non-selection placement-miss, §11.3 *Route*, §11.5 selection non-inferiority, §11.5 false-activation bounds, §11.5 composite runs, criterion 14, criterion 16 and *Static pre-measurement*. A 2026-10-04 decision entry is added to the header. |
| **G7** — requalification after a harness-caused failure | Requires a new profile key, a fresh §6 pre-run check and a fresh full campaign. The failed campaign stays on record. |
| **Minor** — "each of which" | Reworded: the deterministic *stratum* must meet the §2 minimums. |
| **Minor** — composite-ordinary residue | Removed from contract §4 and §6. The workplan §11.5 sentence carries a marker. |
| **Minor** — stakeholder record status | Updated. |
| **Minor** — README overstates the probe | README now says OMP *RPC mode* (interactive UI untested) and Claude Code *print mode* (interactive untested). |
| **Revision-1 m2** — untracked closeout record | Still uncommitted, and labelled as such. Committing it is for the stakeholder. |

## 5. Questions for the fresh independent check
1. Is the request-0 delivery proof well defined and realizable with the existing observer for OMP RPC mode? The adapter currently launches print mode.
2. Do the overlay's markers and named thresholds now leave no contradictory unmarked workplan statement?
3. Is any stakeholder attribution still beyond the recorded words?
4. Does any route remain for passing the activation criterion without a runtime's own command loading the skill on a flash-class profile?

## 6. Still blocked until both checks pass
- adapter changes (OMP RPC mode, the observer request-0 delivery check, transform freezing);
- profile freezes;
- the §6 pre-run check;
- fresh fixtures;
- any qualification run.
