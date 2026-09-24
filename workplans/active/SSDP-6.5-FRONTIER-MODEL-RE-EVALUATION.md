---
kind: protocol-successor-workplan
workplan_id: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
protocol_version: 6.4.0
target_protocol_version: 6.5.0
subject_baseline: P0 = Protocol 6.4 at 55c085261eb827e3047637d045a8e6917ea6b962 (recovery 74bc572ef516cae417437a2027eeff52a2e25c15)
diagnostic_commit: 81375d8142a8130b80cd82f2304d3e16bc3fc390
status: active-p3-review-no-pass-repair-required
current_phase: PHASE VII P3 NO-PASS / D4 REPAIR REQUIRED / NEW CANDIDATE REQUIRED
branch: ssdp-6.5-frontier-model-re-evaluation
created_date: 2026-09-24
adjudication: qualification/ssdp65/CROSS-MODEL-ADJUDICATION-2026-09-24.md
active_serious_challenge: none against accepted D1-D4 doctrine
second_frontier_diagnostic: waived-for-this-cycle-by-stakeholder-resource-constraint
design_closure: qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md
implementation_handoff: workplans/active/SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md
independent_review: qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P3-NO-PASS.md
---

# Protocol 6.5 Frontier-Model Re-evaluation and Successor Workplan

## 1. Current disposition

```text
P0 CONTROL:                         FROZEN — 55c085261eb827e3047637d045a8e6917ea6b962
OPUS 5.5 PHASE I-III DIAGNOSTIC:    FROZEN — 81375d8142a8130b80cd82f2304d3e16bc3fc390
GPT-5.6 SOL HISTORICAL CROSS-CHECK: COMPLETE
CROSS-MODEL ADJUDICATION:           COMPLETE — qualification/ssdp65/CROSS-MODEL-ADJUDICATION-2026-09-24.md
SECOND FRONTIER DIAGNOSTIC:         WAIVED FOR THIS CYCLE; CLEAN BRANCH RESERVED FOR FUTURE REPLICATION
SUCCESSOR DECISION:                 PROTOCOL 6.5 WARRANTED
D1-D4 DOMAIN MODEL:                 PRESERVE
PHASE IV PRINCIPLE EXTRACTION:      COMPLETE — qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md
PHASE V CANDIDATE DESIGN:           COMPLETE — DESIGN PASS
PHASE VI IMPLEMENTATION:            REOPENED — P3 REVIEW BLOCKERS REQUIRE D4 REPAIR
P1 CANDIDATE:                       FROZEN / FAILED REVIEW — b565e28aeacea002cefe27e6b9594fe99d653c0a
P2 CANDIDATE:                       FROZEN / FAILED REVIEW — e8edb353e172aef933ed5e58eeabe897d0cc98d1
P2 EXACT PR QUALIFICATION:          PASS — run 35996488794\nP3 CANDIDATE:                       FROZEN — 89ccc71a7b0e9458a3e77306be2a773d4059f0f2\nP3 EXACT PR QUALIFICATION:          PASS — run 36018551068
PHASE VII QUALIFICATION/REVIEW:     NO-PASS — P3 IMMUTABLE / NEW CANDIDATE REQUIRED
PROTOCOL 7 D3/D4:                   OUT OF SCOPE / UNCHANGED
```

The frozen Opus findings remain evidence, not successor authority. The admitted defect set is the adjudicated four-family model below.

## 2. Governing objective

Produce a backward-compatible Protocol 6.5 that improves SSDP's reliable engineering intelligence by making the protocol obey its own ownership, evidence, convergence and representation principles.

The target is not more process. The target is fewer, stronger self-governance invariants with better evidence binding and lower accidental complexity.

Quality remains multidimensional: correctness, defect discovery, authority preservation, evidence quality, generalization, useful autonomy, structural simplicity and resource cost.

## 3. Accepted and preserved authority

6.5 SHALL preserve unless explicitly strengthened without semantic loss:

- D1 scientific/mathematical authority;
- D2 numerical/algorithm authority;
- D3 software-architecture authority;
- D4 specification/implementation authority;
- abstraction adequacy versus concretization fidelity;
- Serious Challenge as the route for materially defective accepted authority;
- evidence specification/realization/observation/assessment separation;
- stale-evidence and proxy-proof rules;
- PEM as non-authoritative project learning rather than D5;
- conditional PEM/HAS activation;
- frozen historical version/recovery/profile identity;
- public-source fallback distinct from recovery;
- progressive disclosure and Lossless Representation;
- bounded impact closure and preservation of unaffected siblings/evidence.

No Protocol 7 architecture change is authorized.

## 4. Admitted defect families

### DF-1 — Release-state/version lifecycle ownership

Current mutable lifecycle truth is copied into immutable/versioned semantic artifacts and many secondary surfaces. The same defect family was seen by historical Sol reviews and remains in accepted P0.

Required end state:

1. Separate **version-intrinsic semantics** from **mutable repository release state**.
2. Establish one current release-state owner for accepted-current version, ratification state, public fallback mapping and recovery mapping.
3. Version-bound immutable source/package/profile SHALL NOT assert mutable current lifecycle truth except explicitly time-scoped historical snapshot facts.
4. Secondary current surfaces SHALL reference or be generated from the owner rather than hand-copy values.
5. Preserve bootstrap/recovery distinction.
6. Reorder successor publication so the final public fallback source is not published until the exact semantic candidate has passed independent assembled-candidate Review and required stakeholder ratification.
7. Publish mapping identities only from later descendants when Git self-reference requires it.
8. Recovery remains a distinct later immutable acceptance/rollback identity.
9. Protocol-version acceptance requires explicit stakeholder ratification; Review PASS establishes technical eligibility only.
10. If 6.5 is materially delayed, repair P0 A-01 current-state contradictions as a separate 6.4.x patch rather than leaving known false current surfaces indefinitely.

Design constraint: prefer an existing owner plus generated/reference projections. If one small machine-readable release-state artifact is necessary to eliminate multiple hand-maintained owners, it is allowed only if it becomes the single current owner rather than another mirror.

### DF-2 — Qualification and Review epistemology

Required end state:

1. Distinguish three evidence classes:
   - structural/executable consistency;
   - semantic adequacy/conformance;
   - engineering-outcome improvement.
2. Every qualification result names its exact subject and property.
3. Mechanical tests SHALL NOT claim arbitrary prose semantic correctness.
4. Exact wording pins are retained only for actual syntax/public/machine contracts.
5. Synthetic QF-style fixtures may test executable predicates, but passing their own fixture matrix cannot qualify the prose authority they model.
6. Semantic qualification is performed by independent Review of the assembled candidate, including concrete counterexamples and actual owner/consumer paths.
7. Every protocol Review includes an **out-of-matrix abstraction-adequacy pass**: search for a locally compliant/global-failure trajectory not represented by the author workplan, obligation matrix or tests.
8. Review must explicitly challenge the adequacy of the qualification method itself.
9. Claims that 6.5 improves engineering behavior require targeted matched P0/P1 task evidence; ordinary patch releases do not inherit a mandatory large A/B benchmark program.
10. Protocol-level semantic mutation evaluation is split: machine-readable/state/schema mutants go to executable tests; prose semantic mutants go to fresh independent semantic Review.

Forbidden solution: universal prose theorem prover, ontology database, semantic registry, or broad exact-string pinning introduced merely to raise a mutation-detection percentage.

### DF-3 — Meta-control semantics and governance

Add one canonical, compact definition for each high-leverage control predicate and route all domain-local consequences to it.

Required definitions/contracts:

- **material/materially**: decision-local significance where a plausible change under the governed scope can alter interpretation, admissibility, evidence applicability, acceptance/reopen state, protected risk or outcome; remote speculative possibility alone is insufficient.
- **independent Review/falsification**: context/reviewer did not author the candidate and does not inherit author conclusions; different model family is stronger corroboration but not mandatory.
- **Serious Challenge threshold**: requires concrete contradiction, counterexample, materially consequential ambiguity/incompatibility, or admissible evidence that accepted authority may be inadequate; mere possibility does not qualify.
- **Challenge resolution**: the owning authority resolves/adjudicates; ambiguity-narrowing clarification is semantic when it narrows materially admissible behavior and therefore triggers applicable impact/evidence closure.
- **protocol-version acceptance**: independent Review PASS -> technically eligible; explicit stakeholder ratification -> accepted decision; publication automation represents but does not manufacture acceptance.
- **accepted PEM base/publication policy**: explicit project integration identity; never default/latest/file-presence/self-declaration.

Do not create a closed ontology of all protocol predicates. Define only predicates that materially gate behavior.

### DF-4 — Representation/schema/convergence self-application

Required end state:

1. Add the invariant that SSDP development is itself governed by accepted SSDP ownership/evidence/representation/convergence rules, except explicit bounded version-bootstrap exceptions.
2. Integrate current 6.4 release-labelled amendment sections into their canonical owner sections; move historical rationale to history rather than keeping amendment replay in hot current doctrine.
3. Remove stale predecessor version labels from current role metadata, templates and current navigation.
4. Avoid hardcoded current-version labels in generic role descriptions when protocol/profile identity already carries the version.
5. Collapse duplicated generic PEM activation/routing predicates to canonical owner + local consequence where possible.
6. Reconcile PEM doctrine, template, validator and tests. Executable-required fields/relations either become documented schema semantics or are removed/narrowed from executable enforcement.
7. Reconcile the repository's self-hosted PEM from its stale 6.2/6.3 basis through the accepted 6.4 interval and the 6.5 work, including applicable positive and negative learning.
8. Cross-workplan current-version/fallback copies are replaced by owner references where the consumer does not semantically require a frozen value.
9. Measure always-loaded context and duplication before/after. Target no increase in the always-loaded kernel relative to P0; any necessary added definition must be paid for by integration/removal of equal-or-larger duplicate/amendment text unless losslessness proves otherwise.
10. Do not remove PEM temperature/maturity machinery in 6.5 solely because this repository has not exercised it; A-13 remains deferred pending downstream evidence.

## 5. Phase IV — Principle extraction and design closure

Before normative source mutation, produce a design record that proves coverage/exclusion/generalization for these principles:

### P65-1 — Self-application
The protocol's own release engineering is subject to the same owner/evidence/representation/convergence rules it imposes downstream.

### P65-2 — State/semantics separation
Mutable release state is not version-intrinsic protocol semantics.

### P65-3 — Evidence-claim congruence
No evidence class may claim more than the property and subject it actually discriminates.

### P65-4 — Review abstraction adequacy
Independent Review tests both candidate conformance and whether the author's decomposition/qualification is itself strong enough.

### P65-5 — Minimal meta-governance
Materiality, independence, Challenge resolution, acceptance authority and accepted-memory publication are explicit; no unnecessary new control ontology is introduced.

### P65-6 — Integrated current representation
Accepted release amendments are folded into current owners; history remains cold/discoverable; generated/executable schema cannot become a second owner.

For each principle record:
- admitted findings covered;
- old rules subsumed;
- counterexamples excluded;
- newly permitted behavior;
- compatibility consequences;
- affected canonical owners;
- evidence required for qualification;
- ablation case that should regress if the principle is removed.

Gate status: **SATISFIED.** All six principles are closed in `qualification/ssdp65/PHASE-IV-V-DESIGN-CLOSURE.md`; no unresolved owner conflict or Serious Challenge remains. Phase VI is authorized under `workplans/active/SSDP-6.5-D3-D4-IMPLEMENTATION-HANDOFF.md`.

## 6. Phase V — Candidate design contract

The design SHALL map changes to canonical owners before implementation.

Expected affected owners/surfaces:

- universal kernel / abstraction-concretization owner;
- protocol versioning/compatibility owner;
- workflow/workplan/Challenge lifecycle owner;
- testing/validation owner;
- evidence owner where qualification terminology requires alignment;
- convergence/cycle-economy owner;
- PEM owner + template + validator;
- development workflow prompts;
- role/specialist frontmatter/routing text;
- generic plan/handoff templates whose current labels/contracts are stale;
- build/generation/parity tests and current protocol snapshot;
- root project routing/current-state surfaces only as derived/reference projections;
- self-hosted PEM and semantic history;
- Protocol 7 inheritance identity only after 6.5 acceptance, with no D3 architecture mutation.

A 6.4 -> 6.5 preservation/supersession map is mandatory before candidate freeze.

## 7. Phase VI — Implementation order

Implement in dependency order, preferring removal/rewiring over additive machinery:

1. canonical definitions/self-application and owner boundaries;
2. release-state/versioning lifecycle architecture;
3. Challenge/acceptance/PEM-basis governance;
4. qualification/Review semantics and executable oracle cleanup;
5. PEM schema/template/validator reconciliation;
6. representation integration/compression and template/role cleanup;
7. generator/package/profile updates from canonical sources;
8. self-hosted PEM + history reconciliation;
9. tests/qualification instruments at real owners;
10. generated descendants only after canonical source is coherent.

Do not edit generated artifacts as independent fixes.

## 8. Phase VII — Qualification

### 8.1 Mandatory structural/current-state evidence

- inherited repository regression;
- PEM validator after schema reconciliation;
- canonical package build + independent validation;
- committed distribution parity;
- generated current snapshot parity;
- frozen 5.16-6.4 historical profile/resource identity;
- full Orchestrator Core affected regression;
- whitespace/presentation checks;
- one-current-release-state coherence across every declared projection;
- negative fixtures proving stale/contradictory lifecycle projections fail;
- PEM doctrine/template/validator parity checks;
- no exact-wording false-positive test for meaning-preserving paraphrases unless wording is itself contract.

### 8.2 Semantic falsification

Use a fresh context that did not author P1.

Required passes:

1. all four admitted defect families;
2. locally-compliant/global-failure counterexamples;
3. owner-conflict and current-vs-history;
4. semantic Review of a fresh post-freeze mutation/counterexample set authored by a non-P1-author context;
5. explicit attempt to find a defect outside the workplan/qualification matrix;
6. preservation map falsification;
7. ablation of each major P65 principle on at least its motivating counterexample.

The semantic reviewer, not the ordinary mechanical suite, decides arbitrary prose semantic mutations.

### 8.3 Targeted P0/P1 behavior comparison

Because 6.5 is explicitly an intelligence-uplift release, run matched P0/P1 trials on at least four representative difficult tasks spanning:

- lifecycle/current-state drift;
- proxy/oracle adequacy;
- authority/Challenge routing;
- mature-system simplification/review convergence.

Use the same task/model/tool budget per pair. GPT-5.6 Sol is the historical control model. Opus 5.5 is the frontier evaluator when budget permits; if frontier paired trials cannot be completed, report that limitation and do not make quantitative frontier-performance claims.

Replicate only stochastic/ambiguous cases where another realization can change the bounded decision. Do not mechanically require three repeats of deterministic or already decisive cases.

Reserve at least one historical/novel task family not used to design P1.

### 8.4 Simplicity evidence

Compare P0/P1:

- always-loaded kernel/context words;
- duplicated generic rule/value copies;
- number of release lifecycle stages and hand-maintained state projections;
- exact-string semantic pins;
- current-owner/schema duplications.

6.5 must not solve the defects by net proliferation of parallel authorities.

## 9. Phase VIII — Independent assembled-candidate Review and ratification

Final Review must be performed in a fresh context that did not author P1. Opus 5.5 is preferred when resource is available because it supplied the frontier diagnostic; GPT-5.6 Sol may provide an additional historical/control review but is not a substitute for labeling the evidence honestly.

Review receives:
- P0;
- immutable P1;
- preservation/supersession map;
- adjudication record;
- qualification evidence;
- holdout/ablation evidence;
- exact known limitations.

It must not inherit author conclusions.

A PASS means technically eligible for acceptance. Protocol 6.5 becomes accepted only after explicit stakeholder ratification.

## 10. Publication/cutover lifecycle for 6.5

The 6.5 lifecycle SHALL avoid the pre-Review immutable-fallback trap:

1. implement and qualify a self-reference-safe semantic candidate;
2. freeze exact P1;
3. perform independent assembled-candidate Review;
4. obtain explicit stakeholder ratification of the reviewed semantics;
5. only then publish the exact reviewed source candidate as the version-bound public fallback from a later descendant;
6. establish a distinct immutable recovery target containing the required accepted review/ratification/publication lineage;
7. publish recovery mapping from a later descendant;
8. regenerate/reconcile current mutable release-state projections and packages;
9. rerun affected recovery/package/profile/Core/current-state acceptance;
10. update Protocol 7 inheritance identity only, preserving Protocol 7 D3 architecture;
11. closeout learning and archive the 6.5 workplan only after the current-state repository is coherent.

Any material semantic change after Review reopens Review and invalidates the would-be public fallback candidate.

## 11. Benchmark design correction

The original preregistration remains preserved, but its §4.6/§6.4 interpretation is repaired before P1 design:

- arbitrary prose semantic mutants are not required to be detected by the ordinary mechanical test suite;
- mechanical mutation detection is required for machine-readable/state/schema/generated invariants;
- arbitrary semantic mutants are evaluated by independent semantic Review of the assembled candidate;
- paraphrase false positives remain defects when exact wording is not a contract;
- fixed three-fold replication is replaced by proportional replication of stochastic/ambiguous paired trials.

See the dated amendment appended to `qualification/ssdp65/BENCHMARK-AND-EVALUATION-DESIGN.md`.

## 12. Project Engineering Memory / HAS

PEM remains activated for this mature rework.

Current applicable lessons:

- FF-001: premature immutable fallback publication — applicable, but 6.5 repairs the structural cause by moving final fallback publication after semantic Review/ratification.
- PC-001: frozen predecessor preservation — binding capability to preserve.
- SP-001: repair canonical owners then regenerate derivatives — binding as evidence-backed engineering guidance.

The self-hosted PEM itself is stale and must be reconciled during implementation. Until then, absence remains non-evidence and the current HAS retains explicit basis uncertainty.

## 13. Non-goals

- no redesign of D1-D4 scientific/software authority;
- no Protocol 7 architecture or D4 implementation;
- no universal semantic parser, theorem prover, registry or ontology;
- no requirement that mechanical tests understand arbitrary prose;
- no merge of public fallback and recovery identities merely for simplicity;
- no removal of PEM maturity/temperature machinery without downstream evidence;
- no rewriting of frozen historical artifacts;
- no broad unrelated repository refactor;
- no permanent large multi-model benchmark mandate for ordinary patch releases.

## 14. Closure criteria

This workplan closes only when:

1. P65-1..P65-6 are implemented losslessly;
2. all admitted DF-1..DF-4 defects are closed or explicitly narrowed with evidence;
3. A-13 remains explicitly deferred rather than accidentally removed;
4. preservation/supersession mapping is complete;
5. structural/current-state/schema/generated/frozen-resource evidence passes;
6. semantic falsification and out-of-matrix Review pass;
7. targeted P0/P1 evidence supports at least one material improvement without unacceptable correctness/authority regression;
8. final fresh assembled-candidate Review passes;
9. stakeholder explicitly ratifies 6.5;
10. public fallback/recovery/cutover are published in the corrected order;
11. current release-state projections and self-hosted PEM are reconciled;
12. Protocol 7 inheritance is updated without D3 mutation;
13. remaining limitations are recorded honestly.

## 15. Reopen triggers

- a proposed simplification loses an accepted 6.4 capability;
- lifecycle design reintroduces mutable current-state claims into immutable fallback payload;
- mechanical qualification again becomes the de facto semantic owner;
- implementation introduces a parallel release-state/schema authority;
- evidence shows a P65 principle increases authority violations or false blockers;
- a fresh semantic mutation/counterexample defeats P1;
- accepted P0/main materially changes before candidate comparison and applicability is not explicitly rebound.


## 16. 2026-09-24 fresh independent Review reopen

Fresh assembled-candidate Review of immutable P1 b565e28aeacea002cefe27e6b9594fe99d653c0a issued NO-PASS with no Serious Challenge. P1 remains immutable and is the failed Review subject.

### R65-1 — bind Review evidence to the exact candidate in the real state validator

Owner: D4 release-state validation.

Repair source/release_state.py and focused tests so PASS/NO_PASS evidence is not accepted by regex shape alone. Resolve the immutable evidence route in this repository, require commit/path existence, require the Review record’s machine-readable candidate identity to equal candidate.semantic_ref, and require disposition/state agreement. Add wrong-candidate, nonexistent-path/commit, wrong-repository and state-mismatch negatives plus a valid exact binding. Do not machine-judge arbitrary Review prose and do not add a parallel evidence registry.

### R65-2 — remove live mutable phase values from long-lived tests

Owner: D4 testing/qualification.

Remove hardcoded live assertions that Review is NOT_RUN, ratification NOT_REQUESTED and publication/recovery UNAVAILABLE from tests that read the mutable owner. Keep state-machine legality and current-file coherence at the release_state owner; exercise legal/illegal transitions using copied lifecycle-independent fixtures. Freeze-time phase facts remain in immutable qualification records. No synchronized phase table or compatibility wrapper.

### R65-3 — remove predecessor-version gates from current 6.5 workflow semantics

Owner: D4/current workflow representation.

In source/shared/references/development-workflow-prompts.md, remove predecessor-only “Protocol 6.4” conditions from inherited D4 exact-contract, Review, Verification, Stabilization, audit and closeout duties. State them as current/generic obligations with the existing materiality triggers. Perform a bounded search of current non-historical operational source for equivalent predecessor-version guards. Regenerate the 6.5 prompt/profile from canonical source. Preserve history in history/archive only.

### Candidate/evidence reset

These repairs change the reviewed semantic/qualification representation. They MUST NOT modify P1 and continue calling it P1.

After R65-1..R65-3:
1. run focused D4 tests and full affected repository acceptance;
2. reconcile preservation/current-state/simplicity evidence;
3. freeze a new semantic candidate SHA;
4. bind that new SHA from a later lifecycle descendant;
5. reset candidate Review to NOT_RUN for the new candidate; ratification remains NOT_REQUESTED; public fallback/recovery remain UNAVAILABLE;
6. rerun fresh post-freeze mutation/counterexample evidence, affected matched P0/new-candidate comparison and exact-candidate normal PR CI;
7. perform a new fresh independent assembled-candidate Review.

Exact-P1 runs 35985539212 / 35985871148 and descendant run 35986452433 remain historical evidence for their exact subjects only.


## 17. P2 repair closure and handoff

The D4 repair ordered by the P1 independent Review is complete.

- B65-R1: closed by real immutable Review-evidence route resolution and exact candidate/disposition binding in the existing release-state validator.
- B65-R2: closed by removing live candidate-phase copies from long-lived tests; the inherited Protocol 6.4 sibling phase oracle was repaired under the same defect family.
- B65-R3: closed by removing predecessor-version gates from current workflow semantics and regenerating the 6.5 prompt/profile from canonical source.
- D3: not reopened.
- Serious Challenge: none.

Exact replacement candidate:

`e8edb353e172aef933ed5e58eeabe897d0cc98d1`

Exact normal PR qualification:

`35996488794` — PASS.

Durable repair evidence: `qualification/ssdp65/P2-REPAIR-QUALIFICATION.md`.
Freeze binding: `qualification/ssdp65/P2-FREEZE-BINDING.md`.
Current Review handoff: `qualification/ssdp65/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.5.md`.

P1 remains an immutable failed candidate. A fresh non-authoring context must independently Review P2 before any stakeholder ratification/publication/recovery/cutover action.


## 18. 2026-09-24 fresh independent P2 Review reopen

Fresh assembled-candidate Review of immutable P2 \`e8edb353e172aef933ed5e58eeabe897d0cc98d1\` issued **NO-PASS** with no Serious Challenge. P2 remains immutable and is now historical failed-candidate evidence.

Durable Review:
\`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P2-NO-PASS.md\`

### R65-P2-1 — finish removal of mutable lifecycle values from inherited tests

Owner: D4 testing/qualification.

The P2 repair changed the direct Protocol 6.5 phase oracle and one Protocol 6.4 sibling, but the same family remains in:

- \`tests/test_protocol_64_bootstrap_readiness.py\`: live \`accepted_current == 6.4.0\` plus current 6.4 public/recovery assertions;
- \`tests/test_protocol_61_evidence_evolution.py\`: live \`accepted_current == 6.4.0\` and \`candidate.version == 6.5.0\`.

Remove only mutable phase copies. Preserve immutable historical release identities and generic release-state-owner routing. Add legal transition fixtures that advance accepted-current to 6.5 and later candidate identity without requiring inherited test edits. Perform a bounded test census for equivalent live current/candidate values. Do not add a synchronized phase table or wrapper.

### R65-P2-2 — bind terminal ratification evidence to exact candidate/disposition

Owner: D4 release-state validation.

The accepted P65 design requires RATIFIED only from explicit stakeholder evidence for the exact reviewed semantic ref. P2 validates only immutable route existence for terminal ratification evidence.

Extend the existing validator with minimal structured binding: terminal RATIFIED/REJECTED evidence must resolve in the project and bind exact \`candidate.semantic_ref\` plus matching terminal disposition. Actual stakeholder authorization remains a human/semantic decision; do not machine-judge arbitrary prose. Add valid binding and wrong-candidate/disposition/repository/commit/path negatives. Do not add a registry, mirror, semantic parser, or new authority.

### Candidate/evidence reset

Any repair changes executable/semantic acceptance behavior and therefore requires a new immutable candidate identity; never mutate P2 and continue calling it P2.

Rerun:
1. focused lifecycle/release-state tests including legal transition counterexamples;
2. complete repository build and Orchestrator Core workflow on the new candidate;
3. affected Phase VII lifecycle mutation set, P65 ablations, and P0/new-candidate matched lifecycle/oracle comparison;
4. simplicity/preservation applicability checks;
5. new freeze/binding qualification with Review reset to NOT_RUN;
6. fresh independent assembled-candidate Review.

Exact-P2 runs \`35996488794\`, \`35996817388\`, and \`35996964858\` remain historical evidence for their exact subjects only. Frozen-resource and unchanged D1/D2/formal-definition evidence may be reused only after applicability is re-established.


## 19. P3 repair closure and fresh-Review handoff

The D4 repair ordered by the P2 independent Review is complete without reopening D3.

### B65-P2-1 closure — lifecycle test ownership

- \`tests/test_protocol_64_bootstrap_readiness.py\` now resolves immutable Protocol 6.4 release identity from \`accepted_current\` while 6.4 is current and from \`historical["6.4.0"]\` after succession.
- The same test includes a successor-cutover fixture proving the 6.4 identity survives an owner-only 6.5 cutover shape.
- \`tests/test_protocol_61_evidence_evolution.py\` no longer pins live accepted-current or candidate versions; its historical 6.2 assertions are explicitly exercised under a future accepted/candidate version shape.
- A bounded census of all current \`tests/*.py\` found no other invalid live \`accepted_current\` / \`candidate\` version copies. Remaining 6.4/6.5 literals are version-intrinsic, frozen historical, synthetic state-machine fixtures, or current source-version checks.

No synchronized lifecycle table/helper/state mirror was added.

### B65-P2-2 closure — terminal ratification evidence binding

The existing \`source/release_state.py\` owner now uses the same immutable route/front-matter mechanism for terminal stakeholder-ratification evidence and requires:

- same-repository immutable commit/path resolution;
- safe repository-relative path;
- exact candidate semantic-ref binding;
- terminal disposition agreement for \`RATIFIED\` versus \`REJECTED\`.

Actual stakeholder authorization remains a human/semantic decision; the validator does not parse arbitrary ratification prose or infer intent.

Candidate binding metadata is generalized to \`candidate_ref\` / \`semantic_ref\` plus historical \`pN\` compatibility rather than hard-coding P1/P2 names.

### Exact P3 evidence

P3 = \`89ccc71a7b0e9458a3e77306be2a773d4059f0f2\`.

Normal PR workflow run \`36018551068\` evaluated exact P3 and passed:

- repository release-state validation;
- PEM validation;
- complete protocol regression;
- canonical package build;
- independent package validation;
- committed distribution parity;
- whitespace;
- packaged Protocol 6.5 snapshot parity;
- Orchestrator Core acceptance.

P3 remains immutable. This later lifecycle descendant binds P3 with Review \`NOT_RUN\`, ratification \`NOT_REQUESTED\`, public fallback \`UNAVAILABLE\`, recovery \`UNAVAILABLE\`, and accepted-current Protocol 6.4.

Binding descendant `c3df40cdb144c66a390b5d69b49e6fe8a81ad825` passed normal workflow run `36018970303`; this confirms the mutable P3 binding representation is mechanically coherent without altering P3.

The next step is a fresh independent assembled-candidate Review of P3. P1 and P2 NO-PASS conclusions remain historical evidence only and must not be inherited as the P3 verdict.


## 20. 2026-09-24 fresh independent P3 Review reopen

Fresh independent assembled-candidate Review of immutable P3 `89ccc71a7b0e9458a3e77306be2a773d4059f0f2` issued **NO-PASS** with no Serious Challenge.

Durable Review:

`qualification/ssdp65/INDEPENDENT-REVIEW-2026-09-24-PROTOCOL-6.5-P3-NO-PASS.md`

P3 remains immutable. B65-P2-1/B65-R2 lifecycle-copy repair is closed, and the original B65-R3 workflow predecessor gate is closed. Two blockers remain at existing D4/current-representation owners.

### R65-P3-1 — make evidence subject identity unambiguous

Owner: existing D4 release-state evidence validation in `source/release_state.py`.

The shared `_bound_candidate_refs` set-membership rule is too permissive. If the target candidate appears in any `candidate_ref`, `semantic_ref` or `pN` field, the record is accepted even when another field identifies a different actual subject. This affects both Review and terminal ratification.

Repair by altering the existing binder only:

- resolve exactly one machine-readable evidence subject;
- when `candidate_ref` and/or `semantic_ref` are present, require all explicit subject fields to agree and equal the state `candidate.semantic_ref`;
- keep legacy `pN` compatibility only through a bounded unambiguous rule; comparator/control/history `pN` metadata must not become alternate reviewed subjects;
- reject ambiguous multiple candidate-subject fields instead of accepting set membership;
- do not inspect arbitrary Review/ratification prose and do not add a registry, mirror, compatibility subsystem or semantic parser.

Required focused cases:

- exact candidate + PASS/NO-PASS;
- exact candidate + RATIFIED/REJECTED;
- wrong candidate;
- disposition mismatch;
- explicit `candidate_ref` conflict with matching historical `p3`;
- explicit `semantic_ref` conflict with matching historical `p3`;
- multi-`pN` record where historical P3 and future P4 coexist;
- future P4 as the sole/unambiguous subject;
- wrong repository, unsafe path, missing commit/path and malformed front matter.

### R65-P3-2 — remove predecessor scope from the current evidence owner

Owner: current canonical `source/shared/references/evidence-evolution-and-dependencies.md` representation under accepted P65-6.

Replace the residual current statement `Protocol 6.4 remains document-controlled` with protocol-current/generic wording that preserves the same no-universal-graph meaning. Perform a bounded sibling scan for predecessor-qualified normative scope in current non-historical canonical source. Do not add a new section/table/version adapter.

Regenerate affected package descendants from canonical source and rerun parity. Frozen 5.16-6.4 resources must remain byte-identical.

### Candidate/evidence reset

Any repair changes current executable/semantic representation and therefore requires a new immutable candidate identity. Never mutate P3 and continue calling it P3.

Rerun, proportionately:

1. focused release-state/evidence-binding tests including the new ambiguity negatives;
2. current-representation/predecessor-scope census;
3. source -> generated/package/profile parity and full inherited regression;
4. Orchestrator Core acceptance;
5. affected preservation/P65-3/P65-6 ablations and fresh semantic mutants;
6. hot-current measurement after the one-line owner repair;
7. exact-new-candidate normal PR CI;
8. new freeze/binding qualification with Review reset to NOT_RUN and ratification NOT_REQUESTED;
9. a new fresh independent assembled-candidate Review.

Exact P3 runs `36018551068`, `36018970303` and `36019184556` remain historical evidence for their exact subjects/properties only. No stakeholder ratification/publication/recovery/cutover/merge/Protocol-7 mutation is authorized.
