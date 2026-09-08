---
kind: protocol-major-revision-workplan
workplan_id: SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL
protocol_version: 5.16.0
target_protocol_version: 6.0.0
status: active
created_date: 2026-09-08
base_protocol: Protocol 5.16
repository_rename_deferred: true
---

# SSDP 6.0 Recursive Abstraction–Realization Scientific Software Development Protocol Workplan

## 1. Objective / core problem of concern

Protocol 5.16 has matured into a strong software-development control system. It provides disciplined separation between product/problem invariants, cycle-scoped Frozen architecture, delegated implementation machinery, implementation fidelity, affected-surface validation, proxy-proof acceptance, active simplicity, independent review, adversarial verification, long-horizon health sensing, documentation maintenance, language-aware engineering, tool routing, and a profile-driven orchestration seam.

The remaining structural defect is upstream of software architecture.

Scientific and numerical concerns currently exist in Protocol 5 as requirements, review concerns, testing doctrine, and documentation guidance, but they do not exist as first-class authority-bearing lifecycle domains with their own normative artifacts, design responsibilities, handoff contracts, verification semantics, and change-propagation rules. Scientific and mathematical formulation, numerical/algorithmic design, software architecture, and implementation are therefore partially conflated. In particular:

- scientific/problem truth is flattened into broad product truth;
- high-level algorithm decisions can be frozen directly by Software Design together with software architecture;
- methods/theory documentation is explanatory and non-normative by default;
- scientific/numerical verification consumes scientific authorities but the protocol does not govern how those authorities are created, ratified, revised, or kept aligned;
- code, architecture, specifications, methods papers, tests, and scientific intent can become mutually consistent at the software level while still implementing an incorrect or drifted scientific model;
- downstream implementation evidence can reveal an upstream modeling or numerical defect, but Protocol 5 has no general cross-domain authority ladder for routing such contradictions to the earliest affected abstraction.

This creates the possibility of **high-integrity wrongness**: scientifically incorrect software that is nevertheless architecturally coherent, well tested, reproducible, performant, and faithfully implemented relative to an insufficient or wrong upstream contract.

SSDP 6.0 shall repair this by replacing the software-specific Tier-1A/Tier-1B/Tier-2 framing with a more general **recursive abstraction–realization doctrine** that applies across scientific modeling, mathematical formulation, numerical/algorithmic design, software architecture, and code.

The central conceptual relation is:

```text
ABSTRACTION  --design / constrain-->  REALIZATION
ABSTRACTION  <--verify / reconstruct-- REALIZATION
```

The abstraction defines the invariant semantic problem and the admissible realization space. The realization is selected by constrained optimization: first satisfy the abstraction faithfully, then optimize among admissible realizations according to the domain-appropriate form of engineering fitness, minimum justified solution complexity, and development economy. Verification is the inverse semantic direction: reconstruct what the realization actually means/does and establish whether it is a valid realization of the abstraction.

Every interior level is simultaneously:

```text
a realization of the level above
and
an abstraction constraining the level below.
```

This recursive relation is the governing philosophical and engineering foundation of SSDP 6.0.

## 2. Governing abstraction–realization doctrine

### 2.1 Generic relation

For an abstraction `A`, let `I(A)` denote the set of semantic invariants, constraints, assumptions, bounds, validity conditions, and required observables that every acceptable realization must preserve.

A realization `R` is admissible only when:

```text
semantics(R) satisfies I(A)
```

or, conceptually:

```text
R |= A
```

The realization problem is therefore not an unconstrained tradeoff between correctness, simplicity, performance, and development cost. Fidelity to the abstraction is a feasibility condition.

Among admissible realizations, select the globally best justified realization according to the domain-appropriate lexicographic preference:

```text
engineering / scientific / numerical fitness
    > minimum justified realization complexity
    > development economy
```

Equivalently:

```text
first define the valid realization space;
then optimize inside it.
```

A simple, fast, elegant, or cheap realization that violates the abstraction is not a lower-scoring candidate; it is outside the feasible set.

### 2.2 Invariant versus delegation

The existing Protocol 5 Frozen/delegated doctrine shall be generalized as follows.

At every abstraction–realization boundary ask:

> Is this property part of the abstraction being realized, or merely one way the current realization satisfies it?

The abstraction owns only the semantic commitments that must remain invariant across admissible realizations. Everything not required by those commitments remains delegated realization space by default.

A realization detail does not become an abstraction invariant merely because it:

- already exists;
- is depended upon;
- appears in tests;
- appears in documentation;
- appeared in a prior workplan;
- survived prior review;
- was previously patched;
- is convenient to verify;
- is named by an acceptance path.

Promotion of a realization detail into the parent abstraction requires explicit acceptance at the abstraction-owning domain and a material semantic reason.

### 2.3 Design and verification are inverse semantic operations

Design proceeds top-down:

```text
Given abstraction A:
    recover its invariants and delegated space
    -> search for candidate realizations
    -> reject non-conforming candidates
    -> optimize among conforming candidates
    -> freeze only the lower-level abstraction necessary for the next domain
```

Verification proceeds bottom-up:

```text
Given realization R:
    reconstruct its actual semantics
    -> compare those semantics against the parent abstraction
    -> attempt to falsify conformity
    -> establish R |= A with the strongest justified evidence available
    -> route contradictions to the earliest/highest affected abstraction owner
```

Verification evidence may include formal proof, analytic derivation, symbolic checking, reference comparison, differential testing, metamorphic testing, property/stateful testing, convergence studies, uncertainty analysis, real-owner integration, structural checks, bounded fault injection, empirical validation, or other domain-appropriate methods.

No single verification technique is universally required. Evidence strength must match claim risk and the semantic relation under test.

### 2.4 Downstream evidence may challenge but not silently redefine upstream authority

A lower-level realization is evidence about what actually exists. It is never retroactive authority for what the parent abstraction ought to mean.

Therefore:

```text
downstream contradiction
    -> challenge upstream abstraction
    -> abstraction owner adjudicates
    -> accepted upstream revision may invalidate dependent descendants
```

The forbidden pattern is:

```text
implementation differs
    -> rewrite architecture to match implementation
    -> rewrite algorithm paper to match architecture
    -> rewrite scientific paper to match algorithm
    -> declare restored consistency
```

unless independent upstream reasoning actually establishes that each changed abstraction is the newly accepted correct one.

### 2.5 Change propagation and bounded invalidation

Upstream accepted changes invalidate only dependent downstream authority/evidence whose claim could materially change.

```text
accepted abstraction change
    -> invalidate affected child abstraction/realization claims
    -> propagate only through dependent descendants
    -> preserve unrelated accepted authority and still-valid evidence
```

Bottom-up observations do not automatically invalidate upstream authority. They produce a challenge requiring adjudication.

This generalizes Protocol 5's evidence invalidation and bounded Design reopening into a domain-independent rule.

### 2.6 Reopen the earliest materially affected abstraction

When new evidence invalidates an accepted decision, route rework to the earliest/highest domain whose abstraction may be wrong.

Examples:

```text
local helper defect                         -> implementation realization
component ownership/dataflow defect         -> software architecture
solver/discretization/estimator defect      -> numerical/algorithmic design
incorrect objective/model/definition        -> scientific & mathematical formulation
empirical/model-reality mismatch            -> scientific validation / formulation reconsideration
```

Do not reopen higher domains merely because lower affected surfaces grow. Do not keep repair artificially low when the parent abstraction itself is invalid.

### 2.7 External validation boundary

The recursive abstraction–realization relation governs the engineered hierarchy. At the highest scientific boundary, correctness against an internal parent abstraction is insufficient.

SSDP shall distinguish:

- **verification:** whether a realization faithfully realizes an accepted abstraction;
- **validation:** whether the scientific formulation/model is adequate for the intended real-world/research context;
- **uncertainty quantification:** how uncertainty in data, parameters, modeling assumptions, stochastic processes, and numerical approximation affects conclusions.

The top boundary is therefore:

```text
scientific formulation <-> empirical/research evidence and intended context of use
```

A mathematically and computationally perfect realization of an invalid scientific model is not scientifically valid software.

## 3. Four-domain hierarchy

SSDP 6.0 defines four first-class engineering domains.

```text
D1  Scientific & Mathematical Formulation
        |
        | defines the scientific/mathematical problem
        v
D2  Algorithm & Numerical Methods
        |
        | defines the computational/numerical problem
        v
D3  Software Architecture
        |
        | defines the software realization problem
        v
D4  Software Implementation
```

The reverse verification ladder is:

```text
D4 implementation
    -> reverse-engineer semantics and verify against D3
D3 architecture
    -> reverse-engineer effective computational semantics and verify against D2
D2 algorithm/numerics
    -> reconstruct effective mathematical problem and verify against D1
D1 scientific/mathematical formulation
    -> validate against scientific evidence, intended use, and reality where applicable
```

Not every task activates every domain. Affected-domain routing shall activate the highest domain whose abstraction may materially change and all required descendants, while preserving still-valid authority above and outside the affected dependency surface.

### 3.1 D1 — Scientific & Mathematical Formulation

D1 owns the most abstract internal semantic authority.

It shall govern, as applicable:

- scientific/research question and context of use;
- target observable, quantity, estimand, objective, or scientific conclusion;
- theoretical/physical/statistical basis;
- definitions, notation, conventions, units, frames, sign/index/tensor conventions;
- mathematical formulation;
- governing equations or probabilistic/statistical model;
- initial/boundary conditions;
- symmetry, conservation, invariance, and exact identities;
- assumptions and approximations with scientific meaning;
- identifiability/well-posedness concerns;
- validity regime and known invalid regimes;
- scientific/model uncertainty;
- external literature and source provenance;
- scientific validation strategy and falsification criteria;
- human-ratified scientific judgments when required.

D1 delegates the choice of computational/numerical realization unless a particular numerical property is itself scientifically intrinsic.

### 3.2 D2 — Algorithm & Numerical Methods

D2 realizes the accepted D1 mathematical/scientific abstraction and becomes the abstraction for D3.

It shall govern, as applicable:

- algorithm family and computational formulation;
- discretization;
- numerical estimator construction;
- approximation scheme;
- conditioning and sensitivity;
- consistency;
- stability;
- convergence and expected order/rate where meaningful;
- solver semantics;
- stopping/convergence criteria;
- numerical error budget;
- truncation/discretization error;
- floating-point/roundoff requirements;
- stochastic/randomized semantics;
- numerical reproducibility requirements;
- reference/direct/slow oracle methods;
- analytical/limiting/manufactured-solution checks where appropriate;
- degeneracies and numerical failure regimes;
- computational complexity/scaling envelope;
- admissible numerical alternatives and substitution criteria;
- accuracy/performance trade space without permitting silent scientific-fidelity loss.

D2 delegates software decomposition, ownership, storage, API, concurrency mechanism, and low-level implementation unless those details are necessary to preserve a numerical invariant.

### 3.3 D3 — Software Architecture

D3 realizes the accepted D2 computational/numerical abstraction and becomes the abstraction for D4.

D3 shall govern, as applicable:

- semantic/component ownership;
- package/module/service boundaries;
- public/internal interfaces;
- authoritative representations;
- data and control flow;
- state and lifecycle;
- persistence/checkpoint/cache authority;
- concurrency/orchestration architecture;
- resource and backend policy;
- hardware/accelerator realization boundaries;
- compatibility/migration boundaries;
- fault/recovery semantics;
- security/trust boundaries;
- architecture fitness rules;
- mapping from algorithmic responsibilities to software owners.

Algorithmic meaning inherited from D2 is not to be redefined by D3 merely because a particular software decomposition is convenient.

### 3.4 D4 — Software Implementation

D4 realizes the accepted D3 software architecture subject to all inherited upstream constraints.

D4 owns, as delegated:

- concrete functions/classes/templates/modules within architectural ownership;
- local data structures;
- helpers and idioms;
- library/tool use;
- low-level optimizations;
- implementation-local control flow;
- code/refactor execution;
- executable tests and validation machinery;
- repository reconciliation;
- implementation specifications and concrete public contracts where delegated by D3.

D4 may replace, remove, consolidate, or simplify realization machinery while preserving all applicable D3/D2/D1 invariants.

## 4. One-to-one documentation correspondence

SSDP 6.0 shall establish a first-class durable documentation stack corresponding to the abstraction hierarchy.

```text
D1 -> Scientific Method Paper
D2 -> Numerical & Algorithmic Method Paper
D3 -> Architecture Manual
D4 -> Specification + Code Base
```

These are current-state semantic records, not implementation chronology.

The purpose is not documentation symmetry for its own sake. The stack provides a human-readable, AI-readable, publishable reconstruction of the scientific software from scientific intent through executable realization. A technically competent researcher should be able to understand what the software claims scientifically, how the claim is formulated mathematically, how the formulation is solved numerically, how the computation is architected, and how the public software realizes it without source archaeology or historical-chat recovery.

### 4.1 D1 Scientific Method Paper

Owned and maintained by `scientific-formulation`.

This is a normative scientific/mathematical authority for the affected current method, not merely explanatory prose.

It should contain, proportionately:

1. background and scientific context;
2. motivation and research/problem statement;
3. goals and intended context of use;
4. theoretical foundation;
5. definitions and notation;
6. conventions and units;
7. mathematical formulation;
8. assumptions and approximations;
9. validity regime and known limitations;
10. observable/estimand/objective definitions;
11. validation/falsification strategy;
12. uncertainty/model-adequacy considerations;
13. relation to prior literature and project-specific adaptations;
14. references;
15. explicitly delegated numerical realization space.

The paper may be publication-quality and may support derived PDF/publication formats, but publication polish must not replace semantic authority.

### 4.2 D2 Numerical & Algorithmic Method Paper

Owned and maintained by `numerical-algorithm-design`.

This is a normative computational/numerical authority for the accepted realization of D1.

It should contain, proportionately:

1. inherited scientific/mathematical problem;
2. computational objective and numerical motivation;
3. algorithmic formulation;
4. discretization/estimation method;
5. data/operation model where algorithmically material;
6. pseudocode/flow description where useful;
7. conditioning/sensitivity analysis;
8. consistency/stability/convergence reasoning;
9. error model and numerical error budget;
10. tolerance, precision, stopping, and resolution policy;
11. stochastic semantics where applicable;
12. reference/oracle algorithm;
13. analytical/limiting/reference cases;
14. degenerate and failure regimes;
15. complexity/scaling characteristics;
16. accepted performance/fidelity trade space;
17. relation to standard algorithms/literature and project adaptations;
18. delegated software-architecture realization space.

This document must be computer-science/numerical-method oriented rather than merely repeating the D1 paper in implementation language.

### 4.3 D3 Architecture Manual

Owned and maintained by `software-design`.

The existing architecture doctrine shall be narrowed to software architecture. The architecture manual documents the accepted realization of D2 in terms of software ownership, boundaries, representations, state, persistence, concurrency, interfaces, resource policy, failure semantics, and mapping from algorithmic responsibility to software owners.

The architecture manual must not become the canonical owner of scientific formulation or numerical-method meaning merely because those semantics are implemented through the architecture.

### 4.4 D4 Specification and Code Base

Owned and maintained by `software-implementation`, subject to D3 authority.

The code base is the executable realization. Specifications own concrete externally relied-upon software contracts such as API/CLI/configuration, schemas/formats, units/shapes/order/precision at software boundaries, persistence semantics, compatibility/migration behavior, and durable error/fallback behavior where those are not already fixed by a higher abstraction.

Specifications must not silently redefine D1/D2 scientific or numerical semantics. When a concrete specification exposes an upstream invariant, it references/preserves that invariant rather than becoming an independent competing authority.

### 4.5 Documentation authority inversion to repair

Protocol 5 currently treats methods/theory papers as explanatory and non-normative by default and places architecture/specification above them for behavior authority. SSDP 6.0 must reverse this where the method paper owns an upstream abstraction.

The authority chain shall be semantic rather than based on file type:

```text
Scientific Method Paper
    -> Numerical & Algorithmic Method Paper
        -> Architecture Manual
            -> Specification + Code Base
```

Each document owns only its abstraction layer. Lower documents may add delegated detail but may not contradict upstream authority.

A downstream document/code disagreement is first classified as realization drift unless independent evidence establishes that the upstream abstraction itself must be reconsidered.

### 4.6 Documentation maintenance is domain ownership, not a parallel documentation bureaucracy

The existing `software-documentation` specialist remains useful for editorial synthesis, reconciliation, publication, information architecture, user guides, and generated-document maintenance.

However, SSDP 6.0 must not delegate semantic ownership of D1/D2/D3 normative documents to a generic documentation specialist.

Semantic ownership remains with the domain role:

```text
scientific-formulation      -> D1 semantics and Scientific Method Paper
numerical-algorithm-design  -> D2 semantics and Numerical/Algorithmic Method Paper
software-design             -> D3 semantics and Architecture Manual
software-implementation     -> D4 specification/code semantics
```

`software-documentation` may assist any domain with presentation, coherence, publishing, cross-document navigation, and non-authoritative user documentation, but it may not approve or invent the owning domain's semantics.

## 5. Lifecycle roles

SSDP 6.0 introduces four authority-bearing roles.

```text
scientific-formulation
        -> numerical-algorithm-design
        -> software-design
        -> software-implementation
```

This is an incompatible lifecycle change and therefore requires Protocol major version 6 according to existing versioning doctrine.

### 5.1 `scientific-formulation`

Owns D1 design, maintenance, review, and D1->D2 handoff.

Responsibilities include:

- recover and define the scientific question independently of current code;
- reconcile literature, existing method papers, equations, experiments, and intended context;
- derive/critique mathematical formulation;
- identify assumptions, approximations, validity regimes, and falsification criteria;
- define scientific/model uncertainty requirements where material;
- maintain the Scientific Method Paper;
- review D2 as a realization of D1;
- adjudicate bottom-up challenges to D1;
- require human scientific ratification for consequential epistemic changes under the HITL policy.

It does not own software architecture or implementation realization.

### 5.2 `numerical-algorithm-design`

Owns D2 design, maintenance, review, and D2->D3 handoff.

Responsibilities include:

- translate accepted D1 formulation into a computational/numerical problem;
- select/derive numerical algorithms and admissible alternatives;
- reason about conditioning, consistency, stability, convergence, precision, stochastic semantics, and error budgets;
- design reference/oracle methods and numerical verification strategy;
- maintain the Numerical & Algorithmic Method Paper;
- review D3/assembled computation as a realization of D2;
- adjudicate bottom-up numerical challenges;
- escalate to D1 when numerical evidence invalidates a mathematical/scientific premise.

It does not own software component structure except where software properties are necessary to preserve the numerical abstraction.

### 5.3 `software-design`

Protocol 5 Software Design shall be narrowed and refactored to own D3 rather than D1-D3 simultaneously.

It retains strong existing doctrine for:

- software architecture and ownership;
- interfaces/data/state/persistence/concurrency/resources/security;
- minimum justified software-system complexity;
- implementation workplans;
- acceptance-boundary design;
- independent implementation review;
- active simplicity and architecture stabilization;
- architecture fitness and affected-surface reasoning.

It must consume D2 authority rather than inventing or silently freezing algorithmic/scientific semantics itself.

### 5.4 `software-implementation`

Retains D4 execution authority and most Protocol 5 implementation doctrine.

It implements accepted D3 while preserving all inherited upstream authority, runs required executable evidence, reconciles affected surfaces, simplifies delegated machinery, and routes invalidated parent abstractions upward instead of silently changing them.

## 6. Domain handoff contract

Every material domain-to-domain handoff shall use the same generic semantic structure.

A handoff is snapshot-complete for the affected abstraction without requiring Git history, prior chat, unavailable papers, or superseded artifacts to recover still-binding semantics.

Each handoff records, proportionately:

- parent abstraction/problem;
- invariants/required outcomes;
- assumptions and validity conditions;
- explicitly Frozen child-abstraction decisions for the next realization cycle;
- delegated realization space;
- non-goals;
- acceptance/verification relations;
- oracle/reference sources;
- relevant uncertainty/error budget;
- affected dependent claims/surfaces;
- genuine reopen triggers;
- human-ratification state when required.

The handoff is a semantic contract, not a proof script and not a requirement to duplicate the full method paper into every workplan.

## 7. Verification ladder

SSDP 6.0 shall distinguish four verification/validation boundaries.

### 7.1 D4 -> D3: implementation conformance verification

Question:

> Does the assembled executable software realize the accepted architecture and concrete software contracts completely and correctly?

Evidence may include focused tests, affected regression, integration/end-to-end paths, structural/source checks, architecture fitness checks, real-owner execution, property/stateful testing, mutation/counterfactual evidence, failure injection, sanitizers/static analysis, and production qualification where independently required.

### 7.2 D3 -> D2: algorithmic realization verification

Question:

> Does the assembled software architecture and execution path realize the accepted numerical/algorithmic method without changing its computational semantics?

Evidence may include mapping algorithm stages to semantic software owners, reference implementation comparison, numerical invariants, backend equivalence, ordering/reduction semantics, precision/tolerance checks, restart equivalence, deterministic/stochastic semantics, and end-observable comparison.

### 7.3 D2 -> D1: mathematical/scientific fidelity verification

Question:

> Does the selected numerical/algorithmic method solve/estimate the accepted mathematical formulation within its governed approximation and error envelope?

Evidence may include analytical cases, manufactured solutions where valid, refinement studies, observed convergence order, residual/error analysis, conditioning studies, exact invariants, symmetry/conservation checks, estimator bias/variance analysis, sensitivity analysis, cross-method comparison, and independent derivation.

### 7.4 D1 -> empirical/research reality: validation and UQ

Question:

> Is the accepted scientific/mathematical formulation adequate for the intended scientific context and are its conclusions supported within understood uncertainty?

Evidence may include experimental/reference data comparison, held-out validation, model discrepancy analysis, uncertainty quantification, parameter identifiability, sensitivity, external literature, domain-expert judgment, and explicit falsification tests.

This boundary often requires human scientific judgment and must not be reduced to ordinary software test passing.

## 8. Human-in-the-loop scientific authority

SSDP shall increase autonomy without delegating consequential scientific authority blindly to agents.

AI agents may autonomously perform substantial upstream work including:

- literature search and synthesis;
- equation/derivation reconstruction;
- consistency checking;
- alternative formulation generation;
- symbolic/numerical sanity checks;
- sensitivity/convergence experiments;
- counterexample/falsification attempts;
- traceability maintenance;
- draft method-paper updates;
- downstream propagation of already-ratified semantic changes.

Human ratification is normally required before materially accepting changes to:

- the research/scientific question or intended interpretation;
- target observable/estimand/objective semantics;
- governing physical/statistical model;
- major modeling assumptions or closures;
- mathematical formulation with scientific consequences;
- context-of-use or validity regime;
- approximation that may change scientific conclusions;
- scientific/model uncertainty assumptions;
- acceptance of unexplained model-data discrepancy;
- algorithmic changes that materially alter scientific/numerical guarantees or interpretation;
- numerical error budgets/tolerances where the choice may alter scientific conclusions.

Projects may explicitly delegate lower-risk upstream decisions after establishing a policy. Absence of a human at every routine step must not force a synchronous waterfall; the gate is semantic-risk based.

The protocol and orchestrator must represent `human ratification required/pending/accepted/rejected` truthfully rather than allowing a model to self-approve an explicitly human-owned decision.

## 9. Sparse semantic claim lineage

SSDP 6.0 shall provide lightweight traceability between material claims across abstraction levels without requiring a universal requirements database or exhaustive graph of every function/equation.

Projects should be able to express relations conceptually such as:

```text
SCI-04  target observable definition
    -> MATH-07 mathematical estimator
        -> NUM-12 finite numerical estimator
            -> ARCH-21 aggregation owner
                -> IMPL semantic owner/symbol family
                    -> EV-31 verification evidence
```

Only claims whose cross-layer dependency materially improves correctness, impact analysis, verification, publication, or change propagation need durable identities.

The lineage system must support:

- parent/child abstraction relation;
- realization-of relation;
- verifies/evidence-for relation;
- supersedes/revises relation where needed;
- dependency-aware stale/invalidation state.

Do not build a large ontology, graph database, or mandatory identifier bureaucracy unless concrete use proves it necessary. Markdown-native structured metadata or another lightweight representation is preferred initially.

## 10. Recasting Protocol 5 doctrine in SSDP language

SSDP 6.0 shall preserve the successful substance of Protocol 5 while reducing conceptual duplication.

### 10.1 Product truth / Tier 1A

Refactor into **parent abstraction invariants**. What Protocol 5 called intrinsic product/problem truth is the abstraction that constrains a realization at the relevant boundary.

### 10.2 Frozen high-level architecture / Tier 1B

Generalize into **accepted child abstraction**. Every domain may freeze only the material decisions needed to define the next domain's problem for the current realization cycle.

The concept is no longer software-architecture-specific.

### 10.3 Tier 2 delegated machinery

Generalize into **delegated realization space** at every boundary.

Scientific modeling choices, numerical algorithms, software architecture, and code can each be delegated relative to an upstream abstraction until explicitly fixed by the owning domain.

### 10.4 Engineering fitness / simplicity / economy

Retain as the constrained-realization objective hierarchy.

At each domain:

```text
fidelity to parent abstraction = feasibility constraint
then optimize:
    domain fitness
    > minimum justified realization complexity
    > development economy
```

Domain fitness changes meaning by layer but not structure:

- D1: scientific explanatory/predictive adequacy for intended use;
- D2: numerical correctness, accuracy, robustness, scaling, tractability;
- D3: architectural fitness, ownership clarity, operability, resources, maintainability;
- D4: implementation correctness, idiomatic realization, efficiency, testability.

### 10.5 Active simplicity

Generalize from Tier-2 code/architecture cleanup to **realization simplification at any layer**.

If a realization accumulates patches, exceptions, compensating assumptions, duplicated authority, special cases, repeated reconciliation, or a materially simpler equally valid realization becomes evident, simplify/rederive that realization before adding further durable complexity.

This applies to:

- scientific models with accumulating ad hoc corrections;
- numerical methods with compensating heuristic patches;
- software architectures with wrappers/fallbacks/duplicated state;
- implementations with patch-on-patch machinery.

Never simplify by weakening the parent abstraction silently.

### 10.6 Affected surface

Generalize into **affected semantic dependency surface**.

A changed abstraction may affect child algorithms, architecture, implementation, tests, documentation, validation evidence, benchmarks, or published conclusions. Expansion of the affected surface does not create new upstream requirements.

### 10.7 Proxy-proof acceptance

Generalize into **semantic-owner proof at each layer**.

Evidence must exercise or otherwise establish the actual realization component/semantic relation that constitutes the claim. A proxy that could remain green while the real semantic owner/algorithm/formulation is wrong cannot close the claim.

### 10.8 Evidence invalidation and reuse

Retain but generalize across all domains. Reuse evidence until a changed parent/realization dimension can plausibly alter the claim. Invalidate only dependent evidence.

### 10.9 Independent review and adversarial verification

Retain the falsification-oriented philosophy, but review independence is now available at each abstraction boundary rather than being only a Software Design mode over implementation.

### 10.10 Snapshot-complete handoff

Retain and generalize to all domain transitions. No still-binding semantic decision may exist only in lost chat, Git history, obsolete revisions, or unsupplied external context.

### 10.11 Convergence and recurrence

Retain as evidence that the current realization or abstraction boundary may be wrong. Repeated local failures should broaden reasoning to the shared semantic owner and may trigger re-derivation at the appropriate domain.

## 11. Required protocol artifacts and repository changes

The implementation of this workplan shall determine the minimum coherent repository structure, but the following semantic artifacts are required.

### 11.1 New role skills

Create first-class source roles:

```text
source/roles/scientific-formulation/SKILL.md
source/roles/numerical-algorithm-design/SKILL.md
```

with generated/installable distributions following existing source->dist build rules.

### 11.2 Refactor existing roles

Refactor:

```text
source/roles/software-design/SKILL.md
source/roles/software-implementation/SKILL.md
```

so they participate in the four-domain recursive model without duplicating D1/D2 authority.

### 11.3 Canonical shared references

Introduce or refactor canonical references sufficient to own:

- recursive abstraction-realization doctrine;
- scientific formulation and scientific validation;
- mathematical formulation and scientific authority;
- numerical/algorithmic design and numerical verification;
- cross-domain workflow/handoffs/reopen semantics;
- documentation-stack ownership;
- human scientific ratification;
- semantic claim lineage/invalidation;
- SSDP 6 versioning/compatibility/migration.

Prefer refactoring and splitting existing references over adding duplicative parallel prose. Existing `scientific-software.md` and `scientific-technical-writing.md` should be decomposed/reassigned where their current mixed responsibility becomes obsolete.

### 11.4 Normative document templates

Add lightweight templates for:

```text
Scientific Method Paper
Numerical & Algorithmic Method Paper
Architecture Manual guidance/template where not already adequately governed
Implementation workplan / specification linkage
```

Templates shall support progressive disclosure and publication-quality scientific writing without becoming mandatory fill-every-field forms.

### 11.5 Workflow prompt/profile changes

Extend the human-facing workflow prompt system and protocol profile so the four domains can be selected/routed explicitly and automatically by affected-domain reasoning.

Preserve local-first/public-fallback skill resolution and protocol-version coherence.

### 11.6 Protocol version

Set target protocol version to `6.0.0` only after the full incompatible lifecycle/doctrine migration is complete and independently reviewed.

The repository may retain its current name during implementation. Repository rename to SSDP is explicitly deferred and must not be coupled to semantic implementation unless a later migration step requires it.

## 12. Workflow architecture

SSDP must avoid becoming a mandatory four-domain waterfall.

A full scientific feature may follow:

```text
scientific question / evidence
    -> D1 formulation + human ratification when required
    -> D1 verification/validation readiness
    -> D2 algorithm/numerical design
    -> D2 verification against D1
    -> D3 software architecture/workplan
    -> D3 verification against D2
    -> D4 implementation
    -> D4 verification against D3
    -> upward cross-verification through affected domains
    -> publication/documentation reconciliation
    -> closeout
```

A software-local change may activate only:

```text
D3 -> D4 -> D3 verification
```

A pure implementation refactor may remain within D4 when D3/D2/D1 semantics are provably unchanged.

A numerical optimization may begin at D2 and propagate through D3/D4 while preserving D1.

A changed scientific hypothesis may begin at D1 and invalidate dependent descendants downward.

The routing rule is:

> Start at the earliest/highest abstraction whose accepted semantics may materially change, then realize downward only as far as necessary and verify back upward across the affected dependency surface.

## 13. Numerical and scientific oracle requirements

SSDP shall strengthen D1/D2 oracle engineering beyond the current downstream scientific-software reference.

The numerical-method doctrine should route proportionately among methods such as:

- dimensional/unit consistency;
- analytical exact cases;
- limiting/asymptotic cases;
- manufactured solutions where valid;
- residual checking;
- conservation/invariant checks;
- mesh/time-step/order refinement;
- observed convergence-order analysis;
- Richardson/extrapolation methods where justified;
- conditioning and sensitivity analysis;
- forward/backward error reasoning;
- floating-point cancellation/range/precision analysis;
- reference/direct solver comparison;
- cross-implementation differential validation;
- stochastic convergence/bias/variance analysis;
- uncertainty propagation;
- seed/backend/precision robustness;
- performance-versus-accuracy Pareto analysis.

The scientific-formulation doctrine should route proportionately among methods such as:

- empirical validation against appropriate data;
- calibration-versus-validation separation;
- parameter identifiability analysis;
- model discrepancy analysis;
- sensitivity to modeling assumptions;
- falsification/counterexample design;
- external literature reconciliation;
- uncertainty quantification;
- robustness of conclusions to plausible model alternatives.

Do not mandate every technique. Select the cheapest sufficiently strong evidence for the claim, escalating when risk, ambiguity, or failed falsification warrants it.

## 14. Protocol qualification

Protocol 6 acceptance must include behavioral qualification scenarios that distinguish superficially compliant but scientifically wrong behavior from sound SSDP reasoning.

At minimum add scenarios covering:

1. code perfectly matches architecture but the governing equation has the wrong sign;
2. architecture faithfully implements the wrong estimator;
3. a numerical algorithm converges reliably to the wrong continuous model;
4. tests duplicate the implementation's incorrect formula and all pass;
5. tolerance is widened solely to make an optimized backend pass;
6. reduced precision introduces scientifically meaningful bias while ordinary unit tests remain green;
7. method paper and implementation use different normalizations;
8. units are numerically compatible but physically interpreted incorrectly;
9. a stable stochastic estimator is biased relative to D1;
10. observed convergence order degrades after optimization;
11. boundary-condition implementation changes the modeled physics;
12. calibration data is reused as validation evidence;
13. parallel reduction/summation changes results beyond the accepted numerical error budget;
14. restart/checkpoint semantics alter the stochastic estimator;
15. a downstream implementation is used to rewrite upstream authority without independent adjudication;
16. D1 changes only one observable and the protocol invalidates unrelated D2/D3/D4 evidence unnecessarily;
17. a software-local refactor incorrectly escalates to D1/D2 despite unchanged semantics;
18. a numerical contradiction is incorrectly treated as a local code bug rather than reopening D2;
19. a human-owned scientific decision is self-approved by an agent;
20. a method paper is historically coherent but no longer represents the accepted current science.

Qualification should test role routing, authority precedence, correct reopen domain, documentation ownership, evidence invalidation, and refusal to counterfeit closure.

## 15. Orchestrator compatibility and integration

The current orchestrator architecture already makes workflow routing profile-owned and keeps the orchestrator subordinate to protocol intent. SSDP 6 shall preserve that architecture.

Do not hard-code scientific workflow semantics into Tracker/Adapters/Scheduler as a second authority.

After SSDP 6 semantics stabilize, extend the protocol profile minimally to represent, as needed:

- domain identity;
- role owner;
- artifact kind;
- upstream authority dependencies;
- verification target;
- affected-domain/invalidation edges;
- recognized outcomes;
- human-ratification requirement/state;
- reopen/routing semantics.

Tracker may project these states and recommend next actions. It must consume the compatible protocol profile rather than independently interpreting scientific doctrine.

Adapter/Scheduler capability and resource routing remains subordinate to the required SSDP stage/domain. Resource optimization may choose among engineering-sufficient execution routes but may never decide scientific truth or bypass a required human epistemic gate.

Existing Protocol 5.16 profiles and historical workplans remain version-bound and must not be silently reinterpreted under SSDP 6.

## 16. Migration strategy

### Phase 0 — Parent authority freeze

This workplan is the parent transition contract. Before broad implementation, independently review it for conceptual completeness, contradictions with preserved Protocol 5 guarantees, lifecycle ambiguity, and unnecessary machinery.

Do not begin by mechanically editing all skills.

### Phase 1 — Core recursive doctrine

Create the canonical abstraction-realization reference and refactor governing README/workflow/versioning language around it.

Acceptance:

- `R |= A` feasibility semantics are explicit;
- invariant/delegated classification is generic;
- fitness/simplicity/economy is expressed as optimization inside the feasible realization space;
- design/verification inverse relation is explicit;
- upward challenge/downward invalidation semantics are explicit;
- validation boundary is distinguished from verification.

### Phase 2 — D1 scientific-formulation role and paper

Implement the D1 role, method-paper ownership, scientific validation/UQ doctrine, literature/provenance rules, and HITL scientific authority.

Acceptance includes behavioral qualification against model/formulation drift.

### Phase 3 — D2 numerical-algorithm-design role and paper

Implement D2 role, numerical-method doctrine, numerical paper ownership, error/convergence/conditioning/oracle requirements, and D1<->D2 handoff/verification.

Acceptance includes genuine numerical qualification scenarios rather than phrase-only checks.

### Phase 4 — Narrow/refactor D3 Software Design

Remove D1/D2 semantic ownership from Software Design while preserving its strong architecture, workplan, active-simplicity, review, tool-routing, resource, security, state, and acceptance doctrine.

Do not duplicate old algorithm/scientific language in D3 for compatibility. Route it upward.

### Phase 5 — Adapt D4 Software Implementation

Teach Implementation to consume D3/D2/D1 authority, distinguish parent-abstraction invalidation from local realization reconciliation, and preserve multi-domain evidence invalidation.

### Phase 6 — Four-layer documentation architecture

Refactor documentation doctrine so normative current scientific/numerical papers are first-class upstream authorities.

Preserve `software-documentation` as a semantic-subordinate editorial/publication specialist.

Add cross-document navigation/traceability conventions sufficient for a human researcher to traverse the full stack.

### Phase 7 — Sparse claim lineage and affected-domain routing

Implement the minimum useful structured representation for cross-layer material claims, dependencies, stale state, and reopen routing.

Do not introduce a database or heavy graph machinery unless markdown/profile-level structures prove insufficient through concrete evidence.

### Phase 8 — Workflow prompts and protocol profile

Add four-domain stage/routing support, human-gate states, and domain-aware invalidation to the canonical prompt/profile system.

Preserve profile ownership and orchestrator compatibility.

### Phase 9 — Protocol qualification and self-review

Run static package/build validation plus adversarial behavioral qualification across the scenarios above.

Review whether SSDP 6 itself creates unnecessary bureaucracy, duplicated authority, or fixed-stage overhead. Simplify before release where equivalent semantics can be preserved.

### Phase 10 — Orchestrator SSDP 6 integration

Only after the protocol profile is accepted, update the orchestrator's compatible snapshot/profile support. Preserve the existing orchestrator architecture unless concrete evidence forces a bounded reopen.

### Phase 11 — Release/closeout

- set `PROTOCOL_VERSION` to `6.0.0`;
- regenerate skill distributions;
- validate source/dist coherence;
- update repository README/portability guidance;
- preserve Protocol 5 historical compatibility semantics;
- close/archive this workplan only after independent Review passes;
- repository rename to SSDP remains a separate user-controlled operation.

## 17. Required implementation obligations

### Obligation A — Replace the three-tier software-specific authority model with recursive abstraction–realization semantics

**Required end state:** Protocol-wide governing doctrine uses abstraction invariants, delegated realization space, constrained optimization, and inverse verification as the primary conceptual vocabulary. Tier-1A/Tier-1B/Tier-2 terminology may survive only in historical compatibility explanations or where needed to explain Protocol 5 workplans.

**Anti-shortcut:** Do not merely add abstraction-realization prose above unchanged role semantics while Software Design still owns D1/D2 authority.

### Obligation B — Establish four true authority-bearing domains

**Required end state:** D1-D4 have distinct semantic ownership, mutation authority, handoff/reopen behavior, and verification responsibility.

**Anti-shortcut:** Do not implement D1/D2 as optional references or documentation specialists under Software Design.

### Obligation C — Establish one-to-one normative documentation ownership

**Required end state:** Scientific Method Paper, Numerical & Algorithmic Method Paper, Architecture Manual, and Specification+Code correspond to D1-D4 and are maintained by their semantic owners.

**Anti-shortcut:** Do not leave D1/D2 papers non-normative while claiming the documentation stack is complete.

### Obligation D — Preserve valid Protocol 5 strengths by semantic refactoring rather than additive duplication

**Required end state:** active simplicity, proxy-proof acceptance, snapshot-complete handoffs, affected-surface reasoning, evidence invalidation, convergence, language profiles, tool routing, long-horizon quality, security/resource/performance doctrine, and version binding remain effective under SSDP 6.

**Anti-shortcut:** Do not create parallel `ssdp-*` references that duplicate existing doctrine wholesale while leaving the old system intact underneath.

### Obligation E — Generalize verification to every abstraction boundary

**Required end state:** every domain can design downward and independently verify upward using domain-appropriate methods; scientific validation remains distinguished at the top boundary.

### Obligation F — Add risk-sensitive human scientific ratification

**Required end state:** consequential D1 and scientifically material D2 decisions cannot be silently self-approved by autonomous agents; ordinary delegated work remains automatable.

### Obligation G — Add bounded cross-layer lineage and invalidation

**Required end state:** material upstream changes can identify dependent downstream authority/evidence as stale without invalidating unrelated work; downstream contradictions route upward without rewriting authority.

### Obligation H — Keep SSDP proportional

**Required end state:** software-only projects and local changes can use reduced profiles. The protocol must not force four documents, four reviews, or four stages when upstream domains are not material.

### Obligation I — Preserve orchestrator authority separation

**Required end state:** the orchestrator consumes SSDP profile semantics; it does not become an independent scientific workflow engine or epistemic authority.

### Obligation J — Self-qualify with adversarial scientific/numerical scenarios

**Required end state:** Protocol 6 acceptance demonstrates correct behavior on intentionally deceptive cross-layer cases, not only static textual structure.

## 18. Delegated implementation space

The following remain delegated unless later evidence requires a Frozen decision:

- exact role names if equivalent clearer names are found before public release;
- exact file names of new references/templates;
- whether D1 mathematical formulation is one reference or split scientific/mathematical references;
- exact Markdown metadata schema for claim lineage;
- exact profile-schema field names;
- exact qualification harness implementation;
- exact document directory conventions in downstream scientific repositories;
- whether architecture manual/specification templates are full files or doctrinal templates;
- exact symbolic/numerical tools named as examples;
- exact publication/PDF generation stack;
- exact human-approval UI in future orchestrator modules.

Prefer reuse and refactoring. New durable machinery must either provide a capability impossible to express cleanly in the simplified existing system or replace broader duplicated complexity.

## 19. Explicit non-goals

- Do not rename the GitHub repository as part of this workplan.
- Do not rewrite or invalidate historical Protocol 5 workplans.
- Do not force non-scientific software to invent scientific papers or numerical methods.
- Do not create four mandatory approvals for every change.
- Do not make documentation volume a proxy for rigor.
- Do not require formal proof where empirical/numerical evidence is the correct epistemic tool.
- Do not let empirical validation substitute for software/numerical verification, or vice versa.
- Do not create a universal claim graph/database covering every line, function, equation, or test.
- Do not make the orchestrator an authority over scientific truth.
- Do not turn human-in-the-loop into human-in-every-loop.
- Do not preserve obsolete Protocol 5 conceptual duplication merely for wording compatibility inside Protocol 6 roles.
- Do not create patches/wrappers around role-boundary problems that are more cleanly solved by moving ownership to the correct abstraction layer.

## 20. Acceptance criteria

SSDP 6.0 is ready for release only when all of the following are true.

### Conceptual closure

- recursive abstraction-realization is the clearly governing doctrine;
- realization fidelity is a feasibility constraint, not a weighted tradeoff;
- invariant versus delegated realization is consistently defined across domains;
- design and verification are expressed as forward/inverse semantic relations;
- upstream authority/downstream evidence direction is unambiguous;
- validation/UQ are correctly distinguished from internal verification;
- active simplicity and engineering economy remain subordinate to semantic fidelity.

### Domain closure

- D1-D4 roles and authority boundaries are complete and non-overlapping;
- D1/D2 no longer depend on Software Design to own scientific/numerical semantics;
- D3 no longer silently owns algorithm/scientific meaning;
- D4 retains adaptive implementation authority within inherited constraints;
- reopen routing reaches the earliest materially affected abstraction.

### Documentation closure

- D1 Scientific Method Paper is normative for D1;
- D2 Numerical & Algorithmic Method Paper is normative for D2;
- D3 Architecture Manual is normative for D3;
- D4 specification/code own concrete software behavior for D4;
- semantic ownership and editorial/documentation-specialist responsibilities are separated;
- methods papers are publication-quality capable but not made bureaucratically mandatory when the domain is absent.

### Verification closure

- each abstraction boundary has clear verification questions and evidence routes;
- numerical verification includes genuine convergence/error/conditioning/oracle reasoning;
- scientific validation includes context-of-use/model-adequacy/UQ reasoning where applicable;
- proxy-proof evidence principles generalize across layers;
- evidence invalidation is dependency-aware.

### Autonomy/HITL closure

- human scientific ratification triggers are explicit and risk-based;
- autonomous agents can perform substantial derivation/search/testing without unnecessary synchronous gates;
- orchestrator/profile semantics can represent pending human authority truthfully.

### Compatibility and implementation closure

- Protocol 5.16 historical semantics remain recoverable and version-bound;
- Protocol 6 source/dist build and package checks pass;
- all new roles build as installable skills under existing packaging rules;
- workflow prompts/profile resolve the correct roles and stages;
- orchestrator integration remains subordinate to profile authority;
- repository/project test suites and new qualification scenarios pass;
- `git diff --check` and existing repository acceptance commands pass after implementation;
- independent Review finds no genuine blocking semantic or architectural defect.

## 21. Genuine redesign / simplification triggers

Reopen this parent authority only when evidence shows that one of its central assumptions is wrong, including:

- the recursive abstraction-realization relation cannot cleanly represent a material scientific/software development class;
- D1-D4 boundaries produce unavoidable competing authority;
- the one-to-one documentation stack forces systematic duplication rather than semantic ownership;
- human ratification rules materially block ordinary autonomous work without increasing scientific assurance;
- lightweight lineage cannot support bounded invalidation without disproportionate machinery;
- the four-role lifecycle causes unavoidable orchestration ambiguity that cannot be resolved through profile semantics;
- a simpler equivalent domain decomposition explains and controls the same failure modes with less authority machinery.

Before adding another role, stage, registry, database, wrapper, or reconciliation mechanism, determine whether the issue can be solved by reducing, moving, or clarifying abstraction ownership.

## 22. Final design invariant

The target SSDP 6.0 system should be understandable through one recursive rule:

```text
Every downstream domain is a realization of an upstream abstraction.
The upstream abstraction defines what must remain true.
The downstream domain is free to optimize how it is made true.
Verification reconstructs the realization and attempts to prove/falsify that it is faithful.
A realization may challenge its abstraction through evidence but may never silently redefine it.
Accepted upstream change invalidates only dependent downstream authority and evidence.
```

Applied recursively:

```text
scientific intent / empirical reality
          <->
scientific & mathematical formulation
          <->
algorithm & numerical methods
          <->
software architecture
          <->
specification & implementation
          <->
executable behavior and evidence
```

SSDP 6.0 shall teach agents to engineer scientific software as **recursive abstraction-preserving realization under constrained optimization, closed by inverse semantic verification and bounded scientific validation**.

That principle, rather than the incidental machinery of any current implementation, is the central invariant of this protocol revision.
