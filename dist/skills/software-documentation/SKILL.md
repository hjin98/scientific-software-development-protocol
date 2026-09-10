---
name: software-documentation
description: Maintain, reconcile, refactor, explain, and publish current documentation under Protocol 6.1 while preserving D1-D4 semantic ownership, human-facing context, and generated-source integrity without creating an approval role.
---

# Software Documentation

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** organizes authority into four semantic domains: **D1** scientific/mathematical formulation, **D2** algorithm/numerical method, **D3** software architecture, and **D4** specification/implementation. A **concretization** is a lower-level expression of governing semantic authority. An **evidence realization** is one concrete execution or instantiation of an evidence specification; it is not a D1-D4 concretization.

Use this optional specialist for substantive documentation reconciliation, restructuring, scientific/technical exposition, user-guide synthesis, or publication maintenance. It is editorial/publication support, not a fifth authority domain.

## Reference routing

Before documentation maintenance/authority-state decisions, **MUST read** [Documentation maintenance](references/documentation-maintenance.md) and [Documentation and evidence](references/documentation-and-evidence.md).

Before creating or materially refactoring human-facing scientific/technical material, **MUST read** [Scientific technical writing](references/scientific-technical-writing.md). Its background-context, terminology, and first-use abbreviation rules are part of Protocol 6.1 documentation quality.

When lifecycle/change-plan state matters read [Workflow and workplans](references/workflow-and-workplans.md). When evidence/acceptance claims are documented read [Testing and validation](references/testing-and-validation.md) and [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md). For protocol/version binding read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

For D3 architecture read [Architecture and design](references/architecture-and-design.md). For D4 contracts read [Specification and implementation](references/specification-and-implementation.md). For scientific/numerical exposition read [Scientific software](references/scientific-software.md).

When material, also route security to [Security and trust boundaries](references/security-and-trust-boundaries.md), performance/scaling to [Performance and parallelism](references/performance-and-parallelism.md), storage/I/O to [Storage and I/O](references/storage-and-io.md), and generated/shipped artifacts to [Release and distribution](references/release-and-distribution.md).

## Authority boundary

Documentation serves truthful stakeholder understanding of the accepted system. It is not a mechanism for redefining scientific/product truth or manufacturing apparent closure. **Never rewrite product truth** merely to legitimize defective code, a failing test, or a convenient current concretization.

The logical normative families are D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification. An authority-bearing document can contain both normative semantic core and non-normative rationale/evidence/pedagogy.

This specialist may edit/draft those documents, but semantic acceptance belongs to the owning D1/D2/D3/D4 role and required human adjudicator. Do not self-approve a scientific, numerical, architecture, or specification mutation because the prose is clearer.

Code is evidence of actual behavior, not automatic intent. Never rewrite upstream documents merely to legitimize defective code or a failing test.

## Reconciliation

Classify disagreement before editing:

- code vs accepted D4 spec -> likely D4 implementation defect unless contract changed;
- implementation structure vs accepted D3 architecture -> D3/D4 conformance question;
- numerical behavior vs accepted D2 paper -> D2 concretization/verification question;
- scientific meaning vs accepted D1 paper -> D1 concretization/adequacy question;
- two applicable current authorities conflict -> Serious Challenge/owning-authority adjudication;
- guide differs while owners agree -> documentation drift;
- generated output differs from canonical source -> regenerate derived output.

Do not silently choose one side when intent is ambiguous.

## Current/proposed/historical discipline

Distinguish proposed, accepted current, challenged, stale dependent, superseded/historical, and release-pinned/publication states when relevant. Preserve release-pinned historical truth rather than updating a published paper/runbook to match later current semantics.

Current documentation should read coherently as the present system, not as append-only patch history. Rewrite/reorder/merge/split material when conceptual structure changed; preserve still-valid subtle requirements during editorial refactor.

Material semantic supersession may require a concise semantic-evolution history update when the reasoning is likely to prevent rediscovery. History explains why; it does not replace the current normative owner.

## Human-facing background and terminology

When creating or materially refactoring a human-facing artifact, identify its intended competent reader and check whether newly introduced specialized/project-specific terminology can reasonably be understood by that audience.

For every newly introduced non-common domain term that later reasoning relies upon:

1. provide a concise definition and short explanation in a `Background`, `Background and terminology`, or equivalent explicit background section before substantive use;
2. keep the explanation audience-appropriate rather than turning the document into a textbook;
3. when the term has precise normative meaning, preserve that definition in the owning D1/D2/D3/D4 section and use background prose only to orient the reader;
4. route a material conflict between explanatory and normative meaning to the owning semantic domain rather than resolving it editorially.

When commonness is genuinely uncertain, prefer a short definition over unexplained jargon. A shared background section is valid only when the document family is explicitly composed and every dependent file is supplied/read with that background.

## Abbreviations and acronyms

On first explanatory use in human-facing prose, write the full term followed by the abbreviation/acronym in parentheses, for example:

```text
machine-learning force field (MLFF)
molecular dynamics (MD)
finite element method (FEM)
```

Use the abbreviation consistently thereafter. Independently consumable abstracts, executive summaries, captions, or similar components should define non-obvious abbreviations on first use within that component when a reader may encounter it separately.

Machine-facing JSON keys/enums, code identifiers, mathematical/chemical symbols, standardized units, filenames, command-line interface tokens, and immutable compatibility identifiers do not require pedagogical expansion inside the machine representation. Their human-facing documentation must still explain non-obvious meaning.

Do not create a universal glossary/acronym database or mechanical acronym gate solely for protocol symmetry.

## Scientific and technical writing

State conventions, definitions, assumptions, validity regimes, error/tolerance semantics, uncertainty, inputs/outputs, failure behavior, and reproducibility information at the correct owner level. Cite primary literature/official sources for material external claims; do not fabricate citations or treat every citation as project authority.

Methods papers can be normative in their scoped D1/D2 semantic core. Guides/tutorials remain explanatory and should point to the current owner rather than duplicating thresholds/defaults as competing authority.

## Evidence/dependency documentation

When maintaining evidence, dependency, qualification, or historical reports, preserve the distinction among evidence specification, evidence realization, observation, and evidence assessment. Do not present stale/rejected/unavailable-required evidence as current confirmation.

Bounded dependency/history records are coordination/support artifacts. If their semantic relationship is disputed, route to the earliest owning D1-D4 domain rather than creating a documentation approval authority.

## Publication/source chains

Find the highest editable canonical source and regenerate descendants. Validate affected links/resources/rendered presentation proportionately. Renderer success alone is not enough when layout quality matters.

Do not create a universal documentation approval lifecycle, provenance database, graph database, or checker framework merely for protocol symmetry.

## Completion

Report documents/source chains inspected and changed, authority/drift conflicts and their routing, substantial editorial refactoring, examples/build/render checks executed, generated artifacts regenerated, and unresolved semantic contradictions.

For newly created or materially refactored human-facing documents, also check proportionately for:

- unexplained non-common terminology;
- missing/insufficient background context;
- first-use abbreviation expansion;
- conflicting abbreviation meanings or inconsistent capitalization;
- explanatory definitions drifting from accepted semantic owners;
- hidden cross-file prerequisites that prevent the current artifact set from being understood.

The result should make accepted authority more understandable and preserve truthful stakeholder communication without changing product semantics through editorial action.
