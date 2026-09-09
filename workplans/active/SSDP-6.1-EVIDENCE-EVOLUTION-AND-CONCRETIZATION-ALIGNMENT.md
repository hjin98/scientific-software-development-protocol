---
kind: protocol-minor-revision-workplan
workplan_id: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
protocol_version: 6.0.0
target_protocol_version: 6.1.0
status: active
created_date: 2026-09-09
reviewed_date: 2026-09-09
design_review: pass
review_rounds: 3
ready_for_implementation: true
base_protocol: Protocol 6.0
base_protocol_commit: 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
active_serious_challenge: none
---

# SSDP 6.1 Evidence, Evolution, and Concretization Alignment

## 1. Objective and version boundary

Protocol 6.1 is the final **document-controlled** SSDP release before the Protocol 7 orchestrator-control-plane transition. It strengthens the dynamic scientific-development model, evidence validity, dependency tracing, historical reasoning, and terminology while preserving the complete Protocol 6 workflow and every still-valid inherited Protocol 5.16 safeguard.

Protocol 6.1 remains backward-compatible in control architecture:

```text
human/agent activation prompt
 -> version-bound Protocol skill/profile resolution
 -> workplan/change-plan and current D1-D4 authority
 -> agent reasoning and repository work
 -> evidence/review
 -> manual/semi-automatic lifecycle update
```

Workplans, current domain authorities, skills, prompts, and the compatible Orchestrator Core/Profile remain sufficient to execute Protocol 6.1. No JSON control plane, mandatory orchestrator reducer, machine-authoritative dependency graph, event store, or Task/Result envelope is required for Protocol 6.1 execution.

After acceptance, preserve Protocol 6.1 as an immutable pre-automation recovery snapshot. Protocol 7 development must not retroactively alter that snapshot or make its operation depend on Protocol 7 infrastructure.

## 2. Governing inherited authority — lossless preservation is mandatory

This workplan refines Protocol 6.0; it does not reopen or weaken its accepted parent doctrine absent a genuine Serious Challenge.

Implementation MUST preserve all still-valid Protocol 6.0 and inherited Protocol 5.16 behavior, including at minimum:

- recursive D1 scientific formulation, D2 algorithm/numerical method, D3 architecture, and D4 specification/implementation authority;
- authority-source/semantic-level orthogonality and simultaneous governed side constraints;
- fidelity as feasibility, then domain fitness, minimum justified complexity, and development economy;
- delegated lower-level freedom and explicit promotion of durable invariants only by the owning authority;
- snapshot-complete handoff and version-bound workplans;
- reduced D4-only, D3->D4, D2->D4, and D1->downstream paths when semantically justified;
- reverse semantic verification, child-abstraction adequacy, bounded Challenge Pass, Serious Challenge routing, and human ratification/risk-override semantics;
- proxy-proof acceptance and real-semantic-owner evidence;
- focused/stage-local/final affected regression, integration, repository checks, and production-qualification separation;
- evidence reuse with bounded invalidation;
- active simplicity, recurrence-driven shared-owner reasoning, convergence/revision economy, and no patch-on-patch preservation of delegated machinery;
- language/tool routing, long-horizon quality sensing, optional Verification/Stabilization/Audit/support-specialist boundaries;
- compact resumable working state where needed without creating parallel authority;
- immutable historical protocol recovery and current-versus-historical authority separation;
- adversarial behavioral qualification of Protocol behavior rather than wording-only conformance;
- semantic-candidate versus later evidence/lifecycle-commit distinction when qualification evidence itself must be committed after the candidate it describes.

Compression, consolidation, renaming, or structural refactoring is permitted only when these capabilities remain semantically recoverable. A shorter formulation that deletes a protection is a defect.

## 3. Terminology migration: abstraction/concretization and evidence realization

Protocol 6.0 uses `abstraction <-> realization` for semantic descent while evidence discussion also uses realization-like language for concrete executions. Protocol 6.1 SHALL remove this collision for current 6.1 authority.

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

- **evidence specification** — reusable definition of a test, experiment, benchmark, proof/check procedure, validation procedure, or other evidence-generating instrument;
- **evidence realization** — one concrete execution/instantiation of that specification under identified subject revision, inputs/regime, environment, and applicable assumptions;
- **observation** — result produced by that realization;
- **evidence assessment** — interpretation of one or more observations with respect to a governed claim, including support, contradiction/challenge, or inconclusive result.

### 3.1 Historical compatibility and opaque legacy identifiers

Do NOT rewrite immutable Protocol 6.0/5.x archive records merely to replace vocabulary. Historical artifacts retain the terminology of the protocol version that governed them.

A protocol-stable identifier/path created under an earlier version MAY retain a legacy `realization` lexeme when renaming would create unnecessary compatibility breakage, link churn, package/profile incompatibility, or historical ambiguity. Examples include existing filenames, workplan IDs, serialized identifiers, or public API tokens.

Such retained text is an **opaque compatibility identifier**, not current 6.1 semantic vocabulary. Current prose, new identifiers, headings, and normative explanations SHALL use `concretization` for semantic descent and `evidence realization` for evidence instantiation. Where a retained identifier could confuse a reader, provide one concise compatibility mapping at the owning current reference rather than maintaining two competing vocabularies.

A version-bound 6.0 workplan continues to mean Protocol 6.0. Terminology migration does not silently change the governing version of historical or still-bound work.

## 4. Dynamic scientific-development doctrine

Protocol 6.1 SHALL make temporal development dynamics explicit:

```text
observation/context
 -> model or authority proposal
 -> accepted abstraction
 -> downstream concretization
 -> prediction/behavior
 -> evidence realization
 -> observation
 -> evidence assessment/challenge
 -> authority or concretization revision when justified
 -> bounded dependency impact
 -> reconcretization/revalidation
```

Scientific/software development is an iterative model-evidence process, not a one-way production pipeline. Models, algorithms, architectures, and implementations remain subject to evidence-backed challenge when edge cases, new regimes, contradictions, or a more general adequate abstraction expose under-generalization or inadequacy.

A contradiction observed at D4 does not establish that D4 is the faulty owner. Investigation must distinguish among:

- D4 concretization nonconformance;
- D3 abstraction inadequacy or architectural defect;
- D2 algorithm/numerical inadequacy;
- D1 scientific/model/context inadequacy;
- contradictory simultaneous authority;
- invalid evidence specification/oracle;
- invalid or inapplicable evidence realization;
- incorrect interpretation of an observation.

Route challenge to the earliest materially affected owner. Do not repair downstream code or tests around an upstream defect.

## 5. Authority–Evidence–Evolution model

Protocol 6.1 SHALL explicitly maintain three orthogonal concerns without creating a new authority domain:

1. **Authority/concretization structure** — what is currently supposed to be true and how accepted abstractions are concretized downstream.
2. **Evidence structure** — what evidence specifications, realizations, observations, and assessments bear on which governed claims and under what assumptions/regimes.
3. **Evolution history** — how and why authorities, concretizations, evidence expectations, and delegated mechanisms changed over time.

Evidence is not D5 and does not become semantic truth by packaging. Tests, experiments, proofs, benchmarks, literature, and runtime observations remain instruments used to challenge or support D1-D4/external claims.

Central doctrine:

> Evidence has a validity domain and a dependency structure just as models do. Evidence must therefore evolve under explicit applicability and supersession rules; passing obsolete evidence must never be mistaken for confirmation of current authority.

## 6. Typed semantic dependency documentation

Protocol 6.1 SHALL strengthen bounded-dependency tracing by permitting maintained **Markdown semantic dependency records** where material complexity or change frequency makes implicit links insufficient.

These records SHALL remain lightweight, human/agent-readable semantic artifacts. They are not a machine-authoritative graph database and must not duplicate ordinary source-code dependency graphs.

### 6.1 Relationship semantics and direction

When a typed relationship is recorded, use consistent direction:

- `CONCRETIZES`: child/concretization -> governing parent abstraction;
- `DERIVED_FROM`: subject -> semantic/source basis;
- `DEPENDS_ON`: subject -> material semantic dependency when no more specific relation fits;
- `ASSUMES`: subject -> governing assumption;
- `CONSTRAINED_BY`: subject -> external/domain constraint;
- `SUPERSEDES` / `REPLACES`: new/current item -> old/superseded item;
- `CHALLENGES` / `CONTRADICTS`: observation/assessment/finding/authority -> challenged target;
- `EVIDENCES`: evidence specification -> intended governed claim;
- `EXECUTION_DEPENDS_ON`: evidence specification or realization -> machinery/data/environment needed to execute or interpret it;
- `INSTANTIATES`: evidence realization -> evidence specification;
- `GENERATED_BY`: observation -> evidence realization.

Use `DEPENDS_ON` only for a genuinely material semantic dependency; do not use it as a generic substitute for source imports, call graphs, or evidence execution dependencies already represented by `EXECUTION_DEPENDS_ON`.

Alternative concretizations and multi-parent constraints are valid. A many-to-many relationship does not imply contradictory authority when all applicable parents can be jointly satisfied.

### 6.2 Reference integrity

Every material relationship must identify endpoints unambiguously enough for a later reviewer to recover the intended subject without hidden chat. Use the cheapest sufficient combination, such as:

- stable logical name or existing domain/workplan ID;
- repository path and section/anchor;
- governing protocol/release identity;
- Git commit/tag when a historical revision matters;
- another already-governed project identity where superior.

A new globally unique ID is not required when existing repository/version identity is sufficient. If a current artifact is renamed/moved/split/merged and a maintained dependency reference would otherwise become ambiguous or dangling, reconcile it in the same closeout. Historical entries intentionally referring to an old revision retain their immutable old reference.

### 6.3 Bounded completeness and the absence rule

A bounded dependency record is not automatically complete merely because it exists.

> **Absence of an edge is not evidence of independence unless the relevant scope has been explicitly reviewed as complete for that exclusion.**

When a dependency view is used to justify that an authority/evidence surface is unaffected, either:

- the relevant bounded scope is explicitly complete for that purpose; or
- the reviewer performs independent affected-surface reasoning using current authorities/code/evidence rather than treating missing edges as proof.

This prevents a lightweight partial map from becoming a false negative oracle.

### 6.4 Current dependency view versus evolution history

The current dependency representation describes currently applicable material relationships needed for impact analysis and verification. The semantic evolution record explains material supersession/rejection/generalization and why the current state changed. Git retains detailed chronology.

When a current relationship is superseded, remove/replace it from the current dependency view as appropriate and preserve the material reason in evolution history when the recording threshold is met. Stale dependency edges must not remain current merely for history.

### 6.5 Proportionality

Create/maintain an explicit dependency record only when it materially reduces ambiguity, invalidation risk, rediscovery, or stale-evidence confusion better than existing links/anchors/workplan mappings.

Counterfactual:

> If this record were absent, could a competent reviewer still identify the materially dependent authority/evidence surface reliably and economically from current canonical artifacts?

If yes, existing references are sufficient. If no, add the bounded record.

## 7. Evidence target versus execution dependency

Protocol 6.1 SHALL explicitly distinguish:

### 7.1 Evidentiary target

The proposition/invariant the evidence specification is intended to evaluate.

### 7.2 Execution dependency

The implementation, harness, fixture, dataset, environment, backend, tool, or other machinery needed to realize and interpret the evidence.

A test may evidence a D1/D2 invariant while executing through a D4 concretization. Replacing that D4 concretization can therefore produce different consequences:

- the evidence specification remains valid and is rerun against the new concretization;
- the specification remains semantically valid but its execution mapping requires revision;
- the oracle/assumption is concretization-specific and becomes stale;
- a prior evidence realization becomes inapplicable to the new subject revision while the specification remains durable.

Invalidation must follow actual typed dependency and applicability, not file proximity or generic transitive coupling.

## 8. Evidence lifecycle, applicability, and admissibility

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

`stale` means the prior realization/specification mapping cannot currently support or refute the target claim without review, rerun, or remapping. It does **not** by itself prove the governed claim false. Use `review-required` when applicability is uncertain rather than known invalid.

A PASS/accepted/closed claim may not depend on stale, rejected, unavailable-required, or otherwise inadmissible evidence.

Evidence validity has a domain. Where material, enough provenance must be recoverable to determine applicability across the relevant combination of:

- evidence specification revision;
- subject/candidate revision;
- governed claim/authority revision;
- input/validity regime;
- oracle semantics;
- environment/backend/precision/configuration when capable of changing interpretation;
- stochastic seed/replicate identity when material;
- required protocol obligation.

Do not require a universal manifest/hash envelope for every ordinary test run. Native CI/test/benchmark/experiment artifacts remain sufficient when they already establish the needed identity and interpretation.

A rerun against a changed candidate creates a new evidence realization; it does not mutate an old result into evidence for the new candidate.

## 9. Evidence durability, sufficiency, and independence

When equivalent evidentiary strength is available, prefer specifications coupled to durable governed invariants over replaceable concretization details.

Typical preference:

```text
scientific/mathematical invariant evidence
 > algorithm/numerical property evidence
 > behavioral/architectural contract evidence
 > concretization-specific evidence
```

This is a **durability preference**, not an evidence-substitution hierarchy. It SHALL NOT be interpreted as:

- D1 evidence replacing required D2 numerical verification;
- D1/D2 invariant evidence replacing required D4 functional/integration evidence;
- high-level end-to-end success proving lower-level conformance it cannot discriminate;
- lower-level unit precision establishing scientific adequacy.

Evidence may satisfy only claims its oracle and exercised semantic owner can establish. Preserve both:

```text
durability preference
AND
claim-specific evidentiary sufficiency
```

Proxy-proof/real-owner rules remain controlling. Do not weaken a stronger oracle merely to make a test more durable.

Low-level/concretization-specific evidence remains appropriate for fault localization, memory/lifetime safety, explicit public interfaces, persistence/serialization, numerical corner cases, performance regressions, historically recurring defects, implementation-specific failure behavior, and similar D4 claims.

### 9.1 Evidentiary independence and common-mode risk

For important/high-risk claims, prefer more than one independently justified evidence route when it materially reduces common-mode error risk. Examples may include a property test plus an independent reference method, analytical/limiting case plus numerical convergence evidence, or real-owner integration plus a structurally independent oracle.

Do not count multiple tests as independent merely because they are separate functions. Shared fixtures, shared expected-value generation, the same reference implementation, the same dataset defect, or the same mistaken assumption may create common-mode dependence.

This is risk-triggered, not a universal duplication requirement. Evidentiary diversity should improve confidence in a material claim rather than optimize a count.

## 10. Evidence assessment may aggregate multiple realizations

An evidence assessment may combine multiple realizations/observations when the governed claim requires replication, stochastic/statistical interpretation, convergence, cross-backend comparison, or independent evidence sources.

The assessment must preserve enough information to understand material dependence/common-mode assumptions and cannot erase contradictory admissible observations merely to manufacture a pass.

## 11. Bounded change impact and manual impact closure

When accepted authority or a material concretization changes:

```text
identify materially dependent descendants/evidence
 -> preserve unaffected siblings and still-valid evidence
 -> mark only affected items review-required/stale
 -> reconcretize/remap as needed
 -> realize required evidence again
 -> verify upward across the affected surface
```

A changed parent creates a review obligation over materially dependent descendants; it does not automatically prove every descendant wrong. A changed delegated owner does not freeze the old owner merely because historical evidence exercised it.

For a material authority/concretization change, the workplan/review impact set should account proportionately for:

```text
changed authority/concretization
 -> affected descendant authority/concretizations
 -> affected evidence specifications/realizations
 -> affected documentation/current dependency view
 -> required human re-ratification where applicable
 -> required revalidation/retirement/history update
```

Before closure, every material impact item must be resolved, preserved as still-valid with reason, or explicitly unavailable/blocking. “Old tests still pass” is never a substitute for impact closure.

### 11.1 Manual Protocol 6.1 integrity checks

Because 6.1 remains document-controlled, these checks are performed by workplan/review/Closeout reasoning rather than a mandatory machine graph:

- no accepted-current concretization is knowingly left bound to a superseded parent without an explicit compatibility/historical relationship;
- no PASS relies on stale/rejected/unavailable-required evidence;
- every material accepted authority change has its bounded impact closure evaluated;
- tests/evidence targeting superseded propositions are reviewed rather than silently retained as current confirmation;
- invariant-level evidence is preferentially preserved/remapped when still applicable;
- new material authoritative claims receive appropriate evidence;
- unresolved material dependency/evidence ambiguity remains a blocker rather than being inferred away from an incomplete map.

## 12. Historical semantic evolution record

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

- affected authority/concretization/evidence specification;
- previous and replacement semantics;
- triggering observation/evidence/challenge;
- relevant validity regime/assumptions;
- rationale and owning-domain disposition;
- affected descendants/evidence;
- references to current authority/workplans/reports/commits.

Do not duplicate full debate transcripts or turn history into a second current authority. Current normative documents must remain semantically complete for the accepted present system **without requiring historical chronology to reconstruct what is currently true**. History explains why the current state exists; it does not become hidden current authority.

## 13. Maintenance ownership and authority boundary

Dependency/history records are support/coordination artifacts; they do not become a fifth semantic authority.

Responsibility follows the semantic change:

1. the D1/D2/D3/D4 owner responsible for accepting or executing a material semantic change ensures materially affected dependency references and evolution-history obligations are identified;
2. `software-documentation` may reconcile, restructure, and publish those records as support but may not decide a disputed D1-D4 semantic relationship;
3. a material disagreement about concretization, assumptions, dependency, or evidence applicability routes to the earliest owning domain;
4. Closeout verifies required record updates are complete but does not invent product/scientific truth.

Do not require a permanent centralized historian role or separate approval gate.

## 14. Repository hygiene and retirement

Extend existing cleanup doctrine:

- obsolete concretizations, tests, guides, and compatibility machinery must not remain active merely because they once carried evidence or were historically important;
- historical value is preserved through Git/version-pinned artifacts and concise semantic evolution records;
- current active surfaces should not present superseded tests or implementations as competing apparent authority;
- removal remains conservative when a current supported compatibility, forensic, qualification, or explicit historical role still requires an artifact.

A superseded artifact is ordinarily eligible for retirement when:

1. it no longer owns current semantic authority;
2. no current supported concretization/evidence/compatibility path materially depends on it; and
3. material historical rationale needed to prevent rediscovery/confusion has been preserved through Git and/or the semantic evolution record.

Stale passing tests are particularly dangerous because they can fabricate confidence. Treat them as authority-confusion risk, not harmless excess coverage.

## 15. Workplan and workflow integration — document control remains authoritative in 6.1

Workplans remain bounded implementation/change contracts and remain the controlling task artifacts when materially warranted.

Workplans and reviews SHALL, proportionately to risk/scope, identify:

- materially affected authority/concretization relationships;
- evidence specifications and prior realizations likely to be invalidated;
- required new/repeated evidence;
- historical-record/current-dependency updates triggered by material supersession;
- genuine reopen triggers and unavailable-required evidence.

Do not require a workplan for every local D4 repair solely to populate dependency/history records. Existing proportionality rules remain binding.

The canonical human-facing Protocol 6 workflow prompt/profile remains active in 6.1. Installed-compatible-first/public-source-fallback resolution remains supported. Manual web copy/paste operation remains first-class.

## 16. Expected owning and affected surface

Implementation must begin from actual repository search/inspection, but the following are known expected current owners/consumers and must not be silently omitted when materially affected:

### 16.1 Canonical protocol source

- `source/shared/references/abstraction-and-realization.md` — retain this existing path as an opaque compatibility filename unless independent evidence justifies migration; rewrite current content/title/link text to abstraction/concretization semantics;
- `source/shared/references/workflow-and-workplans.md`;
- `source/shared/references/testing-and-validation.md`;
- `source/shared/references/documentation-and-evidence.md`;
- `source/shared/references/documentation-maintenance.md`;
- `source/shared/references/protocol-versioning-and-compatibility.md`;
- `source/shared/references/architecture-and-design.md`;
- `source/shared/references/specification-and-implementation.md`;
- D1/D2/scientific-software/language/convergence/health references where current abstraction-descent or evidence semantics occur;
- D1-D4 role skills and affected support-specialist skills;
- `source/shared/references/development-workflow-prompts.md`;
- affected workplan/change-plan templates, including the existing `abstraction_realization_change_plan_template.md` path as a compatibility identifier if retained;
- `source/README.md`, root `README.md`, `PORTABILITY.md`, and other current navigation/version documentation;
- `source/PROTOCOL_VERSION` only at coherent candidate promotion.

### 16.2 Build/generated/package surfaces

- `source/build_skills.py` and package manifests only where canonical file membership/names change;
- generated `dist/` skill packages and parity checks regenerated from canonical source, never patched independently.

### 16.3 Orchestrator/Profile compatibility

- current profile/version resolution code and tests;
- packaged protocol resources/snapshots;
- prompt/profile generation/parity checks;
- Orchestrator Core user documentation materially describing current profile/source resolution.

### 16.4 Qualification/tests

- repository protocol contract/portability tests;
- full existing Protocol 6 behavioral qualification scenario set plus the 6.1 additions below;
- affected package/profile/orchestrator acceptance tests.

The list is a known minimum surface, not a ceiling. Re-derive the final affected surface from the actual candidate before acceptance. Do not broad-rename archived/version-pinned files merely because search finds legacy vocabulary.

## 17. Protocol/profile migration and immutable 6.0 recovery

The pre-6.1 repository base for this workplan is commit `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`, where canonical `source/PROTOCOL_VERSION` is `6.0.0` and current Orchestrator profile identity is `ssdp-protocol-6.0`.

Before the first accepted-current 6.1 source mutation is treated as replacing current 6.0 authority:

1. preserve/document an immutable Protocol 6.0 recovery identity for the current accepted 6.0 source/profile behavior;
2. preserve existing `ssdp-protocol-6.0` packaged profile/resources as version-bound compatibility bytes rather than mutating them into 6.1;
3. keep existing 6.0 workplans resolvable under 6.0 semantics after 6.1 becomes current.

Protocol 6.1 SHALL introduce a distinct current profile identity, **`ssdp-protocol-6.1`**, using profile schema v2 unless implementation discovers a genuinely new profile-control field that requires a separately justified schema revision. Do not bump profile schema merely for terminology/prose changes.

After qualification, current/default profile selection may move to `ssdp-protocol-6.1`; a declared 6.0 workplan must continue to resolve the frozen 6.0 profile rather than being silently rendered through 6.1.

Current 6.1 public-source fallback documentation/prompts SHALL use the actual canonical repository identity:

`https://github.com/hjin98/scientific-software-development-protocol`

Historical 5.x/6.0 prompt/profile snapshots retain their historical bytes/URLs. Do not rewrite historical profiles merely because the repository was renamed.

## 18. Orchestrator compatibility in 6.1

The existing orchestrator remains non-mandatory infrastructure under 6.1. Update only what is necessary for correct 6.0/6.1 profile resolution, packaging, prompt/source compatibility, and current terminology.

Protocol 6.1 SHALL NOT silently adopt Protocol 7 workflow authority. In particular, do not introduce under 6.1:

- orchestrator-only canonical lifecycle state;
- mandatory TaskEnvelope/ResultEnvelope exchange;
- an orchestrator-owned deterministic reducer as the sole workflow authority;
- a machine-authoritative dependency/evidence graph;
- mandatory remote polling/web-agent transport;
- removal of manual first-class operation;
- removal of lifecycle/control responsibilities current skills/prompts/workplans still need.

## 19. Protocol 6.1 recovery snapshot

After complete acceptance and behavioral qualification, create an immutable release/tag/commit mapping for Protocol 6.1 analogous to existing historical recovery practice.

The snapshot must restore the semi-automated system without Protocol 7 components, including:

- current 6.1 canonical skills/references/templates/prompts;
- `ssdp-protocol-6.1` compatible profile/snapshot;
- workplan-guided manual/semi-automatic workflow;
- Markdown dependency/evolution doctrine and any project records needed for the release;
- required package/build/parity artifacts.

Document the immutable identity in protocol versioning/portability guidance. Do not maintain two live canonical branches after Protocol 7 cutover merely for fallback; fallback uses the pinned 6.1 release.

## 20. Implementation sequence

1. Confirm the governing base and preserve/document immutable Protocol 6.0 source/profile recovery before replacing current 6.0 authority.
2. Reconstruct the complete inherited 6.0/5.16 capability set relevant to this change and classify stable legacy `realization` identifiers/paths as immutable history, retained compatibility identifiers, or rename-safe current semantics.
3. Refactor the canonical authority/challenge owner around abstraction/concretization without losing feasibility, authority, Challenge, human-gate, bounded-invalidation, or multi-parent DAG doctrine.
4. Add evidence specification/realization/observation/assessment, evidence applicability, target/execution dependency, durability/sufficiency/independence, and manual impact-closure doctrine to the minimum current canonical owners.
5. Define the minimal Markdown conventions/location for bounded current semantic dependency records and semantic evolution history; define their ownership/Closeout triggers without creating duplicate authority.
6. Reconcile role skills, workflow prompts, templates, documentation/testing/architecture references, current public-source URL, README/navigation, and profile wording.
7. Introduce `ssdp-protocol-6.1` while freezing `ssdp-protocol-6.0` compatibility behavior; update default/current profile only when coherent.
8. Regenerate all derived skill packages and 6.1 snapshots from canonical source.
9. Run repository static/source/package/profile/orchestrator acceptance.
10. Run the complete inherited behavioral qualification set plus all new 6.1 scenarios against a real current Protocol 6.1 role/workflow decision surface.
11. Perform independent final Review and bounded Challenge Pass on the final semantic candidate and inspect qualification evidence rather than summary counts alone.
12. Set/confirm `source/PROTOCOL_VERSION = 6.1.0`, update compatibility/portability mappings, archive/close the workplan, and pin the immutable 6.1 recovery identity only after the coherent candidate passes.

## 21. Required adversarial qualification additions

The 6.1 qualification SHALL **extend, not replace, the complete existing Protocol 6 behavioral scenario set**. Run the inherited scenarios plus bounded additions demonstrating at least:

- declared 6.0 work resolves frozen 6.0 semantics/profile and is not reinterpreted under 6.1 vocabulary;
- current 6.1 work resolves `ssdp-protocol-6.1` and current canonical repository fallback;
- retained legacy path/ID lexemes remain compatibility identifiers without leaking old semantic vocabulary into current prose;
- relation direction is unambiguous, including `CONCRETIZES`, `SUPERSEDES`, evidence target, instantiation, observation generation, and execution dependency;
- absence of a bounded dependency edge cannot prove independence unless completeness for that scope was explicitly established;
- a stale passing test cannot close a current claim;
- a stale failing result cannot refute a current claim without applicability reconciliation;
- replacement of a delegated D4 concretization does not automatically invalidate a durable invariant-level evidence specification;
- a concretization-specific oracle is marked stale/remapped when its owner is superseded;
- an upstream authority change invalidates only materially dependent descendants/evidence;
- a D4 observation can route a Serious Challenge to D1/D2/D3 rather than forcing local repair;
- evidence/specification/oracle failure is considered as an alternative explanation for contradiction;
- evidence durability cannot substitute high-level evidence for required lower-level conformance or vice versa;
- important independent evidence routes are not falsely counted as independent when they share a common oracle/fixture/assumption;
- semantic history preserves material rationale without becoming current authority or a prerequisite for reconstructing current semantics;
- retirement removes superseded active authority/evidence only when current dependencies/compatibility no longer require it;
- workplan/prompt/manual operation remains sufficient without Protocol 7 machinery.

Behavioral meaning, not exact wording, is the oracle.

## 22. Candidate identity and qualification records

Qualification must identify the semantic candidate it evaluates. If committing the qualification result or archiving the workplan necessarily creates later commits, preserve the existing Protocol 6 distinction:

- **semantic candidate commit** — the source/profile/product semantics under qualification;
- **evidence-bearing/lifecycle commit** — later commit containing qualification records or closeout-only changes that do not alter the qualified semantic candidate.

A later evidence-only commit does not require circularly treating the result record as having existed inside the commit it records. Any later semantic mutation invalidates/reopens the applicable qualification surface.

## 23. Acceptance criteria

Protocol 6.1 is PASS only when all of the following hold on one coherent semantic candidate, allowing later verified evidence/lifecycle-only commits:

1. current 6.1 authority consistently uses abstraction/concretization and evidence specification/realization/observation/assessment terminology;
2. historical/version-pinned 6.0 and 5.x truth remains intact, recoverable, and not silently reinterpreted;
3. `ssdp-protocol-6.0` remains frozen/resolvable for declared 6.0 work and a distinct `ssdp-protocol-6.1` current profile is qualified;
4. every still-valid Protocol 6.0/5.16 safeguard remains semantically recoverable;
5. evidence is first-class support/challenge material without becoming D5 or parallel truth authority;
6. evidence target, execution dependency, specification, realization, observation, and assessment are distinguished;
7. evidence applicability/admissibility and stale passing/failing semantics are explicit;
8. evidence durability preference cannot replace claim-specific sufficient/proxy-proof evidence;
9. material evidentiary independence/common-mode risk is addressed proportionately for high-risk claims;
10. typed semantic dependency tracing has explicit direction/reference integrity and bounded completeness semantics without a mandatory machine graph/database;
11. absence of an unrecorded edge is not treated as proof of non-impact unless completeness for that exclusion is established;
12. bounded manual impact closure is integrated into workplan/review/Closeout and unresolved material impact remains blocking;
13. concise semantic evolution history is integrated with authority/workplan/review/cleanup without becoming a second current authority;
14. current normative documents remain present-state owners reconstructable without hidden chat/history;
15. retirement/cleanup does not leave superseded tests/concretizations as competing current authority and does not delete still-supported compatibility/evidence paths;
16. current skills/prompts/workplans retain the full document-controlled Protocol 6.1 execution contract;
17. existing local/manual/web activation remains usable without Protocol 7;
18. current 6.1 public repository fallback points to `hjin98/scientific-software-development-protocol` while historical profile bytes remain version-pinned;
19. canonical-source/generated-source/profile/version compatibility is coherent;
20. repository tests, package validation/parity, frozen-6.0 + current-6.1 profile/snapshot checks, applicable Orchestrator Core acceptance, and the complete inherited-plus-new behavioral qualification execute and pass;
21. independent final Review finds no blocker and no active Serious Challenge;
22. an immutable documented Protocol 6.1 pre-automation recovery identity is established at closeout.

## 24. Explicit non-goals

- Do not build the Protocol 7 control plane in this workplan.
- Do not make the orchestrator mandatory.
- Do not replace semantic Markdown documents with JSON.
- Do not introduce a graph database merely because semantic dependencies form a graph.
- Do not create a universal claim/edge/ID/evidence manifest merely for symmetry.
- Do not treat missing edges in a partial Markdown dependency view as proof of independence.
- Do not rewrite historical Protocol 6.0/5.x artifacts or frozen profiles to current vocabulary.
- Do not create a fifth authority-bearing evidence role or centralized historian approval role.
- Do not weaken existing real-owner/proxy-proof evidence to increase test durability.
- Do not require universal dependency/history records for trivial/local work.
- Do not treat Git chronology alone as sufficient semantic rationale for material supersession.
- Do not replace the complete inherited behavioral qualification with only new 6.1 delta scenarios.
- Do not release 6.1 with an unresolved governing Serious Challenge or missing required qualification.

## 25. Final pre-implementation review disposition

```text
SERIOUS CHALLENGE: NONE
FINAL WORKPLAN DESIGN REVIEW: PASS
BLOCKING DESIGN GAPS: CLOSED
READY FOR IMPLEMENTATION: YES
GOVERNING IMPLEMENTATION CONTRACT: THIS CONSOLIDATED WORKPLAN
```

When accepted after implementation, Protocol 6.1 becomes:

> **the final stable semi-automated, document-controlled SSDP release and the immutable recovery baseline for Protocol 7 development.**

Protocol 7 may supersede its workflow-control mechanism but must preserve its semantic authority, evidence, evolution, challenge, engineering-quality, and historical-recovery doctrine unless a deliberate higher-authority revision explicitly replaces a rule with a stronger one.
