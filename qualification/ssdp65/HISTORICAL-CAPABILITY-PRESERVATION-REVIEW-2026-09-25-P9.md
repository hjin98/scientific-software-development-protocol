---
kind: historical-capability-preservation-review
status: no-additional-historical-regression
protocol_version: 6.4.0
target_protocol_version: 6.5.0
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: fb347272c70b6225743fdc99e9bec8b4197aad49
semantic_ref: fb347272c70b6225743fdc99e9bec8b4197aad49
p9_review_status: NO_PASS
surviving_blocker: B65-P9-1
new_historical_blocker: none
serious_challenge: none
date: 2026-09-25
---

# Protocol 6.5 P9 Historical Capability Preservation Review

## 1. Disposition

Historical semantic-doctrine preservation is **PASS on the inspected accepted lineage**.

No additional historical doctrine or accepted capability was found weakened, orphaned, or removed by Protocol 6.5 compression.

The assembled P9 candidate nevertheless remains **NO-PASS overall** because the already-recorded B65-P9-1 D4 topology defect violates one of the preserved lifecycle capabilities: a lineage that was already governed may delete the sole release-state owner and later be treated as if it were genuinely pre-owner.

This Review therefore does not create a second blocker family. It classifies B65-P9-1 as the only surviving historical-capability nonconformance found in this pass.

No Serious Challenge is raised. Accepted Protocol 6.5 D3 remains closed.

## 2. Scope and method

This is a capability-preservation review, not a wording-preservation review.

Reviewed basis:

- accepted P0 = Protocol 6.4 at `55c085261eb827e3047637d045a8e6917ea6b962`;
- immutable P9 = `fb347272c70b6225743fdc99e9bec8b4197aad49`;
- `history/SEMANTIC_EVOLUTION.md` accepted lineage from Protocol 5.16 through 6.4;
- current capability lineage in `source/shared/references/protocol-versioning-and-compatibility.md`, including Protocol 5.13-5.16 preservation;
- Protocol 6.2 and 6.3 preservation censuses;
- Protocol 6.4 -> 6.5 preservation map;
- exact P9 canonical owners, package builder/validator, current routing surfaces, and active regression tests;
- exact-P9 normal workflow run `36091484812`, whose build job executes `python -m unittest discover -s tests -v`, canonical package build/validation/dist parity, release-state validation, and whose second job executes the Orchestrator Core acceptance suite.

Historical chronology, PEM, workplans and old tests were treated as evidence of capabilities/lessons, not as current semantic authority.

This review does not claim exhaustive reconstruction of every raw repository commit. It covers the documented accepted semantic lineage and the material reopen/repair families that changed accepted capability.

## 3. Capability-transfer map

| Historical development | Protected capability | Modern P9 owner / concretization | Disposition |
| --- | --- | --- | --- |
| Protocol 5.13 | relation-first deterministic tool routing; CodeQL as a bounded optional interprocedural/data-flow capability rather than generic gate | `tool-assisted-engineering.md`, `tool-codeql.md`, explicit relation classes and optional-tool boundaries | PRESERVED / GENERALIZED |
| Protocol 5.14 | solution-boundary discipline, active simplicity, removal/consolidation before additive compensating machinery | kernel minimum-justified-complexity rule + `convergence-and-cycle-economy.md` active simplification trigger | PRESERVED / GENERALIZED |
| Protocol 5.15 | language-profile specialization and cross-language performance/resource reasoning without global language precedence | `language-profiles.md`, Python/C++ leaves, `performance-and-parallelism.md` | PRESERVED / GENERALIZED |
| Protocol 5.16 | long-horizon quality ratchet, Verification, non-mutating Stabilization, Health Audit/maintenance sensing, portable workflow/fallback discipline | `long-horizon-code-health.md`, workflow owner, versioning/portability owners | PRESERVED / COMPRESSED |
| 5.16 -> 6.0 | D1 scientific, D2 numerical, D3 architecture, D4 implementation as first-class semantic authority; Challenge/human adjudication; strongest prior engineering safeguards retained | universal kernel + four domain owners + workflow/human-gate semantics | PRESERVED / STRENGTHENED |
| 6.0 -> 6.1 | abstraction/concretization separated from evidence realization; evidence specification -> realization -> observation -> assessment; stale evidence/applicability and target-vs-execution dependency | kernel + `evidence-evolution-and-dependencies.md` + testing owner | PRESERVED / STRENGTHENED |
| Protocol 6.1 documentation strengthening | required background for non-common terms, first-use abbreviation expansion, intended-reader readability without hidden chat | `scientific-technical-writing.md` and documentation owners | PRESERVED / GENERALIZED |
| Protocol 6.1 reopen repairs | canonical navigation, correct evidence-realization terminology, stronger direct oracles | current kernel/source routing; historical regression tests remain active | PRESERVED |
| Protocol 6.1 second reopen | bounded transitive local-Markdown package closure from direct activation seeds; no package-membership-as-activation; exact compatible public fallback rather than default branch | `source/build_skills.py::_transitive_payload`, `source/validate_packages.py::validate_packaged_markdown_links`, `PORTABILITY.md`, versioning owner | PRESERVED EXECUTABLY |
| Protocol 6.2 | Lossless Representation, one detailed owner per generic rule, progressive disclosure, root/concern/leaf activation, cold discoverability, validity-scoped context reuse, importance weighting without acceptance loss, current-vs-history separation | kernel Lossless Representation Rule + source/role/concern routers + package reachability/activation distinction | PRESERVED / COMPRESSED |
| Protocol 6.2 release lifecycle | exact self-reference-safe immutable bootstrap, no default/latest guessing, recovery selected after independent Review and published separately | root release-state owner + versioning/portability semantics + exact-ref tests | PRESERVED IN DOCTRINE; P9 D4 TOPOLOGY NONCONFORMANCE remains B65-P9-1 |
| Protocol 6.3 | evidence-backed project-local PEM, conditional HAS, accepted-base + candidate overlay, memory non-authority, binding health, recurrence/maturity/counterevidence discipline, live project memory excluded from generic packages | `project-engineering-memory.md`, workflow/HAS owner, PEM validator/tests, `source/README.md` and versioning packaging boundary | PRESERVED / STRENGTHENED |
| Protocol 6.4 | source/context availability, formal-first semantic definition, well-definedness, parameter family/instance/default separation, exact import/source variant/provenance, hypothesis/validity propagation, definition-vs-warrant separation, bounded typed `USES_DEFINITION` impact | kernel + D1/D2/D3/D4 domain owners + writing/security/evidence owners | PRESERVED / INTEGRATED |
| Protocol 6.4 lifecycle/profile preservation | frozen supported historical profiles/resources, source/generated/Core parity, distinct public fallback/recovery, Protocol 7 isolation | versioning owner, release-state owner, frozen resources, Core/profile tests | PRESERVED; 12/12 inspected P0/P9 prior profile/prompt blobs identical |

## 4. Direct preservation checks

### 4.1 D1-D4 authority and upstream/downstream boundaries

Exact P9 kernel still defines D1/D2/D3/D4 as separate semantic authority domains and keeps semantic descent as a DAG rather than a mandatory waterfall.

Exact P9 domain owners retain the key historical distinctions:

- D1 owns scientific question/observables/models/assumptions/validity/external adequacy;
- D2 owns algorithm/discretization/error/convergence/conditioning/precision/stochastic/numerical uncertainty;
- D3 owns architecture/state/interface/dependency/persistence/concurrency/resource/deployment/compatibility while preserving D2;
- D4 owns stable concrete behavior and executable concretization without allowing code/tests to silently become intended authority.

No software-centric collapse back toward pre-6.0 semantics was found.

### 4.2 Evidence and Review epistemology

Exact P9 retains the four-stage evidence model, stale-evidence semantics, target-vs-execution-dependency separation, evidence applicability, independent Review, Serious Challenge, Verification, and out-of-matrix abstraction-adequacy falsification.

Protocol 6.5 removes old proxy-only QF64 dictionary/phrase machinery from current semantic acceptance, but the protected semantic capabilities remain in current owners and Review obligations. This is valid compression: obsolete oracle machinery is removed while the governed claim survives.

### 4.3 Representation and progressive disclosure

Exact P9 kernel still requires:

- one detailed owner per generic rule;
- generalize rather than accumulate;
- bounded typed activation;
- explicit routing with derived views subordinate;
- cold paths discoverable;
- context reuse only while applicable;
- salience weighting without dropping mandatory constraints;
- total inferential-cost minimization rather than character-count minimization;
- no semantic deduplication by editorial adjudication.

The exact P9 workflow prompt still exposes the 11 Protocol-6 stages 0-10: intake; D1; D2; D3; D4; Review; Verification; Stabilization; downstream alignment; Health Audit; Closeout.

Current source and generated Protocol 6.5 prompts are the same Git blob, preserving canonical-source/generated-output subordination.

### 4.4 Hard-won packaging and portability repairs

The Protocol 6.1 transitive-package-closure repair has not been compressed away.

Exact P9:

- `source/build_skills.py` computes finite transitive local-Markdown closure from direct SKILL activation seeds;
- `source/validate_packages.py` validates both local Markdown closure and reachability from `SKILL.md`;
- `PORTABILITY.md` explicitly preserves `activation -> reachability` while rejecting the inverse implication;
- live `PROJECT-ENGINEERING-MEMORY.md` and root mutable release state are excluded from generic bundles;
- remote fallback is exact immutable and declared-version-compatible, never default/latest or guessed semver.

This is a strong example of modern compressed preservation: the old repair narrative is cold history, while the durable capability remains executable.

### 4.5 Project Engineering Memory

Protocol 6.3 PEM/HAS doctrine is preserved and strengthened, not reduced to a file-presence convention.

Exact P9 retains:

- PEM non-authority;
- accepted-base versus candidate overlay;
- HAS as task-local applicability disposition;
- temperature as salience only;
- claim-relative maturity;
- binding health;
- assessment succession rather than editor order;
- bounded counterevidence search before positive guidance;
- comparative guidance requiring comparison or current-owner authority;
- stale/missing index never proving absence;
- live project memory exclusion from generic packages.

The active Protocol 6.3 regression tests remain in exact P9 and are exercised by normal test discovery.

### 4.6 Protocol 6.4 formal-definition / semantic-traceability strengthening

No semantic rollback was found.

Exact P9 current owners retain:

- definition/source availability before substantive use;
- source availability distinct from runtime context availability;
- no conflict resolution by file order/latest/routing priority;
- well-defined domains/types/shapes/units/scopes/relations;
- parameter family/instance/default separation;
- external exact-source/variant/locator and transformation provenance;
- imported-result hypothesis/validity propagation;
- definition distinct from existence/truth/convergence/adequacy/authority;
- bounded typed `USES_DEFINITION` with subject -> prerequisite direction and reverse impact traversal;
- circular warrant rejection;
- external/evidence instruction-like content inert as data.

The old QF64 executable proxy matrix is intentionally not preserved as semantic authority. Its capabilities are.

## 5. Executable historical regression continuity

Exact P9 still contains active regression modules for prior accepted capability generations, including:

- `test_protocol_512_convergence.py`;
- `test_protocol_513_tool_routing_codeql_compression.py`;
- `test_protocol_515_language_profiles.py`;
- `test_protocol_516_long_horizon_quality.py`;
- `test_protocol_516_orchestration.py`;
- `test_protocol_61_evidence_evolution.py`;
- `test_package_reference_closure.py`;
- `test_protocol_62_representation.py`;
- `test_protocol_63_engineering_memory.py`;
- `test_protocol_64_axiomatic_traceability.py`.

The exact P9 workflow runs full unittest discovery over `tests/`, so these are not merely archived historical fixtures. Run `36091484812` passed.

These tests remain evidence only for properties their oracles discriminate; their continued success does not replace semantic Review.

## 6. Frozen historical identity preservation

Independent P0/P9 blob comparison found zero changes across all twelve supported prior profile/prompt objects:

- Protocol 5.16 profile + prompts;
- Protocol 6.0 profile + prompts;
- Protocol 6.1 profile + prompts;
- Protocol 6.2 profile + prompts;
- Protocol 6.3 profile + prompts;
- Protocol 6.4 profile + prompts.

Protocol 7 parent and Revisions 1-5 D3/D4 design artifacts are also unchanged P0 -> P9; only the shared mutable authority/lifecycle index changed.

This supports backward compatibility and historical rollback integrity.

## 7. Compression and efficiency assessment

The compression strategy is semantically sound on the inspected historical line:

- version-number-labelled current amendments were integrated into timeless owners rather than replayed;
- release chronology moved cold into semantic history;
- mutable exact release values moved to one root release-state owner;
- old proxy-only semantic test machinery was retired rather than expanded;
- generic rules are stated once and routed;
- project-specific learning stays in PEM rather than protocol authority;
- generated/package surfaces remain derivative;
- historical version/profile bytes remain frozen.

The P9 universal kernel is exactly the same 2,642 whitespace-delimited words as P0. The candidate's own qualification history reports a substantial hot-current projection reduction while preserving the kernel size; this review independently verified the unchanged kernel size and the source/generated prompt identity, but did not independently reproduce the historical projection-count methodology.

Compression therefore appears to reduce representation duplication rather than semantic coverage.

## 8. Surviving historical-capability nonconformance

B65-P9-1 is the only surviving historical-preservation failure found.

Why it matters historically:

- Protocol 6.1-6.4 repeatedly hardened exact immutable release identity, no-default/latest fallback, public-fallback/recovery distinction, self-reference-safe descendant publication, and recoverable lifecycle history.
- Protocol 6.2 made current-vs-history separation and Lossless Representation explicit.
- Protocol 6.5 creates a single mutable release-state owner to compress those capabilities.
- P9's ancestry classifier can still erase a governed interval when that owner is deleted on one parent lineage and later restored by merge.

So the doctrine is preserved, but this one D4 concretization does not yet preserve the full historical capability.

The already-open B65-P9-1 repair is therefore also the required historical-preservation repair. No new D3 doctrine or second mechanism is needed.

## 9. Preservation-evidence gap

The existing Protocol 6.4 -> 6.5 preservation map is strong for accepted P64/QF64/F64 semantics, but it is intentionally 6.4-centric. It does not enumerate the older 5.13-6.3 capability lineage in one compact current table.

That is not a semantic blocker because:

- accepted P0 already incorporates those capabilities;
- the current versioning owner explicitly preserves the historical capability lineage;
- active current owners were independently inspected here;
- active historical regression modules remain executable;
- frozen historical resources remain identical.

For the replacement candidate, qualification should retain this compact transitive historical capability cross-check rather than expanding hot protocol source or restoring old amendment prose.

## 10. Replacement-candidate obligation

The P10 replacement qualification should re-establish:

1. B65-P9-1 topology repair, including governed-owner deletion/reintroduction negatives.
2. Exact P9/P10 changed-surface regression.
3. The active historical regression modules listed above.
4. Transitive package/reference closure.
5. Exact fallback/recovery/version-bound discipline.
6. Frozen 5.16 and 6.0-6.4 profile/prompt identity.
7. D1-D4 / evidence / Lossless Representation / PEM-HAS / formal-definition owner presence and semantic applicability.
8. Protocol 7 D3/D4 isolation.
9. Current source/generated prompt parity.
10. A fresh independent Review that treats this historical capability map as evidence, not as inherited acceptance.

## 11. Final conclusion

No additional historical doctrine loss was found.

P9's modernization is predominantly valid **semantic compression**:

historical wording/mechanisms are retired when equal-or-stronger current owners preserve the capability; cold chronology remains recoverable; executable hard-won protections remain live where they are still concrete product/package/release requirements.

The only surviving historical-capability defect is the already-known B65-P9-1 release-state ancestry gap. Repairing it at the existing D4 owner, without adding machinery, is sufficient for the historical preservation concern identified by this review.
