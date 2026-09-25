---
kind: implementation-workplan
workplan_id: SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: ready-p11-independent-review
parent_workplan: workplans/active/SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION.md
design_authority: qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md
baseline: 55c085261eb827e3047637d045a8e6917ea6b962
branch: ssdp-6.5-frontier-model-re-evaluation
---

# Protocol 6.5 D3 -> D4 Implementation Handoff

## 1. Outcome and authority

Implement the accepted Phase IV-V design for Protocol 6.5.

Protected outcome:

> SSDP's own lifecycle, qualification, Review, project-memory and representation machinery obey the same ownership/evidence/convergence principles SSDP imposes on downstream engineering, while preserving the complete accepted Protocol 6.4 D1-D4/formal-definition capability and reducing duplicated/stale self-governance machinery.

Accepted D3 design is `qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md`. The frozen diagnostic/adjudication remain evidence, not implementation authority.

Applicable parent constraints:

- accepted Protocol 6.4 at P0;
- 6.4 consolidated workplan preservation obligations;
- frozen 5.16-6.4 resource/profile/recovery identities;
- Protocol 7 D3 architecture untouched;
- remove/rewire/modify before add;
- no generated artifact as independent owner.

Non-goals: see parent workplan §13 plus no unrelated refactor.

## 2. Frozen cycle decisions

1. Add exactly one mutable release-state owner: root `PROTOCOL-RELEASE-STATE.yaml`.
2. Versioned `source/`, packaged skills and profiles own version-intrinsic semantics, not current mutable release status.
3. Review PASS is technical eligibility; explicit stakeholder ratification is the protocol-version acceptance decision.
4. Public fallback is published only after Review PASS + stakeholder ratification; recovery remains distinct/later.
5. Mechanical qualification, semantic Review and outcome qualification are separate evidence classes.
6. Substantial protocol Review includes out-of-matrix abstraction-adequacy falsification.
7. High-leverage meta predicates are defined at canonical owners, not repeated in roles.
8. Current 6.4 amendment sections are integrated into owner prose instead of renamed/appended.
9. PEM validator/schema split is reconciled; temperature/maturity model stays.
10. Protocol 7 receives only inheritance identity reconciliation after 6.5 acceptance.

## 3. Delegated D4 space

Delegated:

- helper/function/test names;
- YAML parser organization;
- exact prose editing/section placement;
- generated-file plumbing;
- fixture representation;
- local refactoring required to delete duplicate current-state values.

Forbidden:

- second release-state registry/file;
- universal semantic parser;
- exact prose pins used as semantic oracle;
- new D5/meta-authority;
- public fallback == recovery collapse;
- self-issued ratification;
- frozen historical mutations.

Simplification target: remove current lifecycle value copies, version-labelled amendment replay, stale role/template labels and QF proxy-only machinery rather than layering 6.5 wrappers around them.

## 4. Implementation obligations

### I65-01 — Release-state owner

Create `PROTOCOL-RELEASE-STATE.yaml` according to Phase IV-V §5.

Initial branch state must truthfully keep Protocol 6.4 accepted-current and 6.5 candidate/unfrozen. Do not claim 6.5 Review/ratification/publication/recovery before those events exist.

Add executable validation for:

- one accepted-current version;
- legal sentinel/state combinations;
- exact SHA syntax where required;
- referenced commits exist;
- mapped commit `source/PROTOCOL_VERSION` matches version;
- candidate Review evidence binds candidate semantic ref when PASS;
- RATIFIED requires explicit immutable stakeholder-ratification evidence;
- public-source mapping impossible before PASS+RATIFIED;
- accepted-current promotion impossible before recovery exists.

Use existing validation/test infrastructure unless a tiny shared parser materially reduces duplication. Do not create a new service/subsystem.

### I65-02 — Remove mutable lifecycle truth from versioned semantics

Rework:

- `source/README.md`;
- `source/shared/references/development-workflow-prompts.md`;
- `source/shared/references/protocol-versioning-and-compatibility.md`;
- role/specialist descriptions;
- current source dependency/navigation views;
- generated current profile/prompts.

Versioned source may state its own protocol version and generic lifecycle rules. It may not claim global accepted-current/candidate/recovery/public-ref facts that can change after the source snapshot is frozen.

Current root docs/indexes route to release-state owner rather than duplicate values.

### I65-03 — Correct 6.5 lifecycle order

Implement generic versioning/workflow semantics:

`candidate -> implementation acceptance -> freeze -> independent Review -> stakeholder ratification -> public fallback publication -> exact-ref verification -> distinct recovery -> mapping -> current-state cutover`.

No bootstrap/public-fallback publication before semantic Review/ratification.

Preserve self-reference-safe descendant publication.

### I65-04 — Meta-control definitions

Implement Phase IV-V P65-5:

- materiality in kernel;
- credible Serious Challenge threshold and resolution semantics in kernel;
- Review/falsification independence in workflow;
- protocol acceptance/ratification in versioning;
- accepted PEM integration policy in Git/workflow plus repository-local project instruction.

Avoid repeated near-definitions in every role.

### I65-05 — Qualification/Review epistemology

Refactor testing/workflow/evidence consequences so every qualification claim has explicit subject/property/method/result/limitations.

Audit `tests/test_protocol_64_axiomatic_traceability.py` and related QF64 assertions:

- keep real structural/state/schema/route tests;
- rebind tests to real owner/consumer paths where possible;
- retire proxy-only dict predicates and arbitrary wording pins from current acceptance;
- preserve historically useful cases in qualification/history when they are not current executable oracles.

Add 6.5 tests for release-state schema/projection/current-vs-history properties.

Add the out-of-matrix Review obligation to current workflow/Review prompts.

### I65-06 — PEM schema owner reconciliation

Update `project-engineering-memory.md` and the canonical template to specify justified schema fields currently enforced by the validator, including structured recurrence, PROVEN maturity obligations, comparative basis/owner authority, temperature override and bounded counterevidence search.

Remove redundant executable-only `provenance_independence_required`.

Keep Git patch-id as replaceable implementation evidence for copied-event non-independence, not schema authority.

If `alias_of` remains, document its optional semantics; otherwise remove the check cleanly.

Fix template YAML/example structure.

Update validator tests so doctrine/template/validator parity is directly checked rather than inferred from happy-path parsing.

### I65-07 — Integrate current doctrine and compress representation

Integrate all thirteen 6.4-labelled current-owner appendices identified in design §9 into their natural sections; do not simply rename headings to 6.5.

Repair stale current labels:

- 7 role/specialist descriptions currently saying Protocol 6.3;
- D1/D2 paper templates saying Protocol 6.1;
- language router saying Protocol 6.2;
- current navigation/intake/dependency surfaces carrying stale candidate/older-version state.

Remove release-specific narrative from hot versioning owner when exact history belongs in `history/SEMANTIC_EVOLUTION.md`.

Measure P0/P1 hot-context/duplication metrics. Kernel may not grow beyond P0 word count.

### I65-08 — Source/generated/profile reconciliation

After canonical source is coherent:

- bump canonical protocol source to 6.5.0 at the correct stage;
- build `dist/`;
- generate a new `ssdp-protocol-6.5` snapshot/profile without modifying frozen 6.4 or older profile bytes;
- update Core recognition only as required for the new profile/version;
- ensure generated prompts do not embed mutable current release state;
- validate package/profile/source parity.

Do not mutate frozen 6.4 resources to make current tests pass.

### I65-09 — Preservation/supersession map

Before P1 freeze create `qualification/ssdp65/PROTOCOL-6.4-TO-6.5-PRESERVATION-MAP.md` satisfying design §13.

Map every accepted 6.4 semantic capability to its 6.5 owner. Treat removed QF machinery carefully: remove only the invalid proxy representation, not the protected semantic rule.

### I65-10 — Self-hosted PEM and history

Reconcile `PROJECT-ENGINEERING-MEMORY.md` through the accepted 6.3/6.4 interval and this 6.5 intervention.

At minimum assess:

- FF-001 recurrence across later bootstrap episodes;
- successful descendant self-reference-safe publication pattern;
- qualification-proxy/review-matrix learning from this investigation;
- representation-integration/compression evidence when realized.

Record only evidence-backed families/episodes. Do not promote the new 6.5 design into memory merely because it was proposed.

Update semantic history for the accepted doctrine changes, keeping detailed release chronology out of hot current owners.

### I65-11 — Project-local accepted PEM policy

Declare in the repository's current project instruction surface that `main` is the integration publication line for accepted/base PEM, with candidate branch PEM treated as overlay unless an active workplan binds/rebinds another exact accepted state.

Do not make `main` the semantic-version oracle.

### I65-12 — Current-state projection census

Before P1 freeze search current non-historical surfaces for mutable lifecycle copies and stale version labels.

Classify each remaining exact version/SHA occurrence as:

- version-intrinsic/historical;
- deliberately frozen cycle input;
- current release-state owner;
- invalid duplicate to remove.

A generic grep count is discovery evidence, not semantic proof; final Review adjudicates borderline cases.

## 5. Evidence and acceptance

### Stage A — canonical ownership/meta semantics

Implement I65-01..I65-04. Run focused tests plus affected protocol tests. No generated descendants yet except scratch validation.

Acceptance:
- one release-state owner;
- no owner conflict;
- state schema rejects incoherent transitions;
- meta definitions are canonical and routed.

### Stage B — qualification/PEM reconciliation

Implement I65-05..I65-06.

Acceptance:
- proxy-only semantic qualification no longer gates current acceptance;
- structural tests remain strong at real owners;
- PEM doctrine/template/validator agree;
- existing valid PEM data remains readable or receives explicit schema-compatible reconciliation.

### Stage C — representation integration

Implement I65-07 plus canonical portions of I65-08/I65-11/I65-12.

Acceptance:
- release-labelled appendices integrated;
- stale role/template labels removed;
- no hot-kernel growth;
- current lifecycle copies materially reduced to owner/reference/frozen cases.

### Stage D — generated/package/profile integration

Complete I65-08.

Acceptance:
- full repository regression;
- package build/validation/dist parity;
- current 6.5 snapshot/profile parity;
- frozen 5.16-6.4 profile/resource identity;
- Core accepts/selects 6.5 without reinterpreting older versions.

### Stage E — preservation/PEM/history/candidate freeze readiness

Complete I65-09..I65-12 and impact closure.

Acceptance:
- preservation map complete;
- self-hosted PEM/history reconciled;
- final affected-surface census;
- no unresolved material impact;
- no stakeholder ratification claimed.

Then freeze P1 and enter Phase VII qualification.

## 6. Required qualification after P1 freeze

Follow the parent workplan and benchmark amendment.

At minimum:

- inherited regression and package/profile checks;
- release-state transition negative fixtures;
- stale-current-value negative cases;
- PEM schema parity;
- fresh semantic counterexample/mutation Review;
- explicit out-of-matrix Review;
- P65-1..P65-6 ablations;
- targeted P0/P1 behavior comparisons;
- simplicity/duplication/hot-context comparison.

A green mechanical suite cannot close arbitrary prose semantic adequacy.

## 7. Authority/documentation/history impact

- D1: preserved.
- D2: preserved.
- D3: protocol self-governance architecture changes as frozen here.
- D4: implementation/test/generator/profile changes required.
- Human-facing docs: current navigation/version semantics updated.
- PEM schema: semantic clarification/reconciliation within schema 1 unless implementation proves schema identity must change; do not bump schema reflexively.
- Semantic history: required.
- Protocol 7: inheritance identity only after 6.5 accepted; no architecture mutation.

## 8. Reopen / Challenge triggers

Reopen D3 before continuing if:

- one release-state file cannot replace value copies without creating another parallel owner;
- public fallback still requires mutable lifecycle truth embedded in immutable source;
- generated profiles require current mutable release status for correct execution;
- removing QF proxy machinery exposes an unowned semantic acceptance requirement;
- PEM validator behavior cannot be reconciled to accepted 6.3 doctrine without changing memory semantic identity;
- representation compression would lose a P64/inherited capability;
- hot-kernel non-growth cannot be met without hiding mandatory semantics.

Raise Serious Challenge if accepted D1-D4/formal-definition doctrine itself is shown materially false/incoherent; none is currently active.

## 9. Final handoff state

```text
D3 DESIGN: PASS / NOT REOPENED
PHASE VI IMPLEMENTATION: REPAIR COMPLETE — P5 FROZEN
P1: FROZEN / FAILED REVIEW — b565e28aeacea002cefe27e6b9594fe99d653c0a
P2: FROZEN / FAILED REVIEW — e8edb353e172aef933ed5e58eeabe897d0cc98d1
P2 NORMAL PR QUALIFICATION: 35996488794 / PASS\nP3: FROZEN — 89ccc71a7b0e9458a3e77306be2a773d4059f0f2\nP3 NORMAL PR QUALIFICATION: 36018551068 / PASS
P4: FROZEN / FAILED REVIEW — 43ff4273fbdaf46b9677cffdb091b741ce754a7d
P5: FROZEN — d2d672a3e814438fb618f901137f88c8698a205d
P5 NORMAL PR QUALIFICATION: 36047926253 / PASS
P4 NORMAL PR QUALIFICATION: 36041360949 / PASS
PUBLIC 6.5 FALLBACK: UNAVAILABLE
6.5 RECOVERY: UNAVAILABLE
6.5 RATIFICATION: NOT REQUESTED
ACCEPTED CURRENT: resolve from PROTOCOL-RELEASE-STATE.yaml
PROTOCOL 7 D3/D4: UNCHANGED
```


## 10. Independent Review repair delta — 2026-09-24

The accepted D3 design remains valid. Fresh independent Review found three D4/current-representation nonconformances; do not redesign P65-1..P65-6.

- B65-R1: release_state.py must resolve immutable Review evidence and bind exact candidate/disposition rather than accepting regex shape alone.
- B65-R2: long-lived release-state tests must not copy the live lifecycle phase; move freeze-time observations back to qualification evidence and test invariant transitions with lifecycle-independent fixtures.
- B65-R3: canonical/current 6.5 workflow prompts must not predecessor-gate inherited 6.4 obligations. Remove those operational version qualifiers and regenerate descendants.

Repair by alteration/removal inside existing owners. Do not add a state mirror, semantic parser, compatibility wrapper or prose theorem prover.

P1 b565e28aeacea002cefe27e6b9594fe99d653c0a is immutable and failed Review. The repaired implementation must freeze a new semantic candidate and rerun affected Phase VII evidence plus fresh independent Review.


## 11. P2 D4 repair closure

B65-R1 through B65-R3 are implemented at their existing D4/current-representation owners with no P65 D3 redesign.

The repair also removed the sibling live-phase oracle in `tests/test_protocol_64_axiomatic_traceability.py`, because it encoded the same duplicated mutable lifecycle truth as B65-R2.

Exact P2 is `e8edb353e172aef933ed5e58eeabe897d0cc98d1`; normal repository qualification run `35996488794` passed both build and Orchestrator Core jobs.

Implementation is complete for the bounded repair. The next stage is a fresh independent assembled-candidate Review of P2 by a non-authoring context.


## 12. P2 independent Review repair delta — 2026-09-24

Fresh independent assembled-candidate Review of P2 issued **NO-PASS** without reopening D3.

### B65-P2-1 — inherited lifecycle-value copies remain

Repair at D4 testing/qualification only:

- remove live \`accepted_current == 6.4.0\` / current 6.4 mapping assertions from \`tests/test_protocol_64_bootstrap_readiness.py\`; preserve the immutable Protocol 6.4 bootstrap/recovery contract independent of whether 6.4 is current or historical;
- remove live \`accepted_current == 6.4.0\` and \`candidate.version == 6.5.0\` assertions from \`tests/test_protocol_61_evidence_evolution.py\`; preserve historical 6.1/6.2 identity and generic release-state-owner routing;
- perform a bounded census for equivalent mutable phase values in long-lived tests;
- add legal lifecycle-transition fixtures so current-owner advancement does not require test edits.

Prefer direct alteration/removal. No synchronized phase table, compatibility wrapper, or second state owner.

### B65-P2-2 — terminal ratification binding is incomplete

Repair in existing \`source/release_state.py\` and focused tests:

- keep immutable repository/path resolution;
- for terminal RATIFIED/REJECTED evidence require minimal machine-readable binding to the exact current \`candidate.semantic_ref\` and matching disposition;
- keep actual stakeholder authorization outside machine prose interpretation;
- add wrong candidate, wrong disposition, wrong repository, missing commit/path, and valid exact binding cases.

No new registry/service/parser is authorized.

P2 \`e8edb353e172aef933ed5e58eeabe897d0cc98d1\` is immutable and failed Review. Repairs create a new candidate identity and require exact-candidate requalification plus fresh independent Review.


## 13. P3 D4 repair closure

P2 Review blockers B65-P2-1 and B65-P2-2 are repaired at the existing D4 owners.

- Lifecycle-value duplication was removed/rebound in the two surviving inherited tests, with explicit successor transition fixtures and a bounded current test census.
- Terminal ratification evidence now binds immutable route + exact candidate + matching terminal disposition in the existing release-state validator.
- Review/ratification candidate metadata no longer hard-codes P1/P2 labels; generic candidate fields and historical \`pN\` compatibility are accepted.
- No state mirror, compatibility wrapper, semantic registry, prose parser, or generated-source edit was introduced.

Exact P3 is \`89ccc71a7b0e9458a3e77306be2a773d4059f0f2\`. Exact-P3 normal PR workflow \`36018551068\` passed the complete build and Orchestrator Core jobs.

Binding descendant `c3df40cdb144c66a390b5d69b49e6fe8a81ad825` passed normal workflow run `36018970303` with Review still `NOT_RUN` and no ratification/publication/recovery advancement.

D3 remains closed. P3 must now receive a fresh independent assembled-candidate Review before stakeholder ratification or publication.


## 14. P4 D4 repair closure

Fresh independent P3 Review found two remaining D4/current-representation blockers. Both are repaired by alteration inside existing owners.

### B65-P3-1

`source/release_state.py` no longer accepts set membership across all candidate-like metadata. It resolves one evidence subject: agreeing explicit `candidate_ref`/`semantic_ref` when present, otherwise the highest legacy `pN` candidate generation. Historical/lower `pN` fields cannot rescue a wrong explicit subject or let P3 borrow P4 disposition.

Focused Review and ratification counterexamples cover explicit-vs-historical conflict, conflicting explicit fields, and P3/P4 legacy coexistence. No registry, wrapper or prose semantic parser was added.

### B65-P3-2

The current canonical evidence owner no longer scopes impact-closure semantics to Protocol 6.4. A fresh 34-file current shared-reference census found no remaining predecessor-scoped labels. Generated package descendants were regenerated; frozen historical profiles were not edited.

Exact replacement candidate P4 is `43ff4273fbdaf46b9677cffdb091b741ce754a7d`; normal repository qualification run `36041360949` passed both build and Orchestrator Core jobs.

D3 remains closed. P4 must receive fresh independent assembled-candidate Review before any stakeholder ratification or publication.


## 15. P4 independent Review repair delta — 2026-09-24

Fresh independent assembled-candidate Review of P4 issued **NO-PASS** without reopening D3.

### B65-P4-1 — structural evidence-front-matter ambiguity

Repair only the existing D4 owner in source/release_state.py and its focused tests:

- reject duplicate YAML mapping keys in evidence front matter;
- treat candidate_ref / semantic_ref key presence as explicit binding intent even when the parsed value is empty/null;
- require present explicit subject fields to be nonempty valid exact candidate SHAs and to agree;
- never let legacy pN rescue a present-but-invalid explicit subject field;
- retain the generic highest-generation legacy pN rule only when explicit subject keys are absent;
- retain arbitrary prose outside machine semantic judgment.

Add duplicate-candidate-key, duplicate-status, empty/null explicit-subject negatives to the full existing Review/ratification matrix. Preserve future candidate-generation behavior and do not add candidate-specific logic.

P4 is immutable and failed Review. The repair must freeze a new candidate and rerun affected exact-candidate qualification plus fresh independent Review.


## 16. B65-P4-1 implementation closure

Implemented by direct alteration of the existing D4 parser/binder:

- strict duplicate-key rejection in evidence YAML front matter;
- explicit subject-field presence is authoritative even for invalid/empty/null values;
- present explicit subjects require exact lowercase 40-hex commit identities and agreement;
- legacy highest-generation pN fallback applies only when explicit subject fields are absent;
- invalid/empty highest legacy generation rejects instead of falling back to a lower historical candidate.

No registry, mirror, compatibility subsystem, candidate-specific table, prose parser, or D3 change was added.

Focused tests cover the P4 holdouts for both Review and terminal ratification plus future p5 behavior. Exact replacement-candidate identity and CI are pending freeze from this implementation commit; a later descendant must bind that immutable identity with Review reset to NOT_RUN.


## 17. P5 D4 repair closure

B65-P4-1 is closed at the existing D4 parser/binder owner.

Exact P5 is d2d672a3e814438fb618f901137f88c8698a205d. Exact-P5 normal PR workflow 36047926253 passed repository release-state validation, PEM validation, complete protocol regression, package build/validation/parity, whitespace, packaged Protocol 6.5 snapshot parity, and Orchestrator Core acceptance.

A later descendant now binds P5 with Review reset to NOT_RUN and no ratification/publication/recovery advancement.

D3 remains closed. P5 must receive fresh independent assembled-candidate Review before stakeholder ratification or publication.


## 18. P5 independent Review repair delta — 2026-09-24

Fresh independent assembled-candidate Review of exact P5 issued **NO-PASS** without reopening D3.

### B65-P5-1 — root release-state duplicate-key ambiguity

Alter only the existing D4 root-state loader/validator:

- apply the existing duplicate-rejecting YAML loader to `PROTOCOL-RELEASE-STATE.yaml`, not only Review/ratification evidence front matter;
- reject duplicate top-level and nested lifecycle keys before `validate_release_state()`;
- make focused tests exercise the real load boundary rather than pre-normalizing with `yaml.safe_load`.

### B65-P5-2 — candidate succession underconstrained

Alter only the existing D4 state validator:

- require a pre-cutover active candidate version to be a semantic-version successor of accepted-current;
- reject active candidate collision with any historical version;
- retain the already-authorized coherent terminal accepted-current == candidate state;
- add lower/equal/historical negative fixtures and patch/minor/major successor positives.

P5 `d2d672a3e814438fb618f901137f88c8698a205d` remains immutable. Repair must freeze a new candidate and rerun affected exact-candidate qualification plus fresh independent Review. No registry, mirror, compatibility subsystem, synchronized phase table, or D3 redesign is authorized.


## 19. B65-P5-1 / B65-P5-2 D4 repair closure

Implemented by direct alteration inside the existing release-state owner:

- root state YAML now rejects duplicate mappings before semantic validation using the same strict loader already used for evidence front matter;
- active pre-cutover candidate versions must be newer than accepted-current and cannot collide with historical versions;
- terminal accepted-current == candidate remains legal only through the existing fully closed terminal predicate;
- focused tests exercise the actual root load boundary, a real historical-ref collision, a lower non-historical candidate, and patch/minor/major successor controls.

P5 remains immutable and is now bound to its durable NO-PASS evidence in mutable lifecycle state. The replacement semantic candidate is the implementation commit containing these changes; its exact SHA must be frozen and qualified from a later descendant before fresh independent Review.


## 20. P6 D4 repair closure

B65-P5-1 and B65-P5-2 are implemented at their existing D4 owner.

Exact P6 is `dd06da8136416e67644586c44880b466f982b8ff`; normal repository qualification run `36051369390` passed both build and Orchestrator Core jobs.

A later descendant binds P6 with Review reset to `NOT_RUN` and no ratification/publication/recovery advancement.

D3 remains closed. P6 must now receive a fresh independent assembled-candidate Review before stakeholder ratification or publication.


## 21. P6 binding qualification

P6 `dd06da8136416e67644586c44880b466f982b8ff` remains immutable. Binding descendant `758490c11f90b587c7dfaadddab958751f2881c9` passed normal workflow run `36051619464` with Review `NOT_RUN` and no ratification/publication/recovery advancement.

Implementation repair is mechanically closed. The next stage is fresh independent assembled-candidate Review of P6.


## 22. P6 independent Review repair delta — 2026-09-24

Exact P6 \`dd06da8136416e67644586c44880b466f982b8ff\` received fresh independent **NO-PASS**. Accepted P65 D3 remains closed.

### B65-P6-1 — strict root-state parser must own every root-state read

Alter existing D4 consumers only:

- route every read of root \`PROTOCOL-RELEASE-STATE.yaml\` used for mechanical qualification through existing \`release_state.load()\`;
- eliminate direct ordinary \`yaml.safe_load\` pre-normalization of that authoritative root file;
- preserve unrelated YAML parsing and all immutable historical assertions;
- rerun all affected inherited/current state tests and full duplicate/alias structural falsification.

### B65-P6-2 — historical state must be temporally behind accepted-current

Alter the existing validator only:

- establish one canonical ASCII x.y.z numeric identity;
- require each historical version to be strictly older than accepted-current;
- preserve numeric \`6.10.0\` ordering, patch/minor/major successors, terminal equality, and next-successor behavior;
- add the real-ref unsuperseded-history negative and canonical-version spelling negatives.

No D3 redesign, registry, mirror, wrapper, compatibility subsystem, candidate-specific table, semantic parser, or synchronized phase table is authorized.

Freeze a new immutable candidate after repair; rerun affected exact-candidate qualification and fresh independent Review.


## 23. P7 D4 repair closure

B65-P6-1 and B65-P6-2 are implemented by direct alteration/rewiring at existing D4 owners.

- Root release-state consumers route through existing strict `release_state.load()`; no second parser/wrapper was introduced.
- Version identity is canonical ASCII x.y.z; history is strictly older than accepted-current; candidate/history disjointness and ordering remain generic.
- Focused qualification covers real-ref future-history rejection, canonical-spelling negatives, `6.10.0`, patch/minor/major successors, terminal equality, and post-cutover successors.
- Exact P7 `133c747a1f9ab4372c9e1af7a7e9666316dc892b` passed normal workflow run `36058860629` across full build and Orchestrator Core.
- D3 remains closed; no registry, mirror, compatibility subsystem, candidate-specific table, semantic parser, or synchronized phase table was added.

P7 must receive fresh independent assembled-candidate Review before any stakeholder ratification or publication.


## 24. P7 binding qualification

P7 `133c747a1f9ab4372c9e1af7a7e9666316dc892b` remains immutable. Binding descendant `a0ee73af1b2d6af1cdd42533ca007e8a99073ef9` passed normal workflow run `36059112506` with Review `NOT_RUN` and no ratification/publication/recovery advancement.

Implementation repair is mechanically closed. The next stage is fresh independent assembled-candidate Review of P7.


## 25. P7 independent Review repair delta — 2026-09-24

Fresh independent assembled-candidate Review of exact P7 `133c747a1f9ab4372c9e1af7a7e9666316dc892b` issued **NO-PASS** with no Serious Challenge. Accepted P65 D3 remains closed.

Governing Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P7-NO-PASS.md`

### B65-P7-1 — release-state transition and recovery lineage are under-enforced

The existing D4 release-state validator proves snapshot coherence but does not generically prove the accepted temporal transaction.

Repair only the existing release-state owner/validator and focused consumers:

1. validate release-state transitions against the immediately prior governed state when the root state changes;
2. preserve all prior historical mappings unchanged unless an explicitly authorized correction exists;
3. when accepted-current advances, require the previously accepted mapping to move unchanged into historical;
4. when candidate recovery becomes available, require a genuine later recovery target that:
   - is distinct from semantic/public fallback;
   - descends from the semantic candidate;
   - already contains the same exact candidate subject, Review PASS evidence, RATIFIED evidence, and public fallback mapping required by the accepted release sequence;
5. keep accepted-current cutover illegal until those temporal predicates hold;
6. keep patch/minor/major and multi-digit future progression generic.

Mandatory fresh negatives include:

- exact P7 public fallback with stale P6 as the alleged 6.5 recovery target;
- a same-version recovery commit that lacks P7 Review/ratification/publication state;
- terminal 6.5 cutover omitting historical 6.4;
- terminal cutover mutating the 6.4 public or recovery mapping;
- deletion or rewrite of an already historical mapping.

Mandatory positives include:

- a later recovery descendant containing the complete reviewed/ratified/published lifecycle state;
- legal 6.4 -> 6.5 cutover preserving exact 6.4 historical identity;
- equivalent future 6.5 -> 6.6 and patch/major controls.

Do not add a transition registry, second state file, state mirror, compatibility subsystem, candidate-specific table, semantic prose parser, or synchronized phase table. Reuse the existing release-state owner and its existing Git/ref boundary.

P7 remains immutable and failed Review. Any semantic repair creates a new candidate identity and requires affected exact-candidate qualification, freeze/binding, and another fresh independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.


## 26. B65-P7-1 D4 repair implementation

B65-P7-1 is repaired by direct strengthening of the existing `source/release_state.py` transaction owner. Accepted P65 D3 remains closed.

The owner now enforces two relations in addition to snapshot coherence:

1. **release-state transition continuity**
   - accepted-current identity cannot be rewritten while its version is unchanged;
   - existing historical mappings cannot be deleted or rewritten;
   - history cannot grow unless accepted-current advances;
   - accepted-current advancement must promote the immediately previous fully closed candidate;
   - the previous accepted-current mapping must move unchanged into history;
   - no unrelated historical insertion is admitted during cutover.

2. **recovery lineage**
   - recovery must descend from the semantic candidate;
   - Review evidence must descend from the semantic candidate;
   - ratification evidence must follow Review evidence;
   - recovery must follow the Review/ratification lineage and be an ancestor of the mapping-publishing state;
   - the recovery target's own root release state must already contain the exact candidate, PASS evidence, RATIFIED evidence, and exact public fallback while its own recovery field is still UNAVAILABLE.

Transition validation resolves the prior governed state from the repository history of the sole root state file, so PR merge-checkout shape does not create a second transition authority.

Focused tests include the exact stale P6-as-P7-recovery holdout, accepted-current cutover without 6.4 history transfer, mutated historical identity, accepted-current identity rewrite, and a positive complete recovery snapshot.

No second release-state file, registry, mirror, transition service, compatibility subsystem, semantic prose parser, candidate-specific table, or synchronized phase table was introduced.

The semantic replacement candidate is the implementation commit containing this repair. Its exact SHA must be frozen only after exact-candidate normal CI passes. P7 remains immutable and failed Review.


## 27. P8 freeze and binding handoff

B65-P7-1 repair passed exact-candidate normal workflow run `36067942018`.

Immutable replacement candidate:

`P8 = ed782ccad73b43c9052ecc926177c36846b9328d`

This later descendant binds P8 in the sole mutable release-state owner with Review `NOT_RUN`, ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

The binding descendant must pass the normal workflow before a fresh independent assembled-candidate Review begins. No D3 reopening or acceptance/publication action is authorized.


## 28. P8 binding qualification complete

Lifecycle descendant `65cd5da2d6793733e87d0b97f9ccce23d22b9154` binds exact P8 `ed782ccad73b43c9052ecc926177c36846b9328d` with Review `NOT_RUN`, ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

Normal workflow run `36068315599` passed the complete build and Orchestrator Core jobs, including the new release-state transition validator.

B65-P7-1 is mechanically repaired and qualified at the existing D4 owner. The next stage is a genuinely fresh independent assembled-candidate Review of exact P8. Accepted P65 D3 remains closed.


## 29. B65-P8-1 D4 repair contract — transition-history resolution

P8 independent Review found one surviving D4 blocker. Accepted P65 D3 remains closed.

**Owner:** source/release_state.py::_previous_governed_release_state and its direct integration with root release-state validation.

**Failure:** the current resolver uses ordinary path history and can select a sibling merge-parent state as the previous governed release state. A fresh merge-DAG holdout demonstrates a false pass: sibling S1 -> merge M2 passes while actual first-parent F1 -> M2 rejects deletion of an immutable historical mapping.

Repair the existing owner only.

Required behavior:

1. derive the prior governed state from Git ancestry/parent topology, not default path-log ordering;
2. when the working tree differs from HEAD, compare against committed HEAD state;
3. on a linear committed transition, compare against the actual parent-line governed predecessor;
4. on merge/synthetic-PR checkouts, inspect materially relevant parent release states;
5. if divergent parent states make the governed predecessor ambiguous, validate against every materially applicable parent state or fail closed under the existing integration-line authority;
6. retain correct evidence-only-descendant and consecutive-transition behavior;
7. preserve generic patch/minor/major and multi-digit semver behavior;
8. do not add a second registry, state mirror, transition table, candidate-specific branch, or compatibility subsystem.

Mandatory fresh negatives/holdouts:

- date-reordered merge parents where path log lists the sibling before the governed parent;
- divergent parent state where one parent would pass and the other rejects historical deletion/rewrite;
- synthetic PR merge topology;
- sibling/non-fast-forward recovery;
- recovery with correct protocol version but wrong ancestry.

Mandatory positives:

- working tree change against HEAD;
- linear root-state transition;
- evidence-only descendants;
- transition followed by unrelated commits;
- consecutive legal transitions;
- equivalent merge-parent state;
- legal future patch/minor/major and 6.10 controls;
- complete recovery-target lineage.

After repair, rerun the complete release-state suite, full repository build/Core, preservation and parity checks, freeze a new immutable candidate, bind it from a later descendant, and perform a fresh independent assembled-candidate Review.

P8 is immutable and remains NO-PASS.


## 30. B65-P8-1 implementation closure — ancestry-boundary resolver

B65-P8-1 is repaired at the existing D4 release-state owner without reopening P65 D3.

The former global path-log resolver is removed. The owner now derives predecessor state from Git ancestry:

- an uncommitted root-state edit is compared directly with committed HEAD;
- for a committed state, direct parents are inspected;
- ancestry is traversed only through parents whose parsed root release state is semantically equal to the current state;
- the first differing release-state snapshot on each parent lineage is a governed predecessor boundary;
- equivalent predecessor states are deduplicated;
- merge/synthetic-PR states therefore validate against every materially divergent parent boundary instead of whichever path commit Git lists second;
- parent lineages predating introduction of the root release-state owner contribute no predecessor state.

This preserves evidence-only descendants and consecutive transitions while eliminating date/topology ordering as an authority mechanism.

Fresh real-Git resolver tests cover:

- working-tree change versus HEAD;
- linear committed transition;
- evidence-only descendant after a transition;
- date-reordered divergent merge parents, including the exact false-pass shape from the P8 Review;
- equivalent merge-parent lineages;
- synthetic PR merge with a pre-owner base parent.

The P8 NO-PASS evidence is also bound in the root release state from immutable Review commit 39f3703ad1e07457d5fcc9b2dc6f39c55c69fc98.

No second release-state registry, mirror, transition table, compatibility subsystem, candidate-specific branch, or D3 mechanism is introduced.

The implementation commit produced by this section is the prospective P9 semantic candidate. It must pass exact-candidate normal CI before its SHA is frozen/bound as P9.


## 31. P9 freeze and binding handoff

Exact prospective-P9 workflow run `36091484812` passed the complete build and Orchestrator Core jobs.

The replacement semantic candidate is therefore frozen as:

`P9 = fb347272c70b6225743fdc99e9bec8b4197aad49`

This descendant binds the already-existing P9 identity in root `PROTOCOL-RELEASE-STATE.yaml` with Review `NOT_RUN`, ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

Binding qualification must pass before the fresh independent assembled-candidate Review handoff is advanced to P9.


## 32. P9 binding qualification complete

Lifecycle descendant `69f7cda3bd9bdfdbc113b4ec5ac6da044a7d46ab` binds exact P9 `fb347272c70b6225743fdc99e9bec8b4197aad49` with Review `NOT_RUN`, ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

Normal workflow run `36091605214` passed the complete build and Orchestrator Core jobs, including the real Git ancestry-boundary transition resolver tests, release-state validation, PEM validation, inherited regression, package build/independent validation/dist parity, whitespace, packaged Protocol snapshot parity, and Orchestrator Core acceptance.

B65-P8-1 is mechanically repaired and qualified at the existing D4 owner. Accepted P65 D3 remains closed.

The next stage is a genuinely fresh independent assembled-candidate Review of exact P9. This repair/authoring context is not eligible to self-issue that verdict.


## 33. P9 independent Review NO-PASS — governed-owner deletion topology

Fresh independent assembled-candidate Review of immutable P9 `fb347272c70b6225743fdc99e9bec8b4197aad49` issued **NO-PASS**.

Durable Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P9-NO-PASS.md`

Review publication commit:

`98fcef496f10d4980d97099ea4607d60ef3e812a`

One D4 blocker survives:

**B65-P9-1 — governed release-state owner deletion is conflated with genuine pre-owner ancestry in production predecessor resolution.**

The exact P9 resolver correctly removes date/path-log ordering as authority for owner-present ancestry, but `_previous_governed_release_states()` treats every parent lacking `PROTOCOL-RELEASE-STATE.yaml` as if the lineage genuinely predates owner introduction. A fresh holdout demonstrated that a branch can contain the governed owner, delete it, and later merge into an owner-restoring branch; the deleted parent is silently skipped and the malformed governed interval is never validated.

Repair only the existing D4 release-state ancestry classifier:

1. Preserve an explicit distinction between a valid parsed state and path absence.
2. For a missing parent state, inspect that lineage's ancestry to determine whether the owner genuinely never existed.
3. Ignore a missing lineage only when no governed ancestor exists.
4. If a governed ancestor exists, post-introduction owner deletion/reintroduction must fail rather than masquerade as pre-owner history.
5. Keep behavior independent of timestamps, default `git log` ordering, branch names, newest/default refs, sibling enumeration, and traversal-stack order.
6. Preserve current working-tree, linear, evidence-only, consecutive-transition, equivalent-parent, divergent-owner-present-parent, genuine-pre-owner PR-merge, and recovery-lineage behavior.

Mandatory fresh repair controls:

- owner introduced -> sibling deletes owner -> merge restores owner: reject;
- same topology with reversed parent order: reject;
- same topology with reversed timestamps: reject;
- multiple commits while owner absent: reject;
- delete then reintroduce on the same governed lineage: enforce the explicit governed deletion/reintroduction rule rather than silently classifying it pre-owner;
- genuine pre-owner base + governed feature lineage: continue to pass;
- long genuine pre-owner ancestry: continue to pass;
- all P9 owner-present topology and recovery controls: continue to pass.

Do not reopen accepted P65 D3. Do not add a second state authority, registry, transition mirror, compatibility layer, topology service, or candidate-specific branch.

P9 remains immutable failed Review evidence. Any semantic repair creates a new candidate identity. After repair: rerun the focused topology/transition/recovery suite, full repository build/Core, preservation/parity evidence, exact replacement-candidate CI, freeze/binding, then a new fresh independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.


## 34. Historical capability preservation obligation for the P9 replacement

A dedicated historical-capability preservation review of exact P9 is recorded at:

`qualification/ssdp65/HISTORICAL-CAPABILITY-PRESERVATION-REVIEW-2026-09-25-P9.md`

Disposition:

- no additional historical doctrine loss was found;
- P9's compression preserves the inspected accepted Protocol 5.13-6.4 capability lineage in modern owners/concretizations;
- B65-P9-1 is also the sole surviving historical-capability nonconformance because it can erase a post-introduction governed release-state interval;
- no D3 reopen is required.

The replacement candidate qualification must preserve this transitive capability closure. In addition to the B65-P9-1 focused topology matrix, rerun the active historical regression modules for convergence/simplicity, relation-first tools/CodeQL, language profiles, long-horizon quality/orchestration, Protocol 6.1 evidence evolution and package closure, Protocol 6.2 representation, Protocol 6.3 PEM, and Protocol 6.4 structural traceability.

Also re-establish exact frozen Protocol 5.16 and 6.0-6.4 profile/prompt identity, source/generated current-prompt parity, Protocol 7 D3/D4 isolation, and the current-owner semantic presence of D1-D4 authority, evidence lifecycle, Lossless Representation/progressive disclosure, PEM/HAS non-authority, exact fallback/recovery/version binding, and Protocol 6.4 formal-definition/source-availability doctrine.

Do not restore old amendment prose, proxy-only QF machinery, duplicated release-state values, or historical implementation mechanisms merely to make preservation more visible. Capability, not old representation, is the preservation oracle.


## 35. B65-P9-1 implementation closure — prospective P10

B65-P9-1 is repaired at the existing D4 release-state ancestry owner without reopening P65 D3.

The production resolver now distinguishes three outcomes when reading a historical release-state path:

- a valid parsed governed state;
- explicit path absence;
- malformed/unreadable state that already emits validation error.

Path absence no longer means pre-owner by assumption. For any absent HEAD/parent boundary, the resolver performs a bounded ancestry-history query for the exact sole owner path. If that lineage has any ancestor commit containing a parseable release-state owner, the absence is rejected as a governed deletion/reintroduction. Only a lineage with no such ancestor is treated as genuinely pre-owner and ignored.

This ancestry query is existential only. It does not select a predecessor state, does not use timestamp ordering, branch names, default/latest refs, sibling order, or traversal-stack order, and therefore does not reintroduce B65-P8-1.

Fresh real-Git qualification added at the production resolver covers:

- governed owner -> sibling deletion -> owner-restoring merge: reject;
- reversed merge-parent order: reject;
- reversed parent timestamps: reject;
- multiple commits while the governed owner is absent: reject;
- delete then reintroduce on the same governed lineage: reject;
- long genuinely pre-owner ancestry merged with a governed feature lineage: pass;
- all P9 owner-present topology controls remain active.

The accepted PEM basis remains P0 `55c085261eb827e3047637d045a8e6917ea6b962` with the current branch overlay. SP-002 and FF-001 remain release-lifecycle evidence, PC-001 remains an authority-bound frozen-resource preservation obligation, and DS-001 requires real-owner qualification rather than proxy-only closure. No PEM item requires preserving the P9 mechanism itself.

The implementation commit produced by this section is only the **prospective P10** semantic candidate. P9 remains immutable NO-PASS evidence and remains the root release-state candidate until the implementation commit passes exact-candidate normal CI. After that pass, a later descendant may freeze/bind the exact implementation SHA as P10 with Review reset to `NOT_RUN`.


## 36. P10 freeze and lifecycle binding

Exact prospective-P10 workflow run `36098785911` passed the complete build and Orchestrator Core jobs.

The immutable replacement semantic candidate is therefore frozen as:

`P10 = 275b23bfa45cc72145d2079c8d945a6ff5a5c216`

This later descendant binds exact P10 in root `PROTOCOL-RELEASE-STATE.yaml` with Review reset to `NOT_RUN`, stakeholder ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current Protocol 6.4.

Two additional evidence-only topology tests are added in this binding descendant to exercise the new explicit HEAD-missing branch:

- genuine first owner introduction from pre-owner HEAD remains legal;
- working-tree owner reintroduction after a governed deletion is rejected.

These tests do not mutate P10 production semantics. Normal workflow qualification of this binding descendant is required before fresh independent Review handoff.


## 37. P10 binding qualification complete

Immutable P10 `275b23bfa45cc72145d2079c8d945a6ff5a5c216` passed exact-candidate normal workflow run `36098785911` across the complete build and Orchestrator Core jobs.

Binding descendant `82949a0c8325fce602c39fb3dfdab56352d94b73` passed normal workflow run `36098950938` with:

- candidate semantic ref: exact P10;
- Review: `NOT_RUN`;
- stakeholder ratification: `NOT_REQUESTED`;
- public fallback/recovery: `UNAVAILABLE`;
- accepted-current: Protocol 6.4;
- Protocol 7 D3/D4: unchanged.

The binding run also exercised the evidence-only working-tree first-introduction versus governed-reintroduction controls added after P10 freeze.

Durable qualification records:

- `qualification/ssdp65/P10-REPAIR-QUALIFICATION.md`;
- `qualification/ssdp65/P10-FREEZE-BINDING.md`;
- `qualification/ssdp65/P10-BINDING-QUALIFICATION.md`.

B65-P9-1 is mechanically repaired and qualified at the existing D4 owner. Accepted P65 D3 remains closed.

The next authorized stage is a genuinely fresh independent assembled-candidate Review of exact P10.


## 44. P10 independent Review NO-PASS — incomplete-ancestry repair

Fresh independent assembled-candidate Review of immutable P10
`275b23bfa45cc72145d2079c8d945a6ff5a5c216` issued **NO-PASS**.

Durable Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P10-NO-PASS.md`

Immutable Review publication commit:

`964815e81c3ea538ba01789ca54d12e284fd14e2`

### B65-P10-1 — incomplete ancestry is conflated with genuine pre-owner ancestry

The P10 repair is correct when the relevant Git ancestry is complete: visible post-introduction owner deletion is
rejected, and parent order, timestamps, sibling enumeration, and traversal-stack order do not select authority.

The remaining D4 defect is the negative inference in the existing release-state ancestry classifier. An empty
`git rev-list --full-history <ref> -- PROTOCOL-RELEASE-STATE.yaml` result proves only that no owner-bearing commit is
visible in the searched object graph. In a shallow/incomplete repository, it does not prove that the lineage never
previously contained the governed owner.

A fresh real-Git holdout demonstrated:

```text
pre-owner
-> owner introduced
-> owner deleted
-> depth-1 shallow checkout at deletion
-> working-tree owner reintroduction
-> visible exact-path history is empty
-> P10 classifies the lineage as pre-owner
-> no deletion/reintroduction error
```

This violates the existing D3 contract that a missing owner may be ignored only when ancestry establishes genuine
pre-owner history.

### Earliest owner and repair boundary

Earliest owner: **D4 `source/release_state.py`**, specifically the negative-result semantics of
`_lineage_has_governed_release_state()` / `_reject_governed_owner_absence()`.

Do **not** reopen P65 D3.

Do **not** add a second state owner, registry, transition mirror, topology service, compatibility layer, branch-name
policy, timestamp policy, candidate-specific branch, or semantic parser.

### Minimum repair contract

1. Preserve the current positive existential rule: if any visible ancestor contains a valid governed owner, the
   lineage is governed.
2. A negative owner-history result may mean "genuinely pre-owner" only when the ancestry searched is known complete
   enough to support that negative claim.
3. If the repository is shallow/incomplete and no governed owner has been found, fail closed with an explicit
   incomplete-ancestry validation error rather than classifying the lineage as pre-owner.
4. Preserve existing fail-closed behavior for an ancestry query that itself fails.
5. Keep timestamps, default `git log` order, branch names, repository default/latest, sibling-parent order,
   traversal-stack order, and candidate identities non-authoritative.
6. Preserve all complete-history P10 positives/negatives: working-tree vs HEAD, linear transitions, evidence-only
   descendants, consecutive material transitions, equivalent/divergent parents, genuine pre-owner history, visible
   deletion/reintroduction, recovery lineage, canonical semver, and evidence binding.

### Mandatory fresh holdouts

Exercise the real production resolver with real Git repositories:

- owner introduction hidden beyond a shallow boundary -> visible owner deletion -> working-tree reintroduction:
  **reject/fail closed**;
- owner introduction hidden beyond a shallow boundary on a missing merge-parent lineage: **reject/fail closed**;
- complete-history genuine pre-owner HEAD -> first working-tree introduction: **pass**;
- complete-history genuine pre-owner merge parent + governed feature lineage: **pass**;
- rerun all P10 complete-history topology/recovery controls.

### Replacement-candidate rule

P10 remains immutable. Any semantic change implementing this repair creates a **new candidate identity**. Do not
predeclare that identity before the repair commit exists and exact-candidate normal CI passes. After exact-candidate
qualification, bind the new candidate from a later lifecycle descendant with Review reset to `NOT_RUN`, rerun
binding qualification, and perform a new fresh independent assembled-candidate Review.

No stakeholder ratification, public fallback, recovery, accepted-current cutover, PR merge, or Protocol 7 D3/D4
mutation is authorized.


## 45. B65-P10-1 implementation — prospective replacement candidate

B65-P10-1 is repaired at the existing D4 release-state ancestry classifier without reopening accepted Protocol 6.5 D3.

The existing positive existential owner-history query remains unchanged. The repair narrows only the former negative
conclusion: after an exact-path ancestry search finds no visible governed owner, the resolver now verifies Git ancestry
completeness with `git rev-parse --is-shallow-repository`. A shallow/incomplete repository cannot prove that the
lineage never previously contained the owner, so the resolver fails closed instead of classifying the lineage as
genuinely pre-owner. A failure or unrecognized result from the ancestry-completeness query also fails closed.

No registry, mirror, topology service, compatibility layer, branch-name/default/latest policy, timestamp policy,
candidate-specific identity, or second state owner is introduced.

Fresh real-Git holdouts exercise the production resolver for:

- governed owner introduction hidden beyond a depth-1 shallow boundary, followed by visible deletion and working-tree
  reintroduction: fail closed;
- governed owner introduction hidden beyond a depth-2 shallow boundary on a missing merge-parent lineage: fail closed;
- existing complete-history genuine pre-owner working-tree introduction: remains legal;
- existing complete-history genuine pre-owner merge lineage: remains legal;
- all prior P10 complete-history topology, transition, recovery, schema, and evidence-binding controls remain in the
  affected regression surface.

This commit is only the **prospective replacement semantic candidate**. P10 remains immutable NO-PASS evidence.
Do not assign the next P-number until exact-candidate normal CI passes. After that pass, bind the exact repair SHA from
a later lifecycle descendant with Review reset to `NOT_RUN`, rerun binding qualification, and require another fresh
independent assembled-candidate Review.


## 46. P11 freeze and lifecycle binding

The B65-P10-1 repair commit passed exact-candidate normal workflow run `36103358186` across both complete build and
Orchestrator Core jobs.

The immutable replacement semantic candidate is therefore frozen as:

`P11 = 6352accc7962fc188976fc1bcea5e081681d99c5`

This later lifecycle descendant binds exact P11 in root `PROTOCOL-RELEASE-STATE.yaml` with Review reset to
`NOT_RUN`, stakeholder ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current
Protocol 6.4.

P10 remains immutable NO-PASS evidence. Binding/full workflow qualification of this descendant is required before
advancing the independent Review handoff to P11.

No independent Review, stakeholder ratification, public-fallback publication, recovery establishment, accepted-current
cutover, PR merge, or Protocol 7 mutation is authorized by this binding.


## 47. P11 binding qualification complete

Immutable P11 `6352accc7962fc188976fc1bcea5e081681d99c5` passed exact-candidate workflow run `36103358186`.

Binding descendant `0490ecb0c685b403df78f62f143896c44c078d68` passed normal workflow run `36103484871` with:

- candidate semantic ref: exact P11;
- Review: `NOT_RUN`;
- stakeholder ratification: `NOT_REQUESTED`;
- public fallback/recovery: `UNAVAILABLE`;
- accepted-current: Protocol 6.4;
- Protocol 7 D3/D4: unchanged.

Durable qualification records:

- `qualification/ssdp65/P11-REPAIR-QUALIFICATION.md`;
- `qualification/ssdp65/P11-FREEZE-BINDING.md`;
- `qualification/ssdp65/P11-BINDING-QUALIFICATION.md`.

The next authorized stage is a genuinely fresh independent assembled-candidate Review of exact P11. No stakeholder
ratification, publication, recovery, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.


## 48. P11 independent Review NO-PASS — canonical ancestry completeness remains unsound

Fresh independent assembled-candidate Review of immutable P11
`6352accc7962fc188976fc1bcea5e081681d99c5` issues **NO-PASS**.

Durable Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P11-NO-PASS.md`

### B65-P11-1 — non-shallow Git state can still be mistaken for complete canonical ancestry

P11 correctly fails closed for the authored shallow-history cases, but its negative ancestry proof remains too weak.

Two fresh real-Git holdouts falsify it:

1. a historical governed owner exists, but its historical blob is unavailable while commit/tree traversal remains
   non-shallow; `_release_state_at_ref(..., missing_ok=True)` converts the failed content read to
   `_MISSING_RELEASE_STATE`, and P11 returns "pre-owner";
2. a local Git replacement ref rewrites effective parents so the governed owner-introduction commit disappears from
   ordinary path-history traversal while `--is-shallow-repository` remains `false`.

Both are one causal defect: "no readable owner + non-shallow" is not proof of complete canonical pre-owner ancestry.

Accepted Protocol 6.5 D3 remains closed. Serious Challenge: none.

### Earliest owner and minimal repair boundary

Earliest owner: **D4 `source/release_state.py`**, at
`_release_state_at_ref(..., missing_ok=True)` and
`_lineage_has_governed_release_state()`.

Repair the existing classifier only:

- distinguish genuine path absence from unreadable/unavailable tree/blob/object state;
- fail closed whenever an object needed by the negative ancestry proof cannot be established;
- retain the shallow check as one incompleteness signal, not proof that a non-shallow repository is complete;
- make the negative proof use canonical ancestry rather than silently honoring local replace/graft overlays, or
  explicitly reject/fail closed when such an overlay is active;
- preserve all existing complete-history and shallow-history controls;
- do not add a second state owner, registry, transition mirror, topology service, compatibility layer,
  branch/default/latest/timestamp policy, candidate-specific logic, or universal history framework.

Required fresh production-resolver holdouts include non-shallow missing historical owner object, unreadable tree/path
object, partial/promisor/alternate object availability where supported, and replace/graft ancestry rewriting, in
addition to all P11 shallow and complete-history controls.

P11 remains immutable failed Review evidence. Any semantic repair creates a new candidate identity. Do not assign the
next P-number until the repair commit exists and exact-candidate normal CI passes. After that pass, a later descendant
may bind the new candidate with Review reset to `NOT_RUN`, rerun binding qualification, and require a fresh
independent assembled-candidate Review.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge,
or Protocol 7 D3/D4 mutation is authorized.


## 49. B65-P11-1 implementation — prospective replacement candidate

B65-P11-1 is repaired at the existing D4 release-state ancestry classifier without reopening accepted Protocol 6.5
D3.

The repair removes the unsound negative-proof shortcut rather than adding another completeness heuristic.

- Historical path membership is first inspected with canonical-tree `git --no-replace-objects ls-tree`. Only a
  successful tree lookup with no path entry means the owner is genuinely absent at that commit.
- If the path entry exists but its content cannot be read, validation fails closed. Unreadable/missing tree or blob
  objects are never converted to `_MISSING_RELEASE_STATE`.
- Canonical ancestry is walked from raw commit-object parent headers using
  `git --no-replace-objects cat-file -p`, rather than revision traversal affected by replacement refs or deprecated
  `info/grafts` overlays.
- A negative genuine-pre-owner conclusion is emitted only after the complete canonical parent graph has been traversed
  and every inspected historical state is either readable or structurally proven to lack the owner.
- Standard shallow clones now fail closed because raw boundary commits still name parent object IDs whose commit
  objects are unavailable. This retains the P11 shallow behavior without treating
  `--is-shallow-repository=false` as a universal completeness proof.

No registry, mirror, topology service, compatibility layer, branch/default/latest/timestamp policy, candidate-specific
identity, or second state owner is introduced.

Fresh real-Git production-resolver holdouts cover:

- non-shallow missing historical owner blob: fail closed;
- non-shallow missing historical tree: fail closed;
- replacement-ref ancestry that hides owner introduction: canonical history still rejects reintroduction;
- deprecated graft ancestry that hides owner introduction: canonical raw-parent history still rejects reintroduction;
- readable alternate object store: canonical ancestry remains usable and governed reintroduction is rejected;
- both existing P11 shallow-history negatives and all prior complete-history topology/recovery controls remain active.

This commit is only the **prospective replacement semantic candidate**. P11 remains immutable NO-PASS evidence. Do not
assign the next P-number until exact-candidate normal CI passes. After that pass, bind the exact repair SHA from a later
lifecycle descendant with Review reset to `NOT_RUN`, rerun binding qualification, and require another fresh
independent assembled-candidate Review.


## 50. P12 freeze and binding qualification complete

Prospective repair commit `c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6` passed exact-candidate normal workflow run `36121450601` across the complete
build and Orchestrator Core jobs.

The immutable replacement semantic candidate is therefore frozen as:

`P12 = c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`

Later lifecycle descendant `dc1595219ebfd76ee2451b406a549a4a012370e0` binds exact P12 in root `PROTOCOL-RELEASE-STATE.yaml` with Review
`NOT_RUN`, stakeholder ratification `NOT_REQUESTED`, public fallback/recovery `UNAVAILABLE`, and accepted-current
Protocol 6.4.

Binding workflow run `36121601230` passed both jobs completely.

Durable qualification records:

- `qualification/ssdp65/P12-REPAIR-QUALIFICATION.md`;
- `qualification/ssdp65/P12-FREEZE-BINDING.md`;
- `qualification/ssdp65/P12-BINDING-QUALIFICATION.md`.

B65-P11-1 is mechanically repaired and qualified at the existing D4 owner. Accepted Protocol 6.5 D3 remains closed.

The next authorized stage is a genuinely fresh independent assembled-candidate Review of exact P12.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR merge,
or Protocol 7 D3/D4 mutation is authorized.


## 51. P12 independent Review NO-PASS — bounded D4 reopen

Fresh independent assembled-candidate Review of exact immutable P12
`c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6` issues **NO-PASS**.

Durable Review evidence:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-25-PROTOCOL-6.5-P12-NO-PASS.md`

Immutable Review publication commit:

`042256b8ecfa390c58764ad6e795a39db231aab3`

Serious Challenge: **none**. Accepted Protocol 6.5 D3 remains closed. Reopen only the existing D4
`source/release_state.py` implementation scope for the two independently reproduced blockers below.

### B65-P12-1 — canonical ancestry authority is inconsistent across release-history predicates

P12 repairs canonical ancestry in the predecessor resolver, but `_check_ancestor()` still delegates to ordinary
`git merge-base --is-ancestor`. Fresh real-Git replace-ref and `info/grafts` holdouts show that a canonically false
Review/ratification/recovery/publication lineage can be made to appear true.

Repair contract:

- make all release-history ancestry predicates use the same canonical raw commit-parent authority already introduced
  by P12, or an equally bounded canonical helper;
- replacement refs and deprecated grafts must not redefine release-history ancestry;
- fail closed if required canonical commit objects are unavailable;
- preserve readable alternate/promisor-backed object use when required evidence resolves;
- add direct production holdouts for both `git replace` and `info/grafts` against the ancestor predicate and at
  least one real recovery/evidence lineage consumer;
- do not create a second topology registry, service, mirror, or branch/default/latest/timestamp authority.

### B65-P12-2 — governed owner deletion/reintroduction can be laundered by a later material transition

Fresh real-Git trajectory:

```text
A(owner/state A) -> D(owner absent) -> B(owner reintroduced/state B) -> C(later legal state C)
```

P12 rejects B when B is current, but at C it selects B as the immediate differing predecessor and stops that lineage.
The malformed A -> D -> B interval is therefore no longer inspected, and C validates with no ancestry error.

Repair contract:

- preserve immediate material-predecessor semantics for transition validation;
- independently establish history integrity behind every selected predecessor so no post-introduction owner-absence
  interval can be hidden by a later state transition;
- the A -> D -> B -> C trajectory above must fail at C;
- genuine pre-owner first introduction/merge, evidence-only descendants, ordinary consecutive transitions, equivalent
  and divergent merge parents, and parent-order/timestamp independence must remain valid;
- reuse P12's canonical raw-parent/path-presence machinery rather than adding a historical transaction registry or
  replay subsystem.

P12 remains immutable failed Review evidence. Any semantic repair creates a new immutable candidate identity. Do not
assign the next candidate number until the repair commit exists and exact-candidate normal CI passes. After that pass,
a later descendant may bind the new exact candidate at Review `NOT_RUN` and a genuinely fresh independent assembled-
candidate Review is required.

No stakeholder ratification, public-fallback publication, recovery establishment, accepted-current cutover, PR #33
merge, or Protocol 7 D3/D4 mutation is authorized.


## 52. B65-P12-1 / B65-P12-2 implementation — prospective replacement

The bounded P12 NO-PASS repair is implemented at the existing D4 owner without reopening accepted Protocol 6.5 D3.

### Canonical release-history ancestry

`_check_ancestor()` no longer delegates release authority to overlay-sensitive
`git merge-base --is-ancestor`. It now traverses the same raw canonical commit-parent graph used by the P12
predecessor resolver. Replacement refs and deprecated `info/grafts` therefore cannot redefine Review,
ratification, fallback, recovery, or publication ancestry.

Exact immutable evidence/version/recovery content reads now also use `--no-replace-objects`, preventing a local
replacement object from changing the bytes attributed to an immutable SHA.

### Continuous owner history

The predecessor resolver now performs one canonical path-presence continuity pass over reachable HEAD ancestry before
accepting an owner-present transition. The pass computes governance forward over the canonical DAG and rejects any
reachable commit that lacks `PROTOCOL-RELEASE-STATE.yaml` after at least one parent lineage was already governed.
This preserves genuine pre-owner branches while ensuring a malformed A(owner) -> D(absent) -> B(reintroduced) interval
cannot be hidden by a later material state C or evidence-only descendants.

No transition registry, replay engine, topology service, branch/default/latest/timestamp policy, candidate-specific
table, or second state owner is introduced.

Fresh real-Git production holdouts cover:

- replacement-ref sibling ancestry rejected by the canonical ancestor predicate;
- graft-rewritten sibling ancestry rejected by the canonical ancestor predicate;
- replacement-rewritten sibling recovery rejected by the real recovery-lineage consumer;
- immutable Review evidence content remains bound to the canonical commit under a replacement ref;
- governed A -> deletion -> reintroduced B -> later C -> evidence-only descendant remains rejected.

All prior P12 shallow/object-readability/alternate-store/topology/transition/recovery/parser/semver/evidence-binding
controls remain in the affected regression surface.

This commit is only a **prospective replacement semantic candidate**. P12 remains immutable NO-PASS evidence. Do not
assign the next candidate number until exact-candidate normal CI passes.
