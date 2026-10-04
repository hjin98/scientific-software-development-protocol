---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 10
status: revision 10 drafted; fresh independent check required (contract and workplan §0.1 entry and markers) together with fresh independent D3 acceptance of the package-access ledger decision revision 4
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 10)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision's owner-read and byte accounting for process-executed package reads is a supervisor accounting record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** None new. The stakeholder authorized the bounded D3 repair of the process/file-access observation gap and asked for the recommended resolution of C-4 to proceed. **This is a drafted proposal, not a stakeholder decision.** It changes no threshold, floor, fixture, exposure minimum or case. Where a rule is a recorder choice it is labelled R-op in the contract item. Four stakeholder decisions it depends on are open (§5).
- **History.**
  - Revision 9 (`8d04088`): independent NO-PASS for the contract plus workplan marker and for D3 revision 3, recorded in `/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV3-AND-CONTRACT-REV9-20261004T231706Z.md`. No Serious Challenge; blockers C-1 to C-6, W-1, W-2 and D3-1 to D3-3. It confirmed that revision 9 adds no floor or threshold and leaves revision 8 unchanged in effect.
  - Revision 10 (this file) repairs them.
- **Authorship.** The same context authored the earlier independent review that raised C-4, N-1 and N-2, the D3 revision 3 and 4 amendments, and contract revisions 9 and 10. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 received independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`). Revision 10 changes those bytes (a new §1 item 13, pointers in items 4, 5, 11 and §6, §8) and so requires a fresh check even though it is additive.

## 2. Contract and workplan changes

| Location | Change |
|---|---|
| Front matter `status` | Now revision 10 pending fresh independent check. |
| §1 item 4 | Derived event kind `package_access` (supervisor-owned); the owner-read sentence names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a declared reduction, lossless for the item 13 oracles, of the kernel stream (not "raw"); the completeness map maps it, with its heartbeat records, to the `package_access` event and the rows, loss and timing-loss conditions and counts must reconcile. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the governing decision's document path, commit and SHA-256 as recorded by its independent acceptance. |
| §1 item 13 | Ledger profile or no ledger; the `package_access` event and payload (brackets, timing-loss conditions, three exactness values, `owner_read_observed`); claim scope with positive evidence never suppressed; owner-access time; campaign effect; rehearsal gate per arm and per question; Record pointer. |
| §6 | A paragraph listing the ledger demonstrations, the known-broken probes and the known-good probes, including the pre-R2 owner open shown later and drained late. |
| §8 | Revision 8's stale "no independent check" sentence corrected; a revision 10 entry. |
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

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. Recorded as the fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule.
- **A supervisor sentinel at each request for event ordering.** Not available without a new edge: the supervisor is not in the request path. The in-queue heartbeat gives the same ordering without one.
- **Decide replacement semantics or the rehearsal target here.** Rejected: both are stakeholder decisions that depend on the campaign run count.

## 5. Stakeholder decisions this amendment depends on (open)

1. **Replacement runs.** Recommended: bounded replacement of observation-inexact originals only, cap as in §5, originals retained and disclosed with per-arm inexact rates, a material arm difference leaves the claim UNRESOLVED, and a positive owner read is never replaced.
2. **Rehearsal-gate target.** Recommended: accept the structural gate with reported per-form, per-arm, per-question rates, and set a campaign target (for example, 80% probability that no owner-unresolved run voids the campaign) once the run count N is known.
3. **Positive evidence.** Recommended: a definite pre-R2 owner read is a FAIL even when other observation is inexact.
4. **Observation boundary.** Recommended: the supervisor ledger is an admissible observation of supervisor-owned inputs alongside the provider-control observer.

## 6. Questions for the fresh independent check

1. Is the mechanical bracket sound: can a late drain, a heartbeat gap, a wall-clock step or subject load make an owner access appear later than its true turn without timing loss being recorded? Is the earliest-consistent-turn rule conservative on every path?
2. Is making the owner-access question depend only on the ledger and timing (any owner open is access) sound, and does it create false owner accesses on any runtime behavior the build exhibits?
3. Is route (iii) (whole-file same-turn delivery) free of the shared-block failure that revision 2 repaired, and does it leave any opened file explained that the model has not wholly received?
4. Is the `package_access` event derivable and recomputable from retained artifacts alone, and does the completeness map account for the ledger artifact and its heartbeat records without a loophole?
5. Can item 13 create any path to PASS when observation is not exact, when positive evidence exists, or when the gate target is unrecorded? Is the campaign-effect sentence a faithful clarification of item 7 or a new floor?
6. Are the workplan §0.1 entry and the two markers consistent with the overlay convention, and do revision 8's criteria, family rule and activation-strata bytes stay unchanged in effect?

## 7. Still blocked

- Independent acceptance of D3 revision 4 and of this amendment together.
- The four decisions in §5, and the gate target (needs N).
- D4 realization of revision 4 (heartbeat and bracketed rows, earliest-consistent-turn mapping, route (iii), the split exactness fields and positive-evidence retention, the `package_access` event, the native `owner_reads` basename rule, the rehearsal).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
