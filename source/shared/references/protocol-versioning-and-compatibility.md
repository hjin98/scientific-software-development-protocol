# Protocol Versioning, Release State, Historical Recovery, and Compatibility

Own protocol/workplan/profile version binding, immutable historical recovery, public-source fallback semantics, protocol-version acceptance/ratification semantics, Project Engineering Memory (PEM) schema/version adoption behavior, and compatibility interpretation. Mutable SSDP repository release values are not owned here; they are project state in root `PROTOCOL-RELEASE-STATE.yaml`. Detailed release chronology belongs in `history/SEMANTIC_EVOLUTION.md`.

## Version classes

`source/PROTOCOL_VERSION` identifies the version-intrinsic canonical source contract being built.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 introduced first-class D1-D4 authority. Protocol 6.1 strengthened terminology/evidence/handoff/documentation; 6.2 strengthened lossless representation/progressive disclosure; 6.3 added evidence-backed non-authoritative project engineering memory; 6.4 strengthened definition/source availability, well-definedness, parameterization, typed semantic dependencies, imported-source discipline and claim warrant. A compatible successor preserves those accepted capabilities unless an explicit stronger authority supersedes them.

## Version-intrinsic semantics versus mutable release state

Let (S_v) be protocol semantics for version (v), and (L_t) mutable repository/project release state at project state (t). They are distinct:

```text
version-intrinsic source/profile/package semantics != mutable accepted/current/publication/recovery state
```

An immutable version snapshot may define lifecycle concepts, but it must not be the current owner of facts that can change later, such as which version is accepted-current, whether a candidate passed Review, or which recovery commit was subsequently published.

For the SSDP repository, root `PROTOCOL-RELEASE-STATE.yaml` is the sole mutable owner of:
- accepted-current protocol version;
- exact version-bound public-source fallback mapping;
- exact recovery mapping;
- active successor semantic-candidate identity;
- independent Review state/evidence;
- stakeholder-ratification state/evidence.

Secondary current surfaces route to that owner or deliberately freeze an exact value as a bounded workplan input; they do not hand-maintain competing current values. A copy of the state file in an older immutable commit is historical snapshot evidence, not current release authority.

Repository merge/integration publishes a ratified state but does not manufacture the acceptance decision.

## Protocol-version acceptance and publication

Independent assembled-candidate Review and stakeholder ratification are distinct:

```text
independent Review PASS -> technically eligible for acceptance
explicit stakeholder ratification of that exact reviewed semantic candidate -> accepted decision
publication/cutover -> representation and distribution of that accepted decision
```

An agent, CI system, merge, branch position, or Review PASS cannot infer or self-issue stakeholder ratification.

For a successor release:

1. implement and functionally qualify version-intrinsic semantics without claiming public fallback/recovery;
2. freeze an immutable semantic candidate;
3. perform independent assembled-candidate Review of that exact candidate;
4. obtain explicit stakeholder ratification of that reviewed candidate;
5. from a later descendant, publish the exact reviewed/ratified semantic-candidate SHA as the version-bound public-source fallback;
6. verify exact-ref remote/source/package/profile realization;
7. select a distinct later immutable recovery target containing required Review/ratification/publication lineage;
8. publish recovery mapping from a later descendant;
9. reconcile mapping-dependent current projections and rerun affected package/profile/Core/current-state acceptance;
10. promote accepted-current only when the release-state transaction is coherent.

A material semantic mutation after Review invalidates Review/ratification for the modified candidate and reopens affected qualification. Public fallback and recovery are deliberately distinct. Git commits cannot self-name, so mapping publication is necessarily descendant state.

## Capability preservation across versions

Protocol 6 generalizes Protocol 5 capability rather than invalidating supported version-bound semantics, and recovers the former software-local design->implementation specialization inside the broader D1->D4 abstraction/concretization system.

Historical capability lineage includes:
- **5.13 deterministic tool entry/CodeQL/progressive disclosure**;
- **5.14 solution-boundary/active simplicity**;
- **5.15 language profiles/cross-language performance**;
- **5.16 long-horizon health/verification/stabilization/maintenance audit/workflow prompts/public fallback**;
- **Protocol 6.2 is a backward-compatible representation/progressive-disclosure strengthening** over the accepted Protocol 6 line.

Capability, not obsolete wording, is the compatibility oracle. A successor must preserve every still-valid accepted capability or explicitly classify and justify its supersession/removal. Compression that loses behavior is a defect; historical terms need not remain hot when an equal-or-stronger current invariant preserves their meaning.

Version-bound work remains interpreted under its declared `protocol_version`. A newer installed/latest skill or default profile never silently reinterprets older work. Adoption of a compatible newer version reconciles only newly applicable obligations and materially affected evidence/dependencies.

Frozen historical source/profile/publication/recovery artifacts remain historical truth and are never rewritten to current terminology. Current release mappings are resolved from the project release-state owner rather than replayed from this semantic owner.

## Workplan binding, PEM adoption, and evidence reuse

Every workplan inheriting protocol behavior binds its declared `protocol_version`. Older active work may continue under that version or explicitly adopt a compatible successor after changed obligations are reconciled.

PEM `memory_schema_version` is independent of SSDP protocol version and orchestration profile schema. A compatible protocol successor may retain a memory schema while clarifying its documented semantics. Unknown/newer/incompatible schemas fail safe for memory-dependent decisions; unsupported memory does not block unrelated protocol routes.

A restored old PEM snapshot is not current merely because it parses. Re-adoption/recovery reconciles schema, project/scope identity, accepted base, candidate overlay, owners, evidence/binding health, and the uncovered project interval. `reconciled_through` is an identity horizon, not proof of exhaustive history.

Previously executed evidence remains reusable only while no changed protocol obligation, claim/concretization, evidence specification/oracle, candidate, material parameter/regime/source binding, or material environment dimension can plausibly alter applicability.

## Immutable historical recovery

Immutable historical mappings are retained in the project release-state owner and semantic history. Historical work resolves through its exact version-specific source/profile semantics, never by assuming repository default/latest or treating a semantic-version string as a Git ref.

A **public-source fallback** is the exact immutable source snapshot authorized for version-bound remote bootstrap when no compatible installed/local source is available. A **recovery** target is a distinct immutable rollback/accepted lifecycle state. One does not imply the other.

Invalidated bootstrap attempts remain historical evidence only and must not be silently reused. Replacement fallback publication follows exact-source qualification and descendant mapping publication.

## Orchestration profiles

Profiles remain independently version-bound. Schema identity is separate from protocol version. Supported profile identities include `sdp-protocol-5.16` and `ssdp-protocol-6.0` through `ssdp-protocol-6.5`. The 6.x profile family may reuse the same machine stage/result schema while carrying distinct version-intrinsic prompt semantics.

Core selects by declared protocol/profile identity, not a global semantic "latest". When a new profile becomes current, every older supported profile remains frozen and independently testable. Generic packages/profiles may include PEM doctrine/templates but never a live project's `PROJECT-ENGINEERING-MEMORY.md` or mutable project release-state file.

## Candidate identity and compatibility

For normal Git repositories, semantic candidate commit plus absence of unintended product-defining changes is usually sufficient source identity. Later qualification/lifecycle/PEM-reconciliation commits distinguish themselves from the semantic candidate; any later semantic mutation reopens affected qualification. Same-branch PEM remains a candidate overlay until project integration policy accepts it.

Preserve API/data/runtime/profile compatibility only where an actual supported contract requires it. Historical machinery does not become compatibility authority through existence or memory recording. Retain compatibility layers only for a supported migration window or while they remain the minimum justified concretization.

Apply the Lossless Representation Rule: keep current operational state hot through its one mutable owner, keep version-intrinsic semantics with their canonical owners, and keep detailed release chronology cold but recoverable.
