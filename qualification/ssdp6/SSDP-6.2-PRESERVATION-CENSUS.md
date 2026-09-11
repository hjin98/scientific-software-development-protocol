---
kind: protocol-implementation-preservation-evidence
protocol_version: 6.1.0
target_protocol_version: 6.2.0
authority: non-normative-evidence
baseline_commit: cec29671b9db59d20124a6e2ce99725ed60b8f0a
workplan: workplans/active/SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT.md
status: transformation-map-complete-pending-independent-review
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

## Artifact-level finite census

This closes the Stage-A artifact granularity explicitly. `Refactor` means the artifact's current representation changed while its accepted semantic obligations remain mapped below; `route-only` means navigation/activation wording changed without taking semantic ownership; `unchanged` means the current owner text remains materially identical for this cycle; `generated` and `frozen/historical` are not independent current authority.

### Role and specialist entrypoints

| Artifact | Disposition | Reason |
| --- | --- | --- |
| `source/roles/scientific-formulation/SKILL.md` | refactor | compact D1 root router; detailed D1/evidence/workflow/writing doctrine remains at owners |
| `source/roles/numerical-algorithm-design/SKILL.md` | refactor | compact D2 root router; detailed numerical/evidence/resource doctrine remains at owners |
| `source/roles/software-design/SKILL.md` | refactor | compact D3 root router; language/tool leaves delegated through concern routers |
| `source/roles/software-implementation/SKILL.md` | refactor | compact D4 root router; implementation acceptance/simplicity/real-owner duties preserved |
| `source/specialists/software-documentation/SKILL.md` | refactor | compact editorial router; explicit cold concern routes remain resolvable |
| `source/specialists/software-maintenance-audit/SKILL.md` | refactor | compact non-authoritative longitudinal audit router |
| `source/specialists/repository-hygiene/SKILL.md` | refactor | compact hygiene router with authority/source-chain boundaries preserved |

### Shared references — all 33 current artifacts

| Artifact | Disposition | Reason |
| --- | --- | --- |
| `abstraction-and-concretization.md` | refactor/current owner | renamed current kernel, compacted universal semantics, adds Lossless Representation Rule |
| `architecture-and-design.md` | refactor | D3 owner retains architecture adequacy/fitness/simplicity semantics |
| `concurrency-and-orchestration.md` | unchanged | concern-local engineering owner remains cold until triggered |
| `configuration-and-policy.md` | unchanged | concern-local policy owner remains cold until triggered |
| `convergence-and-cycle-economy.md` | unchanged | recurrence/simplification/cycle-economy owner retained |
| `cpp-engineering.md` | refactor | C++ language-profile detail retained; terminology/CPU interpretation aligned |
| `debugging-and-state-recovery.md` | unchanged | concern-local debugging/recovery owner retained |
| `development-workflow-prompts.md` | refactor | eleven stage prompts share one execution/authority/evidence contract; stage deltas retained |
| `documentation-and-evidence.md` | refactor | engineering documentation/evidence communication owner compacted |
| `documentation-maintenance.md` | refactor | current-vs-history/source-chain lifecycle owner compacted |
| `evidence-evolution-and-dependencies.md` | refactor | evidence lifecycle/applicability/dependency/evolution becomes sole detailed owner |
| `git-and-version-control.md` | unchanged | Git mechanics owner remains concern-local |
| `language-profiles.md` | refactor | becomes explicit language concern router for Python/C++ leaves |
| `long-horizon-code-health.md` | refactor | health/Verification/Stabilization sensor semantics compacted at owner |
| `numerical-algorithm-design.md` | refactor | D2 owner receives detailed numerical doctrine removed from root duplication |
| `performance-and-parallelism.md` | unchanged | performance/resource owner remains conditionally activated |
| `protocol-versioning-and-compatibility.md` | refactor | version/profile/fallback/recovery owner compacted; exact historical identities preserved |
| `python-engineering.md` | refactor | current routing/nomenclature aligned; Python-specialist semantics remain at leaf |
| `release-and-distribution.md` | unchanged | release/package concern owner remains conditional |
| `repository-intake.md` | refactor | repository/context-economy owner compacted; stale-context constraints preserved |
| `scientific-formulation.md` | refactor | D1 detailed owner receives doctrine removed from root duplication |
| `scientific-software.md` | unchanged | cross-domain scientific/numerical integration evidence owner retained |
| `scientific-technical-writing.md` | refactor | exposition/background/terminology/abbreviation owner compacted |
| `security-and-trust-boundaries.md` | unchanged | security/trust concern owner remains conditional |
| `specification-and-implementation.md` | refactor | D4 specification/code/adaptive-concretization owner compacted |
| `storage-and-io.md` | unchanged | storage/I/O concern owner remains conditional |
| `testing-and-validation.md` | refactor | testing/oracle/proxy-proof/regression/failure-injection methodology owner compacted |
| `tool-assisted-engineering.md` | unchanged/current router | relation-first concern router remains authoritative for tool-leaf dispatch |
| `tool-codeql.md` | unchanged | conditional analyzer leaf retained |
| `tool-hypothesis.md` | unchanged | conditional property-testing leaf retained |
| `tool-semgrep.md` | unchanged | conditional structural-analysis leaf retained |
| `tool-serena.md` | unchanged | conditional semantic-navigation leaf retained |
| `workflow-and-workplans.md` | refactor | workflow/handoff/stage/accepted-plan owner compacted |

### Shared templates — all four current artifacts

| Artifact | Disposition | Reason |
| --- | --- | --- |
| `abstraction_concretization_change_plan_template.md` | refactor/rename | current concretization terminology; material authority/handoff/review fields preserved |
| `implementation_workplan_template.md` | refactor | D3->D4 contract compacted while snapshot completeness/acceptance/reopen fields remain |
| `numerical_algorithmic_method_paper_template.md` | unchanged | current D2 human-facing paper structure retained |
| `scientific_method_paper_template.md` | unchanged | current D1 human-facing paper structure retained |

### Repository, qualification, profile, generated, and historical surfaces

| Artifact/family | Disposition | Reason |
| --- | --- | --- |
| `AGENTS.md` | route-only | compact repository entry routing; no new semantic precedence |
| `README.md` | route-only | current navigation/version state; canonical owners remain authoritative |
| `PORTABILITY.md` | refactor | portability/routing/fallback qualification contract |
| `source/README.md` | route-only | current owner/navigation map |
| `source/SEMANTIC_DEPENDENCIES.md` | route-only | typed current dependency/navigation view; not activation authority |
| `qualification/ssdp6/SCENARIOS.md` + `SCENARIOS-6.1-ADDITIONS.md` | unchanged evidence | frozen semantic capability surface 1–95 |
| `qualification/ssdp6/SCENARIOS-6.2-ADDITIONS.md` | new evidence | representation/routing falsification cases 96–115 |
| `qualification/reference-routing/*` + `qualification/tool-routing/*` | unchanged evidence | existing bounded live-routing/tool assets retained |
| `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` | route-only | lifecycle authority index reconciled without changing Protocol 7 design |
| this 6.2 workplan | current cycle authority | governs this refinement and acceptance sequence |
| `history/SEMANTIC_EVOLUTION.md` | frozen/historical during implementation | prior history unchanged; 6.2 append occurs only at closeout |
| archived workplans | frozen/historical | cold lineage evidence only when current mapping is insufficient |
| packaged 5.16/6.0/6.1 orchestrator resources | frozen | historical profile/prompt bytes and behavior remain version-bound |
| `ssdp-protocol-6.2` profile/prompts | generated/current candidate | schema v2, distinct 6.2 identity, 6.1 stage topology semantics retained |
| `dist/` | generated | canonical skill-package descendants, package membership is not activation |

## Transformation-level closure map

The following rows close the materially transformed accepted obligations from baseline `cec29671b9db59d20124a6e2ce99725ed60b8f0a`. A row may group several old textual manifestations only where the governed obligation and preservation argument are the same. `PRESERVED` means the current 6.2 owner logically retains an equal-or-stronger obligation and the listed oracle would detect material loss; it is evidence, not self-approval. Any future row that cannot be established must be marked `BLOCKING` rather than omitted.

| ID | 6.1 owner/location and transformed obligation | 6.2 owner/location | Preservation relation and evidence | Disposition |
| --- | --- | --- | --- | --- |
| T01 | `abstraction-and-realization.md`: fidelity is feasibility; optimize domain fitness, justified complexity, then economy | `abstraction-and-concretization.md` | Same ordering is stated verbatim-equivalently before representation optimization; `test_protocol_portability`, contract/economy regressions, inherited 95 scenarios | PRESERVED |
| T02 | kernel: authority provenance is orthogonal to D1-D4; side constraints may enter where semantically applicable | kernel + affected concern owners | Current kernel keeps project/external/domain authority and direct side constraints; D3/D4 roots expose security/resource/etc. routes; contract regressions + inherited scenarios | PRESERVED |
| T03 | kernel: D1-D4 form a layered DAG, not mandatory waterfall; reduced routes are valid | kernel + workflow prompts | Current kernel states DAG/non-waterfall; prompts preserve D4-only/D3->D4/D2->D4/D1->D3/D4 paths; `test_protocol_516_orchestration` | PRESERVED |
| T04 | kernel/D3/D4: delegated mechanisms gain no authority by existence; remove/narrow/alter/consolidate before additive machinery | kernel + `architecture-and-design.md` + `specification-and-implementation.md` | Same non-promotion and owning-layer simplification obligations remain; stewardship/effective-compression tests + inherited scenarios | PRESERVED |
| T05 | kernel: reverse verification separately checks concretization fidelity and abstraction adequacy | kernel + role methods | Both questions remain explicit and D1/D2/D3 roots apply them at handoff/review; protocol contract/scenario oracles | PRESERVED |
| T06 | kernel: proposed/accepted/challenged/risk-accepted/stale/historical states; material D1/D2/durable-D3 acceptance requires independent falsification and human gate where applicable | kernel + workflow prompts + D1/D2/D3 roots | Lifecycle states and pre-acceptance independence remain explicit; `test_protocol_516_orchestration`, 6.1 evidence tests, scenarios | PRESERVED |
| T07 | kernel/evidence: accepted changes invalidate only materially dependent descendants/evidence; incomplete dependency view cannot prove independence | kernel + `evidence-evolution-and-dependencies.md` | Current owner retains bounded impact closure, unaffected siblings, incomplete-map caution; `test_protocol_61_evidence_evolution` + scenarios | PRESERVED |
| T08 | kernel/testing: composed D4->D2->D1 closure and problem-appropriate external adequacy; D1/D2 uncertainty stays layer-aware | kernel + `testing-and-validation.md` + D1/D2 owners | Current kernel/testing preserve composed closure and external adequacy distinction; D1/D2 roots retain layer-specific uncertainty | PRESERVED |
| T09 | kernel: bounded Challenge/Serious Challenge; challenged authority stays baseline; risk override does not create ordinary closure | kernel + workflow prompts | Current kernel/prompt keeps trigger, prominence, owner routing, provisional propagation and no counterfeit pass; orchestration/Challenge regressions + scenarios | PRESERVED |
| T10 | `scientific-formulation/SKILL.md`: D1 meaning boundary, independent formulation, external adequacy, evidence/human gate, impact closure, background/abbreviation quality | compact D1 root -> `scientific-formulation.md`, evidence/workflow/testing/writing owners | Root preserves D1 boundary/method/gates and explicit conditional routes; human-facing terminology rule remains; D1 qualification scenarios + routing/package tests | PRESERVED |
| T11 | `numerical-algorithm-design/SKILL.md`: D2 estimator/discretization/error/convergence/precision/stochastic semantics, authority-backed oracles/tolerance, evidence/human gate | compact D2 root -> `numerical-algorithm-design.md`, testing/evidence/performance owners | Root preserves numerical semantics, oracle/tolerance rule, independent acceptance and impact closure; numerical tests + inherited scenarios | PRESERVED |
| T12 | `software-design/SKILL.md`: D3 architecture fitness, accepted/cycle-scoped distinction, minimal ownership/interfaces/state, D4 Review, upstream Challenge | compact D3 root -> `architecture-and-design.md`, workflow/testing/evidence owners | Root retains D3 method, minimum justified architecture, delegation, real-owner acceptance and independent Review/Challenge; architecture/stewardship/proxy tests + scenarios | PRESERVED |
| T13 | `software-implementation/SKILL.md`: adaptive D4, local reconciliation vs redesign, stage-local regression, real-owner proxy proof, final assembled acceptance, stale evidence, impact closure | compact D4 root -> `specification-and-implementation.md`, testing/evidence/workflow/convergence owners | Root retains all decision obligations while detailed test/evidence mechanics move to owners; proxy-proof/effective-compression/testing regressions + scenarios | PRESERVED |
| T14 | `software-documentation/SKILL.md`: editorial-only authority, disagreement classification, current-vs-history, human-facing terminology/abbreviation, source/generated chain | compact documentation root -> documentation owner trio + conditional represented-domain owners | Same authority boundary and human-facing quality rules remain; explicit four cold concern routes repaired; representation/package-route tests | PRESERVED |
| T15 | `repository-hygiene/SKILL.md`: hygiene cannot redefine authority; operate on canonical/source-chain state and preserve version/history | compact hygiene root + repository/document/version/Git owners | Specialist remains non-authoritative and routes semantic questions to owners; package/routing + inherited specialist scenarios | PRESERVED |
| T16 | `software-maintenance-audit/SKILL.md`: longitudinal sensing, metrics are sensors, do not fabricate trends, audit does not implement/accept repair | compact audit root + `long-horizon-code-health.md` | Same non-authoritative longitudinal role and routing boundary remain; long-horizon tests + orchestration scenario | PRESERVED |
| T17 | `evidence-evolution-and-dependencies.md`: evidence specification/realization/observation/assessment, target vs execution dependency, stale pass/fail, common-mode risk, typed dependencies, impact closure, evolution/retirement | same file as sole detailed evidence owner | All listed distinctions and both stale polarities remain explicit; `test_protocol_61_evidence_evolution`, proxy/evidence scenarios | PRESERVED |
| T18 | `testing-and-validation.md`: anti-counterfeit oracles; D1 adequacy; D2 verification/tolerance; D3 checks; D4 focused+affected+integration; stage-local regression; proxy-proof; structural/liveness/failure injection; composed closure; production qualification | same testing owner, compacted | Each material methodology remains explicit; evidence lifecycle detail is routed to evidence owner rather than duplicated; testing/proxy/counterfactual regressions + scenarios | PRESERVED |
| T19 | `workflow-and-workplans.md` + role restatements: accepted-plan binding, bounded redesign/rework, snapshot-complete handoff, stage ownership, impact/closure/reopen discipline | `workflow-and-workplans.md` + compact root local consequences | Generic workflow remains at one owner; roots carry trigger/local consequence; workflow/orchestration tests + inherited cases | PRESERVED |
| T20 | `architecture-and-design.md` + D3 duplication: one authoritative state/ownership, acyclic dependency, minimum justified architecture, resource/security/compatibility adequacy, active simplicity | `architecture-and-design.md` | D3 generic architecture semantics consolidated at accepted owner; D3 root no longer duplicates details; architecture/stewardship/effective-compression tests | PRESERVED |
| T21 | `scientific-formulation.md` + D1 root duplication: observables/models/assumptions/validity/interpretation/external adequacy | `scientific-formulation.md` + compact D1 root | Detailed D1 semantics retained at canonical owner; root activates it unconditionally for D1; D1 scenarios | PRESERVED |
| T22 | `numerical-algorithm-design.md` + D2 root duplication: approximation/error/convergence/conditioning/precision/stochastic semantics | `numerical-algorithm-design.md` + compact D2 root | Detailed D2 semantics retained at canonical owner; root activates it unconditionally for D2; D2/numerical scenarios | PRESERVED |
| T23 | D4 role/spec duplication: D4 specification is intended behavior, code is actual concretization; wrong code does not rewrite spec; compatibility/persistence/errors remain governed | `specification-and-implementation.md` + compact D4 root | Same intended-vs-actual distinction, adaptive implementation, compatibility/error/state and impact rules remain; contract/proxy tests | PRESERVED |
| T24 | long-horizon role/reference duplication: changed-code/structural risk, Verification, Stabilization, maintenance sensors; metrics are sensors | `long-horizon-code-health.md` + audit/D3/D4 local routes | Detailed longitudinal doctrine centralized; prompts preserve distinct Review/Verification/Stabilization/Audit stages; long-horizon/orchestration tests | PRESERVED |
| T25 | documentation duplication: current-vs-history/source chain; technical exposition; evidence communication; background terms/first-use abbreviation | `documentation-maintenance.md`, `scientific-technical-writing.md`, `documentation-and-evidence.md` | Three concerns remain distinct owners; documentation root routes by predicate; 6.1 documentation/evidence qualification + human-facing scenarios | PRESERVED |
| T26 | D3/D4 roots directly enumerated Python/C++ leaves | `language-profiles.md` router -> `python-engineering.md` / `cpp-engineering.md` | Routing representation changes only: executable language semantics still activate when material, now through one concern owner; `test_protocol_portability`, `test_protocol_515_language_profiles`, scenarios 101/103 | PRESERVED |
| T27 | D3/D4 roots directly enumerated Serena/Semgrep/Hypothesis/CodeQL triggers | `tool-assisted-engineering.md` router -> `tool-*` leaves | Relation-first tool semantics and conditional leaf triggers remain at existing router/leaves; tool-routing regressions + scenarios 102/106 | PRESERVED |
| T28 | specialized configuration/concurrency/performance/storage/security/release/debugging/Git/scientific-software/tool-leaf doctrine | same named concern owners | Text is materially unchanged in this cycle or only reached through changed root routing; explicit hot trigger + package closure preserves availability without making it universal context; package closure/routing tests | PRESERVED |
| T29 | version owner: workplan binding, frozen 5.16/6.0/6.1 recovery/profile identities, compatible-local/public resolution, bootstrap vs recovery staging | `protocol-versioning-and-compatibility.md` | Exact frozen identities remain; 6.2 now explicitly distinguishes invalidated bootstrap attempt, self-reference-safe bootstrap staging and later recovery; portability/profile/orchestration tests | PRESERVED |
| T30 | workflow-prompt source: 11 parameterized stages, AUTO_EXECUTE/REPORT_ONLY, mutation boundaries, reduced routes, Challenge, evidence state, independent D1/D2/D3 acceptance, risk override | `development-workflow-prompts.md` shared contract + 11 stage deltas | Generic clauses occur once; every stage keeps role/mutation-specific inputs/actions/stops; `test_protocol_516_orchestration` + orchestrator snapshot/profile tests | PRESERVED |
| T31 | `abstraction_realization_change_plan_template.md`: current generic authority-change plan fields | `abstraction_concretization_change_plan_template.md` | Current terminology corrected without alias; authority, parent/child constraints, evidence, Challenge, acceptance/handoff fields retained; representation/nomenclature tests + frozen historical path tests | PRESERVED |
| T32 | `implementation_workplan_template.md`: snapshot-complete D3->D4 freeze, delegated space, stages, evidence/acceptance/reopen/impact | same template, compacted | Required handoff and closure fields remain; workplan/scenario coverage including snapshot-complete case 111 | PRESERVED |
| T33 | root/source navigation repeated role/reference details | `AGENTS.md`, `README.md`, `source/README.md`, `source/SEMANTIC_DEPENDENCIES.md` as route-only views | Navigation now points to canonical owners and explicitly says links/package membership are not activation; no authority moves into navigation; representation tests | PRESERVED |
| T34 | 6.1 orchestrator current profile semantics and frozen 5.16/6.0 behavior | frozen 5.16/6.0/6.1 resources + new `ssdp-protocol-6.2` schema-v2 profile | 6.2 keeps 6.1 stage topology/machine contract while changing version identity/default current-source profile; frozen bytes independently checked by `orchestrator/tests/test_ssdp6_profiles.py` | PRESERVED |
| T35 | canonical-source distribution contract | generated `dist/` + generated 6.2 orchestrator snapshot | Generated descendants remain subordinate and reproducible from source; package validation/dist parity/snapshot parity are acceptance evidence, not authority | PRESERVED |
| T36 | Protocol 6.1 behavioral capability surface 1–95 | same scenarios rerun under 6.2 plus 96–115 | Frozen-version cases retain their original identities; 6.2 additions falsify compaction/routing/scope/stale-summary/exact-text/public-fallback risks; qualification evidence remains non-authoritative | PRESERVED |
| T37 | accepted 6.1 `software-documentation/SKILL.md`: when material, explicitly route security, performance/scaling, storage/I/O, and generated/shipped-artifact concerns to their named Markdown owners | current `source/specialists/software-documentation/SKILL.md` explicit conditional routes to the same four concern owners | Current router preserves the accepted 6.1 resolvable-route obligation after repairing an intermediate 6.2 compaction regression; `test_documentation_specialist_cold_domain_routes_are_resolvable_and_packaged` + package closure | PRESERVED |
| T38 | 6.1 current prose uses concretization while historical current filename retained `abstraction-and-realization.md` for compatibility | 6.2 current kernel/template use concretization names; frozen 5.16/6.0/6.1 artifacts retain historical paths | Current terminology becomes internally direct without rewriting release-pinned history; nomenclature/frozen-profile tests + scenarios 94/114 | PRESERVED |
| T39 | 6.1 compatible-local/public fallback and immutable bootstrap principle | 6.2 version/prompt/portability staging + remote exact-ref bootstrap oracle | Capability is preserved without advertising a known-stale ref: pre-publication requires truthful non-closure; after publication current mapping must resolve an exact immutable snapshot whose real remote routes are recursively checked | PRESERVED |

## Closure statement for Implementation and Review

All materially transformed obligations identified by the baseline-to-current semantic comparison are represented above as `PRESERVED`; no row is intentionally omitted because it is inconvenient or low-salience. Unchanged concern leaves and frozen historical resources are explicitly classified in the artifact census rather than expanded into fictitious transformations. The later independent reviewer must sample/falsify this map against baseline `cec29671...`; this evidence does not make its own preservation claims authoritative.
