# Software Architecture and Design (D3)

D3 owns software architecture: the accepted structural abstraction that realizes applicable D1/D2 semantics and domain-local governed engineering constraints while constraining D4 specification/implementation.

Read [Abstraction, realization, authority, and challenge](abstraction-and-realization.md) first for the protocol-wide authority model.

## D3 boundary

D3 may own material decisions about:

- component/subsystem ownership and dependency direction;
- public/internal architectural interfaces and extension boundaries;
- data/control flow and durable representation architecture;
- persistence/recovery/checkpoint architecture;
- concurrency/scheduling/process/service topology;
- security/trust boundaries;
- resource/hardware/deployment/compatibility architecture;
- architecture-level fault handling and lifecycle;
- architecture choices required to preserve D2 computational semantics.

D3 does **not** own the scientific model merely because software implements it, and does not own the numerical algorithm merely because components execute it. Route a change in equation/estimand/assumption to D1 and a change in estimator/discretization/error/precision semantics to D2.

## Governing feasibility

A D3 candidate is admissible only when it satisfies every applicable upstream D1/D2 claim and every domain-local governed constraint such as security, reliability, compatibility, target hardware, resource limits, performance/scaling, deployment, and external API obligations.

Among admissible architectures prefer:

```text
software engineering fitness
> minimum justified total architecture/system complexity
> development economy
```

A locally simple architecture that violates numerical fidelity, resource bounds, security, reliability, or a public contract is outside the feasible set.

## Architecture Manual

The logical D3 normative document family is the **Architecture Manual**. It describes accepted current ownership, interfaces, data/control flow, persistence/concurrency/security/resource boundaries, and material architecture decisions. Each material architecture claim has one current semantic owner.

Keep current architecture separate from workplan-specific cycle freeze. A workplan can freeze a solution decision for one realization cycle without making it permanent architecture. Promote it into the Architecture Manual only when D3 deliberately accepts it as durable current structure.

## Minimum justified architecture

Prefer cohesive ownership, direct control flow, one authoritative representation/state, acyclic understandable dependencies, and the fewest necessary components/interfaces/synchronization points/compatibility paths.

A first clean local defect can receive a direct repair. Before another additive durable repair, mandatory simplification/re-derivation is triggered by structural evidence such as:

- patch-on-patch repair around one owner;
- accumulating wrappers/adapters/retries/fallbacks/special cases;
- duplicated or synchronized authoritative state;
- competing ownership or reconciliation machinery;
- lifecycle states existing mainly to manage solution-created machinery;
- tests dominated by reimplementing internal orchestration;
- an evident materially simpler architecture satisfying the same authority.

When triggered:

```text
recover applicable parent invariants and external constraints
 -> identify cycle-scoped D3 decisions
 -> treat lower realization as replaceable
 -> remove / narrow / alter / consolidate / refactor where sufficient
 -> add machinery only for a genuinely missing capability
    or when one canonical mechanism replaces broader complexity
```

Do not simplify by weakening D1/D2 semantics or governed engineering constraints.

## Solution-created problems and recurrence

A problem created only by delegated realization remains a realization problem. Dependency on a helper, wrapper, synchronized representation, state machine, or previous patch is evidence about that realization's cost and shape; it does not make the mechanism an invariant.

A first clean local defect remains local. **Recurrence is evidence about the shared owner/mechanism**, not evidence that the current realization should survive. Material sibling recurrence changes the unit of reasoning to that shared owner/mechanism. If recurrence also exposes accumulating complexity, simplify/re-derive delegated realization before another additive repair.

## Cross-cutting concerns route by semantic effect

Topic names do not determine domain ownership.

- Parallel summation that changes estimator/error semantics -> D2.
- Parallel process/component topology preserving D2 semantics -> D3.
- Thread primitive inside unchanged topology -> D4.
- GPU support as a required deployment/resource architecture -> D3, while accepted numerical equivalence/error semantics remain D2.
- Units/observable meaning -> D1 when scientifically semantic; concrete public serialization of those units -> D4 specification.

## D2 -> D3 abstraction adequacy

Before D3 acceptance, challenge whether the architecture preserves all D2 semantics needed downstream: ordering/reduction, precision, state/restart behavior, reproducibility, data dependencies, error/fallback semantics, and target resource/hardware constraints where material.

An architecture can satisfy its own local diagrams while being too weak to preserve the numerical method. That is a D3 abstraction-adequacy defect.

## D3 -> D4 handoff

A D3->D4 implementation workplan should freeze only material architecture decisions needed to bound implementation. It should state accepted D3 invariants, applicable side constraints, delegated D4 realization space, non-goals, task-specific acceptance boundaries, and genuine redesign/simplification triggers.

Functions, helper APIs, wrappers, retries, caches, local algorithms, internal state machines, exact library choices, and current acceptance-owner identity remain D4-delegated unless architecture or a governed contract explicitly requires them.

Affected-surface expansion is not requirement expansion. Additional callers/configuration/persistence/tests may need implementation or validation without becoming new architecture authority.

## Architecture fitness evidence

When an architectural rule is objective, durable, and cheap to encode, an executable fitness check may protect it—for example dependency direction, acyclicity, forbidden imports, independence, or structural absence/uniqueness of a retired owner. Do not create a universal architecture manifest solely for protocol compliance.

Metrics such as complexity, churn, duplication, coverage, and centrality are sensors, not architecture truth. Investigate the semantic reason behind a signal before changing authority.

## Review and Serious Challenge

D3 Review reconstructs applicable D1/D2 semantics, D3 architecture, side constraints, and actual D4 behavior. It attempts targeted falsification of ownership, dependency, state, reliability, security, scaling/resource, compatibility, and abstraction-adequacy claims.

If D4 fails a coherent D3 contract, route an ordinary blocker to D4. If D3 itself appears contradictory, materially ambiguous, unrealizable under its simultaneous constraints, or incapable of preserving D2 semantics, raise a Serious Challenge to D3 rather than adding a D4 workaround.

At a convergence boundary, stabilization asks whether the architecture would still be deliberately chosen today for the same governing contract. If not, route the smallest coherent D3 simplification or upstream reconsideration; do not accrete another compatibility layer automatically.
