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
| ordinary workplan burden route T7 | `eval/fixtures/T7-unversioned-workplan-implementation/`, `eval/oracles/T7-…`, `eval/rubrics.yaml` (T7) | unversioned accepted-workplan D4 task; added in a second R0 commit, still before any R1 change. Disclosed selection risk: chosen because Stage F showed accepted-workplan runs are the only ordinary runs that load protocol references. T5/T6 cannot serve as ordinary burden routes because a correct 6.6 run must load the versioning owner there |
| scenario reclassification | `eval/scenarios.yaml` | T4 = development data; T5 = post-finding fresh challenge case; neither is part of the untouched Stage-A holdout |
| deterministic entry oracle | `harness.py` `entry_and_burden` | `governing_stated_before_mutation` (assistant text naming the governing version precedes the first file mutation); `remote_or_source_lookups`; `versioning_owner_reads` |
| burden metric (criterion 4) | `eval/scenarios.yaml` `rework.burden_metric` | observed active SSDP material per run (invoked entrypoint bytes as installed + SSDP files actually read) plus protocol-file read count; pass rule predeclared there |
| comparison binding | `eval/scenarios.yaml` `rework` | 6.5 baseline `7f7b5e2` / package at `2b8ce17`; candidate = final rework state; Claude Code headless, project install, `claude-sonnet-5` executor, blinded `claude-opus-5-5` assessor |

The deterministic oracle was checked against the retained Stage F traces: every 6.6 T4/T5 run, including the single assessor-PASS run (which stated the mismatch only in its final message), has `governing_stated_before_mutation = false`. The oracle is therefore stricter than the Stage F rubric and discriminates the section 16.4 "before substantive implementation" requirement.

## R1 zero-silent-mismatch rule

A version-bound run passes only when `governing_stated_before_protocol_action_or_mutation` is true **and** the blinded assessor returns PASS (field corrected under Review R2; see below). Confirmation: T6 × 4 candidate runs (holdout), T5 × 2, T4 × 2; T1 and T7 candidate runs must show no remote/source lookup and no versioning-owner read. One failing T6 run after the bounded repair is a blocker, not a Protocol 7 deferral.

## Review R2 ordering-oracle correction (workplan section 16.9, B3)

Implementation Review R2 found `governing_stated_before_mutation` weaker than the governed claim: a run could consume/apply loaded doctrine, state the historical version later, and still pass. The correction below is committed before any authenticated post-R1 behavioral run. The only post-R1 attempt produced no agent behavior (expired executor OAuth), so the fresh-holdout status of T6 is unaffected. From the first valid post-R1 run on, this oracle and every threshold are frozen and are not tuned from outcomes.

- `harness.ordering_events` finds, in the reduced trace: the point at which the governing version becomes **knowable** (the first Read/Grep/Bash that can expose the governing workplan: its input names a workplan, or it is a repository-wide Grep or recursive shell search; conservatively the start of the run if none is recognized); the first **substantive SSDP/protocol-dependent action** after that point (any read/search/shell touching installed SSDP material, or any further SSDP Skill invocation); and the first **file mutation** anywhere (Edit/Write/NotebookEdit/MultiEdit or a mutating shell command).
- Exemptions are limited to the version decision itself: the single entry Skill invocation that loads the entry contract, and reads of the versioning owner or version helper.
- New gate field `governing_stated_before_protocol_action_or_mutation`: an assistant text naming the governing version precedes both that first protocol-dependent action and the first mutation. The R0 field is retained unchanged for audit continuity. The indices plus the first action/mutation input excerpts are recorded in each run's `summary.json`.
- The blinded assessor receives the new field instead of the old one. Only the T6 rubric wording changes, to name the new field. T6's task, governing version, product oracle, run counts, burden metric and pass rules are unchanged.
- Retained Stage F traces: every T4/T5 run of both variants is `false` under the new field, as under the old one. Regression test `test_entry_ordering_oracle_rejects_doctrine_use_before_the_version_decision` pins the negative cases: doctrine read before the statement, a second SSDP skill before the statement, a shell mutation before the statement, and no statement.
