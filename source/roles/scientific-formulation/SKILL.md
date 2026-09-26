---
name: scientific-formulation
description: Use for defining, reviewing, or challenging the scientific or mathematical problem behind scientific software - the question, observables/estimands, model equations, assumptions, validity regime, interpretation, model-level uncertainty, and external validation - and for its handoff to numerical-method design. Not for numerical method, architecture, or code work that leaves the scientific meaning unchanged.
---

# Scientific Formulation

Own **D1 scientific/mathematical meaning**: the question, observable/estimand, model/equations, assumptions, validity regime, interpretation, model-level uncertainty, and external adequacy. Do not absorb D2 numerical method, D3 architecture, or D4 implementation merely because they affect results.

## Routing

Before substantive D1 reasoning, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) (the universal kernel, including the version check at entry) and [Scientific and mathematical formulation](references/scientific-formulation.md).

Then load only the concern whose predicate fires:

- change plan, handoff, working state, acceptance state, authority lifecycle, invalidation or impact closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- a specialized symbol/quantity/relation, parameter family/instance/default binding, imported external result, formal claim/warrant, definition-dependency impact, or material ambiguity -> [Semantic definition and traceability](references/semantic-definition-and-traceability.md);
- evidence design/applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); testing/oracle method only when required -> [Testing and validation](references/testing-and-validation.md) and, for executable scientific evidence, [Scientific software](references/scientific-software.md);
- project history can change the decision (substantial rework of mature D1 meaning, suspected recurrence, recovery/revert, memory-bound workplan) -> [Project Engineering Memory](references/project-engineering-memory.md);
- rigor or cognitive-resource escalation -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md);
- protocol-version mismatch or historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- human-facing scientific writing -> [Scientific and technical writing](references/scientific-technical-writing.md); document/evidence communication when material -> [Documentation and evidence](references/documentation-and-evidence.md).

For a material D1 authority mutation use the [Abstraction-concretization change plan](templates/abstraction_concretization_change_plan_template.md); use the [Scientific Method Paper template](templates/scientific_method_paper_template.md) when a canonical D1 paper is useful. A first clean local issue or unrelated task loads none of the conditional owners merely because they exist; ordinary hyperlinks and package membership are not activation commands.

## D1 contract

1. Recover the actual scientific/theoretical/engineering question and accepted current D1 independently of current code.
2. Separate observed facts, external-source claims, derivations, assumptions, uncertainty, and counterevidence.
3. Define the minimum normative D1 semantic core downstream must preserve; keep rationale/literature/pedagogy distinguishable from that core.
4. Challenge ambiguity, hidden assumptions, contradictory equations/definitions, wrong estimands, dimensional/interpretive errors, and context-of-use mismatch.
5. Define problem-appropriate adequacy/falsification and allocate scrutiny by consequence plus decision-sensitive uncertainty; a public/durable claim does not by itself require maximal evidence when the questioned uncertainty cannot change its interpretation or acceptance.
6. Define material evidence targets and their execution/validity dependencies; choose the cheapest sufficiently strong applicable route without treating evidence as authority.
7. Draft proposed authority. A consequential D1 mutation requires the owning acceptance process, including independent falsification and designated human ratification where required; afterwards perform bounded impact closure and hand D2 only the minimum accepted invariants, uncertainty/validity semantics, constraints, and reopen conditions.

When creating human-facing D1 material, give the intended competent reader sufficient background for newly introduced non-common terminology and expand non-obvious abbreviations at first explanatory use (`full term (ABC)`). Explanatory context never silently redefines the normative D1 owner.

## Evidence and Challenge

A stale pass is not current confirmation; a stale fail is not current refutation. Important/high-risk claims should use independent evidence routes when they materially reduce common-mode risk.

Every material D1 Review includes the bounded Challenge Pass. If accepted D1 may be materially false, contradictory, ambiguous, inadequate, or impossible to concretize, raise **SERIOUS CHALLENGE** before ordinary findings and route human adjudication. Literature or implementation output is evidence, not authority to silently rewrite accepted formulation. A sound rebuttal must be genuinely reconsidered.

## Completion

Report only material decision state: accepted/proposed/challenged D1 authority, governing invariants and external constraints, uncertainty/adequacy route, required human decision state, evidence/applicability, D1->D2 handoff, affected descendants/documentation/dependencies/history, and unresolved blockers/Challenge. Do not create extra process artifacts when existing current authority and native evidence already carry the semantics.
