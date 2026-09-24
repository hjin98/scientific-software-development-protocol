---
kind: independent-assembled-candidate-review
protocol_under_review: 6.5.0
status: no-pass
candidate_ref: d2d672a3e814438fb618f901137f88c8698a205d
p5: d2d672a3e814438fb618f901137f88c8698a205d
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
lifecycle_evidence_head: f24f619c9976f79039221f1ed7eff3d850f7d92f
reviewer: GPT-5.6 Sol
date: 2026-09-24
serious_challenge: none
blockers:
  - B65-P5-1
  - B65-P5-2
stakeholder_ratification: NOT_REQUESTED
---

# Fresh Independent Assembled-Candidate Review - Protocol 6.5 P5

## 1. Disposition

**NO-PASS.**

Immutable semantic Review target:

`P5 = d2d672a3e814438fb618f901137f88c8698a205d`

Accepted Protocol 6.4 control:

`P0 = 55c085261eb827e3047637d045a8e6917ea6b962`

P5 is not technically eligible for stakeholder ratification.

The P4 blocker B65-P4-1 is independently closed on its actual evidence-front-matter surface. Two fresh D4 blockers survive outside that repair matrix:

1. **B65-P5-1 — the sole mutable release-state YAML owner still accepts duplicate mapping keys before validation.**
2. **B65-P5-2 — the release-state validator does not require the active candidate version to be a successor of accepted-current and can admit an immutable historical protocol identity as the active candidate.**

Neither finding challenges accepted D3. Both are defects in the existing `source/release_state.py` concretization and its focused tests. Repair must preserve P5 immutably and produce a new semantic candidate identity.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.

## 2. Serious Challenge pass

**No Serious Challenge.**

The reconstructed accepted D3 model is coherent and realizable:

- version-intrinsic semantics are distinct from mutable repository release state;
- root `PROTOCOL-RELEASE-STATE.yaml` is the sole mutable owner of accepted-current, active successor candidate identity, Review/ratification state, public fallback, and recovery;
- immutable historical mappings remain frozen facts;
- independent Review, stakeholder ratification, publication, recovery, and accepted-current cutover are distinct lifecycle events;
- one authoritative representation and Lossless Representation remain required.

The two surviving defects are lower-layer validator/parser failures against that coherent architecture. They are ordinary blockers, not reasons to challenge D3.

## 3. Independently reconstructed authority and lifecycle state

Authority was reconstructed from P5 canonical source and accepted P0 before using repair/qualification conclusions.

The applicable current rules require:

- D1/D2/D3/D4 ownership separation;
- one semantic owner for each current material claim;
- Lossless Representation and progressive disclosure;
- version-intrinsic semantics distinct from mutable lifecycle state;
- exact-candidate evidence applicability;
- Review PASS as technical eligibility only;
- explicit stakeholder ratification for the exact reviewed candidate before publication;
- public fallback distinct from later recovery;
- current generated representations subordinate to canonical source;
- PEM as non-authoritative project learning;
- frozen historical version/profile/recovery identities preserved;
- candidate succession and lifecycle state owned by the one root state artifact.

Later lifecycle descendants were inspected only for mutable state. At both P5 binding descendant `7db6b19a8f5039a4e328f4a99ea66e939efba67e` and final evidence-only descendant `f24f619c9976f79039221f1ed7eff3d850f7d92f`:

- accepted-current = `6.4.0`;
- accepted 6.4 public fallback = `e09a9d1480211eea2d16d722182bb5c6de1bee12`;
- accepted 6.4 recovery = `74bc572ef516cae417437a2027eeff52a2e25c15`;
- candidate = `6.5.0`;
- candidate semantic ref = exact P5;
- Review = `NOT_RUN`;
- ratification = `NOT_REQUESTED`;
- public fallback = `UNAVAILABLE`;
- recovery = `UNAVAILABLE`.

P5 itself still records the prior P4 NO-PASS state, as expected for a commit that cannot self-name as the replacement candidate. P5->final-head contains only later lifecycle/evidence/workplan changes; no later semantic commit was substituted for P5.

Exact CI applicability was also checked:

- run `36047926253` has head SHA exact P5 and completed successfully;
- run `36048168248` has head SHA exact P5 binding descendant and completed successfully;
- run `36048331437` has head SHA exact final evidence descendant and completed successfully.

Each run passed both repository build and Orchestrator Core jobs, including release-state validation, PEM validation, full protocol regression, package build/validation/parity, packaged Protocol 6.5 snapshot parity, and Core acceptance. These observations establish only the properties those oracles discriminate.

## 4. Mandatory P5 repair falsification

### 4.1 B65-P4-1 - structural evidence-front-matter ambiguity

The P5 repair is correct on the shared Review/terminal-ratification evidence parser/binder.

The actual P5 owner:

- uses a SafeLoader subclass that rejects duplicate mapping keys before semantic binding;
- detects `candidate_ref` / `semantic_ref` by key presence rather than truthiness;
- requires every present explicit subject to be a nonempty lowercase 40-hex identity;
- requires explicit fields to agree when both are present;
- refuses legacy `pN` fallback whenever an explicit subject key is present;
- otherwise chooses the highest numeric legacy `pN` generation;
- rejects an invalid/empty highest generation instead of borrowing a lower generation;
- treats future numeric generations generically;
- shares the same subject binder between Review and terminal ratification;
- reads only structural front matter for machine disposition/subject judgment and does not parse arbitrary prose semantically.

Fresh structural probes and direct source-path inspection produced the following disposition:

| Case | Review / ratification result |
| --- | --- |
| exact candidate + PASS | accepts |
| exact candidate + NO_PASS | accepts |
| exact candidate + RATIFIED | accepts |
| exact candidate + REJECTED | accepts |
| wrong candidate SHA | rejects exact-subject binding |
| disposition mismatch | rejects |
| wrong repository | rejects |
| absolute path | rejects |
| parent traversal | rejects |
| nonexistent commit | rejects |
| nonexistent path | rejects |
| malformed front matter | rejects |
| missing front matter | rejects |
| wrong explicit `candidate_ref` + matching lower legacy `pN` | rejects; explicit wins |
| wrong explicit `semantic_ref` + matching lower legacy `pN` | rejects; explicit wins |
| conflicting explicit fields | rejects |
| duplicate `candidate_ref` | rejects before semantic binding |
| duplicate `semantic_ref` | rejects before semantic binding |
| duplicate `status` | rejects before disposition binding |
| empty explicit `candidate_ref` + matching legacy | rejects |
| null explicit `semantic_ref` + matching legacy | rejects |
| malformed explicit subject + matching legacy | rejects |
| lower+higher legacy generations | highest generation is the sole subject |
| valid lower generation + invalid/empty highest generation | rejects; no fallback lower |
| future `p6`, `p7`, later numeric generation | remains generic |
| structurally valid metadata + false/unrelated Review prose | machine structural check accepts; semantic Review owns prose |
| structurally valid metadata + false/unrelated ratification prose | machine structural check accepts; stakeholder authorization remains outside prose parsing |

Additional alias/duplicate holdouts did not disclose a bypass: the strict evidence loader rejects ambiguous duplicate mappings rather than normalizing them, and no candidate-specific P1-P5 table exists.

**B65-P4-1: CLOSED.**

### 4.2 B65-P3-1 - exact evidence-subject identity

Still closed.

Explicit fields dominate historical context; conflicting explicit fields reject; `p4`+`p5` without explicit subject resolves only to the highest generation; future generations remain generic; Review and terminal ratification share the same structural subject owner.

### 4.3 B65-P3-2 - current representation convergence

Still closed on the reviewed source surface.

A fresh census of all 34 current canonical `source/shared/references/*.md` files found zero literal matches for `Protocol 6.4`, `6.4.0`, or `predecessor`. The two current-source mentions found outside that shared-reference scope are legitimate frozen-history statements in `source/SEMANTIC_DEPENDENCIES.md`: the 6.5 profile preserves frozen 6.4 profile/schema capability, and older resources are described as frozen historical/version-bound resources.

Semantic inspection, not just grep, found Review, Verification, Stabilization, audit, evidence, formal-definition, exact-contract, and closeout obligations expressed intrinsically in current workflow/evidence/testing owners rather than conditioned on Protocol 6.4 identity.

Generated Protocol 6.5 prompts reproduce canonical current prompt semantics; no generated representation became a second owner. Frozen Protocol 7 authority was not mutated by P0->P5.

### 4.4 B65-P2-1 / B65-R2 - lifecycle-value and phase duplication

The prior duplication family remains closed on the known surfaces.

Long-lived 6.4 bootstrap tests resolve 6.4 identity from accepted-current while it is current and from `historical["6.4.0"]` after a successor cutover. The legal cutover fixture moves 6.4 to historical without changing its immutable bootstrap/recovery identity. The release-state tests also admit a legal terminal 6.5 state and then a new `6.6.0 / UNFROZEN / NOT_RUN / NOT_REQUESTED / UNAVAILABLE` successor candidate without phase-specific test edits.

The current hot projection contains no accepted-6.4 public/recovery SHA copies outside the root owner. The surviving P5 blockers are not copied lifecycle values; they are invalid states/representations that the owner itself admits.

### 4.5 B65-P2-2 / B65-R1 - Review and terminal-ratification applicability

Still closed on the evidence-route/binder surface. Wrong subject, wrong disposition, wrong repository, unsafe route, missing commit/path, explicit/legacy conflict, and future-generation cases are discriminated structurally for both Review and terminal ratification.

No prose theorem prover, semantic registry, or second evidence authority was introduced.

### 4.6 B65-R3 - predecessor-version gating

Still closed. Current operational obligations apply intrinsically under 6.5 and do not require a predecessor-version predicate.

## 5. Blocking findings

### B65-P5-1 - sole mutable release-state YAML is structurally ambiguity-tolerant

**finding ->** The evidence-front-matter parser is strict, but the authoritative root release-state file is still loaded by `yaml.safe_load`. PyYAML accepts duplicate mapping keys with last-key-wins normalization. Therefore duplicate `accepted_current`, `candidate`, `semantic_ref`, Review/ratification `state`, or evidence fields can be erased before `validate_release_state()` sees them.

**exact owner ->** D4 concretization in `source/release_state.py`, specifically root release-state loading. Root `PROTOCOL-RELEASE-STATE.yaml` remains the D3-selected sole mutable state owner.

**violated invariant ->** Lossless Representation; one authoritative representation/state; P65-1 self-application; P65-2 state/semantics separation; P65-4 abstraction-adequate Review; exact candidate/lifecycle ownership.

**counterexample/evidence ->** A root YAML document containing two `candidate.semantic_ref` keys or two Review `state` keys is normalized by the current `load()` path before validation. The same strict duplicate-key loader already exists for evidence front matter, proving this does not require new machinery. `tests/test_protocol_65_release_state.py` and `tests/test_protocol_65_current_state_ownership.py` also load the root file with ordinary `yaml.safe_load`, so their fixtures share the blind spot. A locally compliant parsed dict can therefore pass while the authoritative source representation is ambiguous.

**consequence ->** CI can report “release state is coherent” for a structurally ambiguous sole owner. Exact candidate/Review/ratification facts can depend on parser overwrite behavior rather than one unambiguous source representation. That is a release-state ownership defect and blocks P5.

**smallest owning-layer repair ->** Reuse/consolidate the existing strict duplicate-key YAML loader for the root `load()` path and test fixtures. Reject duplicate mappings anywhere in the authoritative state document before semantic validation. Do not add a second parser service, schema registry, state mirror, wrapper, or compatibility layer.

**affected qualification to rerun ->** Root release-state structural negative fixtures; Review/ratification focused tests to ensure shared-loader behavior remains correct; lifecycle transition tests; complete repository regression; exact replacement-candidate CI; binding qualification; fresh independent assembled-candidate Review. P5 CI remains valid historical evidence only for the exact parser behavior it exercised.

### B65-P5-2 - active candidate can be a historical/non-successor protocol version

**finding ->** `validate_release_state()` validates semantic-version syntax and exact ref/version agreement but does not require the active candidate version to be a semantic successor of accepted-current, nor does it reject collision with an existing historical version. Its only candidate-vs-accepted comparison handles equality as a terminal cutover case.

**exact owner ->** D4 lifecycle/state validation in `source/release_state.py`.

**violated invariant ->** The versioning owner declares the field to be the **active successor semantic-candidate identity**; historical mappings are immutable superseded facts; P65-2 requires a coherent one-owner lifecycle transaction; compatibility requires historical versions to remain historical rather than silently re-enter the active candidate slot.

**counterexample/evidence ->** Accepted-current is 6.4.0 and historical state contains 6.3.0. Immutable commit `9f353097fab36e325a325f1c2f9d9cec32e86177` declares `source/PROTOCOL_VERSION = 6.3.0`. A state using `candidate.version = 6.3.0`, that real 6.3 commit as `candidate.semantic_ref`, `review = NOT_RUN`, `ratification = NOT_REQUESTED`, and unavailable publication/recovery satisfies every current validator branch: semver is valid, the ref resolves to the named version, the candidate is not equal to accepted-current, and no later lifecycle gate fires. The same version can therefore be both immutable historical state and the “active successor” candidate.

**consequence ->** A locally valid state can reverse the lifecycle direction, alias historical authority into current candidate state, and make subsequent Review/ratification evidence appear applicable to a non-successor. Candidate succession and historical immutability are not mechanically protected by the sole state owner.

**smallest owning-layer repair ->** In the existing validator, define the minimum semantic-version comparison needed by the state machine and require any pre-cutover active candidate version to be strictly greater than accepted-current and not collide with historical version keys. Preserve the existing explicitly terminal accepted-current == candidate case. Add negative fixtures for historical collision and lower/equal/non-successor candidates plus positive fixtures for patch/minor/major successors and the current terminal transition. Do not introduce a version registry or synchronized phase table.

**affected qualification to rerun ->** Lifecycle transition/current-owner tests; historical mapping preservation tests; exact-ref candidate/version checks; complete regression; exact replacement-candidate CI; changed-surface preservation/applicability review; new freeze/binding qualification; fresh independent assembled-candidate Review.

## 6. Full defect-family reassessment

### DF-1 - release-state/version lifecycle ownership

**Not closed.** P5 has one designated mutable owner and eliminates the known copied values, but B65-P5-1 means its serialized state can be ambiguous before validation, and B65-P5-2 means the state machine admits a non-successor/historical candidate trajectory.

### DF-2 - qualification/Review epistemology

**Substantially improved but not sufficient for PASS.** The exact Review/ratification evidence binder is strong and arbitrary prose is correctly outside machine semantic judgment. However the normal green CI does not discriminate the two new release-state defects. Claims must remain narrower than “state model fully coherent.”

### DF-3 - meta-control semantics/governance

**Closed on the reviewed semantic-owner surface.** Materiality, Serious Challenge, Review independence, stakeholder ratification, and authority boundaries are coherent and centrally owned. No new meta-control defect was found.

### DF-4 - representation/schema/convergence self-application

**Not closed.** Current doctrine convergence and generated/source parity are good, but the project’s own sole machine-readable lifecycle owner is not held to the strict structural representation standard already applied to Review evidence. This is a self-application failure.

## 7. Local-compliance/global-failure trajectories

1. **Lifecycle:** all parsed fields have legal syntax and refs, yet candidate 6.3.0 is historical while simultaneously occupying the active successor slot.
2. **Evidence applicability:** Review metadata binds one exact candidate correctly, yet a duplicate key in the outer lifecycle state can alter which semantic ref or Review state is presented to the evidence checker before it runs.
3. **Authority separation:** D3 correctly declares one release-state owner, yet D4 parser normalization can make that owner contain two human-visible claims and one parser-selected claim.
4. **Review/ratification/publication ordering:** the existing gates prevent publication before PASS+RATIFIED, but they do not prevent those gates being applied to a historical/non-successor candidate identity.
5. **Generated representation:** source/generated parity remains green even if canonical source is semantically wrong; therefore parity is necessary transport evidence, not semantic acceptance.
6. **PEM:** no PEM record is permitted to cure either state defect; doing so would create a non-authoritative workaround.
7. **Compatibility:** frozen historical profiles/resources remain unchanged, but reactivating a historical version in the candidate slot violates compatibility/lifecycle identity even without mutating its bytes.
8. **Candidate succession:** the positive 6.5->6.6 fixture shows one legal successor path but does not discriminate an older/historical candidate.

## 8. Out-of-matrix abstraction-adequacy pass

The author’s P5 matrix focused correctly on evidence front-matter ambiguity. Temporarily ignoring that matrix exposed two sibling classes at the actual sole lifecycle owner:

- structural duplicate-key ambiguity in root state parsing;
- missing successor-direction/version-disjointness in the state machine.

Both allow all obvious local field rules to pass while a protected global invariant fails. This satisfies the required holdout requirement and demonstrates why P65-4 remains causally necessary.

No additional material blocker was found in PEM boundaries, generated ownership, current doctrine convergence, formal-definition preservation, Protocol 7 isolation, or frozen-resource preservation.

## 9. Qualification-method challenge

For every major green claim:

- **Evidence front-matter duplicate rejection:** strong for the evidence record itself; uses the real shared binder and negative fixtures.
- **Exact candidate precedence:** strong for explicit-vs-legacy metadata; future numeric generations remain generic.
- **Root release-state structural coherence:** too strong if inferred from CI. The oracle loads with ordinary `yaml.safe_load`; duplicate source keys can disappear before validation.
- **Lifecycle transition coherence:** too strong if inferred from current transition fixtures. They test legal 6.4->6.5->6.6 paths but not historical/non-successor re-entry.
- **Exact-ref version mapping:** strong for a supplied version/ref pair, but cannot establish that the supplied candidate version is actually a successor.
- **Current representation convergence:** literal tests alone would be weak against semantic predecessor gating; independent semantic inspection found no such surviving gate.
- **Source/generated parity:** proves derivation fidelity, not semantic correctness.
- **Frozen-resource parity:** strong for byte identity of the compared 12 profile/prompt objects.
- **Compression:** word/SHA counts prove reduction only; preservation still depends on semantic Review and frozen/inherited evidence.
- **P5 full CI:** exact-subject observation is valid, but the two holdouts show it cannot establish the stronger claim “complete lifecycle/schema coherence.”

No CI conclusion beyond its discriminated property is inherited.

## 10. Fresh post-P5 mutation/counterexample set

### Machine/state/schema/generated mutants -> executable/structural oracles

Fresh holdouts include:

- duplicate root `candidate.semantic_ref`;
- duplicate root Review `state`;
- duplicate root accepted-current mapping/value;
- evidence duplicate explicit fields/status;
- explicit candidate-field disagreement;
- empty/null/malformed explicit subject;
- lower+higher legacy `pN` coexistence;
- invalid highest-generation `pN`;
- future `p6`/`p17`;
- active candidate version equal to a historical version with a real matching historical commit;
- lower-than-accepted candidate version;
- legal future patch/minor/major successor controls;
- stale mutable lifecycle copies in hot projections;
- source/generated prompt divergence;
- frozen-resource mutation;
- unsafe evidence route forms.

The evidence-binder mutants reject as required. Root duplicate-key and historical-candidate mutants are admitted by the current owner and are blockers.

### Prose semantic mutants -> independent semantic Review

Fresh prose mutants include:

- predecessor-scoped current doctrine expressed by paraphrase without the literal “Protocol 6.4”;
- structurally correct Review metadata with unrelated/false prose;
- structurally correct ratification metadata with unrelated/false prose;
- ratification prose that claims authorization not supplied by the stakeholder;
- generated text semantically diverging from its canonical owner while retaining plausible release terminology.

Meaning-preserving paraphrase controls were used to avoid treating exact wording as a semantic contract. Arbitrary Review/ratification prose remains intentionally outside machine parsing; its semantic truth/authorization is owned by Review/stakeholder processes.

## 11. P65-1 through P65-6 causal ablation

- **P65-1 self-application:** removing it permits SSDP’s own release-state source to receive weaker representation discipline than evidence records. B65-P5-1 is the concrete recurrence. Principle is causal and retained; P5 realization is incomplete.
- **P65-2 state/semantics separation:** removing it recreates copied mutable lifecycle truth and stale immutable semantics. P5 largely realizes ownership separation, but B65-P5-2 shows the owner’s lifecycle domain is underconstrained.
- **P65-3 evidence-claim congruence:** removing it allows green CI to be described as semantic proof. The two holdouts show why claim scope must remain exact.
- **P65-4 Review abstraction adequacy:** removing it would confine Review to B65-P4-1 and miss both new blockers. This Review directly demonstrates causal necessity.
- **P65-5 minimal meta-governance:** removing exact Review/ratification ownership permits inferred acceptance and self-ratification. P5 realizes the principle on the inspected surface.
- **P65-6 integrated current representation:** removing it recreates predecessor-labelled current doctrine and duplicate hot owners. P5 realizes current doctrine convergence on the inspected surface.

No new P65 principle is warranted. The repair is lower-layer concretization work.

## 12. Protocol 6.4 -> 6.5 preservation falsification

The preservation map was treated as a claim to challenge, not authority.

Independently supported preservation includes:

- D1-D4 remain the only semantic authority domains;
- accepted formal-definition/source-availability/well-definedness/parameter/default/warrant semantics remain in current owners;
- evidence specification/realization/observation/assessment and stale/proxy rules remain;
- PEM remains schema-1, project-local, conditionally activated, evidence-backed, and non-authoritative;
- public fallback remains distinct from recovery;
- frozen historical source/profile behavior remains version-bound;
- QF64 proxy predicates may be removed as acceptance machinery without removing their semantic capabilities because those capabilities remain current Review/owner obligations;
- F64 falsification capabilities remain recoverable through current Review/evidence/owner rules;
- Protocol 7 D3/D4 remains isolated.

The map is overstrong where it implies that the new release-state state machine fully preserves/elevates P64-K/P64-O and QF64-K/O/P lifecycle identity. B65-P5-1 and B65-P5-2 show that this concretization is not yet lossless. Repair does not require restoring obsolete QF proxy machinery.

## 13. P0/P5 matched comparison and measurements

Independent matched measurements:

| Measure | P0 | P5 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public fallback SHA copies in that projection | 20 | 0 |
| accepted-6.4 recovery SHA copies in that projection | 12 | 0 |
| frozen 5.16 and 6.0-6.4 profile/prompt objects changed | - | 0 / 12 |
| current canonical shared-reference files in predecessor-scope census | - | 34; 0 scoped matches |

Matched difficult-area assessment:

- **lifecycle/current-state drift:** P5 materially reduces P0 duplication, but its sole owner admits the two blocking state trajectories above;
- **proxy/oracle adequacy:** P5’s Review/ratification evidence oracle is materially stronger than P0-era proxy approaches, but root state and successor-direction oracles remain incomplete;
- **authority/Serious-Challenge routing:** D1-D4 ownership, Challenge routing, and Review/ratification separation remain coherent;
- **mature-system simplification/Review convergence:** kernel size is unchanged, hot projection is smaller, exact mutable SHA copies are eliminated, and no second state registry was added.

No quantitative frontier-model superiority claim is justified. The second contemporary frontier diagnostic remains waived for this cycle.

## 14. Simplicity and total complexity

P5’s P4 repair is appropriately small: one existing loader/binder is strengthened and focused tests are added. It does not introduce a semantic registry, state mirror, candidate-specific table, compatibility subsystem, or prose parser.

The two required repairs should remain equally small:

1. reuse/consolidate the existing duplicate-rejecting loader at the root state boundary;
2. add the missing candidate-successor invariant to the existing state validator.

Do not create a second schema object, candidate registry, migration framework, synchronized phase table, or general semantic-version subsystem where a direct validator predicate suffices.

## 15. Evidence applicability and stale evidence

Still-applicable exact evidence:

- P5 run `36047926253`: valid observation for exact P5 and the actual CI oracles;
- binding run `36048168248`: valid for exact binding descendant state;
- final evidence run `36048331437`: valid for exact final descendant state;
- frozen-resource byte comparison: applicable because P4->P5 did not modify those resources and P0/P5 blob identities were rechecked;
- kernel/hot-projection/SHA-copy measurements: remeasured directly at P0/P5;
- current shared-reference predecessor census: rechecked at exact P5;
- B65-P4-1 focused evidence: applicable to the unchanged repaired binder.

Not transferable as whole-candidate acceptance:

- P1-P4 NO-PASS conclusions;
- P5 author repair conclusion;
- green CI as proof of semantic adequacy;
- any future replacement-candidate Review/ratification status.

A repair to `source/release_state.py` creates a new semantic candidate and invalidates P5-specific whole-candidate Review eligibility. Unchanged-surface preservation evidence may be reused only after verifying implementation dependency remains unaffected.

## 16. Required repair and next lifecycle state

P5 remains immutable and receives **NO-PASS**.

Earliest owning layer remains D4; D3 is not reopened.

Required minimal repairs:

1. **B65-P5-1:** make root release-state loading duplicate-key rejecting using the existing strict YAML mechanism; exercise the actual load boundary with duplicate nested and top-level keys.
2. **B65-P5-2:** require the active pre-cutover candidate to be a true semantic-version successor of accepted-current and disjoint from historical version keys; preserve the explicit terminal accepted-current == candidate cutover state.

Required focused qualification:

- root YAML duplicate-key negatives for top-level and nested lifecycle/evidence fields;
- historical-candidate collision negative using a real version-compatible historical ref;
- lower/equal candidate negatives;
- positive patch/minor/major successor controls;
- existing terminal cutover and next-successor controls;
- full Review/ratification evidence matrix to prove no regression;
- current-owner/historical preservation tests;
- complete inherited regression;
- package/profile/generated parity;
- Orchestrator Core;
- exact-new-candidate normal PR workflow;
- changed-surface evidence-applicability/preservation assessment;
- fresh holdout mutation set;
- later descendant binding with Review reset to `NOT_RUN`;
- fresh independent assembled-candidate Review.

P5-specific binding/evidence descendants become historical lifecycle evidence for P5. They must not be edited to make a replacement candidate appear reviewed.

No stakeholder ratification, public fallback, recovery, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.
