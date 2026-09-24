---
kind: independent-assembled-candidate-review
status: no-pass
protocol_under_review: 6.5.0
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_candidate_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_candidate_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_candidate_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
candidate_ref: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
lifecycle_descendant_examined: 72ea6663d5d0e4d0b6baa864937eaf54c07fa380
reviewer_model: GPT-5.6-Sol
review_date: 2026-09-24
serious_challenge: none
blockers: 1
impact_closure: repair-required-new-candidate
stakeholder_ratification: NOT_REQUESTED
public_fallback: UNAVAILABLE
recovery: UNAVAILABLE
accepted_current: 6.4.0
protocol_7_d3_d4: unchanged
---

# Fresh Independent Assembled-Candidate Review - Protocol 6.5 P4

## 1. Disposition

**NO-PASS.**

P4 is materially closer to the accepted Protocol 6.5 design than P1-P3, and the predecessor-scope/current-representation repair independently holds. However, one genuine D4 evidence-applicability blocker survives in the existing release-state evidence binder.

P4 remains immutable at 43ff4273fbdaf46b9677cffdb091b741ce754a7d.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.

## 2. Serious Challenge pass

**No Serious Challenge.**

The accepted P65 D3 architecture is coherent and realizable: one mutable release-state owner, version-intrinsic semantics separated from mutable state, independent Review separated from stakeholder ratification, exact immutable evidence routes, and human semantic authorization kept outside mechanical prose interpretation.

The surviving defect is a D4 concretization failure in the structural evidence parser. It does not show the accepted D3 parent to be false, contradictory, ambiguous, mutually incompatible, inadequate, or unrealizable.

## 3. Independently reconstructed authority and lifecycle state

The Review reconstructed applicable authority from P0 and P4 before using repair-side conclusions. Governing constraints include:

- D1/D2/D3/D4 ownership separation;
- one current semantic/state owner per material claim;
- state/semantics separation;
- evidence specification/realization/assessment and exact applicability;
- Lossless Representation and progressive disclosure;
- Serious Challenge only for defective accepted authority;
- active simplicity and removal/rewiring before additive machinery;
- PEM as non-authoritative project learning;
- stakeholder ratification as a distinct human acceptance gate;
- frozen historical compatibility and Protocol 7 isolation;
- self-application and current-representation convergence.

The later lifecycle descendant 72ea6663d5d0e4d0b6baa864937eaf54c07fa380 independently resolves to:

- accepted-current: Protocol 6.4.0;
- candidate: Protocol 6.5.0;
- candidate semantic ref: exact P4;
- Review: NOT_RUN;
- ratification: NOT_REQUESTED;
- public fallback: UNAVAILABLE;
- recovery: UNAVAILABLE.

All six active Protocol 7 workplan blobs are identical between P0 and P4. No Protocol 7 D3/D4 mutation was found.

## 4. Mandatory P4 repair falsification

### 4.1 B65-P3-1 - exact evidence-subject identity

The P4 binder is materially improved over P3:

- same-repository immutable commit/path resolution is required;
- absolute and parent-traversal paths reject;
- nonexistent commit/path reject;
- Review and terminal ratification share the same subject resolver;
- explicit candidate_ref / semantic_ref values, when truthy, override legacy pN;
- conflicting truthy explicit fields reject;
- otherwise the highest numeric legacy pN generation is selected;
- future generations such as p5 require no P4-specific code;
- arbitrary prose is intentionally outside machine semantic judgment.

A fresh isolated probe reproducing the exact P4 front-matter and subject-resolution logic produced the required baseline outcomes:

| Case | Result |
| --- | --- |
| exact candidate + PASS | ACCEPT |
| exact candidate + NO_PASS | ACCEPT |
| exact candidate + RATIFIED | ACCEPT |
| exact candidate + REJECTED | ACCEPT |
| wrong candidate | REJECT |
| Review disposition mismatch | REJECT |
| terminal ratification disposition mismatch | REJECT |
| wrong repository | REJECT |
| absolute path | REJECT |
| parent traversal | REJECT |
| nonexistent commit | REJECT |
| nonexistent path | REJECT |
| missing front matter | REJECT |
| wrong explicit candidate_ref + matching historical p3 | REJECT |
| wrong explicit semantic_ref + matching historical p3 | REJECT |
| conflicting truthy candidate_ref / semantic_ref | REJECT |
| p3 + p4, validate as P3 | REJECT |
| p3 + p4, validate as P4 | ACCEPT |
| future p5 | ACCEPT |
| structurally valid Review metadata + false/unrelated prose | ACCEPT, intentionally |
| structurally valid ratification metadata + false/unrelated prose | ACCEPT, intentionally |

The mandatory baseline therefore closes the original P3 set-membership defect for ordinary unambiguous mappings.

A fresh holdout outside the author test matrix defeats the stronger P4 structural claim, however:

1. duplicate candidate_ref keys are silently normalized by yaml.safe_load using last-key-wins behavior;
2. duplicate status keys are likewise silently normalized;
3. an explicitly present but empty candidate_ref is ignored because the binder tests metadata.get(key), then legacy pN is allowed to bind the candidate;
4. an explicitly present semantic_ref: null is similarly ignored and legacy pN is allowed to bind.

Concrete counterexamples accepted by the P4 logic include:

~~~yaml
---
status: pass
candidate_ref: 3333333333333333333333333333333333333333
candidate_ref: 4444444444444444444444444444444444444444
---
~~~

when validating candidate 4444..., and:

~~~yaml
---
status: pass
candidate_ref:
p4: 4444444444444444444444444444444444444444
---
~~~

when validating the same candidate.

A disposition can also be normalized from contradictory duplicate status fields:

~~~yaml
---
status: no-pass
status: pass
candidate_ref: 4444444444444444444444444444444444444444
---
~~~

and then accepted as PASS.

These are machine-readable structural ambiguities, not arbitrary prose semantics.

### 4.2 B65-P3-2 - current representation convergence

**Closed for P4.**

An independent bounded scan of all 34 current canonical source/shared/references/*.md owners found no current normative occurrence of:

- Protocol 6.4;
- 6.4.0;
- predecessor;
- equivalent previous/prior/older protocol/version conditioning.

Manual semantic inspection of the kernel, workflow, evidence, testing, and versioning owners found current obligations expressed intrinsically rather than gated on predecessor identity.

The repaired evidence-owner sentence is protocol-current. Its generated copies in all seven generated skill trees are content-identical to the canonical owner. Frozen 5.16 and 6.0-6.4 resources remain untouched.

Protocol 7's frozen inheritance baseline remains distinct from current Protocol 6.5 ownership.

## 5. Blocking finding

### B65-P4-1 - structurally ambiguous evidence front matter can still manufacture an exact binding

**Finding ->** P4's front-matter normalization can convert an ambiguous or explicitly invalid machine-readable evidence record into a single apparently valid candidate/disposition before the exact-subject check runs.

**Exact owner ->** D4 release-state evidence validation in source/release_state.py, specifically the front-matter parser and candidate-subject resolver shared by Review and terminal ratification.

**Violated invariant ->**

- exact evidence-subject identity;
- explicit subject fields take precedence when present;
- invalid/ambiguous structural bindings reject;
- evidence-claim congruence;
- Lossless Representation of decision-critical candidate/disposition identity.

**Counterexample/evidence ->**

- duplicate candidate_ref values collapse last-wins;
- duplicate status values collapse last-wins;
- present empty/null explicit subject fields are treated as absent and legacy pN is allowed to rescue the record.

The existing P4 test suite does not cover these cases, and exact-P4 CI remains green while they survive.

**Consequence ->** A lifecycle transition can record Review PASS/NO-PASS or terminal RATIFIED/REJECTED against a structurally ambiguous record even though the binder claims one unambiguous exact evidence subject and disposition. The machine layer can therefore overstate the evidence property it discriminates.

**Smallest owning-layer repair ->**

1. alter the existing front-matter parser to reject duplicate mapping keys rather than silently normalize them;
2. determine explicit candidate-field presence by key membership, not truthiness;
3. if candidate_ref or semantic_ref is present, require a nonempty valid exact candidate SHA value; do not fall back to legacy pN from an empty/null/malformed explicit field;
4. when both explicit fields are present, require exact agreement;
5. keep the current generic highest-generation legacy pN rule only when no explicit subject key is present;
6. keep arbitrary prose outside machine semantic judgment;
7. do not add a registry, state mirror, candidate-specific table, compatibility subsystem, or semantic prose parser.

**Affected qualification to rerun ->**

- full exact Review/ratification subject/disposition matrix;
- duplicate-key, empty/null explicit-subject, and duplicate-status negatives;
- future pN generation;
- wrong repository/path/commit/path negatives;
- lifecycle transition fixtures;
- complete repository regression and Orchestrator Core;
- exact replacement-candidate CI;
- fresh independent assembled-candidate Review.

Any semantic repair requires a new immutable candidate identity.

## 6. Re-falsification of earlier blocker families

### B65-P2-1 / B65-R2 - lifecycle values and phase duplication

**Closed on the reviewed P4 surface.**

The root release-state file remains the sole mutable owner. The surviving tests exercise lifecycle-independent invariants rather than requiring hard-coded live Review/ratification/publication phase values.

The legal 6.4 -> 6.5 fixture can move 6.4 into historical state and establish 6.5 as accepted-current, then begin a 6.6 candidate at UNFROZEN / NOT_RUN / NOT_REQUESTED / UNAVAILABLE / UNAVAILABLE.

No inspected current operational document or executable invariant requires an edit merely because the sole mutable owner legally advances.

The validator does not, by itself, prove append-only preservation of historical mappings across arbitrary future edits. That is a qualification-method limitation to retain at cutover; it is not a P4 assembled-state blocker because the actual P4 state preserves the accepted mappings and frozen historical resources.

### B65-P2-2 / B65-R1 - Review and terminal-ratification applicability

The original exact-candidate/disposition route is improved and shared, but **not fully closed** because B65-P4-1 permits structural ambiguity before binding. This family therefore remains blocking only through the newly isolated parser boundary.

### B65-R3 - predecessor-version gating

**Closed.**

Inherited exact-contract, formal-definition, Review, Verification, Stabilization, audit, evidence, and closeout obligations are expressed as current/generic obligations rather than Protocol-6.4-conditioned rules.

## 7. Full defect-family reassessment

### DF-1 - release-state/version lifecycle ownership

Materially improved and assembled coherently in P4. One root mutable state owner exists; current hot surfaces route rather than copy exact mutable mappings.

### DF-2 - qualification/Review epistemology

Improved but **NO-PASS** because the structural evidence oracle can still accept ambiguous machine evidence. The defect is not that arbitrary prose remains unparsed; that separation is correct.

### DF-3 - meta-control semantics/governance

No blocker found. Independent Review, Serious Challenge, stakeholder ratification, accepted-memory policy, and acceptance/publication distinctions remain separated.

### DF-4 - representation/schema/convergence self-application

No blocker found outside B65-P4-1. Current predecessor-labelled doctrine is integrated, generated representation remains derivative, and the protocol is applying its own Review/evidence rules to this successor cycle.

## 8. Local-compliance/global-failure trajectories

Fresh trajectories were constructed rather than inheriting the author's matrix.

### Evidence applicability

All obvious route, SHA, candidate, and disposition checks can appear locally satisfied after YAML normalization while the original evidence text contains contradictory duplicate candidate/disposition fields. Local parser success therefore permits global evidence-applicability failure.

### Lifecycle ordering

Review PASS and stakeholder ratification remain distinct and publication/recovery ordering is structurally guarded. No trajectory was found that publishes fallback before PASS+RATIFIED through the reviewed state machine.

### Authority separation

No local route was found that lets CI, merge, branch position, PEM, or generated packages manufacture stakeholder ratification or accepted-current authority.

### Generated representation

Canonical/generated parity can remain green if canonical semantics themselves are wrong; parity is therefore treated as representation evidence only. No generated copy was found acting as a second semantic owner.

### PEM

PEM remains decision support rather than a fifth authority domain. No candidate acceptance route was found through memory state.

### Compatibility and succession

Frozen predecessor resource identity holds. Generic legacy pN subject resolution supports P5 and later numeric generations without candidate-specific branches.

## 9. Out-of-matrix abstraction-adequacy pass

The fresh holdout is the structural-normalization boundary itself.

P4's author matrix tests semantic disagreement after YAML has become a Python mapping. It does not challenge whether parsing can erase disagreement before the subject/disposition validator sees it.

This is a material sibling defect not supplied by the P4 repair matrix and demonstrates why the accepted P65-4 out-of-matrix Review principle remains causal.

No accepted D3 abstraction change is required: the existing architecture already requires an unambiguous machine evidence subject. The D4 parser simply fails to realize it completely.

## 10. Qualification-method challenge

For each major claim:

- **Exact candidate evidence applicability:** current oracle can remain green under duplicate/empty explicit-field mutants -> claim stronger than oracle; blocking.
- **Review prose semantic adequacy:** machine suite intentionally cannot prove it -> independent semantic Review remains required; not a defect.
- **Stakeholder authorization:** candidate/disposition metadata cannot prove a human actually authorized the record -> human semantic adjudication remains required; do not strengthen the machine claim.
- **Lifecycle transition legality:** state fixtures prove selected legal/illegal states, not append-only historical transition provenance -> retain future cutover semantic/diff review.
- **Source/generated parity:** proves representation equality, not semantic correctness.
- **Frozen-resource parity:** proves predecessor bytes unchanged, not full successor capability preservation.
- **Compression:** word/SHA-copy counts prove compression and copy removal, not lossless semantic preservation.
- **Predecessor-scope census:** literal/semantic census is evidence, not a theorem; manual current-owner Review was also performed.
- **Future-candidate generality:** regex numeric-generation selection is generic; no P1-P4 enumeration was found.

## 11. Fresh mutation/counterexample set

### Machine/state/schema/generated mutants -> executable oracle

Expected to reject:

- duplicate candidate_ref;
- duplicate semantic_ref;
- duplicate status;
- explicit candidate field present but empty/null;
- conflicting explicit candidate fields;
- lower/higher pN coexistence when validating lower generation;
- wrong repository;
- unsafe path;
- missing commit/path;
- stale mutable lifecycle copies;
- source/generated divergence.

Expected to accept where structurally valid:

- exact subject/disposition;
- highest unambiguous future p5/later pN;
- meaning-preserving prose paraphrase because prose is not the mechanical contract.

### Prose semantic mutants -> independent semantic Review

- structurally correct Review metadata with unrelated/false prose;
- structurally correct ratification metadata whose prose does not establish real stakeholder authorization;
- predecessor-scoped current doctrine expressed through a paraphrase rather than the literal old label.

No prose theorem prover or broad exact-string semantic oracle is warranted.

## 12. P65-1 through P65-6 causal ablation

| Principle | Ablation consequence | P4 realization |
| --- | --- | --- |
| P65-1 self-application | protocol release work can exempt itself from its own evidence/Review rules | materially realized; this Review is exercising it |
| P65-2 state/semantics separation | immutable/current surfaces drift when lifecycle advances | realized through root release-state owner and removal of hot exact copies |
| P65-3 evidence-claim congruence | structural evidence can claim a subject/property it did not actually discriminate | **not fully realized due B65-P4-1** |
| P65-4 Review abstraction adequacy | author matrix can pass while an out-of-matrix structural boundary remains broken | realized by this independent holdout; principle remains causal |
| P65-5 minimal meta-governance | acceptance/Challenge/ratification controls can proliferate or blur | realized without a new registry/ontology |
| P65-6 integrated current representation | release-labelled amendment residue and generated owners can fragment current meaning | materially realized; predecessor residue repair and generated parity hold |

## 13. Protocol 6.4 -> 6.5 preservation falsification

No loss was found in:

- D1-D4 authority separation;
- formal-definition/axiomatic doctrine;
- evidence/evolution semantics;
- Serious Challenge routing;
- PEM boundaries;
- compatibility/recovery distinction;
- frozen historical mappings/resources;
- Protocol 7 isolation.

Removed proxy/exact-string machinery is not treated as protected capability where stronger current semantic Review/evidence rules preserve the real property.

The structural binder blocker does not imply general P64 capability loss; it prevents P4 from proving the strengthened P65 exact-evidence capability required for acceptance.

## 14. P0/P4 matched comparison and measurements

Independently reproduced exact measurements:

| Measure | P0 | P4 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public fallback SHA copies in that projection | 20 | 0 |
| accepted-6.4 recovery SHA copies in that projection | 12 | 0 |
| frozen 5.16 and 6.0-6.4 profile/prompt objects changed | - | 0 / 12 |

Matched difficult-area assessment:

- **lifecycle/current-state drift:** P4 materially reduces P0's duplicated mutable state by centralizing ownership;
- **proxy/oracle adequacy:** P4 improves exact route/subject/disposition checking but the holdout structural-normalization counterexample remains;
- **authority/Serious-Challenge routing:** P4 preserves the D1-D4/Challenge distinction and separates Review from stakeholder ratification;
- **mature-system simplification/convergence:** kernel size is unchanged while the defined hot projection is substantially smaller and exact mutable SHA copies are eliminated without adding a second registry.

The duplicate-key/null-explicit-field holdout was not used to design the P4 repair and provides the required fresh case.

No quantitative frontier-model superiority claim is made. The second contemporary frontier diagnostic remains waived for this cycle.

## 15. Simplicity and total complexity

P4 does **not** introduce a second release-state owner, semantic registry, prose parser, candidate-specific phase table, or synchronized state mirror.

The remaining repair should stay inside the existing parser/binder. A new evidence subsystem would be less justified than making the current structural parser strict.

## 16. Evidence applicability and stale evidence

Exact-P4 CI run 36041360949 is a valid observation that the repository build and Orchestrator Core oracles passed P4. Binding run 36042040459 and final evidence run 36042262606 are likewise valid for their exact descendant states.

They do **not** discriminate duplicate-key or present-empty-explicit-field ambiguity and therefore cannot close B65-P4-1.

After repair and a new candidate identity:

**Must rerun / becomes stale for whole-candidate closure:**

- P4 exact evidence-binding qualification;
- P4 B65-P3-1 closure claim;
- exact replacement-candidate build/Core CI;
- replacement-candidate Review applicability;
- fresh mutation/out-of-matrix Review.

**Reusable only after unchanged-surface identity is verified:**

- P0 accepted baseline;
- B65-P3-2 current-representation convergence;
- P0/P4 measurement method and P0 counts;
- frozen-resource identity evidence;
- unchanged D1/D2/formal-definition owners;
- Protocol 7 isolation.

P4 itself and its Review remain immutable historical evidence.

## 17. Required repair and next lifecycle state

Reopen only the existing D4 release-state validation owner.

The next repair candidate must:

1. reject duplicate YAML mapping keys in evidence front matter;
2. reject empty/null/malformed explicit candidate fields rather than silently treating them as absent;
3. preserve explicit-field precedence and agreement;
4. preserve generic highest-generation legacy pN behavior only when explicit subject keys are absent;
5. preserve the machine/prose boundary;
6. rerun affected exact-candidate qualification and fresh independent Review.

D3 remains closed unless the implementation proves strict structural binding cannot be realized within the accepted owner architecture.

P4 is **not technically eligible for stakeholder ratification**.
