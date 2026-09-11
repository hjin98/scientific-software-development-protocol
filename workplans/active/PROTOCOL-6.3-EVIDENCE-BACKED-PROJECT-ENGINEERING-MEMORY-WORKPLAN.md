---
kind: protocol-revision-workplan
workplan_id: PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY
protocol_version: 6.3.0-proposed
parent_protocol: 6.2.0
status: active
change_class: additive-protocol-revision-with-self-hosted-migration
baseline_branch_point: bf856f742d1744a8ff50f300ee6493fb93e5c9d0
---

# SSDP Protocol 6.3 — Evidence-Backed Project Engineering Memory

**Revision:** Scientific Software Development Protocol (SSDP) 6.3  
**Parent:** accepted SSDP Protocol 6.2  
**Status:** design-ready workplan  
**Change class:** additive protocol revision with self-hosted migration  
**Primary concern:** durable transfer of evidence-backed project engineering experience across fresh agent contexts without weakening Protocol 6.2 lossless-representation guarantees

---

# 0. Authority and baseline

Protocol 6.3 SHALL be implemented as an additive extension of the accepted Protocol 6.2 baseline.

The branch containing this workplan was created from accepted `main` at:

```text
bf856f742d1744a8ff50f300ee6493fb93e5c9d0
```

Before implementation begins, confirm and record:

```text
accepted_protocol_6_2_sha:
implementation_branch:
workplan_sha:
qualification_baseline:
```

If repository truth has advanced after creation of this workplan, the implementation SHALL explicitly reconcile the accepted Protocol 6.2 baseline rather than silently assuming the branch-point SHA remains authoritative.

Previously reviewed semantic candidates or implementation commits MUST NOT be silently promoted to baseline authority merely because they appear in historical discussion.

Protocol 6.3 MUST preserve without semantic regression:

- the complete accepted Protocol 6.2 doctrine;
- the existing Protocol 6.2 preservation map T01–T39;
- replacement-bootstrap semantics;
- cold-route repair and activation boundaries;
- original Protocol 6.2 qualification;
- every requalification affected by Protocol 6.2;
- static activation sensors;
- frozen profile behavior and identity;
- generated/package integrity guarantees;
- all four existing Protocol 6.2 falsification passes;
- independent-review requirements;
- assembled-candidate review rather than PR-diff-only review;
- fail-closed handling of unresolved semantic contradictions;
- historical provenance and archived workplans;
- existing human-facing documentation requirements;
- definitions of newly introduced non-common domain terminology in Background;
- expansion of abbreviations on first use;
- owner-layer repair rather than compensating wrapper proliferation;
- preference for reduction, rewiring, or correction of existing ownership over unnecessary parallel machinery.

T01–T39 SHALL retain their existing identifiers and meaning. They MUST NOT be renumbered, rewritten into weaker abstractions, or replaced by a new 6.3 map.

Protocol 6.3 requirements SHALL be appended beginning with the next unoccupied preservation identifier.

---

# 1. Background

## 1.1 Problem

Agent contexts are transient.

A project may spend substantial engineering effort discovering that:

- an expensive computation can be eliminated;
- an intermediate artifact can safely be reused;
- independent work can be parallelized;
- a route should remain lazy;
- a lifecycle boundary should own particular initialization;
- a wrapper is inferior to repairing ownership directly;
- a specific architecture causes repeated regressions;
- a previously intuitive algorithm scales badly;
- a new algorithm materially improves scaling;
- a specific safeguard prevents a recurring failure class.

The repository may preserve all individual incidents in commits, patches, reviews, qualifications, and archived workplans while still failing to transfer the resulting engineering judgment efficiently to a fresh agent.

The result is repeated rediscovery:

```text
failure
  -> diagnosis
  -> repair
  -> optimization
  -> later architectural rewrite
  -> knowledge disappears from active context
  -> same failure or lost optimization
  -> rediscovery
```

Protocol 6.3 SHALL close this gap.

## 1.2 Project Engineering Memory

**Project Engineering Memory (PEM)** is a compact, evidence-backed, importance-weighted representation of engineering knowledge learned from the project's historical record.

PEM is not a replacement for history.

It is a derived active-memory layer over authoritative evidence.

Conceptually:

```text
LOSSLESS HISTORICAL CORPUS
    commits
    patches
    workplans
    reviews
    qualifications
    tests
    benchmarks
    analyses
    archived decisions
          |
          | evidence binding
          v
PROJECT ENGINEERING MEMORY
    compact lessons
    failure statistics
    successful patterns
    discoveries
    preservation capabilities
          |
          | applicability
          v
CURRENT ENGINEERING WORK
```

## 1.3 Historical corpus

The **historical corpus** is the authoritative collection of repository-tracked evidence from which PEM conclusions are derived.

It includes, where applicable:

- Git commits and ancestry;
- patch history;
- active and archived workplans;
- design reviews;
- implementation reviews;
- qualification artifacts;
- test results;
- benchmark outputs;
- profiling results;
- algorithmic analyses;
- static-analysis evidence;
- generated artifacts;
- package-integrity evidence;
- accepted architectural decisions.

PEM SHALL never become an independent historical authority capable of contradicting this corpus.

## 1.4 Evidence binding

An **evidence binding** is a compact, resolvable reference connecting a PEM claim to the artifact that demonstrates it.

A binding should identify enough information to recover the evidence without reconstructing an old agent conversation.

Examples include:

```text
qualification artifact + section/test ID + candidate SHA
workplan + finding ID + repair commit
benchmark record + baseline/candidate SHAs
static sensor + test name + candidate SHA
algorithm analysis + implementation commit
```

## 1.5 Learning family

A **learning family** is a stable generalized engineering lesson supported by one or more concrete historical observations.

Protocol 6.3 SHALL support at least:

```text
FAILURE_FAMILY
SUCCESS_PATTERN
DISCOVERY
PRESERVATION_CAPABILITY
```

A family identifier survives wording refinement and additional evidence.

## 1.6 Occurrence

An **occurrence** is one independently introduced or independently existing manifestation of a failure family.

Multiple symptoms caused by one causal engineering change normally count as one occurrence.

Example:

```text
one bad refactor
  -> 14 failing tests
  -> 3 commands affected
```

is normally:

```text
occurrence_count += 1
affected_surfaces += 3
```

A later reintroduction after an accepted repair is a new occurrence.

## 1.7 Successful application

A **successful application** is one accepted use of a positive engineering pattern for which qualification or analysis supports the claimed benefit.

Writing an optimization is not a successful application.

An agent saying that a design "looks cleaner" is not a successful application.

The claimed property must have evidence.

## 1.8 Temperature

**Temperature** is an importance/attention classification derived from accumulated evidence.

Temperature is not confidence.

A lesson may be:

```text
high confidence + cold importance
```

or:

```text
high confidence + hot importance
```

Temperature primarily controls how aggressively the lesson must enter future engineering context.

## 1.9 Evidence maturity

**Evidence maturity** describes how strongly a conclusion is supported.

At minimum:

```text
PROVISIONAL
SUPPORTED
PROVEN
CONTRADICTED
RETIRED
```

Only evidence-backed states may influence active project doctrine.

---

# 2. Core Protocol 6.3 principle

Protocol 6.3 SHALL establish the following governing rule:

> Project memory stores engineering conclusions together with their warrant.

The system SHALL distinguish:

```text
idea
hypothesis
attempt
observation
qualified finding
generalized lesson
project engineering knowledge
```

These states MUST NOT be silently collapsed.

In particular:

> Improvement is evidence-based, not aspiration-based.

Statements such as:

```text
"this should be faster"
"this seems cleaner"
"this might scale better"
"I am trying a new optimization"
```

MUST NOT become positive project lessons without supporting evidence.

---

# 3. Design goals

Protocol 6.3 SHALL provide a fresh-context engineer or agent with rapid access to:

1. recurring failure classes;
2. known regression hazards;
3. successful repair strategies;
4. pervasive high-value optimization patterns;
5. architectural approaches demonstrated to work;
6. important engineering discoveries;
7. capabilities that must survive architectural replacement;
8. evidence establishing each important conclusion;
9. statistics describing recurrence or repeated success;
10. limits and applicability conditions of learned patterns.

The intended effect is:

> A fresh agent should begin work with the crystallized engineering experience of the project rather than behaving as though every historical lesson must be rediscovered.

This memory SHALL encourage effective change rather than defensive immobility.

---

# 4. Explicit non-goals

Protocol 6.3 MUST NOT:

- replace full historical records with summaries;
- delete archived workplans after extracting lessons;
- treat agent opinion as qualification evidence;
- create architectural vetoes merely because a historical approach once worked;
- turn previous implementations into mandatory mechanisms when only their capability matters;
- encourage agents to preserve obsolete machinery;
- count every failing test as a separate historical occurrence;
- fabricate missing statistics as zero;
- infer quantitative improvements without measurements or valid analysis;
- claim asymptotic improvement from one runtime measurement;
- promote provisional experiments into active engineering doctrine;
- create a second competing source of truth;
- introduce a parallel bootstrap, packaging, or qualification framework when the existing Protocol 6.2 owner can be extended;
- add wrapper machinery around existing control flow when ownership can be corrected directly.

---

# 5. Architecture

## 5.1 Canonical project artifact

Protocol 6.3 SHALL define one canonical logical artifact:

```text
PROJECT-ENGINEERING-MEMORY.md
```

Its physical location SHALL follow the existing SSDP project-control/document placement convention.

Do not create a new root-layout convention solely for Protocol 6.3 if Protocol 6.2 already has an appropriate canonical location.

## 5.2 Authority hierarchy

The authority hierarchy SHALL be:

```text
Level 1 — authoritative historical evidence
          commits / workplans / qualification / tests / analyses

Level 2 — accepted generalized engineering findings
          PROJECT-ENGINEERING-MEMORY.md

Level 3 — current-work applicability interpretation
          active workplan / implementation plan / review

Level 4 — transient agent reasoning
```

A lower level cannot silently override a higher one.

PEM may summarize evidence but cannot modify what the evidence says.

## 5.3 Internal document topology

The document SHALL be optimized for low-context retrieval.

Recommended topology:

```text
1. Engineering instincts / active memory
2. Hot positive patterns
3. Hot failure families
4. Statistical pattern index
5. Detailed hot/warm family records
6. Preservation capabilities
7. Contradicted / retired lessons
8. Maintenance metadata
```

Cold history SHOULD remain compact.

Hot and relevant warm entries receive greater representation budget.

---

# 6. Active engineering memory

The beginning of the document SHALL contain a tightly bounded active-memory summary.

It should answer, rapidly:

```text
What repeatedly hurts this project?
What repeatedly works well?
What should I preserve?
What should I actively look for?
What engineering approaches have unusually strong evidence here?
```

Each active entry should contain approximately:

```text
ID
one-line lesson
temperature
evidence maturity
occurrence/application count
primary applicability signal
short evidence reference
```

Example form:

```text
SP-004 — Reuse provenance-valid intermediate work
HOT / PROVEN
6 qualified applications across 4 surfaces.
Before introducing expensive preparation, test whether an equivalent
validated product already exists.
Evidence: Q-..., Q-..., WP-...
```

The active-memory section SHALL be aggressively compacted.

Detailed historical prose belongs in the referenced historical corpus, not here.

---

# 7. Learning-family model

## 7.1 Failure family

A failure-family record SHALL answer:

```text
What fails?
Under what conditions?
Why?
How often?
Where?
How was it repaired?
What evidence demonstrates the diagnosis and repair?
What future changes are likely to reintroduce it?
```

Required statistical fields:

```yaml
family_id:
kind: FAILURE_FAMILY

statistics:
  occurrence_count:
  independent_repair_cycle_count:
  affected_surface_count:
  recurrence_after_accepted_repair_count:
  first_confirmed:
  last_confirmed:

importance:
  maximum_observed_severity:
  temperature:

evidence_maturity:
```

Unknown values remain explicitly unknown.

## 7.2 Success pattern

A success-pattern record SHALL answer:

```text
What approach works?
What measurable or analytically demonstrated property improves?
How many qualified applications exist?
Across how many independent surfaces?
Under what assumptions does it work?
Where should an agent consider using it?
Where should it not be generalized?
```

Required fields:

```yaml
family_id:
kind: SUCCESS_PATTERN

statistics:
  qualified_application_count:
  independent_surface_count:
  first_qualified:
  last_qualified:

importance:
  maximum_demonstrated_impact:
  temperature:

evidence_maturity:
```

## 7.3 Discovery

A discovery captures a demonstrated conceptual improvement that changes how the project should reason about a problem.

Examples:

```text
an expensive stage is mathematically unnecessary;
a previously shared lifecycle actually has route-local ownership;
an apparent precision defect is instead an objective-function problem;
a particular representation allows work to be reused safely.
```

A discovery SHALL require evidence just as a performance optimization does.

## 7.4 Preservation capability

A preservation capability records a property future architecture must retain independently of the machinery currently providing it.

Examples:

```text
bounded independent parallelism
checkpoint continuation
lazy route activation
semantic equivalence
artifact reuse
deterministic ordering
generated/package identity
```

This supports the rule:

> Replace mechanisms freely when justified; preserve demonstrated capabilities unless intentionally and explicitly superseded.

---

# 8. Evidence model

## 8.1 Claim-matched evidence

Evidence type SHALL match claim type.

| Claim | Suitable evidence |
|---|---|
| Crash repaired | reproducer + regression test |
| Semantic preservation | differential/oracle/qualification evidence |
| Route no longer activates machinery | static or runtime activation sensor |
| Runtime improvement | controlled benchmark |
| Memory improvement | peak-memory measurement/profile |
| Throughput improvement | representative throughput benchmark |
| O(N²) → O(N log N) | algorithmic analysis, preferably plus scaling study |
| Improved robustness | property/stress/fuzz qualification |
| Package equality | generated/package integrity qualification |
| Repeated project-wide utility | multiple independent accepted applications |

Evidence MUST NOT be generalized beyond what it establishes.

## 8.2 Quantitative findings

Where quantitative evidence exists, preserve the effect size.

Prefer:

```text
4.0x faster
8.1x lower peak memory
91% fewer recomputations
42.1 s -> 10.3 s
15.8 GiB -> 1.96 GiB
O(N^2) -> O(N log N)
```

over:

```text
much faster
lower memory
more efficient
better scaling
```

Include experimental envelope when material:

```text
input size
hardware
worker count
candidate SHA
baseline SHA
configuration/profile
measurement method
```

## 8.3 Qualitative evidence

Quantitative evidence is not mandatory when the claim itself is qualitative.

A valid minimal repair finding may be:

```text
baseline reproducer crashes deterministically
candidate no longer crashes
targeted regression passes
affected qualification passes
```

This is adequate evidence for the bounded claim:

```text
the demonstrated crash is repaired
```

It is not adequate evidence for:

```text
the architecture is faster
```

---

# 9. Evidence-binding schema

Each concrete historical occurrence/application SHALL have a compact evidence record.

Recommended failure form:

```text
O3
date:
affected_surface:
introducing_change:      # when known
detection_evidence:
observed_failure:
generalized_cause:
repair_reference:
repair_qualification:
```

Recommended successful-application form:

```text
A5
date:
affected_surface:
implementation_reference:
qualification_reference:
demonstrated_property:
effect_size:
limits:
```

Every reference SHALL resolve to repository evidence.

No orphan statistic is allowed.

Therefore:

```text
occurrence_count
```

MUST equal the number of valid counted occurrence records.

Likewise:

```text
qualified_application_count
```

MUST equal valid accepted successful-application records.

---

# 10. Statistical counting rules

## 10.1 Failure occurrence counting

Count one occurrence for one independent causal manifestation.

Do not count:

```text
one defect -> 20 test failures
```

as 20 occurrences.

Do count:

```text
initial defect
 -> accepted repair
 -> later rewrite independently reintroduces same family
```

as two occurrences.

A single change manifesting in several surfaces is normally:

```text
occurrence_count += 1
affected_surface_count += number of distinct surfaces
```

If evidence demonstrates independently introduced defects in separate surfaces, they may count separately.

Ambiguous cases MUST remain explicitly unresolved rather than being used to inflate frequency.

## 10.2 Positive application counting

One qualified use of a success pattern counts once.

Repeated test executions of the same implementation do not increase the application count.

A later independent implementation of the same generalized pattern may count as another application when independently qualified.

## 10.3 Repair cycles

A repair cycle is:

```text
confirmed occurrence
 -> engineering repair
 -> accepted qualification
```

Several commits in one repair attempt remain one repair cycle.

## 10.4 Recurrence

A recurrence-after-repair count increases only where:

1. the failure family had previously been accepted as repaired;
2. a later change or latent independent manifestation causes the same generalized family;
3. evidence supports the family classification.

This statistic is especially important because it demonstrates failed project-level retention of an earlier lesson.

---

# 11. Temperature policy

Temperature SHALL be reproducible from documented rules rather than free-form agent judgment.

Frequency is the primary statistical input, but not the sole one.

## 11.1 Failure-family temperature

A failure family is **HOT** when any sufficiently strong condition applies, including:

```text
occurrence_count >= 3
```

or:

```text
recurrence_after_accepted_repair_count >= 1
AND recurrence is materially relevant
```

or a single occurrence has demonstrated critical project-wide impact.

A family is normally **WARM** when:

```text
occurrence_count == 2
```

or a single high-impact occurrence has credible architectural recurrence risk.

A family is normally **COLD** when:

```text
occurrence_count == 1
```

and impact, breadth, and recurrence risk are limited.

Severity, architectural breadth, cost, and recency may promote importance.

They MUST NOT silently erase the raw counts.

## 11.2 Positive-pattern temperature

A positive pattern is normally **HOT-POSITIVE** when:

```text
qualified_application_count >= 3
```

and evidence demonstrates meaningful repeated benefit,

or where a smaller number of applications establishes unusually high, broad, and well-qualified impact.

It is **WARM-POSITIVE** when evidence is meaningful but generality remains more limited.

A promising but insufficiently qualified technique is **PROVISIONAL**, not Hot.

## 11.3 No opaque importance score

Protocol 6.3 SHOULD prefer explicit rule-based classification over an unexplained weighted scalar.

If a future protocol introduces a numerical score, the raw statistics and derivation MUST remain inspectable.

---

# 12. Evidence maturity and promotion

## 12.1 PROVISIONAL

Used for:

```text
hypothesis
promising experiment
single uncontrolled observation
unqualified optimization
unconfirmed family assignment
```

Provisional findings MUST NOT become mandatory active-memory guidance.

## 12.2 SUPPORTED

Meaningful evidence exists, but generality or qualification remains incomplete.

## 12.3 PROVEN

The bounded claim is supported by adequate test, qualification, measurement, or analysis.

## 12.4 CONTRADICTED

Later evidence materially conflicts with the earlier conclusion.

Contradiction MUST be represented explicitly rather than deleting the old evidence.

## 12.5 RETIRED

The finding was valid under an earlier architecture but no longer applies because its assumptions or owner surface disappeared.

Retirement is not historical deletion.

The evidence chain remains recoverable.

---

# 13. Negative and positive learning must coexist

Protocol 6.3 MUST explicitly prevent a negative-only memory model.

The purpose is not:

```text
remember every dangerous thing and make agents afraid to change code
```

The purpose is:

```text
remember what history has demonstrated about effective engineering
```

The active summary SHALL include both:

```text
what repeatedly fails
what repeatedly succeeds
```

Positive patterns SHOULD be phrased as useful engineering instincts.

Examples:

```text
Prefer reuse of provenance-valid intermediate work.

Move conditional expensive preparation under the route that consumes it.

Preserve concurrency as an architectural capability when qualification
shows it materially matters.

Repair incorrect ownership directly instead of surrounding it with
compensating machinery.

Preserve capabilities during mechanism replacement rather than retaining
obsolete implementations.
```

Only evidence-backed instances may be promoted.

---

# 14. Failure-to-success linkage

PEM SHALL support explicit relationships among lessons.

Example:

```text
FAILURE_FAMILY:
  duplicate expensive preparation
        |
        v
DISCOVERY:
  preparation ownership is route-local
        |
        v
SUCCESS_PATTERN:
  lazy route-owned construction
        |
        v
PRESERVATION_CAPABILITY:
  cold routes do not activate expensive machinery
```

Multiple failures may support one stronger success pattern.

Multiple successful patterns may jointly establish a preservation capability.

This relationship SHOULD be represented compactly rather than duplicating evidence.

---

# 15. Applicability and architectural-rework gate

## 15.1 Mandatory consultation

Before substantial rework of existing architecture, the agent SHALL consult PEM.

This includes changes involving:

- architectural ownership;
- routing;
- state lifecycle;
- caching or reuse;
- scheduler/executor behavior;
- concurrency;
- performance-critical loops;
- generated/runtime representations;
- bootstrap behavior;
- package generation;
- frozen configuration/profile semantics;
- persistence;
- checkpoints;
- expensive preparation;
- replacement of mature machinery;
- cross-module interfaces.

## 15.2 Historical Applicability Set

The workplan or implementation record SHALL contain a **Historical Applicability Set (HAS)**.

Example:

```text
HF-003  applicable
SP-004  applicable
PC-006  applicable
HF-009  not applicable — checkpoint ownership unchanged
```

Hot entries MUST be considered when their applicability surface intersects the change.

A Hot entry may be marked not applicable, but a reason is required.

## 15.3 Capability-transfer map

When machinery is replaced, require:

```text
old mechanism
 -> demonstrated capability
 -> new owner/mechanism
 -> verification
```

Example:

```text
old executor
 -> bounded parallel execution
 -> new scheduler
 -> concurrency qualification Q63-...
```

Removal of old machinery does not grant permission to remove demonstrated capabilities.

---

# 16. Avoiding architectural timidity

Historical evidence SHALL behave as an engineering prior, not an absolute veto.

Protocol 6.3 SHALL state:

> Past success creates an evidence-backed preference, not architectural immunity.

> Past failure creates an evidence-backed warning, not a permanent prohibition.

A new approach MAY replace a proven approach when:

1. applicable historical evidence has been considered;
2. required preservation capabilities are identified;
3. the new design gives a coherent reason for replacement;
4. evidence appropriate to the new claims is produced;
5. relevant qualification passes.

This allows aggressive simplification and innovation without historical amnesia.

---

# 17. Promotion into invariants and executable sensors

Repeated learning SHOULD become increasingly executable.

Preferred progression:

```text
incident
 -> generalized lesson
 -> repeated evidence
 -> hot project memory
 -> preservation capability
 -> invariant
 -> regression/static sensor
```

Examples:

```text
repeated calculation
 -> call-count/reuse sensor

cold-route leakage
 -> activation sensor

accidental serialization
 -> concurrency/trace qualification

generated divergence
 -> package-integrity sensor

stale artifact reuse
 -> provenance validation
```

Not every lesson warrants automation.

Do not introduce test machinery whose maintenance cost exceeds demonstrated risk.

---

# 18. Protocol lifecycle integration

## 18.1 Design phase

For significant changes:

- read active engineering memory;
- resolve relevant learning families;
- create Historical Applicability Set;
- add preservation capabilities to the workplan;
- identify claims requiring new evidence.

## 18.2 Implementation phase

Implementation SHALL preserve applicable known capabilities unless the workplan explicitly supersedes them.

No new positive pattern is accepted merely because implementation completes.

## 18.3 Review phase

Review SHALL explicitly test for:

```text
historical defect recurrence
lost optimization
lost reuse
lost parallelism
new eager work
removed sensors
lost generated/package integrity
capability loss during mechanism replacement
```

## 18.4 Qualification phase

Qualification is the arbiter of bounded claims.

Where a workplan claims:

```text
faster
lower memory
better scaling
equivalent behavior
removed redundant work
preserved parallelism
```

qualification SHALL contain evidence suited to the claim.

## 18.5 Closeout phase

Every accepted significant repair/rework SHALL ask:

```text
Did this produce a new generalized lesson?
Did an existing failure family recur?
Did an existing positive pattern succeed again?
Did evidence contradict an existing lesson?
Should temperature change?
Should a preservation capability or sensor be promoted?
```

PEM MUST be updated when the answer materially affects project engineering knowledge.

---

# 19. Update transaction

A PEM update SHALL be treated as part of engineering closeout, not optional editorial cleanup.

For each relevant closeout:

1. identify candidate learning;
2. locate exact historical evidence;
3. classify family or create a new stable family;
4. update occurrence/application statistics;
5. bind evidence;
6. update cause or applicability only when evidence warrants it;
7. update temperature deterministically;
8. update evidence maturity;
9. update active summary if importance changed;
10. verify no existing still-valid lesson was lost;
11. run PEM structural/integrity checks;
12. commit the memory update with the engineering change or its accepted closeout.

---

# 20. Compactness and context-budget rules

PEM SHALL be useful to a fresh agent without forcing it to ingest the entire historical corpus.

Therefore:

- the active summary MUST remain tightly bounded;
- detailed incident narratives SHOULD remain in historical artifacts;
- PEM SHOULD contain generalized conclusions and compact evidence bindings;
- repetitive evidence prose MUST be deduplicated;
- cold families SHOULD be represented compactly;
- hot families MAY receive expanded treatment;
- exact references MUST replace unnecessary copied historical prose.

A periodic compaction pass MAY rewrite wording, merge duplicate exposition, and shorten evidence descriptions.

Such compaction MUST preserve:

```text
family identity
statistics
distinct evidence
cause distinctions
applicability
limits
preservation capabilities
contradictions
retirement state
```

This is a direct Protocol 6.2 lossless-representation obligation.

---

# 21. Protocol 6.2 preservation extension

The implementation SHALL copy T01–T39 unchanged and append 6.3 obligations.

The following logical requirements must appear using the next available stable IDs:

```text
T40  authoritative-history / derived-memory separation
T41  compact active engineering-memory representation
T42  stable learning-family identity
T43  exact evidence binding
T44  reproducible occurrence statistics
T45  evidence-backed positive success patterns
T46  hypothesis/evidence/maturity separation
T47  deterministic temperature classification
T48  architectural-rework applicability gate
T49  mechanism-to-capability transfer accounting
T50  promotion of repeated lessons into invariants/sensors
T51  mandatory closeout learning update
T52  preservation of quantitative effect size
T53  contradiction and retirement without historical erasure
T54  PEM generated/package/bootstrap integrity
T55  human-facing background and terminology completeness
T56  independent assembled-candidate qualification/review
```

If the accepted 6.2 baseline already uses any identifier after T39, append rather than collide.

No earlier row may be repurposed.

---

# 22. Owner-layer implementation strategy

Protocol 6.3 SHALL modify existing SSDP owner surfaces.

The implementer SHALL first identify the existing owners for:

```text
protocol doctrine
project bootstrap
project templates
workplan guidance
implementation guidance
review guidance
qualification
static activation sensors
generated/package synchronization
frozen profiles
documentation packaging
```

Extend those owners directly.

Do not introduce:

```text
memory-bootstrap-v2
parallel qualification wrapper
shadow package generator
second protocol dispatcher
compatibility adapter around incorrect ownership
```

unless repository architecture demonstrates that such machinery is genuinely the correct owner.

Reduction and rewiring are preferred over additive compensation.

---

# 23. Self-hosted migration

Protocol 6.3 SHALL use SSDP itself as the first qualified PEM project.

Create the initial SSDP Project Engineering Memory from repository history.

The backfill SHALL inspect at least:

- archived protocol workplans;
- Protocol 6.0/6.1/6.2 evolution where available;
- patch/commit history;
- Protocol 6.2 preservation evidence;
- qualification failures and repairs;
- independent reviews;
- replacement-bootstrap work;
- cold-route repair;
- static activation-sensor history;
- frozen-profile preservation;
- generated/package-integrity repairs;
- documentation-standard improvements.

These are candidate discovery surfaces, not pre-approved families.

The backfill agent MUST NOT invent occurrence counts from recollection.

Every initial family must be evidence-bound.

---

# 24. Initial candidate-learning investigation

During backfill, specifically investigate whether evidence supports generalized families around:

```text
loss of mature optimization during rework
repeated computation after architecture changes
cold-route activation
eager route-independent preparation
accidental serialization
loss of checkpoint/intermediate reuse
ownership leakage
generated/package divergence
replacement-bootstrap drift
frozen-profile mutation
loss of static activation protection
surface-level repair via wrappers instead of owner correction
documentation terminology/background drift
reviewing diffs instead of assembled candidates
```

Also investigate positive families around:

```text
route-local lazy activation
reuse of provenance-valid artifacts
bounded independent parallelism
direct ownership repair
semantic preservation maps
static activation sensors
assembled-candidate independent review
qualification-driven architectural acceptance
lossless compression with exact reconstruction references
```

No candidate becomes established project knowledge until its evidence is checked.

---

# 25. Validation and static integrity

Introduce only the minimum validation necessary to prevent memory corruption.

The validator or existing qualification owner SHOULD check:

- duplicate family IDs;
- malformed evidence references;
- count/evidence mismatch;
- invalid maturity values;
- invalid temperature values;
- Hot entries absent from active summary without justification;
- active summary referencing nonexistent families;
- retired entries still presented as active guidance;
- provisional findings presented as proven;
- lost T01–T39 preservation rows;
- generated/package divergence.

If equivalent validation can be integrated into an existing Protocol 6.2 checker, extend it there rather than creating a parallel tool.

---

# 26. Qualification plan

## Q63-01 — 6.2 semantic preservation

Demonstrate that Protocol 6.3 leaves every accepted 6.2 semantic obligation intact.

Requirements:

```text
T01–T39 preserved
replacement bootstrap preserved
cold-route behavior preserved
static activation sensors preserved
frozen profiles preserved
generated/package integrity preserved
```

## Q63-02 — Original and affected requalification

Re-run:

- original Protocol 6.2 qualification;
- every qualification previously required for replacement bootstrap;
- every qualification affected by cold-route repair;
- affected generated/package checks;
- affected frozen-profile checks.

## Q63-03 — PEM bootstrap activation

Demonstrate that a qualifying architectural-rework workflow receives the PEM consultation requirement.

Demonstrate that a trivial unrelated route does not unnecessarily activate expensive new machinery.

This SHALL preserve the cold-route principle rather than recreating an eager project-history scan everywhere.

## Q63-04 — Evidence resolution

For every seeded family:

```text
family -> occurrence/application -> evidence
```

must resolve.

No dangling binding passes qualification.

## Q63-05 — Statistical reproducibility

Independently reconstruct:

```text
occurrence_count
qualified_application_count
repair_cycle_count
recurrence count
```

from evidence records.

Stored totals must match.

## Q63-06 — One-cause/many-symptom counting

Create a fixture where one causal defect produces many failing tests.

Expected:

```text
occurrence_count == 1
```

## Q63-07 — Recurrence counting

Create or use a historical fixture:

```text
defect
 -> accepted repair
 -> later reintroduction
```

Expected:

```text
occurrence_count == 2
recurrence_after_accepted_repair_count == 1
```

## Q63-08 — Positive-evidence promotion

A claimed optimization with no benchmark/analysis must remain provisional.

A qualified optimization with valid evidence may become Supported/Proven.

## Q63-09 — Quantitative effect preservation

Verify that a qualified effect such as:

```text
4x runtime improvement
8x peak-memory reduction
```

survives summarization with baseline/candidate context and evidence reference.

## Q63-10 — Complexity-claim discipline

A claim of:

```text
O(N^2) -> O(N log N)
```

must fail promotion when supported only by one timing result.

It may pass when supported by adequate algorithmic analysis and, where appropriate, empirical scaling evidence.

## Q63-11 — Contradiction handling

Introduce counterevidence against a previously Supported/Proven pattern.

Expected behavior:

```text
old evidence retained
new counterevidence retained
maturity updated appropriately
active summary refreshed
```

No historical deletion.

## Q63-12 — Retirement

Retire a lesson whose architectural assumptions no longer exist.

Verify that it leaves active guidance while remaining recoverable historically.

## Q63-13 — Capability transfer

Replace a mechanism in a qualification fixture while preserving its demonstrated capability through a different implementation.

The system must permit the change when qualification succeeds.

This guards against architectural ossification.

## Q63-14 — Active-memory compactness

Verify that a fresh agent can obtain the high-importance project guidance without loading the full historical corpus.

Exact context-budget threshold should follow the existing SSDP profile mechanism rather than inventing an unrelated hard-coded limit.

## Q63-15 — Historical Applicability Set

Verify that architectural rework records relevant Hot families and preservation capabilities.

Verify that an applicability exclusion requires explicit rationale.

## Q63-16 — Closeout learning update

A qualified recurrence or successful new application must update PEM before final closeout when it materially changes project learning.

## Q63-17 — Package/generated integrity

All installed/generated copies of the protocol, templates, and guidance must agree with canonical sources according to existing Protocol 6.2 package-integrity semantics.

---

# 27. Required Protocol 6.2 falsification preservation

All four existing Protocol 6.2 falsification passes SHALL run unchanged.

Protocol 6.3 MUST NOT replace them with nominally similar new tests.

Their existing assertions, environments, and semantic purpose remain authoritative.

Any failure is blocking.

---

# 28. Protocol 6.3 falsification passes

In addition to the four inherited 6.2 passes, perform the following adversarial checks.

## F63-A — Speculation laundering

Attempt to promote:

```text
"this seems faster"
```

with no measurement.

Expected: rejected from Proven/active positive guidance.

## F63-B — Statistical inflation

Present:

```text
one defect
multiple symptoms
many failing tests
```

and attempt to count them independently.

Expected: one causal occurrence unless independent introduction is demonstrated.

## F63-C — Cargo-cult success pattern

Take a historically successful optimization and apply it where its required assumptions are absent.

Expected: PEM's applicability/limits prevent treating historical success as universal proof.

## F63-D — Summary divergence

Modify an active-memory conclusion without changing underlying detailed evidence.

Expected: qualification detects mismatch or independent review blocks acceptance.

## F63-E — Architectural ossification

Replace old machinery with a simpler/new mechanism that preserves all demonstrated capabilities and passes qualification.

Expected: Protocol 6.3 allows the replacement.

Historical memory is not an implementation veto.

## F63-F — Evidence contradiction

Supply valid later evidence opposing an earlier lesson.

Expected: no silent deletion; maturity and active guidance change explicitly.

## F63-G — History compression loss

Compact multiple family entries.

Expected: distinct occurrences, counts, evidence bindings, causes, limits, and preservation capabilities remain reconstructible.

## F63-H — False quantitative generalization

Provide one microbenchmark showing improvement and claim global project-wide scaling superiority.

Expected: claim strength reduced/rejected.

---

# 29. Performance and activation requirements

Protocol 6.3 itself MUST NOT become a new source of expensive repeated work.

Specifically:

- do not rescan the entire Git history on every ordinary task;
- do not recompute family statistics from all historical artifacts at every bootstrap;
- do not activate migration/backfill machinery during normal use;
- do not parse irrelevant archived workplans when the compact PEM already supplies the active context;
- do not serialize unrelated project initialization merely to load PEM.

The normal runtime path should primarily consume the already-curated compact artifact.

Deep historical traversal occurs when:

```text
creating/backfilling PEM
validating disputed evidence
updating a family
performing dedicated qualification
independent review requires source evidence
```

This requirement is itself subject to activation sensors and cold-route qualification.

---

# 30. Human-facing documentation requirements

Protocol 6.3 documentation SHALL follow the existing human-facing standard.

In particular:

- define Project Engineering Memory (PEM) before using the abbreviation;
- define learning family;
- define evidence binding;
- define occurrence;
- define successful application;
- define temperature;
- define evidence maturity;
- explain the distinction between history, memory, evidence, and transient context;
- define any additional non-common terminology in Background;
- expand abbreviations at first occurrence using conventional form.

Documentation SHOULD explain not merely what fields exist but why the distinction matters.

---

# 31. Workplan implementation phases

## Phase 6.3-A — Baseline capture and preservation map

1. Resolve accepted Protocol 6.2 SHA.
2. Inventory canonical owners.
3. Copy/verify T01–T39 unchanged.
4. Inventory 6.2 qualification and falsification gates.
5. Record generated/package and frozen-profile surfaces.
6. Append 6.3 preservation requirements.

**Gate:** no implementation before lossless baseline map is complete.

## Phase 6.3-B — Canonical doctrine and PEM schema

Implement:

- definitions;
- authority hierarchy;
- learning-family taxonomy;
- evidence model;
- statistics;
- temperature;
- maturity;
- contradiction/retirement;
- positive/negative balance;
- capability-transfer doctrine.

**Gate:** semantic review against 6.2.

## Phase 6.3-C — Workflow integration

Wire PEM into existing:

```text
design
workplanning
implementation
review
qualification
closeout
bootstrap
```

Do so through existing owners.

Add Historical Applicability Set and capability-transfer obligations.

**Gate:** no cold-route/eager activation regression.

## Phase 6.3-D — Integrity validation

Extend existing validation surfaces for:

- IDs;
- statistics;
- evidence bindings;
- active-summary consistency;
- maturity;
- package/generated integrity.

**Gate:** targeted structural qualification passes.

## Phase 6.3-E — Self-hosted historical backfill

Construct SSDP's own initial PEM from actual evidence.

Do not seed from recollection.

Investigate candidate families listed above.

Assign counts only after evidence inspection.

**Gate:** independent evidence reconstruction reproduces all statistics.

## Phase 6.3-F — Full qualification and falsification

Run:

- complete inherited Protocol 6.2 qualification set;
- affected requalifications;
- four inherited falsification passes;
- Q63-01 through Q63-17;
- F63-A through F63-H;
- generated/package integrity;
- frozen-profile verification.

## Phase 6.3-G — Independent Protocol Review

Perform a fresh-context independent review of the assembled candidate.

The reviewer SHALL:

- start from the workplan and independent-review handoff;
- independently inspect historical evidence;
- review the assembled candidate rather than only the diff;
- verify 6.2 preservation;
- verify all PEM statistics on sampled and Hot families;
- attempt falsification;
- inspect positive as well as negative guidance;
- verify that history does not become architectural dogma;
- verify that unsupported claims have not entered active memory.

PASS only if no genuine blocking issue remains.

---

# 32. Independent-review handoff requirements

Create a Protocol 6.3 independent-review handoff analogous to the established Protocol 6.2 model.

It SHALL identify:

```text
accepted Protocol 6.2 baseline SHA
Protocol 6.3 semantic candidate SHA
implementation workplan
T01–T39 preservation map
6.3 appended preservation rows
PEM artifact
self-hosted backfill evidence
qualification outputs
falsification outputs
generated/package state
frozen-profile state
```

The reviewer MUST NOT inherit implementation conclusions.

---

# 33. Pass / No-Pass criteria

## PASS

Protocol 6.3 passes only when:

1. all Protocol 6.2 doctrine remains preserved;
2. T01–T39 remain semantically unchanged;
3. all inherited qualification/falsification requirements pass;
4. PEM is clearly subordinate to authoritative evidence;
5. negative and positive learning are both represented;
6. statistics are reproducible;
7. counts are evidence-backed;
8. active guidance excludes unsupported speculation;
9. quantitative claims preserve evidence and scope;
10. architectural replacement remains possible;
11. demonstrated capabilities survive rework or are explicitly superseded with evidence;
12. normal workflows do not trigger unnecessary historical computation;
13. closeout updates project learning when warranted;
14. self-hosted SSDP memory is constructed from actual evidence;
15. generated/package integrity passes;
16. frozen profiles remain preserved;
17. independent review finds no genuine blocker.

## NO-PASS

Any of the following is blocking:

- loss or weakening of Protocol 6.2 doctrine;
- renumbering or semantic drift of T01–T39;
- unsupported positive guidance presented as fact;
- occurrence counts not recoverable from evidence;
- stale active summary;
- contradiction silently erased;
- memory becoming an independent source of truth;
- memory forcing preservation of obsolete mechanisms rather than capabilities;
- lost optimization or parallelism without explicit qualification;
- new eager full-history scanning on ordinary routes;
- package/generated divergence;
- frozen-profile drift;
- bypassed independent review;
- reviewing only the patch rather than the assembled candidate.

---

# 34. Reopen rule

If independent review finds a genuine blocker:

- reopen the workplan;
- identify the owning architectural layer;
- give precise repair instructions;
- prefer altering/removing incorrect ownership over adding compensating machinery;
- update qualification where the discovered defect represents a generalized recurrence risk.

If review uncovers a new evidence-backed project lesson while doing so, update PEM as part of the same repair cycle.

---

# 35. Definition of done

Protocol 6.3 is complete only when the repository can demonstrate the complete learning cycle:

```text
historical event
 -> exact evidence
 -> generalized finding
 -> statistical family record
 -> importance classification
 -> compact active memory
 -> applicability during future rework
 -> qualification
 -> updated project learning
```

and simultaneously demonstrate:

```text
no loss of Protocol 6.2 semantics
no loss of historical authority
no unsupported project doctrine
no architecture freeze
no ordinary-route historical rescan
```

---

# 36. Final architectural invariant

The central Protocol 6.3 invariant SHALL be:

> The project must be able to learn even when the individual agent does not persist.

The project accomplishes this not by preserving agent opinion, but by preserving evidence-backed engineering knowledge:

```text
what failed,
what succeeded,
why,
under what conditions,
how often,
with what demonstrated effect,
and where the evidence can be recovered.
```

The resulting memory should make a fresh agent neither timid nor amnesiac.

It should make the agent project-aware.
