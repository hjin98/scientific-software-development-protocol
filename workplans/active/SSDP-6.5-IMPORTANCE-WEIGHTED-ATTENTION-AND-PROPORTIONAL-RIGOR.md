---
kind: protocol-doctrine-workplan
workplan_id: SSDP-6.5-IMPORTANCE-WEIGHTED-ATTENTION-AND-PROPORTIONAL-RIGOR
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: design-reviewed-ready-for-implementation
branch: ssdp-6.5-frontier-model-re-evaluation
accepted_control: 55c085261eb827e3047637d045a8e6917ea6b962
superseded_review_ready_candidate: a2e5f01e258f249f74d1eda74b883efb98fd7d59
serious_challenge: active-against-current-doctrine
workplan_review: pass-after-third-adversarial-review
workplan_review_date: 2026-09-25
created_date: 2026-09-25
---

# Protocol 6.5 Importance-Weighted Attention and Proportional-Rigor Workplan

## 1. Status and disposition

**REVIEWED D3 / protocol-doctrine reopen — implementation-ready.**

Protocol 6.5 P18 remains an immutable mechanically qualified historical candidate, but its fresh independent Review
gate is suspended. P18 repaired B65-P17-1 correctly; it did **not** close the broader development-economy defect exposed
by the repair/review trajectory.

This workplan does not authorize ratification, publication, recovery, accepted-current cutover, PR #33 merge, or any
Protocol 7 D3/D4 mutation.

The next semantic candidate must incorporate this workplan before Protocol 6.5 can return to independent Review.

**Design-review disposition: PASS after three adversarial pre-implementation passes.** The active file is the single
current implementation contract; prior review chronology is Git/qualification evidence rather than appended authority.
Further design review should be driven by a concrete new counterexample or materially changed premise, not amendment
accumulation.

## 2. Serious Challenge

Accepted Protocol 6.4 and the current Protocol 6.5 candidate contain the right principles in fragments:

- engineering fitness precedes simplicity and development economy;
- importance-weighted attention is preferred in representation;
- a first clean local defect remains local;
- evidence should be the cheapest sufficiently strong evidence for the claim;
- agents should stop search when further work has lower expected engineering value;
- project history and evidence are activated conditionally;
- repeated repair should trigger simplification rather than patch accumulation.

The abstraction remains inadequate because these principles are **not operationally connected**.

Current workflow can still behave as though:

1. every discovered problem deserves comparable reasoning depth;
2. every evidence or fixture defect deserves comparable closure ceremony;
3. a high-stakes parent task makes every child diagnostic high-stakes;
4. every uncertainty should be eliminated rather than bounded;
5. every evidence route can recursively demand equivalent evidence about its own bindings;
6. any failing test or newly surfaced edge case can indefinitely retain blocker-level attention without an explicit
   consequence/importance judgment.

That behavior is incompatible with finite human attention, model tokens, compute, CI, wall time, and project schedules.
The result can be locally rigorous while globally irrational.

The missing doctrine is:

> **Before allocating rigor, classify what is actually at stake. Allocate analysis, evidence, review, and search effort
> in proportion to the consequence and decision value of the uncertainty being resolved.**

Correctness obligations remain owner-bound. **Confidence expenditure is not uniform.**

## 3. Recent convergence evidence

### 3.1 mdstats MLFF campaign doctor failure

The recent MLFF campaign work showed a stage-priority failure:

- the user was blocked at the doctor stage;
- work began drifting toward prepare-stage activity before the doctor failure was actually resolved;
- the local fixture/gate problem attracted machinery and analysis that did not directly advance the blocked user
  outcome;
- process completion began competing with the real objective: make the doctor diagnose the campaign correctly.

The lesson is not "test less." It is:

> **Keep attention attached to the highest-value unresolved user outcome. A local fixture or intermediate gate earns
> only the rigor needed to decide or repair that outcome unless it can materially falsify a higher-level claim.**

### 3.2 Protocol 6.5 P16 -> P18 review/repair loop

The P16-P18 sequence contained genuine release-state integrity defects and therefore justified careful exact-ref
reasoning. But the trajectory also exposed a second-order economy failure:

- repeated immutable candidates and independent Reviews were consumed by progressively narrower release-state cases;
- P18 repair qualification required multiple temporary diagnostic workflow descendants to isolate one stale
  discovery/fixture expectation;
- the release-state invariant itself was important, while several diagnostic subproblems were routine and reversible;
- the protocol had no first-class rule preventing routine child problems from inheriting the full rigor of the
  release-integrity parent problem;
- even after P18 became mechanically green, the broader resource-allocation defect remained untouched.

The lesson is not that P16-P18 findings were unimportant. It is that **importance must be assessed at each problem
node, not inherited automatically from the surrounding high-stakes project**.

### 3.3 Historical doctrine already points here

Protocol 5.4 explicitly targeted human/model/context/token/tool/compute/I/O/wall-time development cost.
Protocol 5.12 targeted repeated low-value repair cycles.
Protocol 5.14 warned that solution-created intermediate problems can become quasi-authority and drive complexity
ratchets.

This workplan is therefore a strengthening and operational completion of existing simplicity/economy doctrine, not a
license to abandon rigor.

### 3.4 Project-memory basis and bounded Historical Applicability Set

This mature doctrine rework is history-sensitive, so project memory is activated as bounded decision support rather
than replayed as authority.

```yaml
pem_basis:
  accepted_project_state: 55c085261eb827e3047637d045a8e6917ea6b962
  accepted_pem: hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: a2e5f01e258f249f74d1eda74b883efb98fd7d59
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: Exact immutable release/publication identity remains a genuinely high-consequence release concern; proportional rigor must preserve it rather than generalize its cost to unrelated details.
  - id: PC-001
    disposition: APPLICABLE
    reason: Protocol 6.5 changes must preserve frozen prior-version profiles/resources independently.
  - id: DS-001
    disposition: APPLICABLE
    reason: Synthetic fixture success or failure is bounded evidence; it must not automatically acquire the same importance as the real semantic owner claim.
  - id: SP-002
    disposition: APPLICABLE
    reason: Self-reference-safe release publication remains a demonstrated release mechanism whose exact-ref integrity is material, while its surrounding diagnostics remain separately prioritizable.
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: Canonical route regeneration is not a governing mechanism for the attention-allocation redesign.
```

PEM supplies hypotheses and preservation cues only. The accepted D1-D4/current project owners still determine the
normative design.

## 4. Governing objective

Preserve the existing feasibility rule:

```text
a concretization must satisfy applicable governing authority and directly governed constraints
```

But distinguish **claim correctness** from **required confidence expenditure**.

For finite engineering resources, optimize:

```text
protect material governing outcomes and unacceptable-risk constraints
> allocate confidence/evidence in proportion to consequence and uncertainty
> choose the simplest sufficient solution
> minimize total human/model/token/tool/compute/I/O/wall-time cost
```

This is not a scalar optimization score. It is a decision discipline.

**Applicability/obligation comes before importance.** If an external contract, accepted authority, or project-required
acceptance condition applies, it remains mandatory. Importance controls how economically the obligation is understood
and satisfied; it does not erase the obligation. A low-consequence mandatory item should normally receive the cheapest
sufficient compliant treatment, not DEFER/OMIT.

**Importance is also not the same as unresolved uncertainty.** High consequence with a cheap exact oracle and an
obvious reversible repair may require little analysis. Deep treatment is justified when consequence combines with
material unresolved uncertainty, irreversibility, adversarial exposure, or a fixed external evidence floor.

A low-importance issue does not become high-importance merely because it appears during high-importance work.
A high-importance issue does not become low-importance merely because the cheap fix is attractive.

### 4.1 Version/compatibility posture

This change is intended to remain a backward-compatible Protocol **6.5 minor strengthening** over accepted 6.4:

- it changes how attention and evidence effort are allocated, not which applicable governing obligations are true;
- it preserves D1-D4 ownership, Challenge, independent Review, evidence applicability, affected acceptance, safety/security,
  release integrity, and historical recovery;
- it may eliminate process that was never independently required by those owners.

If implementation can achieve proportional rigor only by waiving a mandatory 6.4 obligation, changing D1-D4 authority,
making independent Review optional for a boundary where it is currently required, or weakening a fixed
safety/security/external evidence floor, stop and reopen the version/doctrine decision rather than silently calling the
change backward-compatible.

## 5. Importance assessment

### 5.1 Required question before escalation

Before broad analysis, new machinery, historical intake, multi-route evidence, statistical qualification, or repeated
review, ask:

> **If we are wrong about this issue, what materially bad outcome can actually occur?**

Assess the answer using the following dimensions:

- **consequence** — scientific conclusion, safety/security, corruption/data loss, wrong release authority, user-visible
  correctness, performance/resource failure, inconvenience only;
- **scope/exposure** — one fixture, one caller, a common path, an entire model/campaign/release;
- **reversibility** — trivial local retry/revert versus expensive or irreversible publication/data/decision;
- **authority proximity** — D1/D2 scientific meaning, accepted public/external contract, frozen architecture, delegated
  D4 detail, test-harness detail;
- **decision sensitivity** — whether plausible uncertainty could change the engineering/scientific decision;
- **recurrence/systemic signal** — isolated local defect versus repeated family/structural failure;
- **time/resource opportunity cost** — what more important work is displaced by deeper investigation.

Do not require numeric scoring.

If importance itself is uncertain, do **not** resolve the uncertainty by simply choosing a lower class. First take the
cheapest action that can bound consequence, affected scope, or decision sensitivity. If a plausible MATERIAL/CRITICAL
consequence cannot yet be ruled out at reasonable cost, use a provisional higher-attention posture only for the
uncertain dimension until it is bounded. Unknown impact is not evidence of low impact.

Conversely, do not retain a provisional high class after a cheap discriminating result has bounded the consequence.
Uncertainty about importance is a reason for targeted discrimination, not permanent caution.

Importance/rigor labels are **coordination metadata, not semantic authority**. Reuse a still-applicable prior
classification as a working hypothesis to avoid repeated reclassification, but revise it freely when consequence,
scope, evidence, or dependencies change. Changing a priority label alone does not require a D1-D4 redesign or
workplan revision.

### 5.2 Obligation status is orthogonal to importance

Before DEFER/OMIT, distinguish:

- **MANDATORY/APPLICABLE** — explicitly required by current authority, external contract, safety/security policy, or
  repository/project acceptance. It must be satisfied, but low consequence favors the cheapest sufficient compliant
  method.
- **DISCRETIONARY** — not required for the governed outcome. It may be estimated, deferred, omitted, or handled
  opportunistically according to importance and opportunity cost.

Do not create a persistent obligation ledger or classify every tiny issue. This distinction may remain implicit for
small work.

Priority may reorder a mandatory obligation **within** a cycle, but may not starve it past the acceptance boundary that
owns it. A deferred mandatory item remains visibly open and must be closed before that boundary can claim PASS unless
the real governing owner explicitly supports a provisional/risk-accepted continuation. Priority classification itself
cannot mint such an override.

### 5.3 Ordinal importance classes

Use four default classes. For tiny work the classification may remain implicit.

#### CRITICAL

Wrongness can materially corrupt a scientific conclusion, safety/security boundary, durable data, accepted authority,
public release/recovery identity, or another high-consequence irreversible outcome.

Default: STANDARD-to-DEEP only while decision-relevant uncertainty, irreversibility, adversarial exposure, or an
external evidence floor justifies it; a cheap decisive oracle may close it more lightly.

#### MATERIAL

Wrongness can break a primary capability, common user path, reproducibility/recovery property, frozen architecture
contract, major compatibility/resource/performance requirement, or broad correctness surface.

Default: standard-to-deep scrutiny according to uncertainty.

#### ROUTINE

Wrongness is bounded, local, reversible, and does not plausibly alter higher-level scientific/product/architecture
meaning.

Examples: ordinary implementation bugs, local parsing/fixture defects, isolated integration mistakes, obvious bounded
numerical handling within an already accepted error envelope.

Default: light-to-standard scrutiny.

#### INCIDENTAL

Wrongness has little or no consequence for the governed outcome and is primarily cosmetic, diagnostic, test-harness,
presentation, low-value provenance, or optional cleanup.

Default: defer, omit, or repair cheaply.

### 5.4 No automatic priority inheritance

A subproblem inherits a parent's high importance **only if there is a credible causal path by which being wrong about
the subproblem can materially compromise the parent outcome**.

Examples:

- release-state cutover integrity may be CRITICAL;
- a temporary CI log-classification helper used while diagnosing it is INCIDENTAL/ROUTINE;
- a core scientific coverage statistic may be CRITICAL or MATERIAL;
- a plotting label around that analysis is INCIDENTAL;
- a numerical tolerance near a scientific acceptance boundary may be MATERIAL/CRITICAL;
- a tolerance well inside an accepted analytical error envelope may be ROUTINE.

### 5.5 Problem importance is not the same as next-action priority

**Importance** asks what happens if a claim/problem is wrong. **Action priority** asks where the next unit of engineering
effort has the highest governed value.

Choose the next action using, qualitatively:

- mandatory dependency/gate status;
- unresolved decision sensitivity and unblocking value;
- critical-path/deadline relevance where a real schedule or external dependency exists;
- expected information or repair value;
- reversibility and failure cost;
- effort/opportunity cost relative to other live problems.

Do not optimize only for the cheapest available action: an expensive necessary critical-path action can outrank many
cheap peripheral tasks.

A CRITICAL issue already settled by strong applicable evidence should not keep consuming attention. A MATERIAL issue
that blocks the user and has a cheap decisive action may deserve the next action before an unrelated CRITICAL question
that is already bounded or externally blocked.

Do not require a numeric priority score.

### 5.6 Sunk-cost and attention-overrun guard

If a supposedly LIGHT/ROUTINE investigation starts consuming materially more reasoning, test cycles, candidate churn,
or machinery than its consequence justified, stop at the next safe boundary and reassess. Either:

- new evidence has revealed a genuinely more important/systemic problem -> escalate at the real owner; or
- the problem remains low consequence -> simplify the approach, use a cheaper reversible action, defer it if
  discretionary, or accept the bounded uncertainty where allowed.

Prior effort already spent is never justification for continuing a low-value path.

Repeated rediscovery of the same deferred/discretionary issue is itself evidence that the original economy judgment may
be wrong. Reassess when cumulative rediscovery, workaround, or interruption cost becomes material; either fix the shared
cause, record a reusable bounded lesson when PEM admission is justified, or continue to omit it if the cumulative cost
still does not matter. Do not create a general deferred-issue backlog merely for compliance.

## 6. Attention and rigor modes

Importance chooses a **default attention mode**, not a rigid workflow. Choose mode from consequence **and remaining
decision-relevant uncertainty**. CRITICAL does not automatically mean DEEP: if a cheap exact/reference oracle settles
the question and the repair is reversible, STANDARD or LIGHT may be sufficient. Conversely, repeated ROUTINE failures
that expose one systemic owner defect may escalate.

### DEEP

Use when consequence and uncertainty justify it.

May include independent semantic reconstruction, multiple discriminating evidence routes, adversarial holdouts,
statistical uncertainty analysis, convergence/conditioning studies, production-scale qualification, historical
counterevidence, independent Review, and composed D4 -> D2 -> D1 closure.

### STANDARD

Use focused owner analysis, one or a few strong discriminating oracles, affected regression/integration, and bounded
counterfactual reasoning. Expand only when evidence creates a real material uncertainty.

### LIGHT

Use direct owning-layer repair, bounded engineering judgment, a focused check/regression, and the ordinary final
repository gate. Estimates and approximations are allowed when their error cannot plausibly affect a material decision.

Do not manufacture a design reopen, evidence campaign, history census, or multi-stage qualification for a routine
local issue.

### DEFER / OMIT

When an issue is non-mandatory, low-consequence, and lower-value than the work it displaces, leave it unresolved,
record it only if future discovery value is material, or omit it entirely.

Bounded omission is not falsification or concealment. Known material failures, governing-contract violations,
security/safety hazards, and scientific uncertainties capable of changing the conclusion cannot be omitted this way.

### 6.1 Escalation, de-escalation, and stopping

Start with the least expensive mode plausibly capable of resolving the decision. Escalate only when a concrete
uncertainty, counterexample, recurrence signal, or external requirement makes stronger scrutiny decision-relevant.
De-escalate once that uncertainty is bounded.

Prefer a cheap reversible repair, experiment, or discriminating test over prolonged analysis when it can settle the
same decision without violating authority.

Stop when either:

- remaining uncertainty cannot plausibly change the governed decision; or
- a cheaper reversible action can establish the needed result with equal or stronger decision value.

Do not keep spending resources to convert sufficient confidence into psychological certainty.

## 7. Evidence proportionality

### 7.1 Evidence burden follows the decision

Evidence exists to change or justify a decision. Do not gather evidence merely because another evidence artifact exists.

**Evidence applicability remains a feasibility condition.** Proportional rigor may reduce how much evidence is needed;
it cannot make stale, wrong-subject, wrong-regime, wrong-parameter, invalid-oracle, or otherwise inapplicable evidence
count as current support for a mandatory claim. Reuse evidence aggressively only while the existing evidence owner says
its material applicability dimensions remain unchanged.

Use:

```text
claim importance + uncertainty + irreversibility
    -> required confidence
    -> cheapest sufficiently strong evidence
```

A full statistical campaign is appropriate when statistical uncertainty can change the scientific conclusion.
It is not appropriate merely because a floating-point tolerance exists.

### 7.2 Stop recursive evidence inflation

Normal durable closure should end once the material claim and the integrity of its evidence route are sufficiently
established for the consequence at stake.

Do not create:

```text
evidence
 -> evidence binding
 -> evidence for the evidence binding
 -> evidence binding for that evidence
 -> ...
```

unless a concrete failure/adversary model makes the next level materially capable of changing acceptance.

Exact provenance and immutable binding remain justified for high-consequence release/authority claims. A routine local
test does not need the same provenance machinery.

### 7.3 Confidence can be asymmetric

False acceptance and false rejection often have different costs.

Where appropriate, design evidence to spend effort on the expensive error:

- safety/release/scientific acceptance may demand strong false-pass resistance;
- a cheap local diagnostic may tolerate a false alarm if repair/retry is trivial;
- a non-blocking exploratory heuristic may tolerate approximation and uncertainty.

Do not silently apply this to an external/regulatory contract whose evidence threshold is fixed externally.

### 7.4 Evidence correction must not automatically create semantic-candidate churn

Tests, fixtures, qualification scripts, review records, lifecycle bindings, and diagnostic workflow instrumentation are
evidence or coordination surfaces unless they themselves define accepted D4 semantics.

If an evidence-instrument correction leaves the immutable D1-D4/product semantic subject unchanged:

- repair/remap the evidence at its own owner;
- rerun the affected qualification against the **same semantic candidate** when the release lifecycle can represent
  that honestly;
- bind the qualification to both the exact immutable **semantic subject ref** and the exact **evidence-realization
  descendant ref**, plus the exact workflow/run identity when execution is external to that commit;
- inspect the delta between those identities far enough to establish that no governed semantic source/product/public
  contract changed under the label "evidence-only";
- do not mint a replacement semantic candidate solely because an oracle, fixture, diagnostic, or evidence route was
  repaired;
- do not restart an otherwise applicable independent semantic Review merely to replay unaffected candidate semantics.

A new semantic candidate is required when the governed semantic source/product behavior/accepted contract actually
changes. If corrected evidence invalidates a material premise of a prior Review, rerun the affected Review claim
against the same semantic subject or repeat the full Review only when its independence/applicability was materially
compromised.

Implementation must reconcile the release-state/workflow machinery to express this distinction without adding a
second candidate registry or parallel lifecycle. Prefer existing immutable workflow/run head identity plus compact
qualification metadata over a new persistent state plane. If the evidence correction also changes governed semantic
source or product behavior, the "same candidate" route is invalid and a replacement semantic candidate is required.

## 8. Fixture and test authority

Tests and fixtures are evidence instruments, not automatically co-equal product problems.

On fixture/test failure:

1. identify the protected owner claim;
2. ask whether the fixture still represents that claim;
3. classify the consequence of fixture wrongness separately from product wrongness;
4. use the cheapest discriminating check that tells whether production or the oracle is wrong;
5. repair the fixture locally if the oracle is stale;
6. do not expand production architecture merely to satisfy a low-importance harness artifact.

A failing stale fixture is not a reason for deep product investigation after the owner claim has been independently
established.

## 9. Numerical/scientific proportionality

D1/D2 rigor must scale with **decision sensitivity**, not merely with the presence of numbers.

### Full scientific/numerical treatment is justified when

- uncertainty can change a scientific conclusion or ranking;
- a numerical method is near its validity/stability/convergence boundary;
- conditioning, stochastic uncertainty, bias, precision, or discretization error is material to interpretation;
- the result will become a durable/public scientific claim **and** unresolved numerical/statistical uncertainty can
  materially affect its interpretation, validity, or acceptance;
- materially different plausible methods disagree.

### Lightweight treatment is justified when

- the issue is clearly inside an already accepted error/equivalence envelope;
- a tolerance is an implementation detail far from a decision boundary;
- a manufactured/exact/reference case cheaply resolves the question;
- the numerical behavior is local, reversible, and cannot affect the scientific observable materially.

Never widen a tolerance solely because a test failed. But do not launch a statistical qualification campaign when the
governing D2 envelope already makes the outcome obvious.

## 10. Workflow priority discipline

At every material stage maintain an explicit or implicit ordering:

```text
highest-value unresolved governed outcome
    -> highest-information affordable action
    -> stop when sufficient confidence is reached
    -> proceed
```

A stage gate may block progression, but work should remain attached to the blocked outcome rather than drifting into
dependent later stages whose completion does not unblock it.

If the active blocker depends on an actually unavailable external input, service, hardware resource, approval, or human
decision, independent work may proceed when it does not assume the blocker passed, does not invalidate later evidence,
and has higher value than idling. Preserve the blocker as explicitly unresolved; parallel progress is not acceptance.

For a doctor -> prepare -> production pipeline, a failing doctor remains the active objective until:

- the doctor is repaired; or
- the doctor is independently shown to be a stale/invalid gate and the governing owner authorizes its correction.

Do not advance into dependent work merely to accumulate downstream evidence.

When deciding the next action, compare the value of **investigating**, **repairing/experimenting**, and **deferring**.
For a cheap reversible local defect, direct repair plus a discriminating check may be more rational than proving the
entire causal chain before touching code. For irreversible/high-consequence changes, diagnosis may dominate.

## 11. Review proportionality and convergence

Independent Review must still surface genuine blockers. It must not become an engine for exhaustive low-value defect
enumeration.

A reviewer should:

- independently reconstruct finding importance/consequence rather than inherit the implementer's CRITICAL/MATERIAL/
  ROUTINE/INCIDENTAL label;
- rank findings by consequence before expanding them;
- investigate cheap sibling variants far enough to identify a material family;
- stop sibling search when additional findings are low-consequence duplicates or implementation-like exploration;
- distinguish "candidate is unsafe/incorrect" from "candidate has an imperfect fixture/tooling detail";
- avoid another whole-candidate review cycle solely for a ROUTINE/INCIDENTAL issue unless it invalidates a required
  gate or reveals a material family;
- distinguish semantic candidate failure from evidence-instrument failure; the latter routes to evidence repair and
  targeted requalification when candidate semantics are unchanged;
- issue NO-PASS only for genuine semantic/conformance blockers or mandatory acceptance deficiencies that prevent the
  governed decision, not merely because another low-value imperfection can be imagined;
- reopen upstream doctrine only when the abstraction itself is materially inadequate, as in this workplan.

Review sufficiency is not proof that no conceivable defect exists. An implementer-supplied low-priority label is a
hypothesis, not authority; a reviewer must escalate it when a credible causal path to a material governed outcome is
found, and must likewise avoid preserving a high-priority label after the causal path is falsified. Priority changes
**investigation effort, not the acceptance threshold** for an applicable requirement.

## 12. Workplan attention budget

Substantial workplans should add a compact section:

```markdown
## Importance and attention allocation

### Highest-value outcomes
- ...

### Mandatory acceptance floors
- ...

### Critical/material uncertainties
- ...

### Routine/incidental surfaces
- ...

### Rigor plan
- DEEP: ...
- STANDARD: ...
- LIGHT: ...
- DEFER/OMIT: ...

### Escalation / de-escalation / stop triggers
- ...
```

This is an attention map, not a ledger. Do not require per-issue numeric scores, token budgets, or exhaustive
classification tables.

When a material priority judgment changes scope, evidence depth, defers a nontrivial issue, or permits bounded
approximation/omission, preserve the **smallest useful rationale** in the workplan/handoff: consequence, mandatory vs
discretionary status, decisive uncertainty/evidence, chosen rigor mode, and escalation/stop trigger. This makes the
decision reviewable without turning every issue into permanent process state.

For small local work, do not require this section at all.

## 13. Required protocol surfaces

Implementation should reconcile the doctrine through existing owners rather than add another parallel control plane.

### A. `abstraction-and-concretization.md`

Make importance-weighted attention operational:

- correctness/authority remains a feasibility condition;
- required confidence/evidence intensity is consequence-sensitive;
- low-consequence **non-mandatory** uncertainties may use bounded engineering judgment, estimation, deferral, or
  omission;
- high-consequence claims retain strong closure;
- stop-search/development-economy semantics apply before evidence proliferation, not only after.

### B. `convergence-and-cycle-economy.md`

Add problem-priority and attention-allocation rules before family expansion.

Convergence should minimize **total expected engineering loss + development cost**, not merely cycle count.
Repeated low-importance findings must not keep a project in high-rigor review loops unless they reveal a material
shared failure.

### C. `workflow-and-workplans.md`

Require substantial plans to identify highest-value outcomes, material uncertainties, non-priorities, rigor modes, and
escalation triggers. Preserve lightweight local routes.

### D. `evidence-evolution-and-dependencies.md`

Prevent recursive evidence inflation. Evidence dependencies are followed to the depth needed to establish the material
decision, not to an unbounded proof graph.

Reuse still-applicable evidence aggressively when its uncertainty cannot change the current decision. Importance must
not be used to relabel stale/inapplicable evidence as current. Same-semantic-candidate requalification after an
evidence-only correction must bind the exact semantic subject and exact realization descendant/run separately.

### E. `testing-and-validation.md`

Make oracle/fixture failures consequence-aware. Add explicit distinction between:

- material owner failure;
- stale/incorrect evidence instrument;
- routine harness defect.

Strengthen the existing "cheapest sufficiently strong" rule into a general proportional-rigor rule.

### F. D1/D2 role and numerical/scientific references

State that scientific/statistical/numerical rigor scales with the consequence and decision sensitivity of uncertainty.
Do not turn every numerical detail into a research-grade qualification campaign.

### G. software-design / software-implementation entrypoints

Before broadening scope, require a bounded importance judgment.

Implementation should fix ROUTINE local defects directly.
Design should reserve architecture/doctrine reopening for materially consequential evidence.

### H. implementation workplan template

Add the compact "Importance and attention allocation" section for substantial work and make it explicitly optional for
small/local changes.

### I. Protocol release documentation closeout and persistence

Every protocol successor cycle must include a **documentation closeout after semantic implementation stabilizes and
before the replacement immutable semantic candidate is frozen**.

#### Root README

Recompile/review root `README.md` as the current user-facing guide, not as normative protocol authority or release
state. It should remain useful to a technically competent newcomer without requiring them to read historical workplans.

General writing guidance:

- open with a concise explanation of what SSDP is for and the core philosophy;
- explain the D1 -> D4 abstraction/concretization hierarchy and why it matters;
- explain how to select and use the skills, the normal development cycle, common workflows, and the simplicity/economy
  doctrine;
- summarize current major capabilities only to the level needed to orient use;
- keep practical examples close to the decisions they clarify;
- prefer clear, direct, digestible prose and progressive disclosure over amendment chronology, jargon accumulation, or
  exhaustive feature catalogs;
- revise for the "well-written" standard: remove redundancy, vague abstractions, needless ceremony, and sentences that
  a new user would have to reverse-engineer;
- keep mutable accepted/candidate/public/recovery identities out of the guide and route them to
  `PROTOCOL-RELEASE-STATE.yaml`;
- route capability history to `CHANGELOG.md` and detailed semantic/release chronology to
  `history/SEMANTIC_EVOLUTION.md`.

This is a semantic writing review, not a requirement that every release mechanically rewrite every paragraph. If a
section is already the clearest accurate statement of current doctrine, preserving it is preferable to churn.

Stop the writing pass when the guide is accurate, newcomer-comprehensible, current, navigable, and free of material
redundancy or misleading historical residue. Do not turn "well written" into an open-ended polishing campaign.

#### CHANGELOG

Update root `CHANGELOG.md` for every new protocol version with a concise user-facing summary of capabilities added,
strengthened, replaced, or deliberately retired. It must not become a mutable release-status ledger or a dump of
candidate SHAs/review iterations. Detailed rationale and failed-attempt chronology remain in semantic history.

#### Source README

Keep `source/README.md` a concise source/contributor map. Do not duplicate the full root user guide there.

#### Persistence mechanism

Persist this obligation in root `AGENTS.md` so future protocol work cannot silently omit documentation closeout.
Also add one **small objective release-document persistence check** to the existing repository acceptance path during
implementation:

- the version declared by `source/PROTOCOL_VERSION` has a corresponding capability entry in root `CHANGELOG.md`;
- root `README.md` retains routes to `CHANGELOG.md` and `PROTOCOL-RELEASE-STATE.yaml`.

This check must establish presence/routing only. Do **not** make it score prose quality, require feature keywords, parse
doctrine meaning, or force paragraph churn. Semantic README quality remains a human/agent review responsibility.
Prefer an existing test/check surface over a new framework.

Explain proportional rigor in the final README as the operational completion of development economy and active
simplicity. Preserve frozen historical resources and regenerate derived/package surfaces only through the canonical
build.

## 14. Required counterfactual scenarios

Qualification must test decisions, not wording.

1. **Doctor-stage local fixture defect.**
   A campaign is blocked at doctor. The agent stays on doctor, uses a light focused diagnostic, fixes or invalidates
   the fixture, and does not advance to prepare simply to make progress.

2. **Core scientific inference.**
   A result can change a scientific conclusion. The agent selects DEEP treatment with appropriate uncertainty,
   convergence/statistical/external adequacy evidence.

3. **Trivial numerical tolerance inside accepted envelope.**
   The agent uses the existing D2 error envelope and a focused check; it does not launch an independent statistical
   campaign.

4. **Tolerance near decision boundary.**
   The same tolerance becomes MATERIAL/CRITICAL because plausible uncertainty can change acceptance; D2 scrutiny
   escalates.

5. **Release authority mapping.**
   Public/recovery/accepted-current identity remains high-consequence and exact-ref/fail-closed evidence remains
   justified.

6. **Stale merge/test fixture during release work.**
   The parent release invariant stays high-importance while the stale fixture is repaired locally without promoting it
   into another architecture problem.

7. **Evidence recursion.**
   A durable claim has a valid evidence route and one justified integrity check. The agent stops rather than requiring
   an infinite hierarchy of evidence bindings.

8. **No priority inheritance.**
   A low-consequence diagnostic child inside a high-consequence scientific/release project remains LIGHT unless a real
   causal path to the parent outcome is shown.

9. **Bounded omission.**
   An INCIDENTAL non-mandatory imperfection may remain unresolved when fixing it has lower expected value than
   proceeding; it is not mislabeled as PASS evidence for a material claim.

10. **Escalation on recurrence.**
    Several ROUTINE local failures revealing one shared material owner defect escalate to family-level
    STANDARD/DEEP analysis rather than remaining individually cheap forever.

11. **Security/safety/external threshold.**
    A fixed external obligation cannot be downgraded by local importance ranking.

12. **Review saturation.**
    A reviewer stops low-value sibling enumeration after the material family is characterized; another independent
    full review is not demanded merely to search for more inconsequential variants.

13. **Uncertain importance.**
    A defect has unclear blast radius. The agent performs the cheapest bounded impact/discriminating check rather than
    defaulting it to INCIDENTAL or launching a whole-system campaign; the class then de-escalates or escalates from
    evidence.

14. **Implementer misclassification.**
    Implementation labels a finding ROUTINE, but independent Review identifies a credible path to a material governed
    outcome and escalates it. The reverse case also de-escalates a disproven high-priority label.

15. **Stale evidence cannot be cheapened into applicability.**
    A low-priority mandatory claim has stale wrong-regime evidence. The agent must obtain current applicable evidence
    or otherwise satisfy the owner; proportional rigor may choose a cheap oracle but may not reuse the stale pass.

16. **Same semantic subject, corrected evidence instrument.**
    A frozen candidate's test fixture is wrong but product semantics are unchanged. Requalification binds the original
    semantic subject plus the exact descendant/run containing the corrected fixture, verifies the intervening delta is
    evidence-only, and does not mint a replacement semantic candidate.

17. **Attention overrun / sunk cost.**
    A ROUTINE investigation starts accumulating repeated diagnostics and machinery without revealing higher
    consequence. The agent reclassifies at the safe boundary and simplifies/stops rather than continuing because of
    prior effort.

18. **Release-document persistence.**
    A protocol version advances without a corresponding CHANGELOG capability entry, or README loses its release-state/
    changelog routes. The cheap objective repository check fails; prose quality remains outside that check.

19. **Mandatory low-salience starvation.**
    A mandatory but low-consequence obligation is repeatedly deprioritized. The task may schedule it late, but the
    owning acceptance boundary cannot PASS until it is closed or the real owner explicitly authorizes provisional/risk-
    accepted continuation.

20. **Externally blocked critical path.**
    The highest-priority task waits on unavailable hardware/approval. Independent useful work may continue without
    pretending the blocker passed or collecting dependent evidence that assumes it did.

21. **Priority label persistence without authority.**
    A handoff reuses a prior ROUTINE/MATERIAL classification to avoid rediscovery, but new evidence changes consequence.
    The next agent revises the label without D3 reopening and preserves only the material rationale.

22. **Repeated deferred rediscovery.**
    An INCIDENTAL issue is rediscovered across several cycles. Cumulative interruption cost becomes material and
    triggers reassessment/shared repair or bounded PEM learning rather than endless re-deferral.

## 15. Acceptance

The redesign is successful only if an agent can reliably distinguish:

- important problem from nearby low-value detail;
- material product/scientific uncertainty from evidence-instrument noise;
- need for proof from desire for certainty;
- high-value next action from process-completion activity;
- necessary evidence integrity from recursive provenance bureaucracy;
- justified deep scientific qualification from a routine numerical implementation check;
- a genuine blocker from an imperfection that can be tolerated, estimated, deferred, or omitted;
- uncertain importance from genuinely low importance;
- problem importance from next-action priority;
- applicable evidence from stale evidence that is merely cheap to reuse;
- semantic mutation from an evidence-only descendant;
- scheduling a mandatory low-salience obligation from waiving it;
- a reusable priority judgment from a new authority;
- productive work around an external blocker from falsely advancing a dependent gate;
- genuinely cheap omission from repeated rediscovery whose cumulative cost has become material.

Repository qualification should include focused semantic counterfactuals plus the ordinary assembled repository build.
It must also demonstrate that evidence-only/fixture corrections can be requalified without unnecessary semantic
candidate churn when the semantic subject is unchanged.

Before freeze, documentation closeout must confirm that root `README.md` accurately explains the current protocol to
a new user and that `CHANGELOG.md` contains the target-version capability summary without duplicating mutable release
state. The small objective release-document persistence check must also pass. Semantic writing quality remains
inspection, not a word-presence score.

Do **not** create a large new validator framework, scoring engine, attention database, mandatory telemetry system, or
prose-quality checker.

## 16. Non-goals / forbidden implementation

Do not introduce:

- a universal numeric importance/risk score;
- mandatory token accounting;
- fixed per-task time/tool-call budgets;
- a new lifecycle role or approval gate;
- an "importance reviewer";
- a persistent issue-priority ledger;
- a second evidence registry;
- a recursively self-validating evidence graph;
- blanket permission to ignore failing tests;
- blanket permission to weaken tolerances;
- a rule that every scientific task requires statistical qualification;
- a rule that every low-priority problem must be fixed before progress.

Do not encode model-specific behavior.

## 17. Implementation sequence

1. **Doctrine reconciliation first.**
   Reconcile the universal kernel, convergence/economy, workflow, evidence, and testing owners around proportional
   rigor and no automatic priority inheritance.
2. **Domain consequences.**
   Reconcile D1/D2 scientific/numerical evidence intensity and D3/D4 local-repair behavior.
3. **Entrypoints/template.**
   Make the decision discipline operational while keeping small work lightweight.
4. **Lifecycle/evidence economy.**
   Reconcile evidence-only correction, targeted requalification, and semantic-candidate identity so fixture/oracle
   repairs do not automatically force replacement semantic candidates or whole-candidate Review churn.
5. **Counterfactual qualification.**
   Add the bounded scenarios above and remove/relax any existing policy oracle that forces uniform rigor for trivial
   delegated details.
6. **Generated/build parity.**
   Regenerate derived distributions, profiles, and snapshots through canonical builders without mutating frozen
   prior-version resources.
7. **Documentation closeout.**
   After semantic content stabilizes, recompile/review root `README.md`, update `CHANGELOG.md`, reconcile concise
   versioning/history text as needed, confirm `AGENTS.md` retains this closeout obligation, and add/run the small
   objective current-version/changelog + README-route persistence check in the existing repository acceptance path.
8. **Stabilization.**
   Inspect the final design specifically for a new bureaucracy that would defeat its own purpose and for any
   high-consequence requirement accidentally weakened by priority language.
9. **Freeze replacement candidate.**
   Only after assembled qualification **and documentation closeout** freeze the next Protocol 6.5 semantic candidate
   and return to fresh independent Review.

## 18. Implementation authority

### Frozen for this workplan

- Engineering/scientific correctness and governing authority remain protected.
- Applicability/mandatory obligation is orthogonal to importance; priority never waives a binding requirement.
- Safety/security/external/regulatory obligations cannot be downgraded by local priority judgments.
- Importance is consequence-based and decision-local; unknown impact is not evidence of low impact.
- Importance/rigor labels are coordination metadata, not D1-D4 authority or acceptance thresholds.
- Attention intensity also depends on unresolved decision-relevant uncertainty and irreversibility; CRITICAL does not
  mechanically imply DEEP when a cheap strong oracle already settles the issue.
- Subproblems do not inherit parent priority automatically.
- Evidence intensity is proportional to consequence, uncertainty, and irreversibility.
- Cheapest-sufficient evidence remains the default.
- Bounded engineering judgment, estimation, deferral, and omission are legitimate for low-consequence non-mandatory
  uncertainty.
- Full scientific/statistical qualification is reserved for claims whose uncertainty justifies it.
- Development economy includes real human/model/token/tool/compute/I/O/wall-time opportunity cost, critical-path
  opportunity cost, and cumulative rediscovery cost where material.
- Evidence applicability remains mandatory: priority cannot revive stale/inapplicable evidence.
- Evidence-instrument correction must not automatically mint a replacement semantic candidate when D1-D4/product
  semantics are unchanged; same-candidate requalification binds semantic subject and evidence realization identities
  separately and verifies the intervening change is non-semantic.
- Every protocol successor performs README/CHANGELOG documentation closeout before semantic-candidate freeze, with the
  persistent repository instruction owned by `AGENTS.md` and a minimal objective version/route persistence check in
  repository acceptance.
- No new lifecycle role, separate approval gate, registry, scoring engine, telemetry bureaucracy, or prose-quality parser; bounded assertions may be added inside the existing repository acceptance path when they protect stable objective invariants.

### Delegated

- Exact terminology for importance and rigor classes.
- Exact section placement within existing canonical owners.
- Exact counterfactual test organization.
- Whether a compact importance statement is prose or a tiny structured block in substantial workplans.
- Exact implementation details for context/routing reductions.

### Reopen on evidence

Reopen this design only if:

- qualitative importance classes are too ambiguous to produce consistent decisions;
- proportional evidence cannot preserve a material accepted scientific/safety/release guarantee;
- a fixed external standard requires a stronger uniform evidence floor for a bounded domain;
- counterfactual qualification shows low-priority deferral can silently hide material failures;
- the proposed attention mechanism itself adds more process cost than it removes;
- the release lifecycle cannot safely distinguish semantic mutation from evidence-only correction without introducing
  more complexity than it saves; or
- the minimal release-document persistence check cannot be implemented without becoming a semantic/prose parser.

Do not reopen merely because an existing test or fixture encodes uniform-rigor behavior. Such a test is evidence to
reconcile against the new accepted doctrine if this workplan is ratified.
