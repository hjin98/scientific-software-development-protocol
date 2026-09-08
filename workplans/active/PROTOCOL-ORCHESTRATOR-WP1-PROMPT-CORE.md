---
kind: implementation-workplan
workplan_id: PROTOCOL-ORCHESTRATOR-WP1-PROMPT-CORE
protocol_version: 5.16.0
status: reopened
reviewed_date: 2026-09-08
reviewed_candidate: 5562a426df24e82621bd94756cb1c0c70cdc1cb1
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

WP-1 delivers the smallest independently useful SDP Orchestrator: one installable `sdp-orchestrator-core` distribution, one installer-generated `sdp` console command, and one repository-local zero-install `orchestrator/sdp.py` development launcher. Both invocation paths execute the same Core CLI owner. Core observes a configured repository, resolves the governing workplan and compatible Protocol 5.16 profile/source, prepares a route-independent public record, renders one complete local/web stage prompt, requests the versioned terminal result envelope, and composes optional extensions through one public SPI.

Core-only operation is a finished product mode. It requires no Tracker, Adapters, Scheduler, persistence, agent runner, model/account catalog, benchmark catalog, quota/resource predictor, or AUTO scheduler.

This workplan is governed by Protocol 5.16.0 and Frozen `orchestrator/docs/architecture.md` Architecture 1.6.0. Canonical human-facing stage prose remains `source/shared/references/development-workflow-prompts.md`; packaged prompt/profile resources are reproducible derivatives, not competing authorities.

This file is the snapshot-complete current WP-1 handoff. Superseded repair chronology is non-normative history; all still-binding product/Frozen semantics and current blockers are carried below.

## 2. Product and Frozen invariants

### 2.1 Tier 1A — stakeholder/product invariants

1. **Core works alone.** Config, project/worktree observation, workplan/profile/source resolution, prepare, render, CLI, and diagnostics work without higher modules.
2. **Observation is non-mutating.** Inspection does not change worktree content, index, HEAD, refs, remote-tracking refs, or remotes. Refresh is a bounded read-only query, never fetch/pull.
3. **Prompt/workflow authority is singular.** Canonical Protocol source owns stage prose/workflow meaning; package resources/tests do not become semantic authorities.
4. **Protocol binding is explicit and precedence-correct.** A selected governing workplan's declared Protocol contract is never silently ignored or vetoed by a lower-precedence project default. Unsupported/incompatible authority fails truthfully.
5. **Ambiguity remains explicit.** Project/workplan/profile/source/remote/stage/routing ambiguity fails or remains ambiguous rather than using fuzzy names, recency, ordering, or undocumented heuristics.
6. **Prompt context is truthful.** Web mode never represents dirty/local-only/known-divergent state as remotely inspectable; local mode may reference the authorized worktree.
7. **Privacy/security guarantees are bounded and truthful.** Automatically derived web content excludes private local paths, credential-bearing remote userinfo, ambient environment values, credential-helper output, and private orchestrator state. User-authored task/input text is intentional content.
8. **Core v1 is the durable lower seam.** Higher modules consume documented `api.v1`/`spi.v1` value records/protocols only; no private implementation objects or duplicated workplan/profile logic cross the boundary.
9. **One composition root.** Core owns the CLI, service registry, extension entry-point group, and event-subscription seam.
10. **Manual tracking compatibility exists from day one.** Every successful prompt requests exactly one terminal `StageResultEnvelope v1` bound to RunId/prompt fingerprint and emits only the subscribed non-durable prompt event.
11. **Admission precedes route-sensitive render.** `prepare()` is route-independent; later admission can occur before `render()` without provisional prompt/event side effects.
12. **Stage identity is profile-bound.** User input is a `StageSelector`; `StageRef` exists only after compatible profile resolution.
13. **Render consistency is optimistic but coherent.** Material candidate/workplan/source/selection drift between prepare and final return yields stale/incoherent failure, not a mixed snapshot. WP-1 introduces no repository lock/persistence.
14. **Determinism follows semantic state.** Fixed RunId + unchanged material state yields stable identities/bytes; wall-clock diagnostics and unrelated extension configuration do not perturb them.
15. **Installed behavior is the release acceptance owner.** Source helper tests cannot proxy-pass broken wheel/sdist, packaged resources, real Git observer, extension composition, installed CLI/stdout, privacy, or wire behavior.
16. **Repository containment is mandatory.** Orchestrator-owned source/build/test/fixture/script/doc material lives under `orchestrator/`; Protocol workplans remain under `workplans/`; repository CI contains thin invocation only.
17. **The source tree is a maintained human interface.** Core uses a conventional shallow repository layout, obvious module names, and discoverable CLI ownership. Speculative collection directories and blanket private-looking module names are not justified.
18. **Development execution does not require package installation.** A checkout can run the current source directly through `orchestrator/sdp.py` without installing/editable-installing `sdp-orchestrator-core`; the launcher uses the same CLI owner and checkout source wins over a stale installed copy.

### 2.2 Tier 1B — Frozen architecture for this cycle

Preserve Architecture 1.6.0:

- capability/dependency ladder `core <- tracker <- adapters <- scheduler`; lower modules never depend on higher modules;
- distribution ladder `sdp-orchestrator-core <- sdp-orchestrator-tracker <- sdp-orchestrator-adapters <- sdp-orchestrator-scheduler`; when higher distributions are implemented/installed, they install their required lower distributions, while Core alone pulls no higher dependencies;
- one Python 3.11+ Core distribution now, one installer-generated `sdp` entry point, and one thin repository-local development launcher dispatching the same CLI implementation;
- native PEP 420 `sdp_orchestrator` namespace and no `sdp_orchestrator/__init__.py`;
- future versioned public API namespaces remain `sdp_orchestrator.core.api.v1`, `.tracker.api.v1`, `.adapters.api.v1`, `.scheduler.api.v1`; corresponding provider SPI namespaces remain `.core.spi.v1`, `.tracker.spi.v1`, `.adapters.spi.v1`, `.scheduler.spi.v1`;
- one config normalization path, one non-mutating Git observer, one workplan selection owner, one Protocol profile/source owner, and no duplicated workflow authority;
- public Core/Application/Extension API/SPI value boundaries; no implementation objects in public signatures;
- route-independent `PreparedPrompt` before route-sensitive `RenderedPrompt`;
- one extension registry/entry-point group with passive metadata-only discovery and failure-atomic normal activation;
- one exact terminal result-footer/fingerprint wire;
- no persistence, workflow reducer, agent runner, benchmark/resource/scheduler machinery in Core.

Repository containment is Frozen; exact physical subdirectory naming beneath `orchestrator/` is delegated unless explicitly fixed below. Everything beneath the product/Frozen boundaries remains Tier 2 and should be altered/reduced rather than wrapped when a simpler equivalent realization exists.

## 3. Required Core behavioral contract

### 3.1 Configuration, project selection, and prompt mode

Use one bounded TOML parser/validator. Prompt-mode precedence is explicit CLI/API -> project default -> core default -> built-in `web`. `PromptExecutionMode(local|web)` is distinct from canonical prompt `EXECUTION_MODE`; Core never silently falls from web to local.

CLI project convenience when `--project` is absent is unique configured project containing cwd -> configured default -> sole project -> structured ambiguous/not-found. Public Core requests use explicit `ProjectKey`.

Core-owned config is closed. Extension namespaces are bounded opaque data interpreted only by their activated extension. Credential-bearing URLs are rejected/redacted. Unrelated extension configuration does not enter Core preparation/prompt identity.

### 3.2 Git/worktree/remote observation

`ObservationPolicy` supports `local_only`, `use_cached_remote`, and `refresh_remote`; programmatic default is local-only. Cached mode performs no network; refresh performs one bounded noninteractive read-only query.

`CandidateRef` identifies repository/worktree, branch/detached state, HEAD, staged/index + unstaged + untracked material state, selected remote/target evidence, provenance/freshness, and identity completeness. `sdp.git-working-tree.v1` includes staged blobs/modes and worktree/untracked content under finite per-file/count/aggregate bounds. Unsupported/unreadable/embedded state gives incomplete identity rather than false completeness. Non-UTF-8 Git paths do not crash identity construction.

Remote selection is configured remote -> branch upstream remote -> origin -> sole remote -> ambiguous/unavailable. Evidence remains bound to the selected remote/target. Filesystem/file remotes are local-only. Web mode requires known target existence, blocks dirty state and known divergence, and preserves ambiguity. Unknown-age cached evidence cannot satisfy an explicit freshness maximum; a refresh may establish observation time.

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

### 3.4 Protocol source/profile/workflow authority

V1 supports the explicitly compatible Protocol 5.16 profile. Source precedence for the selected profile is configured compatible local source -> exact packaged derivative -> explicitly permitted bounded remote source at an explicit ref -> truthful incompatible/unavailable failure.

A remote source resolves one requested ref to one immutable identity before multi-file use, reads only bounded required data, revalidates the ref, never executes repository/downloaded code, and records requested/resolved provenance/content digests. Local multi-file reads are coherent or fail changed. Packaged resources reproduce exactly from canonical Protocol source and `source/PROTOCOL_VERSION`.

Canonical extraction requires the exact numbered stage-heading set and one fenced text body per stage. The machine profile carries bounded control metadata only. Routing is conservative: context-dependent Protocol outcomes expose alternatives/ambiguity rather than one guessed transition.

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

`doctor` and default `capabilities` are passive: no provider import, target-repository mutation, or hidden network. Doctor's `packaged_profile` is packaged-only and cannot fall through configured local/remote source precedence.

## 4. Required source tree and CLI ownership

WP-1 Core is the direct Python project rooted at `orchestrator/`:

```text
orchestrator/
  sdp.py
  pyproject.toml
  README.md
  requirements-dev.txt
  src/
    sdp_orchestrator/
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
        api/{__init__.py,v1.py}
        spi/{__init__.py,v1.py}
        resources/protocol/...
  tests/
  docs/
  scripts/
```

No `orchestrator/packages/core` compatibility tree, symlink, or forwarding module remains. Primary implementation modules use descriptive names rather than blanket `_foo.py` names. The supported consumer boundary remains `sdp_orchestrator.core.api.v1` / `.spi.v1`; implementation modules remain internal by API policy rather than by leading underscore convention.

Installed entry point:

```toml
[project.scripts]
sdp = "sdp_orchestrator.core.cli:main"
```

`orchestrator/sdp.py` is a thin standard-library development bootstrap only: resolve adjacent `src/`, place it ahead of site-packages, import the same `sdp_orchestrator.core.cli:main`, and execute it. It contains no Typer commands, parsing, validation, project/workplan/profile logic, output logic, or other product behavior. It works from arbitrary cwd and wins over an older installed package. Runtime dependencies still come from the active Python environment; no vendoring/bundling is introduced.

Future Tracker/Adapters/Scheduler physical roots are added only when those modules are implemented; this does not alter the Frozen distribution/dependency/API ladder.

## 5. Acceptance obligations

O1. **Layout/distribution/launcher:** required §4 tree; absence of legacy package/private-module shims; wheel + sdist build/inspect/install; installed entry point; installed CLI outside checkout; zero-install launcher from arbitrary cwd and with a stale installed package; PEP 420 sibling coexistence; no root namespace init/higher imports.

O2. **Config/projects:** precedence/default/ambiguity, bounded malformed/oversized config, no semantic env override surface, extension namespace preservation, secret URL rejection/redaction, source policy.

O3. **Git/remote:** real temporary Git/worktree/remotes; staged/index/worktree/untracked identity, modes/non-UTF8/bounds, alias vs linked worktree, selected-remote evidence/freshness, no mutation, bounded subprocess/environment behavior.

O4. **Workplans:** exact path/ID, branch binding, supersession ambiguity, lifecycle, bounded parser, symlink/path escape, every stage policy and Protocol-binding/precedence case.

O5. **Protocol/profile/workflow:** exact canonical extraction, package/generator parity, local/packaged/remote coherence, immutable remote identity, unsupported version rejection, conservative routing.

O6. **Public prepare/render:** public API completeness, StageSelector -> profile-bound StageRef, governing-workplan precedence, external admission between phases, complete preparation identity, JSON tamper rejection, optimistic stale checks, no private objects.

O7. **Inputs:** all stages/inputs, required-user completeness, prompt-mode vs canonical execution mode, governing Protocol ref, reversible scalar encoding, atomic invalid failures.

O8. **Renderer/wire/events:** canonical body fidelity, deterministic preparation/prompt fingerprints, exactly-one terminal footer, opaque RunId/placeholder collision behavior, JSON-compatible additive fields, explicit subscription/EventId/failure behavior.

O9. **Privacy/web truth:** final RenderedPrompt/stdout tests for paths/credentials/environment/local remotes/dirty/divergent/stale/absent/ambiguous cases.

O10. **Extensions/diagnostics:** real installed entry-point metadata; passive discovery; compatible/incompatible/missing/cyclic/alternative-provider graphs; staged activation; canonical ID/API/multiplicity/SPI; passive doctor/capabilities with no hidden network/mutation.

O11. **CLI product/development boundary:** installed `sdp` and zero-install `orchestrator/sdp.py` converge on one `core.cli:main` behavior owner; stdout atomic/prompt-only; failures redacted/nonzero; clipboard additive; representative stage/doctor commands work through both supported invocation modes.

O12. **Documentation/Frozen authority:** architecture retains all still-Frozen distribution/dependency/API commitments while documenting the shallow WP-1 physical tree; user/developer docs accurately describe exact footer semantics, installed vs zero-install invocation, and the public-vs-internal module boundary.

O13. **Final repository acceptance:** complete Core affected regression with Hypothesis active where configured, canonical snapshot generator check, wheel+sdist integration, zero-install launcher regression, ordinary Protocol unit/build/validate/package-parity checks, `git diff --check`, and final simplicity/absence of duplicate authority or higher-module machinery.

Acceptance must execute the real semantic owner. Evidence that could stay green while the final owner is broken does not close the claim.

## 6. Independent Review of candidate `5562a426df24e82621bd94756cb1c0c70cdc1cb1` — 2026-09-08

**Verdict: NO-PASS. WP-1 remains reopened.**

The candidate is one implementation commit directly on the accepted WP-1 amendment. The structural simplification is successful at source level: `orchestrator/packages/core` is gone, Core is rooted directly under `orchestrator/`, primary modules are descriptively named, `sdp.py` is thin, and installed metadata targets `sdp_orchestrator.core.cli:main`.

Source inspection also shows substantial closure of the prior F1-F9 defects: routing now preserves blocker alternatives; extension activation uses actual active capability satisfaction and rejects invalid SPI returns; complete DigestRef fields participate in preparation identity; doctor calls packaged resolution directly; the footer extractor rejects duplicate exact markers; explicit optional plans with unsupported declared versions reject; public open records enforce JSON/UTC boundaries; executable Git transport environment overrides are removed; and the source/launcher migration is present.

Those repairs do not close the candidate because the following blockers remain. They are existing-authority conformance/acceptance failures; the parent architecture does not require redesign.

### B1 — Explicit selected-workplan Protocol precedence is still ordered incorrectly in `prepare()`

`CoreService.prepare()` first resolves `context.section.protocol_profile` as a bootstrap source, and only afterward resolves `request.workplan_selector`. Therefore a lower-precedence project-default profile can fail before an explicitly selected workplan's declared Protocol version is even examined.

Counterexample: configure the project with unsupported `protocol_profile = "sdp-protocol-9.9"`; explicitly select an exact active workplan declaring compatible `protocol_version = "5.16.0"`; request Implementation (or another stage where the selected plan is governing). The accepted contract says the selected authority's declared Protocol contract takes precedence over project defaults. Current ordering instead raises profile/source incompatibility from the project default before the selected workplan can govern.

**Repair:** rewire the existing preparation/catalog/selection flow so an explicit exact selector's already-existing workplan metadata is available early enough to determine/reconcile its declared Protocol version before project-default profile bootstrap. Reuse the existing exact-selector semantics and one catalog/selection owner; do not implement a second selector/resolver or wrapper. After the governing profile is known, apply the real stage policy and lifecycle/authority validation through the same workplan resolution owner.

**Required tests:**
- compatible explicitly selected required-stage workplan succeeds even when project default names an unsupported different profile;
- compatible explicitly selected optional authority with a declared version likewise binds/reconciles before the project default;
- unsupported selected workplan still fails;
- optional selected workplan with absent version retains the accepted evidence-only fallback;
- no selector continues to use the configured/default profile normally.

### B2 — Implementation edited Frozen parent architecture beyond the authorized layout reconciliation

The accepted Architecture 1.6.0 explicitly fixes the distribution ladder semantics: installing a higher distribution installs required lower distributions, and it names future versioned public APIs for Core, Tracker, Adapters, and Scheduler. The implementation was authorized to replace the illustrative `orchestrator/packages/core/...` physical layout because exact subdirectory naming was delegated. It was not authorized to delete those still-Frozen future distribution/public-API commitments.

Candidate `orchestrator/docs/architecture.md` replaced the installation statement with WP-1-only wording and removed the future `tracker.api.v1`, `adapters.api.v1`, and `scheduler.api.v1` entries while leaving the document at Architecture 1.6.0 / status Frozen. That is Tier-1B authority drift, not a necessary consequence of the source-tree simplification.

**Repair:** restore the still-Frozen distribution installation/dependency semantics and the full future public API namespace list in Architecture 1.6.0. Keep the new shallow WP-1 layout example and clarify that future physical package roots are deferred/delegated until those modules are implemented. Do not create future package directories or compatibility scaffolding. Do not change architecture version/semantics unless a genuine Design reopen is separately justified.

### B3 — Durable user/developer documentation still contradicts the accepted product contract

The code-side F5 repair is correct, but `orchestrator/docs/core-user-guide.md` still says the **last** exact begin marker starts the result footer. The accepted wire and current extractor instead require exactly one begin marker and one end marker; any extra exact marker invalidates extraction. This is a direct user-facing contract contradiction.

The Development section also begins with an editable-install command even though the accepted development mode is explicitly usable without installing/editable-installing the orchestrator. The guide already contains the zero-install launcher; the development entry should not make installation appear prerequisite.

**Repair:** alter the existing guide only. State the exact unique-marker rule and rejection of any extra exact begin/end marker. Present `python orchestrator/sdp.py ...` as the default checkout execution path; if editable installation is retained as an optional convenience, label it optional. Keep runtime dependency ownership in `pyproject.toml`/existing development dependency files rather than duplicating dependency lists in prose.

### B4 — Required exact-candidate acceptance is incomplete both in definition and execution evidence

The workplan explicitly invalidated most pre-migration evidence because F9 moved package/import/launcher boundaries. Candidate `5562a426...` does not record a fresh final affected-regression/integration/project-check run in the workplan or another supplied current acceptance artifact. The repository CI workflow runs on `main` pushes or pull requests, so this branch-head commit has no GitHub status contexts. The independent review environment could inspect the exact GitHub source but could not obtain a runnable checkout; no independent runtime rerun is claimed.

In addition, several focused counterexamples required by the accepted F1-F9 repair contract are still absent from the candidate test source:

1. **Digest identity matrix:** current regression mutates one prompt-source digest scheme, but acceptance requires algorithm and canonicalization-scheme tampering across material candidate/workplan/profile/source DigestRefs.
2. **Passive doctor failure path:** current installed doctor smoke covers the happy path, but acceptance requires a forced packaged-profile failure while local/remote source configuration is present and proof that doctor performs zero remote fallback/query.
3. **Git executable override liveness:** current test checks that `GIT_SSH*` variables are absent from `_git_env()`, but acceptance requires a test-owned ambient executable helper/marker exercised through the relevant remote-query path and proof that the helper is not executed.
4. **B1 precedence counterexample:** the newly identified explicit-workplan-before-project-default case must be executable regression, not source reasoning only.

**Repair:** add only focused tests at the existing real owners; no new test framework, transport abstraction, resolver, or diagnostic layer. Then execute and record the exact assembled candidate's required acceptance. Existing tests may be parameterized/consolidated rather than duplicated.

## 7. Re-review gate

Return WP-1 to independent Review only after B1-B4 are closed on one exact assembled candidate.

Required final evidence:

1. focused B1 plus complete F1-F9 counterexamples, including the DigestRef matrix, passive-doctor no-network failure path, and ambient Git-helper non-execution;
2. complete Core affected regression with Hypothesis active where configured;
3. real installed extension composition and passive diagnostics;
4. preparation/public API-SPI/wire/privacy tests;
5. real Git/remote non-mutation and environment-boundary tests;
6. canonical profile/snapshot generator parity;
7. wheel and sdist build/inspection/install plus installed CLI outside checkout;
8. zero-install `orchestrator/sdp.py` from arbitrary cwd, including checkout-source precedence over a stale installed package;
9. repository structural absence checks proving no legacy package/private-path compatibility layer or duplicate CLI implementation;
10. ordinary Protocol regression, skill build/validate/package parity, and `git diff --check`;
11. architecture/user-guide reconciliation showing no Tier-1B semantic deletion and no stale footer/install guidance.

Record exact candidate identity and commands/results sufficient to establish that the checks actually ran after the final material edit. Still-valid evidence may be reused only where the changed dimension cannot plausibly affect the claim.

**Current verdict: NO-PASS — return to `software-implementation`; repair B1 by reordering existing ownership, restore the unintentionally deleted Frozen architecture statements, correct the existing guide, complete the focused acceptance tests, then rerun final assembled acceptance and submit the exact candidate for fresh Review.**
