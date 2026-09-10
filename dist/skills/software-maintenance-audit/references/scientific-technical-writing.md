# Scientific and Technical Writing

Write scientific/technical material so it is rigorous, reproducible, interpretable, and clear about semantic authority.

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** treats human-facing documentation as a semantic communication surface: readers must be able to recover the meaning needed to interpret the document without hidden chat or unexplained project jargon.

For this reference:

- **human-facing documentation** means material intended to be read directly for scientific, engineering, operational, review, handoff, or explanatory understanding rather than consumed only as machine data;
- **intended competent reader** means the audience the document is reasonably written for, including its stated or evident scientific/engineering background;
- **non-common domain terminology** means a specialized term, named method, project-specific concept, or domain-specific usage that cannot reasonably be assumed to be understood by that intended reader without explanation;
- **background definition** means a concise explanatory definition sufficient to orient the reader before the term carries substantive reasoning.

The standard is audience-relative. A term common to specialists in the explicitly intended audience need not be re-taught merely because it is technical. Project-specific and unusually specialized terminology must not be hidden behind an artificially expert audience assumption. When commonness is genuinely uncertain, prefer a short definition over unexplained jargon.

## Authority-aware writing

Before drafting, identify the document's role:

- D1 Scientific Method Paper;
- D2 Numerical & Algorithmic Method Paper;
- D3 Architecture Manual;
- D4 Specification;
- non-normative guide/tutorial/rationale/evidence/history/publication output.

A D1/D2 methods document can contain an accepted normative semantic core plus supporting explanation/evidence. Do not declare all methods prose non-normative, and do not treat every sentence/citation inside an authority-bearing file as an invariant.

State proposed/current/challenged/stale/historical/release-pinned status when ambiguity could cause the wrong document to govern work.

## Human-facing background-context standard

Every newly introduced non-common domain-knowledge term used by a current human-facing document must be backed by a concise definition and short contextual explanation in a `Background`, `Background and terminology`, or equivalently explicit background section before the reader is expected to rely on that term for substantive reasoning.

This applies, proportionately, to D1/D2 method papers, D3 Architecture Manuals, D4 Specifications that introduce domain concepts, substantial workplans/handoffs, guides/runbooks, review/verification/qualification reports, semantic-evolution reports, and human-readable schema/control documentation.

For substantial D1/D2 papers and other documents introducing several specialized concepts, place `Background and terminology` near the beginning, before the normative formulation or design discussion depends on those concepts. Explain only enough background to make later reasoning interpretable; detailed derivations, normative equations, algorithm guarantees, architecture contracts, and implementation specifications remain in their owning sections.

A short artifact introducing only one or two specialized terms may use a compact explicit background subsection. Do not create a universal glossary database or terminology registry solely for protocol symmetry.

A multi-file document family may share one background section when composition is explicit and every dependent file is supplied/read with it as part of the current artifact set. A standalone file must not require hidden chat or an unsupplied document to decode essential terminology.

### Explanatory versus normative definitions

A background explanation does not automatically become D1/D2/D3/D4 semantic authority merely because it defines a term for the reader.

When a term has project-specific normative meaning capable of changing scientific conclusions, numerical semantics, architecture, or public behavior:

1. provide the concise human-facing explanation in background context;
2. place the precise normative definition/contract in the appropriate D1/D2/D3/D4 owner;
3. cross-reference that owner when useful rather than creating a competing definition.

If explanatory prose and accepted semantic authority disagree materially, route the disagreement to the owning domain. Documentation support may repair explanatory drift but may not choose new scientific/numerical/architectural/product truth editorially.

## Abbreviations and acronyms

Human-facing prose introduces a non-obvious abbreviation or acronym at first explanatory use by writing the full term followed immediately by the abbreviation in parentheses:

```text
alpha beta gamma (ABG)
```

After introduction, `ABG` may be used consistently within the same standalone document or explicitly composed document unit.

Examples:

```text
machine-learning force field (MLFF)
molecular dynamics (MD)
finite element method (FEM)
```

An abstract, executive summary, figure/table caption, or other independently consumable human-facing component should define a non-obvious abbreviation on first use within that component when a reader may encounter it without the main body. The main body may define it again at first use when that materially improves standalone readability.

Prefer the full term in titles/headings when practical. If a conventional or externally fixed abbreviation must appear in a title, filename, command-line interface (CLI) token, application programming interface (API) identifier, profile key, or other opaque label, define it at the first explanatory prose occurrence where a human reader must understand the meaning.

Machine-facing values, code identifiers, JSON keys/enums, mathematical symbols, chemical symbols, standardized units, filenames, and immutable compatibility identifiers do not require expansion inside the machine representation. Their human-facing reference/schema documentation must still explain non-obvious meaning.

Do not use one abbreviation for two different terms in the same document unless unavoidable and explicitly disambiguated. Preserve one expansion and capitalization convention after introduction. Do not mechanically expand every capitalized token with an acronym linter; abbreviation correctness is semantic/contextual.

## Style and structure

Prefer direct prose, explicit definitions, stable terminology, coherent sections, and enough local context to interpret equations, algorithms, inputs, outputs, assumptions, and limitations. Avoid filler, repetitive restatement, implementation chronology, and unexplained internal jargon.

Write permanent current documentation as a coherent present-state explanation rather than a chain of patch notes.

## Mathematical and scientific conventions

State conventions before ambiguity can change meaning: units, signs, coordinates/frames, indexing/tensor order, periodic/boundary assumptions, normalization, estimator/sample semantics, and precision/tolerance policy where material.

Use LaTeX for formulas. Define symbols near first use. Distinguish exact identities, approximations, empirical relationships, heuristics, assumptions, and conclusions.

## D1 writing

A Scientific Method Paper should explain the problem/context, background terminology, governing formulation, observables/estimands, assumptions, validity regime, model uncertainty, limitations, external adequacy/falsification route, and supporting literature/provenance. It should hand D2 the minimum semantic invariants needed for faithful numerical concretization.

## D2 writing

A Numerical & Algorithmic Method Paper should explain prerequisite terminology and then define the governed algorithm/estimator/discretization, normalization/order/precision/stochastic semantics, approximation/error/convergence/conditioning behavior, numerical uncertainty, verification oracles, and the minimum computational semantics D3 must preserve.

## Architecture and specification writing

Architecture documentation explains accepted ownership, interfaces, data/control flow, persistence/concurrency/security/resource boundaries, and durable structure without freezing private D4 mechanics unnecessarily. Introduce specialized domain concepts before relying on them in architecture reasoning.

Specifications state concrete stable behavior needed by consumers/automation/persisted state. Keep them minimal and precise; do not turn source-code detail into public contract merely because it exists.

## Reproducibility and provenance

Document material inputs, units/shapes/constraints, preprocessing/normalization, algorithms, tolerances/cutoffs, seeds/stochastic semantics, backend/dtype/model/schema identities, failure behavior, approximation regime, and material resource/scaling behavior according to the owning domain.

Do not fabricate citations. Prefer primary scientific sources and official software/API documentation when external claims matter. Distinguish project-specific adaptation from standard borrowed methods.

## User guides

Bridge concept to operation:

```text
scientific/technical concept
 -> package abstraction
 -> CLI/API/configuration
 -> minimal workflow
 -> output interpretation
```

Lead with the supported current workflow; put compatibility and advanced alternatives later. Define non-obvious package/project terminology before operational instructions depend on it.

## Historical/version-bound discipline

Do not retroactively edit release-pinned historical artifacts solely to satisfy a later presentation standard. Current documentation should supply enough context to interpret cited historical terminology without rewriting historical truth.

## Presentation quality

For rendered PDF/site outputs, preserve coherent headings, equations/tables, useful figures/captions, readable code blocks, working cross-references, consistent notation, and absence of clipping/overlap/broken glyphs on materially changed pages. Renderer success alone is not presentation acceptance.

## Completion check

For newly created or materially refactored human-facing documentation, review proportionately for:

- unexplained non-common terminology;
- missing or insufficient background context;
- first-use abbreviation expansion;
- abbreviation collisions/inconsistent capitalization;
- explanatory definitions that drift from their accepted semantic owner;
- hidden cross-file prerequisites that prevent standalone/current composition from being understood.

These are semantic/editorial checks, not a mandate for a universal glossary or acronym-checking framework.