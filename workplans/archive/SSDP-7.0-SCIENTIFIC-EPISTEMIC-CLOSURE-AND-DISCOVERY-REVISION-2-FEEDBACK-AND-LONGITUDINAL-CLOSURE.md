---
kind: protocol-major-revision-workplan-revision
workplan_id: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-2
protocol_version: 6.6.0
target_protocol_version: 7.0.0
status: superseded
superseded_by: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED
created_date: 2026-09-27
parent_workplan: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY
depends_on_revision: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-1
review_round: 2
active_serious_challenge: none
---

# Protocol 7.0 Revision 2 — Feedback Persistence and Longitudinal Discovery Closure

This revision supplements the parent and Revision 1. All earlier requirements remain binding unless explicitly strengthened here.

## 1. Second-review findings

Fresh out-of-matrix review of the composed workplan found two remaining blocking gaps and three material gaps:

1. **BLOCKING — discovery evaporation:** the plan required agents/programs to surface new questions but did not require material discoveries or human decisions that change scientific direction to survive the transient conversation/run.
2. **BLOCKING — single-run tunnel:** the plan made individual runs legible but did not adequately require semantic comparability across iterations/campaigns, even though scientific learning often arises from change between runs.
3. **MATERIAL — AI-narrative monoculture:** an AI-generated summary could become the only practical human interface even when underlying structured observations exist.
4. **MATERIAL — destructive retention boundary:** the plan did not state strongly enough that scientifically valuable information can be lost before reporting if a pipeline performs irreversible aggregation/deletion.
5. **MATERIAL — observation/report schema evolution:** changing metric definitions, populations, or report schemas can create false longitudinal comparisons unless semantic changes remain explicit.

The clauses below close these gaps.

## 2. Discovery-to-next-question persistence

A material discovery that changes the next scientific action must not depend on transient chat memory.

When an observation leads to a consequential new question, hypothesis, Challenge, requested experiment/analysis, or human decision, preserve the **minimum decision-sufficient scientific feedback state** in the appropriate existing artifact:

- D1/D2 proposal or Challenge when authority is implicated;
- workplan/working state when it changes the active investigation;
- evidence record when it defines a new evidence question;
- issue/task/native project state when it is an implementation or analysis follow-up;
- PEM only when existing PEM admission criteria are independently satisfied.

Do not create a universal "discovery database."

The persisted feedback should distinguish:

```text
observation
 -> interpretation/hypothesis
 -> why it matters
 -> next discriminating question/action
 -> authority/scope status
```

A material human rejection, reinterpretation, or redirection based on scientific evidence must likewise be recoverable when losing it would cause a later agent to repeat the obsolete path.

## 3. Longitudinal scientific comparability

Scientific transparency must span not only one execution but, where the science is iterative, the relation among materially comparable executions.

For run/campaign/generation/model comparisons, preserve enough semantic identity to determine whether quantities are actually comparable:

- observable/metric definition and units;
- population/split/selection regime;
- normalization/aggregation;
- model/method/configuration identity;
- uncertainty/error semantics;
- relevant D1/D2 revision;
- analysis transformation/version when material.

A report should support comparison across runs when such comparison is central to scientific interpretation, but must not place values side by side as if comparable when their semantics changed materially.

When semantics changed, show the change explicitly and either:

- provide a valid mapping/recalculation;
- narrow the comparison;
- or mark the quantities non-comparable.

Protocol 7 qualification shall include a counterexample where the same metric label changes population/definition between runs and verify that the system does not present a misleading trend.

## 4. Human-accessible non-narrative evidence

AI-generated prose is an analysis/presentation layer, not the sole scientific interface.

For material scientific judgments, the human must have a direct route from any AI summary to non-narrative evidence appropriate to the claim, such as:

- tables;
- plots;
- structured observations;
- individual cases;
- documented query/export views;
- canonical evidence records.

This does not prohibit AI explanation. It prevents human agency from depending entirely on one model's framing, compression, or omission choices.

Where AI selects which findings are prominent, the coverage and drill-down rules from Revision 1 still apply.

## 5. Information-preserving destructive boundaries

Before scientifically material raw/intermediate state is irreversibly discarded, aggregated, overwritten, compressed, or transformed beyond faithful recovery, the owning design must consider whether later scientific judgment reasonably needs information that would be lost.

If full retention is unjustified, preserve the minimum sufficient alternative, such as:

- scientifically meaningful aggregate/statistic;
- histogram/distribution;
- sampled/representative cases under an explicit sampling rule;
- extrema/outliers;
- decision inputs and margins;
- checkpointed trajectory;
- reproducible transformation inputs/parameters.

The retained substitute must be sufficient for the intended scientific judgment and must disclose the loss relative to raw state.

Resource economy can justify bounded loss. It cannot silently erase information whose absence can materially alter interpretation.

## 6. Observation/report semantic evolution

Scientific observation and report schemas are derived interfaces and may evolve, but their meaning must remain version/revision coherent.

A stable field/plot/metric label must not silently change:

- definition;
- population;
- units;
- normalization;
- aggregation;
- uncertainty semantics;
- selection rule.

When meaning changes materially, either version the semantic identity or provide an explicit compatibility mapping.

Historical run reports remain historically truthful. Current tooling may render old data through a new presentation layer only if it preserves the original scientific meaning or visibly declares the transformation.

## 7. Agent initiative across the technical chain

The epistemic-initiative contract applies when an agent performs substantial scientific **or engineering work that can affect scientific interpretation**, including:

- data-pipeline design;
- model-training orchestration;
- evaluation/reporting code;
- numerical backend changes;
- persistence/retention changes;
- publication tooling.

An engineer-agent noticing that a design would make scientifically important state unobservable must surface that as a design concern even if the immediate coding task would otherwise pass.

This does not broaden the agent's mutation authority.

## 8. Qualification additions

Add behavioral cases for:

1. **Feedback persistence:** a material anomaly produces a follow-up scientific question; a fresh context can recover why that question exists without replaying the original chat.
2. **Longitudinal semantic drift:** two runs use the same metric name with different populations; the comparison is blocked/narrowed rather than plotted as one trend.
3. **AI summary drill-down:** an AI narrative claims an anomaly; the user can reach the underlying plot/table/observations directly.
4. **Lossy boundary:** a pipeline cannot retain all raw intermediates; it retains a scientifically sufficient bounded projection and discloses what is lost.
5. **Historical report semantics:** a later report renderer does not silently reinterpret an older run under changed metric semantics.

## 9. Second-review disposition

With Revision 2 applied:

```text
SERIOUS CHALLENGE: NONE
ROUND-2 BLOCKERS: 2 FOUND / 2 CLOSED BY REVISION 2
ROUND-2 MATERIAL GAPS: 3 FOUND / 3 CLOSED BY REVISION 2
COMPOSED WORKPLAN: READY FOR FINAL FRESH WORKPLAN-LEVEL REVIEW
D4 IMPLEMENTATION: NOT YET STARTED
```
