# Stage F pre-run qualification-integrity actual-profile repair — 2026-09-28

## Status

**IMPLEMENTED — PENDING FRESH INDEPENDENT ACTUAL-PROFILE RECHECK**

This is an implementation/repair record, not a runner-admission record and not a PASS record.
The comparative Stage F campaign remains unauthorized. The immutable Protocol 7 semantic
candidate `db94a2dfb7fef480f37227eab5c45256e89901b8` is unchanged.

Starting branch head:

`5a5fcd2332fbac5a1972fcd0921aabc024bbc96d`

Stdio-MCP implementation commit:

`303ead02e91c923fec991cc447f8b892b7fee88a`

Implementation tree:

`5d29f4869c111c29fd1a31a29dd195c9ae135407`

The prior STOP record was treated as defect input, not as authority.

During this implementation session the branch concurrently advanced from the requested start head to
`75841d5b546bca0f470786c0670447bbb7a4ab0e` (`Replace Stage F socket mediator with stdio MCP`).
That commit was inspected rather than overwritten. The final implementation commit
`303ead02e91c923fec991cc447f8b892b7fee88a` is a fast-forward child of that concurrent commit and
preserves its deletion of the obsolete `stub_tools/issues.py` and `stub_tools/delegate.py` files while
hardening two remaining containment properties: the MCP executable is now run-owned/private, and its
subprocess environment is started from `env -i` rather than inheriting Claude parent credentials.

## Reconstructed authority

Governing implementation protocol: SSDP `6.6.0`.

Authority was reconstructed independently from:

- repository `AGENTS.md`;
- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`;
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`,
  especially §1 runner-admission items 1–11 and §6.

The portable core remains authoritative for execution-profile identity, semantic capability
classification, normalized evidence, manifests and scoring inputs. The runtime adapter owns
native realization and translation only. This repair does not introduce an MCP-specific
scoring path, evidence authority, threshold, fixture rule, human-trial rule, or Stage G/H
semantic rule.

## Scope and exclusions

The final reconciliation commit changes only files under `qualification/ssdp70/eval/` and preserves the concurrent commit's removal of the two obsolete stub CLI files.
No files under `source/`, `dist/`, or `orchestrator/` changed. The qualification
contract, immutable Protocol 7 candidate, thresholds, fixtures, human-trial rules, and Stage
G/H semantics were not modified.

The fixture-custody store `~/ssdp70-fixture-custody` was not read, listed, or written.
No comparative campaign was started and no admission PASS evidence was created.

## Implemented A2 replacement — qualification-owned stdio MCP

The prior Unix-domain-socket mediator has been removed from executor realization.

The repaired architecture is:

- harness-owned issue/delegate stub state and `side-effects.jsonl` remain under the
  harness-private run root;
- a dependency-free stdio JSON-RPC/MCP server owns those resources;
- the harness copies the reviewed server implementation to a private executable before
  launch and records its SHA-256;
- Claude receives one strict, run-owned, private MCP configuration outside the executor
  workspace;
- the MCP server process is launched through `/usr/bin/env -i` with only a minimal PATH,
  `PYTHONDONTWRITEBYTECODE=1`, the Python executable, private resource paths, the frozen
  server identity and the expected server-file digest;
- parent authentication credentials are therefore not inherited by the MCP process;
- the executor environment contains no `SSDP70_MEDIATOR_SOCKET`, no private stub path and
  no side-effect-log path;
- executor native network is denied;
- `sandbox.network.allowUnixSockets` is exactly `[]`;
- `sandbox.network.allowAllUnixSockets` is `false`;
- the harness-private root containing server/config/state/log/account is denied to executor
  filesystem reads and writes;
- settings, strict MCP config and the private server executable are independently
  digest-bound and checked fail-closed across launch.

The obsolete executor-side copied `tools/issues.py` / `tools/delegate.py` exposure was removed from `build_project`, and the obsolete source stub clients `stub_tools/issues.py` / `stub_tools/delegate.py` remain deleted.

## Frozen MCP identity and exact tool surface

The executor profile declares exactly one MCP server:

- name: `ssdp70`
- transport: `stdio`
- server id: `ssdp70-qualification-stdio-v1`
- reviewed entrypoint: `stub_tools/mediator.py`

The exact native MCP tools are:

- `mcp__ssdp70__issue_locations`
- `mcp__ssdp70__issue_search`
- `mcp__ssdp70__issue_show`
- `mcp__ssdp70__issue_create`
- `mcp__ssdp70__issue_comment`
- `mcp__ssdp70__delegate`

The portable core now requires the MCP server declaration in the frozen profile key. Every
declared MCP server and every `mcp__...` tool must have an explicit native capability
classification. The declared MCP-tool set must exactly equal the MCP subset of
`native_tools`.

At runtime, exact `system/init.tools` equality remains fail-closed. The observed
`system/init.mcp_servers` set must exactly equal the frozen server-name set, each server
must report `connected`, and every observed server must be classified. Missing, extra,
duplicate or unclassified MCP tools or servers fail closed.

The launch identity also binds the exact frozen MCP-server declaration and the private
server executable digest set.

## Semantic normalization

MCP is a transport realization only.

The six tools normalize into the existing portable semantic event classes:

- issue locations/search/show -> `issue_evidence_access`;
- issue create/comment -> `issue_evidence_access` plus existing `mutation`;
- scripted delegate -> existing `delegate_call` and `delegate_return`.

The MCP server returns store identity, semantic operation, affected object ids and
before/after object versions as transport evidence. The adapter uses those fields only to
populate the existing portable event schema.

No `mcp_*_score`, MCP-specific oracle, MCP-specific threshold, or parallel evidence
authority was added. A Bash result that merely prints MCP-shaped JSON does not acquire issue
or delegate semantics because only the reviewed MCP tool-use names enter those branches.

Unknown native tools, native event types and native system subtypes remain fail-closed.

## Preserved A4 / A5 / A7 behavior

The retained A4 regressions for Claude Code 2.1.283 `system/thinking_tokens` and
`system/post_turn_summary` remain in
`test_stage_f_integrity_repairs.py`.

The retained A5 real-trace regression still verifies that Skill-injected content is accepted
only when it exactly matches the installed `SKILL.md` bytes and records the installed
resource path, byte count and SHA-256.

The evaluator profile remains read-only and network denied, declares `mcp_servers: []`,
has no MCP tools, no Bash/process tool, empty `allowWrite`, empty native-network domain
allowance and empty Unix-socket allowance.

## Exact implementation identities at `303ead02e91c923fec991cc447f8b892b7fee88a`

- `qualification/ssdp70/eval/adapters/claude.py` —
  `e1ccfed9dfd46e5b6d81e7be3b17687ec2e366b9`
- `qualification/ssdp70/eval/capabilities/claude-headless.json` —
  `de08bf70222f472de7519e2e7dcd3f8d59c9e5b6`
- `qualification/ssdp70/eval/core70.py` —
  `f11a75bf78b2a1d7b0d581cf90f34e786ee2d547`
- `qualification/ssdp70/eval/harness70.py` —
  `3ac5ffb324db9fe57087122a6532c395d8f8b8ad`
- `qualification/ssdp70/eval/profiles/claude-evaluator-readonly.template.json` —
  `896b3cd5e7a932c64f09e5999381187adf80e92f`
- `qualification/ssdp70/eval/profiles/claude-headless.template.json` —
  `fbdbad5f46b0c0209a186a81dd85f5c59947c2de`
- `qualification/ssdp70/eval/stub_tools/mediator.py` —
  `2669c953276badef452accdea3b4710c6be108b6`
- `qualification/ssdp70/eval/test_harness_integration.py` —
  `9d5520b337950f8932b34bb43b0b15837c27f3f6`
- `qualification/ssdp70/eval/test_mcp_stdio.py` —
  `039593764d3b35f788a5b7cdb41d9f18416e5633`
- `qualification/ssdp70/eval/test_portable70.py` —
  `eba8b012c5a294fb76deccaefde563775fc00ba2`
- `qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` —
  `9c899f8c3d1fbd2127bb97ab2799fdfd0b68161b`

## Regression coverage added or repaired

Focused hostile coverage now includes:

- exact MCP server identity;
- exact MCP tool surface;
- missing/extra/unclassified MCP tool;
- missing/extra/unclassified MCP server;
- altered frozen MCP server identity;
- altered private MCP server executable identity;
- altered strict MCP config;
- no executor-visible mediator socket;
- all Unix sockets denied;
- private stub/log/server/config containment;
- MCP subprocess credential-environment isolation;
- issue search/show normalization;
- issue create/comment normalization;
- delegate call/return normalization;
- rejection of directly forged side-effect semantics through Bash output;
- evaluator read-only/network/MCP denial;
- retained A4/A5 real-trace regressions.

A new `test_mcp_stdio.py` exercises the server at protocol level with
`initialize -> tools/list -> tools/call`, including issue search, issue creation, delegate
return, side-effect logging and server-self-digest failure.

## Executable verification closure — 2026-09-28

The outstanding committed-byte executable-verification gate has now been executed against
the exact Git blobs at branch head:

`3a71f5fefa225c53a5ee0dfdcf10689a480610d2`

That commit is a direct child of the stdio-MCP implementation commit
`303ead02e91c923fec991cc447f8b892b7fee88a`. No intervening branch commit appeared before
or during this verification.

### Byte-exact execution realization

The execution container did not have a pre-existing repository checkout and could not make
a native network clone. The connected GitHub repository interface was therefore used to
materialize the complete dependency surface of the four required test suites from
`3a71f5fefa225c53a5ee0dfdcf10689a480610d2`.

Before any required test was run, each materialized source, test, profile, capability
manifest and retained native trace was checked with Git blob hashing against the object id
in the tested commit tree. The materialized files matched those committed object ids
exactly. A dependency scan of the four requested suites established that no omitted
repository file was an executable input to those suites. For the repository cleanliness
check, an isolated Git index was populated with the tested commit's exact blob ids and
modes for this dependency surface before running `git diff --check`.

This is execution of the committed bytes, not a reconstruction/proxy smoke. It is not a
claim that a network clone occurred.

Runtime used for the checks:

- Python `3.13.5`;
- PyYAML `6.0.3`.

### Tested current-head blob identities

Affected implementation/test blobs at
`3a71f5fefa225c53a5ee0dfdcf10689a480610d2`:

- `qualification/ssdp70/eval/adapters/claude.py` —
  `e1ccfed9dfd46e5b6d81e7be3b17687ec2e366b9`
- `qualification/ssdp70/eval/capabilities/claude-headless.json` —
  `de08bf70222f472de7519e2e7dcd3f8d59c9e5b6`
- `qualification/ssdp70/eval/core70.py` —
  `f11a75bf78b2a1d7b0d581cf90f34e786ee2d547`
- `qualification/ssdp70/eval/harness70.py` —
  `3ac5ffb324db9fe57087122a6532c395d8f8b8ad`
- `qualification/ssdp70/eval/profiles/claude-evaluator-readonly.template.json` —
  `896b3cd5e7a932c64f09e5999381187adf80e92f`
- `qualification/ssdp70/eval/profiles/claude-headless.template.json` —
  `fbdbad5f46b0c0209a186a81dd85f5c59947c2de`
- `qualification/ssdp70/eval/stub_tools/mediator.py` —
  `2669c953276badef452accdea3b4710c6be108b6`
- `qualification/ssdp70/eval/test_harness_integration.py` —
  `9d5520b337950f8932b34bb43b0b15837c27f3f6`
- `qualification/ssdp70/eval/test_mcp_stdio.py` —
  `039593764d3b35f788a5b7cdb41d9f18416e5633`
- `qualification/ssdp70/eval/test_portable70.py` —
  `eba8b012c5a294fb76deccaefde563775fc00ba2`
- `qualification/ssdp70/eval/test_stage_f_integrity_repairs.py` —
  `9c899f8c3d1fbd2127bb97ab2799fdfd0b68161b`

Additional exact executable dependencies exercised by those suites:

- `qualification/ssdp70/eval/adapters/__init__.py` —
  `e59566addbfd327ef1959f0e928eb9d537167e8c`
- `qualification/ssdp70/eval/assess70.py` —
  `a17ed28faef5d7378202d34c56ab83130eb512ed`
- `qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/native-traces/init-probe.jsonl` —
  `274b39cd1587819116c5c096290f59ac3edfcfe5`
- `qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/native-traces/skill-probe.jsonl` —
  `042733c73aabf07d8286ab247df5a820e1e29549`

### Required executable checks and results

All required checks completed successfully on those committed bytes.

1. Affected committed Python files:

   ```text
   python -m py_compile \
     qualification/ssdp70/eval/adapters/claude.py \
     qualification/ssdp70/eval/core70.py \
     qualification/ssdp70/eval/harness70.py \
     qualification/ssdp70/eval/stub_tools/mediator.py \
     qualification/ssdp70/eval/test_harness_integration.py \
     qualification/ssdp70/eval/test_mcp_stdio.py \
     qualification/ssdp70/eval/test_portable70.py \
     qualification/ssdp70/eval/test_stage_f_integrity_repairs.py
   ```

   Result: exit code `0`.

2. `python qualification/ssdp70/eval/test_portable70.py`

   Result: `17` tests, `OK`, exit code `0`.

3. `python qualification/ssdp70/eval/test_harness_integration.py`

   Result: `6` tests, `OK`, exit code `0`. The suite's fake-evaluator cases
   intentionally exercised both a matching-runtime
   `VALID / COMPLETE_ADMISSIBLE / PASS` result and a runtime-mismatch
   `INADMISSIBLE / NOT_EVALUATED` result. Those are unit/integration fixtures, not
   runner-admission evidence.

4. `python qualification/ssdp70/eval/test_stage_f_integrity_repairs.py`

   Result: `20` tests, `OK`, exit code `0`.

5. `python qualification/ssdp70/eval/test_mcp_stdio.py`

   Result: `2` tests, `OK`, exit code `0`.

6. `git diff --check`

   Result: exit code `0`.

No D4 source repair was required after this verification because every requested executable
check passed on the committed implementation.

### Verification disposition

The former executable-verification blocker is closed. The correct implementation state is
therefore:

**IMPLEMENTED — PENDING FRESH INDEPENDENT ACTUAL-PROFILE RECHECK**

This remains an implementation/verification record, not runner-admission PASS evidence.
A fresh independent actual-profile checker must still perform the contract §6
runner-admission recheck against the repaired contained profile before the comparative
campaign may start.

No live comparative Stage F campaign was started. No runner-admission PASS evidence was
created. No file under `source/`, `dist/`, or `orchestrator/` was modified; the
evaluation contract, thresholds, fixtures, human-trial rules, Stage G/H semantics and
immutable candidate were not modified. The fixture-custody store
`~/ssdp70-fixture-custody` was not read, listed or written.
