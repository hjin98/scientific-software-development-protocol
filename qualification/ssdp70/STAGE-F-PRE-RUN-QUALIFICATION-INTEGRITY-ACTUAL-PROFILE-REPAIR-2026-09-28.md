# Stage F pre-run qualification-integrity actual-profile repair — 2026-09-28

## Status

**IMPLEMENTED — PENDING FRESH INDEPENDENT ACTUAL-PROFILE RECHECK.**

This is an implementation/repair record, not a runner-admission record and not a PASS record.
The comparative Stage F campaign remains unauthorized. The immutable Protocol 7 semantic
candidate `db94a2dfb7fef480f37227eab5c45256e89901b8` is unchanged.

Implementation commit:

`f4206d06c1c5005c8a14c6bb53ae719ecb39044f`

Repair input was
`STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-ACTUAL-PROFILE-RECHECK-STOP-BLOCKED-2026-09-28.md`
at `8e05a7b8920415727e32ce778cdf4737ea59d530`. That record was treated as defect input,
not as authority.

## Reconstructed authority

Governing implementation protocol: SSDP `6.6.0`.

Task authority was reconstructed independently from:

- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`
  (governing `protocol_version: 6.6.0`, target `7.0.0`);
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`,
  especially §1 runner-admission items 1–11 and §6.

The repaired D4 behavior preserves the contract, qualification thresholds, fixtures,
human-trial rules, and Stage G/H semantics. No adapter-specific scoring path or parallel
authority registry was introduced.

Project Engineering Memory was checked. DS-001 (do not substitute semantic/proxy evidence
for the real semantic owner) applies directly: the new synthetic/retained-trace tests prove
mechanics only and are not actual-profile containment or admission evidence.

## Scope and exclusions

Changed scope is only `qualification/ssdp70/eval/`. This record itself is under
`qualification/ssdp70/`.

No files under `source/`, `dist/`, or `orchestrator/` were changed. The Protocol 7
candidate was not modified. The fixture custody store `~/ssdp70-fixture-custody` was not
read, listed, or written. A1 remains the fixture custodian's responsibility.

No comparative campaign was started. No admission PASS evidence was created.

## Repair summary

### A2 — pre-effect containment and custody

The Claude adapter now realizes containment before launch rather than merely declaring it:

- explicit `--restricted`;
- explicit run-owned `--settings` whose control file lives under the harness-private/runtime
  root outside the executor/evaluator working directory;
- fail-closed sandbox startup (`failIfUnavailable: true`);
- unsandboxed command escape disabled;
- native network allowlist empty;
- Unix-socket allowlist restricted to the run-owned qualification mediator socket;
- fresh run-owned HOME/XDG state instead of inherited host HOME;
- explicit environment allowlist plus subprocess environment scrubbing;
- ambient credential-like variables are not inherited and common credential variables are
  denied to sandboxed commands;
- auto-memory, scheduling, Artifact publication, and background-task surfaces are disabled
  in the contained runtime environment;
- strict explicit empty MCP configuration (`--mcp-config ... --strict-mcp-config`) stored
  beside the private settings file, outside the working directory;
- filesystem deny roots cover the harness-private/runtime state, host HOME, `/home`,
  `/root`, `/run/user`, `/proc`, `/mnt`, `/media`, `/srv`, and `/var/tmp`;
- write-deny construction explicitly avoids placing an ancestor of the writable executor
  project in `denyWrite`, so the sandbox does not shadow its own allowed workspace;
- the active settings/MCP control files are outside the restricted file-tool working
  directory, inside the denied private root, and their exact bytes are digest-checked before
  and after launch;
- containment settings and exact bytes are bound into launch identity and a retained
  `containment-realization.json`.

Issue state and the side-effect ledger are now harness-owned state behind a separate
Unix-socket mediator (`stub_tools/mediator.py`). Executor-side `issues.py` and
`delegate.py` receive only the mediator socket path and cannot receive direct stub/log
paths. The mediator alone reads/writes stub issue state and appends side-effect evidence.

### A3 — exact native surface and fail-closed classification

The frozen profiles now declare an exact `native_tools` set and launch with exact
`--tools`:

Executor:

`Skill, Read, Glob, Grep, Edit, Write, Bash`

Evaluator:

`Read, Glob, Grep`

The launch identity must match the frozen list exactly. Runtime `system/init.tools` must
match the declared set; a difference is an error. Every observed runtime capability must
have a capability-manifest classification. Unknown tools/capabilities fail closed.

The retained 2.1.283 runtime capability surface is classified, including interrupt/message
lifecycle capabilities, MCP read/tool metadata, the messaging socket, and auto-memory state.
Cross-session messaging, remote triggers, scheduling, publication, worktrees, delegation,
and other non-required native tools are removed from the exact admitted tool surface and
also listed as disallowed defense-in-depth.

### A4 — real-stream normalization

The Claude normalizer now explicitly classifies retained Claude Code 2.1.283
`system/thinking_tokens` and `system/post_turn_summary` as reviewed non-oracle native
events with completeness-map entries and no normalized semantic event.

Unknown native event types/subtypes remain fail-closed.

A focused regression derives these cases from the retained real traces rather than an
invented trace.

### A5 — explicit-root byte accounting

For a successful `Skill` root selection, a subsequent `isSynthetic` user message is
treated as the runtime-injected SKILL.md body only when all of the following are true:

- a successful logical root selection exists;
- the synthetic payload has the expected base-directory declaration;
- the selected installed `SKILL.md` exists at the bound skills root;
- the injected body exactly equals the installed UTF-8 file bytes.

Only then does normalization emit a successful `resource_access` carrying the exact
resource path, byte count, SHA-256, result content, and package identity.

The retained `skill-probe.jsonl` is used by a focused regression to establish that this
mechanism supplies the exact-byte evidence required by `validate_claim_observability` for
T1/T7/T8. A mismatch fails closed.

### A7 — evaluator realization

The evaluator uses the same pre-effect realization path with evaluator-specific constraints:

- exact `Read, Glob, Grep` native surface;
- no Bash/process or mutation tools;
- empty filesystem `allowWrite`;
- native network denied;
- no mediator socket;
- strict empty MCP configuration;
- fresh run-owned HOME/XDG;
- ambient credentials scrubbed/denied;
- auto-memory/scheduling/publication/background-task surfaces disabled.

A hostile regression asserts the evaluator realization has no write or network/socket
capability in the realized sandbox.

## Focused hostile/retained-trace regression additions

`qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` covers:

- retained 2.1.283 `thinking_tokens` and `post_turn_summary`;
- retained synthetic Skill-injected SKILL.md exact-byte/hash evidence;
- unknown native system subtype fail-closed behavior;
- runtime tool-surface mismatch;
- declared native tool without capability classification;
- host HOME/credential environment leakage;
- launch refusal when containment config is absent;
- direct stub/log path non-exposure and mediator-only access;
- executor sandbox realization without a writable-project/deny-write ancestor conflict;
- private settings/MCP control files outside the native file-tool working directory;
- control-file mutation detection;
- evaluator read-only/network-denied realization.

Existing portable/integration tests were updated only as required by the new profile and
adapter contracts.

## Implementation blob identities at `f4206d06c1c5005c8a14c6bb53ae719ecb39044f`

- `qualification/ssdp70/eval/adapters/claude.py` — `52f20cfcf0621cc15307325c4ebcf50dce80d200`
- `qualification/ssdp70/eval/assess70.py` — `a17ed28faef5d7378202d34c56ab83130eb512ed`
- `qualification/ssdp70/eval/capabilities/claude-evaluator-readonly.json` — `b4f39d045b5a5655d36c9944ef8aead562c9de9a`
- `qualification/ssdp70/eval/capabilities/claude-headless.json` — `3055dd4acbcc90fc1b19689632ec2ba10211d2e0`
- `qualification/ssdp70/eval/core70.py` — `31af182c467e50bc3a4d946c71654213d02c950c`
- `qualification/ssdp70/eval/harness70.py` — `a92110e5c91c40fff1b0ee96fb4ccb5e4f7e3c56`
- `qualification/ssdp70/eval/profiles/claude-evaluator-readonly.template.json` — `3faa5f6bfea1d73142c07531e3b9ec668eff2f26`
- `qualification/ssdp70/eval/profiles/claude-headless.template.json` — `2328b8fc899b16bb791dd19222cf7a65a78f3da2`
- `qualification/ssdp70/eval/stub_tools/delegate.py` — `8847efed0e50634162ae8d4728b3d6a39ffc9e35`
- `qualification/ssdp70/eval/stub_tools/issues.py` — `47762f947d8cb6b22e5cb209d8942268233eaba5`
- `qualification/ssdp70/eval/stub_tools/mediator.py` — `b257322b208d235c94a41ec7579f1cbf238bbfba`
- `qualification/ssdp70/eval/test_harness_integration.py` — `10a5be8da90d96b266987e4b6bcf06a8f63424e0`
- `qualification/ssdp70/eval/test_portable70.py` — `8c574c9dcab0405445c5a817c9dcaed0869ddddf`
- `qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` — `f810ca015b078f34a5bb539cb39536007fb188c3`

The final implementation identity supersedes the earlier intermediate repair identities
`3afae4fa...` through `112f75a7...`. The final D4 reconciliation in
`f4206d06...` removes a writable-project `denyWrite` ancestor conflict and relocates the
active settings/MCP control files outside the executor/evaluator working directory. Those
post-intermediate corrections are part of the implementation being handed to the fresh
checker.

## Checks executed and unavailable

### Executed

- Reconstructed the governing workplan/contract authority independently.
- Compared `8e05a7b8920415727e32ce778cdf4737ea59d530...f4206d06c1c5005c8a14c6bb53ae719ecb39044f`
  through the repository API. The changed-file set is exactly the 14 files under
  `qualification/ssdp70/eval/` listed above plus this repair record under
  `qualification/ssdp70/`; no `source/`, `dist/`, or `orchestrator/` file changed.
- Scanned the final comparison patch through the repository API for added-line trailing
  whitespace: zero findings.
  This is supplementary evidence only; it is **not** reported as execution of
  `git diff --check`.
- Inspected the retained real 2.1.283 init/skill/evaluator traces used by the new
  regressions.
- No live `claude -p` qualification/campaign execution was performed.

### Unavailable in this implementation session — NOT PASSED

The required executable checks below could not be run against an exact checkout in this
agent's code-execution container:

- `python -m py_compile ...`
- full `test_portable70.py`
- full `test_harness_integration.py`
- `test_stage_f_integrity_repairs.py`
- `git diff --check`

Reason: all code execution for this implementation session is constrained to the provided
container. That container has no repository checkout and cannot resolve or connect to
GitHub; clone/remote probes failed at the network/DNS boundary. Repository reads/writes were
available only through the connected GitHub repository API, which does not provide a shell
or workflow-dispatch execution surface. No proxy/synthetic execution is substituted for the
missing checks.

Therefore these checks are unresolved evidence obligations for the next executable
environment. Their non-execution is not a PASS and must not be converted into admission
evidence.

## Remaining gate

A fresh independent checker must now:

1. execute `py_compile`, `test_portable70.py`, `test_harness_integration.py`,
   `test_stage_f_integrity_repairs.py`, and `git diff --check` against the exact repair
   descendant;
2. independently realize the actual Claude Code 2.1.283 executor/evaluator profiles and
   execute the contract §6 actual-profile probes, including hostile containment,
   credential/network, tool-surface, completeness, and evaluator read-only checks;
3. verify that runtime `system/init.tools` equals each declared exact set and that every
   exposed native capability is classified or absent;
4. verify actual substrate denial of direct stub/log/custody access rather than accepting
   settings text as proof;
5. verify exact Skill-injection byte accounting on the real retained/runtime stream;
6. obtain/verify A1 fixture-custodian evidence separately;
7. issue the runner-admission result independently.

Until that independent evidence exists, the Stage F comparative campaign remains blocked
and no PASS admission claim is authorized.

## Scientific/evidence completion

This repair produced no comparative scientific result, no candidate-vs-control result, and
no human-trial result. It changed qualification evidence machinery only. The consequential
choice was to use substrate containment plus a harness-owned mediator rather than an
adapter-specific scoring path; that choice is bound to the governing workplan and
qualification contract. Synthetic tests and retained-trace normalization tests are
mechanics evidence only.

No selection among scientific result variants occurred. No Serious Challenge to the
governing D1/D2/D3/qualification authority was found. The unresolved evidence is the
unexecuted local regression suite plus the intentionally independent actual-profile
admission recheck described above.
