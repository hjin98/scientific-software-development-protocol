---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stages: F, G
evaluated_source: 3fac7d1c34822ba82785e0b41f6e340fd7cfa6d5
rework_semantic_state: c01eeee47989cbbf9ed5e87df50756c23d912f79
implementation_review: NO_PASS_R1 at 26059544204c65b1e0292cd229e95f61b5f970bb; NO_PASS_R2 at 390613b27d7304f08ee819d968a47119f48b57f9
ordering_oracle_freeze: f34ffef46c8e1dd635affc60e719c9f7996a2123
live_confirmation: R1/R2 matrix on dist/skills unchanged since c01eeee (FAILED both hard-stop gates; section 10.5)
---

# Protocol 6.6 Stages F-G — Empirical Evaluation and Assembled Qualification

Evidence coordination under the [Protocol 6.6 Evaluation and Qualification Contract](PROTOCOL-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT.md). It is not D1-D4 authority, a Review, or release state. It establishes only what its oracles discriminate; semantic adequacy of the assembled candidate still requires fresh independent Review.

## 1. Disposition

```text
SERIOUS CHALLENGE: RAISED (candidate; section 10.6) - versioning adoption/compatible-source
  semantics inherited from accepted 6.5 let executors self-adopt the loaded successor for
  older version-bound work; adjudication belongs to the reopened D3 / versioning owner
IMPLEMENTATION BLOCKERS: OPEN - D4 STOPPED; D3 REOPEN REQUIRED (workplan 16.8, 16.9 item 6)
  B1 R1 fresh-holdout confirmation: FAILED - T6 2/4 (hard stop: any T6 failure)
  B2 criterion 4 direct live burden reduction: FAILED on T1 and T7 (hard stop: both routes)
  B3 entry-ordering oracle: CLOSED - strengthened and frozen at f34ffef before any valid run
NEW CORRECTNESS REGRESSION vs 6.5 ON MATCHED CASES: none observed (T1-T3, T7; section 10.5)
READY FOR FRESH INDEPENDENT REVIEW: NO
CANDIDATE FREEZE / PUBLICATION / RATIFICATION / CUTOVER: NOT PERFORMED (Stage H)
```

Sections 1-9 record the original Stage F/G evidence on `3fac7d1`; they are retained, not rewritten. The implementation Review (NO-PASS R1) rejected two of their conclusions, and section 10 carries the current rework state. Where sections 1-9 conflict with section 10 or with the corrections below, the later text governs. Section 10.3 records the failed first attempt; sections 10.5-10.6 carry the valid live confirmation and its stop disposition.

Corrections required by the Review:

- Finding 1 below treated manual-mode compliance as a shared weakness to route to Protocol 7. The Review classified it as 6.6 nonconformance: a check that is not effective at the real execution boundary is proxy evidence, not closure. It is blocker B1.
- Finding 2 and criterion row 4 treated fewer missed selections as an intervention/activation burden gain. Selection accuracy is a separate quality metric; no intervention was measured. It is blocker B2.
- Section 2 reused T2/T3 across the `4f566b6 -> 3fac7d1` entrypoint change because no run read a changed reference. That reasoning is invalid: the invoked `SKILL.md` is part of every explicit-skill trajectory. T2/T3 evidence does not apply to any later entrypoint state.

**Material finding 1 — prose-only entry instructions are weakly followed (shared with 6.5).** In the reference harness no agent read the universal kernel or the D4 owner before acting, in any trajectory of either variant; the observed protocol context was the injected `SKILL.md`. Version-bound workplans (T4 6.4-bound, T5 6.3-bound holdout) were silently implemented by 6.5 in 4/4 runs; 6.6 stated the mismatch in 1/4 final-candidate runs (T4 1/2, T5 0/2) and 0/6 intermediate runs. The versioning doctrine is not false (the offline `version_preflight.py` and Orchestrator profile selection enforce it mechanically), so this is not a Serious Challenge to 6.5; it is not a 6.6 regression. It is material evidence that manual-mode compliance with prose entry checks is unreliable in this harness, routed to Review and to the required Protocol 7 D3 reopen (workplan §13, final trigger).

**Material finding 2 — the live burden gain is in activation, not in trajectory tokens.** Structural hot-path reduction is clear, and live selection improved beyond run noise, but trajectory turns/tokens/cost are unchanged within noise because agents in this regime load only the entrypoint, whose size 6.6 did not materially change. Review must judge whether the activation/intervention improvement satisfies workplan acceptance criterion 4 (see section 5).

## 2. Identities and regime

| Item | Identity |
| --- | --- |
| baseline semantic source | `7f7b5e24858e813e45ace867a7f8ea5180f43bf0` |
| baseline installed package surface | `dist/skills` at cutover `2b8ce17b1f086dc85e6fa8014c4a7bcc45ef60cb` (6.5.0) |
| main live-matrix candidate | `dist/skills` at `31730c042f3b0f7649df89056241fb1b2b16d271` (selection) / `4f566b624d9d9ad0ed38c74a99f4f1423f444dee` (trajectories) |
| final evaluated source | `3fac7d1c34822ba82785e0b41f6e340fd7cfa6d5` |
| evaluation freeze | Stage A commit `bdd2064` (`eval/scenarios.yaml`, fixtures, oracles); T4 reclassified and T5 added in `46e7b16` before the repaired candidate ran |
| harness | Claude Code 2.1.283 headless (`claude -p`, stream-json), project-installed skills, isolated sessions (invoking-session env stripped) |
| executor model | `claude-sonnet-5` (default reasoning); tools: Skill/Read/Glob/Grep/Edit/Write/python/git/read-only shell |
| assessor | fresh `claude-opus-5-5` context, single turn, no tools, blinded to variant (6.5/6.6 identifiers redacted), rubric fixed in `eval/rubrics.yaml` before assessment |

Confounders recorded: the ambient catalog also exposed ~30 non-SSDP user/account skills (identical across variants); runs were paired and order-counterbalanced within minutes; service drift over ~2 h is not excluded. Claims bind to this harness/model/install mode only; the OpenAI adapter and other harnesses were not exercised.

Changes after the main live matrix: `4f566b6 -> 3fac7d1` shortened the entrypoint version-check wording, removed two entrypoint restatements of the writing owner's terminology rule, and added one owner route to each D1-D4 domain owner. Selection metadata is unchanged since `31730c0`. T1/T4/T5 were re-run on `3fac7d1` (section 4.3); T2/T3 were not, because none of their runs read a changed file and the changed entrypoint text is not exercised by their decisions.

## 3. Structural evidence (layers 0-1)

Source: `eval/results/static-baseline-6.5.json` vs `eval/results/static-candidate-6.6.json` (`harness.py static`).

Catalog metadata (frontmatter): 2,230 -> 2,024 bytes (−9%); adapters unchanged (913 bytes).

| Route | 6.5 mandatory | 6.6 mandatory | Δ | 6.5 route closure | 6.6 route closure | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 local D4 repair | 38,187 | 28,463 | −25% | 38,187 | 28,463 | −25% |
| R2 D4 + workplan + tests | 38,187 | 28,463 | −25% | 72,996 | 64,187 | −12% |
| R3 D3 mature replacement (PEM) | 42,030 | 33,017 | −21% | 102,594 | 78,442 | −24% |
| R4 D2 specialized import | 36,100 | 27,279 | −24% | 36,100 | 37,419 | +4% |
| R5 D1 parameter/default binding (holdout) | 35,569 | 26,644 | −25% | 52,397 | 54,527 | +4% |
| R6 memory-governance update (holdout) | 33,456 | 24,414 | −27% | 61,189 | 59,353 | −3% |

R4/R5 grow slightly by design: the specialized owner (10 KB) now loads explicitly when its predicate fires instead of riding unconditionally inside the kernel. No fired concern is unreachable and no forbidden concern is eager on any route (`test_frozen_routes_fire_reachably_and_forbid_eager_loading`). Entrypoint `SKILL.md` totals: 45,061 -> 45,372 bytes (+0.7%; D4 −7%, others within ±5%).

## 4. Live evidence (layers 0, 2, 3)

### 4.1 Selection (16 scenarios × 2 variants × 2 reps, counterbalanced)

| Outcome | 6.5 | 6.6 |
| --- | ---: | ---: |
| admissible root selected | 17/26 | 23/26 |
| missed activation | 9/26 | 3/26 |
| false activation on negatives | 0/6 | 0/6 |
| wrong or extra root | 0 | 0 |

All six discordant scenario-rep pairs favor 6.6 (S03 r0, S04 r0/r1, H03 r1, H05 r0/r1; exact sign test p ≈ 0.03), three of them holdout. Both variants miss the mixed D4/D2 Monte-Carlo case S08 in every run. Mean input tokens per selection run: 98.5k vs 97.5k (dominated by harness system context; not a protocol signal). Raw: `eval/results/stageF/selection/`, `selection-summary.json`.

### 4.2 Trajectories (T1-T5, explicit-skill regime)

| Case | 6.5 assessed PASS | 6.6 assessed PASS | Deterministic oracle | Notes |
| --- | ---: | ---: | --- | --- |
| T1 first clean local repair | 2/2 | 2/2 (+2/2 confirm) | hidden tests pass, both | no protocol reference read in any run |
| T2 tolerance within envelope | 2/2 | 2/2 | bound-derived tolerance, method unchanged, both | no research-campaign escalation |
| T3 D2-owned default (holdout) | 2/2 | 2/2 | default unchanged, both | one 6.6 run loaded `semantic-definition-and-traceability.md` on its own |
| T4 6.4-bound workplan (dev after first use) | 0/2 | 0/2 main, 1/2 confirm | implementation correct, all | the passing run read the versioning owner and stated the mismatch |
| T5 6.3-bound workplan (holdout, added in F) | 0/2 | 0/2 (confirm) | implementation correct, all | — |

Paired totals over the ten main final-candidate runs (T1-T5 × 2): turns 114 vs 113, cost $1.54 vs $1.46, input tokens 3.60M vs 3.48M — differences inside run-to-run spread (e.g., T5 6.5 runs alone span $0.15-$0.25). Raw: `trajectory-6.5/`, `trajectory-6.6-final/`, `trajectory-6.6-confirmation/`; superseded/intermediate runs are retained in `trajectory-6.6-intermediate/` and `trajectory-6.5-superseded/`.

### 4.3 Repair history driven by evidence

1. T4 (then holdout) showed neither variant noticed the 6.4 binding with the check placed in the kernel, which no agent read. The check moved to every entrypoint (true execution entry); T4 became development data; T5 was added as fresh holdout before the repaired candidate ran.
2. A stronger imperative wording ("do this first") produced no observed change in a bounded 2-run iteration and was reverted to the compact wording (no burden without demonstrated value).
3. The initially rewritten descriptions grew catalog metadata by 27%; they were shortened to −9% before the live matrix.

No 6.6 mechanism was retained whose only justification was a live gain it did not show; the entry check is retained because workplan §5.11 requires the check at execution entry and the entrypoint is its cheapest location.

## 5. Acceptance-criteria reconciliation (workplan §11)

| # | Criterion | Evidence | Disposition |
| --- | --- | --- | --- |
| 1 | every accepted 6.5 capability mapped to a preserved owner/route | Stage A map (section 7 there) re-verified: section 6 below; sentence-level preservation tests for moved kernel sections | MET (structural); semantic adequacy for Review |
| 2 | inherited regression/package/profile/Core/frozen-history checks pass | section 7 | MET |
| 3 | new routing/context/state/version/eval counterfactuals pass | `tests/test_protocol_66_cognitive_optimization.py` (28 tests), Core 6.6 schema oracle | MET mechanically; live version counterfactual fails for both variants (finding 1) — superseded: blocker B1, section 10 |
| 4 | clear structural reduction + bounded live burden reduction beyond noise | −21…−27% mandatory closure; live: missed activations 9 -> 3 (intervention/activation dimension), trajectory tokens/turns unchanged | STRUCTURAL MET; LIVE NOT MET — superseded: selection is not burden (blocker B2, section 10) |
| 5 | specialized/high-risk sentinels recover cold capability | route tests R4/R5/R6; T3 PASS both, one live load of the semantic owner | MET within scope |
| 6 | no mandatory orchestrator/service/vendor/model/subagent | doctrine + no-vendor-name test; harness optional/removable | MET |
| 7 | Working State/eval/summaries/indexes non-authoritative | workflow owner + tests; no Working-State artifact exists | MET (structural) |
| 8 | live evidence for any trajectory claim; claims regime-bounded | this record | MET — no trajectory-efficiency claim is made |
| 9 | no open Serious Challenge or material preservation gap | section 6 | MET, subject to Review |
| 10 | minimum-justified operational architecture, no second control framework | new permanent machinery: two reference owners (split, not added doctrine), `version_preflight.py` (95 lines, repository-only, not packaged), entry-check line; eval harness removable | MET |
| 11 | manual/portable use complete | skills self-contained; prompts complete; Orchestrator optional | MET |
| 12 | 6.5 working-state and version-resolution semantics consolidated, not duplicated | Working State extends the existing workflow section; entry check routes to the versioning owner | MET |
| 13 | discovery, transport, activation distinct and qualified | PORTABILITY four-boundary statement; transport/activation tests; live selection matrix | MET |
| 14 | admissible-root selection, no increase in missed/wasteful activation | section 4.1 | MET (decrease) |
| 15 | generic validity independent of vendor adapters | `test_generic_core_validity_does_not_require_vendor_adapter`; OpenAI adapter not live-qualified (no claim) | MET |
| 16 | durable scenario/provenance identities; independent assessment | section 2 | MET |
| 17 | 6.6 profile preserves pre-7 lifecycle/control semantics/schema | `test_protocol_66_preserves_pre7_lifecycle_control_schema`; 6.5 bytes frozen by blob hash | MET |

## 6. Final capability-preservation dispositions

Every row of the Stage A map is **PRESERVED** at its planned 6.6 owner/route, with these clarifications:

- semantic-definition (6.4): **PRESERVED / RELOCATED** — every 6.5 kernel sentence survives verbatim at the new owner or kernel (mechanical check); the hard availability invariant remains in the kernel; D1-D4 domain owners route to it.
- authority lifecycle/mutation (6.0): **PRESERVED / RELOCATED** to workflow — every 6.5 sentence survives verbatim (mechanical check).
- PEM (6.3/6.5): **PRESERVED / SPLIT** — agent contract + cold schema; HAS shape validator-parity and schema-field parity tests retargeted, not weakened.
- compact working state (6.2/6.5): **PRESERVED / OPERATIONALIZED** in the same owner.
- version-bound interpretation (5.16-6.5): **PRESERVED / STRENGTHENED MECHANICALLY**; live manual-mode compliance remains weak (finding 1).
- D4 real-owner/proxy-proof/fidelity sentinels (5.5-5.7): **PRESERVED** — exact accepted wording restored after the first rewrite paraphrased it.
- D1/D2 human-facing terminology rule (6.1): **PRESERVED** at the writing owner; the entrypoint restatement was removed as duplication.

No row is superseded or removed.

## 7. Executed acceptance (final source `3fac7d1`, re-run on the qualification head)

```text
python source/release_state.py                                        -> coherent (candidate 6.6.0 UNFROZEN / NOT_RUN)
python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md -> schema 1 valid, 5 families
python -m unittest discover -s tests                                  -> 380 tests OK (3 skipped: CI/remote-only)
python source/build_skills.py --output <tmp>                          -> OK
python source/validate_packages.py --dist <tmp>                       -> all bundles/ZIPs structurally valid
python source/check_dist.py --expected <tmp> --committed dist         -> parity OK
python orchestrator/scripts/generate_protocol_snapshot.py --check     -> 6.6 current; 5.16-6.5 frozen and coherent
python orchestrator/scripts/run_core_tests.py                         -> 383 tests OK
git diff --check                                                      -> clean
```

Remote public-fallback realization tests remain skipped outside CI, as for 6.5.

## 8. What Review should challenge first

1. Finding 1: whether 6.6 should strengthen manual-mode version enforcement further (e.g., packaged executable check) or leave it to Protocol 7's control plane; and whether declared "mandatory reads" that the reference harness skips undermine the tiny-kernel acceptance property.
2. Finding 2: whether activation/intervention improvement plus structural reduction meets acceptance criterion 4.
3. The kernel/entrypoint split: attempt a locally compliant D1-D4 trajectory that violates a universal invariant now carried only by the kernel.
4. PEM agent contract vs schema owner: attempt a memory-triggering decision that the agent contract lets through but the 6.5 single owner would have blocked.
5. The generality of the selection gain beyond Claude Code / `claude-sonnet-5`.

## 9. Deferred closeout-learning candidates (PEM)

The closeout-learning assessment runs at lifecycle closure after acceptance, against the then-current accepted memory basis. Candidates identified now, none admitted:

- `DS-001` — a further supporting application: static mandatory-closure structure did not predict observed context (agents loaded only entrypoints), reinforcing that structural evidence claims only structure;
- possible new discovery — prose-only entry/mandatory-read instructions were not reliably followed by the reference harness in either protocol version; admission needs broader harness/model evidence and a counterevidence search;
- `SP-002` — the accepted 6.5 release episode is a not-yet-recorded supporting application (noted in the memory front matter).

## 10. Implementation-Review rework state (workplan section 16)

### 10.1 R0 — frozen before repair

`REWORK-R0-FREEZE.md` (commits `c73fdd3`, `07af511`, both before any R1 change): fresh 6.2.0-bound holdout T6; ordinary unversioned workplan route T7 (its disclosed selection risk is recorded there); T4 reclassified as development data and T5 as a post-finding challenge case; the deterministic `entry_and_burden` trace oracle; and the predeclared burden metric and pass rule (`eval/scenarios.yaml` `rework`).

### 10.2 R1 — repair implemented (`c01eeee`)

- Every generated entrypoint carries one `## Entry contract` block inlined by `build_skills.py` at `<!-- SSDP-ENTRY-CONTRACT -->`: the versioning owner's marked step, which is an unconditional one-line governing-version declaration before the first file change or protocol-dependent decision, with no lookup when the answer is `none`; plus the kernel's `Universal invariant` block, extended to carry every section 5.1 hot-path element.
- One owner per element: the step lives only in `protocol-versioning-and-compatibility.md` and the invariant only in `abstraction-and-concretization.md`. `validate_packages.py` independently re-derives the block from each bundle's packaged owners and rejects drift or a missing placeholder (negative tests).
- The full kernel changed from a declared unconditional pre-reasoning read, which live agents skipped, to a predicate-routed owner. **Review should challenge this first:** the D4 argument is that section 5.1 requires the universal semantics to be always loaded and section 8 delegates the file partition. The inlined block is now the always-loaded tiny kernel, and the kernel file is its canonical owner and elaboration. If Review judges this a D3 change, reverting it is a one-sentence restoration per entrypoint and does not affect the version step.
- Structural effect (harness `static`, which now expands the inlined block): R1-route mandatory closure is 38,187 B at 6.5 and 17,205 B now. The consumed D4 entrypoint grows from 8,360 B (6.5) and 7,762 B (`3fac7d1`) to 9,816 B. That growth is the price of putting the universal contract in the consumed surface. Because observed Stage F runs loaded only the entrypoint, the T1 burden route is expected to **increase** under the frozen metric; this is stated before measurement and must not be explained away.
- No control plane, service, vendor dependency, or Orchestrator/profile change was added. `version_preflight.py` is unchanged.

### 10.3 Live confirmation — NOT EXECUTED (blocking)

The matched R1/R2 matrix (T6×4, T1×3, T7×3, T5×2, T4×2, T2×2, T3×2 per variant, 6.5 package at `2b8ce17` vs candidate `c01eeee`) was launched in Claude Code 2.1.218 headless. Every executor session ended after one turn with `Failed to authenticate: OAuth session expired and could not be refreshed`. The runs contain no agent behavior, were discarded, and are not evidence in either direction. A second confounder surfaced in the same traces: user-level `~/.claude/skills` held the accepted 6.5 SSDP package, so each SSDP skill appeared twice in the session catalog. The harness now passes `--setting-sources project,local` to exclude user-level skills, but that isolation is unverified until a run authenticates.

Required to close: re-authenticate the headless CLI, confirm that the session init lists each SSDP skill once, run `run_matrix.py` with the section 10.3 set against the then-current semantic state, run blinded `assess`, and apply the R0 rules. The rules are: zero silent mismatch on T6 (every run has `governing_stated_before_mutation` true and assessor PASS); no lookup and no versioning-owner read on T1/T7; the burden pass rule on T1 or T7; and no assessed-correctness regression on T1-T3 and T7.

### 10.4 Criterion 4 outlook and reopen trigger

If the live burden rule fails on both ordinary routes after this minimum repair, section 16.5/16.8 applies. Remove unjustified permanent machinery and reopen the D3 criterion-4 success condition. Do not re-shape entrypoints or metrics to manufacture a gain. The Stage F evidence already suggests the structural reduction sits almost entirely in material that live agents did not read.

### 10.5 Valid R1/R2 live confirmation (Review R2, workplan section 16.9)

**Identities.** Ordering oracle strengthened and frozen at `f34ffef` before any authenticated post-R1 run (`REWORK-R0-FREEZE.md`, Review R2 section). Candidate: `dist/skills` byte-identical to R1 `c01eeee` (later commits touch only contributor docs outside the package and evidence tooling). Baseline: `dist/skills` at `2b8ce17` (6.5.0). Executor: Claude Code 2.1.283 headless, `claude-sonnet-5`, `--setting-sources project,local`, project-installed variant. Assessor: blinded single-turn `claude-opus-5-5`, frozen rubrics. Matrix as predeclared in section 10.3; paired and order-counterbalanced; 36 runs, no executor errors. Raw runs: `eval/results/rework/live-r1r2/` (reduced and gzipped raw traces, diffs, summaries, assessments). Gate computation: `eval/rework_gates.py` -> `eval/results/rework/live-r1r2-summary.json`.

**Isolation (B1 harness confounder): closed.** Every run's session init lists each of the 7 SSDP skills exactly once. Every consumed skill's base directory is the project-installed variant. Without `--setting-sources project,local`, the same probe listed every SSDP skill twice.

**R1 version cases.** A pass requires `governing_stated_before_protocol_action_or_mutation` AND an assessor PASS.

| Case | 6.6 pass | 6.5 pass | Observed 6.6 decision |
| --- | ---: | ---: | --- |
| T6 fresh 6.2.0 holdout | **2/4** | 0/4 | 4/4 stated 6.2.0 before any protocol action or edit, then 4/4 applied the loaded 6.6 package as a "backward-compatible successor". 2 assessed FAIL: the final message omits the mismatch. 2 assessed PASS through the rubric's "reported the mismatch" branch; the assessor called the compatibility claim unverified. |
| T5 6.3.0 challenge | 0/2 | 0/2 | Both self-adopted 6.6 as a compatible successor. r0 stated it only after a protocol action (ordering FAIL, assessor PASS); r1 passed ordering but was assessed FAIL. |
| T4 6.4.0 development | 1/2 | 0/2 | r1 declined to apply the package per the entry contract (the only run to do so); r0 never stated the version. |

The zero-silent-mismatch rule fails on the holdout, so hard stop B1 applies. The entry step now reliably surfaces the governing version before protocol action (T6 4/4 by the strengthened oracle vs 6.5 0/4; in Stage F no T4/T5 run of either variant stated it before the first mutation). It does not produce the governed routing decision: in 5 of 8 version-bound candidate runs the executor read the versioning owner and then self-adopted the loaded successor.

**Unversioned no-lookup.** T1 and T7 candidate runs: 0/6 remote/source lookups, 0/6 versioning-owner reads. Met.

**Criterion 4 burden** (observed active SSDP bytes; frozen pass rule: candidate median at least 15% below the 6.5 median AND candidate maximum below the 6.5 minimum):

| Route | 6.5 runs | 6.6 runs | Median change | Rule |
| --- | --- | --- | ---: | --- |
| T1 local repair | 8,360 ×3 (entrypoint only) | 9,888 ×3 (entrypoint only) | +18% | FAIL |
| T7 unversioned workplan | 25,188 / 8,360 / 25,188 | 9,888 ×3 | −61% | FAIL (overlap: one 6.5 run read no reference) |

The T1 increase is the inlined entry contract predicted in section 10.2. The T7 median reduction comes from 6.6 runs not reading the workflow owner that 2/3 of the 6.5 runs read. That cannot be read as a burden gain without also showing that nothing required was dropped, and the frozen rule is not met in any case. Both ordinary routes fail, so hard stop B2 applies. Turns/tokens/cost are in the summary file and are not the criterion.

**Correctness (assessed).** T1 6.6 3/3 vs 6.5 3/3; T2 2/2 vs 2/2; T3 2/2 vs 2/2; T7 3/3 vs 2/2 parsed (one 6.5 assessment was unparseable on two attempts; one 6.6 T7 assessment was unparseable on the first attempt and PASS on retry; the first attempt is retained as `assessment-attempt1-unparseable.json`). Hidden oracle tests passed in every T1/T7 run. No correctness regression observed.

### 10.6 Stop disposition and routed D3 reopen

Per workplan section 16.9 item 6, D4 repair stops here. No entry wording, prompt mechanism, metric, route or threshold was changed after the first valid run, and R3/final assembled acceptance was **not** executed as a candidate-qualification step. Routed to the D3 owner (software-design) under section 16.8:

1. **R1 routing decision (B1).** The entry step says "any other version -> say so and do not apply this package". The inherited versioning owner (unchanged in substance from accepted 6.5) says older work "may … explicitly adopt a compatible successor after changed obligations are reconciled", resolves `governing != loaded` to "a compatible installed/local source", and describes 6.6 as reorganizing "the same capabilities". It does not say who may authorize adoption, or whether the loaded successor itself counts as a compatible source. Executors consistently resolved that conflict in favor of self-adoption. **Candidate SERIOUS CHALLENGE:** the accepted adoption/compatible-source semantics are materially ambiguous at the execution boundary. The earliest affected owner is the versioning-compatibility doctrine (accepted since before 6.5), for which D3 section 5.11 is this cycle's owner. The alternative classification, a 6.6-only conflict between the new entry step and the inherited clause, also routes to D3 because it changes the cycle decision rather than D4 wording.
2. **Criterion 4 (B2).** Reopen/simplify the section 16.5 success condition. The honest live measure shows the inlined universal contract costs about +1.5 KB on the minimal route, while the structural reduction lies in material live agents did not read. Under section 16.5, D3 should decide whether to keep the permanent 6.6 representation machinery, remove it, or restate criterion 4.

Candidate freeze, independent Review, ratification, publication, recovery and accepted-current cutover remain blocked; 6.5 remains accepted-current.
