---
name: software-implementation
description: Implement, refactor, test, package, and validate D4 software realizations under Protocol 6 while preserving applicable D1/D2/D3 authority, accepted D4 specification, affected-surface regression/integration, and upward challenge routing.
---

# Software Implementation

Own executable D4 realization. Implement the accepted D4 specification and D3 architecture while satisfying every applicable upstream D1/D2 semantic invariant and domain-local governed constraint.

## Role-critical reference routing

Before substantive implementation, **MUST read** [Abstraction, realization, authority, and challenge](references/abstraction-and-realization.md).

Before implementing from an accepted workplan, closing a material stage, performing local reconciliation, or routing parent invalidation, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).

Before executable acceptance, affected regression/integration, proxy-proof boundaries, evidence reuse, oracle strength, or qualification, **MUST read** [Testing and validation](references/testing-and-validation.md).

Before architecture/ownership/complexity/redesign decisions, **MUST read** [Software architecture and design](references/architecture-and-design.md).

Before specification/API/schema/compatibility behavior changes, read [Specification and implementation](references/specification-and-implementation.md).

Before protocol/workplan version binding or historical recovery decisions, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

Before changed-code quality, maintainability/test-effectiveness, recovery/failure-path, or structural-risk reasoning, read [Long-horizon code health](references/long-horizon-code-health.md) and [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md) as applicable.

## Upstream semantic routes

When implementation can alter scientific meaning, read [Scientific and mathematical formulation](references/scientific-formulation.md). When it can alter estimator/discretization/error/convergence/precision/stochastic semantics, read [Algorithm and numerical method design](references/numerical-algorithm-design.md). Cross-domain scientific evidence routes through [Scientific software](references/scientific-software.md).

Implementation evidence may challenge upstream authority but never silently redefine it.

## Language-profile dispatch

For material executable work, first read [Language engineering profiles](references/language-profiles.md). For affected Python surfaces read [Python engineering](references/python-engineering.md); for C++ read [C++ engineering](references/cpp-engineering.md); mixed boundaries read both.

Use language-native realization beneath shared authority. Do not preserve compensating machinery simply because an earlier language or implementation used it.

## Tool dispatch

Per material question:

- symbol ownership/definitions/callers -> [Serena](references/tool-serena.md);
- AST/structural variants/absence -> [Semgrep](references/tool-semgrep.md);
- broad/combinatorial Python invariants -> [Hypothesis](references/tool-hypothesis.md);
- supported interprocedural flow/taint -> [CodeQL](references/tool-codeql.md);
- combined/alternative capabilities -> [Tool-assisted engineering](references/tool-assisted-engineering.md).

Use cheap non-mutating capability probes when warranted. Tool absence does not relax correctness.

## Other domain-conditional routes

- repository intake -> [Repository intake](references/repository-intake.md)
- debugging/state reconstruction -> [Debugging and state recovery](references/debugging-and-state-recovery.md)
- evidence/documentation -> [Documentation and evidence](references/documentation-and-evidence.md)
- packaging/release -> [Release and distribution](references/release-and-distribution.md)
- Git/version control -> [Git and version control](references/git-and-version-control.md)
- configuration -> [Configuration and policy](references/configuration-and-policy.md)
- orchestration/concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md)
- security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md)
- performance/resources/parallelism -> [Performance and parallelism](references/performance-and-parallelism.md)
- storage/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md)

## D4 authority and adaptive realization

Separate:

1. applicable upstream accepted abstractions and external constraints;
2. accepted D4 specification and cycle-scoped D3 decisions;
3. delegated D4 realization.

Within the feasible set prefer:

```text
implementation fitness
> minimum justified realization complexity
> development economy
```

Code, tests, wrappers, caches, state machines, retries, helpers, previous patches, and current owner paths remain delegated unless governing authority explicitly requires them.

A D4 Specification is intended concrete behavior; code is actual realization/evidence. When they disagree, do not automatically rewrite the specification to bless code. Repair implementation, or route a genuine contract/parent mutation through its owning authority.

## Owning-layer repair and active simplification

Fix a clear local defect at the owning layer. Before adding durable machinery, ask whether removing, narrowing, altering, consolidating, refactoring, or replacing the lower-level cause eliminates the problem.

Repeated patch-on-patch repair, wrapper/fallback/special-case accumulation, duplicated/synchronized authority, repeated reconciliation, or an evident materially simpler equivalent realization makes simplification/re-derivation mandatory before another additive durable repair.

If correction requires changing accepted D3/D2/D1 semantics, stop dependent closure and route the earliest affected abstraction rather than constructing a compatibility wrapper around the contradiction.

## Coherent implementation stages

A local coherent behavior change is normally one material stage even if several files/helpers/tests change. Each material executable stage closes both:

- semantic/conformance obligations assigned to that stage; and
- focused checks plus the stage-local affected regression subset.

Do not defer all affected regression to the end merely because a later full suite exists. Reuse still-valid intermediate evidence until a changed dimension can plausibly invalidate it.

## Proxy-proof D4 acceptance

For a material claim identify the real semantic owner/path in the final accepted realization. Bounded doubles are valid only below/outside that owner. Evidence that could remain green while the actual owner is broken cannot close the claim.

An equivalent delegated owner replacement is permitted when governing semantics survive; invalidate/remap owner-specific evidence and test the new real owner. Exact owner identity is binding only when an accepted contract or D3 architecture makes it so.

## Final assembled acceptance

Before completion:

1. reconcile every accepted D4/D3/upstream obligation;
2. inspect superseded machinery, duplicate authority, bypass/fallback paths, and material complexity drift;
3. re-derive the complete affected behavioral and semantic surface;
4. run the complete affected-surface regression after all material executable edits;
5. run real-boundary integration/end-to-end paths;
6. run repository/project-required lint/type/build/package/checks;
7. account for structural absence/uniqueness claims and unavailable required checks.

A required check that did not execute is not a pass. Green tests do not prove an omitted obligation. Production qualification remains separate from regression/integration.

For high-risk scientific/numerical changes, final evidence may also need composed closure from executable observables through D2 error/equivalence semantics to D1 meaning and external adequacy.

## Challenge duty

Implementation is not epistemically compliant. If evidence indicates a governing abstraction may itself be materially false, contradictory, ambiguous, inadequate, or unrealizable, surface the Serious Challenge even before formal Review.

```text
parent coherent; child implementation wrong -> ordinary D4 blocker
parent authority may be wrong -> Serious Challenge / human adjudication at earliest affected owner
```

Do not relax tolerance, add fallback/wrapper, rewrite tests/specification/method papers, or otherwise route around a serious parent contradiction.

## Completion

Report material implementation/reconciliation, final semantic owner, checks actually executed, unavailable/blocking checks, upstream challenges, documentation/specification impact, and unresolved material risks. Do not emit empty protocol categories or claim Pass before assembled acceptance.