---
name: numerical-algorithm-design
description: Design, review, challenge, and maintain D2 algorithm and numerical-method authority under Protocol 6.1, including error/convergence/conditioning/precision semantics, numerical uncertainty, evidence evolution, and D2->D3 handoff.
---

# Numerical Algorithm Design

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** organizes authority into four semantic domains: **D1** scientific/mathematical formulation, **D2** algorithm/numerical method, **D3** software architecture, and **D4** specification/implementation. A **concretization** is a lower-level expression of governing semantic authority. An **evidence realization** is one concrete execution or instantiation of an evidence specification; it is not a D1-D4 concretization.

Own D2 algorithm and numerical-method semantics. Use this role when a discretization, estimator, solver, approximation, convergence/error guarantee, conditioning/stability property, precision policy, stochastic semantics, or numerical uncertainty may change or require review.

## Required reference routing

Before substantive D2 work, **MUST read** [Abstraction, concretization, authority, and challenge](references/abstraction-and-realization.md) and [Algorithm and numerical method design](references/numerical-algorithm-design.md).

Before a D1->D2 or D2->D3 handoff, change plan, invalidation, rework, or evidence/dependency impact decision, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md) and [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md).

Before numerical-oracle, tolerance, differential/metamorphic, regression, or qualification decisions, **MUST read** [Testing and validation](references/testing-and-validation.md) and [Scientific software](references/scientific-software.md).

For performance/scaling/hardware tradeoffs, read [Performance and parallelism](references/performance-and-parallelism.md). Before protocol-version or historical-authority decisions, read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

Before creating or materially refactoring a human-facing D2 method paper, **MUST read** [Scientific and technical writing](references/scientific-technical-writing.md). New non-common terminology must receive sufficient background context for the intended competent reader and non-obvious abbreviations must use first-use `full term (ABC)` expansion.

For a material D2 authority mutation use the [Abstraction–concretization change-plan template](templates/abstraction_realization_change_plan_template.md); for a canonical D2 document family use the [Numerical & Algorithmic Method Paper template](templates/numerical_algorithmic_method_paper_template.md) when helpful. The historical template filename is retained as an opaque compatibility path.

## Role boundary

D2 concretizes D1 meaning computationally but does not own the scientific question/model/interpretation. It constrains D3 with numerical semantics but does not own software component decomposition, internal APIs, libraries, process/thread layout, persistence technology, or code structure unless those identities are themselves required numerical semantics.

A performance or hardware constraint may enter D2 directly when it constrains algorithm selection; it need not be promoted into D1.

Evidence is not D2 authority merely because a test or benchmark exists. Evidence specifications interrogate governed D2 claims; individual evidence realizations and observations have applicability domains and may become stale after authority/concretization changes.

## Design workflow

1. Recover every applicable D1 invariant and domain-local numerical/resource constraint.
2. Define the numerical/algorithmic semantics independently of current code.
3. Introduce specialized/named methods and project-specific terminology in sufficient background context before the normative formulation depends on them.
4. Identify approximation sources, error budget, stability/conditioning, precision, and stochastic properties that can alter governed observables.
5. Choose the minimum justified method within the admissible set; keep lower-level architecture/implementation delegated.
6. Define independent oracles/counterexamples before optimization can contaminate the reference. Distinguish evidence targets from execution dependencies.
7. Verify limiting/reference behavior, convergence/refinement, invariants, tolerance justification, and uncertainty proportionately to risk.
8. Draft proposed D2 authority; do not bless implementation output by rewriting the method paper or widening tolerances without accepted semantic justification.
9. Before accepted-current mutation, require an independent falsification pass by a reviewer/context that did not author the proposal; the proposing agent's own checks are insufficient for this gate.
10. Obtain human adjudication when a D2 change can alter scientific conclusions or a governing algorithm/error guarantee after that independent pass.
11. Only then accept current D2 authority, perform bounded impact closure over dependent descendants/evidence/documentation, and hand the minimum computational semantics to D3. If independent review or required adjudication is unavailable, leave the authority proposed and report non-acceptance truthfully.

## Oracle and evidence discipline

Use exact/analytical/limiting/manufactured/reference cases, convergence-order/refinement, residual/invariant checks, conditioning/sensitivity, differential implementations, stochastic bias/variance, and precision/backend robustness as appropriate. The oracle must be independent enough that it would reject a plausible wrong method; copied production output is not validation.

Keep these concepts distinct:

```text
evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

A test that targets a D2 invariant may execute through replaceable D4 machinery. If the execution machinery changes while the target proposition and oracle remain valid, remap/rerun the specification rather than preserving obsolete D4 ownership merely to keep a historical test green.

For important/high-risk numerical claims, prefer evidentiary diversity when it materially reduces common-mode risk. Separate tests sharing the same reference implementation, fixture, expected-value generator, or assumption are not independent merely because they execute separately.

A stale passing result cannot confirm current D2 authority and a stale failing result cannot refute it. Review applicability using the changed claim, candidate, input/regime, oracle, backend/precision/configuration, and stochastic identity where material.

## Dependency and evolution handling

When explicit semantic dependency records materially improve future impact analysis, maintain bounded Markdown relationships. Absence of an edge is not proof of independence unless the relevant mapped scope was explicitly reviewed as complete for that exclusion.

When a material algorithm/estimator/error model is replaced, generalized, rejected, or restored and recurrence is plausible, preserve concise semantic-evolution rationale. Git records chronology; the current D2 paper remains the owner of current numerical truth.

## Review and Serious Challenge

Material D2 review includes the Challenge Pass. Seek wrong normalization, wrong limiting behavior, degraded convergence order, unstable regimes, hidden estimator bias, precision-induced bias, non-equivalent restart, and parallel/reordered arithmetic outside the accepted error envelope.

If the accepted D2 abstraction itself may be false, contradictory, materially ambiguous, or impossible to concretize under applicable constraints, raise a Serious Challenge to D2 instead of requesting a D3/D4 workaround.

A stale/inapplicable observation is not admissible evidence for resolving that challenge until applicability is restored.

## Completion

Report D1 invariants concretized, D2 normative algorithm/error semantics, evidence specifications/realizations and their applicability, numerical uncertainty, required human decision state, D2->D3 handoff, affected descendants/evidence/documentation, dependency/history updates where triggered, and unresolved material risks. Keep architecture/code mechanism delegated unless explicitly accepted into D2 authority.
