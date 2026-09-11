# Protocol Versioning, Historical Recovery, and Compatibility

Own protocol/workplan/profile version binding, immutable historical recovery, public-source fallback identity, and compatibility interpretation. Detailed semantic chronology belongs in `history/SEMANTIC_EVOLUTION.md`; ordinary current work should not replay old control-plane vocabulary.

## Version classes

`source/PROTOCOL_VERSION` identifies the canonical source contract being built.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 is major because D1 scientific formulation and D2 numerical-method design become first-class authority domains in a recursive D1-D4 abstraction/concretization model. Protocol 6.1 is minor: current concretization terminology, evidence lifecycle/applicability/dependency/evolution, impact closure, human-facing background/abbreviation standards, and distinct frozen/current profiles. Protocol 6.2 is a backward-compatible representation/progressive-disclosure strengthening: accepted 6.1 semantics remain required while current communication/routing is losslessly compacted and the current kernel path becomes `abstraction-and-concretization.md`.

## Capability preservation across versions

Protocol 6 generalizes Protocol 5 rather than maintaining a second current vocabulary. Restricting active scope to D3 architecture and D4 implementation recovers the former software-local design->implementation specialization. Historical Tier terms map to applicable accepted parents/constraints, cycle-scoped child decisions, delegated concretization, and development economy.

Capability, not obsolete wording, is the compatibility oracle. Every still-valid Protocol 5 safeguard remains recoverable under current generalized rules unless deliberately replaced by stronger accepted authority; compression that loses behavior is a defect. Concise lineage: 5.1 documentation specialist; 5.2 hygiene; 5.3 stage/final acceptance + separate production qualification; 5.4 development economy/version-bound plans/evidence-context reuse; 5.5 implementation fidelity; 5.6 proxy-proof acceptance; 5.7 stewardship/outcome alignment; 5.8 effective compression/canonical ownership; 5.9 portable deterministic routing; 5.10 snapshot-complete handoff; 5.11 tool-assisted engineering; 5.12 convergence/cycle economy; 5.13 deterministic tool entry/CodeQL/progressive disclosure; 5.14 solution-boundary/active simplicity; 5.15 language profiles/cross-language performance; 5.16 long-horizon health/Verification/Stabilization/maintenance audit/workflow prompts/public fallback. Detailed rationale is historical, not normal hot-path doctrine.

## Workplan binding and evidence reuse

Every workplan that inherits protocol behavior binds to its declared `protocol_version`. A newer installed/latest skill never silently reinterprets older work. Older active work may continue under its declared version or explicitly adopt a compatible newer version after changed obligations are reconciled. A 5.x->6.x adoption is a major migration; 6.0->6.1->6.2 are backward-compatible minor steps but still preserve explicit version identity.

Previously executed evidence remains reusable only while no changed protocol obligation, governed claim/concretization, evidence specification/oracle, candidate, or material environment dimension can plausibly change applicability. Apply the evidence owner; version adoption does not automatically invalidate unrelated evidence.

## Immutable historical recovery

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639
```

Resolve historical work through immutable version-specific source/profile semantics, never `main`/latest. Frozen source/publication/profile artifacts remain historical truth and are not rewritten to current terminology.

Protocol 6.1 public-source bootstrap is distinct from recovery:

```text
repository -> https://github.com/hjin98/scientific-software-development-protocol
6.1.0 public-source bootstrap -> 47e9155632c44493644b0b02fa1fa625703cf480
```

The first Protocol 6.2 pre-acceptance bootstrap attempt was later invalidated by a required routing repair:

```text
6.2.0 invalidated bootstrap attempt -> 1181c2031710c5d343194d87d08543290fded0ab
```

That SHA remains historical implementation evidence only. It **must not** be used as current Protocol 6.2 public fallback because it predates the repaired explicit `software-documentation` cold concern routes.

The repository default branch is never a protocol-version oracle and a semantic version string is not assumed to be a Git ref.

## Orchestration profiles

Profiles remain independently version-bound:

| Profile | Protocol | Schema | State |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen historical |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen historical |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | accepted current until 6.2 closeout |
| `ssdp-protocol-6.2` | 6.2.0 | 2 | candidate/current-source successor; accepted only after 6.2 qualification/Review/recovery closeout |

Schema v2 remains unless an actual machine profile contract changes. Core selects by declared protocol/profile identity, not one global latest constant. Frozen profile bytes/behavior remain independently testable.

## Protocol 6.2 public-source and recovery staging

Git commits cannot self-name. A valid Protocol 6.2 bootstrap source snapshot therefore carries no automatic current-6.2 mapping to itself. The lifecycle is deliberately staged:

1. **candidate bootstrap source snapshot** — an internally coherent source/routing/package source set that is usable when reached through an explicit immutable ref, but does not claim its own unknown SHA;
2. **public-source publication mapping** — only a later current-source commit may publish `6.2.0 public-source bootstrap -> <exact validated bootstrap SHA>`;
3. **recovery snapshot** — a still later accepted rollback commit containing the qualified semantic candidate and required decision evidence through ancestry, selected only after independent Review passes.

Until step 2 is committed, **automatic current-6.2 public fallback is unavailable**. If `AUTO_LOCAL_FIRST` finds no governing-version-compatible installed source, report truthful non-closure instead of using the invalidated attempt, `main`, latest, or a guessed semantic-version ref. If this source snapshot was already reached through an explicit immutable ref or through a later exact mapping, continue using that already-resolved source and do not recursively resolve through repository-default bytes.

After a replacement bootstrap is validated, its exact immutable SHA is published only in a descendant mapping commit. After candidate qualification and independent Review, choose an immutable recovery commit; only a later mapping commit publishes `6.2.0 -> <recovery SHA>`.

Until all 6.2 acceptance stages complete, Protocol 6.1 remains accepted-current/rollback authority and public fallback for accepted 6.1 work.

## Candidate identity and compatibility

For normal Git repositories, semantic candidate commit plus absence of unintended product-defining changes is usually sufficient source identity. Later qualification/lifecycle commits must distinguish themselves from the semantic candidate; any later semantic mutation reopens affected qualification.

Preserve API/data/runtime/profile compatibility only where an actual supported contract requires it. Historical machinery does not become compatibility authority through existence. Retain compatibility layers only for a supported version/migration window or while they remain the minimum justified concretization.

Apply the Lossless Representation Rule: keep current operational version/recovery decisions hot and exact; keep detailed historical chronology cold but discoverable through semantic history and immutable recovery sources.