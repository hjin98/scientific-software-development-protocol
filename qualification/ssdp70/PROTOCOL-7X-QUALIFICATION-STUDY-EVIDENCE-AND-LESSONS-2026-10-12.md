---
kind: study-summary
status: recorded
governing_protocol_version: 6.6.0
subject: Protocol 7.0 – 7.2.1 qualification study (2026-09-26 to 2026-10-12)
author: design lead (Opus 5.5), at the stakeholder's request
date: 2026-10-12
---

# Protocol 7.x qualification study: evidence and lessons

The stakeholder asked that this multi-week study be recorded as durable knowledge, not discarded because no round
produced a statistical pass. This record is the summary. It states what was measured, what it showed and what it means
for the next design. Each figure cites its owning record; the owning record wins on any discrepancy. Paths are relative
to `qualification/ssdp70/`; campaign directories live outside the repository under `~/ssdp70-omp-stagef/qualification/`,
and their outcome notes are copied into `qual-v2/evidence/campaign-outcomes/`.

## 1. Outcome in one paragraph

Four candidate generations (7.0, 7.1, 7.2.0, 7.2.1) were developed and measured against 6.6/6.5 baselines with
blinded custody, frozen decision rules, independent review and a light-model operator. No round reached a statistical
pass. 7.0 was NON-QUALIFIED (skills rarely activated). 7.1 was a development NO-GO (owner loads unreliable). 7.2.0 was
NOT ESTABLISHABLE (13 of 15 gates robust pass, 2 fragile). 7.2.1 was a frozen-rule NO-GO (target improvement fragile,
one single-event harm flag) with every other measure neutral or favourable. On 2026-10-12 the stakeholder accepted
7.2.1 **with conditions** (eighteenth ruling set): users are warned that the protocol is not statistically robust, that
a purely language-based skill cannot guarantee full compliance, and that reliability depends on the model. The study's
main finding is that limit itself, and it is the evidence base for a deterministic SSDS 8.0+ design.

## 2. Evidence by round

| Round | What was measured | Key result | Record |
|---|---|---|---|
| 7.0 pre-run checks (09-29) | custodian oracles vs checker probes | oracles mis-scored 84 of 171 probes before any run | `STAGE-F-PRE-RUN-CUSTODY-AND-ORACLE-CHECK-2026-09-29.md` |
| 7.0 Stage 7 (10-01..04) | skill activation, Flash executor (GLM-5.3-Flash) | a skill was loaded in 13 of 122 candidate runs; Stage 7 closed NON-QUALIFIED | `STAGE-7-SELECTION-STRONGER-EXECUTOR-PROBE-RESULT-2026-10-04.md`, `STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-NON-QUALIFICATION-CLOSEOUT.md`, `...-DETERMINISTIC-ACTIVATION-AND-ACTIVATION-QUALIFICATION.md` |
| 7.0 stronger-model probe | same tasks, GLM-5.3 vs Flash (10 episodes) | selection 4/10 vs 2/10; decided by whether the model thinks to consult the skill catalog at all | same |
| 7.0 doctrine-loaded probe | uptake when the skill *was* loaded | 10 of 25 owed delegate-request parts asked; 1 of 7 episodes fully conformant | `STAGE-7-M07-DOCTRINE-LOADED-PROBE-RESULT-2026-10-04.md` |
| 7.0 checklist probe | structured checklist inline | uptake 14/50 (28%) to 46/50 (92%); strict pre-return conformity 0/50 (small, unblinded) | `STAGE-7-M07-CHECKLIST-PROBE-RESULT-2026-10-04.md` |
| 7.0 package-access ledger | measurement mechanism design | seven review rounds NO-PASS, each additive repair creating new blockers; mechanism frozen by the stakeholder | `PACKAGE-ACCESS-LEDGER-DECISION-CLOSEOUT-2026-10-04.md` |
| 7.1 dev matrix (10-06) | 300-run operator matrix | not a qualification: probe mode, disclosed corpus, script-synthesized assessments; withdrawn and relabelled | `PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md` |
| 7.1 dev probe (10-07) | "read the owner when ..." routing, 184 runs | owner-load hits 15/41 (37%); 25 misses never touched the owner; 3 false early loads; NO-GO + SERIOUS CHALLENGE | `PROTOCOL-7.1-DEV-PROBE-2026-10-07-RESULT.md` |
| 7.2 redesign (10-07) | design analysis | absolute floors measured the model, not the protocol; replaced by paired, calibrated non-inferiority vs 6.6; one inline "Scientific checks" block per entrypoint; lossless compression yielded almost nothing (92.8–98.8% of the 7.1 block) | `D3-PROTOCOL-7X-RELIABILITY-SIMPLIFICATION-AND-CALIBRATED-QUALIFICATION-DESIGN-2026-10-07.md` |
| 7.2 S4 dev probe (10-08) | candidate-only probe | GO to commission the campaign | `S4-DEVELOPMENT-PROBE-REPORT-2026-10-08.md` |
| 7.2.0 campaign (10-08..11) | 640 executor runs, MiMo-V2.6-Flash evaluator | ~11% of first-pass assessments format-invalid; reruns did not converge (17 of 48 second draws failed again); 20 runs / 60 items unresolved; 13/15 gates ROBUST PASS, Q3 (duty composite) and Q4d (over-reporting) FRAGILE: NOT ESTABLISHABLE. Expected-case reading: Q4d a likely failure — the candidate narrated "Scientific checks" where none was owed (10 vs 0 runs) | `qual-v2/evidence/campaign-outcomes/campaign-72-BOUNDED-SENSITIVITY-RESULT.md` (copy of the campaign-dir note) |
| 7.2.1 design (10-11) | reduction cycle targeting that narration | operating-characteristics simulation of the frozen rule: a favourable candidate reaches go only 39/300 (13%); the cause is the W/B unresolved bracket at the evaluator's unresolved rate (44/300 at observed rate, 274/300 at zero), not margins or sample size | `qual-v2/S5-721-REDUCTION-PLAN-2026-10-11.md`, `qual-v2/evidence/721-codex-review/oc-gate-diagnostic-2026-10-11.md` |
| 7.2.1 campaign (10-12) | 703 executor runs, 453 assessments, 7.2.1 vs 7.2.0 paired on 122 episodes | narration (P1) resolved fail 10.4% vs 17.1% but FRAGILE on 12 vs 14 unresolved items; retained duties (P2) and outcome items (P3) ROBUST non-inferior; harm flag delegate_request.unowed.R (1 fail vs 0): NO-GO. Infra loss 3.7% after reruns; 9 of 453 assessments unresolved | `qual-v2/evidence/campaign-outcomes/campaign-721-FINAL-REPORT-2026-10-12.md` and `campaign-721-comparison-statistical.md` (copies) |
| Across all arms (13th set) | detection, claim integrity, unauthorized mutation, version ordering | no protocol effect in any arm, 6.6 included | `qual-v2/S4-STAKEHOLDER-RULINGS-2026-10-08.md` (thirteenth set) |

## 3. Lessons about language-based protocols

1. **Compliance is probabilistic and model-dependent.** At every layer — activating the skill, loading further text,
   asking each owed question — compliance was partial, varied run to run, and rose with model strength without
   becoming reliable. A purely language-based skill cannot guarantee 100% compliance.
2. **Only text that reaches the context acts.** Conditional instructions to read more ("read the owner when ...")
   mostly failed (37% hits). Inline, enumerated, structured text worked best (checklist 28% to 92%). 7.2 therefore
   moved the minimum duty inline; that is the right shape for a text protocol, and its ceiling.
3. **Activation must be deterministic.** Wording and descriptions do not reliably select a skill on Flash-tier models.
   Explicit commands (`/software-design`, `$software-design`) are the supported activation path.
4. **Errors are two-sided.** More inline duty text produced over-application: narrated checks on tasks that owed none
   (7.2.0 Q4d). The 7.2.1 reduction moved that in the right direction but could not be shown robustly. Text can shift
   the balance between omission and over-reporting; it cannot make an agent apply a duty exactly when its trigger holds.
5. **Some behaviours do not respond to protocol text at all** (detection, claim integrity, unauthorized mutation,
   version ordering). They are candidates for mechanical enforcement, not more prose.
6. **Compression has little room left.** A lossless block cannot be made much smaller than its content; size and
   salience trade against completeness.

## 4. Lessons about measuring them

1. **Absolute floors measure the model.** Compare paired arms on the same episodes and executor, against a calibrated
   baseline, with margins fixed before exposure.
2. **The LLM evaluator's unassessable tail sets the power ceiling.** About 4–11% of assessments were format-invalid or
   unresolved; reruns did not converge. Under a conservative W/B bracket that tail, not sample size, decided both
   campaigns. Simulate operating characteristics on the frozen rule before spending, and treat a low go probability
   for a good candidate as a reason to redesign, not to proceed.
3. **Validate oracles and instruments before runs.** The 84/171 oracle mis-scoring and a C(b) calibration step caught
   instrument defects that would otherwise have been read as candidate effects.
4. **Additive repair loops on measurement machinery diverge.** Seven ledger rounds each produced new blockers; freezing
   the mechanism and stating limitations was cheaper and more honest.
5. **Frozen rules, custody and blinding worked.** They prevented post-hoc tuning and made the fragile results
   interpretable. Independent review caught real defects each round (for example the 429 classifier gap, evaluator
   reruns never being assessed, and an operator collect run on a stale tool copy).
6. **Operations need mechanical guards.** Provider throttling at high concurrency cost 27–31% of runs per stage until
   arm-blind, failure-class-selected reruns recovered them; hash-gated tools, absolute tool paths, closed runbooks and
   lead-only authorizations let a light-model operator run long campaigns safely.
7. **Small effects are expensive to establish.** A ~$20 campaign could not resolve a few-point effect at the evaluator's
   unresolved rate; each further round cost days of compute and review for shrinking expected gain.

## 5. Implications for SSDS 8.0+ (direction, not a plan)

- Activation by deterministic command or harness hook, never by wording.
- Trigger evaluation and report-structure checks by machinery (schemas, validators, gates) rather than by the agent
  remembering a duty; text then explains intent instead of carrying enforcement.
- Mechanical enforcement for the behaviours text did not move (unauthorized mutation, version ordering, claim checks).
- Deterministic verdicts where possible, so qualification is not bounded by an LLM evaluator's unresolved tail.

## 6. Acceptance condition carried into the release

7.2.1 is accepted with conditions: users must be told that the protocol is not statistically robust, that a purely
language-based skill can never guarantee full compliance, and that reliability depends on the strength of the model.
The README carries this as a closing warning; the CHANGELOG and the ratification record state the measurement result.
