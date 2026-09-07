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
forbidden_higher_module_dependencies:
  - sdp-orchestrator-tracker
  - sdp-orchestrator-adapters
  - sdp-orchestrator-scheduler
---

# Protocol Orchestrator WP-1 — Prompt Module + Core Program Workplan

## 1. Objective / problem invariants / non-goals

### 1.1 Original problem

The first useful Protocol Orchestrator release must remove repeated manual prompt lookup/editing without requiring any history database, agent integration, benchmark service, quota meter, or scheduler.

A user who has configured a target software repository must be able to run a command such as:

```text
sdp design
sdp implementation
sdp review
sdp prompt verification
```

and receive on stdout one **complete, copy/paste-ready, stage-correct Protocol prompt** whose ordinary repository/workplan/protocol inputs have already been resolved from the configured project and its current Git/workplan state.

This smallest installation is a complete product mode, not a stub for later modules. Higher modules may later consume its public API/SPI, but Core must remain independently installable, testable, releasable, and useful when every higher distribution is absent.

### 1.2 Tier-1 product invariants

1. **Immediate usefulness:** Core-only installation performs the complete Prompt Module job by itself.
2. **Read-only target behavior:** prompt/status observation performed by Core never edits, pulls, merges, rebases, commits, pushes, checks out, or otherwise mutates the configured target repository.
3. **Canonical prompt authority:** prompt bodies come from a governing-version-compatible Software Development Protocol prompt source; no manually copied second set of stage prompt bodies becomes independent authority.
4. **Protocol-version coherence:** a workplan bound to Protocol version `X` is never silently rendered through an incompatible newer profile merely because the installed orchestrator is newer.
5. **Deterministic ambiguity handling:** Core resolves what repository/workplan/profile evidence actually supports and reports `AMBIGUOUS`, `INCOMPATIBLE`, or `UNAVAILABLE` rather than guessing.
6. **Web/local privacy separation:** web-mode prompt rendering never leaks local absolute paths, private orchestrator paths, credentials, or credential-bearing remotes; local-mode rendering may include local execution context when authorized.
7. **Stable future seam:** the public Core API/SPI established here is sufficient for Tracker, Adapter, and Scheduler to consume later without private imports or reverse dependency.
8. **No higher-module preimplementation:** WP-1 contains no durable development-history store, next-stage projection, agent subprocess/ACP machinery, benchmark networking, account/model recommendation, quota/resource ledger, usage prediction, or automatic route selection.
9. **One CLI/composition root:** the `sdp` executable and extension composition root are owned by Core from the first release.
10. **Manual result compatibility seam:** rendered prompts carry a stable `RunId`, fingerprint, and requested `StageResultEnvelope v1` so later Tracker ingestion does not require changing Prompt API semantics.

### 1.3 Explicit non-goals

WP-1 does **not** implement:

- SQLite or any durable workflow/event/run history;
- `sdp status`, `sdp next`, `sdp ingest`, `sdp history`, `sdp graph`, or persistent workplan selection;
- direct execution of Claude, Codex, OMP, Pi, Antigravity, ACP, subprocess agent sessions, approval handling, or cancellation;
- Artificial Analysis, DeepSWE, benchmark fetching/recommendation, model/account catalogs, or route ranking;
- quota/cost meters, resource ledgers, reservations, prediction, or Scheduler AUTO routing;
- a daemon, background service, resident watcher, generic workflow engine, ORM, event-sourcing framework, or repository-local orchestrator state;
- automatic installation/upgrading of protocol sources, agents, plugins, or providers;
- speculative backward-compatible profiles for Protocol versions whose exact prompt/workflow contract is not supplied and validated.

## 2. Governing authority and current baseline

### 2.1 Parent authority

This workplan derives from and is subordinate to:

```text
orchestrator/docs/architecture.md
architecture_version = 1.5.0
protocol_version = 5.16.0
```

The architecture's module ladder, dependency direction, API/SPI roles, protocol-profile binding, privacy boundary, Prompt/Tracker/Adapter/Scheduler ownership, and WP-1 acceptance obligations are Frozen for this implementation cycle.

### 2.2 Protocol authority

Implementation/review inherit Protocol 5.16 from this workplan and must use the governing `software-implementation` / `software-design` roles at that version-compatible contract. The canonical human prompt source for the initial profile is:

```text
source/shared/references/development-workflow-prompts.md
```

with workflow/authority semantics additionally governed by the supplied Protocol 5.16 references rather than by a new orchestrator-private doctrine.

### 2.3 Baseline / change-health intake

At WP-1 creation there is no executable orchestrator package under `orchestrator/`; only architecture documentation exists. `workplans/active/` did not exist before this workplan. The baseline therefore has no legacy executable Core machinery to preserve.

The quality ratchet for this greenfield module is consequently:

- do not introduce a second prompt authority;
- do not create persistence, routing, transport, resource, or benchmark machinery below its owning future module;
- keep runtime dependency and public surface proportional to the immediate Core job;
- make objective dependency-direction/packaging invariants executable where cheap;
- ensure important decision boundaries (workplan ambiguity, protocol compatibility, privacy, fingerprinting) have rejection-capable tests rather than mere coverage.

## 3. Frozen high-level architecture and engineering envelope

### 3.1 Distribution/module boundary

WP-1 creates one independently installable Python distribution:

```text
sdp-orchestrator-core
```

under the native PEP 420 namespace:

```text
sdp_orchestrator.core
```

The namespace root must not gain an `sdp_orchestrator/__init__.py` that would prevent later distributions from contributing sibling namespace packages.

The supported initial runtime floor is **Python 3.11+**. Implementation should remain OS-neutral where practical; do not claim untested platform-specific behavior beyond actual acceptance evidence.

### 3.2 Core ownership

Core owns:

- `sdp` CLI/application composition;
- Core configuration/project catalog;
- stable Core identifiers and public records;
- read-only project/Git/workplan observation;
- worktree identity;
- Protocol profile/workflow descriptor resolution;
- canonical prompt-source resolution and packaged compatible snapshot;
- prompt input resolution/rendering;
- `RunId`, prompt fingerprint, and `StageResultEnvelope v1` request contract;
- one extension entry-point registry and service/capability composition root;
- Core-only diagnostics/capability/project commands;
- optional clipboard output.

Core does not own any responsibility listed in §1.3.

### 3.3 One package/CLI composition root

The public console entry point is:

```text
sdp
```

Core discovers installed extensions only through:

```text
sdp_orchestrator.extensions.v1
```

No arbitrary directory scanning, repository plugin loading, `try: import tracker`, or higher-module special casing is permitted.

### 3.4 Configuration boundary

Core uses one TOML configuration path and one validation layer. Default config location is obtained via `platformdirs`; CLI/API may explicitly override the config path. WP-1 does not add an environment-variable override unless implementation evidence shows it is materially necessary.

The v1 configuration semantics are:

```toml
schema_version = 1

[core]
default_project = "mdstats"                 # optional when selection is otherwise unambiguous
default_execution_mode = "web"              # optional; local | web

[projects.mdstats]
repo = "/absolute/path/to/mdstats"
protocol_profile = "sdp-protocol-5.16"
default_execution_mode = "web"              # optional per-project override
```

Additional source/profile fields may be added only when needed to realize the Frozen compatible-source resolver; secrets/tokens are never normal config snapshot values.

CLI project selection when a Core command does not receive an explicit project is Frozen as:

```text
explicit --project
  -> unique configured project whose canonical worktree contains current cwd
  -> configured core.default_project
  -> the sole configured project
  -> AMBIGUOUS / NOT_FOUND
```

The program must not silently choose among multiple plausible projects.

### 3.5 Read-only repository observation

Core uses the configured repository as evidence, not authority over the workplan target. Normal observation is local-only and read-only.

`ObservationPolicy` supports:

```text
local_only
use_cached_remote
refresh_remote
```

Programmatic/default CLI behavior is `local_only`. Network access occurs only when configuration/request explicitly enables it. Results carry observation time/freshness/provenance.

A candidate identifies branch/detached HEAD, commit, upstream/observed remote when known, and material staged/unstaged/untracked state. The versioned `sdp.git-working-tree.v1` identity may use any deterministic Git-native realization that detects source-relevant dirty state without unbounded reads. If relevant state cannot be fingerprinted within safe bounds, set `identity_complete=false`; do not counterfeit a clean/exact identity.

`WorktreeKey` must identify the physical Git worktree rather than only ProjectKey: aliases/symlink paths to the same worktree resolve to the same key, while distinct Git worktrees resolve to distinct keys.

### 3.6 Workplan discovery and resolution

Core catalogs workplans using repository conventions under `workplans/active/` and `workplans/archive/`, including nested `AUTHORITY.md` and frontmatter-marked implementation-workplan documents. Discovery must deduplicate documents that represent the same `workplan_id` and must not treat historical numbered revisions as independent current workplans when a current authority file clearly owns the workplan.

For a stage requiring a governing workplan, resolution is:

```text
explicit workplan selector supplied by PromptRequest/CLI
  -> exact branch binding explicitly declared in workplan metadata, if unique
  -> exactly one active workplan
  -> AMBIGUOUS / REQUIRED
```

No fuzzy filename similarity, mtime recency, or guessed semantic association is acceptance authority.

For Design on a new task, no existing workplan is required when `first_task`/TASK is supplied.

`WorkplanRef` carries exact artifact digest and deterministic semantic digest. Under canonicalization `sdp.workplan-semantic.v1`, known lifecycle-only frontmatter fields may be excluded so archive/status bookkeeping can preserve semantic identity; unknown/unrecognized semantics are treated conservatively. A body/authority change must alter semantic identity. If safe semantic canonicalization cannot be established, set `semantic_identity_complete=false` rather than guessing.

### 3.7 Protocol profile and canonical prompt source

The initial release supports a **Protocol 5.16-compatible profile** and must not claim compatibility with other versions unless explicit supplied evidence/profile fixtures establish it.

Resolution order is Frozen:

```text
explicit configured compatible local protocol source/profile
  -> exact compatible packaged profile/prompt snapshot
  -> explicitly permitted canonical read-only remote source at an explicit evidence-backed ref
  -> truthful INCOMPATIBLE / UNAVAILABLE non-closure
```

A semantic version string is never guessed to be a Git branch/tag. A newer profile may serve older work only after explicit compatibility is represented and tested; WP-1 need not create such compatibility.

The packaged profile/snapshot is **derived/version-bound runtime material**, not a second independently edited prompt authority. Prompt bodies must be extracted/copied reproducibly from the canonical Protocol reference at build/source-preparation time. A small machine-readable profile metadata source is permitted for stage keys, aliases, workflow transition trigger classes, profile compatibility, and source identities, but it must not duplicate prompt prose and must be validated against the canonical prompt/workflow references.

The installed wheel must remain able to render its compatible packaged profile offline when target repository evidence is local and sufficient.

### 3.8 Prompt execution modes and privacy

Core v1 supports prompt execution modes:

```text
local
web
```

`web` is a privacy boundary, not merely presentation:

- no local absolute repository path;
- no orchestrator private-state/config path;
- no credentials/tokens;
- no credential-bearing Git URL/userinfo;
- no future account/quota/resource telemetry;
- repository target uses sanitized remote identity + branch/commit/workplan path where available.

`local` may include local repository/worktree paths needed by a local agent.

The renderer resolves every ordinary input for which Core has authoritative mechanical evidence. Inputs whose meaning requires agent semantic investigation remain the canonical explicit `AUTO`/`NONE` values from the source prompt rather than guessed values. No unresolved square-bracket template placeholder may survive in a successfully rendered prompt unless the canonical prompt explicitly defines that literal as user-facing content.

### 3.9 Prompt stdout contract

For stage prompt commands, stdout is the complete prompt and nothing else. Diagnostics, warnings, ambiguity messages, and errors go to stderr with deterministic exit behavior. This allows:

```text
sdp review > prompt.txt
```

without cleanup.

Optional clipboard behavior is additive (`pyperclip` extra or equivalent). Clipboard unavailability must not make ordinary stdout rendering fail.

## 4. Public Core API/SPI v1 contract to establish

The following semantic public surface is part of WP-1 acceptance. Exact private classes/helpers are delegated. Public records use JSON-compatible immutable-by-convention value semantics; Pydantic is the initial realization but not the contract itself.

### 4.1 Stable public value types

Core must expose at least:

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
```

Opaque IDs serialize as strings. Timestamps serialize as timezone-aware UTC ISO-8601. `DigestRef` carries algorithm + canonicalization scheme + value.

### 4.2 CoreAPI v1

The accepted public method family is:

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

All are read-only with respect to target repositories. `allocate_run_id` allocates identity only and creates no persistent record.

### 4.3 Application/composition API v1

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

Capability keys are semantic and unversioned; API compatibility is separate. Initial Core provisions are at least:

```text
prompt.render
project.observe
workplan.catalog
```

Service registration is by capability + API major + provider. Singular services may not be silently replaced.

### 4.4 Extension SPI v1

Core establishes:

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Manifest inspection is side-effect-minimal: no process launch, network I/O, repository mutation, or storage migration. Activation is dependency-topological. An incompatible/failed extension disables itself and dependents without breaking healthy Core service.

The SPI context supplies only explicit versioned composition services: effective namespaced configuration, already-activated required services, CLI/config/event/diagnostic registration. Do not expose Core private implementation objects.

### 4.5 Workflow profile contract

Core's 5.16 profile exposes:

```text
WorkflowProfileDescriptor
  profile
  schema_version
  stages
  transitions
```

Stage descriptors carry stage identity, role owner, mutation class, optionality, and recognized outcome values. Transition descriptors carry from-stage, opaque profile-defined trigger key, target stage/terminal, optional priority hint, and explanation.

This is a bounded machine-readable projection of Protocol routing, not a generic executable workflow DSL. Core does not infer current next-stage state in WP-1.

### 4.6 PromptRequest / RenderedPrompt

`PromptRequest v1` must represent:

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

`RenderedPrompt v1` must return:

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

`list_stages()` is a bounded convenience view over `workflow().stages`, never a separate stage authority.

### 4.7 Prompt fingerprint and result-envelope contract

Under `sdp.prompt-fingerprint.v1`:

1. allocate/use RunId;
2. render the exact prompt bytes with a fixed fingerprint placeholder;
3. hash the exact UTF-8 placeholder-form artifact with SHA-256;
4. substitute `sha256:<hex>` into the final artifact.

WP-1 must freeze the literal placeholder and normalization by executable fixture.

Every prompt requests `StageResultEnvelope v1` carrying at minimum:

```text
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
```

`BlockerRecord` includes optional id, optional classification, summary, and optional authority class. The footer must not request hidden chain-of-thought. Core does not interpret/persist the result in WP-1.

### 4.8 Error contract

Public Python failures raise one `OrchestratorError` carrying:

```text
Problem(code, message, retryable, details)
```

Consumers branch on stable namespaced code, not human message text. WP-1 must establish/test a minimal useful code set covering at least:

```text
core.config.invalid
core.project.not_found
core.project.ambiguous
core.repository.invalid
core.workplan.required
core.workplan.ambiguous
core.protocol.incompatible
core.protocol.unavailable
core.stage.unknown
core.remote.unavailable
core.extension.incompatible
core.extension.activation_failed
core.clipboard.unavailable
```

Do not create a large exception subclass hierarchy.

## 5. Implementation obligations and delegated solution space

### O1 — Establish the Core distribution and packaging boundary

**Concern / rationale:** every later module depends asymmetrically on an independently usable Core package.

**Required end state:** `sdp-orchestrator-core` builds as a standard Python distribution, provides the PEP 420 namespace and `sdp` console entry point, declares only justified Core dependencies, and contains the compatible packaged Protocol profile/prompt resources required for offline rendering.

**Runtime dependencies:** use the architecture-approved focused set unless evidence shows a simpler equivalent:

```text
platformdirs
typer
pydantic
python-frontmatter
packaging
```

Clipboard support is optional (`pyperclip` extra or equivalent); Core runtime must not require `filelock`, ACP, `httpx`, ORM/event-sourcing, ML, Tracker, Adapter, or Scheduler packages.

**Delegated:** PEP 517 build backend, exact internal package/module layout below public paths, test runner details.

**Acceptance:** build wheel/sdist as supported; independently inspect metadata/resources/entry point; install wheel into an isolated environment outside source checkout; run `sdp --help`, `sdp projects`, and at least one prompt command through the installed entry point.

### O2 — Implement one validated Core configuration/project resolution path

**Required end state:** TOML config, explicit API/CLI overrides, project selection, execution mode, and profile selection pass through one canonical validation/resolution layer with provenance; no duplicate CLI-only config semantics.

**Acceptance:** tests for explicit project, cwd project, configured default, sole project, ambiguity, invalid/missing repo, config precedence, local/web default override, and redaction/no secret persistence.

### O3 — Implement read-only Git/project/worktree observation

**Required end state:** Core observes real Git repositories without mutation, returns stable ProjectDescriptor/CandidateRef/WorktreeKey, detects relevant dirty state conservatively, and separates local path data from sanitized prompt-safe context.

**Acceptance boundary:** exercise actual temporary Git repositories/worktrees using the production observer; do not accept a test that replaces the observer owner with precomputed candidate objects.

**Acceptance:** branch/detached HEAD, upstream known/unknown, staged+unstaged+untracked changes, symlink alias same WorktreeKey, distinct Git worktree different WorktreeKey, credential-bearing remote sanitization, identity-incomplete bounded-input case, target `git status --porcelain` unchanged by Core commands.

### O4 — Implement deterministic workplan catalog/resolution/identity

**Required end state:** catalog active/archive plans across supported repository conventions, expose paginated descriptors, compute artifact + semantic identities, and select only with the deterministic rules in §3.6.

**Acceptance:** top-level active plan, nested `AUTHORITY.md`, archive lifecycle move, exact semantic-body change, lifecycle-only metadata change, multiple active ambiguous, explicit selector, explicit branch metadata match, no-active Design case, required-workplan failure for Implementation/Review.

**Oracle-strength relation:** a counterfactual repository with two plausible active plans must fail rather than select one by mtime/path ordering.

### O5 — Implement Protocol 5.16 profile/snapshot generation and resolver

**Required end state:** installed Core has a version-bound compatible Protocol 5.16 profile containing prompt source and WorkflowProfileDescriptor. Prompt bodies are reproducibly obtained from canonical Protocol source rather than independently rewritten.

**Acceptance:** source-to-packaged prompt parity for all stage blocks; workflow stage keys/aliases correspond to canonical source; profile transition metadata is reconciled against the supplied 5.16 workflow references; package records source/profile digest/identity; offline wheel rendering succeeds; 5.15/unknown workplan does not silently render with 5.16; explicit incompatible local/remote source fails truthfully.

**Anti-shortcut:** copying current prompt text into Python constants and testing only those constants against themselves does not satisfy canonical-source parity.

### O6 — Implement CoreAPI/ApplicationAPI/extension SPI v1

**Required end state:** public imports exist at the architecture paths, stable value models serialize cleanly, application composition discovers the single entry-point group, capability/API-major compatibility is enforced, and failed optional providers degrade cleanly.

**Acceptance:** API import/serialization fixtures; semantic capability key separate from API version; fake compatible and incompatible providers exercise production composition root; duplicate singular service rejected; extension manifest inspection has no activation side effects; Core still renders when optional provider fails activation.

**Objective architecture-fitness rule:** static/import test rejects production Core imports of `sdp_orchestrator.tracker`, `.adapters`, or `.scheduler`, and rejects root `sdp_orchestrator/__init__.py` ownership.

### O7 — Implement canonical prompt input resolution/rendering

**Required end state:** stage alias resolves through the compatible workflow profile; mechanical project/branch/candidate/workplan/protocol variables are concretely populated; semantic-discovery values remain explicit canonical `AUTO`/`NONE`; successful prompt contains no unresolved user-edit placeholder that Core should have resolved.

**Acceptance:** golden semantic fixtures for Design, Implementation, Review, Verification and at least one optional stage; explicit input override precedence; new-task Design without workplan; prompt-source/profile identities; no accidental cross-stage prompt body.

### O8 — Implement local/web privacy modes

**Required end state:** RenderedPrompt uses PromptProjectSnapshot appropriate to execution mode.

**Acceptance:** fixture repo/config containing distinctive local home path, private config path, credential-bearing HTTPS remote, SSH-style remote, and unrelated secret-like config values; web prompt/output must not contain prohibited local/credential data while retaining sufficient remote repository/branch/workplan context; local mode may contain authorized local repo path but still never secrets.

**Acceptance boundary:** inspect the final `prompt_text` from the production renderer/installed CLI, not a sanitized helper return alone.

### O9 — Implement RunId/fingerprint/StageResultEnvelope v1

**Required end state:** caller-supplied RunId is preserved; auto RunId is opaque/unique enough for local attempt identity; fingerprint follows the frozen placeholder algorithm; footer includes matching identity and structured result request without chain-of-thought demand.

**Acceptance:** same fixed RunId + identical observations/source yields same fingerprint; changing stage/workplan/candidate/mode materially changes fingerprint; self-placeholder fixture verifies algorithm; final prompt contains final digest and no placeholder token; result schema fields/BlockerRecord are present.

### O10 — Implement Core CLI behavior

**Required commands:**

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

Equivalent stage aliases may be added only without changing these canonical names.

**Required behavior:** prompt commands emit prompt only to stdout; diagnostics/errors to stderr; deterministic nonzero exits on ambiguity/incompatibility; `--project`, `--workplan`, `--execution-mode`, `--config`, and observation-policy override have API-equivalent semantics; optional `--copy` never removes stdout usability.

**Acceptance boundary:** execute the installed `sdp` entry point in subprocess tests; direct Typer callback invocation alone is insufficient.

### O11 — Core-only documentation and operator usability

**Required end state:** concise user documentation under `orchestrator/docs/` or Core package docs explains installation, config path/schema, project selection, stage commands, web/local mode, workplan ambiguity handling, protocol-version binding, piping/copying, and the explicit absence of Tracker/Adapter/Scheduler features.

Do not document planned higher-module commands as currently available.

### O12 — Final assembled conformance and simplicity reconciliation

Before implementation completion, reconcile every WP-1 obligation against the assembled Core. Remove unused compatibility shims, duplicate prompt/profile representations, speculative persistence/transport/resource hooks, or helpers whose only purpose is future modules rather than the accepted API/SPI seam.

Re-derive final affected surface and run complete Core affected regression, package/install integration, and repository-required Protocol tests.

## 6. Implementation authority

### 6.1 Frozen

The following are Frozen for WP-1:

- parent architecture 1.5.0 module/dependency/ownership boundaries;
- Core-only independent usefulness;
- `sdp-orchestrator-core` + `sdp` ownership;
- PEP 420 shared namespace and one extension entry-point group;
- public Core API/SPI semantic method families in §4;
- Python 3.11+ initial compatibility floor;
- read-only target repository behavior;
- deterministic project/workplan ambiguity behavior;
- Protocol-version-bound compatible profile resolution;
- canonical/derived prompt-source relationship;
- local/web privacy separation;
- RunId -> route-independent prompt-attempt identity, prompt fingerprint v1, StageResultEnvelope v1 request seam;
- no Tracker/Adapter/Scheduler responsibilities in Core.

### 6.2 Delegated

Implementation may choose/simplify:

- exact private class/function/module decomposition;
- PEP 517 backend and test-runner mechanics;
- Git plumbing commands/library-free implementation, provided it stays read-only and satisfies identity semantics;
- internal prompt parser/extractor implementation;
- exact cache structure for bounded packaged/profile source caches;
- text formatting of non-prompt diagnostic commands;
- internal Pydantic model decomposition and validators so long as accepted public v1 wire semantics remain intact;
- optional clipboard implementation;
- standard-library versus focused dependency realization where the resulting system is simpler and contract-equivalent.

Do not add abstractions solely because a later module might hypothetically need them; later modules consume the accepted v1 API/SPI.

### 6.3 Reopen Design only on evidence

Reopen only the affected parent/API surface if implementation demonstrates that:

- Core cannot expose the required workflow/profile information without a materially different ownership boundary;
- canonical prompt source cannot be converted into an offline compatible package without creating a second authority under the current Frozen source model;
- the public Core API/SPI method families cannot support the accepted Tracker/Adapter dependency direction without private imports/reverse dependency;
- one extension registry cannot compose the required modules safely;
- supported target-repository/workplan structures cannot be represented without changing the Frozen workplan identity/selection model;
- Python 3.11+ materially violates an independently required compatibility target;
- local/web privacy cannot be preserved under the selected prompt-context ownership model.

Ordinary parser, packaging-backend, Git-command, model-field, or CLI formatting changes remain Implementation discretion.

## 7. Affected surface and task-specific acceptance

### 7.1 Expected product surface

Initially expected new/changed surface:

```text
orchestrator/core/                         # new Core distribution/workspace
orchestrator/docs/                         # Core user/operator docs; architecture preserved
workplans/active/PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE.md
source/shared/references/development-workflow-prompts.md   # read-only canonical input unless a proven defect requires Design
source/shared/references/workflow-and-workplans.md         # read-only authority input
repository packaging/CI configuration only where needed to build/test Core
repository tests/qualification only where needed for Core acceptance/architecture fitness
```

The final affected surface must be re-derived from the assembled implementation; this list is not a ceiling.

### 7.2 Real semantic-owner acceptance boundaries

1. **Prompt product boundary:** installed `sdp` console entry point -> Core composition -> project/workplan/profile observer/resolver -> production renderer -> stdout. A helper that returns expected text while installed CLI is broken cannot close the prompt claim.
2. **Repository observation boundary:** production Core observer executes against actual temporary Git repositories/worktrees. Preconstructed `CandidateRef` fixtures may unit-test downstream logic but cannot close observer behavior.
3. **Canonical-source boundary:** package/source preparation reads the actual canonical Protocol prompt reference and validates generated packaged resources; a test comparing two copies generated from the same stale private constant cannot prove parity.
4. **Packaging boundary:** built wheel installed outside source tree; source checkout import success is insufficient.
5. **Privacy boundary:** inspect final production `RenderedPrompt.prompt_text` / installed CLI stdout for leak claims.
6. **Extension composition boundary:** production application composition/service registry executes with representative compatible/incompatible test providers; replacing the composition owner with a fake registry does not close the claim.

### 7.3 Required functional evidence

At minimum, final acceptance includes:

- focused Core API/config/observer/workplan/profile/renderer/fingerprint/SPI tests;
- Core stage-local affected regression after each material executable stage;
- final Core affected regression on the assembled candidate;
- existing repository protocol regression suite because shared packaging/tests/CI may be affected;
- build + independent artifact inspection + isolated installed-wheel CLI integration;
- `git diff --check` or repository equivalent;
- project-configured fast Python lint/type/static checks if such checks exist or are introduced as part of the Core package; do not add a second checker merely for protocol symmetry;
- objective import-direction/namespace-package guards;
- no-network/offline packaged-profile prompt integration;
- web privacy and credential-redaction integration;
- ambiguity/incompatibility rejection counterfactuals.

If impact cannot be bounded confidently after implementation, run the broader/full available test suite.

### 7.4 Production qualification

**Unnecessary for WP-1.** Core is local metadata/prompt orchestration with bounded inputs; no production-scale performance/resource claim is being made. Basic bounded latency/resource sanity may be observed, but no separate production qualification is required.

## 8. Implementation sequence

### Stage 1 — Core package, public contracts, config, and repository observation

Create the distribution/namespace/entry point, Core API/SPI value/service contracts, canonical config/project resolution, read-only Git/Candidate/Worktree observation, and workplan catalog/identity/resolution.

**Stage closure:** focused contract/config/Git/workplan tests + affected Core regression; no higher-module imports/persistence.

### Stage 2 — Protocol profile/snapshot and prompt renderer

Implement version-bound profile/source resolution, reproducible canonical prompt extraction/packaged snapshot, WorkflowProfileDescriptor, input resolver, local/web context, RunId/fingerprint/result-envelope footer, stage aliases, and prompt-only stdout behavior.

**Stage closure:** canonical-source parity, protocol incompatibility counterfactual, local/web privacy, fingerprint fixtures, stage prompt integration, offline packaged-profile test + affected regression.

### Stage 3 — Composition/CLI/package integration and final closure

Complete extension discovery/service registry, Core diagnostics/project commands, optional clipboard, operator docs, build/install integration, architecture-fitness checks, full accepted-contract reconciliation, final affected-surface regression, existing repository checks, and simplification cleanup.

**Stage closure:** isolated installed-wheel end-to-end acceptance on representative temporary target repositories, full required regression, package inspection, no higher-module leakage, and implementation handoff ready for independent Review.

## 9. Genuine simplification triggers

Before adding durable machinery, simplify/re-derive if implementation starts producing:

- a second manually maintained set of prompt bodies;
- separate local/web renderers that duplicate most prompt logic instead of one context policy;
- multiple project/config resolution paths for CLI versus API;
- multiple plugin registries/loaders;
- a generic workflow engine instead of the bounded 5.16 descriptor;
- persistent run/event tables or database abstractions in Core;
- transport/account/model/resource placeholder classes in Core;
- fuzzy workplan-selection heuristics that require exception stacks;
- wrappers/fallbacks compensating for an unnecessarily complicated profile extraction mechanism;
- custom semantic-version, TOML, YAML, CLI, or packaging machinery where maintained focused libraries already own the problem;
- public API records leaking Git subprocess/Pydantic/private implementation objects rather than stable values.

## 10. Final workplan review

The plan was derived against the current frozen architecture and Protocol 5.16 Software Design workplan/testing/architecture/versioning/Python/configuration/security/release rules.

Snapshot-loss counterfactual: with prior chats and Git history removed, `orchestrator/docs/architecture.md`, this workplan, and the supplied Protocol 5.16 source/reference tree recover the complete WP-1 product/Frozen contract, non-goals, public API/SPI role, expected acceptance boundaries, and Design-reopen triggers.

No Tracker, Adapter, benchmark, metering, prediction, or Scheduler implementation is necessary to satisfy WP-1. The future-facing surface is limited to the public API/SPI and identifiers explicitly required by the parent architecture.

**Design verdict: PASS — WP-1 Prompt Module + Core Program is snapshot-complete and ready for `software-implementation`.**
