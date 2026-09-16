---
kind: ssdp64-independent-protocol-review
protocol_version: 6.4.0
reviewer: GPT-5.6 Sol
date: 2026-09-15
authority: independent-review-evidence
status: no-pass
accepted_baseline_repository_state: 0928accd337a13f864b292ed81c36372828cfb4c
accepted_baseline_protocol: 6.3.0
assembled_review_target: 31818ca1c64548abda355d9be03fb5b353f5a43a
assembled_review_target_ci: 35037085174
handoff_descendant: 718747381f1ff8c483c7af1556d1704911fa68cb
blockers: 2
serious_challenges: 0
stage_f_authorized: false
protocol_64_recovery: unavailable
---

# Protocol 6.4 Independent Stage-E Review — 31818

## Disposition

**INDEPENDENT STAGE-E REVIEW: NO-PASS.**

No Serious Challenge to accepted Protocol 6.3 authority or to the Protocol 6.4 D1-D4 semantic doctrine was found. Two genuine D4 qualification/lifecycle blockers remain in immutable assembled target `31818ca1c64548abda355d9be03fb5b353f5a43a`: B64-R8 and B64-R9. Stage F is not authorized.

The Review reconstructed the candidate independently from accepted Protocol 6.3 repository state `0928accd337a13f864b292ed81c36372828cfb4c`, the current consolidated Protocol 6.4 workplan, and the assembled candidate itself. Bound descendant handoff `718747381f1ff8c483c7af1556d1704911fa68cb`, exact-target ordinary PR CI `35037085174`, earlier Stage-C/Stage-D records, and prior Review records were treated as evidence to challenge rather than authority.

## Independent reconstruction and falsification

The Review re-examined all preservation obligations `P64-A..P64-O`, qualification families `QF64-A..QF64-P`, and falsification passes `F64-A..F64-L` rather than limiting review to B64-R6/B64-R7.

The canonical Protocol 6.4 owners remain coherent on the substantive semantic model: source-level availability is distinct from runtime context availability; current semantic ownership cannot be selected by file/latest/routing order; definitions do not manufacture existence/truth/convergence/adequacy; semantic roles and provenance dimensions remain orthogonal; material family/instance/default bindings are explicit; external imports require exact source/variant/locator/assumptions and remain inert data; warrant/validity relations remain typed; `USES_DEFINITION` is stored as `subject -> prerequisite` with prerequisite-change impact found by reverse traversal; ordinary hyperlinks/import/call graphs are not semantic-definition edges; and partial traces cannot prove global independence. D1/D2/D3/D4 local consequences preserve their abstraction boundaries.

The prior SC64-R1 and B64-R2..B64-R7 findings are materially closed at the semantic/previously identified qualification surfaces. In particular, QF64-H now includes theorem/result subject coverage and direction/impact mutants, and the authority-index lifecycle helper no longer hard-codes a historical blocker label.

Frozen Protocol 6.3 profile resources remain byte-identical at the inspected target, including `ssdp-protocol-6.3/profile.json` blob `bef61c9ed9e1f273770feb01704e648d1fa0720b` and `ssdp-protocol-6.3/prompts.md` blob `67f3784dcc7ae259472d176498cc9e4556292898`. Exact-target run `35037085174` passed repository regression, canonical package build, independent package validation, committed-distribution parity, whitespace, packaged-snapshot parity, and the full Orchestrator Core suite. Those green results are applicable execution evidence but cannot close omitted qualification counterfactuals.

The authorized Protocol 6.4 public bootstrap `e09a9d1480211eea2d16d722182bb5c6de1bee12` remains self-reference-safe: its canonical prompt source still carries the pre-publication `UNAVAILABLE_PENDING_6_4_BOOTSTRAP` sentinel, while later descendant `142992f6f77025be938376b0fbd680ce9851edb9` publishes the immutable mapping. The current findings are D4 qualification/lifecycle-oracle defects and do not require a semantic-source mutation, so they do not by themselves invalidate that bootstrap. Protocol 6.3 remains accepted-current and Protocol 6.4 recovery remains absent.

Protocol 7 remains isolated: Revision 4 retains `d3_architecture_mutation: none` and `PROTOCOL 7 D4 IMPLEMENTATION: NOT AUTHORIZED`.

## Blocking finding B64-R8 — QF64-P still makes the PASS handoff state impossible

**Earliest owner: D4 Protocol 6.4 qualification/current-lifecycle oracle.**

The R7 repair correctly generalized `protocol64_lifecycle_state_ok` so the authority index can represent a truthful future state `PASS / STAGE F AUTHORIZED` with `PROTOCOL 6.4 RECOVERY: UNAVAILABLE PENDING STAGE F RECOVERY PUBLICATION` and `STAGE F: AUTHORIZED`.

However, `test_qf64_p_one_current_snapshot_complete_handoff` still unconditionally requires the real handoff metadata to contain:

```text
protocol_64_recovery: unavailable_pending_independent_review
stage_f: blocked_pending_independent_review
```

before it branches on the recognized lifecycle phase. The same test then explicitly accepts the `pass` phase and requires the target binding to remain bound. Therefore a truthful independent-PASS transition has no coherent representation that satisfies the oracle: updating the handoff to Stage-F-authorized truth fails the unconditional assertions, while retaining the pre-Review handoff values makes the current handoff stale.

This is not a merely future cosmetic problem. QF64-P exists to prove that current lifecycle truth can move through the authorized transition without checker rewrite-by-incident. As written, Stage F cannot be entered truthfully under the existing oracle.

### Required repair for B64-R8

Repair the existing QF64-P lifecycle model, not by adding a wrapper or another lifecycle authority. Validate a coherent **pair** of authority-index state and handoff metadata by phase:

- `repair-required` / `repair-complete` / `review-ready`: Protocol 6.4 recovery remains unavailable pending independent Review and Stage F remains blocked;
- `pass`: independent Review is PASS, target binding remains bound to the reviewed immutable candidate/evidence, Protocol 6.4 recovery remains unavailable **pending Stage-F recovery publication**, and Stage F is authorized;
- no phase may manufacture or self-name a recovery SHA.

Add a known-broken counterfactual where the index says PASS/Stage-F-authorized but handoff metadata remains in the pre-Review blocked state; it must fail. Add the converse mismatch as well. Historical blocker labels remain review history, not lifecycle invariants.

## Blocking finding B64-R9 — mandatory QF64 counterfactual matrix is materially incomplete

**Earliest owner: D4 Protocol 6.4 qualification oracle, concretized by `tests/test_protocol_64_axiomatic_traceability.py`.**

The governing testing owner requires Protocol 6.4 qualification to pair every material semantic-definition/traceability claim with discriminating positive and negative cases and explicitly says the counterfactual set **must include** ambiguous binder shadowing, unsupported/wrong-version imported citations, `USES_DEFINITION` traces that misclassify hyperlinks/call graphs, and runtime inference that does not load the exact required owner, among the other named classes. The consolidated workplan likewise makes QF64-A..QF64-P and their subcases mandatory.

The current synthetic predicates/fixture matrix does not discriminate that complete contract. Representative accepted-but-wrong cases include:

1. **QF64-A external import identity/support.** `qf_a` requires only truthy `meaning`, `source`, `locator`, and `assumptions`. It has no source-variant/version or support/admissibility discriminator. A wrong-version or unsupported citation can therefore satisfy the helper if those four fields are truthy. The negative matrix only mutates `defined`, `conflict`, and `locator`.
2. **QF64-C binder/provenance semantics.** `qf_c` checks primitive signature, binder scope/domain, and presence of a role, but it has no ambiguous-shadowing discriminator and no test of the required orthogonality between availability/provenance basis and semantic role. The negative matrix contains no shadowing/provenance-role mutant.
3. **QF64-E well-definedness coverage.** The helper has coarse `relation`, `logic`, and `totality` gates, but the negative fixture matrix does not exercise those failure branches and has no branch-selection or state/time/order ambiguity mutant required by QF64-E. The current green test therefore does not evidence those named counterfactuals.
4. **QF64-G/K unexercised required branches.** `qf_g` contains a `widened` validity guard and `qf_k` contains a `split_merge`/lineage guard, but neither is exercised by a negative fixture, so removal/regression of those guards would leave the declared counterfactual suite green.
5. **QF64-H typed-edge classification.** `qf_h` now correctly checks theorem/result subject coverage, endpoints, direction, reverse impact, bounded independence, and recursion, but it has no representation of the **kind/source of the purported edge**. A hyperlink/call-graph edge mislabeled as `USES_DEFINITION` passes whenever the other synthetic fields are valid, despite the canonical evidence owner expressly forbidding that classification.
6. **QF64-M exact runtime owner identity.** `qf_m` checks only `source`, `loaded`, and `edge_activates`. It cannot distinguish loading the exact version-bound canonical owner required by the inference from loading a similarly named/wrong-version owner while the actual prerequisite is merely discoverable.

These are not requests for a semantic theorem prover. Every case above is the bounded, mechanically expressible **counterfactual polarity** already required by the testing owner/workplan. The source doctrine itself already supplies the semantic rule; the defect is that qualification claims closure without a mutant capable of falsifying several required wrong concretizations.

### Required repair for B64-R9

Extend the existing bounded QF64 fixture/oracle only. Do not create a semantic registry, universal graph, citation database, or second authority layer.

At minimum:

- QF64-A: represent exact variant/version/locator identity and a structural support/applicability flag; reject wrong-version and explicitly unsupported imports without pretending the checker can establish real literature truth;
- QF64-C: represent ambiguous shadowing and provenance/role conflation; reject both while retaining open/extensible role vocabulary;
- QF64-E: add direct negative fixtures for relation/logical direction, partial-as-total, branch ambiguity, undefined operator, and material state/time/order ambiguity already named by the workplan;
- QF64-G: execute the widened-validity negative;
- QF64-H: add a relation-kind/source discriminator and mutants for hyperlink/import/call-graph/evidence-execution edges mislabeled as semantic-definition edges;
- QF64-K: execute unreconciled split/merge lineage negative;
- QF64-M: bind required-owner identity/version separately from loaded-owner identity and reject a wrong-owner/wrong-version loaded-context mutant;
- rerun the complete A-P polarity suite and ensure each mandatory workplan/testing-owner counterfactual has an executed discriminating negative or an explicit human-semantic-review boundary where mechanization would be dishonest.

## Obligation disposition

- `P64-A..P64-N`: no new source-semantic preservation blocker found.
- `P64-O`: **BLOCKED** by B64-R8 until the Review-PASS -> Stage-F transition can be represented truthfully end-to-end.
- `QF64-B`, `QF64-D`, `QF64-F`, `QF64-I`, `QF64-J`, `QF64-L`, `QF64-N`, `QF64-O`: no new blocking counterexample found.
- `QF64-A`, `QF64-C`, `QF64-E`, `QF64-G`, `QF64-H`, `QF64-K`, `QF64-M`: **BLOCKED** by B64-R9's incomplete mandatory counterfactual coverage. The earlier theorem/result/direction defects in QF64-H are closed; the remaining H defect is edge-class discrimination.
- `QF64-P`: **BLOCKED** by B64-R8.
- `F64-A..F64-D` and `F64-I`: no independent source-semantic blocker found.
- `F64-E/F64-F/F64-H/F64-J`: **TRIGGERED** B64-R9 through missing well-definedness, typed-edge, external-import, and exact-runtime-owner mutants.
- `F64-K/F64-L`: **TRIGGERED** B64-R8 through the inconsistent current-to-PASS lifecycle transition.

## Re-entry contract

After B64-R8/B64-R9 repair:

1. keep the repairs in the existing D4 qualification/lifecycle surfaces unless implementation discovers an actual source-semantic defect; do not change public-bootstrap/source doctrine merely to satisfy tests;
2. rerun focused Protocol 6.4 qualification plus the complete inherited repository regression, PEM validation where applicable, canonical package build, independent package validation, committed-dist parity, frozen-profile checks, packaged snapshot parity, full Orchestrator Core, and whitespace/index integrity;
3. freeze a **new immutable assembled candidate** because the qualification/lifecycle tree changes;
4. obtain applicable exact-target ordinary PR CI for that immutable target;
5. from a later descendant, bind the already-existing target SHA and exact-target CI without candidate self-reference;
6. perform another fresh independent full Stage-E Review over all `P64-A..P64-O`, `QF64-A..QF64-P`, and `F64-A..F64-L`, not merely B64-R8/B64-R9.

The existing public bootstrap `e09a9d1480211eea2d16d722182bb5c6de1bee12` remains authorized because these findings do not require public-source semantic mutation. If repair work unexpectedly changes canonical public-source semantics, the bootstrap lifecycle must be re-evaluated from its owning rule rather than presumed reusable.

Protocol 6.3 remains accepted-current. Protocol 6.4 recovery remains unavailable. Stage F remains blocked.

**Verdict: NO-PASS — blockers 2; Serious Challenges 0.**
