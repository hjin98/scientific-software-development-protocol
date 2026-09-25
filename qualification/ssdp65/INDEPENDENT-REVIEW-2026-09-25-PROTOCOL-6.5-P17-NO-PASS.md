---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: feca003e577fdfa2ae4219e0df2a2cdb38e5d757
semantic_ref: feca003e577fdfa2ae4219e0df2a2cdb38e5d757
binding_descendant: 30c7793f80dd99702608ae6e7f8cba9bab0c3b6c
readiness_descendant: 8730a7c0e8aa7ecb9e1335a557fd61194fd7bbbb
exact_candidate_run: 36167091971
binding_run: 36167377663
readiness_run: 36167578975
serious_challenge: none
blocking_findings:
  - B65-P17-1
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P17

## Disposition

**NO-PASS.**

Exact immutable P17 `feca003e577fdfa2ae4219e0df2a2cdb38e5d757` was reviewed against accepted
Protocol 6.4 control `55c085261eb827e3047637d045a8e6917ea6b962`. The binding/readiness descendants were
used only for lifecycle and mechanical evidence.

**SERIOUS CHALLENGE: NONE.** Accepted Protocol 6.5 D3 remains coherent and implementable.

One genuine D4 blocker survived fresh holdout falsification:

**B65-P17-1 — an owner-present invalid release-state transition can be laundered by a later material transition.**

P17 correctly closes B65-P16-1 by fully revalidating the exact predecessor candidate closure during accepted-current
promotion. However, predecessor discovery validates only the nearest differing material predecessor plus continuity of
owner presence behind it. An earlier owner-present transition can therefore violate protected temporal invariants,
be followed by a snapshot-valid later material transition, and disappear behind the selected predecessor boundary.

Fresh holdouts demonstrated the defect with protected historical mapping rewrite/deletion and same-version
accepted-current identity rewrite. In each case the malformed intermediate snapshot can remain internally coherent
while the later state validates against it; only the earlier temporal transition proves the rewrite illegal.

Required repair: preserve the existing immediate-predecessor semantics and exact-boundary P17 validation, but establish
semantic transition integrity behind every reachable governed predecessor so an earlier owner-present invalid transition
cannot be hidden by a later state. Reuse the existing canonical Git traversal and transition validator; add no release
registry, replay service, second state owner, or D3 redesign.

P17 remains immutable. This Review authorizes no stakeholder ratification, publication, recovery, accepted-current
cutover, PR merge, or Protocol 7 D3/D4 mutation.
