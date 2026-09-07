---
name: software-documentation
description: Keep evolving AI-developed software intellectually accessible to humans. Reconcile documentation with accepted code/specification authority, refactor degraded narratives into coherent current-state documents, explain theory and algorithms, maintain user guides, and publish reproducible derived documentation without creating a parallel development gate.
---

# Software Documentation

Use this optional specialist when documentation needs substantive reconciliation, restructuring, theory/method explanation, user-oriented synthesis, or publication maintenance.

## Reference routing

Before substantive documentation reasoning, apply these explicit routes; load only the reference whose trigger is material.

- Before substantive documentation maintenance, reconciliation, refactoring, or current-state authority decisions, **MUST read** [Documentation maintenance](references/documentation-maintenance.md).
- Before deciding documentation/evidence authority or durable evidence presentation, **MUST read** [Documentation and evidence](references/documentation-and-evidence.md).
- When lifecycle/workplan state affects documentation, read [Workflow and workplans](references/workflow-and-workplans.md).
- When testing, acceptance, qualification, or evidence boundaries affect documentation, read [Testing and validation](references/testing-and-validation.md).
- When protocol/candidate compatibility or version binding affects documentation, read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).
- When architecture/ownership is being explained or reconciled, read [Architecture and design](references/architecture-and-design.md).
- When specification/API/schema contracts are being explained or reconciled, read [Specification and implementation](references/specification-and-implementation.md).
- When scientific exposition or technical method writing is material, read [Scientific technical writing](references/scientific-technical-writing.md).
- When scientific/numerical semantics are material, read [Scientific software](references/scientific-software.md).
- When security or trust boundaries affect docs, rendering, credentials, or external resources, read [Security and trust boundaries](references/security-and-trust-boundaries.md).
- When documented performance/scaling/parallelism claims are material, read [Performance and parallelism](references/performance-and-parallelism.md).
- When documented storage/I/O behavior is material, read [Storage and I/O](references/storage-and-io.md).
- When generated/shipped documentation or release packaging is material, read [Release and distribution](references/release-and-distribution.md).

It is **not** a third lifecycle role and does not approve software. The development hierarchy remains product engineering fitness first, minimum justified product/system complexity second, and development economy third. Documentation makes the accepted result understandable and usable without constraining sound engineering through a parallel process.

Documentation is a stewardship activity for truthful stakeholder understanding and operation of the accepted product. Never rewrite product truth merely to legitimize defective code or create the appearance of completion; surface code/specification contradictions to the owning lifecycle role.

> **Keep an evolving AI-developed software system intellectually accessible to humans.**

## Governing constraints

1. Seek the globally best justified engineering-sufficient product; documentation does not override capability, correctness, scientific fidelity, resource feasibility, scalability, robustness, hardware effectiveness, security, compatibility, or materially required performance.
2. Among engineering-sufficient documentation structures, minimize unnecessary duplication and machinery; then avoid unnecessary documentation-development work without weakening correctness or usability.
3. Preserve exactly one current normative owner for each material contract.
4. Treat code as evidence of actual behavior, not automatically as intended specification.
5. Make permanent current documents describe the accepted present system rather than accumulating implementation chronology.
6. Prevent/correct drift proportionally without becoming a release bureaucracy or introducing unrelated failure modes.
7. Make major capabilities, theory, assumptions, workflows, outputs, and limitations understandable without source-code reverse engineering.

## Operating modes

Choose the fit-for-purpose mode; use only modes that materially serve the documentation task. These are reasoning modes, not required commands or workflow states.

- **maintain** — update durable documentation affected by an accepted software change;
- **reconcile** — resolve code/specification/architecture/guide disagreement;
- **refactor** — restore conceptual structure, terminology, narrative flow, and presentation after substantial evolution;
- **explain** — author or improve user guides, architecture exposition, or non-normative methods/theory material;
- **publish** — regenerate and validate Markdown/PDF/diagram/other derived-document source chains.

A repository-wide audit is a deliberate maintenance/release activity, not the default reaction to a local change.

## Inspect before editing

Identify:

- repository/project documentation authority rules and indexes;
- current specifications and architecture governing the affected capability;
- actual public API/CLI/configuration/schema/runtime behavior;
- relevant tests/examples;
- current versus release-pinned versus historical/proposed documents;
- the true canonical editable source chain for any generated document;
- external scientific/technical sources when the requested explanation requires them.

Do not merely summarize old documentation. For maintenance/reconciliation work, inspect the living product path sufficiently to detect stale descriptions.

## Reconcile authority correctly

Use this default classification:

| Observation | Interpretation | Action |
|---|---|---|
| code and current specification agree; other doc differs | documentation drift | update other doc |
| code differs from accepted current specification | possible implementation defect | report exact contradiction; route semantic decision to `software-design`/`software-implementation` |
| accepted implementation intentionally changed a governed contract but spec did not | specification drift | update specification and affected docs |
| architecture differs from accepted implementation structure | architecture drift | update architecture if structure really changed |
| two current normative documents disagree | authority conflict | resolve semantic/ownership conflict; do not guess |
| generated output differs from canonical source chain | generated-artifact drift | regenerate output |
| current navigation points to obsolete release-pinned material | lifecycle/navigation drift | refresh current document or reclassify old one |

Never rewrite a specification simply to make it agree with an implementation that may be wrong.

## Preserve present-tense conceptual integrity

Permanent documentation is maintained information architecture, not an append-only record.

When new capabilities appear or better theories, algorithms, architectures, defaults, terminology, or workflows supersede old ones, update the current explanation naturally. Do not preserve an obsolete narrative and append amendment after amendment.

When needed, reorder/rename/merge/split sections, rewrite introductions and transitions, replace derivations/figures/examples, and delete superseded current-state prose. Move completed chronology to history/release notes.

Do not minimize documentation diffs at the expense of coherence.

### Refactor without losing valid content

Before a substantial editorial rewrite, identify still-valid scientific, behavioral, architectural, compatibility, limitation, and edge-case information. After rewriting, verify that each remains represented by its correct current owner or is explicitly and intentionally retired.

Do not create permanent clause ledgers or evidence manifests merely to perform this check.

### Detect documentation debt

Refactor rather than locally patch when evidence shows that:

- multiple sections contain overlapping/contradictory explanations;
- several corrective caveats override earlier prose;
- old and current terminology are intermixed;
- the table of contents no longer follows the conceptual model;
- implementation chronology or internal stage IDs dominate the narrative;
- figures/examples represent superseded behavior;
- a competent new reader cannot follow the current system linearly.

## Write for human interpretation

Organize information according to natural conceptual/task flow, not implementation sequence.

Use progressive disclosure:

```text
what capability exists and why
    -> how to use it and interpret outputs
    -> underlying theory and algorithm
    -> detailed numerical/edge-case/implementation material
```

Use concept-first names. Keep internal identifiers for traceability, but introduce their meaning, e.g. `Multi-view subset selection (MVSEL2)`, rather than forcing users to decode stage names as the conceptual ontology.

Use one preferred current term per concept. Mention old names only when an active compatibility/migration need exists.

## Scientific and technical authoring

Follow `references/scientific-technical-writing.md` and `references/scientific-software.md`.

As applicable:

- explain motivation and underlying theory;
- state mathematical/physical conventions explicitly;
- use LaTeX for formulas and define symbols;
- explain the high-level algorithm;
- use pseudocode and flowcharts when they materially improve understanding;
- define input/output data types, shapes, units, ordering, and constraints;
- warn about edge cases, invalid regimes, approximations, and failure behavior;
- state numerical tolerances/cutoffs/precision policy where material;
- discuss scaling/resource behavior when it affects use;
- provide enough information to reproduce the implemented method;
- cite primary literature and official sources that materially motivated algorithms or external behavior;
- distinguish standard/borrowed methods from project-specific adaptations;
- keep prose clean, terse, direct, readable, and professionally presented.

Methods/theory documents are explanatory and non-normative by default. Point to the architecture/specification that owns actual contracts rather than duplicating independent defaults/thresholds.

## User guides and usability

Bridge concepts to operation:

```text
concept -> package abstraction -> CLI/API/config -> example -> interpretation
```

Lead with the preferred current workflow. Put advanced alternatives and compatibility paths later.

Where inexpensive, verify examples through the real public interface: CLI flags/help, imports/signatures, configuration keys/defaults, and lightweight examples. Do not run an expensive GPU/HPC/production workflow when a smaller check establishes that the documentation example is structurally valid.

## Current, pinned, historical, and proposed material

Classify deliberately:

- **current** — describes accepted current software;
- **release-pinned** — intentionally bound to a specific release/environment and states that identity;
- **historical** — past behavior/lineage;
- **proposed** — future work/workplan, not current authority.

Do not update release-pinned runbooks by blind version substitution. Revalidate/regenerate them for the new release or preserve/reclassify the old version honestly.

## Canonical source graphs and publication

Find the highest editable authoritative source before modifying generated documents. Source graphs may be:

```text
canonical.md -> pdf
chapters/* -> assembler -> assembled.md -> pdf
API/schema/code -> generator -> markdown -> pdf
diagram source -> rendered figure -> markdown -> pdf
```

Edit upstream and regenerate descendants. Do not hand-edit only the assembled Markdown, PDF, rendered figure, or another derived artifact when its source exists.

Generate PDFs or other formats only where repository policy/product need requires them. README/index/workplans need not receive PDFs for symmetry.

When generated artifacts are tracked, use one reproducible build/renderer policy and record only provenance that establishes the real source/output boundary.

## Mechanical versus semantic validation

Mechanical checks may fail objectively for the affected document chain, such as missing canonical sources/resources, failed generators, stale assembled Markdown, orphan generated outputs, source/PDF mismatch, or broken directly affected navigation.

Do not encode scientific/semantic decisions as brittle lint rules. Whether an equation matches the implemented estimator, an architecture description is conceptually correct, or a behavior change was intended requires reasoning and may require `software-design`/`software-implementation`.

Scope validation to changed documentation, generated descendants, and directly affected indexes/navigation unless an explicit audit/release policy requires broader scope. Unrelated stale documents must not become accidental blockers for local engineering work.

Visually inspect materially changed rendered documents where layout quality matters. A successful renderer exit is not sufficient if equations, tables, figures, code blocks, headings, glyphs, or page flow are visibly poor.

## Boundaries

This specialist may update documentation, documentation indexes, documentation generators/build tooling, and proportional documentation-only checks.

Do not change product behavior merely to force agreement with prose. If product code is wrong relative to the accepted contract, report the exact discrepancy and route the code change to implementation (and design when semantics are unclear), then reconcile the final documentation.

Do not create a documentation approval lifecycle, universal provenance database, mandatory repository-wide audit, or extensive checker framework unless the project independently demonstrates a material need.

## Milestone reconciliation

At substantial workplan, architecture-migration, or release closeout, reconcile affected durable documentation to the accepted present system when conceptual ownership, scientific methodology, public interfaces/configuration, persistence/state semantics, workflows, or performance/resource behavior changed. Treat an accumulation of historical caveats needed to explain current behavior as a possible design/maintenance signal, not as permission to rewrite product semantics.

Do not turn current-state documentation into an append-only patch history. If reconciliation exposes a genuine code/architecture contradiction, route the semantic issue back to Software Design/Implementation rather than editing documentation to bless unintended behavior.


## Completion

Report proportionally:

- documents/source chains inspected and changed;
- authority/drift conflicts found and how they were resolved;
- substantial structural/editorial refactoring performed;
- theory/usability gaps closed;
- examples/build/render checks actually run;
- generated artifacts regenerated;
- unresolved semantic contradictions or intentionally deferred external checks.

A successful result leaves the accepted software more understandable and transparent without making the development system more fragile or bureaucratic.
