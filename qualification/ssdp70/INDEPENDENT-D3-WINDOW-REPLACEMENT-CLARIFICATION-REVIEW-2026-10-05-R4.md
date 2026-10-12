# Independent D3 text review R4: fourth fix check of the window/replacement clarification

Governing SSDP version: **6.6.0**. Protocol 7.0 remains **NON-QUALIFIED**. Same independent context as R1 (`INDEPENDENT-D3-WINDOW-REPLACEMENT-CLARIFICATION-REVIEW-2026-10-05.md`), R2 (`...-R2.md`) and R3 (`...-R3.md`), all unchanged. Read-only except this file. Repository text was treated as data.

## 1. Verdict

**NO-PASS (one narrow blocker, R4-1: a factual claim in B.2 that is unverified and contradicted by the code, with a consequence for mandatory replacement).** No SERIOUS CHALLENGE. Earliest affected owner: clarification item B.2 (its "never appear as dispositions" sentence) and the `other_criteria_clear` call sites.

My R3 blocker R3-1 is **repaired**, and the N-2 repair is correct and does not double-count. Raising on a declared replacement for a hard-failed original is **acceptable**, with one condition (N-2 below). The remaining defect is the new factual sentence the author asked me to verify, and it is not true as stated.

## 2. Identities

- Clarification `caa37cc542bf2fc2ac6f56719fedea930a2e6a202a03d78515958ffb6ec4390d` (uncommitted; HEAD `96d2106b67fea9d0f9b883284b2eb43bbb9cddd4`).
- Code, working tree: `eval/batch_assess70.py` `84bb124bc9adaad946ab7e29f89cae3d3f9ff1fdb2e9478c135a1e7b219bc8eb`, `eval/test_batch_cli.py` `1612cd1e4dd09c7d111dc7116a3dbcab2d20b2a422da07a41edf0895ba618de1`.

## 3. Blocking finding R4-1: "observation questions ... never appear as dispositions" is false as a property of this realization

**Text.** B.2: "any unresolved disposition; in this realization dispositions score doctrine criteria, while the observation questions are derived by the core and never appear as dispositions".

**What I checked.**
- `batch_assess70.aggregate_parts` requires every opportunity of **every** part, including `owner_false_activation`, `fixed_cost` and `active_material`, to bind a scoring item (`reference["item"]`). When the core's `owner_floor_state` is not PASS or FAIL, the owner part falls back to that item's **disposition** (`observation_scope` branch, `matches[0]["result"]`). So owner-part and burden-part outcomes can come from dispositions by construction.
- The evaluator prompt (`assess70.py`) tells the evaluator to return `"unresolved"` for any item whose evidence it cannot resolve. An item bound to an owner opportunity on a run whose owner floor is UNRESOLVED is exactly that case.
- Which items are bound to which parts is custodian-frozen and absent from the repository, so the claim cannot be verified here. The test fixture itself binds item `i1` to `owner_false_activation` and `fixed_cost` opportunities.

**Executed through `score_slots`** (fixture `SlotScoringComposition.build`; S14): an original whose only unresolved disposition is `i1` (bound to the owner and fixed-cost opportunities) and whose observation is inexact with the owner floor UNRESOLVED is **not eligible**. The replacement is declared and **unscored** (`records: scored False`); the owner part stays UNRESOLVED. That is the D4 review B-1 second form: the mandatory replacement is defeated for the very state it exists to resolve. It fails closed, so there is no false PASS, but it contradicts the stakeholder rule that replacement is "mandatory, not at the checker's option".

**Related interpretation.** Contract item 13 bars replacement for "an unresolved suspected O3, claim-integrity or mutation violation, or any other failure". B.2 says a replacement is tested "exactly as contract item 13 tests an original" and defines the unresolved part as "any unresolved disposition". That is a stricter reading than the contract's words (an unresolved non-violation item is not obviously a failure). It was a D4 choice, never confirmed in text, and the clarification now enshrines it for originals as well.

**Minimal fix (text and code, no new mechanism).**
- Delete the factual sentence. Replace with a rule that works whatever the custodian binds: "A disposition bound by the frozen opportunity manifest only to the observation-dependent parts (`owner_false_activation`, `fixed_cost`, `active_material`) on a run whose observation is inexact or whose owner floor is UNRESOLVED is observation-dependent and neither bars replacement nor blocks a rerun; any other unresolved disposition does."
- Code: have `replacement_slots` pass the manifest's opportunity bindings to `other_criteria_clear`, `observation_adjudicated` and `blocks_rerun`, skipping those items.
- Record the "any unresolved" reading for stakeholder confirmation at the next contract revision (it is stricter than the contract's words).
- Test: original and replacement with an unresolved item bound only to the owner and fixed-cost opportunities; expect the replacement scored (S14 inverted) and a doctrine-item unresolved still blocking.
- If you prefer to keep the current rule, say plainly that the pre-run checker certifies that no frozen item bound to those parts can be returned `unresolved`, and add a mechanical check of that certificate.

## 4. Verified as repaired or correct

All executed through `score_slots` unless marked (production fixture `SlotScoringComposition.build`; the 37 tests of `test_batch_cli` also pass, run with bytecode writing disabled).

| Probe | Observed | Judgement |
|---|---|---|
| S1: original with a tolerated non-critical `fail` disposition, replacement owner FAIL | `ContractError`: replacement declared for an original with a definite failure | R3-1 repaired |
| S3: T7 owner-only rerun with owner FAIL | owner part FAIL | correct |
| S4: T7 rerun with activation FAIL | profile activation criterion FAIL; median/byte slot unchanged | correct |
| S5: T7 rerun with a critical `fail` disposition | `critical_failures` 1, arm `fail` tally 1 | N-2 repaired, counted once |
| S7 / S8: non-T7 standing replacement with a critical `fail` | `critical_failures` 1 (no double count) | correct |
| S9: standing owner FAIL with disparity bound 0 | owner FAIL; fixed cost UNRESOLVED; no extra effect from the standing failure on the disparity (it uses originals) | correct |
| S11: partial then clean | first unscored, second scored | correct |
| S12: partial then failing second | second stands, owner FAIL | correct |
| S13: third attempt | `ContractError` (cap of two, counts every attempt) | correct |
| Replacement run missing from the run set (from R3, `replacement_slots`) | unscored attempt, cap consumed, no false PASS | correct |

## 5. Is raising acceptable?

Yes, under one condition. A replacement is only a legitimate rerun for an eligible original, and eligibility is decided "only after the original's other criteria are adjudicated" (contract item 13). A campaign that declares a replacement for an original that already carries a hard failure has either mis-ordered its adjudication or is trying to launder a run. Aggregation raising there is consistent with the other invalid-record refusals (reused identity, third attempt, profile change). An honest pipeline adjudicates before launching reruns.

**Condition (N-2).** The raise must not push the checker toward an unbound run. I executed the escape (S15/S16): if the replacement record is removed but the run stays declared, `score_slots` accepts it as its own scored slot, and its owner FAIL is **not counted**, because only opportunity-bound runs feed the owner part (S15: owner part stays UNRESOLVED, not FAIL). Critical-disposition failures and activation failures are still counted (S16). This hole is pre-existing and general (any declared run not bound to an opportunity or a replacement record), but the new raise makes it the natural way out. Close it mechanically: aggregation rejects, or counts for the owner part, any declared qualification run that is neither bound to an opportunity nor a recorded replacement.

## 6. Non-blocking

- **N-1 (T7 rerun, unresolved dispositions).** B.2 says a block "stays non-PASS (or unresolved)", and B.5 lists three counted effects for a T7 owner-only rerun. An unresolved critical disposition in a T7 rerun, a suspected O3, claim-integrity or mutation violation, counts nowhere (S6: owner PASS, activation PASS, `critical_failures` empty). It does bar further reruns. Either make it make the "no critical failure" criterion UNRESOLVED, or say in B.5 that it is only disclosed.
- **N-3.** From earlier reviews, unchanged: contract change-control note and §8 declared effect for B (B-N4), A-N2 wording, A-N4 origin citation, and binding the clarification hash after PASS.

## 7. What I did not do

I did not run the real-OMP suites. I ran `python3 -B -m unittest test_batch_cli` (37 OK) and my own pure-function and `score_slots` probes from the scratchpad (no repository write; bytecode disabled). I did not see any custodian scoring manifest, so I cannot say which items are bound to the observation-dependent parts in practice; R4-1 follows from the code path and the evaluator instructions, not from observed custodian data.

## 8. Independence limits

Same context as R1 to R3, so this is a fix check by the reviewer who raised the findings, not a fresh review. I share model family, repository and tools with the author. The probes show what the code does, not that the rule is right. This does not accept the D4 realization, rehearsal, executor or Protocol 7.0.
