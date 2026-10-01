---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.6.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-10-01
active_serious_challenge: none
---

# SSDP 6.1 / 6.2 / 6.3 / 6.4 / 6.5 / 6.6 / 7.0 / SSDS 8.0 Workplan Authority Index

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** uses D1 scientific/mathematical, D2 algorithm/numerical, D3 software-architecture, and D4 specification/implementation authority. This file is only a routing/index artifact: it identifies complete workplan composition and lifecycle state, but creates no independent D1-D4 semantic authority. A **semantic candidate** is the immutable Git commit under qualification; a **recovery snapshot** is an immutable commit accepted for rollback.

## Purpose

Do not copy substantive requirements into this index. Read the listed governing artifacts themselves. Archived workplans preserve the exact historical handoff that governed completed cycles or design-review snapshots; later work may supersede current release/closeout disposition without rewriting those historical artifacts.

## Current major-version reassignment

Protocol 7.0 is now the proposed **Scientific Inspectability, Epistemic Initiative, and Scientific Feedback Loop** major revision (workplan IDs retain the historical `EPISTEMIC-CLOSURE` lexeme). Its single current planning handoff is:

- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`

It supersedes the earlier composition, now preserved as historical design-review evidence only:

1. `workplans/archive/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY.md`
2. `workplans/archive/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-1-FIRST-REVIEW-CLOSURE.md`
3. `workplans/archive/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-2-FEEDBACK-AND-LONGITUDINAL-CLOSURE.md`

The author-side review record `qualification/ssdp70/WORKPLAN-REVIEW-2026-09-27-PROTOCOL-7.0-PASS.md` applies only to the superseded composition, was not independent, and establishes no implementation-handoff readiness. The consolidated handoff's §0 routes prior NO-PASS records and the unchanged stakeholder SC1/SC2 decisions. Its latest independent Review, at `b2d1f4ef28705528406d0fc6e7abde7d6c6c8050`, returned **PASS** with four minor findings, binding that revision only: `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-B2D1F4E-PASS.md`. The handoff file is byte-identical to that revision; its own §0, §0.1 and §16 status lines, which still describe the minor repairs as awaiting Review, are superseded by that record (the preceding `5a2f8c8` PASS record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-5A2F8C8-PASS.md`, the `3baf279` NO-PASS record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-3BAF279-NO-PASS.md`, the `1b21b17` record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-1B21B17-NO-PASS.md`, the `3b12a83` record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-3B12A83-NO-PASS.md`, the `5cfaca7` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-5CFACA7-NO-PASS.md`, the `31845d8` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-31845D8-NO-PASS.md`, the `cb9542d` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-CB9542D-NO-PASS.md`, the `179c7e0` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-179C7E0-NO-PASS.md`, the `4e778e2` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-4E778E2-NO-PASS.md`, the `adaac7b` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-ADAAC7B-NO-PASS.md`, the `41434b1` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-41434B1-NO-PASS.md` and the `67fb29d` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-67FB29D-NO-PASS.md`; the `677a7a82` NO-PASS left no durable record). The reviewer recommends fixing its first three minor findings before Stage A freezes the §11 contract; implementation remains unauthorized until the stakeholder acts on the Review. Stakeholder decision SD-B (2026-09-27) superseded the 6.6 per-route burden cap with a compression target subordinate to lossless required elements: `qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SD-B.md`. The earlier `27fb2bd` Review (`qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-27FB2BD-NO-PASS.md`) found SD-B's premise inaccurate (6.6's cap was relative to 6.5). The stakeholder confirmed SD-B with the corrected premise and retained 6.6's fixed-cost condition as a backstop and escalation trigger: `qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SD-B-CONFIRMATION.md`. Any semantic change to the handoff after `b2d1f4e` needs fresh independent Review by a context that authored neither the workplan nor that change.

The stakeholder subsequently accepted the first three minor-wording repairs and authorized D4 Stages A–F. The revised handoff is independently reviewed at `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-AD0A441-PASS.md`. Stage A's static measurement and independent draft check stopped the cycle before Stage B; the current evidence and open challenge are in `qualification/ssdp70/STAGE-A-STOP-2026-09-28.md`. These current records supersede the preceding paragraph's readiness and authorization status, while its Review chronology remains historical.

The stakeholder then authorized one narrow §8.3 label-table exception for O1, and that exact workplan amendment passed fresh independent Review: `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-69C6383-PASS.md`. The O1 Challenge is resolved for this cycle. One bounded compressed D4 draft passed independent fidelity/attribution checking but still breached the static fixed-cost backstop; `qualification/ssdp70/STAGE-A-COMPRESSION-BACKSTOP-STOP-2026-09-28.md` is the current Stage A stop record. The preceding O1 stop record remains historical.

The stakeholder then relaxed only the Protocol 7 fixed-cost multiplier to 2.0 × fresh paired accepted-6.5 median on each T1/T7/T8 route, preserving the 512 B static margin and other conditions (`qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-28-PROTOCOL-7.0-BACKSTOP-RELAXATION.md`). The substantive handoff overlay passed fresh independent Review at `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-66F2943-PASS.md`, binding handoff SHA-256 `66f29437af5bde3381a66c8a7609ef3ee87b230f32c210eb7fbf1858e22d78b1` and decision SHA-256 `b1ae718c37e17c085146eac085f69e3fc7b6ae5825003fe2c0be746d86cc85e2`. The prior static-cost stop is historical; Stage A is resumed but not closed. Fresh paired live measurements and all later stage gates remain open.

The first Stage A qualification-framework draft failed its independent pre-run check on three material threshold/exposure gaps (`qualification/ssdp70/STAGE-A-CONTRACT-NO-PASS-STOP-2026-09-28.md`, now historical). The repaired framework (SHA-256 `02dd12dbf2468c5134119146bd04b8ae9d46551a505e498aa0e2b885030ce077`) passed a fresh independent recheck (`qualification/ssdp70/STAGE-A-INDEPENDENT-CONTRACT-RECHECK-PASS.md`), a separate fixture custodian is designated, and Stage A is closed: `qualification/ssdp70/STAGE-A-CLOSURE-2026-09-28.md`. Withheld-instance and actual-harness pre-run checks remain required before any candidate run. Stages B–E then implemented and assembled the unfrozen 7.0 candidate (independent Stage D wording recheck PASS). Stage F stopped at entry because the frozen human legibility trial needs stakeholder-designated participants: `qualification/ssdp70/STAGE-F-ENTRY-STOP-2026-09-28.md`. The workplan-level Review PASS above does not pass this later contract.

A fresh Stage F pre-run integrity review at tooling head `1d2ac73ceabb8efce40005540c118e5fbfc407af` returned **STOP/BLOCKED** and is recorded at `qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md`. It found unavailable required withheld/actual-runner evidence and D4 tooling fail-open paths; no comparative campaign ran and the semantic candidate `db94a2d...` remained unchanged. The stakeholder then directed the Stage F plan to remove environment/vendor lock-in. The first portable architecture amendment at `62aa1bbaa9d2d1dfef1b48cede6bc1500837658f` received a fresh independent **NO-PASS** at `qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-NO-PASS-2026-09-28.md`: the core/adapter split was accepted in principle, but execution-profile equivalence, capability/containment/custody semantics, normalized-trace completeness, exact scoring closure, provenance and profile-scoped PASS remained under-specified. The current workplan/contract/amendment repair closes those five D3 gaps while keeping the Protocol 7 semantic candidate unchanged. **Fresh independent Review of the repaired exact bytes is still required before dependent Stage F tooling repair or candidate runs.** Historical Claude Code/`claude-sonnet-5` observations remain bounded evidence about 6.6, not a normative runtime requirement.

```text
PROTOCOL 7 WORKPLAN DESIGN REVIEW: 62aa1bb Stage F portable amendment received fresh independent NO-PASS (011b4fe review record); B1-B5 D3 repair authored and PENDING FRESH INDEPENDENT REVIEW
PROTOCOL 7 D4: stakeholder-authorized Stages A-F; Stages A-E COMPLETE (65b0121, 645ba2e, 980ec18, 67977c6, db94a2d); Stage F PRE-RUN remains STOP/BLOCKED pending repaired-architecture Review PASS, portable-runner tooling repair, and withheld/actual-runner requalification; no active Serious Challenge
PROTOCOL 7 SD-B: SUPERSEDE (2026-09-27); size budget is a compression target, never a reason to break a lossless condition;
  2026-09-28 stakeholder decision supersedes the backstop multiplier with 2.0 x fresh paired accepted 6.5 median on T1/T7/T8;
  current independently fidelity-checked compressed D4 draft 14,331 B is below the historical 16,720 B planning cap and leaves more than the predeclared 512 B margin;
  fresh paired live medians remain unrun
STAKEHOLDER DECISIONS: section 4 rule ACCEPTED; SC1 claim-integrity floor ACCEPTED; SC2 Option B SELECTED (2026-09-27)
```

The previously proposed deterministic control-plane / mandatory-orchestrator design was reassigned to **Protocol 8.0** (2026-09-27) and is now consolidated into one proposed handoff (section below). Its archived design artifacts retain their historical `SSDP-7.0-...` filenames and embedded target wording; those target-version labels mean Protocol 8.0. They do not compete with the Protocol 7.0 target and do not authorize D4 implementation.

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
- those repairs changed no accepted D1/D2/D3 doctrine and introduced no successor deterministic-orchestrator implementation machinery.

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

## Protocol 6.4 completed handoff

Protocol 6.4 design/implementation/review SHALL use the single current consolidated handoff:

1. `workplans/archive/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md`

Earlier parent/Revisions 1-2 and the fifth-review consolidated snapshot are archived design-review evidence. They preserve how the design evolved but are not required to reconstruct the current implementation contract. The current consolidated workplan integrates the still-binding prior semantics plus sixth-review closure for unique canonical-owner conflict handling, extensible semantic-role status, parameterized-family/instance/default semantics, parameter-sensitive evidence applicability, external-content trust/instruction separation, and current-vs-history cleanup.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
STAGE E INDEPENDENT REVIEW: PASS
PUBLIC BOOTSTRAP: e09a9d1480211eea2d16d722182bb5c6de1bee12
RECOVERY: 74bc572ef516cae417437a2027eeff52a2e25c15
RECOVERY MAPPING COMMIT: 6e66478f37de197b6d28707e087c61d687fcfa41
STAGE F: PASS / LIFECYCLE CLOSED
HISTORICAL ACCEPTED DOCUMENT-CONTROLLED BASELINE FOR THIS CLOSED CYCLE: Protocol 6.4
PROTOCOL 8 DETERMINISTIC-ORCHESTRATOR INHERITANCE OF 6.4: RECONCILED / REVISION 5
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

Protocol 6.4 was the accepted-current backward-compatible minor strengthening at this closed cycle boundary. Its immutable accepted release identity remains recovery `74bc572ef516cae417437a2027eeff52a2e25c15` with distinct public bootstrap `e09a9d1480211eea2d16d722182bb5c6de1bee12`. The repository default branch is not a protocol-version oracle, so no `main` merge is required to make that version-bound acceptance true; version-bound 6.3 and older work retains its immutable historical semantics.

## Protocol 6.6 completed handoff

Protocol 6.6 cognitive/operational optimization is complete. Its governing workplan is preserved as historical evidence at:

1. `workplans/archive/SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION.md`

Current disposition:

```text
P66 SEMANTIC CANDIDATE: 22f4bdba53795da3a6f13f162529f3a843fc37ae
INDEPENDENT REVIEW: PASS — 356d13f05ae56892dc1a75f1eae4c5d3d47881ee
STAKEHOLDER RATIFICATION: RATIFIED — 073aa74d0e786f8997d7a2885a67160000bd031c
PUBLIC FALLBACK: 22f4bdba53795da3a6f13f162529f3a843fc37ae
RECOVERY: 384666764da4c55b282e6b1595ab97e2f86e1dc4
RECOVERY MAPPING COMMIT: 777ae85ac5770ac67a2f85ad441e7b993babf65a
ACCEPTED-CURRENT CUTOVER: 8457fe9d3f30e7b21663f57645816cec8d0ef343
PROTOCOL 8 D3 REASSESSMENT INPUT: REVISION 7 / REQUIRED BEFORE D4
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

Protocol 6.6 is accepted-current. Its reduced-root-router, strict no-self-adoption version semantics, stochastic Protocol-6 robustness boundary, and bounded live trajectory evidence are inputs to Protocol 8's preserved deliberate D3 Orchestrator architecture reopen. They do not themselves select a Protocol 8 architecture or authorize Protocol 8 D4.

## SSDS 8.0 deterministic orchestration architecture future design handoff

The deterministic control-plane / mandatory-orchestrator line (Protocol 8.0) is now targeted as **SSDS 8.0**, the system-level successor to the document-controlled SSDP line. Its single current prospective handoff is:

- `workplans/active/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE.md`

The workplan ID keeps the historical `GRAPH-NATIVE` lexeme; the 2026-10-01 first-principles redesign replaced the graph-native hypothesis with an architecture of basis-stamped judgments over content-addressed units (ledger plus pure derivation, single Admission writer, optimistic concurrency, one intake route, refinement-based migration). That handoff supersedes, and its §18 dispositions every guarantee and capability of, these archived byte-identical records:

1. `workplans/archive/SSDS-8.0-GRAPH-NATIVE-DETERMINISTIC-ORCHESTRATION-ARCHITECTURE-BEFE678-HYPOTHESIS.md` (the `befe678` graph-native hypothesis)
2. `workplans/archive/SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED.md` (the consolidated Protocol 8 plan), which itself carried as one composition:
   1. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
   2. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
   3. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`
   4. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`
   5. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md`
   6. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION.md`
   7. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION.md`
   8. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT.md`
   9. `workplans/archive/SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md`

The consolidated plan's Revisions 1-2 closed ownership, semantic/control binding, storage/transport, cutover, determinism and recovery gaps; Revisions 3-7 advanced only inherited baseline identity (6.2 through 6.6), with Revision 7 binding Protocol 6.6 evidence as mandatory input to the deliberate D3 reassessment; the rebind reassigned the target from 7.0 to 8.0. Those historical inheritance dispositions remain true and are carried by the SSDS 8 handoff's §18.1 and §24. If the SSDS 8 handoff and an archived predecessor disagree about an inherited guarantee, the omission is a losslessness defect to repair in the handoff, not a narrowing.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
SSDS 8 ARCHITECTURE: PROPOSED (2026-10-01 first-principles redesign; not accepted-current)
SOURCE SNAPSHOT: f96b7ccf90dede4150d0efa17264fff07ec12d0d; DESIGN BASIS: befe6782e7c8fe038bf7cb764646d133ca167855
PROTOCOL 6.1 HISTORICAL COMPLETION/RECOVERY: SATISFIED
PROTOCOL 6.2 COMPLETION/QUALIFICATION/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.2 REPRESENTATION-INHERITANCE RECONCILIATION: SATISFIED
PROTOCOL 6.3 COMPLETION/QUALIFICATION/R2-REVIEW/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.3 INHERITANCE RECONCILIATION: SATISFIED
PROTOCOL 6.4 COMPLETION/REVIEW/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.4 INHERITANCE RECONCILIATION: SATISFIED
PROTOCOL 6.5 COMPLETION/REVIEW/RATIFICATION/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.5 INHERITANCE RECONCILIATION: SATISFIED
PROTOCOL 6.6 COMPLETION/REVIEW/RATIFICATION/RECOVERY PREREQUISITE: SATISFIED
PROTOCOL 6.6 INHERITANCE/REASSESSMENT INPUT: SATISFIED / SSDS 8 handoff §18.1, §24
CURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.6 recovery 384666764da4c55b282e6b1595ab97e2f86e1dc4
PROTOCOL 7 INHERITANCE: NOT FINAL — Protocol 7 closure is still active; prospective inputs only (handoff §19)
INDEPENDENT D3 REVIEW: READY for fresh independent falsification of the redesigned architecture;
  a PASS cannot authorize D4 before Protocol 7 reconsolidation (Phase A) and the SSDS 8 Architecture Manual (Phase C)
SSDS 8 D4: NOT AUTHORIZED
```

The Protocol 7 consolidated workplan's Stage H assigns its closeout the Protocol 8 inheritance reconciliation of the consolidated Protocol 8 plan. Because that plan is superseded, the obligation now applies to the SSDS 8 handoff (its §0, §19 and §24): advance the pre-cutover baseline to the Protocol 7 recovery and public fallback (kept distinct), bind Protocol 7 inputs to the SSDS 8 D3 reassessment, select no architecture, authorize no D4, and recommend, never self-adopt, a governing-version adoption.

SSDP 7.0 remains the active scientific inspectability/epistemic-initiative closure line and the latest manual/document-driven fallback. This SSDS 8 branch is intentionally isolated and implies no cutover, merge to `main`, or implementation authorization.

## Protocol 6.5 completed handoff

Protocol 6.5 self-governance, release-state, evidence-binding, representation, and proportional-rigor work is complete. The governing workplans are preserved as historical evidence at:

1. `workplans/archive/SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md`
2. `workplans/archive/SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md`
3. `workplans/archive/SSDP-6.5-IMPORTANCE-WEIGHTED-ATTENTION-AND-PROPORTIONAL-RIGOR.md`

Current disposition:

```text
P21 SEMANTIC CANDIDATE: 7f7b5e24858e813e45ace867a7f8ea5180f43bf0
INDEPENDENT REVIEW: PASS — 29077c564140d3902ac1764d8eb8acd0b9a6be2c
STAKEHOLDER RATIFICATION: RATIFIED — 95f106558c0c046eb46bc1239cb511231c5cce07
PUBLIC FALLBACK: 7f7b5e24858e813e45ace867a7f8ea5180f43bf0
RECOVERY: c4d5da1e0acb0e9f27376bf69561e8762747cd2d
RECOVERY MAPPING COMMIT: 56381b89eb10d473fb6b1ef30c7c4ad14e825954
ACCEPTED-CURRENT CUTOVER: 2b8ce17b1f086dc85e6fa8014c4a7bcc45ef60cb
PROTOCOL 8 DETERMINISTIC-ORCHESTRATOR INHERITANCE OF 6.5: RECONCILED / REVISION 6
LIFECYCLE STATUS: COMPLETED / ARCHIVED
```

Protocol 6.5 was accepted-current at its closed cycle boundary. Mutable current release identity remains owned only by `PROTOCOL-RELEASE-STATE.yaml`; the exact immutable 6.5 public fallback and recovery remain distinct. Protocol 6.4 is preserved as historical rollback, and the Protocol 8 deterministic-orchestrator D3 architecture/D4 authorization remain unchanged.

## Version/cutover rule

There is exactly one mutable repository release-state owner: `PROTOCOL-RELEASE-STATE.yaml`.

- Repository default/latest is never a protocol-version oracle.
- Protocol 6.6 is accepted-current with exact public fallback `22f4bdba53795da3a6f13f162529f3a843fc37ae` and recovery `384666764da4c55b282e6b1595ab97e2f86e1dc4`.
- Protocol 7 is the proposed scientific inspectability/epistemic-initiative/feedback-loop revision governed by its single consolidated workplan above; select its artifacts by exact ID, never by `SSDP-7.0*` globs, because the historical deterministic-orchestrator family shares that prefix.
- SSDS 8.0 is the proposed deterministic orchestration successor through its single prospective architectural workplan. It is currently based on the active Protocol 7 branch snapshot and MUST be re-consolidated against final accepted Protocol 7 inheritance before D4; it does not authorize implementation or cutover. Select its artifacts by exact ID.
- Under future SSDS 8 per-unit native cutover, a single Admission writer would serialize canonical state into an append-only ledger and all lifecycle state would be derived; authority documents and change plans remain semantic artifacts, D4 code remains executable authority, and agents/humans retain semantic judgment according to their owning gates.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- No `main` merge or Protocol 7/8 D4 cutover is authorized merely by these active design workplans.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0/6.1/6.2/6.3 records merely to adopt later terminology or presentation rules. Current successor work must preserve historical capability while expressing current doctrine directly and compactly; detailed history remains recoverable without becoming parallel current authority.
