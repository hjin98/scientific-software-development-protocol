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

## Protocol 6.1 completed repaired handoff

Protocol 6.1 was originally implemented and reviewed from the composed historical handoff:

1. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`
2. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE.md`

A later independent review found two current-source conformance defects and an acceptance-oracle gap. The bounded repair was governed by:

3. `workplans/archive/SSDP-6.1-REOPENED-FINAL-REVIEW-REPAIR.md`

All three files are now archived historical handoff evidence. Their historical frontmatter is preserved rather than rewritten after execution/review. Current completion is established by this index, the fresh qualification/Review records, semantic-evolution history, and the immutable recovery mapping.

Precedence for reconstruction remains:

- the consolidated parent governed evidence/evolution/concretization implementation;
- Revision 1 supplemented it with the human-facing background/terminology/abbreviation standard and fourth-review closures;
- the reopened repair corrected discovered nonconformance without changing Protocol 6.1 doctrine;
- every parent requirement not explicitly narrowed by a later artifact remains binding;
- the composition remains lossless with respect to Protocol 6.0 and inherited Protocol 5.16 doctrine.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
PREVIOUS FINAL WORKPLAN DESIGN REVIEW: PASS — HISTORICAL
PREVIOUS IMPLEMENTATION/QUALIFICATION/REVIEW CLOSEOUT: SUPERSEDED FOR RELEASE CLOSURE
REOPENED IMPLEMENTATION STATUS: COMPLETE
BEHAVIORAL QUALIFICATION: PASS — 94/94
FINAL INDEPENDENT REVIEW: PASS — qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1-REOPENED.md
OPEN BLOCKING FINDINGS: 0
SEMANTIC CANDIDATE: 5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef
PREVIOUS RECOVERY SNAPSHOT: dec5ff2767e14fd1cda46e073757aa27f40e270c — HISTORICAL, NOT FINAL ACCEPTED RECOVERY
REPLACEMENT RECOVERY SNAPSHOT: THIS LIFECYCLE-CLOSEOUT COMMIT — IMMUTABLE SHA RECORDED BY THE IMMEDIATELY FOLLOWING METADATA-ONLY PIN
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

The prior Review `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1.md` remains historical evidence for the earlier candidate. The fresh current Review is `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1-REOPENED.md`, which reviews semantic candidate `5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef` after complete repository/package acceptance and fresh 94-scenario qualification.

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
PROTOCOL 6.1 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED BY THIS CLOSEOUT; EXACT IMMUTABLE SHA IS RECORDED BY THE IMMEDIATELY FOLLOWING METADATA-ONLY PIN
REMAINING PRE-D4 REQUIREMENTS:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
```

Protocol 7 D4 implementation remains unauthorized until the remaining D3 Orchestrator architecture prerequisite closes. The completed Protocol 6.1 repair does not modify Protocol 7 semantics; it restores and pins the valid pre-automation baseline Protocol 7 requires.

Protocol 7 machine control records remain compact machine data. Human-readable control/schema/user documentation inherits the Protocol 6.1 background-context and first-use abbreviation requirements.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Under Protocol 6.1, workplan/skill/prompt/profile document control remains valid and the Protocol 7 control plane is non-authoritative.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Protocol 7 fallback uses the replacement immutable Protocol 6.1 recovery commit established by this closeout and identified by the immediately following metadata-only pin. The historical `dec5ff2767e14fd1cda46e073757aa27f40e270c` snapshot is not the final rollback baseline after the discovered defects.

## Historical discipline

Do not edit archived/version-pinned Protocol 6.0/5.x transition records merely to adopt 6.1 terminology or presentation rules. Current 6.1/7.0 work follows abstraction/concretization terminology and the human-facing documentation standard while legacy stable identifiers may retain older lexemes only under the explicit compatibility rule in the current 6.1 handoff.

The original Protocol 6.1 workplans and the reopened repair workplan remain archived as exact historical handoff artifacts. Current completion/recovery state is recorded by this index, current portability mapping, semantic-evolution history, the fresh qualification/Review records, and the replacement immutable recovery pin.