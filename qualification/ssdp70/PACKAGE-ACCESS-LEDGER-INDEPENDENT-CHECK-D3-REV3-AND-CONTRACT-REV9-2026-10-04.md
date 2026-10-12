# Independent check: D3 package-access ledger decision revision 3 and contract revision 9

- Reviewer: an independent context. I did not author the bytes under review or any earlier review of them. I read no `/tmp/SSDP70-*`/`ssdp70-*` file and no memory directory. All authority was rebuilt from repository bytes.
- Governing SSDP version: **6.6.0**. Protocol 7.0 is NON-QUALIFIED; `PROTOCOL-RELEASE-STATE.yaml` gives accepted_current 6.6.0.
- Subject: commit `8d04088c450ccca0de2eabb2ac6f3185e54f2ffa`, tree `bd59d117a655755df92d9c22991978487ba1a111`.
  - HEAD equals the subject.
  - `git archive` of the subject reproduces the tree hash.
  - The code is identical to parent `8be024a`, which differs only in four documents.
  - Tracked working-tree files for the reviewed paths equal HEAD.
  - The eight untracked files are out of scope and were not opened.
- Method: the software-design Review/Challenge contract. Parent semantics were rebuilt from the contract, the consolidated workplan and the shipped `dist/skills`. Falsification probes ran in a scratch area. The repository was not modified.

## Reviewed bytes (SHA-256 of the committed blobs at 8d04088)

| File | SHA-256 |
|---|---|
| qualification/ssdp70/D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION-2026-10-04.md | 26376d59bd37e968519721f1a3bf5ca8a1bc89b14cc5915413bb5f1287c77183 |
| qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md | f7deafe0c0cb8c83bcc0e0df112b590c45496a64732d4295a09fd55783d5753f |
| qualification/ssdp70/PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md | a5eec3a9319f4be605672c05eee1d929eb6f645774322aca68b7a73d87e53ddd |
| workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md | 16348ada13c94a0fbfdac80db9d323c9e3e4b185e57117c9736f5ff57fc52756 |
| qualification/ssdp70/eval/package_ledger.py | 71cb1c8f8e0ee64a3ff0b3363d035e20bbf07d8f46c347f2a9473d9371669e4b |
| qualification/ssdp70/eval/harness70.py | b58d8637442e17834f84310dfba9e98c501b500c6354720e787e22df2709989a |
| qualification/ssdp70/eval/core70.py | e7545a83d9ad802f39c997fc5eb2462d1f767aa8bf9a365e0bb2d7336af19215 |
| qualification/ssdp70/eval/adapters/omp.py | dfc2b1ae6d886eb8b08da04bd29f72d1695be19fdca12d42ad4dce24dfc405ac |
| qualification/ssdp70/eval/batch_assess70.py | b477eea615350b7497fe2d7b7476298e02281166922d6e9a94ba57ba3fdf4756 |
| qualification/ssdp70/eval/test_package_ledger.py | 6a4ce91b351f8defc2a14e94c929f2756966ab6e2c4ca23eda910ac14eddb8be |
| qualification/ssdp70/eval/test_activation_accounting.py | 184c35fca53df240f8bc360646fde4558466b7d6fd06e36ab7ef0b93d35f80c3 |
| qualification/ssdp70/eval/test_batch_cli.py | 4f206e79340e1e6c7e11c7df166d50491a02faf06adcc1fd5a8b61c767902e20 |

**Common-mode dependencies that limit independence.**
- The real-OMP tests and my timing probes share the authors' stand-in provider, `omp_rig`, the frozen OMP build and the host kernel.
- My probes call the committed `account()` and reuse the authors' unit-test helpers (`overlap_ledger`, `event`).
- My timing measurements come from one host, using the stand-in provider. A real provider was not exercised.
- I used the authors' own test oracles for the real-OMP path. I did not write an independent real-OMP oracle.

## Serious Challenge

**None** against D1/D2 or accepted D3. The defects below sit inside the revision under review, and each has a bounded repair.

One item needs the owner's explicit reconciliation, but I do not raise it as a Serious Challenge:
- The workplan's "Trusted runtime-observation contract" makes the provider-control/observation principal "the only approved independent observation boundary for the missing fields".
- The D3 decision adds a second observation boundary: the supervisor's kernel ledger.
- I read the "missing fields" list (build, catalog, MCP and runtime surface) as not covering subject consumption, so no direct conflict follows.
- However, D3 lists that bullet as a parent without reconciling the word "only", and the workplan marker annotates only the Root-selection bullet. See W-2.

## Blockers, by earliest owner

### D3 (decision revision 3)

**D3-1: Owner-read access-bound timing errs in the unsafe direction, and items 5 and 6 contradict each other.**
- Item 5 says clock or drain skew "cannot change counted bytes or owner sequences".
- Item 6 says "a late drain stamp can only move the bound later by one turn".
- These statements contradict each other. Item 6 is the true one.
- Ledger stamps are drain times, never earlier than the event. The computed access bound is therefore the *latest* turn consistent with the open, never the earliest.
- For a zero-tolerance "read before R2" floor, that is the non-conservative direction. A pre-R2 open drained after the next request's stamp is mapped to the next turn's result events. If R2 is a model action in that next turn, the action's start sequence precedes those result sequences, so the read is scored *after* R2.
- The "one turn" limit is asserted, but no mechanism bounds drain latency.

Evidence I executed:
- **Probe** (`probes/probe_bound.py`, committed `account()`):
  - With the same `wc -l owner` open at 2400, prompt drain gives earliest owner sequence 4, which is before the R2 step at 6.
  - The same open stamped at 2550, after the request-1 stamp of 2500, gives sequence 6.
  - `owner_read_exact` stays True in both cases, so nothing flags it.
- **Real margin:** across 47 post-request-0 package opens in 30 scratch real-OMP runs, the gap from the drain stamp to the next observer request stamp was 6.06–22.6 ms (minimum 6.06 ms, owner minimum 6.75 ms).
- **Watcher lag** (`probes/probe_lag.py`, committed `LedgerWatcher`, 300 opens):
  - Idle: median 0.013 ms, max 0.032 ms.
  - With one CPU-bound Python thread in the same process (GIL contention): median 5.2 ms, p99 31 ms.
  - Under supervisor-process contention the lag therefore reaches the real margin and can exceed it.

Item 6 itself calls same-turn tie-breaking "conservative for the zero-tolerance floor", but the cross-turn rule is not conservative.

Required repair, mechanism delegated:
- Either make the bound conservative (map to the earliest turn consistent with a recorded lag bound, and classify a request stamp inside that window as ambiguous R2 timing),
- or obtain a mechanical ordering, for example a supervisor-owned sentinel event in the same inotify queue at each request.
- Then fix item 5's text and add a timing-stress form to the item 8 rehearsal.

**D3-2: The N-2 repair is incomplete — the rehearsal gate covers only the owner question and the candidate package.**
- Item 8 derives the threshold only from the owner aggregation rule, through "the shipped package shape" (singular).
- The T1/T7/T8 burden metric "applies identically to the 6.5, 6.6 and 7.0 arms", and each arm ships a different package shape:
  - 7.0 candidate: 238 files, 63 distinct, 38 twin groups, 213 twinned. I verified this matches the D3 text.
  - 6.6 public source `22f4bdba`: 212 / 62 / 37 / 187.
  - 6.5 `7f7b5e24`: 198 / 60 / 35 / 173.
- In the realized aggregation, any inexact burden run (null `active_ssdp_bytes` or `owner_read_sequences`) makes the whole `fixed_cost`/`active_material` part UNRESOLVED (`batch_assess70.quantitative_part`). So the byte question has the same "any run" aggregation, across up to 7 pairs × 3 arms on T7.
- The gate can therefore be "met" while burden remains infeasible. This fails closed, but the gate exists precisely to bind feasibility.

Required repair:
- Rehearse each arm's package shape.
- Derive the threshold for both questions (`exact` for burden, `owner_read_exact` for owner) from their campaign aggregation rules.

**D3-3: The decision suppresses positive owner evidence.**
- Item 4a nulls `owner_read_sequences` unless `owner_read_exact`.
- A native read event or a supply event that shows an owner read before R2 is sound positive evidence whatever happens to other files. Nulling it turns a definite zero-tolerance FAIL into UNRESOLVED.
- This also changes routing. The workplan §0.1 item 7 reopen trigger fires on "a retained false-activation floor failure", not on UNRESOLVED.
- Exactness is needed only for *negative* conclusions. The contract's own "No ledger" bullet ("no negative owner-read conclusion is published") points the same way.
- D4 realizes this suppression: `harness70.py` sets `owner_read_sequences` to None unless `owner_observation_exact`.
- Repair: positives survive inexactness; negatives require exactness. Contract item 13 must say the same (C-3).

Non-blocking D3 notes:
- **D3-n1, unstated premise.** The independence of `owner_read_exact` from "unrelated" unexplained files assumes no non-owner file carries owner material. I verified this holds for the shipped 7.0 package: 0 of 242 owner lines of 48 bytes or more appear in any non-owner file. Record it as an assumption and a reopen trigger.
- **D3-n2, over-count is not always safe.** The residual says path-linkage over-count "never under-counts". Over-count is conservative on the candidate arm but inflates the 6.5/6.6 denominators of the 2.0× and median+bounds. Rare forms (for example `wc -l B; cat A` with twins A/B) — state the direction honestly.
- **D3-n3, watch mechanism.** Item 2 says "per-inode marks". D4 sets directory watches, which report by parent dentry. They are equivalent here only because install is a fresh `copytree` exposed through one read-only bind, which means no hardlinks and `EXDEV`. State that this equivalence condition is a D4 premise.

### D4 (realization at 8be024a; not accepted, recorded for impact)

- **D4-1, acceptance boundary (l) is only partly met.** `adapters/omp.owner_reads` still matches by substring (`owner_name in target`), not by the basename rule. Today this only over-matches (conservative), but the "one rule" claim is not true for the native path.
- **D4-2, no `package_access` event yet.** There is no normalized event, no completeness-map entry for the ledger artifact, and no binding of the decision identity or the ledger digest (contract rev9 items 4, 5, 11 and 13). The accounting lives only in `summary.json`, and lacks several required payload fields: per-file size, sha, stamps and phase for every opened file, and the request stamps used. This is expected while rev9 is a draft, but it is a precondition for any admission.
- **D4-3, rehearsal gate not enforced.** No code requires a recorded rehearsal threshold before a qualification-purpose ledger run. That is left to the pre-run checker or admission. The contract assigns it there; the admission machinery must check it.
- **D4-4 (minor), claim gating keys off substrings.** The harness detects claims by substrings (`t1`/`t7`/`t8`/`burden`/`active-byte`/`owner`). A run with differently worded claims stays COMPLETE_ADMISSIBLE when inexact. Campaign aggregation still fails closed, via `owner_observation_complete` and the null checks in `quantitative_part`, so I found no path to PASS.

### Contract revision 9

- **C-1, wrong cross-references.** Item 13 "Owner-read time" cites "zero-tolerance floor, §3" and "(§3: unresolved and independently adjudicated)". The zero-tolerance owner false activation and the ambiguous-R2-timing clause are in **§4**; §3 contains neither. Amendment question 3 repeats the error.
- **C-2, the campaign-effect sentence is self-contradictory on replacement.**
  - It says the criterion "cannot be PASS while any qualification run is unresolved on it", while "a replacement never removes the original".
  - Read literally, that already forbids rescue, yet the sentence ends by saying it "does not decide that question".
  - Item 12's Blocking rule counts final states "after the replacements … §§4–5 … allow", which makes the interaction ambiguous.
  - Either state plainly that an original that is still unresolved keeps the criterion non-PASS until the stakeholder decides replacement semantics, or defer the whole sentence. As written, it partly decides while saying it does not.
- **C-3, positives are masked.** "Claim scope" makes any owner-read claim with `owner_read_exact` false INADMISSIBLE. This masks a definite pre-R2 owner read (see D3-3). The required rule is that positive owner-read evidence is scorable as FAIL while negative conclusions require exactness. This also conflicts with the "No ledger" bullet's narrower "no negative owner-read conclusion".
- **C-4, a §6 probe is in the wrong category.** "an owner copy opened before R2 and shown only later" is listed among known-broken probes "rejected". Its correct expected result is an *exact* observation whose owner-read sequence comes before R2, so the zero-tolerance owner false activation detects it (a FAIL of the probe-local criterion), not a rejection. A frozen integrity expectation written from this text would be wrong, or would accept an INADMISSIBLE result that hides a broken access bound.
- **C-5, change-control gaps.**
  - Item 13 has no "Record." pointer to `PROTOCOL-7.0-PACKAGE-ACCESS-LEDGER-CONTRACT-AMENDMENT-2026-10-04.md`. Item 12 has one for revision 8.
  - §8 "Status and change control" has no revision-9 entry and still says no independent check accepts revision 8, which is now stale.
  - Item 13 binds the D3 decision by "revision accepted by independent D3 acceptance". Item 11 binds "document and revision". Bind by commit and SHA-256: a revision label is not an immutable identity.
- **C-6, inherits D3-2.** The rehearsal-gate bullet inherits D3-2: one package shape, owner-only aggregation. It must cover the burden question and each arm's package.

Minor:
- Item 5 calls the folded ledger a "raw observable". It is a D4 reduction (fold per file and flags, with first/last/count) of the kernel stream. D3 item 7 argues the fold is sufficient for the oracles, and I agree: first/last suffice for phase, first-open suffices for owner time. The contract should name it a declared lossless-for-oracle reduction rather than "raw".

### Workplan marker

- **W-1, the marker bypasses §0.1 change control.** The overlay convention (§0.1: "each affected location carries a marker pointing here") is not followed. The new marker points to contract item 13. §0.1 records neither this governed change, its authority, its review status nor an overlay revision, and still names contract revision 8 as "the contract realization".
  - The marker's wording is present-tense operative ("is an admissible exposure"). Its effect is limited only indirectly, through item 13's binding to an accepted D3 revision.
  - Repair: a §0.1 entry (authority, revision, pending status) and a marker that points to it.
  - This answers amendment §3's open question: yes, §0.1 must record it.
- **W-2.** Reconcile, or mark, the "Trusted runtime-observation contract" bullet's word "only" (see the Serious Challenge note).

## Answers to amendment §5 questions

1. **Derivable and recomputable?**
   - In principle yes. The retained inputs are the ledger, the normalized events (`result_request_index`), the observer request stamps, the package recoverable by `dist_tree_sha256` (re-verified post-run), and the accounting-code digest.
   - Item 5's "artifact present but event absent" and "rows dropped" loopholes are closed by the text: the mapping is mandatory and the rows must reconcile.
   - Not yet realized in D4 (D4-2).
   - The fold must be declared a reduction (minor note above).
2. **Any PASS path when observation is not exact, or the threshold is unrecorded?**
   - None found, in the text or in the code. Campaign `owner_observation_complete` forces UNRESOLVED, and `quantitative_part` returns UNRESOLVED on null bytes or null owner sequences.
   - However, D3-1 is a path to a *false* PASS of the owner floor *with* observation labelled exact.
   - Code does not enforce the unrecorded-threshold rule (D4-3).
3. **Consistent with the zero-tolerance floor and the ambiguous-R2 clause?**
   - The floor is in §4, not §3 (C-1).
   - The rule is consistent in intent, but it inherits D3-1's non-conservative timing.
   - Item 13 partly restates the access-bound mechanism. The joint-change clause covers future D3 changes.
4. **Is "Campaign effect" faithful?**
   - It is faithful to §4's "on every trajectory" and to the item 7/12 fail-closed rules, and adds no new floor.
   - However, its replacement disclaimer is internally contradictory (C-2), and together with "Claim scope" it masks positive FAILs (C-3).
5. **Revision 8 bytes unchanged in effect?**
   - Yes. Item 12, the §3 table, §4, §5 and the §6 deterministic-entry text are unchanged.
   - Additions are scoped to ledger profiles. The no-ledger branch restates the existing guard.
   - Only §8 is stale (C-5).
   - **No threshold, floor, fixture or exposure minimum was added or changed.** I compared the full diff.

## Evidence

**Executed by me.** All runs used committed bytes: a `git archive` snapshot at tree bd59d117, and a scratch clone checked out at 8d04088 for root tests.
- `test_package_ledger` and `test_batch_cli`: 40 tests OK (Python 3.10.12).
- `test_activation_accounting` on the real frozen OMP: **14 tests OK in 440 s, none skipped.** This includes the N-1 real test, overlap/twin, entrypoint-only, owner-question scope, ledger-less guard and the campaign test.
  - Run under scratch `HOME=/tmp/rv9h`, with `runtime-closures` symlinked and `SSDP70_OMP_EXE=/home/samjin/.local/bin/omp`.
- Root `python -m unittest discover -s tests` in a scratch clone at the subject commit: 407 OK, 3 skipped.
  - An earlier run in a history-less snapshot had 2 failures. Both were caused by that environment (missing git history refs) and are inapplicable.
- `git diff --check 8be024a 8d04088`: clean.
- Package-shape, twin and owner-overlap analysis of `dist/skills` at 8d04088, and of the 6.6 and 6.5 public refs.
- Probes `probe_bound.py`, `probe_lag.py` and `gap.py`, under `/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/61e3dd0f-9d97-4f8d-8b42-9030c60ade6d/scratchpad/probes/`.

**Reused:** none of the authors' logs or counts were relied on.

The D3 record's "D4 realization facts" (for example 60 412 bytes) and the 933dcd3 check logs are bound to older trees (rev1 code). They are not applicable to rev3 and were not used.

**Missing — required, not run, and not counted as passing:**
- The item 8 rehearsal gate, for any arm.
- `test_omp_integration`.
- A real-provider run.
- inotify exhaustion and overflow under subject load, and unmount.
- A drain-lag stress run through the real adapter.
- A recomputation of a `package_access` event (it does not exist yet).
- The non-runtime eval set beyond the two modules above (the authors report 178).
- `test_stage_f_*_repairs`.

## Impact-closure state (open)

- **Batch aggregation:** fails closed for both questions. No false-PASS route was found other than the D3-1 timing defect.
- **D4 rework after acceptance:** the `package_access` event and completeness entry; item 11 bindings; positive-evidence retention; the conservative timing bound; native-path basename rule; enforcement of the rehearsal threshold at admission.
- **Workplan:** a §0.1 entry and the marker routing (W-1), and the "only" boundary wording (W-2).
- **Contract:** C-1 to C-6 and §8.
- **Evidence:** all development evidence must be re-bound to the accepted tree. The custody, frozen and activation-implementation directories were not touched.

## Verdicts

1. **D3 decision revision 3: NO-PASS.**
   - Blockers: D3-1 (non-conservative owner-read timing, unbounded drain lag, and the item 5/6 contradiction), D3-2 (rehearsal gate covers neither the byte question nor the comparator package shapes) and D3-3 (positive owner evidence suppressed).
   - The core architecture is sound within the accepted graph: supervisor kernel observation, supply by identity, per-question exactness and the fail-closed fallback. The D4 realization behaves as described on the real path for every case its tests cover.
2. **Contract revision 9 plus the workplan marker: NO-PASS.**
   - Blockers: C-1 (§3 should be §4), C-2 (replacement self-contradiction), C-3 (positive FAIL masked), C-4 (§6 probe category error), C-5 (no record pointer, §8 stale, revision-label binding), C-6 (inherits D3-2) and W-1 (marker outside §0.1 change control).
   - The single-owner structure (contract defers attribution rules to D3, with joint-change acceptance) is sound, and no new floor or threshold is introduced.

## For stakeholder decision

1. **Replacement semantics:** can a replacement run resolve an owner-inexact original? This must come before the rehearsal threshold, because the (1−p)^N derivation assumes no rescue.
2. **Rehearsal acceptance thresholds**, for both questions and per arm (6.5/6.6/7.0), from the planned N. Accept that honest non-literal path forms make runs inexact on these twin-heavy packages, or authorize the pre-registered turn-window fallback.
3. **Positive owner evidence:** confirm that a definite pre-R2 owner read is a FAIL even when the observation is otherwise inexact (C-3/D3-3). This changes routing to the reopen trigger.
4. **Workplan observation boundary:** confirm that the supervisor ledger is an admissible observation boundary alongside the provider-control observer (W-2), and record it in §0.1.
