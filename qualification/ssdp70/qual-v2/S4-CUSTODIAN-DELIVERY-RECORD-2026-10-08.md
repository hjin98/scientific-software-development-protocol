---
kind: delivery-record
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate `2dedcfa`; non-governing)
date_utc: 2026-10-08
recorded_by: S4 analyst
---

Governing SSDP version: 6.6.0. This record is data.

# Custodian addendum: delivery and role naming

On 2026-10-08 (about 15:50Z) the stakeholder told the analyst to name the sessions and deliver the addendum. The analyst did this by launching agent sessions. That is weaker than separate human-operated sessions: the sessions share the host, and the analyst launched them. The stakeholder accepted that trade-off. The custody control is the written attestation and access log (decision 1 of the campaign draft), not technical denial.

| Role | Session name | Model | Status |
|---|---|---|---|
| Fixture custodian | custodian-7.2-a | claude-opus-5-5 (agent) | Launched with the addendum, revision 2, sha256 `fd29633c73804352896150569c5924299e9ac7ca8be9fed38969857b6c67124f` (repo commit `f7de43e`) |
| Independent check of the campaign draft and the S4 exposure changes (contract §8) | checker-draft-7.2-a | agent, default model | Launched earlier the same day; report pending |
| Pre-run checker (P5) | not yet named | must be a fresh session, not custodian-7.2-a, not the analyst | Open |
| Evaluator | not yet named | a model other than the executor (GLM-5.3-Flash); recommended claude-opus-5-5 in a session separate from the custodian | Open until the evaluator profile is frozen (campaign draft gap 6) |

## Scope delivered

Only the addendum, items 1, 2, 5, 6 and 7: calibration fixtures, owed-ness rulings and attestation, in a new store at `~/ssdp72-fixture-custody` (outside the repository). The full P3b corpus, keys, aggregate-oracle changes and human-trial banks are **not** delivered. They need their own work order, because the 7.1 custodian work package depends on retired tooling.

## Custodian constraints stated in the delivery

- It may open only the old store's `CUSTODY-RULES.md` and `HARNESS-INTERFACE.md`.
- It must not read the S4 report, any S4 or 7.1 run directory, or the adjudication.
- It must not edit the repository.
- It reports counts, digests, opened paths and UNDETERMINED items only, with no fixture text.
- It leaves `FREEZE-GATE.json` unfrozen.

The analyst does not open the new store and does not read fixture content. The analyst reads only the counts and digests the custodian reports.

## Update (same day): revision 3 and the first custodian report

- The independent check found that revision 2 disclosed candidate-result figures, the adjudication class and named hit mechanisms to the custodian, and invited a re-read of development runs. Revision 3 (sha256 `69594fb935faf7ca7d1bdea941206e3bcd810229627aa8037224be7df826ec89`, commit `9392ac7`) removes them.
- The custodian's **first pass ran on revision 2** (it verified revision 2's digest). It reports that it did not re-read the development runs or the S4 report, but it did read revision 2. Its fixtures are therefore not independent of that disclosure until it shows otherwise. Revision 3 and a follow-up were sent to it with instructions to record the disclosure in its attestation and rebuild any fixture it cannot show derives from the contract and protocol text. The stakeholder may instead restart with a fresh custodian session on revision 3.
- First report (counts only): 121 fixtures in `~/ssdp72-fixture-custody`, 119 with a fixed verdict and 2 UNDETERMINED; store unfrozen; FREEZE.sha256 file digest `2fe5ef768325ae2ba4db89dbc63a6245931e96a4d0d45bc55ab71be08cfd5916`; ATTESTATION digest `b23de24e158d8861fa747872cc429eadc0dead63c6c4136cbe56d3179ca6550e`. It found the old store path in the addendum does not exist (D-1), and that a deterministic Q4b/Q4d oracle needs structured trace facts (D-2). Open rulings are in the campaign draft, section 8, items 8 to 10.

## Second custodian report (after revision 3 and the follow-up; counts only)

- Store unfrozen. FREEZE.sha256 file digest `6f1199d30ef71c5302c4f937c8edfff6b129a5d556e8b34f4899bc628d959a95` (14 entries); ATTESTATION digest `3b90f1ee6db5a7dfe9a12f6f05b7f9cd4c909aec62530c47e878f009e1393e95` (entries 1 and 2). 121 fixtures: 26 carry a `pending` mark on an open ruling (14 on A-1, 2 on A-3, 1 on A-5, 6 on U-1, 1 each on U-2 and U-3).
- The custodian disclosed in attestation entry 2 that it read revision 2 in full before authoring (result figures, that hits were adjudicated, the hit mechanisms). It rebuilt 7 fixtures that reused revision 2's hedged-clause wording and kept six C1 fixtures with "none" headings, disclosed as possibly primed. It opened no run, transcript, episode or adjudication text. The stakeholder decides whether this residual contamination is acceptable or whether to restart with a fresh custodian.
- It read governing workplan §8.3 (in `SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`) and only `CUSTODY-RULES.md` and `HARNESS-INTERFACE.md` in `~/ssdp70-fixture-custody`. One ruling (R-5, owed-ness depends on the delegator's skill) changed; no verdict changed.
- Open rulings for the stakeholder before any freeze: U-1 (hedged clause under Q2b), U-2 (AST-preserving formatting of scientific source), U-3 (comment/docstring spelling fix), A-1 (gate for unearned claims), A-3 (scope statement in a non-owed run), A-5 (a part that drops its in-question qualifier), A-8 (fixtures assume the delegator is a D1-D4 role skill), A-9 (mapping of the classes to the 7.0 measure vocabulary). The interface mapping needs confirmation, and the fixtures and rulings need an independent pre-run check.
- The deterministic-oracle trace facts the custodian lists (D-2) are in its `calibration/FORMAT-AND-ORACLE-SPEC.md`; the analyst has not read the store.

## Custodian restart report (custodian-7.2-b; counts only; the analyst has not opened the store)

- Store `~/ssdp72b-fixture-custody`, mode 0700, unfrozen. Addendum revision 3 (digest verified). The custodian read rulings v1 (`004a7de6…659d`) first and authored against them from 16:09Z, then verified rulings v2 (`bef89f60…4117`, commit `2b56b85`) at 16:19:07Z and rebuilt what v2 affected. It reports that v1 had already shaped authoring.
- FREEZE.sha256 file digest `f51f79b3595575152ba7616dfc9d646f4f461d7b3770b376debfc4af74f13984` (16 entries); ATTESTATION digest `da2691edfe1e8ede9c6d774995a8dc845913992ca436208ed1ecfbbf529b29f1`.
- 125 fixtures: C1A 6/6, C1B 6/6, C1U 9/6, C2 10/7 (+2 pending), C5i 6/6, C5ii 6/1 (+6 label-only), C5-N 3, C6 7/7, C7 10/12 (+3 pending) as known-good/known-bad; 5 fixtures carry `pending` marks.
- Paths: it opened only the allowed files; it read workplan §8.3 and the two 7.0 interface files; it did not open the first store or any forbidden path; the git greps it ran scanned `dist/` and `source/` content and printed file names only.
- UNDETERMINED: U-A (read-only lookup delegated inside scientific code), U-B (spelling fix in scientific documentation or report prose outside source), U-C (conditional tension question when reliance on accepted authority is not evident), U-D (question set when the agent picks a different route or none), U-G (relaying a delegate's own answered null in a non-owed run), U-H (bare "tried no alternatives"), U-I (silently omitted gap that makes no false statement).
- Readings applied for the checker to confirm: A-x1 (OD-3 qualifiers taken from the candidate wording), A-x2 to A-x4 (parts not owed on a route, the hedged/full boundary), A-x5 and A-x6 (the undefined "non-owed run" and "disclosure"), A-x7, A-x8 (the 7.0 measure definitions were unavailable, so the A-9 mapping is name-based only), A-x9 (custodian labels for C(b), where the contract says analyst labels), A-x10 (scored-run ruling applied to Q4b, Q4c and Q4d).
- Defects in the work order, as reported: addendum item 2 still lists unearned claims under Q4d, which A-1 overrides; the contract gives no item definitions for claim integrity or over-reporting; the 7.1 layout differs from the prescribed layout.

## custodian-7.2-b second pass (after rulings set 2 and addendum revision 4; counts only)

- Inputs verified at 16:42:00Z: rulings `41e6faff156dbebaf3764615cf6c899afb662429e0d1c57d5c851836459fb52d` (commit `d7475ae`), addendum revision 4 `2a52d25f13f1e6f2e8a31015a2482e5c2bf34d4cff74c27baa97f22dfd18a3fb`. Opened only those two files and its own store.
- 132 fixtures, none pending, none removed: C1A 6/6, C1B 6/6, C1U 9/6, C2 12/8, C5i 6/6, C5ii 6/1 (+6 label-only), C5-N 3, C6 8/7, C7 16/14 (known-good/known-bad). Five pending fixtures resolved; seven added; the owed-ness rule, format spec, trace-facts spec, per-fixture rulings and MANIFEST regenerated.
- Digests: FREEZE.sha256 `68c16945eaffe97213a2161e00f72f39dad9d8e83b38962e648b918a9319c3cb` (16 entries); ATTESTATION `88f4a41a3a9d98ed2bdf74c28011e7709bf9d6e6dababc95d721778b13737ac4` (entry 2 appended). Unfrozen.
- Verdicts that still rest on a provisional reading: A-x1 (qualifier list taken from the candidate wording, OD-3 not seen), A-x2 to A-x6, and a new A-x11 (a conditionally phrased tension question is not an unowed part when reliance on accepted authority does not hold; C7-P03 depends on it). A-x5 and A-x6 touch every Q4d verdict.
- Next: `checker-p5-7.2-a` (launched) confirms or rejects the readings, the A-9 mapping and each fixture's verdict, then reports counts and pass/fail only.

## custodian-7.2-b repair pass (after the pre-run check NO-PASS; counts only)

- Rulings set 3 (`d0a936ec…2691`, commit `ebbbcb2`) verified at 16:57:41Z. 133 fixtures, none pending, none removed: C1A 6/6, C1B 6/6, C1U 9/6, C2 12/8, C5i 6/6, C5ii 6/1 (+6 label-only), C5-N 3, C6 8/7, C7 16/15.
- Repairs: A-x11 label and a new twin; the qualifier list narrowed to the §11.3 list; trace facts added across C2 and C6; mapping to one item per unowed part, Q4d prefix-scoped, Q4b claim integrity only; evaluator view with neutral ids separated from the custodian-held labels; bad twins rewritten to defeat length and token shortcuts (best shortcut accuracy 0.58 to 0.75 against chance 0.50 to 0.60; C2 twins are not length-matched).
- Digests: FREEZE.sha256 `94e4ec8e0c224bcee68298805a427785c2e004df516e0b2facd7a7a4ca06d312` (152 entries); ATTESTATION `b86fa83b127a1fd675168754cd83fb187e666c70ae10a5cd86a5077069e01a2d`; LABELS.json `07f493d1…16ed2`; MANIFEST.json `4280bbdb…bb7`. Unfrozen.
- Open: the checker re-checks the repairs and the provisional readings A-x2, A-x3, A-x4, A-x6, A-x8 and the mapping. A-x7 is accepted as a stated limitation (fourth ruling).

## Pre-run check, delta re-check (checker-p5-7.2-a): PASS for freeze readiness (counts only)

- Verified: FREEZE.sha256 `94e4ec8e…d312` (152/152 OK, ACCESS-LOG excluded), ATTESTATION `b86fa83b…a2d`, FREEZE-GATE unfrozen, modes 0700/0600, rulings at `ebbbcb2` (`d0a936ec…691a`, the version the custodian used) and at HEAD `200a2b8` (`d32e273b…23d4`, adds the A-x7 limitation; no fixture depends on it). The store's LABELS and MANIFEST cite the earlier rulings digest.
- Blind verdicts on all 133 evaluator views agreed with the custodian's labels (133/133, none disputed). No fixture ids, placeholders, twin or verdict markers in the evaluator views. Separability: C1A 0.67, C1B 0.67, C1U 0.71, C2 0.79 (the null statement itself, the claim under test), C6 0.73, against chance 0.50 to 0.58.
- Confirmed: A-x2, A-x3, A-x4, A-x6, A-x8 and the A-9 mapping; A-x1, A-x5, A-x11 and A-x7 as ruled.
- For the campaign: give the evaluator only `calibration/evaluator-view/`; `tools/build_views.py` holds the id salt and `labels/` the answers. The view shows `non_owed`, which is acceptable. A delegate slot that owes zero parts makes h4 report EXPOSURE for the whole of Q2; the builder now treats unequal or zero-part delegate episodes as an INTEGRITY finding (the development corpus has 12 delegate episodes of unequal size, 47 parts, and the regression test asserts that finding).
- The operator sets the freeze gate after the candidate is frozen. The store is not frozen.

## custodian-7.2-b P3b corpus report (counts only; the analyst has not opened the store)

- All five stages of the work order are complete in `~/ssdp72b-fixture-custody`; unfrozen. The custodian could not report per stage (a subagent hands back once); the per-stage counts and check output are in its `operator/STAGE-REPORTS.md` and ATTESTATION entries 4 to 8.
- 179 episodes; `check-corpus` PASS (179 episodes, delegate 12, non-owed 86). Main: 12 delegate episodes (one route, exactly 4 owed parts each, each also carrying 4 unowed-part evidence items) and 104 duty episodes (86 non-owed, 18 owed). Routing 19 episodes (3 replicates), versioning 8 (3), burden 9, burden-add 4, sentinels 4, sentinels-add 4, unversioned 9, unversioned-add 6. The optional `r2` and `ordinary` panels and the human-trial banks were not produced.
- Reported exposure (main panel): Q2a 48 owed parts, Q2b 48 unowed-part items, Q3 139 opportunities in 100 episodes with every family at least 6, Q4a 44 critical items, Q4b 116, Q4c 116, Q4d 86 non-owed runs per arm; 707 scoring items, 125 fixtures.
- C(b) set: 40 items (Q4b 17, Q4d 13, Q3 10), 19 known failures, labels held by the custodian (ruling A-x9). Best single-token accuracy 0.80 (Q3, 10 items), 0.77 (Q4d), 0.71 (Q4b); length ruled out.
- Digests: FREEZE.sha256 `a0aae583bc0eb1660f36b0e199fed086cfdf7ca2b23f0b03e9f205dcf7118ac8`; ATTESTATION `0ae17020d84984ddaf4fc4aa113bcf5eb18edcc57776de7cf4724ac45a151e4f`; IDENTITIES `54992633…734a`; gate map `afd29f49aacec81328feda7f03e977a98098a9c7f81e7716c9eb23daacc5107b`; slot flags `9126fbbeded72c1d9ec55057dafcd5d7c3a7f98a4753ec9d5dc8f0db6c1f5716`; frozen rubric `252f4a8d…6386`; CB-SET `c9cfaed5…8b51`.
- Disclosed: it read `ssdp70/eval/stub_tools/mediator.py` (outside the `eval/*.py` allowance); the routing, versioning, burden, sentinel and unversioned panels are imported from the accepted 6.6 sources and wired to the 7.0 harness, with probe solutions it wrote for the provider-free oracle probes.
- UNDETERMINED/open: P-1 (the gate-map shape was not checked against the builder, which was off its read list), P-2 (qualifier presence is detected by text patterns; a present part whose pattern does not match goes to the evaluator as unresolved, so the evaluator decides A-5 in those cases), P-3 (r2, ordinary, human-trial not produced). The "8 version cases" are the 6.6 version-regression run counts (T6 x4, T5 x2, T4 x2), the custodian's reading. The slot-flags file format is a flat map, undocumented.
- Next: `checker-p5-7.2-b` (launched) recounts exposure, checks freshness and independence, re-runs the provider-free oracle probes, confirms the gate map against the builder end to end on a synthetic run tree, builds the plan in a scratch directory and judges the C(b) set blind.

## custodian-7.2-b corpus repair pass (after the corpus pre-run check NO-PASS; counts only)

- Interrupted by a provider rate limit (HTTP 429) after check-corpus passed; resumed, inspected the store, re-verified and rebuilt the stale derived files (attestation entry 9). Rulings fifth set (`8437364f…c9a`, commit `beab304`) verified; it also read `build_campaign_record.py` and `h4.py` read-only (newly permitted).
- 185 episodes; check-corpus PASS. Main 122 (14 delegate episodes, 90 non-owed, all scored); routing 19 (57 runs per arm), versioning 8 (24), burden 9, burden-add 4, sentinels 4, sentinels-add 4, unversioned 9, unversioned-add 6. 747 scoring items, 131 fixtures.
- Exposure: Q2a 56 owed parts in 14 episodes (one route, 4 each), Q2b 56 unowed-part items, Q3 147 opportunities in 104 episodes (finding 33, null 18, variants 8, tension 28, choices 34, delegated 14, o1 12), Q4a 53 critical items, Q4b 122, Q4c 122, Q4d 90 non-owed runs per arm.
- Probes: 503 cases and 903 item checks pass; 359 of 372 binding items probed two-sided (the other 13 are `burden_record` items with no fail branch). Gate map tested through the builder on 31 synthetic runs (12 episodes, every panel kind): exit 0, no findings.
- C(b) set: 40 items (Q4b 13, Q4d 9, Q3 14, version-strict advisory 2, sentinel advisory 2), 20 known failures; the designated 10 scored failures are Q3 4, Q4b 3, Q4d 3 (ids in the custodian's report; hashed as SENSITIVITY-SET). Best single-feature accuracy: Q3 length 0.64 token 0.79 (chance 0.50), Q4b 0.62 and 0.69 (0.54), Q4d 0.78 and 0.78 (0.56).
- Hygiene: all files 0600, directories 0700, no `__pycache__`, `CUSTODY-CANARIES.json` with 371 canaries, Q4c count stated.
- Digests: FREEZE.sha256 `0ea0ca72df7e9e835960617d06b8a7ba130f99505db7b9a87274cb5c49ace7bd`; ATTESTATION `d8f31aa169d194688e18313c76f1a9e3c7ee942fa09db9e83998be81abec6c23`; IDENTITIES `88b4e8a09e8f0bcf5d97f6c4f2e1d833698b45bb793204360c44a58758a5cf01`; STORE-MANIFEST `e46903fb…490a`; gate map `2eaabe78…9115`; slot flags `f635b7f2…85a7`; rubric `c4cedcd2…4a25`; CB-SET `7584c47a…310d`; SENSITIVITY-SET `ed0edfdb…fafe1`; canaries `d89304ce…ba09`; expected scoring items `972adf14…f4ac5`.
- Open for the checker: the single-token and length separability on the small C(b) gate sets (Q4d length 0.78 is above the earlier 0.69).
