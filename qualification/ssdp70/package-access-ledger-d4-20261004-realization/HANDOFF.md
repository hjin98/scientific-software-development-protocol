# D4 package-access ledger realization: hand-off to independent Review and the pre-run checker

Written 2026-10-04 (CDT). Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. **D4 realization is implemented and its executed checks pass. It is NOT accepted: an independent implementation Review has not happened, and the implementer cannot accept its own work.** Nothing is committed, pushed or admitted.

## Authority used
- D3 revision 8 (`fccb9a3a…cd783`) and contract revision 15 (`c08a3e65…e1920`), unchanged.
- `D3-PACKAGE-ACCESS-PREMISE-CLOSURE-2026-10-04.md` (`5f713e2b…a3316`), independent R2 text PASS (`ee5dd4e7…a29a2ed`), recorded in `PACKAGE-ACCESS-PREMISE-RESOLUTION-2026-10-04.md`. It resolves the historical Serious Challenge in `package-access-ledger-d4-20261004-025110Z/HANDOFF.md` at the D3 text boundary. The mechanism is unchanged; no new principal or channel.
- The task hand-off said `eval/` was unchanged since `8be024a`; that was stale. The tree already held the draft described in the earlier HANDOFF, and this session continued it.

## Identities (see `identity.json`, `code-file-hashes.sha256`)
HEAD `c4b8781b…`, HEAD tree `a3efc6c7…`. The code under review is **uncommitted**: 12 modified tracked files plus `eval/package_premise.py` and `eval/test_package_premise.py`; per-file hashes are in `code-file-hashes.sha256` (manifest digest `f29b2c32…2242`). OMP 18.0.11 `6054460b…cd26`. Logs here were produced against exactly that code (no edits after the runs; `git diff --check` clean).

## Executed (hash-bound in SHA256SUMS)
| Check | Result |
|---|---|
| `test_activation_accounting` (real OMP → observer → harness/core → scorer; HOME=/tmp/s70h) | 23 OK, 810 s |
| `test_omp_integration` (real OMP, 54 tests; clears the old AF_UNIX item with a short HOME) | 54 OK, 1286 s |
| eval non-runtime set (omp_units, portable70, stage_f x2, control_path_policy, mcp_stdio, harness_integration, package_ledger, batch_cli, package_premise) | 295 OK |
| root `unittest discover -s tests` | 407 OK, 3 skipped |

The 3 skips are remote public-fallback realizations (CI / `SSDP_VALIDATE_PUBLIC_FALLBACK=1`). They are **not run** and not a pass; they do not exercise eval code.

## Counterfactual (pre-change code)
Old production code from `HEAD` with the new tests: `test_batch_cli` gives 5 failures and 7 errors (replacement bookkeeping, T7 unknown value, owner-question scope, positive identity). `test_package_ledger` fails at import (no `PARAMETERS`), which shows the old API is missing, **not** a per-case discrimination. The real-OMP discriminators were **not** run against old code; they are not claimed to satisfy the counterfactual requirement.

## Case coverage map (names; Review must judge sufficiency)
(a)(b)(e)(g)(h)(i) `test_activation_accounting` process-read/inadmissible/entrypoint/ledger-less tests; (c)(d)(j)(s)(v)(x) `test_c_d_j_p_s_v_x_real_artifacts_…`; (k) `test_k_basename_is_the_only_copy_rule`; (l)(w) `test_l_w_…` and `test_w_single_long_line_…`; (m)(t)(y) `test_m_t_y_…`; (n) `test_unshown_scan_…`/`test_process_access_without_shown_content_…`; (o) `test_o_provably_post_r2_…`; (p)(q)(u) `test_l_p_q_u_…` plus real-kernel `HeartbeatKernelBoundary`; (r)(x) `test_r_background_…`, `test_r_x_request_retry_…`; (z) `test_z_encoded_full_package_and_owner_only_…` plus `test_package_premise`; replacement/T7/byte bound in `test_batch_cli`. (f) is the append-only evidence rule, not a test.

## NOT run / open (blocking admission, not this realization's execution)
- **Independent implementation Review** (required before any acceptance).
- Per-case counterfactual for the real-OMP tests (above).
- Executor rehearsal, per-arm package shapes (238/63/38/213, 212/62/37/187, 198/60/35/173), common honest forms, bracket-width distributions, per-question rates; frozen run count N and instantiated 0.8 target; F-5; stakeholder ratification; runner/profile/transform admission.
- **Production premise witness:** only development witnesses exist. The mechanical tool verifies bindings, closure and collisions; it cannot grant substantive warrants. A development witness cannot qualify a profile (`verify_report(..., qualification=True)` rejects it).
- Real-OMP forms not exercised in this stage: above-quantum keyword grep as an intended non-replaceable pre-R2 FAIL, R2 as a parallel tool action, compaction/long-session rescan, supervisor CPU-contention timing stress, non-literal `PROTOCOL_VERSION` paths. These are checker rehearsal forms.
- Known earlier-draft items (malformed-artifact fail-closed, request-position primitive at first tool-call/result event incl. no-tool final turns, typed R2/replacement adjudication, overflow-cause adjudication, per-question availability without a byte bound) are present in code/tests but their sufficiency is **unreviewed**; Review should probe them first.

## Text items recorded, passed documents untouched
Effect (d) means a censored burden sample neutral on outcome; align effect (f) with the no-ledger bullet; state the T7 owner-floor rerun cap unit (per affected original run, at most twice); per-question availability when the byte bound is absent; minor-exposure placement; request-position versus same-response wording; reduce repeated 256-byte restatements in the workplan to pointers. Monotonic request stamping is implemented (`evidence70.py`) and exercised in the real-OMP tests.

## Checker brief (rehearsal; independent)
Freeze before admission: common honest forms, per-arm package identities, N and target, all gate parameters, and the premise witness source envelope. Rehearse every form in D3 item 8 plus: full-package and owner-only copies under computational encodings, generator-output and joint-envelope warrants (must be UNRESOLVED/FAIL, never PASS by label), same-response owner load, pairing mismatch, request retries, compaction/long-session rescan, supervisor contention. Report per form/arm/question the exactness, cause, verdict and bracket-width distribution. Reopen D3 per its triggers if rehearsal disproves containment or honest UNRESOLVED rates exceed what replacement absorbs.

## Cautions kept
No commit, push, release-state edit, custody or frozen evidence write; `activation-implementation-20261004/` untouched; the eight out-of-scope untracked files untouched; PEM cold.

## Retained code snapshot and reproduction (added)
`implementation.patch` is the complete in-scope code delta against HEAD `c4b8781b…` (tracked diff of `eval/` plus the two new files `package_premise.py` and `test_package_premise.py`; the eight out-of-scope files are excluded). It was verified to apply to a clean `git archive HEAD` copy and to reproduce every hash in `code-file-hashes.sha256`. A reviewer should apply it to a clean checkout of HEAD (not trust the live working tree) and re-run:

```
export PYTHONDONTWRITEBYTECODE=1 SSDP70_OMP_EXE=$HOME/.local/bin/omp
mkdir -p /tmp/s70h/ssdp70-omp-stagef && ln -sfn $HOME/ssdp70-omp-stagef/runtime-closures /tmp/s70h/ssdp70-omp-stagef/runtime-closures
cd qualification/ssdp70/eval
python3 -m unittest test_package_ledger test_batch_cli test_package_premise                 # seconds
HOME=/tmp/s70h python3 -m unittest test_activation_accounting                               # ~14 min, real OMP
HOME=/tmp/s70h python3 -m unittest test_omp_integration                                     # ~21 min, real OMP
python3 -m unittest test_omp_units test_portable70 test_stage_f_integrity_repairs test_stage_f_v4_repairs test_control_path_policy test_mcp_stdio test_harness_integration test_package_ledger test_batch_cli test_package_premise
cd ../../.. && python3 -m unittest discover -s tests
```
`test_stage_f_*_repairs` need git history, so run them in a real clone, not a `git archive` copy. Real-OMP runs use the local stand-in provider only, with the fixed harmless `SENTINEL` credential; they are development evidence, never qualification.

## What the Review should attack first (highest false-PASS consequence)
1. `package_ledger.account()` owner-class supply and the provably-post-R2 test: can any trajectory yield `owner_floor_state` PASS with an owner read before R2?
2. Positive evidence under lost observation: a pre-R2 positive must stay FAIL after ledger loss, timing loss or an inexact byte observation (`core70.owner_floor_state`, harness summary).
3. Request-position pairing, its verification and the start-of-trace fallback (`adapters/omp.py`), including retries and parallel R2.
4. `package_premise.check` and `verify_report`: a hash match must never become a substantive warrant, and development witnesses must never qualify.
5. Replacement and T7 bookkeeping (`batch_assess70.py`, `core70.campaign_manifest_errors`): original retained and disclosed, a positive pre-R2 read bars replacement, overflow needs a disclosed cause, owner-floor-only rerun outside the median and capped.
