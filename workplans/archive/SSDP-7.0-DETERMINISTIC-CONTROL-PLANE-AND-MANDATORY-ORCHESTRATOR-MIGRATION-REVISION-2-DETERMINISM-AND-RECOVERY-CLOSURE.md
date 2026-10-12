---
kind: protocol-major-revision-workplan-amendment
workplan_id: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE
amends_workplan: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
extends_amendment: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE
protocol_version: 6.1.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-09
review_round: 2-final-determinism-pass
requires_completed_workplan: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
active_serious_challenge: none
---

# SSDP 7.0 — Revision 2 Determinism and Recovery Closure

## 1. Purpose

This amendment closes the remaining deterministic-control gap after Revision 1. Parent + Revision 1 + this Revision 2 form the complete current Protocol 7 design handoff.

The issue is fundamental: an event-sourced controller is not replay-deterministic if historical reduction consults changing ambient state.

## 2. Reducer purity and explicit observation boundary

Canonical state reduction SHALL be deterministic from version-bound accepted inputs.

The reducer MUST NOT determine historical transition results by querying ambient mutable state such as:

- current wall-clock time;
- live filesystem contents;
- current Git branch/remote state;
- present network availability;
- current quota/account/resource meters;
- current process state;
- random-number generation;
- an LLM or other nondeterministic semantic evaluator;
- mutable external service state.

When such information can affect control, acquire it outside the reducer and represent the relevant fact as a typed, provenance-bearing accepted observation/event before reduction.

Examples:

```text
clock/lease condition
 -> recorded timer/expiry observation
 -> reducer applies transition rule

remote Git condition
 -> recorded fetch/ref/candidate observation
 -> reducer applies reconciliation rule

resource/quota condition
 -> Scheduler/meter observation or admission result
 -> reducer records execution readiness/blocking consequence

agent/human semantic judgment
 -> typed assessment/decision with provenance
 -> reducer validates and propagates legal consequence
```

Event timestamps may be retained for provenance and deterministic rule inputs, but replay SHALL use the recorded event data/ruleset rather than asking "what time is it now?" to reinterpret old history.

If ordering depends on time, define deterministic ordering/tie semantics in the control contract.

## 3. External effects are not reducer mutations

Launching an agent, creating/pushing a branch, sending a control response, invoking a tool, reserving a resource, or writing outside the canonical event transaction is an **external effect**.

The architecture SHALL prevent a crash between canonical state mutation and an external effect from producing unbounded duplicate/phantom executions.

Use the minimum justified pattern that establishes these semantics:

1. persist a deterministic intent/obligation with stable idempotency identity before or atomically with effect eligibility;
2. perform the external effect through an idempotent/reconcilable adapter boundary;
3. record the observed effect outcome as a new accepted event;
4. on ambiguous crash/restart, reconcile actual external state before retrying rather than assuming success or failure.

This does not mandate a specific "outbox" framework or distributed transaction system. It mandates the behavior.

An external effect SHALL NOT be considered completed merely because the reducer intended it, and the reducer SHALL NOT perform nondeterministic I/O during historical replay.

## 4. Canonical control durability and recovery

Because Protocol 7 makes the control plane mandatory, its canonical event history becomes operationally critical and requires an explicit durability/recovery contract.

The D3 architecture SHALL define, proportionately to the deployment model:

- transactional/atomic accepted-event publication boundary;
- corruption detection and recovery behavior;
- durable flush/commit semantics sufficient for the claimed crash model;
- backup/export and restore/import path for canonical non-secret control history;
- project/repository identity mapping needed to recover state after moving/recreating a local worktree;
- compatibility checks preventing restore under an incompatible reducer/schema/protocol without explicit migration;
- retention policy for transport-only and derived data distinct from canonical accepted history.

Do not require a network database or distributed consensus for a single-user/local orchestrator unless deployment requirements justify it. SQLite or another small transactional store may be sufficient. The requirement is recoverable deterministic authority, not infrastructure size.

Derived state/indexes may be discarded and rebuilt. Loss of canonical accepted history must not be silently papered over by reconstructing workflow authority from workplan prose or Git directory placement.

## 5. Snapshots/checkpoints remain derived acceleration

A control-state snapshot/checkpoint may accelerate startup/replay when the event history grows, but it SHALL identify:

- protocol/control/ruleset versions;
- last included accepted event/sequence;
- integrity identity sufficient to detect mismatched history;
- derived-state schema version.

A snapshot is not an independent authority. If it disagrees with the canonical event lineage, treat that as corruption/integrity failure and rebuild or repair rather than choosing whichever state is convenient.

## 6. Scheduler observations and replay

Revision 1 preserves Scheduler as resource-routing authority subordinate to workflow readiness. Complete that rule:

- Scheduler may observe live resource/account state for **new** admission/routing decisions;
- the resulting admission/reservation/route decision that affects workflow must be captured as a control observation/event;
- historical replay reuses the recorded accepted decision/facts and does not recompute old routing against today's quotas/prices/account availability;
- rerouting after a new resource observation is a new event/decision, not reinterpretation of the old event.

This preserves both deterministic history and evolving resource conditions.

## 7. Qualification additions

Protocol 7 qualification SHALL include bounded scenarios for:

1. replay produces identical state even when wall-clock time and live external state differ from the original execution environment;
2. lease/timer expiry is driven by recorded control observations rather than ambient replay time;
3. crash after effect intent but before external start reconciles without duplicate execution;
4. crash after external start but before outcome recording reconciles the ambiguous start before retry;
5. historical Scheduler decisions are not recomputed from current resource state during replay;
6. derived-state/snapshot corruption is detected and rebuilds from canonical history;
7. canonical event-history export/restore reproduces the same state under the compatible ruleset;
8. incompatible restore/replay is blocked pending explicit migration rather than silently reinterpreted;
9. loss of a derived index does not force fallback to document-controlled workflow authority.

## 8. Additional D3 and acceptance requirements

The Protocol 7 D3 architecture cannot close until it specifies the observation/effect/reducer boundary and a recoverable canonical persistence model.

Protocol 7 cannot cut over until:

- reducer behavior is independent of ambient mutable state during replay;
- all transition-affecting nondeterministic/external facts cross a typed observation/event boundary;
- effect execution is idempotent or reconcilable across crash/retry boundaries;
- canonical history has a tested backup/export and compatible restore path;
- project/worktree relocation does not silently orphan or alias control authority;
- deterministic replay/recovery qualification above passes.

## 9. Final second-review disposition

```text
SERIOUS CHALLENGE: NONE
SECOND REVIEW FINAL PASS: PASS AFTER REVISIONS 1 AND 2
REMAINING IDENTIFIED BLOCKING DESIGN GAPS: NONE
PROTOCOL 7 IMPLEMENTATION: PROPOSED / BLOCKED ON COMPLETED QUALIFIED 6.1 AND REQUIRED D3 REDESIGN
CURRENT HANDOFF: PARENT + REVISION 1 + REVISION 2
```
