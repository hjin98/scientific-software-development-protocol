---
kind: independent-d3-and-qualification-contract-review
governing_protocol_version: 6.6.0
date_utc: 2026-10-05
base_commit: 6d09418b3d5946207324d7f53956eaaf34c6726e (plus the uncommitted subject bytes below)
reviewer: independent context; did not author any subject byte
subjects:
  design: qualification/ssdp70/D3-PROTOCOL-7.1-OBLIGATION-SALIENCE-AND-STRATIFICATION-DESIGN-2026-10-05.md sha256 75003ab846304afc985b7b72a53511ebb24d6b6fa408decbd512f059ae203915 (verified)
  contract_rev16: qualification/ssdp70/PROTOCOL-7.1-QUALIFICATION-CONTRACT-AMENDMENT-2026-10-05.md sha256 94d6b0ed2ded2f59244ba9208f9ce4c7d0d6e27bef8fdb098a10ed2ca45f646a (verified)
  overlay_rev8: workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md sha256 c4f0f604bc71036a019a15b464e2ee0413f30cc17be48494d73e3b732d67bbb6 (verified; scope = the new §0.1 "Option B re-open" entry and the two changed header lines per `git diff`)
design_verdict: NO-PASS
contract_rev16_verdict: NO-PASS
overlay_rev8_verdict: PASS
---

# Independent Review: Protocol 7.1 delegate-request salience design, contract revision 16, overlay revision 8

Governing SSDP version: 6.6.0. Applied: the `software-design` Independent Review and Challenge contract. All 7.x material is non-governing development data.

## Serious Challenge

None. The accepted authority (§4, §8.3 elements and label table, §11.3 rules, owner §6.3.11) is coherent for this change. The defects below are in the subject records, not in their parents.

## Blockers (by earliest owner)

### B-D1 — Design §5 / Appendix A: the reference wording is not lossless, so the §5 "carried" verdicts are false

The frozen CD-1 to CD-6 decisions are sound. The defect is in the relocation map and the measured wording used as feasibility evidence. Two meanings are weakened.

1. **"On return" narrows element 1's gap rule.** The receiving-side rule opens "On return, report each unanswered part … findings always; …". Frozen element 1 has no return condition: "Report an unanswered part … as a gap" (the current D4 text says "Unanswered findings are always a gap"). Only element 2's variant gap is conditioned on a returned result. The block also removes element 1's own delegate sentences, so nothing else carries the duty.
   - *Failure scenario:* a delegate times out, crashes or exhausts its budget and returns nothing. Under the reference wording no findings or null gap is owed, and the delegator reports the delegated work without one. That is the silence the findings part's no-exemption rule forbids.
2. **The Variants question narrows the requested disclosure.** Element 2 and §6.3.11 ask for the delegate's "variant-search disclosure". By the label table, that includes selection data with held-out reuse and, where earlier history is unavailable, a known lower bound, unknown interval and claim limit. The reference question asks only for "count and kind, selection criterion and data, and lineage". CD-2's premise is that agents copy the questions verbatim (checklist probe), so the narrowed list is what reaches the delegate.
   - *Failure scenario:* a resumed delegate whose earlier history is unavailable is never asked for the bound and interval. Its local count is returned and carried forward as the whole search, against the §3 variant-disclosure floor's "or the specified lower-bound/unknown-interval/claim limit".
   - §5 row E2a's claim "disclosure fields named" is therefore false.

*Repair (cheap):*
- drop "On return," or replace it with a condition that covers non-return;
- either ask for "your variant-search disclosure" or name the full label-table field set;
- re-measure, and correct the §5 verdicts.

My estimate for the fuller variant wording is about +111 B net per role. That puts the D4 generated entrypoint near 15,138 B, still under 16,208 B. Without this repair, the design's lossless claim, which D4's independent lossless check is told to check against (§7), is wrong.

### B-C1 — Contract revision 16 A2: the concealment rule's checker scope is unrealizable, and the rule is ambiguous about the facts owed dispositions depend on

1. **A cue that A2 bans is outside A2's verification scope.** A2 says executor-visible artifacts must not state or imply that a delegate is scripted or stubbed. It has the pre-run checker verify this "on the executor package". The current delegate mediator, however, returns model-visible tool content that names the stand-in.
   - In the checklist probe run `runs/C042-p70ck-r1/trace.jsonl`, the `delegate` tool-result `content` seen by the model is `{"evidence": {…, "store_identity": "ssdp70-private-issue-standin"}, …}`, from MCP server `ssdp70`.
   - A re-call returns byte-identical content (`raw_result_sha256` 96911bdf… on both calls), which by itself reveals the scripting.
   - Fixture delegates must stay wording-independent (§11.3), so the second cue cannot be removed. A2 as written promises a property the mechanism cannot give and verifies it where the known cue is not.
   - *Repair:*
     - extend the checker scope to the runtime-visible delegate interface: tool name and description, and the mediator return wrapper;
     - state as a disclosed residual that a delegate's wording-independent re-return reveals scripting.
2. **Task facts and return facts are not distinguished.** The rename and compaction cases' null and variant exemptions, and the silent-delegated-review case's element 3 non-applicability, rest on facts that must be evident to the delegator before the return. Examples are "fully specified by the task, with no run", "launches_work: false" in the current case files, and "no accepted D1/D2 authority governs that dataset".
   - A2 bans artifacts that "pre-state or summarize a delegate's return or envelope". A "no run" or "launches_work: false" statement can be read as pre-stating the null envelope or the launched-work coverage.
   - *Failure scenario:* the checker either voids those cases, or the custodian strips the evident facts. Either way an exempt part becomes an owed gap, and the §11.3 unowed-gap and burden dispositions flip.
   - The chained-case sentence ("may show only … that the delegate launched work") also leaves open whether that is visible before or only after the return.
   - So the property §5 of the amendment asks to be checked ("A2 hides no fact any owed disposition depends on") cannot be confirmed from the text. "Not SSDP governed" itself is safe to conceal: owner §6.3.11's request and gap rules do not depend on governance status.
   - *Repair:* say that task facts the §11.3 cases require to be evident to the delegator stay visible and are not return pre-statements, and fix the chained-case timing.

## Gaps (should be fixed with the above; not independently blocking)

- **G-1 — Evidence is restated without its timing caveat.** Both probes counted reactive follow-up calls as requested parts ("Follow-up calls count and are flagged"). Under A3's timing, which this cycle adopts, the checklist-probe figures fall.
  - My recount from the scorer's own annotations in `scores.json`: p70ck core 46 → 42/50 and strict 4 → **0/50** (all four strict hits were follow-up-only, C042-r1); fully conformant 12 → 11/14. p70 core 14 → 10/50 and strict 5 → 2/50.
  - The design (§2, §3), the overlay's evidence line and A2's rationale quote the lenient figures without saying so. The direction (copyable questions lift core uptake) survives. The 100% strict floor's feasibility evidence is zero pre-return strict hits, which strengthens R3.
- **G-2 — CD-7 scores only core and strict.** The checklist probe observed unowed tension requests (C048, C052). The §5 bound allows at most 1 unowed request part per 12 eligible parts. A copyable four-question block is the likeliest cause of that failure. CD-7 and R3 should also score unowed request parts and unowed gaps against §5, and A3's follow-up timing.
- **G-3 — A3 and scripted delegates.** "Its answer can still supply the part" depends on how a scripted delegate answers a post-return message. The current stub re-returns identical bytes. The contract should predeclare that follow-up behavior (arm-independent) and say whether a re-invocation after return is a follow-up or a new delegation. The design's §6 summary of A3 ("scored on the instruction that launches") also omits A3's pre-return-message allowance.
- **G-4 — A1 scope.** "Fresh fixtures for every case" should be scoped to custodian-authored §11.3 and blind material. As written it could be read to replace the 6.6 paired preservation panels (S01–S11/H01–H05, P01–P19, T1–T8), which must stay matched to their 6.6 and 6.5 baselines. The contract also needs a reading rule for its "7.0 arm/candidate" references.
- **G-5 — A4 wording.** "Every headline count names its stratum and profile key" conflicts with §1 item 12's mandated pooled predicate-false-firing and owner-false-activation counts, which pool across family keys and both strata; that pool needs a carve-out. "Never … comparative evidence" is too broad: ordinary runs are where the description (selection-surface) change acts. It should read "comparative evidence of doctrine effect". A4 otherwise loses no reported information.
- **G-6 — Missing stakeholder record.** Option B has no stakeholder record. The design discloses this. Every earlier governed overlay rests on a verbatim stakeholder record, so record the direction verbatim before acceptance. The closeout decision §3 does anticipate redesign.

## Minor

- **m-1 — OD-2 scope inconsistency.** Design §0 says OD-1 and OD-2 "bound the contract amendment, not the entrypoint design". However, CD-5's feasibility (16,208 B) and the overlay's "against the 16,208 B static limit" hold only if OD-2 carries the "for Protocol 7.0 only" 2.0× backstop. Otherwise the limit is 1.10×, about 9,196 B, which 14,454 B already breaches (R4). OD-2 is correctly treated as blocking in §10, the contract §1 and the overlay status. State the dependency in §0 and CD-5.
- **m-2 — Tension question beyond element 3.** The tension question's "including any tools or agents you launched" and "(or none)" go beyond frozen element 3's request text. The owner's Form sentence and the §3 row arguably support the launched-work clause. Under SD-B these bytes are attributable only on that reading; record it for the attribution check, alongside OD-3.
- **m-3 — Acceptance list too narrow.** §7 acceptance lists static re-measurement of only the D4 entrypoint. §8.3's *Static pre-measurement* also requires owner sizes per observed mode (T7 workflow owner) before any live run. The obligation is unchanged, but keep it on the list.
- **m-4 — Stale §0.1 lines.** The existing package-access §0.1 entry and contract §8 still say "pending independent Review" for revision 15, which has a PASS. The overlay's "reused unchanged" sits next to that stale text. The package-access entry also never received an overlay number, so "revision 8" here should state that it is the next activation-overlay number.
- **m-5 — Header scope.** The header field `implementation_handoff: not-authorized-…` is file-global. Scope it to the salience/entrypoint D4, so it is not read as withdrawing separately governed package-access/harness D4 work. `target_protocol_version` stays `7.0.0` pending OD-1, which is acceptable.
- **m-6 — No §8.3 marker.** The overlay adds no "[Affected by … overlay revision 8]" marker at §8.3, unlike the earlier overlays.
- **m-7 — Delegate-route convergence not addressed.** The workplan's *Delegate-route convergence* paragraph prescribes narrowing the claim as the remedy after further delegate findings. The design does not say why a form change rather than a narrowing is the right response to Stage 7. R3's "floor reconsideration" partly covers this.

## Checked and holding

- **Losslessness, other than B-D1.** All of these are carried in the reference wording:
  - the condition "unless the predicate evidently excludes";
  - the same delegate set for every part (element 2's "each delegate asked for findings");
  - launched-work coverage in every question;
  - the null envelope with its label meaning;
  - change-only owed answers, and element 1's "adds nothing except asked delegate answers/gaps", which stays in place;
  - the findings part with no exemption;
  - the null exemption, which is stricter than the current D4 text;
  - the variant "returned result" condition and exemption;
  - unknown selection history and the claim limit;
  - the partial-coverage rule;
  - the tension gate and its fields.

  Specialists keep E1 only, matching frozen specialist placement and owner line ~399. "Consequential judgment" and "tension" keep their label meanings on the surface through element 3's retained text.
- **Authority.** Reading the block as internal structure of the one §8.3 completion clause is defensible:
  - the existing realization is already a separate "Scientific completion…" section;
  - element numbers are not an order;
  - only Protocol 7 additions move, so the 6.6 text-preservation rule holds.

  The overlay covers the alternative reading. The specialist two-question scope matches frozen placement and owner. CD-6 timing matches owner "in its instruction" and §11.3 "the delegator's instruction". No O1–O3 or §4.5 change was found.
- **Burden arithmetic.**
  - 2.0 × 8,360 − 512 = 16,208 B, from the backstop record.
  - T1, T7 and T8 are all rooted at `software-implementation` (`qualification/ssdp66/eval/scenarios.yaml`).
  - The D4 dist entrypoint goes 14,454 → 15,027 B, leaving 1,181 B.
  - Routing OD-3 (per-question repetition under SD-B) to the stakeholder rather than self-deciding is correct. SD-B's "redundancy is a D4 defect" can plausibly be read against the repetition.
- **Evidence figures.** Checked against `tally.txt` and `scores.json`: core 14→46/50, fully conformant 1→12/14, strict 5→4/50, 6→10/25 (one replicate), and 211 of 244 no-root runs. The figures are quoted correctly, with development-data limits stated (but see G-1).
- **Contract.**
  - The claim that revision 8 already realizes the strata objectives is accurate (§1 item 12, §3 activation row; independent PASS in `ACTIVATION-OVERLAY-REV7-AND-CONTRACT-REV8-INDEPENDENT-CHECK-2026-10-04.md`).
  - No A-delta changes a numeric threshold.
  - The text A4 replaces exists verbatim (contract line 112).
  - The contract file sha256 equals the amendment's `amends` value.
  - Treating OD-2 as blocking is correct: the backstop record says "For Protocol 7.0 only".
- **PEM.** `main` = 2585b73f…, and the PEM blob 15617971… is identical on HEAD 6d09418. The HAS dispositions are plausible. No PEM mutation.

## Executed checks

| Check | Result |
|---|---|
| `sha256sum` of the three subjects | match the brief |
| Own byte re-measurement: Appendix blocks extracted from the design file; sentences located by regex at `git show 6d09418:source/…`, each matched exactly once (also in committed dist); block inserted after the heading (scratch script `…/scratchpad/rev/mine.py`) | Role block 1,589 B (+1 B newline = 1,590). Deltas: roles +573, documentation and audit +379. D4 dist 14,454 → 15,027. software-design dist would be 17,111 B, but that is not a backstop route. Reproduces the reference script, which I read and found consistent. |
| `python3 -m unittest tests.test_protocol_70_scientific_inspectability` at HEAD | 9 tests OK (the pytest plugin environment is broken, so unittest was used) |
| `git diff --check`; trailing whitespace in both new files | clean / 0 |
| Probe data: `tally.txt`, `scores.json` follow-up recount; `C042-p70ck-r1` `tool-calls.jsonl` and `trace.jsonl` | Figures as in G-1. The stand-in cue and identical re-return were observed (B-C1). |
| Read the owners | owner §6.3.11 and lines ~395–405; workplan §0.1, §8.3 (elements, table, specialist placement, SD-B, backstop), §11.3 delegate rules; contract rev 15 §1 items 7 and 12, §2, §3, §4, §5, §8; the backstop, closeout and stakeholder decision records; `scenarios.yaml`; the current D4 entrypoint |

## Not checked

- Package build, committed-dist parity against a fresh build, and the Orchestrator Core snapshot: no candidate source changed.
- The other role entrypoints' completion text beyond the exact-match removal.
- The deterministic-activation decision record beyond its version scoping.
- The earlier ACTIVATION-* reports beyond their verdict lines.
- Other probe runs beyond C042-p70ck-r1 for the stand-in cue. The cue comes from the shared mediator, so I expect it in all of them, but I did not verify that.
- No live run.

The verdicts accept no implementation, change no qualification determination (Protocol 7.0 remains NON-QUALIFIED), and leave D4 unauthorized under the overlay's own status line.
