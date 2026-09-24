---
kind: ssdp65-p2-repair-qualification
status: repair-complete-candidate-frozen
protocol_version: 6.4.0
target_protocol_version: 6.5.0
p0: 55c085261eb827e3047637d045a8e6917ea6b962
failed_p1: b565e28aeacea002cefe27e6b9594fe99d653c0a
p2: e8edb353e172aef933ed5e58eeabe897d0cc98d1
exact_p2_pr_run: 35996488794
date: 2026-09-24
d3_reopened: false
serious_challenge: none
---

# Protocol 6.5 P2 Repair Qualification

## 1. Scope and identity

This record qualifies the bounded D4 repair ordered by the fresh independent P1 Review.

- accepted control P0: `55c085261eb827e3047637d045a8e6917ea6b962`
- immutable failed P1: `b565e28aeacea002cefe27e6b9594fe99d653c0a`
- replacement immutable candidate P2: `e8edb353e172aef933ed5e58eeabe897d0cc98d1`
- exact-P2 normal pull-request qualification: run `35996488794`

P1 remains the immutable failed Review subject. P2 is a new candidate identity; no P1 Review result is transferred to P2.

The accepted P65 D3 design was not reopened. No Serious Challenge was raised.

## 2. B65-R1 closure — Review evidence binds the exact candidate

Owner repaired: `source/release_state.py` and focused release-state tests.

The existing release-state validator now:
- parses immutable evidence routes as repository + commit + repository-relative path;
- rejects wrong-repository and unsafe parent/absolute paths;
- requires the evidence commit and path to resolve in Git;
- parses Review YAML front matter;
- requires the Review record to bind the current `candidate.semantic_ref`;
- requires Review record disposition to agree with `candidate.review.state`;
- applies minimal immutable-route existence validation to terminal ratification evidence without attempting to machine-judge arbitrary ratification prose.

Focused counterfactuals cover exact binding, wrong candidate, disposition mismatch, wrong repository, missing commit and missing path.

This closes the P1 failure where regex shape could masquerade as candidate-bound Review evidence.

## 3. B65-R2 closure — mutable lifecycle phase is no longer copied into tests

Long-lived tests no longer assert that the live candidate must remain `NOT_RUN`, `NOT_REQUESTED`, or publication/recovery `UNAVAILABLE`.

The equivalent inherited Protocol 6.4 test family was also repaired:
- immutable 6.4 public/recovery identity remains tested whether 6.4 is accepted-current or historical;
- the live 6.5 Review phase is not copied into the inherited 6.4 test.

Freeze-time phase facts remain in immutable qualification/Review evidence. The executable suite tests lifecycle invariants and legal/illegal transitions rather than acting as a second mutable lifecycle owner.

## 4. B65-R3 closure — inherited safeguards are no longer predecessor-gated

The canonical current workflow prompt no longer conditions inherited exact-contract, Review, Verification, Stabilization, audit or closeout obligations on the phrase `Protocol 6.4`.

The six operational predecessor gates were generalized in the canonical source and the 6.5 prompt/profile were regenerated from that owner. A structural current-source guard rejects reintroduction of `Protocol 6.4` into the canonical workflow prompt; this guard claims only the syntactic current-representation property, not arbitrary prose semantic correctness.

Generated 6.5 prompt source digest changed from:
`7a15b110af011937f203c4dae6c215e6aedacc3fc4a846028bd83c82d18ec7cf`
to:
`fece917a2bc4a19964c16a500b7f474c7133d99396d4db68dfff13b0434e1b08`.

## 5. Exact-P2 mechanical evidence

Normal repository PR workflow run `35996488794` evaluated exact P2 and passed:

- repository release-state validation;
- Project Engineering Memory validation;
- complete inherited protocol unittest regression;
- canonical skill package build;
- independent package validation;
- committed distribution parity;
- whitespace;
- packaged Protocol 6.5 snapshot parity;
- Orchestrator Core acceptance.

This establishes only the executable/structural properties those oracles discriminate. It is not semantic Review PASS.

Development failures at intermediate repair commits remain historical failed observations and are not rewritten as passes.

## 6. Simplicity and preservation checks

Independent measurement after repair:

| Measure | P0 | P2 |
| --- | ---: | ---: |
| universal kernel words | 2,642 | 2,642 |
| D1/D2/D3/D4 hot owner contexts | unchanged from P1; each remains 3 words below P0 | preserved |
| defined hot-current projection | 10,540 | 7,354 |
| accepted-6.4 public-fallback SHA copies in that scope | 20 | 0 |
| accepted-6.4 recovery SHA copies in that scope | 12 | 0 |

P2 therefore reduces the already-compressed P1 hot-current projection by a further 15 words rather than adding compensating machinery.

Frozen orchestrator resources for Protocol 5.16 and 6.0–6.4 were compared by Git object identity across P0/P2: 12 paths compared, 0 differences.

No Protocol 7 D3/D4 mutation was introduced by this repair.

## 7. Candidate boundary

P2 is frozen at `e8edb353e172aef933ed5e58eeabe897d0cc98d1`.

A later descendant may bind that already-existing SHA into mutable release state and the independent-Review handoff. That descendant is lifecycle evidence, not P2.

P2 Review state must begin `NOT_RUN`; stakeholder ratification remains `NOT_REQUESTED`; public fallback and recovery remain `UNAVAILABLE`; accepted-current remains Protocol 6.4.

A fresh context that did not author P2 must perform the next assembled-candidate Review. This repair/authoring context cannot self-issue that Review PASS.
