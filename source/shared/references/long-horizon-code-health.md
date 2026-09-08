# Long-Horizon Code Health and Autonomous Quality

Long-horizon quality protects the minimum justified realization over time. It does not create new scientific/product truth, extra approval roles, or a numeric definition of quality.

```text
accepted D1-D4 authority
 -> realization + executable/scientific evidence
 -> independent review / risk-triggered verification
 -> structural and oracle-strength signals
 -> stabilization / longitudinal health sensing
 -> bounded simplification or earliest-domain reconsideration
```

## Quality ratchet

Existing debt does not justify making a materially touched surface harder to reason about, more cyclic, more duplicated in authority, more weakly protected, or more dependent on exceptions without a governing reason.

For substantial/structurally risky work capture only the task-local before-state needed for meaningful comparison. Do not create a permanent health ledger solely for compliance.

## Metrics are sensors, not verdicts

Complexity, CRAP-like measures, churn, temporal change coupling, **architectural centrality**/cycles, duplication, coverage, mutation survival, public/configuration growth, and related metrics can identify risk concentration. They do not independently prove correctness or require refactoring.

A useful qualitative model is:

```text
maintenance risk ~ change frequency x structural complexity x test weakness x architectural centrality
```

No universal threshold is normative. Metrics are sensors; investigate the semantic reason behind the signal before acting.

## Test effectiveness and oracle strength

For important decision logic/high-risk changed code, ask what plausible wrong behavior could still pass. Strengthen evidence with counterfactual/mutation, property/stateful, differential/metamorphic, reference, or real-owner integration when economical. The semantic claim decides whether a surviving mutant matters.

Mutation testing is conditional. Surviving mutants are investigation evidence; they may reflect weak assertions, untested decisions, dead/equivalent code, or ambiguous requirements. **Do not require 100% mutation** scores or optimize tests for a score rather than product/domain behavior.

Scientific/numerical relations come from D1/D2 authority, not from test convenience.

## Executable architecture fitness

Objective stable D3 rules may be executable: dependency direction, acyclicity, independence, or absence/uniqueness of a retired owner. Do not build a universal architecture model just to obtain a score.

## Review

Independent Review reconstructs the applicable current authority and actual realization, then attempts falsification. Prefer fresh operational context for substantial/high-risk work when practical.

Every material review/verification boundary includes the bounded Challenge Pass. Review must distinguish an ordinary child nonconformance from evidence that accepted authority itself is false, contradictory, inadequate, materially ambiguous, or unrealizable. The latter is a Serious Challenge routed to the earliest affected owner/human adjudicator.

Review readiness normally includes final accepted-contract reconciliation, final affected-surface regression, real-boundary integration, repository/project-required checks, and required structural/liveness evidence. A requested review still proceeds if evidence is missing but records that missing evidence as a blocker.

## Verification

Verification is a deeper optional **risk-triggered** falsification mode for materially high-risk scientific, numerical, architecture, or implementation claims. It may reconcile authorities, construct counterexamples, compare reference methods, inspect failure paths, or trace composed D4->D1 behavior. It is not a routine duplicate Review.

## Stabilization / architecture GC

At a material convergence boundary after ordinary review otherwise passes, ask:

> If this realization appeared fully formed today, would we deliberately choose it again for the same governing authority?

Inspect duplicate representations, competing authorities, wrappers/adapters/fallbacks/special cases, stale compatibility, unnecessary state/config/public API, ownership leakage, dependency cycles, historical-exception conditionals, dead/bypassed paths, duplicated algorithms, and tests dominated by internal orchestration.

Stabilization is **non-mutating**. Required changes return through the **normal Design**/Implementation/acceptance/Review path at the owning domain rather than being silently edited during stabilization. If D4 machinery can be simplified under unchanged D3, keep it D4. If D3 architecture must change, reopen D3 through Software Design. If evidence shows D2/D1 is the problem, route further upstream rather than architecture-patching it.

## Health Audit

A periodic Health Audit combines current semantic inspection with available history such as churn, change coupling, recurring defect families, complexity, dependency centrality/cycles, public/configuration growth, test weakness, and documentation difficulty.

Do not fabricate trends when history is unavailable. Audit findings route work but do not mutate D1-D4 authority.

## Failure-path evidence

For persistence/restart/orchestration/cancellation/failure propagation, use bounded deterministic fault injection where it materially strengthens evidence while keeping the real semantic owner live. Prefer controlled failpoints to resource exhaustion or indiscriminate chaos.

## Closeout

At substantial workplan/release completion reconcile current documentation, generated artifacts, completed/superseded workplan state, and conservative repository hygiene. Closeout does not mutate product semantics and must not archive authority whose semantics have not yet been consolidated into current canonical owners.
