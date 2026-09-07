# Long-Horizon Code Health and Autonomous Quality

Use this reference when a task materially concerns maintainability drift, test-oracle strength, adversarial verification, stabilization, architecture fitness, changed-code quality, failure-path evidence, or periodic repository health.

## Authority and scope

Long-horizon quality strengthens the existing Protocol 5 control loop. It does not create new product truth, a third approval role, or a numeric definition of quality.

```text
product/Frozen authority
    -> implementation + executable evidence
    -> independent review / risk-triggered verification
    -> structural and test-effectiveness signals
    -> stabilization / longitudinal health sensing
    -> bounded simplification or Design reconsideration
```

Review, Verification, Stabilization, Health Audit, qualification, documentation, and hygiene are modes or supporting capabilities under the existing `software-design -> software-implementation` lifecycle.

## Quality ratchet

Existing debt does not excuse new debt. A materially touched subsystem should ordinarily leave the repository no harder to reason about, no more weakly protected, no more cyclic, no more duplicated in authority, and no more dependent on special-case machinery unless the additional complexity is required by product/Frozen authority.

This is a semantic ratchet, not a repository-wide score. For substantial or structurally risky work, establish only the task-local baseline needed to compare relevant before/after properties. Useful evidence can include affected dependency structure, important real-owner tests, selected complexity/hotspot observations, reference numerical behavior, public/configuration surface, known recurring defects, and candidate identity. Do not create a permanent health ledger solely for protocol compliance.

## Metrics are sensors, not verdicts

Complexity, CRAP-like measures, churn, change coupling, dependency centrality/cycles, duplication, coverage, mutation survival, public/configuration surface growth, and related metrics may identify where engineering attention has high expected value. They do not independently prove correctness, architectural fitness, or a required refactor.

Prefer risk concentration over raw complexity. A useful conceptual model is:

```text
maintenance risk ~ change frequency x structural complexity x test weakness x architectural centrality
```

No exact formula or universal threshold is normative. Investigate the semantic reason behind a signal before acting.

## Test effectiveness and oracle strength

Coverage answers whether code executed, not whether the test oracle can reject materially wrong behavior. For important decision logic, boundary-heavy code, historically escaped defects, high-risk changed code, or suspiciously weak assertions, ask:

> What is the smallest plausible semantically wrong implementation that could still pass these tests?

When that counterexample is material and economically testable, strengthen the oracle. Useful methods include:

- mutation testing or equivalent semantic perturbation;
- counterfactual known-broken versus corrected behavior;
- property/stateful testing;
- differential comparison against a trusted/reference implementation;
- metamorphic relations where exact expected values are difficult;
- real-owner integration that cannot remain green while the semantic owner is broken.

Mutation testing is conditional. Surviving mutants are investigation evidence; they may reflect weak assertions, untested decisions, dead/equivalent code, or ambiguous requirements. Do not require 100% mutation scores or optimize tests for a score rather than product behavior.

## Differential and metamorphic evidence

Use differential testing when two independently justified realizations should agree on governed observables. Use metamorphic testing when a controlled transformation implies a relation on outputs even when a complete fixture oracle is difficult.

Examples include:

- restart/continuation versus uninterrupted execution equivalence;
- permutation-invariant aggregate statistics;
- unit-consistent transformation;
- translation/rotation symmetry or equivariance where physically valid;
- normalized-weight rescaling that should preserve ranking;
- reference versus optimized/backend equivalence within justified tolerance.

The relation itself must come from product/scientific authority; do not invent invariants merely because they are easy to test.

## Executable architecture fitness

When an architectural rule is objective, stable, and cheap to encode, prefer an executable fitness check over repeated prose-only review. Suitable claims can include:

- forbidden dependency/import direction;
- layer direction;
- acyclic package/subsystem relationships;
- independence constraints;
- absence/uniqueness of a deprecated owner/path;
- one authoritative representation where duplicate ownership would be a defect.

Do not build a global machine-readable architecture model solely for protocol compliance. Encode only rules with durable semantic value and clear ownership.

## Changed-code and affected-surface quality

When suitable project tools exist, use changed-code/affected-surface observations as ratchets rather than requiring a legacy repository to satisfy arbitrary global thresholds immediately. Material questions include:

- is new/modified important behavior behaviorally protected;
- did the change introduce a new dependency cycle or objective architecture violation;
- did it create an unexplained high-complexity hotspot;
- did it expand public/configuration surface without product/Frozen need;
- did it weaken an important oracle when mutation/counterfactual evidence is available.

A metric change triggers semantic inspection. It does not become an automatic pass/fail threshold unless project authority explicitly adopts one.

## Review, Verification, Stabilization, and Health Audit

Keep these modes distinct.

### Review

Independent implementation Review is a Software Design mode. It evaluates a candidate after normal Implementation completion evidence: final accepted-contract reconciliation, final affected-surface regression, real-boundary integration, and repository/project-required checks, or explicitly reports missing evidence as a blocker. Reconstruct the governing contract independently and attempt to falsify important implementation claims rather than merely repeating the implementer's rationale.

Prefer a fresh context/model instance when practical. Do not require hidden chain-of-thought transfer or permanent review manifests.

### Verification

Verification is a deeper optional Software Design mode for materially high-risk scientific, numerical, product, or architectural claims. It may reconcile multiple documented authorities, construct counterexamples, compare references, exercise metamorphic relations, or inspect production paths more broadly than ordinary workplan review. It does not replace Review and is not mandatory for routine changes.

### Stabilization / architecture GC

At a material convergence boundary, after ordinary implementation review has otherwise passed, ask:

> If this implementation appeared fully formed today, would we deliberately choose this realization again for the same product/Frozen contract?

Inspect duplicate representations, competing authorities, wrappers/adapters/fallbacks/special cases, stale compatibility paths, unnecessary states/configuration/public API, ownership leakage, dependency cycles, historical exception conditionals, dead/bypassed paths, duplicated algorithms, and tests dominated by internal orchestration.

Stabilization is non-mutating. If Tier-2 simplification is justified, route the smallest coherent change through the normal Design/Implementation/acceptance/review path. If Frozen architecture must change, reopen only the affected Design surface.

### Health Audit

A periodic Health Audit examines longitudinal repository risk rather than feature conformance. Combine semantic inspection with available history such as churn, temporal change coupling, recurring defect families, complexity, dependency centrality/cycles, public/configuration growth, test weakness, and documentation difficulty.

Do not fabricate trends from a static snapshot. If VCS/history evidence is unavailable, report static risks and downgrade or omit longitudinal claims.

A Health Audit may route findings but does not define Frozen architecture or accept implementation contracts. Local Tier-2 repairs may proceed under existing authority; substantial/new workplans and Frozen-architecture concerns route to Software Design. Documentation drift routes to `software-documentation`; lifecycle residue routes to `repository-hygiene`.

## Bounded failure injection

For persistence, restart, orchestration, recovery, or failure-propagation claims, happy-path coverage can be misleading. When material, use deterministic bounded fault injection or equivalent simulation at the real semantic owner boundary. Representative cases include:

- interrupted checkpoint publication or truncated artifacts;
- stale/missing cache state;
- restart at material transition boundaries;
- controlled worker/task death;
- controlled I/O failure;
- duplicate callback/event delivery;
- partial transition state.

Prefer bounded simulation over resource exhaustion or indiscriminate chaos. The production recovery/state owner must still execute; a harness that reimplements the recovery algorithm is not proxy-proof evidence.

## Closeout and temporal maintenance

Long-term coherence also depends on lifecycle convergence. At substantial workplan/release completion, reconcile affected current documentation, archive/close completed workplans according to repository policy, and perform conservative repository hygiene. Do not delete branches/files or alter product semantics merely because closeout is due.

Periodic maintenance should be scheduled by engineering value, not by a fixed per-change gate count. The objective is earlier detection of entropy and weak evidence while the repair surface is still small.
