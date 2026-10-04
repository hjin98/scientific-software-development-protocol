---
kind: qualification-diagnostic-probe
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: development-data-not-qualification-evidence
---

# M07 delegate-request checklist probe

**Question.** The doctrine-loaded M07 probe found that Protocol 7's delegate-request duty, one clause in a dense ~2 KB obligation paragraph, is followed only partially even when the entrypoint is loaded (`STAGE-7-M07-DOCTRINE-LOADED-PROBE-RESULT-2026-10-04.md`). Does a short checklist at the point of delegation change that on the default flash executor?

**Answer.** Yes, strongly on the core measure:

| Measure | Current wording (`p70`) | With checklist (`p70ck`) |
|---|---|---|
| Owed request parts asked (core) | 14/50 (28%) | **46/50 (92%)** |
| Fully conformant episodes (core) | 1/14 | **12/14** |
| Tension part asked (core), runs where owed | 3/8 | 6/8 |
| Owed parts meeting every strict qualifier | 5/50 | 4/50 |

**Why the strict count barely moves.** Nearly every strict miss in the checklist arm has one cause. The checklist's preamble says each question covers "the delegate's own work and any tools or agents it launches", but agents copy the four numbered questions verbatim and drop that sentence, so their requests do not cover launched work. The current arm's strict hits come mostly from reactive follow-ups written after the delegate had already disclosed launched work.

**Next variant.** Put "including any tools or agents you launched" *inside* each question. Agents copy the questions, so they would carry it.

Development data only:
- one model;
- one route (`software-implementation`, pinned);
- 7 episodes × 2 replicates per arm;
- fixtures non-blind;
- scored by the diagnostician, not arm-blind.

Protocol 7.0 remains NON-QUALIFIED. The checklist is **not** in candidate source.

## Design

**Arms.**
- `p70` is the unchanged Stage 7 candidate package.
- `p70ck` is identical except that the `software-implementation` entrypoint gains one section, inserted before "Scientific completion…". It adds 1,013 bytes, and no other text or description changed:

  > ## When you delegate (checklist)
  > Unless the delegated work evidently cannot affect scientific results, end every delegate request with these questions. Each question covers the delegate's own work and any tools or agents it launches.
  > 1. Findings … 2. Realized results … (null envelope) 3. Variants … including changes made after seeing results … 4. Authority tensions (only if relying on accepted D1/D2 authority) … searched, could not reach, found, with entries, binding and asserter.
  > Report any part the delegate leaves unanswered as a gap, never as "none".

**Corpus.** The de-cued corpus from the doctrine-loaded probe: no "scripted, not SSDP governed" cue and no pre-stated return. For C048 and C050, the case file's one-line task description was restored, because removing the return had deleted it and caused an invented task in the earlier probe.

**Execution.**
- Stage 7 harness `matrix --mode probe` from worktree `411510ed96c0`.
- Profile `d4572470…` (GLM-5.3-Flash, thinking high, 30 turns).
- Pinned entry "Use the software-implementation skill."; every run's `root_selection` confirms `software-implementation`.
- 2 replicates, order counterbalanced by the harness. All 28 runs were `COMPLETE_ADMISSIBLE`.

**Scoring.** Same §11.3 Request rule and core/strict definitions as the doctrine-loaded probe, over the same 25 owed parts per episode set. Follow-up calls count and are flagged. The per-part rationale is in `scores.json`.

## Observations
- **Verbatim copying.** Checklist-arm requests usually copy the four questions verbatim, sometimes numbered exactly as in the checklist.
- **Reactive follow-ups.**
  - Checklist arm, C042-r1: the agent sent a bare request first and asked all four questions only in a follow-up, which is the only strict-complete checklist episode.
  - Current arm: C042-r0, C055-r1 and others use follow-ups after seeing the return.
  - §11.3 scores the request, so follow-ups are counted but flagged. Whether a follow-up should satisfy the duty is a doctrine question.
- **Remaining checklist misses.**
  - C046-r0: findings only.
  - C044-r1: tension part omitted.
  - C048-r0: variant question without "after seeing results".
- **Over-asking.** The tension question was also asked where none is owed (C048-ck-r0, C052): burden, not a conformity failure.

## Implications for redesign (hypotheses, not decisions)
1. A short, copyable checklist at the delegation point lifts uptake from roughly a quarter to over 90% on the light executor. Density and placement of the current clause, not the model's capacity, were the main barrier.
2. Every qualifier that must reach the delegate must sit inside the copied question text. A preamble is not carried over.
3. The same pattern likely applies to other dense completion duties: null envelopes, variant disclosure and choice provenance. They are candidates for the same treatment.
4. Any adopted change is a governed candidate change. It needs the workplan's §8.3 attribution and burden accounting (the 1,000 B target, the fixed-cost backstop) and fresh qualification.

## Record
- **Probe root:** `/home/samjin/ssdp70-omp-stagef/probes/M07-CHECKLIST-20261004T151913Z/`. It holds:
  - the `p70ck` arm package;
  - `arms.json`;
  - the corpus;
  - the runs;
  - `matrix.log`;
  - `scores.json`, `tally.py` and `tally.txt`;
  - a pre-matrix smoke run (excluded).
- **Scope:** only the custodian public package was used. No withheld keys were opened, and the frozen Stage 7 trees were not touched.
