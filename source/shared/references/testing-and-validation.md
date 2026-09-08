# Testing, Verification, and Validation

Evidence exists to test governed claims; it is not a parallel authority system. Read [Abstraction, realization, authority, and challenge](abstraction-and-realization.md) for the authority model.

## Evidence integrity

Tests, proofs, benchmarks, metrics, reports, literature, and runtime observations are **measurement instruments**, not truth or product objectives. They do not manufacture the claim they measure.

Without an accepted semantic change or independent proof that the prior oracle was wrong, it is invalid to create a pass by **deleting/weakening its assertion**, **removing known failing inputs** from the fixture population, copying **buggy implementation output** into expected values, converting a required failure/exception into **warning/success**, skipping or **making a required check optional**, **relaxing a material threshold** or widening tolerance merely because it failed, adding product fallback solely for test scaffolding, or **rewriting specification/documentation** to bless unintended implementation. The same anti-counterfeit rule applies to method papers and architecture authority.

**Test, fixture, threshold, and specification changes remain legitimate** when their governing authority genuinely changed, the previous expectation is independently shown incorrect, or a stronger oracle preserves the same accepted claim. The justification must be semantic rather than merely that the old check is inconvenient or red.

For material completion claims apply a bounded **independent-evaluator counterfactual**: if the visible acceptance harness were replaced by an independent expert evaluation of the same accepted stakeholder/domain outcome and engineering envelope, would the candidate still deserve to pass? If materially no, local green evidence is insufficient.

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

## Oracle strength, counterfactuals, and mutation evidence

Coverage and green execution do not show that an oracle rejects materially wrong behavior. For important changed logic ask:

> What is the smallest plausible semantically wrong realization that could still pass this evidence?

When material and economical, strengthen the oracle through a known-broken/corrected counterfactual, property/stateful testing, mutation/semantic perturbation, differential comparison, metamorphic relation, reference solution, or real-owner integration.

Mutation survival is investigation evidence, not a universal score. **Do not require 100% mutation** scores or optimize tests for coverage/mutation percentages rather than governed behavior. Mutation/counterfactual work is **not a universal test stage**; use it only when it materially strengthens an important oracle.

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

## Proxy-proof acceptance and allowed test-double boundary

For a material acceptance claim identify the **semantic owner under acceptance**: the real production decision-maker/state transition/persistence boundary/orchestrator/algorithm/consumer path whose behavior constitutes the claim. Then state the **allowed test-double boundary** below or outside that owner.

Apply this counterfactual:

> **Could this evidence remain green** while the semantic owner under acceptance is materially broken?

If yes, it cannot establish **proxy-proof acceptance** and **cannot close the owner claim**.

Historical invalid substitutions include evidence that:

- **mocks, stubs, monkeypatches**, precomputes, or substantially reimplements the semantic owner;
- **directly invokes a downstream helper** when the production caller/orchestrator/restart/reconciliation/authorization detection is part of the claim;
- **seeds post-decision or post-transition state** when the decision/transition is under acceptance;
- **replaces durable/project persistence** with an in-memory substitute when persistence/restart semantics are the claim;
- **reimplements production compatibility**/migration/scheduling/authorization logic in the harness;
- accepts a **helper-produced plan/result** when production construction/routing of that plan/result is the behavior being verified.

This is **not a global ban on mocks or fakes**. **Bounded deterministic fixtures remain preferred** where they establish the claim economically, and bounded test doubles remain valid below or outside the real owner to control external services, hardware, data volume, nondeterminism, and **expensive ML/scientific training or prediction**. Production-scale execution is required only when production-scale behavior/resource qualification is itself the claim.

When an exact owner/path is merely delegated realization, the lower-level Tier-2 owner **does not become Frozen** in historical Protocol 5 vocabulary merely because acceptance named it. Suppose accepted semantics move from delegated owner `A` to equivalent owner `B`: **equivalent owner `B`** is valid when governing authority is unchanged, but owner-specific evidence for `A` is stale. **Reconcile the acceptance mapping to the new real owner** and rerun owner-specific evidence instead of preserving `A` or calling the remap proxy-passing.

If the required real-owner boundary is unavailable, mark the claim **unavailable/blocking** rather than substituting a proxy and declaring a pass.

When a bypass is easy to regress and the claim is structural, a **robust inexpensive structural/negative check** can protect the boundary. Do **not require universal AST scanning**, a **global monkeypatch ban**, or a **new anti-mocking framework** merely to police ordinary tests.

## Conformance and structural evidence

Green tests do not prove that every accepted implementation obligation was performed. Semantic/workplan conformance and functional testing answer different questions and both must close.

For **removal, uniqueness, ownership, or no-legacy-path claims**, use **structural/source** inspection or negative/absence assertions when runtime tests cannot establish the claim directly.

## Acceptance liveness and failure injection

When evidence depends on a hook/failpoint/callback/state transition, establish that the trigger actually fired when practical. Green evidence that never exercised the intended boundary is insufficient.

For persistence/restart/orchestration/recovery/failure-propagation claims, use deterministic bounded failure injection where it materially strengthens evidence: interrupted publication, truncated artifact, stale/missing cache, restart at material boundaries, worker/task death, controlled I/O failure, duplicate callback/event, or partial transition state.

Keep the real recovery/state owner executing. Prefer bounded simulation over actual resource exhaustion. Bounded failure injection is conditional on the claim and is **not a universal test stage**.

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

This **composed end-to-end scientific closure** is risk-triggered; do not force it onto a local software refactor with no plausible upstream semantic impact.

## Review readiness and final assembled acceptance

Normal review readiness follows final accepted-contract reconciliation, **final complete affected-surface regression**, real-boundary integration, repository/project-required checks, and task-required structural/liveness evidence on the candidate whose relevant dimensions have not changed afterward. Missing required evidence remains blocking; Review does not move those checks later.

Before implementation completion:

1. reconcile every accepted governing obligation and material structural/absence claim;
2. re-derive the affected behavioral/semantic surface from the final assembled implementation;
3. account for every affected path with executed coverage or an explicit **unavailable/blocking** result;
4. rerun complete affected-surface regression after all material executable edits;
5. run assembled real-boundary integration/end-to-end tests;
6. run repository/project-required build/lint/type/package checks.

A successful production run does not substitute for missing regression/integration.

## Production qualification

Production qualification is distinct from functional acceptance. Use real long/data-heavy/target-hardware workloads only when explicitly required or necessary to establish production-scale wall time, throughput, RAM/VRAM/storage/I/O, scaling, accelerator utilization, or recovery cost. Bounded performance/equivalence/resource checks remain normal implementation evidence when sufficient.

## Resource safety

Honor explicit CPU/RAM/VRAM/storage/I/O/wall-time limits. Do not exhaust the machine merely to prove functionality. Use bounded representative fixtures and controlled failure simulation when they establish the same claim.
