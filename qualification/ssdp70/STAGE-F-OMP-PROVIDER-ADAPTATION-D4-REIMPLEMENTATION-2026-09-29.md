# OMP-only Stage F provider adaptation — fresh D4 implementation and recheck record

- Date: 2026-09-29
- Branch: `ssdp-7.0-scientific-epistemic-closure`; verified starting head `9b657e2f42b13865ff5ea5b2441e52e0e9fa957c` (tree identical to the accepted D3 baseline `7761cef`)
- Governing SSDP: `6.6.0`. Governing authority: the OMP-only provider-adaptation slice, the accepted D3 trust-topology/runtime-observation repair, the B1/B2/B3 gate and the 14-item D4 repair tranche of `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`; `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` §1 items 1-11 and §6.
- **Status: D4 implemented and rechecked. OMP is NOT admitted, NOT frozen as an admitted profile, and no Stage F qualification result is claimed.** Fresh exact-profile operator probes and an independent runner-admission review (§1 items 1-11, §6) remain mandatory.
- Supersession: this record supersedes the D4 implementation attempt `03fcaae` (reverted at `9b657e2`; kept in history only as defect evidence, not resurrected) and corrects the understatement in `OMP-PROVIDER-ADAPTATION-BLOCKER-AND-SERIOUS-CHALLENGE-2026-09-29.md`. Historical evidence and that record are unchanged.

## 0. Decision

No D3 reopen condition occurred and no Serious Challenge is raised. The accepted three-principal graph was realized with the exact OMP build (`omp/18.0.11`, sha256 `6054460b…6d26`). B1, B2 and B3 were demonstrated on the assembled production path, not on standalone helpers. Six review points for the independent D3/D4 reviewer are listed in §8; none requires a topology change, but two touch the graph's wording (the in-sandbox relay endpoint, and launcher attestation of build identity).

## 1. Architecture realization

Production path exercised by every acceptance test: `harness70.run_episode` → `adapters.omp` (realization, principals, sandbox, launch) → frozen OMP executable inside bubblewrap → qualification observer → qualification MCP bridge + unchanged `stub_tools/mediator.py` → deterministic local model-provider stand-in (the only substituted component; it lies below every semantic owner being accepted) → raw hash-linked evidence + native JSON trace → adapter normalization → core validation.

| Principal | Realization | Owns / holds | Cannot |
|---|---|---|---|
| Qualification supervisor | `harness70.py`, `adapters/omp.py`, `mcp_bridge70.py` (+ unchanged mediator as its stdio child) | frozen profile, control files, run identity, mediator stub root/log/account/server, custody | — |
| Provider-control / observation | `observer70.py` (own process) | the provider credential (own environment only), the only provider route, raw hash-linked request/response evidence | anything but `POST <inference path>`; no custody, no mediator state; body forwarded byte-identical, only the placeholder key swapped for the credential |
| Subject / executor | frozen OMP + every process it starts, in `bwrap` (user/pid/ipc/uts/cgroup/net namespaces, empty network namespace, all capabilities dropped, seccomp denylist, `--as-pid-1` launcher) | run project (rw), run HOME (rw, control files read-only-overlaid), tmpfs `/tmp`, read-only `/usr`, synthetic read-only `/etc`, read-only arm package, read-only launcher/OMP | credential, host HOME, custody, mediator/observer/supervisor state, any network but loopback, any transport authority |

**Authority mechanism (the D4 choice inside the accepted graph).** The subject reaches the two authorized edges only through `subject_launcher.py`, the supervisor-authored, read-only-mounted, non-dumpable, pid-1 process of the sandbox. Each edge is one inherited anonymous-pipe pair (`muxhttp70.py`: framed HTTP/1.1 over a descriptor pair) whose other end is held by exactly one principal. There is no filesystem socket, host port, token or executable identity involved. The launcher listens on loopback inside the empty network namespace (`127.0.0.1:31001` inference, `:31002` MCP) and relays a connection only if its client socket is held **solely by the OMP process the launcher started** (`/proc/net/tcp` inode → `/proc/*/fd` holders). A `bash` child, a second copy of the same executable, or a process that inherited a descriptor is refused and the attempt is retained as a blocked `network_external_action` event. The launcher closes every other inherited descriptor, is non-dumpable (its `/proc/<pid>/{mem,environ,fd,maps}` are closed to siblings), OMP's stdout/stderr are private loopback sockets (a socket cannot be re-opened through `/proc/<pid>/fd/N`, so the native trace cannot be forged or read), and a seccomp denylist plus Yama close `ptrace`/`process_vm_*`/`pidfd_*`. Because the inference capability belongs to the launcher-started instance and its inherited descriptors, executable identity is never used as authorization.

**Evidence path.** The observer, bridge and launcher write append-only hash-linked chains (`evidence70.py`, drained concurrently by the harness) that the adapter verifies (`parse_chain`: dropped, reordered, altered and truncated records are detected; the `end` record counts records). The harness persists them as `adapter-artifacts/*` (now an integrity root).

Files: new `observer70.py`, `mcp_bridge70.py`, `muxhttp70.py`, `evidence70.py`, `subject_launcher.py`, `seccomp70.py`, `omp_inventory_probe.py`, `omp-build-inventory-18.0.11.json`, `stand_in_provider.py`, `omp_rig.py`, `test_omp_units.py`, `test_omp_integration.py`, `test_control_path_policy.py`; rewritten `adapters/omp.py`, `capabilities/omp-headless.json`, `profiles/omp-headless.template.json`; shared changes `core70.py`, `harness70.py`, `adapters/claude.py` (§7). `stub_tools/mediator.py`, `source/`, `dist/`, fixtures/oracles/thresholds, custody and Claude Run 6 evidence are untouched.

## 2. B1 — real observation and event completeness: DEMONSTRATED

Every claim below is derived from the observer/bridge/launcher chains plus the native trace, and compared (never sourced) against the installed package, the frozen profile, launch argv and the harness prompt.

| Bound item | Runtime evidence |
|---|---|
| Executable/build identity | launcher: sha256 of the mounted executable = frozen digest, `/proc/<omp>/exe` inode = that file, the exact binary's own `--version` = `omp/18.0.11` (probe run in the sandbox before start); observer: every request's client identity is `Bun/1.4.0`; bridge: MCP `clientInfo` `omp-coding-agent/1.0.0` |
| Provider/model, reasoning, output mode | request body `model`; `reasoning_effort` bound to the frozen thinking level (`high`→`high`, `medium`→`medium`, `off`→`minimal`; a mismatch or a non-reasoning model with a non-`off` level fails); native `session` version 3 event = the JSON output mode |
| Effective configuration source | the exact binary reports all 481 settings before the run (`omp config list --json` in the sandbox); every key must equal the exact-build inventory, the 65 frozen keys must equal their frozen values; any difference (`retry.enabled` patched on in a test) fails |
| Complete native tool surface | first request's `tools[]` = exactly `read, glob, grep, edit, write, bash` + the six minted MCP ids, unchanged in every request; extra (`task`, `eval` injected via argv in a test) fails |
| Connected MCP server + exact MCP tool surface | bridge `initialize` + `tools/list`; raw mediator tool names → OMP-minted ids bijection, and the observed native parameter schemas/descriptions equal the raw `inputSchema`/`description` (intent tracing is frozen off, xd:// devices frozen off) |
| Runtime-visible catalog, package identity, multiplicity | parsed from the system prompt the model received; must equal the mounted package's entries exactly, each skill once; a runtime-only hide (`skills.ignoredSkills`) with unchanged files fails |
| Root activation / consumed material | §5 |
| Model input integrity (new) | every request must be the reviewed grammar: system prompt (starts with the OMP base prompt, no `<project>`/context files, ends with the MCP server's own `instructions`), one user message `[dated <system-reminder>, harness prompt]`, then exactly the provider's earlier assistant messages and tool results; anything else (the build's hard-coded `<system-injection>` steering) is inadmissible |
| Event completeness | native events + observer + bridge + launcher records form one classified stream (`normalization-map.json` covers every record); the native message events must equal `agent_end`'s transcript; every native assistant message/tool call must equal the observer-retained provider response; every tool result must equal the model-received tool message; every mediator result must equal the bridge-retained raw result; request count must equal assistant turns (provider-layer resends accounted separately) |

Unknown native event kinds (all 14 hard-coded provider-managed kinds and any other), dropped/reordered/duplicated/truncated native lines, unmatched starts/ends, a tool pending at EOF, forged tool ids, tampered/truncated observer or launcher evidence, raw/native MCP identity mismatch and a missing `rawContent` all fail closed (tests in §6).

## 3. B2 — privilege separation while inference works: DEMONSTRATED (one probe not executable here)

Simultaneously, in real runs: inference succeeded through the observer (the stand-in verified the sentinel credential arrived only upstream), MCP through the bridge succeeded, and a scripted executor attempted the following from `bash`/python (results are retained in the run's normalized events):

- **Credential**: not in the environment, files (`grep -r` of the sentinel over every subject-visible root), `/proc/*/environ`; the observer is not in the subject pid namespace.
- **Transport**: python connections to `127.0.0.1:31001/31002` (with the correct placeholder key) were relayed to nothing and recorded as blocked events; a second copy of `/opt/omp/omp` launched from `bash` made 14 relay attempts, all denied — the stand-in still saw only the authorized instance's requests.
- **Network**: `93.184.216.34:80`, `1.1.1.1:53` → `ENETUNREACH`; other loopback ports (including the host stand-in's port) → `ECONNREFUSED`.
- **Host HOME / files / escapes**: no `/home/<user>`, `/root`, `/etc/shadow`; a host-only secret file could not be read by absolute path, `../` traversal, `/proc/self/root`, or a workspace symlink to it; `/etc` is a synthetic read-only view.
- **Supervisor/mediator/observer state**: `find /` for the mediator log/account/server, evidence and observer names → empty; `/proc/self/mountinfo` contains none of their names; the pid namespace holds only the launcher (pid 1), OMP and its children; `/proc/1/{environ,mem,fd,maps}` → `EACCES`; `ptrace`, `process_vm_readv`, `pidfd_open/getfd` → `EPERM`; `open(/proc/<omp>/fd/{1,2,socket})` → `ENXIO`.
- **Writes/immutability**: writes to `/usr`, `/etc`, the package, and OMP's `config.yml` fail (`EROFS`/`EACCES`); `/tmp` and HOME scratch are writable but ephemeral/inventoried; control/package digests before = after; host-side mutation of `mcp.json`/the package is detected post-run.

**Not executable in this environment (UNRESOLVED as a positive probe):** the Claude Code Bash sandbox this work ran in forbids creating `AF_UNIX` sockets for every descendant, so an executor `connect()` to a *local UNIX-domain socket* cannot be exercised as a substrate denial (it returns `EPERM` from the outer sandbox, which would prove nothing). The design uses no UNIX-domain socket at all; the subject view contains no socket file (`find / -type s` empty), `/proc/net/unix` is the sandbox's own, and the IPC/net/pid namespaces are unshared. This is evidence of absence of a route, not a demonstrated denial of an attempted connection.

## 4. B3 — provider-managed state closure: CLOSED OR CLAIM-SCOPED

The retained inventory `qualification/ssdp70/eval/omp-build-inventory-18.0.11.json` (digest-bound into the profile) records: all 481 settings with default, effective value under the frozen profile and closure class (65 frozen, rest sub-parameters of closed features, UI-irrelevant, network-unreachable, tool-not-exposed or default-retained-and-observed); every path the build probes at startup (214 project-relative, 110 HOME-relative, ancestor probes), programs it executes (`lspci`), network destinations it attempts (local model-server probes `127.0.0.1:11434/1234/8080`, provider catalogs — all unreachable in the empty namespace), and hostile-source effect tests.

| State | Disposition |
|---|---|
| retry / model fallback / compaction / branch summary / context promotion / advisor / prewalk / plan / goal / memory / autolearn / recap / title / TTSR / todo reminders / loop guards / magic keywords / vision describe / update check / autoqa push / power / notifications | **disabled** by frozen settings; effective values re-read from the exact binary each run |
| OMP, Claude, Codex, Gemini, OpenCode, Cursor, Windsurf, VS Code, GitHub/agents, standalone-MCP, plugin/extension/hook discovery | project- and HOME-level foreign **skills** and **project MCP** are disabled by settings (`skills.enable*=false` + `customDirectories`, `mcp.enableProjectConfig=false`, `--no-extensions --no-rules --no-lsp`); the sources that the build reads regardless of settings (context files `AGENTS.md`/`CLAUDE.md`/`.github/copilot-instructions.md`/… , HOME `SYSTEM.md`/`APPEND_SYSTEM.md`/`AGENTS.md`, HOME `.env` files, HOME-level MCP configs) are **refused before launch** when present in the fixture baseline or HOME, and **detected from the observed prompt** if they nevertheless enter. Hostile probe result: only `.github/copilot-instructions.md` and HOME `AGENTS.md` reached the prompt (detected → inadmissible); no foreign skill, hook, extension, MCP tool, bunfig code or project `.env` took effect; HOME `.env` did enter OMP's environment, hence the refusal. |
| ancestor-directory discovery | closed by the substrate (no host ancestors exist in the sandbox) |
| session state | `--no-session`; runtime state confined to run HOME and inventoried (`control` + `omp-runtime-state` only in a normal run) |
| **Provider-layer retry (newly discovered, not configurable)** | hard-coded below OMP's `retry.*`: identical-request resends after transient errors (observed up to ≥6 after HTTP 5xx, 5 after 429; ≤10 accepted) and after an empty completion (2). **Frozen + observed**: allowed only when byte-identical to the predecessor after a retryable/empty response within those limits; recorded in `usage_timing.provider_layer_retries`; arm-neutral profile unknown `provider-layer-retry-of-transient-errors-and-empty-completions`. |
| **Runtime-injected steering (newly discovered, not configurable)** | after repeated empty completions the build appends a hard-coded `<system-injection>` user message (`Attempt #n/3`) that the native JSON stream never shows. **Claim-scoped inadmissible**: any run containing it fails closed with the message quoted; not silently absorbed. |
| Hardware/host fingerprint in the prompt (`<workstation>`), dated reminder | recorded; arm-neutral provider-managed unknowns in the profile |
| Local model-server discovery probes | unreachable by construction (empty network namespace); listed |

## 5. Root selection and consumed resources (T1/T7/T8)

`root_selection` is emitted only at a **successful** native `read` of `skill://<root>` (or the mounted `SKILL.md`) whose returned material the observer saw delivered to the model; it binds the logical root, `ordinary-skill-read` vs `explicit-instruction-skill-read` (from the episode entry), the native operation/input, the exact resolved package identity, and the consumed resource (`consumed_resource`: sandbox path, package-relative path, resource sha256/bytes, observer request index/record position, `match` = exact/partial/none with line ranges parsed from OMP's hashline/footer/gap forms). A failed or attempted read, a read by `bash`, and catalog visibility create no root selection. Reads truncated by the build's 300-line default are `partial` with exact ranges, never `exact`. Exact consumed SSDP material **is observable** on this build, so the adapter does not scope T1/T7/T8 inadmissible; whether the frozen Stage A byte-accounting semantics are computable from these fields, and the fixtures' freedom from provider context files, are for the independent checker.

## 6. Status of the 14 D4 repairs

| # | Repair | Status |
|---|---|---|
| 1 | Real execution `run_episode → omp.launch` | DONE — `launch()` starts principals, sandbox, real OMP; every integration test uses it |
| 2 | One provider-neutral private MCP layout | DONE — `core70.private_mcp_paths`, created by the harness, consumed by Claude and OMP; no parallel layout |
| 3 | Sound control-path exclusion | DONE — baseline-absence refusal; type/digest before+after (`project-control-record.json`); `immutable` policy detection; OMP has no project control path. Claude keeps its adapter-classified `.claude` policy (unchanged behavior) |
| 4 | Minimal filesystem visibility, host-read denial | DONE — §3 |
| 5 | Immutable OMP config/MCP config/package + digests | DONE — read-only overlays, pre-launch and post-run digest verification, host-mutation detection |
| 6 | Actual three-principal realization | DONE — §1 |
| 7 | Trusted-observer evidence ingested by the real harness path | DONE — `adapter_artifacts` persisted and hash-protected; disconnecting the observer (misrouted or emptied) is not green |
| 8 | Genuine root selection | DONE — §5 |
| 9 | Lossless mediator normalization | DONE — store identity, actual operation, query, object ids, before/after versions (bound to the stand-in's final files), status/reference, mutation disposition, delegate id/parent/relation, `serverName`, `mcpToolName`, native tool id, raw/trusted-bridge result digests; cross-checked, missing/contradictory identity fails. The raw *device id* is not applicable: xd:// devices are frozen off, so MCP tools are top-level native ids |
| 10 | Exact native tool-surface restriction | DONE — `--tools` + runtime-observed equality; attempts to call unexposed tools are retained as blocked attempts |
| 11 | Complete exact-build discovery closure | DONE / CLAIM-SCOPED — §4 |
| 12 | Fail-closed normalization edge cases | DONE — pending/unmatched/truncated/dropped/reordered/duplicated/unknown, external write classification (`external` vs `workspace`, blocked vs sandboxed), turn cap (`turn_cap`), token cap (`token_cap`), timeout (`timeout`), error, all distinct from `completed` |
| 13 | Exact OMP MCP name minting | DONE — `mint_mcp_tool_name` reproduces `Qro`/`hft` (digit runs become `_`, not removed); >64-character names are refused because the Bun.hash suffix is not reproduced; tests include normalization/collision cases; a real run confirms the six ids |
| 14 | Superseding record | this document |

## 7. Shared-harness and shared-core changes (provider-neutral; Claude behavior preserved)

`core70.py`: `PRIVATE_MCP_LAYOUT`/`private_mcp_paths`; three new evidence-integrity roots. `harness70.py`: private layout via core; control-path baseline refusal and before/after record; optional adapter hooks (`support_files` in run identity, `adapter_artifacts`, `post_run_integrity`, `runtime_observation(stdout, context)` + `observation_errors`, normalization context incl. `entry`/`profile`/`prompt`). `adapters/claude.py`: consumes the shared layout only. Three **pre-existing supervisor defects that the OMP attack probes exposed, fixed for both providers**: (a) `capture_project_state` followed executor-created symlinks with `copytree` (a workspace symlink to `../../..` copied the host filesystem into the evidence/oracle view — reproduced, filled the disk); now `symlinks=True` plus `final-tree-symlinks.json`; (b) the supervisor wrote `.git/info/exclude` through an executor-planted symlink (arbitrary host file overwrite) and ran `git add`/`git diff` with executor-controlled config (`core.fsmonitor`, filters, textconv, hooks); now no write-through, raw executor config retained as evidence, harness-owned config, config-borne execution disabled, a `.git` that is not a plain directory reported and not used. Both have tests in `test_control_path_policy.py`.

## 8. Review points for the independent reviewer (not blockers)

1. The in-sandbox relay is the subject-side endpoint of the two authorized edges (single-purpose, holds no credential, forwards to the two fixed descriptors). If the D3 reviewer reads "new process" broadly, this is the item to rule on; realizing the edges without it would need an OMP-side unix-socket transport OMP does not offer.
2. Executable/build identity is attested by supervisor code (launcher) — the observer sees only the client identity `Bun/1.4.0`; the OMP build string is not on the inference path.
3. The mediator's declared transport stays `stdio` (its own identity); OMP reaches it as streamable-HTTP MCP through the supervisor bridge.
4. Two hard-coded runtime behaviours (provider-layer resend, empty-stop steering) cannot be disabled; the first is frozen+observed, the second claim-scoped inadmissible (§4). Real-provider runs will occasionally hit them and must be re-run, not adjusted.
5. `/proc` global files (`cpuinfo`, `version`, …) and the names of run-owned bind-mount source directories (`/proc/self/mountinfo`) are readable; contents of harness-private state are not.
6. Verified with `bwrap 0.6.1`, Linux 6.8, Yama scope 1, unprivileged user namespaces; the adapter records and fails closed on capability set, `no_new_privs`, seccomp mode and Yama scope.

## 9. Evidence executed

Command, from `qualification/ssdp70/eval` on this checkout (Python 3.10, bubblewrap 0.6.1, Linux 6.8.0, Yama scope 1):

```
python3 -W ignore -m unittest -v test_omp_units test_omp_integration test_control_path_policy \
  test_portable70 test_harness_integration test_mcp_stdio test_stage_f_integrity_repairs test_stage_f_v4_repairs
Ran 220 tests in 362s — OK (0 skipped, 0 expected failures)
```

| Module | Tests | What it proves |
|---|---|---|
| `test_omp_integration` (real path) | 48 | B1 (15): full-path completeness and runtime-derived surfaces, every record classified, credential only upstream, runtime-only catalog difference, observer disconnected/misrouted/evidence removed, MCP-alive/inference-dead, perturbed effective setting, native tool restriction and contamination, model/reasoning binding, unknown/dropped/reordered/truncated/duplicated/unmatched/pending native events, raw↔native MCP identity mismatch, forged/altered assistant events against the provider response, tampered principal evidence. Root selection and consumed resources (7). Mediator normalization (2, all six operations incl. refused mutation, version binding to the stand-in files, delegate found/unknown). Termination, caps, provider-managed behaviour (10): turn cap, token cap, timeout (sandbox fully gone), provider-layer retry/empty-completion accounting and limits, runtime-injected steering, enabled auto-retry, frozen 429. Discovery/provider-managed state (8): hostile project sources, context-file detection, HOME override/append detection, HOME `.env` effect, pre-launch refusal through the harness, ancestor discovery, HOME inventory, profile/digest perturbations. B2 (6): inference+MCP working with credential/HOME/escape/mediator-state denial, transport and second-OMP denial, no read/tamper of launcher/trace/`/proc`, external-write and immutable-control containment, host-side mutation detection, structurally empty local IPC. |
| `test_omp_units` | 38 | exact name minting, catalog/consumption parsing, evidence chains, descriptor transport, seccomp filter, profile/digest/build perturbations, inventory closure, discovery refusal for every identified project (22) and HOME (39) source and every credential variable |
| `test_control_path_policy` | 17 | control-path shadowing refusal, before/after binding, immutable mutation detection, support files in run identity, legacy (Claude-style) adapter unchanged, supervisor never follows executor symlinks or executes executor git config |
| `test_portable70`, `test_harness_integration`, `test_mcp_stdio`, `test_stage_f_integrity_repairs`, `test_stage_f_v4_repairs` | 17 / 6 / 2 / 32 / 60 | the complete existing portable, Claude, MCP-mediator and Stage F suites, unchanged, after the shared harness/core edits |

Also executed: `python3 omp_inventory_probe.py` (two real sandboxed runs with hostile sources; strace trace and observer-evidence effects) regenerating the retained inventory; the exploratory B2 attack scenarios that found the three defects fixed in §7 and the pid-1 descriptor exposure (bwrap's init process held the transport descriptors; the launcher is now pid 1 and non-dumpable).


## 10. Not executed / limits

- The `AF_UNIX` positive-connect probe (§3); no real provider or credential was used or needed (sentinel only); no live provider retry/rate-limit behaviour beyond the stand-in's scripted 429/5xx/empty responses; no Pi work; no operator exact-profile probes; no independent runner-admission review; no Protocol 7 qualification subject was run.
- `omp_inventory_probe.py` must be re-run (and the digest re-frozen) for any other OMP build.

## 11. Admissibility summary

- **T1/T7/T8**: exact consumed SSDP material and root activation are observable and bound (§5); not scoped inadmissible by this adapter. Open for the checker: Stage A byte-accounting computability and provider-context-file-free fixtures.
- **General OMP claims**: admissible-in-principle under this frozen build/profile shape with the claim-scoped exclusions of §4 (runtime-injected steering runs; fixtures/HOME containing provider context or discovery sources) and the arm-neutral unknowns (backend shard, host-derived prompt block, provider-layer resend). Nothing here is an admission.
- **Still unadmitted**: OMP remains unadmitted pending fresh exact-profile operator probes and an independent runner-admission review under contract §1 items 1-11 and §6.
