---
kind: protocol-major-revision-workplan-consolidated
workplan_id: SSDP-8.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-CONSOLIDATED
protocol_version: 6.6.0
target_protocol_version: 8.0.0
status: proposed
created_date: 2026-09-28
base_protocol: pre-cutover document-controlled baseline (section 28.1; currently Protocol 6.6)
supersedes:
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-1-SECOND-REVIEW-CLOSURE
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION
  - SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT
  - SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND
design_review_state: consolidation-pending-independent-losslessness-review
d3_architecture_state: proposed; deliberate D3 orchestrator reassessment required before D4
implementation_handoff: not-authorized
active_serious_challenge: none
---

# SSDP 8.0 — Deterministic Control Plane and Mandatory Orchestrator Migration — Consolidated Workplan

## 0. Current disposition

This file is the **single current planning handoff** for the deterministic control-plane / mandatory-orchestrator major revision, now targeting **Protocol 8.0**. It supersedes the composition of the parent workplan, Revisions 1-7 and the Protocol 8.0 version-rebind record. Those nine files are preserved byte-identically under `workplans/archive/` as historical design and review evidence. Design, reassessment and Review SHALL reconstruct the contract from this file plus accepted current owners, not by replaying the amendment chain.

**Terminology.** In this file **Protocol 8** means this deterministic-control revision and **Protocol 7** means the scientific inspectability / epistemic initiative revision governed by `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`. The archived `SSDP-7.0-DETERMINISTIC-*` identifiers are historical design identities; their embedded "Protocol 7.0" target labels mean Protocol 8.0 (§37.1). The **pre-cutover baseline** is the accepted document-controlled protocol that Protocol 8 inherits and falls back to (§28.1).

**What consolidation changed.** It is a representation and version-label change only:

- the target version is 8.0.0, as the rebind record decided;
- "Protocol 7" meaning this design reads as "Protocol 8";
- statements that name Protocol 6.1 (or 6.2-6.5) as the current document-controlled baseline, fallback or rollback read as the pre-cutover baseline of §28.1;
- where Revisions 1 and 2 narrowed, corrected or strengthened the parent, the governing result is stated once in place; superseded parent wording (for example the over-broad Scheduler supersession bullet) survives only in the archive;
- the inheritance revisions (3-7) and the rebind are folded into §2, §3.2, §28 and §37.

It adds no requirement, removes none, and changes no D3 decision. If this file and the composed archived family disagree materially, that is a consolidation defect: the composed family's meaning governs until the owning process repairs this file, and dependent work reports it rather than choosing the more convenient reading.

```text
TARGET: Protocol 8.0.0 (deterministic control plane / mandatory orchestrator)
GOVERNING BASE: Protocol 6.6.0 accepted-current (identities owned by PROTOCOL-RELEASE-STATE.yaml)
PRE-CUTOVER BASELINE: Protocol 6.6 recovery 384666764da4c55b282e6b1595ab97e2f86e1dc4 (§28.1)
DESIGN REVIEW HISTORY: parent + Revisions 1-2 second-review final PASS under Protocol 6.1 (dispositions recorded
  only in archived Revision 1 §18 and Revision 2 §9; no separate durable review record); Revisions 3-7 changed no D3
  semantics; that PASS does not make the proposed D3 architecture accepted-current
CONSOLIDATION: pending independent losslessness check against the archived family
DELIBERATE D3 ORCHESTRATOR REASSESSMENT/SUPERSESSION: REQUIRED BEFORE D4 (§3)
PROTOCOL 8 D4 IMPLEMENTATION: NOT AUTHORIZED
MAIN MERGE / PROTOCOL 8 CUTOVER: NOT IMPLIED BY THIS DESIGN WORKPLAN
SERIOUS CHALLENGE: NONE
NEXT ACTION: independent losslessness check of this consolidation; then the deliberate D3 reassessment (§3.2, §30)
```

## 1. Objective and major-version boundary

Protocol 8.0 changes workflow authority itself. It is therefore a major revision.

The pre-cutover baseline remains the final document-controlled protocol. Protocol 8.0 moves machine workflow control into a lightweight formal control plane and makes the orchestrator a mandatory participant in the standard SSDP development cycle.

The transition must preserve, losslessly, all still-valid scientific, numerical, architectural, implementation, evidence, challenge, historical, versioning, simplicity, validation and qualification doctrine of the pre-cutover baseline (§2). Protocol 8.0 changes **how workflow state and transitions are controlled**, not where substantive engineering/scientific meaning lives.

Target architecture:

```text
rich semantic repository
  D1/D2/D3/D4 authority
  workplans/change plans
  scientific/method papers
  architecture/specifications
  source code
  evidence specifications/results
  historical reasoning/review reports
          |
          | referenced by
          v
lightweight deterministic control plane
  identity + revision
  typed relationships
  state + obligations
  events + provenance
  task/result contracts
  transition rules
          |
          v
mandatory orchestrator
          |
          v
stochastic/exploratory agents and tools
```

The control plane SHALL coordinate and index semantic artifacts, not reproduce them.

## 2. Governing inherited doctrine — no semantic regression

Protocol 8.0 SHALL preserve every still-valid accepted capability of the pre-cutover baseline and of the earlier accepted versions it inherits, including:

- D1-D4 semantic authority and abstraction/concretization doctrine;
- authority-source/semantic-level orthogonality and governed side constraints;
- feasibility before optimization, minimum justified complexity, active simplification, recurrence/convergence economics;
- version-pinned historical truth and non-retroactive reinterpretation;
- snapshot-complete semantic handoff;
- bounded Challenge Pass, Serious Challenge, human ratification/risk override, truthful non-closure;
- evidence specification -> evidence realization -> observation -> assessment;
- evidence admissibility, bounded invalidation, stale passing/failing protection, and durable-evidence preference;
- proxy-proof/real-semantic-owner acceptance;
- focused/stage-local/final affected regression, integration, required-check accounting, and production-qualification separation;
- language/tool dispatch and optional specialist boundaries;
- semantic evolution history distinct from current normative documents;
- behavioral qualification of governed decisions rather than wording;
- **Protocol 6.2 Lossless Representation:** governed scope cannot be narrowed for convenience; generic doctrine has one canonical detailed owner; root/concern/leaf activation is explicit, bounded and acyclic; ordinary links, semantic-dependency views, package membership and generated routing traces do not become activation authority; cold doctrine remains discoverable/reachable; context reuse is validity-scoped; current truth is separated from history; importance weighting cannot omit lower-salience mandatory closure; static routing/package evidence is not represented as live model telemetry;
- **Protocol 6.3 project learning:** Project Engineering Memory (PEM) is evidence-backed project-local decision support, not D5; activation is conditional on material historical relevance; Historical Applicability Set (HAS) closure is task-local; stable family identity cannot launder semantic change; evidence/binding health and current authority remain independently governed; positive guidance requires discriminating evidence; summaries/temperature/maturity do not create authority or applicability;
- the accepted Protocol 6.4, 6.5 and 6.6 doctrine carried into the pre-cutover baseline, including the Protocol 6.6 capabilities bound in §3.2;
- when Protocol 7 is accepted before Protocol 8 cutover, Protocol 7 doctrine through its inheritance reconciliation (§37.2).

Protocol 8 automation SHALL NOT weaken a substantive pass threshold, manufacture closure, or transform an epistemic judgment into a deterministic fact merely because machine control requires a finite state vocabulary.

**Inheritance does not mutate the control design.** No Protocol 8 control-plane field, state transition, reducer rule, event schema, persistence contract, ownership boundary, recovery algorithm, cutover invariant or D3 component identity changes merely because the inherited document-controlled baseline advanced. Do not introduce a wrapper, compatibility registry, duplicate activation graph, PEM registry, shadow control plane, duplicate memory database or machine field solely to mirror inherited representation or project-learning doctrine. If future Protocol 8 architecture cannot preserve an accepted inherited invariant, reopen the earliest affected D3 authority and resolve the contradiction there; do not patch D4 around an inadequate D3 abstraction.

## 3. Deliberate D3 orchestrator-architecture supersession and reassessment

### 3.1 Required supersession

The currently frozen orchestrator architecture (`orchestrator/docs/architecture.md`, architecture version 1.6.0) predates Protocol 8 and includes invariants that intentionally make manual operation first-class and prevent Tracker/Scheduler from becoming workflow authority. Protocol 8 changes some of those assumptions.

Therefore this workplan SHALL NOT implement the new control plane as a hidden layer beneath the existing frozen orchestrator Architecture 1.6.0.

Before implementation, Protocol 8 must reopen the affected D3 orchestrator authority and produce a new accepted Architecture Manual revision that explicitly supersedes incompatible current invariants, including as applicable:

- workplan/profile/result ownership of workflow routing/control;
- Tracker-as-evidence-only semantics where incompatible with the new canonical event/state store;
- manual operation as an independently complete standard execution mode;
- existing result-envelope semantics where they conflict with TaskEnvelope/ResultEnvelope authority boundaries;
- current module ownership boundaries if the new reducer/state/event/graph owner cannot fit coherently without violating dependency direction.

Scheduler is not on this list: its subordination to workflow intent is preserved (§4).

Preserve unrelated architectural guarantees unless independently invalidated, including progressive modularity where still admissible, strict dependency direction, graceful failure where compatible with mandatory control, one composition root, versioned public boundaries, explicit route identity, repository containment, private-state/security rules, idempotency, bounded concurrency, and no duplicated workflow authority.

Prefer alteration/reduction of the existing architecture over additive wrapper machinery. Do not retain contradictory old and new workflow owners behind adapters.

### 3.2 Protocol 6.6 reassessment input

Protocol 6.6 evidence and capabilities are mandatory inputs to this reopen. The reopen must explicitly reconsider whether the proposed mandatory control-plane/orchestrator architecture remains the minimum justified architecture in light of Protocol 6.6's demonstrated operational simplification (reduced root router), stochastic-prose limits (the stochastic Protocol-6 robustness boundary and bounded live trajectory evidence), strict no-self-adoption version semantics and root-router preservation results. It may confirm, simplify, narrow or supersede the design in this file only through the normal D3 acceptance process, including independent falsification before accepted-current promotion. Nothing in this file performs that adjudication or makes the proposed architecture accepted-current.

## 4. Workflow reducer versus Scheduler ownership

Protocol 8 SHALL preserve this ownership separation unless an independently reviewed D3 redesign demonstrates a materially superior coherent decomposition without duplicate authority:

```text
workflow reducer / obligation engine
    owns legal workflow-state transitions,
    dependency/impact propagation,
    readiness/blocking,
    and required next obligations

Scheduler
    owns resource/account/model/route feasibility,
    metering/prediction/reservation,
    and selection among execution routes for work
    that the workflow control kernel has already declared ready
```

Scheduler may provide resource facts that cause a ready obligation to become execution-blocked or may reject a route on hard feasibility grounds. It does not decide that a scientific/design/implementation/review stage is semantically complete, invent the next authority mutation, or become a second reducer. Scheduling remains subordinate to workflow intent: Protocol 8 changes the owner of deterministic workflow state from document interpretation to the control kernel; it does not make resource optimization the workflow authority.

Scheduler observations and replay:

- Scheduler may observe live resource/account state for **new** admission/routing decisions;
- the resulting admission/reservation/route decision that affects workflow is captured as a control observation/event;
- historical replay reuses the recorded accepted decision/facts and does not recompute old routing against today's quotas/prices/account availability;
- rerouting after a new resource observation is a new event/decision, not reinterpretation of the old event.

The D3 architecture reopen SHALL explicitly place reducer, obligation, graph, scheduling and agent-execution ownership and verify one-way dependency boundaries among them.

## 5. Plane separation and semantic authority

### 5.1 Semantic plane

Carries substantive scientific/engineering meaning:

- D1 Scientific Method Paper family;
- D2 Numerical & Algorithmic Method Paper family;
- D3 Architecture Manual family;
- D4 Specification/code/executable behavior;
- workplans/change plans;
- review/qualification reports;
- semantic evolution records;
- evidence specifications and bulk/raw evidence artifacts;
- guides/runbooks/publication material as applicable.

### 5.2 Control plane

Carries only information needed for deterministic coordination:

- stable logical IDs and revision identities;
- typed semantic/control relationships;
- task/run/attempt identity;
- lifecycle and validity states;
- obligations/readiness/blockers;
- action type and transition preconditions;
- evidence admissibility state and artifact references;
- event/provenance records;
- human-gate state;
- semantic artifact references and immutable task/result bindings.

### 5.3 Execution plane

Contains orchestrator, agent harnesses, tools, local/remote transports, test runners, repository adapters, and other execution machinery.

Global invariant:

> The control plane is a lightweight deterministic coordination skeleton over the semantic repository. It indexes, relates, validates, and transitions semantic artifacts; it does not replace or reproduce them.

### 5.4 Semantic authority versus control projection

- D1-D4 semantic artifacts and accepted governed external authority remain the owners of substantive meaning;
- the control plane is authoritative for **workflow/control facts** such as accepted identity bindings, lifecycle state, obligation readiness, admissibility classification, and legal transitions;
- graph/state records representing semantic relationships are accepted **projections/bindings of semantic facts**, not an independent source entitled to redefine the underlying scientific/engineering meaning.

> A control record may bind to and operationalize an accepted semantic fact, but it may not silently replace the semantic owner of that fact.

If a current semantic artifact and its canonical control projection disagree materially, classify this as a **control/semantic integrity defect**. Stop dependent canonical transitions until the disagreement is reconciled at the proper owner. Do not automatically prefer JSON because it is machine-readable, and do not automatically overwrite JSON from prose without a validated transition.

Every accepted semantic-classification fact used for deterministic propagation carries sufficient provenance to identify the semantic subject/revision, the owning domain/authority, the assessment/decision that established the classification, and required independent/human ratification state where applicable. The orchestrator validates authorization and transition legality; it does not manufacture semantic acceptance.

## 6. Minimal-sufficient-control-data doctrine

For each proposed control field ask:

> Does the deterministic controller need this value to select, validate, serialize, replay, or audit a legal transition?

If no, keep it in a referenced semantic artifact.

Control records SHOULD contain references plus bounded classifications, not essays, equations, source patches, full review reasoning, or large test logs.

Required anti-duplication rules:

1. control records SHALL reference semantic authority rather than duplicate it except for bounded transition-critical values;
2. semantic documents SHALL NOT remain canonical stores of machine workflow state after that state is migrated to Protocol 8;
3. raw evidence stays in native/referenced artifacts; control state records admissibility, subject/revision, observation class, and pointers needed for transition logic;
4. machine event history records control transitions; semantic historical documentation records why scientific/engineering meaning changed. Neither replaces the other.

## 7. Formal control data standard and compatibility

Define a versioned SSDP control data model. Canonical interchange SHOULD be JSON unless design review finds a concrete superior alternative.

At minimum specify formal schemas/contracts for:

- protocol/control metadata;
- semantic subject/reference identity;
- authority/concretization graph nodes/edges;
- evidence specification/realization/observation references;
- task envelope;
- result envelope;
- typed finding;
- obligation;
- action/transition proposal;
- human gate/decision;
- accepted event;
- derived/current state view.

Use JSON Schema or an equivalently rigorous validation mechanism for syntax and bounded enumerations. Schema versioning is independent of Protocol semantic versioning where justified; compatibility rules must be explicit. Do not allow free-form prose values to substitute for fields the reducer must interpret deterministically.

Forward compatibility preserves the existing orchestrator principle that public records tolerate additive optional fields while unsupported required semantics fail explicitly:

- unknown optional non-transition-critical fields may be preserved/ignored according to the declared schema compatibility contract;
- an unknown action, required state, transition-critical edge type, or mandatory field is not silently dropped;
- unsupported required semantics produce a structured incompatible/blocked result;
- action/state vocabularies may evolve through explicit versioning rather than pretending one enum is permanently complete.

## 8. Identity, revision, and semantic-reference model

Separate stable logical identity from semantic revision:

```text
D2:target-size-objective
!=
D2:target-size-objective@<specific semantic revision>
```

Relationships/evidence whose meaning depends on a particular accepted revision must bind to that revision.

Artifact references must identify enough source state to avoid silent drift, using Git commit/path/section identity or another justified immutable identity. Additional hashing/manifest machinery is required only where Git/repository identity is insufficient. Protocol 8 SHALL NOT invent a universal per-claim hash graph if bounded artifact/revision references establish the necessary control invariant more simply.

## 9. Typed authority/concretization and evidence graph

Migrate the material dependency model of the pre-cutover baseline into a formal typed graph sufficient for impact closure and orchestration. Candidate edge semantics include `CONCRETIZES`, `DERIVED_FROM`, `DEPENDS_ON`, `ASSUMES`, `CONSTRAINED_BY`, `SUPERSEDES` / `REPLACES`, `CHALLENGES` / `CONTRADICTS`, `EVIDENCES` and `GENERATED_BY`. The schema must distinguish evidentiary target from execution dependency.

The graph is logically machine-authoritative for Protocol 8 control decisions only after cutover, and only as a projection of semantic facts (§5.4). Its physical storage may be relational tables, JSONL-derived indexes, SQLite, or another minimal adequate implementation. Do not require a dedicated graph database absent demonstrated need. Derived graph/index stores must be reproducible from canonical accepted records/events and must not become independently edited parallel authority.

**Graph completeness is scoped to deterministic decisions.** Protocol 8 does not require formalizing every semantic relationship in the repository. The machine graph must be complete enough for the deterministic control claims it actually makes. If the orchestrator cannot establish the material dependency closure for a requested transition because required semantic relationships are absent/ambiguous, it SHALL create a review/discovery obligation or block rather than assuming no dependency exists:

> absence of an edge is not automatically evidence of independence unless the governing schema/authority explicitly guarantees graph completeness for that relation/scope.

Graph-completeness declarations themselves must be scoped/versioned and evidence-backed where they are used to justify automatic closure.

## 10. Evidence formalization without bulk-data migration

Formalize the baseline's evidence semantics while leaving substantive evidence in native artifacts. Control metadata for an evidence realization should be sufficient to determine, when applicable:

- evidence specification ID/revision;
- governed subject ID/revision;
- evidentiary target;
- execution dependencies;
- run/environment/input-regime identity required for applicability;
- observation/result class;
- admissibility/validity state;
- referenced detailed report/raw artifacts;
- supersession/invalidation reason when stale or rejected.

Do not equate test source with evidence. A reusable evidence specification may survive while previous realizations become stale or require rerun/remapping.

## 11. Composed state model, not one monolithic FSM

Protocol 8 SHALL use bounded interacting state dimensions rather than an exponentially large single state enum. At minimum consider:

- **Authority state:** `proposed`, `accepted_current`, `challenged`, `superseded`, `retired`.
- **Validity state:** `unassessed`, `valid`, `review_required`, `invalid`, plus existing risk-accepted/provisional semantics where dependent on unresolved human-overridden challenge.
- **Evidence state:** `pending`, `admissible`, `inconclusive`, `challenged`, `stale`, `rejected`, `retired`.
- **Obligation state:** `pending`, `ready`, `running`, `blocked`, `completed`, `failed`, `cancelled`, `human_required`.
- **Work/run state:** finite states sufficient for issue, execution, review, blocking, acceptance, closure, retry, and stale result handling.

Exact states require D3/D4 design and must preserve current Protocol semantics rather than forcing all semantic nuance into one workflow stage.

## 12. Event-sourced deterministic control kernel

### 12.1 Version-bound replay

Canonical machine workflow history SHALL use immutable accepted events or an equivalently replayable append-only model. The required deterministic property is:

```text
(protocol semantic version,
 control-schema version,
 transition/reducer ruleset version,
 initial/genesis state,
 ordered accepted events)
 -> exactly one resulting control state
```

Each accepted event retains sufficient provenance, including event identity/order, event type, subject/task/run identity, source state revision, actor/agent/human provenance, governing transition/action rule, causal accepted result/decision, and resulting state revision.

Historical accepted events SHALL NOT be silently reinterpreted through whatever reducer happens to be latest. When reducer/schema/control semantics evolve:

- preserve compatibility with the historical ruleset where practical; or
- perform an explicit, reviewable migration producing a new versioned genesis/snapshot/event lineage while preserving the old immutable history; or
- use another deterministic migration mechanism with equivalent auditability.

Migration must distinguish mechanical schema evolution from semantic reinterpretation. A migration cannot silently turn an old ambiguous/blocked result into a new PASS.

### 12.2 Reducer purity and the observation boundary

Canonical state reduction SHALL be deterministic from version-bound accepted inputs. The reducer MUST NOT determine historical transition results by querying ambient mutable state such as current wall-clock time, live filesystem contents, current Git branch/remote state, present network availability, current quota/account/resource meters, current process state, random-number generation, an LLM or other nondeterministic semantic evaluator, or mutable external service state.

When such information can affect control, acquire it outside the reducer and represent the relevant fact as a typed, provenance-bearing accepted observation/event before reduction:

```text
clock/lease condition
 -> recorded timer/expiry observation
 -> reducer applies transition rule

remote Git condition
 -> recorded fetch/ref/candidate observation
 -> reducer applies reconciliation rule

resource/quota condition
 -> Scheduler/meter observation or admission result
 -> reducer records execution readiness/blocking consequence

agent/human semantic judgment
 -> typed assessment/decision with provenance
 -> reducer validates and propagates legal consequence
```

Event timestamps may be retained for provenance and deterministic rule inputs, but replay SHALL use the recorded event data/ruleset rather than asking "what time is it now?" to reinterpret old history. If ordering depends on time, define deterministic ordering/tie semantics in the control contract.

### 12.3 Derived state and snapshots

Current state, graph indexes, ready-action queues and similar projections may be materialized for efficiency but remain derived/rebuildable. A control-state snapshot/checkpoint may accelerate startup/replay, but it SHALL identify protocol/control/ruleset versions, the last included accepted event/sequence, integrity identity sufficient to detect mismatched history, and derived-state schema version. A snapshot is not an independent authority. If it disagrees with the canonical event lineage, treat that as corruption/integrity failure and rebuild or repair rather than choosing whichever state is convenient.

## 13. Validation layers and single canonical writer

Only the orchestrator's authoritative reducer may commit canonical Protocol 8 workflow transitions. Before accepting an agent/human/system result, perform at least:

1. **schema validation** — structurally legal record;
2. **referential/revision validation** — referenced IDs/revisions/task binding exist and match;
3. **semantic graph validation** — edge/state combination is permitted and no prohibited authority cycle/ownership conflict is introduced;
4. **transition validation** — action is legal from current state and required preconditions/gates/evidence are satisfied;
5. **concurrency/staleness validation** — result still applies to the expected state/run/attempt;
6. **atomic event commitment** — no partial canonical mutation;
7. **derived impact/obligation update**.

The single-writer rule applies to every external actor:

- agent output is a proposal/assessment/evidence input and may not directly mutate canonical control authority;
- human input is an authenticated decision/ratification/override input;
- system/tool observations are typed observations;
- only the reducer commits the resulting canonical transition/event.

A human may have semantic authority to decide a claim, but the machine workflow state representing that decision is still committed through the canonical reducer so event ordering, provenance, replay and dependency propagation remain coherent. This does not subordinate human scientific authority to the orchestrator; it separates **who is authorized to decide meaning** from **who serializes workflow state**.

## 14. External effects are not reducer mutations

Launching an agent, creating/pushing a branch, sending a control response, invoking a tool, reserving a resource, or writing outside the canonical event transaction is an **external effect**. The architecture SHALL prevent a crash between canonical state mutation and an external effect from producing unbounded duplicate/phantom executions. Use the minimum justified pattern that establishes these semantics:

1. persist a deterministic intent/obligation with stable idempotency identity before or atomically with effect eligibility;
2. perform the external effect through an idempotent/reconcilable adapter boundary;
3. record the observed effect outcome as a new accepted event;
4. on ambiguous crash/restart, reconcile actual external state before retrying rather than assuming success or failure.

This does not mandate a specific "outbox" framework or distributed transaction system; it mandates the behavior. An external effect SHALL NOT be considered completed merely because the reducer intended it, and the reducer SHALL NOT perform nondeterministic I/O during historical replay.

## 15. Canonical control store, durability and recovery

### 15.1 Canonical store versus transport artifacts

Protocol 8 SHALL distinguish **canonical control persistence** from **transport artifacts**. Default architectural requirement, preserving the existing private-state boundary:

- canonical event history, current control state, leases, scheduler/account telemetry and private coordination data live in the orchestrator's governed user-local/private state root outside target/project repositories;
- project repositories contain semantic artifacts and only bounded transport/control artifacts when required for a transport such as web-agent Git handoff;
- secrets and private account/resource telemetry never enter project/run branches merely because TaskEnvelope/ResultEnvelope uses Git transport.

A project MAY deliberately persist selected non-secret control state in-repository only if a later D3 authority explicitly adopts that storage/trust model and resolves concurrency, privacy, history and ownership consequences. It is not the default. This separation prevents the lightweight control plane from becoming a large committed project data stream.

### 15.2 Durability and recovery contract

Because Protocol 8 makes the control plane mandatory, its canonical event history is operationally critical. The D3 architecture SHALL define, proportionately to the deployment model:

- transactional/atomic accepted-event publication boundary;
- corruption detection and recovery behavior;
- durable flush/commit semantics sufficient for the claimed crash model;
- backup/export and restore/import path for canonical non-secret control history;
- project/repository identity mapping needed to recover state after moving/recreating a local worktree;
- compatibility checks preventing restore under an incompatible reducer/schema/protocol without explicit migration;
- retention policy for transport-only and derived data distinct from canonical accepted history.

Do not require a network database or distributed consensus for a single-user/local orchestrator unless deployment requirements justify it. SQLite or another small transactional store may be sufficient; the requirement is recoverable deterministic authority, not infrastructure size. Derived state/indexes may be discarded and rebuilt. Loss of canonical accepted history must not be silently papered over by reconstructing workflow authority from workplan prose or Git directory placement.

## 16. Formal action registry

Define a finite, versioned action vocabulary. Candidate action families include:

- review/challenge/revise authority;
- review/revise/revalidate/retire concretization;
- run/revalidate/retire evidence specification or regenerate evidence;
- update semantic documentation/history;
- open/reopen/close bounded work obligations;
- request human ratification/decision;
- route to D1/D2/D3/D4/support specialist;
- retry/reconcile stale or failed execution where policy permits.

Each action definition must specify allowed source states, required input references, permitted execution capability/role, required evidence/gates, allowed result classifications, and deterministic consequences or next-obligation derivation.

Do not encode scientific truth as an action-table lookup. Semantic judgments enter the control plane only as typed observations/assessments with provenance and appropriate ratification.

## 17. Agent boundary: stochastic reasoning, deterministic interface

> Agents reason; schemas communicate; evidence supports/challenges; rules govern; the orchestrator transitions.

Agents may use exploratory, stochastic, abductive, falsification-oriented reasoning over semantic documents/code. At the control boundary they must produce schema-valid bounded outputs. The orchestrator SHALL NOT parse prose reports to infer canonical transition state when a formal field exists. Conversely the schema SHALL NOT attempt to encode the agent's entire reasoning trace; detailed findings/rationale remain referenced semantic reports where needed.

## 18. Immutable TaskEnvelope and ResultEnvelope

Define one logical SSDP agent protocol shared by local and web/manual transports.

### 18.1 TaskEnvelope

Task records are immutable after issue and include only control-critical data/references such as task/run/attempt IDs; protocol/control schema versions; base control-state revision; base repository commit/branch/worktree where relevant; requested action/stage/domain capability; subject IDs/revisions; governing/relevant semantic artifact references; required checks/evidence classes; allowed result classifications; human gates/constraints visible to execution; and the expected ResultEnvelope schema and writeback destination.

### 18.2 ResultEnvelope

Result records bind to the exact task identity/digest/state revision and may carry execution status; a bounded agent assessment such as `PASS_RECOMMENDED`, `NO_PASS_RECOMMENDED`, `HUMAN_REVIEW_REQUIRED`, `UPWARD_CHALLENGE_REQUIRED`; typed findings with severity/owner/evidence/report references; proposed actions; produced commit/artifact/evidence references; unresolved blockers/human-gate request; and execution provenance needed for deterministic acceptance. Detailed reasoning belongs in referenced review/workplan/history/qualification artifacts rather than large JSON prose fields.

### 18.3 Candidate identity without self-reference

A ResultEnvelope committed together with its own result file cannot require its own enclosing Git commit SHA as a pre-existing field. Protocol 8 SHALL define candidate/result identity so publication is realizable. Acceptable patterns include, depending on D3 design:

- ResultEnvelope binds to the task/base state and identifies the **semantic candidate parent commit**, while the enclosing later commit adds only the result/transport record;
- ResultEnvelope is stored outside the semantic candidate commit and the orchestrator records the publication commit after ingestion;
- another equivalent two-phase identity model with explicit semantics.

Do not require a file to contain the hash of the commit that cannot exist until after that file is committed. This follows the existing distinction between a semantic candidate and later evidence/lifecycle-only commits.

### 18.4 Transport artifacts are not semantic repository content

For Git/web execution, TaskEnvelope and ResultEnvelope files on an isolated run branch are **transport records**. They SHALL NOT be merged automatically into the project's canonical semantic branch merely because the agent's implementation commit is accepted:

```text
run branch
  -> validate Task/Result binding and candidate lineage
  -> ingest accepted ResultEnvelope/control facts into canonical control store
  -> integrate only the intended semantic/product commits/artifacts
  -> retire/delete/archive the transport branch according to policy
```

Preserve a durable control/audit reference to the accepted remote commit/result as required, but do not pollute project history with every ephemeral TaskEnvelope unless project policy explicitly chooses that representation.

Agents SHALL NOT modify the issued TaskEnvelope. They also SHALL NOT gain authority to modify canonical schemas, reducer policy, event history or control rules merely because those files are visible in a repository checkout; such changes require their own explicitly authorized Protocol task. Result validation must detect unauthorized modification of protected task/control surfaces.

## 19. Agent PASS is not canonical PASS

Protocol 8 enforces the privilege boundary between assessment and workflow transition:

```text
canonical PASS/closure
 = valid applicable agent assessment
   AND no unresolved blocking finding
   AND no active governing Serious Challenge without permitted qualified continuation
   AND required impact closure resolved
   AND required evidence admissible/executed
   AND required human gates satisfied
   AND result state/task revision current
   AND all governing Protocol acceptance conditions satisfied
```

The reducer determines whether the transition is legal. An agent cannot close work simply by writing `PASS` into a file.

## 20. Human gates and Serious Challenge preservation

Represent pending/accepted/rejected human state formally, preserving existing semantics:

- designated human adjudication is required where Protocol authority assigns it;
- agents/orchestrator may request a gate but may not synthesize successful human ratification;
- risk override permits bounded continuation only and does not resolve the epistemic claim;
- dependent descendants preserve risk-accepted/provisional state and cannot emit an unqualified closure;
- Serious Challenge must remain prominent and block dependent ordinary closure until resolved or explicitly risk-overridden where permitted.

The deterministic control plane governs propagation/status, not truth creation. Known Protocol 7 constraints on this surface are recorded in §37.2.

## 21. Deterministic dependency impact and obligation generation

Once a semantic classification/authority change has been accepted, downstream control consequences should be deterministic where rules are well-defined:

```text
accepted upstream semantic change
 -> traverse materially relevant typed dependencies
 -> preserve unaffected siblings/evidence
 -> mark affected descendants/evidence review_required/stale
 -> create bounded obligations
 -> schedule ready obligations
```

Do not infer semantic materiality solely from a text diff. Classification of editorial vs contract-preserving vs authority-changing edits may require agent/human semantic judgment. Once ratified as a typed fact, its control consequences must not depend on another LLM rereading prose to decide what to do. Missing graph edges follow §9's completeness rule.

## 22. Workplans, skills and semantic documents after cutover

Protocol 8 does not remove workplans or skills; it narrows their responsibilities.

- **Workplans** remain semantic engineering/change plans carrying problem statement, intended transformation, governing constraints, cycle-scoped decisions, delegated space, rationale, non-goals, affected semantic surfaces, acceptance reasoning, and reopen triggers. They cease to be canonical stores for machine lifecycle state, run assignment, retry count, readiness, PASS/NO-PASS control, or next-stage routing.
- **Skills** remain epistemic/domain execution procedures for D1-D4 and specialists. They teach how to investigate, design, challenge, implement, verify, and report. They cease to independently own workflow transitions already represented by the Protocol 8 control model.
- **Historical/evidence/review documents** remain substantive semantic artifacts. Control records bind to/reference them rather than replacing their reasoning.

**Lifecycle metadata migration.** Existing templates/frontmatter contain lifecycle fields such as `status` and filesystem placement such as `workplans/active`. At cutover the protocol SHALL choose one coherent compatibility strategy: remove canonical lifecycle fields from new Protocol 8 semantic workplans, or retain them only as **derived/advisory human-readable projections** generated from the control state and clearly non-authoritative. Do not permit manually edited `status: completed` or directory movement to enact a Protocol 8 transition. A `workplans/active` versus `archive` convention may remain temporarily for compatibility or generated human navigation, but after cutover it must not be a second canonical lifecycle authority. Any generated current-state annotation must be reproducible from the control plane and cannot become a second independent writer. Historical pre-cutover workplans remain immutable under their original lifecycle semantics; do not rewrite their metadata to look like Protocol 8.

## 23. Activation prompt minimization and bootstrap discoverability

Protocol 8 SHOULD reduce interactive web activation toward a generic bootstrap such as:

```text
Execute SSDP run <run-id>.
```

The task envelope, not the prompt, identifies action, protocol version, required capability/skill, repository state, semantic artifacts, and expected output contract. Preserve compatible installed-skill-first / immutable repository fallback resolution as a capability-resolution rule, but move task-specific routing/control data out of verbose activation prompts. The bootstrap must truthfully fail/non-close if compatible protocol material cannot be resolved; do not execute from model memory as though the required skill were loaded.

The minimized prompt is valid only if the agent can deterministically locate the immutable TaskEnvelope. Given the activation information, a competent compatible agent must be able to resolve without guessing: repository identity/remote when not already fixed by harness context; run branch/ref; task path or standardized run-ID-to-task-path convention; governing Protocol/control version source; and the required skill/capability resolution route. If `Execute SSDP run <run-id>` suffices because repository/ref/path are already bound by the environment, keep it that small. If not, the bootstrap includes the minimum missing locator information; do not re-expand it with task semantics that belong in the TaskEnvelope.

## 24. One logical agent protocol, multiple transport adapters

Local and web agents SHALL use the same TaskEnvelope/ResultEnvelope semantics. Transport differences must not create separate workflow protocols.

- **Local transport.** The orchestrator may create an isolated worktree/branch/run directory, invoke the configured local harness, observe an atomic/committed ResultEnvelope, validate, reduce, and continue without human workflow mediation.
- **Web/manual Git transport.**
  1. the orchestrator creates an isolated run branch from a known base;
  2. writes the immutable task envelope and required bootstrap references;
  3. pushes the run branch;
  4. a human performs the minimal unavoidable interactive activation unless a supported direct API/adapter exists;
  5. the web agent reads the task/protocol/semantic artifacts, performs work, and commits product/semantic artifacts plus ResultEnvelope to that branch;
  6. the orchestrator periodically `git fetch`es/inspects the specific run branch rather than blindly pulling into its active worktree;
  7. validates exact expected result path/task binding/base revision/commit lineage;
  8. accepts/rejects/retries/reconciles deterministically.

Git is transport/persistence/revision identity, not SSDP workflow semantics.

**Polling first.** Initial remote/web completion detection SHOULD use simple periodic fetch/polling when sufficient. Do not make the first release depend on webhook server infrastructure, external message brokers, distributed queues, or always-on network control services. A later transport may use webhooks/events without changing agent/control semantics if operational evidence justifies it.

## 25. Isolated runs, atomic publication, concurrency and stale-result protection

Every mutating orchestrator-controlled run must have an unambiguous execution identity and repository isolation consistent with current worktree-safety doctrine. Result acceptance must protect against old attempts arriving after retry/reassignment; concurrent agents acting on the same stale state; duplicate result publication; partial/half-written local results; remote branch commits unrelated to the expected run; repository base divergence/conflict; and ambiguous execution start/retry.

Use task digest/base-state revision/run/attempt or lease identity and base commit as appropriate. Require atomic publication via Git commit or validated temporary-write + atomic rename for local files. A stale result is evidence/history, not authority to overwrite current state. Policy may reject, revalidate, or create a new obligation; it must not silently commit.

## 26. Security and trust boundaries

The new control plane creates a stronger privilege boundary. At minimum:

- only trusted orchestrator/reducer code writes canonical control state/events;
- agent branches/results are untrusted proposals until validation;
- malformed or adversarial ResultEnvelope content cannot inject arbitrary actions/state transitions;
- file/artifact references remain repository-contained/explicitly governed;
- secrets/private account telemetry remain outside project repositories unless a governed contract explicitly requires otherwise (§15.1);
- web/manual remote execution cannot grant broader repository authority than its isolated branch/task requires;
- human decisions are authenticated through the applicable local/project trust boundary;
- control-plane corruption/replay/rollback behavior is explicitly handled.

Do not overclaim cryptographic guarantees not actually implemented.

## 27. Failure semantics, degraded operation and manual work

Because Protocol 8 makes the orchestrator mandatory for current workflow control, the old "manual operation is independently complete" invariant no longer applies to **Protocol 8 canonical execution**. Failure must remain truthful and recoverable:

- unavailable orchestrator/control store => Protocol 8 workflow cannot make canonical transitions; report blocked/unavailable rather than silently falling back to document control;
- agent/harness/remote transport failure => retain task/control state and retry/failover according to policy without counterfeit completion;
- corrupted/inconsistent event/state projection => stop mutation, rebuild/verify from canonical history where possible, otherwise require repair/human intervention;
- loss of a derived index does not force fallback to document-controlled workflow authority;
- fallback to the pre-cutover baseline is a **version rollback**, not simultaneous dual authority (§28).

Protocol 8 removes **independently complete manual document control**, not the ability for a human to invoke or supervise an agent manually. A manually activated web/local agent may read the TaskEnvelope and semantic artifacts, perform authorized reasoning/implementation/review, write the ResultEnvelope and semantic changes, and request human intervention. Without successful orchestrator ingestion/reduction, that work has not advanced canonical Protocol 8 workflow state. Exploratory/report-only scientific or engineering work may likewise occur while the orchestrator is unavailable, but it cannot claim Protocol 8 canonical lifecycle completion until represented and accepted through the control plane.

## 28. Pre-cutover baseline, rollback and cutover quiescence

### 28.1 Pre-cutover baseline and historical rollbacks

Current release identities are owned only by `PROTOCOL-RELEASE-STATE.yaml`; the values below record what this handoff was reconciled against and are re-resolved there before use.

```text
PRE-CUTOVER DOCUMENT-CONTROLLED BASELINE: Protocol 6.6
  recovery        384666764da4c55b282e6b1595ab97e2f86e1dc4
  public fallback 22f4bdba53795da3a6f13f162529f3a843fc37ae (distinct from recovery)
HISTORICAL, FOR EXPLICITLY VERSION-BOUND WORK ONLY:
  6.5 recovery c4d5da1e0acb0e9f27376bf69561e8762747cd2d / public 7f7b5e24858e813e45ace867a7f8ea5180f43bf0
  6.4 recovery 74bc572ef516cae417437a2027eeff52a2e25c15 / public e09a9d1480211eea2d16d722182bb5c6de1bee12
  6.3 recovery 9f353097fab36e325a325f1c2f9d9cec32e86177 / public 86c13cab6bdd1991dffa94e277db8eacf87e2e11
  6.2 recovery b59adc77efe6951912cfd705cc43830c58ca27d0 / public 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
  6.1 recovery 802e75af261efb4f70d71284d860613a2197b639 / public 47e9155632c44493644b0b02fa1fa625703cf480
```

Each later accepted protocol version advances the baseline only through an explicit inheritance reconciliation of this workplan (§37.3). Public fallback and recovery stay distinct; recovery identity is never substituted for public source, and later source-resolution or migration machinery must preserve that distinction.

### 28.2 Rollback and no dual-current control

During Protocol 8 development, preserve the pre-cutover baseline's immutable snapshot. If Protocol 8 is unsafe before/after early cutover:

1. stop Protocol 8 orchestrator mutation;
2. restore/check out the pinned pre-cutover baseline release and compatible profile/tooling;
3. resume its document-controlled workflow there;
4. repair Protocol 8 separately.

Do not allow live baseline workplan status and Protocol 8 control state to both claim canonical workflow authority over the same current run. Shadow comparison before cutover is permitted because only one side is authoritative.

### 28.3 Cutover quiescence and in-flight work

Before Protocol 8 canonical cutover, every active task/workplan/run within the migration scope that is governed by the pre-cutover baseline (or bound to an older version) SHALL be placed in exactly one category:

1. **drained** — finish/close under its pinned authority before cutover;
2. **remain pinned** — intentionally continue only in an isolated release/workspace of its governing version with no Protocol 8 authority over the same run;
3. **explicitly migrated to 8.0** — reconcile the governing semantic snapshot, outstanding obligations, evidence validity, Serious Challenges/human gates and current candidate; then create a Protocol 8 genesis/import event or equivalent typed migration record.

Never infer a Protocol 8 canonical state merely by scraping `status:` text or `workplans/active` placement from an in-flight document-controlled artifact. A migrated task's old document lifecycle fields become historical/provenance input; the Protocol 8 reducer owns the newly established current control state after the explicit migration boundary. Cutover acceptance SHALL include an inventory proving that no in-scope run is simultaneously live under both authorities.

## 29. Migration phases

- **Phase A — complete and freeze the pre-cutover baseline.** Canonical-control cutover does not begin until the baseline is completed, behaviorally qualified and has an immutable recovery identity. Satisfied for Protocol 6.6 (§28.1); if Protocol 7 is accepted first, satisfied for it only through its inheritance reconciliation (§37.3).
- **Phase B — deliberate D3 reassessment and redesign.** Reopen/supersede the affected orchestrator architecture (§3), including the Protocol 6.6 reassessment input. Define control-plane ownership, schemas, typed graph semantics, event/state model, action registry, privilege boundaries and migration topology, and close every §30 obligation before implementation.
- **Phase C — deterministic kernel.** Implement schema/reference/semantic/transition/staleness validation, reducer, event history, derived state, graph/index, obligation calculation, and deterministic replay/recovery.
- **Phase D — agent contract/transports.** Implement immutable TaskEnvelope/ResultEnvelope, local execution adapter, isolated Git/web transport, polling, idempotency, concurrency and stale-result handling.
- **Phase E — shadow orchestration under baseline authority.** Keep the baseline document workflow canonical while Protocol 8 computes non-authoritative expected state/transitions from the same observed work. Compare at least stage/domain routing; blocker/Serious-Challenge propagation; evidence invalidation/admissibility; workplan reopen/closure; human gates/risk override; stale-result behavior; next obligation/action. Classify each difference as a Protocol 8 defect, a baseline ambiguity/defect, a deliberate stronger rule, or a genuinely unresolved semantic judgment. Do not force equality when Protocol 8 intentionally improves the semantics, but document and independently review every material difference.
- **Phase F — adversarial qualification and fault injection** (§31, §32) before cutover.
- **Phase G — cutover.** Only after accepted D3 architecture, implementation acceptance, shadow qualification, independent Review, and required human/project approval: make Protocol 8 control state canonical; remove duplicate workflow-control duties from current skills/workplans/prompts; keep semantic documents intact; make orchestrator participation mandatory for Protocol 8 current workflow; retain the baseline only as immutable rollback/recovery version.

## 30. D3 design obligations

The Protocol 8 D3 architecture SHALL explicitly decide and document, and cannot close until it does:

1. canonical ownership and persistence location of reducer, event history, derived state, graph/index, obligations, leases, scheduler state, and transport metadata;
2. the reducer/Scheduler/Adapter/Core/Tracker responsibility split and dependency direction (§4);
3. canonical versus derived versus transport-only data classifications;
4. semantic-owner/control-projection consistency handling (§5.4);
5. event/reducer/schema versioning and migration/replay semantics (§12.1);
6. in-flight pre-cutover cutover/migration behavior (§28.3);
7. protected control surfaces agents may read but not mutate (§18.4);
8. semantic-candidate versus result-publication commit identity (§18.3);
9. run-branch retirement/integration policy (§18.4);
10. graph completeness/unknown-dependency behavior (§9);
11. authenticated human-decision ingestion (§13);
12. bootstrap locator contract for zero-context web execution (§23);
13. the observation/effect/reducer boundary (§12.2, §14);
14. a recoverable canonical persistence model (§15.2);
15. the §3.2 minimum-justified-architecture reassessment against Protocol 6.6 evidence, and any Protocol 7 inputs bound by §37.2.

Do not defer these as incidental D4 implementation details because they define the control/trust architecture.

## 31. Required deterministic/failure qualification

At minimum test:

- deterministic replay from canonical event history under the declared reducer/schema/ruleset version;
- replay stability across at least one schema/ruleset evolution or a controlled compatibility fixture;
- replay produces identical state even when wall-clock time and live external state differ from the original execution environment;
- lease/timer expiry driven by recorded control observations rather than ambient replay time;
- restart/crash recovery at event/state publication boundaries;
- crash after effect intent but before external start reconciles without duplicate execution;
- crash after external start but before outcome recording reconciles the ambiguous start before retry;
- historical Scheduler decisions are not recomputed from current resource state during replay;
- Scheduler cannot enact semantic workflow transitions and remains subordinate to reducer readiness;
- malformed/unknown-schema agent output;
- unknown required action/state semantics fail explicitly rather than being ignored;
- illegal transition proposals;
- task/result digest mismatch;
- an agent-modified TaskEnvelope/protected control file is rejected;
- ResultEnvelope publication avoids Git self-reference and preserves semantic candidate identity;
- stale state revision/old attempt/expired lease result;
- duplicate/idempotent result ingestion;
- concurrent local/remote agents;
- remote branch divergence/unrelated commit;
- partial local result publication;
- unavailable Git remote/network;
- interrupted local harness;
- agent execution failure/cancellation;
- unavailable/mismatched skill/protocol source;
- zero-context web activation locates the correct immutable task using only the declared bootstrap contract;
- canonical control/private state does not leak into a project repository by default;
- accepted semantic changes can be integrated without merging ephemeral TaskEnvelope/ResultEnvelope transport files;
- Serious Challenge and human gate propagation;
- authenticated human decision enters through the reducer while retaining human semantic authority;
- risk-accepted/provisional descendant behavior;
- stale passing evidence rejection;
- bounded graph invalidation preserving unaffected siblings;
- partial graph coverage cannot be interpreted as proven independence;
- a semantic artifact/control-projection mismatch blocks rather than allowing JSON to silently redefine semantic authority;
- graph/index rebuild from canonical history;
- derived-state/snapshot corruption is detected and rebuilds from canonical history;
- loss of a derived index does not force fallback to document-controlled workflow authority;
- canonical event-history export/restore reproduces the same state under the compatible ruleset;
- incompatible restore/replay is blocked pending explicit migration rather than silently reinterpreted;
- manually editing a Protocol 8 workplan `status` cannot transition canonical state;
- an in-flight baseline task is drained, pinned, or explicitly migrated without dual authority;
- rollback to the immutable pre-cutover baseline.

## 32. Required semantic/adversarial qualification

Protocol 8 must additionally prove that automation preserves Protocol semantics rather than only state-machine mechanics. Scenarios must include:

- a D4 defect remains D4 when upstream authority is coherent;
- a downstream observation can challenge D3/D2/D1 and blocks dependent closure appropriately;
- the orchestrator does not auto-resolve scientific ambiguity;
- changed authority invalidates only materially dependent descendants/evidence;
- an evidence specification may survive concretization replacement while prior realization becomes stale/remapped;
- proxy evidence cannot close the real semantic owner;
- a missing required check cannot be converted into PASS by reducer policy;
- human risk override remains non-epistemic and visibly provisional downstream;
- local and web transports produce equivalent logical control outcomes for the same accepted ResultEnvelope;
- verbose/alternative agent prose cannot alter control outcome when structured fields are identical;
- workplan/document wording no longer secretly overrides formal lifecycle state;
- semantic historical reasoning remains accessible and referenced after control-plane cutover;
- minimum justified control machinery is maintained and no duplicate second authority emerges;
- when Protocol 7 is inherited, the §37.2 inputs hold: gate-evidence adequacy is not reduced to a presence predicate, and marked product-surface acceptance is never self-accepted or inferred from technical D3 Review.

## 33. Versioning and historical preservation

Protocol 8 major-version implementation must update protocol versioning/compatibility documentation so that:

- work bound to any earlier protocol version (5.16, 6.x, and 7.x once it exists) remains governed by that version and resolves through its immutable profile/snapshot;
- Protocol 8 work uses the new control schema/profile/architecture intentionally;
- historical 5.16, 6.x and 7.x truth remains immutable/version-bound, and every older supported orchestrator profile remains frozen and independently testable;
- the control schema version, orchestrator API/SPI version, profile version and Protocol semantic version are not silently conflated;
- migration tools, if any, never reinterpret old semantic records as though they had been authored under Protocol 8.

## 34. Acceptance criteria

Protocol 8.0 cannot cut over or PASS until all of the following hold:

1. the pre-cutover baseline is completed, qualified and immutably recoverable (§28.1);
2. the affected frozen orchestrator D3 architecture has been deliberately reopened and reassessed (§3.2), independently reviewed, and superseded by a coherent Protocol 8 architecture rather than patched around; the new D3 Architecture Manual resolves every §30 obligation;
3. the new architecture has exactly one canonical workflow-control writer/owner and no contradictory document/Tracker/profile/reducer authority; reducer and Scheduler ownership are unambiguous and no resource-routing module is a second workflow reducer;
4. a versioned formal control data contract exists and is syntactically/semantically validated; unsupported transition-critical schema/action semantics fail explicitly;
5. semantic artifacts remain authoritative carriers of substantive reasoning and are referenced rather than duplicated into control JSON; semantic authority and machine control projection have an explicit consistency/error rule;
6. logical identity/revision and typed dependency/evidence relations support bounded deterministic impact closure; graph incompleteness cannot silently suppress required impact invalidation;
7. evidence specification/realization/observation/admissibility semantics preserve the baseline's behavior;
8. immutable TaskEnvelope and bound ResultEnvelope contracts are implemented; candidate/result publication has a non-self-referential identity contract;
9. agent assessment is separated from canonical transition authority; human decisions are serialized through the single canonical reducer without transferring semantic authority to it;
10. deterministic event replay produces exactly the same state for the same accepted history, bound to explicit reducer/schema/ruleset versions and migration behavior; reducer behavior is independent of ambient mutable state during replay, and every transition-affecting nondeterministic/external fact crosses a typed observation/event boundary;
11. stale/concurrent/duplicate/partial result behavior is deterministic and tested; effect execution is idempotent or reconcilable across crash/retry boundaries;
12. Serious Challenge, human gates and risk-accepted/provisional semantics cannot be bypassed by automation;
13. local transport runs fully automatically through the common logical agent protocol where configured;
14. web/manual Git transport uses the same logical protocol and validates isolated remote writeback without unsafe pull/mutation of the active orchestrator worktree; web/manual bootstrap is deterministically discoverable without hidden conversation state;
15. polling-first remote completion works without requiring unjustified server/message-broker infrastructure;
16. mandatory orchestrator failure produces truthful Protocol 8 non-closure rather than implicit document-control fallback;
17. canonical control persistence and Git transport persistence are separated, with private state outside target repositories by default; ephemeral run Task/Result artifacts are not automatically merged into semantic project history; canonical history has a tested backup/export and compatible restore path; project/worktree relocation does not silently orphan or alias control authority;
18. all in-scope in-flight baseline work has been drained, pinned or explicitly migrated with no dual-current run; Protocol 8 workplan lifecycle metadata cannot independently transition canonical state;
19. shadow-mode comparison has explained all material baseline/Protocol 8 differences;
20. deterministic/failure, replay/recovery and semantic/adversarial qualification execute and pass;
21. repository/build/package/profile/orchestrator affected regression/integration checks execute and pass;
22. independent final Review/Challenge Pass finds no genuine blocker or active governing Serious Challenge;
23. cutover removes duplicate control duties from current Protocol 8 workplans/skills/prompts without deleting their semantic content;
24. rollback to the immutable pre-cutover baseline has been demonstrated.

## 35. Explicit non-goals

- Do not convert scientific/method/architecture/workplan/history/review documents into JSON content stores.
- Do not encode full agent reasoning or raw evidence in the control plane.
- Do not add a dedicated graph database without demonstrated need.
- Do not implement a monolithic combinatorial FSM when composed state dimensions are sufficient.
- Do not let Git branch/PR/commit state implicitly define SSDP workflow semantics.
- Do not let agents directly mutate canonical control state.
- Do not make the reducer decide scientific truth or replace human ratification.
- Do not retain the old document-controlled workflow as a simultaneously canonical Protocol 8 fallback.
- Do not layer the new control owner under contradictory frozen orchestrator 1.6.0 authority; explicitly redesign/supersede the affected D3 surface.
- Do not weaken inherited evidence/acceptance/Challenge safeguards for automation convenience.
- Do not add webhook/message-broker/distributed infrastructure before the simpler Git/polling transport is shown insufficient.
- Do not add registries, wrappers or machine fields solely to mirror inherited document-controlled doctrine (§2).

## 36. Final target

```text
semantic artifacts carry meaning;
agents investigate and reason;
evidence supports or challenges governed claims;
schemas communicate bounded control facts;
rules validate legal transitions;
the orchestrator alone commits workflow state.
```

The central deterministic contract is the version-bound replay property of §12.1. It is a deterministic **control** guarantee, not a claim that scientific reasoning is deterministic. Semantic judgment remains agent/human reasoning until accepted as a typed, provenance-bearing control fact; only then do deterministic consequences propagate.

## 37. Version identity, Protocol 7 inputs and lineage

### 37.1 Version rebind

The deterministic control-plane / mandatory-orchestrator revision was reassigned from Protocol 7.0 to Protocol 8.0 on 2026-09-27, because a more fundamental deficiency in scientific epistemic transparency, human-legible realized-data reporting, epistemic initiative and discovery feedback was assigned Protocol 7.0; deferring this design avoids two independent major doctrine changes colliding. The reassignment was a version/lifecycle change only: it did not accept, reject, implement, simplify or otherwise mutate the design. Every archived target-version statement that designates Protocol 7.0 for this family means Protocol 8.0. Any current routing/index artifact that calls this family "Protocol 7" is stale with respect to target-version identity and is reconciled without rewriting immutable historical release records. Tests and closeout checks select these artifacts by exact ID, never by `SSDP-7.0*` or `SSDP-8.0*` globs.

### 37.2 Known Protocol 7 inputs to the D3 reassessment

These are inputs, not Protocol 8 design decisions:

- Protocol 7's human-gate evidence contract is a semantic adequacy judgment. A deterministic control plane may represent gate state, but a machine-checkable presence predicate (for example "evidence artifact attached") cannot satisfy it. Protocol 8 must not reduce gate-evidence adequacy to such a predicate.
- Protocol 7 keeps realized-scientific-record and feedback-persistence state in existing project artifacts, not in control-plane state, and requires no orchestrator transition/control-semantics change.
- Protocol 7 (as proposed) requires product-scope acceptance of marked product inspectability surfaces at existing human/task gates. A control plane may represent that pending/accepted state but cannot self-accept it or infer it from technical D3 Review.

### 37.3 Inheritance reconciliations

If Protocol 7 is accepted, its closeout authors the Protocol 8 inheritance reconciliation of this workplan (Protocol 7 workplan, Stage H). That reconciliation advances the §28.1 pre-cutover baseline from Protocol 6.6 recovery to Protocol 7 recovery, binds Protocol 7 gate-evidence and RSR semantics as mandatory inputs to the §3 reassessment, selects no Protocol 8 architecture, authorizes no Protocol 8 D4, and recommends (never self-adopts) whether this family should adopt Protocol 7 as its governing `protocol_version` under the versioning owner's adoption sequence. Until then, the Protocol 6.6 baseline stands. Later accepted versions follow the same pattern.

### 37.4 Lineage (archived, byte-identical)

| Archived artifact (`workplans/archive/`) | Governed | Now carried in |
|---|---|---|
| `SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION.md` (6.1.0, 2026-09-09) | the parent design | §1-§36 |
| `…-REVISION-1-SECOND-REVIEW-CLOSURE.md` (6.1.0) | Scheduler/reducer ownership, semantic/control projection, canonical store, transport artifacts, candidate identity, version-bound replay, cutover quiescence, lifecycle metadata, human decisions through the writer, bootstrap locator, manual work, graph completeness, forward compatibility, D3 obligations, tests, criteria | §4, §5.4, §7, §9, §12.1, §13, §15.1, §18.3-§18.4, §22, §23, §27, §28.3, §30-§31, §34 |
| `…-REVISION-2-DETERMINISM-AND-RECOVERY-CLOSURE.md` (6.1.0) | reducer purity, external effects, durability/recovery, snapshots, Scheduler replay, tests, criteria | §4, §12.2-§12.3, §14, §15.2, §27, §30-§31, §34 |
| `…-REVISION-3-PROTOCOL-6.2-INHERITANCE-RECONCILIATION.md` (6.2.0) | 6.2 baseline and representation inheritance | §2, §28.1 |
| `…-REVISION-4-PROTOCOL-6.3-INHERITANCE-RECONCILIATION.md` (6.3.0) | 6.3 baseline and project-learning inheritance | §2, §28.1 |
| `…-REVISION-5-PROTOCOL-6.4-INHERITANCE-RECONCILIATION.md` (6.4.0) | 6.4 baseline identity | §28.1 |
| `…-REVISION-6-PROTOCOL-6.5-INHERITANCE-RECONCILIATION.md` (6.5.0) | 6.5 baseline identity | §28.1 |
| `…-REVISION-7-PROTOCOL-6.6-INHERITANCE-AND-D3-REASSESSMENT.md` (6.6.0) | 6.6 baseline and D3 reassessment input | §3.2, §28.1, §30 |
| `SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md` (6.6.0) | 7.0 → 8.0 reassignment, Protocol 7 inputs, stale-label rule | §0, §37 |

The archived Revision 3-7 records were version-bound to the protocol accepted when each was written; they keep that historical meaning and are not reinterpreted under 6.6. Their pre-D4 gate dispositions ("inheritance reconciliation: SATISFIED", "D3 reopen still required", "D4 not authorized") remain true and are summarized in §0.

## 38. Handoff state

```text
GOVERNING BASE: Protocol 6.6.0
TARGET: Protocol 8.0.0 — deterministic control plane / mandatory orchestrator
SINGLE CURRENT HANDOFF: this file (parent + Revisions 1-7 + version rebind archived byte-identically)
PRE-CUTOVER BASELINE: Protocol 6.6 recovery 384666764da4c55b282e6b1595ab97e2f86e1dc4; advances only by inheritance reconciliation
PROTOCOL 7 RELATION: independent proposed major revision; its closeout authors this workplan's inheritance reconciliation
DESIGN: proposed; second-review PASS history under 6.1 (parent + Revisions 1-2); not accepted-current
DELIBERATE D3 ORCHESTRATOR REASSESSMENT/SUPERSESSION: REQUIRED BEFORE D4
PROTOCOL 8 D4 IMPLEMENTATION: NOT AUTHORIZED
SERIOUS CHALLENGE: NONE
NEXT ACTION: independent losslessness check of this consolidation against the archived family,
  then the deliberate D3 reassessment
```
