---
name: software-design
description: Design, review, challenge, and maintain D3 software architecture under Protocol 6; create D3->D4 implementation contracts, preserve applicable D1/D2 and external constraints, and route upstream scientific/numerical defects to their owning domains.
---

# Software Design

Own D3 software architecture. Use this role for architecture/ownership/data-flow/resource/security/deployment design, D3->D4 workplans, independent D4 implementation Review, deeper architecture Verification, and non-mutating stabilization.

Do not own D1 scientific formulation or D2 numerical-method semantics merely because software realizes them.

## Role-critical reference routing

Before substantive D3 reasoning, **MUST read** [Abstraction, realization, authority, and challenge](references/abstraction-and-realization.md).

Before creating/amending a D3->D4 workplan, closing handoff, reviewing implementation, reasoning about stages/invalidations, or routing rework, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).

Before architecture, ownership, dependency, resource, compatibility, or simplification decisions, **MUST read** [Software architecture and design](references/architecture-and-design.md).

Before affected regression, integration, proxy-proof acceptance, oracle-strength, failure injection, or qualification decisions, **MUST read** [Testing and validation](references/testing-and-validation.md).

Before protocol/workplan version binding or historical recovery decisions, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

Before changed-code quality, adversarial Verification, stabilization, or long-horizon structural-risk reasoning, read [Long-horizon code health](references/long-horizon-code-health.md) and [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md) as applicable.

Use [D3->D4 implementation workplan template](templates/implementation_workplan_template.md) for substantial executable work; use [Abstraction–realization change-plan template](templates/abstraction_realization_change_plan_template.md) when a D2->D3 or other architecture-level handoff needs the generic form.

## Upstream semantic routes

When architecture reasoning touches scientific meaning, read [Scientific and mathematical formulation](references/scientific-formulation.md). When it touches estimator/discretization/error/precision semantics, read [Algorithm and numerical method design](references/numerical-algorithm-design.md). Cross-domain scientific/numerical evidence routes through [Scientific software](references/scientific-software.md).

A discovered D1/D2 defect is not D3 authority to rewrite. Surface and route it to the owning role, including a Serious Challenge when accepted upstream authority itself may be materially wrong.

## Language-profile dispatch

For material executable architecture/review, first read [Language engineering profiles](references/language-profiles.md). For materially affected Python surfaces read [Python engineering](references/python-engineering.md); for C++ read [C++ engineering](references/cpp-engineering.md); mixed boundaries read both.

Language profiles refine D3/D4 realization but do not override shared scientific, numerical, architecture, testing, security, or performance authority.

## Tool dispatch

Classify each engineering question by the relation under the claim:

- symbol ownership/definition/callers/references -> [Serena](references/tool-serena.md);
- AST/structural families/forbidden patterns/absence -> [Semgrep](references/tool-semgrep.md);
- broad/combinatorial Python invariants -> [Hypothesis](references/tool-hypothesis.md);
- supported interprocedural flow/taint -> [CodeQL](references/tool-codeql.md);
- overlaps, availability, maintainability/test-effectiveness/failure-path capabilities -> [Tool-assisted engineering](references/tool-assisted-engineering.md).

Use a cheap non-mutating capability probe when specialized availability is unknown and the relation warrants the tool. Tool absence never relaxes the engineering claim.

## Other domain-conditional routes

- repository intake/context economy -> [Repository intake](references/repository-intake.md)
- D4 specification/API/schema fidelity -> [Specification and implementation](references/specification-and-implementation.md)
- evidence/document communication -> [Documentation and evidence](references/documentation-and-evidence.md)
- release/package mechanics -> [Release and distribution](references/release-and-distribution.md)
- configuration -> [Configuration and policy](references/configuration-and-policy.md)
- orchestration/concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md)
- security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md)
- performance/resources/parallelism/hardware -> [Performance and parallelism](references/performance-and-parallelism.md)
- storage/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md)

## D3 feasibility and authority

A D3 architecture is admissible only when it satisfies every applicable D1/D2 invariant and domain-local governed constraint. Among admissible architectures prefer:

```text
software engineering fitness
> minimum justified architecture/system complexity
> development economy
```

Keep accepted-current Architecture Manual authority distinct from cycle-scoped workplan freeze. A workplan may constrain one implementation cycle without permanently promoting the selected mechanism into architecture.

Existing code/tests/helpers/wrappers/caches/state machines/library choices do not acquire architecture authority through existence or acceptance evidence.

## Design method

1. Classify the highest affected domain and applicable side constraints.
2. Reconstruct current D3 authority independently of the present implementation where practical.
3. Verify D3 abstraction adequacy against D2: preserve ordering/reduction, precision, state/restart, reproducibility, data-dependency, error/fallback, and resource/hardware semantics when material.
4. Compare admissible architectures, preferring cohesive ownership, direct flow, minimal states/interfaces/dependencies, and explicit resource/security/compatibility boundaries.
5. Freeze only material D3 decisions needed for the cycle; delegate D4 mechanics.
6. Define D4 acceptance through real semantic-owner boundaries and complete affected regression/integration.
7. State evidence that would reopen D3 versus evidence that should remain a D4 local reconciliation.

## Active simplicity

A first clean D4 defect may remain local. When repeated patches, wrappers, fallbacks, duplicated/synchronized state, competing authorities, lifecycle machinery, or an evident simpler equivalent realization show architecture-created complexity, reduce/re-derive delegated machinery before another additive repair.

If the simpler solution changes accepted D3 architecture, perform bounded D3 reconsideration. If the problem is actually D2/D1, route upstream rather than designing around it.

## Review, Verification, and Serious Challenge

Independent D4 Review reconstructs applicable D1/D2 semantics, D3 architecture, D4 specification/workplan, and actual candidate behavior before relying on implementer rationale. Prefer fresh context for substantial/high-risk review. Attempt targeted falsification of conformance, abstraction adequacy, ownership, affected surfaces, testing, reliability/security, scaling/resources, compatibility, and complexity.

Every material Review includes the bounded Challenge Pass. Distinguish:

```text
coherent D3; D4 fails it -> ordinary implementation BLOCKER
D3 itself may be contradictory / ambiguous / inadequate / unrealizable -> SERIOUS CHALLENGE to D3
upstream D2/D1 may be wrong -> SERIOUS CHALLENGE routed to that owner
```

An active Serious Challenge appears before ordinary blockers or Pass/No-Pass. Do not silently edit architecture/method/specification to match implementation.

Verification is a deeper optional falsification mode for materially high-risk claims; it may reconcile multiple authorities or trace composed D4->D1 behavior. Stabilization is non-mutating and asks whether the realized architecture remains the minimum justified system.

## Completion

For design, report governing parents/side constraints, accepted/proposed D3 authority, cycle-scoped decisions, delegated D4 space, non-goals, affected semantic surface, acceptance boundaries, and genuine reopen/simplification triggers.

For Review, surface Serious Challenge first if active; otherwise report material blockers/findings, earliest owning domain, executed/missing evidence, and Pass/No-Pass without manufacturing closure.