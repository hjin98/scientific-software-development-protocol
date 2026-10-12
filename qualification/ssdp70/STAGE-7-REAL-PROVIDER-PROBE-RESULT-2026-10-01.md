# SSDP 7.0 OMP Stage 7 — host-bound profile and real-provider probe result

- **Record date:** 2026-10-01
- **Governing SSDP:** 6.6.0
- **Record type:** implementer-produced evidence handoff; not an independent admission decision
- **Disposition:** replacement profile and one fresh probe completed; Stage 7 runner remains **UNADMITTED**

## Scope and candidate identity

This record captures the requested target-host profile freeze and fresh real-provider probe. It is a result summary for designer evaluation, not normative authority, independent review, a Stage 7 admission campaign result, or Protocol 7 qualification.

- Repository: `hjin98/scientific-software-development-protocol`
- Branch: `ssdp-7.0-scientific-epistemic-closure`
- Candidate head: `d605ff2e9448990e3ac75755fa4cee96c443a2c3`
- Immutable Protocol 7 semantic subject: `db94a2dfb7fef480f37227eab5c45256e89901b8`
- Repository worktree was clean at candidate creation; this report is the sole worktree addition, and no source files were edited.
- The campaign remains `CANDIDATE_EVIDENCE`. No `status=ADMITTED` record was created.

Per the operator's report, the focused Stage 7 tests and complete affected `qualification/ssdp70/eval/test_*.py` suite passed on this target host after the fixture repair. They were not rerun while preparing this record.

## Frozen campaign and profile

Campaign directory:

`/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261001T135855Z-e0d62ddad00e-hostbound/`

| Identity | Value |
|---|---|
| Candidate campaign state | `CANDIDATE_EVIDENCE` |
| Replacement profile ID | `omp-headless-deepinfra-glm53-flash-stage7-hostbound-d605ff2e9448990e3ac75755fa4cee96c443a2c3` |
| Replacement profile-key SHA-256 | `e0d62ddad00e15bdf19c66def518a1ace96f95ab8fb36b7c3198c579e4c7c4f4` |
| Profile document SHA-256 | `50d3bd68ee06e9a6549adcc153e1ed9bb13e43851cadd80eadd45714b3d08344` |
| Capability snapshot SHA-256 | `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd` |
| Capability identity bound into the profile key | `f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55` |
| Runtime-closure identity | `6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499` |
| Runtime-dependency manifest SHA-256 | `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216` |

The new profile key differs from the historical route-source key `86da2241272919344cd40075bcf79e61c63dbd3eb27249c8bd2f729fcca89a10`. The historical profile and probe supplied route configuration only; they are not evidence for this replacement host-bound profile.

Frozen `host_execution_environment`:

```json
{"kernel":{"machine":"x86_64","release":"6.8.0-138-generic","sysname":"Linux","version":"#138~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug  7 13:43:15 UTC "},"os_release":{"id":"ubuntu","sha256":"594d5ddd35aedb47f00d9c34d140017907a5b9f93c975aba125fc924daac5c07","version_id":"22.04"},"schema":1,"supervisor_python":{"executable_sha256":"a2f33a6e006989270f4340528eb61f8f97366e00a5d1b602ac8672ea44fc56ae","implementation":"CPython","version":"3.10.12"}}
```

Frozen and observed provider route:

- Provider: `deepinfra`
- Model: `zai-org/GLM-5.3-Flash`
- Upstream: `https://api.deepinfra.com/v1/openai`
- Reasoning configuration: `{"source":"--thinking","thinking":"high"}`
- OMP executable: `/opt/omp/omp`, version `18.0.11`, build ID `2c2e51f3b6fae6722da4f7b69751a2e9467ab063`, SHA-256 `6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26`
- Bubblewrap substrate: `/usr/bin/bwrap`, version `0.6.1`, SHA-256 `bf6cf3d4456665f5d80c14eb79a76e0ce87b39a0883e614a161658b4ec33492c`

Profile-bound adapter/support identities include:

| Component | SHA-256 |
|---|---|
| `adapters/omp.py` | `5881ca8929cc929b5a1a270a4988f7c139ca4659eb9c1027068a27cf66aae5b4` |
| `core70.py` | `13a9455bf7ddeb3147c2aaf067db89773b4687f2bf805bb8ce4d0948b7d6e7e2` |
| `harness70.py` | `63082ca276f5f62e32db62c75252952d7201efe321894d61cabf8601a3c1da8f` |
| `profiles/omp-headless.template.json` | `cc57855c0b03928da9d4babf30141a9c3c729d879feaad690b4458aa44d266eb` |
| `evidence70.py` | `9ab473c56855d5d1e5ebcd7e77cbb1bcc7a25eedfb9030f4c45b485fc6ed7ed3` |
| `mcp_bridge70.py` | `cbb6f6b615de153ab4e814b7adbdc237702c35c1620457a603c7dfb52f501ff3` |
| `muxhttp70.py` | `9db135ba2048092678b1983ba578152205cb0e5d8c51fa903a2d33996582e012` |
| `observer70.py` | `13dbb679cda7ed5c24fd11fb2f092e9db3bbc49495093c0744894b29629bd2ff` |
| `observer_exec_helper70.py` | `8891d415d3d0c10bea887caabdfda6bb9f510523f5a1e54eda4d45165a270972` |
| `seccomp70.py` | `c81bef42fd310f30c177681cd7b9592158a16f4f164a22fa427804224fa617f9` |
| `stub_tools/mediator.py` | `e51f0641907215c9d5a0acb607f967363fc7491fa572a70cfb8701acd2308c2e` |
| `subject_launcher.py` | `42b3438182b50741329c6c2c97b18be2d4b9ac9aca50733f69429b7b441fccf5` |

## Fresh probe realization

Unique probe root:

`/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T140827Z-d605ff2e9448990e-e0d62ddad00e-4da244ff3406/`

Run evidence directory:

`/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T140827Z-d605ff2e9448990e-e0d62ddad00e-4da244ff3406/out/E1-p70-r0/E1-p70-r0/`

| Probe result | Value |
|---|---|
| `execution_mode` | `probe` |
| `evidence_state` | `COMPLETE_ADMISSIBLE` |
| `qualification_outcome` | `NOT_EVALUATED` |
| Execution | `execution_ok=true` |
| Native / normalized events | 554 / 27 |
| Run-identity SHA-256 | `870da5598e5823fb3a211078a6db13645f5c6618842f53a98da9e0b7a832a527` |
| Evidence-integrity manifest SHA-256 | `d4c29c294391b8f2425a2d6f0e09cf7e5fb2e1d947594259bba7631bc32af6aa` |
| Evidence-integrity validation | Passed; 33 files covered |
| Runtime-dependency errors before / after launch | None |
| Credential leakage scan | Passed |

The current harness recomputed the run identity and it matched the retained value. Current complete-run and evidence-integrity validation returned no errors. The retained profile and capability snapshots match the frozen documents; the host identity in containment matches the frozen host identity; and the runtime-closure identity and dependency-manifest digest match the replacement profile.

The integrity-bound run retains the exact Protocol 7 semantic subject and package digest `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`, catalog/root/package consumption, native trace, normalized trace, raw-to-normalized map, mediator and provider observations, containment realization, runtime-dependency manifest and attestation, terminal summary, and integrity manifest. The trace records eight `POST /chat/completions` requests and eight HTTP 200 responses; the request observations identify the frozen model and `reasoning_effort=high`.

Key retained files include `run-identity.json`, `summary.json`, `evidence-integrity.json`, `profile-snapshot.json`, `capability-manifest-snapshot.json`, `trace.jsonl`, `events.normalized.jsonl`, `normalization-map.json`, `containment-realization.json`, and `adapter-artifacts/runtime-dependency-attestation.json` under the run evidence directory above. The raw SHA-256 of `summary.json` is `9ab8166cd7c3cb78accdff5a13786654b2266b988ea329df59d11ce21224f93b`.

The credential value was not included in this record or retained evidence. Scanning the successful probe root for the raw value and checked encoded forms found no occurrence.

A separate fresh realization at `/home/samjin/ssdp70-omp-stagef/probes/OMP-LIVE-20261001T140521Z-d605ff2e9448990e-e0d62ddad00e-f83d78c0936c/` stopped before a provider request because the default sandbox could not resolve DNS. It remains preserved as produced. It was not reused or overwritten; the successful probe used the distinct realization above.

## Remaining Stage 7 work

This record closes only the replacement-profile freeze and fresh-probe prerequisite. It does not close the exact-profile admission campaign. The campaign must still produce and retain its required executor-check and §6 evidence, including the independent semantic/evaluator proof obligations. No `prepare-arms`, `run-exact` matrix, deterministic falsification, independent proof recording, admission finalization, qualification-mode dry run, or blinded Protocol 7 qualification was run in this task.

The next designer/reviewer evaluation should inspect the current Stage 7 campaign and admission owners at candidate head against the active Protocol 7 workplan and qualification contract. The fresh real-provider probe is candidate evidence for the frozen profile; it is not a substitute for the exact-profile campaign, independent review, or admission. **OMP remains UNADMITTED.**

Relevant repository authority and working-state routes at the candidate head:

- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`
- `qualification/ssdp70/STAGE-7-OMP-RUNNER-ADMISSION-REPAIR-WORKING-STATE-2026-09-30.md`
- `qualification/ssdp70/eval/omp_stage7_campaign.py`
- `qualification/ssdp70/eval/omp_stage7_admission.py`
