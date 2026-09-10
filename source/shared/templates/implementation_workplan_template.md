---
kind: implementation-workplan
workplan_id: REPLACE_ME
protocol_version: REPLACE_WITH_SKILL_PROTOCOL_VERSION
status: proposed
---

# <Task> D3 -> D4 Implementation Workplan

This is the D3->D4 specialization of the generic abstraction–concretization change plan. Use it for material executable software work. It must not absorb D1/D2 authority merely because implementation is scientific or numerical.

## Background and terminology

For a substantial human-facing plan that introduces non-common project/domain terminology, define it briefly here before later sections rely on it. State intended reader/assumed prerequisites when material. Expand non-obvious abbreviations at first explanatory use with `full term (ABC)`.

Background explanation is not a substitute for precise D1/D2/D3/D4 normative definitions.

## 1. Target outcome, governing authority, and non-goals

- Stakeholder/product outcome:
- Accepted D3 architecture being concretized:
- Applicable D1/D2 invariants that reach this implementation surface:
- Domain-local governed D4 constraints/contracts:
- Explicit non-goals:

If the task is claimed D4-only, state the proportionate upstream-impact exclusion when scientific/numerical semantics could plausibly be affected.

## 2. Cycle-scoped D3 decisions and delegated D4 concretization

### Cycle-scoped decisions

List only material D3 architecture/ownership/interface/data-flow/resource/security/compatibility decisions deliberately fixed for this implementation cycle plus any exact acceptance identity required by governing authority.

A cycle-scoped decision is not automatically durable current Architecture Manual authority.

### Delegated D4 concretization

List implementation-local mechanisms that remain replaceable: helpers, internal APIs, data structures, wrappers, retries, caches, state machines, library choices, local algorithms, synchronization primitives, and current delegated owner paths unless exact identity is governed.

### Active simplification

State existing machinery/state/path that should be removed, narrowed, altered, consolidated, or replaced. New durable machinery must protect a governing capability the simpler system cannot provide or replace broader complexity.

## 3. Implementation obligations

For each material obligation capture only what is needed. Attach only when material:

- concern/rationale;
- required end state / governing constraint;
- delegated concretization freedom;
- task-specific acceptance evidence;
- **acceptance boundary** — governing claim, current real semantic owner/path or owner class, allowed doubles, forbidden substitutions, and observable evidence when proxy acceptance is a material risk; state whether the owner is governed identity or merely the current delegated concretization so an equivalent delegated replacement remaps acceptance rather than freezing the old owner;
- oracle-strength relation or structural absence/uniqueness check when ordinary tests are weak;
- anti-shortcut/integrity constraint — a known way local compliance/evidence manipulation could appear to pass while defeating the governed outcome.

Green tests do not prove an omitted obligation was implemented.

## 4. Evidence specifications, realizations, and dependencies

For material acceptance claims distinguish:

- evidence specification / governed proposition;
- real semantic owner the specification interrogates;
- execution dependencies such as harness, fixtures, datasets, backend, environment, or replaceable D4 machinery;
- evidence-realization identity dimensions that can change applicability;
- prior evidence expected to remain admissible, become review-required, or become stale;
- independent evidence routes warranted to reduce common-mode risk.

A rerun against a changed candidate is a new evidence realization. A stale passing observation cannot confirm the current candidate and a stale failing observation cannot refute it.

## 5. Affected surface and acceptance

Initial expected affected behavior may include callers/consumers, shared utilities, public interfaces, configuration, persistence/restart, orchestration/concurrency, packaging/entrypoints, compatibility, documentation/specification, dependency/history records, evidence specifications/realizations, and transitive scientific/numerical behavior. This list is provisional and must be re-derived from the final assembled candidate.

Executable acceptance inherits Protocol 6.1 requirements:

- focused checks;
- stage-local affected regression for each material behavior-changing stage;
- final accepted-contract reconciliation;
- final affected-surface re-derivation and complete regression;
- integration/end-to-end through real semantic-owner/consumer boundaries;
- repository/project-required checks;
- bounded impact closure over materially dependent authority/evidence/documentation;
- explicit blocking treatment of any required check or impact item that did not close.

Production qualification: <required / deferred / unnecessary with reason if material>.

## 6. Specification, documentation, dependency, and history impact

- D4 Specification changes required? If yes, distinguish accepted contract mutation from implementation repair.
- D3 Architecture Manual update required?
- D2/D1 authority affected? If yes, this plan is insufficient by itself; route to the earliest affected domain.
- Guides/runbooks/generated artifacts affected?
- Current semantic dependency view affected?
- Evidence specifications/realizations needing remap/rerun/retirement?
- Semantic-evolution history triggered by material supersession/rejection/generalization/restoration?

Do not rewrite specification/architecture/method papers or evidence oracles merely to match unintended code.

## 7. Stages, dependency order, and evidence reuse

Use coherent behavior/risk stages only where ordering reduces ambiguity or rework. Several tightly coupled file/helper/test edits may form one stage. Reuse still-valid evidence until a changed authority/concretization/evidence-specification/environment dimension can plausibly invalidate it.

If a bounded dependency map is used to justify non-impact, state whether that scope is complete for the exclusion. Missing edges in a partial map are not proof of independence.

## 8. Reopen, Serious Challenge, and simplification triggers

- D4-local implementation blockers that stay within this plan:
- evidence requiring D3 architecture reopen:
- evidence requiring D2 or D1 challenge/reopen:
- structural complexity requiring simplification before another additive repair:
- material authority contradiction that would require `SERIOUS CHALLENGE` rather than ordinary implementation repair:

An unresolved Serious Challenge to governing authority blocks normal Pass for the dependent claim.

## 9. Impact closure

Before final closure account for every materially affected descendant, evidence specification/realization, documentation/current dependency record, human re-ratification obligation, retirement/cleanup action, and semantic-history update. Resolve it, preserve it as still-valid with reason, or mark it unavailable/blocking. Old green tests do not substitute for this closure.
