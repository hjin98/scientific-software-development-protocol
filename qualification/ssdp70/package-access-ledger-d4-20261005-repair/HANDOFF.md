# D4 repair after the independent review (NO-PASS on `9de893a`): evidence and hand-off

Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. This directory records the repair work after `qualification/ssdp70/INDEPENDENT-D4-PACKAGE-ACCESS-IMPLEMENTATION-REVIEW-2026-10-04.md`. **It is not an acceptance.** The repaired code has not had a second independent Review, and the implementer cannot accept its own work. The earlier bundle `package-access-ledger-d4-20261004-realization/` is left unchanged and describes `9de893a`.

## Identities
Base: HEAD `5a6e29b` (tree in `identity.json`). The tested tree is that HEAD plus the uncommitted delta in `implementation-delta-over-5a6e29b.patch` (per-file hashes in `code-file-hashes.sha256`). The delta is committed together with this directory. Files not in the delta (for example `test_activation_accounting.py`) are unchanged from `5a6e29b`. OMP 18.0.11 `6054460b…cd26`. Host: AMD Ryzen 9 5950X (16 cores, 32 threads); `nproc` prints 1 because `OMP_NUM_THREADS=1`.

## Review findings and disposition
| Finding | Disposition |
|---|---|
| B-1 replacement bars on `not-applicable` | Fixed (`other_criteria_clear`). `fail` and `unresolved` dispositions still bar, per contract item 13; the owner floor is derived by the core, not an evaluator disposition. |
| B-2 tests stay green on broken code | Closed to 44 of 46 mutants in the fast suites. M44 (recompute never compares) is killed by the real-OMP test `test_c_tampered_or_missing_derived_event_fails_recomputation_on_a_real_run`, verified in a scratch copy. Aggregation wiring (M36-M38) is now tested through the extracted `batch_assess70.score_slots`. |
| 6 owner-read claim matching narrowed | Fixed: `"owner-read" in claim` except `owner-read-absence` (core70, harness70). |
| 7 native owner-read target sets differ | Fixed: one shared `package_ledger.native_owner_target` used by ledger and adapter. Test fails on the old predicate. |
| 4 second replacement after a partial first aborts aggregation | Fail-closed instead of aborting: disclosed as unscored, the question stays required. Which run scores the other criteria is **not decided** (contract/D3 question). Same-question reuse still raises. |
| 11c scan cache key, 11d line segmentation | Fixed in `package_premise.py` (key includes floor and owner name; segmentation as the accounting; an undecodable owner copy is UNRESOLVED). |

## A mistake made and corrected during the repair (kept on record)
I changed `candidate_window` so a window with no earlier request or an empty window kept its end ("literal reading" of D3 item 5, review finding 15). That made the honest "read the owner through a non-literal path, then answer in text" form depend on heartbeat phase: a text-only final turn has no request position, its fallback makes the window end 0, and an empty window cannot explain a whole-file read. `test_c_d_j_p_s_v_x_real_artifacts…` failed deterministically on that tree (`diagnostic-failed-run/`). An earlier serial 24/24 pass on the same code was luck and is **not** evidence. The change is reverted to the reviewed behavior (whole-trace window); a deterministic unit test now pins that honest form. **D3 should state what an empty window resets.**

## Executed on the final tree (logs hash-bound in SHA256SUMS)
| Check | Result |
|---|---|
| `test_activation_accounting`, 16-way parallel, run 3 times | 24/24 each (flake check) |
| `test_omp_integration`, 16-way parallel | 54/54 |
| eval non-runtime set (omp_units, portable70, stage_f x2, control_path_policy, mcp_stdio, harness_integration, package_ledger, batch_cli, package_premise) | 324 OK |
| root `unittest discover -s tests` | 407 OK, 3 skipped (remote public-fallback checks; **not run**) |
| mutation list (`logs/mutate.py`, fast suites) | 44 of 46 killed; survivors M4 (deliberate, D3 text item) and M44 (killed by the real-OMP test, see above) |
| `git diff --check` | clean |
Parallel runs used one scratch HOME per test process (`ptest.sh` pattern: one process per test id, 16 at once). Real-OMP runs use the local stand-in provider only and are development evidence.

## NOT run / still open
- **Second independent Review** of the repaired code.
- Executor rehearsal, run count N and the 0.8 target, F-5, a production premise witness, stakeholder ratification, any runner/profile/transform admission.
- Review items not repaired because they are rehearsal or text items: 1-3 (final-text-turn window start, stand-in latency hiding timing effects, 5 ms clock tolerance vs NTP slew), 5 (inexact-rate counting), 8-10, 12-14, 16. Finding 15/M4 and finding 4 need a D3/contract decision.
- The real-OMP mutation of the recompute test was run in a scratch copy for M44 only, not for every mutant.
- The untracked `package-access-ledger-d4-20261004-continuation/` directory and the eight out-of-scope files are untouched and uncommitted.
