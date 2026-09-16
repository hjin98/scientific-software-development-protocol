# Abstraction, Concretization, Authority, Challenge, and Representation

Protocol 6.4 governs scientific-software work through recursively constrained abstraction/concretization. This is the universal semantic kernel; detailed workflow, evidence, testing, project engineering memory, domain, language, tool, history, and release rules live with their canonical owners and are loaded only when their decision predicates fire.

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** separates four semantic authority domains: **D1** scientific/mathematical formulation, **D2** algorithm/numerical method, **D3** software architecture, and **D4** specification/implementation.

An **abstraction** is an intentionally incomplete normative contract: the material invariants, required outcomes, assumptions, validity conditions, observables, bounds, and governed relations descendants must preserve. A **concretization** is a lower-level choice that satisfies applicable parent abstractions and governed side constraints. An interior D1-D4 artifact may concretize its parent while abstracting its descendants. **Realization** is reserved for concrete evidence execution; see [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) when evidence lifecycle or applicability is material.

**Project Engineering Memory (PEM)** is optional-to-activate, project-local, evidence-backed engineering learning intended to reduce rediscovery and preserve both failure lessons and demonstrated successful patterns. It is **not a fifth authority domain**: when substantial work can materially benefit from project history, route to [Project Engineering Memory](project-engineering-memory.md) and the workflow owner; otherwise keep it cold.

## Feasibility, authority, and delegation

For concretization `K`, parents `A1 ... An`, and directly applicable governed constraints `C`:

```text
semantics(K) |= I(A1) AND ... AND I(An) AND C
```

Fidelity is a feasibility condition, not a weighted preference. Among admissible concretizations prefer:

```text
domain engineering fitness
> minimum justified concretization complexity
> development economy
```

Stop when further search has lower expected engineering value than proceeding with the best justified admissible option; exhaustive global optimization is not required.

Semantic level and authority provenance are independent. Preserve applicable safety, explicit stakeholder/project authority, external contracts/standards, and accepted current domain authority before delegated implementation preference. A security, reliability, performance, compatibility, hardware, regulatory, or public-contract constraint may enter at the domain where it semantically applies.

Steward the stakeholder's governed durable product/outcome rather than the process artifacts used to reach it. Workplans, tests, gates, metrics, reviews, reports, and implementation machinery are constraints, evidence, or concretizations—not objectives. Historical frequency and project memory are likewise decision inputs or coordination state, not self-authorizing rules. Interpret stakeholder and governed requirements non-adversarially according to their protected purpose. This stewardship is bounded by the governed task/contracts/affected surfaces and does not authorize unrelated enhancement, opportunistic redesign, or speculative future-proofing.

Each material normative claim has one current semantic owner, while one concretization may satisfy several parents/side constraints. Current normative ownership must remain acyclic. Materially conflicting applicable authorities are not silently prioritized: expose the conflict and route adjudication.

The four domains are:

- **D1 — Scientific & Mathematical Formulation:** question, observable/estimand, model/equations, assumptions, validity regime, interpretation, external adequacy.
- **D2 — Algorithm & Numerical Method:** discrete/stochastic method, approximation/error/convergence/conditioning/precision semantics, numerical uncertainty.
- **D3 — Software Architecture:** component/state/interface ownership, data/control flow, persistence, concurrency, security, resources, deployment and compatibility architecture.
- **D4 — Specification & Implementation:** accepted concrete software behavior plus executable concretization, tests, packaging and operations.

This is a layered directed acyclic graph (DAG), not a mandatory four-stage waterfall. Start at the earliest/highest domain whose semantics may change and preserve unaffected parents/siblings.

A lower-level mechanism does not acquire authority because it exists, is depended upon, is tested, is documented, survived review, appeared in an earlier plan, repeatedly failed, repeatedly succeeded, or is prominent in project memory. Promote it only through explicit acceptance by the owning abstraction for a material reason. When delegated machinery creates its own problems, prefer removing, narrowing, altering, consolidating, re-deriving, or replacing it before adding durable compensating machinery. Never simplify by weakening governing semantics.

PEM may classify a learned capability as `EVIDENCE_ONLY`, `AUTHORITY_BOUND`, or `PROPOSED_FOR_PROMOTION`; only the independently resolved real current owner can supply normative force. Frequency, memory temperature, maturity, qualification, documentation, or historical survival cannot mint an invariant. A proposed promotion remains non-mandatory until accepted through the owner’s normal process.

## Design, verification, and lifecycle state

Design is generally one-to-many:

```text
A -> {K | K satisfies A and applicable C}
```

Verification therefore is opposite-direction semantic reconstruction, not a bijective inverse:

```text
actual concretization
 -> reconstruct material semantics
 -> compare with every applicable parent/constraint
 -> attempt to falsify conformity
```

At every material boundary distinguish:

1. **concretization fidelity** — the child satisfies all applicable parents/constraints;
2. **abstraction adequacy** — the child abstraction is strong enough that its descendants cannot satisfy it while violating material upstream meaning.

A child can perfectly satisfy a too-weak abstraction and still be wrong; that is an upstream abstraction defect.

Projects may encode lifecycle locally, but must distinguish enough state to prevent speculative or stale material from becoming current authority: proposed; accepted-current; challenged; risk-accepted/provisional; stale-dependent; superseded/historical; release-pinned/publication. Human-ratification state is orthogonal. Non-authoritative project memory has its own evidence/coverage/maturity/accepted-base/candidate-overlay lifecycle and must not be confused with D1-D4 acceptance state.

A durable authority mutation follows the owning domain's acceptance contract: proposal -> independent falsification where required -> required human ratification -> acceptance -> bounded dependent impact -> reconcretization/revalidation. Repository presence alone does not promote a proposal. A PEM record may support/challenge/propose such a change, but cannot perform the acceptance step itself.

When accepted authority changes, review only materially dependent descendants/evidence and preserve unaffected siblings/still-valid evidence. A bounded dependency view is an aid, not proof of independence unless its relevant scope was explicitly reviewed complete. Detailed evidence/dependency rules are owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md). When the changed owner is cited by an authority-bound learned capability/current notice, reconcile that non-authoritative binding as a dependent representation rather than allowing memory to preserve obsolete force.

For high-risk scientific/numerical claims, pairwise checks may be insufficient; trace composed closure when material:

```text
actual D4 behavior
 -> governed numerical observables
 -> D2 error/equivalence envelope
 -> D1 scientific/mathematical meaning
 -> problem-appropriate external adequacy / proof / standards evidence
```

## Challenge and human adjudication

Every material Review/Verification/acceptance boundary includes a bounded **Challenge Pass**. For tiny low-risk work it may be implicit. Ask whether accepted authority is internally coherent, sufficiently unambiguous, jointly concretizable under simultaneous constraints, adequate for its protected outcome, and free of a known material counterexample.

A coherent parent with a wrong child is an ordinary blocker. Raise **SERIOUS CHALLENGE** only when accepted authority itself may be materially false, contradictory, ambiguous, inadequate, mutually incompatible, or impossible to concretize. Surface it before ordinary blockers/Pass language; identify the challenged owner/scope, concrete contradiction/evidence, consequence, assumptions, and what could resolve or falsify it. Preserve the challenged authority as the explicit baseline rather than silently editing it to fit downstream behavior.

PEM is a high-information hypothesis index during Review, not proof. Historical recurrence, successful prior patterns, temperature, counts, or previous review outcomes may guide falsification effort but cannot replace independent reconstruction of current authority, current applicability, evidence quality, and assembled candidate behavior.

Human adjudication governs acceptance where project/domain policy assigns a human gate; it does not create truth by assertion. A visible risk override may authorize bounded continuation where allowed, but does not resolve the challenged claim. Materially dependent descendants remain visibly provisional and cannot emit unqualified closure while the governing challenge remains unresolved.

## Lossless Representation Rule

This rule governs SSDP-authored communication surfaces: skills, references, prompts, workplans, handoffs, specifications, method/architecture documents, agent/inter-agent messages, reviews, evidence summaries, Project Engineering Memory, dependency/evolution records, guides, runbooks, and resumable state.

A representation is admissible only when a competent intended reader/agent can recover and correctly interpret every material semantic element required by the **governed scope**: the surface imposed by user/task authority, selected domain/role, affected dependencies, compatibility obligations, and applicable evidence/closure requirements. The writer may summarize scope but may not narrow it merely to make the representation appear complete.

Losslessness includes governing ownership/lifecycle state, invariants, exceptions, constraints, non-goals, uncertainty, evidence qualification, dependencies/reopen conditions, discoverability of conditionally relevant information, and decision-critical salience. Materiality is decision-local: a rule or memory entry may remain cold for one task without becoming removable from its canonical owner.

Among lossless representations prefer, in order:

```text
semantic correctness and completeness
> semantic precision and unambiguity
> importance-weighted attention
> cognitive digestibility
> context/routing efficiency
> representational compactness
```

Operational consequences:

1. **One detailed owner per generic rule.** Secondary artifacts carry only their local consequence and precise route unless a short restatement lowers total inferential cost.
2. **Generalize rather than accumulate.** Preserve historical capability in an equal-or-stronger current invariant when legitimately promoted; keep project-specific evidence/lessons in PEM and detailed chronology/rationale cold in semantic history unless currently decision-relevant. Promotion requires the real owner’s acceptance, not editorial deduplication.
3. **Use progressive disclosure.** Potential relevance to a broad task class does not justify unconditional loading. PEM/history specifically remains cold for non-triggering local work.
4. **Use bounded typed activation.** A role/specialist entrypoint owns root routing to canonical concern owners; a concern owner may conditionally dispatch to narrower leaves when the decision becomes knowable only inside that concern. Ordinary hyperlinks, semantic dependency and package membership do not imply activation.
5. **Keep routing explicit and derived views non-authoritative.** Each activation hop names a resolvable resource and decision predicate, adds required semantics or narrows the question, avoids cycles/back-edges, and reuses an already-loaded owner while applicable. Graphs/matrices/traces/active summaries/indexes are diagnostics or derived views from canonical owners, not parallel authority.
6. **Keep cold paths discoverable.** Information capable of changing a decision has a visible trigger and supported retrieval route. Importance/temperature may rank attention but cannot make a materially applicable lower-salience item unreachable.
7. **Reuse context only while applicable.** Summaries/caches/handoffs/HAS are derived coordination state. Re-read/remap when protocol/source identity, governing authority/workplan, candidate/regime/scope, accepted-memory basis/overlay, or materially relevant evidence changes, or exact wording becomes necessary. Do not recursively promote stale summaries into authority.
8. **Weight attention without weakening acceptance.** Serious Challenges, safety/governing conflicts, current authority, blockers, high-impact unresolved risk, contradictory/unavailable evidence and required decisions receive prominence; lower-salience mandatory constraints still remain active closure obligations. A memory summary is not a positive-success leaderboard.
9. **Minimize total inferential cost, not character count.** Avoid duplicated restatement, gratuitous routing depth, amendment replay, excessive abbreviation, fragmentation, hidden prerequisites, eager cold-history loading, or long indirection that makes a shorter representation harder to use.
10. **Preserve evidence visibility.** Compression may keep raw detail cold but cannot hide failures, warnings, contradictory/neutral/inconclusive applicable evidence, unavailable required checks, uncertainty, coverage limitations, or provenance needed to interpret a material claim.
11. **Do not deduplicate by adjudicating semantics.** If apparent duplicates materially disagree in scope, threshold, authority, family identity, applicability, or meaning, stop editorial compaction and route the conflict to its owner/explicit split-merge reconciliation.
12. **Keep derivatives subordinate.** Compact prompts, handoffs, summaries, indexes, records and generated representations do not replace canonical authority or canonical project memory.

Historical identifiers may retain old lexemes inside frozen/version-pinned artifacts. Current Protocol 6.4 prose uses **concretization** for D1-D4 descent and **realization** for evidence execution.

## Protocol 6.4 semantic-definition and traceability strengthening

A **semantic object/unit** is a materially governed term, symbol, quantity, operator, relation, state, proposition, algorithmic object, invariant, parameterized family, instantiated object, or contract whose meaning or conditions can alter governed interpretation, admissible concretization, evidence applicability, or acceptance if changed. A **canonical semantic statement** is the one current owner statement, or explicitly coordinated owner-local statement set, that establishes that object's project-visible meaning. A **substantive semantic use** is an occurrence that participates in a declaration/definition, premise, inference, constraint, theorem/result, algorithm, contract, acceptance decision, or governed interpretation. A harmless forward name supports no inference and is not substantive use.

For a version-coherent composed authority family `D`, `source_available_D(x)` holds only when the exact meaning of `x` is reconstructible from a bounded foundational envelope, an exact external import, an explicit project declaration/definition, or a valid scope-local binder whose referenced domain/type is already available; the current semantic owner is recoverable; and no simultaneously applicable owner statements materially conflict without an accepted compatibility/equivalence/adjudication mapping. Routing order, file order, aliasing, or newest-version preference cannot turn conflicting meanings into one canonical object.

For actual runtime context `C`, `context_available_C(x)` additionally requires the exact canonical meaning needed for the current inference to have been supplied/loaded in that context. Therefore:

```text
substantive_use_D(x) -> source_available_D(x)
infer_C(x) -> context_available_C(x) -> source_available_D(x)
```

The source-availability basis is `FOUNDATIONAL_ASSUMED`, `EXTERNAL_IMPORTED`, or `PROJECT_DECLARED`, plus scope-local binders/declarations whose referenced domain/type is already available. This basis is orthogonal to novelty, semantic role, historical provenance, evidence strength, and normative force.

Semantic/epistemic roles are non-exclusive and extensible. Representative roles include `PRIMITIVE`, `DEFINITION`, `AXIOM`, `PREMISE`, `ASSUMPTION`, `DERIVED_RESULT`, `CONJECTURE`/`HYPOTHESIS`, `OBSERVATION`/`EMPIRICAL_RELATION`, `APPROXIMATION`/`HEURISTIC`, `NORMATIVE_CONTRACT`/`EXTERNAL_CONSTRAINT`, and `EXAMPLE`/`COUNTEREXAMPLE`. This is not a closed ontology and a validator must not reject a valid status merely because it is absent from the illustrative list.

Axiomatic dependency order is semantic, not merely typographic. Specialized substantive use requires prior source availability. A non-foundational project root may be an explicit primitive when its signature/constraints bound meaning. A local binder introduces its variable only within scope and may reference only already available domains/types. A definition stipulates meaning relative to available objects; it does not by notation alone establish existence, uniqueness, empirical truth, convergence, optimality, safety, adequacy, or authority. Those are separate claims requiring the appropriate premise, proof, evidence, or owner.

A formal-looking statement is admissible only when well-defined enough for its governed use. State when material: bound/free-variable scope and quantifier order; domain/codomain/type/shape/unit; total versus partial behavior; branch/sign/order/normalization/frame conventions; deterministic/stochastic/set-valued semantics; existence/uniqueness; piecewise precedence; boundary/initial conditions; singular/undefined cases; relation kind (`=`, definitional equality, equivalence, approximation, asymptotic relation, assignment, membership, implication, distributional relation); logical direction; and state/time/concurrency semantics needed to distinguish outcomes. Equations and mappings over physical/typed quantities must be dimensionally/type consistent.

For a material parameterized family distinguish family, instance, and default explicitly. Schematically `F: Theta -> O`, `theta -> F_theta`: define the parameter domain and admissibility, which parameters are free/fixed/derived/estimated/externally constrained/defaulted, the binding source for a concrete `F_theta0`, the owning layer of a governed default, and parameter-dependent validity/error/uncertainty/equivalence. A default supplied by software is not intrinsic mathematical meaning unless its owner makes it so. Evidence/quantitative claims bind to the material parameter/regime identity actually exercised.

For every imported or derived result `r` with material hypotheses/validity conditions `H(r)`, substantive use requires each condition to be discharged or explicitly propagated. A claim warrant is not closed by citation count, test count, reviewer count, or a generated trace; each normative claim remains owner-bound and each factual/empirical/mathematical claim must retain the appropriate source, proof, observation, assumption, or uncertainty chain without circular self-support.

A material direct prerequisite relation may be represented as `x USES_DEFINITION -> y` when the canonical meaning of subject `x` directly depends on prerequisite `y`. The stored relation direction is therefore `subject -> prerequisite`. If prerequisite `y` changes, dependent subjects are discovered by reverse traversal over stored `USES_DEFINITION` edges; reverse impact traversal is a query, not a second relation or a change in canonical direction. Dependency traces/graphs are derived review and impact aids, not authority, and may claim completeness/absence only for an explicitly bounded reviewed scope. Mutually recursive definitions use an explicit simultaneous definition/composite node or strongly connected component (SCC) condensation; accidental circular warrant remains invalid.

The formal-first rule is therefore not “more equations.” It is: use the strongest practical exact representation that materially reduces interpretive freedom, then explain it in natural language. Do not create decorative mathematics, a fifth semantic authority plane, or a universal ontology/database/checker merely for protocol symmetry.

## Universal invariant

```text
accepted authority defines what must be true;
admissible concretization preserves every applicable authority/constraint;
within that feasible set optimize domain fitness, justified simplicity, then development economy;
delegated mechanisms remain replaceable unless explicitly accepted into authority;
verification reconstructs semantics and attempts falsification;
evidence and project memory may support, challenge, or guide work but never silently redefine authority;
accepted change invalidates only materially dependent descendants/evidence/derived learning bindings;
Serious Challenge stops counterfeit closure when accepted authority itself may be defective;
representation must preserve complete governed meaning before optimizing attention/context cost;
specialized substantive use requires a coherent definition/import/declaration path and exact owner;
formal statements must be well-defined, parameter bindings explicit when material, and claims separately warranted;
derived semantic traces remain subordinate evidence for review/impact rather than parallel authority;
project learning stays evidence-backed, applicability-bounded, conditionally loaded, and non-authoritative.
```
