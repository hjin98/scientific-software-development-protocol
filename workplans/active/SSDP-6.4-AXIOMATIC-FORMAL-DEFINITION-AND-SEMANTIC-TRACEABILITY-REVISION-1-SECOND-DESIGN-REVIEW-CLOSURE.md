---
kind: abstraction-concretization-change-plan-amendment
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-REVISION-1-SECOND-DESIGN-REVIEW-CLOSURE
amends_workplan: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: active
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: pass-after-second-review
implementation_handoff: authorized
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
parent_workplan_commit: f5d9dc2565751056947d8284b8f239da23940628
accepted_parent_protocol: 6.3.0
accepted_parent_recovery: 9f353097fab36e325a325f1c2f9d9cec32e86177
accepted_parent_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
---

# Protocol 6.4 Revision 1 — Second Design Review Closure

## Current disposition and precedence

**SECOND DESIGN REVIEW: PASS AFTER GAP CLOSURE.** No Serious Challenge to accepted Protocol 6.3 or to the protected Protocol 6.4 outcome remains.

Implementation and independent Review SHALL read this revision together with `workplans/active/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY.md` as one composed handoff. This revision has latest precedence only for the corrected semantic model, definition-dependency representation, import/provenance rules, cross-domain traceability, adoption semantics, and extended qualification below. Every parent obligation not explicitly changed here remains binding.

The second review found real design defects in the initial workplan rather than implementation details. Most importantly, the parent conflated source provenance with inferential status, described a directed acyclic graph while allowing raw cycles, and used one dependency edge for definition, derivation, interpretation, and validity despite Protocol 6.3's typed-dependency doctrine. Those defects are closed here before implementation.

## 1. Review findings closed by this revision

### R64-01 — Provenance and inferential status were conflated

The parent used one classification in which `IMPORTED`, `DERIVED`, and `ORIGINAL` appeared as mutually exclusive provenance classes. That is not generally well formed. A project-local result may be both original to the project and derived from imported premises; an independently re-derived literature result is project-local as a derivation without thereby being novel; an imported result can be used as an assumption, definition, approximation, or theorem.

**Closure:** separate source provenance from semantic/epistemic role as defined in Section 2.

### R64-02 — The proposed DAG admitted cycles

The parent called the definition graph a directed acyclic graph (DAG) while permitting recursive/mutually recursive cycles in that same graph. That is mathematically inconsistent.

**Closure:** the external definition-dependency representation remains a true DAG. An explicitly simultaneous/recursive/fixed-point definition is represented as one composite semantic node; its internal recurrence is part of that node's definition, not an inter-node cycle. Equivalently, an implementation may form the raw strongly connected component and expose its condensation as the normative traceability DAG.

### R64-03 — Definition edges were too broad and effectively untyped

The parent edge `x \prec y` covered definition, derivation, interpretation, and validity dependence at once. That risks recreating the universal untyped dependency graph that Protocol 6.3 explicitly rejects.

**Closure:** the definition DAG owns only direct **definition-use** prerequisites. Assumption, derivation, validity, authority, evidence, execution, and concretization relations retain their existing typed semantics.

### R64-04 — Cross-domain traceability was asymmetric

The parent explicitly required D2 objects to trace to D1 but did not state the corresponding material D3->D2 and D4->D3/upstream obligations strongly enough.

**Closure:** material lower-domain semantics that concretize or preserve an upstream definition/invariant carry an exact typed upstream route under the existing `CONCRETIZES`, `CONSTRAINED_BY`, `ASSUMES`, or other appropriate relation rather than being folded into `USES_DEFINITION`.

### R64-05 — Citation presence was stronger than nothing but weaker than source binding

The parent required a source and an exact local statement but did not require enough source identity/version/locator information to discriminate variants, nor did it require Review to verify that the cited source actually supports the imported claim.

**Closure:** Section 5 adds exact import binding, source-support verification, and notation/convention mapping.

### R64-06 — The foundational envelope still admitted scope laundering

The conservative fallback was present, but the workplan lacked a direct counterfactual against declaring a specialized named method/result “foundational” merely because the intended reader is expert.

**Closure:** Section 6 defines the exclusion and qualification cases explicitly.

### R64-07 — Term identity and symbol identity were not separated

Scoped symbol reuse was covered, but a symbol, abbreviation, section label, or definition ID could still be mistaken for the semantic object's identity. Silent aliases could also become duplicate definitions.

**Closure:** Section 7 separates semantic identity from notation/labels and makes aliases explicit mappings to one canonical definition.

### R64-08 — Backward compatibility lacked an adoption rule

The parent correctly preserved version-bound 6.3 work but did not say what a project or active workplan must reconcile when it explicitly adopts 6.4 while depending on older accepted D1-D4 authority.

**Closure:** Section 8 adds bounded adoption semantics. Adoption does not force a repository-wide rewrite, but 6.4-bound work may not rely on materially ambiguous prerequisite authority merely because that authority predates 6.4.

### R64-09 — Background/import ownership needed one more boundary

Imported specialized knowledge may be introduced in Background, but Background explanation alone must not silently become the project's normative adoption of the premise.

**Closure:** the owning D1-D4 formulation explicitly invokes/adopts the imported object where it is normative, while Background supplies its precise prerequisite statement and source.

### R64-10 — The new active workplan was not represented in the active authority index

A workplan that changes current protocol doctrine must be discoverable through the repository's active workplan routing surface.

**Closure:** the branch authority index is updated in the same review closure to route Protocol 6.4 through the parent plus this revision while keeping Protocol 6.3 accepted-current and Protocol 7 pre-cutover.

## 2. Corrected semantic classification

The parent `origin(x) in {FOUNDATIONAL, IMPORTED, DERIVED, ORIGINAL}` model is superseded.

For every material semantic object `x`, keep **source provenance** distinct from **semantic/epistemic role**:

\[
\operatorname{provenance}(x)
\in
\{\mathrm{FOUNDATIONAL},\mathrm{IMPORTED},\mathrm{PROJECT\_LOCAL}\}.
\]

As applicable, identify the role/status independently:

\[
\operatorname{role}(x)
\in
\{
\mathrm{DEFINITION},
\mathrm{AXIOM\_OR\_PREMISE},
\mathrm{ASSUMPTION},
\mathrm{DERIVED\_RESULT},
\mathrm{EMPIRICAL\_RELATION},
\mathrm{APPROXIMATION},
\mathrm{HEURISTIC},
\mathrm{NORMATIVE\_CONTRACT}
\}.
\]

The list is extensible only when a real semantic distinction requires it; do not create a taxonomy for its own sake.

When originality/novelty matters, state it as a separate claim, for example `BORROWED`, `ADAPTED`, `INDEPENDENTLY_DERIVED`, or `ORIGINAL_CONTRIBUTION`, with the evidentiary/literature basis appropriate to that claim. Novelty is not inferred from `PROJECT_LOCAL` provenance.

Consequences:

- a new project theorem derived from imported lemmas is `PROJECT_LOCAL` + `DERIVED_RESULT`;
- a standard external theorem used as a premise is `IMPORTED` + `AXIOM_OR_PREMISE` for the local formulation;
- an independently re-derived known theorem may be `PROJECT_LOCAL` + `DERIVED_RESULT` + `INDEPENDENTLY_DERIVED`, but must not be called novel merely because the local proof is original;
- a project adaptation has an `IMPORTED` base plus a `PROJECT_LOCAL` modification and must preserve that decomposition.

Any parent references to `ORIGINAL`/`DERIVED` as provenance SHALL be read under this corrected two-axis model.

## 3. Correct definition-dependency model

### 3.1 Definition DAG

For a composed authority family `D`, define the direct definition-use graph

\[
G^{\mathrm{def}}_D=(V_D,E^{\mathrm{def}}_D),
\]

with

\[
(x,y)\in E^{\mathrm{def}}_D
\iff
\text{the canonical definition of }y\text{ directly uses the already-available semantic object }x.
\]

`E_def` does **not** mean “any kind of semantic dependence.” The parent phrase that one edge may represent definition, derivation, interpretation, or validity dependence is superseded.

`G_def` SHALL be acyclic.

### 3.2 Recursive and simultaneous definitions

A recurrence, fixed-point system, simultaneous equation system, mutually recursive grammar, or other mathematically legitimate recursive definition does not create an exception to DAG acyclicity. Instead, its mutually dependent internal objects are represented as one **composite definition node** whose internal semantics include the base/initial condition, fixed-point construction, simultaneous system, or other well-posed definition.

An implementation MAY discover such a group by strongly connected components, but the reviewable external traceability representation is the condensation graph and remains a DAG.

A cycle between independently claimed definition nodes with no explicit composite recursive semantics is invalid.

### 3.3 Other typed relations remain separate

Derivation/proof, assumptions, validity, external constraint, concretization, authority, evidence, and execution relations use their existing typed owners, for example:

```text
DERIVED_FROM
ASSUMES
CONSTRAINED_BY
CONCRETIZES
EVIDENCES
EXECUTION_DEPENDS_ON
```

A human-facing traceability table MAY show several relation types together for convenience, but it must preserve each edge type. It must not serialize them into a single generic `depends_on` relation whose interpretation is ambiguous.

## 4. Cross-domain semantic traceability

Definition closure exists inside and across document families, but D1-D4 authority relations remain typed and directional.

Where materially applicable:

```text
D2 numerical object  --CONCRETIZES/USES_DEFINITION--> exact D1 object
D3 architecture rule --CONCRETIZES/CONSTRAINED_BY--> exact D2/D1 invariant
D4 stable contract   --CONCRETIZES/CONSTRAINED_BY--> exact D3 and directly applicable upstream invariant
```

Use `USES_DEFINITION` only when the lower definition literally uses that semantic object. Use `CONCRETIZES`, `ASSUMES`, `CONSTRAINED_BY`, or the narrower existing relation when that is the real relationship.

The required property is not a fully connected global graph. It is that every **material upstream semantic dependency needed to determine correctness or impact** has a recoverable exact route. A lower-domain object that is independent of a particular upstream definition need not invent an edge.

This typed cross-domain closure is what permits composed impact analysis without turning semantic traceability into a fifth authority plane.

## 5. Imported specialized knowledge and exact source binding

The parent import rule is strengthened as follows.

For an imported specialized object, theorem, model, method, standard, or result, the documentation SHALL identify the external source precisely enough to recover the intended semantics. When variants matter, include the relevant edition/version/revision and theorem/section/equation/standard clause or equivalent stable locator. A floating web page or unversioned “latest” standard is insufficient when later changes could alter the imported meaning.

Review SHALL check **source support**, not citation presence alone: the cited source must actually state or justify the imported object in the form relied upon, within its assumptions and validity regime.

When local notation, units, sign conventions, coordinate conventions, normalization, or terminology differ from the source, define the mapping explicitly before the imported result is reused. A citation plus an unexplained notation translation is not definition closure.

For human-facing scientific/numerical method papers, specialized imported prerequisites normally appear in `Background` / `Background and terminology`. If structure places the detailed statement elsewhere, the Background section must route to that supplied prerequisite before reasoning depends on it.

Background introduction does not itself create project authority. Where an imported result is a normative premise of D1-D4, the owning formulation/specification explicitly invokes or assumes the imported object under the stated conditions. The detailed imported statement may remain in Background by reference; do not duplicate it unnecessarily.

An explicit independent derivation can satisfy semantic closure without relying on an external proof, as the parent allows. It does **not** authorize a false claim of novelty or erase known literature provenance when novelty/priority is itself asserted.

## 6. Foundational knowledge envelope hardening

The foundational knowledge envelope is explicit enough to identify the intended competent audience and the kind of prerequisite curriculum assumed. It is a bounded readability assumption, not an author-controlled escape hatch.

The following are not foundational merely because the reader is a specialist:

- project-specific terms, models, abbreviations, conventions, or named internal methods;
- specialized named theories/methods/theorems for which materially different variants exist;
- field-specific conventions whose sign, normalization, boundary, estimator, or scope can change conclusions;
- a result whose applicability assumptions are themselves material to the project argument.

A genuinely common named theorem or axiom MAY be invoked without local proof/citation when the intended audience can identify the exact standard statement unambiguously and no variant distinction matters. If reasonable uncertainty remains, define or import it.

Independent Review SHALL actively attempt **foundational-scope laundering** by selecting specialized terms that an expert author might be tempted to leave implicit.

## 7. Semantic object identity, notation, and aliases

The semantic object is not identified solely by its symbol, abbreviation, heading, anchor, or definition ID.

- stable labels/anchors support routing and change impact but remain representation identifiers;
- a symbol is notation scoped to a semantic object;
- an alias/synonym is an explicit mapping to the same canonical object, not a second definition;
- materially different meanings require distinct semantic objects even when the same symbol is conventional;
- materially identical meanings should not be duplicated under separate definitions merely because terminology differs.

For a canonical object `x` with aliases `a_i`, the intended relation is

\[
\forall i,\quad \operatorname{denotes}(a_i)=x,
\]

not a family of independently editable definitions.

This rule applies to terms as well as mathematical symbols and prevents terminology drift from bypassing definition traceability.

## 8. Protocol 6.4 adoption and bounded migration

Protocol 6.4 remains backward-compatible with explicitly version-bound 6.3 work. Nothing here retroactively changes a 6.3 contract or rewrites frozen historical artifacts.

When a project/workplan **explicitly adopts 6.4**, apply the new representation obligations over the governed task scope and its materially depended-on authority closure:

1. identify the D1-D4 definitions/invariants actually relied upon by the 6.4-bound work;
2. confirm they already satisfy 6.4 definition/provenance closure or repair their representation at the canonical owner without changing meaning;
3. preserve unrelated current authority and historical artifacts when they are outside the affected closure;
4. if representational repair exposes a real ambiguity that requires choosing among materially different meanings, stop treating it as editorial repair and reopen/challenge the owning D1-D4 authority;
5. remap/review only materially dependent evidence/concretizations under the existing impact rules.

Thus 6.4 adoption is neither a repository-wide rewrite mandate nor permission to rely indefinitely on ambiguous predecessor prose.

A secondary workplan, handoff, review, or summary need not repeat a canonical definition. `available(x)` may be satisfied by a supplied/resolvable, version-bound canonical owner already in the composed context. This preserves Protocol 6.2/6.3 one-owner/progressive-disclosure doctrine while still prohibiting hidden chat/history as a prerequisite.

## 9. Revised preservation obligations

The parent T64-01..T64-30 remain binding except where their wording is superseded by the corrected model above. Add:

| ID | Obligation |
| --- | --- |
| T64-31 | Keep source provenance orthogonal to semantic/epistemic role; `PROJECT_LOCAL` does not imply `ORIGINAL_CONTRIBUTION`, and `DERIVED_RESULT` is not a source-provenance class. |
| T64-32 | Restrict the definition DAG to direct `USES_DEFINITION` prerequisites; keep derivation, assumptions, validity, concretization, evidence, and execution relations typed separately. |
| T64-33 | Keep the external definition traceability graph acyclic by representing a valid recursive/simultaneous system as one composite definition node or equivalent SCC condensation. |
| T64-34 | Require exact typed cross-domain routes for material lower-domain semantics to the upstream definitions/invariants they concretize or are constrained by. |
| T64-35 | Bind specialized imports to exact recoverable source identity/version/locator when variants matter and verify that the source actually supports the imported claim. |
| T64-36 | Define local-to-source notation/unit/convention mappings when they differ materially. |
| T64-37 | Prevent foundational-scope laundering; expertise alone does not make specialized ambiguous named knowledge foundational. |
| T64-38 | Keep semantic identity distinct from symbols/labels/anchors and make aliases explicit mappings to one canonical object. |
| T64-39 | Preserve one canonical definition across secondary artifacts; version-bound resolvable routing satisfies availability without duplicate restatement. |
| T64-40 | Define bounded 6.4 adoption: reconcile materially depended-on prerequisite authority without global rewrite or silent reliance on unresolved ambiguity. |
| T64-41 | Keep Background import exposition subordinate to the owning D1-D4 formulation; normative use explicitly invokes/adopts the imported premise. |
| T64-42 | Keep Protocol 6.4 discoverable through the active workplan authority index as a parent+Revision-1 composed handoff while Protocol 6.3 remains accepted-current. |

Parent T64-13 is superseded specifically by T64-31: implementation must not encode `FOUNDATIONAL/IMPORTED/DERIVED/ORIGINAL` as one mutually exclusive provenance enum. Parent T64-17 is superseded specifically by T64-32/T64-33: valid recursion does not create a raw exception to DAG acyclicity.

## 10. Qualification extensions

Parent Q64-01..Q64-30 remain binding with Q64-11/Q64-12 interpreted under the composite-node rule. Add these discriminators:

```text
Q64-31 project-local theorem derived from imported premises is PROJECT_LOCAL + DERIVED_RESULT, not forced into ORIGINAL-vs-DERIVED provenance -> PASS
Q64-32 known literature method with project-local adaptation explicitly separates imported base from local modification -> PASS
Q64-33 specialized named domain method marked FOUNDATIONAL solely because audience is expert -> FAIL
Q64-34 citation resolves but cited source/version/section does not support the exact imported claim -> FAIL
Q64-35 imported formula is restated in different notation/units with no recoverable mapping and ambiguity results -> FAIL
Q64-36 imported formula with explicit source-to-local notation/unit mapping -> PASS
Q64-37 mutually recursive definitions exposed as an unqualified cycle among independent definition nodes -> FAIL
Q64-38 mutually recursive/fixed-point system represented as one well-posed composite definition node with acyclic external prerequisites -> PASS
Q64-39 material D3/D4 constraint claims to preserve upstream semantics but has no recoverable exact typed upstream route -> FAIL
Q64-40 lower-domain object has no material dependence on a candidate upstream definition and therefore creates no artificial edge -> PASS
Q64-41 same semantic object is duplicated under two editable aliases with no canonical mapping -> FAIL
Q64-42 secondary handoff reuses a canonical version-bound definition through an exact supplied route without restating it -> PASS
Q64-43 6.4-bound work relies on a materially ambiguous predecessor definition and neither reconciles nor challenges it -> FAIL
Q64-44 bounded 6.4 adoption reconciles only materially depended-on authority and preserves unrelated predecessor authority unchanged -> PASS
Q64-45 Background precisely defines/cites an imported theorem but normative D1 silently depends on it without an explicit assumption/invocation -> FAIL
```

The qualification oracle for Q64-33, Q64-34, Q64-39, Q64-43, and Q64-45 is independent semantic Review or a deliberately bounded fixture whose wrong state is objectively encoded; do not build a parser that pretends to adjudicate expertise, literature truth, or scientific dependence from word presence.

## 11. Falsification extensions

Parent F64-A..F64-F remain binding. Extend them and add:

### F64-G — Classification / identity challenge

Attempt to construct objects that are simultaneously project-local and derived, imported and assumed, independently derived but not novel, aliased under multiple terms, or represented by reused symbols. The candidate fails if its model forces false mutual exclusivity or lets label/symbol identity substitute for semantic identity.

### F64-H — Import / adoption / cross-domain challenge

Attempt to falsify exact external source support, source-to-local notation mapping, foundational-envelope claims, explicit normative adoption of imported premises, typed D1->D2->D3->D4 traceability, and bounded 6.4 migration. In particular, search for a 6.4-bound task that can remain apparently conformant while relying on a materially ambiguous predecessor definition.

F64-B additionally checks foundational-scope laundering. F64-C additionally verifies source support rather than citation presence. F64-D additionally verifies that definition-use edges remain distinct from typed cross-domain concretization/constraint edges.

## 12. Implementation-stage amendments

### Stage A amendment

Canonical doctrine must implement the corrected two-axis provenance/role model and the strict `USES_DEFINITION` DAG with composite recursive nodes. Do not implement the superseded single `origin` enum or broad untyped `x \prec y` relation.

The scientific-writing owner shall define import binding, exact source/variant support, source-to-local notation mapping, foundational-envelope limits, alias discipline, and the secondary-artifact routing rule. D1-D4 owners carry only their local consequence plus exact routes to the generic owner.

### Stage B amendment

`protocol-versioning-and-compatibility.md` shall specify bounded 6.4 adoption semantics in addition to the parent version/profile/bootstrap rules. Existing 6.3-bound work remains unchanged.

### Stage C amendment

Qualification includes Q64-31..Q64-45 and explicit negative fixtures for the mechanically representable portions. Source-support/foundational/semantic-dependence claims remain independent-review obligations where no honest executable oracle exists.

### Stage E amendment

Independent Review uses the parent plus this revision and executes F64-A..F64-H. It must review the **assembled** canonical source, generated descendants, profile/snapshot/package surface, and exact-ref bootstrap candidate rather than only the workplan wording or diff.

### Stage F amendment

Final closeout updates the active authority index from proposed 6.4 to accepted/archived only after independent PASS, recovery mapping, mapping-bearing regeneration, Protocol-7 inheritance-only reconciliation, and all inherited Stage-F closure conditions pass.

## 13. Second-review verdict

The corrected workplan now preserves Protocol 6.3 doctrine while making the 6.4 axiomatic objective internally coherent:

```text
source provenance       != inferential role
semantic object         != symbol / alias / anchor
definition dependency   != derivation / assumption / validity / evidence dependency
valid recursion         -> composite semantic definition -> acyclic external DAG
Background import       != project authority
citation presence       != source support
expert audience         != unlimited foundational exemption
6.4 adoption            != global rewrite and != permission to inherit ambiguity
traceability            != shadow authority registry
```

**SECOND DESIGN REVIEW VERDICT: PASS — blockers 0; Serious Challenges 0.**
