# D4 Specification and Implementation

D4 is the concrete software-contract and executable-concretization domain. It is constrained by applicable D3 architecture, upstream semantics that reach D4 directly, and domain-local governed contracts.

## Background and terminology

Under Protocol 6.1, **concretization** names downstream scientific/software expression of an abstraction. **Evidence realization** instead names one concrete execution of an evidence specification. Code/executable behavior is the actual D4 concretization and a source of evidence about what exists; a test run is an evidence realization.

## Specification versus code

Where a concrete behavior is governed, the accepted **D4 Specification** is the normative statement of intended software behavior. Code/executable behavior is the concretization and evidence of what actually exists.

```text
accepted D4 specification  --constrains--> code / executable behavior
accepted D4 specification  <--verify------ code / executable behavior
```

Code does not become the intended contract merely because it exists or because tests encode its current output. If code disagrees with an accepted specification, classify the disagreement before editing either side:

- code is wrong -> repair implementation;
- specification is stale because an accepted upstream/D4 contract legitimately changed -> update specification and affected consumers/evidence;
- intent is ambiguous -> route to the owning authority;
- accepted specification itself may be materially wrong/contradictory -> Serious Challenge rather than silent rewrite.

Never rewrite a specification solely to make unintended implementation pass.

## What belongs in a D4 Specification

Specify only concrete stable contracts that consumers, persisted data, automation, or scientific interpretation rely on, such as:

- public application programming interface (API), command-line interface (CLI), and configuration behavior;
- formats, schemas, units/shapes/order/precision exposed at the concrete boundary;
- persistence/restart/migration semantics;
- compatibility and supported-version behavior;
- concrete backend/device policy when it is public or governed;
- durable error/fallback behavior;
- externally observable state transitions and authorization/security contracts.

Do not specify private helpers, incidental call graphs, local data structures, or other replaceable machinery unless their identity is genuinely part of an accepted contract.

Current human-facing D4 specifications that introduce non-common domain concepts follow [Scientific and technical writing](scientific-technical-writing.md): provide concise background before relying on specialized terminology and expand non-obvious abbreviations at first explanatory use. Background explanation does not replace the precise D4 contract.

## Implementation authority

Within the feasible set defined by specification, architecture, upstream semantics, and external constraints, implementation remains adaptive. Prefer direct control flow, cohesive ownership, one authoritative state/representation, established language/library mechanisms, and deletion/consolidation over compensating wrappers.

Existing tests, documentation, helpers, caches, retry loops, state machines, or previous patches do not promote machinery into authority.

## Contract-changing implementation

When an accepted upstream/domain decision changes a concrete contract:

1. change the authoritative specification deliberately;
2. identify affected consumers, persisted state, compatibility surfaces, evidence specifications/realizations, examples, documentation, dependency views, and semantic-history obligations;
3. implement the new specification;
4. verify actual behavior through affected regression and real integration boundaries;
5. review prior evidence applicability and mark/remap/rerun only materially affected evidence;
6. close the material impact set before claiming completion.

Specification mutation and implementation repair are separate semantic actions even when committed together.

## Evidence and execution dependency

Keep the evidentiary target separate from the machinery required to execute evidence. A durable behavior/property test may remain a valid evidence specification after internal D4 ownership changes, while a helper-specific test/oracle may become stale. Remap/rerun against the new real semantic owner rather than preserving obsolete machinery for historical test convenience.

A passing stale result is not confirmation of the current specification; a failing stale result is not refutation. Evidence applicability follows the current claim, candidate, oracle, regime, and material execution environment.

## Compatibility

Preserve compatibility only when an actual supported contract or migration requirement needs it. Compatibility machinery has product complexity cost. Remove obsolete paths when their supported window ends; do not preserve historical implementation merely because it once existed.

Derived caches may often be invalidated/rebuilt. Authoritative user/project data may require explicit migration.

## Errors and state

Validate meaningful boundaries and fail actionably. Do not hide invariant violations behind permissive fallback. Persistence, restart, transaction, cleanup, and state-transition behavior must match the accepted specification and D3 ownership model where material.

## Verification and impact closure

Before D4 acceptance, compare actual executable semantics against the accepted D4 specification, D3 architecture, and directly applicable upstream/external constraints. Green tests do not prove a missing specification obligation.

For public/consumer contracts, test through the real supported interface or semantic owner. Direct helper invocation cannot prove caller/orchestrator/persistence behavior when those are part of the claim.

A D4-only local refactor needs only a proportionate check that no plausible D3/D2/D1 semantics changed, plus affected evidence remapping/rerun where owner-specific evidence was invalidated. If implementation evidence reveals a parent defect, challenge the earliest affected abstraction rather than forcing code to preserve a wrong contract.

For material contract/concretization changes, bounded impact closure must account for materially dependent consumers, evidence, documentation/dependency records, compatibility/persistence consequences, and semantic-history updates where triggered. Absence of an edge in a partial dependency map is not proof of independence.
