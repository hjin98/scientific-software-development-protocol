---
kind: architecture
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.1.0
supersedes_architecture_version: 1.0.0
protocol_version: 5.16.0
status: frozen
frozen_date: 2026-09-07
---

# SDP Orchestrator Architecture

## 1. Purpose and authority

This document is the parent architectural authority for the SDP/Protocol Orchestrator. It defines a **nested capability ladder** whose lower levels remain independently useful, installable, testable, and releasable:

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

Every higher level requires the complete lower level. No lower level may require, import, instantiate, persist state for, or otherwise depend on a higher level in order to perform its own accepted functions.

This architecture is **Tier 1B Frozen architecture** for the orchestrator implementation series. Individual module workplans derive implementation obligations losslessly from it. They may choose delegated realization details, but may not silently change the dependency direction, authority boundaries, public API/SPI semantics, persistence ownership, capability roles, or module responsibilities defined here.

This manual is intentionally more durable than an implementation workplan. If implementation evidence invalidates a Frozen choice, reopen only the affected architecture surface before changing it.

## 2. Product invariants

1. **Progressive usefulness.** The smallest installation performs a useful job by itself: resolve and print a complete Protocol prompt. Each extension adds capability without making the lower mode incomplete.
2. **Strict asymmetric dependencies.** `core <- tracker <- adapters <- scheduler`. Reverse or lateral production dependency is forbidden.
3. **Graceful degradation.** If an optional extension is absent, disabled, incompatible, or fails activation, the application falls back to the highest healthy lower capability level. Core prompt rendering remains available unless Core itself is broken.
4. **One CLI and one composition root.** The `sdp` executable and application composition root are owned by Core. Extensions register capabilities and commands through versioned SPIs; Core does not contain scattered imports or special cases for Tracker/Adapter/Scheduler implementations.
5. **Versioned public boundaries.** Higher modules consume lower modules only through documented `api.vN` surfaces and explicitly documented `spi.vN` extension contracts, never private implementation modules.
6. **No duplicated workflow authority.** Git, workplans, compatible Protocol profiles, and Design/Implementation results remain semantic authorities. Tracker history is evidence; benchmark data is recommendation evidence; Scheduler resource models select routes only.
7. **Manual operation remains first-class.** Tracker works with copy/pasted agent input/output. Adapter direct execution is an extension, not a prerequisite for workflow tracking.
8. **Static capability recommendation precedes dynamic scheduling.** Adapter may recommend models/routes using external benchmark evidence, but it does not meter quota, learn resource consumption, or automatically route work. Scheduler owns those functions.
9. **Benchmark observations preserve context.** Intelligence/coding numbers are never flattened into timeless scalar properties of a model. Source, benchmark/version, model identity, effort, harness/configuration, uncertainty, freshness, and identity-match quality remain attached.
10. **Scheduler remains subordinate to workflow intent.** It may select an execution route only after the required workflow stage has been determined and only among routes meeting that stage's engineering requirements.
11. **Private state remains outside project repositories.** Tracker and higher modules persist history/telemetry under the user-local state root, never in the protocol repository or target software repository by default.
12. **Subset acceptance is permanent.** A later module is not allowed to make an earlier module's standalone acceptance fail or require a higher-module installation.
13. **Stable IDs cross modules; implementation objects do not.** Cross-module references use small versioned value objects and opaque IDs rather than private repositories, ORM/SQL objects, backend sessions, or mutable implementation instances.
14. **Read-only query and mutating admission are distinct.** APIs must not hide durable mutation behind methods that appear to be previews/queries. In particular, Scheduler preview is read-only while admission is atomic and reserving.
15. **Long-running execution is modeled explicitly.** Agent execution must support start, event observation, permission response, cancellation, and terminal result without freezing one backend's event-loop/session mechanism into the API.

## 3. Capability ladder and install profiles

### 3.1 Level 0 — Core / Prompt Module

Required product capability:

```text
command
  -> observe configured repository/workplan/protocol inputs
  -> resolve one stage
  -> render canonical prompt
  -> print complete copy/paste-ready prompt
```

No durable development history, direct agent execution, benchmark refresh, metering, or scheduling is required.

### 3.2 Level 1 — Tracker Module

Adds:

- persistent development-cycle history;
- prompt/output association;
- manual response ingestion;
- current development projection;
- active/retired workplan tracking;
- PASS/NO-PASS and stale-evidence handling;
- next-action recommendation;
- text/JSON history and workflow graph.

All agent interaction may remain manual copy/paste.

### 3.3 Level 2 — Adapter Module

Adds:

- configured agent/backend/account/model/effort routes;
- ACP/native structured agent execution;
- explicit one-command execution of a user-selected route;
- current model-capability benchmark collection;
- static capability recommendations for stages/tasks.

There is **no quota metering, usage prediction, or resource-aware automatic route selection** at this level. A route is explicitly selected by the user or by an explicit user-configured default.

### 3.4 Level 3 — Scheduler Module

Adds:

- account/resource ledgers and meters;
- usage telemetry and attribution;
- atomic quota reservations and uncertainty holds;
- task feature extraction;
- usage/outcome prediction;
- quota/cost-aware route feasibility and scoring;
- default `AUTO` route selection;
- receding-horizon rescheduling/failover.

Scheduler reuses Adapter execution/capability evidence and Tracker history. It does not create a second transport, process runner, workflow reducer, or task database.

### 3.5 Distribution dependency graph

The intended install units are separate Python distributions in one repository/workspace:

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

Exact build/workspace tooling is delegated, but this dependency graph is Frozen.

Installing a higher distribution installs required lower distributions through ordinary package dependencies. Installing Core alone must not pull Tracker, Adapter, Scheduler, ACP, DB-locking, benchmark-network, or ML-only dependencies merely for future convenience.

## 4. Python packaging and namespace standard

Use the shared native PEP 420 namespace `sdp_orchestrator` so separately installable distributions can contribute subpackages without owning the same package file.

Frozen packaging rule:

```text
src/sdp_orchestrator/              # namespace package; NO __init__.py
    core/                           # regular package
    tracker/                        # regular package, separate distribution
    adapters/                       # regular package, separate distribution
    scheduler/                      # regular package, separate distribution
```

Every distribution contributing to `sdp_orchestrator` must preserve the native namespace-package rule. Do not place `sdp_orchestrator/__init__.py` in one distribution because that can hide portions supplied by the others.

Public API packages:

```text
sdp_orchestrator.core.api.v1
sdp_orchestrator.tracker.api.v1
sdp_orchestrator.adapters.api.v1
sdp_orchestrator.scheduler.api.v1
```

Service-provider/extension packages:

```text
sdp_orchestrator.core.spi.v1
sdp_orchestrator.tracker.spi.v1
sdp_orchestrator.adapters.spi.v1
sdp_orchestrator.scheduler.spi.v1
```

Adapter/Scheduler SPIs exist so new transports, benchmark sources, route policies, meters, or pricing sources can be added without changing Core or creating a second plugin loader. They do not imply that every module must expose many plugins.

## 5. Public API standard

This section is Frozen because these contracts become dependency boundaries for later modules.

### 5.1 API versus SPI

- **API** is consumed by application code and higher modules to use a module's semantic services.
- **SPI** is implemented by extensions/providers to contribute behavior to a lower owner.
- An API consumer does not depend on provider/private classes.
- An SPI provider receives only the capabilities explicitly granted by its SPI context.
- First-party modules obey the same boundary as third-party extensions.

### 5.2 Compatibility rule

A public major is a semantic compatibility contract.

- Breaking request/response semantics, required-field changes, method removal/renaming, changed ID meaning, changed mutation semantics, or changed error meaning require `api.v2`/`spi.v2`.
- Adding optional response fields with safe defaults, adding new methods, adding new namespaced event/error/capability values, or adding new data values such as a model/stage may remain within v1 when old consumers continue to behave correctly.
- Existing callers must not be forced to enumerate every future stage/model/effort/error/event value.
- Persisted schema versions are independent of Python API major versions.
- Event type versions and benchmark-source schema versions are independent of API major versions.

### 5.3 Public records are data contracts

Cross-module request/response records are immutable-by-convention value objects with JSON-compatible serialization. Pydantic is the initial implementation technology, but Pydantic internals are not the semantic contract.

Required rules:

- timestamps serialize as timezone-aware ISO-8601 UTC values;
- IDs serialize as strings and remain opaque to consumers unless their structure is explicitly documented;
- source digests use `DigestRef` rather than bare hashes;
- request models reject unsupported/incompatible required semantics rather than silently dropping them;
- response models may gain optional fields within a major; callers must tolerate such additive data;
- cross-module records do not contain open file handles, DB connections, subprocess objects, event loops, backend SDK objects, or mutable repository objects.

### 5.4 Stable generic page/cursor contract

Potentially unbounded collections do not return an unbounded `Sequence` as their compatibility contract. Use a cursor page:

```text
Page[T]
  items: tuple[T, ...]
  next_cursor: str | None
```

Cursor structure is opaque and valid only under the owning API/version/query semantics. Short bounded catalogs may still return tuples directly when the owner guarantees bounded size.

### 5.5 Stable problem/error contract

Do not freeze a large exception-class hierarchy. Public API failures expose one stable problem envelope:

```text
Problem
  code: str                  # stable namespaced machine code
  message: str               # human-readable, not for control flow
  retryable: bool | None
  details: mapping           # bounded/redacted machine detail
```

Python APIs raise `OrchestratorError` carrying `Problem`. CLI maps the same `Problem.code` to deterministic exit behavior and stderr diagnostics.

Core generic codes include semantic classes such as:

```text
core.invalid_request
core.not_found
core.ambiguous
core.incompatible
core.unavailable
core.conflict
core.stale
core.permission_required
core.timeout
core.cancelled
```

Modules may add namespaced codes without requiring a Core release. Consumers branch on `code`, not message text.

### 5.6 Idempotency and mutation semantics

- Methods named `list`, `get`, `observe`, `status`, `preview`, `predict`, `recommend`, `probe`, or equivalent are read-only unless explicitly documented otherwise.
- Durable mutation methods return an acknowledgement/identity; they do not return `None` when retry/idempotency matters.
- Event recording is idempotent by `EventId`.
- Manual ingestion is idempotent by ingestion/result identity when the same artifact is supplied again.
- Scheduler admission is atomic with reservation creation.
- Adapter `start` creates at most one active execution for one `RunId`; retry after an ambiguous transport failure must reconcile before creating another execution.

### 5.7 Sync/async boundary

Core, Tracker, benchmark catalog queries, and Scheduler planning APIs remain callable synchronously. Long-running agent transports may be asynchronous internally, but the cross-module Adapter API uses an explicit run handle + cursor/event control surface rather than exposing a backend/event-loop-specific coroutine object.

This allows CLI, future TUI/MCP/service layers, and synchronous programmatic callers to share the same semantic API while transport implementations use asyncio/ACP/SDK facilities internally.

### 5.8 Construction and service acquisition

Do not freeze each module's concrete constructor. Core exports the application composition contract:

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, capability: CapabilityKey) -> bool: ...
    def service(self, capability: CapabilityKey, *, api_major: int = 1) -> object: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

`create_application` loads Core configuration, discovers compatible installed extensions, activates them dependency-topologically, and returns the highest healthy capability set. The CLI uses the same composition path.

Consumers that request a capability whose provider is absent/disabled/incompatible receive a structured `core.unavailable`/`core.incompatible` problem, not an import-time crash.

Concrete implementation classes/factories beneath this composition root remain private Tier 2.

## 6. Core extension composition SPI v1

### 6.1 One entry-point registry

Core discovers installed extensions using Python package metadata entry points under exactly one group:

```text
sdp_orchestrator.extensions.v1
```

Do not scan arbitrary directories or import arbitrary repository files as plugins.

An entry point resolves to an `ExtensionProvider` object/factory implementing the Core SPI.

### 6.2 Extension manifest

Manifest inspection must be side-effect-minimal and must not start subprocesses, perform network I/O, open the target repository for mutation, or migrate storage.

```text
ExtensionManifest
  extension_id: str
  extension_version: str
  core_spi_spec: str
  requires_extensions: mapping[extension_id, version_spec]
  requires_capabilities: tuple[CapabilityRequirement, ...]
  provides_capabilities: tuple[CapabilityKey, ...]
  optional_capabilities: tuple[CapabilityKey, ...]
```

`extension_id` is globally stable within an installation and should use a collision-resistant namespaced form. First-party IDs are reserved under `sdp.*`.

Use the maintained `packaging` library for version/specifier comparison rather than custom semantic-version parsing.

### 6.3 Activation contract

Conceptual SPI:

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

`ExtensionContext` provides only versioned Core services needed for composition:

- read-only effective Core configuration + the extension's own namespaced config data;
- service registry access to already-activated required lower capabilities;
- CLI registrar;
- config-schema registrar;
- event publisher/subscriber registrar;
- diagnostic registrar.

`ExtensionRegistration` identifies successfully published services/capabilities and cleanup hooks if the extension owns process-local resources.

Activation order is dependency-topological. Incompatible or failed extensions are disabled together with dependents; healthy lower levels continue. `sdp capabilities` and `sdp doctor` report reasons.

### 6.4 Service registry

Services are published under `CapabilityKey + api_major`.

- A capability documented as singular must have at most one active primary service. Ambiguity is a composition error for dependents.
- Provider-style capabilities may be multi-valued and are returned in stable provider-ID order.
- A higher module may request a lower capability through the registry, then type-check/use it through the lower module's public API/SPI protocol.
- Service registration cannot replace an already active singular service silently.

### 6.5 CLI registration

CLI command names are owned by the first module that defines their semantic command. A later module may contribute lower-defined policy hooks or subcommands, but may not silently replace another module's command handler.

This rule specifically prevents Scheduler from defining a second competing `sdp run`. Adapter owns `sdp run`; Scheduler extends its omitted-route behavior through the Adapter route-policy SPI defined below.

### 6.6 Config registration

Core owns one canonical config loader/resolution path. Extensions register exactly one namespaced config schema/default provider through the SPI. Core preserves unknown config belonging to absent extensions but does not interpret it.

Precedence:

```text
built-in defaults
  -> config file/profile
  -> documented environment allowlist
  -> explicit CLI/API override
```

Resolved values preserve provenance where automatic decisions matter. Secrets remain references/environment/approved secret-store inputs and never appear in ordinary resolved snapshots.

### 6.7 Event publication

Core owns the generic event envelope and process-local publisher. Extensions may register event sinks/subscribers.

Event delivery to optional sinks is at-least-once within the process attempt when retry is practical; therefore sinks must be idempotent by `EventId`. Sink failure cannot corrupt or counterfeit the primary lower-module result. Capability owners decide whether their own health must degrade after sink failure.

## 7. Core shared identifiers and records

Core `api.v1` owns only the small records genuinely needed across modules.

### 7.1 Stable identifiers

```text
ProjectKey       config-declared stable local project key; does not require Tracker DB
RunId            opaque Core-generated ID for one prompt/execution attempt envelope
EventId          opaque unique event identity
StageRef         protocol profile identity + protocol version + stage key
RouteId          stable Adapter-owned configured route key
CapabilityKey    opaque versioned capability identifier
ExtensionId      extension manifest identity
```

`RunId` is allocated when Core renders a prompt. One `RunId` may proceed to zero or one logical agent execution. Reusing identical prompt content for a second independent agent attempt requires a new render/new `RunId`.

### 7.2 DigestRef

```text
DigestRef
  algorithm: str
  value: str
```

Initial canonical digest algorithm is SHA-256. Callers must not assume all future digest algorithms have the same textual length.

### 7.3 StageRef

`StageRef` contains enough identity to prevent a stage named `review` under one Protocol profile/version from being confused with another. Stage names remain data, not closed enums.

### 7.4 WorkplanRef

`WorkplanRef` preserves both exact artifact identity and semantic authority identity:

```text
WorkplanRef
  workplan_id
  protocol_version
  path
  artifact_digest: DigestRef
  semantic_digest: DigestRef
  lifecycle_state
```

Lifecycle-only movement/status bookkeeping may change `artifact_digest/path` while preserving `semantic_digest`; substantive authority changes must alter `semantic_digest`.

### 7.5 CandidateRef

`CandidateRef` represents observed candidate identity rather than a mutable repository object:

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

A material staged/unstaged/untracked source change must change `working_tree_digest`. When Core cannot fingerprint relevant dirty state confidently, `identity_complete=false` rather than inventing durable identity.

### 7.6 EventEnvelope

```text
EventEnvelope
  event_id: EventId
  event_type: str
  schema_version: int
  occurred_at
  project_key: ProjectKey
  run_id: RunId | None
  producer_extension: ExtensionId
  payload: JSON-compatible producer-owned object
```

Event type values are namespaced and versioned, e.g. `core.prompt.rendered.v1`, `tracker.result.ingested.v1`, `adapters.run.completed.v1`, `scheduler.admission.created.v1`.

Events are evidence, not workflow authority. Tracker may persist unknown future event types opaquely while projecting only semantics it understands.

## 8. Core / Prompt Module

### 8.1 Responsibilities

Core owns:

- `sdp` CLI bootstrap and application/extension composition;
- project configuration sufficient to locate target repositories and compatible Protocol prompt sources;
- read-only Git/repository/workplan observations needed by all later modules;
- protocol-profile/stage catalog;
- canonical prompt loading and declared-input substitution;
- local/web prompt rendering;
- prompt/run identity and fingerprinting;
- stdout output and optional clipboard integration;
- capability/doctor reporting.

Core does **not** own durable workflow history, next-stage inference from past agent results, agent processes, benchmark data, resource meters, or scheduling.

### 8.2 CoreAPI v1

Core's public service must expose repository/workplan observation as well as prompt rendering so Tracker does not need Core internals.

```python
class CoreAPI(Protocol):
    def list_stages(self, project: ProjectKey) -> tuple[StageDescriptor, ...]: ...
    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...
    def workplans(self, request: WorkplanQuery) -> WorkplanCatalog: ...
    def render(self, request: PromptRequest) -> RenderedPrompt: ...
```

`observe`, `workplans`, and `render` are read-only with respect to the target repository. They may read local Git/workplan files and perform explicitly configured read-only remote observation; they may not silently pull/merge/rebase/push or edit the target repository.

### 8.3 ProjectObservation

The observation provides the current repository/workplan inputs required by higher modules without exposing Git-library/private objects. It includes project identity, sanitized repository identity, `CandidateRef`, upstream/remote freshness where known, Protocol profile identity, and relevant observation warnings/incompleteness.

### 8.4 WorkplanQuery / WorkplanCatalog

The catalog reports active/archive candidates, exact + semantic fingerprints, lifecycle consistency, and selection evidence. It does not silently choose among materially plausible workplans by mtime.

Core may return a selected workplan when an explicit selector or unambiguous configured/repository rule resolves it; ambiguity is preserved as data/problem rather than hidden guessing.

### 8.5 PromptRequest v1

Required semantics:

```text
project: ProjectKey
stage: StageRef
execution_mode: local | web
workplan_selector: optional explicit selector
first_task: optional task description for workplan-free Design
input_overrides: mapping of declared prompt input -> value
```

Execution mode is a data value rather than a Python enum closed against future modes; v1 validates at least `local` and `web`.

### 8.6 RenderedPrompt v1

Required semantics:

```text
run_id: RunId
prompt_text: str
prompt_fingerprint: DigestRef
stage: StageRef
prompt_source: PromptSourceRef
resolved_inputs: mapping + provenance
project_observation: sanitized ProjectObservation
selected_workplan: WorkplanRef | None
```

`prompt_text` is the complete copy/paste-ready artifact. Diagnostics/recommendations are not inserted into stdout prompt text.

### 8.7 Prompt fingerprint v1

Prompt association must not depend on an ambiguous self-hash.

For v1, Core renders the full copyable prompt using a fixed fingerprint placeholder in the structured footer, after the final `RunId` is known. It computes SHA-256 over the exact UTF-8 bytes of that placeholder-form prompt, then replaces the placeholder with `sha256:<hex>`.

Thus the fingerprint covers the exact rendered prompt, including `RunId`, canonical prompt prose, resolved inputs, and orchestrator context, while excluding only its own final digest value. The literal placeholder token and normalization rule are part of Prompt fingerprint v1 and must be documented/tested by WP-1. Future fingerprint algorithms use a new fingerprint scheme/version, not silent reinterpretation.

### 8.8 Core command behavior

Core-only commands include:

```text
sdp prompt <stage>
sdp design
sdp implementation
sdp review
... compatible protocol-profile stage aliases ...
sdp capabilities
sdp doctor
```

Default stdout for a prompt command is only the complete prompt. Warnings/diagnostics go to stderr or explicit diagnostic commands.

If workplan selection is ambiguous, Core requires a bounded explicit choice. Design with no workplan may require `--task`.

Core must operate offline from a compatible packaged prompt snapshot when local repository information is sufficient.

### 8.9 Core dependencies

Expected justified dependencies:

- `platformdirs`;
- `typer`;
- `pydantic`;
- `python-frontmatter`;
- `packaging`.

Clipboard is an optional Core extra using `pyperclip`; stdout remains mandatory and sufficient.

Core must not require `filelock`, `agent-client-protocol`, `httpx`, an ML library, or higher-module code merely for future convenience.

## 9. Tracker Module

### 9.1 Responsibilities

Tracker adds persistent development history while preserving manual agent I/O.

It owns:

- one user-local SQLite control database and migrations;
- project/run/event history partitioning;
- prompt recording from Core events;
- pasted/output artifact storage according to retention policy;
- structured-result parsing and run association;
- workplan observations/lifecycle history;
- development projection from current Core repository evidence + recorded results;
- stale/ambiguous/inconsistent evidence handling;
- next-stage/action recommendation;
- status/history/workplans/graph interfaces;
- private-state retention/export/purge;
- extension-storage coordination for higher modules.

Tracker does not run agents or rank models from online benchmarks.

### 9.2 TrackerAPI v1

```python
class TrackerAPI(Protocol):
    def record(self, event: EventEnvelope) -> RecordReceipt: ...
    def ingest(self, request: IngestRequest) -> IngestResult: ...
    def status(self, project: ProjectKey) -> DevelopmentProjection: ...
    def next_action(self, project: ProjectKey) -> NextAction: ...
    def get_run(self, run_id: RunId) -> TrackedRun: ...
    def history(self, query: HistoryQuery) -> Page[EventEnvelope]: ...
```

`record` is idempotent by `EventId` and returns whether the event was newly stored or already present. Replaying the same event must not create duplicate semantic history.

`ingest` binds outputs to Core-created `RunId` + prompt fingerprint. Wrong-run or ambiguous pasted output fails safely or requires explicit bounded confirmation. Re-ingesting the exact same result is idempotent.

`status` and `next_action` reconcile fresh `CoreAPI.observe/workplans` evidence before making claims. A stored PASS does not override a changed candidate/workplan/protocol identity.

`history` is paginated and ordered deterministically by the query's documented ordering, with event ID as tie-breaker.

### 9.3 DevelopmentProjection v1

The projection is derived, never a mutable source-of-truth row. It minimally identifies:

- project/current candidate/workplan/protocol;
- known stage attempts and semantic outcomes;
- stale/ambiguous/inconsistent evidence;
- active blockers/route classes reported by results;
- recommended next workflow stage/action + reason codes;
- observation freshness.

Execution status and semantic outcome remain distinct.

### 9.4 Tracker storage

Tracker introduces the private user-global state root:

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/       # optional bounded raw events/transcripts
  exports/                           # explicit user action only
```

SQLite is the v1 durable control store. WAL mode is the intended single-user multi-process configuration.

`filelock` is introduced here for migration/process coordination and later per-worktree run ownership. Core alone does not need it.

### 9.5 Tracker storage SPI v1

Higher modules may add namespaced durable tables without importing Tracker SQL internals.

Conceptual SPI:

```python
class TrackerStorageSPI(Protocol):
    def register_migrations(self, extension: ExtensionId, migrations: tuple[MigrationSpec, ...]) -> None: ...
    def transaction(self, extension: ExtensionId, *, write: bool) -> ContextManager[sqlite3.Connection]: ...
```

Frozen semantics:

- Tracker owns DB opening, WAL/configuration, migration ordering, backup/recovery policy, and transaction boundaries.
- Extension table names are namespaced by stable extension ownership.
- An extension may read/write only its own semantic tables through this SPI; cross-module semantic reads use public APIs.
- Higher modules may not alter Tracker-owned tables directly.
- Scheduler can perform atomic transactions across its own global resource/reservation tables in the shared DB.
- Migration order follows module/extension dependency order.
- Removing a higher extension may leave its tables dormant; lower modules remain readable/functional.

SQLite is explicitly part of Tracker SPI v1. A future non-SQLite storage replacement requires a new SPI major rather than pretending the DB boundary never existed.

### 9.6 Tracker CLI additions

```text
sdp status
sdp next
sdp ingest ...
sdp history
sdp workplans
sdp use <workplan>
sdp graph ...
```

When Tracker is absent these commands need not exist; Core prompt commands remain fully functional.

## 10. Adapter Module

### 10.1 Responsibilities

Adapter adds explicit direct agent execution and capability evidence, but **not resource-aware automatic routing**.

It owns:

- agent/backend transport profiles;
- account/credential references without storing raw secrets;
- model/effort catalog;
- execution routes;
- ACP/native structured transport integration;
- explicit route execution lifecycle;
- benchmark-source providers, caching, identity matching, and static capability recommendation;
- route health/capability probing;
- automatic tracking of direct-run visible output/results through Tracker.

### 10.2 Route identities

Keep distinct:

```text
ModelRef
BackendRef / HarnessRef
AccountRef
TransportRef
EffortRef
ExecutionRoute(RouteId)
```

A route is configured identity, not a model alias:

```text
Route = backend + account + transport + model + effort + repository-access mode
```

`RouteId` must be stable across process restarts and configuration reloads. It is a configured opaque key, not a hash of mutable display fields.

Scheduler later attaches resource-ledger mappings; Adapter does not need quota state to define a route.

### 10.3 AdapterAPI v1

```python
class AdapterAPI(Protocol):
    def routes(self, query: RouteQuery | None = None) -> Page[ExecutionRoute]: ...
    def probe(self, route: RouteId) -> RouteCapabilitySnapshot: ...
    def benchmarks(self, query: BenchmarkQuery) -> Page[BenchmarkObservation]: ...
    def recommend(self, request: RecommendationRequest) -> RecommendationSet: ...
    def start(self, request: ExplicitExecutionRequest) -> AgentRunHandle: ...
    def events(self, request: AgentEventQuery) -> Page[AgentEvent]: ...
    def respond(self, request: AgentControlResponse) -> AgentControlReceipt: ...
    def cancel(self, run_id: RunId) -> AgentControlReceipt: ...
    def wait(self, request: AgentWaitRequest) -> AgentRunResult: ...
```

This replaces a one-shot `execute() -> AgentRunResult` contract because real coding-agent integration requires streaming/progress, permission requests, cancellation, and terminal reconciliation.

### 10.4 Explicit execution semantics

`ExplicitExecutionRequest` requires:

- Core `RenderedPrompt`/binding for the same `RunId`;
- explicit `RouteId` or an explicit user-configured default already resolved before `start`;
- project/candidate identity expected at start;
- allowed interaction/permission policy.

AdapterAPI itself does **not** choose an automatic route. If Scheduler is absent and no explicit/default route is available, direct execution is unresolved and recommendations may be shown to the user.

`start` returns promptly with an `AgentRunHandle`. The handle contains only stable run/route/process-session references, not backend SDK/process objects.

`events` returns normalized user-visible/tool/permission/status events using cursor pagination. Event type is a namespaced data value, not a closed enum.

`respond` answers a pending control/permission request using its stable request ID. Unsupported response modes return a structured problem.

`cancel` is idempotent. `wait` blocks up to an optional timeout and returns the terminal result or a timeout problem without destroying the underlying run automatically.

The same `RunId` must not have two concurrently active Adapter executions. An ambiguous crash/start result is reconciled before another execution is created.

### 10.5 AgentRunResult v1

Terminal result separates process/execution status from agent-reported workflow semantics. It minimally includes:

- `RunId`, `RouteId`, backend/session identity when available;
- execution terminal status;
- user-visible final response if available;
- normalized structured result if available;
- pre/post candidate observations or references;
- interruption/quota/provider failure classification when known;
- telemetry made available by the transport, with missing fields left missing;
- evidence/diagnostics needed for Tracker ingestion.

A zero process exit does not manufacture workflow PASS.

### 10.6 Adapter transport SPI v1

New agent integrations implement an Adapter-owned structured transport provider rather than changing AdapterAPI:

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

Adapter normalizes transport-specific objects into public `Agent*` records. Prefer ACP where sufficiently conformant; use documented native structured RPC/SDK/JSON fallbacks where needed. PTY scraping is not the primary supported path when structured transport exists.

Initial backend families remain Claude, Codex, OMP, Pi, and Antigravity. Exact flags and ACP/native selection are delegated and capability-probed.

### 10.7 Adapter automatic-route policy SPI v1

Adapter owns `sdp run`, so Scheduler must not replace that command. Adapter defines one optional route-policy extension point for the omitted-route case:

```python
class RoutePolicyProvider(Protocol):
    def preview(self, request: RoutePolicyRequest) -> RoutePolicyDecision: ...
    def admit(self, request: RoutePolicyRequest) -> RouteAdmission: ...
    def reconcile(self, request: RoutePolicyReconciliation) -> None: ...
```

Without an active provider, Adapter requires an explicit/user-configured default route. Scheduler implements this SPI later.

`admit` may be mutating/reserving; `preview` is read-only. Adapter passes terminal/interruption reconciliation back to the provider after execution. Provider failure must fail safely without bypassing its own reservation/admission semantics.

### 10.8 Benchmark source SPI v1

External benchmark data is a versioned observation source, not model truth.

```python
class BenchmarkSourceProvider(Protocol):
    def descriptor(self) -> BenchmarkSourceDescriptor: ...
    def fetch(self, request: BenchmarkFetchRequest) -> RawBenchmarkSnapshot: ...
    def normalize(self, raw: RawBenchmarkSnapshot) -> BenchmarkSnapshot: ...
```

`BenchmarkSnapshot` preserves source ID/name, endpoint/schema/version identity, fetched/generated timestamps, content digest/ETag where available, observations, and source/license/attribution metadata required for safe caching/display.

`BenchmarkObservation` preserves:

- metric ID and direction;
- numeric value/unit;
- confidence/uncertainty when published;
- external model/source identity;
- effort/reasoning setting where relevant;
- harness/configuration where relevant;
- benchmark/source version;
- generated/fetched freshness;
- internal identity-match quality.

### 10.9 Artificial Analysis source

Current preferred general-intelligence evidence is the official Artificial Analysis Data API. At this architecture review, the documented Free language-model endpoint is:

```text
GET https://artificialanalysis.ai/api/v2/language/models/free
```

It requires a user-owned API key and exposes headline indices including the Artificial Analysis Intelligence Index plus an `intelligence_index_version`.

The source provider must:

- keep API keys in approved secret inputs, never Tracker DB/public repo;
- prefer stable upstream model/creator identifiers over display-name matching;
- preserve index version/freshness;
- obey current API terms/attribution and rate-limit/error semantics;
- cache privately;
- never redistribute cached source data through this public repository/package unless licensing permits;
- degrade to last-known-good attributed data or `UNAVAILABLE`, never fabricate a score.

Exact endpoint/tier/rate limits are external mutable policy, not Frozen architecture.

### 10.10 DeepSWE source

Current preferred coding-capability evidence is DeepSWE. The current v1.1 public artifact is:

```text
https://deepswe.datacurve.ai/artifacts/v1.1/leaderboard-live.json
```

DeepSWE observations are configuration-level, not timeless model scalars. The source/official benchmark materials distinguish agent harness, model, and reasoning effort and report solve/pass-rate and efficiency metadata.

Identity transfer quality is represented explicitly:

```text
EXACT_CONFIG_MATCH
MODEL_EFFORT_PROXY
MODEL_ONLY_PROXY
UNRESOLVED
```

A DeepSWE score measured under one harness is not silently relabeled as the measured success rate of another harness such as Codex CLI or Claude Code. It may be used as a coding prior with benchmark context and transfer quality shown.

Endpoint/version evolution is handled by source-provider updates and schema checks, not silent wrong parsing.

### 10.11 Model identity resolution

Internal model identities are stable local keys separate from external source slugs/names. Source providers produce candidate mappings; one Adapter-owned resolver owns accepted aliases.

Automatic mapping requires sufficient provider/model/effort evidence. Ambiguous aliases require explicit local configuration. Source-specific effort labels are normalized inside their source mapping rather than by a Core closed enum.

### 10.12 Static recommendation policy

Adapter recommendation is capability recommendation, not scheduling.

Initial role policy:

- Design/architecture/difficult diagnosis: prioritize current general-intelligence evidence among configured eligible routes;
- Implementation/repair: prioritize current DeepSWE/coding evidence, preferring exact configuration evidence and clearly labeling proxies;
- Review/Verification: prioritize high general intelligence; when Tracker knows implementation route, independent model/provider diversity may be shown as a secondary robustness signal.

Do not combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into a universal scalar unless a later explicit policy validates that transformation. Missing benchmark evidence is `UNSCORED`, not zero.

### 10.13 Adapter CLI additions

```text
sdp agents
sdp routes
sdp benchmarks status
sdp benchmarks refresh
sdp models
sdp recommend <stage>
sdp run <stage> --route <route-id>
```

When Scheduler is absent, `sdp run` without explicit/user-pinned/default route must not silently choose the top recommendation.

## 11. Scheduler Module

### 11.1 Responsibilities

Scheduler is the final nested extension. It owns dynamic resource-aware route selection/learning:

- resource ledgers/account meters;
- transparent pricing and opaque quota units;
- reset/window inference and provenance;
- global reservations/uncertainty holds;
- usage telemetry/attribution;
- deterministic task features;
- usage/outcome prediction;
- dynamic future-stage reserves;
- route admission/scoring;
- default `AUTO` route selection;
- quota/provider interruption rescheduling.

Scheduler never launches agent processes directly. It selects/reserves a `RouteId` and delegates execution to Adapter.

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

The preview/admit distinction is Frozen:

- `preview` is read-only and may be called repeatedly for UI/explanation;
- `admit` atomically re-evaluates current feasibility, selects a route, and creates all required reservations in one DB transaction;
- an earlier preview is advisory and cannot be converted into a reservation without revalidation;
- `reconcile` applies observed outcome/meter evidence and releases/adjusts reservations or retains uncertainty holds.

### 11.3 AdmissionDecision v1

An admitted run records:

- selected `RouteId`;
- `RunId`/project/stage/task identity;
- decision timestamp;
- binding resource-ledger observations/freshness;
- prediction quantiles used;
- one or more reservation IDs/amounts;
- rejected alternatives + reason codes;
- deterministic score/explanation components;
- expiration/revalidation conditions for the admission.

Reservation identity is opaque Scheduler data. Adapter sees it only through the RoutePolicy SPI context needed for reconciliation.

### 11.4 Resource model

A route consumes zero or more Scheduler-owned resource ledgers.

A ledger records concepts such as:

- allowance visibility: `OPAQUE` / `PRICED`;
- expiration: `EXPIRING` / `NON_EXPIRING`;
- reset/window semantics: `NONE`, `FIRST_USE_ANCHORED`, `ACCOUNT_FIXED`, `BILLING_CYCLE`, `CALENDAR_FIXED`, `CONTINUOUS_ROLLING`, `UNKNOWN`;
- funding behavior: `HARD_STOP`, `FALLBACK_TO_OVERAGE`, `POSTPAID`;
- current observed balance/usage when available;
- units/provenance/confidence;
- reservations/uncertainty holds.

`UNMETERED_FOR_SCHEDULER`, `METERED`, and `UNKNOWN` remain distinct route/resource states. Shared account quota is represented once and referenced by every consuming route. Dual short/long subscription windows are simultaneous constraints.

Opaque subscription quota remains in observed provider meter units. Transparent PAYG uses versioned pricing functions; do not invent token-equivalent conversions for opaque quotas.

### 11.5 Meter SPI v1

Scheduler meter providers are independent of Adapter transports:

```python
class AccountMeterProvider(Protocol):
    def descriptor(self) -> MeterDescriptor: ...
    def observe(self, request: MeterRequest) -> MeterSnapshot: ...
```

Prefer official API/backend machine-readable meter state, then stable provider/account knowledge, empirical inference, and explicit user-supplied snapshots where automatic evidence is unavailable. Browser scraping is not the normal meter source.

Every meter observation preserves source, time/freshness, unit, and confidence.

### 11.6 Reservation semantics

Before a metered direct run, Scheduler `admit` reserves predicted capacity atomically on every consumed ledger in the user-global SQLite DB.

Reservations are predictive holds, not vendor-reported consumption. If a run dies before final meter state is known, do not release the hold as though usage were zero; preserve uncertainty until authoritative observation/policy resolves it.

Observed provider hard limits/refreshed meters override stale predictions/reservations.

### 11.7 Usage/outcome predictor

Predict distributions, not single guesses, for task `t` on route `r`:

```text
runtime
consumption per resource ledger
billable token categories when relevant
monetary cost when priced
probability of stage-quality completion
probability of quota/provider interruption
future repair-round distribution
```

Cold start uses conservative interpretable priors by stage/role × model × effort × backend/transport with project corrections when evidence exists. Early learning uses empirical quantiles/EWMA/shrinkage without mandatory ML dependency. Persist prediction-versus-actual calibration evidence.

The target is expected resource/cash cost to accepted stage completion, not merely first-call usage.

### 11.8 Scheduling policy

`AUTO` becomes the default omitted-route policy only when Scheduler capability is active.

Hard feasibility precedes ranking. Feasibility includes stage capability/effort requirements, tools/skills/MCP visibility, repository access, privacy/security, session independence, provider/backend health, interactive-versus-unattended constraints, predicted capacity at configured quantile, and protected future Review/Design reasoning reserve.

Ranking inside the feasible set considers required-quality completion probability, interruption risk, future reasoning capacity, expiring-subscription opportunity cost, PAYG cost, manual handoff/continuity penalty, independence/diversity preference where relevant, and latency.

Manual web may be `UNMETERED_FOR_SCHEDULER` yet infeasible for unattended execution. Zero tracked quota is not infinite capability.

### 11.9 Scheduler Adapter policy integration

Scheduler implements `adapters.spi.v1.RoutePolicyProvider`:

- `preview` maps to SchedulerAPI `preview`;
- `admit` maps to atomic SchedulerAPI `admit`;
- Adapter executes the returned `RouteId`;
- Adapter reports terminal/interruption reconciliation to the provider;
- Scheduler updates reservation/meter/usage state.

Thus Scheduler extends the existing Adapter `sdp run` command without reverse imports or command replacement.

### 11.10 Scheduler persistence

Scheduler depends on Tracker and adds namespaced tables/migrations to the same user-global SQLite DB through Tracker storage SPI. Resource state remains Scheduler-owned and references public `ProjectKey`, `RunId`, `RouteId`, etc.

Scheduler may not modify Tracker-owned workflow tables directly.

## 12. Configuration ownership

Core owns the canonical configuration loader/resolution path and project identity. Extensions contribute namespaced validated sections through Core SPI.

Conceptual TOML:

```toml
[core]

[projects.mdstats]
repo = "/path/to/mdstats"
mode = "hybrid"

[tracker]
retention = "..."

[adapters]
# backend/model/route/benchmark configuration

[scheduler]
# ledgers/meter/prediction/admission policy
```

`ProjectKey` is the stable configuration key such as `mdstats`; Core therefore can identify projects without Tracker persistence.

Unknown config belonging to absent extensions is preserved/diagnosed rather than interpreted. Secrets are never serialized into ordinary config/history.

## 13. Persistence and ownership

Core is stateless across invocations except configuration and bounded prompt/cache artifacts needed for prompt operation.

Tracker introduces persistence. Higher modules extend it through Tracker SPI.

Rules:

- one SQLite file may contain tables from multiple installed extensions, but every table has one semantic owner;
- only the owner writes its tables;
- shared transactional substrate is exposed through Tracker SPI rather than private helper imports;
- semantic cross-module reads use public APIs, not another module's SQL tables;
- migration order follows dependency order;
- uninstalling/disablement of a higher extension must not make lower tables unreadable;
- raw prompt/output retention and numeric telemetry retention are separable;
- persisted state remains private local evidence, not repository authority.

## 14. CLI capability behavior

The CLI is cumulative and capability-driven.

### Core only

```text
sdp design
sdp implementation
sdp review
sdp prompt <stage>
sdp capabilities
sdp doctor
```

### Core + Tracker

Core prompt commands remain semantically identical, with Tracker event persistence added. Additional commands:

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

No quota-aware AUTO selection exists.

### + Scheduler

```text
sdp resources
sdp usage
sdp predict <stage> [--route <id>]
sdp schedule <stage> --explain
sdp run <stage>              # omitted route may use Scheduler AUTO policy
```

An explicit route bypasses ranking but not hard compatibility/safety checks or, when Scheduler is active, resource admission required by configured policy.

A failed Scheduler must not make Adapter explicit-run unavailable if Adapter remains healthy. A failed Adapter must not make Tracker/Core manual mode unavailable.

## 15. Extension failure and downgrade

Extension discovery/activation is not all-or-nothing.

Examples:

```text
Scheduler incompatible
  -> disable Scheduler
  -> Adapter explicit-run + benchmark recommendation still work

One Adapter transport unavailable
  -> disable that route/transport capability
  -> other Adapter routes and Tracker manual mode remain available

Tracker DB unavailable/corrupt
  -> Tracker reports non-closure/repair path
  -> dependent Adapter/Scheduler disable
  -> Core prompt rendering remains available
```

A higher extension may expose partial capabilities only when the remaining subset has a coherent documented contract. Do not advertise `agent.execute.v1` if only benchmark recommendation loaded.

## 16. Security and privacy boundaries

- Plugin discovery loads only installed package entry points, not arbitrary repository/user directories.
- Extension code executes in-process and is trusted-code-only; entry-point discovery is not a sandbox.
- External benchmark/meter responses are untrusted data: enforce byte/time/schema bounds before persistence/use.
- API keys/tokens are never embedded in benchmark caches, prompts, events, logs, or repository files.
- Web prompts contain sanitized remote repository identity and omit local paths/private account/resource state.
- Agent subprocess execution uses direct argv/structured transports, bounded output/time, and explicit permission handling.
- External benchmark data may influence recommendations but cannot execute commands or mutate repository state.
- Benchmark/source licensing and attribution metadata travels with cached observations.
- No module automatically injects complete historical transcripts into later prompts; only bounded structured state is automatic.

## 17. Benchmark freshness and recommendation integrity

Every recommendation using online benchmark data is reconstructible from `BenchmarkSnapshot`/`BenchmarkObservation` records.

Material context includes source, metric, benchmark/index version, source-generated/fetched time, model + effort + harness/config, value + uncertainty if available, identity-match quality, and staleness.

Do not compare values from incompatible benchmark/index versions as if they were one stable scale. Do not combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into a universal scalar without separate explicit design/validation.

The Adapter may rank lexicographically or by documented role-specific policy without inventing a universal score.

## 18. Architecture fitness rules

Objective dependency/API rules become executable once packages exist:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core public API/SPI only
Adapters    may import Core + Tracker public API/SPI only
Scheduler   may import Core + Tracker + Adapters public API/SPI only
```

Cross-module production imports must target `api.v1`/documented `spi.v1` paths. Static architecture tests reject reverse/private imports.

Additional durable checks:

- Core minimal-install smoke with higher distributions absent;
- Tracker minimal-install smoke without Adapter/Scheduler;
- Adapter minimal-install smoke without Scheduler;
- Scheduler full-stack smoke;
- extension activation failure degrades to highest healthy lower level;
- public API model serialization/round-trip compatibility fixtures;
- v1 error-code and idempotency behavior;
- API consumers do not import concrete/private implementation classes.

## 19. Module acceptance ladder

Each module is implemented, independently reviewed, and accepted before the next workplan begins.

### Prompt Module acceptance

Must prove:

- Core-only install/CLI works;
- project observation/workplan catalog/public CoreAPI work without Tracker;
- explicit stage command produces complete prompt with correctly resolved project/branch/workplan/protocol inputs;
- ambiguous workplans are not guessed;
- local/web privacy boundary is correct;
- `RunId` + prompt fingerprint v1 are deterministic/recomputable under the specified scheme;
- application/extension composition works with no extensions installed;
- Core public API/SPI compatibility fixtures exist;
- no Tracker/Adapter/Scheduler import or persistence requirement exists.

### Tracker Module acceptance

Must prove all Prompt acceptance still passes with/without Tracker, plus:

- Core events persist idempotently;
- manual response associates to correct run and duplicate ingest is idempotent;
- projection refreshes through public CoreAPI and handles candidate/workplan changes + PASS/NO-PASS correctly;
- status/history/graph survive restart;
- history paging is deterministic;
- Tracker storage SPI migrations/ownership work without private imports;
- deleting/disabling Tracker leaves Core usable.

### Adapter Module acceptance

Must prove all lower acceptance plus:

- explicit selected-route direct execution through real normalized transport boundary;
- start/events/respond/cancel/wait lifecycle works through fake protocol streams and representative real adapter smoke where available;
- permission/cancellation/terminal states are distinct;
- output is tracked automatically;
- benchmark refresh/cache/provenance/identity mapping works;
- Artificial Analysis/DeepSWE source failures degrade without fabricated scores;
- recommendation semantics distinguish Design intelligence from Implementation coding evidence;
- route-policy SPI works with no provider and with deterministic fake provider;
- no metering or resource-aware automatic route selection exists;
- disabling Adapter returns to Tracker manual mode.

### Scheduler Module acceptance

Must prove all lower acceptance plus:

- preview is read-only;
- admit atomically revalidates/selects/reserves;
- shared account ledgers and dual windows;
- cross-project atomic reservation;
- `UNMETERED_FOR_SCHEDULER` vs `UNKNOWN`;
- usage history/prediction/calibration;
- dynamic Review/reasoning reserve;
- PAYG/expiring-subscription decisions;
- Scheduler implements Adapter route-policy SPI without command replacement;
- automatic route selection only among engineering-sufficient routes;
- interruption/reconciliation/failover without false acceptance;
- disabling Scheduler restores Adapter explicit-route behavior.

## 20. Lossless module-workplan derivation

Implementation order is Frozen:

```text
WP-1  Prompt Module
WP-2  Tracker Module
WP-3  Adapter Module
WP-4  Scheduler Module
```

Each workplan must declare:

```text
parent_architecture: orchestrator/docs/architecture.md
parent_architecture_version: 1.1.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

Each workplan carries:

1. parent product/invariants relevant to the module;
2. module Frozen responsibilities/non-responsibilities;
3. exact lower public API/SPI contracts consumed;
4. public API/SPI surface it must establish for the next module;
5. module-specific affected surface/acceptance boundaries;
6. standalone-install acceptance with higher modules absent;
7. compatibility acceptance with all lower modules present;
8. simplification/reopen triggers.

A workplan must not pre-implement later modules merely to make future extension easier. The versioned API/SPI seams and stable IDs defined here are the justified future-facing surface; speculative meter/scheduler tables/classes in Core/Tracker are forbidden.

When a module passes independent Review, its accepted `api.v1`/required `spi.v1` semantics become the compatibility floor for subsequent workplans. A breaking change thereafter requires bounded parent/API Design reconsideration and a new API/SPI major or explicit compatibility/migration plan.

## 21. Versioning and evolution

Architecture versioning:

- major: breaks module ladder, authority model, dependency direction, or public API role boundaries;
- minor: backward-compatible architecture/API strengthening before/alongside module adoption;
- patch: clarification without semantic contract change.

Version 1.1.0 supersedes the initial 1.0.0 draft because the final pre-implementation review materially strengthened the API/SPI contract before WP-1 implementation.

Module package versions are independent but declare compatible lower API/SPI majors.

External benchmark/provider versions do not determine package versions. They are runtime data behind versioned source providers.

A new benchmark source normally implements Adapter SPI. A new agent transport normally implements Adapter SPI. A new meter/pricing source normally implements Scheduler SPI. These do not require Core changes unless the stable lower SPI is genuinely insufficient.

## 22. Active simplicity and redesign triggers

Simplify/reopen before adding machinery if implementation starts to create:

- multiple extension registries/plugin loaders;
- lower-module imports of higher modules;
- duplicated CLI composition paths or command replacement;
- both event history and a separate mutable workflow-authority database;
- benchmark-specific fields in Core model objects;
- quota/resource abstractions in Adapter/lower layers;
- duplicated model identity mapping per benchmark provider;
- backend-specific workflow logic instead of transport normalization;
- Scheduler-owned agent execution parallel to Adapter execution;
- public APIs exposing private SQL/backend/process objects;
- unbounded collection returns where history/telemetry can grow;
- broad exception-class hierarchies used instead of stable problem codes;
- hidden durable mutation in preview/query calls;
- stubs/fallbacks whose only purpose is preserving a broken higher extension when clean downgrade is possible.

Reopen this parent architecture only when evidence shows a Frozen boundary cannot satisfy the product, such as a required capability needing a reverse dependency, the single extension registry proving insufficient for safe composition, a public API role being fundamentally unable to support the next module without semantic breakage, or the chosen Adapter execution lifecycle being unable to represent a required supported agent safely.

Ordinary provider/API churn, new models, benchmark-version updates, new adapter flags, and predictor algorithm improvements are delegated changes and should not reopen parent architecture.

## 23. Final API/design review — 2026-09-07

The final pre-implementation review explicitly challenged whether the first lower APIs could support every later module without private imports, reverse dependencies, command replacement, or semantic reinterpretation.

Material gaps closed:

1. **Core observation gap:** Tracker previously needed fresh Git/workplan evidence but Core exposed only prompt rendering. `CoreAPI.observe/workplans` now owns that public read boundary.
2. **Prompt self-hash ambiguity:** Prompt fingerprint v1 now defines a non-recursive placeholder hash over the exact rendered artifact.
3. **Workplan identity gap:** `WorkplanRef` explicitly separates exact artifact digest from semantic authority digest so lifecycle closeout does not counterfeit semantic invalidation.
4. **Candidate identity gap:** `CandidateRef` carries dirty-state identity completeness rather than only branch/HEAD.
5. **Tracker idempotency/paging gap:** event recording and ingestion are idempotent, and unbounded history uses cursor pages.
6. **Persistence SPI gap:** higher modules can own namespaced SQLite tables/migrations without importing Tracker SQL internals; SQLite is honestly part of SPI v1.
7. **Adapter lifecycle gap:** one-shot `execute()` was insufficient. Adapter v1 now models `start/events/respond/cancel/wait` and normalized terminal results.
8. **Scheduler race gap:** read-only `preview` is separated from atomic revalidating `admit`, preventing stale schedule previews from becoming unreserved executions.
9. **CLI ownership gap:** Adapter owns `sdp run`; Scheduler extends omitted-route behavior through Adapter route-policy SPI instead of replacing the command or creating a reverse import.
10. **Plugin composition gap:** Core SPI now defines manifest, activation, service registry, config, CLI, event and diagnostic registration semantics.
11. **Provider extensibility gap:** Adapter/Scheduler now expose their own provider SPIs under the same single Core entry-point registry.
12. **Error/evolution gap:** APIs use stable problem codes, opaque IDs, cursor pages, additive-field compatibility, and explicit API/SPI major evolution instead of relying on exception text or concrete classes.
13. **PEP 420 packaging gap:** the root namespace-package file-ownership rule is explicit so separate distributions cannot mask one another.

The current benchmark design remains supported by current external interfaces: Artificial Analysis documents a versioned Intelligence Index in its Data API and DeepSWE publishes harness/model/effort-sensitive coding-agent results. Those are runtime evidence sources, not Frozen score values.

No remaining architecture-level blocker was found. The architecture is intentionally complete enough to derive WP-1 through WP-4 losslessly while leaving implementation algorithms/classes below the public boundaries delegated.

## 24. Design verdict

**PASS — architecture 1.1.0 is implementation-ready.**

The next active implementation contract should cover **WP-1 Prompt Module only**. WP-1 establishes Core, the CLI/composition root, Core API/SPI v1, repository/workplan observation, canonical prompt rendering, and prompt identity. It must not introduce Tracker persistence, agent adapters, benchmark network integration, or Scheduler/resource machinery.
