---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: 6352accc7962fc188976fc1bcea5e081681d99c5
semantic_ref: 6352accc7962fc188976fc1bcea5e081681d99c5
binding_descendant: 0490ecb0c685b403df78f62f143896c44c078d68
review_basis_descendant: ce03232a2a7868a573e0491a083595e5c1f7a27a
exact_candidate_run: 36103358186
binding_run: 36103484871
readiness_run: 36103644189
serious_challenge: none
blocking_findings:
  - B65-P11-1
historical_capability_preservation: no-pass-d4-lifecycle-only
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P11

## 1. Review disposition

**NO-PASS.**

Exact immutable P11
`6352accc7962fc188976fc1bcea5e081681d99c5`
is **not technically eligible for stakeholder ratification**.

One genuine D4 blocker survives:

**B65-P11-1 — non-shallow Git state can still be mistaken for complete canonical ancestry.**

P11 correctly rejects the authored shallow-history counterexamples, but its negative proof remains unsound outside that
matrix. The production resolver can still conclude "genuinely pre-owner" when a governed owner is hidden by unavailable
historical objects or by local Git ancestry-rewriting overlays even though
`git rev-parse --is-shallow-repository` reports `false`.

No Serious Challenge is raised. Accepted Protocol 6.5 D3 remains coherent, jointly concretizable, and closed. The
defect is localized to the existing D4 release-state ancestry classifier.

P11 remains immutable. Any semantic repair requires a new immutable candidate identity.

## 2. Review independence, subject, and evidence boundary

This Review was reconstructed independently from:

- accepted Protocol 6.4 control P0
  `55c085261eb827e3047637d045a8e6917ea6b962`;
- exact semantic candidate P11
  `6352accc7962fc188976fc1bcea5e081681d99c5`;
- current Protocol 6.5 canonical owners and real D4 production paths;
- the sole mutable root release-state owner and its P11 binding descendant;
- frozen prior-version/profile resources and Protocol 7 design artifacts;
- exact-candidate, binding, and readiness workflow evidence;
- current Project Engineering Memory only as evidence-backed hypothesis input;
- prior P1-P10 Reviews only as historical evidence to be re-falsified where relevant.

The mutable branch head and binding descendant were not substituted for P11 as the semantic Review target.

The following workflow runs were independently resolved as successful, but are used only for the properties their
oracles discriminate:

- exact P11: `36103358186`, head SHA exact P11;
- binding descendant: `36103484871`, head SHA
  `0490ecb0c685b403df78f62f143896c44c078d68`;
- readiness descendant: `36103644189`, head SHA
  `ce03232a2a7868a573e0491a083595e5c1f7a27a`.

Green CI is not treated as semantic Review PASS.

## 3. Serious Challenge pass

**Serious Challenge: none.**

Accepted Protocol 6.5 D3 remains adequate for the protected release-lifecycle outcome:

- mutable release values have one repository owner;
- version-intrinsic protocol semantics remain separate from mutable release state;
- Review, stakeholder ratification, public fallback, recovery, and accepted-current remain distinct;
- exact immutable identity rather than branch/default/latest/timestamp is authoritative;
- history needed to validate release-state continuity must not be silently erased or inferred from an incomplete view;
- qualification claims remain bounded to the properties their methods discriminate.

The surviving defect does not require a new architectural owner, registry, topology service, or D3 doctrine. It is a
D4 false-negative in how the current implementation realizes the existing ancestry-completeness contract.

## 4. Project Engineering Memory basis and Historical Applicability Set

Project-local policy identifies `main` as the accepted/base PEM publication line. At Review time `main` resolves
to exact P0
`55c085261eb827e3047637d045a8e6917ea6b962`.
The candidate branch carries a validated same-branch overlay. PEM remains non-authoritative.

```yaml
pem_basis:
  accepted_project_state: 55c085261eb827e3047637d045a8e6917ea6b962
  accepted_pem: hjin98/scientific-software-development-protocol@55c085261eb827e3047637d045a8e6917ea6b962:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: 6352accc7962fc188976fc1bcea5e081681d99c5
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: exact immutable release/publication lifecycle integrity is in scope; this remains evidence-only
  - id: PC-001
    disposition: APPLICABLE
    reason: frozen prior-version profile/resource preservation is directly in scope; normative force comes from the current versioning owner
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: source-to-package routing repair is not the mechanism under Review; package closure is checked separately under current authority
  - id: SP-002
    disposition: APPLICABLE
    reason: immutable candidate followed by descendant lifecycle publication is directly relevant evidence
  - id: DS-001
    disposition: APPLICABLE
    reason: claim-method congruence and proxy/fixture overclaim risk are directly material to the P11 completeness guard
```

No PEM item is used as D1-D4 authority.

## 5. Exact P11 production repair and actual call path

P11 changes the existing release-state ancestry classifier in
`source/release_state.py`.
The relevant production path is:

```text
main()
 -> _previous_governed_release_states()
 -> _reject_governed_owner_absence()
 -> _lineage_has_governed_release_state()
 -> git rev-list --full-history <ref> -- PROTOCOL-RELEASE-STATE.yaml
 -> _release_state_at_ref(..., missing_ok=True)
 -> git rev-parse --is-shallow-repository
```

P11's added behavior is narrow:

1. retain the positive existential rule: a visible readable ancestor containing the owner means the lineage is governed;
2. after no readable owner is found, ask
   `git rev-parse --is-shallow-repository`;
3. if Git reports `true`, fail closed;
4. if the query fails or returns an unrecognized result, fail closed;
5. otherwise return `False`, meaning a genuine pre-owner lineage may be admitted.

That repair is correct for the authored shallow cases, but `is-shallow-repository=false` is not a proof that every
object and canonical parent relation needed by the negative owner-history claim is available and unmodified.

A second material implementation detail is decisive:
`_release_state_at_ref(..., missing_ok=True)` maps **every** non-zero
`git show <ref>:PROTOCOL-RELEASE-STATE.yaml` result to
`_MISSING_RELEASE_STATE`.
It therefore does not distinguish:

- path genuinely absent from the historical tree; from
- path present but its blob/tree/object unreadable or unavailable.

The latter is not evidence of pre-owner history.

## 6. B65-P11-1 — non-shallow negative ancestry can still overclaim completeness

### 6.1 Fresh holdout A — historical owner blob unavailable in a non-shallow repository

A fresh real-Git topology was constructed outside the authored P11 test matrix:

```text
A: pre-owner
 -> B: introduce PROTOCOL-RELEASE-STATE.yaml
 -> C: delete PROTOCOL-RELEASE-STATE.yaml
 -> working tree: reintroduce owner
```

The historical owner blob used by B was then made unavailable while commit/tree ancestry remained readable.

Observed Git behavior:

```text
git rev-parse --is-shallow-repository
=> false

git rev-list --full-history HEAD -- PROTOCOL-RELEASE-STATE.yaml
=> success; includes the deletion and owner-introduction commits

git show <deletion>:PROTOCOL-RELEASE-STATE.yaml
=> non-zero because the path is absent

git show <owner-introduction>:PROTOCOL-RELEASE-STATE.yaml
=> non-zero because the historical owner object is unavailable/unreadable
```

Under exact P11 production semantics both non-zero `git show` results become
`_MISSING_RELEASE_STATE`.
The loop finds no readable owner; the shallow discriminator reports `false`; the resolver returns
"not governed" with no ancestry-completeness error.

The assembled consequence is a false pass:

```text
governed owner existed
 -> later deletion
 -> owner data unavailable at the historical introduction
 -> working-tree reintroduction
 -> P11 classifies ancestry as genuine pre-owner
 -> transition continuity is not enforced for the erased governed interval
```

This is a direct false negative in the property P11 was created to repair.

Alternates/object-store layouts are not defective merely because they are alternates: if all required objects are
readable, the current positive path remains valid. The defect arises when required historical objects are unavailable
or unreadable and that failure is converted to "path absent."

A promisor/partial-clone implementation that successfully materializes every required object before the proof may also
remain admissible. If required ancestry/path objects cannot be obtained, the proof must fail closed rather than convert
unavailability to historical absence.

### 6.2 Fresh holdout B — local replacement ref rewrites effective ancestry

A second real-Git holdout used the same governed introduction/deletion history but installed a local Git replacement
ref for the deletion commit whose replacement parent bypassed the owner-introduction commit.

Observed behavior:

```text
git rev-parse --is-shallow-repository
=> false

ordinary Git parent traversal
=> follows replacement history and skips the governed owner introduction

git rev-list --full-history HEAD -- PROTOCOL-RELEASE-STATE.yaml
=> empty under the rewritten effective ancestry
```

P11 therefore admits the lineage as genuinely pre-owner even though canonical repository history contains the governed
owner.

This is materially relevant because the validator itself uses ordinary Git history as release authority and does not
currently declare replacement refs/grafts to redefine that authority. A local replacement/graft overlay is not an
accepted release-state transition and cannot silently erase canonical historical ownership.

The required repair need not invent a topology service. It may either perform the relevant authoritative history
queries against canonical ancestry with replacement effects disabled, or explicitly detect and fail closed when a
replacement/graft overlay makes the negative proof non-canonical.

### 6.3 Common cause

The two holdouts are one blocker family, not two unrelated defects.

P11's negative inference effectively assumes:

```text
no readable owner returned by exact-path traversal
AND repository is not marked shallow
=> canonical owner ancestry is complete and owner never existed
```

That implication is false.

The correct bounded proposition is stronger:

```text
genuine pre-owner classification is admissible only when
the canonical ancestry needed by the claim is available,
unmodified by local history-rewrite overlays,
and every relevant owner-path state can be distinguished
as truly absent versus unreadable/unavailable.
```

## 7. Could all authored P11 tests and normal CI remain green?

**Yes.**

All three supplied workflows are green, and the authored P11 tests specifically discriminate the two shallow-history
cases. They do not discriminate the fresh failure modes above.

Inspection of exact P11's release-state tests found no dedicated holdout for:

- missing historical owner blob;
- unreadable historical owner state;
- missing tree/path object with otherwise non-shallow Git status;
- partial/promisor object unavailability;
- Git graft ancestry;
- Git replacement-ref ancestry.

Therefore the current suite can remain completely green while the production resolver:

- overclaims a negative ancestry result;
- silently omits a governed lineage; and
- skips the temporal transition that should have been validated.

This answer follows from the production algorithm plus real-Git counterexamples, not from test count.

## 8. Qualification-method challenge

For each material oracle, the smallest semantically wrong implementation that can still pass was considered.

### `git rev-parse --is-shallow-repository`

Useful for detecting standard shallow boundaries, but insufficient as a completeness proof.
Current P11 itself is the counterexample: it passes the authored shallow tests while remaining wrong for unreadable
objects and replacement-rewritten ancestry.

### Exact-path `rev-list --full-history`

Useful as a positive existential search when a returned candidate can be read and validated. An empty result does not
by itself prove canonical historical nonexistence when ancestry is rewritten or required objects are unavailable.

### Strict YAML parsing and evidence subject binding

These remain useful for syntax/ambiguity/exact-subject properties. They cannot establish history completeness and are
not treated as doing so.

### Generated snapshot parity and package/reference closure

These remain evidence for representation parity/reachability. They cannot establish release-history correctness.

### Transition/recovery lineage predicates

They remain useful once the correct historical states and canonical lineage are identified. P11's blocker occurs
earlier: a governed predecessor can be omitted from the set to which those predicates are applied.

The repair must strengthen the existing owner-history classifier rather than replace these specific oracles with a
universal semantic framework.

## 9. Re-falsification of prior blocker families

The P11 semantic delta is confined to the release-state ancestry classifier, its tests, and workplan evidence.
Critical current canonical owners for authority/evidence/versioning/PEM/D1-D4 remain unchanged from P10, and their
assembled behavior was re-inspected rather than inherited as accepted.

| Historical blocker family | Fresh P11 disposition |
| --- | --- |
| B65-P10-1 incomplete ancestry vs genuine pre-owner | **NOT CLOSED**; narrowed to B65-P11-1 because non-shallow does not prove canonical/readable completeness |
| B65-P9-1 governed owner deletion vs genuine pre-owner | **NOT GLOBALLY CLOSED** for the same surviving D4 negative-proof defect |
| B65-P8-1 predecessor resolution / merge ordering | CLOSED on inspected complete owner-present ancestry; parent topology, not timestamp/default log order, selects predecessors |
| B65-P7-1 transition continuity / recovery lineage | CLOSED on inspected complete-history transaction/recovery predicates once correct predecessors are visible |
| B65-P6-1 strict root-state parser convergence | CLOSED; root/evidence YAML uses duplicate-key-rejecting safe parsing |
| B65-P6-2 canonical semantic-version identity/history ordering | CLOSED; canonical ASCII semver syntax and tuple ordering remain enforced |
| B65-P5-1 duplicate-key root ambiguity | CLOSED |
| B65-P5-2 candidate succession / historical-version collision | CLOSED |
| B65-P4-1 evidence-front-matter duplicate/subject ambiguity | CLOSED |
| B65-P3-1 exact Review/ratification subject binding | CLOSED on inspected immutable route, subject, disposition, and lineage behavior |
| B65-P3-2 current representation convergence | CLOSED; current canonical/generated Protocol 6.5 prompt is one Git blob |
| B65-P2-1 / B65-R2 duplicated mutable lifecycle state | CLOSED; root YAML remains sole mutable owner |
| B65-P2-2 / B65-R1 immutable evidence applicability | CLOSED on inspected exact evidence-route/subject/disposition behavior |
| B65-R3 predecessor-version gating | CLOSED; no predecessor-version gate was found in current workflow semantics |

No additional blocker was found in those families.

## 10. DF-1 through DF-4

### DF-1 — release-state/version lifecycle ownership

Ownership architecture is convergent and minimal, but D4 behavior remains **NO-PASS** because B65-P11-1 can erase a
governed interval from transition validation.

### DF-2 — qualification and Review epistemology

The repository correctly distinguishes mechanical qualification from independent semantic Review. This Review is a
direct demonstration of why: exact P11, binding, and readiness CI are all green while the production resolver still
admits a semantic false negative.

The P11 qualification records remain applicable only to their actual shallow-history and regression oracles. They do
not establish arbitrary Git-history completeness.

### DF-3 — meta-control semantics and governance

No blocker found. Current owners retain materiality, independent falsification, Serious Challenge threshold,
Challenge resolution, and stakeholder ratification distinct from technical Review PASS. No closed ontology is
required.

### DF-4 — representation/schema/convergence self-application

No new blocker found. SSDP applies its own release/evidence/Review distinctions; one mutable state owner remains;
current-vs-history representation is separated; PEM remains project-local/non-authoritative; current source/generated
Protocol 6.5 prompts converge.

B65-P11-1 is a self-application failure in lifecycle behavior, not a second representation/schema owner.

## 11. Fresh local-compliance / global-failure trajectory

A fresh assembled trajectory satisfies every local-looking condition while violating a global invariant:

```text
root release state parses
+ current owner is unique
+ exact P11 is immutable
+ binding descendant points to exact P11
+ Review is NOT_RUN
+ all authored CI is green
+ Git reports repository non-shallow
+ exact-path history command itself returns success
+ a historical owner blob is unavailable
= classifier silently treats the owner-bearing commit as path-absent
= governed deletion/reintroduction is misclassified as first introduction
= global release-history continuity fails
```

The replacement-ref holdout yields the same global failure with all objects present but effective parent traversal
locally rewritten.

This is precisely the kind of locally compliant/global-failure trajectory P65-4 requires independent Review to find.

## 12. P65-1 through P65-6 causal ablation

| Principle | Fresh causal ablation result |
| --- | --- |
| P65-1 self-application | Necessary; without it SSDP's own release resolver could escape normal authority/evidence discipline |
| P65-2 version-intrinsic semantics vs mutable release state | Necessary; removing it recreates duplicated mutable lifecycle truth |
| P65-3 evidence-claim congruence | Necessary and directly demonstrated; shallow-only evidence cannot prove all canonical ancestry completeness |
| P65-4 independent out-of-matrix abstraction-adequacy Review | Necessary and directly demonstrated by the missing-object/replacement-ref holdouts |
| P65-5 compact canonical meta-control definitions | Necessary; removing independence/materiality/Challenge/ratification boundaries re-admits governance ambiguity |
| P65-6 integrated/current convergent representation | Necessary; predecessor-labelled operational amendments would re-admit stale conditional semantics |

No principle should be removed because P11's concretization is incomplete. The repair remains D4.

## 13. Historical capability-preservation review

Historical preservation was rechecked as capability preservation rather than wording/mechanism preservation.

No additional regression was found in the inspected lineage for:

- Protocol 5.13 relation-first deterministic tool routing and bounded optional CodeQL;
- Protocol 5.14 solution-boundary discipline, active simplicity, and removal/narrowing/rewiring before additive durable machinery;
- Protocol 5.15 language-profile specialization and cross-language performance/resource reasoning without global language precedence;
- Protocol 5.16 Verification, non-mutating Stabilization, Health Audit/maintenance sensing, and portable workflow/fallback discipline;
- Protocol 6.0 D1-D4 authority, DAG ordering, Challenge/human adjudication, and lower-layer non-authority;
- Protocol 6.1 abstraction/concretization vs evidence realization, evidence lifecycle/applicability, background/terminology, canonical navigation, transitive package closure, activation-vs-reachability, and exact immutable fallback;
- Protocol 6.2 Lossless Representation, one owner, progressive disclosure, bounded activation, cold discoverability, current-vs-history separation, exact bootstrap publication, and fallback-vs-recovery distinction;
- Protocol 6.3 PEM non-authority, accepted base plus candidate overlay, HAS, salience-only temperature, binding health, counterevidence/maturity discipline, and live-memory package exclusion;
- Protocol 6.4 source-vs-context availability, formal-first definitions, well-definedness, parameter family/instance/default separation, exact external source binding, validity propagation, definition-vs-warrant separation, typed `USES_DEFINITION`, and inert external/evidence content.

Direct immutable-identity checks found all twelve prior profile/prompt objects for Protocol 5.16 and 6.0-6.4
byte-identical between P0 and P11.

All six inspected Protocol 7 D3/D4 architecture/workplan artifacts are likewise byte-identical P0 to P11.

The current Protocol 6.5 generated prompt and canonical source
`source/shared/references/development-workflow-prompts.md`
are the same Git blob.

Transitive package/reference closure and frozen-resource/Core acceptance were exercised by the successful exact-P11
workflow; those results remain mechanical evidence for those properties only.

**Historical-capability preservation disposition: NO-PASS only at the D4 release-lifecycle capability represented by
B65-P11-1. No additional historical capability loss was found.**

## 14. Simplicity / total-system-complexity inspection

P11 remains structurally small: it did not introduce a second state owner, registry, transition mirror, topology
service, compatibility layer, candidate-specific branch, timestamp policy, or semantic phrase parser.

The problem is insufficient discrimination, not excess architecture.

The next repair should remain a bounded strengthening of the existing D4 ancestry classifier:

- distinguish true historical path absence from unreadable/unavailable owner content;
- fail closed when any object needed to prove the negative claim cannot be established;
- ensure the negative proof reflects canonical ancestry rather than local replace/graft overlays;
- retain the existing shallow guard as one useful incompleteness signal, not a universal completeness proof.

No D3 redesign is justified.

## 15. Exact evidence applicability

Applicable evidence and its bounded claim:

- P11 `6352accc7962fc188976fc1bcea5e081681d99c5`: semantic Review subject;
- run `36103358186`: exact-P11 mechanical regression/package/Core evidence;
- binding descendant `0490ecb0c685b403df78f62f143896c44c078d68`: lifecycle binding evidence only;
- run `36103484871`: binding-descendant mechanical evidence;
- readiness descendant `ce03232a2a7868a573e0491a083595e5c1f7a27a`: mutable handoff/evidence state only;
- run `36103644189`: readiness-descendant mechanical evidence;
- P11 repair/freeze/binding qualification records: evidence for the properties they explicitly discriminate;
- P10 and earlier Reviews: immutable historical hypotheses/evidence, not inherited P11 disposition;
- historical capability review: hypothesis map and bounded historical evidence, independently rechecked against current owners and identities.

No later descendant replaces P11 as the semantic Review subject.

## 16. Earliest owner and minimum repair contract

### Earliest owner

**D4 `source/release_state.py`**, specifically the negative-result contract spanning:

- `_release_state_at_ref(..., missing_ok=True)`;
- `_lineage_has_governed_release_state()`;
- `_reject_governed_owner_absence()`.

Accepted Protocol 6.5 D3 remains closed.

### Minimum repair

1. Preserve the existing positive rule: a visible readable ancestor containing a governed owner proves governed lineage.
2. Distinguish "the path is absent in this historical tree" from "the path/tree/blob/object cannot be read or resolved."
   The latter must produce an explicit validation error, not `_MISSING_RELEASE_STATE`.
3. A negative genuine-pre-owner conclusion is admissible only if every object and parent relation needed for that
   bounded canonical ancestry claim is available/readable.
4. Keep the shallow-repository check as a fail-closed signal, but do not treat
   `is-shallow-repository=false` as sufficient proof of completeness.
5. Prevent local replacement/graft overlays from silently becoming release-history authority. Use canonical ancestry
   for this proof or explicitly detect the overlay and fail closed.
6. Do not add a second state owner, registry, transition mirror, topology service, branch/default/latest policy,
   timestamp policy, candidate-specific identity, or universal Git-history framework.
7. Preserve all existing complete-history, shallow-history, transition, recovery, schema, semver, evidence-binding,
   source/generated, frozen-resource, and Protocol 7 controls.

### Mandatory fresh replacement-candidate holdouts

Exercise the **real production resolver** with real Git repositories:

- non-shallow repository with a historical owner blob unavailable: fail closed;
- required historical tree/path object unreadable or unavailable: fail closed;
- partial/promisor/alternate object-store case when supported: either obtain all required objects and prove the bounded
  claim, or fail closed;
- active replacement-ref or graft that hides a governed owner: use canonical history or fail closed;
- both existing P11 shallow-history negatives;
- complete-history genuine pre-owner HEAD first introduction;
- complete-history genuine pre-owner merge plus governed feature lineage;
- all P10/P11 complete-history topology and recovery controls.

Any semantic repair creates a new immutable candidate identity. Do not assign the next P-number before the repair
commit exists and exact-candidate normal CI passes.

## 17. Final disposition

- **Review disposition:** NO-PASS.
- **Serious Challenge:** none.
- **Genuine blocking finding:** B65-P11-1 only.
- **Historical-capability preservation:** no additional regression; NO-PASS only because the preserved release-lifecycle capability is still violated in D4.
- **Earliest owner:** D4 `source/release_state.py` ancestry classifier.
- **Exact evidence applicability:** mechanical workflows remain valid only for their discriminated properties and do not prove semantic ancestry completeness.
- **P11 technically eligible for stakeholder ratification:** **no**.
- **Next authorized lifecycle action:** publish this NO-PASS Review, bind exact P11 to Review `NO_PASS` from a later descendant, reopen the existing D3->D4 workplan at the existing D4 ancestry classifier, and implement only the bounded repair above as a new prospective candidate. No stakeholder ratification, public fallback, recovery establishment, accepted-current cutover, PR merge, or Protocol 7 D3/D4 mutation is authorized.
