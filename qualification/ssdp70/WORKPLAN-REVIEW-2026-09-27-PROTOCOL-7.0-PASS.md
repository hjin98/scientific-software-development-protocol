---
kind: protocol-workplan-review
protocol_version: 6.6.0
target_protocol_version: 7.0.0
review_date: 2026-09-27
branch: ssdp-7.0-scientific-epistemic-closure
review_scope: composed Protocol 7.0 workplan + revisions + Protocol 8.0 version rebind + active authority-index reconciliation
disposition: PASS
active_serious_challenge: none
---

# Protocol 7.0 Scientific Epistemic Closure — Final Workplan-Level Review

## 1. Review basis and independence boundary

This review evaluates the assembled planning state on branch `ssdp-7.0-scientific-epistemic-closure` against accepted Protocol 6.6.0.

Reviewed composition:

1. `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY.md`
2. `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-1-FIRST-REVIEW-CLOSURE.md`
3. `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-2-FEEDBACK-AND-LONGITUDINAL-CLOSURE.md`
4. `workplans/active/SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND.md`
5. `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` as current routing/lifecycle projection.

The review reconstructs the required scientific loop from Protocol 6.6 authority rather than treating the workplan's own section/acceptance matrix as proof.

This pass is intentionally separated from the authoring passes and uses out-of-matrix falsification, but it is **not represented as the later required fresh independent assembled-candidate Review**: the actual Protocol 7 semantic candidate, once implemented, must still be reviewed from a context that did not author that candidate under the normal SSDP acceptance process.

## 2. Reconstructed protected outcome

The proposed major revision is adequate only if it closes this loop without weakening existing authority discipline:

```text
question / hypothesis
 -> D1 scientific meaning
 -> D2 numerical method
 -> D3 architecture
 -> D4 implementation / execution
 -> realized scientific observations and data
 -> faithful analysis / human-legible presentation
 -> bounded active discovery
 -> human scientific judgment
 -> Challenge / new question / revised hypothesis
 -> owning authority acceptance process
```

The key protected properties are:

- task fidelity remains mandatory;
- evidence remains evidence rather than self-promoting into authority;
- materially meaningful execution becomes scientifically observable and legible;
- data can challenge methods through the existing authority/Challenge machinery;
- human scientific gates receive evidence adequate for actual judgment;
- agent delegation preserves discovery opportunities rather than suppressing them;
- discovery pressure does not incentivize hallucinated novelty or uncontrolled mutation;
- transparency remains proportionate rather than becoming a universal telemetry/reporting bureaucracy.

## 3. Out-of-matrix falsification

### 3.1 Fully reproducible but scientifically opaque execution

**Counterexample:** every input, seed, checkpoint, hash, and database row is retained, but a scientist must inspect source code and private schemas to learn which epoch was selected, what errors occurred, or why a model was published.

**Disposition:** CLOSED.

The composed plan explicitly distinguishes provenance/recoverability from scientific accessibility, requires authority-to-observation closure, a human-facing scientific front door, and a discoverable inspection surface for reasonable unanticipated questions.

### 3.2 Polished canned report hides retained scientific information

**Counterexample:** the default report is attractive and accurate but exposes only preselected metrics, while scientifically meaningful retained state is undiscoverable without internal-schema knowledge.

**Disposition:** CLOSED by Revision 1.

The scientific inspection surface must expose what observations/analyses exist, their coverage/meaning, supported inspection/export routes, and missing retained information.

### 3.3 Favorable aggregate hides adverse subgroup or tail

**Counterexample:** global error passes while a scientifically meaningful subgroup fails badly; the report shows only the aggregate.

**Disposition:** CLOSED by Revision 1.

Coverage envelope, denominators, filters, exclusions, failed/missing cases, sampled/top-k state, and material subgroup/tail behavior are explicitly governed. Qualification must include this counterexample.

### 3.4 Scientifically decisive state was never retained

**Counterexample:** a run passes, but a trajectory needed to assess a later scientific concern was overwritten and cannot be reconstructed.

**Disposition:** CLOSED by Revision 1 and Revision 2.

Missing observability must be classified as limitation/uncertainty/blocker/provisional state as appropriate; historical observations may not be fabricated. Destructive retention boundaries must preserve the minimum sufficient scientific substitute when justified.

### 3.5 Agent discovers pattern and treats the same search as confirmation

**Counterexample:** an AI searches many views, finds one striking correlation, and immediately presents it as strong confirmation of a newly generated hypothesis.

**Disposition:** CLOSED by Revision 1.

Exploratory discovery is separated from confirmatory evidence. Data-dependent selection, search breadth, leakage, population reuse and common-mode dependence are accounted for proportionately to claim strength.

### 3.6 Agent manufactures discoveries because the protocol asks for initiative

**Counterexample:** no material anomaly exists, but the agent invents "interesting" findings to satisfy a required discovery section.

**Disposition:** CLOSED.

The obligation is to search, not to manufacture novelty. "No material unexpected finding in the bounded search" is an accepted outcome, and observation/inference/hypothesis are explicitly separated.

### 3.7 Material observation lies outside task mutation scope

**Counterexample:** an implementation agent notices scientifically suspicious behavior in an adjacent surface and either suppresses it as out of scope or silently edits unrelated science.

**Disposition:** CLOSED.

The workplan establishes that task scope constrains mutation, not observation. Material observations are surfaced and routed; they do not grant mutation authority.

### 3.8 AI narrative becomes the only practical lens on evidence

**Counterexample:** the AI supplies a persuasive summary, but the human cannot directly inspect the underlying structured evidence.

**Disposition:** CLOSED by Revision 2.

Material AI summaries must drill to non-narrative evidence such as plots, tables, structured observations, cases, supported queries/exports, or canonical evidence records.

### 3.9 Long-running process reveals anomaly too late

**Counterexample:** a training/simulation campaign becomes scientifically suspect early, but the anomaly is presented only after an expensive irreversible final stage.

**Disposition:** CLOSED by Revision 1.

Scientifically meaningful intermediate observability is required where delayed feedback materially destroys decision value, without granting observers unauthorized control.

### 3.10 Discovery disappears with chat/session state

**Counterexample:** an important new scientific question is found, discussed, then lost when the session ends, causing a later agent to repeat the obsolete path.

**Disposition:** CLOSED by Revision 2.

Material feedback that changes the next scientific action must persist in the appropriate existing authority/workplan/evidence/task surface; no universal discovery database is required.

### 3.11 Longitudinal comparison silently changes meaning

**Counterexample:** two campaigns both report "force RMSE", but one uses a different population/normalization; a trend plot treats them as directly comparable.

**Disposition:** CLOSED by Revision 2.

Longitudinal comparison binds metric meaning, population, normalization, method/configuration, uncertainty semantics, D1/D2 revision, and analysis identity; incompatible semantics must be mapped, narrowed, or marked non-comparable.

### 3.12 Report creates a parallel scientific truth system

**Counterexample:** rendered reports/cache summaries can diverge from authoritative run state and become the de facto source of truth.

**Disposition:** CLOSED.

Reports and derived analyses are projections of canonical observations, with transformation lineage and no independent editing authority.

### 3.13 Transparency becomes maximal data dumping

**Counterexample:** the system satisfies "transparency" by exposing millions of raw records without salience, discoverability, or interpretive structure.

**Disposition:** CLOSED by Revision 1.

Scientific legibility optimizes inferential cost through progressive disclosure and salience. Undifferentiated dumps can explicitly fail the legibility requirement.

### 3.14 Protocol creates universal reporting bureaucracy

**Counterexample:** every scientific utility must adopt a dashboard, event bus, metric registry, observation database, and fixed plot suite.

**Disposition:** CLOSED.

The workplan repeatedly binds observability/reporting depth to materiality, consequence, path dependence, uncertainty, human-gate significance, cost of information loss, and privacy/resource burden. Universal machinery is explicitly non-goal.

### 3.15 Privacy/resource constraint conflicts with transparency

**Counterexample:** raw data cannot be retained/exposed safely or economically.

**Disposition:** CLOSED.

The plan permits the strongest safe bounded aggregate/derived projection and requires the information loss/limitation to remain visible. Transparency does not override legitimate privacy/security constraints.

### 3.16 Discovery directly rewrites D1/D2

**Counterexample:** a surprising plot or AI interpretation automatically changes accepted scientific authority.

**Disposition:** CLOSED.

Data remain evidence. Material findings can generate a hypothesis or Serious Challenge, but authority changes still use the owning D1/D2 acceptance process and human gates where required.

### 3.17 Protocol 7 quietly absorbs deterministic-orchestrator machinery

**Counterexample:** epistemic-closure implementation opportunistically imports the proposed deterministic control plane to manage observations/discoveries.

**Disposition:** CLOSED.

The deterministic-orchestrator proposal is explicitly rebound to Protocol 8.0 and remains D4-unauthorized. Protocol 7 may not implement it. Any future incompatibility is routed to Protocol 8 D3 reassessment.

## 4. Cross-domain adequacy

### D1

The workplan gives realized evidence a proper feedback role without making observations authoritative. D1 remains owner of scientific meaning, interpretation, uncertainty, validity, and external adequacy. The new doctrine strengthens the route by which observations can generate a scientifically grounded Challenge or new question.

**Disposition: ADEQUATE.**

### D2

The plan requires meaningful numerical trajectories, intermediate states, decision quantities, failure/fallback visibility, and semantic comparability while explicitly avoiding a mandate to expose every loop variable.

**Disposition: ADEQUATE.**

### D3

D3 receives a coherent architectural obligation: preserve/own enough scientific observation state, retention boundaries, canonical-vs-derived separation, identity linkage and drill-down to support the scientific contract. It is not forced into a universal observability subsystem.

**Disposition: ADEQUATE.**

### D4

The workplan leaves implementation mechanisms delegated while providing real acceptance boundaries for reporting, inspection, lineage, human gating and discovery behavior.

**Disposition: ADEQUATE FOR HANDOFF.**

## 5. Version and lifecycle review

- Protocol 6.6.0 remains accepted-current.
- `source/PROTOCOL_VERSION` remains 6.6.0 at this planning stage.
- `PROTOCOL-RELEASE-STATE.yaml` is intentionally unchanged.
- Protocol 7.0 is proposed, not accepted-current.
- Protocol 8.0 deterministic-orchestrator work remains proposed and D4-unauthorized.
- The current authority index explicitly routes Protocol 7 to epistemic closure and Protocol 8 to the preserved deterministic-orchestrator design family.
- Older deterministic workplan filenames retain `SSDP-7.0-...` as historical identities; the Protocol 8 rebind explicitly supersedes their old target-version designation.
- The authority-index filename `SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` is intentionally retained as a stable locator because existing historical qualification/test artifacts reference that exact path. Its current title/content identify the expanded 7.0/8.0 scope.

**Disposition: COHERENT.**

## 6. Complexity and scope review

The composed plan adds one preferred cohesive cross-cutting doctrine owner and local consequences in existing D1-D4/workflow/writing/testing surfaces. It explicitly rejects:

- D5;
- universal report/database/dashboard machinery;
- exhaustive anomaly search;
- mandatory plot catalogs;
- discovery quotas;
- out-of-scope mutation;
- deterministic-control machinery in Protocol 7.

This is commensurate with the identified major scientific-software gap and is materially simpler than introducing a parallel authority/control plane.

**Disposition: PROPORTIONATE.**

## 7. Remaining implementation risks to falsify later

These are not workplan blockers; they are implementation/review targets:

1. root-router compression could make the new doctrine hard to activate;
2. implementers may duplicate the new doctrine across many references instead of keeping one owner;
3. qualification may degenerate into phrase/schema pins rather than behavioral discrimination;
4. scientific-report examples may accidentally become universal mandatory field lists;
5. implementations may over-retain raw state rather than designing scientifically sufficient projections;
6. agent discovery behavior may become noisy unless stopping/salience rules are concretized carefully;
7. future Protocol 8 D3 may need to reconcile deterministic workflow state with Protocol 7 observation/discovery state without conflating semantic evidence and control state.

These are explicitly covered by the handoff's acceptance/review/reopen rules.

## 8. Final disposition

```text
SERIOUS CHALLENGE: NONE

ROUND 1:
  BLOCKERS: 4 FOUND / 4 CLOSED
  MATERIAL GAPS: 4 FOUND / 4 CLOSED

ROUND 2:
  BLOCKERS: 2 FOUND / 2 CLOSED
  MATERIAL GAPS: 3 FOUND / 3 CLOSED

FINAL OUT-OF-MATRIX REVIEW:
  NEW BLOCKERS: 0
  NEW MATERIAL WORKPLAN GAPS: 0
  VERSION/LIFECYCLE AMBIGUITY: CLOSED
  MINIMUM-JUSTIFIED-COMPLEXITY CHECK: PASS
  GLOBAL SCIENTIFIC-LOOP ADEQUACY: PASS

WORKPLAN-LEVEL DISPOSITION: PASS
IMPLEMENTATION HANDOFF READINESS: READY
PROTOCOL 7 ACCEPTANCE/RELEASE: NOT YET — IMPLEMENTATION, QUALIFICATION,
FRESH INDEPENDENT ASSEMBLED-CANDIDATE REVIEW, AND HUMAN RATIFICATION REMAIN REQUIRED.
```

The composed Protocol 7 planning state is mature enough to hand to implementation.
