---
kind: abstraction-concretization-change-plan
workplan_id: PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY
protocol_version: 6.2.0
target_protocol_version: 6.3.0
status: active
created_date: 2026-09-11
reviewed_date: 2026-09-12
design_closure_status: pass-after-sixth-review-repair
implementation_handoff: authorized
implementation_review_state: independent-review-no-pass-owner-binding-repair-open
reviewed_candidate_no_pass: 100cbde296de6c1a8db14151f34cfacfebc90eb3
reviewed_candidate_no_pass_2: 3bbbdfa8120646d76336c7b916e6a891c9ed38f2
qualified_semantic_candidate: 3bbbdfa8120646d76336c7b916e6a891c9ed38f2
f2_qualification_commit: 6fc26ce374b5346495782871d5d7241de5b90071
f2_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F2.md
reopened_stages: D4R3,E3,F3
stage_g_recovery_gate: blocked-pending-D4R3-E3-F3-independent-review
active_serious_challenge: none
parent_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
parent_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
parent_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
parent_protocol_62_mapping_commit: bc76b16fda96be09f38a1b40a2ef877e8309534d
parent_protocol_62_generated_reconciliation: ca622ea2b1c33e70668060cf0cc2fe9138776f7f
branch_point: bf856f742d1744a8ff50f300ee6493fb93e5c9d0
---

# SSDP 6.3 Evidence-Backed Project Engineering Memory

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** already preserves engineering history in Git, workplans, reviews, qualifications, tests, benchmarks, semantic-evolution records, generated/package evidence, and immutable recovery snapshots. Protocol 6.2 added lossless representation and progressive disclosure, but a fresh-context engineer can still miss important project-specific lessons distributed across that history.

Protocol 6.3 adds **Project Engineering Memory (PEM)**: a compact, project-local, non-authoritative representation of demonstrated engineering lessons. It must help a fresh agent recover what repeatedly failed, what repeatedly worked, why, under what conditions, with what evidence, and with what current applicability. It must not become a fifth authority domain, a substitute for history, or a mechanism for freezing old implementations.

Terms used by this workplan:

- **historical evidentiary corpus** - durable project evidence from which PEM findings are assessed; evidence/provenance, not D1-D4 authority;
- **evidence binding** - a resolvable reference from a PEM claim to the evidence specification, realization, observation, and assessment that warrants it;
- **binding health** - whether a material evidence/authority route remains resolvable and interpretable (`HEALTHY`, `REVIEW_REQUIRED`, `UNAVAILABLE`, `RETIRED`);
- **evidence admissibility state** - whether a row may contribute to a current bounded claim/count (`ADMISSIBLE`, `REVIEW_REQUIRED`, `INCONCLUSIVE`, `CHALLENGED`, `REJECTED_OR_INVALID`, `STALE_OR_INAPPLICABLE`, `RETIRED`);
- **learning family** - a stable generalized project lesson, classified as `FAILURE_FAMILY`, `SUCCESS_PATTERN`, `DISCOVERY`, or `PRESERVATION_CAPABILITY`;
- **semantic identity envelope** - the bounded generalized meaning attached to one accepted family ID: family kind, governing invariant/claim, owner class, causal/mechanistic family, and materially relevant applicability dimensions. Wording may evolve inside the envelope; a material change requires explicit lineage rather than silent ID reuse;
- **occurrence** - one independently introduced or independently existing confirmed manifestation of a failure family; one causal episode producing many symptoms is normally one occurrence;
- **evaluated application episode** - one materially distinct engineering intervention/application of a positive pattern under a declared regime, assessed as `SUPPORTING`, `NEUTRAL`, `CONTRADICTING`, or `INCONCLUSIVE`; one coordinated intervention propagated across many files/sites is normally one episode plus multiple affected surfaces, not many applications;
- **successful application** - an evaluated application episode whose claimed benefit and governing constraints are supported by admissible evidence;
- **evidence provenance cluster** - a set of evidence/application episodes sharing a material upstream intervention, implementation lineage, PEM selection policy, oracle, dataset, benchmark harness, or other dependency that limits evidentiary independence;
- **aggregation scope** - the bounded regime over which statistics may be combined without hiding material differences in owner, implementation class, language/runtime, backend/hardware, input regime, lifecycle context, or project identity;
- **coverage state** - declared historical-search coverage (`UNINITIALIZED`, `PARTIAL`, `RECONCILED_FOR_DECLARED_SCOPE`); absence from incomplete memory is never evidence of absence;
- **memory temperature** - importance/attention classification (`HOT`, `WARM`, `COLD`, `UNASSESSED`), distinct from Protocol 6.2 hot/cold activation and never authority or a pass threshold;
- **evidence maturity** - claim-relative confidence in a bounded finding (`PROVISIONAL`, `SUPPORTED`, `PROVEN`), distinct from admissibility and current applicability;
- **authority binding** - relation between a learned capability and current authority: `EVIDENCE_ONLY`, `AUTHORITY_BOUND`, or `PROPOSED_FOR_PROMOTION`;
- **governing-owner binding** - an immutable route to the real owner relied upon for normative or acceptance force, grounded in the project-governed accepted state; a free-text owner label, a branch-only descendant, or an unrelated healthy evidence route is not authority;
- **positive-guidance eligibility** - whether a success pattern may be phrased as a recommended project instinct; it requires current applicability, adequate support, healthy/admissible warrants, and no unresolved material contradiction for the stated regime;
- **comparative guidance claim** - a stronger claim that one viable approach should be preferred, is better/best, should be default, or is higher leverage relative to another; it requires comparative evidence or current owner authority appropriate to the governing objective/tradeoff, not merely evidence that one approach works;
- **lifecycle context** - where an event was observed, such as development, qualification, accepted-current runtime, production, recovery/migration, or historical-only;
- **Historical Applicability Set (HAS)** - the current-work record of materially relevant PEM entries and their applicability dispositions, together with the accepted project-memory basis used to derive those dispositions;
- **capability-transfer map** - mapping from replaced machinery to learned capability, authority-binding state, current owner if any, replacement/retirement, and verification;
- **logical canonical memory** - one project-level PEM source of current meaning with one discoverable root; cold canonical detail may be partitioned only when justified and without duplicate hand-authored truth;
- **logical-memory publication unit** - the coherent root/detail state that must be reviewed and published together when one semantic PEM change spans multiple canonical files;
- **accepted project-memory basis** - the exact project integration/release/acceptance state selected by project Git/workflow policy whose PEM is the base for new work; branch/default/latest/timestamp/self-declaration is insufficient;
- **candidate memory overlay** - validated same-branch candidate PEM changes composed explicitly over the accepted/base memory for that branch only;
- **PEM relation** - a typed non-authoritative relationship among PEM entries used for lineage or impact closure; it may not recursively manufacture warrant;
- **causal attribution** - a claim that an intervention or mechanism caused an observation, stronger than merely recording the observation or association and therefore requiring discriminating evidence;
- **fresh-context agent** - an agent or engineer that must recover project state from durable artifacts rather than private conversational memory.

## 1. Outcome, authority, and parent contract

Protocol 6.3 is a backward-compatible minor strengthening of accepted Protocol 6.2. The accepted semantic/rollback parent is `b59adc77efe6951912cfd705cc43830c58ca27d0`; the 6.2 semantic candidate through that recovery is `ebbc4591bdfed039512026b8acb3a6749475c1c5`; public-source bootstrap is `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`; mapping and generated reconciliation are `bc76b16fda96be09f38a1b40a2ef877e8309534d` and `ca622ea2b1c33e70668060cf0cc2fe9138776f7f`. These identities are distinct and must remain distinct.

Protocol 6.3 SHALL preserve every accepted Protocol 6.2 doctrine and still-valid historical capability, including T01-T39, D1-D4 authority and routing, Challenge/Serious Challenge, evidence lifecycle/applicability/independence, first-clean-local-defect economy, owner-layer simplification, lossless representation, current-vs-history separation, cold-route behavior, replacement-bootstrap discipline, static activation sensors, immutable 5.16/6.0/6.1/6.2 resources, profile identity, source/generated/package parity, all 115 accepted 6.2 behavioral scenarios, affected requalifications and Stage-G recovery/package acceptance, human-facing background/terminology rules, assembled-candidate independent Review, and Git/concurrent-work/history-mutation safeguards.

Tests, commits, reviews, workplans, statistics, history, and PEM are evidence/coordination/representation according to their actual role. None becomes D1-D4 semantic authority through repetition, packaging, temperature, maturity, or qualification status. If implementation exposes a genuine defect in accepted 6.2 authority, stop at the earliest affected owner and use the existing Challenge process; PEM cannot choose new semantic truth.

Protocol 6.2 remains accepted-current until the full 6.3 lifecycle passes. This workplan does not authorize merge/cutover to `main`.

### 1.1 Non-goals

Protocol 6.3 MUST NOT create a universal database/graph/daemon/background indexer; force full-history scans on ordinary tasks; make PEM universal hot context; turn every local bug into durable memory; infer probabilities from raw counts; treat historical mechanisms as invariants; create a second hand-authored JSON/YAML authority; package live project PEM as generic SSDP content; silently interpret unknown schemas; pool incompatible regimes or projects; count copied/forked history as local incidence; reuse accepted family IDs for materially different meanings; multiply one positive intervention across many surfaces into many applications; rewrite historical observations to match later assessments; promote `PROVEN` from counts/temperature/reviewer votes; convert "works" into "best/preferred/default" without stronger warrant; leave overlapping incompatible guidance unconditional; treat `reconciled_through` as historical-coverage proof; or broaden this revision into unrelated Protocol 7 architecture.

## 2. Governing learning and evidence rules

### 2.1 Evidence-backed learning

The required epistemic chain is:

```text
idea/hypothesis
 -> implementation or attempted intervention
 -> evidence specification
 -> evidence realization
 -> observation
 -> assessment
 -> bounded finding
 -> generalized project lesson when justified
 -> current PEM representation
```

Statements such as "this should be faster", "this seems cleaner", or "this might scale better" remain hypotheses until evidence suitable to the bounded claim exists. Qualification decides whether a bounded claim is accepted under its governing authority; qualification itself is not a new authority domain.

### 2.2 Outcome, association, and causal attribution

PEM MUST NOT strengthen the claim beyond the evidence. Keep distinct:

```text
observed outcome
association with a change
mechanism-specific causal attribution
generalized transferable lesson
```

A bundled repair A+B+C may prove that the assembled candidate no longer crashes without proving that A alone caused the repair, that B/C were irrelevant, or that the mechanism generalizes. A causal/mechanism-specific claim requires discriminating evidence appropriate to the claim: isolation, ablation/counterfactual comparison, causal trace, owner-tied static/property analysis, algorithmic proof, or another independently justified method. Temporal proximity to a commit is investigation evidence, not root-cause proof. Where isolation is unavailable, preserve the combined-change outcome and keep causal interpretation provisional/bounded.

### 2.3 Positive and negative evidence balance

Before admitting or materially strengthening a `SUCCESS_PATTERN`, perform a bounded evidence-directed search over the declared coverage/aggregation scope for materially applicable supporting, neutral, contradicting, failed, and inconclusive attempts. State the search basis and material blind spots. Incomplete counterevidence search may support `PROVISIONAL`/`REVIEW_REQUIRED`, not an unqualified project instinct.

After admission, materially applicable evaluated attempts must not be selectively omitted by outcome. Failure families likewise preserve material safe/disconfirming evidence that narrows or falsifies an overbroad cause or regime. Real occurrences remain history; overbroad interpretation must narrow, split, or reclassify.

### 2.4 Evidence admissibility, observation/assessment preservation, contradiction, and disagreement

Historical realization/observation evidence is distinct from assessment. Once a material realization and observation are durably recorded, later invalidation, disagreement, reclassification, or stronger analysis SHALL normally add/supersede the assessment/admissibility relation rather than rewrite what was observed. A clerical correction is permitted only when the original record and correction provenance remain recoverable enough to explain the change.

Only currently admissible rows for the stated bounded claim/family assignment contribute to current confirmation/support counts. Invalidated oracle, confounded benchmark, stale realization, or disproven family assignment triggers bounded reassessment, recomputation of affected counts/maturity/temperature/guidance, and preservation of unaffected evidence.

Conflicting competent assessments are not resolved by majority vote, reviewer prestige, chronology, or latest-editor wins. Assess applicability, oracle strength, independence/common-mode risk, aggregation scope, and governing claim. If material disagreement remains, mark the claim contested/`REVIEW_REQUIRED`; do not present it as established positive guidance.

### 2.5 Counts, application episodes, and recurrence

Counts are descriptive under declared coverage and aggregation scope. They are not probabilities, rates, or causal strength unless an explicit exposure/opportunity denominator and defensible sampling basis exist.

One causal episode producing many failures is normally one occurrence. A recurrence-after-accepted-repair requires evidence that an earlier repair was actually accepted before a later independent occurrence in the relevant project/causal lineage. Author/committer/issue/file timestamps and cherry-pick order are supporting metadata only; rebases or copies must not manufacture recurrence chronology.

For positive patterns, one coordinated engineering intervention/application is one evaluated application episode even when it touches many modules, call sites, files, tests, workers, or downstream surfaces. Record surface breadth separately. Repeated executions and cherry-picked/copied instances of the same underlying intervention do not multiply application count. A later materially distinct engineering application may count once when separately assessed.

### 2.6 Evidence independence, provenance clusters, and policy-induced dependence

Repeated executions, reviews, or application episodes sharing one defective oracle, fixture, benchmark harness, dataset, reference implementation, implementation lineage, PEM selection policy, or other upstream decision are correlated. They do not automatically constitute independent evidence even when they are legitimately separate application episodes.

Record a material **evidence provenance cluster** when common dependence affects interpretation. Multiple deployments selected because the same PEM recommendation and using the same copied implementation may demonstrate breadth/continued robustness, but they are not automatically multiple independent proofs that the recommendation is comparatively superior. Independence-sensitive maturity or comparative claims must account for the cluster rather than count filenames/runs/applications mechanically.

### 2.7 Claim-relative maturity and comparative guidance

Evidence maturity is always relative to an explicitly bounded claim and regime:

```text
PROVISIONAL - material evidence obligations or uncertainty for the bounded claim remain open, or evidence is exploratory
SUPPORTED   - admissible evidence materially supports the bounded claim, but evidence obligations needed for a stronger/generalized claim remain open
PROVEN      - every evidence obligation required by the governing owner/workplan for that exact bounded claim is closed with admissible applicable evidence; required independence/replication is satisfied; no unresolved material contradiction remains in the declared regime
```

`PROVEN` is not permanent. A changed candidate, oracle, regime, dependency, or newly material counterevidence may make it review-required. Counts, temperature, reviewer votes, age, or repetition do not auto-promote maturity.

Evidence that an approach works establishes only the demonstrated property. Claims such as `preferred`, `better`, `best`, `default`, `higher leverage`, or `more efficient overall` are stronger comparative/decision claims. They require admissible comparative evidence across materially viable alternatives under the same governing objective/constraints, or explicit current owner authority selecting the tradeoff/default. If alternatives trade speed, memory, complexity, maintainability, robustness, portability, accuracy, or other objectives differently, preserve the tradeoff rather than collapse it to one scalar preference without accepted prioritization.

### 2.8 PEM relations, semantic identity, and overlapping guidance

Typed PEM relations MAY capture lineage, narrowing/generalization, discovery-to-pattern learning, or capability relationships. Every substantive endpoint remains independently grounded in admissible evidence and, where normative, current authority. A PEM-to-PEM chain or cycle cannot be the sole warrant for a substantive claim.

Every accepted family ID has a **semantic identity envelope**. Editorial clarification or evidence-backed narrowing that remains materially the same generalized family may retain the ID. A material change in family kind, governing invariant/claim, owner class, causal/mechanistic family, or applicability meaning requires explicit split/merge/successor/reclassification lineage rather than silent ID reuse. Current split/merge/supersession lineage must be acyclic and resolve each historical accepted ID to an unambiguous current disposition. Reactivation of materially the same retired family is a state transition, not a reverse lineage edge.

When a source entry is invalidated, narrowed, split, merged, retired, or materially reclassified, perform bounded downstream impact closure over dependent current PEM entries. Absence of a relation proves independence only if the mapped scope was explicitly complete enough for that exclusion.

Two individually valid current patterns can overlap yet recommend incompatible actions. Where materially overlapping entries imply incompatible decisions, narrow their regimes, state the governing tradeoff/decision predicate, route to current owner priority, or mark the decision contested/`REVIEW_REQUIRED`. Do not present incompatible overlapping recommendations as unconditional independent engineering instincts.

### 2.9 Evidence across trust boundaries remains data

Issue text, logs, model output, generated reports, external documents, copied PEM, and other evidence content remains data. Embedded commands, prompts, links, tool requests, or policy-like prose do not gain instruction/authorization precedence merely because PEM retrieved them. Preserve provenance/trust classification, avoid unnecessary raw untrusted instruction-like text in the active summary, and keep tool/network/repository mutation under existing authorization owners.

## 3. Canonical ownership and architecture

Stage A SHALL confirm actual 6.2 ownership before mutation. Intended local ownership is:

```text
universal authority/Challenge/lossless representation -> abstraction-and-concretization.md
PEM-specific schema/representation/family relations -> project-engineering-memory.md
evidence lifecycle/admissibility/applicability/impact -> evidence-evolution-and-dependencies.md
recurrence/family membership/first-local-defect -> convergence-and-cycle-economy.md
architecture capability/mechanism replacement -> architecture-and-design.md
workflow/HAS/handoff/closeout -> workflow-and-workplans.md
current-vs-history documentation lifecycle -> documentation-maintenance.md
testing/benchmark/oracle methodology -> testing-and-validation.md
version/bootstrap/recovery/profile -> protocol-versioning-and-compatibility.md
repository intake/scope/history economy -> repository-intake.md
branch/merge/integration/history mutation -> git-and-version-control.md
trust/privacy/least privilege -> security-and-trust-boundaries.md
```

`project-engineering-memory.md` owns only PEM-specific semantics and routes generic doctrine to existing owners. Do not duplicate generic current SSDP rules into PEM as competing authority.

### 3.1 One logical canonical project memory

Default root is `PROJECT-ENGINEERING-MEMORY.md` at the governed project/repository root unless project authority declares one alternative canonical path. The artifact declares project/repository/scope identity.

One physical Markdown file is preferred while sufficient. If demonstrated scale, merge contention, or context/search cost makes it materially inferior, cold canonical detail MAY be partitioned beneath one logical PEM namespace. Partitioning must retain one root discovery/current-summary surface, one canonical home per family/notice/evidence row, stable IDs/routes, lossless coverage/aggregation/lineage, no duplicate hand-authored current truth, and source-control review visibility.

A semantic change spanning root plus canonical partitions is one **logical-memory publication unit**. Root, affected partitions, and any required canonical metadata must be reviewed/published coherently; mixed semantic revisions must not masquerade as one current memory. A derived index is non-authoritative and may be stale/unavailable; stale index results cannot prove absence. Fall back to canonical search where feasible or expose `REVIEW_REQUIRED` uncertainty.

### 3.2 Project, fork, and multi-project scope

Copied/forked PEM may be useful evidence but does not automatically become local incidence or accepted local memory. Preserve source-project identity. Local continuity requires project governance to declare lineage continuity/reconciliation. Cross-project aggregation requires an explicitly multi-project aggregation scope and compatible evidence; nearest-file discovery never decides precedence.

For non-local evidence, a bare commit SHA plus path is insufficient because Git object identities are repository-relative in interpretation. Bind source repository/project identity (or equivalent durable source identity), immutable revision, and stable locator. Repository moves/renames require explicit alias/lineage or binding health degrades.

### 3.3 Schema and accepted-memory basis

Initial PEM schema is `memory_schema_version: 1`, separate from SSDP protocol version and orchestration profile schema. A reader must not infer compatibility from similar Markdown headings. Unknown/incompatible schema permits only explicitly forward-readable identity metadata; substantive memory becomes unsupported/`REVIEW_REQUIRED` for tasks requiring it. Supported migration is a `PEM_SCHEMA_OR_PROTOCOL_CHANGE` and must losslessly preserve accepted IDs, evidence/assessments, coverage, aggregation scope, lineage, counterevidence, authority bindings, notices, and cold routes.

Accepted/base memory comes from the exact project integration/release/baseline selected under project workflow/Git policy. `main`, default/latest, timestamp, or the PEM file claiming itself accepted is not sufficient by itself.

A validated same-branch **candidate memory overlay** composes over that accepted/base PEM for later work on the same branch:

```text
accepted/base PEM
 + explicit candidate overlay for this branch/cycle
 -> effective branch-local decision support
```

The overlay remains visibly candidate, preserves its base identity, cannot self-ratify or override current authority, and cannot silently erase an accepted entry through omission. Candidate deletion/retirement is explicit. Conflict or partial reconciliation between base and overlay is `REVIEW_REQUIRED` until resolved.

### 3.4 Conditional activation, applicability, and HAS basis

PEM activation is decision-local. Trigger it for substantial rework of mature D1-D4 semantics/concretization, replacement/consolidation of mature machinery, suspected recurrence, substantial optimization/scaling work, migration/recovery/revert where historical choices matter, or an active workplan explicitly binding relevant PEM entries.

A first clean local defect with no recurrence/generalization signal remains local. Ordinary/trivial/unrelated routes do not load PEM merely because it exists. Memory temperature does not activate context.

When triggered, use progressive disclosure:

```text
accepted base + validated branch overlay
 -> active summary
 -> cheapest sufficient metadata-level applicability match
 -> relevant family/notice detail
 -> raw evidence only when needed
```

Applicability matching uses owner, surface, mechanism, capability, regime, project scope, and current task. The active/Hot summary is not the complete search boundary. Warm/Cold entries can be materially applicable.

Applicability metadata is part of current family semantics. When claim/cause/scope/owner/regime/split/merge/retirement/project identity changes, update matching predicates in the same semantic publication. Stale tags cannot prove non-applicability; suspect metadata requires broader canonical search or `REVIEW_REQUIRED` uncertainty.

A memory-triggering workplan/HAS records the exact accepted project-memory basis and material candidate overlay, if any, consulted when deriving its applicability dispositions. If the target accepted memory, overlay, or governing owner materially advances before integration/closeout, perform bounded reconciliation over the changed interval/surface and refresh affected HAS dispositions. A HAS derived from an obsolete basis cannot silently close current work.

## 4. Canonical PEM content model

### 4.1 Global metadata and coverage watermark

Expose at least:

```text
memory_schema_version
maintained_under_protocol
project/repository/scope identity
coverage_state and coverage_basis
reconciled_through: already-existing immutable accepted project identity
known unreviewed ranges/surfaces when material
accepted/base identity used by a candidate overlay
open review-required families/notices
```

`RECONCILED_FOR_DECLARED_SCOPE` claims only the declared bounded scope. `reconciled_through` is an identity horizon for reconciliation, not proof that every earlier commit/event was examined. Coverage completeness derives only from `coverage_state` plus `coverage_basis`, including declared owners/surfaces/ranges/sources and material blind spots. Advancing `reconciled_through` cannot silently upgrade PARTIAL coverage or prove absence.

### 4.2 Family and notice identifiers

Use stable namespaces:

```text
FF-### failure family
SP-### success pattern
DS-### discovery
PC-### preservation capability
NT-### current notice
```

Occurrence/application IDs are family-scoped (`O01`, `A01`, ...). Accepted IDs are stable and never recycled. Branch-local IDs are provisional and collision-safe reconciliation is required before acceptance. Cherry-picked/rebased copies of one underlying event are provenance aliases, not new occurrences.

Each accepted family records enough of its semantic identity envelope and lineage/current disposition to detect silent semantic reuse. Split/merge/supersession/alias topology must be acyclic; a current reader must not encounter one accepted historical ID resolving to incompatible simultaneous current meanings.

### 4.3 Admission threshold

Admit/materially update a family only when evidence supports materially recurring same-family failure; reintroduction after accepted repair; one high-impact broadly reusable lesson; meaningful likely-reusable optimization/simplification; repeated successful use with independence represented honestly; a discovery materially changing preferred recurring work; mechanism replacement/generalization/rejection/restoration likely to prevent rediscovery; or a high-risk temporary fact best represented as a current notice.

A first clean local defect normally stays local. Generic textbook knowledge/current generic protocol doctrine stays at its existing owner.

### 4.4 Failure-family semantics

Membership requires materially equivalent governing invariant, semantic owner/authority class, and failure mechanism/cause at the repair-relevant level. Symptom/error/file/subsystem similarity is insufficient. Record observed failure separately from causal interpretation. Preserve safe/disconfirming cases that narrow the family.

A compact occurrence retains immutable event identity, lifecycle context, aggregation/project dimensions, subject/candidate, owner/surface, observed failure, bounded cause claim plus cause evidence, repair reference, post-repair qualification, material disconfirming evidence, admissibility/family assignment, limits, and applicability.

### 4.5 Success-pattern semantics

Record every materially applicable evaluated **application episode**, not only wins: intervention/application identity, affected surfaces, selection/provenance cluster when material, subject/candidate/comparator, regime, intended benefit, outcome, qualification/analysis binding and health/admissibility, effect size when available, experimental envelope/uncertainty, governing correctness/constraints, costs/tradeoffs, applicability/limits, project/lifecycle context.

A supporting outcome increments support only while admissible. Neutral/contradicting/inconclusive/rejected/stale rows remain historically recoverable and constrain current interpretation. One coordinated intervention counts once regardless of how many surfaces it affects; surface breadth is tracked separately.

A positive recommendation requires positive-guidance eligibility, not merely high temperature or high historical support count. Comparative/default/preferred guidance additionally requires the stronger comparative warrant defined in Section 2.7.

### 4.6 Discovery and preservation capability

A discovery records the changed project understanding, bounded evidence, regime, competing prior interpretation, and whether authority changed separately.

A preservation capability is explicitly `EVIDENCE_ONLY`, `AUTHORITY_BOUND`, or `PROPOSED_FOR_PROMOTION`. Only `AUTHORITY_BOUND` is mandatory, and only because the cited current owner requires it. Repetition/temperature/qualification cannot promote evidence into authority.

When machinery is replaced:

```text
old mechanism -> learned capability -> authority-binding/current owner
              -> new mechanism or justified omission/retirement -> verification
```

Preserve demonstrated capabilities as evidence and actual owner-bound obligations as requirements; do not preserve obsolete wrappers/caches/executors/checkpoint formats merely because history mentions them.

### 4.7 Typed PEM relations and overlapping guidance

Relations MAY include `LED_TO`, `NARROWS`, `GENERALIZES`, `SUPERSEDES`, `REPLACES`, `SUPPORTS_LEARNING_FROM`, and equivalent explicitly defined types. Keep current lineage direction unambiguous and acyclic. Same underlying evidence reused by multiple entries does not become multiple independent routes or multiple events.

When current relation/applicability analysis reveals overlapping incompatible guidance, store enough decision/tradeoff boundary to prevent unconditional simultaneous recommendation; otherwise mark the overlap contested/review-required.

### 4.8 Current notices

A notice stores stable ID, current bounded claim/state, governing owner when normative or explicit non-authoritative status, evidence/source route with health/admissibility, applicability, and review/expiry condition. Notices do not contribute to family counts. When expiry/review triggers, remove unqualified active guidance and reconcile to `REVIEW_REQUIRED`, `RETIRED`, a family, or current owner as appropriate.

## 5. Evidence, statistics, temperature, maturity, and salience

### 5.1 Evidence bindings and immutable observation provenance

Prefer immutable Git revision + path + stable section/test/finding identifier. For expiring external CI/benchmark evidence on which long-lived PEM depends, preserve a compact durable repository record of the material observation and exact external run/candidate identity when policy permits. PEM or a generated summary cannot be the sole warrant for its own substantive claim.

A material evidence record preserves realization identity and observed result separately from time/version-bound assessment and admissibility. Later invalidation changes current assessment/admissibility; it does not silently rewrite the old measurement/output. A clerical correction preserves correction provenance.

Material current bindings are checked when activated, semantically reconciled, or reached by affected impact closure; no full-memory daemon is required. Broken/uninterpretable bindings preserve historical record but remove unsupported unqualified current guidance.

### 5.2 Self-reference-safe updates

If a PEM event must bind exact engineering/evidence commit identity, use:

```text
engineering/evidence candidate exists immutably
 -> qualification/assessment exists or is durably identifiable
 -> descendant PEM reconciliation binds those identities
 -> later closeout/mapping binds reconciliation if needed
```

A PEM-containing commit never needs to know its own SHA. Same-commit update is permitted only when all material subject/evidence identities already exist independently.

### 5.3 Quantitative evidence and comparative claim strength

Preserve effect size rather than adjectives when quantitative evidence exists, together with material baseline/candidate identity, input/data, hardware/backend/precision/toolchain, concurrency/resources, warm-up/cache/checkpoint state, measurement definition, normalization/scaling basis, replicate count, and dispersion/uncertainty where noise can change the conclusion.

Do not attribute a gain to one mechanism when candidate and baseline differ materially elsewhere unless the claim explicitly concerns the combined change. Complexity claims such as `O(N^2) -> O(N log N)` require adequate algorithmic analysis plus evidence that implementation realizes the analyzed algorithm; a single timing sample is insufficient.

Do not infer overall preference from one metric. If A is 4x faster but materially worse in memory, accuracy, portability, complexity, robustness, or another governed objective, preserve that tradeoff. Comparative guidance must identify the comparison set and governing objective/priority or route to current owner authority.

### 5.4 Derived statistics and provenance dependence

Counters are derived from current admissible ledger rows/application episodes, never independently hand-maintained. Track at minimum:

```text
failure: confirmed occurrences, repair cycles, affected surfaces,
         recurrence-after-accepted-repair, first/last confirmed,
         coverage, aggregation scope, lifecycle strata
success: evaluated application episodes, supporting/neutral/contradicting/inconclusive,
         rejected/invalid when material, affected/independent surfaces,
         evidence provenance clusters when material,
         first/last evaluated, coverage, aggregation scope, lifecycle strata
```

Split/merge/reclassification preserves lineage, reallocates rows, deduplicates underlying events, and prevents superseded parent plus children from being double-counted as one current total.

Do not pool materially different owner/invariant, failure mechanism, implementation class, language/runtime/toolchain, backend/precision, scale, lifecycle, or project regimes unless the generalized claim explicitly spans them and evidence supports that aggregation. Otherwise stratify or split.

A support count counts legitimate application episodes; an independence-sensitive claim additionally accounts for provenance clustering. Five application episodes selected by one policy using one copied realization may be five deployments but are not automatically five independent demonstrations of comparative superiority.

### 5.5 Memory temperature and evidence maturity

Default frequency floors inside declared aggregation scope:

```text
confirmed failures >=3 -> HOT
confirmed failures ==2 -> WARM
confirmed failures ==1 -> COLD only with adequate coverage; else UNASSESSED
qualified supporting application episodes >=3 -> HOT
==2 -> WARM
==1 -> COLD/UNASSESSED subject to coverage
```

A single event/application may receive evidence-backed impact promotion for demonstrated severity, breadth, cost, architectural criticality, or exceptional benefit. Preserve base classification, reason, and final temperature. Recency may affect attention/review, not erase counts.

Temperature is only salience. It is not authority, probability, acceptance, applicability, activation, maturity, or comparative ranking.

Evidence maturity follows Section 2.7 and must be reproducible from the bounded claim's declared required evidence obligations. `PROVEN` does not mean universal or permanent.

### 5.6 Active-summary salience

The active summary must not become a positive-success leaderboard. Current high-impact unresolved states - `REVIEW_REQUIRED`, material contradiction, unavailable warrant, expired high-risk notice, security/reliability hazard, authority-binding uncertainty, or unresolved overlapping guidance - receive consequence-aware visibility before lower-consequence optional positive guidance. Authority-bound obligations remain governed by their owners. Compact/group as needed, but do not hide material unresolved risk to satisfy a fixed positive/negative balance or aesthetic quota.

Positive guidance must reflect its actual claim strength: "works under X" may appear where supported; "prefer/default/best" appears only when the stronger comparative decision claim is warranted.

## 6. Workflow integration

### 6.1 Design/workplan

For a memory-triggering substantial task:

1. resolve accepted/base PEM from project integration/Git policy;
2. validate supported schema and compose any validated same-branch candidate overlay;
3. record the accepted-memory basis and overlay identity/state used for HAS;
4. determine governing D1-D4 parents/side constraints;
5. read active summary and perform bounded metadata-level applicability matching beyond Hot entries;
6. create HAS for every materially relevant current family/capability/notice surfaced or independently known;
7. inspect only relevant detail/evidence;
8. identify materially overlapping/conflicting guidance and record tradeoff/decision boundary or contested state;
9. build capability-transfer map where mature machinery is replaced;
10. identify new claims and required qualification;
11. preserve lower-salience mandatory constraints regardless of memory ranking.

Missing/partial PEM, absent dependency edge, stale index, stale applicability tag, or advanced reconciliation watermark cannot prove independence/non-applicability. Established projects adopting 6.3 may use bounded historical intake for the affected scope rather than mandatory global backfill, while keeping uncertainty explicit.

If the target accepted memory/overlay or governing owner materially advances before integration/closeout, reconcile the changed interval/surface and refresh affected HAS dispositions before relying on the earlier design decision.

### 6.2 Implementation and review

Implementation preserves actual owner-bound obligations and considers evidence-only learned capabilities as strong but replaceable design priors. Review challenges historical recurrence, lost optimization/reuse/parallelism, eager preparation, lost sensors, package drift, shadow authority, stale/invalid/counterevidenced guidance, applicability omissions, unsafe aggregation, broken bindings, unsupported schema, branch/base confusion, expired notices, causal overclaim, timestamp recurrence laundering, cross-repository ambiguity, derived-index omission, partial publication, untrusted-evidence instruction injection, semantic-ID drift/cyclic lineage, positive application inflation, observation rewriting, count-to-`PROVEN` promotion, works-to-best laundering, overlapping incompatible guidance, stale HAS basis, policy-induced fake independence, watermark false completeness, and context-scaling regression.

Review evaluates current owners and the assembled candidate. PEM is a high-information hypothesis index, not proof.

### 6.3 Impact closure and transitive PEM effects

When authority, concretization, evidence, family semantics, or a materially depended-on PEM entry changes, identify bounded materially dependent entries, preserve unaffected siblings with reason, mark affected entries appropriately, rerun/remap/reassess required evidence, recompute statistics/guidance, update applicability metadata, and close downstream PEM relations whose current meaning changes. No universal graph is required; repository search/bounded dependency views are sufficient when they establish the affected scope.

Changes to an owner cited by `AUTHORITY_BOUND` capability/current normative notice require reverse impact closure: confirm, remap, downgrade to `EVIDENCE_ONLY`, mark review-required/retired, or raise a real Challenge.

### 6.4 Closeout learning assessment

Every accepted material repair/rework/optimization/revert/restoration asks whether a known family recurred; a positive pattern gained supporting/neutral/contradicting/inconclusive/invalidating evidence; a genuinely new application episode occurred versus another surface/run of the same episode; evidence shares a material provenance cluster; a reusable discovery/capability emerged; evidence narrowed/retired/invalidated a lesson; maturity or comparative claim strength changed; overlapping guidance acquired a conflict/tradeoff boundary; coverage/aggregation/project scope changed; a binding became unhealthy; a notice expired; project/fork identity changed interpretation; causal attribution strength changed; a PEM dependency changed; HAS basis advanced; `reconciled_through` diverged from coverage; or schema/base/overlay reconciliation is needed.

Update PEM only when admission threshold is met or an existing entry materially changes. Ordinary fix chronology stays out of permanent memory.

## 7. Maintenance, branch reconciliation, and recovery

### 7.1 Update transaction and publication

A material update SHALL bind admissible evidence while preserving realization/observation separately from assessment; search bounded counterevidence when required; classify/reclassify family under semantic-identity rules; identify application episodes and provenance clusters; update ledger rows and superseding admissibility/assessment; recompute statistics; update coverage/aggregation/lifecycle/project scope without treating watermark as completeness; update claim-relative maturity/conflict, binding health, temperature, authority binding, comparative/positive-guidance eligibility, applicability metadata and active summary; preserve acyclic lineage/relations; disposition overlapping guidance; perform bounded downstream/reverse impact closure; run structural/security/schema checks; and publish one coherent logical-memory unit under Git policy.

Derived index regeneration may fail without corrupting canonical truth, but the index must then be explicitly stale/unavailable and cannot silently serve incomplete applicability results.

Update classes:

```text
EVIDENCE_APPEND - meaning/applicability unchanged; focused evidence/statistical checks
EVIDENCE_REASSESSMENT - prior realization/observation receives a new assessment/admissibility state; preserve observation and recompute affected current state
SEMANTIC_RECONCILIATION - claim/cause/semantic identity/lineage/scope/relations/applicability/authority binding/maturity/comparative guidance/split/merge/promotion/retirement changes; affected owner review + proportionate falsification
PEM_SCHEMA_OR_PROTOCOL_CHANGE - representation/routing/schema semantics change; protocol/workplan path
```

### 7.2 Branch/merge behavior and atomic publication

Branch-local PEM is a candidate overlay over the target accepted/base memory. A memory-triggering workplan/HAS records that basis. Before merge/rebase: inspect repository/concurrent state under Git owner; reconcile against target accepted memory; resolve provisional ID collisions; validate semantic identity/acyclic lineage; deduplicate shared/cherry-picked events; reconcile application episodes/provenance clusters; preserve underlying event and repair-acceptance lineage; re-evaluate applicability/admissibility/binding health after target changes; reconcile aggregation/project scope; update applicability predicates and relations; recompute statistics/temperature/maturity/guidance; refresh HAS if its basis changed materially; and rerun affected validation. Textual merge success is not semantic reconciliation.

A semantic change spanning root/partition/index surfaces is accepted only as one coherent assembled logical-memory publication state. Partial writes or mixed semantic revisions cannot replace the accepted/base memory. Internal memory files need not self-hash; external project integration/tree identity supplies atomic state identity.

No PEM rule authorizes force push, destructive rebase, history rewrite, or overwrite of unrelated/concurrent work.

### 7.3 Event-driven freshness

No daemon or periodic full scan is required. Reconciliation triggers include accepted authority/concretization change; evidence oracle/assessment invalidation; evidence retention/path change; revert/restoration; project/fork/scope change; schema migration/reader change; PEM activation for a relevant task; PEM semantic/evidence reconciliation; branch integration or accepted-memory-basis advance; and an otherwise justified maintenance audit.

A stale untouched Cold family need not be refreshed by time alone. A current recommendation whose warrant is unavailable/inadmissible/plausibly invalidated cannot remain unqualified merely because no scheduled audit ran.

### 7.4 Corruption, rollback, downgrade, and re-adoption

Malformed/unreadable/unsupported/corrupt PEM makes memory unavailable/partial for memory-dependent decisions; it does not block unrelated routes. Recover through project Git/document ownership, not an alternate memory authority.

Restored old PEM must be reconciled against current accepted state, schema, scope, owners, and evidence. Version-bound Protocol 6.2 leaves 6.3 PEM inert rather than deleting/reinterpreting it. Re-adopting 6.3 requires supported schema and reconciliation from the last covered accepted identity. Revert/restoration preserves historical events but reconciles current applicability, admissibility, authority binding, statistics, relations, maturity, and guidance where affected.

## 8. Context economy and scalability

Normal behavior must be structurally decoupled from raw historical-corpus growth:

```text
non-triggering route -> no substantive PEM/history load
triggering route -> root summary + cheapest sufficient metadata match
                  -> selected detail -> raw evidence only if needed
material update -> affected families + declared search scope
                  -> full corpus only for genuinely exhaustive/backfill/migration claims
```

Do not preload all family prose or all cold evidence. Family-count growth may increase search work, but use repository search/range/derived index rather than eager context. A stale/missing index falls back to canonical search or explicit uncertainty. Static bytes/tokens/routes/call counts are structural sensors only; claims about actual model latency, attention, cache behavior, productivity, or live memory use require live evidence for the stated harness/model/install regime.

## 9. Self-hosted SSDP migration/backfill

SSDP SHALL be the first qualified project-local PEM instance. Backfill from actual repository evidence, not examples in this workplan or agent recollection. Inspect semantic evolution, relevant archived workplans, Protocol 6.1/6.2 qualification/review, commit/patch episodes, replacement-bootstrap repair, cold-route requalification, static activation sensors, frozen-profile preservation, generated/package repairs, documentation-standard repairs, and materially relevant optimization/simplification history.

Candidate investigations include mature optimization loss, repeated computation, eager/cold-route contamination, accidental serialization, checkpoint/intermediate reuse loss, ownership leakage, generated/package drift, bootstrap identity drift, frozen-profile mutation, activation-sensor loss, wrapper accumulation, documentation source-chain drift, and diff-only review. Positive candidates include evidence-backed route-local lazy activation, provenance-valid artifact reuse, bounded independent parallelism, and direct owner-layer simplification.

Candidates are not pre-approved families. For each seeded family record semantic identity envelope, coverage, aggregation/project scope, lifecycle context, binding health, admissibility, claim-relative maturity, causal claim strength, material counterevidence, application episodes, and provenance clusters where material. Do not infer exhaustive coverage from `reconciled_through`; do not infer independent successes from one rollout/policy. Self-hosted PEM remains branch-candidate memory until actual project integration accepts it.

## 10. Finite representation census and preservation map

Before protocol-source mutation, Stage A SHALL create `qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md`. Inventory all current role/specialist entrypoints, shared references/templates, AGENTS/README/PORTABILITY/semantic dependencies/version, workflow-prompt source, profile/prompts/snapshots, schemas/renderers/help/status text, qualification/routing/package assets, workplan authority index, semantic history, archived workplans, `dist/`, generated snapshots, and frozen 5.16/6.0/6.1/6.2 resources. Classify each `refactor`, `route-only`, `new`, `generated`, `frozen/historical`, or `intentionally unchanged with reason`.

Independently reconstruct T01-T39 from accepted 6.2; do not inherit labels as proof. Append collision-free 6.3 preservation hypotheses with these meanings:

```text
T40 authority/current-owner vs non-authoritative memory separation
T41 compact active PEM representation
T42 stable family identity and lineage
T43 exact durable evidence binding
T44 ledger-derived recurrence/application statistics
T45 evidence-backed positive patterns and tradeoffs
T46 hypothesis/maturity/applicability separation
T47 reproducible temperature and explicit impact override
T48 coverage state; no absence inference from incomplete memory
T49 semantic family-membership discipline
T50 first-local-defect/admission economy
T51 HAS for materially memory-relevant work
T52 mechanism-to-capability transfer
T53 owner-backed promotion into invariants/sensors
T54 material closeout learning assessment
T55 quantitative effect/envelope preservation
T56 contradiction/retirement without erasure
T57 evidence applicability/staleness/bounded invalidation
T58 independence/common-mode risk
T59 active-summary progressive disclosure/cold reachability
T60 project-local PEM vs generic package/template separation
T61 one logical canonical memory; derived indexes subordinate; optional partition lossless
T62 6.3 bootstrap/profile/recovery/version staging
T63 frozen prior profiles/resources
T64 source/generated/package parity and exact-ref fallback
T65 static-vs-live claim discipline
T66 Protocol 7 inheritance/current-lifecycle reconciliation
T67 human-facing background/terminology/abbreviation completeness
T68 independent assembled-candidate qualification/Review
T69 anti-scope-laundering/lower-salience mandatory preservation
T70 no recursive summary/evidence laundering
T71 capability authority binding; PEM cannot mint invariants
T72 self-reference-safe routine updates
T73 balanced positive supporting/neutral/contradicting/inconclusive evidence
T74 descriptive count vs rate/probability
T75 memory temperature vs activation state
T76 accepted/base vs branch-candidate lifecycle/merge reconciliation
T77 stable accepted IDs; collision-safe provisional IDs; no reuse
T78 security/trust/privacy persistence
T79 owner-responsible learning assessment/update classes
T80 cross-domain D1-D4/specialist applicability without universal activation
T81 owner deduplication after doctrine promotion
T82 occurrence/application lifecycle context
T83 pre-admission counterevidence/anti-selection bias
T84 applicability-led HAS independent of temperature/summary presence
T85 aggregation scope/cross-regime stratification
T86 evidence/authority binding-health
T87 reverse owner-impact closure for authority-bound PEM
T88 failure-family safe/disconfirming evidence
T89 current-notice expiry/review
T90 matched comparator/uncertainty for quantitative claims
T91 positive-guidance eligibility under conflict/unhealthy evidence
T92 active workplan current-state representation; no review replay
T93 PEM schema compatibility/migration/unknown-schema fail-safe
T94 accepted memory basis distinct from default/latest/self-declaration
T95 PEM corruption/rollback/downgrade/re-adoption
T96 evidence admissibility/retraction and recomputation
T97 unresolved assessment disagreement without vote/latest-editor laundering
T98 context/maintenance scaling independent of raw-history growth
T99 logical canonical partitioning and stale-index fallback
T100 fork/copy/cross-project provenance/local-count separation
T101 Git ownership for branch/merge/self-reference/history behavior
T102 revert/restoration impact closure
T103 typed PEM relations, non-recursive warrants, transitive impact closure
T104 atomic logical-memory publication across root/partition/index surfaces
T105 accepted-base plus explicit branch-candidate overlay composition
T106 applicability metadata co-evolution; no stale-match false negatives
T107 observation/association/causal-attribution claim-strength discipline
T108 recurrence chronology from accepted repair/event lineage, not timestamps
T109 cross-repository evidence includes unambiguous source identity
T110 active-summary salience preserves current high-impact unresolved state
T111 untrusted evidence content remains data, not instruction/tool authorization
T112 accepted-family semantic identity envelope and acyclic unambiguous lineage
T113 causal positive application-episode counting separated from affected-surface breadth
T114 immutable realization/observation provenance with superseding assessment/correction lineage
T115 claim-relative evidence maturity; no count/temperature/reviewer-vote promotion
T116 absolute success distinct from comparative/preferred/default guidance
T117 overlapping current guidance conflict/tradeoff disposition
T118 HAS pins accepted-memory/overlay basis and reconciles material late basis advance
T119 evidence provenance clusters preserve policy/implementation/common-dependence limits
T120 reconciled-through watermark distinct from historical-coverage completeness
```

For every materially changed obligation, census records old owner, new owner, obligation, preservation/generalization relation, discriminating oracle/evidence, and `PRESERVED` or `BLOCKING` disposition. These rows are evidence, not authority.

## 11. Protocol 6.3 bootstrap, profile, package, and recovery lifecycle

Preserve the repaired 6.2 self-reference discipline.

1. Complete and validate self-reference-safe 6.3 canonical source, including PEM doctrine/template, version/navigation, and package closure.
2. Create immutable 6.3 public-source bootstrap only after source regression, canonical package build, standalone package/link validation, and routing reachability pass.
3. Publish that exact bootstrap only from a later semantic-candidate/publication commit. Never use `main`, latest, semantic-version guessing, or future recovery identity as fallback.
4. Create distinct `ssdp-protocol-6.3` profile/snapshot; profile schema and PEM schema are separate contracts. Do not mutate 5.16/6.0/6.1/6.2 resources.
5. Bind qualification to one immutable semantic candidate. Later evidence/generated/lifecycle commits contain no hidden canonical semantic mutation; otherwise affected qualification reopens.
6. Regenerate `dist/` and orchestrator descendants from canonical source and validate parity, package closure, profile identity/topology, exact fallback, and closest supported consumer ingestion. Generic packages contain PEM doctrine/template/reader semantics, never live project PEM.
7. After semantic qualification and independent Review PASS, choose immutable 6.3 recovery containing candidate and required decision evidence through ancestry.
8. Publish `6.3.0 -> <exact recovery>` only in a later mapping commit, regenerate mapping-bearing descendants, and rerun targeted recovery/parity/package/Core acceptance.
9. Reconcile semantic evolution, workplan authority index, navigation/portability, self-hosted PEM accepted basis, final HAS basis, and Protocol 7 inheritance representation. Protocol 7 D3 architecture remains unchanged unless separately reopened.
10. Archive workplan only after current 6.3 semantics live at canonical owners and impact closure is complete.

## 12. Qualification obligations

Run complete affected repository/package/orchestrator regression, all 115 accepted Protocol 6.2 semantic scenarios against 6.3, all affected prior requalifications, the four inherited 6.2 Challenge falsifications, focused Q63 cases below, generated/profile/package checks, and independent assembled-candidate Review.

```text
Q63-01 complete 6.2/T01-T39 no-loss preservation
Q63-02 finite representation census and transformation closure
Q63-03 authority/evidence/PEM separation
Q63-04 conditional activation and cold-route behavior
Q63-05 missing/partial memory cannot prove absence/non-applicability
Q63-06 durable non-recursive evidence binding
Q63-07 stale evidence in both polarities and bounded invalidation
Q63-08 evidence independence/common-mode risk/visible contradiction
Q63-09 semantic failure-family membership, not textual similarity
Q63-10 one causal episode/many symptoms counts once
Q63-11 genuine recurrence after accepted repair increments correctly
Q63-12 split/merge lineage, deduplication, recomputed totals
Q63-13 coverage-sensitive reproducible temperature
Q63-14 importance is not authority/pass threshold
Q63-15 positive promotion requires suitable evidence and governing constraints
Q63-16 quantitative effect survives compaction
Q63-17 complexity claim discipline
Q63-18 capability transfer permits simpler/new mechanism without losing owner-bound requirement
Q63-19 first-local-defect economy
Q63-20 invalidation/contradiction/retirement retains history and refreshes guidance
Q63-21 lossless active-summary compaction
Q63-22 no repeated-history/full-corpus scan on normal routes
Q63-23 static-vs-live claim discipline
Q63-24 project-local PEM excluded from generic package/profile
Q63-25 exact immutable 6.3 public fallback
Q63-26 frozen 5.16/6.0/6.1/6.2 integrity
Q63-27 final generated/package/profile/Core acceptance
Q63-28 self-hosted backfill statistics independently reconstructed
Q63-29 material closeout update; non-material local repair creates no memory noise
Q63-30 bootstrap/recovery/version/Protocol-7 lifecycle separation
Q63-31 evidence-only capability cannot become mandatory through PEM
Q63-32 routine PEM update is self-reference-safe
Q63-33 supporting count cannot hide neutral/contradicting/inconclusive outcomes
Q63-34 counts cannot masquerade as rates/probabilities
Q63-35 temperature distinct from current activation/applicability
Q63-36 concurrent branch/ID/merge/cherry-pick reconciliation
Q63-37 sensitive/private evidence preservation rules
Q63-38 update-class and owner responsibility; documentation cannot self-promote findings
Q63-39 bounded cross-domain D1-D4/specialist applicability
Q63-40 lesson promoted to current doctrine does not remain competing PEM rule
Q63-41 lifecycle context prevents development-to-production incidence laundering
Q63-42 pre-admission counterevidence search catches favorable-history cherry-pick
Q63-43 HAS surfaces materially relevant non-Hot entry
Q63-44 incompatible regimes are stratified/split rather than pooled
Q63-45 broken material binding degrades current guidance
Q63-46 current-owner change closes reverse authority-binding impact
Q63-47 safe/disconfirming evidence narrows overbroad failure family
Q63-48 notice expiry removes unqualified active guidance
Q63-49 quantitative comparator/uncertainty integrity
Q63-50 contested/unhealthy success not phrased as "what works"
Q63-51 active workplan is current-state contract; review chronology stays cold
Q63-52 schema compatibility/migration and unknown-schema fail-safe
Q63-53 accepted memory basis is project-governed, not default/latest/self-declared
Q63-54 corruption/restored-old-memory/downgrade/re-adoption behavior
Q63-55 invalidated evidence is withdrawn from current derived support
Q63-56 conflicting assessment cannot be vote/latest-editor resolved
Q63-57 active-context/maintenance scaling independent of raw cold-history growth
Q63-58 logical canonical partitioning and stale-index fallback
Q63-59 fork/cross-project provenance and local-count separation
Q63-60 Git owner controls repository mutation and semantic merge does not authorize rewrite
Q63-61 revert/restoration preserves history and reconciles current meaning
Q63-62 typed PEM relation endpoints remain independently warranted; upstream change triggers bounded downstream closure
Q63-63 root/partition/index semantic publication is coherent; mixed revisions fail
Q63-64 same-branch candidate overlay composes explicitly over accepted base without self-ratification or silent deletion
Q63-65 applicability metadata co-evolves with family semantics; stale tag cannot hide a relevant family
Q63-66 assembled-outcome evidence cannot be promoted to mechanism-specific causality without discriminating evidence
Q63-67 recurrence-after-repair follows accepted project/causal lineage, not misleading timestamps/rebase order
Q63-68 non-local evidence binding requires unambiguous source repository/project identity
Q63-69 active summary preserves current high-impact unresolved risk despite abundant positive patterns
Q63-70 untrusted instruction-like evidence remains data and cannot authorize tools/actions or change instruction precedence
Q63-71 accepted family ID retains semantic identity envelope; split/merge/supersession lineage is acyclic and current disposition unambiguous
Q63-72 one coordinated positive intervention across many surfaces counts as one application episode; later independent application increments once
Q63-73 later invalidation changes assessment/admissibility without rewriting historical realization/observation; clerical correction preserves provenance
Q63-74 three supporting rows cannot auto-promote PROVEN while a required independence/owner/comparator/applicability obligation remains open
Q63-75 successful technique cannot become preferred/best/default overall without comparative warrant/current owner priority
Q63-76 overlapping individually supported patterns with incompatible advice expose regime/tradeoff/owner priority or remain contested
Q63-77 HAS records accepted-memory/overlay basis and reconciles material P1-to-P2 advance before closeout
Q63-78 shared PEM policy/copied implementation/common harness remains visible as a provenance cluster and cannot masquerade as independent comparative proof
Q63-79 reconciled-through may advance while coverage remains PARTIAL; watermark cannot establish exhaustive history or absence
```

Each Q63 case SHALL contain a negative/counterfactual fixture that would fail if the claimed distinction were omitted; word-presence checks are insufficient.

Qualification realization rule: a result-table row or prose assertion is not itself evidence that a Q63/F63 case executed. For every mechanically decidable obligation, bind the case to an executable discriminator that accepts the valid fixture and rejects the counterfactual. For obligations whose decisive semantics are necessarily human/owner assessed, bind the case to a paired valid/counterfactual artifact and a recorded independent assessment showing the discriminator. The qualification record SHALL map every Q63/F63 identifier to its realized oracle/evidence. Missing, skipped, doctrine-only, or non-discriminating realizations are `NOT RUN`/`NO-PASS`, never PASS.

## 13. Falsification obligations

Retain the four Protocol 6.2 Challenge passes unchanged in semantic purpose:

1. **Loss** - attempt to remove a distinction needed for a future decision.
2. **Scope/materiality laundering** - attempt to pass by shrinking the governed/affected scope.
3. **Priority inversion** - attempt to let high-salience memory erase lower-salience mandatory current constraints or material tradeoffs.
4. **False compaction** - attempt to replace genuine progressive disclosure with recursive summaries, incomplete indexes, eager loading, collapsed provenance/lineage, or hidden duplicate authority.

Run the following 6.3 adversarial cases:

```text
F63-A speculation laundering
F63-B statistical inflation
F63-C family overgeneralization
F63-D incomplete-history false Cold
F63-E cargo-cult positive pattern
F63-F summary/evidence recursion
F63-G stale-green/stale-red laundering
F63-H common-mode fake independence
F63-I architectural ossification
F63-J history-compaction loss
F63-K false quantitative generalization
F63-L eager memory regression
F63-M project-memory package contamination
F63-N shadow capability authority
F63-O routine self-SHA recursion
F63-P positive survivor bias after admission
F63-Q pseudo-statistical risk/rate
F63-R temperature/activation conflation
F63-S branch memory overwrite
F63-T accepted-ID reuse
F63-U sensitive-evidence laundering
F63-V documentation self-promotion
F63-W generic-doctrine duplication
F63-X lifecycle-incidence laundering
F63-Y pre-admission favorable-history cherry-pick
F63-Z Hot-summary applicability trap
F63-AA cross-regime pooling
F63-AB broken-warrant persistence
F63-AC authority-binding drift
F63-AD failure-family safe-counterexample suppression
F63-AE expired-notice persistence
F63-AF benchmark confounding
F63-AG contested pattern presented as "what works"
F63-AH active-workplan amendment replay
F63-AI unknown-schema reinterpretation
F63-AJ default/latest memory laundering
F63-AK stale restored-memory laundering
F63-AL invalid-evidence persistence in current statistics
F63-AM review-vote/latest-editor truth
F63-AN cold-history scaling regression
F63-AO canonical-memory representation ossification/duplicate authority
F63-AP fork-count contamination
F63-AQ stale-index omission
F63-AR revert erases/strands learning
F63-AS recursive PEM-to-PEM warrant
F63-AT half-published root/partition state
F63-AU accepted-base/candidate-overlay confusion
F63-AV stale applicability-tag false negative
F63-AW post-hoc causal laundering
F63-AX timestamp-based recurrence laundering
F63-AY bare cross-repository evidence identity
F63-AZ positive-guidance salience starvation of unresolved risk
F63-BA evidence-content instruction injection
F63-BB semantic-ID drift or lineage cycle
F63-BC one-intervention/many-surface positive-count inflation
F63-BD historical observation rewritten to match later assessment
F63-BE count/temperature/reviewer-vote to PROVEN laundering
F63-BF works-to-best/preferred/default laundering
F63-BG overlapping incompatible positive guidance without decision boundary
F63-BH moving accepted-memory/HAS basis without reconciliation
F63-BI policy/implementation/common-harness dependence presented as independent comparative proof
F63-BJ reconciled-through watermark used as false coverage completeness
```

A required case that does not execute is not PASS.

## 14. Implementation stages

### Stage A - baseline and no-loss map
Reconfirm accepted 6.2 identities; build finite representation census; independently reproduce T01-T39; map actual owners/consumers; append T40-T120 or collision-free successors; classify prior evidence applicability. **Gate:** no source mutation until finite no-loss scope is adequate.

### Stage B - canonical doctrine and schema
Add the smallest justified `source/shared/references/project-engineering-memory.md` owner or prove existing owner sufficient. Implement schema, families, semantic identity/acyclic lineage, relations, evidence/admissibility/observation-assessment preservation, aggregation, causality, application episodes/provenance clusters, claim-relative maturity, comparative/overlap guidance, statistics, temperature/salience, scope/provenance, branch overlay, logical publication, trust handling, notices, and optional cold partition semantics. Update existing concern owners only with their local consequences/routes. **Gate:** no duplicate owner, shadow authority, recursive warrant, unknown-schema laundering, duplicate canonical memory, semantic-ID drift, application inflation, observation rewrite, maturity laundering, or unsupported comparative guidance.

### Stage C - routing and workflow
Add visible conditional routes from relevant D1-D4/specialist/workflow entrypoints; implement accepted-base plus candidate overlay, bounded applicability matching/HAS with basis pinning/reconciliation, capability transfer, overlapping-guidance disposition, missing/partial/corrupt memory behavior, reverse/transitive impact, applicability co-evolution, expiry, binding-health/admissibility checks, revert/restoration, causal-claim distinction, and closeout responsibility. **Gate:** first-local, Hot-irrelevant, Cold-material, non-Hot-HAS, stale-tag, overlay, moving-HAS-basis, conflicting-guidance, expired-notice, unsupported-schema, and ordinary-route cases behave correctly.

### Stage D - validation and self-hosted backfill
Extend existing validators rather than create parallel compliance machinery. Validate schema, IDs/semantic envelopes/acyclic lineage, logical-publication coherence, relations, evidence resolution/source identity/admissibility, immutable observation versus assessment, derived counts/application episodes, provenance clusters, claim maturity, comparative guidance, recurrence lineage, aggregation/project scope, counterevidence, coverage/watermark distinction, temperature/activation, salience, positive eligibility, authority binding, branch overlay, HAS basis, Git state, security/trust, notice expiry, partition/index parity, applicability metadata, and active-summary integrity. Build SSDP PEM from real evidence. **Gate:** independent reconstruction and counterevidence checks pass; no cross-regime/project pooling, recursive warrant, half-publication, causal overclaim, positive-count inflation, false independence, works-to-best laundering, or cold-history load regression.

### Stage E - bootstrap/profile/candidate/generated descendants
Complete self-reference-safe source, validate, create immutable public bootstrap, publish exact bootstrap later, create distinct 6.3 profile/snapshot, keep old resources frozen, regenerate/package, and bind one immutable semantic candidate. **Gate:** exact self-reference-safe bootstrap/candidate/profile/package separation.

A canonical 6.3 semantic repair made after publication of a public-source bootstrap invalidates that bootstrap for current 6.3 fallback whenever the immutable snapshot lacks the repaired required semantics. Preserve the old ref as historical evidence, choose a new already-existing validated replacement bootstrap only after repaired source/package/profile readiness passes, publish the replacement exact ref from a later descendant, and rerun exact-ref bootstrap requalification. Never retain a stale bootstrap merely to avoid remapping generated descendants.

### Stage F - qualification and independent Review
Run full affected regression, all 115 6.2 scenarios, affected prior requalifications, Q63-01 through Q63-79, F63-A through F63-BJ, and the four inherited Challenge passes. Use static activation/context sensors without overclaiming live performance. Prepare snapshot-complete handoff and perform independent assembled-candidate Protocol/D3 Review. **Gate:** no missing check, unresolved preservation row, hidden red/unavailable evidence, shadow authority, invalid count, semantic-ID/lineage defect, stale applicability, stale HAS basis, partial publication, causal overclaim, observation rewrite, maturity/comparative-claim laundering, provenance fake-independence, false coverage watermark, trust-boundary defect, or package/profile drift.

If independent Review falsifies a qualification oracle or demonstrates that a recorded PASS accepts an invalid counterfactual, the affected qualification result is historical evidence only and cannot remain Stage-F acceptance. Repair the owner/oracle first, bind a replacement semantic candidate, then execute a fresh assembled-candidate Stage F. Reuse of demonstrably unaffected underlying realizations is allowed only when applicability is explicitly preserved; the new Stage-F decision must still account for all 115 inherited scenarios, all Q63/F63 cases, the four Challenge passes, affected prior requalifications, and generated/package/profile/Core acceptance against the replacement candidate.

### Stage G - recovery and closeout
After Stage-F PASS choose immutable recovery, later publish mapping, regenerate mapping-bearing descendants, rerun targeted recovery/parity/package/Core acceptance, reconcile semantic evolution/authority index/navigation/self-hosted accepted PEM basis/final HAS basis/Protocol-7 inheritance, and archive only after current doctrine resides at owners. No `main` cutover without separate authorization.

## 15. Independent-review handoff

Create `qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md` only after implementation/qualification readiness. Bind exact 6.2 parent identities; 6.3 bootstrap/candidate; complete preservation census/map; supported PEM schema; self-hosted PEM scope/coverage/aggregation; accepted base and candidate overlay; workplan/HAS basis and late-basis reconciliation; logical publication state; semantic identity/acyclic lineage; typed relation/transitive-impact state; applicability metadata; supporting/disconfirming/invalidated evidence; immutable observation/superseding assessment state; application episodes/provenance clusters; claim-relative maturity/comparative-guidance basis; causal-attribution basis; recurrence lineage; non-local source identities; binding health/admissibility; salience state; static/live evidence with correct claim scope; generated/package/profile/frozen-resource evidence; candidate-to-evidence descendant range; known red/unavailable/contested observations; and security-sensitive evidence handling.

Reviewer independently reconstructs governing semantics and attempts falsification. It MUST inspect the assembled candidate rather than PR diff, implementer summary, preservation labels, or green statuses alone. It samples positive claims for omitted counterevidence, application-count inflation, common provenance and works-to-preference laundering; failure families for overbroad causes and semantic-ID drift; relations for recursive warrant/transitive staleness/lineage cycles; recurrence for timestamp laundering; non-Hot applicability; branch overlays/HAS basis changes; root/partition coherence; causal claims; cross-repository evidence identity; unresolved-risk salience; watermark/coverage distinction; and trust-boundary handling.

## 16. PASS / NO-PASS

PASS requires: complete 6.2 preservation; all new T rows closed; authority/evidence separation; one coherent logical project-local PEM; valid schema and accepted-base semantics; explicit branch overlay; evidence-backed balanced positive/negative learning; stable semantic identity with acyclic lineage; immutable observation plus superseding assessment; causal application-episode statistics with provenance dependence visible; claim-relative maturity; comparative guidance no stronger than its warrant; conflicting guidance bounded/contested; admissibility-driven statistics; honest coverage/watermark/aggregation/lifecycle/project scope; non-recursive typed relations and bounded transitive impact; claim-strength/causal discipline; genuine recurrence lineage; healthy source-identified bindings; applicability-led HAS with accepted-memory-basis reconciliation; consequence-aware salience; no shadow authority; safe rollback/revert/fork behavior; bounded context/maintenance cost; lossless optional partitioning/index fallback; untrusted evidence treated as data; Git-owner control; all inherited/new qualification and falsification passing; exact 6.3 bootstrap/recovery/profile/package lifecycle; frozen old resources; bounded Protocol 7 reconciliation; and independent Review with no genuine blocker/Serious Challenge.

NO-PASS includes any material violation of those requirements, especially: loss of accepted 6.2 semantics; memory/evidence becoming authority; cherry-picked positive learning; overbroad negative learning; semantic-ID reuse/cyclic lineage; one intervention counted as many positive applications; invalid/stale evidence contributing current support; historical observation rewritten to fit later interpretation; causal attribution stronger than evidence; fabricated recurrence from timestamps/copies; correlated/provenance-cluster evidence called independent; count/temperature/vote promoted to PROVEN; absolute success converted to preferred/best/default without comparative warrant; overlapping incompatible guidance left unconditional; probability claims without denominator; incompatible aggregation; stale applicability hiding a relevant lesson; stale HAS after accepted-memory-basis advance; `reconciled_through` used as coverage proof; recursive PEM warrant; half-published logical memory; branch candidate mistaken for accepted memory; silent accepted-entry deletion; source-ambiguous cross-repository warrant; unresolved high-impact state crowded out by positive guidance; instruction-like evidence treated as executable instruction/authorization; unsupported schema interpretation; stale restored PEM; destructive Git behavior authorized by PEM; eager history activation; package/live-PEM contamination; frozen/profile/package drift; semantic mutation after candidate without requalification; diff-only Review; premature recovery mapping; or silent Protocol 7 architecture change.

## 17. Reopen and repair rule

If implementation or independent Review finds a genuine blocker, route to the earliest owning D1/D2/D3/D4 or concern layer; reopen this workplan only when its cycle contract must change; give precise owner-layer repair instructions; prefer removal/narrowing/rewiring/consolidation/re-derivation over compensating wrappers; rerun only affected evidence while preserving demonstrably unaffected admissible evidence and historical observations; recompute affected PEM state; preserve semantic-ID/application/provenance integrity; and use the Git owner for repository/history operations. Raise Serious Challenge only when accepted governing authority may itself be defective.

### 17.1 Completed Protocol 6.3 implementation-review repair contract

The Protocol 6.2-governed assembled-candidate Review of branch state `100cbde296de6c1a8db14151f34cfacfebc90eb3` was **NO-PASS** with **no Serious Challenge** to accepted Protocol 6.2 authority or the Protocol 6.3 D3 design contract. That Review opened D4R2, D5R2, E2, and F2 while preserving the repaired D1 binding-health, D2 logical-publication, D3 observation-identity, D6 typed-notice, and D7 HAS/template behavior.

Those implementation-context repairs are now closed by immutable semantic candidate `3bbbdfa8120646d76336c7b916e6a891c9ed38f2` and fresh F2 evidence `6fc26ce374b5346495782871d5d7241de5b90071` / `qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F2.md`. D4R2 binds accepted-repair evidence to the exact repair subject, explicit accepted state, and accepting owner; D5R2 derives replication and independent-replication obligations for every schema-1 `PROVEN SUCCESS_PATTERN` rather than trusting claimant omission. E2 publishes self-reference-safe bootstrap `e12572c021087308570abfa41657a910c6896457` only through later mapping descendant `e6a8c12f065c3d25a41da804c129d6bc0a4f7b50`. F2 freshly accounts for all 260 required inherited/Q63/F63/Challenge cases and reruns the assembled source/package/profile/Core/frozen-resource gates.

Earlier 6.3 candidates, bootstraps, mappings, and Stage-F result sets remain immutable historical evidence only. They remain useful falsification fixtures but are not current acceptance anchors. The repair specifications below are retained as the auditable contract that the current candidate was required to satisfy; they are no longer open implementation blockers. Stage G remains blocked on the fresh independent assembled-candidate Review and the separate recovery lifecycle.

#### Repair D4R2 - acceptance evidence must establish acceptance of the same repair

Owner: convergence/evidence semantics concretized by the existing PEM validator and Git owner. Extend the existing recurrence path; do not add an acceptance registry, daemon, shadow manifest, or wrapper.

- Preserve the real-prior-occurrence, resolvable-repair, later-independent-event, lineage-order, explicit-independence, and alias/patch-equivalence guards.
- A healthy descendant evidence route plus Git ancestry is not proof that the repair was accepted. Each Git-native repair-acceptance route must resolve to immutable content carrying a typed acceptance record that binds the exact `repair_identity`, has state `ACCEPTED`, and names a non-empty governing/accepting owner. Its revision must lie after/at the repair and before the later recurrence event.
- The PEM row references the durable acceptance record; it cannot self-attest acceptance by naming an arbitrary descendant commit/file.
- Reject an unrelated descendant route, an acceptance record for a different repair, missing/ambiguous acceptance state, missing owner, reversed order, and copied/rebased/cherry-picked alias recurrence.
- Non-Git recurrence requires an equivalent durable acceptance relation binding the same repair identity plus durable verified order evidence; prose chronology or a self-declared state alone cannot increment recurrence.

**Gate D4R2:** Q63-11/Q63-67/Q63-72 and F63-AX/F63-BC, including unrelated-descendant and wrong-subject counterfactuals, discriminate correctly.

#### Repair D5R2 - `PROVEN` success-pattern independence cannot be waived by omission

Owner: evidence/testing maturity semantics concretized by the existing PEM validator. Strengthen the existing typed obligation model rather than adding a parallel mechanism.

- In schema-1 Protocol 6.3, a `PROVEN` `SUCCESS_PATTERN` is a generalized transferable engineering claim. Derive `replication` and `independent_replication` from that family/claim class in addition to claim support, applicability, and contradiction closure; independent replication requires at least two admissible supporting provenance clusters.
- Claimant fields such as `requires_replication`, `requires_independence`, or `provenance_independence_required` may be redundant assertions but cannot waive derived obligations when omitted or false.
- Comparative guidance continues to derive comparator plus comparative-independence or accepted-owner-priority obligations. Unknown/arbitrary CLOSED obligations cannot substitute for required classes.
- Multiple supporting episodes from one provenance cluster cannot establish a `PROVEN` success pattern even when all `requires_*` flags are omitted.

**Gate D5R2:** Q63-08/Q63-15/Q63-49/Q63-74/Q63-75/Q63-78 and F63-H/F63-AF/F63-BE/F63-BF/F63-BI include a direct omission counterfactual.

#### Repair E2 - replacement bootstrap after repaired readiness

After D4R2/D5R2 source, tests, doctrine, self-hosted PEM, generated descendants, full affected regression, package validation, profile/snapshot parity, Core acceptance, frozen-prior-resource integrity, and whitespace/clean-tree checks pass, choose an already-existing immutable repaired source snapshot. Publish that exact snapshot only from a later descendant mapping commit, rerun exact-ref public realization, regenerate 6.3 descendants, and keep every earlier 6.3 bootstrap/candidate as historical negative fixtures.

**Gate E2:** Q63-25/Q63-26/Q63-27/Q63-30 and bootstrap affected requalification pass against the new exact mapping with frozen 5.16/6.0/6.1/6.2 bytes unchanged.

#### Repair F2 - rebuild Stage F on the new assembled candidate

Produce a fresh mechanically auditable per-case map for every Q63-01..Q63-79, F63-A..F63-BJ, and all four inherited Challenge passes. Bind the D4R2 unrelated-descendant/wrong-subject acceptance counterfactuals and the D5R2 omitted-`requires_*` counterfactual explicitly. Run all 115 inherited 6.2 scenarios, affected 6.1/6.2 requalifications, source/PEM/security regression, static activation sensors, new-bootstrap exact-ref realization, frozen-resource checks, build/dist validation, profile/snapshot parity, and Orchestrator Core acceptance. Refresh preservation census, sensors, implementation state, self-hosted PEM/HAS as affected, and independent-review handoff to the new identities. Then perform a fresh independent assembled-candidate Review.

**Gate F2:** no missing/skipped/doctrine-only/non-discriminating claimed PASS; no known false-pass oracle; fresh independent Review finds no blocker or Serious Challenge.

#### Repair sequencing and preservation

```text
D4R2 owner repair + direct counterfactuals
 -> D5R2 derived obligation repair + omission counterfactual
 -> preserve/reverify D1/D2/D3/D6/D7
 -> full affected regression/build/package/profile/Core/frozen checks
 -> E2 immutable replacement bootstrap + later exact mapping
 -> regenerate descendants and bind one new semantic candidate
 -> F2 fresh complete Stage-F qualification and lifecycle-evidence refresh
 -> fresh independent assembled-candidate Review
 -> only then Stage G
```

Do not introduce a second PEM database, resolver daemon, acceptance registry, qualification wrapper, shadow manifest, package-side patch, or HAS adapter. Preserve accepted 6.2 doctrine, frozen resources, repaired D1/D2/D3/D6/D7 behavior, and admissible historical observations.


## 18. Current design closure state

The fresh independent assembled-candidate Review of semantic candidate `3bbbdfa8120646d76336c7b916e6a891c9ed38f2` is **NO-PASS** with **no Serious Challenge** to accepted Protocol 6.2 authority or the Protocol 6.3 D3 design. The Review found one shared D4 false-pass family: owner-bearing records can establish acceptance or normative force from structurally healthy evidence plus a self-declared non-empty owner without binding that owner to accepted project authority.

The prior D4R2/D5R2/E2/F2 repair round remains useful historical evidence. D5R2 and the previously repaired D1/D2/D3/D6/D7 behaviors remain preserved unless affected evidence proves otherwise. However, D4R2 is incomplete at the real-owner boundary, and because the repair changes canonical 6.3 semantics the prior semantic candidate `3bbbdfa8120646d76336c7b916e6a891c9ed38f2`, public bootstrap `e12572c021087308570abfa41657a910c6896457`, mapping `e6a8c12f065c3d25a41da804c129d6bc0a4f7b50`, and F2 qualification are no longer current acceptance anchors. D4R3, E3, and F3 are reopened. Stage G, recovery, accepted-current status, workplan archive, and `main` cutover remain blocked.

### 18.1 Repair D4R3 - authority and repair acceptance require accepted-state governing-owner binding

Owner: existing PEM evidence/authority-binding concretization plus Git accepted-base semantics. Strengthen the existing validator and schema-1 representation; do **not** add an authority registry, acceptance registry, daemon, shadow manifest, package-side patch, or parallel ownership database.

- Any owner field relied upon to create normative force or accepted-repair recurrence is a durable owner binding, not descriptive prose. `AUTHORITY_BOUND` families, normative notices, comparative owner-priority decisions, and typed repair-acceptance records must route to an immutable owner artifact rather than accepting an arbitrary non-empty label.
- Mechanical `HEALTHY` current-owner validation is grounded in the exact project-governed `accepted_base.project_state`. The owner route must resolve in the local accepted lineage, precede or equal that accepted state, and resolve to the same owner content at the accepted state. A candidate-only owner, missing owner, owner path removed or changed since the cited revision, non-local owner with no source-specific resolver, or unresolvable accepted base cannot silently become healthy current authority; current normative use becomes `REVIEW_REQUIRED`/invalid until independently resolved.
- `AUTHORITY_BOUND` families additionally carry explicit authority evidence for the capability/claim. At least one authority-evidence route must be accepted-state-bound; ordinary observational evidence may remain candidate/historical evidence and cannot substitute for this authority relation.
- Comparative owner priority must bind both the immutable owner and the evidence for the owner's explicit decision to accepted project state. A branch-local decision cannot manufacture `PREFERRED`/`DEFAULT`/`BEST` authority.
- A normative current notice must bind its owner and normative evidence to accepted project state; otherwise it cannot remain an unqualified normative/current notice. Non-authoritative notices retain the existing evidence lifecycle.
- A recurrence repair-acceptance artifact must itself be contained by accepted project state. Its typed record must still bind the exact repair, `state: ACCEPTED`, and an immutable owner route whose owner content is the same at the acceptance event. An arbitrary later descendant, branch-only acceptance file, free-text owner, wrong repair subject, owner-content drift, reversed chronology, or copied/rebased/cherry-picked alias cannot increment recurrence.
- The structural validator establishes immutable accepted-state provenance and fails safe where it cannot. Semantic Review still independently verifies that the cited accepted owner is the **correct** governing owner for the exact claim; accepted-state containment is not permission to replace D1-D4 reasoning with filename matching.
- Preserve candidate observational evidence, historical observations, provenance clusters, family identities, D5R2 maturity rules, and all unaffected 6.2/6.3 semantics. Route owner changes through bounded reverse impact closure rather than silently rewriting authority-bearing records.

**Gate D4R3:** direct executable counterfactuals reject (1) branch-only repair acceptance, (2) free-text or candidate-only authority owner, (3) accepted owner whose content changed before the accepted base, (4) missing/unaccepted authority evidence, (5) candidate-only comparative owner decision, and (6) candidate-only normative notice authority. Re-run affected Q63-03/Q63-11/Q63-31/Q63-45/Q63-46/Q63-67/Q63-75 and corresponding F63 authority/recurrence/adversarial cases. Preserve still-applicable F2 evidence only with explicit applicability; do not label reused evidence as freshly executed.

### 18.2 Repair E3 - replace the invalidated public bootstrap after D4R3

The D4R3 semantic repair invalidates `e12572c021087308570abfa41657a910c6896457` as the current 6.3 fallback. Preserve it as historical evidence. Before choosing a replacement, restore the no-current-bootstrap sentinel in canonical source and generated descendants, complete D4R3 source/tests/doctrine/self-hosted-PEM repair, regenerate packages/profile, and run the repository/frozen/Core gates. Then choose an **already-existing** immutable repaired source snapshot that contains the sentinel, validate exact-ref public realization, and publish that exact SHA only from a later descendant mapping commit. Never make a bootstrap commit self-name.

**Gate E3:** exact public fallback resolves only the new immutable repaired snapshot; `e12572c021087308570abfa41657a910c6896457` and all earlier 6.3 attempts remain invalidated historical fixtures; frozen 5.16/6.0/6.1/6.2 resources remain byte-identical.

### 18.3 Repair F3 - candidate-bound affected qualification and independent re-review

Bind one new semantic candidate after E3 publication/generation. Freshly execute D4R3 owner-binding discriminators, PEM validation, full source regression, public-bootstrap exact-ref realization, canonical build/package validation/committed parity, profile/snapshot parity, frozen-resource integrity, whitespace checks, and Orchestrator Core acceptance. Recompute static activation evidence where canonical routed bytes changed. Re-evaluate the affected Q63/F63/Challenge cases against the new candidate and explicitly carry forward only unaffected F2 cases whose claim/candidate-independent applicability remains intact. Refresh preservation census, implementation state, self-hosted PEM/HAS as affected, and independent-review handoff.

**Gate F3:** no authority-bearing owner path can pass solely from a non-empty label or branch-local artifact; no stale F2 claim is represented as fresh execution; no required affected check is missing; a fresh independent assembled-candidate Review remains the final Stage-F lifecycle gate.

### 18.4 Repair sequencing and preservation

```text
D4R3 accepted-state governing-owner binding + direct falsification fixtures
 -> preserve/reverify D1/D2/D3/D5R2/D6/D7 and unaffected evidence
 -> source/PEM/doctrine/template reconciliation
 -> full repository/build/package/profile/Core/frozen checks with no current 6.3 bootstrap
 -> E3 immutable replacement bootstrap + later exact mapping
 -> regenerate/check all affected descendants
 -> F3 candidate-bound affected qualification + evidence applicability map
 -> fresh independent assembled-candidate Review
 -> only then Stage G
```

No Serious Challenge is active. The intended design remains evidence-backed project-local memory with non-authoritative learning, exact durable warrants, immutable observations, stable semantic identity, provenance-aware episodes, claim-relative maturity, accepted-state-bounded authority, actual accepted-repair recurrence rather than chronology or self-attestation, one HAS/overlay interface, atomic publication, and lossless progressive disclosure.

## 19. Intended end state

```text
lossless accepted Protocol 6.2 semantics
+ exact cold historical observations/evidence remain recoverable
+ one coherent logical compact current project memory
+ evidence-backed negative and positive learning
+ stable family semantic identity and acyclic lineage
+ observation/assessment and observation/association/causal claims kept distinct
+ causal positive application episodes with provenance dependence visible
+ invalidated evidence retained historically but removed from current support
+ claim-relative maturity rather than count-to-proof promotion
+ demonstrated success distinguished from comparative/default preference
+ overlapping guidance carries explicit decision/tradeoff boundaries
+ typed lesson relations without recursive proof
+ statistics with honest coverage, watermark, aggregation/project scope, lifecycle, and chronology
+ branch-safe accepted-base/candidate-overlay composition
+ HAS binds the memory basis actually consulted and reconciles late change
+ atomic root/partition publication and subordinate derived indexes
+ applicability-led activation with no stale-tag false negatives
+ high-impact unresolved state cannot be crowded out by success stories
+ learned capabilities distinguished from accepted invariants
+ simpler/new mechanisms remain admissible
+ self-reference-safe and Git-owner-safe updates
+ untrusted evidence remains data, never instruction/authorization
+ no routine history replay or cold-history context growth
+ qualification proportional to each bounded claim
+ fresh-context agents inherit demonstrated project experience instead of guesses
```

Central invariant:

> The project must be able to learn even when the individual agent does not persist, and every claimed lesson must remain traceable to preserved observations, admissible non-recursive claim-relative evidence, honest causal/provenance structure, bounded applicability and coverage, supported schema, project scope, coherent publication state, and current authority boundaries rather than memory, repetition, selective success reporting, misleading aggregation, stale/invalid warrants, branch/default recency, reviewer votes, count-to-proof promotion, post-hoc causality, timestamp chronology, instruction-like evidence, or historical mechanism worship.
