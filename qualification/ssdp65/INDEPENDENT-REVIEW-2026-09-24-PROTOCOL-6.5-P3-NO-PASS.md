---
kind: independent-assembled-candidate-review
status: no-pass
protocol_under_review: 6.5.0
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_candidate_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_candidate_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
lifecycle_descendant_examined: 75d73e73d0a6a8bcfc08e9b6f2df1d5488fe7f01
reviewer_model: GPT-5.6-Sol
review_date: 2026-09-24
serious_challenge: none
blockers: 2
impact_closure: repair-required-new-candidate
stakeholder_ratification: NOT_REQUESTED
public_fallback: UNAVAILABLE
recovery: UNAVAILABLE
accepted_current: 6.4.0
protocol_7_d3_d4: unchanged
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P3

## 1. Disposition

**NO-PASS.**

No Serious Challenge is raised against accepted Protocol authority. The reconstructed parent system is coherent and jointly realizable. The surviving defects are P3 concretization/current-representation defects and therefore remain ordinary blockers.

P3 remains immutable:

```text
P3 = 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
```

against accepted Protocol 6.4 control:

```text
P0 = 55c085261eb827e3047637d045a8e6917ea6b962
```

P1 and P2 remain immutable historical NO-PASS evidence only. No prior Review conclusion was inherited.

## 2. Independent authority reconstruction

Before consulting P3 repair/handoff conclusions, this Review reconstructed the applicable authority from P0 and the assembled P3 canonical owners.

The governing constraints are:

- D1, D2, D3 and D4 remain the only semantic authority domains; evidence and PEM do not become D5;
- each material normative claim has one current owner and current normative ownership is acyclic;
- concretization fidelity and abstraction adequacy are distinct;
- mutable lifecycle state is separate from version-intrinsic semantics;
- evidence establishes only the exact subject/property its oracle can discriminate;
- stale evidence cannot close current claims;
- Review reconstructs authority independently and must include a bounded Serious Challenge pass and out-of-matrix abstraction-adequacy pass;
- human/stakeholder ratification is orthogonal to technical Review and cannot be manufactured by automation;
- Lossless Representation requires recoverable ownership, lifecycle, constraints, applicability, uncertainty and reopen conditions;
- progressive disclosure and active simplicity prefer one owner, direct routing and removal/consolidation over wrappers or mirrors;
- historical versions/resources remain frozen and version-bound;
- Protocol 7 D3/D4 remains isolated from this cycle.

The accepted parent authority is not contradictory, materially ambiguous, mutually incompatible, inadequate, or unrealizable. Therefore **SERIOUS CHALLENGE: NONE**.

## 3. Blocking findings

### B65-P3-1 — candidate-subject ambiguity survives in Review and ratification evidence binding

**finding ->** P3's shared evidence binder treats every top-level `candidate_ref`, `semantic_ref`, or `pN` value as an interchangeable candidate binding and accepts the current `candidate.semantic_ref` if it appears anywhere in that set. This is weaker than binding the evidence disposition to one unambiguous reviewed/ratified subject.

**exact owner ->** D4 release-state validation in `source/release_state.py`, specifically `_bound_candidate_refs` as consumed by `_check_review_evidence` and `_check_ratification_evidence`.

**violated invariant ->** exact-candidate evidence applicability; P65-3 evidence-claim congruence; Review/ratification state-semantic separation; the accepted requirement that PASS/NO-PASS and RATIFIED/REJECTED evidence apply to the exact current `candidate.semantic_ref`.

**counterexample/evidence ->** the P3 implementation computes a set of all candidate-like front-matter values and checks only set membership. Fresh counterexamples against that exact logic produced **no validation error** for each of:

```yaml
status: pass
candidate_ref: cccccccccccccccccccccccccccccccccccccccc
p3: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

when the state candidate is `aaaaaaaa...`;

```yaml
status: pass
semantic_ref: cccccccccccccccccccccccccccccccccccccccc
p3: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

when the state candidate is `aaaaaaaa...`; and

```yaml
status: pass
p3: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
p4: cccccccccccccccccccccccccccccccccccccccc
```

when validating P3, even though the same record can naturally designate P4 as the reviewed subject. The analogous `status: ratified` conflict is also accepted.

This is not hypothetical version mismatch protection: P3 and a replacement P4 are both Protocol 6.5 candidates, so `_check_version_ref` does not distinguish them.

The existing focused tests cover one correct candidate field or a wholly wrong candidate field, but not contradictory/multi-candidate metadata. The repository's P1 historical Review also demonstrates why generic `pN` fields are contextual metadata rather than intrinsically unique subject fields: it contains both `p0` control and `p1` subject fields.

**consequence ->** a structurally valid Review or stakeholder-ratification record can be attributed to a candidate merely mentioned in metadata rather than the record's actual subject. That can make the sole lifecycle owner accept wrong-subject PASS/NO-PASS or RATIFIED/REJECTED evidence while all ordinary route, commit, path, disposition and version checks remain green.

**smallest owning-layer repair ->** alter the existing evidence-binding helper; do not add a registry, mirror, semantic parser or compatibility subsystem. Resolve exactly one machine-readable evidence subject. Explicit `candidate_ref` / `semantic_ref`, when present, must be mutually consistent and must equal the state semantic ref. Legacy `pN` support must have a bounded rule that yields exactly one subject; ambiguous multiple non-baseline `pN` fields without an explicit unique subject must reject rather than become a set-membership success. Historical comparator/control fields remain contextual metadata, not alternate subjects. Keep arbitrary prose outside machine semantic judgment.

**affected qualification to rerun ->** focused Review and ratification binding tests; fresh conflicting-field and multi-`pN` negatives; future-P4 positive/negative fixtures; legal lifecycle transitions; full repository build/regression; Orchestrator Core; exact-new-candidate CI; fresh binding descendant qualification; Phase-VII evidence-applicability/mutation pass; fresh independent Review. P3's CI remains valid for the properties it actually discriminated but cannot establish closure of this ambiguity.

### B65-P3-2 — predecessor-scoped current doctrine remains in the canonical evidence owner

**finding ->** current Protocol 6.5 canonical evidence doctrine still states:

```text
Protocol 6.4 remains document-controlled: these are reasoning obligations,
not a required universal machine graph/database.
```

inside the current impact-closure rule.

**exact owner ->** current canonical `source/shared/references/evidence-evolution-and-dependencies.md`; the generated software-design package faithfully carries the same line.

**violated invariant ->** P65-6 Integrated Current Representation; Lossless Representation/current representation convergence; the accepted Phase-IV/V requirement that the existing 6.4-labelled additions in this exact owner be integrated as current doctrine rather than retained as predecessor-scoped current text.

**counterexample/evidence ->** a bounded scan of current canonical shared doctrine found this as the residual explicit `Protocol 6.4` predecessor label. It is not historical/archive text and is not a version-intrinsic frozen resource. Because source/generated parity reproduces the line exactly, all parity/build checks can remain green while the current 6.5 owner still scopes a decision-relevant architecture statement to its predecessor.

**consequence ->** the current evidence owner is not fully self-applied/converged: a reader can recover the impact-closure obligations but not unambiguously recover that the document-controlled/no-universal-graph consequence is current Protocol 6.5 doctrine. Generated parity propagates rather than detects the semantic defect.

**smallest owning-layer repair ->** alter that current owner directly to protocol-current/generic wording while preserving the existing meaning; perform a bounded sibling scan for predecessor-qualified normative scope. Do not add a new section, wrapper, version table or compatibility layer. Regenerate only affected descendants from canonical source.

**affected qualification to rerun ->** source/generated/package parity; relevant representation/current-label checks; hot-current measurement; preservation-map applicability for P65-6/QF64-P/F64-K; full repository/Orchestrator acceptance on the new candidate; fresh semantic paraphrase/inversion Review. Frozen 5.16-6.4 resources remain unaffected.

## 4. Mandatory P3 repair falsification

### B65-P2-1 — lifecycle-value duplication

**Closed for the P3 repaired test family.**

Fresh transition checks admit:

1. legal 6.4 -> 6.5 accepted-current transition with immutable 6.4 bootstrap/recovery moved to `historical["6.4.0"]`;
2. a next 6.6 candidate initialized as `UNFROZEN / NOT_RUN / NOT_REQUESTED / UNAVAILABLE`.

The broader census covered current role/specialist entrypoints, canonical shared doctrine, relevant inherited tests and active operational workplans. Remaining matches classify as:

- immutable historical/version-intrinsic identities, e.g. Protocol 6.3/6.4 bootstrap/recovery tests;
- synthetic transition fixtures, including the 6.5/6.6 future-state fixture;
- frozen qualification/handoff facts;
- Protocol 7's deliberately pinned pre-cutover 6.4 recovery dependency, whose own authority explicitly says it changes only through a separate inheritance reconciliation.

No current executable invariant was found that must be edited merely because the release-state owner legally advances.

### B65-P2-2 — terminal ratification binding

**Not closed.** Route existence, repository identity, commit/path existence, path safety, disposition matching, malformed front matter and simple exact-candidate tests work as intended, and arbitrary stakeholder prose remains outside machine semantic judgment. However B65-P3-1 is a surviving false-accept in the exact-candidate binding itself.

### B65-R1 — Review evidence binding

**Not closed** for the same shared-owner ambiguity in B65-P3-1.

### B65-R2 — lifecycle-phase duplication

**Closed.** No sibling live Review/ratification/publication/recovery phase mirror survived the bounded current test/current-operation census. Snapshot facts and transition fixtures were not misclassified as owners.

### B65-R3 — predecessor-version gating

**Original workflow-gating blocker closed.** Current workflow prompts no longer condition exact-contract, Review, Verification, Stabilization, audit or closeout duties on Protocol 6.4. The broader current-source pass found no sibling predecessor gate. B65-P3-2 is a different but related P65-6 representation defect: a predecessor-scoped current statement in the evidence owner rather than a conditional workflow gate.

## 5. Four defect-family re-falsification

| Family | P3 result | Review assessment |
| --- | --- | --- |
| DF-1 release-state/version lifecycle ownership | materially improved, but NO-PASS | one mutable state owner and legal transitions work; exact evidence applicability is still unsound through B65-P3-1 |
| DF-2 qualification/Review epistemology | NO-PASS | P3 correctly rejects many malformed/wrong routes, but its oracle can remain green for contradictory candidate metadata |
| DF-3 meta-control/governance | NO-PASS as realized | Serious Challenge and human-ratification ownership are coherent, but wrong-subject terminal evidence can still drive governance state |
| DF-4 representation/schema/convergence self-application | NO-PASS | B65-P3-2 leaves predecessor-scoped text in a mandatory current owner |

## 6. Local-compliance / global-failure trajectories

1. **Evidence trajectory:** immutable route exists -> repository/path safe -> front matter parses -> status matches -> current SHA appears in one historical `p3` field -> every local evidence check passes -> record's explicit/newer candidate subject is different -> exact-candidate applicability fails globally.
2. **Generated-representation trajectory:** canonical source contains predecessor-scoped current doctrine -> generated packages reproduce it byte-for-byte -> package parity and Core selection pass -> current representation convergence remains false.
3. **Lifecycle trajectory:** state schema, Review ordering, ratification ordering, publication ordering and recovery ordering can all be locally legal -> ambiguous evidence subject can still attach a terminal disposition to the wrong 6.5 candidate.
4. **PEM/authority trajectory:** PEM remains non-authoritative and release state remains singular -> a wrong-subject evidence assessment can nevertheless contaminate lifecycle state unless applicability is exact.
5. **Compatibility trajectory:** all frozen predecessor bytes remain identical -> successor current doctrine can still be semantically incomplete; frozen-byte preservation is necessary but not sufficient.

These failures require no Serious Challenge because the parent abstractions prohibit them already.

## 7. Out-of-matrix abstraction-adequacy pass

The fresh out-of-matrix search deliberately ignored B65-R1..R3 and B65-P2-1..2 as an exhaustive defect matrix.

It found both surviving classes above:

- **ambiguous multi-field evidence subject**, not represented by the author's simple correct-vs-wrong candidate fixtures;
- **predecessor-scoped current evidence doctrine**, outside the repaired workflow-prompt gate.

Therefore the author matrix and green qualification were not sufficient proof of global closure.

## 8. Qualification-method challenge

For each major positive claim this Review asked whether the oracle could stay green while the claimed real property is broken.

- **release-state transition tests:** discriminate ordering/state legality, but not unique evidence-subject identity unless contradictory metadata is exercised;
- **exact-candidate evidence tests:** current simple positive/wrong-candidate cases are insufficient; B65-P3-1 remains green;
- **source/generated parity:** proves parity, not semantic correctness; B65-P3-2 is copied faithfully;
- **frozen-resource parity:** proves predecessor-byte preservation, not successor semantic adequacy;
- **hot-context/SHA-copy counts:** are useful complexity/duplication sensors, not semantic closure;
- **CI success:** establishes the listed executable checks only; it does not establish independent semantic Review;
- **semantic mutation evidence:** arbitrary prose inversions remain a Review obligation; exact strings must not become a surrogate prose theorem prover.

No positive claim is rejected merely because its oracle is partial; the disposition changes only where a required claim exceeds what the available oracle discriminates.

## 9. Fresh post-P3 mutation/counterexample set

### Machine/state/schema/generated mutants -> executable oracles

Fresh cases included:

- legal 6.4 -> 6.5 cutover: accepted;
- legal next 6.6 initial candidate: accepted;
- valid exact Review PASS/NO-PASS binding: accepted;
- valid exact RATIFIED/REJECTED binding: accepted;
- wrong candidate: rejected when it is the only candidate binding;
- disposition mismatch: rejected;
- wrong repository: rejected;
- absolute path: rejected;
- parent traversal: rejected;
- nonexistent commit/path: rejected;
- malformed/missing front matter: rejected;
- sole future `p4` binding: accepted;
- **conflicting explicit subject + matching historical `p3`: incorrectly accepted**;
- **`p3` + `p4` multi-candidate Review checked as P3: incorrectly accepted**;
- generated/source divergence remains covered by existing parity oracles.

### Prose semantic mutants -> independent semantic Review

Meaning-preserving paraphrases remain admissible when they preserve the same governed semantic set. A paraphrase such as “an oracle warrants no property it cannot distinguish” remains equivalent to the evidence-claim congruence rule and should not fail merely for wording.

Semantic inversions such as “green CI establishes arbitrary prose correctness,” “PEM history may mint authority,” or “stakeholder ratification can be inferred from Review PASS” remain Review failures even if regenerated packages are perfectly in parity.

B65-P3-2 is a concrete semantic-scope mutant that demonstrates why parity cannot replace Review.

## 10. P65-1..P65-6 causal ablation

| Principle | Causal ablation result | P3 realization |
| --- | --- | --- |
| P65-1 self-application | removing it permits SSDP qualification/release machinery to escape its own owner/evidence rules | materially realized |
| P65-2 state/semantics separation | removing it recreates stale current refs/phase mirrors after cutover | realized for the repaired lifecycle-copy family |
| P65-3 evidence-claim congruence | removing it permits wrong subject/property claims from structurally green evidence | **not fully realized: B65-P3-1** |
| P65-4 Review abstraction adequacy | removing it would stop at known repair fixtures and miss both P3 blockers | realized as doctrine; this Review demonstrates its necessity |
| P65-5 minimal meta-governance | removing it encourages duplicate registries/parsers/owners | realized: P3 uses the existing state/evidence owner and no new semantic registry |
| P65-6 integrated current representation | removing it permits predecessor-labelled current doctrine and generated propagation | **not fully realized: B65-P3-2** |

The principles remain justified; the defects are implementation/concretization misses.

## 11. Protocol 6.4 -> 6.5 preservation falsification

The preservation map was treated as evidence, not authority.

Independent checks found no loss of:

- D1-D4 ownership separation;
- formal-definition/axiomatic source-availability, unique-owner, conservativity, parameterization, validity and warrant semantics;
- evidence specification/realization/observation/assessment and stale-evidence semantics;
- Serious Challenge/human adjudication;
- PEM non-authority and conditional activation;
- version-bound compatibility/recovery semantics;
- public-fallback/recovery distinction;
- Protocol 7 isolation.

QF64 proxy machinery was removed as an acceptance oracle, but its protected semantic capabilities remain represented in current owners and fresh semantic Review obligations. That is machinery retirement, not capability loss.

F64 falsification capability remains materially available, including out-of-matrix Review, owner conflicts, evidence/warrant laundering, version/evolution errors, source trust, D1-D4 leakage and current/history separation.

Frozen Protocol 5.16 and 6.0-6.4 orchestrator profile/prompt objects were compared by Git blob identity: all **12/12** are identical between P0 and P3.

The preservation result is therefore **no detected inherited capability loss**, but preservation does not cure the two successor-specific blockers.

## 12. Simplicity and total complexity

Independent measurements reproduce:

| Measure | P0 | P3 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public-fallback SHA copies in that scope | 20 | 0 |
| accepted-6.4 recovery SHA copies in that scope | 12 | 0 |

The hot-current projection is exactly: `README.md`, `AGENTS.md`, `PORTABILITY.md`, `source/README.md`, `source/SEMANTIC_DEPENDENCIES.md`, current workflow prompts and the versioning owner.

This is real structural compression without frozen-resource drift. P3 did not introduce a second release-state registry, lifecycle mirror, prose semantic parser, wrapper stack or candidate-specific P3 branch in the validator.

The required repairs remain small owning-layer alterations. Adding machinery would be contrary to active simplicity.

## 13. Targeted P0/P3 matched comparison

### Lifecycle/current-state drift

P0 carries exact accepted-6.4 fallback/recovery values across the defined hot projection (20 and 12 copies). P3 reduces both to zero and routes mutable state through one release owner. This is a material ownership improvement, but exact evidence subject binding remains defective.

### Proxy/oracle adequacy

P0's accepted 6.4 history included synthetic semantic proxies that could remain green while canonical prose changed. P3 correctly narrows executable claims and routes arbitrary semantic adequacy to Review. The new conflicting-metadata counterexample shows that P3's structural oracle itself still needs one more negative class.

### Authority/Serious-Challenge routing

Both P0 and P3 retain D1-D4 ownership and coherent Serious Challenge routing. P3 clarifies credible-basis/materiality and human ratification without changing the upstream authority model. No Challenge was warranted here.

### Mature-system simplification / Review convergence

P3 materially reduces hot state duplication and keeps the universal kernel flat. It also demonstrates that compression metrics cannot establish convergence: B65-P3-2 survives in the compressed current owner and B65-P3-1 survives in a compact shared helper.

### Holdout not used to design the P3 repair

A holdout trajectory placed a predecessor-scoped current statement in a canonical owner and regenerated all derivatives. Local source/generated parity remains perfect while global current-representation convergence fails. P3 contains exactly this failure shape in the evidence owner, discriminating P65-6 independently of the known P2 repair matrix.

No quantitative frontier-model superiority claim is made. The second contemporary frontier diagnostic remains waived for this cycle.

## 14. Mechanical evidence applicability

Verified workflow runs:

- exact P3 run `36018551068`: completed successfully at head SHA P3; build and Orchestrator Core jobs both passed;
- P3 binding descendant `c3df40cdb144c66a390b5d69b49e6fe8a81ad825`, run `36018970303`: both jobs passed;
- evidence-only descendant `75d73e73d0a6a8bcfc08e9b6f2df1d5488fe7f01`, run `36019184556`: both jobs passed.

Those runs include release-state validation, PEM validation, protocol regression, package build/independent validation/parity, whitespace, packaged 6.5 snapshot parity and Orchestrator Core acceptance.

Applicability is bounded:

- run 36018551068 applies to exact P3 executable/source/package behavior but P3's embedded mutable state still names P2 by self-reference-safe construction;
- run 36018970303 establishes mechanical coherence of the later P3 binding;
- run 36019184556 establishes mechanical coherence of the evidence-only descendant;
- none discriminates the contradictory candidate-metadata counterexample or arbitrary prose adequacy.

## 15. Lifecycle state entering Review

Resolved from the later lifecycle descendant, not from P3 itself:

```text
accepted-current:       Protocol 6.4
candidate:              Protocol 6.5
candidate semantic ref: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
Review:                 NOT_RUN
ratification:            NOT_REQUESTED
public fallback:         UNAVAILABLE
recovery:                UNAVAILABLE
Protocol 7 D3/D4:        unchanged
```

This state was coherent and non-premature.

## 16. Impact and repair gate

P3 is **not** technically eligible for stakeholder ratification.

Required next candidate work is bounded to the two owners above. D3 is not reopened; no Serious Challenge is active.

Any semantic/executable repair creates a new immutable candidate identity. Do not mutate P3 and continue calling it P3.

Evidence becoming stale for a replacement candidate:

- P3-specific Review applicability is terminal NO-PASS history;
- exact-P3 run 36018551068 does not transfer as whole-candidate qualification;
- P3 binding runs 36018970303 / 36019184556 remain historical lifecycle evidence only;
- P3 repair qualification claims closing B65-P2-2/B65-R1 are superseded by this counterexample;
- P65-6/current-representation closure evidence must be refreshed after the canonical evidence-owner edit;
- hot-current counts must be remeasured after the representation edit;
- source/generated/package/Core qualification must rerun after regeneration.

Evidence potentially reusable after explicit applicability check:

- unchanged D1/D2/formal-definition semantics;
- P0 baseline;
- frozen 5.16-6.4 blob-identity comparison;
- B65-P2-1/B65-R2 lifecycle-copy census logic, provided the new candidate does not alter those surfaces;
- Protocol 7 isolation, provided no Protocol 7 artifact changes.

## 17. Authorized next action

Reopen the existing Protocol 6.5 workplan at D4/current representation only.

Do not perform stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR #33 merge, or Protocol 7 D3/D4 mutation.

After the two owning-layer repairs, require:

1. focused conflicting-subject evidence tests plus prior route/disposition negatives;
2. bounded predecessor-scope/current-representation census;
3. regeneration of affected descendants;
4. complete affected repository and Orchestrator acceptance;
5. new immutable candidate identity;
6. later descendant binding with Review reset to NOT_RUN;
7. fresh post-freeze mutation/ablation/matched comparison evidence as affected;
8. fresh independent assembled-candidate Review.
