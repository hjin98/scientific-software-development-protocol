# Protocol Versioning, Historical Recovery, and Compatibility

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** binds every workplan and orchestration profile to an explicit protocol version. Protocol 6.1 uses **concretization** for downstream D1-D4 semantic expression; historical Protocol 6.0 uses **realization** for the same relation and remains correct within its release-pinned context.

## Versioning

`source/PROTOCOL_VERSION` identifies the current canonical protocol contract.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control-plane strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 is a major revision because scientific/mathematical formulation and numerical/algorithm design become first-class authority-bearing domains and the governing doctrine changes from a software-centric two-role hierarchy to recursive abstraction–realization across D1-D4.

Protocol 6.1 is a backward-compatible minor revision. It preserves the Protocol 6 control architecture while:

- resolving current semantic-descent terminology to abstraction/concretization and reserving realization for evidence execution;
- making evidence specification, evidence realization, observation, assessment, applicability, stale-evidence handling, and evidentiary common-mode risk explicit;
- introducing bounded Markdown semantic-dependency and semantic-evolution-history conventions without requiring a machine graph/database;
- requiring manual impact closure for material authority/concretization changes;
- strengthening human-facing background/context and first-use abbreviation standards;
- preserving a distinct frozen Protocol 6.0 profile while introducing `ssdp-protocol-6.1` as the current profile after qualification.

Protocol 6.1 is the final document-controlled/semi-automated release before the Protocol 7 mandatory deterministic orchestrator control-plane transition.

Protocol 6 preserves the strongest Protocol 5 engineering guarantees by refactoring them into the new hierarchy: minimum justified complexity, adaptive concretization, snapshot-complete handoff, proxy-proof acceptance, affected regression/integration, evidence reuse/invalidation, active simplification, convergence-aware reasoning, language/tool routing, long-horizon quality, bounded urgent mitigation, compact resumable working state, and version-bound workplans.

## Protocol 6 generalization and Protocol 5 specialization

Protocol 6 is the general theory. Protocol 5 is a narrower software-local specialization recoverable inside it. Restricting active scope to software architecture and executable concretization recovers the former `software-design -> software-implementation` loop as the D3 -> D4 specialization of recursive abstraction/concretization.

The concise historical mapping is:

```text
Protocol 5 Tier 1A
    -> applicable accepted parent-abstraction invariants
       + directly governed external/domain constraints

Protocol 5 Tier 1B / Frozen high-level architecture
    -> cycle-scoped child-concretization decisions
       and, when explicitly accepted as durable, current D3 architecture

Protocol 5 Tier 2
    -> delegated concretization beneath the governing abstraction

Protocol 5 Tier 3
    -> development economy after fidelity and minimum justified complexity
```

This mapping preserves capability, not vocabulary. Every material Protocol 5 safeguard must remain recoverable as Protocol 6 behavior unless deliberately replaced by a stronger/general rule. Compression that deletes a capability is a defect; compression that expresses the same behavior once in broader Protocol 6 language is preferred.

Current Protocol 6.1 operational roles, routing references, templates, and guidance should speak Protocol 6.1 semantics directly. Legacy Protocol 5/6.0 vocabulary belongs in immutable/version-pinned artifacts, compatibility mappings, and explicitly historical qualification—not as a second current vocabulary. Current regression tests should protect semantic capability rather than require obsolete words merely for recognizability.

## Historical Protocol 5 lineage

Protocol 5 established the governing product doctrine: material engineering requirements define the feasible product space, and among engineering-sufficient solutions the protocol prefers the globally justified software/system design with the lowest unnecessary total complexity.

Protocol 5.1 added the optional `software-documentation` specialist. Protocol 5.2 added the optional `repository-hygiene` specialist. Protocol 5.3 strengthened stage-local/final functional acceptance and separated production qualification. Protocol 5.4 added development-economy, accepted-workplan authority, bounded redesign, version-bound workplan inheritance, evidence/context reuse, coherent stage granularity, and evidence-directed review.

Protocol 5.5 is a backward-compatible implementation-fidelity and workflow-integration refinement. Protocol 5.6 is a backward-compatible proxy-proof acceptance and test-double-boundary strengthening. Protocol 5.7 is a backward-compatible engineering-stewardship and outcome-alignment strengthening. Protocol 5.8 is a backward-compatible effective-compression and canonical-ownership refinement. Protocol 5.9 is a backward-compatible agent-portable deterministic-routing refinement. Protocol 5.10 is a backward-compatible snapshot-complete handoff refinement. Protocol 5.11 is a backward-compatible tool-assisted engineering methodology and capability refinement. Protocol 5.12 is a backward-compatible development-convergence and cycle-economy control refinement. Protocol 5.13 is a backward-compatible deterministic tool-entry, CodeQL, and progressive-disclosure compression refinement. Protocol 5.14 is a backward-compatible solution-boundary and active-simplicity strengthening. Protocol 5.15 is a backward-compatible language-engineering-profile and cross-language performance refinement. Protocol 5.16 is a backward-compatible long-horizon code-health, adversarial-verification, and portable workflow-orchestration refinement.

Protocol 5.16 was the final backward-compatible refinement of the Protocol 5 software-centric lifecycle. It preserved the Protocol 5 hierarchy and two-role lifecycle while adding non-authoritative quality ratchets and maintenance sensors, conditional mutation/differential/metamorphic/failure-injection evidence, executable architecture-fitness guidance, fresh-context falsification-oriented review, risk-triggered Verification, non-mutating milestone Stabilization, one optional semantic maintenance-audit specialist, stronger lifecycle closeout, and a canonical parameterized human-facing prompt entrypoint with compatible-local-first/public-repository-fallback skill resolution.

Earlier completed Protocol 5 work remains valid under the version that governed it. Protocol 6 does not retroactively rewrite that history.

## Workplan protocol binding

Every workplan that inherits protocol-wide behavior binds to its declared `protocol_version`.

A workplan governed by version `X` continues to mean Protocol `X` after newer releases. Do not reinterpret active or completed 5.x or 6.0 work using Protocol 6.1 merely because the installed/latest skill changed.

Historical wording remains authoritative for work under the version that introduced it. Active older workplans may continue under their declared version or explicitly adopt a newer compatible version only after reconciling changed obligations.

A 5.x -> 6.x adoption is a major semantic migration and is never silent. A 6.0 -> 6.1 adoption is minor/backward-compatible but still must preserve version binding when the workplan remains declared as 6.0.

Previously executed evidence remains reusable when no changed protocol obligation, governed claim, concretization, evidence specification/oracle, candidate, or material environment dimension can plausibly alter its applicability.

## Immutable Protocol 5.16 recovery

Historical Protocol 5.16 authority is pinned to immutable repository commit:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
```

That commit is the canonical source snapshot immediately preceding the SSDP 6 transition workplan. Historical resolution must use this immutable identity (or another explicitly equivalent release/tag mapping), never `main`/latest.

The orchestrator's packaged `sdp-protocol-5.16` profile remains a reproducible version-bound snapshot and must continue to resolve 5.16 workplans under profile schema v1 after Protocol 6 releases.

## Immutable Protocol 6.0 recovery

The accepted pre-6.1 Protocol 6.0 source/profile baseline is pinned to:

```text
6.0.0 -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
```

This identity represents the canonical Protocol 6.0 source and `ssdp-protocol-6.0` behavior immediately before Protocol 6.1 implementation began.

Historical/declared 6.0 resolution must continue to use immutable 6.0 source/profile semantics after 6.1 becomes current. Do not mutate packaged `ssdp-protocol-6.0` resources into 6.1 vocabulary or routing.

## Immutable Protocol 6.1 recovery

The accepted Protocol 6.1 pre-automation source/profile/lifecycle snapshot is pinned to:

```text
6.1.0 -> dec5ff2767e14fd1cda46e073757aa27f40e270c
```

This identity contains the qualified Protocol 6.1 canonical skills/references/templates/prompts, current `ssdp-protocol-6.1` profile/snapshot, frozen 5.16/6.0 compatibility resources, generated package artifacts, evidence/dependency/evolution doctrine, final qualification/review records, and archived Protocol 6.1 implementation handoff. It is the immutable document-controlled/semi-automated rollback baseline for Protocol 7 development.

Protocol 7 must not retroactively mutate or dependently reinterpret this snapshot. Fallback from Protocol 7 is version rollback to this identity, not simultaneous dual-current workflow authority.

## Protocol 6 orchestration profiles

Protocol 6 uses separately versioned profile identities under profile schema v2 rather than overloading Protocol 5 schema v1.

- `sdp-protocol-5.16` -> Protocol 5.16, profile schema v1, frozen compatibility;
- `ssdp-protocol-6.0` -> Protocol 6.0, profile schema v2, frozen compatibility after 6.1 acceptance;
- `ssdp-protocol-6.1` -> Protocol 6.1, profile schema v2, current/default after 6.1 qualification.

Profile schema v2 is retained for 6.1 because the minor revision changes doctrine/prose/version identity rather than introducing a new machine-control field. A future schema bump requires an actual profile-contract change.

Core selects by declared protocol/profile identity rather than by one global current constant. Historical 5.16 and 6.0 behavior must remain testable independently of the current 6.1 profile.

## Public-source resolution

Current Protocol 6.1 local-first/public-fallback guidance uses the canonical public repository:

```text
https://github.com/hjin98/scientific-software-development-protocol
```

Historical release-pinned prompts/profiles retain their historical bytes and URLs. Do not rewrite a frozen profile merely because the repository identity or current documentation changed later.

## Evidence invalidation across version changes

Reuse evidence until a changed protocol obligation or governed authority/concretization/evidence dimension can plausibly alter the claim or interpretation. Version adoption does not automatically invalidate unrelated executable evidence.

A stale passing result cannot close a current 6.1 claim; a stale failing result cannot refute it. Review/remap/rerun the applicable evidence specification as required.

Final assembled acceptance must still reflect the candidate after all material executable edits and material authority/evidence impacts.

## Protocol 6.1 recovery and Protocol 7 rollback boundary

Protocol 6.1 implementation, complete qualification, independent Review, and lifecycle closeout are represented by the immutable recovery mapping above. The pinned snapshot is sufficient to restore the document-controlled/semi-automated workflow without Protocol 7 machinery.

Protocol 7 fallback is version rollback to that immutable Protocol 6.1 snapshot, never simultaneous dual-current workflow authority.

## Candidate identity

For a normal Git repository, semantic candidate commit plus absence of unintended product-defining working-tree changes is usually sufficient source identity. Additional hashes/manifests are required only at real boundaries not represented by Git.

If qualification results or workplan closeout necessarily create later commits, distinguish the **semantic candidate commit** from later evidence-bearing/lifecycle-only commits. A later semantic mutation invalidates/reopens the applicable qualification surface.

## Software/product compatibility

Preserve application-programming-interface (API), data, runtime, and profile compatibility only where an actual supported contract requires it. Historical implementation machinery does not become a compatibility requirement through existence. Retain compatibility layers only for a supported version/migration window or when they remain the minimum justified concretization.