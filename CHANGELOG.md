# Changelog

This is the **user-facing capability history** of the Scientific Software Development Protocol (SSDP). It explains what each version added or clarified without turning historical chronology into current authority.

- Current mutable acceptance/publication/recovery state: [`PROTOCOL-RELEASE-STATE.yaml`](PROTOCOL-RELEASE-STATE.yaml)
- Detailed semantic rationale, superseded candidates, and historical release events: [`history/SEMANTIC_EVOLUTION.md`](history/SEMANTIC_EVOLUTION.md)
- Current normative protocol semantics: `source/`

Older README files accumulated release mappings, bootstrap attempts, and version-specific narrative because the README was doing too many jobs. That material is now intentionally separated: this changelog keeps the **capability story**, semantic history keeps the **why**, and release state keeps the **current exact identities**.

## Protocol 7.x

### 7.2.0 — reliable consumed surface and calibrated qualification

Protocol 7.2 carries forward every Protocol 7.0 and 7.1 duty, drops only the requirement to load the owner, and changes how reliably an agent meets the duties. Development probing of 7.1 showed that agents obeyed text on the surface they read but did not reliably follow "read the owner when ..." instructions, and that the absolute qualification floors measured the model rather than the protocol. 7.2 removes the dependency on loading and recalibrates the measurement.

Main improvements:

- **One generated *Scientific checks* section per entrypoint.**
  - It replaces the 7.1 owner routing bullet and the completion clause. It states when the duties apply, the delegate questions (each with its launched-work qualifier), the gap rule and the numbered duties, so an agent that reads only the entrypoint holds the whole obligation.
  - It is built from one shared fragment, so the six entrypoints cannot drift, and every other 6.6 line is byte-identical apart from the generated governing-version line and the implementation skill's description (unchanged from 7.1).
  - Element 3 now also carries the owner's inaccessible-home rule: a named coverage limit is enough by default, it qualifies the judgment when the project designates or evidently uses the home, and it blocks only on the three stated conditions.
- **Owner reads are optional depth.** The scientific-inspectability owner remains the place for definitions and examples, most useful before consequential judgments over realized results, D1-D3 authority work or gate evidence. No duty depends on reading it.
- **Calibrated qualification (contract v2).** Gates compare the candidate with accepted 6.6 on the same executor and fixtures, with margins derived from a cluster-aware model; Precondition C checks the instrument before any candidate result counts. Stated operating characteristics replace absolute floors.
- **A consolidated qualification harness.** One scorer, the provider relay and containment kept, and the package-access ledger replaced by a conservative consumed-bytes count.

Stated limits:

- No qualification campaign has been run for 7.2. A PASS would claim only improvement over 6.6 on the gating executor and corpus, at the stated operating characteristics.
- The consumed surface is longer than 6.6's, so the fixed-cost backstop (2.0× the accepted 6.5 median) leaves little headroom, and a run that also reads the owner would breach it.
- Mandatory activation, typed delegation schemas and mechanical write enforcement need a deterministic control plane and stay with Protocol 8.
- 7.1.0 is superseded and was not qualified.

The Orchestrator gains a 7.2 profile with unchanged lifecycle, transition graph and profile schema; the 7.1 profile is frozen. Release status is deliberately not stated here; resolve it from `PROTOCOL-RELEASE-STATE.yaml`.

### 7.1.0 — obligation salience, structured delegation requests, and stratified qualification

Protocol 7.1 is a capability and presentation refinement to Protocol 7.0 following empirical evaluation under Stage 7. It preserves all Protocol 7.0 doctrine, owners, predicates, and thresholds while restructuring delegate requests for execution reliability and refining qualification precision.

Main improvements:

- **Structured delegate-request blocks:**
  - Relocates delegate questions from scattered element prose to a dedicated, prominent block at the head of the Scientific completion clause on all four role entrypoints and two specialists (`software-documentation`, `software-maintenance-audit`).
  - Formulates each owed question as an explicit, answerable-either-way prompt containing the launched-work qualifier inside the question itself: Findings (findings or none), Realized results (null envelope of examined and unexamined areas), Variants (variant-search disclosure including changes after seeing results, held-out reuse, lineage, and lower-bound/unknown-interval/claim-limit for unavailable history), and Tensions (gated to consequential judgments, asking for search scope, unreachable places, and found records with bindings and asserters).
  - Establishes explicit gap rules without an artificial return condition: an unanswered question (including when a delegate returns nothing) or partial coverage is reported as a gap, never as none, a null, or no selection.
- **Specialist entrypoint adaptation:**
  - `software-documentation` and `software-maintenance-audit` carry only Findings and Realized results questions, matching their historical scope and omitting variant and tension duties. `repository-hygiene` remains unburdened.
- **Timing and follow-up semantics:**
  - Separates launch-time requests from post-return follow-ups. A follow-up re-invocation does not satisfy an initial request part, but answers supplied in frozen returns can remove owed gaps to the extent already addressed.
- **Execution-surface realism:**
  - Model-visible surfaces are neutralized of stand-in and qualification cues, ensuring delegator agents interact with tools without artificial status indicators, while adapter-pinned server and store identities are tracked as disclosed residuals.
- **Undelivered-treatment stratification:**
  - Ordinary-run episodes where no SSDP skill was selected are classified as undelivered-treatment outcomes rather than candidate doctrine failures, preventing unselected runs from masking the performance of delivered doctrine.

### 7.0.0 — scientific inspectability, epistemic initiative, and the scientific feedback loop

Protocol 7 is a major revision. It changes what counts as an adequately inspectable scientific computation, what agents must notice and report, and what human gates must receive. It keeps every accepted 6.6 capability unless a stakeholder decision explicitly superseded it. It adds no D5 layer and changes neither the pre-routing kernel nor the Orchestrator control semantics.

Main improvements:

- **One conditional owner** (`scientific-inspectability-and-initiative.md`) defines the realized scientific record, scientific inspectability, epistemic initiative, the three channels (task report, product inspection surface, governance gate), feedback persistence and the claim-integrity floor.
- **An obligation-binding rule.**
  - D1–D3 authors state the inspectability need and visibly mark product inspectability surfaces (O1).
  - Agents perform a bounded inquiry and report findings and gaps (O2).
  - Product retention, projection and exposure bind only through accepted authority, an explicit instruction or an existing contract (O3), never through the protocol alone. A marked surface beyond the requested deliverable binds only after stakeholder/task-authority acceptance.
  - Without O1 content, an agent records its retention/projection choices as a visible proposed default.
- **A claim-integrity floor** on every agent-authored assertion, including product content an agent writes. It covers selected or post hoc results, unqualified conclusions past known material limits, and interpretation laundered into fact. It never adds product capability.
- **Inspectability doctrine.**
  - Recoverability is not accessibility.
  - Progressive disclosure, meaning preservation and a coverage envelope that includes the stratification axes examined.
  - Faithful deterministic projection with lineage and source-to-rendered verification.
  - Non-narrative and tool-independent routes.
  - Retention and destructive boundaries with per-unit keys, and semantic stability across runs.
  - Decision/trajectory/negative-result visibility, explicit insufficiency, interim visibility and privacy limits.
- **Decision provenance and variant-search disclosure.** Effective choice, origin, actor and exact binding are separate facts. An instruction is not ratification. Disclosure covers result-contingent iteration, tool-launched searches, and delegated/resumed selection lineage with explicit unknown history.
- **Bounded epistemic initiative.**
  - An expectation record, and a too-good-to-be-true finding class.
  - A fixed finding shape, and a null only with its search envelope.
  - No manufactured novelty, and exploratory kept apart from confirmatory.
  - Engineering-task and AI-consumer rules.
  - An answerable-either-way delegate request, with unanswered parts reported as gaps.
- **Data → authority feedback.**
  - Tensions are recorded outside authority text and bound to every plausibly implicated authority and its subject.
  - They are searched across revisions, former names and recorded predecessors before authority is relied on or revised, and reported with native asserters and per-binding status.
  - D1/D2 revisions make revision-scoped applicability assessments that reach the revision gate.
  - Inaccessible homes qualify or block only under stated conditions.
- **Feedback persistence** goes to one existing authorized home when writable. Otherwise the report carries a non-writing fallback, and no universal discovery database exists.
- **Consumed-surface placement.** Every D1–D4 entrypoint, plus the documentation and maintenance-audit specialists, carries the obligation predicate, the owner-load trigger and a completion clause with the minimum duties and their label meanings. The implementation skill's description now also selects scientific run/analysis, results-review, gate-evidence, copying/transcribing/relaying of scientific results or decisions, and delegated scientific work. The user guide now directs users to activate skills with deterministic runtime commands (`/skill`, `$skill`, `/skill:name`) rather than wording, after Stage 7 showed that ordinary-entry selection is unreliable.
- **Local deltas.**
  - D1/D2/D3 O1 content.
  - Evidence: the realized-record/observation overlap, and exploratory/confirmatory inquiry status on `CHALLENGES`.
  - Writing: recommendation/next-probe and authority-Challenge reporting roles.
  - Workflow: bidirectional scientific Review, the Channel C gate-evidence contract and product-scope acceptance.
  - Templates: O1, revision-record and variant-disclosure fields.
  - Workflow prompts.
  - A versioning note that the ratification package is decision-sufficient gate evidence.

Stated limits:

- The tension claim is a bounded disclosed search, not exhaustive retrieval.
- Documentation and audit routes do not perform tension searches or ask delegates for variant/tension returns.
- Delegate answers are reported as given.
- Adoption is prospective, and version-bound 6.x work stays 6.x.

The stakeholder superseded 6.6's per-route 1.10 burden cap with a 1,000 B-per-entrypoint compression target that is subordinate to lossless required elements. The retained fixed-cost backstop is 2.0 × the fresh paired accepted-6.5 median on the T1/T7/T8 reference routes.

The Orchestrator gains a 7.0 profile with unchanged lifecycle, transition graph and profile schema. The 6.6 profile is frozen. The deterministic control plane remains Protocol 8. Release status is deliberately not stated here; resolve it from `PROTOCOL-RELEASE-STATE.yaml`.

## Protocol 6.x

### 6.6.0 — cognitive and operational optimization

Protocol 6.6 preserves every accepted 6.5 engineering capability while reducing how much protocol machinery an agent must keep active, reconstruct, or replay during ordinary work.

Main improvements:

- a smaller universal kernel that keeps only cross-domain semantics (D1-D4 ownership, abstraction/concretization, authority vs evidence, materiality, feasibility before simplicity, Challenge, proportional rigor, Lossless Representation, and the hard specialized-semantics availability invariant);
- specialized semantic-definition/traceability detail moved to its own risk-triggered owner: ordinary engineering meaning stays lightweight, while specialized objects, parameter/default bindings, imports and formal claims still require the exact owner meaning before inference;
- authority lifecycle states and the mutation/acceptance sequence moved to the workflow owner, loaded when authority actually changes;
- Project Engineering Memory split into a compact agent-facing contract (when memory activates, retrieval, Historical Applicability Set, authority binding, counterevidence, when to update) and a cold schema/governance owner; duplicated retrieval procedures now route to the one owner;
- decision-sufficient handoffs and an operational, explicitly non-authoritative Working State for long or interruption-prone work, plus a clear rule that transient progress does not mutate workplans;
- vendor-neutral cognitive-resource escalation (model, reasoning, context, tool breadth, independent trajectories, subagents) under the existing proportional-rigor rule, without duplicating host routing;
- optional independent review trajectories with explicit common-mode limits, and a Review strategy switch after related repeated findings;
- strict version binding: a task or workplan that declares `protocol_version` stays governed by it until the authority over that work rebinds it. Compatibility makes a newer protocol eligible for adoption but never adopts it; an agent may recommend a successor and must never self-adopt one. A mismatch resolves a source of the declared version or its exact immutable mapped source, else reports non-closure;
- a generated entry contract inlined into every skill entrypoint that carries only a one-line governing-version declaration and a four-line pre-routing safety kernel (earliest-owner routing, material semantic routing, closure integrity, instruction boundary). The rest of the universal doctrine stays in its conditional owner, reached by one generated kernel route rather than a per-skill copy. The contract reuses `PROTOCOL_VERSION`, manifests and release state (with an offline repository helper) and is re-derived from its owners during package validation;
- smaller consumed entrypoints: every direct route, predicate, exclusion and role-local authority boundary is kept, while generic method detail lives with its routed owner (the implementation entrypoint is about 16% smaller than in 6.5);
- thinner skill descriptions written as selection interfaces (task class plus exclusions) rather than compressed doctrine, with generic package validity kept independent of vendor adapters;
- a small, removable empirical evaluation harness comparing 6.5 and 6.6 on selection, declared and observed protocol context, and trajectory outcomes under a named reference harness.

The Orchestrator gains a 6.6 profile that rebinds version-bound prompts only; the machine lifecycle, transition graph and profile schema are unchanged. Release status is deliberately not stated here; resolve it from `PROTOCOL-RELEASE-STATE.yaml`.

### 6.5.0 — self-governance, proportional rigor, and release-state strengthening

Protocol 6.5 preserves the accepted D1-D4 model while tightening how the protocol governs its own development and release lifecycle.

Main improvements:

- applies SSDP ownership/evidence/representation/convergence rules to SSDP's own release engineering;
- separates immutable version semantics from mutable repository release state;
- establishes one mutable release-state owner instead of copying current lifecycle facts through versioned source/docs;
- makes independent Review PASS only technical eligibility, distinct from explicit stakeholder ratification;
- strengthens evidence-claim congruence: mechanical, structural, semantic, and outcome evidence may claim only what their oracles actually discriminate;
- makes out-of-matrix abstraction-adequacy falsification a first-class independent-Review obligation for substantial protocol work;
- integrates current doctrine instead of replaying predecessor-numbered amendment sections;
- hardens self-hosted Project Engineering Memory evidence realization around canonical Git ancestry/content, immutable durable identities, exact file/blob artifacts, parser strictness, and fail-closed missing evidence;
- preserves frozen historical profiles/resources rather than rewriting them under new terminology;
- operationalizes **importance-weighted attention**: mandatory obligations remain mandatory while analysis/evidence depth follows consequence, decision-sensitive uncertainty, irreversibility, and opportunity cost;
- separates problem importance from next-action priority, prevents automatic parent-to-child priority inheritance, and adds escalation/de-escalation/stop and sunk-cost/rediscovery safeguards;
- makes scientific/numerical rigor decision-sensitive so trivial in-envelope numerical details do not automatically trigger research-grade qualification while boundary-sensitive uncertainty still escalates;
- treats fixtures/tests as evidence instruments rather than product authority and allows corrected evidence instruments to requalify the same immutable semantic candidate when the intervening change is demonstrably non-semantic;
- adds protocol-release documentation closeout: the root README is recompiled as a current user guide, CHANGELOG records capability evolution, and a small objective repository check preserves version/changelog and README routing without attempting to score prose quality.

Release status is deliberately not stated here; resolve it from `PROTOCOL-RELEASE-STATE.yaml`.

### 6.4.0 — semantic definition and traceability

Protocol 6.4 made hidden semantic ambiguity harder to smuggle through apparently precise documents or code.

Added/strengthened:

- source availability before substantive semantic use;
- one coherent canonical meaning for materially governed semantic objects;
- proportional formal-first definitions: equations where useful, structured contracts where better, no decorative formalism;
- well-defined domains/types/shapes/units/scope/quantifier/order/failure semantics where material;
- parameterized family vs concrete instance vs governed default;
- exact specialized external imports with variant/locator/assumption mapping;
- separation of definition from existence/truth/convergence/adequacy/authority warrant;
- bounded typed `USES_DEFINITION` dependency traces for impact/review;
- external content treated as evidence/data rather than instruction authority;
- preservation of all accepted 6.3 Project Engineering Memory and routing semantics.

### 6.3.0 — Project Engineering Memory

Protocol 6.3 added evidence-backed project-local learning without creating a fifth authority domain.

Added:

- Project Engineering Memory (PEM) as non-authoritative reusable project learning;
- conditional activation only when project history can materially change the decision;
- Historical Applicability Sets (HAS) for task-local disposition of relevant project learning;
- stable memory identities, maturity, temperature/salience, binding health, counterevidence, and assessment lineage;
- accepted-base plus candidate-overlay memory semantics;
- capability-transfer checks when replacing mature machinery;
- explicit guardrails preventing frequency/history/documentation from becoming authority.

### 6.2.0 — Lossless Representation and progressive disclosure

Protocol 6.2 focused on communicating the same accepted semantics with lower cognitive and routing cost.

Added/strengthened:

- universal Lossless Representation Rule;
- progressive disclosure through explicit skill/concern routing;
- package membership and hyperlinks distinguished from activation;
- current semantics kept hot while specialized/history detail remains cold but discoverable;
- canonical-owner-first documentation instead of amendment accumulation;
- source/package/profile closure and exact immutable fallback discipline.

### 6.1.0 — evidence lifecycle, terminology, and human-facing rigor

Protocol 6.1 separated two ideas that had previously shared the word 'realization':

```text
abstraction -> concretization       # D1-D4 semantic descent
evidence specification -> realization -> observation -> assessment
```

It also strengthened:

- evidence applicability and stale-evidence semantics;
- target-vs-execution dependency separation;
- typed dependency/evolution records and bounded impact closure;
- common-mode risk and evidence durability;
- Challenge/Review handoffs;
- human-facing background/terminology and first-use abbreviation discipline;
- frozen/current profile separation and version-bound interpretation.

### 6.0.0 — scientific software becomes first-class

Protocol 6.0 generalized the former software-local protocol into four semantic domains:

```text
D1 scientific/mathematical formulation
 -> D2 algorithm/numerical method
 -> D3 software architecture
 -> D4 specification/implementation
```

The key change was not more process; it was making scientific and numerical meaning explicit authority rather than implicit context around software engineering. Protocol 6 retained the strongest Protocol 5 engineering safeguards inside this broader abstraction/concretization hierarchy.

## Protocol 5.x capability lineage

Protocol 5 was the software-engineering foundation later generalized by Protocol 6. Its capabilities remain historically important even though current Protocol 6 vocabulary is different.

| Version | Capability introduced or strengthened |
| --- | --- |
| **5.1** | documentation specialist and documentation lifecycle discipline |
| **5.2** | conservative repository hygiene |
| **5.3** | stage/final acceptance separation and production qualification |
| **5.4** | development economy, version-bound plans, and evidence-context reuse |
| **5.5** | implementation fidelity to design authority |
| **5.6** | proxy-proof acceptance and real-owner testing |
| **5.7** | stewardship of durable stakeholder outcomes over process artifacts |
| **5.8** | effective compression and canonical ownership |
| **5.9** | portable deterministic routing |
| **5.10** | snapshot-complete handoffs |
| **5.11** | tool-assisted engineering |
| **5.12** | convergence and development-cycle economy |
| **5.13** | deterministic tool entry, CodeQL/tool routing, progressive disclosure |
| **5.14** | solution-boundary discipline and active simplicity |
| **5.15** | language profiles and cross-language performance engineering |
| **5.16** | long-horizon health, Verification, Stabilization, maintenance audit, workflow prompts, public fallback |

### 5.16 — long-horizon engineering quality

Late Protocol 5 explicitly treated complexity/churn/coverage/dependency structure/mutation survival and related measurements as **sensors, not verdicts**. It added:

- a semantic quality ratchet for touched code;
- Verification as deeper risk-triggered design falsification;
- Stabilization as non-mutating architecture GC;
- periodic software-maintenance audit;
- fault-injection, differential/metamorphic, and architecture-fitness evidence where appropriate;
- public fallback and portable skill-routing discipline.

### 5.15 — language-native engineering

Protocol 5.15 introduced thin differential language profiles so the shared engineering rule remained canonical while Python/C++ and mixed-language work could load only the runtime/tooling details that materially applied.

### 5.14 — active simplicity

Protocol 5.14 made the solution boundary explicit: a clean bug gets a clean owning-layer fix, while repeated wrappers, fallback paths, duplicated state/authority, repeated reconciliation, or a materially simpler equivalent design are signals to simplify/re-derive instead of adding another patch.

### 5.13 — deterministic tools and progressive disclosure

Protocol 5.13 strengthened deterministic tool entry, static-analysis routing such as CodeQL where applicable, and progressive disclosure so optional tools and specialized guidance did not become a mandatory global pipeline.

## Historical release identities and invalidated attempts

Old README versions contained exact recovery/public-bootstrap SHAs and several invalidated bootstrap attempts. Those records are intentionally **not duplicated here**.

- Use `PROTOCOL-RELEASE-STATE.yaml` for the repository's current exact accepted/public/recovery mappings.
- Use `history/SEMANTIC_EVOLUTION.md` for historical identities, invalidated attempts, reopen/repair chronology, and the semantic reason a transition occurred.
- Use the version-bound source/profile itself when reconstructing historical work.

This separation keeps the README and changelog useful to humans without creating competing release-state or semantic authority.
