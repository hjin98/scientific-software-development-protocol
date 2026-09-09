---
kind: protocol-minor-revision-workplan-amendment
workplan_id: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE
amends_workplan: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
protocol_version: 6.0.0
target_protocol_version: 6.1.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-09
review_round: 4
design_review: pass
active_serious_challenge: none
---

# SSDP 6.1 Human-Facing Documentation Context Standard and Final Review Closure

## 1. Authority and purpose

This amendment is a mandatory current companion to `SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`.

It adds one human-facing documentation requirement requested after the consolidated third review and closes the ambiguities exposed by applying that requirement across the Protocol. It does not reopen the Protocol 6.1 evidence/evolution objective, change the pre-automation control boundary, or authorize Protocol 7 machinery.

The parent plus this amendment form the current Protocol 6.1 implementation handoff. Every parent requirement remains binding unless this amendment explicitly narrows or supplements it.

No Serious Challenge was found. The remaining issues were documentation-comprehension and scope precision.

## 2. Background and terminology

The **Scientific Software Development Protocol (SSDP)** treats human-readable scientific and engineering documents as the primary carriers of substantive semantic reasoning, while Protocol 6.1 remains document-controlled.

For this amendment:

- **human-facing documentation** means documentation intended to be read directly for scientific, engineering, operational, review, handoff, or explanatory understanding rather than consumed only as machine data;
- **intended competent reader** means the audience the document is reasonably written for, including its assumed scientific/engineering background;
- **non-common domain terminology** means a specialized term, named method, project-specific concept, or domain-specific usage that cannot reasonably be assumed to be understood by that intended reader without explanation;
- **background definition** means a concise explanatory definition sufficient to orient the reader before the term carries substantive reasoning in the document.

The standard is audience-relative. A term common to specialists in the explicitly intended audience need not be re-taught merely because it is technical. When commonness is genuinely uncertain, prefer a short definition over unexplained jargon.

## 3. Human-facing background-context standard

Protocol 6.1 SHALL strengthen scientific/technical writing with the following rule:

> Every newly introduced non-common domain-knowledge term used by a human-facing current document must be backed by a concise definition and short contextual explanation in a `Background`, `Background and terminology`, or equivalently explicit background section before the reader is expected to rely on that term for substantive reasoning.

This requirement applies to human-facing artifacts including, but not limited to:

- D1 Scientific Method Papers;
- D2 Numerical & Algorithmic Method Papers;
- D3 Architecture Manuals;
- D4 Specifications when they introduce domain concepts rather than only concrete interface syntax;
- substantial workplans/change plans and handoffs;
- user/developer guides and runbooks;
- review, verification, qualification, and historical-evolution reports when they introduce specialized concepts needed to interpret their conclusions;
- human-readable control/schema documentation introduced later under Protocol 7.

### 3.1 Intended reader and assumed background

A substantial scientific/technical document SHOULD make its intended reader or assumed background apparent when that is necessary to decide what terminology requires explanation.

Do not exploit an artificially expert audience assumption to avoid defining project-specific or unusually specialized terminology. Conversely, do not expand a methods paper into a textbook by defining ordinary discipline vocabulary already common to its stated audience.

### 3.2 Definition placement and progressive disclosure

For substantial D1/D2 papers and other documents that introduce several specialized concepts, use an explicit `Background and terminology` section near the beginning of the semantic document family, before the normative formulation or design discussion depends on those concepts.

The section should explain only enough background to make later reasoning interpretable. Detailed derivations, normative equations, algorithm guarantees, architecture contracts, or implementation specifications remain in their owning sections.

For a short human-facing artifact introducing only one or two specialized terms, a compact explicit `Background` / `Background and terminology` subsection is sufficient. Do not create a separate glossary database or terminology artifact solely for protocol symmetry.

A multi-file document family may use one shared background section when composition is explicit and every dependent file is distributed/read with that background as part of the current artifact set. A standalone file must not require hidden chat or an unsupplied document to decode its essential terminology.

### 3.3 Explanatory definition versus normative definition

A background explanation does not automatically become D1/D2/D3/D4 semantic authority merely because it defines a term for the reader.

If a term has project-specific normative meaning capable of changing scientific conclusions, numerical semantics, architecture, or public behavior:

1. provide the concise human-facing explanation in background context;
2. place the precise normative definition/contract in the appropriate D1/D2/D3/D4 owner;
3. cross-reference the owner when useful rather than creating a competing definition.

If the background explanation and accepted semantic owner disagree materially, route the disagreement to the owning domain. `software-documentation` may repair explanatory drift but may not choose new scientific/numerical/architectural/product truth editorially.

## 4. Abbreviation and acronym standard

Human-facing prose SHALL introduce an abbreviation/acronym by writing the full term followed immediately by the abbreviation in parentheses on first explanatory use, using the conventional form:

```text
alpha beta gamma (ABG)
```

After that introduction, `ABG` may be used consistently within the same standalone document or explicitly composed document unit.

Examples:

```text
machine-learning force field (MLFF)
molecular dynamics (MD)
finite element method (FEM)
```

### 4.1 Independently consumable summaries

An abstract, executive summary, figure/table caption, or other independently consumable human-facing component should define a non-obvious abbreviation on first use within that component when a reader may encounter it without the main body.

The main body may define it again at first use when doing so materially improves standalone readability. Avoid forcing the reader to search backward into an abstract for the only expansion.

### 4.2 Titles, headings, metadata, and identifiers

Prefer the full term in a title/heading when practical. If a conventional or externally fixed abbreviation must appear in a title, identifier, profile key, filename, CLI token, or other opaque label, define it at the first explanatory prose occurrence where a human reader must understand its meaning.

Machine-facing values, code identifiers, JSON keys/enums, mathematical symbols, chemical symbols, standardized units, filenames, and immutable compatibility identifiers do not require expansion inside the machine representation itself. Their human-facing reference/schema documentation must still explain non-obvious meaning.

### 4.3 Collision and consistency

Do not use one abbreviation for two different terms within the same human-facing document unless the distinction is unavoidable and explicitly disambiguated. Preserve one expansion and capitalization convention after introduction.

Do not mechanically expand every capitalized token with an acronym linter. Abbreviation correctness is semantic/contextual; mechanical checks may protect known templates/examples but cannot replace editorial review.

## 5. Historical and version-bound discipline

Do not retroactively edit release-pinned or historical Protocol 5.x/6.0 artifacts solely to satisfy this new 6.1 presentation standard.

Current Protocol 6.1 documentation, templates, skills, guides, and generated current packages SHALL follow the new standard. Historical material remains truthful to its governing version. When current documentation cites historical terminology or unexplained historical abbreviations, provide enough current context for a reader to understand the citation without rewriting the historical artifact.

## 6. Canonical ownership and implementation surface

Implement this standard through the minimum coherent source chain rather than duplicating the full rule everywhere.

### 6.1 Canonical writing owner

`source/shared/references/scientific-technical-writing.md` SHALL become the primary current Protocol 6.1 owner of the human-facing background/terminology and first-use abbreviation standard.

It should define:

- intended-reader / assumed-background reasoning;
- background-section requirements;
- concise terminology explanation;
- normative-definition boundary;
- first-use abbreviation convention;
- independently consumable summary behavior;
- machine-only/identifier exceptions;
- anti-overdocumentation proportionality.

### 6.2 Documentation specialist

`source/specialists/software-documentation/SKILL.md` SHALL explicitly require the specialist, when creating or materially refactoring human-facing documentation, to check:

- unexplained non-common terminology;
- missing/insufficient background context;
- first-use abbreviation expansion;
- conflicting abbreviation meanings;
- explanatory definitions drifting from accepted semantic owners.

The skill should route substantive scientific/numerical definition disputes to D1/D2 rather than resolving them through editorial authority.

### 6.3 D1/D2 authoring paths and templates

The current D1 and D2 role authoring guidance SHALL preserve this standard through their existing scientific-writing route.

Update at least:

- `source/shared/templates/scientific_method_paper_template.md` to include a `Background and terminology` section before the normative scientific/mathematical formulation;
- `source/shared/templates/numerical_algorithmic_method_paper_template.md` to include a `Background and terminology` section before the governing numerical/algorithmic formulation.

Each template's background section should ask for:

- intended reader / assumed prerequisites where material;
- definitions and short explanations of specialized terminology introduced by the paper;
- expansion of abbreviations on first prose use;
- references to external standard methods/literature where materially helpful.

Do not move normative D1/D2 definitions out of their normative sections merely to populate the background section.

### 6.4 Other current documentation surfaces

Reconcile `documentation-maintenance.md`, `documentation-and-evidence.md`, role skills, workplan templates, user guides, README/navigation, and generated packages only to the extent needed for coherent routing and no contradictory instruction.

Do not reproduce the whole rule in every role skill. Prefer one canonical writing reference plus concise role/specialist obligations.

## 7. Interaction with Protocol 7

Protocol 7 inherits this accepted human-facing documentation standard unless a later accepted authority explicitly replaces it.

Protocol 7 machine control records remain lightweight machine data and are not required to carry pedagogical background prose. However:

- human-readable control/schema specifications must define non-common concepts and abbreviations;
- user/admin/orchestrator guides must provide sufficient background for control-plane terminology;
- TaskEnvelope/ResultEnvelope fields and action/state names may remain compact identifiers when their human-facing schema documentation explains them;
- the minimal web activation prompt need not become a tutorial; the referenced run/protocol/user documentation carries the background obligation.

This preserves the semantic/control-plane separation rather than bloating JSON with explanatory prose.

## 8. Final review findings and closures

Applying the new standard to the current repository exposed and closes the following design gaps:

1. **D1/D2 template gap** — both current method-paper templates lack an explicit background/terminology section. Section 6.3 makes the required repair explicit.
2. **Documentation-skill gap** — the current specialist says to state definitions but does not require enough background context or first-use acronym expansion. Section 6.2 closes this.
3. **Audience ambiguity** — `non-common` was otherwise subjective. Section 3.1 makes it relative to the intended competent reader and requires conservative definition when uncertain.
4. **Normative-authority ambiguity** — explanatory background could otherwise accidentally become or contradict semantic authority. Section 3.3 separates explanatory and normative definitions.
5. **Cross-file hidden-context risk** — a term defined only in an unsupplied file would violate snapshot-complete comprehension. Section 3.2 requires explicit composed background or local definition.
6. **Abstract/summary acronym gap** — first-use rules can fail when summaries are read independently. Section 4.1 closes this.
7. **Opaque-machine-token overreach** — applying prose expansion inside JSON/code/IDs would damage the lightweight control-plane principle. Sections 4.2 and 7 constrain the rule to human-facing explanation.
8. **Acronym collision** — first expansion alone does not prevent ambiguous reuse. Section 4.3 requires consistent unambiguous use.
9. **Historical-mutation risk** — applying the new style retroactively would violate version-pinned truth. Section 5 preserves historical artifacts.
10. **Mechanical-linter overreach** — contextual terminology cannot be reliably decided by capitalization alone. Section 4.3 keeps review semantic and permits only bounded mechanical checks.

No additional blocking contradiction was found between this standard and the Protocol 6.1 authority/evidence/evolution model.

## 9. Additional qualification requirements

Protocol 6.1 behavioral/static qualification SHALL additionally establish, proportionately:

- a new D1 paper that introduces a specialized project/domain term provides concise background before normative reasoning depends on it;
- a new D2 paper introducing a named numerical method or specialized concept provides concise background without replacing the precise D2 normative definition;
- an abbreviation such as `MLFF` is introduced as `machine-learning force field (MLFF)` before ordinary subsequent use;
- an unexplained acronym/non-common term in a human-facing methods document is detected as documentation incompleteness rather than accepted because the model happens to know it;
- an abstract/summary that uses a non-obvious abbreviation remains interpretable when read independently;
- a shared multi-file background is accepted only when the composition is explicit and supplied;
- a project-specific explanatory definition that conflicts with the governing D1/D2 owner is routed as semantic/documentation reconciliation rather than silently chosen by the documentation specialist;
- machine-only JSON keys/enums or opaque compatibility identifiers are not polluted with explanatory prose merely to satisfy the human-facing rule;
- human-readable schema/user documentation still explains those machine identifiers;
- historical 5.x/6.0 documents are not retroactively rewritten solely for 6.1 terminology/background style.

Static checks should verify the canonical templates/routing instructions where economical. Do not attempt a universal automated detector for whether every specialized term is `common`; behavioral/editorial review remains the semantic oracle.

## 10. Additional acceptance criteria

The Protocol 6.1 workplan cannot PASS implementation until, in addition to the parent criteria:

1. the current scientific/technical writing reference contains the human-facing background-context and abbreviation rules;
2. the documentation specialist explicitly checks those rules during substantive human-facing documentation work;
3. D1 and D2 current method-paper templates contain a usable `Background and terminology` section before their normative method sections;
4. D1/D2 role authoring routes make the standard discoverable without duplicating semantic authority;
5. explanatory background definitions are not treated as a substitute for precise owning-domain definitions;
6. multi-file composition does not create hidden-context requirements;
7. non-obvious abbreviations are expanded on first explanatory use with the `full term (ABG)` convention;
8. independently consumable summaries define abbreviations sufficiently for standalone interpretation;
9. machine-facing identifiers/control records remain compact while human-facing documentation explains them;
10. current generated packages/source-chain derivatives contain the accepted standard consistently;
11. inherited plus new qualification demonstrates the behavior above;
12. independent final Review finds no documentation-standard blocker or active governing Serious Challenge.

## 11. Fourth-review disposition

```text
SERIOUS CHALLENGE: NONE
FINAL WORKPLAN DESIGN REVIEW: PASS AFTER THIS AMENDMENT
BLOCKING DESIGN GAPS FOUND IN ROUND 4: CLOSED BY THIS AMENDMENT
READY FOR IMPLEMENTATION: YES
GOVERNING IMPLEMENTATION CONTRACT: CONSOLIDATED PARENT + THIS AMENDMENT
```

This amendment is intentionally small relative to the parent. It adds human-facing comprehension discipline without converting documentation into a glossary database, adding a new approval role, weakening D1-D4 authority, or moving semantic reasoning into machine control data.