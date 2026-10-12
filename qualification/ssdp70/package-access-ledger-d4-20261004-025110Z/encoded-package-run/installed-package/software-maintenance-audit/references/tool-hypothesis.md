# Hypothesis: Invariant-Driven Property and Stateful Testing

Use Hypothesis for property-based test generation, shrinking, and rule-based stateful testing on Python test surfaces where governed behavior defines a meaningful input or state space.

## Selection boundary

Useful cases include round-trip invariants, parser/normalizer boundaries, algebraic/data-structure properties, numerical/domain edge cases, optimized-versus-independent-reference equivalence, large combinations that are impractical to enumerate manually, and operation/state-transition sequences.

Small deterministic examples and already-exhaustive finite cases do not require Hypothesis merely because it is installed.

When a Hypothesis-class question is triggered, read this method before relying solely on hand-enumerated examples. If Hypothesis availability is unknown, use a cheap non-mutating capability probe when practical. When available and the governed behavior exposes a meaningful broad/combinatorial state or input space, presumptively use generated property/stateful testing; otherwise take a concrete fallback without weakening required coverage.

## Property and oracle integrity

Derive properties from governed behavior and invariants rather than merely from current implementation output. A property or model that reproduces the same implementation logic is **not an independent oracle**.

Keep generated domains representative of the contract. **Do not use excessive filtering or `assume`, over-narrow strategies, exclusions, health-check suppression, disabled useful phases, removed deadlines, or reduced exploration solely to make a property green.** Change settings when project/test semantics justify it and **required coverage remains intact**.

Hypothesis generation heuristics and distributions can change between versions. Assert durable properties rather than depending on a particular generated sequence or list of examples.

## Resource bounds and state isolation

Bound `max_examples`, **object sizes**, **stateful step counts**, **deadlines/expensive operations**, and **scientific workloads** according to existing resource-safety doctrine while **preserving representative coverage**.

Property/stateful tests can execute and shrink the body many times. Each example must begin from sufficiently **isolated/reset test-owned state** for the claim. Do not repeatedly mutate irreversible production/user data or depend on state leaked from a previous generated example.

When a persistent/state-machine owner is itself the acceptance claim, execute that real owner using bounded test-owned persistence/state rather than replacing the owner with the test model. A model may be an oracle; it may not proxy-pass the production owner.

## Durable counterexamples and reproducibility

The local Hypothesis **example database** is useful cache/replay state, **not durable regression authority by itself**.

When a **material minimized counterexample** exposes a durable bug contract, preserve it with an **explicit ordinary regression**, **Hypothesis `@example`**, or **another understandable governed test input** when that **adds stable protection**. Do not rely only on `.hypothesis` cache state or an opaque reproduction blob.

**Seeds and failure-replay mechanisms are debugging aids.** Do not permanently pin one seed merely to make routine acceptance deterministic if doing so materially weakens exploration.

When CI/runtime reproducibility or resource budgeting is material, define an explicit repository-owned Hypothesis **settings profile** appropriate to that environment. The profile is ordinary governed test configuration and must not silently weaken the accepted property.

Hypothesis tests participate in the same focused, stage-local affected-regression, and final-regression rules as other tests. Passing generated properties do not prove omitted workplan obligations or untested integration boundaries. Longer fuzz/exploratory runs can provide additional discovery but are not automatically production qualification or a mandatory release gate.
