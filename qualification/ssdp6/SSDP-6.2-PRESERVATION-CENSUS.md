---
kind: protocol-implementation-preservation-evidence
protocol_version: 6.1.0
target_protocol_version: 6.2.0
authority: non-normative-evidence
baseline_commit: cec29671b9db59d20124a6e2ce99725ed60b8f0a
workplan: workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md
status: implementation-baseline
---

# Protocol 6.2 Representation Preservation Census

This is implementation/review evidence, not protocol authority. Current owners govern semantics. It records the finite Protocol 6.1 representation surface and the lossless mapping obligations for the Protocol 6.2 representation refactor.

## Preservation invariant

Protocol 6.2 may compact, generalize, relocate, reroute, or make information cold only when every accepted Protocol 6.1 doctrine and still-valid historical capability remains recoverable with equal-or-stronger semantics. Task-local non-materiality changes activation, not global preservation. A genuine semantic conflict is blocking and must be resolved by the owning authority outside this representation-only cycle.

## Current representation census

| Family | 6.2 disposition |
| --- | --- |
| `source/roles/*/SKILL.md` (4) | refactor to compact root routers + role method/completion delta |
| `source/specialists/*/SKILL.md` (3) | refactor to compact specialist routers + specialist method/output delta |
| universal kernel | rename to `abstraction-and-concretization.md`; compact to irreducible cross-role semantics; add Lossless Representation Rule |
| workflow/evidence/testing/architecture/version/health references | refactor generic duplication toward canonical owners; preserve all distinct domain consequences |
| D1/D2/D4, scientific-software, documentation, convergence, repository, language/tool, security, storage, performance, configuration, concurrency, release, debugging, Git references | preserve domain semantics; update routing/nomenclature and compact only where generic doctrine is duplicated |
| shared templates (4) | rename abstraction/concretization template; apply concise current terminology and representation rule without losing required fields |
| `AGENTS.md`, root/source README, `PORTABILITY.md`, `source/SEMANTIC_DEPENDENCIES.md` | reconcile current 6.2 navigation, routing, version identity, and representation contract |
| workflow prompt source | refactor shared cross-stage contract + stage deltas; preserve all stop/authority/evidence semantics |
| orchestrator 5.16/6.0/6.1 resources | frozen; byte/behavior semantics preserved |
| new orchestrator 6.2 profile/prompts/snapshot | generated/current successor; schema v2 unless machine contract changes |
| qualification scenario/routing assets | preserve existing 95-case semantics; add 6.2 representation/routing counterexamples |
| `history/SEMANTIC_EVOLUTION.md` | cold historical owner; append concise 6.2 evolution at closeout, do not rewrite prior entries |
| archived workplans | frozen cold evidence; inspect only for ambiguous/unmapped/challenged lineage |
| `dist/` and generated snapshots | generated descendants; rebuild from canonical source, never hand-author as independent authority |
| active authority index + 6.2 workplan | current cycle routing/coordination; preserve implementation/cutover state |

All 33 current shared references and all four shared templates are included by the family classification above. No current reference is excluded merely because it is not expected to change text.

## Canonical owner map to preserve

```text
universal authority / Challenge / representation -> abstraction-and-concretization.md
D1 formulation                                -> scientific-formulation.md
D2 numerical method                           -> numerical-algorithm-design.md
D3 architecture                               -> architecture-and-design.md
D4 specification                              -> specification-and-implementation.md
workflow / handoff / stages                   -> workflow-and-workplans.md
evidence lifecycle / evolution / dependency   -> evidence-evolution-and-dependencies.md
testing / oracle / validation                 -> testing-and-validation.md
scientific/numerical integration evidence     -> scientific-software.md
recurrence / simplification / cycle economy   -> convergence-and-cycle-economy.md
longitudinal health / stabilization            -> long-horizon-code-health.md
version selection / recovery                  -> protocol-versioning-and-compatibility.md
repository inspection / context economy       -> repository-intake.md
document lifecycle / current-vs-history       -> documentation-maintenance.md
technical/scientific exposition               -> scientific-technical-writing.md
engineering-document/evidence communication   -> documentation-and-evidence.md
language dispatch                             -> language-profiles.md
Python/C++ specialization                     -> python-engineering.md / cpp-engineering.md
relation-first tool dispatch                  -> tool-assisted-engineering.md
specific analyzer methods                     -> tool-serena.md / tool-semgrep.md / tool-hypothesis.md / tool-codeql.md
configuration                                 -> configuration-and-policy.md
concurrency / orchestration engineering       -> concurrency-and-orchestration.md
performance / parallelism                     -> performance-and-parallelism.md
storage / I/O                                 -> storage-and-io.md
security / trust                              -> security-and-trust-boundaries.md
release / distribution                        -> release-and-distribution.md
debugging / recovery                          -> debugging-and-state-recovery.md
Git / version-control mechanics               -> git-and-version-control.md
workflow prompt source                        -> development-workflow-prompts.md
```

If implementation evidence shows accepted ownership differs, preserve the accepted owner and treat this map as wrong evidence rather than creating new precedence.

## Historical capability lineage that must remain recoverable

The normal proof path is current 6.1 owners + the 95 qualification scenarios + semantic evolution. Archived workplans are loaded only where this compact mapping is insufficient.

- **Protocol 5.0:** engineering fitness first; among admissible systems prefer minimum justified total complexity.
- **5.1:** optional software-documentation specialist.
- **5.2:** optional repository-hygiene specialist.
- **5.3:** stage-local/final functional acceptance; production qualification separated from functional acceptance.
- **5.4:** development economy, accepted-workplan authority, bounded redesign, version-bound inheritance, evidence/context reuse, coherent stage granularity, evidence-directed review.
- **5.5:** implementation-fidelity and workflow integration.
- **5.6:** proxy-proof acceptance and explicit test-double boundaries.
- **5.7:** engineering stewardship and protected-outcome alignment.
- **5.8:** effective compression and canonical ownership.
- **5.9:** agent-portable deterministic routing.
- **5.10:** snapshot-complete handoffs.
- **5.11:** relation-first tool-assisted engineering.
- **5.12:** convergent development, recurrence/family reasoning, cycle economy.
- **5.13:** deterministic tool entry, CodeQL routing, progressive-disclosure compression.
- **5.14:** solution-boundary discipline and active simplicity.
- **5.15:** language engineering profiles and cross-language performance semantics.
- **5.16:** long-horizon quality sensors, adversarial Verification, Stabilization, maintenance audit, bounded mutation/differential/metamorphic/failure-injection evidence, canonical parameterized workflow prompts, compatible-local-first/public-source fallback.
- **6.0:** D1-D4 recursive scientific-software authority model; abstraction/concretization generalization; composed scientific closure; bounded Challenge/Serious Challenge; Protocol 5 software-local lifecycle recoverable as D3->D4 specialization.
- **6.1:** current concretization terminology; evidence specification/realization/observation/assessment and applicability; evidence target vs execution dependency; stale evidence both polarities; evidentiary independence/common-mode risk; bounded semantic dependency/evolution records; manual impact closure; background/context + first-use abbreviation standard; distinct frozen 6.0/current 6.1 profiles; immutable compatible public fallback/recovery staging.

## Behavioral preservation oracle

All 95 accepted Protocol 6.1 scenario outcomes remain required. In particular, 6.2 must preserve: root-cause rather than symptom duplication; remove/rewire before additive wrappers; metrics as sensors; compatible-local/public fallback; capability preservation without obsolete vocabulary; bounded urgent mitigation without promotion; compact resumable state without parallel authority; immutable historical-version routing; evidence-target/execution-dependency distinction; stale pass/fail non-admissibility; common-mode evidence reasoning; incomplete-map caution; history-vs-current authority; reader background/abbreviation requirements; frozen 6.0 identity; and current 6.1 profile semantics.

## Routing baseline and expected change

Protocol 6.1 role entrypoints routinely make workflow, evidence, testing, versioning, architecture/health and sometimes language/tool documents unconditional for broad task classes. Protocol 6.2 must preserve every triggered doctrine while reducing initial context through this typed shape:

```text
task/orchestration
 -> role or specialist SKILL.md
      -> minimal universal kernel + owning domain
      -> conditional concern owner
           -> conditional concern-local leaf
```

Activation implies package/source reachability; reachability, hyperlinks, semantic dependency, and package membership do not imply activation. Router prose remains authority; any graph/matrix/trace is derived evidence only.

Representative baseline tasks for before/after comparison: local D4 repair; D3 workplan; independent D4 Review; D2 work; D1 work; documentation reconciliation; maintenance audit; release/package work; historical recovery/migration; closeout. Sensors: unique active protocol bytes/tokens, repeated owner loads, unconditional vs conditional reads, and routing hops. No numerical sensor is a pass threshold.

## Compression proof obligations

For each materially removed/merged/relocated/generalized rule, Review must be able to identify its accepted old owner/location, current 6.2 owner/location, why the new form logically preserves the old obligation over its applicable regime, and the scenario/test/inspection evidence that would detect loss. Multiple old manifestations may map to one stronger current rule; no accepted obligation may be marked superseded merely for compactness.
