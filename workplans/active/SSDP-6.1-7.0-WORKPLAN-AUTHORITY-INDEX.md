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

Protocol 6.1 second-reopen implementation/review is complete. The governing handoff is preserved as one composed archived record:

1. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT.md`
2. `workplans/archive/SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT-REVISION-1-HUMAN-FACING-DOCUMENTATION-AND-FINAL-REVIEW-CLOSURE.md`
3. `workplans/archive/SSDP-6.1-REOPENED-FINAL-REVIEW-REPAIR.md`
4. `workplans/archive/SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR.md`
5. `workplans/archive/SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR-REVISION-1-PACKAGE-CLOSURE.md`

Precedence and preservation:

- the consolidated parent governs evidence/evolution/concretization semantics and lossless Protocol 6.0/5.16 inheritance;
- Revision 1 supplements it with the human-facing background/terminology/abbreviation standard;
- the first reopened repair corrected D3/D4 evidence-realization terminology, canonical navigation, and associated acceptance oracles;
- the second reopened repair corrected package reference closure, version-correct immutable public fallback/recovery documentation, and incomplete application of the already-accepted human-facing standard;
- second-reopen Revision 1 superseded only the parent repair's direct-only package-membership freeze after live counterexample evidence exposed 68 unresolved transitive local Markdown routes; direct `SKILL.md` routes remain activation seeds while transport payload uses bounded transitive local-Markdown closure;
- every parent requirement not explicitly narrowed by a later artifact remains binding;
- the repair changed no accepted D1/D2/D3 doctrine and introduced no Protocol 7 implementation machinery.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SECOND REOPEN FINDINGS: 3 BLOCKING — ALL CLOSED
PACKAGE-DESIGN RECONCILIATION: COMPLETE — DIRECT-ONLY MEMBERSHIP SUPERSEDED BY BOUNDED TRANSITIVE CLOSURE
SECOND REOPEN IMPLEMENTATION STATUS: COMPLETE — SEMANTIC CANDIDATE be7d05827f52a3029c294c38edf5ede1afb1f9b4; PUBLIC BOOTSTRAP 47e9155632c44493644b0b02fa1fa625703cf480
FRESH QUALIFICATION: 95/95 PASS — EVIDENCE COMMIT 48771f9235232bf59428d78686d116ef52965571
FRESH INDEPENDENT REVIEW: PASS — ZERO OPEN BLOCKERS — REVIEW COMMIT 802e75af261efb4f70d71284d860613a2197b639
OPEN IMPLEMENTATION/REVIEW FINDINGS: 0
PREVIOUS SEMANTIC CANDIDATE: 5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef — HISTORICAL
PREVIOUS RECOVERY SNAPSHOT: 0c90fda19bf6ed9cb0c4511beb3da80ace6584ed — IMMUTABLE HISTORICAL, SUPERSEDED
REPLACEMENT RECOVERY SNAPSHOT: 802e75af261efb4f70d71284d860613a2197b639 — ACCEPTED IMMUTABLE ROLLBACK
RECOVERY MAPPING COMMIT: dfc09bb54cd407f64e4b2a07f1bba0a1e4f76b3c
STAGE-D MAPPING ACCEPTANCE: PASS — GITHUB ACTIONS RUN 34451700073; GENERATED-DISTRIBUTION COMMIT 5458b1be2b536b83b6854ab9906602acc5f5f0c4
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

The current closeout evidence is `qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED-95.md` plus `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED.md`. Earlier 92/94-scenario qualification and Review records remain historical evidence only for the candidates they evaluated. Stage-D mapping acceptance regenerated the affected tracked package transports from canonical source, reran repository/package/orchestrator checks, and removed temporary transport machinery before lifecycle closeout.

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
PROTOCOL 6.1 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED — RECOVERY 802e75af261efb4f70d71284d860613a2197b639
REMAINING PRE-D4 REQUIREMENTS:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
```

Protocol 7 D4 implementation remains unauthorized until the remaining deliberate D3 Orchestrator architecture reopen/supersession requirement closes. The completed second Protocol 6.1 repair did not modify Protocol 7 semantics; it restored and qualified the pre-automation baseline Protocol 7 requires.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Under Protocol 6.1, workplan/skill/prompt/profile document control remains valid and the Protocol 7 control plane is non-authoritative.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Protocol 7 fallback uses replacement immutable Protocol 6.1 recovery identity `802e75af261efb4f70d71284d860613a2197b639`. Earlier Protocol 6.1 recovery snapshots remain historical evidence.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0 records merely to adopt 6.1 terminology or presentation rules. Do not rewrite the earlier Protocol 6.1 workplans or prior qualification/Review reports merely to hide the reason for reopening. Current 6.1 artifacts follow abstraction/concretization terminology and the human-facing documentation standard while legacy stable identifiers may retain older lexemes only under the explicit compatibility rule.
