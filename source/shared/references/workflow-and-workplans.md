# Workflow, Change Plans, Handoffs, and Review

Protocol 6.1 uses recursive abstraction–concretization rather than one mandatory linear lifecycle. Read [Abstraction, concretization, authority, and challenge](abstraction-and-realization.md) as the governing semantic model and [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for evidence/dependency/history semantics.

Workplans, gates, reviews, tests, and process stages are coordination/evidence mechanisms, **not terminal objectives**. They are bounded by explicit stakeholder requirements, accepted domain authority, and the affected semantic scope and **must never create pressure to manufacture a pass**.

## Background and terminology

A **concretization** is a downstream scientific, numerical, architectural, specification, or implementation choice constrained by governing abstractions. An **evidence realization** is instead one concrete execution of an evidence specification. Protocol 6.1 reserves these terms for those distinct relations.

## Roles and semantic domains

The authority-bearing roles are:

```text
D1 scientific-formulation
    -> D2 numerical-algorithm-design
        -> D3 software-design
            -> D4 software-implementation
```

This is a semantic ordering, not a required four-stage waterfall. A local implementation refactor can remain D4-only after a proportionate upstream-impact exclusion. A software-architecture change can be D3->D4. A numerical change can begin at D2. A scientific formulation change begins at D1 and concretizes downward only through materially dependent descendants.

Supporting capabilities such as `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` are not authority-bearing approval roles. The software-local subcycle remains `software-design -> software-implementation` at D3->D4; it does not own D1/D2.

## Start at the highest potentially affected domain

Before mutation classify:

1. the earliest/highest accepted abstraction whose semantics may materially change;
2. every applicable domain-local governed external constraint; and
3. the dependent semantic/evidence surface below it.

Route by semantic effect rather than topic. A parallel-reduction change that can alter estimator meaning is D2 even if implemented in C++; a process-topology change with unchanged numerical semantics is D3; a mutex replacement under unchanged architecture is D4.

Do not escalate merely because many files are affected. Do not keep work artificially low when evidence shows the parent abstraction is wrong. Reopen only the affected semantic surface and do not reopen unrelated design.

## Typical workflows

**Small/local executable work may look like**:

```text
inspect -> implement -> conformance + affected regression -> integration -> done
```

Substantial work normally behaves like:

```text
classify highest affected domain
  -> design/diagnose at that domain when needed
  -> freeze only material child-abstraction decisions
  -> coherent material concretization/implementation stage
       -> semantic/conformance closure
       -> focused + affected regression
  -> active simplification if structural complexity triggers fire
  -> final accepted-contract reconciliation
  -> re-derive final affected semantic/evidence surface
  -> final affected regression + integration + project-required checks
  -> independent Review when warranted
  -> deeper Verification only when high-risk claims warrant it
  -> Stabilization / architecture-GC at material convergence boundaries when warranted
  -> documentation + dependency/history + repository closeout when affected
```

These are patterns, not fixed gate counts. Production qualification is appended only when independently required.

## Workplans as bounded implementation contracts

Use a change plan/workplan when it materially reduces rediscovery, ambiguity, sequencing risk, cross-domain drift, or downstream rework. Workplans remain subordinate to the protected stakeholder/domain outcome and are not proof scripts.

A substantial handoff separates:

1. **governing parent/problem invariants and side constraints**;
2. **cycle-scoped child decisions** deliberately fixed for the current concretization cycle; and
3. **delegated concretization space** that remains replaceable, reducible, consolidatable, or deletable while the first two classes remain satisfied.

A D3->D4 executable workplan is a specialization of this generic abstraction-concretization handoff, not a separate philosophy. A **suggested concretization does not become a cycle-scoped or durable authority** merely because Design discussed or documented it.

For material obligations preserve as applicable: concern/rationale, required end state, required constraints/preservation/forbidden behavior, useful expected owning/affected surface, task-specific acceptance evidence, and stage/dependency where material. Attach a suggested concretization, proxy-proof acceptance boundary, or anti-shortcut only when it materially improves correctness.

The accepted plan is the minimum known contract, not a ceiling only for **newly discovered affected behavior** and logically necessary consequences of already-binding authority. Affected-surface expansion is not requirement expansion.

## Durable current authority versus cycle-scoped freeze

Keep two concepts distinct:

- **accepted-current domain authority** is the durable current semantic owner in D1, D2, D3, or D4;
- **cycle-scoped concretization freeze** is the subset of child-concretization decisions a change plan fixes to bound one implementation/design cycle.

A cycle-scoped decision does not become durable scientific, numerical, architectural, or specification authority merely because a workplan froze it. Durable authority must be explicitly accepted by the owning domain. Conversely, a workplan cannot ignore already-current authority merely because it is not restated in the cycle freeze.

## Snapshot-complete handoff

The accepted current handoff artifact set must recover every still-binding task-specific invariant, applicable side constraint, cycle-scoped decision, non-goal, material acceptance boundary, authority state, evidence/dependency obligation, and genuine reopen trigger without requiring prior chat or hidden Git history.

Current composition can span multiple supplied artifacts. Do not copy generic protocol doctrine into every plan. Use the snapshot-loss counterfactual: if `.git`, old discussions, and superseded revisions disappear, can a competent implementer still reconstruct the complete governing contract from the supplied current authority?

If not, the handoff is deficient.

## Compact resumable working state

For long, interruption-prone, multi-session, or materially handed-off work, maintain compact temporary coordination state sufficient to resume without hidden chat/history or needless rediscovery. Capture only what materially helps continuation: the current governing snapshot, open/closed obligations, material evidence/results and known invalidations, unresolved blockers/risks/Serious Challenges/reopen triggers, and the next action.

This working state is coordination machinery, **not normative authority**. It should disappear when no longer useful. Do not create a permanent ledger, database, manifest, or parallel requirements/evidence system solely to satisfy resumability.

## Concretization and bounded local reconciliation

A child role may choose any concretization that satisfies every applicable parent and side constraint. Existing helpers, wrappers, algorithms, APIs, processes, caches, states, and prior patches remain replaceable unless explicitly accepted as authority.

**Local reconciliation** may remove, consolidate, or replace an expected lower-level mechanism with an **equivalent local concretization** when governing semantics survive. Reopen the parent only when evidence shows a governing abstraction or cycle-scoped decision must change. Reopen only the affected semantic surface.

A workplan's suggested concretization is not automatically authoritative. Newly discovered affected behavior must be incorporated, but discovery does not mint unrelated authority.

## Active simplicity and recurrence

A **first clean local defect remains local**. It does not require a census merely because variants are imaginable.

**Material sibling recurrence** changes the unit of reasoning to the **shared owner/mechanism**. Recurrence is evidence about the shared semantic owner or mechanism, not proof that the current concretization must survive. Material sibling recurrence plus structural complexity triggers simplification/re-derivation before another additive durable repair.

When repeated patches, wrappers, fallbacks, synchronized representations, competing authorities, special cases, repeated reconciliation, or an evident materially simpler equivalent concretization show structural complexity, **active simplification/re-derivation of delegated concretization is required** before adding another durable repair.

If post-simplification recurrence or evidence shows the accepted parent abstraction or a material cycle-scoped decision is wrong, route bounded reconsideration to the earliest affected D1-D3 owner. **No recurrence/review count can force acceptance**; escalation changes the engineering method, not the pass threshold.

### Bounded urgent mitigation

When an independently governed urgency, safety, security, reliability, or incident-containment constraint requires immediate action, a **bounded reversible or safely replaceable mitigation may precede the normal simplification/re-derivation pass**. Keep unresolved structural debt/risk explicit, do not let emergency use promote the mitigation into durable authority, and reconcile the owning concretization/abstraction at the earliest safe point. Urgency changes sequencing; it does not authorize counterfeit closure or permanent patch accretion.

**Ordinary implementation attempts and review cycles do not require a numbered authority revision** unless accepted task semantics actually change.

## Verification at each boundary

Every material handoff evaluates both:

1. **concretization fidelity** — does the child satisfy every applicable parent and side constraint?; and
2. **abstraction adequacy** — does the child abstraction preserve enough upstream meaning to constrain its own descendants safely?

Verification reconstructs actual child semantics and attempts falsification. It is not a bijective inverse of Design and finite evidence does not prove total semantics.

Material review/verification includes the bounded Challenge Pass from [Abstraction, concretization, authority, and challenge](abstraction-and-realization.md). An ordinary child defect under a coherent parent is a blocker. Evidence that accepted authority itself may be contradictory, materially ambiguous, false, inadequate, or impossible to concretize is a **Serious Challenge** requiring explicit adjudication.

## Human ratification

Human gates attach to semantic risk, not every domain transition. D1 and scientifically consequential D2 decisions normally require designated human adjudication when they change scientific meaning, governing models/assumptions, material algorithm guarantees, or error/tolerance semantics capable of changing conclusions.

The orchestrator may represent pending/accepted/rejected human state but may not self-approve a human-owned decision. A human risk override is visible authorization to continue with unresolved risk; it is not epistemic resolution and cannot be used to release Protocol 6.1 itself under an unresolved governing Serious Challenge.

Any dependent descendant created while that override remains active is risk-accepted/provisional for the challenged claim. Preserve that state through downstream handoffs/results; unaffected siblings may close normally, but dependent work may not silently reset to accepted-current or emit an unqualified Pass/complete result.

## Bounded invalidation and stale descendants/evidence

When accepted authority changes:

```text
accept upstream change
 -> identify materially dependent descendants/evidence
 -> mark only those descendants/evidence review-required or stale
 -> preserve unrelated siblings and still-valid evidence
 -> concretize downward as needed
 -> realize required evidence again
 -> verify upward across the affected surface
```

Use existing document links, workplan references, section anchors, profile metadata, and bounded Markdown dependency records before inventing a registry or claim database. Absence of an edge in an incomplete map is not proof of independence.

## Manual impact closure

For a material authority/concretization change, workplan/review impact reasoning should account proportionately for:

```text
changed authority/concretization
 -> affected descendant authority/concretizations
 -> affected evidence specifications/realizations
 -> affected documentation/current dependency view
 -> required human re-ratification where applicable
 -> required revalidation/retirement/semantic-history update
```

Before closure, every material impact item must be resolved, preserved as still-valid with reason, or explicitly unavailable/blocking. Old green tests are never a substitute for impact closure.

## D4 executable implementation acceptance

Executable D4 changes retain strict functional closure. Each material behavior-changing implementation stage needs:

- semantic/conformance closure against the accepted D4 specification, D3 architecture, and directly applicable constraints;
- focused checks appropriate to the changed mechanism;
- stage-local affected regression before dependent executable work proceeds, unless a genuinely non-executable intermediate stage must combine with the nearest executable stage.

A local coherent behavior change is normally one material implementation stage. **Several tightly coupled edits may close under one stage** when they form one coherent behavior/risk boundary; they do not become separate stages merely because they touch separate files/functions.

**Green tests never prove an omitted obligation was implemented. Silent omission is not an accepted state.**

Final assembled acceptance requires:

1. reconcile the complete accepted contract;
2. inspect obsolete/bypassed/duplicate ownership and material complexity drift;
3. re-derive the affected behavioral/semantic/evidence surface from the final candidate;
4. run the complete affected-surface regression;
5. run integration/end-to-end paths through the real semantic owner/consumer boundaries;
6. run repository/project-required checks;
7. close material evidence/dependency/history impacts or record them unavailable/blocking.

Full production qualification is separate. A production run does not replace regression or integration.

## Proxy-proof semantic-owner evidence

When material acceptance depends on a real owner/path, identify the **real production owner/consumer boundary** constituting the claim and the allowed lower test-double boundary. At every layer, evidence must exercise the actual semantic owner. A test, derivation, benchmark, or review that could stay green while the real formulation/method/architecture/implementation owner is materially wrong cannot close that owner claim.

For D4 integration, bounded doubles are valid below or outside the semantic owner under acceptance. Do not mock, bypass, precompute, or substantially reimplement the owner whose behavior constitutes the claim. Exact lower-owner identity remains delegated unless parent/domain authority makes it an invariant.

When delegated owner identity changes under equivalent semantics, owner-specific prior evidence may become stale while the higher-level evidence specification remains valid. Remap and rerun rather than preserving obsolete machinery for the test.

## Independent Review, Verification, Stabilization, and Audit

**Review** reconstructs the governing contract and candidate behavior, then attempts targeted falsification. Review readiness follows final accepted-contract reconciliation, final affected regression/integration, real-boundary checks, material impact closure, and repository/project-required checks. Missing required implementation/evidence acceptance remains a blocker, not a reason to move checks after Review.

**Verification** is a deeper optional, risk-triggered mode for materially high-risk claims. It may reconcile several authorities, construct counterexamples, compare reference methods, or inspect composed D4->D1 closure. It does not replace ordinary Review.

**Stabilization / architecture-GC** is a non-mutating milestone review of whether the accepted concretization remains the minimum justified system. Required changes re-enter the owning domain; stabilization is not an extra approval authority.

**Health Audit** is periodic longitudinal sensing. It may route findings but does not mutate D1-D4 authority.

## Review outputs and routing

Before ordinary blockers or Pass/No-Pass language, surface any active Serious Challenge prominently. Otherwise classify findings by earliest owning domain:

- D4 concretization nonconformance -> `software-implementation`;
- D3 architecture deficiency -> `software-design`;
- D2 numerical/algorithm deficiency -> `numerical-algorithm-design`;
- D1 scientific/mathematical deficiency -> `scientific-formulation`;
- documentation-only drift -> `software-documentation` support;
- lifecycle residue -> `repository-hygiene` support.

Equivalent preferences without material engineering benefit are not blockers.

## Closeout

After semantic/functional closure, reconcile current normative documents, guides, generated artifacts, dependency/evidence views, semantic-evolution history where triggered, workplan state, and conservative repository hygiene. Closeout must not mutate product semantics. Archive/supersede completed transition artifacts only after their accepted semantics are represented by current canonical authority.
