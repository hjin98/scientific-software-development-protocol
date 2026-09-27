---
kind: protocol-major-revision-workplan-revision
workplan_id: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-1
protocol_version: 6.6.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-27
parent_workplan: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY
review_round: 1
active_serious_challenge: none
---

# Protocol 7.0 Revision 1 — First Independent Falsification Closure

This revision supplements the parent workplan. Every parent requirement remains binding unless explicitly strengthened here.

## 1. Review disposition before repair

The first workplan-level falsification did **not** pass the parent unchanged. It found four blocking and four material gaps:

1. **BLOCKING — canned-report loophole:** progressive reports could satisfy the written contract while still preventing a scientist from discovering what other scientifically meaningful data exist or asking unanticipated questions without internal-schema knowledge.
2. **BLOCKING — selective-presentation loophole:** a faithful report could still be materially misleading through favorable population/metric/view selection, hidden denominators, omitted failures, or aggregate-only presentation.
3. **BLOCKING — missing-observation closure ambiguity:** the parent required unavailable quantities to be marked unavailable but did not define when missing scientific visibility blocks acceptance or human adjudication.
4. **BLOCKING — exploratory/confirmatory conflation:** active anomaly/discovery search creates data-dependent hypotheses; the parent did not explicitly prevent the same exploratory observation from being laundered into confirmatory evidence without accounting for selection and common-mode dependence.
5. **MATERIAL — derived-analysis provenance:** plots/tables/aggregates need their own reproducible transformation semantics back to canonical observations.
6. **MATERIAL — comparison context:** isolated values can be legible yet scientifically uninterpretable without relevant baseline/reference/previous-regime context.
7. **MATERIAL — transparency overload:** maximal exposure can bury the human in data and defeat agency just as effectively as opacity.
8. **MATERIAL — delayed discovery:** for long/expensive/irreversible processes, waiting until final closeout can destroy the value of timely scientific feedback.

The following clauses close these gaps.

## 2. Scientific inspection surface and discoverability

Scientific legibility requires not only a preselected report but a supported **scientific inspection surface** proportionate to the system.

For substantial scientific processes, the human-facing front door must make discoverable:

- what scientifically meaningful observations/analyses are available;
- their semantic identity, units/populations/regimes, and coverage;
- how to inspect or export them through supported interfaces;
- which potentially material observations were not retained or are unavailable.

A supported inspection surface may be a CLI, report index, query/export API, interactive report, structured dataset with documented semantic schema, or another low-friction interface. No specific technology is mandatory.

A scientist should be able to formulate an unanticipated but reasonable question over retained scientific observations without first reverse-engineering private storage layout or source code.

This is **bounded open interrogation**, not a requirement to support arbitrary computation through the production application.

## 3. Coverage, denominators, and anti-selection-bias presentation

Human-facing scientific summaries must make their **coverage envelope** recoverable when selection could change interpretation.

Where material, report:

- population/denominator represented;
- included/excluded/missing/failed counts;
- selection/filtering rule;
- aggregation definition;
- whether a view is complete, sampled, stratified, top-k, thresholded, or otherwise selected;
- material subgroup/tail behavior hidden by the aggregate;
- relevant competing candidates or alternatives when a decision comparison is being explained.

The report must not imply global adequacy from a favorable subset.

A visualization or summary is scientifically defective if a reasonable competent reader would draw a materially different conclusion after learning a hidden selection/denominator fact that the system possessed and should have exposed.

Protocol 7 qualification shall include a counterexample where an aggregate metric passes while a scientifically meaningful subgroup/tail fails, and verify that the human-facing projection does not hide it.

## 4. Observability insufficiency is explicit scientific state

When scientifically material information was never recorded, was discarded, or cannot be safely exposed, the system must classify the consequence rather than merely print "unavailable."

Use the existing authority/evidence workflow to determine whether the missing visibility is:

- non-material limitation;
- material uncertainty requiring explicit qualification;
- blocker for the current scientific judgment/acceptance;
- reason for provisional/risk-accepted continuation where independently allowed;
- trigger for prospective instrumentation/retention in a future run.

A human scientific gate may not close unqualified when missing observation could plausibly change the judgment assigned to that gate.

No implementation may manufacture historical observations that were not retained.

## 5. Exploratory discovery versus confirmatory evidence

Protocol 7 SHALL distinguish **discovery observations** from evidence used to confirm a claim.

A pattern found because an agent or human searched the realized data is valid as an observation and may motivate a hypothesis, Challenge, or follow-up. It does not automatically become independent confirmatory evidence for the hypothesis generated from that same search.

Where claim strength makes the distinction material:

```text
exploratory observation
 -> hypothesis / candidate explanation
 -> explicit evidence question
 -> appropriately independent or selection-aware follow-up
 -> assessment
 -> possible authority Challenge / revision
```

D1/D2 must account proportionately for data-dependent selection, reuse of the same population, multiple comparisons/search breadth, leakage, and shared-oracle/common-mode dependence when these can inflate apparent support.

The protocol SHALL NOT require formal multiple-testing machinery for every exploratory plot. The rule is claim-strength alignment: exploratory findings remain labeled exploratory until an evidence route adequate for the resulting claim is established.

This preserves discovery pressure without institutionalizing p-hacking or AI-generated narrative overfitting.

## 6. Derived-analysis lineage

A human-facing plot/table/summary that materially affects scientific interpretation is a derived scientific analysis and must retain enough lineage to reconstruct:

- source observation set;
- filtering/selection;
- transformation/normalization;
- aggregation/statistic;
- uncertainty/error computation where applicable;
- relevant parameter/regime;
- software/version identity when the analysis itself is nontrivial.

The rendered artifact is a projection; its derived values must not become independently edited truth.

Where feasible, generate machine-readable and rendered views from the same analysis specification/state.

## 7. Interpretive comparison context

When an absolute value is not scientifically meaningful enough by itself, the report must include or directly route to the relevant comparator, such as:

- accepted/reference theory or oracle;
- baseline method/model;
- previous iteration/generation;
- training versus validation/test population;
- competing candidate;
- tolerance/acceptance boundary;
- expected limiting behavior.

Do not require comparisons that have no justified scientific meaning.

## 8. Cognitive accessibility and salience

Transparency is not achieved by dumping all retained state on the human.

Human-facing scientific projections must optimize **scientific inferential cost**:

```text
orientation / identity
 -> high-information summary
 -> material anomalies, uncertainty, decisions
 -> key trajectories/distributions/comparisons
 -> drill-down detail
 -> raw/provenance state
```

The system must preserve lower-salience adverse facts while giving them proportionate prominence. A thousand-page undifferentiated dump that technically contains the answer but makes it practically undiscoverable remains a legibility failure.

Agents producing summaries should explicitly surface the small number of findings most likely to change interpretation or next action, while keeping routes to the full evidence.

## 9. Timely feedback for long-running processes

For long-running, expensive, irreversible, or adaptively controlled scientific processes, observability requirements apply at scientifically meaningful intermediate boundaries when waiting until completion would materially reduce the value of human/agent judgment.

Where justified, expose interim trajectories, anomaly summaries, and decision state at checkpoints that permit:

- safe continuation;
- pause/abort/reconfiguration through separately authorized mechanisms;
- early investigation of a potentially invalid regime;
- preservation of evidence before it is overwritten or discarded.

This does not authorize an observer to mutate a run outside existing control authority.

## 10. Discovery sufficiency versus exhaustive search

Epistemic initiative must use a bounded search envelope.

For substantial work, the agent should inspect the most information-rich and decision-sensitive views first, including obvious residual/distribution/trajectory/subgroup/decision-margin surfaces when applicable.

The agent is not required to exhaust every variable pairing, clustering, hypothesis, or visualization.

The stopping condition is reached when additional search has low plausible information value relative to cost or when further investigation would become a new research task requiring explicit scope.

The agent should state material areas it could not inspect when those omissions limit the discovery assessment.

## 11. Qualification additions

Add behavioral cases that discriminate the Revision-1 closures:

1. **Discoverability:** a scientifically meaningful retained quantity exists but is absent from the default report; a competent user can discover and inspect it through the supported inspection surface without internal-schema knowledge.
2. **Selective aggregate:** global error is acceptable but one material subgroup is poor; the report exposes the subgroup/coverage rather than presenting only the favorable aggregate.
3. **Missing state:** a scientifically decisive trajectory was not retained; the system reports non-closure/limitation rather than reconstructing or claiming full transparency.
4. **Exploratory reuse:** an agent discovers a correlation in a searched dataset and labels it hypothesis-generating rather than confirmatory.
5. **Derived plot lineage:** plotted values trace reproducibly to canonical observations and transformation semantics.
6. **Overload:** the system preserves full drill-down but leads with a compact scientifically salient view.
7. **Timely anomaly:** a long-running process develops a material anomaly before completion and exposes it at an appropriate intermediate boundary without granting unauthorized mutation.

## 12. Version/lifecycle closure added to the planning cycle

The Protocol 8 version-rebind record is immediately authoritative for target-version identity within this branch.

Before Protocol 7 implementation handoff, reconcile the active workplan authority index so it has:

- Protocol 7.0 -> scientific epistemic closure / transparency / discovery;
- Protocol 8.0 -> deterministic control plane / mandatory orchestrator, still proposed and D4-unauthorized.

The eight older deterministic design artifacts retain their historical filenames and wording, but current routing must never require a reader to infer whether their embedded "Protocol 7" target is still live; the Protocol 8 rebind must be named explicitly wherever they are routed as current future-design inputs.

## 13. Revised workplan-review disposition

With these clauses applied, the first-review blockers are closed at the planning level.

```text
SERIOUS CHALLENGE: NONE
ROUND-1 BLOCKERS: 4 FOUND / 4 CLOSED BY REVISION 1
ROUND-1 MATERIAL GAPS: 4 FOUND / 4 CLOSED BY REVISION 1
IMPLEMENTATION AUTHORIZATION: STILL PENDING FINAL WORKPLAN-LEVEL RE-REVIEW
NEXT ACTION: fresh out-of-matrix second review
```
