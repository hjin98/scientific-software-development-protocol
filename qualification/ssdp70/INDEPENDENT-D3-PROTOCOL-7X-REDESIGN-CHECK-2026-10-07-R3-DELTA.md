---
kind: independent-d3-check
governing_protocol_version: 6.6.0
subject: minimal-delta repair of the round-3 findings (N3-G1..G5, N3-m1..m7), uncommitted, in the design (rev 3, §12b), contract v2 rev 3, qual-v2/operating_characteristics.py, workplan rev 3 and the stakeholder record (SD-R11, SD-R12)
checked_against: INDEPENDENT-D3-PROTOCOL-7X-REDESIGN-CHECK-2026-10-07-R3.md; STAKEHOLDER-DECISION-2026-10-07-PROTOCOL-7X-REDESIGN.md SD-R1..SD-R12 (not re-litigated)
round: 3-delta
date_utc: 2026-10-07
checker: independent context; authored nothing under review
---

Governing SSDP version: 6.6.0.

# Independent delta check of the round-3 repairs

## Verdict

**PASS WITH GAPS.** No SERIOUS CHALLENGE and no blockers. Every round-3 finding is repaired in the bytes. The back-references in elements 3 and 6 are lossless, and every variant fits the hard limit.

This check also found two gaps. Both predate the delta; round 3 missed them. Both sit in the static acceptance definitions that D4 would test against (§5.1 span; O-2/Q5d). Each needs a one-sentence repair before S1. Neither changes a figure, so the S1 independent mapping check and the S3 D4 Review can confirm the repairs.

## Repair verification (against the bytes)

| Finding | Verdict | Basis |
|---|---|---|
| N3-G1 | REPAIRED | `ni_runs`/`ni_items` (script :90-111) estimate p̂ from simulated B1+B2, and δ = max(3, ⌈2.326·√…⌉) (:36-44). SD-R11 is recorded with its costs. Every figure reproduces (table below). Design §0, §4.3 and §4.4, contract §5 and record :29 are consistent. |
| N3-G2 | REPAIRED | Design Appendix A :423-427 restores all six items: custodian/destination; former names or paths; external/product contract; the shared-account wording "neither which human or agent … nor any dispositioning authority"; "visibly"; and "other indications qualify the judgment". It also adds the "local count" clause and the change-only relief "except answers its delegator asked for and gaps owed for its delegates", which now matches the frozen row. See the back-reference check below. |
| N3-G3 | REPAIRED | Principle 5 (design :79), contract §1:30 and workplan :31 state the conditional rule, the S4 estimate of P(Q5c pass) and the unconditional report before the campaign. |
| N3-G4 | REPAIRED (residual D-m2) | §0:28, §13.16, Stage G :1068 and owner :35 are in design §3:96 and workplan `amends` :6 and O-5. The (a)–(c) rule joins the frozen minimum through a new label-table row, and the §8.3:630 depth list drops it (design §3:92). |
| N3-G5 | REPAIRED | Workplan :92 and :185 read X1–X6. |
| N3-m1 | REPAIRED | Appendix :425, "owner or acceptance authority of that authority". |
| N3-m2 | REPAIRED | Via N3-G4. |
| N3-m3 | REPAIRED | Design §5.1, "Five of six". |
| N3-m4 | PARTLY | The carry-over is decided (SD-R12). The run mode is named as "6.6 run mode", which conflicts with the deterministic-entry overlay (D-m1). |
| N3-m5 | REPAIRED | Record :49 strikes and annotates the figure. |
| N3-m6 | REPAIRED | Design m-7 row. |
| N3-m7 | REPAIRED | Docstring :5-7. My recomputation gives SE ≈ P·√(Σ(1 − pᵢ)/(pᵢN)) ≈ 0.003. The word "summed" should read "combined in quadrature" (cosmetic). |

### Back-references in elements 3 and 6 (scope item 1)

- **Element 3 (:425).** It reads "with its asserter stated in content as in element 1". Element 1 (:423) states "asserter stated in its content as human or AI and which agent (the writing account does not show this)". That is the full frozen written-record asserter row, account clause included. Element 3 is carried only by the four roles, all of which carry element 1. **Lossless.**
- **Element 6 (:427).** It reads "cite the exact element-4 source (authority, instruction or contract)". Element 4 (:426) lists "accepted authority, explicit stakeholder/task instruction or an existing external/product contract", which is exactly the frozen consequential-choice-status row. Element 6 is carried by the four roles and by documentation (role map 1, 4, 6), all of which carry element 4. **Lossless.** The reference is in fact stronger than the earlier "the accepted authority, explicit instruction or contract".
- **Condition.** Both references depend on the generated block keeping the element numbers 1 and 4 as visible labels. The fragment and role map do keep them. O-3's mapping test should assert this, so that a later renumbering cannot break the reference silently.

### Hard limit (scope item 2)

My `variants.py` rebuild from Appendix A matches the author's figures within 1 B on the roles and 13 B on the specialists; mine are smaller on the specialists. All six variants are within ≤ 100%.

| Entrypoint | Rebuilt | Stated | Limit | Margin (stated) |
|---|---|---|---|---|
| D1/D2 | 9,815 | 9,814 | 9,823 | 9 B |
| D3 | 9,128 | 9,127 | 9,150 | 23 B |
| D4 | 8,148 | 8,147 | 8,192 | 45 B |
| documentation | 5,067 | 5,080 | 5,451 | 371 B |
| audit | 3,865 | 3,878 | 4,047 | 169 B |

A 9 B margin on D1/D2 leaves D4 almost no room. Design §5.1 states the stakeholder route for an omission that cannot be restored, which is the correct rule.

## New findings

### Gaps (predate the delta; missed in round 3)

**D-G1. The frozen span measures the source file, but under O-1 the block is not in the source file.**
- **Where.** Design §5.1 :179 (generation by marker injection, "reusing the `SSDP-ENTRY-CONTRACT` mechanism"), :202 (span = "lines the entrypoint's `source/` file adds relative to `22f4bdba`"); O-1 :121 rejects hand-editing the blocks; O-4 :124; contract Q5d.
- **Evidence.** Under the `SSDP-ENTRY-CONTRACT` mechanism, `source/…/SKILL.md` holds only the placeholder, and `build_skills.py` expands it into `dist/` (`source/build_skills.py:38`; `source/roles/software-implementation/SKILL.md:10`). After S1, the source file adds only the marker line (about 50 B). The O-4 "static test on the frozen span" would then pass vacuously for any block size.
- **Repair.** Measure the generated `dist/skills/<entrypoint>/SKILL.md` against `22f4bdba` `dist`, excluding the `description:` line and the generated `**Governing version.**` line. I verified that this measure at `58fd67b` gives exactly the stated 7.1 references: 9,823 / 9,150 / 8,192 / 5,451 / 4,047. No figure changes.

**D-G2. "6.6 text byte-identical in `dist/` apart from the description" cannot be met.**
- **Where.** Contract Q5d :96; O-2 :122; design §8 :272-274.
- **Evidence.** The generated entry contract carries the package version. Between `22f4bdba` and `58fd67b` the `dist` D4 entrypoint differs outside the block in two lines: the description, and "**Governing version.** This package is SSDP `6.6.0`" → `7.1.0`. In 7.2 that line must read `7.2.0` (O-9), so O-2/Q5d as written fail on every `dist` entrypoint.
- **Repair.** Name the generated governing-version line as the second sanctioned exception.

### Minors

- **D-m1. "6.6 run mode" conflicts with the activation overlay.** Contract Q5c (:95) says "in 6.6 run mode", and SD-R12 repeats "same … run mode". Governing §0 :174 (2026-10-04 activation overlay) runs T1/T7/T8 on deterministic entry, and contract §2 runs every arm under one OMP deterministic-activation profile. H1 provides no other mode. State that "run mode" here means 6.6's measurement procedure (fresh paired, counterbalanced, per-mode reporting) under the v2 profile's deterministic entry.
- **D-m2. Old floors survive in the §0.1 overlay text.** The activation-overlay list (governing :170-172) still keeps "floors" and "predicate/owner false-activation floors" on profile runs. These overlay items are current for 7.0/7.1 but not in `amends`. Annotate them with the §0:28 change.
- **D-m3. The new label-table row has no wording.** The row "inaccessible home (element 3)" (design §3:92; O-5) is a frozen-table amendment, but its text is not given. Specify it, or state that it reproduces owner :300-308 (default, qualify, block (a)–(c), other indications qualify and go to the human).
- **D-m4. The m = 4 compound sits on the rule.** At ICC 0.5 and m = 4 the compound is 0.802, within one Monte Carlo SE (about 0.003) of 0.80. It is a sensitivity case, not the planning assumption, but it should be labelled "at the rule" rather than read as meeting it with margin.

## Operating-characteristics reproduction (20,000 trials, fixed seed)

```
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000 --icc 0.5
python3 qualification/ssdp70/qual-v2/operating_characteristics.py --trials 20000 --icc 0.5 --q4a-m 4
```

| Figure | Stated | Reproduced |
|---|---|---|
| Good compound, ICC 0.3 / 0.5 / 0.5 with m = 4 | 0.821 / 0.815 / 0.802 | 0.821 / 0.815 / 0.802 |
| No-effect (Q3 null) | ≤ 0.004 / ≤ 0.008 | 0.0040 / 0.0065 (m = 4: 0.0076) |
| Q4 limits 0.02→0.06 / 0.05→0.15 / 0.25→0.37 | 0.73 / 0.44 / 0.76 | 0.735 / 0.438–0.440 / 0.757–0.766 |
| Q4, base 0.33, +12 pp | about 0.80 | 0.796 / 0.818 (my run; δ = 14) |
| Q4a δ at m = 1/2/4; 0.10 → 0.25 | 7/8/10; 0.62–0.78 | 7/8/10; 0.617–0.777 |
| Q4d at 1 / 2 / 5 / 10% | 0.995 / 0.95 / 0.54 / 0.08 | 0.995–0.996 / 0.951–0.953 / 0.536–0.539 / 0.076–0.081 |
| SD-R11 "was" figures (z 2.054, floor 2, p̂ model) | 0.36; Q4d 5% 0.43 | 0.356; 0.419 |
| Verbatim rules together | 0.58–0.63 | 0.576 / 0.628 |
| Q2, Q3, Q5a/Q5b, C(b) | unchanged | unchanged from round 3 |

The p̂ simulation in the script agrees with my independent round-3 `phat.py` construction. With the old margin it gives 0.79 / 0.78, matching N3-G1.

## Could not check

- **D4's final wording.** Margins of 9–45 B on the roles leave little room for anything the S1 independent mapping check (O-3) finds. That decides whether a stakeholder escalation occurs.
- **Live behaviour, S4 estimates and repository acceptance.** Not required at S0. No live runs were made and nothing under `source/` changed.

## Closing check

I checked the one-line fixes against the current bytes, under the same rules as above.

**Check 1: the dist-based span reproduces the 7.1 references.** The new rule (design §5.1:202) measures the lines that generated `dist/skills/<entrypoint>/SKILL.md` adds at `58fd67b` against `22f4bdba`, excluding the `description:` line and the generated `**Governing version.**` line. Measured that way:

| Entrypoint | Bytes |
|---|---|
| D1 and D2 | 9,823 |
| D3 | 9,150 |
| D4 | 8,192 |
| documentation | 5,451 |
| audit | 4,047 |

These equal the stated references, so no figure changes.

**Check 2: the Q5c run mode is coherent.** Contract Q5c (:97) now runs both arms under the frozen deterministic-activation profile of §2, and defines "mode" in the matched-mode report as entrypoint-only versus owner-read.
- **Against governing §0:174.** The 2026-10-04 activation overlay sets deterministic entry for T1/T7/T8, and the Q5c wording matches it.
- **Against the 2026-09-28 decision.** That decision says "6.6 run mode". The later governed overlay replaced its entry mode. Every other operative part is kept: accounting, fresh paired counterbalanced 6.5 runs, the T7 rule, the 512 B margin and stop/escalation. It also keeps the per-mode reporting, now defined as entrypoint-only versus owner-read, which matches the 6.6 T7 bimodality the rule was written for.
- **Against SD-R12.** SD-R12's "same … run mode" reads consistently as this overlaid mode. No conflict remains.

| Finding | Verdict | Basis |
|---|---|---|
| D-G1 | REPAIRED | Design §5.1:202 measures on generated `dist/` with both exclusions, and states why. O-4 (:124) and Q5d (:98) cite the dist span. Check 1 reproduces the references. |
| D-G2 | REPAIRED | The governing-version line is the second sanctioned exception in design §8:274, §4.3 Q5(d):131, contract Q5d:98 and O-2:122. Residual (cosmetic): the workplan §2 floor summary (:71) still reads "byte-identical in source and `dist/`" without the exceptions. O-2 governs the check. |
| D-m1 | REPAIRED | See check 2. |
| D-m2 | REPAIRED | Overlay :170-172 is in design §3:96 and workplan `amends` (:6). |
| D-m3 | REPAIRED | Design §3:92 gives the row's meaning as owner :300-308: default disclosure; qualify when designated or evidently used; block only on (a)–(c); other indications qualify and go to the human; no blanket withholding. |
| D-m4 | REPAIRED | Design §4.3 and contract :107 flag 0.802 as on the rule within Monte Carlo error. Script docstring :7 says "in quadrature". |

The O-3 test now also asserts that elements 1 and 4 stay visibly numbered (workplan :123; design §8:275).

**Overall S0 verdict: PASS.** No SERIOUS CHALLENGE, blocker or open gap remains across rounds 1–3 and the delta. The one residual (workplan :71 wording) is cosmetic and is superseded by O-2. Still open are the stage-bound checks named above: the S1 independent mapping check (O-3) against role margins of 9–45 B; the live relay at S2; the S4 estimates, including P(Q5c pass); and repository acceptance at S1/S3.
