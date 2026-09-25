---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: d792f219ad361b6acb2663833beec1c179ea5793
semantic_ref: d792f219ad361b6acb2663833beec1c179ea5793
binding_descendant: c2c6baab291c22591c9ddc82eb0378fd3c92b264
readiness_descendant: b4116f55e2896b3f02d27c039abafac8b70928a6
exact_candidate_run: 36133381631
binding_run: 36133589027
readiness_run: 36133804528
serious_challenge: none
blocking_findings:
  - B65-P14-1
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P14

## 1. Disposition

**NO-PASS.**

The semantic Review target is exact immutable P14:

`d792f219ad361b6acb2663833beec1c179ea5793`

against accepted Protocol 6.4 control P0:

`55c085261eb827e3047637d045a8e6917ea6b962`.

The P14 binding and readiness descendants were used only for lifecycle/qualification state. They were not substituted
for P14.

One genuine D4 blocker survives fresh independent out-of-matrix falsification:

**B65-P14-1 — local PEM authority/evidence routes can be mechanically HEALTHY while their Git revision is a mutable
branch/tag name rather than an immutable revision identity.**

P14 correctly repairs the P13 local-Git overlay defect: replacement objects and grafts no longer control canonical
ancestry, replacement objects no longer control immutable local content reads, and release-state and PEM ancestry share
one bounded raw-parent implementation utility. However, the production PEM route grammar still accepts an arbitrary
non-whitespace Git revision token, and the live authority/evidence consumers resolve that token at validation time
without requiring it to be an immutable commit identity.

A mutable route such as:

`local@durable-owner:owner.md#anchor`

can therefore pass the exact P14 production predicates, then silently resolve to a different commit after
`durable-owner` moves, while continuing to pass accepted-project containment and same-path-content checks. The route
has changed temporal subject without changing serialized evidence identity.

This violates current PEM/evidence authority, which requires an `AUTHORITY_BOUND` owner route to be immutable and
requires durable material evidence to survive ordinary branch movement. It also violates P65-1 self-application,
P65-3 evidence-claim congruence, and P65-5 exact accepted/base/evidence governance at D4.

P14 remains immutable. Any semantic repair requires a new candidate identity.

## 2. Independence and evidence boundary

This Review reconstructed the current project instructions, accepted Protocol 6.5 D3->D4 contract, exact P14
production owners, exact lifecycle owner, preserved historical/profile surfaces, and current project memory before
using prior failed-candidate Reviews as hypothesis/evidence.

The three supplied workflows are bounded mechanical evidence only:

- exact P14 workflow `36133381631`: completed successfully at exact P14;
- binding workflow `36133589027`: completed successfully at
  `c2c6baab291c22591c9ddc82eb0378fd3c92b264`;
- readiness workflow `36133804528`: completed successfully at
  `b4116f55e2896b3f02d27c039abafac8b70928a6`.

The connected repository API was used to inspect exact immutable source blobs, commits, trees, lifecycle state, and
workflow subjects. The execution environment could not resolve github.com for a local clone, so fresh Git holdouts
were constructed in local temporary repositories using the exact P14 production predicates/raw-parent algorithm
rather than rerunning the full repository suite locally. That limitation does not affect the reproduced blocker: the
wrong acceptance follows directly from the exact P14 route grammar and production validation sequence.

## 3. Serious Challenge pass

**SERIOUS CHALLENGE: NONE.**

Accepted Protocol 6.5 D3 is coherent and realizable. It already requires:

- self-application of ownership/evidence/representation rules;
- exact accepted/base project-memory identity;
- immutable authority/evidence routes for authority-bearing PEM;
- evidence claims no stronger than their realization method;
- mechanical qualification separate from semantic Review;
- no fifth semantic authority/control plane;
- explicit stakeholder ratification after technical Review.

B65-P14-1 is not a contradiction in those requirements. It is an incomplete D4 concretization in
`source/project_engineering_memory.py`.

Earliest owning domain: **D4 PEM validation**, not D3.

## 4. Lifecycle state independently verified

At readiness descendant `b4116f55e2896b3f02d27c039abafac8b70928a6`, the sole mutable owner
`PROTOCOL-RELEASE-STATE.yaml` independently verifies:

- accepted-current: `6.4.0`;
- candidate version: `6.5.0`;
- candidate semantic ref: exact P14
  `d792f219ad361b6acb2663833beec1c179ea5793`;
- Review: `NOT_RUN`;
- stakeholder ratification: `NOT_REQUESTED`;
- candidate public fallback: `UNAVAILABLE`;
- candidate recovery: `UNAVAILABLE`.

The binding descendant is exactly one descendant commit after P14; the readiness descendant is exactly one further
descendant. Neither changes the semantic candidate.

No accepted-current cutover, ratification, public-fallback publication, recovery establishment, PR merge, or Protocol
7 mutation is authorized by this Review.

## 5. Mandatory B65-P13-1 repair falsification

### 5.1 Canonical ancestry under replace refs

**CLOSED at P14.**

`source/canonical_git.py` resolves the named commit with replacement objects disabled, reads the raw commit object,
parses only raw `parent` headers, and traverses those raw parents. PEM accepted-project containment delegates to this
mechanism.

A replacement object can still make ordinary Git revision traversal report a false sibling ancestry relation, but it
cannot change the raw-parent relation used by P14.

### 5.2 Canonical ancestry under deprecated grafts

**CLOSED at P14.**

Grafts alter revision traversal even when `--no-replace-objects` is supplied to ordinary graph commands. P14 does
not delegate the governing relation to `merge-base --is-ancestor`; it parses raw commit-parent objects, so grafts do
not become ancestry authority.

### 5.3 Live AUTHORITY_BOUND consumer

**EXERCISED.**

Exact P14 `PROJECT-ENGINEERING-MEMORY.md` contains current PC-001 with:

- `authority_binding: AUTHORITY_BOUND`;
- owner and authority-evidence routes bound to exact P0;
- `binding_health: HEALTHY`.

That path reaches the production owner/evidence validation logic rather than a test-only helper.

Its current exact-SHA binding is healthy. B65-P14-1 concerns the validator's acceptance envelope: the same field also
accepts a mutable Git ref.

### 5.4 Immutable content/path/locator under replacement objects

**CLOSED for replacement-object rewriting.**

All local PEM object/content realization through `_git_ok()` and `_git_text()` now invokes Git with
`--no-replace-objects`. A fresh blob-level replacement holdout independently confirmed that ordinary Git can expose
forged blob content while the P14-style replacement-disabled read returns the canonical blob bytes.

The authored commit-replacement locator test is consistent with this production behavior but is not the sole basis of
this conclusion.

### 5.5 Repair-acceptance containment and recurrence chronology

**CLOSED for overlay rewriting.**

`_validate_repair_acceptance_routes()` uses canonical raw-parent containment. The typed acceptance artifact is read
with replacement objects disabled. Its owner is routed through accepted-project owner validation. Git-native recurrence
then requires canonical:

`prior occurrence -> repair -> accepted repair evidence -> later event`.

Neither ordinary replace-ref ancestry nor graft traversal owns those relations after P14.

### 5.6 Canonical patch-ID / copied-event evidence

**CLOSED for replacement objects.**

`_git_patch_id()` resolves the canonical commit and canonical first parent through the raw-parent helper, computes
the diff with replacement objects disabled, and pipes those bytes to stable patch-ID. A replacement object cannot
substitute the event diff.

Patch-ID remains a replaceable implementation heuristic, not schema authority; failure to derive a patch-ID does not
itself prove independence.

### 5.7 Missing canonical parent/tree/blob/path objects

**FAIL-CLOSED for the repaired properties.**

Fresh local holdouts independently produced:

- a commit whose canonical parent object is unavailable: raw-parent traversal fails instead of proving ancestry;
- an unavailable blob: canonical content realization fails;
- an unavailable tree: canonical tree/path inspection fails;
- an absent path: canonical path realization fails.

The release-state implementation also distinguishes unreadable historical owner objects from genuine pre-owner
absence; unreadability does not become negative evidence of prior non-governance.

### 5.8 Alternate/promisor-backed canonical stores

**PRESERVED where Git can read the canonical object.**

Fresh local holdouts verified replacement-disabled canonical reads through:

- a shared alternate object store; and
- a local promisor/partial clone with lazy object fetch.

The shared helper does not introduce its own object database or bypass Git's ordinary object-resolution layer.

### 5.9 Release-state Review/ratification/publication/recovery ancestry

**CLOSED after helper consolidation.**

`source/release_state.py` delegates ancestry to the same raw-parent helper for:

- candidate Review evidence lineage/publication;
- stakeholder-ratification evidence lineage/publication;
- public-fallback lineage;
- recovery lineage/publication.

Evidence and version content reads are replacement-disabled and evidence routes require exact 40-hex commit subjects.

### 5.10 Release-state owner deletion/reintroduction continuity

**CLOSED after helper consolidation.**

The production continuity pass traverses the complete canonical reachable DAG, records owner-path presence, propagates
governance from parents, and rejects owner absence after any governed parent. Missing canonical ancestry/tree/content
fails closed.

### 5.11 Genuine pre-owner classification and pre-owner merges

**CLOSED.**

Pre-owner absence is accepted only after complete canonical ancestry establishes no governed owner on that lineage.
A genuine pre-owner merge parent can coexist with a governed parent while the merge retains the owner; a later
deletion/reintroduction cannot masquerade as pre-owner history.

### 5.12 No split topology authority introduced

**CLOSED.**

Extracting `source/canonical_git.py` reduces duplicated raw-parent D4 machinery. It does not decide policy,
accepted state, lifecycle meaning, PEM semantic ownership, or evidence admissibility. Release-state and PEM semantic
owners remain in their respective modules/doctrine; the helper is a delegated Git mechanism rather than a new control
plane.

## 6. Fresh holdout beyond P14 tests — mutable-route temporal drift

P14's PEM route grammar accepts any revision token matching the generic route syntax. The local resolver then asks Git
whether that token currently resolves as a commit/path and applies canonical containment/content checks.

A fresh temporary repository was constructed:

1. commit C1 introduced `owner.md`;
2. branch `durable-owner` pointed at C1;
3. C2 and accepted target C3 descended from C1 without changing `owner.md`;
4. route `local@durable-owner:owner.md#anchor` passed the P14 production predicates;
5. `durable-owner` was moved from C1 to C2;
6. the exact same serialized route passed again, now resolving to C2.

Observed:

```text
route=local@durable-owner:owner.md#anchor
accepted_before_move=true
accepted_after_move=true
resolved_before=<C1>
resolved_after=<C2>
accepted_target=<C3>
```

No replace ref, graft, missing object, malformed YAML, or path mutation is involved.

The validator has therefore certified a mutable ref as if it were an immutable evidence identity. A later branch move
changes the evidence transaction/temporal subject while leaving the route string and HEALTHY result unchanged.

This case is absent from the authored P14 PEM tests, which cover replacement/graft topology, canonical content,
repair-acceptance overlay containment, patch-ID stability, and alternates but not branch/tag revision immutability.

### Required explicit answer

> Could all P14 tests and normal CI remain green while a production self-governance validator still accepts
> noncanonical ancestry/content or validates the wrong temporal transaction?

**Yes.**

For the specific replace/graft/noncanonical-content families repaired from P13, fresh falsification found the P14
repair effective. But all current P14 tests and normal clean CI can remain green while the production PEM validator
accepts a mutable branch/tag revision as an "immutable" authority/evidence route and therefore validates a different
temporal transaction after that ref moves.

This is a local-compliance/global-failure trajectory: every authored overlay test can pass while the exact
self-governance claim is still broader than the production realization.

## 7. Historical blocker-family re-falsification at current owners

Current-owner disposition:

| Blocker family / obligation | P14 result |
| --- | --- |
| B65-P13-1 replacement/graft-sensitive PEM Git realization | **CLOSED for overlays** by shared raw-parent ancestry + replacement-disabled content |
| canonical ancestry/readability completeness | **CLOSED** for required release-state/PEM repaired paths; unavailable canonical objects fail closed |
| incomplete ancestry vs genuine pre-owner ancestry | **CLOSED** by complete canonical traversal before negative pre-owner classification |
| governed owner deletion/reintroduction continuity | **CLOSED** by canonical DAG continuity pass |
| merge predecessor selection | **CLOSED** by raw parent material-boundary traversal, independent of default log ordering |
| parent-order / timestamp independence | **CLOSED**; governing transition inference is structural, not timestamp selected |
| transition and recovery continuity | **CLOSED** at release-state owner |
| strict root release-state parsing | **CLOSED** by duplicate-key-rejecting YAML loader and fixed root schema |
| strict immutable evidence/front-matter parsing | **CLOSED** for release-state Review/ratification evidence; exact SHA route + duplicate-key rejection + exact subject/disposition binding |
| semantic-version and historical ordering | **CLOSED** by strict ASCII semver syntax/tuple ordering and historical constraints |
| candidate/history succession and collision rules | **CLOSED** at release-state owner |
| exact Review/ratification subject binding | **CLOSED** by explicit exact candidate subject + disposition matching |
| source/generated/package/reference convergence | **No new P14 regression found**; sampled source/dist blobs are identical and exact P14 workflow is green within its oracle scope |
| mutable lifecycle-state uniqueness | **No new duplicate owner found**; root release-state remains the only mutable release-state owner |
| evidence applicability | **BLOCKED in PEM durability envelope by B65-P14-1**: mutable local revision aliases can be marked HEALTHY |
| predecessor-version gating | **No recurrence found** in current successor/cutover semantics |
| fail closed on unavailable required canonical objects | **CLOSED** for inspected current owners |

B65-P14-1 is not a reopening of the P13 overlay defect. It is a distinct durability/identity defect exposed by the
same self-application boundary.

## 8. DF-1 through DF-4

- **DF-1 — release-state/version lifecycle ownership:** materially closed. One root mutable lifecycle owner remains;
  version-intrinsic source/package semantics stay separate.
- **DF-2 — qualification/Review epistemology:** doctrine remains coherent and useful. The new blocker demonstrates why
  green CI cannot establish an untested durability/identity property.
- **DF-3 — meta-control governance:** no material defect found in Serious Challenge, Review independence,
  stakeholder-ratification separation, or acceptance authority.
- **DF-4 — self-application/current representation:** **NO-PASS at D4** because a self-hosted authority/evidence
  validator can call a moving local Git ref an immutable/durable binding.

## 9. P65-1 through P65-6 causal usefulness

- **P65-1 Self-application:** causal; exposes the project’s own PEM route as governed rather than exempt.
- **P65-2 State/semantics separation:** preserved; the blocker does not reintroduce mutable release-state values into
  immutable protocol semantics.
- **P65-3 Evidence-claim congruence:** causal; `HEALTHY`/immutable authority is stronger than what a movable ref token
  establishes.
- **P65-4 Review abstraction adequacy:** causal; the failure lies outside the authored overlay matrix while all normal
  workflows are green.
- **P65-5 Minimal meta-governance:** remains coherent; the correct repair is narrower validation at the existing owner,
  not a new registry/control plane.
- **P65-6 Integrated current representation:** no separate generated/source owner drift was found; B65-P14-1 is
  validation semantics, not a representation-copy defect.

No principle needs D3 reopening.

## 10. Protocol 6.4 -> 6.5 and historical capability preservation

Capability preservation, not historical wording/mechanism identity, was used as the oracle.

Independent exact-tree comparison found all ten frozen Orchestrator `profile.json` / `prompts.md` artifacts for
Protocol 5.16 and 6.0-6.4 byte-identical P0 -> P14.

The six active Protocol 7 parent/revision workplan blobs are also byte-identical P0 -> P14.

No new regression was found in the historically required capabilities around:

- exact immutable release identity;
- self-reference-safe publication;
- public fallback distinct from recovery;
- conditional PEM/HAS and PEM non-authority;
- evidence lifecycle/binding health;
- proxy-proof/real-owner acceptance;
- lossless/progressive representation;
- routing/package canonical ownership;
- long-horizon preservation and recovery.

The historical-preservation surface is not the reason for NO-PASS.

## 11. Current source/generated/package/reference convergence

At exact P14, sampled canonical source and committed software-design distribution blobs are byte-identical for:

- role `SKILL.md`;
- `PROTOCOL_VERSION`;
- project-engineering-memory reference;
- testing-and-validation reference;
- workflow-and-workplans reference;
- protocol-versioning-and-compatibility reference.

Exact P14 workflow `36133381631` also passed the repository's package build, independent validation,
committed-distribution parity, snapshot parity, full protocol regression, and Orchestrator Core jobs. Those results are
accepted only for those mechanical properties.

No generated artifact was found acting as an independent semantic owner.

## 12. Qualification-method limits and fresh mutants

The smallest wrong implementation that current P14 qualification can still accept is the production behavior already
present: retain all replacement/graft protections but permit `route.revision` to be a movable local branch/tag name.

Fresh falsification classes considered:

- **topology:** replace/graft siblings — rejected correctly;
- **object/content:** commit/blob replacement — canonical bytes preserved;
- **state:** missing parent/tree/blob/path — fails closed;
- **storage:** alternate/promisor canonical object stores — readable;
- **schema/identity:** mutable local Git revision alias — **survives and is blocking**;
- **generated:** sampled source/dist exact-blob parity — preserved;
- **prose-semantic:** immutable/durable route claim versus runtime-resolved movable token — **mismatch**.

Therefore adding more overlay tests alone would not close this Review. The production route identity contract itself
must be narrowed to what the accepted doctrine requires.

## 13. Simplicity and total-system complexity

The P14 extraction of `source/canonical_git.py` is a net simplification: one raw-parent mechanism replaces duplicated
ancestry logic and remains delegated D4 plumbing.

B65-P14-1 does not justify another history registry, resolver daemon, transaction ledger, or semantic authority.

The simplest coherent repair is to make the existing local evidence-route resolver distinguish an immutable Git object
identity from a movable ref and refuse to call the latter a mechanically healthy immutable/durable route in contexts
that require immutability.

## 14. Protocol 7 isolation and SSDP self-application

Protocol 7 D3/D4 remains unchanged. P0 -> P14 exact-tree comparison found no changes in the six active Protocol 7
architecture workplans.

SSDP self-application is precisely where B65-P14-1 matters: the protocol requires immutable/durable evidence binding
from downstream projects while its own PEM validator currently admits a movable local ref as the same class of
binding.

## 15. Required D4 repair contract

Reopen only `source/project_engineering_memory.py` and directly affected tests/qualification/evidence surfaces.
`source/canonical_git.py` need not change unless a minimal helper addition reduces duplication without adding policy.

Minimum semantic repair:

1. **Immutable local revision identity.** A local route used where schema/current doctrine requires immutable/durable
   evidence must not be mechanically `HEALTHY` merely because an arbitrary branch/tag token currently resolves.
   Require an exact immutable Git object/revision identity, or an equivalently durable identity whose immutability is
   actually established by the owning resolver.
2. **AUTHORITY_BOUND owner/evidence.** `authority_owner` and accepted authority evidence must reject or downgrade a
   movable local Git ref; candidate/local branch movement must not change the bound temporal subject.
3. **Repair acceptance / recurrence.** Typed repair-acceptance routes and their authority owner must carry durable
   immutable local revision identity before they may establish accepted repair chronology.
4. **Ordinary material evidence health.** Do not label a bare local branch/default/latest ref `HEALTHY` as durable
   current support when the schema/evidence owner requires branch-movement-resistant identity. Use the existing
   `REVIEW_REQUIRED`/`UNAVAILABLE` semantics where appropriate rather than inventing a new state.
5. **Preserve canonical overlay resistance.** Keep raw-parent ancestry, replacement-disabled content, fail-closed
   missing-object behavior, and alternate/promisor readability.
6. **No new authority plane.** Do not create a ref registry, timestamp oracle, branch history database, or separate PEM
   topology owner.
7. **Fresh production tests.** Add at least:
   - an `AUTHORITY_BOUND` owner route using a branch alias that would otherwise pass accepted-project containment;
   - movement/retargeting of that branch while owner content remains unchanged;
   - an equivalent movable tag/ref case if the resolver accepts it;
   - an exact immutable SHA positive control;
   - a repair-acceptance route using a movable local ref;
   - regression of P14 replace/graft/content/missing-object/alternate/promisor behavior.
8. **Replacement candidate.** Preserve P14 immutably. Any semantic repair creates a new candidate identity (P15 or the
   next project-assigned identity), runs exact-candidate normal CI, then is bound at Review `NOT_RUN` before another
   genuinely fresh independent assembled-candidate Review.

## 16. Lifecycle boundary

This NO-PASS means only that P14 is **not technically eligible for stakeholder ratification**.

It does not:

- ratify Protocol 6.5;
- publish a Protocol 6.5 public fallback;
- establish Protocol 6.5 recovery;
- change `accepted_current`;
- merge PR #33;
- mutate Protocol 7 D3/D4.

The next authorized semantic work is only the bounded B65-P14-1 D4 repair and replacement-candidate qualification.
