---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.0.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-10
active_serious_challenge: none
---

# SSDP 6.1 / 6.2 / 7.0 Workplan Authority Index

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** uses D1 scientific/mathematical, D2 algorithm/numerical, D3 software-architecture, and D4 specification/implementation authority. This file is only a routing/index artifact: it identifies complete workplan composition and lifecycle state, but creates no independent D1-D4 semantic authority. A **semantic candidate** is the immutable Git commit under qualification; a **recovery snapshot** is an immutable commit accepted for rollback.

## Purpose

Do not copy substantive requirements into this index. Read the listed governing artifacts themselves. Archived workplans preserve the exact historical handoff that governed completed cycles; later work may supersede current release/closeout disposition without rewriting those historical artifacts.

## Protocol 6.1 completed handoff

Protocol 6.1 second-reopen implementation/review is complete. Its governing handoff is preserved as one composed archived record:

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
- second-reopen Revision 1 superseded only the parent repair's direct-only package-membership freeze after live counterexample evidence exposed unresolved transitive local Markdown routes; direct `SKILL.md` routes remain activation seeds while transport payload uses bounded transitive local-Markdown closure;
- every parent requirement not explicitly narrowed by a later artifact remains binding;
- those repairs changed no accepted D1/D2/D3 doctrine and introduced no Protocol 7 implementation machinery.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SECOND REOPEN FINDINGS: 3 BLOCKING — ALL CLOSED
PACKAGE-DESIGN RECONCILIATION: COMPLETE — BOUNDED TRANSITIVE TRANSPORT CLOSURE
SEMANTIC CANDIDATE: be7d05827f52a3029c294c38edf5ede1afb1f9b4
PUBLIC BOOTSTRAP: 47e9155632c44493644b0b02fa1fa625703cf480
FRESH QUALIFICATION: 95/95 PASS — EVIDENCE COMMIT 48771f9235232bf59428d78686d116ef52965571
FRESH INDEPENDENT REVIEW: PASS — REVIEW/RECOVERY COMMIT 802e75af261efb4f70d71284d860613a2197b639
RECOVERY MAPPING COMMIT: dfc09bb54cd407f64e4b2a07f1bba0a1e4f76b3c
STAGE-D GENERATED-DISTRIBUTION COMMIT: 5458b1be2b536b83b6854ab9906602acc5f5f0c4
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

Current closeout evidence is `qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED-95.md` plus `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED.md`. Earlier qualification/Review records remain historical evidence only for their evaluated candidates.

## Protocol 6.2 current implementation handoff

Current governing workplan:

1. `workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md`

Protocol 6.2 is a backward-compatible representation/progressive-disclosure strengthening governed by accepted Protocol 6.1. It preserves every accepted 6.1 doctrine and still-valid historical capability as a hard prerequisite; it may generalize, relocate, compact, or reroute their representation but may not semantically retire them inside this cycle. The workplan also corrects current terminology by migrating `abstraction-and-realization.md` to `abstraction-and-concretization.md` while leaving frozen historical releases untouched.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
FINAL WORKPLAN CLOSURE REVIEW: PASS AFTER REPAIR
WORKPLAN STATUS: ACTIVE CYCLE AUTHORITY
IMPLEMENTATION HANDOFF: AUTHORIZED
IMPLEMENTATION STATUS: EXECUTED / ASSEMBLED
SEMANTIC CANDIDATE: ebbc4591bdfed039512026b8acb3a6749475c1c5
PUBLIC BOOTSTRAP: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
INVALIDATED BOOTSTRAP ATTEMPT: 1181c2031710c5d343194d87d08543290fded0ab
QUALIFICATION: ORIGINAL 115/115 PASS + COLD-ROUTE REQUALIFICATION PASS + BOOTSTRAP REQUALIFICATION PASS
GENERATED / PACKAGE / CORE ACCEPTANCE: PASS — CLEAN RUN 34556209092; POST-EVIDENCE RUN 34556568108 PASS
INDEPENDENT REVIEW: PENDING — REQUIRED BEFORE STAGE G
RECOVERY MAPPING: NOT PUBLISHED
LIFECYCLE STATUS: ACTIVE — BLOCKED ON INDEPENDENT REVIEW, THEN RECOVERY / CLOSEOUT
PARENT ACCEPTED BASELINE: Protocol 6.1 closeout cec29671b9db59d20124a6e2ce99725ed60b8f0a
PARENT RECOVERY: 802e75af261efb4f70d71284d860613a2197b639
TARGET: Protocol 6.2.0
```

The current review packet is `qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.2.md`. It binds Review to semantic candidate `ebbc4591bdfed039512026b8acb3a6749475c1c5`, replacement public bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`, the original 115-case qualification plus both bounded affected requalifications, the preservation transformation map, and refreshed static activation sensors. Author-context reviews and qualification evidence do not satisfy the required independent Review.

Protocol 6.1 remains accepted-current and the rollback authority until Protocol 6.2 independent candidate Review, immutable recovery mapping, mapping-bearing generated-artifact reconciliation, semantic-evolution/lifecycle closeout, and archive transition all pass. On this branch, Protocol 6.2 completion/reconciliation precedes further Protocol 7 D4 work.

## Protocol 7.0 current design handoff

Protocol 7.0 design/implementation/review SHALL read and satisfy, as one composed handoff:

1. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`

Precedence:

- Revision 1 closes ownership, semantic/control binding, storage/transport, cutover, lifecycle-migration, graph-completeness, and compatibility gaps and corrects Scheduler/control-kernel ownership;
- Revision 2 closes reducer-purity, ambient-state, external-effect, deterministic replay, and canonical recovery gaps;
- every parent requirement not explicitly changed by the revisions remains binding;
- the accepted Protocol 7 design currently inherits Protocol 6.1 semantics; after 6.2 acceptance its representation-rule inheritance/cutover references must be reconciled explicitly without silently changing Protocol 7 architecture semantics.

Current review disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: PROPOSED
PROTOCOL 6.1 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED
BRANCH-LOCAL PROTOCOL 6.2 PRE-D4 PREREQUISITE: PENDING INDEPENDENT REVIEW / RECOVERY / CLOSEOUT
REMAINING PROTOCOL-7-SPECIFIC PRE-D4 REQUIREMENT:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
```

Protocol 7 D4 remains unauthorized on this branch until both Protocol 6.2 completion/reconciliation and the existing deliberate Protocol 7 D3 Orchestrator architecture reopen/supersession requirement close.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Protocol 6.1 remains accepted-current while 6.2 remains under independent Review and lifecycle closeout; 6.2 work is governed by this accepted 6.1 cycle handoff.
- After qualified 6.2 acceptance/cutover, Protocol 6.2 becomes the document-controlled current baseline unless separately superseded.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- Until Protocol 6.2 has an accepted immutable recovery identity and Protocol 7 is reconciled to it, the existing Protocol 7 fallback remains Protocol 6.1 recovery `802e75af261efb4f70d71284d860613a2197b639`.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0/6.1 records merely to adopt later terminology or presentation rules. Current 6.2 work must preserve historical capability while expressing current doctrine directly and compactly; detailed history remains recoverable without becoming parallel current authority.
