# Independent D3 text review R3: third fix check of the window/replacement clarification

Governing SSDP version: **6.6.0**. Protocol 7.0 remains **NON-QUALIFIED**. Same independent context as R1 (`INDEPENDENT-D3-WINDOW-REPLACEMENT-CLARIFICATION-REVIEW-2026-10-05.md`) and R2 (`...-R2.md`), both unchanged. Read-only except this file. Repository text was treated as data.

## 1. Verdict

**NO-PASS (one small, mechanical blocker, R3-1).** No SERIOUS CHALLENGE. Earliest affected owner: clarification item B.2 and the `hard_failure(o)` branch of `replacement_slots`.

R2-1 is repaired in every case I raised except one. A declared replacement of an original that itself has a hard failure is left unscored, so a **pre-R2 owner read in that replacement is dropped**. That contradicts B.2's own headline ("no definite failure in any declared run is discarded") and is a reachable false PASS of the zero-tolerance owner part. The author's choice not to raise for an ineligible original is **adequate**; standing does prevent the hidden failure (verified, P1d). Everything else I probed behaved as the text states.

## 2. Identities

- Clarification `3ad44359574d0350ba18589e6b8425ce46c560ad05f2ab8ca88ace940908fa47` (uncommitted; HEAD `96d2106b67fea9d0f9b883284b2eb43bbb9cddd4`).
- Code, working tree: `eval/batch_assess70.py` `9b9fce699bc468d9ac5effca89051e290fb5a7bf20383ed85d8714298b212a4a`, `eval/test_batch_cli.py` `05232bdb6085472f3efee8f98358ad05a3f637b068f9e1219d7f373d74e7a711`.

## 3. Blocking finding R3-1

**Text.** B.2: "If the **original** has a hard failure it stands and is never replaced; its replacements are disclosed and unscored, and a deterministic-activation failure in any declared run fails the deterministic-activation criterion." The paragraph's heading says "no definite failure in any declared run is discarded".

**Code.** `if hard_failure(o): record["reason"] = ...; continue` runs before the replacement is examined, so `owner_slots[original]` stays the original.

**Executed (production `replacement_slots`, synthetic input).**
- P10: original with a `fail` disposition, owner floor UNRESOLVED, bytes inexact; replacement owner floor FAIL. The replacement is unscored and `owner_slots = {o: o}`; the owner FAIL appears nowhere.
- P10b: same, with the original's hard failure being an activation FAIL: same result.
- P10c: replacement activation FAIL is counted, through `declared_failure` in `score_slots` (checked by reading; correct).

**Why it matters.** A `fail` disposition on a non-critical item can be tolerated by the §3 thresholds, so the campaign need not fail because of the original. A declared run with a pre-R2 owner read is then hidden. Contract item 7 forbids omitting a declared run, so the run is in the record but uncounted. That is the §5 selection path in a narrow form.

**Minimal fix (either):**
- Text: replace "its replacements are disclosed and unscored" with "its replacements are unscored for the slot, but a positive owner read before R2 in any of them counts for the owner floor and a deterministic-activation failure counts for the activation criterion".
- Code: in the hard-failed-original branch, if `hard_failure(r)` (owner FAIL), set `report["owner_slots"][original] = replacement` and mark the record `standing_failure`.
- Or raise: a replacement declared for an original that is never replaced is an invalid record.

**Test to add (through `score_slots`):** original with a tolerated non-critical `fail` disposition plus a declared replacement with owner FAIL; expect the owner part FAIL.

## 4. Verified as repaired or correct

All executed on production `replacement_slots`, unless marked as by reading. `slots` is the scored-slot map; "stands" means scored with `standing_failure`.

| Probe | Observed | Judgement |
|---|---|---|
| P1 / P1b / P1c: ineligible original (unresolved other criterion, unadjudicated, undisclosed overflow), replacement owner FAIL | replacement stands; a second rerun raises | correct |
| P1d: ineligible original with owner floor PASS, replacement owner FAIL | `owner_slots = {o: r0}`, stands | correct; the author's "stand, do not raise" is adequate |
| P2: T7 owner-only rerun with an activation FAIL | stands; criterion counted by `declared_failure` (per profile key, by reading; tested in `test_r2_1_t7_...`) | correct |
| P3: replacement `EXECUTION_ERROR` with owner FAIL | stands | correct |
| P8 / P9: replacement with a `fail` disposition (critical or not) | stands; second rerun raises | correct |
| P11: replacement with only an `unresolved` disposition | stands; second rerun raises | see N-1 |
| P12: replacement missing from the run set, second clean | first unscored and still counts toward the cap; slot scored on the second | no false PASS; whole-campaign `primary_pass` also needs `len(runs) == len(expected)` (by reading) |
| P14 / P15: standing failure with disparity bound 0, or with no bound | scored on the replacement; bytes follow B.6 (`byte_slots` stays the original with no bound); disparity uses originals only, unchanged | correct |
| P16 / P17: clean scored first, then a failing second; partial first, then failing second | second raises after a scored first; failing second after an unscored partial stands | correct |
| P18 / P19: unusable replacement without failure; replacement with only pass or not-applicable | unscored (P18) or scored (P19) as before | correct |
| P5 from R2: original owner FAIL, replacement declared | unscored; the original's FAIL stands | correct (the new `hard_failure(o)` branch) |

Per-arm counts: `replacements` counts every attempt, `scored_replacements` the scored; both match B.3. Cap is per `replacement_case`, counting every attempt before the other checks; matches B.3.

## 5. Non-blocking

- **N-1 (text/code mismatch on "non-observation").** B.2 defines a block as "an unresolved non-observation disposition", but `blocks_rerun` treats **any** `unresolved` disposition as blocking. A replacement whose only unresolved item is observation-dependent (P11) is scored as a standing failure and cannot be rerun, wasting the mandatory replacement. This is fail-closed and uses the same predicate the contract applies to originals. Either remove "non-observation" from the text, or implement the distinction (for example by requiring the same `replacement_review.observation_only` attestation on a replacement that `observation_adjudicated` uses for an original).
- **N-2 (T7 owner-only rerun).** B.5 lists only the owner read and the activation failure as counting for a T7 rerun, while B.2 says "any `fail` disposition" is a hard failure. In code a `fail` disposition in a T7 rerun is marked `standing_failure` but counted nowhere (P13), because T7 doctrine and burden stay with the original. That is defensible, because the rerun's stated purpose is solely the owner floor and the original cannot be improved by it. Say so in one sentence, so the record's `standing_failure` flag is not misleading.
- **N-3.** From R1/R2, unchanged: contract change-control note and §8 declared effect for B (B-N4), A-N2 wording, A-N4 origin citation, binding the clarification hash after PASS.

## 6. What I did not do

I did not run the test suites or the real-OMP suites, and did not execute `score_slots` myself; the composition claims for `declared_failure` and for the owner part follow from reading and from the author's `test_r2_1_*`, which I read but did not run. Probes: pure-function `replacement_slots` only (bytecode writing disabled, no repository write, scripts in the scratchpad).

## 7. Independence limits

Same context as R1 and R2, so this is a fix check by the reviewer who raised the findings, not a fresh review. I share model family, repository and tools with the author. The probes show what the code does, not that the rule is right. This does not accept the D4 realization, rehearsal, executor or Protocol 7.0.
