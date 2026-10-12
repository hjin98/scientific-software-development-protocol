# OMP-only Stage F — Stage 6 evidence and closure

- **Date:** 2026-09-30
- **Governing SSDP:** 6.6.0
- **Branch and starting head:** `ssdp-7.0-scientific-epistemic-closure` at `0850d61f0302e1c22eae54f6b4c81cdff7af2ba1`
- **Immutable Protocol 7 semantic candidate:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **Status:** **STAGE 6 BLOCKED. OMP remains UNADMITTED.** This record does not admit the profile, authorize qualification subjects, or replace the fresh independent Stage 7 runner-admission review.

## Authority and scope

The task was reconstructed from repository `AGENTS.md`, the active consolidated SSDP 7.0 workplan, evaluation contract §1 items 1–11 and §6, current code under `qualification/ssdp70/eval/`, and the existing Stage F OMP D3/D4 records. The D3 three-principal architecture remains the accepted boundary. No condition requiring a D3 reopening was found, and no Serious Challenge to that architecture is raised here.

Stage 6 requires both retained exact-profile operator evidence and hostile containment/discovery verification. Required checks that fail before reaching their intended owner do not count as PASS. The later independent runner-admission reviewer must still assess every contract §1 item 1–11 and §6; that review and all Protocol 7 subjects were out of scope and were not run.

## Retained positive real-provider probe

The supplied directory was kept read-only:

`/home/samjin/ssdp70-omp-live-probe-20260930T041652Z/out/OMP-LIVE-1-p70-r0`

Its retained `run-identity.json`, `summary.json`, and `evidence-integrity.json` agree on internal identity `6fe36d822c54c5dd5b0b8921937bdc32227e67b59ddfeacc4810d68757b34fdc`. All 34 files declared by the integrity manifest still match their recorded byte counts and SHA-256 values. The terminal state is `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED`, and `execution_mode=probe`; NOT_EVALUATED is expected for this probe mode.

There is a material identity discrepancy: the user-supplied run identity `c88938172de9ab888692e42f7fafca4653a5cf4c289cb4ed3a6ab3a32adaaa95` does not match the retained identity-bearing artifacts. This record therefore identifies the evidence by its actual internal identity (`6fe36d…`) and does not claim that the supplied `c889…` value was verified. A fresh reviewer should reconcile this discrepancy before relying on the run for admission.

From the internally consistent retained evidence, the probe establishes:

- The exact `omp/18.0.11` executable and build identity, DeepInfra model `deepinfra/zai-org/GLM-5.3-Flash`, high reasoning setting, JSON v1 output mode, and bound profile/configuration. The probe's adapter support hashes match the current production sources.
- Protocol package identity `db94a2dfb7fef480f37227eab5c45256e89901b8`, with the installed tree matching digest `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b` and the profile-document digest bound by run identity.
- The runtime-derived catalog contains each of the seven expected skills once. The observed native surface is `read`, `glob`, `grep`, `edit`, `write`, `bash`, plus the six runtime-minted `ssdp70` MCP tools (`issue_locations`, `issue_search`, `issue_show`, `issue_create`, `issue_comment`, and `delegate`).
- The actual `root_selection` and `resource_access` records show ordinary `software-implementation` selection by a successful skill read and exact consumption from the bound installed package. No generic or qualification-specific `owner-read` claim is added.
- Retained mediator and normalized events demonstrate an issue read, a mutation with before/after object-version binding, and scripted delegation. Provider observation binds seven inference requests and responses. The exact OMP metadata catalog request `GET /models?filter=with_meta&sort_by=omp` is locally classified and denied with no provider egress.
- Observer evidence records credential receipt after lockdown without subject custody or secret-value retention. The run also retains denials for the probed host/custody/private paths, unrelated network access, and local socket creation. These are evidence for the probes actually recorded in this run; they do not replace the broader hostile matrix required below.
- Evidence chains and normalized completeness checks are admissible. Before/after package and control digests agree. The run-owned HOME inventory classifies its control and OMP-created entries without unclassified residue.

## Negative discovery and containment evidence

The current canonical adapter lists 22 project discovery sources, 39 HOME discovery sources, and 14 credential environment names. Direct `DiscoveryBaselineRefusal` unit tests for the source lists and credential-variable guard passed. Those unit tests establish the validator's refusal behavior; they do not establish assembled exact-profile containment.

The prior integration tests that bypassed the discovery guard to let prohibited configuration reach OMP were replaced in the working tree. The revised tests preserve the production guard and require a source-specific pre-launch refusal, no OMP process start, and no local provider request for each project/HOME source and credential variable. The separate project `.env` fixture-inertness check remains, since project `.env` is not a discovery source under the accepted implementation.

Those assembled controls did **not** execute to their intended assertions on this host. `realize_containment()` stops first at the frozen runtime dependency check, before ambient-source validation, control-tree realization, OMP launch, or provider request. Consequently, no project-source, HOME-source, injected-credential, or project `.env` integration case in this run is counted as a source-specific negative PASS. The same gate prevented assembled tests of host-only files, private supervisor/observer/mediator state, local IPC, unrelated network access, control mutation, and runtime-created-entry integrity.

## Test and repository checks

| Check | Result |
| --- | --- |
| Focused `test_omp_units` and `test_omp_integration` suites | **FAIL.** The exact-profile integration path and frozen host-dependency unit check encounter the dependency mismatch described below. |
| Complete affected evaluation suite: `python3 -W ignore -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -q` | **FAIL:** 238 tests, 77 failures, 47 errors, zero skips. All 47 assembled OMP errors terminate at the same runtime dependency check. The 75 source/credential subcases fail because that earlier dependency error masks their expected ambient-source refusal; the remaining two failures are the active-thread assembled-launch regression and frozen host-dependency assertion, both blocked by the same mismatch. |
| Compile check: `python3 -m compileall -q qualification/ssdp70/eval` | PASS. |
| Static launch check `test_real_omp_launch_path_has_no_preexec_fn_and_binds_exec_helper_digest` | PASS in the focused suite. |
| Project Engineering Memory schema validation | PASS: 5 families, 0 notices. PEM was not changed. |
| `git diff --check` | PASS. |

No required suite was reported as skipped. Passing compile/static/repository checks do not offset the failed assembled tests.

## Blocking environment mismatch and repair disposition

The frozen file `qualification/ssdp70/eval/omp-runtime-dependencies-18.0.11.json` requires:

| Host library | Frozen SHA-256 / bytes | Current SHA-256 / bytes |
| --- | --- | --- |
| `/lib/x86_64-linux-gnu/libssl.so.3` | `3db6aff36baf2ced6dde3f340159edd2504f089c0d735765596ce96d2d835cb1` / 667864 | `51fc92556f11ddce62f3f988d3fe973fab8fb4742032e61a713688581c924262` / 671960 |
| `/lib/x86_64-linux-gnu/libcrypto.so.3` | `7be3a37c9d754ec214b30db1d00ce329d22ccebd5654dd7c3f92010a7b1ccf07` / 4455728 | `7cc817ff1841b59516d684f357bc0c3fc2cc52c3fa9b4ffb8ce8bdc215f02915` / 4455728 |

`runtime_dependency_errors()` rejects both differences, as designed. This is a fail-closed current-host dependency mismatch, not evidence that the discovery or containment checks themselves are defective. The frozen dependency file participates in the OMP profile and run identity. Updating it would create a different exact profile and invalidate the existing exact-profile binding; it would require renewed exact-profile evidence. No dependency hash, profile, D3 boundary, or production code was changed to bypass the gate. No fresh provider credential was requested or used.

The only executable/test-file change is `qualification/ssdp70/eval/test_omp_integration.py`: the test-only replacement of guard-bypassing hostile cases with pre-launch refusal cases. This closure record is the requested evidence update. No production-source defect was found or repaired. Historical evidence from tests that deliberately bypassed the discovery guard is not used here as proof of source-specific pre-launch refusal. The retained successful positive probe remains unmodified; its internal identity discrepancy is recorded above.

## Unavailable checks and remaining risk

- Exact-profile assembled hostile discovery/containment matrix and runtime-created-entry integrity are **UNRESOLVED** on this host because the runtime dependency gate prevents launch.
- Focused and complete affected test suites are not green. The canonical frozen dependency manifest must be made available in a compatible execution environment, or any proposed profile change must be independently governed and requalified; this record does neither.
- The retained positive probe's actual internal run identity differs from the supplied identity. Its internal evidence is integrity-consistent, but that discrepancy remains for independent reconciliation.
- No fresh independent Stage 7 runner-admission review occurred. OMP is **not admitted**, and no Protocol 7 qualification subject was run.

## Stage 6 closure decision

**BLOCKED.** The positive probe supplies substantial exact-profile live evidence, but the required assembled negative controls and affected test acceptance did not close on the current host. The supplied run-identity discrepancy also remains unresolved. Do not admit OMP or run qualification subjects on this basis. Because Stage 6 is not closed, this record does not issue the conditional handoff for a fresh Stage 7 runner-admission reviewer.
