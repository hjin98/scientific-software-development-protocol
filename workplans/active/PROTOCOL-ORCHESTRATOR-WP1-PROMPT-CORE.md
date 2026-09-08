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

## 1. Current authority and objective

WP-1 delivers the smallest independently useful Protocol Orchestrator: an installable `sdp-orchestrator-core` distribution and `sdp` CLI that observe a configured repository, resolve the governing workplan and compatible Protocol 5.16 workflow/profile, prepare a route-independent public record, render one complete local/web stage prompt, request a structured terminal result envelope, and compose optional extensions through one public SPI.

Core-only operation is a finished product mode. It must not require Tracker, Adapters, Scheduler, persistence, agent execution, model/account catalogs, benchmarking, quota/resource prediction, or AUTO scheduling.

This workplan is governed by `orchestrator/docs/architecture.md` version 1.6.0 and Protocol 5.16.0. The canonical human-facing prompt authority is `source/shared/references/development-workflow-prompts.md`; packaged prompt/profile resources are reproducible derivatives only.

Repeated implementation-review history has been consolidated into this current snapshot. Earlier R1-R11 labels are no longer a separate normative patch log: every still-binding semantic end state is carried below under the product/Frozen contract, acceptance obligations, and current open findings. Git history may retain the chronology, but it is not required to recover the active contract.

## 2. Authority classes

### 2.1 Problem / product invariants (Tier 1A)

1. **Core works alone.** Configuration, project/worktree observation, workplan selection, compatible profile/source resolution, prepare, render, CLI, and required diagnostics work without higher modules.
2. **Observation is non-mutating.** Core inspection does not change target worktree content, index, HEAD, refs, remote-tracking refs, or remotes. Explicit refresh is a bounded read-only query, never fetch/pull.
3. **Prompt/workflow authority is singular.** Canonical Protocol source owns stage prose and workflow meaning; packaged resources and tests do not become competing semantic authorities.
4. **Protocol binding is explicit.** A workplan governed by Protocol X is never silently interpreted under an incompatible newer profile. A semantic version is never guessed into a Git ref.
5. **Ambiguity remains explicit.** Project/workplan/profile/source/remote/stage/routing ambiguity fails or remains ambiguous rather than using fuzzy names, recency, ordering, or undocumented heuristics.
6. **Prompt context is truthful.** Web mode never represents dirty/local-only or known-divergent state as remotely inspectable; local mode may reference the authorized worktree.
7. **Privacy/security guarantees are bounded and truthful.** Automatically derived web prompt content excludes private local paths, credential-bearing remote userinfo, ambient environment values, credential-helper output, and private orchestrator state. User-authored task/input text is intentional content, not subject to a fictitious arbitrary-secret detector.
8. **Core v1 is the durable lower seam.** Higher modules consume only documented `api.v1`/`spi.v1` value records/protocols; no private implementation objects or duplicated workplan/profile logic cross the boundary.
9. **One composition root.** Core owns the single CLI, service registry, extension entry-point group, and event-subscription seam.
10. **Manual tracking compatibility exists from day one.** Every successful final prompt requests exactly one terminal `StageResultEnvelope v1` associated with RunId/prompt fingerprint and emits only the subscribed non-durable prompt event.
11. **Admission precedes final route-sensitive render.** `prepare()` is route-independent; later Adapter/Scheduler admission can occur before `render()` without provisional prompt/event side effects.
12. **Stage identity is profile-bound.** User input is a `StageSelector`; a `StageRef` exists only after compatible profile resolution.
13. **Render consistency is optimistic but coherent.** Material candidate/workplan/source/selection drift between prepare and final return produces stale/incoherent failure, not a mixed snapshot. No WP-1 repository lock/persistence is introduced.
14. **Determinism follows semantic state.** Fixed RunId + unchanged material preparation/mode/input state yields stable identities/bytes; wall-clock diagnostics and unrelated extension configuration do not perturb them.
15. **Installed behavior is the acceptance owner.** Source helper tests cannot proxy-pass a broken wheel/sdist, packaged profile, real Git observer, entry-point composition, CLI/stdout, or final privacy/wire behavior.
16. **Repository containment is mandatory.** Orchestrator-owned source/build/test/fixture/script/doc material lives under `orchestrator/`; Protocol workplans remain under `workplans/`; repository CI contains only thin invocation wiring.

### 2.2 Frozen high-level architecture (Tier 1B)

The parent Architecture 1.6.0 remains fully Frozen. WP-1 additionally fixes these task-local consequences:

- one Python 3.11+ `sdp-orchestrator-core` distribution, one `sdp` entry point, native PEP 420 `sdp_orchestrator.core`, and no root namespace `__init__.py`;
- strict lower-to-higher dependency direction; Core has no Tracker/Adapter/Scheduler dependency or placeholder state;
- one TOML normalization path and no semantic environment-variable override surface unless explicitly accepted;
- one non-mutating Git/worktree/remote observer and one stage-specific workplan resolver;
- one compatible Protocol 5.16 profile/source owner and one canonical body extraction/generation path;
- public `CoreAPI`, `ApplicationAPI`, `ExtensionProvider`/`ExtensionContext`, JSON-compatible records, stable value identities, and no private implementation types in public signatures;
- route-independent `PreparedPrompt` plus route-sensitive final `RenderedPrompt`;
- one extension registry/entry-point group with metadata-only discovery and failure-atomic normal activation;
- one exact terminal result-footer/fingerprint wire contract;
- no persistence, workflow reducer, agent runner, benchmark/resource/scheduler machinery in Core.

Everything below those boundaries is Tier 2 and may be altered, reduced, consolidated, or replaced when the same contract is satisfied more simply.

## 3. Frozen WP-1 behavioral contract

### 3.1 Configuration, project selection, and prompt mode

Core uses one bounded TOML parser/validator. Core prompt-mode precedence is explicit CLI/API -> project default -> core default -> built-in `web`. `PromptExecutionMode(local|web)` is distinct from canonical prompt `EXECUTION_MODE` (`AUTO_EXECUTE`, `REPORT_ONLY`, etc.). Core never silently falls from web to local.

CLI project convenience when `--project` is absent is: unique configured project containing cwd -> configured default -> sole project -> structured ambiguous/not-found. Public Core requests use explicit `ProjectKey`.

Core-owned config is closed; extension namespaces are bounded opaque data interpreted only by their activated extension. Credential-bearing URLs are rejected/redacted. Unrelated extension config does not enter Core preparation/prompt identity.

### 3.2 Git/worktree/remote observation

`ObservationPolicy` supports `local_only`, `use_cached_remote`, and `refresh_remote`, with programmatic default `local_only`. Cached mode performs no network; refresh performs a bounded noninteractive read-only query.

`CandidateRef` identifies repository/worktree, branch/detached state, HEAD, materially relevant staged/index + unstaged + untracked state, selected remote/target evidence, provenance/freshness, and identity completeness. `sdp.git-working-tree.v1` includes staged blob/mode identity and worktree/untracked content under finite per-file/count/aggregate bounds. Unsupported/unreadable/embedded state gives incomplete identity rather than false completeness. Non-UTF-8 Git paths must not crash identity construction.

Remote selection is configured remote -> branch upstream remote -> origin -> sole remote -> ambiguous/unavailable. Evidence is always bound to the selected remote/target. Filesystem/file remotes are local-only. Web rendering requires known target existence, blocks dirty state and known local/remote divergence, and preserves `core.remote.ambiguous` when ambiguity is the cause.

`max_remote_staleness_seconds` is behavioral policy. Unknown-age cached evidence cannot satisfy an explicit maximum; a successful refresh may establish an observation timestamp. Core never invents age from convenient ref/file mtimes or silently refreshes cached mode.

Git subprocesses are bounded during collection, non-mutating, noninteractive, and use an intentionally constructed environment rather than arbitrary ambient Git semantic overrides.

### 3.3 Workplan catalog, lifecycle, and Protocol binding

Core catalogs bounded regular workplan text under `workplans/active/` and `workplans/archive/`; symlink aliases/special files/path escapes are ignored/rejected safely. Frontmatter is bounded before/during data-only YAML materialization; aliases/anchors or unsupported complex forms may be rejected rather than materialized unboundedly.

Explicit selector is an exact `workplan_id` or exact canonical repository-relative POSIX path under a recognized workplan root. Traversal/absolute/dot/backslash aliases do not normalize into matches. Current-authority deduplication uses explicit supersession evidence only; ambiguity remains ambiguity.

Lifecycle directory and declared status must agree for current governance. Implementation/Review/Alignment require a current active semantically identified governing workplan; Closeout may bind the completed-plan case authorized by the stage policy.

Stage workplan policy remains:

| Stage | Policy |
| --- | --- |
| baseline | optional explicit only |
| design | optional explicit only; no implicit active capture |
| implementation | governing workplan required |
| review | governing workplan required |
| verification | optional explicit governing authority |
| stabilization | optional explicit governing authority |
| alignment | exact downstream workplan required |
| health-audit | workplan disallowed |
| closeout | optional exact completed binding; otherwise `COMPLETED_WORK` |

A governing selected workplan with a declared Protocol version takes precedence over project defaults. Required stages fail on missing/invalid/unsupported governing version. An explicitly selected optional authority whose Protocol metadata is absent may remain evidence-only where the stage does not require it to determine the governing contract; a version that is actually declared is never silently ignored.

### 3.4 Protocol source/profile/workflow authority

V1 supports the explicitly compatible Protocol 5.16 profile. Source precedence is configured compatible local source -> exact packaged derivative -> explicitly permitted bounded remote source at an explicit ref -> truthful incompatible/unavailable failure.

A remote source resolves one requested ref to one immutable identity before multi-file use, reads only bounded required data, revalidates the ref, never executes repository/downloaded code, and records requested/resolved provenance/content digests. Local multi-file reads are optimistic/coherent or fail as changed. Packaged profile and prompt resources must reproduce exactly from canonical Protocol source and `source/PROTOCOL_VERSION`.

Canonical extraction requires the exact numbered stage-heading set and exactly one fenced text body per stage; extras/duplicates/conflicts are source-incoherent. The machine profile carries bounded control metadata only, no duplicated prompt prose or generic workflow DSL.

Workflow routing is conservative: relations that are optional/context-dependent in Protocol 5.16 remain multiple alternatives/ambiguous; the profile never invents a deterministic edge from an outcome that is insufficient to choose one stage.

### 3.5 Input ownership

Every canonical INPUT is `mechanical`, `canonical_default`, or `required_user`. Mechanical/first-class bindings cannot be overridden by generic input. Canonical `PROTOCOL_REF` follows the governing Protocol contract; `PROTOCOL_SOURCE` defaults to `AUTO_LOCAL_FIRST`; canonical `EXECUTION_MODE` is independent of local/web prompt mode.

Required user inputs remain: Baseline `BASELINE_SCOPE`; Design `--task`; Verification `VERIFICATION_SCOPE`; Stabilization `STABILIZATION_SCOPE`; Alignment `UPSTREAM_ACCEPTED_WORK` plus exact plan; Health Audit `AUDIT_SCOPE`; Closeout `COMPLETED_WORK` unless selected completed plan supplies it. Generic overrides accept declared overridable inputs only.

Concrete inserted values use the single reversible structure-safe scalar encoding. NUL/CR/LF/control data cannot inject additional prompt grammar; arbitrary user content remains reversible data.

### 3.6 Two-phase preparation/render identity

`PreparedPrompt` contains RunId, ProjectKey/WorktreeKey observation, resolved StageRef, candidate, WorkplanResolution, complete WorkflowProfileDescriptor/ProtocolProfileRef, PromptSourceRef, resolved mode-independent inputs/provenance, result-schema identity, and `sdp.prompt-preparation.v1`.

The preparation fingerprint binds the complete material public admission surface, including complete `DigestRef` identity (algorithm + canonicalization scheme + value), complete workflow/profile facts, candidate/workplan/source identity, selection basis/policy, and mode-independent inputs. It excludes only genuinely volatile/non-semantic diagnostics/timestamps and unrelated extension config.

At render entry Core recomputes the preparation fingerprint and rejects tampering. Final render uses revalidated current repository/worktree/selected-remote/workplan-resolution/source state rather than caller-supplied locations. Packaged/local/remote source provenance is compared with the prepared source; mutable local source is stability-checked again. A final optimistic unchanged-state check occurs before event publication/return.

### 3.7 Prompt artifact, result footer, events, and public values

Canonical body is preserved except declared INPUT substitutions. Fingerprint substitution changes only Core-owned fingerprint slots; user/canonical occurrences of the placeholder literal remain data. Caller RunId is serialized safely and remains one coherent value.

Every prompt requests ordinary prose followed by **exactly one** exact-line terminal JSON footer for `StageResultEnvelope v1`. Prose may precede, but no non-whitespace follows the end marker. Duplicate exact footer blocks/marker pairs are invalid. Additive result fields are permitted only as JSON-compatible value data. Core requests the footer but does not persist/interpret result semantics in WP-1.

All public records remain JSON-compatible immutable value data. Open event/result payload fields accept JSON-compatible nested values, not live implementation objects. Public timestamps are UTC ISO-8601. `Problem` is one structured error record with `code`, redacted `message/details`, `retryable: bool | None`, and no exception subclass hierarchy.

Only a successful final render emits `core.prompt.rendered.v1`, only to explicitly subscribed sinks. EventId is stable for event type + RunId + prompt fingerprint. Sink failure is redacted/diagnosed but cannot counterfeit the primary result.

### 3.8 Extension composition and passive diagnostics

Core discovers extensions only through `sdp_orchestrator.extensions.v1`. Discovery-only reads installed distribution/entry-point metadata without importing provider code and does not claim unobserved capability/health. Metadata failure is diagnosed truthfully rather than silently represented as no extensions.

Normal activation uses the public manifest/SPI, canonical extension ID, API/multiplicity requirements, hard `requires_extensions`, and actual capability satisfaction from Core/already-active compatible providers. Activation registrations/subscriptions are staged and committed atomically only after successful `ExtensionRegistration` validation. A provider returning the wrong SPI result is not promoted to active. Failed/incompatible providers disable only themselves and truly dependent providers; healthy Core/alternative providers remain available. Core-owned singular services cannot be replaced silently; multi-provider order is deterministic where multiplicity permits it.

`doctor` and default `capabilities` remain passive: no provider import, target-repository mutation, or hidden network. Doctor's `packaged_profile` observation is packaged-only and cannot fall through configured local/remote source precedence.

### 3.9 Bounded trust/resource boundary

Core-controlled config/workplan/source/archive/subprocess/network readers enforce finite byte/count/nesting/time/output/aggregate limits before unbounded materialization. Remote/downloaded material remains data; repository build hooks/files are not executed merely to inspect state. User-facing external diagnostics are redacted.

Subprocess environments follow least privilege. Ambient variables that redirect Git repository/config/object semantics or specify executable transport commands are not inherited merely because they exist. Established non-secret process/credential environment may be preserved only where it is actually needed by the supported transport contract.

## 4. Public API/SPI floor

The v1 consumer surface remains the Architecture 1.6.0 `CoreAPI`/`ApplicationAPI` family with `allocate_run_id`, project/observation/workplan/workflow/list-stages, `prepare`, and `render`. Public requests/responses are versioned JSON-compatible records; no Git/subprocess/file/DB/lock/event-loop/private Core implementation types appear in public signatures.

The provider surface remains one `ExtensionProvider.manifest() -> ExtensionManifest` and `activate(context) -> ExtensionRegistration` SPI. `ExtensionContext` exposes public Core API, the extension's own bounded config namespace, and staged service/event registrars only.

Core provisions exactly the WP-1 lower capabilities: `prompt.render`, `project.observe`, `workplan.catalog`, `workflow.profile`. Semantic capability keys are unversioned; API compatibility is separate.

## 5. Acceptance obligations and real owners

O1. **Distribution/layout:** wheel + sdist build, independent metadata/resource inspection, clean install outside checkout, installed `sdp` smoke, PEP 420 sibling coexistence, no root namespace init/higher imports, repository containment fitness.

O2. **Config/projects:** precedence/default/ambiguity, bounded malformed/oversized config, empty semantic env override surface, absent extension namespace preservation, secret URL rejection/redaction, local/remote source policy.

O3. **Git/remote:** real temporary Git/worktree/remotes; staged/index/worktree/untracked identity, modes/non-UTF8/bounds, alias vs linked worktree, remote selection/evidence/freshness, no mutation, bounded subprocess/environment behavior.

O4. **Workplans:** top-level/nested/archive, exact path/ID, branch binding, supersession ambiguity, lifecycle, bounded parser, symlink/path escape, every stage policy and Protocol-binding case.

O5. **Protocol/profile/workflow:** exact canonical extraction, package/generator parity, local/packaged/remote source coherence, immutable remote identity, unsupported version rejection, conservative/ambiguous routing.

O6. **Public prepare/render seam:** public API completeness, StageSelector -> profile-bound StageRef, governing-workplan precedence, adapter-shaped external admission between phases, full preparation identity, JSON roundtrip tamper rejection, optimistic stale checks, no private objects.

O7. **Inputs:** all stages/inputs, required-user completeness, prompt-mode vs canonical execution mode, governing Protocol ref, structure-safe reversible scalar encoding, atomic invalid-input failures.

O8. **Renderer/wire/events:** canonical body fidelity, deterministic preparation/prompt fingerprints, exactly-one terminal footer extraction, opaque RunId/placeholder collisions, JSON-compatible additive fields, explicit subscription/EventId/failure behavior.

O9. **Privacy/web truth:** final RenderedPrompt/stdout tests for paths/credentials/ambient environment/local remotes/dirty/divergent/stale/absent/ambiguous remote cases.

O10. **Extensions/diagnostics:** real installed entry-point metadata; passive discovery/no import; compatible/incompatible/missing/cyclic/alternative-provider graphs; staged activation; canonical ID/API/multiplicity/SPI; explicit event subscription; doctor/capabilities no hidden network/mutation.

O11. **CLI product boundary:** installed `sdp` subprocess, every stage alias and generic prompt path, stdout atomic/prompt-only, redacted stderr/nonzero failures, additive clipboard, passive doctor.

O12. **Final repository acceptance:** complete affected Core regression, Hypothesis where installed, canonical generator check, ordinary Protocol unit/build/validate/package-parity checks, `git diff --check`, and final simplicity/absence of higher-module or duplicate-authority machinery.

Acceptance must execute the real semantic owner. Evidence that could remain green while the final owner is broken does not close the claim.

## 6. Implementation evidence reviewed

The independent Review evaluated implementation candidate `121ca48454e222740db9606e3a4a2f22719ef5e9`, directly based on review-contract commit `fc466570e7a9a3b6d2fab99a1440fe72a0a46064`.

Implementation recorded the following exact-candidate evidence before Review:

- focused affected regression: 312 tests / 10 modules / 10 workers;
- complete Core acceptance: 339 tests / all 11 modules / 11 workers, including wheel+sdist build/install/installed CLI, real Git/remotes, extensions, privacy/wire/API;
- Hypothesis active with 400 + 200 generated scalar examples;
- canonical snapshot generator `--check` and incompatible-version counterexample;
- ordinary repository acceptance: 172 tests plus skill build/validate/check-dist and `git diff --check`;
- focused local Semgrep checks and Serena owner/reference inspection.

This is strong evidence and most previously identified defects are genuinely closed. It is not a substitute for the independent counterexamples below, and there were no GitHub commit-status contexts to add independent CI evidence at Review time.

## 7. Independent implementation Review — 2026-09-08

**Verdict: NO-PASS. WP-1 remains reopened.**

The parent Architecture 1.6.0 is not reopened. Every finding below is implementation nonconformance or oracle/documentation drift under the already-binding contract. Repair existing owners in place; do not add parallel registries/resolvers/renderers/workflow engines/wrappers/persistence/higher-module dependencies.

### F1 — Workflow profile still over-resolves blocker outcomes

`_TRANSITIONS` still collapses context-dependent outcomes to one next stage, including `implementation/blocked -> design`, `review/no_pass -> implementation`, `alignment/no_pass -> alignment`, and `closeout/blocked -> implementation`. Protocol 5.16 routes by the actual blocker/authority class; outcome alone is insufficient. This violates Architecture invariant 25 and O5.

**Repair:** alter the existing profile transition metadata so each outcome exposes all authority-backed alternatives when it cannot determine one stage. Preserve ambiguity; do not add a routing DSL/engine.

**Required tests:** every context-dependent blocker/no-pass trigger above is non-deterministic where Protocol permits Design/Implementation/stay-stage alternatives; truly deterministic outcomes remain deterministic; regenerated package parity passes.

### F2 — Capability dependency ordering can manufacture a cycle despite a healthy provider

The current topological graph makes a capability consumer depend on *all* compatible providers. Counterexample: `B` independently provides `cap.shared`; `A` also provides it but requires extension `D`; `D` requires `cap.shared`. A valid order is `B -> D -> A`, but the current graph makes `D` depend on both A and B and reports a cycle, disabling the manifest set. This violates R5/O10 graceful degradation and actual-satisfaction semantics.

The same composition owner still masks two SPI/discovery failures: entry-point metadata enumeration failure becomes an indistinguishable empty installation, and `activate()` returning `None` is silently converted to a successful empty registration despite the public SPI return contract.

**Repair:** keep hard extension-ID dependencies as graph edges, but make capability readiness depend on Core or any compatible provider that is actually active; one iterative activation/readiness owner is preferable to an over-constrained provider graph. Report metadata discovery failure truthfully. Reject non-`ExtensionRegistration` activation results. Keep the existing one registry and staged failure-atomic commit path.

**Required tests:** B/A/D activates; true unsatisfiable cycle stays disabled; metadata discovery failure is not “zero extensions”; `activate(None)` is not active; unrelated Core/healthy providers remain available.

### F3 — Preparation identity drops `DigestRef` algorithm/scheme

Preparation/revalidation helpers reduce candidate/workplan/profile/source digests to `.value`, omitting `DigestRef.algorithm` and `canonicalization_scheme`. Those fields are part of the public identity and visible to external admission, so a JSON-roundtrip caller can alter only the algorithm/scheme while retaining the old preparation fingerprint/comparison result.

**Repair:** use the existing preparation identity owner to serialize the complete digest record (`algorithm`, `canonicalization_scheme`, `value`) everywhere a material DigestRef participates. Do not add a second digest/preparation schema.

**Required tests:** altering only algorithm or scheme on working-tree, selected workplan artifact/semantic, profile-source, or prompt-source content digests invalidates the old preparation; unchanged exact records remain deterministic.

### F4 — `doctor` is not guaranteed packaged-only/no-network

`doctor_command()` labels its result `packaged_profile` and promises no network, but calls normal `workflow()` resolution. A configured `local_root` can therefore supply the reported profile, and if the packaged snapshot is unavailable/incoherent while remote fallback is enabled, the normal source path may query the network. Current tests do not install a network trap on this failure/fallback path.

**Repair:** make doctor inspect the packaged snapshot directly or use an existing explicitly network-disabled packaged-source path. Do not create another general Protocol resolver.

**Required tests:** configured local/remote sources cannot change doctor’s packaged-profile observation; forced packaged failure with remote allowed reports a packaged problem and performs zero remote calls; provider import/repository mutation remain absent.

### F5 — Footer extractor and test oracle accept duplicate complete footers

The Frozen wire says exactly one terminal uniquely marked footer. `extract_result_footer()` instead selects the last complete block, and `test_extraction_takes_the_last_marked_block` positively asserts this invalid behavior. The user guide likewise says “exactly one” but documents a last-marker extraction rule.

**Repair:** alter the existing extractor to reject duplicate exact begin/end marker blocks while preserving exact-line matching, terminal whitespace-only semantics, and the valid single-footer path. Replace the weakened test and reconcile the guide. No general parser is needed.

**Required tests:** one terminal footer extracts; two complete footers reject; extra exact begin/end markers reject; indented/near-match/trailing-prose cases remain rejected.

### F6 — Explicit optional workplan can have its declared Protocol version ignored

`prepare()` only treats the selected workplan as governing profile input for `REQUIRED`/`EXPLICIT_REQUIRED` policies. In `EXPLICIT_ONLY` stages, a selected plan with a declared `protocol_version` is therefore silently rendered using project/default profile. The accepted evidence-only exception applies to optional authorities with **incomplete** Protocol metadata; it does not authorize ignoring a version that is present.

**Repair:** in the one existing prepare/profile-binding path, reconcile/bind a declared Protocol version on any explicitly selected governing authority. Preserve the evidence-only fallback when optional selected metadata is absent.

**Required tests:** explicitly selected incompatible-version plans for Verification/Stabilization/other explicit-only stages fail rather than silently 5.16; compatible declared version agrees; optional selected plan with no version retains the accepted evidence-only behavior.

### F7 — Open public record fields can carry non-JSON/live values; timestamp contract is unenforced

The public v1 floor promises JSON-compatible immutable values and UTC ISO-8601 timestamps, but `EventEnvelope.payload: dict[str, Any]` and additive `StageResultEnvelope` fields can accept arbitrary live Python objects and only fail later at JSON serialization. Public timestamp fields also accept arbitrary strings.

**Repair:** add the smallest validation at the existing public-record boundary: recursively accept JSON-compatible scalar/list/map values in open payload/additive fields and reject live/non-JSON objects; validate declared public timestamps as UTC ISO-8601. Do not create a parallel schema/type system.

**Required tests:** nested JSON payload/extra fields round-trip; `object()`, file handles, and similar live values reject at construction; produced/deserialized public timestamps satisfy UTC ISO-8601; additive JSON compatibility remains.

### F8 — Ambient executable Git transport overrides remain inherited

The repaired Git environment removes repository/config/object redirection but still allowlists ambient `GIT_SSH`, `GIT_SSH_COMMAND`, and `GIT_SSH_VARIANT`. `GIT_SSH_COMMAND` is executable process configuration: a remote refresh/source query can execute an arbitrary ambient command that Core never configured. That conflicts with the no-semantic-environment-override and least-privilege trust boundary. Normal SSH can use standard client/config and agent state without inheriting an arbitrary command string.

**Repair:** narrow the existing `_git_env()` allowlist. Preserve only process/credential environment actually needed by the accepted normal transport contract; do not inherit executable Git command overrides without an explicit accepted configuration surface. Do not add a transport framework.

**Required test:** ambient `GIT_SSH_COMMAND`/equivalent helper that would create a marker is not executed by the relevant remote-query path; normal supported SSH-agent/environment-independent observation remains available.

## 8. Re-review gate

WP-1 may return to independent Review only after F1-F8 are repaired in the existing owners and the assembled exact candidate re-establishes affected acceptance. The strong prior evidence remains reusable only for dimensions these edits cannot plausibly affect.

The next exact candidate must record:

1. focused counterexamples for F1-F8;
2. complete Core regression with Hypothesis active;
3. real installed extension composition and passive-doctor tests;
4. preparation/public API-SPI/wire/privacy tests;
5. real Git/remote non-mutation and environment-boundary tests;
6. canonical profile/snapshot generator parity;
7. wheel and sdist build/inspection/install/installed CLI outside checkout;
8. ordinary repository Protocol tests/build/package parity and `git diff --check`.

Any required unavailable owner check remains a blocker unless the governing contract explicitly permits substitute evidence. A green test whose oracle encodes the wrong contract does not count as closure.

**Current verdict: NO-PASS — return to `software-implementation`, repair F1-F8 without adding parallel machinery, then submit one exact assembled candidate for fresh independent Review.**
