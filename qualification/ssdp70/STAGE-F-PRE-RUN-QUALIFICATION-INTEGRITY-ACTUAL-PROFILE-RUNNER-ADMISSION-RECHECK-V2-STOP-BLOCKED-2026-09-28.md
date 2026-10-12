---
kind: independent-stage-f-pre-run-actual-profile-runner-admission-recheck
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: STOP/BLOCKED
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_head: c47b2d7c96d44a22fc5fb97e5a5d5c88210dbb5a
stdio_mcp_implementation: 303ead02e91c923fec991cc447f8b892b7fee88a
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
target_runtime: Claude Code 2.1.284 (environment-local, this host)
qualification_campaign_authorized: false
active_serious_challenge: none
evidence_directory: qualification/ssdp70/stage-f-runner-admission-recheck-v2-2026-09-28/
---

# Protocol 7.0 Stage F actual-profile runner-admission recheck (v2 profiles) — STOP/BLOCKED

## Disposition

**STOP/BLOCKED / NO-PASS. Do not begin the Stage F comparative campaign.**

This is a fresh independent recheck of head `c47b2d7c96d44a22fc5fb97e5a5d5c88210dbb5a` on the
actual local Claude Code runtime. The local and remote branch heads were verified equal to that head
before work began (`git ls-remote` and local `HEAD`). The prior STOP/BLOCKED record was used as defect
input only; the result below was re-derived.

No Serious Challenge is raised against the accepted portable runner-admission contract. The block is
environmental and D4-implementation: the actual profile **cannot be launched, authenticated or admitted**
on this host, and three D4 defects that would make every run inadmissible even on a provisioned host were
observed. The immutable Protocol 7 candidate `db94a2dfb7fef480f37227eab5c45256e89901b8`, `source/`,
`dist/`, `orchestrator/`, the contract, thresholds, fixtures, human-trial rules and Stage G/H semantics
were not modified. `~/ssdp70-fixture-custody` was not read, listed, written, enumerated, copied or hashed.
No 6.5/6.6/7.0 comparative episode, pair, burden comparison, human trial or Stage G/H work was run.

## Authority reconstructed

Governing implementation protocol: SSDP `6.6.0`. Reconstructed from `AGENTS.md`, the governing workplan
(Stage F portable execution-profile architecture), contract §1 items 1–11 and §6, the actual-profile repair
record (implementation evidence only) and the prior runner-admission STOP record (defect input only). The
repair record's claim that unit suites pass was independently re-executed here as supporting evidence
only (below); it is not admission evidence.

## Exact identities

| Item | Value |
| --- | --- |
| Tested commit | `c47b2d7c96d44a22fc5fb97e5a5d5c88210dbb5a` (executable eval code identical to `3a71f5f`/`303ead0`) |
| Claude Code | `2.1.284 (Claude Code)`; binary `~/.local/share/claude/versions/2.1.284`, SHA-256 `5cd90aabd83f8a15136c35aa37bb1d92b348993573316643dc3fe4e04afbf88f`, 243,059,896 B |
| Model | `--model claude-sonnet-5`; live init reports `claude-sonnet-5` (serving revision behind the alias not exposed; classified arm-neutral) |
| Reasoning | frozen `effort: high` passed as `--effort high`; the init event does not expose effort, so it is command-bound, not runtime-observed |
| Adapter | `claude-stream-json-v2`, `adapters/claude.py` SHA-256 `cc4066bf03bc3eb56f8e1affe88d8704ee0c5316e5096307fa05428f0054b622` (git blob `e1ccfed9…`) |
| Core | `core70.py` SHA-256 `75f40d7e9d7258ce192555704d55464565e52ee4ba37e5d6da124abc86df11f7` |
| Harness | `harness70.py` SHA-256 `c530d6da48f907fae65f9efcd71941e83bc0c669e3e820eb9a261be3b7438be2` |
| Assessment wrapper | `assess70.py` SHA-256 `290cd862f0431ae79ae15bb93186fefbb6de7072c1cb83d68524d7fef86d30c6` |
| Executor capability manifest | `claude-headless.json` file SHA-256 `81611be8…`; normalized digest `048c00f6e18af92641cd934d015afc706c070c5699604491f9158944da2cd9cb` |
| Evaluator capability manifest | `claude-evaluator-readonly.json` file SHA-256 `3459789787…`; normalized digest `a138808f4ec3970a06a4480e08eb969f3bec7ded4352e8939e8a8deb41063ca3` |
| Executor profile | `claude-code-2.1.284-sonnet5-high-local-samjin-executor-v2`; document SHA-256 `fff6e548adeea1d7a0e7c9b3527d4501c180b5f23e3958bf31c23fbeac325e77`; profile key SHA-256 `c30ea2157a57129071e6cbc2bcb11431f61adfbe2ed6c17f62b09ec721d5213d` |
| Evaluator profile | `claude-code-2.1.284-sonnet5-high-local-samjin-evaluator-v2`; document SHA-256 `e6c06d88f8861cee49e2197995b39fe31f3d8f5cc7a46778da5160d1e05d71f6`; profile key SHA-256 `9747eb8a00f5e162b5f3214eec15f12ba4ca10182df13a04be3aea143e8ac90a` |
| Private MCP executable | copy of `stub_tools/mediator.py`, SHA-256 `e51f0641907215c9d5a0acb607f967363fc7491fa572a70cfb8701acd2308c2e`, equal to the reviewed source and recorded in the harness containment realization |
| Subject packages | `arms.json`: p65 `7d61d8b7…`, p66 `e6d960a8…`, p70 `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b` (commit `db94a2d…`), each identical to the previously retained tree digests |

The historical v1 frozen profiles in `stage-f-prerun-actual-profile-recheck-2026-09-28/profiles/` were not
modified. The new profiles differ from the reviewed templates only in `profile_id`, `provider_runtime`
(version + binary digest), `reasoning_configuration`, and `provider_managed_unknowns` (the template's
"uncontrolled until frozen" build marker is replaced by exact version/binary binding; backend shard and
serving-revision remain arm-neutral, as in the prior freeze). Both bind `claude-stream-json-v2`,
`claude-code-restricted-sandbox-v1`, strict MCP with server `ssdp70` / `ssdp70-qualification-stdio-v1` /
exactly six tools, and empty MCP for the evaluator.

Native tool surfaces (frozen; init observed them exactly equal in the diagnostic runs below):

- executor (13): `Skill`, `Read`, `Glob`, `Grep`, `Edit`, `Write`, `Bash`, `mcp__ssdp70__issue_locations`,
  `mcp__ssdp70__issue_search`, `mcp__ssdp70__issue_show`, `mcp__ssdp70__issue_create`,
  `mcp__ssdp70__issue_comment`, `mcp__ssdp70__delegate`;
- evaluator (3): `Read`, `Glob`, `Grep`; `mcp_servers: []`.

## Blocking findings

### B1 — the actual profile cannot start: required restricted sandbox is unavailable (§1.8)

Live harness episode through the frozen executor profile (`harness70.py episode --mode probe`, checker-owned
synthetic corpus, `p70` arm) produced `EXECUTION_ERROR` / `NOT_EVALUATED` with runtime message:

> sandbox required but unavailable: … dependencies are missing: socat not installed …
> sandbox.failIfUnavailable is set — refusing to start without a working sandbox.

`bwrap` is present; `socat` is not, and installing it is a host-system change that this task did not
authorize. Claude Code correctly **failed closed** before any model call (this fail-closed behavior is
itself observed live), but it means no containment/escape probe, and therefore no pre-effect
containment demonstration, can run: filesystem/HOME/run-state denial, native-network denial, Unix-socket
denial, external-write mediation, repository/object-store crossing denial and MCP `env -i` credential isolation
remain **unverified**. Sandbox declarations in the realized settings are not evidence without probes.

### B2 — no qualification-only authentication source; the frozen realization cannot authenticate (§1.8 credential policy)

The frozen realization uses a fresh run-owned HOME and denies ambient credentials. It reads a parent
credential only from exactly one of `SSDP70_CLAUDE_CODE_OAUTH_TOKEN`, `SSDP70_ANTHROPIC_API_KEY`,
`SSDP70_ANTHROPIC_AUTH_TOKEN`. None is set. Under the adapter's clean environment the runtime returns
`Not logged in · Please run /login` (`apiKeySource: none`). The only working login on this host is the
user's own OAuth credential file in the host `~/.claude`, which the profile denies by design; it was **not**
copied, exported or otherwise reused, because that would both breach the contract's credential policy and
use a personal credential the task did not authorize for this purpose.

Consequence: no model-driven probe can execute under the exact frozen profile — containment canaries
(filesystem, credential, repository, network, external-write, Unix-socket), ordinary-entry/explicit-root/owner-read,
A4 reviewed system subtypes on live traces, A5 Skill-body binding, evaluator read-only/network/MCP denial,
turn-capped/incomplete termination, and every §6 branch. A required live check that did not execute is not a PASS.

### B3 — three D4 defects observed on the actual runtime (each independently prevents admission)

Observed with diagnostic launches that use the frozen profile's exact command shape but relax only
`sandbox.failIfUnavailable` in a copy of the settings (`diagnostic_init_probe.py`). The launches were
unauthenticated, so no model call and no tool effect were possible. This is **diagnostic, not admission
evidence**; each defect must be re-verified on the repaired profile with a working sandbox and auth source.

1. **`--restricted` hides the project-installed SSDP skills.** Executor init catalog with `--restricted`:
   0 of 7 SSDP skills (only 16 built-in skills). The identical launch without `--restricted`: all 7 SSDP skills
   exactly once (23 skills). The adapter always passes `--restricted`, and the harness installs the arm's skills
   in `project/.claude/skills`. Every executor run would therefore fail `catalog_isolation` (§1.2, catalog/root
   activation, `INADMISSIBLE`), and explicit root activation through `Skill` could not resolve.
2. **The profile requires a native surface the adapter itself suppresses.** The frozen `native_surface_requirements`
   contains `auto_memory_write`, but `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` (adapter environment and settings) makes
   init report `memory_paths: null`. `core70.validate_runtime_observation` then reports
   `runtime did not expose required classified native surface 'auto_memory_write'` for **both** executor and
   evaluator, turning every run into `INADMISSIBLE`.
3. **Realized permission mode differs from the frozen mode and nothing checks it.** Frozen: executor `dontAsk`,
   evaluator `plan`. Observed init `permissionMode: "default"` for both; the runtime states that
   `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` forces default. Effect is likely limited under explicit allowed/disallowed
   tools, but the frozen profile does not describe the realized runtime and `validate_runtime_observation`
   does not compare the observed permission mode.

Positive diagnostic observations (not admission): init `tools` equalled the frozen native surfaces exactly
(13 executor, 3 evaluator); executor `mcp_servers` was exactly `[ssdp70: connected]` under `env -i` stdio launch and
evaluator `mcp_servers` was `[]`; init `claude_code_version` `2.1.284`, model `claude-sonnet-5`;
`messaging_socket_path` is exposed (classified); the private MCP executable digest equalled the reviewed source.

### B4 — custody and withheld-oracle checks cannot be completed (§1.9, §6)

The contract requires fixture-key/answer custody denial to the executor and the §6 known-good/known-broken
branch matrix to be run through the admitted profile using custodian keys/oracles/probes. Access to
`~/ssdp70-fixture-custody` was forbidden for this task, and the earlier record found that material
incomplete. These properties are **UNVERIFIED / BLOCKING**; no proxy (the checker-owned synthetic probe corpus
contains no custody material) was substituted.

## Runner-admission disposition

| Property | Disposition |
| --- | --- |
| §1.1 exact subject/profile identity | **BLOCKED.** Subject/package identity verified (installed package digest equalled arm digest before launch). Profiles frozen with exact bindings. Not admissible: B3.2/B3.3 make the frozen profile and observed runtime disagree; effort is command-bound only. |
| §1.2 fresh arm isolation | **BLOCKED.** Harness created fresh run-owned HOME/temp/control and exactly-one-arm install; runtime catalog check fails under the frozen command (B3.1). Concurrent-pair independence not exercised. |
| §1.3 capability manifest / native surface | **UNVERIFIED through the admitted profile.** Exact tool/MCP equality seen only in diagnostic init (B3); B1 blocks a real launch. |
| §1.4 raw/normalized trajectory | **UNVERIFIED.** Only a one-event failed-launch trace exists (retained). |
| §1.5 raw-to-normalized completeness | **UNVERIFIED** on live traces; the failed-launch map is retained. Unit regressions are supporting only. |
| §1.6 evidence/scoring manifests | **PARTIAL.** Live: qualification mode without an admission record raises `ContractError` before launch and creates no run directory. Missing artifact/oracle/scoring-disposition branches through the actual profile not executed. |
| §1.7 fail-closed states | **PARTIAL.** Live: failed launch (rc 1, API error) → `EXECUTION_ERROR`, `NOT_EVALUATED`, no `ok` surfaced. Incomplete/turn-capped/terminal-missing not exercised. |
| §1.8 containment and side effects | **BLOCKED** (B1, B2). No pre-effect escape probe executed; no external-write mediation demonstrated. |
| §1.9 custody | **UNVERIFIED / BLOCKING** (B4). |
| §1.10 pair scheduling | **NOT EXERCISED** by design. |
| §1.11 evidence/cache provenance | **UNVERIFIED.** No COMPLETE_ADMISSIBLE run exists to perturb. Unit regressions are supporting only. |
| §6 actual-profile oracle-integrity suite | **BLOCKED / UNEXECUTED** (B1, B2, B4). |

Required checks not executed and therefore blocking: all model-driven live probes and the §6 branch matrix as
enumerated under B2/B4, plus incomplete, turn-capped and missing-artifact/oracle live behavior.

## Supporting (non-admission) evidence executed on the same head

Interpreter Python `3.13.14`, PyYAML `6.0.3` (scratch venv). `py_compile` of the affected files: OK.
`test_portable70.py` 17 OK; `test_harness_integration.py` 6 OK; `test_stage_f_integrity_repairs.py` 20 OK;
`test_mcp_stdio.py` 2 OK; `git diff --check` clean. These reproduce the repair record's mechanics claims and
are not runner-admission evidence.

## Commands actually executed

- `git rev-parse HEAD`, `git fetch`/`git ls-remote` on the branch; `claude --version`, binary path and SHA-256.
- Unit suites, `py_compile` and `git diff --check` as above; `prepare_arms70.py --repo . --out <scratch>` (verified
  source and package version stamps).
- `freeze_profiles.py` (writes `profiles/*.frozen.json`); key/capability digests via `core70.load_profile` (`identities.json`).
- Auth feasibility: one-turn `claude -p` under the adapter's clean environment with a fresh HOME (`Not logged in`); one
  ambient-environment one-turn `claude -p` to confirm the host login works in general (feasibility only; not evidence,
  not the frozen realization).
- `harness70.py episode --mode probe … --id PROBE1` through the executor profile (→ B1 failure, retained in `harness-probe-run/`).
- `harness70.py episode --mode qualification …` without an admission record (rejected pre-launch).
- `diagnostic_init_probe.py executor|evaluator` and the `no-restricted` executor variant (→ B3, retained in `diagnostic/`).

Not executed: any model-driven probe, any escape/canary run, evaluator assessment run, the §6 matrix, any custody access.

## Evidence locations

`qualification/ssdp70/stage-f-runner-admission-recheck-v2-2026-09-28/`: `profiles/`, `identities.json`, `arms.json`,
`freeze_profiles.py`, `probe-corpus/` (checker-owned synthetic, no custody data), `harness-probe-run/`
(run-identity, summary, trace, stderr, containment-realization, normalized events/map), `diagnostic/` and
`diagnostic_init_probe.py`. Scratch paths are replaced by `<checker-scratch>`/`<run-tmp>`; trailing blank lines at the end of the captured `stderr` files were trimmed for the repository whitespace check (no content line changed).

## Minimal repair and re-run conditions

1. **Host provisioning (user/operator):** install the sandbox dependency (`socat`; `bwrap` is present) and provision one
   qualification-only auth source (`SSDP70_*`) for the checker session; do not reuse the personal login file.
2. **D4 repair of the adapter/profile:** make the catalog contain each arm's SSDP skills exactly once under the frozen
   command (B3.1); reconcile `native_surface_requirements` with the suppressed auto-memory surface (B3.2); either realize
   the frozen permission mode or freeze and validate the observed one, and make the core compare it (B3.3). Then
   re-freeze profiles from the repaired templates.
3. **Custodian/checker:** complete custodian materialization and give the pre-run checker role/time-scoped access to
   the withheld keys/oracles/probes as the contract §1.9/§6 provides, then run the full escape, entry, termination,
   perturbation and §6 suites through the exact profiles.

## Final outcome

**STOP/BLOCKED / NO-PASS.** The Stage F comparative campaign remains unauthorized.
