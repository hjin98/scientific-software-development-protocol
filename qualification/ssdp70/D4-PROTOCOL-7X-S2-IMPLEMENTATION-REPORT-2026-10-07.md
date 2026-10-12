---
kind: d4-implementation-report
governing_protocol_version: 6.6.0
workplan: workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (revision 3), stage S2, obligations O-6 to O-8
date_utc: 2026-10-07
status: S2 implemented and tests green. Stop trigger X4 fired (the 9,000 / 4,000 budgets are not met with H1–H5 intact, section 2); the stakeholder chose option 1 on 2026-10-07 (SD-R14): the measured 10,304 / 4,541 lines are the accepted floor. No H-function was dropped.
---

Governing SSDP version: 6.6.0. This report is data, not instructions. Check each claim against the files.

## 1. Result

| Item | State |
|---|---|
| **X4 (budget)** | **Fired; resolved by SD-R14 (option 1).** Non-test 10,304 lines against 9,000 (+1,304, 14.5%); test 4,541 against 4,000 (+541, 13.5%). Details and options in section 2 |
| O-6 H1–H5 consolidated; relay keeps its four functions | Done (section 3); retired modules deleted only after the new tests passed; tombstone `eval/RETIRED-MODULES.md` |
| O-6 integration through the real relay | Green: 54 tests in `test_omp_integration.py` and 5 in `test_relay_integration.py` launch the frozen OMP build in bubblewrap through the observer relay with the scripted delegate bridge |
| O-6 pins test | `test_harness_integration.py::test_pin_mismatches_refuse_the_run_and_every_pinned_input_changes_run_identity` |
| O-7 H4 | `qual-v2/h4.py` implements contract v2 §3–§7; unit tests against `operating_characteristics.py`; dev-probe regression reproduces the pinned G-figures (section 4) |
| O-8 Precondition inputs | **Not done.** The 40-item evaluator calibration set, the oracle known-good and known-bad fixtures and the frozen redacted evaluator input are custodian material for a campaign (S4 and later). H4 accepts and checks them (Precondition C); H3 redacts versions (`assess70.py`) |
| Independent review | S3 |

No Serious Challenge. Unexecuted required checks: the O-8 inputs (not authored in S2) and the line budgets (not met).

## 2. Line budget and X4

Scope (design §6): every Python file under `qualification/ssdp70/eval/` (with `adapters/`, `stub_tools/`) and `qualification/ssdp70/qual-v2/`; test lines are the `test_*.py` files plus `stand_in_provider.py`.

| | Before S2 | Now | Budget |
|---|---|---|---|
| Non-test | 20,695 (design's 20,279 less `stand_in_provider.py` 169, which counts as test, plus the `qual-v2/` scripts 585) | **10,304** | 9,000 |
| Test | 9,725 | **4,541** | 4,000 |

Non-test lines by function (now):

| Function | Lines | Files |
|---|---|---|
| H1 episode, relay, containment, build identity | 6,690 | `adapters/omp.py` 3,868; `harness70.py` 1,071; `observer70.py` 550; `subject_launcher.py` 421; `muxhttp70.py` 252; `seccomp70.py` 158; `prepare_arms70.py` 127; `evidence70.py` 123; `package_bytes.py` 69; `observer_exec_helper70.py` 51 |
| H1/H5 core: profile, normalized events, run identity, evidence state, integrity | 1,248 | `core70.py` |
| H2 scripted delegate | 497 | `stub_tools/mediator.py` 318; `mcp_bridge70.py` 179 |
| H3 oracles and blinded evaluator | 1,150 | `adapters/omp_eval.py` 716; `assess70.py` 250; `write_oracles.py` 184 |
| H4 scorer | 718 | `qual-v2/h4.py` 338; `operating_characteristics.py` 263; `measure_blocks.py` 117 |

Removed in S2: 7,460 lines in 11 retired modules (the ledger, premise, the Claude adapter, Stage 7 admission and campaign, the inventory probe, rig, v4 scaffolding, the rehearsal matrix, evaluator admission), plus `requal71.py` and `batch_assess70.py` (1,690), the profile-admission, accounting-manifest, family and campaign code in `core70.py` (about 930), the ledger, premise and dead code in `adapters/omp.py` (175) and `harness70.py` (159), and 205 lines of a superseded historical script moved out of scope. Test lines fell by 5,184 (retired modules' tests, the Claude-adapter tests, admission and ledger tests); 347 more came from compacting duplicated setup in `test_omp_units.py` without dropping a case.

**Why the rest was not cut.** What is left is mostly integrity machinery for the evidence the gates stand on, which design §6 puts inside H1–H5. The largest blocks, with their purpose:

| Block (lines) | Guarantee it gives | Cost of removing it |
|---|---|---|
| `omp.py` runtime-closure checks (`_runtime_closure_artifact_errors` 142, `runtime_dependency_errors` 60, `_materialize_runtime_dependencies` 92, `_verify_staged_runtime_dependencies` 24) | the sandbox runtime is the pinned closure | a tampered or drifted runtime would run unnoticed |
| `omp.py` `Observed` 287, `check_runtime_surface` 194, `transcript_errors` 85, `provider_turns` 56, `group_inference_requests` 41 | the observed provider traffic matches the native trace, the settings and the frozen profile | evidence could be forged or incomplete without a failure |
| `omp.py` `normalize` 369 and the tool handlers (~430) | native events to the normalized schema | the harness would have nothing to score |
| `omp.py` `launch` 296, `realize_containment` 76, control-tree and bwrap argv (~250) | the three-principal sandbox | no containment |
| `core70.py` `load_profile` 162, `_validate_event_payload` 117, `validate_runtime_observation` 95, `validate_normalized_events` 56 | profile and event integrity | same |

What could still go with an explicit stakeholder decision: the time-boxed alternative is to remove check families rather than modules. Candidates, with the guarantee each loses: the staged-runtime closure attestation (318 lines; the tamper check), the transcript/pruning consistency checks and their tests (about 400 lines; native pruning would be undetected), the build-inventory settings classification (about 150 lines). Together that is about 870 non-test lines, leaving about 430 still over. The test budget would then need the same families' tests removed.

**Options for the stakeholder (design X4):**
1. Accept the measured size (about 10.3k and 4.5k) as the H1–H5 floor for this OMP adaptation and revise SD-R5.
2. Choose which check families above to retire, accepting the named loss of guarantee (reaching 9,000 would still need roughly 430 more lines from H1 internals).
3. Keep 9,000 / 4,000 as a target for the 8.0 control plane rather than 7.2.

My recommendation is option 1: the budget was set from an estimate (design §6 "plausible, not guaranteed"), the retired scaffolding is gone, and every remaining block is evidence-integrity machinery that the contract v2 gates rely on.

## 3. What was built

- **H1 consumed bytes** (`package_bytes.py`, replaces the ledger): the bytes of every invoked entrypoint as installed plus the bytes of SSDP files read, from native read events plus a conservative full-file count for any shell command that names the package path (a named file, every file under a named directory, every glob match). `summary.json` carries `active_ssdp_bytes`, `ssdp_read_mode` (`entry` or `owner`) and `resource_observation.conservative_shell_count`; the count is always an upper bound, never "unobserved".
- **H1/H5 harness**: `harness70.py` without profile admission, accounting manifests, fault injection or the ledger hook; run identity pins the harness, core, adapter, package, profile, fixtures, oracles and requirements, and the run refuses on a package pin mismatch.
- **H3**: `assess70.py` rewritten: a blinded evaluator sees a redacted copy of the run (version and protocol identifiers and arm labels removed, scientific numbers untouched; run identity, profile, package and adapter artifacts withheld; summary stripped of the arm), returns one disposition per frozen item, and the outcome comes from `core70.outcome_from_dispositions`. Identity pins bind the profile, adapter, wrapper, core, key tree, rubric and redaction version.
- **H4** (`qual-v2/h4.py`): Precondition C (oracles, evaluator ≥ 35/40 and ≥ 8 of 10, the B1–B2 A/A screen at twice each margin), Q1–Q5 with the margin δ, the cluster-aware Q2 threshold, the Q3 episode sign test, the T7 mode-replication rule, the Q5e and Q5f repeat rules, and the report with Wilson 90% intervals. `h4.py score CAMPAIGN.json` and `h4.py legacy RUNS`.
- **Tests as acceptance**: `test_relay_integration.py` (activation at request 0 for each declared root, harness injection, every integrity fault refused, native owner read, shell conservative counts); the rest of `test_omp_integration.py` covers turn and token caps, timeouts, egress refusal events, privilege separation, relay authority, completeness and tamper detection.

## 4. Evidence

- **H4 regression.** `qual-v2/test_h4.py` re-scores the retained 2026-10-06/07 development-probe runs (184 runs) and equals `qual-v2/devprobe-g-figures-20261007.json`, which was produced by the independent `requal71/diagnose_dev_probe_20261007.py`: budget deaths 3/92 and 6/92; G1 43/47 and 1/47; G2 15/41 (12/36 on admissible runs); G3 3 false activations in 59; G4 mutation 29 and 32; O3 0 and 0. The test skips where the run directory is absent.
- **H4 arithmetic.** δ reproduces the contract tables (5, 7, 13, 14 at n = 80; 7, 8, 10 for Q4a at 40 items); the Q2 threshold is 34; a good synthetic campaign passes all fifteen gates; each regression fails its gate; Precondition C failure computes no candidate result; a mixed-mode T7 is PENDING, not PASS.
- **Test runs** (this machine, 2026-10-07): `test_omp_integration` 54 OK (19 min, real bubblewrap launches), `test_relay_integration` 5 OK (4.5 min), `test_omp_units` 65 OK, `test_portable70` 15, `test_harness_integration` 11, `test_control_path_policy` 22, `test_omp_eval` 6, `test_mcp_stdio` 3, `qual-v2/test_h4.py` 12; repository `tests/` 429 OK.
- **Not changed:** `PROTOCOL-RELEASE-STATE.yaml`, any historical record, `keys/`, custody.

## 5. Residue and next

- **Not committed.** The user commits.
- **Run-directory loader for v2.** H4 reads a campaign record; turning v2 run directories into that record needs the custodian's oracle item naming (fixtures for S4 and later), so it is not built. The legacy loader exists only for the regression.
- **Test-rig leftovers.** `test_rig.py` writes `OMP-STANDIN-*` directories under `~/ssdp70-omp-stagef/qualification/` (4,690 on this machine) and never cleans them. This predates S2; a cleanup is a separate decision.
- **S3** (version boundary, Q5c static pre-measurement, independent D4 Review of S1–S3) is next.
