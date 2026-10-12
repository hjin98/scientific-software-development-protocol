# OMP-only Stage F — Stage 6 repair and recheck evidence

- **Date:** 2026-09-30 (America/Chicago)
- **Governing SSDP:** 6.6.0
- **Branch:** `ssdp-7.0-scientific-epistemic-closure`
- **Verified starting head:** `3804a2edd8bc96b70826de662f80fba57764777d`
- **Exact implementation and acceptance head:** `d03216d76d8860f42dc2ccc598e3c8d49d36203e`
- **Immutable Protocol 7 semantic candidate:** `db94a2dfb7fef480f37227eab5c45256e89901b8`
- **Disposition:** **Implementation and exact-head offline/stand-in acceptance PASS. Fresh real-provider probe is `COMPLETE_ADMISSIBLE` with `NOT_EVALUATED` qualification outcome. OMP remains UNADMITTED pending the independent Stage 7 runner-admission review.**

The implementation head above is the candidate on which all executable changes and the complete affected suite were frozen. This record is committed as an evidence-only descendant; no executable bytes changed after that acceptance head. The last commit before this candidate added a concurrent observer-launch regression only; profile-bound production/support bytes stayed unchanged. The historical Stage 6 blocked record remains unchanged.

## Authority and scope

The repair was checked against repository `AGENTS.md`, the active consolidated SSDP 7.0 workplan and its D4 Stage 6 closeout amendment after `ac251e75d7ba8161b6c1ac088371e1900dafbade`, Protocol 7 evaluation contract §1 items 1–11 and §6, the historical Stage F Stage 6 record, and the current OMP implementation. The accepted qualification-supervisor / provider-control-observer / subject-executor topology and shared supervisor-owned mediator remain unchanged. No D3 Serious Challenge was found or raised.

The work closes the two specified D4 implementation defects: destructive run-output reuse and dependence on mutable host runtime-library bytes. A changed closure and changed profile-bound support bytes require a fresh execution-profile identity. Historical live evidence is not reused for this profile. Independent Stage 7 runner admission and Protocol 7 qualification-subject runs were not performed and are not authorized by this record.

## Repairs implemented

1. `harness70.run_episode` now creates a previously nonexistent realization directory atomically before its first output write and raises an explicit realization-collision error if the caller selects an existing path. It no longer removes prior output. Logical `run-identity.json` semantics are unchanged. The OMP rig and the V4 replay caller choose distinct output locations for repeated logical runs.
2. The exact OMP subject/observer runtime is reconstructed from a qualification-owned content-addressed archive, not live host library paths. Production verifies the manifest pin and archive contents before realization, materializes only declared files/symlinks into fresh subject and observer roots, then re-verifies staged contents before launch. Existing exact dependency checks remain before ambient-discovery checks.
3. Profile identity binds the new closure/manifest and changed adapter, core, harness, capability and principal/support bytes. The fresh profile below does not inherit applicability from the prior profile or its live evidence.
4. Hostile project, HOME and credential discovery execute through the production containment/launch path. The assembled cases assert refusal before OMP/provider activity when the discovery guard owns the refusal.

No files in `source/` or `dist/` changed. Protocol 7 semantics, qualification thresholds, fixtures, scoring semantics, custody rules, and the accepted three-principal topology were not changed.

## Exact runtime and execution-profile identities

The closure was built from the current trusted runtime artifacts because the historical host OpenSSL bytes were unavailable. It is a new exact profile, not a relabeling of the old profile.

| Identity | Value |
| --- | --- |
| OMP executable | `omp/18.0.11`, build `2c2e51f3b6fae6722da4f7b69751a2e9467ab063` |
| Executable SHA-256 / bytes | `6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26` / `194573512` |
| Immutable closure artifact | `/home/samjin/ssdp70-omp-stagef/runtime-closures/omp-runtime-18.0.11-sha256-143e32dfed72332af7976f0588591d3ddf1661cb24cad6f47794cc1fd6715a56.tar.gz` |
| Artifact SHA-256 / bytes / mode | `143e32dfed72332af7976f0588591d3ddf1661cb24cad6f47794cc1fd6715a56` / `144271269` / `0444` |
| Closure identity SHA-256 | `6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499` |
| Runtime manifest SHA-256 | `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216` |
| Declared manifest entries | 1,531 |
| Subject tree | 1,521 entries; `f32f15656223d8b445b13674a898dadd44879339b5c57ae40e69d471813d9711` |
| Observer tree | 1,522 entries; `689c2934b6022b81cc9702e88a2912971d0fc9eec63914dc5795a830f398dc29` |
| Fresh profile ID | `omp-headless-deepinfra-glm53-flash-stage6-repair-20261001T000313%NZ-c0cce5a575a9` |
| Fresh profile-key SHA-256 | `86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10` |
| Profile document SHA-256 | `29c7578d39a8441f34309643f75aa91241047f7d226b2ecca948dab046aacac8` |
| Capability content identity / file SHA-256 | `f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55` / `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd` |
| Profile preflight artifact | `/home/samjin/ssdp70-omp-stagef/probes/profile-preflights/20261001T000313%NZ-c0cce5a575a9` |

The profile preserves the previously approved probe configuration: DeepInfra `zai-org/GLM-5.3-Flash`, `openai-completions`, `https://api.deepinfra.com/v1/openai`, reasoning enabled with `--thinking high`, 30 turns and a 900-second budget. The only credential binding is the approved environment-variable **name**; no credential value was present in or written by the preflight.

The profile preflight was generated on `c0cce5a575a9df9e806b7087888e14fd62d7ad18`. The subsequent `d03216d…` change added only acceptance-test coverage in `test_omp_integration.py`, outside the profile-key inputs; the profile-bound production/support digests and key remained unchanged, and the post-suite attempt on `d03216d…` used that same exact profile key.

The literal `%NZ` characters in the profile ID and preflight directory name are part of their exact recorded identities, not an unresolved timestamp placeholder.

### Profile-bound support digests

| File | SHA-256 |
| --- | --- |
| `qualification/ssdp70/eval/adapters/omp.py` | `588c8390fdcc2e568058394cd47765cb267839da50c9f0287f4954a6b2b77ad7` |
| `qualification/ssdp70/eval/core70.py` | `13a9455bf7ddeb3147c2aaf067db89773b4687f2bf805bb8ce4d0948b7d6e7e2` |
| `qualification/ssdp70/eval/harness70.py` | `73b439a670bccfc56897cc9a88d593356b22a47baa3e84ab89345e7a0e5bbbc5` |
| `qualification/ssdp70/eval/profiles/omp-headless.template.json` | `62881b137a6269db386077120ce165496cf003a5a1c65a042103950e8f6b90a0` |
| `qualification/ssdp70/eval/capabilities/omp-headless.json` (file bytes) | `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd` |
| `qualification/ssdp70/eval/omp-build-inventory-18.0.11.json` | `7d0deedbf8d4bd9d53818535f57774ef6e8e41f406c7944dc85ac2d86cb12914` |
| `qualification/ssdp70/eval/observer70.py` | `13dbb679cda7ed5c24fd11fb2f092e9db3bbc49495093c0744894b29629bd2ff` |
| `qualification/ssdp70/eval/observer_exec_helper70.py` | `8891d415d3d0c10bea887caabdfda6bb9f510523f5a1e54eda4d45165a270972` |
| `qualification/ssdp70/eval/mcp_bridge70.py` | `cbb6f6b615de153ab4e814b7adbdc237702c35c1620457a603c7dfb52f501ff3` |
| `qualification/ssdp70/eval/muxhttp70.py` | `9db135ba2048092678b1983ba578152205cb0e5d8c51fa903a2d33996582e012` |
| `qualification/ssdp70/eval/evidence70.py` | `9ab473c56855d5d1e5ebcd7e77cbb1bcc7a25eedfb9030f4c45b485fc6ed7ed3` |
| `qualification/ssdp70/eval/seccomp70.py` | `c81bef42fd310f30c177681cd7b9592158a16f4f164a22fa427804224fa617f9` |
| `qualification/ssdp70/eval/subject_launcher.py` | `42b3438182b50741329c6c2c97b18be2d4b9ac9aca50733f69429b7b441fccf5` |
| `qualification/ssdp70/eval/stub_tools/mediator.py` | `e51f0641907215c9d5a0acb607f967363fc7491fa572a70cfb8701acd2308c2e` |
| `qualification/ssdp70/eval/omp-runtime-dependencies-18.0.11.json` | `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216` |

The capability content identity is also embedded in the profile key; its file-byte digest is shown separately. The exact profile and its detailed key/support digests are retained in the external profile-preflight artifact.

## Exact-head executable acceptance

The following command ran on exact implementation head `d03216d76d8860f42dc2ccc598e3c8d49d36203e` after all executable edits:

```text
python3 -W ignore -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -q
Ran 248 tests in 1174.537s
OK
```

No `skipped=` result was emitted: **248 executed, zero skips, zero failures, zero errors**. The retained log is `/home/samjin/ssdp70-omp-stagef/logs/acceptance-20261001T001122.609076648Z-d03216d76d8860f4.log`. It covers all eight discovered test modules: `test_control_path_policy.py`, `test_harness_integration.py`, `test_mcp_stdio.py`, `test_omp_integration.py`, `test_omp_units.py`, `test_portable70.py`, `test_stage_f_integrity_repairs.py`, and `test_stage_f_v4_repairs.py`.

| Acceptance area | Executed coverage | Result |
| --- | --- | --- |
| Portable, Claude, MCP and Stage-F regressions | All discovered portable/control-path/MCP/Stage-F test modules listed above | PASS |
| Append-only evidence lifecycle | `test_completed_realization_collision_is_byte_and_metadata_preserving`; `test_interrupted_partial_realization_collision_is_byte_and_metadata_preserving`; `test_terminal_integrity_artifacts_survive_realization_collision` | PASS; prior bytes and metadata preserved |
| Runtime closure identity, provenance and changed-profile binding | `test_content_addressed_runtime_closure_identity_and_surface_match`; `test_manifest_dependency_drift_fails_closed`; `test_changed_closure_artifact_bytes_fail_before_archive_read`; `test_exact_profile_key_binds_runtime_closure_and_executable_support` | PASS |
| Staged-runtime verification and omitted host software | `test_staged_runtime_tampering_fails_before_subject_or_provider_execution`; `test_minimal_runtime_keeps_required_tools_and_omits_host_software` | PASS |
| Hostile project, HOME and credential discovery | Unit baseline refusals and assembled `test_every_project_discovery_source_is_refused_before_omp_or_provider`, `test_every_home_discovery_source_is_refused_before_omp_or_provider`, `test_every_credential_environment_name_is_refused_before_omp_or_provider` | PASS through production containment/launch; no subject/provider execution on owned refusals |
| Observer privilege boundary and handoff | Seccomp filesystem/process/network filters; `test_inference_and_mcp_work_while_credential_home_and_state_are_denied`; active-thread FD remapping and post-lockdown handoff probes | PASS |
| Local IPC and relay discrimination | `test_discriminating_external_local_ipc_sentinel_is_unreachable`; `test_bash_cannot_use_the_inference_or_mcp_transport_or_launch_a_second_omp` | PASS |
| Observer launch safety | `test_real_observer_fd_map_excludes_inheritable_supervisor_sentinel`; `test_repeated_launches_with_active_threads_have_an_outer_watchdog`; `test_concurrent_observer_launches_with_active_threads_have_an_outer_watchdog` | PASS; three repeated launches and two concurrent launches under active unrelated threads |
| TLS and provider catalog/model discovery | `test_tls_handshake_uses_explicit_staged_ca_bundle`; `test_observer_ca_path_is_the_bundle_staged_by_the_adapter`; `test_exact_omp_model_catalog_probe_is_blocked_without_provider_egress` | PASS |
| Native tool surface, MCP identity, root selection and consumed resources | `test_native_tool_surface_is_exactly_restricted_and_contamination_is_detected`; runtime-derived catalog checks; root-selection and resource-consumption tests | PASS |
| Mediator normalization and ordering | `test_all_six_mediator_operations_normalize_losslessly_with_version_binding`; parallel OMP tool-result bijection/order tests | PASS |
| Truncation, unmatched events and evidence integrity | Incomplete/reordered/duplicated/truncated native-event cases, response truncation, evidence-chain mutation checks, and harness integrity tests | PASS |

The three focused regressions that failed in the preceding full-suite attempt were rerun after their caller/assertion fixes: **3 tests, 53.372s, OK**. The new concurrent-launch stress regression also passed alone (**1 test, 16.045s, OK**) before commit, then ran in the exact full suite above. The `git diff --check` check is repeated after this record is added.

## Fresh external OMP probe executions

### Preserved no-credential attempts

Two earlier fresh attempts used the same exact profile and production `realize_containment -> launch` path but had no provider credential in the command environment. They remain unchanged at:

- `/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T000617696764Z-c0cce5a575a9df9e/`
- `/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T003151211608Z-d03216d76d8860f4/`

Both independently retain canonical logical run identity `6af45ec8db956e3a24981aaf24cb3befcc7053c0eda85077bdc4d6b7918b028c`. Each correctly refused before subject launch because `SSDP70_OMP_PROVIDER_CREDENTIAL` was unavailable; neither is provider evidence.

### Preserved credentialed attempt with an incompatible probe manifest

After the approved `SSDP70_DEEPINFRA_API` environment variable became available, a fresh attempt reached the subject and provider. Its separate append-only realization is `/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005440470282Z-d03216d76d8860f4-cce1b4a01771/`. It returned `execution_ok=true` and process return code 0, but the external probe input manifest incorrectly required `prelaunch-refusal.json` even on the successful-launch path. The actual semantic result was retained as `evidence_state=MISSING_REQUIRED_EVIDENCE`, `qualification_outcome=NOT_EVALUATED`, with missing artifact `prelaunch-refusal.json`; it was not relabeled or repaired in place. Its integrity validation passed, and its exact credential-value scan found no match in the realization.

That manifest was a non-qualification probe input, not the frozen Protocol 7 qualification contract, fixture set, thresholds or scoring semantics. The successful probe below uses a distinct fresh realization and a positive-path probe artifact manifest bound into that run's inputs and logical run identity. The incomplete realization above remains available as historical evidence of the first credentialed attempt.

### Fresh completed real-provider probe

The completed non-qualification probe used the exact repaired profile and production harness, containment and launch path. Its unique external realization is:

`/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T005750650447Z-d03216d76d8860f4-5ea83cffdd46/`

The canonical run directory is `out/E1-p70-r0/`. It retains the run identity, profile and capability snapshots, requirements snapshot, integrity manifest, native and normalized events, complete normalization map, OMP trace, provider-control/observer transcript, mediator bridge transcript, launcher and containment attestations, runtime closure evidence, consumed package/root evidence, and terminal summary. The exact profile preflight snapshot is retained in `profile-preflight/`; the external runner summary and log contain no credential value.

| Probe evidence | Result |
| --- | --- |
| Protocol 7 semantic candidate / package digest | `db94a2dfb7fef480f37227eab5c45256e89901b8` / `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b` |
| Exact profile ID / key SHA-256 | `omp-headless-deepinfra-glm53-flash-stage6-repair-20261001T000313%NZ-c0cce5a575a9` / `86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10` |
| Profile document SHA-256 | `29c7578d39a8441f34309643f75aa91241047f7d226b2ecca948dab046aacac8` |
| Runtime closure / manifest SHA-256 | `6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499` / `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216` |
| Canonical run identity SHA-256 | `509d8459969962f9fc793c6aecd717894408b3ee1a4e7feb4db4f6bc4f362e1f` |
| Independent identity recomputation | PASS; recomputed value equals `run-identity.json` |
| Probe artifact-manifest SHA-256 | `e5c8769ee07c0aa10e79758da135275ce56ce355dc5c5c9440b30afb51fec9ed` |
| Integrity manifest SHA-256 / validation | `b47c06708ce11a7ae2b08abfddf0d571eb453a229a2386883de594df71d12d27`; PASS, no validation errors |
| Runtime/profile execution | OMP 18.0.11, build `2c2e51f3b6fae6722da4f7b69751a2e9467ab063`; DeepInfra `zai-org/GLM-5.3-Flash`; high reasoning |
| Provider and mediator observations | 3 provider requests and 3 responses; credential receipt after observer lockdown; 3 mediator requests and 3 responses |
| Normalized/native evidence | 11 normalized events; 145 native events; catalog snapshot, root selection and six resource-access events retained |
| Credential-value scan | PASS; no credential value found in any file under the realization |
| Actual semantic terminal state | `execution_mode=probe`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED` |
| Probe log | `/home/samjin/ssdp70-omp-stagef/logs/omp-live-20261001T005750650447Z-d03216d76d8860f4.log` |

The changed probe artifact manifest is included in the completed run's requirements digest and explains why its logical run identity differs from the earlier prelaunch attempts. The profile key and profile-bound production/support digests are unchanged. No credential value was written to profile/configuration files, logs, observer evidence, normalized evidence, runner summaries or run summaries.

## Evidence applicability and historical identity discrepancy

The new closure, manifest, adapter, harness and support bytes define a new exact execution profile. Prior live probe artifacts, including the retained `6fe36d822c54c5dd5b0b8921937bdc32227e67b59ddfeacc4810d68757b34fdc` realization, do not apply to this changed profile and were not copied forward as evidence. The operator-observed historical terminal identity `c88938172de9ab888692e42f7fafca4653a5cf4c289cb4ed3a6ab3a32adaaa95` is also preserved unchanged.

The `6af45ec8…` identity is from a prelaunch-refused run; the successful `509d8459…` identity comes from a new non-qualification probe input manifest. Neither establishes a causal link to the earlier `6fe36d…` versus `c889…` discrepancy. No causal reproduction was established. The prior destructive-output behavior was a plausible lifecycle weakness; the new collision tests prove that collisions now fail closed, but that fact alone does not prove the cause of the historical identity discrepancy. **Historical discrepancy disposition: unresolved.**

The local stand-in suite establishes the listed offline and assembled control behavior for the exact implementation bytes; the completed probe separately establishes the retained real-provider interaction for this exact profile. Neither establishes Stage 7 admission. No §1 items 1–11 or §6 runner-admission PASS is declared, and no Protocol 7 qualification-subject execution occurred. The implementation-side Stage 6 repair evidence is complete. The remaining gate is the fresh independent Stage 7 runner-admission recheck against the exact candidate and profile; the historical identity discrepancy remains explicitly unresolved for that review. OMP remains **UNADMITTED**.
