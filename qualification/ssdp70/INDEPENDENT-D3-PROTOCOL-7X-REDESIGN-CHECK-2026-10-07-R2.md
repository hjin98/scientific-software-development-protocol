---
kind: independent-d3-check
governing_protocol_version: 6.6.0
subject:
  - qualification/ssdp70/D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md (revision 2)
  - qualification/ssdp70/PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md (revision 2)
  - qualification/ssdp70/qual-v2/operating_characteristics.py (revision 2)
  - workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (revision 2)
checked_against: STAKEHOLDER-DECISION-2026-10-07-PROTOCOL-7X-REDESIGN.md, SD-R1..SD-R9 (not re-litigated)
round: 2
round_1_record: INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07.md
date_utc: 2026-10-07
checker: independent context; authored nothing under review
role_text_used: software-design SKILL.md as accepted at 6.6.0 (22f4bdba, per PROTOCOL-RELEASE-STATE.yaml); source/ is at 7.1.0 and was read only as the subject's baseline
---

Governing SSDP version: 6.6.0.

# Independent D3 check, round 2: Protocol 7.x redesign and contract v2

## Verdict

**NO-PASS.** No SERIOUS CHALLENGE. Three blockers (N-B1 to N-B3), eight gaps and nine minors. Revision 2 repairs most of round 1. The three blockers are new or residual, and each has a small repair:

- **N-B1.** The "lossless" Appendix A still drops frozen-minimum meanings. With them restored, the 95% limit is met by no margin or missed on three of six entrypoints.
- **N-B2.** The Q5c backstop is called "verbatim" but changes the stakeholder-fixed accounting and drops its operative parts.
- **N-B3.** The governing workplan's §12–§14 still require the mandatory owner load and the absolute floors, and they are not on the amendment list.

The workplan must not go to S1.

## SERIOUS CHALLENGE

None. SD-R4 as revised (a lossless block, ≤ 95% of the 7.1 block) is not shown to be unrealizable. My restored-lossless estimate sits within 0.1–0.9% of the limit, so D4 compression may still fit. Its recorded basis, however, is again misreported (N-B1). If D4 cannot meet both conditions, this becomes a SERIOUS CHALLENGE to SD-R4 at the stakeholder.

## Round-1 repair verification (checked against the revision-2 bytes)

| Item | Verdict | Basis |
|---|---|---|
| SC-1 | PARTLY | The stakeholder chose a lossless block. The "gloss" row is gone, and design §3/§5.2 no longer demote required meaning. But Appendix A, the stated lossless reference and the source of the 7,405 B figure behind SD-R4 as revised, still drops label-table meanings (N-B1). |
| B-1 | REPAIRED | Contract §3:47-51 scores against the frozen §8.3 list, not D4 wording. Workplan O-3:123 adds a mapping file, a static test and an independent check. |
| B-2 | PARTLY | Owner lines 29, 33 and 389 and the §8.2/§8.3 R2 sentences are now listed (design §3:88-91). Still in force and unlisted: governing workplan §11:989, §12 Stage B/D (1011, 1027), §13 items 13–14 (1106-1107) and §14 (1123). See N-B3. |
| B-3 | PARTLY | The limit is now relative to each entrypoint's own block. Only the D4 variant was measured. Appendix A fits all six variants, but the lossless restoration does not (N-B1). |
| B-4 | PARTLY | Q2 and Q3 are now cluster-aware (episode random effect; per-episode sign test). The Q4 item-count gates still assume independent items (N-G1). |
| B-5 | REPAIRED | Relabelled as an assumed minimum material improvement (design §4.4:139-143). Sensitivity reproduced (0.817 / 0.514 at +20 / +15 pp). S4 re-sizes the exposures (X1). |
| B-6 | DISPUTE-UPHELD on the backstop figure; otherwise REPAIRED | See the ruling below. The `max(·, δ)` construction is gone, and the recalibration is listed (§3:97) and adopted by the stakeholder (SD-R9). New residuals: N-B2 and N-G3. |
| B-7 | REPAIRED | H1 (design §6:212) keeps the relay with credential separation, single-endpoint egress with refusal logging, the activation proof and the turn cap. `seccomp70.py` is kept. O-6:126 requires a real bubblewrap launch through the relay. Residual: N-G7. |
| G-1 | REPAIRED | B1 is the interleaved baseline and B2 serves only p̂. C is limited to two attempts. C(b)'s false-failure rate is computed. Residual: a 0.90-agreement evaluator fails C(b) 26% of the time per attempt. |
| G-2 | REPAIRED | 35/40 and 8/10, with discrimination computed (0.975 / 0.738 / 0.355 / 0.109). Bias and blinding limits stated. |
| G-3 | REPAIRED | Q4c at base 0.33 reproduces (margin 13; +12 pp passes 0.742). Residual: N-m1. |
| G-4 | REPAIRED | The ambiguity rule is removed. Q5e/Q5f extra runs are modelled. |
| G-5 | PARTLY | Disposition-specific Q3 scoring and per-family reporting are added. The new Q4d is mis-calibrated against a 6.6 baseline (N-G2). |
| G-6 | REPAIRED | All four items are listed in §3. New unlisted items: N-B3 and N-G3. |
| G-7 | REPAIRED | Design §8:258-262 and workplan O-9:129. |
| G-8 | REPAIRED | Design §11 dispositions all five `main` entries (DS-001, FF-001, PC-001, SP-001, SP-002). |
| G-9 | PARTLY | Sentinels, Q2b, Q5f and Q1a are modelled. Q5c is asserted as 0.99, not derived (`operating_characteristics.py:192`), and is the check most at risk (N-B2). "13 cluster-modelled checks" overstates it: only Q2 and Q3 carry an episode effect. |
| G-10 | REPAIRED | Budget revised to 9,000 / 4,000. Retained-line arithmetic verified: 12,650 = 20,279 − 7,629. |
| G-11 | REPAIRED | Mapping test, quantified X1, and an S4 threshold computed for the actual n. |
| G-12 | REPAIRED | The tension question has its qualifier and label meaning, and the gap rule has its exemptions and the partial-answer rule (Appendix A:347-349). |
| m-1 | PARTLY | See N-m3. The per-opportunity shared-`u` mixture remains and is undocumented. |
| m-2 | REPAIRED | Workplan front matter corrected. |
| m-3 | REPAIRED | O-2 covers `dist/`. |
| m-4 | REPAIRED | Q5c has no count margin. |
| m-5 | REPAIRED | 788 + 1,700 + 5,141 = 7,629. |
| m-6 | REPAIRED | The block sits at the 7.1 completion position. |
| m-7 | REPAIRED | Disclosed in L9. Residual: the stated "about 10%" saving comes from lossy wording; the lossless saving is about 0–5%. |

## B-6 dispute ruling

**Upheld on the number.** The backstop in force is 2.0×, not 1.10×. Sources:
- governing workplan header line 18 (`stakeholder_sd_b_confirmation`);
- §0 line 28: "replaced … 1.10 multiplier with 2.0 … Read every older 1.10 fixed-cost statement … including frozen §8.3, as superseded";
- `STAKEHOLDER-DECISION-2026-09-28-PROTOCOL-7.0-BACKSTOP-RELAXATION.md`.

Round 1 read the frozen §8.3:632 bytes without that override.

**The same sources also fix what stays operative.** The decision keeps:
- the denominator, measured in 6.6 run mode;
- "the same accounting";
- counterbalancing;
- the T7 mode-replication rule;
- the 512 B static margin;
- the stop/escalation rule.

Contract v2 Q5c drops or changes several of these while calling the backstop "verbatim" (N-B2). The dispute succeeds on the multiplier only.

## New findings

### Blockers

**N-B1. Appendix A is not lossless, and the lossless block may not fit the 95% limit.**
- **Where.** Design §0:36, §3:92, §9:273, §12:305/308, Appendix A:334-357; stakeholder record :49.
- **Evidence.** Each meaning below is in the frozen label table or §8.3 and in the 7.1 block, and absent from Appendix A (checked by grep):
  - Change-only relief: "when it finds nothing, adds nothing" (workplan:607).
  - Feedback persistence (:608):
    - "later status changes go to that home" (7.1: "update that home");
    - "decision-sufficient content";
    - "leaves required persistence unresolved";
    - "searchable";
    - "the account it is written through does not show this". This last one is also missing from element 3 (:616).
  - O1 content (:620): "draft or unaccepted text does not bind"; "answered through agent reports only" / "None" valid.
  - Short form (:621): "no retention/projection change" completes only that statement.
  - Authority identity (:613): heading/object ID, and "claim or locator". Element 1 drops "claim"; element 3 drops "locator".
  - Re-evaluation when a new effect arises (:629; 7.1 "Re-evaluate if new effects arise").
- **Measurement.**
  - I restored only these, minimally, into Appendix A: 7,405 → 7,786 B.
  - I then built each variant: element 7 (957 B) and element 5 (672 B) taken verbatim from 7.1; the specialists by deletion from the restored text.
  - The limit is 95% of each 7.1 bullet-plus-completion block, which I measure at 8,191 B for D4, not the design's 8,174.

| Entrypoint | Appendix A as written | Restored (lossless) | Limit |
|---|---|---|---|
| D4 | 7,405 | **7,786** | 7,781 (7,765 on 8,174) |
| D3 | 8,362 | **8,743** | 8,692 |
| D1/D2 | 9,034 | **9,415** | 9,332 |
| documentation | 4,565 | 4,946 | 5,178 |
| maintenance audit | 3,487 | 3,772 | 3,845 |

  The (a)–(c) sentence that was added (~300 B, owner depth under §8.3:630) is what pushes the role variants over.
- **Failure scenario.**
  - D4 starts from Appendix A, as design §5.1 tells it to.
  - The independent mapping check (O-3) finds the missing meanings. Restoring them breaks O-4 on three roles.
  - O-4's "shortcut to reject" forbids moving meaning to the owner. No rule says whether losslessness or the hard limit wins, so D4 either cuts again or stops.
  - SD-R4 as revised was decided on "7,405 B lossless", which is the same misreported-basis defect as round-1 B-3.
- **Minimal repair.**
  - Correct Appendix A (or mark it lossy) and the 7,405 figure everywhere it is cited.
  - Measure lossless wording for all six variants.
  - State a precedence rule: losslessness governs, and a block that cannot meet its limit losslessly goes to the stakeholder.
  - Either put the true figures to the stakeholder, or drop the (a)–(c) sentence, which is not frozen minimum, to recover about 300 B.
  - Freeze the exact byte span the limit is measured on.

**N-B2. The Q5c backstop is not verbatim. Its accounting would omit the entrypoint itself.**
- **Where.** Contract §3:62, §5:95; design §0:52, §3:102.
- **Evidence.**
  - Contract §3 counts "native read events, plus every shell command touching the package path".
  - The operative accounting is 6.6 `entry_and_burden`: "bytes of every invoked SSDP entrypoint as installed + bytes of SSDP files actually read" (`qualification/ssdp66/eval/harness.py:332`; 2026-09-28 decision: "same accounting").
  - Under the profile's `harness-injection` activation, the installed `SKILL.md` goes into the prompt (`eval/adapters/omp.py:1094-1098`) and is never a native read.
  - Q5c also omits the 512 B static margin, the pre-run static measurement, the T7 mode-replication rule and the counterbalancing. All remain operative per the 2026-09-28 record and workplan line 28.
  - The script hard-codes Q5c = 0.99 (`operating_characteristics.py:192`).
- **Failure scenario.**
  - Expected 7.2 D4 installed entrypoint: 15,463 − 8,191 + ~7,786 ≈ 15.1 KB.
  - Static limit on the historical 6.5 median: 16,208 B. That leaves about 1.1 KB headroom.
  - Under v2's accounting the entrypoint counts as 0 B, so the backstop is close to vacuous. Under the operative accounting, any median run that reads the owner (45,958 B; L3 shows Flash reads it "to be safe") breaches it.
  - Neither outcome is visible before the campaign, and the 0.99 in the compound is unsupported.
- **Minimal repair.**
  - Define Q5c accounting as 6.6 `entry_and_burden`, with the injected entrypoint counted as installed.
  - Carry the 512 B margin, the static pre-measurement at D4 (add it to design §8), the T7 rule and the counterbalancing.
  - Derive or justify the Q5c pass figure, or report it as an unmodelled risk.

**N-B3. The governing workplan still carries the old mandatory owner load and the absolute floors outside the amended sections. The (a)–(c) inlining conflicts with §8.3 text marked "not reopened".**
- **Where.** Workplan front matter :6 ("amends §8.2, §8.3, §11"); O-5:125; design §3:100-103.
- **Evidence.**
  - Governing workplan §13 item 13 (:1106) requires "the §8.2 … owner-load trigger … realized, including R1/R2".
  - §13 item 14 (:1107) requires "both absolute adequacy floors".
  - §12 Stage B/D (:1011, :1027) and §11:989 require R1/R2 in place.
  - §8.3:630 says the owner supplies "the (a)-(c) blocking conditions" as depth and "The owner's doctrine is not inlined (I66-3)".
  - §8.3:631 makes "inlined owner doctrine" a D4 defect under the attribution rule, which design §3:101 says is not reopened.
  - Owner line 389 keeps "It is not inlined". Design §3:91 amends only part of that line.
- **Failure scenario.** After S1, either:
  - O-5's consistency test fails on §12/§13 text that the workplan does not authorize D4 to edit; or
  - 7.2 can never meet governing §13 item 14 under contract v2.

  Both are simultaneously applicable current meanings with no owner reconciliation.
- **Minimal repair.**
  - Add §11:989, §12 Stage B/D, §13 items 13–14 and §14 (:1123) to design §3 and to the workplan's `amends`.
  - List the §8.3:630/631 I66-3 and attribution sentences as reopened for the (a)–(c) sentence, or drop that sentence (see N-B1).

### Gaps

- **N-G1. The Q4 item gates are not cluster-modelled.**
  - Where: contract §5:89-92; script `ni()`.
  - Q4a counts ≥ 40 critical items, and Q4b/Q4d count violations and disclosures, but `ni()` treats each unit as an independent pair.
  - My simulation (arm-specific episode effect, p = 0.10, margin δ(40, 0.10) = 6) gives a Q4a A/A pass of:

| Items per episode | ICC 0.3 | ICC 0.5 |
|---|---|---|
| 1 | 0.993 | 0.993 |
| 2 | 0.984 | 0.974 |
| 4 | 0.953 | 0.940 |

  - Q4d at 2 items per episode: 0.976 (ICC 0.3) and 0.965 (ICC 0.5).
  - Scenario: at 4 items per episode and ICC 0.5, the good-candidate compound falls from about 0.81 to about 0.74, below the ≥ 0.80 design rule.
  - Repair: define the Q4a/Q4b/Q4d units as per-run indicators, or cluster-adjust δ (design effect), and model it.
- **N-G2. Q4d is effectively an absolute cap, and its 0.99 assumes equal rates.**
  - Where: contract :92; script :190.
  - 6.6 (B1/B2) produces essentially no Protocol 7 nulls or envelopes, so p̂ ≈ 0 and δ = 2.
  - With B1 at 0.005, a candidate over-reporting on 2%, 5% and 10% of non-owed runs passes 0.84, 0.31 and 0.03.
  - This reintroduces the L4/L5 uncalibrated-floor problem.
  - The Q2b rate (0.02 unowed parts) is likewise unsourced.
  - Repair: calibrate Q4d's base from S4 on the candidate, or state it as an absolute rule with its own operating characteristic.
- **N-G3. Q5f is recalibrated without being listed.**
  - Where: contract :98; design §3:97; SD-R9.
  - 6.6's rule is "unversioned no-lookup 0/9 … none" (`ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md`, final table). v2 makes it "reproducible failure". Neither §3 nor SD-R9 (three rules) lists it.
  - Repair: list it and record the stakeholder's decision. Under the script's calibration the verbatim rule passes 0.913.
- **N-G4. The SD-R9 record's "verbatim" figures are not produced by the cited script.**
  - Where: stakeholder record :51; design §9:278, L5:64.
  - The script computes only the version rule (0.731–0.748).
  - Under the script's own calibration (hit mean 0.95):
    - verbatim route probes (19×2, hits ≥ basis − 2): 0.914;
    - sentinels (all 4 pass): 0.923;
    - battery with the three verbatim rules: about 0.55 (about 0.50 with the no-lookup rule too). The record says 0.42.
  - 0.86 reproduces only with independent binomial probes at p = 0.92, the candidate arm's own rate. That calibration is inconsistent with the recalibrated model's 0.95.
  - The SD-R9 decision does not change, because the verbatim rules still break the ≥ 0.80 rule. But the adopted record carries unsourced figures.
  - Repair: add the verbatim computations to the script and correct the record.
- **N-G5. The description contradicts the 6.6 byte-identity rule.**
  - Where: design §8:248-250; contract Q5d:96; O-2:122.
  - The 7.1 `software-implementation` description differs from 6.6 (466 B against 252 B). "6.6 text byte-identical outside the block" and "description unchanged from 7.1" cannot both hold.
  - Governing §8.3:631 exempts "the description amendment", but v2 never says so.
  - Repair: state that exemption explicitly.
- **N-G6. Appendix A's depth line reads as mandatory, and its (a)–(c) sentence changes the owner's default.**
  - Where: Appendix A:341, 354.
  - "read it before a consequential judgment …" is imperative. Placed beside "These checks are the complete obligation", it is the L3 pair that Flash resolved both ways, and O-5 forbids it.
  - "otherwise qualify the judgment" contradicts the owner (:300-302): disclosure suffices by default, and a home qualifies only when designated or evidently used.
  - Repair: word the depth line as optional ("for definitions and examples, see …"), and keep the owner's default/qualify/block structure.
- **N-G7. Retiring `stand_in_provider.py` breaks the O-6 integration test.**
  - Where: design §6:224; O-6:126.
  - It is the deterministic provider used by `test_activation_accounting.py`.
  - Without it, the required relay integration test (activation proof, turn cap, egress refusal) needs live paid provider calls and becomes nondeterministic.
  - Repair: keep it, counted against the test budget, or name its replacement.
- **N-G8. The release documents keep the old doctrine.**
  - `README.md:99` and `source/README.md:41` say entrypoints carry the "owner-load trigger".
  - O-9 requires only "README routes intact", but AGENTS.md documentation closeout requires recompiling the README.
  - Repair: add a README/source-README update to O-9, and to O-5's consistency scope.

### Minors

- **N-m1.** Design §4.4:153 and contract :118 put the Q4a margin at 40 items at 5. The script prints 6 at its modelled base of 0.10; the margin is 5 only when p̂ ≤ 0.08.
- **N-m2.** In contract Q3:88, "0.15 n" does not define n. The script uses opportunities (160 → 24). If H4 used episodes (80 → 12), the null pass rises from 0.004 to 0.035.
- **N-m3.** The `--icc` value is not the model's correlation.
  - Measured within-arm intra-episode correlation: 0.36 at nominal 0.3, and 0.63 at nominal 0.5. The between-arm pairing correlation is about 0.03.
  - `q5b_*` hard-code 0.3 (:92, :104).
  - The docstring does not document the shared-`u` mixture (:50-53, :65-67).
- **N-m4.** `K_Q2 = 34` is fixed (:17). The comment says re-derivation gives 33–34. P(pass | 0.85) is 0.970–0.976 at ICC 0.3, at the 0.97 criterion, and 0.948–0.958 at ICC 0.5.
- **N-m5.** The compound is a product of marginals across gates that share B1 and the same runs. This is probably conservative, but it is unstated. The Monte Carlo error is about ±0.01: ICC 0.5 gives 0.805 at 3,000 trials, 0.818 at 4,000 and 0.809 at 20,000. The margin over 0.80 is inside that noise, so fix the trials and seed for the quoted figures.
- **N-m6.** The scope of the harness line budget is undefined: `eval/` only, or also `requal71/` and `qual-v2/`.
- **N-m7.** Design §3:101 says the "frozen §8.3 minimum" is not reopened, yet R2 is part of it (§8.3:630, "R1, R2 and the required clause elements … complete minimum").
- **N-m8.** Stale text:
  - The stakeholder record front matter :7 says "SD-R1..SD-R8".
  - Design §9:278 and record :51 still end the SD-R9 row with "Recommendation: adopt" after adoption.
- **N-m9.** Design §3:95 says the selection surface is "untouched". That holds relative to 7.1 only. Against accepted 6.6, the implementation description is widened, and under deterministic activation selection is not exercised at all. This is listed, but the wording overstates it.

## Operating-characteristics reproduction

Commands, run with python3 from the repository root:

```
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 4000
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 4000 --icc 0.5
python3 qualification/ssdp70/qual-v2/operating_characteristics.py            # default 3000
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --icc 0.5  # default 3000
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000 [--icc 0.5]
```

My own checks are in the scratch scripts `oc_check.py` and `blocks.py` (session scratchpad, not committed).

| Figure | Stated | Reproduced |
|---|---|---|
| Good compound, ICC 0.3 | 0.818 | 0.821 (3k), 0.818 (4k), 0.820 (20k) |
| Good compound, ICC 0.5 | 0.805 | 0.805 (3k), 0.818 (4k), 0.809 (20k) |
| No-effect (Q3 null bound), ICC 0.3 / 0.5 | ≤ 0.005 / ≤ 0.008 | 0.003–0.005 / 0.007–0.010; 20k: 0.0043 / 0.0068 |
| Q2 ≥ 34/48 at 0.85 | 0.97 | 0.970–0.976 (ICC 0.3); 0.948–0.958 (ICC 0.5) |
| Q3 sensitivity, +25 / +20 / +15 pp | 0.95 / 0.82 / 0.51 | 0.953 / 0.817 / 0.514 |
| Q4 limits | 0.72 / 0.35 / 0.71 / 0.74 | 0.720 / 0.347 / 0.710 / 0.742 |
| Q4a margin at 40 | 5 | 6 at p = 0.10; 5 at p ≤ 0.08 (N-m1) |
| Verbatim version rule | 0.73 | 0.731–0.748 |
| Verbatim route-probe rule | 0.86 | not in script; 0.914 under the script's calibration; 0.859 only with binomial p = 0.92 (N-G4) |
| Verbatim battery cap | ~0.42 | not in script; ≈ 0.50–0.55 by my composition (N-G4) |
| Recalibrated Q5a / Q5b / sentinels | ~0.97 | 0.965–0.973 / 0.964–0.970 / 0.992–0.997 |
| One lost route case detected | ~89% | passes 0.113–0.124, so detection 0.88–0.89 |
| Q5b halving / total loss | 0.30 / ≤ 0.004 | 0.28–0.30 / 0.002–0.004 |
| C(b) at 0.95 / 0.90 / 0.85 / 0.80 | 0.975 / — / — / 0.11 | 0.975 / 0.738 / 0.355 / 0.109 |
| C(c) gross screen | ≈ 1.00 | 0.999–1.000 |

**Derivation check.**
- The sign test (one-sided exact, over episodes with a nonzero difference) is valid under the null whatever the within-episode correlation, because episodes are independent and the arms exchangeable. The no-effect bound is therefore sound.
- δ is the one-sided 98% normal quantile for a difference of two binomials. It is correct under independence, but not for clustered items (N-G1).
- The Q2 structure matches the dev probe: 47 owed parts from 12 episodes (11 × 4, 1 × 3).
- The Q5f model (9 × `sentinel_route`) does not match the rule as specified (3 routes × 3 runs, a recurrence within 2 reruns). The effect is negligible: 0.9980 as specified against 0.9963 modelled.

## Checked and found sound

- No self-acceptance. Release state untouched. Governing version 6.6.0 stated in every subject file. S0 is gated on this check, and SD-R9 is recorded as adopted.
- The scored minimum is decoupled from D4 wording (B-1). The interleaved B1 baseline, the limit of two C attempts and the removal of adaptive replicates are coherent.
- H1–H5 cover the run, the relay functions and integrity. The retained-line arithmetic matches `qualification/ssdp70/eval/` (20,279 non-test, 9,556 test).
- PEM HAS dispositions cover every `main` entry. The FF-001/PC-001 version boundary (7.2.0 identity frozen only after S1–S3 review; 7.1.0 preserved and given a terminal disposition) is sound.
- The 7.1 blocks at `58fd67b` equal those at HEAD. Per-entrypoint 7.1 block sizes: D1/D2 9,823 B; D3 9,150; D4 8,191; documentation 5,451; audit 4,047.
- Design, contract, workplan and stakeholder record agree on every gate number, exposure and compound figure, apart from the items above.

## Could not check

These are blocking only where noted. None is required of an S0 design check, but each is a required check at its own stage.

- **Live OMP behaviour.** Relay, activation proof, turn cap and egress refusal under OMP 18.x. Not checked: no live runs, per the brief. Required at S2 (O-6).
- **Whether D4 can compress the restored lossless text under the 95% limit.** I give an estimate, not wording. It decides whether N-B1 escalates to a SERIOUS CHALLENGE.
- **Whether the 7.1 block is itself fully lossless.** I used it as the restoration reference, so further omissions would enlarge N-B1.
- **Whether the 6.6 route-probe (P01–P19), version (T4–T6), sentinel (T2/T3) and burden (T1/T7/T8) panels are ported to OMP/Flash.** Their realism decides the SD-R9 calibration inputs.
- **The real ICC, items per episode for Q4a/Q4d, and the base rates of unowed disclosures.** These come from S4. The dev-probe advisory items are unadjudicated.
- **Repository acceptance.** Not run: nothing under `source/` changed in this subject.
