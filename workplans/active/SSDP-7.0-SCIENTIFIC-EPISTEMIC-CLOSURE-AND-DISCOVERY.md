---
kind: protocol-major-revision-workplan
workplan_id: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY
protocol_version: 6.6.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-27
base_protocol: Protocol 6.6
active_serious_challenge: none
requires_version_rebind: SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND
---

# SSDP 7.0 — Scientific Epistemic Closure, Transparency, and Discovery

## 1. Objective and major-version boundary

Protocol 7.0 SHALL make scientific epistemic closure a first-class SSDP objective alongside task fidelity, semantic authority, evidence integrity, and engineering robustness.

Protocol 6.x is mature at specifying what scientific/numerical methods mean, how downstream software must remain faithful to them, how evidence supports or challenges claims, and how work is reviewed. It is materially weaker at requiring a real scientific execution to expose what actually happened in a form that a competent human scientist can understand, critique, interrogate, and use to generate new questions. It is also under-specified about an agent's obligation to search realized evidence for material anomalies, contradictions, uncertainty, and discovery opportunities outside the narrow success criterion of the assigned task.

This omission leaves the scientific loop open:

```text
question / hypothesis
 -> D1 scientific formulation
 -> D2 numerical method
 -> D3 architecture
 -> D4 implementation / execution
 -> realized data, states, trajectories, decisions
 -> analysis and human-legible scientific presentation
 -> active search for anomaly / contradiction / opportunity
 -> human scientific judgment
 -> Challenge / new hypothesis / revised method
 -> ...
```

Protocol 7.0 SHALL close the right-hand side of that loop without creating a new D5 authority layer and without allowing observations, AI interpretation, or reports to self-promote into scientific authority.

This is a major revision because it changes the governing doctrine for what counts as an adequately transparent scientific computation, what agents are expected to notice and report, what human gates must be given, and what scientific-software architecture must preserve for inspection and discovery.

## 2. Motivating defect

The triggering failure class is broader than missing metrics or poor user interfaces.

A scientific program may currently:

- implement a well-specified D1/D2 method faithfully;
- retain enough hashes, internal state, databases, logs, checkpoints, and provenance to reconstruct what happened;
- pass qualification and produce a reproducible final artifact;

while still forcing a scientist to reverse-engineer source code, traverse opaque identifiers, inspect internal schemas, write bespoke extraction scripts, or hand the entire state directory to an AI before learning basic scientifically material facts about the run.

Examples include selected epoch/checkpoint, error-versus-epoch behavior, data preparation outcomes, exclusions, per-population error structure, automated-decision margins, outliers, trajectories, internal scientific states, candidate comparisons, and the evidence by which a final model/result was selected.

This is not adequate scientific transparency. Recoverability is not accessibility.

The deeper failure is epistemic: if scientific work is delegated to software or AI and only the requested terminal result returns to the human, discovery opportunities encountered inside that delegated work disappear from the human's perceptual field. The more work is automated, the more damaging this becomes unless transparency and epistemic initiative increase with delegation.

## 3. Core doctrinal additions

Protocol 7.0 SHALL introduce and integrate the following concepts.

### 3.1 Scientific observability

Scientifically material realized states, transformations, trajectories, decisions, observations, failures, exclusions, and results of an execution must be retainable and inspectable at a level sufficient for their scientific interpretation.

Observability is not identical to operational logging. Scheduler status, stack traces, runtime telemetry, and debug messages may be useful but do not satisfy scientific observability when the scientist needs quantities, populations, units, distributions, trajectories, comparison context, and decision semantics.

### 3.2 Scientific legibility

Scientifically material realized information must be consolidated and projected into forms an intended competent scientist can understand without source-code inspection, internal-database archaeology, hash traversal, or bespoke reconstruction machinery for routine scientific questions.

Legibility is audience-relative and uses progressive disclosure. It does not require flattening all detail into one report.

### 3.3 Scientific epistemic closure

Scientific epistemic closure is the property that a scientific computation produces sufficiently observable and human-legible evidence to support:

- verification of faithful execution;
- criticism and challenge;
- anomaly discovery;
- uncertainty and limitation recognition;
- hypothesis generation;
- meaningful human adjudication;
- justified feedback into D1/D2 where warranted.

### 3.4 Epistemic initiative

An agent performing substantial scientific or technical work must proportionately search realized evidence for material information beyond the literal completion criterion when that information could reasonably:

- challenge a governing assumption or accepted interpretation;
- expose an unexpected regime or consequential anomaly;
- reveal uncertainty or missing visibility;
- show materially structured residual/error behavior;
- identify sensitivity, instability, or near-boundary decisions;
- motivate a high-value new question or discriminating analysis.

The obligation is to look and surface supported findings, not to manufacture novelty.

### 3.5 Discovery pressure

Scientific workflows must contain a positive pressure toward discovering materially informative structure, not merely toward converging on the original request. Completion and discovery are separate objectives.

Discovery pressure SHALL remain proportionate. It must not become an obligation to produce a fixed number of "interesting insights," pursue arbitrary tangents, or convert weak correlations into scientific claims.

### 3.6 Transitive epistemic transparency

Delegation across AI, software, model, data-preparation, optimization, training, evaluation, and publication layers must not sever the route from human-facing scientific meaning to realized data and decisions.

The human need not inspect every layer routinely, but when a material question arises there must be a semantically coherent drill-down route from summary -> analysis -> individual observations/state -> exact provenance/raw evidence, subject to privacy/security/storage constraints.

### 3.7 Human scientific agency

A human approval step is not a meaningful human-in-the-loop design unless the human receives scientifically intelligible evidence adequate for the judgment assigned to them.

Protocol 7.0 SHALL therefore distinguish mere human presence from human scientific agency. Human gates involving scientific judgment must receive decision-sufficient evidence and, where discovery/criticism is material, enough contextual scientific visibility to generate and investigate new questions rather than only approve a predetermined conclusion.

## 4. Fundamental bidirectional doctrine: method <-> data

Protocol 7.0 SHALL explicitly recognize that scientific authority and realized data form a feedback system rather than a one-way hierarchy.

```text
D1 / D2 authority
    -> determines meaning, valid operations, observables, uncertainty and interpretation
execution / data
    -> provides observations that can support, falsify, qualify, challenge or motivate revision
```

Data are evidence, not authority. An observation, plot, anomaly, or AI interpretation does not self-amend D1/D2. But D1/D2 governance is incomplete if the software prevents realized evidence from becoming visible enough to challenge them.

The existing Serious Challenge mechanism SHALL remain the route for evidence that may invalidate or materially undermine accepted authority. Protocol 7.0 extends the system upstream of Challenge by requiring sufficient observation, presentation, and active discovery for such evidence to become noticeable.

## 5. Core invariants

The Protocol 7 implementation SHALL preserve these invariants.

### 5.1 Authority-to-observation closure

For every scientifically material D1/D2 object or process whose realized behavior can affect trust, interpretation, acceptance, uncertainty, or subsequent scientific reasoning, the implementation must establish a proportionate route:

```text
governing meaning
 -> executable realization
 -> persisted/available scientifically meaningful observation
 -> human-legible projection
 -> exact drill-down/provenance
```

Not every internal variable is scientifically material.

### 5.2 Observation scope may exceed mutation scope

Task scope constrains what an agent may mutate, not what it may notice.

A material out-of-scope observation SHALL be surfaced without silently expanding implementation authority. The agent may recommend a follow-up, Challenge, or separately scoped investigation.

### 5.3 Observation / interpretation / hypothesis separation

Human-facing and agent-generated scientific reporting SHALL distinguish, where material:

- direct observation;
- derived analysis;
- interpretation;
- hypothesis/conjecture;
- recommendation or next probe;
- authority Challenge.

No presentation layer may launder interpretation into measured fact.

### 5.4 No manufactured novelty

Agents SHALL NOT be required to produce novelty, anomalies, or new hypotheses when evidence does not support them. "No material unexpected finding observed in the bounded search" is a valid outcome.

### 5.5 Faithful projection, not parallel truth

Scientific reports, dashboards, plots, tables, summaries, and terminal views must be derived from authoritative realized state/evidence. They are projections, not independently edited scientific truth.

If a displayed value cannot be faithfully obtained from retained state, it must be marked unavailable rather than reconstructed by guess.

### 5.6 Recoverability is not accessibility

The existence of sufficient bytes somewhere in a database, log, hash chain, cache, checkpoint, or source tree does not satisfy the reporting obligation if a routine scientifically material question requires reverse engineering or bespoke extraction.

### 5.7 Progressive disclosure

The normal interface should lead with high-information scientific summaries, then permit drill-down to detailed analyses, individual observations, and raw/provenance state.

The protocol SHALL NOT require one giant report, universal dashboard, or full duplication of raw data.

### 5.8 Meaning-preserving reporting

Reported quantities must retain the semantic context needed for interpretation: definition, unit, sample/population, normalization, aggregation, uncertainty/error semantics, model/checkpoint/regime identity, and other D1/D2 conditions where material.

### 5.9 Decision transparency

A scientifically consequential automated decision must make recoverable and human-legible:

- what decision was made;
- what candidates/options were considered;
- the governing decision rule;
- the scientifically meaningful input quantities;
- their relevant observed values;
- exclusions/ties/tolerances/fallbacks where material;
- the selected outcome;
- the route to complete underlying evidence.

A decision digest alone is never a sufficient human-facing explanation.

### 5.10 Trajectory visibility

For iterative processes where the path materially affects scientific trust or interpretation, the relevant trajectory must be retained and exposable, not only the terminal state.

Examples include optimization convergence, training/error versus epoch, active-selection progression, sampling/equilibration histories, iterative solver residuals, or other method-specific trajectories.

### 5.11 Negative-result visibility

Scientifically meaningful exclusions, failures, missing values, fallbacks, rejected candidates, outliers, invalid regimes, and warnings must not disappear merely because an aggregate stage passes.

## 6. Scientific reporting as part of the scientific instrument

Scientific reporting SHALL be treated as part of the scientific software's functional scientific interface, not as optional documentation polish.

The protocol SHALL distinguish:

```text
machine provenance / internal state
    !=
operational diagnostics / logs
    !=
scientific observation record
    !=
human-facing scientific analysis and presentation
```

These surfaces may share data but serve different consumers and questions.

Scientific software should provide an obvious human-facing front door for a completed or ongoing scientific process. Exact UI/format remains delegated unless project/user contracts require it. Acceptable mechanisms may include generated reports, CLI inspection, notebooks generated from canonical state, web views, portable tables/plots, structured JSON plus rendered projections, or combinations thereof.

The architectural requirement is faithful, low-friction scientific access, not a specific rendering technology.

## 7. Data as a first-class scientific concern

Protocol 7.0 SHALL correct the current asymmetry between method authority and realized data.

Where scientifically material, scientific software must make intelligible the data lifecycle itself:

- source population and identity;
- preprocessing/transformation;
- filtering and exclusion;
- grouping/correlation structure;
- weighting;
- sampling/selection;
- splitting;
- derived quantities;
- missing/invalid values;
- coverage/population summaries;
- before/after distributions when transformations can change interpretation;
- lineage between source, transformed, selected, and evaluated populations.

D1/D2 remain semantic owners where those transformations alter scientific/numerical meaning. D3/D4 must preserve adequate state and interfaces for observation and reporting.

## 8. Agent discovery contract

For substantial scientific/technical tasks, agents SHALL perform a bounded epistemic-initiative pass proportionate to consequence, uncertainty, information value, and cost.

A useful conceptual output projection is:

```text
requested result
material observations
anomalies / tensions
uncertainty / missing visibility
discovery opportunities
possible authority Challenges
high-value next probes
```

These are semantic channels, not mandatory headings.

The agent must distinguish:

- required task blockers from optional discoveries;
- observations from interpretations;
- local implementation defects from D1/D2 Challenge;
- high-information follow-up from curiosity-driven scope expansion.

The agent may stop the discovery pass when additional search is unlikely to change scientific understanding, reveal a material anomaly, or justify a new question at proportionate cost.

## 9. Derived AI/software interaction doctrine

The transparency obligation applies not only to direct human <-> AI dialogue but transitively to derived work products.

If an AI writes a method, program, data pipeline, training campaign, evaluation system, or publication mechanism, that artifact must still satisfy the same scientific inspectability obligations when its outputs later mediate human scientific judgment.

AI authorship does not justify opaque machine-facing-only state.

Likewise, an AI consuming a scientific program should prefer existing supported scientific-report interfaces over reverse engineering internal storage. Repeated need for bespoke AI reconstruction is evidence of an observability/legibility defect and should be reported as such.

## 10. D1 / D2 integration

### 10.1 D1

Scientific formulation should identify, proportionately:

- observables and realized evidence that can materially support/challenge the scientific interpretation;
- scientifically meaningful populations/regimes;
- uncertainty/discrepancy views whose absence would impair judgment;
- what external or realized evidence could falsify or reopen the formulation;
- human judgments requiring scientific evidence.

D1 SHALL NOT prescribe plots or storage mechanisms unless scientifically necessary.

### 10.2 D2

Numerical/algorithmic authority should identify, proportionately:

- meaningful convergence/iteration/error trajectories;
- intermediate states needed to assess numerical faithfulness;
- sensitivity/conditioning/uncertainty information that can change interpretation;
- decision quantities used by numerical selection/optimization;
- failure/fallback regimes that must remain visible.

D2 SHALL NOT turn every loop variable into a reporting requirement.

## 11. D3 architecture integration

D3 must ensure that architecture does not discard, overwrite, or make unreasonably inaccessible scientifically material realized state before it can support required analysis and reporting.

Where material, D3 should define:

- ownership of scientific observation state;
- persistence/retention boundaries;
- canonical source vs derived projection;
- drill-down path and identity linkage;
- decision-observation linkage;
- streaming/incremental observation where long processes require mid-run inspection;
- recovery/restart semantics for observation continuity;
- privacy/security/resource boundaries;
- bounded retention or aggregation when full raw retention is unjustified.

Avoid a universal scientific-observability database or event bus unless actual project requirements justify one.

## 12. D4 implementation integration

D4 must concretize the reporting/inspection contract through the minimum coherent mechanism.

Where a program already retains sufficient authoritative state, prefer projection/adaptation over duplicating state.

Where state is insufficient, implementation may need to retain additional scientifically material observations prospectively. The work must explicitly distinguish:

- information already recorded but poorly presented;
- information reconstructible but at unreasonable friction;
- information never recorded and therefore irrecoverable;
- information intentionally omitted for privacy/resource/scientific reasons.

## 13. Human-facing presentation standard

Extend the Lossless Representation Rule for scientific execution outputs.

A substantial scientific report should lead with enough context to orient the intended competent reader, then expose:

- scientific identity of the run/result;
- material configuration/regime;
- key data/population summary;
- main trajectories and outcomes;
- consequential automated decisions and rationale;
- central error/uncertainty/validation results;
- anomalies, exclusions, failures, warnings, and missing visibility;
- notable discovery findings;
- route to detailed evidence and provenance.

Opaque identifiers/hashes remain available for exact identity but should be subordinate to human-readable semantic identity in normal presentation.

Visualizations should be selected for information value, not mandated decoratively. Plots must preserve definitions, units, populations, uncertainty, and selection markers where needed for interpretation.

## 14. Review becomes bidirectional

Protocol Review SHALL retain the existing authority -> candidate falsification direction and add a candidate/data -> authority discovery direction.

For substantial scientific work, Review asks both:

1. Is the implementation/execution faithful to accepted authority?
2. Did the realized behavior reveal evidence that should challenge, qualify, or motivate investigation of the authority or framing itself?

A Review need not invent a Challenge. It should report when no material reverse-direction finding survives bounded scrutiny.

Out-of-matrix abstraction-adequacy review should include the possibility that formally compliant execution exposes scientifically important behavior not represented in the original acceptance matrix.

## 15. Human-gate evidence contract

When SSDP requires human scientific adjudication, the handoff to the human must provide a scientifically intelligible evidence projection adequate to the decision.

The human should not be asked to ratify a scientific result based only on:

- PASS/FAIL labels;
- opaque digests;
- agent conclusions;
- database locations;
- raw logs;
- references whose meaning requires substantial reconstruction.

For consequential decisions, the human-facing projection should also make material anomalies, uncertainty, alternatives, and unresolved discovery findings visible so approval does not collapse into confirmation of the agent's original framing.

## 16. Evidence and qualification integration

Existing evidence/provenance doctrine remains valid but is not sufficient by itself.

Protocol 7.0 qualification SHALL test both semantic correctness and human-accessibility properties with behavioral scenarios such as:

- a domain scientist can identify what was run and on what data without code inspection;
- a consequential automated decision can be explained from persisted authoritative observations;
- a selected checkpoint/model/result exposes the metrics/trajectory that drove selection;
- an iterative process exposes scientifically material trajectory information;
- rejected/excluded/failed scientific cases remain visible;
- a report value traces to canonical state and exact provenance;
- observation/interpretation/hypothesis are not conflated;
- an agent surfaces a material out-of-scope anomaly without silently mutating scope;
- an agent does not manufacture novelty when no material anomaly is present;
- a human gate receives enough scientific evidence to adjudicate rather than merely trust an agent summary.

Synthetic proxy fixtures may test structural properties, but assembled semantic adequacy and human legibility require independent Review; green phrase/schema checks cannot prove them.

## 17. Proportionality and anti-bureaucracy constraints

This revision must not become "record and plot everything."

Use the existing importance/proportional-rigor doctrine. The obligation scales with:

- consequence of misinterpretation;
- scientific decision sensitivity;
- uncertainty;
- iterative/path dependence;
- irreversibility;
- anomaly potential;
- human-gate significance;
- cost of losing the observation;
- storage/compute/privacy burden.

A trivial deterministic utility does not need a scientific dashboard. A long-running model-training, simulation, optimization, or data-selection campaign may require substantial scientific reporting.

No universal metric registry, plot checklist, observation ontology, dashboard framework, or mandatory database is authorized merely by Protocol 7.0.

## 18. Privacy, security, proprietary data, and resource limits

Transparency does not override legitimate confidentiality, privacy, safety, or storage constraints.

Where raw scientific data cannot be exposed or retained, provide the strongest safe aggregate/derived view that preserves the intended scientific judgment, and make the limitation visible.

Do not silently downsample, aggregate, redact, or discard information whose loss can materially change interpretation. Such transformations need explicit semantics/provenance at their owning layer.

## 19. Project Engineering Memory and discovery

PEM remains non-authoritative.

A recurring scientific observability failure, repeated discovery pattern, or demonstrated preservation capability may enter PEM only under existing evidence-backed admission rules.

Ordinary interesting observations from one scientific run do not become PEM merely because they are surprising. They remain run evidence/hypotheses unless they constitute reusable project engineering learning.

## 20. Required source/protocol surfaces

Implementation is expected to inspect and reconcile at minimum:

- `source/shared/references/scientific-formulation.md`;
- `source/shared/references/numerical-algorithm-design.md`;
- `source/shared/references/scientific-software.md`;
- `source/shared/references/architecture-and-design.md`;
- `source/shared/references/specification-and-implementation.md`;
- `source/shared/references/evidence-evolution-and-dependencies.md`;
- `source/shared/references/testing-and-validation.md`;
- `source/shared/references/workflow-and-workplans.md`;
- `source/shared/references/scientific-technical-writing.md`;
- `source/shared/references/documentation-and-evidence.md`;
- `source/shared/references/convergence-and-cycle-economy.md`;
- `source/shared/references/abstraction-and-concretization.md`;
- relevant skill `SKILL.md` routers;
- implementation workplan templates;
- protocol versioning/compatibility;
- package/profile generation and qualification surfaces;
- README / CHANGELOG / semantic-evolution history at closeout.

A dedicated `scientific-epistemic-closure.md` owner is the preferred design starting point because the doctrine is cross-cutting and substantial. The implementation may choose a differently named cohesive owner if independent design review finds a clearer ownership structure.

Keep root routers compact: the new doctrine should add a high-reliability route, not duplicate its full semantics into every `SKILL.md`.

## 21. Versioning and Protocol 8 preservation

Protocol 7.0 inherits accepted Protocol 6.6 capabilities unless explicitly superseded through this work.

The previously proposed deterministic control-plane / mandatory-orchestrator work is reassigned to Protocol 8.0 by `SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md`.

Protocol 7.0 SHALL NOT opportunistically implement the deterministic orchestrator. However, Protocol 7 design must not create unnecessary constraints that make the future Protocol 8 architecture impossible. Any material conflict discovered between epistemic-closure requirements and the preserved deterministic-orchestrator proposal must be surfaced for later Protocol 8 D3 reassessment rather than silently solved by importing Protocol 8 machinery.

## 22. Implementation stages

### Stage A — version/lifecycle reconciliation

- establish Protocol 7.0 as the epistemic-closure major revision;
- rebind deterministic-orchestrator target to Protocol 8.0;
- reconcile active authority index/routing so no current artifact ambiguously assigns two meanings to Protocol 7;
- leave accepted Protocol 6.6 release state unchanged.

### Stage B — canonical doctrine

- create the canonical scientific-epistemic-closure owner;
- define observability, legibility, epistemic closure, initiative, discovery pressure, transitive transparency, human scientific agency, authority-to-observation closure, and proportionality;
- establish no-D5 / data-is-evidence-not-authority / no-manufactured-novelty boundaries.

### Stage C — D1/D2/D3/D4 integration

- add only the layer-local consequences needed for each domain;
- establish retention/reporting responsibilities without duplicating doctrine;
- preserve existing semantic ownership.

### Stage D — agent/workflow integration

- add bounded epistemic-initiative behavior to substantial scientific/technical work;
- update Review to bidirectional falsification/discovery;
- update human-gate and handoff requirements;
- preserve mutation-scope discipline while allowing observation beyond task scope.

### Stage E — human-facing scientific reporting

- integrate progressive scientific reporting/drill-down requirements;
- distinguish logs, provenance, observation records, derived analyses, and human-facing projections;
- strengthen opaque-identifier handling and human-readable semantic identity.

### Stage F — qualification

Construct behavioral qualification that discriminates the targeted doctrine rather than pinning wording. Include both positive and negative cases for:

- hidden-but-reconstructible state;
- faithfully projected state;
- meaningful iterative trajectory;
- consequential automated decision;
- anomaly discovery outside task mutation scope;
- no-anomaly case;
- data limitation/privacy case;
- human scientific gate;
- report/provenance consistency.

### Stage G — independent assembled-candidate Review

Review must reconstruct the global scientific loop independently of the workplan matrix and attempt at least these counterexamples:

- a fully reproducible but scientifically opaque run;
- a polished report backed by parallel/stale/non-authoritative values;
- an agent that completes the task but suppresses a material anomaly;
- an agent that hallucinates novelty to satisfy discovery pressure;
- a report that exposes aggregates while hiding scientifically decisive tails/exclusions;
- a human gate that technically receives evidence but cannot reasonably judge it;
- observability machinery whose complexity exceeds its scientific value;
- a new doctrine that accidentally promotes data/AI findings into authority;
- a root-router compression that makes the new owner unreliable to reach.

### Stage H — release closeout

After qualification, independent Review, required human ratification, and accepted candidate selection:

- update `source/PROTOCOL_VERSION` to 7.0.0 only at the correct semantic-candidate/release stage;
- create self-reference-safe public-source/recovery mappings under existing release discipline;
- update generated packages/profiles;
- update README and CHANGELOG;
- add concise semantic-evolution history;
- reconcile workplan authority index;
- perform closeout learning assessment;
- preserve Protocol 6.6 immutable recovery;
- keep Protocol 8 deterministic-orchestrator proposal explicitly future/proposed.

## 23. Acceptance criteria

Protocol 7.0 is not ready for implementation completion or release unless all of the following hold:

1. There is one clear canonical owner for scientific epistemic closure and no parallel shadow doctrine.
2. Methods and realized data are explicitly connected bidirectionally without allowing evidence to self-promote into authority.
3. Scientific observability and human legibility are obligations where material, not optional documentation polish.
4. Routine scientific interrogation does not depend on source-code archaeology when the program already possesses the relevant material information.
5. Consequential automated decisions have faithful human-readable decision evidence.
6. Material iterative/path-dependent scientific processes expose relevant trajectories.
7. Data preparation/transformation/exclusion/selection can be scientifically inspected where material.
8. Human scientific gates receive evidence adequate for actual judgment.
9. Agents have a bounded epistemic-initiative obligation that can surface material out-of-scope observations without expanding mutation authority.
10. The protocol explicitly prevents manufactured novelty and distinguishes observation, interpretation, hypothesis, recommendation, and Challenge.
11. Review includes a reverse data -> authority discovery/challenge direction.
12. Transparency survives derived AI/software workflows through semantically coherent drill-down.
13. Reporting is derived from canonical state and does not become a parallel truth system.
14. Proportionality prevents universal logging/plot/database bureaucracy.
15. Privacy/resource constraints have explicit safe handling without silent scientific information loss.
16. Root routing remains reliable and cognitively economical.
17. Behavioral qualification discriminates the new capabilities at real semantic boundaries.
18. Accepted Protocol 6.6 capabilities remain losslessly preserved unless explicitly superseded.
19. The deterministic-orchestrator major proposal is unambiguously Protocol 8.0 and remains unimplemented.
20. Independent assembled-candidate Review finds no unresolved Serious Challenge or blocking defect.

## 24. Non-goals

Protocol 7.0 does not:

- create D5;
- make AI a scientific authority;
- require autonomous hypothesis acceptance;
- require exhaustive anomaly mining;
- require a fixed number of discoveries;
- require every program to emit plots;
- require a universal dashboard or observation database;
- require retention of all raw intermediate state forever;
- replace provenance/reproducibility/evidence doctrine;
- weaken task fidelity;
- authorize out-of-scope mutation;
- implement the Protocol 8 deterministic orchestrator;
- prescribe mdstats-specific reports as universal SSDP doctrine.

## 25. Reopen / serious-challenge triggers

Reopen the design before D4 if implementation shows that:

- the proposed doctrine cannot be represented without a new authority plane;
- observability requirements materially conflict with D1/D2 ownership;
- faithful reporting requires an architecture substantially more complex than justified by the protected outcome;
- discovery pressure cannot be bounded without incentivizing hallucinated novelty or uncontrolled scope expansion;
- required data retention violates unavoidable privacy/security/resource constraints with no adequate safe projection;
- the doctrine conflicts materially with accepted Protocol 6.6 versioning/review/evidence semantics;
- the future Protocol 8 deterministic-control architecture becomes incompatible in a way that requires current Protocol 7 semantic compromise rather than later D3 reassessment.

## 26. Handoff state

```text
GOVERNING BASE: Protocol 6.6.0
TARGET: Protocol 7.0.0
OBJECTIVE: scientific epistemic closure + transparency + discovery
DETERMINISTIC ORCHESTRATOR: reassigned to Protocol 8.0
D4 IMPLEMENTATION: NOT YET AUTHORIZED BY THIS WORKPLAN ALONE
REQUIRED NEXT ACTION: independent workplan-level falsification / gap closure
ACTIVE SERIOUS CHALLENGE: NONE KNOWN AT AUTHORING
```
