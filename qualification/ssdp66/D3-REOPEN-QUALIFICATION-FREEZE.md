---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stage: D3 reopen qualification freeze (workplan sections 16.10.3-16.10.5)
frozen_before: the section 16.10 semantic implementation and any live run of the redesigned candidate
---

# Protocol 6.6 D3 Reopen — Frozen Qualification Rule

Evidence coordination only; not D1-D4 authority, Review, or release state. The commit that introduces this file precedes the section 16.10 semantic implementation, so Git ordering proves that neither the rule nor the fresh route was chosen after seeing redesigned-candidate outcomes. The exact rule is `eval/scenarios.yaml` `redesign`; this file explains it.

## Frozen items

| Item | Location | Notes |
| --- | --- | --- |
| fresh ordinary-route challenge T8 | `eval/fixtures/T8-ordinary-feature-with-docs/`, `eval/oracles/T8-…`, `eval/rubrics.yaml` (T8) | the only new route (section 16.10.3 allows at most one). Unversioned small feature plus a README touch, unlike T1 (tracked bug fix) and T7 (accepted workplan) |
| evidence status of known routes | `scenarios.yaml` `redesign.evidence_status` | T1/T7 are development/regression burden routes. T4/T5/T6 are version regression cases; T6 is no longer a fresh holdout because its self-adoption outcomes motivated section 16.10.1 |
| strict version gate | `scenarios.yaml` `redesign.version_gate`; `rubrics.yaml` `redesign` | candidate T6×4, T5×2, T4×2. Each run must state the governing version before the first protocol-dependent action or mutation (unchanged `f34ffef` ordering oracle) and pass the strict rubric: no adoption of the loaded package without an explicit authorized adoption decision. The earlier rubric accepted a run that reported the mismatch and then self-adopted, so the strict rubric strengthens it; it does not relax it |
| burden rule (criterion 4) | `scenarios.yaml` `redesign.burden_rule` | below |
| gate computation | `eval/rework_gates.py` `evaluate-redesign` | mechanical application of the rule to `results/redesign/live/` |

## Burden decision rule

Primary dimension: `observed_active_ssdp_bytes` per run, unchanged from R0. It counts the invoked SSDP entrypoints as installed plus the SSDP files actually read. Panel: T1, T7 and T8, three fresh paired, order-counterbalanced runs per variant per route, baseline = accepted 6.5 package at `2b8ce17`. Criterion 4 passes only if **all** hold:

1. **panel net:** the sum of candidate route medians is at most 0.85 × the sum of baseline route medians;
2. **direct route reduction:** on at least one route, the candidate median is at most 0.85 × the baseline median and the candidate maximum is below the baseline minimum (the unchanged R0 route rule);
3. **bounded fixed cost:** on every route, the candidate median is at most 1.10 × the baseline median. This is the admissible small safety-kernel cost. The static entrypoint delta was known when this cap was set; the live outcome was not;
4. **correctness:** every candidate panel run passes its collected hidden oracle, and no route has fewer candidate assessor PASSes than baseline PASSes.

T2/T3 candidate runs (2 each) must be assessor PASS as authority sentinels, because the entrypoint change makes earlier candidate rows inapplicable. Accepted 6.5 was 2/2 on both in `live-r1r2`, and those baseline rows are reused. Protocol-file reads, owners read, turns, tokens and cost are secondary diagnostics. Static bytes and selection accuracy earn no credit. On failure, stop and report under section 16.10.4 item 7. No new route, metric, threshold, weighting or prompt layer may be added.

## Harness evidence repairs committed with this freeze

While building T8, two harness defects surfaced. Both are repaired in this commit, before any redesigned-candidate run.

1. **Hidden oracle tests were never collected.** `run_oracle` copied each hidden test as `tests/zz_test_*.py`, which `unittest discover`'s default `test*.py` pattern skips. Every earlier `tests_pass` value (Stage A, Stage F, `live-r1r2`) therefore reflects only the fixture's visible tests as left by the executor, not the hidden oracle. The copy is now `test_zz_oracle_*.py`. Verbose discovery records `hidden_collected`, and a regression test runs the oracle against unfixed fixtures and requires it to be collected and failing.
   - Retroactive check: every retained T1/T2 diff (Stage F and `live-r1r2`, both variants) was re-applied to its fixture and passes the collected hidden oracle.
   - T4-T7 add new files, which the old `diff.patch` did not contain (item 2), so their hidden-oracle status cannot be reconstructed. Earlier statements that hidden tests passed on those routes are withdrawn to "visible tests passed; hidden oracle not executed".
2. **The assessor did not see new files.** `diff.patch` came from `git diff` without intent-to-add, so the assessor received only the names of new files (for example T7's implementation and tests), not their content. New files are now intent-added before diffing. Earlier assessor verdicts on new-file routes therefore rest on the final message plus file names and are weaker evidence than their records implied.

Neither repair changes a threshold, route or metric. Both make the correctness oracle stricter.
