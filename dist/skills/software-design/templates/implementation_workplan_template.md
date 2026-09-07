---
kind: implementation-workplan
workplan_id: REPLACE_ME
protocol_version: 5.16.0
---

# <Task> Workplan

## Objective / problem invariants / non-goals

<State the original stakeholder, research, computational, scientific, or operational problem independently of the current implementation where possible. Record the Tier-1 product requirements, governed contracts, durable-success criteria, and explicit non-goals.>

## Frozen high-level architecture and engineering envelope

<Record only the material high-level architecture/ownership/algorithm/data-representation/resource/compatibility decisions Software Design deliberately freezes for this implementation cycle, plus material correctness/scientific/resource/scaling/hardware/performance/security/reliability requirements.>

Ask explicitly:

- What high-level architecture is deliberately Frozen for this cycle?
- Which details are intentionally **not** Frozen?
- Would changing a listed detail alter high-level architecture, or only the delegated realization?

For substantial or structurally risky work, note any task-local baseline/change-health evidence needed later to judge whether the affected system regressed in maintainability or behavioral protection. Do not create a permanent metric ledger solely for protocol compliance.

## Implementation obligations and delegated solution space

Record task-specific obligations, not generic protocol prose or a frozen proof script. An ordinary material obligation should preserve:

- **Concern / rationale:** why the outcome matters.
- **Required end state / constraint:** what must hold at product/Frozen-architecture level.
- **Delegated solution space:** what implementation-local machinery may be replaced, consolidated, simplified, or deleted while preserving the end state.
- **Acceptance evidence:** focused/regression/integration, numerical/resource/compatibility threshold, structural/absence check, or other proof.

Attach only when material:

- **Suggested realization:** useful guidance, explicitly replaceable by an equivalent simpler realization.
- **Acceptance boundary:** product/Frozen claim, current real semantic owner/path or owner class, allowed doubles, forbidden substitutions, and observable evidence when proxy acceptance is a material risk. State whether exact owner/path identity is itself product/Frozen authority or merely the current Tier-2 realization; if delegated, an equivalent replacement remaps acceptance to the new real owner rather than reopening Design.
- **Oracle-strength relation:** reference/differential/metamorphic/property/counterfactual/failure-path evidence when ordinary fixture equality would be weak.
- **Objective architecture-fitness rule:** a stable dependency/absence/uniqueness constraint worth executable enforcement.
- **Stage/dependency:** when ordering materially reduces risk or rework.
- **Anti-shortcut / integrity constraint:** a known way local compliance/evidence manipulation could appear to pass while defeating the stakeholder outcome.

For simplification/refactor work, state what existing machinery/state/path should be removed, narrowed, altered, or consolidated. If net-new machinery is required, state which Tier-1/Frozen capability cannot be met cleanly without it, or which broader existing machinery it replaces to reduce total system complexity.

The accepted plan is the minimum known contract, not a ceiling only for newly discovered affected behavior and logically necessary consequences of already-binding product/Frozen-architecture semantics. Affected-surface expansion does not itself create a new product requirement or freeze the current realization.

## Implementation authority

### Frozen

<List only Tier-1 product/problem requirements, deliberately Frozen high-level architecture, and acceptance boundaries whose exact identity is independently required by product/Frozen authority. Do not freeze a Tier-2 owner merely because current acceptance executes it.>

### Delegated

<List implementation-local mechanics and solution machinery intentionally left replaceable. Existing code, helpers, wrappers, state machines, retries, caches, adapters, synchronization, or prior patches are delegated unless explicitly promoted above.>

### Reopen only on evidence

<List material Frozen assumptions/decisions that may change only after a genuine redesign trigger. Reopen only the affected surface and preserve still-valid accepted work/evidence.>

## Affected surface and task-specific acceptance

<Initially expected changed/new behavior plus callers/consumers/shared utilities/configuration/persistence/state/orchestration/interfaces/packaging/documentation/transitive behavior that could plausibly change. This is provisional and must be re-derived from the final assembled implementation.>

Generic functional-acceptance requirements are inherited from the protocol version declared by `protocol_version`; later releases do not silently reinterpret this workplan. Record only task-specific mappings, thresholds, real-owner/test-double boundaries, repository-required checks, structural/absence claims, and quality-ratchet/failure-path evidence not already clear in the obligations.

Production qualification: <required / deferred / unnecessary, with reason when materially relevant>.

## Implementation sequence and genuine redesign / simplification triggers

<List only coherent behavior/risk stages where ordering materially reduces ambiguity or rework. A local coherent behavior change is normally one material stage; do not split tightly coupled helper/caller/test edits merely by file/function.>

<Record structural evidence that should trigger active Tier-2 simplification before another additive durable repair: repeated patches, patch-on-patch repair, wrapper/fallback/special-case accumulation, duplicated/synchronized authoritative state, competing authorities, repeated reconciliation machinery, or a materially simpler equivalent realization.>

<Record separately the evidence that would require bounded Design reconsideration because a **Frozen high-level architecture** decision itself must change.>
