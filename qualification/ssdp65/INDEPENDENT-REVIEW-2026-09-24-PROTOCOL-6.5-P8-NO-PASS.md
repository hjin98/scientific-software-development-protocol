---
kind: independent-review
status: no-pass
protocol_under_review: 6.5.0
candidate_ref: ed782ccad73b43c9052ecc926177c36846b9328d
p8: ed782ccad73b43c9052ecc926177c36846b9328d
accepted_control_p0: 55c085261eb827e3047637d045a8e6917ea6b962
review_start_lifecycle_head: 7c83df20f3989b7d8217405555d5f7c5a1d356fe
exact_candidate_ci: 36067942018
binding_descendant: 65cd5da2d6793733e87d0b97f9ccce23d22b9154
binding_ci: 36068315599
final_evidence_descendant: 7c83df20f3989b7d8217405555d5f7c5a1d356fe
final_evidence_ci: 36068513780
date: 2026-09-24
reviewer: GPT-5.6 Sol
serious_challenge: none
d3_reopened: false
blockers:
  - B65-P8-1
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P8

## 1. Disposition

**NO-PASS.**

Immutable semantic Review target:

P8 = ed782ccad73b43c9052ecc926177c36846b9328d

Accepted Protocol 6.4 control:

P0 = 55c085261eb827e3047637d045a8e6917ea6b962

P8 is not technically eligible for stakeholder ratification.

P8 remains immutable. One genuine D4 blocker survives:

**B65-P8-1 — transition-history resolution can select a sibling/merge-parent release-state snapshot instead of the actual prior governed state, allowing temporal continuity validation against the wrong transaction predecessor.**

No Serious Challenge is raised. Accepted P65 D3 remains coherent and closed. The defect is in the D4 concretization of the existing release-state transaction owner.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized by this Review.

## 2. Independence and authority reconstruction

This Review reconstructed the applicable authority from accepted Protocol 6.4, the assembled P8 source, the accepted P65 D3 design, and current owner semantics before considering P8 repair conclusions.

The governing requirements are:

- D1, D2, D3, and D4 remain the semantic authority domains;
- root PROTOCOL-RELEASE-STATE.yaml is the sole mutable repository release-state owner;
- immutable/version-intrinsic protocol semantics remain separate from mutable release lifecycle state;
- Review evidence binds the exact semantic candidate and Review PASS means technical eligibility only;
- stakeholder ratification is a distinct human acceptance decision for that exact reviewed candidate;
- the public fallback is the exact reviewed and ratified semantic candidate, published only from a later descendant;
- recovery is a distinct later immutable target on the reviewed, ratified, published candidate lineage;
- accepted-current advances only after publication and recovery are complete;
- the immediately previous accepted mapping moves unchanged into historical state;
- already historical mappings are immutable absent an explicitly authorized correction;
- current doctrine is intrinsic rather than predecessor-gated;
- generated representations remain subordinate to canonical source;
- frozen historical resources and recovery identities remain preserved;
- Protocol 7 D3/D4 remains isolated;
- Lossless Representation, evidence applicability, Serious Challenge semantics, progressive disclosure, active simplicity, PEM non-authority, and current representation convergence remain binding.

### PEM / Historical Applicability Set

PEM is material because this is repeated mature self-governance and release-state rework. It was used only as evidence-bounded hypothesis input.

| PEM item | Disposition | Independent use |
| --- | --- | --- |
| FF-001 premature immutable bootstrap publication | APPLICABLE | publication/recovery ordering hypothesis only |
| PC-001 frozen predecessor preservation | APPLICABLE | authority-bound preservation capability |
| SP-002 self-reference-safe descendant publication | APPLICABLE | evidence for later-descendant publication and bootstrap/recovery separation |
| DS-001 proxy qualification overclaim | APPLICABLE | directly relevant to the transition-history oracle challenge |
| SP-001 canonical router repair | NOT_APPLICABLE to the surviving blocker | no router defect is implicated |

No PEM entry supplies normative force by itself.

## 3. Serious Challenge pass

**No Serious Challenge.**

The accepted D3 design is coherent, jointly realizable, and already requires temporal continuity, historical immutability, distinct later recovery, exact evidence lineage, and one release-state owner.

B65-P8-1 is therefore an ordinary D4 blocker: the implementation can be repaired without changing the accepted architecture.

## 4. Exact identity and entering lifecycle state

P8 itself is the semantic Review target. The mutable branch head was not substituted for P8.

Independent Git and workflow inspection established:

- exact P8: ed782ccad73b43c9052ecc926177c36846b9328d;
- P8 normal PR qualification run 36067942018: success;
- P8 binding descendant: 65cd5da2d6793733e87d0b97f9ccce23d22b9154;
- binding run 36068315599: success;
- final pre-Review evidence descendant: 7c83df20f3989b7d8217405555d5f7c5a1d356fe;
- final pre-Review workflow run 36068513780: success.

The later descendant state entering Review is:

- accepted-current: 6.4.0;
- accepted public fallback: e09a9d1480211eea2d16d722182bb5c6de1bee12;
- accepted recovery: 74bc572ef516cae417437a2027eeff52a2e25c15;
- candidate: 6.5.0;
- candidate semantic ref: exact P8;
- Review: NOT_RUN;
- ratification: NOT_REQUESTED;
- candidate public fallback: UNAVAILABLE;
- candidate recovery: UNAVAILABLE.

The green workflows establish only the structural and executable properties their actual oracles discriminate.

## 5. Mandatory P8 repair falsification

### 5.1 Transition and recovery predicates when the correct previous state is supplied

The P8 owner directly implements the following required properties:

1. same accepted version with changed accepted identity rejects;
2. an existing historical mapping cannot be deleted;
3. an existing historical mapping cannot be rewritten;
4. history cannot gain a version without accepted-current advancement;
5. accepted-current advancement requires the previous accepted mapping unchanged in history;
6. accepted-current advancement cannot add unrelated historical entries;
7. accepted-current advancement promotes the immediately previous candidate version;
8. promotion requires previous candidate Review PASS;
9. promotion requires previous candidate RATIFIED state;
10. promotion requires a valid public fallback;
11. promotion requires a valid recovery target;
12. the new accepted public fallback must equal the previous candidate public fallback;
13. the new accepted recovery must equal the previous candidate recovery;
14. recovery must descend from the semantic candidate;
15. Review evidence must descend from the semantic candidate;
16. ratification evidence must follow Review evidence;
17. recovery must follow the Review and ratification lineage;
18. the mapping-publishing state must descend from the recovery target;
19. the recovery target root state must contain the exact candidate version/ref, PASS evidence, RATIFIED evidence, exact public fallback, and recovery still UNAVAILABLE;
20. terminal accepted-current equality remains constrained by complete PASS, RATIFIED, public, recovery, and mapping agreement;
21. semantic-version ordering is numeric and generic across patch, minor, major, and multi-digit versions;
22. no P8-specific, Protocol-6.5-specific, or contiguous-pN transition branch was found;
23. no second release-state registry, transition mirror, phase table, candidate registry, or compatibility subsystem was introduced.

The exact stale-recovery counterexample is rejected: P7 as semantic/public fallback with immutable P6 as the alleged recovery fails ancestry.

These properties close the P7 snapshot-versus-transition gap only if the transition oracle first identifies the correct previous governed state.

### 5.2 Fresh P8 holdout — wrong previous state selected on a merge DAG

P8 resolves the previous governed state with:

    git log -2 --format=%H -- PROTOCOL-RELEASE-STATE.yaml

and then compares the current root state against the first or second path-history commit depending on whether the latest state equals the current state.

That query is not constrained to first-parent history, direct-parent state, a designated integration lineage, or all materially divergent merge parents.

A fresh synthetic Git DAG was constructed:

- S0: common ancestor;
- F1: first-parent governed line adds a protected historical mapping H;
- S1: sibling branch, committed later by date, does not contain H;
- M2: merge/current state, different from both parents, also does not contain H.

For the root state path, ordinary Git history returned:

    M2
    S1
    F1
    S0

while first-parent history returned:

    M2
    F1
    S0

Therefore P8 resolves S1 as the previous state even though F1 is the first-parent governed predecessor.

The exact transition predicate then yields:

- S1 -> M2: PASS;
- F1 -> M2: REJECT because historical H was deleted.

This is a local-compliance/global-failure trajectory: the same current snapshot and same transition validator can pass or fail solely because the history resolver selected a sibling state.

### 5.3 Consequence

A merged or synthetic-checkout state can be validated against the wrong prior transaction.

That can hide:

- deletion or rewrite of an already historical mapping;
- loss or mutation of the accepted-current identity that should be preserved;
- cutover based on a candidate closure state that existed only on a sibling parent;
- other temporal discontinuity that is invalid relative to the governed integration lineage.

The sole state owner therefore does not yet generically establish the temporal transaction it claims to validate.

### 5.4 Transition-history resolution challenge matrix

| Case | Result |
| --- | --- |
| working tree differs from latest committed root state | resolver compares against latest committed path state; acceptable in a linear checkout |
| working tree equals latest committed root state | resolver steps to the prior path commit; acceptable in a linear history |
| multiple evidence-only descendants with unchanged root state | path filtering skips unrelated commits; acceptable on a linear lineage |
| root-state change followed by unrelated commits | path filtering finds the root transition; acceptable on a linear lineage |
| consecutive root-state transitions | direct ordered path history is adequate on a linear lineage |
| current PR checkout against P0, where only candidate parent owns the new root state | observed workflows pass, but this does not discriminate future divergent-parent cases |
| merge with two materially different parent root histories | **FAIL: default path-history ordering can select the sibling parent** |
| candidate branch ancestry versus merge-base | merge-base alone is not the governed prior state; P8 does not explicitly resolve this distinction |
| non-fast-forward or sibling recovery ref | recovery ancestry check rejects |
| correct PROTOCOL_VERSION but wrong recovery ancestry | recovery ancestry check rejects |

The surviving failure is specifically previous-state resolution, not the transition predicate after the pair is known.

## 6. Qualification-method challenge

The central question is:

> Could all P8 tests remain green while a locally valid release-state snapshot still represents a temporal transaction that did not occur?

**Yes.**

The exact P8 test module exercises validate_release_transition directly with author-constructed previous/current dictionaries and exercises recovery lineage with mocked Git calls. It contains no test of _previous_governed_release_state.

Therefore the tests prove that the transition predicate rejects selected bad pairs; they do not prove that production Git-history resolution supplies the correct pair under merge topology.

Runs 36067942018, 36068315599, and 36068513780 are all legitimately green yet do not discriminate the fresh holdout.

The P8 repair qualification claim that the transition baseline is resolved from Git history is stronger than its executable oracle. The claim must be narrowed until the resolver itself is qualified.

## 7. Re-falsification of earlier repaired blocker families

| Family | P8 result | Independent basis |
| --- | --- | --- |
| B65-P6-1 strict root parser | CLOSED | root and evidence front matter use the same duplicate-rejecting loader; P7->P8 introduces no alternate root consumer |
| B65-P6-2 historical ordering/canonical version identity | CLOSED | canonical ASCII semver and numeric tuple ordering remain unchanged; future-history and collision guards remain |
| B65-P5-1 duplicate-key root ambiguity | CLOSED | duplicate mappings reject before semantic binding, recursively |
| B65-P5-2 candidate succession/history collision | CLOSED | lower/equal/historical collision guards and patch/minor/major/multi-digit successor semantics remain generic |
| B65-P4-1 evidence-front-matter ambiguity | CLOSED | strict loader plus explicit-subject precedence and conflict rejection remain |
| B65-P3-1 exact evidence-subject identity | CLOSED | Review and ratification still share one generic subject-binding owner; no known-candidate table |
| B65-P3-2 current canonical source convergence | CLOSED on canonical source | P7->P8 does not mutate shared canonical protocol references; prior exact-P7 census remains applicable to unchanged source |
| B65-P2-1 / B65-R2 lifecycle-value duplication | CLOSED structurally | P8 adds no second mutable release-state authority |
| B65-P2-2 / B65-R1 evidence applicability | CLOSED structurally | exact subject, disposition, route, and lineage binding remain generic |
| B65-R3 predecessor-version gating | CLOSED on canonical source | P7->P8 leaves the relevant canonical current doctrine unchanged |

A fresh structural holdout confirmed ordinary aliases remain usable while duplicate mappings inside anchored structures and unsupported merge-key normalization fail closed rather than silently creating another normalization path.

## 8. Current representation convergence

A separate lifecycle-representation drift was found at Review entry:

- the active successor workplan front matter said status: ready-p8-independent-review;
- the same front matter still said current_phase: PHASE VII P7 FROZEN / FRESH INDEPENDENT REVIEW REQUIRED;
- its top Current disposition still named P7 as the current candidate and fresh P7 Review as the next step;
- its independent_review field still pointed to the P6 Review.

Later sections correctly described P8.

This is a genuine current coordination contradiction, but it belongs to mutable lifecycle/workplan state rather than immutable P8 protocol semantics. This Review output repairs the active workplan foreground while recording the P8 NO-PASS. It is therefore not counted as a second surviving semantic-candidate blocker.

The defect is still material evidence for P65-6: current representations must converge at their foreground/current-state surface, not merely append a newer section at the tail.

## 9. Four defect families

| Defect family | Result |
| --- | --- |
| DF-1 release-state/version lifecycle ownership | **NO-PASS** — B65-P8-1 leaves temporal transaction ownership topology-unsound |
| DF-2 qualification/Review epistemology | PASS with bounded claims — exact subject/disposition binding is sound, but the transition-history closure claim was overstrong |
| DF-3 meta-control semantics/governance | PASS — Review, ratification, Challenge, and PEM authority boundaries remain coherent |
| DF-4 representation/schema/convergence self-application | **NO-PASS through B65-P8-1** — the sole state owner exists but does not yet losslessly validate the transaction under merge topology |

## 10. Local-compliance/global-failure trajectories

### T1 — merge sibling hides historical deletion

F1 contains historical H. S1 does not. M2 omits H.

All local snapshot checks for M2 can be coherent. If S1 is selected as previous, transition validation passes. Relative to governed predecessor F1, the transaction illegally deletes H.

### T2 — sibling closure launders cutover readiness

One parent can contain a fully closed candidate while the actual governed predecessor does not. If the sibling is selected as previous, accepted-current advancement can be judged against closure state that was never present on the governed line.

### T3 — stale recovery

P7 semantic/public fallback plus P6 recovery is rejected by P8 ancestry. This known P7 counterexample is closed.

### T4 — structurally correct but semantically unrelated Review prose

The machine binder can accept structurally correct Review metadata even when prose is unrelated. That remains an intentional oracle boundary: independent semantic Review, not a prose parser, owns semantic adequacy.

## 11. Fresh post-P8 mutation set

### Machine/state/schema/generated mutants

The following were independently classified against the actual P8 owner behavior:

- duplicate top-level or nested root YAML: rejects;
- duplicate Review/ratification front matter: rejects;
- conflicting explicit candidate fields: rejects;
- null/empty/malformed explicit subject: rejects;
- lower/higher pN coexistence: highest numeric generation controls when no explicit subject exists;
- invalid highest-generation pN: rejects rather than falling back lower;
- noncanonical leading-zero or Unicode-digit version identity: rejects;
- historical future-version insertion: rejects;
- candidate resurrection from history: rejects;
- 6.10.0 lexical/numeric trap: numeric tuple semantics are correct;
- accepted-current same-version identity rewrite: rejects;
- historical deletion/rewrite when the correct previous state is supplied: rejects;
- cutover missing or mutating prior accepted mapping when the correct previous state is supplied: rejects;
- stale/sibling recovery: rejects by ancestry;
- recovery with correct version but wrong ancestry: rejects;
- recovery with ancestry but incomplete lifecycle state: rejects;
- recovery mapping published from a non-descendant: rejects;
- source/generated divergence: existing parity oracles remain applicable;
- **merge-history prior-state substitution: admitted by the resolver and is B65-P8-1**.

### Prose semantic mutants

Predecessor-scoped current doctrine, stakeholder-authorization laundering, and semantically unrelated Review prose remain semantic Review questions. No fresh material canonical-prose defect survived independent inspection of the P7->P8 semantic delta.

## 12. P65-1 through P65-6 causal ablation

- **P65-1 self-application:** removing it permits SSDP release machinery to evade the same real-owner evidence standard imposed downstream. B65-P8-1 demonstrates the principle is causally necessary. P8 realizes it incompletely because the production resolver is not itself falsified.
- **P65-2 state/semantics separation:** removing it recreates stale copied release truth. P8 preserves one root mutable owner; principle realized structurally.
- **P65-3 evidence-claim congruence:** removing it permits direct transition tests to stand in for production history resolution. B65-P8-1 is a direct causal example. P8 documents the principle but overstates this repair evidence.
- **P65-4 Review abstraction adequacy:** removing out-of-matrix Review would leave the merge-topology defect invisible behind green authored tests. This Review demonstrates causal value.
- **P65-5 minimal meta-governance:** removal reopens ambiguity in Review, ratification, materiality, and memory-base semantics. P8 introduces no new meta-plane and remains minimal here.
- **P65-6 integrated current representation:** removing it recreates stale foreground workplan state. The stale P7 Current disposition found at Review entry is a direct causal example. The Review descendant reconciles that mutable surface.

All six principles remain justified. The blocker is concretization, not principle inadequacy.

## 13. Protocol 6.4 -> 6.5 preservation

The preservation map remains substantially applicable because P7->P8 changes only the release-state transaction owner, focused tests, and lifecycle/review coordination surfaces.

Independently checked consequences:

- D1-D4 authority separation remains unchanged;
- Protocol 6.4 formal-definition/source-availability/well-definedness/parameter/warrant doctrine is unchanged;
- evidence/evolution and PEM authority boundaries are unchanged;
- QF64 semantic capabilities remain represented by current owners/Review rather than proxy-only semantic fixtures;
- F64 falsification capability remains available through owner-level tests and independent Review;
- public fallback and recovery remain distinct identities;
- frozen prior resources are not mutated by P8;
- Protocol 7 D3/D4 remains untouched;
- current semantic source/generated surfaces are unchanged from P7 across the P8 repair delta.

However, preservation is not lossless at the release transaction boundary until B65-P8-1 is closed: a future merge can lose an accepted historical identity while the wrong pair is validated.

## 14. Simplicity and total complexity

P8 repairs the existing release-state owner directly.

No wrapper, mirror, transition registry, second state file, semantic registry, compatibility subsystem, candidate table, or synchronized phase table was added.

The new Git-history machinery is conceptually justified because temporal continuity requires repository ancestry. The problem is not that history lookup exists; it is that the current lookup is under-specified for non-linear Git topology.

The minimum repair remains inside the same owner. Do not add a new registry to solve B65-P8-1.

## 15. P0/P8 matched comparison and preserved measurements

The prior matched P0/P1 qualitative comparison remains applicable to unchanged owner semantics where P8 does not alter those surfaces:

- lifecycle/current-state ownership is materially consolidated in P8 compared with P0, but P8's temporal resolver still has the topology defect;
- semantic proxy claims are better bounded in P8, but the transition repair qualification again demonstrates why real-owner oracle scope matters;
- Serious Challenge, human ratification, and D1-D4 authority routing are preserved;
- current representation is materially compressed relative to P0.

The preserved measurements are applicable by unchanged-surface analysis rather than a new recount:

- universal kernel: P0 2642; P7 2642; P8 does not change that surface;
- defined hot-current projection: P0 10540; P7 7354; P8 does not change that surface;
- accepted-6.4 public fallback SHA copies in the defined current scope: 20 -> 0; P8 does not reintroduce copies;
- accepted-6.4 recovery SHA copies: 12 -> 0; P8 does not reintroduce copies;
- 12 frozen Protocol 5.16 and 6.0-6.4 profile/prompt objects: P8 does not touch those resources;
- 34-file current canonical shared-reference predecessor census: P8 does not change that shared-reference surface.

These compression figures are not treated as correctness proof. B65-P8-1 prevents a whole-candidate PASS.

## 16. Evidence applicability

Evidence retained as applicable after independent target/oracle/regime/dependency review:

- P8 exact normal CI 36067942018: applicable to the checks that actually ran;
- binding CI 36068315599 and final evidence CI 36068513780: applicable to their exact lifecycle snapshots and repository suites;
- earlier P7 evidence for parser, semver, evidence binder, canonical shared-source convergence, frozen resources, and generated parity: applicable because P8 does not alter those surfaces except the release-state owner delta explicitly re-reviewed here.

Evidence that is stale or insufficient for the surviving claim:

- P8 repair qualification's whole claim that transition-history resolution is closed;
- authored transition tests as proof of production prior-state resolution;
- all three green workflows as proof of merge-topology transaction correctness.

After repair, rerun the transition-history topology matrix, complete release-state suite, full repository build/Core, preservation/current-representation checks, exact replacement-candidate qualification, binding qualification, and a fresh independent assembled-candidate Review.

## 17. Blocking finding

### B65-P8-1 — transition-history resolution is topology-unsound

**Finding**

Production prior-state resolution uses unqualified path-history ordering and can select a sibling merge parent rather than the actual governed predecessor.

**Exact owner**

D4 source/release_state.py, specifically _previous_governed_release_state and its integration with main release-state validation.

**Violated invariants**

- sole release-state ownership;
- temporal transition continuity;
- accepted-current continuity;
- historical immutability;
- compatibility/recovery integrity;
- evidence-claim congruence;
- self-application;
- Lossless Representation of lifecycle state.

**Counterexample/evidence**

Fresh merge-DAG holdout F1/S1/M2:

- F1 contains protected historical H;
- S1 omits H and has a later commit date;
- M2 omits H and changes candidate state;
- ordinary path history orders M2, S1, F1;
- S1 -> M2 transition passes;
- F1 -> M2 transition rejects historical deletion.

P8 has no executable test of _previous_governed_release_state, so all authored tests and CI can remain green.

**Consequence**

A locally coherent current release-state snapshot can be accepted as a legal temporal transaction even though the actual governed lineage lost immutable lifecycle state.

**Smallest owning-layer repair**

Alter the existing D4 history resolver only.

Required end state:

1. resolve transition truth from Git ancestry, not default path-log date/topology ordering;
2. for an uncommitted/working-tree change, compare against the committed HEAD state;
3. for a linear committed state, compare against the actual parent-line governed predecessor;
4. for merge or synthetic-PR checkouts, inspect materially relevant parent root states rather than selecting whichever path commit Git lists second;
5. if multiple parent histories carry divergent governed release state, either validate the current transition against every materially applicable parent state or fail closed until one governed integration predecessor is unambiguous under existing repository authority;
6. preserve evidence-only descendant behavior without treating unrelated commits as state transitions;
7. keep consecutive transitions and patch/minor/major future versions generic;
8. do not add a transition registry, second state file, merge-state mirror, candidate table, or compatibility subsystem.

The exact implementation mechanism remains delegated to D4. A simple ancestry/direct-parent solution is preferred over new machinery.

**Affected qualification to rerun**

- focused _previous_governed_release_state tests;
- working tree equals HEAD;
- working tree differs from HEAD;
- evidence-only descendants;
- root transition followed by unrelated commits;
- consecutive root transitions;
- date-reordered merge parents;
- synthetic PR merge topology;
- divergent sibling parent state where one parent would pass and the other reject;
- equivalent-parent merge positive;
- stale P6 recovery negative;
- sibling/non-descendant recovery negative;
- correct-version/wrong-ancestry negative;
- complete recovery-target positive;
- accepted-current/history continuity matrix;
- patch/minor/major/6.10 controls;
- full release-state tests;
- full repository build and Orchestrator Core;
- frozen-resource and source/generated parity;
- exact new-candidate qualification and binding;
- fresh independent assembled-candidate Review.

## 18. Final disposition and next authorized action

**NO-PASS.**

P8 is immutable historical Review evidence and is not technically eligible for stakeholder ratification.

Reopen the existing Protocol 6.5 workplan at D4 for B65-P8-1 only. Repair the current release-state history resolver without adding a second authority. Any material semantic repair creates a new immutable candidate identity.

All unaffected P8/P7 evidence remains usable only within its verified applicability boundary.

Do not ratify Protocol 6.5, publish a public fallback, establish recovery, cut over accepted-current, merge PR #33, or mutate Protocol 7 D3/D4.
