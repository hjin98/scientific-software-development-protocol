---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: reopened
reviewed_date: 2026-09-08
reviewed_candidate: b7d18506d1fb7e07b32db0527c7fece9aa633716
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

WP-1 delivers the smallest independently useful SDP Orchestrator: one installable `sdp-orchestrator-core` distribution, one installer-generated `sdp` console command, and one repository-local zero-install `orchestrator/sdp.py` launcher. Both invocation paths execute the same Core CLI owner. Core observes a configured repository, resolves the governing workplan and compatible Protocol 5.16 profile/source, prepares a route-independent public record, renders one complete local/web stage prompt, requests the versioned terminal result envelope, and composes optional extensions through one public SPI.

Core-only operation is a finished product mode. It requires no Tracker, Adapters, Scheduler, persistence, agent runner, model/account catalog, benchmark catalog, quota/resource predictor, or AUTO scheduler.

This workplan is governed by Protocol 5.16.0 and Frozen `orchestrator/docs/architecture.md` Architecture 1.6.0. Canonical human-facing stage prose remains `source/shared/references/development-workflow-prompts.md`; packaged prompt/profile resources are reproducible derivatives, not competing authorities.

This file is the snapshot-complete current WP-1 handoff. Superseded review chronology is non-normative Git history. Only the current blockers in §6 remain open.

## 2. Product and Frozen invariants

### 2.1 Tier 1A — stakeholder/product invariants

1. **Core works alone.** Config, project/worktree observation, workplan/profile/source resolution, prepare, render, CLI, and diagnostics work without higher modules.
2. **Observation is non-mutating.** Inspection does not change worktree content, index, HEAD, refs, remote-tracking refs, or remotes. Refresh is a bounded read-only query, never fetch/pull.
3. **Prompt/workflow authority is singular.** Canonical Protocol source owns stage prose/workflow meaning; package resources/tests do not become semantic authorities.
4. **Protocol binding is explicit and precedence-correct.** A profile-bound StageRef or selected governing workplan's declared Protocol contract is never silently reinterpreted or vetoed by a lower-precedence project default. Unsupported/incompatible authority fails truthfully.
5. **Ambiguity remains explicit.** Project/workplan/profile/source/remote/stage/routing ambiguity fails or remains ambiguous rather than using fuzzy names, recency, ordering, or undocumented heuristics.
6. **Prompt context is truthful.** Web mode never represents dirty/local-only/known-divergent state as remotely inspectable; local mode may reference the authorized worktree.
7. **Privacy/security guarantees are bounded and truthful.** Automatically derived web content excludes private local paths, credential-bearing remote userinfo, ambient environment values, credential-helper output, and private orchestrator state. User-authored task/input text is intentional content.
8. **Core v1 is the durable lower seam.** Higher modules consume documented `api.v1`/`spi.v1` value records/protocols only; no private implementation objects or duplicated workplan/profile logic cross the boundary.
9. **One composition root.** Core owns the CLI, service registry, extension entry-point group, and event-subscription seam.
10. **Manual tracking compatibility exists from day one.** Every successful prompt requests exactly one terminal `StageResultEnvelope v1` bound to RunId/prompt fingerprint and emits only the subscribed non-durable prompt event.
11. **Admission precedes route-sensitive render.** `prepare()` is route-independent; later admission can occur before `render()` without provisional prompt/event side effects.
12. **Stage identity is profile-bound.** User input begins as `StageSelector`; public `StageRef` exists only after compatible profile resolution and carries that profile identity across API calls.
13. **Render consistency is optimistic but coherent.** Material candidate/workplan/source/selection drift between prepare and final return yields stale/incoherent failure, not a mixed snapshot. WP-1 introduces no repository lock/persistence.
14. **Determinism follows semantic state.** Fixed RunId + unchanged material state yields stable identities/bytes; wall-clock diagnostics and unrelated extension configuration do not perturb them.
15. **Installed behavior is the release acceptance owner.** Source helper tests cannot proxy-pass broken wheel/sdist, packaged resources, real Git observer, extension composition, installed CLI/stdout, privacy, or wire behavior.
16. **Repository containment is mandatory.** Orchestrator-owned source/build/test/fixture/script/doc material lives under `orchestrator/`; Protocol workplans remain under `workplans/`; repository CI contains thin invocation only.
17. **The source tree is a maintained human interface.** Core uses a conventional shallow repository layout, obvious module names, and discoverable CLI ownership. Speculative collection directories and blanket private-looking module names are not justified.
18. **Development execution does not require package installation.** A checkout can run current source directly through `orchestrator/sdp.py` without installing/editable-installing `sdp-orchestrator-core`; the launcher uses the same CLI owner and checkout source wins over a stale installed copy.

### 2.2 Tier 1B — Frozen architecture for this cycle

Preserve Architecture 1.6.0:

- capability/dependency ladder `core <- tracker <- adapters <- scheduler`; lower modules never depend on higher modules;
- distribution ladder `sdp-orchestrator-core <- sdp-orchestrator-tracker <- sdp-orchestrator-adapters <- sdp-orchestrator-scheduler`; higher distributions install required lower distributions, while Core alone pulls no higher dependencies;
- one Python 3.11+ Core distribution now, one installer-generated `sdp` entry point, and one thin repository-local launcher dispatching the same CLI implementation;
- native PEP 420 `sdp_orchestrator` namespace and no `sdp_orchestrator/__init__.py`;
- versioned public API namespaces `sdp_orchestrator.core.api.v1`, `.tracker.api.v1`, `.adapters.api.v1`, `.scheduler.api.v1`, with corresponding SPI namespaces;
- one config normalization path, one non-mutating Git observer, one workplan selection owner, one Protocol profile/source owner, and no duplicated workflow authority;
- public Core/Application/Extension API/SPI value boundaries with no implementation objects in public signatures;
- route-independent `PreparedPrompt` before route-sensitive `RenderedPrompt`;
- one extension registry/entry-point group with passive metadata-only discovery and failure-atomic normal activation;
- one exact terminal result-footer/fingerprint wire;
- no persistence, workflow reducer, agent runner, benchmark/resource/scheduler machinery in Core.

Repository containment is Frozen; exact physical subdirectory naming beneath `orchestrator/` is delegated except where §4 fixes the WP-1 layout. Everything beneath product/Frozen boundaries remains Tier 2 and should be altered/reduced rather than wrapped when a simpler equivalent realization exists.

## 3. Required Core behavioral contract

### 3.1 Configuration, project selection, and prompt mode

Use one bounded TOML parser/validator. Prompt-mode precedence is explicit CLI/API -> project default -> core default -> built-in `web`. `PromptExecutionMode(local|web)` is distinct from canonical prompt `EXECUTION_MODE`; Core never silently falls from web to local.

CLI project convenience when `--project` is absent is unique configured project containing cwd -> configured default -> sole project -> structured ambiguous/not-found. Public Core requests use explicit `ProjectKey`.

Core-owned config is closed. Extension namespaces are bounded opaque data interpreted only by their activated extension. Credential-bearing URLs are rejected/redacted. Unrelated extension configuration does not enter Core preparation/prompt identity.

### 3.2 Git/worktree/remote observation

`ObservationPolicy` supports `local_only`, `use_cached_remote`, and `refresh_remote`; programmatic default is local-only. Cached mode performs no network; refresh performs one bounded noninteractive read-only query.

`CandidateRef` identifies repository/worktree, branch/detached state, HEAD, staged/index + unstaged + untracked material state, selected remote/target evidence, provenance/freshness, and identity completeness. `sdp.git-working-tree.v1` includes staged blobs/modes and worktree/untracked content under finite per-file/count/aggregate bounds. Unsupported/unreadable/embedded state gives incomplete identity rather than false completeness. Non-UTF-8 Git paths do not crash identity construction.

Remote selection is configured remote -> branch upstream remote -> origin -> sole remote -> ambiguous/unavailable. Evidence remains bound to the selected remote/target. Filesystem/file remotes are local-only. Web mode requires known target existence, blocks dirty state and known divergence, and preserves ambiguity. Unknown-age cached evidence cannot satisfy an explicit freshness maximum; refresh may establish observation time.

Git subprocesses are bounded, non-mutating, noninteractive, and receive an intentionally constructed environment. Ambient repository/config/object redirection and executable transport command overrides are not inherited merely because they exist.

### 3.3 Workplans and Protocol binding

Catalog bounded regular workplan text under `workplans/active/` and `workplans/archive/`. Symlink aliases/special files/path escapes are ignored/rejected safely. Frontmatter is bounded before/during data-only materialization.

Explicit selectors are exact `workplan_id` or exact canonical repository-relative POSIX path. Traversal/absolute/dot/backslash aliases do not normalize into matches. Current authority uses explicit supersession evidence only; ambiguity remains ambiguity. Lifecycle directory and declared status must agree for current governance.

Stage policies remain:

| Stage | Workplan policy |
| --- | --- |
| baseline | optional explicit only |
| design | optional explicit only |
| implementation | governing workplan required |
| review | governing workplan required |
| verification | optional explicit authority |
| stabilization | optional explicit authority |
| alignment | exact downstream workplan required |
| health-audit | workplan disallowed |
| closeout | optional exact completed binding, otherwise `COMPLETED_WORK` |

A selected authority with a declared Protocol version is reconciled before a lower-precedence project default can determine the governing profile. Required stages fail on missing/invalid/unsupported governing version. An optional explicitly selected authority whose version metadata is absent may remain evidence-only where the stage does not need it to determine the governing contract.

Public `resolve_workplan()` receives a profile-bound `StageRef`; it validates and applies workplan policy under that StageRef's compatible profile identity. It must not re-bootstrap stage semantics from a conflicting project-default profile after the caller already supplies a valid StageRef.

### 3.4 Protocol source/profile/workflow authority

V1 supports compatible Protocol 5.16. Source precedence for the selected profile is configured compatible local source -> exact packaged derivative -> explicitly permitted bounded remote source at an explicit ref -> truthful incompatible/unavailable failure.

A remote source resolves one requested ref to one immutable identity before multi-file use, reads only bounded required data, revalidates the ref, never executes repository/downloaded code, and records requested/resolved provenance/content digests. Local multi-file reads are coherent or fail changed. Packaged resources reproduce exactly from canonical Protocol source and `source/PROTOCOL_VERSION`.

Canonical extraction requires the exact numbered stage-heading set and one fenced text body per stage. Machine profile carries bounded control metadata only. Routing is conservative: context-dependent Protocol outcomes expose alternatives/ambiguity rather than one guessed transition.

### 3.5 Inputs, two-phase identity, and public values

Every canonical INPUT is `mechanical`, `canonical_default`, or `required_user`. Mechanical/first-class bindings cannot be overridden generically. `PROTOCOL_REF` follows the governing contract; `PROTOCOL_SOURCE` defaults `AUTO_LOCAL_FIRST`; canonical `EXECUTION_MODE` is independent of prompt mode. Inserted values use one reversible structure-safe scalar encoding.

`PreparedPrompt` carries RunId, Project/Worktree observation, profile-bound StageRef, candidate, WorkplanResolution, complete WorkflowProfileDescriptor/ProfileRef, PromptSourceRef, resolved mode-independent inputs/provenance, result-schema identity, and `sdp.prompt-preparation.v1`.

Preparation identity binds the complete material public admission surface, including every material `DigestRef` as `{algorithm, canonicalization_scheme, value}`. Render recomputes the fingerprint, revalidates current worktree/remote/workplan/source state, uses the same resolved source snapshot, and performs a final optimistic unchanged-state check before event publication/return.

Public records are immutable JSON-compatible value data. Open event/result payloads accept recursively JSON-compatible values, not live implementation objects. Public timestamps are UTC ISO-8601. `Problem` is one structured error record with `code`, redacted `message/details`, `retryable: bool | None`, and no exception subclass hierarchy.

### 3.6 Prompt wire and events

Canonical body changes only at declared INPUT substitutions. Fingerprint replacement touches only Core-owned fingerprint slots. Opaque RunId remains one coherent JSON-safe value.

Every prompt requests ordinary prose followed by **exactly one** exact-line terminal JSON footer for `StageResultEnvelope v1`. Exactly one begin marker and one end marker must exist; any duplicate/extra exact marker invalidates extraction. Prose may precede; only whitespace may follow the end marker. Additive result fields are allowed only as JSON-compatible values.

Only successful final render emits `core.prompt.rendered.v1`, only to explicitly subscribed sinks. EventId is stable for event type + RunId + prompt fingerprint. Sink failure is diagnosed/redacted but cannot counterfeit the primary result.

### 3.7 Extension composition and passive diagnostics

Core discovers extensions only through `sdp_orchestrator.extensions.v1`. Discovery-only reads installed distribution/entry-point metadata without importing provider code and reports metadata failure truthfully rather than as zero extensions.

Normal activation uses canonical extension ID, SPI/API/multiplicity requirements, hard `requires_extensions`, and actual capability satisfaction from Core/already-active compatible providers. Registrations/subscriptions are staged and committed only after a valid `ExtensionRegistration`; wrong activation return type is failure. Alternative healthy providers may satisfy a capability when another provider fails/cycles. Failed/incompatible providers disable only themselves and truly dependent providers; healthy Core remains available.

`doctor` and default `capabilities` are passive: no provider import, target-repository mutation, or hidden network. Doctor's `packaged_profile` is packaged-only and cannot consult or fall through configured local/remote Protocol-source precedence, including when packaged-profile loading fails.

## 4. Required source tree and CLI ownership

WP-1 Core is the direct Python project rooted at `orchestrator/`:

```text
orchestrator/
  sdp.py
  pyproject.toml
  README.md
  requirements-dev.txt
  src/sdp_orchestrator/core/
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
    api/{__init__.py,v1.py}
    spi/{__init__.py,v1.py}
    resources/protocol/...
  tests/
  docs/
  scripts/
```

No `orchestrator/packages/core` compatibility tree, symlink, or forwarding module remains. Primary implementation modules use descriptive names rather than blanket `_foo.py` names. The supported consumer boundary remains `sdp_orchestrator.core.api.v1` / `.spi.v1`; implementation modules remain internal by API policy rather than leading-underscore convention.

Installed entry point remains:

```toml
[project.scripts]
sdp = "sdp_orchestrator.core.cli:main"
```

`orchestrator/sdp.py` is a thin standard-library development bootstrap only: resolve adjacent `src/`, place it ahead of site-packages, import the same `sdp_orchestrator.core.cli:main`, and execute it. It contains no Typer commands, parsing, validation, project/workplan/profile logic, output logic, or product behavior. It works from arbitrary cwd and wins over an older installed package. Runtime dependencies come from the active Python environment; no vendoring/bundling is introduced.

Future Tracker/Adapters/Scheduler physical roots are added only when those modules are implemented; this does not alter the Frozen distribution/dependency/API ladder.

## 5. Acceptance obligations

O1. **Layout/distribution/launcher:** §4 tree; absence of legacy package/private-module shims; wheel + sdist build/inspect/install; installed entry point and CLI outside checkout; zero-install launcher from arbitrary cwd and with a stale installed package; PEP 420 sibling coexistence; no root namespace init/higher imports.

O2. **Config/projects:** precedence/default/ambiguity, bounded malformed/oversized config, no semantic env override surface, extension namespace preservation, secret URL rejection/redaction, source policy.

O3. **Git/remote:** real temporary Git/worktree/remotes; staged/index/worktree/untracked identity, modes/non-UTF8/bounds, alias vs linked worktree, selected-remote evidence/freshness, no mutation, bounded subprocess/environment behavior, and liveness proof that ambient executable Git transport overrides are not executed by the real remote-query path.

O4. **Workplans:** exact path/ID, branch binding, supersession ambiguity, lifecycle, bounded parser, symlink/path escape, every stage policy and Protocol-binding/precedence case, including public `resolve_workplan()` with a profile-bound StageRef whose profile differs from the project default.

O5. **Protocol/profile/workflow:** exact canonical extraction, package/generator parity, local/packaged/remote coherence, immutable remote identity, unsupported version rejection, conservative routing.

O6. **Public prepare/render:** public API completeness, StageSelector -> profile-bound StageRef, governing-workplan precedence, external admission between phases, complete preparation identity, JSON tamper rejection, optimistic stale checks, no private objects.

O7. **Inputs:** all stages/inputs, required-user completeness, prompt-mode vs canonical execution mode, governing Protocol ref, reversible scalar encoding, atomic invalid failures.

O8. **Renderer/wire/events:** canonical body fidelity, deterministic preparation/prompt fingerprints, exactly-one terminal footer, opaque RunId/placeholder collision behavior, JSON-compatible additive fields, explicit subscription/EventId/failure behavior.

O9. **Privacy/web truth:** final RenderedPrompt/stdout tests for paths/credentials/environment/local remotes/dirty/divergent/stale/absent/ambiguous cases.

O10. **Extensions/diagnostics:** real installed entry-point metadata; passive discovery; compatible/incompatible/missing/cyclic/alternative-provider graphs; staged activation; canonical ID/API/multiplicity/SPI; passive doctor/capabilities with no hidden network/mutation. Doctor failure-path evidence must distinguish packaged-only behavior from both configured valid-local-source consultation and configured remote fallback.

O11. **CLI product/development boundary:** installed `sdp` and zero-install `orchestrator/sdp.py` converge on one `core.cli:main` behavior owner; stdout atomic/prompt-only; failures redacted/nonzero; clipboard additive; representative stage/doctor commands work through both invocation modes.

O12. **Documentation/Frozen authority:** architecture retains all still-Frozen distribution/dependency/API commitments while documenting the shallow WP-1 physical tree; user/developer docs accurately describe exact footer semantics, installed vs zero-install invocation, and public-vs-internal module boundary.

O13. **Final repository acceptance:** complete Core affected regression with Hypothesis active where configured, canonical snapshot generator check, wheel+sdist integration, zero-install launcher regression, ordinary Protocol unit/build/validate/package-parity checks, `git diff --check`, and final simplicity/absence of duplicate authority or higher-module machinery. Record exact assembled candidate identity and commands/results sufficient to establish that these checks actually ran after the final material edit.

Acceptance must execute the real semantic owner. Evidence that could stay green while the final owner is broken does not close the claim.

## 6. Independent Review of candidate `b7d18506d1fb7e07b32db0527c7fece9aa633716` — 2026-09-08

**Verdict: NO-PASS. WP-1 remains reopened. Parent Architecture 1.6.0 remains valid and does not reopen.**

Candidate `b7d18506...` is one implementation commit directly on review authority `90029fb4923110158e0856129bf7b2757cd0bc5b`. The delta is appropriately narrow: one owning-layer service rewire plus deletion of an obsolete helper, and focused test-oracle changes. It adds no resolver, wrapper, compatibility layer, transport abstraction, persistence, or higher-module machinery.

### 6.1 Closed in this candidate

**C1 is closed.** `CoreService.resolve_workplan()` now derives the descriptor from `request.stage.profile_id`, validates the supplied full `StageRef` through the existing `P.stage_descriptor`, then calls the existing `W.resolve`. `_workflow_descriptor_for_project()` was removed. The focused public-API regression covers the conflicting project-default counterexample and unsupported profile identity. This is the intended reduction/rewiring solution and preserves one workplan owner and one Protocol profile/source owner.

**C2 remote-fallback half is closed.** The installed-product doctor test now contains a `remote-only` case with no local root, an intentionally corrupted packaged profile, remote fallback enabled, and a fake Git executable marker. A regression to the known-broken general configured-source resolver would attempt the remote query and trip the marker.

No new evidence reopens the previously closed source-tree, architecture, footer, extension, digest-identity, Git-environment, public-value, or documentation families.

### D1 — The doctor "valid-local" adversarial case is still not a valid local Protocol source

**Authority:** Tier 1A invariant 15; §3.7; O10; Protocol 5.16 proxy-proof/oracle-strength rules.

`orchestrator/tests/test_installed_product.py` defines `PACKAGE_ROOT = Path(__file__).resolve().parents[1]`, which is the repository's `orchestrator/` directory. The new test passes `PACKAGE_ROOT` as the `local_root` for its `valid-local` subcase. But the real local Protocol-source owner resolves `source/PROTOCOL_VERSION` and `source/shared/references/development-workflow-prompts.md` beneath `local_root`. Those paths exist beneath the repository root, not beneath `orchestrator/`.

Therefore the supposedly valid-local subcase still exercises an invalid/missing local source. A broken doctor implementation that consults configured local source state can fail immediately on that invalid root and still satisfy the subcase's current `packaged_profile_problem` assertions. The `remote-only` subcase correctly protects the remote-fallback half, but O10 requires installed evidence that configured **valid local source** also cannot affect doctor.

**Repair:** change the existing test fixture only. Point the local-source case at the actual repository root containing `source/PROTOCOL_VERSION` and `source/shared/references/development-workflow-prompts.md` (for this test layout, derive it from the existing package root rather than hard-coding a machine path). Keep the installed wheel's packaged profile corrupted. Under correct packaged-only doctor behavior, the command must still report `packaged_profile_problem`; under a broken configured-local-source path, the valid local source would succeed and the test must fail. Retain the separate remote-only fake-Git marker case. Do not change production doctor code or introduce new source/network abstractions.

### D2 — Exact assembled-candidate final acceptance is still not evidenced

**Authority:** O13 and Protocol 5.16 final affected-regression/integration requirements.

Candidate `b7d18506...` has no GitHub status contexts, no check runs, and no Actions runs. Its commit message does not carry the required final commands/results, and the active workplan still contains no exact-candidate execution record. The independent Review environment attempted an exact checkout for runtime falsification, but outbound DNS/network access from that execution environment was unavailable; no independent runtime pass is claimed.

**Repair:** after D1, run final acceptance on the resulting exact assembled candidate and record concise evidence tied to that exact commit. No new evidence manifest, framework, or reporting subsystem is needed.

Minimum final execution set:

1. focused D1 plus the already-present C1, digest-identity, Git transport-helper, explicit-workplan precedence, duplicate-footer, extension/provider, public-record, and doctor remote-only regressions;
2. complete Core regression with Hypothesis active where configured;
3. installed extension composition/passive diagnostics and public API-SPI/wire/privacy suites;
4. real Git/remote non-mutation and environment-boundary tests;
5. canonical profile/snapshot generator parity;
6. wheel and sdist build/inspection/install plus installed CLI outside checkout;
7. zero-install `orchestrator/sdp.py` from arbitrary cwd, including checkout-source precedence over a stale installed package;
8. structural absence checks for legacy package/private-path compatibility and duplicate CLI authority;
9. ordinary Protocol regression, skill build/validate/package parity, and `git diff --check`.

Record the exact candidate SHA and command/result summary after the final material edit. A required check that did not execute is not a pass.

## 7. Re-review gate

Return WP-1 to independent Review only after D1-D2 close on one exact assembled candidate. Preserve the C1 closure and do not revisit previously closed architecture/layout/footer/extension/digest/Git families without new contradicting evidence.

**Current routing: NO-PASS -> `software-implementation`. Correct the existing doctor valid-local test fixture, execute and record final assembled acceptance, then resubmit the exact candidate.**
