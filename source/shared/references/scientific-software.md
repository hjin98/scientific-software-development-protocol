# Scientific and Numerical Software Evidence

This reference provides cross-domain scientific/numerical evidence guidance. It is **not** the semantic owner of the scientific model or numerical method.

- D1 meaning and external adequacy are owned by [Scientific and mathematical formulation](scientific-formulation.md).
- D2 algorithm/error/convergence/precision semantics are owned by [Algorithm and numerical method design](numerical-algorithm-design.md).
- D3 owns software architecture needed to preserve them.
- D4 implements and evidences the accepted contracts.

## Conventions and units

State coordinate/cell/vector conventions, units, signs, indexing, periodicity, tensor ordering, normalization, estimator/sample semantics, and precision at the owning authority level when ambiguity can change results. Convert at explicit D4 boundaries and preserve one canonical internal convention where feasible.

Units and frame meanings are semantic data, not comments. Never fabricate missing physical data; represent unavailable quantities explicitly.

## Authority-backed invariants

Tests and diagnostics should derive from accepted D1/D2 authority, for example:

- symmetry/antisymmetry or equivariance;
- conservation/normalization;
- periodic/basis invariance;
- positivity/finite/bounded behavior;
- deterministic canonical ordering where governed;
- exact integer/image/topological identities;
- monotonicity;
- estimator/sample semantics;
- restart/continuation equivalence when method authority requires it.

Do not invent an invariant solely because it is easy to test.

## Exactness and tolerance

Use exact equality for exact discrete identities and contracts. Floating/statistical tolerances must be justified by accepted D2 conditioning/precision/stochastic/error semantics, not chosen after observing a failing backend.

Validate optimized kernels/backends against final governed observables, not only internal intermediates. Record dtype/backend/compiler/device when those dimensions can materially change the result.

## Independent reference and oracle strength

Retain or construct a simple independently justified reference method when its assurance value exceeds maintenance cost. A reference that substantially duplicates the production defect is not independent evidence.

Use differential, metamorphic, property, analytical, manufactured, limiting, convergence/refinement, residual, conditioning, or stochastic evidence according to the governing D2 claim. Ask what smallest plausible wrong realization could still pass the current oracle.

## Approximation and performance

Do not silently trade scientific fidelity for speed. Any material approximation needs accepted ownership of:

- the mathematical/scientific approximation and valid regime;
- the error metric/envelope;
- failure/fallback behavior where applicable;
- user visibility/configuration when governed;
- accuracy evidence separate from performance benefit.

Changing cutoff, resolution, sampling, precision, estimator, convergence criteria, reduction ordering, or restart semantics to improve benchmark numbers is a D1/D2 semantic change when it can alter governed conclusions.

## Provenance and reproducibility

Record only material identity needed to reproduce or interpret results, such as input/source identity, normalization/preprocessing, algorithm/backend policy, seeds, precision/dtype, model/checkpoint/schema version, tolerances/cutoffs, fallback events, cache/checkpoint lineage, and relevant execution configuration.

Diagnostics remain observational; they must not change scientific ordering/outcomes unless that behavior is explicitly part of authority.

## ML, stochastic, and accelerator execution

Separate model/scientific identity from execution optimization where possible. Validate checkpoint/schema compatibility. Compare accelerated/fused/mixed-precision execution with the accepted reference under D2 equivalence/error rules; do not widen tolerance merely to accept a device backend.

Training stochasticity is distinct from deterministic inference/evaluation equivalence. CPU-only checks do not establish GPU qualification, and GPU availability does not authorize accelerator semantics when D3 architecture does not support them.

## Composed closure

For material scientific claims, local green checks can miss an omitted intermediate invariant. Trace:

```text
actual executable observables
 -> D2 algorithm/error/equivalence envelope
 -> D1 meaning
 -> external adequacy/validation/proof/standards evidence as applicable
```

This composed closure is risk-triggered, not mandatory ceremony for every software change.