# Numerical & Algorithmic Method Paper

> Canonical D2 document-family template for Protocol 6.1. Adapt structure to the project; one physical file is not mandatory.

## Authority metadata

- State: proposed | accepted current | challenged | risk-accepted/provisional | stale dependent | superseded/historical | release-pinned/publication
- Scope / claim ownership:
- Governing D1 authority and other applicable constraints:
- Human ratification: not-required | required-pending | accepted | rejected

## Background and terminology

State the intended competent reader or assumed prerequisites where material. Define and briefly explain newly introduced non-common domain terminology, named numerical methods, specialized estimators, discretizations, or project-specific concepts before the governing numerical formulation depends on them.

Introduce non-obvious abbreviations at first explanatory use using the conventional `full term (ABC)` form. Cite standard references where they materially improve interpretation.

Keep this section explanatory. Precise normative algorithm definitions, error semantics, convergence guarantees, and tolerances remain in the governing D2 sections below.

## Governing numerical / algorithmic formulation

State the accepted algorithm, estimator/discretization/solver semantics, normalization/ordering, approximation regime, convergence/stopping semantics, precision policy, and other properties that materially determine the governed result.

## Error and numerical uncertainty

State applicable discretization/truncation/iteration/stochastic/conditioning/floating-point error semantics and how they propagate into D1 observables.

## Verification strategy

Identify authoritative exact/limiting/manufactured/reference cases, invariants, convergence/refinement tests, conditioning/sensitivity checks, differential/metamorphic relations, stochastic bias/variance checks, and justified tolerances as applicable. Do not create an oracle by copying production output.

Distinguish evidence specifications from individual evidence realizations and observations. State when repeated realizations, independent evidence routes, or cross-backend comparison are needed for the intended assessment.

## Evidence applicability and dependencies

Identify material evidentiary targets separately from execution dependencies. Record assumptions, input/validity regime, backend/precision/configuration dimensions, and subject revisions when they can change whether prior evidence remains admissible.

When D2 authority or a material concretization changes, review affected evidence specifications/realizations rather than treating old passing observations as automatic confirmation.

## Performance / resource constraints

Record only performance, hardware, scaling, or resource constraints that materially constrain the D2 search space. Keep software implementation detail delegated when possible.

## D2 -> D3 handoff

State the minimum computational semantics architecture must preserve: data/operation dependencies, precision/reproducibility, state/restart semantics affecting the method, error envelope, and material target-resource constraints. Record material dependency links needed for bounded invalidation and impact closure.

## Supporting derivation, references, and alternatives

Explain derivations and literature, and document alternatives where they materially illuminate the accepted choice without creating competing authority.

## Open challenges

Record unresolved material authority challenges or concise resolved rationale needed to prevent recurrence; do not preserve full review transcripts.
