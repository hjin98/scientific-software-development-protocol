---
kind: implementation-workplan
workplan_id: SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: reopened-p5-review-repair-required
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
