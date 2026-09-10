---
kind: abstraction-concretization-change-plan
workplan_id: SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT
protocol_version: 6.1.0
target_protocol_version: 6.2.0
status: proposed
created_date: 2026-09-10
reviewed_date: 2026-09-10
self_review_status: pass-after-repair
active_serious_challenge: none
parent_semantic_baseline: cec29671b9db59d20124a6e2ce99725ed60b8f0a
parent_protocol_61_recovery: 802e75af261efb4f70d71284d860613a2197b639
---

# SSDP 6.2 Lossless Representation and Progressive-Disclosure Refinement

## Background and terminology

The Scientific Software Development Protocol (SSDP) is intentionally thorough. Protocol 6.2 addresses how that sophistication is represented: semantically complete doctrine can still become hard to execute when rules are repeatedly restated, activation paths become deep, historical revisions remain in the normal reasoning path, or routine detail competes with governing decisions.

For this plan:

- **representation** — an SSDP-controlled human/agent communication surface: skills, references, prompts, workplans, handoffs, specifications, method/architecture documents, reviews, qualification/evidence summaries, dependency/evolution records, guides, runbooks, and resumable state;
- **lossless representation** — every material semantic element required by the representation's declared scope remains recoverable, correctly interpretable, and sufficiently salient to support the intended decision;
- **hot path** — information normally loaded/presented to make the current decision;
- **cold path** — recoverable detail loaded only when a visible condition makes it relevant;
- **progressive disclosure** — adding doctrine to active context only when the current semantic question triggers it;
- **activation dependency** — an explicit read prerequisite for a named decision; it is distinct from ordinary hyperlinks, semantic dependencies, evidence execution dependencies, and package transport dependencies;
- **attention balance** — prominence/context allocation proportional to consequence, uncertainty, risk, and immediate decision relevance.

The objective is not minimum bytes, paragraphs, or files. Over-compression, excessive abbreviations, fragmentation, hidden prerequisites, or long reference chains may increase cognitive cost. The target is the minimum complete, precise, readily interpretable representation.

## 1. Target outcome, authority, and scope

Protocol 6.2 SHALL preserve all accepted Protocol 6.1 semantics and still-valid historical capabilities while making current representation terser, more precise, shallower to route, less repetitive, importance-weighted, and cheaper in active context.

A representative substantial D3 Review under 6.1 can load roughly 112 kB of protocol Markdown before task-specific workplan/code/tests/evidence, versus roughly 80 kB for the analogous 6.0 core. These counts are sensors, not thresholds: physical package size is not the concern; repeated doctrine, salience dilution, unnecessary activation, and synchronization debt are.

Governing preservation baseline:

- final Protocol 6.1 closeout: `cec29671b9db59d20124a6e2ce99725ed60b8f0a`;
- accepted 6.1 recovery: `802e75af261efb4f70d71284d860613a2197b639`;
- immutable 6.0 recovery: `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`;
- immutable 5.16 recovery: `e151daaf5c8eebb351a85cfed86170fda80fb5e3`;
- the complete 95-case Protocol 6.1 behavioral qualification plus applicable static/package/orchestrator tests;
- current 6.1 canonical owners and `history/SEMANTIC_EVOLUTION.md`/archived workplans where they preserve material rationale or subtle inherited behavior.

This is a protocol-wide representation-doctrine strengthening with D3/D4 routing/document/package/profile consequences. It does not alter scientific D1 or numerical D2 meaning merely because D1/D2 artifacts must obey the representation rule. If implementation discovers an actual D1/D2 semantic conflict, route it to that owner rather than resolving it editorially.

The rule governs SSDP-authored/controlled representations. It does not authorize rewriting higher-priority user, platform/system, safety, legal/regulatory, external API, or other governed source authority. When exact source wording itself is material, retain or directly reference the exact text rather than paraphrasing it into a weaker contract.

Non-goals: reduce ZIP size for its own sake; weaken doctrine to shorten prose; impose arbitrary token/paragraph quotas; create a universal graph/database/context manager/new approval role; rewrite frozen 5.16/6.0/6.1 artifacts; implement Protocol 7 control machinery; or merge/cut over to `main` without separate authorization.

## 2. Protocol 6.2 Lossless Representation Rule

### 2.1 Admissibility first

A representation `R` of governed information `S` is admissible only if a competent intended reader/agent can recover and correctly interpret every material semantic element required by the declared scope without hidden chat, unavailable history, or unstated prerequisites.

Losslessness includes not only fact retention but also:

- authority/ownership and lifecycle state;
- governing invariants, exceptions, constraints, non-goals, uncertainty, evidence qualification, dependencies, and reopen conditions;
- discoverability of conditionally relevant cold-path information;
- decision-critical salience where burying the information could change action or closure.

A historical improvement may disappear as separate current prose only when an equal-or-stronger generalized current rule preserves its behavior and material historical rationale remains recoverable.

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
2. **Generalize rather than accumulate.** Strengthen the current rule into one coherent form; move chronology/supersession rationale to history rather than retaining amendment layers in the hot path.
3. **Use progressive disclosure.** Potential relevance to a broad task class does not justify unconditional loading.
4. **Keep activation explicit and shallow.** Ordinary links/package membership do not create read obligations. Each role/specialist `SKILL.md` owns its internal reference-activation rules; orchestration selects the role and common execution contract but does not independently duplicate the role's reference-routing logic. Shared references may link to other references for navigation, but must not create hidden transitive activation requirements.
5. **Make cold paths visibly reachable.** If information can materially affect a decision, the hot path must expose the condition and route by which it becomes active. Cold must not mean undiscoverable.
6. **Reuse established context.** Do not reload unchanged authority solely to restate it; reread when exact wording is newly material or later evidence plausibly invalidates the established interpretation.
7. **Balance attention by consequence.** Serious Challenges, safety/governing conflicts, current authority, blockers, high-impact uncertainty, and required decisions precede routine mechanics and historical provenance.
8. **Minimize total inferential cost.** Do not replace one clear local statement with a long reference chain, and do not fragment one coherent concept merely to reduce file length. Prefer section-targeted reads when tooling supports them.
9. **Preserve evidence visibility.** Summaries may keep raw detail cold, but must not hide failures, warnings, contradictory admissible evidence, unavailable required checks, uncertainty, or provenance needed to interpret the claim.
10. **Do not resolve semantic disagreement through deduplication.** If apparently duplicate current texts differ materially in meaning, scope, authority, or threshold, stop editorial compaction and route the conflict to the owning authority; use Serious Challenge when the accepted authority itself may be defective.

Derived summaries/hand-offs are representations, not replacement authority. If a compact derivative conflicts with its canonical owner, the owner governs and the derivative is defective.

## 3. Target representation architecture

### 3.1 Universal kernel and terminology correction

Rename the current 6.2 kernel:

```text
source/shared/references/abstraction-and-realization.md
-> source/shared/references/abstraction-and-concretization.md
```

Add the Lossless Representation Rule there so no new universally mandatory reference is created. Update current 6.2 links, packages, tests, dependency views, prompts, top-level/current documentation, and generated resources. Frozen 5.16/6.0/6.1 content retains historical paths/terminology.

Also rename current `abstraction_realization_change_plan_template.md` to `abstraction_concretization_change_plan_template.md` unless a concrete supported current consumer contract requires the old path. Audit all current `realization` identifiers: use **concretization** for D1-D4 semantic descent and reserve **realization** for evidence execution. Do not add aliases/wrappers merely because Git history contains the old name.

### 3.2 Canonical owners

Preserve one detailed owner for each generic concern:

```text
universal authority/challenge/representation -> abstraction-and-concretization.md
workflow/handoff/stages                    -> workflow-and-workplans.md
evidence lifecycle/evolution/dependencies -> evidence-evolution-and-dependencies.md
testing/oracles/validation                 -> testing-and-validation.md
D1 formulation                             -> scientific-formulation.md
D2 numerical/algorithm method              -> numerical-algorithm-design.md
D3 architecture                            -> architecture-and-design.md
D4 specification                           -> specification-and-implementation.md
recurrence/simplification/cycle economy    -> convergence-and-cycle-economy.md
longitudinal health/stabilization           -> long-horizon-code-health.md
version selection/recovery                 -> protocol-versioning-and-compatibility.md
technical writing                          -> scientific-technical-writing.md
document authority/current-vs-history      -> documentation-maintenance.md
repository inspection/context economy      -> repository-intake.md
```

Owner normalization is not license to invent precedence. Use existing accepted ownership to decide where duplicate prose belongs. If ownership is genuinely ambiguous or current texts conflict materially, treat that as an authority issue, not an editorial choice.

### 3.3 Role and activation topology

Target route:

```text
orchestration / user task
  -> selected role SKILL.md
       -> universal kernel
       -> owning domain reference
       -> direct decision-conditional concern owner(s)
       -> direct conditional language/tool owner(s)
```

`SKILL.md` should primarily contain ownership/activation boundary, minimal standalone background, direct conditional routing, role-specific method/delta, and completion/stop semantics. It should not reteach complete evidence, Challenge, convergence, versioning, or testing doctrine.

A shared reference link is navigation, not activation. If a role decision needs both reference A and B, the role router should expose both conditions directly rather than relying on A to activate B. This makes runtime activation one-hop and inspectable even when package transport remains transitively self-contained.

### 3.4 Hot/cold path discipline

Current operational rules required for routine decisions remain hot. Historical lineage, supporting rationale, raw evidence detail, and specialized concern doctrine stay cold until a visible trigger fires. Every cold-path item capable of changing the decision must remain reachable in standalone supported execution—through the installed package or an explicit immutable compatible public-source route—not merely through repository archaeology.

Current truth must be reconstructable without replaying revision history. History explains why; current owners explain what is true.

## 4. Lossless preservation contract

### 4.1 Reviewable preservation map

Before semantic compaction, construct a bounded work-specific preservation map covering:

- every current 6.1 canonical owner and role/specialist obligation materially touched;
- all 95 qualified 6.1 behaviors;
- applicable route/package/language/tool/orchestrator tests;
- material historical guarantees from semantic evolution and archived workplans not already obvious from the 95 cases;
- frozen 5.16/6.0/6.1 identities and behavior.

The unit is a semantic obligation/capability family, not every paragraph. For each materially removed/merged/generalized rule, record its old owner/location, new owner/location, preservation rationale, and acceptance evidence.

This map is evidence/coordination, not parallel authority. It must be available to Implementation and independent Review. At closeout it may be retired after its decision-level conclusions are preserved in qualification/Review/evolution records and the current owners/tests make the mapping reconstructable; do not create a permanent universal traceability registry by default.

### 4.2 Compression proof obligation

Acceptable compaction includes: identical semantics moved to the canonical owner; narrower rules replaced by a demonstrably stronger general rule; generic prose removed from a secondary artifact while direct routing plus local consequence preserves behavior; or historical amendment prose moved cold while current generalized doctrine and history preserve capability/rationale.

No-Pass examples: deleting untested doctrine; replacing a precise exception with a vague principle; expecting common-sense inference for an omitted obligation; retaining vocabulary while losing behavior; changing an authority boundary/evidence threshold/failure condition during editorial compaction; or preserving every paragraph while only rearranging links and leaving the same unnecessary activation load.

Exact wording, equations, external contracts, immutable identifiers, or quoted source authority must remain exact when wording itself carries the governed meaning.

### 4.3 Frozen-version isolation

Do not rewrite historical 5.16, 6.0, or 6.1 source/profile/publication semantics. Current 6.2 should use clean 6.2 terminology and routing while resolving historical work through immutable version-specific authority.

## 5. Refinement targets from the 6.1 scan

- **Skills:** remove generic doctrinal restatement; make mandatory reads narrowly role-critical and other reads decision-triggered.
- **Testing vs evidence:** evidence lifecycle/applicability/common-mode semantics stay with the evidence owner; testing retains oracle integrity, numerical/architectural/D4 validation, regression/integration, proxy-proof, failure-injection, and qualification methods.
- **Convergence vs architecture/workflow/health:** convergence owns the generic recurrence/simplification rule; other owners retain only domain-specific consequences. Long-horizon health owns longitudinal sensing/stabilization rather than a parallel simplification doctrine.
- **Challenge:** the kernel owns the full Serious Challenge model; other artifacts keep only their threshold/routing consequence.
- **Documentation:** `scientific-technical-writing.md` owns exposition; `documentation-maintenance.md` owns document lifecycle/current-vs-history/source-chain semantics; `documentation-and-evidence.md` keeps engineering-document/evidence communication consequences. All inherit rather than restate the universal representation rule.
- **Handoffs/records:** remain snapshot-complete for task-specific governing information, but generic protocol doctrine is referenced. Lead with disposition, governing constraints/blockers/uncertainty, then evidence; keep closed chronology/raw detail cold unless decision-relevant.
- **Repository intake:** retain targeted inspection and context reuse as repository-specific consequences of the universal rule.
- **Workflow prompts:** keep one shared execution/authority/evidence/representation preamble and concise stage-specific inputs/actions/outputs/stops; role `SKILL.md`, not prompt duplication, owns subreference activation.
- **Versioning/history:** keep current version selection/recovery operationally compact; move detailed lineage cold while retaining exact immutable mappings and discoverable historical routes.
- **Dependency/package topology:** distinguish semantic, activation, evidence, source/generated, and transport relationships. Bounded transitive package closure may remain if it is still the simplest self-contained transport; package membership never implies active-context loading.

Do not mechanically deduplicate similar text: first determine whether it is the same semantic rule or a distinct domain consequence.

## 6. Implementation sequence

### Stage A — Baseline and preservation evidence

1. Freeze `cec29671...` as the 6.1 parent baseline.
2. Inventory current owners, direct/conditional activation routes, ordinary cross-links, package closure, generated/profile routes, and representative hot paths.
3. Build the bounded preservation map above and identify duplicate/near-duplicate doctrine, amendment-style current prose, hidden/transitive activation, and cold-path reachability risks.
4. Baseline representative tasks: local D4 repair; D3 workplan; independent D4 Review; D2 work; D1 work; documentation reconciliation; maintenance audit; release/package work; historical recovery/migration; closeout. Record required protocol files and why each activation edge exists. Token/byte/document counts are sensors only.

Stage A changes no accepted protocol semantics.

### Stage B — Kernel and nomenclature

1. Rename the current kernel and current abstraction/concretization template as specified.
2. Add the universal Lossless Representation Rule and reconcile current `realization` usage.
3. Update current source links/tests/dependency records without touching frozen releases.
4. Verify no required current consumer depends on a legacy path before deleting it; if such a contract exists, preserve the minimum explicit compatibility mechanism and document its retirement condition.

### Stage C — Owner normalization

1. Consolidate each generic doctrine at its accepted owner.
2. Replace secondary full restatements with local consequences and precise owner routes.
3. Resolve any discovered semantic/ownership conflict through the owning authority before deduplication.
4. Keep enough local background for standalone comprehension; do not split concepts merely to improve counts.
5. Reconcile `source/SEMANTIC_DEPENDENCIES.md` and current documentation with the resulting ownership model.

### Stage D — Progressive-disclosure routing and communication surfaces

1. Refactor all role/specialist `SKILL.md` files to compact direct routers plus role-specific method/completion semantics.
2. Make role `SKILL.md` the source of truth for role-internal reference activation; remove hidden activation directives from shared references or convert them to non-activating navigation.
3. Refactor workflow prompts to shared cross-stage contracts plus stage deltas; avoid duplicating internal skill routing.
4. Apply the representation rule to templates, handoffs, reviews/qualification/audit reporting, resumable state, and technical-writing guidance.
5. Ensure every material cold-path condition has a visible hot-path trigger and supported standalone retrieval path.

### Stage E — 6.2 profile, immutable public fallback, and packages

A Git commit cannot self-name. Avoid repeating the 6.1 recovery/bootstrap defect by staging identities explicitly:

1. Make the 6.2 canonical source/profile/package inputs internally coherent without claiming an unknown self SHA; retain profile schema v2 unless an actual machine-profile contract changes.
2. Create an immutable **6.2 public-source bootstrap commit** after the 6.2 role/reference/routing source needed for fallback is complete.
3. In a later **semantic-candidate commit**, publish that exact bootstrap SHA in current public-resolution prompts/versioning/portability surfaces. Apart from required generated descendants, this mapping step must not smuggle unrelated semantic changes.
4. Add/freeze `ssdp-protocol-6.2`; preserve `sdp-protocol-5.16`, `ssdp-protocol-6.0`, and `ssdp-protocol-6.1` byte/behavior semantics.
5. Rebuild all current distributions and snapshots from canonical source; validate package structure, link closure, source-to-generated parity, version identity, and closest supported consumer ingestion.
6. Test the no-local-compatible-skill / incompatible-default-branch case against the exact immutable 6.2 bootstrap. The repository default branch is never a version oracle.

### Stage F — Qualification and independent Review

1. Run complete affected repository/package/orchestrator regression.
2. Re-run the semantic capability of all 95 Protocol 6.1 scenarios against 6.2, preserving frozen-version semantics where cases intentionally target 5.16/6.0/6.1.
3. Add focused 6.2 cases for: lossless vs lossy compression; stronger generalization vs amendment accumulation; one owner + local delta; non-activating ordinary hyperlink; required conditional activation; established-context reuse; blocker/Serious-Challenge salience; cold historical recoverability; snapshot-complete compact handoff; exact-text preservation; authority-conflict non-editorial resolution; current renamed kernel vs frozen historical path; and immutable 6.2 public fallback under incompatible/default-branch conditions.
4. Compare 6.1 and 6.2 activation traces for the representative Stage-A tasks. Require materially cleaner unnecessary-context/repetition behavior, with every retained mandatory load justified; do not game numerical context metrics by hiding required information.
5. Perform an **independent** D3/protocol Review by a reviewer/context that did not author the candidate. It must review the preservation map, final owner topology, cold-path reachability, representative routing, generated/profile/package correctness, and qualification evidence.
6. No PASS if compaction makes any accepted behavior ambiguous, unavailable, less salient where salience affects correct action, or dependent on hidden context.

### Stage G — Recovery, mapping, closeout, and Protocol 7 reconciliation

1. After semantic candidate qualification and independent Review pass, choose an immutable 6.2 recovery commit that contains the accepted candidate and required decision evidence through ancestry.
2. Publish `6.2.0 -> <exact recovery SHA>` only in a later mapping commit; preserve the distinct public-source bootstrap identity. Regenerate any mapping-bearing generated/package outputs and rerun targeted recovery/parity checks.
3. Record material 6.2 semantic evolution; archive this workplan only after accepted rules reside in current canonical owners and evidence/impact closure is complete.
4. Keep Protocol 6.1 as accepted rollback/current baseline until 6.2 qualification, Review, recovery mapping, generated-artifact reconciliation, and lifecycle closeout all pass.
5. Reconcile the active Protocol 7 handoff explicitly after 6.2 acceptance. If Protocol 7 has not begun D4, it may adopt 6.2 representation doctrine through an explicit compatible handoff update. Do not silently rewrite Protocol 7 architecture semantics; any material D3 change remains subject to its existing deliberate architecture reopen.
6. Do not merge/cut over `main` without separate authorization.

## 7. Acceptance and falsification

### 7.1 Hard no-loss gates

Protocol 6.2 is No-Pass if any accepted 6.1 doctrine/still-valid historical capability becomes unrecoverable or behaves differently without explicit accepted semantic revision; a frozen historical artifact/profile is rewritten; a secondary artifact gains a hidden prerequisite; a cold-path condition is not discoverable; a current route depends on incidental Markdown/package topology; exact governing wording is weakened by paraphrase; deduplication resolves a real semantic conflict editorially; or representation becomes shorter but materially harder to interpret.

Before closure, every materially transformed obligation in the preservation map must be accounted for as preserved, deliberately superseded through accepted authority, or blocking. Green tests alone do not prove losslessness.

### 7.2 Representation-quality gates after no-loss passes

Independent Review must establish:

- one identifiable detailed current owner for each generic rule;
- justified local delta rather than parallel doctrine in secondary artifacts;
- direct, decision-triggered role activation with no hidden transitive reads;
- visible and supported hot-to-cold retrieval triggers;
- materially lower unnecessary/repeated context on representative routes without arbitrary quotas;
- current documents that explain present truth without requiring amendment replay;
- importance-weighted reporting with high-consequence state salient;
- snapshot-complete handoffs/reports without generic doctrine duplication;
- package transport correctness independent of runtime activation;
- consistent current abstraction/concretization terminology, with `realization` reserved for evidence execution outside frozen history.

### 7.3 Challenge Pass

Attempt both falsifications:

1. **Loss test:** identify apparently repetitive text whose removal actually loses an edge case, qualification, authority boundary, historical compatibility rule, evidence threshold, or decision salience. Restore the distinct content at its correct owner.
2. **False-compaction test:** identify a refactor that preserves all paragraphs but merely moves links while routing/context remains unnecessarily dense. It does not satisfy 6.2.

A Serious Challenge is raised only if accepted Protocol 6.1 authority itself appears materially false, contradictory, inadequate, or impossible to preserve coherently. None is currently identified.

## 8. Handoff state

This reviewed workplan remains **proposed cycle authority**, not accepted Protocol 6.2 doctrine. This self-review may repair the plan but does not substitute for the independent candidate Review required in Stage F.

Implementation must treat as one contract: the 6.1 preservation baseline; no-loss/salience prerequisites; canonical-owner and activation-source rules; hot/cold reachability; nomenclature migration; immutable bootstrap/candidate/recovery sequencing; affected current/generated/profile/package surfaces; qualification strategy; and Protocol 7/main cutover boundaries.

Intended end state:

```text
thorough and sophisticated semantics
+ zero material information loss
+ one detailed owner per generic rule
+ terse precise local representations
+ shallow explicit decision-driven activation
+ visible cold-path reachability
+ importance-weighted attention
+ history available without dominating current context
+ minimum justified cognitive/context cost
```

Protocol 6.2 succeeds only if the same or stronger SSDP becomes easier for an agent or human to understand and execute correctly—not merely shorter.