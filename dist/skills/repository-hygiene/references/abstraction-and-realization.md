# Abstraction, Concretization, Authority, and Challenge

Protocol 6.1 governs scientific-software development through one recursive relation:

```text
ABSTRACTION  --design / constrain-->  CONCRETIZATION
ABSTRACTION  <--verify / reconstruct-- CONCRETIZATION
```

The historical filename `abstraction-and-realization.md` is retained as an opaque Protocol 6.0 compatibility path. In current Protocol 6.1 semantic prose, **concretization** names downstream scientific/software expression of an abstraction and **realization** is reserved for concrete evidence execution as defined in [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md).

## Background and terminology

An **abstraction** is an intentionally incomplete but normative semantic contract. It states the material invariants, required outcomes, assumptions, validity conditions, observables, bounds, and governed relations that every admissible concretization must preserve.

A **concretization** is a lower-level scientific, numerical, architectural, specification, or implementation choice that satisfies applicable parent abstractions and governed side constraints. An interior D1-D4 artifact may be a concretization of its parent while serving as an abstraction for its descendants.

The **Scientific Software Development Protocol (SSDP)** uses four semantic domains: D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation.

## Feasibility before optimization

For a concretization `K` constrained by applicable upstream abstractions `A1 ... An` and domain-local governed constraints `C`:

```text
semantics(K) |= I(A1) AND ... AND I(An) AND C
```

Fidelity is a feasibility condition, not a weighted objective. Among admissible concretizations prefer, in order:

```text
domain engineering fitness
> minimum justified concretization complexity
> development economy
```

This is a bounded engineering search rule, not a demand for exhaustive global optimization. Stop when further search has lower expected engineering value than proceeding with the best justified admissible concretization.

## Authority source is orthogonal to abstraction level

D1-D4 describe semantic level. They do not determine where authority originated. Preserve this precedence:

```text
safety / explicit stakeholder and project authority / governed external contracts
    -> accepted current domain abstractions and ratified decisions
    -> repository/runtime evidence about actual concretization state
    -> delegated concretization discretion
```

A security, reliability, performance, compatibility, hardware, regulatory, or public-contract constraint may enter directly at D2, D3, or D4. Do not force every external requirement through D1 merely to make the hierarchy linear.

Each material claim has one current normative semantic owner, but a concretization may be constrained by many applicable authorities simultaneously. If applicable authorities conflict materially, do not silently choose one; surface the conflict for adjudication.

## Four semantic domains

The scientific-software specialization is:

- **D1 — Scientific & Mathematical Formulation:** the scientific question, observables/estimands, governing model/equations, assumptions, validity regime, interpretation, and external adequacy semantics. Owned by `scientific-formulation`.
- **D2 — Algorithm & Numerical Methods:** numerical/discrete/stochastic concretization of D1, approximation/error/convergence/conditioning/precision semantics, algorithmic guarantees, and numerical uncertainty. Owned by `numerical-algorithm-design`.
- **D3 — Software Architecture:** component ownership, data/control flow, interfaces, persistence/concurrency/resource/security/deployment architecture, and cycle-scoped architectural decisions. Owned by `software-design`.
- **D4 — Specification & Implementation:** accepted concrete software contract plus code/executable behavior, tests, packaging, and operational concretization. Implemented by `software-implementation`; the accepted specification remains normative where one exists and code is evidence of actual behavior.

The four levels form a layered directed acyclic graph (DAG), not necessarily one linear chain. Shared algorithms, shared architecture, alternative concretizations, and multi-parent constraints are valid. Current normative ownership must remain acyclic so authority can be resolved independently.

## Invariant versus delegated concretization

At every boundary ask:

> Is this property required by the abstraction or an applicable governed constraint, or is it merely one way the current concretization satisfies them?

A lower-level detail does not acquire authority because it exists, is depended upon, is tested, is documented, survived review, appears in a previous workplan, or is convenient to verify. Promote a concretization property into an abstraction only through explicit acceptance by that abstraction's owning authority and for a material semantic reason.

When solution-created machinery causes its own intermediate problems, prefer removing, narrowing, altering, consolidating, re-deriving, or replacing that machinery before adding another durable repair. Never simplify by weakening a governing abstraction.

## Design and reverse semantic verification

Design is normally one-to-many:

```text
A -> {K | K satisfies A and applicable C}
```

Verification therefore is not a mathematical inverse. It operates in the opposite semantic direction:

```text
actual concretization
 -> reconstruct/project material semantics
 -> compare with every applicable parent and side constraint
 -> attempt to falsify conformity
```

Every material handoff asks two different questions:

1. **Concretization fidelity:** does the child concretize its governing parents correctly?
2. **Abstraction adequacy:** is the child abstraction strong and complete enough to preserve the material upstream meaning for the next concretization?

A concretization can perfectly satisfy a too-weak abstraction and still be wrong. Such abstraction inadequacy is an upstream design defect, not a successful handoff.

## Current, proposed, challenged, stale, and historical authority

Normative artifacts must distinguish lifecycle state sufficiently to prevent speculative edits from becoming authority accidentally. Projects may use their own metadata syntax, but the semantic states are:

- **proposed** — candidate authority; not yet governing;
- **accepted current** — current normative semantic owner for its claim scope;
- **challenged** — accepted current authority whose correctness is under a material unresolved challenge; still the explicit baseline, but dependent closure is blocked unless a visible human risk override applies;
- **risk-accepted/provisional** — a descendant artifact/evidence result whose validity depends on an unresolved challenged claim under explicit human risk override; it may support bounded continuation but cannot close the challenged claim or propagate an unqualified Pass;
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
 -> mark only dependent descendants/evidence review-required or stale
 -> concretize downward
 -> verify upward
```

Do not mutate current normative documents speculatively and then treat the edit as authority merely because it exists in the repository.

## Bounded dependency tracing, evidence, and invalidation

Represent only material semantic dependencies needed for concretization, impact analysis, invalidation, or verification. Section anchors, document links, workplan mappings, profile metadata, and bounded Markdown dependency views are normally sufficient. Protocol 6.1 does not require a universal claim graph or database.

When a dependency view is partial, absence of an edge does not prove independence. See [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for typed relationship direction, evidence applicability, stale-evidence semantics, and manual impact closure.

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

Every material review or verification/acceptance boundary includes a bounded adversarial Challenge Pass before normal closure. Ask whether governing authority is internally consistent, sufficiently unambiguous, jointly concretizable under all constraints, logically/mathematically coherent, adequate for its problem, complete enough to preserve upstream semantics, compatible with simultaneous authorities, and free from a known material counterexample.

For tiny low-risk work this may be implicit and brief. It is not a mandatory standalone stage or checklist.

Raise a **Serious Challenge** only for a material potential defect in accepted authority, such as:

- unconcretizable or contradictory invariants;
- material ambiguity that admits incompatible semantics;
- logical/mathematical fallacy or counterexample;
- scientific/model contradiction;
- abstraction inadequacy that permits high-integrity wrongness;
- genuine conflict among applicable authorities;
- a major conceptual decomposition that solves the wrong problem;
- a requirement to counterfeit closure by hiding or weakening contradictory evidence.

Ordinary concretization nonconformance under a coherent parent remains an ordinary blocker.

An active Serious Challenge must be prominent before ordinary blockers or Pass/No-Pass language, using an equivalent of:

```text
SERIOUS CHALLENGE — BLOCKED PENDING HUMAN ADJUDICATION
```

or, when redesign is implicated:

```text
SERIOUS CHALLENGE — CONSIDER REDESIGN / UPSTREAM AUTHORITY REOPEN
```

State the challenged authority/scope, concrete contradiction, evidence and assumptions, consequence if correct, suggested resolution direction, and what evidence would resolve or falsify the challenge. Preserve the accepted authority as the challenged baseline; do not silently rewrite it to fit downstream concretization.

## Human adjudication and truth

Humans, agents, papers, workplans, architecture, specification, code, and tests are instruments for recovering and preserving truth; authority governs action and mutation, not truth creation.

Consequential scientific or mathematically material decisions require the designated human domain authority when project policy assigns that gate. Typical human-gated surfaces include a change to the scientific question/interpretation, observable or estimand, governing model/equations/closures, material assumptions/validity regime, scientifically consequential approximation/model uncertainty, unexplained discrepancy acceptance, material algorithm guarantees, or error/tolerance budgets capable of changing scientific conclusions.

Routine delegated derivation, implementation, refactoring, bounded numerical checks, and literature gathering remain autonomous unless their result crosses such a decision boundary.

A human may accept, reject with reason, revise/clarify authority, request discriminating evidence, or—where safety/project rules allow—issue an explicit visible risk override. A risk override authorizes bounded continuation but does not resolve the truth claim and may not be used to release Protocol 6.1 itself while a governing Serious Challenge remains unresolved.

Every materially dependent descendant produced under that override remains risk-accepted/provisional with respect to the challenged claim. Unaffected siblings may close normally; dependent results must preserve the marker and may not be represented as ordinary accepted-current closure or an unqualified downstream Pass.

When a serious challenge is rejected with satisfactory reasoning, genuinely reconsider it. If resolved, preserve only the concise material rationale needed to prevent plausible recurrence; do not create a permanent challenge database or review transcript.

## Final invariant

```text
An abstraction states the semantic invariants that must survive concretization.
A concretization must satisfy every applicable upstream abstraction and governed external constraint.
Within that feasible set, optimize domain fitness, then minimum justified complexity, then development economy.
A concretization remains delegated except where an owning authority explicitly accepts a property into the abstraction.
Verification reconstructs concretization semantics and attempts to falsify conformity; it is opposite-direction reasoning, not a bijective inverse function.
Evidence realizations may challenge upstream authority through observations and assessments but may never silently redefine it.
Accepted upstream change invalidates only materially dependent downstream authority/evidence.
Current normative documents change only through accepted authority mutation, not speculative edits.
Accepted authority is governable but not infallible.
```