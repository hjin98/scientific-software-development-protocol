# Development Workflow Orchestration Prompts

This file is the canonical **human-facing prompt entrypoint** for orchestrating the Software Development Protocol across common development stages.

The prompts do not create new protocol authority. They route a user request into the existing protocol skills and references with enough stage-specific control to make skill activation, evidence gathering, authority handling, and handoff behavior reliable.

## How to use this reference

1. Choose the stage that matches the current development state.
2. Copy that stage prompt as a whole.
3. Edit only the `INPUTS` block at the top unless the task genuinely needs an additional explicit user constraint.
4. Define each input once. The rest of the prompt refers to the variable name instead of repeating paths, branches, workplan names, or authorities.
5. Use `AUTO` when the agent should discover the value from the repository/protocol, and `NONE` when the parameter intentionally does not apply.
6. Input variables identify task context; they do not override higher-authority product requirements, Frozen architecture, safety rules, or repository/project instructions.

For substantial work, the common lifecycle is:

```text
design/workplan
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

---

## 1. Design / Workplan

```text
INPUTS
TASK = [describe the stakeholder, scientific, computational, architectural, or operational change/problem]
REPOSITORY_TARGET = [repository/worktree/branch to inspect; AUTO = current repository]
EXISTING_AUTHORITIES = [existing workplans/specifications/architecture/method papers/contracts to preserve or reconcile; AUTO = discover relevant authorities]
WORKPLAN_DESTINATION = [desired workplan path; AUTO = repository convention]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-design` skill from PROTOCOL_SOURCE.

Diagnose TASK from the actual state of REPOSITORY_TARGET and create or update the governing workplan at WORKPLAN_DESTINATION. Load and reconcile EXISTING_AUTHORITIES rather than treating any single surface-level document as automatically complete.

State the original stakeholder/scientific/computational/operational problem independently of the current realization where possible. Explicitly separate:
1. problem/product invariants;
2. Frozen high-level architecture for this implementation cycle; and
3. delegated solution space.

Freeze only architecture-level decisions that genuinely need to remain invariant during implementation. Do not promote existing helpers, wrappers, state machines, intermediate representations, prior patches, or implementation-created constraints into requirements merely because they already exist.

Inspect the real implementation, callers, tests, specifications, architecture documentation, relevant scientific/method documentation, and other affected authorities sufficiently to ensure that the plan describes the actual engineering problem rather than a superficial repository interpretation.

Prefer the minimum justified total product/system complexity. Before proposing new machinery, determine whether the problem can instead be solved by removing, narrowing, rewiring, consolidating, or replacing existing Tier-2 machinery.

Define the affected and owning surfaces, scientific/numerical invariants where relevant, real semantic-owner acceptance boundaries, focused/affected-regression/integration acceptance, relevant resource/performance requirements, simplification triggers, genuine Design-reopen triggers, and explicit non-goals.

Apply the protocol's relation-first tool routing for each material engineering question. When a specialized capability directly models the question and is available/current, use it. If it is unavailable, use a concrete justified fallback rather than silently defaulting to generic search.

Do not implement the solution in this stage.

Finish with a Pass / No-Pass verdict on whether the resulting workplan is snapshot-complete, internally coherent, and ready for Implementation.
```

---

## 2. Implementation

```text
INPUTS
WORKPLAN = [governing workplan path/identifier]
REPOSITORY_TARGET = [repository/worktree/branch to modify; AUTO = current repository]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-implementation` skill from PROTOCOL_SOURCE.

Implement WORKPLAN in full against the current state of REPOSITORY_TARGET.

Treat the workplan's problem/product invariants and explicitly Frozen high-level architecture as binding. Treat delegated implementation machinery as replaceable. Prefer an equivalent simpler realization when it preserves the binding contract.

Implement at the semantic owning layer. Do not add a patch, wrapper, adapter, fallback, synchronization mechanism, state, compatibility path, or other durable machinery merely to compensate for a problem created by the current realization when removal, rewiring, consolidation, narrowing, or replacement solves the underlying problem more cleanly.

Prefer reduction or alteration over addition when engineering-equivalent. New machinery must either provide a genuinely missing Tier-1/Frozen capability or replace broader existing complexity so that total system complexity decreases.

If implementation evidence invalidates a Frozen architecture decision, stop dependent work and route only the affected design surface back to `software-design`. Do not silently redesign around WORKPLAN.

For each material engineering question, apply the protocol's relation-first tool routing. Use semantic navigation, structural analysis, property/generative testing, data-flow analysis, debuggers, sanitizers, profilers, or other specialized capabilities when their relation is triggered and they provide higher-information evidence. Do not invoke tools ceremonially, but do not ignore a directly triggered specialized capability merely because generic search is familiar.

For executable changes:
- close each material behavior-changing stage semantically and functionally;
- run focused checks and stage-local affected regression before dependent work proceeds;
- parallelize tests only when the suite supports safe parallel execution;
- size test parallelism from the effective CPU allocation and resource limits of the current environment rather than raw host CPU count;
- avoid nested oversubscription and resource-exhaustive execution;
- do not rerun unchanged evidence without a plausible invalidating change or useful information gain.

Regression scope must include every behavior plausibly affected directly or transitively by the implementation. If the affected surface cannot be bounded confidently, broaden to the relevant larger/full regression suite rather than assuming unexamined targets are unaffected.

Before completion:
1. reconcile the complete accepted WORKPLAN against the assembled implementation;
2. inspect for superseded machinery, stale paths, duplicate authority, unnecessary wrappers/fallbacks, ownership drift, and accidental complexity;
3. re-derive the affected behavioral surface from the final implementation;
4. run the complete required affected regression;
5. run required integration/end-to-end paths through the real production semantic owners;
6. run repository/project-required checks;
7. report any unavailable required acceptance evidence explicitly.

Do not manufacture success by weakening tests, specifications, thresholds, fixtures, or acceptance boundaries.

Report material implementation decisions, simplifications, legitimate delegated-space reconciliations, tests and tools actually executed, unavailable checks, and unresolved risks.
```

---

## 3. Review & Update

```text
INPUTS
WORKPLAN = [governing workplan path/identifier]
IMPLEMENTATION_TARGET = [implemented branch/commit/worktree; AUTO = current implementation]
RELATED_AUTHORITIES = [parent/relative workplans, architecture, specifications, method papers, contracts; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-design` skill from PROTOCOL_SOURCE in independent implementation-review mode.

WORKPLAN has been implemented in IMPLEMENTATION_TARGET. Thoroughly review the assembled current implementation, not merely its diff or the implementer's summary. Reconcile WORKPLAN with RELATED_AUTHORITIES and the actual repository state.

Prefer a fresh review context where practical. Treat implementation explanations and previous review conclusions as evidence, not authority. Independently reconstruct the relevant behavior from the governing workplan, current code, tests, architecture/specifications, and affected product paths.

Review in two passes.

First, contract/outcome conformance: determine whether the implementation actually realizes every still-binding problem/product invariant, Frozen architectural decision, acceptance boundary, and required scientific/numerical behavior.

Second, independent engineering challenge: actively search for defects or unjustified assumptions in correctness, scientific methodology, numerical behavior, ownership, architecture, state transitions, persistence/recovery, concurrency, resources, performance, security, affected-surface coverage, testing quality, and total system complexity.

For each material engineering question, apply the protocol's relation-first tool routing. Use specialized semantic, structural, generative, data-flow, runtime, memory, race, performance, or other evidence channels when they directly model the claim.

Do not merely confirm that tests are green. Determine whether the tests could remain green while the real semantic owner or claimed behavior is materially broken.

Classify every material finding as one of:
- implementation nonconformance — the existing workplan is sufficient and implementation must be repaired;
- workplan/design deficiency — the governing design is incomplete or incorrect and must be reconciled before reimplementation;
- newly discovered affected behavior under existing authority — implementation/test scope must expand without inventing a new product requirement;
- independent unrelated issue — record separately unless it materially interacts with the active work.

Do not revise governing semantics merely to make IMPLEMENTATION_TARGET compliant.

When proposing repair, first challenge whether the problem is caused only by delegated Tier-2 machinery. Do not prescribe another patch, wrapper, adapter, fallback, or special case when removal, rewiring, consolidation, or replacement eliminates the cause more cleanly.

Issue Pass / No-Pass based only on genuine material blockers.

If blockers remain:
- reopen only the affected workplan/design surface;
- preserve still-valid Frozen decisions and accepted evidence;
- add precise, implementation-actionable repair instructions;
- distinguish clearly whether repair is implementation-only or requires Design reconsideration;
- do not create a new numbered authority revision merely because another implementation/review iteration is required.

If no blockers remain and all workplan-required acceptance/qualification obligations are complete or explicitly outside the plan, close WORKPLAN.

Do not modify production implementation during this review stage.
```

---

## 4. Verification

```text
INPUTS
VERIFICATION_SCOPE = [subsystem/workplan/feature/campaign/release whose claims must be verified]
IMPLEMENTATION_TARGET = [branch/commit/worktree to verify; AUTO = current implementation]
GOVERNING_DESIGN = [Frozen architecture/specifications/workplans/product contracts; AUTO = discover relevant normative authorities]
SCIENTIFIC_AUTHORITIES = [method papers/equations/reference methods/domain documentation; AUTO = discover relevant authorities; NONE if non-scientific]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-design` skill from PROTOCOL_SOURCE in independent adversarial-verification mode.

Verify that IMPLEMENTATION_TARGET faithfully realizes the Frozen scientific, computational, product, and architectural design governing VERIFICATION_SCOPE.

Prefer a fresh context independent of the implementation trajectory. The objective is to falsify incorrect claims, not to confirm the implementer's reasoning.

Begin by reconstructing the authority map. Distinguish stakeholder/product requirements, Frozen architecture and current normative specifications, scientific/methodological authorities, implementation code as evidence of actual behavior, and tests/benchmarks/documentation as evidence rather than automatic truth.

Do not assume any single documentation layer is correct merely because it is labeled architecture, specification, manual, workplan, or method documentation. Search broadly enough across IMPLEMENTATION_TARGET, GOVERNING_DESIGN, SCIENTIFIC_AUTHORITIES, and other relevant authorities to detect contradictions. When authorities disagree, determine which authority is normative and surface the conflict rather than silently choosing the implementation.

Verify material claims through their real semantic owner and real production path. Evidence that could remain green while the claimed production owner is broken cannot establish the claim.

For scientific/numerical behavior, explicitly challenge as applicable: mathematical/statistical methodology; units and conventions; normalization; indexing/ordering/sign conventions; checkpoint/restart semantics; estimator/sample semantics; algorithmic boundaries; conservation/symmetry/monotonicity/invariance/equivariance; precision and justified tolerances; reference-versus-optimized/backend equivalence; deterministic/stochastic behavior; and data selection/ranking/weighting/filtering/aggregation/stopping logic.

Use reference implementations, differential testing, metamorphic testing, property/generative testing, counterexamples, mutation-style reasoning, and targeted executable experiments when they materially strengthen a claim.

Apply the protocol's relation-first tool routing to each material engineering question and use the highest-information appropriate evidence channel available.

Search specifically for cases where:
- code can violate a documented claim while tests remain green;
- documentation and implementation share the same mistaken assumption;
- a helper test bypasses the production caller/orchestrator;
- a scientific method has been approximately or accidentally reimplemented;
- boundary cases exercise behavior different from nominal examples;
- historical patches changed semantics without corresponding architectural reconciliation.

Finish with Pass / No-Pass.

For each blocker, state:
1. the violated product/Frozen/scientific claim;
2. the actual implementation behavior;
3. evidence demonstrating the mismatch;
4. whether the problem is implementation nonconformance or a design/authority conflict;
5. the correct repair route.

Do not repair production implementation during this verification stage.
```

---

## 5. Stabilization / Architecture GC

```text
INPUTS
STABILIZATION_SCOPE = [completed subsystem/workplan/feature cluster/migration/repair sequence to stabilize]
IMPLEMENTATION_TARGET = [accepted branch/commit/worktree; AUTO = current implementation]
GOVERNING_AUTHORITY = [workplan/Frozen architecture/product constraints to preserve; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-design` skill from PROTOCOL_SOURCE in stabilization / architecture-GC mode.

Run this stage only after STABILIZATION_SCOPE has otherwise passed ordinary implementation review. The purpose is not to invent missing feature requirements. Determine whether the assembled accepted implementation has accumulated unnecessary Tier-2 complexity and whether it remains intellectually tractable for future development.

Evaluate IMPLEMENTATION_TARGET as if the current implementation had appeared fully formed today.

Ask: if we were implementing the same problem/product invariants and Frozen high-level architecture from the current repository state, would we deliberately choose this realization again?

Inspect STABILIZATION_SCOPE and its meaningful surrounding architecture for duplicated or synchronized domain representations; competing authority; wrappers/adapters/compatibility layers/retries/fallbacks/special cases; internal state machines created mainly to manage other machinery; unnecessary intermediate representations/conversion chains; ownership ambiguity; cross-module control leakage; circular or surprising dependencies; unnecessary configuration/public API surface; historical-exception conditionals; stale migration paths; dead/superseded/bypassed paths; test-only seams leaked into production; tests dominated by internal orchestration; duplicated algorithms/rules; and structures that require historical context to explain coherently.

Use structural analysis, dependency information, complexity/churn observations, duplication detection, git history, test-effectiveness evidence, and other maintainability signals when useful. Treat all metrics as sensors and prioritization evidence, never as product truth or automatic failure thresholds.

Classify material findings as:
- Tier-2 simplification — the same problem/Frozen architecture can be preserved through deletion, consolidation, rewiring, narrowing, representation unification, ownership repair, or equivalent implementation-level simplification;
- Frozen-architecture concern — a materially simpler/coherent solution requires changing a Frozen decision and must route to bounded Design reconsideration;
- no material issue — remaining complexity is justified by real product/Frozen requirements or removal would not materially improve maintainability.

Do not implement refactors during this stabilization-review stage.

If material Tier-2 simplification is warranted, create or update a bounded stabilization workplan containing only justified simplifications and their required regression/integration evidence. Route that work through the normal Implementation -> Review cycle.

If Frozen architecture needs reconsideration, reopen only the affected design surface.

If no material simplification/design issue remains, declare STABILIZATION_SCOPE stable and ready for closeout.
```

---

## 6. Alignment of a Downstream Workplan

```text
INPUTS
DOWNSTREAM_WORKPLAN = [workplan that must be realigned before implementation]
UPSTREAM_ACCEPTED_WORK = [accepted/implemented predecessor workplans, commits, branches, migrations, or feature stages whose results change the starting state]
FROZEN_PARENT_AUTHORITY = [parent workplan/design/architecture that remains authoritative; AUTO = discover governing parent authority]
IMPLEMENTATION_TARGET = [repository/worktree/branch containing the accepted upstream state; AUTO = current repository]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-design` skill from PROTOCOL_SOURCE.

Re-align DOWNSTREAM_WORKPLAN with the accepted current implementation state produced by UPSTREAM_ACCEPTED_WORK in IMPLEMENTATION_TARGET.

FROZEN_PARENT_AUTHORITY remains authoritative unless explicitly reopened through the protocol's Design process. Treat UPSTREAM_ACCEPTED_WORK and the actual implementation as evidence of the repository's current state, not as permission to rewrite governing requirements around whatever code happens to exist.

Inspect the accepted upstream work sufficiently to determine:
- which assumptions in DOWNSTREAM_WORKPLAN are now satisfied;
- which delegated realization details changed legitimately;
- which expected files/symbols/owners no longer exist;
- which affected surfaces expanded or contracted;
- which implementation stages or obligations are now obsolete;
- which acceptance mappings must follow a legitimately replaced Tier-2 semantic owner;
- which newly discovered downstream consequences follow from already-binding parent authority.

Update DOWNSTREAM_WORKPLAN to describe the current implementation starting point accurately while preserving all still-binding parent problem/product invariants, Frozen architecture, non-goals, and acceptance requirements.

Remove obsolete implementation-history assumptions and already-completed obligations when they no longer serve the downstream plan. Prefer a coherent current-state plan over an append-only record of revisions.

Do not normalize implementation drift into DOWNSTREAM_WORKPLAN. If the accepted-looking upstream implementation actually violates FROZEN_PARENT_AUTHORITY, record the discrepancy and route it as implementation nonconformance or bounded Design reconsideration. Do not alter DOWNSTREAM_WORKPLAN merely to legitimize that drift.

Affected-surface expansion may change implementation/testing scope; it does not by itself create new product requirements or make implementation-created machinery invariant.

Apply the protocol's relation-first tool routing where semantic ownership, structural families, or other material relations require specialized evidence.

Finish with Pass / No-Pass on whether DOWNSTREAM_WORKPLAN is snapshot-complete, aligned to the real current starting state, and ready for Implementation.

Do not implement DOWNSTREAM_WORKPLAN during this stage.
```

---

## 7. Health Audit

```text
INPUTS
AUDIT_SCOPE = [repository, subsystem, package set, or architectural region to audit]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
HISTORY_WINDOW = [history range/release interval/commit range to consider; AUTO = enough history to identify material trends]
GOVERNING_ARCHITECTURE = [current architecture/product/scientific authorities; AUTO = discover relevant authorities]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
EXCLUSIONS = [explicitly excluded surfaces; NONE if absent]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use the `software-maintenance-audit` specialist from PROTOCOL_SOURCE when available. Until that specialist is implemented/available, use `software-design` in repository semantic-health audit mode under the same authority boundaries.

This is a periodic long-horizon repository audit, not a feature review and not a new approval gate.

Assess whether AUDIT_SCOPE is becoming more stable, coherent, testable, and simple over HISTORY_WINDOW, or whether locally defensible changes are producing architectural entropy that has not yet surfaced as an obvious implementation failure.

Inspect both the current repository and relevant development history. Prioritize change-sensitive risk rather than static ugliness alone.

Evaluate as applicable:
- high-churn x high-complexity code;
- high-churn x weak-test/oracle regions;
- highly central modules with disproportionate change risk;
- repeated bug-fix concentration and recurring semantic defect families;
- repeated edits to the same orchestration/state machinery;
- duplicated/synchronized domain representations and competing authorities;
- dependency cycles and boundary erosion;
- temporal change coupling between supposedly independent modules;
- wrapper/fallback/adapter/special-case accumulation;
- configuration/public API growth;
- stale compatibility/migration paths;
- increasing state-transition complexity;
- code duplication and parallel implementations of the same rule;
- mutation survivors or other evidence of weak tests in important code;
- weak changed-code coverage where material;
- scientific/numerical logic with inadequate invariant/reference/metamorphic protection;
- documentation that no longer describes a coherent present-tense system;
- completed/superseded workplans or lifecycle residue still appearing active;
- temporary diagnostics, test seams, or compatibility machinery that became accidentally permanent.

Use git history, semantic/structural tools, dependency analysis, complexity measures, coverage, mutation evidence, duplication analysis, documentation reconciliation, and other relevant signals where available and economical.

Metrics are sensors, not verdicts. Do not declare code unhealthy merely because a threshold is exceeded. Investigate whether the signal corresponds to a real maintenance, ownership, correctness, or architectural problem.

For each material finding, identify:
1. the affected subsystem;
2. the long-horizon evidence/trend;
3. the product/Frozen concern, if any;
4. whether the problem is Tier-2 realization debt or Frozen-architecture debt;
5. the smallest justified corrective scope;
6. the expected simplification or risk reduction.

Route findings as:
- Tier-2 simplification candidate -> bounded workplan and `software-implementation` when worthwhile;
- Frozen-architecture concern -> `software-design`;
- test/oracle weakness -> strengthen validation at the owning behavioral boundary;
- documentation reconciliation -> `software-documentation`;
- repository/lifecycle residue -> `repository-hygiene`;
- watch item -> retain as observation when evidence is insufficient to justify work.

Do not perform a repository-wide refactor merely because debt is visible. Do not create workplans whose maintenance cost exceeds the demonstrated problem.

Conclude with one of:
- HEALTHY — no material long-horizon deterioration requiring action;
- WATCH — meaningful signals exist but current evidence does not justify intervention;
- ACTION REQUIRED — evidence-backed problems materially threaten long-term correctness, architecture, maintainability, or development convergence.

When action is required, recommend the minimum coherent set of workplans needed to address root causes rather than one workplan per symptom.
```

---

## 8. Closeout

```text
INPUTS
COMPLETED_WORK = [completed workplan/feature/migration/release scope being closed]
IMPLEMENTATION_TARGET = [accepted branch/commit/worktree; AUTO = current repository]
AFFECTED_DOCUMENTATION = [known documentation surfaces; AUTO = discover affected durable documentation]
PROTOCOL_SOURCE = [installed software-development-protocol skills or repository/ref containing them; AUTO = available current protocol]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Use `software-documentation` and `repository-hygiene` from PROTOCOL_SOURCE when their respective protocol triggers apply.

Run this stage only after the relevant implementation, review, required verification, stabilization, and required qualification for COMPLETED_WORK have closed.

First reconcile durable documentation with the accepted present system when COMPLETED_WORK materially changed architecture, scientific methodology/interpretation, public APIs/configuration, workflows, persistence/state semantics, performance/resource behavior, or user-facing behavior.

Write current documentation as a coherent description of the accepted present system, not an append-only history of patches and workplan revisions.

Then perform conservative repository-hygiene closeout.

Verify that:
- completed workplans are moved out of active state according to repository convention;
- superseded temporary plans and coordination artifacts are classified correctly;
- generated artifacts match canonical sources;
- temporary diagnostics, test residue, caches, and scratch outputs are removed only when positively proven disposable;
- stale branches are considered separately under branch-safety rules;
- no active evidence, unique work, compatibility material, or recoverable state is lost;
- repository indexes/navigation reflect the accepted current lifecycle state.

Do not alter product behavior during closeout. Any semantic defect discovered here routes back to the appropriate Design/Implementation stage.

Finish by reporting documentation reconciled, workplans archived/closed, residue removed or intentionally retained, repository-state limitations, and unresolved lifecycle inconsistencies.
```

---

## Stage-selection rule of thumb

Use **Review & Update** to ask: *Was this workplan implemented correctly?*

Use **Verification** to ask: *Are the scientific, product, numerical, and architectural claims actually true in the real implementation?*

Use **Stabilization** to ask: *Even if correct, is the accepted realization now unnecessarily complicated?*

Use **Alignment** to ask: *Does a not-yet-implemented downstream plan still describe the repository state after accepted predecessor work?*

Use **Health Audit** to ask: *Across time and multiple changes, is the repository accumulating structural/test/ownership risk faster than it is being resolved?*

Use **Closeout** to make the accepted present system and repository lifecycle state coherent after engineering work is complete.
