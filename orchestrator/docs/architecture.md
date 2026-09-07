---
kind: architecture
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.6.0
supersedes_architecture_version: 1.5.0
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

This architecture is Tier 1B Frozen architecture for the orchestrator implementation series. Module workplans derive implementation obligations losslessly from it. They may choose delegated realization details, but may not silently change dependency direction, authority boundaries, public API/SPI semantics, persistence ownership, capability roles, repository-containment rules, or module responsibilities.

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
19. **Route admission precedes final prompt rendering.** Selected route determines prompt context, so route admission occurs after route-independent Core preparation and before final execution prompt rendering.
20. **Run identity precedes scheduling and rendering.** Core allocates a RunId without persistence so Scheduler, prompt, Tracker, and Adapter share one attempt identity.
21. **Manual result tracking has a structured seam from day one.** Core prompts request a versioned terminal machine-readable result envelope with run/fingerprint identity.
22. **Protocol version binding is explicit.** An older workplan is never silently rendered through a newer incompatible workflow profile merely because the installed orchestrator is newer.
23. **One mutating run owns one local worktree.** Concurrent orchestrator-controlled mutating local executions against the same physical worktree are serialized through a cross-process lease keyed by worktree identity, not project name.
24. **Workflow routing authority is profile-owned.** Tracker may project history and recommend the next action, but it consumes the compatible Core Protocol profile's declared stage/routing contract rather than duplicating private prompt/profile logic.
25. **Uncertain routing remains uncertain.** Unknown result outcomes, blocker classes, or multiple materially valid next stages produce an explicit ambiguous recommendation rather than a guessed transition.
26. **Repository containment is Frozen.** All orchestrator-owned executable source, package/build metadata, tests, fixtures, package resources, developer scripts, and orchestrator documentation live under repository-relative `orchestrator/`. Protocol-standard workplans remain under `workplans/`; existing repository-level CI/config may contain only thin invocation/wiring that points into `orchestrator/`. No orchestrator implementation logic is placed in top-level `source/`, `tests/`, `tools/`, `scripts/`, or another sibling tree merely for convenience.

## 3. Capability ladder and distributions

### 3.1 Level 0 — Core / Prompt

```text
command
  -> observe configured repository/workplan/protocol inputs
  -> resolve requested stage under compatible Protocol profile
  -> prepare route-independent prompt context
  -> render canonical compatible prompt for selected prompt mode
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

## 4. Repository layout, Python packaging, and namespace

Repository containment is architectural; exact subdirectory naming beneath `orchestrator/` remains delegated. A conforming multi-distribution layout may be:

```text
orchestrator/
  docs/
    architecture.md
    ...
  packages/
    core/
      pyproject.toml
      src/
        sdp_orchestrator/
          core/
      tests/
      fixtures/
    tracker/
      pyproject.toml
      src/
        sdp_orchestrator/
          tracker/
      tests/
    adapters/
      pyproject.toml
      src/
        sdp_orchestrator/
          adapters/
      tests/
    scheduler/
      pyproject.toml
      src/
        sdp_orchestrator/
          scheduler/
      tests/
  scripts/                 # orchestrator-owned development/release helpers only
  tests/                   # optional cross-distribution integration tests
```

All of the above remain under `orchestrator/`. Existing Protocol source under `source/`, Protocol workplans under `workplans/`, and generated/install artifacts outside the repository are external authorities/integration outputs, not alternate orchestrator implementation locations. Repository-level `.github/...` or equivalent CI may invoke commands under `orchestrator/`, but reusable test/build/orchestration logic remains contained.

Use native PEP 420 namespace packaging. No distribution owns `sdp_orchestrator/__init__.py`.

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

Python raises `OrchestratorError(Problem)`. CLI uses `Problem.code` for deterministic exits/stderr. Modules add namespaced codes; callers do not parse human messages. User-facing problem serialization is JSON-safe and redacts credentials/sensitive local values according to the owning boundary.

### 5.6 Idempotency/mutation

Read-looking methods (`list/get/observe/status/preview/predict/recommend/probe/prepare/render`) are read-only unless explicitly documented. Durable writes return receipts/IDs where retry matters.

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

Normal extension loading uses:

```text
ExtensionManifest
  extension_id
  extension_version
  core_spi_spec
  requires_extensions
  requires_capabilities
  provides_capabilities
```

Use `packaging` version/specifier comparison. First-party IDs are reserved under `sdp.*`.

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Normal activation imports/loads trusted provider code, obtains a side-effect-minimal manifest, then activates in dependency-topological order. Failed providers disable dependents while lower healthy services remain.

`ApplicationRequest.activation_policy` supports at least:

```text
normal
 discovery_only
```

Discovery-only reads package/distribution entry-point metadata only. It does **not** import/execute provider code and therefore reports extensions as discovered/not-loaded rather than claiming unobserved provider health/capabilities. `sdp doctor` and `sdp capabilities` use discovery-only by default. Normal composition is the provider-loading path.

### 6.4 Service registry/application API

Services register by capability + API major + provider. Singular service cannot be silently replaced; multi-provider order is stable by provider ID.

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

Core owns config precedence: defaults -> config/profile -> documented environment allowlist -> explicit CLI/API. Absent-extension config is preserved/diagnosed. Secrets are references/approved secret inputs.

Event sinks register explicit event-type subscriptions during normal activation. Prompt-containing events are not broadcast to unsubscribed sinks. Core events are non-durable; sinks are idempotent by EventId and sink failure cannot counterfeit the primary operation result.

## 7. Core shared records

### 7.1 IDs

```text
ProjectKey
WorktreeKey
RunId
EventId
StageSelector
StageRef
CapabilityKey
ExtensionId
```

Route/model/backend/account/transport/effort identities belong to Adapter.

`StageSelector` is profile-neutral user/request input. `StageRef` includes Protocol-profile identity + protocol version + resolved stage key and is created only after compatible profile resolution.

`WorktreeKey` identifies one configured physical local worktree after canonical path/repository resolution. Different ProjectKeys targeting the same checkout resolve to the same WorktreeKey. Distinct Git worktrees resolve to distinct WorktreeKeys.

### 7.2 DigestRef

```text
DigestRef
  algorithm
  canonicalization_scheme | None
  value
```

Initial crypto is SHA-256. Domain digests carry versioned schemes such as `sdp.prompt-preparation.v1`, `sdp.prompt-fingerprint.v1`, `sdp.workplan-semantic.v1`, and `sdp.git-working-tree.v1`. Scheme semantics never change silently.

### 7.3 ProtocolProfileRef

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
  configured_prompt_mode
  protocol_profile
  configuration_identity
```

ProjectDescriptor is trusted local-process data, not auto-embedded in web prompts. `PromptProjectSnapshot` contains only prompt-mode-safe repository/workplan/candidate context; web mode excludes local paths/private state/secrets/account-resource telemetry/credential-bearing remotes.

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

Event types are namespaced/versioned. Events are evidence, not workflow authority; unknown future types may be stored opaquely.

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

`trigger_key` is a profile-defined opaque routing class, not executable expression text. The profile documents how normalized result facts map to trigger keys. Optional/context-dependent Protocol relations remain alternatives/ambiguous rather than being invented as deterministic edges.

The descriptor defines allowed/recognized routing relations, not an autonomous approval engine. Tracker may recommend only a transition compatible with the descriptor and current evidence. If evidence maps to zero or multiple materially plausible routing classes, recommendation is `AMBIGUOUS` rather than guessed.

### 7.9 StageResultEnvelope v1

Every rendered prompt requests an ordinary human-readable response followed by exactly one terminal uniquely marked machine-readable JSON footer representing:

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

Outcome, blocker classification, authority class, and check states are extensible strings. A profile may recognize some values and leave unknown values unresolved. `recommended_next_stage` is reported evidence/hint, not routing authority; Tracker reconciles it against WorkflowProfileDescriptor and blocker/outcome evidence.

The literal footer marker, terminal-block extraction rule, and exact accepted v1 schema fixture are frozen during WP-1 independent Review before Tracker depends on them. Core renders the result request but does not persist or interpret returned semantics.

## 8. Core / Prompt Module

### 8.1 Responsibilities

Core owns CLI/application composition, project/protocol-profile config, project catalog/worktree identity, read-only Git/workplan observation, compatible workflow-profile/stage catalog, governing-workplan resolution, compatible prompt-source resolution, canonical prompt loading/substitution, route-independent preparation, local/web final rendering, run/preparation/prompt/result-envelope identity, stdout/optional clipboard, and capability/doctor reporting.

Core does not own durable workflow history, next-stage inference, agent processes, benchmarks, resources, or scheduling.

### 8.2 Prompt mode versus canonical EXECUTION_MODE

Core's prompt-context selector is `PromptExecutionMode` with v1 values `local` and `web`. It answers where/how the final prompt will be consumed. It is deliberately distinct from the canonical SDP prompt INPUT `EXECUTION_MODE`, whose values such as `AUTO_EXECUTE` and `REPORT_ONLY` govern what the receiving agent is authorized to do.

Core config/CLI uses `default_prompt_mode` / `--prompt-mode`; generic prompt input may separately set `EXECUTION_MODE` when the selected canonical prompt declares it. Changing one does not silently change the other.

### 8.3 Observation policy

```text
ObservationPolicy
  remote_mode: local_only | use_cached_remote | refresh_remote
  max_remote_staleness | None
```

Programmatic default is local-only unless explicitly configured/requested. `refresh_remote` is a bounded non-mutating query such as `git ls-remote`, not fetch/pull. Results carry freshness/provenance. Unknown/stale beats hidden network I/O or invented freshness.

### 8.4 Workplan resolution and Protocol binding

Core owns exact stage-specific workplan resolution. Explicit selector is exact workplan ID or repository-relative path. A profile defines whether a stage requires, permits explicit-only, or disallows a workplan. Governing workplan `protocol_version` takes precedence over project default when resolving the compatible workflow profile. A missing/invalid/unsupported required protocol version fails rather than silently assigning a newer default.

### 8.5 Protocol profile and Core render-source resolution

Core resolves workflow semantics only through a compatible ProtocolProfileRef:

```text
explicit configured compatible local protocol source/profile
  -> exact compatible packaged prompt/profile snapshot
  -> explicitly permitted read-only canonical remote source/profile at one resolved immutable identity
  -> truthful incompatible/unavailable non-closure
```

Semantic protocol version is never guessed to be a Git ref/tag. Packaged snapshots are derived/version-bound artifacts, not independently edited authority.

`PromptSourceRef` is Core's provenance for where canonical prompt/profile material was read. It is distinct from the canonical agent-facing `PROTOCOL_SOURCE` INPUT, whose default remains `AUTO_LOCAL_FIRST`; Core local filesystem source paths therefore do not leak into web prompts. Canonical `PROTOCOL_REF` follows the governing Protocol contract.

### 8.6 Two-phase Core API

Core separates route-independent preparation from route-sensitive final rendering so higher modules can insert route admission without duplicating Core authority or rendering a provisional prompt.

```text
Core-only:
  allocate/prepare -> configured or explicit prompt mode -> render

Adapter/Scheduler:
  allocate/prepare
    -> Adapter/Scheduler admission
    -> render using admitted route.prompt_execution_mode
    -> Adapter.start
```

Public v1 surface:

```python
class CoreAPI(Protocol):
    def allocate_run_id(self) -> RunId: ...
    def projects(self, query: ProjectQuery | None = None) -> Page[ProjectDescriptor]: ...
    def get_project(self, project: ProjectKey) -> ProjectDescriptor: ...
    def observe(self, request: ProjectObservationRequest) -> ProjectObservation: ...
    def workplans(self, request: WorkplanQuery) -> Page[WorkplanDescriptor]: ...
    def resolve_workplan(self, request: WorkplanResolutionRequest) -> WorkplanResolution: ...
    def workflow(self, request: WorkflowRequest) -> WorkflowProfileDescriptor: ...
    def list_stages(self, request: WorkflowRequest) -> tuple[StageDescriptor, ...]: ...
    def prepare(self, request: PromptPreparationRequest) -> PreparedPrompt: ...
    def render(self, request: PromptRenderRequest) -> RenderedPrompt: ...
```

All are read-only with respect to target repositories. `resolve_workplan()` is the public owner of stage-specific selection; Tracker/Adapter do not reproduce it. `list_stages()` is a convenience view of the same workflow descriptor.

`PromptPreparationRequest` semantically carries optional RunId, ProjectKey, StageSelector, optional exact workplan selector, Design first task, declared input overrides, and ObservationPolicy; it intentionally carries no local/web prompt mode.

`PreparedPrompt` carries RunId, preparation fingerprint, resolved StageRef, ProjectObservation/CandidateRef, selected WorkplanResolution, WorkflowProfileDescriptor/ProtocolProfileRef, PromptSourceRef, classified/resolved mode-independent inputs with provenance, and requested result-schema identity.

`PreparedPrompt.preparation_fingerprint` uses versioned `sdp.prompt-preparation.v1`, SHA-256 over canonical JSON of the material mode-independent preparation identity. Volatile observation timestamps/diagnostics and unrelated extension config are excluded; material stage/candidate/workplan/profile/source/input identity is included.

`PromptRenderRequest` carries PreparedPrompt + `prompt_execution_mode: PromptExecutionMode(local|web)`. Render derives prompt-mode-safe target/context, revalidates material preparation identity, then returns final artifact. Candidate/workplan/mutable local Protocol-source drift produces a stale-context problem rather than a mixed snapshot.

### 8.7 Prompt input binding

Every canonical INPUT is profile-classified as:

```text
mechanical
canonical_default
required_user
```

Core never guesses a semantic user decision merely to produce a prompt. Canonical `REPOSITORY_TARGET`/equivalent is final-render mode-dependent mechanical context; `PROTOCOL_SOURCE` defaults to `AUTO_LOCAL_FIRST`; `PROTOCOL_REF` is governing-contract mechanical; canonical `EXECUTION_MODE` defaults to `AUTO_EXECUTE`; `ADDITIONAL_CONSTRAINTS` defaults to `NONE` where canonical source permits it.

Generic input overrides may set only declared inputs not exclusively owned by a first-class/mechanical binding. Concrete inserted values use deterministic structure-safe scalar representation; raw structural control injection is not spliced into the canonical INPUT grammar.

### 8.8 Prompt fingerprint/footer

Under `sdp.prompt-fingerprint.v1`, Core renders exact prompt bytes using a fixed fingerprint placeholder after RunId is known, hashes normalized placeholder-form UTF-8 bytes with SHA-256, then substitutes the digest. WP-1 freezes the placeholder, line-ending, terminal-newline, scalar normalization, and result-footer request fixtures.

Only successful final render emits `core.prompt.rendered.v1`, and only to explicitly subscribed sinks. Core constructs complete prompt bytes before writing stdout; failure produces no partial prompt artifact. Prompt stdout is prompt-only; diagnostics go to stderr. Optional clipboard is additive.

### 8.9 Core CLI/dependencies

Core exposes at least:

```text
sdp prompt <stage>
sdp baseline
sdp design
sdp implementation
sdp review
sdp verification
sdp stabilization
sdp alignment
sdp health-audit
sdp closeout
sdp projects
sdp capabilities
sdp doctor
```

Expected Core dependencies: platformdirs, typer, pydantic, python-frontmatter, packaging; clipboard extra may use pyperclip. No filelock/ACP/httpx/ML/higher-module requirement.

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

Status/next/graph consume public Core workflow descriptors plus fresh Core observations; they do not parse Core private profile/prompt files.

### 9.3 Manual result ingestion

Precedence: matching valid StageResultEnvelope -> bounded deterministic strong markers -> explicit user confirmation/selection. No mandatory LLM classification. Pasted data is untrusted and cannot execute orchestrator commands. Exact duplicate ingest is idempotent; mismatch fails safely unless explicitly rebound by user after disclosure.

If parsing cannot confidently determine a profile-recognized outcome/blocker class needed for routing, Tracker stores the evidence but reports next action as ambiguous.

### 9.4 RecordedEvent / projection / graph

```text
RecordedEvent
  sequence: monotonically increasing Tracker-local integer
  recorded_at
  event
```

Recording order differs from producer wall clock. DevelopmentProjection is bounded current summary; attempts remain in history. Execution status and semantic outcome are distinct.

Persistent workplan selection is private convenience used only while compatible with current Core evidence. WorkflowGraph uses Core WorkflowProfileDescriptor topology and overlays attempts/outcomes/current recommendation. Agent `recommended_next_stage` can corroborate but never override an incompatible profile transition.

### 9.5 Tracker storage/coordination SPI v1

Private root:

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/
  exports/
```

SQLite/WAL is v1 control store; owner-only filesystem permissions where supported. Higher modules add namespaced tables through Tracker-owned migrations/transactions and may not directly read/write another module's semantic tables.

```python
class TrackerStorageSPI(Protocol):
    def register_migrations(self, extension: ExtensionId, migrations: tuple[MigrationSpec, ...]) -> None: ...
    def transaction(self, extension: ExtensionId, *, write: bool) -> ContextManager[sqlite3.Connection]: ...
    def acquire_lease(self, request: LeaseRequest) -> LeaseRef: ...
    def renew_lease(self, request: LeaseRenewalRequest) -> LeaseRef: ...
    def release_lease(self, request: LeaseReleaseRequest) -> LeaseReceipt: ...
```

Lease requests carry extension owner, resource key, RunId/owner identity, TTL/renewal policy. Crashed/stale leases recover deterministically; duplicate acquire by same owner is idempotent. SQLite is explicitly part of this SPI major.

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

Admission consumes the Core `PreparedPrompt` identity/context or an equivalent public projection sufficient to bind RunId, project, resolved stage, workplan, candidate, profile, and task constraints. It may include an optional requested route plus interaction/manual/tool/privacy constraints.

No route-policy provider: admit explicit route or explicit configured default only. Active route-policy provider: explicit route is admitted unchanged or rejected; omitted route may AUTO select.

ExecutionAdmission returns selected route, prompt mode, candidate/preparation binding, optional policy admission ref, expiry/revalidation, and reason metadata.

For mutating local-worktree routes, Adapter acquires a Tracker coordination lease on WorktreeKey before start and holds/renews it through terminal/abandonment. Different ProjectKeys targeting the same WorktreeKey conflict.

### 10.5 Frozen execution flow

```text
Core.allocate_run_id / Core.prepare
  -> Adapter.admit(route explicit/default/AUTO policy; acquire required admission/lease)
  -> Core.render(same PreparedPrompt; prompt_execution_mode = admitted route.prompt_execution_mode)
  -> Adapter.start(exact admission + rendered prompt)
```

Start rejects RunId/preparation/stage/candidate/profile/prompt-mode mismatch or stale admission. Render/user-confirm failure before start invokes Adapter.abandon. Expiry is fail-safe, not normal cleanup.

### 10.6 Manual/direct lifecycle

Manual route start spawns no process; it returns awaiting-external-result handle + ManualHandoffArtifact. User response enters Tracker ingest; wait may observe completion/timeout. Direct process controls on manual route return structured unsupported problem.

Direct route start returns stable handle; events are cursor-paged normalized events; respond uses stable control-request IDs; cancel is idempotent; wait returns terminal result/timeout without destroying the underlying run automatically.

One RunId has at most one active execution. Ambiguous start/crash reconciles before retry. Worktree lease releases only after safe terminal/abandon reconciliation.

### 10.7 AgentRunResult

Separates process status from workflow semantics. Includes run/admission/route, configured route, ObservedExecutionIdentity + provenance/confidence, backend/session where available, visible final response, structured result, candidate observations, interruption/failure class, transport telemetry, and Tracker evidence. Planned and observed identity remain distinct. Zero exit is not workflow PASS.

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

Prefer ACP where conformant; use documented native structured RPC/SDK/JSON otherwise. PTY scraping is not primary when a structured interface exists. Initial families: Claude, Codex, OMP, Pi, Antigravity.

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

Benchmark providers fetch/normalize versioned observations preserving source/schema/version, fetched/generated time, digest/ETag, licensing/attribution, metric value/unit/uncertainty, external model identity, effort, harness/config, freshness, and identity-match quality.

Artificial Analysis is preferred current general-intelligence evidence; DeepSWE preferred current coding evidence. Exact endpoints/tiers are provider configuration. DeepSWE match quality remains `EXACT_CONFIG_MATCH`, `MODEL_EFFORT_PROXY`, `MODEL_ONLY_PROXY`, or `UNRESOLVED`. Never fabricate missing scores or a universal scalar combining incompatible metrics.

Role policy: Design/hard semantic work prioritizes general intelligence; Implementation prioritizes coding evidence; Review/Verification prioritize high general intelligence and may show provider/model independence secondarily.

ACP is optional transport dependency; bounded source HTTP may justify httpx. No Scheduler/ML requirement.

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

Preview is read-only; admit atomically re-observes resources, revalidates feasibility, selects/validates route, and creates reservations.

### 11.3 ScheduleRequest/idempotency

Request includes RunId, project/stage/task features, candidate/workplan/profile/preparation identity, Adapter candidate route snapshots, optional requested RouteId, interaction/manual constraints, and policy overrides.

Requested route evaluates exact route only. Omitted route AUTO may choose. Manual route requires allowed handoff; unattended requires automatable route.

Admission fingerprint covers all feasibility/reservation semantics. Same RunId+fingerprint retry returns same live admission; conflicting live request fails. Release handles never-started admission; expiration is fail-safe. Reconcile is idempotent.

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

`UNMETERED_FOR_SCHEDULER`, `METERED`, and `UNKNOWN` remain distinct. Shared account quota is represented once/referenced by routes; dual windows are simultaneous constraints. Opaque quota remains provider units; PAYG uses versioned pricing.

### 11.5 Meter SPI/reservations

```python
class AccountMeterProvider(Protocol):
    def descriptor(self) -> MeterDescriptor: ...
    def observe(self, request: MeterRequest) -> MeterSnapshot: ...
```

Prefer official/machine-readable sources; browser scraping is not normal. Preserve source/unit/time/freshness/confidence/account.

Metered execution reserves predicted capacity across consumed ledgers atomically. Manual/unmetered route may have no quota reservation but still has admission identity. Crash before authoritative post-meter keeps an uncertainty hold; current provider meters/hard limits outrank stale predictions.

### 11.6 Prediction/scheduling

Predict distributions for runtime, per-ledger consumption, token categories where relevant, monetary cost, stage-quality completion probability, interruption probability, and future repair rounds. Cold start uses interpretable priors by stage/role x model x effort x backend/transport with project corrections; early learning uses empirical quantiles/EWMA/shrinkage without mandatory ML; persist calibration.

AUTO exists only when Scheduler is active. Apply hard feasibility before ranking. Feasibility includes capability/effort, tools/skills, repository access, privacy, independence, backend health, interaction, predicted capacity, and protected future Review/Design reserve. Ranking may consider quality completion, interruption, future capacity, expiring-quota opportunity cost, PAYG cost, handoff/continuity, independence/diversity, and latency.

### 11.7 Adapter integration/persistence

Scheduler implements Adapter route-policy SPI. Adapter supplies candidate routes/request; Scheduler validates/selects/reserves; Adapter renders/starts; pre-start failure abandons/releases; terminal/manual completion reconciles.

Scheduler adds namespaced tables/migrations to Tracker user-global SQLite through Tracker SPI. Quota/account state is global across projects. No Tracker workflow-table mutation.

### 11.8 Scheduler availability policy

Standalone Adapter operation remains valid when Scheduler is not installed/enabled.

If Scheduler was configured as required and fails activation/becomes unavailable, Adapter does not silently treat it as absent for a resource-governed run. AUTO is unavailable and such execution fails closed or requires an explicit user-approved downgrade/override according to configuration. Unmetered/manual routes may remain available when policy permits.

## 12. Configuration ownership

Core owns canonical config/project identity. Extensions contribute namespaced validated sections.

```toml
[core]

[projects.mdstats]
repo = "/path/to/mdstats"
default_prompt_mode = "web"

[tracker]
# retention/history

[adapters]
# routes/backends/models/benchmark sources

[scheduler]
# ledgers/meters/prediction/admission/failure policy
```

Unknown absent-extension sections are preserved/diagnosed. Secrets are references/approved secret inputs, never ordinary snapshots/history.

## 13. Persistence/event ownership

Core is stateless across invocations except config/bounded prompt-profile cache. Tracker introduces persistence; higher modules extend through Tracker SPI.

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

Additional canonical stage aliases may be exposed by the compatible workflow profile.

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

No resource-aware AUTO. Manual routes remain valid.

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
- Discovery-only diagnostics do not import/execute extension providers.
- Pasted agent output, structured results, benchmark/meter responses, and remote metadata are untrusted data: enforce size/time/schema bounds; never execute embedded instructions as control commands.
- API keys/tokens never enter prompts/caches/events/logs/repositories.
- Web prompt context excludes local paths/private state/account-resource telemetry/credential remotes.
- ProjectDescriptor local path stays local-process data.
- Agent subprocesses use direct argv/structured transport with explicit permission policy; no dangerous bypass default.
- Historical transcripts are not auto-injected into later prompts; only bounded structured projection is automatic.
- Benchmark licensing/attribution travels with cache.
- Private state/export files use restrictive permissions where platform supports; export is explicit user action.

## 17. Benchmark integrity

Recommendations reconstruct from source snapshots/observations preserving source, metric, benchmark/index version, generated/fetched time, model+effort+harness/config, value/uncertainty, identity match, and staleness. Do not compare incompatible benchmark versions as one scale or combine Artificial Analysis Intelligence Index and DeepSWE pass@1 into a universal scalar absent separate validated design.

## 18. Executable architecture fitness

Static checks once packages exist:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core public API/SPI only
Adapters    may import Core + Tracker public API/SPI only
Scheduler   may import Core + Tracker + Adapters public API/SPI only
```

Also enforce:

- every orchestrator-owned repository implementation/test/package/doc/script path is under `orchestrator/` except Protocol-standard workplans and minimal repository-level invocation wiring;
- native namespace packaging with no root `sdp_orchestrator/__init__.py`;
- one extension group;
- no private cross-module imports;
- one ownership of `sdp run`;
- no Scheduler process runner;
- Tracker graph/next-action use public Core workflow profile rather than private profile parsing;
- Adapter/Scheduler use Core preparation/workplan/profile services rather than duplicating resolution.

## 19. Module acceptance ladder

Each module is implemented, independently reviewed, and accepted before the next.

### WP-1 Prompt

Prove Core-only install/CLI; all orchestrator implementation files contained under `orchestrator/`; project/worktree identity; RunId allocation; local observation/workplan paging/resolution; Protocol-profile version binding and exact compatible snapshot resolution; StageSelector -> StageRef and WorkflowProfileDescriptor fixtures; route-independent prepare + final render; preparation/prompt digest schemes; explicit remote observation; prompt privacy; ambiguity; terminal StageResultEnvelope/BlockerRecord fixture; extension discovery/activation boundaries; API/SPI/error serialization; no higher imports/persistence.

### WP-2 Tracker

Re-prove Prompt with/without Tracker plus event/result idempotency; structured/manual ingest precedence; blocker/outcome classification and ambiguous-route behavior; run association; fresh Core observation; next-action/graph use of public WorkflowProfileDescriptor; deterministic history; subordinate workplan selection; persistence/restart; storage/migration/lease SPI; lease crash recovery; restrictive state permissions; Core usable without Tracker; all Tracker code/tests/resources contained under `orchestrator/`.

### WP-3 Adapter

Re-prove lower plus manual/direct routes; Core prepare -> pre-render admission -> Core render -> start; explicit/default behavior; route-policy no/fake provider; admission abandon; prompt-mode/profile/preparation binding; same-worktree mutating-run exclusion across ProjectKeys/processes; start/events/respond/cancel/wait; planned-vs-observed identity; tracking; benchmark identity/provenance/failure degradation; no quota AUTO; Adapter code/tests/resources contained under `orchestrator/`.

### WP-4 Scheduler

Re-prove lower plus read-only preview; atomic/idempotent admit; pre-start release; explicit route no substitution; AUTO; manual scheduling; shared/dual-window ledgers; cross-project reservations; UNMETERED vs UNKNOWN; prediction/calibration; future reserve; PAYG/expiring quota; idempotent reconcile/uncertainty; route-policy integration; configured-required Scheduler failure does not silently bypass policy; disabled/not-installed Scheduler restores intended Adapter mode; Scheduler code/tests/resources contained under `orchestrator/`.

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
parent_architecture_version: 1.6.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

Each carries relevant parent invariants, responsibilities/non-responsibilities, consumed lower APIs/SPIs, public API/SPI established, repository-containment obligation, affected/acceptance surface, standalone acceptance, lower-stack compatibility, and simplification/reopen triggers. Do not pre-implement later modules merely for future convenience.

## 21. Versioning/evolution

Architecture major breaks ladder/authority/dependency/API role; minor is backward-compatible strengthening before/alongside adoption; patch is clarification.

`1.6.0` supersedes `1.5.0` because the final WP-1 closure review exposed two parent-authority gaps before implementation: Core needed the public route-independent `prepare`/workplan-resolution/profile-resolution seam implied by the already-Frozen admission-before-render architecture, and the stakeholder explicitly froze repository containment of orchestrator implementation under `orchestrator/`. This version also names `PromptExecutionMode` separately from the canonical SDP `EXECUTION_MODE` input and records passive package-metadata-only extension discovery so the lower API can be implemented without semantic collision.

Module package versions are independent. New benchmarks/transports/meters use owning SPIs. Ordinary provider/model/benchmark/flag/predictor churn does not reopen parent architecture unless a Frozen boundary is insufficient.

## 22. Active simplicity/reopen triggers

Reopen/simplify before multiple plugin loaders, reverse dependencies, duplicated CLI composition, separate mutable workflow authority, Tracker private parsing of Core profile files, a generic workflow-expression engine where profile transition descriptors suffice, benchmark fields in Core, quota abstractions below Scheduler, duplicated model identity mapping, backend-specific workflow logic, Scheduler process execution, private SQL/process objects in public API, hidden preview writes, provisional prompts used merely for admission, duplicated workplan/profile resolution outside Core, orchestrator implementation/test/build logic outside `orchestrator/`, or stubs preserving broken higher layers instead of downgrade.

Reopen parent only if evidence shows required reverse dependency, single registry insufficiency, WorkflowProfileDescriptor unable to encode required Protocol routing without a materially different owner, public API role unable to support the next module without semantic break, protocol-profile model insufficient for compatibility, execution lifecycle unable to represent a required backend safely, or the `orchestrator/` repository-containment boundary irreconcilably conflicts with an independently required build/release mechanism that cannot be expressed through thin repository-level invocation wiring.

## 23. Final pre-implementation review closure — 2026-09-07

Across repeated independent review passes, material pre-freeze gaps were closed before any module implementation began:

1. capability identity separated from API version and provider compatibility became explicit;
2. Core exposes trusted local project/worktree data separately from prompt-safe web context;
3. repository/workplan observation has explicit network/freshness policy;
4. WorkplanRef/CandidateRef have versioned conservative identity semantics;
5. Tracker history is idempotent/paged/deterministically ordered and owns a namespaced SQLite/lease substrate;
6. direct agent execution uses explicit admission/start/events/respond/cancel/wait rather than a one-shot call;
7. manual-web is a first-class route, while planned and observed model identities remain separate;
8. route admission occurs before route-sensitive prompt rendering, with pre-start abandonment/release;
9. explicit Scheduler routes are admitted unchanged or rejected, not silently substituted, and reservations/reconciliation are idempotent;
10. Protocol prompt/profile resolution is version-bound and cannot silently reinterpret older workplans;
11. mutating local executions serialize by physical WorktreeKey rather than ProjectKey;
12. configured-required Scheduler failure cannot silently bypass resource policy;
13. Core requests a stable terminal StageResultEnvelope and Tracker uses structured-first/manual-safe ingestion;
14. Core exposes WorkflowProfileDescriptor stage/transition semantics and structured BlockerRecord classification so Tracker next-action/graph logic does not duplicate private Protocol routing authority;
15. Core now exposes route-independent `prepare`, stage-specific `resolve_workplan`, profile-aware `workflow`, and final `render` so Adapter/Scheduler can honor admission-before-render without duplicating Core authority or creating provisional prompt artifacts;
16. local/web `PromptExecutionMode` is distinct from canonical agent `EXECUTION_MODE`;
17. discovery-only diagnostics stop at package metadata and do not execute extension providers;
18. all orchestrator-owned implementation, package, test, fixture, script, and documentation files are contained under repository-relative `orchestrator/`, with only Protocol-standard workplans and minimal repository-level invocation wiring outside that boundary.

No remaining architecture-level blocker is known. The cross-module seams are specific enough to derive WP-1 through WP-4 losslessly, while module-local algorithms/classes remain delegated. Further speculative generalization should be rejected unless implementation evidence triggers a stated reopen condition.

## 24. Design verdict

**PASS — architecture 1.6.0 is implementation-ready.**

The active implementation contract is WP-1 Prompt Module. It establishes Core, CLI/composition, Core API/SPI v1, RunId/ProjectKey/WorktreeKey/ProtocolProfileRef identity, repository/workplan observation and resolution, WorkflowProfileDescriptor, route-independent prompt preparation, compatible canonical final prompt rendering, StageResultEnvelope/BlockerRecord request schema, preparation/prompt identity, and repository containment under `orchestrator/`. It must not introduce Tracker persistence, agent integration, benchmark networking, or Scheduler/resource machinery.
