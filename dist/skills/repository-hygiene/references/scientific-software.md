# Scientific and Numerical Software Evidence

This reference provides cross-domain scientific/numerical evidence guidance. It is **not** the semantic owner of the scientific model or numerical method.

- D1 meaning and external adequacy are owned by [Scientific and mathematical formulation](scientific-formulation.md).
- D2 algorithm/error/convergence/precision semantics are owned by [Algorithm and numerical method design](numerical-algorithm-design.md).
- D3 owns software architecture needed to preserve them.
- D4 concretizes and evidences the accepted contracts.

Read [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for evidence specification/realization/observation, applicability, stale-evidence, and impact-closure rules.

Apply these rules when software represents physical, mathematical, statistical, geometry, signal-processing, simulation, or machine-learning (ML) evaluation semantics.

## Background and terminology

An **evidence specification** defines how a claim is interrogated. An **evidence realization** is one concrete execution under identified subject/input/environment conditions. An **observation** is the result, and an **evidence assessment** states what one or more observations can legitimately support/challenge.

A **concretization** is instead a downstream D1-D4 scientific/software expression of a governing abstraction.

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

Use these invariants as evidence specifications in addition to fixture equality. Do not invent an invariant merely because it is convenient to test.

## Equivalence and tolerances

Use exact equality for discrete identities, indices, graph topology, categorical states, and serialization where required.

Use justified absolute/relative tolerances for floating values; choose them from accepted D2 numerical conditioning/precision/error semantics, not merely to make tests pass. Compare final physical/scientific observables after optimizing an intermediate kernel. Preserve deterministic ordering when downstream reproducibility depends on it. Record dtype/backend when numerical differences can arise.

## Reference/oracle strategy

Retain a simple trusted or independently justified implementation when practical, even if slower, to validate optimized backends on bounded fixtures. A reference that substantially duplicates the production defect is not independent evidence.

For randomized scientific evidence realizations:

- seed deterministically where determinism is part of the evidence design;
- save enough failing input/provenance to reproduce;
- include physically difficult geometries/regimes, not only random nominal cases.

A rerun against a changed candidate is a new evidence realization, not a mutation of the prior result.

## Differential and metamorphic validation

When exact fixture outputs are incomplete or the implementation change is substantial, strengthen scientific evidence with independently justified relations.

- **Differential testing:** compare a trusted/reference concretization against an optimized/new/backend concretization on governed observables.
- **Metamorphic testing:** apply an authority-backed transformation and verify the required relation on outputs.

Useful examples include permutation-invariant aggregate statistics, restart/continuation versus uninterrupted equivalence, unit-consistent transformation, valid translation/rotation symmetry or equivariance, normalized-weight rescaling that should preserve ranking, and backend equivalence within justified tolerance.

Do not invent a metamorphic relation merely because it is convenient. It must follow from accepted D1/D2 authority, and tolerance rules remain governed by numerical conditioning and precision.

## Evidence durability and common-mode risk

When evidentiary strength is equivalent, prefer specifications tied to durable scientific/numerical properties over incidental implementation detail. This does not let high-level evidence substitute for required D2/D4 conformance.

For important/high-risk claims, use independently justified evidence routes when they materially reduce common-mode risk. Multiple tests that share one reference implementation, dataset defect, fixture, expected-value generator, or mistaken assumption do not become independent merely because they execute separately.

A passing stale result is not current confirmation; a failing stale result is not current refutation. Review applicability after changes to the governed claim, candidate, regime, oracle, backend/precision/configuration, stochastic replicate, or other material dimension.

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

Record material choices needed to reproduce or interpret an evidence realization/result:

- subject/candidate and input/source identity;
- evidence specification/oracle revision where material;
- normalization/preprocessing;
- algorithm/backend and policy resolution;
- random seeds/replicate identity;
- precision/dtype;
- model/checkpoint/schema versions;
- numerical tolerances and cutoffs;
- fallback events;
- cache/checkpoint identity and source-data lineage when derived state is reused;
- relevant resource/execution configuration when it can affect result or interpretation.

Diagnostics should be observational and should not influence scientific ordering or outcomes unless that behavior is explicitly governed.

## ML, stochastic, and accelerator-specific rules

- Separate model/scientific identity from execution optimization when possible.
- Validate checkpoint/schema compatibility explicitly.
- Compare accelerated/fused/mixed-precision execution against an accepted reference on representative data under D2 equivalence/error rules.
- Treat training stochasticity separately from deterministic inference/evaluation equivalence.
- Do not claim graphics-processing-unit (GPU) qualification from central-processing-unit (CPU)-only tests; mark target-hardware qualification blocked/deferred until actually run.
- GPU availability does not authorize accelerator semantics when D3 architecture does not support them.

## Impact closure after scientific/numerical change

When D1/D2 authority or a material concretization changes, identify materially dependent evidence specifications/realizations and preserve unaffected evidence. Remap/rerun evidence whose execution owner changed; retire or revise evidence whose oracle/target proposition became obsolete. Reconcile documentation/current dependency views and semantic-evolution history when triggered.

A partial dependency map is not proof of non-impact merely because an edge is absent.

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
