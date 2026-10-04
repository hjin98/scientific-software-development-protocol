---
kind: qualification-diagnosis
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date_utc: 2026-10-04
status: diagnostic-evidence-not-authority
---

# Stage 7 diagnosis: M07 delegate-request conformity and treatment delivery

**Question.** Delegate-request conformity (M07) was 1/25 for Protocol 7 (p70) and 0/25 for 6.6 (p66). Is Protocol 7's delegate-request duty inadequate, unfollowable or mis-scored?

**Answer.** None of these can be decided from this campaign: **in all 50 M07 opportunities the executor never loaded any SSDP skill.**
- The Protocol 7 duty was never in the agent's context, so the campaign gives no evidence about it, for or against.
- Under the workplan's own §11.3 Route rule, these opportunities are placement misses for non-selection, but they were scored as request-content failures.
- The same non-delivery covers 42 of p70's 43 critical failures. Stage 7 therefore measured mostly whether this executor activates SSDP at all, not how Protocol 7's doctrine performs once loaded.

This document is diagnostic evidence for the stakeholder and the redesign owner. It changes no determination: Protocol 7.0 remains NON-QUALIFIED (see the corrigendum, §6). Figures are reproduced by `diagnose_stage7_treatment_delivery.py` over the frozen campaign. Both `FREEZE.sha256` trees were verified intact.

## 1. Treatment delivery

Executor: `deepinfra/zai-org/GLM-5.3-Flash`, reasoning effort high, 30 turns, 900 s. The task prompts do not name a skill; entry is ordinary catalog selection.

| | p66 | p70 |
|---|---|---|
| Runs with a `root_selection` (any SSDP skill loaded) | 20 / 122 | **13 / 122** |
| Outcomes, root selected | 16 PASS, 1 UNRESOLVED, 3 NOT_EVALUATED | 10 PASS, **1 FAIL (C069)**, 2 NOT_EVALUATED |
| Outcomes, no root | 62 PASS, 31 FAIL, 3 UNRESOLVED, 6 NOT_EVALUATED | 63 PASS, 36 FAIL, 3 UNRESOLVED, 7 NOT_EVALUATED |
| Critical failures in no-root runs | **31 / 31** | **42 / 43** |
| M07 opportunities in no-root runs | **25 / 25** | **25 / 25** |

**What actually differed between arms in no-root runs (211 of 244 runs, 86%):**
- The arms differ only in the catalog descriptions shown in the system prompt.
- Six of the seven role/specialist descriptions are byte-identical across arms.
- Only `software-implementation`'s description changed. p70 adds "run or analyze … pipelines; review scientific results or reports, or prepare human scientific gate evidence".
- The p70 skill bodies (role entrypoints 2.0–2.4× larger, e.g. scientific-formulation 6,317 → 15,131 B; specialists 1.6–1.8×; repository-hygiene unchanged) were never read in those runs.

**Limit on any p66-vs-p70 conclusion.** The p66/p70 differences in these runs come from one changed sentence plus stochastic variation, with a non-blind evaluator (corrigendum §3.2). They are not effects of Protocol 7 doctrine.

## 2. M07 in detail

There are seven delegate-case episodes, all §11.3 delegate cases with scripted stand-in delegates:
- C042 silent
- C044 repair
- C046 (no case kind stated)
- C048 rename
- C050 compaction
- C052 review
- C055 chained

These kinds are as stated in the case's own delegation text.

In both arms, every run made exactly one delegate call without any root selected.

The p70 requests are task relays, for example:
- C044: "Read the case file cases/C044.json and perform the assigned case task as instructed therein, then report the decision."
- C048: "… No execution, results review or gate preparation; no variant selection. Do not launch work."

This pre-empts the variant question instead of asking it. None asks for findings-or-none, realized-results/null or variant history in answerable-either-way form. The single M07 pass (C046-p70 findings part) came from an instruction ending "report findings and the returned envelope", produced without the doctrine loaded.

**The rubric matches the spec on content.** The evaluator scored the rename and compaction parts as owed, which agrees with workplan §11.3 ("the predicate does not evidently exclude it"). No rubric-versus-doctrine contradiction was found on the parts scored.

**Mis-scoring on route (scoring defect).** Workplan §11.3, *Route*: "A case is scored against the elements carried on the route its delegator runs on (§8.3), as the ordinary-entry cases are, including their placement-miss rule for non-selection."
- With no SSDP route selected, no Protocol 7 element was carried.
- The correct disposition is therefore a placement miss for non-selection, not 24 request-content failures.
- The evaluator bundle carries the selection evidence (`events.normalized.jsonl`), but neither the rubric nor the expected-scoring manifest conditions M07 on route.
- Either way it is a qualification failure, so the determination is unaffected. The attribution is wrong, and attribution is what a redesign would act on.

## 3. What this does and does not establish

**Established:**
- (a) Under ordinary entry with this executor, SSDP is rarely activated for these tasks: 11% of p70 runs, 16% of p66 runs.
- (b) The Protocol 7 delegate-request duty had **zero** effective exposure.
- (c) When a root was loaded, critical failures were rare in both arms (p66 0, p70 1), on small and non-matched samples.

**Not established:**
- Whether the duty is adequate or followable once loaded.
- Whether Protocol 7 is better or worse than 6.6 on any doctrine measure.
- Whether p70's lower selection count (13 vs 20) is a real effect of the changed description. This is untested: one replicate, and selection episodes are not matched.

**Withdrawn as redesign guidance.** The original report's causal "insights" (M02 probing, M06 disclosure, M15 provenance) had already been withdrawn on labelling grounds in the corrigendum. They also lack treatment exposure, since 42 of the 43 p70 critical failures came from runs where Protocol 7 was not loaded.

## 4. Hypotheses about the doctrine (untested here; for a doctrine-loaded probe)

1. **Salience.** The duty is one clause inside a single dense ~2 KB obligation paragraph in each role entrypoint ("Unless the predicate evidently excludes a delegate's work, ask for findings or none …"). A model that loads the entrypoint may still not act on it at the delegation step.
2. **Fixture cue.** Every case file states "delegate is scripted, not SSDP governed" and pre-states the returned envelope. Both signal that the request wording is immaterial and invite relaying. §11.3 makes delegates scripted by design, but exposing that fact to the delegator is a fixture-realism choice that may depress conformity regardless of doctrine.

## 5. SERIOUS CHALLENGE (qualification design; route to the stakeholder and the qualification-contract owner)

**Two claims are conflated.** Under ordinary entry with an executor that activates SSDP in roughly 1 run in 8, the Stage 7 design cannot tell apart:
- "Protocol 7 is activated when it should be" (a placement/selection claim); and
- "Protocol 7's doctrine produces correct behaviour once active" (the semantic claims of §§11.4–11.6).

The contract treats non-selection as a placement miss (workplan §11.3 *Route*; contract §4). However, the frozen scoring manifest and evaluator score doctrine measures on non-selected runs as if the doctrine were in play.

**Two defects.**
- Any future campaign must report these as **separate strata**: selection/placement, and doctrine conformity given activation.
- It must also meet minimum doctrine-loaded exposure per measure. Otherwise the contract §2 exposure minimums are met only nominally.

This is a defect in the qualification design and its scoring realization. It is not a reason to change Protocol 7 doctrine.

## 6. Recommended next actions (cheapest discriminating first)

1. **Doctrine-loaded M07 probe.**
   - Re-run the seven M07 episodes per arm with explicit root activation (route chosen per case).
   - Do it twice: as-is, and with the "scripted, not SSDP governed" cue removed.
   - This separates "the doctrine is not followed" from "the doctrine was never delivered" and tests hypothesis 2.
   - It is development data, not qualification. These fixtures are no longer blind: their content is disclosed in the assessment evidence and in this document.
2. **Selection diagnosis.**
   - Find out why the executor rarely selects SSDP: OMP catalog presentation, prompts that do not cue a skill, or model behaviour. Compare against a stronger executor on a small sample.
   - Run this before any redesign of doctrine content.
3. **Scoring repair.** Condition doctrine measures on the route actually carried (§11.3 *Route*), and add selection/placement as its own reported measure.
4. **Fresh fixtures** for any future qualification, since the current set is now development data.

## Custody disclosure (contract §1 item 9(d))

- The host is single-UID and reads are unauditable.
- This diagnosis read the frozen runs, the frozen assessments, the per-arm installed skills and the repository workplan/contract. It did not read withheld custody keys or rubrics.
- Fixture content quoted above was already disclosed in the frozen assessment evidence.
