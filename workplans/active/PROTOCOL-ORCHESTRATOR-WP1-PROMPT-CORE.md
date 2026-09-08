---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: reopened
reviewed_date: 2026-09-08
reviewed_candidate: 442fc776b0999363d81179e4706e7732661cb266
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

This file is the snapshot-complete current WP-1 handoff. Superseded repair chronology is non-normative Git history; all still-binding product/Frozen semantics and current blockers are represented below.

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

O10. **Extensions/diagnostics:** real installed entry-point metadata; passive discovery; compatible/incompatible/missing/cyclic/alternative-provider graphs; staged activation; canonical ID/API/multiplicity/SPI; passive doctor/capabilities with no hidden network/mutation. Doctor failure-path evidence must distinguish a correct packaged-only path from the known-broken configured local/remote resolution path.

O11. **CLI product/development boundary:** installed `sdp` and zero-install `orchestrator/sdp.py` converge on one `core.cli:main` behavior owner; stdout atomic/prompt-only; failures redacted/nonzero; clipboard additive; representative stage/doctor commands work through both invocation modes.

O12. **Documentation/Frozen authority:** architecture retains all still-Frozen distribution/dependency/API commitments while documenting the shallow WP-1 physical tree; user/developer docs accurately describe exact footer semantics, installed vs zero-install invocation, and public-vs-internal module boundary.

O13. **Final repository acceptance:** complete Core affected regression with Hypothesis active where configured, canonical snapshot generator check, wheel+sdist integration, zero-install launcher regression, ordinary Protocol unit/build/validate/package-parity checks, `git diff --check`, and final simplicity/absence of duplicate authority or higher-module machinery. Record exact assembled candidate identity and commands/results sufficient to establish that these checks actually ran after the final material edit.

Acceptance must execute the real semantic owner. Evidence that could stay green while the final owner is broken does not close the claim.

## 6. Independent Review of candidate `442fc776b0999363d81179e4706e7732661cb266` — 2026-09-08

**Verdict: NO-PASS. WP-1 remains reopened. Parent Architecture 1.6.0 remains valid and does not reopen.**

The candidate is one implementation commit directly on review authority `4482ec3b9174c60bac41d9231800ea512247232c`. Its eight-file delta is appropriately narrow: existing workplan/profile resolution owners, Frozen/user documentation, and focused tests. It introduces no new resolver, wrapper hierarchy, transport layer, persistence, or higher-module machinery.

### 6.1 Confirmed closure since the previous Review

- The shallow source tree, descriptive module names, installed `sdp` entry point, and thin zero-install `orchestrator/sdp.py` remain aligned.
- `prepare()` now looks up an explicit exact workplan from the existing catalog before project-profile bootstrap and then returns to the existing `W.resolve` owner for stage-policy/lifecycle validation. The previously reported explicit required/optional workplan precedence counterexamples are covered by focused tests.
- Architecture 1.6.0 again states higher-distribution -> lower-distribution installation semantics, retains the shallow WP-1 layout, defers future physical roots without scaffolding, and restores all future API/SPI namespace commitments.
- The user guide now requires exactly one begin/end result marker and makes the zero-install launcher the normal checkout-development path; editable installation is explicitly optional.
- The preparation-identity regression now varies both `DigestRef.algorithm` and `canonicalization_scheme` across candidate, workplan, profile, and prompt-source material digests.
- The Git regression now arms an ambient executable `GIT_SSH_COMMAND` helper and exercises the real refreshed remote-observation path, proving the helper is not executed.
- Production `doctor` remains correctly implemented through direct packaged-only resolution.

These closures do not justify a parent redesign and should not be reopened absent new evidence.

### C1 — Public `resolve_workplan()` still reinterprets a profile-bound StageRef through the project default

**Authority:** Tier 1A invariants 4, 8, and 12; §3.3; O4/O6; Frozen Core v1 value-boundary semantics.

`PromptPreparationRequest` was repaired, but the public sibling `CoreService.resolve_workplan()` still calls `_workflow_descriptor_for_project(context)`, which loads `context.section.protocol_profile`, before applying the request's already profile-bound `StageRef`. This allows a lower-precedence or unsupported project default to veto a valid StageRef produced under the governing workplan/profile.

Concrete counterexample:

1. Project config names unsupported `protocol_profile = "sdp-protocol-9.9"`.
2. A compatible workplan declaring Protocol 5.16 is resolved/cataloged and `workflow(WorkflowRequest(workplan=<ref>))` yields the compatible 5.16 descriptor.
3. The caller passes that descriptor's Implementation `StageRef` plus the exact workplan selector to public `resolve_workplan()`.
4. Current `resolve_workplan()` tries the project's 9.9 profile before honoring the supplied 5.16 StageRef and fails for the wrong authority.

**Repair:** alter the existing `resolve_workplan()` ownership path so stage validation is derived from `request.stage.profile_id` through the existing Protocol-source/profile owner, then validate the full `StageRef` with the existing `P.stage_descriptor`, and call the existing `W.resolve`. Do not add another resolver or compatibility wrapper. If `_workflow_descriptor_for_project()` becomes unused, remove it rather than retaining dead bootstrap machinery.

**Required regression:** exercise the public `CoreAPI.resolve_workplan()` counterexample above. A compatible profile-bound StageRef must not be vetoed by an unrelated unsupported project default; a mismatched/unsupported StageRef must still fail truthfully. Preserve ordinary configured/default behavior where no already-bound StageRef overrides it.

### C2 — The new passive-doctor adversarial test can still pass the known-broken configured-source behavior

**Authority:** Tier 1A invariant 15; §3.7; O10; Protocol 5.16 proxy-proof/oracle-strength rules.

Production `doctor` is correct, but its new installed-product failure-path test is not yet a discriminating oracle. The test corrupts the packaged profile, configures both `local_root` and remote fallback, but makes `local_root` nonexistent. Under the previously broken implementation that called general configured Protocol-source resolution, `resolve()` would fail immediately on that nonexistent local root before reaching the packaged snapshot or remote query. The CLI could still emit `packaged_profile_problem`, the fake Git marker would remain absent, and every current assertion could pass while `doctor` was incorrectly consulting configured source state.

**Repair:** strengthen the existing test, not the product. The test must make the known-broken configured-source path observably differ from packaged-only behavior. A minimal repair is either:

- use a valid configured local Protocol source while corrupting the installed packaged profile, so any accidental local-source consultation would incorrectly succeed and fail the packaged-only assertion; and separately arm remote fallback with no local short-circuit to prove no remote query after packaged failure; or
- split these into two focused cases using the existing installed-product harness: one valid-local-source isolation case and one no-local-root + fake-Git remote-fallback trap.

Do not introduce a network abstraction, doctor-specific resolver, or new test framework.

### C3 — Exact assembled-candidate final acceptance is still not evidenced

**Authority:** O13 and the Re-review gate; Protocol 5.16 final affected-regression/integration requirements.

No GitHub status context, check run, or Actions run exists for candidate `442fc776b0999363d81179e4706e7732661cb266`, and the implementation commit does not record the required final assembled commands/results. The Review environment could inspect the exact GitHub source but could not obtain a runnable checkout, so it does not substitute an independent execution claim.

**Repair:** after C1/C2 and any resulting material edits, run final acceptance on one exact assembled candidate and record concise evidence tied to that candidate. No evidence manifest or new reporting subsystem is required.

Minimum final execution set:

1. focused C1/C2 plus the already-added digest/Git/explicit-precedence regressions;
2. complete Core regression with Hypothesis active where configured;
3. installed extension composition/passive diagnostics and public API-SPI/wire/privacy suites;
4. real Git/remote non-mutation and environment-boundary tests;
5. canonical profile/snapshot generator parity;
6. wheel and sdist build/inspection/install plus installed CLI outside checkout;
7. zero-install `orchestrator/sdp.py` from arbitrary cwd, including checkout-source precedence over a stale installed package;
8. repository structural absence checks for legacy package/private-path compatibility and duplicate CLI authority;
9. ordinary Protocol regression, skill build/validate/package parity, and `git diff --check`.

## 7. Re-review gate

Return WP-1 to independent Review only after C1-C3 close on one exact assembled candidate. Do not reopen already-closed architecture/layout/footer/extension/digest/Git families unless new evidence materially contradicts them.

**Current routing: NO-PASS -> `software-implementation`. Rewire the existing public `resolve_workplan()` profile ownership, strengthen the existing doctor adversarial oracle, execute final assembled acceptance, and resubmit the exact candidate.**
