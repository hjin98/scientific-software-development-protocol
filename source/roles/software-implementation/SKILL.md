---
name: software-implementation
description: Use to implement, fix, debug, refactor, test, or package scientific/technical code under unchanged scientific, numerical, and architectural contracts. Routes changes to those contracts to the SSDP formulation, numerical, or design skills.
---

# Software Implementation

Own **D4 executable concretization** of accepted D4 specification and D3 architecture under applicable D1/D2 invariants and governed constraints; code, tests, wrappers, helpers and caches are delegated machinery unless authority requires them.

<!-- SSDP-ENTRY-CONTRACT -->

## Routing

Before substantive D4 implementation, read [spec](references/specification-and-implementation.md). Load only triggered concern owners:

- governing workplan, stage/handoff/rework, working state, authority lifecycle or impact closure -> [workflow](references/workflow-and-workplans.md)
- evidence applicability/dependency/evolution -> [evidence](references/evidence-evolution-and-dependencies.md); acceptance/regression/integration/proxy-proof/oracle/qualification -> [testing](references/testing-and-validation.md)
- a specialized scientific/numerical object, parameter/default binding, external result/import, formal claim or material ambiguity used by the change -> [defs](references/semantic-definition-and-traceability.md)
- project history can change the decision (mature rework/replacement, suspected recurrence, substantial optimization/scaling, migration/recovery/revert, memory-bound workplan) -> [PEM](references/project-engineering-memory.md)
- architecture/ownership/complexity/redesign -> [D3](references/architecture-and-design.md); recurrence/simplification/rigor or cognitive-resource escalation -> [convergence](references/convergence-and-cycle-economy.md); long-horizon structural/test risk or Stabilization -> [health](references/long-horizon-code-health.md)
- protocol-version mismatch or historical recovery -> [versioning](references/protocol-versioning-and-compatibility.md)
- material executable language/runtime/build semantics -> [language](references/language-profiles.md), which dispatches to Python/C++ profiles; specialized engineering relation -> [tools](references/tool-assisted-engineering.md), which owns tool-leaf routing
- the change can alter scientific meaning -> [D1](references/scientific-formulation.md); estimator/discretization/error/convergence/precision/stochastic semantics -> [D2](references/numerical-algorithm-design.md); cross-domain scientific evidence -> [science](references/scientific-software.md)

Other concerns route when material: repository/context -> [intake](references/repository-intake.md); debugging/recovery -> [debug](references/debugging-and-state-recovery.md); documentation -> [docs](references/documentation-and-evidence.md), [writing](references/scientific-technical-writing.md); release/package -> [release](references/release-and-distribution.md); Git -> [git](references/git-and-version-control.md); configuration -> [config](references/configuration-and-policy.md); concurrency -> [concurrency](references/concurrency-and-orchestration.md); security -> [security](references/security-and-trust-boundaries.md); performance -> [performance](references/performance-and-parallelism.md); storage/I/O -> [storage](references/storage-and-io.md).

A first clean local defect under sufficient authority loads none of these owners; ordinary hyperlinks and package membership are not activation commands.

## Implementation contract

1. Reconstruct the accepted contract and bound consequence before broadening scope. For ROUTINE/INCIDENTAL defects prefer direct owning-layer repair with focused evidence: the simplest admissible concretization; remove/narrow/alter/consolidate/refactor lower-level cause before adding wrappers/fallbacks.
2. An equivalent local concretization is D4 reconciliation, not redesign. Reopen D3/D2/D1 only when the governing abstraction/cycle decision must change; never change a D1/D2-owned meaning, default or tolerance for convenience.
3. Close each material stage with affected regression before dependent work. Before completion reconcile every obligation, inspect obsolete/bypassed/duplicate ownership, re-derive the complete final affected semantic/behavioral/evidence/documentation surface, remap/rerun evidence whose owner changed, and run affected regression, real-boundary integration and required checks.

A required check that did not execute is not a pass; green tests do not prove omitted workplan obligations. Name each material claim's real semantic owner/path and ask whether evidence could remain green while that owner is broken; test doubles may control dependencies below/outside the owner, never replace it. If that boundary is unavailable, report unavailable/blocking rather than proxy-passing it. Stale results neither confirm nor refute; stop when uncertainty cannot change the decision.

## Challenge and completion

Challenge upward when admissible evidence indicates accepted authority may itself be materially false, contradictory, ambiguous, inadequate or unrealizable; never weaken tests, tolerances or specification or discard contradictory evidence to route around it. Parent coherent, child wrong -> D4 blocker; parent authority may be wrong -> SERIOUS CHALLENGE at earliest affected owner.

Report implementation, final semantic owner, evidence applicability, checks executed or unavailable, upstream Challenge, documentation/dependency/history impact and unresolved risk; lead with any Serious Challenge or blocker.
