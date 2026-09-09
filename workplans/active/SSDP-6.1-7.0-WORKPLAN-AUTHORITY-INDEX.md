---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.0.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-09
active_serious_challenge: none
---

# SSDP 6.1 / 7.0 Workplan Authority Index

## Purpose

This file is a **routing/index artifact**, not a D1-D4 semantic authority and not an independent implementation contract. It identifies the complete current workplan composition so an implementer/reviewer does not miss a governing artifact.

Do not copy substantive requirements into this index. Read the listed governing artifacts themselves.

## Protocol 6.1 current implementation handoff

Protocol 6.1 is intentionally consolidated into one snapshot-complete current workplan:

1. `workplans/active/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`

The former second-review companion was folded losslessly into the parent during final pre-implementation review and is no longer a separate current contract. Git retains its development history; implementation must use the consolidated parent rather than mentally applying amendment history.

Current review disposition:

```text
SERIOUS CHALLENGE: NONE
FINAL WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: ACTIVE
READY FOR IMPLEMENTATION: YES
```

Protocol 6.1 remains the final document-controlled/semi-automated release and must be completed, behaviorally qualified, independently reviewed, and pinned as an immutable recovery snapshot before Protocol 7 cutover work can become canonical.

## Protocol 7.0 current design handoff

Protocol 7.0 design/implementation/review SHALL read and satisfy, as one composed handoff:

1. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`

Precedence:

- Revision 1 closes ownership, semantic/control binding, storage/transport, cutover, lifecycle-migration, graph-completeness, and compatibility gaps and corrects Scheduler/control-kernel ownership.
- Revision 2 closes reducer-purity, ambient-state, external-effect, deterministic replay, and canonical recovery gaps.
- Every parent requirement not explicitly changed by the revisions remains binding.
- Protocol 7 inherits the accepted final Protocol 6.1 authority/evidence/evolution terminology and dependency semantics unless 7.0 explicitly replaces a rule through its own accepted authority revision.

Current review disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: PROPOSED
BLOCKED ON: COMPLETED + QUALIFIED + IMMUTABLY PINNED PROTOCOL 6.1
ALSO REQUIRES: DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION BEFORE D4 IMPLEMENTATION
```

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Under Protocol 6.1, workplan/skill/prompt/profile document control remains valid and the Protocol 7 control plane is non-authoritative.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Fallback from Protocol 7 uses the immutable Protocol 6.1 release as a version rollback, never a simultaneous dual-current control system.

## Historical discipline

Do not edit archived/version-pinned Protocol 6.0/5.x transition records merely to adopt 6.1 terminology. Current 6.1/7.0 work follows abstraction/concretization terminology while legacy stable identifiers may retain older lexemes only under the compatibility rule in the consolidated 6.1 workplan.

When these workplans complete, preserve normal repository closeout/history conventions; this index may then be archived or replaced by accepted release/version authority mapping. It must not become a permanent parallel protocol authority.
