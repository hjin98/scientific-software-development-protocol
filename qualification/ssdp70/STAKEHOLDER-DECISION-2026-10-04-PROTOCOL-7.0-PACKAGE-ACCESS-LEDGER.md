---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date_utc: 2026-10-04
status: stakeholder-adopted-pending-fresh-independent-check
---

# Package-access ledger — stakeholder decisions on the open items

After the independent check of D3 revision 3 and contract revision 9 returned NO-PASS, the recommended resolution for the four open stakeholder decisions was given as: replacement runs (bounded, observation-inexact originals only), rehearsal-gate acceptance (structural gate with reported rates and a campaign target set once the run count is known), positive owner evidence (a definite pre-R2 owner read is a FAIL even when other observation is inexact), and the observation boundary (the supervisor ledger is admissible for supervisor-owned inputs alongside the provider-control observer). The stakeholder then instructed: **“Also apply your recommendation for the stakeholder's decision.”** This record applies those recommendations as written in `PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md` §5 at commit `b7fdd0d` and adopts contract revision 10's normalized-event route for open item C-4. It is a qualification evidence-contract decision under SSDP 6.6.0; Protocol 7 successor source is not adopted.

## Adopted decisions

1. **Replacement runs.** A qualification run that is unresolved on an owner floor, or `INADMISSIBLE` for a burden claim, *only because the package-access observation is not exact* and with no positive owner evidence, may be replaced under the contract §5 rule (at most two independent reruns per affected case; T7 keeps its own pair-addition rule and is not extended by replacement; no threshold change). The original stays on record with both identities and its cause disclosed; per-arm and per-form inexact-run and replacement counts are reported. A replacement resolves the slot only if it is exact for the question concerned. A positive owner-access observation before R2 is never replaced, and a run inadmissible or failed for another reason is not replaced under this rule. **Recorder choice (R-op), to be confirmed by the stakeholder:** the campaign record freezes, before runs, a per-arm bound on the difference in inexact-run rates; absent a frozen bound replacement is unavailable (fail-closed), and a disparity above the frozen bound leaves the affected comparative claim `UNRESOLVED`.
2. **Rehearsal-gate acceptance.** The structural gate with reported per-form, per-arm, per-question rates is accepted. The campaign target is that the probability that no owner-unresolved run voids the campaign is at least **0.8** with replacement allowed; the independent checker instantiates it from the frozen run count N, the per-form rehearsal rates and the replacement cap and records the arithmetic before runs. The 0.8 value is the recommendation's example, adopted as a recorder choice (R-op) for the stakeholder to confirm; another target needs a written stakeholder decision. Until instantiated the gate is unmet.
3. **Positive owner evidence.** A definite owner access before the first predeclared R2 event is a zero-tolerance FAIL even when the byte, owner-access or owner-load observation is otherwise inexact.
4. **Observation boundary.** The supervisor package-access ledger is an admissible observation of supervisor-owned inputs alongside the provider-control/observation principal, which remains the only approved independent boundary for the model-facing runtime fields of the workplan's "Trusted runtime-observation contract". The ledger adds no cross-principal edge.
5. **Open item C-4.** The contract-amendment route (contract revision 10, §1 item 13, derived `package_access` event) is adopted instead of the accounting-record fallback.

## Not decided here

F-5 (T7 mixture reporting at seven pairs; 6.5 comparator owner naming) and the run count N remain open. Whether the owner-access rule (any post-request owner open is access) needs a bounded exemption is left to the independent check and the multi-turn rehearsal.

## Pending acceptance

**Stakeholder adoption is recorded; fresh independent acceptance remains pending.** The authoring context cannot independently accept these bytes. No runner, profile, transform, qualification, subject, provider or evaluator run is authorized by this decision. D3 revision 4, contract revision 10 and the workplan §0.1 entry need a fresh independent check before dependent D4 realization or admission.
