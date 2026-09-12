---
name: numerical-algorithm-design
description: Design, review, challenge, and maintain D2 algorithm/numerical-method authority under Protocol 6.3, including approximation, error/convergence/conditioning/precision/stochastic semantics, numerical uncertainty, evidence impact, and D2->D3 handoff.
---

# Numerical Algorithm Design

Own **D2 algorithm and numerical-method semantics**: discretization, estimator/solver/approximation, convergence/error/conditioning/stability, precision and stochastic behavior, and numerical uncertainty. D2 concretizes D1 but does not own scientific meaning; it constrains D3 without owning ordinary software decomposition.

## Routing

Before substantive D2 reasoning, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) and [Algorithm and numerical method design](references/numerical-algorithm-design.md).

Then load only triggered concerns:

- change plan, D1->D2/D2->D3 handoff, lifecycle/invalidation/impact closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- evidence applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); numerical oracle/tolerance/differential/metamorphic/qualification method -> [Testing and validation](references/testing-and-validation.md) and [Scientific software](references/scientific-software.md) when cross-domain scientific evidence is material;
- mature algorithm/method rework, substantial optimization/scaling, suspected recurrence, recovery/revert, or an active workplan whose decision can materially depend on demonstrated project history -> [Project Engineering Memory](references/project-engineering-memory.md); resolve the accepted/base memory plus any validated branch overlay and include every materially relevant family/capability/notice in the workplan/Historical Applicability Set (HAS), independent of memory temperature;
- scaling/resource/hardware tradeoff -> [Performance and parallelism](references/performance-and-parallelism.md);
- protocol-version/historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- human-facing D2 paper -> [Scientific and technical writing](references/scientific-technical-writing.md).

For material D2 authority mutation use [Abstraction-concretization change plan](templates/abstraction_concretization_change_plan_template.md). Use the [Numerical and Algorithmic Method Paper template](templates/numerical_algorithmic_method_paper_template.md) when useful.

Ordinary hyperlinks in routed references are navigation, not activation unless the current owner states an explicit predicate.

## D2 method

1. Recover every applicable D1 invariant and directly governed numerical/resource constraint.
2. Define algorithmic semantics independently of current code: approximation sources, error budget, stability/conditioning, precision/range, stochastic properties, ordering/reduction/restart/reproducibility when material.
3. Choose the minimum justified method inside the admissible set; delegate architecture/implementation identities not required by D2.
4. Define independent oracles/counterexamples before optimization contaminates the reference. Tolerances come from accepted error semantics, never from observing a failing backend.
5. Verify proportionately with exact/analytical/limiting/manufactured/reference cases, residuals/invariants, refinement/convergence order, sensitivity/conditioning, differential or metamorphic relations, stochastic bias/variance, and precision/backend robustness as applicable.
6. Distinguish evidentiary target from replaceable execution dependency; remap/rerun valid specifications when D4 machinery changes rather than preserving obsolete production ownership for a harness.
7. Draft proposed D2 authority. Material accepted-current mutation requires the owning acceptance process, including independent falsification and human adjudication when the change can alter scientific conclusions or a governing guarantee.
8. After acceptance, perform bounded impact closure over dependent D3/D4 concretizations, evidence, documentation/dependency views, and semantic history; preserve unaffected siblings/still-valid evidence.
9. Hand D3 the minimum computational semantics and resource/compatibility constraints it must preserve.

When creating/materially refactoring human-facing D2 prose, define newly introduced non-common terminology in background context and expand non-obvious abbreviations at first explanatory use.

## Evidence and Challenge

Evidence lifecycle/applicability/common-mode rules are owned by the evidence reference. A stale pass is not current confirmation and a stale fail is not current refutation. Tests sharing one expected-value generator, fixture, dataset defect, reference implementation or assumption are correlated even when separately executed.

Material D2 Review seeks wrong normalization/limits, degraded convergence, unstable regimes, hidden estimator bias, precision-induced bias, non-equivalent restart, or reordered/parallel arithmetic outside the accepted envelope. If accepted D2 itself may be false, contradictory, materially ambiguous, or impossible to concretize, raise **SERIOUS CHALLENGE** to D2 rather than asking D3/D4 to work around it.

## Completion

Report material D1 invariants concretized, D2 normative method/error/uncertainty semantics, evidence and applicability, required human state, D2->D3 handoff, affected descendants/documentation/dependencies/history, and unresolved blockers/Challenge. Keep architecture/code mechanisms delegated unless D2 authority actually requires them.
