---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stage: final whole-entrypoint simplification (workplan section 16.11)
basis: 47dc85de6dd6be8b0adfb1a66024cfdd5397f3d8
frozen_before: any SKILL.md change of the final simplification and any run of the simplified candidate
---

# Protocol 6.6 Final Simplification — Frozen Routing Map and Qualification Contract

Evidence coordination only; not D1-D4 authority, Review, or release state. The commit that adds this file changes no `SKILL.md`, entry-contract owner or generated package. Its Git position therefore shows that the routing-preservation map and the pass rules were fixed before the simplified entrypoints existed. The machine-readable rule is `eval/scenarios.yaml` `final`; the map is `eval/routing-preservation-map.yaml`.

## 1. Routing-preservation map (16.11.3)

The map covers all 122 direct reference/template routes of the seven consumed entrypoints at `47dc85d`, including the two routes in the generated entry contract. It is organized as:

- **concerns** (32): each canonical target owner with positive and negative routing counterfactuals. The concerns cover D1, D2, D3, D4, workflow, evidence, testing, PEM, versioning, semantic definition, convergence, long-horizon health, repository intake, debugging, documentation, writing, release, Git, configuration, concurrency, security, performance, storage, language profiles, tool-assisted engineering and the four templates;
- **per skill**: every route, with its basis trigger quoted verbatim, the discriminating predicate terms, the concern it realizes and its disposition; skill-level gates (for example `only triggered`, `route when material`); exclusions (first-clean-local / in-envelope / local-design negatives, `ordinary hyperlinks`, `package membership`, `not activation`); and the role-local authority boundary;
- **entry contract**: the versioning and kernel routes and the 16.10.1 version-binding terms;
- **forbidden direct routes**: the PEM schema, workflow prompts, language leaves and tool leaves.

Dispositions: 115 PRESERVE. The seven per-skill universal-kernel routes are CONSOLIDATE, for one reason: their predicate is identical in all seven skills, and it moves into the generated entry-contract clause, which already links the same kernel owner. The result is one clause per entrypoint with the same predicate and the same owner, and no route is removed.

`tests/test_protocol_66_final_simplification.py` enforces the map on the consumed `dist/skills/*/SKILL.md`. It requires:

- exactly the basis direct-route set per skill;
- for each route, a clause that links the target and contains every predicate term, checked with link markup removed so that a label cannot stand in for its predicate;
- every gate, exclusion, authority and version term;
- no forbidden eager route;
- byte-identical catalog frontmatter.

At freeze the test passes on the basis entrypoints, which shows the terms were extracted faithfully. A negative test shows that the oracle rejects a label-only route, a dropped trigger, and a predicate detached from its link. Term preservation is necessary but not sufficient: material equivalence of each trigger against its quoted basis text remains a Review question.

## 2. Ordering oracle update (16.11.1 item 7)

`harness.ordering_events` now treats a call as part of the version decision only when **every** installed-SSDP path it names is a version-identity file: `PROTOCOL_VERSION`, `protocol-manifest.json`, the versioning owner, or the version helper. A call that also touches any other SSDP file, or that lists the package, remains protocol action. Mutation before the statement remains a failure. Unit cases cover the exempt identity read, identity bundled with doctrine, and a whole-package listing. As a diagnostic on the recorded `47dc85d` traces only (not a re-judgment): the six runs that failed solely on identity inspection become ordering-true, T5 r0 (never stated) and T5 r1 (mutation before statement) still fail, and T6 r0 still counts its package-wide Glob as protocol action. The same oracle applies to both variants of every final run.

## 3. Final qualification rule (16.11.4-16.11.5)

Variants: `v65` is accepted 6.5 `dist/skills` at `2b8ce17` (the criterion-4 baseline, unchanged). `v66b` is the redesigned basis `dist/skills` at `47dc85d`. `v66f` is the simplified candidate, whose exact commit is recorded before the runs. Executor `claude-sonnet-5`, headless, project-only settings. Blinded single-turn assessor `claude-opus-5-5` with the unchanged `6c76ef1` rubrics and hidden-oracle repairs.

Routing and correctness are lexicographically prior to burden. The final result passes only if **all** of the following hold.

| Item | Rule |
| --- | --- |
| structural routing | the map test and the full repository acceptance pass on the exact candidate |
| route probes (19 cases × 2 reps, `v66b` vs `v66f`) | a probe asks the agent to load exactly the owners its routing requires, without doing the task. A run hits iff the named root was invoked and every `expect` owner was read; it violates iff any `forbid` owner was read. Pass: no case with `v66b` 2/2 hits and `v66f` 0/2; no case with `v66b` 0/2 violations and `v66f` 2/2; total `v66f` hits ≥ `v66b` − 2; total `v66f` violations ≤ `v66b` + 2 |
| selection (existing corpus, 2 reps, `v66b` vs `v66f`) | correct `v66f` ≥ `v66b` − 2 out of 32; false activations `v66f` ≤ `v66b` + 1 |
| version regression (T6×4, T5×2, T4×2, `v66b` vs `v66f`, fresh paired) | stochastic robustness evidence, not a language proof (16.11.1). Strict pass = ordering field true and strict-rubric PASS. Pass: `v66f` strict passes ≥ `v66b` − 1; never-stated runs `v66f` ≤ `v66b` + 1. Report every failing run and self-adoption/non-closure observations. The deterministic preflight and the no-self-adoption structure remain hard repository tests |
| authority sentinels (T2×2, T3×2, `v66f`) | every run assessor PASS and hidden checks pass |
| criterion 4 | `redesign.burden_rule` unchanged: panel T1/T7/T8, 3 fresh paired runs of `v65` vs `v66f`, `observed_active_ssdp_bytes`, panel net ≤ 0.85, at least one direct route reduction with non-overlapping ranges, every route ≤ 1.10, collected hidden oracle and assessor parity |
| hygiene | no remote/source lookup or versioning-owner read in `v66f` T1/T7/T8 runs; every run isolated (each SSDP skill listed once, project-resolved); no run errors |

Gate computation: `eval/rework_gates.py assess-final` then `evaluate-final`, over `eval/results/final/{routes,selection,trajectory}`.

The route-probe and selection tolerances (±2 runs) and the version tolerance (1 run) bound stochastic noise at these sample sizes, and they were chosen before any candidate existed. Routing preservation itself is gated structurally without tolerance. On any failure, Protocol 6.6 stops under workplan 16.11.5. No rewording, route, metric, threshold, weighting or prompt layer may be added after the first final-candidate run.
