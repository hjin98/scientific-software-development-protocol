---
kind: architecture
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.5.0
supersedes_architecture_version: 1.4.0
protocol_version: 5.16.0
status: frozen
frozen_date: 2026-09-07
---

# SDP Orchestrator Architecture

## 1. Purpose and authority

This document is the parent architectural authority for the SDP/Protocol Orchestrator. It defines a nested capability ladder whose lower levels remain independently useful, installable, testable, and releasable:

```text
Level 0  Core + Prompt
            |
            v
Level 1  Tracker
            |
            v
Level 2  Adapters + capability recommendation
            |
            v
Level 3  Scheduler + metering + prediction + AUTO routing
```

Every higher level requires the complete lower level. No lower level may require, import, instantiate, persist state for, or otherwise depend on a higher level in order to perform its accepted functions.

This architecture is Tier 1B Frozen architecture for the orchestrator implementation series. Module workplans derive implementation obligations losslessly from it. They may choose delegated realization details, but may not silently change dependency direction, authority boundaries, public API/SPI semantics, persistence ownership, capability roles, or module responsibilities.

If implementation evidence invalidates a Frozen choice, reopen only the affected architecture surface before changing it.

## 2. Product invariants

1. **Progressive usefulness.** Core alone resolves and prints a complete Protocol prompt. Every extension adds capability without making the lower mode incomplete.
2. **Strict asymmetric dependencies.** `core <- tracker <- adapters <- scheduler`. Reverse or lateral production dependencies are forbidden.
3. **Graceful degradation.** If a higher extension is absent, disabled, incompatible, or unhealthy, the application falls back to the highest healthy lower capability set. Degradation does not silently bypass an explicitly configured safety/resource policy.
4. **One CLI and one composition root.** Core owns `sdp` and application composition. Extensions register through versioned SPIs; Core does not contain scattered imports or special cases for higher implementations.
5. **Versioned public boundaries.** Higher modules consume lower modules only through documented `api.vN` and `spi.vN` surfaces.
6. **No duplicated workflow authority.** Git, workplans, compatible Protocol profiles, and Design/Implementation results remain semantic authorities. Tracker history is evidence; benchmark data is recommendation evidence; Scheduler resource models select routes only.
7. **Manual operation is first-class.** Prompt and Tracker modes remain useful with copy/paste I/O. Direct agent execution is optional.
8. **Capability recommendation precedes resource scheduling.** Adapter may recommend routes using capability evidence but does not meter quota, learn resource consumption, or automatically resource-route work. Scheduler owns those functions.
9. **Benchmark observations preserve context.** Scores retain source, benchmark/version, model identity, effort, harness/configuration, uncertainty, freshness, and identity-match quality.
10. **Scheduler remains subordinate to workflow intent.** It selects routes only after the required workflow stage is known and only among engineering-sufficient routes.
11. **Private state stays outside project repositories.** Tracker and higher modules persist history/telemetry under user-local state roots, never in protocol/target repositories by default.
12. **Subset acceptance is permanent.** A later module may not make an earlier module's standalone acceptance depend on the later module.
13. **Stable IDs cross modules; implementation objects do not.** Cross-module references use small value objects/opaque IDs, not private repositories, SQL/ORM objects, backend sessions, event loops, or subprocess instances.
14. **Read-only query and durable mutation are visibly distinct.** Preview/query calls may not hide durable writes. Scheduler preview is read-only; admission is atomic/reserving.
15. **Long-running execution is explicit.** Agent execution supports admission, start, event observation, control/permission response, cancellation, and terminal result without exposing backend async/session internals.
16. **Manual and direct routes share one route vocabulary.** A web/manual route is first-class with explicit delivery, prompt-context, and repository-access capabilities.
17. **Capability identity is independent of API version.** Semantic capability keys do not embed `v1`; API compatibility is represented separately.
18. **Explicit route choice is not an admission bypass.** With Scheduler active, explicit route bypasses ranking but still undergoes configured hard feasibility/resource admission; it may be rejected but not silently substituted.
19. **Route admission precedes final prompt rendering.** Selected route determines prompt context, so route admission occurs before execution prompt rendering.
20. **Run identity precedes scheduling and rendering.** Core allocates a RunId without persistence so Scheduler, prompt, Tracker, and Adapter share one attempt identity.
21. **Manual result tracking has a structured seam from day one.** Core prompts request a versioned result envelope with run/fingerprint identity.
22. **Protocol version binding is explicit.** An older workplan is never silently rendered through a newer incompatible workflow profile merely because the installed orchestrator is newer.
23. **One mutating run owns one local worktree.** Concurrent orchestrator-controlled mutating local executions against the same physical worktree are serialized through a cross-process lease keyed by worktree identity, not project name.
24. **Workflow routing authority is profile-owned.** Tracker may project history and recommend the next action, but it consumes the compatible Core Protocol profile's declared stage/routing contract rather than duplicating private prompt/profile logic.
25. **Uncertain routing remains uncertain.** Unknown result outcomes, blocker classes, or multiple materially valid next stages produce an explicit ambiguous recommendation rather than a guessed transition.

## 3. Capability ladder and distributions

### 3.1 Level 0 — Core / Prompt

```text
command
  -> observe configured repository/workplan/protocol inputs
  -> resolve requested stage under compatible Protocol profile
  -> render canonical compatible prompt
  -> print complete copy/paste-ready prompt
```

No durable workflow history, agent process, benchmark refresh, metering, or scheduling is required.

### 3.2 Level 1 — Tracker

Adds persistent development history, prompt/output association, manual result ingestion, current development projection, active/retired workplan history, PASS/NO-PASS/stale-evidence handling, next-action recommendation grounded in the Core workflow profile, persistent user workplan selection, workflow graph, retention/export/purge, and shared private coordination/storage substrate for higher modules.

### 3.3 Level 2 — Adapters

Adds configured routes, direct structured agent integration, manual-web handoff routes, selected-route execution, benchmark collection, and static capability recommendation. No quota metering/prediction/resource-aware AUTO exists without Scheduler.

### 3.4 Level 3 — Scheduler

Adds account/resource ledgers and meters, usage attribution, atomic reservations, task features, usage/outcome prediction, route feasibility/scoring, default AUTO selection, future-stage reserves, and failover. It never creates a second agent runner/workflow reducer.

### 3.5 Distribution graph

```text
sdp-orchestrator-core
        ^
        |
sdp-orchestrator-tracker
        ^
        |
sdp-orchestrator-adapters
        ^
        |
sdp-orchestrator-scheduler
```

Installing a higher distribution installs required lower distributions. Core alone does not pull higher/ACP/DB-lock/benchmark/ML dependencies merely for future convenience.

## 4. Python packaging and namespace

Native PEP 420 namespace:

```text
src/sdp_orchestrator/              # NO __init__.py
    core/
    tracker/
    adapters/
    scheduler/
```

Public APIs:

```text
sdp_orchestrator.core.api.v1
sdp_orchestrator.tracker.api.v1
sdp_orchestrator.adapters.api.v1
sdp_orchestrator.scheduler.api.v1
```

Provider SPIs:

```text
sdp_orchestrator.core.spi.v1
sdp_orchestrator.tracker.spi.v1
sdp_orchestrator.adapters.spi.v1
sdp_orchestrator.scheduler.spi.v1
```

Cross-module production imports target public API/SPI only.

## 5. Public API standard

### 5.1 API versus SPI

API is consumed to use semantic services; SPI is implemented to contribute behavior to a lower owner. Consumers do not depend on provider/private classes. Providers receive only explicit SPI context. First-party modules obey the same boundary.

### 5.2 Compatibility

A public major is a semantic compatibility contract. Breaking request/response semantics, required-field changes, method removal/renaming, changed ID/mutation/error meaning, or incompatible serialization require a new API/SPI major. Additive optional fields/new methods/namespaced values may remain within a major when old consumers behave correctly.

Callers are not required to enumerate every future stage/model/effort/event/status/error. Persisted schema, event schema, benchmark schema, digest canonicalization, protocol profile, workflow-profile schema, and API majors are independent version dimensions.

### 5.3 Public records

Cross-module records are immutable-by-convention JSON-compatible value objects. Pydantic is initial implementation technology, not semantic authority.

- timestamps: timezone-aware ISO-8601 UTC;
- IDs: opaque strings;
- digests: cryptographic algorithm + canonicalization scheme + value;
- unsupported required request semantics fail rather than silently disappear;
- response consumers tolerate additive optional fields;
- records never contain open files, DB connections, subprocess/SDK/session objects, event loops, locks, or mutable repository objects.

### 5.4 Pagination

Potentially unbounded collections use:

```text
Page[T]
  items: tuple[T, ...]
  next_cursor: str | None
```

Cursor is opaque/query-version scoped. Bounded catalogs may return tuples.

### 5.5 Problems/errors

```text
Problem
  code: str
  message: str
  retryable: bool | None
  details: mapping
```

Python raises `OrchestratorError(Problem)`. CLI uses `Problem.code` for deterministic exits/stderr. Modules add namespaced codes; callers do not parse human messages.

### 5.6 Idempotency/mutation

Read-looking methods (`list/get/observe/status/preview/predict/recommend/probe`) are read-only unless explicitly documented. Durable writes return receipts/IDs where retry matters.

- Tracker event record idempotent by EventId.
- Result ingest idempotent for same artifact/run binding.
- Workplan selection idempotent for same project/selection.
- Coordination lease acquire/release idempotent for same owner/resource semantics.
- Adapter admission idempotent for same run/request.
- Adapter start creates at most one active execution per RunId; ambiguous start reconciles before retry.
- Control response idempotent by stable request identity where backend supports acknowledgement.
- Scheduler admit idempotent by RunId + request fingerprint.
- Scheduler release/reconcile idempotent; no double release/charge.

### 5.7 Sync/async boundary

Core, Tracker, benchmark queries, Adapter admission, and Scheduler planning/admission are synchronously callable. Adapter long-running execution uses explicit handles/event/control methods. Implementations may use asyncio internally.

### 5.8 Two-stage API freeze

This parent freezes semantic roles, method families, mutation/idempotency behavior, required identity dimensions, workflow-routing ownership, and cross-module ownership. Each module workplan may finalize exact Pydantic field spelling/private realization only within these semantics. After independent module Review passes, that module's accepted v1 schema is the compatibility floor for later modules.

## 6. Core composition SPI

### 6.1 One extension registry

Exactly one Python entry-point group:

```text
sdp_orchestrator.extensions.v1
```

No arbitrary directory/repository plugin scanning.

### 6.2 Capability identity/version

CapabilityKey is semantic and unversioned. Initial first-party keys:

```text
prompt.render
project.observe
workplan.catalog
workflow.profile
workflow.track
workflow.project
agent.catalog
agent.execute
benchmark.catalog
benchmark.recommend
resource.meter
usage.predict
route.schedule
```

```text
CapabilityRequirement
  key
  api_spec
  multiplicity: singular | many

CapabilityProvision
  key
  api_major
  multiplicity: singular | many
```

### 6.3 Extension manifest/activation

Manifest inspection is side-effect-minimal: no subprocess/network/repository mutation/storage migration.

```text
ExtensionManifest
  extension_id
  extension_version
  core_spi_spec
  requires_extensions
  requires_capabilities
  provides_capabilities
```

Use `packaging` version/specifier comparison. First-party IDs reserved under `sdp.*`.

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Context exposes effective Core config/provider namespace, required active services, CLI/config/event/diagnostic registrars. Activation is dependency-topological; failed providers disable dependents, lower healthy services remain.

### 6.4 Service registry/application API

Services register by capability + api major + provider. Singular service cannot be silently replaced; multi-provider service order is stable by provider ID.

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, requirement: CapabilityRequirement) -> bool: ...
    def service(self, requirement: CapabilityRequirement) -> object: ...
    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

Missing/disabled/incompatible service is a structured problem, not import crash.

### 6.5 CLI/config/event ownership

The first module defining a semantic command owns it; later modules extend through lower hooks. Adapter owns `sdp run`; Scheduler extends admission through Adapter SPI.

Core owns config precedence: defaults -> config/profile -> documented env allowlist -> explicit CLI/API. Absent-extension config is preserved/diagnosed. Secrets are references/approved secret inputs.

Core process event publisher gives at-least-once optional sink delivery when retry is practical. Sinks are idempotent by EventId; sink failure cannot counterfeit primary result.

## 7. Core shared records

### 7.1 IDs

```text
ProjectKey
WorktreeKey
RunId
EventId
StageRef
CapabilityKey
ExtensionId
```

Route/model/backend/account/transport/effort identities belong to Adapter.

`WorktreeKey` identifies one configured physical local worktree after canonical path/repository resolution. Different ProjectKeys targeting the same checkout resolve to the same WorktreeKey. Distinct Git worktrees resolve to distinct WorktreeKeys.

### 7.2 DigestRef

```text
DigestRef
  algorithm
  canonicalization_scheme | None
  value
```

Initial crypto is SHA-256. Domain digests carry versioned schemes such as `sdp.prompt-fingerprint.v1`, `sdp.workplan-semantic.v1`, and `sdp.git-working-tree.v1`. Scheme semantics never change silently.

### 7.3 StageRef / ProtocolProfileRef

`StageRef` includes protocol-profile identity + protocol version + stage key. Stage names are data.

`ProtocolProfileRef` identifies the workflow/prompt interpretation contract used for a project/workplan. A profile declares protocol-version compatibility explicitly; compatibility is not inferred merely because versions share a major.

### 7.4 WorkplanRef

```text
WorkplanRef
  workplan_id
  protocol_version
  path
  artifact_digest
  semantic_digest | None
  semantic_identity_complete
  lifecycle_state
```

Semantic identity is deterministic/profile-aware, never LLM-guessed. Lifecycle-only changes may preserve semantic digest. Unsupported/ambiguous schema gives incomplete semantic identity and conservative invalidation.

### 7.5 CandidateRef

```text
CandidateRef
  repository_id
  branch_or_detached
  head_commit
  working_tree_digest | None
  identity_complete
  upstream_ref | None
  observed_remote_commit | None
  observed_at
```

Material staged/unstaged/untracked source changes alter versioned working-tree digest. Inability to fingerprint confidently gives `identity_complete=false`.

### 7.6 ProjectDescriptor / PromptProjectSnapshot

```text
ProjectDescriptor
  project_key
  worktree_key | None
  local_repo_root | None
  sanitized_remote_repository
  configured_mode
  protocol_profile
  configuration_identity
```

ProjectDescriptor is trusted local-process data, not auto-embedded in web prompts. PromptProjectSnapshot contains only execution-mode-safe repository/workplan/candidate context; web mode excludes local paths/private state/secrets/account-resource telemetry/credential-bearing remotes.

### 7.7 EventEnvelope

```text
EventEnvelope
  event_id
  event_type
  schema_version
  occurred_at
  project_key
  run_id | None
  producer_extension
  payload
```

Event types namespaced/versioned. Events are evidence, not workflow authority; unknown future types may be stored opaquely.

### 7.8 Workflow profile contract

Core exposes the machine-readable subset of the compatible Protocol workflow needed by Tracker without creating a generic workflow DSL.

```text
WorkflowProfileDescriptor
  profile: ProtocolProfileRef
  schema_version
  stages: tuple[StageDescriptor, ...]
  transitions: tuple[StageTransitionDescriptor, ...]

StageDescriptor
  stage: StageRef
  role_owner
  mutation_class
  optionality
  recognized_outcomes: tuple[str, ...]

StageTransitionDescriptor
  from_stage: StageRef
  trigger_key: str
  to_stage: StageRef | terminal
  priority_hint | None
  explanation
```

`trigger_key` is a profile-defined opaque semantic routing class, not arbitrary executable expression text. The profile documents how normalized result facts map to trigger keys. Typical Protocol 5 classes may distinguish pass/complete, implementation nonconformance, design/workplan deficiency, new independent issue, optional verification/stabilization/closeout, and terminal closure, but exact classes belong to the profile/version.

The descriptor defines allowed/recognized routing relations, not an autonomous approval engine. Tracker may recommend only a transition compatible with the descriptor and current evidence. If normalized evidence maps to zero or multiple materially plausible routing classes, recommendation is `AMBIGUOUS` rather than guessed.

### 7.9 StageResultEnvelope v1

Every rendered prompt requests:

```text
StageResultEnvelope
  schema_version
  run_id
  prompt_fingerprint
  stage
  outcome
  recommended_next_stage | None
  blockers: tuple[BlockerRecord, ...]
  completed_obligations
  pending_obligations
  checks_executed
  checks_unavailable
  candidate | None
  summary | None

BlockerRecord
  blocker_id | None
  classification: str | None
  summary: str
  authority_class | None
```

Outcome, blocker classification, authority class, and check states are extensible strings. A profile may recognize some values and leave unknown values unresolved. `recommended_next_stage` is reported evidence/hint, not routing authority; Tracker reconciles it against the WorkflowProfileDescriptor and blocker/outcome evidence.

Core renders the result request but does not persist or interpret the reported semantics.

## 8. Core / Prompt Module

### 8.1 Responsibilities

Core owns CLI/application composition, project/protocol-profile config, project catalog/worktree identity, read-only Git/workplan observation, compatible workflow-profile/stage catalog, compatible prompt-source resolution, canonical prompt loading/substitution, local/web rendering, run/prompt/result-envelope identity, stdout/optional clipboard, and capability/doctor reporting.

Core does not own durable workflow history, next-stage inference, agent processes, benchmarks, resources, or scheduling.

### 8.2 CoreAPI v1

```python
class CoreAPI(Protocol):
    def allocate_run_id(self) -> RunId: ...
    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]: ...
    def get_project(self, project: ProjectKey) -> ProjectDescriptor: ...
    def workflow(self, project: ProjectKey) -> WorkflowProfileDescriptor: ...
    def list_stages(self, project: ProjectKey) -> tuple[StageDescriptor, ...]: ...
    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...
    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]: ...
    def render(self, request: PromptRequest) -> RenderedPrompt: ...
```

`list_stages` is a bounded convenience view over `workflow().stages`, not a second source of stage semantics.

Run allocation creates an opaque ID only, no persistence. Render accepts caller RunId or allocates one. All methods are read-only with respect to target repositories.

### 8.3 Observation policy

```text
ObservationPolicy
  remote_mode: local_only | use_cached_remote | refresh_remote
  max_remote_staleness | None
```

Programmatic default local-only unless explicitly configured/requested. Results carry freshness/provenance. Unknown/stale beats hidden network I/O or invented freshness.

### 8.4 Protocol profile and prompt-source resolution

Core renders and exposes workflow semantics only through a compatible ProtocolProfileRef.

Resolution order:

```text
explicit configured compatible local protocol source/profile
  -> exact compatible packaged prompt/profile snapshot
  -> explicitly permitted read-only canonical remote source/profile
  -> truthful incompatible/unavailable non-closure
```

Rules:

- workplan `protocol_version=X` is not silently interpreted as latest installed protocol;
- a newer profile serves older work only when it explicitly declares compatibility preserving the older contract;
- semantic protocol version is not guessed to be a Git ref/tag;
- packaged snapshots are derived/version-bound artifacts, not independently edited authority;
- PromptSourceRef and WorkflowProfileDescriptor record profile/version/source identities so Tracker can reconstruct the contract used.

### 8.5 Workplan catalog

Paginated active/archive descriptors with exact/semantic identity completeness, lifecycle consistency, and selection evidence. No mtime guessing among materially plausible plans.

### 8.6 PromptRequest / RenderedPrompt

```text
PromptRequest
  run_id | None
  project
  stage
  execution_mode
  workplan_selector | None
  first_task | None
  input_overrides
  observation_policy | None

RenderedPrompt
  run_id
  prompt_text
  prompt_fingerprint: DigestRef
  stage
  prompt_source: PromptSourceRef
  workflow_profile: ProtocolProfileRef
  resolved_inputs + provenance
  prompt_context: PromptProjectSnapshot
  selected_workplan | None
  requested_result_schema identity
```

Execution mode is extensible data; v1 supports local/web.

### 8.7 Prompt fingerprint/footer

Under canonicalization `sdp.prompt-fingerprint.v1`, Core renders exact prompt bytes using fixed fingerprint placeholder after RunId is known, SHA-256 hashes placeholder-form UTF-8 bytes, then substitutes digest. WP-1 freezes literal placeholder/byte-normalization fixtures.

Every prompt asks agent to emit StageResultEnvelope v1 with matching RunId/fingerprint when possible, without requesting hidden chain-of-thought.

### 8.8 Core CLI/dependencies

```text
sdp prompt <stage>
sdp design
sdp implementation
sdp review
sdp projects
sdp capabilities
sdp doctor
```

Prompt stdout is only complete prompt. Ambiguous workplan requires bounded explicit selection. Offline compatible packaged profile/snapshot works when local repo evidence is sufficient.

Expected Core dependencies: platformdirs, typer, pydantic, python-frontmatter, packaging; optional pyperclip. No filelock/ACP/httpx/ML/higher module requirement.

## 9. Tracker Module

### 9.1 Responsibilities

Tracker owns private SQLite history/migrations, run/event/prompt/output history, manual result ingestion, workplan observation/history/user selection, derived development projection, profile-grounded next-action recommendation, graph/history/workplan interfaces, retention/export/purge, and shared durable coordination/storage for higher modules.

### 9.2 TrackerAPI v1

```python
class TrackerAPI(Protocol):
    def record(self, event: EventEnvelope) -> RecordReceipt: ...
    def ingest(self, request: IngestRequest) -> IngestResult: ...
    def status(self, request: StatusRequest) -> DevelopmentProjection: ...
    def next_action(self, request: NextActionRequest) -> NextAction: ...
    def get_run(self, run_id: RunId) -> TrackedRun: ...
    def history(self, query: HistoryQuery) -> Page[RecordedEvent]: ...
    def workplans(self, query: TrackedWorkplanQuery) -> Page[TrackedWorkplan]: ...
    def select_workplan(self, request: WorkplanSelectionRequest) -> WorkplanSelectionReceipt: ...
    def graph(self, request: WorkflowGraphRequest) -> WorkflowGraph: ...
```

Status/next/graph consume the compatible public Core `workflow()` descriptor plus fresh Core observations; they do not parse Core private profile/prompt files.

### 9.3 Manual result ingestion

Precedence: matching valid StageResultEnvelope -> bounded deterministic strong markers -> explicit user confirmation/selection. No mandatory LLM classification. Pasted data is untrusted and cannot execute orchestrator commands. Exact duplicate ingest is idempotent; mismatch fails safely unless explicitly rebound by user after disclosure.

If fallback parsing cannot confidently determine a profile-recognized outcome/blocker classification needed to route rework, Tracker stores the evidence but reports the next action as ambiguous instead of inventing classification.

### 9.4 RecordedEvent / projection / selection / graph

```text
RecordedEvent
  sequence: monotonically increasing Tracker-local integer
  recorded_at
  event
```

Recording order differs from producer wall clock. DevelopmentProjection is bounded current summary; detailed attempts remain in history. Execution status and semantic outcome are distinct.

Persistent workplan selection is private convenience, only used while compatible with current Core evidence. Stale/disappeared/conflicting selection is reported, not forced.

WorkflowGraph uses Core WorkflowProfileDescriptor stages/transitions as the allowed topology and overlays observed attempts/outcomes/current recommendation. CLI supports text + JSON; Mermaid/DOT optional presentation.

`next_action` uses normalized current evidence + profile transitions. Agent `recommended_next_stage` can corroborate but cannot override an incompatible profile transition. Multiple valid optional follow-ups may be returned as alternatives rather than forced into one pseudo-authoritative next stage.

### 9.5 Tracker storage/coordination SPI v1

Private root:

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/
  exports/
```

SQLite/WAL is v1 control store; owner-only filesystem permissions are used where OS supports them. Filelock may support local process coordination but semantic lease ownership is exposed through Tracker SPI.

```python
class TrackerStorageSPI(Protocol):
    def register_migrations(self, extension: ExtensionId, migrations: tuple[MigrationSpec, ...]) -> None: ...
    def transaction(self, extension: ExtensionId, *, write: bool) -> ContextManager[sqlite3.Connection]: ...
    def acquire_lease(self, request: LeaseRequest) -> LeaseRef: ...
    def renew_lease(self, request: LeaseRenewalRequest) -> LeaseRef: ...
    def release_lease(self, request: LeaseReleaseRequest) -> LeaseReceipt: ...
```

Tracker owns DB/config/migration/lease recovery policy. Extensions own namespaced tables and may not read/write another module's semantics directly. Lease requests carry extension owner, resource key, RunId/owner identity, TTL/renewal policy. Crashed/stale leases recover deterministically; duplicate acquire by same owner is idempotent. SQLite is explicitly part of this SPI major.

### 9.6 Tracker CLI

```text
sdp status
sdp next
sdp ingest
sdp history
sdp workplans
sdp use <workplan>
sdp graph
```

Without Tracker Core remains functional.

## 10. Adapter Module

### 10.1 Responsibilities

Adapter owns route/model/backend/account/effort identity, manual/direct delivery, prompt-context requirement, structured transports, pre-render admission, local-worktree execution lease use, execution lifecycle, benchmark source/cache/model-identity resolver, static recommendation, and automatic Tracker integration.

Adapter does not own quota/resource ledgers.

### 10.2 Adapter identities / ExecutionRoute

```text
RouteId
ExecutionAdmissionId
ModelRef
BackendRef/HarnessRef
AccountRef
TransportRef
EffortRef
ObservedExecutionIdentity
```

RouteId is stable configured opaque key.

```text
ExecutionRoute
  route_id
  backend
  account
  transport
  model
  effort
  delivery_mode: direct | manual_handoff
  prompt_execution_mode: local | web | future compatible value
  repository_access: local_worktree | remote_connector | future compatible value
  mutability: mutating | read_only | unknown
  configured capability metadata
```

Manual-web routes are first-class. Prompt mode is explicit rather than inferred from delivery. Internal model IDs are separate from external benchmark names; one Adapter resolver owns aliases/mappings and ambiguity handling.

### 10.3 AdapterAPI v1

```python
class AdapterAPI(Protocol):
    def routes(self, query: RouteQuery | None = None) -> Page[ExecutionRoute]: ...
    def probe(self, route: RouteId) -> RouteCapabilitySnapshot: ...
    def benchmarks(self, query: BenchmarkQuery) -> Page[BenchmarkObservation]: ...
    def recommend(self, request: RecommendationRequest) -> RecommendationSet: ...
    def admit(self, request: ExecutionAdmissionRequest) -> ExecutionAdmission: ...
    def abandon(self, request: ExecutionAdmissionAbandonRequest) -> ExecutionAdmissionReceipt: ...
    def start(self, request: AgentStartRequest) -> AgentRunHandle: ...
    def events(self, request: AgentEventQuery) -> Page[AgentEvent]: ...
    def respond(self, request: AgentControlResponse) -> AgentControlReceipt: ...
    def cancel(self, run_id: RunId) -> AgentControlReceipt: ...
    def wait(self, request: AgentWaitRequest) -> AgentRunResult: ...
```

### 10.4 Pre-render admission and worktree lease

Admission request includes allocated RunId, project/stage/task/workplan/candidate, optional requested route, interaction/manual constraints, capability/tool/privacy constraints, and Adapter-generated candidate route snapshots.

No route-policy provider: admit explicit route or explicit configured default only. Active route-policy provider: explicit route admitted unchanged/rejected; omitted route may AUTO select.

ExecutionAdmission returns selected route, prompt mode, candidate binding, optional policy admission ref, expiry/revalidation, and reason metadata.

For a mutating local-worktree route, Adapter acquires a Tracker coordination lease on WorktreeKey before start and holds/renews it through terminal/abandonment. Different ProjectKeys targeting the same WorktreeKey conflict. Read-only local sharing is allowed only if explicit lease semantics safely support it; mutating default is exclusive.

### 10.5 Frozen execution flow

```text
Core.allocate_run_id
  -> Core.observe/resolve stage + candidate/workplan/profile
  -> Adapter.admit(route explicit/default/AUTO policy; acquire required admission/lease)
  -> Core.render(same RunId; execution_mode = admitted route.prompt_execution_mode)
  -> Adapter.start(exact admission + rendered prompt)
```

Start rejects RunId/stage/candidate/profile/prompt-mode mismatch or stale admission. Render/user-confirm failure before start invokes Adapter.abandon. Expiry is fail-safe, not normal cleanup.

### 10.6 Manual/direct lifecycle

Manual route start spawns no process; returns awaiting-external-result handle + ManualHandoffArtifact. User response enters Tracker ingest; wait may observe completion/timeout. Direct process controls on manual route return structured unsupported problem.

Direct route start returns stable handle; events are cursor-paged normalized events; respond uses stable control-request IDs; cancel idempotent; wait returns terminal result/timeout without destroying underlying run automatically.

One RunId has at most one active execution. Ambiguous start/crash reconciles before retry. Worktree lease releases only after safe terminal/abandon reconciliation.

### 10.7 AgentRunResult

Separates process status from agent workflow semantics. Includes run/admission/route, configured route, ObservedExecutionIdentity + provenance/confidence, backend/session where available, visible final response, structured result, candidate observations, interruption/failure class, transport telemetry, and Tracker evidence. Planned identity and observed identity remain distinct. Zero exit is not workflow PASS.

### 10.8 Agent transport SPI

```python
class AgentTransportProvider(Protocol):
    def descriptor(self) -> TransportDescriptor: ...
    def probe(self, request: TransportProbeRequest) -> TransportProbeResult: ...
    def start(self, request: TransportStartRequest) -> TransportRunRef: ...
    def events(self, request: TransportEventQuery) -> Page[TransportEvent]: ...
    def respond(self, request: TransportControlResponse) -> TransportControlReceipt: ...
    def cancel(self, ref: TransportRunRef) -> TransportControlReceipt: ...
    def wait(self, request: TransportWaitRequest) -> TransportTerminalResult: ...
```

Prefer ACP where conformant; use documented native structured RPC/SDK/JSON otherwise. PTY scraping not primary when structured interface exists. Initial families: Claude, Codex, OMP, Pi, Antigravity.

### 10.9 Route-policy SPI

```python
class RoutePolicyProvider(Protocol):
    def preview(self, request: RoutePolicyRequest) -> RoutePolicyDecision: ...
    def admit(self, request: RoutePolicyRequest) -> RoutePolicyAdmission: ...
    def abandon(self, request: RoutePolicyAbandonment) -> RoutePolicyReceipt: ...
    def reconcile(self, request: RoutePolicyReconciliation) -> RoutePolicyReceipt: ...
```

Preview read-only; admit may reserve; explicit route unchanged/rejected; omitted may select; abandon handles pre-start; reconcile handles started/terminal/manual result. Idempotent.

### 10.10 Benchmark SPI/recommendation

Benchmark providers fetch/normalize versioned snapshots preserving source/schema/version, fetched/generated time, digest/ETag, licensing/attribution, metric value/unit/uncertainty, external model identity, effort, harness/config, freshness, and identity-match quality.

Artificial Analysis is preferred current general-intelligence evidence; DeepSWE preferred current coding evidence. Exact endpoints/tiers are mutable provider configuration. DeepSWE match quality remains `EXACT_CONFIG_MATCH`, `MODEL_EFFORT_PROXY`, `MODEL_ONLY_PROXY`, or `UNRESOLVED`. Never fabricate missing scores or a universal scalar combining incompatible metrics.

Role policy: Design/hard semantic work prioritizes general intelligence; Implementation prioritizes coding evidence; Review/Verification prioritize high general intelligence and may show provider/model independence secondarily.

ACP is optional transport dependency; httpx justified for bounded source HTTP. No Scheduler/ML requirement.

### 10.11 Adapter CLI

```text
sdp agents
sdp routes
sdp benchmarks ...
sdp models
sdp recommend <stage>
sdp run <stage> --route <route-id>
```

Manual route produces/copies handoff and awaits external result.

## 11. Scheduler Module

### 11.1 Responsibilities

Scheduler owns resource ledgers/meters, pricing/opaque quotas, reset/window inference, global reservations/uncertainty holds, usage attribution, task features, usage/outcome prediction, future-stage reserves, route admission/scoring, AUTO selection, and interruption rescheduling. It never launches agents directly.

### 11.2 SchedulerAPI v1

```python
class SchedulerAPI(Protocol):
    def resources(self, query: ResourceQuery | None = None) -> Page[ResourceState]: ...
    def usage(self, query: UsageQuery) -> Page[UsageRecord]: ...
    def predict(self, request: PredictionRequest) -> UsagePrediction: ...
    def preview(self, request: ScheduleRequest) -> ScheduleDecision: ...
    def admit(self, request: ScheduleRequest) -> AdmissionDecision: ...
    def release(self, request: AdmissionReleaseRequest) -> AdmissionReleaseReceipt: ...
    def reconcile(self, request: ReservationReconciliationRequest) -> ReservationReconciliation: ...
```

Preview read-only; admit atomically re-observes resources, revalidates feasibility, selects/validates route, creates reservations.

### 11.3 ScheduleRequest/idempotency

Request includes RunId, project/stage/task features, candidate/workplan/profile identity, Adapter candidate route snapshots, optional requested RouteId, interaction/manual constraints, policy overrides.

Requested route evaluates exact route only. Omitted route AUTO may choose. Manual route requires allowed handoff; unattended requires automatable route.

Admission request fingerprint covers all feasibility/reservation semantics. Same RunId+fingerprint retry returns same live admission; conflicting live request fails. `release` handles never-started admission; expiration is fail-safe. Reconcile idempotent.

### 11.4 Resource ledger model

```text
allowance_visibility: OPAQUE | PRICED
expiration: EXPIRING | NON_EXPIRING
reset_semantics:
  NONE | FIRST_USE_ANCHORED | ACCOUNT_FIXED | BILLING_CYCLE |
  CALENDAR_FIXED | CONTINUOUS_ROLLING | UNKNOWN
funding_behavior:
  HARD_STOP | FALLBACK_TO_OVERAGE | POSTPAID
meter/source/provenance/freshness
reservations/uncertainty holds
```

`UNMETERED_FOR_SCHEDULER`, `METERED`, `UNKNOWN` remain distinct. Shared account quota represented once/referenced by routes; dual windows simultaneous. Opaque quota remains provider units; PAYG uses versioned pricing.

### 11.5 Meter SPI/reservations

```python
class AccountMeterProvider(Protocol):
    def descriptor(self) -> MeterDescriptor: ...
    def observe(self, request: MeterRequest) -> MeterSnapshot: ...
```

Prefer official/machine-readable sources; browser scraping not normal. Preserve source/unit/time/freshness/confidence/account.

Metered execution reserves predicted capacity across consumed ledgers atomically. Manual/unmetered route may have no quota reservation but still admission identity. Crash before authoritative post-meter keeps uncertainty hold; current provider meters/hard limits outrank stale predictions.

### 11.6 Prediction/scheduling

Predict distributions for runtime, per-ledger consumption, token categories where relevant, monetary cost, stage-quality completion probability, interruption probability, and future repair rounds. Cold start uses interpretable priors by stage/role x model x effort x backend/transport with project corrections; early learning uses empirical quantiles/EWMA/shrinkage without mandatory ML; persist calibration.

AUTO only when Scheduler active. Hard feasibility before ranking. Feasibility includes capability/effort, tools/skills, repository access, privacy, independence, backend health, interaction, predicted capacity, and protected future Review/Design reserve. Ranking may consider quality completion, interruption, future capacity, expiring quota opportunity cost, PAYG cost, handoff/continuity, independence/diversity, latency.

### 11.7 Adapter integration/persistence

Scheduler implements Adapter route-policy SPI. Adapter supplies candidate routes/request; Scheduler validates/selects/reserves; Adapter renders/starts; pre-start failure abandons/releases; terminal/manual completion reconciles.

Scheduler adds namespaced tables/migrations to Tracker user-global SQLite through Tracker SPI. Quota/account state is global across projects. No Tracker workflow-table mutation.

### 11.8 Scheduler availability policy

Standalone Adapter operation remains valid when Scheduler is not installed/enabled.

If Scheduler was configured as required and fails activation/becomes unavailable, Adapter does not silently treat it as absent for a resource-governed run. AUTO is unavailable and such execution fails closed or requires an explicit user-approved downgrade/override according to configuration. Unmetered/manual routes may remain available when policy permits.

This distinguishes modular degradation from accidental resource-policy bypass.

## 12. Configuration ownership

Core owns canonical config/project identity. Extensions contribute namespaced validated sections.

```toml
[core]

[projects.mdstats]
repo = "/path/to/mdstats"
mode = "hybrid"

[tracker]
# retention/history

[adapters]
# routes/backends/models/benchmark sources

[scheduler]
# ledgers/meters/prediction/admission/failure policy
```

Unknown absent-extension sections preserved/diagnosed. Secrets are references/approved secret inputs, never ordinary snapshots/history.

## 13. Persistence/event ownership

Core stateless across invocations except config/bounded prompt-profile cache. Tracker introduces persistence; higher modules extend through Tracker SPI.

- one SQLite DB may contain multiple extension table families with one semantic owner each;
- only owner writes tables; semantic cross-module reads use APIs;
- migration order follows dependency order;
- removing higher extension leaves lower data readable;
- raw prompt/output and numeric telemetry have separable retention;
- private state files use restrictive owner-only permissions where supported;
- persisted state is evidence/convenience, not repository authority.

## 14. CLI capability behavior

### Core

```text
sdp design
sdp implementation
sdp review
sdp prompt <stage>
sdp projects
sdp capabilities
sdp doctor
```

### + Tracker

```text
sdp next
sdp status
sdp ingest
sdp history
sdp workplans
sdp use <workplan>
sdp graph
```

### + Adapter

```text
sdp recommend <stage>
sdp routes
sdp benchmarks ...
sdp run <stage> --route <id>
```

No resource-aware AUTO. Manual routes valid.

### + Scheduler

```text
sdp resources
sdp usage
sdp predict <stage> [--route <id>]
sdp schedule <stage> --explain
sdp run <stage>
```

Omitted route may AUTO; explicit route bypasses ranking, not hard/resource admission.

## 15. Failure/degradation

```text
Scheduler absent by design
  -> Adapter explicit/default/manual behavior

Scheduler configured-required but unhealthy
  -> no silent resource-policy bypass; fail closed/explicit override per policy

one direct transport unavailable
  -> disable route; other/manual routes remain

Adapter unavailable
  -> Tracker manual mode remains

Tracker DB unavailable/corrupt
  -> Tracker/Adapter/Scheduler unavailable
  -> Core prompt rendering remains
```

A module advertises only healthy semantic capabilities.

## 16. Security/privacy

- Installed entry-point code is trusted code, not sandboxed.
- Pasted agent output, structured results, benchmark/meter responses, remote metadata are untrusted data: enforce size/time/schema bounds; never execute embedded instructions as control commands.
- API keys/tokens never enter prompts/caches/events/logs/repositories.
- Web prompt context excludes local paths/private state/account-resource telemetry/credential remotes.
- ProjectDescriptor local path stays local process data.
- Agent subprocesses use direct argv/structured transport with explicit permission policy; no dangerous bypass default.
- Historical transcripts are not auto-injected into later prompts; only bounded structured projection is automatic.
- Benchmark licensing/attribution travels with cache.
- Private state/export files use restrictive permissions where platform supports; export is explicit user action.

## 17. Benchmark integrity

Recommendations reconstruct from source snapshots/observations preserving source, metric, benchmark/index version, generated/fetched time, model+effort+harness/config, value/uncertainty, identity match, staleness. Do not compare incompatible benchmark versions as one scale or combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into a universal scalar absent separate validated design.

## 18. Executable architecture fitness

Static checks once packages exist:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core public API/SPI only
Adapters    may import Core + Tracker public API/SPI only
Scheduler   may import Core + Tracker + Adapters public API/SPI only
```

Also enforce native namespace packaging, one extension group, no private cross-module imports, one ownership of `sdp run`, no Scheduler process runner, and Tracker graph/next-action use of Core workflow profile rather than private profile parsing.

## 19. Module acceptance ladder

Each module is implemented, independently reviewed, accepted before next.

### WP-1 Prompt

Prove Core-only install/CLI; project/worktree identity; RunId allocation; local observation/workplan paging; protocol-profile version binding and exact compatible snapshot resolution; WorkflowProfileDescriptor/stage-transition fixtures; digest/incomplete-identity schemes; explicit remote observation; prompt privacy; ambiguity; fingerprint/StageResultEnvelope+BlockerRecord fixtures; composition no extensions; API/SPI/error serialization; no higher imports/persistence.

### WP-2 Tracker

Re-prove Prompt with/without Tracker plus event/result idempotency; structured/manual ingest precedence; blocker/outcome classification and ambiguous-route behavior; run association; fresh Core observation; next-action/graph use of public WorkflowProfileDescriptor; deterministic history; subordinate workplan selection; persistence/restart; storage/migration/lease SPI; lease crash recovery; restrictive state permissions; Core usable without Tracker.

### WP-3 Adapter

Re-prove lower plus manual/direct routes; pre-render admission -> render -> start; explicit/default behavior; route-policy no/fake provider; admission abandon; prompt-mode/profile binding; same-worktree mutating-run exclusion across ProjectKeys/processes; start/events/respond/cancel/wait; planned-vs-observed identity; tracking; benchmark identity/provenance/failure degradation; no quota AUTO.

### WP-4 Scheduler

Re-prove lower plus read-only preview; atomic/idempotent admit; pre-start release; explicit route no substitution; AUTO; manual scheduling; shared/dual-window ledgers; cross-project reservations; UNMETERED vs UNKNOWN; prediction/calibration; future reserve; PAYG/expiring quota; idempotent reconcile/uncertainty; route-policy integration; configured-required Scheduler failure does not silently bypass policy; disabled/not-installed Scheduler restores intended Adapter mode.

## 20. Lossless module-workplan derivation

Frozen order:

```text
WP-1 Prompt Module
WP-2 Tracker Module
WP-3 Adapter Module
WP-4 Scheduler Module
```

Each declares:

```text
parent_architecture: orchestrator/docs/architecture.md
parent_architecture_version: 1.5.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

Each carries relevant parent invariants, responsibilities/non-responsibilities, consumed lower APIs/SPIs, public API/SPI established, affected/acceptance surface, standalone acceptance, lower-stack compatibility, and simplification/reopen triggers. Do not pre-implement later modules merely for future convenience.

## 21. Versioning/evolution

Architecture major breaks ladder/authority/dependency/API role; minor is backward-compatible strengthening before/alongside adoption; patch is clarification.

1.5.0 supersedes 1.4.0 because this final pre-implementation review added the public workflow-profile/routing contract and structured blocker routing needed by Tracker before WP-1 freezes Core API v1.

Module package versions are independent. New benchmarks/transports/meters use owning SPIs. Ordinary provider/model/benchmark/flag/predictor churn does not reopen parent architecture unless Frozen boundary is insufficient.

## 22. Active simplicity/reopen triggers

Reopen/simplify before multiple plugin loaders, reverse dependencies, duplicated CLI composition, separate mutable workflow authority, Tracker private parsing of Core profile files, a generic workflow-expression engine where profile transition descriptors suffice, benchmark fields in Core, quota abstractions below Scheduler, duplicated model identity mapping, backend-specific workflow logic, Scheduler process execution, private SQL/process objects in public API, hidden preview writes, or stubs preserving broken higher layers instead of downgrade.

Reopen parent only if evidence shows required reverse dependency, single registry insufficiency, workflow-profile descriptor unable to encode required Protocol routing without a materially different owner, public API role unable to support next module without semantic break, protocol-profile model insufficient for compatibility, or execution lifecycle unable to represent a required backend safely.

## 23. Final pre-implementation review closure — 2026-09-07

Across the repeated independent review passes, the following material pre-freeze gaps were closed before any module implementation began:

1. capability identity separated from API version and provider compatibility became explicit;
2. Core exposes trusted local project/worktree data separately from prompt-safe web context;
3. repository/workplan observation has explicit network/freshness policy;
4. WorkplanRef/CandidateRef have versioned conservative identity semantics;
5. Tracker history is idempotent/paged/deterministically ordered and owns a namespaced SQLite/lease substrate;
6. direct agent execution uses explicit admission/start/events/respond/cancel/wait rather than a one-shot call;
7. manual-web is a first-class route, while planned and observed model identities remain separate;
8. route admission occurs before route-sensitive prompt rendering, with pre-start abandonment/release;
9. explicit Scheduler routes are admitted unchanged or rejected, not silently substituted, and reservations/reconciliation are idempotent;
10. protocol prompt/profile resolution is version-bound and cannot silently reinterpret older workplans;
11. mutating local executions serialize by physical WorktreeKey rather than ProjectKey;
12. configured-required Scheduler failure cannot silently bypass resource policy;
13. Core requests a stable StageResultEnvelope and Tracker uses structured-first/manual-safe ingestion;
14. Core now exposes WorkflowProfileDescriptor stage/transition semantics and structured BlockerRecord classification so Tracker next-action/graph logic does not duplicate private Protocol routing authority.

No remaining architecture-level blocker was found. The cross-module seams are now specific enough to derive WP-1 through WP-4 losslessly, while module-local algorithms/classes remain delegated. Further speculative generalization should be rejected unless implementation evidence triggers a stated reopen condition.

## 24. Design verdict

**PASS — architecture 1.5.0 is implementation-ready.**

The next active implementation contract should be WP-1 Prompt Module only. WP-1 establishes Core, CLI/composition, Core API/SPI v1, RunId/ProjectKey/WorktreeKey/ProtocolProfileRef identity, repository/workplan observation, WorkflowProfileDescriptor, compatible canonical prompt rendering, StageResultEnvelope/BlockerRecord request schema, and prompt identity. It must not introduce Tracker persistence, agent integration, benchmark networking, or Scheduler/resource machinery.
