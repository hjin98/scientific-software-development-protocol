# Testing, Verification, and Validation

Evidence exists to test governed claims; it is not a parallel authority system. Read [Abstraction, realization, authority, and challenge](abstraction-and-realization.md) for the authority model.

## Evidence integrity

Tests, proofs, benchmarks, metrics, reports, literature, and runtime observations are instruments. They do not manufacture the claim they measure.

Without an accepted semantic change or independent proof that the prior oracle was wrong, it is invalid to create a pass by deleting/weakening assertions, excluding known failing inputs, copying buggy output into expected values, converting required failure into warning/success, skipping a required check, widening a material tolerance merely because it failed, adding product fallback only for the harness, or rewriting specification/method/architecture to bless unintended behavior.

A test or threshold may change when its governing authority genuinely changed or when the old oracle is independently shown incorrect. The justification must be semantic, not convenience.

## Two closure questions at every abstraction boundary

For a material parent->child handoff establish:

1. **realization fidelity:** actual child semantics satisfy every applicable parent and domain-local governed constraint;
2. **abstraction adequacy:** the child abstraction is strong enough that downstream realization cannot satisfy it while violating material upstream meaning.

Evidence that exercises only a proxy abstraction cannot close an omitted upstream invariant.

Every material acceptance/review boundary includes the bounded Challenge Pass. A defect in a coherent realization is an ordinary blocker. Evidence that accepted authority itself may be contradictory, false, materially ambiguous, inadequate, or unrealizable triggers Serious Challenge/human adjudication rather than oracle manipulation.

## D1 external adequacy is not internal verification

Internal D2/D3/D4 correctness cannot prove that D1 is adequate for its intended world/context. Use problem-appropriate evidence:

- empirical validation / independent observations for empirical science;
- proof, axiomatic consistency, limiting/reference theory for mathematical/theoretical work;
- standards, qualification experiments, safety margins, or stakeholder context for engineering work.

Likewise, good external agreement does not prove the numerical method or code faithfully realizes the accepted formulation.

## D2 numerical verification

Use the cheapest sufficiently strong combination of authority-backed evidence, such as analytical/exact/limiting cases, manufactured solutions, residuals, conservation/invariants, mesh/time-step/order/sample refinement, observed convergence order, Richardson/extrapolation, conditioning/sensitivity, forward/backward error, precision/range/cancellation analysis, trusted reference comparison, differential implementations/backends, stochastic bias/variance/convergence, and seed/backend/precision robustness.

Tolerance comes from accepted numerical/error semantics, not from observing what a backend happens to produce.

## Oracle strength

Coverage and green execution do not show that an oracle rejects materially wrong behavior. For important changed logic ask:

> What is the smallest plausible semantically wrong realization that could still pass this evidence?

When material and economical, strengthen the oracle through a known-broken/corrected counterfactual, property/stateful testing, mutation/semantic perturbation, differential comparison, metamorphic relation, reference solution, or real-owner integration.

Mutation survival is investigation evidence, not a universal score. Do not optimize tests for 100% mutation or coverage rather than governed behavior.

## Differential and metamorphic evidence

Use differential testing only when independently justified realizations should agree on governed observables. Use metamorphic testing only when accepted authority implies the relation. Examples include valid symmetry/equivariance, permutation-invariant aggregate statistics, restart/continuation equivalence, unit-consistent transformations, normalized rescaling that preserves ranking, and reference/backend equivalence within a justified D2 envelope.

Do not invent relations because they are convenient.

## D3 architecture verification

Architecture evidence may include dependency/ownership inspection, structural fitness checks, real state/consumer boundaries, recovery/concurrency/security/resource tests, and configuration/deployment checks. Objective stable rules such as forbidden dependency direction, acyclicity, or uniqueness/absence of a retired owner may be executable. Do not create a universal architecture manifest solely for protocol compliance.

If D4 violates a coherent D3 architecture, repair D4. If D3 itself cannot preserve D2 semantics or simultaneous constraints, challenge D3.

## D4 executable functional acceptance

Every executable product change requires:

1. **focused checks** appropriate to the changed mechanism;
2. **affected-surface regression** covering changed behavior and every existing behavior that could plausibly change;
3. **integration/end-to-end evidence** through the assembled affected product and relevant real consumer/state/interface boundaries.

Affected surface can include callers/consumers, shared utilities, public interfaces, configuration, persistence/restart, caches/checkpoints, orchestration/concurrency, packaging/entrypoints, compatibility, documentation/contracts, and transitive scientific/numerical behavior.

A required check that did not execute is not a pass. If impact cannot be bounded confidently, run the broader/full available suite.

## Stage-local regression

After each material executable behavior-changing stage, run focused checks plus the affected regression subset relevant to that stage before dependent executable work continues. A tiny atomic change may use the final pass as its stage pass. A genuinely non-executable intermediate may combine with the nearest executable stage when that dependency is explicit.

Stage-local evidence improves fault localization; it does not remove final assembled regression.

## Proxy-proof semantic-owner evidence

Identify the real semantic owner of the claim in the current realization. Evidence cannot close that owner claim if it mocks, stubs, monkeypatches, precomputes, substantially reimplements, or bypasses the owner whose behavior constitutes the claim.

Bounded doubles remain valid below or outside the owner to control external services, hardware, data volume, expensive ML/scientific work, or nondeterminism.

Examples of invalid owner proof include:

- patching the production decision-maker to return the expected answer;
- direct helper invocation when caller/orchestrator detection is part of the claim;
- seeding post-transition state when the transition itself is under acceptance;
- replacing persistence with an in-memory substitute when restart/persistence semantics are the claim;
- reimplementing compatibility/migration/scheduling/authorization logic in the harness.

After a legitimate delegated-owner replacement, old owner-specific evidence is stale for that claim and must be remapped to the new real owner.

## Acceptance liveness and failure injection

When evidence depends on a hook/failpoint/callback/state transition, establish that the trigger actually fired when practical. Green evidence that never exercised the intended boundary is insufficient.

For persistence/restart/orchestration/recovery/failure-propagation claims, use deterministic bounded failure injection where it materially strengthens evidence: interrupted publication, truncated artifact, stale/missing cache, restart at material boundaries, worker/task death, controlled I/O failure, duplicate callback/event, or partial transition state.

Keep the real recovery/state owner executing. Prefer bounded simulation over actual resource exhaustion.

## Evidence reuse and invalidation

Reuse evidence until a changed authority/realization/environment dimension can plausibly alter its claim or interpretation. Accepted upstream changes invalidate only dependent evidence. Executable refactors invalidate affected D4 regression; serialization changes invalidate persistence/compatibility evidence; GPU execution-policy changes invalidate GPU equivalence/performance evidence without automatically invalidating an unchanged CPU reference.

Final assembled D4 regression/integration always reflects the candidate after all material executable edits that could affect behavior.

## Changed-code quality ratchets

Complexity, duplication, coverage, mutation, churn, dependency centrality/cycles, and changed-line metrics are sensors. Use them to prioritize semantic inspection and to prevent touched code from becoming harder to reason about without authority-backed need. They become hard thresholds only when project/task authority explicitly adopts them.

## Composed end-to-end scientific closure

For material/high-risk scientific claims, pairwise checks can all pass while an omitted intermediate invariant makes the assembled conclusion wrong. Trace:

```text
actual D4 executable behavior
 -> final governed numerical observables
 -> D2 error/equivalence/uncertainty envelope
 -> D1 scientific/mathematical meaning
 -> external adequacy/validation/proof/standards evidence where applicable
```

This is risk-triggered; do not force it onto a local software refactor with no plausible upstream semantic impact.

## Final assembled acceptance

Before implementation completion:

1. reconcile every accepted governing obligation and material structural/absence claim;
2. re-derive the affected behavioral/semantic surface from the final assembled implementation;
3. account for every affected path with executed coverage or an explicit unavailable blocker;
4. rerun complete affected-surface regression after all material executable edits;
5. run assembled real-boundary integration/end-to-end tests;
6. run repository/project-required build/lint/type/package checks.

A successful production run does not substitute for missing regression/integration.

## Production qualification

Production qualification is distinct from functional acceptance. Use real long/data-heavy/target-hardware workloads only when explicitly required or necessary to establish production-scale wall time, throughput, RAM/VRAM/storage/I/O, scaling, accelerator utilization, or recovery cost. Bounded performance/equivalence/resource checks remain normal implementation evidence when sufficient.

## Resource safety

Honor explicit CPU/RAM/VRAM/storage/I/O/wall-time limits. Do not exhaust the machine merely to prove functionality. Use bounded representative fixtures and controlled failure simulation when they establish the same claim.