---
kind: protocol-minor-revision-workplan
workplan_id: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
protocol_version: 6.0.0
target_protocol_version: 6.1.0
status: active
created_date: 2026-09-09
base_protocol: Protocol 6.0
active_serious_challenge: none
---

# SSDP 6.1 Evidence, Evolution, and Concretization Alignment

## 1. Objective and version boundary

Protocol 6.1 is the final **document-controlled** SSDP release before the Protocol 7 orchestrator-control-plane transition. It strengthens the dynamic scientific-development model, evidence validity, dependency tracing, historical reasoning, and terminology while preserving the complete Protocol 6 workflow and all still-valid inherited Protocol 5.16 guarantees.

Protocol 6.1 remains backward-compatible in control architecture:

```text
human/agent activation prompt
 -> version-bound Protocol skill/profile resolution
 -> workplan/change-plan and current D1-D4 authority
 -> agent reasoning and repository work
 -> evidence/review
 -> manual/semi-automatic lifecycle update
```

Workplans, current domain authorities, skills, prompts, and existing Orchestrator Core/Profile behavior remain sufficient to execute Protocol 6.1. No JSON control plane, mandatory orchestrator reducer, machine-authoritative dependency graph, event store, or Task/Result envelope is required for Protocol 6.1 execution.

After acceptance, preserve Protocol 6.1 as an immutable pre-automation recovery snapshot. Protocol 7 development must not retroactively alter that snapshot or make its operation depend on Protocol 7 infrastructure.

## 2. Governing inherited authority — lossless preservation is mandatory

This workplan refines Protocol 6.0; it does not reopen or weaken its accepted parent doctrine absent a genuine Serious Challenge.

Implementation MUST preserve all still-valid Protocol 6.0 and inherited Protocol 5.16 behavior, including at minimum:

- recursive domain authority across D1 scientific formulation, D2 algorithm/numerical method, D3 architecture, and D4 specification/implementation;
- authority-source/abstraction-level orthogonality and simultaneous governed side constraints;
- fidelity as feasibility, then domain fitness, minimum justified complexity, and development economy;
- delegated lower-level freedom and explicit promotion of durable invariants only by the owning authority;
- snapshot-complete handoff and version-bound workplans;
- reduced D4-only, D3->D4, D2->D4, and D1->downstream paths when semantically justified;
- reverse semantic verification, abstraction adequacy, bounded Challenge Pass, Serious Challenge routing, and human ratification/risk-override semantics;
- proxy-proof acceptance and real-semantic-owner evidence;
- focused/stage-local/final affected regression, integration, repository checks, and production-qualification separation;
- evidence reuse with bounded invalidation;
- active simplicity, recurrence-driven shared-owner reasoning, convergence/revision economy, and no patch-on-patch preservation of delegated machinery;
- language/tool routing, long-horizon quality sensing, optional Verification/Stabilization/Audit/support-specialist boundaries;
- immutable historical protocol recovery and current-versus-historical authority separation;
- adversarial behavioral qualification of Protocol behavior rather than wording-only conformance.

Compression, consolidation, renaming, or structural refactoring is permitted only when these capabilities remain semantically recoverable. A shorter formulation that deletes a protection is a defect.

## 3. Terminology migration: abstraction/concretization and evidence realization

Protocol 6.0 uses `abstraction <-> realization` for semantic descent and also uses realization language around executed evidence. Protocol 6.1 SHALL remove this collision for current 6.1 authority.

Current Protocol 6.1 terminology:

```text
ABSTRACTION  --design / constrain-->  CONCRETIZATION
ABSTRACTION  <--verify / reconstruct-- CONCRETIZATION
```

A concretization is a lower-level scientific, numerical, architectural, specification, or implementation choice that satisfies applicable parent abstractions and governed side constraints. An interior D1-D4 artifact may be a concretization of its parent while serving as an abstraction for its descendants.

Reserve `realization` for evidence instantiation:

```text
EVIDENCE SPECIFICATION
 -> EVIDENCE REALIZATION
 -> OBSERVATION
 -> EVIDENCE ASSESSMENT
```

Definitions:

- **evidence specification** — reusable definition of a test, experiment, benchmark, proof procedure, static check, validation procedure, or other evidence-generating instrument;
- **evidence realization** — one concrete execution/instantiation of that specification under identified subject revision, inputs/regime, environment, and applicable assumptions;
- **observation** — result produced by that realization;
- **evidence assessment** — interpretation of whether the observation supports, contradicts, challenges, or is inconclusive for a governed claim.

### 3.1 Historical compatibility rule

Do NOT rewrite immutable Protocol 6.0/5.x archive records merely to replace vocabulary. Historical artifacts retain the terminology of the protocol version that governed them.

Current Protocol 6.1 canonical source, generated packages, current prompts/templates/guides, and current-facing documentation SHALL use the new vocabulary coherently. Where readers may encounter historical material, add a concise compatibility mapping rather than maintaining two current vocabularies.

A version-bound 6.0 workplan continues to mean 6.0 semantics. Terminology migration does not silently change the governing version of historical or still-bound work.

## 4. Dynamic scientific-development doctrine

Protocol 6.0 describes a correct authority/concretization structure and bounded invalidation. Protocol 6.1 SHALL make the system's temporal dynamics explicit:

```text
observation/context
 -> model or authority proposal
 -> accepted abstraction
 -> downstream concretization
 -> prediction/behavior
 -> evidence realization
 -> observation
 -> assessment/challenge
 -> authority or concretization revision when justified
 -> bounded dependency impact
 -> reconcretization/revalidation
```

Scientific/software development is therefore an iterative model-evidence process, not a one-way production pipeline.

A contradiction observed at D4 does not establish that D4 is the faulty owner. Investigation must distinguish among:

- D4 concretization nonconformance;
- D3 abstraction inadequacy or architectural defect;
- D2 algorithm/numerical inadequacy;
- D1 scientific/model/context inadequacy;
- contradictory simultaneous authority;
- invalid evidence specification/oracle;
- invalid or inapplicable evidence realization;
- incorrect interpretation of an observation.

Route the challenge to the earliest materially affected owner. Do not repair downstream code or tests around an upstream defect.

## 5. Authority–Evidence–Evolution model

Protocol 6.1 SHALL explicitly maintain three orthogonal concerns without creating a new authority domain:

1. **Authority/concretization structure** — what is currently supposed to be true and how accepted abstractions are concretized downstream.
2. **Evidence structure** — what evidence specifications/realizations/observations bear on which governed claims and under what assumptions/regimes.
3. **Evolution history** — how and why authorities, concretizations, evidence expectations, and delegated mechanisms changed over time.

Evidence is not D5 and does not become semantic truth by packaging. Tests, experiments, proofs, benchmarks, and runtime observations remain instruments used to challenge or support D1-D4/external claims.

## 6. Typed semantic dependency documentation

Protocol 6.1 SHALL strengthen the current bounded-dependency doctrine by introducing maintained **Markdown semantic dependency records** where material complexity or change frequency makes implicit links insufficient.

These records SHALL remain lightweight, human/agent-readable semantic artifacts. They are not a machine-authoritative graph database and must not duplicate ordinary source-code dependency graphs.

Relationships may include, as applicable:

- `CONCRETIZES`;
- `DERIVED_FROM`;
- `DEPENDS_ON`;
- `ASSUMES`;
- `CONSTRAINED_BY`;
- `SUPERSEDES` / `REPLACES`;
- `CHALLENGES` / `CONTRADICTS`;
- `EVIDENCES`;
- `GENERATED_BY`.

The record should use stable logical identifiers where that materially improves continuity, but Protocol 6.1 SHALL NOT require a universal claim registry, per-line graph, global database, or identity machinery disproportionate to the project.

Existing section anchors, document links, workplan mappings, profile metadata, and repository paths remain valid lower-cost representations when they are sufficient.

## 7. Evidence target versus execution dependency

Protocol 6.1 SHALL explicitly distinguish two relationships that must not be conflated:

### 7.1 Evidentiary target

The proposition/invariant the evidence specification is intended to evaluate.

### 7.2 Execution dependency

The concrete implementation, harness, fixture, dataset, environment, tool, or other machinery needed to realize the evidence.

A test may evidence a D1/D2 invariant while executing through a D4 concretization. Replacing that D4 concretization can therefore produce different consequences:

- the evidence specification remains valid and is simply rerun against the new concretization;
- the specification remains semantically valid but its harness mapping requires revision;
- the oracle/assumption is concretization-specific and becomes stale;
- a prior evidence realization becomes inapplicable to the new subject revision even though the specification remains durable.

Invalidation must follow the actual typed dependency, not file proximity or generic transitive coupling.

## 8. Evidence lifecycle and admissibility

Protocol 6.1 SHALL distinguish enough evidence states to prevent false closure. Exact metadata syntax remains repository-local, but semantics must cover at least:

- pending/unrealized;
- admissible/valid for the current claim and regime;
- review-required;
- inconclusive;
- challenged;
- stale/inapplicable;
- rejected/invalid;
- retired/historical.

Core rule:

> A valid failing observation is evidence. A stale failing observation is not admissible evidence against current authority. A stale passing observation is not admissible confirmation of current authority.

A PASS/accepted/closed claim may not depend on stale, rejected, unavailable-required, or otherwise inadmissible evidence.

Evidence validity has a domain: subject revision, governing claim, assumptions, input/regime, environment, oracle semantics, and relevant protocol obligation. Preserve reusable evidence when none of these materially changed.

## 9. Test/evidence durability

When equivalent evidentiary strength is available, prefer specifications coupled to durable governed invariants over replaceable concretization details.

Typical preference:

```text
scientific/mathematical invariant evidence
 > algorithm/numerical property evidence
 > behavioral/architectural contract evidence
 > concretization-specific evidence
```

This is not a prohibition on low-level tests. Concretization-specific evidence remains appropriate for fault localization, memory/lifetime safety, explicit public interfaces, persistence/serialization, numerical corner cases, performance regressions, historically recurring defects, implementation-specific failure behavior, and similar D4 claims.

Governing principle:

> Maximize evidentiary authority and durability while minimizing unnecessary coupling to replaceable concretizations.

Do not weaken a stronger real-owner oracle merely to make a test more durable.

## 10. Bounded change-impact and stale-artifact propagation

When accepted authority or a material concretization changes:

```text
identify typed materially dependent descendants/evidence
 -> preserve unaffected siblings and still-valid evidence
 -> mark only affected items review-required/stale
 -> reconcretize or remap as needed
 -> realize required evidence again
 -> verify upward across the affected surface
```

A changed parent creates a review obligation over materially dependent descendants; it does not automatically prove every descendant wrong.

A changed delegated owner does not freeze the old owner merely because historical evidence exercised it. Reconcile evidence to the new real semantic owner.

This doctrine SHALL integrate with workplan affected-surface derivation, Review, Closeout, repository hygiene, and version migration.

## 11. Historical semantic evolution record

Protocol 6.1 SHALL introduce/standardize a maintained Markdown historical record for material semantic evolution that ordinary Git diffs cannot explain adequately.

Record only decisions whose rationale is likely to matter to future scientific/engineering reasoning, such as:

- authority/model replacement or generalization;
- algorithm rejection or supersession;
- architecture supersession;
- retirement of delegated machinery after recurrence/complexity evidence;
- invalidated assumptions or validity regimes;
- evidence that triggered upstream reconsideration;
- evidence specifications retired because their governed proposition/oracle became obsolete;
- previously attempted and rejected approaches when recurrence is plausible;
- restoration of an older approach and the new evidence that justified it.

Each material entry should identify, where applicable:

- affected logical authority/concretization/evidence specification;
- previous and replacement semantics;
- triggering observation/evidence/challenge;
- relevant validity regime/assumptions;
- rationale and owning-domain disposition;
- affected descendants/evidence;
- references to current authority/workplans/reports/commits.

Do not duplicate full debate transcripts or turn history into a second current authority. Current normative documents continue to describe the accepted present system coherently; chronology belongs in the historical record.

## 12. Repository hygiene and stale evidence

Extend existing cleanup doctrine:

- obsolete concretizations, tests, guides, and compatibility machinery must not remain active merely because they once carried evidence or were historically important;
- historical value is preserved through Git/version-pinned artifacts and concise semantic evolution records;
- current active surfaces should not present superseded tests or implementations as competing apparent authority;
- removal remains conservative: retain an artifact when a current supported compatibility, forensic, qualification, or explicit historical role still requires it.

Stale passing tests are particularly dangerous because they can fabricate confidence. Review/cleanup must treat them as authority-confusion risk, not harmless excess coverage.

## 13. Workplan and workflow integration — document control remains authoritative in 6.1

Workplans remain bounded implementation/change contracts and remain the controlling task artifacts when materially warranted.

Workplans and reviews SHALL, proportionately to risk/scope, identify:

- materially affected authority/concretization relationships;
- evidence specifications and prior realizations likely to be invalidated;
- required new/repeated evidence;
- historical-record updates triggered by a material semantic supersession;
- genuine reopen triggers and unavailable-required evidence.

Do not require a workplan for every local D4 repair solely to populate dependency/history records. Existing proportionality rules remain binding.

The canonical human-facing Protocol 6 workflow prompt/profile remains active in 6.1. Installed-compatible-first/public-source-fallback resolution remains supported. Manual web copy/paste operation remains first-class.

## 14. Skill/reference/template migration

Update current 6.1 canonical source losslessly:

- protocol-wide abstraction/concretization/evidence terminology;
- D1-D4 role skills and required references;
- workflow/workplan guidance;
- testing/validation guidance;
- documentation/evidence and documentation-maintenance guidance;
- architecture/design and D4 specification guidance where terminology or evidence dependencies appear;
- workplan/change-plan templates;
- canonical workflow prompts/profile text;
- Protocol versioning/compatibility documentation;
- README/source navigation and generated skill packages where derived from canonical source.

Preserve source-chain discipline: edit canonical `source/` owners and regenerate committed derivatives. Do not independently patch generated `dist/` copies.

Do not mechanically rename the word `realization` where it refers to historical Protocol 6.0 terminology, ordinary English, or evidence realization. Perform semantic reconciliation.

## 15. Orchestrator compatibility in 6.1

The existing orchestrator architecture/profile remains non-mandatory infrastructure under 6.1. Update only what is necessary for 6.1 protocol/profile compatibility and terminology.

Protocol 6.1 SHALL NOT silently adopt Protocol 7 workflow authority.

In particular, do not introduce under 6.1:

- orchestrator-only canonical lifecycle state;
- mandatory TaskEnvelope/ResultEnvelope exchange;
- an orchestrator-owned deterministic reducer as the sole workflow authority;
- a machine-authoritative dependency/evidence graph;
- mandatory remote polling/web-agent transport;
- removal of manual first-class operation;
- removal of lifecycle/control responsibilities that current skills/prompts/workplans still need.

## 16. Protocol 6.1 recovery snapshot

After complete acceptance and behavioral qualification, create an immutable release/tag/commit mapping for Protocol 6.1 analogous to existing historical recovery practice.

The snapshot must be sufficient to restore the semi-automated system without Protocol 7 components:

- current 6.1 canonical skills/references/templates/prompts;
- compatible Protocol profile/snapshot;
- workplan-guided manual/semi-automatic workflow;
- Markdown dependency/evolution records and procedures;
- required package/build/parity artifacts.

Document the immutable identity in protocol versioning/portability guidance. Do not maintain two live canonical branches after Protocol 7 cutover merely for fallback; fallback uses the pinned 6.1 release.

## 17. Implementation sequence

1. Reconstruct and freeze the complete inherited 6.0 capability set relevant to this change.
2. Reconcile terminology and version-compatibility rules before broad edits.
3. Refactor the canonical authority/challenge reference around abstraction/concretization without losing its existing feasibility, authority, challenge, human-gate, and bounded-invalidation doctrine.
4. Add dynamic evidence/evolution doctrine to the minimum set of canonical owners; avoid duplicated prose.
5. Define the Markdown semantic dependency and historical evolution artifacts/templates or conventions at the appropriate canonical owner.
6. Reconcile role skills, workflow prompts, templates, documentation/testing/architecture references, and profile wording.
7. Regenerate all derived skill packages/snapshots.
8. Run static/source/package/profile/orchestrator acceptance.
9. Run behavioral qualification that exercises terminology-independent governed decisions plus new evidence/evolution cases.
10. Perform independent final Review and bounded Challenge Pass.
11. Set `source/PROTOCOL_VERSION` to `6.1.0` only as part of the coherent accepted candidate, update compatibility/portability mappings, and preserve the immutable 6.1 recovery identity at closeout.

## 18. Required adversarial qualification additions

Extend Protocol behavioral qualification with bounded scenarios demonstrating at least:

- old 6.0 version-bound work is not reinterpreted under 6.1 vocabulary;
- a stale passing test cannot close a current claim;
- replacement of a delegated D4 concretization does not automatically invalidate a durable invariant-level evidence specification;
- a concretization-specific oracle is marked stale/remapped when its owner is superseded;
- an upstream authority change invalidates only material dependent descendants/evidence;
- a D4 observation can route a Serious Challenge to D1/D2/D3 rather than forcing local repair;
- evidence/specification/oracle error is considered as an alternative explanation for contradiction;
- historical reasoning is preserved without making history a second current authority;
- Markdown dependency records remain proportionate and do not force a universal registry/database;
- workplan/prompt/manual operation remains sufficient without Protocol 7 machinery.

Behavioral meaning, not exact wording, is the oracle.

## 19. Acceptance criteria

Protocol 6.1 is PASS only when all of the following hold on one coherent semantic candidate:

1. current 6.1 authority consistently uses abstraction/concretization and evidence specification/realization/observation terminology;
2. historical/version-pinned 6.0 and 5.x truth remains intact and recoverable;
3. every still-valid Protocol 6.0/5.16 safeguard remains semantically recoverable;
4. evidence is explicitly first-class support/challenge material without becoming D5 or parallel truth authority;
5. evidence target and execution dependency are distinguished;
6. evidence validity/admissibility and stale passing/failing semantics are explicit;
7. durable-test preference preserves proxy-proof/real-owner strength rather than weakening it;
8. typed semantic dependency tracing and bounded invalidation are documented without a mandatory machine graph/database;
9. a concise semantic evolution-history mechanism exists and is integrated with authority/workplan/review/cleanup practice;
10. current normative documents remain present-state owners rather than append-only histories;
11. current skills/prompts/workplans retain the full document-controlled Protocol 6.1 execution contract;
12. existing local/manual/web activation behavior remains usable without Protocol 7;
13. canonical-source/generated-source/profile/version compatibility is coherent;
14. repository tests, package validation/parity, Protocol profile/snapshot checks, applicable Orchestrator Core acceptance, and required behavioral qualification execute and pass;
15. independent final Review finds no blocker and no active Serious Challenge;
16. an immutable, documented Protocol 6.1 pre-automation recovery identity is established at closeout.

## 20. Explicit non-goals

- Do not build the Protocol 7 control plane in this workplan.
- Do not make the orchestrator mandatory.
- Do not replace semantic Markdown documents with JSON.
- Do not introduce a graph database merely because semantic dependencies form a graph.
- Do not rewrite historical Protocol 6.0/5.x artifacts to current vocabulary.
- Do not create a fifth authority-bearing evidence role.
- Do not weaken existing real-owner/proxy-proof evidence to increase test durability.
- Do not require universal dependency/history records for trivial/local work.
- Do not treat Git chronology alone as sufficient semantic rationale for material supersession.
- Do not release 6.1 with an unresolved governing Serious Challenge or missing required behavioral qualification.

## 21. Final intended disposition

When accepted, Protocol 6.1 becomes:

> **the final stable semi-automated, document-controlled SSDP release and the immutable recovery baseline for Protocol 7 development.**

Protocol 7 may supersede its workflow-control mechanism, but must preserve its semantic authority, evidence, evolution, challenge, engineering-quality, and historical-recovery doctrine unless a deliberate higher-authority revision explicitly replaces a rule with a stronger one.
