---
kind: independent-pre-run-contract-check
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: A
result: PASS
---

# Independent Stage A qualification-contract recheck — PASS (framework only)

**Independence and custody.** This checker authored neither the Protocol 7 candidate, the contract, the Stage A draft nor any fixture. It did not read, search for or author any concrete Protocol 7 fixture, planted key, expected answer or human-trial answer, and opened no custody location. Accepted 6.6 identity was resolved from `PROTOCOL-RELEASE-STATE.yaml` (`accepted_current.public_source_ref 22f4bdba…`, `source/PROTOCOL_VERSION` = 6.6.0 via `git show`). The 6.6 selection rule was confirmed at `qualification/ssdp66/eval/scenarios.yaml`. The only file this check wrote is this record. It applies only to the exact subjects below.

| Subject | SHA-256 verified |
| --- | --- |
| Consolidated workplan (governs; §8.3, §11, §12 Stage A) | `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` |
| Stakeholder decision 2026-09-28, backstop relaxation | `b1ae718c37e17c085146eac085f69e3fc7b6ae5825003fe2c0be746d86cc85e2` (the same bytes the 66F2943 Review PASS records) |
| Stage A basis and preservation map | `8ae7a966b2f8f84fd4e999efbd7b06255b692242f343afa8f852db7f5254b333` |
| Revised qualification contract (uncommitted working-tree revision) | `02dd12dbf2468c5134119146bd04b8ae9d46551a505e498aa0e2b885030ce077` |
| Release state | `be05bc06dce9b0f4f75a28ed23aa6bf0cb553fb5532a0e89fc56cb47e5d46085` |
| Prior check (NO-PASS on contract `7fc325b5…`) | `86944fae0b44736ab5542e4422e2a518437f077ab19ac80b9dad9b9afa179619` |

## Serious Challenge

None. No conflict was found between the contract, the workplan, the 2026-09-28 stakeholder decision (2.0 × fresh paired accepted-6.5 median on each T1/T7/T8, 512 B static margin retained) and accepted 6.6.

## Prior material gaps: disposition

1. **Pooled owner-load floor — CLOSED.** Contract §4 now scores owner-load hits per R2 trigger class. The classes are (a) realized-result judgment, (b) D1/D2/D3 authority authoring or acceptance review, with ≥2 authoring/revision and ≥2 acceptance-review opportunities, and (c) gate evidence. Class assignment is predeclared, with no double counting. Each class needs ≥6 distinct opportunities and ≥⌈0.8n⌉ hits. A replicated opportunity counts as a hit only on a strict majority of its replicates. If any class is under-exposed, the whole placement claim fails. A class below its hit floor is a §8.3 placement miss even when the aggregate passes. §2 adds the per-class exposure minimum. Recomputed binomial check at n=6, k≥5: P(pass) is 0.0046 at p=0.25, 0.109 at p=0.5 and 0.886 at p=0.9. These match the contract's stated ≈0.005, ≈0.11 and ≈0.89. The earlier counterexample (8 class-(a) hits and 0 hits elsewhere) now fails.
2. **Ambiguous unnamed denominator — CLOSED.** §3 adds a separate row. The floor is ≥⌈0.8n⌉ of n≥6 eligible unnamed-class properties, critical and non-critical alike. It is counted independently of both the non-critical 16/20 row and the zero-error critical rule. Detection requires surfacing the property's mechanism and affected area. A correct limitation, blocker or withheld conclusion explicitly does not count as detection. The chained anomaly stays excluded, and §2 adds the ≥6 exposure minimum. This matches workplan §11.5 "Out-of-list consequence". At n=6, P(pass) at a true detection rate of 0.5 is 0.109.
3. **Human exposure not per arm — CLOSED.** §7 now requires ≥4 independent participants, each reviewing exactly one fixture per arm (different fixtures). This gives ≥4 participants per arm, a 2/2 counterbalanced order and ≥2 distinct fixtures per arm. Each participant answers ≥5 routine and ≥1 critical question per arm, so each arm has ≥20 routine and ≥4 critical opportunities. The floors are ≥16/20 routine per arm and zero materially wrong critical answers in either arm. A participant who does not complete both arms is dropped from both arms' counts. If exclusions push exposure below the minimum, the result is non-discriminating, never a pass. The workplan §11.6 controls are retained.

## New material gaps

None. A whole-framework re-read against §11.2–§11.6, §8.3 and §12 Stage A found every §11.4 measure with a unit, exposure and floor or bound. The zero-budget O3, critical-claim-integrity and unauthorized-mutation rules each have ≥6 opportunities. The critical oracle carries the specific-limitation and cheap-first-look rules. The 6.6 preservation floors match `qualification/ssdp66/eval/scenarios.yaml`: selection correct ≥ 6.6 − 2 over 32 runs; negative-scenario false activations ≤ 6.6 + 1; route probes ±2 over 38 runs. T4–T6 margins are ±1 over 8 episodes. The fixed-cost backstop reflects the stakeholder decision, with the 6.6 run mode, accounting, fresh paired 6.5 denominator, symmetric T7 replication rule, 512 B static margin and 1,000 B target with lossless attribution. The repairs introduced no contradiction.

## Minor findings (non-blocking; wording or reporting)

- **Joint pass rate across classes.** §4's discrimination statement is per class. With three classes jointly, a true 0.9 per-opportunity hit rate passes only ≈0.69 of the time (≈0.28 at 0.8), so there is a material chance of a false placement-miss reopen. Report the joint rate. More opportunities or majority-of-replicates scoring would reduce it. This is a power cost, not a lax floor.
- **Redundant aggregate.** The aggregate ⌈0.8N⌉ owner-load bound is implied by the per-class floors. It is harmless.
- **T7 "still mixed" is always true.** Once the first three T7 runs are mixed, they remain mixed at five, so the rule is effectively 3 or 7 pairs. It is still outcome-independent.
- **Discrimination statements missing.** Workplan §11.5 asks for an explicit discrimination statement for the near-boundary selection-false-activation margin (≥8 episodes, +1) and the selection non-inferiority bound (32, −2). The contract gives counts and rationale but no statement of what each can discriminate.
- **Two workplan clauses carried only by reference.** The contract relies on "the handoff governs" for (i) the escalation semantics of a Stage E/live backstop breach (stakeholder escalation before any live run or the Stage F freeze, not an acceptance failure) and (ii) the §11.5 structural-check list. A one-line restatement or route would help.
- **No route to the Stage A draft records.** §8.3 says the exact D4 draft text and bytes are recorded "in the qualification contract". They live in `STAGE-A-D4-ENTRYPOINT-COMPRESSED-DRAFT.md` and `STAGE-A-STATIC-PREMEASUREMENT.md`, which the contract does not route to. `STAGE-A-STATIC-PREMEASUREMENT.md` still states the superseded 1.10 rule as historical declaration text.
- **Delegate case list incomplete.** The §2 list of delegate cases supplying the ≥12 request parts omits the result-contingent case; the 100% floor still covers all owed parts. The label "review" is also ambiguous.
- **Two further workplan statements not restated.** "Eligible" unnamed property should cite the §2 resolved-membership rule. The 6.6-near-zero non-inferiority caveat and the "suspected violation stays unresolved until independently assessed" rule are not restated.

## Required pre-run checks still pending (not passed)

- Designation of a separate fixture custodian.
- Checks that need the withheld fixture material (not yet available):
  - classification rationale, including disguised listed mechanisms;
  - per-arm opportunity exposure for every §2 minimum;
  - per-class R2 opportunity counts and class assignments, including the (b) authoring/review split and non-duplicate variants;
  - unnamed eligibility and count;
  - critical answer keys and acceptable dispositions;
  - oracle branches and predeclared R2 events;
  - route classes against the withheld context;
  - the human-trial plan: participants, fixture rotation, frozen questions, time bounds and permitted assistance.
- Checks that need the actual harness (not yet run): every oracle/rubric collected and executed; per-branch known-broken rejection; known-good acceptance including legitimate withholding and designed termination; complete report/file/trace capture; sandboxed side-effect capture with detection of an unauthorized write; composite ordinary-entry capture per case class; the chained-delegate cheap-first-look probe.
- Stage E remeasurement of the generated D4 entrypoint and the owners T7 reads, and fresh paired 6.5 baselines, before any live run.

## Disposition

**PASS for the Stage A qualification-contract framework** at contract SHA-256 `02dd12db…`. All three prior gaps are closed and no new material gap was found. This does not freeze fixture instances, and it passes none of the pending withheld-instance or actual-harness checks above. Each must run and pass before any candidate evaluation run. Any later edit to the contract requires a new applicability check.
