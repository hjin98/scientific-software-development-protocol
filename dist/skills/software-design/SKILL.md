---
name: software-design
description: Design, review, challenge, and maintain D3 software architecture under Protocol 6.3; create D3->D4 implementation contracts, preserve applicable D1/D2 and external constraints, track evidence/dependency impact, and route upstream scientific/numerical defects to their owners.
---

# Software Design

Own **D3 software architecture**: durable component/state/interface ownership, dependency/data/control flow, persistence/recovery, concurrency, security, resource/deployment/compatibility boundaries, and cycle-scoped architectural decisions. Do not absorb D1/D2 semantics merely because software concretizes them.

## Routing

Before substantive D3 reasoning, read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) and [Software architecture and design](references/architecture-and-design.md).

Load only triggered concern owners:

- D3->D4 workplan, handoff, lifecycle/rework/impact closure, implementation Review -> [Workflow and workplans](references/workflow-and-workplans.md);
- evidence applicability/dependency/evolution -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); regression/integration/proxy-proof/oracle/qualification method -> [Testing and validation](references/testing-and-validation.md);
- mature architecture/concretization rework, replacement/consolidation of mature machinery, suspected recurrence, substantial optimization/scaling, migration/recovery/revert, or an active workplan that can materially depend on demonstrated project history -> [Project Engineering Memory](references/project-engineering-memory.md); resolve the project-governed accepted/base memory plus any validated same-branch candidate overlay, build a Historical Applicability Set (HAS) over every materially relevant entry regardless of temperature, and build a capability-transfer map when replacing mature machinery;
- protocol-version/historical recovery -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md);
- recurrence/simplification/review saturation -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md); longitudinal health/Stabilization -> [Long-horizon code health](references/long-horizon-code-health.md);
- scientific meaning -> [Scientific formulation](references/scientific-formulation.md); estimator/discretization/error/precision/stochastic meaning -> [Numerical algorithm design](references/numerical-algorithm-design.md); cross-domain scientific evidence -> [Scientific software](references/scientific-software.md);
- material executable language/runtime/build semantics -> [Language engineering profiles](references/language-profiles.md), which conditionally dispatches to Python/C++ profiles;
- a specialized engineering relation where a tool may materially improve evidence -> [Tool-assisted engineering](references/tool-assisted-engineering.md), which owns analyzer/tool-leaf dispatch.

Other domain concerns route directly when material: repository/context economy -> [Repository intake](references/repository-intake.md); D4 specification -> [Specification and implementation](references/specification-and-implementation.md); documentation -> [Documentation and evidence](references/documentation-and-evidence.md) / [Scientific and technical writing](references/scientific-technical-writing.md); release -> [Release and distribution](references/release-and-distribution.md); configuration -> [Configuration and policy](references/configuration-and-policy.md); orchestration -> [Concurrency and orchestration](references/concurrency-and-orchestration.md); security -> [Security and trust boundaries](references/security-and-trust-boundaries.md); performance -> [Performance and parallelism](references/performance-and-parallelism.md); storage/I/O -> [Storage and I/O](references/storage-and-io.md).

For a substantial executable handoff use [D3->D4 implementation workplan](templates/implementation_workplan_template.md). Ordinary hyperlinks and package membership are not activation commands.

## D3 design method

1. Classify the earliest affected semantic domain and all directly applicable side constraints.
2. Reconstruct accepted D3 authority independently of current implementation where practical; distinguish durable architecture from cycle-scoped workplan freeze and delegated D4 machinery.
3. Test D3 abstraction adequacy against D2: preserve ordering/reduction, precision, state/restart, reproducibility, data dependencies, failure/fallback, resource/hardware semantics when material.
4. Compare admissible architectures. Prefer cohesive ownership, direct flow, one authoritative representation/state, acyclic understandable dependencies, and the fewest necessary components/interfaces/synchronization/compatibility paths.
5. Freeze only material D3 decisions required for the cycle; delegate functions/helpers/wrappers/retries/caches/local algorithms/library identities unless governing authority requires them.
6. Define D4 acceptance at real semantic-owner/consumer boundaries, complete affected regression/integration, and material evidence/dependency/history impact.
7. State what evidence reopens D3 versus what remains equivalent D4 local reconciliation.
8. Durable D3 authority mutation requires its owning acceptance process, including independent falsification before accepted-current promotion. A later implementation Review cannot retroactively legitimize prematurely promoted architecture.

A first clean local defect remains local. When recurrence plus wrappers/fallbacks/duplicated state/competing owners/reconciliation or another clear complexity signal points to a shared mechanism, simplify/re-derive delegated concretization before another additive durable repair. If the simpler solution changes accepted D3, reopen D3; if the defect is D2/D1, route upstream.

## Independent Review and Challenge

Independent D4 Review reconstructs applicable parent semantics, D3/workplan authority, actual candidate behavior, and material evidence applicability rather than replaying implementer rationale. Attempt falsification of conformance, abstraction adequacy, ownership, affected surfaces, testing, reliability/security, scaling/resources, compatibility, complexity, stale evidence, and impact closure.

Literal workplan compliance is insufficient when the workplan/architecture itself is too weak for the protected outcome: classify the deficiency at the earliest owning domain.

Every material Review includes the bounded Challenge Pass. Use:

```text
coherent D3; D4 violates it -> D4 blocker
D3 contradictory / ambiguous / inadequate / unrealizable -> SERIOUS CHALLENGE to D3
upstream D2/D1 may be wrong -> SERIOUS CHALLENGE routed upstream
```

Verification is a deeper risk-triggered falsification mode. Stabilization is non-mutating and asks whether the current concretized architecture remains the minimum justified system.

## Completion

For design, report governing parents/constraints, accepted/proposed D3 state, material cycle decisions, delegated D4 space, non-goals, affected semantic/evidence surface, acceptance boundaries, dependency/history obligations, and genuine reopen/simplification triggers.

For Review, put any Serious Challenge first; otherwise report material blockers by earliest owner, executed/reused/missing evidence with applicability, impact-closure state, and Pass/No-Pass without manufacturing closure. Keep the representation terse but snapshot-complete for the governed decision.
