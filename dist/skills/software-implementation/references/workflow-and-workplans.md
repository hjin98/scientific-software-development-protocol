# Workflow, Change Plans, Handoffs, and Review

Own workflow/lifecycle, authority mutation and acceptance sequencing, workplan, handoff, working state, review sequencing, resumability, and closeout semantics. Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence applicability/dependency/evolution is owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); testing/acceptance methods by [Testing and validation](testing-and-validation.md); Project Engineering Memory (PEM) use, Historical Applicability Set (HAS) and closeout learning by [Project Engineering Memory](project-engineering-memory.md); recurrence/rigor economy by [Convergence and development-cycle economy](convergence-and-cycle-economy.md).

## Semantic routing, not a waterfall

D1 scientific formulation -> D2 numerical method -> D3 architecture -> D4 specification/implementation is semantic ordering, not a mandatory four-stage pipeline. Before mutation classify the earliest/highest accepted abstraction whose semantics may materially change, directly applicable side constraints, and materially dependent descendants/evidence. Start there; preserve unaffected parents/siblings. File count or implementation breadth does not itself raise the domain.

Supporting specialists (`software-documentation`, `software-maintenance-audit`, `repository-hygiene`) are non-authoritative capabilities, not approval stages.

## Authority lifecycle, mutation, and impact closure

Projects may encode lifecycle locally but must distinguish enough state to prevent speculative/stale material becoming current authority: proposed; accepted-current; challenged; risk-accepted/provisional; stale-dependent; superseded/historical; release-pinned/publication. Human ratification is orthogonal. PEM has separate evidence/coverage/maturity/base/overlay lifecycle and is not D1-D4 acceptance.

A durable authority mutation follows the owning domain's acceptance contract: proposal -> independent falsification where required -> required human ratification -> acceptance -> bounded dependent impact -> reconcretization/revalidation. Repository presence alone does not promote a proposal. A PEM record may support/challenge/propose such a change, but cannot perform the acceptance step itself. A clarification that materially narrows/changes admissible interpretation or concretization is a semantic mutation for dependency/evidence/version impact unless established representation-only.

When accepted authority changes, review only materially dependent descendants/evidence and preserve unaffected siblings/still-valid evidence. A bounded dependency view is an aid, not proof of independence unless its relevant scope was explicitly reviewed complete. Detailed evidence/dependency rules are owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md). When the changed owner is cited by an authority-bound learned capability/current notice, reconcile that non-authoritative binding as a dependent representation rather than allowing memory to preserve obsolete force. For high-risk scientific/numerical claims, trace composed D4 -> D2 -> D1 -> external-adequacy closure when material (method owned by [Testing and validation](testing-and-validation.md)).

An unresolved Serious Challenge under an allowed explicit human risk override leaves dependent results `risk-accepted/provisional`; descendants must not reset that state to accepted-current or emit unqualified Pass/closure while the challenge remains unresolved.

## Workplans as bounded contracts

Use a workplan/change plan when it materially reduces ambiguity, rediscovery, sequencing risk, cross-domain drift, or downstream rework. Workplans are coordination/authority for the bounded cycle, not terminal objectives or proof scripts.

A substantial handoff distinguishes:

1. **governing parent/problem invariants and side constraints**;
2. **cycle-scoped child decisions** intentionally fixed for this cycle;
3. **delegated concretization space** that remains replaceable while 1-2 survive.

Preserve material concern/rationale, required end state, constraints/forbidden behavior, known owning/affected surface, task-specific acceptance, dependencies, non-goals and reopen triggers. Suggested mechanisms remain delegated unless explicitly frozen or accepted by the owning authority.

The accepted plan is the minimum known contract, not a ceiling on newly discovered affected behavior or logical consequences of already-binding authority. Affected-surface expansion is not requirement expansion.

### Durable authority vs cycle freeze

Accepted-current D1-D4 authority is durable semantic ownership. A workplan may freeze lower choices for one cycle without promoting them into durable authority. Conversely, a workplan cannot omit already-current authority merely because it does not restate it. Ordinary implementation/review iterations do not need numbered authority revisions unless accepted task semantics actually change.

## Importance and attention allocation

For substantial work, keep a compact attention map rather than an exhaustive priority ledger:

- highest-value governed outcomes and mandatory acceptance floors;
- critical/material uncertainties;
- routine/incidental surfaces;
- intended `DEEP` / `STANDARD` / `LIGHT` / `DEFER-OMIT` treatment;
- escalation, de-escalation and stop triggers.

Applicability comes before importance. Priority may reorder a mandatory obligation but cannot waive or starve it beyond the acceptance boundary that owns it. Importance labels are revisable coordination state, not D1-D4 authority. Preserve only the smallest useful rationale when a material priority judgment changes scope/evidence depth, defers nontrivial work, or permits bounded approximation/omission: consequence, mandatory/discretionary status, decisive uncertainty/evidence, chosen rigor, and reopen/stop trigger. Tiny/local work needs no attention-map ceremony.

Stay attached to the highest-value unresolved governed outcome rather than process-completion activity. If its critical path genuinely waits on unavailable hardware, service, external input, approval, or human decision, independent work may proceed only when it does not assume the blocker passed or invalidate later evidence. Keep the blocker explicitly open; parallel progress is not acceptance.

## Conditional project-memory activation

PEM is decision support, not a mandatory workflow stage. Activate it only when demonstrated project history can materially change the decision: substantial rework of mature D1-D4 semantics/concretization, replacement/consolidation of mature machinery, suspected recurrence, substantial optimization/scaling, migration/recovery/revert/restoration where prior choices matter, or an active workplan explicitly binding relevant memory. A first clean local defect, trivial/unrelated work, or mere presence of a PEM file does not load memory. When it fires, follow the retrieval and HAS contract in [Project Engineering Memory](project-engineering-memory.md); a memory-triggering workplan or handoff records the exact accepted/base memory, candidate overlay and HAS dispositions it relied on, and refreshes them if that basis advances before integration/closeout.

## Decision-sufficient handoffs and working state

A current handoff must be snapshot-complete for its **governed task scope**: recover still-binding task-specific invariants/constraints, cycle decisions, non-goals, material acceptance/evidence obligations, authority state, unresolved blockers/Challenge and genuine reopen triggers without hidden chat or unavailable history. A memory-triggering handoff additionally records its exact PEM basis/overlay and current HAS dispositions; it does not replay the project-memory corpus.

Prefer a decision-sufficient projection over replay. The hot representation leads with:

```text
governed objective
exact protocol / authority / workplan / candidate identities
local decisions and delegated space
open blockers, material uncertainty, Challenge
applicable evidence state (including failed / unavailable / stale)
next action
genuine reopen and stop conditions
```

Do **not** copy generic protocol doctrine, settled rationale, raw chronology or long evidence logs into a handoff: point to resolvable version-bound owners/records and state only the local delta. When the receiver cannot resolve a referenced owner/version, carry the minimum required semantics locally rather than assuming shared hidden context. Dropping an open blocker, required check, uncertainty or reopen condition is a Lossless Representation defect, not compression.

**Working State** (context checkpoint): for long/interruption-prone work, keep compact temporary working state—the same projection, anchored by governing snapshot identity—so compaction/resume does not re-derive settled context. It may be Markdown, YAML, JSON, host session/task state or an equivalent form; no schema, file, tool or Orchestrator is required. It:

- is derived coordination state, not authority: it cannot create or mutate D1-D4 authority, declare acceptance or Review outcome, or replace a canonical workplan/evidence record;
- is never a required repository artifact for local work and should disappear when no longer useful;
- is valid only for the exact protocol/authority/workplan/candidate/regime/scope and accepted-memory basis it records; after any of those change it is stale and must be re-derived from canonical owners, never patched forward by assertion;
- yields to canonical sources whenever they disagree or exact wording is needed.

### Workplan contract versus transient progress

A workplan is a bounded semantic/cycle contract. Change it when its governed contract changes: a material cycle decision, a newly binding obligation, a genuine reopen, or acceptance/lifecycle state the project deliberately records there. Do not amend it merely because a task completed, a command ran, a test passed, a transient blocker cleared, the next action changed, or an implementation-local repair stayed inside delegated space; that progress belongs in Working State, native issue/task/agent state, commits or evidence records.

## Local reconciliation, simplification, and urgency

A child role may choose any concretization satisfying its parents/constraints. Removing/consolidating/replacing expected lower machinery with an equivalent concretization is local reconciliation, not redesign. Reopen the parent only when its accepted abstraction or material cycle decision must change.

Generic recurrence/family/simplification rules are owned by [Convergence and development-cycle economy](convergence-and-cycle-economy.md). A first clean local defect remains local. Material sibling recurrence shifts reasoning to the shared owner/mechanism; when structural complexity is implicated, simplify/re-derive delegated machinery before another additive durable repair.

A separately governed urgency/safety/security/reliability/incident requirement may justify a bounded reversible or safely replaceable mitigation before normal simplification. Keep unresolved debt explicit; emergency use never promotes the mitigation into durable authority or manufactures closure.

## Evidence, stages, and impact closure

Evidence semantics are not repeated here. When a material authority/concretization changes, use the evidence owner to identify materially affected descendants/evidence/documentation/dependency/history, preserve unaffected siblings/still-valid evidence, and close each material impact item as resolved, preserved-with-reason, or unavailable/blocking. If a materially depended-on PEM entry changes, perform the bounded transitive/reverse impact closure required by its canonical owners and refresh affected HAS state.

Executable D4 stage-local/final acceptance is owned by [Testing and validation](testing-and-validation.md). A coherent material behavior/risk boundary is normally one implementation stage even when several files/functions change. Required stage-local affected regression cannot be deferred merely because a later full suite exists; final assembled acceptance still reflects the candidate after all material executable edits.

## Review, Verification, Stabilization, and Audit

**Review** independently reconstructs governing authority/candidate/evidence applicability and attempts targeted falsification. Review independence means the reviewing context did not author the candidate and does not inherit author conclusions; model-family diversity can strengthen corroboration but is not required for ordinary independence. Missing required pre-Review acceptance remains a blocker; Review does not move those checks later. When PEM is material, Review treats it as a high-information hypothesis index and independently verifies current owners/assembled behavior rather than inheriting its conclusions. After repeated related findings, the next Review changes strategy as owned by the convergence reference rather than repeating narrow isolated discovery.

**Optional independent cognitive trajectories.** For substantial/high-risk work whose review questions are loosely coupled, separate agents/contexts may falsify distinct questions—conformance/affected surface, abstraction adequacy/Challenge, simplification/complexity, scientific/numerical specialist review, evidence/oracle challenge. Use them only when expected information gain exceeds decomposition and synthesis cost; not for local/trivial work, questions tightly coupled to one live execution state, or hosts that cannot provide separate contexts. Multi-agent execution is never required. A subagent that receives the author's conclusions is not independent. Separate context improves process independence but not epistemic independence when agents share model, source corpus, toolchain or oracle; when a claim relies on independence, record material common-mode dependencies and add a distinct evidence route or perspective only where it materially reduces that risk. A synthesizer reconciles findings through evidence and owner adjudication; it cannot erase unresolved contradictory material evidence by vote.

For a substantial protocol/authority Review, also perform an **out-of-matrix abstraction-adequacy pass**: reconstruct global invariants from current owners, temporarily ignore the author's workplan/obligation matrix/test decomposition, inspect the assembled candidate, and attempt a locally-compliant trajectory that still violates a material global invariant. Record when no such trajectory survives; do not invent a defect merely to satisfy the pass. Challenge the adequacy of the qualification method itself rather than assuming that green author-supplied checks are sufficient.

**Verification** is a deeper risk-triggered falsification mode for materially high-risk claims; it may reconcile multiple authorities, construct counterexamples, or trace composed D4->D1 behavior. It is not a routine duplicate Review.

**Stabilization / architecture-GC** is a non-mutating convergence-boundary question: would the current concretization still be deliberately chosen for the same governing authority? Required changes return through the owning domain.

**Health Audit** is periodic longitudinal sensing; it routes findings but does not mutate D1-D4 authority or self-admit them into PEM.

Every material Review/Verification/acceptance boundary applies the universal Challenge rule. Surface an active Serious Challenge before ordinary blockers or Pass/No-Pass and route it to the earliest affected semantic owner.

## Specialized semantic definitions

Semantic-definition/traceability adds no workflow stage. At intake/design/review it activates only when the governed work materially introduces, changes, imports, reuses, or depends on specialized semantic objects or parameter/default bindings; then [Semantic definition and traceability](semantic-definition-and-traceability.md) owns handoff identity, binding-impact scope and Review reconstruction.

## Human gates and closeout learning

Human gates attach to governed semantic risk, not every transition. The designated human authority is required where project/domain policy assigns ratification/adjudication. Orchestration may represent pending/accepted/rejected state but cannot self-approve it. A visible risk override authorizes only bounded continuation where allowed; dependent outputs remain provisional and cannot close the challenged claim unqualified.

After every accepted material repair/rework/optimization/revert/restoration, perform the **closeout learning assessment** owned by [Project Engineering Memory](project-engineering-memory.md) before declaring repository/lifecycle closure. Ordinary fix chronology and first-clean local defects stay out of permanent memory; no specialist can self-promote findings into authority.

After semantic/functional closure, reconcile only affected current normative documents, guides, generated artifacts, evidence/dependency views, PEM when triggered, semantic history, workplan state and repository hygiene. Current owners explain what is true; PEM summarizes evidence-backed project learning; history explains why. Archive/supersede transition artifacts only after their still-current semantics reside in canonical current authority/state.

Apply the Lossless Representation Rule to workflow artifacts: lead with disposition/Challenge/blockers/current decisions, avoid amendment replay and generic doctrine duplication, keep historical/raw detail cold but discoverable, and preserve every mandatory lower-salience closure condition.
