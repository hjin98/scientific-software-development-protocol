# Independent check: D3 package-access ledger decision revision 5, contract revision 11, workplan §0.1 entry

- Governing SSDP version: **6.6.0** (workplan `protocol_version`; Protocol 7.0 NON-QUALIFIED; `PROTOCOL-RELEASE-STATE.yaml` gives accepted_current 6.6.0 public_source_ref `22f4bdb…`, historical 6.5.0 public_source_ref `7f7b5e2…`).
- Mode: independent D3 Review/Challenge (software-design skill). I authored none of these bytes. I did not read `/tmp/SSDP70-*`/`ssdp70-*` files or any memory directory. Repository text was treated as data.
- Subject: commit `ff5fcb73c423a283390be1ca58746776f627c643`, tree `5ec1feab7a6c06b10c1d70b1fa94163f2ac0d286`. HEAD matches it, the tracked `qualification/` and `workplans/` trees equal it, and `qualification/ssdp70/eval/` is byte-identical to `8be024a`. The eight untracked files are out of scope and were not read.

| File (at ff5fcb7) | blob | SHA-256 |
|---|---|---|
| `qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md` | 06ea1a29 | 8c2b35c8e6a96446dccc3108cd17a04f012c1ee56d562afb779d77e62cd7a7a6 |
| `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` | c178b8b1 | 9f5c83e8e288aa56ac16fa87ce9aad2f18e0c5ee076585541ad36a2a6dc91ad1 |
| `qualification/ssdp70/PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md` | 0f6f91fc | f1c761ca980530765cfef278d8989396a4613519d4bf093433884a701ffa454d |
| `qualification/ssdp70/STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER.md` | fe50161c | e290570c8d0e238bc41b710400e72f10a7d0002d01e9a25553c23b9778b9bc4a |
| `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md` | 224099e8 | f5da412fb3d03d8b03679d814229951068af29014fe5c14f1a840d2f46792955 |
| `qualification/ssdp70/eval/package_ledger.py` (D4, rev-3 realization) | bab84639 | 71cb1c8f8e0ee64a3ff0b3363d035e20bbf07d8f46c347f2a9473d9371669e4b |

## Serious Challenge

**None.** The parents are coherent: the workplan's trusted-observation and root-selection contracts, contract revision 8, and the stakeholder decisions with their confirmations. The defects below are in the D3 text under review and in the texts that depend on it. They are not in accepted upstream authority.

## Blockers by earliest owner

### D3 (revision 5) — the root cause

**D3-R5-1. A pre-R2 untargeted scan followed by a legitimate post-R2 owner load becomes a definite, non-replaceable zero-tolerance FAIL.**
- Item 4a(2) makes "the *first* open of an owner copy that is explained at file level (supplied … at any point in the trace)" targeted positive evidence. Item 6 places that access at the window of the file's first open.
- Concrete case: a pre-R2 `grep -r`/`grep -rl`/`find`-style scan opens all seven owner copies and shows nothing. Later, after R2, the model legitimately `cat`s its root's owner copy. That copy is now "explained", so its first open counts, and that first open is the scan. The window ends before R2, so the result is a definite FAIL. The run is never replaceable ("a positive owner-access observation before R2 is never replaced").
- This is exactly the trajectory shape of the R2 owner-load opportunities, where loading the owner after R2 is the desired behaviour. So the false FAIL lands on the runs the floor exists to reward.
- It contradicts:
  - the stakeholder confirmation item 2 ("an unshown, unnamed owner open … is UNRESOLVED and replaceable, not a FAIL");
  - D3's own residual ("untargeted owner opens … cannot produce a false FAIL");
  - acceptance boundary (q).
- Item 6 is internally inconsistent: "placement … is the candidate window of … its first open (a native event or a supply event is placed at its own sequence)".
- Contract §6's known-good probe ("an owner copy opened before R2 and shown only later … expected … window ends before R2 … fails") and D3 boundary (j) encode the same rule.
- Executed evidence: `probe/scan_then_load.py` uses the real kernel `LedgerWatcher` through a bwrap read-only bind with the production `account()`. The `grep -rl` and the later `cat` fold into one owner row (count 2, first_ns = scan time), and `owner_access` is placed at sequence 1, before the R2 event at sequence 2. Revision 5 explicitly keeps that first-open placement.
- Repair direction:
  - A supply-targeted or name-targeted access is placed at the open(s) inside the supplying or naming action's window, or at the supply event's own sequence.
  - Earlier opens of the same file that are not themselves targeted remain untargeted (UNRESOLVED).
  - If the deliberate case "`wc -l` via an unnamed path pre-R2, then `cat` post-R2" must stay a FAIL, that needs a stakeholder decision, because it conflicts with confirmation item 2.
  - Note: item 7's "fold is lossless for these oracles" (first/last bracket plus count per file and flags) does not hold for any per-open rule. The fold must keep per-window opens, which is bounded by turns × files.

**D3-R5-2. Owner content that reaches the model is not positive evidence unless it is attributable to one specific file.**
- Item 4a(2) requires file-level explanation by route (i), (ii) or (iii).
- In every shipped package the owner has seven byte-identical copies, so route (i) (distinctive) never applies to owner content. Route (iii) needs whole-file same-turn display.
- So `cd /opt/ssdp/skills/<root> && head -n 40 references/<owner>`, a relative-path `sed`/`grep -n`, or a copy-then-read from `/tmp` in a later turn all show owner content before R2, yet the result is only UNRESOLVED and replaceable.
- That narrows the stakeholder's confirmed definition ("Positive evidence is … supply of the owner content") and the principle "positive evidence is never suppressed".
- Executed evidence: `probe/partial_twin.py` (real kernel ledger, twin owner copies, production `account()`). 530 bytes / 10 owner lines reach the model, but the owner is not `supplied`, it is listed `unexplained`, `_names_path` is False for the relative path, and `contained_content` returns `('partial', False)`.
- The premise D3 already relies on makes the fix cheap. I verified it: no owner line of at least 48 bytes occurs in any non-owner file, 0 of 242, so whole-line owner runs identify the owner *class*. A run of whole owner lines at least the floor long in a tool result is owner supply and can be placed at its own sequence.
- Caveat for the premise wording: at sub-line granularity, 27 maximal shared runs of 48 to 117 bytes do occur in non-owner files. State the premise at whole-line granularity, which is what `_runs` uses.

**D3-R5-3. The "path named in a tool action's recorded input" test (item 4a(3)) is co-occurrence, not causation, and "named" is undefined.**
- inotify carries no pid, so any action in the window that names an owner path makes *any* owner open in that window targeted.
- Honest forms that name without opening, in the same turn as an untargeted scan, therefore yield a definite FAIL when the window is pre-R2: `ls -l <owner path>`, `test -f`, `echo`, a comment, or a `grep` pattern containing the path.
- Executed evidence: `probe/named_cooccur.py` shows `ls -l …; echo …` produce no owner open, while the scan opens it.
- The turn-ambiguity clause ("any candidate turn") widens the co-occurrence set.
- "Named" is not defined for relative paths, `./`, quoting/escaping, globs that match the path, variables, or basenames. The D4 matcher (`_names_path`: mount-prefixed or `<root>/…` package-relative, word-boundary) decides between false FAIL and the detection hole, yet it is not among the frozen decisive parameters of item 6.
- Required:
  - define "named" (or delegate it to a frozen, rehearsed D4 matcher);
  - declare the co-occurrence residual;
  - add the corresponding rehearsal forms to item 8: name-without-open plus scan, pattern-naming scan, relative-path partial owner read, and pre-R2 scan followed by post-R2 load.

### D3 conditions (fix in the same revision; individually not blocking)

- **D3-c1. Timing-loss scope.**
  - Say that clock divergence is measured against a fixed run baseline (realtime − monotonic offset) and that it taints every bracket after the step.
  - If divergence is checked only across the adjacent heartbeat pair, a backward `CLOCK_REALTIME` step makes later legitimate post-R2 opens appear to precede earlier request stamps (observer stamps are realtime only). Their windows then end too early, which manufactures a definite FAIL.
  - Better still, have the observer stamp `CLOCK_MONOTONIC` too.
- **D3-c2. Window edge cases.**
  - Window start is undefined when no request precedes the lower edge (straddling or pre-request opens).
  - Retried requests: a retry carrying the same conversation position gives an empty or inverted window. Say that retries share the original's position and that an empty window sits at that boundary.
  - Define "event time" as kernel event generation. The lower edge can lag the syscall by in-kernel preemption. That affects only the window start, never definite FAILs, but it can turn a targeted open into an untargeted one.
- **D3-c3. Owner-load hits.**
  - "Owner-load hits need `owner_load_exact`" (4a, and contract item 13) suppresses a demonstrated post-R2 supply hit whenever any other owner copy was opened unexplained. A pre-R2 or post-R2 package scan does exactly that, because it opens all seven copies.
  - `owner_load_exact` is needed only to conclude a *miss*. A hit needs demonstrated supply in the R2 interval.
- **D3-c4. Scope of the "no owner read" conclusion.** It requires "no untargeted owner open" with no time qualifier. An untargeted open whose window starts after R2 cannot be a false activation and should not leave the floor UNRESOLVED.
- **D3-c5. Ambiguous-timing positive evidence.**
  - State whether a targeted access whose window contains R2 is replaceable. As written it is positive evidence, so it is excluded from replacement and the floor stays UNRESOLVED pending adjudication.
  - Under timing loss, every legitimate post-R2 owner load in that run becomes this case. The gate must count it as non-replaceable.
- **D3-c6. Stale revision references.** Open item (ii) cites "contract revision 10 §1 item 13". Background-launched delayed reads named outside their window escape (3); either declare that as a residual or keep the stakeholder's unwindowed wording.
- **D3-c7. Recommended rehearsal forms.**
  - `PROTOCOL_VERSION` reads via non-literal paths. The 6-byte file is below the floor, so only (a)/(ii) explain it, and version lookup is an oracle on T1/T7/T8.
  - Request retries.

### Contract revision 11

- **C-R11-1 (inherits D3-R5-1).** The §6 known-good probe "an owner copy opened before R2 and shown only later, drained late … expected … window ends before R2 … fails" fixes the defective rule as an integrity expectation. §6 restates D3 outcomes (known-good/known-broken lists) outside item 13's "single owner" pointer. Either point these at D3 acceptance-boundary items or include §6 explicitly in the "joint change" sentence of item 13.
- **C-R11-2. T7 reading is undefined.**
  - D3 item 8's aggregation says "any inexact burden run leaves the fixed-cost part unresolved". Originals are never removed, and T7 has no replacement. So adding pairs can never resolve an inexact T7 run, yet item 13 says it is "handled by … pair-addition … non-PASS if it remains unresolved at seven pairs".
  - State how an inexact T7 run enters the median: for example, as an unknown value with a worst-case or interval median that resolves only if the bound holds for every value. Otherwise the 0.8 gate target for "T7 with its pair-addition rule" cannot be instantiated without a post-hoc checker choice.
  - Using inexactness as a new pair-addition trigger is also a change in effect that §8 does not list. §8 lists one.
- **C-R11-3. Stale or inconsistent cross-references in the amendment record.**
  - Front matter `status` says "D3 … decision revision 4".
  - The §2 table names an item 13 "owner-access time" bullet that no longer exists.
  - The §2 "Workplan markers" row lists two markers and says "No other workplan text … changed", but revision 11 adds a third marker (§11.5) and a §0.1 sentence.
  - §7 says "D4 realization of revision 4".
  - §3 (revision 9 dispositions) still contains the superseded "any post-request owner open is access" text. That is acceptable only as history, and should be labelled superseded by §3a.

### Workplan §0.1 entry and markers

- **W-R11-1.** The entry's Records clause still binds "the D3 decision … (revision 4, pending independent acceptance)". It should say revision 5. Item 11 binds by commit and SHA, but the authority entry must not name a superseded revision.
- **W-R11-2. Marker at the wrong site.** The read→access change is marked at the §11.5 reuse site (line 916) and at the §0.1 entry's pointer (§0.1 item 5, §11.5). The *defining* text, §11.4 measures ("owner false activations, under this single definition, which §11.5 reuses: … any read of the new owner before the trajectory's R2 point", line 907), carries no marker. That violates the overlay convention that each affected location carries a marker.
- The root-selection and trusted-runtime-observation markers are sound. They are consistent with stakeholder decision 4 and add no edge.
- The stakeholder record's "Pending acceptance" paragraph also still names "D3 revision 4, contract revision 10" (record defect, same class).

## Answers to amendment §6 questions

1. **Windows.** The upper edge is sound: kernel queue order with heartbeat-after-write stamps, so late drain and contention only widen. Definite FAIL ("window ends before R2") is sound for the access whose time is being placed: late drain, in-flight or background opens, opens after the last request, auxiliary requests (excluded as delimiters, which is conservative), and parallel calls (same window, so ambiguous). It is not sound for which open is placed (D3-R5-1). Gaps: wall-clock step scope (D3-c1); retries and undefined starts (D3-c2).
2. **Targeted versus untargeted.**
   - It catches a pre-R2 read by absolute `cat`/`head`/`wc` and by relative whole-file `cat` (route iii).
   - It misses relative or partial owner reads that show content (D3-R5-2).
   - It false-FAILs honest scan-then-load (D3-R5-1) and name-plus-scan co-occurrence (D3-R5-3).
   - Honest scans *alone* stay UNRESOLVED as intended.
   - The detection hole is bounded only by the per-case cap (two reruns), disclosure and the disparity bound. There is no campaign-wide cap on replaced owner-unresolved runs; that is stakeholder-adopted.
3. **Route (iii).** It is free of the shared-block failure on the shipped shapes. I checked all three arms: no distinct file of at least 48 bytes is wholly contained in another distinct file. Its only lenience is identical twins, which the model wholly received (declared over-count residual).
4. **Recomputability.** The `package_access` event is recomputable from the ledger artifact (including heartbeats), the normalized events (action inputs, result sequences, request indexes) and the package. The completeness-map clause is adequate. Classifying a window as definite or ambiguous needs the custodian's R2 key, so it correctly sits in the scorer, not in the event.
5. **Paths to PASS without exact observation.** No path to PASS without exact observation was found. Burden needs `exact`; no-read needs `owner_access_exact` and no untargeted open; replacements must be exact; an unrecorded target leaves the gate unmet. "Campaign effect" is a faithful clarification of item 7.
   - Minor: the "No ledger" bullet makes owner claims INADMISSIBLE without saying that native pre-R2 `resource_access` positive evidence still scores. It is non-PASS either way.
6. **Overlay convention and revision 8.** The workplan entry is consistent with the overlay convention except W-R11-1 and W-R11-2. Revision 8 bytes, checked with `git diff 15a2297 ff5fcb7`: §§2–5, §7, item 12 (activation strata, family rule, criterion map) and all thresholds are byte-unchanged. The edits are front matter, item 4 (pointer), item 5 (addition), item 11 (addition), the new item 13, the §6 paragraph and §8. Changes in effect are confined to ledger profiles. The read→access change is declared in item 13, §8, workplan §0.1 and the §11.5 marker, but not at contract §4/§5, where the floor is stated (recommend a pointer), or at workplan §11.4 (W-R11-2).
7. **Replacement and R-op values.** Replacement is sound in its guards: original retained, positive evidence never replaced, exactness required, overflow cause disclosed, fail-closed without a frozen bound. However:
   - **Selection effect on burden.** Inexactness (scans, hidden reads) correlates with higher byte consumption, so replacing inexact burden runs biases medians low for the arm with more inexact runs. The disparity rule leaves only "the affected comparative claim" UNRESOLVED. State that this includes the 2.0×6.5 and class-iii burden comparisons, or report replaced-original sensitivity.
   - The T7 reading is undefined (C-R11-2).
   - The 0.8 target now covers burden routes.
   - The two R-op values add no outcome threshold that the contract forbids before exposure.

## Evidence

- **Executed by me in my own scratch area (`/tmp/claude-1000/rv/`); no repository modification:**
  - `python3 -m unittest test_package_ledger test_batch_cli`: 40 tests OK. Applicability: revision-3 behaviour only. It is not evidence for revisions 4 or 5.
  - `probe/scan_then_load.py`: real inotify plus bwrap, production `account()` (D3-R5-1).
  - `probe/partial_twin.py` (D3-R5-2).
  - `probe/named_cooccur.py` (D3-R5-3).
  - Package-shape recomputation from `git archive` of `dist/skills` at ff5fcb7 (7.0.0), 22f4bdb (6.6 public) and 7f7b5e2 (6.5 public): **238/63/38/213, 212/62/37/187, 198/60/35/173**, matching the D3 figures.
  - Owner premise: 7 identical copies, 45,958 B, 242 lines of at least 48 B, 0 in non-owner files. Holds at line granularity only.
  - Whole-file containment check on all three arms: none.
  - Rule-of-three arithmetic: about 1,500 runs gives 0.2%, correct.
  - Section and item citation check of D3, contract, amendment and workplan.
- **Reused, not re-verified:** D3's real-OMP observations (`grep -rl` opening 238 files; 16,385-event overflow; pre-request catalog opens; the 60,412 B realization). These are development evidence only.
- **Missing:**
  - No realization of revision 4 or 5 exists (heartbeats, windows, targeted classification, `package_access` event, rehearsal). Nothing in revisions 4/5 is realized or tested.
  - No real-OMP run was executed by me. It was not needed for these text verdicts: every finding is a consequence of the decision text plus kernel semantics demonstrated on the real watcher.
  - Compaction and long-session behaviour remain untested (declared by D3).

## Impact-closure state

Open. D3-R5-1 to D3-R5-3 require a D3 revision 6. Contract item 13 binds D3 by commit and SHA, and §6 restates its outcomes, so the contract must be revised jointly (C-R11-1 to C-R11-3). The workplan needs two text fixes. D4 work stays blocked behind acceptance; the D4 list in the revision 5 note must add per-window open retention, owner-class supply, and the named-path matcher as a frozen parameter.

## Verdicts

1. **D3 decision revision 5: NO-PASS.** Blockers D3-R5-1 (a false definite FAIL on scan then legitimate load; contradicts the stakeholder confirmation), D3-R5-2 (shown owner content is not positive evidence) and D3-R5-3 (co-occurrence naming test is undefined and unrehearsed). Plus conditions D3-c1 to D3-c7.
2. **Contract revision 11: NO-PASS.** C-R11-1 (§6 encodes D3-R5-1 and restates D3), C-R11-2 (T7 inexact-run reading undefined; extra change in effect not declared) and C-R11-3 (stale amendment cross-references). Revision 8's criteria, family rule and strata are unchanged, and no forbidden threshold was added.
3. **Workplan §0.1 entry and markers: NO-PASS (text-only).** W-R11-1 (stale "revision 4") and W-R11-2 (no marker at the §11.4 single defining site). The observation-boundary reading and the root-selection and trusted-observation markers are sound.

## Recommend the stakeholder confirm

- Whether a pre-R2 *unnamed, unshown* open of an owner copy that is *later* shown after R2 is a FAIL (revision 5 says yes, which contradicts confirmation item 2) or UNRESOLVED. I recommend UNRESOLVED, with targeting placed at the supplying or naming action's window.
- That "supply of the owner content" includes partial owner content identified at owner-class level (whole owner lines, at least the floor), placed at its supply sequence.
- That a naming-only co-occurrence (path in `ls`/`echo`/pattern/comment) is acceptable as targeted, or that "named" is restricted to path arguments under a frozen matcher.
- How inexact T7 runs enter the median under pair addition.
- That the disparity bound applies to burden comparisons, and who sets its numeric value.
- Whether a campaign-wide cap on replaced owner-unresolved runs is wanted beyond the per-case cap.

## Independence limits

I share a model family with the authoring and prior reviewing contexts (Claude; author co-signed Sonnet 5.5; I am Opus 5.5), which is a common-mode reasoning dependency. My probes reuse the production `package_ledger` watcher, `account()` and test helpers (`make_tree`, `sandbox_read`, `event`), so a defect shared by those helpers and my probes would be common-mode. The kernel ordering and coalescing claims rest on my understanding of Linux fsnotify; I did not verify them against kernel source here.
