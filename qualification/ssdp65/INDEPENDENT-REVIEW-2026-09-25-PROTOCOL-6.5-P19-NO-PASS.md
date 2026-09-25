---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: b38f2525677888956c4802afd758c98c65b79f1c
semantic_ref: b38f2525677888956c4802afd758c98c65b79f1c
binding_descendant: d4bfb9032612395ed3d5dbff462acb86ed538944
readiness_descendant: fb37f25aa2c099ddfdfc664ff76a162b0b3a1e9a
exact_candidate_run: 36195532806
binding_run: 36195685076
readiness_run: 36195854459
serious_challenge: none
blocking_findings:
  - B65-P19-1
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P19

## Disposition

**NO-PASS.**

Exact immutable P19 `b38f2525677888956c4802afd758c98c65b79f1c` was reviewed against accepted
Protocol 6.4 control `55c085261eb827e3047637d045a8e6917ea6b962`. Binding/readiness descendants were used
only for lifecycle and mechanical evidence.

**SERIOUS CHALLENGE: NONE.** The proportional-rigor doctrine is coherent and implementable; no D1, D2, or D3 reopen is justified.

## Blocking finding

**B65-P19-1 — historical accepted-current promotion can lose P17's exact predecessor evidence revalidation behind a later material transition.**

P17 repaired B65-P16-1 by requiring accepted-current advancement to revalidate the complete exact predecessor release-state snapshot, including Review/ratification evidence realization and publication/recovery lineage at the predecessor boundary.

P18 repaired B65-P17-1 by walking governed release-state history and applying `validate_release_transition()` to each owner-present material parent -> child edge. P19 preserves that implementation.

The protections do not fully compose. `_governed_owner_history_is_continuous()` calls:

`validate_release_transition(parent_state, state)`

without `repo_root` or the exact parent ref. For accepted-current advancement, `validate_release_transition()` performs P17's complete predecessor revalidation only when `repo_root is not None`. Therefore an earlier predecessor with PASS/RATIFIED labels but forged or wrong-subject evidence can be structurally promoted and later hidden after another material transition.

Fresh cross-generation holdout:

`valid A -> invalid promotion B -> later material C`

At C, current-state validation no longer inspects A as the current candidate; nearest-predecessor validation sees B; and full-history traversal reaches A -> B but skips P17's repository-backed evidence realization because the historical transition call omits the exact repository boundary.

This is a genuine D4 release-integrity blocker.

## Minimal repair contract

Keep D1-D3 and proportional-rigor doctrine closed.

At the existing D4 release-state owner, preserve the exact historical parent ref and invoke the existing transition validator with repository realization for every differing owner-present edge, equivalent to:

`validate_release_transition(parent_state, child_state, repo_root=root, previous_ref=parent_ref)`.

Add focused regression proving that a wrong-subject Review/ratification promotion source cannot be hidden behind one later material transition. Preserve legal multi-transition, owner deletion/reintroduction, protected-history rewrite, merge-parent, canonical-Git, missing-object, and exact-boundary behavior.

Do not add a registry, replay engine, evidence database, second state owner, topology service, compatibility layer, or lifecycle role.

Because the repair changes governed D4 release-validation semantics, freeze a new immutable semantic candidate after exact-candidate qualification and perform another fresh independent assembled-candidate Review.

## Other reviewed surfaces

The proportional-rigor doctrine passed independent falsification for mandatory low-salience obligations, uncertain importance, no automatic parent-to-child priority inheritance, action priority versus importance, evidence applicability/recursion stopping, fixture/oracle versus owner defects, same-semantic-candidate evidence-only requalification, D1/D2 decision-sensitive rigor, reviewer independence, external blockers, sunk-cost/rediscovery behavior, and documentation persistence.

Exact P19, binding, and readiness workflows passed their complete build/Core jobs. Frozen 5.16-6.4 profile/prompt resources remain unchanged P0 -> P19; source/generated package parity is intact; documentation closeout is present; Protocol 7 D3/D4 is unchanged.

P19 remains immutable. This Review authorizes no stakeholder ratification, public fallback, recovery, accepted-current cutover, PR #33 merge, or Protocol 7 mutation.
