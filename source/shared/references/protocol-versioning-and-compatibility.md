# Protocol Versioning, Historical Recovery, and Compatibility

## Versioning

`source/PROTOCOL_VERSION` identifies the current canonical protocol contract.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control-plane strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 is a major revision because scientific/mathematical formulation and numerical/algorithm design become first-class authority-bearing domains and the governing doctrine changes from a software-centric two-role hierarchy to recursive abstraction–realization across D1-D4.

Protocol 6 preserves the strongest Protocol 5 engineering guarantees by refactoring them into the new hierarchy: minimum justified complexity, adaptive realization, snapshot-complete handoff, proxy-proof acceptance, affected regression/integration, evidence reuse/invalidation, active simplification, convergence-aware reasoning, language/tool routing, long-horizon quality, and version-bound workplans.

## Workplan protocol binding

Every workplan that inherits protocol-wide behavior binds to its declared `protocol_version`.

A workplan governed by version `X` continues to mean Protocol `X` after newer releases. Do not reinterpret active or completed 5.x work using Protocol 6 merely because the installed/latest skill changed.

A plan may explicitly adopt a newer compatible contract only after reconciling changed obligations. A 5.x -> 6.0 adoption is a major semantic migration and is never silent.

## Immutable Protocol 5.16 recovery

Historical Protocol 5.16 authority is pinned to immutable repository commit:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
```

That commit is the canonical source snapshot immediately preceding the SSDP 6 transition workplan. Historical resolution must use this immutable identity (or another explicitly equivalent release/tag mapping), never `main`/latest.

The orchestrator's packaged `sdp-protocol-5.16` profile remains a reproducible version-bound snapshot and must continue to resolve 5.16 workplans under profile schema v1 after Protocol 6 release.

## Protocol 6 orchestration profile

Protocol 6 uses a separately versioned profile identity/schema. If its domain-aware routing cannot be represented without overloading profile schema v1, schema v2 is required. Core may support both schemas; it must select by declared protocol/profile identity rather than by a global current constant.

Historical 5.16 source/profile behavior must remain testable independently of the Protocol 6 current profile.

## Evidence invalidation across version changes

Reuse evidence until a changed protocol obligation or product/authority dimension can plausibly alter the claim. Version adoption does not automatically invalidate unrelated executable evidence.

Final assembled acceptance must still reflect the candidate after all material executable edits.

## Software/product compatibility

Preserve API/data/runtime compatibility only where an actual supported contract requires it. Historical implementation machinery does not become a compatibility requirement through existence. Retain compatibility layers only for a supported version/migration window or when they remain the minimum justified realization.

## Historical Protocol 5 lineage

Protocol 5.16 was the final backward-compatible refinement of the Protocol 5 software-centric lifecycle. It included long-horizon quality, adversarial Verification, portable workflow orchestration, language profiles, active simplicity, tool routing, snapshot-complete handoff, proxy-proof acceptance, and strict implementation regression/integration.

Earlier completed Protocol 5 work remains valid under the version that governed it. Protocol 6 does not retroactively rewrite that history.