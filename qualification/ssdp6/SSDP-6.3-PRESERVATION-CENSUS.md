---
kind: protocol-implementation-preservation-evidence
protocol_version: 6.2.0
target_protocol_version: 6.3.0
authority: non-normative-evidence
accepted_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
implementation_branch_start: 5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
semantic_candidate: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
public_source_bootstrap: e12572c021087308570abfa41657a910c6896457
public_source_mapping_commit: e6a8c12f065c3d25a41da804c129d6bc0a4f7b50
stage_f_static_sensor_commit: 6fc26ce374b5346495782871d5d7241de5b90071
stage_f_qualification_commit: 6fc26ce374b5346495782871d5d7241de5b90071
independent_review_handoff: qualification/ssdp6/INDEPENDENT-REVIEW-HANDOFF-PROTOCOL-6.3.md
workplan: workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md
status: f5-qualified-independent-review-pending
---

# Protocol 6.3 Preservation Census

This file is implementation and Review evidence, not semantic authority. Accepted Protocol 6.2 owners define the inherited contract; the active Protocol 6.3 workplan defines the bounded proposed change. The census preserves the finite pre-mutation surface and the independently reconstructed T01-T39 baseline while recording the repaired candidate's T40-T120 closure state. A row that belongs to independent Review or Stage G remains open until that event actually occurs.

## Baseline, repaired candidate, and frozen identities

```text
accepted Protocol 6.2 recovery:            b59adc77efe6951912cfd705cc43830c58ca27d0
accepted Protocol 6.2 semantic candidate:  ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted Protocol 6.2 public bootstrap:    5a062ebc472755607b9dc66d33a5ebbc4b7429aa
6.3 implementation branch start:           5508911f3227c7bcb7e38b0c74a7a37f13fd6b7c
accepted-main branch point:                bf856f742d1744a8ff50f300ee6493fb93e5c9d0

historical invalidated chain 1:             1484c1d3... -> 8d0ad239...
historical invalidated chain 2:             5ee4b3ac... -> 1bfb7894... -> 7f677415... -> 5f52fbdf...
reviewed NO-PASS repair state:              100cbde296de6c1a8db14151f34cfacfebc90eb3

current repaired public bootstrap:          e12572c021087308570abfa41657a910c6896457
later public mapping descendant:            e6a8c12f065c3d25a41da804c129d6bc0a4f7b50
final implementation semantic candidate:    3bbbdfa8120646d76336c7b916e6a891c9ed38f2
fresh F2/static-sensor evidence:             6fc26ce374b5346495782871d5d7241de5b90071
independent Review:                          PENDING
Protocol 6.3 recovery:                       UNAVAILABLE
```

Frozen orchestrator resource trees retained across 6.3 implementation:

```text
sdp-protocol-5.16: 10a5f6707697e55d9e762db7f3b25b19640fccb4
ssdp-protocol-6.0:  16e5b378a87e32ec648305ba865377bfdf5bdf62
ssdp-protocol-6.1:  437f95bf15fb8f9ec430fa5e6de221c9a99af299
ssdp-protocol-6.2:  b111f80e39ace08e3888530277ce89743461329d
```

Accepted 6.2 packaged blobs remain:

```text
prompts.md:   159c58cbac0a8cf66311ddf7e11ad8eb03644e8c
profile.json: 6f21ad0592da343db951ffd56d25aa74a881bd8c
```

Earlier 6.3 chains are preserved as historical evidence and negative fixtures only; no current PASS disposition relies on them as acceptance identities.


## Finite durable and generative surface

| Surface | 6.3 disposition | Reason / owner |
| --- | --- | --- |
| `source/roles/scientific-formulation/SKILL.md` | route-only/refactor | retain D1 owner; conditional PEM route/version identity |
| `source/roles/numerical-algorithm-design/SKILL.md` | route-only/refactor | retain D2 owner; conditional PEM route/version identity |
| `source/roles/software-design/SKILL.md` | route-only/refactor | retain D3 owner; conditional PEM/HAS/capability-transfer route |
| `source/roles/software-implementation/SKILL.md` | route-only/refactor | retain D4 owner; conditional PEM/HAS route |
| `source/specialists/software-documentation/SKILL.md` | route-only/refactor | PEM reconciliation without semantic self-promotion |
| `source/specialists/software-maintenance-audit/SKILL.md` | route-only/refactor | longitudinal sensing may propose PEM; audit stays non-authoritative |
| `source/specialists/repository-hygiene/SKILL.md` | route-only/refactor | preserve PEM/evidence bindings through cleanup/archive |
| `source/shared/references/abstraction-and-concretization.md` | minimal refactor | retain universal kernel; PEM/evidence non-authority and conditional routing |
| `source/shared/references/project-engineering-memory.md` | new owner | canonical PEM semantics, family/notice/summary/partition contract |
| `source/shared/references/evidence-evolution-and-dependencies.md` | refactor | admissibility, binding health, observation/assessment lineage, provenance, impact |
| `source/shared/references/convergence-and-cycle-economy.md` | refactor | family admission/membership/occurrence/recurrence/semantic identity |
| `source/shared/references/architecture-and-design.md` | refactor | capability authority binding and mechanism-to-capability transfer |
| `source/shared/references/workflow-and-workplans.md` | refactor | conditional activation, accepted base/overlay/HAS, closeout learning |
| `source/shared/references/testing-and-validation.md` | refactor | claim-relative maturity and counterfactual/causal/comparative evidence discipline |
| `source/shared/references/documentation-maintenance.md` | refactor | current PEM/history/source-chain lifecycle; no editorial promotion |
| `source/shared/references/protocol-versioning-and-compatibility.md` | refactor | 6.3 schema/profile/bootstrap/recovery/version behavior |
| `source/shared/references/repository-intake.md` | refactor | bounded PEM intake/progressive disclosure/partial-memory/stale-index behavior |
| `source/shared/references/git-and-version-control.md` | refactor | accepted base vs overlay, provisional IDs, semantic merge, self-reference-safe publication |
| `source/shared/references/security-and-trust-boundaries.md` | refactor | durable privacy/trust and evidence-as-data instruction boundary |
| other current shared references | intentionally unchanged unless bounded impact proves otherwise | existing concern owners remain authoritative/cold |
| `source/shared/templates/project_engineering_memory_template.md` | new | one supported human-editable schema-1 template |
| existing D1/D2/D3-D4 plan templates | intentionally unchanged | 6.3 does not redefine their semantics |
| `source/shared/references/development-workflow-prompts.md` | refactor | current workflow conditionally consumes PEM/HAS where material |
| `source/PROTOCOL_VERSION` | refactor | canonical source `6.3.0` in candidate |
| `source/SEMANTIC_DEPENDENCIES.md` | route-only | navigation gains PEM owner/profile relation; remains non-authoritative |
| root/source README, `PORTABILITY.md`, `AGENTS.md` | route/version reconciliation | navigation and lifecycle wording only |
| `PROJECT-ENGINEERING-MEMORY.md` | new project-local state | self-hosted schema-1 PEM; excluded from generic packages |
| `source/project_engineering_memory.py` | new D4 validation utility | deterministic schema/semantic validation; no DB/index authority/daemon |
| `tests/test_protocol_63_engineering_memory.py` | executable qualification | original 6.3 counterfactual coverage |
| `tests/test_protocol_63_reopened_repairs.py` | executable qualification | reopened D1-D7 discriminators |
| `tests/test_protocol_63_bootstrap.py` | executable qualification | self-reference-safe exact-fallback lifecycle |
| inherited tests including `test_protocol_62_*` | affected regression | accepted 6.2 behavior remains required |
| inherited scenario files through 6.2 | frozen evidence | scenarios 1-115 |
| `qualification/ssdp6/SCENARIOS-6.3-ADDITIONS.md` | new evidence | Q63/F63 scenario specification |
| 6.3 qualification/handoff/review records | new evidence | non-authoritative lifecycle/Review evidence |
| orchestrator canonical/profile/generator code | refactor | distinct `ssdp-protocol-6.3` using inherited 6.x topology |
| `orchestrator/.../resources/protocol/ssdp-protocol-6.3/*` | generated new | canonical 6.3 profile/prompts/snapshot only |
| earlier orchestrator protocol resources | frozen | immutable 5.16/6.0/6.1/6.2 resources |
| `dist/` | generated | canonical-source build; live project PEM excluded |
| `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` | Stage-G reconciliation | no silent Protocol-7 D3 change |
| active 6.3 workplan | current cycle contract | remains active through independent Review and Stage G |
| `history/SEMANTIC_EVOLUTION.md` | Stage-G/closeout append only | history explains why; never current authority |
| archived workplans/reviews | frozen historical evidence | no retroactive rewrite |

Later discovery of a materially affected current surface expands this evidence map under already-binding authority; omission does not become permission to shrink scope.

## Inherited T01-T39 preservation map

| ID | Inherited obligation | 6.3 owner/disposition | Discriminating evidence |
| --- | --- | --- | --- |
| T01 | fidelity before fitness/complexity/economy | universal kernel; PRESERVED | inherited contracts/scenarios |
| T02 | authority provenance orthogonal to domain; semantic side constraints apply | kernel + concern owners; PRESERVED | role/contract regression |
| T03 | D1-D4 DAG, not waterfall; reduced routes valid | kernel/workflow; PRESERVED | orchestration scenarios |
| T04 | delegated mechanism gains no authority; simplify owner before additive machinery | kernel/architecture/convergence; PRESERVED | stewardship/compression cases |
| T05 | verification separates concretization fidelity from abstraction adequacy | kernel/roles; PRESERVED | contract/scenario cases |
| T06 | lifecycle states; material authority acceptance needs required falsification/human gate | kernel/workflow/roles; PRESERVED | orchestration/evidence cases |
| T07 | bounded impact closure; incomplete map cannot prove independence | evidence owner; PRESERVED | 6.1 evidence tests/scenarios |
| T08 | composed D4->D2->D1 closure and external adequacy distinction | kernel/testing/D1/D2; PRESERVED | scientific/numerical scenarios |
| T09 | Challenge/Serious Challenge prominence; no counterfeit closure | kernel/workflow; PRESERVED | Challenge/orchestration scenarios |
| T10 | D1 boundary/method/evidence/human/background rules | D1 root + owners; PRESERVED | D1/routing/package cases |
| T11 | D2 numerical semantics/oracle/tolerance/evidence rules | D2 root + owners; PRESERVED | D2/numerical cases |
| T12 | D3 architecture fitness/delegation/Review/upstream Challenge | D3 + architecture/workflow/testing; PRESERVED | architecture/proxy cases |
| T13 | D4 adaptive implementation/reconciliation/stage+final acceptance/real-owner/stale evidence | D4/testing/evidence; PRESERVED | proxy/testing cases |
| T14 | documentation non-authority/current-history/background/source chain | documentation owners; PRESERVED | documentation/package cases |
| T15 | hygiene cannot redefine authority/history/source chain | hygiene + Git/repository/docs; PRESERVED | specialist/package cases |
| T16 | maintenance audit is sensing; metrics not verdict; no self-repair authority | audit + health owner; PRESERVED | long-horizon cases |
| T17 | evidence specification/realization/observation/assessment/applicability/dependency/evolution distinctions | evidence owner; PRESERVED | 6.1 evidence/proxy cases |
| T18 | testing/oracle/D1-D4/stage-local/proxy/failure-injection/final acceptance methodology | testing owner; PRESERVED | testing/counterfactual cases |
| T19 | accepted-plan binding, bounded rework, snapshot handoff, impact/closure/reopen | workflow owner; PRESERVED | workflow/orchestration cases |
| T20 | one D3 authoritative state/ownership, acyclic dependencies, minimum architecture | architecture owner; PRESERVED | architecture/stewardship cases |
| T21 | D1 observables/models/assumptions/validity/interpretation/adequacy | D1 owner; PRESERVED | D1 scenarios |
| T22 | D2 approximation/error/convergence/conditioning/precision/stochastic semantics | D2 owner; PRESERVED | D2 scenarios |
| T23 | D4 intended-vs-actual behavior; compatibility/persistence/error contracts | D4 owner; PRESERVED | contract/proxy cases |
| T24 | health/Verification/Stabilization sensors; metrics remain sensors | health owner + routes; PRESERVED | long-horizon cases |
| T25 | documentation current/history/source chain/exposition/evidence/background abbreviation | documentation owners; PRESERVED | documentation qualification |
| T26 | language router preserves conditional Python/C++ specialization | language router; PRESERVED | portability/language-profile cases |
| T27 | relation-first tool router preserves specialized tool triggers | tool router; PRESERVED | tool-routing cases |
| T28 | specialized cold doctrine remains reachable without universal activation | concern owners; PRESERVED | package/routing closure |
| T29 | version binding, immutable recovery/profiles, exact fallback, bootstrap/recovery distinction | version owner; PRESERVED | portability/profile cases |
| T30 | parameterized workflow stages/modes/reduced routes/Challenge/evidence/acceptance | workflow prompts; PRESERVED | orchestration/profile cases |
| T31 | generic authority-change template semantics under current terminology | existing template; PRESERVED | template tests |
| T32 | D3->D4 workplan snapshot/delegation/stages/evidence/reopen | implementation template; PRESERVED | workplan scenarios |
| T33 | root/source docs are navigation/derived views, not authority/activation | navigation; PRESERVED | representation tests |
| T34 | 6.x machine profile topology + immutable historical resources | profile owner; PRESERVED | orchestrator/frozen-resource tests |
| T35 | canonical source -> generated dist/profile reproducibility | generators; PRESERVED | build/validate/dist/snapshot |
| T36 | behavioral scenario surface 1-115 remains required | qualification; PRESERVED | replacement 260-decision Stage-F result |
| T37 | documentation cold routes to security/performance/storage/release remain packaged/reachable | documentation root; PRESERVED | route/package tests |
| T38 | current terminology while frozen historical lexemes remain unchanged | current owners + frozen resources; PRESERVED | nomenclature/frozen tests |
| T39 | compatible local/public fallback uses exact validated immutable bootstrap; never default/latest | version owner; PRESERVED | replacement exact-ref bootstrap qualification |

## Protocol 6.3 T40-T120 closure map

`QUALIFICATION_CLOSED` means candidate semantics plus discriminating implementation-context evidence are closed. It does not mean independent Review, recovery, accepted-current state, or Stage G is closed.

| IDs | Target semantic group | Current disposition | Current evidence / remaining gate |
| --- | --- | --- | --- |
| T40-T61 | authority separation through logical canonical memory, evidence/statistics/temperature/HAS/capability/coverage/progressive disclosure/package separation | QUALIFICATION_CLOSED | final candidate `3bbbdfa81206...`; focused Protocol 6.3 counterfactuals; F2 result `6fc26ce374b5...`; rebound static sensors at the same evidence commit |
| T62 | 6.3 bootstrap/profile/recovery/version staging | PARTIAL_STAGE_G | bootstrap `e12572c02108...`, later mapping `e6a8c12f065c...`, candidate `3bbbdfa81206...` qualified; immutable recovery selection/mapping remains Stage G after independent Review |
| T63-T65 | frozen prior resources; source/generated/package parity; static-vs-live claim discipline | QUALIFICATION_CLOSED | fresh F2 assembled gates at `6fc26ce374b5...`; static evidence explicitly makes no live-telemetry claim |
| T66 | Protocol 7 inheritance/current-lifecycle reconciliation | OPEN_STAGE_G | no silent Protocol-7 D3 change; accepted-current/history/authority-index reconciliation remains post-Review/recovery |
| T67 | human-facing background/terminology/abbreviation completeness | QUALIFICATION_CLOSED | inherited documentation/orchestration regression plus full source/package pass |
| T68 | independent assembled-candidate qualification/Review | OPEN_INDEPENDENT_REVIEW | handoff targets `3bbbdfa81206...`; implementation-context 260/260 cannot satisfy independent Review |
| T69 | anti-scope-laundering/lower-salience mandatory preservation | QUALIFICATION_CLOSED | fresh Scope/materiality laundering + Priority inversion Challenge dispositions in F2 evidence |
| T70-T120 | recursive-warrant prevention through watermark/coverage separation, including authority binding, atomic publication, base/overlay, trust, provenance, immutable observation/correction, recurrence lineage, semantic identity, maturity/comparative guidance, salience and HAS-basis rules | QUALIFICATION_CLOSED | current owners + focused executable PEM tests + final assembled regression + exact Q63/F63 accounting in `6fc26ce374b5...` |

The surviving review defects are closed in implementation context: D4R2 binds accepted-repair evidence to the exact repair subject/state/owner rather than chronology; D5R2 derives replication/independence obligations for `PROVEN SUCCESS_PATTERN` rather than trusting claimant flags. D1/D2/D3/D6/D7 remain reverified preserved repairs.


## Source-generation and lifecycle boundary

Completed implementation-side sequence:

```text
canonical 6.3 doctrine/routes/template + PEM validator/tests
 -> reviewed D1-D7 repair state and NO-PASS at 100cbde...
 -> D4R2/D5R2 owner-level false-pass repair
 -> self-reference-safe immutable public bootstrap e12572c02108...
 -> later exact public mapping e6a8c12f065c...
 -> final semantic candidate 3bbbdfa81206...
 -> full source/package/profile/Core/frozen-resource acceptance
 -> final static-sensor recomputation
 -> exact 260-case F2 qualification 6fc26ce374b5...
 -> current independent assembled-candidate Review handoff
```

Still-open lifecycle:

```text
fresh independent assembled-candidate Review of 3bbbdfa81206...
 -> immutable recovery descendant only after Review PASS
 -> later recovery mapping + mapping-bearing regeneration
 -> targeted recovery/profile/package/Core acceptance
 -> lifecycle/history/authority-index/self-hosted accepted-PEM/Protocol-7 reconciliation
 -> workplan archive / separately authorized cutover
```

`PROJECT-ENGINEERING-MEMORY.md` remains project-local PARTIAL candidate-overlay state and is never copied into generic `dist/` packages or protocol profile snapshots.


## Current gate disposition

```text
SERIOUS CHALLENGE: NONE IDENTIFIED IN IMPLEMENTATION-CONTEXT QUALIFICATION
INHERITED T01-T39: RECONSTRUCTED, PRESERVED, AND REQUALIFIED
T40-T61: QUALIFICATION_CLOSED
T62: PARTIAL_STAGE_G — public bootstrap/profile leg closed; recovery leg intentionally open
T63-T65: QUALIFICATION_CLOSED
T66: OPEN_STAGE_G — final Protocol-7/current-lifecycle reconciliation
T67: QUALIFICATION_CLOSED
T68: OPEN_INDEPENDENT_REVIEW
T69-T120: QUALIFICATION_CLOSED
SEMANTIC CANDIDATE: 3bbbdfa8120646d76336c7b916e6a891c9ed38f2
PUBLIC BOOTSTRAP: e12572c021087308570abfa41657a910c6896457
PUBLIC MAPPING DESCENDANT: e6a8c12f065c3d25a41da804c129d6bc0a4f7b50
F2 260-CASE RESULT COMMIT: 6fc26ce374b5346495782871d5d7241de5b90071
INDEPENDENT REVIEW: PENDING
PROTOCOL 6.3 RECOVERY: UNAVAILABLE
ACCEPTED CURRENT PROTOCOL: 6.2.0
WORKPLAN: ACTIVE
MAIN CUTOVER: NOT AUTHORIZED
```


## F3 owner-binding preservation delta

Candidate `026eecf6ce382c3445ed218aeca80dcf2fb9a426` preserves the prior census except where D4R3 deliberately strengthens authority/acceptance concretization. T45/T46/T67/T75-class owner-bearing paths now require accepted-state governing-owner binding; this is a monotonic repair of the reviewed false-pass, not a relaxation. Frozen Protocol 5.16/6.0/6.1/6.2 resources were rechecked by the fresh candidate package/profile/Core gates. Prior F2 labels remain historical evidence; affected authority/recurrence cases are rebound to fresh F3 discriminators and full candidate regression. Independent Review remains open.


## F5 / D9 preservation refresh

Exact repaired semantic candidate: `190c8b4d352c203ef74c94d57c4f18d30eb7186d`. D9 narrows same-ID reconciliation validation and adds reconciliation evidence to the existing material-route health path; it does not alter D1-D3 authority, accepted Protocol 6.2 T01-T39 semantics, cold-route activation topology, frozen 5.16/6.0/6.1/6.2 resources, or package/profile ownership. F2/F3/F4 candidate identities remain historical evidence only. Static activation active sets were mechanically rechecked against this exact candidate with all documented candidate-side byte totals unchanged. Stage G and Protocol 6.3 recovery remain blocked pending fresh independent Review.
