---
kind: protocol-doctrine-workplan
workplan_id: SSDP-6.5-IMPORTANCE-WEIGHTED-ATTENTION-AND-PROPORTIONAL-RIGOR
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: p19-review-ready
branch: ssdp-6.5-frontier-model-re-evaluation
accepted_control: 55c085261eb827e3047637d045a8e6917ea6b962
superseded_review_ready_candidate: a2e5f01e258f249f74d1eda74b883efb98fd7d59
serious_challenge: active-against-current-doctrine
workplan_review: pass-after-third-adversarial-review
workplan_review_date: 2026-09-25
created_date: 2026-09-25
---

# Protocol 6.5 — Importance-Weighted Attention and Proportional Rigor

## 1. Disposition

**D3/protocol-doctrine reopen — P19 implementation complete and fresh-Review ready.**

P18 `a2e5f01e258f249f74d1eda74b883efb98fd7d59` remains immutable mechanically qualified historical evidence.
Its planned independent Review is suspended because P18 repaired the release-state defect B65-P17-1 but did not address
the broader resource-allocation defect identified by the stakeholder.

This file is the **single current implementation contract** for that reopen. Prior review chronology remains Git/history
evidence and is not appended as authority.

No ratification, publication, recovery, accepted-current cutover, PR #33 merge, or Protocol 7 D3/D4 mutation is
authorized by this workplan.

Design-review disposition: **PASS after three adversarial pre-implementation passes.** Further D3 review should be
driven by a concrete counterexample or materially changed premise, not amendment accumulation.

## 2. Serious Challenge and diagnosis

Accepted 6.4/current pre-repair 6.5 doctrine already contains the right ingredients:

- engineering fitness before simplicity before development economy;
- importance-weighted attention;
- cheapest sufficiently strong evidence;
- first clean local defect remains local;
- stop search when further work has lower expected engineering value;
- conditional history/evidence activation;
- simplification before repeated additive repair.

The abstraction is inadequate because those rules are not operationally connected. An agent can still treat every
uncertainty, fixture, evidence binding, and edge case as deserving comparable scrutiny, allowing local rigor to consume
resources irrationally and slow the actual governed outcome.

Recent evidence makes the failure concrete:

- in the mdstats doctor episode, work drifted toward downstream/process activity while the real blocking outcome was
  still the doctor gate, and local fixture mechanics attracted disproportionate analysis;
- in the P16-P18 loop, important release-state invariants justified exact reasoning, but routine diagnostic and fixture
  subproblems inherited the surrounding release campaign's scrutiny and contributed to repeated candidate/review
  cycles.

Historical Protocol 5.4, 5.12, and 5.14 already define development economy, convergence economy, and active simplicity.
The missing strengthening is an explicit **importance -> attention -> evidence-cost** decision discipline.

### Project-memory basis

Project history is activated because this is mature doctrine rework:

```yaml
accepted_project_state: 55c085261eb827e3047637d045a8e6917ea6b962
accepted_pem: hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:PROJECT-ENGINEERING-MEMORY.md
candidate_overlay_semantic_candidate: a2e5f01e258f249f74d1eda74b883efb98fd7d59
```

Bounded HAS:

- `FF-001` APPLICABLE — exact immutable release/publication identity remains genuinely high consequence;
- `PC-001` APPLICABLE — prior-version profiles/resources remain frozen preservation obligations;
- `DS-001` APPLICABLE — fixture/synthetic evidence is bounded by what its oracle discriminates;
- `SP-002` APPLICABLE — exact-ref self-reference-safe release publication remains a demonstrated release mechanism;
- `SP-001` NOT_APPLICABLE — source-route regeneration is not a governing mechanism for this redesign.

PEM supplies hypotheses/preservation cues only; current D1-D4/project/external owners remain authoritative.

## 3. Governing doctrine

Preserve the feasibility condition:

```text
every concretization satisfies all applicable governing authority and directly governed constraints
```

Then allocate finite development resources as:

```text
protect mandatory governed outcomes and unacceptable-risk constraints
> bound consequence and decision-relevant uncertainty
> use the cheapest sufficiently strong applicable evidence/action
> choose the simplest sufficient solution
> minimize total human/model/token/tool/compute/I/O/wall-time and opportunity cost
```

This is a decision discipline, not a scalar score.

### 3.1 Obligation is orthogonal to importance

Classify applicability before priority:

- **MANDATORY/APPLICABLE** — required by current authority, external contract, safety/security policy, or project
  acceptance. It remains mandatory regardless of salience.
- **DISCRETIONARY** — not required for the governed outcome and may be estimated, deferred, omitted, or handled
  opportunistically.

Priority may reorder mandatory work within a cycle but cannot starve it past its owning acceptance boundary. A deferred
mandatory item remains visibly open and prevents PASS unless the real owner explicitly supports provisional/risk-
accepted continuation. Priority classification cannot create such an override.

### 3.2 Importance asks consequence

Before broad analysis, new machinery, historical intake, statistical qualification, multi-route evidence, or repeated
Review, ask:

> **If we are wrong about this issue, what materially bad outcome can actually occur?**

Use qualitative dimensions only:

- consequence;
- scope/exposure;
- reversibility/irreversibility;
- authority proximity;
- decision sensitivity;
- recurrence/systemic signal;
- opportunity cost.

Default classes:

- **CRITICAL** — plausible wrongness materially affects scientific conclusions, safety/security, durable data,
  accepted authority, public release/recovery identity, or another high-consequence irreversible outcome.
- **MATERIAL** — plausible wrongness affects a primary capability/common path, reproducibility/recovery, frozen
  architecture, major compatibility/resource/performance requirement, or broad correctness.
- **ROUTINE** — bounded, local, reversible wrongness with no plausible higher-level semantic effect.
- **INCIDENTAL** — cosmetic/diagnostic/harness/presentation/optional-cleanup issues with little governed consequence.

Do not require numeric scoring.

If importance is uncertain, do not optimistically downgrade it. Use the cheapest action that can bound consequence,
scope, or decision sensitivity. Maintain only the provisional higher attention justified by the unresolved dimension,
then de-escalate when evidence bounds it. Unknown impact is not evidence of low impact.

A child problem inherits parent importance only when a credible causal path connects child wrongness to the parent
outcome. High-stakes projects do not make every internal detail high-stakes.

### 3.3 Importance is not next-action priority

Importance asks the cost of being wrong. Next-action priority asks where the next unit of engineering effort creates the
most governed value.

Choose the next action qualitatively from:

- mandatory dependency/gate status;
- unresolved decision sensitivity and unblocking value;
- real critical-path/deadline relevance;
- expected information or repair value;
- reversibility/failure cost;
- effort/opportunity cost.

Do not optimize only for cheap actions: an expensive necessary critical-path action can outrank many cheap peripheral
tasks. Conversely, a CRITICAL issue already settled by strong applicable evidence should stop consuming attention.

Importance/rigor labels are coordination metadata, not D1-D4 authority or acceptance thresholds. Reuse a still-
applicable prior label as a working hypothesis to avoid rediscovery, but revise it freely when consequence, scope,
evidence, or dependencies change.

## 4. Attention modes and stopping

Choose the least expensive mode plausibly capable of resolving the governed decision.

### DEEP

Use when consequence combines with material unresolved uncertainty, irreversibility, adversarial exposure, or a fixed
external evidence floor. It may include independent reconstruction, multiple evidence routes, adversarial holdouts,
statistical/convergence/conditioning studies, production qualification, or composed D4->D1 closure.

### STANDARD

Use focused owner analysis, one or a few strong discriminating oracles, affected regression/integration, and bounded
counterfactual reasoning.

### LIGHT

Use direct owning-layer repair, bounded engineering judgment, focused checking/regression, and the ordinary final
repository gate. Estimates/approximations are permitted only when their uncertainty cannot plausibly alter a material
decision.

### DEFER / OMIT

Use only for non-mandatory low-consequence work whose expected value is below the work it displaces. Record it only
when future discovery value is material.

Known material failures, governing-contract violations, safety/security hazards, or scientific uncertainties capable
of changing the conclusion cannot be omitted under this rule.

### Escalate, de-escalate, stop

- escalate only when a concrete uncertainty, counterexample, recurrence signal, or external requirement makes stronger
  scrutiny decision-relevant;
- de-escalate when that uncertainty is bounded;
- prefer a cheap reversible repair/experiment/discriminating test over prolonged analysis when it settles the same
  decision without weakening authority;
- stop when remaining uncertainty cannot plausibly change the governed decision, or when a cheaper reversible action
  can establish the same result;
- do not spend resources merely to convert sufficient confidence into psychological certainty.

If a supposedly LIGHT/ROUTINE issue starts consuming materially more reasoning, test cycles, candidate churn, or
machinery than its consequence warrants, stop at the next safe boundary. Either evidence revealed a genuinely more
important shared problem, or the method should be simplified/deferred/omitted where allowed. Sunk cost is not a reason
to continue.

Repeated rediscovery of a deferred issue is itself evidence: when cumulative interruption/workaround cost becomes
material, reassess, fix the shared cause or admit a bounded PEM lesson when justified. Do not create a general deferred-
issue ledger merely for compliance.

## 5. Evidence, fixtures, and candidate identity

### 5.1 Evidence proportionality

Evidence exists to support or change a decision, not because another evidence artifact exists.

```text
claim consequence + unresolved uncertainty + irreversibility
    -> required confidence
    -> cheapest sufficiently strong applicable evidence
```

**Applicability remains a feasibility condition.** Priority cannot make stale, wrong-subject, wrong-regime,
wrong-parameter, invalid-oracle, or otherwise inapplicable evidence current.

Stop evidence recursion once the material claim and the integrity of its evidence route are sufficiently established
for the consequence at stake. Add another evidence-binding layer only when a concrete failure/adversary model makes it
capable of changing acceptance.

Exact immutable provenance remains justified for high-consequence release/authority claims. A routine local test does
not inherit that machinery.

False-pass and false-reject cost may be asymmetric, but an external/regulatory evidence floor cannot be changed by
local priority judgment.

### 5.2 Fixtures and tests are instruments

On fixture/test failure:

1. identify the protected owner claim;
2. ask whether the fixture still represents that claim;
3. classify fixture wrongness separately from product wrongness;
4. use the cheapest discriminating check that separates production from oracle failure;
5. repair the fixture locally when stale;
6. never expand production architecture merely to satisfy low-importance harness machinery.

A stale fixture does not justify deep product investigation after the owner claim is independently established.

### 5.3 Evidence-only correction versus semantic mutation

Tests, fixtures, qualification scripts, review records, lifecycle bindings, and diagnostic workflow instrumentation are
evidence/coordination surfaces unless they themselves define accepted D4 semantics.

If a correction leaves the immutable D1-D4/product semantic subject unchanged:

- repair/remap the evidence at its owner;
- requalify the **same semantic candidate** when the lifecycle can represent that honestly;
- bind the qualification to the exact immutable semantic-subject ref, exact evidence-realization descendant ref, and
  exact external workflow/run identity when execution occurs outside that commit;
- inspect the intervening delta sufficiently to establish no governed semantic source/product/public contract changed;
- do not mint a replacement semantic candidate solely for an evidence-instrument correction;
- do not repeat unaffected independent semantic Review merely to replay unchanged semantics.

If governed semantic source, product behavior, or accepted contract changed, the same-candidate route is invalid: freeze
a replacement semantic candidate.

If corrected evidence invalidates a material premise of a prior Review, rerun the affected Review claim against the same
semantic subject, or repeat full Review only when independence/applicability was materially compromised.

Use existing release/workflow identities and compact qualification metadata; do not create a second candidate registry
or evidence state plane.

## 6. Scientific and numerical proportionality

D1/D2 rigor scales with **decision sensitivity**, not merely with the presence of numbers.

Use deeper scientific/numerical treatment when unresolved uncertainty can change a scientific conclusion/ranking,
validity/acceptance, or when the method is near a validity/stability/convergence boundary, material
conditioning/stochastic/bias/precision/discretization uncertainty exists, or materially plausible methods disagree.

Use lightweight treatment when the issue is demonstrably inside an accepted error/equivalence envelope, far from a
decision boundary, cheaply resolved by an exact/manufactured/reference case, or local/reversible with no plausible
effect on the scientific observable.

Never widen a tolerance solely because a test failed. Do not launch a research-grade statistical campaign merely
because a floating-point tolerance exists.

A public scientific result merits DEEP numerical/statistical treatment only when unresolved uncertainty can materially
affect interpretation, validity, or acceptance.

## 7. Workflow and Review

### 7.1 Stay attached to the real blocker

At each material stage:

```text
highest-value unresolved governed outcome
    -> highest-value affordable discriminating/repair action
    -> sufficient confidence
    -> proceed
```

Do not advance into dependent stages merely to accumulate evidence.

If the active blocker genuinely waits on unavailable external input, service, hardware, approval, or human decision,
independent useful work may proceed when it does not assume the blocker passed and will not invalidate later evidence.
Keep the blocker explicitly unresolved; parallel progress is not acceptance.

For a doctor -> prepare -> production pipeline, a failing doctor remains the active gate until repaired or shown to be
a stale/invalid gate and corrected by its owner.

### 7.2 Review proportionality

Independent Review still reconstructs current authority, candidate behavior, evidence applicability, and consequence
independently. Implementer priority labels are hypotheses, not authority.

A reviewer should:

- independently reconstruct finding consequence;
- inspect cheap sibling variants far enough to characterize a material family;
- stop when additional sibling search becomes implementation-like, expensive, or duplicative;
- distinguish semantic/product failure from evidence-instrument failure;
- route evidence-only defects to targeted repair/requalification when candidate semantics are unchanged;
- issue NO-PASS for genuine semantic/conformance blockers or mandatory acceptance deficiencies, not merely because a
  further low-value imperfection can be imagined;
- reopen upstream doctrine only when the abstraction itself is materially inadequate.

Priority changes investigation effort, **not the pass threshold** for an applicable requirement. Review sufficiency is
not proof of zero conceivable defects.

## 8. Workplan and handoff representation

Substantial workplans should include a compact attention map:

```markdown
## Importance and attention allocation

### Highest-value outcomes
### Mandatory acceptance floors
### Critical/material uncertainties
### Routine/incidental surfaces
### Rigor plan — DEEP / STANDARD / LIGHT / DEFER-OMIT
### Escalation / de-escalation / stop triggers
```

This is not a ledger. Do not require per-issue scores, token budgets, or exhaustive classifications. Small/local work
does not require the section.

When a material priority judgment changes scope/evidence depth, defers a nontrivial issue, or permits bounded
approximation/omission, preserve only the smallest useful rationale in the workplan/handoff:

- consequence;
- mandatory vs discretionary status;
- decisive uncertainty/evidence;
- chosen rigor mode;
- escalation/stop trigger.

This keeps a consequential resource-allocation decision reviewable without creating permanent process state.

## 9. Required implementation surfaces

Reconcile through existing canonical owners; do not add a parallel control plane.

1. **Universal kernel — `abstraction-and-concretization.md`**
   - make importance-weighted attention operational;
   - keep authority/applicability as feasibility conditions;
   - permit bounded judgment/estimate/deferral/omission only where non-mandatory and consequence-safe;
   - apply stop-search economy before evidence proliferation.

2. **Convergence — `convergence-and-cycle-economy.md`**
   - classify importance before family expansion;
   - separate problem importance from next-action priority;
   - add escalation/de-escalation, sunk-cost, cumulative rediscovery, and review-saturation rules;
   - ensure repeated low-value findings do not force high-rigor loops unless they reveal a material family.

3. **Workflow — `workflow-and-workplans.md`**
   - add the compact attention map for substantial work only;
   - preserve mandatory closure floors, productive work around unavailable external blockers, and lightweight local
     routes;
   - keep priority labels non-authoritative.

4. **Evidence — `evidence-evolution-and-dependencies.md`**
   - preserve applicability as a feasibility condition;
   - stop recursive evidence inflation;
   - support same-semantic-candidate targeted requalification with separate semantic-subject and realization identity.

5. **Testing — `testing-and-validation.md`**
   - distinguish owner failure, stale/incorrect evidence instrument, and routine harness defect;
   - generalize cheapest-sufficient evidence into proportional rigor without weakening required D4 affected
     regression/integration.

6. **D1/D2 references and roles**
   - scale scientific/statistical/numerical scrutiny to decision sensitivity;
   - retain deep treatment where uncertainty can alter scientific meaning;
   - keep trivial in-envelope numerical details lightweight.

7. **D3/D4 roles**
   - require bounded importance judgment before broadening scope;
   - fix routine local defects directly;
   - reserve architecture/doctrine reopening for materially consequential evidence.

8. **Implementation workplan template**
   - add the optional substantial-work attention map;
   - do not impose it on small/local work.

9. **Release/documentation closeout**
   - implement Section 10 below.

Do not create a new importance service, risk database, evidence registry, or lifecycle role.

## 10. Protocol release documentation closeout

Every protocol successor cycle performs documentation closeout **after semantic implementation stabilizes and before
the replacement immutable semantic candidate is frozen**.

### Root README

Recompile/review root `README.md` as the current user-facing guide, not normative authority or mutable release state.
It should:

- explain SSDP's purpose and core philosophy quickly;
- explain D1->D4 abstraction/concretization and why it matters;
- teach skill selection, the development cycle, common workflows, and simplicity/economy doctrine;
- summarize current major capabilities only enough to orient use;
- use practical examples where they clarify decisions;
- use clear, direct, newcomer-comprehensible, progressively disclosed prose;
- remove redundancy, vague abstraction, needless ceremony, amendment chronology, and jargon accumulation;
- keep accepted/candidate/public/recovery identities in `PROTOCOL-RELEASE-STATE.yaml`;
- route capability history to `CHANGELOG.md`;
- route detailed rationale/release chronology to `history/SEMANTIC_EVOLUTION.md`.

Apply the well-written/Lossless Representation principles. Preserve already-clear prose instead of rewriting for churn.
Stop when the guide is accurate, current, newcomer-comprehensible, navigable, and free of material redundancy or
misleading historical residue.

### CHANGELOG and source README

Update root `CHANGELOG.md` for every protocol version with concise user-facing capabilities added, strengthened,
replaced, or deliberately retired. Do not turn it into a candidate-SHA/review-iteration/release-state ledger.

Keep `source/README.md` a concise source/contributor map rather than a duplicate user guide.

### Persistence

Root `AGENTS.md` permanently carries the closeout obligation.

Add one bounded assertion to the **existing** repository acceptance path:

- `source/PROTOCOL_VERSION` has a corresponding root CHANGELOG capability entry;
- root README retains routes to `CHANGELOG.md` and `PROTOCOL-RELEASE-STATE.yaml`.

The check tests only stable presence/routing invariants. It must not score prose, require feature keywords, parse
doctrine meaning, or force paragraph churn. Semantic writing quality remains a human/agent review responsibility.

## 11. Required qualification counterfactuals

Qualification tests decisions, not wording. Cover at least:

1. doctor-stage fixture failure stays on the doctor outcome rather than drifting to dependent prepare work;
2. core scientific inference with conclusion-sensitive uncertainty receives DEEP treatment;
3. trivial numerical tolerance inside an accepted D2 envelope uses a focused cheap oracle;
4. the same tolerance near a decision boundary escalates D2 scrutiny;
5. release accepted/public/recovery identity retains exact-ref/fail-closed evidence;
6. stale release fixture is repaired locally without promoting the fixture into architecture;
7. valid evidence route stops instead of creating recursive evidence bindings;
8. low-consequence diagnostic child does not inherit a high-stakes parent's priority without causal linkage;
9. non-mandatory INCIDENTAL work may be omitted without being mislabeled as PASS evidence;
10. repeated ROUTINE defects revealing one material shared owner escalate to family-level analysis;
11. fixed safety/security/external evidence floors cannot be downgraded;
12. Review stops low-value sibling enumeration after the material family is characterized;
13. uncertain importance triggers the cheapest bounding action, then escalation/de-escalation;
14. Review can overturn an implementer's incorrect priority classification in either direction;
15. stale/wrong-regime evidence cannot be cheapened into applicability;
16. same semantic candidate + corrected fixture binds semantic subject, realization descendant, and run separately and
    verifies the intervening delta is non-semantic;
17. attention overrun/sunk-cost continuation triggers reassessment rather than more low-value machinery;
18. protocol version without CHANGELOG entry or README release-state/changelog routes fails the bounded docs check;
19. mandatory low-salience work may be scheduled late but cannot survive its owning PASS boundary without an explicit
    owner-authorized provisional/risk state;
20. unavailable hardware/approval may permit independent useful work without pretending a dependent gate passed;
21. prior priority labels may be reused as coordination state and revised without D3 reopening;
22. repeated deferred rediscovery whose cumulative cost becomes material triggers reassessment/shared repair or bounded
    learning rather than endless deferral.

## 12. Acceptance

Implementation is complete only when the assembled candidate demonstrates that agents can distinguish:

- important governed problem from nearby low-value detail;
- mandatory obligation from discretionary work;
- consequence importance from next-action priority;
- unknown importance from genuinely low importance;
- need for proof from desire for certainty;
- applicable evidence from stale evidence that is merely cheap to reuse;
- owner failure from fixture/evidence-instrument failure;
- scientific uncertainty requiring deep analysis from routine in-envelope numerical handling;
- semantic mutation from evidence-only requalification;
- productive work around an external blocker from false dependent-stage advancement;
- legitimate omission from repeated rediscovery whose cumulative cost is material.

Required repository qualification:

- focused semantic counterfactuals above;
- inherited protocol regression;
- assembled source/package/profile/Core acceptance;
- frozen prior-version preservation;
- same-candidate evidence-only requalification discrimination;
- README/CHANGELOG semantic closeout plus the bounded objective documentation assertion.

No claim of improved real-world development efficiency should be made solely from static contract tests; actual outcome
evidence remains separate.

## 13. Non-goals

Do not introduce:

- numeric importance/risk scoring;
- mandatory token accounting or fixed time/tool budgets;
- a new lifecycle/approval role or separate gate;
- an importance reviewer;
- persistent issue-priority/deferred-work ledgers;
- a second evidence/candidate registry;
- recursively self-validating evidence graphs;
- blanket permission to ignore failing tests or weaken tolerances;
- universal statistical qualification for scientific work;
- a prose-quality/doctrine parser;
- model-specific behavior.

Bounded assertions inside the existing acceptance path are allowed when they protect stable objective invariants.

## 14. Implementation sequence

1. Reconcile universal kernel, convergence, workflow, evidence, and testing owners.
2. Reconcile D1/D2 proportional scientific/numerical scrutiny and D3/D4 local-repair behavior.
3. Update role entrypoints and the implementation-workplan template without burdening small work.
4. Reconcile evidence-only correction and same-semantic-candidate targeted requalification.
5. Add/refactor bounded decision counterfactuals; remove/relax superseded uniform-rigor policy oracles rather than
   layering another large test family.
6. Regenerate canonical distributions/profiles/snapshots and preserve frozen prior-version resources.
7. After semantic stabilization, perform README/CHANGELOG/source-README closeout and add/run the bounded documentation
   assertion in the existing repository acceptance path.
8. Stabilization: inspect specifically for new bureaucracy, duplicated doctrine, accidental weakening of high-
   consequence requirements, or priority labels promoted into authority.
9. Run final assembled acceptance and freeze the replacement Protocol 6.5 semantic candidate.
10. Return to fresh independent assembled-candidate Review.

## 15. Implementation authority

### Frozen

- Governing authority/applicability/correctness remain feasibility conditions.
- Mandatory obligations and fixed safety/security/external floors cannot be waived by priority.
- Importance is consequence-based and decision-local; unknown impact is not low impact.
- Importance and action priority are distinct.
- Priority/rigor labels are coordination metadata, not authority or acceptance thresholds.
- Subproblems do not inherit parent importance without causal linkage.
- Evidence intensity scales with consequence, unresolved uncertainty, irreversibility, and external floors.
- Evidence applicability remains mandatory.
- Cheapest sufficiently strong applicable evidence/action is preferred.
- Bounded estimate/deferral/omission is allowed only for consequence-safe non-mandatory uncertainty.
- Full scientific/statistical qualification is reserved for decision-relevant uncertainty.
- Development economy includes human/model/token/tool/compute/I/O/wall time, critical-path opportunity cost, and
  cumulative rediscovery cost where material.
- Evidence-only correction does not automatically mint a new semantic candidate; same-candidate requalification binds
  semantic subject and evidence realization separately and verifies the intervening delta is non-semantic.
- Every protocol successor performs README/CHANGELOG closeout before semantic-candidate freeze, with persistent
  `AGENTS.md` guidance and the bounded objective docs assertion.
- No new lifecycle role, separate approval gate, registry, score engine, telemetry bureaucracy, or prose-quality parser.

### Delegated

- Exact terminology of importance/rigor classes.
- Exact wording/section placement in current canonical owners.
- Exact counterfactual test organization.
- Exact representation of the compact substantial-work attention map.
- Exact existing test/check location for the documentation assertion.
- Exact context/routing reductions.

### Reopen D3 only on evidence

Reopen if implementation shows that:

- qualitative importance cannot produce sufficiently consistent material decisions;
- proportional rigor cannot preserve a material accepted scientific/safety/release guarantee;
- a fixed external domain requires a stronger uniform evidence floor;
- low-priority deferral can silently hide material failures despite the safeguards;
- the attention mechanism costs more process than it removes;
- safe same-candidate evidence-only requalification requires a new state plane or materially different release
  architecture;
- the bounded documentation assertion cannot be implemented without becoming a semantic/prose parser; or
- a mandatory Protocol 6.4 obligation/authority must actually be weakened, making the intended backward-compatible
  6.5 minor posture false.

Do not reopen because an old fixture/test encodes superseded uniform-rigor behavior; reconcile it against this current
contract.


## 16. P19 implementation freeze

The reviewed proportional-rigor implementation is frozen as immutable semantic candidate:

`P19 = b38f2525677888956c4802afd758c98c65b79f1c`

Exact-P19 ordinary workflow `36195532806` passed both complete jobs, including inherited regression, release-state/PEM
validation, package build/independent validation, committed distribution parity, documentation persistence,
whitespace, Protocol snapshot parity, and Orchestrator Core.

P19 contains the completed documentation closeout and regenerated generic distributions. The temporary one-shot
distribution-regeneration helper is absent from the P19 tree; it was implementation tooling only.

This descendant binds exact P19 in the sole mutable release-state owner with Review `NOT_RUN`, stakeholder
ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, accepted-current Protocol 6.4, and Protocol 7
D3/D4 unchanged. Binding workflow qualification is required before independent Review is authorized.


## 17. P19 binding qualification — fresh Review ready

Exact P19 `b38f2525677888956c4802afd758c98c65b79f1c` passed workflow `36195532806`.

Binding descendant `d4bfb9032612395ed3d5dbff462acb86ed538944` passed workflow `36195685076` with Review `NOT_RUN`, ratification
`NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, accepted-current Protocol 6.4, and Protocol 7 D3/D4
unchanged.

The implementation stage has no known surviving blocker. The durable independent-Review handoff now targets exact P19.
This implementation context must not self-issue that Review.
