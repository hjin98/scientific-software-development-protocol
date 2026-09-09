# Protocol Versioning, Historical Recovery, and Compatibility

## Versioning

`source/PROTOCOL_VERSION` identifies the current canonical protocol contract.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control-plane strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 is a major revision because scientific/mathematical formulation and numerical/algorithm design become first-class authority-bearing domains and the governing doctrine changes from a software-centric two-role hierarchy to recursive abstraction–realization across D1-D4.

Protocol 6 preserves the strongest Protocol 5 engineering guarantees by refactoring them into the new hierarchy: minimum justified complexity, adaptive realization, snapshot-complete handoff, proxy-proof acceptance, affected regression/integration, evidence reuse/invalidation, active simplification, convergence-aware reasoning, language/tool routing, long-horizon quality, bounded urgent mitigation, compact resumable working state, and version-bound workplans.

## Protocol 6 generalization and Protocol 5 specialization

Protocol 6 is the general theory. Protocol 5 is a narrower software-local specialization recoverable inside it. Restricting active scope to software architecture and executable realization recovers the former `software-design -> software-implementation` loop as the D3 -> D4 specialization of recursive abstraction-realization.

The concise historical mapping is:

```text
Protocol 5 Tier 1A
    -> applicable accepted parent-abstraction invariants
       + directly governed external/domain constraints

Protocol 5 Tier 1B / Frozen high-level architecture
    -> cycle-scoped child-realization decisions
       and, when explicitly accepted as durable, current D3 architecture

Protocol 5 Tier 2
    -> delegated realization beneath the governing abstraction

Protocol 5 Tier 3
    -> development economy after fidelity and minimum justified complexity
```

This mapping preserves capability, not vocabulary. Every material Protocol 5 safeguard must remain recoverable as Protocol 6 behavior unless deliberately replaced by a stronger/general rule. Compression that deletes a capability is a defect; compression that expresses the same behavior once in broader Protocol 6 language is preferred.

Current Protocol 6 operational roles, routing references, templates, and current guidance should therefore speak Protocol 6 semantics directly. Legacy control-plane vocabulary belongs here, in immutable/version-pinned 5.x artifacts, and in explicitly historical qualification—not as a second current control plane. Current regression tests should protect semantic capability rather than require obsolete words merely for recognizability.

## Historical Protocol 5 lineage

Protocol 5 established the governing product doctrine: material engineering requirements define the feasible product space, and among engineering-sufficient solutions the protocol prefers the globally justified software/system design with the lowest unnecessary total complexity.

Protocol 5.1 added the optional `software-documentation` specialist. Protocol 5.2 added the optional `repository-hygiene` specialist. Protocol 5.3 strengthened stage-local/final functional acceptance and separated production qualification. Protocol 5.4 added development-economy, accepted-workplan authority, bounded redesign, version-bound workplan inheritance, evidence/context reuse, coherent stage granularity, and evidence-directed review.

Protocol 5.5 is a backward-compatible implementation-fidelity and workflow-integration refinement. Protocol 5.6 is a backward-compatible proxy-proof acceptance and test-double-boundary strengthening. Protocol 5.7 is a backward-compatible engineering-stewardship and outcome-alignment strengthening. Protocol 5.8 is a backward-compatible effective-compression and canonical-ownership refinement. Protocol 5.9 is a backward-compatible agent-portable deterministic-routing refinement. Protocol 5.10 is a backward-compatible snapshot-complete handoff refinement. Protocol 5.11 is a backward-compatible tool-assisted engineering methodology and capability refinement. Protocol 5.12 is a backward-compatible development-convergence and cycle-economy control refinement. Protocol 5.13 is a backward-compatible deterministic tool-entry, CodeQL, and progressive-disclosure compression refinement. Protocol 5.14 is a backward-compatible solution-boundary and active-simplicity strengthening. Protocol 5.15 is a backward-compatible language-engineering-profile and cross-language performance refinement. Protocol 5.16 is a backward-compatible long-horizon code-health, adversarial-verification, and portable workflow-orchestration refinement.

Protocol 5.16 was the final backward-compatible refinement of the Protocol 5 software-centric lifecycle. It preserved the Protocol 5 hierarchy and two-role lifecycle while adding non-authoritative quality ratchets and maintenance sensors, conditional mutation/differential/metamorphic/failure-injection evidence, executable architecture-fitness guidance, fresh-context falsification-oriented review, risk-triggered Verification, non-mutating milestone Stabilization, one optional semantic maintenance-audit specialist, stronger lifecycle closeout, and a canonical parameterized human-facing prompt entrypoint with compatible-local-first/public-repository-fallback skill resolution.

Earlier completed Protocol 5 work remains valid under the version that governed it. Protocol 6 does not retroactively rewrite that history.

## Workplan protocol binding

Every workplan that inherits protocol-wide behavior binds to its declared `protocol_version`.

A workplan governed by version `X` continues to mean Protocol `X` after newer releases. **Do not reinterpret active or completed 5.x work using Protocol 6** merely because the installed/latest skill changed.

Historical Protocol 5 wording remains authoritative for those workplans. In particular, **active older workplans do not automatically adopt Protocol 5.16 or any later release**. They **may continue under their declared version** or explicitly adopt a newer compatible version after reconciling changed obligations. A 5.x -> 6.0 adoption is a major semantic migration and is never silent.

A plan may explicitly adopt a newer compatible contract only after reconciling changed obligations. Previously executed evidence remains reusable when no changed protocol obligation or affected product/authority dimension can plausibly alter its claim.

## Immutable Protocol 5.16 recovery

Historical Protocol 5.16 authority is pinned to immutable repository commit:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
```

That commit is the canonical source snapshot immediately preceding the SSDP 6 transition workplan. Historical resolution must use this immutable identity (or another explicitly equivalent release/tag mapping), never `main`/latest.

The orchestrator's packaged `sdp-protocol-5.16` profile remains a reproducible version-bound snapshot and must continue to resolve 5.16 workplans under profile schema v1 after Protocol 6 release.

## Protocol 6 orchestration profile

Protocol 6 uses a separately versioned profile identity/schema. Its domain-aware routing is represented under profile schema v2 rather than overloading profile schema v1. Core supports both schemas and selects by declared protocol/profile identity rather than by a global current constant.

Historical 5.16 source/profile behavior must remain testable independently of the Protocol 6 current profile.

## Evidence invalidation across version changes

Reuse evidence until a changed protocol obligation or product/authority dimension can plausibly alter the claim. Version adoption does not automatically invalidate unrelated executable evidence.

Final assembled acceptance must still reflect the candidate after all material executable edits.

## Candidate identity

For a normal Git repository, candidate commit plus absence of unintended product-defining working-tree changes is usually sufficient source identity. Additional hashes/manifests are required only at real boundaries not represented by Git.

## Software/product compatibility

Preserve API/data/runtime compatibility only where an actual supported contract requires it. Historical implementation machinery does not become a compatibility requirement through existence. Retain compatibility layers only for a supported version/migration window or when they remain the minimum justified realization.
