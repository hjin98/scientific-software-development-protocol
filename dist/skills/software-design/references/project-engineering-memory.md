# Project Engineering Memory

Own **Project Engineering Memory (PEM)** representation: the compact project-local, non-authoritative record of demonstrated recurring failures, successful engineering patterns, discoveries, preservation capabilities, and temporary current notices. PEM helps a fresh-context engineer reuse project experience without turning history, statistics, reviews, tests, benchmarks, or old mechanisms into D1-D4 authority.

## Background and terminology

A **learning family** is one stable generalized project lesson. Current kinds are `FAILURE_FAMILY`, `SUCCESS_PATTERN`, `DISCOVERY`, and `PRESERVATION_CAPABILITY`. A **semantic identity envelope** is the bounded meaning attached to an accepted family identifier: kind, governing invariant or claim, semantic owner class, causal/mechanistic family, and materially relevant applicability dimensions. Wording may improve inside that envelope; a materially different meaning requires explicit lineage rather than silent identifier reuse.

An **occurrence** is one independently introduced or independently existing confirmed manifestation of a failure family. An **evaluated application episode** is one materially distinct engineering intervention applying a positive pattern. One coordinated intervention propagated across many files or sites is normally one episode plus multiple affected surfaces, not many applications. An **evidence provenance cluster** groups observations/applications that share a material upstream implementation, policy, oracle, dataset, benchmark harness, or other common dependency that limits evidentiary independence.

A **Historical Applicability Set (HAS)** is a current-work record of materially relevant PEM entries and their dispositions, bound to the exact accepted project-memory basis and candidate overlay used to make the decision. **Memory temperature** (`HOT`, `WARM`, `COLD`, `UNASSESSED`) is attention/salience only; it is not semantic authority, probability, evidence maturity, applicability, acceptance, or an activation command.

PEM evidence lifecycle, admissibility, stale state, observation/assessment separation, binding health, common-mode risk, and impact closure remain owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md). Failure-family membership and recurrence economy remain owned by [Convergence and development-cycle economy](convergence-and-cycle-economy.md). Capability ownership remains with [Software architecture and design](architecture-and-design.md); workflow/HAS/closeout with [Workflow and workplans](workflow-and-workplans.md); evidence methodology with [Testing and validation](testing-and-validation.md); accepted/base and branch mutation with [Git and version control](git-and-version-control.md); trust/privacy with [Security and trust boundaries](security-and-trust-boundaries.md); protocol/schema compatibility with [Protocol versioning and compatibility](protocol-versioning-and-compatibility.md).

## Authority boundary

PEM is evidence-backed decision support, never a fifth semantic authority domain.

```text
accepted D1-D4 / project / external authority -> what must be true
historical evidence                           -> what was observed
PEM                                            -> compact current learning representation
workplan/HAS                                   -> bounded cycle coordination
```

A test, benchmark, commit, review, count, temperature, or repeated historical success cannot promote a mechanism into authority. A `PRESERVATION_CAPABILITY` therefore declares one of:

- `EVIDENCE_ONLY` — demonstrated project property and design prior;
- `AUTHORITY_BOUND` — exact current owner independently requires the capability; mandatory because that owner requires it;
- `PROPOSED_FOR_PROMOTION` — evidence suggests the real owner may need amendment; not mandatory until that owner accepts it.

An authority-bearing owner is not free text. Schema 1 represents a mechanically healthy governing-owner binding as an immutable evidence route to the owner artifact plus accepted-state authority evidence. The route must resolve in the project-governed accepted state; candidate-only owner text/artifacts cannot create authority. When the generic validator cannot establish that accepted-state provenance, current normative use is `REVIEW_REQUIRED`. Structural resolution does not replace semantic Review: the reviewer still verifies that the cited accepted artifact is the real D1-D4/project/external owner for the exact claim.

When a project lesson becomes generic accepted doctrine at its actual owner, PEM retains only project-specific evidence/context that still improves decisions or retires redundant active guidance. It must not become a competing restatement of the current rule.

## Project-local canonical memory

Default discovery root is `PROJECT-ENGINEERING-MEMORY.md` at the governed project/repository root unless project authority declares one alternative path. The root records schema, protocol, project/repository/scope identity, coverage, accepted-base/candidate-overlay state, and the active summary.

One physical Markdown file is preferred while sufficient. Demonstrated scale, merge contention, or context/search cost may justify partitioning cold canonical detail. A partitioned memory still has:

```text
one root discovery/current-summary surface
one canonical home per family, notice, and ledger row
stable identifiers and routes
one coherent logical publication unit per semantic change
no duplicate hand-authored active truth
```

Root plus affected canonical partitions are published/reviewed coherently. A mixed revision is not a valid current memory. A generated index is optional and non-authoritative; stale/missing/corrupt index results cannot prove absence. Fall back to canonical search where feasible or expose `REVIEW_REQUIRED` uncertainty.

The packaged protocol contains this doctrine and the [Project Engineering Memory template](../templates/project_engineering_memory_template.md), never a live project's `PROJECT-ENGINEERING-MEMORY.md`.

## Schema 1

Protocol 6.3 supports `memory_schema_version: 1`. Schema identity is distinct from SSDP protocol version and Orchestrator workflow-profile schema.

The root front matter carries at least:

```yaml
memory_schema_version: 1
maintained_under_protocol: 6.3.0
project_id: stable-project-identity
repository: owner/name-or-project-defined-equivalent
scope: repository-or-bounded-project-scope
coverage_state: UNINITIALIZED | PARTIAL | RECONCILED_FOR_DECLARED_SCOPE
coverage_basis: explicit bounded sources/owners/surfaces/ranges plus blind spots
reconciled_through: already-existing accepted project identity
accepted_base: exact accepted project-memory basis
candidate_overlay: NONE-or-explicit-branch/cycle-identity
detail_files: []
```

`reconciled_through` is an identity horizon only. It does not say all earlier history was searched. Coverage completeness comes only from `coverage_state` plus `coverage_basis`; advancing a watermark cannot convert `PARTIAL` into exhaustive history or prove absence.

Unknown/newer/incompatible schemas are not guessed from similar headings. Only explicitly forward-readable identity metadata may be inspected; memory-dependent decisions become `REVIEW_REQUIRED` until compatible interpretation or explicit lossless migration exists.

## Canonical family records

Each family has one `### <ID> — <title>` section followed by exactly one fenced `yaml pem-family` record. Accepted identifiers use:

```text
FF-### failure family
SP-### success pattern
DS-### discovery
PC-### preservation capability
```

Each record carries enough current metadata to decide relevance before loading raw evidence:

```yaml
id: FF-001
kind: FAILURE_FAMILY
state: CURRENT
maturity: SUPPORTED
temperature: UNASSESSED
summary: one bounded lesson
semantic_identity:
  invariant_or_claim: ...
  owner_class: ...
  mechanism_family: ...
  applicability_dimensions: ...
aggregation_scope: ...
coverage_state: PARTIAL
coverage_basis: ...
applicability: [owner/surface/mechanism/regime cues]
relations: []
```

Accepted IDs are never recycled. Material change outside the semantic identity envelope requires explicit `SUPERSEDES`, `SPLIT_FROM`, `MERGED_FROM`, `REPLACES`, or equivalent defined lineage. Current lineage must be acyclic and resolve each accepted historical ID to one unambiguous current disposition. A family that is the historical target of active superseding/replacement/split/merge lineage cannot simultaneously remain an unqualified `CURRENT` peer. Split/merge reallocates existing ledger identities and prevents parent-plus-child double counting.

Typed PEM relations may also express `LED_TO`, `NARROWS`, `GENERALIZES`, `SUPPORTS_LEARNING_FROM`, `CONFLICTS_WITH`, and other explicitly defined non-authoritative relationships. Relations help retrieval/impact closure; they cannot recursively manufacture warrant. Every substantive endpoint remains independently evidence-bound and, if normative, authority-bound.

## Failure occurrences

Failure membership follows the convergence owner: materially equivalent governing invariant, semantic owner class, and repair-relevant mechanism. Symptoms, filenames, error text, or broad subsystem labels are insufficient.

A failure record uses `occurrences`, each with a stable family-scoped ID and, when material:

```yaml
- id: O01
  event_identity: immutable project/commit/incident identity
  lifecycle_context: qualification
  source_project: local-or-explicit-source
  surfaces: [...]
  observation: what actually happened
  cause_claim: bounded causal interpretation
  cause_evidence: [...]
  repair: immutable repair identity
  repair_acceptance: immutable accepted qualification identity
  assessments:
    - id: AS01
      state: ADMISSIBLE
      conclusion: CONFIRMED
      evidence: [...]
```

One causal episode producing many failing tests is normally one occurrence. A later independent reintroduction after an actually accepted repair is another occurrence and recurrence. Commit/file/issue timestamps or rebase order alone cannot establish recurrence chronology. For Git-native recurrence, a repair-acceptance evidence route must resolve to immutable content contained by the exact accepted project state. Its typed `pem-repair-acceptance` record names the exact `repair_identity`, declares `state: ACCEPTED`, and binds `owner` to an immutable owner route whose content is unchanged at that acceptance event. An arbitrary descendant commit/file, candidate-only acceptance artifact, free-text owner, or owner route that changed before acceptance is not acceptance evidence. Non-Git recurrence requires an equivalent durable accepted-state relation binding the same repair identity plus independently warrantable ordering; unresolved ownership remains review-required and cannot increment recurrence.

```yaml pem-repair-acceptance
repair_identity: commit:<immutable-repair-identity>
state: ACCEPTED
owner: owner/project@<immutable-owner-revision>:path/to/governing-owner.md#stable-section
```

Safe/disconfirming evidence that shows a family cause/regime is too broad narrows, splits, or reclassifies the family; it does not erase the real historical occurrence.

## Positive application episodes

A success pattern records **all materially applicable evaluated episodes**, not only favorable ones:

```yaml
applications:
  - id: A01
    episode_identity: immutable intervention identity
    lifecycle_context: qualification
    source_project: local
    surfaces: [...]
    provenance_cluster: CLUSTER-01
    subject: ...
    comparator: ...
    intended_benefit: ...
    outcome: SUPPORTING | NEUTRAL | CONTRADICTING | INCONCLUSIVE
    observation: ...
    assessments: [...]
    quantitative_effect: ...
    uncertainty: ...
    costs_tradeoffs: ...
```

Repeated executions of one intervention and one coordinated rollout across many sites remain one application episode. Surface breadth is tracked independently. A later materially distinct qualified application may add one episode. Copied/cherry-picked history does not multiply it.

Before a new/strengthened success pattern becomes current positive guidance, search the declared bounded coverage/aggregation scope for materially applicable neutral, contradicting, failed, and inconclusive attempts as well as wins. After admission, material counterevidence remains visible. A pattern with unresolved material contradiction is narrowed/split or becomes `REVIEW_REQUIRED`; high historical support cannot average away a contradiction.

## Evidence maturity and guidance strength

Maturity is relative to the exact bounded claim/regime:

```text
PROVISIONAL -> plausible but material evidence obligations remain open
SUPPORTED   -> at least one suitable admissible route supports the bounded claim
PROVEN      -> every owner/workplan evidence obligation for that exact claim is closed
               with applicable admissible evidence, including required independence,
               replication/comparator, and contradiction closure
```

For schema-1 Protocol 6.3 `SUCCESS_PATTERN` records, `PROVEN` is the generalized transferable pattern claim: replication and independent replication are therefore derived obligations even if claimant-supplied `requires_*` flags are absent or false. Independent replication requires at least two admissible supporting provenance clusters. Claimant flags may add detail but cannot waive obligations implied by the claim/family class.

Count, temperature, age, reviewer vote, or repeated assertion cannot auto-promote maturity.

Keep claim strength explicit:

```text
OBSERVED/WORKS   -> supported absolute outcome in stated regime
RECOMMENDED      -> eligible project instinct under stated applicability/limits
PREFERRED/DEFAULT/BEST -> comparative decision claim
```

Evidence that one technique works does not establish that it is best, preferred, default, or highest leverage. Comparative guidance requires admissible comparison over viable alternatives under the governing objective/constraints, or explicit priority from the real current owner. Multi-objective tradeoffs stay visible unless accepted authority supplies the priority.

Two individually supported current patterns that overlap but recommend incompatible actions must narrow regimes, state a decision/tradeoff predicate, route to current owner priority, or remain contested/`REVIEW_REQUIRED`. They cannot appear as simultaneous unconditional instincts.

Positive guidance is eligible only while the pattern is `CURRENT`, sufficiently mature for the wording used, supported by healthy/admissible bindings, and free of unresolved material contradiction in the stated regime.

## Evidence rows, assessments, and provenance

Realization/observation and assessment are separate. A later discovery that an oracle was defective, a benchmark confounded, or a family assignment wrong supersedes assessment/admissibility; it does not rewrite the original observation. A genuine clerical correction preserves correction provenance and enough prior record to explain the change.

Assessment succession is explicit rather than positional. A reassessment that replaces earlier current interpretation records `supersedes: [AS01, ...]`; serialized row order, editor chronology, reviewer count, or reviewer prestige never selects current truth. Assessments not superseded by another assessment are live. If multiple live competent assessments materially disagree in state or conclusion, current use is contested/`REVIEW_REQUIRED` until discriminating evidence or an explicit adjudicating assessment supersedes the resolved live assessments. Equivalent live assessments may corroborate interpretation but do not multiply the underlying observation/application episode.

Only rows whose current explicitly resolved applicable assessment is admissible for the bounded claim contribute to current confirmation/support statistics. Invalid, stale, rejected, retired, challenged, inconclusive, or unresolved-disagreement rows remain historically recoverable when material but cannot silently remain current support.

Material evidence routes prefer immutable repository/project identity + revision + path + stable section/test/finding. A bare branch/default path is not a durable warrant. For non-local evidence, include source repository/project identity; a commit SHA alone is not globally unambiguous. If a material binding becomes unavailable/uninterpretable, current use degrades to `REVIEW_REQUIRED`/`UNAVAILABLE` and unsupported positive guidance is withdrawn.

Distinct application episodes may still share a material provenance cluster. That is compatible with counting distinct applications, but independence-sensitive maturity or comparative claims must not treat shared policy/implementation/oracle/dataset/harness dependence as independent corroboration.

## Derived statistics and temperature

Ledger rows are canonical; counters are derived, never independently hand-maintained.

Failure statistics include confirmed occurrences, independent repair cycles, affected surfaces, recurrence after accepted repair, first/last confirmed, coverage/aggregation scope, and lifecycle strata. Success statistics include evaluated/supporting/neutral/contradicting/inconclusive applications, rejected/invalid rows when material, independent surfaces, first/last evaluated, coverage/aggregation scope, and lifecycle strata.

Counts are descriptive within declared coverage/aggregation scope. They are not probability, rate, incidence, or causal strength without an explicit exposure/opportunity denominator and defensible sampling basis.

Default salience floors:

```text
confirmed failure occurrences >= 3       -> HOT
confirmed failure occurrences == 2       -> WARM
confirmed failure occurrences == 1       -> COLD only with adequate coverage; otherwise UNASSESSED
qualified supporting applications >= 3   -> HOT
qualified supporting applications == 2   -> WARM
qualified supporting applications == 1   -> COLD or UNASSESSED subject to coverage
```

A single event may be promoted for demonstrated severity, breadth, cost, architectural criticality, or exceptional benefit, but the base classification, evidence-bound override, and final temperature remain distinguishable. Temperature never selects authority, applicability, or acceptance.

## Active summary and salience

The active summary is a derived attention view of canonical current records. It should answer compactly: what repeatedly fails, what repeatedly works, what capabilities matter and which are authority-bound, what current notices matter, and what engineering instincts are useful now. Its family rows retain stable ID, kind, temperature, maturity/state, authority-binding/binding-health status, guidance strength, current evidence count, and the bounded lesson so an unavailable material warrant or authority-bound capability is not hidden by compaction.

Do not turn it into a positive leaderboard. Current high-impact unresolved contradiction, unavailable warrant, security/reliability hazard, expired high-risk notice, or authority-binding uncertainty receives consequence-aware visibility before lower-consequence optional positive guidance. Lower-salience mandatory owner constraints remain active even if absent from the summary.

When PEM is triggered, applicability matching is not restricted to active-summary or `HOT` entries. Match bounded current metadata over owner, surface, mechanism/capability, regime, project scope, and task; a `COLD` family may be decisive while a `HOT` unrelated family remains unloaded.

## Current notices

Temporary high-impact state that is not yet a generalized family may use `NT-###`. A notice records bounded claim, normative owner or explicit non-authoritative status, evidence/source binding and health, applicability, and review/expiry condition. Notices never contribute to family counts. When review/expiry triggers, remove unqualified active guidance and reconcile to current owner, family, `REVIEW_REQUIRED`, or `RETIRED`.

## Branch overlays, HAS, and publication

The accepted/base memory is selected by project workflow/Git acceptance semantics, never simply `main`, default/latest, timestamp, or self-declaration. For schema-1 authority-bearing structural validation, `accepted_base` exposes the exact immutable accepted `project_state` separately from explanatory basis text; opaque prose cannot be used to self-ratify a current owner. Same-branch candidate memory composes explicitly:

```text
accepted/base PEM + validated branch candidate overlay -> effective branch-local decision support
```

The overlay preserves its exact base identity, remains visibly candidate, cannot self-ratify, and cannot erase accepted entries by omission. Candidate deletion/retirement is explicit. Conflicting/partial composition is `REVIEW_REQUIRED`.

A memory-triggering workplan/HAS records the exact accepted memory basis and candidate overlay used. If the accepted basis materially advances before integration/closeout, inspect the changed interval/affected owners/surfaces and refresh dispositions. Do not let a stale HAS remain apparently reproducible.

Routine evidence/PEM updates avoid self-SHA recursion:

```text
engineering/evidence commit exists immutably
 -> qualification/assessment exists or is durably identifiable
 -> descendant PEM reconciliation binds those pre-existing identities
```

A PEM-containing commit never needs its own SHA to establish its substantive claim.

## Conditional activation and missing memory

Load PEM only when project history can materially change the decision: substantial rework of mature D1-D4 semantics/concretization, replacement/consolidation of mature machinery, suspected recurrence, substantial optimization/scaling work, migration/recovery/revert/restoration, or an active workplan explicitly binding PEM.

A first clean local defect with no recurrence/generalization signal remains local. Ordinary documentation, trivial implementation, and unrelated cold concerns do not load PEM merely because it exists.

Missing, malformed, unsupported, or partial PEM cannot prove no relevant lesson exists. For an established project doing memory-triggering work, perform bounded historical intake for the affected scope or retain explicit uncertainty. Unrelated routes remain usable; PEM is not a runtime/build single point of failure.

## Project/fork scope and rollback

Copying/forking a PEM does not manufacture local incidence. Preserve source-project identity and treat inherited entries as external/historical evidence until project governance declares lineage continuity/reconciliation. Cross-project aggregation requires an explicit multi-project scope and compatible evidence.

Restoring an older PEM snapshot does not make it current merely because it parses. Reconcile its schema, scope, accepted basis, owners, evidence, and uncovered project interval. Version-bound Protocol 6.2 work leaves a 6.3 PEM inert rather than deleting/reinterpreting it. Re-adoption of 6.3 validates supported schema and reconciles from the last covered accepted identity.

## Maintenance and closeout

A material accepted repair/rework/optimization/revert/restoration asks whether a known family recurred, a positive pattern gained any outcome class, a discovery/capability emerged, evidence narrowed/retired/invalidated a lesson, coverage/aggregation/project scope changed, a binding became unhealthy, a notice expired, a causal claim changed, or base/overlay/schema reconciliation is required.

Update PEM only when admission threshold is met or an existing entry materially changes. Ordinary fix chronology stays in Git/native evidence. Responsibility follows the substantive owner; `software-documentation` may reconcile representation but cannot self-promote a finding, declare `AUTHORITY_BOUND`, or adjudicate a material evidence conflict.

Apply the Lossless Representation Rule: compact by generalization and progressive disclosure, not by deleting identity, scope, lifecycle, counterevidence, assessment lineage, uncertainty, tradeoffs, authority binding, evidence routes, or conditions needed to decide applicability.
