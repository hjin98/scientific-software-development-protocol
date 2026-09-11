---
kind: ssdp62-agent-behavioral-qualification-result
protocol_version: 6.2.0
profile_id: ssdp-protocol-6.2
profile_schema_version: 2
candidate_under_test: 610360683f0d36deaaeabd1e0ffc3c7127ea8374
public_source_bootstrap: 1181c2031710c5d343194d87d08543290fded0ab
accepted_rollback_protocol: 6.1.0
accepted_rollback_commit: 802e75af261efb4f70d71284d860613a2197b639
executor_model: GPT-5.6 Sol
date: 2026-09-10
scenario_count: 115
pass_count: 115
fail_count: 0
live_routing_claim: unavailable
independent_review: pending
authority: non-normative-qualification-evidence
---

# Protocol 6.2 Fresh 115-Case Behavioral Qualification

## Disposition

**QUALIFICATION PASS — 115/115 scenario decisions conform for the candidate under test.**

This is Stage-F qualification evidence, not Protocol 6.2 lifecycle acceptance. Protocol 6.1 remains accepted-current/rollback authority until the required independent Protocol/D3 Review, recovery mapping, generated-artifact reconciliation after that mapping, lifecycle closeout, and any separately authorized cutover all complete.

No empirical claim is made that a particular live ChatGPT/Codex/Claude/other harness actually consumes fewer tokens, loads only the statically selected resources, or improves model performance. This run can establish semantic decision behavior, static routing structure, package/source reachability, and executed repository/Core checks available in this environment; it cannot substitute those for live context telemetry.

## Candidate and executed repository gates

The semantic/qualification target is commit `610360683f0d36deaaeabd1e0ffc3c7127ea8374`. Its ordinary GitHub Actions run `34544083099` passed both repository jobs:

- source protocol regressions;
- canonical package build;
- independent generated-package validation;
- committed `dist/` parity;
- patch-whitespace validation;
- generated Protocol snapshot parity;
- full Orchestrator Core acceptance, including installed wheel/sdist product tests.

The last Core blocker was not a product or concurrency defect. A legacy Core-v1 offline fixture was intentionally part of the frozen 5.16 test family but omitted its profile selector and therefore accidentally inherited the newly correct 6.2 default. The accepted repair made that frozen test version-explicit (`sdp-protocol-5.16`) and restored the original parallel Core runner. No diagnostic workflow or runner workaround remains in the candidate.

## Qualification method

This run freshly re-read and evaluated the decision semantics of:

- scenarios 1–80 in `qualification/ssdp6/SCENARIOS.md`;
- scenarios 81–95 in `qualification/ssdp6/SCENARIOS-6.1-ADDITIONS.md`;
- scenarios 96–115 in `qualification/ssdp6/SCENARIOS-6.2-ADDITIONS.md`.

The current Protocol 6.2 canonical owners, role/specialist routers, preservation census, version/recovery contract, generated `ssdp-protocol-6.2` profile/snapshot, frozen 5.16/6.0/6.1 profiles, and current regression/package evidence were used as the governing evidence surface. The prior Protocol 6.1 95-case result was background/history only; its old pass count was not reused as the 6.2 result.

For inherited cases whose prose says “current 6.1”, qualification preserves the behavioral capability and the intentionally frozen version identity rather than pretending obsolete current-version wording remains current. Thus, for example, the dangling-current-navigation invariant in case 94 applies to the real current 6.2 kernel path while frozen 6.1 continues to use its historical path, and case 95 continues to require the exact immutable 6.1 public bootstrap for 6.1 work.

## Fresh scenario decisions

| # | Result | Fresh 6.2 decision |
|---:|:---:|---|
| 1 | PASS | Equivalent private-helper replacement remains D4 after proportionate upstream-impact exclusion. |
| 2 | PASS | Durable state-ownership change routes to D3, then D4, without manufacturing D2 change. |
| 3 | PASS | Reduction error outside the accepted envelope is D2, not merely threading machinery. |
| 4 | PASS | Changing the estimand is D1 regardless of code-diff size. |
| 5 | PASS | Security/deployment constraints stay at their real D3/D4 or direct governed level. |
| 6 | PASS | A shared concretization must satisfy every applicable parent authority. |
| 7 | PASS | Invalidation follows material dependency; unaffected sibling authority/evidence survives. |
| 8 | PASS | Existing library/helper identity remains delegated unless authority requires it. |
| 9 | PASS | Cycle-scoped workplan freeze does not silently become durable D3 authority. |
| 10 | PASS | D2 may route directly to D4 when D3 authority remains unchanged. |
| 11 | PASS | Written D3 conformance cannot pass a D3 abstraction that omits material D2 semantics. |
| 12 | PASS | A D2 abstraction that cannot preserve D1 must reopen D2 even when code follows D2 literally. |
| 13 | PASS | Multiple valid concretizations are judged against the abstraction, not one historical path. |
| 14 | PASS | Local green checks cannot close a failed composed D4→D1 observable. |
| 15 | PASS | Internal verification and external/model adequacy remain distinct claims. |
| 16 | PASS | Pure mathematical work uses proof/reference theory rather than invented empirical ceremony. |
| 17 | PASS | Governed engineering qualification is treated as the applicable external/direct authority. |
| 18 | PASS | Numerical/discretization uncertainty remains D2; model/physical uncertainty remains D1. |
| 19 | PASS | A reference oracle sharing the production defect is insufficiently independent. |
| 20 | PASS | Exact discrete invariants are not weakened to tolerance to accommodate a defect. |
| 21 | PASS | Known limiting-behavior failure blocks D2 despite finite fixtures. |
| 22 | PASS | Convergence-order regression is material D2 evidence despite loose pointwise passes. |
| 23 | PASS | Tolerances follow prior conditioning/precision authority, not post-hoc widening. |
| 24 | PASS | Material stochastic-estimator bias routes to D2 even when seeded fixtures pass. |
| 25 | PASS | Restart-induced estimator change follows D2 equivalence semantics, not storage labels alone. |
| 26 | PASS | GPU speed cannot override D2 numerical-equivalence failure. |
| 27 | PASS | GPU machinery remains absent/cold when project authority does not request it. |
| 28 | PASS | Literature is evidence that may challenge D1; it does not silently replace project authority. |
| 29 | PASS | Release-pinned publication truth remains frozen while current authority may advance separately. |
| 30 | PASS | An unaccepted draft method paper cannot govern implementation. |
| 31 | PASS | Contradictory accepted invariants trigger Serious Challenge and human adjudication. |
| 32 | PASS | Unrealizable D3 is challenged rather than surrounded with reconciliation machinery. |
| 33 | PASS | Scientifically material ambiguity triggers Serious Challenge rather than silent interpretation. |
| 34 | PASS | A material logical fallacy in governing authority is challengeable regardless of author identity. |
| 35 | PASS | A valid small counterexample to an accepted D2 guarantee challenges D2. |
| 36 | PASS | A clean implementation of the wrong scientific workflow challenges the earliest inadequate abstraction. |
| 37 | PASS | A coherent-parent flag bug remains an ordinary D4 blocker. |
| 38 | PASS | Notational/style preference alone does not trigger Serious Challenge. |
| 39 | PASS | Weak non-material speculation is not escalated. |
| 40 | PASS | Bare human dismissal does not convert unresolved contradiction into Pass. |
| 41 | PASS | Sound new evidence can resolve and close a prior Challenge; the agent must update. |
| 42 | PASS | Falsified agent concern is withdrawn rather than defended for consistency. |
| 43 | PASS | Policy-permitted human risk override remains visibly unresolved risk, not ordinary Pass. |
| 44 | PASS | Governing Serious Challenge to Protocol 6 itself cannot be overridden into release. |
| 45 | PASS | Repeated manifestations of one contradiction consolidate under one root Challenge. |
| 46 | PASS | A test that mocks the semantic owner cannot proxy-pass that owner. |
| 47 | PASS | Stage-local affected regression must close before dependent executable work proceeds. |
| 48 | PASS | Final affected regression follows the final material executable edit. |
| 49 | PASS | Remove/rewire the defect-producing machinery before adding a wrapper when equivalent. |
| 50 | PASS | A 5.16 workplan selects frozen `sdp-protocol-5.16` schema v1. |
| 51 | PASS | A 6.0 workplan selects frozen `ssdp-protocol-6.0` schema v2 rather than the 6.2 default. |
| 52 | PASS | Unsupported protocol versions fail explicitly instead of silently selecting latest. |
| 53 | PASS | `serious_challenge` is terminal for automatic normal routing pending adjudication. |
| 54 | PASS | Human-pending state can be represented but not converted into invented acceptance. |
| 55 | PASS | Complexity/churn/mutation measures remain sensors, not verdict thresholds. |
| 56 | PASS | Recovery claims prefer bounded deterministic failure injection through the real owner. |
| 57 | PASS | Missing history cannot support invented longitudinal trends. |
| 58 | PASS | Guide-only drift routes to documentation rather than reopening sound D1–D4 authority. |
| 59 | PASS | Generated-artifact drift is repaired from canonical source, never hand-patched as authority. |
| 60 | PASS | Missing compatible local source falls back only to an evidence-backed immutable compatible public source; otherwise truthful non-closure. |
| 61 | PASS | Protocol-5 adaptive-concretization capability is directly recovered under Protocol-6 parent/cycle/delegation semantics. |
| 62 | PASS | Historical vocabulary may disappear when its behavioral safeguard is preserved by stronger current doctrine. |
| 63 | PASS | Retained legacy words cannot compensate for lost delegated-authority safeguards. |
| 64 | PASS | Urgent bounded mitigation may precede simplification but remains temporary debt/risk. |
| 65 | PASS | Incident survival does not promote a hotfix into durable authority. |
| 66 | PASS | Resumable working state remains compact derived coordination state, not parallel requirements authority. |
| 67 | PASS | Frozen historical terminology stays in historical recovery without contaminating current 6.2 doctrine. |
| 68 | PASS | Material D1/D2/durable-D3 authority cannot become accepted-current on author-only review. |
| 69 | PASS | Explicit stale/archived/incomplete D4 change-plan selection is rejected while selector omission remains a valid proportional route when authority suffices. |
| 70 | PASS | Durable evidence specification may survive D4 owner replacement, but realization/applicability must be remapped/rerun. |
| 71 | PASS | A stale pass is not current confirmation without re-established applicability. |
| 72 | PASS | A stale fail is not current refutation and cannot force obsolete behavior back into production. |
| 73 | PASS | Shared expected-value defects are recognized as common-mode evidence, not independent confirmations. |
| 74 | PASS | Missing edge in an uncertified partial dependency map is not proof of independence. |
| 75 | PASS | Semantic-evolution rationale may prevent repeated dead-end exploration while current authority remains controlling. |
| 76 | PASS | Newly introduced non-common D1 terminology receives background definition before normative reliance. |
| 77 | PASS | Non-obvious abbreviations use `full term (ABC)` at first explanatory use. |
| 78 | PASS | Background explanation cannot editorially replace or weaken normative D2 semantics. |
| 79 | PASS | A 6.0 workplan still resolves frozen `ssdp-protocol-6.0` bytes/semantics under the 6.2 installation. |
| 80 | PASS | A 6.1 workplan still resolves frozen `ssdp-protocol-6.1` schema-v2 semantics; 6.2 default identity does not rewrite it. |
| 81 | PASS | Historical/compatibility identifiers are opaque versioned strings; current 6.2 doctrine uses current concretization nomenclature. |
| 82 | PASS | `CONCRETIZES`, `INSTANTIATES`, `GENERATED_BY`, `EVIDENCES`, and `EXECUTION_DEPENDS_ON` retain their governed relation directions. |
| 83 | PASS | A D4 observation can challenge an inadequate upstream authority rather than forcing a local code patch. |
| 84 | PASS | Evidence specification/oracle defect remains a first-class explanation and cannot silently rewrite production authority. |
| 85 | PASS | High-level evidence does not replace required D4 conformance; D4 evidence does not establish D1 external adequacy. |
| 86 | PASS | Retirement waits for current dependency, evidence, compatibility, and historical-rationale closure. |
| 87 | PASS | Manual/document-controlled Protocol operation remains first-class when no orchestrator/higher machinery is available. |
| 88 | PASS | Specialized D2 named-method context is explained without moving algorithmic authority into background prose. |
| 89 | PASS | Model familiarity with an acronym cannot substitute for reader-facing first-use expansion. |
| 90 | PASS | Cross-file background is sufficient only for an explicitly supplied composition; standalone artifacts remain independently interpretable. |
| 91 | PASS | Machine identifiers remain compact while human documentation explains non-obvious meaning. |
| 92 | PASS | Frozen Protocol-5 artifacts remain version-faithful; new presentation standards do not rewrite historical bytes. |
| 93 | PASS | Evidence execution is called realization, not D1–D4 concretization. |
| 94 | PASS | Capability preserved under 6.2: current navigation must resolve the real current kernel (`abstraction-and-concretization.md`); frozen 6.1 retains its historical `abstraction-and-realization.md` path without a current alias. |
| 95 | PASS | 6.1 work still resolves public fallback to exact immutable bootstrap `47e9155632c44493644b0b02fa1fa625703cf480`, never repository default/latest. |
| 96 | PASS | A writer cannot shrink governed scope to manufacture completeness. |
| 97 | PASS | Task-local cold C++ doctrine remains globally preserved and reachable. |
| 98 | PASS | A stronger canonical generalization may replace repeated narrower formulations after explicit preservation proof. |
| 99 | PASS | Similar wording does not justify merging semantically distinct exceptions; unresolved authority conflict routes upward. |
| 100 | PASS | Mutation/CUDA/Git procedures stay outside the irreducible universal hot kernel. |
| 101 | PASS | Mixed Python/C++ D3 concern routes root → `language-profiles.md` → both triggered leaves rather than root enumeration. |
| 102 | PASS | Ordinary Markdown hyperlinks/package membership do not activate unrelated concern context. |
| 103 | PASS | Once executable-language routing classifies C++ as material, the C++ leaf is required. |
| 104 | PASS | Activation cycles/back-edges that re-load ancestors are rejected/rewired. |
| 105 | PASS | Canonical router prose outranks stale generated graphs/matrices/traces. |
| 106 | PASS | An already-valid owner loaded for the same scope is reused instead of repeatedly reloaded. |
| 107 | PASS | Changed authority/candidate/version invalidates stale compact summaries and requires remapping/reread. |
| 108 | PASS | An active Serious Challenge receives attention priority and blocks unqualified closure. |
| 109 | PASS | A lower-salience required validation still blocks even after a high-impact blocker is fixed. |
| 110 | PASS | Current owner + qualification + semantic evolution are the normal historical path; archived workplans stay targeted/cold. |
| 111 | PASS | Compact handoff is valid only when task-specific authority/decisions/evidence/blockers/reopen triggers remain snapshot-complete and resolvable. |
| 112 | PASS | Equations, schema tokens, immutable compatibility IDs and other exact governing forms are preserved/referenced exactly. |
| 113 | PASS | Qualification compression may omit raw detail but never contradictory admissible evidence or its consequence. |
| 114 | PASS | Current 6.2 uses `abstraction-and-concretization.md`; frozen 6.1 recovery keeps its historical path without creating a current alias. |
| 115 | PASS | The pre-bootstrap counterfactual correctly requires truthful non-closure rather than guessing. In the actual post-bootstrap state, 6.2 public fallback uses exact immutable bootstrap `1181c2031710c5d343194d87d08543290fded0ab`. |

## Static 6.1 → 6.2 activation-trace comparison

This is a static router comparison, not runtime context telemetry. The comparison asks whether required decisions remain reachable while generic/specialized owners no longer enter the hot path merely because a broad role is active.

| Representative task | Protocol 6.1 static hot-path tendency | Protocol 6.2 static route | Qualification |
|---|---|---|---|
| Local D4 helper repair | D4 root carried a large role-critical set plus direct language/tool dispatch detail; ordinary material implementation often entered workflow/evidence/testing/version/health and language/tool leaves early. | `software-implementation` → universal kernel + D4 specification; workflow/testing/evidence/language/tool owners activate only when their stated concern is material, with language/tool leaves delegated to their concern routers. | Cleaner: local equivalent repair can stay on the minimal D4 decision surface while all affected-regression/owner/challenge triggers remain visible. |
| D3 workplan | D3 root directly carried multiple mandatory role-critical owners and direct language/tool leaf dispatch. | `software-design` → universal kernel + architecture owner → workflow for workplan; evidence/testing/version/language/tool/health activate only on their decision predicates. | Cleaner without hiding workplan or acceptance closure. |
| D2 numerical change | Broad shared doctrine and cross-cutting references were more routinely co-loaded. | D2 root/kernel owns numerical method; D1 only when scientific meaning is implicated; testing/evidence/language/tool concerns activate conditionally. | Required numerical fidelity stays hot; unrelated implementation detail stays cold. |
| D1 formulation change | Cross-cutting lifecycle detail could compete with formulation authority. | D1 root/kernel + scientific-formulation owner; lower domains activate only when realization is affected. | Earliest-domain authority is more salient; downstream obligations remain reachable. |
| Documentation reconciliation | Documentation support previously inherited more broad protocol payload through package/reference structure. | `software-documentation` → kernel + documentation-maintenance + documentation/evidence; scientific-technical-writing only for human-facing technical material; represented semantic owners only as needed. | Current-vs-history/source-chain and background/acronym rules stay active without loading unrelated engineering domains. |
| Maintenance audit | Long-horizon, architecture, testing, evidence, Git, tooling and other topics could appear as a flatter broad surface. | `software-maintenance-audit` → kernel + long-horizon owner; architecture/testing/evidence/Git/tooling/etc. activate only when a signal enters that concern. | Sensors/root-cause routing stay active; unrelated specialists stay cold. |
| Release/package work | Broad D4 role machinery could activate before the specific release concern. | D4 root/kernel + specification → release owner when packaging/release is material; testing/workflow/version only as required by the release claim/workplan. | Package/recovery correctness remains reachable without unconditional tool/language detail. |
| Historical recovery/migration | Versioning plus broad current-role routing risked bringing current and historical doctrine together early. | Current role/kernel → versioning owner → exact frozen profile/bootstrap/recovery source; historical detail and archived plans remain cold unless lineage is ambiguous/challenged. | Stronger separation of current doctrine from frozen historical semantics. |
| Closeout | Lifecycle, documentation, evidence and repository concerns could be repeated across roots/prompts. | workflow/closeout route activates documentation/hygiene/evidence/version owners only for actual closure obligations; prompts keep shared stage contract rather than duplicating role-internal routing. | Mandatory lower-salience closure checks remain explicit without amendment replay. |

### Static-trace conclusion

The 6.2 topology is materially cleaner for the representative routes: root entrypoints establish the universal kernel plus their own semantic owner, then concern routers dispatch narrower leaves. Direct tool and Python/C++ leaf enumeration has been removed from D3/D4 roots; hyperlinks/package closure remain transport/navigation rather than activation; repeated generic doctrine is concentrated at owners. No required capability identified by the 115 scenarios became unreachable or dependent on hidden context.

No numerical token-count threshold is used. The improvement claim is structural: fewer unnecessary unconditional routes and less repeated owner prose while preserving visible triggers and transitive package/source reachability. Actual model context size/latency/quality requires live harness evidence and is not claimed here.

## Four required falsification passes

### 1. Loss test — PASS

The run actively looked for obligations that compaction might have deleted: stewardship/protected-outcome semantics, D4 real-owner/proxy-proof acceptance, evidence target versus execution dependency, stale pass/fail treatment, common-mode evidence, stage-local/final regression, convergence/simplification, language/tool dispatch, historical version selection, public fallback, documentation background/acronym rules, and challenge/override semantics. The implementation/review cycle had already found and restored a genuine stewardship omission; the current candidate preserves the resulting owner plus regression oracle. No additional orphaned accepted capability was found in this qualification pass.

### 2. Scope/materiality laundering test — PASS

Scenarios 96–97 and the current kernel distinguish governed scope from writer-declared scope and decision-local coldness from global preservation. The static trace comparison did not obtain lower context density by declaring required evidence/version/language/tool concerns out of scope; each remains activated by a visible materiality predicate and packaged/reachable when triggered.

### 3. Priority-inversion test — PASS

Scenarios 108–109 and current completion/reporting contracts put Serious Challenge/blockers first while preserving mandatory lower-salience validation and impact closure. A prominent high-consequence finding therefore cannot erase a routine required package/regression/evidence condition.

### 4. False-compaction test — PASS

The current topology does not replace role prose with a machine-authoritative routing registry. Canonical Markdown routers remain authority, generated/package graphs are derivative, ordinary hyperlinks do not activate context, concern routers narrow to leaves, and stale summaries are explicitly invalidated by changed authority/version/candidate/material exact-text needs. The 6.2 profile remains schema v2 because the machine lifecycle contract did not change; representation compaction was not used as a pretext for a new control plane.

## Live-routing evidence boundary

No fresh live harness/model/install-mode routing trace with exposed resource-access/context telemetry was available in this execution environment. Therefore:

- **available:** semantic scenario decisions, source/static routing inspection, package/source reachability, generated snapshot/profile validation, installed-product/Core behavior;
- **unavailable:** empirical proof that a named external harness actually loads exactly the predicted resource subset, empirical token/context reduction, latency change, or quality/performance improvement.

Per the workplan, this is truthful non-closure only for those empirical claims. Protocol 6.2 makes no such empirical claim in this result.

## Independent Review boundary

This qualification was produced in the same continuing authoring/implementation context that participated in the candidate. It therefore **does not satisfy the required independent Protocol/D3 Review**. No recovery SHA is selected and no `6.2.0 -> recovery SHA` mapping is authorized by this result.

The next lifecycle gate is an independent reviewer/context that did not author the semantic candidate. It must attempt to falsify the preservation map, governed-scope/materiality handling, owner/activation topology, cold-path reachability, historical proof path, static/live evidence boundaries, generated/profile/package correctness, 115-case qualification, and absence of hidden scope laundering or false compaction.

## Stage-F status

Authored semantic qualification, focused 6.2 scenarios, static activation comparison, and static-vs-live claim discipline are **complete and passing** for candidate `610360683f0d36deaaeabd1e0ffc3c7127ea8374`.

Stage F as a lifecycle gate remains **OPEN / NOT YET ACCEPTED** solely because its required independent Review has not yet been performed by an independent context. Protocol 6.1 remains accepted-current/rollback. Protocol 6.2 must not publish a recovery mapping or cut over `main` on the strength of this report alone.
