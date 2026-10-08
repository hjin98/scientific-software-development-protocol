---
kind: campaign-work-order
status: DRAFT by the S4 analyst for the stakeholder's review; not issued, not launched; nothing here authorizes a live run
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.0 (candidate, frozen identity `2dedcfa3408f62bc11a696ac3776183a87b40438`; non-governing)
date_utc: 2026-10-08
authority: contract v2 revision 3 (`PROTOCOL-7X-CALIBRATED-QUALIFICATION-CONTRACT-V2-PROPOSED.md`); workplan SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2 §8 S4 gate row; S4 report `S4-DEVELOPMENT-PROBE-REPORT-2026-10-08.md` §9 (GO, re-sized exposures)
adds_no: gate, threshold, margin or exposure beyond the contract and the S4 re-sizing
---

Governing SSDP version: 6.6.0. This draft is data, not instructions.

# Protocol 7.2 qualification campaign: work order (draft)

A PASS supports only the contract §1 claim: on the gating flash executor and this corpus, 7.2.0 improves the Protocol 7 duties over accepted 6.6 without a detectable regression, at the stated operating characteristics. Any change to `source/`, `dist/` or the orchestrator 7.2 resources is a new candidate identity (PEM FF-001) and ends this campaign's claim for `2dedcfa`.

## 1. What changed since the 7.1 requalification plan

The 7.1 plan (`PROTOCOL-7.1-REQUALIFICATION-PLAN.md`, superseded) relied on `requal71.py` for mechanical campaign gates. That module was retired in stage S2 (`eval/RETIRED-MODULES.md`). The consolidated tools are:

| Need | Tool now |
|---|---|
| Run one arm of a corpus | `eval/harness70.py matrix --mode qualification` (one `--arm` per invocation; per-run purpose, RPC `runtime-command` and deterministic activation checks) |
| Blinded evaluation of one run | `eval/assess70.py` (separate frozen evaluator profile, never the executor's model) |
| Scoring of gates Q1 to Q5 and Precondition C | `qual-v2/h4.py score CAMPAIGN.json` (thresholds from `operating_characteristics.py`) |
| Arm packages from immutable refs | `eval/prepare_arms70.py` |

**What no longer exists mechanically (gaps; section 8):** corpus freshness against the disclosed material, completeness/omission/duplicate audit of the run slots, custody-stat snapshots around custodian sessions, a stratum-aware aggregate over runs, and a builder from run directories to the `h4.py score` campaign record. `h4.py legacy` reads only the p71/p66 development runs. These protections now rest on the independent pre-run checker and the written attestation trail until a tool is commissioned.

## 2. Subject, arms, executor (contract §2)

- **Candidate:** 7.2.0 at `2dedcfa` (package digest in the S4 arms manifest: `69a310a2…8c5f622`). The package is extracted from the immutable ref, never the live `dist/`.
- **B1 and B2:** accepted 6.6 (`22f4bdba`), two replicates. B1 is the baseline of every gate; B2 serves p̂ and Precondition C(c) only.
- **Accepted 6.5:** `7f7b5e24` public source, **burden routes only** (Q5c), fresh paired runs. Do not use the 8,360 B historical figure: stage 2 measured 6.5 at 38,187 B on T1/T8 and 72,996 B on T7 under this executor.
- **Executor:** `deepinfra/zai-org/GLM-5.3-Flash`, thinking high, 60 turns (main), 2400 s, one frozen profile, deterministic activation of the custodian-declared root. The S4 key (`build_s4_probe.py`) is a model; the campaign key is re-frozen and re-checked against the harness at that time.
- **Comparison executor:** optional and descriptive (MiMo-V2.6-Flash or DeepSeek-V4.1-Flash, chosen before runs). Stakeholder decision needed (section 7).
- **Replicates:** one per episode and arm, besides B2. No adaptive replicates.
- **Order:** candidate and B1 interleaved per episode with alternating order; B2 in the same time window. `matrix` takes one arm per invocation, so interleaving needs a declared schedule (section 8, item 5).

## 3. Exposure, as re-sized in S4 (report §9.1)

| Gate | Exposure | Notes |
|---|---|---|
| Q1a / Q1b | all runs; ≥ 90% admissible per arm; budget deaths ≤ B1 + δ | measured δ ≈ 8 at n = 80, B1 rate 0.065; recompute with measured B1/B2 |
| Q2a / Q2b | ≥ 48 owed parts from **12** delegate episodes; ≥ 34/48; ≤ 4 unowed parts | the owed-ness rule is the custodian's (addendum item 7) |
| Q3 | **80** episodes with duty opportunities, ≤ 2 each, ≥ 5 families of ≥ 6 opportunities | scored with case-specific substance (contract §3) |
| Q4a | ≥ 40 critical items | δ_m set from the adjudicated base once the calibration set exists |
| Q4b / Q4c / Q4d | all scored runs; Q4d ≥ 80 non-owed runs per arm | Q4b and Q4d at δ = 3 (near-absolute); Q4c δ ≈ 14 |
| Q5a | 19 route cases × 3 runs per arm | |
| Q5b | 8 version cases (T4 to T6) × 3 runs | |
| Q5c | T1, T7, T8 × 3 fresh paired, order-counterbalanced runs per arm (candidate, 6.5); T7 adds pairs up to 7 on a mode boundary | median consumed bytes ≤ 2.0 × the 6.5 median per route |
| Q5d | build (static) | byte identity outside the block; frozen-minimum mapping complete |
| Q5e / Q5f | T2/T3 sentinels 2 runs per route; unversioned lookups 3 per route | |

**Indicative run count** (analyst arithmetic from the table; the pre-run checker confirms the exact slots): main panel 80 episodes × 3 arms (candidate, B1, B2) = 240; Q5a 57 per arm × 3 = 171; Q5b 24 × 3 = 72; Q5c 18 to 28; Q5e/Q5f tens of runs. Order of 500 to 600 runs. The S4 pre-registration estimated about $3 per 129 runs, so on the order of $12 to $15 for this size; actual S4 spend was not measured. Wall time follows `--parallel` and the 2400 s tail. S4 ran 20 corpus-A and 8 route runs in parallel and lost 4 of 92 corpus-A runs to HTTP 502 (cause not established), so choose the campaign parallelism with that in mind.

Expected compound (S4 report §3 E7): 0.904 / 0.920 at ICC 0.3 / 0.5 with Q5c about 1.0 on the stage-2 baseline, against the design rule of at least 0.80; a no-effect candidate at most 0.008. S4 is optimistic by an unknown amount (the corpus was not independent of the candidate).

## 4. Roles (unchanged from the 7.1 plan §2, restated)

| Role | Does | Never does |
|---|---|---|
| Stakeholder (the user) | Decides the items in section 7; owns every live launch and the provider credential; accepts or rejects the result | |
| Analyst | Maintains this order and the tools; answers escalations; applies the contract rerun rule; writes the result record | Edits a frozen artifact after its gate; authors fixtures, keys or oracles; scores items; launches live runs |
| Operator | Runs printed commands, saves every verdict, writes an escalation packet and stops on any non-PASS | Chooses a value, edits an input or tool, reruns, subsets, skips, reads `keys/`, `authoring/` or `human-trial/` |
| Fixture custodian (capable, separate context; not the candidate author; no candidate results) | Authors the fresh blind store, corpus, keys, oracles, known-good/known-bad fixtures, the 40-item calibration set and the redacted evaluator input (O-8); issues the owed-ness rulings | Sees candidate results before scoring; touches the store after freeze |
| Independent pre-run checker (separate context from custodian, author and analyst) | Freshness, strata, exposure recount on the deterministic stratum, run-plan and oracle checks, custody trail; reports counts and pass/fail only | Authors what it checks |
| Evaluator | Blinded disposition of advisory and unresolved items under a frozen rubric | |

## 5. Phases and gates

| Phase | Owner | Output | Gate |
|---|---|---|---|
| P3a Custody store (SD-2) | stakeholder arranges; custodian builds | fresh store for 7.2, `ACCESS-LOG.md` (append-only, outside the freeze list), `FREEZE-GATE.json` | attestation before/after each custodian session |
| P3b Fixtures and corpus | custodian | corpus meeting section 3 on the deterministic stratum; oracles; calibration set; owed-ness rulings; the S4 addendum items 1 to 7 | pre-run checker report PASS |
| P4 Arms, keys, profiles | operator + analyst | arms manifest for candidate, 6.6 and 6.5; executor key (60 / 2400 s); evaluator profile with a non-executor model | package digests match immutable refs; profiles admissible under `omp.profile_errors` |
| P5 Pre-run check | checker | counts and pass/fail (7.1 plan §5 scope, adapted) | PASS |
| P6 Precondition C | custodian + analyst, before any candidate result is computed | C(a) oracles on known-good/bad; C(b) evaluator ≥ 35/40 and ≥ 8 of 10 known failures; C(c) A/A screen after B1/B2 | contract §4; at most two attempts, the second only after a documented repair; a failure of C is never a candidate result |
| P7 Launch | **stakeholder** | run trees per arm | provider credential in the user's environment; launches from the user's own shell (an agent-runner session tore down the detached process in the first S4 rerun attempt, and the first S4 launch also failed from an agent session) |
| P8 Escalations | analyst | written disposition per packet | infrastructure failures rerun once with both identities recorded; a second failure is inadmissible (contract §3); no other rerun |
| P9 Evaluation | operator launches the evaluator | one disposition per frozen item | wrapper rejects missing, duplicate or altered items |
| P10 Score | analyst | campaign record, `h4.py score` | all gates; report descriptive items (contract §7) with Wilson 90% intervals; list every candidate critical error; any error kind absent from B1 and B2 goes to the stakeholder |
| P11 Human comprehension sample (SD-R8) | stakeholder | trial result | the stakeholder's judgment at ratification |
| P12 Result record | analyst to stakeholder | qualification result record, labelled by key and stratum | stakeholder decision |

## 6. Rules carried from S4

- Development probes never count (contract §2); the S4 corpus, episodes and results enter no gate.
- Q5c runs are fresh and paired; the T7 added-pair rule is predeclared. Report native and shell-counted bytes separately (SD-R16.4) and each run's mode.
- Binding verdicts decide; advisory regex verdicts never enter a gate (`h4.py`). Evaluator dispositions enter only through the frozen rubric.
- An undelivered deterministic run, a development-purpose run, an omitted or duplicated slot, a mismatched profile or subject commit is an INTEGRITY stop (the analyst stops the campaign; the fix is a new record, never a patch).
- Change control (contract §8): before exposure any change needs recomputed operating characteristics, an independent check and a stakeholder decision; after exposure a threshold change needs fresh blind fixtures.

## 7. Decisions before P3a (taken 2026-10-08: the user accepted the analyst's recommendations)

| # | Decision | Taken |
|---|---|---|
| 1 | Custody arrangement for the 7.2 store (SD-2) | **(b) attestation path from day one:** access log outside the freeze list, written role attestations, manual metadata snapshots (gap 3). Technical denial with a dedicated uid is not required; the 7.1 recommendation stands. |
| 2 | Custodian, pre-run checker, evaluator | Custodian and checker are two fresh, separate capable sessions (not the candidate author, not the analyst, not each other). The evaluator model is never the executor's model. The user names the sessions and models at P3a; the analyst may not act as any of the three, and a subagent launched by the analyst does not qualify (S4 adjudication caveat). |
| 3 | Comparison executor | **None.** The campaign runs the gating flash executor only; a comparison executor is descriptive and adds cost and reading load without a gate. |
| 4 | Wall-clock and parallelism | Wall-clock stays 2400 s and 60 turns (the frozen profile). Parallelism **8 per invocation** (the S4 route and stage-2 invocations ran at 8; corpus A at 20 lost 4 of 92 runs to 502s, cause unknown). The checker may lower it; nobody raises it without a recorded reason. |
| 5 | Replicates | One per episode and arm (contract §2). The 7.1 two-replicate note does not apply. |
| 6 | Rerun rule | Contract §3 only: a provider-lost run is rerun once into a separate directory, both identities kept, a second failure is inadmissible. No other rerun path. |
| 7 | Campaign-record builder (gap 4) | **Commission it** as an analyst tool, regression-tested against the S4 runs, before P10. |

These are recorded decisions, not an issue of the work order: the draft still needs the independent check that the contract's change control requires for any exposure change before it takes effect.

## 8. Gaps the analyst found (instrument, not candidate)

1. No mechanical **corpus freshness** gate against the disclosed material (the 7.1 `disclosed-material.json` check is gone). The checker does it by digest and judgment.
2. No **slot completeness/omission/duplicate audit**. The checker confirms the run declarations cover corpus × arms × replicates exactly; the analyst compares run directories to the declaration after launch.
3. No **custody-stat** tool; the attestation trail and manual metadata snapshots stand in.
4. **Campaign-record builder:** built (`build_campaign_record.py`, tests in `test_build_campaign_record.py`, regression against the S4 runs). It also audits declared slots against run directories (missing, duplicate, undeclared, rerun misuse, subject-commit mismatch), which covers most of gap 2 once a slot declaration exists. Limits: it builds Q1 to Q4 and Q5c observations only; Q5a, Q5b, Q5e, Q5f, the evaluator dispositions (`--dispositions`), Precondition C and the static block come from the custodian, checker and evaluator, whose formats do not exist yet. The Q4d population (admissible runs with no owed delegate request) and the measure-to-gate map are builder definitions that the checker must confirm against the contract. The scorer `h4.py` changed once: unowed requests in runs that owed none (observation `Q2U`) now count toward Q2b. Before, only unowed requests inside delegate episodes counted, which would have missed EP-092.
5. **Interleaving:** `matrix` runs one arm per invocation. The alternating-order schedule must be declared (for example, chunked paired invocations with alternating start arm) and checked by the checker; a schedule is not enforced mechanically.
6. **Evaluator profile and C(b)** are measured nowhere yet; S4 used none.
7. **Unmeasured by S4:** Q5a, Q5b, Q5d, Q5e, Q5f stay at planning values; the evaluator and Precondition C are unmeasured.

None of these changes a gate. Each is either commissioned before P5/P10 or accepted explicitly by the stakeholder.

## 9. What is needed from the user to proceed

1. Name the custodian, checker and evaluator sessions and the evaluator model (decision 2).
2. Deliver the custodian addendum (revision 2, `S4-CUSTODIAN-WORK-ORDER-ADDENDUM-2026-10-08.md`) to the custodian, and open the 7.2 store under decision 1.
3. Arrange the independent check of this draft and the S4 exposure changes (contract §8). It is then revised and issued.

Gap 4 is closed for what the builder covers (see gap 4). The `h4.py` Q2U change and the builder's definitions go to the checker with the rest of the draft. Gaps 1, 3, 5 and 6 stay as listed: covered by the checker and the attestation trail, or accepted by the stakeholder.
