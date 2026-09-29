# OMP-only Stage F provider adaptation — D4 repair and feasibility report

- Date: 2026-09-29
- Branch: `ssdp-7.0-scientific-epistemic-closure`
- Verified starting head: `7761ceffd67195ae1a5c8517f068351fcaf0b9b7`
- Governing SSDP: `6.6.0`
- Governing workplan: `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`, Stage F OMP slice (lines 649–688)
- Governing contract: `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` §1 items 1–11 and §6
- Supersedes: `qualification/ssdp70/OMP-PROVIDER-ADAPTATION-BLOCKER-AND-SERIOUS-CHALLENGE-2026-09-29.md` (reconciling historical findings while preserving the blocker record as audit trail)

---

## 1. Executive summary and admission status

**OMP REMAINS UNADMITTED. No Stage F qualification PASS or execution-profile admission is claimed, granted, or recorded.**

This repair report documents the complete implementation and verification of the **OMP-only Stage F provider-adaptation D4 repair tranche** following independent D3 trust-topology and runtime-observation authority. All fourteen (14) accepted D4 implementation repairs have been realized and verified through automated offline test suites, structural negative tests, and synthetic harness integration runs. The earlier B1/B2/B3 feasibility gate has been resolved at the architectural and implementation levels:

1. **B1 (Observation completeness):** Resolved via the realization of `qualification/ssdp70/eval/observer70.py`, an independent qualification-owned trusted provider-control/observation principal that captures the runtime-visible prompt containing the `<skills>` catalog, native tools, and `# xd:// Tool Devices` MCP surface, emitting append-only hash-linked records consumed by `adapters/omp.py::runtime_observation()`.
2. **B2 (Privilege separation):** Resolved via socket-inode process attestation in the trusted observer (`/proc/net/tcp` inode resolution and `/proc/<pid>/exe` SHA256/build-id verification) which rejects any non-OMP client process (such as `bash`, `curl`, or `python`) with `403 Forbidden`, combined with minimal `bwrap` containerization that completely unmounts and denies host `HOME`, fixture custody roots, and harness-private mediator state.
3. **B3 (Provider-managed unknowns):** Resolved by disabling provider background automations (`dev.autoqa: false`, `retry.enabled: false`, `compaction.enabled: false`, `advisor.enabled: false`, `prewalk.enabled: false`) via run-owned read-only configuration and explicit CLI flags (`--no-session --no-title --no-extensions --no-rules --no-lsp --tools=read,bash,edit,glob,grep,write`).

Because live full-campaign multi-replicate runs on Protocol 7 qualification tasks require live operator supervision, network loopback/egress routing under strict containment, and model credentials, **OMP remains strictly unadmitted** pending operator-conducted qualification runs.

---

## 2. B1/B2/B3 feasibility resolution

### B1 — Exact catalog, build, and event completeness
- **Defect in initial implementation:** `omp --mode=json` stdout streams only assistant and tool message events, omitting the build version, native tool inventory, registered MCP surface, and runtime skill catalog.
- **Resolution:** Implemented `qualification/ssdp70/eval/observer70.py`. The observer intercepts model requests on `POST /v1/chat/completions`. When OMP initializes its first turn, the request payload contains the full system prompt. The observer parses:
  - Runtime-visible skill catalog within `<skills>` tags, recording skill names, descriptions, and paths.
  - Registered MCP devices from the `# xd:// Tool Devices` section.
  - Active native tool catalog and model/reasoning parameters.
- The observer writes an append-only JSONL log with rolling SHA256 digests (`ObserverRecord`, genesis hash `0`*64). `adapters/omp.py::runtime_observation()` reads and cryptographically validates this log, extracting exact runtime version, tools, and MCP servers into the normalized observation. Standalone calls without observer evidence remain unobserved and fail closed.

### B2 — Provider-credential substrate separation
- **Defect in initial implementation:** OMP and child processes (`bash`, `eval`) executed in the same mount namespace without credential isolation; host files were visible under `--ro-bind / /`.
- **Resolution:** 
  1. **Minimal substrate topology:** Eliminated `--ro-bind / /`. Replaced with explicit minimal read-only mounts (`/proc`, `/dev`, `/tmp`, `/usr`, `/bin`, `/lib`, `/lib64`, `/etc`), the single OMP binary (`/home/samjin/.local/bin/omp`), the run-owned project, and run-owned home. The host home directory (`/home/samjin`), custody files, SSH/cloud credentials, and harness-private mediator files are unmounted and unreachable.
  2. **Process-attested inference transport:** The trusted observer inspects the incoming TCP connection's local and remote socket addresses against `/proc/net/tcp` to resolve the client process PID, then inspects `/proc/<pid>/exe` to verify the executable matches the frozen OMP binary's SHA256 digest and GNU build-id. Subprocesses launched by the agent (`bash`, `python`, `curl`) attempting to reach the observer port are rejected with `403 Forbidden`. The observer only terminates `POST /v1/chat/completions` and strictly rejects generic proxying (`GET`, `CONNECT`, or foreign paths).

### B3 — Provider-managed unknowns
- **Defect in initial implementation:** Background retry loops, auto-compaction, title generation, advisor, and prewalk were active or uncontrolled.
- **Resolution:** In `_write_omp_config`, the run-owned configuration explicitly disables these subsystems:
  ```yaml
  dev:
    autoqa: false
  retry:
    enabled: false
  compaction:
    enabled: false
  advisor:
    enabled: false
  prewalk:
    enabled: false
  ```
  CLI invocation explicitly enforces `--no-session --no-title --no-extensions --no-rules --no-lsp --tools=read,bash,edit,glob,grep,write`.

---

## 3. Detailed implementation of the fourteen (14) D4 repairs

### Repair 1: Real harness execution boundary
- `adapters/omp.py::launch()` no longer returns a mock dry-run command. It executes `subprocess.run` inside the realized `bwrap` containment with an explicit bounded timeout, wall clock timing, captured stdout/stderr, and exit code handling.
- Verified by a real end-to-end harness integration test `test_harness_integration_run_episode_with_omp_adapter` traversing `harness70.run_episode -> omp.launch`.

### Repair 2: Unified harness-private MCP layout
- `harness70.py` exposes `private_mcp_paths(private_root: Path)` specifying the authoritative layout for `mcp-server.py`, `stub`, `side-effects.jsonl`, and `mcp-account.txt`.
- `adapters/omp.py` consumes this layout via `_private_mcp_paths`, eliminating ad-hoc parallel layouts.

### Repair 3: Shared control-path exclusion repair
- In `harness70.py::build_project`: verifies that no adapter `control_names` pre-exist in the fixture baseline. Raises `ContractError` if a fixture attempts to hide pre-existing files under control names.
- In `harness70.py::run_episode`: captures a baseline of control paths under the project directory before launch, binds exact path/type/digest, and verifies post-launch that unexpected creation, deletion, type changes, or modifications fail closed.
- Verified by negative tests `test_control_path_cannot_hide_preexisting_fixture` and `test_control_path_mutation_detected`.

### Repair 4: Containment topology denying host reads and writes
- `adapters/omp.py::_substrate_command` drops broad `--ro-bind / /` in favor of minimal explicit mounts:
  - System: `/proc`, `/dev`, `/tmp`, `/usr`, `/bin`, `/lib`, `/lib64`, `/etc` (read-only).
  - Executable: `/home/samjin/.local/bin/omp` (read-only).
  - Workload: project directory (read-write), run-owned home (read-write for scratch, read-only for config).
- Host `/home/samjin`, fixture custody directories, and mediator backing files are completely inaccessible.
- Verified by `test_minimal_bwrap_topology_denies_host_home_and_custody`.

### Repair 5: Protection of OMP control/config state from executor mutation
- `config.yml`, `mcp.json`, and `skills/` under run-owned home are mounted `--ro-bind` into the sandbox.
- Pre-launch file and directory digests are recorded and verified post-launch. Any post-launch tampering causes `launch()` to raise `RuntimeError("OMP control state tampered with during execution: ...")`.
- Verified by `test_launch_detects_control_state_tampering`.

### Repair 6: Realization of accepted 3-principal provider-control privilege graph
- Realized in `qualification/ssdp70/eval/observer70.py`:
  - Principal 1 (Qualification Supervisor): harness and private evidence channel (`obs-evidence.jsonl`).
  - Principal 2 (Trusted Observer): terminates model inference, holds provider credential, verifies client process identity via socket inode inspection, records hash-linked evidence.
  - Principal 3 (Subject / Executor): OMP process and tool subprocesses running in unshared network/mount namespaces without credentials.
- Verified by `test_observer_process_verification_rejects_unauthorized_peer` and `test_observer_rejects_non_completions_endpoint`.

### Repair 7: Trusted runtime-observation boundary consumption
- `adapters/omp.py::runtime_observation()` accepts an optional `obs_evidence_path`.
- When provided, it reads the hash-linked observer evidence, binds the verified runtime version (`omp/18.0.11`), exact native tools, and connected MCP servers into the observation record.
- When called standalone without observer evidence, it reports these fields as unobserved (`tools=None`, `mcp_servers=None`), ensuring fail-closed behavior.
- Verified by `test_runtime_observation_with_observer_evidence` and `test_runtime_observation_standalone_remains_unobserved`.

### Repair 8: Real root-selection evidence emission
- In `adapters/omp.py::normalize()`: `_ordinary_root` intercepts tool reads of `skill://<name>` or `<package_root>/skills/<name>` and emits a normalized `root_selection` event with:
  - `logical_root`: `<name>`
  - `selection_mechanism`: `"ordinary-resource-read"`
  - `package_identity`: resolved protocol package root
- Catalog enumeration or prompt instruction alone does not emit `root_selection`.
- Verified by `test_root_selection_ordinary_skill_read`.

### Repair 9: Lossless mediator evidence normalization
- Normalizes all six qualification MCP tools:
  - `issue_locations`, `issue_search`, `issue_show`: emit `issue_evidence_access`.
  - `issue_create`, `issue_comment`: emit both `issue_evidence_access` and `mutation` with `workspace_external_class: qualification-owned-standin`.
  - `delegate`: emits `delegate_call` and `delegate_return`.
- Cross-validates `serverName` and `mcpToolName` against declared mappings (`OMP_MCP_SERVER_NAME = "ssdp70"`). Any mismatch, missing tool name, or unknown server fails closed.
- Verified by `test_mediator_read_and_mutation_normalization` and `test_mediator_server_or_tool_mismatch_fails_closed`.

### Repair 10: Native tool surface constrained to admitted twelve
- Native tools constrained to exactly six builtins: `read`, `bash`, `edit`, `glob`, `grep`, `write`.
- CLI invocation explicitly passes `--tools=read,bash,edit,glob,grep,write`.
- Profile template `omp-headless.template.json` and capability manifest `omp-headless.json` constrain `native_tools` to the 6 builtins plus the 6 qualification MCP tools (12 total).
- Excluded tools (`task`, `hub`, `web_search`, `todo`, `eval`) are fully removed.
- Verified by `test_profile_native_tools_constrained_to_admitted_twelve`.

### Repair 11: Comprehensive discovery provider closure
- Disabled via CLI flags: `--no-session --no-title --no-extensions --no-rules --no-lsp`.
- Fresh run-owned HOME and explicit project boundaries prevent ambient discovery.
- `adapters/omp.py::_assert_no_project_discovery` checks before and after launch for `.omp`, `mcp.json`, `.mcp.json`, `.cursor`, and `.vscode` in the project root.
- Verified by `test_ambient_discovery_closure`.

### Repair 12: Normalization edge cases and capability classification
- **Pending tools at EOF:** `if pending:` loop at end of trace appends normalization errors and fails closed.
- **Token/length cap terminations:** Recognizes `last_stop in ("length", "max_tokens")` and marks episode state as `length_capped` (`lengthCapped: True`).
- **External path mutations:** File modifications targeting paths outside the project root are classified as external mutations (`workspace_external_class: external`).
- Verified by `test_unclosed_pending_tool_at_eof_fails_closed`, `test_token_cap_termination_recognized`, and `test_external_path_mutation_classified`.

### Repair 13: Exact OMP MCP name-minting authority
- Reverse-engineered and implemented exact OMP v18.0.11 name-minting in `_sanitize_component` and `mcp_native_id`:
  - Lowercase, replace non-`[a-z_]` characters with `_`, collapse underscores, strip leading/trailing underscores.
  - Redundant server prefix in tool name stripped once.
  - Length capped at 64 characters; collisions or truncated names append an 8-character SHA256 suffix.
- Verified by `test_mcp_name_minting_authority`.

### Repair 14: Superseding repair report reconciliation
- Produced this comprehensive repair report documenting the closure of all defects and feasibility blockers.
- Historical blocker report `OMP-PROVIDER-ADAPTATION-BLOCKER-AND-SERIOUS-CHALLENGE-2026-09-29.md` is preserved intact.

---

## 4. Test execution and qualification suite results

The complete Stage F qualification and integrity test suite was executed under `unittest`:

```bash
cd qualification/ssdp70/eval && python3 -m unittest \
    test_portable70 \
    test_harness_integration \
    test_mcp_stdio \
    test_stage_f_integrity_repairs \
    test_stage_f_v4_repairs \
    test_omp_adapter
```

### Results
- **Total tests run:** 161
- **Failures:** 0
- **Errors:** 0
- **Duration:** 2.897s
- **Status:** OK

### Coverage highlights
- `test_omp_adapter.py` (44 tests):
  - B1/B2 trusted observer socket-inode peer verification, endpoint rejection, streaming SSE chunks, log hash-linking.
  - Real name-minting authority, collision handling, 64-char cap.
  - Root selection normalization on `skill://` reads.
  - Full mediator normalization (reads, mutations, delegation, stand-in classifications).
  - Fail-closed validation for server/tool mismatches and unclosed pending tools at EOF.
  - Token-cap termination differentiation.
  - Minimal `bwrap` containment topology and host-home denial.
  - Tampering detection for immutable control state.
  - Harness integration via `run_episode` with synthetic OMP adapter.
- `test_harness_integration.py`, `test_stage_f_integrity_repairs.py`, `test_stage_f_v4_repairs.py`:
  - Preserved shared harness integrity, Claude adapter compatibility, control path exclusion checks, and fail-closed scoring behavior.

---

## 5. Invariant preservation

- **Immutable Protocol 7 candidate:** No modifications to `source/` or `dist/`.
- **Release state:** `PROTOCOL-RELEASE-STATE.yaml` remains untouched.
- **Stage A contract & thresholds:** Evaluation contract, fixtures, oracles, scoring thresholds, and historical Claude Run 6 qualification evidence remain untouched.
- **No evidence transfer:** No Claude evidence is claimed or transferred to OMP.

---

## 6. Admissibility and operator live qualification campaign boundary

While the D4 repair tranche has completed all 14 repairs and verified feasibility, **OMP profile admission remains blocked pending live multi-replicate campaign qualification**:

1. **Substrate network bridging:** Under `--unshare-net`, a local proxy route (via veth pair, loopback bridge, or abstract domain socket) must be bridged to allow OMP to reach the trusted observer while preventing arbitrary internet egress.
2. **Operator live probes:** Before admitting the OMP profile, an operator must execute and verify the live qualification episodes (T1–T8) across three replicates (R0, R1, R2) with live model backing, recording full traces, observer logs, mediator side-effects, and oracle evaluations.
3. **Claim-scoped admissibility:** Any claim where runtime-visible tool or root consumption cannot be definitively established by the live evidence channel shall remain claim-scoped inadmissible.
