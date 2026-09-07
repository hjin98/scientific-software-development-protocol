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

Build the smallest independently useful Protocol Orchestrator product: a user configures a target software repository, runs a command such as

```text
sdp design --task "..."
sdp implementation
sdp review
sdp prompt verification
```

and receives on stdout one complete, copy/paste-ready, stage-correct Protocol prompt whose mechanically knowable repository/workplan/protocol inputs are already resolved.

This Core-only installation is a finished product mode. It must not require a history database, agent integration, benchmark service, quota meter, or scheduler.

### 1.2 Tier-1 product invariants

1. Core alone performs prompt retrieval/resolution/rendering end to end.
2. Core observation is read-only with respect to the configured target repository: no checkout, pull, merge, rebase, commit, push, edit, or hidden mutation.
3. Prompt bodies come from a governing-version-compatible canonical SDP prompt source; Core may package derived/version-bound snapshots but may not create an independently edited second prompt authority.
4. A workplan bound to Protocol version `X` is never silently interpreted with an incompatible newer profile.
5. Repository/workplan/profile ambiguity is explicit; Core does not guess using mtime, fuzzy names, or ungrounded heuristics.
6. Web-mode prompt rendering excludes local paths, private state/config paths, credentials, and credential-bearing remotes; local mode may include authorized local execution context.
7. The accepted Core API/SPI is sufficient for later Tracker/Adapter/Scheduler modules without private imports or reverse dependency.
8. Core does not pre-implement durable history, next-stage projection, agent transport, benchmark recommendation, metering, prediction, or automatic routing.
9. Core owns the single `sdp` CLI/composition root and the single extension entry-point group.
10. Every rendered prompt carries `RunId`, prompt fingerprint, and a requested `StageResultEnvelope v1`, establishing a future Tracker-compatible result seam without adding persistence now.

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
- speculative compatibility profiles for unsupplied/untested Protocol versions.

## 2. Governing authority and baseline

### 2.1 Parent authority

This workplan derives from and is subordinate to:

```text
orchestrator/docs/architecture.md
architecture_version = 1.5.0
protocol_version = 5.16.0
```

The parent module ladder, ownership, dependency direction, API/SPI roles, protocol-profile binding, privacy boundary, and WP-1 acceptance obligations are Frozen for this implementation cycle.

### 2.2 Protocol authority

Implementation/review inherit Protocol 5.16. Initial canonical prompt source:

```text
source/shared/references/development-workflow-prompts.md
```

Workflow/authority semantics remain governed by the supplied Protocol 5.16 source/reference tree, not by a new orchestrator-private doctrine.

### 2.3 Baseline / quality ratchet

At workplan creation, `orchestrator/` contains architecture documentation but no executable Core package. There is therefore no legacy Core machinery to preserve.

The greenfield quality ratchet is:

- no second prompt authority;
- no higher-module machinery below its owning future module;
- minimal justified runtime/public surface;
- executable guards for objective package/dependency direction;
- rejection-capable tests for ambiguity, compatibility, privacy, and identity rather than coverage-only evidence.

## 3. Frozen high-level architecture and engineering envelope

### 3.1 Distribution and namespace

Create one independently installable distribution:

```text
sdp-orchestrator-core
```

under native PEP 420 namespace `sdp_orchestrator.core`. The namespace root must not contain `sdp_orchestrator/__init__.py`.

Initial supported runtime floor: **Python 3.11+**. Keep implementation OS-neutral where practical; claim only platform behavior actually tested.

### 3.2 Core ownership

Core owns:

- `sdp` CLI/application composition;
- Core configuration/project catalog;
- public Core identifiers/value records;
- read-only Git/project/workplan observation;
- worktree identity;
- compatible Protocol profile/workflow descriptor resolution;
- canonical prompt source resolution + packaged compatible snapshot;
- prompt input resolution/rendering;
- RunId/fingerprint/result-envelope request identity;
- one extension registry/service composition root;
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

Use one TOML resolution/validation path. Default config location comes from `platformdirs`; CLI/API can explicitly override it. Do not add environment overrides unless implementation evidence makes one necessary.

V1 semantics:

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

CLI project resolution when `--project` is absent:

```text
unique configured project containing cwd
  -> core.default_project
  -> sole configured project
  -> AMBIGUOUS / NOT_FOUND
```

An explicit `--project` overrides that chain. The API itself receives explicit `ProjectKey`.

### 3.5 Read-only repository/candidate/worktree observation

`ObservationPolicy` supports:

```text
local_only
use_cached_remote
refresh_remote
```

Default is `local_only`; network use requires explicit request/configuration. Results carry provenance/freshness.

`CandidateRef` captures branch/detached HEAD, commit, relevant staged/unstaged/untracked state, upstream/observed remote when known, and identity completeness. `sdp.git-working-tree.v1` may use any bounded deterministic Git-native realization. If relevant state cannot be safely fingerprinted, set `identity_complete=false` rather than claiming exact identity.

`WorktreeKey` identifies the physical Git worktree: path aliases to the same worktree resolve to the same key; distinct Git worktrees resolve to distinct keys.

### 3.6 Workplan discovery, resolution, identity

Catalog repository conventions under `workplans/active/` and `workplans/archive/`, including nested current `AUTHORITY.md` files and frontmatter-marked implementation workplans. Deduplicate documents sharing the same `workplan_id`; do not treat historical numbered revisions as independent active authorities when a current authority file clearly owns the workplan.

For a stage requiring a governing workplan:

```text
explicit selector
  -> unique exact branch binding explicitly declared in workplan metadata
  -> exactly one active workplan
  -> AMBIGUOUS / REQUIRED
```

No fuzzy filename matching or recency guessing.

Design of a new task may proceed without an existing workplan only when `first_task`/`--task` is supplied.

`WorkplanRef` carries exact artifact digest plus deterministic semantic digest. `sdp.workplan-semantic.v1` may exclude only documented lifecycle-only frontmatter so lifecycle moves/status bookkeeping can preserve semantic identity. Unknown semantics are conservative. If safe canonicalization is unavailable, mark semantic identity incomplete.

### 3.7 Protocol profile and prompt source

Initial release supports a Protocol 5.16-compatible profile only, unless additional compatibility is explicitly supplied and tested.

Resolution order:

```text
explicit configured compatible local source/profile
  -> exact compatible packaged profile/prompt snapshot
  -> explicitly permitted canonical read-only remote source at explicit evidence-backed ref
  -> truthful INCOMPATIBLE / UNAVAILABLE
```

Never guess a semantic version string as a Git ref.

The packaged profile/snapshot is derived runtime material. Canonical stage prompt bodies must be reproduced from `development-workflow-prompts.md`, not independently rewritten. A small machine-readable profile metadata source is allowed for stage keys/aliases, transition trigger classes, compatibility, and source identity, but it must not duplicate prompt prose and must be validated against supplied Protocol references.

Installed wheel must render its compatible packaged profile offline when target-repository evidence is local and sufficient.

### 3.8 Prompt rendering modes and privacy

Core v1 execution modes:

```text
local
web
```

Web prompt must exclude local absolute repository/config/private-state paths, credentials/tokens, and credential-bearing Git URL userinfo. It uses sanitized remote repository identity plus branch/commit/workplan path where available. Local mode may include authorized local paths but still never secrets.

Renderer fills all mechanically supported stage inputs. Values requiring semantic agent investigation remain canonical explicit `AUTO`/`NONE`; Core does not guess them. A successful render contains no unresolved square-bracket user-edit placeholder that Core was responsible for resolving.

### 3.9 Canonical body plus orchestrator footer

The canonical stage prompt body is preserved except for filling its declared `INPUTS` values. Core may append only the architecture-approved orchestration metadata/result-request footer containing RunId/fingerprint/result-envelope instructions.

The footer is not an alternate stage prompt and may not weaken, replace, or reinterpret the canonical stage body. Canonical-source parity tests compare the stage body separately from this appended footer.

### 3.10 Prompt stdout contract

Prompt commands write exactly the complete prompt to stdout; diagnostics/errors go to stderr with deterministic nonzero exits. Therefore:

```text
sdp review > prompt.txt
```

produces a clean prompt artifact. Optional clipboard support is additive and may never make stdout rendering dependent on clipboard availability.

## 4. Public Core API/SPI v1 contract

### 4.1 Public value types

Expose at least:

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

Opaque IDs serialize as strings; timestamps as UTC ISO-8601; `DigestRef` carries algorithm + canonicalization scheme + value. Public records are JSON-compatible immutable-by-convention values. Pydantic is initial realization, not contract authority.

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

All methods are read-only with respect to target repositories. `allocate_run_id` creates identity only, no persistent record. `list_stages()` is a bounded view of `workflow().stages`, not separate authority.

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

Initial Core capability keys include `prompt.render`, `project.observe`, and `workplan.catalog`. Capability key is semantic/unversioned; API compatibility is separate. Singular service registration cannot silently replace another provider.

### 4.4 Extension SPI v1

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Manifest inspection is side-effect-minimal: no subprocess, network, repository mutation, or storage migration. Activation is dependency-topological. Failed/incompatible optional providers disable themselves/dependents without breaking healthy Core.

Context exposes only explicit versioned composition services: effective namespaced config, already-active required services, CLI/config/event/diagnostic registrars. No Core private implementation object crosses the SPI.

### 4.5 WorkflowProfileDescriptor v1

Profile exposes bounded machine-readable Protocol routing:

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

`trigger_key` is profile-defined opaque routing class, not executable expression text. Core exposes the profile but does not infer the current next action in WP-1.

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
3. SHA-256 hash exact UTF-8 placeholder-form bytes;
4. substitute `sha256:<hex>`.

WP-1 freezes the literal placeholder/normalization with executable fixtures.

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
core.workplan.ambiguous
core.protocol.incompatible
core.protocol.unavailable
core.stage.unknown
core.remote.unavailable
core.extension.incompatible
core.extension.activation_failed
core.clipboard.unavailable
```

Do not create a broad exception subclass hierarchy.

### 4.9 CLI request mapping

The CLI must expose every Core-only input needed to form a complete PromptRequest without interactive stdout contamination:

```text
--project <ProjectKey>
--workplan <selector>
--execution-mode local|web
--config <path>
--remote-mode local_only|use_cached_remote|refresh_remote
--task <text>                         # maps to first_task; required for workplan-free Design
--input NAME=VALUE                    # repeatable; maps to input_overrides
--copy                                # optional clipboard extra
```

`--task` and `--input` are ordinary data inputs, not permission to override higher authority. A missing required first task fails clearly instead of prompting on stdout.

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

**Acceptance:** build wheel/sdist as supported; independently inspect metadata/resources/entry point; install wheel outside source checkout; execute installed `sdp --help`, `sdp projects`, and prompt command.

### O2 — Canonical config/project resolution

Implement the §3.4 TOML/project resolution through one API/CLI path with provenance.

**Acceptance:** explicit project, cwd match, configured default, sole project, ambiguity, invalid repo, CLI/API precedence, mode override, and secret-redaction cases.

### O3 — Real read-only Git/worktree observation

Implement production observer for actual Git repositories.

**Acceptance boundary:** actual temporary Git repos/worktrees, not precomputed CandidateRefs.

**Acceptance:** branch/detached HEAD; upstream known/unknown; staged/unstaged/untracked state; symlink alias same WorktreeKey; separate Git worktree different key; credential-bearing remote sanitization; identity-incomplete bounded case; target `git status --porcelain` unchanged after Core commands.

### O4 — Workplan catalog/resolution/semantic identity

Support current active/archive conventions, nested `AUTHORITY.md`, frontmatter IDs, deterministic selection and conservative identity.

**Acceptance:** top-level plan; nested authority; archive/lifecycle-only change; body semantic change; multiple active ambiguity; explicit selector; exact branch-metadata match; Design without plan + task; required-plan failure for Implementation/Review.

**Counterfactual:** two plausible active plans must fail rather than select by mtime/path ordering.

### O5 — Version-bound Protocol 5.16 profile/snapshot

Produce reproducible packaged prompt/profile resources from canonical supplied Protocol authority.

**Acceptance:** source-to-packaged stage-body parity for all stages; workflow keys/aliases/transitions reconciled with supplied 5.16 references; package source/profile identity recorded; offline installed-wheel rendering; older/unknown workplan not silently rendered as 5.16; incompatible explicit source fails truthfully.

**Anti-shortcut:** comparing two copies derived from the same stale private constant does not prove canonical-source parity.

### O6 — Core API/Application API/extension SPI v1

Implement public import paths, JSON-compatible records, composition/service registry, capability/API-major matching, and graceful optional-provider degradation.

**Acceptance:** API serialization fixtures; capability/version separation; representative compatible/incompatible test providers through production composition root; duplicate singular service rejected; manifest inspection has no activation side effects; failed optional provider does not break prompt rendering.

**Architecture fitness:** reject Core production imports of `sdp_orchestrator.tracker`, `.adapters`, or `.scheduler`; reject root namespace `__init__.py` ownership.

### O7 — Canonical prompt renderer

Resolve stage via compatible profile; fill mechanically known inputs; preserve canonical `AUTO`/`NONE` for semantic discovery; preserve canonical stage body except declared INPUT substitution; append only approved orchestrator footer.

**Acceptance:** Design, Implementation, Review, Verification, and at least one optional-stage fixture; explicit `--input`/API override parity; workplan-free Design with `--task`; no cross-stage body; no unresolved Core-owned placeholder.

### O8 — Local/web privacy boundary

Test a fixture containing distinctive home/config/private paths, credential-bearing HTTPS remote, SSH-style remote, and unrelated secret-like values.

**Acceptance boundary:** final production `RenderedPrompt.prompt_text` and installed CLI stdout.

Web output must contain none of the prohibited local/credential values while retaining sufficient remote/branch/workplan identity. Local output may include authorized repo path but never secrets.

### O9 — RunId/fingerprint/StageResultEnvelope v1

Preserve caller RunId, allocate opaque IDs otherwise, implement the frozen placeholder hash, and append matching structured result request without chain-of-thought demand.

**Acceptance:** fixed RunId + identical observation/source gives identical fingerprint; stage/workplan/candidate/mode change alters fingerprint when artifact changes; placeholder algorithm fixture; final prompt has digest and no placeholder; result schema/BlockerRecord present.

### O10 — Core CLI

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

Canonical option mapping is §4.9. Prompt command stdout is prompt-only; diagnostics stderr; deterministic nonzero exits on ambiguity/incompatibility. Optional `--copy` cannot remove stdout usability.

**Acceptance boundary:** installed `sdp` subprocess execution; direct Typer callback tests alone are insufficient.

### O11 — Core-only user documentation

Document installation, config location/schema, project selection, `--task`, `--input`, stage commands, local/web behavior, ambiguity handling, protocol binding, piping/copying, and explicit absence of Tracker/Adapter/Scheduler features. Do not present future commands as current.

### O12 — Final assembled conformance/simplicity closure

Reconcile every obligation against assembled Core. Remove duplicate prompt/profile representations, speculative persistence/transport/resource hooks, unused compatibility shims, and helpers serving only hypothetical later modules rather than accepted API/SPI seams.

Re-derive final affected surface and run complete Core affected regression, package/install integration, and repository-required Protocol regression.

## 6. Implementation authority

### Frozen

- parent architecture 1.5.0 module/dependency/ownership boundaries;
- Core independent usefulness;
- `sdp-orchestrator-core`, `sdp`, PEP 420 namespace, one extension group;
- public Core API/SPI semantic method families in §4;
- Python 3.11+ initial compatibility floor;
- read-only target behavior;
- deterministic project/workplan ambiguity rules;
- version-bound Protocol profile resolution;
- canonical prompt body + derived packaged snapshot relationship;
- local/web privacy separation;
- RunId/fingerprint v1/StageResultEnvelope v1 request seam;
- no Tracker/Adapter/Scheduler responsibilities in Core.

### Delegated

- private class/function/module decomposition;
- PEP 517 backend/test-runner details;
- Git plumbing implementation satisfying read-only identity semantics;
- internal prompt parser/extractor;
- bounded profile/source cache layout;
- non-prompt diagnostic formatting;
- internal Pydantic decomposition/validators preserving accepted wire semantics;
- optional clipboard implementation;
- standard-library versus focused dependency choice when contract-equivalent and simpler.

Do not add abstractions merely for hypothetical later use; later modules consume accepted v1 APIs/SPIs.

### Reopen only on evidence

Reopen only affected Design surface if evidence shows:

- required workflow/profile information cannot be exposed without materially different ownership;
- canonical prompt cannot be packaged offline without creating a second authority under current model;
- Core API/SPI cannot support Tracker/Adapter direction without private/reverse dependency;
- one extension registry cannot compose required modules safely;
- material target workplan conventions cannot fit the Frozen identity/resolution model;
- Python 3.11+ violates an independently required compatibility target;
- local/web privacy cannot be preserved under current prompt-context ownership.

Ordinary parser, packaging backend, Git command, internal model field, or diagnostic formatting changes remain Implementation discretion.

## 7. Affected surface and task-specific acceptance

### 7.1 Expected affected surface

```text
orchestrator/core/                         # new Core distribution
orchestrator/docs/                         # Core user/operator docs; architecture preserved
workplans/active/PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE.md
repository packaging/CI/tests only where required for Core build/acceptance
source/shared/references/development-workflow-prompts.md   # canonical input; do not modify absent proven authority defect
source/shared/references/workflow-and-workplans.md         # authority input
```

Re-derive final surface from assembled implementation; this is not a ceiling.

### 7.2 Real semantic-owner boundaries

1. **Prompt product:** installed `sdp` -> Core composition -> production observer/resolver/renderer -> stdout. A direct helper returning expected text cannot close a broken installed CLI.
2. **Repository observation:** production observer against actual temporary Git repositories/worktrees.
3. **Canonical source:** source/package preparation reads actual canonical Protocol prompt source; stale private-copy self-comparison cannot close parity.
4. **Packaging:** built wheel installed outside source tree.
5. **Privacy:** final `prompt_text` / installed CLI stdout.
6. **Extension composition:** production composition/service registry with representative test providers; do not replace the owner with a fake registry.

### 7.3 Required evidence

At minimum:

- focused API/config/Git/workplan/profile/renderer/fingerprint/SPI tests;
- stage-local affected regression after each material executable stage;
- final Core affected regression;
- existing repository Protocol regression suite when shared packaging/tests/CI are affected;
- built artifact inspection + isolated installed-wheel CLI integration;
- objective import-direction/namespace-package guards;
- offline packaged-profile prompt integration;
- web privacy/credential-redaction integration;
- ambiguity/incompatibility counterfactuals;
- project-configured fast Python static checks if present or legitimately introduced; do not add a second checker for symmetry;
- `git diff --check` or repository equivalent.

If final impact cannot be bounded confidently, run the broader available suite.

Production qualification: **unnecessary** for WP-1; no production-scale performance/resource claim is being made.

## 8. Implementation sequence

### Stage 1 — Package/contracts/config/repository observation

Create distribution/namespace/entry point, public API/SPI values/services, canonical config/project resolution, Git/Candidate/Worktree observation, and workplan catalog/identity/resolution.

**Closure:** focused contract/config/Git/workplan tests + affected Core regression; no higher-module imports/persistence.

### Stage 2 — Protocol profile/snapshot + prompt renderer

Implement version-bound source/profile resolution, reproducible canonical stage extraction/packaged snapshot, WorkflowProfileDescriptor, input resolver, local/web context, RunId/fingerprint/result footer, stage aliases, `--task`/`--input`, and prompt-only stdout.

**Closure:** source parity; incompatible-version rejection; local/web privacy; fingerprint fixtures; Design task and other stage prompt integration; offline packaged-profile test + affected regression.

### Stage 3 — Composition/CLI/package integration and final closure

Complete extension composition, diagnostics/projects commands, optional clipboard, docs, build/install integration, architecture-fitness checks, final accepted-contract reconciliation, final affected regression, existing repository checks, and simplification cleanup.

**Closure:** isolated installed-wheel end-to-end acceptance on representative temporary target repositories and implementation handoff ready for independent Review.

## 9. Simplification triggers

Simplify/re-derive before adding machinery if implementation starts producing:

- a second manually maintained prompt-body set;
- duplicated local/web renderers instead of one context policy;
- separate CLI/API config semantics;
- multiple plugin registries/loaders;
- a generic workflow engine instead of bounded 5.16 descriptors;
- persistent run/event/database machinery in Core;
- transport/model/account/resource placeholder objects in Core;
- fuzzy workplan heuristic exception stacks;
- wrappers/fallbacks compensating for an overcomplicated profile extractor;
- custom semver/TOML/YAML/CLI/package machinery where focused maintained libraries already own the problem;
- public objects leaking Git subprocess/Pydantic/private implementation state.

## 10. Final workplan review

This plan was derived against the current frozen orchestrator architecture and the remote Protocol 5.16 `software-design` role plus required workflow, testing, architecture, versioning, Python, configuration, security, specification, and release guidance.

Snapshot-loss counterfactual: with prior chat and Git history removed, `orchestrator/docs/architecture.md`, this workplan, and the supplied Protocol 5.16 source/reference tree recover all still-binding WP-1 problem/Frozen semantics, public API/SPI roles, non-goals, acceptance boundaries, and Design-reopen triggers.

No Tracker, Adapter, benchmark, metering, prediction, or Scheduler implementation is required for WP-1. The only future-facing machinery justified now is the parent-required public API/SPI and stable identifiers.

**Design verdict: PASS — WP-1 Prompt Module + Core Program is snapshot-complete and ready for `software-implementation`.**
