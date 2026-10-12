---
kind: independent-stage-f-pre-run-qualification-integrity-recheck
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: STOP/BLOCKED
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_head: 55e5ee94e069acca0ef144db0617a0dcd75d4d81
tooling_implementation: 0be3f979e66d1ea3a51c554bdd70c541e3d22d8a
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
target_runtime: Claude Code 2.1.283 (environment-local, this host)
qualification_campaign_authorized: false
active_serious_challenge: none
evidence_directory: qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/
---

# Protocol 7.0 Stage F pre-run integrity recheck (actual Claude Code profile): STOP/BLOCKED

## Disposition

**STOP/BLOCKED / NO-PASS. Do not begin the comparative 6.5/6.6/7.0 qualification campaign.**

This is a fresh independent pre-run recheck. It uses the environment-local Claude Code runtime as
the actual target runtime. The checker context authored none of the Protocol 7 candidate, the
fixtures, the qualification contract or the Stage F tooling.

No Serious Challenge is raised. The accepted evaluation contract and the portable-core/adapter
architecture are coherent and realizable on this runtime. The blockers are:

- the custodian's withheld material is incomplete;
- the actual Claude realization has D4/environment defects, found only by running the real
  runtime;
- mandatory actual-profile probes could not execute in this environment.

The immutable Protocol 7 candidate `db94a2dfb7fef480f37227eab5c45256e89901b8` was not modified.
`git diff db94a2d..HEAD` touches no `source/`, `dist/`, `orchestrator/`, `README.md` or
`CHANGELOG.md` path. No candidate run, 6.5/6.6 baseline run, comparative scoring or human trial
was started.

## Authority reconstructed independently

The following authorities were reconstructed:

- **Governing workplan.**
  `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md` governs
  under Protocol 6.6.0, targeting 7.0.0. It includes the binding Stage F portable
  execution-profile architecture and the §11 custody split.
- **Controlling evidence contract.**
  `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, specifically §1
  (runner-admission items 1–11, profile-scoped rule) and §6 (runner/harness oracle integrity).
- **Release identities.** `PROTOCOL-RELEASE-STATE.yaml` gives accepted 6.6.0 at `22f4bdba…` and
  historical 6.5.0 at `7f7b5e24…`.
- **Prior records, used as defect input only.**
  - `STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-RECHECK-STOP-BLOCKED-2026-09-28.md` (B1–B7).
  - `STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-RECHECK-REPAIR-2026-09-28.md`, which leaves B1 open by
    design.
- **Reviewed tooling blobs.** These match the repair record exactly:
  - `core70.py` `cef064ea…`
  - `harness70.py` `e81af692…`
  - `assess70.py` `42378844…`
  - `adapters/claude.py` `71ede0d9…`

## What executed

| Check | Realization | Result |
| --- | --- | --- |
| Exact subject resolution | `prepare_arms70.py` from immutable commits; source and package version stamps verified | **PASS.** p65 `7d61d8b7…`, p66 `e6d960a8…`, p70 `7ec95162…` (package tree SHA-256); `arms.json` retained |
| Profile freeze | Executor and evaluator templates frozen to runtime `2.1.283`, model `claude-sonnet-5`, effort `high`; the frozen profile records the actual containment realization | Frozen, **not admitted**. Executor profile key `94b1c505…`, evaluator profile key `90030ec0…` |
| Runtime observation vs. frozen profile | Real `claude -p` stream-json init through `adapters/claude.runtime_observation` and `core70.validate_runtime_observation` | **PASS**: observed `2.1.283` / `claude-sonnet-5`, no errors |
| Catalog contamination (user-level 6.6 skills present in `~/.claude/skills`) | Real init event plus an explicit `Skill` call, `--setting-sources project,local` | **PASS for this realization.** Each SSDP skill appears exactly once. `software-implementation` resolved to the run-local arm package, not the user-level 6.6 copy |
| Explicit root selection | Real `Skill` trace normalized by the actual adapter | `root_selection` start/result carries the verified-install package identity (commit `db94a2d…`, package digest) |
| Actual-runtime normalization completeness | Real traces through `adapters/claude.normalize` and core validators | **FAIL** (A4) |
| T1/T7/T8 observability under explicit root | `core70.validate_claim_observability(..., ['t1-burden'])` on the real trace | **FAIL** (A5): inadmissible |
| Ordinary-entry observability | Same, `['ordinary-entry']` | Not demonstrated: no ordinary-entry live run executed (A6) |
| Evaluator native capability surface | Real `claude -p` with the frozen evaluator command shape | **FAIL** (A3) |
| Qualification mode without admission | Harness `qualification` mode with the frozen profile and the template profile; launch stubbed so no API call could occur | **PASS**: both rejected before launch |
| Mechanics suite | `py_compile`; `unittest test_portable70.py test_harness_integration.py` | **PASS**: 23/23 (mechanics only) |

Evidence stored in `qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/`:

- the frozen, non-admitted profiles;
- `arms.json`;
- the three native stream-json traces, with checker scratch paths replaced by `<checker-scratch>`.

The original trace SHA-256 values before path sanitization were:

- `init-probe.jsonl`: `088dcd12…`
- `skill-probe.jsonl`: `37f472a1…`
- `eval-read-probe.jsonl`: `62c8f793…`

## Blocking findings

### A1 — the custodian's withheld material is incomplete

The designated custody store (environment-local, same host) was inspected. As pre-run checker, the
checker read only its structure, rules, access log and materializer entry point; no key or answer
exists to read. The store has these gaps:

- The corpus materialization stopped partway. Fixture project trees exist, but the materializer's
  own outputs are absent: no corpus `manifest.yaml`, no episode prompts/entries/budgets and no
  `stubs/`.
- `keys/`, `oracles/`, `probes/` and `human-trial/` are **empty**. There are no planted-property
  keys, classification rationale, critical flags, acceptable dispositions, R2 classes/events, owed
  delegate parts, opportunity ledger, deterministic oracles, rubrics, known-good/known-broken
  deliverables or frozen human-trial questions.
- The custody rules name `METADATA-FOR-IMPLEMENTER.md` and `HARNESS-INTERFACE.md`. Neither exists.
- The access log promises a per-session write list, which is also absent.

As a result, none of the following can be checked:

- the withheld classification rationale (the unnamed-class share);
- opportunity exposure and minimums;
- R2 per-class assignment;
- critical-case marking, including the both-arms-miss aggregate-gain counterexample;
- the §6 per-branch known-broken rejection and known-good acceptance;
- the human-trial plan.

The §6 oracle-integrity suite cannot run in any environment until this material exists.

**Minimal repair.** The separate fixture-custodian context completes materialization:

- manifest, prompts and stubs;
- keys, oracles, probes and human-trial material;
- the implementer-visible metadata and interface files;
- the access log's write list.

The checker must not author these. A fresh checker then reruns this gate.

### A2 — no pre-effect containment or custody denial in the actual executor realization

The contract requires containment to be *demonstrated* (§1 item 8, §1 item 9). No such mechanism
exists in the realization:

- `adapters/claude.clean_env()` passes the entire host environment, dropping only `*SESSION*` and
  two Claude keys. The run uses the host `HOME` and ambient credentials and network.
- The adapter writes no sandbox settings. The run-owned project contains only
  `.claude/skills/`, and `--setting-sources project,local` loads nothing else. No OS-level
  sandbox, container or namespace is applied.
- The frozen executor surface allows `Bash(python3:*)` and `Bash(git:*)`. Prefix-matched command
  permission cannot constrain arbitrary interpreter code, so filesystem, network, credential and
  repository crossings are reachable in principle.
- The custody store is readable by the same uid as the executor (mode `0775`, same home).
- `SSDP70_STUB_DIR` and `SSDP70_SIDE_EFFECT_LOG` are executor-writable host paths. The executor can
  therefore write the issue store directly, bypassing the mediating stub, and can forge or erase
  side-effect evidence. This gives the `issue_evidence_store` and `external_mutation`
  `SANDBOX/MEDIATE` classes an unmediated equivalent route.

**Live escape matrix not executed.** A canary-based live escape matrix was prepared. It covered:

- Read, `cat` and Python reads of a same-uid canary;
- a Python write and a `Write` outside the workspace;
- a `git push` to a canary bare repository;
- network access through Python and `git ls-remote`;
- a canary credential file and a canary environment variable.

It was not executed. The session's safety classifier refused to launch a tool-enabled executor
with this profile. The account spend limit then ended further live runs.

The execution would not change the decision. The contract requires demonstrated pre-effect
blocking, and no blocking mechanism exists, so an escape run can only confirm failure.

**Minimal repair.** Run the executor, and separately the evaluator, inside real substrate
containment. Examples: Claude Code sandbox settings with a filesystem allow-list of the project and
package plus network deny, or a container, VM or `bwrap` with a scrubbed environment, no host
`HOME`/credentials and no network namespace. Additionally:

- place stub state and the side-effect log behind a mediating process outside executor-writable
  scope;
- hold custody under a separate uid or host;
- then run the escape matrix above through the admitted profile.

### A3 — the actual native capability surface is wider than, and unclassified by, the capability manifest

The real 2.1.283 init event for the frozen evaluator command shape exposed 23 tools. Besides
`Read`, `Glob` and `Grep`, these include:

- `Artifact`, `ArtifactData` and `ArtifactComments`;
- `SendMessage` and `ListAgents`;
- `RemoteTrigger`, `CronCreate` and `ScheduleWakeup`;
- `PushNotification`, `EnterWorktree`, `Workflow` and `Monitor`;
- `DesignSync`, `ToolSearch` and `TaskStop`.

The init event also exposes a local `messaging_socket_path`.

The adapter passes only `--allowedTools` (pre-approval) and `--disallowedTools` (a partial deny
list). It never sets the exact tool surface, even though `--tools` does restrict it: the tool-less
probe showed `tools: []`.

The capability manifests do not classify these native tools. Some of them are unmediated
equivalents of `DENY` classes: delegation or cross-session messaging, remote service, external
publication or write, and persistent scheduling. The normalizer's unknown-tool failure acts only
after use, which is post-effect.

The executor surface was not observed live (see A6). It is realized with the same adapter pattern
and has the same defect.

**Minimal repair.**

- The adapter launches with an exact `--tools` surface.
- Admission verifies that the init `tools` list equals the profile-declared set.
- The manifest maps every exposed native capability, including cross-session messaging, auto-memory
  writes and any socket, to a semantic class.

### A4 — real 2.1.283 streams cannot reach `COMPLETE_ADMISSIBLE`

Both real traces yield normalization errors: native `system/thinking_tokens` and
`system/post_turn_summary` events "have no reviewed classification". This is correct fail-closed
behavior, but it means every real run on this runtime becomes malformed or inadmissible, so no
known-good branch can be accepted.

**Minimal repair.** Add an explicit, reviewed non-oracle classification for these native subtypes
with completeness-map entries. Add a regression built from the retained real trace.

### A5 — T1/T7/T8 burden observability fails under the mandated explicit root selection

A real `Skill` call returns `Launching skill: …`. The installed `SKILL.md` body arrives as a
separate `isSynthetic` user message. The adapter emits `root_selection` but no `resource_access`
with exact bytes and SHA-256 for the loaded `SKILL.md`.

`validate_claim_observability(['t1-burden'])` therefore reports "no successful exact SSDP-resource
evidence". The T1/T7/T8 logical 6.6 profile requires explicit root selection, and its active-byte
metric counts the whole installed `SKILL.md`. Every T1/T7/T8 run on this adapter is therefore
claim-inadmissible, including the fixed-cost backstop floor.

**Minimal repair.** Normalize the Skill-injected body as a successful `resource_access` for the
installed `SKILL.md`. Bind it to exact file bytes and hash, verified against the injected text or
exact path, and add a regression from the retained real trace.

### A6 — the mandatory actual-profile known-good/known-broken suite did not execute

These probes were not run through the live executor:

- ordinary-entry and owner-read capture;
- incomplete, failed or turn-capped termination;
- cache, profile, core and evaluator perturbations on live evidence;
- catalog contamination under a full run;
- containment escapes;
- withheld oracle branches.

There were three causes:

- A1 left no withheld material to run.
- The safety classifier refused the tool-enabled executor launch.
- The account then reported "hit your individual spend limit" on the next live call.

The evaluator canary-read probe consequently has no result. The prepared mechanics corpus is
checker-owned and synthetic, so even a successful run would support mechanics only. It is not
withheld evidence.

Required unexecuted checks are blocking, not passes.

**Minimal repair.**

1. Repair A1–A5.
2. Restore run budget.
3. Run the complete matrix through the admitted contained profile. Where an operator runs it
   outside this session, grant explicit authorization for the tool-enabled executor.

### A7 — the evaluator realization is not admissible

`EVALUATOR_ADMISSION_CHECKS` requires `read_only_capability_enforcement` and
`credential_network_denial`. Neither holds for the actual evaluator shape:

- **Read-only enforcement.** The native surface includes publish, messaging, scheduling and
  worktree tools (A3).
- **Credential and network denial.** The host environment and `HOME` are inherited (A2). `Read`
  has no path scope beyond the runtime default, and this could not be measured (A6).

**Minimal repair.** Covered by the A2/A3 repairs, applied to the evaluator profile, followed by the
evaluator admission probes.

## Reassessment of prior B1–B7

| Prior | This recheck |
| --- | --- |
| B1: actual-profile/withheld evidence | **Still open.** Split into A1, A2, A6 and A7 above |
| B2: admission fail-open | Closed in mechanics. Qualification refuses without admission, verified here with a real frozen profile |
| B3: per-kind trajectory | Closed in mechanics. Fail-closed on real unknown subtypes, but the real stream cannot yet be admitted (A4) |
| B4: ordinary entry, owner reads, T1/T7/T8 | **Not closed on the actual runtime** (A5). Ordinary entry not demonstrated live (A6) |
| B5: runtime/cache | Runtime observation verified against the real runtime. Live cache perturbation not run (A6) |
| B6: evaluator admission | Gate exists in mechanics. The actual evaluator realization fails its admission premises (A3, A7) |
| B7: evidence/snapshot trust | Closed in mechanics (23/23). Not exercised on live evidence (A6) |

## Custody access by this checker

The checker exercised pre-run-checker role access only:

- a directory structure listing of the custody store;
- `CUSTODY-RULES.md` and `ACCESS-LOG.md`;
- the materializer's `main()`;
- file names of two fixture trees.

No key, oracle, probe or human-trial material existed to read. Nothing from custody is reproduced
here beyond counts and absence.

All live probes used checker-planted canaries. The real credential store was not accessed, and a
probe that would have tested it was withdrawn in favor of a canary. The canary directory was
removed after the review.

## Final outcome

**STOP/BLOCKED / NO-PASS.** The Stage F pre-run integrity gate is not satisfied for the
environment-local Claude Code profile. The comparative 6.5/6.6/7.0 campaign remains unauthorized,
and the Protocol 7 candidate remains unchanged.

The next admissible step is a fresh independent pre-run recheck, after all of the following:

1. The custodian completes A1.
2. D4 repairs A2–A5 and A7 in the adapter, profiles and substrate, without changing the contract
   or the candidate.
3. A run budget and authorization for the contained executor exist.
