---
kind: abstraction-concretization-change-plan-consolidated
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: active
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: pass-after-sixth-review
independent_review_state: repaired-awaiting-fresh-review
implementation_handoff: repair-complete-awaiting-fresh-review
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
reviewed_input_head: 4974058020cdda1325ef899c04b3cd13d5ae44c2
independent_review_target: 0377e798fbbb1054badd1193950d9c10f723be75
independent_review_baseline: 0928accd337a13f864b292ed81c36372828cfb4c
stage_f: blocked
branch_point: 0928accd337a13f864b292ed81c36372828cfb4c
accepted_parent_protocol: 6.3.0
accepted_parent_recovery: 9f353097fab36e325a325f1c2f9d9cec32e86177
accepted_parent_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
---

# SSDP 6.4 — Axiomatic Formal Definition and Semantic Traceability — Consolidated Workplan

## Current disposition

**STAGE-E REPAIR COMPLETE; FRESH INDEPENDENT RE-REVIEW REQUIRED.** The NO-PASS on immutable assembled target `0377e798fbbb1054badd1193950d9c10f723be75` remains historical Review evidence, while its three owning-layer repairs are now integrated under Section 27. The `USES_DEFINITION` direction is explicitly adjudicated as subject -> prerequisite with prerequisite-change impact using reverse traversal; the QF64-H oracle discriminates reversed edges and wrong impact traversal; and the canonical Markdown fence defect is repaired with a real structural presentation oracle. Protocol 6.3 remains accepted-current. Protocol 6.4 recovery remains unavailable and Stage F remains blocked until a fresh independent Review passes a new immutable assembled target. The sixth design-review disposition below records the pre-implementation design acceptance that authorized the original implementation.

**SIXTH DESIGN REVIEW: PASS AFTER GAP CLOSURE.** This file is the single current implementation/review handoff for Protocol 6.4. Earlier design-review workplans and the fifth-review consolidated snapshot are historical evidence only; implementation and independent Review SHALL reconstruct the current contract from this file plus accepted Protocol 6.3 owners, not by replaying amendment chronology.

Protocol 6.3 remains accepted-current until Protocol 6.4 completes implementation, qualification, independent assembled-candidate Review, self-reference-safe public-bootstrap publication, immutable recovery mapping, mapping-bearing generated reconciliation, Protocol-7 inheritance-only reconciliation, and lifecycle closeout.

The protected outcome is:

> Every materially governed technical concept can be reconstructed by a competent intended reader or downstream agent with minimum interpretive freedom; specialized prerequisites, assumptions, validity, support/provenance, normative force, parameterization, direct semantic dependencies, and claim warrant are recoverable; formal expressions are well-defined; conflicting current meanings cannot be hidden by routing; and changes can be propagated through bounded typed impact closure without hidden context, mixed-version meaning, external-content instruction injection, or lower-domain semantic leakage.

## Background and formal terminology

The **Scientific Software Development Protocol (SSDP)** separates four semantic authority domains: **D1 scientific and mathematical formulation**, **D2 algorithm and numerical method**, **D3 software architecture**, and **D4 specification and implementation**. **Project Engineering Memory (PEM)** is project-local evidence-backed decision support and is not a fifth authority domain. A **Historical Applicability Set (HAS)** is the session-local workflow record of materially relevant PEM items and their applicability dispositions.

For governed scope `S`, a **semantic object/unit** is a materially governed term, symbol, quantity, operator, relation, state, proposition, algorithmic object, invariant, parameterized family, instantiated object, or contract whose meaning or conditions can alter governed interpretation, admissible concretization, evidence applicability, or acceptance if changed.

A **canonical semantic statement** of object `x` is the one current semantic-owner statement or coordinated owner-local statement set that establishes the project-visible meaning of `x` for the governed scope. It may comprise a primitive declaration, definition, proposition/theorem statement, assumption/premise, algorithmic contract, or D3/D4 contract together with owner-local conditions needed to identify its meaning. One logical owner may use several coordinated clauses; this does not authorize duplicate independently editable authorities.

A **substantive semantic use** of `x` is an occurrence whose meaning participates in a declaration/definition, premise, inference, constraint, theorem/result statement, algorithm, contract, acceptance decision, or interpretation. A harmless forward name that supports no inference is not a substantive use.

A **material direct prerequisite** `x` of semantic unit `y` is one whose meaning is directly invoked by the canonical semantic statement of `y`, and for which a materially different admissible meaning of `x` can change the denotation, admissible domain, validity, governed contract, parameterization, or accepted interpretation of `y`.

A **directed acyclic graph (DAG)** is a directed graph with no directed cycle. A **strongly connected component (SCC)** is a maximal set of nodes mutually reachable by directed paths; a legitimate mutually recursive definition may be represented as one composite node or by SCC condensation.

## 1. Parent authority and compatibility

Protocol 6.4 is a backward-compatible minor strengthening over accepted Protocol 6.3. It preserves every accepted 5.16/6.0/6.1/6.2/6.3 capability and doctrine unless this workplan explicitly strengthens representation.

The following remain invariant:

- D1-D4 remain the only semantic authority domains; no D5, documentation authority plane, ontology authority, traceability authority, or warrant authority is created.
- Accepted current authority defines what must be true. Literature, tests, evidence, documentation, PEM, generated traces, frequency, and historical survival do not silently mint authority.
- Applicable external contracts, standards, regulations, stakeholder constraints, and other external requirements retain only the normative force supplied by their real governing authority.
- Concretization fidelity and abstraction adequacy remain distinct.
- One detailed owner per generic rule, progressive disclosure, explicit typed routing, cold-path discoverability, and derived-view subordination remain binding.
- Evidence specification -> realization -> observation -> assessment remains binding.
- Serious Challenge, human adjudication where assigned, bounded impact closure, Review/Verification/Stabilization, and workflow semantics remain binding.
- PEM remains schema-1, project-local, conditionally activated, evidence-backed, and non-authoritative.
- Frozen 5.16/6.0/6.1/6.2/6.3 source/profile/recovery/bootstrap/qualification artifacts remain immutable.
- Protocol 6.3 public bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11` and recovery `9f353097fab36e325a325f1c2f9d9cec32e86177` remain distinct and valid for version-bound 6.3 work.
- Protocol 7 remains proposed/pre-cutover. Protocol 6.4 implementation does not mutate its current D3/control-plane semantics.

## 2. Source-level and runtime semantic availability

For a version-coherent composed authority family `D`, define source-level semantic availability:

\[
\operatorname{source\_available}_D(x)
\]

iff all of the following hold:

1. the canonical semantic meaning of `x` is reconstructible in `D` from the bounded foundational envelope, exact external import, project declaration/definition, or a valid local binder whose referenced domain/type is already source-available;
2. the current semantic owner is recoverable;
3. simultaneously applicable owner statements do not materially disagree about `x`, unless an explicit accepted compatibility/equivalence/adjudication mapping resolves the apparent multiplicity; and
4. no unresolved owner conflict is being hidden by file order, newest-version preference, routing priority, or aliasing.

Thus two incompatible applicable meanings are not made unambiguous merely because one route is easier to load. Material owner conflict is `REVIEW_REQUIRED` and may trigger Serious Challenge under accepted 6.3 rules.

For actual runtime context `C`, define:

\[
\operatorname{context\_available}_C(x)
\]

iff the exact canonical meaning required for the current inference is actually supplied/loaded in `C` under the governing version/snapshot.

The authoring invariant is:

\[
\operatorname{use}_D(x)\Rightarrow\operatorname{source\_available}_D(x),
\]

and the runtime invariant is:

\[
\operatorname{infer}_C(x)
\Rightarrow
\operatorname{context\_available}_C(x)
\Rightarrow
\operatorname{source\_available}_D(x).
\]

A route can make an object source-available without loading it into a particular runtime context. Hidden chat/runtime prose cannot make an object source-available when no coherent canonical owner/source exists.

The source-availability basis is:

\[
\operatorname{availability\_basis}(x)
\in
\{\mathrm{FOUNDATIONAL\_ASSUMED},\mathrm{EXTERNAL\_IMPORTED},\mathrm{PROJECT\_DECLARED}\},
\]

or a scope-local binder/declaration whose referenced domain/type is already available at the corresponding layer.

This classification is orthogonal to historical provenance, evidence strength, semantic role, novelty, and normative force.

## 3. Semantic roles and axiomatic order

Semantic/epistemic roles are non-exclusive. Representative roles include:

```text
PRIMITIVE
DEFINITION
AXIOM
PREMISE
ASSUMPTION
DERIVED_RESULT
CONJECTURE / HYPOTHESIS
OBSERVATION / EMPIRICAL_RELATION
APPROXIMATION / HEURISTIC
NORMATIVE_CONTRACT / EXTERNAL_CONSTRAINT
EXAMPLE / COUNTEREXAMPLE
```

This is not a closed ontology or schema. Add a real status distinction when needed to prevent semantic ambiguity; do not invent taxonomy merely for symmetry. A validator must not reject a valid current semantic status only because it is absent from an illustrative list.

A compliant authority family may use flexible visual organization, but its semantic dependency order is equivalent to:

```text
FOUNDATIONAL_ASSUMED reader knowledge
+ exact EXTERNAL_IMPORTED specialized prerequisites
+ PROJECT_DECLARED primitives/signatures
 -> explicit axioms/premises/assumptions/validity conditions
 -> definitions from available objects
 -> derived propositions/theorems/results
 -> algorithms/contracts/consequences using those semantics
 -> interpretation/evidence/rationale/limitations/explanatory prose
```

A later definition cannot retroactively supply meaning required by an earlier normative inference. Brief forward naming is allowed only when no substantive inference depends on the undeclared meaning and the canonical route is explicit.

## 4. Foundational knowledge envelope

Each human-facing authority document/family identifies an intended competent reader and a bounded foundational knowledge envelope proportionately to risk.

Ordinary logic, numbers, standard calculus, linear algebra, probability, common mathematical notation, and similarly broad foundations may be assumed when genuinely standard for that audience. Project-specific terminology, specialized named theories/methods/theorems with materially different variants, and field-specific conventions that can change conclusions are not foundational merely because the reader is expert.

Use the conservative rule:

\[
\operatorname{uncertain\_foundational}(x)\Rightarrow\operatorname{define\_or\_import}(x).
\]

Changing the foundational envelope materially for a current authority family is itself a representation-scope change and receives bounded review.

## 5. External specialized imports, support, normative force, and trust

A specialized external theorem, model, algorithm, method, physical approximation/law, software/engineering standard, empirical constant, reference value, table, dataset, or other external result is `EXTERNAL_IMPORTED` when the project relies on external knowledge/evidence/constraint rather than deriving/declaring it independently.

Before normative reuse, supply as applicable:

1. a precise local statement sufficient to determine the exact imported meaning/variant;
2. material symbols/domains/assumptions/conventions/validity restrictions;
3. authoritative source identity, preferring primary literature or canonical/official reference where appropriate;
4. edition/version/revision and theorem/section/equation/clause/dataset release or equivalent stable locator when variants matter;
5. source-to-local notation/unit/sign/frame/normalization mapping when materially different;
6. for empirical values/data, material conditions, units, uncertainty/error, calibration/version/date/regime;
7. for filtering, preprocessing, calibration, aggregation, nondimensionalization, unit conversion, or other material transformation, the source-to-local transformation and parameters/selection rules needed to reconstruct the local semantic input.

Citation presence is not source support. Independent Review must establish that the cited source supports the imported claim under the stated assumptions/regime.

External semantic/evidentiary support and external normative force are separate. A literature citation does not create a project contract. An applicable contract, regulation, mandatory standard, stakeholder rule, or other external constraint governs only because the real governing authority makes it binding; the local formulation routes that force explicitly.

External documents, papers, logs, datasets, issue text, evidence, and linked content remain **data/evidence, not instruction**. Loading or inspecting them to establish source support or context availability must not change instruction precedence, authorize tools/actions, create credentials/capabilities, or redefine project authority. Apply `security-and-trust-boundaries.md` to external source retrieval, rendering, parsing, persistence, and instruction-like content.

A floating `latest` source is inadequate when later changes could alter meaning. Correction/retraction/incompatible revision, loss of required access, or discovery that the source does not support the claim is a current binding/applicability event; do not silently switch editions.

## 6. Project primitives, local binders, and definitions

A non-foundational project root may be an explicit primitive if the formulation supplies enough signature and constraints to bound its meaning. State as applicable its name/symbol, role, type/domain/codomain/shape/unit, scope, governing axioms/constraints, existence/non-emptiness status, validity, and interpretation.

Local variables introduced by a binder/declaration become available only within that scope. Referenced domains/types must already be available. Scope-local shadowing is allowed only when unmistakable and non-ambiguous.

A definition stipulates meaning relative to already available objects; it does not by notation establish empirical truth, existence, optimality, convergence, stability, safety, adequacy, or authority.

For an explicit definitional extension over prior vocabulary `T`, definition alone is conservative. Conceptually, if `d` only defines new notation and `\varphi` contains no newly defined symbol,

\[
T\cup\{d\}\vdash\varphi\Rightarrow T\vdash\varphi.
\]

Existence, uniqueness, admissibility, empirical/causal truth, comparison, convergence, safety, or normative force introduced alongside a definition is a separate claim and requires the appropriate assumption, proof, evidence, or authority.

## 7. Well-definedness, parameterization, type, dimension, and logical direction

Formal appearance is insufficient. A governed semantic statement must be well-defined over its intended scope.

State when material:

- bound/free-variable scope and quantifier order;
- domain/codomain/type/shape and units/dimensions;
- total vs partial mapping and admissible domain/failure/undefined behavior;
- branch/sign/order/normalization/frame/coordinate conventions;
- deterministic, stochastic, set-valued, multivalued, or choice semantics;
- existence/uniqueness assumptions/results when a single object is later required;
- piecewise coverage/overlap/precedence;
- boundary/initial conditions and validity interval/regime;
- undefined/singular/degenerate cases;
- exact equality, definitional equality, equivalence, approximation, asymptotic relation, assignment/update, membership, implication, distributional relation, or other materially distinct relation;
- necessary, sufficient, or necessary-and-sufficient/biconditional direction when material;
- for stateful/time-dependent semantics, material state, transition/order/time basis, initialization, termination, atomicity/concurrency, or clock semantics needed to distinguish outcomes.

Where physical/typed quantities are involved, equations and mappings must be dimensionally/type consistent. Nontrivial unit conversion, affine/logarithmic units, nondimensionalization, or coordinate transforms that change interpretation are explicit.

### Parameterized families and instantiated objects

For a material parameterized semantic family, distinguish the family from a concrete instance. Schematically:

\[
F:\Theta\to\mathcal O,\qquad \theta\mapsto F_\theta.
\]

Define as material:

- parameter domain `Theta`, type/shape/units and admissibility constraints;
- which parameters are free, fixed, derived, estimated, externally constrained, or defaults;
- the binding source for a concrete instance `F_{theta_0}`;
- whether a default is part of D1/D2 method semantics, a D3 deployment choice, a D4 public/configuration contract, or merely delegated implementation detail;
- parameter-dependent validity/error/uncertainty/equivalence conditions.

A family definition and an instantiated object are not interchangeable identities. A default value is not intrinsic mathematical meaning merely because software supplies it. Changing a governed default/parameter binding may require bounded descendant/evidence impact even when the family equation is unchanged.

Evidence realizations and quantitative claims bind to the material parameter/regime identity actually exercised. Do not reuse evidence across materially different parameter bindings solely because the family name is unchanged.

If the strongest practical formal/structured representation still admits materially different interpretations, preserve `REVIEW_REQUIRED`/Challenge or refine the owning abstraction; inconvenience is not closure.

## 8. Stochastic semantic closure

When randomness materially affects scientific/numerical meaning, define enough structure to distinguish material alternatives, including as applicable random object/state/sample space, law/sampling mechanism, independence/dependence/exchangeability/conditioning assumptions, conditioning information, estimator/statistic semantics, finite-sample vs asymptotic status, convergence mode, and seed/reproducibility policy when governed.

Do not restate full measure theory when common foundations suffice. Do distinguish cases such as **independent and identically distributed (IID)** versus correlated sampling when they change the result.

## 9. Assumption, validity, approximation, and applicability closure

For every material use of imported or derived result `r` with hypotheses/validity conditions `H(r)`:

\[
\operatorname{use}(r)\Rightarrow\operatorname{discharged\_or\_propagated}(H(r)).
\]

Each material condition is established, explicitly adopted as an assumption by the owner, or propagated as a condition on the dependent result/concretization. A citation or definition-use edge does not discharge hypotheses. Known-false conditions invalidate the use; materially uncertain satisfaction is `REVIEW_REQUIRED`/challenged as appropriate.

Validity, uncertainty, approximation, and assumption relations stay typed. Descendants may narrow a validity regime but cannot silently broaden it or promote an approximation/empirical relationship into an exact unconditional identity.

## 10. Derivation, proof, and typed warrant closure

Material `DERIVED_RESULT` claims expose direct proof/premise dependencies proportionately to risk. A derivation cannot receive warrant from a live dependency chain that materially depends on its own conclusion. Legitimate mutual induction/simultaneous proof is represented as one composite proof unit with external premises and internal well-founded structure visible enough for Review.

More generally:

\[
\operatorname{established}(c)
\Rightarrow
\operatorname{warrant\_closure}(c)
\text{ terminates in admissible roots and contains no self-supporting warrant cycle.}
\]

Admissible roots include foundational knowledge; explicit accepted axioms/assumptions whose conditional status is propagated; exact source-supported imported premises; admissible empirical evidence for empirical claims; and current project/external authority for normative contracts.

This is a bounded Review obligation over existing typed relations, not a new warrant database or untyped edge class.

## 11. Semantic-definition-use dependency and ownership

For composed authority family `D`, define the direct semantic-definition-use graph:

\[
G_D^{\mathrm{def}}=(V_D,E_D^{\mathrm{def}}),
\]

with

For semantic unit `s` (the subject) and material direct prerequisite `p`,

\[
(s,p)\in E_D^{\mathrm{def}}
\iff
\text{the canonical semantic statement of }s\text{ directly requires the canonical meaning of }p.
\]

Thus the stored semantic-relation direction is `subject -> prerequisite`. If a prerequisite changes, dependent subjects are discovered by reverse traversal of `E_D^{\mathrm{def}}`; reverse impact traversal is a query over the stored relation, not a second semantic relation or a reversal of its canonical direction.

The retained typed relation is:

```text
subject USES_DEFINITION -> exact semantic object whose canonical declaration/definition/semantic statement is directly required to interpret the subject
```

The subject may be a definition, theorem/result, assumption, algorithm, D3 rule, or D4 contract. A primitive declaration may be an endpoint/root.

A direct edge is material when varying the prerequisite's admissible meaning can change the subject's denotation, parameterization, admissible domain, validity, governed contract, or accepted interpretation. Incidental lexical mention is not an edge.

The external reviewable graph is acyclic. Legitimate recursive/simultaneous systems are represented as composite nodes/SCC condensation.

Keep other relations typed and separate, including `DERIVED_FROM`, `ASSUMES`, `CONSTRAINED_BY`, `CONCRETIZES`, `EVIDENCES`, `EXECUTION_DEPENDS_ON`, `SUPERSEDES`, and `REPLACES`.

Canonical ownership:

- `abstraction-and-concretization.md`: universal semantic availability/definition closure requirement;
- `evidence-evolution-and-dependencies.md`: `USES_DEFINITION` direction, endpoint durability, declared-scope completeness/absence semantics, and impact behavior;
- `scientific-technical-writing.md`: human-facing definition/import/alias/scope/dependency presentation;
- D1-D4 owners: actual semantic statements/contracts;
- `source/SEMANTIC_DEPENDENCIES.md`: subordinate derived current view only.

For declared canonical scope, direct `USES_DEFINITION` edges are materially complete. Missing edges in a partial diagnostic view cannot prove independence.

Material cross-document endpoints use the cheapest sufficient durable identity: semantic owner + version/snapshot identity + stable logical locator such as definition/claim label, section/anchor, or exact path location. No global ID registry is required.

## 12. Cross-domain direction and canonical-owner conflict

Traceability preserves D1 -> D2 -> D3 -> D4 abstraction direction.

Where materially applicable:

```text
D2 object --CONCRETIZES / USES_DEFINITION--> D1 object
D3 rule   --CONCRETIZES / CONSTRAINED_BY / USES_DEFINITION--> D2/D1 object
D4 contract --CONCRETIZES / CONSTRAINED_BY / USES_DEFINITION--> D3 and directly applicable upstream object
```

Lower-domain artifacts may reference upstream definitions. Upstream definitions do not acquire incidental lower-domain implementation meaning.

One semantic object has one current semantic owner for a governed scope. Several physical clauses/files may constitute that owner family, and aliases may route to it. If two simultaneously applicable current owner statements materially disagree, do not choose one by lexical order, timestamp, branch position, tool preference, or popularity. Preserve the conflict and route adjudication/Serious Challenge to the earliest affected owner.

## 13. Version-coherent composition, identity, equivalence, and lineage

A definition may be supplied by another file/owner rather than repeated, but the composed authority closure must be version-coherent. Across repositories, releases, frozen versions, or independently moving owner families, bind enough immutable/version identity to prevent accidental mixed semantics.

Do not compose D1 from one semantic revision with incompatible D2/D3/D4 definitions unless explicit accepted compatibility/adoption mapping establishes that composition. Unknown mixed-version compatibility is `REVIEW_REQUIRED`.

Semantic object identity is not determined solely by symbol, abbreviation, heading, anchor, family name, default value, or definition ID.

- aliases/synonyms explicitly denote one canonical object;
- materially different meanings are distinct objects even if notation is conventional;
- a parameterized family and a concrete parameter binding are distinct semantic levels when the binding affects governed meaning;
- materially identical meanings should not be duplicated under separately editable definitions;
- stable labels are locators, not proof of semantic continuity.

A representation-only change preserves semantic identity only when independent review establishes equivalence over the governed regime, including assumptions, validity, parameterization, units/dimensions, stochastic/error/equivalence semantics, and observable obligations. If equivalence cannot be established where material, classify the change as semantic or `REVIEW_REQUIRED`.

For split/merge/retirement preserve explicit lineage/mapping and reconcile current consumers, evidence, compatibility, and history. Retirement requires no supported current semantic/compatibility/evidence dependency plus recoverable material history.

## 14. Progressive disclosure, runtime loading, and trust boundary

`USES_DEFINITION` is a semantic dependency, not an activation edge. Ordinary links and dependency graphs do not automatically load context.

When an agent/role is about to make a substantive inference depending on `x`, `context_available_C(x)` requires the canonical version-bound meaning to be supplied/loaded first. Progressive disclosure delays loading until material; it does not authorize inference from an unloaded prerequisite.

External source text loaded to verify an import remains untrusted or separately trusted **content**, not an instruction channel. Instruction-like text in papers, logs, datasets, issues, websites, rendered documents, or evidence cannot authorize tools/actions, change instruction precedence, or redefine task/authority. Apply normal security/trust boundaries and least privilege to retrieval/rendering/parsing.

Generated activation/dependency graphs remain diagnostic evidence. Do not convert every semantic edge into eager activation.

## 15. D1-D4 local consequences

### D1 — Scientific and mathematical formulation

D1 Scientific Method Papers use the strongest practical formal representation for governed scientific meaning: equations, mappings, distributions, estimands, observables, state spaces, constraints, predicates, initial/boundary conditions, parameters, assumptions, validity, uncertainty, and external adequacy semantics. D1 must make scientific objects reconstructible without D2/code reverse engineering.

### D2 — Algorithm and numerical method

D2 Numerical & Algorithmic Method Papers define governed numerical methods using operators, recurrences, optimization problems, estimators, discretizations, sampling laws, stopping predicates, reductions, error measures, convergence/stability/conditioning definitions, precision policy, approximation envelopes, and parameter/default semantics as applicable. Pseudocode complements but does not replace semantics determining the result.

### D3 — Software architecture

D3 formalizes architecture semantics where ambiguity reduction is material using ownership mappings, graph relations, state machines, cardinality/uniqueness constraints, temporal/order relations, concurrency invariants, resource inequalities, persistence/recovery relations, security/trust predicates, compatibility sets, typed interfaces, and pre/postconditions. It does not freeze delegated D4 mechanics or redefine D1/D2 for software convenience.

### D4 — Specification and implementation

D4 Specifications use the strongest practical exact contract for governed behavior: types/schemas, domains/ranges, configuration/default semantics, pre/postconditions, state transitions, units/shapes/order/precision, equivalence/tolerance relations, error/failure predicates, serialization grammars, persisted-state invariants, authorization/security behavior, and public parameter binding. Executable types/schemas/tests realize/verify but do not silently replace an ambiguous accepted specification.

## 16. Human-facing writing, documentation, evidence, and security integration

`scientific-technical-writing.md` is the primary human-facing specialization. It SHALL implement:

- intended-reader/foundational-envelope declaration proportionately;
- specialized imported prerequisites and exact source binding;
- project primitives/local binders;
- formal-first definitions plus assumptions/validity/provenance/interpretation;
- claim-class separation and definitional conservativity;
- parameterized-family/instance/default semantics;
- well-definedness, notation/relation/type/dimension/quantifier/stochastic/temporal rules;
- first-use abbreviation expansion and explicit aliases;
- source-level vs runtime-context availability;
- direct semantic-definition-use dependency exposure/routing;
- external support vs normative-force separation;
- source-to-local transformation lineage;
- natural-language interpretation sufficient for the intended reader.

Current 6.4 canonical human-facing references and this workplan apply these rules proportionately. Frozen historical artifacts are not rewritten to current style.

Owner integration:

- `documentation-maintenance.md`: current-vs-history, source-chain, current owner composition, and documentation impact closure;
- `documentation-and-evidence.md`: authority/evidence communication boundaries;
- `evidence-evolution-and-dependencies.md`: typed semantic/evidence dependency semantics and impact;
- `workflow-and-workplans.md`: snapshot-complete handoff, bounded adoption, runtime loading, HAS, and closeout;
- `testing-and-validation.md`: honest mechanization, counterfactual qualification, and real-owner evidence;
- `protocol-versioning-and-compatibility.md`: version/profile/bootstrap/recovery behavior;
- `security-and-trust-boundaries.md`: external content remains data, source retrieval/rendering/parsing trust boundaries, and instruction-channel separation;
- `source/SEMANTIC_DEPENDENCIES.md`: subordinate derived current view.

## 17. Protocol 6.4 adoption

Version-bound 6.3 work remains governed by 6.3. A newer installed/latest skill never silently reinterprets it.

When a project/workplan explicitly adopts 6.4 over bounded scope:

1. identify materially relied-upon D1-D4 semantic objects/invariants and material parameter bindings;
2. confirm source availability, unique/reconciled ownership, provenance/support, validity, parameterization, and warrant closure;
3. preserve unrelated authority and historical artifacts;
4. if representation repair exposes materially different meanings or owner conflict, stop editorial repair and reopen/challenge the owning domain;
5. reconcile only materially dependent concretizations/evidence/docs/history/PEM bindings;
6. ensure composed versions are mutually compatible;
7. ensure agents making dependent inferences actually load required canonical owners;
8. apply trust rules to external content used for source verification.

Adoption is not a global rewrite mandate and does not license indefinite reliance on ambiguous predecessor prose.

## 18. Repository implementation scope

Implementation SHALL reconcile at least:

```text
source/PROTOCOL_VERSION
source/shared/references/abstraction-and-concretization.md
source/shared/references/scientific-technical-writing.md
source/shared/references/scientific-formulation.md
source/shared/references/numerical-algorithm-design.md
source/shared/references/architecture-and-design.md
source/shared/references/specification-and-implementation.md
source/shared/references/documentation-maintenance.md
source/shared/references/documentation-and-evidence.md
source/shared/references/workflow-and-workplans.md
source/shared/references/evidence-evolution-and-dependencies.md
source/shared/references/testing-and-validation.md
source/shared/references/protocol-versioning-and-compatibility.md
source/shared/references/security-and-trust-boundaries.md
source/SEMANTIC_DEPENDENCIES.md
source/README.md
README.md
AGENTS.md
relevant role/specialist SKILL.md routing/local consequences
profile/protocol manifest/version metadata
orchestrator protocol snapshot/profile resources generated from canonical source
history/SEMANTIC_EVOLUTION.md
workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md
```

Edit canonical source first and regenerate descendants. Do not hand-edit generated `dist/`, package, prompt/profile, or snapshot outputs as independent truth.

Protocol 7 active parent/Revisions 1-4 remain semantically untouched during 6.4 implementation. Only after 6.4 acceptance add a narrow inheritance-only Protocol-7 revision.

## 19. Mechanization and presentation integrity

Prefer documentation convention plus bounded structural/static sensors over a persistent subsystem. Automation may honestly verify mechanically decidable properties such as required structured fields, cross-reference/locator resolution, duplicate/unresolved IDs, generated trace parity, frozen prior-version byte stability, profile/schema/version consistency, explicit machine-encoded type/unit metadata, and supported Markdown/link/anchor/LaTeX/render integrity.

Automation SHALL NOT claim to prove arbitrary mathematics, scientific truth, theorem applicability, semantic equivalence, hidden dimensional validity, literature support, audience expertise, complete dependency discovery, owner equivalence, role-taxonomy completeness, or warrant sufficiency.

A supported rendered/publication surface that breaks a material formula/link/anchor or changes apparent notation fails presentation integrity. Renderer success does not prove semantics.

No theorem prover, ontology service, citation database, semantic hash registry, shadow definition store, warrant database, or universal dependency graph is required by 6.4.

## 20. Protocol/profile/PEM integration

- Set canonical candidate protocol version to `6.4.0` only during candidate integration.
- Generate distinct `ssdp-protocol-6.4` profile/resources without mutating frozen 6.3 bytes.
- Retain orchestration profile schema v2 unless the machine-readable profile contract genuinely changes.
- PEM schema 1 remains independent and unchanged unless separately justified.
- Do not churn PEM merely to mirror protocol text.
- Keep 6.4 bootstrap and recovery self-reference-safe, immutable once published, and intentionally distinct.

PEM remains activated as decision support because this is mature protocol rework. The design HAS remains:

```yaml
pem_basis:
  accepted_project_state: 0928accd337a13f864b292ed81c36372828cfb4c
  accepted_pem: 0928accd337a13f864b292ed81c36372828cfb4c:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: NONE
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: Do not publish a 6.4 public bootstrap until the complete repaired source/route/package semantics exist and qualify at that exact immutable snapshot.
  - id: PC-001
    disposition: APPLICABLE
    reason: Add 6.4 doctrine/profile/resources while frozen predecessor resources remain immutable and independently testable.
  - id: SP-001
    disposition: APPLICABLE
    reason: Repair canonical owners first, then regenerate descendants; never create package-side shadow authority.
```

## 21. Lossless preservation obligations

Implementation/qualification/Review SHALL preserve all of the following. These grouped obligations supersede the fifth-review workplan's enumerative acceptance numbering while preserving every previously identified failure class.

### P64-A — Accepted Protocol 6 inheritance

Preserve accepted D1-D4 authority boundaries; concretization/abstraction adequacy; evidence lifecycle/applicability; Serious Challenge/human gates; bounded impact closure; lossless representation/progressive disclosure; source-generated ownership; current-vs-history separation; project-memory non-authority/HAS/binding semantics; and minimum justified mechanism.

### P64-B — Frozen version/recovery/package preservation

Keep all frozen 5.16/6.0/6.1/6.2/6.3 source/profile/package/bootstrap/recovery artifacts byte/behavior stable as applicable. Generate distinct 6.4 resources. Keep public bootstrap distinct from recovery and use exact immutable refs.

### P64-C — Formal-first semantic availability

Require non-foundational substantive semantic objects to be source-available before use and context-available before agent inference. Permit bounded foundational knowledge, exact imports, explicit project declarations/primitives, and local binders. Prevent foundational-scope laundering and hidden prerequisites.

### P64-D — Unique current meaning and owner conflict

Keep one current semantic owner per material object/scope. Coordinated clauses and aliases may compose one owner; incompatible simultaneously applicable meanings remain unresolved/Challenged rather than selected by order/latest/routing convenience.

### P64-E — Claim/role/provenance separation

Keep availability basis, semantic role, novelty, support, evidence, and normative force orthogonal. Role tags are extensible status descriptors, not a closed ontology. Distinguish definition, axiom, premise, assumption, derived/conjectural/empirical/approximate claims, normative contracts, examples, and observations when material.

### P64-F — Definition and mathematical well-definedness

Enforce definitional conservativity; explicit domain/type/shape/unit; scope/quantifiers; partiality/failure; branch/selection/piecewise semantics; existence/uniqueness; exact/approximate/equivalence/logical direction; dimensional consistency; stochastic semantics; state/temporal semantics when material; and no under-formalization escape hatch.

### P64-G — Parameterized family/instance discipline

Distinguish parameterized families from instantiated objects; define parameter domains/units/constraints, free/fixed/derived/default/external bindings, parameter-dependent validity/error semantics, and the owning level of defaults. Bind evidence to material parameter/regime identity and review governed default changes.

### P64-H — Import/source/provenance/trust discipline

Bind specialized imports to exact source/variant/locator and verify support. Preserve source-to-local notation/unit/transformation lineage and empirical uncertainty/conditions. Separate support from normative force. Treat imported/external content as data, not instruction, under security/trust boundaries.

### P64-I — Typed semantic dependency and impact

`USES_DEFINITION` records direct material semantic-meaning prerequisites for any governed semantic unit, including primitives/theorems/assumptions/algorithms/contracts. Keep derivation, assumption, constraint, concretization, evidence, execution, supersession, and replacement relations separate. Preserve acyclic external semantic-definition-use trace with composite recursive nodes and materially complete declared scope.

### P64-J — Validity, approximation, warrant, and non-circularity

Discharge/assume/propagate material hypotheses and validity. Preserve approximation/uncertainty status downstream. Require bounded typed warrant closure for established claims without pure or mixed-relation self-supporting cycles.

### P64-K — Identity, equivalence, composition, evolution

Keep semantic identity distinct from labels/anchors/family names/default values. Require version-coherent composition; unknown compatibility is review-required. Establish representation-only equivalence rather than assuming it. Reconcile split/merge/retirement, source corrections, owner mutations, descendants/evidence, and semantic history.

### P64-L — D1-D4 abstraction fit

Use strongest practical formal representation in D1/D2 and formal relations/contracts in D3/D4 where ambiguity reduction is material, without decorative mathematics, upstream leakage of incidental implementation, or freezing delegated mechanisms.

### P64-M — Human-facing/self-hosting/presentation integrity

Define newly appearing non-common terminology and first-use non-obvious abbreviations; keep natural-language interpretation; self-host 6.4 on current canonical references/workplan; keep historical documents frozen; and ensure supported render/link/formula surfaces preserve readable canonical meaning.

### P64-N — Bounded adoption and runtime routing

Older version-bound work remains governed by its version. Bounded 6.4 adoption reconciles only material scope. Semantic dependency is not activation; load canonical prerequisites before inference. Generated graphs/indexes remain subordinate.

### P64-O — Lifecycle and Protocol-7 isolation

Qualify assembled 6.4 source/generated/package/profile/Core surfaces, publish self-reference-safe bootstrap then independent Review then distinct recovery, reconcile mapping-bearing descendants, perform closeout learning, and add only a narrow Protocol-7 6.4 inheritance reconciliation after acceptance.

## 22. Qualification and counterfactual requirements

Qualification SHALL pair each material positive claim with discriminating negative/counterfactual cases. The following families are mandatory; the previously identified fifth-review cases are preserved as regression examples within these families rather than as a hot-path 112-item proof script.

### QF64-A — Undefined/import/foundational boundary

Fail specialized terms/symbols/methods used before definition/import, hidden roots, expert-audience laundering, wrong/missing source variant, and unsupported citations. Pass genuine foundational objects and precise imported prerequisites.

### QF64-B — Owner conflict and canonicality

Fail two materially conflicting simultaneously applicable current meanings when routing/latest/file order silently chooses one. Pass coordinated owner clauses or aliases proven to denote one compatible canonical object.

### QF64-C — Primitive/binder/scope/role classification

Fail undeclared primitives, ambiguous shadowing, false mutually exclusive provenance/role classification, and validators that treat the illustrative role list as a closed ontology. Pass explicit primitives, scoped binders, and real additional statuses such as conjecture/example/observation when semantically needed.

### QF64-D — Definition laundering and conservativity

Fail desired properties asserted only by naming/`:=`, explicit definitions that create new truth about old vocabulary, vacuous inconsistent premise sets, and empirical/normative claims hidden inside definitions. Pass conservative definitions plus separately warranted additional claims.

### QF64-E — Well-definedness/logical/type/dimension

Fail ambiguous argmin/fixed-point/choice, piecewise gaps/overlap, partial-as-total mappings, branch ambiguity, dimensional inconsistency, quantifier/necessary-sufficient reversal, undefined operators, and materially ambiguous state/time/order semantics. Pass explicit alternatives/selection/typing/units/logical direction.

### QF64-F — Parameterized family/instance/defaults

Fail a parameterized method whose parameter domain/binding/default is ambiguous, family/instance identity collapse, evidence reused across materially different bindings, or a governed default change treated as automatically non-semantic. Pass explicit family/instance binding, owning default semantics, and evidence/impact reconciliation.

### QF64-G — Stochastic/approximation/validity

Fail underspecified IID/correlation/conditioning/convergence, cited theorem with false/undischarged hypotheses, bounded approximation promoted to exactness, or widened validity. Pass sufficient stochastic semantics and explicit discharge/assumption/propagation.

### QF64-H — Typed dependency/trace completeness/cycles

Fail definition-only trace implementations that omit theorem/assumption/algorithm/contract uses, omitted material direct prerequisites, raw semantic cycles, partial traces used to infer independence, and missing canonical endpoint. Pass materially complete direct semantic-use trace and composite recursion.

### QF64-I — Warrant/evidence/proof separation

Fail circular `DERIVED_FROM`, mixed-relation circular warrant, empirical evidence presented as deductive proof, citation used to mint authority, or evidence dependency inferred solely from semantic-use relation. Pass claim-appropriate independent roots and typed relations.

### QF64-J — External support/force/transformation/trust

Fail citation prestige treated as binding contract, binding constraint with no real authority route, transformed data with only raw-source provenance, floating `latest`, or external instruction-like content followed as agent instruction/tool authorization. Pass explicit authority route, source transformation lineage, source lifecycle review, and inert-data handling.

### QF64-K — Version composition/identity/equivalence/evolution

Fail incompatible mixed D1-D4 versions, stable labels used as proof of semantic continuity, duplicated editable aliases, unreconciled split/merge, or source/definition mutation with stale dependents/evidence. Pass coherent snapshot/compatibility mapping, independently established equivalence, and lineage closure.

### QF64-L — Cross-domain abstraction adequacy

Fail D1/D2 depending on incidental D4 helpers, D3/D4 claiming upstream preservation with no typed route, decorative formalism that freezes lower mechanisms, or D4 exactness/uniqueness strengthening upstream set-valued/approximate semantics. Pass exact lower-to-upstream preservation routes.

### QF64-M — Runtime availability/progressive disclosure

Fail inference from a discoverable-but-unloaded prerequisite. Pass version-bound loading before substantive inference while keeping semantic edges distinct from activation/eager loading.

### QF64-N — Human-facing/self-hosting/presentation

Fail specialized core terminology or non-obvious abbreviations used before explanation, current 6.4 references violating their own doctrine, broken rendered formulas/links/anchors, or examples becoming authority by placement. Pass readable notation-preserving supported surfaces and subordinate examples/background.

### QF64-O — Frozen/generated/profile/bootstrap/recovery lifecycle

Fail frozen predecessor mutation, generated-source mismatch, invalid/mutable/self-naming public bootstrap, schema bump solely for prose doctrine, recovery published before independent PASS, or Protocol-7 D3 mutation through inheritance reconciliation. Pass exact frozen-resource, package/profile/Core, bootstrap/recovery, and inheritance checks.

### QF64-P — Current-contract representation

Fail a live 6.4 handoff that requires replaying superseded review amendments or embeds old review chronology as current obligations after the same semantics are integrated. Pass one current snapshot-complete workplan while exact prior designs remain recoverable from archive/Git.

## 23. Independent falsification passes

Independent assembled-candidate Review SHALL execute at least these bounded passes:

- **F64-A Alternate-formalization:** construct materially different meanings satisfying representative prose.
- **F64-B Hidden-prerequisite/foundational:** trace roots and challenge undeclared specialized knowledge.
- **F64-C Owner-conflict/canonicality:** search for competing current meanings, duplicate owners, and order/latest resolution.
- **F64-D Claim/provenance/warrant:** search for definition/proof/evidence/citation/normative-force laundering and mixed warrant cycles.
- **F64-E Well-definedness/parameterization:** attack existence/uniqueness/choice, type/dimension, logical direction, parameter domains/defaults/instances, stochastic and temporal semantics.
- **F64-F Typed dependency/impact:** mutate semantic prerequisites, inspect descendants, and challenge missing/wrong typed edges.
- **F64-G Composition/identity/equivalence:** attack mixed versions, alias duplication, stable-label continuity, parameter-instance collapse, split/merge/retirement.
- **F64-H External-source/trust:** falsify source support, variant/locator, transformation lineage, binding-force routing, correction/retraction handling, and instruction-like external content.
- **F64-I Cross-domain/formalism-overreach:** seek upstream leakage, decorative mathematics, frozen delegated mechanisms, and wrong exactness/uniqueness strengthening.
- **F64-J Progressive-disclosure/runtime:** attempt inference from unloaded prerequisites and accidental eager activation of all semantic edges.
- **F64-K Self-hosting/presentation/current-vs-history:** apply 6.4 to its own current references/workplan, inspect abbreviations/rendering, and confirm old review chronology is not needed for current semantics.
- **F64-L Lossless inheritance/lifecycle:** re-run inherited 6.3 preservation/routing/PEM/package/profile/bootstrap/recovery/Challenge oracles and prove Protocol-7 isolation.

## 24. Implementation stages

### Stage A — Canonical doctrine

1. Amend `abstraction-and-concretization.md` with source availability, owner-conflict uniqueness, core semantic-unit terminology, definition closure, primitive roots, and derived-trace subordination.
2. Rewrite `scientific-technical-writing.md` around formal-first/axiomatic doctrine, parameterized family/instance semantics, claim separation, import/trust discipline, and human readability.
3. Add D1/D2 mathematical consequences and D3/D4 formal-contract consequences without domain leakage.
4. Amend `evidence-evolution-and-dependencies.md` to own widened `USES_DEFINITION`, durable endpoints, completeness/absence, parameter-sensitive impact/applicability interaction, and source-binding evolution.
5. Reconcile documentation/workflow/testing/versioning/security owners only for their local consequences.
6. Reconcile `source/SEMANTIC_DEPENDENCIES.md` as a derived current view.
7. Apply the new doctrine proportionately to current 6.4 canonical references and this workplan; frozen predecessors remain untouched.

### Stage B — Versioned profile/source integration

1. Set candidate `source/PROTOCOL_VERSION` to `6.4.0` at the appropriate candidate stage.
2. Generate distinct `ssdp-protocol-6.4` profile/snapshot/package resources through existing generators.
3. Keep profile schema v2 unless a separately justified machine-contract change is required.
4. Keep all prior frozen resources byte-identical.
5. Update current manifests/README/AGENTS/history/current authority surfaces without claiming accepted-current/recovery prematurely.

### Stage C — Qualification

1. Implement all QF64-A..QF64-P families with positive/negative fixtures and semantic review where automation cannot decide the claim.
2. Preserve coverage of every previously identified fifth-review counterexample class; compaction of numbering is not permission to weaken the oracle.
3. Re-run complete inherited repository regression and applicable 6.3 qualification/preservation oracles.
4. Independently build/validate packages and committed distribution parity.
5. Verify profile/snapshot/Core acceptance when affected.
6. Verify frozen predecessor trees byte-identically.
7. Execute self-hosting review over current 6.4 references/workplan.
8. Execute supported Markdown/link/anchor/LaTeX/source-to-render integrity checks and human presentation inspection where supported.
9. Include security counterfactuals demonstrating external source/evidence content remains inert data rather than an instruction channel.

### Stage D — Semantic candidate and public bootstrap

1. Freeze immutable 6.4 semantic candidate only after semantic-source repairs/qualification.
2. Construct/qualify an already-existing self-reference-safe public-source bootstrap that does not need to self-name its SHA.
3. Publish exact bootstrap identity only from a later descendant.
4. Re-run exact-ref remote source/package/profile/routing realization after publication.
5. Preserve failed bootstrap attempts as historical evidence only.

### Stage E — Independent assembled-candidate Review

Reviewer reconstructs from accepted Protocol 6.3 plus this single consolidated handoff, not implementer conclusions or historical design snapshots. Review P64-A..P64-O, QF64-A..QF64-P, F64-A..F64-L, frozen resources, owner-conflict/source/context availability, parameterization/defaults, semantic-use/type/validity/warrant/trace semantics, external support/force/trust, generated/profile/schema surfaces, exact-ref bootstrap, self-hosting, presentation integrity, and compatibility.

Any material semantic mutation after the reviewed candidate reopens affected qualification/Review.

### Stage F — Recovery and closeout

Only after independent PASS:

1. select an already-existing immutable recovery target containing reviewed candidate/evidence/Review through ancestry;
2. publish `6.4.0 -> <recovery SHA>` from a later descendant;
3. regenerate mapping-bearing descendants and rerun recovery/bootstrap-distinction/package/profile/Core acceptance;
4. reconcile semantic history, authority index, README/AGENTS, accepted-current release text, and any affected security/documentation routes;
5. add narrow Protocol-7 6.4 inheritance reconciliation without changing/re-accepting its D3 architecture or authorizing D4;
6. perform PEM closeout-learning assessment;
7. archive this workplan only after current semantics/lifecycle state reside in canonical owners.

## 25. Non-goals

Protocol 6.4 does not:

- require every sentence to be mathematical notation;
- require re-proving foundational mathematics/science;
- classify all graduate-level knowledge as foundational;
- replace natural-language explanation/motivation/interpretation/rationale/limitations;
- require theorem proving, symbolic-math checking, global ontology, citation database, semantic hash registry, warrant registry, shadow definition store, or universal dependency graph;
- claim automated proof of mathematical/scientific correctness, theorem applicability, warrant sufficiency, source support, semantic equivalence, or owner conflict resolution;
- turn literature/background/evidence/examples into project authority;
- deny the normative force of genuinely applicable external constraints whose real owner makes them binding;
- treat external source/evidence prose as instruction merely because an agent loads it;
- change existing project scientific/numerical meaning merely to improve representation;
- retroactively rewrite frozen historical protocol artifacts;
- change PEM schema solely for definition traceability;
- mutate Protocol-7 D3/control-plane semantics or authorize Protocol-7 implementation/cutover;
- force a full project documentation rewrite on bounded 6.4 adoption;
- force formalization beyond the owning domain's abstraction boundary;
- permit material ambiguity to be declared closed because stronger formalization is inconvenient;
- require review-history narration in the current implementation handoff after current semantics are consolidated.

## 26. Reopen / Challenge triggers

Reopen the earliest affected owner when:

- strict traceability requires changing D1-D4 semantics rather than representing them;
- foundational/imported/project-declared boundaries remain materially ambiguous;
- two simultaneously applicable current semantic-owner statements materially conflict;
- source-level availability or unique canonical meaning cannot be established;
- a formal definition is ill-defined or requires unresolved existence/uniqueness/consistency assumptions material to outcome;
- a parameterized family/instance/default binding is materially ambiguous or evidence applicability cannot be bounded across parameter changes;
- theorem/result hypotheses cannot be discharged/assumed/propagated coherently;
- an established claim's warrant is circular, unavailable, or incompatible with its claim class;
- typed semantic-use/derivation/validity relations conflict with dependency authority;
- cross-domain dependencies create an unjustified upstream implementation back-edge;
- composed authority cannot be made version-coherent without semantic migration;
- external support, normative-force routing, or source trust cannot be resolved;
- imported data transformation prevents recoverable source-to-local semantic identity;
- formal representation freezes delegated lower mechanisms;
- strongest practical formalization still leaves materially different interpretations without accepted uncertainty/Challenge treatment;
- 6.4 cannot preserve frozen 6.3 capability/profile/recovery contract;
- a validator would need to adjudicate semantic truth rather than structural well-formedness;
- a profile/schema change is actually required and its machine-contract owner has not justified it;
- Protocol 7 cannot inherit accepted 6.4 without genuine D3 architecture mutation.

**SIXTH DESIGN REVIEW VERDICT: PASS — blockers 0; Serious Challenges 0.**

## 27. Stage-E repair closure — 2026-09-15

The Stage-E NO-PASS on `0377e798fbbb1054badd1193950d9c10f723be75` identified three blocking findings. Their detailed review chronology remains recoverable in Git and the review handoff; this current handoff records only the resolved contract and the remaining lifecycle gate.

- **SC64-R1 — RESOLVED at D3.** Canonical `USES_DEFINITION` orientation is `subject -> prerequisite`. Formally, `(s,p) in E_D^def` means the canonical semantic statement of subject `s` directly requires prerequisite `p`. A prerequisite mutation discovers dependent subjects by reverse traversal. Stored semantic direction and impact traversal direction are distinct.
- **B64-R2 — RESOLVED at D4 qualification.** QF64-H now encodes subject/prerequisite endpoint roles, rejects the same endpoints with a reversed `USES_DEFINITION` edge, and rejects an impact query that fails to reach the dependent subject from the changed prerequisite while preserving the existing completeness, endpoint, relation-family, cycle and composite-recursion checks.
- **B64-R3 — RESOLVED at canonical source plus D4 qualification.** The Protocol 6.4 public-bootstrap Markdown fence in `protocol-versioning-and-compatibility.md` closes on its own line. A bounded structural Markdown-fence oracle executes over the current 6.4 canonical owner/handoff surfaces and includes a malformed closing-fence-plus-prose negative fixture.

The D3 direction repair is a clarification of the already-implemented subject-to-prerequisite semantics in the canonical 6.4 source owners and derived dependency view; it does not alter the scientific/numerical/software meaning of the published self-reference-safe bootstrap `e09a9d1480211eea2d16d722182bb5c6de1bee12`. The additional source sentences make the already-existing direction/impact distinction explicit. Therefore the published bootstrap identity remains valid; no new bootstrap or recovery identity is invented by this repair.

### Fresh Stage-E re-entry gate

Before Stage F, freeze a new immutable assembled review target containing these repairs and fresh applicable qualification evidence, then perform a fresh independent Stage-E Review against accepted Protocol 6.3 repository state `0928accd337a13f864b292ed81c36372828cfb4c`. The re-review SHALL cover all P64-A..P64-O, QF64-A..QF64-P and F64-A..F64-L obligations, not only the three repaired findings. Until that Review passes, Protocol 6.3 remains accepted-current, Protocol 6.4 recovery remains absent, and Stage F remains blocked.
