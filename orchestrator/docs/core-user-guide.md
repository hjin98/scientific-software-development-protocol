# SDP Orchestrator Core — user guide

`sdp-orchestrator-core` turns "which Protocol prompt do I need right now, filled
in correctly for this repository?" into one command. It resolves everything that
is mechanically knowable — repository, candidate commit, governing workplan,
compatible Protocol profile, and prompt context — and *requires* the things that
are genuinely your decision instead of leaving editable placeholders behind.

Core works alone. It has no history database, no agent runner, no model catalog,
and no scheduler, and it does not need them.

---

## 1. Install

```bash
pip install sdp-orchestrator-core          # Python 3.11+
pip install "sdp-orchestrator-core[clipboard]"   # optional --copy support
sdp doctor
```

`sdp doctor` reports readiness without importing extension code, touching the
network, or modifying anything.

---

## 2. Configure

Configuration is one TOML file. Its default location comes from `platformdirs`
(`~/.config/sdp-orchestrator/config.toml` on Linux); `--config` overrides it.

```toml
schema_version = 1

[core]
default_project = "mdstats"      # optional
default_prompt_mode = "web"      # optional; the built-in default is web

[projects.mdstats]
repo = "/absolute/path/to/mdstats"
protocol_profile = "sdp-protocol-5.16"
default_prompt_mode = "web"      # optional, per project
remote_name = "origin"           # optional; a remote *name*, never a credential URL

[protocol_sources."sdp-protocol-5.16"]
local_root = "/path/to/software-development-protocol"   # optional
allow_remote = false                                    # default
remote_repository = "https://github.com/hjin98/software-development-protocol"
remote_ref = "<explicit evidence-backed ref>"           # required if allow_remote

[extensions."some.extension"]
# extension-owned data; Core preserves it but does not interpret it
```

Core-owned sections are **closed**: an unrecognized key is rejected. That is also
why API tokens and passwords have no home in this file — use your existing Git
credential helper instead. A `repo` or `remote_repository` URL containing
credentials is rejected outright.

`[extensions."<ns>"]` is the one open section. Namespaces belonging to
extensions you have not installed are preserved verbatim and reported by
`sdp doctor` as inactive. They never affect project, preparation, or prompt
identity.

### Which project?

When `--project` is omitted:

```
the unique configured project whose worktree contains the current directory
  -> [core].default_project
  -> the sole configured project
  -> core.project.ambiguous / core.project.not_found
```

There is no fuzzy matching. Ambiguity is reported, never guessed.

---

## 3. Render a prompt

```bash
sdp design --task "split the ingest pipeline from the storage layer"
sdp implementation
sdp review
sdp verification --input VERIFICATION_SCOPE="the 2.4 release claims"
sdp prompt closeout --workplan PROTOCOL-5.16-EXAMPLE
```

The prompt goes to **stdout only**, and only once the complete artifact exists.
Diagnostics go to stderr as redacted JSON with a nonzero exit status, so piping
is always safe:

```bash
sdp implementation | pbcopy
sdp implementation > prompt.txt
sdp implementation --copy          # additive; never blocks the prompt
```

Exit statuses: `0` success, `2` a structured Core problem (JSON on stderr),
`1` an unexpected internal failure.

### Commands

| Command | Purpose |
| --- | --- |
| `sdp baseline` … `sdp closeout` | render that stage's prompt |
| `sdp prompt <stage>` | the same, by stage key or profile alias |
| `sdp projects [--workplans]` | list configured projects and their workplan catalog |
| `sdp capabilities` | capability status (metadata-only discovery by default) |
| `sdp doctor` | readiness report with no hidden loading, network, or mutation |

### Options

| Option | Meaning |
| --- | --- |
| `--project <key>` | configured project key |
| `--workplan <id-or-path>` | exact workplan id or exact repository-relative path |
| `--prompt-mode local\|web` | where the prompt will be consumed |
| `--config <path>` | explicit configuration file |
| `--remote-mode <mode>` | `local_only`, `use_cached_remote` (CLI default), `refresh_remote` |
| `--task <text>` | Design-stage task |
| `--input NAME=VALUE` | a declared profile INPUT (repeatable) |
| `--copy` | additionally copy to the clipboard |

---

## 4. Two things called "mode" — and they are not the same

This distinction is deliberate and worth reading twice.

**`--prompt-mode` (`local` / `web`)** answers *where the prompt will be pasted*.
It changes only the repository context Core renders into the prompt.

**`EXECUTION_MODE` (`AUTO_EXECUTE` / `REPORT_ONLY` / …)** is a canonical SDP
prompt input. It answers *what the receiving agent is authorized to do*.

Changing one never changes the other:

```bash
sdp implementation --prompt-mode web                      # EXECUTION_MODE stays AUTO_EXECUTE
sdp implementation --input EXECUTION_MODE=REPORT_ONLY     # prompt mode is unchanged
```

There is a second, similar separation. Core's **render source** is where Core
read the canonical prompt text (a packaged snapshot, a configured local
checkout, or an explicitly permitted remote). The canonical **`PROTOCOL_SOURCE`**
input tells the receiving agent how to find SDP skills, and defaults to
`AUTO_LOCAL_FIRST`. A local render-source path therefore never appears in a
prompt — including a web prompt — merely because Core happened to read from it.
`PROTOCOL_REF` is bound mechanically to the governing Protocol contract and
cannot be overridden.

---

## 5. Local vs web: what each prompt may contain

**Local mode** may reference your authorized worktree: absolute path, branch or
detached HEAD, commit, and whether the tree is clean.

**Web mode** renders only the sanitized remote repository, the target branch, and
the exact candidate commit — and it renders that only when it can be truthful.
Web mode refuses, rather than guessing or silently downgrading to local, when:

| Situation | Reported as |
| --- | --- |
| the worktree has uncommitted changes | `core.prompt.mode_invalid` |
| local and remote are known to diverge | `core.remote.stale` |
| no evidence establishes that the target exists | `core.remote.target_unavailable` |
| the branch is absent on the remote | `core.remote.target_unavailable` |
| HEAD is detached | `core.remote.target_unavailable` |
| the remote is a path or `file://` URL | `core.remote.local_only` |
| several remotes and none is selected | `core.remote.unavailable` |

Target *existence* must be known; only *freshness* may be cached, and cached
freshness is labelled as such in the prompt.

Web prompts never automatically carry local paths, credential-bearing remote
URLs, ambient environment values, credential-helper output, or private
orchestrator state. Text you supply yourself — `--task`, `--input` — is
intentional prompt content and is rendered as written. Core does not pretend to
run a general secret scanner over your own words.

### Remote observation

Observation never mutates your repository: no fetch, no pull, no ref writes, not
even an opportunistic index refresh.

| `--remote-mode` | Behaviour |
| --- | --- |
| `local_only` | repository configuration only; nothing about the remote side |
| `use_cached_remote` | reads existing remote-tracking refs; no network |
| `refresh_remote` | one bounded, noninteractive, read-only `git ls-remote` |

The CLI defaults to `use_cached_remote` — enough to tell whether a web target
exists, without touching the network. The programmatic API defaults to
`local_only`.

---

## 6. Workplans and required inputs

Core resolves the governing workplan per stage. Selection is exact — by workplan
id or repository-relative path, by a `target_branch` binding matching the current
branch, or because exactly one active workplan exists. Filename similarity and
modification time are never evidence.

| Stage | Workplan policy | Required user input |
| --- | --- | --- |
| `baseline` | optional explicit only | `BASELINE_SCOPE` |
| `design` | optional explicit only | `--task` |
| `implementation` | required (resolved) | — |
| `review` | required (resolved) | — |
| `verification` | optional explicit only | `VERIFICATION_SCOPE` |
| `stabilization` | optional explicit only | `STABILIZATION_SCOPE` |
| `alignment` | exact selector required | `UPSTREAM_ACCEPTED_WORK` |
| `health-audit` | `--workplan` rejected | `AUDIT_SCOPE` |
| `closeout` | optional exact binding | `COMPLETED_WORK` unless the selected plan supplies it |

Design with no `--workplan` is new-task Design: it will **not** adopt an
unrelated sole active workplan. A `--workplan` passed to a stage that disallows
one fails rather than being ignored.

Documents sharing a `workplan_id` are collapsed only through explicit
`parent_workplan` / `supersedes_revision` evidence. Where that evidence does not
single one out, Core reports `core.workplan.ambiguous`; the exact path still
works.

A governing workplan for Implementation, Review, or Alignment must declare a
supported `protocol_version`. A missing or unsupported version fails; it is never
silently reinterpreted under a newer profile.

---

## 7. The result footer

Every rendered prompt asks for an ordinary human-readable response **followed by
exactly one terminal, uniquely marked JSON footer**:

```
<<<SDP_STAGE_RESULT_V1
{ "schema_version": 1, "run_id": "...", "prompt_fingerprint": "sha256:...",
  "stage": "implementation", "outcome": "complete", ... }
SDP_STAGE_RESULT_V1>>>
```

Extraction rule: the **last** line equal to the begin marker starts the footer;
the next line equal to the end marker ends it. Ordinary prose may surround it.
Unrecognized additional fields are permitted and ignored.

The prompt never requests hidden reasoning. Core renders this request but does
not parse or store the response; that is Tracker's job in a later module.

Identity is versioned and reproducible. With a fixed `run_id` and unchanged
material state, the same command produces byte-identical output. Wall-clock
timestamps and unrelated extension configuration do not perturb it.

---

## 8. Extensions

Extensions are discovered through exactly one Python entry-point group,
`sdp_orchestrator.extensions.v1`. There is no directory scanning and no
repository-loaded plugin path.

**Installed extension code is trusted in-process code — Core does not sandbox
it.** What Core does guarantee is that `sdp doctor` and `sdp capabilities`
default to metadata-only discovery: they read installed entry-point metadata
without importing provider code, and therefore report extensions as
*discovered / not loaded* rather than claiming capabilities or health they never
observed. Use `--load-extensions` to actually load providers.

A failed or incompatible optional extension disables itself and its dependents;
healthy Core services keep working. Events carrying prompt text are delivered
only to sinks that subscribed to that event type by name, and a failing sink
cannot invalidate a successful render.

---

## 9. What Core deliberately does not do

No run history or `sdp status`/`next`/`ingest`/`graph`. No agent execution,
sessions, or worktree leases. No model, backend, or benchmark catalogs. No quota
meters or scheduling. No daemon. No repository-local orchestrator state. Those
belong to the Tracker, Adapter, and Scheduler modules.

---

## 10. Repository layout

Every orchestrator-owned implementation, test, fixture, script, package, and
documentation file lives under `orchestrator/`. Repository-level CI may invoke
commands under `orchestrator/`, but hosts no orchestrator logic. Protocol source
under `source/` and workplans under `workplans/` are inputs, not alternate
homes for orchestrator code.

```
orchestrator/
  docs/          architecture.md, core-user-guide.md
  packages/core/ pyproject.toml, src/sdp_orchestrator/core/, tests/
  scripts/       snapshot generation, test runner
```

## 11. Development

```bash
pip install -e orchestrator/packages/core -r orchestrator/packages/core/requirements-dev.txt
python orchestrator/scripts/run_core_tests.py            # parallel, sized to the machine
python orchestrator/scripts/generate_protocol_snapshot.py --check
```

The packaged Protocol snapshot under
`src/sdp_orchestrator/core/resources/protocol/` is generated from
`source/shared/references/development-workflow-prompts.md` and is never edited by
hand; `--check` proves the committed copy matches canonical source.
