---
kind: protocol-major-revision-workplan
workplan_id: SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL
protocol_version: 5.16.0
target_protocol_version: 6.0.0
status: active
created_date: 2026-09-08
base_protocol: Protocol 5.16
base_commit: e151daaf5c8eebb351a85cfed86170fda80fb5e3
repository_rename_deferred: true
---

# SSDP 6.0 Recursive Abstraction–Realization Scientific Software Development Protocol Workplan

## 1. Objective / core problem of concern

Protocol 5.16 is a strong software-development control system. It already separates product/problem invariants from cycle-scoped Frozen architecture and delegated implementation machinery; preserves implementation fidelity, affected-surface validation, proxy-proof acceptance, active simplicity, version binding, independent review, adversarial Verification, long-horizon quality sensing, language-aware engineering, tool routing, and profile-owned orchestration.

Its remaining structural defect is upstream of software architecture.

Scientific and numerical concerns currently exist as product requirements, review concerns, testing doctrine, and documentation guidance, but not as first-class authority-bearing domains with their own normative current-state artifacts, mutation authority, design responsibilities, handoff contracts, verification semantics, and change-propagation rules. Scientific/mathematical formulation, numerical/algorithmic design, software architecture, and implementation are therefore partially conflated. In particular:

- scientific/problem truth is flattened into broad software product truth;
- high-level algorithm decisions are owned and frozen together with software architecture;
- methods/theory documentation is explanatory and non-normative by default;
- scientific/numerical Verification consumes scientific authorities but Protocol 5 does not govern how those authorities are created, accepted, challenged, revised, or synchronized;
- code, architecture, specifications, methods papers, tests, and scientific intent can become mutually consistent at the software level while implementing the wrong scientific model or numerical method;
- downstream evidence can reveal an upstream scientific, mathematical, numerical, or architectural defect, but Protocol 5 has no generic cross-domain authority model for routing that contradiction to the earliest affected abstraction.

This permits **high-integrity wrongness**: scientifically incorrect software that is architecturally coherent, well tested, reproducible, performant, and faithfully implemented relative to an incomplete or incorrect upstream contract.

SSDP 6.0 shall repair this by making **recursive abstraction–realization** the governing doctrine:

```text
ABSTRACTION  --design / constrain-->  REALIZATION
ABSTRACTION  <--verify / reconstruct-- REALIZATION
```

The abstraction states what must remain semantically true. The realization is free to optimize how those truths are achieved. Fidelity is a feasibility condition, not a weighted objective. Among admissible realizations, the protocol prefers the domain-fit realization with the minimum justified complexity, then minimizes development cost.

Every interior domain is simultaneously a realization of upstream authority and an abstraction constraining downstream realization. The four scientific-software domains are applications of one general relation, not four unrelated process philosophies.

The revision must preserve Protocol 5's strongest engineering safeguards by **semantic refactoring rather than additive overlay**. The result should be simpler to reason about than Protocol 5 despite covering a broader scientific-development stack.

## 2. Governing abstraction–realization doctrine

### 2.1 Abstraction is a semantic contract, not vagueness

An abstraction is an intentionally incomplete but normative semantic description. It hides realization choices while preserving the properties that every acceptable realization must satisfy.

For abstraction `A`, let `I(A)` denote its material invariants, required outcomes, assumptions, bounds, validity conditions, observables, and governed semantic relations.

An abstraction is **not** merely a higher-level summary of the current realization. It exists to permit multiple valid realizations without losing the semantics that matter.

The design question at every boundary is:

> Which properties must remain invariant across acceptable realizations, and which properties are merely choices inside the realization search space?

### 2.2 Realization feasibility includes inherited authority and domain-local external constraints

Protocol 5 Tier 1A includes stakeholder, scientific, security, reliability, compatibility, resource, performance, and governed external-contract constraints. SSDP 6 must not accidentally force all such constraints through D1.

A domain realization may therefore be constrained by both inherited upstream abstractions and **domain-local externally governed constraints** that enter directly at the level where they matter.

For realization `R_i` with upstream semantic authorities `A_i1 ... A_in` and domain-local governed constraints `C_i`:

```text
R_i is admissible only if

semantics(R_i) |= I(A_i1) AND ... AND I(A_in) AND C_i
```

Examples:

- a target scientific observable constrains D2-D4 through D1;
- an externally required numerical accuracy or hardware budget may constrain D2 directly;
- a security, reliability, compatibility, deployment, or accelerator requirement may constrain D3 directly;
- a language/compiler/platform or concrete public-interface constraint may constrain D4 directly.

These side constraints are not lower-authority merely because they enter below D1. Their authority comes from their governed source.

### 2.3 Authority source and abstraction level are orthogonal

The D1-D4 hierarchy describes **semantic abstraction level**. It does not by itself determine where a requirement came from or who may change it.

SSDP 6 shall preserve an orthogonal authority-precedence rule:

```text
safety / explicit project and stakeholder authority / governed external contracts
    -> accepted current domain abstractions and ratified decisions
    -> repository/runtime evidence about actual realization state
    -> delegated realization discretion
```

A material external constraint may attach to D1, D2, D3, or D4. Repository code/tests remain evidence of actual state and do not gain authority over accepted intent through existence.

This preserves the protected purpose of Protocol 5 Tier 1A while replacing the software-specific tier vocabulary.

### 2.4 Invariant versus delegated realization

At every abstraction–realization boundary ask:

> Is this property part of the abstraction being realized, or merely one way the current realization satisfies it?

Everything not required by inherited or domain-local governed constraints remains delegated realization space by default.

A realization detail does not become an abstraction invariant merely because it:

- exists;
- is depended upon;
- appears in tests or documentation;
- appeared in a prior workplan;
- survived prior review;
- was previously patched;
- is convenient to verify;
- is named by an acceptance path;
- is currently the only implementation.

Promotion into an abstraction requires explicit acceptance by the abstraction-owning authority and a material semantic reason.

### 2.5 Constrained optimization is conceptual and heuristic, not exhaustive search

If `F_i(R)` denotes domain fitness, the realization problem is conceptually:

```text
choose R* among admissible R
such that domain fitness is best justified;
then prefer minimum justified realization complexity;
then minimize development economy cost.
```

The preference is lexicographic only after all material feasibility constraints are satisfied:

```text
semantic fidelity / governed constraints = feasibility
then
    domain engineering fitness
    > minimum justified realization complexity
    > development economy
```

SSDP does not require mathematical global optimization or exhaustive enumeration of all possible realizations. Agents use bounded, evidence-motivated heuristic search and stop when additional search has lower expected engineering value than proceeding with the best justified admissible realization.

A simple, fast, elegant, familiar, or cheap realization that violates a governing abstraction or external constraint is outside the feasible set rather than merely lower-scoring.

### 2.6 Design and verification are opposite-direction semantic operations, not a bijective inverse

Design is generally one-to-many:

```text
A -> { R | R satisfies A and applicable C }
```

Verification is not the mathematical inverse of Design because many realizations can satisfy the same abstraction. It is the opposite-direction semantic operation:

```text
R -> reconstruct/projection of actual semantics
  -> compare against A and applicable C
  -> attempt to falsify conformity
```

Use the language **inverse semantic direction** or **reverse semantic verification**, not a claim that Design and Verification are bijective inverse functions.

Verification establishes material claims with evidence appropriate to the risk. It need not and usually cannot prove the entire implementation state exhaustively. Formal proof is used where it is the right tool; elsewhere confidence comes from appropriately strong falsification-oriented evidence.

### 2.7 Abstraction adequacy is itself a review obligation

A realization can satisfy an abstraction perfectly while the abstraction omits a material requirement. Therefore every material handoff must challenge both:

1. **realization fidelity** — does the child realize the parent correctly?; and
2. **abstraction adequacy** — does the accepted child abstraction preserve enough of the parent/external authority to constrain the next realization safely?

A too-weak abstraction is a design defect even if every downstream verification against its literal wording passes.

This is the generic form of Protocol 5's independent-evaluator and protected-outcome doctrine.

### 2.8 Real systems form a layered dependency DAG, not necessarily one linear chain

D1-D4 define semantic levels, but a repository may contain:

- several D1 methods sharing one D2 algorithm;
- one D1 formulation realized by several alternative D2 methods;
- multiple D2 methods sharing one D3 subsystem;
- one D3 component realizing obligations from multiple D2 authorities;
- cross-cutting external constraints attached at lower domains.

Therefore the authoritative dependency structure is a **layered directed acyclic graph for a given accepted snapshot**, not necessarily a single parent-child chain.

The pairwise abstraction–realization relation remains fundamental. Multi-parent realizations must satisfy every applicable upstream authority and governed side constraint. Development may iterate over time, but a current authority snapshot must not require circular normative ownership to determine what is true.

### 2.9 Downstream evidence may challenge but never silently redefine upstream authority

A lower-level realization is evidence about what actually exists. It is not retroactive authority over what an upstream abstraction ought to mean.

```text
downstream contradiction
    -> challenge the earliest potentially wrong abstraction
    -> owning authority adjudicates
    -> accepted revision may invalidate dependent descendants
```

Forbidden counterfeit reconciliation:

```text
implementation differs
    -> rewrite architecture to match implementation
    -> rewrite numerical paper to match architecture
    -> rewrite scientific paper to match numerical paper
    -> declare restored consistency
```

unless independent reasoning at each affected authority level establishes those upstream changes as the newly accepted correct semantics.

### 2.10 Change propagation and bounded invalidation

Accepted upstream changes invalidate only dependent downstream authority/evidence whose claim could materially change.

```text
accepted authority change
    -> identify dependent semantic surface
    -> mark affected descendant authority/evidence stale
    -> preserve unrelated accepted authority/evidence
    -> re-realize only as far downward as necessary
    -> re-verify upward across the affected dependency surface
```

Bottom-up observations produce challenges. They do not automatically mutate or supersede upstream authority.

### 2.11 Reopen the earliest materially affected abstraction

Route rework to the earliest/highest domain whose accepted abstraction may be wrong, bounded to the affected semantic surface.

Examples:

```text
local helper/data-structure defect                    -> D4
component ownership/dataflow/state defect             -> D3
discretization/solver/estimator/precision defect      -> D2
observable/model/equation/assumption/meaning defect   -> D1
model/context/evidence mismatch                       -> D1 validation/reconsideration
```

Do not escalate merely because many lower files are affected. Do not keep repair artificially low when the parent abstraction is itself invalid.

### 2.12 External adequacy boundary: validation, proof, standards, and uncertainty

The engineered D1-D4 hierarchy is internally governed by realization verification. D1 also has an external adequacy boundary whose evidence depends on the problem class.

For empirical/model-based science this includes **validation** against intended context and observed reality. For theoretical/mathematical software it may instead include proof, axiomatic consistency, reference theory, or accepted mathematical authority. For engineering software it may include experiments, standards, safety margins, qualification data, or stakeholder context-of-use requirements.

SSDP shall therefore distinguish:

- **verification** — whether a realization faithfully realizes an accepted abstraction;
- **external adequacy/validation** — whether D1 is adequate for its intended scientific/theoretical/engineering context;
- **uncertainty quantification** — characterization/propagation of material uncertainty affecting conclusions.

Do not force empirical validation language onto pure mathematical problems, and do not treat internal numerical verification as empirical scientific validation.

Uncertainty is layer-aware:

- D1 owns data/parameter/model/assumption and scientific interpretive uncertainty as applicable;
- D2 owns discretization, truncation, stochastic numerical, conditioning, and floating-point uncertainty/error as applicable;
- D3/D4 must preserve and expose those semantics without inventing a competing uncertainty model.

## 3. Four-domain hierarchy and boundary rule

SSDP 6.0 defines four first-class semantic domains:

```text
D1  Scientific & Mathematical Formulation
        |
        | defines accepted scientific/mathematical semantics
        v
D2  Algorithm & Numerical Methods
        |
        | defines accepted computational/numerical semantics
        v
D3  Software Architecture
        |
        | defines accepted software-system semantics
        v
D4  Software Implementation
```

Internal reverse verification proceeds upward:

```text
D4 -> reconstruct executable/software semantics -> verify D3
D3 -> reconstruct effective computational semantics -> verify D2
D2 -> reconstruct effective mathematical/scientific semantics -> verify D1
D1 -> external adequacy/validation against its problem-specific authority/evidence
```

### 3.1 D1 — Scientific & Mathematical Formulation

D1 owns, as applicable:

- scientific/research/engineering question and intended context of use;
- target observable, quantity, estimand, objective, or conclusion semantics;
- theoretical, physical, mathematical, or statistical basis;
- definitions, notation, units, frames, signs, indexing, tensor/order conventions;
- mathematical formulation, governing equations, objective, or probabilistic/statistical model;
- initial/boundary conditions;
- symmetries, conservation laws, invariances, exact identities;
- assumptions, closures, and scientifically meaningful approximations;
- identifiability and well-posedness concerns;
- validity regime and known invalid regimes;
- scientific/model/data/parameter uncertainty as applicable;
- literature/reference provenance;
- external adequacy, validation, and falsification strategy;
- human-ratified epistemic decisions when required.

D1 delegates computational/numerical realization unless a property of that realization is itself part of the scientific/mathematical meaning.

### 3.2 D2 — Algorithm & Numerical Methods

D2 realizes applicable D1 authority and becomes a computational abstraction for D3.

D2 owns, as applicable:

- algorithm family and computational formulation;
- discretization and approximation scheme;
- numerical estimator construction;
- solver semantics;
- conditioning and sensitivity;
- consistency, stability, and convergence;
- expected order/rate where meaningful;
- stopping/convergence criteria;
- numerical error budget;
- discretization/truncation error;
- floating-point/roundoff/cancellation/range requirements;
- stochastic/randomized semantics;
- numerical reproducibility requirements;
- reference/direct/slow oracle methods;
- analytical, limiting, and manufactured-solution checks where appropriate;
- degeneracies and numerical failure regimes;
- computational complexity/scaling envelope;
- admissible numerical alternatives and equivalence criteria;
- accuracy/performance trade space without silent scientific-fidelity loss.

D2 delegates software ownership, storage, APIs, concurrency mechanism, persistence, and low-level realization unless a software property is necessary to preserve numerical semantics.

### 3.3 D3 — Software Architecture

D3 realizes applicable D2 authority plus D3-local governed constraints and becomes the software-system abstraction for D4.

D3 owns, as applicable:

- semantic/component ownership;
- package/module/service boundaries;
- interfaces and dependency direction;
- authoritative representations;
- data/control flow;
- state and lifecycle;
- persistence/checkpoint/cache authority;
- concurrency/orchestration architecture;
- resource/backend/hardware realization policy;
- compatibility/migration boundaries;
- fault/recovery semantics;
- security/trust boundaries;
- architecture-fitness rules;
- mapping from algorithmic responsibilities to software owners.

D3 must not redefine inherited D2 meaning merely because a software decomposition is convenient.

### 3.4 D4 — Software Implementation

D4 realizes applicable D3 authority plus inherited D1/D2 constraints and D4-local governed constraints.

D4 owns delegated realization such as:

- concrete functions/classes/templates/modules within architectural ownership;
- local data structures;
- helpers and idioms;
- libraries/tool use;
- low-level control flow and optimizations;
- code/refactor execution;
- executable tests and evidence machinery;
- repository reconciliation;
- concrete implementation specifications/public contracts delegated by D3.

D4 may remove, replace, consolidate, or simplify local machinery while preserving all applicable upstream constraints.

The abstraction–realization relation may recurse below D4 internally, but SSDP stops creating additional authority-bearing lifecycle roles at code/implementation unless future evidence justifies a protocol redesign.

### 3.5 Cross-cutting concerns are classified by semantic effect, not topic label

A concern belongs to the highest abstraction whose semantics it can change, not to a fixed domain merely because of its name.

Examples:

- an accuracy requirement that changes the estimator/error envelope -> D2;
- parallel summation order that changes estimator semantics -> D2;
- choice of distributed ownership/process topology with unchanged numerical semantics -> D3;
- choice of mutex/thread primitive under accepted concurrency architecture -> D4;
- security/trust policy -> usually D3 external constraint;
- a concrete secure API implementation -> D4;
- accelerator availability policy -> D3 when architectural;
- kernel precision/vectorization -> D4 unless it changes D2 numerical guarantees.

This rule prevents duplicated ownership across domain-specific references and language profiles.

## 4. One-to-one durable documentation correspondence

SSDP 6.0 shall establish a first-class durable documentation stack aligned with the abstraction hierarchy:

```text
D1 -> Scientific Method Paper / canonical scientific-method document family
D2 -> Numerical & Algorithmic Method Paper / canonical numerical-method document family
D3 -> Architecture Manual / canonical architecture document family
D4 -> Specification + Code Base
```

The correspondence is **logical one-to-one semantic ownership**, not a requirement that every project keep exactly one physical Markdown file per domain. Large packages may use a coherent document family, shared method authorities, and per-capability papers. Each material claim must nevertheless have exactly one current normative semantic owner.

These are current-state records, not implementation chronology. Together they should let a competent researcher reconstruct the package from scientific intent through executable behavior without source archaeology or lost conversation history.

### 4.1 Normative authority is scoped inside a document

Calling a method paper normative does not make every sentence, citation, historical discussion, or pedagogical explanation an invariant.

Templates and doctrine shall distinguish, semantically and proportionately:

- accepted definitions/formulation/assumptions/contracts/validity conditions — normative for that domain;
- derivation, motivation, discussion, literature survey, examples, and evidence — supporting explanation/evidence unless explicitly adopted as a governed claim.

External literature is evidence/provenance. It does not automatically override the project's accepted current formulation.

### 4.2 D1 Scientific Method Paper

Owned semantically by `scientific-formulation`.

It is the canonical current authority for D1 and should contain, proportionately:

1. background/scientific context;
2. motivation and problem statement;
3. goals and intended context of use;
4. theoretical foundation;
5. definitions, notation, conventions, units;
6. mathematical formulation;
7. assumptions, closures, and approximations;
8. validity regime and limitations;
9. observable/estimand/objective definitions;
10. external adequacy/validation/falsification strategy;
11. model/data/parameter uncertainty where material;
12. relation to prior literature and project-specific adaptations;
13. references/provenance;
14. delegated D2 realization space.

### 4.3 D2 Numerical & Algorithmic Method Paper

Owned semantically by `numerical-algorithm-design`.

It is the canonical current authority for D2 and should contain, proportionately:

1. inherited D1 problem;
2. computational objective and numerical motivation;
3. algorithmic formulation;
4. discretization/estimation/approximation method;
5. algorithmically material data/operation model;
6. pseudocode/flow where useful;
7. conditioning/sensitivity;
8. consistency/stability/convergence reasoning;
9. numerical error model/budget;
10. tolerance/precision/stopping/resolution policy;
11. stochastic semantics;
12. trusted reference/oracle algorithm;
13. analytical/limiting/manufactured/reference cases;
14. degenerate/failure regimes;
15. complexity/scaling characteristics;
16. accepted performance/fidelity trade space;
17. relation to standard algorithms/literature/project adaptations;
18. delegated D3 realization space.

It must not merely restate D1 in implementation vocabulary.

### 4.4 D3 Architecture Manual

Owned semantically by `software-design`.

It documents the accepted realization of D2 and applicable D3-local constraints in terms of software ownership, boundaries, representations, interfaces, data/control flow, state, persistence, concurrency, resource/backend policy, compatibility, failure/security semantics, and mapping from algorithmic responsibility to software owner.

It must not become the canonical owner of D1/D2 meaning merely because those semantics are represented in software.

### 4.5 D4 Specification and Code Base

Owned operationally by `software-implementation`, subject to all accepted parent authority.

D4 contains two distinct surfaces:

- **D4 specification** — the normative human-readable owner for concrete delegated software contracts such as API/CLI/configuration, schema/format, software-boundary units/shapes/order/precision, persistence, compatibility/migration, and durable error/fallback semantics where those are not already fixed upstream;
- **code/executable behavior** — the actual realization and strongest evidence of what the software currently does.

Code disagreement with an accepted D4 specification is not permission to rewrite the specification. It is first an implementation-conformance problem unless independent authority shows the specification itself must change.

The code base therefore remains evidence/realization, not automatic intended authority. This preserves Protocol 5's anti-counterfeit specification rule while respecting the user's D4 `Specification + Code Base` documentation layer.

### 4.6 Current, proposed, accepted, challenged, stale, superseded, and release-pinned states

A normative paper/manual/specification must not become current authority merely because an agent drafted an edit.

SSDP shall distinguish at least these semantic states without requiring a heavy database:

- **proposed** — candidate change; not current authority;
- **accepted current** — governing current semantic authority;
- **challenged** — current authority has evidence questioning it but remains the explicit authority until adjudicated or marked unusable by policy;
- **stale dependent** — a descendant artifact/evidence claim is no longer sufficient because an upstream accepted change may affect it;
- **superseded/historical** — no longer current authority;
- **release-pinned/publication snapshot** — intentionally frozen to a release/publication and not edited to track future current behavior.

Human-ratification state is orthogonal and may be `not_required`, `required/pending`, `accepted`, or `rejected`.

Exact metadata syntax is delegated. The semantic distinctions are not.

### 4.7 Atomic authority mutation

For material changes to a current normative abstraction:

```text
propose in a workplan/change artifact
    -> independently review/falsify
    -> obtain required human ratification
    -> accept the new abstraction
    -> update the canonical current normative document
    -> mark dependent descendants/evidence stale as applicable
    -> realize downward
    -> verify upward
```

Do not edit a current D1/D2/D3 authority into a speculative state and then ask downstream agents to infer which sentences are accepted.

An accepted change may be committed together with its current document update; the protocol does not require a separate database transaction. The requirement is semantic atomicity, not implementation machinery.

### 4.8 Publication and documentation specialist boundary

`software-documentation` remains useful for editorial synthesis, information architecture, publication, generated artifacts, user guides, and cross-document navigation.

It is subordinate to domain semantic owners and may not approve or invent D1/D2/D3 meaning.

Publication-ready PDF/article outputs may be derived from current method sources or intentionally release-pinned. Published historical snapshots must not be rewritten merely because current science evolves.

## 5. Authority-bearing roles and boundary ownership

SSDP 6.0 introduces four authority-bearing lifecycle roles:

```text
scientific-formulation
        -> numerical-algorithm-design
        -> software-design
        -> software-implementation
```

This is an incompatible lifecycle/governing-doctrine change and therefore requires Protocol major version 6.

### 5.1 Generic boundary responsibility

For a material boundary `A -> R`:

- the upstream/domain owner defines and maintains the accepted abstraction;
- the downstream owner constructs the realization and produces conformance evidence;
- the upstream owner accepts or rejects the child's fidelity to the upstream abstraction;
- for substantial/high-risk claims, the acceptance pass should be operationally independent from the child authoring context when practical, using fresh-context falsification-oriented review;
- no separate permanent verifier role is required;
- required human ratification overlays acceptance where policy says the epistemic decision is human-owned.

A child role may and should self-verify during design/implementation, but self-checking does not replace required independent parent-boundary review.

### 5.2 `scientific-formulation`

Owns D1 design, current authority maintenance, D1 external-adequacy reasoning, D1->D2 handoff, and acceptance/review of D2 fidelity to D1.

Responsibilities include:

- recover/define the scientific/theoretical/engineering question independently of current code;
- reconcile literature, accepted equations, experiments, standards, and intended context;
- derive/critique mathematical formulation;
- identify assumptions, approximations, validity regimes, uncertainty, and falsification criteria;
- maintain the accepted-current Scientific Method Paper;
- adjudicate D1 challenges;
- route material human-ratification decisions.

It does not own D2 numerical mechanism, D3 software architecture, or D4 code.

### 5.3 `numerical-algorithm-design`

Owns D2 design, current authority maintenance, D1->D2 realization, D2->D3 handoff, and acceptance/review of D3 computational fidelity to D2.

Responsibilities include:

- translate accepted D1 semantics into a computational/numerical problem;
- select/derive admissible numerical algorithms;
- reason about conditioning, consistency, stability, convergence, precision, stochastic semantics, and error budgets;
- define reference/oracle methods and numerical verification strategy;
- maintain the accepted-current Numerical & Algorithmic Method Paper;
- adjudicate D2 challenges;
- escalate to D1 when numerical evidence invalidates a scientific/mathematical premise.

It does not own D3 decomposition except where a software property is necessary to preserve D2 semantics.

### 5.4 `software-design`

Protocol 5 Software Design shall be narrowed to D3.

It retains strong doctrine for:

- software architecture/ownership;
- interfaces/data/state/persistence/concurrency/resources/security;
- minimum justified software-system complexity;
- D3->D4 workplans;
- acceptance-boundary design;
- independent D4 review;
- active simplicity and architecture stabilization;
- architecture fitness and affected-surface reasoning.

It consumes D2 authority instead of inventing or silently freezing D1/D2 semantics.

### 5.5 `software-implementation`

Retains D4 execution authority and most Protocol 5 implementation doctrine.

It implements accepted D3 while preserving applicable D1/D2/D3 and D4-local constraints, runs executable evidence, reconciles affected surfaces, maintains delegated D4 specification/code coherently, simplifies delegated machinery, and routes invalidated parent abstractions upward instead of silently changing them.

## 6. Generic change-plan and handoff contract

Protocol 5's implementation workplan is too software-specific to be the only transition artifact in a four-domain protocol.

SSDP 6 shall refactor toward **one generic abstraction–realization change-plan contract**, specialized only where a domain materially needs additional fields. Do not create four nearly identical workplan templates.

A material D1/D2/D3/D4 change plan records, proportionately:

- external/problem authority and affected upstream abstractions;
- current accepted authority being changed or realized;
- target abstraction/realization outcome;
- invariants/required outcomes;
- domain-local governed constraints;
- assumptions/validity conditions;
- accepted child-abstraction decisions that constrain the next domain;
- delegated realization space;
- non-goals;
- verification/acceptance relations and real semantic owners;
- oracle/reference sources;
- uncertainty/error budget where material;
- affected dependency surface;
- genuine reopen/simplification triggers;
- authority state and required human-ratification state;
- protocol/profile version binding.

The existing implementation workplan may become a D3->D4 specialization of this generic contract or be refactored into it. Preserve its strong proxy-proof acceptance, affected-surface, active-simplicity, and evidence clauses.

A handoff must be snapshot-complete for still-binding task-specific semantics without requiring Git history, lost chat, unsupplied papers, or superseded artifacts. It must not duplicate whole method papers merely for ceremony; references to supplied current canonical authorities are valid composition.

## 7. Verification ladder and composed scientific closure

### 7.1 D4 -> D3: implementation conformance verification

Question:

> Does the assembled executable software faithfully realize the accepted D3 architecture and applicable concrete D4 contracts?

Evidence may include focused tests, stage-local/final affected regression, integration/end-to-end paths, structural checks, architecture fitness, real-owner execution, property/stateful testing, mutation/counterfactual evidence, failure injection, static analysis, sanitizers, and independently required production qualification.

### 7.2 D3 -> D2: computational realization verification

Question:

> Does the assembled software architecture and execution path realize the accepted D2 method without changing its computational semantics?

Evidence may include algorithm-stage-to-owner mapping, trusted-reference comparison, numerical invariants, backend equivalence, ordering/reduction semantics, precision/tolerance checks, restart equivalence, stochastic semantics, and final governed-observable comparison.

### 7.3 D2 -> D1: mathematical/scientific fidelity verification

Question:

> Does the accepted D2 method solve/estimate the D1 formulation within its governed approximation and numerical-error envelope?

Evidence may include analytical cases, manufactured solutions where valid, refinement/convergence studies, observed order, residual/error analysis, conditioning, exact invariants, symmetry/conservation, bias/variance analysis, sensitivity, cross-method comparison, and independent derivation.

### 7.4 D1 -> external authority: adequacy/validation

Question:

> Is D1 adequate for its intended scientific, mathematical, or engineering context, and are conclusions supported within understood uncertainty?

Evidence depends on problem class: experiments/reference data, held-out validation, model discrepancy analysis, uncertainty quantification, parameter identifiability, standards, proof/theory, external literature, domain-expert judgment, and falsification tests.

### 7.5 Adjacent verification is necessary but not always sufficient

Even when every adjacent contract appears satisfied, an omitted or underspecified invariant can allow the assembled product to violate the original scientific intent. Therefore material/high-risk scientific changes require a **composed end-to-end closure check** proportionate to risk:

```text
actual D4 executable behavior
    -> final governed numerical observables
    -> D2 error/equivalence envelope
    -> D1 scientific/mathematical meaning
    -> external adequacy/validation evidence where applicable
```

This is not a mandatory production-scale run. A bounded representative reference case may be sufficient. The purpose is to detect semantic loss at interfaces and incomplete abstractions that pairwise local checks missed.

## 8. Human-in-the-loop scientific authority

SSDP shall increase autonomy without blindly delegating consequential scientific authority to agents.

Agents may autonomously perform substantial upstream work including literature search/synthesis, derivation reconstruction, consistency checking, alternative generation, symbolic/numerical sanity checks, sensitivity/convergence studies, falsification attempts, traceability maintenance, proposed method-paper edits, and downstream propagation of already accepted changes.

Human ratification is normally required before materially accepting changes to:

- research/scientific question or intended interpretation;
- target observable/estimand/objective semantics;
- governing physical/statistical/modeling assumptions;
- closures or mathematical formulation with scientific consequence;
- context-of-use/validity regime;
- approximation that can alter scientific conclusions;
- scientific/model uncertainty assumptions;
- acceptance of unexplained model-data discrepancy;
- D2 algorithm changes that materially alter scientific/numerical guarantees or interpretation;
- numerical error budgets/tolerances where conclusions can change.

Projects may explicitly delegate lower-risk classes after establishing a policy. Human approval is semantic-risk based, not a mandatory synchronous gate between every domain.

Required human approval state and scope must be durable enough for later agents to know what was accepted. The protocol must not require storing unnecessary personal identity data merely to prove that a gate occurred.

The orchestrator may represent and route ratification state but may never self-approve a decision that policy assigns to a human.

## 9. Sparse semantic lineage without a parallel requirements system

Cross-layer dependency knowledge is necessary for bounded invalidation, but SSDP must not create a universal graph/database merely because graph language is convenient.

Projects shall be able to represent material relations such as:

```text
scientific observable
    -> mathematical estimator
        -> numerical estimator
            -> architecture owner
                -> implementation semantic owner
                    -> verification evidence
```

Possible relation classes include:

- realizes / constrained-by;
- depends-on;
- verifies / evidence-for;
- supersedes/revises;
- stale-because-of.

Durable claim IDs are optional unless they materially improve correctness, impact analysis, publication, or automation. Section anchors, document references, workplan mappings, or profile metadata may be sufficient.

The requirement is **bounded traceability of material semantic dependencies**, not a separate lineage product.

## 10. Recasting Protocol 5 doctrine in SSDP language

### 10.1 Tier 1A product/problem truth

Preserve its protected purpose as **governed external/domain constraints plus accepted parent-abstraction invariants**. Do not collapse external constraints into D1.

### 10.2 Tier 1B Frozen architecture

Generalize into **accepted child abstraction for a realization cycle**. Every domain may freeze only material child-abstraction decisions needed to constrain the next realization.

### 10.3 Tier 2 delegated machinery

Generalize into **delegated realization space** at each boundary.

### 10.4 Tier 3 development economy

Preserve as optimization after feasibility and minimum justified realization complexity.

### 10.5 Active simplicity

Generalize to realization simplification at any layer. Before adding another durable correction around accumulating exceptions, compensating assumptions, duplicated authority, wrappers, synchronized states, or heuristic patches, ask whether the current realization can be removed, narrowed, consolidated, rederived, or replaced while preserving governing authority.

This applies to scientific models, numerical methods, software architecture, and code. Never simplify by silently weakening the parent abstraction or external constraint.

### 10.6 Affected surface

Generalize to **affected semantic dependency surface** spanning descendant methods, architecture, implementation, tests, papers, specifications, validation evidence, benchmarks, profile state, and published/release-pinned conclusions. Affected-surface expansion does not mint new upstream requirements.

### 10.7 Proxy-proof acceptance

Generalize to semantic-owner proof at every layer. Evidence that could remain green while the actual formulation/method/architecture/implementation owner is wrong cannot close that claim.

### 10.8 Evidence reuse/invalidation

Reuse evidence until a changed authority/realization dimension can plausibly alter its claim. Invalidate only dependent evidence; final assembled D4 regression/integration rules remain intact.

### 10.9 Independent review and Verification

Retain fresh-context, falsification-oriented independent review. Make it available at every material abstraction boundary without proliferating verifier roles.

### 10.10 Snapshot-complete handoff

Generalize to all domain transitions and current normative document stacks.

### 10.11 Convergence and recurrence

Repeated failures are evidence about the shared semantic owner, not proof that the current realization must survive. Broaden to the earliest shared abstraction/mechanism and simplify before another additive repair when structural evidence warrants it.

### 10.12 Long-horizon quality

Long-horizon audit, documentation, language-profile, testing, performance, security, storage, and tool-routing doctrine must be made domain-aware where they currently assume Software Design owns scientific/numerical semantics. Do not duplicate those references per domain.

## 11. Required protocol artifacts and repository changes

### 11.1 New role skills

Create:

```text
source/roles/scientific-formulation/SKILL.md
source/roles/numerical-algorithm-design/SKILL.md
```

and generated installable distributions under existing source->dist rules.

### 11.2 Refactor existing roles

Refactor:

```text
source/roles/software-design/SKILL.md
source/roles/software-implementation/SKILL.md
```

so D3/D4 participate in the recursive model without retaining duplicate D1/D2 authority.

### 11.3 Canonical shared doctrine

Introduce/refactor the minimum canonical references needed to own:

- abstraction–realization doctrine and authority provenance;
- scientific/mathematical formulation and external adequacy/validation;
- numerical/algorithmic design and numerical verification;
- cross-domain workflow, change plans, handoffs, authority state, reopen/invalidation;
- four-layer documentation ownership;
- human scientific ratification;
- bounded semantic lineage;
- SSDP 6 versioning/compatibility/migration.

Prefer moving/splitting existing content over parallel `ssdp-*` duplication. Existing `scientific-software.md`, `scientific-technical-writing.md`, `workflow-and-workplans.md`, `architecture-and-design.md`, `testing-and-validation.md`, `documentation-maintenance.md`, language profiles, and long-horizon doctrine must be reconciled with the new ownership model.

### 11.4 Generic change-plan and document templates

Add/refactor lightweight templates for:

- generic abstraction–realization change plan/handoff;
- Scientific Method Paper;
- Numerical & Algorithmic Method Paper;
- Architecture Manual guidance where current doctrine is insufficient;
- D3->D4 implementation workplan/specification linkage.

Do not create one near-duplicate workplan template per domain unless evidence proves a specialization necessary.

### 11.5 Qualification

Extend protocol qualification with behavior scenarios that exercise authority routing and semantic falsification, not only static phrase tests.

### 11.6 Workflow prompt/profile changes

Extend human-facing workflow prompts and the protocol profile to represent four domains, affected-domain routing, current/proposed/stale authority, verification target, and human ratification as needed.

### 11.7 Protocol version and historical recovery

`source/PROTOCOL_VERSION` remains `5.16` until the complete SSDP 6 candidate is coherent and independently accepted.

Before switching to 6.0, establish and test an immutable historical-resolution path from Protocol `5.16.0` to a known source/bundle identity, such as an immutable tag/release/commit mapping. The exact mechanism is delegated; silent use of `main`/latest for a 5.16 workplan is forbidden.

The existing packaged `sdp-protocol-5.16` orchestrator profile and its semantics must remain recoverable after 6.0 release.

Repository rename remains explicitly deferred.

## 12. Workflow architecture and affected-domain routing

SSDP must not become a mandatory four-domain waterfall.

Before mutation, classify the **highest potentially affected semantic domain** plus applicable side constraints. A claim that a change is D4-only or D3-only should include a proportionate upstream-impact check when there is plausible scientific/numerical risk.

Full scientific change example:

```text
external question/evidence
    -> proposed D1 change
    -> D1 review + human ratification when required
    -> accept current D1 / invalidate dependent descendants
    -> D2 realization + D1 acceptance of D2 fidelity
    -> D3 realization + D2 acceptance of D3 computational fidelity
    -> D4 implementation + D3 acceptance of D4 fidelity
    -> composed end-to-end scientific closure when material
    -> current documentation/specification reconciliation
    -> closeout
```

Reduced examples:

```text
software-local architecture change:   D3 -> D4 -> verify D4 against D3
pure implementation refactor:         D4 only, after plausible upstream-impact exclusion
numerical optimization:               D2 -> D3 -> D4 -> verify back to D1 as affected
scientific formulation change:        D1 downward through dependent descendants
```

Routing rule:

> Start at the earliest/highest abstraction whose accepted semantics or applicable external constraints may materially change; realize downward only through dependent surfaces; verify back upward through the affected semantic dependency graph.

Do not require unaffected sibling branches of the authority DAG to rerun merely because they share a repository.

## 13. Scientific and numerical oracle doctrine

D2 doctrine should route proportionately among:

- dimensional/unit consistency;
- analytical/exact/limiting/asymptotic cases;
- manufactured solutions where valid;
- residual checking;
- conservation/invariant checks;
- mesh/time-step/order refinement;
- observed convergence order;
- Richardson/extrapolation methods where justified;
- conditioning/sensitivity;
- forward/backward error;
- floating-point range/cancellation/precision analysis;
- reference/direct solver comparison;
- cross-implementation differential testing;
- stochastic convergence/bias/variance;
- numerical uncertainty propagation;
- seed/backend/precision robustness;
- accuracy/performance Pareto analysis.

D1 doctrine should route proportionately among:

- empirical validation where applicable;
- calibration-versus-validation separation;
- parameter identifiability;
- model discrepancy;
- sensitivity to assumptions;
- falsification/counterexample design;
- proof/theory/standards where appropriate;
- external literature reconciliation;
- scientific/model uncertainty quantification;
- robustness of conclusions to plausible alternative models.

Select the cheapest sufficiently strong evidence for the claim. Escalate when risk, ambiguity, failed falsification, or conflicting authorities warrant it.

## 14. Protocol qualification

SSDP 6 acceptance must include adversarial behavioral scenarios. At minimum cover:

1. code matches architecture but the governing equation has the wrong sign;
2. architecture faithfully implements the wrong estimator;
3. numerical algorithm converges reliably to the wrong continuous model;
4. tests duplicate the implementation's incorrect formula and all pass;
5. tolerance is widened solely to make an optimized backend pass;
6. reduced precision introduces scientifically meaningful bias while unit tests remain green;
7. D2 paper and implementation use different normalizations;
8. units are numerically compatible but physically interpreted incorrectly;
9. stable stochastic estimator is biased relative to D1;
10. observed convergence order degrades after optimization;
11. boundary-condition implementation changes modeled physics;
12. calibration data is reused as validation evidence;
13. parallel reduction/summation exceeds the numerical error budget;
14. restart/checkpoint behavior changes a stochastic estimator;
15. implementation is used to rewrite upstream authority without adjudication;
16. one D1 observable changes and unrelated descendant evidence is invalidated unnecessarily;
17. software-local refactor escalates to D1/D2 despite unchanged semantics;
18. numerical contradiction is treated as local code defect instead of reopening D2;
19. human-owned scientific decision is self-approved by an agent;
20. historically coherent method paper no longer represents accepted current science;
21. a draft D1/D2 paper edit is incorrectly treated as current authority before acceptance;
22. code conflicts with accepted D4 specification and the specification is rewritten merely to match code;
23. D3 security/reliability constraint entering directly from project authority is lost because it is absent from D1;
24. one shared D3/D4 realization serves multiple D2 authorities and a change to one incorrectly invalidates all siblings;
25. a realization has two applicable upstream authorities and satisfies only one;
26. all adjacent checks pass but an end-to-end governed observable violates D1 because an intermediate abstraction omitted a necessary invariant;
27. release-pinned/published method paper is rewritten to follow current science rather than preserved as historical publication truth;
28. pure mathematical/theoretical software is forced through meaningless empirical validation instead of proof/reference-theory adequacy;
29. a D4-only claim is accepted without checking an obvious possible D2 precision/ordering impact;
30. supporting literature prose is treated as stronger normative authority than the project's accepted D1 formulation;
31. a lower-domain hardware/performance constraint is incorrectly promoted into D1 merely to fit a linear hierarchy;
32. a candidate introduces circular normative ownership between documents so no authority can be resolved independently.

Qualification should test role routing, authority provenance, correct reopen domain, current-vs-proposed document state, multi-parent constraints, documentation ownership, bounded invalidation, D4 spec/code precedence, composed scientific closure, and refusal to counterfeit completion.

## 15. Orchestrator compatibility and profile evolution

The orchestrator architecture correctly makes workflow routing profile-owned and keeps Core/Tracker/Adapters/Scheduler subordinate to protocol intent. Preserve that architecture.

Do not hard-code SSDP scientific semantics independently into Tracker, Adapters, or Scheduler.

The existing Protocol 5.16 profile schema is stage-oriented and versioned. SSDP 6 may extend it only as far as the accepted workflow semantics require. If required domain/dependency/authority-state semantics cannot be represented safely as backward-compatible additive fields, create a new `profile_schema_version` rather than overloading version-1 fields.

The orchestrator must then support the required old/new schema versions explicitly while preserving the immutable `sdp-protocol-5.16` profile.

SSDP 6 profile semantics may need to represent:

- domain identity;
- role owner;
- artifact/authority kind;
- upstream authority dependencies, potentially multiple;
- domain-local governed constraints;
- verification target;
- affected-domain/invalidation edges;
- accepted/proposed/stale state as required for routing;
- recognized outcomes;
- human-ratification requirement/state;
- reopen/routing semantics.

Tracker may project these states and recommend next actions. It must not independently infer scientific truth from code or user telemetry.

Scheduler/resource optimization may select among engineering-sufficient execution routes only after protocol-required domain/authority constraints and human gates are satisfied.

## 16. Migration strategy

### Phase 0 — Parent authority review/freeze

Independently review this workplan for conceptual completeness, loss of Protocol 5 guarantees, lifecycle/document ambiguity, and unnecessary machinery. Do not begin broad skill edits until this parent authority passes.

### Phase 1 — Core recursive doctrine and compatibility scaffold

Create/refactor the canonical abstraction–realization doctrine, authority-precedence model, generic change-plan semantics, and versioning/migration rules.

Acceptance:

- feasibility includes inherited abstractions plus domain-local external constraints;
- abstraction level and authority source are orthogonal;
- Design/Verification opposite-direction relation is explicit without claiming bijective inversion;
- abstraction adequacy is reviewable;
- multi-parent layered DAG semantics are supported;
- upward challenge/downward invalidation are explicit;
- external adequacy/validation is distinguished from internal verification;
- immutable Protocol 5.16 recovery path is designed before 6.0 cutover.

Do not make `source/README.md` or `PROTOCOL_VERSION` claim current 6.0 authority before the complete candidate is coherent.

### Phase 2 — D1 scientific-formulation role and paper

Implement D1 role, accepted/proposed Scientific Method Paper semantics, external adequacy/validation/UQ doctrine, provenance rules, and HITL policy.

### Phase 3 — D2 numerical-algorithm-design role and paper

Implement D2 role, Numerical & Algorithmic Method Paper, D1->D2 handoff/review, error/convergence/conditioning/oracle doctrine, and numerical uncertainty.

### Phase 4 — Narrow/refactor D3 Software Design

Remove D1/D2 semantic ownership from Software Design while preserving architecture/workplan/acceptance/active-simplicity/resource/security/tool-routing strengths. Reclassify cross-cutting references by semantic effect.

### Phase 5 — Adapt D4 Software Implementation and specification semantics

Teach Implementation to consume applicable upstream authorities/side constraints, preserve D4 spec-versus-code precedence, maintain affected-surface regression/integration, and route parent invalidation upward.

### Phase 6 — Four-layer documentation architecture

Refactor documentation doctrine for logical one-to-one domain correspondence, current/proposed/release-pinned state, scoped normative sections, publication derivation, and semantic-owner/editorial-specialist separation.

### Phase 7 — Minimal dependency lineage and affected-domain routing

Implement only the minimum representation necessary to identify material cross-layer dependencies, stale descendants, and reopen routing. Prefer existing document links/workplans/profile structures before new registries.

### Phase 8 — Workflow prompts and protocol profile

Add affected-domain routing and human/authority-state support. Evolve profile schema version only if semantically required; preserve 5.16 profile behavior.

### Phase 9 — Protocol qualification and self-review

Run static/source-package validation plus adversarial behavioral qualification, including multi-parent, side-constraint, draft-authority, spec/code, and end-to-end composition cases.

Review whether SSDP itself introduced avoidable bureaucracy or duplicated authority; simplify before release where equivalent semantics survive.

### Phase 10 — Orchestrator SSDP 6 integration

After SSDP 6 profile semantics are accepted, update orchestrator support minimally. Preserve profile ownership and 5.16 compatibility; reopen orchestrator architecture only on evidence.

### Phase 11 — Atomic release/closeout

Before release:

- establish/test immutable 5.16 protocol-source/profile recovery;
- set `PROTOCOL_VERSION` to `6.0.0` only on the coherent accepted candidate;
- regenerate all skill distributions;
- validate source/dist coherence;
- update root/source README and portability guidance;
- run repository tests/package checks and new behavioral qualification;
- verify 5.16 and 6.0 profile resolution independently;
- perform independent final Review;
- archive this workplan only after Pass;
- leave repository rename as separate user-controlled work.

Do not publish a mixed current state where canonical docs claim 6.0 while required roles/profile/distributions still encode 5.16 semantics.

## 17. Required implementation obligations

### Obligation A — Make recursive abstraction–realization the primary doctrine

**Required end state:** protocol-wide language centers on abstraction invariants, applicable governed constraints, delegated realization space, constrained realization search, abstraction adequacy, reverse semantic verification, and bounded invalidation.

**Anti-shortcut:** do not add new prose above unchanged software-specific authority semantics.

### Obligation B — Preserve authority provenance and lower-domain external constraints

**Required end state:** user/project/safety/external contracts remain authoritative and may constrain any domain directly. D1 is not a universal dumping ground for every product constraint.

### Obligation C — Establish four true authority-bearing domains

**Required end state:** D1-D4 have distinct semantic ownership, mutation/acceptance authority, handoff/reopen behavior, and verification responsibility.

**Anti-shortcut:** D1/D2 are not optional documentation specialists under Software Design.

### Obligation D — Establish logical one-to-one normative documentation ownership

**Required end state:** D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification+Code correspond to the four domains with exactly one current semantic owner per material claim.

**Anti-shortcut:** do not interpret one-to-one as mandatory monolithic files or make every explanatory sentence normative.

### Obligation E — Define current/proposed/stale authority semantics and atomic acceptance

**Required end state:** speculative edits cannot become current authority accidentally; accepted upstream changes invalidate only dependent descendants; publication/release-pinned snapshots remain historical.

### Obligation F — Preserve D4 specification/code distinction

**Required end state:** accepted D4 specification is intended concrete contract; code is actual realization/evidence. Neither may silently rewrite higher authority, and implementation disagreement does not automatically bless code.

### Obligation G — Generalize Verification without false invertibility or false completeness

**Required end state:** every material boundary supports reverse semantic reconstruction/falsification; the doctrine does not claim Design is bijective or that finite tests prove total semantics.

### Obligation H — Add composed end-to-end scientific closure where risk warrants it

**Required end state:** important assembled claims can be checked from executable observables through D2 error semantics to D1 meaning/external adequacy rather than relying exclusively on pairwise contract checks.

### Obligation I — Add risk-sensitive human scientific ratification

**Required end state:** consequential D1 and scientifically material D2 decisions cannot be silently self-approved, while routine delegated work remains autonomous.

### Obligation J — Provide bounded multi-parent dependency tracing and invalidation

**Required end state:** shared/multi-authority realizations satisfy all applicable parents and invalidate only affected descendants without requiring a universal graph database.

### Obligation K — Preserve Protocol 5 strengths by refactoring, not duplication

**Required end state:** active simplicity, proxy-proof acceptance, snapshot-complete handoff, affected regression/integration, evidence reuse/invalidation, convergence, language profiles, tool routing, long-horizon quality, resource/security/performance doctrine, and version binding remain effective.

### Obligation L — Keep SSDP proportional

**Required end state:** reduced profiles support software-only/local work. The protocol does not force four papers, four reviews, or four stages when upstream domains are absent/unaffected.

### Obligation M — Preserve historical Protocol 5.16 and orchestrator authority separation

**Required end state:** 5.16 workplans/profile remain resolvable under 5.16 semantics; SSDP 6 profile may evolve schema explicitly; orchestrator never becomes scientific authority.

### Obligation N — Self-qualify adversarially

**Required end state:** Protocol 6 passes deceptive scientific/numerical/authority/document-state scenarios, not only static wording tests.

## 18. Delegated implementation space

Delegated unless evidence requires a Frozen decision:

- exact final role names;
- exact reference/template filenames;
- physical document directory/file topology;
- whether D1 science and mathematics use one or several files within one semantic document family;
- exact proposed/current/stale metadata syntax;
- exact dependency-link/claim-ID syntax;
- exact profile-schema field names and whether SSDP 6 requires schema v2;
- exact qualification harness implementation;
- exact symbolic/numerical tools named as examples;
- exact publication/PDF stack;
- exact human-approval UI;
- exact immutable historical-ref mechanism, provided 5.16 recovery is deterministic and tested.

Prefer reduction, movement of authority, and refactoring. New durable machinery must provide a capability the simplified existing system cannot express cleanly or replace broader duplicated machinery.

## 19. Explicit non-goals

- Do not rename the repository under this workplan.
- Do not reinterpret historical Protocol 5 workplans under SSDP 6.
- Do not force non-scientific software to invent D1/D2 documents.
- Do not force a linear four-stage waterfall.
- Do not force every project into exactly four physical files.
- Do not make documentation volume a rigor proxy.
- Do not require formal proof where empirical/numerical evidence is appropriate.
- Do not force empirical validation onto pure theoretical/mathematical problems.
- Do not let validation substitute for numerical/software verification or vice versa.
- Do not create a universal requirements/claim graph or semantic database.
- Do not make orchestrator/Tracker scientific authority.
- Do not turn HITL into human-in-every-loop.
- Do not preserve obsolete Protocol 5 duplication merely for wording compatibility inside 6.0.
- Do not create wrappers around role-boundary defects that are solved more cleanly by moving ownership.
- Do not make code automatically normative when it contradicts accepted specification.
- Do not make every literature citation or explanatory paragraph a normative scientific invariant.
- Do not assume one parent abstraction when a realization genuinely serves several authorities.

## 20. Acceptance criteria

SSDP 6.0 is release-ready only when all are true.

### Conceptual closure

- abstraction is defined as an intentionally incomplete normative semantic contract;
- realization feasibility includes inherited authority plus domain-local governed constraints;
- abstraction level and authority source are orthogonal;
- fidelity is a feasibility condition, not a weighted objective;
- realization search is proportionate heuristic engineering rather than a false global-optimum requirement;
- Design and Verification are opposite-direction semantic operations without false bijective-inverse claims;
- abstraction adequacy/incompleteness can block handoff;
- multi-parent layered-DAG semantics are supported;
- upward challenge/downward bounded invalidation are unambiguous;
- external adequacy/validation and layer-aware uncertainty are distinguished from internal verification.

### Domain closure

- D1-D4 role boundaries are complete and non-competing;
- cross-cutting concerns route by semantic effect;
- D3 no longer owns D1/D2 semantics;
- D4 remains adaptive under inherited constraints;
- reduced-domain routing works;
- reopen reaches the earliest affected abstraction.

### Documentation closure

- logical D1-D4 documentation correspondence exists;
- exactly one current normative owner exists per material claim;
- normative versus supporting/evidence prose is distinguishable semantically;
- proposed edits cannot masquerade as accepted current authority;
- release-pinned/publication snapshots are preserved;
- D4 specification and code have explicit non-competing roles;
- `software-documentation` is editorial/publication support, not semantic approval authority.

### Verification closure

- every material abstraction boundary has a verification question and evidence route;
- parent-boundary review is independently falsification-oriented when risk warrants it;
- numerical verification includes convergence/error/conditioning/oracle reasoning;
- external D1 adequacy fits empirical, theoretical, and engineering problem classes;
- composed end-to-end scientific closure exists for material/high-risk claims;
- proxy-proof evidence and evidence invalidation generalize across layers.

### Workflow/autonomy closure

- generic abstraction–realization change-plan/handoff semantics exist;
- D4-only/local routes require only proportionate upstream-impact exclusion;
- human ratification is risk-based and represented truthfully;
- multi-parent dependency invalidation is bounded;
- no unnecessary fixed gate count is introduced.

### Compatibility/implementation closure

- immutable Protocol 5.16 source/profile recovery is demonstrably available;
- 5.16 workplans are not silently interpreted by 6.0 roles;
- Protocol 6 source/dist build/package checks pass;
- all four role skills build/install correctly;
- workflow prompts/profile route domains correctly;
- any required profile-schema major/version evolution is explicit and backward support for 5.16 is tested;
- orchestrator remains subordinate to profile authority;
- repository tests and new adversarial qualification pass;
- existing repository acceptance commands and `git diff --check` pass;
- no mixed 5.16/6.0 canonical release state remains;
- independent final Review finds no genuine blocking defect.

## 21. Genuine redesign / simplification triggers

Reopen this parent authority only on evidence that a central assumption is wrong, including:

- pairwise abstraction–realization cannot represent a material scientific/software development class even with multi-parent/side-constraint semantics;
- D1-D4 boundaries produce unavoidable competing authority;
- logical one-to-one documentation ownership causes systematic duplication rather than clarity;
- current/proposed authority state requires disproportionate bureaucracy;
- human ratification blocks ordinary autonomous work without increasing assurance;
- bounded dependency tracing cannot support correct invalidation without heavy machinery;
- profile-driven orchestration cannot express affected-domain routing without redesigning orchestrator architecture;
- a simpler domain decomposition controls the same failure modes with less authority machinery.

Before adding another role, stage, registry, database, wrapper, ledger, or reconciliation mechanism, determine whether reducing, moving, or clarifying abstraction ownership solves the problem.

## 22. Final design invariant

The target SSDP 6.0 system should be understandable through a small recursive rule set:

```text
An abstraction states the semantic invariants that must survive realization.
A realization must satisfy every applicable upstream abstraction and governed external constraint.
Within that feasible set, optimize domain fitness, then minimum justified complexity, then development economy.
A realization remains delegated except where an owning authority explicitly accepts a property into the abstraction.
Verification reconstructs realization semantics and attempts to falsify conformity; it is opposite-direction reasoning, not a bijective inverse function.
A realization may challenge upstream authority through evidence but may never silently redefine it.
Accepted upstream change invalidates only dependent downstream authority/evidence.
Current normative documents change only through accepted authority mutation, not speculative edits.
```

Applied to scientific software:

```text
external scientific / theoretical / engineering authority and evidence
                 ||  adequacy / validation / proof / UQ
                 \/
D1 scientific & mathematical formulation
                 <-> design / verification
D2 algorithm & numerical methods
                 <-> design / verification
D3 software architecture
                 <-> design / verification
D4 specification & implementation
                 -> executable behavior / evidence
```

The simple chain is a pedagogical projection; the accepted dependency structure may be a layered DAG with multiple applicable upstream authorities and domain-local governed constraints.

SSDP 6.0 shall teach agents to engineer scientific software as **recursive abstraction-preserving realization under constrained optimization, closed by reverse semantic verification, bounded dependency-aware invalidation, and problem-appropriate external scientific/theoretical/engineering adequacy**.

That principle, rather than any incidental role, file layout, algorithm, code mechanism, or orchestrator implementation, is the central invariant of this protocol revision.
