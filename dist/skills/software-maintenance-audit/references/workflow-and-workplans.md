# Workflow, Change Plans, Handoffs, and Review

Own workflow/lifecycle, workplan, handoff, review sequencing, resumability, and closeout semantics. Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence applicability/dependency/evolution is owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); testing/acceptance methods are owned by [Testing and validation](testing-and-validation.md).

## Semantic routing, not a waterfall

D1 scientific formulation -> D2 numerical method -> D3 architecture -> D4 specification/implementation is semantic ordering, not a mandatory four-stage pipeline. Before mutation classify the earliest/highest accepted abstraction whose semantics may materially change, directly applicable side constraints, and materially dependent descendants/evidence. Start there; preserve unaffected parents/siblings. File count or implementation breadth does not itself raise the domain.

Supporting specialists (`software-documentation`, `software-maintenance-audit`, `repository-hygiene`) are non-authoritative capabilities, not approval stages.

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

## Lossless handoff and resumable state

A current handoff must be snapshot-complete for its **governed task scope**: recover still-binding task-specific invariants/constraints, cycle decisions, non-goals, material acceptance/evidence obligations, authority state, unresolved blockers/Challenge and genuine reopen triggers without hidden chat or unavailable history.

Do **not** copy generic protocol doctrine into every handoff. Point to resolvable version-bound owners and state only the local delta. When the receiver cannot resolve a referenced owner/version, carry the minimum required semantics locally rather than assuming shared hidden context.

For long/interruption-prone work, keep compact temporary working state: governing snapshot identity, open/closed material obligations, applicable evidence/results and invalidations, blockers/risks/Challenge, and next action. It is derived coordination state, not authority, and should disappear when no longer useful. Reuse it only while its protocol/authority/workplan/candidate/regime/scope remain applicable.

## Local reconciliation, simplification, and urgency

A child role may choose any concretization satisfying its parents/constraints. Removing/consolidating/replacing expected lower machinery with an equivalent concretization is local reconciliation, not redesign. Reopen the parent only when its accepted abstraction or material cycle decision must change.

Generic recurrence/family/simplification rules are owned by [Convergence and development-cycle economy](convergence-and-cycle-economy.md). A first clean local defect remains local. Material sibling recurrence shifts reasoning to the shared owner/mechanism; when structural complexity is implicated, simplify/re-derive delegated machinery before another additive durable repair.

A separately governed urgency/safety/security/reliability/incident requirement may justify a bounded reversible or safely replaceable mitigation before normal simplification. Keep unresolved debt explicit; emergency use never promotes the mitigation into durable authority or manufactures closure.

## Evidence, stages, and impact closure

Evidence semantics are not repeated here. When a material authority/concretization changes, use the evidence owner to identify materially affected descendants/evidence/documentation/dependency/history, preserve unaffected siblings/still-valid evidence, and close each material impact item as resolved, preserved-with-reason, or unavailable/blocking.

Executable D4 stage-local/final acceptance is owned by [Testing and validation](testing-and-validation.md). A coherent material behavior/risk boundary is normally one implementation stage even when several files/functions change. Required stage-local affected regression cannot be deferred merely because a later full suite exists; final assembled acceptance still reflects the candidate after all material executable edits.

## Review, Verification, Stabilization, and Audit

**Review** independently reconstructs governing authority/candidate/evidence applicability and attempts targeted falsification. Missing required pre-Review acceptance remains a blocker; Review does not move those checks later.

**Verification** is a deeper risk-triggered falsification mode for materially high-risk claims; it may reconcile multiple authorities, construct counterexamples, or trace composed D4->D1 behavior. It is not a routine duplicate Review.

**Stabilization / architecture-GC** is a non-mutating convergence-boundary question: would the current concretization still be deliberately chosen for the same governing authority? Required changes return through the owning domain.

**Health Audit** is periodic longitudinal sensing; it routes findings but does not mutate D1-D4 authority.

Every material Review/Verification/acceptance boundary applies the universal Challenge rule. Surface an active Serious Challenge before ordinary blockers or Pass/No-Pass and route it to the earliest affected semantic owner.

## Human gates and closeout

Human gates attach to governed semantic risk, not every transition. The designated human authority is required where project/domain policy assigns ratification/adjudication. Orchestration may represent pending/accepted/rejected state but cannot self-approve it. A visible risk override authorizes only bounded continuation where allowed; dependent outputs remain provisional and cannot close the challenged claim unqualified.

After semantic/functional closure, reconcile only affected current normative documents, guides, generated artifacts, evidence/dependency views, semantic history, workplan state and repository hygiene. Current owners explain what is true; history explains why. Archive/supersede transition artifacts only after their still-current semantics reside in canonical current authority.

Apply the Lossless Representation Rule to workflow artifacts: lead with disposition/Challenge/blockers/current decisions, avoid amendment replay and generic doctrine duplication, keep historical/raw detail cold but discoverable, and preserve every mandatory lower-salience closure condition.
