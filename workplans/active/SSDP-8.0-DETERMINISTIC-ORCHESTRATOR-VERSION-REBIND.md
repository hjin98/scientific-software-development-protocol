---
kind: protocol-future-major-version-rebind
workplan_id: SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND
protocol_version: 6.6.0
status: active
created_date: 2026-09-27
supersedes_target_version: 7.0.0
new_target_version: 8.0.0
active_serious_challenge: none
---

# SSDP 8.0 Deterministic Orchestrator Version Rebind

## Purpose

The previously proposed deterministic control-plane / mandatory-orchestrator major revision is reassigned from Protocol 7.0 to Protocol 8.0.

This is a version/lifecycle reassignment only. It does not accept, reject, implement, simplify, or otherwise mutate the substantive deterministic-orchestrator design. The existing active design family beginning with:

`workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`

and its Revisions 1-7 remains the historical and substantive design input for the future deterministic-orchestrator cycle, but every target-version statement in that family that formerly designated Protocol 7.0 is superseded by this record and SHALL be interpreted as targeting Protocol 8.0.

The old filenames are intentionally preserved as historical design identities rather than rewritten in place. No Protocol 8.0 D4 implementation is authorized by this rebind.

## Reason

A newly identified major protocol deficiency in scientific epistemic transparency, human-legible realized-data reporting, epistemic initiative, and discovery feedback is more fundamental to the current scientific-software contract and is assigned Protocol 7.0. The deterministic control-plane proposal remains important but is deferred to Protocol 8.0 so the two independent major doctrine changes do not collide.

## Current disposition

```text
ACCEPTED CURRENT: Protocol 6.6.0
NEW PROTOCOL 7 TARGET: scientific epistemic closure / transparency / discovery
DETERMINISTIC ORCHESTRATOR TARGET: Protocol 8.0
DETERMINISTIC ORCHESTRATOR DESIGN CONTENT: PRESERVED
DETERMINISTIC ORCHESTRATOR D3 REASSESSMENT: STILL REQUIRED BEFORE D4
PROTOCOL 8 D4: NOT AUTHORIZED
```

## Known Protocol 7 inputs to the Protocol 8 D3 reassessment

These are recorded now so the Protocol 8 reassessment does not rediscover them. They are inputs, not Protocol 8 design decisions:

- Protocol 7's human-gate evidence contract is a semantic adequacy judgment. A deterministic control plane may represent gate state, but a machine-checkable presence predicate (for example "evidence artifact attached") cannot satisfy it. Protocol 8 must not reduce gate-evidence adequacy to such a predicate.
- Protocol 7 keeps realized-scientific-record and feedback-persistence state in existing project artifacts, not in control-plane state, and requires no orchestrator transition/control-semantics change.
- If Protocol 7 is accepted, its closeout authors the Protocol 8 inheritance reconciliation (Revision 8). That reconciliation advances the pre-cutover fallback/rollback baseline from Protocol 6.6 recovery to Protocol 7 recovery. Until then, Revision 7's Protocol 6.6 baseline stands.

Governing Protocol 7 handoff: `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`.

## Stale-label rule

Any current routing/index artifact that calls the deterministic-orchestrator family "Protocol 7" is stale with respect to target-version identity and must be reconciled during the Protocol 7 planning/implementation cycle without rewriting immutable historical release records.
