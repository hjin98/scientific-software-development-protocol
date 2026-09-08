# Scientific and Technical Writing

Write scientific/technical material so it is rigorous, reproducible, interpretable, and clear about semantic authority.

## Authority-aware writing

Before drafting, identify the document's role:

- D1 Scientific Method Paper;
- D2 Numerical & Algorithmic Method Paper;
- D3 Architecture Manual;
- D4 Specification;
- non-normative guide/tutorial/rationale/evidence/history/publication output.

A D1/D2 methods document can contain an accepted normative semantic core plus supporting explanation/evidence. Do not declare all methods prose non-normative, and do not treat every sentence/citation inside an authority-bearing file as an invariant.

State proposed/current/challenged/stale/historical/release-pinned status when ambiguity could cause the wrong document to govern work.

## Style and structure

Prefer direct prose, explicit definitions, stable terminology, coherent sections, and enough local context to interpret equations, algorithms, inputs, outputs, assumptions, and limitations. Avoid filler, repetitive restatement, implementation chronology, and unexplained internal jargon.

Write permanent current documentation as a coherent present-state explanation rather than a chain of patch notes.

## Mathematical and scientific conventions

State conventions before ambiguity can change meaning: units, signs, coordinates/frames, indexing/tensor order, periodic/boundary assumptions, normalization, estimator/sample semantics, and precision/tolerance policy where material.

Use LaTeX for formulas. Define symbols near first use. Distinguish exact identities, approximations, empirical relationships, heuristics, assumptions, and conclusions.

## D1 writing

A Scientific Method Paper should explain the problem/context, governing formulation, observables/estimands, assumptions, validity regime, model uncertainty, limitations, external adequacy/falsification route, and supporting literature/provenance. It should hand D2 the minimum semantic invariants needed for faithful numerical realization.

## D2 writing

A Numerical & Algorithmic Method Paper should define the governed algorithm/estimator/discretization, normalization/order/precision/stochastic semantics, approximation/error/convergence/conditioning behavior, numerical uncertainty, verification oracles, and the minimum computational semantics D3 must preserve.

## Architecture and specification writing

Architecture documentation explains accepted ownership, interfaces, data/control flow, persistence/concurrency/security/resource boundaries, and durable structure without freezing private D4 mechanics unnecessarily.

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

Lead with the supported current workflow; put compatibility and advanced alternatives later.

## Presentation quality

For rendered PDF/site outputs, preserve coherent headings, equations/tables, useful figures/captions, readable code blocks, working cross-references, consistent notation, and absence of clipping/overlap/broken glyphs on materially changed pages. Renderer success alone is not presentation acceptance.