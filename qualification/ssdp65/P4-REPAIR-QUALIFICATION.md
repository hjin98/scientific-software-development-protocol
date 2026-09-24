---
kind: ssdp65-p4-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
failed_p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
failed_p3: 89ccc71a7b0e9458a3e77306be2a773d4059f0f2
p4: 43ff4273fbdaf46b9677cffdb091b741ce754a7d
exact_p4_pr_run: 36041360949
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P4 Repair Qualification

## 1. Scope and identity

This record qualifies the bounded D4/current-representation repair ordered by the fresh independent P3 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P1: `b565e28aeacea002cefe27e6b9594fe99d653c0a`
- immutable failed P2: `e8edb353e172aef933ed5e58eeabe897d0cc98d1`
- immutable failed P3: `89ccc71a7b0e9458a3e77306be2a773d4059f0f2`
- replacement immutable candidate P4: `43ff4273fbdaf46b9677cffdb091b741ce754a7d`
- exact-P4 normal PR qualification: run `36041360949`

P1-P3 remain immutable failed Review subjects. No prior Review verdict transfers to P4. The accepted P65 D3 design was not reopened and no Serious Challenge was raised.

## 2. B65-P3-1 closure — evidence subject is now unambiguous

The repair alters only the existing release-state evidence-binding owner.

`source/release_state.py` now resolves one evidence subject:

1. explicit `candidate_ref` / `semantic_ref` fields take precedence when present and must agree with each other;
2. otherwise legacy `pN` metadata resolves to the highest candidate generation, with lower `pN` fields treated as predecessor/control context;
3. absence or ambiguity rejects instead of becoming a set-membership success.

Review and terminal ratification both use the same helper. Arbitrary Review/stakeholder prose remains outside machine semantic judgment.

Fresh focused counterexamples added for both Review and ratification prove:

- a wrong explicit subject cannot be rescued by a matching historical `p3`;
- a `p3` + `p4` record binds P4, not P3;
- conflicting explicit `candidate_ref` / `semantic_ref` fields reject;
- a future P4-style sole/highest legacy subject remains accepted.

Existing wrong candidate, disposition mismatch, repository, unsafe path, missing commit/path and ordinary valid-binding coverage remains intact.

## 3. B65-P3-2 closure — current evidence doctrine is protocol-current

The residual current canonical sentence:

`Protocol 6.4 remains document-controlled...`

was replaced in its existing owner by protocol-current wording:

`These remain document-controlled reasoning obligations...`

No new section, wrapper, version table or compatibility layer was introduced.

A fresh bounded census covered all 34 current `source/shared/references/*.md` canonical owners and found zero occurrences of `Protocol 6.4`, `6.4.0`, or `predecessor`. Frozen historical resources were not edited.

The affected generated skill-package copies were regenerated from the canonical owner; committed ZIPs preserve the same semantic file trees.

## 4. Exact-P4 mechanical evidence

Normal repository PR workflow run `36041360949` evaluated exact P4 and passed both jobs completely:

- release-state validation;
- Project Engineering Memory validation;
- complete inherited protocol regression;
- canonical skill package build;
- independent package validation;
- committed distribution semantic parity;
- whitespace;
- packaged Protocol 6.5 snapshot parity;
- Orchestrator Core acceptance.

This establishes only the executable/structural properties those oracles discriminate. It is not independent semantic Review PASS.

## 5. Preservation and simplicity checks

Independent measurements after repair:

| Measure | P0 | P4 |
| --- | ---: | ---: |
| universal kernel words | 2642 | 2642 |
| defined hot-current projection words | 10540 | 7354 |
| accepted-6.4 public-fallback SHA copies in that scope | 20 | 0 |
| accepted-6.4 recovery SHA copies in that scope | 12 | 0 |

The one-line evidence-owner repair is outside the defined hot-current projection, so the P3 compression result is unchanged.

All 12 frozen Protocol 5.16 and 6.0-6.4 Orchestrator profile/prompt objects are Git-blob identical between P0 and P4.

No D1/D2/D3/formal-definition owner, PEM schema, Protocol 7 D3/D4 artifact, release-state architecture, or frozen predecessor resource changed.

## 6. Evidence applicability

P3-specific Review and exact-P3 whole-candidate qualification remain historical. They do not transfer as P4 closure.

Still-applicable evidence was reused only after changed-surface inspection:

- P0 baseline and accepted Protocol 6.4 authority;
- frozen-resource object identity;
- unchanged D1/D2/formal-definition semantics;
- B65-P2-1/B65-R2 lifecycle-transition/current-copy repair;
- Protocol 7 isolation.

P65-3 exact-subject evidence and P65-6 current-representation evidence were rerun for P4 because those were the changed claims.

## 7. Candidate boundary

P4 is frozen at `43ff4273fbdaf46b9677cffdb091b741ce754a7d`.

This candidate does not self-name as mutable current candidate. A later descendant may bind P4 in `PROTOCOL-RELEASE-STATE.yaml`, record the handoff, and carry qualification evidence without changing P4 semantics.

Review begins `NOT_RUN`; stakeholder ratification remains `NOT_REQUESTED`; public fallback and recovery remain `UNAVAILABLE`; accepted-current remains Protocol 6.4.

A fresh non-authoring context must independently Review P4. This repair context cannot self-issue that verdict.
