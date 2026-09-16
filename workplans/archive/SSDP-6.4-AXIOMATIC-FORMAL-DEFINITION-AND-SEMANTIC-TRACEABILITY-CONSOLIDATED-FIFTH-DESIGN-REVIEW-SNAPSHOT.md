---
kind: abstraction-concretization-change-plan-consolidated
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED
consolidates:
  - SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY
  - SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-REVISION-1-SECOND-DESIGN-REVIEW-CLOSURE
  - SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-REVISION-2-THIRD-DESIGN-REVIEW-CLOSURE
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: active
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: pass-after-fifth-review
implementation_handoff: authorized
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
reviewed_composed_head: f94723215dc0ed9eeadf0bc298e4cce579fab810
branch_point: 0928accd337a13f864b292ed81c36372828cfb4c
accepted_parent_protocol: 6.3.0
accepted_parent_recovery: 9f353097fab36e325a325f1c2f9d9cec32e86177
accepted_parent_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
---

# SSDP 6.4 — Axiomatic Formal Definition and Semantic Traceability — Consolidated Workplan

## Current disposition

**FIFTH DESIGN REVIEW: PASS AFTER GAP CLOSURE.** This file is the single current implementation/review handoff for Protocol 6.4. The original parent and Revisions 1-2 remain immutable design-review history and Git evidence, but implementation and independent Review SHALL NOT need to replay their amendment precedence to reconstruct the current contract.

Protocol 6.3 remains accepted-current until Protocol 6.4 completes implementation, qualification, independent assembled-candidate Review, self-reference-safe public-bootstrap publication, immutable recovery mapping, mapping-bearing generated reconciliation, Protocol-7 inheritance-only reconciliation, and lifecycle closeout.

The protected outcome is not “more equations.” It is:

> Every materially governed technical concept can be reconstructed by a competent intended reader or downstream agent with minimum interpretive freedom; specialized prerequisites, assumptions, validity, provenance/support, authority force, and direct semantic dependencies are recoverable; formal expressions are well-defined; claim warrant is non-circular; and changes can be propagated through bounded typed impact closure without prose inference, hidden context, mixed-version meaning, or lower-domain semantic leakage.

## Background and formal terminology

The **Scientific Software Development Protocol (SSDP)** separates four semantic authority domains: **D1 scientific and mathematical formulation**, **D2 algorithm and numerical method**, **D3 software architecture**, and **D4 specification and implementation**. **Project Engineering Memory (PEM)** is project-local evidence-backed decision support and is not a fifth authority domain. A **Historical Applicability Set (HAS)** is the session-local workflow record of materially relevant PEM items and their applicability dispositions.

For a governed scope `S`, a **semantic object/unit** is a materially governed term, symbol, quantity, operator, relation, state, proposition, algorithmic object, invariant, or contract whose meaning or conditions can alter governed interpretation, admissible concretization, evidence applicability, or acceptance if changed. This is a semantic identity, not merely a spelling, symbol, anchor, or file location.

A **canonical semantic statement** of object `x` is the one current owner statement that establishes the project-visible meaning of `x` for the governed scope. Depending on role it may be a primitive declaration, explicit/implicit definition, proposition/theorem statement, assumption/premise statement, algorithmic contract, or D3/D4 contract. For externally imported knowledge, the canonical project-visible statement includes the precise local statement plus its exact source route; the external source does not thereby become project authority.

A **substantive semantic use** of `x` is an occurrence whose meaning participates in a declaration/definition, premise, inference, constraint, theorem/result statement, algorithm, contract, acceptance decision, or interpretation. A harmless forward name in an abstract/summary that supports no inference is not a substantive use.

A **material direct prerequisite** `x` of semantic unit `y` is one whose meaning is directly invoked by the canonical semantic statement of `y`, and for which a materially different admissible meaning of `x` can change the denotation, admissible domain, validity, governed contract, or accepted interpretation of `y`. Materiality is bound by the existing governed scope; an author may not narrow it merely to make a trace appear complete.

A **directed acyclic graph (DAG)** is a directed graph with no directed cycle. A **strongly connected component (SCC)** is a maximal set of nodes mutually reachable by directed paths; legitimate mutually recursive definitions may be represented as one composite node or by condensation of such a component.

The rest of this workplan uses these terms normatively. Where a generic predicate such as `available(x)` would be ambiguous, it distinguishes source-level semantic availability from runtime-context availability explicitly.

## 1. Parent authority and compatibility

Protocol 6.4 is a backward-compatible **minor** strengthening over accepted Protocol 6.3. It preserves all accepted 5.16/6.0/6.1/6.2/6.3 doctrine and historical capability unless this workplan explicitly strengthens representation.

The following remain invariant:

- D1-D4 remain the only semantic authority domains; no D5, documentation authority plane, ontology authority, or traceability authority is created.
- Accepted current authority defines what must be true; literature, tests, evidence, documentation, PEM, generated graphs, and historical frequency cannot silently mint authority.
- Applicable external contracts, standards, regulations, or stakeholder constraints retain whatever normative force their real governing authority supplies; citation/import alone does not create that force.
- Concretization fidelity and abstraction adequacy remain distinct.
- One detailed owner per generic rule, progressive disclosure, explicit typed routing, cold-path discoverability, and derived-view subordination remain binding.
- Evidence specification -> realization -> observation -> assessment remains binding.
- Serious Challenge, human adjudication where assigned, bounded impact closure, Review/Verification/Stabilization, and workflow semantics remain binding.
- PEM remains schema-1 project-local evidence-backed decision support, conditionally activated, non-authoritative, and version-independent unless separately changed through its owner.
- Frozen 5.16/6.0/6.1/6.2/6.3 source/profile/recovery/bootstrap/qualification artifacts remain immutable.
- Protocol 6.3 public bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11` and recovery `9f353097fab36e325a325f1c2f9d9cec32e86177` remain distinct and valid for version-bound 6.3 work.
- Protocol 7 remains proposed/pre-cutover. Existing Protocol-7 D3/control-plane semantics are not changed by 6.4 implementation; after 6.4 acceptance, only a narrow inheritance reconciliation is authorized unless Protocol 7 independently reopens D3.

## 2. Governing semantic-availability invariant

For a version-coherent composed authority family `D`, define **source-level semantic availability**:

\[
\operatorname{source\_available}_D(x)
\]

iff the canonical semantic statement of `x` is reconstructible within `D` from the declared foundational envelope, an exact external import, a project declaration/definition, or a valid local binder whose referenced domain/type is already source-available.

For an actual agent/reader runtime context `C`, define **context availability**:

\[
\operatorname{context\_available}_C(x)
\]

iff the exact canonical meaning required for the current inference is actually supplied/loaded in `C` under the governing version/snapshot.

The authoring/document invariant is:

\[
\boxed{
\operatorname{use}_D(x)
\Rightarrow
\operatorname{source\_available}_D(x)
}
\]

and the runtime inference invariant is:

\[
\boxed{
\operatorname{infer}_C(x)
\Rightarrow
\operatorname{context\_available}_C(x)
\Rightarrow
\operatorname{source\_available}_D(x)
}
\]

A route can make an object source-available without loading it into a particular runtime context. Conversely, runtime prose or hidden chat cannot make an object source-available when no canonical version-bound owner/source exists.

The source-availability basis is:

\[
\operatorname{availability\_basis}(x)
\in
\{\mathrm{FOUNDATIONAL\_ASSUMED},\mathrm{EXTERNAL\_IMPORTED},\mathrm{PROJECT\_DECLARED}\},
\]

or a scope-local binder/declaration whose referenced domain/type is already available at the corresponding layer.

This is an availability classification, not a claim of historical discovery, intellectual provenance, evidence strength, or normative force.

Semantic/epistemic roles are non-exclusive:

\[
\operatorname{roles}(x)\subseteq
\{\mathrm{PRIMITIVE},\mathrm{DEFINITION},\mathrm{AXIOM},\mathrm{PREMISE},\mathrm{ASSUMPTION},\mathrm{DERIVED\_RESULT},\mathrm{EMPIRICAL\_RELATION},\mathrm{APPROXIMATION},\mathrm{HEURISTIC},\mathrm{NORMATIVE\_CONTRACT}\}.
\]

Novelty/priority is a separate optional claim such as `BORROWED`, `ADAPTED`, `INDEPENDENTLY_DERIVED`, or `ORIGINAL_CONTRIBUTION`; it requires appropriate literature/evidence and is never inferred merely from `PROJECT_DECLARED`.

## 3. Axiomatic semantic order

A compliant authority family may use flexible visual organization, but its semantic dependency order is equivalent to:

```text
FOUNDATIONAL_ASSUMED reader knowledge
+ exact EXTERNAL_IMPORTED specialized prerequisites
+ PROJECT_DECLARED primitive objects/signatures
 -> explicit axioms/premises/assumptions/validity conditions
 -> definitions from available objects
 -> derived propositions/theorems/results
 -> algorithms/contracts/consequences using those semantics
 -> interpretation/evidence/rationale/limitations/explanatory prose as appropriate
```

Definitions/results may be interleaved when dependency order remains valid. A later definition cannot retroactively supply meaning required by an earlier normative inference. Brief forward naming in abstracts/summaries is allowed only when no normative inference depends on the undeclared meaning and the canonical definition route is explicit.

## 4. Foundational knowledge envelope

Each human-facing authority document/family establishes an intended competent reader and a bounded foundational knowledge envelope. Ordinary logic, numbers, standard calculus, linear algebra, probability, common mathematical notation, and similarly broad scientific foundations may be assumed when genuinely standard for that audience.

The envelope is not an author-controlled escape hatch. The following are not foundational merely because the reader is expert:

- project-specific terms/models/abbreviations/conventions;
- specialized named theories/methods/theorems with materially different variants;
- field-specific sign/normalization/boundary/estimator conventions that can change conclusions;
- specialized results whose applicability assumptions are material to the project argument.

Use the conservative rule:

\[
\operatorname{uncertain\_foundational}(x)\Rightarrow\operatorname{define\_or\_import}(x).
\]

A genuine common theorem/axiom may be invoked without local proof/citation when the intended audience can identify the exact standard statement unambiguously and no variant distinction matters.

Changing the foundational envelope materially for a current authority family is itself a representation-scope change and receives bounded review; it cannot be silently widened to make unresolved definitions disappear.

## 5. External specialized imports, support, and authority force

A specialized external theorem, model, algorithm, method, physical approximation/law, software/engineering standard, empirical constant, reference value, table, dataset, or other external result is `EXTERNAL_IMPORTED` when the project relies on external knowledge/evidence/constraint rather than deriving/declaring it independently.

Before normative reuse, supply:

1. a precise local statement sufficient to determine the exact imported meaning/variant;
2. material symbols/domains/assumptions/conventions/validity restrictions;
3. authoritative source identity, preferring primary literature or a canonical standard/official reference where appropriate;
4. edition/version/revision and theorem/section/equation/clause/dataset release or equivalent stable locator when variants matter;
5. explicit source-to-local notation/unit/sign/frame/normalization mapping when they differ;
6. for empirical constants/data/reference values, material reference conditions, units, uncertainty/error, calibration/version/date/regime, or other qualifiers needed for correct use;
7. when the imported data/value is filtered, transformed, calibrated, aggregated, nondimensionalized, unit-converted, or otherwise changed before local use, the material source-to-local transformation and parameters/selection rules needed to reconstruct the local semantic input.

Citation presence is not source support. Independent Review must establish that the cited source actually supports the imported claim under the stated assumptions and regime.

External **semantic support** and external **normative force** are separate. Scientific literature, datasets, measurements, and explanatory standards references may supply knowledge/evidence without becoming project authority. An applicable contract, regulation, mandatory standard, stakeholder rule, or other external constraint can govern because the real external/project authority makes it binding; the local document must route that force to the actual owner/constraint rather than infer it from citation prestige or publication status.

Background normally introduces specialized imported prerequisites for D1/D2 human-facing papers, but Background does not create project authority. When an imported result is a normative premise, the owning D1-D4 formulation explicitly invokes/assumes it under stated conditions. When an imported external constraint is itself binding, its binding route remains explicit and separate from the citation used to state it.

A floating `latest` source is inadequate when later changes could alter meaning. Retraction, correction, incompatible revision, loss of required access, or discovery that the source does not support the claim is a current binding/applicability event: review dependent use; do not silently switch editions. Semantically equivalent source remapping may be accepted through normal review without manufacturing a semantic change.

An independent local derivation can establish a result without depending on the external proof, but it neither creates a novelty claim nor erases known literature when priority/originality is itself asserted.

## 6. Project primitives and local binders

A non-foundational project root need not be constructively defined. It may be an explicit primitive if the current formulation supplies enough signature and constraints to bound its meaning.

For a primitive, state as applicable:

- name/symbol and role;
- sort/type/domain/codomain/shape/unit;
- scope;
- axioms/constraints/relations characterizing admissible use;
- whether existence/non-emptiness is assumed, constructed, or established;
- validity regime and interpretation when material.

Anything beyond the declared signature and axioms/constraints remains unavailable.

Definition closure may therefore terminate in:

```text
FOUNDATIONAL_ASSUMED reader knowledge
EXTERNAL_IMPORTED specialized knowledge with exact source support
PROJECT_DECLARED primitive with explicit signature/axioms
PROJECT_DECLARED definition whose prerequisites close recursively
```

Local variables introduced by a binder/declaration become available within that scope, e.g.

\[
\forall x\in X:P(x),\qquad \sum_{i=1}^{N}a_i.
\]

Here `x` and `i` are locally bound; `X`, `P`, `N`, and the indexed family `a_i` must already be available at the corresponding source/context layer. Scope-local shadowing is allowed only when unmistakable and non-ambiguous.

## 7. Definition, premise, assumption, claim, and example discipline

- **Definition:** stipulates meaning relative to already available objects; it does not by notation establish empirical truth, existence, optimality, convergence, stability, safety, adequacy, or authority.
- **Axiom:** explicitly accepted proposition of a formal system, not derived inside that system.
- **Premise:** proposition imported or otherwise accepted for a bounded argument.
- **Assumption:** conditional premise adopted for a bounded model/method/regime and therefore part of validity/interpretation.
- **Derived result:** proposition established from stated premises/definitions through recoverable derivation/proof appropriate to the claim.
- **Empirical relation:** observation/model relationship supported by empirical evidence rather than deductive proof.
- **Normative contract:** requirement adopted by project/external authority; normative force comes from that owner.
- **Example/counterexample:** explanatory or falsification instance; it is non-normative unless the owning authority explicitly adopts its values/behavior as a governed case.

Writing `:=` cannot manufacture a proposition. A name such as “stable method” may be defined, but applying that name to a method requires the stability property to be separately established/assumed/contracted. Existence, uniqueness, causal, empirical, comparative, convergence, safety, and adequacy claims embedded inside apparent definitions must be exposed separately with appropriate warrant.

For an **explicit definitional extension** that merely introduces a new symbol/name in prior vocabulary `T`, the definition is conservative: it must not create a new proposition about the pre-existing vocabulary merely by being called a definition. Conceptually, if `d` is only a definition and `\varphi` contains no newly defined symbol,

\[
T\cup\{d\}\vdash\varphi\quad\Rightarrow\quad T\vdash\varphi.
\]

When a proposed “definition” also asserts existence, uniqueness, admissibility, causal/empirical truth, comparison, convergence, safety, or normative requirement, separate that additional claim as an assumption/axiom/result/empirical claim/contract and warrant it appropriately. Implicit/recursive definitions may constrain a jointly introduced object, but their existence/well-posedness is separately assumed or established as required.

Semantic roles may be non-exclusive, but that is not permission to collapse logically different claim units. If one sentence/formula contains a definitional statement plus an empirical, derived, approximate, or normative assertion, make the separable claims recoverable with their own status/warrant.

Project-local axiom/assumption sets must be coherent enough for governed use. When non-emptiness, consistency, realizability, or existence of admissible states is material, provide a construction/model/witness/derivation or mark the condition explicitly unresolved; do not claim substantive conclusions solely by vacuity. Protocol 6.4 does not require foundational consistency proofs for ordinary mathematics.

## 8. Formal well-definedness, notation, type, dimension, and logical direction

Formal appearance is insufficient. A governed definition/contract must be well-defined over its intended scope.

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
- exact equality, definitional equality, equivalence, approximation, asymptotic relation, assignment/update, membership, implication, distributional relation, or other materially distinct relation actually intended;
- necessary, sufficient, necessary-and-sufficient/biconditional direction when changing that direction changes the conclusion or admissible set.

Use relation/operator notation consistently enough that a competent reader cannot confuse, for example, mathematical equality with assignment, approximation with identity, equality in distribution with pointwise equality, or a sufficient condition with a necessary one. Define nonstandard operators before reuse.

Where physical/typed quantities are involved, expressions and mappings must be dimensionally/type consistent. A declared unit does not rescue a dimensionally inconsistent equation. Nontrivial unit conversions, affine/logarithmic units, nondimensionalization, or coordinate transforms that can change interpretation must be explicit.

Quantifier order is semantic. `for all x exists y` and `exists y for all x` must not be interchangeable through prose compression. Index ranges and scopes that affect boundary/reduction semantics must be explicit.

For

\[
x^*=\operatorname*{argmin}_{x\in X}f(x),
\]

if later reasoning treats `x*` as one deterministic object, establish/assume uniqueness, define a selection rule, or use set-valued semantics.

A fixed-point/implicit definition must identify the intended solution set and required selection/uniqueness semantics. D3/D4 cannot silently strengthen a set-valued/approximate D1/D2 object into a unique/exact one.

If the strongest practical formal/structured representation still leaves two materially different interpretations that can change governed meaning, the ambiguity is not excused merely because fuller formalization is inconvenient. Preserve the ambiguity explicitly as `REVIEW_REQUIRED`/Challenge or refine the owning abstraction until the protected outcome is unambiguous enough for its intended descendants.

## 9. Stochastic semantic closure

When randomness materially affects scientific/numerical meaning, define enough stochastic structure to distinguish materially different interpretations. As applicable state:

- random object/variable and its state/sample space;
- governing distribution/law or sampling mechanism;
- independence/dependence/exchangeability/conditioning assumptions;
- conditioning sigma-field/information set when material;
- expectation/probability/variance/quantile or estimator semantics;
- finite-sample vs asymptotic statement;
- almost-sure/in-probability/in-distribution/mean-square or other convergence mode;
- stochastic seed/reproducibility policy when it is part of D2/D4 governed behavior.

Do not require a full measure-theory restatement when common probability foundations suffice. Do require the distinctions that can change the result. A phrase such as “draw random samples” is inadequate when **independent and identically distributed (IID)** versus correlated sampling materially changes the estimator or guarantee.

## 10. Assumption, validity, applicability, and approximation closure

For every material use of imported or derived result `r` with hypotheses/validity conditions `H(r)`:

\[
\operatorname{use}(r)\Rightarrow\operatorname{discharged\_or\_propagated}(H(r)).
\]

Each material condition is either:

1. established from available premises/results;
2. explicitly adopted as an assumption by the owning formulation; or
3. explicitly propagated as a condition on the dependent result/concretization.

A citation or definition-use edge does not discharge hypotheses. Known-false conditions invalidate the use. Materially uncertain satisfaction is `REVIEW_REQUIRED`/challenged as appropriate.

Validity, uncertainty, approximation, and assumption relations remain typed rather than being collapsed into `USES_DEFINITION`. Descendants may narrow a validity regime but cannot silently broaden it or promote an approximation/empirical relationship into an exact unconditional identity.

## 11. Derivation, proof, and warrant closure

For material `DERIVED_RESULT` claims, expose direct proof/premise dependencies proportionately to risk via `DERIVED_FROM` or an equivalent explicit route.

A derivation cannot obtain warrant from a live dependency chain that materially depends on its own conclusion. Legitimate mutual induction/simultaneous proof is represented as one composite proof unit with its external premises and internal well-founded structure visible enough for Review.

A project-local claim without an adequate derivation/proof may remain a conjecture/hypothesis/proposed claim where allowed, but not an established theorem/result. Empirical evidence may warrant empirical claims or motivate conjectures but does not silently become deductive proof.

More generally, an established material claim `c` must have bounded **typed warrant closure** appropriate to its claim class. Conceptually:

\[
\operatorname{established}(c)
\Rightarrow
\operatorname{warrant\_closure}(c)
\text{ terminates in admissible roots and contains no self-supporting warrant cycle.}
\]

Admissible roots include, as applicable: foundational knowledge; explicit accepted axioms/assumptions whose conditional status is propagated; exact source-supported imported premises; admissible empirical evidence for empirical claims; and current project/external authority for normative contracts. A derived claim terminates through a valid derivation at such roots. No combination of `DERIVED_FROM`, hypothesis-discharge reasoning, citation/source support, evidence interpretation, or authority reference may bootstrap a claim by ultimately relying on that same claim as its warrant.

This is a bounded Review obligation over existing typed relations, not a new universal `warrant` database or untyped edge class.

## 12. Semantic-definition-use DAG and typed dependency ownership

For a composed authority family `D`, define the direct semantic-definition-use graph

\[
G_D^{\mathrm{def}}=(V_D,E_D^{\mathrm{def}}),
\]

where each node is a material semantic object/unit and

\[
(x,y)\in E_D^{\mathrm{def}}
\iff
\text{the canonical semantic statement of }y\text{ directly requires the canonical meaning of }x.
\]

The retained relation name is:

```text
subject USES_DEFINITION -> exact semantic object whose canonical declaration/definition/semantic statement is directly required to interpret the subject's own canonical semantic statement
```

Thus `USES_DEFINITION` is not limited to definition-to-definition edges. A theorem/result statement, assumption, algorithm, D3 rule, or D4 contract may use a definition even though the subject is not itself a definition. A project primitive may be a root with a canonical declaration rather than a constructive definition and can still be the endpoint of another unit's `USES_DEFINITION` edge.

A direct edge is material when varying the prerequisite's admissible meaning can change the subject's denotation, admissible domain, validity, governed contract, or accepted interpretation. An incidental mention that cannot change those semantics is not an edge merely because the same word appears.

`G_D^def` is a DAG. A legitimate recurrence/fixed-point/simultaneous definition/mutually recursive grammar is one composite semantic node, or equivalently its raw SCC is condensed into one node in the reviewable DAG.

Other relations stay typed and separate:

```text
DERIVED_FROM
ASSUMES
CONSTRAINED_BY
CONCRETIZES
EVIDENCES
EXECUTION_DEPENDS_ON
SUPERSEDES / REPLACES
```

Canonical ownership:

- `abstraction-and-concretization.md`: universal definition/prerequisite closure requirement;
- `evidence-evolution-and-dependencies.md`: `USES_DEFINITION` direction, durable endpoint identity, declared-scope completeness/absence semantics, and impact behavior;
- `scientific-technical-writing.md`: human-facing definition/dependency/import/alias/scope presentation;
- D1-D4 owners: their actual semantic declarations/definitions/statements/contracts and local consequences;
- `source/SEMANTIC_DEPENDENCIES.md`: subordinate derived current relationship view only.

For the declared canonical scope, direct `USES_DEFINITION` edges are materially complete under the criterion above. A derived partial view may be marked partial, but missing edges cannot prove independence. No repository-wide ontology/graph/database is required.

A material cross-document endpoint must be recoverable by the cheapest sufficient durable identity: semantic owner plus version/snapshot identity and a stable logical locator such as a definition/claim label, section/anchor, or exact path location. A repository-global ID registry is not required; an ambiguous floating locator is insufficient when ordinary document movement or version advancement could retarget the edge silently.

For object `z`, a complete bounded trace permits recovery of direct/transitive ancestors and descendants. Descendant closure is a candidate impact set, not proof that every descendant changes.

## 13. Cross-domain direction and authority boundaries

Definition/dependency traceability must preserve the D1->D2->D3->D4 abstraction direction rather than creating semantic back-edges merely for convenience.

Where materially applicable:

```text
D2 object --CONCRETIZES / USES_DEFINITION--> exact D1 object
D3 rule   --CONCRETIZES / CONSTRAINED_BY / USES_DEFINITION--> applicable D2/D1 object
D4 contract --CONCRETIZES / CONSTRAINED_BY / USES_DEFINITION--> applicable D3 and directly applicable upstream object
```

A lower-domain artifact may reference an upstream definition. An upstream definition must not acquire D2/D3/D4 implementation meaning merely because a lower-level mechanism exists. If a D1 object truly depends on a hardware/software fact because that fact is scientifically semantic or an external constraint entering D1, state that side constraint at D1 rather than importing a D4 implementation identifier as scientific meaning.

Cross-domain traceability is material and exact, not artificially complete. Do not invent edges where no semantic dependence exists.

## 14. Coherent composed-authority snapshots

A definition may be supplied by another file/owner rather than repeated, but the composed authority closure must be version-coherent.

A current task may rely on one accepted repository/protocol/project snapshot whose internal paths identify current owners; every link need not carry a redundant commit SHA when the whole snapshot identity already supplies coherence. Across repositories, releases, frozen versions, or independently moving owner families, bind enough immutable/version identity to prevent accidental mixed semantics.

Do not compose D1 from one semantic revision with D2/D3/D4 definitions accepted against an incompatible revision unless an explicit compatibility/adoption mapping establishes that composition. A floating current path cannot silently advance one prerequisite underneath an otherwise version-bound handoff.

When a referenced canonical owner materially advances, dependent current work either remains explicitly bound to the old supported version or performs bounded adoption/reconciliation. Mixed-version composition with unknown compatibility is `REVIEW_REQUIRED`.

## 15. Semantic object identity, aliases, equivalence, split/merge, retirement

A semantic object is not identified solely by symbol, abbreviation, heading, anchor, or definition ID.

- aliases/synonyms explicitly denote one canonical object;
- materially different meanings are distinct objects even if notation is conventional;
- materially identical meanings should not be duplicated under separately editable definitions merely because terminology differs;
- stable labels are locators, not proof of semantic continuity.

For aliases `a_i` of `x`:

\[
\operatorname{denotes}(a_i)=x.
\]

A representation-only change may preserve semantic identity only when equivalence is established over the governed regime. Let `R_1` and `R_2` be old/new representations under admissible context `\Gamma`. Treat them as semantically equivalent only when a competent independent reviewer can establish that they denote the same governed object/contract for all material admissible states in `\Gamma`, preserving assumptions, validity, units/dimensions, stochastic/error/equivalence semantics, and observable obligations. Bijective notation renaming or correctly defined unit/coordinate conversion may establish equivalence; visual similarity or stable labels do not.

If equivalence cannot be established where it matters, classify the change as semantic or `REVIEW_REQUIRED` rather than editorial by default.

Material definition mutation uses the owning D1-D4 acceptance process and bounded impact closure over `USES_DEFINITION`, `DERIVED_FROM`, `ASSUMES`, `CONCRETIZES`, evidence, documentation, and other material dependents.

When one object splits into several, several merge, or a current definition is retired, preserve explicit lineage/mapping and reconcile all current consumers. Retirement is allowed only when no supported current semantic/compatibility/evidence path materially depends on the retired definition and material history remains recoverable.

## 16. Progressive disclosure and runtime availability

`USES_DEFINITION` is a semantic dependency relation, **not an activation edge**. Ordinary Markdown links and dependency graphs still do not automatically load context.

When a role/agent is about to make a substantive inference whose correctness depends on semantic object `x`, the runtime condition is `context_available_C(x)`, not merely source discoverability. It is satisfied when:

- the canonical definition/declaration/semantic statement is already supplied in the governing runtime context; or
- the active router/concern owner follows a supported version-bound route and loads the canonical owner before that inference.

A discoverable-but-unloaded definition can be `source_available_D(x)` while remaining unavailable in the current runtime context. Progressive disclosure delays loading until the dependency becomes material; it does not authorize inference from an unloaded prerequisite.

Generated activation graphs remain diagnostic evidence. Do not convert every `USES_DEFINITION` edge into eager activation.

## 17. D1 local consequences

D1 Scientific Method Papers use axiomatic dependency ordering for governed scientific/mathematical meaning. Express scientific objects using the strongest practical formal representation: equations, mappings, distributions, estimands, observables, state spaces, constraints, predicates, boundary/initial conditions, assumptions, validity, uncertainty, and external adequacy semantics.

D1 must make recoverable without reverse-engineering D2/code:

- the scientific question/quantity/proposition;
- domains/types/units/dimensions/conventions;
- primitives/definitions/assumptions/derived vs observed status;
- model/validity/excluded regimes and uncertainty/limitations;
- specialized external prerequisites and source support;
- material semantic-use and derivation dependencies;
- dimensional and stochastic semantics when scientifically material.

Do not import lower-domain implementation detail upward unless it is genuinely scientific meaning or a directly governed external constraint entering D1.

## 18. D2 local consequences

D2 Numerical & Algorithmic Method Papers define the governed numerical method strongly enough that a competent reader can reconstruct it without D3/D4 reverse engineering. Use operators, update equations, recurrences, optimization problems, estimators, discretizations, distributions, stopping predicates, reductions, error measures, convergence/stability/conditioning definitions, precision policy, approximation envelopes, and stochastic dependence/convergence semantics as applicable.

Pseudocode complements mathematics when sequencing/control is material but does not replace semantics that determine numerical result. “Iterate until convergence” is inadequate when update map, norm/residual, tolerance, reduction/order, or stopping predicate is material.

D2 explicitly traces material D1 definitions/invariants it concretizes; it does not prescribe software decomposition/library/device identity unless numerically semantic.

## 19. D3 local consequences

D3 does not require decorative mathematics. Formalize architecture semantics where ambiguity reduction is material using ownership mappings, graph relations, state machines, cardinality/uniqueness constraints, temporal/order relations, concurrency invariants, resource inequalities, persistence/recovery relations, security/trust predicates, compatibility sets, typed interfaces, and pre/postconditions as appropriate.

Formalization must preserve D2/D1 semantics without freezing delegated D4 mechanics. D3 cannot redefine an upstream mathematical object merely for software convenience.

## 20. D4 local consequences

D4 Specifications use the strongest practical exact contract for governed behavior: types/schemas, domains/ranges, preconditions/postconditions, state transitions, units/shapes/order/precision, equivalence/tolerance relations, error/failure predicates, serialization grammars, persisted-state invariants, and authorization/security behavior.

For `f:X\to Y`, define material admissible inputs, output properties, failure/undefined behavior, and accepted equivalence/tolerance. Executable types/schemas/tests may realize/verify a contract but do not silently replace human-recoverable accepted specification when intent remains ambiguous.

Private implementation remains delegated unless current authority makes it contract.

## 21. Human-facing writing and background

`scientific-technical-writing.md` is the primary human-facing specialization of the universal rule. It SHALL implement:

- audience/foundational-envelope declaration proportionately;
- specialized imported prerequisite definitions and exact source binding;
- project primitive/local-binder discipline;
- formal-first definition followed by assumptions/validity/provenance/interpretation;
- distinction among definitions, axioms, assumptions, derived/empirical/approximate claims, normative contracts, examples, and explanations;
- definitional conservativity and separable claim-unit status;
- well-definedness, notation/relation/type/dimension/quantifier/stochastic rules;
- first-use abbreviation expansion and explicit aliases;
- source-level vs context-level availability distinction where agent/runtime reasoning is discussed;
- direct semantic-definition-use dependency exposure/routing;
- source lifecycle, external normative-force separation, and source-to-local transformation mapping;
- natural-language interpretation sufficient for intended reader.

Formalism does not excuse opacity. Mathematical notation that hides assumptions, validity, uncertainty, units, provenance, failure cases, authority force, or interpretation is lossy.

Current 6.4 canonical human-facing protocol/reference documents, including this current workplan where applicable, SHALL themselves satisfy the 6.4 rules proportionately. Frozen historical artifacts/workplans are not retroactively rewritten merely to match current style.

## 22. Documentation/evidence/dependency integration

- `documentation-maintenance.md`: route current-vs-history, canonical-source, composition, and impact obligations without duplicating formal-definition doctrine.
- `documentation-and-evidence.md`: preserve document authority/evidence communication boundaries.
- `evidence-evolution-and-dependencies.md`: canonical owner of `USES_DEFINITION` typed relation semantics, endpoint durability, completeness/absence semantics, source-binding-health interaction, and impact closure.
- `workflow-and-workplans.md`: version-bound/snapshot-complete handoff, 6.4 adoption, current-context loading obligations, and closeout.
- `testing-and-validation.md`: structural/static qualification only for mechanically decidable properties; independent semantic Review for mathematical/scientific adequacy; rendered/source integrity checks where they actually establish availability/readability rather than semantic truth.
- `source/SEMANTIC_DEPENDENCIES.md`: subordinate derived current view.

## 23. Protocol 6.4 adoption

Version-bound 6.3 work remains governed by 6.3. A newer installed/latest skill never silently reinterprets it.

When project/workplan explicitly adopts 6.4 over a bounded task scope:

1. identify materially relied-upon D1-D4 semantic objects/definitions/invariants;
2. confirm 6.4 source-availability, definition/provenance/validity/warrant closure or repair representation at the canonical owner without changing meaning;
3. preserve unrelated authority and historical artifacts;
4. if representation repair exposes multiple materially different meanings, stop editorial repair and reopen/challenge owning D1-D4 authority;
5. reconcile only materially dependent evidence/concretizations;
6. ensure composed owner versions are mutually compatible under Section 14;
7. ensure any agent/runtime making dependent inferences actually loads the required canonical owner under Section 16.

Adoption is neither a global rewrite mandate nor permission to rely indefinitely on ambiguous predecessor prose.

## 24. Repository implementation scope

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

Edit canonical source first; regenerate descendants. Do not independently hand-edit `dist/`, packages, or orchestrator generated snapshots.

Protocol 7 active parent/Revisions 1-4 remain semantically untouched during 6.4 implementation. Only after 6.4 acceptance add a narrow inheritance-only Protocol-7 revision.

## 25. Mechanization and presentation-integrity constraint

Prefer documentation convention plus bounded structural/static sensors over a persistent subsystem. Automated checks may honestly verify such properties as:

- required labels/fields under an explicitly structured canonical format;
- cross-reference, stable logical locator, and local dependency-ID resolution;
- duplicate IDs or unresolved labels;
- generated trace parity with canonical source;
- frozen prior-version byte stability;
- profile/schema/version consistency;
- obvious type/unit metadata consistency where explicitly machine-encoded;
- Markdown link/anchor integrity and LaTeX/delimiter/parser integrity where the repository has a supported checker/renderer;
- source-to-render parity and absence of broken/clipped/unreadable equations/tables on supported rendered documentation surfaces, using human/visual review where automation cannot decide presentation quality.

Automation SHALL NOT claim to prove arbitrary natural-language mathematics, scientific truth, theorem applicability, semantic equivalence, dimensional validity hidden in prose, literature support, audience expertise, complete dependency discovery, or whether an acronym is truly obvious to every intended reader. Human/independent Review remains responsible for those semantic questions.

A mechanically valid source file is not sufficient if a supported rendered/publication surface makes a material definition unreadable or changes its apparent notation. Conversely, no rendered-output ceremony is required for a source-only surface that has no supported renderer.

No theorem prover, ontology service, citation database, semantic hash registry, shadow definition store, or universal dependency graph is required by 6.4.

## 26. Protocol/profile/PEM version integration

- Set canonical candidate protocol version to `6.4.0` only during candidate integration.
- Generate distinct `ssdp-protocol-6.4` profile/resources without mutating frozen 6.3 bytes.
- Retain orchestration profile schema **v2** unless implementation genuinely changes the machine-readable profile contract. Protocol-version change alone is not a schema change.
- PEM schema 1 remains independent and unchanged unless separately justified.
- Do not churn PEM merely to mirror new protocol text; update it only when normal admission/update criteria are met.
- Keep 6.4 bootstrap/recovery self-reference-safe and intentionally distinct, following the proven 6.3 lifecycle.

## 27. PEM/HAS basis for this mature protocol revision

PEM remains activated as decision support because this is mature protocol rework. The Historical Applicability Set (HAS) for this design is:

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
    reason: Add new 6.4 versioned doctrine/profile/resources while frozen predecessor resources remain immutable and independently testable.
  - id: SP-001
    disposition: APPLICABLE
    reason: Repair canonical owners first, then regenerate deterministic descendants; never create package-side shadow authority.
```

These memory entries guide work only through their independent current-owner/evidence support. Perform normal closeout learning assessment; do not manufacture a PEM episode merely because files changed.

## 28. Preservation matrix

The following are explicit acceptance obligations in addition to all inherited Protocol 6.3 qualification:

| ID | Obligation |
| --- | --- |
| T64-01 | Preserve accepted 6.3 D1-D4 authority boundaries and recursive abstraction/concretization semantics. |
| T64-02 | Preserve 6.2 lossless-representation/progressive-disclosure capability through 6.3. |
| T64-03 | Preserve 6.3 PEM non-authority, conditional activation, HAS, evidence-binding, lineage, and counterevidence semantics. |
| T64-04 | Preserve evidence lifecycle and typed applicability/dependency distinctions. |
| T64-05 | Preserve Serious Challenge, independent Review, human gates, and bounded impact closure. |
| T64-06 | Preserve one detailed owner per generic rule and subordinate derived indexes/graphs. |
| T64-07 | Preserve current-vs-history separation; do not rewrite frozen historical authority into 6.4 style. |
| T64-08 | Preserve 5.16/6.0/6.1/6.2/6.3 frozen profile/resource bytes and exact historical bootstrap/recovery mappings. |
| T64-09 | Preserve canonical-source -> generated-package/profile/snapshot ownership. |
| T64-10 | Preserve Protocol-7 proposed/pre-cutover state and existing D3 semantics during 6.4 implementation. |
| T64-11 | Add formal-first doctrine without banning explanatory prose or forcing artificial equations. |
| T64-12 | Add strict definition-before-substantive-use for non-foundational governed objects. |
| T64-13 | Use corrected availability-basis + non-exclusive-role model; do not encode the superseded origin enum. |
| T64-14 | Require specialized external prerequisites to be precisely stated and source-bound. |
| T64-15 | Distinguish imported/base knowledge, project declarations/modifications, derivation, and novelty claims. |
| T64-16 | Require symbol/domain/unit/convention/assumption/validity closure at first formal occurrence when material. |
| T64-17 | Use a true acyclic direct semantic-definition-use DAG; valid recursive systems are composite nodes/SCC condensation. |
| T64-18 | Include definition/semantic-use descendants in bounded semantic impact analysis after material change. |
| T64-19 | Keep canonical semantic statements in D1-D4 owners; traceability artifacts remain subordinate. |
| T64-20 | Apply strongest practical mathematical/axiomatic form to D1/D2 while preserving delegation. |
| T64-21 | Apply formal relations/contracts to D3/D4 where ambiguity reduction is material without freezing private mechanics. |
| T64-22 | Preserve background terminology and first-use abbreviation rules. |
| T64-23 | Preserve primary/canonical-source preference and prohibit fabricated citation/provenance. |
| T64-24 | Keep proof/derivation, empirical evidence, executable tests, citation, and authority epistemically distinct. |
| T64-25 | Keep version-bound 6.3 work governed by 6.3; no silent reinterpretation. |
| T64-26 | Publish 6.4 bootstrap/recovery only through self-reference-safe lifecycle inherited from 6.3. |
| T64-27 | Generate distinct `ssdp-protocol-6.4` resources without mutating frozen 6.3. |
| T64-28 | Reconcile README/AGENTS/version/history/authority index from canonical semantics only. |
| T64-29 | After 6.4 acceptance, reconcile Protocol 7 inheritance only; do not authorize Protocol-7 D4 through that revision. |
| T64-30 | Preserve minimum justified mechanism; no ontology/shadow database/compliance wrapper absent demonstrated need. |
| T64-31 | Keep availability/source support orthogonal to semantic/epistemic role, novelty, and normative force. |
| T64-32 | Restrict `USES_DEFINITION` to direct semantic-meaning prerequisites; keep derivation, assumption, validity, evidence, execution, and concretization relations typed separately. |
| T64-33 | Represent legitimate recursive/simultaneous definitions as composite nodes so external trace remains acyclic. |
| T64-34 | Require exact typed cross-domain routes for material lower-domain semantics to upstream definitions/invariants. |
| T64-35 | Bind imported specialized knowledge to exact source/version/locator when variants matter and verify support. |
| T64-36 | Define source-to-local notation/unit/convention mapping when materially different. |
| T64-37 | Prevent foundational-scope laundering. |
| T64-38 | Keep semantic identity distinct from symbols/labels/anchors and map aliases explicitly. |
| T64-39 | Preserve one canonical semantic statement across secondary artifacts; exact supplied/version-bound routing satisfies source availability without duplication. |
| T64-40 | Apply bounded 6.4 adoption over materially depended-on authority, not global rewrite. |
| T64-41 | Keep Background import exposition subordinate to owning D1-D4 normative invocation. |
| T64-42 | Keep 6.4 discoverable through active authority routing while 6.3 remains accepted-current. |
| T64-43 | Treat foundational knowledge as an availability basis, not historical provenance; roles are non-exclusive. |
| T64-44 | Permit explicit project primitives only with recoverable signature/scope/axioms/constraints. |
| T64-45 | Treat formal binders/local declarations as scoped availability while referenced domains remain available. |
| T64-46 | Keep definitions distinct from axioms/premises/assumptions/empirical claims/normative contracts. |
| T64-47 | Require proportionate mathematical well-definedness. |
| T64-48 | Require imported/derived-result uses to discharge, assume, or propagate hypotheses/validity. |
| T64-49 | Preserve approximation/empirical/uncertainty status downstream. |
| T64-50 | Require material derivations to expose direct proof/premise dependencies and reject circular warrant. |
| T64-51 | Make `evidence-evolution-and-dependencies.md` canonical owner of `USES_DEFINITION` relation semantics. |
| T64-52 | Require material completeness of direct semantic-definition-use edges over declared canonical scope. |
| T64-53 | Treat material semantic-definition change as owner-level mutation; stable labels do not preserve applicability. |
| T64-54 | Treat source correction/retraction/incompatible revision as present-use binding/applicability event. |
| T64-55 | Keep profile schema v2 unless machine-readable profile contract actually changes. |
| T64-56 | Preserve PEM schema independence and avoid memory churn absent admitted learning. |
| T64-57 | Preserve axiomatic semantic ordering with flexible document layout. |
| T64-58 | Require proportionate coherence/non-vacuity of local axioms/assumptions where material. |
| T64-59 | Require type/dimensional consistency and explicit nontrivial transformations where they affect meaning. |
| T64-60 | Require quantifier order/scope and materially distinct relation/operator semantics to be explicit. |
| T64-61 | Require stochastic dependence/distribution/convergence semantics sufficient to distinguish material alternatives. |
| T64-62 | Prohibit lower-domain implementation details from becoming upstream semantic definitions without real upstream meaning/constraint. |
| T64-63 | Require version-coherent composed authority; unknown mixed-version compatibility is review-required. |
| T64-64 | Extend import provenance to empirical constants/data/reference values with material conditions/uncertainty/version. |
| T64-65 | Define a conservative semantic-equivalence criterion for editorial/notation changes; uncertainty defaults to review-required. |
| T64-66 | Preserve explicit semantic identity/lineage across split/merge/retirement and reconcile all current consumers. |
| T64-67 | Keep examples/counterexamples non-normative unless explicitly adopted by the real owner. |
| T64-68 | Keep `USES_DEFINITION` distinct from activation while requiring prerequisite owner loading before substantive inference. |
| T64-69 | Self-host the new doctrine on current 6.4 canonical protocol/reference documents proportionately. |
| T64-70 | Use this consolidated file as the sole current 6.4 implementation/review handoff; parent/Revisions 1-2 remain design-history evidence. |
| T64-71 | Define the core 6.4 terms `semantic object/unit`, canonical semantic statement, substantive semantic use, and material direct prerequisite before relying on them. |
| T64-72 | Separate source-level semantic availability from runtime-context availability and enforce both invariants at their proper layer. |
| T64-73 | Make `USES_DEFINITION` cover any governed semantic unit whose canonical statement directly requires another object's meaning, including primitive declarations, theorem/result statements, assumptions, algorithms, and contracts; do not restrict it to definition-to-definition edges. |
| T64-74 | Bind direct-edge materiality to a falsifiable semantic-change criterion and to the inherited governed scope; author convenience cannot narrow trace completeness. |
| T64-75 | Require explicit definitions intended as definitional extensions to be conservative over prior vocabulary; separate any additional existence/empirical/normative claim. |
| T64-76 | Require bounded typed warrant closure for established material claims and reject self-supporting cycles across mixed relation types. |
| T64-77 | Keep external semantic/evidentiary support separate from external normative force; binding standards/contracts/regulations govern only through their real authority route. |
| T64-78 | Preserve source-to-local transformation lineage for imported empirical data/reference values when preprocessing/selection/calibration/conversion materially changes meaning. |
| T64-79 | Make necessary/sufficient/biconditional direction explicit when it can change the conclusion or admissible set. |
| T64-80 | Give material cross-document semantic endpoints a durable owner + version/snapshot + logical locator sufficient to survive ordinary movement without a global registry. |
| T64-81 | If the strongest practical formal representation still leaves material alternative interpretations, preserve `REVIEW_REQUIRED`/Challenge rather than declaring prose adequate by convenience. |
| T64-82 | Self-host first-use expansion/background requirements in current 6.4 documents, including this workplan; non-obvious abbreviations must not remain unexplained. |
| T64-83 | Preserve source/render/link/formula integrity on supported documentation surfaces so a formally correct source cannot become semantically unavailable through broken presentation. |

## 29. Required qualification/counterfactual catalog

Qualification includes executable/static fixtures where honest and independent semantic Review where not mechanically decidable.

```text
Q64-01 specialized term used before definition/import -> FAIL
Q64-02 foundational common mathematical object used without redundant local definition -> PASS
Q64-03 specialized theorem cited but exact variant/assumptions ambiguous -> FAIL
Q64-04 specialized imported theorem precisely stated + source-bound -> PASS
Q64-05 project-declared estimator defined from available prerequisites -> PASS
Q64-06 project-local estimator silently presented as standard literature fact -> FAIL
Q64-07 definition depends on undefined specialized symbol -> FAIL
Q64-08 formal definition declares material domains/units/conventions -> PASS
Q64-09 same symbol silently changes material meaning/unit in one scope -> FAIL
Q64-10 harmless explicitly scoped local symbol reuse -> PASS
Q64-11 raw dependency cycle among independent definition nodes -> FAIL
Q64-12 valid recurrence/fixed-point represented as a well-posed composite node -> PASS
Q64-13 trace points to nonexistent canonical definition -> FAIL
Q64-14 derived trace matches canonical definitions -> PASS
Q64-15 derived trace disagrees with canonical owner -> FAIL
Q64-16 prose-only D1 definition admits two materially distinct formal interpretations -> FAIL
Q64-17 formal D1 definition plus interpretation -> PASS
Q64-18 “iterate until convergence” with materially unspecified predicate -> FAIL
Q64-19 D2 update + stop predicate + approximation/error semantics -> PASS
Q64-20 unambiguous D3 prose receives no decorative equation -> PASS
Q64-21 D3 unique-owner claim ambiguous about multiplicity -> FAIL
Q64-22 D4 operation omits material admissible-domain/failure semantics -> FAIL
Q64-23 executable schema exists but accepted human contract remains ambiguous -> FAIL
Q64-24 upstream definition changes while known dependent definition is unreconciled -> FAIL
Q64-25 unrelated sibling explicitly preserved after bounded impact analysis -> PASS
Q64-26 evidence dependency inferred solely from definition edge -> FAIL
Q64-27 frozen 6.3 resource/profile changes -> FAIL
Q64-28 generated package/profile/snapshot differs from canonical 6.4 source -> FAIL
Q64-29 6.4 public bootstrap is mutable/unqualified/self-naming current state -> FAIL
Q64-30 Protocol-7 existing D3 semantics changed by inheritance reconciliation alone -> FAIL
Q64-31 project-local theorem derived from imports is PROJECT_DECLARED + DERIVED_RESULT, not forced into false provenance exclusivity -> PASS
Q64-32 known method adaptation separates imported base from local modification -> PASS
Q64-33 specialized named method marked foundational solely because audience is expert -> FAIL
Q64-34 citation resolves but cited version/section does not support imported claim -> FAIL
Q64-35 imported formula translated to different notation/units without recoverable mapping -> FAIL
Q64-36 imported formula with explicit source-to-local mapping -> PASS
Q64-37 mutually recursive definitions exposed as unqualified independent-node cycle -> FAIL
Q64-38 mutual/fixed-point definition represented as well-posed composite node -> PASS
Q64-39 D3/D4 claims upstream preservation but lacks recoverable typed route -> FAIL
Q64-40 lower object has no material upstream dependence and creates no artificial edge -> PASS
Q64-41 same semantic object duplicated under separately editable aliases -> FAIL
Q64-42 secondary handoff reuses exact supplied/version-bound canonical definition without restating -> PASS
Q64-43 6.4 work relies on materially ambiguous predecessor definition without reconciliation/challenge -> FAIL
Q64-44 bounded adoption reconciles only materially depended-on authority -> PASS
Q64-45 Background defines imported theorem but normative owner silently depends on it without explicit invocation -> FAIL
Q64-46 project primitive introduced by signature + governing axioms before use -> PASS
Q64-47 project primitive appears with no signature/domain/axioms and later reasoning infers meaning -> FAIL
Q64-48 local bound variable introduced by binder with domain already available -> PASS
Q64-49 local symbol shadowing crosses ambiguous scope boundary -> FAIL
Q64-50 desired stability/uniqueness/accuracy asserted only by definition/name -> FAIL
Q64-51 property separately stated as assumption/theorem/empirical claim/contract with proper warrant -> PASS
Q64-52 single-valued argmin/implicit solution used without uniqueness/choice where multiple solutions possible -> FAIL
Q64-53 set-valued semantics, choice rule, or justified uniqueness closes same case -> PASS
Q64-54 piecewise definition overlaps materially without precedence or leaves treated-as-defined gap -> FAIL
Q64-55 partial mapping states admissible domain and governed undefined/failure behavior -> PASS
Q64-56 imported theorem correctly cited but material hypothesis false/undischarged at use -> FAIL
Q64-57 every material hypothesis established, assumed, or propagated -> PASS
Q64-58 bounded approximation later treated as exact unconditional identity -> FAIL
Q64-59 project-local theorem has circular live DERIVED_FROM warrant -> FAIL
Q64-60 mutual induction/simultaneous proof represented as well-founded composite proof unit -> PASS
Q64-61 complete trace omits known direct USES_DEFINITION prerequisite -> FAIL
Q64-62 partial diagnostic trace marked PARTIAL and not used to infer independence -> PASS
Q64-63 canonical meaning changes materially under same anchor while dependents/evidence remain accepted without review -> FAIL
Q64-64 proven semantically equivalent notation/explanation repair preserves identity -> PASS
Q64-65 imported source silently floats to materially different newer `latest` -> FAIL
Q64-66 source correction/retraction is surfaced and dependent applicability reviewed -> PASS
Q64-67 distinct 6.4 profile with unchanged machine contract retains schema v2 -> PASS
Q64-68 profile schema/fields change solely to mirror documentation doctrine -> FAIL
Q64-69 USES_DEFINITION appears in traces but canonical dependency owner never defines relation semantics -> FAIL
Q64-70 inconsistent/empty local axiom set produces substantive conclusion by undisclosed vacuity -> FAIL
Q64-71 physical equation has declared units but incompatible dimensions across equality -> FAIL
Q64-72 unit/nondimensionalization transformation is explicit and dimensionally consistent -> PASS
Q64-73 quantifier order can change conclusion but is left to prose inference -> FAIL
Q64-74 quantifiers/scopes are explicit and stable -> PASS
Q64-75 stochastic estimator says “random samples” while IID/correlation materially changes semantics and is unspecified -> FAIL
Q64-76 stochastic law/dependence/conditioning/convergence mode is defined sufficiently -> PASS
Q64-77 D1 scientific definition depends on a D4 helper/library identifier with no scientific/external meaning -> FAIL
Q64-78 D4 contract traces to upstream D1/D2/D3 semantics without redefining them -> PASS
Q64-79 composed authority silently mixes incompatible D1 and D2 revisions -> FAIL
Q64-80 composed authority is bound to one coherent accepted snapshot or explicit compatibility map -> PASS
Q64-81 stable label is used as proof that a material rewrite is semantically equivalent -> FAIL
Q64-82 bijective notation/unit transformation with same assumptions/validity/observables is independently established equivalent -> PASS
Q64-83 illustrative example silently becomes normative acceptance behavior -> FAIL
Q64-84 imported empirical constant/value lacks material reference conditions/uncertainty/version -> FAIL
Q64-85 current 6.4 canonical reference uses a specialized new concept normatively before defining/importing it -> FAIL
Q64-86 active reasoning depends on an unloaded canonical definition and proceeds merely because a link exists -> FAIL
Q64-87 router loads required owner before substantive dependent inference -> PASS
Q64-88 semantic object splits/merges but current consumers remain bound to ambiguous old identity -> FAIL
Q64-89 retired definition has no supported current consumers, material history/lineage remains recoverable -> PASS
Q64-90 implementation/reviewer must replay parent+multiple amendments because no single current 6.4 handoff exists -> FAIL
Q64-91 specialized core term such as `semantic object` is used normatively before its meaning is established -> FAIL
Q64-92 object is source-available by route but agent performs dependent inference without loading the exact canonical meaning into runtime context -> FAIL
Q64-93 router loads the version-bound canonical owner before dependent inference, preserving source/context availability distinction -> PASS
Q64-94 project primitive has no constructive definition but its canonical declaration is traced as a root used by downstream semantic units -> PASS
Q64-95 theorem/assumption/algorithm/contract uses a definition materially but is omitted because trace implementation only records definition-to-definition edges -> FAIL
Q64-96 author labels a direct prerequisite “immaterial” even though changing its admissible meaning changes the subject's denotation/domain/validity/contract -> FAIL
Q64-97 explicit “definition” adds a new property of prior vocabulary without exposing the additional assumption/result/contract -> FAIL
Q64-98 conservative definitional extension plus separately classified/warranted additional proposition -> PASS
Q64-99 claim appears supported only through a mixed circular chain of derivation, hypothesis discharge, citation/evidence interpretation, or authority references that ultimately depends on the same claim -> FAIL
Q64-100 material established claim has bounded typed warrant closure terminating in admissible independent roots -> PASS
Q64-101 scientific literature citation is treated as a binding project contract solely because it is authoritative literature -> FAIL
Q64-102 applicable external standard/contract/regulation is explicitly bound through the real governing authority while its source citation separately states its content -> PASS
Q64-103 imported dataset/reference value is materially filtered/transformed/calibrated locally but only raw-source provenance is recorded -> FAIL
Q64-104 source identity plus material source-to-local transformation/selection/calibration mapping is recoverable -> PASS
Q64-105 necessary and sufficient conditions are reversed or left ambiguous and the distinction changes admissibility/conclusion -> FAIL
Q64-106 implication/biconditional direction is explicit and matches the governed claim -> PASS
Q64-107 material cross-document semantic dependency uses a floating/ambiguous locator that can retarget silently under ordinary movement/version change -> FAIL
Q64-108 strongest practical formalization still admits materially different interpretations but document declares closure instead of `REVIEW_REQUIRED`/Challenge -> FAIL
Q64-109 unresolved formalization boundary is made explicit and routed as `REVIEW_REQUIRED`/Challenge rather than hidden -> PASS
Q64-110 current 6.4 human-facing document uses a non-obvious abbreviation such as IID/SCC/HAS before first-use expansion -> FAIL
Q64-111 supported rendered/source surface breaks or alters a material formula/link/anchor so the canonical meaning cannot be recovered reliably -> FAIL
Q64-112 supported source/render/link checks pass and independent inspection finds material equations/tables/definitions readable and notation-preserving -> PASS
```

Semantic cases such as Q64-16, 33-35, 39, 43, 50, 56, 59, 63-66, 70-89, and 91-112 rely on independent Review or deliberately bounded objective fixtures where lexical/static checking cannot honestly decide the claim.

## 30. Independent falsification passes

Independent assembled-candidate Review executes all of:

### F64-A — Alternate-formalization challenge
Attempt to construct materially different formal meanings that satisfy representative D1-D4 prose.

### F64-B — Undefined-root / hidden-prerequisite challenge
Trace representative ancestors to foundational knowledge, exact external imports, or explicit project declarations; challenge hidden specialized roots and foundational-scope laundering.

### F64-C — Provenance / epistemic-laundering challenge
Search for imported claims presented as original, project modifications presented as standard, definitions used to assert truth, empirical evidence used as proof, citations used as authority mutation, and examples/tests used to define intent.

### F64-D — Typed-dependency / impact challenge
Mutate representative definitions and verify correct typed descendant review while unaffected siblings remain preserved; reject universal untyped dependency collapse.

### F64-E — Formalism-overreach challenge
Find equations/registries/labels that add complexity without reducing ambiguity or freeze delegated mechanics.

### F64-F — Lossless inheritance challenge
Re-run inherited 6.3 preservation/routing/PEM/package/profile/frozen-resource/Challenge/bootstrap/recovery oracles sufficient to prove no doctrine loss.

### F64-G — Classification / identity challenge
Construct project-local+derived, imported+assumed, independently derived but non-novel, aliased, and symbol-reused cases; reject false exclusivity/label identity.

### F64-H — Import / adoption / cross-domain challenge
Falsify source support, source-to-local mapping, foundational-envelope claims, normative adoption, typed D1-D4 routes, and bounded 6.4 migration.

### F64-I — Primitive / definition / well-definedness challenge
Find undeclared primitives, hidden scope assumptions, truth claims smuggled into definitions, missing existence/uniqueness/choice semantics, ambiguous piecewise/branch behavior, partial-as-total mappings, and vacuous local axiom sets.

### F64-J — Applicability / derivation challenge
Reconstruct hypotheses/validity/approximation/proof dependencies; attempt out-of-regime use, dropped assumptions, exactness promotion, and circular derivation.

### F64-K — Trace completeness / evolution / schema challenge
Omit definition edges from allegedly complete traces, mutate meaning under stable labels, float source versions, or bump profile schema without machine-contract change.

### F64-L — Type / quantifier / stochastic / layer-direction challenge
Attempt dimensionally invalid but well-typeset equations, quantifier swaps, underspecified stochastic dependence/convergence, or upward D1/D2 dependence on incidental D3/D4 mechanisms.

### F64-M — Composition / self-hosting / routing / consolidation challenge
Attempt incompatible mixed-version authority composition, semantic-equivalence laundering, example-to-authority promotion, unloaded-prerequisite reasoning under progressive disclosure, definition split/merge/retirement drift, or violation of 6.4 by its own current canonical documentation. Confirm this consolidated workplan alone reconstructs the current 6.4 implementation contract.

### F64-N — Core-term / availability / semantic-use challenge
Attempt to use undefined core 6.4 terminology, conflate source availability with runtime loading, omit primitive/theorem/assumption/algorithm/contract uses from `USES_DEFINITION`, or manipulate “materiality” to hide a meaning-changing direct prerequisite.

### F64-O — Warrant / authority-force / import-transformation challenge
Attempt mixed-relation circular warrant, citation-to-authority laundering, external-binding ambiguity, or use of transformed empirical inputs whose local semantic lineage cannot be reconstructed from their source.

### F64-P — Definitional-conservativity / logical-direction / presentation-integrity challenge
Attempt to introduce new truth through a definition, reverse necessary/sufficient conditions, close materially ambiguous under-formalized prose, leave non-obvious abbreviations undefined, or render/break a source-valid formal statement so the intended reader cannot recover its canonical meaning.

## 31. Implementation stages

### Stage A — Canonical doctrine

1. Amend `abstraction-and-concretization.md` with the core semantic-unit terminology, source-level semantic availability, definition/provenance closure, primitive roots, direct-prerequisite materiality, and derived-trace subordination.
2. Rewrite `scientific-technical-writing.md` around the consolidated formal-first/axiomatic doctrine while preserving readability/background/progressive disclosure, including definitional conservativity, external-support/authority-force separation, and first-use abbreviation discipline.
3. Add D1/D2 mathematical consequences and D3/D4 formal-contract consequences without domain leakage.
4. Mandatorily amend `evidence-evolution-and-dependencies.md` to own widened `USES_DEFINITION` direction, durable endpoints, bounded completeness/absence, source-binding/evolution interaction, and impact closure.
5. Reconcile documentation/workflow/testing/versioning owners only for their local consequences, including source-vs-context availability and bounded warrant closure.
6. Reconcile `source/SEMANTIC_DEPENDENCIES.md` as a derived current view.
7. Apply the new doctrine to current 6.4 canonical protocol/reference prose and this current workplan proportionately; frozen predecessors remain untouched.

### Stage B — Versioned profile/source integration

1. Set candidate `source/PROTOCOL_VERSION` to `6.4.0` at the appropriate candidate stage.
2. Generate distinct `ssdp-protocol-6.4` profile/snapshot/package resources through existing generators.
3. Keep profile schema v2 unless a separately justified machine-contract change is genuinely required.
4. Keep all prior frozen resources byte-identical.
5. Update current manifests/README/AGENTS/history/current authority surfaces consistently without yet claiming accepted-current/recovery.

### Stage C — Qualification

1. Implement Q64-01..Q64-112 with semantic review fixtures and machine checks only where honest.
2. Re-run complete inherited repository regression and applicable 6.3 qualification/preservation oracles.
3. Independently build/validate packages and committed distribution parity.
4. Verify orchestrator profile/snapshot/Core acceptance when affected.
5. Verify prior frozen trees byte-identically.
6. Execute self-hosting review over current 6.4 canonical references and this workplan.
7. Execute supported Markdown/link/anchor/LaTeX/source-to-render integrity checks and human presentation inspection where a supported rendered surface exists; do not claim these prove semantic correctness.

### Stage D — Semantic candidate and bootstrap

1. Freeze immutable 6.4 semantic candidate only after semantic-source repairs/qualification.
2. Construct/qualify an already-existing self-reference-safe public-source bootstrap that does not need to self-name its SHA.
3. Publish exact bootstrap identity only from a later descendant.
4. Re-run exact-ref remote source/package/profile/routing realization after publication.
5. Preserve failed bootstrap attempts as historical evidence only.

### Stage E — Independent assembled-candidate Review

Reviewer reconstructs from accepted Protocol 6.3 plus this consolidated handoff, not implementer conclusions or superseded amendment text. Review T64-01..T64-83, Q64-01..Q64-112, F64-A..F64-P, frozen resources, source/context availability, semantic-use/definition/type/validity/warrant/trace semantics, external support/authority force, generated/profile/schema surface, exact-ref bootstrap, self-hosting, presentation integrity, and compatibility.

Any material semantic mutation after reviewed candidate reopens affected qualification/Review.

### Stage F — Recovery and closeout

Only after independent PASS:

1. select an already-existing immutable recovery target containing reviewed candidate/evidence/Review through ancestry;
2. publish `6.4.0 -> <recovery SHA>` from a later descendant;
3. regenerate mapping-bearing descendants and rerun recovery/bootstrap-distinction/package/profile/Core acceptance;
4. reconcile semantic history, authority index, README/AGENTS and accepted-current release text;
5. add narrow Protocol-7 6.4 inheritance reconciliation without changing/re-accepting its D3 architecture or authorizing D4;
6. perform PEM closeout-learning assessment;
7. archive this consolidated workplan and the superseded design-review workplan artifacts only after current semantics/lifecycle state reside in canonical owners.

## 32. Non-goals

Protocol 6.4 does not:

- require every sentence to be mathematical notation;
- require re-proving foundational mathematics/science;
- classify all graduate-level knowledge as foundational;
- replace natural-language explanation/motivation/interpretation/rationale/limitations;
- require theorem proving, symbolic-math checking, global ontology, citation database, semantic hash registry, or universal dependency database;
- claim automated proof of scientific/mathematical correctness, warrant sufficiency, or semantic equivalence;
- turn literature/background/evidence/examples into project authority;
- deny the normative force of genuinely applicable external contracts/standards/regulations merely because they are external; their force remains owned by the actual governing constraint;
- change existing projects' scientific/numerical meaning merely to improve representation;
- retroactively rewrite frozen historical protocol artifacts;
- change PEM schema solely for definition traceability;
- mutate Protocol-7 D3/control-plane semantics or authorize its implementation/cutover;
- force a full project documentation rewrite on bounded 6.4 adoption;
- force formalization beyond the owning domain's abstraction boundary;
- permit materially ambiguous semantics to be declared closed merely because a stronger formalization is inconvenient.

## 33. Reopen / Challenge triggers

Reopen the earliest affected owner when:

- strict traceability requires materially changing D1-D4 semantics rather than representing them;
- foundational/imported/project-declared boundaries remain materially ambiguous;
- source-level semantic availability cannot be established from a coherent canonical owner/source;
- a proposed formal definition is not well-defined or requires unresolved existence/uniqueness/consistency assumptions that matter to outcome;
- theorem/result hypotheses cannot be discharged/assumed/propagated coherently;
- an established claim's warrant is circular, unavailable, or incompatible with its claim class;
- typed semantic-definition-use/derivation/validity relations conflict with existing semantic-dependency authority;
- cross-domain definition dependencies create an unjustified upstream back-edge;
- current composed authority cannot be made version-coherent without semantic migration;
- external support and normative-force routing conflict or cannot be resolved;
- imported data transformation prevents recoverable source-to-local semantic identity;
- formal representation freezes delegated lower-level mechanisms;
- the strongest practical formalization still leaves materially different interpretations without an accepted uncertainty/Challenge treatment;
- 6.4 cannot preserve frozen 6.3 capability/profile/recovery contract;
- a validator would need to adjudicate scientific truth rather than structural well-formedness;
- a profile/schema change is actually required, in which case its machine-contract owner must explicitly justify it;
- Protocol 7 cannot inherit accepted 6.4 without genuine D3 architecture mutation, which belongs to Protocol-7 D3 reopen.

## 34. Fourth-review gap closure

The fourth review added these closures beyond the third-review state:

1. dimensional/type consistency;
2. relation/operator semantics;
3. quantifier order;
4. stochastic closure;
5. layer-direction protection;
6. coherent authority composition;
7. empirical imports;
8. semantic-equivalence criterion;
9. split/merge/retirement;
10. example status;
11. progressive-disclosure reconciliation;
12. self-hosting;
13. workplan consolidation.

## 35. Fifth-review gap closure

The fifth review found and closed fourteen additional gaps in the single consolidated contract:

1. **Core-term self-definition:** `semantic object/unit`, canonical semantic statement, substantive semantic use, and material direct prerequisite are now defined before normative reuse.
2. **Two availability layers:** source/document semantic availability is distinct from runtime-context loading; authoring and agent inference have separate explicit invariants.
3. **Trace subject completeness:** `USES_DEFINITION` now covers governed semantic units generally, not only definition-to-definition dependencies.
4. **Primitive-root semantics:** canonical declarations can be dependency roots even when no constructive definition exists.
5. **Materiality criterion:** direct-edge omission is no longer author-discretionary when changing the prerequisite can change governed meaning.
6. **Mixed-relation warrant closure:** established claims cannot acquire warrant through a circular combination of derivation, hypothesis discharge, citation/evidence interpretation, or authority reference.
7. **Definitional conservativity:** a true definitional extension cannot create new truth about prior vocabulary; additional claims are separated and warranted.
8. **Support vs authority:** imported knowledge/evidence is distinct from genuinely binding external constraints, whose force comes from the real governing authority.
9. **Empirical transformation lineage:** transformed/filtered/calibrated imported data preserve a reconstructible source-to-local semantic mapping.
10. **Logical direction:** necessary, sufficient, and biconditional conditions are explicit when material.
11. **Durable semantic locators:** cross-document endpoints bind owner + version/snapshot + stable logical location without requiring a global ID registry.
12. **No under-formalization escape hatch:** if strongest practical formalization still leaves material alternatives, closure becomes `REVIEW_REQUIRED`/Challenge rather than assumed adequacy.
13. **Self-hosting abbreviations/background:** Scientific Software Development Protocol, D1-D4, Project Engineering Memory, Historical Applicability Set, directed acyclic graph, strongly connected component, and independent and identically distributed are defined/expanded before non-obvious shorthand is relied upon.
14. **Presentation integrity:** supported source/render/link/formula failures that make canonical meaning unreadable are now explicit qualification failures without pretending rendering proves mathematical truth.

**FIFTH DESIGN REVIEW VERDICT: PASS — blockers 0; Serious Challenges 0.**
