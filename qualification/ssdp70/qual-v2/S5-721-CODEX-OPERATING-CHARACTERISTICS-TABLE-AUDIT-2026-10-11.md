# Independent bounded operating-characteristic table audit — 2026-10-11

Governing SSDP 6.6.0; reduction plan revision4 §7. Disposition: **PASS for recorded simulation/table consistency; S4 live-release STOP remains.** This is an audit of completed synthetic evidence, with no re-simulation, new acceptance run, changed thresholds, live call or authorization. The separate applicability/runbook review remains unchanged.

## Binding and executed checks

Subject candidate `52ac475ce81d89b3e8ccb7c393fa0daa028d01b0`. Completed table `OPERATING-CHARACTERISTICS.md` SHA `49fbb2f16c5747ce52a3c4e02cf0365bed0905dd15a62a3c35318f59a625df13`; frozen comparison script SHA `7541b0d5e2a1c8d46de41d69ed40cee5c2cd5f9c0ae9d266085d0f1318c95db3`. Independently hashed actual table/script bytes against `OPERATING-CHARACTERISTICS-IDENTITY.json`; both match. Both table and identity are included in updated `FREEZE.sha256`; reviewer reran checksum verification and all13 entries passed.

Recorded invocation:

`env -u SSDP70_OMP_PROVIDER_CREDENTIAL python3 qualification/ssdp70/qual-v2/compare_721.py simulate --reps 300 --icc 0.3 --resamples 10000 --seed 20261011`

Its parameters match the table header, identity and frozen specification: nine scenarios, 300 simulated campaigns each, 10,000 paired episode-cluster bootstrap resamples per campaign, seed20261011, latent logit ICC0.3, historical unresolved rates multiplied by the default1.0, external conditions assumed true. The script's simulator invokes the reviewed evaluate decision function on synthetic clustered tallies with W/B bracket and both replicates carried by episode. No alternate decision function, margin or item pool is invoked. Completed output contains all nine rows; this audit checks the retained invocation/result and does not independently reproduce the stochastic simulation.

All nine outcome dictionaries independently sum to300 (2,700 synthetic campaigns total), and each rendered go probability equals its count/300 rounded to two decimals:

| Scenario | Go count /300 | Exact percentage |
|---|---:|---:|
| narration2%, otherwise neutral | 39 | 13.00% |
| narration5% | 8 | 2.67% |
| no narration improvement | 0 | 0% |
| good + delegated_finding_loss3/14 | 16 | 5.33% |
| good + tension_report17/26 | 13 | 4.33% |
| good + detection.unnamed85% | 7 | 2.33% |
| good + claim_integrity20% | 1 | 0.33% |
| good + o1_authoring100% | 0 | 0% |
| good + delegate F/R/T/V at6.6 rates | 0 | 0% |

The good scenario's remaining outcomes are168 no-go and93 not established; narration5% has168 no-go and124 not established; no improvement has250 no-go and50 not established. The rounded0.00 for the claim-integrity regression row means1/300, not an observed zero; its integer count remains visible.

## Interpretation and governing consequence

The final required synthetic table supersedes the earlier pre-W/B87–89% forecast as decision-support evidence for this declared synthetic regime. A favorable synthetic candidate now reaches go39/300 even while external conditions are assumed satisfied. This supports the lead's **SERIOUS CHALLENGE to the measurement campaign's planning forecast and cost/decision justification**, and the recommendation to hold the approximately$20 spend pending the real owner/stakeholder's reconsideration. It does not prove that the actual7.2.1 candidate fails, nor that the underlying decision rule is universally inadequate. No live candidate outcomes exist.

The simulation is limited by 300 campaigns/scenario, synthetic item assignment, the specified latent correlation, historical unresolved-rate assumptions, and assumed external passes. Those assumptions do not establish actual candidate error rates, empirical episode dependence or evaluator resolution performance. Differences from the old forecast cannot be causally allocated among W/B, clustering and other jointly changed modelling assumptions from this table alone. No threshold, fixture, replicate or semantic change follows automatically.

The root decision packet `S5-721-CODEX-S4-DECISION-PACKET-2026-10-11.md` correctly preserves this evidence scope, labels the forecast challenge, recommends hold, and independently retains the unresolved C(b) execution-support applicability STOP. No new calibration attempt is authorized; exact calibrated source recovery or explicit evidence-limitation adjudication remains a separate gate. Candidate S2b/S3 bounded passes remain unaffected. The now-completed table closes only the previously pending simulation-table publication task; it does not close campaign-value adjudication, calibration applicability, live spend release, dependent authorizations, execution, actual result interpretation, ratification or qualification.
