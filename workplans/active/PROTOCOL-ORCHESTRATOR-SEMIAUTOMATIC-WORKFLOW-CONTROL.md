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

Protocol 5.16 has a canonical parameterized workflow-prompt reference, but the user still has to select a stage, discover the current workplan/branch/candidate, substitute inputs, remember prior PASS/NO-PASS outcomes, decide what comes next, move prompts/results between agents, and reconstruct workflow state afterward. That bookkeeping is especially awkward when semantic work happens in a web agent against a remote Git repository while implementation happens in a local coding agent against a local worktree.

Build a **local, privacy-preserving protocol orchestrator** that turns those stages into an executable control surface. The common path should approach:

```text
sdp status
sdp next
# or explicitly
sdp design
sdp implementation --run
sdp review
```

A stage command renders a directly usable prompt with repository/workplan/protocol variables resolved from current evidence. Manual-web mode makes prompt copy and response ingestion one-step operations. Local mode can invoke supported agent CLIs, stream the user-visible result, ingest structured completion metadata, reconcile the repository afterward, and preserve private history.

### Tier-1 product invariants

1. **The orchestrator is not protocol authority.** Product/problem truth, Frozen architecture, workplan meaning, implementation behavior, and Design/Implementation verdicts remain owned by governing repository artifacts, protocol skills, and the agents/users acting in those roles. The orchestrator observes, remembers, reconciles, transports, and recommends; it must not silently invent or override product/Frozen authority.
2. **Current repository evidence outranks stale local history.** Every material command reconciles private history with present Git/worktree/upstream/remote observations and present active/archive workplans. A stale database record cannot silently override a repository fact.
3. **Private history stays private and local.** Prompts, pasted/final responses, structured stage results, backend/session metadata, and optional raw event logs live outside both the protocol repository and target software repository by default.
4. **One workflow semantics, multiple transports.** Manual web, Claude CLI, Codex CLI, Pi, OMP, and Antigravity consume the same rendered stage semantics. Backend adapters may differ in process/RPC/SDK transport, structured I/O, session handling, sandbox controls, and repository representation; they must not fork protocol doctrine.
5. **Web and local execution modes are explicit.** Web mode identifies the remote repository/branch/candidate and assumes remote tools/connectors. Local mode identifies the configured worktree and allows direct local repository work. Web prompts must not leak local absolute paths, private state paths, credential-bearing remote URLs, or other machine-private details.
6. **Automatic when evidence is strong; bounded choice when consequentially ambiguous.** Branch, HEAD, upstream, protocol version, workplan path, and known stage history should resolve automatically. Multiple materially plausible workplans or routes produce `AMBIGUOUS`/`INCONSISTENT` state and one bounded selection rather than a guess.
7. **Agent results are evidence with provenance.** PASS/NO-PASS, blockers, completed/pending obligations, checks, and routing are stored with stage/run/backend/candidate/workplan identity. The orchestrator may detect contradictions but must not rewrite a reported verdict to manufacture closure.
8. **Prompt generation remains useful without any local agent integration.** Manual web is a first-class mode, not an error path.
9. **Direct integration is capability-aware and safe by default.** Initial local adapters: OMP, Pi, Claude CLI, Codex CLI, Antigravity CLI. Probe installed version/capabilities; degrade clearly to manual prompt generation when unsupported. Never default to dangerous permission/sandbox bypass.
10. **Workflow state is inspectable.** Query current workplan/stage, branch/candidate/upstream/remote relation, previous attempts/verdicts, blockers, completed/pending obligation observations, active/retired workplans, and current/recommended action as text/JSON and as a workflow graph.
11. **The private database is disposable convenience state.** Deleting it may lose private history but must not damage/redefine the repository. Fresh bootstrap recovers the strongest state Git/workplans can establish and reports genuinely unrecoverable history as unknown.
12. **Historical transcripts do not become automatic prompt context.** Future prompts receive a compact structured projection of relevant state/blockers, not raw prior agent transcripts. Raw history is injected only by an explicit user action. This prevents context bloat, stale authority, and prompt-injection propagation from archived outputs.

### Explicit non-goals for v0.1

- No new lifecycle/approval role; no replacement for Git, workplans, skills, CI, or agent-native safety systems.
- No mandatory repository-local `.sdp` ledger/state/transcript directory.
- No browser DOM automation, credential scraping, or brittle automation of ChatGPT/Claude/Gemini web UIs. Web transport is user-mediated clipboard/stdin/stdout.
- No cloud orchestration/multi-user service.
- No hidden automatic merge/rebase/pull/push. Remote/local synchronization is observed and reported; mutations follow explicit delivery policy.
- No requirement to persist hidden reasoning/thought channels. Store user-visible final responses and normalized metadata by default; raw event streams are optional.
- No LLM dependency for basic state classification. Structured output + deterministic parsing/reconciliation is primary; ambiguous pasted text requires confirmation.
- No mandatory resident daemon/MCP service in v0.1.

## Frozen high-level architecture and engineering envelope

### A. Product placement and runtime

Implement a Python 3.11+ subproject distributed alongside the protocol but logically separable from skill bundles, e.g.:

```text
orchestrator/
  pyproject.toml
  src/sdp_orchestrator/
  tests/
```

Install console entrypoint `sdp`; retain `python -m sdp_orchestrator` fallback. Prefer standard-library SQLite/TOML-reading/subprocess/async/json/hash/path/compression mechanisms; dependencies must earn portability/correctness value.

### B. Authority model: repository evidence + private journal -> derived projection

```text
TARGET/PROTOCOL REPOSITORY EVIDENCE
              +
PRIVATE APPEND-ONLY OBSERVATIONS/RUNS
              |
              v
DERIVED CURRENT WORKFLOW PROJECTION
```

Do not create an independent mutable `current_state` source of truth. Current state is recomputed/reconciled from present Git/workplan/protocol observations plus private stage-run/result/user-selection history. A cached projection is allowed only when invalidated/reconciled before use.

### C. Canonical prompt ownership and protocol-source resolution

`source/shared/references/development-workflow-prompts.md` remains canonical prompt prose. Do not hand-maintain backend-specific copies.

The orchestrator uses a strict prompt loader that extracts stage blocks and `INPUTS`, then substitutes resolved values. It may wrap the canonical block with:

1. compact `ORCHESTRATOR_CONTEXT` (derived, explicitly non-authoritative); and
2. versioned `ORCHESTRATOR_RESULT` schema request.

The installed package must work without a protocol-repository checkout. Therefore use a **protocol source resolver** with this conceptual order:

1. explicit configured compatible protocol source/ref;
2. version-bound prompt snapshot packaged with the orchestrator, generated from the canonical prompt during build/release and carrying protocol version/source identity;
3. compatible remotely readable canonical protocol source when network use is allowed;
4. truthful non-closure if the required governing version cannot be resolved.

The packaged snapshot is a generated transport artifact, not a second editable authority. Build tests must prove byte/semantic parity with its canonical source. A bundled 5.16 prompt must not silently serve an incompatible older/newer workplan.

### D. Project config and private state

Use local TOML config supporting multiple named projects. Resolve defaults -> local config/profile -> documented environment allowlist if any -> CLI overrides. A project profile minimally carries:

- local repo path;
- remote name/URL policy and main/default branch as needed;
- active/archive workplan globs;
- protocol source/ref policy;
- mode (`hybrid`, `web`, `local`) and per-stage routing;
- privacy/retention/session policy;
- optional backend executable/sandbox/delivery settings.

Do not store credentials. Sanitize Git remote URLs before display/persistence/prompt rendering: strip URL userinfo/tokens and normalize an SSH/HTTPS remote to a safe display identity.

Private state defaults under the user's platform state directory with owner-only permissions where supported. SQLite stores metadata/history. Optional large raw event streams may be bounded compressed files under the same private root and referenced by the DB.

### E. Workplan discovery/selection

Scan configured active/archive workplan locations; parse simple frontmatter (`workplan_id`, `protocol_version`, `status` where present), path, and content hash.

Selection precedence:

1. explicit command workplan;
2. still-valid private user pin;
3. unambiguous branch/workplan association from current evidence + recorded association;
4. exactly one active candidate;
5. else `AMBIGUOUS` and offer `sdp use <workplan>`.

Never silently choose among plausible plans by mtime. Track archive/retirement from current files plus historical observations; disappearance is reported as disappearance, not invented archive state.

### F. Workflow/state model

Registry stages: baseline/change-health, design/workplan, implementation, review/update, verification, stabilization/architecture-GC, downstream alignment, health audit, closeout.

Separate execution status (`pending`, `running`, `completed`, `failed`, `cancelled`, `blocked`, `unknown`) from semantic outcome (`pass`, `no_pass`, `action_required`, `complete`, `not_applicable`, `unknown`). `UNKNOWN`, `AMBIGUOUS`, and `INCONSISTENT` are first-class projection states.

Projection exposes selected workplan, local branch/HEAD/dirty fingerprint/upstream/divergence, observed remote head, protocol identity, recent/completed stage attempts, blocker classifications, completed/pending obligation observations bound to current workplan hash, stale evidence, recommended next stage/action, and reason.

### G. First-task Design gap

A brand-new task cannot always be inferred from Git. Support `sdp start <task>` and `sdp design --task ...` to record a private pending task description once. If no active workplan and no task evidence exist, ask for that genuinely missing input rather than fabricating a task. Once a workplan exists, subsequent stages derive context from repository authority.

### H. Result contract and ingestion

Every rendered prompt requests a compact versioned JSON result after the normal human-readable response. It must normalize at least:

- schema version, stage, reported outcome;
- reported recommended next stage/action;
- workplan identity/path;
- candidate branch/HEAD/remote identity if known;
- blockers with route class (implementation nonconformance, design deficiency, missing evidence, independent issue, etc.);
- completed/pending obligation locators/summaries;
- checks/evidence executed or unavailable;
- planning/product artifacts claimed changed;
- concise summary.

Store **reported route** separately from **derived route**. Material conflict -> inconsistent/needs confirmation.

Manual ingestion accepts stdin/file/clipboard. Parse structured block first, then conservative strong markers, then bounded user confirmation. Pasted text is inert data: never execute embedded commands/code/instructions.

### I. Mode-specific prompt rendering

One renderer, transport-specific context.

**Local:** local worktree/branch/candidate; normally compatible local-first protocol source; constraints say work happens in configured worktree and remote delivery follows explicit policy.

**Web:** sanitized remote repo identity + remote branch/candidate only; no local paths/private state. Prefer explicit remotely readable canonical protocol source/ref. Constraints say inspect/mutate only through authorized remote tools/connectors and do not assume local filesystem execution.

**Hybrid:** selects web/local per stage policy, otherwise same renderer/reconciler.

### J. Backend adapter architecture

One thin `BackendAdapter` contract reports/probes executable/version and capabilities such as one-shot/headless, structured stream/final schema, session resume, cwd control, sandbox/permission controls, approval events, and RPC/SDK where useful.

Initial local backends: Claude CLI, Codex CLI, Pi, OMP, Antigravity CLI. Current implementation evidence includes Claude JSON/stream-JSON print mode, Codex `exec` JSONL, Pi JSON/RPC, OMP one-shot plus RPC/SDK/ACP, Antigravity headless stream-JSON/programmatic session. Exact current flags are delegated/version-gated, not Frozen permanent syntax.

Do not create five workflow engines. Backend-specific logic ends at delivery/event normalization/approval/cancellation/session/result extraction.

### K. Manual-web transport

`manual-web` is first-class. A stage command reconciles, renders, prints, copies to clipboard when safely supported, and prints the one follow-up ingestion command (`sdp ingest --clipboard`). Clipboard support is a platform adapter with stdout fallback; no browser automation.

### L. Local process/approval/session safety

Use direct argv process APIs (`shell=False` semantics), target repo cwd, bounded streaming, configurable timeout, and cancellation escalation. Record pre/post Git identity independently of agent claims.

Never default to `--dangerously-*`, `--yolo`, unrestricted sandbox bypass, or equivalent. Normalize backend approval-request events. In interactive orchestrator use, surface the request and allow explicit approve/deny when supported; in non-interactive mode follow configured deny/allow policy and fail safely rather than hanging.

Backend-native session persistence is distinct from orchestrator history. Record session ID when available. Allow config to request ephemeral/no-native-session persistence where a backend supports it; document that backends may maintain their own local auth/session stores outside the orchestrator DB. Fresh-context Review/Verification defaults to a fresh session; implementation repair may resume if policy chooses.

Do not serialize environment secrets into prompts/logs/DB. Bounded output capture must not accumulate unbounded transcript RAM.

### M. Remote/local synchronization

Track local worktree HEAD/status, tracking ref, and observed remote branch HEAD separately. After web response ingestion, safely refresh remote identity and report advancement; do not auto-merge/rebase/pull. After local run, report local change/ahead-behind state; pushing is explicit/configured delivery.

### N. Workflow graph/recommendation

Maintain a small deterministic stage graph matching Protocol 5.16 conditional routing (e.g. Review NO-PASS -> Implementation or bounded Design by finding class; Verification blockers route by class; Stabilization action re-enters normal cycle; Closeout terminal; Health Audit outside linear flow). Overlay actual stage attempts/outcomes.

Formats: ASCII, Mermaid, DOT, JSON. No Graphviz installation required to emit DOT.

Recommendation text is deterministic from reconciled state + reported results. It proposes action; it does not declare semantic correctness itself.

### O. Privacy/retention/context policy

Default stored content: rendered prompt, user-visible final response, structured result, backend/run/session IDs, Git/workplan/protocol observations. Raw event/tool streams default off. Hidden reasoning/thought channels default not persisted.

Provide redaction hooks, retention, export, purge. Do not automatically inject full past prompts/responses into new prompts; only derived structured state/blocker summaries are automatic. Do not invent custom cryptography; owner-only permissions + OS/disk encryption are baseline, with future maintained keyring/crypto integration behind storage abstraction if needed.

### P. Future service/MCP seam

Core services (state query, render prompt, report stage result, get next action, run backend) must be callable without terminal rendering so a later `sdp mcp`/local service/TUI can reuse them. No mandatory daemon/MCP in v0.1.

## Implementation obligations and delegated solution space

### O1 — Installable package and core API
Provide package/console entrypoint with separable services for config, observations, workplans, persistence, reconciliation, prompt source/rendering, ingestion, graph/status, and backend execution. Package install/import + `sdp --help` smoke.

### O2 — Config resolution
One validated multi-project resolution path with provenance for material auto/default values; cwd project auto-selection when unambiguous; no secrets persisted. Test precedence/invalid combinations/path normalization/redaction.

### O3 — Git observer and safe repository identity
Machine-readable Git inspection for root/branch/detached/HEAD/dirty/staged/untracked fingerprint/upstream/ahead-behind/remote. Sanitize remote URLs before any durable/user/web representation. Test clean/dirty/detached/no-upstream/divergence/token-bearing remotes.

### O4 — Workplan catalog/selection
Discover active/archive plans, parse frontmatter/hash, track observations, implement Frozen selection precedence, `sdp workplans`, `sdp use`. Test zero/one/multiple candidates, pin/stale pin, branch affinity, archive/move/delete. Multiple plausible plans must not collapse to mtime.

### O5 — Private SQLite history/migrations
Versioned transactional schema for project identity, observations, stage runs/results, explicit selections/overrides, prompt/final-response retention metadata, optional raw-log refs. Current state remains derived. Test migration, rollback, reopen, purge, absent/corrupt DB truthful recovery.

### O6 — Reconciler/recommendation reducer
Deterministically combine current repo/workplan/protocol evidence and historical results; preserve reported-vs-derived route; expose UNKNOWN/AMBIGUOUS/INCONSISTENT. Table-test lifecycle loops and contradictory/stale cases.

### O7 — Protocol source resolver and canonical prompt renderer
Resolve explicit source -> generated compatible package snapshot -> remote canonical source -> non-closure. Parse canonical blocks/input topology, resolve variables, keep intentional `AUTO`/`NONE`, add transport context/result contract. Build parity checks prove bundled snapshot comes from canonical source. Test every stage local/web, version mismatch, no local-path leak.

### O8 — New-task capture
Implement `sdp start` / `design --task`; no-task/no-plan gives one bounded missing-input error. Test new and existing-workplan flows.

### O9 — Structured result ingestion
Versioned schema, structured extraction, conservative fallback, user confirmation, workplan-hash binding for obligation observations, inert handling of malicious pasted text. Test conflicting/missing/invalid/ambiguous outputs and plan-change invalidation.

### O10 — CLI surface
At minimum:

```text
sdp init / config
sdp status [--json]
sdp next [--copy] [--run]
sdp baseline | design | implementation | review | verification
sdp stabilization | alignment | health | closeout
sdp ingest [--stdin|--clipboard|FILE]
sdp history
sdp workplans
sdp use <workplan>
sdp graph [--format ascii|mermaid|dot|json]
sdp backends
sdp sync
```

Stage commands default to render/copy; `--run` dispatches policy/backend. End-to-end fake-backend CLI tests.

### O11 — Manual-web round trip
Web rendering + clipboard fallback + response ingestion + remote-ref refresh/report + local/private-data non-disclosure. Test assembled render->clipboard->ingest->reconcile path with fake clipboard/remote.

### O12 — Backend adapter/probes
One adapter/event/result/approval interface. Probe executable/version/help/capabilities cheaply. Missing/unsupported backend gives concrete reason and configured manual fallback. Test capability matrices/version mismatch/cancellation/error normalization.

### O13 — Five direct local adapters
Claude, Codex, Pi, OMP, Antigravity direct execution via installed supported machine-readable/headless/RPC interface. Set cwd, stream user-visible output, normalize approval events, capture final result/session, honor sandbox/session policy. Command/probe/parser fixtures for all; live smoke optional when installed/authenticated, never CI credential requirement.

### O14 — Hybrid routing
Config supports global web/local/hybrid + per-stage route/backend. Shipped hybrid defaults:

- Design/Review/Verification/Stabilization -> manual web;
- Implementation -> configured local backend;
- Baseline/Health Audit -> local;
- Closeout -> local;
- Alignment -> web default, configurable.

Defaults are convenience policy, not protocol authority. Missing preferred local provider must not silently switch to another paid provider unless policy explicitly allows it.

### O15 — Local process lifecycle/approval/resource safety
Direct argv, no shell interpolation, bounded streams, explicit timeouts/cancel escalation, approval handling, no default bypass flags, no secret logging, pre/post Git snapshots. Test hanging child, approval request, large output, nonzero exit, interruption, dirty baseline attribution, secret env non-persistence.

### O16 — Privacy/retention/export/purge
Configurable prompt/final/raw retention; raw off by default; private permissions; redaction; export/purge/retention. Export does not target either repo implicitly. Test permissions where supported, purge, redaction, raw-disabled, and no automatic historical transcript injection.

### O17 — Status/history/workplans/graph UX
`status` shows project/workplan/branch/candidate/upstream/remote, last outcome, blockers, stale/ambiguous evidence, next command. `history` chronology; `workplans` active/retired/ambiguous; graph highlights current/recommended/loops. Deterministic text/JSON snapshots.

### O18 — Remote/local reconciliation without surprise mutation
`sdp sync` refreshes observations and explains divergence. Fetch/ls-remote behavior explicit/configurable. Fast-forward/push/merge/rebase separate explicit operations/policies. Test remote-only advancement, local-only advancement, divergence, no implicit worktree mutation.

### O19 — Documentation/distribution
Document isolated install (pipx-class), project registration, manual web round-trip, hybrid/local adapters, privacy/state/session locations, retention/purge, graph/status, troubleshooting. Protocol README/prompt reference may link to orchestrator as optional convenience layer; do not make it a lifecycle requirement or include private state in skill `dist/`.

### O20 — Future MCP/service seam
Core APIs remain terminal-independent and suitable for later `get_state`, `render_prompt`, `report_stage_result`, `get_next_action` local service/MCP exposure. No mandatory daemon/MCP in v0.1.

## Implementation authority

### Frozen

- local private control plane, not authority;
- canonical prompt prose remains `development-workflow-prompts.md`; bundled prompt is generated/version-bound transport only;
- derived state from repository + private evidence, never stale DB override;
- history outside repositories;
- explicit web/local privacy/mutation boundary;
- one backend-adapter abstraction for five CLIs + manual web;
- SQLite local durable metadata/history for v0.1;
- Python 3.11+;
- no browser automation or mandatory daemon in v0.1.

### Delegated

Exact Python modules/classes/CLI library; SQLite table/index names; clipboard mechanism; optional display dependencies; exact probed backend flags; one-shot vs RPC/SDK choice where equivalent; graph styling/aliases/TUI; raw-log compression.

### Reopen only on evidence

Reopen only affected Design if canonical Markdown cannot be robustly parsed/versioned (then consider a single structured canonical source that also generates the human reference), SQLite cannot meet local recovery/privacy needs, a named backend exposes no safely automatable supported interface, Python materially blocks required portability, or user-mediated web transport cannot meet supported-platform privacy/usability.

## Affected surface and task-specific acceptance

Expected protocol-repo surfaces: new `orchestrator/` package/tests/docs; small optional README/prompt-reference links; CI/package/release hooks as needed. Existing skill prompt semantics and skill `dist/` should remain unchanged except justified links/build parity metadata.

### Real-owner acceptance boundaries

1. **Prompt correctness:** real prompt source resolver/loader/renderer operating on canonical/generated compatible source; hand-written duplicate prompt is not acceptance.
2. **State correctness:** real reconciler over actual Git/workplan observations + recorded runs; seeding a final state object bypasses the claim.
3. **Backend execution:** real adapter/process/event/approval normalization with deterministic fake streams plus optional live smoke; command construction alone is insufficient.
4. **Privacy:** assembled web prompt + persistence path; prove local path/credential/raw-event non-disclosure under relevant config.
5. **Manual web:** real render -> clipboard/stdout -> ingest -> reconcile path.

### Required evidence

- unit tests for config, Git observer/sanitization, workplans, DB/migrations, reducer, prompt source/extraction/rendering, result parser, graph, clipboard, routing, all adapters;
- temporary-Git integration for active/archive, branch/upstream/divergence, local/remote advancement;
- end-to-end fake-backend loop: Design -> Implementation -> Review NO-PASS -> Implementation -> Review PASS -> Closeout;
- web end-to-end local-path/credential non-disclosure;
- package install/entrypoint smoke;
- full existing protocol regression/build/package validation;
- live backend smoke only when installed/authenticated, skip-with-reason otherwise.

Production qualification: unnecessary beyond bounded startup/status/render/history latency/storage sanity for realistic local run counts.

## Implementation sequence and redesign/simplification triggers

### Stage 1 — Core model/config/observers/private history
Package, config, Git/workplan observation, DB migrations, event/run persistence, reconciler, UNKNOWN/AMBIGUOUS/INCONSISTENT semantics. Close with temporary-repo integration.

### Stage 2 — Canonical prompt + manual web core
Protocol source resolver/generated snapshot parity, renderer/result contract, clipboard/stdin ingestion, start/use/status/next/stage/history/workplans/graph commands, web/local privacy separation. This stage must already be useful with no agent CLI.

### Stage 3 — Local execution framework
Adapter protocol, probes, normalized events/approvals, safe subprocess/cancel/session policy, fake backend, routing.

### Stage 4 — Five adapters
Claude, Codex, Pi, OMP, Antigravity one by one. Each closes probe/parser/command tests before the next. No vendor may force backend-specific core workflow state.

### Stage 5 — Hybrid/remote/privacy/docs/package closure
Default routing, fresh-review/resume policy, retention/export/purge, remote observation, docs/install/release, full protocol regression and end-to-end acceptance.

### Future extension
After core stabilizes, consider `sdp mcp`, local dashboard/TUI, richer live events, and SDK-native integration. Reuse core APIs rather than create a second orchestration model.

### Active simplification triggers

Before adding durable machinery, simplify if implementation develops backend-specific prompt/state copies; both mutable current-state tables and reconciler authority; duplicated local/web project models; multiple workplan parsers; duplicate full transcript storage in DB + files; wrapper-on-wrapper subprocess/retry/cancel frameworks; or daemon/MCP/TUI introduced only to compensate for unclear core APIs.

### Genuine Design-reopen triggers

Backend CLI flag churn, missing clipboard utility, or presentation preferences do not reopen Design. Reopen only a Frozen choice listed above when evidence shows it cannot satisfy the product invariants.

## Design verdict

**PASS — implementation-ready.**

The design closes the material gaps in the initial concept: the DB cannot become a competing source of truth; multiple-workplan and first-task ambiguity have safe resolution; web/local identities and privacy boundaries are explicit; installed operation has a version-bound generated prompt source instead of requiring a protocol checkout; historical transcripts are not silently recycled into prompts; responses are machine-ingestible but inert; local approval/session behavior is normalized; backend integration is capability-probed behind one adapter boundary; and the product remains useful as a simple one-command prompt generator even when direct IPC is unavailable.
