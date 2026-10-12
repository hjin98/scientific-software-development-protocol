# Independent D3 text review R2: fix check of the window/replacement clarification

Governing SSDP version: **6.6.0**. Protocol 7.0 remains **NON-QUALIFIED**. Same independent context as `INDEPENDENT-D3-WINDOW-REPLACEMENT-CLARIFICATION-REVIEW-2026-10-05.md` (R1, unchanged, sha256 `724068598c7172553a8e9b6acf2ee839c5ff792158077147a13c8dc30a2b7a91`). Read-only except this file. Repository text was treated as data.

## 1. Verdict

**NO-PASS (narrow).** No SERIOUS CHALLENGE. Earliest affected owner: the clarification text, item B.2, with its code realization.

- My R1 blocker **B-1 is repaired for its stated form**: an eligible original, and a usable replacement with a positive pre-R2 owner read or a deterministic-activation failure on a non-T7 slot.
- Parts A and B-N1 to B-N3 are adequately repaired.
- **One new blocking finding (R2-1).** B.2 now says "A definite failure observed in it is never discarded", but the code and the enumerated list discard definite failures in several reachable cases. The same outcome-selection path survives for failures other than the two named, and for a replacement of an ineligible original. I confirmed each case by executing production `replacement_slots` on synthetic input (section 3).

The fix is a short text change plus a small predicate change in `replacement_slots`. I would re-read only B.2, item 5 and the matching code/tests.

## 2. Status of my R1 findings

| R1 finding | Status |
|---|---|
| B-1 positive pre-R2 owner read dropped in a not-scored replacement | **Repaired** for eligible originals and non-T7 slots. Executed: standing failure scores the slot on the replacement, further reruns raise, `owner_floor` FAIL counts. Tests `test_b1_*` meaningful. Residual cases under R2-1. |
| B-N1 questions open only on the replacement | **Repaired.** B.1(a): the replacement's own owner floor is always required; bytes when open on the original and available. Code `needed` matches. Test `test_bn1_*`. |
| B-N2 cap scope, "refused", byte-question definition | Repaired in text and code, except one wording point (N-1). Refusal = `ContractError` matches B.4. Byte question defined and matches `non_t7_bytes`. |
| B-N3 attempt vs scored counts | **Repaired**: `replacements` counts every attempt, `scored_replacements` the scored; cap counts every attempt. |
| B-N4 contract wording and §8 effect | Not addressed in text; unchanged non-blocking (record at the next contract revision). |
| A-N1 effects understated | **Repaired**: unverified pairing gives whole-trace windows, twin over-counting on comparator arms stated with direction, rehearsal measurement, reopen condition. |
| A-N2 "even if a still later request is positioned" | Not added; non-blocking. |
| A-N3 superseded wording | Mostly repaired: the "can only enlarge" parenthetical and case (x) are covered. D3 item 5's retry-vs-mismatch tension and "empty window starts at the beginning" remain, harmless. |
| A-N4 origin citation | Unchanged; non-blocking. |

## 3. Blocking finding R2-1: "never discarded" is not true of the realization

**Text.** B.2: "A definite failure observed in it is never discarded: a positive owner read before R2 ... or a deterministic-activation failure in a usable replacement stands for the slot exactly as it would on an original". B item 5 (T7) says only that a positive pre-R2 owner read stands.

**Code.** `standing_failure = original_eligible and replacement_usable and (owner_floor_state == "FAIL" or deterministic activation == "FAIL")`.

**Executed cases** (production `replacement_slots`; `slots` is the scored-slot map that feeds `aggregate_parts` and `score_slots`):

| Case | Observed | Problem |
|---|---|---|
| P1: original **ineligible** (other criterion unresolved), replacement owner FAIL, then clean | both replacements unscored, slot stays on the original | A pre-R2 owner read in a declared run is dropped. |
| P1d: ineligible original with owner floor PASS, bytes inexact; replacement owner FAIL | slot owner floor stays PASS | **False PASS of the zero-tolerance owner part.** Overall the campaign is non-PASS because of the original's other item, but the FAIL is hidden and a FAIL becomes UNRESOLVED/PASS in the owner part. |
| P1b, P1c: unadjudicated original; undisclosed-overflow original | same: replacement FAIL dropped | Same. |
| P2: **T7** owner-only rerun with deterministic-activation FAIL | record says `scored`, `standing_failure True`; `slots[o]` stays the original, so `score_slots` never counts the rerun's activation FAIL | Contract §1 item 12 says an activation failure "fails the deterministic-activation criterion ... rerunning it cannot rescue". The record claims it stands; the scoring ignores it. |
| P3, P1e: replacement `EXECUTION_ERROR` or `MALFORMED_EVIDENCE_OR_ASSESSMENT` carrying owner FAIL, then clean | FAIL dropped, clean rerun scored PASS | "Usable" is undefined in the text. Contract (f) says positive evidence scores FAIL "although the run's evidence state is not `COMPLETE_ADMISSIBLE`". |
| P8, P9: partial replacement (INADMISSIBLE with `original_dispositions` fail, or COMPLETE_ADMISSIBLE with a critical `fail` disposition), then clean | failing dispositions dropped, clean rerun scored | **Rerun-until-clean on doctrine criteria.** Contract §8 (d) justifies discarding an original as "neutral on outcome" only because it "can discard an original's non-failing measurements"; eligibility bars originals with failures. A replacement is given no equivalent protection. |

The repaired items are exactly those named in R1 B-1, but R1 also asked that "a definite failure of another criterion in it" be treated as it would be on an original. The revision narrowed that to two failure kinds, kept the sentence "A definite failure ... never discarded", and made standing conditional on the original's eligibility. Contract §5 says to "report unresolved rather than selecting the favorable run".

**Minimal text fix** (replace the second half of B.2 and align item 5):

> A **definite failure** observed in any declared run of the slot, scored or not, stands for the slot and bars every further rerun. Definite failures are: a positive owner read before R2 (in any evidence state in which the core derives it); a deterministic-activation failure; a `fail` disposition; and an unresolved suspected O3, claim-integrity or mutation violation, tested on the replacement exactly as contract item 13 tests an original. The slot is scored on that run and stays non-PASS. It stands whatever the original's eligibility and for T7 owner-only reruns (where it counts for the owner floor and the deterministic-activation criterion but the run stays outside the median). A replacement declared for an **ineligible** original is an invalid campaign record: aggregation raises.

**Minimal code alignment:** apply `other_criteria_clear` to the replacement's dispositions (and `original_dispositions`); drop the `original_eligible` and `replacement_usable` conditions from `standing_failure` (or raise for an ineligible original); for a T7 owner-only standing failure, count the rerun's activation FAIL in the activation criterion.

**Tests to add (through `score_slots`):** replacement 1 partial with a critical `fail` disposition then clean replacement 2, expect the slot non-PASS and no further rerun; ineligible original with a declared replacement (raise); T7 owner-only rerun with activation FAIL (criterion FAIL); unusable replacement with owner FAIL.

## 4. Other checks of the revision (no further blockers)

- **Eligible original, owner UNRESOLVED, replacement carries a standing failure:** stands, scored on the replacement, owner FAIL counts (executed, P4 with no bound, and `test_b1_*`). Correct.
- **Original with owner FAIL declared a replacement (P5):** barred, stays unscored; the original's FAIL stands. Correct.
- **Byte disparity and counts:** `runs`/`inexact` still come from originals, so a standing failure does not change the disparity bound. `replacements` (attempts) and `scored_replacements` tallies are separate and match B.3. With a standing failure and a frozen bound, the byte slot moves to a replacement whose bytes may be inexact, so the burden route is unresolved (non-PASS). With no bound, bytes stay on the original (executed, P4).
- **Cap:** counted per declared `replacement_case` on every attempt, including partial ones. B.3 says "per affected case (per original run ...)". The code allows one case identity to cover several originals. State "per frozen case identity" (N-1).
- **T7 owner-only:** a positive pre-R2 owner read stands for the owner floor only (executed, P2b); correct per item 5. Activation: see R2-1.
- **A:** the new Effects paragraph is accurate and the owner floor is still unaffected (window start only). Left unchanged since R1, in agreement.
- **No new mechanism, principal, channel, threshold, floor, cap or fixture.** B still changes none.

## 5. Non-blocking

- **N-1.** Define "case" as the frozen `replacement_case` identity and say a case may cover several slots. Define "usable replacement" or delete it once R2-1 is applied.
- **N-2.** No-bound sub-case with exact original bytes: the code keeps the original's exact byte total while the replacement scores the other criteria. Say so, or require the byte total from the scored run.
- **N-3.** From R1 and unchanged: B-N4 (contract change-control note and §8 declared effect for B), A-N2, A-N4, and binding the clarification hash after PASS.

## 6. Identities verified

- Revised clarification `2089210de3251dd90587dcf0fa0bde80c21777a060994a988dcb71b853bf6a60` (uncommitted, modified in the working tree; HEAD `96d2106b67fea9d0f9b883284b2eb43bbb9cddd4`).
- Code read from the working tree diff: `eval/batch_assess70.py` `1c46b21977587f374847dd6bbf2a38b3f8781296b5e0e7935a468308e46094ee`, `eval/test_batch_cli.py` `6337bbb20855654fee9ac95aa066394798fd6a9e60b66e35eea624cbc783d516`.
- Untracked files of the earlier list unchanged.

## 7. What I did not do

Did not run the test suites, the real-OMP suites or the mutation scripts. Executed only a pure-function probe of production `replacement_slots` (bytecode writing disabled; no repository write; probe kept in the scratchpad). I did not execute `score_slots` for the T7 activation case P2; that conclusion follows from reading `score_slots` (activation criteria are computed from scored slots only). Not re-examined: rehearsal, 0.8 arithmetic, premise witness, admission.

## 8. Independence limits

Same context as R1, so this is a fix check by the reviewer who raised the findings, not a fresh review. I share model family, repository and tools with the author. The probes show what the code does; they do not prove that the rule is right. This does not accept the D4 realization, rehearsal, executor or Protocol 7.0.
