---
name: software-implementation
description: Use to implement, fix, debug, refactor, test, or package scientific/technical code under unchanged scientific, numerical, and architectural contracts. Routes changes to those contracts to the SSDP formulation, numerical, or design skills.
---

# Software Implementation

Own **D4 executable concretization**: implement accepted D4 specification and D3 architecture while satisfying every applicable upstream D1/D2 invariant and directly governed constraint. Code, tests, wrappers, helpers, caches, state machines and prior patches are delegated machinery unless authority explicitly requires them.

**Version entry check.** This package is SSDP `6.6.0`. If the task or its governing workplan declares a different SSDP `protocol_version`, say so and resolve that version's compatible source before protocol-dependent reasoning ([Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md)); never apply this package's doctrine to other-version work. No declared version: continue.

## Routing

Before substantive D4 implementation, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) (the universal kernel) and [Specification and implementation](references/specification-and-implementation.md).

Load only triggered concern owners:

- governing workplan, stage/handoff/rework, working state, authority lifecycle or impact closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- evidence applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); executable acceptance/regression/integration/proxy-proof/oracle/qualification -> [Testing and validation](references/testing-and-validation.md);
- a specialized scientific/numerical object, parameter/default binding, external result/import, formal claim, or material ambiguity used by the change -> [Semantic definition and traceability](references/semantic-definition-and-traceability.md);
- project history can change the decision (mature rework/replacement, suspected recurrence, substantial optimization/scaling, migration/recovery/revert, memory-bound workplan) -> [Project Engineering Memory](references/project-engineering-memory.md);
- architecture/ownership/complexity/redesign question -> [Software architecture and design](references/architecture-and-design.md); recurrence/simplification/rigor or cognitive-resource escalation -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md); long-horizon structural/test risk or Stabilization -> [Long-horizon code health](references/long-horizon-code-health.md);
- protocol-version mismatch or historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- material executable language/runtime/build semantics -> [Language engineering profiles](references/language-profiles.md), which dispatches to Python/C++ profiles; specialized engineering relation -> [Tool-assisted engineering](references/tool-assisted-engineering.md), which owns analyzer/tool-leaf routing;
- the change can alter scientific meaning -> [Scientific formulation](references/scientific-formulation.md); estimator/discretization/error/convergence/precision/stochastic semantics -> [Numerical algorithm design](references/numerical-algorithm-design.md); cross-domain scientific evidence -> [Scientific software](references/scientific-software.md).

Other concerns route when material: repository/context -> [Repository intake](references/repository-intake.md); debugging/recovery -> [Debugging and state recovery](references/debugging-and-state-recovery.md); documentation -> [Documentation and evidence](references/documentation-and-evidence.md) / [Scientific and technical writing](references/scientific-technical-writing.md); release/package -> [Release and distribution](references/release-and-distribution.md); Git -> [Git and version control](references/git-and-version-control.md); configuration -> [Configuration and policy](references/configuration-and-policy.md); concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md); security -> [Security and trust boundaries](references/security-and-trust-boundaries.md); performance -> [Performance and parallelism](references/performance-and-parallelism.md); storage/I/O -> [Storage and I/O](references/storage-and-io.md).

A first clean local defect under sufficient authority loads none of the conditional owners above merely because they exist; ordinary hyperlinks and package membership are not activation commands.

## Implementation contract

1. Reconstruct the complete accepted contract: upstream invariants/constraints, D3 architecture, D4 specification/workplan cycle decisions, and delegated space.
2. Inspect the actual affected surface and bound consequence before broadening scope. For ROUTINE/INCIDENTAL delegated defects prefer direct owning-layer repair plus focused affected evidence. Implement the simplest admissible concretization; remove/narrow/alter/consolidate/refactor lower-level cause before adding durable wrappers/fallbacks/special cases.
3. An equivalent local concretization is D4 reconciliation, not redesign. Reopen D3/D2/D1 only when the governing abstraction/cycle decision must change; never change a D1/D2-owned meaning, parameter default or tolerance as an implementation convenience.
4. For each coherent material executable stage, close semantic/conformance obligations plus focused checks and stage-local affected regression before dependent executable work continues. Tightly coupled edits may form one stage; file count does not define stage count.
5. Track evidence target separately from harness/fixture/backend/implementation dependencies. Remap/rerun still-valid evidence specifications after owner replacement rather than preserving obsolete product machinery for the test.
6. Before final completion, reconcile every accepted obligation; inspect obsolete/bypassed/duplicate ownership and complexity drift; re-derive the complete final affected semantic/behavioral/evidence/documentation surface; run complete affected regression, real-boundary integration/end-to-end, and repository/project-required checks; close each material impact item or report unavailable/blocking.

A required check that did not execute is not a pass. Green tests do not prove omitted workplan obligations. For any material acceptance claim identify the real semantic owner/path and ask whether evidence could remain green while that owner is broken; test doubles may control dependencies below/outside the owner but cannot replace it. If that boundary is unavailable, report unavailable/blocking rather than proxy-passing it. A stale pass is not current confirmation; a stale fail is not current refutation. Use the cheapest sufficiently strong applicable evidence and stop when remaining uncertainty cannot change the governed decision.

## Challenge duty

Implementation must challenge upward when admissible evidence indicates accepted authority may itself be materially false, contradictory, ambiguous, inadequate, or impossible to concretize. Do not relax tolerances, weaken tests/specification, add wrappers/fallbacks, or discard contradictory evidence to route around such a defect.

```text
parent coherent; child wrong -> D4 blocker
parent authority may be wrong -> SERIOUS CHALLENGE at earliest affected owner
```

## Completion

Report material implementation/reconciliation, final semantic owner, evidence used and its applicability, checks actually executed, unavailable/blocking checks, upstream Challenge if any, documentation/dependency/history impact, and unresolved risk. Lead with any Serious Challenge or blocker; omit empty categories.
