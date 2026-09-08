---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: reopened
reviewed_date: 2026-09-07
reviewed_candidate: 5e6fd725213ccfdd211f79425d0aef33e03eaeaa
review_verdict: no-pass
reopened_date: 2026-09-07
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

## 11. Independent implementation review — 2026-09-07

**Implementation review verdict: NO-PASS — WP-1 is reopened for bounded implementation repair.**

Reviewed candidate: `5e6fd725213ccfdd211f79425d0aef33e03eaeaa` on `plan/protocol-orchestrator`.

The parent architecture remains valid at 1.6.0. These findings are implementation nonconformance under the already-accepted Core architecture, not evidence for a new subsystem or a parent-architecture redesign. Repair the existing semantic owners in place. Prefer alteration/removal/consolidation; do not add a second observer, second registry, wrapper service, persistence layer, or compatibility shim.

### R1 — Make candidate identity include the staged/index state it claims to identify

**Blocking authority:** product invariants 13-15; §§3.3, 3.8; O3/O6.

The current dirty-worktree fingerprint hashes status/path plus working-tree file content, but does not bind the staged/index blob content. Two candidates can therefore have identical `sdp.git-working-tree.v1` identity while the staged patch differs, with `identity_complete=true`; the same omission lets index drift evade render revalidation.

Repair the existing Git candidate-identity path so materially relevant staged state and working-tree/untracked state are both represented under the one existing candidate identity. Do not introduce a second candidate record or parallel observer. If any relevant index/content state cannot be bounded safely, mark the identity incomplete rather than claiming completeness.

Required counterexample: hold path/status and working-tree bytes constant, change only the staged blob, and prove the candidate digest changes; prepare a prompt, mutate only that staged blob, and prove final render rejects the stale preparation with no prompt event.

### R2 — Bind remote evidence to the selected remote and preserve remote ambiguity as a public semantic result

**Blocking authority:** product invariants 5-6, 13-14; §3.4; §4.6; O3/O9.

Remote selection and target observation are currently separable in a way that can select one remote while consuming another remote's upstream/tracking evidence. A configured `fork` can therefore inherit `origin/main` evidence and render a fork URL even when the target was never established on fork. Conversely, same-branch cached evidence on the actually selected remote is not consistently used when there is no matching upstream. In addition, an ambiguous remote selection is collapsed into `core.remote.unavailable` at the web-render boundary even though `core.remote.ambiguous` is a Frozen caller-visible code.

Rewire the existing observation flow so one coherent tuple owns `selected remote + target branch/ref + evidence provenance + observed commit`. Upstream evidence is valid only when its remote is the selected remote; otherwise use the selected remote's same-branch cached tracking ref or a bounded refresh for that selected target. Never render another remote's `origin/main`-style name as a branch of the selected repository. Preserve `core.remote.ambiguous` rather than recoding it as unavailable when ambiguity is the observed cause.

Required real-Git counterexamples: branch tracks `origin/main`, configured remote is `fork`, fork branch absent -> web render fails target-unavailable/ambiguity truthfully; fork/main cached at the candidate commit -> web target is fork/main (branch `main`) with cached provenance; multiple unresolvable remotes -> caller-visible `core.remote.ambiguous`.

### R3 — Enforce exact canonical workplan paths instead of normalizing traversal aliases into valid selectors

**Blocking authority:** product invariant 5; §3.5; O4.

The current selector normalizer can collapse leading/interior `..` components and make a non-canonical traversal-like input such as `../workplans/active/A.md` resolve to the real in-repository plan. That is not an exact repository-relative canonical selector.

Alter the existing exact-path lookup so an explicit path must already be canonical, relative, traversal-free, and under a recognized workplan root before it can match. Do not add fuzzy recovery or a second path-resolution mode. Exact `workplan_id` lookup remains separate.

Required counterexamples: canonical path succeeds; absolute path, leading/interior `.` or `..` aliases, backslash aliases that are not the canonical repository spelling, and traversal strings that normalize onto an existing plan all fail rather than selecting it.

### R4 — Make `PreparedPrompt` admission identity enforceable and make final render one coherent optimistic snapshot

**Blocking authority:** product invariants 8, 11, 13-14; §§3.6, 3.8; O5/O6/O8.

Two gaps must close in the existing prepare/render owner:

1. `render()` trusts the caller-supplied `preparation_fingerprint` without recomputing it. Because `PreparedPrompt` is intentionally JSON round-trippable, a caller can modify a material mode-independent field after admission, preserve the old fingerprint, reconstruct the record, and render content that no longer corresponds to the admitted identity.
2. mutable local Protocol source is re-resolved after the stale-context check. It may change between validation and body loading, yielding a body from one source state with profile/input identity from another. The current revalidation also occurs before assembly rather than immediately before successful publication/return, leaving a mutation window across final construction.

At render entry, recompute `sdp.prompt-preparation.v1` from the supplied public record and reject a mismatch before any prompt event. Resolve/use mutable source material coherently rather than checking one read and rendering from a later unchecked read. After artifact construction, perform the final optimistic unchanged-state check required by §3.8 before event publication/return so candidate/workplan/local-source movement during assembly cannot escape. This remains lock-free; do not add repository locks or persistence.

Also make local multi-file Protocol-source resolution itself optimistic/coherent: the version/prompts used for one source identity must be proven to belong to one stable read snapshot or fail/retry boundedly.

Required counterexamples: JSON-roundtrip tamper of a material input/workplan/profile/source/observation field while retaining the old preparation fingerprint -> rejection; local source changes between validation and body use -> stale/incoherent failure; candidate/workplan/source changes during final assembly -> no event and no accepted render.

### R5 — Make extension activation failure-atomic and enforce the already-declared capability/API contract

**Blocking authority:** product invariants 8-10; §3.10; §§4.3-4.4; O10.

The current `ExtensionContext` mutates the live service registry and event bus during `activate()`. If a provider registers a service/subscription and then raises, the provider is marked failed but its registrations survive. This can make a failed extension usable, let it receive prompt-bearing events, and allow dependents to activate incorrectly.

The same composition path currently matches dependencies and `Application.has/service/services` by capability key while ignoring `CapabilityRequirement.api_spec` versus the provisioned API major. Manifest-declared provisions are also not reconciled tightly with services registered during activation, allowing the pre-activation dependency authority and post-activation registry to disagree.

Rewire the one existing composition root to stage activation registrations and commit them to the live registry/event bus only after successful activation and contract validation. Use the existing `CapabilityRequirement`, `CapabilityProvision`, `ExtensionManifest`, and `ExtensionRegistration` fields as the single compatibility contract: enforce API compatibility, singular/multi-provider semantics, provider identity consistency, and declared-versus-registered service consistency. Do not introduce another global registry or plugin layer.

Required counterexamples: provider registers/subscribes then raises -> no capability, no event delivery, dependent disabled; requirement `api_spec` incompatible with Core/provider API -> not admitted/available; undeclared or API-major-mismatched registration -> deterministic incompatibility; healthy unrelated providers/Core remain active.

### R6 — Remove private concrete implementation types from the public v1 API/SPI seam

**Blocking authority:** product invariant 8; parent architecture stable-ID/public-boundary rules; §4.1-4.4; O6.

`spi.v1` publicly re-exports `ExtensionContext`, whose `core()` signature returns private concrete `CoreService`; `api.v1` publicly re-exports `create_application`, whose implementation signature returns private concrete `Application` rather than the Frozen `ApplicationAPI` contract. These are exactly the private lower-module types WP-2+ must not bind to.

Change the existing public annotations/contract wiring so public signatures expose `CoreAPI`/`ApplicationAPI` or other public v1 records/protocols only. Do not wrap the implementation solely to hide its type. Extend the seam test to inspect all public exported callables/context methods, not only `CoreAPI`, for private implementation types/modules.

### R7 — Enforce external-output/resource bounds before materialization and keep user-facing diagnostics redacted

**Blocking authority:** product invariant 7; §§3.3, 3.6, 3.11; O3/O5/O11; Protocol security/release requirements.

The current Git helpers use `subprocess.run(..., capture_output=True)` and only inspect output size after the complete stdout has already been materialized; the remote Protocol-source helper likewise captures command output without a streaming/materialization bound. Remote Protocol resolution also performs a Git fetch into a temporary mirror before the later per-file byte checks, so unrelated remote repository content can be downloaded/materialized outside the stated `MAX_REMOTE_READ_BYTES` contract.

Alter the existing subprocess/remote-source readers so time/output/resource bounds are effective while data is being read, not merely asserted afterward, and so resolving two required Protocol files does not require unbounded unrelated repository content. Keep the current Git/data-only approach if it can satisfy those bounds; do not add a general transport framework. Unexpected CLI/event diagnostics that can contain external exception text must pass through the existing redaction boundary or remain generic.

Required boundary tests: oversized stdout/stderr is terminated/rejected without full in-memory materialization; oversized required remote files fail; a remote repository containing large unrelated content does not force unbounded transfer/materialization to read the bounded required source; user-facing diagnostics remain redacted.

### R8 — Make installed-product acceptance fail closed and record final executable closure evidence

**Blocking authority:** product invariant 15; O1/O11/O12; §6; Protocol testing and release/distribution rules.

`InstalledProductTests.setUpClass()` currently converts wheel-build failure, missing wheel/sdist, venv-creation failure, and wheel-install failure into `SkipTest`. Those are the acceptance owner itself, not optional environment conveniences. A broken distributable can therefore proxy-pass the Core suite as skipped. The branch head also has no GitHub check-run/workflow-run evidence, and the workplan contained no implementation-closure command/result record before this review.

Change required build/install/artifact failures to hard acceptance failures in the normal Core acceptance path. If a truly unsupported external environment prevents an owner check, report that check unavailable explicitly; do not count it as pass. Preserve the existing ordinary repository CI job rather than adding a competing workflow.

After R1-R7, rerun the complete affected surface on the exact candidate: Core focused/regression suite, snapshot parity, wheel+sdist build/inspection/install outside checkout, installed `sdp` end-to-end owner tests, extension composition owner tests, real Git/worktree/remote tests, privacy/web tests, layout/architecture fitness, and the ordinary repository Protocol build/validation/parity/`git diff --check` commands. Record the exact candidate and executed/unavailable results in this workplan before requesting independent Review again.

### 11.1 Re-review gate

WP-1 may return to independent Review only when all R1-R8 counterexamples are closed through the existing semantic owners, the complete final affected regression and installed-product integration pass on one exact candidate, ordinary repository validation passes, and no repair has introduced a parallel observer, registry, prompt authority, compatibility wrapper, persistence mechanism, or higher-module dependency.

The positive implementation findings remain valid and should be preserved: one Core distribution and PEP 420 namespace, the intended small runtime dependency set, no higher-module runtime dependency, one extension entry-point group, canonical prompt snapshot parity, one canonical profile/body extraction path, non-mutating target Git commands, final-artifact privacy tests, passive discovery-only diagnostics, thin integration into the existing repository CI workflow, and no competing prompt-prose authority.

## 12. Second independent review of the reopened repair contract — 2026-09-07

**Verdict remains NO-PASS.** No production repair commit followed the first review; branch head at this pass was the review-only commit `455def2a8dc49e46c15015a0e01f239c242ee7cc`, so the executable candidate under review remains `5e6fd725213ccfdd211f79425d0aef33e03eaeaa`.

This pass re-falsified the implementation and the R1-R8 repair contract against Architecture 1.6.0 and Protocol 5.16. It found additional manifestations in the same semantic owners. They are incorporated here to avoid another one-defect-per-review cycle. This section is a normative clarification/amendment of R1-R8 and adds R9-R11. Where wording conflicts, this section controls. It does not change parent architecture or add product capability.

### 12.1 Amendments to R1-R8

#### R1 amendment — candidate identity must cover all Git-material state safely

In addition to staged blob bytes, `sdp.git-working-tree.v1` must distinguish materially different Git file modes/metadata that Git itself treats as candidate state. Non-UTF-8/surrogateescaped Git paths must not crash canonical JSON encoding; represent them deterministically and reversibly enough for identity, or mark identity incomplete. Apply a finite aggregate candidate-fingerprinting budget as well as per-file/path-count bounds so many individually legal files cannot force effectively unbounded reads.

Required additions: mode-only staged/unstaged changes alter identity; a repository containing a non-UTF-8 dirty filename produces a structured stable/incomplete observation rather than an uncaught encoding failure; aggregate dirty-content overflow yields `identity_complete=false` or a structured bounded failure without pretending the candidate was fully fingerprinted.

#### R2 amendment — selected-remote evidence includes enforceable freshness policy

`ObservationPolicy.max_remote_staleness_seconds` is part of the Frozen public policy and currently has no behavioral owner. It must not remain fingerprint-only/no-op data. A caller-supplied maximum applies to the evidence used for the selected target. If cached remote-tracking evidence has no trustworthy observation age, Core must not invent one from a convenient filesystem/ref timestamp; that evidence cannot satisfy an explicit maximum without refresh or another evidence-backed age. A successful `refresh_remote` query may establish freshness at the actual observation time.

Preserve the earlier remote/target-coherence and `core.remote.ambiguous` requirements. Update user documentation so the several-unresolved-remotes case is documented as `core.remote.ambiguous`, not `core.remote.unavailable`.

Required additions: maximum-staleness policy changes feasibility/result when only age-unknown cached evidence exists; refresh satisfies a compatible maximum; no hidden network call occurs in cached mode; freshness provenance remains distinct from target existence.

#### R3 amendment — canonical path selection and lifecycle authority must agree

A lifecycle-inconsistent document must not silently enter `_active_authorities` merely because it physically resides under `workplans/active/`. Likewise, an exact selector must not let a stage that requires a current governing plan silently use an archived/completed or lifecycle-inconsistent document when that stage policy does not permit that lifecycle. Preserve the explicit Closeout completed-work binding and other stage-specific evidence semantics rather than applying one blanket active-only rule to every stage.

Symlink aliases must not create a second lifecycle/authority interpretation of one underlying document. Prefer the simpler realization (for example, ignore symlink workplan entries) unless a real accepted use case requires them; do not maintain alias reconciliation machinery merely to preserve the current implementation.

Required additions: active-directory + completed status is diagnosed and excluded from implicit active selection; Implementation/Review/Alignment cannot use an archive/inconsistent plan as current governance merely by exact path; Closeout can still bind the completed-plan case authorized by §3.5; an in-repository symlink alias cannot manufacture a second active authority.

#### R4 amendment — preparation identity and revalidation cover the actual admission surface

The recomputed preparation identity must bind the workflow/profile information that external admission is allowed to inspect, not merely a subset of fields used by final text rendering. In particular, `PreparedPrompt.workflow` must either participate in `sdp.prompt-preparation.v1` directly or be cryptographically/semantically bound by another included immutable profile/source identity that fully determines the descriptor. A JSON-roundtrip mutation of transitions, stage metadata, or other material workflow facts must not preserve an accepted preparation fingerprint.

Final rendering must use the **revalidated current observation/source**, not unbound location data copied from the caller-supplied `PreparedPrompt`. Revalidate `WorktreeKey`, selected remote/target evidence, and the material workplan-resolution decision in addition to candidate bytes. This closes cases where the same commit/common repository is reached through a different worktree/config context, or where an ignored/unselected workplan changes an implicit resolver decision without changing the selected file.

Protocol source identity must be checked for packaged, local, and remote sources against the prepared `PromptSourceRef`; mutability determines whether a second end-of-render stability check is needed, not whether prepared provenance may be ignored. Resolve one source snapshot for the body and its validation rather than checking one source object and rendering from a different re-resolution.

Required additions: tampered workflow descriptor with old fingerprint is rejected; tampered/unbound local repo root cannot redirect a local prompt; switching to a different worktree/selected remote under the same serialized preparation is rejected; implicit workplan resolution changing between phases is stale; remote/package source identity differing from the prepared source is rejected rather than silently reinterpreted.

#### R5 amendment — one canonical extension identity and satisfiable provider graph

Use one canonical extension identity through entry-point discovery, manifest validation, dependency edges, status, configuration namespace, registration, and event ownership. Entry-point name versus `manifest.extension_id` disagreement and duplicate canonical IDs must fail/disable deterministically instead of creating two names for one provider.

Capability resolution must consider all compatible providers rather than choosing an arbitrary first manifest as the dependency owner. If one provider for a capability fails but another compatible provider activates, a dependent should be admitted or disabled according to the actual satisfied requirement, not entry-point ordering. Extension registration must not collide silently with Core-owned singular capabilities, and manifest multiplicity/API-major declarations must reconcile with what activation registers.

Keep one registry. Prefer making the existing staged activation result the single registration authority rather than synchronizing manifest, live side effects, and returned `ExtensionRegistration` as three competing truths.

Required additions: entry-name/manifest-ID mismatch; duplicate extension ID; attempted registration of a Core-owned singular capability; two providers where the lexically first fails but the second satisfies the requirement; declared MANY/SINGULAR and API-major mismatch cases.

#### R6 amendment — restore the complete parent public error contract

Architecture 1.6.0 freezes `Problem` with `code`, `message`, `retryable: bool | None`, and `details`. WP-1 §4.6 omitted `retryable`, and the implementation omits it as well. Reconcile the workplan and existing `Problem` owner to the parent contract without creating an exception subclass hierarchy. Existing callers must continue branching on `Problem.code`; `retryable` is structured advisory data, not retry machinery.

The prior public-signature requirement remains: all `api.v1`/`spi.v1` exports, including `create_application` and `ExtensionContext` methods, must expose public v1 protocols/records rather than private concrete classes.

Required additions: `Problem.to_dict()` includes JSON-safe `retryable` (null when unknown); representative deterministic/transient classifications are tested only where Core genuinely knows them; all public exported callable signatures are checked for private implementation modules/types.

#### R7 amendment — bound parsers and ambient process semantics, not only subprocess output

Workplan/frontmatter parsing is an externally influenced resource boundary. Enforce the existing frontmatter byte/nesting/count intent **before or during** YAML/frontmatter materialization; do not parse an amplifying alias/object graph and only then discover it is too large/deep. The simplest compliant policy may reject unsupported YAML alias/complex constructs rather than add a general hardened YAML framework.

Git/subprocess environment construction must also honor §3.2's no semantic environment-override contract. Do not copy arbitrary ambient `GIT_*` variables that can change repository discovery/config/object/remote semantics. Preserve only environment needed for normal process operation and explicitly justified credential/transport mechanisms, while forcing Core's noninteractive/non-mutating controls. This is not a request for a secret manager.

Bound stdout **and stderr**, aggregate dirty-content reads, and remote transfer/materialization before exhaustion. Keep all external exception/diagnostic text behind the existing redaction boundary.

Required additions: oversized/alias-amplified frontmatter is rejected without unbounded construction; ambient Git semantic override variables cannot silently change observed project/remote state; large stderr is bounded; an exception from an extension/subprocess containing a credential-bearing URL is redacted at the final CLI/status surface.

#### R8 amendment — validate every produced distribution artifact that WP-1 claims to ship

WP-1 explicitly requires both wheel and sdist. The acceptance owner must independently inspect the sdist's expected package/source metadata/resources and exercise the closest supported install/consumer path, rather than asserting only that a `.tar.gz` exists. If a distribution artifact were not supported, the correct simplification would be to stop claiming/producing it, but WP-1 currently freezes wheel+sdist delivery, so both must be validated.

Required additions: wheel and sdist each contain the expected package metadata/canonical resources and can produce the supported installed Core behavior outside the checkout; build/install/inspection failure is a hard acceptance failure, not a skip.

### R9 — Make prompt fingerprint/footer assembly collision-safe and enforce the terminal wire contract

**Blocking authority:** product invariants 10, 13-15; §3.9; parent architecture result-envelope/fingerprint contract; O8/O11.

The current renderer substitutes the fingerprint with a global `str.replace(FINGERPRINT_PLACEHOLDER, digest_text)`. Any canonical/user input containing the same literal placeholder is therefore modified even though only the architecture-owned fingerprint slots may change. The footer also interpolates caller-provided RunId directly into JSON without JSON-safe serialization, while `RunId` is a public opaque string. Finally, the reference extractor finds a marked block but does not require the end marker to be terminal and uses stripped marker comparisons, so trailing prose/indented pseudo-markers can be accepted despite the Frozen “terminal final content” rule.

Alter the existing renderer only: substitute the digest at the known architecture-owned fingerprint fields/positions, never by replacing arbitrary prompt content. Serialize/validate dynamic footer identity values so the requested JSON is always valid and the RunId has one coherent semantic value across metadata/result identity. Preserve opaque-ID semantics; if a restricted v1 RunId grammar is chosen, validate it centrally rather than relying on accidental string safety.

Freeze the extraction rule to the actual contract: the begin/end marker syntax must match the declared exact-line semantics, and no non-permitted content follows the terminal end marker. Ordinary human prose may **precede** the footer; “surrounding prose” must not be interpreted as permission for trailing prose after the terminal footer.

Required counterexamples: an explicit input equal to or containing the fingerprint-placeholder literal survives unchanged outside the two fingerprint slots; a caller RunId containing quotes/backslashes/control characters either serializes to valid coherent JSON or is rejected through the declared boundary; indented/near-match markers do not masquerade as exact markers; trailing non-whitespace prose after the end marker is rejected by the reference extractor; the valid canonical footer remains extractable and matches RunId/stage/fingerprint exactly.

### R10 — Make workflow/profile resolution obey governing-workplan precedence and validate explicit profile identity

**Blocking authority:** product invariants 4, 8, 12; §4.2; parent architecture Protocol binding/workflow ownership; O5/O6.

`CoreService.workflow()` currently returns the explicit profile whenever `WorkflowRequest.profile` is present, before considering `request.workplan`. This is the reverse of the Frozen rule in §4.2: selected governing-workplan binding takes precedence. It can therefore make a request carrying an older/incompatible governing workplan appear valid under an explicit 5.16 profile.

The explicit `ProtocolProfileRef` path also consumes only `profile_id`; its declared protocol version/schema/source identity can disagree with the resolved profile and be silently discarded. A public profile reference is an identity assertion, not a hint whose material fields may be ignored.

Rewire the existing workflow owner: when a governing WorkplanRef is supplied, resolve its Protocol contract first; an explicit profile, if also supplied, must agree with the resulting compatible identity or fail. With profile only, resolve the named profile and validate the supplied material identity fields against it rather than silently rewriting them. Project default remains fallback only when neither stronger authority determines the contract.

Required counterexamples: explicit 5.16 profile + governing 5.9 workplan fails as incompatible rather than returning 5.16; explicit profile with mismatched protocol/schema/source identity fails; agreeing workplan+profile succeeds; profile-only and project-only paths still resolve through the one profile owner.

### R11 — Make canonical source/profile reconciliation exhaustive and bind packaged generation to `PROTOCOL_VERSION`

**Blocking authority:** product invariants 3-4, 12, 15; §3.6; O5/O8; release/source-of-truth requirements.

The canonical parser proves that each expected 0-8 heading exists but does not reject additional numbered stage headings or conflicting numbered headings with different titles. `build_profile()` then checks its constant stage table rather than the full numbered stage set actually present in the document. A local/remote source can therefore contain an extra stage-like authority that Core silently ignores instead of reporting source/profile incoherence.

The packaged snapshot generator derives `prompts.md` and `profile.json` from the prompt document but does not read/bind canonical `source/PROTOCOL_VERSION`. Today both happen to be 5.16.0, but the generation mechanism can produce a “5.16” package from a later-version canonical source after that version file changes. That violates the claim that the package is a version-bound reproducible derivative.

Make canonical reconciliation exact: the numbered canonical stage-heading set for the supported profile must match the expected set without extras/duplicates/conflicting numbers. Bind generation/check mode to canonical `PROTOCOL_VERSION` and the profile's declared compatibility/version; a mismatch fails generation/check instead of emitting/revalidating a mislabeled package. Reuse the existing profile/source constants and generator; do not create a second manifest authority merely to solve this.

Required counterexamples: extra `## 9. ...` stage heading fails source-incoherent; conflicting extra numbered heading fails; generator `--check`/generation fails when canonical `PROTOCOL_VERSION` is incompatible with the packaged profile; current 5.16 source still reproduces byte-identical packaged prompt/profile resources.

### 12.2 Documentation reconciliation required by the repairs

Update affected user/API documentation in the same implementation cycle so it does not preserve now-known false behavior. At minimum:

- unresolved multiple remotes are `core.remote.ambiguous` when ambiguity is the cause;
- terminal footer prose may precede the footer, not follow it;
- explicit user text is intentional content but structure-sensitive INPUT insertion uses the documented reversible scalar encoding rather than literally splicing raw control characters;
- `max_remote_staleness` behavior and cached-age uncertainty are documented once the existing public field has real semantics;
- `Problem.retryable` is documented as advisory structured data, not automatic retry policy.

Do not add a second specification document merely for these corrections; reconcile the existing architecture/workplan/public API docs and Core user guide.

### 12.3 Final re-review gate

WP-1 may return to independent Review only after R1-R11, including every amendment in §12.1, are closed in the existing semantic owners and no repair creates a parallel candidate identity, workplan resolver, remote observer, Protocol/profile authority, prompt renderer, service registry, compatibility wrapper, persistence layer, or higher-module dependency.

The final exact candidate must have recorded executable evidence for:

1. focused counterexample tests for R1-R11;
2. complete Core regression, including Hypothesis properties when the declared dev dependency is installed;
3. real temporary-Git/worktree/remote owner tests and non-mutation checks;
4. canonical source/profile/generator parity and incompatibility tests;
5. real installed entry-point extension composition tests;
6. wheel **and** sdist build/inspection/install/installed-CLI behavior outside the checkout;
7. final web/local privacy and prompt-wire fixtures;
8. public API/SPI contract/signature fixtures;
9. repository layout/architecture fitness checks;
10. ordinary repository Protocol tests/build/package-parity/`git diff --check` validation.

Any unavailable required owner check is recorded as unavailable and remains a blocker unless the governing contract explicitly permits substitute evidence. A green skip is not closure. Only after those checks pass on one exact candidate may the workplan be closed.

**Second-pass review verdict: NO-PASS — the repair contract is now tightened and snapshot-complete for the currently observed blocker families; return to `software-implementation`, not another Review, until the listed families are repaired and final owner evidence is recorded.**

## 13. Implementation closure evidence — 2026-09-07

Implementation acceptance evidence for the reopened R1-R11 repair contract is
recorded below. This is not an independent Review verdict; the prior Review
verdict remains **NO-PASS** until a separate review evaluates this candidate.

### Exact candidate

- Branch: `plan/protocol-orchestrator`
- Base HEAD before the implementation diff: `fc466570e7a9a3b6d2fab99a1440fe72a0a46064`
- Implementation diff: 26 changed files under `orchestrator/`; SHA-256 of
  `git diff --binary` excluding this workplan evidence section:
  `51e9c4fca97f38da28acd253888ae12251a7ea5139ff700a1021b43899bbc920`
- No commit, reset, stash, or destructive worktree cleanup was performed.

### Executed evidence

All required owner checks were available and passed on this candidate:

1. Focused affected regression:
   `PYTHONPATH=orchestrator/packages/core/src /tmp/sdp-orchestrator-core-venv/bin/python orchestrator/scripts/run_core_tests.py tests.test_config_and_projects tests.test_extension_composition tests.test_git_observation tests.test_input_binding tests.test_layout_and_fitness tests.test_privacy_and_remote_truth tests.test_protocol_source_and_profile tests.test_public_api_seam tests.test_render_and_identity tests.test_workplan_resolution`
   passed **312 tests across 10 modules in 10 concurrent workers**.
2. Complete Core acceptance:
   `PYTHONPATH=orchestrator/packages/core/src /tmp/sdp-orchestrator-core-py311-venv/bin/python orchestrator/scripts/run_core_tests.py`
   passed **339 tests across all 11 modules in 11 concurrent workers**, including
   the installed-product owner: wheel and sdist build, inspection, clean
   installation, installed `sdp` CLI behavior outside the checkout, extension
   composition, real temporary Git/worktree/remote, privacy, wire, and public
   API/SPI fixtures.
3. Hypothesis was installed and active in `test_input_binding`; the two scalar
   properties ran with **400 + 200 generated examples**.
4. Canonical source/profile and generator checks passed:
   `orchestrator/scripts/generate_protocol_snapshot.py --check`, including the
   incompatible canonical-version counterexample.
5. Ordinary repository acceptance passed:
   `python -m unittest discover -s tests` (**172 tests**),
   `source/build_skills.py --output <temporary directory>`,
   `source/validate_packages.py --dist <temporary directory>`,
   `source/check_dist.py --expected <temporary directory> --committed dist`,
   and `git diff --check`.
6. Focused Semgrep scans completed successfully over the tracked Core source:
   `subprocess.run(...)` and `shutil.copytree(...)` each produced zero findings.
   The only direct `os.environ` match was the intended allowlisted environment
   construction in `_git.py`; no managed/cloud scan or source upload was used.
7. Serena project activation and symbol/reference inspection were used during
   owner reconciliation. No additional observer, prompt authority, persistence
   layer, compatibility wrapper, higher-module dependency, or second registry
   was introduced.

The implementation evidence is complete and ready for the separate independent
Review gate; this workplan remains active until that gate records its own
verdict.
