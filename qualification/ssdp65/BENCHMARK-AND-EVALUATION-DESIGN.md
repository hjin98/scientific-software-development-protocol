---
kind: ssdp65-preregistered-evaluation-design
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
governing_protocol_version: 6.4.0
authority: non-normative-preregistration
p0: 55c085261eb827e3047637d045a8e6917ea6b962
p1: NOT_YET_DESIGNED
registered_before_candidate_design: true
created: 2026-09-24
---

# Pre-registered Evaluation Design: P0 = Protocol 6.4 vs P1 = candidate

## 1. Status and purpose

This design is registered **before any Protocol 6.5 candidate exists**. Its purpose is to prevent success from being redefined after `P1` is observed. A later change is permitted only through §8 (benchmark-defect repair), never because a candidate performs poorly.

The outcome "no successor; Protocol 6.4 survives" is an admissible, pre-registered result.

## 2. Background and terminology

- **P0** — frozen control, Protocol 6.4 at repository state `55c0852` (see `P0-BASELINE-BINDING-PROTOCOL-6.4.md`).
- **P1** — any candidate protocol produced on the successor branch after the defect model is frozen.
- **Arm** — one protocol (P0 or P1) supplied to an agent as its skill/reference package.
- **Trajectory** — the full sequence of reads, tool calls, edits, claims and stop decisions an agent makes on a task, not only its final artifact.
- **Mutant** — a deliberate single-point change to canonical protocol text used to measure whether an oracle (test suite, Review, or agent) discriminates semantic change.
- **Lossless paraphrase control** — a rewording that preserves meaning; an oracle that rejects it exhibits a false positive.
- **Holdout** — benchmark material withheld from the designer of P1 and used only after P1 is frozen.

## 3. Evaluation dimensions (quality vector)

`Q = (C, F, A, E, G, U, S, K)` is kept multidimensional. No scalar aggregate is used for acceptance.

| Dim | Operational observable(s) per task/trial | Direction |
| --- | --- | --- |
| **C** technical correctness | final artifact correct against a task oracle written before trials (tests, reference solution, or expert rubric) | higher |
| **F** defect discovery | true defects found / planted-or-known defects; root cause identified at correct owning layer (Y/N) | higher |
| **A** authority preservation | count of authority violations: upstream semantics changed by downstream edit, spec rewritten to fit code, tolerance widened without D2 owner, self-accepted gated change, derived artifact edited as truth | lower |
| **E** evidence quality | fraction of material claims in the final report with an admissible binding `(claim, evidence, exact subject, validity conditions)`; count of stale/proxy/unexecuted evidence presented as confirmation | higher / lower |
| **G** generalization | performance on holdout and novel cases relative to development cases | non-inferior |
| **U** useful autonomous completion | task completed without unnecessary human escalation; false-positive blockers (blocking claims without a genuine blocking defect); false-negative blockers (genuine blocker missed) | higher / lower / lower |
| **S** structural simplicity | protocol: independent concepts, words in always-loaded kernel, duplicated normative statements, number of lifecycle stages/identities; agent output: accidental machinery introduced (wrappers, fallbacks, duplicate state) | lower |
| **K** resource cost | protocol words loaded, files read, tool calls, wall time, review/repair iterations, human interventions, qualification compute | lower |

Protocol-level (text) observables, measurable without agent trials:

| Observable | Instrument |
| --- | --- |
| Semantic-mutant detection rate of the acceptance workflow | a mutation probe (inject one semantic change into canonical source, regenerate descendants, run the documented acceptance workflow) over a pre-registered mutant set plus a fresh post-P1 mutant set (§6.4) |
| Lossless-paraphrase false-positive rate of the acceptance workflow | meaning-preserving rewording controls in the same probe |
| Canonical/generated/project consistency (brief §15, §33) | every surface that asserts a version, lifecycle or authority identity agrees with its owner |
| Duplication census (brief §13) | count of restatements of each generic rule outside its owner; divergences among restatements |
| Always-loaded context | words in role entrypoint + kernel + owning domain reference for each role |

## 4. Acceptance criteria (decision rule for `P1 ≻ P0`)

`P1` may be proposed for acceptance only if **all** of the following hold:

1. **No unacceptable regression.** On development, novel and holdout sets, P1 shows no increase in authority violations (A) and no decrease in correctness (C) or recovery correctness, beyond trial noise, for any supported model in §7.
2. **Material improvement with evidence.** P1 shows improvement, supported by paired per-task evidence, on at least one dimension directly tied to an admitted defect (Phase III), and the improvement survives on holdout material (G).
3. **Every normative change is traceable** `evidence → defect → violated invariant → root cause → repair → qualification`; untraceable changes are removed.
4. **Lossless preservation.** A complete 6.4 → P1 preservation/supersession map classifies every accepted 6.4 normative element as preserved, clarified, generalized, compressed, relocated, superseded or intentionally removed, with evidence for non-preserved items.
5. **Causal usefulness.** Each major new or compressed invariant survives ablation (`P1` vs `P1 − I`) on at least the case(s) it was designed for, or is removed.
6. **Oracle adequacy.** The P1 acceptance workflow detects a strictly larger share of the pre-registered semantic mutant set than P0, without an increase in paraphrase false positives, **and** this also holds for a fresh mutant set authored after P1 is frozen by someone other than the P1 author.
7. **Independent assembled-candidate Review PASS** under the rules in the workplan, performed by a context that did not author P1.
8. **No required check unexecuted.** Any required dimension that could not be measured is reported as unavailable and blocks acceptance unless the governing human authority explicitly accepts the limitation.

A smaller P1 may be superior; an unchanged 6.4 may be superior; a larger P1 is not presumed superior.

## 5. Benchmark sets

### 5.1 Development set (used by a reviewer to derive its defect model — therefore not usable as evidence of generalization)

Each diagnostic reviewer declares its own development set inside its own sealed directory (reviewer A: `reviewer-a/PHASE-II-FALSIFICATION.md` §"Development set"). Reviewer A's development set consists of Protocol 6.1–6.4 in-repository history (workplans, qualification and review records, Git history of `source/`) plus reviewer A's own executed probes. Its case-level annotations are sealed from reviewer B until reviewer B's findings are frozen.

### 5.2 Novel adversarial cases (generated in this investigation; see reviewer-A Phase II for trajectories)

Novel cases are specified as scenario descriptions so they can be executed later as agent tasks under P0 and P1. Reviewer A's cases are recorded in `reviewer-a/PHASE-II-FALSIFICATION.md`; reviewer B generates its own set independently (see handoff).

### 5.3 Holdout (reserved; reviewer A has not read these and commits not to before P1 is frozen)

| ID | Material | Selection rule |
| --- | --- | --- |
| HO1 | Archived Protocol 5.x workplans `workplans/archive/PROTOCOL-5.*` and their qualification sets `qualification/long-horizon/`, `qualification/tool-routing/` | whole directories; reviewer A read only file names |
| HO2 | Scenario corpora `qualification/ssdp6/SCENARIOS*.md` (content) | whole files; only file names/line counts were observed |
| HO3 | Downstream project history (for example `hjin98/mdstats`), if repository access is later granted | all SSDP-governed episodes; not accessed in this pass (access was not granted) |
| HO4 | A fresh semantic-mutant set authored after P1 is frozen by a party other than the P1 author | ≥ 15 mutants across kernel, D1–D4, evidence, PEM, workflow and prompts, plus ≥ 5 lossless paraphrase controls |
| HO5 | Novel task set authored by reviewer B | reviewer B's own cases |

## 6. Trial protocol

### 6.1 Matched A/B trials
- Same repository snapshot, same task statement, same tools, same model, same budget; only the protocol package differs (`dist/skills` of P0 vs P1).
- Historical answers are withheld: tasks are reconstructed at the pre-repair commit with post-repair artifacts removed from the agent's view.
- At least 3 independent replicates per (task, arm, model) because agent trajectories are stochastic; report per-task paired differences and their spread, not only means.

### 6.2 Blind grading
- Final artifacts and trajectory summaries are graded with protocol-version identifiers redacted.
- Graders use rubrics fixed before trials. Where an LLM grader is used, a second grader family or human spot-check is used on a stratified sample, and grader disagreement is reported.

### 6.3 Trajectory measurement
Record for each trial: files and protocol references loaded, words of protocol loaded, tool calls, edits, claims made with and without admissible evidence, blockers raised (and whether genuine), escalations to a human, iterations, final disposition.

### 6.4 Protocol-text qualification
- Run the mutation probe against P0 and P1 with identical harness and mutant set.
- After P1 is frozen, obtain HO4 and repeat.
- Report detection rates and paraphrase false-positive rates separately.

### 6.5 Ablation
For each major new/compressed invariant `I` in P1, construct `P1 − I` (text removed/restored to 6.4 form) and rerun the case(s) that motivated `I` plus at least one holdout case.

## 7. Supported model envelope

The supported model set `M` must be declared before trials (at minimum: one frontier model and one smaller/cheaper model the project intends to support). Results are reported per model. An improvement for stronger models that harms weaker supported models must be surfaced explicitly and resolved by: keeping weaker-model scaffolding, dropping support, or introducing capability profiles — by explicit decision, not silently.

## 8. Benchmark-defect repair rule

If a benchmark element is later shown defective, record, in an appended dated section of this file:

```text
benchmark defect -> repair -> reason the old benchmark was invalid -> which results are affected
```

A benchmark element may not be removed or re-scored because P1 fails it.

## 9. Known limitations at registration time

1. Only one frontier model was available to the diagnostic author in this session; the independent second diagnostic pass is prepared as a handoff rather than simulated.
2. No agent A/B trials were executed during Phases I–III; the only executed protocol-level experiment is the P0 mutation probe.
3. Downstream-project history was not accessible in this session (repository access not granted); HO3 is therefore unexamined.
4. Reviewer A has read the development-set history; reviewer A cannot be blind to it. Generalization claims must therefore rest on HO1–HO5.
5. Trial infrastructure (agent runner, redaction, grading) does not exist in the repository and must be built or supplied before Phase VII; its absence is a blocking unavailable check for any P1 acceptance claim.
6. Agent behavior is stochastic and model-version dependent; results are bound to the exact model identifiers and dates used.
