---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: active
parent_architecture: orchestrator/docs/architecture.md
parent_architecture_version: 1.5.0
base_commit: af4e7ed637891cc49c0ccc40cc9636491df71457
target_branch: plan/protocol-orchestrator
required_lower_module_api_versions: NONE
module_capabilities_delivered:
  - prompt.render
  - project.observe
  - workplan.catalog
  - workflow.profile
forbidden_higher_module_dependencies:
  - sdp-orchestrator-tracker
  - sdp-orchestrator-adapters
  - sdp-orchestrator-scheduler
---

# Protocol Orchestrator WP-1 — Prompt Module + Core Program Workplan

## 1. Objective / problem invariants / non-goals

### 1.1 Original problem

Build the smallest independently useful Protocol Orchestrator product. A user configures a target software repository, runs a command such as:

```text
sdp design --task "..."
sdp implementation
sdp review
sdp prompt verification
```

and receives on stdout one complete, copy/paste-ready, stage-correct Protocol prompt whose mechanically knowable repository, workplan, candidate, and Protocol inputs are already resolved.

This Core-only installation is a finished product mode. It must not require a history database, agent integration, benchmark service, quota meter, or scheduler.

### 1.2 Tier-1 product invariants

1. **Core is independently useful.** Core alone performs project observation, governing-workplan resolution, compatible workflow/profile resolution, and complete prompt rendering end to end.
2. **Target observation is non-mutating.** Core never edits the configured target repository, working tree, index, branch, local refs, or remote repository merely to observe it. Network refresh, when explicitly requested, must use a non-mutating query such as `git ls-remote` or an equivalent read-only remote API rather than `git fetch`/pull.
3. **Canonical prompt authority is singular.** Prompt bodies come from a governing-version-compatible canonical SDP prompt source. Packaged snapshots are derived/version-bound runtime artifacts, never an independently edited prompt authority.
4. **Protocol-version coherence is explicit.** A workplan bound to Protocol version `X` is never silently interpreted with an incompatible newer profile.
5. **Ambiguity stays explicit.** Project/workplan/profile/source ambiguity is reported rather than resolved by mtime, fuzzy similarity, path ordering, or an ungrounded heuristic.
6. **Web/local context is truthful and private.** Web-mode prompt rendering excludes local/private/credential material and does not represent local-only uncommitted state as remotely inspectable. Local mode may include authorized local execution context but never secrets.
7. **The Core API/SPI is a durable lower-module seam.** Tracker, Adapter, and Scheduler must later be able to consume accepted Core v1 services without private imports, duplicated Protocol routing logic, or reverse dependency.
8. **No higher-module preimplementation.** Core does not implement durable history, next-stage projection, agent transport, benchmark recommendation, metering, usage prediction, or automatic routing.
9. **There is one CLI/composition root.** Core owns the `sdp` executable and the single extension entry-point group.
10. **Manual result compatibility exists from day one.** Every rendered prompt carries `RunId`, prompt fingerprint, and a requested `StageResultEnvelope v1`; Core also exposes a bounded prompt-rendered event seam so Tracker can later record prompts without changing the Prompt API.
11. **Public artifacts are deterministic where the semantic state is unchanged.** With a caller-supplied fixed RunId and unchanged material repository/workplan/profile/input state, prompt text/fingerprint do not drift merely because wall-clock observation time changed.
12. **Installed behavior is the acceptance boundary.** Source helpers cannot proxy-pass a broken wheel, console entry point, packaged profile, real repository observer, or final stdout/privacy behavior.

### 1.3 Explicit non-goals

WP-1 does not implement:

- SQLite or durable run/event/workflow history;
- `sdp status`, `sdp next`, `sdp ingest`, `sdp history`, `sdp graph`, or persistent workplan selection;
- Claude/Codex/OMP/Pi/Antigravity/ACP execution, approval handling, or cancellation;
- Artificial Analysis, DeepSWE, model/account catalogs, or benchmark recommendation;
- quota/cost meters, resource ledgers, reservations, prediction, or Scheduler AUTO routing;
- a daemon, resident watcher, generic workflow engine, ORM, or event-sourcing framework;
- repository-local orchestrator state;
- automatic installation/upgrading of protocol sources, plugins, agents, or providers;
- speculative compatibility profiles for unsupplied/untested Protocol versions;
- a second CI authority or generated `dist/skills` representation for the orchestrator package unless repository release policy later requires one.

## 2. Governing authority and baseline

### 2.1 Parent authority

This workplan derives from and is subordinate to:

```text
orchestrator/docs/architecture.md
architecture_version = 1.5.0
protocol_version = 5.16.0
```

The parent module ladder, ownership, dependency direction, API/SPI roles, workflow-profile routing ownership, protocol-version binding, privacy boundary, and WP-1 acceptance obligations are Frozen for this cycle.

### 2.2 Protocol authority

Implementation and Review inherit Protocol 5.16. Initial canonical prompt source:

```text
source/shared/references/development-workflow-prompts.md
```

Workflow and authority semantics remain governed by the supplied Protocol 5.16 source/reference tree, not by a new orchestrator-private doctrine.

### 2.3 Baseline / quality ratchet

At workplan creation, `orchestrator/` contains architecture documentation but no executable Core package. There is no legacy Core machinery to preserve.

The greenfield quality ratchet is:

- no second prompt authority;
- no later-module machinery below its owning future module;
- minimal justified runtime/public surface;
- executable guards for objective namespace/import/entry-point rules;
- rejection-capable tests for ambiguity, version compatibility, remote truthfulness, privacy, and identity;
- one canonical config normalization path for API and CLI;
- no test-only reimplementation of the production observer, resolver, renderer, or extension registry.

## 3. Frozen high-level architecture and engineering envelope

### 3.1 Distribution and namespace

Create one independently installable Python distribution:

```text
sdp-orchestrator-core
```

under native PEP 420 namespace `sdp_orchestrator.core`. The namespace root must not contain `sdp_orchestrator/__init__.py`.

Initial supported runtime floor: **Python 3.11+**. Keep implementation OS-neutral where practical and claim only platform behavior actually tested.

### 3.2 Core ownership

Core owns:

- `sdp` CLI/application composition;
- Core configuration and project catalog;
- public Core identifiers/request/response/value records;
- read-only Git/project/workplan observation;
- candidate and physical worktree identity;
- compatible Protocol profile/workflow descriptor resolution;
- canonical prompt-source resolution and packaged compatible snapshot;
- prompt input resolution/rendering;
- RunId/fingerprint/result-envelope request identity;
- one extension registry/service composition root;
- one in-process event-sink registration/publish seam;
- Core-only `projects`, `capabilities`, and `doctor` diagnostics;
- optional clipboard output.

Core owns none of the §1.3 responsibilities.

### 3.3 CLI/composition root

Console entry point:

```text
sdp
```

Extension discovery group:

```text
sdp_orchestrator.extensions.v1
```

No arbitrary plugin-directory scanning, repository plugin loading, or higher-module import special cases.

### 3.4 Configuration and project resolution

Use one TOML normalization/validation path. Default config location comes from `platformdirs`; CLI/API can explicitly override it. The environment override allowlist is empty in v1 unless implementation evidence establishes a genuine Core need; arbitrary environment variables never alter semantic behavior.

V1 project semantics:

```toml
schema_version = 1

[core]
default_project = "mdstats"       # optional
default_execution_mode = "web"    # optional; local | web

[projects.mdstats]
repo = "/absolute/path/to/mdstats"
protocol_profile = "sdp-protocol-5.16"
default_execution_mode = "web"    # optional per-project override
```

V1 optional Protocol-source override semantics:

```toml
[protocol_sources."sdp-protocol-5.16"]
local_root = "/path/to/software-development-protocol"   # optional
allow_remote = false                                    # default
remote_repository = "https://github.com/hjin98/software-development-protocol"  # optional override only when explicitly supported
remote_ref = "<exact evidence-backed ref>"              # required for remote fallback; never inferred from semantic version
```

Secrets/tokens are not accepted as ordinary persisted Core config values. Authentication for an explicitly permitted remote operation may use the user's established Git/platform credential mechanism without serializing credentials into config snapshots, diagnostics, prompts, or cache identity.

CLI project resolution when `--project` is absent:

```text
unique configured project whose canonical worktree contains cwd
  -> core.default_project
  -> sole configured project
  -> AMBIGUOUS / NOT_FOUND
```

An explicit `--project` overrides that chain. Public Core API requests use explicit `ProjectKey`; CLI convenience resolution does not become hidden API behavior.

### 3.5 Read-only repository/candidate/worktree observation

`ObservationPolicy` supports:

```text
local_only
use_cached_remote
refresh_remote
```

Default is `local_only`. `use_cached_remote` may inspect local remote-tracking/upstream refs without updating them. `refresh_remote` may query the remote explicitly but must not mutate the target repository; use `git ls-remote` or an equivalent read-only API, not `git fetch`/pull. Results carry observation time, source, freshness/confidence, and whether remote visibility is known.

`CandidateRef` captures branch/detached HEAD, commit, relevant staged/unstaged/untracked state, upstream/observed remote when known, and identity completeness. `sdp.git-working-tree.v1` may use any bounded deterministic Git-native realization, but materially different dirty content at the same paths must change the digest. If relevant state cannot be fingerprinted within safe resource bounds, set `identity_complete=false` rather than claiming exact identity.

`WorktreeKey` identifies the physical Git worktree: aliases/symlinks to the same worktree resolve to the same key; distinct Git worktrees resolve to distinct keys.

Observation of the target repository treats repository content as data. Core must not execute repository files merely to discover Git/workplan state.

### 3.6 Workplan discovery, selection, path safety, and identity

Catalog repository conventions under `workplans/active/` and `workplans/archive/`, including nested current `AUTHORITY.md` files and frontmatter-marked implementation workplans. Discovery is bounded to regular text files whose resolved paths remain within the configured repository root; do not follow symlink/path traversal outside the repository. Bound individual file size/frontmatter parsing sufficiently to avoid accidental unbounded reads.

Deduplicate documents sharing the same `workplan_id`; do not treat historical numbered revisions as independent active authorities when a current authority file clearly owns the workplan. Where current repository conventions cannot determine ownership without guessing, return ambiguity instead of encoding a heuristic exception stack.

An explicit selector has exact semantics only:

```text
exact workplan_id
or exact repository-relative canonical workplan path
```

If either maps to more than one material authority, selection is ambiguous.

For a stage requiring a governing workplan:

```text
explicit selector
  -> unique exact branch binding declared by recognized workplan metadata (initial recognized key: target_branch)
  -> exactly one active workplan
  -> AMBIGUOUS / REQUIRED
```

No fuzzy filename matching or recency guessing.

Design of a new task may proceed without an existing workplan only when `first_task`/`--task` is supplied.

`WorkplanRef` carries exact artifact digest plus deterministic semantic digest. `sdp.workplan-semantic.v1` may exclude only documented lifecycle-only metadata so archive/status bookkeeping can preserve semantic identity. A body/Frozen-authority change must alter semantic identity. Unknown/unrecognized semantics are conservative; if safe canonicalization is unavailable, mark semantic identity incomplete.

### 3.7 Protocol profile and canonical prompt source

Initial release supports a Protocol 5.16-compatible profile only unless additional compatibility is explicitly supplied and accepted later.

Resolution order:

```text
explicit configured compatible local source/profile
  -> exact compatible packaged profile/prompt snapshot
  -> explicitly permitted canonical read-only remote source at exact evidence-backed ref
  -> truthful INCOMPATIBLE / UNAVAILABLE
```

Never guess a semantic version string as a Git ref.

The packaged profile/snapshot is derived runtime material. Canonical stage prompt bodies are extracted reproducibly from `development-workflow-prompts.md`, not independently rewritten. For v1, the selected stage prompt body is the literal contents of the fenced `text` block belonging to the uniquely identified canonical stage heading. If the canonical source structure no longer supports unambiguous stage extraction, generation fails rather than heuristically choosing another block.

A small machine-readable profile metadata source is allowed for stage keys/aliases, transition trigger classes, compatibility, first-class input bindings, and source identity. It must not duplicate prompt prose and must be validated against the supplied Protocol references.

The installed wheel must render its compatible packaged profile offline when target-repository evidence is local and sufficient. Source-to-packaged parity must compare against the actual canonical source, not against another generated/private constant.

### 3.8 Prompt execution modes, remote truthfulness, and privacy

Core v1 execution modes:

```text
local
web
```

Web mode is both a privacy and repository-visibility boundary:

- no local absolute repository/config/private-state path;
- no credential/token or credential-bearing Git URL userinfo;
- no local file:// or filesystem remote identity in the prompt;
- no future account/quota/resource telemetry;
- repository target uses sanitized remote identity plus branch/commit/workplan path when available;
- material uncommitted local state is not representable as a remotely inspectable candidate and therefore blocks a web render with a structured problem;
- if Core has evidence that the committed local candidate differs from the observed remote candidate, web rendering fails as stale/unavailable rather than pretending they are the same;
- when remote visibility is not freshly established, the prompt/footer reports that visibility as cached/unknown according to actual provenance rather than asserting freshness.

Local mode may include authorized local repository/worktree paths but still never secrets.

### 3.9 Prompt input ownership and override semantics

The renderer fills all mechanically supported stage inputs. Values requiring semantic agent investigation remain the canonical explicit `AUTO`/`NONE`; Core does not guess them.

Profile metadata defines the mapping from canonical stage INPUT names to first-class PromptRequest fields/mechanically owned values. `input_overrides` may set only names declared by the selected canonical stage INPUT block and not owned by a first-class request field. Unknown names fail with `core.prompt.input_unknown`; attempting to use generic input override to contradict a first-class/mechanically owned field fails with `core.prompt.input_conflict` and points to the dedicated API/CLI option.

Examples of first-class ownership include project/repository target, selected workplan where the stage has one, protocol source/profile/ref, execution mode, and Design `TASK` through `first_task`/`--task`. Stage-specific semantic inputs such as additional constraints or authority hints may remain explicit overrides when declared by the canonical stage.

A successful render contains no unresolved square-bracket user-edit placeholder that Core was responsible for resolving.

### 3.10 Canonical body plus orchestrator footer

The canonical stage prompt body is preserved except for substitution of declared INPUT values under the binding rules above. Core may append only the architecture-approved orchestration metadata/result-request footer containing RunId, prompt fingerprint, bounded prompt-source/candidate/remote-visibility provenance, and `StageResultEnvelope v1` instructions.

The footer is not an alternate stage prompt and may not weaken, replace, or reinterpret the canonical stage body. Canonical-source parity tests compare the body separately from the appended footer.

Volatile observation timestamps and diagnostics are returned as structured provenance but are not injected into prompt text unless a canonical input materially requires them. With fixed RunId and identical semantic inputs/candidate/source, repeated renders must be byte-stable.

### 3.11 Prompt stdout contract

Prompt commands write exactly the complete prompt to stdout. Diagnostics/errors go to stderr with deterministic nonzero exits. Therefore:

```text
sdp review > prompt.txt
```

produces a clean prompt artifact. Optional clipboard support is additive and may never make ordinary stdout rendering depend on clipboard availability.

## 4. Public Core API/SPI v1 contract

### 4.1 Public-record rule

Every request, response, identifier, descriptor, receipt, query, and nested record reachable from a public `api.v1`/`spi.v1` signature must itself be public under that versioned surface or be a standard immutable scalar/container type. Public methods must not expose private Pydantic models, subprocess/session objects, Git-library objects, file handles, locks, or implementation repositories.

Public records are JSON-compatible immutable-by-convention values. Pydantic is the initial realization, not semantic authority. Opaque IDs serialize as strings; timestamps as timezone-aware UTC ISO-8601; `DigestRef` carries algorithm + canonicalization scheme + value. Potentially unbounded collections use `Page[T]` with opaque query-scoped cursors.

Core must expose at least the parent-required identities/descriptors plus all request/response records used below, including:

```text
ProjectKey
WorktreeKey
RunId
EventId
StageRef
CapabilityKey
ExtensionId
DigestRef
ProtocolProfileRef
PromptSourceRef
WorkplanRef
CandidateRef
ProjectDescriptor
PromptProjectSnapshot
EventEnvelope
WorkflowProfileDescriptor
StageDescriptor
StageTransitionDescriptor
BlockerRecord
StageResultEnvelope
Problem
Page[T]
ProjectQuery
ProjectObservationRequest
ProjectObservation
WorkplanQuery
WorkplanDescriptor
PromptRequest
RenderedPrompt
CapabilityRequirement
CapabilityProvision
CapabilityStatus
ExtensionManifest
ExtensionRegistration
```

Exact field spelling/serialization may be finalized during implementation only within the semantics in this plan and parent architecture. Before WP-1 Review passes, the accepted `api.v1`/`spi.v1` wire/schema fixtures become the compatibility floor for WP-2+.

### 4.2 CoreAPI v1

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

All methods are read-only with respect to target repositories. `allocate_run_id` creates identity only, no persistent record. `list_stages()` is a bounded convenience view of `workflow().stages`, not a second source of stage semantics.

### 4.3 Application/composition API v1

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, requirement: CapabilityRequirement) -> bool: ...
    def service(self, requirement: CapabilityRequirement) -> object: ...
    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

Core provisions at least:

```text
prompt.render
project.observe
workplan.catalog
workflow.profile
```

Capability keys are semantic/unversioned; API compatibility is separate. Singular services may not be silently replaced. Multi-provider ordering, when a future capability permits it, is stable by provider ID.

### 4.4 Extension SPI v1 and event sink

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Manifest inspection is side-effect-minimal: no subprocess, network, repository mutation, or storage migration. Activation is dependency-topological. Failed/incompatible optional providers disable themselves/dependents without breaking healthy Core.

`ExtensionContext` exposes only explicit versioned composition services: effective namespaced config, already-active required services, CLI/config/event/diagnostic registrars. No Core private implementation object crosses the SPI.

The event registrar supports a minimal sink contract finalized under `core.spi.v1` with semantics equivalent to:

```python
class EventSink(Protocol):
    def handle(self, event: EventEnvelope) -> None: ...
```

Core emits at least `core.prompt.rendered.v1` after a successful render. Its payload is sufficient for an authorized later Tracker sink to reconstruct the rendered prompt record, including RunId, fingerprint, stage/project/workplan/source/context identity and the complete rendered prompt. The event identity is stable for the same RunId + prompt fingerprint + event type so an invocation retry may redeliver without creating a distinct logical event. Core has no durable queue in WP-1; a sink failure is diagnosed and may be retried in-process where practical, but it cannot counterfeit/fail an otherwise successful primary prompt result. Sinks must tolerate duplicate delivery by EventId.

### 4.5 WorkflowProfileDescriptor v1

Profile exposes the bounded machine-readable Protocol routing contract required by Tracker later:

```text
WorkflowProfileDescriptor
  profile
  schema_version
  stages
  transitions

StageDescriptor
  stage
  role_owner
  mutation_class
  optionality
  recognized_outcomes

StageTransitionDescriptor
  from_stage
  trigger_key
  to_stage | terminal
  priority_hint | None
  explanation
```

`trigger_key` is a profile-defined opaque routing class, not executable expression text. The 5.16 profile documents how normalized StageResultEnvelope facts map to trigger classes. Core exposes this contract but does not infer current next action in WP-1.

### 4.6 PromptRequest / RenderedPrompt

`PromptRequest v1` represents:

```text
run_id | None
project: ProjectKey
stage: StageRef
execution_mode: local | web
workplan_selector | None
first_task | None
input_overrides
observation_policy | None
```

`RenderedPrompt v1` returns:

```text
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

### 4.7 Run/fingerprint/result-envelope contract

Under `sdp.prompt-fingerprint.v1`:

1. allocate/use RunId;
2. render the exact full artifact using a fixed fingerprint placeholder;
3. SHA-256 hash exact UTF-8 placeholder-form bytes under a frozen line-ending/terminal-newline normalization;
4. substitute `sha256:<hex>`.

WP-1 freezes the literal placeholder and byte normalization with executable fixtures.

Every prompt requests:

```text
StageResultEnvelope v1
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
  classification | None
  summary
  authority_class | None
```

The footer must not request hidden chain-of-thought. Core neither persists nor semantically interprets returned results in WP-1.

### 4.8 Error contract

Python APIs raise one `OrchestratorError` carrying:

```text
Problem(code, message, retryable, details)
```

Consumers branch on code, not message text. Establish/test at least:

```text
core.config.invalid
core.project.not_found
core.project.ambiguous
core.repository.invalid
core.workplan.required
core.workplan.not_found
core.workplan.ambiguous
core.protocol.incompatible
core.protocol.unavailable
core.stage.unknown
core.remote.unavailable
core.remote.stale
core.prompt.input_unknown
core.prompt.input_conflict
core.extension.incompatible
core.extension.activation_failed
core.clipboard.unavailable
```

Do not create a broad exception subclass hierarchy.

### 4.9 CLI request mapping

The CLI exposes every Core-only input needed to form a complete PromptRequest without interactive stdout contamination:

```text
--project <ProjectKey>
--workplan <exact workplan_id-or-relative-path>
--execution-mode local|web
--config <path>
--remote-mode local_only|use_cached_remote|refresh_remote
--task <text>                         # first_task; required for workplan-free Design
--input NAME=VALUE                    # repeatable; only non-first-class declared stage inputs
--copy                                # optional clipboard extra
```

A missing required first task fails clearly instead of prompting on stdout. Unknown/conflicting `--input` values fail before render. CLI and API route through the same normalization/validation layer.

## 5. Implementation obligations

### O1 — Core distribution/package boundary

Create `sdp-orchestrator-core`, PEP 420 namespace, `sdp` entry point, packaged 5.16 profile/prompt resources, and only justified Core dependencies.

Expected runtime dependencies unless a simpler equivalent is demonstrated:

```text
platformdirs
typer
pydantic
python-frontmatter
packaging
```

Clipboard support optional (`pyperclip` extra/equivalent). No `filelock`, ACP, `httpx`, ORM/event-sourcing, ML, Tracker, Adapter, or Scheduler runtime dependency.

**Acceptance:** build supported wheel/sdist; independently inspect metadata/resources/entry point; install wheel outside source checkout; execute installed `sdp --help`, `sdp projects`, and representative prompt commands; prove no root namespace `__init__.py` and no forbidden higher-module imports.

### O2 — Canonical config/project/source resolution

Implement §3.4 through one API/CLI normalization path with provenance and redaction. Explicit source override/remote fallback are opt-in and exact-ref-bound; default packaged/offline operation requires no network.

**Acceptance:** explicit project, cwd match, configured default, sole project, ambiguity, invalid repo, CLI/API precedence, mode override, local protocol-source override, remote disabled by default, exact remote-ref validation, malformed TOML/frontmatter, and secret-redaction cases.

### O3 — Real non-mutating Git/worktree/remote observation

Implement production observation against actual Git repositories.

**Acceptance boundary:** actual temporary Git repositories/worktrees, not precomputed CandidateRefs.

**Acceptance:** branch/detached HEAD; upstream known/unknown; staged/unstaged/untracked state; two different dirty contents at the same paths produce different working-tree identities; symlink alias same WorktreeKey; separate Git worktree different WorktreeKey; credential-bearing remote sanitization; local/file remotes do not leak into web context; identity-incomplete bounded case; cached-remote provenance; `refresh_remote` through non-mutating remote query; target worktree/index/HEAD/local refs/remote-tracking refs remain unchanged after observation.

### O4 — Workplan catalog/resolution/path safety/semantic identity

Support current active/archive conventions, nested `AUTHORITY.md`, frontmatter IDs, exact selectors, deterministic branch binding, conservative identity, and repository-bound path handling.

**Acceptance:** top-level plan; nested authority; lifecycle-only archive/status change; body/Frozen semantic change; multiple-active ambiguity; exact ID/path selector; not-found selector; exact `target_branch` match; Design without plan + task; required-plan failure for Implementation/Review; symlink/path escape rejected/ignored safely; oversized/malformed workplan handled without arbitrary read/execute.

**Counterfactual:** two plausible active plans fail rather than select by mtime/path ordering.

### O5 — Version-bound Protocol 5.16 profile/snapshot

Produce reproducible packaged prompt/profile resources from canonical supplied Protocol authority.

**Acceptance:** uniquely extract every canonical stage fenced body; source-to-packaged body parity for all stages; workflow keys/aliases/transitions/input-binding metadata reconciled with supplied 5.16 references; package source/profile identity recorded; offline installed-wheel rendering; unknown/older workplan not silently rendered as 5.16; explicit local source success; remote fallback disabled by default and exact-ref-bound when enabled; incompatible explicit source fails truthfully.

**Anti-shortcut:** comparing two products of the same stale private constant does not prove canonical-source parity.

### O6 — Core API/Application API/extension/event SPI v1

Implement public import paths, JSON-compatible public request/response records, composition/service registry, capability/API-major matching, extension activation/degradation, and the prompt-rendered event seam.

**Acceptance:** public API round-trip/schema fixtures; no public signature references private classes; capability/version separation including `workflow.profile`; compatible/incompatible providers through production composition root; duplicate singular service rejected; manifest inspection has no activation side effects; failed optional provider does not break Core prompt rendering; `core.prompt.rendered.v1` event emitted with stable logical EventId; duplicate delivery tolerated; sink failure does not change primary render result.

**Real integration boundary:** exercise discovery through actual Python entry-point metadata in an isolated installed test extension/fixture distribution or equivalent real `importlib.metadata` installation boundary; an in-memory fake provider list alone is insufficient to prove plugin discovery.

### O7 — Canonical prompt renderer and input contract

Resolve stage via compatible profile; fill mechanically known first-class inputs; preserve canonical `AUTO`/`NONE` for semantic discovery; enforce override ownership; preserve canonical stage body except declared INPUT substitution; append only approved orchestrator footer.

**Acceptance:** all canonical stage bodies, with focused fixtures for Design/Implementation/Review/Verification/optional stages; exact body extraction; workplan-free Design with `--task`; unknown/conflicting override rejection; API/CLI override parity; no cross-stage body; no unresolved Core-owned placeholder; fixed RunId + unchanged semantic state remains byte-stable across time.

### O8 — Local/web privacy and remote-access truthfulness

Use fixtures containing distinctive home/config/private paths, credential-bearing HTTPS remote, SSH-style remote, local/file remote, dirty local state, cached-remote divergence, and unrelated secret-like values.

**Acceptance boundary:** final production `RenderedPrompt.prompt_text` and installed CLI stdout.

Web output contains none of the prohibited local/credential values while retaining sufficient remote/branch/workplan identity when safely available. Material dirty local state blocks web mode. Known committed local/remote divergence blocks web mode. Unknown/cached remote visibility is labeled with actual provenance, not asserted fresh. Local output may include authorized repo path but never secrets.

### O9 — RunId/fingerprint/StageResultEnvelope v1

Preserve caller RunId, allocate opaque IDs otherwise, implement frozen placeholder/UTF-8 normalization hash, and append matching structured result request without chain-of-thought demand.

**Acceptance:** fixed RunId + identical semantic observation/source/input gives identical prompt/fingerprint across wall-clock time; stage/workplan/candidate/mode/input change alters fingerprint when prompt artifact changes; placeholder algorithm fixture; final prompt has digest and no placeholder; result schema/BlockerRecord present and matches requested schema identity.

### O10 — Core CLI/diagnostics

Required canonical commands:

```text
sdp prompt <stage>
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

Canonical option mapping is §4.9. Prompt stdout is prompt-only; diagnostics use stderr; ambiguity/incompatibility has deterministic nonzero exit. Optional `--copy` never removes stdout usability.

`sdp doctor` is non-mutating and reports only Core-relevant readiness: config validity, selected/known projects and repository reachability, packaged/profile identity/compatibility, extension activation status, optional clipboard availability, and explicitly requested remote-probe status. It performs no hidden network operation by default and does not report higher-module health when those modules are absent.

**Acceptance boundary:** installed `sdp` subprocess execution; direct Typer callback tests alone are insufficient.

### O11 — Core-only user documentation

Document installation, config/schema/source policy, project selection, `--task`, `--input`, stage commands, local/web behavior and remote-visibility requirements, ambiguity handling, protocol binding, piping/copying, event/plugin trust, and explicit absence of Tracker/Adapter/Scheduler features. Do not present future commands as current.

### O12 — Repository CI/release integration

Integrate Core acceptance into the repository's ordinary validation path without creating a competing workflow authority. Prefer extending the existing `.github/workflows/protocol-check.yml`/repository validation invocation so Core tests plus package/install smoke run in normal CI. Do not place the orchestrator wheel into generated `dist/skills` unless a separate release policy explicitly requires that representation.

**Acceptance:** ordinary CI/repository validation fails when Core unit/integration/package acceptance is broken and remains compatible with existing Protocol skill build/validation/parity checks.

### O13 — Final assembled conformance/simplicity closure

Reconcile every obligation against assembled Core. Remove duplicate prompt/profile representations, speculative persistence/transport/resource hooks, unused compatibility shims, and helpers serving only hypothetical later modules rather than accepted API/SPI seams.

Re-derive final affected surface and run complete Core affected regression, installed-package integration, and the repository-required Protocol validation on the final assembled candidate.

## 6. Implementation authority

### Frozen

- parent architecture 1.5.0 module/dependency/ownership boundaries;
- Core independent usefulness;
- `sdp-orchestrator-core`, `sdp`, PEP 420 namespace, one extension group;
- public Core API/SPI semantic method families and event seam in §4;
- Python 3.11+ initial compatibility floor;
- non-mutating target/remote observation semantics;
- deterministic project/workplan selection rules and exact selector semantics;
- version-bound Protocol profile resolution;
- canonical prompt body + derived packaged snapshot relationship and deterministic fenced-stage extraction;
- local/web privacy and remote-access truthfulness;
- first-class input ownership/override-conflict semantics;
- RunId/fingerprint v1/StageResultEnvelope v1 request seam;
- Core capability set including `workflow.profile`;
- no Tracker/Adapter/Scheduler responsibilities in Core.

### Delegated

- private class/function/module decomposition;
- PEP 517 backend/test-runner details;
- Git plumbing implementation satisfying the Frozen non-mutating identity semantics;
- bounded workplan/prompt parser implementation;
- bounded protocol-source cache layout;
- non-prompt diagnostic formatting;
- internal Pydantic decomposition/validators preserving accepted public wire semantics;
- optional clipboard implementation;
- standard-library versus focused dependency choice when contract-equivalent and simpler;
- exact public field spelling only until WP-1 Review accepts the `api.v1`/`spi.v1` schema, after which it is compatibility authority.

Do not add abstractions merely for hypothetical later use; later modules consume accepted v1 APIs/SPIs.

### Reopen only on evidence

Reopen only the affected Design surface if evidence shows:

- required workflow/profile information cannot be exposed without materially different ownership;
- canonical prompt cannot be packaged offline without creating a second authority under the current model;
- Core API/SPI cannot support Tracker/Adapter direction without private/reverse dependency;
- one extension registry/event seam cannot compose required modules safely;
- material target-workplan conventions cannot fit the Frozen identity/resolution model without systematic false ambiguity;
- Python 3.11+ violates an independently required compatibility target;
- local/web privacy or remote truthfulness cannot be preserved under the current prompt-context ownership.

Ordinary parser, packaging backend, Git command, internal model field, or diagnostic-format choices remain Implementation discretion.

## 7. Affected surface and task-specific acceptance

### 7.1 Expected affected surface

```text
orchestrator/core/                         # new Core distribution/source/tests/package data
orchestrator/docs/                         # Core user/operator docs; parent architecture preserved
workplans/active/PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE.md
.github/workflows/protocol-check.yml       # minimally extend ordinary validation if needed
repository test/build configuration        # only as needed for Core package acceptance
source/shared/references/development-workflow-prompts.md   # canonical input; do not modify absent proven authority defect
source/shared/references/workflow-and-workplans.md         # routing authority input
```

Re-derive final surface from assembled implementation; this is not a ceiling.

### 7.2 Real semantic-owner boundaries

1. **Prompt product:** installed `sdp` -> production Core composition -> production observer/resolver/renderer -> stdout. A direct helper returning expected text cannot close a broken installed CLI.
2. **Repository observation:** production observer against actual temporary Git repositories/worktrees and non-mutating remote query boundary.
3. **Canonical source:** source/package preparation reads the actual canonical Protocol prompt source; stale private-copy self-comparison cannot close parity.
4. **Packaging:** built wheel installed outside source tree, including packaged profile/resources and console entry point.
5. **Privacy/remote truthfulness:** final `RenderedPrompt.prompt_text` and installed CLI stdout.
6. **Extension composition:** production `importlib.metadata`/entry-point discovery plus service registry with a real installed fixture provider; an injected in-memory provider list alone is not enough.
7. **Event seam:** production render path -> registered event sink; test cannot bypass render and manually call the sink.
8. **Repository CI:** ordinary repository validation path actually invokes the Core acceptance surface.

### 7.3 Required evidence

At minimum:

- focused API/config/Git/workplan/profile/renderer/fingerprint/SPI/event tests;
- stage-local affected regression after each material executable stage;
- final Core affected regression;
- actual temporary Git repo/worktree/remote fixtures for observer claims;
- built artifact inspection + isolated installed-wheel CLI integration;
- actual entry-point discovery integration with an installed fixture extension;
- objective import-direction/namespace-package guards;
- offline packaged-profile prompt integration;
- web privacy/credential-redaction/dirty-local/remote-divergence integration;
- ambiguity/incompatibility/override-conflict counterfactuals;
- project-configured fast Python static checks when available/justified; do not add a second checker for symmetry;
- repository-required Protocol validation on the final candidate exactly as documented by the governing repository, currently:

```text
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

Core-specific package/test commands are additional to, not substitutes for, those repository checks. If final impact cannot be bounded confidently, run the broader available suite.

Production qualification: **unnecessary** for WP-1; no production-scale performance/resource claim is made.

## 8. Implementation sequence

### Stage 1 — Package/contracts/config/repository observation

Create distribution/namespace/entry point, public API/SPI records/services, canonical config/project/source resolution, Git/Candidate/Worktree observation, and workplan catalog/identity/resolution.

**Closure:** focused public-contract/config/Git/workplan/path-safety tests + affected Core regression; dirty-content identity; non-mutating remote refresh; no higher-module imports/persistence.

### Stage 2 — Protocol profile/snapshot + prompt renderer

Implement version-bound source/profile resolution, deterministic canonical fenced-stage extraction/packaged snapshot, WorkflowProfileDescriptor, input binding/override validation, local/web context and remote truthfulness, RunId/fingerprint/result footer, event publication, stage aliases, `--task`/`--input`, and prompt-only stdout.

**Closure:** canonical source parity; incompatible-version rejection; local/web privacy and remote-visibility cases; fingerprint byte-stability; structured event/result fixtures; Design task and all-stage prompt extraction; offline packaged-profile test + affected regression.

### Stage 3 — Composition/CLI/package/CI integration and final closure

Complete real entry-point discovery/service composition, diagnostics/projects/doctor commands, optional clipboard, docs, build/install integration, ordinary repository-CI integration, architecture-fitness checks, final accepted-contract reconciliation, final affected regression, repository-required checks, and simplification cleanup.

**Closure:** isolated installed-wheel end-to-end acceptance on representative temporary target repositories plus ordinary repository validation on the final candidate; implementation handoff ready for independent Review.

## 9. Simplification triggers

Simplify/re-derive before adding machinery if implementation starts producing:

- a second manually maintained prompt-body set;
- duplicated local/web renderers instead of one context/privacy policy;
- separate CLI/API config semantics;
- multiple plugin registries/loaders;
- a generic workflow engine instead of bounded 5.16 descriptors;
- persistent event queue/run database machinery in Core;
- transport/model/account/resource placeholder objects in Core;
- fuzzy workplan heuristic exception stacks;
- wrappers/fallbacks compensating for an overcomplicated profile extractor;
- custom semver/TOML/YAML/CLI/package machinery where focused maintained libraries already own the problem;
- public objects leaking Git subprocess/Pydantic/private implementation state;
- remote observation implemented by mutating the target repository;
- generic input override logic capable of contradicting first-class prompt identity/context;
- a separate orchestrator CI workflow duplicating the ordinary repository validation path without a real isolation requirement.

## 10. Independent workplan review closure — 2026-09-07

This workplan was re-reviewed against `orchestrator/docs/architecture.md`, the remote Protocol 5.16 `software-design` role, and the supplied workflow/workplan, testing, architecture, versioning, Python, configuration, security, specification, release, repository instructions, and canonical prompt source.

The review found and closed the following material pre-implementation gaps:

1. added the parent-required `workflow.profile` capability to the delivered Core capability set;
2. made target/remote observation genuinely non-mutating by defining `refresh_remote` as a read-only remote query rather than an implicit fetch;
3. strengthened working-tree identity so content changes, not merely dirty path/status, change candidate identity;
4. bounded workplan discovery to repository-owned regular files and defined exact selector/path-safety behavior;
5. defined canonical stage extraction from the canonical fenced prompt block, preventing heuristic/stale stage-body selection;
6. made Protocol-source override/remote fallback explicit, opt-in, and exact-ref-bound while preserving offline packaged operation;
7. defined first-class prompt-input ownership and rejection of unknown/conflicting generic overrides;
8. added a real Core event-sink/prompt-rendered seam required for later Tracker integration without persistence in Core;
9. strengthened plugin acceptance to exercise actual installed Python entry-point discovery rather than only injected providers;
10. made web mode truthful about local-only dirty state and known local/remote divergence;
11. removed volatile observation time from default prompt bytes so fixed-RunId identical semantic state is reproducible;
12. bound completion to the repository's actual required Protocol validation commands and ordinary CI path, in addition to Core package/install acceptance.

Snapshot-loss counterfactual: with prior chat and Git history removed, `orchestrator/docs/architecture.md`, this workplan, and the supplied Protocol 5.16 source/reference tree recover all still-binding WP-1 product/Frozen semantics, public API/SPI roles, non-goals, acceptance boundaries, and Design-reopen triggers.

No Tracker, Adapter, benchmark, metering, prediction, or Scheduler implementation is required for WP-1. The only future-facing machinery justified now is the parent-required public API/SPI, stable identities, workflow profile, extension registry, and non-durable event seam.

**Design verdict: PASS — WP-1 Prompt Module + Core Program is snapshot-complete, internally coherent, and ready for `software-implementation`.**
