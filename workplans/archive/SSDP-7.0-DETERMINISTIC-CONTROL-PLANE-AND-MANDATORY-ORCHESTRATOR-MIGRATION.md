---
kind: protocol-major-revision-workplan
workplan_id: SSDP-7.0-DETERMINISTIC-CONTROL-PLANE-AND-MANDATORY-ORCHESTRATOR-MIGRATION
protocol_version: 6.1.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-09
base_protocol: Protocol 6.1
active_serious_challenge: none
requires_completed_workplan: SSDP-6.1-EVIDENCE-EVOLUTION-AND-CONCRETIZATION-ALIGNMENT
---

# SSDP 7.0 Deterministic Control Plane and Mandatory Orchestrator Migration

## 1. Objective and breaking-version boundary

Protocol 7.0 changes workflow authority itself. It is therefore a major revision.

Protocol 6.1 remains the final document-controlled protocol. Protocol 7.0 moves machine workflow control into a lightweight formal control plane and makes the orchestrator a mandatory participant in the standard SSDP development cycle.

The transition must preserve, losslessly, all still-valid Protocol 6.1 scientific, numerical, architectural, implementation, evidence, challenge, historical, versioning, simplicity, validation, and qualification doctrine. Protocol 7.0 changes **how workflow state and transitions are controlled**, not where substantive engineering/scientific meaning lives.

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

Protocol 7.0 SHALL preserve every still-valid accepted Protocol 6.1 capability, including:

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
- behavioral qualification of governed decisions rather than wording.

Protocol 7 automation SHALL NOT weaken a substantive pass threshold, manufacture closure, or transform an epistemic judgment into a deterministic fact merely because machine control requires a finite state vocabulary.

## 3. Deliberate D3 orchestrator-architecture supersession

The currently frozen orchestrator architecture predates Protocol 7 and includes invariants that intentionally make manual operation first-class and prevent Tracker/Scheduler from becoming workflow authority. Protocol 7 changes those assumptions.

Therefore this workplan SHALL NOT implement the new control plane as a hidden layer beneath the existing frozen orchestrator Architecture 1.6.0.

Before implementation, Protocol 7 must reopen the affected D3 orchestrator authority and produce a new accepted Architecture Manual revision that explicitly supersedes incompatible current invariants, including as applicable:

- workplan/profile/result ownership of workflow routing/control;
- Tracker-as-evidence-only semantics where incompatible with the new canonical event/state store;
- manual operation as an independently complete standard execution mode;
- existing result-envelope semantics where they conflict with TaskEnvelope/ResultEnvelope authority boundaries;
- assumptions that Scheduler never participates in deterministic workflow transition selection;
- current module ownership boundaries if the new reducer/state/event/graph owner cannot fit coherently without violating dependency direction.

Preserve unrelated architectural guarantees unless independently invalidated, including progressive modularity where still admissible, strict dependency direction, graceful failure where compatible with mandatory control, one composition root, versioned public boundaries, explicit route identity, repository containment, private-state/security rules, idempotency, bounded concurrency, and no duplicated workflow authority.

Prefer alteration/reduction of the existing architecture over additive wrapper machinery. Do not retain contradictory old and new workflow owners behind adapters.

## 4. Plane separation

Protocol 7 SHALL explicitly separate three planes.

### 4.1 Semantic plane

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

### 4.2 Control plane

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

### 4.3 Execution plane

Contains orchestrator, agent harnesses, tools, local/remote transports, test runners, repository adapters, and other execution machinery.

Global invariant:

> The control plane is a lightweight deterministic coordination skeleton over the semantic repository. It indexes, relates, validates, and transitions semantic artifacts; it does not replace or reproduce them.

## 5. Minimal-sufficient-control-data doctrine

For each proposed control field ask:

> Does the deterministic controller need this value to select, validate, serialize, replay, or audit a legal transition?

If no, keep it in a referenced semantic artifact.

Control records SHOULD contain references plus bounded classifications, not essays, equations, source patches, full review reasoning, or large test logs.

Required anti-duplication rules:

1. control records SHALL reference semantic authority rather than duplicate it except for bounded transition-critical values;
2. semantic documents SHALL NOT remain canonical stores of machine workflow state after that state is migrated to Protocol 7;
3. raw evidence stays in native/referenced artifacts; control state records admissibility, subject/revision, observation class, and pointers needed for transition logic;
4. machine event history records control transitions; semantic historical documentation records why scientific/engineering meaning changed. Neither replaces the other.

## 6. Formal control data standard

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

Use JSON Schema or an equivalently rigorous validation mechanism for syntax and bounded enumerations. Schema versioning is independent of Protocol semantic versioning where justified; compatibility rules must be explicit.

Do not allow free-form prose values to substitute for fields the reducer must interpret deterministically.

## 7. Identity, revision, and semantic-reference model

Separate stable logical identity from semantic revision.

Conceptually:

```text
D2:target-size-objective
!=
D2:target-size-objective@<specific semantic revision>
```

Relationships/evidence whose meaning depends on a particular accepted revision must bind to that revision.

Artifact references must identify enough source state to avoid silent drift, using Git commit/path/section identity or another justified immutable identity. Additional hashing/manifest machinery is required only where Git/repository identity is insufficient.

Protocol 7 SHALL NOT invent a universal per-claim hash graph if bounded artifact/revision references establish the necessary control invariant more simply.

## 8. Typed authority/concretization and evidence graph

Migrate the material Protocol 6.1 dependency model into a formal typed graph sufficient for impact closure and orchestration.

Candidate edge semantics include:

- `CONCRETIZES`;
- `DERIVED_FROM`;
- `DEPENDS_ON`;
- `ASSUMES`;
- `CONSTRAINED_BY`;
- `SUPERSEDES` / `REPLACES`;
- `CHALLENGES` / `CONTRADICTS`;
- `EVIDENCES`;
- `GENERATED_BY`.

The schema must distinguish evidentiary target from execution dependency.

The graph is logically machine-authoritative for Protocol 7 control decisions only after cutover. Its physical storage may be relational tables, JSONL-derived indexes, SQLite, or another minimal adequate implementation. Do not require a dedicated graph database absent demonstrated need.

Derived graph/index stores must be reproducible from canonical accepted records/events and must not become independently edited parallel authority.

## 9. Evidence formalization without bulk-data migration

Formalize Protocol 6.1 evidence semantics while leaving substantive evidence in native artifacts.

Control metadata for an evidence realization should be sufficient to determine, when applicable:

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

## 10. Composed state model, not one monolithic FSM

Protocol 7 SHALL use bounded interacting state dimensions rather than an exponentially large single state enum.

At minimum consider:

### Authority state
`proposed`, `accepted_current`, `challenged`, `superseded`, `retired`.

### Validity state
`unassessed`, `valid`, `review_required`, `invalid`, plus existing risk-accepted/provisional semantics where dependent on unresolved human-overridden challenge.

### Evidence state
`pending`, `admissible`, `inconclusive`, `challenged`, `stale`, `rejected`, `retired`.

### Obligation state
`pending`, `ready`, `running`, `blocked`, `completed`, `failed`, `cancelled`, `human_required`.

### Work/run state
finite states sufficient for issue, execution, review, blocking, acceptance, closure, retry, and stale result handling.

Exact states require D3/D4 design and must preserve current Protocol semantics rather than forcing all semantic nuance into one workflow stage.

## 11. Event-sourced deterministic control kernel

Canonical machine workflow history SHALL use immutable accepted events or an equivalently replayable append-only model.

Required deterministic property:

```text
(protocol/control schema version,
 initial control state,
 ordered accepted events)
 -> exactly one resulting control state
```

Each accepted event must retain sufficient provenance, including:

- event identity/order;
- event type;
- subject/task/run identity;
- source state revision;
- actor/agent/human provenance;
- governing transition/action rule;
- causal accepted result/decision;
- resulting state revision.

Current state, graph indexes, ready-action queues, and similar projections may be materialized for efficiency but remain derived/rebuildable.

## 12. Validation layers and single canonical writer

Only the orchestrator's authoritative reducer may commit canonical Protocol 7 workflow transitions.

Before accepting an agent/human/system result, perform at least:

1. **schema validation** — structurally legal record;
2. **referential/revision validation** — referenced IDs/revisions/task binding exist and match;
3. **semantic graph validation** — edge/state combination is permitted and no prohibited authority cycle/ownership conflict is introduced;
4. **transition validation** — action is legal from current state and required preconditions/gates/evidence are satisfied;
5. **concurrency/staleness validation** — result still applies to the expected state/run/attempt;
6. **atomic event commitment** — no partial canonical mutation;
7. **derived impact/obligation update**.

Agent output may propose or assess. It may not directly mutate canonical control authority.

## 13. Formal action registry

Define a finite, versioned action vocabulary. Candidate action families include:

- review/challenge/revise authority;
- review/revise/revalidate/retire concretization;
- run/revalidate/retire evidence specification or regenerate evidence;
- update semantic documentation/history;
- open/reopen/close bounded work obligations;
- request human ratification/decision;
- route to D1/D2/D3/D4/support specialist;
- retry/reconcile stale or failed execution where policy permits.

Each action definition must specify:

- allowed source states;
- required input references;
- permitted execution capability/role;
- required evidence/gates;
- allowed result classifications;
- deterministic consequences or next-obligation derivation.

Do not encode scientific truth as an action-table lookup. Semantic judgments enter the control plane only as typed observations/assessments with provenance and appropriate ratification.

## 14. Agent boundary: stochastic reasoning, deterministic interface

Global architecture rule:

> Agents reason; schemas communicate; evidence supports/challenges; rules govern; the orchestrator transitions.

Agents may use exploratory, stochastic, abductive, falsification-oriented reasoning over semantic documents/code. At the control boundary they must produce schema-valid bounded outputs.

The orchestrator SHALL NOT parse prose reports to infer canonical transition state when a formal field exists.

Conversely the schema SHALL NOT attempt to encode the agent's entire reasoning trace. Detailed findings/rationale remain referenced semantic reports where needed.

## 15. Immutable TaskEnvelope and ResultEnvelope

Define one logical SSDP agent protocol shared by local and web/manual transports.

### 15.1 TaskEnvelope

Task records are immutable after issue and include only control-critical data/references such as:

- task/run/attempt IDs;
- protocol/control schema versions;
- base control-state revision;
- base repository commit/branch/worktree where relevant;
- requested action/stage/domain capability;
- subject IDs/revisions;
- governing/relevant semantic artifact references;
- required checks/evidence classes;
- allowed result classifications;
- human gates/constraints visible to execution;
- expected ResultEnvelope schema and writeback destination.

### 15.2 ResultEnvelope

Result records bind to the exact task identity/digest/state revision and may carry:

- execution status;
- bounded agent assessment such as `PASS_RECOMMENDED`, `NO_PASS_RECOMMENDED`, `HUMAN_REVIEW_REQUIRED`, `UPWARD_CHALLENGE_REQUIRED`;
- typed findings with severity/owner/evidence/report references;
- proposed actions;
- produced commit/artifact/evidence references;
- unresolved blockers/human-gate request;
- execution provenance needed for deterministic acceptance.

Detailed reasoning belongs in referenced review/workplan/history/qualification artifacts rather than large JSON prose fields.

## 16. Agent PASS is not canonical PASS

Protocol 7 must enforce the privilege boundary between assessment and workflow transition.

Conceptually:

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

## 17. Human gates and Serious Challenge preservation

Represent pending/accepted/rejected human state formally, preserving existing semantics:

- designated human adjudication is required where Protocol authority assigns it;
- agents/orchestrator may request a gate but may not synthesize successful human ratification;
- risk override permits bounded continuation only and does not resolve the epistemic claim;
- dependent descendants preserve risk-accepted/provisional state and cannot emit an unqualified closure;
- Serious Challenge must remain prominent and block dependent ordinary closure until resolved or explicitly risk-overridden where permitted.

The deterministic control plane governs propagation/status, not truth creation.

## 18. Deterministic dependency impact and obligation generation

Once a semantic classification/authority change has been accepted, downstream control consequences should be deterministic where rules are well-defined.

Example:

```text
accepted upstream semantic change
 -> traverse materially relevant typed dependencies
 -> preserve unaffected siblings/evidence
 -> mark affected descendants/evidence review_required/stale
 -> create bounded obligations
 -> schedule ready obligations
```

Do not infer semantic materiality solely from a text diff. Classification of editorial vs contract-preserving vs authority-changing edits may require agent/human semantic judgment. Once ratified as a typed fact, its control consequences must not depend on another LLM rereading prose to decide what to do.

## 19. Workplans, skills, and semantic documents after cutover

Protocol 7 does not remove workplans or skills; it narrows their responsibilities.

### Workplans

Remain semantic engineering/change plans carrying problem statement, intended transformation, governing constraints, cycle-scoped decisions, delegated space, rationale, non-goals, affected semantic surfaces, acceptance reasoning, and reopen triggers.

They cease to be canonical stores for machine lifecycle state, run assignment, retry count, readiness, PASS/NO-PASS control, or next-stage routing.

### Skills

Remain epistemic/domain execution procedures for D1-D4 and specialists. They teach how to investigate, design, challenge, implement, verify, and report. They cease to independently own workflow transitions already represented by the Protocol 7 control model.

### Historical/evidence/review documents

Remain substantive semantic artifacts. Control records bind to/reference them rather than replacing their reasoning.

A `workplans/active` versus `archive/completed` filesystem convention may remain temporarily for compatibility or generated human navigation, but after cutover it must not be a second canonical lifecycle authority.

## 20. Activation prompt minimization and capability resolution

Protocol 7 SHOULD reduce interactive web activation toward a generic bootstrap such as:

```text
Execute SSDP run <run-id>.
```

The task envelope, not the prompt, identifies action, protocol version, required capability/skill, repository state, semantic artifacts, and expected output contract.

Preserve compatible installed-skill-first / immutable repository fallback resolution as a capability-resolution rule, but move task-specific routing/control data out of verbose activation prompts.

The bootstrap must truthfully fail/non-close if compatible protocol material cannot be resolved; do not execute from model memory as though the required skill were loaded.

## 21. One logical agent protocol, multiple transport adapters

Local and web agents SHALL use the same TaskEnvelope/ResultEnvelope semantics. Transport differences must not create separate workflow protocols.

### 21.1 Local transport

The orchestrator may create an isolated worktree/branch/run directory, invoke the configured local harness, observe an atomic/committed ResultEnvelope, validate, reduce, and continue without human workflow mediation.

### 21.2 Web/manual Git transport

For a web agent:

1. orchestrator creates an isolated run branch from a known base;
2. writes the immutable task envelope and required bootstrap references;
3. pushes the run branch;
4. human performs the minimal unavoidable interactive activation unless a supported direct API/adapter exists;
5. web agent reads the task/protocol/semantic artifacts, performs work, commits product/semantic artifacts plus ResultEnvelope to that branch;
6. orchestrator periodically `git fetch`es/inspects the specific run branch rather than blindly pulling into its active worktree;
7. validates exact expected result path/task binding/base revision/commit lineage;
8. accepts/rejects/retries/reconciles deterministically.

Git is transport/persistence/revision identity, not SSDP workflow semantics.

## 22. Polling-first remote implementation

Initial remote/web completion detection SHOULD use simple periodic fetch/polling when sufficient.

Do not make first release depend on:

- webhook server infrastructure;
- external message brokers;
- distributed queues;
- always-on network control services.

A later transport may use webhooks/events without changing agent/control semantics if operational evidence justifies it.

## 23. Isolated runs, atomic publication, concurrency, and stale-result protection

Every mutating orchestrator-controlled run must have an unambiguous execution identity and repository isolation consistent with current worktree-safety doctrine.

Result acceptance must protect against:

- old attempts arriving after retry/reassignment;
- concurrent agents acting on the same stale state;
- duplicate result publication;
- partial/half-written local results;
- remote branch commits unrelated to the expected run;
- repository base divergence/conflict;
- ambiguous execution start/retry.

Use task digest/base-state revision/run/attempt or lease identity and base commit as appropriate. Require atomic publication via Git commit or validated temporary-write + atomic rename for local files.

A stale result is evidence/history, not authority to overwrite current state. Policy may reject, revalidate, or create a new obligation; it must not silently commit.

## 24. Security and trust boundaries

The new control plane creates a stronger privilege boundary and must be designed accordingly.

At minimum:

- only trusted orchestrator/reducer code writes canonical control state/events;
- agent branches/results are untrusted proposals until validation;
- malformed or adversarial ResultEnvelope content cannot inject arbitrary actions/state transitions;
- file/artifact references remain repository-contained/explicitly governed;
- secrets/private account telemetry remain outside project repositories unless a governed contract explicitly requires otherwise;
- web/manual remote execution cannot grant broader repository authority than its isolated branch/task requires;
- human decisions are authenticated through the applicable local/project trust boundary;
- control-plane corruption/replay/rollback behavior is explicitly handled.

Do not overclaim cryptographic guarantees not actually implemented.

## 25. Failure semantics and degraded operation

Because Protocol 7 makes the orchestrator mandatory for current workflow control, the old `manual operation is independently complete` invariant no longer applies to **Protocol 7 canonical execution**.

However, failure must remain truthful and recoverable:

- unavailable orchestrator/control store => Protocol 7 workflow cannot make canonical transitions; report blocked/unavailable rather than silently falling back to document control;
- agent/harness/remote transport failure => retain task/control state and retry/failover according to policy without counterfeit completion;
- corrupted/inconsistent event/state projection => stop mutation, rebuild/verify from canonical history where possible, otherwise require repair/human intervention;
- Protocol 6.1 fallback is a **version rollback**, not simultaneous dual authority.

The preserved immutable Protocol 6.1 release remains the recovery path while Protocol 7 matures.

## 26. Protocol 6.1 rollback boundary and no dual-current control plane

During Protocol 7 development, preserve the accepted 6.1 immutable snapshot.

If Protocol 7 is unsafe before/after early cutover:

1. stop Protocol 7 orchestrator mutation;
2. restore/check out the pinned Protocol 6.1 release and compatible profile/tooling;
3. resume the 6.1 document-controlled workflow there;
4. repair Protocol 7 separately.

Do not allow live Protocol 6.1 workplan status and Protocol 7 JSON state to both claim canonical workflow authority over the same current run.

Shadow comparison before cutover is permitted because only one side is authoritative.

## 27. Migration phases

### Phase A — complete and freeze Protocol 6.1

Protocol 7 implementation does not begin its canonical-control cutover until the 6.1 workplan passes, is behaviorally qualified, and an immutable recovery identity exists.

### Phase B — D3 redesign and control ontology

Reopen/supersede the affected orchestrator architecture. Define control-plane ownership, schemas, typed graph semantics, event/state model, action registry, privilege boundaries, and migration topology before implementation.

### Phase C — deterministic kernel

Implement schema/reference/semantic/transition/staleness validation, reducer, event history, derived state, graph/index, obligation calculation, and deterministic replay/recovery.

### Phase D — agent contract/transports

Implement immutable TaskEnvelope/ResultEnvelope, local execution adapter, isolated Git/web transport, polling, idempotency, concurrency and stale-result handling.

### Phase E — shadow orchestration under 6.1 authority

Keep Protocol 6.1 document workflow canonical while Protocol 7 computes non-authoritative expected state/transitions from the same observed work.

Compare at least:

- stage/domain routing;
- blocker/Serious-Challenge propagation;
- evidence invalidation/admissibility;
- workplan reopen/closure;
- human gates/risk override;
- stale-result behavior;
- next obligation/action.

Differences require classification: Protocol 7 defect, 6.1 ambiguity/defect, deliberate stronger rule, or genuinely unresolved semantic judgment. Do not force equality when 7.0 intentionally improves the semantics, but document and independently review every material difference.

### Phase F — adversarial qualification and fault injection

Qualify deterministic and semantic behavior before cutover.

### Phase G — cutover

Only after accepted D3 architecture, implementation acceptance, shadow qualification, independent Review, and required human/project approval:

- make Protocol 7 control state canonical;
- remove duplicate workflow-control duties from current skills/workplans/prompts;
- keep semantic documents intact;
- make orchestrator participation mandatory for Protocol 7 current workflow;
- retain 6.1 only as immutable rollback/recovery version.

## 28. Required deterministic/failure qualification

At minimum test:

- deterministic replay from canonical event history;
- restart/crash recovery at event/state publication boundaries;
- malformed/unknown-schema agent output;
- illegal transition proposals;
- task/result digest mismatch;
- stale state revision/old attempt/expired lease result;
- duplicate/idempotent result ingestion;
- concurrent local/remote agents;
- remote branch divergence/unrelated commit;
- partial local result publication;
- unavailable Git remote/network;
- interrupted local harness;
- agent execution failure/cancellation;
- unavailable/mismatched skill/protocol source;
- Serious Challenge and human gate propagation;
- risk-accepted/provisional descendant behavior;
- stale passing evidence rejection;
- bounded graph invalidation preserving unaffected siblings;
- graph/index rebuild from canonical history;
- derived-state corruption detection;
- rollback to immutable Protocol 6.1.

## 29. Required semantic/adversarial qualification

Protocol 7 must additionally prove that automation preserves Protocol semantics rather than only state-machine mechanics.

Scenarios must include:

- D4 defect remains D4 when upstream authority is coherent;
- downstream observation can challenge D3/D2/D1 and blocks dependent closure appropriately;
- orchestrator does not auto-resolve scientific ambiguity;
- changed authority invalidates only materially dependent descendants/evidence;
- evidence specification may survive concretization replacement while prior realization becomes stale/remapped;
- proxy evidence cannot close the real semantic owner;
- missing required check cannot be converted into PASS by reducer policy;
- human risk override remains non-epistemic and visibly provisional downstream;
- local and web transports produce equivalent logical control outcomes for the same accepted ResultEnvelope;
- verbose/alternative agent prose cannot alter control outcome when structured fields are identical;
- workplan/document wording no longer secretly overrides formal lifecycle state;
- semantic historical reasoning remains accessible and referenced after control-plane cutover;
- minimum justified control machinery is maintained and no duplicate second authority emerges.

## 30. Versioning and historical preservation

Protocol 7 major-version implementation must update protocol versioning/compatibility documentation so that:

- Protocol 6.1 workplans remain governed by 6.1 and can resolve through the immutable 6.1 profile/snapshot;
- Protocol 7 work uses the new control schema/profile/architecture intentionally;
- historical 5.16 and 6.0/6.1 truth remains immutable/version-bound;
- the control schema version, orchestrator API/SPI version, profile version, and Protocol semantic version are not silently conflated;
- migration tools, if any, never reinterpret old semantic records as though they had been authored under Protocol 7.

## 31. Acceptance criteria

Protocol 7.0 cannot cut over or PASS until all of the following hold:

1. Protocol 6.1 is completed, qualified, and immutably recoverable;
2. the affected frozen orchestrator D3 architecture has been deliberately reopened, independently reviewed, and superseded by a coherent Protocol 7 architecture rather than patched around;
3. the new architecture has exactly one canonical workflow-control writer/owner and no contradictory document/Tracker/profile/reducer authority;
4. a versioned formal control data contract exists and is syntactically/semantically validated;
5. semantic artifacts remain authoritative carriers of substantive reasoning and are referenced rather than duplicated into control JSON;
6. logical identity/revision and typed dependency/evidence relations support bounded deterministic impact closure;
7. evidence specification/realization/observation/admissibility semantics preserve Protocol 6.1 behavior;
8. immutable TaskEnvelope and bound ResultEnvelope contracts are implemented;
9. agent assessment is separated from canonical transition authority;
10. deterministic event replay produces exactly the same state for the same accepted history;
11. stale/concurrent/duplicate/partial result behavior is deterministic and tested;
12. Serious Challenge, human gates, and risk-accepted/provisional semantics cannot be bypassed by automation;
13. local transport runs fully automatically through the common logical agent protocol where configured;
14. web/manual Git transport uses the same logical protocol and validates isolated remote writeback without unsafe pull/mutation of the active orchestrator worktree;
15. polling-first remote completion works without requiring unjustified server/message-broker infrastructure;
16. mandatory orchestrator failure produces truthful Protocol 7 non-closure rather than implicit document-control fallback;
17. shadow-mode comparison has explained all material 6.1/7.0 differences;
18. deterministic/failure and semantic/adversarial qualification execute and pass;
19. repository/build/package/profile/orchestrator affected regression/integration checks execute and pass;
20. independent final Review/Challenge Pass finds no genuine blocker or active governing Serious Challenge;
21. cutover removes duplicate control duties from current Protocol 7 workplans/skills/prompts without deleting their semantic content;
22. rollback to immutable Protocol 6.1 has been demonstrated.

## 32. Explicit non-goals

- Do not convert scientific/method/architecture/workplan/history/review documents into JSON content stores.
- Do not encode full agent reasoning or raw evidence in the control plane.
- Do not add a dedicated graph database without demonstrated need.
- Do not implement a monolithic combinatorial FSM when composed state dimensions are sufficient.
- Do not let Git branch/PR/commit state implicitly define SSDP workflow semantics.
- Do not let agents directly mutate canonical control state.
- Do not make the reducer decide scientific truth or replace human ratification.
- Do not retain the old document-controlled workflow as a simultaneously canonical Protocol 7 fallback.
- Do not layer the new control owner under contradictory frozen orchestrator 1.6.0 authority; explicitly redesign/supersede the affected D3 surface.
- Do not weaken Protocol 6.1 evidence/acceptance/Challenge safeguards for automation convenience.
- Do not add webhook/message-broker/distributed infrastructure before the simpler Git/polling transport is shown insufficient.

## 33. Final target

Protocol 7.0 shall establish this governing separation:

```text
semantic artifacts carry meaning;
agents investigate and reason;
evidence supports or challenges governed claims;
schemas communicate bounded control facts;
rules validate legal transitions;
the orchestrator alone commits workflow state.
```

The central deterministic contract is:

```text
(protocol/control versions, initial state, ordered accepted events)
 -> exactly one resulting control state
```

This is a deterministic **control** guarantee, not a claim that scientific reasoning is deterministic. Semantic judgment remains agent/human reasoning until accepted as a typed, provenance-bearing control fact; only then do deterministic consequences propagate.
