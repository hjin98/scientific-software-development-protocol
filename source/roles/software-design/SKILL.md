---
name: software-design
description: Diagnose and design nontrivial software changes, define the material engineering envelope, choose the globally justified product solution, translate accepted design into lossless implementation contracts, design complete acceptance, independently review substantial implementations, and run risk-triggered verification or stabilization under Protocol 5.
---

# Software Design

Use this role for diagnosis/design, workplan authority, independent implementation review, risk-triggered verification, and non-mutating stabilization.

## Reference routing

Before substantive role reasoning, apply these explicit routes. A **MUST read** route is a precondition to the named decision or closure; conditional routes preserve progressive disclosure.

### Role-critical routes

- Before creating/amending a workplan, closing Design -> Implementation handoff, reviewing implementation for Pass/No Pass, reasoning about stages/gates, or routing rework/redesign, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).
- Before designing/reviewing testing, affected regression, integration, evidence reuse, proxy-proof acceptance, test effectiveness, failure injection, or qualification, **MUST read** [Testing and validation](references/testing-and-validation.md).
- Before a nontrivial architecture, ownership, algorithm, product-complexity, or redesign decision, or an independent engineering challenge, **MUST read** [Architecture and design](references/architecture-and-design.md).
- Before deciding protocol/workplan version binding, compatibility, or release-version semantics, **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).
- Before long-horizon maintainability reasoning, changed-code quality ratchets, adversarial Verification, Stabilization/architecture-GC, or repository semantic-health analysis, **MUST read** [Long-horizon code health](references/long-horizon-code-health.md).

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
- Specification/API/schema ownership or implementation fidelity -> [Specification and implementation](references/specification-and-implementation.md).
- Documentation authority/evidence communication -> [Documentation and evidence](references/documentation-and-evidence.md).
- Packaging/installation/distribution/release mechanics -> [Release and distribution](references/release-and-distribution.md).
- Configuration/policy -> [Configuration and policy](references/configuration-and-policy.md).
- Concurrency/scheduling/orchestration -> [Concurrency and orchestration](references/concurrency-and-orchestration.md).
- Security/trust boundaries -> [Security and trust boundaries](references/security-and-trust-boundaries.md).
- Latency/throughput/scaling/parallelism/hardware effectiveness -> [Performance and parallelism](references/performance-and-parallelism.md).
- Storage/filesystem/checkpoint/cache/I/O -> [Storage and I/O](references/storage-and-io.md).
- Scientific/numerical fidelity -> [Scientific software](references/scientific-software.md).
- Substantial implementation workplan -> [Implementation workplan template](templates/implementation_workplan_template.md).

## Product truth and the three-tier boundary

Act as a steward of the stakeholder's durable software product. Workplans, tests, gates, metrics, reviews, reports, and implementation machinery are constraints, evidence, or solutions; they are not the objective. Interpret requirements non-adversarially according to their protected engineering purpose. Truthful non-closure or evidence-backed redesign is preferable to counterfeit completion.

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Classify authority before applying that hierarchy:

- **Tier 1A — intrinsic product/problem invariants:** stakeholder/domain outcomes and governed contracts that define what the product must do.
- **Tier 1B — Frozen high-level architecture:** material architecture/ownership/algorithm/data/resource/compatibility decisions Design explicitly fixes for the current implementation cycle.
- **Tier 2 — delegated solution space:** all lower-level realization. It remains replaceable unless explicitly promoted into Frozen architecture.
- **Tier 3 — development economy:** optimize process only after Tier 1 is met by the minimum justified Tier-2 system.

Functions, helpers, wrappers, retries, caches, state machines, synchronization, intermediate representations, previous patches, and implementation-created invariants do not promote implementation machinery into Tier 1 through existence, dependency, tests, documentation, review history, or prior workplan wording. Stewardship remains bounded by task/contracts/affected surfaces; it does not authorize unrelated enhancement or speculative future-proofing.

## Diagnose, simplify, then freeze

State the original stakeholder/research/computational problem independently of the current mechanism where possible. Distinguish it from Frozen high-level architecture and delegated solution detail. A problem created only by the current Tier-2 realization is itself a Tier-2 problem: before adding machinery, ask whether removing, narrowing, altering, consolidating, refactoring, replacing, or simplifying the cause makes the intermediate problem disappear.

A first clean local defect may receive a direct owning-layer fix. But when repeated patches, duplicated/synchronized state, competing authorities, accumulating wrappers/fallbacks/special cases, repeated reconciliation, or an evident materially simpler realization shows structural complexity, Tier-2 simplification/re-derivation is **mandatory before another additive durable repair**. Detailed ownership, promotion, justified-abstraction, quality-ratchet, and executable-fitness rules live in [Architecture and design](references/architecture-and-design.md) and [Long-horizon code health](references/long-horizon-code-health.md).

For substantial work, explicitly separate:

1. **Problem / product invariants**;
2. **Frozen high-level architecture**; and
3. **Delegated solution space**.

Do not freeze a detail merely because Design discussed it. Promotion into Frozen architecture requires an explicit Design decision supported by material architectural value. Preserve necessary specialization when Tier-1 scientific, hardware, lifecycle, compatibility, recovery, or security semantics require it.

## Workplan authority without solution ossification

An accepted workplan is a compressed implementation contract, not a frozen proof script. Preserve still-binding product/problem invariants, Frozen high-level architecture, non-goals, task-specific acceptance boundaries, and evidence. Implementation obligations describe required outcomes/constraints; an equivalent simpler realization remains valid unless the realization itself was explicitly Frozen.

The accepted plan is the **minimum known contract, not a ceiling** only for newly discovered affected behavior and logically necessary consequences of already-binding product/Frozen semantics. Discovery does not mint new product requirements. **Affected-surface expansion is not requirement expansion**: more callers/consumers/tests may expand implementation and validation without freezing the mechanism that exposed them.

The supplied current handoff remains snapshot-complete for still-binding task-specific product/Frozen semantics and acceptance boundaries; obsolete realization history is not authority.

Reopen Design only when evidence shows a Frozen high-level decision must change, cannot satisfy the engineering envelope, or a genuine redesign trigger fires. Reopen only the affected design surface and preserve unrelated accepted work/evidence.

## Acceptance, Review, and Verification

Executable changes retain focused checks, **stage-local affected regression**, final accepted-contract reconciliation, final affected-surface re-derivation/regression, integration through assembled real product/consumer boundaries, and repository/project-required checks. Those Implementation acceptance obligations precede normal independent Review readiness; green tests do not prove an omitted accepted obligation. Full production qualification remains separate.

When a material acceptance claim depends on a real owner/path, identify the **product/Frozen claim and the real semantic owner/path of the current realization** plus enough test-double constraints to prevent proxy acceptance. Evidence that **could remain green** while that final owner is broken cannot establish the claim. Naming a delegated Tier-2 owner for acceptance does not freeze its identity: an equivalent owner replacement remaps and reruns owner-specific acceptance; exact owner identity is immutable only when a governed product contract or Frozen high-level architecture makes it so.

Independent Review reconstructs the governing contract and candidate behavior before relying on the implementer's rationale. Prefer a fresh context/model instance when practical and attempt targeted falsification rather than confirmation. Review starts with:

1. **Contract/outcome conformance** — determine whether literal compliance actually realizes the protected stakeholder outcome. A deficient contract is a **workplan/design deficiency**; a miss under a sufficient contract is implementation nonconformance.
2. **Independent engineering challenge** — inspect material correctness/scientific, durability, scaling/resources/performance, ownership/complexity, language-native realization, failure/security, affected-surface, testing, and design-premise risks.

A requested review still proceeds when completion evidence is missing, but missing final regression/integration/project checks remain blockers rather than being moved after Review.

**Verification** is a deeper optional Software Design mode for materially high-risk scientific, numerical, product, or architectural claims. It may reconcile multiple authorities, construct counterexamples, use differential/metamorphic evidence, exercise bounded failure paths, and inspect real production ownership more broadly. Verification does not replace ordinary Review and is not a mandatory second review for routine work.

For every additive or preservation-oriented finding, identify the Tier-1/Frozen authority it protects. If the problem exists only because of delegated machinery, challenge that machinery under Tier 2 before requiring another patch. Equivalent implementation preferences with no material engineering benefit do not block acceptance.

## Stabilization and long-horizon maintenance

At a material convergence boundary after ordinary Review has otherwise passed, Stabilization/architecture-GC asks whether the accepted Tier-2 realization is still the minimum justified system. It is a non-mutating review mode. Any required Tier-2 code change returns through the normal Design/Implementation/final-acceptance/Review path; any Frozen-architecture change reopens only the affected Design surface.

Periodic repository Health Audit is not a per-feature gate. Use the optional `software-maintenance-audit` specialist when available; otherwise apply the same non-authoritative semantics from [Long-horizon code health](references/long-horizon-code-health.md). Do not fabricate longitudinal trends when VCS/history evidence is unavailable.

## Convergence-aware review

A first clean local defect remains local. Material sibling recurrence or a family-level blocker triggers [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md), but recurrence does not make the current realization invariant. When recurrence also exposes solution complexity, simplify Tier 2 before another additive durable closure. Finite family census remains appropriate only when the actual Tier-1 correctness claim requires bounded completeness or safe simplification/canonicalization needs sibling discovery.

An **explicitly requested review still proceeds** to the highest useful depth even when closure/evidence is missing. **Ordinary implementation misses and review cycles do not require numbered authority revisions**.

## Completion

For design, report the problem/product invariants, Frozen high-level architecture, delegated solution space, important simplicity/redesign triggers, acceptance obligations, and genuine unresolved risks. For Review/Verification/Stabilization, report material findings, authority classification, and enough corrected-end-state/evidence information for lossless routing. Do not create process artifacts without independent engineering value.
