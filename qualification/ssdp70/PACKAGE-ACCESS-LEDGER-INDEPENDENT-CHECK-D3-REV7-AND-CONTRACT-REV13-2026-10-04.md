# Independent check: D3 package-access ledger decision revision 7, contract revision 13, workplan §0.1 entry

- Governing SSDP version: 6.6.0 (Protocol 7.0 NON-QUALIFIED; accepted-current 6.6.0 at `22f4bdba…` per `PROTOCOL-RELEASE-STATE.yaml`).
- Reviewer role: independent reviewer under `software-design` Review/Challenge. I wrote none of the bytes under review. I did not read `/tmp/SSDP70-*` or `ssdp70-*` files, any memory directory, or the committed `PACKAGE-ACCESS-LEDGER-INDEPENDENT-*.md` reports.
- Subject: HEAD `16571a1b8c578c843a5eea27ccd41d044f0d78c5`, tree `b3fbe856790ae74ec7ef560c9970616c086da85b` (verified). Tracked working tree is clean (`git diff HEAD --quiet`), so the file bytes are the committed bytes. The eight untracked files are out of scope.
- Posture: wrap-up. Verdicts rest on blockers (A) only. Non-blocking items (B) become conditions for the D4 stage.

## Serious Challenge

**None against the mechanism.** The ledger, the supply-based positive evidence, the conservative provably-post-R2 test, the replacement rule and the T7 unknown-value rule can work as designed. Every blocker below has a text-only fix, with no new mechanism.

One problem is a contradiction inside accepted authority, so it is surfaced here: **stakeholder record, round 3, item 2** is self-contradictory on the shipped package (blocker A-1(ii)). Its headline says "a single matched owner line shown by a package-wide search is not a non-replaceable FAIL". Its rule says "a FAIL needs ≥ 256 bytes of whole owner lines in one result". On the shipped package 46 of the 242 owner lines of 48 bytes or more are each ≥ 256 bytes. For those lines the two clauses give opposite verdicts. Only the stakeholder can choose between them.

## (A) Blockers, by earliest owner

### Stakeholder plus D3 (item 4a, item 8, boundary (w))

**A-1. The owner-load quantum is under-defined, and on the shipped package it contradicts the stakeholder's protected case.** This produces manufactured pre-R2 FAILs and false owner-load hits.

Item 4a defines owner-class supply as whole owner lines (each ≥ 48 B) "occur[ring] as substrings of the result's lines … and total at least the owner-load quantum, 256 bytes". It then gives "one owner line shown by a package-wide keyword `grep`" as the example of minor exposure (below the quantum, UNRESOLVED, replaceable). Boundary (w) and stakeholder round 3 item 2 say the same.

- **(i) Occurrences or distinct lines? The text does not say.** The owner ships in 7 byte-identical copies, so a package-wide `grep -rn` that matches one owner line prints it 7 times.
  - Measured on `dist/skills` at HEAD: `grep -rn granularity` shows one distinct owner line of 254 B, which totals 1,778 B if occurrences are counted. `grep -rn observables` shows one line of 109 B, which totals 763 B.
  - Read as occurrences, every owner line of 48 B or more found by a package-wide grep (7 × 48 = 336 ≥ 256) is positive evidence. That gives a definite, non-replaceable zero-tolerance FAIL before R2, and a false owner-load hit after R2. Both contradict the stakeholder's protected case. The hit side inflates the §4 per-class hit floors, which is a false-PASS direction.
- **(ii) A single long line already reaches the quantum on its own.**
  - 46 of 242 owner lines are ≥ 256 B; the longest is 751 B.
  - 226 single-word keywords match exactly one owner line that is ≥ 256 B (for example `method` → 314 B, `burying` → 515 B).
  - So the D3 example, boundary (w) and the stakeholder headline are false for a large class of honest pre-R2 keyword searches, even if distinct lines are counted. Item 4a's definition makes these a definite FAIL. The stakeholder's headline says they are not.
- **Text fix (no mechanism).**
  - (i) Count each distinct owner line once per result. This needs no stakeholder input; it is the only reading consistent with the record.
  - (ii) The stakeholder chooses either "≥ 256 B of at least two distinct owner lines" (keeps the headline) or "one line ≥ 256 B is positive" (keeps the byte rule; then correct the example, boundary (w) and the headline).

### Contract revision 13

**A-2. §6 cites "its cases (a) to (v)", but D3 revision 7's D4 acceptance boundary runs (a) to (z).**
- §6 is the mandatory pre-run integrity suite. As written it leaves out:
  - (w): error-status owner supply, minor exposure, `cat -n` prefixes;
  - (x): request-stamp decrease and missing bracket-end heartbeat. This is the only known-broken probe guarding the timing path to a false PASS-eligible result;
  - (y): same-response load never a FAIL;
  - (z): the mechanical premise check.
- The same sentence also calls the set "the D4 acceptance boundary of the governing D3 decision", so the contract contradicts itself and contradicts D3.
- Amendment record §2 repeats "(a) to (v)".
- Fix: "(its cases (a) to (z))", or "all its cases" with no range.

**A-3. The owner-floor replacement bound contradicts the stakeholder record and D3.**
- Item 13 *Replacement* freezes, "per question … for the owner floor … an absolute bound on the candidate's replaced owner-unresolved fraction (R-op acceptance-process values confirmed by the stakeholder)". Without that bound, replacement is unavailable.
- The stakeholder record says the opposite twice:
  - round 2 (e): "there is no campaign-wide cap on replaced owner-unresolved runs beyond the per-case cap";
  - round 3 item 1: "no campaign-wide cap on replaced owner-unresolved runs beyond the per-case cap; revisit after the rehearsal".
- D3's residual (detection-hole bullet) agrees with the stakeholder.
- So the contract claims stakeholder confirmation for a value the record rejects. It also makes owner-floor replacement depend on a bound the stakeholder said does not exist. The direction is fail-closed (replacement unavailable, so the floor stays non-PASS), but this is an internal contradiction across three documents.
- Fix: drop the owner-floor bound (follow the record), or record a new stakeholder decision that adopts one.

**A-4. Whether an observation-inexact T7 run that is UNRESOLVED on the owner floor is replaced is contradictory.**
- *Replacement* replaces "a run `UNRESOLVED` on the owner floor" with no T7 exception (the T7 exception is stated only for burden runs). The replacement then becomes "the scored run for every criterion of that slot".
- *T7* says "an observation-inexact T7 run is not replaced"; the original stays and keeps the mixed-mode trigger on.
- §5 allows reruns only "per affected non-T7 case".
- These collide in the common case. On T1/T7/T8 there is often no R2 point, so a package scan always leaves an owner open that is not provably post-R2. The same scan also makes the bytes inexact.
- One reading (replace) discards the T7 unknown value, which counts as +∞ on the candidate. That is lenient against the T7 rule.
- Fix: say whether a T7 run is replaced for the owner floor only, keeping its burden value as unknown, or is never replaced, so the floor stays non-PASS. If the choice goes beyond round 3 items 3 and 5, confirm it with the stakeholder.

### Workplan §0.1 entry and markers

No blockers of its own. The entry's pointers and its summary of the four effects match contract §8. All six markers are present at the six named sites: Trusted runtime-observation (l.708), Root-selection (l.709), §11.4 (l.907), §11.5 (l.916), T7 replication (l.589) and backstop (l.926). The PASS is conditional on the A-1/A-3/A-4 fixes not changing the entry, and on B-13.

## (B) Non-blocking items (conditions for the D4 stage unless noted)

1. Item 13 *Claim scope* cites "the *T7 and burden routes* bullet". That bullet is now titled *T7*, and the sentence reads as if every route resolves by the unknown-value rule. Point it to *T7* and *Replacement*.
2. Amendment record §2 is stale. It lists four workplan markers and says "No other workplan text … changed", but six markers were added (§3 W-B1/W-B2 and the workplan both say so). The §6 row says "(a) to (v)".
3. D3 open-items bullet (iii) still says "Contract revision 12 … is the adopted resolution". The parents line says "§6 (revision 13, which adds item 13)", which is garbled because §6 does not add item 13. Both are stale or garbled pointers.
4. The `package_access` event field list (item 13) omits `owner_minor_exposure` and the owner-load quantum, although D3 item 4a publishes the first and freezes the second. This is not a false-PASS path: given the premises, pre-R2 minor exposure implies an owner open that is not provably post-R2. But recomputability should be complete.
5. **Request-position pairing.** Mispairing toward a later turn (for example a compaction or extra request counted as a conversation request) moves window starts later, which is non-conservative. D4 must verify the pairing, by checking that request k+1 carries turn k's assistant message and results and that the counts agree. On any mismatch, use the beginning-of-trace fallback. Add a rehearsal form for this.
6. **Clock residual.** Request stamps are `CLOCK_REALTIME` only. A realtime step that is reversed within one heartbeat interval passes the monotonicity and per-run-baseline checks. It could move one request stamp earlier and make a window start late. The subject cannot cause this (it is a host event), but D3 should state it as a residual. D4 should also stamp requests with `CLOCK_MONOTONIC`, or record that the host clock was not stepped during the run.
7. **Placement of positive evidence at result sequence.** With parallel tool calls where R2 is itself a tool action, sequential execution can put the owner `cat` result before the R2 action in the trace, although the model sees it only at the next request. This is unchanged from revision 8's native semantics and is covered by §4's adjudication of ambiguous R2 timing. Add a rehearsal form with "R2 as a parallel tool action".
8. **Order of replacement decisions.** Decide replacement eligibility only after the original's other criteria are adjudicated. An original with an unresolved suspected O3, claim-integrity or mutation violation must not be replaced. §3 and the workplan say replication "cannot average it away", and "failed for any other reason" does not literally cover "suspected".
9. **Owner-load hit plus inexact bytes.** On a non-T7 burden route (class iii and new classes) such a run has positive evidence, so it cannot be replaced and that burden slot stays non-PASS. The gate arithmetic must count this. Confirm with the stakeholder.
10. **§8 wording.**
    - Effect (b) says "observation failure with no outcome", but the original has outcomes; they are disclosed and not counted.
    - Effect (c): an outcome-neutral trigger that adds pairs can move the median either way, not only "stricter".
    - Effect (d): add its relation to item 7's no-omission rule.
11. The *No ledger* bullet scores a native pre-R2 FAIL while owner claims are `INADMISSIBLE`. That is an exception to item 7 (stricter) and is not declared in §8, which covers ledger profiles only. Declare it.
12. Stakeholder round 2 (d) "the one declared change in effect" is not explicitly marked as superseded by round 3 item 4 (four effects).
13. Workplan §0.1 and the §11.4/§11.5 markers paraphrase an owner read as "content shown to the model" without the quantum. Add "(a native read or ≥ the owner-load quantum; below it, minor exposure leaves the floor unresolved)", or reduce them to pure pointers.
14. The D4 code at `8be024a` realizes revision 3. For example, `harness70.py` still publishes `observed_ssdp_bytes_lower_bound` when the observation is inexact, which item 13 now forbids. It also nulls `owner_read_sequences` unless exact, `owner_reads` matches by substring, and there are no heartbeats, windows or quantum. All of this is expected D4 work under the revision 6 and 7 notes.
15. **Premise check scope.** Extend "no byte-identical copy reachable" to copies in any encoding (git objects, archives). A hidden transformed read of a non-package copy produces neither an open nor supply, so it would be PASS-eligible rather than UNRESOLVED. Contract item 2's "exactly one copy" partly covers this.
16. *T7* says "pair addition adds exact pairs". This should read "adds pairs; inexact added runs are again unknown values".
17. Item 8 says "common honest forms must be exact by construction" but does not list them. Freeze the list with the rehearsal plan.

## Things to confirm with the stakeholder

- **A-1(ii):** which clause of round 3 item 2 governs a single matched owner line of ≥ 256 B. This is about 19% of owner lines and is reachable by 226 single-word keyword searches.
- **A-3:** whether there is any campaign-wide owner-floor replacement bound. The record says none; the contract requires one.
- **A-4:** how a T7 run that is UNRESOLVED on the owner floor is treated.
- **B-9:** hit-plus-inexact non-T7 burden runs cannot be replaced.
- Under the quantum, a post-R2 keyword grep showing ≥ 256 B of distinct owner lines counts as an owner-load hit. This may inflate §4 per-class hits.
- Owner content shown in chunks below the quantum across several pre-R2 results is UNRESOLVED and replaceable, not a FAIL. This follows from "in one result" in the record. Confirm it is accepted as part of the detection hole even though the content is visible, not transformed.

## Evidence

**Executed (this context):**
- HEAD and tree identity; tracked tree clean.
- Diff of the contract and workplan since the revision 8 PASS commit `86ed09a`. Revision 8 bytes changed only by punctuation and §8's stale "no independent check" sentence, so the criteria, family rule and activation-strata bytes are unchanged. Their effect changes only through the four declared effects in item 13 plus B-11.
- Shipped package shapes extracted with `git archive` and computed: HEAD `dist/skills` 238/63/38/213; 6.6 public ref `22f4bdba…` 212/62/37/187; 6.5 public ref `7f7b5e24…` 198/60/35/173. All three match.
- Owner premise on HEAD:
  - 7 copies, 1 distinct content, 45,958 B;
  - 242 owner lines of ≥ 48 B (all distinct), 0 of them occurring in any non-owner file;
  - comparators ship no owner;
  - the only singleton reference file is `software-implementation/references/debugging-and-state-recovery.md`.
- Keyword-grep simulations for A-1.
- Line-length distribution: 46 lines ≥ 256 B, maximum 751 B.
- `python3 -m unittest test_package_ledger test_batch_cli`: 40 tests OK. This exercises revision 3 code only and is no evidence for revision 4 to 7 behaviour.
- Static reading of `harness70.py` (owner and accounting paths), `adapters/omp.py` (`normalize`, `owner_reads`, `consumption`) and `package_ledger.py` (owner-copy rule) for realizability.

**Reused:** none. No earlier review conclusions were read.

**Missing or not applicable:**
- No real-OMP run. The code realizes revision 3, so a run would not test revision 7.
- No rehearsal (not built).
- No premise check over fixtures, workspace, stubs, MCP results or task text (not frozen or withheld).
- D3's "about 28 shared sub-line runs" figure not verified (not load-bearing).
- inotify event coalescing not probed. By reasoning it drops only later identical events, which is conservative.

## Impact-closure state

Not closed. The A-1 to A-4 fixes are text-only and touch:
- D3 item 4a, item 8, boundary (w) and the open-items bullet;
- contract item 13 (*Replacement*, *T7*, *Claim scope*) and §6;
- amendment record §2;
- possibly stakeholder record round 3 item 2 (A-1(ii)) and round 2 (e) or round 3 item 1 (A-3);
- workplan §0.1, §11.4 and §11.5 marker wording (B-13).

After the fix, a fresh check limited to these deltas is enough; revision 8 is untouched. No D4 evidence is bound to any accepted tree yet.

## Verdicts

1. **D3 revision 7: NO-PASS.** Blocker A-1 (quantum counting rule undefined; single-long-line contradiction with the stakeholder's protected case; manufactured pre-R2 FAILs and false post-R2 hits on honest package-wide keyword searches). There is no other D3 blocker. Timing, windows, request position (with B-5), error-status supply and route (iii) hold up under falsification.
2. **Contract revision 13: NO-PASS.** Blockers A-2 (§6 probe range (a)–(v) versus D3 (a)–(z)), A-3 (owner-floor campaign bound contradicts the stakeholder record and D3) and A-4 (T7 owner-floor replacement contradiction). It also inherits A-1 through its pointer.
3. **Workplan §0.1 entry and six markers: PASS with conditions.** The conditions are B-13, and that the entry is not changed by the A-1/A-3/A-4 fixes. If those fixes change it, a delta check is needed.

## Reviewed bytes and independence

- Commit `16571a1b8c578c843a5eea27ccd41d044f0d78c5` (tree `b3fbe856…`). D4 code unchanged since `8be024a3b1c71332121679a7b60a97b58facdde0` (verified).
- SHA-256 at HEAD:
  - D3 decision `a83c674f…3584`
  - contract `7dae713e…8a62`
  - amendment `5aa8c4b5…252d`
  - stakeholder record `9a9de078…2782267`
  - workplan `dd0d240f…c609c5b`
  - `package_ledger.py` `71cb1c8f…69e4b`
  - `harness70.py` `b58d8637…89a`
  - `adapters/omp.py` `dfc2b1ae…5ac`
- **Common-mode dependency:** I am the same model family as the authoring context and earlier reviewers. I relied on the repository's own package build (`dist/skills`) and public refs for the shapes. Simulations used GNU `grep -rn` output, not OMP's native `grep` formatting; the 7-copy multiplicity holds in any per-match output format.
