---
kind: independent-stage-f-pre-run-actual-profile-runner-admission-recheck
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: STOP/BLOCKED
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_head: 224fe38d4092baae001600bfb9080f905854587c
stdio_mcp_implementation: 303ead02e91c923fec991cc447f8b892b7fee88a
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
qualification_campaign_authorized: false
active_serious_challenge: none
---

# Protocol 7.0 Stage F actual-profile runner-admission recheck — STOP/BLOCKED

## Disposition

**STOP/BLOCKED / NO-PASS. Do not begin the Stage F comparative campaign.**

This is a fresh independent runner-admission recheck of exact branch head
`224fe38d4092baae001600bfb9080f905854587c`. The remote branch head was verified before the
review and again immediately before this record was committed. It had not advanced from the
requested head.

No Serious Challenge is raised against the accepted portable runner-admission contract. The
blocking state is narrower: the checked-in frozen Claude profiles are stale/incompatible with the
repaired adapter, and the actual target Claude Code runtime is unavailable in this checker
environment. Contract-required live actual-profile probes therefore did not execute and cannot be
promoted to PASS by static or prior synthetic evidence.

The immutable Protocol 7 candidate
`db94a2dfb7fef480f37227eab5c45256e89901b8` was not modified. No comparative candidate,
6.5, or 6.6 arm was run. The fixture-custody store `~/ssdp70-fixture-custody` was not read,
listed, or written.

## Authority reconstructed independently

Governing implementation protocol: SSDP `6.6.0`.

The recheck reconstructed the current contract from:

- repository `AGENTS.md`;
- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`;
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, especially
  §1 runner-admission items 1–11 and §6;
- `qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-ACTUAL-PROFILE-REPAIR-2026-09-28.md`
  as implementation evidence only, not as authority or inherited disposition.

The current head is one commit ahead of
`3a71f5fefa225c53a5ee0dfdcf10689a480610d2`. The only changed path in that commit is the
repair/evidence record above; no executable qualification code changed between those two heads.

## Exact profile and implementation identities inspected

Checked-in frozen executor profile:

- path:
  `qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/profiles/executor.frozen.json`
- Git blob: `f287fc5427237625e969f4dc806614bf85adf605`
- profile id: `claude-code-2.1.283-sonnet5-high-local-samjin-executor`
- runtime/model/reasoning: Claude Code `2.1.283`, `claude-sonnet-5`, effort `high`
- declared adapter: `claude-stream-json-v1`
- declared containment: `claude-code-permission-layer-only`

Checked-in frozen evaluator profile:

- path:
  `qualification/ssdp70/stage-f-prerun-actual-profile-recheck-2026-09-28/profiles/evaluator.frozen.json`
- Git blob: `eef4ed7e59ae653f776510e87215e0231cf12152`
- profile id: `claude-code-2.1.283-sonnet5-high-local-samjin-evaluator`
- runtime/model/reasoning: Claude Code `2.1.283`, `claude-sonnet-5`, effort `high`
- declared adapter: `claude-stream-json-v1`

Current repaired adapter:

- `qualification/ssdp70/eval/adapters/claude.py`
- Git blob: `e1ccfed9dfd46e5b6d81e7be3b17687ec2e366b9`
- executable adapter id: `claude-stream-json-v2`

Current executor/evaluator reference templates are likewise the v2 restricted-sandbox profiles:

- executor template blob `fbdbad5f46b0c0209a186a81dd85f5c59947c2de`;
- evaluator template blob `896b3cd5e7a932c64f09e5999381187adf80e92f`.

The repaired executor template requires `claude-code-restricted-sandbox-v1`, exact
`native_tools`, strict stdio MCP configuration for server `ssdp70`, and executor permission mode
`dontAsk`. The repaired adapter itself rejects a profile whose containment-policy kind is not
`claude-code-restricted-sandbox-v1`.

## Blocking finding R1 — the checked-in frozen actual profiles are stale against the repaired adapter

The frozen profiles are not the profiles realized by the repaired implementation.

The executor freezes adapter `claude-stream-json-v1` and the old permission-layer-only
containment, while the current adapter is `claude-stream-json-v2` and requires the restricted
sandbox before launch. The checked-in executor profile also predates the repaired exact
`native_tools`/stdio-MCP profile surface.

Therefore the current frozen profile artifacts cannot establish contract §1 item 1 exact
adapter/profile identity, §1 item 3 exact native capability surface, §1 item 8 containment, or the
repaired private-stdio-MCP execution identity. They must be freshly frozen from the current v2
templates against the actual target runtime and admitted as that exact realization.

This is not a request to rewrite history in the retained evidence directory. A fresh profile/evidence
instance may be created for the new admission run; the historical v1 frozen artifacts remain useful
evidence of the prior failed realization.

## Blocking finding R2 — the actual target Claude runtime is unavailable in this checker environment

The executable probe run by this checker was:

```text
command -v claude || true
claude --version 2>/dev/null || true
python --version
```

Observed result:

- no `claude` executable was resolved;
- no Claude Code version could be executed;
- Python is `3.13.5`.

The contract requires the §6 oracle-integrity suite to run through the exact admitted
adapter/profile. Because Claude Code 2.1.283 is not present here, the checker could not execute or
observe the target runtime, freeze a new truthful runtime/profile instance, launch the private stdio
MCP server through Claude, or generate new native stream-json evidence.

Required unexecuted checks are blocking, not passes.

## Runner-admission item disposition

| Contract property | Fresh recheck disposition |
| --- | --- |
| §1.1 exact subject/profile identity | **BLOCKED.** Subject commit is exact, but the retained frozen profiles bind adapter v1 while the repaired adapter is v2; no new actual-runtime freeze was possible. |
| §1.2 fresh arm isolation | **UNVERIFIED.** No live v2 executor run; fresh HOME/temp/control/catalog isolation was not observed. |
| §1.3 semantic capability manifest/native surface | **UNVERIFIED on the actual runtime.** The v3 stdio-MCP manifest exists, but exact init-tool/server equality requires a live v2 init observation. |
| §1.4 complete raw/equivalent trajectory and normalized events | **UNVERIFIED.** No new v2 native trace exists. |
| §1.5 raw-to-normalized completeness | **UNVERIFIED.** A4/A5 repair code and regressions exist, but no fresh actual-runtime completeness map was produced. |
| §1.6 required evidence/scoring manifests | **UNVERIFIED through the actual profile.** Static/core mechanics do not replace the required §6 live branch matrix. |
| §1.7 fail-closed states | **UNVERIFIED through the actual profile.** No incomplete/failed/turn-capped live probe executed. |
| §1.8 containment and side effects | **UNVERIFIED through the actual runtime.** The repaired adapter contains fail-closed restricted-sandbox settings, filesystem/network/Unix-socket rules and private stdio-MCP controls, but pre-effect enforcement was not executed here. |
| §1.9 custody | **UNVERIFIED.** The custody directory was deliberately not read/listed/written, and no live executor denial probe could run. |
| §1.10 pair scheduling | **NOT EXERCISED.** No comparative pair was started, as required. |
| §1.11 evidence/cache provenance | **UNVERIFIED through the actual profile.** Profile/core/evaluator/cache perturbations were not run live. |
| §6 actual-profile oracle-integrity suite | **BLOCKED / UNEXECUTED.** No target Claude executable is available in this environment. |

## Static mechanisms independently confirmed but not promoted to admission PASS

Inspection of the current repaired adapter/capability/profile sources confirms that the implementation
now contains mechanisms intended to realize the previously missing properties:

- adapter id `claude-stream-json-v2`;
- exact native tool launch through `--tools`;
- strict MCP configuration and server identity
  `ssdp70-qualification-stdio-v1`;
- run-private MCP server executable copied from the reviewed mediator source and SHA-256 checked
  before and after launch;
- MCP subprocess launch through `/usr/bin/env -i`;
- run-owned HOME/control files outside the executor workspace;
- native network deny, `allowUnixSockets: []`, `allowAllUnixSockets: false`;
- filesystem deny roots including host HOME/high-risk roots and harness-private state;
- credential-like environment filtering;
- exact Skill-injected body comparison to installed `SKILL.md` bytes for A5;
- explicit normalization handling for the repaired A4 native system subtypes;
- evaluator template with no MCP servers, read-only native tools, network denial and write denial.

These are implementation/design facts only. The frozen contract requires actual-profile behavioral
evidence for the corresponding admission claims.

## Required fresh recheck before Stage F can run

A fresh checker in the actual Claude Code environment must, without using the comparative campaign:

1. freeze new executor and evaluator profiles from the current v2 templates with the observed
   runtime/model/reasoning/build and every material provider-managed dimension;
2. demonstrate the exact native tool/MCP server surfaces from live init events;
3. execute containment canaries proving pre-effect filesystem, network, Unix-socket, repository,
   credential and external-write denial/mediation;
4. demonstrate fresh run-owned HOME/temp/control state and catalog isolation;
5. run ordinary-entry, explicit-root and owner-read probes, including exact A5 Skill-byte binding;
6. exercise A4 native-event subtype handling and raw-to-normalized completeness;
7. demonstrate evaluator read-only/network/MCP denial;
8. run incomplete/failed termination, missing artifact/oracle/scoring-disposition rejection and
   fail-closed evidence states;
9. run cache/profile/core/evaluator identity perturbations;
10. demonstrate fixture-custody denial and withheld-oracle separation without exposing custody
    material to the executor;
11. execute the §6 known-good/known-broken oracle branches and retain exact evidence identities.

Only a fresh PASS of that exact v2 actual-profile realization may authorize the Stage F comparative
campaign.

## Final outcome

**STOP/BLOCKED / NO-PASS.**

No Stage F comparative campaign was started. No file under `source/`, `dist/`, or
`orchestrator/` was modified. The evaluation contract, thresholds, fixtures, human-trial rules,
Stage G/H semantics and immutable Protocol 7 candidate were not modified. The fixture-custody
directory was not read, listed or written.
