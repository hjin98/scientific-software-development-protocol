---
kind: qualification-diagnostic-probe
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: development-data-not-qualification-evidence
---

# Runtime command-activation probe

**Question.** Does each runtime's explicit skill command load the skill itself, before the model's first request and independently of model choice? The stakeholder made deterministic command activation the supported usage (`STAKEHOLDER-DECISION-2026-10-04-PROTOCOL-7.0-DETERMINISTIC-ACTIVATION-AND-ACTIVATION-QUALIFICATION.md`).

**Answer.** It depends on the runtime and on the mode.

| Runtime and mode | Command | Runtime loads the skill? | Evidence |
|---|---|---|---|
| Claude Code 2.1.289, print (`-p`) | `/zebra-canary` | **Yes** | With every tool disabled (`--tools ""`), the reply began with the canary token; the control without the command did not. |
| OMP, RPC mode (`--mode rpc`, the session path behind the interactive UI) | `/skill:zebra-canary` | **Yes** | The runtime injected a `custom` message, `[IMPORTANT: User invoked the "zebra-canary" skill; follow its instructions. Full skill below.]`, followed by the skill body and skill directory, before the model ran. The token appeared, including with `--no-tools`. |
| OMP, print mode (`-p`, used by the Stage 7 adapter) | `/skill:zebra-canary` | **No** | The command reached the model as literal text. With the read tool available, the model *chose* to `read skill://zebra-canary` and then complied. With tools disabled, it answered "No skill `zebra-canary` is available." |
| Codex CLI 0.160.0, `codex exec` | `$zebra-canary` | **No** | The skill was discovered (it was listed), but the command was not expanded: input tokens were unchanged apart from the prompt. Asked to avoid commands, the model ignored the skill. Otherwise it chose to `cat .agents/skills/zebra-canary/SKILL.md` and still did not follow it. |

**Not tested:** the interactive TUIs of Codex and Claude Code, and Codex with other models. Claude Code print mode was deterministic, but its interactive slash command was not run here.

## Design

- **Canary skill.** `zebra-canary`. Its description restricts it to "zebra stripe genetics", so no model should choose it for the test prompt. Its body says that, when active, the first reply line must be `ZC-7Q4-ACTIVE`.
- **Prompt and controls.** Prompt: "What is 2+2?" with the runtime's command prepended. Controls: no command, and (for OMP) prose "Use the zebra-canary skill."
- **Activation criterion.** Activation counts as **runtime-deterministic** only if the token appears with tools disabled, or with no model tool call reading the skill.
- **Isolation.**
  - OMP ran with a temporary `HOME` holding only the canary skill. A first attempt under the operator's own OMP home was contaminated by user MCP tools and project skill directories that OMP did not discover; it is discarded.
  - Claude Code ran with `--setting-sources project,local` in a fresh git workspace.
  - Codex used the operator's configuration.
- **Models.** OMP `deepinfra/zai-org/GLM-5.3-Flash` with thinking off; Claude Code `claude-haiku-4-5-20251001`; Codex `gpt-6.1-sol` (operator default).
- **Repetitions.** One run per cell (OMP RPC twice). The deterministic results come from runtime code paths, not model choice. The non-deterministic results only need to show one non-activation each.

## Consequences

1. **Deterministic activation is a property of the runtime and mode.** A profile can claim the deterministic stratum only after it has shown, through its exact adapter, that the runtime loads the skill.
2. **The Stage 7 OMP adapter's print mode does not qualify.** Either the adapter moves to RPC mode, or the harness injects the entrypoint itself. If it injects, it should reproduce OMP's own RPC delivery: a pre-model message carrying the invocation notice, the full skill body and the skill directory. Then harness injection matches what a user's command produces in that runtime.
3. **Codex `exec` gives no deterministic command path.** A Codex profile would need harness injection, or an interactive path that has been shown to inject. The user guidance "`$skill-name` in Codex" is therefore only as reliable as the Codex mode in use. The README wording should be qualified accordingly.
4. **Activation and compliance are separate.** In Codex, the model read the canary skill and still did not follow it. Delivery is necessary but does not guarantee conformity; the M07 doctrine-loaded probe showed the same for SSDP.

## Record

- **Probe root:** `/home/samjin/ssdp70-omp-stagef/probes/RUNTIME-COMMAND-ACTIVATION-20261004T142513Z/`. All raw streams are retained: `omp-iso*`, `omp-rpc-*`, `cc-*` and `codex-*`, plus the discarded contaminated `omp-json-*` and `omp-print-*`.
- **Cost:** Claude Code about $0.03; OMP Flash negligible; Codex on the operator's plan.
- **Scope:** no qualification fixture, key or frozen tree was used.
