---
kind: qualification-contract-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
amends: qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
revision: 9
status: revision 9 drafted; fresh independent check required (contract and workplan marker) together with fresh independent D3 acceptance of the package-access ledger decision
---

# Package-access ledger amendment to the Protocol 7.0 qualification contract (revision 9)

## 1. Authority and status

- **What this resolves.** Open item C-4 of the independent D3 review of the package-access ledger decision (`D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md`): the decision's owner-read and byte accounting for process-executed package reads is a supervisor accounting record, while contract §1 item 4 scores owner reads "from complete `resource_access` identity/action records" and item 5 requires raw-to-normalized completeness. It also resolves the decision's open item (i), the workplan "Root-selection evidence contract" sentence that makes T1/T7/T8 burden claims inadmissible "if the exact OMP build cannot expose that consumption".
- **Authority.** None new. The stakeholder authorized the bounded D3 repair of the process/file-access observation gap (decision record header) and asked for the recommended resolution of C-4 to proceed. **This is a drafted proposal, not a stakeholder decision.** It changes no threshold, floor, fixture, exposure minimum or case. Where a rule is a recorder choice it is labelled R-op in the contract item.
- **Authorship.** The same context authored the independent review that raised C-4, N-1 and N-2 and drafted this amendment and D3 revision 3. It cannot accept these bytes. A separate reviewing context must reconstruct authority rather than inherit this record's dispositions.
- **Relation to revision 8.** Revision 8 (`ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`) received independent PASS for its bytes. Revision 9 changes those bytes (a new §1 item 13 and pointers in items 4, 5, 11 and §6) and so requires a fresh check even though it is additive.

## 2. Contract changes

| Location | Change |
|---|---|
| Front matter `status` | Now revision 9 pending fresh independent check. |
| §1 item 4 | New derived event kind `package_access` (supervisor-owned). The owner-read sentence now names it as the complete record for process-executed package access in a ledger profile. |
| §1 item 5 | The ledger artifact is a raw observable mapped to the `package_access` event; file rows, loss conditions and counts must reconcile with the retained artifact. |
| §1 item 11 | A ledger run also binds the ledger artifact digest, the accounting-code digest and the identity (document and revision) of the governing package-access decision. |
| §1 item 13 (new) | Ledger profile or no ledger (claim-scoped inadmissible); the `package_access` event and its required payload; claim scope (`exact` for burden, `owner_read_exact` for owner claims); owner-read time (earliest of native, supply and access bound; read before first R2 is zero-tolerance; same-turn ambiguity is ambiguous R2 timing); campaign effect (an owner-inexact qualification run leaves owner false activation UNRESOLVED; no new rescue); rehearsal gate with a stakeholder-recorded threshold. |
| §6 | A paragraph listing the ledger demonstrations and known-broken/known-good probes for a ledger profile, and the rehearsal gate. |

The contract does not restate the D3 attribution rules (supply by distinctive content or path linkage, phase split, exactness, access bound). Their single semantic owner is the D3 decision; item 13 binds the contract to its accepted revision and makes a change to either a joint change.

## 3. Workplan change

One marker only, at the "Root-selection evidence contract" bullet: for a profile with a supervisor package-access ledger meeting contract §1 item 13, supervisor kernel observation plus observer-seen supply is an admissible exposure of consumed resources for T1/T7/T8; a profile without one keeps the claim-scoped inadmissibility. No other workplan text, threshold or overlay item changed. Whether the overlay revision number and the §0.1 header decision entry should also record this marker is left to the fresh independent Review of the workplan overlay.

## 4. Considered and not chosen

- **Accept the accounting record as the owner-read source (profile-scoped residual).** Defensible because the record is hash-bound, deterministic and recomputable, but the zero-tolerance owner floor would then rest on evidence outside the schema and outside the completeness proof. Recorded as the fallback if the contract-revision cost is judged too high; if chosen, state the residual in every report that relies on it.
- **Restate D3 attribution rules in the contract.** Rejected: two owners for one rule; the contract would then drift from the decision.
- **Decide replacement-run semantics or the rehearsal threshold here.** Rejected: both are stakeholder/contract-owner decisions that depend on the campaign run count.

## 5. Questions for the fresh independent check

1. Is the `package_access` event derivable and recomputable from retained artifacts alone, and does the completeness map account for the ledger artifact without a loophole (artifact present but event absent, event present but rows dropped)?
2. Does item 13 create any path to PASS for a burden or owner claim when the observation is not exact, or when the rehearsal threshold is unrecorded?
3. Is the owner-read time rule consistent with §3's zero-tolerance owner floor and its ambiguous-R2-timing clause, and does it stay consistent if the D3 access-bound mechanism changes?
4. Is the "Campaign effect" sentence a faithful clarification of item 7's fail-closed rule, or does it add a new floor? It states current implemented behaviour (`owner_observation_complete`) as contract text.
5. Do the revision 8 criteria, family rule and activation-strata bytes remain unchanged in effect?

## 6. Still blocked

- Independent acceptance of D3 revision 3 and of this amendment together.
- The rehearsal threshold and replacement-run semantics (stakeholder/contract owner; they need the planned run count N).
- Admission of any runner, profile or transform that relies on the ledger.
- Re-binding D4 evidence to the accepted tree.
