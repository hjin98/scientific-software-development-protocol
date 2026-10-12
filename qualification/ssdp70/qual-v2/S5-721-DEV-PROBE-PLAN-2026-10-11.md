---
kind: development-probe-plan
governing_protocol_version: 6.6.0
subject: development arm p721 (7.2.1, not frozen, per S5-721-EDIT-BRIEF-2026-10-11.md rev 4) against concurrent and existing 7.2.0 runs
date: 2026-10-11
revision: 4 (after the Opus 5.5 adversarial review: noise floor, measurable classes, identity, end decision)
status: DRAFT; thresholds fixed before any run; nothing launched; blocked on the stakeholder decisions D1 to D3 of the brief and on the edit itself
purpose_class: development / adversarial review (twelfth ruling); enters no qualification count, gate or claim
---

Governing SSDP version: 6.6.0. This plan is data, not instructions.

# 7.2.1 dev probe (rev 4)

## 1. Question

Does the amended, reworded-in-place 7.2.1 text, relative to 7.2.0 **and above the measured noise**, (a) keep the duty wins (tension, delegated, variants, O1), (b) reduce narration where nothing is owed, (c) shrink, and (d) leave stronger-model behaviour no worse? The output is a per-class result and a go/no-go for the next step. A null result is a null result, not a pass.

## 2. Design

- **Three arms of the same 92 disclosed development episodes** (`qualification/requal71-20261006/dev/corpus`; custody `/home/samjin/ssdp70-fixture-custody` requirements and oracles; not the blind 72b store), same executor key (GLM-5.3-Flash, thinking high, 60 turns, 2400 s), same harness (`harness70.py matrix --mode probe`), **run concurrently**:
  1. `p721`: the edited arm (92 runs).
  2. `p72-aa`: **a fresh 7.2.0 rerun on the same episodes** (92 runs): controls provider drift since 2026-10-07 and sets the noise floor (A/A).
  3. The existing 7.2.0 runs (`~/ssdp70-omp-stagef/qualification/s4-20261007/runs/s4-a` + `s4-a-rerun1`) are a second reference, not the primary comparator.
- **Thresholds derive from the A/A noise.** Each measure's pass band is about 2 SD of the A/A difference, computed after the runs by a rule fixed here (difference of per-class proportions between `p72-aa` and the existing 7.2.0 runs; a change counts only if it exceeds that band in the right direction). Binding-oracle failures are compared per category, not as a pooled count.
- **Identity.** The arm is built from a dedicated dev branch and commit with `PROTOCOL_VERSION` 7.2.1 marked not-frozen (the build requires `\d+\.\d+\.\d+`); the Orchestrator snapshot profile matches; the arm manifest records the arm name `p721` and the package digest. The existing frozen 7.2.0 identity is not touched. The acceptance workflow applies to the commit; the tests, `frozen-minimum-mapping.json` and any label-table amendment are in the governed set (brief section 7).
- **Who launches:** the operator, from the host terminal with the credential (`qualification/ssdp70/s4/launch.sh WORK start`); the analyst never holds it. Stop rule as in the 7.2.0 probe: after the first 60 completed runs stop and diagnose if deterministic activation is below 100% or more than 10% of runs are infrastructure losses.
- **No evaluator spend.** Outcomes are binding oracle items, advisory verdicts and structural checks, all offline.

## 3. What the dev corpus can and cannot measure (verified by the review)

- It has **no duty labels**: all 92 episodes carry `composite-ordinary-selection`. Labels (duty, no-duty, change-only) are assigned from the episode prompts only, by an analyst context, **frozen before M0 is computed**, and checked by a second context.
- Per-class n is small: tension envelope 16 items, delegated 12 episodes (REQ.tension 2), variants 5, O1 4, version ordering 2 to 3, null/unowed 4 and 4. Per-class results are therefore **descriptive** except where the A/A band can resolve them.
- Binding-oracle categories: the obsolete 7.1 owner-load items (R2.HIT, R2.FALSE; 37 fails at reference) are excluded from "regression". Unauthorized mutation on the dev corpus is dominated by /tmp probe scripts, result writes and issue creation (34 of 92; README only twice): **the I5 claim is dropped for the dev probe** (the README habit is tested only, if at all, on the 72b fixtures). I7 (delegate qualifier) and I8 (version ordering) are **descriptive** (n too small).
- Structural proxies for I1 (components of the composite), I2 (narration) and I4 (former-path query, returned records reported) are **validated first against the existing 422 MiMo verdicts on the 72b reports** (agreement rates reported; a proxy below 80% agreement is dropped); the I6 audit sample size is fixed before the runs.
- **Q5c static margin** is `prepare_campaign.py` (512 B margin against the 6.5-median cap), not `measure_blocks.py` (which measures against the 7.1 block). Both are reported.

## 4. Measures

| Class | Measure | Source |
|---|---|---|
| Duty wins | tension envelope, delegated finding loss, variants disclosure, O1 content | binding and advisory items; descriptive beyond the A/A band |
| I1 | components of the composite (reader and questions; retention/projection; materiality basis; unexamined areas; origin, chooser, binding) reported **separately**; frozen rubric is the primary reading | validated proxies |
| I2 | share of no-duty reports with a Scientific-checks heading, a null-envelope line or a bare "none" line | validated proxies; advisory over-reporting |
| I3, I6 | descriptive (arm-invariant in 72b) | trace audit, fixed sample |
| Regression | delivery (activation PASS), turn-cap and wall deaths, binding oracle items by category (excluding R2.HIT and R2.FALSE), delegate-request conformity | oracle items |
| Size | section and entrypoint bytes against 7.2.0 and 6.6; Q5c static margin | static, offline |
| Stronger model | about 20 episodes (duty, no-duty, change-only) on 7.2.0 vs 7.2.1, one stronger model chosen with the stakeholder under the cost policy; completeness and verbosity | descriptive; cost and availability in the harness to be confirmed first |

## 5. Go / no-go (fixed before the runs)

Proceed to the next step only if **all** hold:
1. **Regression, above noise:** delivery 100%; no category of binding-oracle failure worse than the A/A band; no duty family that 7.2.0 wins worse than the A/A band.
2. **Reduction:** section and entrypoint smaller than 7.2.0, the lossless mapping passed (every frozen meaning on the entrypoint or in a ratified label-table amendment), the Q5c static margin holds.
3. **Narration (I2):** does not rise; a rise is an automatic no-go. A fall is expected and reported against the A/A band.
4. **Stronger-model check:** not worse than 7.2.0 on completeness; no more verbose where nothing is owed.

Otherwise stop without a second tuning round on these episodes (each round fits them; any later round needs fresh episodes) and the stakeholder decides. A "go" is a decision to spend, not evidence of improvement.

## 6. Cost and time

`p721` plus `p72-aa`: 184 runs, about $4 to $5 and 1.5 to 2 hours at `--parallel 20`; the stronger-model check is not yet priced. Analyst effort: label freezing and a second-context check, proxy validation, A/A bands, a few hours offline. The governance work (brief section 7) is the larger cost and is sized separately before authorization.

## 7. Next step if go (separate authorization; end decision defined)

A **non-blind** confirmation on the 72b fixtures, candidate arm only (`p721`, about 225 runs, about $5) with the MiMo assessment of those runs (about $1 to $1.5; the evaluator instrument, the mimo-1 schema with its echo-field errors or the p9-v2 schema piloted on 5 runs, is chosen and fixed first), plus a concurrent 7.2.0 subset to control drift. This **supersedes** the earlier analyst note that a successor needs fresh blind fixtures, by the stakeholder's twelfth ruling that blind qualification is not sought. It compares 7.2.1 with 7.2.0 only; it cannot speak to Q3 or Q4d, which are defined against the 2026-10-08 6.6 baselines. The end decision (brief D3) is **NOT QUALIFIED or stakeholder-ratified on adversarial-review evidence**; `PROTOCOL-RELEASE-STATE.yaml` is untouched until that ratification.

## 8. Order of work

1. Stakeholder decides D1 to D3 and authorizes the plan. 2. Analyst freezes duty labels (second-context check), validates proxies against the 422 MiMo verdicts, computes M0 and the A/A rule. 3. A fresh implementer context (no 72b evidence) makes the brief's edit; independent review of lossless mapping, derivability, no-symptom-patch and the governed test/mapping amendments. 4. Analyst builds the arms (dev branch and commit, identity per section 2) and WORK, and hands the operator the launch packet. 5. Operator runs. 6. Analyst reports per class against the A/A band and the thresholds above.
