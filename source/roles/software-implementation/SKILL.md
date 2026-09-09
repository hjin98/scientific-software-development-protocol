---
name: software-implementation
description: Implement, refactor, test, package, and validate D4 software concretizations under Protocol 6.1 while preserving applicable D1/D2/D3 authority, accepted D4 specification, affected-surface regression/integration, evidence applicability, and upward challenge routing.
---

# Software Implementation

Own executable D4 concretization. Implement the accepted D4 specification and D3 architecture while satisfying every applicable upstream D1/D2 semantic invariant and domain-local governed constraint.

## Engineering stewardship boundary

The stakeholder's **durable software product** and its accepted D1-D4 semantics are the objective. Workplans, tests, metrics, wrappers, helpers, current code, and implementation process are evidence or concretization machinery; they are **not the objective**. Interpret accepted requirements according to their protected engineering purpose. Truthful non-closure is preferable to counterfeit completion, but continue self-correction while a reasonable in-scope engineering path remains.

## Reference routing

Before substantive implementation, **MUST read** [Abstraction, concretization, authority, and challenge](references/abstraction-and-realization.md).

### Role-critical routes

- Before implementing from an accepted workplan, closing a material stage, performing local reconciliation, routing parent invalidation, or resolving material dependency/evidence impact, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md) and [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md).
- Before executable acceptance, affected regression/integration, proxy-proof boundaries, evidence reuse/applicability, oracle strength, or qualification, **MUST read** [Testing and validation](references/testing-and-validation.md).
- Before architecture/ownership/complexity/redesign decisions, **MUST read** [Software architecture and design](references/architecture-and-design.md).
- Before protocol/workplan version binding or historical recovery decisions, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).
- Before changed-code quality, maintainability/test-effectiveness, recovery/failure-path, or structural-risk reasoning, **MUST read** [Long-horizon code health](references/long-horizon-code-health.md).

### Upstream semantic routes

- When implementation can alter scientific meaning, **MUST read** [Scientific and mathematical formulation](references/scientific-formulation.md).
- When it can alter estimator/discretization/error/convergence/precision/stochastic semantics, **MUST read** [Algorithm and numerical method design](references/numerical-algorithm-design.md).
- Cross-domain scientific evidence routes through [Scientific software](references/scientific-software.md).

Implementation evidence may challenge upstream authority but never silently redefine it.

### Language-profile dispatch

For material executable work, language semantics are part of the normal implementation path rather than an optional performance appendix.

- First **MUST read** [Language engineering profiles](references/language-profiles.md) to classify the affected runtime/build surface.
- For materially affected Python executable surfaces, **MUST read** [Python engineering](references/python-engineering.md).
- For materially affected C++ executable surfaces, **MUST read** [C++ engineering](references/cpp-engineering.md).
- Mixed Python/C++ boundaries **MUST read both** language profiles and apply the router's boundary rules. Tiny literal/text/config-only work may remain on shared doctrine when language semantics cannot alter the decision.

Shared owners outrank language profiles. Implement idiomatically for the active language/runtime while preserving the accepted parent contract and minimum justified total complexity.

### Per-question tool dispatch

Classify each material engineering question by the relation under the claim, not once per task:

- literal/path/text lookup or small deterministic local inspection -> ordinary repository search/read normally remains sufficient;
- symbol ownership/definition/callers/references/implementations, bounded semantic navigation, or symbol-aware editing -> **MUST read** [Serena](references/tool-serena.md) before relying solely on lower-information defaults;
- AST/syntax/structural patterns, diagnosed variants, forbidden/legacy constructs, or structural absence/uniqueness -> **MUST read** [Semgrep](references/tool-semgrep.md);
- broad/combinatorial Python input/state invariants -> **MUST read** [Hypothesis](references/tool-hypothesis.md);
- broad/combinatorial non-Python input/state invariants -> use the language-appropriate property/generative route in [Tool-assisted engineering](references/tool-assisted-engineering.md) plus the active language profile;
- supported interprocedural flow/taint/source-to-sink relations -> **MUST read** [CodeQL](references/tool-codeql.md).

Runtime-state/debugger, memory/lifetime/UB, race/synchronization, and performance/vectorization questions route through [Tool-assisted engineering](references/tool-assisted-engineering.md) plus the active language profile rather than a fixed tool sequence. For overlaps/composition/common evidence limits, read [Tool-assisted engineering](references/tool-assisted-engineering.md).

When a specialized trigger fires and availability is unknown, use a cheap non-mutating capability probe when practical. If the capability is available/current/supported and directly models the claim, presumptively use it; otherwise take a concrete fallback such as unsupported backend/language, unavailable tool surface, stale/unreliable analysis state that cannot economically be refreshed, model mismatch, disproportionate setup for a trivially bounded claim, or already-available evidence that establishes the same claim at least as reliably and more cheaply. Familiarity with built-in search/read/shell/test tools is not itself a fallback reason.

### Domain-conditional routes

- Repository intake/context economy -> [Repository intake](references/repository-intake.md).
- Recurrence/family closure/review readiness/review saturation/revision economy -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md).
- Debugging/recovery/state reconstruction -> [Debugging and state recovery](references/debugging-and-state-recovery.md).
- Specification/API/schema ownership or implementation fidelity -> [Specification and implementation](references/specification-and-implementation.md).
- Evidence/documentation -> [Documentation and evidence](references/documentation-and-evidence.md).
- Packaging/release -> [Release and distribution](references/release-and-distribution.md).
- Git/version control -> [Git and version control](references/git-and-version-control.md).
- Configuration -> [Configuration and policy](references/configuration-and-policy.md).
- Orchestration/concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md).
- Security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md).
- Performance/resources/parallelism -> [Performance and parallelism](references/performance-and-parallelism.md).
- Storage/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md).

## D4 authority and adaptive concretization

Separate:

1. applicable upstream accepted abstractions and external constraints;
2. accepted D4 specification and cycle-scoped D3 decisions;
3. delegated D4 concretization.

Within the feasible set prefer:

```text
implementation fitness
> minimum justified concretization complexity
> development economy
```

Code, tests, wrappers, caches, state machines, retries, helpers, previous patches, and current owner paths remain delegated unless governing authority explicitly requires them.

A D4 Specification is intended concrete behavior; code is the actual executable concretization and evidence of actual behavior. When specification and code disagree, do not automatically rewrite the specification to bless code. Repair implementation, or route a genuine contract/parent mutation through its owning authority.

## Adaptive concretization, local reconciliation, and self-correction

An **equivalent local concretization** that preserves governing parent semantics is **local reconciliation**, not redesign. It may remove, consolidate, refactor, or replace previously expected delegated machinery. A suggested concretization does not become accepted authority merely because earlier Design or a workplan named it.

If representative measurement invalidating a premise of accepted D3/D2/D1 authority appears, stop dependent work and reopen only the affected authority surface at the earliest materially affected stage/domain. Do not reopen unrelated design merely because the affected surface is large.

If later evidence proves accepted implementation work unsound, invalidate it and repair/retest. Truthful non-closure is preferable to counterfeit completion, but continue while a reasonable in-scope engineering path remains.

## Evidence specification, realization, and applicability

Keep distinct:

```text
evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

A test definition is an evidence specification; one run against one identified candidate/regime/environment is an evidence realization. A rerun against a changed candidate creates a new evidence realization rather than mutating the old result into evidence for the new candidate.

For material acceptance identify both:

- the governed proposition/real semantic owner the evidence is intended to interrogate; and
- execution dependencies such as harness, fixtures, datasets, backend, environment, and replaceable D4 machinery.

Changing an execution dependency may require remapping/rerunning evidence without changing the proposition. A concretization-specific oracle may instead become stale. Do not preserve obsolete production machinery merely to keep an old harness executable.

A valid failing observation is evidence. A stale failing observation is not admissible evidence against the current claim. A stale passing observation is not admissible confirmation of the current claim. Use `review-required` when applicability is uncertain.

For important/high-risk claims, prefer independent evidence routes when they materially reduce common-mode risk. Multiple tests sharing the same expected-value generator/reference implementation/dataset defect/assumption are not independent merely because they execute separately.

## Owning-layer repair and active simplification

Fix a clear local defect at the owning layer. Before adding durable machinery, ask whether removing, narrowing, altering, consolidating, refactoring, or replacing the lower-level cause eliminates the problem.

A first clean local defect remains local. Material sibling recurrence changes reasoning to the shared owner/mechanism but does not make the current concretization invariant. Repeated patch-on-patch repair, wrapper/fallback/special-case accumulation, duplicated/synchronized authority, repeated reconciliation, or an evident materially simpler equivalent concretization makes simplification/re-derivation mandatory before another additive durable repair.

When an independently governed urgency, safety, security, reliability, or incident-containment constraint requires immediate action, a bounded reversible or safely replaceable mitigation may precede the normal simplification/re-derivation pass. Keep unresolved structural debt/risk explicit, do not let emergency use promote the mitigation into durable authority, and reconcile the owning concretization/abstraction at the earliest safe point.

If correction requires changing accepted D3/D2/D1 semantics, stop dependent closure and route the earliest affected abstraction rather than constructing a compatibility wrapper around the contradiction.

## Coherent implementation stages

A local coherent behavior change is normally one material implementation stage even if several files/helpers/tests change. Several tightly coupled caller/helper/test edits do not become separate stages merely because they touch separate files or functions unless they form an independent risk boundary.

Each material executable stage closes both:

- semantic/conformance obligations assigned to that stage; and
- focused checks plus the stage-local affected regression subset.

Do not defer all affected regression to the end merely because a later full suite exists. Reuse still-valid intermediate evidence until a changed authority/concretization/evidence-specification/environment dimension can plausibly invalidate it.

## Proxy-proof D4 acceptance

For a material claim identify the **real semantic owner/path of the final accepted concretization**. Ask whether evidence could remain green while that actual owner is broken. Bounded test doubles remain valid below or outside the semantic owner, but may not replace the owner under acceptance.

An equivalent delegated owner replacement is permitted when governing semantics survive; invalidate/remap owner-specific evidence and test the new real owner. Do not treat that remapping as proxy-passing or Design reopening merely because the owner identity changed.

If the required real-owner boundary is unavailable, record it as **unavailable/blocking**. Do not declare success by silently proxy-passing the unavailable owner.

## Bounded impact closure

When accepted authority or a material concretization changes, account proportionately for:

```text
changed authority/concretization
 -> materially affected descendant authority/concretizations
 -> affected evidence specifications/realizations
 -> affected documentation/current dependency view
 -> required human re-ratification where applicable
 -> required revalidation/retirement/semantic-history update
```

Preserve unaffected siblings and still-valid evidence. A changed parent creates a review obligation over material descendants but does not automatically prove every descendant wrong.

A bounded dependency record is an aid, not a complete oracle by default. Absence of an edge is not proof of independence unless the relevant mapped scope was explicitly reviewed as complete for the exclusion.

Before closure every material impact item must be resolved, preserved as still-valid with reason, or explicitly unavailable/blocking. Old green tests are never a substitute for impact closure.

## Final assembled acceptance

Before completion:

1. reconcile every accepted D4/D3/upstream obligation; **silent omission is not an accepted state**;
2. inspect superseded machinery, duplicate authority, bypass/fallback paths, stale evidence, and material complexity drift;
3. re-derive the complete affected behavioral, semantic, evidence, and documentation/dependency surface from the final candidate;
4. run the complete affected-surface regression after all material executable edits;
5. run real-boundary integration/end-to-end paths;
6. run repository/project-required lint/type/build/package/checks;
7. account for structural absence/uniqueness claims, material impact-closure items, and unavailable/blocking required checks.

A required check that did not execute is not a pass. Green tests do not prove an omitted obligation. Production qualification remains separate from regression/integration.

For high-risk scientific/numerical changes, final evidence may also need composed closure from executable observables through D2 error/equivalence semantics to D1 meaning and external adequacy.

## Challenge duty

Implementation is not epistemically compliant. If evidence indicates a governing abstraction may itself be materially false, contradictory, ambiguous, inadequate, or impossible to concretize, surface the Serious Challenge even before formal Review.

```text
parent coherent; child concretization wrong -> ordinary D4 blocker
parent authority may be wrong -> Serious Challenge / human adjudication at earliest affected owner
```

Do not relax tolerance, add fallback/wrapper, rewrite tests/specification/method papers, discard contradictory admissible observations, or otherwise route around a serious parent contradiction.

## Completion

Report material implementation/reconciliation, final semantic owner, evidence specifications/realizations used and their applicability, checks actually executed, unavailable/blocking checks, upstream challenges, documentation/dependency/history impact, and unresolved material risks. Do not emit empty protocol categories or claim Pass before assembled acceptance.
