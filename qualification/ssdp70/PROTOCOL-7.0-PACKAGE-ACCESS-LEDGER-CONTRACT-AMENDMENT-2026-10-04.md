---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 11
status: revision 11 drafted on the stakeholder's adoption and confirmations; fresh independent check required (contract and workplan §0.1 entry and markers) together with fresh independent D3 acceptance of the package-access ledger decision revision 4
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 11)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision's owner-read and byte accounting for process-executed package reads is a supervisor accounting record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** The stakeholder authorized the bounded D3 repair of the process/file-access observation gap, asked for the recommended resolution of C-4 to proceed, and then instructed that the recommendations for the four open decisions be applied. `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` records that adoption (replacement runs, gate target, positive evidence, observation boundary, and the contract-amendment route for C-4). Two values are recorder choices (R-op) the stakeholder has confirmed: the per-arm inexact-rate disparity bound frozen before runs with fail-closed default, and the 0.8 campaign target. This amendment changes no outcome floor, exposure minimum, fixture or case; it adds those two acceptance-process values and makes one declared change in effect (owner floor scored on a targeted owner access in ledger profiles). The stakeholder adoption is not an independent acceptance.
- **History.**
  - Revision 9 (`8d04088`): independent NO-PASS for the contract plus workplan marker and for D3 revision 3, recorded in `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV3-AND-CONTRACT-REV9-20261004T231706Z.md`. No Serious Challenge; blockers C-1 to C-6, W-1, W-2 and D3-1 to D3-3. It confirmed that revision 9 adds no floor or threshold and leaves revision 8 unchanged in effect.
  - Revision 10 (`3469e83`, with the stakeholder decisions applied): independent NO-PASS for D3 revision 4 and the contract, PASS for the workplan entry and markers, recorded in `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV4-AND-CONTRACT-REV10-20261004T234050Z.md`. No Serious Challenge; blockers D3-B1, D3-B2, C-B1 to C-B3 and conditional W-1.
  - Revision 11 (this file) repairs them on the stakeholder's confirmation (decision record, *Confirmations and amendments*).
- **Authorship.** The same context authored the earlier independent review that raised C-4, N-1 and N-2, the D3 revision 3 and 4 amendments, and contract revisions 9 and 10. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 received independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Revision 11 changes those bytes (a new §1 item 13, pointers in items 4, 5, 11 and §6, §8) and so requires a fresh check even though it is additive.

## 2. Contract and workplan changes

| Location | Change |
|---|---|
| Front matter `status` | Now revision 11 pending fresh independent check. |
| §1 item 4 | Derived event kind `package_access` (supervisor-owned); the owner-read sentence names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a declared reduction, lossless for the item 13 oracles, of the kernel stream (not "raw"); the completeness map maps it, with its heartbeat records, to the `package_access` event and the rows, loss and timing-loss conditions and counts must reconcile. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the governing decision's document path, commit and SHA-256 as recorded by its independent acceptance. |
| §1 item 13 | Ledger profile or no ledger; the `package_access` event and payload (brackets, timing-loss conditions, three exactness values, `owner_read_observed`); claim scope with positive evidence never suppressed; owner-access time; campaign effect; rehearsal gate per arm and per question; Record pointer. |
| §6 | A paragraph listing the ledger demonstrations, the known-broken probes and the known-good probes, including the pre-R2 owner open shown later and drained late. |
| §8 | Revision 8's stale "no independent check" sentence corrected; a revision 11 entry that declares the read-to-access change and the two acceptance-process values. |
| Workplan §0.1 | New entry for the package-access ledger (authority, pending status, observation-boundary reading, pointers). Overlay revision number assigned by the Review. |
| Workplan markers | The "Root-selection evidence contract" bullet and the "Trusted runtime-observation contract" bullet carry markers pointing at §0.1. No other workplan text, threshold or overlay item changed. |

The contract does not restate the D3 attribution rules (supply routes, phase split, mechanical bracket, exactness questions, rehearsal gate). Their single semantic owner is the D3 decision; item 13 binds the contract to its accepted revision by commit and SHA-256 and makes a change to either a joint change.

## 3. Response to the independent check of revision 9

| Finding | Disposition |
|---|---|
| **D3-1** — owner-access bound maps to the latest consistent turn; items 5 and 6 contradict | Event time is bracketed mechanically (heartbeat source in the same kernel queue; lower edge before the earlier write, upper edge after the later write), so lag only widens a bracket. The bound is the earliest consistent turn; a request stamp inside the bracket is turn-ambiguous and treated as ambiguous R2 timing. Item 5's skew sentence is replaced. Timing loss makes the owner-access question not exact. D3 items 5 and 6; contract item 13 *Owner-access time* and §6 timing-loss probes. |
| **D3-2** — gate covers only the owner question and only the 7.0 package | D3 item 8 and contract item 13 *Rehearsal gate* cover the byte, owner-access and owner-load questions and each arm's package shape (7.0: 238/63/38/213 files/distinct/twin groups/twinned; 6.6: 212/62/37/187; 6.5: 198/60/35/173). The gate is structural plus reported, because a small per-run rate cannot be shown statistically (about 1,500 clean runs bound it at 0.2%). Common honest forms are made exact by D3 route (iii) (whole-file same-turn delivery). The target remains a stakeholder decision. |
| **D3-3 / C-3** — positive owner evidence nulled when inexact | Positive evidence is never suppressed: the owner-access question depends only on the ledger and timing, any owner open is access whether or not explained, and a pre-R2 sequence is a FAIL whatever the other exactness values. `owner_read_exact` splits into `owner_access_exact` (false activation) and `owner_load_exact` (hits need demonstrated supply). `owner_read_observed` is always published. **Deviation to check:** this goes beyond the minimum repair, because it makes the zero-tolerance owner floor independent of twin-path attribution. It scores *any* post-request owner open as access, so a runtime that rescans owner copies mid-run would produce false accesses; the multi-turn rehearsal is the only test of that. |
| **D3-n1 to D3-n3** | Recorded as premises and reopen triggers in D3 (no non-owner file carries owner material, verified 0 of 242 owner lines of at least 48 bytes; over-count is conservative on the candidate but inflates the 6.5/6.6 denominators; directory marks equal per-inode marks only for one fresh copy behind one read-only bind). |
| **C-1** — wrong section | Owner floor and ambiguous-R2 clause are in §4; corrected. |
| **C-2** — replacement self-contradiction | *Campaign effect* now says plainly: an unresolved original keeps the criterion non-PASS; replacements never remove it; until replacement semantics are decided, no rescue. |
| **C-4** — probe filed as a rejection | Moved to the known-good list with the expected result: an exact owner-access observation whose earliest sequence precedes R2, failing the probe-local owner criterion as an expected integrity failure. |
| **C-5** — Record pointer, §8, binding | Record pointer added to item 13; §8 updated and revision 8's stale sentence corrected; item 11 and item 13 bind the D3 decision by path, commit and SHA-256. |
| **C-6** — inherits D3-2 | Closed with D3-2. |
| **Minor** — "raw observable" | Item 5 now names the ledger a declared lossless-for-oracle reduction. |
| **W-1** — marker bypassed §0.1 | §0.1 entry added; markers point at it; overlay revision number left to the Review. |
| **W-2** — "only" in the trusted-observation bullet | Reconciled in the §0.1 entry and a marker on that bullet: the restriction concerns model-facing runtime fields; the supervisor ledger observes supervisor-owned inputs and adds no cross-principal edge. Stakeholder confirmation requested (§5). |
| **D4-1 to D4-4** | Not contract text. Listed in the D3 revision 4 note as D4 work after acceptance (native `owner_reads` basename rule; `package_access` event and completeness entry; enforcement of a recorded rehearsal target at admission; claim detection by substring). |

## 3a. Response to the independent check of revision 10

| Finding | Disposition |
|---|---|
| **D3-B1** — timing loss could become a definite non-replaceable FAIL; mapping not the earliest consistent point | D3 item 5 replaces the single earliest-turn mapping by **candidate windows** of trace events (start: first event after the last request stamped before the bracket's lower edge; end: last event before the first request stamped after its upper edge; end of trace if none; timing loss spans from request 0's first event to the end). An owner access is a **definite** pre-R2 FAIL only if its window ends before R2; a window containing R2 is ambiguous R2 timing. Brackets are widened by the clock tolerance because the observer stamps with `CLOCK_REALTIME`. Covers in-flight and background opens and opens after the last request. |
| **D3-B2** — any owner open is access, giving false FAILs on honest scans | Stakeholder-confirmed disposition: positive evidence is a **targeted** owner access (native event; owner content supplied; or owner path named in a tool action delivered in the open's window). Untargeted owner opens are not positive evidence, leave the owner-access question `UNRESOLVED` and replaceable, and are published as `owner_untargeted_opens`. Item 8 reports verdicts per form so scans show as an UNRESOLVED rate; reopen triggers name model-driven scans; acceptance boundary (q) to (u). The detection hole this opens is stated as a residual. |
| **C-B1** — T7 reading; gate target missed burden | Contract item 13 *Replacement* states the T7 reading; the gate target now covers each burden route. |
| **C-B2** — undeclared change in effect; "no threshold" inexact | Item 13 *Owner access* declares the read-to-access change (ledger profiles only); §8 and §1 now state one declared change in effect and two acceptance-process values (0.8 target, disparity bound), both stakeholder-confirmed. |
| **C-B3** — rule restated; recompute parameters missing | The contract paragraph is a pointer to D3; the `package_access` payload carries the frozen parameters (floor, clock tolerance, bracket-width bound, heartbeat period and gap bound, row bound, mark-lifetime bounds), the targeted/untargeted classification and the windows. |
| **W-1** — workplan owner-read wording | Marker added at the §11.5 "new-owner read before R2" bullet and a sentence in the §0.1 entry. |
| **D3 clarifications** | Per-file explanation and candidate-turn handling for route (iii) (item 6); overflow as a subject-reachable channel with replacement only on disclosed cause (residual, item 13); premise that the supervisor opens no package file while marks are live and marks outlive teardown (item 7); unique heartbeat names (item 5); request 0 as the first subject-conversation request, reconciled with contract item 12 (item 5); decisive parameters frozen before runs (item 6). |

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. Recorded as the fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule.
- **A supervisor sentinel at each request for event ordering.** Not available without a new edge: the supervisor is not in the request path. The in-queue heartbeat gives the same ordering without one.
- **Keep "any owner open is access" and add a verdict-level gate measure instead.** Not chosen: it leaves honest scans as non-replaceable FAILs and moves the cost to the gate.
- **Decide replacement semantics or the rehearsal target in the amendment without a stakeholder decision.** Rejected; now recorded in the stakeholder decision record, with the target instantiated only once N is frozen.

## 5. Stakeholder decisions (adopted and confirmed; record `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md`)

1. **Replacement runs.** Bounded replacement (§5 cap) of observation-inexact originals only; originals retained and disclosed with per-arm and per-form counts; a definite targeted owner access before R2 is never replaced; T7 observation-inexact runs use the pair-addition rule, not replacement. The per-arm disparity bound is frozen before runs with fail-closed default (confirmed R-op).
2. **Rehearsal-gate target.** Structural gate with reported rates and verdicts; probability at least 0.8 (confirmed R-op) that no unresolved run leaves an owner floor or a burden route non-PASS with replacement where available, instantiated by the independent checker from the frozen run count N.
3. **Positive evidence.** A definite targeted owner access before R2 is a FAIL even when other observation is inexact; untargeted owner opens are UNRESOLVED and replaceable.
4. **Observation boundary.** The supervisor ledger is admissible for supervisor-owned inputs alongside the provider-control observer.
5. **C-4.** The contract-amendment route (this revision).

Still open: the run count N and F-5.

## 6. Questions for the fresh independent check

1. Do candidate windows contain the true time on every path (late drain, heartbeat gap, wall-clock step, in-flight or background open, open after the last request, retries, auxiliary requests), and is the definite/ambiguous/post-R2 classification conservative without manufacturing definite FAILs?
2. Is the targeted-versus-untargeted owner-access rule sound: does it still catch a deliberate pre-R2 owner read (named, supplied, or whole-file delivered) while leaving honest scans UNRESOLVED, and is the residual detection hole adequately bounded by replacement caps and disclosure?
3. Is route (iii) (whole-file same-turn delivery) free of the shared-block failure that revision 2 repaired, and does it leave any opened file explained that the model has not wholly received?
4. Is the `package_access` event derivable and recomputable from retained artifacts alone, and does the completeness map account for the ledger artifact and its heartbeat records without a loophole?
5. Can item 13 create any path to PASS when observation is not exact, when positive evidence exists, or when the gate target is unrecorded? Is the campaign-effect sentence a faithful clarification of item 7 or a new floor?
6. Are the workplan §0.1 entry and the two markers consistent with the overlay convention, and do revision 8's criteria, family rule and activation-strata bytes stay unchanged in effect?
7. Is the replacement rule sound (selection effect, positive evidence, T7 pair-addition reading, overflow as a subject-reachable channel, fail-closed default), does the 0.8 target now cover burden, and is the declared read-to-access change in effect stated everywhere it must be (item 13, §8, workplan §0.1 and marker)? Do the two R-op values add anything the contract forbids?

## 7. Still blocked

- Independent acceptance of D3 revision 5 and of this amendment together.
- The frozen run count N and the instantiated gate target.
- D4 realization of revision 4 (heartbeat and bracketed rows, candidate windows, targeted/untargeted owner opens, route (iii), the split exactness fields and positive-evidence retention, the `package_access` event, the native `owner_reads` basename rule, the rehearsal).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
