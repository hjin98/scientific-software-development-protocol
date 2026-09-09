# Testing, Verification, and Validation

Evidence exists to test governed claims; it is not a parallel authority system. Read [Abstraction, concretization, authority, and challenge](abstraction-and-realization.md) for the authority model and [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for evidence specification/realization/observation, applicability, stale-evidence, dependency, and impact-closure semantics.

## Background and terminology

Under Protocol 6.1:

- an **evidence specification** is the reusable test/experiment/benchmark/proof/check definition;
- an **evidence realization** is one concrete execution of that specification under identified conditions;
- an **observation** is the result produced by the realization;
- an **evidence assessment** interprets one or more observations with respect to a governed claim;
- a **concretization** is a downstream scientific/numerical/architectural/software expression of a governing abstraction.

Do not use a test specification, one execution, and the resulting observation as interchangeable concepts when applicability or historical reuse matters.

## Evidence integrity

Tests, proofs, benchmarks, metrics, reports, literature, and runtime observations are **measurement instruments**, not truth or product objectives. They do not manufacture the claim they measure.

Without an accepted semantic change or independent proof that the prior oracle was wrong, it is invalid to create a pass by **deleting/weakening its assertion**, **removing known failing inputs** from the fixture population, copying **buggy implementation output** into expected values, converting a required failure/exception into **warning/success**, skipping or **making a required check optional**, **relaxing a material threshold** or widening tolerance merely because it failed, adding product fallback solely for test scaffolding, or **rewriting specification/documentation** to bless unintended implementation. The same anti-counterfeit rule applies to method papers and architecture authority.

**Test, fixture, threshold, and specification changes remain legitimate** when their governing authority genuinely changed, the previous expectation is independently shown incorrect, or a stronger oracle preserves the same accepted claim. The justification must be semantic rather than merely that the old check is inconvenient or red.

For material completion claims apply a bounded **independent-evaluator counterfactual**: if the visible acceptance harness were replaced by an independent expert evaluation of the same accepted stakeholder/domain outcome and engineering envelope, would the candidate still deserve to pass? If materially no, local green evidence is insufficient.

## Two closure questions at every abstraction boundary

For a material parent->child handoff establish:

1. **concretization fidelity:** actual child semantics satisfy every applicable parent and domain-local governed constraint;
2. **abstraction adequacy:** the child abstraction is strong enough that downstream concretization cannot satisfy it while violating material upstream meaning.

Evidence that exercises only a proxy abstraction cannot close an omitted upstream invariant.

Every material acceptance/review boundary includes the bounded Challenge Pass. A defect in a coherent concretization is an ordinary blocker. Evidence that accepted authority itself may be contradictory, false, materially ambiguous, inadequate, or impossible to concretize triggers Serious Challenge/human adjudication rather than oracle manipulation.

## Evidence applicability and lifecycle

Evidence has a validity domain. A previous result may remain reusable, require review/rerun, or become stale depending on whether materially relevant dimensions changed.

Projects may encode status locally, but interpretation must distinguish enough states to prevent false closure, including:

- pending/unrealized;
- admissible/valid for the current claim and regime;
- review-required;
- inconclusive;
- challenged;
- stale/inapplicable;
- rejected/invalid;
- retired/historical.

Core rule:

> A valid failing observation is evidence. A stale failing observation is not admissible evidence against current authority. A stale passing observation is not admissible confirmation of current authority.

`stale` means the previous specification/realization/subject mapping cannot currently support or refute the target claim without review, rerun, or remapping. It does not by itself prove the claim false. Use `review-required` when applicability is uncertain rather than known inapplicable.

A PASS/accepted/closed claim may not depend on stale, rejected, unavailable-required, or otherwise inadmissible evidence.

Where material, enough provenance must be recoverable to determine applicability across the relevant combination of evidence-specification revision, subject/candidate revision, governed-claim revision, input/validity regime, oracle semantics, environment/backend/precision/configuration, stochastic seed/replicate identity, and protocol obligation. Native continuous-integration (CI), test, benchmark, and experiment artifacts are sufficient when they already establish this identity; do not manufacture a universal evidence manifest.

A rerun against a changed candidate creates a new evidence realization. It does not mutate an old result into evidence for the new candidate.

## Evidence target versus execution dependency

Keep separate:

- **evidentiary target** — the proposition/invariant the evidence specification evaluates;
- **execution dependency** — the implementation, harness, fixture, dataset, environment, backend, tool, or other machinery needed to realize and interpret the evidence.

A test may evidence a D1/D2 invariant while executing through a replaceable D4 concretization. Replacing that D4 concretization may leave the specification valid and require only rerun/remapping; a concretization-specific oracle may instead become stale. Follow the actual dependency and applicability rather than file proximity.

## Evidence durability, sufficiency, and independence

When evidentiary strength is equivalent, prefer specifications coupled to durable governed invariants over replaceable concretization detail:

```text
scientific/mathematical invariant evidence
 > algorithm/numerical property evidence
 > behavioral/architectural contract evidence
 > concretization-specific evidence
```

This is a durability preference, not a substitution hierarchy. D1 evidence does not replace required D2 verification; D1/D2 invariant evidence does not replace required D4 conformance/integration; a low-level unit test does not establish scientific adequacy.

For important/high-risk claims, use more than one independently justified evidence route when that materially reduces common-mode risk. Multiple tests sharing one expected-value generator, reference implementation, defective dataset, fixture, or mistaken assumption are not independent merely because they are separate functions.

An evidence assessment may aggregate several realizations/observations for replication, stochastic/statistical interpretation, convergence, cross-backend comparison, or independent evidence routes. Do not suppress contradictory admissible observations to manufacture a pass.

## D1 external adequacy is not internal verification

Internal D2/D3/D4 correctness cannot prove that D1 is adequate for its intended world/context. Use problem-appropriate evidence:

- empirical validation / independent observations for empirical science;
- proof, axiomatic consistency, limiting/reference theory for mathematical/theoretical work;
- standards, qualification experiments, safety margins, or stakeholder context for engineering work.

Likewise, good external agreement does not prove that the numerical method or code faithfully concretizes the accepted formulation.

## D2 numerical verification

Use the cheapest sufficiently strong combination of authority-backed evidence, such as analytical/exact/limiting cases, manufactured solutions, residuals, conservation/invariants, mesh/time-step/order/sample refinement, observed convergence order, Richardson/extrapolation, conditioning/sensitivity, forward/backward error, precision/range/cancellation analysis, trusted reference comparison, differential implementations/backends, stochastic bias/variance/convergence, and seed/backend/precision robustness.

Tolerance comes from accepted numerical/error semantics, not from observing what a backend happens to produce.

## Oracle strength, counterfactuals, and mutation evidence

Coverage and green execution do not show that an oracle rejects materially wrong behavior. For important changed logic ask:

> What is the smallest plausible semantically wrong concretization that could still pass this evidence?

When material and economical, strengthen the oracle through a known-broken/corrected counterfactual, property/stateful testing, mutation/semantic perturbation, differential comparison, metamorphic relation, reference solution, or real-owner integration.

Mutation survival is investigation evidence, not a universal score. **Do not require 100% mutation** scores or optimize tests for coverage/mutation percentages rather than governed behavior. Mutation/counterfactual work is **not a universal test stage**; use it only when it materially strengthens an important oracle.

## Differential and metamorphic evidence

Use differential testing only when independently justified concretizations should agree on governed observables. Use metamorphic testing only when accepted authority implies the relation. Examples include valid symmetry/equivariance, permutation-invariant aggregate statistics, restart/continuation equivalence, unit-consistent transformations, normalized rescaling that preserves ranking, and reference/backend equivalence within a justified D2 envelope.

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

For a material acceptance claim identify the **real semantic owner**—the real production decision-maker/state transition/persistence boundary/orchestrator/algorithm/consumer path whose behavior constitutes the claim. Then state the **allowed test-double boundary** below or outside that owner.

Apply this counterfactual:

> **Could this evidence remain green** while the semantic owner under acceptance is materially broken?

If yes, it cannot establish **proxy-proof acceptance** and cannot close the owner claim.

Historical invalid substitutions include evidence that:

- **mocks, stubs, monkeypatches**, precomputes, or substantially reimplements the semantic owner;
- **directly invokes a downstream helper** when the production caller/orchestrator/restart/reconciliation/authorization detection is part of the claim;
- **seeds post-decision or post-transition state** when the decision/transition is under acceptance;
- **replaces durable/project persistence** with an in-memory substitute when persistence/restart semantics are the claim;
- **reimplements production compatibility**/migration/scheduling/authorization logic in the harness;
- accepts a **helper-produced plan/result** when production construction/routing of that plan/result is the behavior being verified.

This is **not a global ban on mocks or fakes**. **Bounded deterministic fixtures remain preferred** where they establish the claim economically, and bounded test doubles remain valid below or outside the real owner to control external services, hardware, data volume, nondeterminism, and expensive machine-learning/scientific training or prediction. Production-scale execution is required only when production-scale behavior/resource qualification is itself the claim.

When an exact owner/path is a delegated concretization, acceptance does **not** make that lower-level owner durable authority. If accepted semantics move from delegated owner `A` to equivalent owner `B`, owner-specific evidence for `A` becomes stale. Reconcile the acceptance mapping to the new real owner and rerun owner-specific evidence instead of preserving `A` or calling the remap proxy-passing.

If the required real-owner boundary is unavailable, mark the claim **unavailable/blocking** rather than substituting a proxy and declaring a pass.

When a bypass is easy to regress and the claim is structural, a **robust inexpensive structural/negative check** can protect the boundary. Do not require universal abstract-syntax-tree (AST) scanning, a global monkeypatch ban, or a new anti-mocking framework merely to police ordinary tests.

## Conformance and structural evidence

Green tests do not prove that every accepted implementation obligation was performed. Semantic/workplan conformance and functional testing answer different questions and both must close.

For **removal, uniqueness, ownership, or no-legacy-path claims**, use **structural/source** inspection or negative/absence assertions when runtime tests cannot establish the claim directly.

## Acceptance liveness and failure injection

When evidence depends on a hook/failpoint/callback/state transition, establish that the trigger actually fired when practical. Green evidence that never exercised the intended boundary is insufficient.

For persistence/restart/orchestration/recovery/failure-propagation claims, use deterministic bounded failure injection where it materially strengthens evidence: interrupted publication, truncated artifact, stale/missing cache, restart at material boundaries, worker/task death, controlled input/output (I/O) failure, duplicate callback/event, or partial transition state.

Keep the **real semantic owner** of recovery/state behavior executing. Prefer bounded simulation over actual resource exhaustion. Bounded failure injection is conditional on the claim and is **not a universal test stage**.

## Evidence reuse and invalidation

Reuse evidence until a changed authority/concretization/evidence-specification/environment dimension can plausibly alter its claim or interpretation. Accepted upstream changes invalidate only materially dependent evidence. Executable refactors invalidate affected D4 regression; serialization changes invalidate persistence/compatibility evidence; graphics-processing-unit (GPU) execution-policy changes invalidate GPU equivalence/performance evidence without automatically invalidating an unchanged central-processing-unit (CPU) reference.

Final assembled D4 regression/integration always reflects the candidate after all material executable edits that could affect behavior.

When an accepted authority or material concretization changes, perform bounded impact closure over affected descendants, evidence specifications/realizations, documentation/dependency views, human re-ratification where applicable, revalidation/retirement, and semantic-evolution history. Preserve unaffected siblings and still-valid evidence. Old green tests are never a substitute for impact closure.

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

Normal review readiness follows final accepted-contract reconciliation, **final complete affected-surface regression**, real-boundary integration, repository/project-required checks, task-required structural/liveness evidence, and bounded impact closure for material authority/concretization changes on the candidate whose relevant dimensions have not changed afterward. Missing required evidence remains blocking; Review does not move those checks later.

Before implementation completion:

1. reconcile every accepted governing obligation and material structural/absence claim;
2. re-derive the affected behavioral/semantic surface from the final assembled implementation;
3. account for every affected path with executed coverage or an explicit **unavailable/blocking** result;
4. rerun complete affected-surface regression after all material executable edits;
5. run assembled real-boundary integration/end-to-end tests;
6. run repository/project-required build/lint/type/package checks;
7. resolve or explicitly block every material evidence/dependency impact item.

A successful production run does not substitute for missing regression/integration.

## Production qualification

Production qualification is distinct from functional acceptance. Use real long/data-heavy/target-hardware workloads only when explicitly required or necessary to establish production-scale wall time, throughput, random-access memory (RAM), video random-access memory (VRAM), storage/I/O, scaling, accelerator utilization, or recovery cost. Bounded performance/equivalence/resource checks remain normal implementation evidence when sufficient.

## Resource safety

Honor explicit CPU/RAM/VRAM/storage/I/O/wall-time limits. Do not exhaust the machine merely to prove functionality. Use bounded representative fixtures and controlled failure simulation when they establish the same claim.
