---
kind: abstraction-concretization-change-plan
workplan_id: SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT
protocol_version: 6.1.0
target_protocol_version: 6.2.0
status: active
created_date: 2026-09-10
reviewed_date: 2026-09-10
final_closure_reviewed_date: 2026-09-10
design_closure_status: pass-after-repair
implementation_handoff: authorized
active_serious_challenge: none
parent_semantic_baseline: cec29671b9db59d20124a6e2ce99725ed60b8f0a
parent_protocol_61_recovery: 802e75af261efb4f70d71284d860613a2197b639
---

# SSDP 6.2 Lossless Representation and Progressive-Disclosure Refinement

## Background and terminology

The Scientific Software Development Protocol (SSDP) is intentionally thorough. Protocol 6.2 addresses how that sophistication is represented: semantically complete doctrine can still become hard to execute when rules are repeatedly restated, activation paths become dense, historical revisions remain in the normal reasoning path, or routine detail competes with governing decisions.

For this plan:

- **representation** — any SSDP-controlled human/agent communication surface, including skills, shared references, prompts, workplans, handoffs, specifications, method/architecture documents, direct agent reports/responses, inter-agent/delegation messages, reviews, qualification/evidence summaries, dependency/evolution records, guides, runbooks, and resumable state;
- **governed scope** — the semantic/decision surface imposed by explicit user/task authority, the selected role/domain, affected dependencies, compatibility obligations, and applicable evidence/closure requirements; it is not freely shrinkable by the writer;
- **material semantic element** — information whose omission, weakening, ambiguity, or loss of salience can change a supported decision, behavior, authority/compatibility interpretation, evidence assessment, or closure condition; materiality is decision-local and does not by itself authorize deletion from the protocol;
- **lossless representation** — every material semantic element required by the governed scope remains recoverable, correctly interpretable, and sufficiently salient to support the intended decision;
- **hot path** — information normally loaded/presented to make the current decision;
- **cold path** — recoverable detail activated only when a visible condition makes it relevant;
- **progressive disclosure** — adding doctrine to active context only when the current semantic question triggers it;
- **activation dependency** — an explicit read prerequisite for a named decision; it is distinct from ordinary hyperlinks, semantic dependencies, evidence execution dependencies, and package transport dependencies;
- **attention balance** — prominence/context allocation proportional to consequence, uncertainty, risk, and immediate decision relevance.

The objective is not minimum bytes, paragraphs, files, or hops. Over-compression, excessive abbreviation, fragmentation, hidden prerequisites, or long reference chains can increase cognitive cost. The target is the minimum complete, precise, readily interpretable representation.

## 1. Outcome, authority, and scope

Protocol 6.2 SHALL preserve every accepted Protocol 6.1 doctrine and every still-valid historical capability while making current representation terser, more precise, less repetitive, more importance-weighted, easier to route, and cheaper in active context.

A representative substantial D3 Review under 6.1 can load roughly 112 kB of protocol Markdown before task-specific workplan/code/tests/evidence, versus roughly 80 kB for the analogous 6.0 core. These counts are sensors, not thresholds: physical package size is not the defect; repeated doctrine, salience dilution, unnecessary activation, and synchronization debt are.

Governing preservation baseline:

- final Protocol 6.1 closeout: `cec29671b9db59d20124a6e2ce99725ed60b8f0a`;
- accepted 6.1 recovery: `802e75af261efb4f70d71284d860613a2197b639`;
- immutable 6.0 recovery: `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`;
- immutable 5.16 recovery: `e151daaf5c8eebb351a85cfed86170fda80fb5e3`;
- all 95 accepted Protocol 6.1 behavioral scenarios plus applicable route/package/language/tool/orchestrator tests;
- all accepted current 6.1 protocol owners and the semantic-evolution/archived-workplan record needed to recover still-valid historical capabilities.

This is a backward-compatible representation-doctrine strengthening with D3/D4 routing/document/package/profile consequences. It does not alter D1 scientific meaning, D2 numerical meaning, or any accepted 6.1 authority/evidence/Challenge/compatibility threshold. **This workplan has no semantic-supersession escape hatch:** if compaction exposes a genuine conflict in accepted authority, stop the affected compaction and route a separate owning-domain resolution; do not use 6.2 representation work to choose new truth.

The rule governs SSDP-authored/controlled representations and remains subordinate to higher-priority user, platform/system, safety, legal/regulatory, external API, or other governed source authority. When exact wording, equations, symbols, identifiers, or quoted external authority carry the governed meaning, retain or directly reference the exact form rather than paraphrasing it into a weaker contract.

Non-goals: reduce ZIP size for its own sake; weaken doctrine to shorten prose; impose arbitrary token/paragraph limits; create a universal graph/database/context manager/new approval role; rewrite frozen 5.16/6.0/6.1 artifacts; refactor unrelated Protocol 7 architecture/control machinery; or merge/cut over to `main` without separate authorization.

## 2. Protocol 6.2 Lossless Representation Rule

### 2.1 Admissibility before optimization

A representation `R` of governed information `S` is admissible only if a competent intended reader/agent can recover and correctly interpret every material semantic element required by the **governed scope** without hidden chat, unavailable history, or unstated prerequisites.

The representation may state or summarize its scope, but that declaration cannot narrow the task/domain/affected/compatibility surface merely to make the artifact appear complete. If the governing scope is uncertain, resolve or expose the uncertainty before using compactness as an optimization criterion.

Materiality determines what must be active for a particular decision; it does not determine whether accepted doctrine may disappear globally. A rule can be non-material to one hot path and still require preservation at its canonical owner or another reachable cold path.

Losslessness includes authority/ownership and lifecycle state; governing invariants, exceptions, constraints, non-goals, uncertainty, evidence qualification, dependencies, and reopen conditions; discoverability of conditionally relevant cold-path information; and decision-critical salience where burying information could change action or closure.

A historical improvement may disappear as separate current prose only when an equal-or-stronger generalized current rule preserves its behavior and material historical rationale remains recoverable. Historical vocabulary need not remain current when the capability survives.

### 2.2 Optimization order

Among admissible representations, prefer:

```text
semantic correctness and completeness
> semantic precision and unambiguity
> importance-weighted attention
> cognitive digestibility
> context/routing efficiency
> representational compactness
```

Compactness never trades against completeness. After completeness is secured, avoidable repetition, amendment-style history, gratuitous routing depth, duplicated generic doctrine, and equal prominence for unequal concerns are defects.

### 2.3 Operational consequences

1. **One detailed owner per generic rule.** Secondary artifacts state only their local consequence plus a precise route unless a short restatement lowers total inferential cost.
2. **Generalize rather than accumulate.** Strengthen current doctrine into one coherent form; preserve chronology/supersession rationale in history instead of amendment layers on the hot path.
3. **Use progressive disclosure.** Potential relevance to a broad task class does not justify unconditional loading.
4. **Use bounded typed activation.** The active role/specialist `SKILL.md` owns root activation and routes to the canonical concern owner. A concern owner may conditionally dispatch to a narrower leaf when that question becomes knowable only inside the activated concern (for example `language-profiles.md -> python-engineering.md/cpp-engineering.md` or `tool-assisted-engineering.md -> tool-*`). Do not flatten every leaf into every skill entrypoint.
5. **Keep canonical routers authoritative and derived routing views non-authoritative.** Activation predicates/routes live in the smallest current owner that actually decides them. Any generated activation graph, trace, matrix, or report is validation/diagnostic evidence and must be derivable from those owners rather than maintained as a second routing authority.
6. **Keep activation explicit, acyclic, and useful.** Every activation hop must name a resolvable resource and a decision predicate, narrow the current question or add required semantics, never reactivate an ancestor, and never rely on an ordinary hyperlink or package membership as an implicit read command. If several triggers reach the same owner, load/reuse it once unless exact reread is newly required.
7. **Make cold paths visibly reachable.** If information can materially change a decision, a hot-path owner must expose the condition and supported route by which it becomes active. Cold must not mean undiscoverable.
8. **Reuse only valid established context.** A working summary/read is non-authoritative and reusable only while the material protocol/source identity, governing authority/workplan state, candidate/regime, and task scope remain applicable. Re-read/remap when one changes, when exact wording becomes material, or when later evidence plausibly invalidates the prior interpretation. Do not recursively summarize stale summaries into authority.
9. **Balance attention by consequence without weakening completeness.** Serious Challenges, safety/governing conflicts, current authority, blockers, high-impact uncertainty, and required decisions precede routine mechanics and historical provenance. Lower-salience mandatory constraints still remain active acceptance obligations and must not be omitted merely because they are presented later or more compactly.
10. **Minimize total inferential cost.** Merge adjacent prose/sections with the same semantic function where clarity survives; do not replace one clear local statement with a long reference chain or fragment one coherent concept merely to improve counts. Prefer section-targeted reads when tooling supports them.
11. **Preserve evidence visibility.** Summaries may keep raw detail cold, but must not hide failures, warnings, contradictory admissible evidence, unavailable required checks, uncertainty, or provenance needed to interpret a material claim.
12. **Do not deduplicate through semantic adjudication.** If apparently duplicate current texts differ materially in meaning, scope, authority, or threshold, stop editorial compaction and route the conflict to its owner; raise Serious Challenge when accepted authority itself may be defective.
13. **Keep derivatives subordinate.** Compact summaries, handoffs, prompts, records, and resumable state are representations, not replacement authority. If a derivative conflicts with its canonical owner, the owner governs and the derivative is defective.

## 3. Target representation and routing architecture

### 3.1 Minimal universal kernel and nomenclature correction

Rename the current 6.2 kernel:

```text
source/shared/references/abstraction-and-realization.md
-> source/shared/references/abstraction-and-concretization.md
```

Add the Lossless Representation Rule there so no new universally mandatory reference is created. The kernel itself must also be compacted: retain only irreducible cross-role semantics needed before ordinary role-specific reasoning, and route detailed evidence lifecycle, history, testing methods, domain examples, language/tool mechanics, and specialist doctrine to their owners. A rule is not universal-kernel material when it can be deferred behind a visible trigger without risking incorrect root role/domain classification, authority handling, Challenge/stop behavior, or interpretation of every downstream route.

Rename current `abstraction_realization_change_plan_template.md` to `abstraction_concretization_change_plan_template.md` unless a concrete supported current consumer requires the legacy path. Audit current `realization` identifiers: use **concretization** for D1-D4 semantic descent and reserve **realization** for evidence execution. Frozen 5.16/6.0/6.1 paths and terminology remain historical truth; do not add aliases/wrappers merely because Git history contains the old names.

### 3.2 Canonical owner topology

Stage A must verify the complete owner map; this initial map states the intended 6.1 ownership to preserve, not permission to invent new precedence:

```text
universal authority/challenge/representation -> abstraction-and-concretization.md
D1 formulation                              -> scientific-formulation.md
D2 numerical/algorithm method               -> numerical-algorithm-design.md
D3 architecture                             -> architecture-and-design.md
D4 specification                            -> specification-and-implementation.md
workflow/handoff/stages                     -> workflow-and-workplans.md
evidence lifecycle/evolution/dependencies   -> evidence-evolution-and-dependencies.md
testing/oracles/validation                  -> testing-and-validation.md
scientific/numerical integration evidence   -> scientific-software.md
recurrence/simplification/cycle economy     -> convergence-and-cycle-economy.md
longitudinal health/stabilization           -> long-horizon-code-health.md
version selection/recovery                  -> protocol-versioning-and-compatibility.md
repository inspection/context economy       -> repository-intake.md
document lifecycle/current-vs-history       -> documentation-maintenance.md
technical/scientific exposition             -> scientific-technical-writing.md
engineering-document/evidence communication -> documentation-and-evidence.md
language dispatch                           -> language-profiles.md
Python/C++ specialization                   -> python-engineering.md / cpp-engineering.md
relation-first tool dispatch                -> tool-assisted-engineering.md
specific analyzer methods                   -> tool-serena.md / tool-semgrep.md / tool-hypothesis.md / tool-codeql.md
configuration policy                        -> configuration-and-policy.md
concurrency/orchestration engineering       -> concurrency-and-orchestration.md
performance/parallelism                     -> performance-and-parallelism.md
storage/I/O                                 -> storage-and-io.md
security/trust                              -> security-and-trust-boundaries.md
release/distribution                        -> release-and-distribution.md
debugging/recovery mechanics                -> debugging-and-state-recovery.md
Git/version-control mechanics               -> git-and-version-control.md
workflow prompt source                      -> development-workflow-prompts.md
```

If Stage A finds that accepted 6.1 ownership differs, preserve the accepted owner or block and resolve the authority issue separately. Similar wording is not proof of duplicate semantics.

### 3.3 Bounded hierarchical activation graph

Preferred shape:

```text
orchestration / task
  -> role or specialist SKILL.md
       -> universal kernel + owning domain/concern
       -> conditionally activated concern router
            -> conditionally activated leaf
```

The root skill must expose normal role-critical routes and the conditions that enter a concern. A canonical concern router may own further conditional dispatch only inside that concern; it must not become a second general role router. Router prose should carry only the classification predicate, target, and local consequence needed to select the next owner; detailed leaf doctrine belongs at the leaf. Deeper routing is permitted only when each hop is necessary to decide the next narrower concern and is cheaper/clearer than flattening the routes.

Activation must remain cycle-free and bounded by useful information gain. Every local activation target must also be an explicit resolvable local Markdown route or equivalent validated package resource. **Activation implies reachability; reachability does not imply activation.** Standalone skill packages must contain every local resource their supported activation paths can require. Public fallback must use an explicit immutable compatible source identity rather than an unversioned external dependency.

### 3.4 Hot/cold discipline

Current operational rules required for routine decisions remain hot. Historical lineage, supporting rationale, raw evidence detail, and specialized concern doctrine stay cold until a visible trigger fires. Every cold-path item capable of changing the decision must remain reachable in supported standalone execution through the installed package or an explicit immutable compatible public-source route.

Current truth must be reconstructable without replaying revision history. History explains why; current owners explain what is true. A rule being cold for one task is not evidence that the rule is obsolete globally.

## 4. Lossless preservation contract

### 4.1 Finite representation census

Because this is protocol-wide, Stage A must census the complete durable/generative current 6.1 representation surface before deciding what is “touched.” Classify each current artifact as **refactor**, **route-only**, **cold-path**, **generated**, **frozen/historical**, or **intentionally unchanged with reason**. At minimum include:

- all four `source/roles/*/SKILL.md` entrypoints and all three `source/specialists/*/SKILL.md` entrypoints;
- every current `source/shared/references/*.md` and every current shared template;
- `AGENTS.md`, root `README.md`, `PORTABILITY.md`, `source/README.md`, and `source/SEMANTIC_DEPENDENCIES.md`;
- current workflow-prompt source and current Protocol 6.1 orchestrator profile/prompt/snapshot resources that 6.2 will supersede or generate from;
- protocol-bearing machine-readable schemas/templates and code-embedded/rendered help, status, prompt, or record text when that content communicates protocol decisions to an agent or human; ordinary implementation-only comments that carry no protocol meaning are not pulled into scope merely because they are text;
- current qualification scenario sources and routing/tool-routing qualification assets where representation/routing claims depend on them;
- the active workplan authority index and this workplan;
- `history/SEMANTIC_EVOLUTION.md` and archived workplans as cold historical inputs, without rewriting their frozen content;
- generated `dist/`/snapshot descendants as generated outputs, not independent authority.

The census covers durable sources and generators, not every ephemeral message instance. Direct agent/inter-agent outputs are governed through the rules/templates/renderers that produce them plus representative qualification scenarios.

Do not broaden this cycle into unrelated Protocol 7 architecture/document cleanup. Protocol 7 is reconciled only where version inheritance, routing, or cutover state is affected.

### 4.2 Semantic and historical preservation map

Build a bounded work-specific preservation map before substantive compaction. Use progressive disclosure in the preservation audit itself:

1. start from accepted current 6.1 canonical owners, the 95-case qualification surface, and `history/SEMANTIC_EVOLUTION.md`/current compatibility mapping;
2. map each distinct still-valid capability introduced across Protocol 5.1-5.16, 6.0, and 6.1 to its current 6.1 owner, even when obsolete vocabulary disappeared;
3. consult archived workplans or older records only where the current owner/evolution/qualification chain leaves a material capability ambiguous, apparently unmapped, contradicted, or challenged.

Do not preload or replay every historical workplan merely to prove history exists. Historical records are evidence for ambiguous lineage, not a second mandatory current execution path.

Also cover applicable route/package/language/tool/orchestrator tests and frozen 5.16/6.0/6.1 identity/compatibility behavior. For every materially removed, merged, relocated, or generalized rule, record old owner/location, new owner/location, preservation rationale, and acceptance evidence. Many old manifestations may map to one stronger current owner, but **no accepted obligation may be orphaned**.

The semantic proof direction is from the proposed current rule to every preserved historical/current obligation in its applicable regime: the new/generalized rule must be strong enough that satisfying it also satisfies the old obligation. Similar wording or broader vocabulary alone is not proof.

The preservation map is evidence/coordination, not parallel authority. It must be available to Implementation and independent Review. It may be retired at closeout after its decision-level conclusions are preserved in qualification/Review/evolution records and the final current owners/tests make the mapping reconstructable.

### 4.3 Compression proof and no-supersession rule

Acceptable compaction includes identical semantics moved to the canonical owner; narrower rules replaced by a demonstrably stronger general rule; generic prose removed from a secondary artifact while its activation/local consequence remains correct; or historical amendment prose moved cold while current generalized doctrine plus history preserves capability/rationale.

No-Pass examples include deleting untested doctrine; replacing a precise exception with a vague principle; expecting common-sense inference for an omitted obligation; retaining vocabulary while losing behavior; changing an authority boundary/evidence threshold/failure condition; declaring a narrower scope to evade an obligation; treating task-local non-materiality as authority to delete a global rule; or preserving every paragraph while merely rearranging links and leaving the same unnecessary activation load.

Within this workplan, every existing accepted obligation must finish **preserved or blocking**. Any proposed semantic retirement/supersession requires a separate accepted owning-authority change outside this representation-only cycle, followed by explicit rebase/reconciliation of this preservation baseline.

### 4.4 Context-summary applicability

Any task-local summary, loaded-fact cache, handoff condensation, or resumable state created to save context is derived coordination state. Preserve enough source identity and scope to know when it is reusable. A change in governing protocol/version, authority/workplan revision, semantic candidate, evidence regime, or relevant source can invalidate the summary without invalidating the underlying authority. Re-read the canonical owner when applicability or exact wording is uncertain rather than compounding summaries.

A cross-agent handoff may rely on compact references instead of copying generic doctrine only when the receiving environment can resolve the governing version/owner/resource. Otherwise include the minimum task-specific semantics needed for truthful continuation or report the dependency explicitly; do not assume a shared hidden cache.

### 4.5 Frozen-version isolation

Do not rewrite historical 5.16, 6.0, or 6.1 source/profile/publication semantics. Current 6.2 uses clean 6.2 terminology/routing while resolving historical work through immutable version-specific authority.

## 5. Refinement targets from the 6.1 scan

- **Kernel:** reduce the mandatory universal kernel to irreducible shared semantics; move detailed concern doctrine behind visible conditional routes.
- **Skills/specialists:** remove generic doctrinal restatement; keep root routing compact and delegate concern-local leaf dispatch to canonical routers instead of flattening every leaf into every entrypoint.
- **Evidence/testing:** evidence lifecycle/applicability/common-mode semantics stay with the evidence owner; testing retains oracle integrity, numerical/architectural/D4 validation, regression/integration, proxy-proof, failure-injection, and qualification methods.
- **Convergence/architecture/workflow/health:** convergence owns generic recurrence/simplification; other owners retain only domain-specific consequences. Long-horizon health owns longitudinal sensing/stabilization.
- **Challenge:** the kernel owns the full Serious Challenge model; other artifacts keep only their local threshold/routing consequence.
- **Documentation:** technical writing owns exposition; documentation maintenance owns lifecycle/current-vs-history/source-chain; documentation-and-evidence owns engineering-document/evidence communication. All inherit rather than restate the universal representation rule.
- **Handoffs/agent outputs/records:** remain snapshot-complete for task-specific governing information; lead with disposition, governing constraints/blockers/uncertainty, then supporting evidence; keep closed chronology/raw detail cold unless decision-relevant.
- **Repository/root instructions:** preserve `AGENTS.md` as a compact repository-level router and reconcile root/source README and portability text so they do not duplicate role-internal routing.
- **Workflow prompts:** keep one shared execution/authority/evidence/representation preamble plus concise stage-specific inputs/actions/outputs/stops; do not copy detailed role-internal reference routing into the prompt.
- **Runtime/generative communication:** refactor canonical templates/renderers/help/status/prompt sources rather than hand-editing derived outputs; rendered summaries must preserve stop/blocker/uncertainty/provenance semantics while omitting non-triggered detail.
- **Historical proof path:** current owners + qualification + semantic evolution are the normal preservation route; archived workplans are targeted cold evidence for unresolved lineage, not an unconditional context preload.
- **Versioning/history:** keep current version selection/recovery operationally compact; keep exact immutable mappings and visible triggers to cold historical lineage.
- **Dependency/package topology:** distinguish semantic, activation, evidence, source/generated, and transport relationships. Bounded transitive package closure may remain when it is the simplest self-contained transport; package membership never implies active-context loading.

## 6. Implementation sequence

### Stage A — Census, baseline, and preservation evidence

1. Freeze `cec29671...` as the 6.1 semantic baseline and complete the finite representation census.
2. Verify the complete current owner topology and classify root/role/concern/leaf activation, ordinary cross-links, package closure, generated/profile routes, and cold-path retrieval.
3. Build the semantic/historical preservation map using current owners + 95 cases + semantic evolution first; consult archived workplans only for ambiguous/unmapped/challenged lineage.
4. Identify duplicate/near-duplicate doctrine, amendment-style hot-path prose, scope/materiality laundering opportunities, hidden/transitive activation, cycles/back-edges, repeated owner loading, stale-summary risks, and cold-path reachability gaps.
5. Baseline representative tasks: local D4 repair; D3 workplan; independent D4 Review; D2 work; D1 work; documentation reconciliation; maintenance audit; release/package work; historical recovery/migration; closeout. Record each required protocol resource, trigger/hop, whether it is initial or conditional, and why the load is necessary. Useful sensors include unique active protocol tokens/bytes, duplicated/reloaded content, unconditional initial reads, conditional reads, and routing hops; none is a standalone acceptance threshold.
6. Baseline representative output salience with at least one case containing a high-consequence blocker/Challenge amid routine evidence and one case containing a lower-salience but still mandatory closure condition.

Stage A changes no accepted protocol semantics.

### Stage B — Kernel and nomenclature

1. Rename the current kernel/template as specified and add the Lossless Representation Rule.
2. Compact the universal kernel to the minimum irreducible shared semantics while mapping every removed detail to its owner and applying the deferral test in Section 3.1.
3. Reconcile current `realization` usage and update current source links/tests/dependency records without touching frozen releases.
4. Verify no supported current consumer depends on a legacy path before deleting it; if such a contract exists, retain the minimum explicit compatibility mechanism with retirement condition rather than an accidental permanent alias.

### Stage C — Canonical-owner normalization

1. Consolidate each generic doctrine at its accepted owner and complete the owner map across all current references.
2. Replace secondary full restatements with local consequences and precise routes; keep enough local context for standalone comprehension.
3. If duplicate-looking texts disagree semantically or ownership is ambiguous, block that compaction and resolve through the owning authority outside this plan before continuing.
4. Remove amendment-style current prose only after capability/history preservation is proven.
5. Reconcile `source/SEMANTIC_DEPENDENCIES.md`, root/source navigation, and current documentation with the resulting owner topology.

### Stage D — Progressive disclosure and communication surfaces

1. Refactor all role/specialist `SKILL.md` entrypoints to compact root routers plus role-specific method/completion semantics.
2. Establish the bounded hierarchical activation graph: root role routes to concern owner; concern owner may dispatch to narrower leaves. Remove accidental activation from ordinary hyperlinks, cycles/back-edges, and duplicate reads.
3. Keep canonical router prose as routing authority. If tests or documentation need an activation graph/matrix/trace, derive it from those routers or keep it explicitly diagnostic; do not create a separately maintained routing registry.
4. Refactor workflow prompts to shared cross-stage contracts plus stage deltas; keep role-internal concern/leaf routing in the role/reference hierarchy rather than duplicating it in orchestration.
5. Apply the representation rule to templates, handoffs, direct agent reports/responses, inter-agent messages, reviews/qualification/audit reporting, resumable state, protocol-bearing renderers/help/status records, `AGENTS.md`, portability/navigation, and technical-writing guidance.
6. Ensure every material cold-path condition has a visible hot trigger and supported standalone retrieval path; validate that every activated local resource is packaged/reachable.
7. Validate context-reuse rules with stale-summary counterexamples: changed protocol/authority/candidate or newly material exact wording must trigger reread/remap rather than reuse.

### Stage E — 6.2 profile, immutable public fallback, and packages

A Git commit cannot self-name. Avoid repeating the 6.1 bootstrap/recovery defect:

1. Make the complete 6.2 public-fallback source set internally coherent: current role/specialist entrypoints, every local routed reference/template, `source/PROTOCOL_VERSION`, and required navigation/version-resolution source must build and validate without an unknown self SHA.
2. Create an immutable **6.2 public-source bootstrap commit** only after that fallback source set is complete and standalone package/link validation passes.
3. In a later **semantic-candidate commit**, publish the exact bootstrap SHA in current public-resolution prompts/versioning/portability surfaces. Apart from required generated descendants, this mapping step must not smuggle unrelated semantic changes.
4. Add/freeze `ssdp-protocol-6.2`; preserve `sdp-protocol-5.16`, `ssdp-protocol-6.0`, and `ssdp-protocol-6.1` byte/behavior semantics. Retain profile schema v2 unless an actual machine contract changes.
5. Rebuild current distributions/snapshots from canonical source; validate package structure, every supported activation-resource closure, ordinary link closure, source-to-generated parity, version identity, and closest supported consumer ingestion.
6. Test no-local-compatible-skill and incompatible-default-branch resolution against the exact immutable 6.2 bootstrap. Repository default branch is never a version oracle.

### Stage F — Qualification and independent Review

1. Run complete affected repository/package/orchestrator regression.
2. Re-run the semantic capability of all 95 Protocol 6.1 scenarios against 6.2, preserving frozen-version semantics where cases intentionally target 5.16/6.0/6.1.
3. Add focused 6.2 cases for: lossless vs lossy compression; anti-scope-laundering; task-local non-materiality versus global preservation; stronger generalization vs amendment accumulation; one owner + local delta; minimal-kernel deferral; bounded hierarchical concern routing; non-activating ordinary hyperlink; required conditional leaf activation; activation-cycle/back-edge rejection; derived-routing-view non-authority; duplicate-owner load reuse; stale context-summary invalidation; blocker/Serious-Challenge salience; lower-salience mandatory closure preservation; cold historical recoverability without full-history preload; snapshot-complete compact handoff; exact-text preservation; semantic-conflict non-editorial resolution; current renamed kernel vs frozen historical path; and immutable 6.2 public fallback under incompatible/default-branch conditions.
4. Compare 6.1 and 6.2 static activation traces for the representative Stage-A tasks. Require materially cleaner unnecessary/repeated context with every retained hop justified; do not game numerical metrics by hiding required information or shrinking declared scope.
5. Separately test **live routing behavior** on each harness/model/install mode for which a 6.2 empirical routing claim will be made. Use fresh sessions and normal supported entrypoints rather than preloading the preservation map. Where traces/resource access are exposed, verify that required conditional resources activate, non-triggered concerns remain cold, and attention prioritization does not cause a mandatory lower-salience condition to disappear from closure reasoning. Reuse/extend existing routing sentinels when sufficient; do not invent a broad new framework solely for this release.
6. If live telemetry/harness access is unavailable, report that empirical claim unavailable: static semantics/package tests may still establish the protocol contract but must not be represented as proof of actual model context use or performance improvement.
7. Perform an **independent** D3/protocol Review by a reviewer/context that did not author the semantic candidate. Review the preservation map, scope/materiality handling, owner/activation topology, cold-path reachability, historical proof path, static and available live routing evidence, generated/profile/package correctness, and qualification evidence.
8. No PASS if compaction makes accepted behavior ambiguous, unavailable, stale-context-dependent, less salient where salience affects correct action, dependent on hidden context, or apparently complete only because scope/materiality was narrowed after the fact.

### Stage G — Recovery, closeout, and Protocol 7 reconciliation

1. After semantic-candidate qualification and independent Review pass, choose an immutable 6.2 recovery commit containing the accepted candidate and required decision evidence through ancestry.
2. Publish `6.2.0 -> <exact recovery SHA>` only in a later mapping commit; preserve the distinct public-source bootstrap identity. Regenerate mapping-bearing descendants and rerun targeted recovery/parity checks.
3. Record material 6.2 semantic evolution; archive this workplan only after accepted rules reside in current canonical owners and evidence/impact closure is complete.
4. Keep Protocol 6.1 as accepted current/rollback baseline until 6.2 qualification, Review, recovery mapping, generated-artifact reconciliation, and lifecycle closeout all pass.
5. Reconcile the active Protocol 7 handoff explicitly after 6.2 acceptance. On this branch, Protocol 7 D4 remains downstream of 6.2 completion/reconciliation plus its existing deliberate D3 architecture-reopen prerequisite. Do not silently rewrite Protocol 7 architecture semantics; representation-only inheritance should use a compact compatible handoff update, while any material D3 change remains a D3 reopen.
6. Do not merge/cut over `main` without separate authorization.

## 7. Acceptance and falsification

### 7.1 Hard no-loss gates

Protocol 6.2 is No-Pass if any accepted 6.1 doctrine or still-valid historical capability is orphaned, weakened, ambiguously represented, or behaviorally changed; governed scope is narrowed to avoid an obligation; task-local non-materiality is used to delete globally required doctrine; attention weighting hides a mandatory active constraint; a frozen historical artifact/profile is rewritten; a derivative summary or generated routing view becomes de facto authority; a stale context summary is reused after a materially invalidating change; a secondary artifact gains a hidden prerequisite; a cold-path condition is undiscoverable; an activation edge is cyclic/implicit/unresolvable; a current route depends on incidental Markdown/package topology; exact governing wording is weakened by paraphrase; semantic conflict is resolved editorially; or representation becomes shorter but materially harder to interpret.

Every transformed accepted obligation in the preservation map must close as **preserved or blocking**. Green tests alone do not prove losslessness, and this cycle may not mark an accepted 6.1 capability “superseded” merely to make compaction easier.

### 7.2 Representation-quality gates after no-loss passes

Independent Review must establish:

- complete census disposition and no orphan current representation surface;
- governed-scope integrity and decision-local materiality that cannot be used as deletion authority;
- one identifiable detailed owner for each generic rule and justified local delta elsewhere;
- a minimal universal kernel rather than a universal encyclopedia;
- bounded, explicit, acyclic, decision-triggered activation with concern-local leaf dispatch and reuse rather than repeated loading;
- canonical router ownership with any activation graph/matrix/trace derived or explicitly diagnostic rather than parallel authority;
- visible and supported hot-to-cold retrieval triggers;
- materially lower unnecessary/repeated active context on representative routes without arbitrary quotas;
- validity-scoped context reuse rather than repeated rereads or stale condensation;
- current documents that explain present truth without amendment replay;
- historical preservation that can normally be proven from current owners + qualification + semantic evolution, with archived workplans loaded only when lineage is ambiguous;
- importance-weighted outputs with high-consequence state salient while all mandatory active constraints remain represented for closure;
- snapshot-complete handoffs/agent communications without generic doctrine duplication or hidden shared-cache assumptions;
- package transport/reachability correctness independent from runtime activation semantics;
- consistent current abstraction/concretization terminology, with `realization` reserved for evidence execution outside frozen history;
- empirical routing/performance claims no broader than the live harness/model evidence actually obtained.

### 7.3 Challenge Pass

Attempt four falsifications:

1. **Loss test:** find apparently repetitive text whose removal actually loses an edge case, qualification, authority boundary, historical compatibility rule, evidence threshold, route trigger, or decision salience. Restore the distinct content at its correct owner.
2. **Scope/materiality laundering test:** attempt to make a representation pass by shrinking declared scope or labeling a globally required doctrine non-material because it is cold for the current task. Reject that representation.
3. **Priority-inversion test:** make the highest-consequence item prominent, then check whether a lower-salience but mandatory active constraint still survives through closure. Attention weighting must change prominence, not acceptance semantics.
4. **False-compaction test:** find a refactor that preserves paragraphs but merely moves links, flattens routing into larger entrypoints, substitutes stale summaries, creates a parallel routing registry, or leaves normal context unnecessarily dense. It does not satisfy 6.2.

Raise Serious Challenge only if accepted Protocol 6.1 authority itself appears materially false, contradictory, inadequate, or impossible to preserve coherently. None is identified in this workplan review.

## 8. Active implementation handoff

**WORKPLAN CLOSURE REVIEW: PASS AFTER REPAIR.** This workplan remains active cycle authority and authorizes Protocol 6.2 implementation on `ssdp-6.2-lossless-representation`. Protocol 6.2 itself is **not** accepted-current doctrine until Stage F/G qualification, independent candidate Review, recovery mapping, generated-artifact reconciliation, and closeout pass.

Implementation must treat as one contract: the complete 6.1/historical preservation baseline; governed-scope and decision-local materiality rules; finite durable/generative representation census; no-loss/no-supersession/salience prerequisites; minimal universal kernel; canonical owners; bounded hierarchical activation without a parallel routing authority; validity-scoped context reuse; hot/cold reachability; compact historical proof path; nomenclature migration; immutable bootstrap/candidate/recovery sequencing; current/generated/profile/package surfaces; static-versus-live claim discipline; and Protocol 7/main cutover boundaries.

Intended end state:

```text
thorough and sophisticated semantics
+ zero material information loss
+ governed scope that cannot be narrowed for convenience
+ one detailed owner per generic rule
+ terse precise local representations
+ minimal universal hot kernel
+ bounded explicit decision-driven routing
+ visible cold-path reachability
+ validity-scoped context reuse
+ importance-weighted attention without acceptance loss
+ history recoverable without routine history replay
+ minimum justified cognitive/context cost
```

Protocol 6.2 succeeds only if the same or stronger SSDP becomes easier for an agent or human to understand and execute correctly—not merely shorter.