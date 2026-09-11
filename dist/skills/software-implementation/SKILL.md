---
name: software-implementation
description: Implement, refactor, test, package, and validate D4 concretizations under Protocol 6.2 while preserving accepted D1-D3/D4 authority, affected regression/integration, evidence applicability, active simplicity, and upward Challenge routing.
---

# Software Implementation

Own **D4 executable concretization**. Implement accepted D4 specification and D3 architecture while satisfying every applicable upstream D1/D2 invariant and directly governed constraint. Code, tests, wrappers, helpers, caches, state machines and prior patches are delegated machinery unless authority explicitly requires them.

## Routing

Before substantive D4 implementation, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) and [Specification and implementation](references/specification-and-implementation.md).

Load only triggered concern owners:

- accepted workplan, stage/handoff/rework/impact closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- evidence applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); executable acceptance/regression/integration/proxy-proof/oracle/qualification -> [Testing and validation](references/testing-and-validation.md);
- architecture/ownership/complexity/redesign question -> [Software architecture and design](references/architecture-and-design.md); recurrence/simplification -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md); long-horizon structural/test risk or Stabilization -> [Long-horizon code health](references/long-horizon-code-health.md);
- protocol-version/historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- material executable language/runtime/build semantics -> [Language engineering profiles](references/language-profiles.md), which dispatches to Python/C++ profiles;
- specialized engineering relation -> [Tool-assisted engineering](references/tool-assisted-engineering.md), which owns analyzer/tool-leaf routing.

When implementation can alter scientific meaning route [Scientific formulation](references/scientific-formulation.md); when it can alter estimator/discretization/error/convergence/precision/stochastic semantics route [Numerical algorithm design](references/numerical-algorithm-design.md); use [Scientific software](references/scientific-software.md) for cross-domain scientific evidence.

Other concerns route when material: repository/context -> [Repository intake](references/repository-intake.md); debugging/recovery -> [Debugging and state recovery](references/debugging-and-state-recovery.md); documentation -> [Documentation and evidence](references/documentation-and-evidence.md) / [Scientific and technical writing](references/scientific-technical-writing.md); release/package -> [Release and distribution](references/release-and-distribution.md); Git -> [Git and version control](references/git-and-version-control.md); configuration -> [Configuration and policy](references/configuration-and-policy.md); concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md); security -> [Security and trust boundaries](references/security-and-trust-boundaries.md); performance -> [Performance and parallelism](references/performance-and-parallelism.md); storage/I/O -> [Storage and I/O](references/storage-and-io.md).

Ordinary hyperlinks/package membership are not activation commands.

## Implementation method

1. Reconstruct the complete accepted contract: upstream invariants/constraints, D3 architecture, D4 specification/workplan cycle decisions, and delegated space.
2. Inspect the actual affected surface. Implement the simplest admissible concretization at the owning layer; remove/narrow/alter/consolidate/refactor lower-level cause before adding durable wrappers/fallbacks/special cases.
3. An equivalent local concretization is D4 reconciliation, not redesign. Reopen D3/D2/D1 only when the governing abstraction/cycle decision must change.
4. For each coherent material executable stage, close semantic/conformance obligations plus focused checks and stage-local affected regression before dependent executable work continues. Tightly coupled edits may form one stage; file count does not define stage count.
5. Track evidence target separately from harness/fixture/backend/implementation dependencies. Remap/rerun still-valid evidence specifications after owner replacement rather than preserving obsolete product machinery for the test.
6. Before final completion, reconcile every accepted obligation; inspect obsolete/bypassed/duplicate ownership and complexity drift; re-derive the complete final affected semantic/behavioral/evidence/documentation surface; run complete affected regression, real-boundary integration/end-to-end, and repository/project-required checks; close each material impact item or report unavailable/blocking.

A required check that did not execute is not a pass. Green tests do not prove omitted workplan obligations. Production qualification is separate from functional regression/integration.

## Evidence and real-owner acceptance

For any material acceptance claim identify the real semantic owner/path and ask whether evidence could remain green while that owner is broken. Test doubles may control dependencies below/outside the owner, but cannot replace the owner whose behavior constitutes the claim. If that boundary is unavailable, report unavailable/blocking rather than proxy-passing it.

Use structural/negative evidence for removal/uniqueness/no-legacy-path claims that runtime tests cannot establish. For recovery/state/failure-propagation claims, bounded deterministic failure injection is appropriate when it materially strengthens evidence while the real owner remains live.

A stale pass is not current confirmation; a stale fail is not current refutation. Reuse evidence only while its claim/candidate/regime/oracle/environment applicability remains intact.

## Language/tool execution

Use language-native mechanisms and the project's configured fast static/test/build tooling when materially informative. Do not introduce a tool/dependency solely for protocol symmetry. The language router decides Python/C++ specialization; the relation-first tool owner decides semantic/structural/property/data-flow/runtime/memory/race/performance/etc. capability routing.

## Challenge duty

Implementation must challenge upward when admissible evidence indicates accepted authority may itself be materially false, contradictory, ambiguous, inadequate, or impossible to concretize. Do not relax tolerances, weaken tests/specification, add wrappers/fallbacks, or discard contradictory evidence to route around such a defect.

```text
parent coherent; child wrong -> D4 blocker
parent authority may be wrong -> SERIOUS CHALLENGE at earliest affected owner
```

## Completion

Report material implementation/reconciliation, final semantic owner, evidence used and applicability, checks actually executed, unavailable/blocking checks, upstream Challenge if any, documentation/dependency/history impact, and unresolved risk. Lead with any Serious Challenge or blocker; omit empty process categories. Keep the report compact but complete for the governed scope.
