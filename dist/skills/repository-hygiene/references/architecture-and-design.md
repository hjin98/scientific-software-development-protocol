# Software Architecture and Design (D3)

Own accepted current software architecture: component/state/interface ownership, dependency/data/control flow, persistence/recovery, concurrency, security, resources, deployment and compatibility structure that concretizes applicable D1/D2 semantics and constrains D4.

Universal feasibility/delegation/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md). Generic recurrence/simplification is owned by [Convergence and development-cycle economy](convergence-and-cycle-economy.md); workflow/workplan/Historical Applicability Set semantics by [Workflow and workplans](workflow-and-workplans.md). Project-local learned capabilities are represented by [Project Engineering Memory](project-engineering-memory.md) without becoming D3 authority.

## D3 boundary and feasibility

D3 may own material component/subsystem boundaries, public/internal architectural interfaces, durable representation/state, persistence/recovery/checkpoint structure, concurrency/scheduling/process/service topology, security/trust boundaries, resource/hardware/deployment/compatibility architecture, architecture-level fault/lifecycle behavior, and structure required to preserve D2 semantics.

D3 does not own scientific meaning merely because software implements it, nor numerical-method semantics merely because components execute them. Route equation/estimand/assumption changes to D1 and estimator/discretization/error/precision/stochastic changes to D2.

A D3 candidate is admissible only when it satisfies every applicable D1/D2 invariant and directly governed security, reliability, compatibility, resource, performance/scaling, deployment and external-interface constraint. Among admissible candidates prefer software engineering fitness, then minimum justified total architecture/system complexity, then development economy.

## Current architecture vs cycle decisions

The logical D3 normative family is the **Architecture Manual**: current durable ownership, interfaces, flows and structural boundaries. Each material current architecture claim has one semantic owner.

Keep this separate from workplan cycle freeze. A workplan may fix architecture choices for one concretization cycle without making them durable current architecture. Durable D3 mutation requires the owning acceptance process, including independent falsification before accepted-current promotion where required; later D4 Review cannot retroactively legitimize prematurely promoted architecture.

Functions, helper APIs, wrappers, retries, caches, local algorithms/state machines, exact libraries and current lower-level owner identities remain delegated unless architecture or an external contract makes them invariant.

## Learned capability authority binding

A historical mechanism and a demonstrated **capability** are different things. Project Engineering Memory (PEM) may retain a preservation-capability lesson because history shows that losing the property was costly or that a replacement must consider it. That evidence alone does not make the capability mandatory.

Classify every materially used learned capability as:

- `EVIDENCE_ONLY` — demonstrated project property/design prior; useful evidence, but D3/D4 may replace or omit it when governing authority and current evidence justify doing so;
- `AUTHORITY_BOUND` — exact current D1-D4/project/external owner independently requires the capability; it is mandatory because that owner requires it, not because PEM records it;
- `PROPOSED_FOR_PROMOTION` — evidence suggests the real owner may need amendment; remains non-mandatory until that owner accepts the change through its normal process.

`AUTHORITY_BOUND` records identify the exact current owner/claim. When that owner changes, perform reverse impact reconciliation: confirm/remap the binding, downgrade/reclassify the memory entry, or challenge the owner as appropriate. Frequency, temperature, benchmark success, test survival or historical architecture cannot preserve normative force after the real owner no longer requires the capability.

## Mechanism-to-capability transfer

When replacing/consolidating mature machinery during memory-triggering work, construct a bounded **capability-transfer map** before dependent implementation is treated as closed. For every materially relevant learned capability/HAS item state:

```text
historical capability / evidence
 -> current authority binding (if any)
 -> new mechanism that preserves it, or explicit justified omission/reclassification
 -> acceptance/evidence route under the new concretization
```

Do not preserve obsolete components merely because their tests encode a once-useful property. Preserve owner-required properties and independently justified learned capabilities where they remain applicable; remap evidence to the real current owner. Conversely, do not drop an authority-bound capability merely because the old mechanism is ugly or because a new implementation appears simpler.

A capability-transfer map is cycle evidence/coordination, not a new architecture authority surface. Once the replacement is accepted and current authority/evidence/PEM are reconciled, retire temporary mapping machinery unless project practice gives it continuing value.

## Architecture design test

Prefer cohesive ownership, direct control flow, one authoritative representation/state, acyclic understandable dependencies, and the fewest necessary components/interfaces/synchronization/compatibility paths.

Before D3 acceptance ask whether the architecture preserves all material D2 semantics needed downstream: ordering/reduction, precision, state/restart, reproducibility, data dependencies, error/fallback behavior, and resource/hardware requirements. A locally coherent architecture that permits violation of governing D2 is abstraction-inadequate.

Cross-cutting topics route by semantic effect, not label: parallel arithmetic changing estimator/error -> D2; process/component topology preserving D2 -> D3; thread primitive under unchanged topology -> D4; GPU as required deployment/resource architecture -> D3 while numerical equivalence remains D2; scientifically meaningful units -> D1 while concrete public serialization may be D4.

## Simplicity and recurrence

A solution-created problem remains a cost of delegated concretization; dependence on a helper/wrapper/synchronized state/previous patch does not make that mechanism authority. Apply the convergence owner when recurrence or structural complexity is material.

A first clean local defect may remain local. When sibling recurrence plus wrappers/adapters/retries/fallbacks/special cases, duplicated/synchronized state, competing ownership/reconciliation, lifecycle states created mainly by solution machinery, or another material complexity signal points to a shared mechanism, simplify/re-derive delegated concretization before another additive durable repair. If the required simplification changes accepted D3, reopen D3; if the true defect is D2/D1, route upstream rather than architecture-patching it.

## D3 -> D4 handoff and evidence

A D3->D4 workplan freezes only material D3 decisions needed to bound implementation and states applicable parent/side constraints, delegated D4 space, non-goals, acceptance boundaries and genuine reopen triggers. Affected-surface expansion is not requirement expansion. When PEM is triggered, the handoff also binds the exact accepted/base memory plus branch overlay, records relevant Historical Applicability Set (HAS) dispositions, and includes the capability-transfer obligation where mature machinery is replaced.

Architecture evidence can include dependency/ownership inspection, structural fitness checks, real state/consumer boundaries, recovery/concurrency/security/resource tests, and configuration/deployment checks. Objective stable rules such as dependency direction, acyclicity, independence or absence/uniqueness of a retired owner may be executable. Do not create a universal architecture manifest solely for compliance. Metrics are sensors, not architecture truth.

Evidence lifecycle/applicability is owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); testing methods by [Testing and validation](testing-and-validation.md).

## Review and Stabilization

D3 Review reconstructs governing D1/D2/D3/side constraints and actual D4 behavior, then attempts falsification of ownership, dependency, state, reliability/security, resource/scaling, compatibility and abstraction adequacy. When a replacement uses learned capability evidence, Review independently checks current owner binding and the assembled replacement rather than assuming the historical mechanism or PEM interpretation is correct. D4 violation of coherent D3 is an ordinary D4 blocker. If D3 itself appears contradictory, materially ambiguous, impossible under simultaneous constraints, or incapable of preserving D2, raise Serious Challenge to D3.

At a convergence boundary, Stabilization asks whether the architecture would still be deliberately chosen today for the same governing contract. It is non-mutating; required change returns through the owning domain.

Apply the Lossless Representation Rule to architecture documents: current topology/ownership and decision-critical constraints stay prominent; generic protocol doctrine and historical amendment narrative belong to their owners/cold history rather than being copied into every Architecture Manual.
