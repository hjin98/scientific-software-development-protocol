---
kind: implementation-workplan
workplan_id: REPLACE_ME
protocol_version: REPLACE_WITH_SKILL_PROTOCOL_VERSION
status: proposed
---

# <Task> D3 -> D4 Implementation Workplan

This is the D3->D4 specialization of the generic abstraction–realization change plan. Use it for material executable software work. It must not absorb D1/D2 authority merely because implementation is scientific or numerical.

## 1. Target outcome, governing authority, and non-goals

- Stakeholder/product outcome:
- Accepted D3 architecture being realized:
- Applicable D1/D2 invariants that reach this implementation surface:
- Domain-local governed D4 constraints/contracts:
- Explicit non-goals:

If the task is claimed D4-only, state the proportionate upstream-impact exclusion when scientific/numerical semantics could plausibly be affected.

## 2. Cycle-scoped D3 decisions and delegated D4 realization

### Frozen for this realization cycle

List only material D3 architecture/ownership/interface/data-flow/resource/security/compatibility decisions deliberately fixed for this implementation cycle plus any exact acceptance identity required by governing authority.

A cycle freeze is not automatically durable current Architecture Manual authority.

### Delegated D4 realization

List implementation-local mechanisms that remain replaceable: helpers, internal APIs, data structures, wrappers, retries, caches, state machines, library choices, local algorithms, synchronization primitives, and current Tier-2 owner paths unless exact identity is governed.

### Active simplification

State existing machinery/state/path that should be removed, narrowed, altered, consolidated, or replaced. New durable machinery must protect a governing capability the simpler system cannot provide or replace broader complexity.

## 3. Implementation obligations

For each material obligation capture only what is needed:

- concern/rationale;
- required end state / governing constraint;
- delegated realization freedom;
- task-specific acceptance evidence;
- real semantic-owner/test-double boundary when proxy acceptance is a material risk;
- oracle-strength relation or structural absence/uniqueness check when ordinary tests are weak;
- anti-shortcut/integrity constraint when a known counterfeit-pass path exists.

Green tests do not prove an omitted obligation was implemented.

## 4. Affected surface and acceptance

Initial expected affected behavior may include callers/consumers, shared utilities, public interfaces, configuration, persistence/restart, orchestration/concurrency, packaging/entrypoints, compatibility, documentation/specification, and transitive scientific/numerical behavior. This list is provisional and must be re-derived from the final assembled candidate.

Executable acceptance inherits Protocol 6 requirements:

- focused checks;
- stage-local affected regression for each material behavior-changing stage;
- final accepted-contract reconciliation;
- final affected-surface re-derivation and complete regression;
- integration/end-to-end through real semantic-owner/consumer boundaries;
- repository/project-required checks;
- explicit blocking treatment of any required check that did not execute.

Production qualification: <required / deferred / unnecessary with reason if material>.

## 5. Specification and documentation impact

- D4 Specification changes required? If yes, distinguish accepted contract mutation from implementation repair.
- D3 Architecture Manual update required?
- D2/D1 authority affected? If yes, this plan is insufficient by itself; route to the earliest affected domain.
- Guides/runbooks/generated artifacts affected?

Do not rewrite specification/architecture/method papers merely to match unintended code.

## 6. Stages, dependency order, and evidence reuse

Use coherent behavior/risk stages only where ordering reduces ambiguity or rework. Several tightly coupled file/helper/test edits may form one stage. Reuse still-valid evidence until a changed dimension can plausibly invalidate it.

## 7. Reopen, Serious Challenge, and simplification triggers

- D4-local implementation blockers that stay within this plan:
- evidence requiring D3 architecture reopen:
- evidence requiring D2 or D1 challenge/reopen:
- structural complexity requiring simplification before another additive repair:
- material authority contradiction that would require `SERIOUS CHALLENGE` rather than ordinary implementation repair:

An unresolved Serious Challenge to governing authority blocks normal Pass for the dependent claim.