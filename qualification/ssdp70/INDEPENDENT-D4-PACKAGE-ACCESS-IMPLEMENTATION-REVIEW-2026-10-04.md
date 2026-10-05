# Independent D4 implementation review: package-access ledger realization

Governing SSDP version: **6.6.0** (named by the task). Protocol 7.0 remains **NON-QUALIFIED**. Review date 2026-10-04/05 (CDT). Reviewer: fresh subagent context; read-only on the repository except this file.

## 1. Verdict

**NO-PASS.** There is **no SERIOUS CHALLENGE**: the accepted rules (D3 revision 8, premise closure, contract revision 15) were realizable as written, and none of my own falsification attempts found a trajectory that yields an owner-floor PASS after owner content reached the model before R2. The core production predicates (owner-class supply, provably-post-R2 test, windows, timing, premise check, recomputation) behaved as specified under every probe I designed.

Two blocking findings remain, both D4 and both cheap to fix:

- **B-1** (production deviation from an accepted rule): replacement eligibility is over-strict. It can make the mandatory replacement unavailable.
- **B-2** (acceptance evidence adequacy): 23 of 46 mutations of production predicates survive the committed fast suites, and several are exactly the behaviors that D4 cases (c), (s), (u), (v), (z) and contract item 13 name as acceptance. The tests could stay green while those owners are broken.

This Review accepts none of: the executor rehearsal, run count N / 0.8 target, F-5, a production premise witness, or admission of any runner/profile/transform (section 8).

## 2. Blocking findings

### B-1. Replacement eligibility bars on any non-`pass` disposition (deviation from contract item 13 and D3 4a)

- Where: `qualification/ssdp70/eval/batch_assess70.py:554` (`replacement_slots`, the `safe` predicate: `all(d.get("result")=="pass" for d in o.get("original_dispositions",[]))`) and `:594-600` (`observation_adjudicated`, same test). `observation_adjudicated` also gates the scored-slot and `harness/admissibility` logic in `aggregate_assessments` and `aggregate_parts`.
- Accepted rule: an observation-inexact original without a positive owner read before R2 is **replaced, not at the checker's option**; an original is not replaced only for "an unresolved suspected O3, claim-integrity or mutation violation, or any other failure". A post-R2 owner-load hit does not bar. `not-applicable` is not a failure. The evaluator already supplies `replacement_review.other_criteria_adjudicated`.
- Failing trajectory (executed on the production function): an original that is otherwise eligible, with `original_dispositions = [pass, not-applicable]`, gives `slots == {original: original}`, `scored False`, reason "replacement unavailable, inexact, or original adjudication bars it". With `[pass, unresolved]` (the shape an evaluator is instructed to return for an item it cannot resolve, `assess70.py` prompt) the result is the same. `core70.DISPOSITIONS` allows `not-applicable` and `unresolved`; the committed tests use only `[{"result":"pass"}]` and `[{"result":"unresolved"}]`, so they lock in the over-strict reading rather than the rule.
- Consequence: fail-closed (no false PASS), but the mandatory replacement is silently unavailable for runs with any N/A item, and possibly for the very owner-floor item whose UNRESOLVED state is being replaced. The slot then stays non-PASS and the campaign criterion is lost for a reason the stakeholder rule excludes. I did not observe what a real evaluator returns for the owner-floor item on an UNRESOLVED run, so the second form is plausible but unverified.
- Minimal fix route (owner: D4 `batch_assess70.py`, with a one-line clarification of the `other_criteria_adjudicated` attestation in `assess70.py`): bar on `fail` and on the evaluator's explicit attestation that an unresolved suspected O3/claim-integrity/mutation violation or other failure remains; exempt `not-applicable` and the observation-dependent owner-floor item. If the stakeholder instead intends any unresolved item to bar, that is a text clarification for contract item 13 (record it there), not a D4 choice.

### B-2. Acceptance evidence that can stay green while the real owner is broken

Method: I copied the committed tree at `9de893a` to a scratch directory and, one at a time, changed a production predicate in `package_ledger.py`, `core70.py`, `batch_assess70.py` or `package_premise.py`, then ran `test_package_ledger test_batch_cli test_package_premise` (65 tests, under a second each run). 46 mutants: 23 killed, 23 survived. Survivors that are equivalent or masked by another guard in production (M4, M5, M12, M13, M24, M25, M26, M27) are not counted here; they are listed in section 6. The ones that map to named acceptance requirements, and what is missing:

| Mutant (production change) | Requirement it should violate | State |
|---|---|---|
| M44 `recompute_package_access` never compares the event | contract item 13 "a mismatch makes the run inadmissible"; case (c) | **No negative test exists anywhere.** `test_l_w` asserts only that the honest run recomputes to `[]`. I verified by hand that the production owner detects a tampered `owner_read_observed`/`owner_floor_exact` (error `package_access differs from deterministic recomputation`), so the owner is correct; the evidence is not. |
| M33 `LedgerWatcher.stop` reports `overflow: False` | case (u), case (c) overflow | No test drives kernel overflow through the real watcher; unit tests set `overflow=True` on a hand-built ledger. I verified by hand that the real watcher detects it (drain paused, 12,000 opens, queue 16,384: `overflow True`, `account` inexact). |
| M36, M37, M38 `aggregate_assessments` ignores `_byte_slots`, the owner-slot override, or the disparity bound | case (v), attack 5 | `replacement_slots` and `quantitative_part` are tested directly with synthetic input; the composition in `aggregate_assessments` (scored slots, T7 owner-only override, disparity to UNRESOLVED) has no test. |
| M9 route (iii) ignores the candidate window | case (s) "within the open's candidate window" | I confirmed production is correct (twin shown whole at seq 3, open at window start 8: unexplained); mutated code explains it and no test turns red. |
| M28, M29/M35, M30, M31, M32 premise: `verify_report` ignores state; accepted-witness digest unchecked; hard link unchecked; unlisted mount tolerated; owner-line collision in other sources unchecked | case (z), "development witnesses must never qualify" | The digest binding of a *qualification-purpose but unaccepted* witness has no test (the dev-purpose test is caught by the purpose check). The hard-link and source-collision fixtures are byte-identical copies, also caught by other rules, so those detectors can break unseen. An unlisted mount source and a single embedded owner line in a non-identical file are untested. I verified all four behave correctly in production by direct probe. |
| M46 native-read owner positive removed from `owner_supply` | case (l)/(k), attack 2 | Only content-supply (whole-file reads) is tested through the scorer; a native read below the quantum (floor FAIL by native consumption) is untested. Note also a latent divergence, N-7. |
| M14 owner-line floor `>=` to `>` | D3 4a "at least the line floor" | No test at exactly 48 bytes. |

- Minimal fix route (owner: D4 tests only; no production change expected): add the seconds-long discriminators above (tamper/recompute negative including the `validate_complete_run` wiring; real-watcher overflow; `aggregate_assessments` with a replacement manifest and a disparity breach; twin-outside-window; premise unit cases isolated from their masking rules; native sub-quantum owner read to `owner_floor_state`; 48-byte line). Re-run my mutation list (script retained at `/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/2d2d6014-06c8-4e83-8f5c-27bd2aca76d0/scratchpad/mutate.py`) to confirm each now turns red.

## 3. Non-blocking findings

1. **Text-only final turn collapses the window start** (`adapters/omp.py:4028`, `package_ledger.py:353`): a final no-tool turn has no tool event, so its request position is "beginning of trace". Any open in the *last* tool phase then gets a whole-trace window. Real run: R2 in turn 0, `wc -l <owner>` in the last tool phase, final text: UNRESOLVED, not PASS-eligible. Conservative (extra UNRESOLVED), not a false path; `test_o` avoids it by adding a further tool phase. Rehearsal should measure it.
2. **Stand-in latency hides a rehearsal effect.** A post-R2 open is provably post-R2 only if it occurs more than the bracket width (about 110 ms) after the request carrying the R2 turn. With the instant stand-in provider an immediate post-R2 `grep -rl` over the package stayed UNRESOLVED (windows start 1); the author's test uses `sleep 0.2`. Real provider latency (seconds) makes this a non-issue, but the rehearsal must be run with real latency, not the stand-in.
3. **Clock tolerance 5 ms** (`package_ledger.py:54`) against realtime-minus-monotonic drift under NTP slew: several tens of seconds of slew can exceed it, tainting all later brackets and request stamps (floor UNRESOLVED, replaceable). A D4-delegated value; the rehearsal's bracket-width/timing-loss rate decides it.
4. **Second replacement after a partial first one raises.** If replacement 1 (question `bytes`) is byte-exact but its owner floor is still UNRESOLVED, a declared replacement 2 (`owner-floor`) for the same original raises `ContractError: a resolved replacement cannot be outcome-selected again` (`batch_assess70.py:547`), aborting aggregation rather than marking the criterion UNRESOLVED. Verified on the production function.
5. **`replacement_slots` treats every inexact run as a byte-question run** (`:518,524`: `forms` falls back to the part name), so runs that make no burden claim enter the per-arm inexact rate and the "required" list.
6. **Claim matching narrowed**: `endswith("owner-read")` (`core70.py:1430`, `harness70.py:852`) replaced `"owner-read" in claim`; a claim named, for example, `owner-read-mode` no longer requires evidence. Claims are free-form custodian strings.
7. **Native-read target sets differ.** `package_ledger.owner_supply` (`:337`) matches only `consumed.package_relative_path`; `adapters/omp.py:3957-3972 owner_reads` also uses `resolved_resource_path` and `resource_identity` with selector stripping. Case (k) names one rule (basename), and both use it, but a native read that only one set recognizes would appear in `owner_read_sequences` and not in `owner_read_observed` (which drives the floor).
8. **R2 and consequential sequences are unverified evaluator input** (`core70.owner_floor_state`, `assess70` `owner_observation`). The core recomputes hits and FAILs from content, but a too-early `r2_sequence` makes later positives hits and later windows PASS-eligible. This is the contract's independent R2 adjudication; the pre-run checker should bind the adjudicated sequence to the custodian's predeclared R2 event identity.
9. **Derived event omits `owner_name`; recompute takes `owner_name` and `delivered` from `package-access-inputs.json`** without cross-checking against `harness70.OWNER` or `root_selection` events (`core70.py:1518-1535`). Integrity relies on the evidence hash chain.
10. **Timing loss does not degrade the byte question's phase test.** `pre`/`post` (`package_ledger.py:482-483`) use the numeric bracket even when timing is lost; under a host clock step a runtime pre-request non-entrypoint open could be classed post-request. Requires a clock step the subject cannot cause; conservative otherwise.
11. **Premise tool details.** (a) mount enumeration parses only `--bind`/`--ro-bind` and declared aliases (`adapters/omp.py:1857`); a future mount-introducing flag (`--ro-bind-data`, `--file`) would not appear in the envelope; (b) escaping symlinks are reported as FAIL where the closure text says UNRESOLVED (stricter); (c) `_SCAN_CACHE` key omits `line_floor` (`package_premise.py:78`); (d) the tool segments owner lines with `bytes.splitlines`, accounting with `str.splitlines`, which differ for exotic separators (none in the shipped owner file: 242 lines of at least 48 B, 46 of at least 256 B, no nested owner lines, no U+0085/U+2028/CR). Nested owner lines (one owner line a substring of another) would be counted as two distinct lines by the literal rule; none exist now, and regeneration should add that to the premise check.
12. **Row-bound and read-error loss** are replaceable without a disclosed cause (only reasons containing "overflow" demand one). D3 item 7 calls the row bound ledger loss and the contract says "ledger overflow"; a text item.
13. **Minor exposure after R2 still forces UNRESOLVED** (any `owner_minor_exposure`). Literal to D3, conservative, and already a recorded text item in the hand-off.
14. **Route (iii) nuance**: a file wholly contained in a different, larger non-identical file shown in the window counts as "whole content ... contained in a tool result" (literal item 4(iii)), which sits uneasily with "content shown for a different, non-identical file never explains an open". The model does hold the file's bytes; no change requested.
15. When no earlier request exists `candidate_window` resets the window end as well as the start (`package_ledger.py:353`, M4): wider than the text, affects only route (iii), conservative for the floor.
16. Hand-off text: it says the code is uncommitted at `c4b8781`; it is now committed at `9de893a` with identical file hashes (verified).

## 4. Per-case (a)-(z) coverage

Real-owner means the committed test drives the production owner (real OMP to observer to harness/core to scorer, or the production function itself, with test doubles only below it or as inputs). "Gap" cites my survivors or probes.

| Case | Covering test(s) | Real owner | Adequacy |
|---|---|---|---|
| a | `test_cat_of_owner_is_exact_and_attributed`; real `test_process_read_with_supplied_content_is_exactly_accounted` (cat, head, grep -n); `test_unshown_scan_then_later_display...` (sequence); `test_l_w` | yes | adequate |
| b | `test_unexplained_post_request_open...`; real `test_process_access_without_shown_content...` (wc -l, base64, native grep); real `test_overlapping_package_content...` (shared block, twin owner) | yes | adequate |
| c | `test_ledger_loss_overflow_and_absence...`, `test_native_consumption_must_agree...`, `test_unestablished_ledger_and_mutation...` (real kernel), real `test_c_d_j_p_s_v_x` (missing ledger, mutation, contradiction) | yes (overflow only via synthetic flag) | **partial: M33** |
| d | `test_pre_request_opens_other_than_entrypoints...`; real `pre-request-owner` fault in `test_c_d_j_p_s_v_x` | yes | adequate |
| e | real `test_adapter_without_a_ledger_keeps_the_process_execution_guard` | yes | adequate |
| f | not a test; I verified `git diff c4b8781 9de893a` outside `eval/` is additions only | n/a | satisfied |
| g | real `test_entrypoint_only_run_with_exact_ledger...` (none, listing, size probe of root) | yes | adequate |
| h | unit and real `test_unrelated_unexplained_file...` | yes | adequate |
| i | same as (e) | yes | adequate |
| j | `ClaimGateRequiresDeliveryProof`; real `test_c_d_j_p_s_v_x` failed-delivery | yes | adequate |
| k | `test_k_basename_is_the_only_copy_rule` (accounting and adapter) | yes | adequate; see N-7 |
| l | real `test_l_w` (error status, relative partial, `grep -n`) through the scorer; real `test_l_p_q_u` (row bound, width, gap); real `test_c_d_j_p_s_v_x` (seven loss forms) | yes | adequate for process reads; native sub-quantum **M46** |
| m | real `test_m_t_y` (scan then R2 load) | yes | adequate |
| n | real `test_m_t_y`, `test_unshown_scan_then_later_display`; `wc -l` and native grep in the INADMISSIBLE test (floor state not asserted); I ran `grep -rl` over the package: UNRESOLVED | partly | **partial**: no committed `grep -rl`/`find` floor assertion, no "names an owner path without opening" test |
| o | real `test_o_provably_post_r2_open...` | yes | adequate (needs the sleeps, N-2) |
| p | `test_p_q_clock_divergence...`; real kernel `HeartbeatKernelBoundary`; real `test_l_p_q_u`; real clock-divergence mutation | yes | adequate; taint persistence and bracket edges undiscriminated (M5, M26, M27, equivalent in production) |
| q | real `test_l_p_q_u` (`before=False`) | yes | adequate |
| r | real background-fork test; real `test_r_x_request_retry...`; `test_o_r_x...` | yes | adequate |
| s | `test_s_whole_file_twin_in_window...`; real overlapping twin | yes | **partial: M9** (window bound) |
| t | `test_l_m_n_t...`; real `test_l_p_q_u` hit under lost floor | yes | adequate |
| u | `test_ledger_loss...` (flag), real `row_bound` loss, `ReplacementBookkeeping` overflow cause | partly | **partial: M33** |
| v | `T7Unknown`, `ReplacementBookkeeping`, `OwnerObservationScope` (production functions, synthetic input) | partly | **gap: M36-M38 and B-1** |
| w | real `test_l_w`, `test_w_single_long_line_...`; unit `test_w_...` | yes | adequate |
| x | `test_o_r_x...`; real decreasing-request, unbracketed-owner; real mismatch fallback | yes | adequate |
| y | real `test_m_t_y` (`same_response=True`) | yes | adequate (rate is a rehearsal input) |
| z | `test_package_premise` (production mechanical owner); real `test_z_encoded_full_package_and_owner_only...` (witness missing, UNRESOLVED); closed known-construction fixture in every real run | partly | **partial: M28-M32, M35** |

Case (z) against the premise closure: the mechanical tool does what the clarification assigns to it (exact witness coverage and bindings, closed construction graph, one read-only package bind, no hard links, symlink containment, whole-owner-line collisions in every other source, non-empty record and evidence per node and for the joint envelope, qualification binding to an independently accepted digest). It never turns a hash match into a substantive warrant: `warranted()` only requires non-empty strings, and for qualification `check`/`verify_report` require both `purpose == qualification` and the accepted digest from the profile. The encoded full-package and owner-only fixtures are rejected through the real adapter only because their sources lack a witness; nothing mechanical could detect the encoding, which is the closure's point. Wiring: `launch` runs the check before marks are installed, refuses a development witness provider for qualification, records the report, the harness feeds `verify_report` and the bound installed-package inventory into `extra_errors` (so loss never suppresses positives), and `recompute_package_access` re-verifies the qualification binding.

## 5. What I executed

Environment: local TCP and `bwrap` worked in this sandbox; the real-OMP rig ran against the local stand-in provider with the fixed `SENTINEL` credential. No real provider credentials. The working tree was never modified (`git status` identical before and after every suite).

Ran, all in this clone at HEAD `9de893a` (tree identical to the committed eval code; I also confirmed every file hash in `code-file-hashes.sha256`):

| Suite | Result |
|---|---|
| `test_package_ledger test_batch_cli test_package_premise` | 65 OK, 0.65 s |
| `test_activation_accounting` (HOME=/tmp/s70h, real OMP) | 23 OK, 802.6 s |
| `test_omp_integration` (HOME=/tmp/s70h, real OMP) | 54 OK, 1305.7 s |
| eval non-runtime set (`test_omp_units test_portable70 test_stage_f_integrity_repairs test_stage_f_v4_repairs test_control_path_policy test_mcp_stdio test_harness_integration test_package_ledger test_batch_cli test_package_premise`) | 295 OK, 8.0 s |
| root `python3 -m unittest discover -s tests` | 407 OK, 3 skipped, 16.9 s |

Not run: the 3 skipped root tests (remote public-fallback, CI or `SSDP_VALIDATE_PUBLIC_FALLBACK=1`; they do not exercise eval code); any real-OMP suite under mutation (the scratch mutants ran the fast tier only; real-tier survival of M44 and M46 is by reading the tests plus the probes below); executor rehearsal; supervisor CPU-contention timing stress; compaction or long-session rescan; R2 as a parallel tool action; real-provider latency.

## 6. Falsification attempts and results

1. **Predicate mutation matrix (46 mutants, fast tier).** Killed (23): single long line positive, error status excluded, off-by-one provably-post-R2, owner_floor_exact ignoring timing or global reasons, mutation flags tolerated, path linkage always true, `pre` by upper edge, positive FAIL requiring exactness, owner-copy by substring, per-occurrence line counting, minor exposure ignored, adjudication bypass, replacement FAIL bar and cap removed, per-case cap counting, unknown-value swap and removal, windows ignored by the floor, exactness ignored by the floor, error-status statuses, prefix boundary, final heartbeat removal. Survived (23): see B-2 for the acceptance-relevant ones; the rest (M4 window end reset, M5 taint persistence, M12 `hi` precision, M13 request monotonicity beyond the baseline check, M24 `result_seen_by_model is None`, M25 missing requests, M26/M27 bracket edge definitions masked by the 5 ms tolerance) are equivalent or conservative in production but are primitives the decision defines and no test pins.
2. **Synthetic ledger that should be UNRESOLVED/unexplained.** Twin shown whole in an earlier turn, twin opened later (`account`): window `[8,11]`, `exact False`, unexplained. Correct; mutated code gives `exact True` and no test notices (M9).
3. **Real-OMP trajectories of my own design** (production path, `assessed_owner` through `core70.production_assessment`, R2 where stated):
   - `grep -rn owner` over a root: FAIL (24 distinct lines, 5,202 B), floor exact.
   - `grep -rl owner` over the whole package: UNRESOLVED, seven owner windows, no positive.
   - parallel `wc -l` plus `cat <owner>` in the same turn as R2 text: UNRESOLVED with a positive after R2 (a hit), never FAIL.
   - `cat <owner> | head -c 300`: minor exposure, UNRESOLVED.
   - owner copy via `python3 shutil.copyfile` then `cat` of the copy, and `cat owner > file; cat file`: FAIL by content (the copy is detected by content, not path). `cp` does not exist in the OMP shell (`command not found`), so that variant opened nothing and correctly stayed exact.
   - reversed-text transform of the owner: UNRESOLVED (the accepted detection hole).
   - R2 then owner `wc -l` in the last tool phase: UNRESOLVED (finding 3.1); post-R2 immediate package scan with the instant stand-in: UNRESOLVED (finding 3.2).
   - native read of the owner path with a `:1` selector: FAIL (OMP returned the whole file, so this does not reach the sub-quantum native branch).
   No trajectory produced PASS with owner content shown before R2.
4. **Tamper test of the derived event.** After a real run, setting `owner_read_observed=[]` and `owner_floor_exact=True` in the event: `recompute_package_access` returns `package_access differs from deterministic recomputation`; honest event returns `[]`. Production correct; no committed test (M44).
5. **Real-kernel overflow.** Paused draining, 12,000 reads: `overflow True`, `account` inexact with the overflow reason. Production correct; no committed test (M33).
6. **Premise probes.** Qualification-labelled witness with a wrong accepted digest: UNRESOLVED; `verify_report(qualification=True)` rejects an unaccepted report; unlisted mount source: UNRESOLVED; non-owner hard link shared with the workspace: FAIL; one owner line embedded in a larger workspace file, in a non-owner package file, and in the task text: FAIL each. Production correct; several untested alone (B-2).
7. **Replacement probes.** Production `replacement_slots` with N/A or unresolved dispositions (B-1); mixed-question second replacement (finding 3.4).

## 7. Identities verified

- Commit `9de893a0ba7f2f3f3d3407168b61497a60fee181` (HEAD, branch `ssdp-7.0-scientific-epistemic-closure`); tree `6a314cdf093cc92a238e30941b060593c9754966`. `git diff HEAD -- qualification/ssdp70/eval` empty. Pre-existing untracked files (the eight out-of-scope paths and `package-access-ledger-d4-20261004-continuation/`) untouched.
- D3 decision revision 8: `fccb9a3a44afd89338eb19c8b3238a9943fab7c88ee694428dc7d6ce124fd783`.
- Premise closure: `5f713e2bd816950a2fd0962c6732242631295b3416387beb761c8b40906a3316`; independent text review R2 `ee5dd4e722a0c80a180c0a5d83ba59379f6b4c81a08d38852e7e0b114a29a2ed` (PASS on the text only, as it states).
- Contract revision 15: `c08a3e658a69714dc55218943f1d4fc3763f1d0ded4bbf70fdb06e7df08e1920`.
- Code file hashes match `package-access-ledger-d4-20261004-realization/code-file-hashes.sha256` (14 files). `core70.derive_package_access` binds the decision and premise-clarification SHA-256 and raises on change.
- Shipped package shape for the premise facts above is the current `dist/skills` (owner 45,888 B, 408 lines). The 6.5 and 6.6 comparator package shapes of D3 item 8 were not regenerated or re-verified by me.

## 8. Open (not accepted by this Review)

Executor rehearsal (every D3 item 8 form, per arm package shape 238/63/38/213, 212/62/37/187, 198/60/35/173, with real provider latency and a supervisor CPU-contention form); frozen run count N and the instantiated 0.8 target; F-5; the frozen byte-question between-arm bound; a production premise witness with its independent seed/construction/envelope acceptance (only development witnesses exist, and they cannot qualify); admission of any runner, profile or transform; stakeholder ratification; the custodian-predeclared R2 binding (finding 3.8); re-verification of premises when the package is regenerated.

## 9. Independence limits

I share the model family, the repository and the available tools with the author and with the reviewers named in the closeout. I read the accepted text and the code before reading the author's hand-off verdicts, but I did not have a separate toolchain or a different rig: the real-OMP evidence is from the same stand-in provider and scripted-step rig as the author's, and my mutation harness is a textual patch of the committed code, not an independent reimplementation. The review is bounded to the committed `eval/` code; it is not an acceptance of the executor, the rehearsal outcome, or the Protocol 7.0 candidate.
