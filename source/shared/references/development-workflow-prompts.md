# Development Workflow Orchestration Prompts

This file is the canonical **human-facing prompt entrypoint** for orchestrating the Software Development Protocol across common development stages.

The prompts do not create new protocol authority. They route a user request into the existing protocol skills and references with enough stage-specific control to make skill activation, evidence gathering, authority handling, and handoff behavior reliable across web and local agent harnesses.

## How to use this reference

1. Choose the stage that matches the current development state.
2. Copy that stage prompt as a whole.
3. Edit only the `INPUTS` block unless the task genuinely needs an additional explicit user constraint.
4. Define each input once. The rest of the prompt refers to the variable name instead of repeating paths, branches, workplan names, or authorities.
5. Use `AUTO_LOCAL_FIRST` for portable protocol-skill discovery, `AUTO` when the agent should infer a value from governing repository/protocol authority, and `NONE` when a parameter intentionally does not apply.
6. Input variables identify task context; they do not override higher-authority product requirements, Frozen architecture, safety rules, repository/project instructions, or the protocol version governing an accepted workplan.

For substantial work, the common lifecycle is:

```text
baseline / change-health intake when material
    -> design/workplan
    -> implementation
    -> review/update
         -> implementation repair loop when needed
    -> verification when scientific/architectural/high-risk claims warrant it
    -> stabilization at substantial milestone boundaries
         -> implementation/review loop when simplification is required
    -> closeout

alignment is used before a downstream workplan when accepted upstream work changed its assumed starting state.
health audit is periodic across accumulated repository history rather than mandatory after every local change.
```

Testing, verification, stabilization, qualification, documentation, and hygiene are modes or supporting capabilities. They do not create additional product-approval authorities beyond the protocol's Design and Implementation roles.

## Portable protocol-skill resolution

Every stage below is self-contained and includes `PROTOCOL_SOURCE` plus `PROTOCOL_REF` inputs. Unless the user explicitly supplies another source, resolve each required protocol skill **local first, public repository second**.

When `PROTOCOL_SOURCE = AUTO_LOCAL_FIRST`:

1. Inspect the current harness skill/plugin/command registry **and any documented exposed installed-skill root**. Use a governing-version-compatible local skill through the harness-native selector/invocation mechanism when callable, or read it from the exposed installed-skill root when the selector is user-only. Selectors such as `@software-design` or `/software-implementation` are harness selectors, **not shell commands**.
2. If no compatible local skill is readable, fall back to the canonical public repository `https://github.com/hjin98/software-development-protocol`, resolve an evidence-backed compatible repository ref, read `source/roles/<skill-name>/SKILL.md` or `source/specialists/<skill-name>/SKILL.md`, and load the references that entrypoint requires. `source/` is canonical; generated `dist/` bundles are transport artifacts.
3. Preserve governing protocol-version coherence. A newer installed skill may serve an older workplan only when it can explicitly preserve that older contract. Do not guess that a semantic version is a Git ref and do not silently substitute latest doctrine.
4. If neither a compatible local installation/root nor the compatible public source can be read, report **truthful non-closure** and do not claim protocol execution from memory or from a similarly named unrelated skill.

If `PROTOCOL_SOURCE` is explicit, use that source subject to protocol-version compatibility and higher-authority task/safety constraints.

---

## 0. Baseline / Change-Health Intake

```text
INPUTS
BASELINE_SCOPE = [subsystem/workplan/problem area whose before-state matters]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
GOVERNING_AUTHORITY = [product/Frozen/workplan authority to preserve; AUTO = discover relevant authority]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

Run this intake only when BASELINE_SCOPE is substantial or structurally risky enough that a before/after comparison will materially improve the quality-ratchet judgment. It is not a mandatory per-change gate.

Capture only the task-local evidence needed for later comparison, as applicable: important real-owner tests/acceptance paths; affected dependency and ownership structure; selected complexity/hotspot observations; public/configuration surface; trusted/reference behavior; known recurring defect or compatibility paths; and candidate identity.

Metrics are sensors, not verdicts. Do not create a permanent health ledger, repository-wide score, or new product requirement merely to perform this intake.

Carry the compact baseline into the following Design/Workplan stage or the task-local working state. Do not modify product implementation in this intake.
```

---

## 1. Design / Workplan

```text
INPUTS
TASK = [describe the stakeholder, scientific, computational, architectural, or operational change/problem]
REPOSITORY_TARGET = [repository/worktree/branch to inspect; AUTO = current repository]
EXISTING_AUTHORITIES = [existing workplans/specifications/architecture/method papers/contracts to preserve or reconcile; AUTO = discover relevant authorities]
WORKPLAN_DESTINATION = [desired workplan path; AUTO = repository convention]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing protocol version when task authority declares one, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

If TASK is substantial or structurally risky and no useful baseline was supplied, first capture the minimum task-local Baseline/Change-Health evidence needed for later quality-ratchet comparison. Do not turn that preamble into a mandatory per-change gate or persistent ledger.

Diagnose TASK from the actual state of REPOSITORY_TARGET and create or update the governing workplan at WORKPLAN_DESTINATION. Load and reconcile EXISTING_AUTHORITIES rather than treating any single surface-level document as automatically complete.

State the original stakeholder/scientific/computational/operational problem independently of the current realization where possible. Explicitly separate:
1. problem/product invariants;
2. Frozen high-level architecture for this implementation cycle; and
3. delegated solution space.

Freeze only architecture-level decisions that genuinely need to remain invariant during implementation. Do not promote existing helpers, wrappers, state machines, intermediate representations, prior patches, or implementation-created constraints into requirements merely because they already exist.

Inspect the real implementation, callers, tests, specifications, architecture documentation, relevant scientific/method documentation, and other affected authorities sufficiently to ensure that the plan describes the actual engineering problem rather than a superficial repository interpretation.

Prefer the minimum justified total product/system complexity. Before proposing new machinery, determine whether removal, narrowing, rewiring, consolidation, or replacement of Tier-2 machinery solves the problem more cleanly.

Define owning/affected surfaces, scientific/numerical invariants where relevant, real semantic-owner acceptance boundaries, focused/affected-regression/integration acceptance, relevant resource/performance requirements, simplification triggers, genuine Design-reopen triggers, and explicit non-goals.

Apply relation-first tool routing for each material engineering question. Do not implement the solution in this stage.

Finish with Pass / No-Pass on whether the workplan is snapshot-complete, internally coherent, and ready for Implementation.
```

---

## 2. Implementation

```text
INPUTS
WORKPLAN = [governing workplan path/identifier]
REPOSITORY_TARGET = [repository/worktree/branch to modify; AUTO = current repository]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = WORKPLAN's governing protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-implementation from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-implementation or /software-implementation are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

Implement WORKPLAN in full against REPOSITORY_TARGET. Treat its problem/product invariants and explicitly Frozen high-level architecture as binding; treat delegated machinery as replaceable.

Implement at the semantic owning layer. Prefer removal, narrowing, rewiring, consolidation, or replacement over another patch/wrapper/fallback/state when the current realization created the problem. New durable machinery must provide a genuinely missing Tier-1/Frozen capability or replace broader complexity.

If implementation evidence invalidates a Frozen decision, stop dependent work and route only the affected design surface back to software-design using the same portable resolution contract.

For executable changes, close each material stage semantically and functionally; run focused checks plus stage-local affected regression; size parallelism from effective allocation; avoid nested oversubscription and resource-exhaustive execution; and reuse still-valid evidence until a relevant dimension changes.

Before completion:
1. reconcile the complete WORKPLAN against the assembled implementation;
2. inspect superseded machinery, stale paths, duplicate authority, wrappers/fallbacks, ownership drift, and accidental complexity;
3. re-derive the final affected behavioral surface;
4. run complete affected regression;
5. run required real-owner integration/end-to-end paths; and
6. run repository/project-required checks.

Do not manufacture success by weakening tests, specifications, thresholds, fixtures, or acceptance boundaries. Report checks actually executed and any unavailable required evidence.
```

---

## 3. Review & Update

```text
INPUTS
WORKPLAN = [governing workplan path/identifier]
IMPLEMENTATION_TARGET = [implemented branch/commit/worktree; AUTO = current implementation]
RELATED_AUTHORITIES = [parent/relative workplans, architecture, specifications, method papers, contracts; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = WORKPLAN's governing protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version. Use the resolved skill in independent implementation-review mode.

Review the assembled current implementation, not merely its diff or implementer summary. Prefer a fresh context where practical and reconstruct the contract independently from WORKPLAN, RELATED_AUTHORITIES, repository state, tests, and product paths.

Review in two passes:
1. contract/outcome conformance against every still-binding product invariant, Frozen decision, acceptance boundary, and required scientific/numerical behavior;
2. independent engineering challenge across correctness, science, numerics, ownership, architecture, state/recovery, concurrency, resources, performance, security, affected-surface coverage, oracle quality, and total complexity.

Do not treat green tests as proof of an omitted obligation. Ask whether the evidence could stay green while the real semantic owner is broken.

Classify findings as implementation nonconformance, workplan/design deficiency, newly discovered affected behavior under existing authority, or independent unrelated issue. Do not rewrite governing semantics to bless implementation drift.

When repair is needed, challenge Tier-2 machinery before prescribing another patch/wrapper/fallback. Issue Pass / No-Pass only on genuine material blockers. If blocked, reopen only the affected workplan/design surface with precise repair instructions; do not create a numbered authority revision merely for another iteration.

Do not modify production implementation during Review.
```

---

## 4. Verification

```text
INPUTS
VERIFICATION_SCOPE = [subsystem/workplan/feature/campaign/release whose claims must be verified]
IMPLEMENTATION_TARGET = [branch/commit/worktree to verify; AUTO = current implementation]
GOVERNING_DESIGN = [Frozen architecture/specifications/workplans/product contracts; AUTO = discover relevant normative authorities]
SCIENTIFIC_AUTHORITIES = [method papers/equations/reference methods/domain documentation; AUTO = discover relevant authorities; NONE if non-scientific]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing workplan/design protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version. Use the resolved skill in independent adversarial-verification mode.

Verify that IMPLEMENTATION_TARGET faithfully realizes the Frozen scientific, computational, product, and architectural design governing VERIFICATION_SCOPE. Prefer a fresh context and attempt to falsify claims rather than confirm the implementer's rationale.

Reconstruct the authority map across product requirements, Frozen architecture/specifications, scientific/method authorities, implementation, tests, benchmarks, and documentation. No surface-level document or current code is automatic truth.

Verify material claims through the real semantic owner and production path. For scientific/numerical behavior challenge applicable mathematics/statistics, units/conventions, normalization, indexing/order/signs, restart/checkpoint semantics, estimator/sample semantics, algorithmic boundaries, conservation/symmetry/invariance/equivariance, tolerances, backend equivalence, stochastic behavior, and selection/ranking/weighting/filtering/aggregation/stopping logic.

Use reference, differential, metamorphic, property/generative, counterexample, mutation-style, and targeted executable evidence when it materially strengthens the claim. Search for shared wrong assumptions, production-owner bypasses, approximate reimplementations, boundary divergence, and historical semantic drift.

Finish with Pass / No-Pass and route blockers without repairing production implementation in this stage.
```

---

## 5. Stabilization / Architecture GC

```text
INPUTS
STABILIZATION_SCOPE = [completed subsystem/workplan/feature cluster/migration/repair sequence to stabilize]
IMPLEMENTATION_TARGET = [accepted branch/commit/worktree; AUTO = current implementation]
GOVERNING_AUTHORITY = [workplan/Frozen architecture/product constraints to preserve; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing workplan/design protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version. Use the resolved skill in stabilization / architecture-GC mode.

Run this stage only after STABILIZATION_SCOPE has otherwise passed ordinary implementation review. Ask whether the accepted Tier-2 realization would still be deliberately chosen today for the same product/Frozen contract.

Inspect duplicated/synchronized representations, competing authority, wrappers/adapters/compatibility/retry/fallback/special-case accumulation, machinery-driven states, unnecessary conversion chains, ownership leakage, dependency cycles, unnecessary config/API surface, historical-exception conditionals, stale migrations, dead/bypassed paths, test seams, orchestration-dominated tests, and duplicated rules.

Use metrics only as sensors. Classify findings as Tier-2 simplification, Frozen-architecture concern, or no material issue.

Stabilization is non-mutating. Tier-2 simplification routes through a bounded workplan when one is needed, then normal Implementation -> final acceptance -> Review. Frozen concerns reopen only the affected Design surface. If no material issue remains, declare the scope stable and ready for Closeout.
```

---

## 6. Alignment of a Downstream Workplan

```text
INPUTS
DOWNSTREAM_WORKPLAN = [workplan that must be realigned before implementation]
UPSTREAM_ACCEPTED_WORK = [accepted/implemented predecessor workplans, commits, branches, migrations, or feature stages whose results change the starting state]
FROZEN_PARENT_AUTHORITY = [parent workplan/design/architecture that remains authoritative; AUTO = discover governing parent authority]
IMPLEMENTATION_TARGET = [repository/worktree/branch containing the accepted upstream state; AUTO = current repository]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = DOWNSTREAM_WORKPLAN/FROZEN_PARENT_AUTHORITY governing protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILL = software-design from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-design or /software-design are not shell commands. If no compatible local skill is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical source skill plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor the compatible public source can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

Re-align DOWNSTREAM_WORKPLAN with the accepted current state produced by UPSTREAM_ACCEPTED_WORK while FROZEN_PARENT_AUTHORITY remains binding unless explicitly reopened.

Determine which downstream assumptions are satisfied, delegated realization details changed, expected owners disappeared, affected surfaces changed, stages became obsolete, acceptance mappings must follow a legitimately replaced Tier-2 owner, and downstream consequences follow from already-binding parent authority.

Update the downstream plan to the real current starting point and remove obsolete implementation-history assumptions. Do not normalize upstream implementation drift into the plan: if upstream violates parent authority, route that discrepancy as implementation nonconformance or bounded Design reconsideration.

Affected-surface growth changes implementation/testing scope, not product requirements. Finish with Pass / No-Pass on snapshot completeness and readiness for Implementation. Do not implement the downstream plan in this stage.
```

---

## 7. Health Audit

```text
INPUTS
AUDIT_SCOPE = [repository, subsystem, package set, or architectural region to audit]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
HISTORY_WINDOW = [history range/release interval/commit range to consider; AUTO = enough history to identify material trends]
GOVERNING_ARCHITECTURE = [current architecture/product/scientific authorities; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing architecture/workplan protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
EXCLUSIONS = [explicitly excluded surfaces; NONE if absent]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve PREFERRED_SKILL = software-maintenance-audit from PROTOCOL_SOURCE at PROTOCOL_REF. Under AUTO_LOCAL_FIRST, use a governing-version-compatible skill through a harness-native selector or documented exposed installed-skill root; selectors such as @software-maintenance-audit or /software-maintenance-audit are not shell commands. If no compatible local specialist is readable, fall back to https://github.com/hjin98/software-development-protocol and load the canonical specialist plus required references at an evidence-backed compatible ref. If that governing protocol version has no maintenance-audit specialist, resolve FALLBACK_SKILL = software-design through the same local-root/public-source contract and use semantic-health audit mode. If neither a compatible local installation/root nor compatible public source for the required/fallback skill can be read, report truthful non-closure and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

This is a periodic long-horizon repository audit, not a feature review or approval gate. Inspect current state plus trustworthy history and prioritize change-sensitive risk rather than static ugliness. If history is unavailable, report static risks without fabricating churn/change-coupling trends.

Evaluate as applicable: churn x complexity/test weakness/centrality; recurring defect families; repeated state/orchestration edits; duplicated/synchronized representations and competing authority; dependency cycles/boundary erosion; temporal coupling; wrapper/fallback/adapter/special-case accumulation; config/API/state growth; stale compatibility; duplication; mutation/coverage weakness; insufficient scientific invariant/reference/metamorphic protection; documentation incoherence; lifecycle residue; and temporary seams that became permanent.

Metrics are sensors, not verdicts. For each material finding state subsystem, evidence/trend, product/Frozen implication, Tier-2 versus Frozen debt, smallest justified corrective scope, and expected simplification/risk reduction.

Route findings by authority:
- local Tier-2 repair/simplification under already-sufficient existing authority -> `software-implementation`;
- substantial maintenance that needs a new or revised workplan/implementation contract -> `software-design` first, then Implementation only after that contract is accepted;
- Frozen-architecture concern -> `software-design`;
- test/oracle weakness -> strengthen validation at the owning behavioral boundary under the applicable existing/new workplan;
- documentation reconciliation -> `software-documentation`;
- repository/lifecycle residue -> `repository-hygiene`;
- insufficient evidence -> retain as a watch item.

Resolve every routed skill through the same governing-version-compatible harness-native selector or exposed installed-skill root -> canonical public source -> truthful non-closure chain before invoking it.

Do not perform a repository-wide refactor merely because debt is visible. Conclude HEALTHY, WATCH, or ACTION REQUIRED and recommend the minimum coherent root-cause work when action is justified.
```

---

## 8. Closeout

```text
INPUTS
COMPLETED_WORK = [completed workplan/feature/migration/release scope being closed]
IMPLEMENTATION_TARGET = [accepted branch/commit/worktree; AUTO = current repository]
AFFECTED_DOCUMENTATION = [known documentation surfaces; AUTO = discover affected durable documentation]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository fallback; otherwise explicit source]
PROTOCOL_REF = [AUTO = COMPLETED_WORK governing protocol version when declared, otherwise current compatible protocol; or explicit branch/tag/commit/version]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Before substantive work, resolve REQUIRED_SKILLS = [software-documentation, repository-hygiene] from PROTOCOL_SOURCE at PROTOCOL_REF when their respective triggers apply. Under AUTO_LOCAL_FIRST, resolve each skill independently through a harness-native selector or documented exposed governing-version-compatible installed-skill root; selectors such as @software-documentation, /software-documentation, @repository-hygiene, or /repository-hygiene are not shell commands. For each required skill not readable locally, fall back to https://github.com/hjin98/software-development-protocol and load its canonical specialist plus required references at an evidence-backed compatible ref. If neither a compatible local installation/root nor compatible public source can be read for a required skill, report truthful non-closure for that required closeout capability and do not claim protocol execution from memory. Do not silently substitute a different protocol version.

Run Closeout only after relevant implementation, Review, required Verification, Stabilization, and required qualification have closed.

Reconcile affected durable documentation with the accepted present system when architecture, science, public API/configuration, workflows, persistence/state, performance/resource behavior, or user-facing behavior changed. Write current-state documentation rather than patch chronology.

Then perform conservative repository hygiene: archive completed workplans according to repository policy; classify superseded temporary artifacts; verify generated artifacts against canonical source; remove only positively proven disposable diagnostics/cache/scratch; keep branch pruning under separate safety rules; preserve active evidence, unique work, compatibility material, and recoverable state; and update lifecycle indexes/navigation.

Do not alter product behavior during Closeout. Route any semantic defect back to the owning Design/Implementation stage using the same portable resolution contract.
```

---

## Stage-selection rule of thumb

Use **Baseline / Change-Health Intake** when substantial or structurally risky work needs a compact before-state for later quality-ratchet comparison.

Use **Review & Update** to ask: *Was this workplan implemented correctly?*

Use **Verification** to ask: *Are the scientific, product, numerical, and architectural claims actually true in the real implementation?*

Use **Stabilization** to ask: *Even if correct, is the accepted realization now unnecessarily complicated?*

Use **Alignment** to ask: *Does a not-yet-implemented downstream plan still describe the repository state after accepted predecessor work?*

Use **Health Audit** to ask: *Across time and multiple changes, is the repository accumulating structural/test/ownership risk faster than it is being resolved?*

Use **Closeout** to make the accepted present system and repository lifecycle state coherent after engineering work is complete.
