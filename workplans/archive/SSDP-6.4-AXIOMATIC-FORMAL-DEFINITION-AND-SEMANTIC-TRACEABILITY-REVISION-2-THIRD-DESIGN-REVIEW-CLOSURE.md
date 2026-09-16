---
kind: abstraction-concretization-change-plan-amendment
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-REVISION-2-THIRD-DESIGN-REVIEW-CLOSURE
amends_workplan: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY
extends_amendment: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-REVISION-1-SECOND-DESIGN-REVIEW-CLOSURE
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: active
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: pass-after-third-review
implementation_handoff: authorized
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
reviewed_composed_head: ba23575048c7f36adcc851aa7571b65f0a5416b1
accepted_parent_protocol: 6.3.0
accepted_parent_recovery: 9f353097fab36e325a325f1c2f9d9cec32e86177
accepted_parent_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
---

# Protocol 6.4 Revision 2 — Third Design Review Closure

## Current disposition and precedence

**THIRD DESIGN REVIEW: PASS AFTER GAP CLOSURE.** No Serious Challenge to accepted Protocol 6.3 or to the protected Protocol 6.4 outcome remains.

Implementation and independent Review SHALL read the parent, Revision 1, and this Revision 2 as one composed handoff. This revision has latest precedence only for the availability/classification model, primitive-object and local-binding semantics, axiom/definition discipline, well-definedness, assumption/validity discharge, derivation traceability, `USES_DEFINITION` ownership/completeness, semantic-definition evolution, external-source lifecycle, and profile-schema rules below. Every earlier obligation not explicitly changed remains binding.

The third review deliberately tried to construct documents that look formally rigorous yet remain semantically underdetermined. It found that the parent plus Revision 1 could still pass a notation-rich document whose primitive objects were never declared, whose `argmin` was not single-valued, whose imported theorem was applied outside its assumptions, whose conclusion was smuggled into a “definition,” or whose supposedly complete trace omitted a direct prerequisite. Those are blockers for a strict axiomatic formulation doctrine and are closed here.

## 1. Third-review findings and closure

### R64-11 — `FOUNDATIONAL` is an availability basis, not literal source provenance; roles are not mutually exclusive

Revision 1 correctly separated provenance from inferential status, but its notation still called `FOUNDATIONAL` a source-provenance class and represented semantic role as a single-valued function. Both are too strong. Common calculus or linear algebra is assumed available to the reader; that does not claim anything about the historical provenance of those concepts. Likewise, one object may simultaneously be a normative definition and an approximation, or an imported relation and a local premise.

**Closure:** Section 2 replaces the three-way “provenance” label with an **availability basis** and makes semantic roles a set of orthogonal tags. Historical/literature provenance and novelty remain separate claims.

### R64-12 — Explicit primitive objects and local binders were missing

An axiomatic formulation cannot require every object to be constructively defined. Formal systems legitimately start from primitive sorts, spaces, states, observables, operators, or symbols whose admissible meaning is fixed by a signature plus axioms/constraints. Conversely, local bound variables such as `x` in `for all x in X` are introduced by the binder itself and should not require an earlier global definition.

**Closure:** Section 3 defines project-declared primitive objects and scope-local binders as valid availability roots while prohibiting hidden semantics.

### R64-13 — Definition, axiom, premise, and assumption could still be laundered into one another

The composed plan distinguished roles but did not state the strongest anti-laundering rule: writing `:=` does not make an empirical proposition, algorithmic guarantee, or desired conclusion true. A definition stipulates meaning; an axiom/premise/assumption asserts a proposition under a declared status; a derived result requires derivation/proof/evidence appropriate to its claim class.

**Closure:** Section 4 defines these boundaries and makes “definition laundering” a qualification and falsification target.

### R64-14 — Formal syntax did not yet imply mathematical well-definedness

A formula can be fully typeset yet undefined: a single-valued `argmin` may have several minimizers, a square root may need a branch convention, a piecewise definition may overlap without precedence, a partial function may omit its domain of definition, or an asserted fixed point may not exist.

**Closure:** Section 5 requires proportionate well-definedness: domains/codomains, quantifier/scope, totality/partiality, branch/selection rules, piecewise coverage/overlap, and existence/uniqueness or explicit set-valued/choice semantics when material.

### R64-15 — Imported/derived results lacked explicit use-site assumption and validity discharge

Exact source binding does not prevent misuse. A theorem can be cited perfectly and still be applied when its hypotheses are false; an approximation can be introduced with a validity envelope and then silently treated as exact downstream.

**Closure:** Section 6 requires every material use of an imported or derived result to establish, explicitly assume, or propagate its hypotheses/validity conditions. Unknown satisfaction is `REVIEW_REQUIRED`; violated conditions invalidate the use.

### R64-16 — Derivation/proof dependencies were typed but not required to be well-founded

Revision 1 separated `DERIVED_FROM` from `USES_DEFINITION`, but a project-local theorem could still cite another result that eventually depends on the theorem itself.

**Closure:** Section 7 requires recoverable direct premise/result dependencies for material project-local derivations and rejects circular support. Legitimate mutual induction/simultaneous proof is represented as one explicit composite proof unit, analogous to composite recursive definitions.

### R64-17 — `USES_DEFINITION` had no canonical typed-relation owner

Revision 1 introduced `USES_DEFINITION`, while accepted Protocol 6.3 assigns generic semantic dependency typing and impact semantics to `evidence-evolution-and-dependencies.md`. Leaving the new relation only in the writing/workplan doctrine would create duplicate or orphan semantics.

**Closure:** Section 8 makes `evidence-evolution-and-dependencies.md` the canonical owner of the `USES_DEFINITION` relation semantics and impact behavior. `scientific-technical-writing.md` owns its human-facing presentation; the universal kernel owns the requirement for definition closure. `source/SEMANTIC_DEPENDENCIES.md` remains a derived current view.

### R64-18 — Traceability completeness and absence semantics were underspecified

A “definition DAG” that omits known direct prerequisites is not useful for impact closure. Protocol 6.3 already states that absence of a dependency edge proves independence only when the mapped scope was reviewed complete.

**Closure:** Section 8 requires the canonical 6.4 definition trace for its declared scope to be materially complete over direct `USES_DEFINITION` edges. A deliberately partial derived view must say so and cannot use absence as proof of independence.

### R64-19 — Material definition mutation could hide behind a stable label

Revision 1 correctly separated semantic objects from labels, but did not explicitly say what happens when the canonical meaning of an object changes while its anchor/name remains the same.

**Closure:** Section 9 makes a material definition change an owning-authority mutation with bounded descendant/evidence impact and semantic-history obligations. A stable symbol/anchor cannot preserve old evidence applicability by itself. If incompatible old/new meanings must coexist, distinguish them by version/scope/object identity rather than one ambiguous current definition.

### R64-20 — External-source correction/retraction/version drift was not closed

Exact version binding prevents silent “latest” drift, but the plan did not state what to do when a bound source is corrected, retracted, superseded, or discovered not to support the imported claim.

**Closure:** Section 10 treats this as a source-support/binding-health event: current dependent use becomes `REVIEW_REQUIRED` or challenged as appropriate; the project does not silently switch editions. A meaning-changing source update is a semantic input change and receives bounded impact closure.

### R64-21 — Profile schema independence needed an explicit 6.4 decision

Accepted Protocol 6.3 keeps orchestration profile schema v2 because the machine profile contract did not change. The parent correctly requires a new `ssdp-protocol-6.4` profile but could be read as permission to bump schema merely because doctrine changed.

**Closure:** Section 11 freezes schema v2 for the intended 6.4 doctrine-only change unless implementation actually changes the machine-readable profile contract. Any such contract change is separately justified and reviewed; it cannot be hidden inside definition-traceability work.

### R64-22 — Axiomatic ordering itself was still implicit

The plan required definition-before-use but did not give a complete semantic ordering for primitive declarations, imported prerequisites, axioms/assumptions, definitions, and derived results.

**Closure:** Section 12 defines the semantic order while preserving flexible document layout and progressive disclosure.

## 2. Corrected availability and semantic-role model

Revision 1's `provenance(x) in {FOUNDATIONAL, IMPORTED, PROJECT_LOCAL}` notation is superseded in terminology by the following **availability basis**:

\[
\operatorname{availability\_basis}(x)
\in
\{
\mathrm{FOUNDATIONAL\_ASSUMED},
\mathrm{EXTERNAL\_IMPORTED},
\mathrm{PROJECT\_DECLARED}
\}.
\]

This classifies how the current composed authority makes `x` semantically available. It is not a claim about historical discovery or intellectual priority.

Semantic/epistemic roles are non-exclusive:

\[
\operatorname{roles}(x)\subseteq
\{
\mathrm{PRIMITIVE},
\mathrm{DEFINITION},
\mathrm{AXIOM},
\mathrm{PREMISE},
\mathrm{ASSUMPTION},
\mathrm{DERIVED\_RESULT},
\mathrm{EMPIRICAL\_RELATION},
\mathrm{APPROXIMATION},
\mathrm{HEURISTIC},
\mathrm{NORMATIVE\_CONTRACT}
\}.
\]

The set is illustrative and extensible only for real distinctions. Do not force a universal ontology.

Novelty/priority remains a separate optional claim such as `BORROWED`, `ADAPTED`, `INDEPENDENTLY_DERIVED`, or `ORIGINAL_CONTRIBUTION`, with literature/evidence appropriate to that claim. Historical provenance may be mixed and need not be forced into one enum.

Examples:

- common vector-space notation used by the intended audience: `FOUNDATIONAL_ASSUMED`;
- a published specialized theorem used as a model premise: `EXTERNAL_IMPORTED` + `PREMISE`;
- a project-defined error metric: `PROJECT_DECLARED` + `DEFINITION` + possibly `NORMATIVE_CONTRACT`;
- a project-local approximation formula: `PROJECT_DECLARED` + `DEFINITION` + `APPROXIMATION`;
- a theorem derived locally from imported lemmas: `PROJECT_DECLARED` + `DERIVED_RESULT`, with imported dependencies and a separate novelty claim if one is made.

## 3. Primitive declarations, local binders, and scope-aware availability

A non-foundational semantic root need not always be constructively defined. It may be an explicit project primitive when the formulation declares enough formal signature and constraints to prevent hidden meaning.

Examples include:

\[
X \text{ is a declared state space},
\qquad
s\in X,
\qquad
\mathcal O:X\to\mathbb R.
\]

For a project-declared primitive, state as applicable:

- name/symbol and semantic role;
- sort/type/domain/codomain/shape/unit;
- scope;
- axioms/constraints/relations that characterize admissible use;
- whether existence/non-emptiness is assumed, constructed, or established;
- validity regime and interpretation when material.

A primitive declaration is not permission for prose-implied semantics. Anything beyond its signature and explicit axioms/constraints remains unavailable.

Definition/prerequisite closure may therefore terminate in:

```text
FOUNDATIONAL_ASSUMED reader knowledge
EXTERNAL_IMPORTED specialized knowledge with exact source support
PROJECT_DECLARED primitive with explicit signature/axioms
PROJECT_DECLARED definition whose own prerequisites close recursively
```

### Local binders

A scope-local variable may become available at its binder/declaration rather than through an earlier global definition, for example:

\[
\forall x\in X,\quad P(x),
\qquad
\sum_{i=1}^{N} a_i.
\]

Here `x` and `i` are locally bound; `X`, `P`, `N`, and `a_i` must already be available as required. Local shadowing is permitted only when scope is unmistakable and cannot create a material interpretation collision.

`available(x)` is therefore context- and scope-relative. A version-bound supplied canonical definition, explicit import, project declaration, or local binder can establish availability; hidden chat/history cannot.

## 4. Definition, axiom, premise, assumption, and claim discipline

Use the following semantic distinction:

- **definition** — stipulates the meaning of a symbol/object/term relative to already available objects; it does not by notation alone establish empirical truth, existence, optimality, convergence, stability, safety, or adequacy;
- **axiom** — explicitly accepted proposition of the formal system, not derived inside that system;
- **premise** — proposition imported or otherwise accepted for a particular argument;
- **assumption** — conditional premise adopted for a bounded model/method/regime and therefore part of validity/interpretation;
- **derived result** — proposition established from stated premises/definitions by a recoverable derivation/proof appropriate to the claim;
- **empirical relation** — observation/model relation supported by empirical evidence, not transformed into a theorem by notation;
- **normative contract** — requirement adopted by project/external authority; normative force comes from that owner, not mathematical proof.

A definition must not **launder a proposition**. For example, writing

\[
\text{“stable method”} := \text{“the method whose errors remain bounded”}
\]

may define a term, but it does not prove that a particular method is stable. Likewise, defining a selected solution as “the unique optimum” does not establish uniqueness.

If a purported definition materially embeds an existence, uniqueness, causal, empirical, comparative, convergence, safety, or adequacy claim, expose that claim separately with its owning premise/proof/evidence/authority.

Project-local axiom/assumption sets SHALL be jointly coherent enough for the governed use. When non-emptiness, consistency, or realizability is material, provide a construction/model/witness, derivation, or explicit unresolved assumption rather than relying on vacuity. This is proportionate; Protocol 6.4 does not demand a foundational consistency proof of ordinary mathematics.

## 5. Well-definedness and formal completeness

A formal definition or contract is adequate only when its meaning is well-defined over its governed scope.

State when material:

- bound/free-variable scope and quantification;
- domain, codomain, type, shape, and units;
- whether a mapping is total or partial and, for a partial mapping, its admissible domain/failure status;
- branch/sign/ordering/normalization/coordinate conventions;
- deterministic, stochastic, set-valued, multivalued, or choice semantics;
- existence and uniqueness assumptions/results when later reasoning requires a single object;
- piecewise-case coverage, overlap, and precedence;
- equality/equivalence/approximation/asymptotic/distributional relation actually intended;
- boundary/initial conditions and validity interval/regime;
- undefined/singular/degenerate cases when they can affect interpretation.

For example, if

\[
x^* = \operatorname*{argmin}_{x\in X} f(x)
\]

is later treated as one deterministic value, the formulation must establish or assume uniqueness, define a selection rule, or instead use the set-valued `argmin`. Typography alone does not close that ambiguity.

A fixed-point or implicit definition must state enough conditions to identify the intended solution set and any selection/uniqueness semantics. D2 additionally preserves accepted numerical approximation/error semantics; D3/D4 do not silently strengthen an approximate or set-valued upstream object into an exact unique one.

## 6. Assumption, validity, and applicability closure

For every material use of an imported or derived result `r` with hypotheses/validity conditions `H(r)`, current use is admissible only when each material condition is:

1. established from already available premises/results; or
2. explicitly adopted as an assumption by the owning formulation; or
3. explicitly propagated as a condition on the dependent result/concretization.

Conceptually:

\[
\operatorname{use}(r)
\Rightarrow
\operatorname{discharged\_or\_propagated}(H(r)).
\]

A citation or definition edge does not discharge hypotheses.

If a required condition is known false, the use is invalid. If its satisfaction is materially uncertain, current use is `REVIEW_REQUIRED`/challenged as appropriate; uncertainty must not be compacted away.

Validity, approximation, and uncertainty conditions remain typed relations rather than `USES_DEFINITION` edges. Use `ASSUMES`, `CONSTRAINED_BY`, D1/D2 validity semantics, or a narrower owner-defined relation. Descendants may narrow a validity regime but cannot silently broaden it or promote approximate/empirical relations to exact identities.

When a D1/D2 validity condition materially constrains D3/D4 behavior, the lower domain carries the exact typed upstream route needed to prevent violating that envelope.

## 7. Derivation and proof dependency discipline

For a material project-local `DERIVED_RESULT`, make its direct proof/derivation basis recoverable proportionately to risk. Use the existing `DERIVED_FROM` relation or an equivalent explicit derivation route; do not overload `USES_DEFINITION`.

A derivation cannot obtain warrant from a result that, through the live derivation chain, depends materially on the same conclusion. Circular support is invalid.

Legitimate mutual induction, simultaneous proof, or equivalent coupled derivation is represented as one explicit composite proof unit with its external premises and internal proof structure visible enough to establish well-foundedness. Do not expose it as several independent results that circularly cite one another.

A project-local derived claim with no supplied derivation/proof may remain an explicit conjecture/hypothesis/proposed claim where the owning process permits, but must not be represented as an established theorem/result. Empirical evidence may support an empirical claim or motivate a conjecture but does not silently become deductive proof.

## 8. Typed relation ownership and trace completeness

Protocol 6.4 adds one generic semantic-dependency relation:

```text
subject USES_DEFINITION -> exact semantic object whose canonical definition is directly used
```

Canonical ownership is split without duplication:

- `abstraction-and-concretization.md` owns the universal requirement that material definition/prerequisite closure be recoverable;
- `evidence-evolution-and-dependencies.md`, as the existing semantic-dependency owner, SHALL define `USES_DEFINITION` direction, endpoint durability, absence/completeness semantics, and change-impact interaction alongside the other typed relations;
- `scientific-technical-writing.md` SHALL define how human-facing authority exposes definitions, direct prerequisites, aliases, import binding, and scope;
- `source/SEMANTIC_DEPENDENCIES.md` remains a derived current relationship view and SHALL display the new relation only as current derived navigation, never as authority.

The parent phrase `evidence-evolution-and-dependencies.md (routing/typed-edge interaction only if needed)` is superseded: this owner **is required** because 6.4 introduces `USES_DEFINITION`.

### Completeness

For the declared current authority scope, the canonical definition trace SHALL be materially complete over direct `USES_DEFINITION` prerequisites needed to reconstruct meaning or determine impact. Progressive disclosure may partition the trace, but the composed current authority must close it.

A deliberately partial diagnostic/index may remain useful if marked partial. Its missing edge cannot establish independence. The inherited Protocol 6.3 rule remains:

> absence of an edge establishes independence only when the relevant mapped scope was explicitly reviewed complete for that exclusion.

Do not create a repository-wide universal graph merely to satisfy this rule; completeness is bounded by the authority/document family and material semantics being represented.

## 9. Definition evolution, identity, and impact

A stable label, symbol, heading, definition ID, or anchor is a locator, not semantic continuity proof.

When a canonical definition changes:

1. classify the change as semantic-equivalent editorial/notation repair or material semantic mutation;
2. for material mutation, use the owning D1-D4 acceptance process rather than documentation-only editing;
3. identify materially dependent `USES_DEFINITION`, `DERIVED_FROM`, `ASSUMES`, `CONCRETIZES`, evidence, documentation, and other affected relations through bounded impact closure;
4. mark affected evidence/results review-required/stale where applicability may change, preserving unaffected siblings with reason;
5. record material previous-vs-current meaning and rationale in semantic history when required by the existing evolution owner.

If incompatible old and new meanings must both remain supported, distinguish them by explicit version/regime/object identity or other unambiguous scoping. Do not keep one current canonical definition whose meaning varies silently by reader or call site.

Equivalent notation cleanup, added explanation, or formally redundant clarification may preserve semantic identity when independent Review can establish no material meaning change. No universal semantic hash/signature registry is required.

## 10. External-source lifecycle and binding health

Imported specialized knowledge is bound to the exact source identity/edition/version/locator required by Revision 1. Discovery that the source is retracted, corrected, superseded incompatibly, unavailable in a way that prevents required verification, or simply does not support the project statement is a present-use binding/applicability event.

Do not silently replace the bound source with a newer edition or floating `latest` reference. Instead:

- determine whether the imported semantics remain supported;
- if support is uncertain, mark dependent current use `REVIEW_REQUIRED` or challenge it;
- if a replacement source/result changes material meaning, treat that as an input-semantic change and close dependent impact;
- if a newer source is demonstrably semantically equivalent for the governed use, it may be remapped through the normal owner/evidence review without manufacturing a semantic change.

Historical citation identity remains recoverable even when current support degrades. A retraction or correction does not rewrite history; it changes present confidence/applicability.

## 11. Protocol/profile/PEM schema independence

The intended Protocol 6.4 change is doctrine/representation strengthening, not an orchestration machine-contract redesign.

Therefore:

- create a distinct `ssdp-protocol-6.4` profile/resource set as the parent requires;
- retain orchestration profile **schema v2** if the machine-readable profile contract remains unchanged;
- do not bump profile schema merely because protocol doctrine/version changed;
- if implementation proposes a new machine field/structure for definition traceability, classify that separately as a machine-contract change, justify it at the appropriate owner, and update schema/compatibility/tests only if genuinely required;
- PEM schema 1 remains supported and unchanged unless an independently justified PEM representation change is required; 6.4 definition traceability alone is not such a reason;
- do not churn project-local PEM records merely to mirror protocol-version text. Perform the inherited closeout-learning assessment and mutate PEM only when its admission/update threshold is actually met.

## 12. Axiomatic semantic order

A compliant authority document/family need not use one rigid chapter order, but its semantic dependency order shall be equivalent to:

```text
FOUNDATIONAL_ASSUMED reader knowledge
+ exact EXTERNAL_IMPORTED specialized prerequisites
+ PROJECT_DECLARED primitive objects/signatures
 -> explicit axioms/premises/assumptions/validity conditions
 -> definitions from available objects
 -> derived propositions/theorems/results
 -> algorithms/contracts/consequences that use those semantics
 -> interpretation, evidence, rationale, limitations, and explanatory prose as appropriate
```

Definitions and results may be interleaved when dependency order remains valid. A later definition may not retroactively supply meaning required by an earlier normative inference. A non-normative abstract/summary may briefly forward-name a later concept only under the parent's forward-reference rule; it cannot establish, modify, or reason from that concept before the canonical definition is available.

This is an **axiomatic semantic order**, not a demand that every document visually resemble a mathematics textbook.

## 13. Additional preservation obligations

Parent T64-01..T64-30 and Revision-1 T64-31..T64-42 remain binding except where explicitly superseded above. Add:

| ID | Obligation |
| --- | --- |
| T64-43 | Treat `FOUNDATIONAL_ASSUMED` as an availability basis, not a claim of historical provenance; allow semantic roles to be non-exclusive. |
| T64-44 | Permit explicit project primitive declarations as semantic roots only with recoverable signature/scope/axioms/constraints; prohibit hidden primitive semantics. |
| T64-45 | Treat formal binders/local declarations as scoped availability while requiring their domains/types and referenced objects to be available. |
| T64-46 | Keep definitions distinct from axioms/premises/assumptions/empirical claims/normative contracts; notation cannot manufacture truth or authority. |
| T64-47 | Require proportionate well-definedness: scope/quantification/domain/partiality/branch/piecewise/existence/uniqueness or explicit set-valued/choice semantics when material. |
| T64-48 | Require every material imported/derived result use to discharge, explicitly assume, or propagate its hypotheses and validity conditions. |
| T64-49 | Preserve approximation/empirical/uncertainty status and validity envelopes downstream; descendants cannot silently promote them to exact/unconditional semantics. |
| T64-50 | Require material project-local derivations to expose direct proof/premise dependencies and reject circular warrant outside an explicit composite proof construction. |
| T64-51 | Make `evidence-evolution-and-dependencies.md` the canonical owner of the new `USES_DEFINITION` typed relation semantics and impact behavior. |
| T64-52 | Require material completeness of direct definition-use edges over the declared canonical authority scope; partial views cannot prove independence by omission. |
| T64-53 | Treat material definition change as an owner-level semantic mutation with descendant/evidence/history impact; stable labels cannot launder changed meaning. |
| T64-54 | Treat external-source correction/retraction/incompatible revision as a present-use binding/applicability event; never silently float imports to `latest`. |
| T64-55 | Keep orchestration profile schema v2 unless the machine-readable profile contract actually changes; doctrine-version change alone is not a schema change. |
| T64-56 | Preserve PEM schema independence and avoid memory churn absent an admitted material learning/update. |
| T64-57 | Preserve axiomatic semantic ordering while allowing flexible document layout and progressive disclosure. |
| T64-58 | Require proportionate coherence/non-vacuity of project-local axioms/assumptions when consistency, realizability, or non-empty admissible domain is material to the conclusion. |

Revision-1 terminology referring to `FOUNDATIONAL` as literal source provenance is superseded by T64-43. Revision-1 singular `role(x)` notation is superseded by the non-exclusive `roles(x)` model above.

## 14. Qualification extensions

Parent Q64-01..Q64-30 and Revision-1 Q64-31..Q64-45 remain binding under the latest semantics. Add:

```text
Q64-46 project primitive state space/operator is introduced by explicit signature + governing axioms/constraints before use, without a constructive definition -> PASS
Q64-47 project-specific primitive term appears with no signature/domain/axioms and later reasoning depends on inferred prose meaning -> FAIL
Q64-48 local bound variable introduced by `forall x in X` or an explicit local declaration, with X already available -> PASS
Q64-49 local symbol shadows a materially different object across an ambiguous scope boundary -> FAIL
Q64-50 desired property such as stability/uniqueness/accuracy is asserted only by embedding it in a definition/name -> FAIL
Q64-51 property is separately stated as assumption/theorem/empirical claim/contract with appropriate warrant -> PASS
Q64-52 single-valued `argmin`/implicit solution is used without uniqueness or a selection rule where multiple solutions are possible -> FAIL
Q64-53 set-valued semantics, explicit choice rule, or justified uniqueness closes the same case -> PASS
Q64-54 piecewise definition has materially overlapping cases with no precedence, or uncovered cases treated as defined -> FAIL
Q64-55 partial mapping states its admissible domain and governed failure/undefined behavior -> PASS
Q64-56 imported theorem is cited and defined correctly but a material hypothesis is false/undischarged at the use site -> FAIL
Q64-57 imported/derived result has each material hypothesis established, explicitly assumed, or propagated to descendants -> PASS
Q64-58 approximation introduced under a bounded regime is later treated as an exact unconditional identity -> FAIL
Q64-59 project-local theorem derives through a circular live DERIVED_FROM chain that ultimately relies on the same theorem -> FAIL
Q64-60 mutual induction/simultaneous proof is represented as one explicit well-founded composite proof unit -> PASS
Q64-61 canonical definition trace claims complete scope while omitting a known direct USES_DEFINITION prerequisite -> FAIL
Q64-62 derived diagnostic trace is explicitly PARTIAL and is not used to prove independence; canonical definitions still close prerequisites -> PASS
Q64-63 canonical meaning changes materially under the same anchor while known descendants/evidence are left accepted without impact review -> FAIL
Q64-64 editorial wording/notation clarification proven semantically equivalent preserves identity and still-valid dependent evidence -> PASS
Q64-65 bound imported standard/source is silently changed to a newer materially different revision because it is now `latest` -> FAIL
Q64-66 source correction/retraction is surfaced and dependent applicability is reviewed/challenged rather than silently ignored -> PASS
Q64-67 6.4 receives a distinct profile but unchanged machine contract retains schema v2 -> PASS
Q64-68 profile schema or machine fields change solely to mirror documentation doctrine without an independently justified machine-contract need -> FAIL
Q64-69 USES_DEFINITION appears in project traces but the canonical semantic-dependency owner never defines its direction/completeness/impact semantics -> FAIL
Q64-70 a project-local axiom set is knowingly inconsistent/empty in the governed regime yet a substantive conclusion is claimed by vacuity without disclosure -> FAIL
```

For Q64-50, Q64-56, Q64-59, Q64-63, Q64-66, and Q64-70, use independent semantic Review or bounded objective fixtures rather than pretending lexical checks can establish truth, consistency, theorem applicability, or semantic equivalence.

## 15. Falsification extensions

Parent F64-A..F64-F and Revision-1 F64-G..F64-H remain binding. Add:

### F64-I — Primitive / definition / well-definedness challenge

Attempt to find undeclared project primitives, hidden local-scope assumptions, truth claims smuggled into definitions, single-valued objects lacking existence/uniqueness/selection semantics, ambiguous piecewise/branch behavior, partial mappings presented as total, and inconsistent/vacuous local axiom sets. Passing typography is irrelevant if the object is not mathematically well-defined.

### F64-J — Applicability / derivation challenge

For representative imported and project-derived results, independently reconstruct hypotheses, validity regimes, approximation status, and direct proof/premise dependencies. Attempt to apply them outside their envelope, drop assumptions in descendants, upgrade approximations to exact identities, or construct circular derivations that remain superficially traceable.

### F64-K — Trace completeness / evolution / schema challenge

Attempt to omit a material direct `USES_DEFINITION` edge from an allegedly complete trace, mutate a canonical definition while preserving the same label and stale evidence, silently float an imported source to a changed revision, or bump profile schema without a machine-contract change. Confirm the semantic-dependency owner actually owns the new edge semantics and that derived indexes remain subordinate.

F64-B additionally accepts explicit project primitives as valid roots only when their signature/axioms close. F64-C additionally challenges definition laundering. F64-D additionally checks completeness claims and material definition evolution. F64-H additionally checks use-site assumption/validity discharge for imports.

## 16. Implementation-stage amendments

### Stage A amendment

Canonical doctrine SHALL implement Sections 2-12 above. In particular:

1. universal representation defines scope-aware semantic availability and permits explicit project primitives;
2. `scientific-technical-writing.md` defines axiomatic semantic order, local binder/scope rules, definition-vs-axiom discipline, well-definedness, use-site validity discharge, and source lifecycle presentation;
3. D1/D2 owners require applicable mathematical well-definedness, assumption/validity closure, and derivation discipline; D3/D4 carry only material local consequences without freezing delegated mechanics;
4. `evidence-evolution-and-dependencies.md` is **mandatorily** amended to own `USES_DEFINITION` relation direction, completeness/absence semantics, durable endpoint identity, and impact closure;
5. `source/SEMANTIC_DEPENDENCIES.md` is reconciled as a derived view of those current relations.

Do not implement a parallel definition registry or a second dependency authority.

### Stage B amendment

Protocol/profile integration SHALL preserve orchestration profile schema v2 unless an independently justified machine-readable contract change is actually introduced. A new protocol/profile identity is not itself a schema change. PEM schema remains independent as above.

### Stage C amendment

Qualification SHALL include Q64-46..Q64-70 in addition to all earlier Q64 cases, with executable/static negative fixtures only where the property is honestly machine-decidable. Review fixtures and independent semantic inspection remain mandatory for well-definedness, consistency, theorem applicability, semantic equivalence, and literature/source-support judgments that cannot be inferred mechanically.

### Stage E amendment

Independent assembled-candidate Review SHALL execute F64-A..F64-K against the parent + Revisions 1-2. It SHALL inspect the final current owners, generated descendants, profile/schema surface, exact-ref bootstrap, and representative D1-D4 example/qualification fixtures rather than accepting the amendment text itself as evidence of implementation.

### Stage F amendment

Closeout SHALL reconcile any material definition/source-semantic changes into current dependency views, evidence applicability, semantic history, version/profile documentation, and the Protocol-7 inheritance-only revision. Stable anchors or old green tests do not substitute for impact closure.

## 17. Third-review verdict

After this closure, the composed workplan now enforces the stronger invariant actually needed for axiomatic technical documentation:

```text
availability basis      != historical provenance
semantic roles          are not forced mutually exclusive
primitive declaration   != hidden undefined concept
definition              != axiom / assumption / theorem / empirical truth / authority
formal notation         != mathematical well-definedness
citation/source support != use-site hypothesis satisfaction
USES_DEFINITION         != ASSUMES / DERIVED_FROM / CONCRETIZES / evidence dependency
trace present           != trace complete
a stable label          != unchanged semantic meaning
new protocol profile    != new machine profile schema
```

A compliant 6.4 document must therefore be not only formal-looking but semantically closed, well-defined, applicability-correct, and impact-traceable.

**THIRD DESIGN REVIEW VERDICT: PASS — blockers 0; Serious Challenges 0.**
