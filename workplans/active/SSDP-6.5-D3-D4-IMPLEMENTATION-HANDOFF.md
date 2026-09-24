---
kind: implementation-workplan
workplan_id: SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF
protocol_version: 6.4.0
target_protocol_version: 6.5.0
status: authorized
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
D3 DESIGN: PASS
PHASE VI IMPLEMENTATION: AUTHORIZED
P1: NOT YET FROZEN
PUBLIC 6.5 FALLBACK: UNAVAILABLE
6.5 RECOVERY: UNAVAILABLE
6.5 RATIFICATION: NOT REQUESTED
ACCEPTED CURRENT: Protocol 6.4
PROTOCOL 7 D3/D4: UNCHANGED
```
