---
kind: abstraction-concretization-change-plan
workplan_id: PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY
protocol_version: 6.2.0
target_protocol_version: 6.3.0
status: active
created_date: 2026-09-11
reviewed_date: 2026-09-11
second_reviewed_date: 2026-09-11
design_closure_status: pass-after-second-review-repair
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

The **Scientific Software Development Protocol (SSDP)** preserves detailed engineering history in Git, workplans, reviews, qualifications, semantic-evolution records, generated/package evidence, and immutable protocol recovery snapshots. Protocol 6.2 made that sophistication cheaper to use through lossless representation and progressive disclosure, but a fresh-context engineer can still miss project-specific lessons distributed across long historical evidence chains.

Protocol 6.3 adds a compact, current, evidence-backed learning layer without replacing history, creating a fifth authority domain, or turning historical success into architectural dogma.

For this plan:

- **Project Engineering Memory (PEM)** — a compact, project-local, non-authoritative representation of demonstrated engineering lessons, recurring failure families, successful patterns, important discoveries, capability lessons, and high-impact current notices, with exact routes to supporting evidence and governing authority where one exists;
- **historical evidentiary corpus** — durable project evidence from which PEM findings are assessed, including commits, workplans, reviews, qualification records, tests, benchmarks, profiles, analyses, semantic-evolution records, and other applicable observations; this corpus is evidence/provenance, not D1-D4 authority;
- **evidence binding** — a resolvable, normally immutable reference from a PEM claim to the evidence specification/realization/observation/assessment that warrants it;
- **learning family** — a stable generalized project lesson. Failure-family membership follows the existing convergence rule: materially equivalent manifestations share a governing invariant, semantic owner/authority class, and materially equivalent failure mechanism; textual similarity or a broad subsystem label is insufficient;
- **occurrence** — one independently introduced or independently existing confirmed manifestation of a failure family; one cause producing many symptoms is normally one occurrence;
- **evaluated application** — one materially distinct attempt to apply a positive pattern under a declared regime, with an admissible outcome assessment of supporting, neutral/no-demonstrated-benefit, contradicting, or inconclusive;
- **successful application** — an evaluated application whose claimed benefit and governing constraints are supported by admissible evidence;
- **coverage state** — the declared extent to which the historical corpus has been examined for a family or PEM instance; absence from incomplete memory is not evidence of absence;
- **memory temperature** — an importance/attention classification (`HOT`, `WARM`, `COLD`, or `UNASSESSED`) derived from confirmed recurrence/application statistics plus explicit evidence-backed impact promotion; memory temperature is distinct from Protocol 6.2 hot-path/cold-path activation state and is never authority or an acceptance threshold;
- **evidence maturity** — confidence in a bounded finding (`PROVISIONAL`, `SUPPORTED`, or `PROVEN`), kept distinct from current applicability/conflict/retirement state;
- **authority binding** — the relation between a capability lesson and current accepted semantic authority: `EVIDENCE_ONLY`, `AUTHORITY_BOUND`, or `PROPOSED_FOR_PROMOTION`; only an `AUTHORITY_BOUND` capability is mandatory, and it is mandatory because of its cited current D1-D4/project owner, not because PEM says so;
- **lifecycle context** — where an occurrence/application was observed, such as development branch, qualification, accepted-current runtime, production, recovery/migration, or historical-only regime; this prevents development observations from being misrepresented as production incidence;
- **Historical Applicability Set (HAS)** — the bounded current-work record stating which materially relevant PEM families/capability lessons apply, do not apply with reason, or require deeper evidence inspection;
- **capability-transfer map** — a mapping from a replaced mechanism to each materially relevant learned capability, its authority-binding state, governing owner when any, replacement owner/mechanism or deliberate retirement, and verifying evidence;
- **fresh-context agent** — an agent or engineer that does not carry reliable private conversational memory of prior project cycles and therefore must recover project state from durable artifacts.

The goal is not a bug database, universal project graph, mandatory archaeology pass, or cautious freeze on change. The goal is to give a fresh-context agent the smallest complete project-aware representation of engineering experience likely to improve the current decision while retaining exact evidence, uncertainty, contradictory outcomes, and current authority boundaries.

## 1. Outcome, authority, baseline, and scope

Protocol 6.3 SHALL be a backward-compatible minor strengthening of accepted Protocol 6.2. It adds evidence-backed engineering-memory semantics and workflow integration without weakening accepted D1-D4 authority, evidence, Challenge, compatibility, representation, routing, package, profile, security, or lifecycle rules.

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

The recovery identity is the immutable semantic/rollback baseline. Later mapping/generated/main descendants are separately relevant to current document-control, generated/package parity, and ancestry. Do not collapse these identities.

Protocol 6.2 remains accepted-current until Protocol 6.3 completes semantic qualification, independent Review, immutable public bootstrap, recovery mapping, generated/profile/package reconciliation, semantic-evolution/authority-index reconciliation, affected Protocol 7 inheritance reconciliation, and lifecycle closeout. Version-bound older work remains governed by its declared version; a newer installed skill never silently reinterprets it.

This workplan has no semantic-supersession escape hatch. If implementation reveals that accepted 6.2 authority is materially false, contradictory, inadequate, or impossible to preserve coherently, stop at the earliest affected owner and use the existing Challenge/Serious Challenge process. A PEM edit cannot choose new semantic truth.

### 1.1 Accepted 6.2 preservation baseline

Protocol 6.3 MUST preserve every accepted Protocol 6.2 doctrine and still-valid historical capability, including at minimum:

- complete T01-T39 semantic preservation as independently reviewed under 6.2;
- feasibility/admissibility before optimization and minimum justified total complexity;
- authority provenance, one current semantic owner, precedence, evidence-not-authority, and bounded human ratification;
- D1-D4 directed-acyclic-graph routing, reduced routes, multi-parent fidelity/adequacy review, bounded invalidation, Challenge/Serious Challenge, and composed closure;
- D1, D2, D3, and D4 owner semantics;
- documentation, repository-hygiene, maintenance-audit, evidence, testing, workflow, long-horizon, language/tool, security, performance, storage, release, debugging, Git, and other concern-owner semantics;
- root-cause/semantic-family reasoning, first-clean-local-defect locality, recurrence-driven simplification, and removal/rewiring before compensating machinery;
- snapshot-complete handoffs and validity-scoped context reuse;
- current-vs-history separation and semantic-evolution provenance;
- evidence specification/realization/observation/assessment, applicability, stale evidence in both polarities, evidentiary target versus execution dependency, independence/common-mode risk, and bounded impact closure;
- proxy-proof/real-owner testing, stage-local plus final assembled acceptance, qualification separation, failure paths, and missing-required-check blocking;
- lossless representation, anti-scope-laundering, importance-weighted attention without acceptance loss, one detailed owner per generic rule, bounded typed progressive disclosure, cold-path reachability, non-activating ordinary links, and derived-view non-authority;
- Protocol 6.2 replacement-bootstrap discipline and exact immutable fallback;
- repaired software-documentation cold routes and standalone reachability;
- static activation sensors as structural evidence rather than live-model performance proof;
- immutable 5.16/6.0/6.1 resources and current 6.2 profile behavior/identity;
- source/generated/package/snapshot parity and canonical-generation ownership;
- all 115 accepted Protocol 6.2 behavioral scenarios plus both affected requalifications and Stage G acceptance;
- current abstraction/concretization nomenclature while frozen historical identities remain unchanged;
- the human-facing background/terminology/first-use abbreviation standard;
- assembled-candidate independent Review rather than diff/summary/green-status acceptance;
- immutable bootstrap versus recovery separation and the rule that default/latest is never a protocol-version oracle.

T01-T39 are preservation/review hypotheses and evidence labels, not semantic authority. Current accepted owners remain authority.

### 1.2 Non-goals

Protocol 6.3 MUST NOT:

- replace Git, semantic evolution, workplans, qualifications, or archived evidence with PEM;
- turn tests, benchmarks, commits, history, statistics, or PEM into D1-D4 authority;
- preserve every ordinary bug fix as permanent memory;
- force family census for a first clean local defect merely because siblings are imaginable;
- make historical mechanisms immutable merely because they once worked;
- treat frequency, temperature, benchmark magnitude, review count, or a success count as an acceptance threshold or probability estimate;
- introduce a universal database, graph, daemon, background indexer, or second routing registry;
- load PEM/project history unconditionally for every task;
- scan all Git history on every bootstrap or recompute all statistics on every read;
- create separately maintained Markdown and JSON/YAML authorities for the same memory;
- copy secrets/private data into PEM or durable evidence merely for completeness;
- rewrite archived workplans or frozen protocol/profile resources to match 6.3 terminology;
- broaden a local memory feature into unrelated Protocol 7 control-plane implementation;
- merge/cut over to `main` without separate authorization.

## 2. Governing 6.3 rules

### 2.1 Evidence-backed learning

Project memory stores conclusions together with their warrant.

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

A plausible idea, author preference, attractive implementation, repeated phrase, or existing mechanism is not project knowledge merely because it exists.

Statements such as `this should be faster`, `this seems cleaner`, or `this might scale better` remain hypotheses until evidence suitable to the bounded claim exists.

Conversely, evidence is not authority. Qualification is an acceptance gate for a bounded claim under its governing authority and evidence assessment; it does not become a fifth semantic domain and does not automatically prove that an oracle, model, architecture, or generalization is correct.

### 2.2 Admissibility before optimization

A positive engineering pattern is admissible only when it satisfies all applicable correctness, D1/D2, architecture, compatibility, security, reliability, resource, and external constraints.

A faster implementation that violates accepted semantics is not a successful optimization. Record gains with material costs, tradeoffs, uncertainty, and regime.

### 2.3 Historical evidence is a prior, not a veto or authority

Past success creates an evidence-backed preference, not architectural immunity. Past failure creates an evidence-backed warning, not permanent prohibition.

A new approach MAY replace a proven historical approach when it:

1. considers applicable historical evidence;
2. identifies materially relevant learned capabilities and their authority-binding state;
3. preserves every `AUTHORITY_BOUND` capability because its cited owner requires it;
4. explicitly evaluates `EVIDENCE_ONLY` capabilities as design priors rather than silently treating them as invariants;
5. keeps governing parents/side constraints fixed unless explicitly reopened;
6. supplies evidence appropriate to new claims; and
7. passes affected acceptance/qualification.

An evidence-only capability may be deliberately discarded when a better admissible design justifies doing so. Promotion from evidence-only lesson to mandatory architecture requires acceptance by the actual D1-D4/project owner; PEM cannot perform that promotion itself.

### 2.4 Positive evidence must include counterevidence

Once a success pattern exists, materially applicable evaluated attempts under its declared regime must not be selectively omitted because they were neutral, failed, contradicted the generalized claim, or were inconclusive. The current assessment may keep raw detail cold, but it must preserve a route to material counterevidence and narrow/split/reclassify the pattern when warranted.

### 2.5 Statistics are descriptive unless a denominator exists

Occurrence/application counts are evidence-bound descriptive counts under declared coverage. They do not by themselves estimate failure probability, success probability, comparative risk, causal strength, or incidence rate. Any rate/probability claim requires an explicit opportunity/exposure denominator and defensible sampling/measurement basis.

## 3. Finite representation census and no-loss map

Before protocol-source mutation, Stage A SHALL create `qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md` as non-authoritative implementation/review evidence.

The census SHALL enumerate every current durable/generative Protocol 6.2 representation surface before deciding what is touched, including:

- all four `source/roles/*/SKILL.md` entrypoints and three current specialist entrypoints;
- all current `source/shared/references/*.md`;
- all current shared templates plus the proposed PEM template;
- `AGENTS.md`, root/source `README.md`, `PORTABILITY.md`, `source/SEMANTIC_DEPENDENCIES.md`, and `source/PROTOCOL_VERSION`;
- workflow-prompt source;
- current Protocol 6.2 profile/prompts/snapshot resources and proposed 6.3 successors;
- protocol-bearing schemas/renderers/help/status text affected by this feature;
- qualification scenario/routing/package assets;
- active workplan authority index and this workplan;
- `history/SEMANTIC_EVOLUTION.md` as append-only cold history at closeout;
- archived workplans as frozen cold evidence;
- `dist/` and generated snapshots as generated descendants;
- frozen 5.16/6.0/6.1/6.2 resources.

Classify each as `refactor`, `route-only`, `new`, `generated`, `frozen/historical`, or `intentionally unchanged with reason`.

For every materially changed accepted obligation, record:

```text
preservation ID
accepted 6.2 owner/location
6.3 owner/location
governed obligation
preservation/generalization relation
oracle/evidence that can detect loss
disposition: PRESERVED or BLOCKING
```

Green tests or labels do not prove preservation. Independent Review challenges the map against actual owners and the assembled candidate.

### 3.1 Required appended 6.3 preservation hypotheses

After independently reproducing T01-T39 unchanged, append the next available IDs for at least:

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
T51 Historical Applicability Set for materially memory-relevant work
T52 mechanism-to-capability transfer accounting
T53 justified promotion of repeated lessons into owner-backed invariants/sensors
T54 mandatory material closeout learning assessment
T55 quantitative effect-size and experimental-envelope preservation
T56 contradictory evidence and retirement without historical erasure
T57 evidence applicability/staleness and bounded invalidation of PEM
T58 evidentiary independence/common-mode-risk preservation
T59 active-summary progressive disclosure and cold detail reachability
T60 project-local PEM versus packaged protocol/template separation
T61 single canonical Markdown memory; derived indexes subordinate
T62 6.3 bootstrap/profile/recovery/version-bound compatibility staging
T63 frozen 5.16/6.0/6.1/6.2 profile/resource preservation
T64 generated/package/source parity and exact-ref fallback
T65 static-versus-live claim discipline for context/performance claims
T66 Protocol 7 inheritance/current-lifecycle reconciliation
T67 human-facing background/terminology/abbreviation completeness
T68 independent assembled-candidate qualification/Review
T69 anti-scope-laundering and lower-salience mandatory-constraint preservation
T70 no recursive summary/evidence laundering
T71 preservation-capability authority binding; PEM cannot mint invariants
T72 self-reference-safe routine PEM evidence/update staging
T73 balanced positive-pattern supporting/neutral/contradicting/inconclusive evidence
T74 descriptive-count versus incidence/rate/probability distinction
T75 memory-temperature versus hot/cold activation-state separation
T76 accepted/base versus branch-candidate PEM lifecycle and merge reconciliation
T77 stable accepted IDs, collision-safe pre-acceptance ID reconciliation, no ID reuse
T78 security/trust/privacy constraints on PEM/evidence persistence
T79 owner-responsible learning assessment and bounded PEM update classes
T80 cross-domain D1-D4/specialist applicability without universal activation
T81 current-owner deduplication when a project lesson becomes accepted doctrine
T82 occurrence/application lifecycle-context preservation
```

If the accepted census already uses later IDs, append rather than collide. These IDs remain preservation evidence, not authority.

## 4. Canonical owner and routing architecture

### 4.1 One detailed owner per generic rule

Intended owner topology:

```text
universal authority / Challenge / lossless representation
  -> source/shared/references/abstraction-and-concretization.md

PEM schema / compact representation / coverage / family records
  -> source/shared/references/project-engineering-memory.md

evidence lifecycle / applicability / stale state / independence / impact
  -> evidence-evolution-and-dependencies.md

recurrence / semantic-family membership / first-local-defect / simplification
  -> convergence-and-cycle-economy.md

D3 accepted capability / mechanism replacement / architecture transfer
  -> architecture-and-design.md

workflow activation / HAS / handoff / closeout update responsibility
  -> workflow-and-workplans.md

current-vs-history lifecycle / source-chain reconciliation
  -> documentation-maintenance.md

testing / benchmark / oracle / acceptance methodology
  -> testing-and-validation.md

version / bootstrap / recovery / profile / fallback
  -> protocol-versioning-and-compatibility.md

repository-context reuse / historical intake economy
  -> repository-intake.md

PEM data/evidence trust, secret/private-data handling, least privilege
  -> security-and-trust-boundaries.md
```

`project-engineering-memory.md` owns only PEM-specific semantics and routes generic evidence/family/workflow/security/version doctrine to existing owners rather than restating them. The universal kernel receives only the minimum route/constraint needed to keep PEM subordinate and discoverable; PEM is not universal-kernel material.

If Stage A finds accepted 6.2 ownership differs, preserve that owner or block and resolve ownership before implementation. Do not create a parallel owner to match this proposed map.

### 4.2 Project-local canonical artifact

Default project-local artifact:

```text
PROJECT-ENGINEERING-MEMORY.md
```

at the governed project/repository root unless existing project authority explicitly declares one alternative canonical path. The artifact declares its project/scope identity sufficiently to prevent accidental reuse in an unrelated repository or subproject. Do not invent a hierarchy of nested memories unless a real multi-project ownership boundary requires one; if such a boundary exists, make precedence/scope explicit rather than relying on nearest-file discovery.

Add one packaged protocol template, proposed as:

```text
source/shared/templates/project_engineering_memory_template.md
```

The live project instance is project state and SHALL NOT enter generic SSDP `dist/` skill packages or orchestration profiles. The template and protocol instructions are canonical protocol source and follow normal generated/package closure. In the SSDP repository, self-hosted `PROJECT-ENGINEERING-MEMORY.md` is ordinary project-local content.

Do not maintain a second hand-authored JSON/YAML database. A generated index may exist only for a demonstrated consumer need; it must be reproducible from canonical Markdown and explicitly non-authoritative.

### 4.3 Bounded cross-domain activation

Preferred shape:

```text
task
 -> active D1/D2/D3/D4 role or specialist root
      -> universal kernel + current domain owner
      -> only when a project-memory predicate is material: project-engineering-memory.md
           -> project-local PEM active summary
                -> relevant family/current notice only
                     -> underlying evidence only when needed
```

Triggers include:

- material rework of existing D1/D2/D3/D4 project semantics or mature concretization where prior project lessons can change the decision;
- replacement/consolidation of mature machinery with learned capabilities;
- a defect believed to recur or belong to an existing semantic family;
- substantial optimization/performance/scaling rework of existing machinery or algorithms;
- migration/recovery work where prior project choices can change the decision;
- an active workplan explicitly binding relevant PEM entries.

A first clean local defect with no recurrence/generalization signal remains local. Ordinary documentation, trivial implementation, or unrelated cold concerns do not load PEM because it exists.

**Memory temperature does not itself activate context.** A `HOT` family unrelated to the current governed question remains cold/unloaded. A `COLD` family may become active when its applicability predicate is materially triggered. Ordinary links, package membership, semantic dependencies, or PEM existence do not activate it.

### 4.4 Missing/partial memory and adoption

Missing/partial PEM is not proof of no historical lesson.

For a new project with no material history, initialization may create an empty PEM with explicit coverage state. For an established project adopting 6.3:

- ordinary work may continue without full backfill;
- before a memory-triggering substantial rework, perform bounded relevant historical intake or establish/update PEM coverage for the affected scope;
- if required coverage cannot be established, preserve uncertainty and never claim relevant families are absent;
- version-bound 6.2 work does not retroactively acquire 6.3 obligations unless it explicitly adopts 6.3 after compatibility/impact reconciliation.

## 5. Canonical PEM representation

PEM is current engineering-learning representation, not patch history. Detailed chronology remains in Git/history/evidence artifacts.

### 5.1 Global metadata and coverage

PEM SHALL expose enough metadata to judge applicability without loading history:

```text
memory_schema_version
maintained_under_protocol
project/repository/scope identity
memory_lifecycle_state
coverage_state
coverage_basis: bounded owners/surfaces/history range/sources reviewed
reconciled_through: already-existing immutable accepted project identity
known unreviewed ranges/surfaces when material
open review-required families/notices
```

Coverage states include at least:

```text
UNINITIALIZED
PARTIAL
RECONCILED_FOR_DECLARED_SCOPE
```

`RECONCILED_FOR_DECLARED_SCOPE` means the declared bounded corpus/surface was reviewed sufficiently for represented claims/counts. It claims nothing outside that scope.

Memory lifecycle distinguishes at least accepted/base project memory from branch-candidate memory. A feature-branch PEM edit is a candidate representation for that branch; it does not silently become project-wide accepted memory before merge/acceptance.

`reconciled_through` names already-existing accepted history. PEM never requires the commit containing the PEM edit to self-name.

### 5.2 Active engineering memory

The beginning of PEM SHALL answer compactly:

```text
What repeatedly fails here?
What repeatedly works here?
What learned capabilities should I consider, and which are actually authority-bound?
What high-impact current notices matter?
What evidence-backed engineering instincts are useful now?
```

Each summary item should carry only:

```text
stable ID
kind
one-line bounded lesson
memory temperature
evidence maturity/current applicability
authority-binding state where relevant
confirmed/supporting count plus visible material counterevidence signal
primary applicability trigger
short evidence/authority route
```

No arbitrary token threshold may delete material entries. If dense, generalize genuinely equivalent families, remove duplication, and make detail cold while preserving routes. Metrics are sensors, not thresholds.

A task-specific selected view may be generated transiently from PEM but remains derived coordination state, never a maintained authority.

### 5.3 Current notices

A small current-notice section MAY represent a high-impact project fact that materially affects engineering now but is not a generalized family.

A notice requires:

```text
stable notice ID
current claim/state
governing owner when normative, otherwise explicit non-authoritative/provisional status
source/evidence route
applicability
review/expiry condition
```

A notice cannot become shadow authority. Notices do not contribute to family counts and must be retired or converted when their lifecycle changes.

## 6. Learning-family schema, admission, and identity

### 6.1 Family kinds

At minimum:

```text
FAILURE_FAMILY
SUCCESS_PATTERN
DISCOVERY
PRESERVATION_CAPABILITY
```

Current identifiers use one consistent namespace:

```text
FF-###  failure family
SP-###  success pattern
DS-###  discovery
PC-###  preservation capability
```

Occurrence/application IDs are family-scoped (`O01`, `A01`, ...). Historical aliases remain only where migration evidence requires them.

### 6.2 Admission threshold

PEM is not a permanent ledger of ordinary fix chronology. Admit/materially update a family only when evidence supports at least one:

- materially recurring same semantic failure mechanism;
- reintroduction after accepted repair;
- one high-impact incident exposing a broadly reusable lesson/capability;
- optimization/simplification with meaningful demonstrated benefit likely to matter again;
- repeated independent successful use;
- discovery materially changing preferred project approach to recurring work;
- mechanism replacement/generalization/rejection/restoration whose rationale is likely to prevent rediscovery;
- current high-risk issue best represented as temporary notice rather than false family generalization.

A first clean local defect normally remains local. Generic textbook knowledge or generic protocol doctrine belongs at its owner, not PEM.

### 6.3 Failure-family membership

Failure-family membership requires materially equivalent:

1. governing invariant;
2. semantic owner/authority class; and
3. failure mechanism/cause at the level relevant to repair.

Common symptoms, error messages, file locations, or subsystem labels are insufficient. Uncertain classification stays `PROVISIONAL`/review-required.

### 6.4 Success/discovery/capability minimum fields

A success pattern states its bounded claim, applicable regime, evaluated applications, supporting and counterevidence, demonstrated benefit/cost, and limits.

A discovery states the changed project understanding, exact evidence, applicable regime, competing prior interpretation when material, and whether any current authority was changed separately.

A preservation capability states the capability, applicability, authority-binding state, governing owner if `AUTHORITY_BOUND`, evidence showing why it matters, and mechanism independence. `EVIDENCE_ONLY` capability lessons are strong design context but not mandatory.

### 6.5 Split, merge, reclassification, and accepted ID stability

For split:

- retain predecessor ID as historical/superseded lineage;
- reassign occurrences to justified children;
- avoid double-counting one event across aggregate views.

For merge:

- create/select current generalized family;
- retain predecessor IDs as lineage/aliases;
- deduplicate overlapping event/application identities;
- preserve distinct causes/limits rather than flattening them.

A reclassification changes current interpretation, not historical observation.

An ID becomes stable/no-reuse once present in accepted project memory. New branch-local IDs are provisional until project acceptance. Concurrent branches may choose colliding provisional IDs; merge/rebase reconciliation must resolve collisions before acceptance, update branch-local references, and never renumber an already-accepted ID merely for compactness. Retired accepted IDs are never recycled.

Cherry-picked/rebased copies of the same underlying historical event are provenance aliases, not new occurrences. Deduplicate by the underlying event/evidence identity and causal episode rather than commit-count arithmetic.

### 6.6 Promotion into current doctrine

If a project lesson later becomes explicit accepted D1-D4/project doctrine, the current owner governs. PEM then either:

- retains only compact project-specific recurrence/evidence context that still improves future decisions and points to the owner; or
- retires/removes redundant active guidance while preserving historical lineage.

Do not duplicate generic current protocol doctrine in self-hosted PEM merely to praise it. A project-specific success pattern that adds measured local evidence may remain, but it routes to the current owner and cannot become a second statement of the rule.

## 7. Evidence model, bindings, and security

### 7.1 Inherit complete Protocol 6.2 evidence lifecycle

```text
governed claim
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

For material entries preserve enough to judge applicability:

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
lifecycle context
```

A rerun on a changed candidate is a new realization. Old results are not rewritten into evidence for a new subject.

### 7.2 Exact durable evidence and self-reference-safe update staging

Prefer immutable Git commit + path + stable section/test/finding identifier. A branch/default-branch path alone is insufficient for a long-lived material warrant because later edits can change meaning.

If external CI/benchmark evidence can expire, preserve a compact durable repository record containing the material observation and exact external run/candidate identity when long-lived PEM depends on it.

PEM, generated summaries, implementer narrative, or recursively compressed memory cannot be the sole warrant for their own substantive claim.

A routine PEM update must not recreate the Git self-reference defect fixed by Protocol 6.2. When the new occurrence/application requires exact identity of the engineering/evidence commit, use this order:

```text
engineering/evidence candidate exists immutably
 -> qualification/assessment exists or is durably identifiable
 -> descendant PEM reconciliation binds those pre-existing identities
 -> later closeout/mapping may bind the PEM reconciliation if needed
```

Do not require a PEM-containing commit to know its own SHA. A same-commit PEM edit is allowed only when every material evidence/subject identity it references already exists independently and no self identity is needed to establish the claim. Otherwise use the minimal descendant reconciliation commit; do not invent a new framework.

### 7.3 Failure occurrence evidence

Preserve compactly:

```text
occurrence ID
confirmed date / immutable event identity
lifecycle context
subject/candidate
owner/surface
observed failure
cause claim + cause evidence
repair reference
post-repair qualification
limits/applicability
```

Distinguish incident-level cause from generalized cause and literal patch from generalized repair principle.

### 7.4 Positive-pattern evaluated applications and counterevidence

Once a success pattern is admitted, record materially applicable evaluated applications, not only wins:

```text
application ID
lifecycle context
subject/candidate and comparator when material
owner/surface
intended benefit
outcome: SUPPORTING | NEUTRAL | CONTRADICTING | INCONCLUSIVE
qualification/analysis reference
quantitative effect when available
experimental envelope / uncertainty when material
correctness/constraint evidence
material costs/tradeoffs
applicability/limits
```

A supporting outcome may increment qualified supporting count. Neutral, contradicting, or inconclusive outcomes do not become successes but remain visible in the current assessment when material. If counterevidence narrows the valid regime, narrow/split/reclassify the pattern instead of averaging away the contradiction.

A complexity claim such as `O(N^2) -> O(N log N)` requires adequate algorithmic analysis and evidence that implementation realizes the analyzed algorithm; one timing sample cannot establish asymptotic complexity. Empirical scaling may supplement analysis.

### 7.5 Applicability, stale state, contradiction, and common-mode risk

A valid old pass is not confirmation of a changed candidate; a stale old failure is not refutation.

When protocol obligation, governing claim, candidate, evidence specification/oracle, regime, environment, or execution dependency changes enough to plausibly affect a PEM claim, mark only materially affected family/application `REVIEW_REQUIRED` or stale and preserve unaffected entries with reason.

For important claims account for evidentiary independence/common-mode risk. Multiple checks sharing one defective expected-value generator, fixture, benchmark harness, dataset, or assumption do not automatically provide independent confirmation.

Contradictory admissible observations remain visible.

Evidence maturity:

```text
PROVISIONAL
SUPPORTED
PROVEN
```

Current applicability/lifecycle state:

```text
CURRENT
REVIEW_REQUIRED
STALE_OR_INAPPLICABLE
RETIRED
```

Contradiction is explicit assessment state/flag, not deletion. Temperature/confidence/applicability are orthogonal.

### 7.6 Security and trust boundary

PEM and evidence records are durable repository content and inherit `security-and-trust-boundaries.md`.

- never copy secrets, credentials, private keys, sensitive user data, restricted logs, or unnecessary machine-specific paths into PEM;
- preserve the minimum safe evidence summary/reference necessary for the claim;
- when raw evidence cannot safely be committed, use the project-approved protected evidence location/identifier and record access/retention limitations;
- lack of safe access to required evidence is unavailable/blocking where that evidence is necessary for the claim;
- review staged PEM/evidence/generated outputs for accidental private-data inclusion;
- external links and artifacts remain subject to provenance/trust policy.

Compactness never justifies leaking sensitive evidence.

## 8. Statistics, coverage, and memory temperature

### 8.1 Canonical ledger; derived summaries

Evidence ledger rows are the statistical basis. Displayed counters are derived and never independently hand-maintained.

Failure family tracks at least:

```text
confirmed_occurrence_count
independent_repair_cycle_count
affected_surface_count
recurrence_after_accepted_repair_count
first_confirmed
last_confirmed
coverage_state / coverage_basis
lifecycle-context distribution when material
```

Success pattern tracks at least:

```text
evaluated_application_count
qualified_supporting_application_count
qualified_neutral_count
qualified_contradicting_count
inconclusive_count
independent_surface_count
first_evaluated
last_evaluated
coverage_state / coverage_basis
```

A merge/rebase reconciles evidence rows first and recomputes counts; never sum stored counters blindly.

### 8.2 Counting rules

One causal change producing many failing tests is normally one occurrence. A defect repaired/accepted then independently reintroduced is another occurrence and one recurrence-after-repair. Several commits in one coherent repair episode are one repair cycle when they close one occurrence through accepted qualification.

Repeated executions of one implementation do not create new successful applications. A later materially independent use may count when separately qualified. The same underlying application copied/cherry-picked across branches is not multiplied.

Development/qualification occurrences may count as engineering-history events, but lifecycle context must remain visible; their count cannot be relabeled as production incidence.

### 8.3 Coverage and absence

`confirmed_occurrence_count` is exactly the number of evidence-bound counted occurrences, but may be a lower bound when coverage is partial.

- `>=3` confirmed failure occurrences give a frequency-based `HOT` floor even under partial coverage;
- `2` give at least `WARM`;
- `1` may be `COLD` by frequency only with adequate declared family-relevant coverage; otherwise `UNASSESSED` absent evidence-backed impact promotion;
- `0` or absent family under partial/uninitialized coverage never proves absence.

Apply equivalent coverage discipline to positive-pattern application history.

### 8.4 Reproducible memory temperature

Default frequency classification:

```text
confirmed failure occurrences >= 3            -> HOT
confirmed failure occurrences == 2            -> WARM
confirmed failure occurrences == 1            -> COLD only with adequate declared coverage

qualified supporting applications >= 3        -> HOT
qualified supporting applications == 2        -> WARM
qualified supporting applications == 1        -> COLD/UNASSESSED by frequency subject to coverage
```

A single event/application may be promoted to `WARM`/`HOT` for demonstrated severity, breadth, cost, architectural criticality, or exceptional benefit, but store base class, evidence-bound override, and final temperature.

Counterevidence affects evidence maturity, applicability, regime, and whether a `SUCCESS_PATTERN` remains correctly generalized. A high supporting count does not erase qualified contradictions.

Recency may order attention or trigger applicability review; it does not erase counts or automatically demote an old applicable lesson.

### 8.5 Counts are not rates

Unless an explicit exposure/opportunity denominator and sampling basis exist, do not infer:

```text
FF-A occurred 4 times and FF-B 2 times
therefore FF-A is twice as likely
```

or infer a success probability from supporting/application counts. Counts support recurrence/salience heuristics only within declared coverage.

### 8.6 Memory temperature versus activation/current applicability

Memory temperature records historical/project importance. Activation remains decision-local under Protocol 6.2 progressive disclosure.

- a `HOT` but irrelevant family stays cold for the current task;
- a `COLD` but materially applicable family may become active;
- a historically `HOT` family whose mechanism/regime is retired does not remain active merely because lifetime count is high;
- lifetime statistics remain recoverable while current applicability controls active guidance.

No count or temperature forces a design decision, acceptance, or context load.

## 9. Failure-to-success learning and authority-safe capability transfer

PEM SHALL record what the project learned, not only scars.

```text
FF-### repeated expensive preparation
  -> DS-### preparation ownership is route-local
  -> SP-### lazy route-owned construction repeatedly qualifies
  -> PC-### learned cold-route capability
```

A `PC-###` record MUST say whether it is:

```text
EVIDENCE_ONLY
  useful demonstrated property; design prior only

AUTHORITY_BOUND
  exact current D1/D2/D3/D4/project owner explicitly requires it

PROPOSED_FOR_PROMOTION
  evidence suggests durable authority may need change; route to owner
```

PEM never promotes `EVIDENCE_ONLY` to `AUTHORITY_BOUND` by repetition, temperature, qualification count, or wording. The owning semantic acceptance process does that.

When mechanism is removed/replaced:

```text
old mechanism
 -> learned capability
 -> authority-binding state + governing owner if any
 -> new mechanism / justified omission / deliberate owner-approved retirement
 -> verification
```

Historical wrapper/cache/executor/checkpoint format does not become authority through existence.

## 10. Workflow integration, ownership, and historical applicability

### 10.1 Design/workplan phase

For memory-triggering substantial work:

1. read PEM active summary;
2. determine governed scope from actual parents/side constraints;
3. inspect only relevant family detail/evidence;
4. record HAS;
5. identify learned capabilities and authority-binding state;
6. build capability-transfer map where relevant;
7. identify new claims requiring qualification;
8. preserve lower-salience mandatory constraints regardless of memory ranking.

A `HOT` family intersecting governed scope is dispositioned `applicable`, `not applicable with reason`, or `review required`. Missing/partial memory or missing edges cannot prove non-applicability.

### 10.2 Implementation phase

Implementation MUST preserve authority-bound capabilities because their real owners require them. Evidence-only learned capabilities are considered and dispositioned proportionately but remain replaceable design space. Do not accept a positive pattern merely because code was written or tests happen to be green.

### 10.3 Review phase

Challenge at least:

```text
reintroduced historical failure mechanism
lost mature optimization or valid reuse
accidental serialization / lost parallel capability
new eager preparation
lost sensor/oracle
generated/package drift
shadow authority created by PEM or capability wording
capability loss during mechanism replacement
stale/inapplicable/counterevidenced PEM guidance
scope/materiality laundering through memory selection
security/private-data leakage
branch-candidate memory mistaken for accepted project memory
```

Review proceeds against current owners and assembled candidate. PEM is a high-information hypothesis index, not proof.

### 10.4 Evidence and impact closure

When material authority/concretization change can affect PEM:

```text
identify materially dependent families/applications/capabilities
 -> preserve unaffected entries with reason
 -> mark affected entries REVIEW_REQUIRED/STALE as appropriate
 -> rerun/remap evidence where required
 -> update current PEM only after assessment
```

Changing one family does not invalidate all memory. Old summary text cannot be reused blindly after owner/candidate/regime/evidence changes.

### 10.5 Learning-update responsibility

Responsibility follows the semantic change. The D1/D2/D3/D4 or concern owner responsible for the material change ensures relevant learning assessment and authority binding are correct. `software-documentation` may reconcile wording/source chain but cannot independently promote a substantive finding, declare an authority-bound capability, or adjudicate contradiction.

### 10.6 Closeout learning assessment

Every accepted material repair/rework/optimization asks:

```text
Did a known family recur?
Did an existing positive pattern receive supporting, neutral, contradicting, or inconclusive new evidence?
Did a reusable discovery emerge?
Did a capability lesson emerge, and what is its authority-binding state?
Did evidence contradict/retire/narrow a lesson?
Did coverage materially change?
```

Update PEM only when admission threshold is met or an existing entry materially changes. Ordinary fix chronology remains out of permanent memory.

## 11. Maintenance transaction, update classes, and branch reconciliation

### 11.1 Update transaction

A material PEM update SHALL:

1. identify candidate learning/current notice;
2. bind exact admissible evidence;
3. classify/create family under semantic-family rules;
4. update evidence rows, not counters;
5. recompute statistics;
6. update coverage/applicability/lifecycle context;
7. update evidence maturity/conflict state;
8. compute base temperature and evidence-bound override;
9. update authority-binding state only from actual owner state;
10. update active summary if current importance/applicability changed;
11. preserve split/merge/retirement lineage;
12. verify no still-valid lesson, counterevidence, mandatory condition, or sensitive-data rule was lost;
13. run structural/source-chain/security checks;
14. use self-reference-safe evidence/update staging;
15. commit memory reconciliation as the minimum associated descendant/current-state change.

### 11.2 Update classes

Avoid both unreviewed semantic drift and heavyweight ceremony for every evidence row.

```text
EVIDENCE_APPEND
  family meaning/applicability unchanged; add admissible evidence and derived counts
  -> focused applicability + structural/statistical validation

SEMANTIC_RECONCILIATION
  generalized cause/claim, scope, authority binding, split/merge, applicability,
  contradiction resolution, promotion/retirement, or active lesson materially changes
  -> affected owner review + proportionate independent falsification

PEM_SCHEMA_OR_PROTOCOL_CHANGE
  representation/routing/required field semantics change
  -> protocol/workplan path; do not smuggle through project-memory edit
```

### 11.3 Branch and merge behavior

The accepted/base PEM at branch start remains the project reference. Branch-local memory edits are candidate updates for that branch.

Before merging/rebasing a branch with PEM changes:

- reconcile against target branch accepted PEM;
- resolve provisional family-ID collisions;
- deduplicate shared/cherry-picked event identities;
- re-evaluate evidence applicability if target authority/candidate/regime changed;
- recompute counts/temperature from reconciled ledger;
- rerun affected structural/semantic review;
- do not let later branch text silently overwrite contradictory accepted evidence.

Accepted IDs are stable and never recycled.

### 11.4 Lossless compaction

Active summary stays compact through generalization/progressive disclosure, not deletion by quota. Raw narratives, benchmark tables, patch transcripts, and debate stay at evidence/history owners unless needed for current interpretation.

Compaction may rewrite wording, merge equivalent exposition, or make detail cold only when it preserves identity, statistics, coverage, lifecycle context, supporting/counterevidence, authority binding, cause distinctions, limits, contradiction, capability relationships, and retrieval routes. If apparent duplicates materially differ, stop compaction and preserve/resolve the distinction.

## 12. Performance and activation constraints

Protocol 6.3 MUST NOT recreate the regression class it exists to prevent.

Normal operation primarily consumes the curated PEM summary when its trigger fires. It SHALL NOT:

- rescan Git history on every task;
- recompute all statistics from full corpus on every bootstrap;
- load all family evidence merely to read summary;
- activate backfill machinery during normal use;
- serialize unrelated initialization merely to load PEM.

Deep history is appropriate when creating/backfilling PEM, resolving disputed lineage/evidence, updating a family, dedicated qualification, or independent Review requiring underlying evidence.

Static bytes/tokens/routes/activation traces are sensors only. Claims of actual model latency, attention, cache behavior, context use, or engineering productivity require corresponding live evidence for the claimed harness/model/install regime; otherwise state the empirical claim is unavailable.

## 13. Self-hosted SSDP migration/backfill

SSDP SHALL be the first qualified project-local PEM instance.

Backfill from actual evidence, not this workplan's examples or agent recollection. Inspect where relevant:

- semantic evolution;
- archived Protocol 5.x/6.x workplans only where lineage/family evidence requires them;
- Protocol 6.1/6.2 qualification and independent reviews;
- commit/patch history needed to identify concrete episodes;
- replacement-bootstrap invalidation/repair;
- cold-route repair/requalification;
- static activation-sensor evidence;
- frozen-profile preservation;
- generated/package-integrity repairs;
- documentation background/terminology repairs;
- materially relevant optimization/simplification history.

Candidate investigations, not pre-accepted families:

```text
failure candidates
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

positive candidates
- project-specific qualified examples of route-local lazy activation
- project-specific provenance-valid artifact reuse
- bounded independent parallelism with measured project benefit
- direct owner-layer repair/simplification with qualified outcome
- other concrete project improvements supported by evidence
```

Do not duplicate a generic current SSDP rule merely because SSDP historically discovered it. If the generic doctrine already lives at a current owner, retain only project-specific evidence/recurrence context that materially improves future decisions, otherwise keep the lesson at its canonical owner/history.

For each seeded family declare coverage basis and lifecycle context. A partial search is never exhaustive. Archived workplans remain byte-identical; semantic evolution is appended only through normal closeout.

## 14. Validation architecture

Extend existing qualification/test owners rather than creating competing compliance machinery.

The canonical Markdown PEM is source. Minimum validator SHOULD detect:

- duplicate/current-colliding accepted IDs and invalid provisional-ID merge state;
- invalid kind/maturity/applicability/temperature/authority-binding values;
- malformed/non-resolving required evidence;
- displayed count versus ledger mismatch;
- double-counted event/application identities after split/merge/cherry-pick;
- `COLD` classification unsupported by coverage;
- unexplained temperature override;
- active-summary reference to nonexistent/stale/retired entry;
- `HOT` temperature being used as an unconditional activation command;
- Provisional finding presented as proven fact;
- evidence-only capability presented as mandatory authority;
- contradicted/neutral/inconclusive material evidence hidden from success assessment;
- retired entry presented as active guidance;
- branch-candidate PEM represented as accepted project memory;
- project-local PEM copied into generic protocol package;
- generated index diverging from canonical Markdown;
- self-referential evidence binding requiring current commit SHA;
- forbidden secret/private-data patterns where repository policy can test them;
- loss of T01-T39 or any 6.3 preservation row;
- source/generated/profile/package divergence.

Objective absence/uniqueness/derivation properties may be executable. Do not build a universal database/graph solely for validation.

## 15. Protocol 6.3 version, bootstrap, profile, and package staging

Git commits cannot self-name. Preserve the repaired 6.2 staging discipline.

### 15.1 Public-source bootstrap

1. Complete self-reference-safe 6.3 public-source set: current role/specialist entrypoints, all routed references/templates including PEM doctrine/template, `source/PROTOCOL_VERSION`, navigation/version-resolution source, required package closure.
2. Validate source regression, canonical package build, standalone package/link closure, and routing reachability without unknown self SHA.
3. Create immutable 6.3 public-source bootstrap only after checks pass.
4. In later semantic-candidate/publication commit, publish that exact bootstrap in current 6.3 resolution surfaces. Never use `main`, latest, guessed version, or eventual recovery identity as bootstrap.

### 15.2 Profile and frozen resources

Create distinct `ssdp-protocol-6.3` profile/snapshot using schema v2 unless an actual machine contract requires schema change. Do not mutate packaged/frozen 5.16/6.0/6.1/6.2 resources. Protocol 6.2 becomes historical rollback only after 6.3 cutover; until then it is accepted-current.

Live project PEM is not embedded into generic profile; only doctrine/template/routing needed to use project-local PEM is packaged.

### 15.3 Semantic candidate and generated descendants

Bind qualification to one immutable 6.3 semantic candidate. Later evidence/generated/lifecycle commits contain no hidden canonical semantic mutation; such mutation reopens affected qualification.

Rebuild `dist/` and orchestrator 6.3 descendants from canonical source and validate source parity, package structure/local-resource closure, profile identity/schema/topology, exact immutable fallback, closest supported consumer ingestion, and project-local PEM exclusion.

### 15.4 Recovery and closeout staging

After semantic qualification and independent Review pass:

1. choose immutable 6.3 recovery containing accepted candidate and required decision evidence through ancestry;
2. publish `6.3.0 -> <exact recovery>` only in later mapping commit;
3. regenerate mapping-bearing descendants;
4. rerun targeted recovery/parity/package/Core acceptance;
5. append concise 6.3 semantic evolution;
6. update workplan authority index;
7. reconcile Protocol 7 pre-cutover inheritance/fallback to accepted 6.3 only after 6.3 acceptance, without silently changing Protocol 7 D3 architecture;
8. archive this workplan only when current 6.3 rules reside at owners and impact closure is complete.

No `main` merge/cutover is authorized by this workplan.

## 16. Qualification plan

Run complete affected repository/package/orchestrator regression, all 115 Protocol 6.2 semantic scenarios against 6.3, focused 6.3 cases below, generated/profile/package checks, and independent assembled-candidate Review.

### Q63-01 — Complete 6.2 no-loss preservation
Independently challenge T01-T39 against current owners/assembled 6.3 candidate, including bootstrap, cold-route repair, static sensors, frozen profiles, generated/package integrity, 115-case behavior, affected requalifications, and Stage G lifecycle.

### Q63-02 — Finite census/transformation closure
Every current durable/generative 6.2 artifact receives disposition; each transformed obligation closes `PRESERVED` or `BLOCKING`.

### Q63-03 — Authority/evidence separation
Tests, benchmark, commit, PEM, or history may warrant/challenge but cannot override current D1-D4 owner by existence.

### Q63-04 — Activation/cold-route behavior
A material memory-relevant change activates PEM; first clean unrelated local defect does not; ordinary links/package membership do not; relevant cold detail remains reachable.

### Q63-05 — Missing/partial memory
No PEM/partial coverage cannot prove historical absence/non-applicability; major relevant rework performs bounded intake or carries uncertainty.

### Q63-06 — Evidence-binding durability
Every seeded family resolves to durable evidence; default-branch-only and recursive-PEM-only proof rejected.

### Q63-07 — Stale evidence both polarities
Stale pass cannot confirm and stale fail cannot refute; bounded invalidation preserves unaffected evidence.

### Q63-08 — Independence/common-mode risk
Correlated checks do not masquerade as independent support; contradictory admissible observations remain visible.

### Q63-09 — Semantic family membership
Textually similar but semantically different failures do not merge; equivalent manifestations with shared cause may group.

### Q63-10 — One cause/many symptoms
One causal defect producing many failures/sites counts once absent independent introduction.

### Q63-11 — Recurrence after repair
Independent later reintroduction increments occurrence/recurrence exactly once and binds both repair cycles.

### Q63-12 — Split/merge lineage
Split/merge preserves lineage, deduplicates evidence, recomputes totals.

### Q63-13 — Coverage-sensitive temperature
Three confirmed occurrences Hot; two Warm; one under incomplete coverage not confidently Cold; overrides reproducible.

### Q63-14 — Importance is not authority
Hot family cannot force architecture/pass threshold; Cold but materially mandatory constraint survives closure.

### Q63-15 — Positive-evidence promotion
Unmeasured optimization remains Provisional; qualified benefit is bounded to demonstrated regime and governing constraints.

### Q63-16 — Quantitative effect preservation
Effect sizes retain comparator/candidate/envelope/evidence through compaction.

### Q63-17 — Complexity claim discipline
One timing result cannot establish asymptotic change; adequate analysis + implementation correspondence required.

### Q63-18 — Capability transfer without ossification
Replace historical mechanism with simpler qualified design while preserving actual authority-bound capability; evidence-only capability may be justified away.

### Q63-19 — First-local-defect economy
One clean local bug does not force permanent family/backfill; repeated/high-impact/generalizable case triggers proportionate assessment.

### Q63-20 — Invalidation/contradiction/retirement
Material owner/candidate change updates affected memory while retaining old evidence/history.

### Q63-21 — Active-summary lossless compaction
Compaction preserves identity, statistics, coverage, lifecycle context, applicability, limits, counterevidence, authority binding, capability links, cold routes, and governed scope.

### Q63-22 — No repeated-history regression
Normal triggering operation consumes curated summary without full-history scan/stat recomputation; non-triggering work adds no memory preparation.

### Q63-23 — Static-versus-live claims
Static sensors establish structural claims only; live model/performance claims require live evidence or remain unavailable.

### Q63-24 — Project-local/package separation
Self-hosted PEM is project content absent from generic package/profile; template/doctrine present where routing requires.

### Q63-25 — Exact 6.3 fallback
No-local-compatible and incompatible-default cases resolve only exact validated bootstrap; default/latest/guessed refs rejected.

### Q63-26 — Frozen resource integrity
5.16/6.0/6.1/6.2 resource trees remain byte/behavior identical; 6.3 distinct/version-bound.

### Q63-27 — Full generated/package/Core acceptance
After candidate and recovery mapping validate package build, standalone closure, `dist` parity, snapshot parity, profile identity, consumer ingestion.

### Q63-28 — Self-hosted backfill statistics
Independently reconstruct every Hot family and risk-based Warm/Cold sample; counts and coverage no broader than evidence.

### Q63-29 — Closeout learning transaction
Qualified material recurrence/success/counterevidence updates PEM; non-material local repair creates no noise.

### Q63-30 — Version/recovery/Protocol 7 lifecycle
Verify distinct bootstrap/recovery, late mapping, regeneration, authority-index/semantic-evolution, bounded Protocol 7 inheritance.

### Q63-31 — Capability authority binding
An `EVIDENCE_ONLY` capability cannot become mandatory through PEM, frequency, or qualification count. `AUTHORITY_BOUND` requires exact accepted owner and is enforced because that owner governs.

### Q63-32 — Self-reference-safe PEM update
An occurrence whose repair commit identity is material cannot be bound by a PEM-containing commit to its unknown own SHA. Validate candidate/evidence -> descendant PEM reconciliation staging and allow same-commit update only when all material identities preexist.

### Q63-33 — Balanced positive evidence
Create a success pattern with supporting plus neutral/contradicting/inconclusive evaluated applications. Current assessment preserves all material outcomes; supporting count alone cannot hide counterevidence.

### Q63-34 — Count versus rate
Four occurrences versus two cannot be represented as twice the failure probability without denominator/sampling basis. With a valid denominator, a bounded rate claim may be assessed separately.

### Q63-35 — Temperature versus activation
A Hot irrelevant family remains cold for unrelated work; a Cold materially applicable family activates when required; retired historical Hot family does not activate solely from lifetime count.

### Q63-36 — Concurrent branch/ID/merge reconciliation
Two branches create colliding provisional IDs and shared/cherry-picked event evidence. Merge resolves provisional collision, keeps accepted IDs stable, deduplicates underlying event, recomputes counts, and rechecks applicability.

### Q63-37 — Security/private-data preservation
Attempt to place secret/private material in PEM/evidence. Expected: use safe minimal summary/protected reference; required inaccessible evidence remains unavailable/blocking rather than leaked.

### Q63-38 — Update-class and responsibility discipline
Evidence-only append under unchanged family uses focused checks; semantic split/promotion/authority-binding change triggers affected owner review; schema change cannot be smuggled through project PEM. Documentation support cannot self-promote finding.

### Q63-39 — Cross-domain applicability
A material D2/D1 or specialist project lesson can activate PEM when decision-relevant without making PEM universally hot or allowing it to override domain authority.

### Q63-40 — Promotion-to-current-owner deduplication
Promote a lesson into current accepted doctrine. Current owner becomes governing source; PEM retains only useful project evidence/lineage or retires duplicate active prose.

### Q63-41 — Lifecycle-context integrity
Development/qualification/production occurrences remain distinguishable. Historical counts may aggregate explicitly, but a development count cannot be presented as production incidence.

## 17. Falsification

Retain the four Protocol 6.2 Challenge falsifications unchanged in semantic purpose:

1. **Loss test** — find compaction/generalization that loses edge case, authority/evidence boundary, compatibility rule, trigger, salience, counterevidence, or authority binding.
2. **Scope/materiality laundering test** — reject passing by shrinking scope or calling globally preserved doctrine non-material because cold locally.
3. **Priority-inversion test** — prominent high-importance memory must not erase lower-salience mandatory active constraints.
4. **False-compaction test** — reject link-moving, flattened routing, stale summaries, parallel registry, recursive summaries, or unnecessarily dense active context.

Additional 6.3 falsification:

### F63-A — Speculation laundering
Promote `this seems faster` without suitable evidence. Reject.

### F63-B — Statistical inflation
Turn one causal defect into many occurrences via tests/files. Reject absent independent introduction.

### F63-C — Family overgeneralization
Group superficially similar but semantically different failures. Split/review-required.

### F63-D — Incomplete-history false Cold
One found occurrence under partial coverage cannot prove Cold.

### F63-E — Cargo-cult positive pattern
Apply historical technique outside assumptions or while violating correctness. Historical success does not qualify new use.

### F63-F — Summary/evidence recursion
Use PEM/derived summary as sole warrant. Follow to admissible evidence or remain unsupported.

### F63-G — Stale-green/stale-red laundering
Use old pass/fail after material subject/oracle/regime change. Reject until applicability restored.

### F63-H — Common-mode fake independence
Count correlated checks as independent. Reject.

### F63-I — Architectural ossification
Remove old mechanism while preserving actual owner-bound capabilities with simpler qualified design. Allow.

### F63-J — History-compaction loss
Split/merge/compact while losing event, counterevidence, limit, lifecycle context, or lineage. Block.

### F63-K — False quantitative generalization
Use microbenchmark to claim global scaling/performance superiority. Narrow/reject.

### F63-L — Eager memory regression
Make every task load PEM/history because it might help. Reject.

### F63-M — Project-memory package contamination
Package live SSDP PEM as generic protocol content. Reject.

### F63-N — Shadow capability authority
Mark evidence-only optimization as `must preserve` with no governing owner. Reject; either bind exact authority or keep as design prior.

### F63-O — Routine self-SHA recursion
Require PEM reconciliation commit to cite its own unknown SHA as evidence. Reject and stage against pre-existing evidence identity.

### F63-P — Positive survivor bias
Record three successful applications while omitting a materially applicable qualified failure/neutral result. Reject current assessment.

### F63-Q — Pseudo-statistical risk
Claim `4 occurrences = 2x risk of a 2-occurrence family` without denominator. Reject.

### F63-R — Temperature/activation conflation
Unconditionally load all Hot families or ignore a Cold-but-material family. Reject.

### F63-S — Branch memory overwrite
Merge branch-local PEM over newer accepted memory without reconciliation. Reject.

### F63-T — Accepted-ID reuse
Recycle retired accepted `FF-###` or renumber accepted IDs for compactness. Reject.

### F63-U — Sensitive-evidence laundering
Copy secret/private raw evidence into PEM because exact evidence is required. Reject; use safe approved binding.

### F63-V — Documentation self-promotion
Documentation-only reconciliation upgrades an evidence-only lesson into owner-bound invariant. Reject.

### F63-W — Generic-doctrine duplication
Self-hosted SSDP PEM repeats current generic protocol doctrine as a second active rule without project-specific added evidence value. Reject/deduplicate.

### F63-X — Lifecycle-incidence laundering
Use development-branch occurrence count as production incident rate. Reject.

## 18. Implementation stages

### Stage A — Baseline capture, owner census, preservation map

1. Reconfirm exact accepted 6.2 identities.
2. Build finite artifact census and independently reproduce T01-T39.
3. Identify exact current owners/source/generated/profile/package/security consumers.
4. Append T40+ hypotheses and oracles.
5. Record which 6.2 evidence remains applicable and which requires rerun after planned changes.

**Gate:** no protocol-source mutation before finite no-loss map sufficiently bounds change.

### Stage B — Canonical doctrine and PEM representation

1. Add smallest justified `source/shared/references/project-engineering-memory.md` concern owner, or prove an existing owner sufficient.
2. Implement canonical PEM/template schema, coverage, admission, family/evaluated-application/statistics/temperature, authority binding, evidence binding, counterevidence, branch lifecycle, security, contradiction/retirement.
3. Update evidence, convergence, architecture, workflow, documentation, repository, testing, security, version owners only with local consequences/routes.
4. Keep universal kernel additions minimal.

**Gate:** one semantic owner per rule; no shadow authority, duplicated generic doctrine, or hidden prerequisite.

### Stage C — Routing/workflow/project-local integration

1. Add visible conditional routes from materially relevant D1-D4/specialist/workflow entrypoints without making PEM universal hot context.
2. Implement HAS and authority-safe capability-transfer handoff.
3. Implement project-local discovery, missing/partial-memory, accepted/base versus branch-candidate behavior.
4. Extend closeout so only admitted material learning changes PEM and responsibility follows owner.

**Gate:** first-local-defect, Hot-irrelevant, Cold-material, and ordinary-route cases prove correct activation.

### Stage D — Structural validation and self-hosted backfill

1. Extend validation for canonical Markdown, evidence resolution, derived counts, counterevidence, lineage, coverage, temperature/activation separation, authority binding, branch IDs, security, and active-summary integrity.
2. Create SSDP project-local PEM from actual historical evidence.
3. Qualify seeded families; no recollection-derived counts.
4. Ensure no live project memory enters generic packages.
5. Use self-reference-safe PEM reconciliation commits where current evidence identity must be bound.

**Gate:** independent reconstruction reproduces all Hot statistics and risk-based remainder; no known material counterevidence omitted.

### Stage E — 6.3 bootstrap/profile/semantic candidate/generated descendants

1. Complete/validate self-reference-safe public-source set.
2. Create immutable public bootstrap.
3. Publish exact bootstrap only in later semantic-candidate/publication commit.
4. Add distinct 6.3 profile/snapshot; leave 5.16/6.0/6.1/6.2 frozen.
5. Regenerate/package and validate local routes/links/parity/Core ingestion.

**Gate:** bootstrap and semantic candidate distinct, exact, self-reference-safe.

### Stage F — Qualification and independent Review

1. Run complete affected regression.
2. Re-run all 115 Protocol 6.2 scenarios against 6.3.
3. Run Q63-01 through Q63-41 and F63-A through F63-X.
4. Compare representative 6.2/6.3 static activation traces as sensors.
5. Obtain live evidence only for live empirical claims actually made; otherwise mark unavailable.
6. Prepare snapshot-complete independent-review handoff.
7. Perform independent D3/protocol Review over assembled semantic candidate, not diff/summary/preservation labels.

**Gate:** no PASS with missing required check, stale/counterevidence hidden, sensitive-data defect, shadow authority, or unresolved preservation row.

### Stage G — Recovery/current-state reconciliation/closeout

1. Choose immutable 6.3 recovery only after Stage F PASS.
2. Publish recovery mapping only in later descendant.
3. Regenerate mapping-bearing descendants and rerun targeted recovery/parity/package/Core acceptance.
4. Reconcile semantic evolution, authority index, version/portability/navigation, and project-local PEM.
5. Reconcile Protocol 7 representation/version inheritance only after 6.3 acceptance; preserve existing D3 reopen prerequisite/architecture unless separately reopened.
6. Archive workplan only when current 6.3 semantics reside at canonical owners and impact closure complete.
7. Do not merge/cut over `main` without separate authorization.

## 19. Independent Review handoff

Create `qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md` (or established equivalent) only after implementation/qualification evidence is ready.

Bind at least:

```text
accepted 6.2 recovery/current branch ancestry
6.3 public-source bootstrap
6.3 semantic candidate
preservation census/map T01-T39 + T40+
self-hosted PEM + declared coverage/lifecycle state
qualification/requalification evidence
supporting and material counterevidence
static activation evidence
available live evidence with exact claim scope
generated/package/profile evidence
frozen-profile tree identities
candidate-to-evidence descendant range
known red/unavailable observations
security-sensitive evidence handling where material
```

Reviewer independently reconstructs governing semantics; treats census/PEM/qualification as falsifiable evidence; inspects high-risk current owners; verifies assembled source/generated/package/profile state; checks candidate descendants for semantic mutation; and samples positive claims for omitted counterevidence as well as negative family counts.

## 20. Acceptance and No-Pass criteria

### 20.1 PASS

Protocol 6.3 passes only when:

- every accepted 6.2 doctrine/still-valid historical capability is preserved;
- T01-T39 independently remain preserved and all new rows close;
- D1-D4/current project authority remains distinct from evidence/PEM;
- PEM is compact, project-local, current, evidence-backed, coverage-aware, security-safe, and non-authoritative;
- positive and negative learning are both represented without selective success recording or permanent ordinary-bug chronology;
- family membership, lineage, counts, coverage, lifecycle context, temperature, authority binding, branch state, and active summary are independently reproducible;
- stale/correlated/contradictory/neutral/inconclusive material evidence is handled correctly;
- statistical claims are no broader than their denominator/sampling evidence;
- quantitative/complexity claims no broader than evidence;
- historical mechanism replacement remains possible while actual authority-bound capabilities remain preserved;
- bounded activation prevents ordinary/history-unrelated routes from unnecessary work;
- all 115 inherited scenarios and all 6.3 qualification/falsification pass;
- exact 6.3 bootstrap/recovery/profile/fallback lifecycle passes;
- frozen 5.16/6.0/6.1/6.2 bytes/behavior intact;
- source/generated/package/profile/Core acceptance passes;
- Protocol 7/current lifecycle reconciliation bounded/correct;
- independent Review finds no genuine blocker or Serious Challenge.

### 20.2 NO-PASS

Blocking includes:

- PEM/tests/commits/history/statistics treated as semantic authority;
- evidence-only capability treated as mandatory without accepted owner;
- loss/weakening/orphaning of accepted 6.2 semantics;
- scope shrunk to avoid historical/preservation obligation;
- partial memory used to prove absence/Cold status;
- recurrence manufactured from symptoms/text similarity;
- counters not reproducible from ledger;
- positive record omits material neutral/contradicting/inconclusive evidence;
- unsupported success guidance presented as established knowledge;
- performance gain accepted despite violated constraints;
- stale pass/fail used as current confirmation/refutation;
- correlated evidence represented as independent;
- occurrence counts represented as probability/rate without denominator;
- historical mechanism preserved merely because memory mentions it;
- authority-bound capability silently lost;
- temperature used as activation command or verdict;
- lower-salience mandatory active constraint hidden;
- first local defect forced into permanent memory without rationale;
- branch-candidate memory mistaken for accepted project memory;
- accepted IDs recycled/renumbered or concurrent events double-counted;
- routine PEM update requires self-SHA;
- sensitive evidence leaked into repository memory;
- generic current doctrine duplicated into PEM as competing rule;
- development occurrence count presented as production incidence;
- eager history/PEM activation on ordinary routes;
- live claims inferred only from static sensors;
- live project PEM packaged as generic protocol content;
- frozen profile/resource drift;
- default/latest/guessed-ref 6.3 fallback;
- package/generated/profile divergence;
- semantic mutation after candidate without affected requalification;
- diff-only/summary-only independent Review;
- recovery mapping published before immutable recovery exists;
- Protocol 7 architecture silently changed by 6.3 reconciliation.

## 21. Reopen and repair rule

If implementation/independent Review finds a genuine blocker:

- route to earliest owning D1/D2/D3/D4 or concern layer;
- reopen this workplan only when its accepted D3/cycle contract must change;
- give precise owner-layer repair instructions;
- prefer removal/narrowing/rewiring/consolidation/re-derivation over compensating wrappers;
- rerun only affected evidence while preserving demonstrably unaffected evidence;
- update PEM when repaired episode itself meets admission threshold.

Raise Serious Challenge only when accepted governing authority may be defective; ordinary implementation misses remain ordinary blockers.

## 22. Workplan closure review

**WORKPLAN CLOSURE REVIEW: PASS AFTER SECOND-REVIEW REPAIR.**

The current workplan incorporates the first review repairs and this second independent 6.2-style review without requiring an amendment chain for current meaning.

Second-pass repairs close remaining material gaps:

- capability lessons no longer become shadow architecture authority; each carries explicit authority binding;
- routine PEM updates inherit the Protocol 6.2 self-reference-safe staging lesson;
- positive patterns preserve materially applicable neutral/contradicting/inconclusive evidence rather than success-only survivor bias;
- occurrence/application counts are explicitly descriptive and cannot masquerade as probability/rate without denominator;
- memory temperature is distinct from Protocol 6.2 hot/cold activation and from current applicability;
- branch-candidate memory, accepted ID stability, merge collision/deduplication, and cherry-pick identity are defined;
- durable PEM/evidence obey security/trust/private-data constraints;
- learning-update responsibility follows the real semantic owner and update classes keep review proportional;
- D1/D2/D3/D4/specialist project lessons can activate conditionally without universal loading;
- self-hosted PEM cannot duplicate generic current protocol doctrine as a second authority;
- occurrence/application lifecycle context prevents development evidence from being mislabeled as production incidence.

No Serious Challenge to accepted Protocol 6.2 authority is identified. Implementation remains authorized on the dedicated 6.3 branch subject to Stages A-G. Protocol 6.3 itself remains proposed until qualification, independent Review, immutable bootstrap/recovery, generated/profile/package reconciliation, lifecycle closeout, and separately authorized cutover pass.

## 23. Intended end state

```text
lossless accepted Protocol 6.2 semantics
+ exact historical evidence cold and recoverable
+ one compact current project-engineering memory
+ evidence-backed negative and positive learning
+ material counterevidence visible
+ statistics with declared coverage and honest denominators
+ project-aware engineering instincts without shadow authority
+ learned capabilities distinguished from accepted invariants
+ simpler/new mechanisms remain admissible
+ branch-safe, self-reference-safe memory updates
+ bounded decision-driven activation independent of temperature
+ no routine history replay
+ security-safe evidence persistence
+ qualification proportional to the claim
+ fresh-context agents inherit project experience instead of rediscovering it
```

Central invariant:

> The project must be able to learn even when the individual agent does not persist, and every claimed lesson must remain traceable to admissible evidence and current authority boundaries rather than memory, repetition, selective success reporting, or historical mechanism worship.
