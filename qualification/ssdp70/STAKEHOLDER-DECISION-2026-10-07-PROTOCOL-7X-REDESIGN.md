---
kind: stakeholder-decision-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.x skills-only candidate (7.2.0 per SD-R6)
decision_date_utc: 2026-10-07
status: stakeholder-adopted
decides: D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md §9 SD-R1..SD-R13
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
