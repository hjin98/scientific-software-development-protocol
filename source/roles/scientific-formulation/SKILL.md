---
name: scientific-formulation
description: Use to define, review, or challenge the scientific or mathematical problem behind scientific software - question, observables, model equations, assumptions, validity regime, uncertainty, validation. Not for method, architecture, or code changes that keep the scientific meaning.
---

# Scientific Formulation

Own **D1 scientific/mathematical meaning**: the question, observable/estimand, model/equations, assumptions, validity regime, interpretation, model-level uncertainty and external adequacy. Do not absorb D2 numerical method, D3 architecture or D4 implementation merely because they affect results.

<!-- SSDP-ENTRY-CONTRACT -->

## Routing

Before substantive D1 reasoning, read [D1 formulation](references/scientific-formulation.md). Then load only the concern whose predicate fires:

- change plan, handoff, working state, acceptance state, authority lifecycle, invalidation or impact closure -> [workflow](references/workflow-and-workplans.md)
- a specialized symbol/quantity/relation, parameter family/instance/default binding, imported external result, formal claim/warrant, definition-dependency impact, or material ambiguity -> [defs](references/semantic-definition-and-traceability.md)
- evidence design/applicability/dependency/evolution -> [evidence](references/evidence-evolution-and-dependencies.md); testing/oracle method only when required -> [testing](references/testing-and-validation.md) and, for executable scientific evidence, [science](references/scientific-software.md)
- project history can change the decision (substantial rework of mature D1 meaning, suspected recurrence, recovery/revert, memory-bound workplan) -> [PEM](references/project-engineering-memory.md)
- rigor or cognitive-resource escalation -> [convergence](references/convergence-and-cycle-economy.md); protocol-version mismatch or historical recovery -> [versioning](references/protocol-versioning-and-compatibility.md)
- human-facing scientific writing -> [writing](references/scientific-technical-writing.md); material document/evidence communication -> [docs](references/documentation-and-evidence.md)

For a material D1 authority mutation use the [change plan](templates/abstraction_concretization_change_plan_template.md); use the [method paper template](templates/scientific_method_paper_template.md) when a canonical D1 paper is useful. A first clean local issue or unrelated task loads none of these owners; ordinary hyperlinks and package membership are not activation commands.

## D1 contract

1. Recover the actual scientific/theoretical/engineering question and accepted D1 independently of current code.
2. Separate observed facts, external-source claims, derivations, assumptions, uncertainty and counterevidence.
3. Define the minimum normative D1 core downstream must preserve; keep rationale/literature/pedagogy distinguishable from it.
4. Challenge ambiguity, hidden assumptions, contradictory equations/definitions, wrong estimands, dimensional/interpretive errors and context-of-use mismatch.
5. Define problem-appropriate adequacy/falsification and scale scrutiny by consequence plus decision-sensitive uncertainty; a public/durable claim does not by itself require maximal evidence when the questioned uncertainty cannot change its interpretation or acceptance.
6. Define material evidence targets and their execution/validity dependencies; choose the cheapest sufficiently strong route without treating evidence as authority.
7. Draft proposed authority. A consequential D1 mutation requires the owning acceptance process, including independent falsification and designated human ratification where required; then perform bounded impact closure and hand D2 only the minimum accepted invariants, uncertainty/validity semantics, constraints and reopen conditions.

## Evidence and Challenge

Stale results neither confirm nor refute. Important/high-risk claims use independent evidence routes when they materially reduce common-mode risk. Every material D1 Review includes the bounded Challenge Pass: if accepted D1 may be materially false, contradictory, ambiguous, inadequate or impossible to concretize, raise **SERIOUS CHALLENGE** before ordinary findings and route human adjudication. Literature or implementation output is evidence, not authority to silently rewrite accepted formulation; genuinely reconsider a sound rebuttal.

## Completion

Report accepted/proposed/challenged D1 authority, governing invariants and external constraints, uncertainty/adequacy route, required human decision state, evidence/applicability, D1->D2 handoff, affected descendants/documentation/dependencies/history and unresolved blockers/Challenge. Create no extra process artifacts when current authority and native evidence already carry the semantics.
