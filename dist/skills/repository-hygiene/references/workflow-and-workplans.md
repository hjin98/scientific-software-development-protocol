# Workflow, Change Plans, Handoffs, and Review

Own workflow/lifecycle, workplan, handoff, review sequencing, resumability, Historical Applicability Set (HAS), project-learning closeout, and closeout semantics. Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence applicability/dependency/evolution is owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); testing/acceptance methods are owned by [Testing and validation](testing-and-validation.md); Project Engineering Memory (PEM) representation is owned by [Project Engineering Memory](project-engineering-memory.md).

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

## Conditional project-memory activation and HAS

PEM is decision support, not a mandatory workflow stage. Activate it only when demonstrated project history can materially change the decision: substantial rework of mature D1-D4 semantics/concretization; replacement/consolidation of mature machinery; suspected recurrence; substantial optimization/scaling; migration/recovery/revert/restoration where prior choices matter; or an active workplan explicitly binding relevant memory. A first clean local defect, trivial/unrelated work, or mere presence of a PEM file does not trigger substantive memory loading.

For a memory-triggering task:

1. resolve the **accepted/base PEM** from project integration/Git policy, never from default/latest/timestamp/self-declaration;
2. validate the supported schema and compose any explicit validated same-branch candidate overlay;
3. record the exact accepted/base and overlay identities used for the current decision;
4. read the compact active summary, then perform bounded metadata-level applicability matching across canonical current entries, not only `HOT` or summary-visible entries;
5. record a HAS entry for every materially relevant family/capability/notice surfaced or independently known, with `APPLICABLE`, `NOT_APPLICABLE`, or `REVIEW_REQUIRED` plus reason;
6. load raw family/evidence detail only where needed to decide or falsify the disposition;
7. identify overlapping incompatible guidance and preserve the governing regime/tradeoff/current-owner priority or contested state;
8. when mature machinery is replaced, map demonstrated learned capabilities to the current authority binding and new mechanism/justified omission.

Missing/partial PEM, a stale/missing derived index, an absent dependency edge, or stale applicability metadata cannot prove historical absence/non-applicability. Perform bounded historical intake over the affected scope when necessary or preserve explicit `REVIEW_REQUIRED` uncertainty. Memory temperature is salience only and cannot determine HAS applicability.

If the target accepted memory, candidate overlay, or a governing current owner materially advances before integration/closeout, reconcile the changed interval/affected surface and refresh materially affected HAS dispositions. A HAS derived from an obsolete basis cannot silently close current work.

## Lossless handoff and resumable state

A current handoff must be snapshot-complete for its **governed task scope**: recover still-binding task-specific invariants/constraints, cycle decisions, non-goals, material acceptance/evidence obligations, authority state, unresolved blockers/Challenge and genuine reopen triggers without hidden chat or unavailable history. A memory-triggering handoff additionally records its exact PEM basis/overlay and current HAS dispositions; it does not replay the project-memory corpus.

Do **not** copy generic protocol doctrine into every handoff. Point to resolvable version-bound owners and state only the local delta. When the receiver cannot resolve a referenced owner/version, carry the minimum required semantics locally rather than assuming shared hidden context.

For long/interruption-prone work, keep compact temporary working state: governing snapshot identity, open/closed material obligations, applicable evidence/results and invalidations, blockers/risks/Challenge, and next action. It is derived coordination state, not authority, and should disappear when no longer useful. Reuse it only while its protocol/authority/workplan/candidate/regime/scope remain applicable.

## Local reconciliation, simplification, and urgency

A child role may choose any concretization satisfying its parents/constraints. Removing/consolidating/replacing expected lower machinery with an equivalent concretization is local reconciliation, not redesign. Reopen the parent only when its accepted abstraction or material cycle decision must change.

Generic recurrence/family/simplification rules are owned by [Convergence and development-cycle economy](convergence-and-cycle-economy.md). A first clean local defect remains local. Material sibling recurrence shifts reasoning to the shared owner/mechanism; when structural complexity is implicated, simplify/re-derive delegated machinery before another additive durable repair.

A separately governed urgency/safety/security/reliability/incident requirement may justify a bounded reversible or safely replaceable mitigation before normal simplification. Keep unresolved debt explicit; emergency use never promotes the mitigation into durable authority or manufactures closure.

## Evidence, stages, and impact closure

Evidence semantics are not repeated here. When a material authority/concretization changes, use the evidence owner to identify materially affected descendants/evidence/documentation/dependency/history, preserve unaffected siblings/still-valid evidence, and close each material impact item as resolved, preserved-with-reason, or unavailable/blocking. If a materially depended-on PEM entry changes, perform the bounded transitive/reverse impact closure required by its canonical owners and refresh affected HAS state.

Executable D4 stage-local/final acceptance is owned by [Testing and validation](testing-and-validation.md). A coherent material behavior/risk boundary is normally one implementation stage even when several files/functions change. Required stage-local affected regression cannot be deferred merely because a later full suite exists; final assembled acceptance still reflects the candidate after all material executable edits.

## Review, Verification, Stabilization, and Audit

**Review** independently reconstructs governing authority/candidate/evidence applicability and attempts targeted falsification. Missing required pre-Review acceptance remains a blocker; Review does not move those checks later. When PEM is material, Review treats it as a high-information hypothesis index and independently verifies current owners/assembled behavior rather than inheriting its conclusions.

**Verification** is a deeper risk-triggered falsification mode for materially high-risk claims; it may reconcile multiple authorities, construct counterexamples, or trace composed D4->D1 behavior. It is not a routine duplicate Review.

**Stabilization / architecture-GC** is a non-mutating convergence-boundary question: would the current concretization still be deliberately chosen for the same governing authority? Required changes return through the owning domain.

**Health Audit** is periodic longitudinal sensing; it routes findings but does not mutate D1-D4 authority or self-admit them into PEM.

Every material Review/Verification/acceptance boundary applies the universal Challenge rule. Surface an active Serious Challenge before ordinary blockers or Pass/No-Pass and route it to the earliest affected semantic owner.

## Human gates and closeout learning

Human gates attach to governed semantic risk, not every transition. The designated human authority is required where project/domain policy assigns ratification/adjudication. Orchestration may represent pending/accepted/rejected state but cannot self-approve it. A visible risk override authorizes only bounded continuation where allowed; dependent outputs remain provisional and cannot close the challenged claim unqualified.

After every accepted material repair/rework/optimization/revert/restoration, perform a **closeout learning assessment** before declaring repository/lifecycle closure. Ask whether a known failure family genuinely recurred after accepted repair; a success pattern gained a supporting, neutral, contradicting, inconclusive, rejected/invalid application episode; an episode is genuinely new rather than another surface/run of one coordinated intervention; a material evidence provenance cluster limits independence; a reusable discovery/capability emerged; evidence narrowed/retired/invalidated an existing lesson; maturity/comparative claim strength changed; overlapping guidance acquired a conflict/tradeoff boundary; coverage/aggregation/project scope or binding health changed; a notice expired; causal attribution changed; a PEM dependency or accepted-memory basis advanced; or schema/base/overlay reconciliation is needed.

Update PEM only when its admission threshold is met or an existing current entry materially changes. Ordinary fix chronology and first-clean local defects remain out of permanent memory. Documentation/audit/orchestration may surface candidates, but the appropriate current owner and admissible evidence govern the update; no specialist can self-promote findings into authority.

After semantic/functional closure, reconcile only affected current normative documents, guides, generated artifacts, evidence/dependency views, PEM when triggered, semantic history, workplan state and repository hygiene. Current owners explain what is true; PEM summarizes evidence-backed project learning; history explains why. Archive/supersede transition artifacts only after their still-current semantics reside in canonical current authority/state.

Apply the Lossless Representation Rule to workflow artifacts: lead with disposition/Challenge/blockers/current decisions, avoid amendment replay and generic doctrine duplication, keep historical/raw detail cold but discoverable, and preserve every mandatory lower-salience closure condition.
