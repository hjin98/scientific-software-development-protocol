# Independent D3 review: package-access ledger decision (SSDP 7.0 Stage F, OMP slice)

Reviewer mode: `/software-design` independent Review. The reviewer did not write the decision or the implementation.
Governing SSDP version: **6.6.0**. Protocol 7.0 is **NON-QUALIFIED** (resolved from root `PROTOCOL-RELEASE-STATE.yaml`: accepted_current 6.6.0, public_source_ref `22f4bdba…`, recovery_ref `38466676…`; not guessed).
Report time: 2026-10-04T19:43Z. Report only; no repository file, custody path, frozen artifact or historical evidence was modified (see §10).

## 0. Subject identity (read this first)

- The subject commit `69fcdb2` is **no longer on the branch**. The reflog shows `HEAD@{0}: commit (amend)` created `933dcd3`. Both commits have the identical tree `0a5ce6b3…`, so the code and records reviewed are byte-identical. `933dcd3` is branch HEAD. A reviewer record should cite `933dcd3` (tree `0a5ce6b3…`), mentioning `69fcdb2` as the pre-amend id.
- Re-check of `git status`: exactly the eight unrelated untracked files named in the task, unchanged by this review. Tracked tree equals HEAD.
- All code under review was exercised from a `git archive 69fcdb2` extraction in the session scratchpad (outside the repository), with `HOME` redirected into the scratchpad so no new directory was created under `~/ssdp70-omp-stagef`. The immutable runtime-closure directory was exposed to the scratch HOME by a symlink and only read.

## 1. Verdicts (summary)

| Item | Verdict |
|---|---|
| **D3 decision record** | **ACCEPT WITH CONDITIONS — not acceptable as written.** The topology and mechanism (supervisor-owned kernel observation, no new edge) are sound and survive falsification. Two material rules in the record are false or underdetermined on the real package: the supply-attribution rule (SC-1) and the "clock skew only stricter" statement (B-D3-2). Conditions C-1 … C-6 in §3. |
| **D4 conformance of the realization** | **NO-PASS as realized.** Two production-path blockers (B-D4-1 entrypoint-only runs inadmissible despite exact ledger; B-D4-2 cross-file content overlap yields false "exact" supply). Everything else in the mechanism, fail-closed handling, identity binding and batch changes conforms (details §5–§7). |
| C1 topology | **holds** |
| C2 ledger bounds opens; consumed only when its content is supplied | **fails as stated** (upper bound holds; the supply clause is provenance-free) |
| C3 request-0 cut is safe; skew only stricter | **partly holds / fails as stated** (the model-safety half holds; "only stricter" is falsified) |
| C4 subject cannot suppress/forge/influence; failures recorded and fail closed | **holds**, with a D4 resource finding (unbounded event retention) |
| C5 contract metric preserved; partial supply counts whole file once | **rule holds; realization fails under content overlap** (double counts byte-identical twins) |
| C6 ledger-less adapters keep previous behavior | **holds** (executed), but **no committed test covers it** |

## 2. SERIOUS CHALLENGE (to the pending D3 record as written)

Scope: the pending D3 text only. No accepted authority is contradicted: the baseline remains the consolidated-workplan text that makes burden claims claim-scoped inadmissible when OMP cannot expose consumption (workplan line 707). The decision is "pending independent D3 acceptance".

### SC-1. D3 §4 supply rule ("a file counts as consumed only when its content appears in model-visible tool-result text") is inadequate on the real package and contradicts the record's own acceptance boundary (b)

**Basis.** The rule matches *content*, not the *opened file*. The installed package (`dist/skills`, seven roots, 238 files) contains large amounts of byte-identical or overlapping content:
- The owner `references/scientific-inspectability-and-initiative.md` (45 958 B) is **byte-identical in all seven roots**. `contained_content` of any other root's copy against it is `exact` (42 ordered pairs, `exp1`).
- Each root `SKILL.md` inlines the shared kernel, so one root's `SKILL.md` output `partial`-matches that root's `references/abstraction-and-concretization.md`, every other root's `SKILL.md`, and every other root's copy of that reference (140 ordered pairs from `SKILL.md` alone).
- Any file shorter than the floor (the seven `PROTOCOL_VERSION` files, 6 B `7.0.0\n`) is explained by *any* output containing the string, e.g. `python 3.11; protocol 7.0.0 ok`.

**Concrete counterexamples, production path.** Real OMP 18.0.11 (`6054460b…`), real observer, harness, scorer, ledger; only the provider is the local stand-in. Claim `active-byte burden`; root `software-implementation`:

| Scenario (tool calls) | Result |
|---|---|
| P1: `bash cat <root>/SKILL.md`, then `bash wc -c <root>/references/abstraction-and-concretization.md` | `COMPLETE_ADMISSIBLE`, `resource_observation.exact = true`, `active_ssdp_bytes = 29 715` = 14 454 + **15 261** (the reference was only size-probed; no content shown) |
| P2: `cat software-design/<owner>`, then `wc -c software-implementation/<owner>` (declared-root owner) | `COMPLETE_ADMISSIBLE`, exact, `active_ssdp_bytes = 106 370` = 14 454 + 45 958 × **2** (identical twin counted twice) |

Decision acceptance boundary (b) says that content which cannot be shown supplied (`count/hash/grep/transform/wc -c`) must yield `INADMISSIBLE` "with the file named". P1 is exactly that case and yields the opposite. The existing real-path test avoids this only because it probes one file in isolation. The assertion "exact" is therefore false in a realistic sequence, the byte total is inflated, and the owner-read sequences for a file never shown are attributed to unrelated events (`account` ties `supplied[rel]["sequences"]` to any event whose text matches, with no ordering or tool-call linkage).

**Consequence.** `exact`/`active_ssdp_bytes`/`owner_read_sequences` (T1/T7/T8 burden, T7 mode, R2 owner-read scoring) can be silently wrong while labelled exact. A common offset in both arms moves the 2.0× ratio toward 1, so the error is not one-sided conservative.

**Discriminating evidence for resolution.** After the D3 amendment, P1 and P2 must yield `INADMISSIBLE` naming the probed file, and a read of the file itself (`cat`, `head`, `grep -n` returning ≥ floor distinctive bytes) must stay `exact`.

**Owner / route.** D3 (item 4 and acceptance boundary). D4 cannot choose the attribution rule silently because it defines what "consumed" means.

## 3. Blockers by earliest owner

### D3 (conditions for ACCEPT)

- **C-1 (SC-1).** Replace "content appears" by a supply-attribution rule bound to the opened file, for example: (i) a content block counts only if it is not contained in any *other* package file (distinctive against the whole tree), or the producing tool action's input names the file; (ii) byte-identical twin groups are a single equivalence class whose individual members cannot be told apart by content, so an open of a member is explained only by path-linked supply, otherwise not exact; (iii) sources shorter than the distinctiveness bound are explainable only by whole-output equality or path linkage; (iv) state whether supply must follow the open. Pick any rule that passes the discriminating evidence above; the mechanism is delegated to D4 once the property is fixed.
- **B-D3-2 / C-2. Falsified sentence in §5.** "Clock skew can only move an event into the stricter class" is false. See `exp5`: a model-driven `cat` of **another root's `SKILL.md`** after request 0, whose ledger stamp lands before the cut (wall-clock step back), is classified pre-request, "explained" with no supply, and **not counted** (`consumed_files = {}` although 16 538 B reached the model). Non-`SKILL.md` files under the same skew are classified stricter (as claimed). The ledger stamp is also the *drain* time (`time.time_ns()` after `os.read`), not the event time, and both clocks are `CLOCK_REALTIME` (observer `evidence70.py:48`). Amend: name the clock domain (system-wide monotonic for both, or event-order based), and require supply matching of *all* opened files independent of phase, with the phase deciding only the "unexplained" classification, so skew can never undercount.
- **C-3. Entrypoint-only exactness.** State explicitly that an exact ledger with delivery proof and no post-request-0 opens is an exact observation (bytes = delivered root `SKILL.md`). Item 4 says "files never opened are exactly not consumed" but the claim gate does not honour it (B-D4-1). State also how a post-request re-open of the already-delivered declared-root `SKILL.md` (e.g. `wc -c SKILL.md`, observed `INADMISSIBLE`/unexplained, `H4`) is to be treated (non-blocking over-strictness).
- **C-4. Authority integration.** The decision is a standalone record; `git diff 46ea4a0 69fcdb2 -- workplans` is empty. The workplan "Root-selection evidence contract" (line 707) still says burden claims are inadmissible "if the exact OMP build cannot expose that consumption". The decision silently widens "expose" to include supervisor kernel observation. On acceptance, annotate that bullet (the repository's own "[Affected by …]" pattern). Contract §1 item 4 says owner reads are scored "from complete `resource_access` identity/action records, never from a reduced/truncated summary", and items 5/11 bind a completeness map and a normalized-event-schema version. Ledger-derived consumption exists only in `summary.resource_observation.accounting`, **not** as normalized events and not in `normalization-map.json`. D3 must say how ledger-derived consumption enters the normalized stream (a derived `resource_access` event with source `supervisor-ledger+supply`, schema version bump, completeness accounting) or route a contract amendment through the contract's own change process. Add a pre-run-checker item (contract §6) for the ledger realization.
- **C-5. Scope of inexactness.** The decision speaks of claim-scoped inadmissibility, but `batch_assess70.py:320-322` (pre-existing aggregator) sets the campaign-level `owner_false_activation` part to `UNRESOLVED` if **any** run in the qualification scope has `resource_observation.exact is not True`. One honest `wc -c`, `grep -c`, `grep -rn … | head` or native `grep` over the package in *any* run voids the zero-tolerance owner floor for the whole campaign. For the owner question the ledger already knows precisely whether any owner copy was opened (exactness per question is available). Either define per-question exactness (owner-read absence depends only on opens of owner copies) or accept the campaign-wide consequence explicitly and gate it (below, §8). See F-3.
- **C-6. Provenance wording.** The Gap section says "A real OMP model obtained the T7 owner via `bash cat`". The counterexample runs (verified read-only: `…T171724Z…` is `COMPLETE_ADMISSIBLE`, 14 454 B, owner `[]`; `…T172146Z…` is `INADMISSIBLE` with the interim guard reason) used the real OMP runtime with a **scripted local stand-in provider**. It proves the observation gap, not model behaviour. Reword.

### D4 (conformance blockers; independent of the D3 wording)

- **B-D4-1. Entrypoint-only runs are inadmissible for burden claims although the ledger is exact.** `core70.validate_claim_observability` (`core70.py:1431-1437`) requires `package_reads` (native resource_access events) or ledger `supply` rows. A deterministic OMP run that reads nothing beyond the runtime-delivered `SKILL.md` has neither. Production-path probes with claim `active-byte burden`: `H0` (no tool calls), `H1` (`ls references`), `H6` (`find`), `H7` (`du -sh`) all give `exact = true`, `active_ssdp_bytes = 14 454`, `evidence_state = INADMISSIBLE`, reason "T1/T7/T8 burden claim has no successful exact SSDP-resource evidence". Contract §4 expects an "entrypoint-only mode" for T7 and the fixed-cost panels, and the decision says never-opened files are exactly not consumed. Fix: let an exact accounting with a verified root delivery satisfy the gate. This was pre-existing in the gate, but the commit reordered the gate and claims exact observation, so it is the realization's responsibility.
- **B-D4-2. Realization of attribution (P1, P2 above).** Fix after C-1. `test_package_ledger.py` fixtures are deliberately distinct (`OWNER`, `OTHER` share no 48-byte block), so no committed test can discriminate this. Add real-package overlap cases (the two table rows) to the real-path suite.

## 4. Non-blocking findings

- **F-1 unbounded retention (C4).** `LedgerWatcher` keeps every event row. A subject looping `open/read/close` produced 375 913 retained events and a **41.6 MB** ledger artifact from a single file (729 386 events with two files); overflow was detected correctly but memory and artifact size are subject-controlled. Collapse repeated rows per (file, flags) with first/last stamp and counts, and cap.
- **F-2 silent read errors.** `_drain_once` swallows every `OSError` and returns `False` (`package_ledger.py:103-104`), so an unexpected read error would end draining with no recorded loss (the established and non-overflow ledger would still be labelled exact). Record any error as ledger loss.
- **F-3 residual interaction (see §8).** Native `grep` over the package directory and `grep -r` open every file; `grep -rn … | head`, `grep -c`, `wc -c|-l`, `grep -l` leave opened files unexplained; error-status tool results (e.g. `cat A missing`, non-zero exit) are excluded from supply (`_result_texts` requires `status == result`) even though the model saw the content (stricter, conservative). All yield `INADMISSIBLE` by design, but see C-5.
- **F-4 partial matcher floor.** `PARTIAL_SUPPLY_MIN_BYTES = 48` is an uncalibrated absolute constant, not stated in the D3 record. It is not bypassable by the model, but it is the boundary that makes P1 work (shared kernel blocks exceed 48 B). Replace by a distinctiveness criterion (C-1).
- **F-5 T7 report-mixture.** At seven pairs with mixed modes `quantitative_part` returns `PASS, None`; the contract says "stop at seven and report mixture and median or unresolved uncertainty". The mixture is not reported. Not in scope of D3 but affects §4 conformance.
- **F-6 evidence logs.** The seven check logs are hash-bound by `ARTIFACTS-ADDENDUM-d3-ledger.sha256` (`sha256sum -c`: all OK), but they contain only dot output and counts. They do not bind the tested tree/commit, so they cannot by themselves show that the tested bytes equal `69fcdb2`.
- **F-7 amended subject.** Records and review text must cite the amended commit (see §0).

## 5. Claims C1–C6 (with what was tried)

- **C1 holds.** Data flow traced from `launch()` and `_bwrap_argv`: the watcher is an in-process thread in the supervisor, with `IN_*` marks on the host-side `paths["skills"]` (`private/omp-skills`, a fresh `copytree` copy; no shared inodes, no symlinks). `inotify_init1(O_CLOEXEC | O_NONBLOCK)`; the stop pipe is non-inheritable. No new principal, process, socket, proxy, credential carrier or edge. **Inherited-fd census inside the real subject sandbox** (`P3`, all `/proc/*/fd`): no `anon_inode:inotify`; only OMP's own eventpoll/eventfd/pipes/sockets. Kernel marks fire through the sandbox's read-only bind, `/proc/<pid>/root`, mmap (open fires), `cp`/read, and `O_PATH`+`/proc/self/fd` re-open; `O_PATH`-only produces no event but yields no content. Hard link: `EXDEV`/`EROFS`. A `+x` shebang script yields `open`. Not run: a pure ELF `execve` (kernel uses `IN_OPEN_EXEC`, which `WATCH_MASK` does not subscribe) and an exec of a `+x` text file by an interpreter-less route; the package has no executable files and no model-visible text could come from an ELF exec, so I assess it as immaterial for this claim.
- **C2 fails as stated.** See SC-1. The ledger as an upper bound on opened files holds (§6 completeness).
- **C3 partly holds.** Model safety half: request 0 is the first allowed POST (`observer70._forward_serial`: index counted only for POSTs to the single allowed path; the observer stamps `request` after the full body is read and before forwarding; model discovery GET is blocked and not an index; the transform specification asserts `auxiliary_post_requests == []`), so any open by the model has a stamp after the cut absent clock steps; an earlier-than-conversation cut can only be stricter. Falsified half: "only stricter" (B-D3-2, `exp5`).
- **C4 holds.** Subject cannot read, write or influence the ledger (no channel, caps dropped, RO bind, no fd). It can only create *volume* (F-1). All of the following were produced and produced `exact = false`: natural queue overflow by a hammering sandbox process (`overflow=True`); watch limit (simulated by failing `inotify_add_watch` with `ENOSPC` after 0/3/10 dirs: not established, no fd leak); create a file under the tree; rename a file; move a watched directory away and back; chmod; utime; append; write; unestablished (absent root). `tree_files` is taken before the watches (`start()` order verified); a file created later is flagged by its create/modify/close_write events. Not run: real exhaustion of `max_user_watches` (524 288) or `max_user_instances` (128); unmount (crafted flag in unit test only).
- **C5: rule holds, realization fails under overlap.** Whole-file-once counting matches the native `consumption`/harness rule (`consumed_files[path] = resource_bytes` for exact or partial) and `consumption`'s own `plain-substring` partial is weaker than the ledger's. Under overlap the bytes are inflated (P1, P2) and distinct-twin reads are double counted.
- **C6 holds (executed).** Removing the `package_access_ledger` hook from the real OMP adapter and replaying a `bash cat` of the owner (real runtime, stand-in provider): `INADMISSIBLE`, `exact=false`, reason "process execution lacks complete SSDP resource-read observation", `active_ssdp_bytes = null`, `owner_read_sequences = null`. No committed test covers this branch since the old guard test was replaced (decision boundary (e) is unevidenced in the suite).

## 6. Falsification attempts run (inputs → observed)

All scripts live in the session scratchpad (`exp1…exp7.py`, `lab.py`, `probe_review*.py`, `probe_c6.py`, `probe_out*.json`). Ledger work used the real `LedgerWatcher` and a real `bwrap` reader (sandbox usable without escalation); real-path work used the real OMP/observer/harness/scorer.

1. `exp1` content overlap over `dist/skills`: owner twins explain each other (42 pairs, exact); `SKILL.md` output partially/exactly explains 140 other-file opens (shared kernel, `PROTOCOL_VERSION`).
2. `exp2` + real-path P1/P2: false exact and double counting (§2).
3. `exp2` C3 (`PROTOCOL_VERSION` size probe explained by an unrelated string): exact.
4. `lab` topology: baseline `cat`/`wc -c`; mmap; O_PATH; O_PATH reopen; hard link; `/proc/<pid>/root`; exec; `cp` (§5 C1).
5. `exp3` natural overflow; single-file hammer for size (§5 C4, F-1).
6. `exp4` host-side mutations (create, rename, move dir, chmod, utime, append, write): all `exact=false` with the event named; package restored byte-identical and verified by `diff -r`.
7. `exp6` watch-limit simulation, no fd leak.
8. `exp5` cut/skew orderings: honest post-cut model read counted; same read with stamp before cut uncounted (lenient); non-SKILL file under skew stricter.
9. Real-path `H0…H10` (claim `active-byte burden`, root `software-implementation`):
   - `cat SKILL.md` + `wc -c` reference: exact (P1).
   - `ls references`, `find`, `du -sh`, no tool calls: ledger exact, claim gate rejects (B-D4-1).
   - `wc -c SKILL.md` (delivered root): inadmissible, root named unexplained.
   - `head -n 5` / `tail -n 20` of a reference: exact, whole file counted.
   - `grep -rn owner … | head -5`: inexact, two unshown files named. `grep -rl`: inexact, whole directory named.
   - `cat ref | wc -l`, `grep -c`: inexact.
10. Real-path C6 (hook removed): previous guard behavior (§5 C6).
11. Real-path fd census (§5 C1).
12. `account` cut cases (`exp5`) and ledger-only crafted cases (unit-level): reproduced `test_package_ledger.py` results.
13. Tests: `test_package_ledger` + `test_batch_cli` 18 OK. The two named real-path tests of `test_activation_accounting` re-run on the scratch copy: **2 tests, 6 subtests, OK, 80 s**. A broader scratch set (248 tests) showed 22 failures confined to `test_stage_f_integrity_repairs`/`test_stage_f_v4_repairs`, caused by the scratch copy lacking git history (`git show db94a2df…` unavailable); the same two modules re-run in the real checkout (`HOME` redirected): **92 tests OK**, tracked tree unchanged.
14. Discrimination of the new batch tests: running `test_batch_cli.T7Mode` against the parent's `batch_assess70.py` (`46ea4a0`) fails `test_same_mode_with_different_byte_values_is_not_mixed` (UNRESOLVED instead of PASS) and `test_unobserved_owner_mode_is_unresolved_not_inferred_from_bytes` — the tests discriminate the old behaviour.
15. Identity: `package_ledger.py` is in `execution_support_sha256()` (`adapters/omp.py:463-470`) and enforced by `profile_errors` (`:930`); `adapter-artifacts` (hence `package-access-ledger.json`) is in `EVIDENCE_INTEGRITY_ROOTS` (`core70.py:158`) and hashed when the run is `COMPLETE_ADMISSIBLE` (existing behaviour). No tracked frozen profile contains the old digest set (only the template is tracked). Cache keys change through the profile key, loudly, not silently.
16. Run-id pattern: no tracked manifest run id/episode id is rejected (very few exist in the repository; custodian Stage 7 corpus is not visible to this review). Pre-launch refusal: `main()` validates the manifest and rejects undeclared run directories before any thread pool/evaluator; the three test cases cover it. Other evaluator entry points (`omp_stage7_campaign`, evaluator admission) were not traced.

### Attempts not run

- Full `test_omp_integration` (54, ~1160 s), full `test_activation_accounting` (9, ~335 s), root suite (407) and the whole eval regression: not re-run; the implementer's logs are hash-bound but not tree-bound (F-6). The two ledger-relevant real-path tests were re-run.
- Real `max_user_watches`/`max_user_instances` exhaustion, `unmount`, pure-ELF `IN_OPEN_EXEC`: need privileges or contrived fixtures; see §5.
- Real-model behaviour (a Flash-class executor's tendency to use `grep -r`, `wc`, native `grep`): out of scope (no real provider); drives the open risk in §8.
- Owner naming for the accepted-6.5 comparator arm (the harness `OWNER` constant is the 6.6+ file): not traced; relevant to the T7 mode comparison.
- Wall-clock step/NTP behaviour on this host: not provoked; the skew attack was shown by constructing orderings on the production `account`.

## 7. Owner reads, claim gates, tests (specific questions)

- **Owner reads.** After the merge, `owner_read_sequences` is the union of native reads and *ledger-supplied* sequences for any root's `…/references/<owner>`. Supplied sequences are the events whose text matched, not events tied to the open, so a pre-R2 read of a twin or an overlap event is attributed to the owner open (SC-1). A *pre-request-0* open of the owner is unexplained (stricter), so a runtime pre-request owner open cannot become a model read. An owner read before R2 remains detectable when the owner content is shown by `cat` (sequence reported); when it is not shown it is `INADMISSIBLE`, not silently absent.
- **Claim gates.** Reorder verified: when accounting is inexact, no supply rows are passed to `validate_claim_observability`, and a second error is added for sensitive claims; `active_ssdp_bytes` and `owner_read_sequences` are both null whenever `resource_observation.exact` is false (single variable `opaque_package_access`). Verified in the P1/H-series (null bytes whenever exact false). The converse inconsistency is B-D4-1 (exact true, claim rejected).
- **Proxy-proof (DS-001).**
  - `AccountingFailsClosed` (unit): real owner is `package_ledger.account` against crafted tool-result events and distinct fixtures. These can stay green while the real owner is broken (P1/P2 prove it). Overflow, mutation, absence, unmount, pre-request non-entrypoint and native/ledger contradiction are covered at unit level only. Mutation and unestablished have one real-kernel test; natural overflow, cut skew, entrypoint-only and overlap have no committed test.
  - Real-path tests (`test_activation_accounting`): correct boundary (real OMP, observer, harness, scorer; only the provider stubbed), but their commands probe one file in isolation, which hides P1.
  - `test_batch_cli`: real owner is production `quantitative_part`/`main`; discriminating (§6.14).
  - Absent: a ledger-less-adapter test (C6) and a claim-gate test for entrypoint-only.

## 8. Interpretation of the residuals

- **No pid attribution.** Acceptable under the contract if supply attribution is path/inode-bound (C-1); as written it makes attribution content-only and wrong under overlap.
- **Transformed output deliberately inadmissible.** Acceptable as a conservative, claim-scoped rule *for the burden claim*. The rule must not be allowed to void unrelated floors (C-5). Run-level binary exactness does exactly that through the aggregator.
- **Host-kernel inotify dependence.** Acceptable: exactness is claimed only for established, non-overflowed, non-mutated ledgers; the realization fails closed on every tested way to lose observation. It is host-dependent: record the kernel and `inotify` sysctl values in profile/host identity (host execution environment is already frozen; confirm the three inotify limits are part of it or add them).
- **Layout `/opt/ssdp/skills/<root>/…`.** Acceptable as an OMP-profile assumption; it is also required by the pre-request rule's `<root>/SKILL.md` pattern. Other adapters need their own decision.
- **Is the contract unmeetable?** I do **not** raise a Serious Challenge against the contract. Mechanism shown, magnitude unmeasured: plausible honest behaviours (`grep -rn`, native `grep`, `grep -c`, `wc`, `grep -l`) make a run inexact, and one inexact run voids the campaign-wide `owner_false_activation` part (C-5). If rehearsals show these behaviours are common for the frozen executor, this becomes a Serious Challenge to the D3/contract interaction. Falsifiable gate for the pre-run checker: rehearse the executor model with the T1/T7/T8 and a broad sample of other episodes through the real path and report the fraction of runs with `resource_observation.exact = false` and which commands caused it; refine exactness per question before relying on the observation.
- **Entry-only + deterministic stratum.** Contract §4 requires deterministic activation for T1/T7/T8, so *every* such run has the delivered root without a native read event; B-D4-1 therefore makes the most common mode of the burden panel inadmissible for the OMP profile until fixed. That is a D4 defect today, not a contract defect.

## 9. PEM Historical Applicability Set (workplan-triggered; memory bound by the workplan)

```yaml
pem_basis:
  accepted_project_state: 2585b73f00420daca185a4fbb9ac42a79473eda1   # = current main; ancestor check true
  accepted_pem: PROJECT-ENGINEERING-MEMORY.md blob 1561797125622f355f84eb27319f87e8fa4227d9   # equals HEAD:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: NONE   # the branch carries no PEM change; HEAD PEM blob equals the basis blob
has:
  - id: DS-001
    disposition: APPLICABLE
    reason: Proxy/synthetic fixtures staying green while the real owner is wrong is the mechanism of P1/P2; unit fixtures use distinct synthetic files and cannot see overlap on the real package. Qualification evidence must stay bounded to the property actually tested (supply by content, not consumption by inode). EVIDENCE_ONLY; not used as authority.
  - id: PC-001
    disposition: APPLICABLE
    reason: Successor work must not mutate frozen prior-version/historical bytes. Checked: the commit's name-status touches only qualification/ssdp70/{eval, new D3 record, new activation-implementation-20261004 files}; no ssdp6x/ssdp66, frozen, dist, source or generated path; evidence-addendum files are all added, none modified. Authority owner file source/shared/references/protocol-versioning-and-compatibility.md exists; its 6.5 source commit locator was not re-verified for 6.6 binding health.
  - id: FF-001
    disposition: NOT_APPLICABLE
    reason: Premature immutable public-source/bootstrap publication; nothing is published or frozen by this commit.
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: Source-to-package routing repair; unrelated surface.
  - id: SP-002
    disposition: NOT_APPLICABLE
    reason: Self-reference-safe descendant publication; no release or fallback identity is created.
```

Memory is a PARTIAL coverage record (6.5 era) and cannot prove absence of other relevant lessons; no durable PEM update is recommended from this review alone.

## 10. Documentation, dependency and history impact

- **Documentation.** Workplan line 707 and contract §1 items 4/5/11 are not reconciled with the decision (C-4). The decision's Gap wording needs C-6. No README/CHANGELOG impact (protocol 7.0 unreleased; qualification-only). `source/` and `dist/` are untouched, so no generated-descendant parity is affected.
- **Dependency.** `package_ledger.py` joins the OMP execution-profile identity, so any previously frozen OMP headless profile is invalidated by design (the template is unchanged). `core70.py` changed; the untracked evaluator profile `profiles/omp-evaluator-readonly.json` records core70.py and assess70.py digests that **do not match** the current files (assess70.py was already mismatched; out of scope, mentioned only because the D3 change widens the drift). Retained Stage 7/guard-only evidence is unaffected and remains append-only: the evidence addendum files are new, none modified.
- **History.** The two guard-only realizations remain on record. Any retained realization produced after a D3 amendment (C-1…C-5) must be treated as new evidence; the realizations cited as development evidence in the decision (e.g. 14 454 + 45 958 = 60 412) remain valid for the cases they exercise (`cat` of the owner alone) and are not invalidated by SC-1.
- **Not touched by this review:** the repository, custody, frozen/historical Stage 7 evidence, and the eight untracked files. `~/ssdp70-omp-stagef` was read only (its directory count is unchanged by my runs because `HOME` was redirected to the scratchpad).

## 11. Recommended path (not a design mandate)

1. Amend the D3 record for C-1…C-6, re-submit for independent D3 acceptance (fresh reviewer or this reviewer's re-check against the discriminating evidence in SC-1).
2. D4 after acceptance: attribution rule (B-D4-2), entrypoint-only gate (B-D4-1), phase-independent supply and monotonic/ordering stamps (B-D3-2), retention cap and error recording (F-1/F-2), floor replaced by distinctiveness (F-4).
3. Add tests that would fail today: real-path P1, P2, H0; skew `account` case (`exp5`); ledger-less adapter (C6); a natural-overflow real-kernel test; owner copies in an overlap fixture. Re-run `test_activation_accounting`, `test_omp_integration` and the root suite on the amended tree and bind the logs to the tree id.
4. Before relying on the observation for campaign floors: the rehearsal gate in §8.

*Stop condition.* I did not manufacture closure: C1, C4, C6 were not falsified by the attempts above; C2, C3, C5 were. The remaining unexamined items are listed in "Attempts not run".
