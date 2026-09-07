---
kind: architecture
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.3.0
supersedes_architecture_version: 1.2.0
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
14. **Read-only query and durable mutation are visibly distinct.** Preview/query calls may not hide durable writes. Scheduler `preview` is read-only; admission is atomic and reserving.
15. **Long-running execution is explicit.** Agent execution supports admission, start, event observation, control/permission response, cancellation, and terminal result without exposing one backend's async/session implementation.
16. **Manual and direct routes share one route vocabulary.** A web/manual route is not a failed local route. It is a first-class route with different delivery, prompt-context, and repository-access capabilities.
17. **Capability identity is independent of API version.** Semantic capability keys do not embed `v1`; API compatibility is represented separately.
18. **Explicit route choice is not an admission bypass.** With Scheduler active, an explicitly requested route bypasses ranking but still undergoes configured hard feasibility/resource admission. It may be rejected but not silently substituted.
19. **Route admission precedes final prompt rendering.** The selected route determines prompt context (`local`, `web`, or future mode), so AUTO/explicit route admission must be resolved before the final prompt is rendered for execution.
20. **Run identity precedes both scheduling and rendering.** Core can allocate a `RunId` without persistence so Scheduler admission, prompt rendering, Tracker history, and Adapter execution refer to the same attempt.
21. **Manual result tracking has a structured compatibility seam from day one.** Core prompts request a versioned result envelope carrying run/fingerprint identity. Tracker can later ingest it without changing the Prompt API.

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

Adds persistent development history, prompt/output association, manual response ingestion, current development projection, active/retired workplan history, PASS/NO-PASS and stale-evidence handling, next-action recommendation, persistent user workplan selection, and text/JSON/graph query surfaces.

All agent I/O may remain manual.

### 3.3 Level 2 — Adapters

Adds configured routes, direct structured agent integration, manual-web handoff routes, one-command execution of a selected route, online benchmark collection, and static capability recommendation.

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

Persisted schema, event schema, benchmark-source schema, digest/canonicalization schemes, and API major versions are independent dimensions.

### 5.3 Public records

Cross-module request/response records are immutable-by-convention value objects with JSON-compatible serialization. Pydantic is the initial implementation technology but not the semantic contract.

Rules:

- timestamps serialize as timezone-aware ISO-8601 UTC;
- IDs serialize as opaque strings;
- digests preserve cryptographic algorithm and canonicalization scheme;
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

Public failures use one stable envelope rather than a broad exception hierarchy:

```text
Problem
  code: str
  message: str
  retryable: bool | None
  details: mapping
```

Python APIs raise `OrchestratorError` carrying `Problem`. CLI maps `Problem.code` to deterministic exit behavior/stderr diagnostics. Modules add namespaced codes; consumers branch on code, not message text.

### 5.6 Idempotency and mutation semantics

Methods named `list`, `get`, `observe`, `status`, `preview`, `predict`, `recommend`, `probe`, or equivalent are read-only unless explicitly documented otherwise.

Durable mutation methods return a receipt/identity when retry matters.

- Tracker event recording is idempotent by `EventId`.
- Manual result ingestion is idempotent for the same result artifact/run binding.
- Tracker workplan selection is idempotent for the same project/selection binding.
- Adapter admission is idempotent for the same run/admission request.
- Adapter start creates at most one active execution per `RunId`; ambiguous transport start must reconcile before retry creates another execution.
- Adapter control responses are idempotent by stable control-request identity where the backend supports deterministic acknowledgement.
- Scheduler admission is idempotent by `RunId` + admission-request fingerprint; exact retry returns the same active admission, conflicting retry fails.
- Scheduler release/reconciliation are idempotent and may not double-release/double-charge reservations.

### 5.7 Sync/async boundary

Core, Tracker, benchmark catalog/query, Adapter admission, and Scheduler planning/admission services are synchronously callable. Adapter long-running execution uses explicit handles/event/control methods rather than exposing backend coroutine/event loops. Implementations may use asyncio internally.

### 5.8 Two-stage API freeze

This architecture freezes semantic roles, method families, mutation/idempotency behavior, required identity dimensions, and inter-module ownership. Each module workplan may finalize exact Pydantic field spelling and private realization only within these semantics. Once a module passes independent Review, its accepted `api.v1`/required `spi.v1` schemas become the compatibility floor for later modules.

## 6. Core composition SPI

### 6.1 One extension registry

Core discovers all installed extensions/providers from exactly one entry-point group:

```text
sdp_orchestrator.extensions.v1
```

Do not scan arbitrary directories or import repository/user files as plugins.

### 6.2 Capability identity and service versions

`CapabilityKey` names a semantic service and does not embed an API version. Initial first-party keys:

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

Version compatibility is separate:

```text
CapabilityRequirement
  key: CapabilityKey
  api_spec
  multiplicity: singular | many

CapabilityProvision
  key: CapabilityKey
  api_major
  multiplicity: singular | many
```

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

`ExtensionContext` exposes only versioned services needed for composition: effective Core config plus provider namespace, already-activated required services, CLI registrar, config-schema registrar, process-local event publisher/sink registrar, and diagnostics.

Activation is dependency-topological. Incompatible/failed providers disable themselves and dependents while healthy lower capabilities continue.

### 6.5 Service registry/application API

Services register under `CapabilityKey + api_major + provider_id`. Singular capabilities have one active primary service for a requested major; multi-provider capabilities return stable provider-ID ordering; registration never silently replaces a singular service.

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, requirement: CapabilityRequirement) -> bool: ...
    def service(self, requirement: CapabilityRequirement) -> object: ...
    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

Missing/disabled/incompatible capability returns a structured problem, not import-time crash.

### 6.6 CLI ownership

The first module defining a semantic command owns it. Later modules extend behavior through lower-defined hooks/subcommands, not handler replacement. Adapter owns `sdp run`; Scheduler extends route admission through Adapter route-policy SPI.

### 6.7 Configuration registration

Core owns one config resolution path. Extensions contribute one namespaced validated section/default provider. Precedence is defaults -> config/profile -> documented environment allowlist -> explicit CLI/API override. Unknown absent-extension sections are preserved/diagnosed. Secrets remain references/approved secret inputs.

### 6.8 Event publication

Core owns a generic process-local event publisher. Extension sinks are at-least-once within a process attempt when retry is practical and are idempotent by `EventId`. Sink failure cannot counterfeit a primary lower-module result.

## 7. Core shared records

Core owns only concepts existing independently of higher modules.

### 7.1 Stable identifiers

```text
ProjectKey
RunId
EventId
StageRef
CapabilityKey
ExtensionId
```

Route/model/backend/account/transport/effort identities belong to Adapter API, not Core.

### 7.2 DigestRef

```text
DigestRef
  algorithm: str
  canonicalization_scheme: str | None
  value: str
```

Initial cryptographic algorithm is SHA-256. Domain digests that depend on canonicalization must carry a versioned scheme such as `sdp.prompt-fingerprint.v1`, `sdp.workplan-semantic.v1`, or `sdp.git-working-tree.v1`. Changing canonicalization without changing the scheme is forbidden.

### 7.3 StageRef

Contains protocol profile identity + protocol version + stage key. Stage names remain data rather than closed enums.

### 7.4 WorkplanRef

```text
WorkplanRef
  workplan_id
  protocol_version
  path
  artifact_digest: DigestRef
  semantic_digest: DigestRef | None
  semantic_identity_complete: bool
  lifecycle_state
```

Semantic identity is protocol-profile/schema aware and deterministic; it does not use an LLM to guess what text is semantic. Lifecycle-only movement/status may preserve semantic digest. When the profile cannot confidently distinguish lifecycle-only fields from authority, set `semantic_identity_complete=false`; Tracker then invalidates conservatively on artifact change rather than manufacturing equivalence.

### 7.5 CandidateRef

```text
CandidateRef
  repository_id
  branch_or_detached
  head_commit
  working_tree_digest: DigestRef | None
  identity_complete: bool
  upstream_ref | None
  observed_remote_commit | None
  observed_at
```

Material staged/unstaged/untracked source changes alter the versioned working-tree digest. If relevant dirty state cannot be fingerprinted confidently, `identity_complete=false`.

### 7.6 ProjectDescriptor versus prompt-safe context

```text
ProjectDescriptor
  project_key
  local_repo_root | None
  sanitized_remote_repository
  configured_mode
  protocol_profile
  configuration_identity
```

`ProjectDescriptor` is trusted local-process data and is not automatically embedded in web prompts.

`PromptProjectSnapshot` contains only execution-mode-safe repository/workplan/candidate context. Web mode excludes local absolute paths, private state, secrets, account/resource telemetry, and credential-bearing remotes.

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

Event types are namespaced/versioned. Events are evidence, not workflow authority. Tracker may persist unknown future event types opaquely.

### 7.8 StageResultEnvelope v1

Core defines the minimum structured result contract requested in every rendered prompt so future Tracker/Adapter integration does not require changing Prompt semantics:

```text
StageResultEnvelope
  schema_version
  run_id
  prompt_fingerprint
  stage
  outcome
  recommended_next_stage | None
  blockers: tuple[structured summary, ...]
  completed_obligations: tuple[str, ...]
  pending_obligations: tuple[str, ...]
  checks_executed: tuple[structured summary, ...]
  checks_unavailable: tuple[structured summary, ...]
  candidate: CandidateRef | None
  summary: str | None
```

Outcome/stage/check status values are extensible strings, not closed enums. The envelope is reported evidence, not authority. Core only requests/renders the schema; it does not persist or interpret result semantics.

## 8. Core / Prompt Module

### 8.1 Responsibilities

Core owns CLI/application composition, project config/catalog, read-only Git/workplan observation, protocol-profile/stage catalog, canonical prompt loading/substitution, local/web prompt rendering, run/prompt/result-envelope identity, stdout/optional clipboard, and capability/doctor reporting.

Core does not own durable workflow history, next-stage inference, agent processes, benchmarks, resources, or scheduling.

### 8.2 CoreAPI v1

```python
class CoreAPI(Protocol):
    def allocate_run_id(self) -> RunId: ...
    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]: ...
    def get_project(self, project: ProjectKey) -> ProjectDescriptor: ...
    def list_stages(self, project: ProjectKey) -> tuple[StageDescriptor, ...]: ...
    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...
    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]: ...
    def render(self, request: PromptRequest) -> RenderedPrompt: ...
```

`allocate_run_id` creates an opaque non-secret identifier only; it performs no persistence. `render` accepts an optional caller-supplied `RunId`; if absent, Core allocates one.

All methods are read-only with respect to target repositories. They may perform explicitly requested read-only remote observation but never silently pull/merge/rebase/push/edit.

### 8.3 Observation policy

```text
ObservationPolicy
  remote_mode: local_only | use_cached_remote | refresh_remote
  max_remote_staleness | None
```

Programmatic default is `local_only` unless explicitly configured/requested otherwise. Results carry provenance/freshness. Unknown/stale is preferable to hidden network I/O or invented freshness.

### 8.4 Workplan catalog

`workplans()` is paginated because archives can grow. It reports active/archive descriptors, exact + semantic identity completeness, lifecycle consistency, and selection evidence. It does not guess materially ambiguous plans by mtime.

### 8.5 PromptRequest v1

```text
run_id: RunId | None
project: ProjectKey
stage: StageRef
execution_mode: local | web | future compatible data value
workplan_selector: optional explicit selector
first_task: optional description for workplan-free Design
input_overrides
observation_policy: optional ObservationPolicy
```

### 8.6 RenderedPrompt v1

```text
run_id
prompt_text
prompt_fingerprint: DigestRef
stage
prompt_source
resolved_inputs + provenance
prompt_context: PromptProjectSnapshot
selected_workplan: WorkplanRef | None
requested_result_schema: StageResultEnvelope schema identity
```

`prompt_text` is the complete copy/paste artifact. Diagnostics/recommendations are not inserted into prompt stdout.

### 8.7 Prompt fingerprint v1

Core renders the full prompt using a fixed fingerprint placeholder after `RunId` is known, computes SHA-256 over exact UTF-8 bytes of that placeholder-form artifact under canonicalization scheme `sdp.prompt-fingerprint.v1`, then substitutes `sha256:<hex>`. WP-1 freezes the literal placeholder and byte-normalization fixture. A future scheme changes the canonicalization scheme identifier.

### 8.8 Core prompt footer

Every prompt includes compact machine-readable instructions asking the agent to return `StageResultEnvelope v1` with matching `RunId` and prompt fingerprint when possible. The human-readable response remains unrestricted. The footer must not require hidden chain-of-thought.

### 8.9 Core-only CLI

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

Prompt command stdout contains only the complete prompt. Ambiguous workplans require bounded explicit selection. Core operates offline from a compatible packaged prompt snapshot when local information is sufficient.

### 8.10 Core dependencies

Expected: `platformdirs`, `typer`, `pydantic`, `python-frontmatter`, `packaging`. Clipboard may be optional `pyperclip`. Core does not require `filelock`, ACP, `httpx`, ML, or higher modules.

## 9. Tracker Module

### 9.1 Responsibilities

Tracker owns private SQLite history/migrations, run/event/prompt/output history, manual result ingestion, workplan observation/history and user selection, derived development projection, stale/ambiguous evidence handling, next-action recommendation, graph/history/workplan interfaces, retention/export/purge, and storage coordination for higher modules.

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
    def workplans(self, query: TrackedWorkplanQuery) -> Page[TrackedWorkplan]: ...
    def select_workplan(self, request: WorkplanSelectionRequest) -> WorkplanSelectionReceipt: ...
    def graph(self, request: WorkflowGraphRequest) -> WorkflowGraph: ...
```

`StatusRequest`/`NextActionRequest` include project + observation policy so callers control remote freshness/network cost. Tracker reconciles current public Core observations before current-state claims.

### 9.3 Manual result ingestion

Ingestion precedence:

1. valid `StageResultEnvelope` whose run/fingerprint match known prompt identity;
2. bounded deterministic strong markers when structured output is absent;
3. explicit user confirmation/selection when still ambiguous.

Tracker does not silently call an LLM to reinterpret arbitrary pasted text for basic state classification. Pasted content is untrusted data and cannot issue orchestrator commands.

Re-ingesting the same artifact is idempotent. Wrong-run/mismatched fingerprint fails safely unless the user explicitly binds it after seeing the mismatch.

### 9.4 RecordedEvent and ordering

```text
RecordedEvent
  sequence: monotonically increasing Tracker-local integer
  recorded_at
  event: EventEnvelope
```

Recording order is separate from producer wall-clock `occurred_at`, giving deterministic replay under differing clocks.

### 9.5 DevelopmentProjection

Bounded current/summary state identifies current candidate/workplan/protocol, stage attempts/outcomes summary, stale/ambiguous/inconsistent evidence, current blockers, recommended next stage/action with reason codes, and observation freshness. Detailed attempts remain in history.

Execution status and semantic outcome remain distinct.

### 9.6 Workplan selection

`select_workplan` records a private user preference, not repository authority. It is used only while compatible with current Core workplan evidence. If the selected artifact disappears, becomes semantically incompatible, or conflicts with explicit task input, Tracker reports stale/ambiguous rather than forcing the old selection.

### 9.7 WorkflowGraph

Tracker exposes a structured graph of allowed Protocol-stage relations overlaid with observed attempts/outcomes/current recommendation. Graph data is canonical; rendering is presentation. CLI must support text plus at least one machine-readable form (JSON). Mermaid/DOT are optional renderers and do not require graph-library authority.

### 9.8 Tracker storage

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/
  exports/
```

SQLite/WAL is v1 durable control storage. `filelock` begins here for migration/process coordination and later run ownership.

### 9.9 TrackerStorageSPI v1

```python
class TrackerStorageSPI(Protocol):
    def register_migrations(self, extension: ExtensionId, migrations: tuple[MigrationSpec, ...]) -> None: ...
    def transaction(self, extension: ExtensionId, *, write: bool) -> ContextManager[sqlite3.Connection]: ...
```

Tracker owns DB opening/configuration, migration ordering, backup/recovery policy, and transaction boundaries. Extensions own namespaced tables and may not alter/read another module's semantic tables directly; cross-module semantic reads use APIs. SQLite is honestly part of this SPI major.

### 9.10 Tracker CLI

```text
sdp status
sdp next
sdp ingest ...
sdp history
sdp workplans
sdp use <workplan>
sdp graph ...
```

Without Tracker these commands need not exist; Core remains functional.

## 10. Adapter Module

### 10.1 Responsibilities

Adapter owns route/model/backend/account/effort identity, manual/direct delivery, prompt-context requirements per route, structured transports, pre-render execution admission, execution lifecycle, benchmark source/cache/identity resolution, static capability recommendation, route probing, and automatic tracking through Tracker.

Adapter does not own quota/resource ledgers.

### 10.2 Adapter-owned identities

```text
RouteId
ExecutionAdmissionId
ModelRef
BackendRef / HarnessRef
AccountRef
TransportRef
EffortRef
ObservedExecutionIdentity
```

Route IDs are stable configured opaque keys, not hashes of mutable display fields.

### 10.3 ExecutionRoute v1

```text
ExecutionRoute
  route_id
  backend
  account
  transport
  model
  effort
  delivery_mode: direct | manual_handoff
  prompt_execution_mode: local | web | compatible future value
  repository_access: local_worktree | remote_connector | compatible future value
  configured capability metadata
```

Manual-web routes are first-class for recommendation and Scheduler AUTO. `prompt_execution_mode` is explicit rather than inferred from delivery because a future direct cloud route may still require web/remote-safe prompt context.

### 10.4 Route identity resolution

Internal model/route identities are stable local keys distinct from external benchmark slugs/display names. Adapter owns one alias/mapping resolver shared by benchmark providers. Automatic mapping requires sufficient provider/model/effort evidence; ambiguous aliases require explicit configuration. Source-specific effort labels are normalized inside source mappings, not through a Core closed enum.

### 10.5 AdapterAPI v1

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

### 10.6 Pre-render execution admission

`ExecutionAdmissionRequest` is built from current Core/Tracker state **before final prompt rendering** and includes:

- `RunId` already allocated by Core;
- project/stage/task/workplan/candidate identity;
- optional requested RouteId;
- interaction/manual-handoff constraints;
- required route capabilities/tooling/privacy constraints;
- Adapter-generated candidate route snapshots/capability evidence.

If no route-policy provider exists, Adapter admits the explicit route or explicit configured default and otherwise returns route-required. It does not automatically choose the highest benchmark.

If a route-policy provider exists, Adapter passes the bounded candidate route snapshots to it:

- explicit route is either admitted unchanged or rejected;
- omitted route may be selected automatically;
- provider does not need to call back re-entrantly into Adapter admission to enumerate candidates.

`ExecutionAdmission` returns `ExecutionAdmissionId`, `RunId`, selected route, `prompt_execution_mode`, candidate binding, optional opaque policy-admission reference, expiration/revalidation conditions, and reason metadata.

### 10.7 Render after admission

The application flow for `sdp run` is Frozen at the semantic level:

```text
Core.allocate_run_id
  -> observe/resolve stage + current candidate/workplan
  -> Adapter.admit(route explicit/default/AUTO policy)
  -> Core.render(using same RunId + admitted route.prompt_execution_mode)
  -> Adapter.start(using exact admission + rendered prompt)
```

`AgentStartRequest` must bind the same RunId/stage/candidate and prompt mode as the admission. Adapter rejects mismatches/stale admission rather than starting with a prompt rendered for another route context.

If rendering/user confirmation fails after admission but before start, caller invokes `Adapter.abandon`; admission expiration is a fail-safe, not the normal cleanup mechanism.

### 10.8 Manual handoff lifecycle

For `delivery_mode=manual_handoff`, `start` does not spawn a process. It uses the admitted route + rendered prompt and returns a handle in awaiting-external-result state plus `ManualHandoffArtifact` for clipboard/stdout. User response arrives through Tracker ingestion. `wait` may observe resulting completion or timeout. Direct process controls return a structured unsupported/unavailable problem.

Manual Core/Tracker copy-paste remains possible without Adapter; Adapter only gives that lower flow a common route/run abstraction when installed.

### 10.9 Direct execution lifecycle

For direct routes, `start` returns promptly with stable handle; `events` yields normalized user/tool/permission/status events via cursors; `respond` addresses stable control-request IDs; `cancel` is idempotent; `wait` returns terminal result or timeout without implicitly destroying the run.

One RunId has at most one concurrently active execution. Ambiguous start/crash is reconciled before another execution can be created.

### 10.10 AgentRunResult v1

Result separates execution terminal status from agent-reported workflow semantics. It includes run/admission/route identity, configured route, `ObservedExecutionIdentity` with provenance/confidence, backend/session identity where available, visible final response, structured result when available, candidate observations, interruption/failure class, transport telemetry, and Tracker-ingestion evidence.

Planned/configured identity and observed actual model/backend identity remain distinct, especially for manual web/provider-side routing. Zero process exit does not manufacture workflow PASS.

### 10.11 Agent transport SPI v1

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

Prefer ACP when sufficiently conformant; use documented native structured RPC/SDK/JSON fallbacks where needed. PTY scraping is not primary when structured transport exists. Initial backend families remain Claude, Codex, OMP, Pi, and Antigravity.

### 10.12 Route-policy SPI v1

```python
class RoutePolicyProvider(Protocol):
    def preview(self, request: RoutePolicyRequest) -> RoutePolicyDecision: ...
    def admit(self, request: RoutePolicyRequest) -> RoutePolicyAdmission: ...
    def abandon(self, request: RoutePolicyAbandonment) -> RoutePolicyReceipt: ...
    def reconcile(self, request: RoutePolicyReconciliation) -> RoutePolicyReceipt: ...
```

Preview is read-only. Admit may reserve/mutate. Explicit route is admitted unchanged or rejected; omitted route may be selected. Abandon handles pre-start release; reconcile handles started/terminal/manual-result outcomes. Operations are idempotent.

### 10.13 Benchmark source SPI

```python
class BenchmarkSourceProvider(Protocol):
    def descriptor(self) -> BenchmarkSourceDescriptor: ...
    def fetch(self, request: BenchmarkFetchRequest) -> RawBenchmarkSnapshot: ...
    def normalize(self, raw: RawBenchmarkSnapshot) -> BenchmarkSnapshot: ...
```

Snapshots preserve source/schema/version, fetched/generated times, digest/ETag, licensing/attribution, and observations. Observations preserve metric/direction/value/unit, uncertainty, external model identity, effort, harness/config, benchmark version, freshness, and identity-match quality.

Artificial Analysis is the preferred current general-intelligence source; DeepSWE is the preferred current coding evidence source. Exact endpoints/tier limits are mutable provider configuration, not Frozen architecture. Never fabricate missing scores.

DeepSWE evidence preserves `EXACT_CONFIG_MATCH`, `MODEL_EFFORT_PROXY`, `MODEL_ONLY_PROXY`, or `UNRESOLVED`; a score from one harness is not relabeled as measured success of another.

### 10.14 Recommendation policy

Design/architecture/difficult diagnosis prioritize current general-intelligence evidence among eligible routes. Implementation/repair prioritize current coding evidence, exact configuration first. Review/Verification prioritize high general intelligence and may display model/provider independence as secondary robustness evidence.

Do not combine incompatible Intelligence Index and DeepSWE measures into one universal scalar absent separate validated design. Missing evidence is UNSCORED, not zero.

### 10.15 Adapter dependencies/CLI

ACP support is an optional transport dependency; `httpx` is justified for bounded benchmark/source HTTP. Adapter does not require Scheduler/ML.

```text
sdp agents
sdp routes
sdp benchmarks ...
sdp models
sdp recommend <stage>
sdp run <stage> --route <route-id>
```

Manual route may produce/copy handoff artifact and remain awaiting external result.

## 11. Scheduler Module

### 11.1 Responsibilities

Scheduler owns resource ledgers/meters, pricing/opaque quota representation, reset/window inference, global reservations/uncertainty holds, usage attribution, task features, usage/outcome prediction, future-stage reserves, route admission/scoring, AUTO selection, and interruption rescheduling.

Scheduler never launches agents directly.

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

Preview is read-only. Admit atomically re-observes required resource state, revalidates feasibility, selects/validates route, and creates reservations in one DB transaction.

### 11.3 ScheduleRequest explicit versus AUTO

Schedule request includes RunId, project/stage/task features, candidate/workplan identity, bounded Adapter-supplied candidate route snapshots, optional requested RouteId, interaction/manual-handoff constraints, and policy overrides.

- requested route: evaluate that exact route only;
- omitted route: AUTO may choose among feasible candidates;
- manual route requires allowed user-mediated handoff;
- unattended execution requires a direct/automatable route.

### 11.4 Admission idempotency and release

Admission request fingerprint covers all semantics affecting feasibility/reservation. `admit` is idempotent for `(RunId, fingerprint)`: exact retry returns same live admission; conflicting request for same live run fails.

`release` idempotently abandons an admission that never started and releases/retains reservations according to meter uncertainty. It is the Scheduler implementation of Adapter route-policy abandonment. Expiration is fail-safe cleanup, not normal success path.

### 11.5 AdmissionDecision

Records selected route, run/project/stage/task identity, admission/fingerprint, decision time, binding meter observations/freshness, prediction quantiles, reservation IDs/amounts, rejected alternatives/reason codes, explanation components, and expiration/revalidation conditions.

### 11.6 Resource ledger model

A route consumes zero or more Scheduler-owned ledgers. Each ledger preserves:

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

`UNMETERED_FOR_SCHEDULER`, `METERED`, and `UNKNOWN` remain distinct route/resource states. Shared account quota is represented once and referenced by all routes; dual short/long windows are simultaneous constraints. Opaque quota stays in observed provider units. Transparent PAYG uses versioned pricing functions.

### 11.7 Meter SPI

```python
class AccountMeterProvider(Protocol):
    def descriptor(self) -> MeterDescriptor: ...
    def observe(self, request: MeterRequest) -> MeterSnapshot: ...
```

Prefer official/machine-readable sources; browser scraping is not normal. Preserve source/unit/time/freshness/confidence/account identity.

### 11.8 Reservation/reconciliation

Metered direct execution reserves predicted capacity on every consumed ledger atomically. Manual/unmetered route may need no quota reservation but still receives admission identity when Scheduler selected it.

If execution dies before final meter state is known, preserve uncertainty holds rather than release as zero. Provider current hard limits/meters outrank stale predictions. Reconciliation is idempotent and correlates planned route with observed execution identity when available.

### 11.9 Prediction

Predict distributions for runtime, consumption per ledger, billable token categories where relevant, monetary cost, probability of stage-quality completion, interruption probability, and future repair rounds.

Cold start uses interpretable priors by stage/role x model x effort x backend/transport with project corrections. Early learning uses empirical quantiles/EWMA/shrinkage without mandatory ML. Persist calibration evidence. Optimize expected resource/cash cost to accepted completion, not only first-call usage.

### 11.10 Scheduling policy

AUTO is default omitted-route policy only when Scheduler is active. Hard feasibility precedes ranking. Feasibility includes stage capability/effort, tools/skills, repository access, privacy/security, session independence, backend health, interaction constraints, predicted capacity, and protected future Review/Design reasoning reserve.

Ranking may consider quality-completion probability, interruption risk, future reasoning capacity, expiring quota opportunity cost, PAYG cost, manual handoff/continuity, independence/diversity, and latency. Decisions remain explainable.

### 11.11 Adapter integration

Scheduler implements Adapter `RoutePolicyProvider`. Adapter supplies route candidates and requested-route/AUTO intent; Scheduler preview/admit validates/selects; Adapter receives an admission and then causes Core to render for the selected route mode; Adapter starts direct/manual execution; pre-start failure invokes abandon/release; terminal/manual-result completion invokes reconcile.

Scheduler never replaces `sdp run`; Adapter never imports Scheduler.

### 11.12 Persistence

Scheduler adds namespaced tables/migrations to Tracker's user-global SQLite DB through Tracker SPI. Quota/account state is global across projects. Scheduler does not modify Tracker workflow tables directly.

## 12. Configuration ownership

Core owns canonical config loading and ProjectKey. Extensions contribute namespaced validated sections.

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

## 13. Persistence/event ownership

Core is stateless across invocations except configuration and bounded prompt/cache artifacts. Tracker introduces persistence; higher modules extend it through Tracker SPI.

- one SQLite DB may contain multiple extension table families, each with one semantic owner;
- only owner writes its tables;
- semantic cross-module reads use APIs;
- migration order follows dependency order;
- removing higher extension leaves lower data readable/functional;
- raw prompt/output and numeric telemetry have separable retention;
- persisted state is private local evidence, not repository authority.

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

No resource-aware AUTO. Manual routes are valid explicit/default routes.

### + Scheduler

```text
sdp resources
sdp usage
sdp predict <stage> [--route <id>]
sdp schedule <stage> --explain
sdp run <stage>
```

With Scheduler active, omitted route may AUTO-select. Explicit route bypasses ranking but not configured hard compatibility/resource admission.

## 15. Failure/degradation rules

```text
Scheduler unavailable
  -> Adapter explicit/default/manual routes + benchmark recommendation

one direct transport unavailable
  -> disable that route; manual/other direct routes remain

Adapter unavailable
  -> Tracker manual copy/paste remains

Tracker DB unavailable/corrupt
  -> Tracker/Adapter/Scheduler unavailable
  -> Core prompt rendering remains
```

A module advertises only healthy semantic capabilities.

## 16. Security/privacy

- Plugin entry points are trusted installed code, not a sandbox.
- Pasted agent output, structured results, benchmark/meter responses, and remote metadata are untrusted data: enforce size/time/schema bounds and never execute instructions from them as orchestrator commands.
- API keys/tokens never enter prompts, caches, events, logs, or repositories.
- Web prompt context excludes local paths/private state/account/resource telemetry/credential-bearing remotes.
- ProjectDescriptor local paths remain local process data.
- Agent subprocesses use direct argv/structured transports with explicit permissions; no dangerous bypass by default.
- Historical transcripts are not automatically injected into later prompts; only bounded structured projection is automatic.
- Benchmark licensing/attribution travels with cached observations.

## 17. Benchmark recommendation integrity

Every recommendation using online evidence is reconstructible from source snapshot/observation. Preserve source, metric, benchmark/index version, source-generated/fetched time, model + effort + harness/config, value/uncertainty, identity-match quality, and staleness.

Do not compare incompatible benchmark/index versions as one stable scale. Do not combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into one universal scalar without separate validated design.

## 18. Executable architecture fitness

Once packages exist, static checks enforce:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core public API/SPI only
Adapters    may import Core + Tracker public API/SPI only
Scheduler   may import Core + Tracker + Adapters public API/SPI only
```

Also check native PEP 420 namespace packaging, one extension entry-point group, no private cross-module imports, and one ownership of `sdp run`.

## 19. Module acceptance ladder

Each module is implemented, independently reviewed, and accepted before next workplan.

### WP-1 Prompt

Prove Core-only install/CLI; project descriptor/catalog; run-ID preallocation; read-only observation/workplan paging; versioned workplan/candidate digest schemes and incomplete-identity behavior; explicit remote observation policy; prompt rendering/privacy; ambiguity handling; prompt fingerprint; StageResultEnvelope footer; composition with no extensions; API/SPI serialization/error fixtures; no higher imports/persistence.

### WP-2 Tracker

Re-prove Prompt standalone with/without Tracker plus event/result idempotency; structured/manual ingestion precedence; correct run association; fresh Core observation; deterministic RecordedEvent paging; persistent but subordinate workplan selection; bounded status; structured workflow graph; persistence/restart; storage SPI; Core usability when Tracker disabled/deleted.

### WP-3 Adapter

Re-prove lower acceptance plus manual/direct routes; pre-render admission -> render -> start ordering; explicit/default behavior; route-policy SPI with no/fake provider; admission abandonment; prompt-mode binding; start/events/respond/cancel/wait; planned-vs-observed identity; automatic tracking; benchmark provenance/central identity mapping/failure degradation; capability recommendation separation; no quota-aware selection.

### WP-4 Scheduler

Re-prove lower acceptance plus read-only preview; atomic/idempotent admit; pre-start release; explicit-route validation without substitution; omitted-route AUTO; manual-handoff scheduling; shared/dual-window ledgers; cross-project reservation; UNMETERED vs UNKNOWN; prediction/calibration; future-review reserve; PAYG/expiring quota behavior; idempotent reconciliation/uncertainty holds; Adapter route-policy integration; Scheduler disablement restoring Adapter behavior.

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
parent_architecture_version: 1.3.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

Each workplan carries relevant parent invariants, module responsibilities/non-responsibilities, exact lower API/SPI contracts consumed, public API/SPI it must establish, affected/acceptance surface, standalone acceptance with higher modules absent, compatibility acceptance with lower modules present, and simplification/reopen triggers.

Do not pre-implement later modules merely for future convenience. The API/SPI seams and stable IDs here are the justified future-facing surface.

## 21. Versioning/evolution

- architecture major: breaks ladder, authority, dependency direction, or API role boundaries;
- minor: backward-compatible architecture/API strengthening before/alongside module adoption;
- patch: clarification without semantic change.

1.3.0 supersedes 1.2.0 because this review corrected execution ordering and result/tracker API contracts before WP-1.

Module package versions are independent and declare compatible lower API/SPI majors. New benchmark sources implement Adapter SPI; new transports implement Adapter SPI; new meters/pricing implement Scheduler SPI. Ordinary provider/model/benchmark/flag/predictor churn does not reopen parent architecture unless Frozen boundary is insufficient.

## 22. Active simplicity/reopen triggers

Reopen/simplify before adding multiple plugin loaders, reverse dependencies, duplicated CLI composition, separate mutable workflow authority, benchmark fields in Core, quota abstractions below Scheduler, duplicated model identity mapping, backend-specific workflow logic, Scheduler-owned process execution, private SQL/process objects in public APIs, hidden writes in previews, or stubs preserving broken higher layers instead of clean downgrade.

Reopen parent architecture only when evidence shows a Frozen boundary cannot satisfy the product: required reverse dependency, single registry insufficiency, public API role incapable of supporting next module without semantic break, or execution lifecycle unable to represent a required backend safely.

## 23. Third pre-implementation review — 2026-09-07

This pass challenged the complete control flow rather than individual interfaces. Material gaps closed:

1. **Route/render ordering cycle:** AUTO route selection previously happened after a route-sensitive prompt had already been rendered. Core now allocates RunId first; Adapter admits route; Core renders for admitted prompt mode; Adapter starts.
2. **Pre-start reservation leak:** admitted-but-not-started runs now have explicit Adapter abandonment / Scheduler release semantics plus expiration as fail-safe.
3. **Manual-route prompt mode:** `prompt_execution_mode` is explicit on routes rather than inferred from direct/manual delivery.
4. **Scheduler re-entrant route lookup risk:** Adapter passes bounded candidate route snapshots into route-policy admission rather than requiring policy to re-enter Adapter admission to enumerate candidates.
5. **Tracker public graph gap:** TrackerAPI now exposes structured WorkflowGraph instead of leaving `sdp graph` on private implementation.
6. **Tracker workplan-selection gap:** persistent user workplan choice has a public, subordinate, stale-aware API matching `sdp use`.
7. **Manual output parsing gap:** Core now requests StageResultEnvelope v1; Tracker defines structured-first/deterministic-marker/user-confirmation precedence without mandatory LLM classification.
8. **Digest evolution gap:** digest records carry canonicalization scheme; workplan/candidate identity can report incomplete rather than pretending equivalence across unsupported schemas.
9. **Workplan semantic-equivalence risk:** semantic digest is protocol/schema aware and conservative, not an LLM or heuristic claim that arbitrary metadata/text is non-semantic.
10. **Scheduler resource detail preservation:** ledger reset/expiration/funding categories required by the accepted quota architecture are restored explicitly.
11. **Model alias ownership:** one Adapter-owned model identity resolver prevents benchmark providers from creating competing model identities.
12. **Resource collection growth:** Scheduler resource queries are paginated like other potentially growing catalogs.

No remaining architecture-level blocker was found after these corrections. The architecture can now derive WP-1 through WP-4 without a route/render circularity or a need for future private cross-module imports.

## 24. Design verdict

**PASS — architecture 1.3.0 is implementation-ready.**

The next active implementation contract should be WP-1 Prompt Module only. WP-1 establishes Core, CLI/composition, Core API/SPI v1, run allocation, project/repository/workplan observation, canonical prompt rendering/result envelope, and prompt identity. It must not introduce Tracker persistence, agent integration, benchmark networking, or Scheduler/resource machinery.
