---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
decision_date_utc: 2026-10-04
status: stakeholder-adopted-pending-fresh-independent-check
---

# Package-access ledger — stakeholder decisions on the open items

After the independent check of D3 revision 3 and contract revision 9 returned NO-PASS, the recommended resolution for the four open stakeholder decisions was given as: replacement runs (bounded, observation-inexact originals only), rehearsal-gate acceptance (structural gate with reported rates and a campaign target set once the run count is known), positive owner evidence (a definite pre-R2 owner read is a FAIL even when other observation is inexact), and the observation boundary (the supervisor ledger is admissible for supervisor-owned inputs alongside the provider-control observer). The stakeholder then instructed: **“Also apply your recommendation for the stakeholder's decision.”** This record applies those recommendations as written in `PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md` §5 at commit `b7fdd0d` and adopts the normalized-event route (contract revision 10, carried forward to the current revision) for open item C-4. It is a qualification evidence-contract decision under SSDP 6.6.0; Protocol 7 successor source is not adopted.

## Adopted decisions

1. **Replacement runs.** A qualification run that is unresolved on an owner floor, or `INADMISSIBLE` for a burden claim, *only because the package-access observation is not exact* and with no positive owner evidence, may be replaced under the contract §5 rule (at most two independent reruns per affected case; T7 keeps its own pair-addition rule and is not extended by replacement; no threshold change). The original stays on record with both identities and its cause disclosed; per-arm and per-form inexact-run and replacement counts are reported. A replacement resolves the slot only if it is exact for the question concerned. A positive owner-access observation before R2 is never replaced, and a run inadmissible or failed for another reason is not replaced under this rule. **Recorder choice (R-op), confirmed by the stakeholder below:** the campaign record freezes, before runs, a per-arm bound on the difference in inexact-run rates; absent a frozen bound replacement is unavailable (fail-closed), and a disparity above the frozen bound leaves the affected comparative claim `UNRESOLVED`.
2. **Rehearsal-gate acceptance.** The structural gate with reported per-form, per-arm, per-question rates is accepted. The campaign target is that the probability that no owner-unresolved run voids the campaign is at least **0.8** with replacement allowed; the independent checker instantiates it from the frozen run count N, the per-form rehearsal rates and the replacement cap and records the arithmetic before runs. The 0.8 value is the recommendation's example, adopted as a recorder choice (R-op) and confirmed below; another target needs a written stakeholder decision. The target covers the owner floors and, as amended below, each burden route. Until instantiated the gate is unmet.
3. **Positive owner evidence.** An owner read before the first predeclared R2 event, as defined by the second round below (content that reached the model), is a zero-tolerance FAIL even when the byte, owner-access or owner-load observation is otherwise inexact.
4. **Observation boundary.** The supervisor package-access ledger is an admissible observation of supervisor-owned inputs alongside the provider-control/observation principal, which remains the only approved independent boundary for the model-facing runtime fields of the workplan's "Trusted runtime-observation contract". The ledger adds no cross-principal edge.
5. **Open item C-4.** The contract-amendment route (contract revision 10, §1 item 13, derived `package_access` event) is adopted instead of the accounting-record fallback.

## Confirmations and amendments (2026-10-04, after the second independent check)

The second independent check (`/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV4-AND-CONTRACT-REV10-20261004T234050Z.md`, NO-PASS) found that scoring *any* post-request owner open as access produces false zero-tolerance FAILs on honest package-wide scans (a `grep -rl` over the package opened all seven owner copies with no owner content shown), and listed four items for the stakeholder. The stakeholder replied: **“I confirm the items are accepted.”** The items, as put to the stakeholder, are:

1. **R-op values.** The frozen per-arm inexact-rate disparity bound (fail-closed default) and the 0.8 campaign target are confirmed as acceptance-process values.
2. **Untargeted owner opens.** An unshown, unnamed owner open (for example a package-wide scan) is `UNRESOLVED` and replaceable, not a FAIL. Positive evidence was defined as a *targeted* owner access (a native read, supply of the owner content, or an open of an owner copy whose path is named in a tool action's recorded input). **Superseded by the second round below.**
3. **Read to access.** For ledger profiles the §4/§5 owner floor was to be scored on a targeted owner access rather than only a displayed read, as a declared change in effect. **Superseded by the second round below.**
4. **T7 reading.** An observation-inexact T7 run is handled by T7's pair-addition rule, not by replacement; the T7 fixed-cost claim is non-PASS if it remains unresolved at seven pairs (made precise by (d) of the second round). The 0.8 target covers each burden route as well as the owner floors.

## Second round of confirmations (2026-10-04, after the third independent check)

The third independent check (`/tmp/SSDP70-INDEPENDENT-CHECK-D3-REV5-AND-CONTRACT-REV11-20261004T235855Z.md`, NO-PASS) showed that first-open placement turns an honest pre-R2 package scan followed by a legitimate post-R2 owner load into a definite, non-replaceable FAIL; that shown owner content is not attributable to one of seven identical copies; and that the named-path test is co-occurrence. Each repair since revision 3 had added mechanism and produced new findings, so a simplification was recommended with these items, and the stakeholder replied: **“I confirm. Draft revision 6, commit, refresh handoff, and spawn a fresh review.”**

- **(a) Named-but-unshown owner open.** UNRESOLVED and replaceable, not a FAIL (reverses the named-open part of the first-round confirmation 2).
- **(b) No read-to-access change.** The owner floor stays an owner *read*, now observed for process-executed reads as content that reached the model (a native read, or owner-class supply: whole owner lines at least the floor long, placed at its own result sequence). First-round confirmation 3 is withdrawn.
- **(c) Partial owner content is supply.** Whole owner lines of at least the floor length count, through any path form.
- **(d) T7 definition.** An observation-inexact burden run is not replaced; it is an unknown value (candidate unbounded above, comparator zero) that triggers T7 pair addition, and the bound resolves only under that adversarial assignment. Inexactness as a pair-addition trigger is the one declared change in effect (ledger profiles only).
- **(e) Recorder choices (R-op), applied by the recorder on the stakeholder's confirmation:** the frozen per-arm disparity bound also covers the burden comparisons (the 2.0x-versus-6.5 bound and the class-iii comparisons); there is no campaign-wide cap on replaced owner-unresolved runs beyond the per-case cap. The stakeholder may revise either after the rehearsal.

## Not decided here

F-5 (T7 mixture reporting at seven pairs; 6.5 comparator owner naming) and the run count N remain open. The UNRESOLVED rate of the owner floor on honest runs is measured by the multi-turn rehearsal.

## Pending acceptance

**Stakeholder adoption is recorded; fresh independent acceptance remains pending.** The authoring context cannot independently accept these bytes. No runner, profile, transform, qualification, subject, provider or evaluator run is authorized by this decision. D3 revision 6, contract revision 12 and the workplan §0.1 entry need a fresh independent check before dependent D4 realization or admission.
