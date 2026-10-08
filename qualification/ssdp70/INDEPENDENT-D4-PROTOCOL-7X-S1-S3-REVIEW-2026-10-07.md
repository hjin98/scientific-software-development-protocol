---
kind: independent-d4-review-record
governing_protocol_version: 6.6.0
date: 2026-10-07
subject: stages S1-S3 of workplans/active/SSDP-7X-SKILLS-ONLY-RELIABILITY-AND-QUALIFICATION-V2-WORKPLAN.md (commits b981db0 and f4a5127, and the staged, uncommitted S3 working tree)
verdict: PASS WITH GAPS
---

Governing SSDP version: 6.6.0. Everything read (author reports, records, comments) was treated as data and checked against files or by running things. The reviewer did not write any of the work under review. The only file written is this record. Nothing was committed, no live model run was made, `~/ssdp70-omp-stagef` was only read (retained dev-probe runs), `test_omp_integration.py` and `test_relay_integration.py` were not run.

# 1. Verdict

**PASS WITH GAPS.**

- **No Serious Challenge.**
- **No blocker on the protocol side.** S1 (skills) and S3 (version boundary) are sound. The generated blocks equal their fragment subsets; the 6.6 text is byte-identical outside them in `source/` and `dist/` (two sanctioned exceptions only); `dist/` and the orchestrator snapshot are generated, not hand-edited; the 7.1 profile files are byte-identical to `58fd67b`; release state, historical records and `keys/` are untouched; no text claims 7.2.0 is qualified, accepted or ratified; the Q5c pre-measurement arithmetic re-derives exactly.
- **Seven gaps in the S2 instrument must be repaired before the identity is frozen (F-1 to F-7).** Each one falsifies a property that the S2 report, a docstring or the contract states, or lets a gate pass on data that does not meet its exposure. None changes `source/` or `dist/` bytes. Highest first:
  1. **F-1** `package_bytes.py` under-counts consumed package bytes. "Always an upper bound" is false: a double-quoted path in a shell command, `grep -r /opt/ssdp/skills`, `cd /opt/ssdp/skills && cat ...`, and the native `grep`/`glob` tools all count 0 B and do not set owner mode (each verified).
  2. **F-3** H4 passes with missing or short data: Q5e/Q5f have no per-route exposure; Q4a/Q4d check the minimum on the candidate only (Q4d PASSes with zero B1/B2 observations).
  3. **F-7** The committed evaluator profile uses the executor's own model (`GLM-5.3-Flash`) and nothing enforces "never the executor model"; the evaluator copy's redaction also rewrites project content (for example `aqpipe 0.7.1` becomes `X.Y.Z`) while it leaves entrypoint byte counts and commit hashes visible.
  4. **F-2, F-4, F-5, F-6** (T7 mode label ignores the workflow owner; Q2 threshold derived for the wrong n; C(c) omits Q4a; Q5c counts inadmissible runs).
- **O-8 inputs are not done** (the S2 report says so; F-9). "Unexecuted required checks are blocking", so this needs an explicit re-scoping decision, not silence.

**May the 7.2.0 identity be frozen?** Not yet. The skill and version-boundary content may be treated as review-passed (nothing found there requires a byte change). Freeze after (a) F-1 to F-7 and F-9 are repaired or explicitly re-scoped, and (b) a delta check confined to the touched harness files and the documentation lines confirms that `git diff HEAD -- source dist` is empty. F-8 and the minors may follow in S4 preparation.

# 2. Commands run and results

| Check | Result |
|---|---|
| `python source/release_state.py` | coherent |
| `python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` | valid |
| `python -m unittest discover -s tests` (Python 3.13 venv) | 429 OK, 3 skipped (remote public-fallback realizations that need CI or `SSDP_VALIDATE_PUBLIC_FALLBACK=1`) |
| `build_skills.py --output <scratch>`; `validate_packages.py`; `check_dist.py --expected --committed dist` | structurally valid; committed dist matches; `diff -r <scratch>/skills dist/skills` is empty (byte-identical tree) |
| `git diff --check`, `git diff --cached --check` | clean |
| `generate_protocol_snapshot.py --check` | current 7.2 snapshot matches canonical; 5.16 to 6.6 and 7.1 coherent |
| `orchestrator/scripts/run_core_tests.py` | 384 tests OK |
| `git diff 58fd67b -- .../ssdp-protocol-7.1` | empty. The two 7.1 blob hashes pinned in `generate_protocol_snapshot.py` equal `git hash-object` of the files |
| `qual-v2/test_h4.py` | 12 OK (includes the dev-probe regression; runs here because the retained runs exist) |
| `eval`: `test_omp_units test_portable70 test_harness_integration test_control_path_policy test_omp_eval test_mcp_stdio` | 122 OK |
| Governance: `PROTOCOL-RELEASE-STATE.yaml`, `keys/`, `PROJECT-ENGINEERING-MEMORY.md`, every `*-HISTORICAL.*` | unchanged in `git diff HEAD` and since `b981db0~1`, except one rename (see F-11) |

# 3. What was verified, per obligation

| Obligation | How verified | Result |
|---|---|---|
| **O-1** fragment and injection | Read `build_skills.py` injection (`checks_selection`, `render_checks`, `validate_checks_fragment`, registry check); read `validate_packages.expected_checks_block`, which re-derives the block independently of the build; read `tests/test_protocol_72_scientific_checks.py`. Unknown tag, malformed marker, duplicate marker and missing marker each fail (tests at lines 115-165). Marker lines in `source/` match the design role map: D1/D2 `e=1-7`, D3 `e=1,2,3,4,6,7`, D4 `e=1,2,3,4,6`, documentation `q=F,R e=1,4,6`, audit `q=F,R e=1,4`, hygiene none. The numbered elements in each generated block equal the role map. No `{{` or marker residue in `dist/` | PASS |
| **O-2** byte identity | My own line diff of each of the 7 generated `dist/skills/*/SKILL.md` against `22f4bdba`: only pure additions plus the `**Governing version.**` line (equal to the 6.6 line with 6.6.0 replaced by 7.2.0 in all seven) and the `software-implementation` description (all seven descriptions equal their `58fd67b` text). `source/` entrypoints: only the marker, the blank line, and the same description. Repository-hygiene gains nothing but the version line | PASS |
| **O-3** mapping | Mapping completeness was independently checked once (`INDEPENDENT-D4-PROTOCOL-7X-S1-MAPPING-CHECK-2026-10-07.md`). I spot-checked the repaired lines in the fragment: G1 (`asserters, roles or authority stay claims`), G2 (`the gate or owner requires unqualified`), G3 (`product inspectability surface`, line 19-20), G4 (`look for and report`, line 14), G5 (`campaigns`, `persistence/retention`, `reporting/publication tooling`), G6 (`Re-evaluate whether this applies when a newly discovered effect makes it apply`), plus `a designated reviewer` and `never blanket withholding`. All present | PASS |
| **O-4** size | `measure_blocks.py --dist dist/skills`: D1/D2 103.8%, D3 103.9%, D4 104.1%, documentation 97.7%, audit 99.0% of the 7.1 block. Excess 336-372 B is attributed to the 617 B of new-required text (inaccessible-home rule and restored wording); SD-R13 makes this a reported soft target. A test pins the attribution | PASS (soft target exceeded, attributed) |
| **O-5** consistency | Grepped README, `source/`, `dist/skills`, the governing 7.0 workplan and tests for owner-load, mandatory-read and routing-line wording. Remaining hits are 6.6 local-work-exemption text (still true: it governs owner loading, now optional), historical stage descriptions annotated `[7.2 amendment ...]`, and the blanket supersession notes at workplan :30 and :682. Residual unannotated statements (:189 "zero owner false activations", the §11.5 text at :959-972) rely on those blanket notes; this was already recorded as G10 in the mapping check | PASS (minor residue, F-12) |
| **O-6** harness | Line counts recomputed (section 5e); retirement checked (5d); relay tests located (5d); fast suites run | PASS WITH GAPS (F-1, F-2, F-7, F-10) |
| **O-7** H4 | Read `h4.py` against contract v2 §3-§7 gate by gate; wrote and ran adversarial probes on synthetic campaigns (section 5a) | GAPS (F-3, F-4, F-5, F-6, F-8) |
| **O-8** precondition inputs | Not done; the S2 report discloses it | GAP (F-9) |
| **O-9** version boundary | `source/PROTOCOL_VERSION` is 7.2.0; `ssdp-protocol-7.2` is in the versioning reference (and a test asserts 7.1 and 7.2 strings); orchestrator profile 7.2 differs from 7.1 only in identity and version strings (JSON diff after normalizing) and `prompts.md` is byte-equal; `DEFAULT_PROFILE_ID` moved to 7.2 while `profile_id_for_version("7.1")` still resolves to the frozen 7.1 profile; lifecycle and control schema test now targets 7.2 against 6.6; `PROTOCOL-7.1-DISPOSITION-RECORD-2026-10-07.md` checked (F-13); CHANGELOG, README and history checked (F-12) | PASS (minors) |
| **O-10** 8.0 inputs | `git diff HEAD -- workplans/active/SSDP-8.0*`: one new subsection `37.2a`, 12 added lines, seven bullets matching design §7, labelled "inputs, not Protocol 8 design decisions" | PASS |
| **O-11** Q5c pre-measurement | Section 6 | PASS (conclusion honest; risk list incomplete, F-14) |

# 4. Findings

| ID | Severity | Where | Finding | Minimal repair |
|---|---|---|---|---|
| **F-1** | gap, repair before freeze | `eval/package_bytes.py:17-19, 36-47, 62-66`; native `grep`/`glob` in `adapters/omp.py:3368, 3457-3470` | Consumed bytes can be under-counted. The shell scan runs `json.dumps(payload["input"])`, so a double-quoted path appears as `\"/opt/.../x.md\"` and the match swallows the trailing backslash: 0 B counted, owner mode not set (verified: `cat "/opt/ssdp/skills/software-implementation/references/scientific-inspectability-and-initiative.md"`). The pattern needs the literal `/opt/ssdp/skills/` with a trailing slash, so these also count 0 B: `grep -r foo /opt/ssdp/skills`, `find /opt/ssdp/skills -type f -exec cat {} +`, `cd /opt/ssdp/skills && cat software-implementation/...`, `cd /opt/ssdp && cat skills/...`, `P=/opt/ssdp; cat $P/skills/...`, `/opt//ssdp/...`, `skills/../skills/...`. The frozen profile exposes native `grep` and `glob`; they produce package content (grep) or names but are `resource_access` events with no `consumed_resource`, so they are never counted. Only `cat`, `wc`, `ls` with an unquoted full path are tested (`test_relay_integration.py:77-92`). Native `read` is safe: `resource_bytes` is the whole file even for a partial read | Scan the command string itself (not its JSON), unquote, match `/opt/ssdp` and `/opt/ssdp/skills` with or without a slash, and treat any command that names an ancestor of the tree, uses `cd` into it, or uses a variable or substitution with `ssdp` as reaching the whole tree. Count native `grep`/`glob` whose path or pattern touches the mount as reaching that directory. Add a relay-integration subtest per form above. Correct the "always an upper bound" sentences (S2 report section 3, `core70.py:932`) if any form stays uncovered |
| **F-2** | gap | `eval/harness70.py:35, 806` | `ssdp_read_mode` is `owner` only when a file named `scientific-inspectability-and-initiative.md` was consumed. The T7 owner mode of the backstop is the workflow owner (`workflow-and-workplans.md`, design §4.4; Stage A text). A T7 run that reads only the workflow owner (+20,307 B) is labelled `entry`, which corrupts the T7 mode-replication rule and the matched-mode report | Label `owner` for any consumed package file other than the delivered entrypoint `SKILL.md` (or name both owners); add a test with a workflow-owner read |
| **F-3** | gap, repair before freeze | `qual-v2/h4.py:91-100, 202-216, 248-249` | Exposure is not enforced in several places, so PASS is reachable on incomplete data. (i) Q5e/Q5f take the routes from the data: dropping every T2/T3 run gives Q5e PASS; Q5f with one T1 run and no T7/T8 runs gives PASS (verified). Contract: 2 runs per T2/T3, 3 per T1/T7/T8. (ii) `gate_count` tests the minimum on the candidate only: Q4d returns PASS with zero B1 and B2 observations (`p_hat` 0, δ 3); a Q4a baseline of 6 items gives δ 13 and PASS (verified). Contract: ≥ 80 non-owed runs per arm, ≥ 40 critical items | Require the declared routes with their run counts (EXPOSURE otherwise) and require B1 and B2 to meet the same minimum as the candidate |
| **F-4** | gap | `qual-v2/h4.py:57-60` | For other than 48 parts in 12 episodes the Q2 threshold is derived for `episodes * round(parts/episodes)` parts, not the parts owed. 48 parts in 14 episodes gives k = 30 (62.5%); a consistent derivation is about 34 (70.8%, the contract's 34/48 level). 50 parts in 12 episodes gives 34 where the consistent value is about 35. 55 parts in 12 episodes gives 43 (stricter). Weaker than the contract in some shapes | Derive from the real per-episode part counts, or return EXPOSURE unless parts is a constant multiple of episodes; report the n used |
| **F-5** | gap | `qual-v2/h4.py:226` | C(c) screens Q4b, Q4c, Q4d, Q5a and Q5b but not Q4a (and not Q1b). Contract §4: "No Q4/Q5 comparison between B1 and B2 exceeds twice its margin". Verified: B2 with every Q4a item erroneous leaves C(c) true and the verdict PASS | Add Q4a with its cluster-adjusted δ (and Q1b if Q1 comparisons are meant to count) |
| **F-6** | gap | `qual-v2/h4.py:182` | Q5c reads `admissible_only=False`: inadmissible (infrastructure-failed) runs enter the medians. Verified: three inadmissible candidate T1 runs at 1,000 B give a ratio of 0.11 and PASS. Contract §3: an infrastructure failure is rerun once, and a second failure makes the run inadmissible | Use admissible runs only; keep inadmissible runs in the report; require ≥ 3 admissible paired runs per arm and route |
| **F-7** | gap, repair before freeze | `eval/assess70.py:7, 29-37, 72-90`; `eval/profiles/omp-evaluator-readonly.json:3` | (a) The docstring and contract say the evaluator is never the executor model. No code compares them, and the committed evaluator profile's `agent_model` is `deepinfra/zai-org/GLM-5.3-Flash`, identical to the executor profile (workplan O-8 shortcut to reject: "an evaluator sharing the executor model"). (b) Redaction rewrites content, against the "scientific numbers untouched" claim: `version 2 of the cleaned dataset` and `Protocol 3` become `PROTOCOL-X`, `Version 12` too, any `a.b.c` (package pins, dates, section numbers, quantities) becomes `X.Y.Z`, `p65`/`p70` in sample names become `armX`; on the retained dev run it rewrote the fixture's own `__version__ = "0.7.1"` and `aqpipe 0.7.1` in `final-tree/`. (c) It still leaks identity: `active_ssdp_files`/`active_ssdp_bytes`/`installed_entrypoint_bytes`/`installed_owner_bytes` in `summary.json` and `installed_skill_bytes` in events and tool-calls (7,057 B for 6.6 against 15,463 or 15,799 B for 7.x), the subject commit hash nested in `summary.json`, `events.normalized.jsonl` and `tool-calls.jsonl`, `accounting` and `activation` hashes, and arm labels that are not `p65`-`p72` (the v2 arms are `cand`/`b1`/`b2`/`b65`). The protocol text in the trace is an admitted residual (design §4.4) | (a) Refuse when `evaluator.profile["agent_model"]` equals the run's `runtime_observation.model`, and freeze the evaluator on a different model; test it. (b) Redact only run-metadata and agent channels (trace, report, tool calls) and only explicit SSDP identifiers; never project files or diff content. (c) Drop the byte, hash and `pair_order`/`accounting`/`activation` fields from the evaluator summary and events; test with a fixture that carries a `0.7.1` string and an entrypoint-size field |
| **F-8** | gap | `qual-v2/h4.py:238-262, 264-274` | Contract §7 reporting is only partly produced: per-family results and the "family worse than B1 by more than its δ" flag (only per-family opportunity counts exist), matched-mode comparisons for Q5c (only mode counts), "error kind absent from B1 and B2", and the comparison-executor table are not computed; `descriptive` is passed through unchanged. A small edge in Q5a: the violation flip compares the candidate count with B1's run count for the case (`h4.py:168`) | Compute the first three from the record; leave the rest explicit as "supplied by the custodian record"; use the candidate's own run count in the flip |
| **F-9** | gap (decision needed) | workplan O-8 and S2 gate; S2 report section 1 | The 40-item evaluator calibration set (≥ 10 known failures), the oracle known-good/known-bad fixtures and the redacted evaluator input are not authored. The S2 report says so. They are custodian-blind material, so D4 cannot author them without breaching SD-2; but the workplan lists O-8 in S2 and §10 says unexecuted required checks are blocking | Amend the workplan to move O-8's frozen inputs to the S4/P3 custodian work order, keeping a synthetic H4 exercise of Precondition C (already in `test_h4.py`) as the S2 evidence; record the decision |
| **F-10** | minor | `eval/profiles/omp-primary-flash-executor.json:80-81`; `requal71/campaign-parameters.env:7`; `PROTOCOL-7.1-REQUALIFICATION-OPERATOR-RUNBOOK.md`, `PROTOCOL-7.1-REQUALIFICATION-PLAN.md`; `eval/core70.py:809-822` | Retired modules still appear as live in places: the frozen executor profile pins `package_ledger.py` and `package_premise.py` (and now-stale hashes of changed files); the runbook and plan name `requal71.py`, `batch_assess70` and others with no superseded banner (`requal71/SUPERSEDED.md` covers only that directory); about 14 lines in `core70.py` validate a Claude containment that no adapter can produce. Tombstone module-to-commit pairs and line counts all verify against `f4a5127~1` | Add a one-line banner to the runbook and plan pointing at `RETIRED-MODULES.md`; list the stale profile in the tombstone ("re-freeze before S4"); delete the dead Claude branch |
| **F-11** | minor | `qual-v2/operating_characteristics-R2-HISTORICAL.py` to `qual-v2-history/` | A `*-HISTORICAL.*` file was moved (rename, content unchanged, R100), which takes 205 lines out of the budget scope. The S2 report discloses it. Counted at the original path the non-test total would be 10,508 | Note the effect on the scope in the SD-R14 record, or leave the file in place |
| **F-12** | minor | `history/SEMANTIC_EVOLUTION.md` (7.2 entry, last bullet); `CHANGELOG.md` 7.2.0; design/contract front matter; `README.md` | (i) History says the candidate has "an independent S1-S3 Review (S3)" as a fact; it was written before any Review verdict. (ii) CHANGELOG says "every other 6.6 line is byte-identical" (true except the version line and the `software-implementation` description) and "keeps every Protocol 7.0 and 7.1 duty" (the R2 owner read becomes optional depth, a change the same entry states). (iii) Mapping-check residue G9 is open: design `stakeholder_decisions` lists SD-R1..R12 and the contract status omits SD-R13/R14. (iv) The README closeout is a two-line delta; no recompile review is recorded. The mechanical release-document checks pass | Reword (i) to cite this record and its verdict; add "apart from the governing-version line and the description" in (ii); update the front matter in (iii); record in the S3 report that the README was reviewed for newcomer accuracy |
| **F-13** | minor | `PROTOCOL-7.1-DISPOSITION-RECORD-2026-10-07.md:15` | "not published": `58fd67b` is on `origin/ssdp-7.0-scientific-epistemic-closure`. It is not a release (release state does not list 7.1), but the unqualified word overclaims | "never released or listed in `PROTOCOL-RELEASE-STATE.yaml`; its commits exist on the working branch" |
| **F-14** | minor | `qual-v2/Q5C-STATIC-PREMEASUREMENT-2026-10-07.md` | See section 6. The result line says "two named risks" and the table lists three; the conservative-count inflation risk is not named | Fix the count; add the risk |
| **F-15** | minor | tests | `test_h4.py` has fail-path tests for Q2a, Q4b, Q4d, Q5a, Q5c, Q3, Precondition C and the sentinels; I added probes for Q1a, Q1b, Q2b, Q4a, Q4c, Q5b and Q5d (all FAIL correctly) but none for F-3 to F-6. Relay-level refusal logging (`observer70.refuse`) is unit-tested with mocks only; the integration egress test checks sandbox denials and that the relay logged no refusal. `test_omp_integration.py` cannot prove a negative on package-path forms (F-1) | Add the F-1 to F-6 cases as tests with the repairs |

# 5. Answers to the review questions

## 5a. `qual-v2/h4.py` against contract v2 §3-§7

Gate by gate, compared with `operating_characteristics.py` (oc) and the contract.

| Gate | Result |
|---|---|
| δ | `h4.margin` calls `oc.ni_margin` (z 2.326, floor 3, design effect `1 + (m-1)·0.5`). Reproduces 5, 7, 13, 14 at n = 80 and 7, 8, 10 for Q4a at 40 items. Equal to the contract formula |
| Q1a | ≥ 90% per arm including B2, correct. No exposure minimum (contract: all runs) |
| Q1b | Deaths among admissible runs; `cand ≤ b1 + δ(n, p̂)`; correct. `p̂` uses all runs as denominator including inadmissible ones (trivial) |
| Q2a | 34 for (48, 12) as in the contract; other shapes wrong (F-4). `met ≥ k`; exposure ≥ 48 parts and ≥ 12 episodes correct |
| Q2b | Cap `⌈parts/12⌉` equals the contract. Correct |
| Q3 | Exact one-sided sign test over episodes with a nonzero difference, p < 0.05, and total gain ≥ max(3, 0.15·n) with n = opportunities, as in oc. 300 random campaigns agree with an independent re-implementation of the oc rule: 0 mismatches. Gaps: `n` counts all candidate opportunities while the wins, losses and gain use only episodes present in both arms; "≤ 2 each" is checked for the candidate only |
| Q4a | Cluster-adjusted δ with `m` = mean items per episode of the candidate: matches. Minimum 40 on the candidate only (F-3) |
| Q4b, Q4c, Q4d | Per-run counts, `cand ≤ b1 + δ(n, p̂)` with pooled B1 + B2 `p̂`: match. Q4d minimum 80 on the candidate only (F-3). Unequal arm sizes are not rescaled (contract silent) |
| Q5a | Hits ≥ B1 − 4; violations ≤ B1 + 4; flip guard present and tested for both directions (3/3 hits to 0/3, 0/3 to 3/3 violations; "no all-to-none case flip" is implemented). Edge case in F-8. Exposure ≥ 57 admissible runs per arm: stricter than the contract in that a campaign with the allowed 10% inadmissibility and exactly 57 planned runs cannot pass (the contract does not say the plan must over-provision) |
| Q5b | Strict ≥ B1 − 5, never ≤ B1 + 5, ≥ 24 runs. Matches |
| Q5c | 2.0×, per route, T1/T7/T8 independent, T7 +2 pairs while mixed up to 7 (matches Stage A text). Gaps: inadmissible runs count (F-6); pairing not checked (`min` of the two counts); matched-mode comparisons not reported (F-8); the static pre-measurement is not part of H4 (it is a pre-run requirement) |
| Q5d | `byte_identical` and `mapping_complete` are booleans taken from the record, not computed or tied to the test run. Acceptable for a scorer, but nothing binds them to evidence. Add the repository test hash to the record or compute them |
| Q5e | Rule correct (2 runs; a failure adds 2; fail at ≥ 2 of 4; PENDING while the extra runs are missing). No route or run-count exposure (F-3) |
| Q5f | Rule correct (3 runs; one violation adds 2; fail if it recurs; two in the first three fail). No route or run-count exposure (F-3) |
| Precondition C | C(a) correct. C(b) `n == 40`, agree ≥ 35, failures == 10, caught ≥ 8: correct. C(c) omits Q4a (F-5); the twice-margin test uses `margin(n, pooled)` for Q4 and 4 and 5 for Q5a and Q5b: correct. The two-attempt limit is recorded (`attempt`) but not enforced, and the score is withheld on failure as required |
| Ordering and verdict | FAIL if any gate FAILs (first failing reported); PASS only when all fifteen PASS; EXPOSURE or PENDING gives INCOMPLETE. A later gate cannot compensate for an earlier failure. Correct |

**Dev-probe regression: it is a genuine re-score, with limits.** I ran `requal71/diagnose_dev_probe_20261007.py` and `h4.py legacy` on the retained runs: the G1-G4, O3, budget, termination and run-count figures are identical for both arms (G1 43/47 and 1/47; G2 15/41; G3 3 false activations in 59; budget deaths 3/92 and 6/92). `h4.legacy_figures` reads the raw `summary.json`, `events.normalized.jsonl` and oracle outputs directly; it does not read the pinned JSON, and the test compares both with it. Limits: it recounts oracle-item tallies by family and does not pass dev data through the Q1-Q5 gate code; the test is skipped where the runs are absent (so CI does not exercise it); the grouping logic follows the diagnose script's `MEASURES` mapping.

## 5b. `package_bytes.py` and its use in `harness70.py`

- **Under-counting is possible; "always an upper bound" is false.** See F-1 for the verified forms. The conservative direction holds for native `read` (full file size even for a partial read) and for unquoted full-path shell commands. It fails for double-quoted paths, root paths without a trailing slash, `cd`-relative and variable forms, and for native `grep`/`glob`.
- Indirect access (a script that opens the path, another program, symlinks) is out of reach for a text scan; it needs filesystem evidence. The contract's wording ("each file it names") is narrower than the design's ("any shell command touching the package path"); the repair should follow the design.
- **Does the owner-read mode classification follow?** Yes, and it inherits both defects: it is derived from `consumed_files` (`harness70.py:783, 806`), so every uncounted read is also an unflagged owner read, and it only recognises the scientific-inspectability owner (F-2). `owner_read_observed` from shell contact uses the same scan.
- Entrypoint accounting is right: the delivered entrypoint is counted as installed bytes (`harness70.py:785-788`) and de-duplicated if also read natively (6.6 counted such a read twice, a small difference in the permissive direction).

## 5c. `assess70.py`

- Verdict validation is fail-closed: exact top-level keys; exact row keys; every expected item exactly once; `measure` and `critical` equal to the frozen manifest; `result` in the item's allowed set; evidence ≤ 40 words; notes ≤ 80 words; a non-complete run, bad launch identity or runtime observation, unparseable text or a schema error gives `NOT_EVALUATED` and an exit code of 2 (`validate_verdict`, `core70.validate_dispositions`, `outcome_from_dispositions`). The outcome comes only from `core70.outcome_from_dispositions`.
- Withheld files: `run-identity.json`, `profile-snapshot.json`, `capability-manifest-snapshot.json`, `installed-package`, `adapter-artifacts`, `containment-realization.json`, `evidence-integrity.json`, `normalization-map.json`. Removed summary keys: `arm`, `subject_commit`, `profile_key_sha256`, `run_identity_sha256`, `adapter_command_identity`, `runtime_observation`.
- Not withheld and identifying, and redaction that alters content: see F-7 (verified on a retained run by calling `copy_redacted` on its evidence). The blinding is partial, as design §4.4 already admits; the byte counts and commit hashes were not part of that admission.
- The evaluator uses the executor's model in the committed profile (F-7a).

## 5d. Retirement and the relay

- Tombstone `eval/RETIRED-MODULES.md`: all 13 module and 9 test commit hashes and line counts match `git show f4a5127~1`. No Python file imports a retired module (`omp_rig` hits are the alias for `test_rig`). Residue in F-10.
- Relay functions and where they are exercised against the real relay (I did not run these; the S2 report says they passed):
  - **Credential separation:** `test_omp_integration.py` lines 193 (provider receives the sentinel only upstream), 742 (every credential environment name refused before launch), 823 (inference works while the credential home is denied).
  - **Single-endpoint egress with refusal logging:** line 951 (bash cannot reach the relay ports or external hosts; denials logged as `network_external_action`, all `blocked`/`deny`; the provider saw only the 3 authorised model calls) and 1075 (external local-IPC sentinel unreachable); the relay's own `refused` record path is unit-tested in `test_omp_units.py:306-334` with a mocked connection, and the integration test asserts that no refusal was needed.
  - **Activation-delivery proof:** `test_relay_integration.py` (every declared root delivered at request 0 and counted as entrypoint-only; harness injection; every `INTEGRITY_FAULTS` delivery fault refused as INADMISSIBLE).
  - **Turn cap:** `test_omp_integration.py:565` (`max_turns=3`: `turn_cap` termination, `budget_exhausted` observer record, the fourth request never reached the provider).
- The pins test is `test_harness_integration.py::test_pin_mismatches_refuse_the_run_and_every_pinned_input_changes_run_identity` (ran green here).

## 5e. Line counts (design §6 scope: every `.py` under `eval/` and `qual-v2/`; tests are `test_*.py` and `stand_in_provider.py`)

Recomputed: **non-test 10,303**, **test 4,541** (`splitlines` and `wc -l` agree). The S2 report and SD-R14 say 10,304 and 4,541, so the measured size is one line below the figure the stakeholder accepted: within SD-R14. Excluded from scope: `qual-v2-history/` (205 lines, F-11) and `requal71/`. S3 added no Python in scope.

# 6. Q5c pre-measurement (O-11)

Recomputed from `wc -c` of the generated `dist/` files and from the 6.5 figures in `STAGE-A-STATIC-PREMEASUREMENT.md` (T1/T8 entrypoint-only 8,360 B; T7 owner mode 25,188 B = 8,360 + 16,828):

| Quantity | Recomputed | Record |
|---|---|---|
| D4 entrypoint | 15,799 (7.1: 15,463; 6.6: 7,057) | same |
| Workflow owner | 20,307 (7.1: 20,307; 6.6: 17,743) | same |
| Scientific-inspectability owner | 46,131 (7.1: 45,958; not present in 6.6) | same |
| T1/T8 and T7 entry cap, limit with 512 B, headroom | 16,720; 16,208; 409 | same |
| T7 workflow-owner mode: 15,799 + 20,307; cap; limit; headroom | 36,106; 50,376; 49,864; 13,758 | same |
| T1/T8 run that also reads the inspectability owner | 61,930, over the limit by 45,722 | same |
| T7 workflow-owner run against a 6.5 median in entry mode | 36,106, over 16,208 by 19,898 | same |
| T7 workflow owner plus inspectability owner | 82,237, over 49,864 by 32,373 | same |

**Judgment.** "No static breach under the rule as written" is correct: the two observed modes of the 6.5 and 6.6 runs on these routes both fit, and the 512 B margin is already inside the 16,208 B limit. The risk list is honest about the main exposure (an owner read on T1/T8 breaches the cap by 45 KB; the record also says growth of the entrypoint spends the 409 B headroom). Weaknesses: (i) the result line says "two named risks" while three are tabulated; (ii) the list omits an effect of the conservative shell count (F-1's repair makes it larger): one `ls` or `wc` that names the package directory is counted as a full read of every file below it (the relay test shows `entry + references`, about 430 KB of references plus the 15.8 KB entrypoint), so a plausible shell listing on T1/T8 would breach regardless of whether the owner was read; S4 should report how many runs are affected; (iii) the 6.5 denominators are the historical planning figures, not fresh paired runs (the record says so). No X6 stop is triggered by the static measurement; the three risks and (ii) go to the stakeholder before any campaign, as the design already requires.

# 7. S1 and S3 detail worth recording

- The S1 block in each of the four role entrypoints and two specialists equals the independently re-derived subset (validator and test both). The numbering check shows elements 1 and 4 visibly numbered everywhere they appear, as elements 3 and 6 refer back to them.
- Frozen 7.1: orchestrator files byte-identical to `58fd67b`; the snapshot generator now pins their blob hashes; `profile_id_for_version("7.1.0")` still returns the 7.1 profile.
- The 8.0 workplan edit is one new subsection; nothing else changed.
- No text in the changed files states 7.2.0 is qualified, accepted or ratified; CHANGELOG and the disposition record both state the opposite. README has no mutable release identity and still routes to `CHANGELOG.md` and `PROTOCOL-RELEASE-STATE.yaml`.

# 8. Disposition and next steps

**PASS WITH GAPS.** Repair F-1 to F-7 and decide F-9; apply the documentation lines of F-12 to F-14; add the F-1 to F-6 test cases; then run a delta check limited to the touched files, `git diff HEAD -- source dist` (must be empty), and the commands in section 2. After that, the 7.2.0 identity may be frozen with this record as the Review reference. F-8, F-10, F-11 and F-15 may follow in S4 preparation, with F-10's stale executor profile re-frozen before any live run.

# 9. Delta re-check (same day, after the author's repairs)

Scope: only the delta in the staged working tree against the findings above (`D4-PROTOCOL-7X-S3-IMPLEMENTATION-REPORT-2026-10-07.md` section 2). Same rules: only this record was edited; nothing committed; no live run; the relay and integration suites were not run (the author reports 6 and 54-with-fix OK).

## 9.1 Final verdict: PASS

No Serious Challenge and no blocker. Every pre-freeze gap (F-1 to F-7) is repaired in the code I could test; the residuals below are minors or S4-preparation items and none can change `source/` or `dist/`. **The 7.2.0 identity may be frozen subject only to the two stakeholder decisions in the S3 report section 3** (O-8 placement; budget floor), plus the documentation touch-ups in 9.5 that need no review.

## 9.2 Commands re-run

| Check | Result |
|---|---|
| `git diff HEAD -- source dist` | `source/` changes: `PROTOCOL_VERSION` and the versioning-reference profile list only. `dist/`: 41 files, 41 insertions and 41 deletions, all version tokens (the `**Governing version.**` line in 7 entrypoints, `PROTOCOL_VERSION`, `protocol-manifest.json`, the versioning reference, two template front-matter `protocol_version` lines, zips and `BUILD_INDEX.json`); after normalizing 7.1.0 and 7.2.0 the changed lines are identical. A fresh `build_skills.py` tree is byte-identical to `dist/skills`. No skill content changed |
| `tests/` | 429 OK (3 remote skips) |
| `generate_protocol_snapshot.py --check`, `validate_packages.py`, `check_dist.py`, `git diff --cached --check` | OK; unstaged diff is empty |
| `test_omp_units` | 67 OK |
| `test_portable70 test_harness_integration test_control_path_policy test_omp_eval test_mcp_stdio` | 59 OK |
| `qual-v2/test_h4.py` | 16 OK |
| Line counts (design §6 scope) | **10,358 non-test, 4,669 test**: equal to the S3 report; +55 and +128 over my 10,303 / 4,541 |
| `PROTOCOL-RELEASE-STATE.yaml`, `keys/`, `*-HISTORICAL.*` | unchanged |

## 9.3 Per-finding disposition (independent)

| ID | Status | Evidence |
|---|---|---|
| F-1 | **Repaired, with residuals D-1 and D-2** | I re-ran 18 shell forms and 8 native forms against `package_bytes.account`. Now counted: double-quoted and single-quoted paths, `bash -c '...'`, `$(...)` and heredoc bodies, root without a slash, `cd /opt/ssdp/skills && cat rel`, `cd /opt && cat ssdp/skills/...`, `cd / && cat opt/ssdp/...`, `grep -r ... /opt/ssdp/skills`, `find /opt/ssdp ... | xargs cat`, `ln -s /opt/ssdp/skills ...`, `~/../opt/s*/skills/...`, `..` beside a package path (whole tree), native `grep`/`glob` on the root, a sub-directory or a file, and a native grep with a `glob` argument. Not counted: see D-1 and D-2 |
| F-2 | Repaired | `harness70.py:806` is now `entry` only when every consumed file is `<skill>/SKILL.md`; the relay test covers a workflow-owner read. A read of another role's `SKILL.md` or of `PROTOCOL_VERSION` is `owner`/`entry` accordingly; any whole-tree shell hit is `owner` (conservative) |
| F-3 | Repaired | Dropping all T3 runs now gives Q5e EXPOSURE; Q4d with no B1/B2 observations gives EXPOSURE; Q5f requires T1/T7/T8 with 3 runs. One new defect: D-3 |
| F-4 | Repaired, stricter than the contract | Unequal episode sizes give EXPOSURE (a probe with one 3-part episode: EXPOSURE). Threshold stays 34 for 48 parts in 12 episodes. See D-4 |
| F-5 | Repaired | B2 with all Q4a items erroneous now gives INSTRUMENT_FAIL (diff 36 against limit 26) |
| F-6 | Repaired | Inadmissible candidate T1 runs give EXPOSURE (fewer than 3 admissible), not PASS |
| F-7 | Repaired in code; profile open | The wrapper refuses an evaluator whose `agent_model` equals the run's `profile-snapshot.json` model before loading the adapter (test added). Redaction is narrowed to `SSDP`/`Protocol` + number, bare `x.y.0` SSDP versions and `p65`-`p72` labels; `version 2`, `aqpipe 0.7.1`, package pins and dates are untouched. `_scrub` removes the arm, commit, package hash, entrypoint and owner byte counts, `pair_order`, package identity and read-mode keys from every `.json` and `.jsonl` at any depth. On the retained 7.1 and 6.6 runs the subject commit prefix and the `22f4bdba`/`58fd67ba` strings no longer appear. The committed evaluator profile still equals the executor's model, so a real assessment is refused until it is re-frozen on a different model (fail-closed, stated in the S3 report) |
| F-8 | Partly repaired as reported | `families_report` gives per-family counts, scores and the worse-than-B1 flag; the Q5a flip uses the candidate's own run count. Matched-mode comparison and the error-kind flag are deferred to S4 preparation, as the report says. See D-5 |
| F-9 | Open, stakeholder | See 9.6 |
| F-10 | Repaired except the stale profile | Superseded banners on the plan and runbook (checked); dead Claude branch removed from `core70.py` (diff checked, tests pass). `omp-primary-flash-executor.json` still pins `package_ledger.py`/`package_premise.py`; the report lists it as re-freeze before S4 |
| F-11, F-12, F-13, F-14 | Repaired | SD-R14 note records the 205-line move; the history lifecycle sentence now cites the Review record without claiming a verdict; CHANGELOG states the two byte-identity exceptions and "carries forward ... drops only the requirement to load the owner"; the design/contract front matter name SD-R13 and SD-R14; the disposition record says "never released or listed in `PROTOCOL-RELEASE-STATE.yaml` ... ordinary working-branch history"; the Q5c record says "three named risks and one accounting caveat" and states the whole-package inflation (2,774 KiB). Nothing in the changed text claims 7.2.0 is qualified, accepted or ratified |
| F-15 | Repaired for F-1 to F-7 | New tests: `PackageBytesReach`, `PackageBytesAccount`, relay forms, H4 exposure/C(c)/Q5c/family cases, evaluator-model refusal and structural scrub |

## 9.4 New findings and residuals (none affects the 7.2.0 package)

| ID | Severity | Where | Finding | Minimal repair |
|---|---|---|---|---|
| D-1 | gap (fix before S4; does not hold the freeze) | `eval/package_bytes.py:55-66` (`process=False` skips the `/opt`/`ssdp` rule) | Native tools whose path or pattern is an ancestor or wildcard of the mount count 0 B: `grep {path: "/opt"}`, `grep {path: "/"}`, `glob "/opt/**/*.md"`, `glob "/o*/s*/skills/**/*.md"` (all verified at 0). The S3 report states the residual only for "a path assembled without writing `/opt` or `ssdp`"; here `/opt` is written literally | Apply `_OBFUSCATED`, and a bare `/` or `/opt` path, to native `grep`/`glob`/list actions too |
| D-2 | minor (declared residual) | same | Process commands that never write `/opt` or `ssdp` still count 0 B: `find / -name SKILL.md -exec cat {} +`, `grep -r 'Scientific checks' /`, `cat /o*/s*/skills/...`, python `glob('/'+'*/*/skills/...')`. The docstring (`package_bytes.py:7`), `harness70.py:749` and `core70.py:915` still say the count is "always an upper bound" | State the residual in those three places and in the S4 report; optionally treat a recursive search from `/` as whole-tree |
| D-3 | minor | `qual-v2/h4.py:213` | `sentinel` returns EXPOSURE at the first short route and drops the others, so a real FAIL on an earlier route (probe: both T2 sentinel runs failing, T3 absent) gives verdict INCOMPLETE with no `first_failing_gate`. Not a false PASS | Finish the loop, report the FAIL, then return EXPOSURE only if nothing failed |
| D-4 | minor, design note | `qual-v2/h4.py:119` | Q2 now needs equal-sized delegate episodes. Owed parts normally differ per episode (V and T apply conditionally), so the custodian must author equal-sized episodes or H4 must simulate the real sizes; stricter than contract §5 but fail-closed | Put the constraint in the S4/P3 work order, or simulate the actual sizes |
| D-5 | minor | `qual-v2/h4.py:250-261` | The family flag uses B1's own rate for p̂ and compares unscaled sums when the arm counts differ; contract §5 pools B1 and B2 (report-only, no gate effect) | Pool B2 when it has Q3 observations; rescale to the candidate's n |
| D-6 | minor | `eval/assess70.py:36-39, 218-221` | `Protocol 3` / `protocol 2.1` of a trial in project text still becomes `PROTOCOL-X`; a bare `7.2` ("skills-only 7.2 candidate") and `ssdp-` in `ssdp-protocol-7.2` survive; the evaluator copy still carries `activation` hashes of the injected entrypoint text, `accounting` hashes and, for package reads, `resource_sha256`/`resource_bytes` in `resource_access` events: consistent per-arm fingerprints that name no arm. The model-equality check compares exact strings and passes if the snapshot has no `agent_model`. The package text an agent reads is the known partial-blinding limit | Add `activation`, `accounting`, `resource_sha256`, `resource_bytes` (package paths) to the scrub; require `agent_model` in both profiles |
| D-7 | minor, calibration | `eval/package_bytes.py:46-65` | Any process text containing `/opt` or `ssdp` is a whole-tree read (2.8 MB, against a 16 KB cap). Conservative and now documented in the Q5c record; S4 should report how many candidate and 6.5 runs are shell-counted | Report only; no code change needed before S4 |

## 9.5 Documentation touch-ups (no review needed)

- `history/SEMANTIC_EVOLUTION.md` harness bullet: when the stakeholder decides the budget floor, change "10,304 / 4,541" there, in SD-R14 and in the workplan O-6 row to the adopted figure.
- Update the three "always an upper bound" sentences with the D-2 residual.

## 9.6 View on the two open stakeholder decisions (not decided here)

1. **O-8 placement.** The inputs are blind custodian material (SD-2), so D4 cannot author them without breaking custody; moving them to the S4/P3 custodian work order is the only placement consistent with the workplan's own custody rule. If adopted, the amendment should (a) keep Precondition C exercised by the synthetic cases in `test_h4.py` as the S2 evidence, (b) make "frozen calibration set, oracle fixtures and redacted evaluator input exist and pass Precondition C" an explicit entry condition of S4's campaign step, and (c) list the two profile re-freezes (evaluator on a different model; executor profile without the retired module pins) as S4 entry conditions. Until the workplan says so, O-8 remains an unexecuted required check.
2. **Budget floor 10,358 / 4,669.** I recomputed 10,358 non-test and 4,669 test lines on the design §6 scope; the +55 / +128 over the Review's counts come from the F-1 to F-7 repairs and their tests, and no function was dropped. The earlier figure (10,304 / 4,541) was already one line above my count. The decision should state whether the 205-line history script counts (10,563 if counted) so that the floor is unambiguous, and that the next growth must show its line cost (X5).

## 9.7 Freeze statement

`source/` and `dist/` carry only the 7.2.0 version-bump effects; S1 and S3 content passed the first Review unchanged. With the two stakeholder decisions made and 9.5 applied, the 7.2.0 identity may be frozen with this record and section 1 as the Review reference. D-1 and the profile re-freezes should be closed before S4 begins; D-2 to D-7 may follow in S4 preparation.
