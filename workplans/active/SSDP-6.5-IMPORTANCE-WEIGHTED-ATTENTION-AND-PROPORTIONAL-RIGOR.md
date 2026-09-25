---
kind: protocol-doctrine-workplan
workplan_id: SSDP-6.5-IMPORTANCE-WEIGHTED-ATTENTION-AND-PROPORTIONAL-RIGOR
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: proposed-d3-reopen
branch: ssdp-6.5-frontier-model-re-evaluation
accepted_control: 55c085261eb827e3047637d045a8e6917ea6b962
superseded_review_ready_candidate: a2e5f01e258f249f74d1eda74b883efb98fd7d59
serious_challenge: active
created_date: 2026-09-25
---

# Protocol 6.5 Importance-Weighted Attention and Proportional-Rigor Workplan

## 1. Status and disposition

**PROPOSED D3 / protocol-doctrine reopen.**

Protocol 6.5 P18 remains an immutable mechanically qualified historical candidate, but its fresh independent Review
gate is suspended. P18 repaired B65-P17-1 correctly; it did **not** close the broader development-economy defect exposed
by the repair/review trajectory.

This workplan does not authorize ratification, publication, recovery, accepted-current cutover, PR #33 merge, or any
Protocol 7 D3/D4 mutation.

The next semantic candidate must incorporate this workplan before Protocol 6.5 can return to independent Review.

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

A low-importance issue does not become high-importance merely because it appears during high-importance work.
A high-importance issue does not become low-importance merely because the cheap fix is attractive.

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

### 5.2 Ordinal importance classes

Use four default classes. For tiny work the classification may remain implicit.

#### CRITICAL

Wrongness can materially corrupt a scientific conclusion, safety/security boundary, durable data, accepted authority,
public release/recovery identity, or another high-consequence irreversible outcome.

Default: deep scrutiny.

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

### 5.3 No automatic priority inheritance

A subproblem inherits a parent's high importance **only if there is a credible causal path by which being wrong about
the subproblem can materially compromise the parent outcome**.

Examples:

- release-state cutover integrity may be CRITICAL;
- a temporary CI log-classification helper used while diagnosing it is INCIDENTAL/ROUTINE;
- a core scientific coverage statistic may be CRITICAL or MATERIAL;
- a plotting label around that analysis is INCIDENTAL;
- a numerical tolerance near a scientific acceptance boundary may be MATERIAL/CRITICAL;
- a tolerance well inside an accepted analytical error envelope may be ROUTINE.

## 6. Attention and rigor modes

Importance chooses a **default attention mode**, not a rigid workflow.

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

## 7. Evidence proportionality

### 7.1 Evidence burden follows the decision

Evidence exists to change or justify a decision. Do not gather evidence merely because another evidence artifact exists.

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
- the result will become a durable/public scientific claim;
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
later stages whose completion does not unblock it.

For a doctor -> prepare -> production pipeline, a failing doctor remains the active objective until:

- the doctor is repaired; or
- the doctor is independently shown to be a stale/invalid gate and the governing owner authorizes its correction.

Do not advance merely to accumulate downstream evidence.

## 11. Review proportionality and convergence

Independent Review must still surface genuine blockers. It must not become an engine for exhaustive low-value defect
enumeration.

A reviewer should:

- rank findings by consequence before expanding them;
- investigate cheap sibling variants far enough to identify a material family;
- stop sibling search when additional findings are low-consequence duplicates or implementation-like exploration;
- distinguish "candidate is unsafe/incorrect" from "candidate has an imperfect fixture/tooling detail";
- avoid another whole-candidate review cycle solely for a ROUTINE/INCIDENTAL issue unless it invalidates a required
  gate or reveals a material family;
- reopen upstream doctrine only when the abstraction itself is materially inadequate, as in this workplan.

Review sufficiency is not proof that no conceivable defect exists.

## 12. Workplan attention budget

Substantial workplans should add a compact section:

```markdown
## Importance and attention allocation

### Highest-value outcomes
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

### Escalation triggers
- ...
```

This is an attention map, not a ledger. Do not require per-issue numeric scores, token budgets, or exhaustive
classification tables.

For small local work, do not require this section at all.

## 13. Required protocol surfaces

Implementation should reconcile the doctrine through existing owners rather than add another parallel control plane.

### A. `abstraction-and-concretization.md`

Make importance-weighted attention operational:

- correctness/authority remains a feasibility condition;
- required confidence/evidence intensity is consequence-sensitive;
- low-consequence delegated uncertainties may use bounded engineering judgment or omission;
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

Reuse still-applicable evidence aggressively when its uncertainty cannot change the current decision.

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

### I. README/versioning/generated surfaces

Explain proportional rigor as the operational completion of development economy and active simplicity. Preserve frozen
historical resources and regenerate derived/package surfaces only through the canonical build.

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

## 15. Acceptance

The redesign is successful only if an agent can reliably distinguish:

- important problem from nearby low-value detail;
- material product/scientific uncertainty from evidence-instrument noise;
- need for proof from desire for certainty;
- high-value next action from process-completion activity;
- necessary evidence integrity from recursive provenance bureaucracy;
- justified deep scientific qualification from a routine numerical implementation check;
- a genuine blocker from an imperfection that can be tolerated, estimated, deferred, or omitted.

Repository qualification should include focused semantic counterfactuals plus the ordinary assembled repository build.
Do **not** create a large new validator framework, scoring engine, attention database, or mandatory telemetry system.

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
4. **Counterfactual qualification.**
   Add the bounded scenarios above and remove/relax any existing policy oracle that forces uniform rigor for trivial
   delegated details.
5. **Documentation/build parity.**
   Update concise user-facing doctrine, versioning/history as appropriate, generated distributions, profiles, and
   snapshots without mutating frozen prior-version resources.
6. **Stabilization.**
   Inspect the final design specifically for a new bureaucracy that would defeat its own purpose.
7. **Freeze replacement candidate.**
   Only after final assembled qualification freeze the next Protocol 6.5 semantic candidate and return to fresh
   independent Review.

## 18. Implementation authority

### Frozen for this workplan

- Engineering/scientific correctness and governing authority remain protected.
- Safety/security/external/regulatory obligations cannot be downgraded by local priority judgments.
- Importance is consequence-based and decision-local.
- Subproblems do not inherit parent priority automatically.
- Evidence intensity is proportional to consequence, uncertainty, and irreversibility.
- Cheapest-sufficient evidence remains the default.
- Bounded engineering judgment, estimation, deferral, and omission are legitimate for low-consequence non-mandatory
  uncertainty.
- Full scientific/statistical qualification is reserved for claims whose uncertainty justifies it.
- Development economy includes real human/model/token/tool/compute/I/O/wall-time opportunity cost.
- No new role, gate, registry, scoring engine, or telemetry bureaucracy.

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
- the proposed attention mechanism itself adds more process cost than it removes.

Do not reopen merely because an existing test or fixture encodes uniform-rigor behavior. Such a test is evidence to
reconcile against the new accepted doctrine if this workplan is ratified.
