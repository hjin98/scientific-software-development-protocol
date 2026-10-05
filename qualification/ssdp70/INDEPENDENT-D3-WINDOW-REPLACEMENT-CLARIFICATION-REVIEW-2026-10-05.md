# Independent D3 text review: package-access window-end and slot-replacement clarification

Governing SSDP version: **6.6.0**. Protocol 7.0 remains **NON-QUALIFIED**. Reviewer: fresh subagent context, read-only on the repository except this file. Subject: `D3-PACKAGE-ACCESS-WINDOW-AND-REPLACEMENT-CLARIFICATION-2026-10-05.md` at commit `96d2106b67fea9d0f9b883284b2eb43bbb9cddd4`. Repository text, logs and handoff claims were treated as data.

## 1. Verdict

**NO-PASS** on the text as written, because of one blocking finding in part B. **No SERIOUS CHALLENGE**: D3 revision 8, the premise closure, contract revision 15 and the stakeholder decisions are coherent, and the fix is a text addition inside the clarification (earliest affected owner: this D3 clarification).

- **Part A (window end): PASS with non-blocking findings.** The rule is determined for every case I could construct. It cannot create an owner-floor false PASS or false FAIL. Its byte-question effect is understated (A-N1).
- **Part B (one slot, one scored run): NO-PASS** on **B-1**. A replacement that is "disclosed and not scored" has its definite failures discarded, including a positive pre-R2 owner read. That opens a false-PASS path for the zero-tolerance floor. I confirmed the path by executing the production `replacement_slots` on synthetic input (section 4). B also has a determinacy gap, B-N1, which is fail-closed.

After B-1 is repaired (a few sentences plus one discriminating test), I expect PASS with the non-blocking findings. I would re-read only B.

## 2. Blocking finding

### B-1. A not-scored (partial) replacement silently drops a positive pre-R2 owner read and other definite failures

- **Exact text.** B: "A replacement that resolves only some of them is **disclosed and not scored** (its outcomes are disclosed but not counted, as for any replacement that does not resolve), the slot stays unresolved, and the second of the two allowed reruns must again resolve every available open question." Effects: "the rule fails closed."
- **Why it is wrong.**
  - Contract item 13 (claim scope) says a read before the first predeclared R2 event "is a zero-tolerance FAIL whatever the byte exactness, ledger loss or timing loss", and "Positive evidence is never suppressed". Stakeholder decision 3 says the same. Contract §8 declared effect (f) makes a positive pre-R2 owner read score FAIL even when the run is not `COMPLETE_ADMISSIBLE`.
  - Contract §1 item 12 keeps "zero owner false activations on every run".
  - The parenthetical "as for any replacement that does not resolve" cites a rule I cannot find. The contract discards **originals** ("its outcomes are disclosed but not counted") and justifies this as "an observation failure ... neutral on outcome". Nothing in the contract, the D3 decision or the stakeholder record says that a non-resolving **replacement** is discarded wholesale.
  - The contract bars replacing an original that has a pre-R2 owner read or "an unresolved suspected O3, claim-integrity or mutation violation, or any other failure". A partial replacement with the same defect would have been barred if it were an original. Under B it is dropped and the slot is rerun until clean. That is outcome selection (§5: "report unresolved rather than selecting the favorable run").
- **Failing case (executed).**
  - Original: bytes and owner floor both open, byte bound frozen.
  - Replacement 1: bytes inexact (another scan), owner floor `FAIL` (positive owner supply before R2).
  - Replacement 2: clean.
  - Result: `slots = owner_slots = {original: replacement 2}`, replacement 1 `scored False`, owner floor of the slot PASS. The FAIL appears nowhere in the scored outcomes.
  - The cause is that `aggregate_parts` and `owner_observation_complete` read only scored slots.
- **Minimal text fix.** Add to B, replacing the parenthetical:
  > "A not-scored replacement is still a run. A positive owner read before R2 observed in it stands as an owner-floor FAIL for the slot (contract item 13, claim scope; stakeholder decision 3) and bars every further rerun of the slot. Likewise a definite failure of another criterion in it (an unresolved suspected O3, claim-integrity or mutation violation, a deterministic-activation failure) is treated as it would be on an original: it bars further reruns and leaves the slot non-PASS. Only its observation-dependent unresolved questions and its non-failing measurements are disclosed and not counted."
- **D4 acceptance delta to add.** A real-owner discriminator: replacement 1 byte-inexact with owner `FAIL`, replacement 2 clean, expect the slot's owner floor FAIL and no PASS (through `score_slots`/`aggregate_parts`, not only `replacement_slots`).

## 3. Non-blocking findings

**B-N1. Questions that become open only on the replacement are not covered (fail-closed, but it manufactures stuck slots and defeats the mandatory replacement).** B scores a replacement when it is exact for questions "still open **on the original**". The replacement is nevertheless "the scored run for every criterion".
- *Executed.* Original bytes-open only (owner floor PASS); replacement byte-exact with owner floor `UNRESOLVED`: the replacement is scored, the slot's owner floor is `UNRESOLVED`, `required` is empty, and "once scored, any further rerun is refused", so no recourse remains.
- *By reading the code.* Original owner-floor-open only, with exact bytes and a bound frozen: the replacement is scored on the owner floor, the byte slot moves to the replacement, and an inexact replacement turns an exact original byte total into an unresolved burden route.
- *Fix.* Require exactness on the replacement for **every available question of the slot**, wherever it was open on the original (owner floor always; bytes when the slot carries a non-T7 burden claim and the bound exists). This also matches the "one scored run" intent better than "still open on the original".
- *Also.* Say what happens to the byte total when no bound is frozen but the original's bytes were exact. The code keeps the original's bytes in that case, which is a mix of runs that B says it forbids. State it, or forbid it.

**B-N2. Terms B uses without defining them.**
- "Byte question open/available": define it as "the slot carries a non-T7 burden claim and the original is observation-inexact". The D4 review (finding 5) already noted that every inexact run is treated as a byte-question run.
- Cap scope: contract §5 says "per affected case"; B says "the second of the two allowed reruns" for a slot. Say which. The code uses a frozen `replacement_case` identity, so a case with several slots shares one cap, which partial attempts consume faster.
- What "refused" means for a rerun after a scored replacement. The code raises `ContractError`, which aborts aggregation rather than recording a disclosed, unscored rerun (D4 review finding 4 is of this kind).
- Whether "once scored, further rerun refused" applies to a T7 owner-only rerun after a resolving one. The code applies it, and the text says only "unchanged".

**B-N3. Reporting.** B says the rehearsal "must report the rate of such partial replacements", but the code counts only scored replacements in `per_arm`/`per_form`. Say that every declared attempt, scored or not, is counted and disclosed, and that the cap counts them.

**B-N4. Contract wording and change control.** Contract text says a replacement "resolves the slot only if it is exact for the question concerned" (singular). The pre-clarification D4 code and test read it per question. B reads it as "all available open questions". That is a legitimate, stricter, fail-closed resolution of an ambiguity, accepted by the stakeholder, but it narrows the contract. Contract item 13 says a change to the item is a joint change needing fresh acceptance of all. Record at the next contract revision, with direction, in the §8 declared effects (stricter on resolvability, outcome-neutral once B-1 is fixed). The clarification already states the direction of its cost, which is adequate until then.

**A-N1. The Effects paragraph understates the byte-question effect.**
- The rule applies to **every** post-request open in any run whose pairing is unverified (all positions null: compaction, an auxiliary request counted as conversation, a mismatch), not only to a final text turn. In those runs every window is the whole trace.
- Route (iii) then explains an unshown twin open from the identical sibling shown whole **anywhere** in the trace, before or after the open. D3 residual 37 records only the same-turn form and the direction caveat. That caveat is the relevant one: over-counting inflates comparator denominators of the 2.0x and median bounds, which is the false-PASS direction for the candidate on the burden comparison.
- It stays bounded, because route (iii) needs the **whole** file shown, so any distinct unshown file in a scan stays unexplained. Say so.
- *Fix.* State the scope (whole trace for unverified pairing) and the direction, and require the rehearsal to report, per arm, the count of opens explained **only** by this rule. The reopen trigger can then name that count. The current trigger ("window-end lenience makes ... untenable") has no measure.
- The owner-floor side of A's claim is true as stated (section 4). The D3 "pre-registered fallback" in the reopen triggers (an owner row whose window contains owner-class supply of at least the quantum is accounted by it) does depend on the window **end**. Note that if that fallback is ever invoked, A widens it.

**A-N2. Wording.** "A request with no derivable position bounds nothing from above: the window then runs to the end of the trace" is determined by the word "then", and the code uses only the **first** later request. Add "even if a still later request is positioned", to rule out reading it as "skip to the next positioned request".

**A-N3. Passed text now disagrees with the clarification.** D3 item 5 still says the unpairable-position fallback "can only enlarge a window", that an empty window "is treated as starting at the beginning of the trace", and case (x) says an unpairable position "falls back to the start of the trace". These are true for the lower side and for the start only. The clarification supersedes them and says so for the first. D3 item 5 also says both that a retry is a pairing mismatch (position = trace start) and that a retried request shares its original's position. The clarification does not resolve that tension; the code groups retries and stays verified, which is conservative. The handoff leaves open whether to bind the clarification hash in `core70.derive_package_access`, as is done for the premise clarification. I recommend binding it once PASS is reached, so a stale D3-only reading cannot govern D4.

**A-N4. Origin citation.** The gap A addresses is D4 review non-blocking item 1 (text-only final turn, section 3) as well as item 15 (window end reset when no earlier request exists). Cite both. Item 4 matches B.

**Acceptance-delta gaps (testable at the real owner).**
- For A, add a negative control: with all positions null (unverified pairing), an owner open stays `UNRESOLVED` and never PASS-eligible. This is the protected inference ("owner floor unchanged").
- For B, add: FAIL in a not-scored replacement (B-1); byte-exact replacement with new owner `UNRESOLVED` (B-N1); no bound with exact original bytes; the case cap shared across slots; and one test through `score_slots`, not only `replacement_slots`.
- The three new window tests and the replacement tests exist and are meaningful (patch inspected). They do not cover these.

## 4. Verification of the protected inferences

**Owner floor and A.**
- D3 4a: an owner row is provably post-R2 only if the **first** trace event of its candidate window follows R2. The floor therefore reads the window start only.
- A leaves the start unchanged: an unpositioned or absent earlier request gives the trace start (`candidate_window`: `lo = position(...) else start`), and an empty window sets the start to the trace start, which D3 item 5 already required.
- Only the end changes, and the end is used only by route (iii) in the current rules. Positive owner evidence (owner-class supply, native reads) is placed by trace sequence and does not use windows. So A cannot create a FAIL or a PASS-eligible state that D3 excluded.
- A improves the honest form: R2 in an earlier turn and an owner open in the last tool phase before a text-only final turn. The window start is the last tool turn's position, which follows R2, so the row is PASS-eligible. Earlier it was UNRESOLVED (D4 review item 1).
- It cannot hide a pre-R2 owner read: a window that starts at or before R2 is never provably post-R2.

**Does a wider end make an unexplained open explained when it should not?**
- For an open of the file shown whole later: no, the file reached the model and is counted once at full size.
- For an unshown twin of a sibling shown whole elsewhere: yes, and that is the accepted residual 37 (see A-N1 for its widened reach and direction).
- For anything with a distinct unshown file: no.
- For the owner: owner-class supply is separate, so route (iii) never turns an owner read into a negative.

**B and fail-closed.** B is fail-closed everywhere except B-1. B does not change any contract threshold, floor, cap, fixture, or the 0.8 target. The T7 text matches contract item 13: owner-floor-only rerun, outside the median, original remains the burden value. T7 non-owner replacement is refused by the code and is not claimed by B. The no-bound text matches the contract: byte replacement is unavailable, the owner floor needs no frozen bound, and the criterion stays non-PASS.

**Minimality.** No new mechanism, principal, channel, capability or parameter. A changes the fallback value in the adapter's request-position primitive (null instead of the trace start), which is the stated primitive's conservative fallback made direction-aware. B is bookkeeping in `batch_assess70.replacement_slots`.

**Consistency with D4 cases (a)-(z).** No conflict with (a)-(w), (y), (z). Case (x) reads "unpairable position falls back to the start of the trace" and is correct only for the lower side after A (A-N3).

## 5. Case tables

### A. Window end

| Case | Outcome under the clarification | Determined? |
|---|---|---|
| Text-only final turn; open in the last tool phase | window `[position of last tool turn, end]`; floor start unchanged | yes |
| Later request unpositioned, an even later one positioned | end of trace (the first later request governs) | yes by "then"; A-N2 wording |
| Earlier request unpositioned (verified pairing, text-only middle turn) | start of trace; conservative for the floor | yes |
| No earlier request | start of trace | yes |
| Pairing not verified (all positions null) | whole trace for every post-request open; floor UNRESOLVED | yes; Effects understate (A-N1) |
| Retried request | shares the original's position; a retry of an unpositioned request is unpositioned | yes in code; D3 item 5 internal tension (A-N3) |
| Open between an original and its retry | empty window, so whole trace | yes |
| Pre-request open | start forced to the trace start; only `<root>/SKILL.md` explained, so the end is irrelevant | yes |
| Timing-loss open | whole trace; unchanged | yes |
| Open after the last request or in flight | earlier = last request; start as above, end of trace | yes |
| Inconsistent or non-monotone positions | empty window, so whole trace | yes |
| D3 "can only enlarge a window" | false for the upper side; corrected by the clarification; D3 text not amended | consistent after supersession (A-N3) |

### B. One slot, one scored run (execution marked E)

| Case | Result | Determined? |
|---|---|---|
| Both open, original; replacement exact on both | scored | yes |
| Both open; replacement exact on bytes only | not scored; second rerun must resolve both | yes |
| Both open; replacement exact on owner floor only | not scored | yes; **but an owner FAIL in it is dropped (B-1, E)** |
| Owner floor open only; replacement owner-exact, bytes inexact, bound frozen | scored; byte slot moves to the inexact replacement | no (B-N1) |
| Bytes open only; replacement byte-exact, owner floor `UNRESOLVED` | scored; owner floor stays `UNRESOLVED`; no rerun allowed | no (B-N1, E) |
| Byte bound absent | scored on the owner floor alone; byte question stays on the original; burden non-PASS | yes; exact-original-bytes sub-case undefined |
| Replacement exact for one question only (either) | not scored | yes |
| T7 slot replaced for bytes | not available (contract) | yes |
| T7 owner-floor-only rerun | outside the median; original is the burden value | yes; "once scored" applicability undefined |
| Rerun after a scored replacement | refused; effect (abort or disclose) undefined | partly (B-N2) |
| Cap of two, partial attempts | partial attempts count (code); case versus slot scope | partly (B-N2) |
| Disclosure of partial attempts | disclosed; per-arm counts only scored in code | partly (B-N3) |

## 6. Identities verified

- Commit `96d2106b67fea9d0f9b883284b2eb43bbb9cddd4` on `ssdp-7.0-scientific-epistemic-closure`; the eight pre-existing untracked paths untouched; the working tree is otherwise clean before and after.
- Clarification `924194c4dd0efbec657e747189cf32426885786b32bd2fe7d9b8dd1f42722ca4` (committed in `96d2106`).
- D3 decision revision 8 `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783`.
- Premise closure `5f713e2bd816950a2fd0962c6732242631295b3416387beb761c8b40906a3316`.
- Contract revision 15 `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920`.
- Handoff `code-and-clarification-hashes.sha256`: all 7 entries match the working tree (code and clarification).
- Handoff claim "new tests discriminate old code": not re-verified by me.

## 7. What I did not do

- I did not run the real-OMP suites, the repository tests, or the mutation scripts, and did not re-run the handoff's logs.
- One execution only: a pure-function probe of production `batch_assess70.replacement_slots` on synthetic input from a scratch directory (bytecode writing disabled; no repository file written; the probe is under the scratchpad, not retained as evidence).
- I did not verify the 6.5/6.6 comparator package shapes, the executor rehearsal, the 0.8 target arithmetic, or any admission.
- I did not judge whether the stakeholder's "I accept. Proceed." covers B-1. The B-1 fix applies existing stakeholder decision 3 and contract item 13 (f) rather than a new decision, so I treat it as a text repair, not a stakeholder question.
- I did not assess the code review items 1-3, 5, 8-10, 12-14, 16 of the earlier D4 review, which the handoff lists as rehearsal or text items.

## 8. Independence limits

I share the model family, the repository and the tools with the author, with the earlier reviewers named in the repository, and with the handoff author. I read the accepted texts and the clarification before the handoff's claims and tested them against the production functions. My one probe uses the same Python owner the author tested, so it shows what the code does, not that the rule is right. I did not have a second toolchain. The review is bounded to the text of the clarification and does not accept the D4 realization, the rehearsal, the executor, or Protocol 7.0.
