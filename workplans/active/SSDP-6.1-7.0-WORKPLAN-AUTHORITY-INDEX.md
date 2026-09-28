---
kind: protocol-workplan-authority-index
workplan_id: SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX
protocol_version: 6.6.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-28
active_serious_challenge: none
---

# SSDP 6.1 / 6.2 / 6.3 / 6.4 / 6.5 / 6.6 / 7.0 / 8.0 Workplan Authority Index

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

The author-side review record `qualification/ssdp70/WORKPLAN-REVIEW-2026-09-27-PROTOCOL-7.0-PASS.md` applies only to the superseded composition, was not independent, and establishes no implementation-handoff readiness. The consolidated handoff's §0 routes prior NO-PASS records and the unchanged stakeholder SC1/SC2 decisions. Its latest independent Review, at `1b21b1744cb74eaeefbff732d8f7d48f0a815dda`, returned **NO-PASS**: `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-1B21B17-NO-PASS.md` (the preceding `3b12a83` record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-3B12A83-NO-PASS.md`, the `5cfaca7` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-5CFACA7-NO-PASS.md`, the `31845d8` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-31845D8-NO-PASS.md`, the `cb9542d` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-CB9542D-NO-PASS.md`, the `179c7e0` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-179C7E0-NO-PASS.md`, the `4e778e2` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-4E778E2-NO-PASS.md`, the `adaac7b` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-ADAAC7B-NO-PASS.md`, the `41434b1` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-41434B1-NO-PASS.md` and the `67fb29d` record `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-67FB29D-NO-PASS.md`; the `677a7a82` NO-PASS left no durable record). Proposed repairs are in that same handoff (§0.1–§0.2). Stakeholder decision SD-B (2026-09-27) superseded the 6.6 per-route burden cap with a compression target subordinate to lossless required elements: `qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SD-B.md`. The earlier `27fb2bd` Review (`qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-27FB2BD-NO-PASS.md`) found SD-B's premise inaccurate (6.6's cap was relative to 6.5). The stakeholder confirmed SD-B with the corrected premise and retained 6.6's fixed-cost condition as a backstop and escalation trigger: `qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SD-B-CONFIRMATION.md`. The repairing context also performed this latest Review, so fresh independent acceptance must come from a context that authored neither the workplan nor these repairs.

```text
PROTOCOL 7 WORKPLAN DESIGN REVIEW: NO-PASS (latest 1b21b17); proposed repair pending fresh independent review
PROTOCOL 7 SD-B: SUPERSEDE (2026-09-27); size budget is a compression target, never a reason to break a lossless condition;
  CONFIRMED with corrected premise; backstop median <= 1.10 x accepted 6.5 median on T1/T7/T8 (escalation trigger);
  the recorded D4 probe (10,415 B) and the 67fb29d reviewer's probe (11,121 B; measurement recorded, text not, so unreproducible) exceed the
  9,196 B backstop but predate the current wording, so a stakeholder escalation before Stage B is strongly expected
STAKEHOLDER DECISIONS: section 4 rule ACCEPTED; SC1 claim-integrity floor ACCEPTED; SC2 Option B SELECTED (2026-09-27)
PROTOCOL 7 D4: NOT AUTHORIZED
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

## Protocol 8.0 deterministic-orchestrator future design handoff

Protocol 8.0 deterministic-orchestrator design/review SHALL use the single current consolidated handoff:

- `workplans/active/SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED.md`

It supersedes, as one composition, these archived byte-identical design and review records (its §37.4 maps each to the sections now carrying it):

1. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md`
2. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE.md`
3. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md`
4. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md`
5. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md`
6. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION.md`
7. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION.md`
8. `workplans/archive/SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT.md`
9. `workplans/archive/SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md`

The consolidation is a representation and version-label change only. Revisions 1-2 closed ownership, semantic/control binding, storage/transport, cutover, determinism and recovery gaps; Revisions 3-7 advanced only inherited baseline identity (6.2 through 6.6), with Revision 7 binding Protocol 6.6 evidence as mandatory input to the deliberate D3 reassessment; the rebind reassigned the target from 7.0 to 8.0. If the consolidated file and the composed archived family disagree materially, the composed family governs until the consolidation is repaired.

Current disposition:

```text
SERIOUS CHALLENGE: NONE
WORKPLAN DESIGN REVIEW: PASS HISTORY (parent + Revisions 1-2, second review under 6.1; dispositions recorded in the archived revisions)
CONSOLIDATION: PENDING INDEPENDENT LOSSLESSNESS CHECK AGAINST THE ARCHIVED FAMILY
IMPLEMENTATION STATUS: PROPOSED
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
PROTOCOL 6.6 INHERITANCE/REASSESSMENT INPUT: SATISFIED / CONSOLIDATED §3.2, §28.1
CURRENT PRE-CUTOVER FALLBACK/ROLLBACK BASELINE: Protocol 6.6 recovery 384666764da4c55b282e6b1595ab97e2f86e1dc4
REMAINING PROTOCOL-8-SPECIFIC PRE-D4 REQUIREMENT:
  1. DELIBERATE D3 ORCHESTRATOR ARCHITECTURE REOPEN/SUPERSESSION
PROTOCOL 8 D4: NOT AUTHORIZED
```

Protocol 8 D4 remains unauthorized until the deliberate D3 Orchestrator architecture reopen/supersession closes. No Protocol 8 cutover is implied.

If Protocol 7 is accepted, its closeout SHALL author a Protocol 8 inheritance reconciliation of the consolidated workplan that advances the pre-cutover baseline to Protocol 7 recovery and binds Protocol 7 inputs to the Protocol 8 D3 reassessment. Known Protocol 7 inputs are recorded in the consolidated workplan's §37.2.

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
- The deterministic-orchestrator proposal targets Protocol 8.0 through its single consolidated workplan; that workplan binds Protocol 6.6 recovery as the inherited pre-cutover baseline and does not authorize D4. Select its artifacts by exact ID as well.
- Under the future Protocol 8 deterministic-orchestrator proposal, after its own qualified cutover, the deterministic control plane would own machine lifecycle transitions while workplans/skills/documents remain semantic artifacts.
- Shadow comparison is permitted only while one side remains explicitly non-authoritative.
- No `main` merge or Protocol 7/8 D4 cutover is authorized merely by these active design workplans.

## Historical discipline

Do not edit archived/version-pinned Protocol 5.x/6.0/6.1/6.2/6.3 records merely to adopt later terminology or presentation rules. Current successor work must preserve historical capability while expressing current doctrine directly and compactly; detailed history remains recoverable without becoming parallel current authority.
