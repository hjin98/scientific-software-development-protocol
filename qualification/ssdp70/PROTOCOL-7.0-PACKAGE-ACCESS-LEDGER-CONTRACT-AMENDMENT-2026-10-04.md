---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 14
status: revision 14 drafted on the stakeholder's adoption and confirmations; fresh independent check required (contract and workplan §0.1 entry and markers) together with fresh independent D3 acceptance of the package-access ledger decision revision 8
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 14)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision accounts process-executed package reads in a supervisor record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** The stakeholder authorized the bounded D3 repair of the process/file-access observation gap, asked for the recommended resolution of C-4 to proceed, applied the recommendations for the four open decisions, and confirmed the dispositions recorded in `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` (including its second, third and fourth rounds of confirmations). The two recorder choices (R-op) are confirmed. The stakeholder adoption is not an independent acceptance, and this amendment is a drafted proposal until independently checked.
- **History.** Revisions 9 (`8d04088`), 10 (`3469e83`), 11 (`ff5fcb7`) and 12 (`d56eda8`) each received independent NO-PASS; the reports are `PACKAGE-ACCESS-LEDGER-INDEPENDENT-CHECK-D3-REV3-AND-CONTRACT-REV9-2026-10-04.md`, `…-REV4-AND-CONTRACT-REV10-…`, `…-REV5-AND-CONTRACT-REV11-…` and `…-REV6-AND-CONTRACT-REV12-…` in this directory (the first review is `PACKAGE-ACCESS-LEDGER-INDEPENDENT-REVIEW-D3-REV1-2026-10-04.md`), and their per-finding response tables are not repeated here. Revision 12 simplified the mechanism; the fourth check found only undefined primitives, inconsistencies and undeclared effects. **Revision 13 changes definitions, clarifications and declarations only, by the stakeholder's instruction to stop changing the mechanism.**
- **Authorship.** The same context authored the first independent review that raised C-4, N-1 and N-2, D3 revisions 3 to 8, and contract revisions 9 to 14. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 received independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Revision 14 changes those bytes (a new §1 item 13, pointers in items 4, 5, 11 and §6, §8) and so requires a fresh check even though it is additive.

## 2. Current contract and workplan changes

| Location | Change |
|---|---|
| Front matter `status` | Revision 14 pending fresh independent check. |
| §1 item 4 | Derived event kind `package_access` (supervisor-owned); the owner-read sentence names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a declared reduction, lossless for the item 13 oracles, of the kernel stream; the completeness map maps it, with its heartbeat records, to the `package_access` event; rows, loss and timing-loss conditions and counts must reconcile. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the governing decision's document path, commit and SHA-256 as recorded by its independent acceptance. |
| §1 item 13 (new) | Ledger profile or no ledger; the `package_access` event and payload; claim scope (owner floor by pointer to D3 item 4a); campaign effect; **replacement (mandatory, the replacement is the scored run; byte-question between-arm bound; no owner-floor cap)**; **T7: unknown-value rule and an owner-floor-only rerun**; rehearsal gate; Record pointer. The declared changes in effect, with direction, are listed in §8. The D3 decision owns the attribution, owner-class supply, windows and probe rules; §6 and item 13 are one joint-change set with it. |
| §6 | One paragraph: the ledger demonstrations and the D3 acceptance-boundary probe set (all of its cases), by pointer. |
| §8 | Revision 8's stale "no independent check" sentence corrected; a revision 14 entry declaring six effects with direction ((a) to (f)) and the acceptance-process values. |
| Workplan §0.1 | New entry for the package-access ledger (authority, pending status, observation-boundary reading, the owner-floor statement, pointers). Overlay revision number assigned by the Review. |
| Workplan markers | Six, each pointing at §0.1: the "Root-selection evidence contract" bullet, the "Trusted runtime-observation contract" bullet, the §11.4 owner-false-activation definition (the defining site), the §11.5 reuse site, the T7 replication bullet and the fixed-cost backstop line. No other workplan text, threshold or overlay item changed. |

## 3. Response to the independent check of revision 13 (`16571a1`)

| Finding | Disposition |
|---|---|
| **A-1** — quantum under-defined; a single long owner line reached it | Stakeholder-confirmed rule: distinct owner lines are counted once per result; positive needs at least 256 bytes across at least two distinct owner lines; one line however long, the same line seven times, and chunks below the quantum across several results are minor exposure (UNRESOLVED, replaceable). D3 4a, boundary (w); decision record round 4. |
| **A-2** — §6 range (a) to (v) | §6 and §2 say "all of its cases" with no range. |
| **A-3** — owner-floor replacement bound contradicted the record | Dropped: no campaign-wide cap on replaced owner-floor runs beyond the per-case cap; the byte question keeps its between-arm bound. |
| **A-4** — T7 owner-floor replacement contradiction | A T7 run UNRESOLVED on the owner floor may be rerun solely to resolve the owner floor, outside the median; the original stays an unknown value for the burden route (item 13 *T7*; effect (e)). |
| **B-1 to B-4, B-10 to B-13, B-16** | Claim-scope pointer, amendment record and §8 wording, D3 open-items and parents wording, event fields (`owner_minor_exposure`, quantum), added-pairs wording and workplan marker wording fixed; the no-ledger exception declared as effect (f); round 2 (d) marked superseded. |
| **B-5 to B-9, B-14, B-15, B-17** | Request-position pairing verification and the clock residual stated in D3; rehearsal forms added (R2 as a parallel tool action, pairing mismatch, copies in any encoding); replacement eligibility after adjudication of other criteria and the non-replaceable non-T7 burden slot with positive owner evidence stated and counted in the gate arithmetic; code gaps and the common-honest-forms list recorded as D4 conditions in the D3 revision 8 note. |

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. The fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule.
- **Score any owner open as access (revision 4) or a targeted open (revision 5).** Rejected after two independent NO-PASS checks: honest scans and scan-then-load false-FAIL, and the named-path test is co-occurrence.
- **A supervisor sentinel at each request for event ordering.** Not available without a new edge: the supervisor is not in the request path. The in-queue heartbeat gives the same ordering without one.
- **Decide replacement semantics or the rehearsal target without a stakeholder decision.** Rejected; recorded in the stakeholder decision record, with the target instantiated only once N is frozen.

## 5. Stakeholder decisions (adopted and confirmed; record `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md`)

1. **Replacement runs.** Mandatory replacement (§5 cap) of observation-inexact originals on the owner floor and non-T7 burden routes, after the original's other criteria are adjudicated; the replacement is the scored run; originals retained and disclosed, outcomes not counted; a positive owner read before R2 never replaced, nor a non-T7 burden run with positive owner evidence and inexact bytes; T7 follows the unknown-value rule with an owner-floor-only rerun; a byte-question between-arm bound frozen before runs with fail-closed default; no campaign-wide cap on owner-floor replacements.
2. **Rehearsal-gate target.** Structural gate with reported rates and verdicts; probability at least 0.8 that no unresolved run leaves the owner floor or a burden route non-PASS, instantiated by the independent checker from the frozen run count N.
3. **Positive evidence.** A native read or owner content of at least 256 bytes across at least two distinct owner lines that reached the model before R2 is a FAIL even when other observation is inexact; minor exposure and an owner open with no such evidence that is not provably post-R2 are UNRESOLVED and replaceable. (Rounds two and three: a named-but-unshown open is UNRESOLVED; no read-to-access change; the quantum.)
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

- Independent acceptance of D3 revision 8 and of this amendment together.
- The frozen run count N and the instantiated gate target.
- D4 realization of revision 8 (the lists are in the D3 revision 6, 7 and 8 notes: heartbeat and bracketed rows, candidate windows, provably-post-R2 test, owner-class supply, the split exactness fields, the `package_access` event, the native `owner_reads` basename rule, the T7 unknown-value rule and replacement bookkeeping, the rehearsal).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
