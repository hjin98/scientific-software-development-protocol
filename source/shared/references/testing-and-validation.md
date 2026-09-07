# Testing and Validation

Testing exists to establish product behavior and engineering claims with appropriate confidence. It is not a parallel product or approval bureaucracy, and it does not by itself establish that every accepted implementation obligation was performed.

## Product truth and acceptance integrity

Tests, metrics, gates, benchmarks, and reports are measurement instruments for engineering claims; they are not the product objective. Passing evidence is useful only when it honestly establishes the accepted product behavior it purports to measure.

Do not create acceptance by manipulating the measurement surface instead of correcting or legitimately redefining the product. Without an accepted product-semantic change or proof that the old test itself was wrong, it is invalid to make a required affected check pass by deleting/weakening its assertion, removing known failing inputs from its fixture population, copying buggy implementation output into expected values, converting a required failure/exception into warning/success, skipping or making a required check optional, relaxing a material threshold merely because it failed, adding product fallbacks solely for test scaffolding, or rewriting specification/documentation to bless an unintended implementation.

Test, fixture, threshold, and specification changes remain legitimate when the authoritative product contract genuinely changed, the previous expectation is independently shown incorrect, or a more representative/better test preserves or strengthens the same claim. The justification must be product-semantic rather than merely that the old check was inconvenient or red.

For material completion claims, apply a bounded independent-evaluator counterfactual: if the visible acceptance harness were replaced by an independent expert evaluation of the same accepted stakeholder outcome and engineering envelope, would the candidate still deserve to pass? If materially no, local green evidence is insufficient. This is a reasoning safeguard, not a mandate for hidden tests, mutation testing, or new evaluator infrastructure.

## Oracle strength, counterfactuals, and mutation evidence

Coverage and green execution do not establish that a test can reject materially wrong behavior. For important decision logic, boundary-heavy changed code, historically escaped defects, high-risk hotspots, or suspiciously weak assertions, ask what smallest plausible semantically wrong implementation could still pass the current tests.

When that counterexample is material and economical to test, strengthen the oracle through an appropriate method: mutation testing or equivalent semantic perturbation, a known-broken/corrected counterfactual, property/stateful testing, differential comparison, metamorphic relations, or real-owner integration. Mutation survival is investigation evidence, not a universal failure score: equivalent/dead mutants, ambiguous requirements, and intentionally unobserved behavior must be interpreted semantically. Do not require 100% mutation scores or run mutation testing on every task.

Use **differential testing** when independently justified implementations/backends should agree on governed observables. Use **metamorphic testing** when an authority-backed transformation implies a relation on outputs even when a complete fixture oracle is difficult. The relation must come from product/scientific authority, not from convenience.

## Functional acceptance for executable changes

Every executable product change requires:

1. **Focused checks** appropriate to new/modified mechanisms: unit, property, numerical, boundary, error, or bug-reproducer tests.
2. **Affected-surface regression** covering all new/modified behavior and every existing behavior that could plausibly change because of the revision.
3. **Integration testing** through the assembled affected product path and relevant real consumer/interface/state-transition boundaries.

The affected surface is not limited to changed files. Include callers/consumers, shared utilities, public interfaces, configuration, persistence, caches/checkpoints, orchestration/concurrency paths, packaging/entry points, documentation/contracts, and transitive behavioral dependencies where the change can plausibly propagate.

Do not require one test per function/file. Existing tests count when they genuinely protect the relevant contract; add coverage where they do not.

Repository/project-required checks remain mandatory. If impact analysis cannot confidently bound the affected surface, run the broader/full available regression suite rather than treating unexamined consumers as unaffected.

A required check that did not execute is not a pass. Newly introduced failures and failures plausibly intersecting the affected surface block functional acceptance. Demonstrably pre-existing unrelated failures may be attributed and reported rather than repaired.

## Conformance and testing are complementary

For work governed by an accepted implementation contract, functional evidence and semantic/workplan conformance answer different questions:

- conformance establishes that the required obligations, protected concerns, and frozen decisions were actually realized or legitimately reconciled;
- testing establishes that the resulting behavior works across the required affected surface.

Green tests do not prove an omitted obligation was implemented. Source/conformance inspection does not replace executable regression/integration.

For removal, uniqueness, ownership, or no-legacy-path claims, use structural/source inspection or negative/absence assertions when runtime tests cannot establish the claim directly.

## Proxy-proof acceptance and test-double boundaries

For a material integration or acceptance claim, identify the **semantic owner under acceptance for the current realization**: the production component, state machine, consumer, validator, persistence mechanism, compatibility/migration path, authorization layer, orchestrator, or decision-maker whose real behavior materially constitutes the claim. The authoritative acceptance boundary is the product/Frozen claim plus execution of its actual production owner; a lower-level Tier-2 owner does **not** become Frozen merely because a workplan or test names it. If delegated owner `A` is legitimately replaced by equivalent owner `B` while product/Frozen semantics survive, invalidate/reconcile `A`-specific evidence and establish the same claim through real owner `B`. This is local reconciliation, not proxy-passing. Exact owner/path identity is binding only when that identity is itself a governed product contract or explicitly Frozen high-level architecture.

An **allowed test-double boundary** lies below or outside that semantic owner. A dependency there may be replaced to bound cost, hardware, external services, data volume, or nondeterminism while the owner's real decision/control/state-transition path still executes. **Proxy-proof acceptance** means that a material defect in the required semantic owner would cause the evidence for that owner claim to fail.

An integration or acceptance test does not establish a production-owner claim if it mocks, stubs, monkeypatches, precomputes, substantially reimplements, or bypasses the owner whose behavior is under acceptance. In particular, evidence is insufficient for the corresponding owner claim when it:

- patches the owner to return the desired result;
- directly invokes a downstream helper when production caller/orchestrator/restart/reconciliation/authorization detection is part of the claim;
- seeds post-decision or post-transition state and skips the required production transition;
- replaces durable/project persistence with a custom or in-memory substitute when persistence, restart, or recovery semantics are the claim;
- reimplements production compatibility, migration, identity, scheduling, authorization, or orchestration logic in the harness;
- proves only a helper-produced plan/result when assembled real-consumer behavior is the claim.

This is **not a global ban on mocks or fakes**. Bounded deterministic fixtures remain preferred. Expensive ML/scientific training or prediction, accelerator execution, reduced scientific data, external services, network calls, and other costly dependencies may be faked or reduced when they lie below/outside the required real boundary. The generic requirement is boundary fidelity, not production-scale execution.

Before relying on material acceptance evidence, ask the counterfactual: **could this evidence remain green while the real semantic owner of the accepted current realization is materially broken?** If yes, that evidence cannot close the owner claim. A direct helper call cannot prove that its production caller detects the condition and invokes it correctly. After a legitimate delegated-owner replacement, old owner-specific evidence is stale for the remapped claim even if it remains green.

When exact real owner/path identity is binding because a governed product contract or explicitly Frozen architecture requires that identity, inability to exercise that boundary is an unavailable/blocking acceptance check or an evidence-backed Design-reopen condition; do not silently downgrade it to a proxy pass. Otherwise, a legitimate delegated-owner replacement must reconcile the acceptance mapping to the new real owner and invalidate/rerun owner-specific evidence rather than preserving the old owner. When the task names forbidden semantic-owner substitutions and a robust inexpensive structural/negative check can prevent recurrence, add that guardrail. Do not require universal AST scanning, mutation testing, one test per function, a global monkeypatch ban, or a new anti-mocking framework merely for protocol compliance.

## Acceptance liveness and family-closure evidence

Proxy-proof acceptance also requires the intended acceptance mechanism to be live. When a material regression depends on a patched seam, failpoint, callback, hook, or similar trigger, establish that the trigger actually fired when practical; a green test that never exercised the intended boundary does not close the claim. When a production transition or decision is the claim, execute its real semantic owner and keep doubles below/outside that boundary.

When cheap and meaningful, demonstrate that a bug reproducer or equivalent counterfactual can distinguish known-broken behavior from corrected behavior. This is not a universal requirement to check out historical commits, run mutation testing, or create one test per source site. For family closure, prefer owner-level properties plus representative material transition/equivalence classes when that provides stronger semantic coverage.

Structural/negative scans complement runtime acceptance. If a structural rule establishes an acceptance-critical absence or bypass claim, validate the rule against representative known-positive and known-negative constructs and state its actual scan scope/limitations; zero findings outside a justified scan contract are not proof of absence.

For normal final independent review, functional review readiness includes exact candidate identity, required stage-local closure, final affected-surface re-derivation, final complete affected-surface regression, real-boundary integration, repository/project-required checks, and task-required structural/absence/liveness evidence on a candidate whose relevant dimensions have not changed afterward. A required check that is missing or did not execute remains incomplete acceptance/implementation nonconformance rather than a pass or an automatic design revision. An explicitly requested review still proceeds and reports the missing evidence; review readiness is not a mechanism for refusing review.

## Optimize test cost, not coverage

Coverage breadth follows the affected behavioral surface. Then minimize execution cost while preserving that coverage.

Prefer small deterministic fixtures, bounded datasets, reduced iterations/epochs, synthetic inputs, and representative workloads when they exercise the same contracts. A broad regression suite can be inexpensive if each path is tested with bounded data.

Do not interpret “small,” “focused,” or “representative” as permission to omit affected modules, consumers, interfaces, or integration boundaries.

## Coherent stage granularity and dual closure

A material implementation stage is a coherent behavior-changing unit. It may include several tightly coupled helper/caller/fixture edits whose behavior is only meaningful as one assembled stage. Do not create a separate stage-local regression gate for every file/function edit unless it independently changes executable behavior or forms a useful risk boundary.

Before dependent implementation proceeds, the stage must achieve both:

1. **semantic/conformance closure** of the obligations assigned to that stage; and
2. **functional closure** — focused checks plus the required affected regression subset for executable behavior.

Use the cheapest high-information order within the stage. Cheap focused checks prevent spending broader test cost on obvious local defects, but do not substitute for the affected regression. Obvious conformance defects may likewise be repaired before test cost is spent.

## Stage-local affected regression

After **each material implementation stage that changes executable behavior**, run focused checks and the required **stage-local affected regression** subset relevant to that stage before dependent implementation proceeds. Resolve newly introduced hard failures and affected regressions at the stage that introduced them.

A tiny atomic change may use the final pass as its stage pass. A genuinely non-executable intermediate stage may combine validation with the nearest executable integration stage when that dependency is explicit. Do not defer all regression to final completion merely because a later suite will eventually exercise the code.

This requirement preserves fault localization and prevents defect accumulation; it is not optional based only on whether an agent predicts that intermediate testing will be useful.

## Evidence reuse and invalidation

Reuse still-valid intermediate evidence instead of rerunning it merely because time passed, a new agent session began, or unrelated files changed.

Rerun a check when a changed dimension can plausibly alter the result or interpretation. Examples:

- documentation-only wording does not invalidate an unrelated numerical regression result;
- executable refactoring invalidates regression evidence for behavior that could be affected;
- serialization changes invalidate relevant persistence/compatibility evidence but not an unrelated mathematical oracle;
- GPU execution-policy changes invalidate affected GPU equivalence/performance evidence without automatically invalidating an unchanged CPU reference result.

Evidence reuse is an intermediate development-economy optimization. It never removes final assembled acceptance requirements and never turns an unexecuted required check into a pass.

## Changed-code and affected-surface quality ratchets

When project tooling makes the evidence cheap and stable, prefer changed-code/affected-surface ratchets over arbitrary whole-repository thresholds. Material questions include whether new/modified important behavior is behaviorally protected, whether the change introduced an objective architecture violation or dependency cycle, whether it created an unjustified complexity hotspot/public/configuration expansion, and whether an important oracle became weaker.

Changed-line/diff coverage, complexity, duplication, mutation effectiveness, and similar observations are sensors. They trigger semantic investigation and become hard thresholds only when project/task authority explicitly adopts them. Existing debt does not authorize worsening touched code without product/Frozen justification.

## Final assembled acceptance

Before functional completion:

1. implementation first completes final accepted-contract reconciliation and accounts for material structural/absence claims;
2. re-derive the affected behavioral surface from the final assembled implementation;
3. account for every identified affected path with executed regression coverage, a required broader suite, or an explicit unavailable/blocking check;
4. rerun the complete affected-surface regression after all material executable edits that could invalidate earlier evidence;
5. run integration/end-to-end tests through the assembled affected product path on the same candidate.

Implementation can broaden impact beyond the initial plan, so initial impact analysis is not sufficient final evidence.

## Prefer direct testing

Test through the actual implementation/product path whenever practical. A harness must not substantially reimplement the algorithm, state reconstruction, orchestration, compatibility logic, or other semantic owner it is intended to test.

Synthetic fixtures are useful for bounded execution; they do not replace real integration boundaries when those boundaries are part of the functional claim. Fakes below or outside the accepted semantic-owner boundary remain valid bounded-test tools.

## Production qualification

Full production qualification is distinct from functional testing. It assumes regression and integration acceptance already passed and uses real, long, data-heavy, target-machine/target-hardware workloads to characterize production-scale wall time/throughput, RAM/VRAM/storage/I/O, scaling, accelerator utilization, recovery cost, and related environment-specific behavior.

Do not run full production qualification by default during implementation or between ordinary stages. Run it only when explicitly requested, required by project/release policy, or necessary to establish a material production-scale/resource/performance/hardware claim.

Bounded benchmarks, accelerator smoke tests, reference-equivalence checks, and representative resource checks remain normal implementation validation when relevant.

A successful production run never substitutes for missing focused/regression/integration coverage. Bounded functional testing does not prove production-scale performance/resource qualification.

## Bounded failure injection for recovery claims

For persistence, restart, orchestration, cancellation, or failure-propagation claims, use deterministic bounded failure injection or equivalent controlled simulation when it materially strengthens the evidence. Representative cases include interrupted checkpoint publication, truncated artifacts, stale/missing cache state, restart at material boundaries, controlled worker/task death, controlled I/O failure, duplicate callback/event delivery, and partial transition state.

Keep the real semantic recovery/state owner live and place doubles/failpoints below or outside that owner. A harness that reimplements recovery logic cannot prove the production owner. Prefer bounded simulation over actual resource exhaustion or indiscriminate chaos, and establish failpoint/trigger liveness when practical. Fault injection is conditional on the claim; it is not a universal test stage.

## Resource safety

Honor explicit CPU/RAM/VRAM/storage/I/O/wall-time constraints. Do not exhaust the machine to prove basic functionality. Use bounded failure simulations rather than actual resource exhaustion when they establish the same behavior.

## Domain-specific tests

Security, persistence/recovery, concurrency, configuration, scientific/numerical, performance, packaging, and other specialized test guidance augments this protocol-wide regression/integration contract; it does not replace it.

## Evidence

Command output, CI results, benchmark output, source inspection, or run logs are normally sufficient evidence. Record only metadata needed to interpret the material claim. Do not create qualification/evidence machinery merely for ceremony.
