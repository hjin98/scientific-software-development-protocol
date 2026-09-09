---
name: numerical-algorithm-design
description: Design, review, challenge, and maintain D2 algorithm and numerical-method authority under Protocol 6, including error/convergence/conditioning/precision semantics, numerical uncertainty, and D2->D3 handoff.
---

# Numerical Algorithm Design

Own D2 algorithm and numerical-method semantics. Use this role when a discretization, estimator, solver, approximation, convergence/error guarantee, conditioning/stability property, precision policy, stochastic semantics, or numerical uncertainty may change or require review.

## Required reference routing

Before substantive D2 work, **MUST read** [Abstraction, realization, authority, and challenge](references/abstraction-and-realization.md) and [Algorithm and numerical method design](references/numerical-algorithm-design.md).

Before a D1->D2 or D2->D3 handoff, change plan, invalidation, or rework decision, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).

Before numerical-oracle, tolerance, differential/metamorphic, regression, or qualification decisions, **MUST read** [Testing and validation](references/testing-and-validation.md) and [Scientific software](references/scientific-software.md).

For performance/scaling/hardware tradeoffs, read [Performance and parallelism](references/performance-and-parallelism.md). Before protocol-version or historical-authority decisions, read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

For a material D2 authority mutation use the [Abstraction–realization change-plan template](templates/abstraction_realization_change_plan_template.md); for a canonical D2 document family use the [Numerical & Algorithmic Method Paper template](templates/numerical_algorithmic_method_paper_template.md) when helpful.

## Role boundary

D2 realizes D1 meaning computationally but does not own the scientific question/model/interpretation. It constrains D3 with numerical semantics but does not own software component decomposition, internal APIs, libraries, process/thread layout, persistence technology, or code structure unless those identities are themselves required numerical semantics.

A performance or hardware constraint may enter D2 directly when it constrains algorithm selection; it need not be promoted into D1.

## Design workflow

1. Recover every applicable D1 invariant and domain-local numerical/resource constraint.
2. Define the numerical/algorithmic semantics independently of current code.
3. Identify approximation sources, error budget, stability/conditioning, precision, and stochastic properties that can alter governed observables.
4. Choose the minimum justified method within the admissible set; keep lower-level architecture/implementation delegated.
5. Define independent oracles/counterexamples before optimization can contaminate the reference.
6. Verify limiting/reference behavior, convergence/refinement, invariants, tolerance justification, and uncertainty proportionately to risk.
7. Draft proposed D2 authority; do not bless implementation output by rewriting the method paper or widening tolerances without accepted semantic justification.
8. Before accepted-current mutation, require an independent falsification pass by a reviewer/context that did not author the proposal; the proposing agent's own checks are insufficient for this gate.
9. Obtain human adjudication when a D2 change can alter scientific conclusions or a governing algorithm/error guarantee after that independent pass.
10. Only then accept current D2 authority, invalidate dependent descendants/evidence, and hand the minimum computational semantics to D3. If independent review or required adjudication is unavailable, leave the authority proposed and report non-acceptance truthfully.

## Oracle discipline

Use exact/analytical/limiting/manufactured/reference cases, convergence-order/refinement, residual/invariant checks, conditioning/sensitivity, differential implementations, stochastic bias/variance, and precision/backend robustness as appropriate. The oracle must be independent enough that it would reject a plausible wrong method; copied production output is not validation.

## Review and Serious Challenge

Material D2 review includes the Challenge Pass. Seek wrong normalization, wrong limiting behavior, degraded convergence order, unstable regimes, hidden estimator bias, precision-induced bias, non-equivalent restart, and parallel/reordered arithmetic outside the accepted error envelope.

If the accepted D2 abstraction itself may be false, contradictory, materially ambiguous, or unrealizable under applicable constraints, raise a Serious Challenge to D2 instead of requesting a D3/D4 workaround.

## Completion

Report D1 invariants realized, D2 normative algorithm/error semantics, verification evidence, numerical uncertainty, required human decision state, D2->D3 handoff, affected descendants, and unresolved material risks. Keep architecture/code mechanism delegated unless explicitly accepted into D2 authority.