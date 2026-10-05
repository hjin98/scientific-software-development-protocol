# Fixes after the second code review and the text review of the window/replacement clarification

Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. **Not an acceptance. Both independent reviews are NO-PASS at the moment this was written** (see below); the fixes here have not been re-reviewed. Earlier bundles are unchanged.

## Independent review record (committed with this directory)
| Review | Subject | Verdict | Report |
|---|---|---|---|
| Text, R1 | clarification `924194c4…` | NO-PASS (B-1: a partial replacement dropped a pre-R2 owner read) | `INDEPENDENT-D3-WINDOW-REPLACEMENT-CLARIFICATION-REVIEW-2026-10-05.md` |
| Text, R2 | revised | NO-PASS (R2-1: "never discarded" not true for several cases) | `…-R2.md` |
| Text, R3 | revised | NO-PASS (R3-1: replacement of a hard-failed original dropped) | `…-R3.md` |
| Text, R4 | revised | **NO-PASS (R4-1)** | `…-R4.md` |
| Code, 2nd review | commit `96d2106` | **NO-PASS** (SC-1, B-1, B-2); it did not see any later edit | `INDEPENDENT-D4-PACKAGE-ACCESS-IMPLEMENTATION-REVIEW-2026-10-05-R2.md` |
Each text round found a narrower defect than the last. R4-1 is **not fixed**: dispositions can be bound to owner-floor, fixed-cost and active-material opportunities, so an original whose only unresolved item is bound to those parts is treated as having another unresolved criterion and loses its mandatory replacement (fail closed, availability cost). It is recorded as a known limitation in the clarification, together with unbound declared runs and a T7 owner-only rerun's `unresolved` critical disposition.

## Fixed in this step (identities in `identity.json`, delta over `96d2106` in `implementation-delta-over-96d2106.patch`)
- Slot replacement semantics, `batch_assess70.replacement_slots` / `score_slots`: no definite failure in any declared run is discarded. A **hard failure** (positive pre-R2 owner read, deterministic-activation FAIL, any `fail` disposition) or a **block** (also an unresolved disposition) in a replacement stands for the slot whatever the original's eligibility or the replacement's evidence state and bars further reruns; a replacement declared for an original with a hard failure, or for an original with no open question it can resolve (a reserve cannot override a clean original), is refused (aggregation raises); a replacement must resolve its own owner floor plus the byte question when open and available; attempts and scored replacements are counted separately; a T7 owner-only rerun's `fail` dispositions count in the critical-failure and disposition tallies.
- Activation counts **every declared deterministic run**, scored or not (code review B-2).
- Dead checks removed (an unreachable "already scored" check, redundant eligibility clauses).
- Clarification text updated to match, plus the OMP bash line-truncation rehearsal item.
- Code review SC-1 is the same defect as text review B-1 and is closed by the standing-failure rule.

## Executed on this tree (logs hash-bound in SHA256SUMS)
| Check | Result |
|---|---|
| `test_activation_accounting`, 16-way parallel, twice | 24/24 each |
| `test_omp_integration`, 16-way parallel | 54/54 (run before the last dead-code removal; that module does not import `batch_assess70`) |
| eval non-runtime set | 338 OK |
| root tests | 407 OK, 3 skipped (remote public-fallback checks: **not run**) |
| `git diff --check` | clean |
| Mutation, reviewer's list (`logs/mutate.py`) | 42 killed, 1 survives (M44), 3 targets rewritten (M4, M12, M22: superseded, not counted as killed). M44 is killed by the real-OMP recomputation test (`logs/fin-M44.log`) |
| Mutation, window list | 5 killed; W6, W7 survive the fast suites and are killed by the real-OMP retry/mismatch test (`logs/fin-W6.log`, `fin-W7.log`); 3 patterns superseded (R1-R3, rewritten) |
| Mutation, current replacement/activation list (`logs/mutate_repl.py`) | 12 of 12 killed |
Method caveat: mutation scratch copies lack the repo `dist/` layout, so `test_omp_units` is excluded from them.

## NOT run / open
- A third independent code review of this tree and a fifth text review: **not run**. The code reviewer examined `96d2106` only.
- The clarification text has **no PASS**; binding its hash in `core70.derive_package_access` is deferred until it has one.
- Known limitations of the clarification (above), the code review's other non-blocking findings (about 20, including 22 fast-tier mutation survivors in its 61-mutant matrix, an established ledger with zero rows scoring exact, a non-bool `dir` hiding opens), and the OMP 768-character line truncation (66 of 213 twinned files can never be explained by route (iii)) are not repaired; the last is a rehearsal measurement.
- Executor rehearsal (real provider latency, partial-replacement rate, unverified-pairing rate, truncation rate), run count N and the 0.8 target, F-5, production premise witness, ratification, any admission.
