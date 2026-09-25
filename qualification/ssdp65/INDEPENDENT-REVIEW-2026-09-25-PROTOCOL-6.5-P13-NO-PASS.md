---
kind: independent-assembled-candidate-review
status: no-pass
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
candidate_ref: 05a2b62550adadf271a27f6555da7173902c491c
semantic_ref: 05a2b62550adadf271a27f6555da7173902c491c
binding_descendant: 7e5e5fa68179f9b1d85ed7ab672e6333d99a1e67
readiness_descendant: fa61e43b92df1de4b1144d612b285edd51a2429d
exact_candidate_run: 36127313841
binding_run: 36127440732
readiness_run: 36127652673
serious_challenge: none
blocking_findings:
  - B65-P13-1
historical_capability_preservation: no-additional-regression-observed
stakeholder_ratification: not_authorized
date: 2026-09-25
---

# Fresh Independent Assembled-Candidate Review — Protocol 6.5 P13

## 1. Disposition

**NO-PASS.**

The semantic Review target is exact immutable P13:

`05a2b62550adadf271a27f6555da7173902c491c`

against accepted Protocol 6.4 control P0:

`55c085261eb827e3047637d045a8e6917ea6b962`.

The binding and readiness descendants were used only for mutable lifecycle and qualification evidence. They were not
substituted for P13.

One genuine D4 blocker survives fresh independent out-of-matrix falsification:

**B65-P13-1 — self-hosted PEM accepted-base/evidence realization remains local-Git-overlay-sensitive.**

P13 correctly canonicalizes governed release-state ancestry/content in `source/release_state.py`, but
`source/project_engineering_memory.py` still realizes accepted-project containment, immutable authority/evidence
content, repair-acceptance chronology, and recurrence chronology through ordinary Git revision traversal/content reads.
Active `git replace` refs and deprecated `.git/info/grafts` can therefore redefine evidence that the validator treats
as an exact immutable accepted-project relation.

This is material because `PROJECT-ENGINEERING-MEMORY.md` contains current `AUTHORITY_BOUND` memory, the PEM
validator is an ordinary Protocol build gate, and Protocol 6.5 explicitly self-applies exact accepted/base PEM and
immutable evidence-binding semantics to SSDP itself.

No Serious Challenge is raised. Accepted Protocol 6.5 D3 is coherent and already requires exact immutable accepted
project state/evidence, self-application, evidence-claim congruence, and explicit accepted/base PEM identity. The defect
is an incomplete D4 concretization in the existing PEM validator.

P13 remains immutable. Any semantic repair requires a new immutable candidate identity.

## 2. Independence and evidence boundary

This Review reconstructed the accepted Protocol 6.5 D3 design, D3->D4 handoff, current source owners, P13 production
behavior, current lifecycle state, and P0/P13 preservation independently before using prior failed-candidate Reviews as
hypothesis sources.

Mechanical evidence was treated only within its oracle scope:

- exact P13 workflow `36127313841`: completed success at exact P13;
- binding workflow `36127440732`: completed success at the P13 binding descendant;
- readiness workflow `36127652673`: completed success at the current readiness descendant.

Those clean runs do not exercise adversarial local replace/graft state and therefore do not establish canonical Git
semantics for every self-hosted validator.

## 3. Serious Challenge pass

**SERIOUS CHALLENGE: NONE.**

Accepted Protocol 6.5 D3 remains jointly coherent and realizable. In particular it already requires:

- SSDP self-application;
- exact immutable project/evidence identity where authority-bearing PEM is mechanically realized;
- accepted/base PEM selected by explicit project integration policy rather than branch/default/latest/timestamp;
- evidence claims bounded to what their realization method actually establishes;
- one current semantic owner and no hidden second control plane;
- fresh out-of-matrix semantic Review rather than CI as semantic acceptance.

B65-P13-1 contradicts none of those contracts. It shows that one D4 validator still delegates exact accepted-state
meaning to overlay-sensitive local Git behavior.

Earliest affected implementation owner: **D4 `source/project_engineering_memory.py`**, specifically its Git
realization/chronology helpers.

## 4. Mandatory P12 repair falsification

### 4.1 B65-P12-1 — canonical release-history ancestry

The P13 `source/release_state.py` repair is materially correct at its production owner:

- `_commit_and_parents()` resolves commits with `--no-replace-objects` and parses raw `parent` headers;
- `_canonical_is_ancestor()` traverses those raw canonical parents;
- `_check_ancestor()` uses that canonical relation for Review, ratification, publication, and recovery lineage;
- immutable evidence/version/recovery-state reads use `--no-replace-objects`;
- owner path membership uses canonical tree inspection;
- unavailable required canonical objects fail closed.

A fresh production-semantic holdout beyond the authored P13 tests replaced a canonical version commit with a commit
declaring `9.9.9`. Ordinary `git show <sha>:source/PROTOCOL_VERSION` read `9.9.9`, while the exact P13
`_check_version_ref()` command path read the canonical `6.5.0` bytes and produced no error.

Within the release-state owner, B65-P12-1 is closed.

### 4.2 B65-P12-2 — owner-history continuity

P13's `_governed_owner_history_is_continuous()` independently traverses the complete reachable canonical DAG,
records owner-path presence, and propagates governance forward from parents. Any owner-absent commit after a governed
parent remains fatal even if a later material transition or evidence-only descendant is current.

The P13 reconciliation correctly preserves predecessor discovery after detecting invalid history; the continuity error
remains fatal while independently useful transition diagnostics are retained.

A fresh genuine-pre-owner merge holdout beyond the authored P13 tests constructed a pre-owner branch and merged it
into an already-governed branch while retaining the owner. The exact P13 continuity algorithm accepted the topology
with no errors. This confirms the repair does not collapse a genuine pre-owner merge parent into a governed deletion.

Within the release-state owner, B65-P12-2 is closed.

## 5. B65-P13-1 — PEM accepted-state realization is overlay-sensitive

The full assembled candidate has another Git-semantic consumer on the mandatory build path:
`source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md`.

Production paths include:

- `_validate_accepted_project_route()`:
  ordinary `cat-file`, ordinary `merge-base --is-ancestor`, and ordinary `rev-parse <rev>:<path>`;
- `_validate_owner_binding()` and `_validate_accepted_authority_evidence()`:
  the same accepted-project route realization;
- `evidence_route_health()`:
  ordinary `cat-file` and ordinary `show <immutable-revision>:<path>`;
- `_validate_repair_acceptance_routes()`:
  ordinary `merge-base --is-ancestor` and ordinary immutable-content reads;
- `_validate_recurrence_structure()`:
  ordinary `merge-base --is-ancestor` chronology checks;
- `_git_patch_id()`:
  ordinary `git show` bytes for an independence heuristic.

These are live paths. Current P13 `PROJECT-ENGINEERING-MEMORY.md` contains an `AUTHORITY_BOUND` preservation
capability whose owner and authority evidence bind to exact accepted P0, so the authority-binding path is exercised by
normal self-hosted validation.

### 5.1 Fresh replace-ref ancestry holdout

A real temporary repository was constructed with canonical sibling commits `L` and `R`. Canonically, `L` is not
an ancestor of `R`.

A replacement object for `R` was installed with `L` as its parent.

Observed:

```text
ordinary merge-base --is-ancestor L R              -> true
--no-replace-objects merge-base --is-ancestor L R -> false
raw canonical parent of R                          -> original base, not L
```

Therefore the exact ancestry primitive currently used by `_validate_accepted_project_route()` can accept a route as
contained by an accepted project state when the canonical commit graph says it is not.

### 5.2 Fresh graft ancestry holdout

The same sibling construction was repeated using deprecated `.git/info/grafts`.

Observed:

```text
ordinary merge-base --is-ancestor L R              -> true
--no-replace-objects merge-base --is-ancestor L R -> true
raw canonical parent of R                          -> original base, not L
```

This is important: adding only `--no-replace-objects` to `merge-base` would still be wrong for the accepted-project
containment relation. Canonical ancestry must use raw commit-parent authority, as the P13 release-state owner already
does.

### 5.3 Fresh immutable-content holdout

A canonical evidence commit contained:

```text
CANONICAL OWNER
```

A later commit containing `FORGED OWNER` was installed as its replacement object.

Observed:

```text
ordinary git show <canonical-sha>:owner.md              -> FORGED OWNER
git --no-replace-objects show <canonical-sha>:owner.md -> CANONICAL OWNER
```

The exact production primitive used by PEM evidence/owner realization can therefore attribute noncanonical bytes to an
immutable evidence SHA.

### 5.4 Consequence

All authored P13 tests and normal clean CI can remain green while production still:

- accepts a noncanonical accepted-project ancestry relation;
- reads noncanonical immutable authority/evidence content;
- validates recurrence/repair chronology against locally rewritten topology;
- evaluates copied-event independence from replacement-object bytes.

That is the required local-compliance/global-failure trajectory. The root release-state validator can be fully
canonical while another mandatory self-governance validator silently uses a different Git reality.

## 6. Qualification-method challenge

For the material PEM oracles, the smallest wrong production implementation that can still pass current qualification
is the implementation P13 already contains: ordinary Git traversal/content reads in a clean repository.

The current Protocol 6.5 PEM tests cover reconciliation, schema parity, healthy/unavailable bindings, recurrence
structure, and authority-bound requirements, but contain no replace-ref, graft, or `--no-replace-objects` holdout.
Clean CI therefore proves those predicates only under ordinary local Git state.

The qualification prose overclaims if it generalizes that clean-state result to immutable accepted-project/evidence
identity under arbitrary local Git overlays.

By contrast, the P13 release-state oracles now directly discriminate replacement/graft topology and replacement-object
content. Their claims are appropriately bounded.

## 7. Historical blocker-family re-falsification

Current-owner disposition after fresh inspection:

| Blocker family | Current P13 owner result |
| --- | --- |
| B65-P12-1 canonical release-history ancestry | CLOSED at `release_state.py`; raw canonical parents and replacement-disabled immutable reads |
| B65-P12-2 owner-history continuity | CLOSED at `release_state.py`; complete canonical DAG continuity pass |
| B65-P11-1 ancestry/readability completeness | CLOSED; unresolved canonical commit/tree/blob/path fails closed |
| B65-P10-1 incomplete ancestry vs genuine pre-owner | CLOSED; negative pre-owner classification requires complete canonical ancestry |
| B65-P9-1 governed deletion vs pre-owner | CLOSED; post-governance owner absence remains distinguishable and fatal |
| B65-P8-1 predecessor resolution / merge ordering | CLOSED; direct canonical parent boundaries, not date/default traversal order |
| B65-P7-1 transition continuity / recovery lineage | CLOSED at release-state owner; exact state transitions and canonical recovery lineage retained |
| B65-P6-1 strict root-state parser convergence | CLOSED; unique-key loader owns release-state parsing |
| B65-P6-2 semantic-version/history ordering | CLOSED; canonical semver tuple ordering and historical/accepted constraints remain |
| B65-P5-1 duplicate-key root ambiguity | CLOSED by strict unique-key YAML loading |
| B65-P5-2 candidate/history succession/collision | CLOSED by active-successor and collision constraints |
| B65-P4-1 evidence-front-matter ambiguity | CLOSED by strict unique-key front-matter parsing |
| B65-P3-1 exact Review/ratification subject binding | CLOSED by explicit subject extraction and disposition matching |
| B65-P3-2 current representation convergence | No new P13 regression found; source/generated/package gates remain green |
| B65-P2-1 / B65-R2 duplicated mutable lifecycle ownership | No new duplicate lifecycle owner found; root release-state remains sole mutable release owner |
| B65-P2-2 / B65-R1 immutable Review evidence applicability | CLOSED in release-state validator; B65-P13-1 is a distinct PEM accepted-state/evidence realization defect |
| B65-R3 predecessor-version gating | No recurrence found in current 6.5 workflow semantics |

The new finding is deliberately not relabelled as a surviving P12 release-state defect. It is a separate D4
self-application failure in the PEM validator.

## 8. DF-1 through DF-4 and P65-1 through P65-6

- **DF-1 lifecycle ownership:** release-state ownership and corrected publication order remain coherent; no new root
  lifecycle blocker beyond the PEM self-governance issue.
- **DF-2 qualification/Review epistemology:** canonical doctrine remains sound. B65-P13-1 demonstrates why semantic
  out-of-matrix Review is necessary and why clean structural CI cannot overclaim immutable Git semantics it never
  adversarially exercises.
- **DF-3 meta-control governance:** no defect found in materiality, Serious Challenge, explicit stakeholder
  ratification, or acceptance separation.
- **DF-4 self-application/convergence:** **NO-PASS at D4** because self-hosted authority/evidence validation does not
  preserve exact immutable Git meaning under local overlays.

Principle usefulness remains causal:

- P65-1 exposes the self-hosted PEM validator as governed rather than exempt;
- P65-2 continues to prevent mutable lifecycle truth from becoming version semantics;
- P65-3 exposes the mismatch between an immutable-evidence claim and overlay-sensitive realization;
- P65-4 is the reason this out-of-matrix defect was found despite clean CI;
- P65-5 supplies the exact accepted/base PEM requirement that the validator must concretize;
- P65-6 remains useful for current-owner convergence and shows no new P13 representation drift.

The blocker therefore supports, rather than challenges, the accepted P65 design.

## 9. Preservation, historical capability, generated convergence, and Protocol 7 isolation

No additional preservation blocker was found.

Independent exact-tree comparison establishes that all frozen Protocol 5.16 and 6.0-6.4 Orchestrator
`profile.json` / `prompts.md` blobs are byte-identical P0 -> P13.

All active Protocol 7 parent/revision D3/D4 workplan blobs are also byte-identical P0 -> P13.

The P9 -> P13 semantic implementation interval modifies only the release-state implementation/tests plus lifecycle,
qualification, and workplan evidence. It does not reopen the older 5.13-6.4 scientific/software doctrine or mutate
the preserved Protocol 7 architecture.

Current exact P13 workflow success continues to support generated package parity, current snapshot parity, full
protocol regression, and Orchestrator Core acceptance within those mechanical oracle scopes.

Historical capability preservation is therefore not the reason for NO-PASS.

## 10. Simplicity and total-system complexity

The P13 release-state repair is appropriately narrow: it reuses raw Git object authority and adds no branch/default/
latest/timestamp owner, transaction registry, replay engine, or candidate-specific mechanism.

B65-P13-1 should be repaired with the same discipline. Do not add a second topology registry/service or a PEM-specific
history database merely to defeat local overlays.

## 11. Required D4 repair contract

Reopen only the current PEM validator implementation and its directly affected tests/qualification evidence.

Minimum required repair:

1. **Canonical immutable content.** Every local Git content/object read that can establish accepted/base PEM,
   authority/evidence binding, repair acceptance, recurrence chronology, or independence must prevent replacement
   objects from changing bytes attributed to an immutable commit.
2. **Canonical ancestry.** Accepted-project containment and recurrence/repair chronology must derive ancestry from raw
   canonical commit parents. Do not rely on ordinary `merge-base --is-ancestor`; adding only
   `--no-replace-objects` is insufficient because grafts still rewrite revision traversal.
3. **Fail closed.** Unavailable required canonical commit/tree/blob/path objects must degrade to the existing
   unavailable/review-required/error state rather than becoming a negative or positive ancestry/content proof.
4. **Preserve legitimate object storage.** Readable alternates/promisor-backed canonical objects must remain usable
   when Git can resolve the required raw objects.
5. **Canonical patch evidence.** If patch-id remains as the replaceable copied-event heuristic, derive the patch bytes
   from canonical commit content rather than replacement-object content.
6. **One Git authority mechanism.** Prefer reuse/consolidation of the raw-parent canonical mechanism already proven in
   `release_state.py`; do not independently grow two durable ancestry algorithms if a small shared implementation
   utility can reduce duplication without becoming semantic authority.
7. **Fresh production holdouts.** Add real temporary-Git tests covering:
   - sibling accepted-project containment under `git replace`;
   - the same under `.git/info/grafts`;
   - immutable owner/evidence content under replacement refs;
   - at least one live `AUTHORITY_BOUND` owner/evidence consumer;
   - repair-acceptance or recurrence chronology under an overlay;
   - unavailable canonical objects and a readable alternate store.
8. **Regression closure.** Re-run the complete protocol build/Core gates, PEM schema/reconciliation tests, release-state
   overlay tests, generated/package parity, frozen-resource checks, and affected P65-1/P65-3/P65-5 falsification.

Do not mutate P13. The repaired semantic state, after exact-candidate normal CI succeeds, must be frozen as a new
candidate identity and later bound at Review `NOT_RUN` before another genuinely fresh independent assembled-candidate
Review.

## 12. Lifecycle boundary

This NO-PASS does not:

- ratify Protocol 6.5;
- publish the 6.5 public fallback;
- establish recovery;
- advance `accepted_current`;
- merge PR #33;
- mutate Protocol 7 D3/D4.

The authorized next stage is only the bounded B65-P13-1 D4 repair and replacement-candidate qualification.
