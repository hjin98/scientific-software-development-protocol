---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.3.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-12
active_serious_challenge: none
---

# SSDP 6.1 / 6.2 / 6.3 / 7.0 Workplan Authority Index

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

## Protocol 6.2 completed handoff

Protocol 6.2 lossless-representation/progressive-disclosure implementation, qualification, independent Review, recovery, generated reconciliation, and closeout are complete. The governing workplan is preserved byte-identically at:

1. `workplans/archive/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md`

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SEMANTIC CANDIDATE: ebbc4591bdfed039512026b8acb3a6749475c1c5
PUBLIC BOOTSTRAP: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
INVALIDATED BOOTSTRAP ATTEMPT: 1181c2031710c5d343194d87d08543290fded0ab
QUALIFICATION: ORIGINAL 115/115 PASS + COLD-ROUTE REQUALIFICATION PASS + BOOTSTRAP REQUALIFICATION PASS
INDEPENDENT REVIEW: PASS — qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md
RECOVERY: b59adc77efe6951912cfd705cc43830c58ca27d0
RECOVERY MAPPING COMMIT: bc76b16fda96be09f38a1b40a2ef877e8309534d
MAPPING-BEARING GENERATED COMMIT: ca622ea2b1c33e70668060cf0cc2fe9138776f7f
STAGE G ACCEPTANCE: PASS — GITHUB ACTIONS RUN 34566291966
LIFECYCLE STATUS: COMPLETED / ARCHIVED
PARENT ACCEPTED BASELINE: Protocol 6.1 closeout cec29671b9db59d20124a6e2ce99725ed60b8f0a
PARENT HISTORICAL ROLLBACK: 802e75af261efb4f70d71284d860613a2197b639
CURRENT ACCEPTED DOCUMENT-CONTROLLED BASELINE: Protocol 6.2
```

The public-source bootstrap and accepted recovery remain intentionally distinct. Static activation sensors remain structural evidence only; no live token, latency, cache, or model-performance claim was accepted without corresponding live telemetry.

## Protocol 6.3 completed handoff

Protocol 6.3 evidence-backed project-engineering-memory implementation, qualification, repaired bootstrap publication, independent Review R2, recovery, mapping-bearing regeneration, and Stage G closeout are complete. Its governing workplan is preserved as reviewed historical evidence at:

1. `workplans/archive/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md`

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SEMANTIC CANDIDATE: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
PUBLIC BOOTSTRAP: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
BOOTSTRAP PUBLICATION DESCENDANT: a8dac814cc2813b3bb336e5b6abde5fbcf44949e
QUALIFICATION: F5 + D9 repair + bootstrap/publication affected requalification PASS
INDEPENDENT REVIEW R2: PASS — qualification/ssdp6/FINAL-REVIEW-R2-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3.md
RECOVERY: 9f353097fab36e325a325f1c2f9d9cec32e86177
RECOVERY MAPPING COMMIT: 0c76c0461b7376f17182d29ba145a198a092463c
MAPPING-BEARING GENERATED COMMIT: e75282ae850b774a9466902f4c74ba6a179116bd
STAGE G ACCEPTANCE: PASS — GITHUB ACTIONS RUN 34699052516
LIFECYCLE STATUS: COMPLETED / ARCHIVED
PARENT ACCEPTED BASELINE: Protocol 6.2 recovery b59adc77efe6951912cfd705cc43830c58ca27d0
CURRENT ACCEPTED DOCUMENT-CONTROLLED BASELINE: Protocol 6.3
```

The public-source bootstrap and accepted recovery remain intentionally distinct. Historical invalidated 6.3 bootstrap/candidate attempts remain immutable negative evidence rather than current fallback. PEM remains non-authoritative project-local decision support; no D5 or parallel control plane was accepted.

## Protocol 7.0 current design handoff

Protocol 7.0 design/implementation/review SHALL read and satisfy, as one composed handoff:

1. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`
4. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`
5. `workplans/active/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md`

Precedence:

- Revision 1 closes ownership, semantic/control binding, storage/transport, cutover, lifecycle-migration, graph-completeness, and compatibility gaps and corrects Scheduler/control-kernel ownership;
- Revision 2 closes reducer-purity, ambient-state, external-effect, deterministic replay, and canonical recovery gaps;
- Revision 3 changes only representation/version inheritance after Protocol 6.2 acceptance: current pre-cutover document-controlled baseline and fallback/rollback became Protocol 6.2, while the parent/Revisions 1-2 D3 architecture semantics remained unchanged;
- Revision 4 changes only project-learning/version inheritance after Protocol 6.3 acceptance: current pre-cutover document-controlled baseline and fallback/rollback become Protocol 6.3, while the parent/Revisions 1-3 D3 architecture semantics remain unchanged;
- every parent requirement not explicitly changed by a later revision remains binding.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS
IMPLEMENTATION STATUS: PROPOSED
PROTOCOL 6.1 HISTORICAL COMPLETION/RECOVERY: SATISFIED
PROTOCOL 6.2 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED
PROTOCOL 6.3 COMPLETION/QUALIFICATION/R2-REVIEW/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.3 INHERITANCE RECONCILIATION: SATISFIED
CURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.3 recovery 9f353097fab36e325a325f1c2f9d9cec32e86177
REMAINING PROTOCOL-7-SPECIFIC PRE-D4 REQUIREMENT:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
PROTOCOL 7 D4: NOT AUTHORIZED
```

Protocol 7 D4 remains unauthorized until the existing deliberate D3 Orchestrator architecture reopen/supersession requirement closes. Revisions 3-4 do not perform that reopen and no `main` or Protocol 7 cutover is implied.

## Version/cutover rule

There is exactly one canonical workflow-control authority for any current run.

- Protocol 6.3 is the accepted-current document-controlled baseline; version-bound 6.2 work may still resolve immutable historical recovery `b59adc77efe6951912cfd705cc43830c58ca27d0` and older declared versions retain their own mappings.
- Protocol 7 remains proposed/pre-cutover. Its current fallback/rollback baseline is Protocol 6.3 recovery `9f353097fab36e325a325f1c2f9d9cec32e86177` until Protocol 7 itself completes the outstanding D3 architecture reopen and subsequent D4/Review/qualification/recovery/cutover gates.
- Under Protocol 7 after qualified cutover, the deterministic orchestrator control plane owns machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- No `main` merge or Protocol 7 cutover is authorized by Protocol 6.3 closeout.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0/6.1 records merely to adopt later terminology or presentation rules. Current 6.2 work must preserve historical capability while expressing current doctrine directly and compactly; detailed history remains recoverable without becoming parallel current authority.
