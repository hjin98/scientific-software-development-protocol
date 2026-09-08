# Scientific Software Development Workflow Prompts

This is the canonical human-facing orchestration source for Protocol 6. It routes work through the authority-bearing domain that actually owns the semantics rather than forcing every task through a four-stage waterfall.

Use `AUTO_LOCAL_FIRST` to resolve a governing-version-compatible installed skill first and the canonical public repository second. A workplan's declared `protocol_version` controls its inherited protocol semantics; never silently use current Protocol 6 doctrine for a Protocol 5.16 workplan.

`AUTO_EXECUTE` means perform the selected stage with available authorized tools. `REPORT_ONLY` prohibits repository mutation but still requires real inspection and the strongest available evidence. A stage may mutate only its owned authority/realization surface; when evidence points to another domain, route explicitly rather than silently crossing the boundary.

Before mutation, classify the highest potentially affected semantic domain plus directly applicable governed side constraints. The full scientific path is D1 -> D2 -> D3 -> D4 with reverse verification, but reduced D4-only, D3->D4, or D2->D4 paths are normal when upstream semantics are unaffected.

Every material Review or verification/acceptance boundary includes a bounded Challenge Pass. If accepted authority itself may be materially false, contradictory, ambiguous, inadequate, or unrealizable, surface a `SERIOUS CHALLENGE` before ordinary blockers or Pass/No-Pass. The orchestrator may route and preserve that state but may not decide scientific truth or self-approve a human-owned ratification.

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
HUMAN_RATIFICATION = [AUTO = derive whether human decision is required from semantic risk]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform authorized D1 work; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = scientific-formulation. Reconstruct the scientific/theoretical/engineering question independently of current code. Distinguish normative D1 claims from literature/evidence/rationale. Define or review observables/estimands, governing equations/models, assumptions, validity regime, interpretation, D1 uncertainty, and problem-appropriate external adequacy/validation/proof/standards evidence.

Draft proposed authority separately from accepted-current authority. Consequential changes to scientific meaning, model/equations/closures, material assumptions/validity, model uncertainty, or conclusions require designated human ratification when policy assigns it; do not self-approve them.

Before D1->D2 handoff, test both realization fidelity and abstraction adequacy. On accepted D1 change, mark only materially dependent descendants/evidence stale. If current D1 authority itself appears materially contradictory, false, ambiguous, or unrealizable, raise SERIOUS CHALLENGE before ordinary findings.
```

---

## 2. D2 Algorithm & Numerical Method Design

```text
INPUTS
TASK = [algorithm/numerical-method change, question, or review scope]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
CURRENT_AUTHORITY = [current Numerical & Algorithmic Method Paper / D2 authority; AUTO = discover]
SCIENTIFIC_AUTHORITIES = [applicable D1 authority; AUTO = discover; NONE only when genuinely absent]
HUMAN_RATIFICATION = [AUTO = derive whether human decision is required from semantic risk]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = perform authorized D2 work; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = numerical-algorithm-design. Recover every applicable D1 invariant and domain-local numerical/resource constraint. Define or review estimator/discretization/solver/normalization/order/precision/stochastic semantics, approximation regime, error/convergence/conditioning guarantees, and numerical uncertainty independently of current software machinery.

Choose the minimum justified admissible method. Design sufficiently independent numerical oracles: exact/limiting/manufactured/reference cases, residual/invariants, refinement/convergence order, conditioning/sensitivity, differential/metamorphic relations, stochastic bias/variance, and backend/precision robustness as applicable. Never widen a tolerance or weaken a method merely to accept an implementation/backend.

Draft proposed authority separately. Human adjudication is required when a D2 change can alter scientific conclusions or a governing algorithm/error guarantee. Before D2->D3 handoff test fidelity to D1 and D3-abstraction adequacy needs. If accepted D2 authority itself may be materially wrong/contradictory/ambiguous/unrealizable, raise SERIOUS CHALLENGE rather than requesting a software workaround.
```

---

## 3. D3 Software Architecture / Workplan

```text
INPUTS
TASK = [software architecture/change problem]
REPOSITORY_TARGET = [repository/worktree/branch to inspect; AUTO = current repository]
EXISTING_AUTHORITIES = [current D1/D2/D3/D4 authorities and governed contracts; AUTO = discover]
WORKPLAN_DESTINATION = [D3->D4 implementation workplan path; AUTO = repository convention]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = governing declared protocol/version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = create/update D3 authority/workplan; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = software-design. Treat D3 as software architecture, not as owner of D1 science or D2 numerical method. Reconcile applicable upstream invariants and domain-local security/reliability/performance/resource/compatibility/deployment contracts.

Design the minimum justified admissible architecture. Prefer cohesive ownership, direct flow, one authoritative representation, fewer interfaces/states/dependencies, and removal/consolidation over compensating machinery. Keep durable current Architecture Manual authority distinct from cycle-scoped workplan decisions.

Create/update the D3->D4 workplan at WORKPLAN_DESTINATION when material. Freeze only architecture-level choices needed to bound implementation; leave D4 helpers/APIs/data structures/libraries/local algorithms replaceable. Define real-owner acceptance boundaries, focused/stage-local/final affected regression, integration, repository checks, and genuine simplification/reopen triggers.

Challenge D3 abstraction adequacy against D2. If evidence instead invalidates D2 or D1, route upstream rather than encoding a workaround. Finish with Pass / No-Pass on handoff readiness, with any SERIOUS CHALLENGE first.
```

---

## 4. D4 Software Implementation

```text
INPUTS
WORKPLAN = [governing D3->D4 implementation workplan]
REPOSITORY_TARGET = [repository/worktree/branch to modify; AUTO = current repository]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = WORKPLAN protocol_version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = modify/test the candidate; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve REQUIRED_SKILL = software-implementation under WORKPLAN's declared protocol semantics. Implement the accepted D4 specification and D3 architecture while preserving every applicable D1/D2 invariant and governed side constraint.

Treat D4 machinery as replaceable unless explicitly governed. Prefer owning-layer repair and removal/narrowing/rewiring/consolidation over wrappers/fallbacks/special cases. If code conflicts with accepted D4 specification, do not rewrite the specification merely to make code pass.

Close every material executable stage semantically plus focused/stage-local affected regression. Before completion reconcile the full accepted contract, inspect obsolete/bypassed/duplicate ownership and complexity, re-derive the final affected surface, run complete affected regression, real-owner integration/end-to-end, and repository/project-required checks. A required check not executed is not a pass.

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

Resolve the role owning the parent boundary being reviewed; for normal D4 implementation Review use software-design. Review the assembled candidate, not only the diff or implementer summary. Prefer fresh context for substantial/high-risk work.

First perform the bounded Challenge Pass: ask whether governing authority itself is internally consistent, unambiguous enough to verify, jointly realizable, logically/mathematically coherent, adequate for its problem, complete enough to preserve upstream semantics, and compatible with simultaneous authorities. If a Serious Challenge threshold is met, make it the first-line status and block ordinary unqualified Pass pending human adjudication.

Then reconstruct every still-binding invariant/side constraint/cycle freeze/specification and independently attempt to falsify realization fidelity, abstraction adequacy, ownership, science/numerics, reliability/security, resources/performance, affected-surface completeness, oracle strength, and total complexity.

Missing required regression/integration/repository checks remain blockers. Route ordinary nonconformance to D4, D3 deficiencies to software-design, D2 deficiencies to numerical-algorithm-design, and D1 deficiencies to scientific-formulation. Update/reopen only owned planning/lifecycle artifacts; do not modify production implementation during Review.
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

Perform deeper, non-mutating, risk-triggered falsification. Resolve the owning domain skill(s) for the claims rather than defaulting every scientific/numerical question to software-design.

Reconcile multiple authorities, construct counterexamples, exercise independently justified reference/differential/metamorphic/numerical evidence, inspect real semantic-owner paths, and trace composed executable->D2->D1 closure where material. Distinguish internal verification from D1 external adequacy/validation/proof/standards evidence.

Run the bounded Challenge Pass. An authority contradiction produces SERIOUS CHALLENGE / human adjudication rather than an implementation patch. Verification does not replace ordinary Review and does not mutate product code.
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

After ordinary Review otherwise passes at a material convergence boundary, inspect whether the accepted realization is still the minimum justified system. Look for duplicated authority/state, wrappers/adapters/fallbacks/special cases, stale compatibility, unnecessary states/config/public surface, ownership leakage/cycles, historical-exception branches, dead/bypassed paths, and tests dominated by internal orchestration.

This stage is non-mutating. If simplification is warranted, route the smallest coherent change to D4 under existing D3 authority, D3 if architecture changes, or D2/D1 if evidence reveals an upstream semantic defect. Do not manufacture refactoring merely because this stage exists.
```

---

## 8. Downstream Authority Alignment

```text
INPUTS
UPSTREAM_ACCEPTED_WORK = [accepted upstream authority/change that altered assumptions]
DOWNSTREAM_WORKPLAN = [downstream plan/authority to reconcile]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current repository]
FROZEN_PARENT_AUTHORITY = [accepted parent invariants/cycle decisions; AUTO = discover]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST = compatible installed skill/root first, then canonical public repository; otherwise explicit source]
PROTOCOL_REF = [AUTO = downstream workplan governing version; otherwise explicit immutable compatible ref]
EXECUTION_MODE = [AUTO_EXECUTE = update owned downstream plan/authority; REPORT_ONLY = inspect/report only]
ADDITIONAL_CONSTRAINTS = [optional explicit user constraints; NONE if absent]

Resolve the semantic owner of DOWNSTREAM_WORKPLAN. Reconcile only materially dependent assumptions/invariants/evidence after UPSTREAM_ACCEPTED_WORK. Preserve unaffected siblings and still-valid evidence. Do not invalidate every downstream artifact merely because they share a repository.

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

Resolve REQUIRED_SKILL = software-maintenance-audit when available. Combine semantic inspection with real history when available: churn/change coupling, recurring defect families, complexity, dependency centrality/cycles, public/config growth, weak oracles, documentation difficulty, and architecture drift.

Metrics are sensors, not truth. Do not fabricate longitudinal trends from a static snapshot. Route findings to the earliest owning D1/D2/D3/D4 domain, software-documentation for documentation-only drift, or repository-hygiene for lifecycle residue. Audit itself does not mutate authority or product code.
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

Closeout begins only after semantic/functional acceptance. Reconcile accepted-current D1-D4 authority, guides/runbooks, generated artifacts, release/version information, and completed/superseded workplan state. Preserve release-pinned/publication truth and archive transition artifacts only after their semantics exist in current canonical owners.

Use software-documentation for substantive editorial/publication reconciliation and repository-hygiene for conservative proven residue. Closeout must not change product semantics or turn unresolved acceptance into completion. An unresolved Serious Challenge to governing Protocol 6 authority blocks Protocol 6 release.
```