# Independent check: contract revision 15 (package-access ledger replacement eligibility)

Governing SSDP version: 6.6.0 (Protocol 7.0 NON-QUALIFIED). Reviewer role: independent D3/contract Review under the software-design Review/Challenge contract. I did not author these bytes.

Subject: commit `b8c706f3a8c5ae94bbf0639222e47fe3f8b4ffe6`, tree `742eff06eb019d8f606dcab9e3b6d9c63e66937a`, parent `07a4bb0d2093605425374ac3102c6ac04dbe1652`. HEAD verified equal to the subject. There are no tracked modifications, and the eight untracked files are out of scope and were not read. I read the committed bytes with `git show`/`git diff 07a4bb0 b8c706f`. I modified nothing in the repository.

Excluded by instruction and not read: the committed earlier-review reports `qualification/ssdp70/PACKAGE-ACCESS-LEDGER-INDEPENDENT-*.md`. That includes the new file `…-CHECK-D3-REV8-AND-CONTRACT-REV14-2026-10-04.md`, which this commit adds and whose diff I filtered out. I also did not read any `/tmp/SSDP70-*`/`ssdp70-*` file or any memory directory.

## Serious Challenge

None. The rev15 eligibility rule bars replacement only on a positive owner read before R2. It can be realized on top of D3 rev 8 item 4a without new mechanism. It removes the rev14 dead end (an honest scan followed by a legitimate post-R2 load) without opening a path by which a pre-R2 positive read is replaced away (see the table and B-1).

## (A) Blockers

None found.

I tried to falsify the three protected honest cases named in the brief. Each has exactly one disposition and a path to resolution:
- **Honest pre-R2 package scan, then a legitimate post-R2 owner load.**
  - Owner floor: UNRESOLVED, because the scan's owner open is not provably post-R2 (D3 4a, boundary (m)/(n)).
  - Bytes: inexact (`grep -rl` opens are unexplained).
  - No positive pre-R2 read, so the run is replaced (mandatory). The replacement is the scored run, and the post-R2 hit is disclosed on the original, which is not counted (item 13 Replacement, §8(d), decision record round 5 item 1, amendment §5 item 1).
  - This now matches the D3 residual "an honest scan before a legitimate post-R2 load costs a replacement".
- **Non-T7 burden run with inexact bytes and a post-R2 owner-load hit.** Replaced. Round 4 item 4 is superseded to that extent, and the contract text says the same.
- **T7 run UNRESOLVED on the owner floor.**
  - It may be rerun solely for the owner floor, at most twice, outside the median.
  - Its burden value stays unknown under the adversarial assignment.
  - Pair addition runs to seven pairs.
  - The bar is now keyed on a "positive owner read before R2", which is consistent with the Replacement bullet.

No combination I could build gives a PASS from an inexact observation. A replacement resolves a slot only if it is itself exact for that question. T7 resolves only under the adversarial assignment. No pre-R2 positive read escapes FAIL when the text is read with §4 (B-1).

## (B) Non-blocking items (conditions for the D4 stage / text tidy at next touch)

- **B-1: Eligibility when R2 timing is ambiguous and positive owner evidence exists.**
  - Rev15 narrowed the bar from "positive owner evidence" to "positive owner read before R2". An original whose owner content lies at an ambiguous R2 position, together with an inexact observation, cannot be classified as "without a positive owner read before R2" until the R2 adjudication is done. This is realistic: the same-response or parallel-tool R2 form appears in D3 item 8.
  - It is not a false-PASS path. §4 binds "every trajectory", requires ambiguous R2 timing to be "independently adjudicated before a pass", and item 13 says a pre-R2 positive read "stands as a FAIL and is never replaced". The original stays on record, so an adjudication that places the read before R2 is a FAIL whatever the replacement shows.
  - D4/campaign condition: adjudicate ambiguous R2 timing on any original that carries positive owner evidence before deciding replacement eligibility, and record the ordering.
- **B-2: §8(d) says "neutral on outcome", which overstates.**
  - Replacement is mandatory and outside the checker's control, so there is no selection by the checker.
  - But the trigger, inexactness or an UNRESOLVED owner floor, is caused by subject behaviour (scans, partial reads, minor exposure) that plausibly correlates with higher consumption. Rev15 adds post-R2-owner-load runs, which are by construction high-byte runs, to the replaceable set for non-T7 burden routes.
  - Burden medians are then measured on a censored sample. The frozen between-arm inexact-rate bound and the per-case cap of two limit this. It is a residual, not a neutral property.
  - Suggest: "neutral by design; residual informative-censoring bias on burden bounded by the between-arm bound and the per-case cap". The rehearsal should report per-arm byte totals of replaced originals where they are computable. Confirm with the stakeholder (below).
- **B-3: §8(f) and the item 13 *No ledger* bullet differ.**
  - §8(f) lists positive pre-R2 evidence as "a native `resource_access` event, or owner-class supply where it is observed", for a no-ledger profile and for a lost-observation ledger run.
  - The *No ledger* bullet names only a native pre-R2 `resource_access`. Read literally, (f) extends FAIL to owner-class supply on a no-ledger profile, which item 13 does not state.
  - Both readings are non-PASS, because owner claims are INADMISSIBLE on a no-ledger profile, and the extension is stricter and applies only to genuine positive evidence. So the verdict cannot be wrong; only the label FAIL versus INADMISSIBLE differs.
  - Align them: either "owner-class supply on a ledger run whose observation is lost" in (f), or add it to the No-ledger bullet. The workplan §0.1 summary also mentions only the no-ledger native case and omits the lost-ledger extension.
- **B-4: The T7 owner-floor rerun cap is labelled "(the §5 cap)", but the unit differs.**
  - §5's cap is "two independent reruns per affected **non-T7 case**". Item 13 T7 says "at most twice per affected **run**".
  - With up to 7 pairs, that allows up to two reruns per T7 run, not per case.
  - This is consistent with the stakeholder's "no campaign-wide cap on owner-floor replacement" and cannot create a PASS, but it is a distinct rule, not §5's. Relabel it and declare it in §8(e).
  - The T7 rerun is also "may", while non-T7 replacement is mandatory. Not rerunning only leaves the floor non-PASS, so this is not a selection channel.
- **B-5: The supersession record is incomplete.** Decision round 5 item 1 names only round 4 item 4 as superseded. Round 1 item 1's eligibility phrase "with no positive owner evidence" is overridden only implicitly, by round 5's "Only …". Name it explicitly at the next touch. The amendment §1 *Authority* still lists "second, third and fourth rounds".
- **B-6: Fresh D3 acceptance is stated inconsistently.**
  - Item 13 *Ledger profile* ("a change … to this item … is a joint change and requires fresh independent acceptance of all"), §8 and the decision record all require a fresh check that covers D3 rev 8. Amendment §7 lists only the contract as still blocked.
  - The workplan entry still says D3 rev 8 is "pending independent acceptance".
  - This review supplies verdict (2) below, which settles the matter for this delta. Align the wording at the next touch.
- **B-7: "No positive evidence" in §8(b), the workplan entry and D3 4a is ambiguous.** It could mean any positive evidence or pre-R2 positive evidence. The rule cannot produce a false PASS: D3 4a's negative conclusion independently requires that no owner open is not provably post-R2, so a run with a scan plus a post-R2 hit is still UNRESOLVED (D3 lists "a scan before a legitimate post-R2 load" in the same sentence). D4 should implement the UNRESOLVED state as "negative not concluded", not as "no positive evidence of any kind".
- **B-8 (pre-existing, not part of this delta): per-question availability when the byte bound is absent.** "The scored run for every criterion of that slot" sits beside "absent a frozen bound, replacement for the byte question is unavailable". For a run replaced for the owner floor whose original bytes were inexact, D4 must keep the burden slot non-PASS rather than score the replacement's bytes. Also, "observation-inexact original" has to be read through §8(b) to cover minor exposure with an exact ledger. Record both as D4 interpretation notes.
- **B-9 (D4 conditions carried, amendment §3a):** add the ≥256 B, two-line keyword-`grep` rehearsal form and report its FAIL rate; use `CLOCK_MONOTONIC` request stamps or record no host clock step; state where minor exposure is placed; reconcile the request-position primitive with the same-response R2 wording; reduce the workplan restatements of the quantum to pointers. The code at `8be024a` realizes D3 rev 3 only, and that absence is not a defect here.

## Evidence executed vs missing

Executed:
- HEAD, tree and parent verified. `git diff 07a4bb0 b8c706f` covers 5 files.
- In scope and read in full: the contract (status, item 13, §8), the amendment record, the decision record (round 5 and pending acceptance) and the workplan (two label changes on one line).
- Read for interaction: contract §1 item 7, §3 order, §4 (owner floor, R2 adjudication, T7 pair rule), §5 rerun cap, and §8 in full at the subject.
- Read: D3 rev 8 in full at the subject, with focus on items 4a, 5 and 8 and the residuals.
- I built the disposition table below by hand.

Missing or not done:
- No execution. The delta is text only and the code is unchanged.
- I did not verify the claim that the sixth check passed D3 rev 8 and the workplan entry, because I was barred from reading that report. I relied on my own verdict (2) instead.
- I did not verify the shipped-package line counts quoted in amendment §3a.

## Disposition table (ledger profile unless stated; "repl" = mandatory replacement, at most 2 per affected non-T7 case)

| # | Combination | Owner floor | Byte/burden | Replacement | Consistent across item 13 / §8 / amendment / decision? |
|---|---|---|---|---|---|
| 1 | Positive pre-R2, byte-exact, non-T7 | FAIL | scored exact | none (FAIL stands) | yes |
| 2 | Positive pre-R2, byte-inexact, non-T7 burden | FAIL | INADMISSIBLE, slot non-PASS, counted in gate | never | yes (round 5 keeps it) |
| 3 | Positive pre-R2, T7 (exact/inexact) | FAIL | exact value / unknown value | never | yes |
| 4 | Post-R2 hit only, byte-exact, owner opens provably post-R2 | PASS-eligible + hit | scored | none needed | yes |
| 5 | Post-R2 hit only, byte-inexact, non-T7 burden | per owner state | INADMISSIBLE on original | repl; replacement scored; hit disclosed, not counted | yes (rev15 repair) |
| 6 | Pre-R2 scan + post-R2 load (owner not provably post-R2), non-T7 | UNRESOLVED | usually inexact | repl | yes; matches D3 residual and (m)/(n) |
| 7 | Same as 6, T7 | UNRESOLVED | unknown value, pair addition | owner-floor-only rerun ≤2 per run, outside median | yes (B-4 label) |
| 8 | Owner open not provably post-R2, no content, non-T7 | UNRESOLVED | inexact if unexplained | repl | yes |
| 9 | Minor exposure pre-R2 / not-provably-post-R2, exact ledger, non-T7 | UNRESOLVED | may be exact | repl (via §8(b)); exact original bytes discarded (§8(d)) | yes with B-8 reading |
| 10 | Minor exposure, T7 | UNRESOLVED | exact or unknown | owner-floor-only rerun | yes |
| 11 | Byte-inexact, no owner involvement, non-T7 burden, bound frozen | PASS-eligible if no owner open | INADMISSIBLE | repl for byte question | yes |
| 12 | Same as 11, no frozen bound | as is | non-PASS (fail-closed) | unavailable for byte question | yes; resolution: freeze the bound |
| 13 | Byte-inexact T7, no owner issue | PASS-eligible | unknown value; PASS only under adversarial assignment | none (pair addition) | yes |
| 14 | Ledger run, observation lost, positive pre-R2 | FAIL (§8(f), Claim scope) | INADMISSIBLE | never | yes |
| 15 | Ledger run, observation lost, no positive pre-R2 | UNRESOLVED (owner_floor_exact false) | INADMISSIBLE | repl; overflow cause disclosed and counted | yes |
| 16 | Ledger lost + post-R2 hit only | UNRESOLVED; hit disclosed | INADMISSIBLE | repl | yes |
| 17 | No-ledger, native pre-R2 `resource_access` | FAIL | INADMISSIBLE | n/a (Replacement bullet is ledger-only) | yes |
| 18 | No-ledger, owner-class supply only pre-R2 | INADMISSIBLE (item 13) vs FAIL (§8(f) literal) | INADMISSIBLE | n/a | label differs, both non-PASS (B-3) |
| 19 | No-ledger, process execution, no positive evidence | INADMISSIBLE | INADMISSIBLE | n/a; resolution is a ledger profile | yes |
| 20 | Positive owner evidence at an ambiguous R2 position + inexact | unresolved pending §4 adjudication | — | eligibility after adjudication; FAIL stands if pre-R2 | yes by §4 "every trajectory … before a pass" (B-1) |
| 21 | Original with another failure / suspected O3, claim or mutation violation | per criteria | per criteria | not replaced | yes |
| 22 | Replacement itself inexact or UNRESOLVED | — | — | second rerun; after cap the slot stays non-PASS | yes |
| 23 | Replacement shows a pre-R2 positive read | FAIL (scored run) | — | none | yes; no selection |

Selection resistance:
- Replacement is mandatory, not at the checker's option.
- The replacement is the scored run, including when it is worse.
- The original stays on record with its cause and is not counted.
- There is a per-case cap.
- A between-arm inexact-rate bound is frozen before runs, and its absence fails closed for the byte question.
- The owner floor has no rate bound, by stakeholder decision; this is the accepted detection hole, to be revisited after the rehearsal.
- The residual informative-censoring bias is B-2.

Stuck-honest cases: rows 6–9 exhaust the cap only when honest behaviour systematically produces them. The resolution path is the rehearsal gate with its 0.8 target and the D3 reopen trigger, not a contract dead end. Row 12 resolves by freezing the bound.

## Verdicts

1. **Contract revision 15, with the amendment record and the decision record: PASS.** There are no blockers. B-1 to B-9 are conditions for the D4 stage or tidy-ups at the next touch.
2. **Governing D3 revision 8 and the workplan §0.1 entry remain consistent with revision 15: PASS.** D3 4a, its residuals and boundary cases (m), (n) and (w) agree with the narrowed bar, and rev15 removes the earlier conflict with the D3 residual. Stale labels: D3 (iii) still names "contract revision 14", and the workplan says D3 is "pending independent acceptance" (B-6). Both resolve by path and are not contradictions in effect.

## To confirm with the stakeholder

- B-2: accept that replacing post-R2-load and scan runs leaves an informative-censoring residual on burden medians, bounded by the between-arm bound and the cap, and reword §8(d) from "neutral".
- B-4: whether the T7 owner-floor rerun cap is two per affected run (as written) or two per case.
- B-3: whether owner-class supply on a no-ledger profile is meant to be a FAIL or INADMISSIBLE.

## Commits and hashes reviewed

`b8c706f3a8c5ae94bbf0639222e47fe3f8b4ffe6` (tree `742eff06…`) against parent `07a4bb0d2093605425374ac3102c6ac04dbe1652`. Files in scope:
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`
- `qualification/ssdp70/PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md`
- `qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md`
- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`
- `qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md` (byte-unchanged; read for consistency)

## Common-mode limits

- This is a single reviewer doing a text-only analysis. The disposition table was built by hand, with no executable model of the rules.
- I did not inspect earlier review reports. Claims about the sixth check's verdicts are taken from repository text, not verified.
- Realization (heartbeats, windows, the quantum, replacement bookkeeping) is untested and may expose ambiguities that text review cannot.
- The informative-censoring magnitude (B-2) is unquantified until the rehearsal.
