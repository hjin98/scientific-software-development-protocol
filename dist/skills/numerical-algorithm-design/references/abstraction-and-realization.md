# Abstraction, Realization, Authority, and Challenge

Protocol 6 governs scientific-software development through one recursive relation:

```text
ABSTRACTION  --design / constrain-->  REALIZATION
ABSTRACTION  <--verify / reconstruct-- REALIZATION
```

An abstraction is an intentionally incomplete but normative semantic contract. It states the material invariants, required outcomes, assumptions, validity conditions, observables, bounds, and governed relations that every admissible realization must preserve. A realization is the lower-level scientific, numerical, architectural, or implementation choice that satisfies those semantics.

## Feasibility before optimization

For a realization `R` constrained by applicable upstream abstractions `A1 ... An` and domain-local governed constraints `C`:

```text
semantics(R) |= I(A1) AND ... AND I(An) AND C
```

Fidelity is a feasibility condition, not a weighted objective. Among admissible realizations prefer, in order:

```text
domain engineering fitness
> minimum justified realization complexity
> development economy
```

This is a bounded engineering search rule, not a demand for exhaustive global optimization. Stop when further search has lower expected engineering value than proceeding with the best justified admissible realization.

## Authority source is orthogonal to abstraction level

D1-D4 describe semantic level. They do not determine where authority originated. Preserve this precedence:

```text
safety / explicit stakeholder and project authority / governed external contracts
    -> accepted current domain abstractions and ratified decisions
    -> repository/runtime evidence about actual realization state
    -> delegated realization discretion
```

A security, reliability, performance, compatibility, hardware, regulatory, or public-contract constraint may enter directly at D2, D3, or D4. Do not force every external requirement through D1 merely to make the hierarchy linear.

Each material claim has one current normative semantic owner, but a realization may be constrained by many applicable authorities simultaneously. If applicable authorities conflict materially, do not silently choose one; surface the conflict for adjudication.

## Four semantic domains

The scientific-software specialization is:

- **D1 — Scientific & Mathematical Formulation:** the scientific question, observables/estimands, governing model/equations, assumptions, validity regime, interpretation, and external adequacy semantics. Owned by `scientific-formulation`.
- **D2 — Algorithm & Numerical Methods:** numerical/discrete/stochastic realization, approximation/error/convergence/conditioning/precision semantics, algorithmic guarantees, and numerical uncertainty. Owned by `numerical-algorithm-design`.
- **D3 — Software Architecture:** component ownership, data/control flow, interfaces, persistence/concurrency/resource/security/deployment architecture, and cycle-scoped architectural decisions. Owned by `software-design`.
- **D4 — Specification & Implementation:** accepted concrete software contract plus code/executable behavior, tests, packaging, and operational realization. Implemented by `software-implementation`; the accepted specification remains normative where one exists and code is evidence of actual realization.

The four levels form a layered DAG, not necessarily one linear chain. Shared algorithms, shared architecture, alternative realizations, and multi-parent constraints are valid. Current normative ownership must remain acyclic so authority can be resolved independently.

## Invariant versus delegated realization

At every boundary ask:

> Is this property required by the abstraction or an applicable governed constraint, or is it merely one way the current realization satisfies them?

A lower-level detail does not acquire authority because it exists, is depended upon, is tested, is documented, survived review, appears in a previous workplan, or is convenient to verify. Promote a realization property into an abstraction only through explicit acceptance by that abstraction's owning authority and for a material semantic reason.

When solution-created machinery causes its own intermediate problems, prefer removing, narrowing, altering, consolidating, re-deriving, or replacing that machinery before adding another durable repair. Never simplify by weakening a governing abstraction.

## Design and reverse semantic verification

Design is normally one-to-many:

```text
A -> {R | R satisfies A and applicable C}
```

Verification therefore is not a mathematical inverse. It operates in the opposite semantic direction:

```text
actual realization
 -> reconstruct/project material semantics
 -> compare with every applicable parent and side constraint
 -> attempt to falsify conformity
```

Every material handoff asks two different questions:

1. **Realization fidelity:** does the child realize its governing parents correctly?
2. **Abstraction adequacy:** is the child abstraction strong and complete enough to preserve the material upstream meaning for the next realization?

A realization can perfectly satisfy a too-weak abstraction and still be wrong. Such abstraction inadequacy is an upstream design defect, not a successful handoff.

## Current, proposed, challenged, stale, and historical authority

Normative artifacts must distinguish lifecycle state sufficiently to prevent speculative edits from becoming authority accidentally. Projects may use their own metadata syntax, but the semantic states are:

- **proposed** — candidate authority; not yet governing;
- **accepted current** — current normative semantic owner for its claim scope;
- **challenged** — accepted current authority whose correctness is under a material unresolved challenge; still the explicit baseline, but dependent closure is blocked unless a visible human risk override applies;
- **stale dependent** — downstream authority/evidence invalidated by an accepted upstream change;
- **superseded/historical** — no longer current but retained for history;
- **release-pinned/publication snapshot** — immutable historical representation of a specific release/publication context.

Human-ratification state is orthogonal: `not-required`, `required-pending`, `accepted`, or `rejected` (exact syntax delegated).

Accepted-current authority changes atomically:

```text
propose
 -> independent review/falsification
 -> required human ratification
 -> accept new authority
 -> update canonical current owner
 -> mark only dependent descendants/evidence stale
 -> realize downward
 -> verify upward
```

Do not mutate current normative documents speculatively and then treat the edit as authority merely because it exists in the repository.

## Bounded dependency tracing and invalidation

Represent only material semantic dependencies needed for realization, impact analysis, invalidation, or verification. Section anchors, document links, workplan mappings, and profile metadata are normally sufficient; Protocol 6 does not require a universal claim graph or database.

Accepted upstream change invalidates only descendants/evidence whose claim could materially change. Preserve unaffected siblings and still-valid evidence. Reopen the earliest/highest materially affected abstraction, not every higher domain and not merely the lowest file where the contradiction became visible.

Typical routing:

```text
helper/data-structure/serialization defect                -> D4
component ownership/data-flow/state/deployment defect     -> D3
discretization/solver/estimator/precision defect          -> D2
observable/model/equation/assumption/meaning defect       -> D1
model/context/evidence mismatch                           -> D1 external adequacy
```

A D4-only or D3-only claim needs only a proportionate upstream-impact exclusion when there is plausible scientific/numerical risk. Do not force unaffected projects through four documents or four stages.

## Composed closure

Adjacent pairwise checks are insufficient when a material end-to-end claim can fail through an omitted intermediate invariant. For high-risk scientific/numerical claims, trace the assembled result across the affected path:

```text
actual D4 executable behavior
 -> governed numerical observables
 -> D2 error/equivalence envelope
 -> D1 scientific/mathematical meaning
 -> problem-appropriate external adequacy / validation / proof / standards evidence
```

Pairwise verification and composed closure complement one another. External adequacy is not internal verification: empirical problems may require validation against reality/context; mathematical problems may require proof/reference theory; engineering problems may require standards, qualification experiments, safety margins, or stakeholder context.

Uncertainty is layer-aware. D1 owns model/data/parameter/assumption/model-discrepancy uncertainty. D2 owns discretization/truncation/stochastic/conditioning/floating-point uncertainty and its propagation into D1 observables.

## Mandatory bounded Challenge Pass

Every material review or verification/acceptance boundary includes a bounded adversarial Challenge Pass before normal closure. Ask whether governing authority is internally consistent, sufficiently unambiguous, jointly realizable under all constraints, logically/mathematically coherent, adequate for its problem, complete enough to preserve upstream semantics, compatible with simultaneous authorities, and free from a known material counterexample.

For tiny low-risk work this may be implicit and brief. It is not a mandatory standalone stage or checklist.

Raise a **Serious Challenge** only for a material potential defect in accepted authority, such as:

- unrealizable or contradictory invariants;
- material ambiguity that admits incompatible semantics;
- logical/mathematical fallacy or counterexample;
- scientific/model contradiction;
- abstraction inadequacy that permits high-integrity wrongness;
- genuine conflict among applicable authorities;
- a major conceptual decomposition that solves the wrong problem;
- a requirement to counterfeit closure by hiding or weakening contradictory evidence.

Ordinary realization nonconformance under a coherent parent remains an ordinary blocker.

An active Serious Challenge must be prominent before ordinary blockers or Pass/No-Pass language, using an equivalent of:

```text
SERIOUS CHALLENGE — BLOCKED PENDING HUMAN ADJUDICATION
```

or, when redesign is implicated:

```text
SERIOUS CHALLENGE — CONSIDER REDESIGN / UPSTREAM AUTHORITY REOPEN
```

State the challenged authority/scope, concrete contradiction, evidence and assumptions, consequence if correct, suggested resolution direction, and what evidence would resolve or falsify the challenge. Preserve the accepted authority as the challenged baseline; do not silently rewrite it to fit downstream realization.

## Human adjudication and truth

Humans, agents, papers, workplans, architecture, specification, code, and tests are instruments for recovering and preserving truth; authority governs action and mutation, not truth creation.

Consequential scientific or mathematically material decisions require the designated human domain authority when project policy assigns that gate. Typical human-gated surfaces include a change to the scientific question/interpretation, observable or estimand, governing model/equations/closures, material assumptions/validity regime, scientifically consequential approximation/model uncertainty, unexplained discrepancy acceptance, material algorithm guarantees, or error/tolerance budgets capable of changing scientific conclusions.

Routine delegated derivation, implementation, refactoring, bounded numerical checks, and literature gathering remain autonomous unless their result crosses such a decision boundary.

A human may accept, reject with reason, revise/clarify authority, request discriminating evidence, or—where safety/project rules allow—issue an explicit visible risk override. A risk override authorizes bounded continuation but does not resolve the truth claim and may not be used to release Protocol 6 itself while a governing Serious Challenge remains unresolved.

When a serious challenge is rejected with satisfactory reasoning, genuinely reconsider it. If resolved, preserve only the concise material rationale needed to prevent plausible recurrence; do not create a permanent challenge database or review transcript.

## Final invariant

```text
An abstraction states the semantic invariants that must survive realization.
A realization must satisfy every applicable upstream abstraction and governed external constraint.
Within that feasible set, optimize domain fitness, then minimum justified complexity, then development economy.
A realization remains delegated except where an owning authority explicitly accepts a property into the abstraction.
Verification reconstructs realization semantics and attempts to falsify conformity; it is opposite-direction reasoning, not a bijective inverse function.
A realization may challenge upstream authority through evidence but may never silently redefine it.
Accepted upstream change invalidates only dependent downstream authority/evidence.
Current normative documents change only through accepted authority mutation, not speculative edits.
Accepted authority is governable but not infallible.
```