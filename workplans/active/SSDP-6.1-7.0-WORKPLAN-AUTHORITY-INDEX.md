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

## Protocol 6.1 completed implementation handoff

Protocol 6.1 was implemented and independently reviewed from the composed handoff:

1. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`
2. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE.md`

The archived files preserve the exact reviewed handoff bytes, including their pre-closeout `status: active` metadata. Their **current lifecycle state is completed/archived** as established by this index, the final independent Review, and repository placement; the historical metadata is intentionally not rewritten after Review merely to manufacture a different reviewed artifact.

Precedence for historical reconstruction remains:

- the consolidated parent governed evidence/evolution/concretization implementation;
- Revision 1 supplemented it with the human-facing background/terminology/abbreviation standard and fourth-review closures;
- every parent requirement not explicitly narrowed by Revision 1 remained binding;
- the composition was required to remain lossless with respect to Protocol 6.0 and inherited Protocol 5.16 doctrine.

Final implementation/review/closeout disposition:

```text
SERIOUS CHALLENGE: NONE
FINAL WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION: COMPLETE
BEHAVIORAL QUALIFICATION: PASS — 92 SCENARIOS, NO UNRESOLVED FAILURE
FINAL INDEPENDENT REVIEW: PASS
BLOCKING FINDINGS OPEN: 0
SEMANTIC CANDIDATE: 25d30858e7a33a72cb04b4d07393cb143b7777f8
IMMUTABLE PROTOCOL 6.1 RECOVERY: dec5ff2767e14fd1cda46e073757aa27f40e270c
LIFECYCLE STATUS: COMPLETED / ARCHIVED / PINNED
```

The final Review is `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1.md`. The immutable recovery commit is the coherent lifecycle-closeout snapshot immediately before this documentation-only mapping commit. No qualified Protocol 6.1 semantic source was changed during closeout.

## Protocol 7.0 current design handoff

Protocol 7.0 design/implementation/review SHALL read and satisfy, as one composed handoff:

1. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`

Precedence:

- Revision 1 closes ownership, semantic/control binding, storage/transport, cutover, lifecycle-migration, graph-completeness, and compatibility gaps and corrects Scheduler/control-kernel ownership;
- Revision 2 closes reducer-purity, ambient-state, external-effect, deterministic replay, and canonical recovery gaps;
- every parent requirement not explicitly changed by the revisions remains binding;
- Protocol 7 inherits the accepted final Protocol 6.1 authority/evidence/evolution/dependency doctrine and human-facing documentation standard unless 7.0 explicitly replaces a rule through accepted authority revision.

Current review disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: PROPOSED
PROTOCOL 6.1 COMPLETION/QUALIFICATION/PIN PREREQUISITE: SATISFIED
REMAINING PRE-D4 REQUIREMENT: DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
```

Protocol 6.1 implementation, qualification, independent Review, lifecycle archival, and immutable recovery mapping are complete. This clears only the Protocol-6.1 prerequisite for Protocol 7. It does **not** authorize Protocol 7 D4 implementation until the separately required deliberate D3 orchestrator architecture reopen/supersession is completed under the Protocol 7 handoff.

Protocol 7 machine control records remain compact machine data. Human-readable control/schema/user documentation inherits the Protocol 6.1 background-context and first-use abbreviation requirements.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Under Protocol 6.1, workplan/skill/prompt/profile document control remains valid and the Protocol 7 control plane is non-authoritative.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Fallback from Protocol 7 uses immutable Protocol 6.1 commit `dec5ff2767e14fd1cda46e073757aa27f40e270c` as a version rollback, never a simultaneous dual-current control system.

## Historical discipline

Do not edit archived/version-pinned Protocol 6.0/5.x transition records merely to adopt 6.1 terminology or presentation rules. Current 6.1/7.0 work follows abstraction/concretization terminology and the human-facing documentation standard while legacy stable identifiers may retain older lexemes only under the explicit compatibility rule in the current 6.1 handoff.

The completed Protocol 6.1 workplans are archived as exact reviewed historical handoff artifacts. The active index remains because it also routes the proposed Protocol 7.0 work. It must not become permanent parallel protocol authority.