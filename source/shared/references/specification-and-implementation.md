# D4 Specification and Implementation

D4 owns concrete stable software behavior plus executable concretization. It is constrained by accepted D3 architecture, applicable upstream D1/D2 semantics that reach D4, and directly governed external contracts.

Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence lifecycle in [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); executable acceptance methods in [Testing and validation](testing-and-validation.md).

## Specification versus code

Where concrete behavior is governed, the accepted **D4 Specification** states intended software behavior; code/executable behavior is the concretization and evidence of what actually exists.

```text
accepted D4 specification --constrains--> executable behavior
accepted D4 specification <--verify----- executable behavior
```

Code does not become intended contract through existence or test capture. If code and accepted specification disagree, classify first: repair wrong code; update a genuinely stale specification only after accepted authority changed; route ambiguous intent; Serious Challenge a materially defective accepted specification. Never rewrite the specification merely to make unintended code pass.

Specify only stable consumer/automation/persistence/scientific-interpretation contracts such as public API/CLI/config behavior, formats/schemas/units/shapes/order/precision, persistence/restart/migration, compatibility/supported versions, public backend/device policy, durable error/fallback behavior, externally observable state transitions, and authorization/security behavior. Private helpers/call graphs/data structures remain delegated unless genuinely governed.

## Adaptive implementation

Within the feasible specification/architecture/upstream/external envelope, D4 remains adaptive. Prefer direct flow, cohesive ownership, one authoritative state/representation, established language/library mechanisms, and deletion/consolidation over compensating wrappers. Existing tests/docs/helpers/caches/retries/state machines/patches do not promote machinery into authority.

A contract-changing implementation requires deliberate specification change, affected-consumer/persisted-state/compatibility/evidence/documentation/dependency/history analysis, implementation, affected regression + real integration, evidence applicability review/remap/rerun, and impact closure. Specification mutation and implementation repair are distinct semantic actions even when one commit contains both.

## Evidence, compatibility, errors, state

Keep evidence target separate from execution machinery. A durable behavior/property test may survive internal owner replacement while a helper-specific oracle becomes stale; remap/rerun against the real current owner rather than preserving obsolete product machinery for test convenience. A stale pass cannot confirm and stale fail cannot refute current behavior.

Preserve compatibility only where an actual supported contract/migration requires it. Derived caches may often be invalidated/rebuilt; authoritative user/project data may require explicit migration. Remove obsolete compatibility paths when their support window ends rather than carrying history as product complexity.

Validate meaningful boundaries and fail actionably. Do not hide invariant violations behind permissive fallback. Persistence/restart/transaction/cleanup/state-transition behavior must match accepted D4/D3 ownership where material.

## Verification and impact closure

Before D4 acceptance, compare actual behavior with accepted D4, D3, and directly applicable upstream/external constraints. Green tests do not prove omitted specification obligations. For public/consumer claims, test through the real supported interface/semantic owner; helper invocation cannot prove caller/orchestrator/persistence behavior when those are part of the claim.

A local D4 refactor needs a proportionate upstream-impact exclusion plus remap/rerun of invalidated owner-specific evidence. If implementation evidence reveals a parent defect, challenge the earliest affected abstraction rather than forcing code to preserve a wrong contract.

For material contract/concretization changes, close dependent consumers, evidence, docs/dependency records, compatibility/persistence consequences and semantic history where triggered. Apply the Lossless Representation Rule to D4 specifications: state each stable contract once, avoid freezing incidental code detail, keep exceptions/failure semantics explicit, and make critical behavior salient without dropping lower-salience mandatory constraints.
