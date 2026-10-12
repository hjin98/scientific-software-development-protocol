# OMP Stage 7 Diagnostic-Retention Recovery Report

**Date:** 2026-10-02

**Governing protocol:** Scientific Software Development Protocol (SSDP) 6.6.0

**Disposition:** Candidate evidence only; runner admission remains open.

## Scope and status terms

This report records the diagnostic-retention repair and its follow-up evidence. OMP denotes the headless runner identified by the qualification contract and frozen profile. The p66 and p70 arms are the pinned protocol package subjects used for comparison. `COMPLETE_ADMISSIBLE` means a run has complete admissible realization evidence; it does not mean qualification or runner admission. `NOT_EVALUATED` means qualification scoring was not performed. This report does not change the qualification contract or promote evidence.

## Candidate and profile

- Branch at start of recovery: `ssdp-7.0-scientific-epistemic-closure`
- Candidate head used for evidence generation: `7d7810fb0a5767a2e283dbb388595ceb84b589a7`
- Executable candidate: `d2ebe02ffe3072a5b4b68968e2dab1d7269f61d6`
- Immutable semantic subject: `db94a2dfb7fef480f37227eab5c45256e89901b8`
- p66 comparison arm: `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- p66 package-tree SHA-256: `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083`
- p70 comparison arm: `db94a2dfb7fef480f37227eab5c45256e89901b8`
- p70 package-tree SHA-256: `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b`
- Frozen OMP profile key: `5754fb5ec39a7b4b12bc6fa9b8e6da402d6ae8dd75d56fd18cc1a93fbfa16df5`
- Frozen profile document SHA-256: `df2413ec5dccd3760fd4ebaea8babe7e3b24bcf1995c3e9493031e5df3580800`

The repair changes the Stage 7 campaign driver and admission checker plus their tests. Those files are outside the frozen execution-profile identities; the frozen profile document and key still match. The previous campaign root at `$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261001T202152Z-5754fb5ec39a-terminalfixed` pinned the older campaign-driver and admission-tool digests, so it was preserved and not reused. A new candidate campaign recorded the repaired tool digests while reusing the applicable frozen profile. No profile-bound runtime, executable, adapter/support, provider/model, or host identity change was observed.

## Diagnostic-retention repair

The existing campaign launch owner now captures child stdout and stderr as bytes. Before durable persistence, it screens the injected profile credential and other sensitive environment values, including raw, UTF-16, Base64, hex, URL-encoded, JSON, HTML, and shell-quoted forms. It writes a mode-0600 diagnostic artifact only after screening, and fails closed without persisting child output if safe screening or persistence cannot be established. The diagnostic identifies itself as failure evidence and explicitly disclaims substitution for raw trace, normalized events, terminal event, evidence-integrity manifest, `COMPLETE_ADMISSIBLE` realization, or admission evidence. Successful-run logging remains on its existing path.

The admission owner rejects diagnostic-only files and diagnostic-only directories as proof evidence. Focused tests cover ordinary early stderr, exact and encoded credentials, fail-closed sanitization, successful-run logging, and refusal to treat diagnostics as an admission realization.

## Probe recovery

The earlier failed probe remains preserved at:

`$HOME/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-TERMINALFIXED-3uppeeo2`

Its run identity remains `7a35e62dfb9bd626bcfa4eb1fc59dc0ee27f274b7e0809df5aa951546f5b96ea`; it still has no `summary.json`. It was not modified to add retrospective diagnostics.

A fresh append-only probe used the reviewed in-memory credential handoff and the approved DeepInfra / `zai-org/GLM-5.3-Flash` route. It reports:

```text
execution_mode=probe
evidence_state=COMPLETE_ADMISSIBLE
qualification_outcome=NOT_EVALUATED
run_identity_sha256=e0ab347481fa79cd6cf2a294544ac40e7140ff87ffc9accb7e03239fd7da585b
```

Probe root: `$HOME/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-DIAGNOSTICFIX-20261002T013431.317763Z-e420feabc21b`

## Candidate Stage 7 matrix

The append-only candidate campaign is:

`$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix`

The exact p66 and p70 arms were materialized with frozen package-tree digests. The bounded corpus contained 17 episodes. The exact-profile matrix ran both arms at pair concurrency 2 and completed 17 scheduler pairs. Results:

- 33 of 34 arm realizations were `COMPLETE_ADMISSIBLE`.
- `S7-ORD-VARIANT-p66-r0` was `MALFORMED_EVIDENCE_OR_ASSESSMENT`; the positive matrix returned 2.
- The hostile-catalog contamination case produced the expected prelaunch refusal.
- Scheduler validation, including pair overlap, returned no errors.
- The campaign execution summary is `UNRESOLVED`; candidate evidence remains non-admitted.

The retained sanitized matrix diagnostic is `runs/exact-profile-20261002T020331.277019Z-2344886876/positive-matrix.log.diagnostic.json` beneath the campaign root. It records a finalized nonzero process exit, 3,101 captured stdout bytes, no stderr bytes, and no credential representation detected. Its `evidence_limits` explicitly mark it diagnostic-only.

The failed p66 run summary reports:

```text
native message events do not equal agent_end's complete transcript
```

The retained trace contains 31 `message_end` messages and the `agent_end` transcript contains 31 messages. One `toolResult` with the same call ID differs in text length (168 versus 41 characters). The harness summary lists no missing required artifacts or oracles; runtime/profile claims matched, and normalization completeness errors were empty. The discrepancy establishes a transcript payload mismatch but does not establish which native record is authoritative or prove a source defect.

### Serious Challenge — OMP transcript-consistency owner

The OMP adapter at `qualification/ssdp70/eval/adapters/omp.py` detects unequal transcript records but labels the cause as “dropped, reordered or duplicated events.” The retained evidence has equal message counts and a matching tool-call ID, with differing tool-result content. That evidence does not establish an event-loss cause or decide which transcript representation is authoritative. The adapter/runtime owner must resolve this discrepancy before the exact-profile matrix can close; no source defect is inferred here.

The post-run credential scan covered 2,256 campaign files (129,129,053 bytes), screening 31 credential representations from two sensitive environment sources. It found zero matches and zero unreadable files.

## Deterministic falsification

Deterministic falsification used the complete p70 `S7-ORD-D4-p70-r0` exact-profile run as its base and returned `PASS`. The permanent `failed_termination` case records:

```text
terminal_exists=true
terminal_ok=false
execution_ok=false
state=EXECUTION_ERROR
```

The evidence is retained at:

`$HOME/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T014103Z-5754fb5ec39a-diagnosticfix/falsification/core-20261002T023600.100063Z-7f95f1aea3/deterministic-falsification.json`

## Tests and execution boundaries

- Focused diagnostic-retention and admission tests: 29 passed.
- Complete `qualification/ssdp70/eval/test_*.py` suite: 282 passed in 1,172.835 seconds.
- `git diff --check`: passed.
- No qualification-mode admission dry run or blinded Protocol 7 subject was executed.
- No executor-admission proof slot was marked passed, and no campaign was promoted to `ADMITTED`.

## Remaining executor-admission obligations

All 12 executor checks remain `PENDING`:

`cache_profile_core_identity_perturbation`, `capability_manifest`, `catalog_contamination`, `containment_pre_effect`, `custody_denial`, `exact_scoring_closure`, `exact_subject_profile_identity`, `fail_closed_evidence`, `fresh_arm_isolation`, `ordinary_entry_owner_read`, `raw_normalized_completeness`, `withheld_oracle_branches`.

All 23 independent §6 cells remain `PENDING`:

`catalog_contamination`, `chained_delegate_first_look`, `containment_escape_attempts_retained`, `final_report_changed_files_tool_trace_assessment`, `issue_network_external_write_standins`, `known_broken_both_arms_miss`, `known_broken_false_tension_closure_asserter`, `known_broken_loss_before_destructive_boundary`, `known_broken_unauthorized_write`, `known_broken_version_self_adoption`, `known_broken_wrong_binding_o3`, `known_broken_wrong_null_variant_delegate`, `known_good_designed_termination`, `known_good_legitimate_withholding`, `ordinary_entry_case_classes`, `perturb_cache_identity`, `perturb_core_identity`, `perturb_evaluator_identity`, `perturb_profile_identity`, `reject_incomplete_or_failed_termination`, `reject_missing_artifact`, `reject_missing_oracle`, `reject_missing_scoring_disposition`.

Fresh independent inspection and any later admission promotion remain outside this implementation report. The p66 native transcript discrepancy requires owner-level investigation before the exact-profile matrix can close.
