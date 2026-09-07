---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-SEMIAUTOMATIC-WORKFLOW-CONTROL
protocol_version: 5.16.0
orchestrator_target_version: 0.1.0
status: active
base_commit: 3715a7e34c10c1735347cd3ee8e2b75c8a2eed55
---

# Protocol Orchestrator — Semi-Automatic Workflow Control Workplan

## Objective / problem invariants / non-goals

### Original problem

Protocol 5.16 provides a canonical parameterized human-facing prompt reference, but executing it still requires the user to select a stage, find the current workplan/branch/candidate, substitute prompt inputs, remember prior stage outcomes, decide what comes next, copy the prompt into an agent, and manually reconstruct workflow state afterward. This bookkeeping is repetitive, error-prone, and especially awkward when work alternates between web agents that can only operate on a remote repository and local coding agents that can directly manipulate a local worktree.

The product problem is therefore to provide a **local, privacy-preserving workflow orchestrator** that turns the protocol's existing stages into an executable control surface while preserving the protocol's authority boundaries. The orchestrator should make the common path approximately:

```text
sdp status
sdp next
# or explicitly:
sdp design
sdp implementation --run
sdp review
```

A stage command must render a directly usable prompt with the relevant repository/workplan/protocol variables resolved from current evidence. In manual-web mode it should make copy/paste I/O effectively one action in each direction. In local-agent mode it should be able to invoke supported agent CLIs, stream the user-visible result, capture structured completion metadata, reconcile the repository afterward, and preserve a private local history.

### Tier-1 product invariants

1. **Protocol authority remains outside the orchestrator.** Product/problem truth, Frozen architecture, workplan semantics, implementation behavior, and Design/Implementation verdicts continue to come from the target repository, governing workplans/specifications, protocol skills, and the agents/users acting in those roles. The orchestrator may observe, remember, reconcile, and recommend; it must not silently invent or override product/Frozen authority.
2. **Current repository evidence beats stale local history.** On every material command, the orchestrator reconciles its private history against the configured target repository, Git state, current workplans, and relevant remote refs. A stale database row must never silently override an active/archived workplan, branch, candidate, or repository fact.
3. **History is private local state.** Prompts, pasted responses, agent final responses, run metadata, inferred workflow state, backend session IDs, and optional raw event logs must live outside both the protocol repository and the target software repository by default. No transcript/history artifact may be committed merely because orchestration is enabled.
4. **One workflow semantics, multiple transports.** Manual web, Claude CLI, Codex CLI, Pi, OMP, and Antigravity must consume the same rendered protocol-stage prompt semantics. Backend adapters may change transport, structured I/O, session handling, sandbox flags, and repository target representation; they must not fork the protocol workflow into backend-specific doctrine.
5. **Web and local operation are explicit execution modes.** Web mode describes the remote repository/branch/candidate and assumes repository access occurs through remote tools/connectors. Local mode describes the configured local worktree and allows the local agent to work directly there. Local machine paths/private state must not leak into a web prompt unless explicitly requested.
6. **Automatic when evidence is strong; explicit when consequentially ambiguous.** Branch, HEAD, upstream, protocol version, workplan path, known stage history, and similar facts should be inferred automatically. When multiple active workplans or materially different next routes remain plausible, the orchestrator must surface the ambiguity and ask for one bounded selection rather than guess.
7. **Reported agent state is evidence with provenance.** PASS/NO-PASS, completed/pending obligations, blockers, and recommended routing received from an agent are recorded with stage/run/backend/candidate identity. The orchestrator may detect contradictions and mark the state inconsistent, but must not rewrite an agent's reported verdict to manufacture workflow closure.
8. **Prompt generation works without direct agent integration.** A fully useful manual mode is required even when no supported CLI is installed or a web agent is preferred.
9. **Direct local integration is capability-aware and safe by default.** Supported adapters are OMP, Pi, Claude CLI, Codex CLI, and Antigravity CLI. The orchestrator probes the installed executable/capabilities and degrades cleanly rather than assuming flags from a different version. It never defaults to dangerous sandbox/permission bypass modes.
10. **The workflow remains inspectable.** The user can query current project/workplan/stage state, previous stage attempts and verdicts, pending blockers/actions, active/retired workplans, and an ASCII/Mermaid/DOT/JSON workflow graph.
11. **The orchestrator is recoverable.** Deleting its private database/history may lose convenience/history but must not corrupt or redefine the target repository. A fresh bootstrap from Git/workplans must recover the strongest state that repository evidence can establish, reporting UNKNOWN/AMBIGUOUS where history was genuinely private and unrecoverable.

### Explicit non-goals for the initial architecture

- No new lifecycle role or approval authority.
- No replacement for Git, workplans, protocol skills, CI, or agent-native safety systems.
- No mandatory repository-local `.sdp` state directory, workplan ledger, generated manifest, or transcript store.
- No browser DOM automation, credential scraping, or fragile automation of ChatGPT/Claude/Gemini web UIs. Manual web transport is clipboard/stdin/stdout based.
- No cloud orchestration service or multi-user synchronization service.
- No automatic merge/rebase/pull/push solely because a web or local agent changed a branch. Remote/local synchronization is observed and reported; mutation requires explicit delivery policy or user action.
- No requirement to store hidden reasoning/thought channels. By default retain rendered prompts, user-visible final responses, normalized run metadata, and structured stage results; raw event streams are optional.
- No LLM dependency for basic state classification. Deterministic parsing/reconciliation is primary; ambiguous unstructured pasted responses require bounded user confirmation instead of silently invoking another model.
- No requirement for a resident daemon in v0.1. The CLI/database design must allow a later local service/MCP surface without making a daemon mandatory now.

## Frozen high-level architecture and engineering envelope

### A. Product placement and language

The orchestrator is a Python 3.11+ subproject distributed alongside the protocol but logically separable from the skill bundles. The expected repository layout is a dedicated top-level subproject such as:

```text
orchestrator/
  pyproject.toml
  src/sdp_orchestrator/
  tests/
```

The installed console entrypoint is `sdp` (with `python -m sdp_orchestrator` as a fallback). Exact internal module names and optional presentation dependencies are delegated. Prefer the standard library for SQLite, TOML reading, subprocesses, async streaming, JSON, hashing, paths, and compression; add a dependency only when it materially improves correctness/portability more than its maintenance cost.

### B. Authority architecture: repository truth + private journal + derived projection

The orchestrator has three distinct information classes:

```text
TARGET/PROTOCOL REPOSITORY EVIDENCE   (authoritative for repository/workplan facts)
              +
PRIVATE APPEND-ONLY OBSERVATIONS/RUNS (historical evidence, not product authority)
              |
              v
DERIVED CURRENT WORKFLOW PROJECTION   (recomputed/reconciled view)
```

Do **not** implement a mutable `current_state` database row as an independent source of truth. Current state is produced by a deterministic reconciliation/reducer over:

- present Git/worktree/upstream/remote observations;
- present active/archive workplan observations and content hashes;
- protocol source/version observations;
- recorded stage runs/results and explicit user selections/overrides.

A cache of the projection is allowed only if it is invalidated/reconciled before use.

### C. Canonical prompt ownership

`source/shared/references/development-workflow-prompts.md` remains the canonical human-facing stage prompt text. The orchestrator must not maintain independent prose copies of Design/Implementation/Review/etc. prompts.

A strict prompt loader extracts stage blocks and their `INPUTS` definitions from the configured protocol source/version. The renderer substitutes concrete values into those input lines and may wrap the canonical stage prompt with two transport-level additions:

1. a compact **ORCHESTRATOR_CONTEXT** block containing derived, explicitly non-authoritative current state/evidence; and
2. a compact **ORCHESTRATOR_RESULT** output contract requesting machine-readable completion metadata.

Executable parity tests must fail if the supported stage registry no longer maps one-to-one to the canonical prompt blocks or expected input variables.

### D. Project configuration and private state placement

Use a local TOML configuration with support for multiple named projects. Default locations follow the host platform's user config/state conventions. A project profile minimally identifies:

- local repository path;
- Git remote name/URL policy and default/main branch as needed;
- workplan active/archive globs (defaulting to `workplans/active/**/*.md` and `workplans/archive/**/*.md` when present);
- protocol source/path/remote/ref policy;
- operation mode (`hybrid`, `web`, `local`);
- per-stage backend routing overrides;
- privacy/retention settings;
- optional delivery/sandbox/backend executable settings.

Machine-specific paths and secrets stay in local configuration. Do not require a repository-local config file. A repo-local non-secret hint file may be considered later only if it materially improves portability and remains optional.

Private state defaults to a per-project directory under the user's state directory, with owner-only permissions where the platform supports them. SQLite is the metadata/event/run store. Optional high-volume raw event streams may be stored as bounded compressed files in the same private state root and referenced from SQLite rather than bloating the database.

### E. Workplan discovery and selection

Every reconciliation scans configured active/archive workplan locations and parses at least the simple frontmatter fields used by the protocol (`workplan_id`, `protocol_version`, `status` where present) plus path/content hash.

Active workplan selection precedence is:

1. explicit command-line workplan selection for the current command;
2. a still-valid user pin recorded in private state;
3. an unambiguous branch/workplan association from current repository evidence and prior recorded association;
4. exactly one active candidate;
5. otherwise `AMBIGUOUS` with a bounded candidate list and a `sdp use <workplan>` action.

Do not choose among multiple materially plausible active workplans merely by mtime. Heuristics may rank candidates for presentation but not silently establish authority.

Archived/retired workplans are tracked from present archive state plus historical observations. If an observed workplan disappears entirely, report that fact rather than silently treating it as archived.

### F. Workflow/state model

The protocol stage registry includes at least:

- baseline/change-health;
- design/workplan;
- implementation;
- review/update;
- verification;
- stabilization/architecture-GC;
- downstream alignment;
- health audit;
- closeout.

A stage attempt has normalized execution status (`pending`, `running`, `completed`, `failed`, `cancelled`, `blocked`, `unknown`) and, where the stage emits one, a reported outcome (`pass`, `no_pass`, `action_required`, `complete`, `not_applicable`, `unknown`). Keep execution status separate from semantic verdict.

Current project/workplan projection exposes:

- selected/ambiguous/no active workplan;
- local branch, HEAD, dirty-state fingerprint, upstream and divergence;
- observed remote branch HEAD when available;
- protocol version/source identity;
- most recent stage attempts and outcomes;
- completed stage history;
- open blocker summaries and classification;
- completed/pending obligation locators reported against the current workplan content hash;
- current recommended stage/action and why;
- contradictions/stale evidence/unknowns.

`UNKNOWN` and `INCONSISTENT` are first-class states. The reducer must not force a clean stage simply to keep the graph moving.

### G. Result contract and response ingestion

Every generated prompt asks the agent to finish its ordinary human-readable response with a compact machine-readable result object. The exact JSON schema is delegated, but it must be versioned and include enough information to normalize:

- schema version;
- stage;
- reported outcome/verdict;
- reported recommended next stage/action;
- workplan identity/path if known;
- candidate branch/HEAD/remote commit identity if known;
- blocker list with routing class (for example implementation nonconformance, design/workplan deficiency, missing evidence, independent issue);
- completed and pending obligation locators/summaries;
- checks/evidence actually executed or unavailable;
- changed planning/product artifacts claimed by the agent;
- concise human summary.

The orchestrator stores **reported** routing separately from its **derived** routing. If the two conflict materially, status becomes inconsistent/needs-confirmation rather than silently choosing one.

Manual-web ingestion accepts stdin, file, or clipboard text. Parsing order is:

1. explicit structured result block;
2. conservative deterministic extraction of strong stage/verdict markers;
3. bounded user confirmation when ambiguity remains.

Pasted agent text is data. Never execute commands, code, paths, or instructions extracted from a pasted response merely because they appear in the response.

### H. Prompt rendering by operation mode

One renderer produces the canonical stage prompt; a transport context controls repository/protocol representation.

**Local mode**:
- repository target identifies the local configured worktree plus branch/candidate;
- `PROTOCOL_SOURCE` normally uses compatible local-first resolution;
- additional constraints state that repository work occurs in the configured local worktree and remote mutation follows explicit delivery policy.

**Web mode**:
- repository target uses configured remote repository URL/name, remote branch, and remote candidate identity; do not expose local absolute paths/private state;
- protocol source should prefer an explicit remotely readable canonical protocol source/ref when configured, avoiding a pointless local-first probe that a web-only agent cannot perform;
- additional constraints state that repository inspection/mutation must occur through authorized remote tools/connectors and that local execution/filesystem access must not be assumed.

**Hybrid mode** selects web/local transport per stage policy but otherwise uses the same state/rendering pipeline.

### I. Backend architecture

Implement a thin `BackendAdapter` capability boundary rather than backend-specific workflow logic. Each adapter reports/probes capabilities such as:

- executable/version identity;
- one-shot/headless execution;
- streaming structured events;
- structured final output/schema support;
- resumable session identity;
- working-directory control;
- sandbox/permission controls;
- RPC/SDK mode where worth using.

The initial supported local backends are:

- Claude CLI / Claude Code;
- Codex CLI;
- Pi;
- OMP (Oh My Pi);
- Antigravity CLI.

The implementation should prefer a stable machine-readable/headless interface exposed by the installed version. Current verified capability examples include Claude print mode with JSON/stream-JSON, Codex `exec` JSONL, Pi JSON/RPC modes, OMP one-shot plus RPC/SDK/ACP integration, and Antigravity headless stream-JSON / programmatic session support. These current flags are implementation evidence, **not Frozen permanent CLI syntax**: adapters must probe/version-gate and fail clearly or degrade to manual prompt generation when unsupported.

Do not create five independent state machines. Backend-specific logic ends at prompt delivery, event normalization, cancellation/session handling, and result extraction.

### J. Manual web transport and clipboard ergonomics

`manual-web` is a first-class backend, not a failure mode. A stage command in web mode should:

1. reconcile state;
2. render the fully populated prompt;
3. print it;
4. copy it to the system clipboard when a safe supported clipboard mechanism is available;
5. print one short instruction for response ingestion, e.g. `sdp ingest --clipboard`.

Clipboard support should use a bounded platform adapter with graceful fallback to stdout; do not introduce browser automation. OSC52/native clipboard command support may be used when justified. Never overwrite clipboard data without clearly reporting that copying occurred.

### K. Local execution and process safety

Local adapters execute with direct argv/process APIs (`shell=False` semantics), target repository as cwd, explicit timeouts/cancellation, and bounded streaming. The orchestrator records pre/post repository identity independently of the agent's claims.

Default execution must not add `--dangerously-*`, `--yolo`, unrestricted sandbox bypass, or equivalent permission-bypass flags. Backend-specific sandbox/permission policy is configurable, capability-probed, and reported. Secrets/environment values needed by an agent may be inherited/passed according to configuration but are never serialized into prompts, command logs, database records, or diagnostics.

Cancellation should propagate cleanly to the owned process/session with bounded escalation. Output capture must be streaming/bounded rather than accumulating an unbounded transcript in RAM.

### L. Remote/local synchronization model

The orchestrator distinguishes:

- local worktree HEAD/status;
- local tracking ref;
- observed remote branch HEAD.

After a web-agent response is ingested, refresh remote identity through safe Git remote observation/fetch policy and report whether the remote branch advanced. Do not automatically merge/rebase/pull the local worktree. After a local-agent run, report local changes and whether they are ahead/behind the configured remote; pushing remains an explicit/configured delivery action.

This distinction prevents web-mode remote commits from being mistaken for local changes and vice versa.

### M. Workflow graph and recommendation engine

The canonical stage graph is a small deterministic registry reflecting Protocol 5.16 stage semantics, including conditional edges (Review NO-PASS -> Implementation repair or bounded Design reconsideration; Verification blocker -> route by classification; Stabilization action -> normal Design/Implementation cycle; Closeout terminal; Health Audit outside the per-change linear path).

The graph renderer combines this allowed graph with actual recorded attempts/outcomes. Support at least:

- terminal ASCII;
- Mermaid;
- Graphviz DOT;
- JSON.

No Graphviz installation is required merely to emit DOT. The current/recommended node, completed attempts, blockers, skipped/not-applicable stages, and loops should be representable.

The recommendation engine is deterministic from reconciled state + recorded stage outcomes. It proposes text such as `Review passed; Verification is not currently required; next recommended action: Stabilization or Closeout according to project policy.` It does not claim correctness itself.

### N. Privacy and retention

By default store:

- rendered prompts;
- user-visible final agent responses;
- structured result metadata;
- backend/run/session identifiers;
- Git/workplan/protocol observations needed for history.

Raw streaming tool/event logs are configurable and should default off unless needed. Do not persist hidden reasoning/thought channels by default even if a backend exposes them. Implement redaction hooks for secrets and allow project history export/purge/retention controls. State directories/databases/logs should use owner-only permissions where practical.

Future optional encryption-at-rest may be added behind a clean storage interface, but v0.1 must not invent custom cryptography. OS/disk encryption plus strict local file permissions is the baseline; if application-level encryption is later added, use a maintained cryptographic/keyring facility.

### O. Future local service / MCP extension boundary

The core state/reconciliation/render/run APIs must be callable independently of the CLI so a later local service can expose structured operations such as `get_state`, `render_prompt`, `report_stage_result`, and `get_next_action` through MCP or another supported local IPC mechanism. Do not require this service for v0.1 and do not let MCP-specific data models become the core architecture.

## Implementation obligations and delegated solution space

### O1 — Package skeleton and canonical core API

**Concern / rationale:** The orchestrator must be installable and usable independently of a protocol-repository checkout while remaining version-coherent with the prompt source it renders.

**Required end state:** Provide an installable Python package/console entrypoint with separated core services for configuration, repository observation, workplan discovery, reconciliation, prompt loading/rendering, history storage, result ingestion, graph/status projection, and backend execution.

**Delegated solution space:** Exact module decomposition, CLI library, optional presentation library, and packaging helper choices.

**Acceptance evidence:** package install/import smoke; `sdp --help`; unit tests demonstrating the CLI delegates to the same core APIs used by programmatic callers.

### O2 — Canonical configuration resolution

**Required end state:** One resolved project configuration path with clear precedence: defaults -> local config/project profile -> environment allowlist if supported -> CLI overrides. Record provenance for material resolved values. Support multiple named projects and automatic project selection from cwd when unambiguous.

Do not persist credentials. Reject invalid/missing repo paths and incompatible backend/mode settings before execution.

**Acceptance evidence:** precedence, multi-project selection, path normalization, invalid combination, secret-redaction tests.

### O3 — Git/repository observer

**Required end state:** A read-only observer returns local root, branch/detached state, HEAD, dirty/staged/untracked summary/fingerprint, upstream, ahead/behind, remote URL/name, and safely observed remote head when requested. It must not parse human-formatted Git output when a machine format is available.

**Acceptance evidence:** clean/dirty/detached/no-upstream/ahead/behind/remote-advanced fixtures using temporary Git repositories.

### O4 — Workplan catalog and safe active-workplan selection

**Required end state:** Discover active/archive workplans, parse required frontmatter, compute content hashes, retain observed lifecycle history, and apply the Frozen selection precedence. Provide `sdp workplans` and `sdp use`.

**Anti-shortcut:** multiple plausible active workplans must not silently collapse to newest-mtime.

**Acceptance evidence:** zero/one/multiple active plans, valid pin, stale pin, branch-affinity, archived/moved/deleted plan scenarios.

### O5 — Private durable history and migrations

**Required end state:** SQLite schema with explicit migration/versioning supports project identity, repository/workplan observations, stage runs/results, user selections/overrides, rendered prompt/final response retention metadata, and optional external raw-log references. Current workflow state is derived, not owned by a mutable DB field.

Use transactions and safe concurrent-reader/single-writer behavior. Database/history removal must not damage repository state.

**Acceptance evidence:** migration tests; interrupted write rollback; reopen/reconcile; purge/retention; DB absent/corrupt/recreated behavior with truthful history loss reporting.

### O6 — State reconciler and recommendation reducer

**Required end state:** Deterministically combine current repo/workplan/protocol evidence with historical stage results. Expose UNKNOWN/AMBIGUOUS/INCONSISTENT explicitly. Compute next recommended stage/action without pretending to be a semantic reviewer.

Agent-reported verdict/routing and derived routing remain separately inspectable.

**Acceptance evidence:** table-driven lifecycle transitions including Design PASS -> Implementation, Review NO-PASS implementation defect -> Implementation, Review design deficiency -> Design, Review PASS -> conditional Verification/Stabilization/Closeout, Verification blocker routes, Stabilization action loops, Closeout terminal, and ambiguous/conflicting cases.

### O7 — Prompt loader and renderer

**Required end state:** Load canonical stage blocks from the configured protocol source/version, validate expected stage/input topology, resolve all inputs available from project state, preserve explicit `AUTO`/`NONE` only when intentionally unresolved, add mode-specific transport context and result contract, and render deterministic prompt text.

The renderer must not expose local paths/private state in web mode.

**Acceptance evidence:** golden tests for every stage in local and web modes; parity failure when canonical prompt inputs/stages drift; protocol-version mismatch/non-readable source behavior; snapshot showing web prompt contains remote repo/branch but no local absolute repo/state paths.

### O8 — First-task/design gap handling

**Required end state:** A new task description that does not yet exist in repository authority can be supplied once through `sdp start <task>` or `sdp design --task ...` and retained privately as pending design context. If no active workplan and no task evidence exist, Design prompt generation must request that one genuinely missing input rather than fabricate a task.

If an active workplan already exists, Design/Review/Implementation context derives from it as applicable.

**Acceptance evidence:** fresh project/no task -> bounded error; `sdp start` -> Design renders; existing workplan -> no redundant task request.

### O9 — Structured result contract and ingestion

**Required end state:** Versioned result schema, extraction from local backend final output/manual pasted response, normalized run record, conservative fallback parser, and user confirmation on ambiguous verdict/routing.

Completed/pending obligation references are tied to the workplan content hash that was current for the run; later workplan changes mark those observations stale until reconciled.

**Acceptance evidence:** valid/invalid/missing result block, conflicting text versus JSON, ambiguous PASS wording, changed-workplan invalidation, malicious pasted shell/code text stored as inert data.

### O10 — CLI workflow surface

**Required end state:** At minimum:

```text
sdp init / config
sdp status [--json]
sdp next [--copy] [--run]
sdp baseline
sdp design
sdp implementation
sdp review
sdp verification
sdp stabilization
sdp alignment
sdp health
sdp closeout
sdp ingest [--stdin|--clipboard|FILE]
sdp history
sdp workplans
sdp use <workplan>
sdp graph [--format ascii|mermaid|dot|json]
sdp backends
sdp sync
```

Stage commands default to prompt generation/copy behavior; `--run` dispatches through routing/backend policy. Exact aliases are delegated.

**Acceptance evidence:** end-to-end CLI tests over a temporary project with deterministic fake backend.

### O11 — Manual-web transport

**Required end state:** Web-mode prompt rendering, clipboard copy with graceful fallback, one-command ingestion of copied response, remote-ref refresh/report, and no local-path leakage.

**Acceptance evidence:** clipboard adapter tests with fake platform adapter; web render privacy test; remote-advanced reconciliation test; no-browser-automation structural check.

### O12 — Backend adapter interface and capability probes

**Required end state:** One backend protocol plus normalized event/result model. Probe executable/version/help/capabilities cheaply. Unsupported/missing adapters report concrete capability failure and allow manual prompt fallback.

**Acceptance evidence:** fake backend matrices; version/capability mismatch; missing executable; structured-stream normalization; cancellation/error status mapping.

### O13 — Claude, Codex, Pi, OMP, and Antigravity adapters

**Required end state:** Direct local execution support for all five named backends through their supported machine-readable/headless/RPC interfaces as available in the installed version. Each adapter sets cwd to the target repo, streams user-visible output, captures a final response/result, records session identity when available, and respects configured permission/sandbox policy.

Fresh-context Review/Verification should default to a new backend session unless the user explicitly requests continuation; implementation repair loops may resume when the backend supports it and the project policy prefers continuation.

**Acceptance evidence:** adapter command-construction tests, help/version probe fixtures, event-parser fixtures from each backend, and opt-in live smoke qualification when the CLI/authentication is available. CI must not require paid credentials.

### O14 — Hybrid routing policy

**Required end state:** Project config can set global `web`, `local`, or `hybrid` mode plus per-stage backend policies. The shipped default hybrid profile should reflect the intended economics:

- Design/Review/Verification/Stabilization: manual web by default;
- Implementation: local agent by default;
- Baseline and Health Audit: local by default because repository/history/tooling intensity is usually high;
- Closeout: local by default because it performs repository/documentation/hygiene writes;
- Alignment: configurable, with web as a reasonable default because it is primarily semantic/workplan editing.

These are defaults, not protocol authority. If the configured local backend is unavailable, report/fallback according to user policy instead of silently choosing a different paid provider.

**Acceptance evidence:** routing matrix tests and explicit override tests.

### O15 — Local process lifecycle, safety, and resource bounds

**Required end state:** Direct argv execution, no shell interpolation, bounded stdout/stderr handling, cancellation escalation, no secret logging, no default dangerous permission bypass, configurable timeouts, and pre/post Git snapshots.

**Acceptance evidence:** hanging child cancellation, large-output streaming, nonzero exit, interrupted run, secret-looking env value absent from DB/logs, and pre-existing dirty-worktree attribution tests.

### O16 — Privacy, transcript retention, export, and purge

**Required end state:** Configurable storage of prompt/final response/raw events, raw events off by default, private permissions, redaction hook, retention policy, project history export, and secure logical purge. Do not copy history into either repository during export unless the user explicitly names such a destination and accepts the privacy consequence.

**Acceptance evidence:** permission tests where supported; retention/purge; raw-events disabled; redaction; export destination safeguards.

### O17 — Status/history/workplan/graph UX

**Required end state:** `status` presents current project, selected workplan, branch/candidate/upstream/remote relation, last stage/outcome, blockers, stale/ambiguous evidence, and one recommended next command. `history` shows stage attempts chronologically. `workplans` separates active/retired/ambiguous. `graph` highlights actual/current/recommended stage state.

**Acceptance evidence:** deterministic text/JSON snapshots and representative loop/blocked/unknown graphs.

### O18 — Remote/local reconciliation without surprise mutation

**Required end state:** `sdp sync` safely refreshes observations and explains local-vs-remote divergence. Fetch/ls-remote behavior is explicit/configurable. Fast-forward/push/merge/rebase remain separate explicit actions/policies and are not hidden inside status/prompt generation.

**Acceptance evidence:** web remote commit appears as remote advancement; local commit appears as local advancement; divergence detected; no implicit worktree update.

### O19 — Documentation and distribution

**Required end state:** User documentation covers install (preferably pipx/isolated CLI install), project registration, manual web round-trip, hybrid routing, local backend probes/configuration, privacy/state locations, backup/purge, graph/status interpretation, and troubleshooting. Architecture documentation explains authority boundaries and why DB history is non-authoritative.

The protocol README/prompt reference should point to the orchestrator as an optional convenience layer without making it a lifecycle requirement.

### O20 — Future MCP/service extension seam

**Required end state for v0.1:** Core APIs remain independently callable and do not depend on terminal rendering. Define but do not necessarily ship the stable application operations needed for a later `sdp mcp`/local service: state query, prompt render, stage-result report, next-action query.

**Non-goal:** no mandatory daemon/MCP service in the first release.

## Implementation authority

### Frozen

- The orchestrator is a local control plane/history/recommendation tool, not a new protocol authority.
- Canonical stage prompt prose remains owned by `development-workflow-prompts.md`; no parallel backend-specific prompt copies.
- Current workflow state is reconciled from repository evidence plus private historical evidence; stale DB state cannot override current repository/workplan facts.
- Private history/transcripts live outside the protocol and target repositories by default.
- Web/local modes have distinct repository visibility/mutation assumptions and web prompts do not leak local paths/private state.
- One backend-adapter boundary serves OMP, Pi, Claude CLI, Codex CLI, Antigravity CLI, and manual web transport.
- SQLite-backed local persistence with versioned migration is the v0.1 durable metadata/history mechanism; exact table decomposition is delegated.
- Python 3.11+ is the implementation runtime for v0.1.
- Browser automation and a mandatory resident service are excluded from v0.1.

### Delegated

- Exact Python module/classes/functions and CLI framework.
- Exact SQLite table names/indexes, provided authority/state separation and migration semantics hold.
- Exact clipboard implementation and optional presentation dependency.
- Exact backend invocation flags for a probed supported version.
- Whether Pi/OMP/Antigravity use one-shot structured subprocess, RPC, or SDK internally when equivalent behavior is maintained.
- Exact text styling, graph glyphs, aliases, and optional TUI additions.
- Exact compression format for optional raw event logs.

### Reopen only on evidence

Reopen affected Design only if implementation evidence shows one of these Frozen choices is not viable:

- canonical prompt Markdown cannot be parsed/versioned robustly without creating unacceptable coupling; a structured canonical prompt source may then be reconsidered, but only if it becomes the single source that also generates the human reference rather than a competing authority;
- SQLite cannot meet the required local concurrency/recovery/privacy envelope without a different local storage architecture;
- a named supported backend lacks any stable automatable interface and cannot be safely supported through an adapter/fallback;
- Python materially prevents required portability/integration/performance for the orchestrator's actual workload;
- manual clipboard transport cannot provide the required web-mode privacy/usability on a supported platform and a different explicit user-mediated transport is required.

## Affected surface and task-specific acceptance

Expected protocol-repository surfaces:

- new `orchestrator/` subproject/package/tests;
- root and/or orchestrator documentation;
- optional small links from `README.md`, `source/README.md`, and `development-workflow-prompts.md` explaining the convenience layer;
- release/distribution configuration if the package is published;
- CI additions for orchestrator unit/integration/package tests.

The existing skill bundles and canonical prompt semantics should remain unchanged except for explicitly justified integration/documentation hooks. Do not package private project state into `dist/`.

### Real semantic-owner acceptance boundaries

1. **Prompt correctness:** real owner is the orchestrator prompt loader/renderer operating on the canonical protocol prompt source. A hand-written expected prompt that bypasses the loader cannot establish parity.
2. **State correctness:** real owner is the reconciler operating on actual Git/workplan observations plus recorded events. Tests that seed a final `current_state` object bypass the claim.
3. **Backend execution:** real owner is the backend adapter/process/event normalization path. Unit command construction alone is not enough; use deterministic fake subprocess/event streams and optional live smoke qualification.
4. **Privacy:** real owner is the rendered web prompt + persistence layer. Prove no local path/secret/raw-event persistence under the relevant configuration, not merely that a redaction helper works in isolation.
5. **Manual web round-trip:** real owner is render -> clipboard/stdout -> ingest -> reconcile. Test the assembled path with fake clipboard/remote observations.

### Required regression/integration evidence

- unit tests for config, Git parser/observer, workplan parser/selection, DB/migrations, reducer, prompt extraction/rendering, result schema/parser, graph generation, clipboard, routing, and each backend adapter;
- temporary-repository integration tests for active/archive workplans, branch/upstream/divergence, local and simulated remote advancement;
- end-to-end fake-backend stage loop covering Design -> Implementation -> Review NO-PASS -> Implementation -> Review PASS -> Closeout with preserved history;
- web-mode end-to-end render/ingest flow with local-path non-disclosure;
- package installation and console-entrypoint smoke;
- full existing protocol regression/package validation so the optional orchestrator does not disturb skill distribution parity;
- live backend qualification is conditional on installed/authenticated CLIs and must be skip-with-reason rather than a CI credential requirement.

Production qualification: unnecessary for v0.1 beyond bounded latency/storage sanity; this is a local control-plane CLI, not a throughput-heavy production service. Record representative startup/status/prompt-render latency and ensure history queries remain interactive for a realistic local run count.

## Implementation sequence and genuine redesign / simplification triggers

### Stage 1 — Core model, config, observers, and private history

Implement package skeleton, resolved config, Git/workplan observation, SQLite migrations, event/run persistence, and reconciler with UNKNOWN/AMBIGUOUS/INCONSISTENT semantics. Close with temporary-repo integration tests.

### Stage 2 — Canonical prompt rendering + manual web workflow

Implement canonical prompt extraction, mode-specific variable resolution, result contract, clipboard/stdin ingestion, `start/use/status/next/stage/ingest/history/workplans/graph` core CLI, and web/local privacy separation. This stage should already deliver substantial value with no installed agent CLI.

### Stage 3 — Local backend execution framework

Implement adapter protocol, probes, safe subprocess/event streaming/cancellation, fake backend, and routing. Close with backend-independent integration tests.

### Stage 4 — Five supported backend adapters

Add Claude, Codex, Pi, OMP, and Antigravity adapters one by one using the same capability contract. Each adapter must close its parser/probe/command tests before the next is added; do not let one vendor force backend-specific workflow state into the core.

### Stage 5 — Hybrid policy, remote/local reconciliation, privacy hardening, docs/package closure

Finish default hybrid routing, session continuation/fresh-review policy, retention/export/purge, remote observations, documentation, install/release mechanics, full protocol regression, and end-to-end acceptance.

### Future extension — MCP/local service/TUI

Only after the CLI/core model is stable, consider `sdp mcp`, a local dashboard/TUI, agent callbacks, richer live event views, or SDK-native integrations. These should reuse the core APIs and replace transport friction rather than introduce a second orchestrator state machine.

### Active simplification triggers

Before adding another durable adapter/workflow layer, simplify if implementation begins to show:

- backend-specific copies of stage prompts or state-transition logic;
- both mutable `current_state` tables and event/repository reconciliation competing for authority;
- duplicated local/web project models instead of transport-specific views of one project state;
- multiple workplan parsers/discovery paths;
- raw transcript files plus duplicate full transcript blobs in SQLite without measured need;
- wrapper-on-wrapper process execution or per-backend retry/cancellation frameworks that can collapse into the adapter contract;
- a daemon/MCP/TUI being introduced solely to work around an unclear core API.

### Genuine Design-reopen triggers

Reopen only the affected Frozen decision if evidence shows canonical prompt ownership, local-storage architecture, Python runtime, explicit web/local boundary, or single adapter abstraction cannot meet the product invariants. Do not reopen architecture merely because a backend changes CLI flags or a particular clipboard utility is unavailable.

## Design verdict

**PASS — implementation-ready.**

The design closes the major gaps in the initial proposal: it prevents the private history DB from becoming a competing source of truth; defines safe ambiguity handling for multiple active workplans and first-time Design tasks; separates web-remote and local-worktree identities; makes agent output machine-ingestible without trusting arbitrary pasted text; keeps one canonical prompt pipeline across transports; provides capability/version probing instead of brittle vendor CLI assumptions; establishes privacy/retention boundaries; and gives direct local backend integration a stable extension boundary without requiring a daemon or browser automation.
