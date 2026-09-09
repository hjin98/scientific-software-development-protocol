# Scientific Software Development Workflow Prompts

This is the canonical human-facing orchestration source for Protocol 6.1. These are **execution prompts**, not advisory examples: under `AUTO_EXECUTE` the selected stage performs its authorized work with available tools and returns concrete artifacts/evidence rather than merely suggesting commands or next steps.

Protocol 6.1 routes work through the authority-bearing domain that actually owns the semantics rather than forcing every task through a four-stage waterfall.

## Portable protocol-skill resolution

Resolve compatible skills **local first, public repository second**.

When `PROTOCOL_SOURCE = AUTO_LOCAL_FIRST`:

1. Inspect the current harness skill/plugin/command registry and any **documented exposed installed-skill root**. Use a governing-version-compatible installed skill through the harness-native mechanism. Selectors such as `@software-design` or `/software-implementation` are harness selectors, **not shell commands**.
2. If no compatible local skill is readable, fall back to the canonical public repository `https://github.com/hjin98/scientific-software-development-protocol` and load `source/roles/<skill-name>/SKILL.md` or `source/specialists/<skill-name>/SKILL.md` plus the entrypoint's required references. `source/` is canonical; generated `dist/` is transport output.
3. Preserve governing protocol-version coherence. A workplan's declared `protocol_version` controls inherited semantics. **Do not guess that a semantic version is a Git ref** and **do not silently substitute a different protocol version** merely because current Protocol 6.1 is installed.
4. If neither a compatible local installation/root nor a compatible public source can be read, report **truthful non-closure** and **do not claim protocol execution from memory** or from a similarly named unrelated skill.

This resolution contract applies to every stage below; it is stated once here rather than duplicated eleven times.

## Execution contract

`AUTO_EXECUTE` means inspect the real target, resolve ordinary inferable context from repository/authority evidence, and perform every action the selected stage authorizes. **Do not stop at commands, patch suggestions, sample text, or "next steps"** when the same work can be performed with available authorized tools.

`REPORT_ONLY` prohibits repository/product mutation but still requires real inspection and the strongest available evidence.

Prefer action over clarification when ordinary context is discoverable. Ask only when proceeding would require guessing a genuinely consequential authority, semantic requirement, target, or irreversible action.

A stage may mutate only its owned authority/concretization surface. If evidence points to another domain, route explicitly rather than silently crossing the boundary. Review, Verification, Stabilization, and Health Audit remain non-product-mutation activities except for lifecycle/planning records that their stage explicitly owns.

When an unresolved Serious Challenge is proceeding under explicit human risk override, keep the dependent semantic surface visibly `risk-accepted/provisional`. In the terminal machine-readable footer, use the permitted additional field `authority_state = risk_accepted_provisional` (JSON key `authority_state`) for any result that depends on that unresolved claim. Do not reset the state to ordinary accepted-current merely because a descendant stage locally completes, and do not emit an unqualified downstream Pass/complete result for the affected claim.

For a material D1, D2, or durable D3 authority mutation, `accepted` means accepted-current only after an independent falsification pass by a reviewer/context that did not author the proposal and after any required human ratification. The proposing agent's own checks do not satisfy the independent pass. If the prerequisite evidence is unavailable, keep the authority proposed and return truthful `human_pending` where applicable or No-Pass rather than accepted-current. A later generic Review may add assurance, but it cannot retroactively legitimize authority that was marked accepted-current without this pre-acceptance pass.

## Evidence applicability and impact closure

Protocol 6.1 distinguishes an **evidence specification** from an **evidence realization**, its **observation**, and the resulting **evidence assessment**. A stale passing observation cannot confirm current authority and a stale failing observation cannot refute it until applicability is restored. Keep the governed evidentiary target distinct from replaceable execution dependencies.

When accepted authority or a material concretization changes, perform bounded manual impact closure over materially dependent descendants, evidence specifications/realizations, documentation/current dependency views, re-ratification obligations, retirement/cleanup, and semantic-evolution history. Preserve unaffected siblings and still-admissible evidence. Absence of an edge in a partial dependency view is not proof of independence.

## Stage-selection rule of thumb

Choose by **artifact and mutation boundary**, not keywords:

- scientific/mathematical meaning or model change -> **D1 Scientific & Mathematical Formulation**;
- estimator/discretization/solver/error/precision semantics -> **D2 Algorithm & Numerical Method Design**;
- software architecture/ownership/data-flow/resource/deployment change -> **D3 Software Architecture / Workplan**;
- implement, fix, refactor, test, package, or otherwise mutate product code under sufficient authority -> **D4 Software Implementation**;
- review implementation against governing authority without modifying production code -> **Review & Challenge Pass**;
- deeper risk-triggered falsification -> **Verification**;
- non-mutating post-convergence complexity/architecture-GC -> **Stabilization**;
- changed upstream authority invalidating a downstream plan -> **Downstream Authority Alignment**;
- periodic longitudinal health sensing -> **Health Audit**;
- accepted documentation/lifecycle/generated-artifact reconciliation -> **Closeout**.

For a mixed request such as "review and fix", preserve the mutation boundary: Review determines and records blockers; D4 Implementation performs ordinary code repair, while D1-D3 deficiencies route to their owning design domain.

Before mutation, classify the highest potentially affected semantic domain plus directly applicable governed side constraints. The full scientific path is D1 -> D2 -> D3 -> D4 with reverse verification, but reduced D4-only, D3->D4, or D2->D4 paths are normal when upstream semantics are unaffected.

Every material Review or verification/acceptance boundary includes a bounded Challenge Pass. If accepted authority itself may be materially false, contradictory, ambiguous, inadequate, or impossible to concretize, surface a `SERIOUS CHALLENGE` before ordinary blockers or Pass/No-Pass. The orchestrator may route and preserve that state but may not decide scientific truth or self-approve a human-owned ratification.

---

## 0. Authority / Affected-Domain Intake

```text
INPUTS
TASK = [describe the requested change/problem]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
GOVERNING_AUTHORITY = [known stakeholder/project/domain authority; AUTO = discover current authority]
AFFECTED_DOMAIN = [AUTO = classify highest potentially affected D1/D2/D3/D4 domain]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform this stage; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Inspect the actual target and classify the earliest/highest semantic domain whose accepted meaning may materially change: D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, or D4 specification/implementation. Identify domain-local governed constraints that enter directly below D1 instead of forcing them through a linear hierarchy.

Perform only bounded intake/routing. Do not mutate product/domain authority. Route the next stage to the owning skill: scientific-formulation, numerical-algorithm-design, software-design, or software-implementation. A D4-only/D3-only classification should include a proportionate upstream-impact exclusion when scientific/numerical risk is plausible. Do not invent missing D1/D2 documents for non-scientific local software.
```

---

## 1. D1 Scientific & Mathematical Formulation

```text
INPUTS
TASK = [scientific/mathematical formulation change, question, or review scope]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
CURRENT_AUTHORITY = [current Scientific Method Paper / D1 authority; AUTO = discover]
WORKPLAN_DESTINATION = [generic abstraction-concretization change-plan path for a material D1 mutation/review or authorized direct downstream handoff; AUTO = repository convention]
HUMAN_RATIFICATION = [AUTO = derive whether human decision is required from semantic risk]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform authorized D1 work; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = scientific-formulation. Reconstruct the scientific/theoretical/engineering question independently of current code. Distinguish normative D1 claims from literature/evidence/rationale. Define or review observables/estimands, governing equations/models, assumptions, validity regime, interpretation, D1 uncertainty, and problem-appropriate external adequacy/validation/proof/standards evidence.

Draft proposed authority separately from accepted-current authority. Consequential changes to scientific meaning, model/equations/closures, material assumptions/validity, model uncertainty, or conclusions require designated human ratification when policy assigns it; do not self-approve them.

Before returning `accepted` for a material D1 authority mutation, require evidence that an independent reviewer/context that did not author the proposal attempted falsification and passed it, then obtain any required human ratification. If either prerequisite is missing, keep the authority proposed and return `human_pending` when ratification is pending or truthful No-Pass otherwise.

For a material D1 authority mutation that will use the independent Review stage, actually create or update a snapshot-complete generic abstraction-concretization change plan at WORKPLAN_DESTINATION so Review has a governing artifact. The same plan may govern a direct D1->D3 or D1->D4 handoff that intentionally skips unchanged intermediate domains. Do not create an extra plan when the scope is genuinely trivial/non-material, when a dependent D2/D3 stage will own the next handoff, or when no separate Review/downstream concretization needs one.

Before D1->D2 handoff, test both concretization fidelity and abstraction adequacy. On accepted D1 change, mark only materially dependent descendants/evidence stale. If current D1 authority itself appears materially contradictory, false, ambiguous, or impossible to concretize, raise SERIOUS CHALLENGE before ordinary findings.
```

---

## 2. D2 Algorithm & Numerical Method Design

```text
INPUTS
TASK = [algorithm/numerical-method change, question, or review scope]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
CURRENT_AUTHORITY = [current Numerical & Algorithmic Method Paper / D2 authority; AUTO = discover]
WORKPLAN_DESTINATION = [generic abstraction-concretization change-plan path for a material D2 mutation/review or authorized direct D4 handoff; AUTO = repository convention]
SCIENTIFIC_AUTHORITIES = [applicable D1 authority; AUTO = discover; NONE only when genuinely absent]
HUMAN_RATIFICATION = [AUTO = derive whether human decision is required from semantic risk]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform authorized D2 work; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = numerical-algorithm-design. Recover every applicable D1 invariant and domain-local numerical/resource constraint. Define or review estimator/discretization/solver/normalization/order/precision/stochastic semantics, approximation regime, error/convergence/conditioning guarantees, and numerical uncertainty independently of current software machinery.

Choose the minimum justified admissible method. Design sufficiently independent numerical oracles: exact/limiting/manufactured/reference cases, residual/invariants, refinement/convergence order, conditioning/sensitivity, differential/metamorphic relations, stochastic bias/variance, and backend/precision robustness as applicable. Never widen a tolerance or weaken a method merely to accept an implementation/backend.

Draft proposed authority separately. Human adjudication is required when a D2 change can alter scientific conclusions or a governing algorithm/error guarantee. Before returning `accepted` for a material D2 authority mutation, require evidence that an independent reviewer/context that did not author the proposal attempted falsification and passed it, then obtain any required human ratification. If either prerequisite is missing, keep the authority proposed and return `human_pending` when ratification is pending or truthful No-Pass otherwise. For a material D2 authority mutation that will use the independent Review stage, actually create or update a snapshot-complete generic abstraction-concretization change plan at WORKPLAN_DESTINATION so Review has a governing artifact. Before D2->D3 handoff test fidelity to D1 and D3-abstraction adequacy needs. The same generic plan may govern an authorized direct D2->D4 handoff with unchanged D3 authority so D4 receives a governing implementation contract without manufacturing a D3 change. If accepted D2 authority itself may be materially wrong/contradictory/ambiguous/impossible to concretize, raise SERIOUS CHALLENGE rather than requesting a software workaround.
```

---

## 3. D3 Software Architecture / Workplan

```text
INPUTS
TASK = [software architecture/change problem]
REPOSITORY_TARGET = [repository/worktree/branch to inspect; AUTO = current repository]
EXISTING_AUTHORITIES = [current D1/D2/D3/D4 authorities and governed contracts; AUTO = discover]
WORKPLAN_DESTINATION = [D3 change-plan/workplan path; use the D3->D4 implementation-workplan specialization when D4 is affected; AUTO = repository convention]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = create/update D3 authority/workplan; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = software-design. Treat D3 as software architecture, not as owner of D1 science or D2 numerical method. Reconcile applicable upstream invariants and domain-local security/reliability/performance/resource/compatibility/deployment contracts.

Design the minimum justified admissible architecture. Prefer cohesive ownership, direct flow, one authoritative representation, fewer interfaces/states/dependencies, and removal/consolidation over compensating machinery. Keep durable current Architecture Manual authority distinct from cycle-scoped workplan decisions.

Actually create or update the governing D3->D4 workplan at WORKPLAN_DESTINATION when D4 concretization is materially affected. For a material D3-only authority mutation that will use the independent Review stage, create or update the generic abstraction-concretization change plan there instead so Review has a governing artifact. If accepted D3 authority changes but existing D4 already concretizes it and no implementation work or separate Review is affected, do not manufacture an empty D4 workplan solely to satisfy routing mechanics; the D3-only scope may proceed directly to Closeout. Do not modify product implementation in this stage. Freeze only architecture-level choices needed to bound implementation; leave D4 helpers/APIs/data structures/libraries/local algorithms replaceable. Define real-owner acceptance boundaries, focused/stage-local/final affected regression, integration, repository checks, and genuine simplification/reopen triggers.

Before returning `accepted` for a material durable D3 authority mutation, require evidence that an independent reviewer/context that did not author the proposal attempted falsification and passed it. If the pass is unavailable, keep the authority proposed and return truthful No-Pass. A workplan-only handoff that does not mutate durable D3 authority remains governed by the normal material Challenge Pass and its accepted cycle freeze.

Challenge D3 abstraction adequacy against D2. If evidence instead invalidates D2 or D1, route upstream rather than encoding a workaround. Finish with Pass / No-Pass on handoff readiness, with any SERIOUS CHALLENGE first.
```

---

## 4. D4 Software Implementation

```text
INPUTS
CHANGE_PLAN = [accepted governing change/work plan when one is materially warranted; NONE only for genuinely local D4-only work under sufficient current authority]
REPOSITORY_TARGET = [repository/worktree/branch to modify; AUTO = current repository]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = CHANGE_PLAN protocol_version when supplied, otherwise current compatible Protocol 6.1 profile; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = modify/test the candidate; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = software-implementation under CHANGE_PLAN's declared protocol semantics when a plan is supplied; otherwise use the current compatible Protocol 6.1 profile and the accepted current D1-D4/external authority discoverable from the target. Under AUTO_EXECUTE, actually modify REPOSITORY_TARGET and its owned tests/documentation as required; do not stop at a plan or code snippets when authorized write/execution tools exist.

For genuinely local D4-only work under sufficient current authority, CHANGE_PLAN may be NONE. Perform the proportionate upstream-impact exclusion and do not manufacture a workplan merely to satisfy routing mechanics. For an authorized reduced D2->D4 or D1->D4 route, use the governing upstream abstraction-concretization change plan together with the unchanged current D3 architecture; do not manufacture a D3 authority mutation or empty D3->D4 plan.

Implement the accepted D4 specification and D3 architecture while preserving every applicable D1/D2 invariant and governed side constraint.

Treat D4 machinery as replaceable unless explicitly governed. Prefer owning-layer repair and removal/narrowing/rewiring/consolidation over wrappers/fallbacks/special cases. If code conflicts with accepted D4 specification, do not rewrite the specification merely to make code pass.

Close every material executable stage semantically plus focused/stage-local affected regression. Before completion reconcile the full accepted contract, inspect obsolete/bypassed/duplicate ownership and complexity, re-derive the final affected surface, run complete affected regression, real-owner integration/end-to-end, and repository/project-required checks. Reconcile materially affected evidence applicability, dependency views, and semantic-history obligations before closure. A required check or material impact item not closed is not a pass.

If evidence shows a parent abstraction may itself be materially wrong, surface SERIOUS CHALLENGE and stop dependent closure instead of routing around it.
```

---

## 5. Review & Challenge Pass

```text
INPUTS
WORKPLAN = [governing workplan/change plan]
IMPLEMENTATION_TARGET = [candidate branch/commit/worktree; AUTO = current candidate]
RELATED_AUTHORITIES = [applicable D1/D2/D3/D4 and external authorities; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing workplan protocol_version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform review and owned lifecycle updates; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve the role owning the parent boundary being reviewed; for normal D4 implementation Review use software-design in independent implementation-review mode. Review the assembled candidate, not only the diff or implementer summary. Prefer fresh context for substantial/high-risk work.

First perform the bounded Challenge Pass: ask whether governing authority itself is internally consistent, unambiguous enough to verify, jointly realizable, logically/mathematically coherent, adequate for its problem, complete enough to preserve upstream semantics, and compatible with simultaneous authorities. If a Serious Challenge threshold is met, make it the first-line status and block ordinary unqualified Pass pending human adjudication.

Then reconstruct every still-binding invariant/side constraint/cycle freeze/specification and independently attempt to falsify concretization fidelity, abstraction adequacy, ownership, science/numerics, reliability/security, resources/performance, affected-surface completeness, oracle strength, and total complexity.

Missing required regression/integration/repository checks and unresolved material evidence/dependency impact items remain blockers. Stale or otherwise inadmissible evidence cannot satisfy a current acceptance claim. Review must not modify production implementation, but AUTO_EXECUTE may update, reopen, or close the governing workplan/review lifecycle record when the verdict requires it. Route ordinary nonconformance to D4, D3 deficiencies to software-design, D2 deficiencies to numerical-algorithm-design, and D1 deficiencies to scientific-formulation.
```

---

## 6. Verification

```text
INPUTS
VERIFICATION_SCOPE = [claim/subsystem/workplan/release requiring deeper falsification]
IMPLEMENTATION_TARGET = [candidate branch/commit/worktree; AUTO = current candidate]
GOVERNING_AUTHORITY = [applicable accepted D1-D4/external authority; AUTO = discover]
SCIENTIFIC_AUTHORITIES = [D1/D2 authorities; AUTO = discover; NONE if genuinely irrelevant]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = execute non-mutating verification; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Perform deeper, non-mutating, risk-triggered adversarial-verification. Resolve the owning domain skill(s) for the claims rather than defaulting every scientific/numerical question to software-design.

Reconcile multiple authorities, construct counterexamples, exercise independently justified reference/differential/metamorphic/numerical evidence, inspect real semantic-owner paths, and trace composed executable->D2->D1 closure where material. Distinguish internal verification from D1 external adequacy/validation/proof/standards evidence.

Run the bounded Challenge Pass. An authority contradiction produces SERIOUS CHALLENGE / human adjudication rather than an implementation patch. Verification does not replace ordinary Review and does not modify production implementation.
```

---

## 7. Stabilization / Architecture GC

```text
INPUTS
STABILIZATION_SCOPE = [converged subsystem/workplan/release boundary]
IMPLEMENTATION_TARGET = [candidate branch/commit/worktree; AUTO = current candidate]
GOVERNING_AUTHORITY = [accepted D1-D4 authority to preserve; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform non-mutating stabilization; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

After ordinary Review otherwise passes at a material convergence boundary, inspect whether the accepted concretization is still the minimum justified system. Look for duplicated authority/state, wrappers/adapters/fallbacks/special cases, stale compatibility, unnecessary states/config/public surface, ownership leakage/cycles, historical-exception branches, dead/bypassed paths, and tests dominated by internal orchestration.

Stabilization remains non-mutating. If simplification is warranted, route the smallest coherent change to D4 under existing D3 authority, D3 if architecture changes, or D2/D1 if evidence reveals an upstream semantic defect. Do not manufacture refactoring merely because this stage exists.
```

---

## 8. Downstream Authority Alignment

```text
INPUTS
UPSTREAM_ACCEPTED_WORK = [accepted upstream authority/change that altered assumptions]
DOWNSTREAM_WORKPLAN = [downstream plan/authority to reconcile]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
GOVERNING_AUTHORITY = [accepted parent invariants and cycle-scoped decisions; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = downstream workplan governing version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = update owned downstream plan/authority; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve the semantic owner of DOWNSTREAM_WORKPLAN. Under AUTO_EXECUTE, actually update DOWNSTREAM_WORKPLAN when reconciliation is warranted; alignment must not modify production implementation.

Reconcile only materially dependent assumptions/invariants/evidence after UPSTREAM_ACCEPTED_WORK. Preserve unaffected siblings and still-valid evidence. A missing edge in a partial dependency view is not proof of non-impact. Do not invalidate every downstream artifact merely because they share a repository.

If the upstream change makes the downstream abstraction impossible or contradictory, raise SERIOUS CHALLENGE instead of inventing a compatibility shim. Otherwise update the downstream plan/authority so it is snapshot-complete under its own governing protocol version.
```

---

## 9. Health Audit

```text
INPUTS
AUDIT_SCOPE = [repository/subsystem/history window to assess]
REPOSITORY_TARGET = [repository/worktree; AUTO = current repository]
HISTORY_WINDOW = [AUTO = useful available history; or explicit range]
GOVERNING_ARCHITECTURE = [current D3 authority; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = current compatible protocol; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform non-mutating audit; REPORT_ONLY = inspect/report only]
EXCLUSIONS = [explicit exclusions; NONE if absent]

Resolve REQUIRED_SKILL = software-maintenance-audit when available. Perform a periodic long-horizon repository audit, not a feature review or approval gate. Combine semantic inspection with real history when available: churn/change coupling, recurring defect families, complexity, dependency centrality/cycles, public/config growth, weak oracles, documentation difficulty, and architecture drift.

Metrics are sensors, not truth. Do not fabricate longitudinal trends from a static snapshot. Health Audit does not implement the repairs. Route local D4 repair/simplification under already-sufficient existing authority to software-implementation; substantial maintenance needing new/revised architecture/workplan to software-design first; D1/D2 concerns to their owner; documentation-only drift to software-documentation; lifecycle residue to repository-hygiene. Audit itself does not mutate authority or product code.
```

---

## 10. Closeout

```text
INPUTS
COMPLETED_WORK = [completed workplan/change-plan/release scope; exact selected workplan may supply this]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
AFFECTED_DOCUMENTATION = [current docs/generated artifacts/lifecycle records; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing completed-work version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = reconcile documentation/lifecycle artifacts; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Closeout begins only after semantic/functional acceptance. Under AUTO_EXECUTE, actually perform the documentation, lifecycle, generated-artifact, release/version, and conservative hygiene reconciliation owned by this stage; do not merely list cleanup steps. Closeout must not change product behavior.

Reconcile accepted-current D1-D4 authority, guides/runbooks, generated artifacts, release/version information, current dependency/evidence views, semantic-evolution history where triggered, and completed/superseded workplan state. Preserve release-pinned/publication truth and archive transition artifacts only after their semantics exist in current canonical owners.

Use software-documentation for substantive editorial/publication reconciliation and repository-hygiene for conservative proven residue. Closeout must not turn unresolved acceptance into completion. An unresolved Serious Challenge to governing Protocol 6.1 authority blocks Protocol 6.1 release.
```
