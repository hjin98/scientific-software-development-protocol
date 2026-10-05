# D4 realization of the two accepted D3 decisions: evidence and hand-off

Governing SSDP **6.6.0**; Protocol 7.0 **NON-QUALIFIED**. **Not an acceptance.** The clarification below has no independent text Review yet, and the code has had no second independent Review. The implementer cannot accept its own work. Earlier bundles (`…-realization/`, `…-repair/`) are unchanged.

## What was decided (stakeholder accepted the recommendations on 2026-10-05) and where it lives
`D3-PACKAGE-ACCESS-WINDOW-AND-REPLACEMENT-CLARIFICATION-2026-10-05.md` (sha256 in `code-and-clarification-hashes.sha256`):
- **A. Window end.** A request with no derivable or verified position bounds nothing from above (the window runs to the end of the trace); an unpositioned or absent earlier request starts the window at the trace start; an otherwise empty window is the whole trace. Owner floor depends on the window start only, so it is unchanged.
- **B. One slot, one scored run.** A non-T7 replacement scores only if exact for every available question still open on the original (owner floor always; bytes only with the frozen bound); partial replacements are disclosed and unscored; a scored slot refuses further reruns; T7 owner-only reruns are unchanged.

## Realization
- `adapters/omp.py` `request_positions`: `position: null` for a turn with no tool event and for every request when pairing is not verified (previously the trace start, which could not be told apart from a real position and shrank the upper edge to nothing).
- `package_ledger.candidate_window`: non-integer position is unpositioned; lower side trace start, upper side trace end; empty window is the whole trace; the old "no earlier request widens the end" shortcut is removed.
- `batch_assess70.replacement_slots`: slot-level rule above.
- Base: HEAD `c1e8150`; tested tree = that HEAD plus `implementation-delta-over-c1e8150.patch` (committed with this directory). OMP 18.0.11 `6054460b…cd26`.

## Executed on this tree (logs hash-bound in SHA256SUMS)
| Check | Result |
|---|---|
| `test_activation_accounting`, one process per test, 16 at a time, three runs | 24/24 each |
| `test_omp_integration`, 16-way | 54/54 |
| eval non-runtime set | 328 OK |
| root tests | 407 OK, 3 skipped (remote public-fallback checks: **not run**) |
| `git diff --check` | clean |
| Counterfactual: the new replacement tests on the previous `batch_assess70.py` | 1 error + 1 failure (they discriminate) |
| Mutation, reviewer's list (`logs/mutate.py`) | 43 of 46 killed; M44 survives the fast suites by design and is killed by the real-OMP recomputation test (verified in a scratch copy earlier); M4 and M12 patterns no longer exist (code rewritten) |
| Mutation, new window/replacement mutants (`logs/mutate_window.py`) | W1-W5 and R1-R3 killed by fast tests; adapter mutants W6, W7 killed by the real-OMP test `test_r_x_request_retry_shares_original_position_and_mismatch_falls_back` in scratch copies (`logs/real-W6.log`, `real-W7.log`) |
Caveat on method: the mutation scratch copies lack the repo `dist/` layout, so `test_omp_units` fails there for unrelated reasons; it is excluded from the mutation runs and its failures are not counted as kills.

## NOT run / open
- Independent D3 text Review of the clarification; independent code Review of this realization.
- Whether to bind the clarification's hash in `core70.derive_package_access` (as the premise clarification is) is left to the reviewers; it is not bound.
- Executor rehearsal (must report the partial-replacement rate and the text-final-turn window effects, with real provider latency, not the stand-in), run count N and the 0.8 target, F-5, production premise witness, stakeholder ratification, any admission.
- Review findings 1-3, 5, 8-10, 12-14, 16 remain rehearsal or text items.
- The real-OMP discriminators have not been run against old code.

## Brief for the reviewers
Code reviewer: attack honest-form inexactness as well as false PASS: the text-final-turn run, retries, unverified pairing, a replacement that resolves only bytes or only the owner floor, the no-bound case. Re-run the mutation lists yourself. Text reviewer: judge whether A and B are determined, consistent with D3 revision 8, the premise clarification and contract item 13, and whether any effect on the byte question or the owner floor is understated.
