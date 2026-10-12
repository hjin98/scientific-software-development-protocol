---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.x skills-only candidate (7.2.0 per SD-R6)
decision_date_utc: 2026-10-07
status: stakeholder-adopted
decides: D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md §9 SD-R1..SD-R16
---

Governing SSDP version: 6.6.0.

# Stakeholder decision: 7.x reliability, simplification and calibrated qualification

**Verbatim answer.** "Approve your recommendation except SD-R2. We don't have that much budget. Stick with the flash model for the campaign. You may attempt a different model for comparison, but that must also be flash-tier such as the MiMo V2.6 flash or deepseek v4.1 flash. Proceed."

| # | Decision adopted | Realized in |
|---|---|---|
| SD-R1 | Calibrated philosophy and contract v2 replace the contract revision 16 floors. Fresh blind fixtures remain required. | `PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md` |
| SD-R2 | **As decided, not as recommended.** `GLM-5.3-Flash` is the gating executor. An optional comparison runs one other flash-tier model (MiMo V2.6 Flash or DeepSeek V4.1 Flash), descriptive only. | Contract v2 §2; design §4 |
| SD-R3 | Owner reads become optional depth; every required behaviour sits on the consumed surface | Design §3, §5.2 |
| SD-R4 (revised below) | Block limits: ≤ 3,000 B per role, ≤ 1,600 B per specialist; 6.6 text unchanged this cycle | Design §3; contract v2 Q5d |
| SD-R5 (revised below) | Harness retirement per design §6, only after the v2 harness passes its own acceptance; budget ≤ 5,000 non-test and ≤ 2,500 test lines | Workplan O-6 |
| SD-R6 | Version label 7.2.0; SD-1 subject re-identified after D4 | Workplan O-9 |
| SD-R7 | One rerun for provider-transport or harness failures, with both identities recorded; turn-cap and timeout count as behaviour. Replaces SD-7. | Contract v2 §3 |
| SD-R8 | The human comprehension trial is ratification evidence, not a gate | Contract v2 §1, §7 |

**Consequences of SD-R2:**
- **Re-derived exposures.** The flash executor's lower effect size (dev-probe rates: duty composite 0.25 → 0.50) required re-deriving the exposures. Q3 needs n ≥ 80 paired opportunities from ≥ 40 episodes. (Revision 2: these rates are planning assumptions, not dev-probe measurements (S0 B-5), and Q3 now needs ≥ 80 episodes with at most 2 opportunities each.) Q1 separates admissibility (instrument) from budget deaths (behaviour).
- **Compound with flash.** ~~A good candidate passes with probability 0.86; a no-effect candidate with ≤ 0.010.~~ These figures were superseded the same day. The S0 check (B-4) showed they assumed independent opportunities. The cluster-aware revision 2 figures are 0.818 (ICC 0.3) and 0.805 (ICC 0.5) for a good candidate, and ≤ 0.008 for a no-effect candidate; they assume SD-R9 is adopted. Revision 3 gives 0.821 (ICC 0.3) and 0.815 (ICC 0.5; 0.802 at four critical items per episode) for a good candidate, conditional on the Q5c backstop, and ≤ 0.008 for a no-effect candidate; they assume SD-R9, SD-R10 and SD-R11.
- **Cost.** It stays at the flash rate: about $4 per 184 runs in the dev probe.

**Scope.**
- These decisions authorize the workplan `workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md` once its S0 independent check passes.
- They change no release state.
- Protocol 6.6.0 remains accepted-current per `PROTOCOL-RELEASE-STATE.yaml`.

## Revisions after the S0 independent check (2026-10-07)

The S0 check (`INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07.md`) returned NO-PASS. Its SC-1 showed that the recorded basis for SD-R4 was false: the approximately 3 KB wording was lossy, not lossless. Its B-7 showed that the relay cannot be retired. The analyst put both to the stakeholder.

**Question 1.** "The independent check showed 'lossless' and '~3 KB block' can't both hold. A truly lossless D4 block is ~7.0 KB (7.1 was 8.2 KB). Which do you want?"
- **Answer:** "Lossless ~7 KB (Recommended)".

**Question 2.** "Keeping the observer … makes the 5,000-line harness budget unrealistic. Which budget?"
- **Answer:** "≤9,000 / ≤4,000 (Recommended)".

| # | Decision as revised | Realized in |
|---|---|---|
| SD-R4 (revised) | The block is lossless: it carries the full frozen §8.3 minimum. Hard limit: each generated block ≤ 95% of that entrypoint's 7.1 block. ~~D4 reference: 7,405 B against 8,174 B.~~ (Withdrawn: that wording was not lossless; see the revisions after the second S0 check below.) The 6.6 text is unchanged. | Design rev 2 §3, §5; contract v2 rev 2 Q5d |
| SD-R5 (revised) | Harness budget ≤ 9,000 non-test and ≤ 4,000 test lines. The provider relay is kept. | Design rev 2 §6; workplan rev 2 O-6 |
| **SD-R9 (adopted by the stakeholder, 2026-10-07)** | Recalibrate three 6.6 preservation rules to their measured noise: route probes at 19 × 3 runs with margin 4 and a 3/3 → 0/3 case guard; version cases at 8 × 3 runs with margin 5; T2/T3 sentinels as "no reproducible failure". Kept verbatim, an unchanged arm passes them ~~0.73–0.86 of the time, capping a good candidate's battery at about 0.42~~ 0.75–0.92 each and 0.58–0.63 together (four verbatim rules, including Q5f; corrected in revision 3 after the second S0 check, N-G4: the earlier figures were not computed by the script), which would hold a good candidate's compound to about 0.5. Recalibrated, each passes about 0.97, total loss is still detected, and a single lost route case is still caught about 89% of the time. The correction does not change the decision. | Design rev 2 §4.3, §9; contract v2 rev 2 Q5a, Q5b, Q5e |

**SD-R9 answer (2026-10-07).** Asked directly in the session that commissioned the second S0 check, the stakeholder chose "Adopt (Recommended)". SD-R9 is adopted as stated in the row above. The compound figures in this record (0.818 / 0.805; ≤ 0.008) already assumed it.

## Revisions after the second S0 check (2026-10-07)

The second S0 check (`INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07-R2.md`) returned NO-PASS. Two of its findings needed the stakeholder. The analyst asked both directly in the session.

**Question 3 (N-B1).** "The truly lossless block slightly exceeds SD-R4's hard limit of 95% of the 7.1 block (D4 7,786 vs 7,781 B; D3 8,743 vs 8,692; D1/D2 9,415 vs 9,332; documentation and audit fit). When losslessness and the byte limit conflict, which wins?"
- **Answer:** "Lossless wins; ≤100% hard (Recommended)".

**Question 4 (N-G3).** "The 6.6 'unversioned no-lookup' rule (0 violations in 9 runs on T1/T7/T8) was also recalibrated in rev 2 without being put to you. … Adopt the recalibration?"
- **Answer:** "Adopt (Recommended)".

| # | Decision as revised | Realized in |
|---|---|---|
| SD-R4 (revised again) | Losslessness governs. Hard limit: each generated block ≤ 100% of that entrypoint's 7.1 block (no growth). 95% is a compression target, not a gate. The measured span is frozen in design §5.1. Revision 3 reference measurements after the third check: D1/D2 9,814 / 9,823 B; D3 9,127 / 9,150; D4 8,147 / 8,192; documentation 5,080 / 5,451; audit 3,878 / 4,047. Matches the governing SD-B precedent ("a size budget is a compression recommendation, not a reason to break a lossless condition"). | Design rev 3 §3, §5.1, Appendix A; contract v2 rev 3 Q5d; workplan rev 3 O-4 |
| SD-R10 | Recalibrate the 6.6 unversioned no-lookup rule (0/9, none) to "3 runs per T1/T7/T8 route; a violation triggers 2 more runs of that route; fail if it recurs". Verbatim, an unchanged arm passes 0.914; recalibrated, 0.997. | Design rev 3 §3, §4.3; contract v2 rev 3 Q5f |

## Revision after the third S0 check (2026-10-07)

The third S0 check (`INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07-R3.md`) returned PASS WITH GAPS. Its N3-G1 showed that, with δ computed from the estimated p̂ as the contract specifies, a good candidate passes only 0.79 / 0.78. Asked directly in the session:

**Question 5 (N3-G1).** "How should it be restored? The cost of each option is weaker detection of a regression on the Q4 safety checks."
- **Answer:** "z 2.326 + floor 3 (Recommended)".

| # | Decision | Realized in |
|---|---|---|
| SD-R11 | δ(n, p̂) = max(3, ⌈2.326 · √(2 n p̂ (1 − p̂))⌉). A good candidate then passes 0.821 / 0.815 (ICC 0.3 / 0.5). Cost: a Q4 regression from 0.05 to 0.15 passes 0.44 (was 0.36); over-reporting on 5% of non-owed runs passes Q4d 0.54 (was 0.43). | Contract v2 rev 3 §5; design rev 3 §4.3, §4.4, §9 |

**Question 6 (N3-m4).** "Your 2026-09-28 backstop relaxation (2.0× the fresh paired 6.5 median on T1/T7/T8) was recorded 'for Protocol 7.0 only'. Should it apply unchanged to the 7.2.0 candidate, which is qualified under the same governing 7.0 workplan?"
- **Answer:** "Carry over 2.0× (Recommended)".

| # | Decision | Realized in |
|---|---|---|
| SD-R12 | The 2026-09-28 fixed-cost backstop applies unchanged to 7.2.0: 2.0 × the fresh paired accepted-6.5 median per T1/T7/T8 route, with the same accounting, run mode, counterbalancing, T7 rule, 512 B static margin and stop/escalation rule. | Contract v2 rev 3 Q5c; design rev 3 §9 |

## Decision after S0 PASS (2026-10-07)

**Verbatim instruction.** "Relax size limit <100% as soft target, while losslessness stays hard."

| # | Decision | Realized in |
|---|---|---|
| SD-R13 | Supersedes SD-R4's "≤ 100% hard". Losslessness of the frozen minimum is the hard requirement. Block size against each entrypoint's 7.1 block is a soft target (≤ 100%, with 95% as a goal), reported and not gated. Any excess must be attributable to lossless required content (the SD-B attribution rule); redundancy remains a D4 defect. The 2.0× fixed-cost backstop (Q5c, SD-R12) is unchanged and remains the binding size constraint. | Design rev 3 §0, §3, §5.1, §8, §9; contract v2 rev 3 Q5d; workplan rev 3 §2, §3, O-4 |

## SD-R14 (2026-10-07, after S2): harness budget

**Question put by D4** (S2 report `D4-PROTOCOL-7X-S2-IMPLEMENTATION-REPORT-2026-10-07.md`, section 2; stop trigger X4): the harness is 10,304 non-test and 4,541 test lines against 9,000 and 4,000, with H1–H5 intact. Option 1 was: "Accept the measured size (about 10.3k and 4.5k) as the H1–H5 floor for this OMP adaptation and revise SD-R5."

**Verbatim answer.** "Go with option 1."

| # | Decision | Realized in |
|---|---|---|
| SD-R14 | Supersedes SD-R5's "≤ 9,000 non-test and ≤ 4,000 test lines". The measured size, 10,304 non-test and 4,541 test lines on the design §6 scope, is accepted as the H1–H5 floor for the OMP adaptation. Any later growth is an additive repair that shows its line cost (X5). The relay, H1–H5 and the 6.6 comparison rules are unchanged. (The 205-line superseded script `operating_characteristics-R2-HISTORICAL.py` was moved out of the budget scope to `qual-v2-history/`; counting it would give 10,509 non-test lines.) | Design §6, §9 annotations; workplan §1, §3 and O-6 annotations; S2 report |

## SD-R15 (2026-10-07, after the independent S1-S3 Review): O-8 placement and the budget floor

**Questions put by D4** (S3 report `D4-PROTOCOL-7X-S3-IMPLEMENTATION-REPORT-2026-10-07.md`, section 3, in response to the Review's F-9):
1. O-8 placement: "amend the workplan so that [the O-8 inputs] belong to the S4/P3 custodian work order, and keep the synthetic Precondition C exercise in `qual-v2/test_h4.py` as S2 evidence."
2. Budget floor: "record the new measured floor, 10,364 / 4,672, in SD-R14" (the repairs to the Review's findings F-1 to F-7 and D-1 to D-3 add 60 non-test and 131 test lines to SD-R14's 10,304 / 4,541).

**Verbatim answer.** "Yes for both decisions."

| # | Decision | Realized in |
|---|---|---|
| SD-R15a | O-8 moves from S2 to the S4/P3 custodian work order: the 40-item evaluator calibration set with at least 10 known failures, the oracle known-good and known-bad fixtures and the version-redacted evaluator input are authored and frozen by the custodian under SD-2 custody. Their existence, and the re-freezing of the evaluator profile (currently pinned to the executor's own model) and of the executor profile (it still pins the retired ledger modules), are explicit S4 entry conditions. The synthetic Precondition C exercise in `qual-v2/test_h4.py` stays as S2 evidence. | Workplan O-8, §8 stages S2 and S4 |
| SD-R15b | SD-R14's accepted floor is 10,364 non-test and 4,672 test lines on the design §6 scope (the 205-line superseded history script, moved to `qual-v2-history/`, is not counted). Later growth is an additive repair that shows its line cost (X5). | SD-R14 row, design §6, workplan O-6 |

## SD-R16 (2026-10-07): X6 decision rule for the fixed-cost backstop (Q5c)

**Question put by D4** (the stakeholder asked for a recommendation on X6; the Q5c pre-measurement `qual-v2/Q5C-STATIC-PREMEASUREMENT-2026-10-07.md` shows 409 B of headroom for the D4 entrypoint and a breach if a median T1/T8 run also reads the 46,131 B scientific-inspectability owner). D4 recommended four items.

**Verbatim answer.** "Ok let's go with item 1-4 for now."

| # | Decision | Realized in |
|---|---|---|
| SD-R16.1 | **Pre-registered rule.** S4 measures q, the per-run rate of reading the scientific-inspectability owner on T1 and T8. With q the per-run probability, a route's median of three runs reads the owner with probability 3q²(1−q)+q³, so the unconditional pass probability is the conditional compound (0.821 at ICC 0.3, 0.815 at ICC 0.5) times the square of one minus that. The design rule (at least 0.80) holds up to q = 6.7% at ICC 0.3 and 5.7% at ICC 0.5. If measured q is at most 6%, proceed unchanged; between 6% and 15%, return to the stakeholder; above 15%, treat it as a surface-wording problem, not a cap problem. The estimate is reported with its Wilson 90% interval. | Design §10 X6; workplan S4 gate |
| SD-R16.2 | **Named fallback (not adopted).** If the rule sends the question back, the least-bad relaxation is to make owner reads on T1 and T8 descriptive (reported, not gated). It weakens the backstop's fixed-cost purpose. Raising the multiplier (about 7× to absorb the read) is rejected. | Design §10 X6 |
| SD-R16.3 | **No growth of the D4 entrypoint.** It leaves 409 B under the Q5c limit; any later change that adds text to it needs the stakeholder's prior approval. | Design §10 X5; freeze record |
| SD-R16.4 | **Accounting.** Q5c still gates on the conservative consumed-bytes count (contract §3). S4 reports, per run, the bytes from native reads and the bytes from shell counting separately, so a run that only lists the package is visible as an accounting artifact. | Workplan S4; freeze record |

The contract is unchanged: SD-R16 pre-registers how a measurement will be read; it changes no gate, threshold or exposure.
