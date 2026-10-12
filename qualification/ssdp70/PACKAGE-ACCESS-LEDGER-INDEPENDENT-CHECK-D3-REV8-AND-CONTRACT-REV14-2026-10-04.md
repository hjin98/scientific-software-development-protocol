# Independent check: D3 package-access ledger decision revision 8 and contract revision 14

Governing SSDP version: 6.6.0 (Protocol 7.0 NON-QUALIFIED). Subject: commit 07a4bb0d2093605425374ac3102c6ac04dbe1652, tree addc91b9baf0f8517c78e4bb0ff2dc0257a893f5 (HEAD verified; committed bytes read; working tree has only the eight out-of-scope untracked files and no tracked modification). Nothing in the repository was modified.

## Serious Challenge
None. The mechanism (supervisor ledger, content-based owner-class supply, conservative provably-post-R2 test, replacement, T7 unknown value) can work against the shipped packages.

## (A) Blockers, by earliest owner

### A-1 (contract revision 14, item 13 Replacement and T7 bullets; conflicts with D3 revision 8 item 4a and residuals) - eligibility keyed on "positive owner evidence" makes the most honest owner-load form permanently non-PASS
- D3 4a defines positive evidence as owner content that reached the model, at any result sequence (a post-R2 owner-load hit is positive evidence). D3 4a, the Residuals bullet and probes (m)/(n)/(y) say a pre-R2 scan (for example `grep -rl` opening all seven owner copies) followed by a legitimate post-R2 owner load leaves the floor UNRESOLVED and that it "costs a replacement".
- Item 13 Replacement says an original "without positive owner evidence" is replaced, and the T7 bullet says an owner-floor rerun applies to a run with "no positive owner evidence" and that "a T7 run with positive owner evidence is never replaced". A scan-then-load run has post-R2 positive evidence (the hit) and an UNRESOLVED floor, so by the contract's literal text it is not replaceable and the zero-tolerance floor (and, for non-T7 burden slots with inexact bytes, the burden slot) stays non-PASS with no resolution path. That is a manufactured non-PASS on the honest form the decision was built to protect, and it contradicts D3. The amendment section 5 item 1 and stakeholder record round 4 wording ("positive owner read before R2 never replaced") supports the intended reading for the owner floor.
- Minimal text fix, no mechanism change: in item 13 Replacement and T7 bullets, make owner-floor replacement/rerun ineligible only for a positive owner read before the first R2 event (FAIL); keep "positive owner evidence at any time and inexact bytes => not replaced" only for the non-T7 burden slot if the stakeholder confirms it (see confirmations). Then align the gate-arithmetic sentence.

No other blockers found.

## (B) Non-blocking items (conditions for the D4 stage / text tidy)
1. Stale citations introduced or left by the delta: D3 Parents says "item 13 added in contract revision 13" (item 13 predates it; revision 14 is the current one); amendment section 1 History says "Revision 13 changes definitions, clarifications and declarations only" (should say revision 14 / counting rule and wording) and lists NO-PASS revisions 9 to 12 only (contract section 8 lists 13 too); amendment section 6 question 6 says "four declared effects" (six, (a) to (f)); stakeholder round 3 item 4 says four (superseded in part, marked only for (d)).
2. Declared effect (d) in contract section 8 gives no direction word (the others do). Suggest: neutral on outcome, can discard an original's non-failing measurements.
3. Honest multi-line keyword grep. I measured on dist/skills: owner file `scientific-inspectability-and-initiative.md` has 409 lines, 242 of >=48 bytes, 46 of >=256 bytes, 0 shared with any non-owner file in the 7.0, 6.6 (22f4bdb) or 6.5 (7f7b5e2) packages, and no owner line is a substring of another. A package-wide `grep -rn` for a common word (`authority`, `evidence`, `owner`, `claim`, `scientific`, `D1`) matches 17 to 47 distinct owner lines totalling 3.5 to 11.8 KB, so by the confirmed quantum it is a non-replaceable pre-R2 FAIL when it happens before R2 and output is not truncated below whole lines. This follows the confirmed rule (content reached the model); but item 8's rehearsal list covers only "one line or several lines below the quantum". Add the above-quantum honest keyword grep as a rehearsal form with its FAIL rate reported, and confirm with the stakeholder.
4. Minor exposure leaves the floor UNRESOLVED without saying it must be placed before R2 or on an open not provably post-R2; as worded, a small owner display after a provably post-R2 open also makes UNRESOLVED (conservative, replaceable). Clarify in D4.
5. T7 owner-floor-only rerun has no stated count cap (section 5's two-rerun cap is for non-T7 cases). No selection bias arises (first resolved outcome), but state the cap.
6. Request-position primitive says "first trace event of that turn's tool calls and results", while item 8 says the honest same-response owner load is UNRESOLVED "because the window starts before the R2 text". With the stated primitive the window starts after text in the same response, which is physically correct and conservative only for the parallel-tool-action R2 form. Reconcile the sentence in D4.
7. The `package_access` derivation inputs (item 13) list ledger artifact, normalized events and package but not the observer request records (stamps, bodies) from which supply and request-0 cut are derived; add them to the recomputation inputs. Declare the run evidence state for ledger-loss runs with a positive FAIL (item 7 allows only COMPLETE_ADMISSIBLE into scoring; effect (f) declares only the no-ledger exception).
8. The 256-byte/two-line rule is restated in three workplan places (entry, two markers); D3 owns it; drift risk only.
9. Realtime clock-step residual and request-stamp CLOCK_MONOTONIC stamping should be a "must" D4 condition (a false PASS-eligible path under a host clock step otherwise remains).
10. D4 code (package_ledger.py, harness70.py, core70.py, adapters/omp.py, batch_assess70.py) unchanged since 8be024a realizes revision 3 only: no heartbeats, windows, quantum, minor exposure, split exactness, `package_access` event, replacement or unknown-value bookkeeping. Expected D4 follow-up, not a D3 defect.

## Falsification performed (executed)
- Shipped shapes verified from bytes: 238/63/38/213 (dist/skills), 212/62/37/187 (6.6 ref 22f4bdb), 198/60/35/173 (6.5 ref 7f7b5e2); owner basename has seven byte-identical copies; no hard links.
- Owner premise: 0 of 242 owner lines >=48 bytes occur in any non-owner file of the three packages; 46 of 242 are >=256 bytes (D3 figure confirmed); no distinct owner line is a substring of another, so one long line cannot supply "two distinct lines".
- Same-line-seven-times, `cat -n`/`grep -n` prefixes (substring matching), chunks across results: behave as D3 states (counted once per result; minor exposure below quantum; chunks never accumulate) - by reading the rule against the measured file, not by running code (code does not implement it).
- Owner content before R2 without FAIL or UNRESOLVED: not found; any such content requires an owner open (ledger), which is UNRESOLVED unless provably post-R2, ledger loss, or timing loss, all UNRESOLVED. Positive FAIL cannot be suppressed by exactness loss. PASS-eligible owner floor requires intact ledger, intact timing when an owner open exists, and every owner row provably post-R2. The only PASS-eligible path under inexact observation is the declared clock-step residual (B-9) and the T7 route unknown-value bound (declared, sound: candidate unknown top, comparator zero, all T7 bounds are upper bounds on the candidate).
- Delta scope: against contract revision 8 (15a2297) the only changed contract regions are front matter, items 4, 5, 11, new item 13, section 6 paragraph, section 8; revision 8 criteria, family rule and activation-strata bytes are unchanged. Workplan changed only in the section 0.1 entry and six markers (lines 589, 708, 709, 907, 916, 926), all pointing to section 0.1. Effects (a) to (f) in section 8 match item 13 text and directions, except (d) lacks a direction (B-2).
- Not executed: real-OMP runs and unit tests (code is unchanged and does not realize revisions 4 to 8; they would test nothing in scope).

## Evidence summary
Executed: byte-level package measurements, git diffs, cross-reference review of the five documents. Reused: none. Missing: any realization/rehearsal (expected D4), instantiated N and 0.8 arithmetic (still open), F-5.
Impact closure: A-1 touches contract item 13 only (two sentences) and the gate arithmetic sentence; D3, workplan entry/markers unaffected.

## Verdicts
1. D3 revision 8 as D3: PASS, with conditions B-3 to B-9 and the rehearsal-form additions for the D4 stage.
2. Contract revision 14: NO-PASS on A-1 only (text fix). Re-check can be limited to item 13 Replacement/T7 bullets, gate sentence and amendment section 5 item 1.
3. Workplan section 0.1 entry and six markers: PASS (consistent with D3 and the overlay convention; the entry's "unresolved and replaceable" statement is the D3 intent that A-1 asks the contract to match).

## Confirm with the stakeholder
- Whether "never replaced" for the owner floor means a pre-R2 positive read only (recommended), and whether a non-T7 burden run with post-R2 positive owner evidence (an expected owner load on class iii) and inexact bytes should remain non-replaceable.
- That an honest pre-R2 package-wide keyword grep showing at least 256 bytes over two owner lines is intended to be a non-replaceable FAIL.

## Reviewed identities and independence
fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783  qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md
0084c081e7ba5a186f017283b9c1297828874422a0dc959e4bcaa320583a7001  qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md
b9ff09f9accd42a2ec3cc244dc1e3652763d4635bd08e99e1f18e57711fa61e2  qualification/ssdp70/PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md
6a69d54361c678dbde85d01d12518bb546386720bcde85350b7c5e523f269ac7  qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md
526aa3c7b0875c6f260e716a24bcc5bd42ee4cca6131b90968a38d653951353a  workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md

Independence: I did not read the earlier review reports, /tmp SSDP70 files or memory. Common-mode: same model family and same repository as the authors; the quantum measurement used only repository bytes.
