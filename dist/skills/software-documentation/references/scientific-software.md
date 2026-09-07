# Scientific and Numerical Software Requirements

Apply these rules when code represents physical, mathematical, statistical, geometry, signal-processing, simulation, or ML-evaluation semantics.

## Conventions and units

- State coordinate/cell/vector convention, units, sign convention, indexing, periodicity, tensor ordering, normalization, and precision where ambiguity can change results.
- Convert at explicit boundaries; keep one canonical internal convention where feasible.
- Treat units and frame semantics as part of the data contract, not comments.
- Never fabricate missing physical data. Represent unavailable quantities explicitly.

## Numerical invariants

Identify invariants before optimization or backend changes, such as:

- symmetry or antisymmetry;
- conservation/normalization;
- periodic or basis invariance;
- positive/finite constraints;
- deterministic canonical ordering;
- exact integer/image identities;
- monotonic or bounded quantities;
- estimator/sample semantics.

Use these invariants as tests in addition to fixture equality.

## Equivalence and tolerances

- Use exact equality for discrete identities, indices, graph topology, categorical states, and serialization where required.
- Use justified absolute/relative tolerances for floating values; choose them from numerical conditioning/precision, not merely to make tests pass.
- Compare final physical/scientific observables after optimizing an intermediate kernel.
- Preserve deterministic ordering if downstream code or reproducibility depends on it.
- Record dtype/backend when numerical differences can arise.

## Reference/oracle strategy

Retain a simple trusted implementation when practical, even if slower, to validate optimized backends on bounded fixtures. A dense/direct/reference path is often valuable as a permanent oracle and fallback.

For randomized scientific tests:

- seed deterministically;
- save enough failing input/provenance to reproduce;
- include physically difficult geometries/regimes, not only random nominal cases.

## Differential and metamorphic validation

When exact fixture outputs are incomplete or implementation change is substantial, strengthen scientific evidence with independently justified relations.

- **Differential testing:** compare a trusted/reference implementation against an optimized/new/backend realization on governed observables.
- **Metamorphic testing:** apply an authority-backed transformation and verify the required relation on outputs.

Useful examples include permutation-invariant aggregate statistics, restart/continuation versus uninterrupted equivalence, unit-consistent transformation, valid translation/rotation symmetry or equivariance, normalized-weight rescaling that should preserve ranking, and backend equivalence within justified tolerance.

Do not invent a metamorphic relation merely because it is convenient. It must follow from the scientific/product contract, and tolerance rules remain governed by numerical conditioning and precision.

## Approximation and resolution

Do not silently trade scientific fidelity for speed.

Any approximation must define:

- mathematical/physical approximation;
- valid regime;
- error metric/tolerance;
- failure or fallback behavior;
- user visibility/configuration;
- benchmark benefit separately from accuracy evidence.

Do not tune scientific resolution, cutoff, sampling, precision, estimator, or convergence criteria solely to improve benchmark numbers unless explicitly approved.

## Provenance and reproducibility

Record material choices needed to reproduce results:

- input/source identity;
- normalization/preprocessing;
- algorithm/backend and policy resolution;
- random seeds;
- precision/dtype;
- model/checkpoint/schema versions;
- numerical tolerances and cutoffs;
- fallback events;
- cache/checkpoint identity and source-data lineage when derived state is reused;
- relevant resource/execution configuration when it can affect result or performance.

Diagnostics should be observational and should not influence scientific ordering or outcomes.

## ML and accelerator-specific rules

- Separate model/scientific identity from execution optimization when possible.
- Validate checkpoint/schema compatibility explicitly.
- Compare accelerated/fused/mixed-precision execution against an accepted reference on representative data.
- Treat training stochasticity separately from deterministic inference/evaluation equivalence.
- Do not claim GPU qualification from CPU-only tests; mark target-hardware qualification blocked/deferred until actually run.
