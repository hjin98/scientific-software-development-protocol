---
kind: ssdp65-p18-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p17: feca003e577fdfa2ae4219e0df2a2cdb38e5d757
p18: a2e5f01e258f249f74d1eda74b883efb98fd7d59
exact_p18_pr_run: 36179328663
date: 2026-09-25
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P18 Governed-History Integrity Qualification

P18 is the immutable replacement semantic candidate:

`a2e5f01e258f249f74d1eda74b883efb98fd7d59`

Exact-P18 workflow `36179328663` passed the complete repository build and Orchestrator Core jobs under the restored
canonical workflow.

## Repaired blocker

P18 closes B65-P17-1 at the existing D4 release-state transition owner.

The existing canonical governed-history traversal now retains each readable owner state, rejects owner deletion as
before, and additionally applies the existing pure `validate_release_transition()` contract to every owner-present
material parent -> child edge in reachable canonical ancestry. Genuine pre-owner ancestry remains exempt. The existing
nearest-material-predecessor resolver and P17 exact-boundary predecessor snapshot/evidence validation remain intact.

This closes the laundering trajectory:

`valid A -> owner-present illegal B -> later material C`

because the A -> B violation is now detected even when nearest-predecessor selection for C returns only B.

Focused regressions cover hidden protected-history rewrite, hidden accepted-current identity rewrite, multiple legal
owner-present transitions, and merge-parent behavior under the strengthened invariant. The pre-existing reordered-merge
fixture was corrected to expect discovery-time detection of its deliberately invalid governed edge rather than treating
that edge as diagnostically silent.

## Qualification convergence

Several intermediate implementation/diagnostic descendants were intentionally **not frozen**. They exposed and
isolated a stale regression expectation specific to `unittest discover`. All temporary workflow instrumentation was
removed before P18. Exact P18 `a2e5f01e258f249f74d1eda74b883efb98fd7d59` restores the canonical workflow byte-for-byte and passes the complete
normal workflow at run `36179328663`.

No D1, D2, or D3 authority changed. No new state owner, registry, replay engine, topology service, compatibility layer,
or Protocol 7 machinery was introduced.

P18 requires a later lifecycle binding at Review `NOT_RUN`, mechanical binding qualification, and a genuinely fresh
independent assembled-candidate Review before any stakeholder ratification or release publication.
