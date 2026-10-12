# OMP-only Stage F provider adaptation — blocker and Serious Challenge

- Date: 2026-09-29
- Branch: `ssdp-7.0-scientific-epistemic-closure`
- Verified starting head: `f5f3dc50667e9d57255a014b1599b4df6bdece3a` (exact)
- Bounded implementation commit: `eb3494f82d2348118867671e1f72a0ebfc10e893`
- Governing workplan: `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`, "OMP-only provider-adaptation slice" (lines 616-649)
- Governing contract: `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md` §1 items 1-11 and §6

## 1. Status and decision

**BLOCKED — SERIOUS CHALLENGE. The OMP execution profile is NOT admissible and is NOT frozen or admitted.**

The bounded OMP slice was implemented as far as the evidence permits, but two required
properties demanded by the workplan's feasibility gate could not be established by harmless
non-custody probing:

1. **Exact catalog / build / event completeness is not observable from the published
   machine-readable mode.** `omp --mode=json` exposes neither the OMP build identity nor the
   native tool catalog nor the registered MCP surface. Those appear only in the model request
   / system prompt, which the qualification harness does not retain as native stdout evidence.
2. **Provider-credential separation from agent-exposed processes is not demonstrated.** No
   realized substrate is available in this environment, and the candidate substrate design
   still leaves the provider credential readable by OMP's agent-exposed `bash`/`eval` because
   they share the OMP process mount namespace. No external credential broker route was
   established.

Workplan line 649 is explicit: stop before qualification-subject runs and return to D3 if
"the exact OMP build cannot expose enough evidence to prove catalog/tool/root/event
completeness" or "required process/network capability cannot be substrate-contained without
exposing provider credentials or unmediated external access". Both conditions hold. This
report does **not** propose an OMP-specific scoring path, weaker proxy, contract relaxation,
or transfer of Claude evidence.

## 2. What was implemented (bounded, provider-neutral, fail-closed)

Commit `eb3494f` contains only the portable core/harness repair and the OMP adapter/profile
scaffold. It does not modify `source/`, `dist/`, the Stage A contract, thresholds, fixtures,
oracles, frozen historical evidence, or custody material; `stub_tools/mediator.py` is
byte-identical (no MCP interoperability defect was reproduced).

- `qualification/ssdp70/eval/core70.py` — removed the Claude-only
  `mcp__<server>__<tool>` derivation and the global `startswith("mcp__")` inference. MCP
  tools are now bound by declared identity; a provider-native id declared by more than one
  server is rejected; every declared server tool must still appear exactly once in
  `native_tools` and be classified. Execution-profile schema unchanged.
- `qualification/ssdp70/eval/harness70.py` — provider control paths and the installed
  package root now come from the adapter (`project_control_paths` and the
  `install_skills` return value). No `.claude/skills` hard-coding. Exact-top-level-name
  validation for control/exclusion names is retained.
- `qualification/ssdp70/eval/adapters/claude.py` — compatibility only:
  `install_skills(dist, project, env=None) -> Path` and `project_control_paths` returning
  `[".claude", ".mcp.json"]`.
- `qualification/ssdp70/eval/adapters/omp.py` — new OMP adapter.
- `qualification/ssdp70/eval/capabilities/omp-headless.json` — new candidate capability
  manifest.
- `qualification/ssdp70/eval/profiles/omp-headless.template.json` — new OMP profile
  template, deliberately carrying `MUST-BE-FROZEN-BEFORE-QUALIFICATION` markers.
- `qualification/ssdp70/eval/test_omp_adapter.py` — new focused tests.
- `qualification/ssdp70/eval/test_harness_integration.py` and
  `test_stage_f_v4_repairs.py` — adapted to the narrowed adapter interface.

## 3. OMP capabilities established (harmless local-mock probes; no real credential used)

Exact build: `omp/18.0.11`, ELF x86-64, BuildID
`2c2e51f3b6fae6722da4f7b69751a2e9467ab063`, size `194573512`, sha256
`6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26`.

Established:

- Headless `-p` and `--mode=json` NDJSON event stream (session format version 3) with
  kinds `session, agent_start, turn_start, message_start, message_update, message_end,
  turn_end, tool_execution_start, tool_execution_update, tool_execution_end, auto_retry_end,
  agent_end`; `tool_execution_start`/`tool_execution_end` retain full args/results and
  `isError`.
- Model/thinking selectors: `--model <provider>/<model>`, `--thinking <level>`; run-owned
  config at `$HOME/.omp/agent/{config.yml,models.yml,mcp.json,skills}`.
- **Lossless MCP binding.** MCP tools are reached through the `write` tool as
  `xd://mcp__<server>_<tool>` devices; `tool_execution_end.result.details.xdev` carries
  `serverName`/`mcpToolName`. Observed omp/18.0.11 device-id rule: ASCII digits are
  removed from both components (server `ssdp70`, tool `issue_search` ->
  `xd://mcp__ssdp_issue_search`; server `alpha`, tool `tool_a1` -> `xd://mcp__alpha_tool_a`).
  The adapter proves the six-raw-name to six-native-id bijection and validates the declared
  surface against it.
- **Ambient-discovery closure.** A fresh run-owned HOME plus `--no-extensions --no-rules
  --no-lsp --no-title --no-session` loads only the run-owned `~/.omp/agent` state. Project
  `.omp`/`mcp.json`/`.mcp.json`/`.cursor`/`.vscode` discovery is refused by the adapter
  and re-verified post-run.

## 4. Unresolved required properties (blockers)

### B1 — Exact catalog/build/event completeness (contract §1 items 1, 4, 5; workplan line 641/649)

`omp --mode=json` does not expose the OMP build version, the native tool catalog, the
registered MCP server surface, or an event-kind inventory. The observed stream carries
assistant `provider`/`model` only. Consequently:

- `runtime_observation(stdout)` cannot independently observe `runtime_version`, `tools`,
  `mcp_servers`, or required native surfaces; the adapter reports them as unobserved and
  `core70.validate_runtime_observation` fails closed (verified: "runtime init did not expose
  a valid native tools list", "runtime-observed provider/runtime version does not match").
- The event-kind inventory is only partially probed (delegation/subagent internals,
  compaction, approvals/denials and error variants were not fully exercised).

A qualification-owned logging model proxy (which would retain the exact model request /
system prompt) is a candidate remedy but is **not built or verified**; until then the
catalog cannot be treated as exact.

### B2 — Provider-credential substrate separation (contract §1 items 3, 8; workplan line 631/649)

No admissible substrate is realized here: `bwrap`/`unshare`/`systemd-run` exist, but
`docker`/`podman`/`nsjail`/`firejail` do not. More fundamentally, OMP's agent-exposed
`bash`/`eval`/`write` run inside the same mount namespace as the OMP parent, so a
credential placed in the run-owned HOME is readable by the agent. A network-namespace
substrate can close egress, but it cannot by itself separate the model-control-plane
credential from agent-exposed processes. The profile is inadmissible unless an operator
establishes an external credential broker that the sandbox cannot reach; that route is not
demonstrated. `native web_search` was observed to attempt real external network calls, and
`bash`/`eval`/`write` run with full filesystem/network when unbounded.

### B3 — Provider-managed unknowns (contract §1 item 1)

Auto-retry (cap 3 observed), compaction, maintenance routing, title, advisor, prewalk,
autolearn, memory and background daemons are not fully enumerated or frozen. They are
recorded in the template's `provider_managed_unknowns` as `uncontrolled`.

## 5. Adapter fail-closed behavior (verified)

- `realize_containment` raises unless the profile declares the `omp-bwrap-substrate-v1`
  policy with an operator-frozen substrate digest and a
  `external-broker-outside-sandbox` credential-isolation record; the unfrozen template
  raises "OMP containment substrate is not operator-frozen; OMP admission is blocked".
- Unknown native event kinds are oracle-relevant, mapped to no normalized event, and
  recorded as errors (completeness map fails closed).
- A project-local discovery path or a credential variable in the run environment is refused.
- The template loads schema-correctly but `validate_runtime_observation` rejects it with the
  unfrozen-marker and unobserved-catalog errors (verified).

## 6. Tests run and results

Command: `cd qualification/ssdp70/eval && python3 -m unittest test_portable70
test_harness_integration test_mcp_stdio test_stage_f_integrity_repairs
test_stage_f_v4_repairs test_omp_adapter`

- Result: **Ran 140 tests — OK** (portable, Claude, MCP, Stage F integrity/repair, OMP).
- `test_omp_adapter` alone: **23 tests — OK**, covering provider-neutral MCP binding
  (non-convention ids accepted; cross-server duplicates and missing/unclassified tools
  rejected), OMP normalization against `core70.validate_normalized_events` and
  `validate_completeness_map`, unknown-event fail-closed, ambient-discovery closure,
  containment fail-closed, and package-root binding.
- `test_mcp_stdio.py` remains the shared-mediator proof; `stub_tools/mediator.py` is
  unchanged.

`python3 -m pytest` is unusable in this environment (anyio plugin vs system pytest:
`ModuleNotFoundError: No module named '_pytest.scope'`); `unittest` is the runner used.

## 7. Required operator live probes (not yet run — must not be reported as PASS)

On the exact candidate OMP profile, an operator must run and record:

1. Exact runtime/model/reasoning/output-mode/config-source and exact catalog/server/tool
   identity, including the independent observation channel that `--mode=json` lacks.
2. SSDP root selection and skill read from the exact installed package.
3. One mediator read and one mediator mutation plus scripted delegation, with
   side-effect-log/object-version evidence matching normalized events.
4. Hostile containment/discovery probes (project-local discovery, ambient credential,
   external network, out-of-workspace write, credential read from agent-exposed `bash`).
5. Post-run package, config/control, mediator executable, private-state denial and
   runtime-created-entry integrity.

A required probe not exercised is `UNRESOLVED`, never PASS.

## 8. What this report does NOT claim

- No OMP admission, no OMP execution-profile freeze, and no OMP qualification result.
- No transfer of Claude Run 6 or any Claude-derived live evidence to OMP.
- No modification of the immutable Protocol 7 semantic candidate, the Stage A contract,
  thresholds, fixtures, oracles, or frozen historical evidence.
- No weakening of any runner-admission check.

## 9. Routing

Return the OMP slice to D3 for resolution of B1 and B2 (an independent catalog/build
observation channel and a credential-isolating substrate/broker), or record the OMP profile
as claim-scoped inadmissible. A fresh independent context must review the revised workplan
before dependent OMP D4 is treated as authorized. Pi remains deferred.

### Credential-handling note

A real provider API key value is present in `~/.omp/agent/models.yml`. It was not read,
copied, logged, or used. All probes used a qualification-owned local OpenAI-compatible
stand-in endpoint with a sentinel value, under a fresh run-owned HOME.
