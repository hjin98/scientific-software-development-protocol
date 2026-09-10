---
kind: abstraction-concretization-change-plan
protocol_version: REPLACE_WITH_SKILL_PROTOCOL_VERSION
status: proposed
---

# Abstraction–Concretization Change Plan

> Historical compatibility path: this template remains stored as `abstraction_realization_change_plan_template.md`; new Protocol 6.1 plans use abstraction/concretization terminology.

Use this lightweight template for a material D1->D2, D2->D3, or other abstraction->concretization change. D3->D4 executable work may use the implementation-workplan specialization instead. Omit sections that are genuinely immaterial; do not manufacture four-domain ceremony for a local change.

## Background and terminology

For a substantial human-facing plan that introduces non-common project/domain terminology, define it briefly here before later sections rely on it. State the intended competent reader or assumed prerequisites when needed. Expand non-obvious abbreviations at first explanatory use using `full term (ABC)`.

This section is explanatory and does not replace precise normative definitions owned by D1/D2/D3/D4.

## 1. Target outcome and authority

- Problem/stakeholder outcome:
- Highest potentially affected semantic domain:
- Applicable upstream accepted abstractions:
- Domain-local governed external constraints:
- Current normative authority owner(s):
- Proposed authority state and any required human-ratification state:

## 2. Invariants and delegated concretization

### Governing invariants

State the semantic claims that every admissible child concretization must preserve.

### Cycle-scoped child decisions

State only material decisions deliberately frozen for this concretization cycle. These are not durable domain authority unless separately accepted by the owning domain.

### Delegated concretization space

State what remains replaceable, reducible, consolidatable, or otherwise implementation/design-local.

### Non-goals

State nearby work intentionally excluded.

## 3. Abstraction adequacy and dependency surface

- What upstream semantics must remain expressible/verifiable in the child abstraction?
- Multi-parent/applicable authority relations:
- Material descendants/evidence that would become review-required or stale if this authority changes:
- Unaffected siblings/evidence explicitly expected to remain valid where useful:
- Is any explicit dependency view being used as proof of non-impact? If yes, is that bounded scope complete for the exclusion?

## 4. Evidence, verification, and falsification

- Reverse-semantic verification question at this boundary:
- Evidence specification(s) and governed target claim(s):
- Material execution dependencies/validity regime for those evidence specifications:
- Cheapest sufficiently strong oracles/counterexamples:
- External adequacy/validation/proof/standards evidence if this is a D1 boundary:
- Numerical error/convergence/conditioning/uncertainty evidence if this is a D2 boundary:
- Are multiple independent evidence routes warranted to reduce common-mode risk?
- Composed end-to-end closure required? If yes, define the observable chain.
- Challenge Pass: identify the strongest plausible contradiction or ambiguity to attempt to falsify.

## 5. Implementation / concretization sequence

Describe coherent dependent stages only where sequencing materially reduces risk. Prefer direct alteration/removal/consolidation before additive machinery when equivalent semantics survive.

## 6. Reopen, simplification, and human-adjudication triggers

- Earliest abstraction to reopen for each material failure class:
- Evidence that would invalidate a frozen premise:
- Structural complexity that would require simplification before another additive repair:
- Human decisions that cannot be self-approved:
- Any active Serious Challenge or explicit risk-override state:

## 7. Impact closure and historical reasoning

For a material accepted change, account proportionately for:

- affected descendant authority/concretizations;
- affected evidence specifications/realizations and rerun/remapping needs;
- affected documentation/current dependency view;
- required human re-ratification;
- retirement/cleanup of superseded machinery/tests;
- semantic-evolution history when the reason is likely to matter later.

Preserve unaffected siblings and still-valid evidence. Old green tests are not a substitute for impact closure.

## 8. Acceptance and handoff

A handoff closes only when concretization fidelity and child-abstraction adequacy both pass, required human decisions are resolved, materially dependent stale/review-required authority/evidence is reconciled, bounded impact closure is complete, and the accepted current authority state is unambiguous. Do not convert missing or stale evidence into a Pass.
