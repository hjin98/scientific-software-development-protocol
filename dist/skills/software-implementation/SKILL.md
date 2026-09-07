---
name: software-implementation
description: Implement, refactor, test, benchmark, and validate accepted software designs under Protocol 5 with lossless requirement conformance, adaptive repository reconciliation, stage-local semantic plus functional closure, final affected-surface regression/integration, and robust delivery.
---

# Software Implementation

Implement the accepted product/problem requirements and Frozen high-level design as the globally best justified realization for the target environment.

## Reference routing

Before substantive implementation reasoning, apply these explicit routes. A **MUST read** route is a precondition to the named decision or closure; conditional routes preserve progressive disclosure.

### Role-critical routes

- Before implementing from an accepted workplan, closing a material stage, performing local reconciliation, or routing a material redesign, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).
- Before claiming executable stage/final acceptance or reasoning about affected regression, integration, evidence reuse, semantic-owner/test-double boundaries, or qualification, **MUST read** [Testing and validation](references/testing-and-validation.md).
- Before a material ownership/refactor/architecture/algorithm/complexity/redesign decision, **MUST read** [Architecture and design](references/architecture-and-design.md).
- Before deciding protocol/workplan version binding, compatibility, or release-version semantics, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

- Before reasoning about changed-code quality ratchets, test-oracle strength, maintainability hotspots, architecture fitness, bounded failure injection, or long-horizon structural risk, **MUST read** [Long-horizon code health](references/long-horizon-code-health.md).


### Language-profile dispatch

For material executable work, language semantics are part of the normal implementation path rather than an optional performance appendix.

- First **MUST read** [Language engineering profiles](references/language-profiles.md) to classify the affected runtime/build surface.
- For materially affected Python executable surfaces, **MUST read** [Python engineering](references/python-engineering.md).
- For materially affected C++ executable surfaces, **MUST read** [C++ engineering](references/cpp-engineering.md).
- Mixed Python/C++ boundaries **MUST read both** language profiles and apply the router's boundary rules. Tiny literal/text/config-only work may remain on shared doctrine when language semantics cannot alter the decision.

Shared owners outrank language profiles. Implement idiomatically for the active language/runtime while preserving the accepted product/Frozen contract and minimum justified total complexity.

### Per-question tool dispatch

Classify each material engineering question by the relation under the claim, not once per task:

- literal/path/text lookup or small deterministic local inspection -> ordinary repository search/read normally remains sufficient;
- symbol ownership/definition/callers/references/implementations, bounded semantic navigation, or symbol-aware editing -> **MUST read** [Serena](references/tool-serena.md) before relying solely on lower-information defaults;
- AST/syntax/structural patterns, diagnosed variants, forbidden/legacy constructs, or structural absence/uniqueness -> **MUST read** [Semgrep](references/tool-semgrep.md);
- broad/combinatorial Python input/state invariants -> **MUST read** [Hypothesis](references/tool-hypothesis.md);
- broad/combinatorial non-Python input/state invariants -> use the language-appropriate property/generative route in [Tool-assisted engineering](references/tool-assisted-engineering.md) plus the active language profile;
- supported interprocedural flow/taint/source-to-sink relations -> **MUST read** [CodeQL](references/tool-codeql.md).

Runtime-state/debugger, memory/lifetime/UB, race/synchronization, and performance/vectorization questions route through Tool-assisted engineering plus the active language profile rather than a fixed tool sequence. For overlaps/composition/common evidence limits, read [Tool-assisted engineering](references/tool-assisted-engineering.md).

When a specialized trigger fires and availability is unknown, use a cheap non-mutating capability probe when practical. If the capability is available/current/supported and directly models the claim, presumptively use it; otherwise take a concrete fallback such as unsupported backend/language, unavailable tool surface, stale/unreliable analysis state that cannot economically be refreshed, model mismatch, disproportionate setup for a trivially bounded claim, or already-available evidence that establishes the same claim at least as reliably and more cheaply. Familiarity with built-in search/read/shell/test tools is not itself a fallback reason.

### Domain-conditional routes

- Repository inspection strategy/context economy -> [Repository intake](references/repository-intake.md).
- Recurrence/family closure/review readiness/review saturation/revision economy -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md).
- Debugging/recovery/state reconstruction -> [Debugging and state recovery](references/debugging-and-state-recovery.md).
- Specification/API/schema ownership or implementation fidelity -> [Specification and implementation](references/specification-and-implementation.md).
- Documentation authority/evidence communication -> [Documentation and evidence](references/documentation-and-evidence.md).
- Packaging/installation/distribution/release mechanics -> [Release and distribution](references/release-and-distribution.md).
- Git/branches/commits/version-control operations -> [Git and version control](references/git-and-version-control.md).
- Configuration/policy -> [Configuration and policy](references/configuration-and-policy.md).
- Concurrency/scheduling/orchestration -> [Concurrency and orchestration](references/concurrency-and-orchestration.md).
- Security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md).
- Latency/throughput/scaling/parallelism/hardware effectiveness -> [Performance and parallelism](references/performance-and-parallelism.md).
- Storage/filesystem/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md).
- Scientific/numerical fidelity -> [Scientific software](references/scientific-software.md).

## Product truth and solution authority

Act as a steward of the stakeholder's durable software product. The workplan, tests, gates, metrics, reviews, reports, and current implementation are evidence, constraints, or solution machinery; they are not the objective. Interpret requirements according to their **protected engineering purpose**.

Never manufacture acceptance by weakening affected tests/specifications, hiding failures, bypassing required owners, or adding unjustified permissive fallbacks. If later evidence proves work unsound, **invalidate it and repair/retest**. **Truthful non-closure** is preferable to **counterfeit completion**, but is not permission to stop while a reasonable in-scope engineering path remains.

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Intake three classes separately: **problem/product invariants**, **Frozen high-level architecture**, and **delegated solution space**. Existing helpers, wrappers, retries, caches, state machines, adapters, synchronization, intermediate invariants, and previous patches remain Tier 2 unless current authority explicitly freezes the high-level decision they embody. **Implementation history does not promote machinery into Tier 1** through dependency, tests, documentation, review, or previous repair.

Consume the accepted current handoff as the complete task-specific authority for its scope. Unavailable history is not a normal source of requirements; a still-binding requirement that cannot be recovered from supplied authority is a **workplan/design deficiency**.

## Adaptive realization and bounded redesign

1. **Implementation realization** — local mechanics preserve product/Frozen semantics; proceed.
2. **Local reconciliation** — an **equivalent local realization**, including deletion/consolidation/refactoring of expected Tier-2 machinery, preserves product/Frozen semantics; proceed.
3. **Material redesign** — a Frozen high-level decision must change; stop dependent work and reopen Design on evidence.

Redesign needs evidence such as irreconcilable ownership/contract conflict, inability to meet a requirement, **representative measurement invalidating a premise**, or a stated trigger. Reopen only the affected surface, preserve unrelated work/evidence, resume from the **earliest materially affected stage**, and **do not reopen unrelated design** merely because affected surface grows or another architecture exists.

The accepted plan is the **minimum known contract, not a ceiling** only for **newly discovered affected behavior** and logically necessary consequences of existing product/Frozen authority. Discovery does not mint a new product requirement. **Affected-surface growth does not itself create a new product requirement or freeze the mechanism that caused the impact.**

## Implement at the owning layer; actively restore simplicity

Prefer direct control flow, one authoritative state, cohesive ownership, semantic reuse, consolidation, and deletion of obsolete paths. **Fix a clear local defect at the owning layer** rather than wrapping it.

A problem caused only by the current realization is a Tier-2 problem. Before adding durable machinery, ask whether removing, narrowing, altering, consolidating, refactoring, or replacing the cause eliminates it.

A clean first local defect remains lightweight. But repeated patches, patch-on-patch repair, wrappers/adapters/retries/fallbacks/special cases, duplicated/synchronized state, competing authorities, repeated reconciliation, or an evident materially simpler realization makes Tier-2 simplification/re-derivation **mandatory before another additive durable repair**.

When triggered:

```text
recover Tier-1 product/problem invariants
-> recover Frozen high-level architecture
-> treat lower-level machinery as replaceable
-> remove / narrow / alter / consolidate / refactor where sufficient
-> add machinery only for a genuinely missing required capability
   or when one canonical mechanism replaces broader existing complexity
```

This is not a line-count rule. New machinery is justified when Tier-1/Frozen requirements need a capability the simplified system cannot supply cleanly, or when it reduces total complexity by replacing broader machinery. Detailed criteria live in [Architecture and design](references/architecture-and-design.md).

For material Python/C++ code, this owning-layer rule includes language-native realization: do not preserve Python compensating machinery when C++ offers a simpler value/lifetime/runtime model, and do not reproduce low-level C++ machinery in Python when a high-level compiled/library path is simpler and sufficient. Performance complexity must earn its source/build/dependency/maintenance cost under the shared performance owner.

## Quality ratchet and long-horizon evidence

For substantial or structurally risky work, compare the materially touched subsystem against only the baseline evidence needed for the change. Existing debt does not excuse making touched code harder to reason about, more cyclic, more duplicated in authority, more weakly tested, or more dependent on special-case machinery unless product/Frozen authority requires the added complexity.

Treat complexity, coverage, mutation, duplication, churn, and similar metrics as sensors rather than product truth. When the material question is test effectiveness, changed-code protection, objective architecture dependency, hotspot risk, or failure/recovery behavior, route through [Long-horizon code health](references/long-horizon-code-health.md) and [Tool-assisted engineering](references/tool-assisted-engineering.md) instead of defaulting to a fixed analyzer pipeline.

When persistence/restart/orchestration recovery is part of the claim, use deterministic bounded failure injection or equivalent controlled simulation when it materially strengthens evidence. Keep the real semantic owner executing and do not substitute resource-exhaustive chaos for a bounded failpoint that establishes the same behavior.


## Convergence trigger

If materially equivalent sibling behavior recurs, a canonical mechanism has bypasses, or review identifies a family-level blocker, **MUST read** [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md). Recurrence broadens reasoning to the shared owner/mechanism but does not make the current realization invariant. If recurrence also shows solution complexity, simplify Tier 2 before another equivalent additive repair. Use bounded family census when the actual Tier-1 claim is finite/exhaustive or safe simplification/canonicalization needs sibling discovery. Post-simplification recurrence or evidence that Frozen architecture is wrong routes to bounded Software Design reconsideration.

**No recurrence/review count can force acceptance**; escalation changes engineering method, not the pass threshold.

## Coherent stages and acceptance

**A local coherent behavior change is normally one material implementation stage.** Several tightly coupled caller/helper/test edits **do not become separate stages merely because** they touch separate files/functions.

Each material stage closes semantically and functionally: accepted product/Frozen obligations remain satisfied, **newly discovered affected behavior** is accounted for, focused checks and relevant **stage-local affected regression** execute, and no unintended authority/stale path/unjustified complexity remains. Reuse still-valid intermediate evidence; green tests never prove an omitted obligation.

When acceptance depends on a production owner/state transition/consumer, the **real semantic owner/path of the final accepted realization that constitutes the claim must execute**. Evidence that **could remain green** while it is broken cannot close the claim. **Bounded test doubles remain valid below or outside** that boundary. A delegated Tier-2 owner named by earlier acceptance guidance may be replaced by an equivalent simpler owner when product/Frozen semantics survive; reconcile the acceptance mapping and invalidate/rerun owner-specific evidence against the new real owner. Do not treat that remapping as proxy-passing or Design reopening unless exact owner identity was itself product/Frozen authority. If a binding required boundary cannot execute, report **unavailable/blocking** rather than **silently proxy-passing** it.

For performance-sensitive work, distinguish implementation permission from performance evidence: an obvious semantically equivalent, low-complexity efficiency improvement need not wait for a pre-change benchmark, but quantitative speedup/scaling/resource claims require representative comparable measurement. Supported optimized/production build behavior must be exercised when build mode can change correctness; sanitizer/debug builds are complementary correctness evidence, not production-performance evidence.

Before completion:

1. **Reconcile the complete accepted contract**; **silent omission is not an accepted state**.
2. Inspect superseded machinery, ownership drift, fallbacks, and complexity; use **structural/source** or negative/absence evidence for removal/uniqueness claims.
3. **Re-derive the complete affected behavioral surface**.
4. Run the **complete affected-surface regression**, required **integration/end-to-end** paths, and repository/project-required checks; broaden when impact cannot be bounded.

Contract completeness and functional correctness are separate claims. Full **production qualification is separate**; a **production run never substitutes** for missing regression/integration.

## Completion

Honor explicit resource limits, update durable documentation when its contract changed, and remove obsolete task-owned machinery when safe. Emergency/hotfix mitigation may temporarily bypass the restoring simplification pass only when urgency independently requires it; keep it bounded and explicitly temporary.

Report material changes/reconciliations, checks actually executed, unavailable/blocking checks, and unresolved material risks. Do not emit empty protocol categories.
