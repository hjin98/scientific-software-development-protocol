# Scientific and Technical Writing

Own human-facing scientific/technical exposition. The universal [Lossless Representation Rule](abstraction-and-concretization.md) governs completeness, salience, progressive disclosure and compactness; this reference specializes it for readable technical documents.

## Background and terminology

**Human-facing documentation** is material read directly for scientific, engineering, operational, review, handoff or explanatory understanding rather than only as machine data. The **intended competent reader** is the audience reasonably assumed by the document. **Non-common domain terminology** is a specialized/named/project-specific term that audience cannot reasonably be expected to understand without explanation.

For every newly introduced non-common term on which later reasoning depends, give a concise definition and short contextual explanation in `Background`, `Background and terminology`, or an equivalent explicit early section. Explain enough to make later reasoning interpretable, not to turn the document into a textbook. A shared background section is valid only when the multi-file composition is explicit and supplied/read together; a standalone file cannot depend on hidden context.

The standard is audience-relative: common specialist terminology need not be re-taught, but project-specific/unusually specialized terms cannot be hidden behind an artificially expert audience assumption. When commonness is genuinely uncertain, a short definition is cheaper than unexplained jargon.

### Explanatory vs normative definitions

Background explanation does not acquire D1/D2/D3/D4 authority merely by defining a term. When meaning can change scientific conclusions, numerical semantics, architecture or public behavior, put the precise contract in its semantic owner and keep background prose orienting/consistent. Material disagreement routes to the owner; documentation cannot adjudicate it editorially.

## Abbreviations and opaque identifiers

Introduce a non-obvious abbreviation/acronym at first explanatory use as:

```text
full term (ABC)
```

Use it consistently thereafter. Independently consumable abstracts/executive summaries/captions should define non-obvious abbreviations within that component when needed; the main body may define again when useful for standalone readability. Avoid abbreviation collisions and inconsistent capitalization.

Machine-facing JSON keys/enums, code identifiers, symbols, standardized units, filenames, command-line interface (CLI) tokens, application programming interface (API) identifiers, profile keys and immutable compatibility identifiers need not be expanded inside the machine representation. Explain non-obvious meaning at the first relevant human-facing occurrence. Do not create a universal glossary/acronym registry or mechanical acronym gate solely for protocol symmetry.

## Authority-aware structure

Know whether the artifact is a D1 paper, D2 paper, D3 Architecture Manual, D4 Specification, or non-normative guide/rationale/evidence/history/publication output. An authority-bearing file may contain normative core plus explanation/evidence/pedagogy; do not treat every sentence/citation as invariant or the whole methods paper as non-normative.

State authority/lifecycle status when ambiguity could cause the wrong artifact to govern. Current documentation explains present truth; release-pinned historical material stays historically accurate.

## Lossless technical representation

After semantic completeness is secured, optimize the writing itself:

1. state each generic rule once at its canonical owner; secondary text gives only the local consequence and precise route unless a short restatement lowers inferential cost;
2. lead with the information that determines action/interpretation—governing claim, decision, blocker/Challenge, material uncertainty—then supporting detail;
3. use the fewest paragraphs/sections consistent with unambiguous interpretation; merge adjacent prose serving the same semantic function;
4. prefer direct stable terminology and explicit definitions over rhetoric, filler, repeated restatement, amendment chronology, excessive abbreviation or chained references;
5. keep specialized/historical/raw detail cold until a visible condition makes it relevant, but keep that route discoverable;
6. do not let importance weighting omit a lower-salience mandatory constraint; prominence and acceptance are different;
7. optimize total cognitive/inferential cost, not character count—over-fragmentation and over-compression are defects when they make the document harder to reconstruct.

## Scientific/mathematical conventions

State conventions before ambiguity can change meaning: units, signs, coordinates/frames, indexing/tensor order, boundary/periodic assumptions, normalization, estimator/sample semantics, precision/tolerance policy. Use LaTeX for formulas and define symbols near first use. Distinguish exact identities, approximations, empirical relationships, heuristics, assumptions and conclusions.

### D1

A Scientific Method Paper should communicate problem/context, prerequisite terminology, governing formulation, observables/estimands, assumptions, validity regime, model uncertainty/limitations, external adequacy/falsification, and material provenance/literature; hand D2 only the minimum invariants needed for faithful numerical concretization.

### D2

A Numerical & Algorithmic Method Paper should communicate governed algorithm/estimator/discretization, normalization/order/precision/stochastic semantics, approximation/error/convergence/conditioning, numerical uncertainty, verification oracles, and the minimum computational semantics D3 must preserve.

### D3 / D4

Architecture documentation states accepted ownership, interfaces, data/control flow, persistence/concurrency/security/resource/deployment boundaries and durable structure without freezing private D4 mechanics unnecessarily. Specifications state concrete stable behavior needed by consumers/automation/persisted state; source detail is not public contract merely because it exists.

## Reproducibility and provenance

At the owning domain, document material inputs, units/shapes/constraints, preprocessing/normalization, algorithms, tolerances/cutoffs, seeds/stochastic semantics, backend/dtype/model/schema identities, failure behavior, approximation regime, and material resource/scaling behavior when required for interpretation or reproduction.

Do not fabricate citations. Prefer primary scientific sources and official software/API documentation for material external claims; distinguish standard borrowed method from project-specific adaptation.

## Guides and rendered output

User guides should bridge concept -> package abstraction -> CLI/API/config -> minimal supported workflow -> output interpretation. Lead with current supported operation; compatibility/advanced alternatives follow when relevant.

For rendered PDF/site outputs, materially changed pages should preserve readable headings/equations/tables/code/figures/captions, working cross-references, consistent notation and no clipping/overlap/broken glyphs. Renderer success alone is not presentation acceptance.

## Completion

For newly created/materially refactored human-facing material check proportionately: unexplained non-common terms, insufficient background, first-use abbreviation expansion/collisions, explanatory definitions drifting from semantic owners, hidden cross-file prerequisites, repeated generic doctrine, amendment-style present-state prose, and compression that loses constraints/uncertainty/provenance. These are semantic/editorial checks, not a mandate for new registries or checker frameworks.
