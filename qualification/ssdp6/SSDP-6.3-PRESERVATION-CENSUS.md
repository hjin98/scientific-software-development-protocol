---
kind: protocol-implementation-preservation-evidence
protocol_version: 6.2.0
target_protocol_version: 6.3.0
authority: non-normative-evidence
accepted_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
implementation_branch_start: 5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
workplan: workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md
status: stage-a-census-complete-source-mutation-authorized
---

# Protocol 6.3 Preservation Census

This file is implementation and Review evidence, not semantic authority. Accepted Protocol 6.2 owners define the inherited contract; the active Protocol 6.3 workplan defines the bounded proposed change. `PRESERVED` on T01-T39 means the accepted Protocol 6.2 implementation state inherited at the branch start already satisfies the accepted preservation row. T40-T120 are **qualification targets** and remain `OPEN` until the assembled Protocol 6.3 candidate closes them with the listed owner/evidence. No T40-T120 `OPEN` state is represented as a pass.

## Baseline and frozen identities

```text
accepted Protocol 6.2 recovery:          b59adc77efe6951912cfd705cc43830c58ca27d0
accepted Protocol 6.2 semantic candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted Protocol 6.2 public bootstrap:   5a062ebc472755607b9dc66d33a5ebbc4b7429aa
6.3 implementation branch start:         5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
accepted-main branch point:              bf856f742d1744a8ff50f300ee6493fb93e5c9d0

frozen orchestrator resource trees:
  sdp-protocol-5.16: 10a5f6707697e55d9e762db7f3b25b19640fccb4
  ssdp-protocol-6.0: 16e5b378a87e32ec648305ba865377bfdf5bdf62
  ssdp-protocol-6.1: 437f95bf15fb8f9ec430fa5e6de221c9a99af299
  ssdp-protocol-6.2: b111f80e39ace08e3888530277ce89743461329d

accepted 6.2 packaged prompt/profile blobs:
  prompts.md: 159c58cbac0a8cf66311ddf7e11ad8eb03644e8c
  profile.json: 6f21ad0592da343db951ffd56d25aa74a881bd8c
```

The four historical resource trees above are immutable during 6.3 implementation. The 6.2 tree becomes a frozen rollback resource when the distinct 6.3 profile is created; it is not rewritten in place.

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
| T34 | 6.x profile machine topology plus immutable 5.16/6.0/6.1 resources | profile owner; PRESERVED before 6.3 mutation | orchestrator profile tests |
| T35 | canonical source -> generated dist/profile reproducibility | build/snapshot generators; PRESERVED | build/validate/check-dist/snapshot |
| T36 | behavioral scenario surface 1-115 remains required | qualification; PRESERVED | rerun 115 scenarios under 6.3 |
| T37 | documentation specialist cold routes to security/performance/storage/release remain resolvable/packaged | documentation root; PRESERVED | route/package test |
| T38 | current concretization terminology; frozen historical lexemes remain unchanged | current owners + frozen resources; PRESERVED | nomenclature/frozen-profile tests |
| T39 | compatible-local/public fallback requires exact immutable validated bootstrap; never default/latest | version owner; PRESERVED | exact-ref fallback/remote route oracle |

## Protocol 6.3 qualification targets T40-T120

Each row names the canonical owner or concern whose implementation must close it. `OPEN` is deliberate until implementation and qualification produce evidence.

| IDs | Target semantic group | Owning implementation surface | Stage-A state |
| --- | --- | --- | --- |
| T40-T46 | authority/non-authority separation; compact PEM; stable family identity; durable evidence binding; ledger-derived statistics; positive patterns/tradeoffs; hypothesis/maturity/applicability separation | PEM + evidence + convergence | OPEN |
| T47-T54 | reproducible temperature; coverage/no-absence inference; semantic family membership; local-defect economy; HAS; capability transfer; owner-backed promotion; closeout learning | PEM + convergence + workflow + architecture | OPEN |
| T55-T61 | effect/envelope preservation; contradiction/retirement; evidence applicability; independence; progressive disclosure; project-local/package separation; one logical canonical memory | PEM + evidence + testing + repository/package | OPEN |
| T62-T69 | version/bootstrap/profile/recovery; frozen resources; generated parity; static/live discipline; Protocol 7 lifecycle; human-facing terminology; independent Review; anti-scope laundering | version/profile/package + writing + Review | OPEN |
| T70-T77 | no recursive proof; capability authority binding; self-reference-safe updates; balanced positive evidence; count/rate separation; temperature/activation distinction; base/branch lifecycle; stable accepted/provisional IDs | PEM + evidence + Git + workflow | OPEN |
| T78-T85 | security/privacy; owner-responsible updates; cross-domain conditional applicability; doctrine deduplication; lifecycle context; pre-admission counterevidence; applicability-led HAS; aggregation stratification | security + PEM + workflow/testing | OPEN |
| T86-T93 | binding health; reverse authority impact; failure-family disconfirming evidence; notice expiry; matched comparators; positive-guidance eligibility; current-state workplan; schema compatibility/migration | evidence + PEM + workflow/version/testing | OPEN |
| T94-T102 | accepted memory basis; corruption/rollback/downgrade/re-adoption; evidence retraction; unresolved assessment disagreement; context scaling; canonical partition/index fallback; fork provenance; Git ownership; revert impact | PEM + Git + repository + evidence/version | OPEN |
| T103-T111 | typed non-recursive PEM relations/transitive impact; atomic logical publication; branch overlay; applicability co-evolution; observation/association/causality; recurrence lineage; cross-repo source identity; unresolved-risk salience; untrusted evidence remains data | PEM + evidence + Git + workflow/security | OPEN |
| T112-T120 | semantic-ID envelope/acyclic lineage; application-episode vs surface breadth; immutable observation/superseding assessment; claim-relative maturity; absolute vs comparative guidance; overlapping-guidance conflict; HAS basis pinning; provenance clusters; watermark vs coverage | PEM + evidence + convergence + workflow/testing | OPEN |

The detailed wording and Q63/F63 discriminators for T40-T120 remain in the active workplan and must be implemented losslessly at the named owners. This census deliberately does not copy the entire workplan into a second authority.

## Planned source-generation boundary

The implementation sequence after this Stage-A gate is:

```text
canonical 6.3 doctrine/routes/template + PEM validator/tests
 -> source regression and focused 6.3 qualification
 -> immutable self-reference-safe public-source bootstrap
 -> descendant publication of exact bootstrap identity
 -> distinct 6.3 orchestrator profile/snapshot and generated dist
 -> full inherited + 6.3 qualification
 -> independent assembled-candidate Review
 -> immutable recovery
 -> later recovery mapping + mapping-bearing regeneration
 -> lifecycle/history/authority-index reconciliation
```

`PROJECT-ENGINEERING-MEMORY.md` is project-local state. It is never copied into generic `dist/` packages or protocol profile snapshots.

## Stage-A gate disposition

```text
SERIOUS CHALLENGE: NONE
INHERITED T01-T39: RECONSTRUCTED AND PRESERVED AT BRANCH BASELINE
NEW T40-T120: EXPLICITLY MAPPED; OPEN PENDING IMPLEMENTATION/QUALIFICATION
FINITE DURABLE/GENERATIVE SURFACE: BOUNDED
CANONICAL SOURCE MUTATION: AUTHORIZED BY WORKPLAN STAGE-A GATE
MAIN CUTOVER: NOT AUTHORIZED
```
