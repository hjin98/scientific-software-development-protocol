# Architecture and Design

Architecture exists to help software satisfy the stakeholder's real engineering problem with the lowest justified total system complexity.

Architecture is judged over the material operational and maintenance horizon of the accepted scope. A locally convenient design is not simpler when it knowingly creates avoidable ownership ambiguity, operational fragility, maintenance debt, synchronization burden, or supported-evolution cost. Conversely, stewardship does not justify speculative generalization or unrelated future-proofing.

## Three-tier authority model

The protocol hierarchy is:

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

The hierarchy is lexicographic only after authority is classified correctly.

### Tier 1A: intrinsic product/problem truth

Tier 1A is the stakeholder/domain problem the software must solve: required capability, correctness/scientific invariants, reliability/recovery/security/compatibility, target workload/scaling, CPU/RAM/VRAM/storage/I/O/wall-time limits, target hardware/portability, material latency/throughput, and governed external contracts.

These requirements originate outside the implementation. They constrain every acceptable solution and may be high level. Do not weaken them merely because the current solution is inconvenient.

### Tier 1B: cycle-scoped Frozen architecture

For substantial architecture work, Software Design may deliberately freeze high-level architecture/ownership/algorithm/data-representation/resource/compatibility decisions for the current implementation cycle. This bounds the search space and prevents implementation from continuously reopening settled design.

Tier 1B is solution-derived but temporarily invariant for the cycle. Implementation may not silently change it. Evidence may trigger bounded Design reconsideration; if a Frozen decision is reopened, preserve unrelated accepted design and evidence whose claims remain valid.

### Tier 2: delegated solution machinery

Everything beneath Tier 1A/1B is solution machinery by default: functions, helpers, internal APIs, wrappers, adapters, retries, caches, state machines, synchronization schemes, intermediate representations, local algorithms, implementation-created invariants, and previous patches.

Such machinery does **not** acquire Tier-1 authority merely because it exists, is depended upon, is tested, documented, reviewed, patched, or appears in a previous implementation plan. Correctness of a currently used mechanism is not evidence of necessity of that mechanism.

A detail may be promoted into Frozen architecture only through an explicit Software Design decision supported by material evidence that the architectural commitment is justified.

## Engineering fitness first

Define the Tier-1 engineering envelope before choosing architecture. Reject designs that cannot satisfy it cleanly enough for the actual product. Do not prefer a locally simple architecture that is globally unusable because of poor scaling, excessive resource use, weak hardware utilization, missing capability, scientific error, security weakness, or required compatibility loss.

## Minimum justified product complexity

Among designs satisfying Tier 1, prefer the lowest justified **total product/system complexity**: fewer unnecessary components, states, interfaces, dependencies, synchronization points, duplicated authorities, compatibility paths, runtime/operational stages, special cases, and maintenance burdens.

This is an active product policy, not merely a tie-breaker at initial design time. Necessary specialization remains valid when it protects a real Tier-1 requirement or when one canonical abstraction replaces broader duplicated machinery.

## Quality ratchet and executable architecture fitness

Existing architectural debt does not excuse new debt in a materially touched subsystem. The changed surface should ordinarily leave ownership, dependency direction, state, public/configuration surface, and behavioral protection no harder to reason about unless additional complexity is required by Tier-1/Frozen authority.

Metrics such as complexity, churn, duplication, centrality, CRAP-like measures, or change coupling are sensors rather than architecture truth. Use them to prioritize semantic inspection, especially when risk concentrates where change frequency, structural complexity, test weakness, and architectural centrality overlap.

When an architectural rule is objective, stable, and cheap to encode, prefer an executable fitness check over repeated prose-only review. Suitable examples include forbidden dependency/import direction, layer direction, acyclic package/subsystem relationships, independence constraints, and structural absence/uniqueness of deprecated owners. Do not create a global machine-readable architecture manifest solely for protocol compliance.

## Solution-created problems are not product invariants

An intermediate problem created only by the chosen realization remains Tier 2. For example, if a design creates two synchronized representations, "keep the representations synchronized" is not automatically a new product requirement. An alternative realization that removes one representation can eliminate the intermediate problem while preserving the actual product requirement.

Before adding machinery to repair a Tier-2 problem, distinguish:

1. the original Tier-1 requirement;
2. the Frozen high-level architecture, if any;
3. the lower-level choice that created the intermediate problem; and
4. whether changing/removing/consolidating that choice makes the problem disappear.

Do not preserve a solution merely because later solution code depends on it. Dependency created by a solution is evidence about the cost and shape of that solution, not evidence that the solution became part of the product objective.

## Active complexity restoration

A first clean local defect with a clean local cause receives a direct owning-layer repair. Do not invoke broad redesign merely because alternatives exist.

However, Tier-2 simplification/re-derivation becomes **mandatory before another additive durable repair** when structural evidence shows that the current realization is accumulating unnecessary complexity. Evidence includes materially repeated patches around the same mechanism, patch-on-patch repair, wrappers/adapters/retries/fallbacks/special cases accumulating around one owner, duplicated or synchronized authoritative state, competing authorities, repeated reconciliation machinery, lifecycle/control states primarily managing internal machinery, tests dominated by reimplementing internal orchestration, repeated family closure without reducing the failure surface, or a materially simpler equivalent realization becoming evident.

When triggered, reason in this order:

```text
recover Tier-1 product/problem invariants
-> recover Frozen high-level architecture
-> treat lower-level machinery as replaceable
-> identify problems created only by the current realization
-> remove / narrow / alter / consolidate / refactor where sufficient
-> add machinery only for a genuinely missing required capability
   or when one canonical mechanism replaces broader existing complexity
```

This ordering is semantic, not a mechanical requirement to attempt each verb or minimize lines of code. The burden is against additive preservation of avoidable machinery.

## Justified abstraction and promotion

A new mechanism or abstraction is justified when either:

- Tier 1 requires a capability the simplified existing realization cannot supply cleanly; or
- evidence shows the mechanism is sufficiently general/prevalent across a real problem class that making it canonical replaces multiple authorities, patches, states, or special cases and reduces total system complexity.

Do not promote machinery because hypothetical future uses can be imagined. Promotion from Tier 2 to Frozen architecture requires explicit Design acceptance and a material architectural reason.

## Accepted design and implementation authority

Once a substantial design is accepted, implementation should not repeat the whole architecture search. The workplan distinguishes:

- **Problem/product invariants**;
- **Frozen high-level architecture**;
- **Delegated solution space**; and
- **Reopen only on evidence** assumptions/triggers.

An equivalent local realization that preserves the first two classes remains implementation work even when it removes/consolidates machinery that Design expected but did not freeze. A material redesign changes a Frozen high-level decision and requires Design reconsideration.

Repository evidence may invalidate a Frozen assumption. Treat that as a bounded design-invalidation question rather than silently changing the target or blindly forcing incompatible architecture.

## Recurrence and semantic defect families

Recurrence is evidence about the shared owner/mechanism; it is not evidence that the current realization should survive.

A first clean local defect remains local. Materially equivalent sibling recurrence should stop repeated instance patching and move reasoning to the shared semantic owner/mechanism. If recurrence also exposes structural complexity, the active simplicity rule fires before another additive durable closure.

Use bounded semantic defect families and finite census when the **Tier-1 correctness claim itself** requires completeness, or when sibling discovery is necessary to remove/canonicalize the affected realization safely. Family closure is subordinate to Tier-1 product truth, Frozen architecture, and Tier-2 simplification; it must not turn an accidental mechanism into an invariant merely by completing its current "canonical realization."

Post-simplification recurrence or evidence that a Frozen high-level decision itself is wrong triggers bounded Software Design reconsideration. Reopen only the affected design surface.

## Milestone stabilization / architecture GC

At a material convergence boundary, after ordinary implementation review has otherwise passed, reassess the accepted Tier-2 realization as if it appeared fully formed today. Inspect duplicated representations, competing authorities, wrappers/adapters/fallbacks/special cases, stale compatibility paths, unnecessary states/configuration/public API, ownership leakage, dependency cycles, historical-exception conditionals, dead/bypassed paths, duplicated algorithms, and tests dominated by internal orchestration.

Stabilization is a non-mutating review mode. If the same product/Frozen contract can be realized more simply, route the smallest coherent Tier-2 simplification through the normal Design/Implementation/final-acceptance/review path. If simplification requires changing Frozen architecture, reopen only that affected Design surface.

## Architecture documentation

Permanent architecture documentation describes accepted current product structure, ownership, interfaces, data/control flow, important product/Frozen invariants, persistence/concurrency/security/resource boundaries, target-hardware assumptions where material, and accepted high-level algorithms. Do not turn it into a log of temporary proof machinery, development-process gates, or superseded patches.
