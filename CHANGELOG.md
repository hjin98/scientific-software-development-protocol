# Changelog

This is the **user-facing capability history** of the Scientific Software Development Protocol (SSDP). It explains what each version added or clarified without turning historical chronology into current authority.

- Current mutable acceptance/publication/recovery state: [`PROTOCOL-RELEASE-STATE.yaml`](PROTOCOL-RELEASE-STATE.yaml)
- Detailed semantic rationale, superseded candidates, and historical release events: [`history/SEMANTIC_EVOLUTION.md`](history/SEMANTIC_EVOLUTION.md)
- Current normative protocol semantics: `source/`

Older README files accumulated release mappings, bootstrap attempts, and version-specific narrative because the README was doing too many jobs. That material is now intentionally separated: this changelog keeps the **capability story**, semantic history keeps the **why**, and release state keeps the **current exact identities**.

## Protocol 6.x

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
