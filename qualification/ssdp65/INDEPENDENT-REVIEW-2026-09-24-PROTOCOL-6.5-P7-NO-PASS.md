---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
semantic_ref: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
p7: 133c747a1f9ab4372c9e1af7a7e9666316dc892b
lifecycle_evidence_head: 67e9a924294311c106579cb0926fd9c76c3a8ec0
binding_descendant: a0ee73af1b2d6af1cdd42533ca007e8a99073ef9
exact_candidate_ci: 36058860629
binding_ci: 36059112506
final_evidence_ci: 36059305935
date: 2026-09-24
serious_challenge: none
d3_reopened: false
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P7

## 1. Disposition

**NO-PASS.**

Immutable Review target:

`P7 = 133c747a1f9ab4372c9e1af7a7e9666316dc892b`

Accepted Protocol 6.4 control:

`P0 = 55c085261eb827e3047637d045a8e6917ea6b962`

P7 is not technically eligible for stakeholder ratification.

P7 remains immutable. Any semantic repair creates a new candidate identity and requires affected exact-candidate qualification plus a fresh independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized by this Review.

One genuine blocker family survives:

**B65-P7-1 — release-state snapshot validity does not enforce the accepted temporal transition / recovery-lineage contract.**

The accepted P65 D3 design remains coherent and is not reopened.

## 2. Independent authority reconstruction

This Review reconstructed the applicable authority from exact P7 and accepted P0 before using author-side repair conclusions.

The applicable architecture requires:

- D1/D2/D3/D4 as the semantic authority domains;
- root `PROTOCOL-RELEASE-STATE.yaml` as the sole mutable SSDP release-state owner;
- immutable version semantics separated from mutable release lifecycle;
- exact semantic-candidate Review binding;
- Review PASS as technical eligibility only;
- explicit stakeholder ratification of that exact reviewed candidate before publication;
- the exact reviewed/ratified semantic candidate as public fallback;
- a **distinct later recovery target containing candidate + Review + ratification + required publication lineage**;
- accepted-current cutover only after the complete transaction;
- preservation of the superseded accepted release as immutable historical identity;
- historical mappings as immutable facts once superseded unless an explicit correction invalidates them;
- current doctrine expressed intrinsically, not predecessor-gated;
- generated representations subordinate to canonical source;
- frozen historical/profile/recovery compatibility;
- Protocol 7 D3/D4 isolation;
- Lossless Representation, evidence applicability, Serious Challenge semantics, progressive disclosure, active simplicity, and PEM non-authority.

The accepted D3 state rules explicitly say that recovery remains distinct **and later**, that recovery is published only after the recovery commit exists, and that historical mappings become immutable facts once superseded. The frozen 6.5 release sequence further requires recovery to contain the candidate, Review, ratification, and required publication evidence before accepted-current promotion.

### PEM / Historical Applicability Set

Project Engineering Memory is material because this is repeated mature self-governance rework under an active workplan.

| PEM item | Disposition | Independent use |
| --- | --- | --- |
| FF-001 premature immutable bootstrap publication | APPLICABLE | hypothesis for publication/recovery ordering; not authority |
| PC-001 frozen prior-version profile/resource preservation | APPLICABLE | authority-bound preservation capability; frozen resources independently checked |
| SP-002 self-reference-safe descendant publication | APPLICABLE | historical evidence that accepted releases use later descendants and distinct recovery |
| DS-001 semantic proxy qualification can overclaim | APPLICABLE | directly relevant to challenging state-machine tests that do not discriminate temporal lineage |
| SP-001 canonical router repair + regeneration | NOT_APPLICABLE to the surviving blocker | no router defect survived |

These records were treated as evidence-bounded hypotheses. Current authority and assembled P7 behavior determined the verdict.

## 3. Serious Challenge pass

**No Serious Challenge.**

The parent architecture is neither contradictory nor unrealizable. The surviving defect is a D4 under-concretization of explicit accepted lifecycle semantics.

The fact that transition/lineage checks are missing from P7 does not show that D3 is wrong. The accepted design already states the required temporal relations.

## 4. Exact identity and lifecycle state

P7 is the semantic Review target. The mutable branch head is not substituted for P7.

Independent Git inspection established:

- branch `ssdp-6.5-frontier-model-re-evaluation` entered Review at `67e9a924294311c106579cb0926fd9c76c3a8ec0`;
- exact P7 is `133c747a1f9ab4372c9e1af7a7e9666316dc892b`;
- binding descendant `a0ee73af1b2d6af1cdd42533ca007e8a99073ef9` binds exact P7;
- final evidence-only descendant `67e9a924294311c106579cb0926fd9c76c3a8ec0` does not alter P7 semantic source;
- entering lifecycle state is:
  - accepted-current: 6.4.0;
  - candidate: 6.5.0;
  - semantic ref: exact P7;
  - Review: NOT_RUN;
  - ratification: NOT_REQUESTED;
  - public fallback: UNAVAILABLE;
  - recovery: UNAVAILABLE.

Workflow metadata independently confirms:

- `36058860629` head = exact P7; build + orchestrator-core success;
- `36059112506` head = exact binding descendant; both jobs success;
- `36059305935` head = exact evidence descendant; both jobs success.

Those runs establish only the mechanical properties their oracles discriminate.

## 5. Mandatory P7 repair falsification

### 5.1 B65-P6-1 — one strict root-state parser semantics

**Closed at P7.**

A repository-wide exact-P7 Python census found no current mechanical read of root `PROTOCOL-RELEASE-STATE.yaml` through ordinary `yaml.safe_load`.

All identified root-state mechanical consumers route through `source/release_state.py::load()`.

Unrelated YAML consumers remain independent:

- PEM YAML parsing remains in its PEM owner;
- package YAML validation remains package validation;
- unrelated fixture/front-matter reads were not gratuitously forced through release-state semantics.

The root loader and Review/ratification front-matter loader share the same duplicate-rejecting `_UniqueKeySafeLoader`.

The constructor rejects duplicate mapping keys recursively before semantic binding. The P7 test suite exercises the actual root owner path rather than reproducing loader code.

Required properties:

1. top-level duplicate keys reject — supported;
2. nested duplicate keys reject recursively — supported;
3. duplicate mappings inside anchors reject — supported by the mapping constructor;
4. ordinary mapping aliases remain coherent — supported;
5. YAML merge-key forms do not create an alternate normalization path — owner loader fails closed rather than delegating to ordinary safe-load semantics;
6. evidence front matter and root state use the same structural mapping rule — supported;
7. no second parser/schema owner was introduced — supported;
8. unrelated YAML was left alone — supported.

Fresh structural holdout not used to design P7:

- an alias-expanded scalar key inside `candidate` that resolves to `version` and coexists with an explicit `version` key is a duplicate after alias resolution; the strict mapping constructor compares constructed keys and therefore rejects it before release-state semantics.

Qualification-method challenge:

> Could all P7 tests remain green while a current executable consumer reads the authoritative root state through different parser semantics?

For the bounded current Python/workflow surface inspected at exact P7, no such bypass survives. The workflow invokes `source/release_state.py`, and all identified Python state consumers call `release_state.load()`.

### 5.2 B65-P6-2 — historical ordering and canonical version identity

**Closed at P7.**

P7 uses canonical ASCII numeric three-component identities:

`^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$`

Consequences independently verified from the owner code and focused tests:

- leading-zero identities reject;
- Unicode decimal-digit identities reject;
- malformed semver rejects;
- ordering is numeric tuple ordering, not lexical;
- `6.10.0` is handled numerically;
- every historical version must be strictly older than accepted-current;
- historical equality with accepted-current rejects;
- candidate/history collision is checked on numeric identity after canonical validation;
- lower/equal active candidates reject except legal complete terminal equality;
- patch/minor/major successors remain generic;
- post-cutover patch/minor/major successors remain generic;
- no P1-P7 candidate-specific version branch exists.

The real-ref P6 history counterexample is now rejected: accepted-current 6.4 cannot coexist with historical 6.5 while candidate 6.6 advances.

Fresh succession/history holdout not used to design P7:

- accepted-current `6.10.0`, historical `6.9.10`, candidate `6.10.1` is admitted by numeric ordering;
- substituting historical `6.11.0` is rejected as future history.

The repaired snapshot-order relation is therefore generic. The surviving P7 blocker is a different temporal relation: cross-state transition/recovery lineage.

## 6. Earlier blocker families

### B65-P5-1 — duplicate-key ambiguity

Closed at the root owner boundary.

The strict loader rejects duplicate mappings before semantic validation, including the required root/nested Review/ratification fields. No ordinary root safe-load consumer survives.

### B65-P5-2 — candidate succession and historical collision

Closed for snapshot semantics.

Lower/equal/historical active candidates reject; generic patch/minor/major and multi-digit successors remain legal; complete terminal equality remains legal only through the full terminal predicate.

### B65-P4-1 / B65-P3-1 — evidence front matter and exact subject identity

Closed for structural subject binding.

- duplicate evidence keys reject before semantic binding;
- explicit `candidate_ref` / `semantic_ref` presence dominates legacy fields;
- empty/null/malformed explicit subjects reject;
- conflicting explicit subjects reject;
- explicit subjects cannot be rescued by lower `pN`;
- highest numeric legacy generation is authoritative only when explicit subjects are absent;
- invalid highest generation cannot fall back lower;
- future numeric generations remain generic;
- Review and terminal ratification share one subject-binding helper.

A structurally correct record with semantically unrelated prose can still satisfy the machine binder. That is an intentional oracle boundary: semantic adequacy remains independent Review work.

### B65-P3-2 / B65-R3 — current representation convergence and predecessor gating

Closed on the inspected P7 current source.

An exact-P7 census of all 34 current `source/shared/references/*.md` owners found no `Protocol 6.4`, `6.4.0`, `predecessor`, or obvious previous/prior/older-protocol/version gates.

The remainder of current canonical `source/` contains only legitimate historical/version-intrinsic references, notably the frozen 6.4 profile preservation edge in `source/SEMANTIC_DEPENDENCIES.md`.

Canonical `development-workflow-prompts.md` and generated Protocol 6.5 `prompts.md` are the same Git blob, so the generated representation is subordinate and faithful.

### B65-P2-1 / B65-R2 — lifecycle-value and phase duplication

No live mutable accepted/candidate phase copy requiring routine edit was found in the inspected current owner/consumer paths.

The P7 repair correctly routes root-state consumers through the owner. Existing historical/version-intrinsic assertions remain legitimate frozen facts.

However, B65-P7-1 shows that **single-snapshot ownership is not sufficient to enforce cross-snapshot lifecycle continuity**.

### B65-P2-2 / B65-R1 — Review and ratification evidence applicability

Exact route, candidate subject, and disposition binding remain structurally sound.

The helper has no P1-P7 table, no contiguous-generation assumption, and no semantic prose parser.

Actual stakeholder authorization remains human/semantic authority and is not inferred from CI, merge, branch position, or metadata.

## 7. New blocker family: B65-P7-1

### Finding

P7 validates one release-state snapshot plus referenced commit/version/evidence facts, but it does not validate the accepted **temporal transition relation** between release states or the required **recovery lineage**.

The validator has no check that:

- a candidate recovery target is later than the reviewed/ratified/publication lineage it is supposed to recover;
- the recovery target actually contains the exact candidate + Review + ratification + public-fallback state;
- the previous accepted-current mapping is preserved unchanged into `historical` when accepted-current advances;
- already historical mappings remain unchanged across legal lifecycle transitions.

### Exact owner

D4 `source/release_state.py` release-state validation/transaction boundary.

No D3 change is required.

### Violated invariants

- state/semantics separation;
- release-state ownership;
- historical identity;
- compatibility/recovery integrity;
- preservation of accepted prior capability;
- evidence-claim congruence;
- self-application;
- Lossless Representation of lifecycle state;
- accepted Review/ratification/publication/recovery ordering.

### Counterexample A — stale same-version recovery

Construct a future otherwise locally coherent P7 state:

- candidate version: 6.5.0;
- semantic ref: exact P7;
- Review: PASS with structurally valid exact-P7 evidence;
- ratification: RATIFIED with structurally valid exact-P7 evidence;
- public fallback: exact P7;
- recovery: immutable P6 `dd06da8136416e67644586c44880b466f982b8ff`.

P6 and P7 both declare `source/PROTOCOL_VERSION = 6.5.0`.

P6 is distinct from P7, so P7's current snapshot checks admit the recovery SHA on syntax/version/distinctness grounds once PASS/RATIFIED/publication metadata are otherwise valid.

But P6 predates P7 itself and therefore cannot contain P7, the P7 independent Review, P7 stakeholder ratification, or P7 public-fallback publication lineage.

This directly violates accepted D3 state rule 8 and the frozen release sequence.

### Counterexample B — locally valid terminal cutover with lost prior accepted identity

The terminal-equality test manually constructs a valid 6.5 cutover by first copying accepted 6.4 into history.

The validator itself does not require that transition.

A terminal snapshot can therefore be constructed with:

- accepted-current = 6.5;
- candidate = 6.5 complete terminal state;
- history still containing only versions through 6.3.

Snapshot-local predicates do not encode “the previously accepted 6.4 mapping must move unchanged into historical.”

Current Protocol 6.4 preservation tests happen to protect the presently known 6.4 identity, but the release-state owner remains non-generic: after a future 6.5 -> 6.6 transition, equivalent continuity would require another release-specific assertion unless the owner validates the transition relation itself.

### Counterexample C — historical mapping rewrite

Snapshot validation checks that a historical public/recovery ref exists, declares the mapped version, and is distinct.

It does not compare the mapping with the prior release-state snapshot. Therefore a prior historical mapping can be deleted or replaced by another same-version ref and remain locally schema-valid unless a release-specific test happens to hard-code that identity.

This violates the accepted rule that historical mappings are immutable facts once superseded absent explicit correction.

### Consequence

The sole mutable state file can represent a locally valid state that violates the global lifecycle it is supposed to own.

Most materially, an accepted-current cutover could be paired with a “recovery” target that cannot recover the reviewed/ratified/published release at all.

This is a compatibility and release-integrity blocker.

### Smallest owning-layer repair

Alter the existing release-state owner/validator. Do **not** add a second state file, registry, mirror, transition service, compatibility subsystem, semantic parser, or candidate-specific table.

The existing owner already has Git access through `_git`; use that boundary to validate temporal relations when repository context is available.

Required repair behavior:

1. Treat release-state validation as both snapshot validation and, when the root state changes, transition validation against the immediately prior governed release-state snapshot on the transition history.
2. Preserve every prior historical mapping unchanged unless an explicit separately authorized correction path exists.
3. When `accepted_current.version` advances, require the previous accepted-current mapping to appear unchanged in current `historical`.
4. When `candidate.recovery_ref` becomes available, require it to be a genuine later recovery target:
   - distinct from semantic/public fallback;
   - descendant of the semantic candidate;
   - on the governed lineage leading to the state that publishes the recovery mapping;
   - its repository snapshot must already contain the same candidate semantic ref, Review PASS evidence, RATIFIED evidence, and exact public fallback so the target actually contains the required lifecycle/publication lineage.
5. Terminal accepted-current cutover remains legal only after these transition/lineage predicates are satisfied.
6. Keep future patch/minor/major progression generic. Do not encode P7, 6.5, or contiguous `pN` assumptions.

The repair should use current structural state/evidence fields and Git ancestry/state inspection. It must not attempt to infer human authorization from prose.

### Affected qualification to rerun

At minimum:

- full `tests/test_protocol_65_release_state.py`;
- exact recovery-lineage negative using P6 as the P7 recovery candidate;
- positive recovery descendant that already contains exact candidate + PASS + RATIFIED + public-fallback state;
- recovery target with correct `PROTOCOL_VERSION` but stale/missing lifecycle state;
- accepted-current cutover omitting prior accepted mapping;
- accepted-current cutover mutating prior accepted public or recovery mapping;
- historical deletion/rewrite transition;
- valid 6.4 -> 6.5 cutover preserving exact 6.4 mapping;
- future 6.5 -> 6.6 equivalent transition;
- patch/minor/major successor controls;
- complete terminal equality and incomplete terminal equality;
- full repository build and Orchestrator Core;
- frozen historical-resource parity;
- current-representation/source-generated parity;
- exact replacement-candidate qualification, freeze/binding, and fresh independent assembled-candidate Review.

## 8. Defect-family result

| Defect family | Result | Review |
| --- | --- | --- |
| DF-1 release-state/version lifecycle ownership | **NO-PASS** | B65-P7-1: snapshot validity does not enforce transition/recovery lineage |
| DF-2 qualification/Review epistemology | PASS with bounded claims | structural subject/disposition binding is sound; semantic prose remains Review-owned |
| DF-3 meta-control semantics/governance | PASS | Review/ratification/Challenge/PEM ownership remains coherent |
| DF-4 representation/schema/convergence self-application | **NO-PASS through DF-1 dependency** | one state owner exists, but its representation does not fully encode/validate the temporal lifecycle relation it claims to own |

## 9. Local-compliance / global-failure trajectories

### Trajectory 1 — stale recovery

Every local field is valid:

- canonical 6.5 version;
- exact P7 semantic/public ref;
- PASS;
- RATIFIED;
- distinct 40-hex recovery;
- recovery commit declares 6.5.

Global failure: recovery is P6, which predates P7 and cannot contain P7 lifecycle/publication evidence.

### Trajectory 2 — accepted cutover loses predecessor mapping

Every current terminal predicate can be satisfied for 6.5.

Global failure: prior accepted 6.4 is absent from historical state, breaking exact historical recovery/compatibility.

### Trajectory 3 — historical rewrite

A historical mapping is replaced by a different same-version immutable SHA pair.

Local ref/version checks pass.

Global failure: an already-superseded immutable historical identity silently changes.

### Other trajectories re-falsified

- wrong explicit Review subject + matching lower generation: rejects;
- invalid highest legacy generation + valid lower generation: rejects;
- noncanonical version spellings: reject;
- future historical version above accepted-current: rejects;
- candidate historical resurrection: rejects;
- source/generated current prompt divergence: parity oracle discriminates;
- predecessor-scoped current doctrine: independent current-source inspection found none;
- structurally correct but semantically unrelated Review prose: machine binder can accept; independent semantic Review remains responsible;
- stakeholder-ratification authorization laundering: machine metadata cannot establish human authorization; the protocol correctly keeps this a human/semantic ownership boundary.

## 10. Out-of-matrix abstraction-adequacy pass

A fresh material defect class survives: **temporal transition/lineage congruence**.

This class is distinct from B65-P6-2 snapshot ordering. P7 can have perfectly canonical versions and correctly ordered history inside one snapshot while still representing a lifecycle trajectory that never occurred or a recovery target that cannot recover the accepted lifecycle state.

No Serious Challenge follows because accepted D3 already specifies the missing relation.

No second fresh blocker family survived proportionate inspection.

## 11. Challenge to qualification method

For each major claim:

| Claim | Could the oracle remain green while the claimed property is broken? | Result |
| --- | --- | --- |
| root parser convergence | no current bypass found in bounded Python/workflow census | supported |
| recursive duplicate rejection | strict owner constructor discriminates duplicates | supported |
| aliases/anchors/merge behavior | aliases remain structural; duplicate constructed keys reject; merge does not create ordinary safe-load bypass | supported |
| canonical version identity | regex and numeric tuple ordering discriminate | supported |
| history older than accepted-current | snapshot oracle discriminates | supported |
| candidate/history disjointness | snapshot oracle discriminates | supported |
| terminal equality | complete/incomplete snapshot predicates discriminated | supported but incomplete as a transition oracle |
| recovery is distinct | discriminated | supported |
| recovery is **later and contains lifecycle/publication lineage** | **yes** | **overclaim / B65-P7-1** |
| prior accepted mapping becomes immutable history at cutover | **yes without release-specific assertions** | **overclaim / B65-P7-1** |
| Review evidence exact subject/disposition | discriminated structurally | supported |
| substantive Review prose adequacy | yes | correctly left to independent Review |
| actual stakeholder authorization | yes | correctly left to human authority |
| source/generated prompt parity | exact blob identity discriminates | supported |
| frozen 5.16–6.4 profile/prompt parity | exact blob comparison discriminates | supported |
| compression/simplicity | counts can stay good while lifecycle is wrong | descriptive only |
| predecessor-scope census | literal census can miss paraphrase | independent semantic inspection also performed |
| future version progression | patch/minor/major/multi-digit snapshot progression generic | supported; transition continuity is the missing dimension |

## 12. Fresh post-P7 mutation/counterexample set

### Machine/state/schema/generated mutants

| Mutant | Result |
| --- | --- |
| alias-expanded duplicate scalar key for `candidate.version` | strict owner rejects by constructed-key equality |
| duplicate Review/ratification front-matter keys | reject before semantic binding |
| explicit candidate fields disagree | reject |
| null/empty/malformed explicit subject + valid lower `pN` | reject; no fallback |
| lower/higher `pN` coexist | highest numeric generation owns subject |
| invalid highest generation | reject; no lower fallback |
| noncanonical ASCII leading-zero / Unicode version | reject |
| accepted 6.10.0, history 6.9.10, candidate 6.10.1 | valid numeric progression |
| history 6.11.0 under accepted 6.10.0 | reject |
| historical candidate resurrection | reject |
| source/generated current prompt divergence | exact parity oracle discriminates |
| frozen prior profile/prompt mutation | blob-parity oracle discriminates |
| **P7 public fallback + P6 as recovery** | **snapshot checks do not reject lineage -> blocker** |
| **terminal 6.5 cutover without carrying prior accepted 6.4 into history** | **transition continuity not owned generically -> blocker** |
| **rewrite/delete an existing historical mapping using same-version valid refs** | **snapshot validator has no previous-state congruence -> blocker family** |

### Prose semantic mutants

Independent semantic Review rejects:

- predecessor-conditioned current obligations by paraphrase;
- an agent/CI/merge treating itself as stakeholder ratifier;
- a Review record with structurally correct P7 metadata but prose unrelated to P7;
- a ratification record whose text does not actually express stakeholder authorization;
- compression that drops a protected P64/QF64/F64 capability;
- generated prose that changes canonical semantics while structural format remains valid.

Meaning-preserving paraphrases remain acceptable when owner, lifecycle order, evidence scope, and authority relations are unchanged.

## 13. P65-1 through P65-6 causal ablation

| Principle | Causal ablation | P7 realization |
| --- | --- | --- |
| P65-1 self-application | exempt release engineering from its own lifecycle semantics -> green local state can violate global release order | **incomplete: B65-P7-1** |
| P65-2 state/semantics separation | allow lifecycle truth in versioned source/copies -> stale current state | substantially realized; temporal state relation remains under-enforced |
| P65-3 evidence-claim congruence | allow a terminal/recovery test to claim more than it discriminates -> stale recovery appears valid | **incomplete at recovery/transition oracle** |
| P65-4 Review abstraction adequacy | restrict Review to author repair matrix -> temporal lineage defect survives | causally necessary and realized by this fresh Review |
| P65-5 minimal meta-governance | collapse Review/ratification/PEM/Challenge roles -> inferred acceptance | realized |
| P65-6 integrated current representation | let generated/current surfaces diverge or lifecycle owner omit temporal relation -> fragmented current truth | representation convergence is strong; lifecycle integration remains incomplete through B65-P7-1 |

No new P65 principle is required.

## 14. Protocol 6.4 -> 6.5 preservation falsification

Independent controls support preservation of:

- D1-D4 authority separation;
- formal-definition/axiomatic doctrine;
- evidence/evolution semantics;
- PEM non-authority;
- current-source predecessor-gate removal;
- exact source/generated current prompt parity;
- frozen historical profiles/resources;
- Protocol 7 D3/D4 isolation.

Exact P0/P7 blob comparison found **zero differences across all 12 frozen profile/prompt objects** for Protocol 5.16 and 6.0–6.4.

All six Protocol 7 D3/D4 workplan/reconciliation artifacts inspected are blob-identical P0 -> P7.

Accepted historical recovery behavior also supplies a strong control for B65-P7-1:

- 6.1 recovery is a descendant of its public fallback;
- 6.2 recovery is a descendant of its public fallback;
- 6.3 recovery is a descendant of its public fallback;
- 6.4 recovery `74bc572...` is 62 commits after public fallback `e09a9d1...`.

Thus “later recovery” is demonstrated accepted behavior as well as explicit P65 design authority.

The preservation map is therefore overstrong only where it implies P7 fully preserves generic lifecycle/recovery transition semantics. B65-P7-1 prevents that conclusion.

## 15. Simplicity and total complexity

P7 remains materially simpler than P0 on the intended current-state duplication surface:

- no second release-state file;
- no state mirror;
- no version registry;
- no candidate-specific table;
- no semantic prose parser;
- no synchronized phase table;
- no new YAML parser service;
- no compatibility wrapper.

Independent matched measurements:

| Measure | P0 | P7 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public fallback SHA copies in that projection | 20 | 0 |
| accepted-6.4 recovery SHA copies in that projection | 12 | 0 |
| frozen 5.16/6.0–6.4 profile/prompt object differences | — | 0 / 12 |

Compression is a real representational improvement only because most protected capability is preserved. B65-P7-1 is exactly why the numerical reduction cannot itself justify PASS.

The repair should not add a transition registry or parallel schema. The existing owner already has Git/ref access and should directly enforce the missing relation.

## 16. P0/P7 matched difficult-area comparison

### Lifecycle/current-state drift

P7 is substantially better than P0:

- one mutable owner;
- zero hot copies of accepted 6.4 public/recovery refs in the defined projection;
- strict one-parser root semantics;
- canonical version identity;
- generic snapshot succession/history rules.

It remains NO-PASS because snapshot coherence is weaker than the accepted lifecycle transaction.

### Proxy/oracle adequacy

P7 improved real-owner binding and exact evidence subject checks.

The remaining proxy defect is precise: current terminal/recovery tests prove snapshot legality, not that the recovery target is on the required lineage or that transition continuity preserved the prior accepted state.

### Authority / Serious Challenge routing

No Serious Challenge.

Review PASS, stakeholder ratification, publication, recovery, accepted-current, PEM, and D1-D4 roles remain distinct.

### Mature-system simplification / Review convergence

The system is smaller and more coherent than P0 on the intended duplication surface. The surviving repair is a direct strengthening of the existing owner, not justification for new machinery.

No frontier-model superiority claim is made. The second contemporary frontier diagnostic remains waived.

## 17. Evidence applicability

Still applicable after this NO-PASS, subject to unchanged-surface verification:

- exact-P7 CI `36058860629` for the mechanical properties it actually exercised;
- binding/final descendant runs `36059112506` and `36059305935` for their exact lifecycle/mechanical states;
- B65-P6-1 parser-convergence evidence;
- B65-P6-2 canonical-version/history snapshot evidence;
- exact evidence-subject/disposition binding;
- P0/P7 frozen-resource parity;
- source/generated current-prompt parity;
- current predecessor-scope census;
- unchanged D1/D2/formal-definition/PEM/Protocol-7 surfaces;
- current compression/copy counts as descriptive measurements.

Stale for any replacement candidate:

- whole-candidate P7 semantic Review conclusion;
- P7 exact-candidate CI as replacement-candidate qualification;
- P7 freeze/binding qualification as replacement identity evidence;
- any claim that release-state lifecycle validation is fully closed;
- terminal/recovery mutation conclusions affected by transition-lineage repair;
- candidate-level preservation closure dependent on the release-state transaction.

Any replacement must re-establish applicability rather than inheriting P7 wholesale.

## 18. Required next state

1. Preserve P7 immutably.
2. Record this Review as P7 `NO_PASS` from a later descendant.
3. Reopen the existing D4 workplan only for B65-P7-1.
4. Keep accepted P65 D3 closed.
5. Repair by altering the existing release-state owner/validator, not by adding a new state authority.
6. Add transition-continuity and recovery-lineage holdouts, including the stale-P6-as-P7-recovery counterexample.
7. Freeze a **new immutable semantic candidate**.
8. Rerun affected exact-candidate qualification and normal CI.
9. Bind the replacement from a later descendant with Review reset to `NOT_RUN`.
10. Perform another genuinely fresh independent assembled-candidate Review.

No stakeholder ratification or publication action is authorized.
