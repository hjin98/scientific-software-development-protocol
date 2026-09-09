---
kind: protocol-major-revision-authority-amendment
amends_workplan: SSDP-6-RECURSIVE-ABSTRACTION-REALIZATION-SCIENTIFIC-SOFTWARE-PROTOCOL
protocol_version: 5.16.0
target_protocol_version: 6.0.0
status: accepted-amendment
created_date: 2026-09-08
review_origin: post-implementation-generalization-and-inheritance-review
authority_entrypoint: workplans/active/SSDP-6-AUTHORITY.md
---

# SSDP 6 Authority Revision 2 — Protocol 5 Functional Inheritance and Doctrine Consolidation

## 1. Status and scope

The first SSDP 6 implementation review found **no Serious Challenge** to recursive abstraction-realization, the D1-D4 decomposition, or the new authority model. The conceptual parent remains accepted.

The implementation is nevertheless **NO-PASS** until the migration is consolidated. The defect is not missing new theory; it is incomplete generalization of the old theory. Some current Protocol 6 operational references still require agents to reason in both Protocol 5 and Protocol 6 control-plane vocabulary, some regression oracles preserve legacy words instead of the capability they once denoted, and two useful Protocol 5 operational controls were lost during compression.

This amendment governs that repair. It does not introduce a new lifecycle role, compatibility layer, registry, state machine, or parallel doctrine.

## 2. Generalization-specialization invariant

Protocol 6 is the general theory. Protocol 5 is a narrower software-local specialization that must be reconstructible inside the Protocol 6 abstraction-realization model.

Conceptually:

```text
Protocol 6 recursive abstraction-realization
    -> restrict active semantic scope to software architecture + implementation
    -> recover the Protocol 5 software-local control loop as D3 -> D4
```

This relation is **semantic**, not syntactic. Protocol 6 does not need to preserve Protocol 5 names, section order, or narrower definitions. It must preserve every material engineering capability, decision boundary, acceptance safeguard, and escalation rule unless the new theory deliberately replaces it with a stronger or more general rule.

A current Protocol 6 agent should be able to derive the behavior formerly protected by Protocol 5 without loading or translating Protocol 5 terminology during ordinary current work.

## 3. Functional inheritance and performance-lossless compression

Protocol 5's historical improvements are inherited as capabilities. Compression is allowed and preferred when the resulting current doctrine is easier to route and reason about, but compression is defective if a material behavior disappears or becomes materially harder for an agent to recover.

At minimum the Protocol 6 specialization must retain the functional substance accumulated through Protocol 5.1-5.16, including:

- optional documentation and hygiene support without role proliferation;
- stage-local plus final affected regression/integration and separate production qualification;
- development economy, version-bound workplans, evidence reuse, coherent stage granularity, and bounded redesign;
- lossless workplan-to-realization handoff and minimum-known-contract semantics;
- proxy-proof real-owner acceptance and bounded test doubles;
- protected stakeholder outcome and independent-evaluator reasoning;
- progressive-disclosure compression and canonical ownership;
- portable deterministic routing and snapshot-complete handoff;
- relation-driven tool assistance and stronger property/data-flow evidence where appropriate;
- convergence/family reasoning, revision economy, and acceptance liveness;
- active simplification/re-derivation rather than patch accretion;
- language-aware Python/C++ realization, mixed-language boundaries, performance/resource/parallelism discipline, and architecture-gated accelerators;
- quality ratchets, test-oracle strength, differential/metamorphic/failure-injection evidence, Stabilization, maintenance audit, and workflow orchestration.

A historical capability may be re-expressed by a broader Protocol 6 invariant. It need not be duplicated once the new owner states it completely.

## 4. Canonical Protocol 5 -> Protocol 6 mapping

`protocol-versioning-and-compatibility.md` shall be the single current owner of the concise historical translation needed for version recovery and conceptual comparison.

The intended mapping is:

```text
Protocol 5 Tier 1A
    -> applicable accepted parent-abstraction invariants
       + directly governed external/domain constraints

Protocol 5 Tier 1B / Frozen high-level architecture
    -> cycle-scoped child-realization decisions
       and, only when explicitly accepted as durable, current D3 architecture

Protocol 5 Tier 2
    -> delegated realization beneath the governing abstraction

Protocol 5 Tier 3
    -> development economy after fidelity and minimum justified complexity

Protocol 5 software-design -> software-implementation
    -> the D3 -> D4 specialization of the Protocol 6 recursive lifecycle
```

The mapping is explanatory compatibility authority, not a requirement to retain both vocabularies in current operational doctrine.

## 5. Clean current-language rule

Current Protocol 6 operational roles, routing references, templates, current README guidance, and current profile-facing instructions shall speak **Protocol 6 semantics directly**.

Legacy Protocol 5 control-plane terms such as `Tier 1A`, `Tier 1B`, `Tier 2`, `product/Frozen`, or statements that shared Protocol 5 doctrine remains current authority are permitted only where their historical identity is itself the subject:

- immutable/version-pinned Protocol 5 source/profile/workplans;
- the canonical versioning/compatibility history and translation owner;
- explicitly historical qualification fixtures or tests that inspect historical artifacts rather than current routing.

Do not make current agents translate a live rule from Protocol 6 into Protocol 5 and back again. Do not retain old terminology merely because a regression test asserts the token.

## 6. Semantic-oracle migration rule

Regression tests protect **capabilities and semantic relations**, not obsolete names.

A migrated test should ask whether, for example:

- delegated realization remains replaceable;
- cycle-scoped decisions are distinct from durable accepted authority;
- recurrence broadens reasoning without freezing the current mechanism;
- active simplification precedes another additive repair when structural evidence warrants it;
- real-owner/proxy-proof evidence remains required;
- version-pinned Protocol 5 artifacts remain recoverable under their own historical semantics.

A test that requires current Protocol 6 doctrine to contain `Tier-2`, `Frozen`, or equivalent legacy wording merely to preserve recognizability is an invalid migration oracle unless that wording is itself a historical-artifact claim.

## 7. Restore two compressed-out Protocol 5 capabilities

### 7.1 Bounded urgent mitigation before normal simplification

When an independently governed urgency, safety, security, reliability, or incident-containment constraint makes immediate mitigation necessary, a **bounded, reversible or safely replaceable temporary repair may precede the normal mandatory simplification/re-derivation pass**.

The mitigation:

- does not become durable authority through emergency use;
- remains explicitly temporary where the underlying structural problem is unresolved;
- carries the unresolved structural debt/risk truthfully; and
- is reconciled through normal owning-domain simplification/re-derivation at the earliest safe point.

Urgency changes feasible sequencing; it does not authorize counterfeit closure or permanent patch accretion.

### 7.2 Compact resumable working state

For long, interruption-prone, multi-session, or materially handed-off work, maintain enough **compact temporary coordination state** to resume without depending on lost chat or rediscovering settled evidence.

The minimal useful state includes, as applicable:

- current governing snapshot/authority;
- open and closed obligations;
- material evidence/results and known invalidations;
- unresolved blockers, Serious Challenges, risks, and reopen/simplification triggers;
- next action.

This state is **not normative authority**, is not a permanent evidence system, and should disappear when no longer useful. Do not create a ledger, database, manifest, or parallel requirements store solely to satisfy this rule.

## 8. Minimal second-round repair surface

Repair the current candidate by alteration/removal before addition:

1. make the versioning/compatibility reference own the concise Protocol 5 -> Protocol 6 specialization mapping and functional-inheritance rule;
2. rewrite current language profiles, Python/C++ profiles, performance, tool-routing, convergence, workflow, repository-intake, and role wording into native Protocol 6 semantics where legacy control-plane language remains;
3. restore urgent mitigation and compact resumable working state in their existing generic owners rather than creating new process artifacts;
4. rewrite regression oracles that currently force legacy vocabulary so they protect the inherited semantic capability instead;
5. keep historical 5.16 artifacts and version-specific history unchanged and recoverable;
6. regenerate committed distributions and protocol snapshots from canonical source after the canonical source is semantically closed.

Do not introduce a Protocol-5 compatibility runtime, translation service, glossary copied into every reference, fifth role, migration stage machine, claim registry, or dual current profile semantics.

## 9. Amendments to parent obligations

### Obligation K — Protocol 5 inheritance

Obligation K now means **performance-lossless functional inheritance under generalization**. Every material Protocol 5 capability must be recoverable as a Protocol 6 specialization even when its former terms disappear. Historical vocabulary is not itself a capability unless historical interpretation is the claim.

### Obligation L — proportionality and digestibility

Protocol 6 fails proportionality if routine current work requires simultaneous reasoning in both Protocol 5 and Protocol 6 control planes. Current operational doctrine should route directly through the smallest Protocol 6 rule set that preserves the inherited behavior.

### Obligation N — adversarial self-qualification

Qualification must include migration counterfactuals: deleting legacy vocabulary from current authority must not delete the protected capability; conversely, preserving legacy words while losing the behavior must not pass.

## 10. Second-round acceptance

The consolidation repair is ready for re-review only when:

- current Protocol 6 operational doctrine no longer states that Protocol 5 doctrine is current authority;
- the versioning/compatibility owner contains the explicit generalization-specialization and functional-inheritance mapping;
- current D3/D4, language, performance, tool, convergence, workflow, and intake guidance can be read without legacy control-plane translation;
- semantic regression tests no longer require legacy control-plane tokens in current authority;
- bounded urgent mitigation and compact resumable state are restored in compressed Protocol 6-native form;
- immutable Protocol 5.16 recovery and historical workplan semantics remain unchanged;
- canonical source remains simpler or no more complex than the dual-doctrine candidate for equivalent capability;
- generated distributions/snapshots are regenerated and their normal parity/qualification checks execute before final release acceptance;
- independent re-review finds no material capability loss or new dual ownership.

## 11. Final amendment invariant

```text
Protocol 6 is the general theory; Protocol 5 is a restricted software-local specialization.

Protocol 6 must inherit Protocol 5 capabilities, not its obsolete current-language surface.
A historical capability may be compressed into a broader Protocol 6 invariant only when behavior is preserved.
Current Protocol 6 operational authority speaks Protocol 6 directly.
Historical Protocol 5 vocabulary lives at historical/version-compatibility boundaries, not in the current control plane.
Tests protect semantic capability rather than forcing obsolete words to survive.
The resulting protocol should be easier for an agent to route than the stitched dual-doctrine candidate while remaining functionally lossless.
```
