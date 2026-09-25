---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: fb347272c70b6225743fdc99e9bec8b4197aad49
semantic_ref: fb347272c70b6225743fdc99e9bec8b4197aad49
p9: fb347272c70b6225743fdc99e9bec8b4197aad49
lifecycle_evidence_head: 0834ebd15832ea7d4003268818f92901c28c9b97
binding_descendant: 69f7cda3bd9bdfdbc113b4ec5ac6da044a7d46ab
exact_candidate_ci: 36091484812
binding_ci: 36091605214
final_evidence_ci: 36091819166
date: 2026-09-24
serious_challenge: none
d3_reopened: false
blocking_finding: B65-P9-1
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P9

## 1. Disposition

NO-PASS.

Immutable Review target:

P9 = fb347272c70b6225743fdc99e9bec8b4197aad49

Accepted Protocol 6.4 control:

P0 = 55c085261eb827e3047637d045a8e6917ea6b962

P9 is not technically eligible for stakeholder ratification.

P9 remains immutable. Any semantic repair creates a new candidate identity and requires affected exact-candidate qualification, freeze/binding, and a fresh independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR #33 merge, or Protocol 7 D3/D4 mutation is authorized by this Review.

One genuine blocking defect survives:

B65-P9-1 — governed release-state owner deletion is conflated with genuine pre-owner ancestry in production predecessor resolution.

The accepted Protocol 6.5 D3 design remains coherent and is not reopened.

## 2. Independence and authority reconstruction

This Review reconstructed applicable authority from accepted P0, the accepted Protocol 6.5 Phase IV-V D3 design, the active D3-to-D4 handoff/workplan, exact P9 source, current lifecycle descendants, and independently inspected evidence before using repair-side closure claims.

The governing architecture requires:

- D1-D4 remain the only semantic authority domains;
- root PROTOCOL-RELEASE-STATE.yaml is the sole mutable release-state owner;
- mutable release state is separate from immutable version semantics;
- current release transitions preserve project/schema identity, accepted-current identity, immutable history, candidate identity, Review/ratification evidence applicability, public fallback, recovery, and cutover order;
- Review PASS is technical eligibility only;
- stakeholder ratification remains an explicit human decision;
- public fallback is the exact reviewed/ratified candidate;
- recovery is distinct, later, and lineage-complete;
- historical mappings remain immutable once superseded absent an explicitly authorized correction;
- generated views remain subordinate to canonical owners;
- frozen historical profile/prompt identities remain immutable;
- Protocol 7 D3/D4 remains isolated;
- qualification evidence supports only the exact property and subject discriminated by its oracle;
- substantial independent Review includes out-of-matrix abstraction-adequacy falsification;
- active simplicity requires strengthening the existing owner rather than adding mirrors, registries, compatibility layers, or candidate-specific branches.

No parent authority requires a second release-state registry or a new topology control plane.

## 3. Project Engineering Memory and Historical Applicability Set

The accepted/base PEM identity is P0 = 55c085261eb827e3047637d045a8e6917ea6b962. The current branch PEM is a candidate overlay and is not self-accepting authority.

Bounded Historical Applicability Set:

| PEM item | Applicability | Use in this Review |
| --- | --- | --- |
| SP-002 self-reference-safe descendant publication | applicable | evidence-backed hypothesis for immutable candidate -> descendant publication -> distinct recovery |
| FF-001 premature immutable bootstrap publication | applicable | hypothesis for publication/recovery ordering and stale immutable identity risk |
| DS-001 semantic proxy qualification can overclaim | directly applicable | hypothesis that authored topology tests can stay green while the real owner remains semantically incomplete |
| PC-001 frozen prior-version profile/resource preservation | applicable | preservation hypothesis independently checked against P0/P9 blobs |
| SP-001 canonical router repair/regeneration | not materially applicable to surviving blocker | unrelated mechanism family |

PEM was treated as hypothesis input and historical evidence only. Current authority and exact P9 behavior determine disposition.

## 4. Exact candidate and lifecycle boundary

Independent repository inspection established:

- branch: ssdp-6.5-frontier-model-re-evaluation;
- immutable semantic candidate P9: fb347272c70b6225743fdc99e9bec8b4197aad49;
- exact P9 source/PROTOCOL_VERSION: 6.5.0;
- P9 binding descendant: 69f7cda3bd9bdfdbc113b4ec5ac6da044a7d46ab;
- lifecycle/evidence head entering Review: 0834ebd15832ea7d4003268818f92901c28c9b97;
- exact-P9 workflow 36091484812: completed success, build + orchestrator-core success;
- binding workflow 36091605214: completed success, build + orchestrator-core success;
- final lifecycle workflow 36091819166: completed success, build + orchestrator-core success.

Entering release state at 0834ebd15832ea7d4003268818f92901c28c9b97 is:

- accepted-current: 6.4.0;
- candidate: 6.5.0;
- semantic ref: exact P9;
- Review: NOT_RUN;
- stakeholder ratification: NOT_REQUESTED;
- public fallback: UNAVAILABLE;
- recovery: UNAVAILABLE.

The three workflows are valid structural/executable evidence for their discriminated properties. They are not semantic Review PASS.

## 5. Serious Challenge

No Serious Challenge.

The accepted D3 architecture explicitly requires one governed release-state owner, evidence-claim congruence, real-owner validation, independent out-of-matrix Review, immutable history, and legal release transitions. The surviving problem is a D4 under-concretization in production ancestry classification.

The defect is locally repairable without changing P65-1 through P65-6 or reopening accepted D3.

## 6. Mandatory P8-repair falsification — B65-P8-1

### 6.1 Production resolver and call path

Exact P9 production behavior is owned by source/release_state.py.

main() validates the current snapshot, then calls the production predecessor resolver _previous_governed_release_states(), then calls validate_release_transition(previous, current) for every returned material predecessor.

For committed current state, the resolver:

1. starts from HEAD;
2. inspects direct Git parent topology using rev-list --parents;
3. walks through parent commits whose parsed release-state snapshot equals current;
4. records the first differing release-state state on each traversed lineage;
5. deduplicates equivalent predecessor states;
6. validates current against every returned distinct predecessor.

This removes P8's dependence on ordinary path-log ordering for parents that contain the owner.

The material weakness is a separate branch in the same production resolver:

- a parent for which PROTOCOL-RELEASE-STATE.yaml cannot be read is returned as None;
- every such parent is unconditionally skipped with the assumption that it predates introduction of the owner.

The implementation does not prove that absence is genuinely pre-owner.

### 6.2 Required topology falsification matrix

| Required case | Result | Independent assessment |
| --- | --- | --- |
| Working-tree change versus HEAD | PASS | current differing from committed HEAD returns committed HEAD state directly |
| Linear committed transition | PASS | first differing direct ancestry state is recovered |
| Evidence-only descendants | PASS | equal current states are traversed until the first material boundary |
| Consecutive state transitions | PASS | when immediate parent state differs from current, that immediate predecessor is selected; an older transition is not substituted |
| Date-reordered merge parents | PASS | direct parent traversal does not use timestamps/path-log ordering |
| Divergent merge-parent states | PASS when both parents contain the owner | every materially distinct returned parent boundary is validated, including an unfavorable parent |
| Equivalent merge-parent states | PASS | equivalent predecessor states are deduplicated without losing transition semantics |
| Synthetic PR merge | PASS for a genuinely pre-owner base parent | authored test correctly ignores a base lineage that never had the owner and validates the feature lineage |
| Pre-owner ancestry | NO-PASS distinction | missing owner is assumed pre-owner without proving the lineage genuinely predates owner introduction |
| Long unchanged ancestry | PASS for owner-present ancestry | equal states are traversed until the first differing state |
| Ordering independence | PASS for owner-present parent set; NO-PASS for missing-state classification | timestamps, branch names, stack/sibling order do not choose among present states, but a missing parent is dropped before semantic classification |
| Recovery lineage | PASS at the local recovery predicate | stale/non-descendant/wrong-ancestry recovery and incomplete recovery snapshot are rejected; publication must descend from recovery |

### 6.3 Fresh topology holdout not used to design P9

A fresh temporary Git repository exercised the exact P9 resolver algorithm with this history:

1. commit A introduces PROTOCOL-RELEASE-STATE.yaml with governed state A;
2. good branch changes state A -> B;
3. sibling branch forks from A and deletes PROTOCOL-RELEASE-STATE.yaml;
4. a synthetic merge has parents [good-B, deleted-owner] and restores the B tree.

Observed production-resolver behavior:

- deleted_parent_has_state = false
- resolver_errors = []
- predecessor_count = 1
- predecessor_candidate_refs = [A]
- the deleted-owner lineage is ignored

The resolver traverses the good B parent, finds A as the material predecessor, and validates A -> B. The sibling lineage that deleted the sole governed owner disappears from the semantic transaction because its missing file is treated exactly like a genuinely pre-owner parent.

This is not a timestamp or enumeration-order defect. It is a false equivalence between two materially different histories:

- lineage genuinely predates introduction of the owner;
- lineage was already governed and later deleted the owner.

### 6.4 Mandatory qualification-method answer

Could every authored P9 test and normal CI job remain green while the real production predecessor resolver still validates the wrong temporal transaction?

Yes.

All exact-P9 authored topology tests and normal CI can remain green because the test matrix includes a genuinely pre-owner missing parent but does not include a parent that deletes the owner after owner introduction. The same production branch handles both cases and silently skips both. Therefore green authored tests establish only the covered topologies; they do not discriminate the fresh deletion/reintroduction topology.

This is a real-owner oracle gap, not a test-count concern.

## 7. B65-P9-1 — governed-owner deletion conflated with pre-owner ancestry

### Finding

P9 cannot distinguish a missing release-state file caused by genuine pre-owner ancestry from a missing release-state file caused by deletion after that lineage became governed.

A lineage can therefore:

- contain a valid governed release state;
- delete the sole current state owner;
- accumulate arbitrary commits without the owner;
- later merge into a branch that restores a valid current state;

and production predecessor resolution can ignore that entire malformed governed interval.

### Earliest owner

D4 source/release_state.py, specifically production ancestry/predecessor classification in _previous_governed_release_states() and the helper contract used to classify missing owner state.

No D3 mutation is required.

### Violated invariants

- sole mutable release-state ownership;
- state/semantics separation as an actually governed lifecycle;
- release transition continuity;
- self-application;
- evidence-claim congruence;
- current-vs-history integrity;
- out-of-matrix qualification adequacy;
- preservation of governed history;
- Lossless Representation of the release transaction.

### Consequence

A locally coherent current root state and completely green normal qualification can coexist with a Git parent lineage that abandoned the only governed release-state owner after governance began.

The current release-state validator can therefore validate an incomplete temporal transaction.

This is release/governance integrity, not cosmetic history.

### Smallest owning-layer repair

Alter the existing release-state resolver only. Do not add a second state file, owner registry, transition database, compatibility subsystem, branch-name policy, timestamp policy, candidate-specific exception, or semantic prose parser.

Required behavior:

1. Represent parent-path absence distinctly from a valid parsed release-state snapshot.
2. When a traversed parent lacks PROTOCOL-RELEASE-STATE.yaml, determine from that parent's ancestry whether the lineage is genuinely pre-owner.
3. A lineage with no governed ancestor may be treated as pre-owner and ignored.
4. A lineage with any governed ancestor must not be treated as pre-owner merely because the current parent lacks the file; owner deletion/reintroduction is a malformed governed transition and must fail validation.
5. The result must remain independent of timestamps, default git log ordering, branch names, latest/default refs, sibling enumeration, and traversal-stack order.
6. Preserve existing behavior for equivalent parent states, evidence-only descendants, working-tree transitions, and genuine pre-owner synthetic PR merges.
7. Keep transition/history/recovery predicates in the existing owner. Do not duplicate them in tests or a new topology authority.

Required fresh repair tests include at least:

- owner introduced -> sibling deletes owner -> merge restores owner: reject;
- same topology with reversed merge-parent order: reject;
- same topology with date ordering reversed: reject;
- owner deleted for multiple commits before merge: reject;
- owner deleted then reintroduced on that same lineage before merge: validate the actual material deletion/reintroduction policy explicitly rather than silently classifying it pre-owner;
- genuine pre-owner base parent + governed feature lineage: continue to pass;
- long genuine pre-owner ancestry: continue to pass;
- all P9 owner-present topology controls: continue to pass.

Any repair creates a new immutable candidate identity.

## 8. Earlier blocker-family re-falsification

| Blocker family | P9 result | Review |
| --- | --- | --- |
| B65-P7-1 transition continuity and recovery lineage | core predicates repaired; assembled closure blocked by B65-P9-1 | validate_release_transition preserves history/cutover identity and _check_recovery_lineage enforces descendant/exact-state publication; malformed missing-owner lineage can bypass transition selection |
| B65-P6-1 strict root-state parser convergence | PASS | unique-key loader owns root parsing; evidence front matter uses the same duplicate-rejecting mapping semantics |
| B65-P6-2 canonical semantic-version identity/history ordering | PASS | canonical ASCII x.y.z regex + numeric tuple ordering; leading-zero/Unicode/future-history mutations reject |
| B65-P5-1 duplicate-key root ambiguity | PASS | recursive duplicate mapping keys reject before semantic validation |
| B65-P5-2 candidate succession/history collision | PASS | historical/equal/older active candidates reject; generic patch/minor/major successors remain legal |
| B65-P4-1 evidence-front-matter duplicate/subject ambiguity | PASS structurally | duplicate/conflicting/malformed explicit subject fields reject before fallback |
| B65-P3-1 exact Review/ratification subject binding | PASS structurally | candidate_ref/semantic_ref exact identity and disposition are resolved from immutable evidence route |
| B65-P3-2 current representation convergence | PASS on inspected current representation | current canonical/generated prompt blob identity holds; no operational predecessor gate found |
| B65-P2-1 / B65-R2 duplicated mutable lifecycle state | PASS on bounded current census | mutable accepted 6.4 public/recovery refs have zero copies in inspected hot-current projection outside the root owner |
| B65-P2-2 / B65-R1 immutable Review/ratification applicability | PASS structurally | exact project/commit/path, subject, disposition and ancestry checks remain active |
| B65-R3 predecessor-version gating | PASS | 34 current shared references contain no operational Protocol-6.4/predecessor gate |

Structural PASS does not convert semantic prose or stakeholder authorization into machine proof.

## 9. Recovery-lineage re-falsification

The production recovery predicate was independently inspected rather than accepted from test names.

It requires:

- semantic candidate is an ancestor of recovery;
- Review evidence publication descends from candidate and precedes recovery;
- ratification evidence descends from Review and precedes recovery;
- recovery is an ancestor of current publication state;
- recovery snapshot contains the exact candidate version/ref;
- exact Review PASS evidence;
- exact RATIFIED evidence;
- exact public fallback;
- recovery still UNAVAILABLE inside the recovery target before later mapping publication.

Consequences:

- stale recovery rejects;
- sibling/non-descendant recovery rejects;
- correct-version but wrong-ancestry recovery rejects;
- recovery target missing exact PASS/RATIFIED/public state rejects;
- mapping publication not descending from recovery rejects;
- a complete later recovery target followed by legal descendant mapping is admitted.

P9 tests additionally include the real stale P6-as-P7 recovery negative and positive/incomplete recovery-snapshot controls.

The surviving blocker is predecessor-set completeness, not the recovery predicate itself.

## 10. DF-1 through DF-4

| Defect family | Result | Basis |
| --- | --- | --- |
| DF-1 release-state/version lifecycle ownership | NO-PASS | sole owner exists, but one governed parent lineage can lose that owner and be silently excluded from transition validation |
| DF-2 qualification/Review epistemology | NO-PASS dependency | exact-P9 CI is correctly bounded mechanically, but authored topology oracle omits a production-realizable malformed governed ancestry class |
| DF-3 meta-control/governance | PASS | Review, ratification, PEM, Challenge, publication and recovery remain separate authority/evidence roles; no self-ratification found |
| DF-4 representation/schema/convergence self-application | NO-PASS through DF-1 | representation convergence is strong, but SSDP's own sole release-state owner is not protected against post-introduction disappearance on a parent lineage |

## 11. Local-compliance / global-failure trajectories

### Trajectory A — fresh owner-deletion holdout

Local conditions:

- current root state is coherent;
- exact current candidate/version can be valid;
- good merge-parent transition is legal;
- normal CI and all authored P9 topology tests can pass.

Global failure:

- sibling parent lineage previously contained the governed owner and then deleted it;
- production resolver drops that parent as if governance never existed;
- transition validation never sees the malformed governed interval.

This survives and is blocking.

### Trajectory B — divergent parent states with both owners present

One parent transition passes; another parent exposes historical deletion.

P9 returns both materially distinct predecessor states and validates both. The unfavorable transition fails.

This does not survive; P9 correctly repaired P8's favorable-parent selection defect for owner-present parents.

### Trajectory C — genuine pre-owner base plus governed feature lineage

Base parent genuinely predates introduction of the owner; feature lineage introduces the owner and transitions.

P9 ignores the genuinely pre-owner base and validates the governed feature boundary.

This does not survive and is the intended behavior that must be preserved by repair.

## 12. Out-of-matrix abstraction-adequacy pass

A fresh sibling defect class survives outside the authored repair matrix:

post-introduction owner absence masquerading as pre-owner ancestry.

The authored matrix tested:

- owner-present linear/merge ancestry;
- evidence-only ancestry;
- equivalent/divergent parents;
- timestamp reordering;
- a genuinely pre-owner missing parent.

It did not challenge whether the missing-parent classification itself proves pre-owner status.

No second material fresh blocker family survived proportionate inspection.

No Serious Challenge follows because D3 already requires the distinction between governed current state and genuine historical pre-owner absence.

## 13. Qualification-method challenge

| Claimed property | Could current oracle stay green while property is false? | Assessment |
| --- | --- | --- |
| exact current snapshot schema | no material bypass found | supported |
| duplicate-key rejection | no for owner parser path | supported |
| canonical version identity/order | no for represented states | supported |
| Review/ratification exact subject/disposition | no structurally | supported |
| semantic adequacy of evidence prose | yes | correctly remains independent Review work |
| actual stakeholder authorization | yes | correctly remains human authority |
| transition history for owner-present ancestry | no material ordering bypass found | supported |
| distinction: genuine pre-owner vs owner deleted after introduction | YES | blocker B65-P9-1 |
| recovery ancestry/exact pre-mapping state | no material local bypass found | supported |
| source/generated prompt parity | exact blob identity discriminates | supported |
| frozen historical resources | exact blob identity discriminates | supported |
| compression/simplicity | counts can remain good while lifecycle is wrong | descriptive only, never correctness proof |

## 14. Fresh mutation/counterexample set

### Machine/state/topology mutants

- working-tree current state differs from HEAD -> HEAD is predecessor: rejected/validated correctly;
- long same-state ancestry -> first differing boundary found;
- consecutive A -> B -> C -> immediate B used for C;
- two divergent owner-present parents -> both distinct predecessor states validated;
- equivalent parents -> deduplicated without dropping semantic transition;
- reversed timestamps -> no semantic change;
- genuine pre-owner parent -> ignored correctly;
- owner introduced -> sibling deletes owner -> merge restores owner -> BLOCKER, deleted lineage ignored;
- duplicate root mapping key -> reject;
- leading-zero/Unicode semver -> reject;
- future historical version under older accepted-current -> reject;
- active candidate colliding with history -> reject;
- stale/sibling/wrong-ancestry recovery -> reject;
- recovery target with incomplete PASS/RATIFIED/public snapshot -> reject.

### Prose-semantic mutants

Independent Review continues to reject:

- CI or branch position presented as ratification;
- structurally correct Review metadata attached to prose that does not actually review P9;
- predecessor-conditioned current obligations by paraphrase;
- compression that removes a protected P64 semantic capability;
- generated prose diverging semantically from canonical source despite format validity.

Meaning-preserving paraphrases remain legal.

## 15. P65-1 through P65-6 causal ablation

| Principle | Ablation failure | P9 realization |
| --- | --- | --- |
| P65-1 self-application | exempt SSDP release topology from its own owner/continuity rules -> malformed governance history can remain green | causally necessary; incomplete through B65-P9-1 |
| P65-2 state/semantics separation | restore mutable lifecycle copies into immutable source -> stale current truth | realized strongly |
| P65-3 evidence-claim congruence | let authored topology suite claim all topology semantics -> fresh deletion topology survives green | causally necessary; incomplete oracle coverage exposed by Review |
| P65-4 Review abstraction adequacy | restrict Review to authored matrix -> missing-parent classification is never challenged | causally necessary and realized by this fresh holdout |
| P65-5 minimal meta-governance | collapse Review/ratification/Challenge/PEM roles -> inferred acceptance becomes admissible | realized |
| P65-6 integrated current representation | allow lifecycle and generated/current representations to diverge -> fragmented current truth | representation convergence realized; lifecycle topology owner remains incomplete |

No P65 principle should be removed. No new principle is required.

## 16. Protocol 6.4 -> 6.5 preservation

Independent preservation checks support:

- universal kernel words: P0 = 2642; P9 = 2642;
- exact source/generated Protocol 6.5 prompt parity: same blob 3779f69ec5d4a0ca435b4d1f364a3783a5f4f592;
- accepted-6.4 public fallback SHA copies in the inspected hot-current projection: 0;
- accepted-6.4 recovery SHA copies in the inspected hot-current projection: 0;
- P7 -> P9 canonical shared/root/current semantic prose changes: none; P9 repair is bounded to source/release_state.py plus release-state tests and lifecycle/evidence documents, so the previously established defined hot-current projection remains byte-applicable across P7 -> P9;
- frozen Protocol 5.16 and 6.0-6.4 profile/prompt objects: 0 differences out of 12 exact P0/P9 objects;
- current shared-reference predecessor-scope census: all 34 source/shared/references Markdown owners inspected; no operational Protocol-6.4/predecessor gate survives. Three generic compatibility statements mention prior-version/older-version semantics but do not condition current obligations on Protocol 6.4;
- Protocol 7 D3/D4 isolation: six Protocol 7 parent/revision design artifacts are blob-identical P0 -> P9. The shared 6.1-7.0 authority index changed as a mutable routing/lifecycle surface, not as Protocol 7 D3/D4 architecture;
- preserved formal-definition, authority, evidence, PEM non-authority, and version/frozen-resource capabilities remain represented.

The preservation map therefore remains substantially applicable, but whole-candidate preservation closure is blocked by B65-P9-1 because governed release-state continuity is not complete.

## 17. P0 versus P9 matched comparison

### Lifecycle/current-state drift

P9 is materially better than P0:

- one explicit mutable release-state owner;
- mutable exact accepted-6.4 public/recovery values removed from the inspected hot-current projections;
- exact Review/ratification evidence binding;
- canonical version/history ordering;
- transition and recovery lineage validation;
- topology traversal no longer depends on ordinary path-log date ordering.

P9 remains NO-PASS because missing-owner parent ancestry is semantically under-classified.

### Semantic-owner coherence

P9 consolidates release truth into one owner rather than many value copies. The blocker is not duplicate authority; it is that the sole owner can disappear on a previously governed lineage without being recognized as a violation.

### Proxy/oracle adequacy

P9 is stronger than P0/P8 because authored tests exercise the real production resolver in temporary Git repositories.

The remaining proxy gap is precise: the missing-parent test covers genuine pre-owner ancestry but not post-introduction deletion, so the oracle can remain green while a materially different missing-state history is accepted.

### Authority and Serious-Challenge routing

PASS. No authority collapse or D3 contradiction was found.

### Mature-system simplification

P9 preserves the simplified owner architecture and modifies the existing release-state owner rather than adding a subsystem. The next repair should do the same.

### Review/convergence behavior

Repeated candidate replacement is expensive but has continued to remove real owner-level defects rather than justify candidate-specific machinery. This Review found one concrete counterexample and no reason to fabricate another.

### Net machinery/representation complexity

Compared with P0, P9 adds one justified project-level state owner and executable validation while removing duplicated mutable state from semantic/current projections. P9's topology repair increases logic inside that existing owner, but no second registry/mirror/service exists.

The surviving repair can remain a local alteration to ancestry classification.

## 18. Simplicity / total complexity

Current positive properties:

- no second release-state file;
- no transition registry;
- no version registry;
- no semantic prose parser;
- no candidate-specific P1-P9 branch table;
- no branch-name/timestamp authority;
- no public-fallback/recovery collapse;
- no generated artifact promoted to owner;
- no Protocol 7 machinery introduced.

The blocker must not be repaired by adding one of those mechanisms.

A bounded ancestry classification within the existing owner is the minimum change that solves the actual defect.

## 19. Evidence applicability

Applicable to P9 for the properties actually discriminated:

- exact-P9 run 36091484812;
- binding run 36091605214;
- lifecycle-head run 36091819166;
- strict parser/duplicate-key tests;
- canonical semver/history tests;
- exact Review/ratification evidence-subject tests;
- owner-present topology tests;
- recovery-lineage tests;
- frozen prior-profile/prompt identity;
- source/generated current-prompt identity;
- current representation/predecessor census;
- P0/P9 kernel and mutable-value-copy measurements.

Not sufficient or stale for a replacement candidate:

- P9 whole-candidate semantic disposition;
- any claim that B65-P8-1/topology closure is complete;
- P9 exact-candidate workflow as qualification of repaired successor code;
- P9 freeze/binding as identity evidence for a replacement;
- topology test conclusions affected by missing-parent classification;
- whole-candidate preservation closure dependent on correct transition-history resolution.

Later lifecycle descendants remain lifecycle/evidence state only; none replace P9 as this Review's semantic target.

## 20. Required next state

1. Preserve P9 immutably.
2. Publish this P9 NO-PASS Review from a later descendant.
3. Bind current release state to exact P9 with Review NO_PASS and immutable evidence route to this record.
4. Reopen the existing D4 workplan only for B65-P9-1.
5. Keep accepted Protocol 6.5 D3 closed.
6. Repair missing-parent classification inside source/release_state.py.
7. Add the fresh governed-owner-deletion topology negatives plus genuine-pre-owner positive controls.
8. Freeze a new immutable semantic candidate, expected next identity P10.
9. Rerun affected exact-candidate mechanical qualification and full normal CI.
10. Bind the replacement from a later descendant with Review reset to NOT_RUN.
11. Perform another genuinely fresh independent assembled-candidate Review.

## 21. Final disposition

NO-PASS.

P9 is not technically eligible for stakeholder ratification.

Surviving blocker:

B65-P9-1 — production predecessor resolution silently treats any parent lacking PROTOCOL-RELEASE-STATE.yaml as genuinely pre-owner, even when that lineage was already governed and later deleted the sole release-state owner.

Earliest owner: D4 source/release_state.py ancestry classification.

Smallest repair: distinguish genuine pre-owner absence from post-introduction owner deletion using ancestry in the existing resolver; reject malformed governed absence; preserve all current owner-present and genuine-pre-owner behavior.

No D3 Serious Challenge is raised.
