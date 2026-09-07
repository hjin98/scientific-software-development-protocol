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

# Protocol Orchestrator WP-1 — Prompt Module + Core Program

## 1. Product objective and hard boundaries

WP-1 builds the smallest independently useful Protocol Orchestrator product. A user configures a software repository and runs commands such as:

```text
sdp design --task "..."
sdp implementation
sdp review
sdp prompt verification --input VERIFICATION_SCOPE="..."
```

Core prints one complete, copy/paste-ready, stage-correct Protocol prompt to stdout. Mechanically knowable repository, candidate, workplan, Protocol-profile, and execution-context inputs are resolved automatically. Inputs that are genuinely user-authored and cannot be inferred safely are required explicitly rather than left as editable placeholders.

Core-only installation is a finished operating mode. It requires no history database, agent process integration, benchmark service, account model, quota meter, predictor, or scheduler.

### 1.1 Tier-1 product invariants

1. **Core works alone.** `sdp-orchestrator-core` plus the `sdp` CLI performs configuration, project/worktree observation, workplan resolution, compatible workflow/profile resolution, and prompt rendering end to end without Tracker/Adapter/Scheduler.
2. **Observation is non-mutating.** Core never changes target worktree content, index, HEAD, branches, local refs, remote-tracking refs, or remote repository merely to inspect state. Explicit remote refresh uses a read-only query boundary, not `git fetch`/pull.
3. **Canonical prompt authority is singular.** Stage prompt prose comes from the governing-version-compatible SDP canonical prompt source. Packaged prompt resources are reproducible version-bound derivatives, never independently maintained authority.
4. **Protocol binding is explicit.** Work governed by Protocol `X` is never silently interpreted through an incompatible newer profile. Semantic versions are not guessed to be Git refs.
5. **Ambiguity is explicit.** Project, workplan, Protocol source/profile, Git remote, and required user-input ambiguity fails truthfully instead of using fuzzy names, mtime, path ordering, or undocumented heuristics.
6. **Rendered prompts are operationally truthful.** Web-mode output does not claim that local-only dirty/unpushed state is remotely inspectable. Local mode may reference the local worktree. Both modes preserve actual candidate/profile provenance.
7. **Privacy is bounded and truthful.** Core never automatically embeds local private paths in web prompts, credential-bearing remote userinfo, ambient environment data, credential-helper output, or private orchestrator state. Explicit user-authored `--task`/`--input` text is intentional prompt content and is not subject to impossible arbitrary-secret inference.
8. **Core v1 is a durable lower-module seam.** Later modules can consume accepted public API/SPI services without private imports, duplicated Protocol-routing logic, or reverse dependency.
9. **There is one composition root.** Core owns the `sdp` executable, the application/service registry, and the single extension entry-point group.
10. **Manual tracking compatibility exists from day one.** Every prompt carries a `RunId`, deterministic prompt fingerprint, and a requested `StageResultEnvelope v1`; Core exposes a non-durable prompt-rendered event seam for later Tracker integration.
11. **Determinism follows semantic state.** With a caller-supplied fixed RunId and unchanged semantically relevant project/candidate/workplan/profile/input state, prompt bytes/fingerprint do not drift merely because wall-clock observation metadata or unrelated extension configuration changed.
12. **Installed behavior is the acceptance owner.** Helper-level tests cannot proxy-pass a broken built artifact, packaged profile, extension discovery surface, real Git observer, console entry point, stdout contract, or web privacy/truthfulness boundary.

### 1.2 Explicit non-goals

WP-1 does not implement:

- SQLite or durable event/run/workflow history;
- `sdp status`, `sdp next`, `sdp ingest`, `sdp history`, `sdp graph`, persistent workplan selection, or lifecycle projection;
- Claude/Codex/OMP/Pi/Antigravity/ACP execution, subprocess control, sessions, approvals, or cancellation;
- Artificial Analysis, DeepSWE, model/backend/account catalogs, recommendation/ranking, or network benchmark refresh;
- quota/cost meters, resource ledgers, reservations, usage prediction, or AUTO scheduling;
- daemon/resident watcher, generic workflow engine, ORM, or event-sourcing framework;
- repository-local orchestrator state;
- arbitrary plugin-directory scanning or repository-loaded executable plugins;
- automatic installation/upgrading of Protocol sources, extensions, agents, or providers;
- speculative compatibility profiles for Protocol versions whose exact contract is not supplied and validated;
- a second CI authority or an orchestrator representation under generated `dist/skills` unless later release policy explicitly requires one.

## 2. Governing authority and baseline

Parent authority:

```text
orchestrator/docs/architecture.md
architecture_version = 1.5.0
protocol_version = 5.16.0
```

WP-1 inherits the parent module ladder, one-way dependency direction, Core API/SPI ownership, workflow-profile ownership, Protocol-version binding, privacy boundary, and standalone acceptance rules.

Protocol 5.16 remains the generic lifecycle/testing/review authority. Initial canonical prompt source:

```text
source/shared/references/development-workflow-prompts.md
```

At workplan creation `orchestrator/` contains architecture documentation but no executable Core implementation. The greenfield quality ratchet is therefore: no duplicate prompt authority, no later-module machinery, minimal justified dependencies/public surface, executable namespace/import/entry-point guards, and rejection-capable ambiguity/version/privacy/identity tests.

## 3. Frozen WP-1 architecture

### 3.1 Distribution and package boundary

Create one independently installable Python distribution:

```text
sdp-orchestrator-core
```

with console entry point:

```text
sdp
```

and native PEP 420 namespace:

```text
sdp_orchestrator.core
```

No `sdp_orchestrator/__init__.py` may be owned by Core. Initial supported runtime floor is Python 3.11+. Package release version, architecture version, Protocol version, config schema version, API/SPI major, workflow-profile schema, result schema, and digest-canonicalization versions are independent identities and must not be conflated.

Expected runtime dependencies, unless implementation demonstrates a smaller contract-equivalent set:

```text
platformdirs
typer
pydantic
python-frontmatter
packaging
```

Optional clipboard support may use a `pyperclip` extra/equivalent. Core has no runtime dependency on `filelock`, ACP, `httpx`, ORM/event-sourcing, ML packages, Tracker, Adapter, or Scheduler.

### 3.2 Configuration and extension namespaces

Core owns one TOML normalization/validation path. Default config location comes from `platformdirs`; API/CLI may explicitly override the path. V1 has no semantic environment-variable override allowlist unless implementation evidence establishes a genuine Core need; ambient environment variables do not silently alter prompt semantics.

Minimum Core config:

```toml
schema_version = 1

[core]
default_project = "mdstats"       # optional
default_execution_mode = "web"    # optional; local | web

[projects.mdstats]
repo = "/absolute/path/to/mdstats"
protocol_profile = "sdp-protocol-5.16"
default_execution_mode = "web"    # optional
remote_name = "origin"             # optional; Git remote name, never a credential URL

[protocol_sources."sdp-protocol-5.16"]
local_root = "/path/to/software-development-protocol"   # optional
allow_remote = false                                    # default
remote_repository = "https://github.com/hjin98/software-development-protocol"  # optional
remote_ref = "<exact evidence-backed ref>"              # required when remote fallback is enabled

[extensions."some.extension"]
# extension-owned data; Core preserves but does not semantically interpret it
```

Rules:

- Core validates Core/project/protocol-source namespaces through one canonical model.
- Unknown/absent-extension namespaces are preserved as bounded raw configuration and diagnosed as inactive, not rejected merely because the extension is not installed.
- When an extension activates, only that extension validates/owns its namespace through the Core SPI.
- Opaque extension configuration does not participate in Core prompt identity unless an active extension explicitly changes a Core-owned prompt request through a defined public hook; unrelated extension settings cannot perturb Core-only prompt bytes.
- Secrets/tokens are not supported as ordinary Core config values. Explicit remote authentication may use established Git/platform credential mechanisms without serializing credential values into Core config snapshots, diagnostics, prompt context, event payload metadata, or digests.

CLI project resolution when `--project` is absent:

```text
unique configured project whose canonical worktree contains cwd
  -> configured core.default_project
  -> sole configured project
  -> core.project.ambiguous / core.project.not_found
```

Public Core API requests use explicit `ProjectKey`; CLI convenience resolution is not hidden API behavior.

### 3.3 Read-only repository, candidate, and worktree observation

`ObservationPolicy` v1 supports:

```text
local_only
use_cached_remote
refresh_remote
```

- default = `local_only`;
- `use_cached_remote` may inspect existing upstream/remote-tracking refs without changing them;
- `refresh_remote` performs a bounded noninteractive read-only query such as `git ls-remote`/equivalent and must not mutate target refs/worktree/index;
- remote queries have bounded runtime/output and redact credential-bearing diagnostics;
- Core does not execute repository files or build hooks merely to inspect Git/workplan state.

`CandidateRef` identifies at least repository identity, branch/detached state, HEAD commit, relevant staged/unstaged/untracked state, upstream/observed remote state when known, observation provenance, and identity completeness. `sdp.git-working-tree.v1` must change when materially different dirty content exists at the same paths, not only when path/status changes. If bounded exact fingerprinting is not possible, `identity_complete=false` rather than counterfeit exactness.

`WorktreeKey` identifies one physical Git worktree: symlink/path aliases to the same worktree map to one key; distinct linked Git worktrees map to different keys.

### 3.4 Git remote selection and web target identity

Remote selection is deterministic and separate from credentials:

```text
projects.<key>.remote_name, when configured and valid
  -> current branch upstream remote, when uniquely defined
  -> remote named origin, when present
  -> sole configured Git remote
  -> core.remote.ambiguous / core.remote.unavailable
```

Core records the selected remote name and a sanitized repository identity. It strips URL userinfo/embedded credentials. `file://` and filesystem-path remotes are local-only and are not valid web-agent targets.

For a normal branch, the web target ref is the configured/upstream branch when known, otherwise the current local branch name on the selected remote. Detached HEAD web rendering is unavailable in v1 unless Core can establish an explicit remotely addressable target without guessing; local rendering remains valid.

Web rendering requires a non-local sanitized remote repository identity. Material dirty local state blocks web render. Known local/remote committed divergence blocks web render rather than pretending the local candidate is remotely visible. Cached/unknown remote freshness may still be represented only when the prompt/footer labels that provenance truthfully; explicit `refresh_remote` can establish fresher evidence without mutating the target repository.

### 3.5 Workplan discovery, selection, and identity

Core catalogs repository-owned regular Markdown/text workplan documents under `workplans/active/` and `workplans/archive/`, including nested current `AUTHORITY.md` and frontmatter-marked implementation workplans. Path resolution remains inside the configured repository root; symlink/traversal escapes are rejected/ignored safely. File count, file size, and frontmatter/parser work are bounded.

Parsing is data-only. YAML/frontmatter loading must not permit arbitrary Python object construction or repository code execution.

Documents sharing a `workplan_id` are deduplicated according to explicit current-authority evidence. Historical numbered revisions are not independent active plans when a current authority file clearly owns the workplan. If repository conventions cannot determine current authority without guessing, report ambiguity.

Explicit workplan selector semantics are exact:

```text
exact workplan_id
or exact repository-relative canonical workplan path
```

For stages requiring a governing workplan:

```text
explicit selector
  -> unique current-branch binding from recognized metadata (v1 recognizes target_branch)
  -> exactly one active workplan
  -> required/ambiguous failure
```

No fuzzy filename or recency selection.

`WorkplanRef` carries artifact digest, semantic digest when safely available, semantic-identity completeness, path, protocol version, workplan ID, and lifecycle state. `sdp.workplan-semantic.v1` uses an explicit tested list of lifecycle-only metadata that may be excluded; unknown/unrecognized semantics are conservative. Body/Frozen-authority changes must alter semantic identity. Exact v1 exclusion rules are frozen in fixtures before WP-1 Review acceptance.

### 3.6 Protocol profile, canonical prompt source, and packaged snapshot

V1 supports one explicit Protocol 5.16-compatible profile unless later accepted evidence adds another.

Resolution order:

```text
explicit configured compatible local source/profile
  -> exact compatible packaged profile/prompt snapshot
  -> explicitly permitted canonical read-only remote source at exact evidence-backed ref
  -> truthful core.protocol.incompatible / core.protocol.unavailable
```

A semantic protocol version is never guessed to be a Git branch/tag/ref.

Canonical stage prose is extracted reproducibly from the canonical source. For v1, each stage body is the literal fenced `text` block belonging to the uniquely identified canonical stage heading. If canonical structure no longer permits unique extraction, generation fails instead of choosing heuristically.

A small machine-readable 5.16 profile may define only bounded control metadata: stage keys/aliases, role owner, mutation class, recognized outcomes, routing trigger classes/transitions, workplan requirement, input bindings/default classes, compatibility/source identity, and result-schema identity. It may not duplicate stage prompt prose or become a generic executable workflow DSL.

The installed wheel must render its packaged 5.16 prompt/profile offline when local repository evidence is sufficient. Source-to-package parity compares the actual canonical source against packaged stage bodies/profile metadata; self-comparison of two products of the same stale private constant is not acceptance.

### 3.7 Stage input completeness and ownership

A successful WP-1 render contains no unresolved user-edit placeholder. Every canonical stage INPUT is classified by the 5.16 profile as one of:

```text
mechanical          # Core resolves from project/candidate/workplan/profile/request
canonical_default   # canonical AUTO/NONE/default sentinel remains deliberately
required_user       # caller must provide explicit data; absence is an error
```

Core does not convert a semantic question into an automatic guess merely to avoid asking for required data.

Required user-owned v1 stage inputs are:

| Stage | Required user input | Binding |
| --- | --- | --- |
| baseline | `BASELINE_SCOPE` | `--input BASELINE_SCOPE=...` |
| design | `TASK` | dedicated `--task` |
| implementation | none beyond a resolvable governing workplan | automatic/`--workplan` |
| review | none beyond a resolvable governing workplan | automatic/`--workplan` |
| verification | `VERIFICATION_SCOPE` | `--input VERIFICATION_SCOPE=...` |
| stabilization | `STABILIZATION_SCOPE` | `--input STABILIZATION_SCOPE=...` |
| alignment | downstream workplan + `UPSTREAM_ACCEPTED_WORK` | `--workplan` + `--input UPSTREAM_ACCEPTED_WORK=...` |
| health-audit | `AUDIT_SCOPE` | `--input AUDIT_SCOPE=...` |
| closeout | `COMPLETED_WORK`, unless an explicitly selected workplan satisfies the profile binding exactly | `--input COMPLETED_WORK=...` or exact `--workplan` |

The profile may preserve canonical `AUTO`/`NONE` for fields such as authority discovery, history window, additional constraints, documentation discovery, or implementation target where the canonical prompt explicitly permits that sentinel.

`input_overrides`/`--input` may set only names declared by the selected canonical INPUT block and not already owned by a dedicated first-class request field/mechanical binding. Unknown input => `core.prompt.input_unknown`; missing required user input => `core.prompt.input_required`; conflict with a first-class/mechanical binding => `core.prompt.input_conflict`.

Concrete inserted user/mechanical strings use one deterministic structure-safe single-line serialization rule. Raw NUL/CR/LF or similar structural injection is never spliced directly into the `INPUTS` grammar; the exact reversible v1 encoding is frozen in fixtures before Review. Canonical sentinel values remain canonical. This is representation safety, not a claim that user-authored prompt content is semantically untrusted or secret-scanned.

### 3.8 Prompt modes, privacy, and secret boundary

Core v1 prompt execution modes are `local` and `web`.

Web mode excludes automatically derived local absolute repository/config/state paths, local/file remotes, ambient environment values, credential-helper output, and credential-bearing remote userinfo. It includes only sanitized remotely useful repository/candidate/workplan/profile context whose visibility is represented truthfully.

Local mode may include authorized local repository/worktree paths but still never automatically includes credential values or unrelated environment data.

Core does **not** promise arbitrary secret detection over user-authored `--task`/`--input` text. Explicit user values are intentionally rendered. Documentation must state that secrets should not be placed in prompt inputs. Core's hard guarantee is that it does not automatically source or propagate secrets from unsupported config fields, environment, credential stores/helpers, or URL userinfo.

### 3.9 Prompt artifact, fingerprint, and result envelope

The canonical selected stage body is preserved except for declared INPUT substitution under §3.7. Core may append only the architecture-approved orchestration footer: RunId, prompt fingerprint, bounded source/candidate/remote-visibility provenance, and the `StageResultEnvelope v1` request. The footer cannot weaken or reinterpret stage instructions.

Volatile observation timestamps/diagnostics remain structured provenance and are not injected into prompt bytes unless a canonical input materially requires them.

`sdp.prompt-fingerprint.v1`:

1. use caller RunId or allocate one opaque RunId;
2. render exact full prompt artifact with a fixed fingerprint placeholder;
3. hash the exact normalized UTF-8 placeholder-form bytes with SHA-256;
4. substitute `sha256:<hex>`;
5. freeze placeholder, line-ending, terminal-newline, and input-scalar normalization in executable fixtures.

Every prompt requests `StageResultEnvelope v1` with at least schema version, run_id, prompt_fingerprint, stage, outcome, optional recommended_next_stage, blockers, completed/pending obligations, checks executed/unavailable, candidate, and summary. `BlockerRecord` includes summary plus optional blocker ID/classification/authority class. The footer never requests hidden chain-of-thought. Core renders but does not persist or semantically interpret returned results.

### 3.10 Extension composition and event subscription

Core discovers extensions only through:

```text
sdp_orchestrator.extensions.v1
```

`ExtensionProvider.manifest()` is side-effect-minimal. Activation is dependency-topological, with explicit capability/API-major requirements. Incompatible/failed optional extensions disable themselves and dependents without breaking healthy Core. Dependency cycles/missing required capabilities are diagnosed deterministically. Singular services cannot be silently replaced; multi-provider ordering is stable by provider ID.

In-process extensions are trusted executable code, not a security sandbox. Core nevertheless applies least-privilege API exposure: `ExtensionContext` provides only versioned required services, the extension's own config namespace, and bounded CLI/config/event/diagnostic registrars rather than private Core objects.

Event sinks register explicit event-type subscriptions. Core does not broadcast prompt text to sinks that did not request the prompt-rendered event. `core.prompt.rendered.v1` is a sensitive local-process event whose payload is sufficient for an authorized Tracker sink to reconstruct the `RenderedPrompt` record, including complete prompt text. Its logical `EventId` is stable for event type + RunId + prompt fingerprint so duplicate delivery is idempotent. Core has no durable queue; sink failure is diagnosed but cannot counterfeit or invalidate an otherwise successful primary render result.

### 3.11 CLI stdout and diagnostics

Prompt commands write exactly one complete prompt to stdout. Warnings/errors/diagnostics go to stderr; failure uses deterministic nonzero exit status derived from structured `Problem.code`. Thus:

```text
sdp review > prompt.txt
```

produces a clean prompt artifact.

Optional `--copy` is additive. Clipboard unavailability may produce a clipboard-specific problem/warning for the copy action but never removes the rendered prompt from stdout.

## 4. Public Core API/SPI v1 contract

### 4.1 General public-record rule

Anything reachable from a public `sdp_orchestrator.core.api.v1` or `sdp_orchestrator.core.spi.v1` signature is itself a public v1 record or standard immutable scalar/container. Public records are JSON-compatible immutable-by-convention values; Pydantic is initial technology, not semantic authority. No public record contains open files, subprocess/session objects, Git library objects, locks, event loops, DB connections, or private implementation objects.

Opaque IDs serialize as strings; timestamps as UTC ISO-8601; domain digests carry algorithm + versioned canonicalization scheme + value. Potentially unbounded collections use `Page[T]` with opaque query-scoped cursor.

Critical v1 public types include at least:

```text
ProjectKey, WorktreeKey, RunId, EventId, StageRef, CapabilityKey, ExtensionId
DigestRef, ProtocolProfileRef, PromptSourceRef, WorkplanRef, CandidateRef
RemoteRepositoryRef, ProjectDescriptor, PromptProjectSnapshot
WorkflowProfileDescriptor, StageDescriptor, StageTransitionDescriptor
BlockerRecord, StageResultEnvelope, EventEnvelope
ProjectQuery, ProjectObservationRequest, ProjectObservation, ObservationPolicy
WorkplanQuery, WorkplanDescriptor, PromptRequest, RenderedPrompt, ResolvedInput
CapabilityRequirement, CapabilityProvision, CapabilityStatus
ApplicationRequest, ExtensionManifest, ExtensionContext, ExtensionRegistration
EventSubscription, Problem, Page[T]
```

Exact field spelling/private decomposition may be finalized during Implementation only within the parent/workplan semantics. Independent WP-1 Review freezes accepted `api.v1`/`spi.v1` schemas as the compatibility floor for WP-2+.

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

All methods are read-only with respect to target repositories. `allocate_run_id()` creates identity only, no durable record. `list_stages()` is a convenience view of `workflow().stages`, not second stage authority.

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

Core provisions at least:

```text
prompt.render
project.observe
workplan.catalog
workflow.profile
```

Capability identity is semantic/unversioned; API major/spec compatibility is separate.

### 4.4 Extension SPI v1

```python
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...
    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...
```

Manifest/activation semantics follow §3.10 and parent architecture. `ExtensionContext` must support explicit event subscription/sink registration and preserve absent-extension configuration semantics from §3.2.

### 4.5 PromptRequest / RenderedPrompt

`PromptRequest v1` semantically carries:

```text
run_id | None
project
stage
execution_mode
workplan_selector | None
first_task | None
input_overrides
observation_policy | None
```

`RenderedPrompt v1` semantically carries:

```text
run_id
prompt_text
prompt_fingerprint
stage
prompt_source
workflow_profile
resolved_inputs + provenance
prompt_context
selected_workplan | None
requested_result_schema identity
```

### 4.6 Error contract

Python APIs raise one `OrchestratorError(Problem)`. Callers branch on `Problem.code`, never message text. V1 establishes at least:

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
core.remote.ambiguous
core.remote.local_only
core.remote.stale
core.remote.target_unavailable
core.prompt.input_required
core.prompt.input_unknown
core.prompt.input_conflict
core.prompt.input_invalid
core.extension.incompatible
core.extension.activation_failed
core.extension.dependency_cycle
core.clipboard.unavailable
```

Do not create a large subclass hierarchy merely to mirror codes.

### 4.7 CLI request mapping

All Core prompt request inputs are available non-interactively:

```text
--project <ProjectKey>
--workplan <exact workplan_id-or-relative-path>
--execution-mode local|web
--config <path>
--remote-mode local_only|use_cached_remote|refresh_remote
--task <text>                  # Design TASK
--input NAME=VALUE             # repeatable, profile-declared non-first-class inputs
--copy                         # optional clipboard extra
```

`--task` outside Design fails clearly. Missing required user input, unknown `--input`, and conflicting override fail before rendering. API and CLI share one normalization/validation path.

Canonical stage commands:

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

Aliases resolve through the compatible profile rather than hard-coded duplicate stage semantics.

## 5. Implementation obligations and acceptance

### O1 — Build/install/package boundary

Create `sdp-orchestrator-core`, PEP 420 namespace, `sdp` entry point, packaged 5.16 profile/prompt resources, and only justified Core dependencies.

Acceptance:

- build supported wheel/sdist;
- independently inspect metadata/resources/entry point and absence of accidental secrets/local paths/scratch;
- install wheel outside source checkout;
- execute installed `sdp --help`, `sdp projects`, `sdp capabilities`, `sdp doctor`, and representative prompt commands;
- install a sibling namespace fixture distribution to prove namespace coexistence;
- reject root namespace `__init__.py` and production imports of Tracker/Adapter/Scheduler.

### O2 — Config/project/extension-namespace resolution

Implement §3.2 through one normalization path.

Acceptance covers explicit/cwd/default/sole/ambiguous project selection; invalid/malformed Core config; empty env allowlist; project mode override; absent-extension config preservation; active extension namespace handoff; unrelated extension config not changing fixed-RunId prompt identity; secret-bearing Core config rejection/redaction; local Protocol-source override; remote source disabled by default and exact-ref-bound when enabled.

### O3 — Real Git/worktree/remote observation

Acceptance owner is the production observer against actual temporary Git repositories/worktrees/remotes.

Cover branch/detached HEAD, staged/unstaged/untracked content, two different dirty contents at same paths, symlink alias same WorktreeKey, separate linked worktree different WorktreeKey, upstream known/unknown, deterministic remote-selection precedence, multiple-remote ambiguity, local/file remote rejection for web, sanitized HTTPS/SSH remotes, cached remote provenance, bounded noninteractive read-only remote refresh, and identity-incomplete bounded cases.

Prove target worktree/index/HEAD/local refs/remote-tracking refs remain unchanged after observation/refresh.

### O4 — Workplan catalog and identity

Cover top-level plans, nested current `AUTHORITY.md`, archive state, exact ID/path selector, `target_branch` binding, multiple-active ambiguity, selector not found, safe lifecycle-only semantic-digest preservation, body/Frozen semantic change, malformed/oversized documents, symlink/path escape, duplicate IDs, and conservative unknown-schema handling.

Implementation/Review must fail if no governing workplan can be resolved. Design may run without an existing workplan only with `--task`. Alignment requires an exact downstream plan.

### O5 — Protocol 5.16 source/profile/snapshot

Acceptance:

- uniquely extract every canonical stage fenced body from actual `development-workflow-prompts.md`;
- source-to-packaged body parity for all stages;
- reconcile stage aliases, input bindings, workplan requirements, outcomes/transitions, source/profile identity with supplied 5.16 references;
- offline installed-wheel rendering;
- explicit local source success;
- remote source fallback off by default, exact-ref-bound when enabled;
- older/unknown workplan never silently rendered as 5.16;
- incompatible source fails truthfully.

### O6 — Stage-input completeness

Exercise **all canonical stages**, not only Design/Implementation/Review.

Acceptance proves:

- every canonical INPUT is classified as mechanical/canonical_default/required_user;
- table in §3.7 is enforced;
- missing required user input fails with `core.prompt.input_required` and no partial prompt on stdout;
- unknown/conflicting input fails before render;
- `--task`/API first_task parity;
- selected workplan bindings for Implementation/Review/Alignment/eligible Closeout;
- deterministic structure-safe scalar encoding for multiline/control-bearing values;
- no unresolved editable placeholder in a successful final prompt.

### O7 — Core API/Application API/extension/event SPI

Acceptance:

- public import/schema/round-trip fixtures for every type reachable from v1 signatures;
- no private class in a public signature;
- capability/API-major separation including `workflow.profile`;
- actual `importlib.metadata` entry-point discovery using an installed fixture extension distribution;
- compatible/incompatible/missing-dependency/cyclic extension cases;
- duplicate singular service rejection and stable multi-provider ordering;
- absent-extension config preserved;
- prompt event delivered only to an explicitly subscribed sink;
- unsubscribed sink does not receive complete prompt text;
- stable logical EventId/duplicate delivery tolerance;
- sink failure does not change primary render result.

### O8 — Canonical prompt renderer

Use the production observer/resolver/profile/renderer path.

Acceptance:

- all stage bodies render from the correct canonical fenced block;
- no cross-stage body contamination;
- declared INPUT substitution only;
- canonical AUTO/NONE sentinels preserved when profile-classified as defaults;
- footer is appended separately and cannot rewrite stage prose;
- fixed RunId + identical semantic state gives byte-identical prompt/fingerprint across time;
- relevant stage/workplan/candidate/mode/input/source changes change fingerprint when artifact changes.

### O9 — Web/local privacy and remote truthfulness

Acceptance boundary is final `RenderedPrompt.prompt_text` and installed CLI stdout.

Fixtures include distinctive home/config/private-state paths, credential-bearing HTTPS URL, SSH remote, local/file remote, multiple remotes, dirty local state, local-ahead/remote-ahead divergence, cached/unknown remote state, and ambient secret-like environment values.

Web output must not automatically contain prohibited local/credential/ambient values. Web render requires a deterministic non-local remote target; dirty local state and known committed divergence block. Cached/unknown freshness is labeled truthfully. Local mode may include the authorized repo path.

Explicit user `--task`/`--input` text is expected to appear and is not used as an arbitrary-secret-detection test.

### O10 — Run/fingerprint/result-envelope contract

Freeze and test RunId preservation/allocation, exact placeholder, input-scalar normalization, UTF-8/line-ending/terminal-newline normalization, prompt digest, StageResultEnvelope/BlockerRecord schema identity, and no hidden-chain-of-thought request.

### O11 — CLI and diagnostics

Acceptance boundary is installed `sdp` subprocess execution, not direct Typer callbacks.

Prompt stdout contains prompt only. Errors/ambiguity go to stderr with deterministic nonzero status. Every stage alias and `sdp prompt <stage>` resolves through the same profile. `sdp doctor` is non-mutating/no-network by default and reports Core config/project/profile/extension/clipboard readiness only. Optional `--copy` does not remove stdout usability.

### O12 — Documentation, CI, and final simplicity closure

Document install/config/project/remote selection, required stage inputs, local/web behavior, Protocol binding, exact workplan selection, piping/copying, extension trust/subscriptions, bounded secret guarantee, and explicit absence of higher-module features.

Integrate Core acceptance into the repository's ordinary validation path rather than creating a competing CI authority. Preserve existing Protocol validation:

```text
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

Core package/test/install acceptance is additional. `dist/skills` remains Protocol-skill transport, not an automatic orchestrator wheel destination.

Before handoff, reconcile every WP-1 obligation against the assembled implementation, re-derive affected surface, run final complete Core regression/real-boundary integration/repository checks, and delete speculative persistence/transport/resource/benchmark hooks or duplicate prompt/profile authorities.

## 6. Real semantic-owner acceptance boundaries

1. **Prompt product:** installed `sdp` -> production application composition -> production observer/workplan/profile resolver -> production renderer -> stdout.
2. **Git observation:** production observer against real temporary Git repositories/worktrees/remotes.
3. **Canonical prompt source:** actual canonical Protocol prompt file -> generation/extraction -> packaged wheel resource -> installed renderer.
4. **Packaging:** built wheel installed outside the source checkout.
5. **Namespace/extension composition:** real Python package/entry-point metadata with an installed sibling/extension fixture distribution.
6. **Privacy/remote truth:** final rendered prompt and installed stdout, not an intermediate sanitized helper.
7. **Event seam:** actual production render path -> subscribed production event registrar/sink path.
8. **Repository CI:** ordinary repository validation actually invokes Core acceptance and retains existing Protocol checks.

A fake/helper is valid only below/outside the owner under claim. Evidence that could remain green while these owners are broken cannot close the corresponding obligation.

## 7. Implementation sequence

### Stage 1 — Package/contracts/config/Git/workplans

Implement package skeleton, public value/request/response types, composition root, config/project/extension-namespace normalization, Git/worktree/remote observation, and workplan catalog/identity/resolution.

Closure: focused contract/config/Git/workplan/path-safety/remote tests + affected Core regression; no higher-module dependency or persistence.

### Stage 2 — Protocol profile/snapshot/prompt artifact

Implement canonical stage extraction, packaged 5.16 profile/snapshot, workflow descriptor, stage-input classification/binding, local/web prompt context, RunId/fingerprint/result footer, and prompt-rendered subscribed event.

Closure: all-stage canonical parity/input-completeness, source/version rejection, byte-stability, privacy/remote truthfulness, event/result fixtures, offline packaged-profile integration + affected regression.

### Stage 3 — CLI/extension discovery/package/CI closure

Implement complete CLI aliases/diagnostics/doctor/optional clipboard, real entry-point discovery, installed fixture extension integration, docs, package build/install tests, ordinary repository-CI integration, architecture-fitness checks, final accepted-contract reconciliation, final affected regression/integration, and simplification cleanup.

Closure: isolated installed-wheel end-to-end acceptance on representative temporary repositories plus ordinary repository validation on final candidate; ready for independent Review.

## 8. Frozen versus delegated

### Frozen for WP-1

- parent architecture 1.5.0 module/dependency/ownership direction;
- Core standalone usefulness and one distribution/CLI/composition root;
- public Core API/Application API/Extension SPI method families and semantic roles;
- Core capability set: `prompt.render`, `project.observe`, `workplan.catalog`, `workflow.profile`;
- Python 3.11+ initial floor;
- config/project/extension-namespace ownership and deterministic project selection;
- non-mutating Git/remote observation;
- deterministic remote selection/web-target truthfulness;
- exact workplan selector/branch-binding/ambiguity semantics;
- Protocol-version-bound source/profile/snapshot resolution;
- canonical stage-body extraction and one prompt authority;
- stage input classification and required-user-input table;
- local/web privacy boundary and bounded secret guarantee;
- RunId/fingerprint/result-envelope contract class;
- one extension registry, explicit event subscription, and non-durable prompt event;
- no Tracker/Adapter/benchmark/meter/predictor/Scheduler implementation in Core.

### Delegated to Implementation

- private module/class/function decomposition;
- PEP 517 build backend/test runner;
- concrete Git plumbing satisfying frozen semantics;
- bounded parser implementation;
- exact safe input-scalar representation, lifecycle semantic-digest exclusion list, and public field spelling **only until WP-1 Review freezes the v1 fixtures**;
- diagnostic presentation and numeric exit-code mapping from `Problem.code`;
- optional clipboard implementation;
- focused dependency substitutions that preserve the contract with less complexity.

### Design reopen triggers

Reopen only the affected surface if evidence shows that:

- Core API/SPI cannot support Tracker/Adapter direction without private/reverse dependency;
- required Protocol workflow/profile facts cannot be exposed without a materially different ownership model;
- canonical prompts cannot be packaged offline without creating competing authority;
- target workplan conventions systematically cannot fit exact/conservative resolution;
- one extension registry/subscription seam cannot safely compose required later modules;
- non-mutating observation cannot establish the required target identity;
- web/local privacy/remote truthfulness cannot be preserved under this prompt-context architecture;
- Python 3.11+ violates an independently required distribution target.

Ordinary parser/library/field-layout/Git-command choices remain Implementation discretion.

## 9. Simplification triggers

Stop and simplify before adding durable machinery if implementation starts creating:

- a second maintained prompt-body set;
- separate local/web renderers rather than one renderer plus context/privacy policy;
- separate CLI/API config semantics;
- multiple extension registries;
- a generic workflow/expression engine;
- persistent event queue/history/database in Core;
- agent/model/account/resource placeholder objects in Core;
- fuzzy workplan/remote heuristic stacks;
- custom semver/TOML/YAML/CLI/package mechanisms where focused maintained libraries already own the need;
- public records leaking private implementation objects;
- generic secret scanners presented as a correctness guarantee;
- remote observation implemented by mutating the repository;
- generic `--input` capable of overriding first-class identity/context;
- a second CI workflow duplicating ordinary repository validation without a real isolation need.

## 10. Independent Design review closure — 2026-09-07

This pass re-reviewed WP-1 against the frozen parent architecture, the remote Protocol 5.16 `software-design` role, workflow/workplan authority, testing/proxy-proof acceptance, architecture/active-simplicity doctrine, protocol versioning, long-horizon architecture fitness, Python packaging guidance, configuration rules, security/trust boundaries, release/distribution guidance, repository instructions, and the canonical workflow-prompt source.

The review closed the remaining material gaps:

1. added explicit required-user-input semantics for **every** canonical stage so the product cannot claim a copy/paste-ready prompt while leaving unresolved human placeholders;
2. defined deterministic Git remote selection and web-target availability, including multi-remote/local-only/detached-head failure cases;
3. separated truthful Core secret guarantees from impossible arbitrary-secret detection over user-authored prompt data;
4. made absent-extension configuration forward-compatible and non-authoritative to Core prompt identity;
5. converted prompt events from implicit broadcast to explicit event-type subscription, limiting sensitive complete-prompt delivery to authorized sinks;
6. completed public API/SPI reachability with Application/observation/extension/event and remote records rather than allowing private types to leak through public signatures;
7. added real namespace coexistence, extension dependency-cycle, and installed entry-point acceptance;
8. required deterministic structure-safe input serialization so multiline/control-bearing values cannot corrupt the canonical INPUT block;
9. bound web-mode success to a remotely addressable, non-local target while retaining truthful cached/unknown freshness semantics;
10. clarified that unrelated extension configuration and volatile observation metadata do not perturb prompt identity.

Snapshot-loss counterfactual: with prior chat and Git history removed, the parent architecture, this workplan, and the supplied Protocol 5.16 source/reference tree recover every still-binding WP-1 problem invariant, Frozen architecture decision, public API/SPI role, required stage input, non-goal, real acceptance boundary, and Design-reopen trigger.

**Design verdict: PASS — WP-1 Prompt Module + Core Program is snapshot-complete, internally coherent, and ready for `software-implementation`.**
