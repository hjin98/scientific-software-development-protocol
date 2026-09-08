---
kind: abstraction-realization-change-plan
protocol_version: REPLACE_WITH_SKILL_PROTOCOL_VERSION
status: proposed
---

# Abstraction–Realization Change Plan

Use this lightweight template for a material D1->D2, D2->D3, or other abstraction->realization change. D3->D4 executable work may use the implementation-workplan specialization instead. Omit sections that are genuinely immaterial; do not manufacture four-domain ceremony for a local change.

## 1. Target outcome and authority

- Problem/stakeholder outcome:
- Highest potentially affected semantic domain:
- Applicable upstream accepted abstractions:
- Domain-local governed external constraints:
- Current normative authority owner(s):
- Proposed authority state and any required human-ratification state:

## 2. Invariants and delegated realization

### Governing invariants

State the semantic claims that every admissible child realization must preserve.

### Cycle-scoped child decisions

State only material decisions deliberately frozen for this realization cycle. These are not durable domain authority unless separately accepted by the owning domain.

### Delegated realization space

State what remains replaceable, reducible, consolidatable, or otherwise implementation/design-local.

### Non-goals

State nearby work intentionally excluded.

## 3. Abstraction adequacy and dependency surface

- What upstream semantics must remain expressible/verifiable in the child abstraction?
- Multi-parent/applicable authority relations:
- Material descendants/evidence that would become stale if this authority changes:
- Unaffected siblings/evidence explicitly expected to remain valid where useful:

## 4. Verification and falsification

- Reverse-semantic verification question at this boundary:
- Cheapest sufficiently strong oracles/counterexamples:
- External adequacy/validation/proof/standards evidence if this is a D1 boundary:
- Numerical error/convergence/conditioning/uncertainty evidence if this is a D2 boundary:
- Composed end-to-end closure required? If yes, define the observable chain.
- Challenge Pass: identify the strongest plausible contradiction or ambiguity to attempt to falsify.

## 5. Implementation / realization sequence

Describe coherent dependent stages only where sequencing materially reduces risk. Prefer direct alteration/removal/consolidation before additive machinery when equivalent semantics survive.

## 6. Reopen, simplification, and human-adjudication triggers

- Earliest abstraction to reopen for each material failure class:
- Evidence that would invalidate a frozen premise:
- Structural complexity that would require simplification before another additive repair:
- Human decisions that cannot be self-approved:
- Any active Serious Challenge or explicit risk-override state:

## 7. Acceptance and handoff

A handoff closes only when realization fidelity and child-abstraction adequacy both pass, required human decisions are resolved, dependent stale authority/evidence is identified, and the accepted current authority state is unambiguous. Do not convert missing evidence into a Pass.