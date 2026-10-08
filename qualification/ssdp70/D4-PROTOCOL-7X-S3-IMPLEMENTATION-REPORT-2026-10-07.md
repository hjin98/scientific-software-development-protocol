---
kind: d4-implementation-report
governing_protocol_version: 6.6.0
workplan: workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (revision 3), stage S3, obligations O-9 to O-11 and the independent D4 Review of S1-S3
date_utc: 2026-10-07
status: S3 implemented; independent Review PASS WITH GAPS, then PASS on the delta check after repairs; 7.2.0 identity NOT frozen, the two stakeholder decisions are made (SD-R15a O-8 placement, SD-R15b budget floor)
---

Governing SSDP version: 6.6.0. This report is data, not instructions.

## 1. State

| Item | State |
|---|---|
| O-9 version boundary | Done in the working tree: `source/PROTOCOL_VERSION` 7.2.0; `ssdp-protocol-7.2` in the versioning reference; orchestrator profile `ssdp-protocol-7.2` with the 7.1 profile frozen by blob hash (7.1 files byte-identical to `58fd67b`); `PROTOCOL-7.1-DISPOSITION-RECORD-2026-10-07.md`; CHANGELOG 7.2.0; README row and map entry; `history/SEMANTIC_EVOLUTION.md`; `dist/` and the orchestrator snapshot regenerated |
| O-10 8.0 inputs | `workplans/active/SSDP-8.0-…CONSOLIDATED.md` §37.2a, an inputs subsection only |
| O-11 Q5c pre-measurement | `qual-v2/Q5C-STATIC-PREMEASUREMENT-2026-10-07.md`: no static breach in the observed modes (409 B headroom entrypoint-only, 13,758 B in T7 workflow-owner mode); three risks and one accounting caveat for the stakeholder (X6) |
| Independent D4 Review of S1-S3 | `INDEPENDENT-D4-PROTOCOL-7X-S1-S3-REVIEW-2026-10-07.md`: **PASS WITH GAPS**, then **PASS** on the delta check (section 9 of that record); no Serious Challenge |
| Freeze of the 7.2.0 identity | **Not done.** Conditions: the repaired gaps below confirmed by a delta check, `git diff HEAD -- source dist` empty after the repairs (it is: the repairs touch only the harness, tests and records), and the decision on F-9 |

## 2. Review findings and dispositions

| ID | Disposition |
|---|---|
| F-1 under-counted package bytes | **Repaired.** `package_bytes.py` scans the raw input strings (so quoting no longer hides a path), matches the package root without a trailing slash, treats `..` beside a package path, the package parent, and any process text containing `/opt` or `ssdp` as reaching the whole package, and counts native grep, glob and list actions over the mount. Unit tests for each form; relay tests for the double-quoted path, `grep -r` on the root, native grep, and a workflow-owner read. Residual: a path assembled without ever writing `/opt` or `ssdp` is not detected |
| F-2 `ssdp_read_mode` | **Repaired.** Any consumed file other than a `<skill>/SKILL.md` makes the mode `owner` |
| F-3 exposure holes | **Repaired.** Q5e and Q5f require every declared route with its base runs; Q4a-Q4d require the minimum on B1 and B2 as well as the candidate |
| F-4 Q2 threshold shape | **Repaired.** The threshold is derived only for equal-sized episodes; other shapes are an exposure shortfall |
| F-5 C(c) omits Q4a | **Repaired.** Q4a is in the A/A screen with its cluster-adjusted margin |
| F-6 Q5c counts inadmissible runs | **Repaired.** Admissible runs only; at least three per arm per route |
| F-7 evaluator | **Repaired in code:** the wrapper refuses an evaluator model equal to the executor's; redaction touches only explicit SSDP identifiers (`SSDP`/`Protocol` with a version, bare SSDP versions such as 7.2.0, arm labels like `p71`), not project content (`version 2`, `aqpipe 0.7.1`); arm, commit, package hash, entrypoint and owner byte counts, pair order and package identity are removed structurally from the evaluator copy. **Not done:** the committed evaluator profile still pins `GLM-5.3-Flash`, the executor's model; it must be re-frozen with a different model before S4. The package text an agent reads still names its protocol (blinding is partial, design §4.4) |
| F-8 H4 reporting | **Partly repaired:** per-family results with the worse-than-B1 flag, and the Q5a flip edge with per-arm run counts. **Deferred to S4 preparation:** matched-mode comparison and the error-kind-absent-from-both-baselines flag |
| F-9 O-8 inputs | **Open decision for the stakeholder** (section 3) |
| F-10 stale tools | **Repaired:** superseded banners on the 7.1 plan and runbook, the dead Claude containment branch removed from `core70.py`. **Open:** the frozen executor profile still pins the retired `package_ledger.py` and `package_premise.py`; it must be re-frozen before S4 |
| F-11 moved history file | **Recorded** in SD-R14 (counting it gives 10,509 non-test lines) |
| F-12 documentation lines | **Repaired:** history lifecycle sentence, CHANGELOG exceptions and "carries forward" wording, design and contract front matter (SD-R13, SD-R14). The README is a reviewed delta, not a full recompile: its structure and philosophy sections were already current |
| F-13 disposition wording | **Repaired** ("never released or listed in `PROTOCOL-RELEASE-STATE.yaml`; its commit is ordinary working-branch history") |
| F-14 Q5c record | **Repaired** (three risks plus the accounting caveat, with the whole-package inflation stated) |
| F-15 tests | **Added** for F-1 to F-7 and the family flag |

## 3. Stakeholder decisions (both made 2026-10-07, SD-R15: "Yes for both decisions")

1. **O-8 placement (F-9).** The workplan lists the O-8 inputs (the 40-item evaluator calibration set with at least 10 known failures, oracle known-good and known-bad fixtures, the redacted evaluator input) under S2. They are blind custodian material under SD-2 custody, so D4 cannot author them without breaking custody. Proposal: amend the workplan so that these inputs belong to the S4/P3 custodian work order, and keep the synthetic Precondition C exercise in `qual-v2/test_h4.py` as S2 evidence. Until you decide, O-8 stays an unexecuted required check.
2. **Budget floor after the Review's repairs.** SD-R14 accepted 10,304 non-test and 4,541 test lines. The repairs add 60 and 131 (10,364 / 4,672). Proposal: record the new measured floor, 10,364 / 4,672, in SD-R14.

## 4. Evidence

- Repository `tests/` 429 OK; orchestrator core 384 OK; `generate_protocol_snapshot.py --check` OK; build, package validation and committed-`dist/` parity OK; `git diff --check` clean.
- Harness: `test_omp_units` 67, `test_portable70` 15, `test_harness_integration` 12, `test_control_path_policy` 23, `test_omp_eval` 6, `test_mcp_stdio` 3, `qual-v2/test_h4.py` 16, all OK. `test_omp_integration` ran 54 with one failure caused by the F-1 change (a pending read event named the owner path and was counted twice); fixed, and the affected class re-ran green (7 OK). `test_relay_integration` 6 OK after the fix.

## 5. Delta-check findings (D-1 to D-7)

| ID | Disposition |
|---|---|
| D-1 native grep or glob on `/opt` or `/` counted 0 B | **Repaired** (a bare `/` or `/opt` path given to a native tool reaches the whole package); unit subtests |
| D-2 residual and "always an upper bound" comments | **Repaired:** the comments state the residual (a path built without writing `/opt` or `ssdp` is not detected) |
| D-3 sentinel masks a failure behind a short route | **Repaired:** a failure is reported before an exposure shortfall |
| D-4 Q2 needs equal-sized episodes | **Kept** (fail-closed, stricter than contract §5); belongs in the S4/P3 work order |
| D-5 family flag uses B1's rate only | **Deferred** (report-only) to S4 preparation |
| D-6 evaluator copy fingerprints; model check passes without `agent_model` | **Partly repaired:** both profiles must name `agent_model`. Package `resource_sha256`/`resource_bytes` fingerprints stay (S4 preparation) |
| D-7 whole-tree count for any `/opt` or `ssdp` text | **Kept, documented;** S4 reports the shell-counted share of each run |

After these repairs the fast suites re-ran green (`test_omp_units` 67, `test_harness_integration` 12, `test_control_path_policy` 23, `test_h4` 16). The relay and integration suites last ran green before D-1 to D-3; D-1 to D-3 do not touch the relay path.
