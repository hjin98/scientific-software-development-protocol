# Stage F pre-run qualification-integrity actual-profile repair — 2026-09-28

## Status

**STOP/BLOCKED — A2 EXECUTOR CONTAINMENT IS NOT REALIZABLE FOR THE RETAINED LINUX/WSL CLAUDE CODE 2.1.283 ACTUAL PROFILE WITH THE CURRENT NATIVE-SANDBOX MEDIATOR TRANSPORT.**

This is an implementation/repair record, not a runner-admission record and not a PASS record.
The comparative Stage F campaign remains unauthorized. The immutable Protocol 7 semantic
candidate `db94a2dfb7fef480f37227eab5c45256e89901b8` is unchanged.

Final implementation commit for this repair attempt:

`6e9403820791d8ea20b4c3ec9406434752a343d4`

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

The contract requires pre-effect containment, no unmediated escape route for a denied
semantic capability, raw/evidence completeness, exact execution-profile realization, and
fail-closed treatment when a required property cannot be enforced. No adapter-specific
scoring path or parallel authority registry was introduced.

Project Engineering Memory was checked. DS-001 applies directly: settings text or synthetic
mechanics tests cannot substitute for the substrate enforcement owned by the actual
execution profile.

## Scope and exclusions

Changed scope remains only `qualification/ssdp70/eval/` plus this repair record under
`qualification/ssdp70/`.

No files under `source/`, `dist/`, or `orchestrator/` were changed. The Protocol 7
candidate was not modified. The fixture custody store `~/ssdp70-fixture-custody` was not
read, listed, or written. A1 remains the fixture custodian's responsibility.

No comparative campaign was started. No admission PASS evidence was created.

## Implemented repairs

### A3 — exact native surface and fail-closed classification

The Claude adapter launches from the frozen profile's explicit `native_tools` through
`--tools`, retains the allowed/disallowed permission surface, records launch identity, and
validates the runtime `system/init.tools` surface against the declared set. Duplicate,
missing, extra, or unclassified native tools fail closed.

The retained 2.1.283 native runtime capabilities, messaging socket, MCP capability metadata,
and auto-memory surface are classified in the capability manifests. Native tools not needed
for the qualification profile — including cross-session messaging, remote triggers,
scheduling, publication, worktrees, delegation, and related surfaces — are excluded from
the declared tool set and defense-in-depth disallowed.

### A4 — retained real-stream normalization

The normalizer explicitly classifies retained Claude Code 2.1.283
`system/thinking_tokens` and `system/post_turn_summary` as reviewed non-oracle events.
Retained `rate_limit_event` is also explicitly classified as benign metadata. Unknown
native event types/subtypes remain fail-closed.

Focused regressions are based on the retained real traces under
`stage-f-prerun-actual-profile-recheck-2026-09-28/native-traces/`.

### A5 — explicit-root byte accounting

After a successful `Skill` root-selection result, a subsequent `isSynthetic` user message
is accepted as the injected `SKILL.md` body only when the installed skill is available and
the injected UTF-8 body exactly equals the installed `SKILL.md` bytes.

The resulting successful `resource_access` binds the installed resource path, byte count,
SHA-256, package identity, result reference, and exact injected content. The retained
`skill-probe.jsonl` regression verifies that this evidence satisfies the T1/T7/T8
claim-observability mechanics only when the byte identity is real.

### A7 — evaluator realization

The evaluator profile uses the same private settings/MCP-control path and scrubbed
environment but has only `Read, Glob, Grep`, no Bash/process or mutation tool, no mediator
socket, empty `allowWrite`, empty native network domain allowance, and no Unix-socket
allowance. This implementation remains subject to fresh independent actual-profile proof;
this repair record does not admit it.

## A2 — blocker discovered during continuation

The interrupted implementation moved stub issue state and the side-effect ledger behind a
harness-owned Unix-domain-socket mediator. The executor receives only the mediator socket
path; it does not receive direct stub/log paths. This is the correct ownership direction,
but the retained actual profile is Linux-shaped: the retained Claude Code 2.1.283 traces
expose host paths under `/home/...` and a runtime cross-session messaging socket under
`/run/user/1000/cc-socks/...`.

The executor therefore needs two properties simultaneously:

1. permit connection to exactly the qualification-owned mediator socket so issue/delegate
   stand-ins work; and
2. deny other Unix-domain-socket routes, including the runtime messaging socket, so denied
   delegation/network/external-mutation classes have no unmediated equivalent escape route.

The native Claude Code sandbox cannot supply that pair on Linux/WSL: path-selective
`sandbox.network.allowUnixSockets` enforcement is not available there. Permitting all Unix
sockets would make the profile weaker than its declared DENY/SANDBOX-MEDIATE semantics and
would violate the contract's pre-effect containment requirement. Denying all Unix sockets
would also disable the required qualification mediator.

No independently isolated outer container/VM/mount namespace or alternate mediated
transport is present in the current Stage F harness. The property is therefore not
realized on the retained Linux/WSL profile and must not be approximated.

Commit `6e9403820791d8ea20b4c3ec9406434752a343d4` makes this failure explicit and
fail-closed:

- executor containment that requires the path-selective mediator now refuses realization on
  non-macOS native-sandbox substrates before Claude is launched;
- the executor profile records the mediator-transport limitation;
- the capability manifest no longer implies that broad Unix-socket access is an admissible
  realization;
- a hostile regression asserts Linux rejection rather than treating a settings document as
  proof of substrate enforcement.

The evaluator has no mediator requirement and can keep all Unix sockets denied; this A2
blocker is specifically the executor mediator realization.

## Focused and hostile regression coverage present in the tree

`qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` contains regressions for:

- retained 2.1.283 `thinking_tokens` and `post_turn_summary`;
- retained synthetic Skill-injected `SKILL.md` exact-byte/hash evidence;
- unknown native system subtype fail-closed behavior;
- runtime tool-surface mismatch;
- declared native tool without capability classification;
- host HOME/credential environment leakage;
- multiple/ambient authentication rejection and explicit qualification-only auth;
- launch refusal when containment config is absent;
- direct stub/log path non-exposure and mediator-only ownership;
- executor sandbox-control-file placement and mutation detection;
- evaluator read-only/network/socket denial mechanics;
- missing required classified native surface;
- Linux executor refusal when the qualification mediator would require path-selective
  Unix-socket access that the native sandbox cannot enforce.

These are mechanics tests. They are not actual-profile containment or runner-admission
evidence.

## Blob identities at implementation commit `6e9403820791d8ea20b4c3ec9406434752a343d4`

- `qualification/ssdp70/eval/adapters/claude.py` — `d5f8e040dbd2641ca430c9a1b8f2db48afb3e939`
- `qualification/ssdp70/eval/assess70.py` — `a17ed28faef5d7378202d34c56ab83130eb512ed`
- `qualification/ssdp70/eval/capabilities/claude-evaluator-readonly.json` — `b4f39d045b5a5655d36c9944ef8aead562c9de9a`
- `qualification/ssdp70/eval/capabilities/claude-headless.json` — `88de7990d6044ed8217a3e42fbbcc1e206d7b474`
- `qualification/ssdp70/eval/core70.py` — `31af182c467e50bc3a4d946c71654213d02c950c`
- `qualification/ssdp70/eval/harness70.py` — `a92110e5c91c40fff1b0ee96fb4ccb5e4f7e3c56`
- `qualification/ssdp70/eval/profiles/claude-evaluator-readonly.template.json` — `3faa5f6bfea1d73142c07531e3b9ec668eff2f26`
- `qualification/ssdp70/eval/profiles/claude-headless.template.json` — `503172ec884e7f896e9c4768e7e90173ebdadf8d`
- `qualification/ssdp70/eval/stub_tools/delegate.py` — `8847efed0e50634162ae8d4728b3d6a39ffc9e35`
- `qualification/ssdp70/eval/stub_tools/issues.py` — `47762f947d8cb6b22e5cb209d8942268233eaba5`
- `qualification/ssdp70/eval/stub_tools/mediator.py` — `b257322b208d235c94a41ec7579f1cbf238bbfba`
- `qualification/ssdp70/eval/test_harness_integration.py` — `10a5be8da90d96b266987e4b6bcf06a8f63424e0`
- `qualification/ssdp70/eval/test_portable70.py` — `8c574c9dcab0405445c5a817c9dcaed0869ddddf`
- `qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` — `59f115ac58771515bc65bd71fe60cea95f82cb67`

## Checks executed and unavailable

### Executed

- Reconstructed the governing workplan/contract authority independently.
- Inspected the retained Claude Code 2.1.283 native traces used by the A4/A5 regressions;
  no fixture-custody store access was performed.
- Compared
  `8e05a7b8920415727e32ce778cdf4737ea59d530...6e9403820791d8ea20b4c3ec9406434752a343d4`
  through the repository API. The changed-file set is confined to
  `qualification/ssdp70/eval/` plus this repair record; no `source/`, `dist/`, or
  `orchestrator/` file changed.
- Reviewed current Claude sandbox behavior relevant to Unix-domain-socket enforcement and
  reconciled the profile to fail closed where the substrate cannot realize the declared
  boundary.
- No live `claude -p` qualification/campaign execution was performed.

### Unavailable in this implementation session — NOT PASSED

The executable checks below could not be run against an exact checkout in this agent's
code-execution container:

- `python -m py_compile ...`
- full `test_portable70.py`
- full `test_harness_integration.py`
- `test_stage_f_integrity_repairs.py`
- `git diff --check`

Reason: this implementation session's code-execution container has no repository checkout
and cannot resolve/connect to GitHub. Repository reads/writes are available through the
connected GitHub repository API, which does not provide a shell execution surface. No
synthetic/proxy execution is substituted for these missing checks.

The new Linux fail-closed hostile test is present in the implementation but is **not**
reported as executed.

## Remaining gate

Stage F remains blocked. Before a fresh independent actual-profile checker can even attempt
runner admission for this executor profile, the qualification tooling needs one of these
owning-layer realizations without weakening the contract:

1. an independently enforced outer container/VM/bwrap/mount/network boundary that allows
   only the run-owned project plus required runtime/package reads and only the
   qualification-owned mediator communication route while excluding host/runtime sockets;
   or
2. an alternate mediator transport whose access can be narrowly enforced on Linux/WSL
   without opening an unmediated equivalent route.

After that implementation, an executable environment must run `py_compile`, the complete
portable/integration/integrity regression suites and `git diff --check`. Only then may a
fresh independent checker perform the §6 actual-profile probes, obtain A1 separately, and
issue runner-admission evidence.

Until those conditions are met, the Stage F comparative campaign remains blocked and no
PASS admission claim is authorized.

## Scientific/evidence completion

This repair produced no comparative scientific result, no candidate-vs-control result, and
no human-trial result. It changed qualification evidence machinery only. A3/A4/A5 and the
evaluator-side A7 mechanics are implemented, but A2 cannot be realized for the retained
Linux/WSL executor with the current native-sandbox Unix-socket mediator. The correct outcome
is therefore **STOP/BLOCKED**, not implemented-pending-recheck.
