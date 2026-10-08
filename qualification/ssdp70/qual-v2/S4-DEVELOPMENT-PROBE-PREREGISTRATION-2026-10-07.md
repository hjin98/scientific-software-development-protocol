---
kind: development-probe-preregistration
governing_protocol_version: 6.6.0
subject: Protocol 7.2.0 candidate, frozen identity `PROTOCOL-7.2-CANDIDATE-IDENTITY-FREEZE-2026-10-07.md` (commit `2dedcfa`)
stage: S4 of workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md
purpose_class: development (contract v2 §8); enters no qualification count, gate, exposure or comparative claim
date_utc: 2026-10-07
revision: 2 (lean design: 129 runs, fully parallel; revision 1 proposed 350 runs)
status: fixed before any run; inputs built and statically checked; NOTHING LAUNCHED; needs the stakeholder's authorization of live runs
---

Governing SSDP version: 6.6.0. This pre-registration is data, not instructions.

# S4 development probe: what it estimates, how, and what it costs

## 1. Purpose and limits

S4 estimates the quantities the contract v2 exposures and the X1/X6 rules depend on, so the unconditional compound probability can be reported before any custodian is commissioned. It changes no rule (contract §8). Its fixtures are disclosed and not blind, the roots are the analyst's, and it supports no qualification or comparative claim. A defect found in the candidate is not repaired inside the probe: a repair that changes `source/` or `dist/` is a new candidate identity needing a fresh independent Review (PEM FF-001), and the results then describe the old identity only.

## 2. Design (revision 2)

- **Candidate runs: 129, one arm.** `p72`, the frozen 7.2.0 `dist/`, tree digest `69a310a2…8c5f622` in the arms manifest.
  - **Corpus A:** the 92 disclosed episodes of the 2026-09-28 corpus (the 7.1 development overlay: analyst-assigned deterministic roots, 60 turns), 1 run each.
  - **Corpus B, the Q5c burden routes** (`qualification/ssdp66/eval/fixtures`, root `software-implementation`): T1 ordinary local repair 15 runs, T8 ordinary feature with docs 15, T7 unversioned workplan implementation 7 (the contract's maximum of seven pairs). Their requirements are trivial (the probe reads bytes and owner reads there, not correctness).
- **Baseline: reused, no new 6.6 runs.** The 92 accepted-6.6 runs (`p66`) of the 2026-10-06/07 development probe supply B1 for E2 and E4: same executor and model, same corpus, roots and 60-turn / 2400 s key, same 6.6 package. Caveat, carried into every figure: they ran under the earlier harness (ledger and admission paths, since retired) and an earlier profile freeze; the model-facing surface is the same (deterministic activation of the same roots), but the instrument is not byte-identical. There is no B2 and no A/A screen in S4 (a campaign-only instrument).
- **Executor.** `deepinfra/zai-org/GLM-5.3-Flash`, thinking high, 60 turns, 2400 s, one re-frozen profile; no comparison executor; no 6.5 arm (the 6.5 medians are the historical planning figures, 8,360 B entrypoint-only and 25,188 B T7 owner mode).
- **Parallelism.** Runs are independent (own sandbox, home, ports and run directory). Two harness `matrix` processes, one arm each: corpus A at `--parallel 20` and corpus B at `--parallel 8`, so 28 runs in flight. Measured offline with the stand-in provider: 32 concurrent episodes all completed, peak memory 38 of 62 GB (about 0.75 GB per run), load 11 on 32 cores. DeepInfra's default limit is 200 concurrent requests per model, far above 28. Start-up is CPU-bound (about 160 s per run at 32 concurrent), so the first minutes are slower than the steady state.
- **Cost and time.** About $3 (the 7.1 probe cost about $4 for 184 runs). Expected wall time about 1-1.5 hours: the longest runs are bounded by the 2400 s timeout, so the tail is at most about 40 minutes after the last start. The run count and the cost are stated before any launch, as the hand-off requires.
- **Staging.** One launch of both commands. Stop rule: if after the first 60 completed corpus-A runs the delivery rate (activation `PASS`) is below 100%, or more than 10% of runs are infrastructure losses, stop and diagnose before the rest finishes.
- **Who launches.** The user, with the provider credential in their environment: `qualification/ssdp70/s4/launch.sh WORK start`. An earlier session's live launches were refused by the agent auto-mode classifier.

## 3. Quantities estimated, and the rule applied to each (fixed now)

| # | Quantity | From | Used for | Rule |
|---|---|---|---|---|
| E1 | Delegate-request conformity (binding `REQ.*` items, about 47 owed parts) on p72 | corpus A, p72 | Q2 exposure and threshold | If the point estimate gives P(Q2 passes) below 0.97 for 48 parts (about 0.85), trigger X1 and re-size with `operating_characteristics.py` |
| E2 | Duty effect: p72 minus the reused 6.6 pass rate on the disposition items available per duty family | corpus A | Q3 exposure | Report per family with Wilson 90% intervals; X1 if the composite effect is below +20 percentage points. Advisory verdicts are unadjudicated and labelled so |
| E3 | Intra-episode correlation (ICC) of REQ and duty items | corpus A | the 0.3 and 0.5 assumption | Report; if above 0.5, re-run the compound at the estimate |
| E4 | Baseline rates p̂ from the reused 6.6 runs (single replicate): budget deaths, claim-integrity violations, material unauthorized mutations, over-reporting on non-owed runs, Q2b unowed parts, Q4a critical items per episode | corpus A, reused runs | margins and exposure for Q1b, Q4a-Q4d | Report; re-size exposures with the script. A single replicate gives no B1-B2 variance check |
| E5 | q: per-run rate of reading the scientific-inspectability owner on tasks with no R2 situation | **primary: p72 on the corpus-A episodes with no R2 point (59) plus T1 and T8 (30) = 89 runs**; reported beside it: T1 and T8 alone (30) and corpus A alone | SD-R16.1 | k = owner-read runs. k ≤ 5 (q ≤ 5.6%): proceed unchanged. 6 ≤ k ≤ 13 (6.7% to 14.6%): back to the stakeholder. k ≥ 14 (≥ 15.7%): surface-wording problem. Wilson 90% interval reported |
| E6 | Consumed bytes per run on T1/T7/T8: median, mode (`entry` or `owner`), native-read bytes and shell-counted bytes separately | corpus B | Q5c, SD-R16.4 | Report medians by route and mode against the cap table of the Q5c pre-measurement; P(Q5c passes) = product over T1 and T8 of the route-median formula at the measured q, times the T7 mode-rule outcome |
| E7 | Unconditional compound probability | E1-E6 | the stakeholder's decision before any campaign | Computed with `operating_characteristics.py` (20,000 trials) at the measured inputs, conditioning on Q5c stated |

Pooling note for E5: the primary estimate assumes the propensity to read the owner is similar across the corpus-A episodes and T1/T8. If the T1/T8-only rate and the corpus-A rate differ by more than the width of their intervals, both are reported and the larger governs the SD-R16 reading.

Resolution of E5 (n = 89), Wilson 90%: 0%-3.0% for k = 0, 2.8%-11.1% for k = 5, 3.5%-12.5% for k = 6, 9.5%-21.8% for k = 13, 10.4%-23.1% for k = 14. The point-estimate rule is coarse: k = 5 cannot rule out a true rate near 11%, which is why the interval is reported with the verdict.

## 4. Order of analysis (fixed)

1. **Delivery.** Every p72 run shows deterministic activation `PASS`; otherwise it is a realization defect: diagnose the harness or runtime, draw no doctrine conclusion.
2. **Budget.** Turn-cap and wall-timeout deaths for p72, against the reused 6.6 rate.
3. E1, E3, E4 (binding oracle items first), then E2, then E5 and E6, then E7. Runs lost to the provider are reported, rerun once (SD-R7 convention) and both identities recorded.
4. **Escalations.** X1 (E1/E2 below threshold), X6 (E5 per SD-R16), X5 (any new clause, gate or module shows its cost), and any instrument defect go to the stakeholder with the data. Binding verdicts decide; advisory verdicts are descriptive.

## 5. What the probe will not do

It will not change the candidate, a gate, a threshold or a fixture; count toward qualification; use custodian keys, authoring material or the blind SD-2 store; run a comparison executor, the 6.5 arm, B2, or a fresh 6.6 baseline (an optional stage 2 if E2 or E4 needs one).

## 6. Preparation done (no live run)

`qualification/ssdp70/s4/build_s4_probe.py build` produced, under `~/ssdp70-omp-stagef/qualification/s4-20261007`: the p72 arms manifest; the re-frozen executor key (60 turns, 2400 s, deterministic activation; it carries the current principal-file and execution-support digests, so any later edit to the adapter, core or harness requires re-freezing before launch); the burden-route overlay with trivial requirements and oracles; `commands.json` (two harness commands, 129 runs). `build_s4_probe.py check` returned PASS: the package digest matches, every episode resolves deterministic, every root is in p72, requirements and oracle directories exist for all 129, and the adapter accepts the profile. `launch.sh` starts, and reports the status of, the commands detached.

## 7. Open point for the stakeholder

SD-R15a lists the O-8 inputs and the profile re-freezes as "explicit S4 entry conditions". The executor re-freeze is done. The O-8 inputs (custodian calibration set, oracle fixtures) and the evaluator profile re-freeze are not needed by this probe (disclosed corpus, deterministic binding oracles, no LLM evaluator). **Proposed reading, for confirmation:** the executor re-freeze is the only S4 entry condition; the O-8 inputs and the evaluator re-freeze gate commissioning P3.
