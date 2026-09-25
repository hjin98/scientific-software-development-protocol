---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6
semantic_ref: c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6
binding_descendant: dc1595219ebfd76ee2451b406a549a4a012370e0
readiness_descendant: 93ff388587cbb49a80a9758475a910b05a63f634
exact_candidate_run: 36121450601
binding_run: 36121601230
readiness_run: 36121836579
serious_challenge: none
blocking_findings:
  - B65-P12-1
  - B65-P12-2
historical_capability_preservation: no-pass-d4-lifecycle-only
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P12

## 1. Disposition

**NO-PASS.**

The semantic Review target is exact immutable P12:

`c6a0e9b2ad54fd2cea39bc9a4a1a480c0b9c25f6`

against accepted Protocol 6.4 control P0:

`55c085261eb827e3047637d045a8e6917ea6b962`.

The later binding/readiness descendants were used only for mutable lifecycle and qualification evidence. They were not substituted for P12.

Two genuine D4 blockers survive fresh independent falsification:

1. **B65-P12-1 — canonical Git ancestry is not used consistently by all release-history lineage predicates.**
   P12's repaired predecessor resolver uses raw commit parents and suppresses replacement objects, but shared
   `_check_ancestor()` still delegates to ordinary `git merge-base --is-ancestor`. A local `git replace` ref or
   deprecated `info/grafts` overlay can therefore make a canonically false Review/ratification/recovery/publication
   lineage appear true.
2. **B65-P12-2 — an illegal governed-owner deletion/reintroduction can be laundered by one later material transition.**
   The direct reintroduction commit is rejected when it is HEAD, but once a later legal state C follows the
   reintroduced state B, `_previous_governed_release_states()` stops at B because B differs from C. It never reaches
   the missing-owner parent behind B, so B -> C validates with no error and the governed deletion interval disappears.

No Serious Challenge is raised. Accepted Protocol 6.5 D3 is coherent, jointly concretizable, and remains closed.
Both defects are in the existing D4 release-state implementation.

P12 remains immutable. Any semantic repair requires a new immutable candidate identity.

## 2. Independence and evidence boundary

This Review reconstructed applicable authority and current behavior independently before using prior Review records as
hypothesis/evidence sources.

Inspected subjects included:

- accepted P0 and exact P12 identities;
- accepted Protocol 6.5 D3 design closure and D3->D4 handoff;
- exact P12 production `source/release_state.py` call paths;
- exact P12 tests;
- current root `PROTOCOL-RELEASE-STATE.yaml`;
- P12 repair/freeze/binding qualification;
- exact-candidate, binding, and readiness workflow results;
- current PEM and its accepted-base/candidate-overlay metadata;
- frozen historical profiles/prompts;
- current canonical/generated/Core identities;
- Protocol 7 D3/D4 artifacts;
- prior failed-candidate Reviews only as bounded historical evidence.

Mechanical workflow evidence is green:

- exact P12 run `36121450601`: build PASS, Orchestrator Core PASS;
- binding run `36121601230`: build PASS, Orchestrator Core PASS;
- readiness run `36121836579`: build PASS, Orchestrator Core PASS.

Those runs establish only properties their actual oracles discriminate. They do not establish semantic Review PASS.

## 3. Serious Challenge pass

**SERIOUS CHALLENGE: NONE.**

Accepted Protocol 6.5 D3 already requires:

- one mutable release-state owner;
- lifecycle state separated from version-intrinsic semantics;
- exact Review/ratification subject binding;
- public fallback distinct from later recovery;
- immutable historical mappings;
- continuous release-state transactions;
- evidence-bounded negative history claims;
- Review abstraction adequacy and out-of-matrix falsification;
- no branch/default/latest/timestamp authority;
- no second topology/state authority.

The two findings below do not show contradiction, ambiguity, inadequacy, or unrealizability in those requirements.
They show that P12's D4 concretization does not fully realize them.

Earliest owner for both blockers: **D4 `source/release_state.py`**.

## 4. Mandatory B65-P11-1 repair falsification

P12 materially improves P11:

- tree membership is checked separately from owner-content readability;
- unreadable tree/blob/path evidence fails closed;
- raw commit objects define parent identities;
- replacement objects are disabled in the repaired resolver;
- raw parent parsing bypasses deprecated graft traversal overlays;
- negative pre-owner classification requires exhaustive traversal of the canonical parent graph visible to that resolver;
- standard shallow boundaries fail closed when raw parent objects are unavailable;
- readable alternate object stores remain usable.

A fresh **non-shallow missing canonical parent-commit** holdout beyond the authored P12 additions also failed closed:
the raw parent SHA remained in the child commit but the required parent commit object was unavailable. The production
resolver could not resolve that parent and emitted the genuine-pre-owner incompleteness error rather than returning a
negative ancestry proof.

Therefore the narrow P11 defect in the new resolver is repaired.

However the assembled release-history mechanism is still NO-PASS because canonical-history discipline is not applied
consistently to `_check_ancestor()` (B65-P12-1), and the predecessor boundary is not history-complete across an
already-malformed deletion/reintroduction interval (B65-P12-2).

## 5. Fresh real-Git holdout A — replacement overlay falsifies `_check_ancestor()`

A temporary real Git repository was constructed with:

```text
base
 |\
 L R
```

where L and R are canonical siblings. Canonically, L is **not** an ancestor of R.

A replacement commit for R was then installed with L as its parent:

```text
git replace R replacement-R(parent=L)
```

Observed:

```text
canonical --no-replace-objects merge-base --is-ancestor L R -> false
P12 _check_ancestor-style ordinary merge-base --is-ancestor L R -> true
```

Thus a local replacement ref can redefine the ancestry consumed by P12's Review/ratification/recovery/publication
lineage checks even though the repaired predecessor resolver itself is canonical.

A companion real-Git graft holdout showed the same class and a stronger detail:

```text
ordinary merge-base --is-ancestor L R              -> true
--no-replace-objects merge-base --is-ancestor L R -> true
raw cat-file parent of R                           -> canonical base
```

So merely adding `--no-replace-objects` to `merge-base` would not close deprecated `info/grafts`; the canonical
ancestor relation must reuse raw commit-parent authority or explicitly fail closed on traversal overlays.

### B65-P12-1

**Finding:** release-history authority is split between canonical raw-parent traversal and overlay-sensitive revision
traversal.

**Affected production paths:** `_check_ancestor()` as used by Review evidence lineage/publication, ratification
lineage/publication, public fallback publication, and recovery lineage/publication.

**Consequence:** a stale, sibling, or otherwise wrong canonical target can be made to satisfy a lineage predicate under
local replace/graft state. Branch name, timestamps, and candidate number remain irrelevant; the defect is local Git
topology overlay becoming authority.

**Minimum repair boundary:** replace `_check_ancestor()`'s revision-walk authority with the existing canonical
raw-parent mechanism (or one equally bounded canonical helper) so replacement refs and grafts cannot redefine any
release-history ancestry predicate. Do not add a second topology registry/service.

## 6. Fresh real-Git holdout B — deletion/reintroduction laundering after a later transition

A second temporary real Git repository exercised the exact P12 predecessor algorithm with:

```text
A : governed owner present, state A
D : owner deleted
B : owner reintroduced, state B
C : later ordinary material transition, state C (HEAD/current)
```

P12 correctly rejects B when B itself is the current committed state: B's missing-owner parent D is examined and its
ancestry exposes A.

But at C the production predecessor loop observes immediate parent B, sees `state(B) != state(C)`, records B as the
material predecessor, and stops descending that lineage. The D/A interval is never inspected.

Fresh observed result at C:

```text
errors = []
predecessors = [B]
```

A valid B -> C transition can therefore pass while the repository history contains the forbidden A -> D -> B governed
owner deletion/reintroduction.

### B65-P12-2

**Finding:** transition validation is locally correct but non-compositional across a malformed earlier material
boundary.

**Consequence:** one later valid material transition can erase evidence of an illegal governed interval from the
current acceptance path. This violates transition continuity, one-owner lifecycle integrity, self-application, and the
explicit requirement that no implementation path erase governed release history.

**Minimum repair boundary:** preserve the current immediate-predecessor transition semantics, but independently ensure
that every governed parent lineage traversed to establish current validity contains no post-introduction owner-absence
interval. Reuse the existing canonical raw-parent/owner-presence mechanism. Do not revalidate every historical YAML
transition, create a transaction registry, or add a second release-history authority.

## 7. Mandatory question — can authored P12 tests and normal CI remain green?

**Yes.**

All three supplied workflows are green on exact P12/binding/readiness descendants.

The authored P12 additions exercise missing blobs/trees, replace/graft behavior in
`_previous_governed_release_states()`, and readable alternate object storage. They do **not** install replace/graft
state while exercising `_check_ancestor()`.

The authored same-lineage deletion/reintroduction negative exercises the reintroduction state as the current HEAD. It
does **not** append a later material state and then ask whether the malformed interval remains detectable.

Therefore the complete authored P12 suite can remain green while:

- a non-canonical overlay validates the wrong Review/recovery/publication lineage; and
- a later material transition launders a prior governed owner deletion/reintroduction.

This answer comes from production behavior plus fresh real-Git counterexamples, not from test count.

## 8. Required topology/object/recovery matrix

| # | Required case | P12 independent disposition |
|---:|---|---|
| 1 | non-shallow historical owner blob unavailable | PASS in repaired resolver; unreadable owner fails closed |
| 2 | historical tree unavailable | PASS in repaired resolver; tree membership cannot be established -> fail closed |
| 3 | path/tree failure vs genuine absence | PASS in repaired resolver; `ls-tree` success+no entry is distinct from command/read failure |
| 4 | standard shallow boundary hiding owner introduction | PASS; unavailable raw parent commit prevents negative proof |
| 5 | shallow missing merge-parent lineage | PASS; required parent cannot be read -> fail closed |
| 6 | active `git replace` hiding owner introduction | predecessor resolver PASS; assembled lineage predicates **FAIL** via B65-P12-1 |
| 7 | deprecated `info/grafts` rewriting | predecessor resolver PASS; assembled lineage predicates **FAIL** via B65-P12-1 |
| 8 | readable alternate object store | PASS; required objects remain readable and canonical owner history is found |
| 9 | readable partial/promisor-backed objects | bounded PASS by production semantics when required objects resolve; no separate remote-promisor realization in this Review |
| 10 | unavailable promisor-required evidence | resolver is fail-closed on unresolved commit/tree/blob/path; no separate remote-promisor origin was required to establish the blockers |
| 11 | complete-history first owner introduction from pre-owner HEAD | PASS |
| 12 | genuine pre-owner merge parent + governed feature lineage | PASS |
| 13 | visible post-introduction deletion/restoration | direct current restoration is rejected; **FAIL after later transition** via B65-P12-2 |
| 14 | multiple commits while owner absent | PASS while the malformed interval is directly inspected |
| 15 | same-lineage committed reintroduction | direct reintroduction rejected; **FAIL after later transition** via B65-P12-2 |
| 16 | working-tree transition against owner-present committed HEAD | PASS |
| 17 | ordinary linear committed transition | PASS |
| 18 | evidence-only descendants | PASS |
| 19 | consecutive material transitions | PASS for well-formed ancestry; **not sufficient as a history-completeness oracle** because of B65-P12-2 |
| 20 | equivalent owner-present merge parents | PASS / deduplicated |
| 21 | divergent owner-present merge parents | PASS / each distinct predecessor boundary validated |
| 22 | reversed merge-parent order | PASS for visible canonical predecessor set |
| 23 | reversed relevant timestamps | PASS; timestamps do not select authority |
| 24 | traversal-stack/sibling-enumeration independence | PASS for visible predecessor set; does not close B65-P12-2's stopping boundary |
| 25 | stale recovery target | local predicate rejects without overlays; **canonical guarantee FAILS** under B65-P12-1 |
| 26 | sibling/wrong-ancestry recovery target | local predicate rejects without overlays; **canonical guarantee FAILS** under B65-P12-1 |
| 27 | complete later recovery + legal descendant publication | PASS in canonical no-overlay history; assembled canonicality remains blocked by B65-P12-1 |

## 9. Qualification-method challenge

For each material oracle, the smallest wrong implementation that can still pass was considered.

| Oracle/evidence | Smallest wrong behavior that can still pass | Review |
|---|---|---|
| raw `cat-file` parent reconstruction | canonical resolver is correct, but another lineage helper uses overlay-sensitive revision traversal | **SURVIVES: B65-P12-1** |
| `--no-replace-objects` | protects only commands that use it; does not itself suppress `info/grafts` in `merge-base` | **SURVIVES: B65-P12-1** |
| `ls-tree` path membership | current inspected commit is correctly classified, but traversal stops before an older malformed interval | **SURVIVES: B65-P12-2** |
| historical content reads | every reached blob is readable, but a required older commit is never reached after a material boundary | **SURVIVES: B65-P12-2** |
| shallow-history tests | standard shallow cases fail closed while non-shallow or cross-helper authority remains wrong | useful but bounded |
| replace/graft tests | resolver ignores overlays while `_check_ancestor()` still honors them | **SURVIVES: B65-P12-1** |
| alternate-object tests | readable alternate succeeds while wrong canonical relation elsewhere remains possible | bounded |
| transition/recovery tests | direct malformed state rejects, yet a later transition hides it; no-overlay recovery negatives pass while overlay can invert ancestry | **SURVIVES: both blockers** |
| strict YAML/parser tests | parser can be perfect while temporal graph semantics are wrong | bounded structural claim only |
| evidence-subject binding | subject/disposition can be exact while ancestry from subject to evidence is overlay-rewritten | **B65-P12-1** |
| generated snapshot parity | derived bytes can match while release-history D4 behavior is wrong | bounded representation claim only |
| package/reference closure | package can be complete while lifecycle validator is wrong | bounded distribution claim only |
| frozen-resource tests | historical bytes can remain frozen while current lifecycle concretization is wrong | bounded preservation claim only |
| Orchestrator Core acceptance | Core can accept the assembled package while out-of-matrix Git history violates lifecycle invariants | bounded integration claim only |

## 10. Prior blocker-family re-falsification

| Family | Exact P12 disposition |
|---|---|
| B65-P11-1 canonical ancestry/readability completeness | repaired in the new predecessor resolver, including fresh missing-parent-commit holdout; **assembled canonical history still blocked by new B65-P12-1** |
| B65-P10-1 incomplete ancestry vs genuine pre-owner | closed for inspected raw-parent negative proof; unresolved required parent fails closed |
| B65-P9-1 deletion vs genuine pre-owner | direct classification repaired; **not compositionally closed because B65-P12-2 can hide the malformed interval after a later transition** |
| B65-P8-1 predecessor resolution / merge ordering | closed for owner-present current predecessor selection; direct canonical parents, not date/log order, drive enumeration |
| B65-P7-1 transition continuity and recovery lineage | transition/recovery predicates exist, but assembled closure **fails through B65-P12-1 and B65-P12-2** |
| B65-P6-1 strict root-state parser convergence | closed; duplicate-key-rejecting YAML owner/parser remains |
| B65-P6-2 canonical semantic-version/history ordering | closed; canonical ASCII semver and numeric tuple order remain |
| B65-P5-1 duplicate-key root ambiguity | closed |
| B65-P5-2 candidate succession / historical collision | closed |
| B65-P4-1 evidence-front-matter ambiguity | closed structurally by strict front-matter parsing and explicit-subject precedence |
| B65-P3-1 exact Review/ratification subject binding | closed structurally; ancestry relation around that evidence is blocked by B65-P12-1 |
| B65-P3-2 current representation convergence | closed on inspected canonical/generated/Core prompt identity |
| B65-P2-1 / B65-R2 duplicated mutable lifecycle state | closed on inspected current surfaces; root YAML remains sole mutable owner |
| B65-P2-2 / B65-R1 immutable evidence applicability | exact immutable route/subject/disposition retained; temporal ancestry applicability blocked only where B65-P12-1 applies |
| B65-R3 predecessor-version gating | closed; no current predecessor-version semantic gate was found |

No prior Review conclusion is inherited as acceptance.

## 11. DF-1 through DF-4

### DF-1 — release-state/version lifecycle ownership

One mutable owner exists and P12 removes P11's defective negative-history shortcut. **NO-PASS in D4** because canonical
lineage authority is inconsistent across helpers (B65-P12-1) and transition continuity can forget a previously
malformed owner-absence interval (B65-P12-2).

### DF-2 — qualification and Review epistemology

The mechanical/semantic boundary is correctly represented: green CI remains mechanical evidence only. This Review
demonstrates P65-3/P65-4 in practice because both blockers survive the authored matrix. **PASS in doctrine; P12
qualification claims must be narrowed accordingly.**

### DF-3 — meta-control semantics and governance

Independent Review, Serious Challenge, stakeholder ratification, evidence, PEM, and D1-D4 authority remain distinct.
No hidden D5/meta-authority or self-ratifying mechanism was found. **PASS.**

### DF-4 — representation/schema/convergence self-application

Root state remains one owner; source/generated/Core representation is convergent; PEM remains project-local and
non-authoritative; historical resources remain frozen. Self-application exposes the two D4 lifecycle defects.
**NO-PASS only through the DF-1 lifecycle behavior dependency.**

## 12. Local-compliance / global-failure trajectories

### Trajectory A — canonical resolver + overlay-sensitive recovery lineage

Locally:

- predecessor resolver uses raw canonical parents;
- replace/graft authored predecessor tests pass;
- stale/sibling recovery tests pass in an ordinary repository;
- current YAML is coherent.

Globally, installing a local replacement/graft can change `merge-base --is-ancestor` and make a canonically wrong
lineage satisfy `_check_ancestor()`. This is B65-P12-1.

### Trajectory B — direct deletion/reintroduction rejection + later legal transition

Locally:

- direct B restoration is rejected;
- B -> C is a legal material transition;
- C's immediate predecessor is correctly B;
- all inspected current objects are readable.

Globally, C validation stops at B and forgets A -> D -> B. This is B65-P12-2.

These trajectories show that individually correct mechanisms can compose into an invalid assembled lifecycle.

## 13. Historical capability preservation

Historical preservation was re-evaluated as capability preservation rather than wording preservation.

Material capabilities from Protocol 5.13, 5.14, 5.15, 5.16, 6.0, 6.1, 6.2, 6.3, and 6.4 remain present in current
owners in modern integrated form, including:

- D1-D4 authority separation and abstraction/concretization discipline;
- Serious Challenge and human adjudication;
- evidence specification -> realization -> observation -> assessment;
- source availability versus runtime context availability;
- formal-first definition discipline, definitional conservativity, well-definedness/type/unit/domain closure;
- parameter family/instance/default ownership;
- exact external source/variant/provenance binding;
- validity/hypothesis propagation and definition/warrant separation;
- typed semantic dependencies including `USES_DEFINITION`;
- Lossless Representation, progressive disclosure, and cold discoverability;
- version-bound interpretation and exact fallback/recovery separation;
- PEM accepted-base/candidate-overlay semantics, binding health, and PEM non-authority;
- Review abstraction adequacy/out-of-matrix falsification;
- active simplicity and total-system-complexity discipline;
- Verification/Stabilization/maintenance-audit capability;
- language-profile/cross-language performance semantics.

Independent immutable identity checks found all 12 supported frozen profile/prompt objects for Protocol 5.16 and
6.0-6.4 byte-identical P0 -> P12.

All six inspected Protocol 7 D3/D4 parent/revision artifacts are byte-identical P0 -> P12.

P9 -> P12 changes are limited to release state, release-state D4/tests, qualification/review/handoff evidence, and the
Protocol 6.5 active workplans; no frozen protocol resource or Protocol 7 D3/D4 artifact is changed.

**Historical-capability disposition:** no new doctrine/resource regression. Overall preservation is **NO-PASS only at
the D4 release-lifecycle capability** because B65-P12-1/B65-P12-2 violate preserved canonical/continuous lifecycle
semantics.

## 14. P65-1 through P65-6 causal ablation

| Principle | Counterfactual failure if removed/weakened | P12 result |
|---|---|---|
| P65-1 self-application | SSDP's own release machinery could escape owner/evidence rules | necessary; both blockers are self-application failures in D4 |
| P65-2 lifecycle/version-intrinsic separation | mutable release truth returns to immutable semantic source/copies | necessary and otherwise realized |
| P65-3 evidence-claim congruence | green CI could be treated as proof of canonical/continuous history it does not discriminate | necessary; both blockers demonstrate it |
| P65-4 Review abstraction adequacy | Review stops at authored P12 tests and misses cross-helper/compositional counterexamples | necessary and directly causal |
| P65-5 minimum explicit meta-governance | Review/ratification/Challenge/PEM authority can collapse | necessary and realized |
| P65-6 integrated current representation | current source/generated/lifecycle surfaces can diverge or hide fragmented authority | necessary; representation is convergent, lifecycle D4 still incomplete |

No principle should be removed or materially weakened. No new D3 principle is required.

## 15. Project Engineering Memory / Historical Applicability Set

Accepted/base PEM resolves to P0 `55c085261eb827e3047637d045a8e6917ea6b962`; the branch declares a candidate
overlay and does not self-declare acceptance. PEM is evidence only.

Task-local HAS:

- **FF-001 premature immutable bootstrap publication — APPLICABLE:** exact immutable publication ordering and stale
  fallback risk are in scope; evidence-only.
- **SP-002 self-reference-safe descendant publication — APPLICABLE:** supports candidate -> later fallback -> distinct
  recovery lifecycle hypothesis; evidence-only.
- **PC-001 frozen prior-version profile/resource preservation — APPLICABLE:** independently corroborated by P0/P12
  blob equality; normative force comes from the versioning owner.
- **DS-001 semantic proxy qualification can overclaim — APPLICABLE:** independently corroborated by both fresh
  production-path holdouts.
- **SP-001 owner-layer route repair — NOT MATERIAL TO THE BLOCKER:** package/source closure is independently green;
  routing repair history does not decide lifecycle ancestry correctness.

No PEM entry establishes Review disposition.

## 16. Generated/package/Core convergence and frozen identities

Exact P12 workflow evidence passed package build, independent generated validation, committed-distribution parity,
snapshot parity, and Orchestrator Core.

Independent identity check:

`source/shared/references/development-workflow-prompts.md`

and

`orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.5/prompts.md`

have the same Git blob at P12.

The 12 frozen 5.16/6.0-6.4 profile/prompt blobs are unchanged P0 -> P12.

Protocol 7 D3/D4 artifacts are unchanged P0 -> P12.

No convergence, frozen-identity, package-closure, or Protocol 7 isolation blocker was found.

## 17. Simplicity / total-system complexity

P12's P11 repair is directionally simple: it removes the non-shallow completeness shortcut and reuses Git object
semantics rather than adding a registry.

The required repairs should preserve that shape:

- no second state owner;
- no topology registry/service;
- no branch/default/latest/timestamp authority;
- no candidate-specific table;
- no compatibility layer;
- no broad historical transaction replay engine.

For B65-P12-1, reuse canonical raw parent traversal for ancestor checks.

For B65-P12-2, add one bounded history-integrity traversal/condition to the existing resolver so a post-introduction
owner-absence interval cannot be hidden behind a later material boundary. Do not turn every historical commit into a
new transition authority.

## 18. Evidence applicability and stale-evidence exclusions

Applicable mechanical evidence:

- exact P12 `c6a0e9...` workflow `36121450601`: exact tree mechanical/package/Core behavior under its checkout;
- binding descendant `dc1595...` workflow `36121601230`: exact P12 bound with Review NOT_RUN;
- readiness descendant `93ff38...` workflow `36121836579`: lifecycle/readiness mechanics;
- P12 repair/freeze/binding qualification: author-side bounded claims;
- P9 historical capability record: historical hypothesis/evidence, independently checked against P12 identities;
- fresh real-Git missing-parent-commit holdout: supports closure of P11's new-resolver completeness defect;
- fresh replace/graft `_check_ancestor` holdouts: establish B65-P12-1;
- fresh deletion/reintroduction+later-transition holdout: establishes B65-P12-2.

Excluded as semantic acceptance:

- P1-P11 Review dispositions;
- P11 mechanical evidence as evidence of P12 semantics;
- green P12 CI as semantic Review PASS;
- mutable branch-head position;
- PR mergeability/default branch/latest/timestamps;
- PEM summaries as authority.

## 19. Earliest owners and precise repair contract

### B65-P12-1

Earliest owner: D4 `source/release_state.py::_check_ancestor`.

Required repair:

1. define ancestry from canonical raw commit parent identities, not overlay-sensitive revision traversal;
2. ensure both replacement refs and deprecated grafts cannot redefine Review/ratification/publication/recovery lineage;
3. fail closed if any required canonical commit object is unavailable;
4. preserve readable alternate/promisor-backed objects when Git can actually resolve them;
5. reuse existing raw-parent machinery; do not create a second topology authority;
6. add real-Git replace **and graft** holdouts directly against the production ancestor predicate and at least one
   recovery/evidence lineage consumer.

### B65-P12-2

Earliest owner: D4 `source/release_state.py::_previous_governed_release_states` /
`_lineage_has_governed_release_state` composition.

Required repair:

1. keep immediate material predecessor semantics for transition validation;
2. additionally prove that governed ancestry behind each selected predecessor has not crossed a post-introduction
   owner-absence interval;
3. catch A(owner) -> D(absent) -> B(reintroduced) -> C(later transition) at C;
4. preserve genuine pre-owner introduction/merge behavior;
5. preserve evidence-only descendants and ordinary consecutive transitions;
6. remain parent-order/timestamp/stack independent;
7. reuse canonical raw-parent/path-presence machinery rather than adding a history registry or replay subsystem.

Required fresh replacement holdouts must include both blocker counterexamples plus all P12 object-availability,
shallow, replace/graft, alternate-store, transition, recovery, parser, semver, evidence-binding, package/Core, frozen
resource, and Protocol 7 controls.

## 20. Final lifecycle consequence

```text
REVIEW DISPOSITION:                         NO-PASS
SERIOUS CHALLENGE:                          NONE
ACCEPTED PROTOCOL 6.5 D3:                   CLOSED / NOT REOPENED
GENUINE BLOCKERS:                           B65-P12-1, B65-P12-2
EARLIEST OWNER:                             D4 source/release_state.py
P12 TECHNICALLY ELIGIBLE FOR RATIFICATION:  NO
STAKEHOLDER RATIFICATION:                   NOT AUTHORIZED
PUBLIC FALLBACK / RECOVERY / CUTOVER:       NOT AUTHORIZED
PR #33 MERGE:                               NOT AUTHORIZED
PROTOCOL 7 D3/D4 MUTATION:                  NOT AUTHORIZED
NEXT ACTION:                                bounded D4 repair -> new immutable candidate -> exact-candidate qualification -> later binding -> fresh independent Review
```

P12 must remain immutable.

This Review authorizes only durable NO-PASS publication, exact-P12 NO_PASS lifecycle binding from a later descendant,
and reopening the affected D4 workplan scope. It does not authorize semantic mutation of P12.
