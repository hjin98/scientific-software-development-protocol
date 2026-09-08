# Scientific and Numerical Software Evidence

This reference provides cross-domain scientific/numerical evidence guidance. It is **not** the semantic owner of the scientific model or numerical method.

- D1 meaning and external adequacy are owned by [Scientific and mathematical formulation](scientific-formulation.md).
- D2 algorithm/error/convergence/precision semantics are owned by [Algorithm and numerical method design](numerical-algorithm-design.md).
- D3 owns software architecture needed to preserve them.
- D4 implements and evidences the accepted contracts.

Apply these rules when software represents physical, mathematical, statistical, geometry, signal-processing, simulation, or ML-evaluation semantics.

## Conventions and units

State coordinate/cell/vector conventions, units, signs, indexing, periodicity, tensor ordering, normalization, estimator/sample semantics, and precision at the owning authority level when ambiguity can change results. Convert at explicit D4 boundaries and preserve one canonical internal convention where feasible.

Units and frame meanings are semantic data, not comments. Never fabricate missing physical data; represent unavailable quantities explicitly.

## Authority-backed numerical invariants

Identify governing invariants before optimization or backend changes, such as:

- symmetry or antisymmetry;
- conservation/normalization;
- periodic or basis invariance;
- positive/finite constraints;
- deterministic canonical ordering;
- exact integer/image identities;
- monotonic or bounded quantities;
- estimator/sample semantics;
- restart/continuation equivalence when method authority requires it.

Use these invariants as tests in addition to fixture equality. Do not invent an invariant merely because it is convenient to test.

## Equivalence and tolerances

Use exact equality for discrete identities, indices, graph topology, categorical states, and serialization where required.

Use justified absolute/relative tolerances for floating values; choose them from accepted D2 numerical conditioning/precision/error semantics, not merely to make tests pass. Compare final physical/scientific observables after optimizing an intermediate kernel. Preserve deterministic ordering when downstream reproducibility depends on it. Record dtype/backend when numerical differences can arise.

## Reference/oracle strategy

Retain a simple trusted or independently justified implementation when practical, even if slower, to validate optimized backends on bounded fixtures. A reference that substantially duplicates the production defect is not independent evidence.

For randomized scientific tests:

- seed deterministically;
- save enough failing input/provenance to reproduce;
- include physically difficult geometries/regimes, not only random nominal cases.

## Differential and metamorphic validation

When exact fixture outputs are incomplete or the implementation change is substantial, strengthen scientific evidence with independently justified relations.

- **Differential testing:** compare a trusted/reference implementation against an optimized/new/backend realization on governed observables.
- **Metamorphic testing:** apply an authority-backed transformation and verify the required relation on outputs.

Useful examples include **permutation**-invariant aggregate statistics, **restart**/continuation versus uninterrupted equivalence, unit-consistent transformation, valid translation/rotation **symmetry** or equivariance, normalized-weight rescaling that should preserve ranking, and **backend** equivalence within justified tolerance.

Do not invent a metamorphic relation merely because it is convenient. It must follow from accepted D1/D2 authority, and tolerance rules remain governed by numerical conditioning and precision.

## Approximation and resolution

Do not silently trade scientific fidelity for speed.

Any material approximation must define, through its owning authority:

- mathematical/physical approximation;
- valid regime;
- error metric/tolerance;
- failure or fallback behavior;
- user visibility/configuration when governed;
- benchmark benefit separately from accuracy evidence.

Do not tune scientific resolution, cutoff, sampling, precision, estimator, convergence criteria, reduction ordering, or restart semantics solely to improve benchmark numbers unless the owning D1/D2 authority explicitly accepts the changed semantics.

## Provenance and reproducibility

Record material choices needed to reproduce or interpret results:

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

Diagnostics should be observational and should not influence scientific ordering or outcomes unless that behavior is explicitly governed.

## ML, stochastic, and accelerator-specific rules

- Separate model/scientific identity from execution optimization when possible.
- Validate checkpoint/schema compatibility explicitly.
- Compare accelerated/fused/mixed-precision execution against an accepted reference on representative data under D2 equivalence/error rules.
- Treat training stochasticity separately from deterministic inference/evaluation equivalence.
- Do not claim GPU qualification from CPU-only tests; mark target-hardware qualification blocked/deferred until actually run.
- GPU availability does not authorize accelerator semantics when D3 architecture does not support them.

## Composed closure

For material scientific claims, local green checks can miss an omitted intermediate invariant. Trace:

```text
actual D4 executable behavior
 -> final governed numerical observables
 -> D2 error/equivalence/uncertainty envelope
 -> D1 scientific/mathematical meaning
 -> problem-appropriate external adequacy / validation / proof / standards evidence
```

This composed closure is risk-triggered, not mandatory ceremony for every software change.
