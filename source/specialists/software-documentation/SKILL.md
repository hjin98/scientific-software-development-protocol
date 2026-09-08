---
name: software-documentation
description: Maintain, reconcile, refactor, explain, and publish current documentation under Protocol 6 while preserving D1-D4 semantic ownership and generated-source integrity without creating an approval role.
---

# Software Documentation

Use this optional specialist for substantive documentation reconciliation, restructuring, scientific/technical exposition, user-guide synthesis, or publication maintenance. It is editorial/publication support, not a fifth authority domain.

## Reference routing

Before documentation maintenance/authority-state decisions, **MUST read** [Documentation maintenance](references/documentation-maintenance.md) and [Documentation and evidence](references/documentation-and-evidence.md).

When lifecycle/change-plan state matters read [Workflow and workplans](references/workflow-and-workplans.md). When evidence/acceptance claims are documented read [Testing and validation](references/testing-and-validation.md). For protocol/version binding read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

For D3 architecture read [Architecture and design](references/architecture-and-design.md). For D4 contracts read [Specification and implementation](references/specification-and-implementation.md). For scientific/numerical exposition read [Scientific technical writing](references/scientific-technical-writing.md) and [Scientific software](references/scientific-software.md).

When material, also route security to [Security and trust boundaries](references/security-and-trust-boundaries.md), performance/scaling to [Performance and parallelism](references/performance-and-parallelism.md), storage/I/O to [Storage and I/O](references/storage-and-io.md), and generated/shipped artifacts to [Release and distribution](references/release-and-distribution.md).

## Authority boundary

The logical normative families are D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification. An authority-bearing document can contain both normative semantic core and non-normative rationale/evidence/pedagogy.

This specialist may edit/draft those documents, but semantic acceptance belongs to the owning D1/D2/D3/D4 role and required human adjudicator. Do not self-approve a scientific, numerical, architecture, or specification mutation because the prose is clearer.

Code is evidence of actual behavior, not automatic intent. Never rewrite upstream documents merely to legitimize defective code or a failing test.

## Reconciliation

Classify disagreement before editing:

- code vs accepted D4 spec -> likely D4 implementation defect unless contract changed;
- implementation structure vs accepted D3 architecture -> D3/D4 conformance question;
- numerical behavior vs accepted D2 paper -> D2 realization/verification question;
- scientific meaning vs accepted D1 paper -> D1 realization/adequacy question;
- two applicable current authorities conflict -> Serious Challenge/owning-authority adjudication;
- guide differs while owners agree -> documentation drift;
- generated output differs from canonical source -> regenerate derived output.

Do not silently choose one side when intent is ambiguous.

## Current/proposed/historical discipline

Distinguish proposed, accepted current, challenged, stale dependent, superseded/historical, and release-pinned/publication states when relevant. Preserve release-pinned historical truth rather than updating a published paper/runbook to match later current semantics.

Current documentation should read coherently as the present system, not as append-only patch history. Rewrite/reorder/merge/split material when conceptual structure changed; preserve still-valid subtle requirements during editorial refactor.

## Scientific and technical writing

State conventions, definitions, assumptions, validity regimes, error/tolerance semantics, uncertainty, inputs/outputs, failure behavior, and reproducibility information at the correct owner level. Cite primary literature/official sources for material external claims; do not fabricate citations or treat every citation as project authority.

Methods papers can be normative in their scoped D1/D2 semantic core. Guides/tutorials remain explanatory and should point to the current owner rather than duplicating thresholds/defaults as competing authority.

## Publication/source chains

Find the highest editable canonical source and regenerate descendants. Validate affected links/resources/rendered presentation proportionately. Renderer success alone is not enough when layout quality matters.

Do not create a universal documentation approval lifecycle, provenance database, or checker framework merely for protocol symmetry.

## Completion

Report documents/source chains inspected and changed, authority/drift conflicts and their routing, substantial editorial refactoring, examples/build/render checks executed, generated artifacts regenerated, and unresolved semantic contradictions. The result should make accepted authority more understandable without changing product semantics through editorial action.