---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 13
status: revision 13 drafted on the stakeholder's adoption and confirmations; fresh independent check required (contract and workplan §0.1 entry and markers) together with fresh independent D3 acceptance of the package-access ledger decision revision 7
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 13)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision accounts process-executed package reads in a supervisor record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** The stakeholder authorized the bounded D3 repair of the process/file-access observation gap, asked for the recommended resolution of C-4 to proceed, applied the recommendations for the four open decisions, and confirmed the dispositions recorded in `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` (including its second and third rounds of confirmations). The two recorder choices (R-op) are confirmed. The stakeholder adoption is not an independent acceptance, and this amendment is a drafted proposal until independently checked.
- **History.** Revisions 9 (`8d04088`), 10 (`3469e83`), 11 (`ff5fcb7`) and 12 (`d56eda8`) each received independent NO-PASS; the reports are `PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-D3-REV3-AND-CONTRACT-REV9-2026-10-04.md`, `…-REV4-AND-CONTRACT-REV10-…`, `…-REV5-AND-CONTRACT-REV11-…` and `…-REV6-AND-CONTRACT-REV12-…` in this directory (the first review is `PACKAGE-ACCESS-LEDGER-INDEPENDENT-REVIEW-D3-REV1-2026-10-04.md`), and their per-finding response tables are not repeated here. Revision 12 simplified the mechanism; the fourth check found only undefined primitives, inconsistencies and undeclared effects. **Revision 13 changes definitions, clarifications and declarations only, by the stakeholder's instruction to stop changing the mechanism.**
- **Authorship.** The same context authored the first independent review that raised C-4, N-1 and N-2, D3 revisions 3 to 7, and contract revisions 9 to 13. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 received independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Revision 13 changes those bytes (a new §1 item 13, pointers in items 4, 5, 11 and §6, §8) and so requires a fresh check even though it is additive.

## 2. Current contract and workplan changes

| Location | Change |
|---|---|
| Front matter `status` | Revision 13 pending fresh independent check. |
| §1 item 4 | Derived event kind `package_access` (supervisor-owned); the owner-read sentence names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a declared reduction, lossless for the item 13 oracles, of the kernel stream; the completeness map maps it, with its heartbeat records, to the `package_access` event; rows, loss and timing-loss conditions and counts must reconcile. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the governing decision's document path, commit and SHA-256 as recorded by its independent acceptance. |
| §1 item 13 (new) | Ledger profile or no ledger; the `package_access` event and payload; claim scope (owner floor by pointer to D3 item 4a); campaign effect; **replacement (mandatory, the replacement is the scored run; per-question frozen bounds)**; **T7: unknown-value rule**; rehearsal gate; Record pointer. The declared changes in effect, with direction, are listed in §8. The D3 decision owns the attribution, owner-class supply, windows and probe rules; §6 and item 13 are one joint-change set with it. |
| §6 | One paragraph: the ledger demonstrations and the D3 acceptance-boundary probe set (cases (a) to (v)), by pointer. |
| §8 | Revision 8's stale "no independent check" sentence corrected; a revision 13 entry declaring four effects with direction and the acceptance-process values. |
| Workplan §0.1 | New entry for the package-access ledger (authority, pending status, observation-boundary reading, the owner-floor statement, pointers). Overlay revision number assigned by the Review. |
| Workplan markers | At the "Root-selection evidence contract" bullet, the "Trusted runtime-observation contract" bullet, the §11.4 owner-false-activation definition (the defining site) and the §11.5 reuse site, each pointing at §0.1. No other workplan text, threshold or overlay item changed. |

## 3. Response to the independent check of revision 12 (`d56eda8`)

| Finding | Disposition |
|---|---|
| **D3-B1** — request position in the trace undefined | D3 item 5 freezes the primitive (k-th subject-conversation request paired with the k-th assistant turn; position = first event of that turn's tool calls and results; unpairable means start of trace; the window follows trace order). |
| **D3-B2** — request stamps not monotone; bracket ends undefined | Non-decreasing stamps consistent with the heartbeat baseline are required (else timing loss); a heartbeat before launch and after the last possible event is required (else timing loss). |
| **D3-B3** — error-status and matching granularity | Owner-class supply counts error-status results (byte-supply exclusion only); whole owner lines as substrings of output lines, each at least the 48-byte line floor, total at least the 256-byte quantum; below it is minor exposure (UNRESOLVED, replaceable). |
| **D3-B4, B5** — stale statements; rehearsal forms and premise checks | Parents line, open-items bullet, twin statement and figures corrected; rehearsal adds same-response load, parallel calls, keyword grep, `cat <owner>; false`, and mechanical premise checks re-run on package regeneration; reopen fallback pre-registered. |
| **D3-F3 to F5** | Same-response risk named in the gate and reopen triggers; timing required only when an owner open exists; "every owner row". |
| **C-B1** — burden-route contradiction | T7 is the unknown-value route; non-T7 burden runs are replaced; "never a lower-bound total" is reconciled with the route-level unknown-value bound (item 13, *Claim scope*, *Replacement*, *T7*). Decision record round one is marked superseded to that extent. |
| **C-B2** — undeclared effects | Four effects declared with direction in §8. |
| **C-B3** — rule restated | Owner floor in item 13 is a pointer to D3 item 4a; D3 item 8 points to the contract for the target, aggregation and replacement. |
| **C-B4** — hygiene | Reports committed in this directory and cited by repository path; item 13 lead-in restructured; bounds defined per question. |
| **W-B1, W-B2** | Workplan sentence fixed; markers added at the T7 replication bullet and the fixed-cost backstop line. |
| **Stakeholder confirmations** | The five items of the decision record's third round. |

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. The fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule.
- **Score any owner open as access (revision 4) or a targeted open (revision 5).** Rejected after two independent NO-PASS checks: honest scans and scan-then-load false-FAIL, and the named-path test is co-occurrence.
- **A supervisor sentinel at each request for event ordering.** Not available without a new edge: the supervisor is not in the request path. The in-queue heartbeat gives the same ordering without one.
- **Decide replacement semantics or the rehearsal target without a stakeholder decision.** Rejected; recorded in the stakeholder decision record, with the target instantiated only once N is frozen.

## 5. Stakeholder decisions (adopted and confirmed; record `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md`)

1. **Replacement runs.** Mandatory replacement (§5 cap) of observation-inexact originals on the owner floor and non-T7 burden routes; the replacement is the scored run; originals retained and disclosed, outcomes not counted; a positive owner read before R2 never replaced; T7 follows the unknown-value rule; per-question replacement bounds frozen before runs with fail-closed default.
2. **Rehearsal-gate target.** Structural gate with reported rates and verdicts; probability at least 0.8 that no unresolved run leaves the owner floor or a burden route non-PASS, instantiated by the independent checker from the frozen run count N.
3. **Positive evidence.** A native read or owner content of at least the 256-byte quantum that reached the model before R2 is a FAIL even when other observation is inexact; minor exposure and an owner open with no such evidence that is not provably post-R2 are UNRESOLVED and replaceable. (Rounds two and three: a named-but-unshown open is UNRESOLVED; no read-to-access change; the quantum.)
4. **Observation boundary.** The supervisor ledger is admissible for supervisor-owned inputs alongside the provider-control observer.
5. **C-4.** The contract-amendment route (this revision).

Still open: the run count N and F-5.

## 6. Questions for the fresh independent check

1. Does owner-class supply (whole owner lines of at least the line floor, 256-byte quantum, error-status results included) identify owner reads soundly on the shipped packages, and is placing a positive read at its result sequence free of timing assumptions? Can a deliberate pre-R2 owner read evade it (hidden or transformed output) other than by landing in UNRESOLVED, and is the resulting detection hole adequately bounded?
2. Is the provably-post-R2 test conservative on every path, now with the request-position primitive and request-stamp monotonicity (late drain, heartbeat gap, wall-clock step and baseline divergence, in-flight or background opens, opens after the last request, retries, auxiliary requests, parallel calls), so that timing imprecision can produce UNRESOLVED but never a FAIL or a false PASS-eligible?
3. Is route (iii) free of the shared-block failure, and does per-file explanation lose no consumption?
4. Is the `package_access` event derivable and recomputable from retained artifacts alone, and does the completeness map account for the ledger artifact and its heartbeat records without a loophole? Is the fold per (file, flags, interval) lossless for the owner-open windows and bounded?
5. Can item 13 create any path to PASS when observation is not exact, when positive evidence exists, or when the gate target is unrecorded? Is the campaign effect a faithful clarification of item 7?
6. Are the four declared effects complete and correctly directed, is the T7 unknown-value rule sound and complete (pair addition, mixed-mode trigger, adversarial assignment, median definition), and are replacement (mandatory, scored run) and its per-question bounds well defined for every burden route? Is the replacement rule exploitable (selection effect, positive evidence, overflow as a subject-reachable channel, fail-closed default)?
7. Are the workplan §0.1 entry and the six markers consistent with the overlay convention, and do revision 8's criteria, family rule and activation-strata bytes stay unchanged in effect? Do all cross-references in D3, the contract, this record and the workplan resolve?

## 7. Still blocked

- Independent acceptance of D3 revision 7 and of this amendment together.
- The frozen run count N and the instantiated gate target.
- D4 realization of revision 7 (the list is in the D3 revision 6 and 7 notes: heartbeat and bracketed rows, candidate windows, provably-post-R2 test, owner-class supply, the split exactness fields, the `package_access` event, the native `owner_reads` basename rule, the T7 unknown-value rule and replacement bookkeeping, the rehearsal).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
