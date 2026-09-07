---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: active
parent_architecture: orchestrator/docs/architecture.md
parent_architecture_version: 1.6.0
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

# Protocol Orchestrator WP-1 — Prompt Module + Core Program

## 1. Product objective and authority boundary

WP-1 builds the smallest independently useful Protocol Orchestrator product. A user configures a target repository and can run, for example:

```text
sdp design --task "..."
sdp implementation
sdp review
sdp prompt verification --input VERIFICATION_SCOPE="..."
```

Core emits one complete, copy/paste-ready, stage-correct Protocol prompt. Mechanically knowable repository, candidate, workplan, Protocol-profile, and prompt-context inputs are resolved automatically. Genuinely user-owned inputs are required explicitly rather than left as editable placeholders.

Core-only installation is a finished operating mode. It requires no history database, agent process, benchmark service, account/model catalog, quota meter, predictor, or scheduler.

### 1.1 Product invariants

1. **Core works alone.** `sdp-orchestrator-core` plus `sdp` performs configuration, project/worktree observation, governing-workplan resolution, compatible workflow/profile resolution, prompt preparation, and final prompt rendering without higher modules.
2. **Observation is non-mutating.** Core never changes target worktree content, index, HEAD, branches, local refs, remote-tracking refs, or remote repository merely to inspect state. Explicit remote refresh uses a bounded read-only query, never fetch/pull.
3. **Prompt authority is singular.** Stage prose comes from the governing-version-compatible canonical SDP prompt source. Packaged prompt resources are reproducible version-bound derivatives, never an independently maintained prompt authority.
4. **Protocol binding is explicit.** Work governed by Protocol `X` is never silently interpreted through an incompatible profile. A semantic protocol version is never guessed to be a Git ref.
5. **Ambiguity remains explicit.** Project, workplan, Protocol source/profile, Git remote/target, stage selector, and required user-input ambiguity fail truthfully rather than using fuzzy names, mtime, path ordering, or undocumented heuristics.
6. **Prompt context is truthful.** Web mode never represents local-only dirty/unpushed state as remotely inspectable. Local mode may reference the local worktree. Both preserve candidate/profile/source provenance.
7. **Privacy guarantees are bounded and truthful.** Core never automatically injects private local paths into web prompts, credential-bearing remote userinfo, ambient environment values, credential-helper output, or private orchestrator state. Explicit user-authored task/input text is intentional prompt content and is not subject to an impossible arbitrary-secret detector.
8. **Core v1 is the durable lower seam.** Tracker/Adapter/Scheduler can consume accepted Core services without private imports, duplicated workplan/profile logic, or reverse dependency.
9. **One composition root.** Core owns `sdp`, the application/service registry, and the single extension entry-point group.
10. **Manual tracking compatibility exists from day one.** Every final prompt requests a terminal machine-readable `StageResultEnvelope v1` tied to RunId and prompt fingerprint; final render exposes a non-durable subscribed prompt event.
11. **Route-sensitive rendering is future-safe.** Core resolves route-independent stage/candidate/workplan/profile context before final rendering. Later Adapter/Scheduler can admit/select a route between preparation and rendering without duplicating Core authority.
12. **Resolved stage identity is profile-bound.** User/CLI stage input is an unresolved selector/key; `StageRef` is created only after the governing compatible workflow profile is known.
13. **Render consistency is optimistic and coherent.** Core does not lock repositories in WP-1, but it does not emit a prompt assembled from materially different candidate/workplan/local-source states. Material drift between preparation and final render fails/retries boundedly rather than producing a mixed snapshot.
14. **Determinism follows semantic state.** With fixed RunId and unchanged material preparation state plus prompt mode/input state, preparation/prompt identities do not drift because of wall-clock metadata or unrelated extension configuration.
15. **Installed behavior is the acceptance owner.** Helper tests cannot proxy-pass a broken wheel, packaged profile, extension-discovery surface, real Git observer, console entry point, stdout contract, or privacy/remote-truth boundary.
16. **Repository containment is mandatory.** Every orchestrator-owned executable source file, package/build metadata, test, fixture, package resource, developer script, and orchestrator documentation introduced by WP-1 lives under repository-relative `orchestrator/`. Repository-level workplans remain under the Protocol workplan convention, and existing repository CI/config may invoke `orchestrator/...`, but no orchestrator implementation logic is placed in top-level `source/`, `tests/`, `tools/`, `scripts/`, or another sibling tree merely for convenience.

### 1.2 Non-goals

WP-1 does not implement:

- SQLite or durable run/event/workflow history;
- `sdp status`, `next`, `ingest`, `history`, `graph`, persistent workplan selection, or lifecycle projection;
- Claude/Codex/OMP/Pi/Antigravity/ACP execution, sessions, approvals, cancellation, or worktree leases;
- Artificial Analysis, DeepSWE, model/backend/account catalogs, or capability ranking;
- quota/cost meters, resource ledgers, reservations, prediction, or AUTO routing;
- a daemon/resident watcher, generic workflow engine, ORM, or event-sourcing framework;
- repository-local orchestrator state;
- arbitrary plugin-directory scanning or repository-loaded executable plugins;
- automatic installation/upgrading of Protocol sources, extensions, agents, or providers;
- speculative compatibility profiles for unsupplied/untested Protocol versions;
- a competing CI authority or an orchestrator package under generated `dist/skills` unless later release policy explicitly requires one.

## 2. Governing authority and baseline

Parent authority:

```text
orchestrator/docs/architecture.md
architecture_version = 1.6.0
protocol_version = 5.16.0
```

This workplan inherits the parent module ladder, dependency direction, Core ownership, workflow-profile ownership, Protocol binding, privacy boundary, route-before-render invariant, repository-containment invariant, and standalone acceptance. Protocol 5.16 remains the generic lifecycle/testing/review authority. Canonical prompt source:

```text
source/shared/references/development-workflow-prompts.md
```

At workplan creation there is no executable Core implementation. The greenfield ratchet is therefore: one prompt authority, no higher-module machinery, minimum justified dependencies/public surface, executable dependency/namespace/layout guards, and rejection-capable ambiguity/version/privacy/identity tests.

## 3. Frozen WP-1 architecture

### 3.1 Distribution, repository containment, namespace, and version dimensions

Create one independently installable Python distribution `sdp-orchestrator-core`, console entry point `sdp`, and native PEP 420 namespace `sdp_orchestrator.core`. Core must not own `sdp_orchestrator/__init__.py`. Initial runtime floor is Python 3.11+.

All WP-1 implementation-owned repository files are contained under `orchestrator/`. A conforming layout may be, for example:

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
```

The exact subdirectory names beneath `orchestrator/` are delegated, but the containment boundary is Frozen. Shared repository-level CI/workflow files may contain only the minimal invocation/wiring needed to run orchestrator checks; reusable orchestrator logic, fixtures, package metadata, and test code remain under `orchestrator/`. Existing Protocol source under `source/`, ordinary repository workplans under `workplans/`, and generated/install artifacts outside the repository are inputs/integration surfaces, not orchestrator implementation placement.

Package release version, architecture version, Protocol version, config schema, API/SPI major, workflow-profile schema, result-envelope schema, event schema, and digest-canonicalization schemes are independent identities.

Expected runtime dependencies unless a smaller contract-equivalent set is demonstrated:

```text
platformdirs
typer
pydantic
python-frontmatter
packaging
```

Clipboard may be an optional `pyperclip`-class extra. No `filelock`, ACP, `httpx`, ORM/event-sourcing, ML, Tracker, Adapter, or Scheduler runtime dependency belongs in Core.

### 3.2 Configuration, project selection, and prompt mode

Core owns one TOML normalization/validation path. Default config location comes from `platformdirs`; API/CLI may explicitly override it. V1 has no semantic environment-variable override allowlist unless Implementation proves one necessary.

```toml
schema_version = 1

[core]
default_project = "mdstats"       # optional
default_prompt_mode = "web"        # optional; built-in default is web

[projects.mdstats]
repo = "/absolute/path/to/mdstats"
protocol_profile = "sdp-protocol-5.16"
default_prompt_mode = "web"        # optional
remote_name = "origin"             # optional Git remote name, never a credential URL

[protocol_sources."sdp-protocol-5.16"]
local_root = "/path/to/software-development-protocol"   # optional
allow_remote = false                                    # default
remote_repository = "https://github.com/hjin98/software-development-protocol"  # optional
remote_ref = "<explicit evidence-backed ref>"           # required when remote fallback enabled

[extensions."some.extension"]
# extension-owned bounded data; Core preserves but does not semantically interpret it
```

`default_prompt_mode` means **where/how the final prompt will be consumed** (`web` or `local`). It is intentionally not called `execution_mode`, because canonical SDP prompts already define an unrelated `EXECUTION_MODE` input meaning `AUTO_EXECUTE`, `REPORT_ONLY`, or an explicit delivery constraint.

Core-only prompt-mode precedence:

```text
explicit --prompt-mode
  -> project.default_prompt_mode
  -> core.default_prompt_mode
  -> built-in web
```

Core never silently falls from web to local. If web mode cannot truthfully represent the target, fail with a structured/actionable problem; user may choose local mode or make the candidate remotely available.

CLI project resolution when `--project` is absent:

```text
unique configured project whose canonical worktree contains cwd
  -> core.default_project
  -> sole configured project
  -> project.ambiguous / project.not_found
```

Public Core requests use explicit `ProjectKey`; cwd/default convenience is CLI-only.

Unknown absent-extension namespaces are preserved as bounded raw configuration and diagnosed as inactive. Only an activated extension validates its namespace. Unrelated extension configuration does not participate in Core preparation/prompt identity.

Secrets/tokens are not ordinary Core config values. Explicit remote authentication may use established Git/platform credential mechanisms without serializing credential values into config snapshots, diagnostics, prompt/event metadata, or digests.

### 3.3 Read-only repository/candidate/worktree observation

`ObservationPolicy` supports `local_only`, `use_cached_remote`, and `refresh_remote`. Default is `local_only`.

- `use_cached_remote` reads existing local upstream/remote-tracking evidence without changing it.
- `refresh_remote` performs a bounded noninteractive read-only query such as `git ls-remote`/equivalent; it never mutates target refs/worktree/index.
- Git/network runtime/output are bounded and credential-bearing diagnostics are redacted.
- Repository files/build hooks are never executed merely to inspect state.

`CandidateRef` identifies repository, branch/detached state, HEAD, materially relevant staged/unstaged/untracked content, upstream/selected remote observation when known, provenance/freshness, and identity completeness. `sdp.git-working-tree.v1` changes when materially different dirty content exists at the same paths. If safe bounded fingerprinting is incomplete, `identity_complete=false`.

`WorktreeKey` identifies a physical Git worktree: aliases/symlinks to one checkout map to one key; linked worktrees map to different keys.

### 3.4 Remote selection and web-addressability

Remote selection:

```text
projects.<key>.remote_name when configured and valid
  -> current branch upstream remote when uniquely defined
  -> remote named origin
  -> sole Git remote
  -> remote.ambiguous / remote.unavailable
```

Core records remote name plus sanitized repository identity and strips credential/userinfo material. Filesystem and `file://` remotes are local-only and invalid web targets.

For a normal branch, web target is the known upstream branch when present; otherwise same branch name on selected remote is usable only when remote existence is established by cached tracking evidence or explicit refresh. **Target existence/addressability must be known; only freshness may be cached/unknown.** Detached-HEAD web rendering is unavailable unless an explicit remote target is established without guessing.

Dirty local state blocks web mode. Known local/remote commit divergence blocks web mode. Cached evidence is labeled truthfully. Web context includes repository + target ref + exact intended candidate commit when safely available.

### 3.5 Workplan catalog, stage-specific resolution, and identity

Core catalogs bounded repository-owned regular Markdown/text workplans under `workplans/active/` and `workplans/archive/`, including nested current `AUTHORITY.md` and frontmatter-marked implementation plans. Resolved paths remain inside repository root; symlink/traversal escapes/special files are rejected or ignored safely. Parsing is bounded and data-only; no arbitrary object construction/repository code execution.

Documents sharing `workplan_id` are deduplicated only through explicit current-authority evidence. Historical numbered revisions are not independent active plans when a current authority clearly owns them. If ownership cannot be determined without guessing, return ambiguity.

Explicit selector is exact workplan ID or exact repository-relative canonical path. For stages with normal governing-plan resolution:

```text
explicit selector
  -> unique recognized current-branch binding (v1 metadata: target_branch)
  -> exactly one active workplan
  -> required/ambiguous failure
```

No fuzzy filename/recency selection.

5.16 stage policy:

| Stage | Workplan policy |
| --- | --- |
| baseline | optional explicit authority only; no implicit active-plan capture |
| design | optional explicit existing-plan target; `--task` always required; without `--workplan` this is new-task Design and does not silently adopt a sole active plan |
| implementation | governing workplan required; normal resolver |
| review | governing workplan required; normal resolver |
| verification | optional explicit governing authority; no implicit active-plan capture |
| stabilization | optional explicit governing authority; no implicit active-plan capture |
| alignment | exact downstream workplan required |
| health-audit | no workplan selection; `--workplan` rejected |
| closeout | optional exact completed-workplan binding; otherwise `COMPLETED_WORK` required |

Stage-disallowed `--workplan` fails rather than being ignored.

A selected governing workplan whose required `protocol_version` is absent/invalid/unsupported is not silently assigned the project default profile; governing Implementation/Review/Alignment fails as incompatible/unavailable. An optional explicit authority with incomplete protocol metadata may be represented as evidence only when the selected stage does not require it to determine its governing Protocol contract.

`WorkplanRef` carries artifact digest, semantic digest when safe, semantic-identity completeness, path, protocol version, ID, and lifecycle state/consistency. `sdp.workplan-semantic.v1` uses a finite tested lifecycle-only exclusion list. Unknown semantics are conservative; body/Frozen-authority changes change semantic identity. Exact canonicalization is frozen by Review fixtures.

### 3.6 Protocol profile, Core render source, and packaged snapshot

V1 supports one explicitly compatible Protocol 5.16 profile unless later accepted evidence adds another.

```text
explicit configured compatible local source/profile
  -> exact compatible packaged profile/prompt snapshot
  -> explicitly permitted canonical remote source at explicit ref
  -> protocol.incompatible / protocol.unavailable
```

The **Core render source** and canonical prompt `PROTOCOL_SOURCE` are different:

- `PromptSourceRef` records exact source/snapshot Core used to obtain canonical prompt/profile material.
- Canonical `PROTOCOL_SOURCE` tells the receiving agent how to resolve SDP skills; v1 default is `AUTO_LOCAL_FIRST` unless explicitly overridden through a declared input.
- Canonical `PROTOCOL_REF` is mechanically bound to the governing workplan/profile Protocol contract, never copied from a local render-source path.

A local Core `local_root` therefore never leaks into web prompt `PROTOCOL_SOURCE` merely because Core rendered from it.

Remote Protocol source is opt-in. A requested branch/tag/ref is resolved once to an immutable commit/content identity before multi-file use; all source/profile files for one preparation come from that identity. Record requested ref plus resolved identity/digests. Reads are bounded, authenticated transport preferred, data-only, and never execute downloaded/repository code. Incoherent multi-file read fails.

Canonical stage prose is the literal fenced `text` block belonging to the uniquely identified canonical stage heading. Structural ambiguity fails. Packaged prompt/profile resources are reproducibly derived from actual canonical source. Machine-readable profile contains only bounded control metadata: stage keys/aliases, role/mutation/optionality, recognized outcome/routing classes, allowed transitions, workplan policy, input bindings/default classes, compatibility/source identity, and result-schema identity. It does not duplicate prompt prose or become a generic workflow DSL.

Profile fixtures encode only routing facts justified by supplied 5.16 authority. Optional/context-dependent follow-ups remain alternatives/ambiguous rather than invented deterministic edges.

### 3.7 Stage input ownership — prompt mode is not canonical `EXECUTION_MODE`

Every canonical INPUT is `mechanical`, `canonical_default`, or `required_user`.

Common bindings:

| Canonical input | V1 ownership |
| --- | --- |
| `REPOSITORY_TARGET` / stage-equivalent target | mode-dependent mechanical value produced during final render from prepared candidate + prompt mode |
| `PROTOCOL_SOURCE` | default `AUTO_LOCAL_FIRST`; explicit declared override allowed subject to prompt-mode validation |
| `PROTOCOL_REF` | mechanical governing Protocol contract; conflicting generic override rejected |
| `EXECUTION_MODE` | canonical default `AUTO_EXECUTE`; explicit declared override such as `REPORT_ONLY` allowed; **never** local/web prompt mode |
| `ADDITIONAL_CONSTRAINTS` | canonical default `NONE`; explicit declared override allowed |

Required user inputs:

| Stage | Required user input | Binding |
| --- | --- | --- |
| baseline | `BASELINE_SCOPE` | `--input BASELINE_SCOPE=...` |
| design | `TASK` | `--task` |
| implementation | none beyond governing plan | resolver |
| review | none beyond governing plan | resolver |
| verification | `VERIFICATION_SCOPE` | `--input` |
| stabilization | `STABILIZATION_SCOPE` | `--input` |
| alignment | `UPSTREAM_ACCEPTED_WORK` + exact downstream plan | `--input` + `--workplan` |
| health-audit | `AUDIT_SCOPE` | `--input` |
| closeout | `COMPLETED_WORK` unless exact selected plan supplies it | `--input` or `--workplan` |

Other fields stay mechanical or canonical `AUTO`/`NONE` according to profile, including authority discovery, history window, exclusions, affected-documentation discovery, and implementation-target fields where canonical prompt explicitly permits AUTO. Core may fill an exact safe target mechanically but may not invent semantic authorities.

`input_overrides` accepts only declared INPUT names not exclusively owned by first-class/mechanical fields. Unknown -> `prompt.input_unknown`; missing required -> `prompt.input_required`; first-class/mechanical conflict -> `prompt.input_conflict`; structurally invalid/mode-incompatible -> `prompt.input_invalid`.

Concrete inserted values use one deterministic structure-safe single-line representation; raw NUL/CR/LF/control injection is not spliced into INPUT grammar. Exact reversible v1 encoding is frozen in fixtures. Canonical sentinels remain canonical.

### 3.8 Two-phase prompt API, preparation identity, and coherent snapshot

Core separates route-independent preparation from route-sensitive final rendering:

```text
Core-only CLI:
  prepare -> configured/explicit prompt mode -> render

Later Adapter/Scheduler:
  prepare
    -> admission using prepared stage/candidate/workplan/profile identity
    -> render using admitted route.prompt_execution_mode
    -> Adapter.start
```

Preparation resolves StageSelector under compatible profile, observes candidate, applies stage workplan policy, resolves workflow/profile and canonical source identity, validates user-input completeness, and returns `PreparedPrompt`. It emits no final prompt/prompt event and requires no local/web mode.

`PreparedPrompt.preparation_fingerprint` is `DigestRef` under versioned canonicalization `sdp.prompt-preparation.v1`, SHA-256 over canonical JSON of the mode-independent semantic preparation identity: RunId, ProjectKey/WorktreeKey, resolved StageRef, candidate identity, selected workplan identity/selection basis, Protocol/workflow profile identity, PromptSourceRef identity, classified resolved input values/provenance that are mode-independent, result-schema identity, and other material request policy. Volatile timestamps, diagnostics, and unrelated extension config are excluded. Exact field order/serialization is frozen by fixtures before Review.

Final render accepts PreparedPrompt plus `PromptExecutionMode(local|web)`, derives mode-safe target/context, substitutes inputs, appends footer, and emits prompt event only after successful full artifact construction.

Immediately before final return, Core revalidates material local candidate, selected workplan artifact/semantic/path/lifecycle identity as relevant to rendered context, and mutable explicit local Protocol-source identity. Material drift -> `core.context.stale` or bounded transparent Core-only retry; never mixed snapshot. No lock/persistence is introduced.

### 3.9 Prompt artifact, result-footer wire, fingerprint, privacy, and stdout

Web mode excludes automatically derived local repo/config/state paths, local/file remotes, ambient environment values, credential-helper output, and credential-bearing remote userinfo. Local mode may include authorized repo/worktree paths but never automatically sourced credentials/unrelated environment data. Explicit user task/input text is intentionally rendered and not arbitrary-secret scanned.

Canonical stage body is preserved except declared INPUT substitution. Core appends only architecture-approved orchestration metadata/result request and never weakens/reinterprets stage instructions or requests hidden chain-of-thought.

The result request must be unambiguously machine-locatable for future Tracker without suppressing normal human-readable output. V1 requires ordinary agent response followed by exactly one **terminal uniquely marked JSON result footer** representing `StageResultEnvelope v1`. The footer marker, JSON object schema, required identity fields (`schema_version`, RunId, prompt fingerprint, resolved stage), additive-field policy, and terminal-block extraction rule are frozen in WP-1 executable fixtures before Review. Surrounding prose is allowed; hidden reasoning is not requested. Core requests this footer but does not parse/persist it in WP-1.

`sdp.prompt-fingerprint.v1`:

1. use caller RunId or allocate one;
2. render exact full artifact with fixed fingerprint placeholder;
3. SHA-256 hash frozen normalized UTF-8 placeholder-form bytes;
4. substitute `sha256:<hex>`;
5. freeze placeholder, line endings, terminal newline, input scalar normalization, and result-footer request bytes in fixtures.

Volatile timestamps stay structured provenance unless canonical prompt requires them. Final prompt is constructed fully before stdout; any primary failure emits no partial prompt bytes. Prompt commands write prompt only to stdout; diagnostics use redacted stderr/nonzero exit. Optional `--copy` is additive.

### 3.10 Extension composition, passive discovery, and subscribed events

Core discovers extension entry points only through `sdp_orchestrator.extensions.v1`. Installed extension code is trusted in-process code, not a sandbox.

Normal activation imports/loads eligible providers, obtains side-effect-minimal `manifest()`, resolves capability/API dependencies topologically, and calls `activate()`. Failed/incompatible optional extensions disable themselves/dependents without breaking healthy Core. Cycles/missing requirements are deterministic. Singular service cannot silently replace another; multi-provider order is stable by provider ID. `ExtensionContext` exposes only versioned required services, the extension's own config namespace, and bounded registrars.

`ApplicationRequest.activation_policy` supports at least:

```text
normal
discovery_only
```

**Discovery-only does not import or execute third-party extension provider code.** It reads installed distribution/entry-point metadata only and reports higher extensions as discovered/not-loaded unless equivalent declarative metadata is safely available. Therefore it does not claim provider capabilities/health that were not loaded/probed. `sdp doctor` and `sdp capabilities` use discovery-only by default, preserving their no-hidden-mutation/network guarantee. Normal composition is the path that loads providers and validates manifests/dependency graph.

Event sinks register explicit event-type subscriptions during normal activation. `core.prompt.rendered.v1` contains complete prompt text and is delivered only to explicitly subscribed sinks. Logical EventId is stable for event type + RunId + prompt fingerprint. Delivery is synchronous/non-durable/duplicate-tolerant. Core does not sandbox/time-limit arbitrary trusted in-process sink code; first-party sinks must keep handling bounded. Sink failure is diagnosed but does not invalidate an otherwise successful primary render.

### 3.11 Bounded input/network trust

Core-controlled readers apply finite byte/count/nesting/time/output bounds where malformed/external input could exhaust resources: config, opaque extension config, workplan/frontmatter discovery, canonical/local/remote prompt/profile source, Git subprocess/remote query output, and remote Protocol reads. Exact numeric limits are delegated but documented/tested at boundaries and reject before unbounded materialization.

Remote/downloaded Protocol material is data until schema/version/source validation completes and is never fed to executable loaders/build hooks. Credential-bearing errors/URLs and `Problem.details` are redacted before user-facing serialization.

## 4. Public Core API/SPI v1

### 4.1 Public-record rule and identities

Anything reachable from `sdp_orchestrator.core.api.v1` or `.spi.v1` is a public v1 record/service or standard immutable scalar/container. Pydantic is initial technology, not semantic authority. Records are JSON-compatible immutable-by-convention; IDs opaque strings; timestamps UTC ISO-8601; digests carry algorithm + versioned canonicalization + value; unbounded collections use `Page[T]` with opaque query-scoped cursors.

`StageSelector` is profile-neutral input (key/alias). `StageRef` is resolved profile-bound identity and is never fabricated before compatible profile resolution.

Public types include at least:

```text
ProjectKey, WorktreeKey, RunId, EventId, StageSelector, StageRef, CapabilityKey, ExtensionId
PromptExecutionMode
DigestRef, ProtocolProfileRef, PromptSourceRef, WorkplanRef, CandidateRef, RemoteRepositoryRef
ProjectDescriptor, PromptProjectSnapshot
WorkflowProfileDescriptor, StageDescriptor, StageTransitionDescriptor
BlockerRecord, StageResultEnvelope, EventEnvelope
ProjectQuery, ProjectObservationRequest, ProjectObservation, ObservationPolicy
WorkplanQuery, WorkplanDescriptor, WorkplanResolutionRequest, WorkplanResolution
WorkflowRequest
PromptPreparationRequest, PreparedPrompt, PromptRenderRequest, RenderedPrompt, ResolvedInput
CapabilityRequirement, CapabilityProvision, CapabilityStatus
ApplicationRequest, ExtensionManifest, ExtensionContext, ExtensionRegistration, EventSubscription
Problem, Page[T]
```

No public signature leaks Git/subprocess/file/lock/DB/event-loop/private implementation objects. Independent WP-1 Review freezes accepted v1 wire/schema fixtures as compatibility floor for WP-2+.

### 4.2 CoreAPI v1

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

All are read-only with respect to target repositories. `allocate_run_id()` creates identity only. `resolve_workplan()` is the public owner of stage-specific selection; higher modules do not reproduce it. `WorkflowRequest` resolves from explicit ProtocolProfileRef or WorkplanRef/project context, with selected governing-workplan binding taking precedence. `list_stages()` is a convenience view of the same descriptor.

`PromptPreparationRequest` carries optional RunId, ProjectKey, StageSelector, optional exact workplan selector, Design `first_task`, declared input overrides, and ObservationPolicy; no local/web prompt mode.

`PreparedPrompt` carries RunId, `sdp.prompt-preparation.v1` fingerprint, resolved StageRef, ProjectObservation/CandidateRef, selected WorkplanResolution, WorkflowProfileDescriptor/ProtocolProfileRef, PromptSourceRef, classified/resolved mode-independent inputs with provenance, and result-schema identity.

`PromptRenderRequest` carries PreparedPrompt + `prompt_execution_mode: PromptExecutionMode(local|web)`. Render revalidates consistency before returning artifact.

These additive read-only methods refine the parent-owned Core method family to satisfy the already-Frozen route-admission-before-render and lower-module-no-duplication invariants; they introduce no higher-module behavior.

### 4.3 Application API v1

```python
class ApplicationAPI(Protocol):
    def capabilities(self) -> tuple[CapabilityStatus, ...]: ...
    def has(self, requirement: CapabilityRequirement) -> bool: ...
    def service(self, requirement: CapabilityRequirement) -> object: ...
    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]: ...
    def core(self) -> CoreAPI: ...


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI: ...
```

Core provisions `prompt.render`, `project.observe`, `workplan.catalog`, `workflow.profile`. Capability key is semantic/unversioned; API compatibility is separate. Discovery-only status distinguishes discovered/not-loaded from active/healthy.

### 4.4 Extension/event SPI v1

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Normal mode imports/loads provider code and uses this SPI. Discovery-only stays at package metadata and does not claim unobserved manifest/capability health. Event sinks subscribe explicitly; no durable queue belongs in Core.

### 4.5 Workflow-profile conservatism

Packaged 5.16 descriptor enumerates finite stage set and only authority-backed recognized outcomes/trigger classes/allowed transitions. A relationship left optional/context-dependent by supplied Protocol is represented as optional alternatives or insufficient-to-force-next-stage, never collapsed into an invented deterministic edge.

### 4.6 Error contract

Python APIs raise one `OrchestratorError(Problem)`; callers branch on code. `Problem.message/details` are redacted/JSON-safe. Establish at least:

```text
core.config.invalid
core.project.not_found
core.project.ambiguous
core.repository.invalid
core.context.stale
core.workplan.required
core.workplan.not_found
core.workplan.ambiguous
core.workplan.disallowed
core.protocol.incompatible
core.protocol.unavailable
core.protocol.source_incoherent
core.stage.unknown
core.remote.unavailable
core.remote.ambiguous
core.remote.local_only
core.remote.stale
core.remote.target_unavailable
core.prompt.mode_invalid
core.prompt.input_required
core.prompt.input_unknown
core.prompt.input_conflict
core.prompt.input_invalid
core.extension.incompatible
core.extension.activation_failed
core.extension.dependency_cycle
core.clipboard.unavailable
```

No exception subclass hierarchy mirroring codes.

### 4.7 CLI mapping

```text
--project <ProjectKey>
--workplan <exact workplan_id-or-relative-path>
--prompt-mode local|web
--config <path>
--remote-mode local_only|use_cached_remote|refresh_remote
--task <text>                  # Design only
--input NAME=VALUE             # repeatable profile-declared input
--copy
```

`--prompt-mode` controls local/web context only. Canonical `EXECUTION_MODE` is a separate declared prompt input; e.g. `--input EXECUTION_MODE=REPORT_ONLY` changes stage action semantics without changing prompt mode.

`--task` outside Design fails. Stage-disallowed `--workplan` fails. Missing/unknown/conflicting/invalid input fails before prompt bytes. API/CLI use one normalization owner.

Canonical commands:

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

Aliases resolve through compatible profile, not duplicate hard-coded semantics.

## 5. Implementation obligations and acceptance

### O1 — Build/install/package/layout boundary

Build Core distribution/entry point/PEP 420 namespace/packaged 5.16 resources with justified dependencies. Acceptance: wheel/sdist build, independent artifact inspection, install outside source checkout, installed CLI smoke, sibling namespace coexistence fixture, no root namespace `__init__.py`, no production higher-module imports, and a structural layout check proving all orchestrator-owned source/package/test/fixture/script/doc files introduced by WP-1 are under `orchestrator/` except repository-level workplan authority and minimal pre-existing CI invocation wiring.

### O2 — Config/project/composition normalization

Acceptance: explicit/cwd/default/sole/ambiguous project; built-in web prompt-mode default and precedence; no silent web->local fallback; malformed/oversized config; empty env allowlist; absent-extension config preservation; active extension namespace handoff; unrelated extension config not changing identities; unsupported secret-bearing Core config rejected/redacted; local Protocol-source override; remote source disabled by default.

### O3 — Real Git/worktree/remote observation

Acceptance owner is production observer against real temporary Git repos/worktrees/remotes. Cover branch/detached HEAD, dirty content identity, alias vs linked worktree, upstream known/unknown, remote precedence/ambiguity, local/file remote web rejection, sanitized HTTPS/SSH, cached existence/freshness, bounded noninteractive refresh, incomplete identity; prove no worktree/index/HEAD/local/remote-tracking-ref mutation.

### O4 — Workplan catalog/resolution/stage policy

Cover top-level/nested/archive, exact ID/path, target_branch, duplicate/multiple ambiguity, malformed/oversized/path escape, lifecycle consistency, semantic identity, missing/invalid protocol_version, and every stage policy in §3.5. Counterfactual: new-task Design with an unrelated sole active workplan must not auto-bind it.

### O5 — Protocol source/profile/snapshot/workflow

Acceptance: every canonical stage body uniquely extracted from actual source; source/package parity; profile metadata reconciled with supplied 5.16 authority; offline installed-wheel rendering; compatible local source; remote fallback off by default; remote requested ref resolved once to immutable identity; oversized/incoherent/changed source fails; older/unknown workplan never silently 5.16; optional workflow routing not invented deterministic.

### O6 — Public API completeness and pre-render seam

Acceptance:

- StageSelector resolves to profile-bound StageRef only after compatible profile resolution;
- resolve_workplan is sole selection owner and exposes selection evidence;
- workflow follows governing WorkplanRef protocol rather than project default;
- Core-only `prepare -> render` works;
- Adapter-shaped `prepare -> external no-op admission fixture -> render` works with no provisional prompt/event;
- `sdp.prompt-preparation.v1` has fixed canonicalization fixtures, stable under irrelevant timestamp/extension changes and sensitive to all material preparation changes;
- PreparedPrompt JSON round-trips;
- candidate/workplan/local-source mutation between phases -> context.stale, no prompt event/partial output;
- render may select local/web from same valid preparation subject to mode feasibility;
- no private objects cross v1 surfaces.

### O7 — Canonical input binding/naming separation

Exercise all canonical stages/INPUT lines. Prove classification and required-user table; `--prompt-mode web` leaves canonical `EXECUTION_MODE=AUTO_EXECUTE`; `--input EXECUTION_MODE=REPORT_ONLY` does not alter prompt mode; local render-source path never becomes web `PROTOCOL_SOURCE`; `PROTOCOL_REF` follows governing contract; missing/unknown/conflicting/structurally invalid input fails atomically; structure-safe scalar encoding protects INPUT grammar; no unresolved required placeholder in successful prompt.

### O8 — Renderer/fingerprints/result footer/event

Acceptance: correct fenced body for every stage; declared INPUT substitution only; separate footer; fixed RunId + same semantic state gives byte-identical prompt/fingerprint; material state changes identity; preparation/prompt fingerprint fixtures; terminal uniquely marked JSON `StageResultEnvelope v1` request fixture is unambiguously extractable from surrounding ordinary prose and includes matching RunId/prompt fingerprint/resolved stage; additive fields tolerated per schema; no hidden reasoning request; successful final render alone emits subscribed event; unsubscribed sink no prompt; duplicate EventId tolerated; sink failure does not invalidate primary render.

### O9 — Web/local privacy and remote truthfulness

Acceptance boundary final RenderedPrompt/stdout. Fixtures: distinctive local paths, credential URL, SSH, local/file remote, multiple remotes, dirty state, local-ahead/remote-ahead, cached stale, absent remote target, ambient secret-like environment. Web requires known target existence, blocks dirty/known divergence, labels cached freshness, and automatically leaks none of prohibited values. Explicit user text is expected content, not arbitrary-secret test.

### O10 — Extension discovery/diagnostics

Acceptance through real installed entry-point metadata. Discovery-only does not import/call fixture provider code and reports discovered/not-loaded state. Normal mode imports provider and covers compatible/incompatible/missing-dependency/cycle, duplicate singular/stable multi-provider behavior, explicit prompt-event subscription, optional-provider failure degradation. `doctor`/`capabilities` stay no-hidden-network/no-hidden-mutation by default.

### O11 — CLI product boundary

Installed `sdp` subprocess, not direct callbacks. Every alias and `sdp prompt <stage>` uses same prepare/render path. Stdout atomic/prompt-only; errors redacted stderr/nonzero. Optional copy additive. Doctor reports Core readiness without hidden load/network/mutation.

### O12 — Documentation, CI, and final simplicity

Document install/config/project/remote/prompt mode, prompt-mode vs canonical EXECUTION_MODE, Core render source vs agent PROTOCOL_SOURCE, required inputs/workplan policies, local/web visibility, result-footer contract, piping/copying, extension trust/discovery/subscriptions, bounded secret guarantee, repository-containment rule, and higher-feature absence.

Integrate Core acceptance into ordinary repository validation; do not create a competing CI authority. Preserve:

```text
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

Core package/test/install acceptance is additional and lives under `orchestrator/`; existing repository-level validation/CI may invoke those checks using minimal wiring but must not host orchestrator implementation logic outside the containment boundary. Before handoff reconcile every obligation, re-derive affected surface, run final Core regression/real-owner integration/repository checks, and remove speculative persistence/transport/resource/benchmark hooks, duplicate authorities, or misplaced orchestrator files.

## 6. Real semantic-owner acceptance boundaries

1. Installed `sdp` -> production composition -> prepare/observer/workplan/profile owner -> final renderer -> stdout.
2. Production `prepare()` record is sufficient for external admission; final `render()` consumes same preparation with no provisional prompt side effect.
3. Production observer/revalidation against real temporary Git worktrees/remotes.
4. Actual canonical source -> extraction/generation -> packaged wheel -> installed renderer.
5. Built wheel outside checkout + sibling PEP 420 fixture.
6. Real entry-point discovery in both metadata-only and normal-load modes.
7. Final rendered prompt/stdout for privacy/remote truth.
8. Successful final render -> explicitly subscribed event sink.
9. Repository layout structural check over the final candidate proves the orchestrator implementation surface is contained under `orchestrator/`.
10. Ordinary repository CI actually invokes Core acceptance and retains Protocol checks.

Doubles are valid only below/outside the owner under claim; evidence that stays green with a broken owner cannot close it.

## 7. Implementation sequence

### Stage 1 — Package/contracts/config/Git/workplans

Package skeleton under `orchestrator/`, public records/composition, config/project/prompt-mode normalization, Git/worktree/remote observation, workplan catalog/resolution/stage policy.

Closure: focused contract/config/Git/workplan/path/remote/layout tests + affected regression; no persistence/higher import.

### Stage 2 — Protocol profile + preparation

Canonical source/profile/snapshot, StageSelector -> StageRef, WorkflowProfileDescriptor, workplan-governing workflow resolution, input classification, prepare/preparation fingerprint/consistency identity.

Closure: canonical/profile parity, all-stage workplan/input policy, source/version/incoherence rejection, preparation/fingerprint/stale-context tests + affected regression.

### Stage 3 — Final renderer/composition/CLI/package closure

Mode-sensitive render, privacy/remote target, result-footer/prompt fingerprint/event, real extension discovery/passive diagnostics, CLI/clipboard, docs, package build/install/CI, architecture-fitness/layout checks, final reconciliation/regression/integration/simplification.

Closure: installed-wheel end-to-end acceptance on representative temporary repositories + ordinary repository validation; ready for independent Review.

## 8. Frozen versus delegated

### Frozen for WP-1

- parent architecture 1.6 module/dependency/ownership direction;
- all orchestrator implementation-owned repository files contained under `orchestrator/`, with only minimal repository-level CI invocation wiring and Protocol-standard workplan authority outside it;
- Core standalone distribution/CLI/composition and capabilities;
- Python 3.11+ and PEP 420;
- public Core API/Application/Extension SPI semantic families including `resolve_workplan`, profile-aware `workflow`, route-independent `prepare`, and final `render` required by parent invariants;
- StageSelector vs StageRef;
- PromptExecutionMode(local|web) and separation from canonical EXECUTION_MODE;
- built-in web prompt default/no silent local fallback;
- deterministic project/remote/workplan selection and stage policies;
- non-mutating observation + optimistic preparation revalidation;
- Protocol-version/source/snapshot coherence;
- render-source vs agent PROTOCOL_SOURCE and governing PROTOCOL_REF;
- canonical input classification/required-user policy;
- bounded privacy/addressability/secret guarantee;
- RunId + `sdp.prompt-preparation.v1` + prompt fingerprint + machine-readable result-footer contract class;
- one extension registry, metadata-only discovery policy, normal trusted-code activation, explicit event subscriptions;
- no higher-module implementation.

### Delegated until WP-1 Review freezes fixtures

- private decomposition/build backend/test runner/package release number;
- exact subdirectory naming beneath the Frozen `orchestrator/` containment root;
- concrete Git/network plumbing satisfying semantics;
- finite numeric parser/read/download limits;
- lifecycle-only semantic-digest exclusion list;
- exact safe scalar encoding, preparation canonical JSON field ordering, prompt fingerprint placeholder bytes, and literal terminal result-footer marker/schema field spelling consistent with the Frozen contract;
- exact public field spelling not explicitly fixed above/additive optional fields;
- diagnostics/numeric exit mapping/clipboard;
- simpler focused dependency substitutions.

### Design reopen triggers

Reopen only affected surface if evidence shows Core prepare/render/resolve still cannot support Tracker/Adapter without private/reverse dependency; required workflow facts need a different owner/model; canonical prompt cannot package offline without competing authority; target workplan conventions systematically defeat exact resolution; one extension registry/subscription seam cannot compose later modules; non-mutating observation/revalidation cannot establish coherent identity; web/local privacy/addressability cannot be preserved; the `orchestrator/` repository-containment boundary conflicts with an independently required packaging/release mechanism that cannot be expressed by thin invocation wiring; or Python 3.11+ violates a required distribution target.

## 9. Simplification triggers

Simplify before durable addition if implementation starts creating a second prompt-body authority; separate local/web renderers instead of one context policy; separate CLI/API config logic; multiple plugin loaders; generic workflow DSL; persistence/event queue in Core; agent/model/account/resource placeholders; fuzzy workplan/remote heuristics; generic secret scanner guarantees; repository-mutating observation; generic input overriding first-class identity; provisional prompt rendering for admission; duplicated workplan/profile resolution outside Core; orchestrator implementation/test/build logic outside `orchestrator/`; or a competing CI workflow without real isolation need.

## 10. Final closure review — 2026-09-07

Closure re-read the remote Protocol 5.16 `software-design` role and workflow/workplan, testing/proxy-proof, architecture/simplicity, versioning, long-horizon, Python, configuration, security, specification, release, repository, and canonical workflow-prompt authorities, then falsified WP-1 as the compatibility floor for WP-2 through WP-4.

Repeated review closed: complete stage input ownership; exact/path-safe/stage-specific workplan resolution; deterministic non-mutating Git/remote identity; truthful web/privacy/secret boundaries; conservative candidate/workplan/source identity and stale-snapshot rejection; canonical prompt/remote Protocol source coherence; absent-extension config; one registry/subscribed event seam; installed namespace/entry-point acceptance; prompt-mode versus canonical EXECUTION_MODE separation; render-source versus agent PROTOCOL_SOURCE separation; profile-neutral StageSelector; public workplan/profile resolution; route-independent prepare/final render; versioned preparation identity; passive package-metadata-only diagnostics; an unambiguous terminal machine-readable result-footer contract; and repository containment of all orchestrator implementation-owned files.

The parent architecture was reconciled at 1.6.0 so these Core seams and the `orchestrator/` repository boundary are Tier-1B authority rather than workplan-only refinements.

A final counterexample pass after those corrections finds no significant unresolved Design gap. Remaining choices are Tier-2 realization details or explicitly deferred higher-module concerns.

Snapshot-loss counterfactual: parent architecture + this workplan + supplied Protocol 5.16 source/reference tree recover every still-binding WP-1 invariant, Frozen decision, API/SPI role, stage/workplan/input policy, repository-layout rule, non-goal, acceptance boundary, and reopen trigger without chat or Git review history.

**Design verdict: PASS — WP-1 Prompt Module + Core Program is closure-complete and ready for `software-implementation`.**
