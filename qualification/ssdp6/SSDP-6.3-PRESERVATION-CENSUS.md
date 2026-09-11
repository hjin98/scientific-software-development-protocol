---
kind: protocol-implementation-preservation-evidence
protocol_version: 6.2.0
target_protocol_version: 6.3.0
authority: non-normative-evidence
accepted_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
implementation_branch_start: 5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
semantic_candidate: 8d0ad2395ccd126c133d8aad206cfc859f660124
stage_f_static_sensor_commit: 6d234e583a93a413894393aa2b5ffb8cbbe8ac50
stage_f_qualification_commit: 7ddd3c87b822c3f28bf674f999202e8cd2406aba
independent_review_handoff_commit: 155c25546d37e7ab6be00ec140b912f4bd763434
workplan: workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md
status: stage-f-semantic-qualification-closed-independent-review-pending
---

# Protocol 6.3 Preservation Census

This file is implementation and Review evidence, not semantic authority. Accepted Protocol 6.2 owners define the inherited contract; the active Protocol 6.3 workplan defines the bounded proposed change. The Stage-A census below preserves the pre-mutation mapping and the inherited T01-T39 reconstruction. The later Stage-F closure table records what the assembled Protocol 6.3 candidate actually closed with discriminating qualification evidence. A row that still depends on independent Review or Stage-G lifecycle work remains explicitly open; qualification does not counterfeit those later gates.

## Baseline and frozen identities

```text
accepted Protocol 6.2 recovery:          b59adc77efe6951912cfd705cc43830c58ca27d0
accepted Protocol 6.2 semantic candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted Protocol 6.2 public bootstrap:   5a062ebc472755607b9dc66d33a5ebbc4b7429aa
6.3 implementation branch start:         5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
accepted-main branch point:              bf856f742d1744a8ff50f300ee6493fb93e5c9d0
Protocol 6.3 semantic candidate:          8d0ad2395ccd126c133d8aad206cfc859f660124
Stage-F static sensor evidence:           6d234e583a93a413894393aa2b5ffb8cbbe8ac50
Stage-F 260-decision qualification:       7ddd3c87b822c3f28bf674f999202e8cd2406aba
independent Review handoff:               155c25546d37e7ab6be00ec140b912f4bd763434

frozen orchestrator resource trees:
  sdp-protocol-5.16: 10a5f6707697e55d9e762db7f3b25b19640fccb4
  ssdp-protocol-6.0: 16e5b378a87e32ec648305ba865377bfdf5bdf62
  ssdp-protocol-6.1: 437f95bf15fb8f9ec430fa5e6de221c9a99af299
  ssdp-protocol-6.2: b111f80e39ace08e3888530277ce89743461329d

accepted 6.2 packaged prompt/profile blobs:
  prompts.md: 159c58cbac0a8cf66311ddf7e11ad8eb03644e8c
  profile.json: 6f21ad0592da343db951ffd56d25aa74a881bd8c
```

The four historical resource trees above are immutable during 6.3 implementation. The 6.2 tree is a frozen rollback resource beside the distinct 6.3 profile; it is not rewritten in place.

## Finite durable and generative surface

| Surface | 6.3 disposition | Reason / intended owner |
| --- | --- | --- |
| `source/roles/scientific-formulation/SKILL.md` | route-only/refactor | retain D1 owner; add conditional PEM route and 6.3 version identity |
| `source/roles/numerical-algorithm-design/SKILL.md` | route-only/refactor | retain D2 owner; add conditional PEM route and 6.3 version identity |
| `source/roles/software-design/SKILL.md` | route-only/refactor | retain D3 owner; add conditional PEM/HAS/capability-transfer route |
| `source/roles/software-implementation/SKILL.md` | route-only/refactor | retain D4 owner; add conditional PEM/HAS route |
| `source/specialists/software-documentation/SKILL.md` | route-only/refactor | allow PEM reconciliation without semantic self-promotion |
| `source/specialists/software-maintenance-audit/SKILL.md` | route-only/refactor | longitudinal evidence may surface PEM candidates; audit stays non-authoritative |
| `source/specialists/repository-hygiene/SKILL.md` | route-only/refactor | preserve PEM/evidence bindings through cleanup/archive operations |
| `source/shared/references/abstraction-and-concretization.md` | minimal refactor | retain universal kernel; state PEM/evidence non-authority and conditional routing only |
| `source/shared/references/project-engineering-memory.md` | new current concern owner | canonical detailed PEM schema, family/notice/summary/partition semantics |
| `source/shared/references/evidence-evolution-and-dependencies.md` | refactor | evidence admissibility, observation/assessment lineage, binding health, provenance clusters, PEM impact |
| `source/shared/references/convergence-and-cycle-economy.md` | refactor | family admission/membership/occurrence/recurrence/semantic-ID lineage |
| `source/shared/references/architecture-and-design.md` | refactor | capability authority binding and mechanism-to-capability transfer |
| `source/shared/references/workflow-and-workplans.md` | refactor | conditional activation, HAS/base binding, closeout learning transaction |
| `source/shared/references/testing-and-validation.md` | refactor | claim-relative maturity, counterfactual/causal/comparative evidence discipline |
| `source/shared/references/documentation-maintenance.md` | refactor | current PEM vs history/source-chain lifecycle; no editorial promotion |
| `source/shared/references/protocol-versioning-and-compatibility.md` | refactor | 6.3 schema/profile/bootstrap/recovery/version-bound behavior |
| `source/shared/references/repository-intake.md` | refactor | bounded PEM intake/progressive disclosure/partial-memory and stale-index behavior |
| `source/shared/references/git-and-version-control.md` | refactor | accepted base vs overlay, provisional IDs, semantic merge, self-reference-safe staging |
| `source/shared/references/security-and-trust-boundaries.md` | refactor | durable PEM privacy/trust and evidence-as-data instruction boundary |
| other current shared references | intentionally unchanged unless a later bounded impact proves otherwise | existing concern owners remain authoritative/cold; do not broaden 6.3 mechanically |
| `source/shared/templates/project_engineering_memory_template.md` | new | one supported human-editable canonical schema-1 template |
| existing four shared templates | intentionally unchanged unless bounded impact proves otherwise | 6.3 does not redefine D1/D2/D3-D4 plan template semantics |
| `source/shared/references/development-workflow-prompts.md` | refactor | current 6.3 workflow prompts conditionally consume PEM/HAS where material |
| `source/PROTOCOL_VERSION` | refactor | proposed canonical source advances to `6.3.0` at semantic-source stage |
| `source/SEMANTIC_DEPENDENCIES.md` | route-only | current dependency/navigation view gains PEM owner and profile relation; remains non-authoritative |
| `source/README.md`, root `README.md`, `PORTABILITY.md`, `AGENTS.md` | route/version reconciliation | current navigation and proposed/current lifecycle wording only |
| `PROJECT-ENGINEERING-MEMORY.md` | new project-local state | self-hosted SSDP schema-1 PEM; never generic packaged protocol state |
| `source/project_engineering_memory.py` or smallest equivalent validator | new D4 validation utility if required | deterministic Markdown-schema validation only; no DB/index authority/daemon |
| `tests/test_protocol_63_engineering_memory.py` | new qualification executable evidence | counterfactual structural/semantic cases for 6.3 memory contract |
| existing tests including `test_protocol_62_*` | affected regression, source unchanged unless compatibility test must generalize | all accepted 6.2 behavior remains required |
| `qualification/ssdp6/SCENARIOS.md` and `SCENARIOS-6.1-ADDITIONS.md` | frozen evidence | inherited cases 1-95 |
| `qualification/ssdp6/SCENARIOS-6.2-ADDITIONS.md` | frozen evidence | inherited cases 96-115 |
| `qualification/ssdp6/SCENARIOS-6.3-ADDITIONS.md` | new evidence | Q63/falsification scenario descriptions as needed |
| `qualification/ssdp6/*6.3*` qualification/handoff/review records | new evidence | non-authoritative stage/independent Review evidence |
| `orchestrator/src/.../core/canonical.py` | refactor | distinct `ssdp-protocol-6.3` identity reusing accepted 6.x stage topology |
| `orchestrator/src/.../core/profile.py` | refactor | distinct schema-v2 6.3 definition/default after source candidate; 6.2 becomes frozen |
| `orchestrator/scripts/generate_protocol_snapshot.py` | refactor | generate 6.3 and verify immutable 5.16/6.0/6.1/6.2 resources |
| `orchestrator/src/.../resources/protocol/ssdp-protocol-6.3/*` | generated new | canonical prompt/profile snapshot; no mutation of earlier profile trees |
| orchestrator tests/docs/current default text | affected reconciliation | validate/select 6.3 while preserving explicit older compatibility |
| `dist/` | generated | rebuild only from canonical source; live `PROJECT-ENGINEERING-MEMORY.md` excluded |
| `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` | Stage-G route/lifecycle reconciliation | no silent Protocol 7 D3 change |
| this 6.3 workplan | current cycle contract | remains active until full lifecycle closeout |
| `history/SEMANTIC_EVOLUTION.md` | frozen during implementation; append at accepted closeout | history explains why, never current authority |
| archived workplans/reviews | frozen historical evidence | no terminology rewrite/backfill mutation |

This census is finite over current durable/generative protocol surfaces known at branch start. Later discovery of a materially affected current surface expands the affected implementation surface under already-binding authority; it is not requirement expansion and must be added here rather than omitted.

## Inherited T01-T39 preservation map

The accepted 6.2 census was independently re-read rather than using labels alone. The 6.3 target owner may add PEM-local consequences, but cannot weaken the inherited obligation.

| ID | Inherited obligation | 6.3 owner/disposition | Discriminating evidence |
| --- | --- | --- | --- |
| T01 | fidelity before fitness/complexity/economy | universal kernel; PRESERVED | inherited contracts/scenarios |
| T02 | authority provenance orthogonal to domain; side constraints apply where semantic | kernel + concern owners; PRESERVED | role/contract regression |
| T03 | D1-D4 DAG, not waterfall; reduced routes valid | kernel/workflow; PRESERVED | orchestration scenarios |
| T04 | delegated mechanism gains no authority; simplify owning layer before additive machinery | kernel/architecture/convergence; PRESERVED | stewardship/effective-compression cases |
| T05 | verification separates concretization fidelity from abstraction adequacy | kernel/roles; PRESERVED | contract/scenario cases |
| T06 | lifecycle states; material authority acceptance requires proper falsification/human gate where applicable | kernel/workflow/roles; PRESERVED | orchestration/evidence cases |
| T07 | bounded impact closure; incomplete map cannot prove independence | evidence owner; PRESERVED | 6.1 evidence tests/scenarios |
| T08 | composed D4->D2->D1 closure and external adequacy distinction | kernel/testing/D1/D2; PRESERVED | scientific/numerical scenarios |
| T09 | Challenge/Serious Challenge prominence and no counterfeit closure | kernel/workflow; PRESERVED | Challenge/orchestration scenarios |
| T10 | D1 boundary/method/evidence/human/background rules | D1 root + owners; PRESERVED | D1/routing/package cases |
| T11 | D2 numerical semantics/oracle/tolerance/evidence rules | D2 root + owners; PRESERVED | D2/numerical cases |
| T12 | D3 architecture fitness/delegation/Review/upstream Challenge | D3 root + architecture/workflow/testing; PRESERVED | architecture/proxy cases |
| T13 | D4 adaptive implementation/local reconciliation/stage+final acceptance/real-owner/stale evidence | D4 root + D4/testing/evidence; PRESERVED | proxy/testing cases |
| T14 | documentation specialist non-authority/current-history/background/source chain | documentation root + owners; PRESERVED | documentation routing/package cases |
| T15 | hygiene cannot redefine authority/history/source chain | hygiene + Git/repository/docs; PRESERVED | specialist/package cases |
| T16 | maintenance audit is longitudinal sensing; metrics not verdict; no self-repair authority | audit + health owner; PRESERVED | long-horizon/orchestration cases |
| T17 | complete evidence specification/realization/observation/assessment/applicability/dependency/evolution distinctions | evidence owner; PRESERVED | 6.1 evidence/proxy cases |
| T18 | testing/oracle/D1-D4/stage-local/proxy/failure-injection/final acceptance methodology | testing owner; PRESERVED | testing/counterfactual cases |
| T19 | accepted-plan binding, bounded rework, snapshot handoff, impact/closure/reopen | workflow owner; PRESERVED | workflow/orchestration cases |
| T20 | one D3 authoritative state/ownership, acyclic dependencies, minimum architecture | architecture owner; PRESERVED | architecture/stewardship cases |
| T21 | D1 observables/models/assumptions/validity/interpretation/adequacy | D1 owner; PRESERVED | D1 scenarios |
| T22 | D2 approximation/error/convergence/conditioning/precision/stochastic semantics | D2 owner; PRESERVED | D2 scenarios |
| T23 | D4 specification intended behavior vs actual code; compatibility/persistence/error contracts | D4 owner; PRESERVED | contract/proxy cases |
| T24 | health/Verification/Stabilization sensors; metrics remain sensors | health owner + routes; PRESERVED | long-horizon cases |
| T25 | documentation current/history/source chain/exposition/evidence/background abbreviation | documentation owners; PRESERVED | documentation qualification |
| T26 | language router preserves Python/C++ conditional specialization | language router; PRESERVED | portability/language-profile cases |
| T27 | relation-first tool router preserves Serena/Semgrep/Hypothesis/CodeQL triggers | tool router; PRESERVED | tool-routing cases |
| T28 | specialized cold concern doctrine remains reachable without universal activation | named concern owners; PRESERVED | package/routing closure |
| T29 | version binding, immutable historical recovery/profiles, local/public fallback, bootstrap/recovery distinction | version owner; PRESERVED | portability/profile/orchestration cases |
| T30 | 11 parameterized workflow stages, modes, reduced routes, Challenge/evidence/acceptance semantics | workflow prompt owner; PRESERVED | orchestration/profile cases |
| T31 | generic authority-change template semantics under current terminology | existing template; PRESERVED | nomenclature/template tests |
| T32 | D3->D4 workplan snapshot completeness/delegation/stages/evidence/reopen | implementation template; PRESERVED | snapshot/workplan scenarios |
| T33 | root/source docs are navigation/derived views, not authority/activation | navigation surfaces; PRESERVED | representation tests |
| T34 | 6.x profile machine topology plus immutable 5.16/6.0/6.1 resources | profile owner; PRESERVED | orchestrator profile/frozen-resource tests |
| T35 | canonical source -> generated dist/profile reproducibility | build/snapshot generators; PRESERVED | build/validate/check-dist/snapshot |
| T36 | behavioral scenario surface 1-115 remains required | qualification; PRESERVED | fresh rerun 1-115 inside 260-decision Stage-F result |
| T37 | documentation specialist cold routes to security/performance/storage/release remain resolvable/packaged | documentation root; PRESERVED | route/package test |
| T38 | current concretization terminology; frozen historical lexemes remain unchanged | current owners + frozen resources; PRESERVED | nomenclature/frozen-profile tests |
| T39 | compatible-local/public fallback requires exact immutable validated bootstrap; never default/latest | version owner; PRESERVED | exact-ref fallback/bootstrap qualification |

## Protocol 6.3 Stage-F closure map for T40-T120

The Stage-A mapping originally marked T40-T120 open. The assembled candidate and Stage-F qualification now close the semantic/representation obligations except where the row itself contains a later lifecycle or independent-Review event. `QUALIFICATION_CLOSED` means the candidate semantics and discriminating qualification are closed; it does **not** mean Protocol 6.3 is accepted-current.

| IDs | Target semantic group | Current disposition | Evidence / remaining gate |
| --- | --- | --- | --- |
| T40-T61 | authority separation through logical canonical memory, evidence/statistics/temperature/HAS/capability/coverage/progressive disclosure/package separation | QUALIFICATION_CLOSED | semantic candidate `8d0ad239...`; focused PEM counterfactuals; 260-decision result `7ddd3c87...`; final static sensors `6d234e58...` where structural routing is material |
| T62 | 6.3 bootstrap/profile/recovery/version staging | PARTIAL_STAGE_G | exact bootstrap `1484c1d3...` and distinct schema-v2 profile are qualified; immutable recovery selection/mapping remains Stage G after independent Review |
| T63-T65 | frozen prior resources; source/generated/package parity; static-vs-live claim discipline | QUALIFICATION_CLOSED | candidate CI `34622113601`; hardening CI `34621952288`; final static sensors `6d234e58...`; live telemetry remains deliberately unclaimed |
| T66 | Protocol 7 inheritance/current-lifecycle reconciliation | OPEN_STAGE_G | no silent Protocol-7 D3 change occurred; final accepted-current/history/authority-index reconciliation belongs after Review/recovery |
| T67 | human-facing background/terminology/abbreviation completeness | QUALIFICATION_CLOSED | inherited documentation scenarios plus full source/package regression on candidate |
| T68 | independent assembled-candidate qualification/Review | OPEN_INDEPENDENT_REVIEW | handoff `155c2554...` prepared; implementation-context 260/260 result cannot satisfy independent Review |
| T69 | anti-scope-laundering/lower-salience mandatory preservation | QUALIFICATION_CLOSED | fresh Scope/materiality laundering and Priority inversion Challenge passes in `7ddd3c87...` |
| T70-T120 | recursive-warrant prevention through watermark/coverage separation, including authority binding, base/overlay, trust, provenance, assessment supersession, causality, recurrence, semantic identity, maturity/comparative guidance, salience and HAS-basis rules | QUALIFICATION_CLOSED | current concern owners + executable PEM tests + candidate CI/hardening runs + Q63/F63 counterfactuals in `7ddd3c87...` |

No T40-T120 row is closed merely because prose exists. Mechanically decidable false-pass paths discovered during Stage F were repaired before the candidate freeze: assessment current state now uses explicit supersession rather than list/latest-editor order; discovery/capability evidence requires non-empty routes; unresolved binding state remains visible in the active summary; and active lineage targets cannot simultaneously masquerade as unqualified current peers.

## Source-generation and lifecycle boundary

The completed implementation-side sequence is:

```text
canonical 6.3 doctrine/routes/template + PEM validator/tests
 -> source regression and focused 6.3 qualification
 -> immutable self-reference-safe public-source bootstrap
 -> descendant publication of exact bootstrap identity
 -> distinct 6.3 orchestrator profile/snapshot and generated dist
 -> full inherited + 6.3 Stage-F qualification
 -> snapshot-complete independent assembled-candidate Review handoff
```

The still-open lifecycle is:

```text
fresh independent assembled-candidate Review
 -> immutable recovery descendant only after Review PASS
 -> later recovery mapping + mapping-bearing regeneration
 -> targeted recovery/profile/package/Core acceptance
 -> lifecycle/history/authority-index/self-hosted accepted-PEM/Protocol-7 reconciliation
 -> workplan archive / separately authorized cutover
```

`PROJECT-ENGINEERING-MEMORY.md` is project-local state. It is never copied into generic `dist/` packages or protocol profile snapshots.

## Current gate disposition

```text
SERIOUS CHALLENGE: NONE IDENTIFIED IN IMPLEMENTATION-CONTEXT QUALIFICATION
INHERITED T01-T39: RECONSTRUCTED, PRESERVED, AND REQUALIFIED
T40-T61: QUALIFICATION_CLOSED
T62: PARTIAL_STAGE_G — recovery leg intentionally open
T63-T65: QUALIFICATION_CLOSED
T66: OPEN_STAGE_G — final Protocol-7/current-lifecycle reconciliation
T67: QUALIFICATION_CLOSED
T68: OPEN_INDEPENDENT_REVIEW
T69-T120: QUALIFICATION_CLOSED
SEMANTIC CANDIDATE: 8d0ad2395ccd126c133d8aad206cfc859f660124
POST-CANDIDATE SEMANTIC MUTATION THROUGH HANDOFF: NONE
STAGE-F 260-DECISION RESULT: 7ddd3c87b822c3f28bf674f999202e8cd2406aba
INDEPENDENT REVIEW HANDOFF: 155c25546d37e7ab6be00ec140b912f4bd763434
PROTOCOL 6.3 RECOVERY: UNAVAILABLE
ACCEPTED CURRENT PROTOCOL: 6.2.0
MAIN CUTOVER: NOT AUTHORIZED
```