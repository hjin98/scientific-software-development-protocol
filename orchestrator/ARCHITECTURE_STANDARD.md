---
kind: architecture-standard
architecture_id: SDP-ORCHESTRATOR
architecture_version: 1.0.0
protocol_version: 5.16.0
status: frozen
frozen_date: 2026-09-07
---

# SDP Orchestrator Architecture Standard

## 1. Purpose and authority

This document is the parent architectural authority for the Protocol Orchestrator. It replaces the earlier monolithic implementation-plan shape with a **nested capability ladder** whose lower levels remain independently useful and installable.

The product must be implementable and releasable one coherent module at a time:

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

This manual is **Tier 1B Frozen architecture** for the orchestrator implementation series. Individual module workplans derive implementation obligations from it and may choose lower-level realization details, but may not silently change the dependency direction, authority boundaries, public API roles, persistence ownership, or capability semantics defined here.

The manual is intentionally more durable than an implementation workplan. Module workplans must remain snapshot-complete for their module-specific obligations while referencing this supplied architecture authority. If implementation evidence invalidates a Frozen choice, reopen only the affected architecture surface before changing it.

## 2. Product invariants

1. **Progressive usefulness.** The smallest installation performs a useful job by itself: resolve and print a complete Protocol prompt. Each extension adds capability without making the lower mode incomplete.
2. **Strict asymmetric dependencies.** `core <- tracker <- adapters <- scheduler`. Reverse or lateral dependency is forbidden.
3. **Graceful degradation.** If an optional extension is absent, disabled, incompatible, or fails activation, the application falls back to the highest healthy lower capability level. Core prompt rendering must remain available unless Core itself is broken.
4. **One CLI, one composition root.** The `sdp` executable is owned by Core. Extensions register capabilities and commands through one versioned extension SPI; Core does not contain scattered `try import tracker/adapters/scheduler` branches.
5. **Public APIs are versioned compatibility contracts.** Higher modules consume lower modules only through documented `api.vN` surfaces and explicitly designated `spi.vN` extension contracts, never private implementation modules.
6. **No duplicated workflow authority.** Git, workplans, compatible Protocol profiles, and Design/Implementation results remain the semantic authorities. Tracker history is evidence; benchmark data is recommendation evidence; Scheduler resource models choose routes only.
7. **Manual operation remains first-class.** Tracker works with copy/pasted agent input/output. Adapter direct execution is an extension, not a prerequisite for workflow tracking.
8. **Static capability recommendation precedes resource scheduling.** Adapter may recommend models/routes using external benchmark evidence, but does not meter quota, learn resource consumption, or automatically route work. Scheduler owns those functions.
9. **Benchmark observations preserve context.** Intelligence/coding numbers are never flattened into timeless scalar properties of a model. Source, benchmark/version, model identity, effort, harness/context, uncertainty, freshness, and identity-match quality remain attached.
10. **Scheduler remains subordinate to workflow intent.** It may choose an execution route only after a required stage has been determined and only among engineering-sufficient routes.
11. **Private state remains outside project repositories.** Tracker and higher modules persist history/telemetry under the user-local state root, never in the protocol repository or target software repository by default.
12. **Subset acceptance is permanent.** A later module is not allowed to make an earlier module's standalone acceptance tests fail or require higher-module installation.

## 3. Capability ladder and install profiles

### 3.1 Level 0 — Core / Prompt Module

Required product capability:

```text
command -> resolve repository/workplan/protocol inputs -> print complete prompt
```

No durable development history, direct agent execution, benchmark refresh, metering, or scheduling is required.

### 3.2 Level 1 — Tracker Module

Adds:

- persistent development-cycle history;
- prompt/output association;
- manual response ingestion;
- current stage/progress projection;
- active/retired workplan tracking;
- next-action recommendation;
- text/JSON history and workflow graph.

All agent interaction may still be manual copy/paste.

### 3.3 Level 2 — Adapter Module

Adds:

- configured agents/backends/accounts/models/effort levels;
- ACP/native structured agent execution;
- explicit one-command execution of a user-selected route;
- current model-capability benchmark collection;
- static capability recommendations for stages/tasks.

There is **no quota metering, usage prediction, or automatic route selection** at this level. A route is explicitly selected by the user or by an explicit user-configured default.

### 3.4 Level 3 — Scheduler Module

Adds:

- account/resource ledgers and meters;
- usage telemetry and attribution;
- quota reservations;
- task feature extraction;
- usage/outcome prediction;
- quota/cost-aware route feasibility and scoring;
- default `AUTO` route selection;
- receding-horizon rescheduling/failover.

Scheduler reuses Adapter execution, Adapter capability evidence, and Tracker history. It does not create a second transport or workflow engine.

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

Exact build/workspace tooling is delegated, but the dependency graph is Frozen.

Installing a higher distribution must install its required lower distributions through ordinary package dependencies. Installing Core alone must not pull Tracker, Adapter, Scheduler, ACP, database-locking, benchmark-network, or ML-only dependencies unless Core genuinely needs them.

## 4. Python namespace and compatibility surfaces

Use the shared PEP 420 namespace `sdp_orchestrator` so separate distributions can contribute subpackages without file ownership conflicts.

Public surfaces:

```text
sdp_orchestrator.core.api.v1
sdp_orchestrator.tracker.api.v1
sdp_orchestrator.adapters.api.v1
sdp_orchestrator.scheduler.api.v1
```

Extension/service-provider surfaces are separately identified as SPI:

```text
sdp_orchestrator.core.spi.v1
sdp_orchestrator.tracker.spi.v1      # only if persistent extension storage/events require it
```

Rules:

- higher modules may import lower `api.v1` and explicitly documented `spi.v1` only;
- lower modules never import a higher module;
- no module imports another module's `_internal`, repository implementation, SQL table module, CLI implementation, or backend-specific private code;
- a breaking public contract creates `api.v2`; do not silently reinterpret `api.v1`;
- backward-compatible optional fields/methods may extend a public major when ordinary semantic-version compatibility is preserved;
- persisted schemas have their own migration/schema versions and are not equated with Python API versions.

The first accepted release of a module makes its `api.v1` semantics a compatibility contract for higher modules. Exact private classes and helper layout remain Tier 2.

## 5. Core composition and extension discovery

### 5.1 One extension registry

Core discovers installed extensions through Python package entry points under a single group:

```text
sdp_orchestrator.extensions.v1
```

Do not scan arbitrary directories and import arbitrary files as plugins.

Each extension exposes a side-effect-minimal manifest before activation:

```text
ExtensionManifest
  extension_id
  extension_version
  spi_major
  requires_extensions
  provides_capabilities
  optional_capabilities
```

Version/specifier comparison should use the maintained `packaging` library rather than custom semantic-version parsing.

Activation order is dependency-topological. An incompatible or failed extension is disabled together with dependents, while healthy lower levels continue. `sdp capabilities` and `sdp doctor` report the reason.

### 5.2 Capability identifiers

Capabilities use stable opaque identifiers rather than concrete implementation class names. Initial capability classes include:

```text
prompt.render.v1                 # Core
workflow.track.v1                # Tracker
workflow.project.v1              # Tracker
agent.catalog.v1                 # Adapter
agent.execute.v1                 # Adapter
benchmark.catalog.v1             # Adapter
benchmark.recommend.v1           # Adapter
auto_route.schedule.v1           # Scheduler
resource.meter.v1                # Scheduler
usage.predict.v1                 # Scheduler
```

Capability identifiers describe semantic services, not package presence. A package may be installed but disabled/incompatible and therefore not provide its capability.

### 5.3 Event envelope

Core owns a minimal versioned event envelope that lets Tracker record events from present and future modules without Tracker becoming tightly coupled to every producer:

```text
EventEnvelope
  event_id
  event_type                 # namespaced string, e.g. core.prompt.rendered.v1
  schema_version
  occurred_at
  project_key
  run_id?                    # absent for non-run events
  producer_extension
  payload                    # JSON-compatible producer-owned schema
```

Events are evidence, not workflow authority. Tracker may persist unknown future event types as opaque events while only projecting semantics it understands.

## 6. Common stable domain identifiers

Avoid large cross-module base classes. Freeze only identifiers that genuinely cross module boundaries:

```text
ProjectKey       stable user-local project identifier
RunId            UUID/opaque identifier allocated by Core for each prompt/run attempt
StageRef         protocol-profile identity + stage key
WorkplanRef      workplan id/path/protocol binding + exact artifact identity where available
CandidateRef     sanitized repository/branch/commit/dirty identity where available
RouteId          opaque Adapter-owned execution-route identifier
CapabilityKey    opaque extension capability identifier
```

Stage names, effort levels, model names, provider names, benchmark metric names, and future protocol stages are data, not closed Python enums. Use validated string/value objects with source/profile identity so new models/stages/efforts do not require a Core release.

## 7. Core / Prompt Module standard

### 7.1 Responsibilities

Core owns:

- `sdp` CLI bootstrap and extension registry;
- project configuration sufficient to locate a target repository and compatible Protocol prompt source;
- read-only Git/repository/workplan inspection required for prompt inputs;
- protocol-profile/stage catalog;
- canonical prompt loading and declared-input substitution;
- local/web prompt rendering;
- prompt/run identity and fingerprinting;
- stdout output and optional clipboard integration;
- capability/doctor reporting.

Core does **not** own durable workflow history, next-stage inference from past agent results, agent processes, benchmark data, resource meters, or scheduling.

### 7.2 Prompt public API v1

Semantic contract:

```python
class PromptAPI:
    def list_stages(self, project: ProjectKey) -> Sequence[StageDescriptor]: ...
    def render(self, request: PromptRequest) -> RenderedPrompt: ...
```

`PromptRequest` minimally conveys:

- project;
- stage reference;
- execution mode (`local` or `web`);
- optional explicit workplan selector;
- optional first-task description;
- explicit input overrides.

`RenderedPrompt` minimally conveys:

- `run_id` allocated by Core;
- final prompt text;
- stable prompt fingerprint;
- stage/profile identity;
- canonical prompt-source identity/version/hash;
- resolved input values with provenance;
- sanitized repository/workplan observation used for rendering.

Exact Pydantic field names may be finalized by the Prompt Module workplan while preserving these semantics.

### 7.3 Run/result envelope from day one

Core always allocates a non-secret `RunId` and computes the final prompt fingerprint even when Tracker is not installed. The rendered prompt includes a compact orchestrator footer requesting that an agent echo the run identity/fingerprint in any structured result when possible.

This is not persistence and does not make Tracker mandatory. It gives later Tracker/Adapter installations a stable association primitive without changing the already-released prompt API.

### 7.4 Prompt command behavior

Core commands must be sufficient for the immediate product:

```text
sdp prompt <stage>
sdp design
sdp implementation
sdp review
... protocol-profile stage aliases ...
```

The default stdout contract for a prompt command is the **complete copy/paste-ready prompt**. Diagnostics, capability warnings, and recommendation prose must not contaminate machine-pipeable prompt stdout; use stderr or explicit diagnostic commands.

If workplan selection is ambiguous, Core asks for or requires a bounded `--workplan` choice rather than guessing by mtime. Design with no workplan may require `--task`.

Core must operate offline using a compatible packaged prompt snapshot when configured repository information is local and sufficient.

### 7.5 Core dependencies

Core should remain small. Expected justified dependencies:

- `platformdirs`;
- `typer`;
- `pydantic`;
- `python-frontmatter`;
- `packaging`.

Clipboard support may be a small optional Core extra using `pyperclip`; stdout remains mandatory and sufficient.

Core must not require `filelock`, `agent-client-protocol`, `httpx`, an ML library, or Scheduler/Tracker code merely for future convenience.

## 8. Tracker Module standard

### 8.1 Responsibilities

Tracker adds persistent development history while preserving manual agent I/O.

It owns:

- one user-local SQLite control database and migrations;
- project registration/history partitioning;
- prompt recording from Core events;
- pasted/output artifact storage according to retention policy;
- structured-result parsing/association;
- workplan observations and lifecycle history;
- development-stage projection from current repository evidence + recorded results;
- stale/ambiguous/inconsistent evidence handling;
- next-action recommendation;
- status/history/workplans/graph interfaces;
- private-state retention/export/purge.

Tracker does not run agents or rank models from online benchmarks.

### 8.2 Tracker public API v1

Semantic contract:

```python
class TrackerAPI:
    def record(self, event: EventEnvelope) -> None: ...
    def ingest(self, request: IngestRequest) -> IngestResult: ...
    def status(self, project: ProjectKey) -> DevelopmentProjection: ...
    def next_action(self, project: ProjectKey) -> NextAction: ...
    def history(self, query: HistoryQuery) -> Sequence[EventEnvelope]: ...
```

Tracker binds outputs to Core-created `RunId`/prompt fingerprints. Wrong-run or ambiguous pasted output must fail safely or require explicit bounded confirmation.

The development projection remains derived. A stored `PASS` does not override a changed candidate/workplan/protocol identity.

### 8.3 Tracker storage standard

Tracker introduces the private user-global state root. The initial shape is conceptually:

```text
<platform state>/sdp-orchestrator/
  orchestrator.sqlite
  projects/<project-key>/raw/       # optional bounded raw events/transcripts
  exports/                           # explicit user action only
```

SQLite is the v1 durable control store. WAL mode is appropriate for single-user multi-process operation.

Tracker owns schema migration coordination. Higher first-party modules may register **namespaced extension migrations** through a designated Tracker SPI, but may not alter Tracker-owned tables directly. Each extension owns its tables/data semantics. Shared references use stable public IDs such as `RunId`, `ProjectKey`, and `RouteId` rather than imports of another extension's private repository objects.

`filelock` is introduced here for migration/process coordination and future per-project run ownership. Core alone does not need it.

### 8.4 Tracker CLI additions

Expected commands/capabilities:

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

## 9. Adapter Module standard

### 9.1 Responsibilities

Adapter adds explicit direct agent execution and capability evidence, but **not resource-aware automatic routing**.

It owns:

- agent/backend transport profiles;
- account/credential references without storing raw secrets;
- model/effort catalog;
- execution routes;
- ACP/native structured transport integration;
- explicit route execution;
- benchmark-source plugins, caching, identity matching, and capability recommendation;
- route health/capability probing;
- automatic ingestion of direct-run visible output/results into Tracker.

### 9.2 Route model

Keep the following identities separate:

```text
ModelRef
BackendRef / HarnessRef
AccountRef
TransportRef
EffortRef
ExecutionRoute(RouteId)
```

A route is a configured combination, not a model alias:

```text
Route = backend + account + transport + model + effort + repository-access mode
```

Scheduler later attaches resource-ledger mappings; Adapter does not need quota state to define a route.

### 9.3 Adapter public API v1

Semantic contract:

```python
class AdapterAPI:
    def routes(self, project: ProjectKey | None = None) -> Sequence[ExecutionRoute]: ...
    def probe(self, route: RouteId) -> RouteCapabilitySnapshot: ...
    def recommend(self, request: RecommendationRequest) -> RecommendationSet: ...
    def execute(self, request: ExplicitExecutionRequest) -> AgentRunResult: ...
```

`ExplicitExecutionRequest` requires an explicit `RouteId` or an explicit user-configured default route. Adapter must not choose a route because it has the highest benchmark score. If no route is selected, it may present recommendations and require a choice.

### 9.4 Agent transports

Use one normalized transport/result/permission boundary. Prefer the official `agent-client-protocol` Python client when a backend exposes sufficiently conformant ACP behavior; use documented native structured RPC/SDK/JSON fallbacks where needed.

Initial supported backend families remain Claude, Codex, OMP, Pi, and Antigravity. Exact command flags and ACP/native selection are delegated and capability-probed.

Adapter dependencies may include:

- `agent-client-protocol` for ACP;
- `httpx` for bounded benchmark/source HTTP access and future structured remote integrations.

No PTY scraping should be the primary supported interface when a structured transport exists.

### 9.5 Benchmark-source abstraction

External benchmark data is a **versioned observation source**, not model truth.

Public/extension semantics:

```python
class BenchmarkSource:
    def fetch(self, request: BenchmarkFetchRequest) -> RawBenchmarkSnapshot: ...
    def normalize(self, raw: RawBenchmarkSnapshot) -> BenchmarkSnapshot: ...
```

`BenchmarkSnapshot` preserves:

- source id/name and attribution;
- source endpoint/version/schema identity;
- fetched timestamp and upstream-generated timestamp when available;
- content hash/ETag where available;
- benchmark/index version;
- observations;
- source/license/usage-policy metadata needed for safe caching/display.

`BenchmarkObservation` preserves:

- metric id and direction (`higher_is_better` etc.);
- numeric value and unit;
- uncertainty/confidence interval when published;
- model/source identity;
- effort/reasoning setting when relevant;
- benchmark harness/configuration when relevant;
- benchmark/source version;
- freshness;
- identity-match quality to an internal model/route.

Never overwrite these dimensions with a single timeless `model.intelligence` or `model.coding_score` field.

### 9.6 Artificial Analysis source

Current preferred source for general reasoning/intelligence evidence is the official Artificial Analysis Data API. As of the architecture freeze, its documented Free language-model endpoint is:

```text
GET https://artificialanalysis.ai/api/v2/language/models/free
```

It requires a user-owned API key and returns headline indices including the Artificial Analysis Intelligence Index with an index-version field. The source adapter must:

- keep the API key in an approved secret input, never the Tracker DB or public repo;
- prefer stable upstream model/creator identifiers over display-name matching;
- record `intelligence_index_version` and source freshness;
- obey current API terms/attribution and response rate-limit headers;
- cache privately and avoid redistributing cached Artificial Analysis data through this public repository/package unless licensing explicitly permits it;
- degrade to last-known-good attributed data or `UNAVAILABLE`, never fabricate a score.

Current request quotas/tiers are provider policy, not architecture constants; do not hard-code a numeric daily limit into recommendation semantics.

### 9.7 DeepSWE source

Current preferred coding-capability evidence is DeepSWE. The official current v1.1 public artifact exposes configuration rows at:

```text
https://deepswe.datacurve.ai/artifacts/v1.1/leaderboard-live.json
```

The artifact identifies rows by **harness + model + reasoning effort** and publishes pass rate/pass@1, confidence information, cost/token/step statistics, task count, and generation timestamp.

The source adapter must therefore distinguish:

```text
EXACT_CONFIG_MATCH      internal route maps to same model + effort + compatible harness
MODEL_EFFORT_PROXY      model + effort match but benchmark harness differs
MODEL_ONLY_PROXY        only model-level evidence is safely attributable
UNRESOLVED              identity is ambiguous
```

DeepSWE score under `mini-swe-agent` is not silently relabeled as an observed Codex/Claude-Code route success rate. It may serve as a coding prior with its benchmark context and transfer quality shown.

The current v1.1 endpoint is a source-adapter default, not Frozen forever. The adapter must support benchmark-version evolution and fail clearly on incompatible upstream schema instead of parsing silently wrong data.

### 9.8 Model identity resolution

Internal model identities are stable local keys separate from external source slugs/names. Source adapters produce candidate mappings; one central resolver owns accepted aliases.

Automatic mapping requires sufficient provider/model/effort evidence. Ambiguous aliases require explicit local configuration. Source-specific effort labels are normalized only inside their source adapter/resolver mapping, not by a global hard-coded effort enum.

### 9.9 Static recommendation policy

Adapter recommendation is **capability recommendation**, not scheduling.

Initial role policy:

- Design / architecture / difficult semantic diagnosis: prioritize current Artificial Analysis Intelligence Index evidence among configured eligible models/routes.
- Implementation / repair: prioritize current DeepSWE pass@1 evidence, using exact configuration evidence when available and clearly labeled proxy evidence otherwise.
- Review / Verification: prioritize high general intelligence; when Tracker knows the implementation route, independent model-family/provider diversity may be displayed as an additional robustness signal but is not allowed to override required capability.

Exact weights/tie-breaks are configuration/delegated policy. Recommendations must present the source, metric/version, freshness, match quality, and missing evidence. Missing benchmark data is `UNSCORED`, not zero.

Tracker-derived empirical outcomes may be displayed separately at this level, but Adapter must not learn quota/resource consumption or perform automatic route selection. Those belong to Scheduler.

### 9.10 Adapter CLI additions

Expected commands:

```text
sdp agents
sdp routes
sdp benchmarks status
sdp benchmarks refresh
sdp models
sdp recommend <stage>
sdp run <stage> --route <route-id>
```

If Scheduler is absent, `sdp run` without an explicit/user-pinned route must not silently choose the top recommendation.

## 10. Scheduler Module standard

### 10.1 Responsibilities

Scheduler is the final nested extension. It owns dynamic resource-aware route selection and learning:

- resource ledgers and account meters;
- transparent pricing and opaque quota units;
- reset/window inference and provenance;
- global reservations/uncertainty holds;
- usage telemetry and attribution;
- deterministic task features;
- usage/outcome prediction;
- dynamic future-stage reserves;
- route admission and scoring;
- default `AUTO` route selection;
- quota/provider interruption rescheduling.

Scheduler does not launch agent processes directly. It selects/reserves a `RouteId`, then delegates execution to Adapter.

### 10.2 Scheduler public API v1

Semantic contract:

```python
class SchedulerAPI:
    def resources(self) -> ResourceProjection: ...
    def usage(self, query: UsageQuery) -> UsageHistory: ...
    def predict(self, request: PredictionRequest) -> UsagePrediction: ...
    def schedule(self, request: ScheduleRequest) -> ScheduleDecision: ...
    def reconcile(self, run: RunId) -> ReservationReconciliation: ...
```

`ScheduleDecision` records feasible/rejected routes, reason codes, prediction quantiles, selected route, relevant reservations, and explainable score components.

### 10.3 Scheduler route policy

`AUTO` becomes the default route policy **only when Scheduler capability is installed/enabled**. Without Scheduler, Adapter remains explicit/manual route selection.

Scheduling remains two-stage:

1. hard engineering/operational feasibility;
2. quota/cost/quality ranking inside the feasible set.

Manual web routes may be `UNMETERED_FOR_SCHEDULER` while local routes consume subscription/PAYG ledgers. Unmetered is distinct from unknown. Manual interaction still makes web routes infeasible for unattended execution unless an explicit handoff is allowed.

### 10.4 Scheduler persistence

Scheduler depends on Tracker and adds namespaced tables/migrations to the same user-global SQLite control database through Tracker SPI. This is required for atomic quota reservations shared across projects/accounts.

Scheduler may not modify Tracker-owned workflow tables directly. Resource state remains Scheduler-owned and references project/run/route identifiers through public IDs.

### 10.5 Learning boundary

Cold start uses interpretable benchmark priors + configured conservative resource priors. Initial prediction uses simple empirical quantiles/EWMA/shrinkage without a mandatory ML dependency.

A later statistical/ML dependency may be adopted only after data volume and calibration evidence show material benefit. Black-box end-to-end policy is not workflow authority.

## 11. CLI capability behavior

The CLI is intentionally cumulative.

### Core only

```text
sdp design                  -> print complete Design prompt
sdp implementation          -> print complete Implementation prompt
sdp review                  -> print complete Review prompt
sdp prompt <stage>          -> explicit generic form
sdp capabilities / doctor  -> show Prompt level only
```

### Core + Tracker

Core prompt commands still work identically, but prompts/events are recorded. Additional commands expose manual-cycle state:

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

No quota-aware `AUTO` selection exists.

### + Scheduler

```text
sdp resources
sdp usage
sdp predict <stage> [--route <id>]
sdp schedule <stage> --explain
sdp run <stage>              # AUTO may now select route by default
```

An explicit `--route` always overrides AUTO subject to hard safety/compatibility checks.

The user can inspect installed/disabled/broken capabilities. A failed Scheduler must not make `sdp run --route ...` unavailable if Adapter remains healthy; a failed Adapter must not make Tracker/Core manual mode unavailable.

## 12. Configuration ownership

Core owns the canonical configuration loader/resolution path and project identity. Extensions contribute namespaced validated configuration sections through the SPI.

Conceptual TOML shape:

```toml
[core]

[projects.mdstats]
repo = "/path/to/mdstats"
mode = "hybrid"

[tracker]
retention = "..."

[adapters]
# backend/model/route and benchmark-source configuration

[scheduler]
# ledgers, meter policy, prediction/admission policy
```

Core validates only Core semantics plus extension namespace registration. Each installed extension validates its own section through a versioned Pydantic model. Unknown configuration belonging to an absent extension is preserved/diagnosed rather than interpreted by Core.

Precedence follows one canonical path: built-in defaults -> config -> documented environment allowlist -> CLI/API override. Dynamic automatic selections record value + reason when Tracker exists.

Secrets remain references/environment/approved secret-store inputs and are never serialized into normal resolved configuration/history.

## 13. Persistence and event ownership

Core is stateless across invocations except ordinary configuration/cache artifacts needed for prompt operation.

Tracker introduces persistence. Higher modules extend it through namespaced ownership.

Rules:

- one SQLite file may contain tables from multiple installed extensions, but each table has one owning module;
- only the owning module writes its semantic tables;
- shared transaction needs are exposed through Tracker SPI rather than private SQLite helper imports;
- migration order follows module dependency order;
- uninstalling a higher extension must not make lower tables unreadable;
- removing Scheduler may leave Scheduler-owned historical tables dormant, but Tracker/Core continue functioning;
- raw prompts/outputs and numeric telemetry have separable retention policies;
- persisted data remains private local evidence, not repository authority.

## 14. Extension failure and downgrade rules

Extension discovery/activation is not all-or-nothing.

Examples:

```text
Scheduler incompatible
  -> disable Scheduler
  -> Adapter explicit-run + benchmark recommendation still work

Adapter missing ACP dependency
  -> disable affected direct transports or Adapter execution capability
  -> Tracker manual copy/paste still works

Tracker DB unavailable/corrupt
  -> Tracker reports non-closure/repair path
  -> Core prompt rendering remains available and must not mutate the DB to counterfeit recovery
```

A higher extension may expose partial capabilities only when the remaining subset has a coherent documented contract. Do not advertise `agent.execute.v1` if only benchmark recommendation loaded.

## 15. Security and privacy boundaries

- Plugin discovery loads only installed package entry points, not arbitrary repository/user directories.
- External benchmark responses are untrusted data: enforce byte/time/schema bounds before persistence/use.
- API keys/tokens are never embedded in benchmark caches, prompts, events, logs, or repository files.
- Web prompts contain sanitized remote repository identity and omit local paths/private account/resource state.
- Agent subprocess execution remains direct argv/structured transport with bounded output/time and permission handling.
- External benchmark/cache data may influence recommendations but cannot execute commands or mutate repository state.
- Benchmark/source licensing and attribution requirements travel with cached source metadata.

## 16. Benchmark freshness, provenance, and recommendation integrity

Every recommendation that uses online benchmark data must be reconstructible from a `BenchmarkSnapshot`.

Required displayed/recorded context when material:

```text
source
metric
benchmark/index version
source-generated/fetched time
model + effort + benchmark harness/config
value + uncertainty if available
identity-match quality
staleness
```

Do not compare scores from incompatible benchmark/index versions as though they were one stable scale. Do not merge Artificial Analysis Intelligence Index and DeepSWE pass@1 into a universal scalar unless a later explicitly designed policy defines and validates such a transformation.

The adapter may rank lexicographically by role-relevant evidence without inventing a composite score.

## 17. Architecture fitness rules

Objective dependency rules should be executable once the packages exist:

```text
Core        must not import Tracker/Adapters/Scheduler
Tracker     may import Core only
Adapters    may import Core + Tracker only
Scheduler   may import Core + Tracker + Adapters
```

Cross-module production imports must target public API/SPI paths. A static architecture test should reject reverse/private imports.

Additional durable checks:

- Core minimal-install smoke in an environment where higher distributions are absent;
- Tracker minimal-install smoke without Adapter/Scheduler;
- Adapter minimal-install smoke without Scheduler;
- Scheduler full-stack smoke;
- extension activation failure must degrade to the highest healthy lower level.

## 18. Module acceptance ladder

Each module is independently implemented, reviewed, and accepted before the next workplan begins.

### Prompt Module acceptance

Must prove:

- local install/CLI works with only Core distribution;
- explicit stage command produces a complete prompt with correct automatically resolved project/branch/workplan/protocol inputs;
- ambiguous workplans do not get guessed;
- local/web rendering privacy boundary is correct;
- run id/fingerprint are stable for the rendered artifact;
- no Tracker/Adapter/Scheduler import or persistence requirement exists.

### Tracker Module acceptance

Must prove all Prompt acceptance still passes with and without Tracker installed, plus:

- prompt events persist;
- manual pasted response associates to the correct run;
- development projection handles candidate/workplan changes and PASS/NO-PASS evidence correctly;
- status/history/graph survive restart;
- deleting/disable Tracker leaves Core usable.

### Adapter Module acceptance

Must prove all lower acceptance plus:

- explicit selected-route direct execution through real normalized transport boundary;
- output is tracked automatically;
- benchmark refresh/cache/provenance/identity mapping works;
- Artificial Analysis/DeepSWE source failures degrade without fabricated scores;
- recommendation semantics distinguish Design intelligence from Implementation coding evidence;
- no metering or automatic quota-aware route choice exists;
- disabling Adapter returns to Tracker manual mode.

### Scheduler Module acceptance

Must prove all lower acceptance plus the previously accepted resource/scheduling contract:

- shared account ledgers and dual windows;
- cross-project atomic reservation;
- `UNMETERED_FOR_SCHEDULER` vs `UNKNOWN`;
- usage history/prediction/calibration;
- dynamic review/reasoning reserve;
- PAYG/expiring-subscription decisions;
- automatic route selection only among engineering-sufficient routes;
- interruption/reconciliation/failover without false acceptance;
- disabling Scheduler restores Adapter explicit-route operation.

## 19. Lossless module-workplan derivation standard

The implementation series is fixed in this order:

```text
WP-1  Prompt Module
WP-2  Tracker Module
WP-3  Adapter Module
WP-4  Scheduler Module
```

Each workplan must declare:

```text
parent_architecture: orchestrator/ARCHITECTURE_STANDARD.md
parent_architecture_version: 1.0.0
required_lower_module_api_versions: ...
module_capabilities_delivered: ...
forbidden_higher_module_dependencies: ...
```

A module workplan derives losslessly by carrying:

1. the parent problem/invariants relevant to that module;
2. the module's Frozen responsibilities and non-responsibilities;
3. the exact lower public API contracts it consumes;
4. the public API/SPI surface it must establish for the next module;
5. module-specific affected surface and acceptance boundaries;
6. explicit standalone-install acceptance with higher modules absent;
7. compatibility acceptance with all lower modules present;
8. simplification/reopen triggers.

A workplan must **not** pre-implement later modules merely to make future extension easier. The extension SPI and public IDs defined by this manual are the justified future-facing seams; speculative meter/scheduler tables/classes in Core/Tracker are forbidden.

When a module passes independent Review, its accepted public `api.v1` semantics become the compatibility floor for subsequent module workplans. If later evidence requires a breaking change, reopen the affected parent/API design and use a new API major or an explicit migration/compatibility plan rather than silently changing the lower module.

## 20. Versioning and evolution

Architecture manual versioning:

- major: breaks the module ladder, authority model, dependency direction, or public API role boundaries;
- minor: backward-compatible capability/extension design strengthening;
- patch: clarification with no semantic contract change.

Module package versions are independent but must declare compatible lower API/SPI majors.

External benchmark/source versions do not determine package versions. They are runtime data with source adapters and provenance.

A new benchmark provider should normally be an Adapter-level source plugin. A new agent transport should normally be an Adapter transport/profile. A new resource meter/prediction algorithm belongs in Scheduler. These do not require Core changes unless the stable public/SPI contract is genuinely insufficient.

## 21. Active simplicity and redesign triggers

Simplify/reopen before adding machinery if implementation starts to create:

- multiple extension registries or plugin loaders;
- lower-module imports of higher modules;
- duplicated CLI composition paths;
- both event history and a separate mutable workflow-authority database;
- benchmark-specific fields in Core model objects;
- quota/resource abstractions in Adapter or lower layers;
- duplicated model identity mapping per benchmark provider;
- backend-specific workflow logic instead of transport normalization;
- Scheduler-owned agent execution parallel to Adapter execution;
- public APIs exposing private SQL/backend internals;
- stubs/fallbacks whose only purpose is preserving a higher extension when clean downgrade is possible.

Reopen this parent architecture only when evidence shows a Frozen boundary cannot satisfy the product, such as a required capability needing a reverse dependency, the single extension registry proving insufficient for safe composition, or a public API role being fundamentally unable to support the next module without semantic breakage.

Ordinary provider/API churn, new models, benchmark-version updates, new adapter flags, or predictor algorithm improvement are delegated changes and should not reopen parent architecture.

## 22. Current external benchmark integration evidence

At architecture freeze time:

- Artificial Analysis exposes a documented Data API with a Free language-model endpoint returning headline indices including its Intelligence Index and an `intelligence_index_version`; API use requires a user key and source-specific terms/attribution.
- DeepSWE v1.1 exposes a public JSON leaderboard artifact whose rows are configuration-level observations containing harness, model, reasoning effort, pass rates/confidence, and efficiency metadata.

These facts justify the Adapter benchmark-source abstraction and the contextual `BenchmarkObservation` design. The exact endpoints, score values, rate limits, and future benchmark versions remain external mutable data rather than Frozen architecture.

## 23. Design verdict

**PASS — modular architecture is implementation-ready.**

The next implementation contract should cover **WP-1 Prompt Module only**. It must establish Core, the CLI, the extension composition seam, and prompt API v1 without introducing Tracker persistence, agent adapters, benchmark network integration, or Scheduler/resource machinery.