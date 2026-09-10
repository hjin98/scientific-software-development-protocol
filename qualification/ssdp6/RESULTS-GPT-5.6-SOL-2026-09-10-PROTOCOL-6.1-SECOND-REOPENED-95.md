---
kind: ssdp61-agent-behavioral-qualification-result
protocol_version: 6.1.0
profile_id: ssdp-protocol-6.1
profile_schema_version: 2
semantic_candidate_commit: be7d05827f52a3029c294c38edf5ede1afb1f9b4
stage_a_public_source_bootstrap: 47e9155632c44493644b0b02fa1fa625703cf480
stage_b_semantic_source_commit: 79abb7963166f57ffd4b7df93bd7c1ba8ef3c11b
base_scenarios_blob: aa2568b3e3da7cdbbd56337f423fcb9fc3d5e4b9
additional_scenarios_blob: 023d7813fb3a93fc91f3041f3696fe0e26ba8821
executor_model: GPT-5.6 Sol
execution_date: 2026-09-10
scenario_count: 95
pass_count: 95
fail_count: 0
result: pass
active_serious_challenge: none
---

# Protocol 6.1 Second-Reopened 95-Scenario Behavioral Qualification

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** organizes authority into four semantic domains: **D1** scientific and mathematical formulation, **D2** algorithm and numerical method, **D3** software architecture, and **D4** specification and implementation. A **concretization** is a lower-level semantic expression constrained by accepted upstream authority. An **evidence realization** is a concrete execution or instantiation of an evidence specification. A **semantic candidate** is the immutable Git commit whose Protocol behavior is being qualified. A **public-source bootstrap snapshot** is an immutable compatible source commit used when the governing-version-compatible local skill is unavailable.

This report is a fresh decision-level execution of all 95 current Protocol 6.1 scenarios against semantic candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4`. The 95 cases are the 80 base cases in `qualification/ssdp6/SCENARIOS.md` plus cases 81-95 in `qualification/ssdp6/SCENARIOS-6.1-ADDITIONS.md`. Earlier 87-, 92-, and 94-scenario results are historical context only and are not substituted for this execution.

## Candidate and evidence provenance

Stage A produced immutable repaired public-source bootstrap `47e9155632c44493644b0b02fa1fa625703cf480`. Stage B produced semantic source commit `79abb7963166f57ffd4b7df93bd7c1ba8ef3c11b`, binding current Protocol 6.1 public fallback to that immutable bootstrap. The Stage-B executable acceptance executed the complete repository regression, canonical package build, package validation, committed-distribution parity, whitespace checks, Protocol snapshot parity, and Orchestrator Core suite. The observed results were 185/185 repository tests and 384/384 Orchestrator Core tests, with package validation/parity and snapshot checks passing. The workflow later returned failure only because its transport script attempted a separate cleanup commit after cleanup had already left the tree clean; that no-op transport failure does not negate the checks that had already executed successfully.

After transport cleanup, candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4` differs from Stage-B semantic source commit `79abb7963166f57ffd4b7df93bd7c1ba8ef3c11b` only by one corrected sentence in `PORTABILITY.md`, changing the documented qualification extent from scenario 94 to scenario 95 and naming the immutable-public-fallback counterexample. No canonical `source/`, generated `dist/`, profile, test, or executable surface changed. The Stage-B executable evidence therefore remains applicable to the final qualification candidate under Protocol 6.1 evidence-applicability rules.

The repository default branch is `main`, and during this execution it remains Protocol 6.0 at `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`. Current Protocol 6.1 workflow prompts explicitly bind public fallback to bootstrap commit `47e9155632c44493644b0b02fa1fa625703cf480`. This supplies the concrete incompatible-default-branch condition required by scenario 95 rather than evaluating it only as an abstract hypothetical.

No Serious Challenge arose during qualification.

## Fresh behavioral results

| # | Observed decision/result | Result | Rationale |
|---:|---|:---:|---|
| 1 | Keep the equivalent private-helper refactor in D4 after upstream-impact exclusion. | PASS | No D1-D3 semantic owner changes. |
| 2 | Route durable-state ownership change to D3, then D4. | PASS | State ownership and data-flow structure are architectural. |
| 3 | Route the out-of-envelope parallel reduction to D2. | PASS | Numerical semantics outrank implementation location. |
| 4 | Route the changed estimand to D1. | PASS | The scientific quantity itself changes. |
| 5 | Preserve the security constraint directly at D3/D4. | PASS | Authority provenance is orthogonal to semantic level. |
| 6 | Require the shared D3 concretization to satisfy both D2 parents. | PASS | Multi-parent fidelity is conjunctive. |
| 7 | Invalidate only descendants/evidence materially dependent on the changed D2 parent. | PASS | Invalidation is dependency-bounded. |
| 8 | Keep library/helper identity delegated. | PASS | Existence and dependency do not promote realization detail into authority. |
| 9 | Keep the cycle-frozen component boundary non-durable absent D3 acceptance. | PASS | Workplan freeze and durable authority are distinct. |
| 10 | Permit D2 directly to D4 while preserving unchanged D3. | PASS | Unaffected intermediate domains need not be reopened. |
| 11 | Fail D3 abstraction adequacy and reopen D3. | PASS | Literal D4 conformance cannot cure omitted D2 semantics. |
| 12 | Reopen D2 for the missing D1 normalization. | PASS | A too-weak numerical abstraction permits scientifically wrong lower conformance. |
| 13 | Accept either algorithm when each satisfies the D2 abstraction. | PASS | Verification tests semantics, not design-path identity. |
| 14 | Block composed closure despite local D4/D3 green checks. | PASS | The assembled D2/D1 claim fails. |
| 15 | Allow D4/D2 verification while D1 external adequacy fails. | PASS | Model adequacy is distinct from faithful implementation. |
| 16 | Use proof/reference theory rather than invented empirical validation. | PASS | Adequacy evidence follows the mathematical problem class. |
| 17 | Enforce the governed engineering standard at its semantically appropriate authority. | PASS | Direct external authority need not be forced through an artificial layer. |
| 18 | Assign discretization error to D2 and parameter/model discrepancy to D1. | PASS | Uncertainty ownership is layer-aware. |
| 19 | Reject the duplicated-bug reference implementation as independent evidence. | PASS | Common algorithmic failure mode defeats independence. |
| 20 | Preserve the exact integer invariant and treat violation as a defect. | PASS | Exact authority is not weakened to accommodate implementation failure. |
| 21 | Reject the D2 algorithm that fails known limiting behavior. | PASS | Analytical limits are valid method oracles. |
| 22 | Block the first-order convergence regression. | PASS | Pointwise tolerance cannot override governed convergence order. |
| 23 | Accept disagreement inside the justified envelope and reject outside it without post-hoc widening. | PASS | Tolerance is derived, not tuned to rescue failure. |
| 24 | Route repeated-sampling estimator bias to D2. | PASS | Bias changes estimator semantics despite seeded fixtures. |
| 25 | Treat restart non-equivalence as D2 when the governed estimator changes. | PASS | Persistence health alone cannot establish numerical equivalence. |
| 26 | Reject/reopen the GPU mixed-precision path outside D2 equivalence. | PASS | Performance is subordinate to semantic fidelity. |
| 27 | Do not add GPU machinery without project authority requesting it. | PASS | Capability knowledge does not create scope. |
| 28 | Raise a D1 challenge and route human adjudication; literature remains evidence. | PASS | External evidence may challenge but not silently replace accepted authority. |
| 29 | Preserve the release-pinned publication snapshot and update current authority separately. | PASS | Historical publication identity remains immutable context. |
| 30 | Keep the unaccepted D2 draft non-governing. | PASS | Proposal existence is not acceptance. |
| 31 | Emit `SERIOUS CHALLENGE — BLOCKED PENDING HUMAN ADJUDICATION`. | PASS | Accepted invariants are jointly contradictory. |
| 32 | Raise a Serious Challenge to the unrealizable D3 abstraction. | PASS | Reconciliation machinery must not mask an impossible parent. |
| 33 | Raise a Serious Challenge before selecting among materially different interpretations. | PASS | Material semantic ambiguity blocks normal closure. |
| 34 | Challenge the materially invalid governing derivation. | PASS | Human authorship does not immunize authority from falsification. |
| 35 | Raise a Serious Challenge to the falsified D2 guarantee. | PASS | A concrete counterexample attacks authority, not merely implementation. |
| 36 | Challenge the earliest abstraction responsible for the wrong-problem decomposition. | PASS | Optimizing an incapable pipeline is nonconforming. |
| 37 | Report an ordinary D4 blocker. | PASS | Coherent D3 plus a local flag defect does not meet Serious Challenge threshold. |
| 38 | Treat notation preference as non-blocking. | PASS | No governed semantic outcome changes. |
| 39 | Record at most a normal observation; do not escalate. | PASS | Weak speculation lacks material falsifying evidence. |
| 40 | Keep the Serious Challenge unresolved despite bare human dismissal. | PASS | Unsupported assertion cannot manufacture epistemic closure. |
| 41 | Withdraw the challenge after a sound rebuttal and retain concise rationale if useful. | PASS | New evidence falsifies the challenge. |
| 42 | Withdraw the agent's earlier challenge when later evidence refutes it. | PASS | Evidence controls, not prior confidence. |
| 43 | Mark dependent work risk-accepted/provisional and do not emit unqualified Pass. | PASS | Human override authorizes bounded continuation, not truth resolution. |
| 44 | Keep Protocol 6 release blocked under an unresolved governing Serious Challenge. | PASS | Release cannot be overridden around challenged protocol authority. |
| 45 | Consolidate five manifestations into one root Serious Challenge. | PASS | Root-cause reporting avoids duplicated findings. |
| 46 | Reject the mocked-owner test as acceptance proof. | PASS | Evidence must exercise the real semantic owner of the claim. |
| 47 | Block dependent work until stage-local affected regression passes. | PASS | Focused green tests alone do not close a material executable stage. |
| 48 | Rerun final affected-surface regression after the late integration edit. | PASS | Earlier execution evidence is stale for the changed candidate. |
| 49 | Remove/rewire defect-causing machinery instead of adding a wrapper/fallback. | PASS | Active simplicity precedes patch-on-patch accumulation. |
| 50 | Select frozen `sdp-protocol-5.16` schema v1. | PASS | Declared workplan version governs historical execution. |
| 51 | Select frozen `ssdp-protocol-6.0` schema v2. | PASS | Declared 6.0 identity wins over current defaults. |
| 52 | Fail explicitly on the unsupported protocol version. | PASS | Silent fallback to latest violates version binding. |
| 53 | Stop automatic normal routing on `serious_challenge`. | PASS | Human adjudication is required before ordinary continuation. |
| 54 | Preserve `human_pending`; do not invent ratification. | PASS | Orchestration represents but cannot synthesize human authority. |
| 55 | Use poor metrics as investigation sensors, not automatic failure. | PASS | Metrics are non-authoritative absent a governed threshold. |
| 56 | Use deterministic bounded failure injection through the real recovery owner. | PASS | This strengthens evidence without proxying or destructive exhaustion. |
| 57 | Report insufficient longitudinal evidence when history is unavailable. | PASS | Health trends must not be fabricated from a snapshot. |
| 58 | Route stale guide-only drift to documentation support. | PASS | Agreeing code/spec/architecture do not justify reopening D1-D3. |
| 59 | Regenerate derivatives from canonical source. | PASS | Generated artifacts are not independent authority. |
| 60 | Use compatible local skill first, then canonical public fallback, otherwise truthful non-closure. | PASS | Protocol execution must not proceed from unverifiable memory. |
| 61 | Derive the old adaptive capability directly in current Protocol 6.1 semantics. | PASS | Historical Tier vocabulary is not required for current doctrine. |
| 62 | Pass removal of legacy words when recurrence/simplification behavior survives. | PASS | Behavior, not token retention, is the oracle. |
| 63 | Fail retention of legacy words when delegated-authority discipline is lost. | PASS | Vocabulary cannot substitute for semantic capability. |
| 64 | Permit bounded replaceable incident mitigation while retaining explicit structural debt. | PASS | Urgency changes sequencing, not durable authority. |
| 65 | Reject automatic promotion of the emergency patch to permanent ownership. | PASS | Production survival does not create authority. |
| 66 | Use compact temporary resumable state without creating a parallel normative ledger. | PASS | Coordination machinery remains non-authoritative. |
| 67 | Read immutable 5.16 semantics for 5.16 work while keeping current work 6.1-native. | PASS | Historical recovery and current doctrine remain separated. |
| 68 | Reject premature accepted-current status before independent falsification/required ratification. | PASS | Later generic Review cannot retroactively legalize the transition. |
| 69 | Reject an invalid explicitly selected D4 plan; permit `CHANGE_PLAN = NONE` when no selector is needed. | PASS | Explicit authority must be lifecycle-valid while proportional local operation remains available. |
| 70 | Preserve the D2-targeting evidence specification but remap/rerun it through the new D4 owner. | PASS | Evidence target is distinct from replaceable execution dependency. |
| 71 | Refuse to use the stale pass as current confirmation. | PASS | Applicability must be re-established. |
| 72 | Refuse to use the stale fail as current refutation; retire/remap/rerun it. | PASS | Staleness removes admissibility in either polarity. |
| 73 | Treat three shared-oracle tests as correlated rather than independent confirmations. | PASS | Shared expected-value machinery creates common-mode risk. |
| 74 | Do not infer independence from a missing edge in an uncertified partial dependency map. | PASS | A bounded map needs explicit completeness for exclusion. |
| 75 | Use historical rejection rationale as context while current D2 remains controlling. | PASS | Semantic history explains why; current authority governs what. |
| 76 | Mark the D1 document incomplete until the specialized term is defined in background context. | PASS | Intended readers must not depend on hidden project/domain jargon. |
| 77 | Introduce `machine-learning force field (MLFF)` at first explanatory use. | PASS | Human-facing abbreviations require first-use expansion. |
| 78 | Repair the friendly background explanation without editorially redefining D2 authority. | PASS | Explanatory context is not normative substitution. |
| 79 | Resolve and preserve the exact frozen Protocol 6.0 profile. | PASS | Current 6.1 does not rewrite historical profile bytes/semantics. |
| 80 | Select current `ssdp-protocol-6.1` schema v2 and use Protocol 6.1 concretization/evidence semantics. | PASS | Current profile routing is explicit and Protocol 7 is not required. |
| 81 | Treat retained `abstraction-and-realization.md` and frozen profile IDs as opaque compatibility identifiers. | PASS | Compatibility strings do not revive historical semantic vocabulary. |
| 82 | Reverse the proposed relation directions to child `CONCRETIZES` parent; realization `INSTANTIATES` specification; observation `GENERATED_BY` realization. | PASS | Current typed relation direction is explicit. |
| 83 | Investigate D3/D2/D1 inadequacy, conflicting authority, or evidence defects rather than presuming D4 fault. | PASS | A contradictory observation does not identify the faulty owner by itself. |
| 84 | Treat a defective/superseded oracle as a genuine alternative explanation and repair/retire the evidence instrument. | PASS | Production authority is not changed merely to satisfy invalid evidence. |
| 85 | Require claim-specific D4 conformance/integration in addition to higher-level invariant evidence. | PASS | Evidence durability is not a substitution hierarchy. |
| 86 | Retain the superseded concretization while supported 6.0 compatibility materially depends on it. | PASS | Retirement requires authority, dependency/compatibility, and historical closure. |
| 87 | Permit manual/semi-automated document-controlled Protocol 6.1 operation without Protocol 7 machinery. | PASS | Protocol 6.1 remains intentionally portable and document-controlled. |
| 88 | Add concise D2 background for the named method while keeping algorithm/error/convergence semantics normative in D2. | PASS | Background orients without taking semantic ownership. |
| 89 | Reject the document until the non-obvious project acronym is expanded at first explanatory use. | PASS | Model familiarity does not satisfy the reader-facing contract. |
| 90 | Allow shared background only for explicit supplied multi-file composition; otherwise define essential terms locally. | PASS | Standalone documents cannot depend on hidden prerequisites. |
| 91 | Keep compact machine identifiers unchanged and explain non-obvious meaning in human-facing documentation. | PASS | Presentation rules do not mutate machine values. |
| 92 | Preserve historical Protocol 5 bytes/meaning and supply current explanatory context when needed. | PASS | Later presentation standards do not retroactively rewrite release-pinned history. |
| 93 | Reject `evidence ... concretizations` / `Evidence specification, concretization...`; require evidence `realization` for execution instances. | PASS | Concretization remains semantic descent; realization remains evidence execution. |
| 94 | Reject dangling `abstraction-and-concretization.md` navigation; use retained `abstraction-and-realization.md` without alias. | PASS | Current navigation resolves the actual compatibility path directly. |
| 95 | Resolve current 6.1 public source at immutable bootstrap `47e9155632c44493644b0b02fa1fa625703cf480`, not repository-default `main`. | PASS | `main` is concretely still Protocol 6.0; current prompts/versioning/portability bind the compatible 6.1 bootstrap and forbid default-branch/version substitution. |

## Second-reopen defect confirmation

The second-reopen defects are closed on the evaluated candidate:

- **Package-reference closure:** package validation now traverses local Markdown links contained in shipped Markdown resources, rejects nested missing local routes, and rejects unreachable packaged Markdown. Current bundle construction/validation passed on the Stage-B semantic source.
- **Direct-route versus payload discipline:** skill entrypoint routes remain the activation/progressive-disclosure contract while the distributed package payload is closed under the bounded references required for self-contained use. Existing progressive-disclosure tests and the strengthened closure tests both pass.
- **Version-correct public fallback:** current workflow prompts and versioning guidance explicitly bind Protocol 6.1 public source to immutable bootstrap `47e9155632c44493644b0b02fa1fa625703cf480`; the current default branch is independently verified as Protocol 6.0, so the fallback does not rely on cutover state.
- **Human-facing context:** current Protocol-owned guides/entrypoints introduced by the repair use early background/terminology orientation. This qualification report itself defines SSDP, D1-D4, concretization, evidence realization, semantic candidate, and public-source bootstrap before relying on those concepts.
- **Historical preservation:** the accepted frozen Protocol 5.16 and Protocol 6.0 identities remain version-bound and were validated by the Stage-B snapshot/Core acceptance.
- **Generated-source integrity:** canonical package build, package validation, committed `dist/` parity, and current Protocol 6.1 snapshot parity all passed after the Stage-B source changes.

## Disposition

Fresh behavioral qualification result: **PASS — 95/95, 0 failures, no Serious Challenge**.

This closes only the Stage-C behavioral-qualification gate. It does not constitute the required fresh independent D3 Review and does not authorize replacement recovery or lifecycle closeout by itself. Independent Review of semantic candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4` remains required.