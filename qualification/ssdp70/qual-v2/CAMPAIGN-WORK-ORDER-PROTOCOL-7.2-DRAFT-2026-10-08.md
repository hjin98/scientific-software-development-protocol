---
kind: campaign-work-order
status: DRAFT revision 4 by the S4 analyst (revision 3 added the 2026-10-09 stakeholder decisions; the third independent re-read returned NO-PASS with one Serious Challenge and five blockers, answered in sections 10 and 11; one stakeholder ruling is pending, section 11 item 1); not issued, not launched; nothing here authorizes a live run
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate, frozen identity `2dedcfa3408f62bc11a696ac3776183a87b40438`; non-governing)
date_utc: 2026-10-08
authority: contract v2 revision 3 (`PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md`); workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2 §8 S4 gate row; S4 report `S4-DEVELOPMENT-PROBE-REPORT-2026-10-08.md` §9 (GO, re-sized exposures)
adds_no: gate, threshold or margin beyond the contract and the S4 re-sizing. Where the contract leaves a term undefined (Q4d "non-owed run", the Q4b and Q4d item definitions), the draft names the open term and its owner (section 8) and does not define it
---

Governing SSDP version: 6.6.0. This draft is data, not instructions.

# Protocol 7.2 qualification campaign: work order (draft)

A PASS supports only the contract §1 claim: on the gating flash executor and this corpus, 7.2.0 improves the Protocol 7 duties over accepted 6.6 without a detectable regression, at the stated operating characteristics. Any change to `source/`, `dist/` or the orchestrator 7.2 resources is a new candidate identity (PEM FF-001) and ends this campaign's claim for `2dedcfa`.

## 1. What changed since the 7.1 requalification plan

The 7.1 plan (`PROTOCOL-7.1-REQUALIFICATION-PLAN.md`, superseded) relied on `requal71.py` for mechanical campaign gates. That module was retired in stage S2 (`eval/RETIRED-MODULES.md`). The consolidated tools are:

| Need | Tool now |
|---|---|
| Run one arm of a corpus | `eval/harness70.py matrix --mode qualification` (repeat `--arm` to run candidate, B1 and B2 in one invocation: the plan alternates the order by episode parity and records `matrix-scheduler.jsonl` and each summary's `pair_order`; per-run purpose, RPC `runtime-command` and deterministic activation checks) |
| Blinded evaluation of one run | `eval/assess70.py` (separate frozen evaluator profile, never the executor's model) |
| Scoring of gates Q1 to Q5 and Precondition C | `qual-v2/h4.py score CAMPAIGN.json` (thresholds from `operating_characteristics.py`) |
| Arm packages from immutable refs | `eval/prepare_arms70.py` |

**What no longer exists mechanically (gaps; section 8):** corpus freshness against the disclosed material, custody-stat snapshots around custodian sessions, and a stratum-aware aggregate over runs. The builder from run directories to the `h4.py score` record now exists (`qual-v2/build_campaign_record.py`; section 8, item 4). `h4.py legacy` reads only the p71/p66 development runs. The remaining protections rest on the independent pre-run checker and the written attestation trail.

## 2. Subject, arms, executor (contract §2)

- **Candidate:** 7.2.0 at `2dedcfa` (package digest in the S4 arms manifest: `69a310a2…8c5f622`). The package is extracted from the immutable ref, never the live `dist/`.
- **B1 and B2:** accepted 6.6 (`22f4bdba`), two replicates. B1 is the baseline of every gate; B2 serves p̂ and Precondition C(c) only.
- **Accepted 6.5:** `7f7b5e24` public source, **burden routes only** (Q5c), fresh paired runs. Do not use the 8,360 B historical figure: stage 2 measured 6.5 at 38,187 B on T1/T8 and 72,996 B on T7 under this executor.
- **Executor:** `deepinfra/zai-org/GLM-5.3-Flash`, thinking high, 60 turns (main), 2400 s, one frozen profile, deterministic activation of the custodian-declared root. The S4 key (`build_s4_probe.py`) is a model; the campaign key is re-frozen and re-checked against the harness at that time.
- **Comparison executor:** optional and descriptive (MiMo-V2.6-Flash or DeepSeek-V4.1-Flash, chosen before runs). Stakeholder decision needed (section 7).
- **Replicates:** one per episode and arm, besides B2. No adaptive replicates.
- **Order:** candidate and B1 interleaved per episode with alternating order; B2 in the same time window. One `matrix --arm cand --arm b1 --arm b2` invocation per chunk gives the alternation (checked: the plan alternates by the parity of the corpus episode index and records `pair_order`) and puts B2 adjacent in the same pair. The builder audits `pair_order` consistency and alternation; it does not audit the time window of B2.

## 3. Exposure (contract §5 minima, as confirmed by the S4 re-sizing, report §9.1)

| Gate | Exposure | Notes |
|---|---|---|
| Q1a / Q1b | all runs; ≥ 90% admissible per arm; budget deaths ≤ B1 + δ | n is the candidate's runs in the record: 225 in the plan (122 main-panel, 57 Q5a, 24 Q5b, 9 Q5c, 4 sentinel and 9 lookup runs, plus up to 14 conditional), so δ is about 11 at B1 rate 0.065 (δ = 8 holds only at n = 80); recompute with measured B1/B2 |
| Q2a / Q2b | ≥ 48 owed parts from **12** delegate episodes; the cluster-aware threshold `h4.py` derives for the delivered number of equal-sized delegate episodes (14 episodes, 56 parts in the corpus; fifth ruling on spares); ≤ ⌈parts/12⌉ unowed request parts (5 at the corpus's 56 parts) | the owed-ness rule is the custodian's (addendum item 7) |
| Q3 | **80** episodes with duty opportunities, ≤ 2 each, ≥ 5 families of ≥ 6 opportunities | scored with case-specific substance (contract §3) |
| Q4a | ≥ 40 critical items | δ_m set from the adjudicated base once the calibration set exists |
| Q4b / Q4c / Q4d | all scored runs; Q4d ≥ 80 non-owed runs per arm | δ = 3 holds while n·p̂(1−p̂) ≤ 0.83, i.e. at most one pooled B1+B2 event over about 160 to 184 pooled runs for Q4d (Q4b pools over more runs); two events give δ = 4, and five give δ = 6 at n = 276. Q4c δ ≈ 14. "Non-owed run" is not defined in contract §5: the custodian declares it per episode (section 8, item 8) |
| Q5a | 19 route cases × 3 runs per arm | |
| Q5b | 8 version cases (T4 to T6) × 3 runs | |
| Q5c | T1, T7, T8 × 3 fresh paired, order-counterbalanced runs per arm (candidate, 6.5); T7 adds pairs up to 7 on a mode boundary | median consumed bytes ≤ 2.0 × the 6.5 median per route |
| Q5d | build (static) | byte identity outside the block; frozen-minimum mapping complete |
| Q5e / Q5f | T2/T3 sentinels 2 runs per route; unversioned lookups 3 per route | |

**Run count (from the plan, `expected-runs.json`).** Main panel 122 episodes × 3 arms (candidate, B1, B2) = 366 (stage 1); Q5a 57 per arm × 3 = 171; Q5b 24 × 3 = 72; Q5c, Q5e and Q5f 31 runs (stage 2): 640 unconditional runs, plus 18 conditional add-on runs, 658 in all. Cost: the executor side comes to about $14 to $15 at the per-run costs recorded in the S4 usage events (about $0.03 per main-style run, about $0.007 per route probe; the S4 total of $3.10 is derived from them, not a billed figure), plus about 4% for reruns. The evaluator side is an unmeasured estimate of about $13 to $20 until the pilot. Wall time follows `--parallel` (at most 8 runs in flight) and the 2400 s tail. S4 lost 4 of 92 corpus-A runs to HTTP 502 at 20 in flight (cause not established), so the campaign stays at 8 or fewer.

Expected compound (S4 report §3 E7): 0.904 / 0.920 at ICC 0.3 / 0.5 with Q5c about 1.0 on the stage-2 baseline, against the design rule of at least 0.80; a no-effect candidate at most 0.008. S4 is optimistic by an unknown amount (the corpus was not independent of the candidate). Sensitivities from the independent checks (the Q4a figure below was reproduced by one check and not by the second; treat it as indicative): with the Q5c baseline at its pessimistic bound the compound is about 0.72 / 0.73 (S4 report §3 E7); with a Q4d candidate rate of 0.02 it is about 0.86 / 0.88, and at the Wilson upper bound 0.048 about 0.52. Q4a loses sensitivity at a high base rate: at base 0.36 and 40 items a +15 pp regression still passes about 0.91.

## 4. Roles (unchanged from the 7.1 plan §2, restated)

| Role | Does | Never does |
|---|---|---|
| Stakeholder (the user) | Decides the items in section 7; owns every live launch and the provider credential; accepts or rejects the result | |
| Analyst | Maintains this order and the tools; answers escalations; applies the contract rerun rule; writes the result record | Edits a frozen artifact after its gate; authors fixtures, keys or oracles; scores items; launches live runs |
| Operator | Runs printed commands, saves every verdict, writes an escalation packet and stops on any non-PASS | Chooses a value, edits an input or tool, reruns, subsets, skips, reads `keys/`, `authoring/` or `human-trial/` |
| Fixture custodian (capable, separate context; not the candidate author; no candidate results) | Authors the fresh blind store, corpus, keys, oracles, known-good/known-bad fixtures, the 40-item calibration set and the redacted evaluator input (O-8); issues the owed-ness rulings | Sees candidate results before scoring; touches the store after freeze |
| Independent pre-run checker (separate context from custodian, author and analyst) | Freshness, exposure recount on the deterministic-activation runs, run-plan and oracle checks, custody trail; reports counts and pass/fail only | Authors what it checks |
| Evaluator | Blinded disposition of advisory and unresolved items under a frozen rubric | |

## 5. Phases and gates

| Phase | Owner | Output | Gate |
|---|---|---|---|
| P3a Custody store (SD-2) | stakeholder arranges; custodian builds | fresh store for 7.2, `ACCESS-LOG.md` (append-only, outside the freeze list), `FREEZE-GATE.json` | attestation before/after each custodian session |
| P3b Fixtures and corpus | custodian | corpus meeting section 3 on the deterministic-activation runs; oracles; calibration set; owed-ness rulings; the S4 addendum items 1 to 7 | pre-run checker report PASS |
| P4 Arms, keys, profiles | operator + analyst | arms manifest for candidate, 6.6 and 6.5; executor key (60 / 2400 s); evaluator profile with a non-executor model | package digests match immutable refs; profiles admissible under `omp.profile_errors`; **Q5c static pre-measurement** of the generated installed entrypoint and each owner read on T1/T7/T8, per mode, for the final campaign package leaves the 512 B margin (contract §5; a breach stops qualification and goes to the stakeholder); **Q5d static check** (byte identity outside the block, frozen-minimum mapping complete) run, with its result written into the record's `static` block by the analyst |
| P5 Pre-run check | checker | counts and pass/fail: freshness, exposure recount, run-plan, oracles, custody trail, the slot declaration (`non_owed`, routes, arms, subject commits, profile key) and the gate map for `build_campaign_record.py` | PASS |
| P6 Precondition C | custodian + analyst, before any candidate result is computed | C(a) oracles on known-good/bad; C(b) evaluator ≥ 35/40 and ≥ 8 of 10 known failures; C(c) A/A screen after B1/B2 | contract §4; at most two attempts, the second only after a documented repair; a failure of C is never a candidate result |
| P7 Launch | **stakeholder** | run trees per arm | provider credential in the user's environment; launches from the user's own shell (an agent-runner session tore down the detached process in the first S4 rerun attempt, and the first S4 launch also failed from an agent session) |
| P8 Escalations | analyst | written disposition per packet | infrastructure failures rerun once with both identities recorded; a second failure is inadmissible (contract §3); no other rerun |
| P9 Evaluation | operator launches the evaluator | one disposition per frozen item | wrapper rejects missing, duplicate or altered items |
| P10 Score | analyst | campaign record, `h4.py score` | all gates; report descriptive items (contract §7) with Wilson 90% intervals; list every candidate critical error; any error kind absent from B1 and B2 goes to the stakeholder |
| P11 Human comprehension sample (SD-R8) | stakeholder | trial result | the stakeholder's judgment at ratification |
| P12 Result record | analyst to stakeholder | qualification result record, labelled by key | stakeholder decision |

## 6. Rules carried from S4

- Development probes never count (contract §2); the S4 corpus, episodes and results enter no gate.
- Q5c runs are fresh and paired, and the report carries the matched-mode comparisons (entrypoint-only against owner-read) next to each route's median; the T7 added-pair rule is predeclared. Report native and shell-counted bytes separately (SD-R16.4) and each run's mode.
- Binding verdicts decide; advisory regex verdicts never enter a gate (`h4.py`). Evaluator dispositions enter only through the frozen rubric.
- An undelivered deterministic run, a development-purpose run, an omitted or duplicated slot, a mismatched profile or subject commit is an INTEGRITY stop (the analyst stops the campaign; the fix is a new record, never a patch).
- Change control (contract §8): before exposure any change needs recomputed operating characteristics, an independent check and a stakeholder decision; after exposure a threshold change needs fresh blind fixtures.

## 7. Decisions before P3a (taken 2026-10-08: the user accepted the analyst's recommendations)

| # | Decision | Taken |
|---|---|---|
| 1 | Custody arrangement for the 7.2 store (SD-2) | **(b) attestation path from day one:** access log outside the freeze list, written role attestations, manual metadata snapshots (gap 3). Technical denial with a dedicated uid is not required; the 7.1 recommendation stands. |
| 2 | Custodian, pre-run checker, evaluator | Named in `S4-STAKEHOLDER-RULINGS-2026-10-08.md` (custodian-7.2-b restart on `~/ssdp72b-fixture-custody`; checker-p5-7.2-a; evaluator: deepinfra/deepseek-ai/DeepSeek-V4.1-Flash, section 10). Fresh, separate capable sessions: the analyst is none of them, and the evaluator model is never the executor's. **Exception recorded 2026-10-08:** at the stakeholder's instruction the analyst launched agent sessions, `custodian-7.2-a` (Opus agent) for the addendum items and `checker-draft-7.2-a` for the independent check of this draft (`S4-CUSTODIAN-DELIVERY-RECORD-2026-10-08.md`). The stakeholder accepted that these are weaker than separate sessions; the custody control is the attestation trail. The first custodian pass (`~/ssdp72-fixture-custody`) is superseded. |
| 3 | Comparison executor | **None.** The campaign runs the gating flash executor only; a comparison executor is descriptive and adds cost and reading load without a gate. |
| 4 | Wall-clock and parallelism | Wall-clock stays 2400 s and 60 turns (the frozen profile). Runs in flight stay at 8 or fewer. `--parallel N` runs N pairs, and the arms of a pair run one after another inside one worker, so N is also the number of runs in flight (confirmed against `harness70.py`): use `--parallel 8` at most. A pair of three arms takes up to 3 × 2400 s of wall time. `episode_index` for the alternation is the index in the whole corpus, so chunk with `--only` over both parities; the builder audits the global first-arm balance. Corpus A at 20 in flight lost 4 of 92 runs to 502s, cause unknown. The checker may lower the limit; nobody raises it without a recorded reason. |
| 5 | Replicates | One per episode and arm (contract §2). The 7.1 two-replicate note does not apply. |
| 6 | Rerun rule | Contract §3 only: a provider-lost run is rerun once into a separate directory, both identities kept, a second failure is inadmissible. No other rerun path. |
| 7 | Campaign-record builder (gap 4) | **Commission it** as an analyst tool, regression-tested against the S4 runs, before P10. |

These are recorded decisions, not an issue of the work order: the draft still needs the independent check that the contract's change control requires for any exposure change before it takes effect.

## 8. Gaps the analyst found (instrument, not candidate)

1. No mechanical **corpus freshness** gate against the disclosed material (the 7.1 `disclosed-material.json` check is gone). The checker does it by digest and judgment.
2. No **slot completeness/omission/duplicate audit**. The checker confirms the run declarations cover corpus × arms × replicates exactly; the analyst compares run directories to the declaration after launch.
3. No **custody-stat** tool; the attestation trail and manual metadata snapshots stand in.
4. **Campaign-record builder:** built and fail-closed (`build_campaign_record.py`, tests in `test_build_campaign_record.py`, regression against the S4 runs). It requires the gate map, a slot declaration (with the custodian's `non_owed` flags), the subject commit per arm and the profile key. It treats a mapped measure that matches no item, an item without a resolved verdict, a duplicate or missing slot, a rerun outside the contract rule, a wrong execution mode or purpose, an undelivered activation and non-alternating `pair_order` as findings (exit 3 or 4). It builds Q1 to Q4 and Q5c observations only. Q5a, Q5b, Q5e, Q5f, evaluator dispositions (`--dispositions`), Precondition C and the `static` block come from the custodian, checker, evaluator and analyst, in formats that do not exist yet. The measure-to-gate map is data for the checker to confirm. The earlier `h4.py` Q2U change was reverted: Q2b counts unowed request parts in delegate episodes only, and an unowed request in a run that is not a delegate episode is in no gate (stakeholder ruling U-1): it is a descriptive count per arm. The S4 compound counted the EP-092 case in Q4d as a conservative assumption; under the ruling it is not scored, so the campaign figure is not worse for it.
5. **Interleaving:** satisfied by one `matrix --arm cand --arm b1 --arm b2` invocation per chunk (alternation by episode parity, `pair_order` recorded). The builder audits it; it cannot audit that B2 ran in the same time window, so the checker confirms the schedule from `matrix-scheduler.jsonl`.
6. **Evaluator profile and C(b)** are measured nowhere yet; S4 used none.
7. **Unmeasured by S4:** Q5a, Q5b, Q5d, Q5e, Q5f stay at planning values; the evaluator and Precondition C are unmeasured.

8. **Rulings taken and what remains** (`S4-STAKEHOLDER-RULINGS-2026-10-08.md`). Taken: A-1, A-3, A-5, U-1 (final), U-2, U-3, A-8, the scored-run definition. The custodian (`custodian-7.2-b`) builds on them. Still open: A-9 (the checker confirms the class-to-measure mapping) and the contract terms that remain undefined: "non-owed run" is the custodian's declaration, and any later change to what Q2b, Q4b or Q4d count needs contract §8 change control and, after exposure, fresh blind fixtures.
9. **A deterministic Q4b/Q4d oracle needs structured trace facts** (what the delegate returned, and what the run did), not report text alone. Until the oracle can read them, those fixtures calibrate the evaluator (Precondition C(b)) rather than a deterministic oracle.
10. **Partial delivery:** only the addendum items were delivered to the custodian. The campaign corpus, keys, aggregate-oracle changes and human-trial banks have no work order, because the 7.1 custodian package depends on retired tooling. This blocks P3b, and the campaign cannot start without it.

Gaps 1 to 3, 6 and 7 are covered by the checker and the attestation trail or accepted explicitly by the stakeholder. Gaps 8 to 10 need a stakeholder ruling or a work order before P3b.

## 9. What is needed to proceed

1. The two stakeholder rulings of section 11 and a last independent re-read of the revised text.
2. Precondition C: C(a) from the custodian's probe record, C(b) with the frozen evaluator, C(c) after the B1/B2 runs.
3. The candidate freeze, then the custody freeze (the operator sets FREEZE-GATE after the checker's PASS and the stakeholder's decision).
4. The stakeholder's launch authorization and the credential in the operator's shell; the analyst then writes `READY`.

## 10. Decisions and changes of 2026-10-09 (stakeholder: "go with your recommendation", "freeze the evaluator model as DeepSeek V4.1 Flash")

| Item | Decision |
|---|---|
| Evaluator | `deepinfra/deepseek-ai/DeepSeek-V4.1-Flash`, frozen in the campaign directory (profile digest in `campaign-identity.json`), read-only evaluator profile, 20-turn cap (the template allowed 40), same provider route and credential variable as the executor. Never the executor model (contract section 3; `assess70.py` refuses). |
| Evaluator scope | The main, versioning and sentinel panels. Routing, unversioned and burden items are binding oracles or recorded bytes and need no model. |
| Staged launch (ordering only; see section 11 item 1) | Stage 1 is the main panel (Q1 to Q4 runs), stage 2 the Q5 panels. The analyst computes no candidate gate between the stages; stage 2 is released after `verify --stage 1` shows no INTEGRITY finding. No stage-1 result ends the campaign. An early stop is not available until the stakeholder rules it in under contract section 8 (pending). The runner refuses stage 2 without `authorizations/stage2.ok`, the `READY` line and `DONE-stage1`. |
| Evaluator cost control | A 5-run pilot, measured tokens and dollars (`campaign_assess.py cost`), then the analyst's `authorizations/evaluator-full.ok` before the full evaluator pass. |
| Static margin baseline | The 512 B Q5c static check uses the historical 6.5 figures (8,360 B entry; 25,188 B workflow owner), the figures of the pre-measurement record (the contract states none); the live Q5c gate uses fresh paired 6.5 runs (stage 2 measured 38,187 B and 72,996 B under this executor, so the live caps are far looser). Q5d is checked by `tests/test_protocol_72_scientific_checks.py` (byte identity outside the block, mapping complete), run by `prepare_campaign.py static`. |
| Cost | About $14 executor (per-run costs recorded in the S4 usage events (about $0.03 per main-style run and $0.007 per route probe); the S4 total of $3.10 is derived from them, not a billed figure) and an evaluator estimate of about $13 to $20 to be replaced by the pilot. |
| Precondition C record | `prepare_campaign.py assemble` merges the built record, the custodian's `precondition-c-a.json`, the `score_cb.py` counts (n, agree, failures = the designated 10, caught) and the static block into the `h4.py score` input. |
| Open term | The designated 10 known failures of the C(b) set fix the sensitivity rule at 10 (fifth-set ruling), because `h4.py` and the contract require 10. |

## 11. Answers to the third independent re-read (2026-10-09)

The re-read returned NO-PASS: one Serious Challenge and five blockers.

1. **Serious Challenge: interim scoring between stages conflicts with contract §4 (C(c) before any candidate result is computed), §2 and the Q1 population ("all runs").** Resolved in the conservative direction by default, pending a stakeholder §8 ruling:
   - Stage 1 and stage 2 are an **ordering only**. The analyst computes no candidate gate between them. Stage 2 is released as soon as stage 1 has been verified (`verify --stage 1`, no INTEGRITY finding) and the evaluator pilot has been costed. No stage-1 result ends the campaign.
   - C(c) is computed from B1 and B2 only (`h4.py precondition`), after both stages, before any candidate gate is scored. The analyst scores candidate gates once, on the complete record.
   - **Pending stakeholder ruling (§8 change control, recomputed operating characteristics, independent check):** an optional early stop, i.e. stage 2 is not run if stage 1 alone fails Q2 to Q4. If ruled in: Q1 is never terminal at stage 1 (its population is all runs); a stage-1 FAIL stands without the Q5 A/A screen; C(c) is split (Q4 part before stage-1 scoring, Q5 part blind before any candidate Q5 result). Until it is ruled in, the early stop is not available and the staging saves no runs; it still orders the work and gates the evaluator spend.
2. **Blocker 1, T7 add-pair rule.** Conditional commands now hold two episodes each (the T7 pairs are added two at a time; the analyst re-checks the mode and median after each), so the add-on runs can be authorized one command at a time.
3. **Blocker 2, partial conditional audit.** `verify --include-conditional KEY...` includes only the conditional commands that were authorized and run; each slot carries its command key.
4. **Blocker 3, calibration preflight.** `preflight --phase calibration` accepts `CALIBRATION MAY START` and skips the custody-gate line.
5. **Blocker 4, C(b) calibrates a different task from P9.** C(b) judges one curated item per session; P9 gives the evaluator a whole run bundle. The contract's Precondition C(b) is stated on a frozen calibration set with analyst labels and does not specify the session format, so this is an instrument-validity limitation, not a gate change. **Pending stakeholder acceptance** (section 11 item 2). Mitigation proposed: the analyst reads the evidence strings of the 5 pilot assessments of P9 (no fixture or label content) and reports any that look unsupported before the full evaluator pass.
6. **Blocker 5, residue.** Corrected above (evaluator model, Q2 threshold, 6.5 static figures wording, cost wording). The counts in section 3 are the plan's: 225 candidate runs, 366 main-panel runs, 658 runs in total including 18 conditional.
7. **T7 stopping rule, scorer side.** The operational definition the analyst applies and `h4.py` implements is the one in `Q5C-STATIC-PREMEASUREMENT-2026-10-07.md`: add pairs two at a time while either arm's T7 runs are in mixed modes (entrypoint-only and owner-read), up to seven pairs; stop when both arms are single-mode or at seven. The wording "median on a mode boundary" in the contract and the custodian work order is read this way (a mixed-mode arm is the case where the median can sit on the boundary). The analyst decides after each pair of T7 pairs, from the mode counts only. If the stakeholder prefers a narrower rule it needs section 8 change control.
8. **Visible before C(c):** the `verify` audit prints per-arm admissibility counts including the candidate's (an integrity and rerun check). The analyst computes no candidate gate before C(c).
9. **Non-blocking, fixed:** the full evaluator pass refuses without `authorizations/evaluator-full.ok`; the runner refuses to start a stage unless `READY` releases it; `campaign_cb.py` is pinned in the identity and preflight; `h4.py precondition` exits non-zero if the A/A screen fails; the evaluator scope (main, versioning, sentinels) covers every item needing judgement, and an advisory item on another panel would stay UNRESOLVED and block scoring (the analyst's waiver would label the record NOT A QUALIFICATION RESULT).

Stakeholder rulings pending: (1) the optional early stop above (default: not available); (2) acceptance of the C(b) versus P9 format limitation.
