# Protocol Versioning, Historical Recovery, and Compatibility

Own protocol/workplan/profile version binding, immutable historical recovery, public-source fallback identity, Project Engineering Memory (PEM) schema/version adoption behavior, and compatibility interpretation. Detailed semantic chronology belongs in `history/SEMANTIC_EVOLUTION.md`; ordinary current work should not replay old control-plane vocabulary.

## Version classes

`source/PROTOCOL_VERSION` identifies the canonical source contract being built.

- **major** — incompatible lifecycle/authority/governing-doctrine change;
- **minor** — backward-compatible capability/doctrine/control strengthening;
- **patch** — clarification or defect correction.

Protocol 6.0 is major because D1 scientific formulation and D2 numerical-method design become first-class authority domains in a recursive D1-D4 abstraction/concretization model. Protocol 6.1 is minor: current concretization terminology, evidence lifecycle/applicability/dependency/evolution, impact closure, human-facing background/abbreviation standards, and distinct frozen/current profiles. Protocol 6.2 is a backward-compatible representation/progressive-disclosure strengthening: accepted 6.1 semantics remain required while current communication/routing is losslessly compacted and the current kernel path becomes `abstraction-and-concretization.md`.

Protocol 6.3 is a backward-compatible project-learning strengthening over 6.2: accepted 6.2 semantics remain required while evidence-backed, project-local, non-authoritative engineering memory, conditional Historical Applicability Set (HAS) use, capability-transfer/closeout learning, evidence-binding health, and branch/schema-safe memory lifecycle are added. It does not create D5 or let history/statistics/memory override D1-D4/current project/external authority.

## Capability preservation across versions

Protocol 6 generalizes Protocol 5 rather than maintaining a second current vocabulary. Restricting active scope to D3 architecture and D4 implementation recovers the former software-local design->implementation specialization. Historical Tier terms map to applicable accepted parents/constraints, cycle-scoped child decisions, delegated concretization, and development economy.

Capability, not obsolete wording, is the compatibility oracle. Every still-valid Protocol 5 safeguard remains recoverable under current generalized rules unless deliberately replaced by stronger accepted authority; compression that loses behavior is a defect. Concise lineage: 5.1 documentation specialist; 5.2 hygiene; 5.3 stage/final acceptance + separate production qualification; 5.4 development economy/version-bound plans/evidence-context reuse; 5.5 implementation fidelity; 5.6 proxy-proof acceptance; 5.7 stewardship/outcome alignment; 5.8 effective compression/canonical ownership; 5.9 portable deterministic routing; 5.10 snapshot-complete handoff; 5.11 tool-assisted engineering; 5.12 convergence/cycle economy; 5.13 deterministic tool entry/CodeQL/progressive disclosure; 5.14 solution-boundary/active simplicity; 5.15 language profiles/cross-language performance; 5.16 long-horizon health/Verification/Stabilization/maintenance audit/workflow prompts/public fallback. Detailed rationale is historical, not normal hot-path doctrine.

Protocol 6.3 additionally preserves every accepted 6.2 behavioral/representation/routing/package/profile capability. PEM is additive decision support: a version-bound 6.2 task remains valid without loading/interpreting a 6.3 project memory, and the existence of a 6.3 PEM cannot retroactively alter a 6.2 contract.

## Workplan binding, PEM adoption, and evidence reuse

Every workplan that inherits protocol behavior binds to its declared `protocol_version`. A newer installed/latest skill never silently reinterprets older work. Older active work may continue under its declared version or explicitly adopt a compatible newer version after changed obligations are reconciled. A 5.x->6.x adoption is a major migration; 6.0->6.1->6.2->6.3 are backward-compatible minor steps but still preserve explicit version identity.

For 6.2-bound work, any 6.3 `PROJECT-ENGINEERING-MEMORY.md` is inert protocol-wise: do not delete it, reinterpret it under 6.2, or let it modify 6.2 acceptance. Explicit adoption of 6.3 validates a supported memory schema, resolves the project-governed accepted/base memory, and reconciles materially relevant memory/HAS obligations from the bounded adoption scope.

PEM `memory_schema_version` is independent of SSDP protocol version and orchestration workflow-profile schema. Protocol 6.3 supports PEM schema 1. Unknown/newer/incompatible schemas fail safe for memory-dependent decisions: only explicitly forward-readable identity metadata may be inspected, and the memory-dependent decision becomes `REVIEW_REQUIRED` until a compatible reader or explicit lossless migration exists. Unsupported memory does not block unrelated protocol routes.

A restored old PEM snapshot is not current merely because it parses. Re-adoption/recovery reconciles schema, project/scope identity, accepted base, candidate overlay, owners, evidence/binding health, and the uncovered project interval. `reconciled_through` is an identity horizon, not proof of exhaustive historical coverage.

Previously executed evidence remains reusable only while no changed protocol obligation, governed claim/concretization, evidence specification/oracle, candidate, or material environment dimension can plausibly change applicability. Apply the evidence owner; version adoption does not automatically invalidate unrelated evidence.

## Immutable historical recovery

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639
6.2.0  -> b59adc77efe6951912cfd705cc43830c58ca27d0
6.3.0  -> 9f353097fab36e325a325f1c2f9d9cec32e86177
```

Resolve historical work through immutable version-specific source/profile semantics, never `main`/latest. Frozen source/publication/profile artifacts remain historical truth and are not rewritten to current terminology. Protocol 6.3 must not mutate any frozen 5.16/6.0/6.1/6.2 resource; 6.3 receives new versioned resources after qualification.

Protocol 6.1 public-source bootstrap is distinct from recovery:

```text
repository -> https://github.com/hjin98/scientific-software-development-protocol
6.1.0 public-source bootstrap -> 47e9155632c44493644b0b02fa1fa625703cf480
```

The first Protocol 6.2 pre-acceptance bootstrap attempt was later invalidated by a required routing repair, and the repaired replacement bootstrap was validated before publication:

```text
6.2.0 invalidated bootstrap attempt -> 1181c2031710c5d343194d87d08543290fded0ab
6.2.0 public-source bootstrap -> 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
```

The invalidated SHA remains historical implementation evidence only and **must not** be used as current Protocol 6.2 public fallback. The replacement SHA is the immutable self-reference-safe source snapshot whose source regression, canonical package build, and independent standalone package/link validation passed before this descendant published it.

Protocol 6.3 replacement public-source bootstrap is likewise distinct from future recovery:

```text
6.3.0 invalidated bootstrap attempt -> 1484c1d3caa49d87cc15bc52a5e775399c1dae1b
6.3.0 invalidated second bootstrap -> 5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb
6.3.0 invalidated owner-binding bootstrap -> e12572c021087308570abfa41657a910c6896457
6.3.0 invalidated D4R3 bootstrap -> dc22f09fd38dbbfeaeb0160152da9b284654f66e
6.3.0 public-source bootstrap -> 86c13cab6bdd1991dffa94e277db8eacf87e2e11
```

The pre-repair Protocol 6.3 bootstrap remains immutable historical evidence only and must not be used as current fallback. The value on the `public-source bootstrap` line is the sole current 6.3 fallback mapping: an unavailable sentinel means no replacement fallback is published, while an immutable Git SHA means the already-existing self-reference-safe snapshot passed repository regression, canonical package build, independent package validation and committed-distribution parity, Protocol 6.3 profile/snapshot parity, the full Orchestrator Core acceptance suite, and exact-ref remote source/route realization before a later descendant published it. Protocol 6.3 recovery is separately mapped to `9f353097fab36e325a325f1c2f9d9cec32e86177` after independent Review R2 PASS. Bootstrap and recovery identities are distinct. Mapping-bearing generated descendants were regenerated at `e75282ae850b774a9466902f4c74ba6a179116bd`, and Stage G recovery/parity/package/profile/Core acceptance passed in GitHub Actions run `34699052516`. Protocol 6.3 is accepted-current after lifecycle closeout; Protocol 6.2 remains immutable historical rollback authority for version-bound 6.2 work.

The repository default branch is never a protocol-version oracle and a semantic version string is not assumed to be a Git ref.

## Orchestration profiles

Profiles remain independently version-bound:

| Profile | Protocol | Schema | State |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen historical |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen historical |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | frozen historical rollback |
| `ssdp-protocol-6.2` | 6.2.0 | 2 | frozen historical rollback |
| `ssdp-protocol-6.3` | 6.3.0 | 2 | accepted current |

Protocol 6.3 is accepted-current. The 6.2 profile bytes remain frozen as an immutable predecessor/rollback resource. Schema v2 remains because no machine profile contract changed. Core selects by declared protocol/profile identity, not one global latest constant. Frozen profile bytes/behavior remain independently testable. A generic profile/package may include 6.3 PEM doctrine/template but never a live project's `PROJECT-ENGINEERING-MEMORY.md` or derived local project summary.

## Protocol 6.2 public-source and recovery staging

The replacement public-source bootstrap is `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`. When `AUTO_LOCAL_FIRST` finds no governing-version-compatible installed source, current accepted Protocol 6.2 may fall back to the canonical repository at **that exact immutable ref**. Never use the invalidated attempt, `main`, latest, or a guessed semantic-version ref. The bootstrap source itself intentionally does not self-name; its later descendant mapping is the authority for the exact ref.

The accepted Protocol 6.2 recovery target is:

```text
6.2.0 -> b59adc77efe6951912cfd705cc43830c58ca27d0
```

That immutable commit contains semantic candidate `ebbc4591bdfed039512026b8acb3a6749475c1c5` through ancestry together with its qualification/requalification/generated evidence and independent Review PASS. The public-source bootstrap remains `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` and is intentionally distinct from recovery identity.

Git commits cannot self-name, so the recovery mapping was published only by later descendant mapping commit `bc76b16fda96be09f38a1b40a2ef877e8309534d` after the recovery target already existed. Mapping-bearing generated descendants were regenerated at `ca622ea2b1c33e70668060cf0cc2fe9138776f7f`, and Stage G recovery/parity/package/Core acceptance passed in GitHub Actions run `34566291966`.

Protocol 6.2 is accepted-current after qualification, independent Review, immutable recovery mapping, generated-artifact reconciliation, semantic-evolution/Protocol-7 handoff reconciliation, and lifecycle closeout. Protocol 6.1 remains immutable historical rollback authority at `802e75af261efb4f70d71284d860613a2197b639` for version-bound 6.1 work.

## Protocol 6.3 accepted bootstrap/recovery lifecycle

Protocol 6.3 follows the same self-reference-safe separation learned from 6.2, with stronger memory/version separation:

1. build the semantic/source candidate and self-hosted **candidate** PEM without claiming recovery;
2. run source regression, 6.3 schema/route/counterfactual tests, inherited qualification, package/profile/Core integrity, static sensors and required falsification passes on the assembled candidate;
3. qualify an already-existing self-reference-safe replacement public-source snapshot before publishing its exact immutable identity from a later descendant; never substitute `main`/latest/guessed version or an invalidated attempt;
4. generate a new `ssdp-protocol-6.3` profile/prompts/snapshots without altering frozen 6.2 bytes;
5. perform independent Protocol 6.3 Review against the assembled candidate and accepted 6.2 baseline;
6. only after all required acceptance/Review/impact items pass, establish an immutable 6.3 recovery target and publish its mapping from a descendant commit because a commit cannot self-name;
7. regenerate mapping-bearing descendants and rerun recovery/parity/package/Core acceptance before any accepted-current cutover.

The pre-repair Protocol 6.3 bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, second bootstrap `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding bootstrap `e12572c021087308570abfa41657a910c6896457`, and D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e` remain immutable historical evidence only. D9 changed canonical validator semantics, so Replacement self-reference-safe source snapshot `86c13cab6bdd1991dffa94e277db8eacf87e2e11` passed source regression, package/profile integrity, Orchestrator Core, and bootstrap readiness before descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e` published its exact SHA as the sole current 6.3 public-source fallback. Independent Review R2/recovery target `9f353097fab36e325a325f1c2f9d9cec32e86177` is intentionally distinct; descendant `0c76c0461b7376f17182d29ba145a198a092463c` published the recovery mapping, mapping-bearing descendants were regenerated at `e75282ae850b774a9466902f4c74ba6a179116bd`, and Stage G acceptance passed in run `34699052516`. Protocol 6.3 is accepted-current; version-bound 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0` remains immutable historical rollback. The public bootstrap is not recovery.

## Candidate identity and compatibility

For normal Git repositories, semantic candidate commit plus absence of unintended product-defining changes is usually sufficient source identity. Later qualification/lifecycle/PEM-reconciliation commits must distinguish themselves from the semantic candidate; any later semantic mutation reopens affected qualification. A branch-local PEM overlay is likewise not accepted/base merely because it shares the candidate branch.

Preserve API/data/runtime/profile compatibility only where an actual supported contract requires it. Historical machinery does not become compatibility authority through existence or PEM recording. Retain compatibility layers only for a supported version/migration window or while they remain the minimum justified concretization.

Apply the Lossless Representation Rule: keep current operational version/recovery decisions hot and exact; keep detailed historical chronology cold but discoverable through semantic history and immutable recovery sources.
