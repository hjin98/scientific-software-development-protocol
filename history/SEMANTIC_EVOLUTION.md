# SSDP Semantic Evolution History

This file preserves concise semantic reasons for material protocol evolution that ordinary Git chronology cannot explain economically. It is historical context, not a second current authority. Current normative truth remains in the accepted Protocol source and version-bound profiles.

## Background

The **Scientific Software Development Protocol (SSDP)** evolves by preserving accepted scientific/software capability while replacing weaker abstractions, delegated mechanisms, or workflow conventions when evidence or broader doctrine justifies the change.

Historical entries identify the previous semantics, replacement, triggering evidence or rationale, affected surfaces, and disposition. Release-pinned work remains governed by its own version even when newer protocol semantics supersede the current default.

---

## Protocol 5.16 -> Protocol 6.0

- **Change:** software-centric two-role protocol generalized to four scientific-software semantic domains: D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation.
- **Previous semantics:** Protocol 5 focused primarily on software design/implementation with upstream scientific/numerical semantics treated as external context.
- **Replacement:** recursive abstraction/realization doctrine across D1-D4, with explicit authority/challenge/human-ratification semantics and lossless inheritance of the strongest Protocol 5 engineering safeguards.
- **Reason:** scientific software requires scientific and numerical authority to be explicit first-class owners rather than implicit prerequisites of software work.
- **Historical authority:** `workplans/archive/SSDP-6-AUTHORITY.md` and its referenced transition workplans.
- **Recovery identity:** Protocol 5.16 remains pinned to `e151daaf5c8eebb351a85cfed86170fda80fb5e3`.

## Protocol 6.0 -> Protocol 6.1

- **Change:** current semantic-descent terminology changes from `abstraction <-> realization` to `abstraction <-> concretization`; `realization` is reserved for concrete evidence execution.
- **Previous semantics:** `realization` named both downstream scientific/software choices and concrete evidence execution in adjacent discussion, creating terminology collision.
- **Replacement:**
  - abstraction/concretization for D1-D4 semantic descent;
  - evidence specification -> evidence realization -> observation -> evidence assessment for evidentiary activity.
- **Reason:** evidence is as important as the models it interrogates, and the two relations require unambiguous vocabulary before dependency/evolution tracking can become machine-readable in a later major release.
- **Compatibility:** Protocol 6.0 release-pinned artifacts and opaque compatibility identifiers retain their historical lexemes. Current Protocol 6.1 prose uses the new terms.
- **Affected current surfaces:** governing authority/challenge reference, D1-D4 and support skills, testing/workflow/documentation/versioning references, method-paper/workplan templates, current prompts/README/portability documentation, qualification scenarios, generated skill packages, and the Protocol 6.1 orchestration profile.

### Evidence, dependency, and history strengthening

- **Change:** evidence becomes an explicit evolving structure linked to authority/concretization rather than an undifferentiated set of tests/results.
- **Replacement doctrine:** Authority-Evidence-Evolution model with typed semantic dependencies, evidence applicability/admissibility states, explicit stale-test semantics, evidentiary-target versus execution-dependency separation, durability and common-mode-risk guidance, bounded impact closure, and semantic evolution history.
- **Reason:** a stale passing test can fabricate confidence just as a stale implementation can create competing apparent authority. Model evolution must therefore propagate to dependent evidence and historical reasoning as well as code/document concretizations.
- **Boundary:** Protocol 6.1 uses lightweight Markdown dependency/history records only where they materially improve reasoning. It does not introduce a mandatory graph database, JSON control plane, or machine-authoritative reducer.

### Human-facing documentation strengthening

- **Change:** newly introduced non-common domain terminology must receive concise background definition/explanation for the intended competent reader; non-obvious abbreviations use first-use `full term (ABC)` expansion.
- **Reason:** D1/D2 method papers and other human-facing semantic documents must be interpretable without hidden chat or assumed project jargon. Documentation clarity is part of truthful semantic communication, while precise normative definitions remain owned by D1-D4.
- **Boundary:** release-pinned historical documents are not rewritten solely to satisfy later presentation standards; machine-only identifiers/data records are not polluted with pedagogical prose, but their human-facing documentation must explain non-obvious meaning.

### Version/profile disposition

- **Protocol 6.0 recovery identity:** the accepted pre-6.1 source/profile baseline is repository commit `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`.
- **Profile policy:** packaged `ssdp-protocol-6.0` remains frozen/resolvable for declared Protocol 6.0 work. Protocol 6.1 introduces distinct current profile identity `ssdp-protocol-6.1` under profile schema v2 unless a future accepted change requires a schema revision.
- **Protocol 6.1 semantic candidate:** `25d30858e7a33a72cb04b4d07393cb143b7777f8` is the qualified semantic candidate identified by the final independent Review.
- **Protocol 6.1 immutable recovery identity:** lifecycle-closeout commit `dec5ff2767e14fd1cda46e073757aa27f40e270c` is the accepted pre-automation rollback snapshot. It preserves the qualified 6.1 source/profile/generated artifacts, final evidence/review records, and archived 6.1 handoff without Protocol 7 implementation machinery.
- **Protocol 7 dependency:** Protocol 6.1 is the final stable document-controlled/semi-automated release and immutable rollback baseline for the later mandatory deterministic orchestrator control-plane migration.

### Protocol 6.1 closeout evidence

- **Behavioral qualification:** 92 bounded scenarios, no unresolved failure; scenario 82 was explicitly requalified after its owning relation-token repair rather than retaining stale green evidence.
- **Independent Review:** PASS; no active Serious Challenge and zero blocking findings open.
- **Executable acceptance:** repository regression, canonical package build, package validation, committed-distribution parity, whitespace, Protocol snapshot parity, and Orchestrator Core all passed on the reviewed candidate/evidence chain.
- **Lifecycle disposition:** the two governing 6.1 workplans are archived as exact reviewed historical handoff artifacts. Their pre-closeout frontmatter is preserved rather than edited after Review; current completion is recorded by repository placement, the active 6.1/7.0 authority index, this evolution record, and the final Review.

## Protocol 6.1 reopened final-review repair

A later independent post-closeout review superseded the release/rollback disposition stated in the preceding closeout entry without rewriting that historical evidence.

- **Reopen trigger:** the closed candidate still used `concretization` for evidence execution in current D3/D4 role prose and routed the canonical source README to nonexistent `shared/references/abstraction-and-concretization.md`. The acceptance oracle also lacked direct counterexamples for those failure classes.
- **Historical candidate/recovery disposition:** `25d30858e7a33a72cb04b4d07393cb143b7777f8` and `dec5ff2767e14fd1cda46e073757aa27f40e270c` remain immutable evidence of the earlier closeout, but they are **superseded for current Protocol 6.1 release/recovery authority** and are not the final accepted rollback baseline.
- **Repaired semantic candidate:** `5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef`. The source repair corrects the D3/D4 evidence-realization terminology and README navigation, strengthens direct regression/behavioral oracles, and regenerates the affected D3/D4 ZIP transports from canonical source without changing Protocol 6.1 doctrine.
- **Executable acceptance:** PASS for full repository regression, canonical package build, independent package validation, committed-distribution parity, whitespace, Protocol snapshot parity, Orchestrator Core acceptance, and exact two-ZIP generated-artifact scope in GitHub Actions run `34428272223`. Temporary transport machinery was removed from the final candidate tree.
- **Behavioral qualification:** fresh 94/94 PASS, zero failures, no Serious Challenge; result recorded in commit `d1a6e0fe9fe37d70b2bc72e13332d14891ca034b` and explicitly bound to semantic candidate `5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef`.
- **Independent Review:** fresh PASS with no Serious Challenge and zero open blockers; record `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-09-PROTOCOL-6.1-REOPENED.md`, committed as `2dea21d62bed9f87df4ad168fdaa9d1544024040`. That Review found one additional stale semantic-history lifecycle claim, repaired at the documentation/history owner without mutating the semantic candidate before the final PASS disposition.
- **Lifecycle disposition:** reopened repair workplan archived after all required acceptance, qualification, and Review gates passed. Replacement immutable Protocol 6.1 document-controlled/semi-automated recovery snapshot is commit `0c90fda19bf6ed9cb0c4511beb3da80ace6584ed`.
- **Protocol 7 dependency:** the Protocol 6.1 completion/qualification/recovery prerequisite is satisfied by recovery commit `0c90fda19bf6ed9cb0c4511beb3da80ace6584ed`. Protocol 7 D4 implementation remains separately blocked on its deliberate D3 Orchestrator architecture reopen/supersession prerequisite.

## Protocol 6.1 second reopened portability/documentation/recovery repair

A subsequent Protocol-6.1-self-review reopened release closure again after finding three bounded implementation/acceptance defects: packaged references could contain unresolved nested Markdown routes that the validator did not inspect; current public fallback named the repository but could land on the incompatible Protocol 6.0 default branch; and the accepted human-facing background standard was not consistently applied to current Protocol-owned entrypoints/evidence reports.

- **Authority disposition:** no D1/D2/D3 semantic doctrine changed and no Serious Challenge was active. The repair remained bounded to D4 packaging/validation, documentation concretization, public-source version resolution, and lifecycle/recovery evidence.
- **Prior closeout disposition:** semantic candidate `5f911fecb0de2847f63c0b4859e1dd8c63d3d8ef` and recovery `0c90fda19bf6ed9cb0c4511beb3da80ace6584ed` remain immutable historical evidence but are superseded for final release/recovery authority.
- **Repair authority:** `workplans/archive/SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR.md` plus `workplans/archive/SSDP-6.1-SECOND-REOPENED-PORTABILITY-DOCUMENTATION-AND-RECOVERY-REPAIR-REVISION-1-PACKAGE-CLOSURE.md`. Revision 1 superseded only the direct-only package-membership mechanics with bounded transitive local-Markdown closure from direct activation seeds.
- **Public-source bootstrap:** `47e9155632c44493644b0b02fa1fa625703cf480`; current 6.1 web/manual fallback resolves this immutable compatible source instead of repository-default bytes.
- **Qualified semantic candidate:** `be7d05827f52a3029c294c38edf5ede1afb1f9b4`. It contains the repaired package/public-fallback/documentation behavior and differs from Stage-B semantic source `79abb7963166f57ffd4b7df93bd7c1ba8ef3c11b` only by the pre-qualification `PORTABILITY.md` scenario-count correction.
- **Behavioral qualification:** fresh 95/95 PASS, zero failures, no Serious Challenge; result committed as `48771f9235232bf59428d78686d116ef52965571` and explicitly bound to semantic candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4`.
- **Independent Review:** fresh PASS, no Serious Challenge, zero open blockers; record `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED.md`, committed as `802e75af261efb4f70d71284d860613a2197b639`.
- **Replacement recovery identity:** `802e75af261efb4f70d71284d860613a2197b639`. This immutable commit contains the accepted semantic candidate through ancestry together with the fresh 95-scenario qualification and independent Review needed to interpret rollback.
- **Recovery mapping:** current `source/shared/references/protocol-versioning-and-compatibility.md` and `PORTABILITY.md` publish recovery `802e75af261efb4f70d71284d860613a2197b639`; mapping commit `dfc09bb54cd407f64e4b2a07f1bba0a1e4f76b3c` established the exact identity after Review without attempting impossible self-reference.
- **Stage-D mapping acceptance:** GitHub Actions run `34451700073` passed targeted recovery-mapping checks, full repository regression, canonical package regeneration, independent package validation, committed-distribution parity, whitespace, Protocol snapshot parity, and Orchestrator Core acceptance. Generated recovery-mapped distribution commit `5458b1be2b536b83b6854ab9906602acc5f5f0c4` contains only the expected generated versioning-reference copies and ZIP transports; temporary transport workflow machinery has no final-tree presence.
- **Lifecycle disposition:** COMPLETED / ARCHIVED. The second-reopen parent and package-closure amendment are moved byte-identically from `workplans/active/` to `workplans/archive/`; their historical frontmatter is intentionally preserved. Their blobs remain `9158365969a8aa3564e4edd7c3f4d1355c033992` and `31d8d9800fb05ca74887141d59c5a6885d2b94bb` respectively.
- **Protocol 7 dependency:** the Protocol 6.1 completion/qualification/recovery prerequisite is satisfied by recovery commit `802e75af261efb4f70d71284d860613a2197b639`. Protocol 7 D4 implementation remains separately unauthorized until the deliberate D3 Orchestrator architecture reopen/supersession prerequisite closes.


## Protocol 6.1 -> Protocol 6.2

Protocol 6.2 strengthens representation and progressive disclosure without retiring any accepted Protocol 6.1 doctrine or still-valid historical capability.

- **Change:** current protocol communication is normalized around one canonical detailed owner per generic rule, a minimal universal kernel, explicit bounded root/concern/leaf activation, visible cold-path retrieval, validity-scoped context reuse, importance-weighted salience without acceptance loss, and current-vs-history separation. Current semantic descent uses `abstraction-and-concretization.md`; frozen historical profiles/paths retain their original identifiers and bytes.
- **Preservation:** the accepted Protocol 6.1 baseline is `cec29671b9db59d20124a6e2ce99725ed60b8f0a`. The finite preservation census and T01-T39 transformation map were independently falsified against that baseline; no accepted capability was found weakened, orphaned, or retired for compaction convenience.
- **Public-source staging:** first bootstrap attempt `1181c2031710c5d343194d87d08543290fded0ab` was invalidated after an explicit documentation cold-route defect was found. Replacement self-reference-safe public bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` contains the repaired route set and was validated before later publication; current public fallback resolves only to this exact bootstrap, never default/latest.
- **Qualified semantic candidate:** `ebbc4591bdfed039512026b8acb3a6749475c1c5`. Qualification comprises the original 115/115 behavioral pass plus bounded cold-route and bootstrap affected requalifications. Static activation sensors are structural proxies only; the release makes no unsupported live token, latency, cache, or model-performance claim.
- **Independent Review:** PASS with no Serious Challenge and no blockers; record `qualification/ssdp6/FINAL-REVIEW-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2.md`. Immutable recovery is `b59adc77efe6951912cfd705cc43830c58ca27d0`, chosen only after the independent PASS so the accepted candidate and required decision evidence are present through ancestry.
- **Recovery publication:** mapping commit `bc76b16fda96be09f38a1b40a2ef877e8309534d` publishes `6.2.0 -> b59adc77efe6951912cfd705cc43830c58ca27d0` only after the recovery target exists. Mapping-bearing distributions were regenerated at `ca622ea2b1c33e70668060cf0cc2fe9138776f7f`. Stage G targeted recovery/parity, source regression, canonical package build/validation, committed distribution parity, snapshot parity and Orchestrator Core acceptance passed in GitHub Actions run `34566291966`.
- **Protocol 7 reconciliation:** active Revision 3 changes only the inherited document-controlled baseline/representation contract from Protocol 6.1 to accepted Protocol 6.2. It does not change the proposed deterministic-control-plane D3 architecture and does not authorize D4. Protocol 7 remains blocked on its pre-existing deliberate D3 Orchestrator architecture reopen/supersession requirement.
- **Lifecycle disposition:** COMPLETED / ARCHIVED after current authority/version/portability/dependency/history/index surfaces were reconciled, the Protocol 6.2 workplan was moved byte-identically to `workplans/archive/`, generated descendants were rebuilt from canonical source, and final repository/Core acceptance passed. Protocol 6.2 is accepted-current; Protocol 6.1 recovery `802e75af261efb4f70d71284d860613a2197b639` remains immutable historical rollback for explicitly version-bound 6.1 work.

## Maintenance

Add entries only for material semantic replacement/generalization/rejection/restoration whose rationale is likely to matter to future scientific or engineering reasoning. Do not copy review transcripts or ordinary patch chronology. If an entry conflicts with accepted current authority, current authority governs and the historical record must be corrected as historical documentation rather than treated as a competing source of truth.
