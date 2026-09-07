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

Protocol 5.16 has a canonical parameterized workflow-prompt reference, but the user still has to select a stage, discover the current workplan/branch/candidate, substitute inputs, remember prior PASS/NO-PASS outcomes, decide what comes next, move prompts/results between agents, and reconstruct workflow state afterward. This bookkeeping is especially awkward when semantic work happens in a web agent against a remote Git repository while implementation happens in a local coding agent against a local worktree.

Build a **local, privacy-preserving protocol orchestrator** that turns those stages into an executable control surface. The common path should approach:

```text
sdp status
sdp next
# or explicitly
sdp design
sdp implementation --run
sdp review
```

A stage command renders a directly usable canonical protocol prompt with repository/workplan/protocol variables resolved from current evidence. Manual-web mode makes prompt copy and response ingestion one-step operations. Local mode can invoke supported agents, stream user-visible output, ingest structured completion metadata, reconcile the repository afterward, and preserve private history.

### Tier-1 product invariants

1. **The orchestrator is not protocol authority.** Product/problem truth, Frozen architecture, workplan meaning, implementation behavior, and Design/Implementation verdicts remain owned by governing repository artifacts, protocol skills, and the agents/users acting in those roles. The orchestrator observes, remembers, reconciles, transports, and recommends; it must not silently invent or override product/Frozen authority.
2. **Current repository evidence outranks stale local history.** Every material command reconciles private history with present Git/worktree/upstream/remote observations and present active/archive workplans. A stale database record cannot silently override a repository fact.
3. **Private history stays private and local.** Prompts, pasted/final responses, structured stage results, backend/session metadata, and optional raw event logs live outside both the protocol repository and target software repository by default.
4. **One workflow semantics, multiple transports.** Manual web, Claude, Codex, Pi, OMP, and Antigravity consume the same rendered protocol-stage semantics. Transport adapters may differ in process/RPC/SDK protocol, structured I/O, session handling, permissions, and repository representation; they must not fork protocol doctrine.
5. **Web and local operation are explicit execution modes.** Web mode identifies the remote repository/branch/candidate and assumes remote tools/connectors. Local mode identifies the configured worktree and allows direct local repository work. Web prompts must not leak local absolute paths, private state paths, credential-bearing remote URLs, environment secrets, or machine-private metadata.
6. **Automatic when evidence is strong; bounded choice when consequentially ambiguous.** Branch, HEAD, upstream, protocol version, workplan path, and known stage history should resolve automatically. Multiple materially plausible workplans or routes produce `AMBIGUOUS`/`INCONSISTENT` state and one bounded selection rather than a guess.
7. **Agent results are evidence with provenance.** PASS/NO-PASS, blockers, completed/pending obligations, checks, and routing are stored with stage/run/backend/candidate/workplan/protocol identity. The orchestrator may detect contradictions and staleness but must not rewrite a reported verdict to manufacture closure.
8. **Prompt generation remains useful without direct agent integration.** Manual web is a first-class mode, not an error path.
9. **Direct integration is capability-aware and safe by default.** ACP is preferred when a backend's ACP surface preserves the required capabilities; documented native structured RPC/SDK/JSON is the bounded fallback. Unsupported or incompatible integration degrades clearly to prompt generation. Never default to dangerous permission/sandbox bypass.
10. **Workflow state is inspectable.** Query current workplan/stage, branch/candidate/upstream/remote relation, previous attempts/verdicts, blockers, completed/pending obligation observations, active/retired workplans, stale evidence, and current/recommended action as text/JSON and as a workflow graph.
11. **The private database is disposable convenience state.** Deleting it may lose private history but must not damage or redefine either repository. Fresh bootstrap recovers the strongest state Git/workplans can establish and reports genuinely unrecoverable history as unknown.
12. **Historical transcripts do not become automatic prompt context.** Future prompts receive a compact structured projection of relevant state/blockers, not raw prior agent transcripts. Raw history is injected only by explicit user action. This prevents context bloat, stale authority, and prompt-injection propagation from archived outputs.
13. **Manual result ingestion cannot silently attach to the wrong run.** Every generated prompt carries a non-secret run identity and prompt fingerprint. Structured results echo that identity; ambiguous pasted output requires bounded user selection/confirmation.
14. **Evidence invalidation follows changed dimensions, not timestamps alone.** Workplan semantic changes, candidate changes, protocol changes, and lifecycle-only moves are distinguished so the orchestrator neither reuses stale evidence nor discards still-valid evidence merely because an archive/status field changed.

### Explicit non-goals for v0.1

- No new lifecycle/approval role; no replacement for Git, workplans, protocol skills, CI, or agent-native safety systems.
- No mandatory repository-local `.sdp` ledger/state/transcript directory.
- No browser DOM automation, credential scraping, or brittle automation of ChatGPT/Claude/Gemini web UIs. Web transport is user-mediated clipboard/stdin/stdout.
- No cloud orchestration or multi-user synchronization service.
- No hidden automatic merge/rebase/pull/push. Remote/local synchronization is observed and reported; mutations follow explicit delivery policy.
- No automatic installation/upgrading of agent CLIs, ACP adapters, or registry-discovered binaries.
- No requirement to persist hidden reasoning/thought channels. Store user-visible final responses and normalized metadata by default; raw event streams are optional.
- No LLM dependency for basic state classification. Structured output + deterministic parsing/reconciliation is primary; ambiguous pasted text requires confirmation.
- No mandatory resident daemon/MCP service, generic workflow engine, event-sourcing framework, or TUI in v0.1.
- No orchestrator-managed Git worktree creation/merging or parallel-agent scheduler in v0.1. Multiple independently configured worktrees may be orchestrated as separate project profiles.

## Frozen high-level architecture and engineering envelope

### A. Product placement, runtime, and dependency policy

Implement a Python 3.11+ subproject distributed alongside the protocol but logically separable from skill bundles, e.g.:

```text
orchestrator/
  pyproject.toml
  src/sdp_orchestrator/
  tests/
```

Install console entrypoint `sdp`; retain `python -m sdp_orchestrator` fallback.

Use focused maintained dependencies where they delete meaningful portability/schema/protocol machinery:

- `platformdirs` — cross-platform user config/state/cache roots;
- `typer` — CLI command model and completion; use Rich rendering through Typer or declare `rich` directly only if the package imports Rich APIs itself;
- `pydantic` — versioned configuration, normalized event/result models, validation, and JSON Schema;
- `python-frontmatter` — safe workplan frontmatter parsing; use its safe YAML path and validate the resulting bounded metadata with Pydantic;
- `filelock` — cross-platform private-state project/run lock for long-lived direct-agent execution and migration serialization;
- `pyperclip` — bounded clipboard adapter for manual-web ergonomics, always with stdout/stdin fallback when the platform clipboard is unavailable;
- optional `agent-client-protocol` extra — preferred ACP client implementation for local-agent integration.

Keep `sqlite3`, `tomllib`, `subprocess`, `asyncio`, `json`, `pathlib`, `hashlib`, `uuid/secrets`, and compression on the standard library. Do not add GitPython, a generic FSM/workflow engine, an event-sourcing framework, NetworkX, Jinja2, or an ORM merely for symmetry when the bounded owner is simpler directly.

`tomlkit` is allowed only if v0.1 implements in-place comment-preserving config mutation beyond initial file creation/validation. `markdown-it-py` is allowed only if a strict line/fence parser cannot robustly preserve the canonical prompt blocks. Textual is a future optional TUI dependency, not v0.1 core.

Dependency versions are not Frozen identities. Use deliberate compatible ranges and a reproducible development/test lock. Because ACP SDK releases are pre-1.0, bound the initial supported ACP minor series rather than accepting an unbounded `<1` range; refresh that range only after conformance tests pass. Verify supported Python versions, licenses, source provenance, and dependency changes during release work. The protocol repository is MIT; selected core libraries are permissively licensed, and ACP components are Apache-2.0-compatible dependencies.

### B. Authority model: repository evidence + private journal -> derived projection

```text
TARGET/PROTOCOL REPOSITORY EVIDENCE
              +
PRIVATE APPEND-ORIENTED OBSERVATIONS/RUNS
              |
              v
DERIVED CURRENT WORKFLOW PROJECTION
```

Do not create an independent mutable `current_state` source of truth. Current state is recomputed/reconciled from present Git/workplan/protocol observations plus private stage-run/result/user-selection history. Explicit retention/purge may remove private history; ordinary run records are otherwise immutable evidence. A cached projection is allowed only when invalidated/reconciled before use.

### C. Protocol support, canonical prompt ownership, and source resolution

`source/shared/references/development-workflow-prompts.md` remains canonical prompt prose. Do not hand-maintain backend-specific copies.

The orchestrator uses a strict prompt loader that extracts stage blocks and `INPUTS`, substitutes only declared input values, and preserves the remainder byte-for-byte where practical. It may wrap the canonical block with:

1. compact `ORCHESTRATOR_CONTEXT` (derived, explicitly non-authoritative); and
2. versioned `ORCHESTRATOR_RESULT` schema request carrying `run_id` and `prompt_fingerprint`.

The installed package must work without a protocol-repository checkout. Resolve prompt authority in this order:

1. explicit configured compatible protocol source/ref;
2. version-bound prompt snapshot packaged with the orchestrator, generated from the canonical prompt during build/release and carrying protocol version/source identity;
3. compatible remotely readable canonical protocol source when network use is allowed;
4. truthful non-closure if the required governing version cannot be resolved.

The packaged snapshot is generated transport, not a second editable authority. Build tests prove parity with canonical source.

v0.1 ships a Protocol 5.16 workflow profile and prompt snapshot. It may catalog older/newer workplans, but automatic stage routing/rendering for another governing protocol version requires an explicitly compatible prompt/profile source; it must not silently reinterpret an older workplan through 5.16 semantics merely because the current package contains a 5.16 prompt.

### D. Project configuration and private state

Use local TOML config supporting multiple named projects. Resolve built-in defaults -> local config/profile -> documented environment allowlist if any -> CLI overrides. Parse with `tomllib`; validate the resolved representation with Pydantic. A project profile minimally carries:

- stable local project key and local repository/worktree path;
- remote name/URL policy and main/default branch as needed;
- active/archive workplan globs;
- protocol source/ref/profile policy;
- operation mode (`hybrid`, `web`, `local`) and per-stage route/backend overrides;
- privacy/retention/session policy;
- remote-refresh/network policy;
- optional backend executable/transport/sandbox/delivery settings.

Do not store credentials. Sanitize Git remote URLs before display, persistence, or prompt rendering: strip URL userinfo/tokens and normalize SSH/HTTPS remotes to a safe display identity.

Private state defaults under the user's platform state directory via `platformdirs`, with owner-only permissions where supported. SQLite stores metadata/history. Optional high-volume raw event streams may be bounded compressed files under the same private state root and referenced from SQLite.

### E. Workplan discovery, lifecycle consistency, and semantic identity

Scan configured active/archive workplan locations; parse bounded frontmatter (`workplan_id`, `protocol_version`, `status` and recognized lifecycle metadata), path, exact content hash, and a **semantic authority fingerprint**.

The semantic fingerprint includes the workplan's governing protocol binding and authoritative body while excluding only explicitly recognized lifecycle-only metadata/path changes such as active -> archive relocation or status/completion bookkeeping. A substantive body/authority change must change the semantic fingerprint. Store both exact artifact hash and semantic fingerprint so closeout metadata does not falsely invalidate earlier semantic evidence.

Selection precedence:

1. explicit command workplan;
2. still-valid private user pin;
3. unambiguous branch/workplan association from current evidence + recorded association;
4. exactly one active candidate;
5. else `AMBIGUOUS` and offer `sdp use <workplan>`.

Never silently choose among plausible plans by mtime. An active-path/completed-status or archive-path/active-status contradiction is `INCONSISTENT`, not silently normalized. Track archive/retirement from current files plus historical observations; disappearance is reported as disappearance, not invented archive state.

### F. Candidate identity and evidence invalidation

Candidate identity is stronger than branch name. Observe as applicable:

- repository/project identity;
- local branch or detached state;
- `HEAD` commit;
- source-relevant dirty/staged/untracked fingerprint;
- upstream relation;
- observed remote branch commit;
- observation timestamp/freshness.

Exact fingerprint mechanics are delegated, but a source-relevant working-tree change must alter candidate identity. If a dirty surface cannot be fingerprinted confidently, report identity incomplete rather than pretending a durable candidate exists.

Stage evidence carries the dimensions it depends on. At minimum:

- Baseline binds to the before-candidate identity;
- Design/workplan acceptance binds to protocol identity + workplan semantic fingerprint;
- Implementation completion binds to protocol identity + workplan semantic fingerprint + resulting candidate identity;
- Review/Verification/Stabilization bind to protocol identity + workplan semantic fingerprint + exact reviewed candidate identity;
- lifecycle-only closeout changes may change artifact hash/path without invalidating already valid semantic review evidence when product candidate and semantic fingerprint are unchanged.

The reducer invalidates only evidence whose material dimensions changed. A reported PASS on commit A does not automatically apply to commit B.

### G. Workflow/state model and recommendation engine

Registry stages: baseline/change-health, design/workplan, implementation, review/update, verification, stabilization/architecture-GC, downstream alignment, health audit, closeout.

Separate execution status (`pending`, `running`, `completed`, `failed`, `cancelled`, `blocked`, `unknown`) from semantic outcome (`pass`, `no_pass`, `action_required`, `complete`, `not_applicable`, `unknown`). `UNKNOWN`, `AMBIGUOUS`, `INCONSISTENT`, and `STALE` are first-class projection states.

Projection exposes selected workplan, local branch/HEAD/dirty/upstream/divergence, observed remote head/freshness, protocol identity, recent/completed stage attempts, blocker classifications, completed/pending obligation observations, stale evidence, current recommended stage/action, and machine-readable reason codes.

Maintain a small deterministic **version-bound** stage graph matching the compatible protocol profile. Example 5.16 conditional edges include Review NO-PASS -> Implementation repair or bounded Design reconsideration by finding class; Verification blockers route by class; Stabilization action re-enters normal Design/Implementation cycle; Closeout is terminal for the workplan; Health Audit sits outside the linear per-change path.

Recommendations are derived advice, not semantic verdicts. Record recommendation snapshots/reason codes for history, but recompute them from current evidence before acting.

### H. First-task Design gap

A brand-new task cannot always be inferred from Git. Support `sdp start <task>` and `sdp design --task ...` to record a private pending task description once. If no active workplan and no task evidence exist, ask for that genuinely missing input rather than fabricating a task. Once a workplan exists, subsequent stages derive context from repository authority.

### I. Result contract, run binding, and ingestion

Every rendered prompt requests a compact versioned JSON result after the normal human-readable response. It includes a non-secret `run_id` and `prompt_fingerprint` and must normalize at least:

- schema version, run identity, prompt fingerprint, stage, reported outcome;
- reported recommended next stage/action;
- workplan identity/path + semantic fingerprint when known;
- candidate branch/HEAD/dirty/remote identity when known;
- blockers with route class (implementation nonconformance, design deficiency, missing evidence, independent issue, etc.);
- completed/pending obligation locators/summaries;
- checks/evidence executed or unavailable;
- planning/product artifacts claimed changed;
- concise human summary.

All agent-reported repository identities are claims until independently reconciled against current repository observations. Store **reported route** separately from **derived route**. Material conflict -> inconsistent/needs confirmation.

Manual ingestion accepts stdin/file/clipboard. Association order:

1. exact structured `run_id` + prompt fingerprint match;
2. exact explicit `--run <id>` selected by user;
3. one outstanding compatible manual run with unchanged candidate/workplan, followed by bounded confirmation;
4. otherwise reject ambiguous attachment and list candidate runs.

Then parse structured result first, conservative strong markers second, bounded user confirmation third. Pasted text is inert data: never execute embedded commands/code/paths/instructions merely because they appear in a response. Apply schema/size bounds before persistence.

### J. Mode-specific prompt rendering

One renderer, transport-specific context.

**Local:** local configured worktree + candidate identity; normally compatible local protocol source; constraints say repository work occurs in the configured worktree and remote delivery follows explicit policy.

**Web:** sanitized remote repo identity + remote branch/candidate only; no local paths/private state. Prefer explicit remotely readable canonical protocol source/ref. Constraints say inspect/mutate only through authorized remote tools/connectors and do not assume local filesystem execution.

**Hybrid:** selects web/local per stage policy, otherwise uses the same renderer/reconciler.

### K. ACP-first local-agent transport architecture

Do not build five independent agent protocols. Use one normalized orchestrator `AgentTransport`/event/result/permission boundary.

**ACP is preferred when the requested backend has a sufficiently maintained/conformant ACP surface and that surface preserves the stage-relevant local-agent capabilities.** Use the official Python `agent-client-protocol` SDK for ACP schema models, JSON-RPC/stdio lifecycle, sessions, permission requests, and tool-call/event plumbing rather than duplicating that protocol.

Backend profiles select launch paths and capability requirements; they do not own workflow semantics. Initial preference order:

- Claude: maintained `agentclientprotocol/claude-agent-acp` when its Claude Agent SDK surface preserves the required project skills/MCP/auth/model/permission/session behavior; otherwise documented native structured Claude interface;
- Codex: maintained `agentclientprotocol/codex-acp` when its Codex App Server mapping preserves the required skills/MCP/auth/model/reasoning/sandbox/session behavior; otherwise documented native structured Codex interface;
- OMP: native `omp acp` when conformant for the required tool/MCP/session/permission behavior; native OMP RPC only for a materially required capability absent or defective over ACP;
- Pi: native `pi --mode rpc` initially; an ACP bridge may be explicitly configured only after it satisfies the same capability/conformance contract;
- Antigravity: official structured headless CLI or official Python SDK with schema/streaming support; do not make an unofficial ACP shim a core dependency while official structured surfaces are stronger.

ACP compatibility is not assumed to mean complete behavioral equivalence with a user's interactive CLI. Capability probes and backend qualification must test the properties `sdp` relies on. Known adapter limitations or regressions route to the next supported structured transport; they do not justify PTY scraping or dangerous permission bypass.

ACP Registry may be used as discovery metadata after local capability probing. It must not silently install or upgrade executables. `acpx` may be supported as an optional external bridge/debugging tool, but it is not a core dependency or second session/workflow authority.

### L. Manual-web transport

`manual-web` is first-class. A stage command reconciles, renders, prints, copies to clipboard when safely supported, and prints the one follow-up ingestion command (`sdp ingest --clipboard` or an explicit run-aware variant when needed).

Clipboard use is reported explicitly and configurable. Failure to access a platform clipboard degrades to stdout/stdin without changing workflow semantics. No browser automation.

### M. Local process, permission, session, and concurrency safety

Use direct argv process APIs (`shell=False` semantics), target repo cwd, bounded streaming, configurable timeout, cancellation escalation, and pre/post Git observations independently of agent claims.

Never default to `--dangerously-*`, `--yolo`, unrestricted sandbox bypass, or equivalent. Normalize ACP/native permission-request events. Interactive runs surface approve/deny choices when supported; non-interactive mode follows explicit policy and fails safely rather than hanging.

Backend-native session persistence is distinct from orchestrator history. Record session ID when available. Allow config to request ephemeral/no-native-session persistence where supported. Fresh-context Review/Verification defaults to a fresh agent session; implementation repair may resume only when policy chooses and the candidate/workplan identity is compatible.

Serialize direct local agent runs per configured project/worktree in v0.1 using a private-state cross-platform lock. A second local run against the same worktree reports the active run and refuses by default; it may not create a second mutating authority race. Manual-web prompts may be outstanding concurrently only because run IDs/candidate identities disambiguate them. Parallel agent scheduling/worktree management is a future feature.

A crashed direct run leaves a nonterminal historical attempt; on next reconciliation mark it interrupted/unknown from process/lock evidence rather than completed. SQLite migrations use the same project/state lock and transactions; destructive migrations preserve a recoverable backup when materially necessary.

Do not serialize environment secrets into prompts/logs/DB. Bounded output capture must not accumulate an unbounded transcript in RAM.

### N. Remote/local synchronization

Track local worktree HEAD/status, local tracking ref, and observed remote branch HEAD separately. Remote observations carry freshness.

`status` should not require hidden network mutation. `sdp sync` is the explicit remote refresh boundary by default; web prompt rendering may perform a read-only `ls-remote`-class refresh when project policy allows it and should otherwise state the age/staleness of the remote observation. Do not auto-merge/rebase/pull. After local run, report local changes and ahead/behind state; pushing is explicit/configured delivery.

### O. Privacy, retention, history, and export

Default stored content: rendered prompt, user-visible final response, structured result, backend/run/session IDs, Git/workplan/protocol observations, and recommendation snapshots. Raw event/tool streams default off. Hidden reasoning/thought channels default not persisted or automatically re-exposed.

Provide configurable retention, redaction, export, purge, and optional SQLite FTS/history search where available. Do not automatically inject full past prompts/responses into new prompts; only derived structured state/blocker summaries are automatic. Export never targets either repository implicitly and warns that exported history may contain proprietary/sensitive material.

Do not invent custom cryptography. Owner-only permissions plus user-selected OS/disk-encrypted storage are the v0.1 baseline. Future maintained keyring/encryption integration may sit behind the storage abstraction if explicit at-rest encryption becomes a product requirement.

### P. Future service/MCP/TUI seam

Core services (state query, render prompt, report stage result, get next action, run backend) must be callable without terminal rendering so a later `sdp mcp`/local service/Textual TUI can reuse them. No mandatory daemon/MCP/TUI in v0.1.

### Q. Open-source reuse boundary

Reuse third-party components when they remove delegated plumbing **without importing a competing authority model**.

Adopt the focused dependencies listed in section A and the official ACP Python SDK for the optional agent extra. Treat `acpx`, ACP Registry, Textual, `tomlkit`, and `markdown-it-py` as bounded optional integrations when their specific need appears.

Bernstein, Agetor, Claim Plane, Harnss, Agent Deck, Claude Squad, Beads, Vibe Kanban, and similar projects are useful prior art or potential future interoperability surfaces, but do not adopt their task database, worktree scheduler, approval authority, or repository-local state as the orchestrator's core. Those systems solve overlapping but different ownership problems and would compete with Protocol workplan/Git authority.

Do not adopt a generic workflow/FSM/event-sourcing engine for current-state authority. The projection is a reconciliation over external authority plus subordinate history, not an application-owned transition log. Avoid PTY/tmux scraping as the normal agent integration path; prefer ACP or documented structured RPC/SDK/JSON.

A third-party component is accepted only after license, maintenance, supported-platform, trust-boundary, persistence-location, and semantic-fit review. Reuse must reduce total product complexity, not merely local lines of code while adding another daemon/database/task system.

## Implementation obligations and delegated solution space

### O1 — Installable package and core API
Provide package/console entrypoint with separable services for config, observations, workplans, persistence, reconciliation, prompt source/rendering, ingestion, graph/status, and backend execution. Package install/import + `sdp --help` smoke.

### O2 — Dependency/configuration resolution
Implement the dependency policy above and one validated multi-project configuration path with provenance for material defaults/automatic values; cwd project auto-selection when unambiguous; no secrets persisted. `sdp init` creates a minimal config. `sdp config` at minimum locates/displays/validates effective config; in-place comment-preserving edits are optional and may justify `tomlkit`. Test precedence, invalid combinations, path normalization, license/metadata expectations where release tooling supports them, and redaction.

### O3 — Git observer and safe repository identity
Machine-readable Git inspection for root/branch/detached/HEAD/source-relevant dirty/staged/untracked fingerprint/upstream/ahead-behind/remote. Sanitize remote URLs before any durable/user/web representation. Test clean, dirty, detached, no-upstream, divergence, credential-bearing remotes, and candidate fingerprint invalidation.

### O4 — Workplan catalog, lifecycle consistency, selection, and semantic fingerprints
Discover active/archive plans, safe-parse frontmatter, compute exact + semantic fingerprints, track observations, implement Frozen selection precedence, `sdp workplans`, `sdp use`. Test zero/one/multiple candidates, pin/stale pin, branch affinity, archive/move/delete, lifecycle contradictions, lifecycle-only metadata changes that preserve semantic fingerprint, and substantive edits that invalidate it.

### O5 — Private SQLite history/migrations
Versioned transactional schema for project identity, observations, stage runs/results, explicit selections/overrides, recommendation snapshots, prompt/final-response retention metadata, optional raw-log refs, and migration version. Current state remains derived. Test migration, rollback/recoverable backup where needed, reopen, purge, absent/corrupt DB truthful recovery.

### O6 — Project/run locking and interrupted-run recovery
Use private-state cross-platform locking to serialize direct local runs/migrations per project/worktree. Record active run/process metadata. Test second-run refusal, normal release, crash/interruption recovery, stale history, and read-only status while a run is active.

### O7 — Reconciler, evidence keys, and recommendation reducer
Deterministically combine current repository/workplan/protocol evidence and historical results; preserve reported-vs-derived route; apply stage-specific evidence invalidation; expose UNKNOWN/AMBIGUOUS/INCONSISTENT/STALE. Table-test lifecycle loops, candidate changes after PASS, workplan semantic changes, lifecycle-only moves, contradictory reports, and stale remote observations.

### O8 — Protocol source resolver and canonical prompt renderer
Resolve explicit compatible source -> generated compatible package snapshot -> remotely readable canonical source -> non-closure. Parse canonical blocks/input topology, resolve declared variables, preserve intentional `AUTO`/`NONE`, add transport context/result contract/run identity. Build parity checks prove bundled snapshot comes from canonical source. Test every 5.16 stage local/web, unsupported protocol version, version mismatch, prompt drift, no local-path leak, and stable prompt fingerprint.

### O9 — New-task capture
Implement `sdp start` / `design --task`; no-task/no-plan gives one bounded missing-input error. Test new and existing-workplan flows.

### O10 — Structured result ingestion and run association
Versioned Pydantic schema, run ID/prompt fingerprint binding, structured extraction, conservative fallback, explicit run selection/confirmation, semantic-workplan/candidate binding, inert handling of malicious pasted text, and payload size bounds. Test wrong-run paste, conflicting/missing IDs, invalid/ambiguous outputs, agent-claimed commit mismatch, plan-change invalidation, and multiple outstanding manual prompts.

### O11 — CLI surface and doctor
At minimum:

```text
sdp init
sdp config
sdp doctor
sdp status [--json] [--refresh]
sdp next [--copy] [--run]
sdp baseline | design | implementation | review | verification
sdp stabilization | alignment | health | closeout
sdp ingest [--run ID] [--stdin|--clipboard|FILE]
sdp history [--json]
sdp history export ...
sdp history purge ...
sdp workplans
sdp use <workplan>
sdp graph [--format ascii|mermaid|dot|json]
sdp backends
sdp sync
```

Stage commands default to render/copy; `--run` dispatches policy/backend. `doctor` probes config/state permissions, protocol snapshot/parity identity, Git, clipboard, backend executables/transports, and reports actionable degradation without mutating the target repository. End-to-end fake-backend CLI tests required.

### O12 — Manual-web round trip
Web rendering + clipboard/stdout fallback + run-aware response ingestion + remote-ref refresh/report + local/private-data non-disclosure. Test assembled render -> clipboard/stdout -> ingest -> reconcile path with fake clipboard/remote, including multiple outstanding prompts.

### O13 — ACP transport, normalized agent boundary, and probes
Implement one agent event/result/permission/session interface. Use the official ACP Python SDK for ACP JSON-RPC/stdio/session/permission mechanics. Probe executable/version/capabilities cheaply. Missing/unsupported/degraded transport gives a concrete reason and configured manual fallback. Test ACP initialization/session/prompt/update/permission/cancellation, protocol-version mismatch, adapter failure, and native-fallback normalization.

### O14 — Backend profiles with bounded native fallbacks
Close Claude through its maintained ACP adapter when capability-equivalent, Codex through maintained ACP when capability-equivalent, and OMP through native ACP when conformant. Close Pi through native RPC unless an explicitly selected ACP bridge passes the same contract. Close Antigravity through its official structured CLI or SDK. Each profile must preserve cwd, relevant skill/MCP/config visibility, auth/model/reasoning/sandbox/permission/session semantics required by the stage, stream normalized user-visible output, and capture final result/session when supported. Fixtures demonstrate transport parity at the orchestrator boundary; live authenticated smoke remains optional and never a CI credential requirement.

### O15 — Hybrid routing and session policy
Config supports global web/local/hybrid + per-stage route/backend. Shipped hybrid defaults:

- Design/Review/Verification/Stabilization -> manual web;
- Implementation -> configured local backend;
- Baseline/Health Audit -> local;
- Closeout -> local;
- Alignment -> web default, configurable.

Defaults are convenience policy, not protocol authority. Missing preferred local provider must not silently switch to another paid provider unless explicitly configured. Fresh Review/Verification uses a new backend session by default; implementation repair may resume only under compatible state.

### O16 — Local process lifecycle/permission/resource safety
Direct argv, no shell interpolation, bounded streams, explicit timeouts/cancel escalation, normalized permission handling, no default bypass flags, no secret logging, pre/post Git snapshots. Test hanging child, permission request, large output, nonzero exit, interruption, dirty baseline attribution, branch switch during run, and secret env non-persistence.

### O17 — Privacy/retention/export/purge
Configurable prompt/final/raw retention; raw off by default; private permissions; redaction; export/purge/history search; no automatic historical transcript injection. Test permissions where supported, purge, export warning/boundary, redaction, raw-disabled, and reasoning-event exclusion.

### O18 — Status/history/workplans/graph UX
`status` shows project/workplan/branch/candidate/upstream/remote freshness, last outcome, blockers, stale/ambiguous evidence, active run, and next command/reason. `history` shows chronology; `workplans` active/retired/ambiguous/inconsistent; graph highlights current/recommended/loops. Deterministic text/JSON snapshots and ASCII/Mermaid/DOT/JSON graph output.

### O19 — Remote/local reconciliation without surprise mutation
`sdp sync` refreshes observations and explains divergence. Network/fetch/ls-remote behavior is explicit/configurable. Fast-forward/push/merge/rebase remain separate explicit operations/policies. Test remote-only advancement, local-only advancement, divergence, stale remote observation, offline behavior, and no implicit worktree mutation.

### O20 — Documentation, packaging, and supply-chain closure
Document isolated install (pipx/uv-tool class), project registration, manual web round-trip, ACP/native backends, hybrid policy, privacy/state/session locations, retention/purge, graph/status, dependency extras, adapter installation responsibility, and troubleshooting. Protocol README/prompt reference may link to orchestrator as optional convenience; do not make it a lifecycle requirement or include private state in skill `dist/`.

Package metadata must distinguish lightweight core/manual-web installation from optional local-agent integrations. Do not auto-download agent adapters at runtime. Release validation records supported dependency/ACP ranges and license/provenance checks sufficient to explain the shipped environment.

### O21 — Future MCP/service/TUI seam
Core APIs remain terminal-independent and suitable for later `get_state`, `render_prompt`, `report_stage_result`, `get_next_action`, and `run_backend` service/MCP/TUI exposure. No mandatory daemon/MCP/TUI in v0.1.

### O22 — OSS reuse/conformance guardrail
Maintain tests that prove external transports/libraries remain below the protocol state/authority boundary. A dependency upgrade that changes ACP event/permission/session behavior, frontmatter interpretation, path placement, or prompt rendering must fail focused conformance until reconciled. Do not add a full external orchestrator/task database merely because it offers overlapping UI/session features.

## Implementation authority

### Frozen

- local private control plane, not protocol/product authority;
- canonical prompt prose remains `development-workflow-prompts.md`; bundled prompt is generated/version-bound transport only;
- current workflow projection derives from repository/workplan/protocol evidence + subordinate private history, never stale DB override;
- exact artifact hash and semantic workplan fingerprint remain distinct;
- candidate-bound evidence cannot survive a material candidate-identity change by default;
- history remains outside both repositories;
- explicit web/local privacy and mutation boundary;
- ACP-first normalized local-agent transport with structured native fallback when ACP lacks required capability/fidelity;
- no silent backend/adapter installation or provider substitution;
- serialized direct runs per configured project/worktree in v0.1;
- SQLite local durable metadata/history for v0.1;
- Python 3.11+;
- no browser automation, generic workflow authority, orchestrator worktree scheduler, or mandatory daemon in v0.1.

### Delegated

Exact Python modules/classes; SQLite table/index names and normalized schema details; precise candidate dirty-fingerprint algorithm provided it is change-sensitive; clipboard implementation details; exact compatible dependency patch versions; exact backend launch flags; ACP versus native transport after capability qualification; graph styling/aliases; optional FTS; raw-log compression; config editing beyond init/validate; future TUI presentation.

### Reopen only on evidence

Reopen only the affected Design surface if canonical Markdown cannot be robustly parsed/versioned (then consider one structured canonical source that also generates the human reference); SQLite cannot meet local recovery/privacy/concurrency needs; stage-specific evidence invalidation cannot be represented without a materially different authority model; a named backend exposes no safely automatable structured interface capable of the required stage semantics; ACP-first transport causes unavoidable capability loss that cannot be covered by bounded native fallbacks; Python materially blocks required portability; or user-mediated web transport cannot meet supported-platform privacy/usability.

## Affected surface and task-specific acceptance

Expected protocol-repository surfaces: new `orchestrator/` package/tests/docs; small optional README/prompt-reference links; CI/package/release hooks as needed. Existing skill prompt semantics and skill `dist/` should remain unchanged except justified links/build parity metadata.

### Real-owner acceptance boundaries

1. **Prompt correctness:** real prompt source resolver/loader/renderer operating on canonical/generated compatible source; hand-written duplicate prompt is not acceptance.
2. **State correctness:** real reconciler over actual Git/workplan/protocol observations + recorded runs; seeding a final state object bypasses the claim.
3. **Evidence validity:** real candidate/workplan semantic identity and invalidation path; changing the reviewed candidate or semantic workplan must stale the corresponding result, while lifecycle-only archival metadata must not counterfeit a semantic change.
4. **Manual result association:** real run/prompt identity from render -> clipboard/stdout -> paste/ingest; attaching a response to the wrong outstanding run must fail safely.
5. **Backend execution:** real ACP client/agent handshake or explicitly justified native structured fallback, real process/event/permission/result normalization, deterministic fake protocol streams, and optional live smoke; command construction alone is insufficient.
6. **Concurrency safety:** real project/run lock around direct execution and crash recovery; two local runs may not concurrently own the same configured worktree by default.
7. **Privacy:** assembled web prompt + persistence path + export path; prove local path/credential/raw-event/reasoning non-disclosure under relevant config.
8. **Manual web:** real render -> clipboard/stdout -> ingest -> reconcile path.

### Required evidence

- unit tests for config/dependencies, Git observer/sanitization/candidate identity, workplan parser/fingerprints, DB/migrations, project lock, reducer/evidence invalidation, protocol source/extraction/rendering, result schema/run binding, graph, clipboard, routing, ACP/native transports, and backend profiles;
- temporary-Git integration for active/archive/lifecycle contradictions, semantic-vs-lifecycle workplan changes, branch/upstream/divergence, dirty candidate changes, local/remote advancement, and offline/stale remote state;
- end-to-end fake-backend loop: Design -> Implementation -> Review NO-PASS -> Implementation -> Review PASS -> Closeout, proving stale evidence on candidate changes;
- manual-web test with two outstanding prompts proving wrong-run paste rejection;
- web end-to-end local-path/credential non-disclosure;
- direct-run concurrency/crash test;
- package install/entrypoint/`sdp doctor` smoke for core and agent extra;
- ACP conformance tests against deterministic fake agent plus backend-specific parser/profile fixtures;
- full existing protocol regression/build/package validation;
- live backend smoke only when installed/authenticated, skip-with-reason otherwise.

Production qualification: unnecessary beyond bounded startup/status/render/history latency, SQLite size/retention sanity, and streaming-memory sanity for realistic local run counts.

## Implementation sequence and redesign/simplification triggers

### Stage 1 — Core model/config/observers/private history
Package, selected focused dependencies, config resolution, Git/workplan observation, exact + semantic fingerprints, DB migrations, project locking, run persistence, reconciler, UNKNOWN/AMBIGUOUS/INCONSISTENT/STALE semantics. Close with temporary-repository integration and crash/lock recovery.

### Stage 2 — Canonical prompt + manual web core
Protocol source resolver/generated snapshot parity, version-bound stage profile, renderer/result contract/run identity, clipboard/stdin ingestion, start/use/status/next/stage/history/workplans/graph/doctor commands, web/local privacy separation. This stage must already be useful with no local agent integration.

### Stage 3 — ACP-first local execution framework
Normalized agent transport/event/result/permission boundary; official ACP Python client; capability probes; safe process/cancel/session policy; deterministic fake ACP/native transports; routing. Establish ACP protocol, permission, cancellation, and session tests before backend-specific work.

### Stage 4 — Backend profiles and bounded native fallbacks
Close Claude ACP-or-native capability profile, Codex ACP-or-native profile, OMP ACP-or-RPC profile, Pi RPC profile, and Antigravity official structured profile one by one. Each closes capability/probe/parser/command tests before the next. No vendor may force backend-specific core workflow state. Optional `acpx`/ACP Registry interoperability is qualified only after the direct ACP client path is sound.

### Stage 5 — Hybrid/remote/privacy/docs/package closure
Default routing/fresh-review policy, retention/export/purge/search, remote observation/freshness, supply-chain/package extras, docs/install/release, full protocol regression and end-to-end acceptance.

### Future extensions
After the core stabilizes, consider `sdp mcp`, a local Textual dashboard/TUI, ACP Registry-assisted discovery, richer live events, explicit multi-worktree/parallel scheduling, and optional encrypted storage integrations. Reuse the core APIs; do not create a second orchestration model.

### Active simplification triggers

Before adding durable machinery, simplify if implementation develops backend-specific prompt/state copies; both mutable current-state tables and reconciler authority; duplicated local/web project models; multiple workplan parsers/fingerprints; duplicate full transcript storage in DB + files; wrapper-on-wrapper subprocess/retry/cancel frameworks around ACP; a custom permission protocol parallel to ACP/native structured permission events; a generic workflow/event-sourcing engine; or daemon/MCP/TUI introduced only to compensate for unclear core APIs.

### Genuine Design-reopen triggers

Backend CLI flag churn, ACP adapter bugs with a bounded structured fallback, missing clipboard utility, or presentation preferences do not reopen Design. Reopen only a Frozen choice listed above when evidence shows it cannot satisfy the product invariants.

## Final Design review — 2026-09-06

The final review incorporated the open-source survey and challenged the plan for authority duplication, dependency excess, protocol-version drift, wrong-run ingestion, candidate/workplan evidence staleness, direct-run races, backend capability fidelity, remote/local divergence, privacy, and install-time/runtime supply-chain behavior.

Resolved material gaps:

- replaced five bespoke transport protocols with ACP-first shared plumbing plus bounded native structured fallbacks;
- selected focused maintained dependencies that remove genuine portability/schema/locking/clipboard plumbing while rejecting heavyweight workflow/task/state frameworks;
- added capability-fidelity qualification so ACP adapters do not silently substitute a semantically different Claude/Codex/OMP environment;
- added run ID + prompt fingerprint association for manual/web response ingestion;
- separated exact workplan artifact identity from semantic authority identity;
- made candidate identity include dirty working-tree state and defined stage-specific evidence invalidation;
- added serialized direct-run ownership and interrupted-run recovery;
- made remote observation freshness/network behavior explicit;
- made Protocol 5.16 workflow support version-bound instead of silently reinterpreting older plans;
- added `sdp doctor`, dependency/supply-chain closure, and explicit no-auto-install policy.

No remaining design-level blocker was found. The plan preserves the Protocol 5 two-role authority model, keeps the database subordinate and disposable, remains useful in manual-web-only mode, and reduces rather than expands custom backend machinery.

## Design verdict

**PASS — implementation-ready.**
