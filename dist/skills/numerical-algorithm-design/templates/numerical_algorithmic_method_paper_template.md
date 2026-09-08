# Numerical & Algorithmic Method Paper

> Canonical D2 document-family template. Adapt structure to the project; one physical file is not mandatory.

## Authority metadata

- State: proposed | accepted current | challenged | stale dependent | superseded/historical | release-pinned/publication
- Scope / claim ownership:
- Governing D1 authority and other applicable constraints:
- Human ratification: not-required | required-pending | accepted | rejected

## Governing numerical / algorithmic formulation

State the accepted algorithm, estimator/discretization/solver semantics, normalization/ordering, approximation regime, convergence/stopping semantics, precision policy, and other properties that materially determine the governed result.

## Error and numerical uncertainty

State applicable discretization/truncation/iteration/stochastic/conditioning/floating-point error semantics and how they propagate into D1 observables.

## Verification strategy

Identify authoritative exact/limiting/manufactured/reference cases, invariants, convergence/refinement tests, conditioning/sensitivity checks, differential/metamorphic relations, stochastic bias/variance checks, and justified tolerances as applicable. Do not create an oracle by copying production output.

## Performance / resource constraints

Record only performance, hardware, scaling, or resource constraints that materially constrain the D2 search space. Keep software implementation detail delegated when possible.

## D2 -> D3 handoff

State the minimum computational semantics architecture must preserve: data/operation dependencies, precision/reproducibility, state/restart semantics affecting the method, error envelope, and material target-resource constraints. Record material dependency links needed for bounded invalidation.

## Supporting derivation, references, and alternatives

Explain derivations and literature, and document alternatives where they materially illuminate the accepted choice without creating competing authority.

## Open challenges

Record unresolved material authority challenges or concise resolved rationale needed to prevent recurrence; do not preserve full review transcripts.