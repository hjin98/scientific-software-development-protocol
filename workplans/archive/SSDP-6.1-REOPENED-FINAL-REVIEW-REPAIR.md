---
kind: implementation-workplan
workplan_id: SSDP-6.1-REOPENED-FINAL-REVIEW-REPAIR
protocol_version: 6.1.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-09
active_serious_challenge: none
---

# SSDP 6.1 Reopened Final-Review Repair

## Background and terminology

This repair follows a post-closeout independent review of the Protocol 6.1 candidate. It does not change Protocol 6.1 doctrine. It repairs current-source/documentation nonconformance and strengthens acceptance evidence so the same omissions cannot remain green.

Protocol 6.1 reserves **concretization** for downstream D1-D4 semantic expression. An **evidence realization** is one concrete execution/instantiation of an evidence specification. The retained path `shared/references/abstraction-and-realization.md` is an opaque compatibility filename; current prose inside that file uses abstraction/concretization semantics.

## 1. Target outcome, governing authority, and non-goals

- Stakeholder/product outcome: restore exact Protocol 6.1 current-source coherence and make the final acceptance oracle reject the discovered terminology and navigation defects.
- Governing authority: the archived composed Protocol 6.1 workplan and Revision 1 remain the semantic parent; this repair adds no new D1-D3 doctrine.
- Applicable invariant: current 6.1 prose must not use `concretization` as the name of an evidence execution; canonical navigation must resolve the retained compatibility path.
- Non-goals: no Protocol 7 machinery, no alias/wrapper file, no 6.0 compatibility mutation, no D1/D2/D3 authority change, no broad editorial rewrite.

## 2. Cycle-scoped decisions and delegated D4 concretization

### Cycle-scoped decisions

1. Correct the D3/D4 role wording from evidence `concretizations` to evidence `realizations` where the text refers to evidence execution/instances.
2. Correct `source/README.md` to route to `shared/references/abstraction-and-realization.md` rather than inventing an alias.
3. Add executable regression checks and behavioral qualification cases covering both failure classes.
4. Reopen Protocol 6.1 lifecycle state and the Protocol 7 prerequisite until the repaired candidate is independently requalified and reviewed.

### Delegated D4 concretization

Test implementation details and exact wording remain replaceable provided the two discovered failure classes are directly rejected and existing Protocol 6.1 semantics remain unchanged.

### Active simplification

Repair the wrong text directly. Do not create another compatibility file, checker framework, terminology registry, or wrapper around the defect.

## 3. Implementation obligations

### A. Evidence terminology coherence

Required end state:
- `source/roles/software-design/SKILL.md` uses `evidence specifications/realizations` where evidence instances are meant.
- `source/roles/software-implementation/SKILL.md` uses `Evidence specification, realization, and applicability`, `evidence specifications/realizations`, and the same terminology in completion/impact-closure text.
- generated packaged role entrypoints must match canonical source.

Acceptance boundary: a regression must fail if either current role reintroduces `evidence specifications/concretizations` or the D4 section heading reintroduces `evidence specification, concretization`.

### B. Canonical README navigation

Required end state:
- `source/README.md` points to the retained `shared/references/abstraction-and-realization.md` path everywhere.
- no new `abstraction-and-concretization.md` alias is introduced.

Acceptance boundary: current README-advertised `shared/references/*.md` paths must exist.

### C. Evidence-strength repair

Required end state:
- unit/regression coverage directly exercises both discovered failures;
- behavioral qualification adds the reverse terminology-collision case and dangling canonical-navigation case;
- prior 92-scenario PASS remains historical evidence only and cannot close the repaired candidate.

## 4. Evidence specifications, realizations, and dependencies

Evidence specifications:
1. `tests/test_protocol_61_evidence_evolution.py` current-role terminology negative/positive checks.
2. `tests/test_protocol_61_evidence_evolution.py` canonical README path-existence check.
3. Protocol 6.1 behavioral scenarios 93-94.
4. canonical build/package validation, committed-dist parity, whitespace, Protocol snapshot parity, and Orchestrator Core suite where applicable.

Prior evidence applicability:
- evidence unrelated to these changed dimensions remains reusable;
- prior final 92-scenario assessment and prior package parity are stale for this repaired candidate and must be rerun/remapped;
- frozen Protocol 5.16 and 6.0 profile evidence remains unaffected.

## 5. Affected surface and acceptance

Affected current surface:
- D3/D4 role entrypoints;
- generated D3/D4 skill packages and ZIP transport artifacts;
- `source/README.md`;
- Protocol 6.1 regression and behavioral qualification definitions;
- current lifecycle/index/recovery claims.

Final acceptance requires:
- full repository regression;
- fresh canonical skill build and package validation;
- committed `dist/` parity including ZIP contents;
- whitespace check;
- Protocol snapshot parity and Orchestrator Core suite if the canonical prompt/profile surface is touched or repository policy requires them;
- fresh execution/assessment of all 94 Protocol 6.1 behavioral scenarios;
- independent Review after the final semantic candidate is fixed;
- a new immutable Protocol 6.1 recovery identity only after that Review passes.

## 6. Specification, documentation, dependency, and history impact

- D4 Specification change: none; this is conformance repair.
- D3 Architecture change: none.
- D1/D2 authority change: none.
- Current documentation: `source/README.md` and lifecycle/recovery statements must be reconciled.
- Generated artifacts: affected D3/D4 packages and ZIPs must be regenerated from canonical source.
- Semantic dependency view: no dependency-edge change required.
- Semantic history: preserve the original closeout as historical evidence; record the reopened disposition in current lifecycle state and final history once requalification completes.

## 7. Stages, dependency order, and evidence reuse

1. Repair canonical source and tests/qualification definitions.
2. Regenerate affected generated artifacts from canonical source.
3. Run focused checks, then full repository/package/orchestrator acceptance.
4. Execute/reassess behavioral qualification as 94 scenarios.
5. Run a fresh independent Review.
6. Only after PASS, archive this repair workplan and establish the replacement immutable recovery identity.

## 8. Reopen, Serious Challenge, and simplification triggers

- D4-local blockers: any residual current-role evidence/concretization collision, dangling canonical path, generated-source drift, or failed required acceptance check.
- D3 reopen: only if repair unexpectedly requires a durable architecture change; none is currently indicated.
- D2/D1 reopen: only if evidence shows the terminology separation itself is semantically defective; no such evidence exists.
- Serious Challenge: none active.

## 9. Impact closure

Protocol 6.1 remains reopened until every material affected item is either freshly closed or explicitly blocking. The previous semantic candidate `25d30858e7a33a72cb04b4d07393cb143b7777f8` and recovery snapshot `dec5ff2767e14fd1cda46e073757aa27f40e270c` remain immutable historical evidence but are not the final accepted recovery identity for the repaired 6.1.0 candidate.
