---
kind: abstraction-concretization-change-plan
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: active
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: pass
implementation_handoff: authorized
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
branch_point: 0928accd337a13f864b292ed81c36372828cfb4c
accepted_parent_protocol: 6.3.0
accepted_parent_recovery: 9f353097fab36e325a325f1c2f9d9cec32e86177
accepted_parent_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
---

# SSDP 6.4 — Axiomatic Formal Definition and Semantic Traceability

## Current disposition

**DESIGN REVIEW: PASS.** Protocol 6.4 is a proposed backward-compatible doctrine/representation strengthening over accepted Scientific Software Development Protocol (SSDP) 6.3. No Serious Challenge to accepted 6.3 remains. Implementation is authorized only against this workplan and the accepted 6.3 parent doctrine; Protocol 6.3 remains accepted-current until the complete 6.4 qualification, independent Review, immutable bootstrap/recovery publication, generated reconciliation, and lifecycle closeout finish.

The protected outcome is not “more equations.” It is that a competent reader or downstream agent can reconstruct each governed technical concept with minimum interpretive freedom, identify every specialized prerequisite and its provenance, and trace changes through the exact definitions that depend on it without inventing meaning from prose, code, convention, or hidden chat.

## 1. Problem and earliest affected owner

Accepted Protocol 6.3 already requires semantic completeness, precision, explicit definitions, mathematical formulation in D1/D2, background terminology, provenance, and bounded dependency/impact closure. Those safeguards are necessary but insufficient: they still permit a technically polished authority document to introduce a specialized term in prose, use a symbol before its exact domain/meaning is fixed, cite a literature family without selecting the exact imported result, or describe an algorithm naturally without exposing the formal relation that distinguishes materially different interpretations.

That is an **abstraction-adequacy defect in representation doctrine**. If prose `P` admits materially different formal interpretations `F_1` and `F_2`, then descendants can satisfy the words while implementing different semantics. Formally, for intended abstraction `A`, ambiguity can enlarge the apparent admissible concretization set:

\[
\widetilde{\mathcal K}(A) \supsetneq \mathcal K(A),
\qquad
\mathcal K(A)=\{K\mid K\models I(A)\}.
\]

The earliest generic owner is the universal Lossless Representation Rule in `source/shared/references/abstraction-and-concretization.md`, specialized by `scientific-technical-writing.md` and the D1-D4 owners. This change must therefore be made once at the universal representation owner and propagated as local consequences; it must not be implemented as an independent glossary subsystem, compliance database, or documentation-only convention disconnected from D1-D4 authority.

## 2. Parent authority, preservation, and compatibility

Implementation SHALL preserve every accepted Protocol 6.3 semantic, lifecycle, evidence, routing, project-learning, compatibility, qualification, and historical-recovery capability unless this workplan explicitly strengthens its representation. In particular:

- D1-D4 remain the only semantic authority domains; 6.4 creates no D5 and no documentation authority plane.
- Accepted authority still defines what must be true; evidence, literature, tests, documentation, and Project Engineering Memory (PEM) cannot silently mint project authority.
- Concretization fidelity and abstraction adequacy remain distinct.
- Lossless representation still precedes compactness; importance weighting cannot hide mandatory lower-salience obligations.
- Progressive disclosure, one detailed owner per generic rule, explicit typed routing, cold-path discoverability, and derived-view subordination remain intact.
- Evidence specification -> realization -> observation -> assessment remains intact.
- Serious Challenge, human adjudication, bounded impact closure, Review/Verification/Stabilization, and workplan semantics remain intact.
- Protocol 6.3 PEM remains project-local, evidence-backed, conditionally activated, non-authoritative decision support under schema 1 unless a separately justified schema change is required; 6.4 does not require one.
- Frozen Protocol 5.16/6.0/6.1/6.2/6.3 resources, profiles, recovery mappings, public bootstraps, and historical qualification records remain immutable.
- Protocol 6.3 public bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11` and recovery `9f353097fab36e325a325f1c2f9d9cec32e86177` remain distinct and valid for version-bound 6.3 work.
- Protocol 7 remains proposed/pre-cutover and must not acquire 6.4 semantics by editing its existing D3 design. After 6.4 acceptance, add a narrow inheritance-only Protocol-7 reconciliation, analogous to the existing 6.2/6.3 inheritance revisions.

Protocol 6.4 is a **minor** version: it strengthens how already-governed semantics must be defined, imported, derived, and traced; it does not intentionally change the D1-D4 lifecycle or existing project meaning.

## 3. Governing 6.4 invariant

For every governed semantic object `x` whose meaning is not safely included in the declared foundational knowledge of the intended competent reader:

\[
\boxed{
\operatorname{use}(x)
\Rightarrow
\operatorname{available}(x)
}
\]

where availability means that, before the use that depends on its meaning, `x` is either explicitly defined in the current composed authority or explicitly imported from an identified external source with the exact semantics required by the document.

Every non-foundational object SHALL have one provenance class:

\[
\operatorname{origin}(x)
\in
\{\mathrm{IMPORTED},\mathrm{DERIVED},\mathrm{ORIGINAL}\},
\]

while foundational objects belong to the document's declared reader-knowledge envelope:

\[
\operatorname{origin}(x)=\mathrm{FOUNDATIONAL}.
\]

A definition such as

\[
y := F(x_1,\ldots,x_n)
\]

is well formed only if each dependency is already available:

\[
\forall i,\quad \operatorname{available}(x_i).
\]

The normative presentation preference is:

```text
formal definition / exact structured contract
  -> domain, assumptions, conventions, validity
  -> provenance / derivation
  -> explanatory natural language
```

Natural language remains essential for motivation, interpretation, rationale, limitations, and human comprehension. It MUST NOT be the sole normative definition when multiple materially different formal interpretations remain possible and a stronger practical formal representation exists.

## 4. Foundational knowledge boundary

6.4 SHALL NOT require documents to re-teach ordinary mathematics, physics, statistics, computer science, or other prerequisite material reasonably common to the explicitly declared competent audience. However, “graduate level” is not a blanket exemption: curricula differ, and a specialized domain result cannot be treated as common merely to avoid defining or citing it.

The document or composed document family SHALL establish an audience-relative **foundational knowledge envelope**. It may implicitly include, as appropriate, ordinary logic/sets/numbers, standard calculus/linear algebra/probability, conventional mathematical notation, and broadly standard scientific foundations for the named audience. It MAY rely on universally standard axioms/theorems without local proof when their exact variant is unambiguous.

Use the conservative predicate:

\[
\operatorname{uncertain\_foundational}(x)
\Rightarrow
\operatorname{define\_or\_import}(x).
\]

A foundational exemption concerns definition/provenance overhead only. Material conventions still must be stated when variants can change meaning: units, sign, frame, coordinate system, indexing/tensor order, normalization, estimator/sample semantics, precision/tolerance, boundary/initial conditions, and similar choices.

## 5. Specialized imported knowledge

A literature-established specialized concept, theorem, model, estimator, algorithm, physical law/approximation, numerical result, architectural formalism, or software standard is `IMPORTED` when the project does not derive it independently.

Before a normative project definition depends on such an object, the human-facing authority SHALL provide, normally in `Background` / `Background and terminology`:

1. a precise local statement sufficient to determine the exact imported meaning or theorem variant used;
2. symbols, domains, assumptions, conventions, and validity restrictions material to that use;
3. an authoritative external reference, preferring primary literature or a canonical standard/reference where appropriate;
4. any project-specific restriction or interpretation separated from the imported result.

Citation alone is insufficient when the citation leaves the reader to guess which variant is intended. Conversely, copying a theorem statement does not create project authority: the external result remains external knowledge used by the project formulation.

For specialized `x`:

\[
\operatorname{specialized}(x)
\Rightarrow
\left[
\operatorname{external\_reference}(x)
\lor
\operatorname{explicit\_original\_derivation}(x)
\right].
\]

If an original derivation depends on specialized external premises `r_i`, every `r_i` independently satisfies the import rule.

## 6. Original and derived project semantics

A project-specific concept, observable, estimator, theorem, algorithm, invariant, state model, interface contract, or adaptation is `ORIGINAL` or `DERIVED` and SHALL be identified as such rather than being written as if universally established.

For an original/derived object:

\[
x := F(x_1,\ldots,x_n),
\]

its dependency set, assumptions, validity, and inferential status SHALL be recoverable. Distinguish at least when material:

- definition;
- axiom or accepted premise;
- assumption;
- imported theorem/result;
- derived proposition/lemma/theorem;
- empirical observation/relationship;
- approximation;
- heuristic;
- normative design invariant or contract.

Proof/derivation and empirical evidence are not interchangeable. A numerical test can support an implementation or empirical claim but does not prove a mathematical theorem unless the theorem's accepted proof method makes that execution dispositive. A citation can justify an imported premise but does not prove a project-specific modification.

For adaptations of known methods, make the decomposition explicit:

```text
imported established method
+ project-local modification / restriction
= current project method
```

## 7. Definition-before-use and symbol discipline

For each material semantic object `x`, substantive use SHALL occur only after definition/import availability in semantic dependency order:

\[
\operatorname{available}(x) \prec \operatorname{use}(x).
\]

A brief forward mention is allowed only when no normative inference depends on the undeclared meaning and the definition route is explicit. A symbol MUST NOT acquire normative meaning merely from surrounding prose, code, a later equation, or common local habit.

At first formal introduction, define as applicable:

- object name and symbol;
- mathematical domain/type/set/shape/unit;
- operator/function/predicate semantics;
- indices and ordering;
- parameters and controlled variables;
- assumptions/constraints;
- validity/admissibility regime;
- normalization/sign/frame/boundary conventions;
- exact vs approximate/empirical/heuristic status;
- provenance class and external source or derivation route.

A symbol may be reused in a distinct local scope only when the scope boundary is unmistakable and cannot change interpretation. Material notation collisions across composed authority SHALL be repaired rather than left to reader inference.

## 8. Definition dependency DAG and strict traceability

The user's requested “traceability tree” is implemented as a **definition dependency directed acyclic graph (DAG)** because definitions may have multiple prerequisites and multiple descendants.

For authority document/family `D`, define

\[
G_D=(V_D,E_D),
\]

where each `v \in V_D` is a materially governed semantic object and

\[
(x,y)\in E_D \iff x \prec y
\]

means the definition, derivation, interpretation, or validity of `y` materially depends on `x`.

Ordinarily `G_D` MUST be acyclic. Recursive/simultaneous definitions are permitted only when their semantics are explicitly supplied by a mathematically valid construction such as a fixed point, recurrence with base case, mutually recursive grammar, or simultaneous system.

For every governed object `z`, a reviewer SHALL be able to recover:

\[
\operatorname{Ancestors}(z)=\{x\mid x\prec^{+}z\}
\]

and determine where each non-foundational ancestor is defined/imported, its provenance, assumptions, validity, and source/derivation. Conversely, a changed definition `x` exposes a candidate semantic impact set

\[
\operatorname{Descendants}(x)=\{y\mid x\prec^{+}y\}.
\]

This graph is an impact-analysis aid and traceability representation, **not a second semantic authority store**. The canonical definitions remain in their D1-D4 owners. Any table/index/graph extracted from them is derived and subordinate. Do not create a universal ontology database, registry daemon, shadow schema, or separate semantic truth store merely to satisfy traceability.

### 8.1 Required traceability surface

For human-facing D1/D2 authority and for D3/D4 authority containing specialized formal objects, provide an explicit, reviewable definition/dependency surface. The minimum acceptable representation is one of:

- formal definition blocks with stable section/definition labels plus explicit prerequisite references;
- a compact `Definitions and dependencies` table mapping semantic object -> definition site -> provenance -> direct prerequisites;
- an equivalent mechanically or visually inspectable representation generated from the canonical definitions.

A derived global/section DAG MAY be generated when useful, but the underlying direct prerequisite relation must remain recoverable even without the visualization.

Do not require a heavyweight registry for trivial documents. The strict requirement is semantic traceability, not a particular storage technology.

## 9. D1 local consequence

D1 Scientific Method Papers SHALL use axiomatic dependency ordering for governed scientific/mathematical meaning. Scientific objects should be expressed by the strongest practical formal representation: equations, mappings, distributions, estimands, observables, constraints, predicates, state spaces, boundary/initial conditions, and explicit assumptions.

A competent reader SHALL be able to determine from D1, without reverse-engineering D2/code:

- what quantity/proposition is scientifically meant;
- the domains/units/conventions of its objects;
- what is assumed versus derived versus observed;
- validity/excluded regimes and model uncertainty/limitations;
- which specialized external results are imported and from where;
- how each project-specific scientific concept depends on earlier definitions.

An observable described only as “average error” is inadequate when the actual contract depends on loss choice, weighting, population, sampling, exclusion, unit, or normalization that could change the conclusion.

## 10. D2 local consequence

D2 Numerical & Algorithmic Method Papers SHALL define the numerical method strongly enough that a competent reader can reconstruct the governed algorithm without reverse-engineering D3/D4. Use, as applicable, operators, update equations, recurrences, optimization problems, estimators, discretizations, distributions, stopping predicates, reductions, error measures, convergence/stability/conditioning definitions, precision policy, and approximation envelopes.

Pseudocode MAY complement mathematics when sequencing/control is material, but it does not replace mathematical semantics that determine the result. “Iterate until convergence” is insufficient where the update map or convergence predicate materially matters.

Every D2 object depending on D1 SHALL trace to the exact D1 definition/invariant it concretizes; every new specialized numerical object SHALL be defined/imported before use.

## 11. D3 local consequence

6.4 does not require artificial mathematics for ordinary software prose. D3 SHALL formalize specialized architecture semantics when formalization reduces material ambiguity, using suitable structures such as ownership mappings, graph relations, state machines, cardinality/uniqueness constraints, temporal/order relations, concurrency invariants, resource inequalities, persistence/recovery relations, security/trust predicates, and compatibility sets.

For example, when unique authoritative ownership is normative, a relation such as

\[
\operatorname{owner}: S\to C,
\qquad
\forall s\in S,\ |\operatorname{owner}(s)|=1
\]

is preferable to prose that can be read as advisory or shared ownership.

Do not freeze delegated D4 mechanics merely to create formalism. Formal precision must follow the existing D3 authority boundary.

## 12. D4 local consequence

D4 Specifications SHALL use the strongest practical exact contract for governed behavior: types/schemas, domains/ranges, preconditions/postconditions, state-transition relations, units/shapes/order, equivalence/tolerance relations, error/failure predicates, serialization grammars, persisted-state invariants, and authorization/security behavior.

For governed operation `f:X\to Y`, specify material admissible input subset, output properties, failure behavior, and any accepted equivalence relation. Private implementation detail remains delegated unless current authority makes it part of the contract.

Executable schemas/types/tests MAY realize or verify a formal contract but do not silently replace the human-recoverable accepted specification when the executable artifact alone leaves intent ambiguous.

## 13. Documentation and background integration

`scientific-technical-writing.md` SHALL become the primary human-facing specialization of the universal axiomatic rule. Its current background/terminology and abbreviation requirements remain, strengthened as follows:

- Background contains specialized imported prerequisites needed to understand the normative formulation.
- Project-original semantics remain at their D1-D4 owner, not in background merely because definitions are convenient there.
- Define/cite established specialized knowledge before normative reuse.
- Formal definition precedes explanatory prose when formalization is practical and ambiguity-reducing.
- Natural-language explanation remains required where needed for the intended reader; mathematical notation is not permission to become opaque.
- LaTeX/formal notation must render correctly and every nonstandard symbol must resolve to a definition.
- Current documents explain present truth; historical frozen artifacts are not retroactively rewritten into 6.4 style.

`documentation-maintenance.md` and `documentation-and-evidence.md` SHALL route the new doctrine without creating duplicate detailed owners. `source/SEMANTIC_DEPENDENCIES.md` and routing/documentation indexes SHALL be reconciled only as needed to preserve discoverability and canonical ownership.

## 14. Universal Lossless Representation integration

Amend the universal rule so that semantic precision includes **definition closure and provenance closure**. A representation is not lossless when a material term can only be understood by guessing an undeclared specialized convention or when a definition depends on an unresolved semantic root.

For governed object `x`, require the material prerequisite closure to terminate in:

```text
FOUNDATIONAL reader knowledge
or
IMPORTED externally sourced specialized knowledge
or
explicit ORIGINAL/DERIVED project semantics whose own prerequisites resolve recursively.
```

Formalism does not excuse omission. A compact equation that hides assumptions, validity, units, uncertainty, provenance, or exceptional cases is lossy.

The target property is:

\[
\boxed{
\forall x\in V_D,\quad
\operatorname{meaning}(x),\operatorname{provenance}(x),
\text{ and material prerequisite closure are recoverable.}
}
\]

## 15. Evidence, Review, and impact closure

Review of D1-D4 authority SHALL add bounded falsification of definition adequacy:

1. Can two competent readers construct materially different formal interpretations that both satisfy the text?
2. Is any specialized semantic object used before definition/import availability?
3. Does any imported theorem/result omit its exact variant, assumptions, or authoritative reference?
4. Is external knowledge presented as if project-derived, or project invention presented as established external truth?
5. Does any symbol change meaning, scope, unit, normalization, or status silently?
6. Does the dependency graph contain an unresolved root or unjustified cycle?
7. If a definition changes, were materially dependent definitions/evidence/concretizations considered through descendant closure?

Discovery of such a defect routes to the earliest semantic owner of the defective definition. Documentation may repair exposition only when the underlying D1-D4 owners already agree; it cannot choose new scientific/numerical/architectural truth editorially.

Definition-dependency tracing complements but does not replace the existing evidence/dependency model. A semantic definition edge is not automatically an evidence-applicability edge; both must remain typed according to their real meaning.

## 16. Scope of repository implementation

Implementation SHALL reconcile at least these canonical current owners/surfaces, plus any newly discovered materially dependent surface:

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
source/shared/references/evidence-evolution-and-dependencies.md   (routing/typed-edge interaction only if needed)
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

Do not edit generated `dist/` or orchestrator snapshots independently. Edit canonical source then regenerate.

Protocol 7 active parent/Revisions 1-4 remain semantically untouched during 6.4 implementation. Only after 6.4 qualifies and is accepted SHALL a new inheritance-only Protocol-7 revision update the pre-cutover inherited baseline and 6.4 doctrine, without silently re-accepting or mutating Protocol-7 D3 architecture.

## 17. Definition-traceability implementation constraint

The implementation SHOULD prefer a documentation convention plus validation/static sensors over a new persistent subsystem. If executable checks are added, they SHALL verify stable mechanically decidable properties without claiming to prove scientific truth, for example:

- required definition/dependency fields or labels exist where the repository's own canonical formal-definition format declares them;
- direct definition references resolve;
- obvious duplicate definition IDs or unresolved local dependency labels fail;
- generated traceability views equal their canonical source representation;
- frozen historical resources remain byte-identical.

Do not create a parser that pretends arbitrary natural-language mathematics can be proven complete. Human Review remains responsible for semantic adequacy, provenance correctness, and whether the chosen formalization actually eliminates material ambiguity.

## 18. Project Engineering Memory / HAS for this revision

This is mature protocol rework, so PEM is activated as decision support. Design intake uses the exact current accepted repository state at branch point and its contained PEM publication:

```yaml
pem_basis:
  accepted_project_state: 0928accd337a13f864b292ed81c36372828cfb4c
  accepted_pem: 0928accd337a13f864b292ed81c36372828cfb4c:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: NONE
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: Protocol 6.4 must not publish an immutable public bootstrap until the complete repaired 6.4 source/route/package semantics exist and qualify at that exact snapshot.
  - id: PC-001
    disposition: APPLICABLE
    reason: 6.4 adds new versioned doctrine/profile/resources while all prior frozen protocol/profile/recovery resources remain immutable and independently testable.
  - id: SP-001
    disposition: APPLICABLE
    reason: Canonical-owner-first repair followed by deterministic regeneration is directly relevant to updating shared doctrine and derived distributions/snapshots without package-side shadow authority.
```

PEM does not make these obligations authoritative by itself. FF-001 and SP-001 guide implementation from evidence; PC-001 is mandatory only because its cited accepted protocol-versioning owner independently requires frozen prior-version preservation.

Before closeout, reconcile any material 6.4 learning through the normal PEM closeout process; do not create occurrences/applications merely because files changed.

## 19. Preservation matrix

The following 6.4 preservation obligations are explicit acceptance items in addition to inherited Protocol 6.3 qualification:

| ID | Obligation |
| --- | --- |
| T64-01 | Preserve all accepted 6.3 D1-D4 authority boundaries and recursive abstraction/concretization semantics. |
| T64-02 | Preserve all 6.2 lossless-representation/progressive-disclosure capability through 6.3. |
| T64-03 | Preserve 6.3 PEM non-authority, conditional activation, HAS, evidence-binding, lineage, and counterevidence semantics. |
| T64-04 | Preserve evidence lifecycle and typed applicability/dependency distinctions; definition edges do not silently become evidence edges. |
| T64-05 | Preserve Serious Challenge, independent Review, human gates, and bounded impact closure. |
| T64-06 | Preserve one detailed owner per generic rule and keep derived definition indexes non-authoritative. |
| T64-07 | Preserve current-vs-history separation; do not rewrite frozen historical authority into 6.4 style. |
| T64-08 | Preserve 5.16/6.0/6.1/6.2/6.3 frozen profile/resource bytes and exact historical recovery/bootstrap mappings. |
| T64-09 | Preserve canonical-source -> generated-package/profile/snapshot ownership; no hand-edited derivative truth. |
| T64-10 | Preserve Protocol-7 proposed/pre-cutover state and existing D3 semantics during 6.4 implementation. |
| T64-11 | Add formal-first definition doctrine without banning explanatory prose or forcing artificial equations where structured formal contracts are stronger. |
| T64-12 | Add strict definition-before-use for non-foundational governed semantic objects. |
| T64-13 | Add foundational/imported/derived/original provenance classification with conservative foundational boundary. |
| T64-14 | Require specialized literature-established prerequisites to be locally identified/defined sufficiently and externally cited. |
| T64-15 | Require original/project-specific definitions or derivations to be explicitly distinguishable from imported knowledge. |
| T64-16 | Require symbol/domain/unit/convention/assumption/validity closure at first formal occurrence when material. |
| T64-17 | Require recoverable direct definition dependencies and acyclic definition DAG absent explicit valid recursive construction. |
| T64-18 | Require definition descendant closure to participate in semantic impact analysis after material definition change. |
| T64-19 | Keep canonical definitions in D1-D4 owners; any definition graph/table/index is subordinate derived representation. |
| T64-20 | Apply strongest mathematical/axiomatic form to D1 and D2 while respecting D1/D2 delegation boundaries. |
| T64-21 | Apply formal relations/state/contracts to D3/D4 where ambiguity reduction is material without freezing delegated mechanics. |
| T64-22 | Preserve audience-relative background requirements and first-use abbreviation expansion. |
| T64-23 | Preserve primary/canonical external-source preference and prohibition on fabricated citation/provenance. |
| T64-24 | Keep formal proof/derivation, empirical evidence, executable tests, and external citation epistemically distinct. |
| T64-25 | Keep version-bound 6.3 work interpretable under 6.3; 6.4 never silently reinterprets old active work. |
| T64-26 | Publish 6.4 bootstrap/recovery only through self-reference-safe lifecycle inherited from 6.3. |
| T64-27 | Generate a distinct `ssdp-protocol-6.4` profile/resource set without mutating frozen 6.3. |
| T64-28 | Reconcile README/AGENTS/version/history/authority index only from accepted source semantics and preserve exact current/fallback identities. |
| T64-29 | After 6.4 acceptance, reconcile Protocol 7 inheritance only; do not use that reconciliation to authorize Protocol-7 D4. |
| T64-30 | Preserve minimum justified mechanism: no ontology service, shadow definition database, or compliance wrapper absent independently demonstrated need. |

## 20. Required qualification and counterfactuals

Create focused 6.4 qualification cases with both valid and invalid examples. Exact test numbering may extend during implementation, but the acceptance surface SHALL discriminate at least:

```text
Q64-01 specialized term used before definition/import -> FAIL
Q64-02 foundational common mathematical object used without local redefinition -> PASS
Q64-03 specialized theorem cited but exact variant/assumptions ambiguous -> FAIL
Q64-04 specialized imported theorem precisely stated + cited -> PASS
Q64-05 project-original estimator defined from available prerequisites -> PASS
Q64-06 project-original estimator silently presented as standard literature fact -> FAIL
Q64-07 definition depends on undefined specialized symbol -> FAIL
Q64-08 first formal definition declares domains/units/conventions needed for interpretation -> PASS
Q64-09 same symbol silently changes material meaning/unit in one normative scope -> FAIL
Q64-10 harmless explicitly scoped local symbol reuse -> PASS
Q64-11 direct dependency cycle with no valid recursive construction -> FAIL
Q64-12 explicit recurrence/fixed-point/simultaneous system with valid base/semantics -> PASS
Q64-13 definition table/DAG points to nonexistent canonical definition -> FAIL
Q64-14 derived traceability view matches canonical definitions -> PASS
Q64-15 derived traceability view disagrees with canonical owner -> FAIL
Q64-16 prose-only D1 definition admits two materially distinct equations -> FAIL
Q64-17 formal D1 definition plus explanatory prose -> PASS
Q64-18 “iterate until convergence” with materially unspecified predicate -> FAIL
Q64-19 D2 update rule + stopping predicate + approximation/error semantics -> PASS
Q64-20 D3 prose is already unambiguous and no artificial equation is added -> PASS
Q64-21 D3 unique-owner claim remains ambiguous about multiplicity -> FAIL
Q64-22 D4 governed operation omits material admissible-domain/failure semantics -> FAIL
Q64-23 executable schema exists but human accepted contract remains ambiguous -> FAIL
Q64-24 change to upstream definition leaves known dependent definition unreconciled -> FAIL
Q64-25 unrelated definition sibling preserved after bounded impact analysis -> PASS
Q64-26 evidence dependency incorrectly inferred solely from definition edge -> FAIL
Q64-27 frozen 6.3 resource/profile changed -> FAIL
Q64-28 generated package/profile/snapshot differs from canonical 6.4 source -> FAIL
Q64-29 6.4 public bootstrap equals an unqualified or self-naming mutable/current state -> FAIL
Q64-30 Protocol-7 existing D3 semantics changed by inheritance reconciliation alone -> FAIL
```

Where a requirement is semantic rather than mechanically decidable, qualification SHALL use review fixtures/counterexamples and explicit human/independent Review rather than a fake parser oracle.

## 21. Falsification passes

Independent Review SHALL perform at least these bounded falsification passes over the assembled candidate:

### F64-A — Ambiguity / alternate-formalization challenge

Attempt to construct two materially different formal interpretations from each representative D1/D2/D3/D4 definition family. If both satisfy the words, the owning definition is inadequate.

### F64-B — Undefined-root / hidden-prerequisite challenge

Trace representative definition ancestors until each terminates in declared foundational knowledge, a precise imported source, or explicit project-local definition/derivation. Search for specialized undeclared roots, hidden conventions, and symbol inheritance from code/history/chat.

### F64-C — Provenance / epistemic-laundering challenge

Attempt to find imported specialized claims presented as original, project-local modifications presented as standard, empirical evidence used as mathematical proof, citations used as authority mutation, or tests used to define intent.

### F64-D — Dependency / impact-closure challenge

Mutate representative upstream definitions in fixtures/counterfactuals and verify that materially dependent descendants become review candidates while unaffected siblings remain valid. Confirm definition dependencies do not collapse into a universal untyped dependency graph.

### F64-E — Formalism-overreach challenge

Attempt to identify cases where the implementation added equations/registries/labels that increase complexity but do not reduce ambiguity, or accidentally froze delegated D3/D4 mechanics. Such over-formalization is a defect.

### F64-F — Lossless inheritance challenge

Re-run inherited Protocol 6.3 preservation, routing, PEM, package/profile, frozen-resource, Challenge, and exact-ref bootstrap/recovery oracles sufficient to prove 6.4 did not lose earlier doctrine.

## 22. Implementation stages

### Stage A — Canonical doctrine

1. Update universal representation owner with definition/provenance closure and derived-DAG subordination.
2. Rewrite `scientific-technical-writing.md` around axiomatic/formal-first exposition while preserving background/readability doctrine.
3. Add D1/D2 strict mathematical consequences and D3/D4 formal-contract consequences at their current owners.
4. Reconcile documentation/evidence/maintenance/workflow/versioning owners only where their local semantics change.
5. Update current routing/dependency references without duplicating the detailed generic rule.

### Stage B — Versioned protocol/profile integration

1. Set canonical target version to `6.4.0` only on the candidate branch at the appropriate candidate stage.
2. Add distinct 6.4 profile/snapshot/package resources through existing generators.
3. Keep all frozen prior-version resources byte-identical.
4. Update manifests/README/AGENTS/history/current authority surfaces consistently.
5. Do not yet claim 6.4 accepted-current or publish recovery.

### Stage C — Qualification/oracles

1. Add focused Q64 counterfactual fixtures/tests/static sensors.
2. Re-run complete inherited repository regression and applicable 6.3 qualification.
3. Build/validate canonical packages independently and verify committed distribution parity.
4. Verify orchestrator snapshot/profile/Core acceptance when affected.
5. Verify frozen prior-version trees byte-identically.

### Stage D — Semantic candidate and bootstrap lifecycle

1. Freeze an immutable 6.4 semantic candidate after all semantic-source repairs.
2. Construct/qualify an already-existing self-reference-safe public-source bootstrap whose contents satisfy the 6.4 fallback contract without requiring its own SHA.
3. Publish that exact bootstrap identity only from a later descendant.
4. Re-run exact-ref remote source/package/profile/routing realization after publication.
5. Preserve all failed bootstrap attempts as historical evidence, never current fallback.

### Stage E — Independent assembled-candidate Review

Independent reviewer reconstructs 6.4 from accepted 6.3 rather than inheriting implementer conclusions. Review T64-01..T64-30, Q64, F64-A..F64-F, frozen resources, exact-ref bootstrap, package/profile integrity, definition traceability, false formalization, and compatibility.

Any material semantic mutation after the reviewed candidate reopens affected qualification/Review.

### Stage F — Recovery, generated reconciliation, and closeout

Only after independent PASS:

1. select an already-existing immutable recovery target containing the reviewed candidate/evidence/Review through ancestry;
2. publish `6.4.0 -> <recovery SHA>` only from a later descendant;
3. regenerate mapping-bearing descendants and rerun recovery/bootstrap-distinction/package/profile/Core acceptance;
4. reconcile semantic history, authority index, current README/AGENTS and accepted-current release text;
5. add the narrow Protocol-7 6.4 inheritance reconciliation without altering its D3 architecture or authorizing D4;
6. perform PEM closeout learning assessment;
7. archive this workplan only after current semantics and lifecycle state are represented in canonical owners.

## 23. Non-goals

Protocol 6.4 does **not**:

- require every sentence to be an equation;
- require proofs of standard foundational mathematics/science;
- require all graduate-level knowledge to be treated as foundational;
- replace natural-language explanation, motivation, interpretation, rationale, or limitations;
- create a global semantic ontology, theorem prover, symbolic-math checker, citation database, or registry service;
- attempt automatic proof that arbitrary prose/math is scientifically correct;
- turn literature into project authority;
- change scientific/numerical meaning of existing projects merely by changing documentation style;
- rewrite frozen historical protocol documents;
- change PEM schema solely for definition traceability;
- mutate Protocol-7 D3/control-plane semantics;
- authorize Protocol-7 implementation/cutover.

## 24. Reopen triggers

Reopen the earliest affected owner if implementation discovers that:

- strict definition traceability cannot be achieved without materially changing D1-D4 authority semantics;
- the foundational/imported boundary admits a material ambiguity not resolvable by audience declaration;
- the definition DAG conflicts with existing typed semantic/evidence dependency semantics rather than complementing them;
- a proposed formal representation freezes lower-level machinery that accepted authority intentionally delegates;
- 6.4 cannot preserve a frozen 6.3 capability/profile/recovery contract;
- qualification reveals that a generic validator would need to adjudicate scientific truth rather than structural well-formedness;
- Protocol 7 cannot inherit accepted 6.4 without a genuine D3 architecture change, in which case that change belongs to the existing Protocol-7 reopen, not this workplan.

## 25. Integrated design review and gap closure

The revision was reviewed against accepted 6.3 universal representation, D1/D2 formulation, D3/D4 authority boundaries, documentation maintenance, evidence/dependency typing, workflow/impact closure, protocol versioning, PEM, frozen-resource preservation, generated-source ownership, and the active Protocol-7 handoff.

Gaps closed during review:

1. **Tree vs DAG:** traceability is a DAG so multi-parent definitions and shared descendants do not force duplication.
2. **Registry risk:** canonical definitions stay in D1-D4; traceability indexes/graphs are derived, preventing a shadow authority store.
3. **Over-formalization risk:** D1/D2 receive strongest mathematical requirements; D3/D4 use formal relations/contracts only where they reduce ambiguity and do not freeze delegated mechanics.
4. **Foundational-scope laundering:** “graduate level” is not an unrestricted exemption; the reader foundation is explicit, audience-relative, and conservative under uncertainty.
5. **Citation laundering:** specialized imported knowledge requires exact local semantics plus source; citations neither replace definition nor create project authority.
6. **Originality/provenance drift:** imported, derived, and original semantics are explicitly distinguished; project adaptations separate borrowed method from local modification.
7. **Proof/evidence conflation:** proof/derivation, empirical evidence, executable tests, and citation remain epistemically distinct.
8. **Dependency-type collapse:** definition edges remain distinct from evidence/applicability/authority dependencies.
9. **Impact-closure gap:** changed definitions expose descendant semantic review candidates while unaffected siblings remain preservable.
10. **Historical mutation risk:** frozen historical resources remain byte-identical; 6.4 applies to current/newly refactored authority, not retroactive historical rewriting.
11. **Bootstrap/recovery recurrence:** inherited 6.3 self-reference-safe bootstrap/recovery lifecycle is explicit and reinforced by applicable PEM history.
12. **Protocol-7 interference:** 6.4 implementation does not edit active Protocol-7 D3 semantics; inheritance reconciliation occurs only after 6.4 acceptance.
13. **Mechanized false confidence:** automated checks are restricted to structurally decidable properties; semantic adequacy remains subject to independent falsification.
14. **Natural-language regression:** formal-first does not eliminate explanation; prose follows and interprets formal definitions instead of silently defining them.
15. **Cross-document hidden prerequisites:** composed authority must make shared prerequisite/definition routes explicit and supplied; hidden chat/history cannot satisfy availability.

**Design verdict: PASS — blockers 0; Serious Challenges 0.**
