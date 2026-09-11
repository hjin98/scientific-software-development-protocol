---
kind: abstraction-concretization-change-plan
workplan_id: PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY
protocol_version: 6.2.0
target_protocol_version: 6.3.0
status: active
created_date: 2026-09-11
reviewed_date: 2026-09-11
design_closure_status: pass-after-repair
implementation_handoff: authorized
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

The **Scientific Software Development Protocol (SSDP)** preserves detailed engineering history in Git, workplans, reviews, qualifications, semantic-evolution records, generated/package evidence, and immutable protocol recovery snapshots. Protocol 6.2 made that sophistication cheaper to use through lossless representation and progressive disclosure, but a fresh-context engineer can still miss project-specific lessons that are distributed across years of detailed evidence.

Protocol 6.3 adds a compact, current, evidence-backed learning layer without replacing that history or making historical evidence semantic authority.

For this plan:

- **Project Engineering Memory (PEM)** — a compact, project-local, non-authoritative representation of demonstrated engineering lessons, recurring failure families, successful patterns, important discoveries, preservation capabilities, and high-impact current notices, with exact routes to supporting evidence;
- **historical evidentiary corpus** — the durable project evidence from which PEM findings are assessed, including commits, workplans, reviews, qualification records, tests, benchmarks, profiles, analyses, semantic-evolution records, and other applicable observations; this corpus is evidence/provenance, not a new D1-D4 authority layer;
- **evidence binding** — a resolvable, normally immutable reference from a PEM claim to the evidence specification/realization/observation/assessment that warrants it;
- **learning family** — a stable generalized project lesson. Failure-family membership follows the existing convergence rule: materially equivalent manifestations share a governing invariant, semantic owner/authority class, and materially equivalent failure mechanism; textual similarity or a broad subsystem label is insufficient;
- **occurrence** — one independently introduced or independently existing confirmed manifestation of a failure family; one cause producing many symptoms is normally one occurrence;
- **successful application** — one independently qualified use of a positive pattern whose claimed benefit and governing constraints are both supported by admissible evidence;
- **coverage state** — the declared extent to which the historical corpus has been examined for a family or PEM instance; absence from an incomplete memory is not evidence of absence;
- **temperature** — an importance/attention classification (`HOT`, `WARM`, `COLD`, or `UNASSESSED`) derived from confirmed recurrence/application statistics plus explicit evidence-backed impact promotion; temperature is a sensor for routing and salience, not authority or an acceptance threshold;
- **evidence maturity** — confidence in the bounded claim (`PROVISIONAL`, `SUPPORTED`, or `PROVEN`), kept distinct from current applicability/conflict/retirement state;
- **Historical Applicability Set (HAS)** — the bounded current-work record stating which materially relevant PEM families/capabilities apply, do not apply with reason, or require deeper evidence inspection;
- **capability-transfer map** — a mapping from a replaced mechanism to each demonstrated capability it supplied, the replacement owner/mechanism, and the evidence that verifies preservation or deliberate supersession;
- **fresh-context agent** — an agent or engineer that does not carry reliable private conversational memory of prior project cycles and therefore must recover project state from durable artifacts.

The goal is not to create a bug database, a universal project graph, a second authority system, or a mandatory archaeology pass for every local change. It is to give a fresh-context agent the smallest complete project-aware representation of engineering lessons likely to change current decisions, while keeping detailed history cold and exactly recoverable.

## 1. Outcome, authority, baseline, and scope

Protocol 6.3 SHALL be a backward-compatible minor strengthening of accepted Protocol 6.2. It adds evidence-backed engineering-memory semantics and workflow integration without weakening any accepted D1-D4 authority, evidence, Challenge, compatibility, representation, routing, package, profile, or lifecycle rule.

The exact accepted 6.2 identities governing this plan are:

```text
accepted current protocol:               6.2.0
accepted 6.2 recovery:                   b59adc77efe6951912cfd705cc43830c58ca27d0
6.2 semantic candidate through recovery: ebbc4591bdfed039512026b8acb3a6749475c1c5
6.2 public-source bootstrap:              5a062ebc472755607b9dc66d33a5ebbc4b7429aa
6.2 recovery mapping commit:              bc76b16fda96be09f38a1b40a2ef877e8309534d
6.2 mapping-bearing generated commit:     ca622ea2b1c33e70668060cf0cc2fe9138776f7f
6.3 branch point on accepted main:        bf856f742d1744a8ff50f300ee6493fb93e5c9d0
```

The recovery identity is the immutable semantic/rollback baseline. The later mapping/generated/main descendants are separately relevant to current document-control, generated/package parity, and branch ancestry. Do not collapse these identities.

Protocol 6.2 remains accepted-current until Protocol 6.3 completes semantic qualification, independent Review, immutable public bootstrap, recovery mapping, generated/profile/package reconciliation, semantic-evolution/authority-index reconciliation, affected Protocol 7 inheritance reconciliation, and lifecycle closeout. Version-bound older work remains governed by its declared version; a newer installed skill does not silently reinterpret it.

This workplan has no semantic-supersession escape hatch. If implementation reveals that accepted 6.2 authority is materially false, contradictory, inadequate, or impossible to preserve coherently, stop at the earliest affected owner and raise the existing Challenge/Serious Challenge process. Do not use a memory-summary edit to choose new semantic truth.

### 1.1 Accepted 6.2 preservation baseline

Protocol 6.3 MUST preserve every accepted Protocol 6.2 doctrine and still-valid historical capability, including at minimum:

- the complete T01-T39 semantic preservation surface as independently reviewed under 6.2;
- feasibility/admissibility before optimization and minimum justified total complexity;
- authority provenance, one current semantic owner, precedence, evidence-not-authority, and bounded human ratification;
- D1-D4 DAG routing, reduced routes, multi-parent fidelity/adequacy review, bounded invalidation, Challenge/Serious Challenge, and composed closure;
- D1, D2, D3, and D4 owner semantics;
- documentation, repository-hygiene, maintenance-audit, evidence, testing, workflow, long-horizon, language/tool, security, performance, storage, release, debugging, Git, and other concern-owner semantics;
- root-cause/semantic-family reasoning, first-clean-local-defect locality, recurrence-driven simplification, and removal/rewiring before compensating machinery;
- snapshot-complete handoffs and validity-scoped context reuse;
- current-vs-history separation and semantic-evolution provenance;
- evidence specification/realization/observation/assessment, applicability, stale evidence in both polarities, evidentiary target versus execution dependency, independence/common-mode risk, and bounded impact closure;
- proxy-proof/real-owner testing, stage-local plus final assembled acceptance, qualification separation, failure paths, and missing-required-check blocking;
- lossless representation, anti-scope-laundering, importance-weighted attention without acceptance loss, one detailed owner per generic rule, bounded typed progressive disclosure, cold-path reachability, non-activating ordinary links, and derived-view non-authority;
- Protocol 6.2 replacement-bootstrap discipline and exact immutable fallback;
- the repaired software-documentation cold routes and their standalone reachability;
- static activation sensors as structural evidence rather than live-model performance proof;
- immutable 5.16/6.0/6.1 resources and current 6.2 profile behavior/identity;
- source/generated/package/snapshot parity and canonical-generation ownership;
- all 115 accepted Protocol 6.2 behavioral scenarios plus both affected requalifications and Stage G acceptance;
- current abstraction/concretization nomenclature while frozen historical identities remain unchanged;
- the human-facing background/terminology/first-use abbreviation standard;
- assembled-candidate independent Review rather than diff/summary/green-status acceptance;
- immutable bootstrap versus recovery separation and the rule that default/latest is never a protocol-version oracle.

T01-T39 are review hypotheses/evidence labels, not protocol authority. Current accepted owners remain semantic authority.

### 1.2 Non-goals

Protocol 6.3 MUST NOT:

- replace Git, semantic evolution, workplans, qualifications, or archived evidence with PEM;
- turn tests, benchmarks, commits, or PEM itself into D1-D4 authority;
- preserve every ordinary bug fix as permanent memory;
- force a family census for a first clean local defect merely because similar failures are imaginable;
- make historical mechanisms immutable merely because they once worked;
- treat frequency, temperature, benchmark magnitude, or review count as an acceptance threshold;
- introduce a universal database, graph, daemon, background indexer, or second routing registry;
- load PEM or project history unconditionally for every task;
- scan all Git history on every bootstrap or recompute all statistics on every read;
- create separately maintained Markdown and JSON/YAML authorities for the same memory;
- rewrite archived workplans or frozen protocol/profile resources to match 6.3 terminology;
- broaden a local memory feature into unrelated Protocol 7 control-plane implementation;
- merge/cut over to `main` without separate authorization.

## 2. Governing 6.3 rule

### 2.1 Evidence-backed learning

Project memory stores conclusions together with their warrant.

The system SHALL distinguish:

```text
idea / hypothesis
 -> implementation or attempted intervention
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
 -> bounded finding
 -> generalized project lesson when justified
 -> current PEM representation
```

A plausible idea, author preference, or attractive implementation is not positive project knowledge merely because it exists.

Statements such as `this should be faster`, `this seems cleaner`, or `this might scale better` remain hypotheses until evidence suitable to the bounded claim exists.

Conversely, evidence is not authority. Qualification is an acceptance gate for a bounded engineering claim under its governing authority and evidence assessment; it does not become a fifth semantic domain or automatically prove that the oracle, model, architecture, or generalization is correct.

### 2.2 Admissibility before positive optimization

A positive engineering pattern is admissible only when it continues to satisfy all applicable governing correctness, scientific/numerical, architecture, compatibility, security, reliability, resource, and external constraints.

A faster implementation that violates accepted semantics is not a successful optimization. Record measurable gains together with material costs/tradeoffs and the regime in which the result is admissible.

### 2.3 Past evidence is a prior, not a veto

Past success creates an evidence-backed preference, not architectural immunity. Past failure creates an evidence-backed warning, not permanent prohibition.

A new approach MAY replace a proven historical approach when it:

1. considers applicable historical evidence;
2. identifies demonstrated capabilities that must survive;
3. keeps governing parent/side constraints fixed unless explicitly reopened;
4. supplies evidence appropriate to its new claims; and
5. passes affected acceptance/qualification.

The project should become experienced, not timid.

## 3. Finite representation census and no-loss map

Before modifying protocol source, Stage A SHALL create `qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md` as non-authoritative implementation/review evidence.

The census SHALL enumerate every current durable/generative Protocol 6.2 representation surface before deciding what is touched. At minimum it covers:

- all four `source/roles/*/SKILL.md` entrypoints and three current specialist entrypoints;
- all current `source/shared/references/*.md`;
- all current shared templates plus the proposed PEM template;
- `AGENTS.md`, root/source `README.md`, `PORTABILITY.md`, `source/SEMANTIC_DEPENDENCIES.md`, and `source/PROTOCOL_VERSION`;
- workflow-prompt source;
- current Protocol 6.2 profile/prompts/snapshot resources and the proposed 6.3 successors;
- protocol-bearing schemas/renderers/help/status text affected by the new feature;
- qualification scenario/routing/package assets;
- active workplan authority index and this workplan;
- `history/SEMANTIC_EVOLUTION.md` as append-only cold history at closeout;
- archived workplans as frozen cold evidence;
- `dist/` and generated snapshots as generated descendants;
- frozen 5.16/6.0/6.1/6.2 resources.

Classify each as `refactor`, `route-only`, `new`, `generated`, `frozen/historical`, or `intentionally unchanged with reason`.

For every materially changed accepted obligation, the transformation map SHALL record:

```text
preservation ID
accepted 6.2 owner/location
6.3 owner/location
governed obligation
preservation/generalization relation
oracle/evidence that can detect loss
disposition: PRESERVED or BLOCKING
```

Green tests or labels do not prove preservation. The independent reviewer SHALL challenge the map against actual owners and assembled artifacts.

### 3.1 Required appended 6.3 preservation hypotheses

After independently reproducing T01-T39 unchanged, append the next available IDs for at least these 6.3 obligations:

```text
T40 authoritative-current-owner / non-authoritative-memory separation
T41 compact active project-engineering-memory representation
T42 stable learning-family identity and explicit lineage
T43 exact durable evidence binding
T44 evidence-ledger-derived recurrence/application statistics
T45 evidence-backed positive success patterns and demonstrated tradeoffs
T46 hypothesis / evidence maturity / applicability-state separation
T47 reproducible temperature with explicit evidence-backed overrides
T48 historical-coverage state and no absence inference from incomplete memory
T49 semantic family-membership discipline
T50 first-local-defect / admission-threshold preservation
T51 architectural-rework Historical Applicability Set
T52 mechanism-to-capability transfer accounting
T53 promotion of repeated lessons into invariants/sensors when justified
T54 mandatory material closeout learning assessment
T55 quantitative effect-size and experimental-envelope preservation
T56 contradictory evidence and retirement without historical erasure
T57 evidence applicability/staleness and bounded invalidation of PEM
T58 evidentiary independence/common-mode-risk preservation
T59 active-summary progressive disclosure and cold detail reachability
T60 project-local PEM versus packaged protocol/template separation
T61 single canonical Markdown memory; derived indexes remain subordinate
T62 6.3 bootstrap/profile/recovery/version-bound compatibility staging
T63 frozen 5.16/6.0/6.1/6.2 profile/resource preservation
T64 generated/package/source parity and exact-ref fallback
T65 static-versus-live claim discipline for context/performance claims
T66 Protocol 7 inheritance/current-lifecycle reconciliation
T67 human-facing background/terminology/abbreviation completeness
T68 independent assembled-candidate qualification/Review
T69 anti-scope-laundering and lower-salience mandatory-constraint preservation
T70 no recursive summary/evidence laundering
```

If the actual accepted 6.2 census uses later IDs, append rather than collide. These IDs remain preservation evidence, not semantic authority.

## 4. Canonical owner and routing architecture

### 4.1 One detailed owner per generic rule

Protocol 6.3 SHALL not duplicate its doctrine across every role. The intended owner topology is:

```text
universal authority / Challenge / lossless representation
  -> abstraction-and-concretization.md

PEM-specific schema / compact representation / coverage / family records
  -> NEW project-engineering-memory.md concern owner

evidence lifecycle / applicability / stale state / independence / impact
  -> evidence-evolution-and-dependencies.md

recurrence / semantic-family membership / first-local-defect / simplification
  -> convergence-and-cycle-economy.md

D3 preservation capability / mechanism replacement / capability transfer
  -> architecture-and-design.md

workflow activation / HAS / workplan handoff / closeout update
  -> workflow-and-workplans.md

current-vs-history document lifecycle / source-chain reconciliation
  -> documentation-maintenance.md

testing / benchmark / oracle / acceptance methods
  -> testing-and-validation.md

version / bootstrap / recovery / profile / fallback
  -> protocol-versioning-and-compatibility.md

repository-context reuse / historical intake economy
  -> repository-intake.md
```

`project-engineering-memory.md` owns only PEM-specific semantics. It routes generic evidence/family/workflow/version doctrine to the existing owners rather than restating them.

The universal kernel SHALL receive at most the minimum route/constraint needed to keep memory subordinate and discoverable; PEM is not universal-kernel material.

If Stage A finds accepted 6.2 ownership differs, preserve the accepted owner or block and resolve the ownership issue before implementation. Do not create a parallel owner merely to match this proposed map.

### 4.2 Project-local canonical artifact

Protocol 6.3 SHALL define the default project-local artifact:

```text
PROJECT-ENGINEERING-MEMORY.md
```

at the governed repository root, unless an existing project authority explicitly declares one alternative canonical path. The selected path must be discoverable from ordinary repository intake without hidden chat.

Add one packaged protocol template, proposed as:

```text
source/shared/templates/project_engineering_memory_template.md
```

The **project instance** is project state and SHALL NOT be copied into generic SSDP `dist/` skill packages or orchestration profiles as though it were protocol doctrine. The **template and protocol instructions** are canonical protocol source and follow normal generated/package closure. In the SSDP repository itself, its self-hosted `PROJECT-ENGINEERING-MEMORY.md` is ordinary project-local content.

Do not maintain a second hand-authored JSON/YAML database. A generated index may exist only if a demonstrated consumer needs it; it must be reproducible from canonical Markdown and explicitly non-authoritative.

### 4.3 Bounded activation

Preferred activation shape:

```text
task
 -> role/specialist root
      -> universal kernel + current domain owner
      -> when the memory trigger is material: project-engineering-memory.md
           -> project-local PEM active summary
                -> only relevant family detail
                     -> underlying evidence only when needed
```

A visible PEM trigger includes at least:

- material rework of existing D3 architecture;
- replacement/consolidation of mature machinery with demonstrated capabilities;
- a defect believed to recur or belong to an existing semantic family;
- substantial optimization/performance/scaling rework of existing machinery;
- migration/recovery work where historical design choices can change the decision;
- an active workplan that explicitly binds relevant PEM entries.

A first clean local defect with no recurrence/generalization signal remains local. Ordinary documentation, trivial implementation, or unrelated cold concerns do not load PEM merely because the file exists.

Ordinary links, package membership, semantic dependencies, or the mere existence of PEM do not activate it. If a concern is cold but could change the current decision, a hot owner must expose the trigger and route.

### 4.4 Missing-memory/adoption behavior

A missing or partial PEM is not proof that the project has no historical lessons.

For a new project with no material history, initialization may create an empty PEM with explicit coverage state.

For an established project adopting 6.3:

- ordinary work may continue without inventing a complete backfill;
- before a memory-triggering major rework, perform the bounded relevant historical intake needed for the affected owner/surface or establish/update PEM coverage for that scope;
- if required historical coverage cannot be established, record the uncertainty and do not claim that relevant failure/success families are absent.

Version-bound Protocol 6.2 work does not retroactively acquire a 6.3 PEM obligation unless it explicitly adopts 6.3 after compatibility/impact reconciliation.

## 5. Canonical PEM representation

PEM is a compact current engineering-learning representation, not patch history. Detailed chronology remains in Git/history/evidence artifacts.

### 5.1 Global metadata and coverage

The canonical PEM SHALL expose enough metadata to judge applicability without loading history, including:

```text
memory_schema_version
maintained_under_protocol
project/repository identity when needed for disambiguation
coverage_state
reconciled_through immutable accepted project identity
known unreviewed historical ranges/surfaces when material
open review-required families/notices
```

Coverage states SHALL include at least:

```text
UNINITIALIZED
PARTIAL
RECONCILED_FOR_DECLARED_SCOPE
```

`RECONCILED_FOR_DECLARED_SCOPE` means the declared bounded corpus/surface has been reviewed sufficiently for the represented families/counts. It does not claim omniscience outside that scope.

PEM SHALL never use a commit that must self-name as its own authority. `reconciled_through` identifies already-existing accepted history covered by the memory update.

### 5.2 Active engineering memory

The beginning of PEM SHALL provide a compact importance-weighted view answering:

```text
What repeatedly fails here?
What repeatedly works here?
What capabilities must survive relevant rework?
What high-impact current project notices require attention?
What evidence-backed engineering instincts are most useful now?
```

Each summary item should carry only:

```text
stable ID
kind
one-line bounded lesson
temperature
evidence maturity/current applicability
confirmed count or qualified-application count
primary applicability trigger
short evidence route
```

No arbitrary token threshold may delete material entries. If the active section becomes dense, first generalize genuinely equivalent families, remove duplicated prose, and make details cold while preserving visible routes. Metrics are context sensors, not pass thresholds.

A task-specific selected view may be generated transiently from PEM, but it is derived coordination state and cannot become a second maintained authority.

### 5.3 Current notices

PEM MAY contain a small current-notice section for a high-impact project fact that materially affects engineering now but is not yet a generalized family, for example an active migration boundary or known provisional hazard.

A notice requires:

```text
stable notice ID
current claim/state
source/evidence route
applicability
review/expiry condition
```

Notices do not contribute to family occurrence/application counts and must be retired or converted to a family when their lifecycle changes.

## 6. Learning-family schema and admission

### 6.1 Stable family kinds

At minimum support:

```text
FAILURE_FAMILY
SUCCESS_PATTERN
DISCOVERY
PRESERVATION_CAPABILITY
```

Use one consistent identifier namespace, proposed as:

```text
FF-###  failure family
SP-###  success pattern
DS-###  discovery
PC-###  preservation capability
```

Occurrence/application IDs are scoped to their family (`O01`, `A01`, ...). Do not mix `HF`, `FF`, or other aliases in current artifacts unless migration evidence requires an explicit historical alias.

### 6.2 Admission threshold

PEM is not a permanent ledger of ordinary fix chronology.

Admit or materially update a learning family only when at least one evidence-backed condition applies:

- the same semantic failure mechanism has materially recurred;
- a prior accepted repair was later reintroduced;
- one high-impact incident exposes a broadly reusable architectural lesson or preservation capability;
- an optimization/simplification has a meaningful demonstrated benefit likely to matter again;
- the same successful pattern has qualified across independent surfaces;
- a discovery materially changes the preferred project approach to a recurring class of work;
- a mechanism replacement/generalization/rejection/restoration has rationale likely to prevent rediscovery;
- a current high-risk issue warrants a temporary notice rather than false family generalization.

A first clean local defect normally remains local. Do not mint a family merely because sibling bugs are conceivable.

Generic textbook knowledge or protocol doctrine that is not project-specific belongs at its existing owner, not in PEM.

### 6.3 Family membership

Failure-family membership requires materially equivalent:

1. governing invariant;
2. semantic owner/authority class; and
3. failure mechanism/cause at the level relevant to repair.

Common symptoms, error messages, file locations, or subsystem labels are insufficient.

Where classification is uncertain, mark the candidate `PROVISIONAL`/review-required rather than inflating an established family.

### 6.4 Split, merge, and reclassification

Family taxonomy may improve as evidence accumulates without rewriting history.

For a split:

- preserve the original family ID as historical/superseded lineage;
- assign each occurrence to the justified child family;
- do not double-count one occurrence in aggregate statistics unless explicitly reporting overlapping views.

For a merge:

- create or select the current generalized family;
- retain predecessor IDs as lineage/aliases;
- deduplicate overlapping occurrence/application evidence by immutable identity;
- preserve materially distinct causes/limits rather than flattening them for compactness.

A reclassification changes the current interpretation, not the historical observation.

## 7. Evidence model and bindings

### 7.1 Inherit the complete evidence lifecycle

PEM SHALL use the accepted Protocol 6.2 evidence model:

```text
governed claim
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

For material entries, the binding must preserve enough of the following to judge applicability:

```text
evidentiary target
specification/oracle identity
subject/candidate identity
input/validity regime
environment/backend/precision/configuration when material
execution dependencies
observation
assessment
stochastic replicate identity when material
protocol/workplan obligation
```

A rerun on a changed candidate is a new realization. Do not rewrite old results into evidence for a new subject.

### 7.2 Exact, durable evidence routes

Prefer immutable Git commit + path + stable section/test/finding identifier. A branch/default-branch path alone is not sufficient for a material historical warrant because later edits can change its meaning.

External CI/benchmark run IDs may be referenced, but if the external artifact can expire and its observation is material to long-lived project memory, preserve a compact durable qualification/benchmark record in the repository that states the result and exact run/candidate identity.

PEM itself, a generated active summary, an implementer narrative, or another recursively compressed summary SHALL NOT be the sole evidence for its own substantive claim. Follow the route to the underlying admissible observation/assessment.

### 7.3 Cause and repair evidence

A failure occurrence should preserve compactly:

```text
occurrence ID
confirmed date/commit
subject/candidate
owner/surface
observed failure
cause claim
cause evidence
repair reference
post-repair qualification
limits/applicability
```

Distinguish incident-level cause (`function X called before branch Y`) from generalized cause (`route-exclusive preparation owned by shared pre-dispatch stage`). Distinguish the literal historical patch from the generalized repair principle.

### 7.4 Positive evidence

A successful application should preserve compactly:

```text
application ID
subject/candidate and comparator when material
owner/surface
claimed benefit
qualification/analysis reference
quantitative effect size when available
experimental envelope
correctness/constraint evidence
material costs/tradeoffs
applicability and limits
```

Quantitative claims retain effect size rather than only adjectives. Examples include `4.0x faster`, `8.1x lower peak memory`, `91% fewer repeated constructions`, or a demonstrated scaling change.

A complexity claim such as `O(N^2) -> O(N log N)` requires adequate algorithmic analysis of the governed operation and verification that the implementation realizes the analyzed algorithm; one timing sample cannot establish asymptotic complexity. Empirical scaling evidence should supplement analysis when materially useful.

### 7.5 Applicability, stale state, contradiction, and common-mode risk

A valid old pass is not confirmation of a changed candidate; a stale old failure is not refutation of it.

When protocol obligation, governing claim, implementation/candidate, evidence specification/oracle, material input regime, environment, or execution dependency changes enough to plausibly affect a PEM claim, mark only the materially affected family/application `review-required` or stale and preserve unaffected entries with reason.

For important claims, account for evidentiary independence/common-mode risk. Multiple tests sharing one defective expected-value generator, fixture, benchmark harness, dataset, or mistaken assumption do not automatically provide independent confirmation.

Contradictory admissible observations remain visible. Do not discard inconvenient evidence to keep a success pattern `PROVEN` or a failure family `HOT`.

Evidence maturity is one axis:

```text
PROVISIONAL
SUPPORTED
PROVEN
```

Current evidence/applicability state is separate:

```text
CURRENT
REVIEW_REQUIRED
STALE_OR_INAPPLICABLE
RETIRED
```

Contradiction is an explicit assessment state/flag, not silent deletion. A finding may be high-importance and provisional at the same time; temperature and confidence are orthogonal.

## 8. Statistics, coverage, and temperature

### 8.1 Evidence ledger is canonical; counters are derived

Occurrence/application ledger rows are the canonical statistical basis. Displayed totals are derived summaries and MUST NOT be hand-incremented independently.

For failure families track at least:

```text
confirmed_occurrence_count
independent_repair_cycle_count
affected_surface_count
recurrence_after_accepted_repair_count
first_confirmed
last_confirmed
coverage_state / coverage_basis
```

For success patterns track at least:

```text
qualified_application_count
independent_surface_count
first_qualified
last_qualified
coverage_state / coverage_basis
```

A merge/rebase of concurrent memory edits reconciles evidence rows first and recomputes counts; never sum stored counters blindly.

### 8.2 Counting rules

One causal engineering change that produces 20 failing tests is normally one occurrence, not 20.

A defect repaired and accepted, then independently reintroduced by a later change, is another occurrence and increments recurrence-after-repair.

Several commits in one coherent repair attempt are one repair cycle when they close one occurrence through accepted qualification.

Repeated executions of the same successful implementation do not increase `qualified_application_count`; an independent later use may count when separately qualified.

### 8.3 Incomplete coverage cannot manufacture cold confidence

`confirmed_occurrence_count` is always exactly the number of evidence-bound occurrences in the ledger. It may be a lower bound on historical reality when coverage is partial.

Therefore:

- `>=3` confirmed occurrences are sufficient for a frequency-based `HOT` floor even if additional history is unreviewed;
- `2` confirmed occurrences establish at least `WARM` by frequency;
- `1` confirmed occurrence may be `COLD` by frequency only when the declared family-relevant historical coverage is adequate to support that classification; otherwise temperature remains `UNASSESSED` unless evidence-backed impact promotes it;
- absence of a family or `0` known occurrences in partial/uninitialized coverage is never evidence that the hazard does not exist.

Apply the same discipline to positive application frequency.

### 8.4 Reproducible temperature

Default frequency classification:

```text
confirmed failure occurrences >= 3  -> HOT
confirmed failure occurrences == 2  -> WARM
confirmed failure occurrences == 1  -> COLD only with adequate declared coverage

qualified success applications >= 3 -> HOT
qualified success applications == 2 -> WARM
qualified success applications == 1 -> COLD/UNASSESSED by frequency, unless promoted by demonstrated impact
```

A single event/application may be promoted to `WARM` or `HOT` for demonstrated severity, breadth, cost, architectural criticality, or exceptional benefit, but the override must be explicit and evidence-bound. Store the base frequency class, override reason, and final temperature so another reviewer can reproduce the result.

Recency may order attention within a temperature or trigger review of applicability; it must not erase accumulated counts or automatically demote an old but still-applicable lesson.

No count or temperature can force a design decision or acceptance. They change routing/salience and indicate where stronger reasoning is justified.

## 9. Failure-to-success learning and preservation capabilities

PEM SHALL represent the project lesson, not only the scar.

A valid chain may be:

```text
FF-### repeated expensive preparation
  -> DS-### preparation ownership is route-local
  -> SP-### lazy route-owned construction repeatedly qualifies
  -> PC-### cold routes must not activate expensive machinery
```

Several failures may support one stronger positive pattern; several positive applications may support one preservation capability.

A preservation capability records what future architecture must retain independent of the historical mechanism, for example bounded parallel execution, checkpoint continuation, artifact reuse, lazy activation, deterministic ordering, semantic equivalence, or generated/package identity.

When a mechanism is removed/replaced, record:

```text
old mechanism
 -> demonstrated capability
 -> new owner/mechanism or deliberate retirement
 -> governing rationale
 -> verification
```

The existence of a prior wrapper/cache/executor/checkpoint format does not make that mechanism authority.

## 10. Workflow integration and historical applicability

### 10.1 Design/workplan phase

For a memory-triggering substantial change:

1. read the PEM active summary;
2. determine governed scope from actual parent/side constraints, not from what makes memory convenient;
3. inspect relevant family detail/evidence only where triggered;
4. record a Historical Applicability Set;
5. identify preservation capabilities and any capability-transfer map;
6. identify new claims requiring qualification;
7. preserve lower-salience mandatory constraints even if PEM ranks them cold.

A Hot family that intersects the governed change surface must be dispositioned `applicable`, `not applicable with reason`, or `review required`. A partial memory or missing edge cannot prove non-applicability.

### 10.2 Implementation phase

Implementation preserves applicable demonstrated capabilities unless the accepted workplan deliberately supersedes them under governing authority and fresh evidence.

Do not accept a new positive pattern merely because code was written or tests happen to remain green.

### 10.3 Review phase

Review SHALL challenge at least:

```text
reintroduced historical failure mechanism
lost mature optimization
lost valid reuse
accidental serialization / lost parallel capability
new eager preparation
lost sensor/oracle
lost generated/package integrity
capability loss during mechanism replacement
stale or inapplicable PEM guidance
scope/materiality laundering through memory selection
```

Review proceeds against current owners and the assembled candidate. PEM is a high-information hypothesis index, not proof.

### 10.4 Evidence and impact closure

When a material authority/concretization change can affect PEM:

```text
identify materially dependent families/applications/capabilities
 -> preserve unaffected entries with reason
 -> mark affected entries REVIEW_REQUIRED/STALE as appropriate
 -> rerun/remap evidence where required
 -> update current PEM only after assessment
```

A change to one family does not invalidate all memory. Conversely, old active-summary text cannot be reused blindly after its owner/candidate/regime/evidence changes.

### 10.5 Closeout learning assessment

Every accepted **material** repair/rework/optimization SHALL ask:

```text
Did a known family recur?
Did a successful pattern qualify again independently?
Did a new reusable discovery emerge?
Did a demonstrated capability become important to preserve?
Did new evidence contradict/retire an existing lesson?
Did the memory coverage boundary materially change?
```

Update PEM only when the admission threshold is met or an existing entry materially changes. This preserves the existing rule that ordinary fix chronology is not a permanent ledger.

## 11. Maintenance transaction and compactness

A material PEM update SHALL:

1. identify the candidate learning/current notice;
2. bind exact admissible evidence;
3. classify or create the family under semantic-family rules;
4. update evidence rows, not counters directly;
5. recompute statistics;
6. update coverage and applicability;
7. update evidence maturity/conflict state;
8. compute base temperature and any evidence-bound override;
9. update active summary if current importance changed;
10. preserve family split/merge/retirement lineage;
11. verify no still-valid lesson, contradictory evidence, or mandatory condition was lost;
12. run structural/source-chain checks;
13. commit the current memory reconciliation as part of the engineering closeout or an immediately associated evidence/closeout commit.

The active summary SHALL remain compact through generalization and progressive disclosure, not deletion by quota. Raw incident narratives, benchmark tables, patch transcripts, and old debate stay at their evidence/history owners unless needed for current interpretation.

A compaction pass MAY rewrite wording, merge equivalent exposition, or make details cold only when it preserves family identity, statistics, coverage, distinct evidence, cause distinctions, limits, contradiction, capability relationships, and retrieval routes. If apparently duplicate lessons differ materially, stop compaction and preserve/resolve the distinction rather than editorially adjudicating it.

## 12. Performance and activation constraints

Protocol 6.3 must not recreate the class of regression it is meant to prevent.

Normal operation SHALL primarily consume the already-curated PEM active summary when its trigger fires. It SHALL NOT:

- rescan Git history on every task;
- recompute family statistics from the full corpus on every bootstrap;
- load all detailed family evidence merely to read the active summary;
- activate self-hosted backfill machinery during normal use;
- serialize unrelated initialization merely to load PEM.

Deep history is appropriate when creating/backfilling PEM, resolving disputed lineage/evidence, updating a family, performing dedicated qualification, or when independent Review needs underlying evidence.

Static context bytes/tokens, route counts, or activation traces are sensors only. Any claim that 6.3 improves actual model latency, attention, cache behavior, or engineering performance requires corresponding live evidence on the claimed harness/model/install regime. If telemetry is unavailable, report the empirical claim unavailable rather than laundering static evidence into a live-performance conclusion.

## 13. Self-hosted SSDP migration/backfill

SSDP SHALL be the first qualified project-local PEM instance.

Backfill from actual repository evidence, not this workplan's examples or agent recollection. Inspect, where relevant:

- semantic evolution;
- archived Protocol 5.x and 6.x workplans;
- Protocol 6.1/6.2 qualification and independent reviews;
- commit/patch history needed to identify concrete occurrences;
- replacement-bootstrap invalidation/repair;
- cold-route repair and requalification;
- static activation-sensor evidence;
- frozen-profile preservation;
- generated/package-integrity repairs;
- documentation background/terminology repairs;
- materially relevant optimization/simplification history.

Candidate families to investigate, **not pre-accept**, include:

```text
negative / failure candidates
- mature optimization lost during rework
- repeated calculation after architecture change
- eager/cold-route contamination
- accidental serialization
- loss of checkpoint/intermediate reuse
- ownership leakage
- generated/package divergence
- bootstrap identity drift
- frozen-profile mutation
- loss of activation protection
- patch/wrapper accumulation instead of owner correction
- documentation source-chain/background terminology drift
- diff-only review instead of assembled-candidate review

positive / success candidates
- route-local lazy activation
- provenance-valid artifact reuse
- bounded independent parallelism
- direct owner-layer repair and simplification
- semantic preservation maps
- static activation sensors
- assembled-candidate independent Review
- qualification-driven acceptance
- lossless generalization with exact cold evidence routes
```

For each seeded family, declare the historical coverage basis. Do not represent a partial search count as exhaustive. Archived workplans remain byte-identical; append concise semantic evolution only at normal closeout where the accepted 6.3 meaning warrants it.

## 14. Validation architecture

Extend existing qualification/test owners rather than creating a competing compliance framework.

The canonical Markdown PEM is the source. The minimum structural validator should detect:

- duplicate/current-colliding family IDs;
- invalid family kind/maturity/applicability/temperature values;
- malformed or non-resolving required evidence bindings;
- displayed count versus evidence-ledger mismatch;
- double-counted occurrence/application identity after merge/split;
- `COLD` classification unsupported by declared coverage;
- unexplained temperature override;
- active-summary reference to nonexistent/stale/retired entry;
- Provisional finding presented as proven fact;
- contradicted evidence hidden from current assessment;
- retired entry presented as active guidance;
- project-local PEM copied into generic protocol package;
- a generated index diverging from canonical Markdown;
- loss of T01-T39 or any 6.3 preservation row;
- source/generated/profile/package divergence.

Objective absence/uniqueness/derivation properties may be executable. Do not create a universal machine graph/database solely to validate PEM.

## 15. Protocol 6.3 version, bootstrap, profile, and package staging

Git commits cannot self-name. Protocol 6.3 SHALL preserve the repaired 6.2 staging discipline rather than repeating the bootstrap defect.

### 15.1 Public-source bootstrap

1. Complete the self-reference-safe 6.3 public-source set: current role/specialist entrypoints, all routed references/templates including PEM doctrine/template, `source/PROTOCOL_VERSION`, navigation/version-resolution source, and required package closure.
2. Validate source regression, canonical package build, standalone package/link closure, and routing-resource reachability without requiring an unknown 6.3 self commit.
3. Create an immutable **6.3 public-source bootstrap commit** only after those checks pass.
4. In a later semantic-candidate/publication commit, publish that exact immutable bootstrap identity in current 6.3 version-resolution surfaces. Do not use `main`, latest, a guessed semantic-version ref, or the eventual recovery identity as bootstrap.

### 15.2 Profile and frozen resources

Create a distinct `ssdp-protocol-6.3` profile/snapshot using profile schema v2 unless an actual machine contract change justifies a schema change.

Do not mutate packaged/frozen 5.16, 6.0, 6.1, or 6.2 profile/resource bytes. Protocol 6.2 becomes historical rollback only after 6.3 cutover; until then it remains accepted-current.

PEM project content is not embedded into the generic profile. Only protocol routing/doctrine/templates needed to recognize and use a project-local PEM are packaged.

### 15.3 Semantic candidate and generated descendants

Bind qualification to one immutable 6.3 semantic candidate. Later evidence/generated/lifecycle commits must contain no hidden canonical semantic mutation; any such mutation reopens affected qualification.

Rebuild generated `dist/` and orchestrator 6.3 descendants from canonical source. Validate:

- source-to-generated parity;
- package structure and local resource closure;
- profile identity/schema/stage topology;
- exact immutable public fallback;
- closest supported consumer ingestion;
- project-local PEM exclusion from generic packages.

### 15.4 Recovery and closeout staging

After semantic qualification and independent Review pass:

1. choose an immutable 6.3 recovery commit containing the accepted candidate and required decision evidence through ancestry;
2. publish `6.3.0 -> <exact recovery commit>` only in a later mapping commit;
3. regenerate mapping-bearing descendants;
4. rerun targeted recovery/parity/package/Core acceptance;
5. append concise 6.3 semantic evolution;
6. update the workplan authority index;
7. reconcile Protocol 7's pre-cutover inheritance/fallback baseline to accepted 6.3 **only after 6.3 acceptance**, without silently changing Protocol 7 D3 architecture semantics;
8. archive this workplan only after current 6.3 rules reside at canonical owners and all impact closure is complete.

No `main` merge/cutover is authorized by this workplan.

## 16. Qualification plan

Qualification SHALL include complete affected repository/package/orchestrator regression, the full 115-case Protocol 6.2 semantic capability suite against 6.3, focused 6.3 cases below, generated/profile/package checks, and independent assembled-candidate Review.

### Q63-01 — Complete 6.2 no-loss preservation

Independently challenge T01-T39 against current owners and the assembled 6.3 candidate. Preserve the 6.2 replacement bootstrap semantics, cold-route repair, static activation sensors, frozen profiles, generated/package integrity, original 115-case behavior, affected requalifications, and Stage G lifecycle rules.

### Q63-02 — Finite census and transformation closure

Every current durable/generative 6.2 artifact receives a disposition. Every materially transformed obligation closes `PRESERVED` or `BLOCKING`; no orphan current surface or hidden semantic owner passes.

### Q63-03 — Authority/evidence separation

A valid test, benchmark, commit, PEM entry, or semantic-evolution record may warrant/challenge a claim but cannot override a current D1-D4 owner by existence. Attempt to promote PEM into authority and reject it.

### Q63-04 — Activation and cold-route behavior

A material existing-architecture rework activates the PEM concern and project-local active summary. A first clean unrelated local defect does not. Ordinary hyperlinks/package membership do not activate PEM. Relevant cold family detail remains visibly reachable when its predicate becomes material.

### Q63-05 — Missing/partial memory

With no PEM or `PARTIAL` coverage, absence of a family cannot be used to prove historical absence/non-applicability. A qualifying major rework must perform bounded relevant intake or carry explicit uncertainty.

### Q63-06 — Evidence-binding durability

Every self-hosted family occurrence/application resolves to immutable/durable evidence sufficient to recover the bounded observation/assessment. Default-branch-only and recursive-PEM-only proof routes are rejected.

### Q63-07 — Evidence applicability and stale polarity

A stale passing observation cannot confirm current memory; a stale failing observation cannot refute it. Changed candidate/oracle/regime cases mark only materially affected entries review-required/stale and preserve unaffected evidence.

### Q63-08 — Evidentiary independence/common-mode risk

Several nominally different checks sharing one defective oracle/fixture do not qualify as independent support. Contradictory admissible observations remain visible.

### Q63-09 — Semantic family membership

Textually similar failures with different governing invariant/owner/failure mechanism are not forced into one family. Materially equivalent manifestations with one shared cause may be grouped even across several files.

### Q63-10 — One cause / many symptoms

One causal defect producing many failing tests and affected sites counts once unless independent introductions are evidenced.

### Q63-11 — Recurrence after accepted repair

A later independent reintroduction increments confirmed occurrence and recurrence-after-repair exactly once and binds both repair cycles.

### Q63-12 — Split/merge lineage and merge safety

Split or merge a family fixture. Preserve predecessor lineage, reassign/deduplicate evidence correctly, and recompute totals from evidence rows rather than summing counters.

### Q63-13 — Coverage-sensitive temperature

Three confirmed occurrences are Hot by frequency; two are Warm. One occurrence under incomplete coverage cannot be represented as confidently Cold. Any impact promotion carries an explicit evidence-bound override and reproducible base/final state.

### Q63-14 — Importance is not authority

A Hot family does not force an architecture choice or lower the pass threshold. A Cold but materially applicable mandatory constraint cannot disappear from closure because of ranking.

### Q63-15 — Positive-evidence promotion

An unmeasured optimization remains Provisional. A qualified optimization may become Supported/Proven only within the demonstrated regime and only if governing correctness/side constraints remain satisfied.

### Q63-16 — Quantitative effect preservation

A qualified effect such as `4x faster` or `8x lower peak memory` retains comparator, candidate, measurement envelope, and evidence route through PEM compaction.

### Q63-17 — Complexity-claim discipline

One timing result cannot establish `O(N^2) -> O(N log N)`. Adequate algorithmic analysis plus implementation correspondence, and empirical scaling evidence where material, can support the bounded claim.

### Q63-18 — Capability transfer without ossification

Replace historical machinery with a simpler/new mechanism that preserves all governing constraints and demonstrated capabilities. The protocol must permit the replacement after fresh qualification; no historical mechanism becomes authority.

### Q63-19 — First-local-defect/admission economy

A clean one-off local bug does not require a permanent family/ledger/backfill. A repeated/high-impact/generalizable case does trigger proportionate learning assessment.

### Q63-20 — Current-memory invalidation and contradiction

Materially change an owner/candidate so an old pattern becomes review-required, contradicted, or retired. Preserve the old evidence/history while refreshing current active guidance.

### Q63-21 — Active-summary lossless compaction

Compact several entries. Preserve stable identities, statistics, coverage, applicability, limits, contradictory evidence, capability links, and cold retrieval routes. Do not pass by shrinking governed scope.

### Q63-22 — No repeated-history regression

Normal memory-triggering operation consumes the curated summary without full-history scan/stat recomputation. Ordinary non-triggering work adds no PEM/history preparation. Use activation/call/trace sensors appropriate to the implementation.

### Q63-23 — Static-versus-live claims

Static activation/context measurements establish only structural claims. Live latency/context-use/model-performance claims require fresh live evidence for the claimed harness/model/install regime; otherwise they remain explicitly unavailable.

### Q63-24 — Project-local/package separation

The self-hosted SSDP PEM is present as project content but absent from generic packaged skill/profile payloads. The PEM template/doctrine are present wherever supported routing requires them.

### Q63-25 — 6.3 exact public fallback

No-local-compatible-skill and incompatible-default-branch cases resolve 6.3 only through the exact validated 6.3 public-source bootstrap. Reject default/latest/guessed-version and any invalidated bootstrap attempt.

### Q63-26 — Frozen profile/resource integrity

5.16/6.0/6.1/6.2 profile/resource tree identities remain byte/behavior identical. 6.3 is distinct and version-bound.

### Q63-27 — Full generated/package/Core acceptance

After the semantic candidate and again after recovery mapping, validate canonical package build, standalone link/resource closure, committed `dist` parity, packaged snapshot parity, profile identity, and closest supported orchestrator/Core ingestion.

### Q63-28 — Self-hosted backfill statistics

Independently reconstruct every Hot self-hosted family and a risk-based sample of Warm/Cold families from underlying evidence. Displayed statistics equal valid ledger rows and coverage claims are no broader than the inspected corpus.

### Q63-29 — Closeout learning transaction

A qualified recurrence/success that meets admission threshold updates PEM before final closeout. A non-material local repair does not create noise merely to satisfy the feature.

### Q63-30 — Version/recovery/Protocol-7 lifecycle

Verify distinct 6.3 bootstrap versus recovery identity, late recovery mapping publication, mapping-bearing regeneration, authority-index/semantic-evolution reconciliation, and bounded Protocol 7 inheritance update without D3 architecture mutation.

## 17. Falsification

The four Protocol 6.2 Challenge falsifications remain mandatory and unchanged in semantic purpose:

1. **Loss test** — find a compacted/generalized item whose removal loses an edge case, authority/evidence boundary, compatibility rule, trigger, or salience; restore it at the correct owner.
2. **Scope/materiality laundering test** — attempt to pass by shrinking scope or calling globally preserved doctrine non-material because it is cold locally; reject it.
3. **Priority-inversion test** — make high-importance memory prominent, then verify every lower-salience mandatory active constraint still survives closure.
4. **False-compaction test** — reject a change that merely moves links, flattens routing, uses stale summaries, creates a parallel registry, or leaves normal context unnecessarily dense.

Add Protocol 6.3-specific falsification passes:

### F63-A — Speculation laundering

Promote `this seems faster` with no suitable evidence. Expected: no Proven/current positive lesson.

### F63-B — Statistical inflation

Turn one causal defect into many occurrences via failing tests/files. Expected: rejected unless independent causal introduction is demonstrated.

### F63-C — Family overgeneralization

Group superficially similar but semantically different failures. Expected: split/review-required, not inflated recurrence.

### F63-D — Incomplete-history false cold

Show one found occurrence under partial coverage and claim the family is Cold because no others were found. Expected: rejected/Unassessed absent adequate coverage.

### F63-E — Cargo-cult positive pattern

Apply a historically successful technique outside its assumptions or while violating governing correctness. Expected: historical success does not qualify the new use.

### F63-F — Summary/evidence recursion

Use PEM or a derived summary as the sole warrant for its own claim. Expected: follow to admissible underlying evidence or leave the claim unsupported.

### F63-G — Stale-green/stale-red laundering

Use an old passing or failing result after material candidate/oracle/regime change. Expected: reject as current evidence until applicability is re-established.

### F63-H — Common-mode fake independence

Count several correlated tests as independent support. Expected: common-mode risk remains explicit.

### F63-I — Architectural ossification

Remove a historical mechanism while preserving its demonstrated capabilities with a simpler qualified design. Expected: allowed.

### F63-J — History-compression loss

Compact/split/merge family records and attempt to lose an occurrence, contradictory observation, limit, or lineage. Expected: blocking.

### F63-K — False quantitative generalization

Use one microbenchmark to claim global scaling/performance superiority. Expected: claim narrowed/rejected.

### F63-L — Eager memory regression

Make every task scan/load PEM/history because memory might be useful. Expected: reject; bounded triggers and cold routes must remain explicit.

### F63-M — Project-memory package contamination

Package the live SSDP project PEM inside the generic 6.3 skill/profile. Expected: reject; only doctrine/template belongs in generic distribution.

## 18. Implementation stages

### Stage A — Baseline capture, owner census, and preservation map

1. Reconfirm the exact accepted 6.2 identities listed in Section 1 against repository truth.
2. Build the finite artifact census and T01-T39 independent preservation mapping.
3. Identify exact current owners and all source/generated/profile/package consumers.
4. Append T40+ 6.3 hypotheses and acceptance oracles.
5. Record which 6.2 evidence remains applicable and which will require rerun after each planned owner change.

**Gate:** no protocol-source mutation before the finite no-loss map is complete enough to bound the change.

### Stage B — Canonical doctrine and PEM representation

1. Add the smallest justified `project-engineering-memory.md` concern owner or, if Stage A demonstrates an existing owner is sufficient, integrate there instead and record why no new owner is needed.
2. Implement the canonical PEM/template schema, coverage, admission, family/statistics/temperature, evidence-binding, contradiction/retirement, and positive/negative learning rules.
3. Update existing evidence, convergence, architecture, workflow, documentation, repository, testing, and version owners only with their local consequences/routes.
4. Keep universal kernel additions minimal.

**Gate:** one semantic owner per rule; no duplicated generic doctrine or hidden prerequisite.

### Stage C — Routing/workflow/project-local integration

1. Add visible conditional routes from relevant D3/D4/workflow entrypoints without making PEM universal hot context.
2. Implement Historical Applicability Set and capability-transfer handoff requirements.
3. Implement project-local discovery and missing/partial-memory behavior.
4. Extend closeout/impact closure so only admitted material learning updates PEM.

**Gate:** first-local-defect and cold-route cases prove no eager memory/history activation.

### Stage D — Structural validation and self-hosted backfill

1. Extend existing validation surfaces for canonical Markdown structure, evidence resolution, derived counts, lineage, coverage, temperature, and active-summary integrity.
2. Create SSDP's project-local `PROJECT-ENGINEERING-MEMORY.md` from actual historical evidence.
3. Qualify seeded families; do not infer counts from recollection.
4. Ensure no live project memory enters generic packages.

**Gate:** independent reconstruction reproduces all Hot statistics and a risk-based sample of the remainder.

### Stage E — 6.3 bootstrap, profile, semantic candidate, and generated descendants

1. Complete and validate self-reference-safe 6.3 public-source set.
2. Create immutable 6.3 public-source bootstrap.
3. Publish its exact identity only in a later semantic-candidate/publication commit.
4. Add distinct 6.3 profile/snapshot; leave 5.16/6.0/6.1/6.2 frozen.
5. Regenerate/package from canonical source and validate all local routes/links/parity/Core ingestion.

**Gate:** bootstrap and semantic candidate are distinct, exact, self-reference-safe identities.

### Stage F — Qualification and independent Review

1. Run complete affected repository/package/orchestrator regression.
2. Re-run all 115 Protocol 6.2 semantic scenarios against 6.3.
3. Run Q63-01 through Q63-30 and F63-A through F63-M.
4. Compare representative 6.2/6.3 static activation traces; use metrics only as sensors.
5. Separately obtain live routing/performance evidence for any live empirical claim actually made; otherwise mark it unavailable.
6. Prepare a snapshot-complete independent-review handoff.
7. Perform independent D3/protocol Review over the assembled semantic candidate, not only diff/implementer summary/preservation labels.

**Gate:** no PASS with a missing required check, stale evidence, hidden contradiction, or unresolved preservation row.

### Stage G — Recovery, current-state reconciliation, and closeout

1. Choose immutable 6.3 recovery only after Stage F PASS.
2. Publish recovery mapping only in a later descendant commit.
3. Regenerate mapping-bearing descendants and rerun targeted recovery/parity/package/Core acceptance.
4. Reconcile current semantic evolution, authority index, version/portability/navigation, and project-local PEM.
5. Reconcile Protocol 7 representation/version inheritance only after 6.3 acceptance; preserve its existing D3 reopen prerequisite and architecture semantics unless separately reopened.
6. Archive this workplan only when all current 6.3 semantics reside at canonical owners and impact closure is complete.
7. Do not merge/cut over `main` without separate authorization.

## 19. Independent Review handoff

Create `qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md` (or the established equivalent naming convention) only after implementation/qualification evidence is ready.

It SHALL bind at least:

```text
accepted 6.2 recovery and current branch-point ancestry
6.3 public-source bootstrap
6.3 semantic candidate
6.3 preservation census/map with T01-T39 and T40+
self-hosted PEM + declared coverage
qualification/requalification evidence
static activation evidence
available live evidence with exact claim scope
generated/package/profile evidence
frozen-profile tree identities
candidate-to-evidence descendant range
known red/unavailable observations
```

The reviewer MUST reconstruct governing semantics independently, treat the census/PEM/qualification reports as falsifiable evidence rather than authority, inspect high-risk current owners directly, verify the assembled source/generated/package/profile state, and ensure no semantic mutation occurred after the bound candidate without affected requalification.

## 20. Acceptance and No-Pass criteria

### 20.1 PASS

Protocol 6.3 passes only when:

- every accepted 6.2 doctrine/still-valid historical capability is preserved;
- T01-T39 independently remain preserved and all new transformation rows close;
- current D1-D4 authority remains distinct from evidence and PEM;
- PEM is compact, project-local, current, evidence-backed, coverage-aware, and non-authoritative;
- positive and negative learning are both represented without turning ordinary bug chronology into a permanent ledger;
- family membership, split/merge lineage, counts, coverage, temperature, and active summary are independently reproducible;
- stale/correlated/contradictory evidence is handled under existing 6.2 evidence semantics;
- quantitative/complexity claims are no broader than their evidence;
- historical mechanism replacement remains possible while demonstrated capabilities remain accounted for;
- bounded activation prevents ordinary routes from performing history/memory work unnecessarily;
- all 115 inherited scenarios and all required 6.3 qualification/falsification pass;
- exact 6.3 bootstrap/recovery/profile/fallback lifecycle passes;
- frozen 5.16/6.0/6.1/6.2 bytes/behavior remain intact;
- source/generated/package/profile/Core acceptance passes;
- Protocol 7/current lifecycle reconciliation is bounded and correct;
- independent Review finds no genuine blocker or Serious Challenge.

### 20.2 NO-PASS

Any of the following is blocking:

- PEM/tests/commits/history treated as semantic authority;
- loss/weakening/orphaning of accepted 6.2 semantics;
- workplan scope shrunk to avoid a relevant historical/preservation obligation;
- a partial memory used to prove absence or Cold status;
- family recurrence manufactured from symptoms/textual similarity;
- counters not reproducible from evidence rows;
- unsupported success guidance presented as established project knowledge;
- a performance gain accepted despite violated governing correctness/constraints;
- stale passing/failing evidence used as current confirmation/refutation;
- contradictory admissible evidence hidden;
- historical mechanism preserved merely because memory mentions it;
- demonstrated capability silently lost during rework;
- Hot ranking hides a lower-salience mandatory active constraint;
- first local defects forced into permanent memory without admission rationale;
- eager full-history/PEM activation on ordinary routes;
- live model/performance claims inferred only from static sensors;
- live project PEM packaged as generic protocol content;
- frozen profile/resource drift;
- default/latest/guessed-ref 6.3 fallback;
- package/generated/profile divergence;
- semantic mutation after candidate without affected requalification;
- diff-only/summary-only independent Review;
- recovery mapping published before immutable recovery exists;
- Protocol 7 architecture silently changed by a 6.3 representation/version reconciliation.

## 21. Reopen and repair rule

If implementation or independent Review finds a genuine blocker:

- route to the earliest owning D1/D2/D3/D4 or concern layer;
- reopen this workplan only when its accepted D3/cycle contract must change;
- give precise owning-layer repair instructions;
- prefer removal, narrowing, rewiring, consolidation, or re-derivation over compensating wrappers/machinery;
- rerun only affected evidence while preserving demonstrably unaffected evidence;
- update PEM when the repaired episode itself meets the admitted learning threshold.

A Serious Challenge is raised only when accepted governing authority itself appears materially defective; ordinary implementation misses remain ordinary blockers.

## 22. Workplan closure review

**WORKPLAN CLOSURE REVIEW: PASS AFTER REPAIR.**

This review reconstructed the accepted Protocol 6.2 baseline from current canonical owners, the archived 6.2 workplan, preservation census, independent Review, evidence owner, convergence owner, architecture/workflow/documentation/versioning owners, and the current workplan authority index.

The repaired workplan closes the material pre-implementation gaps found under Protocol 6.2:

- evidence/history is no longer mislabeled as semantic authority;
- a finite Protocol 6.2 artifact census and transformation proof map are mandatory;
- evidence applicability, stale-state, common-mode risk, bounded invalidation, and exact durable evidence binding now govern PEM;
- incomplete historical coverage cannot manufacture negative evidence or Cold confidence;
- semantic family membership, split/merge lineage, first-local-defect locality, and admission thresholds preserve existing convergence doctrine;
- counts are derived from canonical evidence rows rather than manually accumulated state;
- temperature/confidence/applicability are orthogonal and metrics remain sensors rather than verdicts;
- PEM has explicit canonical ownership, project-local/package separation, and bounded activation rather than universal loading;
- mechanism replacement uses capability-transfer evidence without architectural ossification;
- the 6.3 public bootstrap/profile/semantic-candidate/recovery/generated lifecycle now preserves the proven 6.2 staging discipline;
- static versus live empirical claims and Protocol 7 inheritance reconciliation are explicit closure obligations.

No Serious Challenge to accepted Protocol 6.2 authority is identified. Implementation is authorized on the dedicated Protocol 6.3 branch subject to the gates above. Protocol 6.3 itself remains proposed and does not become accepted-current until Stages A-G and independent Review/closeout pass.

## 23. Intended end state

```text
lossless accepted Protocol 6.2 semantics
+ exact historical evidence remains cold and recoverable
+ one compact current project-engineering memory
+ evidence-backed negative and positive learning
+ statistics with declared coverage instead of guessed certainty
+ proven engineering instincts without architectural dogma
+ demonstrated capabilities preserved across mechanism replacement
+ bounded decision-driven activation
+ no routine history replay
+ qualification proportional to the claim
+ fresh-context agents that inherit project experience rather than rediscover it
```

The central Protocol 6.3 invariant is:

> The project must be able to learn even when the individual agent does not persist, and what it claims to have learned must remain traceable to admissible evidence rather than memory, preference, or repetition.
