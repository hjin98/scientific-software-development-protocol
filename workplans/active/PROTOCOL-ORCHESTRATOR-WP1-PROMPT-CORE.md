---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: reopened
reviewed_date: 2026-09-08
reviewed_candidate: 121ca48454e222740db9606e3a4a2f22719ef5e9
review_verdict: no-pass
reopened_date: 2026-09-08
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

## 1. Objective and authority

WP-1 delivers the smallest independently useful SDP Orchestrator: an installable `sdp-orchestrator-core` distribution, installer-generated `sdp` console command, and repository-local zero-install `orchestrator/sdp.py` development launcher that all execute the same Core CLI implementation. Core observes a configured repository, resolves the governing workplan and compatible Protocol 5.16 workflow/profile, prepares a route-independent public record, renders one complete local/web stage prompt, requests a structured terminal result envelope, and composes optional extensions through one public SPI.

Core-only operation is a finished mode. It must not require Tracker, Adapters, Scheduler, persistence, agent execution, model/account catalogs, benchmarking, quota/resource prediction, or AUTO scheduling.

Governing architecture is `orchestrator/docs/architecture.md` 1.6.0. Canonical human-facing prompt authority is `source/shared/references/development-workflow-prompts.md`; packaged prompt/profile resources are reproducible derivatives only.

This file is the current snapshot-complete WP-1 implementation contract. Earlier repair chronology is non-normative Git history unless represented below.

## 2. Product / Frozen invariants

### 2.1 Tier 1A — product and stakeholder invariants

1. **Core works alone.** Config, project/worktree observation, workplan/profile/source resolution, prepare, render, CLI, and diagnostics work without higher modules.
2. **Observation is non-mutating.** Inspection does not change target worktree/index/HEAD/refs/remote-tracking refs/remotes; refresh is bounded read-only query, never fetch/pull.
3. **Prompt/workflow authority is singular.** Canonical Protocol source owns stage prose/workflow meaning; packages/tests do not become competing semantic authorities.
4. **Protocol binding is explicit.** Work governed by Protocol X is never silently interpreted under an incompatible newer profile.
5. **Ambiguity remains explicit.** Project/workplan/profile/source/remote/stage/routing ambiguity fails or remains ambiguous rather than using fuzzy names, recency, ordering, or undocumented heuristics.
6. **Prompt context is truthful.** Web mode never represents dirty/local-only/known-divergent state as remotely inspectable; local mode may reference the authorized worktree.
7. **Privacy/security guarantees are bounded and truthful.** Automatically derived web content excludes private local paths, credential-bearing remote userinfo, ambient environment values, credential-helper output, and private orchestrator state. User-authored text is intentional content.
8. **Core v1 is the durable lower seam.** Higher modules consume only documented `api.v1`/`spi.v1` value records/protocols; no private implementation objects or duplicated workplan/profile logic cross the boundary.
9. **One composition root.** Core owns the CLI, service registry, extension entry-point group, and event-subscription seam.
10. **Manual tracking compatibility exists from day one.** Every successful prompt requests exactly one terminal `StageResultEnvelope v1` tied to RunId/prompt fingerprint and emits only the subscribed non-durable prompt event.
11. **Admission precedes route-sensitive render.** `prepare()` is route-independent; later admission can occur before `render()` without provisional prompt/event side effects.
12. **Stage identity is profile-bound.** User input is `StageSelector`; `StageRef` exists only after compatible profile resolution.
13. **Render consistency is optimistic but coherent.** Material candidate/workplan/source/selection drift between prepare and final return produces stale/incoherent failure, not a mixed snapshot. WP-1 adds no repository lock/persistence.
14. **Determinism follows semantic state.** Fixed RunId + unchanged material state gives stable identities/bytes; wall-clock diagnostics and unrelated extension config do not perturb them.
15. **Installed behavior is the release acceptance owner.** Source helper tests cannot proxy-pass broken wheel/sdist, packaged profile, real Git observer, extension composition, installed CLI/stdout, privacy, or wire behavior.
16. **Repository containment is mandatory.** Orchestrator-owned source/build/test/fixture/script/doc material lives under `orchestrator/`; Protocol workplans remain under `workplans/`; repository CI contains thin invocation only.
17. **The source tree is a maintained human interface.** Core source uses a conventional, shallow repository layout with obvious module names and discoverable CLI ownership. Redundant collection directories and making essentially every implementation module look private are not justified merely for hypothetical future symmetry.
18. **Development execution must not require installing the package.** A developer working from a checkout can run the current source tree directly through one checked-in launcher without installing, uninstalling, or editable-installing `sdp-orchestrator-core`. That launcher must execute the same CLI implementation as the installed `sdp` command and must prefer checkout source over any stale installed copy.

### 2.2 Tier 1B — Frozen architecture for this cycle

Preserve Architecture 1.6.0: one Python 3.11+ `sdp-orchestrator-core` distribution, one installer-generated `sdp` entry point, one thin repository-local development launcher dispatching the same CLI owner, native PEP 420 namespace with no `sdp_orchestrator/__init__.py`, strict `core <- tracker <- adapters <- scheduler` dependency direction, one config path, one Git observer, one workplan resolver, one Protocol/profile/source authority, public Core/Application/Extension API/SPI value boundaries, prepare-before-render, one extension registry, one exact result-footer wire, and no higher-module machinery in Core.

Exact implementation decomposition below those boundaries remains Tier 2 and should be simplified where possible.

## 3. Required Core behavior

### 3.1 Configuration and prompt mode

One bounded TOML path. Prompt-mode precedence: explicit CLI/API -> project default -> core default -> built-in `web`. `PromptExecutionMode(local|web)` is distinct from canonical prompt `EXECUTION_MODE`. No silent web->local fallback. CLI project convenience: unique configured worktree containing cwd -> configured default -> sole project -> structured ambiguous/not-found. Public requests use explicit `ProjectKey`.

Core config is closed; extension namespaces are bounded opaque data interpreted only by activated extensions. Credential-bearing URLs are rejected/redacted. Unrelated extension config does not enter Core prompt/preparation identity.

### 3.2 Git/worktree/remote observation

`ObservationPolicy`: `local_only`, `use_cached_remote`, `refresh_remote`, programmatic default local-only. Cached mode performs no network; refresh performs bounded noninteractive read-only query.

`CandidateRef` binds repository/worktree, branch/detached state, HEAD, staged/index + unstaged + untracked material state, selected remote/target evidence, provenance/freshness, and identity completeness. `sdp.git-working-tree.v1` includes staged blobs/modes and worktree/untracked content under finite per-file/count/aggregate bounds. Unsupported/unreadable/embedded state is incomplete rather than falsely complete. Non-UTF-8 Git paths do not crash identity.

Remote selection: configured remote -> branch upstream remote -> origin -> sole remote -> ambiguous/unavailable. Evidence is bound to the selected remote/target. File/path remotes are local-only. Web requires known target existence, blocks dirty state/known divergence, and preserves remote ambiguity. Unknown-age cached evidence cannot satisfy explicit `max_remote_staleness_seconds`; refresh may establish freshness.

Git subprocesses are bounded during collection, non-mutating, noninteractive, and receive an intentionally constructed environment. Ambient repository/config/object redirection and executable transport overrides are not inherited.

### 3.3 Workplans and Protocol binding

Catalog bounded regular workplan text under active/archive roots. Symlink aliases/special files/path escapes are ignored/rejected safely. Frontmatter is bounded before/during data-only materialization; unsupported amplification constructs may be rejected.

Selectors are exact workplan ID or exact canonical repository-relative POSIX path. Traversal/absolute/dot/backslash aliases do not normalize into matches. Current authority uses explicit supersession evidence only. Lifecycle directory and declared status must agree for current governance.

Stage policy: Baseline/Design/Verification/Stabilization explicit-only; Implementation/Review require governing plan; Alignment exact required; Health Audit disallows; Closeout allows optional exact completed binding otherwise `COMPLETED_WORK`.

Any explicitly selected authority with a declared Protocol version must be reconciled against the compatible profile. Required stages fail on missing/invalid/unsupported governing version. Optional selected authority with absent version may remain evidence-only where the stage does not need it to determine the governing contract.

### 3.4 Protocol source/profile/workflow

V1 supports compatible Protocol 5.16. Source precedence: configured compatible local -> exact packaged derivative -> explicitly permitted bounded remote explicit ref -> truthful incompatible/unavailable failure.

Remote source resolves one requested ref to one immutable identity before multi-file use, reads bounded required data only, revalidates the ref, never executes downloaded/repository code, and records requested/resolved provenance/digests. Local multi-file reads are coherent or fail changed. Packaged resources reproduce exactly from canonical prompt source and `source/PROTOCOL_VERSION`.

Canonical extraction requires exact numbered stage-heading set and one fenced text body per stage. Machine profile carries control metadata only. Optional/context-dependent routing remains multiple alternatives/ambiguous; outcome alone never invents a deterministic next stage.

### 3.5 Inputs and two-phase identity

Every canonical input is mechanical, canonical-default, or required-user. Mechanical/first-class bindings cannot be generic overrides. `PROTOCOL_REF` follows governing Protocol; `PROTOCOL_SOURCE` defaults `AUTO_LOCAL_FIRST`; canonical `EXECUTION_MODE` is independent of prompt mode. Inserted values use one reversible structure-safe scalar encoding.

`PreparedPrompt` contains RunId, Project/Worktree observation, StageRef, candidate, WorkplanResolution, complete WorkflowProfileDescriptor/ProfileRef, PromptSourceRef, resolved mode-independent inputs/provenance, result-schema identity, and `sdp.prompt-preparation.v1`.

Preparation identity binds complete material public admission data, including each `DigestRef` as algorithm + canonicalization scheme + value. Render recomputes the preparation fingerprint, revalidates current worktree/remote/workplan/source state, renders from the same resolved source snapshot, and performs final optimistic unchanged-state validation before event publication/return.

### 3.6 Prompt wire, public values, and events

Canonical body changes only at declared input substitutions. Fingerprint replacement touches only Core-owned footer slots. Opaque RunId is JSON-safe and coherent.

Every prompt requests ordinary prose followed by exactly one exact-line terminal JSON footer. Prose may precede; only whitespace may follow the end marker. Duplicate exact footer/marker pairs are invalid. Additive result/event payload data must be recursively JSON-compatible. Public timestamps are UTC ISO-8601. `Problem` is one structured error record with `code`, redacted message/details, `retryable`, and no mirrored exception hierarchy.

Only successful final render emits `core.prompt.rendered.v1` to explicit subscribers. EventId is stable for event type + RunId + prompt fingerprint. Sink failures are redacted and cannot invalidate primary render.

### 3.7 Extension composition and passive diagnostics

One entry-point group: `sdp_orchestrator.extensions.v1`. Discovery-only reads distribution metadata without provider import and reports metadata failure truthfully. Normal activation uses canonical extension ID, API/multiplicity requirements, hard extension dependencies, and capability satisfaction from Core/already-active compatible providers. Registrations/subscriptions are staged and committed only after successful valid `ExtensionRegistration`. Wrong activation return type is failure. Alternative healthy providers can satisfy a capability even when another provider fails/cycles. Core singular services cannot be replaced silently.

`doctor` and default `capabilities` perform no provider import, target mutation, or hidden network. Doctor's `packaged_profile` is packaged-only and cannot fall through configured local/remote source precedence.

## 4. Source-tree and CLI layout — required simplification

The current `orchestrator/packages/core/src/sdp_orchestrator/core` layout is needlessly deep for WP-1 and pre-allocates a `packages/` collection for higher distributions that do not yet exist. The leading-underscore convention on nearly every implementation module also obscures ownership, including the product CLI. Development additionally needs a no-install path that executes the current checkout directly rather than requiring repeated package installation while the code is changing rapidly.

### 4.1 Target repository layout

Core becomes the direct Python project rooted at `orchestrator/`:

```text
orchestrator/
  sdp.py                      # zero-install development launcher
  pyproject.toml              # sdp-orchestrator-core distribution
  README.md
  src/
    sdp_orchestrator/         # PEP 420 namespace; no __init__.py here
      core/
        __init__.py
        cli.py
        application.py
        service.py
        config.py
        git.py
        workplans.py
        protocol_source.py
        canonical.py
        profile.py
        inputs.py
        render.py
        records.py
        errors.py
        events.py
        digest.py
        limits.py
        redaction.py
        api/
          __init__.py
          v1.py
        spi/
          __init__.py
          v1.py
        resources/
          protocol/...
  tests/
  docs/
  scripts/
```

This preserves the conventional Python `src/sdp_orchestrator/core` import layout while removing the redundant `packages/core` repository layers. It does not use exotic setuptools `package-dir` remapping merely to flatten the import namespace.

If Tracker/Adapters/Scheduler are later implemented, add only the package roots actually needed at that time under `orchestrator/` while preserving the Frozen distribution/import contracts. Do not retain a speculative collection directory solely for symmetry.

### 4.2 Module naming and privacy

The supported public consumer contract remains `sdp_orchestrator.core.api.v1` and `.spi.v1`. Other modules remain implementation detail by documentation/API policy; Python leading underscores are not the authority that makes them private.

Rename primary modules descriptively rather than prefixing essentially every file with `_`:

```text
_app.py         -> application.py
_cli.py         -> cli.py
_config.py      -> config.py
_git.py         -> git.py
_workplans.py   -> workplans.py
_protocolsrc.py -> protocol_source.py
_canonical.py   -> canonical.py
_profile.py     -> profile.py
_inputs.py      -> inputs.py
_render.py      -> render.py
_records.py     -> records.py
_errors.py      -> errors.py
_events.py      -> events.py
_digest.py      -> digest.py
_limits.py      -> limits.py
_redact.py      -> redaction.py
_service.py     -> service.py
```

Implementation may consolidate genuinely tiny modules where ownership becomes clearer, but may not add forwarding modules/wrappers solely to preserve these old private paths. They are pre-release Tier-2 internals, not compatibility contracts.

### 4.3 Installed and zero-install CLI entry points

There are two supported invocation mechanisms but exactly one CLI implementation owner.

**Installed/release path:**

```toml
[project.scripts]
sdp = "sdp_orchestrator.core.cli:main"
```

The package installer generates the `sdp` executable in the active environment. No separately maintained installed shell script is checked in.

**Development/source path:** `orchestrator/sdp.py` is a tiny checked-in launcher. It may contain only standard-library bootstrap needed to locate the adjacent `src/` tree and then delegate to `sdp_orchestrator.core.cli:main`. Its intended semantic shape is:

```python
#!/usr/bin/env python3
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC))

from sdp_orchestrator.core.cli import main

if __name__ == "__main__":
    main()
```

Equivalent simpler bootstrap is acceptable. The key contract is that checkout `src` is placed ahead of site-packages so an older installed `sdp-orchestrator-core` cannot shadow the source under development.

`sdp.py` contains **no Typer command declarations, option parsing, validation, project/workplan/profile logic, output logic, or product behavior**. All of that remains in `core/cli.py`; the launcher only selects the local source tree and calls the same `main`. Therefore it is not a second CLI authority or compatibility wrapper.

Required development usage includes:

```text
python orchestrator/sdp.py --help
python orchestrator/sdp.py doctor --config ...
python orchestrator/sdp.py implementation --config ... --prompt-mode local
```

Optionally the file may be executable (`./orchestrator/sdp.py ...`) through a normal Python shebang. It must work from arbitrary current working directories because it resolves `src/` relative to its own file location.

“Zero-install” means no installation/editable installation of the orchestrator package itself. The active Python environment must still provide declared runtime dependencies; WP-1 does not vendor or bundle Python and third-party dependencies into this development launcher.

For developer inspection, `core/cli.py` should also remain directly module-runnable where practical (`PYTHONPATH=orchestrator/src python -m sdp_orchestrator.core.cli --help`), but `orchestrator/sdp.py` is the ergonomic default checkout entry point and does not require callers to set `PYTHONPATH`.

## 5. Public API/SPI floor

Preserve Architecture 1.6.0 `CoreAPI`/`ApplicationAPI` methods (`allocate_run_id`, project/observation/workplan/workflow/list-stages, `prepare`, `render`) and versioned JSON-compatible records. Public signatures contain no Git/subprocess/file/DB/lock/event-loop/private implementation types.

Provider SPI remains `manifest() -> ExtensionManifest` and `activate(context) -> ExtensionRegistration`; `ExtensionContext` exposes public Core API, extension-owned config, and staged registrars only.

Core capabilities remain `prompt.render`, `project.observe`, `workplan.catalog`, `workflow.profile`.

## 6. Acceptance obligations

O1. **Layout/distribution/development launcher:** target source tree in §4; no `orchestrator/packages/core`; no old underscore-module compatibility shims; wheel + sdist build/inspect/install; generated `sdp` entry point targets `sdp_orchestrator.core.cli:main`; installed CLI works outside checkout; checked-in `orchestrator/sdp.py` runs checkout source without package installation and prefers checkout source over a stale installed copy; PEP 420 sibling coexistence; no root namespace init/higher imports.

O2. **Config/projects:** precedence/default/ambiguity, bounded malformed/oversized config, no semantic env override surface, extension namespace preservation, secret URL rejection/redaction, source policy.

O3. **Git/remote:** real temporary Git/worktree/remotes; staged/index/worktree/untracked identity, modes/non-UTF8/bounds, alias vs linked worktree, selected-remote evidence/freshness, no mutation, bounded subprocess/environment behavior.

O4. **Workplans:** exact path/ID, branch binding, supersession ambiguity, lifecycle, bounded parser, symlink/path escape, every stage policy and Protocol-binding case.

O5. **Protocol/profile/workflow:** canonical extraction, package/generator parity, local/packaged/remote coherence, immutable remote identity, unsupported version rejection, conservative routing.

O6. **Public prepare/render:** public API completeness, profile-bound StageRef, governing-workplan precedence, external admission between phases, complete preparation identity, JSON tamper rejection, stale checks, no private objects.

O7. **Inputs:** all stages/inputs, required-user completeness, prompt-mode vs canonical execution mode, governing Protocol ref, reversible scalar encoding, atomic invalid failures.

O8. **Renderer/wire/events:** body fidelity, deterministic fingerprints, exactly-one terminal footer, opaque RunId/placeholder collisions, JSON-compatible additive fields, explicit subscription/EventId/failure behavior.

O9. **Privacy/web truth:** final RenderedPrompt/stdout tests for paths/credentials/environment/local remotes/dirty/divergent/stale/absent/ambiguous cases.

O10. **Extensions/diagnostics:** real installed entry-point metadata; passive discovery; compatible/incompatible/missing/cyclic/alternative-provider graphs; staged activation; canonical ID/API/multiplicity/SPI; doctor/capabilities no hidden network/mutation.

O11. **CLI product/development boundary:** installed `sdp` subprocess and zero-install `orchestrator/sdp.py` both dispatch the same `core.cli:main` path. Representative commands must produce equivalent governed behavior/exit semantics apart from expected executable-path/environment provenance. Source launcher works from outside `orchestrator/`, requires no package installation, and cannot be satisfied accidentally by an older installed package. Stdout remains atomic/prompt-only; failures redacted on stderr; clipboard additive; doctor passive.

O12. **Documentation:** update architecture layout example so it no longer presents `orchestrator/packages/core/...` as preferred concrete shape; update README/user/developer commands and paths to the new layout; document both invocation modes (`sdp ...` after install and `python orchestrator/sdp.py ...` from checkout), clarify that both share `core.cli:main`, and explain public-vs-internal module boundary once without compatibility-history prose.

O13. **Final repository acceptance:** complete Core regression with Hypothesis where installed, snapshot generator check, wheel+sdist integration, zero-install launcher regression, ordinary Protocol unit/build/validate/package-parity checks, `git diff --check`, and final simplicity/absence of higher-module or duplicate-authority machinery.

## 7. Implementation evidence reviewed

Independent Review evaluated candidate `121ca48454e222740db9606e3a4a2f22719ef5e9`, based directly on review-contract commit `fc466570e7a9a3b6d2fab99a1440fe72a0a46064`.

Recorded evidence: 312 focused tests; 339 complete Core tests including wheel+sdist installed-product owner, Git/remotes/extensions/privacy/wire/API; Hypothesis 400+200 generated examples; canonical generator check; 172 ordinary Protocol tests plus skill build/validate/check-dist and `git diff --check`; focused Semgrep and Serena inspection. This is strong reusable evidence where subsequent edits cannot plausibly invalidate the claim, but it does not override the findings below.

## 8. Open implementation findings — Review verdict NO-PASS

Parent Architecture 1.6.0 remains valid. F1-F8 are implementation nonconformance/oracle drift under existing authority. F9 is a stakeholder-directed Tier-2 source-layout and development-invocation simplification within the parent containment/namespace architecture. Repair existing owners; do not add parallel registries/resolvers/renderers/workflow engines/wrappers/persistence/higher-module dependencies.

### F1 — Workflow profile over-resolves blocker outcomes

`_TRANSITIONS` still collapses context-dependent outcomes (`implementation/blocked`, `review/no_pass`, `alignment/no_pass`, `closeout/blocked`) to one next stage although Protocol 5.16 requires routing by blocker/authority context.

**Repair:** alter the existing profile transition metadata so insufficient outcomes expose all authority-backed alternatives. No routing DSL/engine.

**Tests:** context-dependent blocker/no-pass triggers remain ambiguous where Protocol permits alternatives; truly deterministic outcomes remain deterministic; package parity passes.

### F2 — Capability dependency ordering can manufacture a false cycle

The current graph makes a capability consumer depend on all compatible providers. Counterexample: B independently provides `cap.shared`; A also provides it but requires extension D; D requires `cap.shared`. Valid order B -> D -> A is rejected as a cycle. Metadata enumeration failure also collapses to empty installation, and `activate() -> None` is silently promoted to success.

**Repair:** hard extension-ID dependencies remain graph constraints; capability readiness depends on Core or any compatible provider actually active. Prefer one iterative activation/readiness owner. Report discovery failure truthfully. Reject non-`ExtensionRegistration` activation results. Keep one registry/staged commit path.

**Tests:** B/A/D activates; true unsatisfiable cycle stays disabled; metadata discovery failure is visible; `activate(None)` not active; healthy Core/providers remain available.

### F3 — Preparation identity drops DigestRef algorithm/scheme

Material digest helpers compare/hash only `.value`, omitting public `algorithm` and `canonicalization_scheme`.

**Repair:** serialize complete DigestRef everywhere material identity participates. No second digest schema.

**Tests:** changing only algorithm/scheme on candidate/workplan/profile/source digests invalidates old preparation; unchanged records remain deterministic.

### F4 — Doctor is not guaranteed packaged-only/no-network

`doctor` labels `packaged_profile` but calls normal workflow/source resolution, so configured local source can alter the result and packaged failure can reach remote fallback.

**Repair:** doctor inspects packaged snapshot directly or an existing explicitly network-disabled packaged path. No second Protocol resolver.

**Tests:** local/remote config cannot change doctor packaged observation; forced packaged failure performs zero remote calls; no provider import/repository mutation.

### F5 — Footer extractor/test oracle accepts duplicate complete footers

Frozen wire requires exactly one terminal footer, but extractor selects the last complete block and a test positively asserts this invalid behavior.

**Repair:** reject duplicate exact begin/end marker blocks while preserving exact-line/terminal-whitespace semantics. Replace the weakened test and guide wording.

**Tests:** one footer extracts; duplicate/extra exact markers reject; indented/near-match/trailing prose remain rejected.

### F6 — Explicit optional workplan can have declared Protocol version ignored

Explicit-only stages can select a plan whose declared version is silently ignored in favor of project/default profile.

**Repair:** reconcile any declared version on an explicitly selected authority; preserve evidence-only behavior only when optional version metadata is absent.

**Tests:** incompatible selected Verification/Stabilization/etc. plans fail; compatible version agrees; no-version optional plan retains accepted evidence-only path.

### F7 — Public open fields accept live/non-JSON values and timestamps are unenforced

`EventEnvelope.payload`, additive result fields, and timestamp strings can violate the public JSON/UTC value contract at construction.

**Repair:** smallest validation at existing record boundary for recursively JSON-compatible values and UTC ISO-8601 timestamps. No parallel schema system.

**Tests:** nested JSON round-trips; live objects/file handles reject; produced/deserialized timestamps are UTC ISO-8601; additive JSON compatibility remains.

### F8 — Ambient executable Git transport overrides remain inherited

Git environment still permits ambient `GIT_SSH`, `GIT_SSH_COMMAND`, `GIT_SSH_VARIANT`; `GIT_SSH_COMMAND` can execute arbitrary ambient command during a supposedly controlled query.

**Repair:** narrow existing allowlist to normal required process/credential environment; do not inherit executable Git command overrides without an accepted config surface. No transport framework.

**Test:** ambient helper that would create a marker is not executed by remote-query path; normal supported SSH-agent path remains available.

### F9 — Simplify the source tree and provide both installed and zero-install CLI entry paths

Current path `orchestrator/packages/core/src/sdp_orchestrator/core` is over-nested, repeats `core` as speculative distribution-directory and import package, and makes nearly every implementation module look private. The generated `sdp` command points at `_cli.py`, making product entry source obscure. Development currently also lacks a direct checked-in launcher, forcing package installation/editable-install workflows during rapid source iteration.

**Repair sequence:**

1. First move the Core project to the §4 target layout (`orchestrator/pyproject.toml`, `orchestrator/src/sdp_orchestrator/core`, `orchestrator/tests`). Remove `orchestrator/packages/core`; do not leave symlinks/forwarders.
2. Rename the primary implementation modules per §4.2 and rewire imports/tests/generator/package-data directly. Do not add compatibility aliases for old private module names.
3. Change installed console entry point directly to `sdp_orchestrator.core.cli:main`.
4. Add `orchestrator/sdp.py` as the thin zero-install development launcher described in §4.3. It prepends the checkout `src/` directory and calls the same `core.cli:main`; it contains no CLI/business behavior and is not included as a second installed console-script authority.
5. Reconcile architecture example, README, user/developer paths and commands.
6. Only then implement F1-F8 against the simplified owners, so repair work is not immediately invalidated by second structural churn.

**Tests/structural evidence:** old `orchestrator/packages/core` and old `_app.py`/`_cli.py`-class implementation paths are absent; `api.v1`/`spi.v1` consumer imports remain unchanged; source/wheel/sdist imports work; installed `sdp --help`, `sdp doctor`, and representative render work outside checkout; `python orchestrator/sdp.py --help`, doctor, and render work without installing the package and from an arbitrary cwd; with a deliberately stale/different installed `sdp_orchestrator.core`, the launcher demonstrably executes checkout source; source and installed invocation converge on the same CLI semantics; package resources/generator paths and CI/test runner use the new layout; no higher-module dependency, duplicate parser/command tree, or compatibility wrapper is introduced.

## 9. Re-review gate

WP-1 may return to independent Review only after F1-F9 are repaired on one exact assembled candidate. Because F9 changes import/layout/package/launcher paths, it invalidates most source-tree, packaging, CLI, API/SPI, extension, generator, and full-regression evidence; rerun those owners after the move rather than relying on pre-move green results.

Required final evidence:

1. structural migration evidence and focused F1-F9 counterexamples;
2. complete Core regression with Hypothesis active;
3. real installed extension composition and passive-doctor tests;
4. preparation/public API-SPI/wire/privacy tests;
5. real Git/remote non-mutation and environment-boundary tests;
6. canonical profile/snapshot generator parity;
7. wheel and sdist build/inspection/install plus installed CLI outside checkout from the new `orchestrator/` project root;
8. zero-install `orchestrator/sdp.py` tests from clean checkout-style paths and arbitrary cwd, including proof that local checkout source wins over a stale installed package;
9. repository layout/absence checks proving no old package tree/private-path compatibility layer or duplicate CLI implementation remains;
10. ordinary repository Protocol tests/build/package parity and `git diff --check`.

Any required unavailable owner check remains a blocker unless the governing contract permits substitute evidence. A green test whose oracle encodes the wrong contract is not closure.

**Current verdict: NO-PASS — return to `software-implementation`; perform F9 structural/development-entry simplification first, then repair F1-F8 in the simplified owners, then submit one exact candidate for fresh independent Review.**
