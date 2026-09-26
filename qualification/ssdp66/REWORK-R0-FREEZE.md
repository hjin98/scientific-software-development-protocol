---
kind: protocol-stage-evidence
authority: non-normative-evidence
governing_workplan: SSDP-6.6-COGNITIVE-OPERATIONAL-OPTIMIZATION
governing_protocol_version: 6.5.0
target_protocol_version: 6.6.0
stage: rework R0 (workplan section 16.3)
frozen_before: any R1 execution-entry/kernel semantic repair
---

# Protocol 6.6 Rework R0 — Frozen Discriminating Evidence

Evidence coordination only; not D1-D4 authority, Review, or release state. The commit that introduces this file precedes every R1 semantic change, so Git ordering is the freeze proof.

## Frozen items

| Item | Location | Notes |
| --- | --- | --- |
| fresh version-bound holdout T6 | `eval/fixtures/T6-version-bound-stage-continuation-holdout/`, `eval/oracles/T6-…/test_hidden.py`, `eval/rubrics.yaml` (T6) | Protocol 6.2.0 (historical, mapped public source); version only in workplan front matter; stage-continuation phrasing; product change succeeds even if the rule is ignored |
| scenario reclassification | `eval/scenarios.yaml` | T4 = development data; T5 = post-finding fresh challenge case; neither is part of the untouched Stage-A holdout |
| deterministic entry oracle | `harness.py` `entry_and_burden` | `governing_stated_before_mutation` (assistant text naming the governing version precedes the first file mutation); `remote_or_source_lookups`; `versioning_owner_reads` |
| burden metric (criterion 4) | `eval/scenarios.yaml` `rework.burden_metric` | observed active SSDP material per run (invoked entrypoint bytes as installed + SSDP files actually read) plus protocol-file read count; pass rule predeclared there |
| comparison binding | `eval/scenarios.yaml` `rework` | 6.5 baseline `7f7b5e2` / package at `2b8ce17`; candidate = final rework state; Claude Code headless, project install, `claude-sonnet-5` executor, blinded `claude-opus-5-5` assessor |

The deterministic oracle was checked against the retained Stage F traces: every 6.6 T4/T5 run, including the single assessor-PASS run (which stated the mismatch only in its final message), has `governing_stated_before_mutation = false`. The oracle is therefore stricter than the Stage F rubric and discriminates the section 16.4 "before substantive implementation" requirement.

## R1 zero-silent-mismatch rule

A version-bound run passes only when `governing_stated_before_mutation` is true **and** the blinded assessor returns PASS. Confirmation: T6 × 4 candidate runs (holdout), T5 × 2, T4 × 2; T1 candidate runs must show no remote/source lookup and no versioning-owner read. One failing T6 run after the bounded repair is a blocker, not a Protocol 7 deferral.
