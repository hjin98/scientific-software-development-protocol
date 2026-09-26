---
name: numerical-algorithm-design
description: Use to choose, design, review, or challenge a numerical method or algorithm - discretization, solver, estimator, error/convergence/stability, precision, stochastic behavior, and tolerances derived from the error model. Not for code changes that keep the method.
---

# Numerical Algorithm Design

Own **D2 algorithm and numerical-method semantics**: discretization, estimator/solver/approximation, convergence/error/conditioning/stability, precision and stochastic behavior, and numerical uncertainty. D2 concretizes D1 but does not own scientific meaning; it constrains D3 without owning ordinary software decomposition.

**Version entry check.** This package is SSDP `REPLACE_WITH_SKILL_PROTOCOL_VERSION`. If the task or its governing workplan declares a different SSDP `protocol_version`, say so and resolve that version's compatible source before protocol-dependent reasoning ([Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md)); never apply this package's doctrine to other-version work. No declared version: continue.

## Routing

Before substantive D2 reasoning, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) (the universal kernel) and [Algorithm and numerical method design](references/numerical-algorithm-design.md).

Then load only triggered concerns:

- change plan, D1->D2/D2->D3 handoff, working state, authority lifecycle/invalidation/impact closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- a specialized operator/estimator/recurrence/stochastic object, parameter family/instance/default binding, imported theorem/result with hypotheses, formal claim/warrant, or definition-dependency impact -> [Semantic definition and traceability](references/semantic-definition-and-traceability.md);
- evidence applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); numerical oracle/tolerance/differential/metamorphic/qualification method -> [Testing and validation](references/testing-and-validation.md) and [Scientific software](references/scientific-software.md) when cross-domain scientific evidence is material;
- project history can change the decision (mature method rework, substantial optimization/scaling, suspected recurrence, recovery/revert, memory-bound workplan) -> [Project Engineering Memory](references/project-engineering-memory.md);
- recurrence, rigor or cognitive-resource escalation -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md); scaling/resource/hardware tradeoff -> [Performance and parallelism](references/performance-and-parallelism.md);
- protocol-version mismatch or historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- human-facing D2 paper -> [Scientific and technical writing](references/scientific-technical-writing.md).

For material D2 authority mutation use the [Abstraction-concretization change plan](templates/abstraction_concretization_change_plan_template.md); use the [Numerical and Algorithmic Method Paper template](templates/numerical_algorithmic_method_paper_template.md) when useful. An in-envelope local tolerance question loads none of the conditional owners merely because they exist; ordinary hyperlinks and package membership are not activation commands.

## D2 contract

1. Recover every applicable D1 invariant and directly governed numerical/resource constraint.
2. Define algorithmic semantics independently of current code: approximation sources, error budget, stability/conditioning, precision/range, stochastic properties, ordering/reduction/restart/reproducibility when material.
3. Choose the minimum justified method inside the admissible set; delegate architecture/implementation identities not required by D2.
4. Define independent oracles/counterexamples before optimization contaminates the reference. Tolerances come from accepted error semantics, never from observing a failing backend.
5. Verify proportionately: first bound whether numerical uncertainty can change the governed decision, then use the cheapest sufficiently strong applicable exact/analytical/limiting/manufactured/reference, residual/invariant, convergence, conditioning, stochastic, precision/backend, differential or metamorphic evidence. Do not turn an in-envelope local tolerance into a research campaign.
6. Distinguish evidentiary target from replaceable execution dependency; remap/rerun valid specifications when D4 machinery changes.
7. Draft proposed D2 authority. Accepted-current mutation requires the owning acceptance process, including independent falsification and human adjudication when the change can alter scientific conclusions or a governing guarantee; afterwards perform bounded impact closure and hand D3 the minimum computational semantics and resource/compatibility constraints it must preserve.

When creating human-facing D2 prose, define newly introduced non-common terminology in background context and expand non-obvious abbreviations at first explanatory use.

## Evidence and Challenge

A stale pass is not current confirmation and a stale fail is not current refutation. Tests sharing one expected-value generator, fixture, dataset defect, reference implementation or assumption are correlated even when separately executed.

Material D2 Review seeks wrong normalization/limits, degraded convergence, unstable regimes, hidden estimator bias, precision-induced bias, non-equivalent restart, or reordered/parallel arithmetic outside the accepted envelope. If accepted D2 itself may be false, contradictory, materially ambiguous, or impossible to concretize, raise **SERIOUS CHALLENGE** to D2 rather than asking D3/D4 to work around it.

## Completion

Report material D1 invariants concretized, D2 normative method/error/uncertainty semantics, evidence and applicability, required human state, D2->D3 handoff, affected descendants/documentation/dependencies/history, and unresolved blockers/Challenge. Keep architecture/code mechanisms delegated unless D2 authority actually requires them.
