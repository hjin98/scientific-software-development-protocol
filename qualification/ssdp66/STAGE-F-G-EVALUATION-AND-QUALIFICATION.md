---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stages: F, G
evaluated_source: 3fac7d1c34822ba82785e0b41f6e340fd7cfa6d5
---

# Protocol 6.6 Stages F-G — Empirical Evaluation and Assembled Qualification

Evidence coordination under the [Protocol 6.6 Evaluation and Qualification Contract](PROTOCOL-6.6-EVALUATION-AND-QUALIFICATION-CONTRACT.md). It is not D1-D4 authority, a Review, or release state. It establishes only what its oracles discriminate; semantic adequacy of the assembled candidate still requires fresh independent Review.

## 1. Disposition

```text
SERIOUS CHALLENGE (to accepted 6.5): NONE
IMPLEMENTATION BLOCKERS: NONE KNOWN
NEW CORRECTNESS REGRESSION vs 6.5 ON MATCHED CASES: NONE OBSERVED
READY FOR FRESH INDEPENDENT REVIEW: YES, with the two material findings below carried prominently
CANDIDATE FREEZE / PUBLICATION / RATIFICATION / CUTOVER: NOT PERFORMED (Stage H)
```

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
| 3 | new routing/context/state/version/eval counterfactuals pass | `tests/test_protocol_66_cognitive_optimization.py` (28 tests), Core 6.6 schema oracle | MET mechanically; live version counterfactual fails for both variants (finding 1) |
| 4 | clear structural reduction + bounded live burden reduction beyond noise | −21…−27% mandatory closure; live: missed activations 9 -> 3 (intervention/activation dimension), trajectory tokens/turns unchanged | STRUCTURAL MET; LIVE MET ONLY ON THE ACTIVATION/INTERVENTION DIMENSION — Review to judge sufficiency |
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
