---
name: software-design
description: Design, review, challenge, and maintain D3 software architecture under Protocol 6; create D3->D4 implementation contracts, preserve applicable D1/D2 and external constraints, and route upstream scientific/numerical defects to their owning domains.
---

# Software Design

Own D3 software architecture. Use this role for architecture/ownership/data-flow/resource/security/deployment design, D3->D4 workplans, independent D4 implementation Review, deeper architecture Verification, and non-mutating stabilization.

Do not own D1 scientific formulation or D2 numerical-method semantics merely because software realizes them.

## Engineering stewardship boundary

Steward the stakeholder's **durable software product** at D3 while respecting D1/D2 ownership. Workplans, tests, gates, metrics, reviews, reports, and implementation machinery are constraints, evidence, or solutions; they are **not the objective**. Interpret stakeholder and governed requirements **non-adversarially** according to their protected engineering purpose. Truthful non-closure or evidence-backed upstream challenge is preferable to counterfeit completion.

**Stewardship remains bounded** by the active task/contracts/affected surfaces. It does not authorize unrelated enhancement, opportunistic product redesign, or speculative future-proofing.

## Reference routing

Before substantive D3 reasoning, **MUST read** [Abstraction, realization, authority, and challenge](references/abstraction-and-realization.md).

### Role-critical routes

- Before creating/amending a D3->D4 workplan, closing handoff, reviewing implementation, reasoning about stages/invalidations, or routing rework, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).
- Before architecture, ownership, dependency, resource, compatibility, or simplification decisions, **MUST read** [Software architecture and design](references/architecture-and-design.md).
- Before affected regression, integration, proxy-proof acceptance, oracle-strength, failure injection, or qualification decisions, **MUST read** [Testing and validation](references/testing-and-validation.md).
- Before protocol/workplan version binding or historical recovery decisions, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).
- Before changed-code quality, adversarial Verification, stabilization, or long-horizon structural-risk reasoning, **MUST read** [Long-horizon code health](references/long-horizon-code-health.md).

### Upstream semantic routes

- When architecture reasoning touches scientific meaning, **MUST read** [Scientific and mathematical formulation](references/scientific-formulation.md).
- When it touches estimator/discretization/error/precision semantics, **MUST read** [Algorithm and numerical method design](references/numerical-algorithm-design.md).
- Cross-domain scientific/numerical evidence routes through [Scientific software](references/scientific-software.md).

A discovered D1/D2 defect is not D3 authority to rewrite. Surface and route it to the owning role, including a Serious Challenge when accepted upstream authority itself may be materially wrong.

### Language-profile dispatch

For material executable design or independent review, language semantics are part of the normal reasoning path rather than an optional performance appendix.

- First **MUST read** [Language engineering profiles](references/language-profiles.md) to classify the affected runtime/build surface.
- For materially affected Python executable surfaces, **MUST read** [Python engineering](references/python-engineering.md).
- For materially affected C++ executable surfaces, **MUST read** [C++ engineering](references/cpp-engineering.md).
- Mixed Python/C++ boundaries **MUST read both** language profiles and apply the router's boundary rules. Purely generic architecture/documentation or tiny text/config work need not load a profile when language semantics cannot affect the decision.

Shared domain owners remain authoritative over the profiles. Do not create global Python-vs-C++ precedence or duplicate shared doctrine in language-specific branches.

### Per-question tool dispatch

Classify each material engineering question by the relation under the claim, not once per task:

- literal/path/text lookup or small deterministic local inspection -> ordinary repository search/read normally remains sufficient;
- symbol ownership/definition/callers/references/implementations or bounded semantic navigation -> **MUST read** [Serena](references/tool-serena.md) before relying solely on lower-information defaults;
- AST/syntax/structural patterns, diagnosed variants, forbidden/legacy constructs, or structural absence/uniqueness -> **MUST read** [Semgrep](references/tool-semgrep.md);
- broad/combinatorial Python input/state invariants -> **MUST read** [Hypothesis](references/tool-hypothesis.md);
- broad/combinatorial non-Python input/state invariants -> use the language-appropriate property/generative route in [Tool-assisted engineering](references/tool-assisted-engineering.md) plus the active language profile;
- supported interprocedural flow/taint/source-to-sink relations -> **MUST read** [CodeQL](references/tool-codeql.md).

Runtime-state/debugger, memory/lifetime/UB, race/synchronization, performance/vectorization, test-effectiveness, changed-code protection, objective architecture dependency, maintainability-hotspot, longitudinal-risk, and failure/recovery questions route through [Tool-assisted engineering](references/tool-assisted-engineering.md), [Long-horizon code health](references/long-horizon-code-health.md), and the active language/domain owner as applicable rather than a fixed tool pipeline.

When a specialized trigger fires and availability is unknown, use a cheap non-mutating capability probe when practical. If the capability is available/current/supported and directly models the claim, presumptively use it; otherwise take a concrete fallback such as unsupported backend/language, unavailable tool surface, stale/unreliable analysis state that cannot economically be refreshed, model mismatch, disproportionate setup for a trivially bounded claim, or already-available evidence that establishes the same claim at least as reliably and more cheaply. Familiarity with built-in search/read/shell/test tools is not itself a fallback reason.

### Domain-conditional routes

- Repository inspection strategy/context economy -> [Repository intake](references/repository-intake.md).
- Recurrence/family closure/review readiness/review saturation/revision economy -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md).
- D4 specification/API/schema fidelity -> [Specification and implementation](references/specification-and-implementation.md).
- Evidence/document communication -> [Documentation and evidence](references/documentation-and-evidence.md).
- Release/package mechanics -> [Release and distribution](references/release-and-distribution.md).
- Configuration -> [Configuration and policy](references/configuration-and-policy.md).
- Orchestration/concurrency -> [Concurrency and orchestration](references/concurrency-and-orchestration.md).
- Security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md).
- Performance/resources/parallelism/hardware -> [Performance and parallelism](references/performance-and-parallelism.md).
- Storage/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md).
- Substantial executable workplan -> [D3->D4 implementation workplan template](templates/implementation_workplan_template.md).

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

## Active simplicity and convergence

A first clean local defect remains local. Material sibling recurrence changes the unit of reasoning to the shared owner/mechanism; it does not answer whether the current realization should survive. When repeated patches, wrappers, fallbacks, duplicated/synchronized state, competing authorities, lifecycle machinery, or an evident simpler equivalent realization show architecture-created complexity, remove, narrow, alter, consolidate, refactor, or re-derive delegated machinery before another additive durable repair.

If the simpler solution changes accepted D3 architecture, perform bounded D3 reconsideration. If the problem is actually D2/D1, route upstream rather than designing around it. Recurrence is evidence about the shared owner/mechanism, not authority for preserving that mechanism.

## Review, Verification, and Serious Challenge

Independent D4 Review reconstructs applicable D1/D2 semantics, D3 architecture, D4 specification/workplan, and actual candidate behavior before relying on implementer rationale. Prefer fresh context for substantial/high-risk review. Attempt targeted falsification of conformance, abstraction adequacy, ownership, affected surfaces, testing, reliability/security, scaling/resources, compatibility, and complexity.

Review first asks whether **literal compliance actually realizes the protected stakeholder outcome** and every applicable upstream semantic outcome. If the implementation misses a sufficient accepted contract, that is implementation nonconformance. If the literal workplan/architecture contract is itself too weak or wrong for the protected outcome, classify a **workplan/design deficiency** at the earliest owning domain rather than blessing a compliant-but-wrong realization.

When material acceptance depends on an actual D4 path, identify the historical **product/Frozen claim and the real semantic owner/path of the current realization**—now interpreted as the applicable parent/cycle-freeze claim plus its current delegated owner—and ask whether the evidence **could remain green** while that owner is broken. This compatibility vocabulary preserves Protocol 5 proxy-proof reasoning without promoting D4 machinery into D3 authority.

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
