---
kind: package-access-ledger-decision-closeout
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: independent-text-pass-recorded; not-ratification; nothing-admitted; D4-realization-and-rehearsal-pending
---

# Package-access ledger decision — close-out of the D3 and contract text

## 1. What this records, and what it does not

This records that the **text** of the supervisor-owned package-access ledger decision, its contract amendment and its workplan entry received independent PASS verdicts, and that the stakeholder instructed the design to stop changing mechanism (decision record, rounds 3 to 5). It is a development record under SSDP 6.6.0; Protocol 7.0 remains **NON-QUALIFIED** and `PROTOCOL-RELEASE-STATE.yaml` is unchanged.

It does **not** record: stakeholder ratification of Protocol 7.0 or of the evaluation contract as a whole; realization of any of it in D4 code (the code under `qualification/ssdp70/eval/` is unchanged since `8be024a` and realizes revision 3 of the decision); the executor rehearsal; the run count N and the instantiated 0.8 campaign target; admission of any runner, profile or transform; or any qualification run. A PASS on text is not acceptance of an implementation.

## 2. Independently checked text (identities)

| Item | Path | SHA-256 | Independent verdict |
|---|---|---|---|
| D3 decision, revision 8 | `qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md` | `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783` (identical at `07a4bb0` and `b8c706f`) | PASS with D4-stage conditions, sixth check at `07a4bb0`; unchanged by the seventh |
| Contract, revision 15 | `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920` at `b8c706f` | PASS, seventh (narrow) check at `b8c706f` |
| Amendment record, revision 15 | `qualification/ssdp70/PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md` | `8a5ec9bdd7a0ff2e0e51038b53307ccc1d8ea078f80e402e20abfb1994315e64` at `b8c706f` | PASS with the contract |
| Stakeholder decision record (five rounds) | `qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` | `593c675580ef4b42dced94f48669c3747270e9b00a95db5a6ddbd1651e3d0246` at `b8c706f` | read and found consistent by the seventh check |
| Workplan §0.1 entry and six markers | `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md` | `526aa3c7b0875c6f260e716a24bcc5bd42ee4cca6131b90968a38d653951353a` at `07a4bb0` (PASS, sixth check); `8832c93ac7b4da9e546ebbaada32c73e6f7038ad4c9cdefef4af6e655292f811` at `b8c706f` (two label updates only; consistent, seventh check) | PASS |

Contract revision 8's earlier independent PASS (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`) is not extended by these verdicts to any bytes other than those listed.

## 3. Review chain (reports in this directory)

| Subject | Report | Verdict |
|---|---|---|
| Decision (pending text) | `PACKAGE-ACCESS-LEDGER-INDEPENDENT-REVIEW-D3-REV1-2026-10-04.md` | Serious Challenge SC-1 and conditions C1 to C6 |
| D3 rev 3, contract rev 9 | `…-CHECK-D3-REV3-AND-CONTRACT-REV9-…` | NO-PASS |
| D3 rev 4, contract rev 10 | `…-CHECK-D3-REV4-AND-CONTRACT-REV10-…` | NO-PASS (workplan PASS) |
| D3 rev 5, contract rev 11 | `…-CHECK-D3-REV5-AND-CONTRACT-REV11-…` | NO-PASS |
| D3 rev 6, contract rev 12 | `…-CHECK-D3-REV6-AND-CONTRACT-REV12-…` | NO-PASS ("should converge after one text-only revision") |
| D3 rev 7, contract rev 13 | `…-CHECK-D3-REV7-AND-CONTRACT-REV13-…` | NO-PASS (workplan PASS with conditions) |
| D3 rev 8, contract rev 14 | `…-CHECK-D3-REV8-AND-CONTRACT-REV14-…` | D3 PASS; workplan PASS; contract NO-PASS (one blocker) |
| Contract rev 15 | `…-CHECK-CONTRACT-REV15-…` | PASS |

The reviewers were fresh subagent contexts (Opus and Fable) given identities and scope only; their common-mode limits (same model family as the authors, the repository's own rig and package) are stated in each report. The first review and the revisions' author context cannot be counted as independent of one another.

## 4. Conditions carried to the D4 stage (consolidated, non-blocking)

Each is a condition on D4 realization or on the rehearsal and checker, not an edit to the passed text:

1. **D4 realization of the decision** (the lists in the D3 revision 6, 7 and 8 notes): heartbeat source and bracketed rows folded per (file, flags, interval); candidate windows and the request-position pairing with verification and the start-of-trace fallback; request-stamp monotonicity and bracket-end heartbeats; the provably-post-R2 test; owner-class supply (error-status results included, substring matching, 256 bytes across at least two distinct owner lines, minor exposure); `owner_floor_exact` and `owner_read_observed`/`owner_minor_exposure`/`owner_open_windows` (the harness still nulls `owner_read_sequences` unless exact, publishes `observed_ssdp_bytes_lower_bound` when inexact and matches owner reads by substring); the `package_access` event with the observer request records among its recomputation inputs; replacement and unknown-value bookkeeping with the byte-question between-arm bound; the T7 owner-floor-only rerun; the mechanical premise check.
2. **`CLOCK_MONOTONIC` request stamps** (or a recorded absence of a host clock step) are a **must**: a host realtime step is otherwise a false PASS-eligible path.
3. **Rehearsal forms to add** (D3 item 8's list is open-ended): the above-quantum honest keyword `grep` (a common word prints 17 to 47 distinct owner lines, 3.5 to 11.8 KB; an intended non-replaceable pre-R2 FAIL whose rate is reported); R2 as a parallel tool action; request-position pairing mismatch; copies of the package in any encoding; the same-response owner load and its UNRESOLVED rate; and the freezing of the list of "common honest forms".
4. **Seventh-check items to settle at the D4 stage or the pre-run check:** adjudicate the R2 position **before** deciding replacement eligibility (an ambiguous R2 position is otherwise safe only through §4's adjudication); reword effect (d)'s "neutral on outcome", because the replacement trigger correlates with consumption and burden medians are measured on a censored sample (the between-arm bound and the cap limit it), and confirm the wording with the stakeholder; align effect (f) with the No-ledger bullet on whether owner-class supply (not only a native read) scores on a no-ledger profile; state the unit of the T7 owner-floor rerun cap (per run as written, against §5's per non-T7 case); state per-question availability when the byte bound is absent; clarify "no positive evidence" and the placement of minor exposure; reduce the 256-byte rule's restatements in the workplan to pointers.
5. **Known stale labels left unedited to preserve the verdict hashes:** D3 notes that say "contract revision 10" or "contract revision 14" (they name the revision current when each note was written and resolve by path to contract §1 item 13); the workplan entry's "pending Review" wording; stakeholder round 3 item 4's "four effects" (marked superseded in part). Refresh them at the next governed revision.

## 5. Still open

- **Run count N** and the instantiation of the 0.8 campaign target (checker, before runs); the frozen between-arm bound on the byte question's inexact-run rate.
- **F-5** (T7 mixture reporting at seven pairs; 6.5 comparator owner naming).
- The executor **rehearsal gate** (D3 item 8) is unmet and blocks any ledger-dependent burden or owner claim.
- Reopen triggers of the decision (D3 "Reopen triggers") remain live, notably a high UNRESOLVED rate from honest scans or same-response owner loads, a broken premise, and any realization that needs a new principal, channel or edge.

## 6. Not changed by this close-out

`PROTOCOL-RELEASE-STATE.yaml`, the accepted-current 6.6.0 identities, `qualification/ssdp70/activation-implementation-20261004/`, custody and frozen evidence, and the passed documents listed in §2. No push; the commits since `8be024a` are development commits on `ssdp-7.0-scientific-epistemic-closure`.
