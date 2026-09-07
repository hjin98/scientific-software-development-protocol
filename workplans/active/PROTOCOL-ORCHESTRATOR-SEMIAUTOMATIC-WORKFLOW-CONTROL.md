---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-SEMIAUTOMATIC-WORKFLOW-CONTROL
protocol_version: 5.16.0
orchestrator_target_version: 0.1.0
status: active
base_commit: 3715a7e34c10c1735347cd3ee8e2b75c8a2eed55
---

# Protocol Orchestrator — Semi-Automatic Workflow Control, Metering, and Quota-Aware Scheduling Workplan

## Objective / problem invariants / non-goals

### Original problem

Protocol 5.16 provides canonical parameterized workflow prompts, but the user still has to select a stage, discover the current workplan/branch/candidate, substitute inputs, remember prior PASS/NO-PASS outcomes, decide what comes next, move prompts/results between agents, reconstruct workflow state, choose an execution backend, and manually reason about which provider/account still has enough quota for the next stage.

Build one **local, privacy-preserving protocol orchestrator** that turns those stages into an executable control surface and also meters/predicts resource consumption so the system can choose an engineering-sufficient execution route automatically.

The common path should approach:

```text
sdp status
sdp next
# or explicitly
sdp design
sdp implementation --run
sdp review
```

A stage command first resolves the Protocol stage from repository/workplan evidence. It then selects an execution route from configured web/local agent routes. Manual-web mode makes prompt copy and response ingestion one-step operations. Local mode can invoke supported agents, stream user-visible output, meter usage when available, reconcile the repository afterward, and preserve private history.

### Tier-1 product invariants

1. **The orchestrator is not protocol authority.** Product/problem truth, Frozen architecture, workplan meaning, implementation behavior, and Design/Implementation verdicts remain owned by governing repository artifacts, protocol skills, and the agents/users acting in those roles.
2. **Workflow-stage authority and execution-route scheduling are separate.** The workflow reducer determines which stage is required. The scheduler chooses who executes that already-required stage. Quota pressure may change account/model/harness/effort only inside the stage's engineering-feasible set; it may not skip Review, weaken a required reasoning tier, reinterpret a workplan, or rewrite PASS/NO-PASS.
3. **Current repository evidence outranks stale local history.** Every material command reconciles private history with current Git/worktree/upstream/remote observations and active/archive workplans.
4. **Observed meter state outranks prediction.** Metering describes resources currently observed; prediction estimates future consumption; scheduling chooses a route. A prediction never rewrites a provider-reported balance/quota observation.
5. **`UNMETERED_FOR_SCHEDULER`, `METERED`, and `UNKNOWN` are distinct.** A configured web route may consume no quota tracked by this orchestrator. That is not equivalent to unknown meter state or infinite provider capacity.
6. **Quota/account state is user-global, not project-local.** If two projects share the same Claude/Codex/provider account, they consume the same ledgers and must participate in one atomic reservation domain.
7. **Private history stays private and local.** Prompts, pasted/final responses, structured stage results, account/resource telemetry, predictions, schedule decisions, backend/session metadata, and optional raw event logs live outside both the protocol repository and target software repositories by default.
8. **One workflow semantics, multiple transports.** Manual web, Claude, Codex, Pi, OMP, Antigravity, and future compatible agents consume the same rendered Protocol stage semantics. Transport adapters must not fork workflow doctrine.
9. **Web and local operation are explicit execution modes.** Web mode identifies a sanitized remote repository/branch/candidate and assumes remote tools/connectors. Local mode identifies the configured worktree and allows direct local repository work. Web prompts must not leak local paths, account balances, private state paths, credential-bearing remotes, environment secrets, or machine-private metadata.
10. **Automatic when evidence is strong; bounded choice when consequentially ambiguous.** Multiple plausible workplans, routes, account identities, or materially different next actions produce explicit ambiguity instead of a guess.
11. **Agent results are evidence with provenance.** PASS/NO-PASS, blockers, completed/pending obligations, checks, route identity, and candidate/workplan identity are stored as reported observations, not self-authorizing transitions.
12. **Prompt generation remains useful without direct integration.** Manual web is a first-class route, not an error path.
13. **Direct integration is capability-aware and safe by default.** ACP is preferred when it preserves required capabilities; documented native structured RPC/SDK/JSON is the bounded fallback. Never default to dangerous permission/sandbox bypass.
14. **Workflow and resource state are inspectable and explainable.** The user can query current stage, workplan, candidate, last outcomes, active/retired plans, route/resource state, quota reservations, predictions, selected route, rejected alternatives, and recommendation reason codes.
15. **The private database is disposable convenience state, not product authority.** Deleting it may lose history, predictions, and inferred quota knowledge but must not damage/redefine either repository. Fresh bootstrap recovers the strongest repository facts and reports unrecoverable private history as unknown.
16. **Historical transcripts do not become automatic prompt context.** Future prompts receive compact structured state/blocker summaries, never raw prior transcripts unless explicitly requested.
17. **Manual result ingestion cannot silently attach to the wrong run.** Every generated prompt carries a non-secret run identity and prompt fingerprint.
18. **Evidence invalidation follows changed dimensions.** Candidate changes, semantic workplan changes, protocol changes, route identity uncertainty, and lifecycle-only moves are distinguished.
19. **Scheduler optimization is quality-feasible first.** Cost/quota optimization happens only after filtering out routes that cannot satisfy stage capability, repository-access, privacy, independence, automation, or tooling requirements.
20. **The scheduler remains interpretable.** Cold-start priors, quantile estimates, reservations, reserves, and route scores must be explainable. No black-box model may own admission or stage transitions.

### Explicit non-goals for v0.1

- No new lifecycle/approval role and no replacement for Git, workplans, protocol skills, CI, or agent-native safety systems.
- No mandatory repository-local `.sdp` ledger/state/transcript directory.
- No browser DOM scraping for ChatGPT/Claude/Gemini web interaction or quota meters as a primary mechanism.
- No cloud orchestration/multi-user synchronization service.
- No hidden automatic merge/rebase/pull/push.
- No automatic installation/upgrading of agent CLIs, ACP adapters, or registry-discovered binaries.
- No invented token-equivalent pricing for opaque subscription quotas.
- No assumption that missing meter data means zero usage or unlimited capacity.
- No mandatory resident daemon, Temporal deployment, generic workflow engine, event-sourcing framework, or TUI in v0.1. A later fully autonomous service may adopt a durable execution substrate only if it remains subordinate to the same protocol/workflow authority model.
- No orchestrator-managed parallel worktree scheduler in v0.1. Independently configured worktrees/projects may run concurrently only through global quota reservations and per-worktree run locks.
- No mature neural/black-box learned scheduler before telemetry volume and calibration evidence justify it.

## Frozen high-level architecture and engineering envelope

### A. Product placement, runtime, and dependency policy

Implement a Python 3.11+ subproject distributed alongside the protocol but logically separable from skill bundles:

```text
orchestrator/
  pyproject.toml
  src/sdp_orchestrator/
  tests/
```

Install console entrypoint `sdp`; retain `python -m sdp_orchestrator` fallback.

Use focused maintained dependencies where they remove real portability/schema/protocol machinery:

- `platformdirs` — user config/state/cache roots;
- `typer` — CLI command model/completion;
- `pydantic` — configuration, normalized events/results/resources/predictions, validation, JSON Schema;
- `python-frontmatter` — safe workplan frontmatter parsing;
- `filelock` — cross-platform project/worktree run and migration locks;
- `pyperclip` — bounded clipboard adapter with stdout/stdin fallback;
- optional `agent-client-protocol` extra — preferred ACP client for local-agent integration.

Keep `sqlite3`, `tomllib`, `subprocess`, `asyncio`, `json`, `pathlib`, `hashlib`, `statistics`, `math`, `uuid/secrets`, and compression on the standard library.

Do not add GitPython, an ORM, NetworkX, Jinja2, OR-Tools/PuLP, a generic FSM/event-sourcing framework, or Temporal merely for symmetry. The initial scheduler has a small route set and can enumerate/score feasible routes directly. `tomlkit`, `markdown-it-py`, Textual, or a statistical/ML package such as scikit-learn/River may be added only after their concrete need is demonstrated. Mature predictive models are an optional later dependency surface, not a prerequisite for deterministic metering/scheduling.

Dependency versions are not Frozen identities. Use deliberate compatible ranges and a reproducible development/test lock. Bound pre-1.0 ACP versions to a tested compatible range. Record supported Python versions, licenses, provenance, and dependency changes during release work.

### B. Authority and control-flow architecture

The orchestrator has two subordinate projections and one route-selection boundary:

```text
TARGET/PROTOCOL REPOSITORY EVIDENCE
              +
PRIVATE PROJECT RUN/RESULT HISTORY
              |
              v
DERIVED WORKFLOW PROJECTION
              |
              v
          STAGE INTENT
              |
              +-----------------------------+
                                            |
METER OBSERVATIONS + RESERVATIONS           |
        + USAGE TELEMETRY                    |
              |                              |
              v                              v
   DERIVED RESOURCE PROJECTION      ROUTE CATALOG + POLICY
              |                              |
              +-------------+----------------+
                            v
                  USAGE/OUTCOME PREDICTOR
                            |
                            v
                     ROUTE SCHEDULER
                            |
                            v
                  SELECTED EXECUTION ROUTE
                            |
                +-----------+-----------+
                |                       |
          MANUAL WEB               LOCAL AGENT
```

The workflow reducer owns stage recommendation. The scheduler owns route selection only. Meter observations own present resource facts. The predictor owns no authority; it supplies distributions/uncertainty to the scheduler.

### C. User-global private state and project partitioning

Use one user-global private state root via `platformdirs`. Store one transactional SQLite control database containing project-scoped workflow history **and** user-global account/resource/route/prediction/reservation state. This is required so capacity shared across repositories is reserved atomically.

Conceptual state:

```text
state_root/
  orchestrator.sqlite
  projects/
    <project-key>/
      raw/           # optional bounded raw events/transcripts
      exports/       # only when explicitly requested
```

Project rows remain separable for purge/export. Global account/resource telemetry may retain project/task references according to privacy policy. SQLite WAL mode is appropriate for the single-user multi-process controller. Per-project/worktree `filelock` prevents simultaneous local mutation; SQLite transactions protect global reservations and meter updates across processes.

Do not persist raw provider credentials. Account/credential profiles contain only stable local identifiers and references to provider/backend-native authentication configuration or a secret store.

### D. Protocol support, canonical prompt ownership, and source resolution

`source/shared/references/development-workflow-prompts.md` remains canonical prompt prose. Do not hand-maintain backend-specific copies.

The prompt loader extracts stage blocks and declared `INPUTS`, substitutes only declared input values, and preserves the remaining canonical text where practical. It may wrap the block with:

1. `ORCHESTRATOR_CONTEXT` — compact derived workflow context, explicitly non-authoritative; and
2. `ORCHESTRATOR_RESULT` — versioned structured-result schema carrying `run_id` and `prompt_fingerprint`.

The installed package must work without a protocol checkout. Resolve explicit compatible source -> packaged version-bound generated snapshot -> remotely readable compatible canonical source -> truthful non-closure.

v0.1 ships a Protocol 5.16 workflow profile. Older/newer workplans may be cataloged, but automatic routing/rendering requires an explicitly compatible profile/source.

### E. Workplan discovery, lifecycle consistency, and semantic identity

Discover configured active/archive workplans and parse bounded frontmatter plus path, exact hash, and **semantic authority fingerprint**. Lifecycle-only metadata/path changes may preserve semantic fingerprint; substantive authority/body changes must alter it.

Selection precedence:

1. explicit command selection;
2. still-valid private pin;
3. unambiguous branch/workplan association;
4. exactly one active candidate;
5. otherwise `AMBIGUOUS`.

Lifecycle contradictions are `INCONSISTENT`, not normalized silently.

### F. Candidate identity and evidence invalidation

Candidate identity includes repository/project identity, branch/detached state, HEAD, source-relevant staged/unstaged/untracked fingerprint, upstream relation, observed remote commit, and freshness. If dirty state cannot be fingerprinted confidently, identity is incomplete rather than falsely durable.

At minimum:

- Baseline binds to before-candidate identity;
- Design acceptance binds to protocol + workplan semantic fingerprint;
- Implementation completion binds to protocol + workplan semantic fingerprint + resulting candidate;
- Review/Verification/Stabilization bind to exact reviewed candidate + semantic workplan + protocol;
- lifecycle-only closeout changes may preserve semantic evidence when the product candidate and semantic fingerprint are unchanged.

### G. Workflow-state and stage-intent model

Registry stages: baseline/change-health, design/workplan, implementation, review/update, verification, stabilization/architecture-GC, downstream alignment, health audit, closeout.

Separate execution status (`pending`, `running`, `completed`, `failed`, `cancelled`, `blocked`, `unknown`) from semantic outcome (`pass`, `no_pass`, `action_required`, `complete`, `not_applicable`, `unknown`). `UNKNOWN`, `AMBIGUOUS`, `INCONSISTENT`, and `STALE` are first-class.

The reducer emits a **StageIntent** that includes stage, required capability class, required session freshness/independence, repository-access needs, whether manual interaction is allowed, whether unattended direct execution is required, and task-specific policy constraints. These are scheduling inputs, not scheduler-invented requirements.

A brand-new task still requires `sdp start <task>` or `sdp design --task ...` when no repository evidence can supply the task itself.

### H. Execution-route model

Keep **model**, **backend/harness**, **account/credential profile**, **transport**, **effort**, and **resource-ledger mapping** separate.

Conceptually:

```text
ExecutionRoute =
    provider
  + account_profile
  + backend_profile
  + transport
  + model
  + effort
  + repository_access_mode
  + resource_ledgers
  + metering_class
```

A model can appear in multiple routes and the same account can expose multiple models that share the same quota ledgers.

Examples:

```text
chatgpt-web-sol-high
  transport = manual-web
  model = GPT-5.6 Sol
  effort = high
  repo_access = remote-connector
  metering = UNMETERED_FOR_SCHEDULER
  resource_ledgers = []
  human_interaction = required

codex-a-sol-high
  transport = ACP/native structured
  account = chatgpt-a
  model = GPT-5.6 Sol
  effort = high
  resource_ledgers = [chatgpt-a.5h, chatgpt-a.weekly]

codex-a-luna-high
  account = chatgpt-a
  model = GPT-5.6 Luna
  resource_ledgers = [chatgpt-a.5h, chatgpt-a.weekly]
```

Do not hard-code a provider such as ChatGPT Web as permanently unmetered. Metering class is route configuration with provenance so provider/product policy can change without architecture changes.

Manual web's zero tracked quota cost does **not** make it universally preferred: user interaction, automation availability, repository access, latency, and stage/tool suitability are separate feasibility/score dimensions.

### I. Resource-ledger model

Do not make `SUBSCRIPTION` versus `PAYG` the scheduler primitive. A route consumes zero or more **ResourceLedgers**.

A ledger records:

- allowance visibility: `OPAQUE` / `PRICED`;
- expiration: `EXPIRING` / `NON_EXPIRING`;
- reset/window semantics: `NONE`, `FIRST_USE_ANCHORED`, `ACCOUNT_FIXED`, `BILLING_CYCLE`, `CALENDAR_FIXED`, `CONTINUOUS_ROLLING`, `UNKNOWN`;
- funding behavior: `HARD_STOP`, `FALLBACK_TO_OVERAGE`, `POSTPAID`;
- current observed balance/usage when available;
- meter units and provenance/confidence;
- reservations and uncertainty holds.

A dual-window route must satisfy every active ledger simultaneously. Shared account quota is represented once and referenced by all routes that consume it.

Transparent PAYG uses versioned pricing functions over provider-specific billable components. Opaque subscription quota is modeled/predicted in the provider's observed meter units; never invent unsupported token-equivalent conversion.

A route with no scheduler-tracked quota uses `UNMETERED_FOR_SCHEDULER` and no capacity ledger. `UNKNOWN` means the scheduler lacks enough evidence and must follow configured conservative admission policy.

### J. Metering, reset inference, and provenance

Keep `AccountMeter` separate from `AgentTransport`. A transport may report per-run token/cost events while a meter independently reports account/window state.

Per field, prefer official vendor/API or backend-reported meter state; then stable provider/account profile knowledge; then empirical inference; then explicit user-supplied state where automatic evidence is unavailable. Explicit user overrides may supersede automatic discovery only with visible provenance.

Do not use browser scraping as the normal meter source. Support official APIs/machine-readable backend surfaces, hard-limit events, and explicit manual meter snapshots.

Every observation carries source, timestamp/freshness, unit, and confidence. Meter-delta attribution carries quality such as `EXACT_RUN_REPORTED`, `EXCLUSIVE_INTERVAL`, `PARTIALLY_CONTAMINATED`, or `UNKNOWN`.

Reset inference maintains competing hypotheses (first-use anchored, account fixed, billing-cycle, calendar fixed, continuous rolling) and updates them from observed discontinuities. Use ordinary deterministic/statistical logic, not an LLM. Insufficient evidence remains `UNKNOWN`.

### K. Global reservations and crash reconciliation

Before launching a metered direct run, reserve predicted capacity atomically on every consumed ledger. Admission and reservation occur in one SQLite transaction across all projects/processes using the same user-global database.

Reservations are predictive holds, never vendor-reported consumption. They are reconciled against live/post-run observations. If a run dies and final meter state is unavailable, do not blindly release all capacity as though no consumption occurred: retain an explicit uncertainty hold or conservative unresolved-consumption estimate until the next authoritative observation/policy decision.

Provider-reported hard limits and refreshed meter state override stale reservations/predictions.

### L. Usage telemetry and task features

Reuse the existing private run history as the spine of usage telemetry. A run records the planned route and, when knowable, the actual route/model/effort with provenance. This matters for manual web, where the scheduler can recommend a model but cannot always prove which UI model/effort the user actually used.

Record available run-level values:

- stage/role and repair round;
- project/workplan/candidate identity;
- provider/account/backend/transport/model/effort;
- prompt length and task features;
- wall/model/tool/wait time where available;
- model/tool call counts;
- fresh/cached/output/reasoning token categories where exposed;
- provider monetary cost;
- meter snapshots before/after and attribution confidence;
- outcome, interruption/quota exhaustion, review pass/fail, blocker recurrence.

Missing telemetry stays missing.

Deterministic task features should include stage, task type, scope, diff size/file count, repository/subsystem scale, failing-test count, integration/benchmark burden, repair count, blocker recurrence, workplan-obligation count, prompt size, requested tool classes, and whether Design was reopened.

A semantic feature extractor is optional later. It must not be required for scheduling and must not silently consume scarce quota merely to decide how to spend quota.

### M. Usage/outcome predictor

Predict **distributions**, not point guesses, for task `t` on route `r`:

```text
T(t,r)        runtime
Q_j(t,r)      consumption of each resource ledger j
Token_k(t,r)  billable token categories where relevant
Cost(t,r)     monetary cost where priced
P_pass(t,r)   probability of successful stage completion
P_interrupt   probability of route/quota interruption
N_repair      future repair-round distribution
```

For `UNMETERED_FOR_SCHEDULER` routes, quota prediction is not required, but outcome/runtime/manual-interaction history can still inform route quality.

Cold start uses conservative hierarchical priors by stage/role x model x effort x backend/transport, with optional project-specific corrections. Early online learning uses empirical quantiles/EWMA/Bayesian-style shrinkage that can be implemented without a heavy ML dependency. Mature prediction may add quantile gradient boosting or similar interpretable/tabular methods only after enough data exists.

Persist every prediction before execution and compare with actual observations. Track calibration of P50/P75/P90/P95. Low-confidence meter attribution receives reduced training weight. Selection bias is acknowledged; bounded exploration is optional later and may never sacrifice required engineering quality merely to collect data.

The prediction target is expected resource/cash cost **to accepted stage completion**, not merely first-call usage, because low-quality routes may trigger additional repair/review rounds.

### N. Scheduler and default auto-routing

`AUTO` is the default route policy unless the user/project explicitly pins a route/backend.

Scheduling is two-phase.

**Hard feasibility filter:**

- stage minimum capability and effort policy;
- required tooling/skills/MCP visibility;
- repository-access mode;
- privacy/security policy;
- fresh-session/independence requirements;
- backend/provider health;
- interaction mode: manual-web is infeasible for an unattended `--run` unless the user explicitly allows a manual handoff;
- predicted consumption fits spendable ledger capacity at required quantile;
- required future reasoning/review reserve remains protected.

**Ranking inside the feasible set:**

1. probability of required-quality completion;
2. probability of finishing without interruption;
3. preservation of mandatory future reasoning/review capacity;
4. shadow/opportunity cost of expiring subscription quota;
5. expected PAYG monetary cost;
6. manual-interaction/handoff/continuity penalty;
7. provider/model-family diversity preference for independent review;
8. latency where otherwise equivalent.

Use dynamic future-stage reserve rather than a permanent fixed percentage. The workflow graph supplies expected future Review/Design-reopen demand; reserve a conservative quantile.

Use receding-horizon/MPC behavior without requiring a daemon: on each `sdp next`, run start, completion, interruption, or meter refresh, recompute current resource state, forecast the relevant reset horizon, choose only the next route, observe actuals, and re-optimize later.

Expiring subscription quota has nonzero opportunity cost. A simple explainable shadow price may rise as remaining capacity becomes scarce relative to forecast demand and fall when capacity is likely to expire unused. This permits both conserving scarce weekly reasoning quota and intentionally burning excess quota near reset.

The scheduler records candidate routes, rejection reasons, prediction quantiles, reservations, selected route, and deterministic score components. `sdp schedule --explain` must make the decision understandable.

### O. Mode-specific rendering and manual web

One renderer uses transport-specific context.

**Local:** local configured worktree/candidate; compatible local protocol source; repository work happens locally.

**Web:** sanitized remote repository identity + remote branch/candidate; no local/account/resource paths or quota balances; use remote-readable protocol source; repository inspection/mutation occurs through authorized remote tools/connectors.

**Manual web is a first-class execution route.** When selected, render/print/copy the prompt and provide the run-aware ingestion command. Clipboard failure degrades to stdout/stdin. No browser automation.

For interactive `sdp next`, an unmetered web route may be preferred for Design/Review when it is engineering-sufficient. For `sdp next --run`, manual routes are filtered unless explicit manual handoff is allowed.

### P. ACP-first local-agent transport architecture

Use one normalized `AgentTransport`/event/result/permission boundary.

Prefer official Python `agent-client-protocol` when a backend's ACP surface preserves stage-relevant capabilities. Initial preference:

- Claude: maintained Claude ACP when capability-equivalent; native structured fallback;
- Codex: maintained Codex ACP when capability-equivalent; native structured fallback;
- OMP: native `omp acp`; RPC fallback only for materially missing ACP capability;
- Pi: native JSONL RPC initially; ACP bridge only after equivalent qualification;
- Antigravity: official structured headless CLI or official SDK.

ACP compatibility does not imply perfect equivalence with the user's interactive CLI. Capability tests must verify skills/MCP/config/auth/model/effort/sandbox/session behavior required by the route.

ACP Registry may provide discovery metadata but may not silently install/upgrade agents. `acpx` is optional interoperability/debugging, not a core dependency or second workflow/session authority.

### Q. Local process, permission, session, concurrency, and failover safety

Use direct argv execution, target worktree cwd, bounded streaming, timeout/cancellation escalation, and independent pre/post Git observations.

Never default to dangerous permission bypass. Normalize ACP/native permission events. Noninteractive runs follow explicit allow/deny policy and fail safely rather than hang.

Backend-native session persistence is distinct from orchestrator history. Fresh Review/Verification defaults to a fresh session; Implementation repair may resume only under compatible candidate/workplan/route policy.

Serialize local agent mutation per configured worktree with a private lock. Different projects/worktrees may run concurrently, but all metered routes share global reservation transactions.

On quota/provider interruption, the current worktree/repository state is controller-observed WIP, not accepted state. After the process is terminated and the lock is safely released, the scheduler may choose another eligible route for the same stage/repair attempt. Cross-mode remote/local continuation requires explicit reconciliation of remote/local candidate state before resumption; do not silently pull/merge.

The dying agent is not required to summarize itself. Repository diff/status, workplan, run/result history, checks, blockers, and optional structured agent summary form the continuation context. Automatic controller-owned worktree checkpoint refs and multi-worktree rollback machinery are future autonomy extensions, not required for v0.1.

### R. Remote/local synchronization

Track local HEAD/status, local tracking ref, and observed remote branch HEAD separately with freshness.

`status` does not require hidden network mutation. `sdp sync` is the explicit remote refresh boundary by default; web rendering may use read-only remote observation when policy permits. No automatic merge/rebase/pull/push.

### S. Privacy, retention, history, and export

Default stored content: rendered prompt, user-visible final response, structured result, backend/run/session IDs, Git/workplan/protocol observations, route/schedule decision, numeric usage/resource telemetry, and prediction metadata. Raw tool/model event streams default off; hidden reasoning/thought channels are not persisted/re-exposed by default.

Account/quota identities and balances stay private and are not inserted into agent prompts unless an explicit task genuinely requires them.

Provide retention, redaction, export, purge, and optional SQLite FTS/history search. Allow raw prompt/transcript retention to be purged independently from useful numeric usage telemetry where policy permits. Derived task features/embeddings are also potentially sensitive and follow explicit retention policy.

Do not invent custom cryptography. Owner-only permissions plus user-selected OS/disk-encrypted storage are the baseline.

### T. Open-source reuse and future service boundary

Reuse focused dependencies and ACP where they reduce delegated plumbing without importing a competing task/workflow authority.

Bernstein, Agetor, Claim Plane, Harnss, Agent Deck, Claude Squad, Beads, Vibe Kanban, and similar projects remain prior art/possible future interoperability rather than core state authorities.

Do not adopt a generic FSM/event-sourcing/optimization engine for the bounded stage/resource reducer. The route set is small enough for direct deterministic enumeration initially.

Core services (state query, render prompt, report result, meter snapshot, predict usage, select route, run backend) remain terminal-independent so a later MCP/local service/TUI or durable autonomous outer executor can reuse them without creating a second orchestration model.

## Implementation obligations and delegated solution space

### O1 — Installable package and core APIs
Provide separable services for config, repository/workplan observations, global persistence, reconciliation, prompt rendering, ingestion, resource/metering, prediction, scheduling, graph/status, and backend execution. Package/import/`sdp --help` smoke.

### O2 — Configuration resolution and private global state
Validated multi-project config plus user-global accounts/models/backends/routes/resource-ledgers policy. Cwd project auto-selection when unambiguous. No raw secrets persisted. One global SQLite DB with project-scoped history and account-global resource state. Test precedence, redaction, project isolation, cross-project shared-ledger visibility.

### O3 — Git observer and candidate identity
Machine-readable root/branch/detached/HEAD/dirty/staged/untracked fingerprint/upstream/ahead-behind/remote. Test candidate invalidation and credential-bearing remote sanitization.

### O4 — Workplan catalog/lifecycle/semantic fingerprint
Discover active/archive plans, safe-parse frontmatter, exact + semantic fingerprints, selection precedence, contradictions, move/archive/delete behavior.

### O5 — SQLite schema/migrations and concurrency
Transactional schema for projects, runs/results, observations, accounts, models, backends, routes, ledgers, meter snapshots, reset observations, reservations/uncertainty holds, usage telemetry, predictions, schedule decisions, retention metadata, and migration version. WAL mode. Test rollback/recovery/corrupt DB truthfulness.

### O6 — Project locks and interrupted-run recovery
Serialize local mutation per worktree, retain read-only status access, recover stale/nonterminal attempts after crashes, and separate project lock ownership from global quota transactions.

### O7 — Workflow reducer and stage intent
Derive stage from Protocol/repository evidence, preserve reported-vs-derived routing, stage-specific evidence invalidation, and emit hard scheduling requirements without choosing a provider/model.

### O8 — Protocol source resolver/canonical renderer
Version-bound prompt snapshot/source resolution, declared-input substitution, run ID/prompt fingerprint, local/web privacy separation, unsupported-version non-closure.

### O9 — New-task capture and workplan-free Design entry
`start` / `design --task`; no-task/no-plan gives one bounded missing-input error.

### O10 — Structured result ingestion/run association
Pydantic schema, run/prompt binding, explicit run selection/confirmation, workplan/candidate reconciliation, inert malicious paste handling, size limits, multiple outstanding web prompts.

### O11 — Model/backend/account/route catalog
Implement distinct model capability profiles, backend transport profiles, account/credential references, effort levels, execution routes, repository-access properties, and route -> ledger mapping. Configuration, not hard-coded provider truth.

### O12 — Resource-ledger and pricing model
Opaque/priced, expiring/non-expiring, reset semantics, funding behavior, multiple simultaneous ledgers, shared pools, versioned PAYG pricing. Explicit `UNMETERED_FOR_SCHEDULER` and `UNKNOWN` semantics.

### O13 — Meter interfaces/reset inference
`AccountMeter` abstraction independent of transport; official/machine-readable/manual snapshots; provenance/confidence; hard-limit events; deterministic reset hypothesis inference; no browser-scraping requirement.

### O14 — Atomic reservations/uncertainty reconciliation
Quantile-based reservations on all consumed ledgers in one global transaction; cross-project oversubscription prevention; crash uncertainty holds; authoritative post-run meter reconciliation.

### O15 — Usage telemetry and attribution
Capture available tokens/cost/time/tool events/meter deltas/outcomes; planned versus actual route provenance; attribution confidence; no fabricated zeros.

### O16 — Task feature extraction and cold-start predictor
Deterministic task features plus hierarchical stage/model/effort/backend priors; empirical P50/P75/P90/P95 consumption/runtime/outcome estimates; project/route corrections when evidence exists; prediction persistence/calibration.

### O17 — Deterministic quota-aware scheduler
Hard capability/transport/privacy/automation/quota feasibility; dynamic future reasoning reserve; configurable admission quantile; expiring-ledger shadow cost; PAYG fallback; route quality/continuity/manual-interaction/diversity/latency scoring. Record rejected alternatives and reason codes.

### O18 — Default auto-routing and explicit overrides
`AUTO` default for `next`/stage commands; explicit `--route`/project policies override. Interactive calls may select manual web; unattended `--run` excludes manual routes unless explicitly allowed. No silent provider substitution outside configured eligible routes.

### O19 — CLI/status/doctor/resource UX
At minimum:

```text
sdp init
sdp config
sdp doctor
sdp status [--json] [--refresh]
sdp next [--copy] [--run] [--route ID] [--explain]
sdp baseline | design | implementation | review | verification
sdp stabilization | alignment | health | closeout
sdp ingest [--run ID] [--stdin|--clipboard|FILE]
sdp history [--json]
sdp workplans
sdp use <workplan>
sdp graph [--format ascii|mermaid|dot|json]
sdp backends
sdp routes
sdp resources [--json]
sdp usage [--json]
sdp predict [STAGE] [--route ID]
sdp schedule [STAGE] [--explain]
sdp sync
```

`doctor` probes config/state permissions, protocol snapshot, Git, clipboard, backends/transports, configured meters, stale resource observations, and route eligibility without mutating the target repository.

### O20 — Manual-web round trip
Render/copy/ingest/reconcile with run-aware association, remote refresh, no private/account data leakage. Test unmetered route selection for an interactive semantic stage and exclusion for unattended direct execution.

### O21 — ACP transport and normalized agent boundary
Official ACP Python client for schema/JSON-RPC/session/permission where appropriate, deterministic fake ACP/native streams, capability/version failure handling.

### O22 — Backend profiles and native fallbacks
Claude ACP-or-native, Codex ACP-or-native, OMP ACP-or-RPC, Pi RPC, Antigravity official structured transport. Preserve relevant skills/MCP/config/auth/model/effort/sandbox/session behavior.

### O23 — Local process lifecycle and quota interruption failover
Direct argv, bounded output, timeouts/cancel, permission handling, pre/post Git, quota/hard-limit interruption classification, safe lock release, same-stage rescheduling to another eligible configured route without treating WIP as accepted.

### O24 — Remote/local reconciliation
Explicit remote freshness, remote-only/local-only/divergent state, no surprise mutation, safe handoff boundary between remote web and local continuation.

### O25 — Privacy/retention/export/purge
Separate raw transcript/prompt retention from numeric telemetry; redact secrets/account-sensitive values; export warnings; no automatic transcript injection; no reasoning-channel persistence by default.

### O26 — Status/history/workplans/graph/usage presentation
Deterministic text/JSON and ASCII/Mermaid/DOT graph; route/resource panels show freshness, reservations, binding ledger, predicted usage, and next action without implying semantic authority.

### O27 — Documentation, packaging, and supply-chain closure
Document core/manual-web install versus optional agent extras, account/route/ledger configuration, meter provenance, quota prediction limits, auto-routing overrides, privacy/state locations, ACP/native backends, and troubleshooting. No runtime auto-download of agents/adapters.

### O28 — Predictor evolution/conformance guardrail
Persist calibration evidence. Early predictor stays interpretable. A future ML dependency/model must outperform the simple calibrated baseline materially before adoption and must preserve explainable uncertainty/admission behavior. Dependency upgrades that alter ACP/meter/frontmatter/render semantics fail focused conformance.

### O29 — Future service/MCP/autonomy seam
Core APIs remain terminal-independent for future MCP/TUI/service or durable autonomous execution. Temporal or another workflow engine is not required for v0.1 and may never become protocol authority.

## Implementation authority

### Frozen

- local private control plane, not protocol/product authority;
- scheduler chooses execution route only after the workflow reducer determines the required stage;
- current workflow projection derives from repository/workplan/protocol evidence + subordinate private history;
- observed meter state is distinct from prediction and reservation;
- one user-global private resource/reservation domain across all configured projects/accounts;
- model, backend, account, route, and resource-ledger identities are separate;
- `UNMETERED_FOR_SCHEDULER` is distinct from `UNKNOWN`;
- opaque quota stays in observable provider meter units;
- shared quota is represented by shared ledgers, including simultaneous short/long windows;
- auto-routing is default but may choose only engineering-sufficient routes;
- manual web remains first-class and may be unmetered, but unattended direct execution cannot silently rely on a manual route;
- predictions are distributions with uncertainty/calibration and do not replace observed resource facts;
- global reservations are atomic and cross-project safe;
- exact workplan artifact hash and semantic fingerprint remain distinct;
- candidate-bound evidence cannot survive a material candidate change by default;
- history/resource telemetry remains outside both repositories;
- ACP-first normalized local-agent transport with structured native fallback;
- no silent backend installation/provider substitution;
- serialized direct mutation per configured worktree in v0.1;
- SQLite local durable control state for v0.1;
- Python 3.11+;
- no browser automation, generic workflow authority, mandatory daemon, or black-box scheduler in v0.1.

### Delegated

Exact module/class/table/index names; candidate fingerprint algorithm; specific empirical-prior formula; quantile estimator; shadow-price functional form; reset-hypothesis scoring; exact admission default; exact dependency patch versions; exact backend flags/ACP-vs-native choice after qualification; graph/presentation; optional later ML implementation; raw-log compression.

### Reopen only on evidence

Reopen only affected Design if SQLite cannot provide safe global reservation/concurrency semantics; stage/resource separation cannot represent required policy; a required provider exposes no safe meter or conservative unknown-mode scheduling path; opaque quota cannot be represented in stable observable units at all; a named backend has no safely automatable structured interface; ACP causes unavoidable capability loss without a bounded fallback; Python materially blocks portability; or manual web cannot meet supported privacy/usability needs.

## Affected surface and task-specific acceptance

Expected surfaces: new `orchestrator/` package/tests/docs, optional README/prompt-reference links, CI/package/release hooks. Existing skill prompt semantics and skill `dist/` remain unchanged except justified links/build parity metadata.

### Real-owner acceptance boundaries

1. **Workflow correctness:** real reconciler over actual Git/workplan/protocol evidence; scheduler cannot invent/skip stages.
2. **Prompt correctness:** real canonical source resolver/loader/renderer; no hand-written duplicate prompt acceptance.
3. **Evidence validity:** candidate/workplan semantic identity invalidation works across Review PASS, candidate changes, and lifecycle-only archive moves.
4. **Run association:** wrong outstanding manual response attachment fails safely.
5. **Route separation:** model/backend/account/transport/effort/resource-ledger mappings are independently represented and testable.
6. **Meter correctness:** observed meter state/provenance is distinct from predictions/reservations; unknown never becomes zero/infinite.
7. **Reservation correctness:** two concurrent processes/projects cannot oversubscribe one shared ledger.
8. **Scheduler correctness:** a lower-quota-cost route cannot win if it violates required stage capability/automation/privacy/tooling constraints.
9. **Manual-web correctness:** unmetered route carries zero scheduler-ledger consumption but still has manual/operational constraints; unattended run does not silently select it.
10. **Opaque quota correctness:** predicted directly in observed meter units with uncertainty/attribution quality.
11. **PAYG correctness:** versioned price function and actual billable categories where available.
12. **Backend execution:** real ACP/native structured handshake/event/permission/result normalization.
13. **Failover:** quota-interrupted WIP may be rescheduled but never promoted to accepted state.
14. **Privacy:** assembled web prompt/persistence/export paths prove no local/account/credential/raw reasoning leakage.

### Required evidence

- unit tests for config, Git/candidate identity, workplans, DB/migrations, project lock, global resource transactions, workflow reducer, route/account/model/resource schemas, meter provenance/reset logic, pricing, reservations, predictor, scheduler, prompt rendering, result binding, graph/clipboard, ACP/native transports;
- temporary-Git integration for lifecycle contradictions, candidate changes, remote/local divergence, dirty worktree identity;
- cross-project test where two projects share one dual-window quota account and reservations prevent oversubscription;
- shared-model-pool test where two models consume the same 5h/weekly ledgers;
- explicit `UNMETERED_FOR_SCHEDULER` versus `UNKNOWN` admission tests;
- interactive Design/Review routing test where a sufficient unmetered web route is preferred under policy;
- unattended Implementation test where manual web is filtered and a metered local route is chosen/reserved;
- dynamic reasoning-reserve test that prevents Implementation from starving a mandatory future Review;
- near-reset test that consumes otherwise-wasted expiring subscription capacity when quality constraints are equal;
- PAYG fallback test when subscription route is inadmissible;
- opaque quota prediction/calibration test with low-confidence contaminated observations downweighted;
- crash/reservation uncertainty test;
- quota interruption -> alternate-route same-stage continuation test without false acceptance;
- end-to-end Design -> Implementation -> Review NO-PASS -> repair -> Review PASS -> Closeout with usage/schedule history;
- manual web wrong-run paste test;
- package/`sdp doctor` smoke for core and optional agent extra;
- full existing protocol regression/build/package validation;
- live backend/meter smoke only when installed/authenticated, skip-with-reason otherwise.

Production qualification: bounded startup/status/schedule latency, SQLite size/WAL/reservation behavior, prediction-query latency, and streaming-memory sanity for realistic single-user histories. No distributed-service qualification is required.

## Implementation sequence and redesign/simplification triggers

### Stage 1 — Core workflow, global state, route/resource schemas

Package/dependencies/config; Git/workplan observation; exact + semantic fingerprints; user-global SQLite DB; project locks; run history; workflow reducer; model/backend/account/route/resource-ledger schemas; UNKNOWN/AMBIGUOUS/INCONSISTENT/STALE semantics. Close with temporary-repository and cross-project shared-resource tests.

### Stage 2 — Canonical prompt and manual-web core

Protocol source/snapshot parity; renderer/result/run identity; clipboard/stdin ingestion; start/use/status/next/stage/history/workplans/graph/doctor; web/local privacy separation; manual web represented as a normal schedulable route, including explicit unmetered configuration. Product is useful here even with no local agent integration.

### Stage 3 — ACP-first local execution framework and backend profiles

Normalized transport/event/result/permission boundary; official ACP Python client; safe process/cancel/session policy; deterministic fake ACP/native transports; Claude/Codex/OMP/Pi/Antigravity profiles; project locking and structured quota/hard-limit interruption events where exposed.

### Stage 4 — Metering, pricing, reservations, and deterministic auto-scheduler

Meter interfaces/snapshots/provenance; resource windows/reset hypotheses; PAYG pricing; atomic cross-project reservations; route feasibility; conservative cold-start priors; fixed/empirical reasoning reserve; `AUTO` routing; resources/routes/schedule CLI. This stage must already prevent avoidable quota starvation without learned ML.

### Stage 5 — Telemetry-driven prediction and receding-horizon scheduling

Run usage telemetry; attribution quality; deterministic task features; hierarchical quantile priors/online corrections; prediction calibration; dynamic future-reasoning reserve; expiring-quota shadow pricing; expected cost-to-accepted-completion ranking; repeated reoptimization at each workflow boundary. Use simple interpretable statistics first.

### Stage 6 — Failover, hybrid/remote/privacy/docs/package closure

Quota-interruption same-stage rescheduling; remote/local handoff reporting; retention/export/purge; schedule-decision history; documentation/install/release; full protocol regression and end-to-end acceptance.

### Future extensions

After enough data and core stability: optional quantile boosted predictor/embedding similarity; bounded safe exploration; ACP Registry-assisted discovery; local TUI/MCP; explicit multi-worktree/parallel scheduling; controller-owned WIP checkpoint refs; durable autonomous outer execution such as Temporal only if genuinely needed.

### Active simplification triggers

Simplify if implementation develops a second workflow authority inside the scheduler; duplicate per-project account ledgers; backend-specific quota databases; both mutable current-state tables and reducer authority; wrapper-on-wrapper retry/reservation frameworks; multiple pricing/meter abstractions for the same resource; a generic optimizer for a tiny route set; ML introduced before simple calibrated statistics are exhausted; browser scraping added to compensate for absent official meters; or daemon/TUI/Temporal introduced only because core APIs are unclear.

### Genuine Design-reopen triggers

Provider flag churn, meter unavailability for one route with a conservative fallback, ACP adapter bugs with native fallback, missing clipboard utility, or poor initial calibration do not by themselves reopen Design. Reopen only a Frozen architectural choice listed above when evidence shows it cannot satisfy the product invariants.

## Design integration review — 2026-09-07

The quota/metering plan has been integrated as a subordinate resource-control layer rather than a second workflow controller.

Key reconciliation decisions:

- Protocol workflow projection determines the next required stage; quota scheduler chooses only the execution route.
- Manual web can be configured `UNMETERED_FOR_SCHEDULER`, while local agents commonly consume opaque subscription or PAYG ledgers. Zero scheduler quota cost does not erase manual-interaction/automation/tooling constraints.
- Account/resource state moves to one user-global private database because subscription/PAYG capacity can be shared across projects; project transcripts/history remain logically partitioned.
- Account, model, harness/backend, route, effort, and resource ledgers remain separate so shared quotas and alternate access paths are represented correctly.
- Multiple subscription windows are simultaneous constraints and are reserved atomically across processes/projects.
- Observed meter state, predictive reservation, and predicted consumption remain separate concepts.
- Opaque subscription quotas are learned directly in provider meter units; transparent PAYG uses versioned pricing.
- Existing run/workplan/candidate history supplies the task/outcome spine for quota prediction, minimizing new machinery.
- Auto-routing is default, but feasibility is quality/operational-policy first. Quota cannot downgrade mandatory Design/Review quality.
- Interactive manual-web and unattended direct-run scheduling are intentionally different feasibility contexts.
- Cold-start scheduling is deterministic and conservative; online prediction is introduced only after telemetry exists; mature ML remains optional.
- Receding-horizon scheduling reuses the existing `sdp next`/run-result boundaries and therefore does not require Temporal or a resident daemon.
- Quota interruption can reschedule WIP to another configured route after safe lock/repository reconciliation, without treating interrupted work as accepted.

No architectural conflict remains between the original semi-automatic orchestrator and the quota-aware scheduler. The combined system remains one private control plane with a single Protocol workflow authority boundary.

## Design verdict

**PASS — integrated architecture is implementation-ready.**
