---
kind: protocol-stage-f-execution-architecture-amendment
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date: 2026-09-28
status: proposed-pending-independent-review
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
---

# Stage F portable agent/runtime execution architecture amendment

## Decision

Stage F implementation and qualification SHALL be **agent-, vendor-, and environment-agnostic**. A named CLI, model provider, local filesystem path, local Git checkout, operating system, or machine is not part of Protocol 7 qualification semantics.

The qualification architecture is split into:

1. a **portable qualification core** owning frozen subjects/cases/floors, matched-pair scheduling, custody roles, evidence/admissibility semantics and scoring inputs; and
2. **runtime adapters** that translate those semantic capabilities to a local CLI agent, cloud agent, hosted workspace, container/VM, API-backed agent or another environment.

An adapter is replaceable D4 machinery. It may not weaken the qualification contract to fit its host.

## Admission boundary

Any execution profile is admissible only if its exact adapter/profile passes the pre-run integrity checks for:

- immutable repository+commit and package identity;
- exactly-one-arm catalog isolation;
- matched agent/model/reasoning/capability/resource configuration within a pair;
- complete raw/equivalent and normalized trace evidence;
- complete report, changed/new-file or before/after-tree, side-effect, issue/evidence-store, oracle and metadata capture;
- fail-closed missing/error/malformed states;
- containment of external writes/network actions with attempts observable;
- custody separation;
- sequential arm order within a pair and independent concurrent-pair state;
- cache identity over subject, fixture/oracle, execution profile, adapter, replicate and pair order.

If the host cannot enforce or expose a required boundary, that profile is unavailable for the affected claim. This is **STOP/BLOCKED**, not permission to substitute a proxy.

## Fair comparison

Protocol arms are compared only within the same execution profile. Fresh 6.5/6.6 baselines used by an execution profile are run in that same profile. Results from materially different profiles are reported separately unless a predeclared analysis justifies aggregation.

The historical Protocol 6.6 Claude Code/`claude-sonnet-5` runs remain bounded historical evidence. They do not require Protocol 7 Stage F to use Claude.

## D4 consequence

The current `qualification/ssdp70/eval/` scripts are evidence tooling, not architecture authority. The next implementation cycle may refactor or replace them with a portable core plus adapters. It must repair the blockers in `STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md`, run focused adapter/core regression, and then perform the required withheld-instance and actual-adapter known-good/known-broken pre-run qualification.

## Non-change

This amendment changes no Protocol 7 semantic candidate bytes, scientific doctrine, fixture content, scoring threshold, comparative target, human-trial floor, custody independence requirement or Stage G/H release semantics.

## Review state

This context authored the amendment and cannot independently accept it. Prior workplan and contract PASS records bind earlier exact bytes. A fresh independent Review must check this amendment against the governing workplan, frozen qualification intent and the Stage F STOP/BLOCKED findings before dependent tooling repair or candidate runs.
