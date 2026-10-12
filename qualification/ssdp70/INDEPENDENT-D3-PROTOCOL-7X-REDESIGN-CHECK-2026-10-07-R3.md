---
kind: independent-d3-check
governing_protocol_version: 6.6.0
subject:
  - qualification/ssdp70/D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md (revision 3)
  - qualification/ssdp70/PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md (revision 3)
  - qualification/ssdp70/qual-v2/operating_characteristics.py (revision 3)
  - workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (revision 3)
checked_against: STAKEHOLDER-DECISION-2026-10-07-PROTOCOL-7X-REDESIGN.md, SD-R1..SD-R10 (not re-litigated)
round: 3
prior_records: INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07.md (round 1), INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07-R2.md (round 2)
date_utc: 2026-10-07
checker: independent context; authored nothing under review
role_text_used: software-design SKILL.md as accepted at 6.6.0 (22f4bdba, per PROTOCOL-RELEASE-STATE.yaml); source/ is at 7.1.0 and was read only as the subject's baseline
---

Governing SSDP version: 6.6.0.

# Independent D3 check, round 3: Protocol 7.x redesign and contract v2

## Verdict

**PASS WITH GAPS.** No SERIOUS CHALLENGE and no blockers. All three round-2 blockers are repaired or reduced to bounded residuals. Five gaps (N3-G1 to N3-G5) and seven minors remain. Per workplan S0 (:176), the gaps must be repaired by a minimal delta before S1. The most material gap:

- **N3-G1.** The stated compound (0.814 / 0.808) computes δ from the true base rate. The contract computes it from the estimated p̂. Modelled as specified, the good-candidate compound falls to about 0.79 at both ICCs, below the ≥ 0.80 design rule.

The repair for N3-G1 changes a margin or an exposure, so it needs a recomputation and a check of that delta (contract §8). It does not need a full fourth round.

## SERIOUS CHALLENGE

None. The losslessness/limit conflict that round 2 left open is settled by SD-R4 as revised again. I restored every further omission I found (N3-G2), and each variant still fits the ≤ 100% hard limit (smallest margin: D1/D2, 32 B). Q5c (N3-G3) is a stakeholder-owned risk with an escalation route, not an unrealizable authority.

## Round-2 repair verification (checked against the revision-3 bytes)

| Item | Verdict | Basis |
|---|---|---|
| N-B1 | PARTLY | Everything round 2 listed is restored in Appendix A:393-408. Precedence is decided (SD-R4 revised again; design §5.1:214; O-4:124). The span is frozen (§5.1:202), and I reproduce the 7.1 spans exactly (9,823 / 9,150 / 8,192 / 5,451 / 4,047). I rebuilt all six variants and they match within 1–13 B (D1/D2 9,709, D3 9,022, D4 8,042, documentation 5,043, audit 3,860). Appendix A is still not fully lossless (N3-G2), but restoring the omissions keeps every variant under the limit. |
| N-B2 | REPAIRED (residual N3-G3, N3-m4) | Contract :62 now uses `entry_and_burden` with the injected entrypoint counted as installed. Contract :95 carries the 512 B margin, the static pre-measurement (design §8:275; O-11), the T7 rule, counterbalancing and the stop/escalation rule. The hard-coded 0.99 is removed from the script, and Q5c is stated as not modelled. |
| N-B3 | REPAIRED (residuals N3-G4, N3-m2) | Design §3:92 and :96 and workplan `amends` (:6) now list §11:989, §12 B/D, §13 items 13–14, §14:1123 and the two I66-3/attribution sentences. O-5:125 covers the owner, the governing workplan, the entrypoints and both READMEs. |
| N-G1 | REPAIRED | Q4b–Q4d count runs. Q4a's δ uses the design effect 1 + (m − 1)·0.5. I reproduce 6/7/9 at m = 1/2/4 and A/A ≥ 0.985 at ICC 0.5, m = 4. New, separate issue: N3-G1. |
| N-G2 | REPAIRED | Q4d is stated as a near-absolute cap with its OC (design :160; contract :92, :120). Its rates are listed as S4 planning assumptions. |
| N-G3 | REPAIRED | Listed (design :100) and decided (SD-R10). |
| N-G4 | REPAIRED | The script now computes all four verbatim rules. The record (:51) and design §9 are corrected and reproduce. |
| N-G5 | REPAIRED | The description exemption is cited to governing §8.3:631 (design :200, :274; contract :96; O-2). |
| N-G6 | REPAIRED (residual N3-m1) | The depth line is non-imperative (Appendix :393). Element 3 keeps the default/qualify/block structure. |
| N-G7 | REPAIRED | `stand_in_provider.py` is kept and counted as test (design :248, :252). Arithmetic verified: 788 + 1,700 + 4,972 = 7,460; 20,279 − 7,460 − 169 = 12,650. |
| N-G8 | REPAIRED | README and source README are in §8:278, O-5 and O-9. |
| N-m1 … N-m9 | REPAIRED | N-m4 is stated as a limit (contract :114). N-m5: 20,000 trials and a fixed seed reproduce the quoted figures exactly. Small residuals are under minors. |

**Round-1 items that round 2 marked PARTLY:**

| Item | Verdict | Basis |
|---|---|---|
| SC-1 | PARTLY | Same residual as N-B1 (N3-G2). It is bounded: the omissions fit the limit, and O-3 is a blocking independent check. |
| B-2 | REPAIRED | Through N-B3. |
| B-3 | REPAIRED | All six measured, and reproduced. |
| B-4 | REPAIRED | Q4 is cluster-adjusted (new N3-G1 is about p̂, not clustering). |
| G-5 | REPAIRED | Through N-G2. |
| G-9 | REPAIRED | "14 modelled checks" is accurate (Q1a, Q1b, Q2a, Q2b, Q3, Q4a–d, Q5a, Q5b, Q5d, Q5e, Q5f). Q5c is no longer asserted. |
| m-1 | REPAIRED | The mixture is documented in the docstring. |

## New findings

### Gaps

**N3-G1. The compound uses the true base rate in δ; the contract uses the estimated p̂. Modelled as specified, the compound misses 0.80.**
- **Where.** Contract §5:78-80 ("pooled B1+B2 rate p̂"), :100-105; script `ni_margin` callers (:88-94, :97-104, :232-238 pass the true `p_base`); design §0:41 and §4.3:133-138; stakeholder record :29.
- **Evidence.** My scratch `phat.py` is the script's own gate models, with an independent B2 and δ recomputed from the pooled p̂ in each simulated campaign. Q4d keeps max(2, ·). 20,000 trials. The true-p control reproduces the script.

| Gate | ICC 0.3: true p → p̂ | ICC 0.5: true p → p̂ |
|---|---|---|
| Q1b (0.05) | 0.992 → 0.980 | 0.996 → 0.989 |
| Q4a (0.10, m = 2) | 0.993 → 0.978 | 0.988 → 0.970 |
| Q4b (0.05) | 0.994 → 0.983 | 0.996 → 0.988 |
| Q4c (0.25) | 0.991 → 0.987 | 0.996 → 0.993 |
| Q4d (0.005 vs 0.01) | 0.969 → 0.978 | 0.976 → 0.984 |
| **Compound** | **0.814 → ≈ 0.787** | **0.808 → ≈ 0.785** |

  The cause is estimation noise in p̂ through a concave, ceiled δ. Taking p̂ from B2 alone gives the same result (0.982 / 0.979 / 0.984 / 0.989 at ICC 0.3), so the B1 coupling is not what causes it.
- **Failure scenario.** The stakeholder adopted figures (record :29) that the specified rule does not achieve. A good candidate passes about 0.79, which breaks principle 5 and contract §1:26-28 at both ICCs. That rule is exactly what the redesign exists to guarantee.
- **Minimal repair.**
  - Model p̂ in the script.
  - Restore ≥ 0.80. Options: a slightly larger quantile, a δ floor on an upper bound of p̂, or a small exposure change. Recompute the Q4 detection-limit table.
  - Correct design §0/§4.3, contract §5 and record :29, and have the delta checked (contract §8).

**N3-G2. Appendix A is still not lossless. All restorations fit the hard limit.**
- **Where.** Appendix A, design :404, :406, :407, :408; design :36, :204-214 and record :67 call it lossless.
- **Evidence.** Each item below is in the frozen §8.3 text, and in all but the last two also in the 7.1 block. Each is absent from Appendix A:
  1. Element 1 fallback: "proposed custodian/destination" (§8.3 element 1, feedback-persistence row; 7.1). Appendix :404 has "proposed custodian".
  2. Element 3 search scope: "former names **or paths**" (§8.3 element 3; 7.1). Appendix :406 has "former names". Path moves are the commonest rename.
  3. O3 row: "existing **external/product** contract" (7.1 element 4). Appendix :407 has "an existing contract", which widens O3: any contract, including an internal workplan, would authorize product change.
  4. Found-entry asserter row: the record "does not show which human **or agent** used a shared account". Appendix :406 has "proves no person or authority"; 7.1 has "neither person/agent nor disposition authority".
  5. Reader/questions row and element 6: "**visibly** propose". Appendix :408, and 7.1, have "Independently propose".
  6. The owner's own structure (the named exception): "Any other indication **qualifies** the judgment and is routed to the human". Appendix :406 has "route other indications to the human" and drops the qualify.
- **Judgment items for the O-3 check.**
  - The variant-search row's "rather than presenting a local count as the whole search" (also absent in 7.1). It is arguably entailed by "known lower bound … claim limit".
  - The change-only relief "beyond answers or gaps a delegator asked for" (:404). Its antecedent is ambiguous against the frozen "removes no gap report a delegator owes for a delegate's unanswered part". The unconditional gap rule (:401) covers it, but the relief can be read as overriding the gap rule.
- **Measurement.** My scratch `variants.py` builds the variants per §5.1/Appendix A and restores items 1–6 minimally:

| Entrypoint | Appendix A | Restored 1–6 | Limit | Margin |
|---|---|---|---|---|
| D1/D2 | 9,709 | 9,791 | 9,823 | 32 B |
| D3 | 9,022 | 9,104 | 9,150 | 46 B |
| D4 | 8,042 | 8,124 | 8,192 | 68 B |
| documentation | 5,043 | 5,081 | 5,451 | 370 B |
| audit | 3,860 | 3,889 | 4,047 | 158 B |

  Restoring the "local count" clause verbatim (about 55 B) as well would put D1/D2 about 20 B over, unless D4 compresses elsewhere. The §5.1:214 route to the stakeholder covers that case.
- **Failure scenario.**
  - D4 starts from Appendix A as directed (§5.1:191; workplan :105).
  - If the O-3 check misses these items, the block ships weaker than 7.1 on O3 and the rename search. Item 3 is a safety boundary.
  - The "lossless" label and the SD-R4 basis are again slightly misreported, by ≤ 82 B, which does not change the decision.
- **Minimal repair.**
  - Restore items 1–6 in Appendix A and update the §5.1/record figures.
  - List the two judgment items for the O-3 independent check.

**N3-G3. Q5c is excluded from the design rule without amending principle 5, and X6 does not catch a non-breaching but likely failure.**
- **Where.** Design §2:79 (frozen principle: "computed over every gating check"); contract §1:26 ("every modelled gating check"); design §4.4:161 and X6:313; workplan :31 (unconditional ≥ 0.80).
- **Evidence.**
  - Design :161 gives about 0.9 KB of headroom, so a median T1/T8 run that reads the 45,958 B owner breaches the backstop.
  - L3 (:62) records Flash reading the owner "to be safe", and the block now recommends the owner as depth (:393).
  - Under these conditions P(Q5c pass | good) can sit well below 1 while the S4 median stays under the cap, and then X6 does not fire.
- **Assessment.** Not modelling the backstop is acceptable: it is a stakeholder-fixed rule whose pass depends on an unmeasured read rate. A conditional compound alone does not meet the design rule as frozen, and the unconditional claim in the workplan (:31) is not supported.
- **Minimal repair.**
  - Amend principle 5 (and workplan :31) to state the conditional rule.
  - Make S4 estimate the per-route owner-read fraction and the implied P(Q5c pass).
  - Report the unconditional compound to the stakeholder before the campaign. X6 should fire when that estimate puts the unconditional compound below 0.80, not only on a median breach.

**N3-G4. Two governing-workplan statements that conflict with v2 are still outside the amendment list, and the (a)–(c) rule's required status is not written into §8.3.**
- **Where.** Governing workplan §0:28 ("compression attribution and all non-size floors remain operative"); §13 item 16 (:1109, "§11.5 route-class preservation floors"); §8.3:630-631; design §3:92; workplan :6.
- **Evidence.**
  - §0:28 is current-disposition text that keeps "all non-size floors" operative. SD-R1 replaces those floors, but §0:28 is not in `amends`. O-5's consistency test only looks for owner-read, owner-load and minimum statements, so it would not catch this.
  - Under the attribution rule at :631, "non-required content" on the surface is a D4 defect. The label table (:600) treats "meaning beyond this table" as non-required owner depth. §8.3:630 still lists the (a)–(c) conditions as owner depth.
  - Design §3:92 amends only the "not inlined" and "inlined owner doctrine" phrases. It never says that the (a)–(c) rule joins the frozen minimum. Contract §3:49 does score it as required.
  - An independent attribution check can therefore flag the (a)–(c) sentence as a non-required D4 defect while O-3 requires it.
- **Minimal repair.**
  - Add §0:28 and §13 item 16 to design §3 and to `amends`, annotated as superseded by SD-R1/SD-R4.
  - In the §3:92 row, state that the inaccessible-home rule with (a)–(c) is added to the element-3 frozen minimum, and annotate the depth list at :630 to match.

**N3-G5. Workplan stop/reopen lists omit X6.**
- **Where.** Workplan :92 and :185 ("design §10 X1–X5"). S3/S4 (:179-180) refer to X6, and O-11 depends on it.
- **Failure scenario.** A Q5c static breach found at S3 is not a listed stop or D3-reopen trigger in the workplan's own trigger lists.
- **Repair.** Change both to X1–X6.

### Minors

- **N3-m1.** Appendix :406 (c) reads "from an owner, acceptance authority". The owner says "an owner or acceptance authority *of that authority*". Without that qualifier the actor's standing is ambiguous.
- **N3-m2.** Remaining stale text from the old doctrine:
  - Owner :35, "The trigger holding for one judgment brings in no … other load", which loses its referent once :29 is amended.
  - Governing Stage G list :1068, "a routing line whose load instruction conflicts with the owner-false-activation floor".

  Neither makes a read mandatory. Annotate them with the other §12 annotations.
- **N3-m3.** Design §5.1:214 says "Four of six miss the 95% target". By its own table, five miss (D1, D2, D3, D4 and audit); only documentation meets it.
- **N3-m4.** Contract Q5c (:95) is labelled "verbatim" but does not name the run mode. The 2026-09-28 rule says "6.6 run mode", and governing §0 :174 overlays it with deterministic entry. The decision record also says "For Protocol 7.0 only". State that the 2.0× rule carries over to the 7.2.0 successor under the same governing workplan, and name the run mode.
- **N3-m5.** Stakeholder record :49 still carries "D4 reference: 7,405 B against 8,174 B" with no strike or withdrawal note. §12a :365 says the figure was withdrawn everywhere.
- **N3-m6.** Design §12 m-7 row (:358), "saves only about 10% against 7.1", contradicts L9 (:68, 1–7%).
- **N3-m7.** "Monte Carlo error about ±0.005" (design :133; contract :100) is stated without a basis. It is plausible at 20,000 trials, but is not computed by the script.

## Operating-characteristics reproduction

Commands, from the repository root:

```
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000 --icc 0.5
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000 --icc 0.5 --q4a-m 4
```

Scratch scripts: `phat.py`, `phat_b2.py`, `variants.py`, `span.py` (session scratchpad `check3/`, not committed).

| Figure | Stated | Reproduced (seed fixed) |
|---|---|---|
| Good compound, ICC 0.3 | 0.814 | 0.814 |
| Good compound, ICC 0.5 | 0.808 | 0.808 |
| Good compound, ICC 0.5, m = 4 | 0.805 | 0.805 |
| Good compound with δ from p̂ (N3-G1) | — | ≈ 0.787 / ≈ 0.785 |
| No-effect (Q3 null) | ≤ 0.004 / ≤ 0.008 | 0.0040 / 0.0073 (m = 4: 0.0077) |
| Verbatim rules, each | 0.75–0.92 | route 0.922/0.917; version 0.748/0.815; sentinels 0.922; no-lookup 0.914 |
| Verbatim rules, together | 0.58–0.63 | 0.581 / 0.629 |
| SD-R10 recalibrated Q5f | 0.997 | 0.997 / 0.998 |
| Q2 at 0.85 | 0.97 (0.95 at ICC 0.5) | 0.974 / 0.952 |
| Q3 at +25 / +20 / +15 pp | 0.95 / 0.81 / 0.52 | 0.955 / 0.811 / 0.520 |
| Q4 limits | 0.72 / 0.35 / 0.71 | 0.716 / 0.340 / 0.690 (ICC 0.3); 0.723 / 0.339 / 0.713 (ICC 0.5) |
| Q4a δ at m = 1/2/4; 0.10 → 0.25 | 6/7/9; 0.56–0.78 | 6/7/9; 0.557–0.780 |
| Q4d at 1/2/5/10% | 0.97/0.84/0.31/0.02 | 0.970/0.842/0.307/0.021 |
| Q5a one case lost; Q5b halving / total loss | 0.11; 0.29 / ≤ 0.006 | 0.113; 0.293 / 0.002–0.006 |
| C(b) at 0.95 / 0.80 | 0.975 / 0.11 | 0.975 / 0.109 |

**Derivation check.**
- The Q4a design effect 1 + (m − 1)ρ applied to the variance of the difference of two clustered sums is correct. ρ = 0.5 is conservative up to a realized ICC of 0.5. Ignoring the between-arm pairing correlation is also conservative.
- Q4b–Q4d as per-run indicators need no adjustment.
- The near-absolute Q4d cap is computed correctly: δ = 2 at 0.005 over 80 runs.
- The Q5f model now matches the rule (3 runs per route, a recurrence within 2 reruns).
- The verbatim rules are modelled at 6.6's exposures: 19 × 2 with margin 2; 8 × 1 with margin 1; 2 × 2 sentinels; 0/9.
- The no-effect bound is sound (the episode sign test is exchangeable under the null).
- The only derivation defect is N3-G1.

## Checked and found sound

- No self-acceptance. Release state untouched. Governing version 6.6.0 is stated in every subject file. S0 is gated on this check.
- The §5.1 span definition is reproducible, and the `58fd67b` and HEAD 7.1 spans are identical.
- The variant construction (elements 5 and 7 verbatim from 7.1; the specialists by deletion) gives figures matching §5.1 within 13 B.
- Every frozen §8.3 item not listed under N3-G2 maps onto Appendix A:
  - elements 1–7 per the role map, including the specialist placement;
  - all 20 label-table rows, with the element 5 and element 7 rows carried by the verbatim 7.1 text;
  - the four delegate questions with "including any tools or agents you launched" and the tension definition;
  - the gap rule with its three exemptions and the partial-answer rule;
  - "answers owed even for change-only work";
  - re-evaluation;
  - the pre-irreversible-step inquiry.
- Owner :29, :33 and :389, and the governing §8.2/§8.3 R2 sentences, §11:989, §12 B/D, §13 items 13–14 and §14:1123, are all listed. The (a)–(c) exception is coherent with I66-3 as a named, stakeholder-motivated exception (SC-1). The one open point is N3-G4's required-status sentence.
- The 2026-09-28 Q5c parts are carried (N3-m4 aside). The `entry_and_burden` accounting matches `qualification/ssdp66/eval/harness.py:332-333`.
- Expected installed D4 size: 7,057 + 8,041 + 214 = 15,312 B against 16,208 B, leaving 896 B (design :161).
- Design, contract, workplan and stakeholder record agree on every gate number and exposure, apart from the items above.

## Could not check

None of these is required of an S0 design check. Each is a required check at its own stage.

- **Live OMP behaviour** (relay, activation proof, turn cap, egress refusal). No live runs, per the brief. Required at S2 (O-6).
- **Whether D4 wording fits after the O-3 independent mapping.** Margins after the N3-G2 restorations are 32–68 B on the roles. A further required item found by O-3 could exceed the limit and go to the stakeholder (§5.1:214).
- **The real ICC, p̂, items per episode, and owner-read fraction on T1/T7/T8.** These come from S4, and they decide N3-G1's size after repair and N3-G3.
- **Repository acceptance.** Not run: nothing under `source/` changed in this subject.
