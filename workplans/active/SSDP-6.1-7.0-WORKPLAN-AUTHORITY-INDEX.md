---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.0.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-10
active_serious_challenge: none
---

# SSDP 6.1 / 7.0 Workplan Authority Index

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** uses D1 scientific/mathematical, D2 algorithm/numerical, D3 software-architecture, and D4 specification/implementation authority. This file is only a routing/index artifact: it identifies the complete workplan composition and lifecycle state, but it does not create independent D1-D4 semantic authority. A **semantic candidate** is the immutable Git commit under qualification; a **recovery snapshot** is an immutable commit accepted for rollback.

## Purpose

Do not copy substantive requirements into this index. Read the listed governing artifacts themselves. Archived workplans preserve the exact historical handoff that governed their completed cycles; a later repair may supersede release/closeout disposition without rewriting those historical artifacts.

## Protocol 6.1 second-reopened handoff

Protocol 6.1 implementation/review now SHALL read and satisfy, as one composed handoff:

1. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`
2. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE.md`
3. `workplans/archive/SSDP-6.1-REOPENED-FINAL-REVIEW-REPAIR.md`
4. `workplans/active/SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR.md`

Precedence and preservation:

- the consolidated parent governs evidence/evolution/concretization semantics and lossless Protocol 6.0/5.16 inheritance;
- Revision 1 supplements it with the human-facing background/terminology/abbreviation standard;
- the first reopened repair corrected D3/D4 evidence-realization terminology, canonical navigation, and associated acceptance oracles;
- the second reopened repair corrects package transitive-reference closure, version-correct immutable public fallback/recovery documentation, and incomplete application of the already-accepted human-facing standard;
- every parent requirement not explicitly narrowed by a later artifact remains binding;
- no current repair changes accepted D1/D2/D3 doctrine or authorizes Protocol 7 implementation machinery.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
PREVIOUS 94/94 QUALIFICATION: HISTORICAL FOR CURRENT CLOSEOUT
PREVIOUS FINAL INDEPENDENT REVIEW: HISTORICAL FOR CURRENT CLOSEOUT
SECOND REOPEN FINDINGS: 3 BLOCKING
SECOND REOPEN IMPLEMENTATION STATUS: ACTIVE
OPEN BLOCKING FINDINGS: 3
PREVIOUS SEMANTIC CANDIDATE: 5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef — HISTORICAL
PREVIOUS RECOVERY SNAPSHOT: 0c90fda19bf6ed9cb0c4511beb3da80ace6584ed — IMMUTABLE HISTORICAL, NOT FINAL ACCEPTED RECOVERY
REPLACEMENT RECOVERY SNAPSHOT: PENDING SECOND-REOPEN QUALIFICATION/REVIEW/CLOSEOUT
LIFECYCLE STATUS: ACTIVE / NO-PASS
```

The prior current Review `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1-REOPENED.md` and fresh 94-scenario result remain valid historical evidence for the candidate they evaluated. They cannot close the newly affected package/public-fallback/documentation surfaces.

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
PROTOCOL 6.1 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: REOPENED / UNSATISFIED
REMAINING PRE-D4 REQUIREMENTS:
  1. COMPLETE AND REQUALIFY THE SECOND-REOPEN PROTOCOL 6.1 REPAIR
  2. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
```

Protocol 7 D4 implementation remains unauthorized until both requirements close. The second Protocol 6.1 repair does not modify Protocol 7 semantics; it restores the valid pre-automation baseline Protocol 7 requires.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Under Protocol 6.1, workplan/skill/prompt/profile document control remains valid and the Protocol 7 control plane is non-authoritative.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Protocol 7 fallback may use only the replacement immutable Protocol 6.1 recovery identity accepted after this second reopen. Earlier Protocol 6.1 recovery snapshots remain historical evidence.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0 records merely to adopt 6.1 terminology or presentation rules. Do not rewrite the earlier Protocol 6.1 workplans or prior qualification/Review reports merely to hide the reason for reopening. Current 6.1 artifacts follow abstraction/concretization terminology and the human-facing documentation standard while legacy stable identifiers may retain older lexemes only under the explicit compatibility rule.
