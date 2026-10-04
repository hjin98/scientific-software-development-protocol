---
kind: qualification-diagnostic-probe
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: development-data-not-qualification-evidence
---

# Stage 7 selection probe: stronger executor

**Question.** Stage 7's executor (GLM-5.3-Flash) loaded an SSDP skill in only 13/122 p70 runs. Is the low selection rate mainly a model-capability limit, or does it come from how tasks and the skill catalog meet?

**Answer: both, and the mechanism is specific.**
- The stronger GLM-5.3 selected a skill in **4 of 10** sampled episodes. Flash selected in **2 of 10**, both in a same-day rerun and in Stage 7.
- In both models selection is decided by one step: whether the model thinks to consult the skill catalog at all.
  - When it does, it nearly always loads a fitting skill (or correctly declines a non-scientific task).
  - When it doesn't, its reasoning never mentions skills and it goes straight to the case file.
- The stronger model makes that consultation step more often. It doesn't make it reliably: certain task framings never trigger it in either model.

Development data only: one replicate per cell, a 10-episode sample, scored from traces by the diagnostician. Protocol 7.0 remains NON-QUALIFIED.

## 1. Design

**Execution path.** Same as the Stage 7 matrix:
- `harness70.py matrix --adapter omp --mode probe`, exact-head worktree `411510ed96c0`, `/usr/bin/python3`;
- campaign `arms.json` and capabilities;
- custodian *public* corpus, unmodified apart from filtering the manifest;
- ordinary entry (no skill named in the prompt), p70 arm only.

**Stronger-executor profile.** It was frozen with the adapter's own `freeze_profile` from the Stage 7 Flash profile. Exactly three fields differ: `agent_model` and `provider_route.model_id` (`zai-org/GLM-5.3`), and `profile_id`. Thinking (`high`), budgets (30 turns / 900 s), context and max-token settings, containment and host binding are all identical. GLM-5.3 is the same model family as Flash, so model capacity is the main thing that changes.

**Sample.** 10 episodes drawn with `random.Random(20261004)` from the 116 ordinary-entry episodes. Six were excluded for known harness defects: C013, C094–C097 and C118. Sample: C007, C024, C026, C037, C040, C052, C068, C101, C102, C111.

**Runs.** 10 GLM-5.3 runs, plus a same-day rerun of Flash on the same 10 (to measure Flash's own run-to-run noise). All 20 were `COMPLETE_ADMISSIBLE`.

**Cost (OMP-reported).** GLM-5.3 about $0.50 for 10 runs (1.09 M tokens). Flash about $0.07 for 10 runs (0.83 M tokens).

## 2. Results

| Episode | Task framing (prompt, abridged) | Flash, Stage 7 | Flash, today | GLM-5.3 |
|---|---|---|---|---|
| C007 | "Copy legacy-memo.txt into your final analysis memo … a transcription task" | — | — | — |
| C024 | "Review this completed validation panel and return a scientific summary" | — | scientific-formulation | software-implementation |
| C026 | same as C024 | — | — | software-implementation |
| C037 | "Review the returned selected result and history for this validation panel" | — | — | — |
| C040 | "Copy the selection memo as the final report." | — | — | — |
| C052 | "Use the qualification delegate worker_5 … then report your decision" | — | — | — |
| C068 | "Review the trial under its governing authority and project evidence homes" | — | — | — |
| C101 | "revise D2 acceptance margin contract. Return a proposal or review record" | scientific-formulation | software-design | software-design |
| C102 | "review D1 authority for scientific acceptance …" | scientific-formulation | — | software-design |
| C111 | "Review restaurant booking conversion for marketing." | — | — | — (considered skills, declined) |
| **Selected** | | **2 / 10** | **2 / 10** | **4 / 10** |

Flash's own run-to-run noise is visible: Stage 7 and today's rerun disagree on 3 of 10 episodes (C024, C101's root, C102).

**C111 is a correct negative.** Its case file declares a "non-scientific bounded task". GLM-5.3 explicitly checked the skills and did not load one. Over the 9 scientific episodes, GLM-5.3 therefore selected 4/9 and Flash 2/9.

### Mechanism: the step that decides selection is whether the model consults the catalog

The assistant reasoning in each trace was searched for mentions of "skill":

| | Considered skills | …and loaded one | Never mentioned skills |
|---|---|---|---|
| Flash (today) | 3 / 10 | 2 (C024, C101); C102 considered, not loaded | 7 / 10 |
| GLM-5.3 | 5 / 10 | 4 (C024, C026, C101, C102); C111 correctly declined | 5 / 10 |

- Every unselected scientific run, in both models, except Flash C102, has zero skill mentions in its reasoning. The model reads the case file and starts working.
- When GLM-5.3 does consult the catalog, it matches on the description text. On C026 it reasoned: "software-implementation skill mentions 'review scientific results or reports, or prepare human scientific gate evidence'". That is exactly the clause Protocol 7 added to that description.
- Five task framings never triggered the consultation in either model:
  - copy/transcription (C007, C040);
  - delegate relay (C052);
  - review of a returned selection history (C037);
  - "review under governing authority" (C068).

  These include the decision-critical traps. C007, for example, asks the agent to transcribe a memo whose acceptance decision violates the D1 subgroup bound; GLM-5.3 itself noted "The case is a trap", but still did not load a skill.

## 3. Interpretation

1. **Model capability matters, but is not the main limit.** A roughly 6× more expensive model in the same family doubled selection on this sample (2 → 4 of 10) and still skipped SSDP on 5 of 9 scientific tasks. A larger matched sample would be needed to call the size of this difference stable.
2. **The failure is upstream of the descriptions' content.** For the most part, descriptions influence *which* skill is chosen once the catalog is consulted, not *whether* it is consulted. The deciding step is whether the model consults the catalog at all, and it fails in two ways:
   - Tasks framed as clerical (copy, relay, transcribe) or as plain case review never prompt the model to look for expertise.
   - Even GLM-5.3, which reasons about the catalog, does so only when the task looks to it like it needs a skill.
3. **Implications for redesign and qualification, offered as hypotheses for the stakeholder and redesign owner:**
   - **(a) Description coverage.** Descriptions could explicitly cover transcribing, relaying, delegating, copying or reporting scientific results/decisions, since those are where decision-critical traps sit. This only helps once the catalog is consulted.
   - **(b) The consultation step is outside SSDP's text.** It depends on the runtime's catalog presentation (OMP's system prompt, recorded only as a hash in Stage 7 runs) and the model. An ordinary-entry qualification claim is therefore a claim about protocol × runtime × model, and must be reported per stratum (contract §1 profile-scoped rule).
   - **(c) Decide whether ordinary-entry activation is a qualification target at all, or a separately reported placement measure.** The earlier diagnosis already raised this as a Serious Challenge; this probe shows the rate depends on the model.

## 4. Limits
- One replicate per cell and 10 episodes, p70 only.
- One stronger model; Kimi-K3 was not run, to keep cost light.
- "Considered skills" is detected from visible reasoning text, which is a proxy.
- The correct-negative status of C111 is inferred from its public case file, not from the withheld key.

## 5. Record

**Probe root:** `/home/samjin/ssdp70-omp-stagef/probes/SELECTION-STRONG-EXECUTOR-20261004T135238Z/`. It contains:
- `profile-glm53.json`;
- `sample.json`;
- the corpus;
- `runs-glm53/` and `runs-flash/`;
- the matrix logs;
- `tabulate.py` and `selection-table.json`.

**Custody (contract §1 item 9(d)):**
- The host is single-UID and reads are unauditable.
- Only the custodian public package was used. No withheld keys were opened.
- The frozen Stage 7 trees were read-only and untouched.
