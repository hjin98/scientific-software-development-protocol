---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 12
status: revision 12 drafted on the stakeholder's adoption and confirmations; fresh independent check required (contract and workplan §0.1 entry and markers) together with fresh independent D3 acceptance of the package-access ledger decision revision 6
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 12)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision accounts process-executed package reads in a supervisor record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** The stakeholder authorized the bounded D3 repair of the process/file-access observation gap, asked for the recommended resolution of C-4 to proceed, applied the recommendations for the four open decisions, and confirmed the dispositions recorded in `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` (including its second round of confirmations for revision 6). The two recorder choices (R-op) are confirmed. The stakeholder adoption is not an independent acceptance, and this amendment is a drafted proposal until independently checked.
- **History.** Revisions 9 (`8d04088`), 10 (`3469e83`) and 11 (`ff5fcb7`) each received independent NO-PASS; the findings and their repairs are in `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV3-AND-CONTRACT-REV9-20261004T231706Z.md`, `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV4-AND-CONTRACT-REV10-20261004T234050Z.md` and `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV5-AND-CONTRACT-REV11-20261004T235855Z.md` and in git history; their per-finding response tables are not repeated here. Revision 12 **simplifies**: each earlier repair added mechanism (candidate windows, targeted-access classification, named-path matching, first-open placement) and each produced new blockers, so owner positive evidence is now content that reached the model, and timing decides only a conservative UNRESOLVED-versus-PASS-eligible test.
- **Authorship.** The same context authored the first independent review that raised C-4, N-1 and N-2, D3 revisions 3 to 6, and contract revisions 9 to 12. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 received independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Revision 12 changes those bytes (a new §1 item 13, pointers in items 4, 5, 11 and §6, §8) and so requires a fresh check even though it is additive.

## 2. Current contract and workplan changes

| Location | Change |
|---|---|
| Front matter `status` | Revision 12 pending fresh independent check. |
| §1 item 4 | Derived event kind `package_access` (supervisor-owned); the owner-read sentence names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a declared reduction, lossless for the item 13 oracles, of the kernel stream; the completeness map maps it, with its heartbeat records, to the `package_access` event; rows, loss and timing-loss conditions and counts must reconcile. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the governing decision's document path, commit and SHA-256 as recorded by its independent acceptance. |
| §1 item 13 (new) | Ledger profile or no ledger; the `package_access` event and payload; claim scope; the **owner floor on an owner read (content that reached the model), no change in effect from rev 8**; campaign effect; replacement (disparity bound covers burden comparisons); **T7 and burden routes: unknown-value rule (the one declared change in effect, ledger profiles only)**; rehearsal gate; Record pointer. The D3 decision owns the attribution, owner-class supply, windows and probe rules; §6 and item 13 are one joint-change set with it. |
| §6 | One paragraph: the ledger demonstrations and the D3 acceptance-boundary probe set (cases (a) to (v)), by pointer. |
| §8 | Revision 8's stale "no independent check" sentence corrected; a revision 12 entry declaring the one change in effect and the two acceptance-process values. |
| Workplan §0.1 | New entry for the package-access ledger (authority, pending status, observation-boundary reading, the owner-floor statement, pointers). Overlay revision number assigned by the Review. |
| Workplan markers | At the "Root-selection evidence contract" bullet, the "Trusted runtime-observation contract" bullet, the §11.4 owner-false-activation definition (the defining site) and the §11.5 reuse site, each pointing at §0.1. No other workplan text, threshold or overlay item changed. |

## 3. Response to the independent check of revision 11 (`ff5fcb7`)

| Finding | Disposition |
|---|---|
| **D3-R5-1** — a pre-R2 scan then a legitimate post-R2 owner load became a definite, non-replaceable FAIL | Access is no longer placed at a file's first open. Positive evidence is owner content placed at its own result sequence; a scan that shows nothing leaves the floor UNRESOLVED and replaceable and the later load is an owner-load hit (D3 4a, boundary (m), (n)). |
| **D3-R5-2** — shown owner content not positive evidence unless attributable to one copy | Owner-class supply: whole owner lines at least the floor long identify the owner class regardless of path form or copy; the premise is stated at whole-line granularity (0 of 242 lines; 27 shared sub-line runs exist, so no sub-line claim) (D3 4a, 6). |
| **D3-R5-3** — named-path test is co-occurrence and undefined | Removed. A command that merely names an owner path affects nothing (boundary (n)). |
| **D3-c1 to c7** | Clock divergence against a per-run baseline tainting later brackets; edge cases (no earlier request, retries, empty windows, event time as kernel generation); owner-load hits need no exactness; timing only decides the provably-post-R2 test; stale references fixed; rehearsal forms added (`PROTOCOL_VERSION` via non-literal paths, retries, scan then load, name-without-open) (D3 5, 4a, 8). |
| **C-R11-1** — §6 encoded the defective rule and restated D3 | §6 is a pointer to the D3 acceptance boundary and is part of the joint-change set (item 13, §6). |
| **C-R11-2** — T7 reading undefined | Unknown-value rule: an observation-inexact burden run is not replaced; its bytes are unknown and its owner-read mode unobserved, which counts as the mixed-mode pair-addition trigger; the median bound resolves only under the adversarial assignment (candidate unbounded above, comparator zero), else UNRESOLVED. Declared in §8 as the one change in effect. |
| **C-R11-3** — stale cross-references | This record is rewritten; the superseded per-round tables are routed to the reports and git history. |
| **W-R11-1, W-R11-2** | §0.1 names revision 6 and contract revision 12; marker added at the §11.4 defining site. |
| **Reviewer recommendations** | The disparity bound now covers burden comparisons (2.0x-versus-6.5 and class-iii), a recorder choice recorded in the decision record; no campaign-wide cap on replaced owner-unresolved runs beyond the per-case cap (recorder choice, to be reconsidered by the stakeholder if the rehearsal shows many UNRESOLVED runs). |

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. The fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule.
- **Score any owner open as access (revision 4) or a targeted open (revision 5).** Rejected after two independent NO-PASS checks: honest scans and scan-then-load false-FAIL, and the named-path test is co-occurrence.
- **A supervisor sentinel at each request for event ordering.** Not available without a new edge: the supervisor is not in the request path. The in-queue heartbeat gives the same ordering without one.
- **Decide replacement semantics or the rehearsal target without a stakeholder decision.** Rejected; recorded in the stakeholder decision record, with the target instantiated only once N is frozen.

## 5. Stakeholder decisions (adopted and confirmed; record `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md`)

1. **Replacement runs.** Bounded replacement (§5 cap) of observation-inexact originals only; originals retained and disclosed with per-arm and per-form counts; a positive owner read before R2 never replaced; burden runs follow the unknown-value rule; per-arm disparity bound frozen before runs with fail-closed default, covering burden comparisons.
2. **Rehearsal-gate target.** Structural gate with reported rates and verdicts; probability at least 0.8 that no unresolved run leaves the owner floor or a burden route non-PASS, instantiated by the independent checker from the frozen run count N.
3. **Positive evidence.** Owner content that reached the model before R2 is a FAIL even when other observation is inexact; an owner open with no such evidence that is not provably post-R2 is UNRESOLVED and replaceable. (Second round: a named-but-unshown open is UNRESOLVED, not a FAIL; no read-to-access change.)
4. **Observation boundary.** The supervisor ledger is admissible for supervisor-owned inputs alongside the provider-control observer.
5. **C-4.** The contract-amendment route (this revision).

Still open: the run count N and F-5.

## 6. Questions for the fresh independent check

1. Does owner-class supply (whole owner lines at least the floor) identify owner reads soundly on the shipped packages, and is placing a positive read at its result sequence free of timing assumptions? Can a deliberate pre-R2 owner read evade it (hidden or transformed output) other than by landing in UNRESOLVED, and is the resulting detection hole adequately bounded?
2. Is the provably-post-R2 test conservative on every path (late drain, heartbeat gap, wall-clock step and baseline divergence, in-flight or background opens, opens after the last request, retries, auxiliary requests, parallel calls), so that timing imprecision can produce UNRESOLVED but never a FAIL or a false PASS-eligible?
3. Is route (iii) free of the shared-block failure, and does per-file explanation lose no consumption?
4. Is the `package_access` event derivable and recomputable from retained artifacts alone, and does the completeness map account for the ledger artifact and its heartbeat records without a loophole? Is the fold per (file, flags, interval) lossless for the owner-open windows and bounded?
5. Can item 13 create any path to PASS when observation is not exact, when positive evidence exists, or when the gate target is unrecorded? Is the campaign effect a faithful clarification of item 7?
6. Is the T7 unknown-value rule sound and complete (pair addition, mixed-mode trigger, adversarial assignment, median definition) and is it the only declared change in effect? Is the replacement rule exploitable (selection effect, positive evidence, overflow as a subject-reachable channel, fail-closed default)?
7. Are the workplan §0.1 entry and the four markers consistent with the overlay convention, and do revision 8's criteria, family rule and activation-strata bytes stay unchanged in effect? Do all cross-references in D3, the contract, this record and the workplan resolve?

## 7. Still blocked

- Independent acceptance of D3 revision 6 and of this amendment together.
- The frozen run count N and the instantiated gate target.
- D4 realization of revision 6 (the list is in the D3 revision 6 note: heartbeat and bracketed rows, candidate windows, provably-post-R2 test, owner-class supply, the split exactness fields, the `package_access` event, the native `owner_reads` basename rule, the T7 unknown-value rule and replacement bookkeeping, the rehearsal).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
