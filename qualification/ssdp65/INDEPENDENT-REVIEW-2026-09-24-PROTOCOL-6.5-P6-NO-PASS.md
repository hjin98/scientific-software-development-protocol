---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: dd06da8136416e67644586c44880b466f982b8ff
semantic_ref: dd06da8136416e67644586c44880b466f982b8ff
p6: dd06da8136416e67644586c44880b466f982b8ff
lifecycle_evidence_head: 859275ede6fbd769e979d13893411ca64b6df165
binding_descendant: 758490c11f90b587c7dfaadddab958751f2881c9
exact_candidate_ci: 36051369390
binding_ci: 36051619464
final_evidence_ci: 36051795443
date: 2026-09-24
serious_challenge: none
d3_reopened: false
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P6

## 1. Disposition

**NO-PASS.**

Immutable Review target:

\`P6 = dd06da8136416e67644586c44880b466f982b8ff\`

Accepted Protocol 6.4 control:

\`P0 = 55c085261eb827e3047637d045a8e6917ea6b962\`

P6 is not technically eligible for stakeholder ratification. P6 remains immutable. Any semantic repair creates a new candidate identity and requires affected exact-candidate qualification plus a fresh independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized by this Review.

Two genuine D4/current-representation blockers survive:

1. **B65-P6-1 — authoritative root-state parser semantics are still bypassed by current/inherited state consumers.**
2. **B65-P6-2 — the release-state validator admits impossible future/unsuperseded historical mappings and does not maintain one canonical semantic-version identity.**

The accepted P65 D3 design is not challenged or reopened.

## 2. Independent authority reconstruction

This Review reconstructed the governing boundary from P0 and the assembled P6 source before consulting repair conclusions.

The applicable design requires:

- D1/D2/D3/D4 as the only semantic authority domains;
- one mutable release-state owner at root \`PROTOCOL-RELEASE-STATE.yaml\`;
- version-intrinsic semantics separated from mutable repository release state;
- exact Review/ratification evidence subject binding;
- Review PASS as technical eligibility only;
- explicit stakeholder ratification before public fallback;
- distinct later recovery;
- accepted-current cutover only after the complete transaction;
- historical mappings as facts of superseded releases, not a second route for manufacturing release identity;
- current doctrine represented intrinsically rather than predecessor-gated;
- generated representations subordinate to canonical source;
- preservation of accepted Protocol 6.4 capabilities and frozen historical resources;
- Protocol 7 D3/D4 isolation;
- active simplicity and removal/rewiring before additive machinery.

### Project Engineering Memory / HAS

PEM is material because this is substantial mature self-governance rework with an active workplan.

| PEM item | Disposition | Reason |
| --- | --- | --- |
| FF-001 premature immutable bootstrap publication | APPLICABLE | release-state/publication ordering and immutable fallback identity are directly under Review |
| PC-001 frozen prior-version profile/resource preservation | APPLICABLE | Protocol 6.5 adds a profile while 5.16–6.4 resources must remain frozen |
| SP-002 self-reference-safe descendant publication | APPLICABLE | P6 is intentionally immutable and later descendants own lifecycle binding |
| DS-001 semantic proxy qualification can overclaim | APPLICABLE | the Review must challenge parser/state/evidence oracles rather than inherit green CI |
| SP-001 canonical router repair + regeneration | NOT_APPLICABLE to the surviving blockers | no source-routing defect survived this Review |

These entries were used only as evidence-bounded hypotheses, not as authority or verdicts.

## 3. Serious Challenge pass

**No Serious Challenge.**

The accepted P65 parent architecture is coherent and realizable. The surviving defects are lower-layer D4/current-representation failures to realize that architecture. They do not show that D1, D2, accepted D3, formal-definition doctrine, or the P65 principles are materially false, contradictory, mutually incompatible, or unrealizable.

## 4. Exact identity, lifecycle state, and mechanical evidence

The Review target is exact P6, not the mutable branch head.

Independent inspection established:

- P6 itself still contains the prior P5 NO-PASS lifecycle snapshot. This is legitimate historical snapshot state and is not used as current lifecycle authority.
- descendant \`758490c11f90b587c7dfaadddab958751f2881c9\` binds exact P6 in the root release-state owner;
- current evidence-only descendant \`859275ede6fbd769e979d13893411ca64b6df165\` changes no P6 semantic source;
- current lifecycle state is accepted-current 6.4, candidate 6.5 at exact P6, Review \`NOT_RUN\`, ratification \`NOT_REQUESTED\`, public fallback \`UNAVAILABLE\`, recovery \`UNAVAILABLE\`;
- P6 -> current head changes only release-state/lifecycle/workplan/qualification records, not P6 semantic source.

GitHub workflow metadata independently confirms:

- run \`36051369390\`: exact head SHA P6; \`build=success\`, \`orchestrator-core=success\`;
- run \`36051619464\`: exact binding descendant; both jobs success;
- run \`36051795443\`: exact evidence descendant; both jobs success.

These runs are structural/executable evidence only. They do not establish semantic Review PASS.

## 5. Mandatory P5 repair falsification

### 5.1 B65-P5-1 — duplicate-key ambiguity

P6 alters the real root \`load()\` boundary to use the same \`_UniqueKeySafeLoader\` used for Review/ratification evidence front matter.

An independent exact-constructor harness rejected duplicate mappings for all required owner fields before semantic validation:

1. top-level \`schema_version\`;
2. top-level \`project\`;
3. top-level \`accepted_current\`;
4. top-level \`historical\`;
5. top-level \`candidate\`;
6. \`accepted_current.version\`;
7. \`accepted_current.public_source_ref\`;
8. \`accepted_current.recovery_ref\`;
9. duplicate historical version key;
10. historical \`public_source_ref\`;
11. historical \`recovery_ref\`;
12. \`candidate.version\`;
13. \`candidate.semantic_ref\`;
14. \`candidate.public_source_ref\`;
15. \`candidate.recovery_ref\`;
16. \`candidate.review.state\`;
17. \`candidate.review.evidence_ref\`;
18. \`candidate.ratification.state\`;
19. \`candidate.ratification.evidence_ref\`.

Fresh structural holdouts:

- ordinary YAML mapping aliases are accepted and preserve the aliased mapping;
- a duplicate inside an anchored mapping is rejected recursively;
- YAML merge-key forms are rejected fail-closed by the strict loader;
- root state and evidence front matter therefore use the same strict loader semantics inside \`source/release_state.py\`.

However, the repair is **not globally closed** because numerous current/inherited tests still read the authoritative root file through ordinary \`yaml.safe_load\`. See B65-P6-1.

### 5.2 B65-P5-2 — active candidate succession

The P6 successor relation is numeric rather than lexical. Independent matrix results:

- candidate equal to accepted-current before terminal closure: reject;
- lower non-historical candidate \`6.3.1\` under accepted \`6.4.0\`: reject;
- candidates \`5.16.0\`, \`6.0.0\`, \`6.1.0\`, \`6.2.0\`, \`6.3.0\`: historical collision rejects independently; lower/equal ordering also rejects where applicable;
- real immutable Protocol 6.3 recovery \`9f353097fab36e325a325f1c2f9d9cec32e86177\` declares \`source/PROTOCOL_VERSION = 6.3.0\` and remains invalid as active successor under accepted 6.4;
- \`6.4.1\`, \`6.5.0\`, \`7.0.0\`: accept as generic patch/minor/major successors;
- \`6.10.0\`: accepts correctly as numerically newer than \`6.4.0\`;
- ordinary malformed forms such as \`6.5\`, \`v6.5.0\`, and \`6.5.0-alpha\` reject under the schema's three-component grammar;
- valid terminal \`accepted_current == candidate\` remains legal only through the complete terminal predicate;
- incomplete terminal equality rejects;
- after terminal 6.5 cutover, \`6.5.1\`, \`6.6.0\`, and \`7.0.0\` are generic valid successors.

No P1-P6 candidate-specific branch exists in the ordering implementation.

A fresh sibling defect survives outside the author's matrix: historical-state admission is underconstrained. See B65-P6-2.

## 6. Re-falsification of earlier blocker families

### 6.1 B65-P4-1 / B65-P3-1 — evidence front matter and exact subject identity

These families are closed in the inspected P6 binder implementation:

- duplicate evidence keys reject before subject/disposition binding;
- explicit \`candidate_ref\` / \`semantic_ref\` key presence is authoritative;
- empty/null/malformed explicit subjects reject and cannot borrow a lower legacy \`pN\`;
- conflicting explicit subject fields reject;
- legacy \`pN\` fallback is used only if explicit fields are absent;
- highest numeric generation is authoritative;
- invalid highest generation cannot fall back lower;
- \`p4 + p5 + p6\` selects p6; future numeric generations remain generic;
- Review and terminal ratification share \`_bound_candidate_ref\`, so there is one structural subject owner.

A structurally correct record with semantically unrelated prose can still pass the machine binder. That is intentional: the binder discriminates route/subject/disposition, not arbitrary semantic adequacy. Independent semantic Review remains the owner of prose meaning.

### 6.2 B65-P3-2 / B65-R3 — current representation convergence

Independent census of all 34 current canonical \`source/shared/references/*.md\` files found no literal \`Protocol 6.4\`, \`6.4.0\`, or \`predecessor\` scope gate and no sampled semantic equivalent such as “previous/prior/older protocol/version” conditioning current obligations.

Full inspection of the canonical workflow prompt shows D1/D2/D3/D4, Review, Verification, Stabilization, audit, evidence, formal-definition, and closeout duties expressed intrinsically under the declared governing version.

Two current-source 6.4 references outside that scope, in \`source/SEMANTIC_DEPENDENCIES.md\`, are legitimate frozen-history/profile-preservation statements rather than current semantic gates.

Canonical \`development-workflow-prompts.md\` and the packaged Protocol 6.5 generated prompt are the same Git blob. No generated representation becomes an independent owner.

### 6.3 B65-P2-1 / B65-R2 — lifecycle-value and phase duplication

The inherited tests no longer require manual edits merely because accepted-current advances from 6.4 to 6.5 and a 6.6 successor begins. Existing fixtures preserve immutable historical identities and exercise current-vs-historical lookup or copied synthetic transition state.

The surviving problem is not a copied lifecycle value. It is parser-semantic divergence: those tests often obtain the root owner through ordinary \`yaml.safe_load\` rather than the owner parser. That is B65-P6-1.

### 6.4 B65-P2-2 / B65-R1 — Review and ratification applicability

Review and ratification evidence routes resolve an immutable project commit/path, bind one exact candidate subject, and require matching disposition. The shared subject helper is generation-generic and contains no P1-P6 table or semantic prose parser.

A forged “ratified” file with structurally correct metadata could remain mechanically green if it were not actually authorized by a stakeholder. The current authority explicitly limits the machine oracle: actual stakeholder authorization is a human/semantic ownership decision and cannot be inferred by CI, merge, branch position, or metadata. This is therefore an oracle limitation to preserve, not a reason to add an authorship/semantic parser.

## 7. Full assembled-candidate defect-family result

| Defect family | Result | Review result |
| --- | --- | --- |
| DF-1 release-state/version lifecycle ownership | **NO-PASS** | B65-P6-2 admits unsuperseded/future “historical” releases; B65-P6-1 leaves multiple parser semantics over the sole state owner |
| DF-2 qualification/Review epistemology | PASS with bounded claims | exact subject/disposition binding is sound; prose meaning remains independent Review work; green CI does not override blockers |
| DF-3 meta-control semantics/governance | PASS | Serious Challenge, Review/ratification separation, PEM boundaries, D1-D4 ownership and human ratification ownership remain coherent |
| DF-4 representation/schema/convergence self-application | **NO-PASS** | root state has one data owner but not one mechanical parser semantics across current consumers |

## 8. Local-compliance / global-failure trajectories

### Trajectory A — parser-normalized state

1. Insert a duplicate mapping into root release state.
2. \`release_state.load()\` correctly rejects it.
3. A current/inherited test reading the same file through \`yaml.safe_load\` normalizes it last-key-wins.
4. The test then makes an ownership, compatibility, historical-resolution, or current-state claim over a representation the actual owner parser declares invalid.

Every local test assertion can still be internally coherent while parser semantics differ across the same authoritative state object. The workflow's earlier root validation reduces the chance of an integrated false green, but it does not make the individual oracles congruent with the owner they claim to inspect.

### Trajectory B — future release laundered into history

Construct a state from the currently valid P6 lifecycle state:

- keep \`accepted_current.version = 6.4.0\`;
- add \`historical["6.5.0"]\`;
- use P6 \`dd06...\` as historical public source;
- use binding descendant \`758490...\` as historical recovery;
- set active candidate to generic \`6.6.0 / UNFROZEN / NOT_RUN / NOT_REQUESTED / UNAVAILABLE\`.

Both chosen historical refs are distinct real immutable commits and both declare \`source/PROTOCOL_VERSION = 6.5.0\`. P6's validator checks those facts but never requires a historical version to precede accepted-current. It therefore has no structural reason to reject the state.

The result represents Protocol 6.5 as a historical public/recovery release even though accepted-current is still 6.4 and 6.5 has never completed Review, stakeholder ratification, public fallback publication, recovery establishment, or accepted-current cutover.

This violates lifecycle ownership, stakeholder-ratification ownership, historical identity, evidence-claim congruence, and state/semantics separation.

### Other constructed trajectories

- wrong explicit Review subject + matching lower \`pN\`: rejected;
- valid metadata + semantically unrelated Review prose: machine binder accepts, independent semantic Review rejects any overclaim;
- source/generated workflow divergence: exact blob parity detects current prompt divergence;
- predecessor-scoped current doctrine: independent source inspection rejects;
- stale mutable phase copies: current tests use transition-aware/historical lookup rather than fixed live phase values;
- generated profile mutation of 5.16–6.4: frozen blob comparison detects.

## 9. Out-of-matrix abstraction-adequacy pass

A fresh material sibling defect **did survive**: B65-P6-2 was not one of B65-R1..R3, B65-P2-1..2, B65-P3-1..2, B65-P4-1, or B65-P5-1..2.

The defect arises because “historical” is treated as a syntactic mapping label rather than a lifecycle relation to accepted-current. A local mapping can satisfy all per-ref checks while violating the global temporal meaning of historical/superseded release identity.

The version grammar also accepts non-canonical textual numeric identities such as leading-zero components and Unicode decimal digits because \`SEMVER_RE\` uses \`\d+\`. Numeric comparison maps these to integer tuples while collision checks use raw strings. This is not raised as a separate blocker; it is part of B65-P6-2's requirement that one canonical version identity underlie ordering/disjointness.

## 10. Challenge to the qualification method

| Claim | Can the oracle stay green while the claimed property is broken? | Review |
| --- | --- | --- |
| exact P6 builds/packages/Core | yes, semantic lifecycle defects can survive | CI is applicable only to its structural/executable scope |
| root duplicate rejection | owner path: no; current consumer paths: yes | **overstrong closure claim -> B65-P6-1** |
| recursive duplicate rejection | no for mappings parsed by strict loader | supported |
| YAML alias/merge semantics | aliases supported; merge keys fail closed in strict loader, while ordinary safe loaders accept them | parser split reinforces B65-P6-1 |
| numeric successor ordering | ordinary patch/minor/major/multi-digit traps are discriminated | supported |
| candidate/history disjointness | raw-key collision is checked, but history itself can contain a future release; non-canonical numeric spellings also exist | **overstrong -> B65-P6-2** |
| terminal equality | incomplete equality rejects; complete equality remains legal | supported |
| exact Review/ratification subject | structurally strong | supported |
| substantive Review prose adequacy | machine oracle can stay green | correctly left to independent semantic Review |
| stakeholder authorization | machine oracle can stay green on metadata alone | correctly remains human/semantic authority; no machine overclaim permitted |
| source/generated prompt parity | exact blob identity discriminates this representation | supported |
| frozen 5.16–6.4 preservation | exact blob comparison is strong for those 12 objects | supported |
| simplification/compression | word/copy counts can stay good while lifecycle is wrong | counts are descriptive only, never acceptance |
| predecessor-scope census | literal census can miss paraphrase | independent semantic workflow inspection also performed |
| future-candidate generality | known successor matrix is generic | supported except historical/canonical-version sibling defect |

## 11. Fresh post-P6 mutation / counterexample set

### Machine/state/schema/generated mutants

| Mutant | Outcome |
| --- | --- |
| duplicate each root owner field listed in §5.1 | rejected by strict owner loader |
| nested duplicate inside YAML anchor | rejected recursively |
| ordinary alias to valid mapping | accepted |
| YAML merge-key mapping | strict owner rejects fail-closed; ordinary \`yaml.safe_load\` consumers use different semantics |
| duplicate Review/ratification status/subject | rejected |
| explicit candidate-field disagreement | rejected |
| null/empty/malformed explicit subject + lower \`pN\` | rejected; no fallback |
| lower+higher \`pN\` | highest numeric generation owns subject |
| invalid highest \`pN\` | rejected; no lower fallback |
| p10 future generation | generic numeric-generation rule applies |
| candidate \`6.10.0\` under accepted 6.4 | accepted numerically, not lexically |
| candidate equal/lower/historical | rejected |
| valid terminal equality | accepted |
| incomplete terminal equality | rejected |
| post-cutover patch/minor/major successor | accepted |
| **historical 6.5 injected while accepted-current remains 6.4 using real 6.5 refs** | **survives -> B65-P6-2** |
| root duplicate observed through inherited \`yaml.safe_load\` consumer | **normalizes rather than rejects -> B65-P6-1** |
| source/generated workflow prompt divergence | current exact parity oracle discriminates |
| mutation of frozen 5.16–6.4 profile/prompt object | exact blob comparison discriminates |

Fresh holdouts not used to design P6 include anchored nested duplicate, merge-key YAML, \`6.10.0\`, canonical-version spelling probes, and the real-ref future-history trajectory.

### Prose semantic mutants

Independent semantic Review rejects:

- predecessor-scoped inherited obligations expressed by paraphrase;
- an agent/CI/merge treating itself as stakeholder ratification;
- structurally valid Review metadata attached to prose that does not actually review P6;
- compression that removes a P64/QF64/F64 capability while preserving legacy vocabulary;
- generated/profile prose that changes owner meaning while structural schema remains valid.

Meaning-preserving paraphrases that preserve the same owner, lifecycle order, evidence scope, and authority relation remain acceptable.

## 12. P65-1 through P65-6 causal ablation

| Principle | Causal ablation | P6 realization |
| --- | --- | --- |
| P65-1 self-application | exempt SSDP release engineering and parser consumers -> locally green self-tests can inspect a weaker state representation | **incomplete due B65-P6-1** |
| P65-2 state/semantics separation | allow mutable lifecycle truth in version source or secondary copies -> drift after cutover | materially realized; **historical lifecycle relation incomplete due B65-P6-2** |
| P65-3 evidence-claim congruence | allow green structural evidence to claim semantic correctness -> exact current blockers would be hidden | principle realized in prose, but P6 repair qualification overstates root-parser closure |
| P65-4 Review abstraction adequacy | constrain Review to author matrix -> future-history defect survives | causally necessary and realized by this fresh Review |
| P65-5 minimal meta-governance | remove Review/ratification/Challenge/PEM distinctions -> inferred acceptance and self-review become admissible | realized |
| P65-6 integrated current representation | keep predecessor-labelled operational doctrine/generated copies -> current successor semantics diverge | realized on inspected doctrine/generated surfaces |

The failures do not justify adding P65-7 or redesigning P65-1..P65-6.

## 13. Protocol 6.4 -> 6.5 preservation-map falsification

Independent inspection supports preservation of:

- D1-D4 authority ownership;
- accepted P64 formal-definition/axiomatic doctrine;
- semantic capabilities represented by QF64 even where obsolete proxy machinery was removed;
- F64-style falsification obligations through current Review/evidence doctrine;
- evidence/evolution semantics;
- PEM non-authority and accepted-base/overlay discipline;
- compatibility/public fallback/recovery distinction;
- Protocol 7 D3/D4 isolation;
- frozen historical profile resources.

Exact P0/P6 Git blob comparison found **0 differences across all 12 frozen profile/prompt objects** for Protocol 5.16 and 6.0–6.4.

Only the Protocol-7 authority index changed among paths named for Protocol 7; the change records the 6.5 branch/routing state and explicitly leaves Protocol 7 architecture untouched. Protocol-7 D3/D4 source workplans remain blob-identical to P0.

The preservation map is overstrong where it implies that the 6.5 release-state concretization fully preserves lifecycle/historical identity. B65-P6-1 and B65-P6-2 prevent that conclusion.

## 14. Simplicity and total complexity

P6's direct repair is architecturally economical:

- no second release-state registry;
- no state mirror;
- no candidate-specific table;
- no semantic prose parser;
- no synchronized phase table;
- no new dependency;
- no generated-source shadow owner.

The surviving repairs should preserve that shape.

Do **not** add wrappers or another parser. Reuse the existing strict \`release_state.load\` boundary for every current root-state consumer.

Do **not** add a historical registry. Strengthen the existing state relation and canonical version grammar inside the existing validator.

## 15. P0/P6 matched comparison

Measurements applicable to exact P6:

| Measure | P0 | P6 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public fallback SHA copies in that projection | 20 | 0 |
| accepted-6.4 recovery SHA copies in that projection | 12 | 0 |
| frozen 5.16 and 6.0–6.4 profile/prompt objects changed | — | 0 / 12 |
| current canonical shared-reference predecessor census | — | 34 files; 0 scoped matches |

Applicability basis:

- P5 -> P6 changed the release-state implementation/tests and lifecycle records, not the universal kernel or defined hot-current projection; those word/copy measurements therefore carry by unchanged blob identity.
- frozen-resource parity was independently rechecked P0 -> P6.
- predecessor-scope census was independently rerun at P6.
- exact P6 CI independently confirms package/profile/Core mechanical acceptance.

Matched difficult areas:

- **lifecycle/current-state drift:** materially improved from P0, but still NO-PASS because parser consumers and historical admission violate the one-owner lifecycle model;
- **proxy/oracle adequacy:** materially improved exact evidence subject binding and current semantic Review separation; B65-P6-1 shows one remaining owner/oracle mismatch;
- **authority/Serious-Challenge routing:** coherent and non-inferior; no Serious Challenge;
- **mature-system simplification/Review convergence:** hot duplication is lower and no new control plane was added, but repeated independent Review continues to expose lifecycle concretization gaps, so convergence is not yet complete.

No quantitative frontier-model superiority claim is made. The second contemporary frontier diagnostic remains waived for this cycle.

## 16. Blocking findings and smallest owning-layer repairs

### B65-P6-1 — root-state consumers bypass strict owner parser

**finding ->** The authoritative root state's strict parser is not the sole mechanical read semantics. A bounded P6 census found **16 ordinary \`yaml.safe_load\` reads of \`PROTOCOL-RELEASE-STATE.yaml\` across 11 current/inherited test files**, including current-state ownership, historical resolution, portability, contracts, closeout, bootstrap, and evidence-evolution tests.

**exact owner ->** D4 release-state parsing/qualification consumers. \`source/release_state.py\` already owns the correct parser; affected test consumers must route through it.

**violated invariant ->** Lossless Representation; one authoritative representation; state/semantics separation; evidence-claim congruence; self-application; B65-P5-1's explicit “no ordinary safe_load pre-normalization of authoritative root state” closure criterion.

**counterexample/evidence ->** A duplicate-key or merge-key root file is interpreted differently by \`release_state.load\` and ordinary \`yaml.safe_load\`. Tests can therefore make claims over a state representation the real owner rejects.

**consequence ->** B65-P5-1 is only locally repaired at the CLI/owner path, not across qualification consumers. Parser-path-dependent observations remain possible and qualification claims are stronger than the individual oracles.

**smallest owning-layer repair ->**
- in every test/current mechanical consumer that reads root \`PROTOCOL-RELEASE-STATE.yaml\`, import/use the existing \`source/release_state.py\` \`load()\` path;
- leave unrelated YAML fixture parsing alone;
- remove now-unused direct YAML imports where appropriate;
- do not add a wrapper, second loader, compatibility parser, state mirror, or registry.

**affected qualification to rerun ->**
- complete root duplicate matrix over every top-level/nested owner field;
- fresh alias/anchor/merge holdout;
- all 11 affected state-consuming test files;
- \`tests/test_protocol_65_release_state.py\`;
- full repository build and Orchestrator Core;
- current-state ownership/census and preservation applicability;
- replacement freeze/binding and fresh independent Review.

### B65-P6-2 — historical release relation and version identity are underconstrained

**finding ->** The validator checks that historical keys look like three numeric components and that mapped refs declare the same version, but it does not require a historical version to be older than accepted-current. It also uses a non-canonical \`\d+\.\d+\.\d+\` grammar while ordering is numeric and collision checks are textual.

**exact owner ->** D4 \`source/release_state.py\` release-state schema/validator.

**violated invariant ->** release-state ownership; stakeholder-ratification ownership; historical identity; compatibility/recovery integrity; evidence-claim congruence; generic future lifecycle correctness; preservation of accepted P64 version/evolution semantics.

**counterexample/evidence ->** With accepted-current still 6.4, add \`historical["6.5.0"]\` mapped to real distinct immutable commits P6 and its binding descendant, both of which declare \`6.5.0\`; start candidate 6.6 UNFROZEN. Per-ref, schema, and candidate-order checks are locally satisfied, but 6.5 never passed Review/ratification/publication/recovery/cutover. The state nevertheless represents it as historical release identity. Leading-zero/Unicode numeric spellings further show that tuple identity and textual collision identity are not one canonical relation.

**consequence ->** An unsuperseded release can enter the historical public/recovery namespace without traversing the accepted lifecycle. This is a global lifecycle failure despite locally valid refs.

**smallest owning-layer repair ->**
- define one canonical three-component ASCII numeric version grammar in the existing release-state validator, with one textual representation per numeric identity;
- use that same canonical identity for accepted, historical, and candidate ordering/disjointness;
- require every historical version to be strictly older than \`accepted_current.version\`;
- retain terminal \`accepted_current == candidate\` only through the existing complete terminal predicate;
- do not add a version registry, candidate table, history mirror, or new service.

This repair intentionally enforces only the mechanically decidable lifecycle relation. It does not make the state parser a theorem prover for whether arbitrary historical prose is true.

**affected qualification to rerun ->**
- existing B65-P5-2 matrix;
- real-ref future-history negative described above;
- historical equal/greater-than-accepted negatives;
- canonical-version spelling negatives;
- \`6.10.0\` numeric-order positive;
- patch/minor/major pre-cutover and post-cutover successors;
- valid and invalid terminal equality;
- historical exact-ref preservation tests;
- full build/Core and fresh independent Review.

## 17. Evidence applicability after NO-PASS

Still applicable to exact P6 as historical evidence:

- run \`36051369390\` for exact P6 mechanical properties actually exercised;
- runs \`36051619464\` and \`36051795443\` for exact descendant lifecycle/mechanical observations;
- exact subject/disposition binder evidence where unchanged;
- P0/P6 frozen-resource parity;
- canonical/generated 6.5 workflow prompt parity;
- current predecessor-scope census;
- unchanged D1/D2/formal-definition/PEM/Protocol-7 surfaces.

Stale for any replacement candidate:

- whole-candidate P6 semantic Review conclusion;
- P6 exact-candidate CI as candidate-level acceptance evidence;
- P6 freeze/binding qualification as replacement identity evidence;
- B65-P5-1 “closed everywhere” claim until all root-state consumers route through the strict owner parser;
- release-state/lifecycle qualification affected by historical-order/canonical-version repair;
- mutation/ablation conclusions that depend on the repaired state validator.

Unchanged-surface evidence may be reused only after target/oracle/regime/implementation-dependency applicability is re-established.

## 18. Required next state

- Preserve P6 immutably.
- Record this Review as P6 \`NO_PASS\` from a later descendant.
- Reopen the existing 6.5 D4 workplan only for B65-P6-1 and B65-P6-2.
- Accepted P65 D3 remains closed.
- Implement repair by alteration/rewiring inside the existing parser/state owner and consumers.
- Freeze a **new** immutable semantic candidate.
- Rerun affected qualification and exact-candidate normal CI.
- Bind the replacement candidate from a later descendant with Review reset to \`NOT_RUN\`.
- Perform another genuinely fresh independent assembled-candidate Review.

No stakeholder ratification or publication action is authorized.
