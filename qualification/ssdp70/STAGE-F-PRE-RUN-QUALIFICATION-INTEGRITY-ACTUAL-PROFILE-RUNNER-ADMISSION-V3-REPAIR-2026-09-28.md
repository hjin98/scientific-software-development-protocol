# Stage F runner-admission v3 repair — 2026-09-28

## Status

**IMPLEMENTED — PENDING FRESH INDEPENDENT ACTUAL-PROFILE RECHECK**

This is an implementation/repair record, not a runner-admission record and not a PASS record. The
comparative Stage F campaign remains unauthorized. Governing implementation protocol: SSDP `6.6.0`.
The immutable Protocol 7 candidate `db94a2dfb7fef480f37227eab5c45256e89901b8`, `source/`, `dist/`,
`orchestrator/`, the qualification contract, thresholds, fixtures, human-trial rules and Stage G/H
semantics are unchanged. `~/ssdp70-fixture-custody` was not read, listed or written.

Starting head: `c40d988ef0f94a857d703bbc4bc9dede45118939`. Defect input (not authority):
`STAGE-F-…-RUNNER-ADMISSION-RECHECK-V2-STOP-BLOCKED-2026-09-28.md` (B3 defects). Host `socat` was
installed by the operator before this repair, so the sandbox now starts.

## Defects repaired (D4, eval tooling only)

All four were reproduced first under the real sandbox (unauthenticated launches, no model call).

1. **`--restricted` hid the project-installed SSDP skills** (0/7 in the catalog). Skill discovery is coupled to
   the *project* settings source; `--restricted`, `--setting-sources user|local|""` and `--add-dir` all yielded 0/7.
   Only loading the project source yields 7/7. Repair: the executor profile freezes
   `containment_policy.setting_sources: "project"` and launches with `--setting-sources project` (no
   `--restricted`); the evaluator freezes `"none"` and keeps `--restricted`. Because loading the project source
   makes executor-writable project settings a possible escape route (hooks run outside the sandbox), the adapter
   compensates: the harness writes a fixed `{}` `.claude/settings.json` (digest-bound, pre-launch verified);
   the launch settings set `disableAllHooks: true`, sandbox `denyWrite` for `<project>/.claude`, and permission denies for
   `Edit/Write/NotebookEdit(./.claude/**)`; only the project source is loaded (a planted `settings.local.json` marker was
   verified ignored); after execution the adapter's `validate_post_run_project_state` and the harness's installed-package
   re-digest make any change to project settings, unexpected `.claude` entries (runtime-created *empty* `agents/` and
   `commands/` tolerated) or the installed SSDP package `INADMISSIBLE`.
2. **Required `auto_memory_write` surface was suppressed by the adapter.** The adapter disables auto-memory, so init reports no
   memory path and every run was `INADMISSIBLE`. Repair: `auto_memory_write` is removed from both templates'
   `native_surface_requirements`. Its capability classification remains, so an exposed memory path is still classified and
   still required to lie inside the fresh run-owned HOME.
3. **Realized permission mode differed from the frozen mode and was unchecked.** The runtime forces `default` when
   `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` is set (kept for credential isolation). Repair: both templates freeze `permission_mode: "default"`
   and pass it explicitly; the adapter's runtime observation now exposes init `permissionMode`; `core70.validate_runtime_observation`
   and `validate_launch_identity` reject any difference from the frozen mode.
4. **New: launched-executable shadowing.** `adapters/claude.py::launch` reused the variable `executable` for the MCP server file, so
   `command_identity.executable` recorded the private MCP script path instead of `claude`, and `validate_launch_identity` would reject every
   MCP profile run. Fixed by renaming the loop variable; covered by a regression assertion.

The adapter identity is bumped to `claude-stream-json-v3` (the launch semantics changed); templates were updated accordingly and profiles
must be re-frozen from them. Historical v1/v2 profiles and the earlier STOP records are untouched.

## Verification executed

Interpreter Python `3.13.14`, PyYAML `6.0.3`. `py_compile` OK. `test_portable70.py` 17 OK; `test_harness_integration.py` 6 OK;
`test_stage_f_integrity_repairs.py` 32 OK (was 20; new tests cover the empty-memory frozen template, permission-mode equality, init
`permissionMode`, executor/evaluator launch flags and identity, fail-closed `setting_sources`, project-settings tamper before/after launch,
runtime-created empty dirs, and three real Claude Code 2.1.284 init traces); `test_mcp_stdio.py` 2 OK.

Live, unauthenticated (no model call, no tool effect) through the repaired realization on Claude Code `2.1.284`:

- new profiles frozen from the repaired templates (`profiles/`), `harness70.py episode --mode probe` through the executor profile:
  `profile_claim_errors: []`, catalog isolation OK with each SSDP skill exactly once, observed permission mode `default`,
  13 exact tools, MCP `ssdp70` connected, `command_identity.executable == "claude"`, sandbox started (no `socat` refusal). The
  episode still ends `EXECUTION_ERROR` because no qualification auth source exists (`Not logged in`).
- evaluator profile through the real launch path (`probe_evaluator_init.py`): no launch/runtime validation errors; tools
  `Glob, Grep, Read`; `mcp_servers: []`; permission mode `default`.

Evidence: `qualification/ssdp70/stage-f-runner-admission-v3-repair-2026-09-28/` (`profiles/`, `identities.json`, `arms.json`,
`freeze_profiles.py`, `probe-corpus/` checker-owned synthetic, `harness-probe-run/`, `native-traces/`, `evaluator-probe/`).

| Item | Value |
| --- | --- |
| Executor profile | `claude-code-2.1.284-sonnet5-high-local-samjin-executor-v3`, document `6f9529ce…`, key `698c680f1df289fc6e1b2f0a97f7fa231c7183dc5cab345a0559b0c9866836e2` |
| Evaluator profile | `claude-code-2.1.284-sonnet5-high-local-samjin-evaluator-v3`, document `9e8ddb73…`, key `5032d13abe314fdd446a1171e0091e2fa5c95faad30a095f5a0fd42f5559c5ff` |
| Adapter | `claude-stream-json-v3`, `adapters/claude.py` SHA-256 `d9646a8e46536d5f458b03fd6ce23b45ac331e021a56a41c26fbb7fa3bb8654d` |
| Core / harness | `core70.py` `4d869aee…`; `harness70.py` `14882bad…` |
| Capability manifests | unchanged: executor `048c00f6…`, evaluator `a138808f…` |
| MCP executable | `e51f0641…` (unchanged reviewed `mediator.py`) |

## Not verified by this repair (required in the fresh live recheck)

These need a model to drive tools and therefore an authenticated `SSDP70_*` source; none is claimed here:

- that the executor cannot write outside the project through the `Write`/`Edit` tools (bare `Write`/`Edit` are in `native_allowed_tools`), nor
  write `.claude/**` via the added permission denies or the sandbox `denyWrite`;
- that `default` mode with explicit allow/deny lists denies every tool outside `native_allowed_tools`, matching the intended `dontAsk` behavior;
- that project settings/hooks planted by the executor cannot take effect;
- all §1 items 2–9, 11 containment/entry/owner-read/termination/perturbation behavior and the whole §6 suite.

If any of the first three fails live, it is a further D4 defect for this adapter, not an admission.

## Remaining prerequisites outside this repair

1. **Auth (operator):** one `SSDP70_*` qualification-only source in the recheck session's environment.
2. **Custody (fixture-custodian context, not the checker/implementer):** the contract requires the custodian to author and hold fixtures, keys, oracles,
   probes and human-trial material and the checker to receive role/time-scoped access. This repair does not and cannot author them.
3. A fresh independent recheck of the exact v3 profiles.
