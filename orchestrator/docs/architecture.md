---
kind: architecture
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.2.0
supersedes_architecture_version: 1.1.0
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

This architecture is Tier 1B Frozen architecture for the orchestrator implementation series. Module workplans derive implementation obligations losslessly from it. They may choose delegated implementation details, but may not silently change dependency direction, authority boundaries, public API/SPI semantics, persistence ownership, capability roles, or module responsibilities.

If implementation evidence invalidates a Frozen choice, reopen only the affected architecture surface before changing it.

## 2. Product invariants

1. **Progressive usefulness.** Core alone resolves and prints a complete Protocol prompt. Every extension adds capability without making the lower mode incomplete.
2. **Strict asymmetric dependencies.** `core <- tracker <- adapters <- scheduler`. Reverse or lateral production dependencies are forbidden.
3. **Graceful degradation.** If a higher extension is absent, disabled, incompatible, or unhealthy, the application falls back to the highest healthy lower level. Core prompt rendering remains available unless Core itself is broken.
4. **One CLI and one composition root.** Core owns `sdp` and application composition. Extensions register through versioned SPIs; Core does not contain scattered imports or special cases for higher implementations.
5. **Versioned public boundaries.** Higher modules consume lower modules only through documented `api.vN` and `spi.vN` surfaces.
6. **No duplicated workflow authority.** Git, workplans, compatible Protocol profiles, and Design/Implementation results remain semantic authorities. Tracker history is evidence; benchmark data is recommendation evidence; Scheduler resource models select routes only.
7. **Manual operation is first-class.** Prompt and Tracker modes remain fully useful with copy/paste I/O. Direct agent execution is optional.
8. **Capability recommendation precedes resource scheduling.** Adapter may recommend routes using capability evidence but does not meter quota, learn resource consumption, or automatically resource-route work. Scheduler owns those functions.
9. **Benchmark observations preserve context.** Scores retain source, benchmark/version, model identity, effort, harness/configuration, uncertainty, freshness, and identity-match quality.
10. **Scheduler remains subordinate to workflow intent.** It selects routes only after the required workflow stage is known and only among engineering-sufficient routes.
11. **Private state stays outside project repositories.** Tracker and higher modules persist history/telemetry under user-local state roots, never in the protocol repository or target software repository by default.
12. **Subset acceptance is permanent.** A later module may not make an earlier module's standalone acceptance depend on the later module.
13. **Stable IDs cross modules; implementation objects do not.** Cross-module references use small value objects and opaque IDs, not private repositories, SQL/ORM objects, backend sessions, event loops, or subprocess instances.
14. **Read-only query and durable mutation are visibly distinct.** Preview/query calls may not hide durable writes. Scheduler `preview` is read-only; `admit` is atomic and reserving.
15. **Long-running execution is explicit.** Agent execution supports start, event observation, control/permission response, cancellation, and terminal result without exposing one backend's async/session implementation.
16. **Manual and direct routes share one execution-route vocabulary.** A web/manual route is not a failed local route. It is a first-class route with different delivery and repository-access capabilities.
17. **Capability identity is independent of API version.** Semantic capability keys do not embed `v1`; API compatibility is represented separately so a future v2 service can satisfy the same semantic capability without inventing another capability name.
18. **Explicit route choice is not an admission bypass.** When Scheduler policy is active, an explicitly requested route bypasses ranking but still undergoes configured hard feasibility/resource admission. Scheduler may reject it but may not silently substitute another route.

## 3. Capability ladder and distributions

### 3.1 Level 0 — Core / Prompt

Required capability:

```text
command
  -> observe configured repository/workplan/protocol inputs
  -> resolve requested stage
  -> render canonical prompt
  -> print complete copy/paste-ready prompt
```

No durable workflow history, agent process, benchmark refresh, metering, or scheduling is required.

### 3.2 Level 1 — Tracker

Adds persistent development history, prompt/output association, manual response ingestion, current development projection, active/retired workplan history, PASS/NO-PASS and stale-evidence handling, next-action recommendation, and text/JSON/graph query surfaces.

All agent I/O may remain manual.

### 3.3 Level 2 — Adapters

Adds configured routes, direct structured agent integration, one-command execution of a user-selected route, manual-web route catalog/handoff integration, online benchmark collection, and static capability recommendation.

There is no quota metering, usage prediction, or resource-aware automatic route selection at this level. Without Scheduler, execution requires an explicit route or explicit user-configured default.

### 3.4 Level 3 — Scheduler

Adds resource ledgers/meters, usage attribution, atomic reservations, task features, usage/outcome prediction, route feasibility/scoring, default AUTO selection, and receding-horizon failover.

Scheduler selects/admit routes and delegates execution to Adapter. It does not create another agent runner or workflow reducer.

### 3.5 Distribution dependency graph

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

Installing a higher distribution installs required lower distributions through ordinary dependencies. Core alone must not pull Tracker, Adapter, Scheduler, ACP, DB-locking, benchmark-network, or ML-only dependencies merely for future convenience.

## 4. Python packaging and namespace

Use native PEP 420 namespace packaging:

```text
src/sdp_orchestrator/              # NO __init__.py
    core/                           # regular package
    tracker/                        # separate distribution
    adapters/                       # separate distribution
    scheduler/                      # separate distribution
```

Public API packages:

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

Cross-module production imports target public API/SPI paths only.

## 5. Public API standard

### 5.1 API versus SPI

- API is consumed to use a module's semantic services.
- SPI is implemented to contribute behavior to a lower owner.
- API consumers do not depend on provider/private classes.
- SPI providers receive only services explicitly granted by their context.
- First-party modules obey the same boundaries as third-party providers.

### 5.2 Compatibility rule

A public major is a semantic compatibility contract.

Breaking request/response semantics, required-field changes, method removal/renaming, changed ID meaning, changed mutation semantics, changed error meaning, or incompatible serialization require a new API/SPI major.

Adding optional response fields with safe defaults, new methods, new namespaced values, or new data values may remain within a major when old consumers continue to behave correctly.

Existing callers must not be forced to enumerate every future stage, model, effort, event, status, or error value.

Persisted schema, event schema, benchmark source schema, and API major versions are independent dimensions.

### 5.3 Public records

Cross-module request/response records are immutable-by-convention value objects with JSON-compatible serialization. Pydantic is the initial implementation technology but not the semantic contract.

Rules:

- timestamps serialize as timezone-aware ISO-8601 UTC;
- IDs serialize as opaque strings;
- digests use `DigestRef`;
- request parsing rejects unsupported required semantics rather than silently dropping them;
- response consumers tolerate additive optional fields;
- public records never contain open file handles, DB connections, subprocess/SDK/session objects, event loops, locks, or mutable repository objects.

### 5.4 Pagination

Potentially unbounded collections use:

```text
Page[T]
  items: tuple[T, ...]
  next_cursor: str | None
```

Cursor representation is opaque and valid only for the owning API/query contract. Small bounded catalogs may return tuples where boundedness is guaranteed.

### 5.5 Problems/errors

Do not freeze a broad exception hierarchy. Public failures use:

```text
Problem
  code: str
  message: str
  retryable: bool | None
  details: mapping
```

Python APIs raise `OrchestratorError` carrying `Problem`. CLI maps `Problem.code` to deterministic exit behavior and stderr diagnostics.

Core generic classes include namespaced meanings such as invalid request, not found, ambiguous, incompatible, unavailable, conflict, stale, permission required, timeout, and cancelled. Modules add their own namespaced codes. Consumers branch on `code`, never message text.

### 5.6 Idempotency and mutation semantics

Methods named `list`, `get`, `observe`, `status`, `preview`, `predict`, `recommend`, `probe`, or equivalent are read-only unless explicitly documented otherwise.

Durable mutation methods return a receipt/identity when retry matters.

- Tracker event recording is idempotent by `EventId`.
- Manual result ingestion is idempotent for the same result artifact/run binding.
- Adapter start creates at most one active execution per `RunId`; ambiguous transport start must reconcile before retry creates another execution.
- Adapter control responses are idempotent by stable control-request identity where the backend permits a deterministic acknowledgement.
- Scheduler admission is idempotent by `RunId` + admission-request fingerprint: exact retry returns the same active admission; a conflicting request for the same run fails with conflict.
- Scheduler reconciliation is idempotent by reconciliation identity and may not double-charge or double-release reservations.

### 5.7 Sync/async boundary

Core, Tracker, benchmark catalog/query, and Scheduler planning services are synchronously callable. Adapter long-running execution uses explicit run handles and event/control methods rather than exposing a backend coroutine/event loop. Implementations may use asyncio internally.

### 5.8 Two-stage API freeze

This architecture freezes semantic roles, method families, mutation/idempotency behavior, required identity dimensions, and inter-module ownership. Each module workplan may finalize exact Pydantic field spelling and private realization only within these semantics. Once that module passes independent Review, its accepted `api.v1`/required `spi.v1` wire/model schema becomes the compatibility floor for later modules.

## 6. Core composition SPI

### 6.1 One extension registry

Core discovers all installed extensions/providers from exactly one entry-point group:

```text
sdp_orchestrator.extensions.v1
```

Do not scan arbitrary directories or import repository/user files as plugins.

### 6.2 Capability identity and service versions

`CapabilityKey` names a semantic service and does **not** embed an API version. Initial first-party keys include:

```text
prompt.render
project.observe
workplan.catalog
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

Version compatibility is represented separately:

```text
CapabilityRequirement
  key: CapabilityKey
  api_spec: version/specifier constraint
  multiplicity: singular | many

CapabilityProvision
  key: CapabilityKey
  api_major: int
  multiplicity: singular | many
```

This removes double-versioning such as `agent.execute.v1` plus `api_major=1`.

### 6.3 Extension manifest

Manifest inspection is side-effect-minimal and may not start subprocesses, perform network I/O, mutate repositories, or migrate storage.

```text
ExtensionManifest
  extension_id
  extension_version
  core_spi_spec
  requires_extensions
  requires_capabilities: tuple[CapabilityRequirement, ...]
  provides_capabilities: tuple[CapabilityProvision, ...]
```

First-party extension IDs are reserved under `sdp.*`. Use `packaging` for version/specifier comparison.

### 6.4 Activation contract

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

`ExtensionContext` exposes only versioned services needed for composition: effective Core configuration plus the provider's namespace, already-activated required services, CLI registrar, config-schema registrar, process-local event publisher/sink registrar, and diagnostics.

Activation is dependency-topological. Incompatible/failed providers disable themselves and dependents while healthy lower capabilities continue.

### 6.5 Service registry and application API

Services register under `CapabilityKey + api_major + provider_id`.

- singular capability: at most one active primary service for one requested major;
- many capability: multiple providers returned in stable provider-ID order;
- registration never silently replaces another singular service.

Core exports:

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, requirement: CapabilityRequirement) -> bool: ...
    def service(self, requirement: CapabilityRequirement) -> object: ...
    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

A missing/disabled/incompatible service returns a structured problem, not an import-time crash. Concrete constructors remain private.

### 6.6 CLI ownership

The first module defining a semantic command owns that command. Later modules extend behavior only through lower-defined hooks/subcommands; they do not replace handlers.

Adapter owns `sdp run`. Scheduler extends omitted/explicit-route admission through Adapter's route-policy SPI.

### 6.7 Configuration registration

Core owns one config resolution path. Extensions contribute exactly one namespaced validated section/default provider. Precedence:

```text
built-in defaults
  -> config/profile
  -> documented environment allowlist
  -> explicit CLI/API override
```

Unknown sections belonging to absent extensions are preserved/diagnosed rather than interpreted. Secrets remain references/environment/approved secret-store inputs.

### 6.8 Event publication

Core owns the generic process-local event publisher. Extension sinks are at-least-once within the process attempt when retry is practical and must therefore be idempotent by `EventId`. Sink failure cannot counterfeit the primary lower-module result; the owning extension reports/degrades its own health as appropriate.

## 7. Core shared records

Core owns only cross-module concepts that exist independently of higher modules.

### 7.1 Stable identifiers

```text
ProjectKey
RunId
EventId
StageRef
CapabilityKey
ExtensionId
```

`RouteId`, model/backend/account/transport/effort identities belong to Adapter API, not Core.

### 7.2 DigestRef

```text
DigestRef
  algorithm
  value
```

Initial canonical algorithm is SHA-256. Consumers do not assume fixed digest length for all future algorithms.

### 7.3 StageRef

Contains protocol profile identity + protocol version + stage key. Stage names remain data rather than closed enums.

### 7.4 WorkplanRef

```text
WorkplanRef
  workplan_id
  protocol_version
  path
  artifact_digest: DigestRef
  semantic_digest: DigestRef
  lifecycle_state
```

Lifecycle-only movement/status bookkeeping may alter path/artifact digest while preserving semantic digest. Substantive authority change alters semantic digest.

### 7.5 CandidateRef

```text
CandidateRef
  repository_id
  branch_or_detached
  head_commit
  working_tree_digest | None
  identity_complete: bool
  upstream_ref | None
  observed_remote_commit | None
  observed_at
```

Material staged/unstaged/untracked source changes alter `working_tree_digest`. If relevant dirty state cannot be fingerprinted confidently, `identity_complete=false`.

### 7.6 ProjectDescriptor versus prompt-safe context

Core must distinguish local execution data from prompt-safe data.

```text
ProjectDescriptor
  project_key
  local_repo_root | None
  sanitized_remote_repository
  configured_mode
  protocol_profile
  configuration_identity
```

`ProjectDescriptor` is local process data for trusted lower/higher modules; it is never automatically embedded into a web prompt.

`PromptProjectSnapshot` contains only execution-mode-safe repository/workplan/candidate context. In web mode it excludes local absolute paths, private state paths, secrets, account/resource telemetry, and credential-bearing remotes.

This distinction prevents Adapter from importing Core config internals merely to obtain a local working directory while preserving the web privacy boundary.

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

Event type values are namespaced/versioned (for example `core.prompt.rendered.v1`). Events are evidence, not workflow authority. Tracker may persist unknown future event types opaquely.

## 8. Core / Prompt Module

### 8.1 Responsibilities

Core owns CLI/application composition, project config/catalog, read-only Git/workplan observation, protocol-profile/stage catalog, canonical prompt loading/substitution, local/web prompt rendering, run/prompt identity, stdout/optional clipboard, and capability/doctor reporting.

Core does not own durable workflow history, next-stage inference from prior results, agent processes, benchmarks, resources, or scheduling.

### 8.2 CoreAPI v1

```python
class CoreAPI(Protocol):
    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]: ...
    def get_project(self, project: ProjectKey) -> ProjectDescriptor: ...
    def list_stages(self, project: ProjectKey) -> tuple[StageDescriptor, ...]: ...
    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...
    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]: ...
    def render(self, request: PromptRequest) -> RenderedPrompt: ...
```

These methods are read-only with respect to target repositories. They may read Git/workplans and explicitly requested read-only remote state but never silently pull/merge/rebase/push/edit.

### 8.3 Observation network policy

Network use is explicit in requests:

```text
ObservationPolicy
  remote_mode: local_only | use_cached_remote | refresh_remote
  max_remote_staleness | None
```

Programmatic default is `local_only` unless the caller/configuration explicitly requests otherwise. Results carry provenance/freshness. `UNKNOWN`/stale is preferable to hidden network I/O or invented freshness.

### 8.4 Workplan catalog

`workplans()` is paginated because archives can grow without bound. It reports active/archive descriptors, exact + semantic fingerprints, lifecycle consistency, and selection evidence. It does not guess among materially plausible workplans by mtime.

`ProjectObservation` includes the current workplan resolution state when one is unambiguous/configured; ambiguity remains explicit.

### 8.5 PromptRequest v1 semantics

```text
project: ProjectKey
stage: StageRef
execution_mode: local | web
workplan_selector: optional explicit selector
first_task: optional description for workplan-free Design
input_overrides: declared prompt input -> value
observation_policy: optional ObservationPolicy
```

Execution mode is an extensible data value; v1 validates at least `local` and `web`.

### 8.6 RenderedPrompt v1

```text
run_id: RunId
prompt_text
prompt_fingerprint: DigestRef
stage: StageRef
prompt_source: PromptSourceRef
resolved_inputs + provenance
prompt_context: PromptProjectSnapshot
selected_workplan: WorkplanRef | None
```

`prompt_text` is the complete copy/paste artifact. Diagnostics/recommendations are not inserted into prompt stdout.

### 8.7 Prompt fingerprint v1

Core renders the full prompt using a fixed fingerprint placeholder after `RunId` is known, computes SHA-256 over exact UTF-8 bytes of that placeholder-form artifact, then substitutes `sha256:<hex>`. The placeholder token/normalization rule are frozen by WP-1 compatibility fixtures. A future scheme uses a new explicit fingerprint scheme/version.

### 8.8 Core-only CLI

```text
sdp prompt <stage>
sdp design
sdp implementation
sdp review
... compatible stage aliases ...
sdp projects
sdp capabilities
sdp doctor
```

Prompt command stdout contains only the complete prompt. Ambiguous workplans require bounded explicit selection. Core must operate offline from a compatible packaged prompt snapshot when local information is sufficient.

### 8.9 Core dependencies

Expected: `platformdirs`, `typer`, `pydantic`, `python-frontmatter`, `packaging`. Clipboard may be an optional `pyperclip` extra. Core does not require `filelock`, ACP, `httpx`, ML, or higher modules.

## 9. Tracker Module

### 9.1 Responsibilities

Tracker owns user-local SQLite history/migrations, run/event history, prompt/output association, manual result ingestion, workplan history, derived development projection, stale/ambiguous evidence handling, next-action recommendation, history/workplan/graph interfaces, retention/export/purge, and storage coordination for higher modules.

Tracker does not run agents or rank online benchmarks.

### 9.2 TrackerAPI v1

```python
class TrackerAPI(Protocol):
    def record(self, event: EventEnvelope) -> RecordReceipt: ...
    def ingest(self, request: IngestRequest) -> IngestResult: ...
    def status(self, request: StatusRequest) -> DevelopmentProjection: ...
    def next_action(self, request: NextActionRequest) -> NextAction: ...
    def get_run(self, run_id: RunId) -> TrackedRun: ...
    def history(self, query: HistoryQuery) -> Page[RecordedEvent]: ...
```

`StatusRequest`/`NextActionRequest` include project + observation policy so callers control remote freshness/network cost. Tracker reconciles current public Core observations before current-state claims.

`record` is idempotent by `EventId`. `ingest` binds to Core `RunId` + prompt fingerprint and is idempotent for the exact same result artifact. Wrong-run/ambiguous results fail safely or require explicit bounded confirmation.

### 9.3 RecordedEvent

History exposes Tracker recording order separately from producer wall clock:

```text
RecordedEvent
  sequence: monotonically increasing Tracker-local integer
  recorded_at
  event: EventEnvelope
```

This makes replay/history deterministic even when producer clocks differ. `occurred_at` remains source provenance, not the sole total-order authority.

### 9.4 DevelopmentProjection

The projection is bounded current/summary state, not full history. It minimally identifies current candidate/workplan/protocol, stage attempts/outcomes summary, stale/ambiguous/inconsistent evidence, current blockers, recommended next stage/action with reason codes, and observation freshness. Detailed attempts remain in history.

Execution status and semantic outcome are separate.

### 9.5 Tracker storage

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/
  exports/
```

SQLite/WAL is v1 durable control storage. `filelock` begins here for migration/process coordination and later run ownership.

### 9.6 TrackerStorageSPI v1

```python
class TrackerStorageSPI(Protocol):
    def register_migrations(self, extension: ExtensionId, migrations: tuple[MigrationSpec, ...]) -> None: ...
    def transaction(self, extension: ExtensionId, *, write: bool) -> ContextManager[sqlite3.Connection]: ...
```

Tracker owns DB opening/configuration, migration ordering, backup/recovery policy, and transaction boundaries. Extensions own namespaced tables and may not alter/read another module's semantic tables directly; cross-module semantic reads use APIs. SQLite is honestly part of this SPI major. Scheduler may use transactions across its own resource/reservation tables atomically.

### 9.7 Tracker CLI

```text
sdp status
sdp next
sdp ingest ...
sdp history
sdp workplans
sdp use <workplan>
sdp graph ...
```

Without Tracker these commands need not exist; Core remains fully functional.

## 10. Adapter Module

### 10.1 Responsibilities

Adapter owns agent/backend/account/model/effort route identity, manual/direct delivery modes, structured transports, execution lifecycle, benchmark-source providers/cache/identity resolution, static capability recommendation, route probing, and automatic tracking of direct/manual-run state through Tracker.

It does not own resource ledgers or quota-aware selection.

### 10.2 Adapter-owned route identities

Adapter `api.v1` owns:

```text
RouteId
ModelRef
BackendRef / HarnessRef
AccountRef
TransportRef
EffortRef
ObservedExecutionIdentity
```

`RouteId` is a stable configured opaque key, not a hash of mutable display fields.

### 10.3 ExecutionRoute v1

A route is configured execution identity:

```text
ExecutionRoute
  route_id
  backend
  account
  transport
  model
  effort
  delivery_mode: direct | manual_handoff
  repository_access: local_worktree | remote_connector | other supported data value
  configured capability metadata
```

Manual-web routes are first-class. They can participate in recommendation and later Scheduler AUTO selection. They do not pretend to be direct subprocess routes.

### 10.4 AdapterAPI v1

```python
class AdapterAPI(Protocol):
    def routes(self, query: RouteQuery | None = None) -> Page[ExecutionRoute]: ...
    def probe(self, route: RouteId) -> RouteCapabilitySnapshot: ...
    def benchmarks(self, query: BenchmarkQuery) -> Page[BenchmarkObservation]: ...
    def recommend(self, request: RecommendationRequest) -> RecommendationSet: ...
    def start(self, request: AgentExecutionRequest) -> AgentRunHandle: ...
    def events(self, request: AgentEventQuery) -> Page[AgentEvent]: ...
    def respond(self, request: AgentControlResponse) -> AgentControlReceipt: ...
    def cancel(self, run_id: RunId) -> AgentControlReceipt: ...
    def wait(self, request: AgentWaitRequest) -> AgentRunResult: ...
```

### 10.5 AgentExecutionRequest and route policy

Request includes Core `RenderedPrompt` binding, optional requested `RouteId`, expected project/candidate, interaction/permission policy, and whether manual handoff is allowed.

If no active route-policy provider exists:

- explicit route is used;
- otherwise an explicit user-configured default may be used;
- otherwise return route-required; Adapter does not choose the highest benchmark automatically.

If a route-policy provider is active, Adapter consults it for **every** execution:

- explicit route: provider validates/admit/reserves that exact route; it may reject but may not substitute another route;
- no route: provider may select/admit a route according to its policy (Scheduler AUTO);
- provider returns an opaque admission reference carried through terminal reconciliation.

This resolves both AUTO routing and explicit-route resource safety without command replacement.

### 10.6 Manual handoff lifecycle

For `delivery_mode=manual_handoff`, `start` does not spawn an agent process. It uses the existing Core/Tracker prompt/run binding and returns an `AgentRunHandle` in an awaiting-external-result state plus a `ManualHandoffArtifact` suitable for clipboard/stdout presentation.

The user supplies the external response through Tracker ingestion. Adapter/Tracker can then expose terminal result state for the run. `wait` may observe completion or timeout; unsupported direct control operations return a structured problem rather than fabricating a local process.

Thus manual mode remains usable without Adapter, while Adapter can represent it uniformly once installed and Scheduler can later select it.

### 10.7 Direct execution lifecycle

For direct routes, `start` returns promptly with a stable handle, `events` yields normalized user/tool/permission/status events via cursor pages, `respond` addresses stable control-request IDs, `cancel` is idempotent, and `wait` returns terminal result or timeout without implicitly destroying the underlying run.

One `RunId` has at most one concurrently active Adapter execution. Ambiguous start/crash must reconcile before another execution is created.

### 10.8 AgentRunResult v1

Terminal result separates execution terminal status from agent-reported workflow semantics. It includes run/route identity, configured route, `ObservedExecutionIdentity` with confidence/provenance, backend/session identity where available, final visible response, structured result when available, candidate observations, interruption/failure class, transport telemetry, and Tracker-ingestion evidence.

Configured/planned model identity and observed actual identity remain separate, especially for manual web products whose serving/model routing may not be externally confirmable.

A zero process exit never manufactures workflow PASS.

### 10.9 Agent transport SPI v1

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

Prefer ACP when sufficiently conformant; use documented native structured RPC/SDK/JSON when needed. PTY scraping is not primary when structured transport exists. Initial backend families remain Claude, Codex, OMP, Pi, and Antigravity.

### 10.10 Route-policy SPI v1

```python
class RoutePolicyProvider(Protocol):
    def preview(self, request: RoutePolicyRequest) -> RoutePolicyDecision: ...
    def admit(self, request: RoutePolicyRequest) -> RouteAdmission: ...
    def reconcile(self, request: RoutePolicyReconciliation) -> RoutePolicyReceipt: ...
```

`RoutePolicyRequest` includes `RunId`, stage/task identity, configured candidate context, requested route if any, and interaction/manual-handoff constraints.

- preview is read-only;
- admit may reserve/mutate;
- explicit requested route is either admitted unchanged or rejected;
- omitted route may be selected by provider;
- reconciliation is idempotent.

Without provider, Adapter remains explicit/default-route only.

### 10.11 Benchmark source SPI and observations

```python
class BenchmarkSourceProvider(Protocol):
    def descriptor(self) -> BenchmarkSourceDescriptor: ...
    def fetch(self, request: BenchmarkFetchRequest) -> RawBenchmarkSnapshot: ...
    def normalize(self, raw: RawBenchmarkSnapshot) -> BenchmarkSnapshot: ...
```

Snapshots preserve source identity/schema/version, fetched/generated timestamps, content digest/ETag, source/license/attribution metadata, and contextual observations.

Observation preserves metric/direction/value/unit, uncertainty, external model identity, effort, harness/configuration, benchmark version, freshness, and internal identity-match quality.

### 10.12 Artificial Analysis

Preferred general-intelligence source is the official Artificial Analysis Data API. Current endpoint/version details are adapter defaults, not Frozen architecture. Preserve API/index version, stable upstream identity, source freshness, rate/error semantics, private API-key handling, attribution/licensing, and last-known-good/unavailable behavior. Never fabricate a score.

### 10.13 DeepSWE

Preferred coding evidence is current DeepSWE data. Treat results as harness + model + effort/config observations. Preserve match quality:

```text
EXACT_CONFIG_MATCH
MODEL_EFFORT_PROXY
MODEL_ONLY_PROXY
UNRESOLVED
```

A score from one harness is not relabeled as measured success of another. Endpoint/schema changes fail clearly and are handled by provider updates.

### 10.14 Recommendation policy

Design/architecture/difficult diagnosis prioritize current general-intelligence evidence among eligible routes. Implementation/repair prioritize current DeepSWE/coding evidence, exact configuration first. Review/Verification prioritize high general intelligence and may display provider/model independence as a secondary signal.

Do not invent a universal scalar combining incompatible Intelligence Index and DeepSWE measures. Missing evidence is UNSCORED, not zero.

### 10.15 Adapter CLI

```text
sdp agents
sdp routes
sdp benchmarks ...
sdp models
sdp recommend <stage>
sdp run <stage> --route <route-id>
```

A manual route may make `sdp run` produce/copy a handoff artifact and mark the run awaiting external result instead of launching a process.

## 11. Scheduler Module

### 11.1 Responsibilities

Scheduler owns resource ledgers/meters, pricing/opaque quota representation, reset/window inference, global reservations/uncertainty holds, usage attribution, task features, usage/outcome prediction, future-stage reserves, route admission/scoring, AUTO selection, and quota/provider interruption rescheduling.

Scheduler never launches agents directly.

### 11.2 SchedulerAPI v1

```python
class SchedulerAPI(Protocol):
    def resources(self, query: ResourceQuery | None = None) -> ResourceProjection: ...
    def usage(self, query: UsageQuery) -> Page[UsageRecord]: ...
    def predict(self, request: PredictionRequest) -> UsagePrediction: ...
    def preview(self, request: ScheduleRequest) -> ScheduleDecision: ...
    def admit(self, request: ScheduleRequest) -> AdmissionDecision: ...
    def reconcile(self, request: ReservationReconciliationRequest) -> ReservationReconciliation: ...
```

Preview is read-only. Admit atomically re-observes required resource state, revalidates feasibility, selects/validates route, and creates required reservations in one DB transaction.

### 11.3 ScheduleRequest explicit versus AUTO

`ScheduleRequest` includes `RunId`, project/stage/task features, optional requested `RouteId`, interaction/manual-handoff constraints, candidate/workplan identity, and policy overrides.

- requested route present: evaluate that exact route only; do not replace it with a cheaper/better route;
- requested route absent: AUTO may choose among feasible routes;
- manual-handoff route is feasible only when the request permits user-mediated handoff;
- direct route is required for unattended execution unless another supported automatic transport exists.

### 11.4 Admission idempotency

Admission computes an `admission_request_fingerprint` over all semantics that affect feasibility/reservation. `admit` is idempotent for `(RunId, fingerprint)`: exact retry returns the same live admission/reservation identities. A different fingerprint for the same run while admission is active returns conflict unless the old admission has been explicitly reconciled/cancelled according to policy.

This prevents duplicate reservations after caller/transport retry ambiguity.

### 11.5 AdmissionDecision

Records selected route, run/project/stage/task identity, admission/fingerprint, decision time, binding resource observations/freshness, prediction quantiles, reservation IDs/amounts, rejected alternatives/reasons, score/explanation components, and expiration/revalidation conditions.

### 11.6 Resource model

Routes consume zero or more Scheduler-owned ledgers. Ledgers preserve allowance visibility, expiration, reset/window semantics, funding behavior, source/provenance/freshness, and reservations/uncertainty holds.

`UNMETERED_FOR_SCHEDULER`, `METERED`, and `UNKNOWN` are distinct. Shared account quota is represented once and referenced by all consuming routes. Dual windows are simultaneous constraints. Opaque quota remains in observed provider units; PAYG uses versioned pricing rather than invented token equivalents for opaque quota.

### 11.7 Meter SPI

```python
class AccountMeterProvider(Protocol):
    def descriptor(self) -> MeterDescriptor: ...
    def observe(self, request: MeterRequest) -> MeterSnapshot: ...
```

Prefer official/machine-readable sources. Browser scraping is not normal. Observations preserve source, unit, time/freshness, confidence, and account identity.

### 11.8 Reservation/reconciliation

Before metered direct execution, admit reserves predicted capacity on every consumed ledger atomically. Manual unmetered routes may need no quota reservation but still produce an admission record when Scheduler selected them.

If execution dies before final meter state is known, preserve uncertainty holds rather than releasing as zero usage. Provider hard-limit/current meter observations outrank stale predictions.

Reconciliation is idempotent and correlates planned route with observed execution identity where available.

### 11.9 Prediction

Predict distributions for runtime, consumption per ledger, billable token categories where relevant, monetary cost, probability of stage-quality completion, interruption probability, and future repair rounds.

Cold start uses interpretable priors by stage/role x model x effort x backend/transport with project corrections. Early learning uses empirical quantiles/EWMA/shrinkage without mandatory ML. Persist calibration evidence. Optimize expected resource/cash cost to accepted stage completion, not merely first-call use.

### 11.10 Scheduling policy

AUTO is default omitted-route policy only when Scheduler is active. Hard feasibility precedes ranking. Feasibility includes capability/effort, tools/skills, repository access, privacy/security, session independence, backend health, interaction constraints, predicted capacity, and protected future Review/Design reasoning reserve.

Ranking may consider quality-completion probability, interruption risk, future reasoning capacity, expiring quota opportunity cost, PAYG cost, manual handoff/continuity, independence/diversity, and latency. Decisions remain explainable.

### 11.11 Adapter integration

Scheduler implements Adapter `RoutePolicyProvider`:

- Adapter passes requested route or AUTO request;
- Scheduler preview/admit validates explicit route or chooses omitted route;
- Adapter executes/directs manual handoff using returned route/admission ref;
- Adapter terminal/manual ingestion reconciliation returns to Scheduler;
- Scheduler reconciles resource/usage state.

Scheduler therefore never replaces `sdp run` and Adapter never imports Scheduler.

### 11.12 Persistence

Scheduler adds namespaced tables/migrations to the Tracker-owned user-global SQLite DB through Tracker SPI. Quota/account state is global across projects. Scheduler does not modify Tracker workflow tables directly.

## 12. Configuration ownership

Core owns canonical config loading and `ProjectKey`. Extensions contribute namespaced validated sections.

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
# ledgers/meters/prediction/admission policy
```

Unknown absent-extension sections are preserved/diagnosed. Secrets remain references or approved secret inputs, never ordinary history/config snapshots.

## 13. Persistence and event ownership

Core is stateless across invocations except configuration and bounded prompt/cache artifacts.

Tracker introduces persistence. Higher modules extend it through Tracker SPI.

- one SQLite DB may contain multiple extension table families, each with one semantic owner;
- only the owner writes its tables;
- semantic cross-module reads use APIs;
- migration order follows dependency order;
- removing a higher extension leaves lower data readable/functional;
- raw prompt/output and numeric telemetry have separable retention;
- persisted state remains private local evidence, not repository authority.

## 14. CLI capability behavior

### Core only

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
sdp graph
```

### + Adapter

```text
sdp recommend <stage>
sdp routes
sdp benchmarks ...
sdp run <stage> --route <id>
```

No resource-aware AUTO exists. Manual routes are valid explicit/default routes.

### + Scheduler

```text
sdp resources
sdp usage
sdp predict <stage> [--route <id>]
sdp schedule <stage> --explain
sdp run <stage>
```

With Scheduler active, omitted route may AUTO-select. Explicit route bypasses ranking but not configured hard compatibility/resource admission.

Failure of Scheduler must not make Adapter explicit/manual route operation unavailable when resource policy permits downgrade. Failure of Adapter disables dependent Scheduler but leaves Tracker/Core manual operation.

## 15. Failure/degradation rules

```text
Scheduler unavailable
  -> Adapter explicit/default routes + benchmark recommendation

one direct transport unavailable
  -> disable that direct route; manual/other direct routes remain

Adapter unavailable
  -> Tracker manual copy/paste remains

Tracker DB unavailable/corrupt
  -> Tracker/Adapter/Scheduler report unavailable
  -> Core prompt rendering remains
```

A module advertises only capabilities whose semantic contract is actually healthy.

## 16. Security and privacy

- Plugin entry points are trusted installed code, not a sandbox.
- Manual pasted agent output, structured agent results, benchmark/meter responses, and remote metadata are untrusted data: bound size/time/schema before persistence/use and never execute instructions from them as control commands.
- API keys/tokens never enter prompts, benchmark caches, events, logs, or repository files.
- Web prompt context excludes local absolute paths/private state/account/resource telemetry/credential-bearing remotes.
- ProjectDescriptor local paths remain local process data.
- Agent subprocesses use direct argv/structured transports with explicit permission handling; no dangerous permission bypass by default.
- Historical transcripts are not automatically re-injected into future prompts; only bounded structured projection is automatic.
- Benchmark source licensing/attribution metadata travels with cached observations.

## 17. Benchmark recommendation integrity

Every recommendation using online evidence is reconstructible from source snapshots/observations. Display/record source, metric, version, generated/fetched time, model + effort + harness/config, value/uncertainty, identity-match quality, and staleness when material.

Do not compare incompatible benchmark/index versions as a stable scale. Do not combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into one universal scalar absent separate validated design.

## 18. Executable architecture fitness

Once packages exist, static checks enforce:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core public API/SPI only
Adapters    may import Core + Tracker public API/SPI only
Scheduler   may import Core + Tracker + Adapters public API/SPI only
```

Also check native PEP 420 namespace packaging, one extension entry-point group, no private cross-module imports, and single ownership of `sdp run`.

## 19. Module acceptance ladder

Each module is implemented, independently reviewed, and accepted before the next workplan begins.

### WP-1 Prompt

Must prove Core-only install/CLI; project catalog/descriptor; read-only local observation/workplan paging; explicit remote observation policy; prompt rendering and privacy; ambiguous workplans not guessed; RunId/fingerprint scheme; composition with no extensions; API/SPI serialization/error/idempotency fixtures; no higher imports/persistence.

### WP-2 Tracker

Must re-prove Prompt standalone with/without Tracker plus event/result idempotency, correct run association, fresh Core observation through public API, deterministic RecordedEvent pagination, bounded development projection, persistence/restart, storage SPI/migrations/ownership, and Core usability when Tracker disabled/deleted.

### WP-3 Adapter

Must re-prove lower acceptance plus direct and manual-handoff route lifecycles, explicit route/default behavior, route-policy SPI with no provider and fake provider, start/events/respond/cancel/wait semantics, planned versus observed execution identity, automatic tracking, benchmark provenance/identity mapping/failure degradation, capability recommendation separation, and no quota-aware selection.

### WP-4 Scheduler

Must re-prove lower acceptance plus read-only preview, atomic/idempotent admit, explicit-route validation without substitution, omitted-route AUTO, manual-handoff route scheduling, shared/dual-window ledgers, cross-project reservation, UNMETERED versus UNKNOWN, prediction/calibration, future-review reserve, PAYG/expiring quota behavior, idempotent reconciliation/uncertainty holds, Adapter route-policy integration, and Scheduler disablement restoring Adapter behavior.

## 20. Lossless module-workplan derivation

Implementation order is Frozen:

```text
WP-1 Prompt Module
WP-2 Tracker Module
WP-3 Adapter Module
WP-4 Scheduler Module
```

Each workplan declares:

```text
parent_architecture: orchestrator/docs/architecture.md
parent_architecture_version: 1.2.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

Each workplan carries relevant parent invariants, module responsibilities/non-responsibilities, exact lower API/SPI contracts consumed, public API/SPI it must establish, affected/acceptance surface, standalone acceptance with higher modules absent, compatibility acceptance with lower modules present, and simplification/reopen triggers.

Do not pre-implement later modules merely for future convenience. The API/SPI seams and stable IDs here are the justified future-facing surface.

## 21. Versioning and evolution

Architecture versioning:

- major: breaks module ladder, authority model, dependency direction, or public API role boundaries;
- minor: backward-compatible architecture/API strengthening before/alongside module adoption;
- patch: clarification without semantic change.

1.2.0 supersedes 1.1.0 because this second pre-implementation review materially strengthened route/capability/project/admission contracts before WP-1.

Module package versions are independent and declare compatible lower API/SPI majors.

New benchmark sources normally implement Adapter SPI; new direct transports implement Adapter SPI; new meter/pricing sources implement Scheduler SPI. Ordinary provider/API churn, new models, benchmark versions, agent flags, and predictor algorithms do not reopen this parent architecture unless a Frozen boundary proves insufficient.

## 22. Active simplicity and redesign triggers

Reopen/simplify before adding machinery if implementation creates multiple plugin loaders, reverse dependencies, duplicated CLI composition, separate mutable workflow authority, benchmark fields in Core, quota abstractions below Scheduler, duplicated model identity mapping, backend-specific workflow logic, Scheduler-owned process execution, private SQL/process objects in public APIs, hidden writes in preview/query calls, or stubs whose only purpose is preserving a broken higher layer instead of clean downgrade.

Reopen parent architecture only when evidence shows a Frozen boundary cannot satisfy the product: a required reverse dependency, single registry insufficiency, public API role incapable of supporting the next module without semantic break, or execution lifecycle unable to represent a required backend safely.

## 23. Second pre-implementation review — 2026-09-07

This pass challenged 1.1.0 as if WP-2 through WP-4 already depended on it. Material gaps closed:

1. **Capability double-versioning:** capability keys are now semantic/unversioned; API version is separate in requirement/provision records.
2. **Provider compatibility discovery:** manifests now declare provided capability API majors, allowing dependency compatibility before activation.
3. **Core future-type leakage:** `RouteId` moved from Core shared identifiers to Adapter API ownership.
4. **Project execution-context gap:** Core now exposes trusted local `ProjectDescriptor` separately from prompt-safe `PromptProjectSnapshot`, so Adapter can obtain worktree location without Core-private imports or leaking it to web prompts.
5. **Project/workplan query growth:** project/workplan catalogs are paginated where they can grow.
6. **Hidden network-I/O ambiguity:** repository/status APIs now carry explicit observation policy/freshness instead of silently refreshing remotes.
7. **Tracker history ordering:** Tracker exposes recording sequence separately from producer wall-clock time.
8. **Manual-web route gap:** manual handoff is a first-class Adapter route/delivery mode and can later participate in Scheduler AUTO selection.
9. **Planned-versus-observed identity:** route configuration is separated from actual observed execution/model identity, essential for manual web and provider-side routing.
10. **Explicit-route admission contradiction:** Scheduler policy now applies to every Adapter execution when active; explicit routes are validated/reserved unchanged, while only omitted routes may be selected automatically.
11. **Admission retry race:** Scheduler admit/reconcile semantics are idempotent and fingerprinted, preventing duplicate reservations after ambiguous retries.
12. **Untrusted manual output boundary:** pasted/structured agent output is explicitly treated as untrusted data rather than executable control input.

No remaining architecture-level blocker was found after these corrections. The architecture is sufficiently specific to derive WP-1 through WP-4 without private cross-module coupling while leaving module-local algorithms/classes delegated.

## 24. Design verdict

**PASS — architecture 1.2.0 is implementation-ready.**

The next active implementation contract should be WP-1 Prompt Module only. WP-1 establishes Core, CLI/composition, Core API/SPI v1, project/repository/workplan observation, canonical prompt rendering, and prompt identity. It must not introduce Tracker persistence, agent integration, benchmark networking, or Scheduler/resource machinery.
