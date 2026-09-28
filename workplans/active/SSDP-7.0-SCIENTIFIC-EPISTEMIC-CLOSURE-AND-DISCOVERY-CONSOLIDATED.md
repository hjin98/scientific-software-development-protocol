---
kind: protocol-major-revision-workplan-consolidated
workplan_id: SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED
protocol_version: 6.6.0
target_protocol_version: 7.0.0
status: proposed
created_date: 2026-09-27
base_protocol: Protocol 6.6
supersedes:
  - SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY
  - SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-1
  - SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-REVISION-2
requires_version_rebind: SSDP-8.0-DETERMINISTIC-ORCHESTRATOR-VERSION-REBIND
design_review_state: revised-after-d255a92-no-pass-pending-independent-review
implementation_handoff: not-authorized
stakeholder_confirmation: section-4 obligation-binding rule accepted 2026-09-27; SC1 claim-integrity floor and SC2 Option B accepted 2026-09-27
active_serious_challenge: none-open-SC1-SC2-dispositioned-by-stakeholder; repairs-pending-independent-review
---

# SSDP 7.0 — Scientific Inspectability, Epistemic Initiative, and the Scientific Feedback Loop — Consolidated Workplan

## 0. Current disposition

This file is the **single current planning handoff** for Protocol 7.0. It supersedes the composition of the parent workplan and Revisions 1-2, which are preserved under `workplans/archive/` as historical design-review evidence. Implementation and Review SHALL reconstruct the contract from this file plus accepted Protocol 6.6 owners, not by replaying the earlier amendment chain.

The workplan ID keeps its historical `EPISTEMIC-CLOSURE` lexeme for traceability. The doctrine is renamed (section 3.1) because "epistemic closure" conflicts with SSDP's use of "closure" to mean *done*, and with the philosophical sense of the term.

```text
GOVERNING BASE: Protocol 6.6.0 (accepted-current; release identities owned by PROTOCOL-RELEASE-STATE.yaml)
TARGET: Protocol 7.0.0
DESIGN REVIEW: NO-PASS on 781786339fd83401f9954e663244bc973b0de968 (findings not durably recorded)
               NO-PASS on c50f2679ad8210632d8acfb1f4e61dfb979fff0c
                 (qualification/ssdp70/WORKPLAN-REVIEW-2026-09-27-PROTOCOL-7.0-C50F267-NO-PASS.md)
               NO-PASS on 88a82b57d4b5c937f5d420280896ed38c9c72ac1
                 (qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-88A82B5-NO-PASS.md)
               NO-PASS on d255a9265aeb6aaf2432193b327beb07b9c4740c
                 (qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-D255A92-NO-PASS.md)
               repair proposed; fresh independent re-review pending
PRIOR AUTHOR-SIDE PASS (qualification/ssdp70/WORKPLAN-REVIEW-2026-09-27-PROTOCOL-7.0-PASS.md):
  applies only to the superseded composition; not independent; confers no readiness on this file
STAKEHOLDER DECISIONS (2026-09-27): section 4 obligation-binding rule ACCEPTED;
  SC1 claim-integrity floor ACCEPTED; SC2 Option B (marked product inspectability surface) SELECTED
  (qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SC1-SC2.md)
D4 IMPLEMENTATION: NOT AUTHORIZED
DETERMINISTIC ORCHESTRATOR: Protocol 8.0 (unchanged by this work)
```

### 0.1 Current repair and Review boundary

The latest independent workplan Review, of `d255a92`, returned **NO-PASS** with no Serious Challenge, three blockers and five material gaps. Its durable record is `qualification/ssdp70/WORKPLAN-REVIEW-PROTOCOL-7.0-D255A92-NO-PASS.md`. At the stakeholder's direction, that reviewing context authored the repairs below; it cannot independently accept them. The accepted §4 decisions remain unchanged.

| `d255a92` finding | Proposed repair |
|---|---|
| B1 §8.3 placement cannot reach run, analysis-review and gate-evidence tasks, because selection happens on frontmatter | §8.3 freezes selection-surface coverage through existing role descriptions and drops "always-loaded"; §11.3 adds ordinary-entry cases for these task classes with selection counted; §14 reopen |
| B2 6.6 interval unreconciled and undispositioned in the PEM basis/HAS | §0.2 rebinds `accepted_pem` to the accepted publication, records the stale front matter, performs bounded 6.6 intake with dispositions, and routes the missing 6.6 closeout-learning assessment |
| B3 tension retrieval lost across authority revision or ambiguous owner | §6.4 re-derives one retrieval-key invariant: lineage identity for persistence and search, applicability across revisions, reconciliation at D1/D2 revision; §11.3 revision-drift case |
| G1 out-of-list results decision-inert | §11.5 requires unnamed decision-critical properties, an unnamed-class floor and non-inferiority, and limits generalization claims |
| G2 inaccessible tension home: qualify versus block undefined | §6.4 inaccessible-home rule; §11.3 freezes both dispositions |
| G3 §6.5 retrieval over-claim for non-authority findings | §6.5 subject-identity key; retrieval sits in the §6.3 envelope, with no new mandatory search |
| G4 persisting side of discoverability unqualified | §11.3 chained persist-then-retrieve episode |
| G5 touched 6.6 capabilities lack preservation route | Stage A 6.6 capability-preservation map; §11.4 active-protocol, catalog and selection measures; §11.5 preservation floors |
| Minor: D3 location pointer; harness-oracle integrity | §6.4 limited to D1/D2; §11.5 known-broken oracle check through the actual harness (I66-4) |

Earlier findings (`88a82b5` B1/B2/G1, `c50f267`) and the stakeholder's SC1/SC2 dispositions remain in their Review and decision records; their repair maps are recoverable at `d255a92` §0.1 and `88a82b5` §0.1. The `781786339` Review left no durable finding record; its surviving summaries remain claims only. No historical Review is acceptance of the current repair.

The tension-discovery route has now drawn three related findings (`c50f267` B5, `88a82b5` B1, `d255a92` B3). Following the convergence owner, the repair replaces the accumulated clauses with a single retrieval invariant (§6.4) rather than adding another; a further finding there should question that mechanism, not patch it.

Remaining boundary: fresh independent workplan-level acceptance is required before implementation authorization. The tests and human trial specified below are future implementation qualification, not evidence already executed by this planning repair.

### 0.2 Project-memory basis and capability transfer

PEM activates for this mature protocol successor's routing, qualification and publication changes. Project policy designates `main` as the integrated publication line; this cycle binds its exact state below rather than following a moving branch. Repository identities below are in `hjin98/scientific-software-development-protocol`.

```yaml
pem_basis:
  accepted_project_state: 2585b73f00420daca185a4fbb9ac42a79473eda1
  accepted_pem: "hjin98/scientific-software-development-protocol@2585b73f00420daca185a4fbb9ac42a79473eda1:PROJECT-ENGINEERING-MEMORY.md"
  candidate_overlay_semantic_candidate: NONE
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: Premature immutable publication can omit required repaired routes; Stages F-H freeze, review and ratify before descendant publication and exact-ref verification. Bounded 6.6 intake found no further occurrence (public source equals the reviewed semantic candidate).
  - id: SP-002
    disposition: APPLICABLE
    reason: Stages F-H preserve distinct semantic candidate, descendant public-source mapping and later recovery publication; exact-ref acceptance checks the resulting chain. The 6.5 and 6.6 releases are unrecorded supporting applications (intake I66-6).
  - id: PC-001
    disposition: APPLICABLE
    reason: The accepted 6.6 versioning owner independently requires frozen historical resources; Stage E freezes 6.6 before new generation and Stages F/H verify preservation.
  - id: SP-001
    disposition: APPLICABLE
    reason: Stages B-D repair canonical owners and routing, including selection-visible descriptions; Stage E regenerates descendants; Stage F checks package closure/parity and live activation.
  - id: DS-001
    disposition: APPLICABLE
    reason: Section 11 separates live outcome evidence from structural checks and requires harness-level oracle discrimination; Stage G independently reviews assembled semantic adequacy, including the qualification oracle. The 6.6 cycle supplied further unrecorded applications (intake I66-1, I66-4).
```

**Basis identity and stale metadata.** The accepted publication is the PEM in the designated integrated state `2585b73f`. Its blob `1561797125622f355f84eb27319f87e8fa4227d9` is identical in reviewed/ratified 6.6 candidate `22f4bdba` and on this branch; schema validation passes for five families and no notices. The file's front matter is stale, though: it still names 6.5 state `23e46543` as `accepted_base.project_state` and `reconciled_through`, carries a 6.6 candidate-overlay string, and its coverage basis stops at 6.5. This plan does not read that text as a current overlay or as reconciled coverage. The 6.6 interval `23e46543..2585b73f` is **not** reconciled memory, and the 6.6 closeout (`2818ccf`) records no closeout-learning assessment, although `qualification/ssdp66/STAGE-F-G-EVALUATION-AND-QUALIFICATION.md` §9 deferred three candidates to it. Coverage is **PARTIAL**. The dispositions use canonical family metadata, not temperature or summary inclusion.

**Bounded 6.6 intake** (evidence-only design inputs; not PEM entries, not admitted, no memory mutation). Scope: the routing, qualification and publication surfaces this plan changes, read from `qualification/ssdp66/` stage, freeze and correction records and the 6.6 `history/SEMANTIC_EVOLUTION.md` entries. Admission of any item stays `REVIEW_REQUIRED` for the owning closeout-learning process.

| ID | Observed in 6.6 (bounded to Claude Code headless / `claude-sonnet-5`) | Applicability here | Route in this plan |
|---|---|---|---|
| I66-1 | On ordinary routes, agents consumed only the invoked `SKILL.md`; declared mandatory reads of other owners were not honored, and stronger imperative wording did not change that | APPLICABLE | §8.3: the consumed entrypoint clause must carry the minimum obligation; §11.4 records owner reads; a pass cannot rest on a declared-but-unread owner |
| I66-2 | Selection happens on catalog frontmatter; an unselected body is never consumed; selection-visible changes make the selection differential applicable | APPLICABLE | §8.3 selection-surface decision; §11.3 ordinary-entry cases with selection counted; §11.5 selection floor |
| I66-3 | Inlining broad doctrine into every entrypoint raised ordinary-route active protocol bytes (+18%) and failed the burden rule; important doctrine is not doctrine that must always be active | APPLICABLE | §8.3 keeps entrypoint additions compact; §11.5 fixed-cost bound on predicate-excluded routes |
| I66-4 | Harness/oracle defects: hidden oracle tests never collected; assessor did not see new files; a rubric branch passed self-adoption; an ordering oracle was weaker than its claim; designed termination misclassified | APPLICABLE | §11.5 known-broken oracle check through the actual harness and full-deliverable assessor input before candidate runs |
| I66-5 | User-level installed skills duplicated SSDP entries in the session catalog, confounding arms | APPLICABLE | §11.2 arm isolation recorded and verified per run |
| I66-6 | 6.5 and 6.6 releases followed candidate → descendant public mapping → distinct recovery | APPLICABLE | SP-002 above; supporting only |

**Capability transfer.** PC-001's current mandatory force comes from accepted 6.6 `source/shared/references/protocol-versioning-and-compatibility.md`, "Capability preservation across versions" and "Orchestration profiles", resolved through release state; the other entries and the intake remain evidence-only. The HAS reasons and intake routes are the bounded capability-transfer map for learned capabilities. Accepted 6.6 capabilities that Protocol 7 touches but PEM does not record receive their own preservation map in Stage A (§12). Neither map preserves obsolete mechanisms or asserts that checks already passed.

**Routing and refresh.** No PEM mutation is part of this repair. The missing 6.6 closeout-learning assessment and front-matter reconciliation belong to the repository lifecycle/PEM governance owner. Stage A requests them there. This cycle does not depend on them being completed: the intake above is sufficient for its decisions. If the accepted memory basis, overlay or an applicable owner changes, inspect the affected interval and refresh dispositions through the owning process before dependent closure; do not silently rebind this cycle to moving `main`.

## 1. Objective, protected outcome, and major-version boundary

Protocol 7.0 SHALL make the **scientific feedback loop** a first-class SSDP objective alongside task fidelity, semantic authority, evidence integrity, and engineering robustness:

```text
question / hypothesis -> D1 -> D2 -> D3 -> D4 / execution
 -> realized scientific record (data, states, trajectories, decisions)
 -> human-inspectable projection
 -> bounded active search for anomaly / tension / opportunity
 -> human scientific judgment
 -> persisted next question / Challenge / revised method -> ...
```

**Protected outcome.**

> When scientific work is delegated to software or AI, the scientist keeps the ability to see what actually happened, to judge the evidential weight of the result, and to notice and pursue what the delegated work encountered. This holds without source-code or storage archaeology and without depending on one AI's framing. Neither data nor AI interpretation acquires scientific authority, and the protocol neither mandates unrequested product features nor buries the human in noise.

This is a major revision (versioning owner: incompatible governing-doctrine change). It changes what counts as an adequately inspectable scientific computation, what agents must notice and report, and what human gates must receive. It creates no D5 layer.

## 2. Motivating defect

A program can implement a well-specified D1/D2 method faithfully, retain enough hashes, state, logs, and provenance to reconstruct everything, and pass qualification. Its scientist may still have to reverse-engineer code or storage, or hand the state directory to an AI, to learn basic material facts. Examples: which checkpoint was selected and why, error versus epoch, exclusions, per-population error, decision margins, outliers, and the candidates compared.

**Recoverability is not accessibility.**

The deeper failure is epistemic. When only the requested terminal result returns to the human, the discovery opportunities met inside the delegated work leave the human's field of view. The more work is automated, the worse this gets, unless inspectability and initiative grow with delegation. That includes disclosure of the search the AI itself performed.

## 3. Terminology and ownership map

### 3.1 Protocol 7 terms (defined once, in the new owner)

- **Realized scientific record (RSR).** Retained information about what a real scientific execution did: realized states, transformations, trajectories, decisions, exclusions, failures, and results, at the granularity its scientific interpretation needs.
  - RSR and evidence-owner **observations** can overlap: a result produced by an evidence realization is already an observation, whether or not assessed, and may be retained in the RSR. Other RSR items are execution records, not automatically evidence observations. Later assessment interprets observations; it does not create their existence or rewrite their historical identity. The evidence owner governs this mapping and any later use of retained records in a new evidence realization.
  - It is *not* a D1 **observable**, which is a quantity the science defines. The RSR holds realized values of observables and more.
- **Scientific inspectability.** The material RSR is retained and projected so that the **intended reader** (section 4.3) can answer **routine scientific questions** (section 4.3) without source/storage archaeology or bespoke extraction. Drill-down reaches exact provenance through every delegated layer (AI, software, pipeline, model, report). This one term replaces the earlier separate concepts of observability, legibility, transitive transparency, and progressive disclosure.
- **Epistemic initiative.** The bounded obligation to search realized evidence beyond the literal completion criterion and surface supported, material findings. It replaces the separate term "discovery pressure."
- **Decision-sufficient gate evidence.** Evidence given to a human gate that is adequate for the judgment the gate assigns (section 6.6).
- **Scientific feedback persistence.** The minimum decision-sufficient state that lets a material finding or human redirection survive the transient conversation or run (section 6.5).
- **Product inspectability surface.** The marked part of O1 content stating which routine questions the product itself must support through retention, projection or exposure (section 4.1(ii)).
- **Claim-integrity floor.** The always-binding limit on agent-authored assertions in any authorized deliverable (section 4.5).
- **Boundaries** (constraints, not concepts): evidence is not authority; no manufactured novelty; exploratory is not confirmatory.

New prose uses "RSR" or "realized record" for generic run data, rather than bare "observability" or an overloaded "observation". Where an item is an evidence observation, that existing term remains correct; the representation does not change its evidence lifecycle.

### 3.2 Ownership map against Protocol 6.6

Each row states whether the new owner **DEFINES** the concept, an existing owner **REFINES** its own concept (a local delta in that owner), or the new owner only **ROUTES** to it. Implementation SHALL NOT create a second definition for any REFINES or ROUTES row.

| Concept | Owner after Protocol 7 | Disposition |
|---|---|---|
| RSR; scientific inspectability; epistemic initiative; channels; obligation binding; product inspectability surface; claim-integrity floor; projection faithfulness/lineage; scientific presentation of decision provenance; agent variant-search disclosure; coverage envelope; retention boundaries principle | new owner (§8.1) | DEFINES |
| Evidence specification/realization/observation/assessment; applicability; common-mode | evidence owner | ROUTES. REFINES only with the RSR/observation overlap mapping in §3.1; observation existence remains realization-based, independent of assessment |
| `finding CHALLENGES -> target` relation | evidence owner | REFINES: inquiry status (exploratory/confirmatory) distinct from evidence strength and Challenge disposition (§6.4) |
| Anti-suppression of contradictory evidence; bounded coverage search (`evidence-evolution-and-dependencies.md`, "Do not suppress contradictory…") | evidence owner | ROUTES. The new owner applies the principle to human-facing RSR projections only |
| Observation / association / causal attribution distinction; claim strength | evidence owner | ROUTES. The §4.5 claim-integrity floor applies existing claim-strength rules to agent-authored deliverables; it defines no new strength scale |
| Claim-role distinctions (definition, hypothesis, observation, …) (`scientific-technical-writing.md`) | writing owner | REFINES: adds recommendation/next probe and authority Challenge to reporting roles; no new taxonomy |
| Semantic/epistemic roles; definition versus warrant (`semantic-definition-and-traceability.md`) | semantic-definition owner | ROUTES. Writing's reporting roles specialize the existing non-exclusive, extensible distinctions, never replace them |
| Resolved value/default/automatic-policy provenance (`configuration-and-policy.md`) | configuration owner | ROUTES. §6.2 reuses effective values, origin and rationale; the new owner requires their scientific presentation when bound, with actor and authority status separate |
| Report/projection oracle integrity, real-owner and common-mode qualification (`testing-and-validation.md`) | testing owner, with evidence owner for independence | ROUTES. §6.1.5 applies these rules to source-to-rendered values; accounting or export is not a new sufficiency oracle |
| D1 observables, validity, external adequacy | D1 owner | REFINES: authoring obligation O1 (§4, §7) |
| D2 trajectories, error, failure/fallback | D2 owner | REFINES: authoring obligation O1 (§4, §7) |
| Persistence/retention architecture | architecture owner | REFINES: D3 consequence of §6.1.7–6.1.8, including marking the product inspectability surface (§4.1(ii)) in D3 authority |
| Artifact retention/eviction/cleanup, schema/version and destructive migration (`storage-and-io.md`) | storage owner | ROUTES. §6.1.8 adds only the scientific-judgment weighing before irreversible loss; §6.1.9 semantic stability routes artifact format/version mechanics here |
| Data-exposure, sensitive-data and trust boundaries (`security-and-trust-boundaries.md`) | security owner | ROUTES. §6.1.13 and the initiative pass's handling of sensitive realized data defer to it |
| Progress/ETA and long-run observational reporting (`concurrency-and-orchestration.md`, `performance-and-parallelism.md`) | concurrency/performance owners | ROUTES. §6.1.12 adds only scientific interim visibility; progress mechanics stay there |
| Authority lifecycle states; ratification orthogonality (`workflow-and-workplans.md`) | workflow owner | ROUTES. New prose uses "proposed/unaccepted" for choices lacking acceptance and reserves `risk-accepted/provisional` for its workflow meaning |
| Protocol-version ratification and publication (`protocol-versioning-and-compatibility.md`) | versioning owner | ROUTES. §11.6's decision-sufficient ratification package applies the Channel C contract to that existing gate without changing its sequence |
| Provenance and reproducibility list (`scientific-software.md`) | scientific-software | ROUTES. Projection lineage (§6.1.5) is new-owner content; the provenance list is unchanged |
| Lossless Representation Rule (kernel) | kernel | UNCHANGED. It already governs Channel A agent reports and handoffs. The new owner's product-report guidance (Channel B) references the LRR's attention ordering and does not extend or re-own it |
| Out-of-matrix adequacy pass; Review | workflow owner | REFINES: adds the reverse data→authority question (§6.4) |
| Human gates; ratification | workflow owner | REFINES: Channel C gate-evidence contract (§6.6) lives here |
| "Do not manufacture … report schemas" (`documentation-and-evidence.md`) | documentation owner | PRESERVED. The §6.1.9 semantic-stability rule requires no schema artifacts; a schema exists only where a D4 consumer contract needs one |
| PEM discovery/learning admission | PEM owners | UNCHANGED. Run findings are not PEM (§6.5) |
| Pre-routing safety kernel | kernel | UNCHANGED (§8.3) |

If implementation finds a further overlap, it adds a row here through the owning acceptance process rather than creating parallel text.

## 4. Obligation-binding rule

Protocol 7 distinguishes the following three binding modes plus one always-binding floor on agent-authored assertions (§4.5). Channel C uses the existing workflow gate authority; it is not a fourth route to product obligations. The stakeholder accepted this rule on 2026-09-27, including the SC1 floor and the SC2 marked-surface split (`qualification/ssdp70/STAKEHOLDER-DECISION-2026-09-27-PROTOCOL-7.0-SC1-SC2.md`).

### 4.1 O1 — authoring obligation (protocol-direct, mandatory when the §8.2 predicate fires)

When D1, D2, or D3 authority for software that produces scientific results is authored or materially revised, the author SHALL state, proportionately:

- **(i) Scientific inspectability need** (always required):
  - the material RSR: realized quantities, populations/regimes, trajectories, decisions, exclusions/failures, and retention/destructive boundaries;
  - the **intended reader**;
  - the **routine scientific questions** the intended reader needs answered.
- **(ii) Product inspectability surface** (marked): which of those questions the product itself must support by retaining, projecting or exposing RSR. Each item is visibly marked as a product inspectability surface in the authority and records whether it lies within the requested deliverable. "Answered through agent reports only" and "None" are valid answers.

"None material, because …" is a valid, reviewable answer for (i). O1 content becomes binding on descendants only when that authority is accepted through its normal process, human-gated where D1/D2 policy requires it. A marked (ii) item additionally binds only as §4.3(a) states. Inspectability-driven product requirements left unmarked inside authority text are an O1 defect, not a way around the mark.

### 4.2 O2 — surfacing obligation (protocol-direct, mandatory for agents when the §8.2 predicate fires)

Perform the bounded inquiry in §6.3 within authorized resources and report material scientific findings and inspectability gaps: missing, irrecoverable, archaeology-only, or misleading RSR. O2 is a surfacing obligation: it **never** expands mutation authority and never obliges the agent to build anything.

### 4.3 O3 — product obligation (never protocol-direct)

A requirement that a product retain, project, or expose scientific information arises **only** from:

- (a) accepted project D1-D4 authority, including accepted O1 content. A marked product inspectability surface (§4.1(ii)) that goes beyond the requested deliverable binds only after acceptance by the owner of product scope (the stakeholder or task authority); technical D3 Review alone does not accept it. An applicable D1/D2 human gate satisfies this when it considers the marked surface. Until accepted, the item remains proposed while the rest of the authority may proceed;
- (b) an explicit stakeholder/task instruction;
- (c) an existing external or product contract.

Protocol 7 doctrine alone never mandates building a report, dashboard, inspection surface, or retention mechanism. The 6.6 kernel rule against inferring unrequested enhancement is **preserved, not superseded**.

**Default when no authority exists.** When an agent builds or changes a scientific pipeline, analysis, or report without O1 content:

- it SHALL record its **materiality choices** in its Channel A report as a visible, unaccepted default: what it retained and projected, and what it deliberately did not. When the change leaves retention and projection unchanged, "no retention/projection change" is the complete statement;
- these choices are an agent-chosen consequential curation decision (§6.2.1) that the human may amend;
- a human-facing report the agent builds within authorized scope is governed by the §4.5 floor, not by an added disclosure section;
- it proposes (O2), rather than silently builds, any inspectability capability beyond its task.

The same default defines the intended reader and routine questions: the stakeholder or accepted authority states them; otherwise the agent proposes them visibly. For run/review-only work without O1 content, the agent likewise identifies its provisional reader, questions and materiality basis for O2 judgment; that reporting basis neither amends authority nor requires retrofitting the product. Materiality uses the 6.6 kernel's grounded decision-changing-path definition, not a new scientific threshold.

### 4.4 Binding across all doctrine and channels

Every requirement in §§5–13 is interpreted through this rule, including provenance, persistence, verification and acceptance language:

- O1 governs authority authoring, with descendant force only after owning acceptance and, for marked surfaces beyond the requested deliverable, product-scope acceptance.
- O2 governs bounded agent inquiry and Channel A reporting. Channel C evidence is prepared within the independently authorized governance task. Neither channel authorizes product mutation, additional shared-resource use, or a write to an otherwise unauthorized artifact.
- Channel B retention, computation, report content, exports and inspection interfaces bind **only through O3**, even when an AI writes the code, analysis or report. An agent-authored product is still a product. A narrow report repair does not authorize adding provenance storage or an export interface solely to satisfy this doctrine.
- The §4.5 floor binds agent-authored assertions in every channel. It limits what the agent claims; it never adds capability, so it is not an O3 path.
- A communication containing both task/gate reporting and a product artifact keeps those functions distinct. The agent reports gaps, unavailable evidence and provisional materiality choices in the authorized communication; it does not make the product comply by silently expanding the deliverable.
- An unbound product gap is an O2 finding/proposal, not automatically a product defect or a blocker to an otherwise adequate engineering task. A §4.5 violation is a defect in the agent's deliverable regardless of O3. A gap that defeats an independently required scientific judgment remains a blocker to **that judgment**, under existing evidence/workflow authority. Report it without inventing mutation authority.

These bindings apply irrespective of imperative wording or authorship. No later SHALL, acceptance checklist, or delegated subagent instruction creates an additional product-authorization path.

### 4.5 Claim-integrity floor (always binding on agent-authored assertions)

An agent-authored assertion in any authorized deliverable — Channel A report, Channel C evidence, or Channel B content such as a report, figure caption, summary or analysis output the agent writes — SHALL NOT be stronger than its evidence. In particular it does not:

- present a selected, searched-for or post hoc result as confirmatory or pre-specified (§6.2.2, §6.3.7);
- state a conclusion unqualified when a known material anomaly, exclusion, coverage limit or unresolved finding could change it;
- launder interpretation or hypothesis into measured fact (§6.3.8).

The floor applies the evidence owner's existing claim-strength rules. The agent satisfies it by qualifying, narrowing or withholding the claim inside the authorized scope; disclosure is one admissible means, not a required section. The floor never obliges retention, projection, export or any new capability. It governs only what the agent itself asserts, not pre-existing content it did not author or change.

## 5. Three channels

| Channel | From → to | Semantic owner of the obligation | Obligation kind |
|---|---|---|---|
| **A. Task report** | agent → its delegator (a human, or a delegating agent that reports onward) | new owner (content) + kernel LRR (representation) | O2, §6.2.2 disclosure, §4.5 floor |
| **B. Product inspection surface** | scientific software → end-user scientist | project D1-D4 authority | O3 only (O1 at authoring time); §4.5 floor on agent-authored content |
| **C. Governance gate** | SSDP human gate → ratifier/adjudicator | workflow owner | gate-evidence contract (§6.6); §4.5 floor |

The delegating human, the end-user scientist, and the ratifier may be the same person or different people. Obligations attach to the channel, not the person. A delegated agent's Channel A report to a delegating agent is an intermediate hop; §6.3.11 governs what must survive to the human.

## 6. Doctrine

The named principles and imperative requirements below are normative within their stated predicates and §4.4 binding; SHALL emphasizes force rather than being its sole marker. Lists introduced as examples or illustrations are non-exhaustive options, not required report sections. Preferences ("prefer", "where cheap") remain preferences under §10. Channel A/C communication must truthfully expose available evidence and its limits, and every agent-authored assertion obeys §4.5; inability to produce a desired projection triggers the applicable insufficiency disposition, never an implied product-building obligation.

### 6.1 Scientific inspectability

1. **Authority-to-record route.** For each scientifically material D1/D2 object or process whose realized behavior can affect trust, interpretation, acceptance, or later reasoning, there is a proportionate route: governing meaning → executable realization → retained RSR → human-inspectable projection → exact drill-down/provenance. Not every internal variable is material.
2. **Recoverability is not accessibility.** Bytes somewhere in a database, log, hash chain, checkpoint, or source tree do not satisfy inspectability if a routine scientific question needs reverse engineering. Progressive disclosure applies: orientation → high-information summary → material anomalies, uncertainty and decisions → trajectories, distributions and comparisons → drill-down → raw/provenance. An undifferentiated dump fails just as opacity does. No single giant report, universal dashboard, or full raw duplication is required.
3. **Meaning preservation.** Reported quantities keep the context needed to interpret them: definition, unit, population/denominator, normalization, aggregation, uncertainty semantics, model/checkpoint/regime identity. Where an absolute value is uninterpretable alone, route to the relevant comparator. That includes the trivial/null baseline when a metric could be trivially satisfied (§6.3.4). Human-readable semantic identity leads; opaque hashes stay available but subordinate.
4. **Coverage envelope and selection.** Summaries SHALL make recoverable, where selection could change interpretation:
   - the denominator;
   - included, excluded, missing, and failed counts;
   - the selection/filtering rule;
   - whether a view is complete, sampled, top-k, or thresholded;
   - material subgroup/tail behavior;
   - **which stratification axes were examined, and why those.** The choice of axes is itself a selection. It is anchored to O1/stakeholder content where that exists, and otherwise disclosed as agent-chosen.

   A projection is defective if a competent reader would reach a materially different conclusion after learning a selection fact the system possessed and should have exposed.
5. **Faithful projection, lineage, and accounting.**
   - Human-facing values are deterministic projections of canonical RSR, never independently edited or per-query regenerated truth.
   - A derived analysis that affects interpretation keeps enough lineage to reconstruct it: source set, filtering, transformation, statistic, uncertainty computation, parameters/regime, and analysis software identity when nontrivial.
   - Report-producing code is D4 and is verified at the real source-to-rendered-value boundary under the testing owner. Prefer cheap **accounting identities** where they discriminate the property, e.g. source N = included + excluded + failed + missing. Counts alone cannot prove correct identity joins, normalization, units or uncertainty. For material judgments use an independently justified bounded source/reference or metamorphic check of those transformations; a swapped-identity or wrong-normalization projection must not pass solely because counts balance.
   - A value that cannot be faithfully obtained is marked unavailable, never reconstructed by guess.
6. **Non-narrative and tool-independent routes.**
   - AI prose is a presentation layer, never the sole interface. For material judgments there is a direct route from any AI summary to non-narrative evidence: tables, plots, individual cases, and canonical records, produced by deterministic projection. An AI that computes tables per query is still AI-mediated.
   - Where consequence warrants and it is feasible, at least one route SHALL let the scientist inspect the material RSR **without the project's code or an AI**, e.g. an existing export in a standard self-describing format. Such a route reduces tool dependence; it does not prove semantic independence or correctness when the same defective transformation produced the export and report. Use the evidence/testing owners' common-mode and oracle rules, and verify intended-reader interpretation. Missing routes are handled through §4.4, not built without O3.
7. **Bounded open interrogation.** For substantial processes, the front door makes discoverable which scientific RSR exists, what it means, what it covers, how to inspect or export it, and what potentially material information was not retained. The scientist can pose unanticipated but reasonable questions over retained RSR without private-schema knowledge. The production application is not required to support arbitrary computation.
8. **Retention, granularity, and destructive boundaries.**
   - Before material raw or intermediate state is irreversibly discarded, aggregated, overwritten, or transformed beyond recovery, the owning design weighs what later judgment needs.
   - When cheap relative to its value, prefer retaining **per-unit results with stable identity keys** (per sample/item/configuration) that join to source metadata. Aggregates can be rebuilt from units, never the reverse, and the keys enable cross-run comparison.
   - Retention decided at design time is biased towards anticipated questions. Per-unit retention is the main cheap hedge for discovery.
   - When full retention is unjustified, keep a sufficient disclosed substitute: distributions, extrema/outliers, decision inputs and margins, checkpointed trajectories, or an explicitly sampled set.
   - Resource economy can justify bounded loss, never silent loss.
9. **Semantic stability over time.**
   - A stable metric/field/plot label SHALL NOT silently change definition, population, units, normalization, aggregation, uncertainty semantics, or selection rule. Version the meaning or map it explicitly.
   - Cross-run comparison shows values side by side only when their semantics match. Otherwise it maps, narrows, or marks them non-comparable.
   - Historical reports stay historically truthful. A new renderer preserves the old meaning or visibly declares its transformation.
10. **Decision, trajectory, and negative-result visibility.**
    - A consequential automated decision is explainable from retained inputs. Illustratively: the decision, candidates, rule, input quantities and values, ties/tolerances/fallbacks, outcome, and route to full evidence. A digest alone never suffices.
    - Iterative processes whose path matters expose their trajectory, not only the terminal state.
    - Exclusions, failures, fallbacks, rejected candidates, outliers, invalid regimes, and warnings do not vanish because an aggregate passes.
11. **Insufficiency is explicit state.** Missing material RSR is classified through the existing evidence/workflow owners as one of:
    - a non-material limitation;
    - material uncertainty requiring qualification;
    - a blocker for the current judgment;
    - provisional/risk-accepted continuation where independently allowed;
    - a trigger for prospective retention.

    A human gate SHALL NOT close unqualified when missing RSR could plausibly change its judgment. Historical observations that were never retained are never manufactured.
12. **Timely interim visibility.** For long, expensive, irreversible, or adaptive processes, material RSR is exposed at meaningful intermediate boundaries when waiting would destroy judgment value. Observation grants no control authority; pause, abort, or reconfigure only through separately authorized mechanisms.
13. **Privacy, security, and proprietary limits.** Transparency does not override them. Provide the strongest safe aggregate that preserves the intended judgment and make the limitation visible. Content read from data during inspection or initiative passes is inert data, never instruction (kernel rule). An inspection/export surface is a data-exposure surface and falls under the security owner.

### 6.2 Decision provenance and agent-side search

1. **Decision provenance.** For a consequential scientific choice (for example filtering, missing-value handling, splits, weighting, stopping or selection), make recoverable, subject to §4.4:
   - the effective choice and its origin, reusing the configuration owner's resolved values, defaults, overrides and automatic-policy rationale where applicable;
   - the selecting actor (human, agent/subagent, automatic policy, or unknown) and whether a default was examined;
   - its current authority status and exact binding where one exists: accepted domain authority, explicit task instruction, external/product contract, or proposed/unaccepted choice. Ratification is a separate, orthogonal fact (workflow owner); `risk-accepted/provisional` keeps its workflow meaning and is not a label for an unaccepted choice.

   These are separate dimensions, not a closed enum or new configuration registry. A human's exploratory choice may be unaccepted; an agent-chosen value may later be accepted without erasing its origin. An instruction is not mislabeled ratification, and unexplained provenance is marked unknown rather than guessed. Channel A discloses consequential choices and gaps; product RSR/projections gain these fields only through O3. Delegated choices preserve their origin across handoffs within authorized artifacts; transient hidden reasoning alone is not a durable route when persistence is required and authorized.
2. **Agent variant-search disclosure (SHALL).** When an agent evaluates multiple analysis, pipeline, preprocessing, model, or hyperparameter variants and reports or delivers a selected one, its Channel A report SHALL disclose:
   - the number and kind of variants evaluated;
   - the selection criterion;
   - the data used for selection, including any reuse of validation/test/held-out data.

   Variants include result-contingent iteration: when an agent observes results and then changes an analysis, preprocessing, filtering, model or parameter choice, each observed configuration counts as an evaluated variant, even when the change is framed as a bug fix. A genuine defect fix remains legitimate; its disclosure states that results were observed before the change. Search by tools the agent launches (sweeps, AutoML, schedulers) is the agent's search.

   Disclosure covers the selection lineage that produced the delivered survivor, including delegated and resumed work. Preserve that information in authorized handoffs; reconcile overlapping trials rather than adding duplicate local counts. If earlier search history is unavailable, state the known lower bound and unknown interval and limit the claim accordingly. Do not present a local count as the whole search.

   Selection over variants using data that later supports the reported result is a selection effect and falls under §6.3.7. Any deliverable the agent authors, including a product report, obeys §4.5: it does not present the survivor as pre-specified or its selection-set performance as an unbiased estimate, even when the delivered pipeline is otherwise fully inspectable. The agent meets this by qualifying or narrowing the claim; a disclosure section in the product is required only through O3.

### 6.3 Epistemic initiative

1. **Scope.** Fires by the §8.2 predicate. Task scope bounds what an agent may mutate, not what it may notice. Material out-of-scope findings are surfaced (O2) with a recommendation for follow-up, investigation, or Challenge. The agent never silently expands scope.
2. **Bounded search envelope.** Inspect the most information-rich and decision-sensitive views first: residuals, distributions, trajectories, subgroups, decision margins, and comparisons where applicable. Exhaustive mining is not required. Stop when further search has low plausible information value relative to cost, or would become a new research task needing explicit scope.
   - Cheap read-only probes within the task's declared resource budget are permitted. When no budget is declared, only probes whose cost is negligible relative to the task and that use no shared, metered or queued resource are permitted.
   - Probes that consume material shared compute, time, or cost beyond that are proposed, not run.
   - Probes over sensitive data follow §6.1.13 and the security owner; the report carries the strongest safe aggregate.
3. **Expectation record.** Before a consequential run or analysis, and where cheap, the owning authority or the agent records the expected outcomes: ranges, trends, invariants, and the comparator. An anomaly is a deviation from a stated expectation. When none was stated, findings are labeled post hoc. Expectations do not constrain what may be reported.
4. **Finding classes.** Findings that challenge an assumption or interpretation; unexpected regimes; consequential anomalies; missing visibility; structured residuals; sensitivity/instability/near-boundary decisions; high-value new questions. Also **results that are implausibly good relative to the expectation or the trivial baseline**, which suggest leakage, contamination, or a trivially satisfied metric.
5. **Finding shape and noise control.**
   - Each surfaced finding states: observation → interpretation/hypothesis (labeled) → why it matters → the cheapest check that would settle it → what changes if it holds.
   - Summaries lead with the few findings most likely to change interpretation or the next action, and keep routes to the rest.
   - Dispositions of surfaced findings (confirmed, dismissed, and why) are persisted under §6.5 when a recurring process makes them useful for recalibrating the threshold.
6. **Null result with coverage.** When a realized-data inquiry is owed — the task produced, ran or reviewed realized scientific results, or prepares gate evidence — "no material unexpected finding" is valid only with its search envelope: what was examined, and material areas not examined. A null without coverage is boilerplate and non-compliant. A change-only task that realizes no scientific results owes no null; it surfaces §6.3.9 concerns when they exist and otherwise adds nothing. A proportionate envelope may be one line.
7. **No manufactured novelty; exploratory is not confirmatory.**
   - No quota of findings exists.
   - A pattern found by searching data, or by an agent's variant search (§6.2.2), is an exploratory observation. It may motivate a hypothesis, Challenge, or follow-up, but it is not independent confirmation of the hypothesis it generated.
   - D1/D2 account proportionately for data-dependent selection, population reuse, search breadth, leakage, and common-mode dependence. This is claim-strength alignment, not mandatory multiple-testing machinery.
8. **Reporting roles.** Channel A/B reporting distinguishes, where material: direct observation, derived analysis, interpretation, hypothesis, recommendation/next probe, and authority Challenge (writing owner, REFINES). No presentation launders interpretation into measured fact. For Channel A this is O2 reporting; for agent-authored Channel B content it is the §4.5 floor, satisfied without adding product sections.
9. **Engineering tasks.** An engineering agent (pipeline, training orchestration, evaluation/reporting code, numerical backend, persistence/retention, publication tooling) that notices a change would make material RSR unobservable or misleading surfaces it as a design concern (O2), even if its coding task otherwise passes.
10. **AI as consumer.** An agent consuming a scientific program prefers its supported inspection interfaces over reverse engineering. Repeated bespoke extraction, by an AI **or a human**, for a routine question is reported as an inspectability defect ("question debt").
11. **Delegated findings.** A delegated agent whose work fires the predicate reports its material findings, variant-search disclosure and null envelope to its delegator. A delegating agent carries into its own Channel A report every material finding from its delegates, including findings beyond its own task scope, or an explicit route to them; it may rank and condense but not drop them. The LRR's governed scope does not license dropping an out-of-scope material finding surfaced under O2.

### 6.4 Data → authority feedback

- Data are evidence, not authority. No observation, plot, anomaly, or AI interpretation self-amends D1/D2.
- **Tension accumulation.** A finding that bears on accepted D1/D2 but does not meet the Serious Challenge threshold is recorded, when authorized under §6.5, with the evidence owner's `CHALLENGES` relation to the authority it concerns, bound by the lineage identity below, and its current non-blocking disposition. Record exploratory/confirmatory inquiry status separately from evidence strength, applicability and Challenge disposition. A single exploratory counterexample can already warrant Serious Challenge; a confirmatory label establishes neither strength nor independence.
- **Tension retrieval invariant.** Persistence and search use one key: the **lineage identity** of the authority, meaning its stable logical identity (the evidence owner's stable logical endpoint identity) plus the exact revision and claim/locator the finding examined.
  - *Home.* A tension's canonical home is an evidence record or native issue, never the accepted authority text; writing a tension into accepted authority is an authority mutation and follows its acceptance process. The home carries the lineage identity in searchable content or native metadata. When the challenged owner is uncertain (a D4 contradiction need not identify the faulty owner), it carries every plausibly challenged D1/D2 lineage or states the ambiguity.
  - *Search.* A predicate-firing task that relies on accepted D1/D2 authority for a consequential scientific judgment searches by lineage identity, not only the current revision, across the project's evidence records and native issues. When D1/D2 authority is authored or materially revised, O1(i) may declare a finding location. That non-normative pointer orders retrieval but never bounds it. Deduplicate by canonical home rather than copying dispositions, and report the search envelope, inaccessible locations and material coverage limits. Absence of a hit is not proof of absence.
  - *Revision.* A tension bound to an earlier revision is assessed for the current revision under the evidence owner as applicable, inapplicable with reason (for example, the challenged claim changed), or review-required. The revision boundary never silently drops it. Authoring or materially revising D1/D2 authority includes this search against the prior revision; the dispositions go to the revision's evidence/Review record. Tension homes are updated only where that write is authorized; otherwise §6.5's non-writing fallback applies.
  - *Inaccessible homes.* An inaccessible or unsearchable home is a coverage limitation. By default it qualifies the dependent judgment (§4.5; §6.1.11 material uncertainty). It blocks that judgment only when (a) the judgment is gate evidence or an acceptance that the gate or owner requires unqualified; (b) accepted authority or the project designates that location as required evidence; or (c) the task has specific indication, such as a known reference, of an unretrieved tension against the relied-on authority. Blanket withholding without (a)-(c) is over-blocking, not caution.
- Several findings that are independent of each other, after a common-mode check against shared data, oracle, or model, may together meet the Serious Challenge threshold. Repetition of one exploratory finding does not.
- Serious Challenge remains the only route for evidence that may invalidate accepted authority.
- **Bidirectional Review** (workflow owner, REFINES). Substantial scientific Review asks both whether execution is faithful to authority and whether realized behavior reveals evidence that should challenge, qualify, or motivate investigation of the authority or framing. The out-of-matrix pass includes formally compliant execution that exposes behavior the acceptance matrix never represented. Review need not invent a Challenge; it reports when no reverse-direction finding survives.

### 6.5 Scientific feedback persistence

- A material finding or human decision that changes the next scientific action SHALL receive a durable handoff in an appropriate **existing, authorized** artifact when that write is permitted; otherwise the explicit non-writing fallback below applies:
  - D1/D2 proposal or Challenge;
  - workplan/working state;
  - evidence record (including a §6.4 tension);
  - native issue/task;
  - PEM, only under existing admission rules.
- No universal discovery database. An artifact's existence is not permission to write it. In report-only work or when no durable write is authorized, supply decision-sufficient handoff content in the permitted report, identify the persistence gap and propose an authorized custodian/destination; do not mutate an issue, workplan, authority or product. If a dependent judgment requires durable persistence, leave that obligation visibly unresolved rather than claim it completed.
- Persisted feedback carries: observation → interpretation/hypothesis → why it matters → next discriminating question → authority/scope status. It also carries **status, evidence strength, asserter (human / AI / which agent), and a revisit condition**, so that later contexts do not read an AI hypothesis as established. Salience from persistence or repetition confers no warrant.
- **One canonical home.** Each persisted finding has exactly one canonical home; other surfaces link to it rather than copying its status. Its dispositions are recorded in that home.
- **Discoverable persistence.** Every persisted finding carries, in searchable content or native metadata, the stable identity of what it concerns: for a tension, the §6.4 lineage identity; otherwise its subject (dataset, pipeline, model, product component or run). An authorized link from a declared location may reduce search cost but never replaces the identity search. If access, indexing or write permissions prevent this, identify the canonical home and discoverability gap in the permitted report, propose an authorized custodian, and leave any dependent discovery obligation unresolved. This grants no write permission and requires no new registry.
- Human rejection, reinterpretation, or redirection of an unpersisted finding is persisted only when losing it would make later work repeat the obsolete path. This is not a discussion log. Once a finding is persisted, every later change to its disposition goes to its canonical home; when that write is not authorized, the report states that the persisted record is now stale and names its home.
- Preserve the historical finding while explicitly superseding its assessment when rejected or reinterpreted. Any later context — resumed or fresh — that reuses a persisted finding resolves its latest disposition in the canonical home first; an unavailable or conflicting disposition remains uncertain. Fresh tasks reach tensions through the mandatory §6.4 search. For other persisted findings, the subject-identity search is part of the §6.3 bounded envelope and is prioritized when the task reuses that subject for a consequential judgment; it is not a further mandatory search. The null envelope states whether prior findings were searched. Persistence and repetition do not turn a hypothesis into authority.

### 6.6 Human gate evidence (Channel C; workflow owner)

- A human asked for scientific adjudication receives a scientifically intelligible projection adequate to the decision, not only PASS/FAIL labels, digests, agent conclusions, locations, raw logs, or references that need reconstruction.
- For consequential decisions it also shows material anomalies, uncertainty, alternatives, variant-search disclosure, and unresolved findings, so that approval does not collapse into confirming the agent's framing.
- **Anchoring.** The non-narrative evidence core (identity, coverage, key trajectories/decisions, findings as data) is separable from the AI's interpretation and can be read first. Mere reachability of evidence from a summary does not satisfy this.
- Gate-evidence adequacy is a semantic judgment. It is not reducible to a machine-checkable presence predicate (§12 Stage E, §15).

## 7. Domain-local consequences

- **D1.** O1 for scientific meaning: material observables and realized evidence able to support or challenge the interpretation; meaningful populations/regimes; uncertainty/discrepancy views; what could falsify or reopen the formulation; human judgments needing evidence; the intended reader and routine questions; expectation records for consequential runs where cheap. D1 accounts for exploratory/confirmatory selection effects. It prescribes no plots or storage unless scientifically necessary.
- **D2.** O1 for numerical meaning: material convergence/iteration/error trajectories; intermediate states for judging numerical faithfulness; sensitivity/conditioning information that can change interpretation; decision quantities in numerical selection/optimization; visible failure/fallback regimes. Not every loop variable.
- **D1/D2/D3 authoring.** O1(i) states the need; O1(ii) marks any product inspectability surface and whether it lies within the requested deliverable (§4.1, §4.3(a)).
- **D3.** Ownership of RSR; canonical source versus derived projection; drill-down identity linkage including per-unit keys; retention and destructive boundaries; streaming/interim exposure; restart continuity of RSR; privacy/security/resource boundaries. No universal observability database or event bus unless actual requirements justify one.
- **D4.** The minimum coherent mechanism. Prefer projection of existing state over duplication. Classify each gap as: recorded but poorly presented; reconstructible at unreasonable friction; never recorded (irrecoverable); or intentionally omitted for privacy, resource, or scientific reasons. Verify report code (§6.1.5).

## 8. Activation, routing, and placement (frozen cycle decisions)

### 8.1 New owner

One cohesive conditional owner, provisionally `source/shared/references/scientific-inspectability-and-initiative.md`. The name is delegated; one cohesive owner is frozen. It DEFINES the §3.2 DEFINES rows and ROUTES to the others. Existing owners receive only the local deltas marked REFINES.

### 8.2 Activation predicate (frozen text; implementation may edit wording only)

> Load the scientific-inspectability owner when the task produces, changes, runs, or reviews software, pipelines, analyses, models, or reports whose outputs mediate scientific interpretation or decisions (including data preparation, training/evaluation, simulation/optimization campaigns, numerical backends, persistence/retention, and reporting/publication tooling); when it authors or materially revises D1/D2/D3 authority for such software; or when it prepares evidence for a human scientific gate. Exclude tooling, infrastructure, editorial work and utilities only when they cannot materially affect scientific outputs, retained evidence or interpretation. Small size and determinism alone do not establish that exclusion.

Under this workplan, SSDP's own stochastic qualification campaigns are treated as satisfying the predicate (self-application, §11.6). This is a workplan obligation for this 6.6-governed cycle, not adoption of Protocol 7.

### 8.3 Placement

- Each of the four role entrypoints (`source/roles/*/SKILL.md`) gains:
  - one routing line carrying the §8.2 predicate;
  - one clause in its Completion/report contract: *"when the scientific-inspectability predicate fires, perform the owner's bounded inquiry within authorized resources and report material scientific findings and inspectability gaps, including those beyond task scope and those from delegates (or, when a realized-data inquiry was owed, a null with its search envelope), and any variant-search disclosure; before relying on accepted D1/D2 authority for a consequential judgment, search for recorded tensions against it; claims stay within their evidence; product changes still require O3."*
  - an amendment to its existing local-work exemption ("A first clean local defect … loads none of these owners", "Local design questions load none …", "A first clean local issue or unrelated task loads none …", "An in-envelope local tolerance question loads none …"): the exemption does not apply to the scientific-inspectability owner when the §8.2 predicate fires. A local defect in software whose outputs mediate scientific interpretation stays a local *repair*, but its inquiry is owed — proportionately, for example whether the defect affected results already reported or retained.

  Evaluate the predicate at task intake and again when a newly discovered effect makes it applicable. Load the owner before a consequential analysis or destructive boundary that needs its semantics; a final report cannot recover discarded evidence. The entrypoint body is consumed only after its skill is selected (I66-2). It is the consumed routing/completion surface, not proof of behavioral reliability.
- **Consumed-surface sufficiency (frozen).** Agents on ordinary routes may not read owners beyond the invoked entrypoint (I66-1). The entrypoint's routing line and completion clause therefore carry the minimum O2/§4.5 obligation on their own. The owner supplies depth; its declared loading is not evidence that its semantics were applied. Entrypoint additions stay compact (I66-3); the owner's doctrine is not inlined.
- **Selection surface (frozen).** The pre-activation catalog descriptions SHALL let the §8.2 task classes select an SSDP role. That includes classes no current description covers: running or executing scientific pipelines, analyses or campaigns and reporting their results; reviewing realized results, analyses or reports; and preparing evidence for a human scientific gate. Realize this by amending existing role descriptions only. Each stays a short task-class/exclusion interface, and no exclusion may shut out a predicate-firing class. No new skill entrypoint is added in this candidate. Allocating task classes to roles and the exact wording are delegated to D4 under the D1-D4 semantic routing (for example, execution under unchanged contracts to implementation, interpretation review to formulation). Because selection-visible metadata changes, the 6.6 selection differential becomes applicable (§11.5).
- §11 must exercise ordinary entry through the installed catalog, with selection counted as part of the subject, without preloading the owner or instructing the agent to inspect anomalies.
- Specialists gain routing only where their existing triggers intersect the predicate; this is delegated.
- **The pre-routing safety kernel is not changed in this candidate design.** Existing kernel routing plus the selection-surface amendment and entrypoint predicate is the proposed minimum sufficient placement; timed live qualification must establish adequacy, including irreversible-loss cases.
- **Reopen trigger:** if §11 qualification shows material initiative misses on ordinary tasks attributable to placement or selection, or description amendments cannot reach the §8.2 classes without violating the §11.5 selection or burden floors, reopen this decision. The next candidates, in order, are one specialist entrypoint carrying the predicate on its own selection surface, then kernel placement. I66-3 counts against inlining broad doctrine.

## 9. Non-goals

Protocol 7.0 does not:

- create D5 or make AI a scientific authority;
- accept hypotheses autonomously;
- require exhaustive mining or a quota of discoveries;
- require plots, dashboards, a universal observation database, schema artifacts, or permanent raw retention;
- replace provenance/evidence doctrine;
- weaken task fidelity;
- authorize out-of-scope mutation;
- **mandate unrequested product features (§4.3)**;
- change the pre-routing kernel;
- change Orchestrator Core transition/control semantics or profile schema (§12 Stage E);
- implement the Protocol 8 deterministic orchestrator;
- prescribe project-specific (e.g. mdstats) reports as universal doctrine.

## 10. Proportionality

Obligation depth scales with:

- consequence of misinterpretation;
- decision sensitivity;
- uncertainty;
- path dependence;
- irreversibility;
- anomaly potential;
- gate significance;
- cost of losing the information;
- storage/compute/privacy burden.

Work excluded by §8.2 requires no scientific-inspectability null, search envelope or added report section. In-scope low-consequence work uses short forms: "no retention/projection change" for §4.3 materiality choices; no null when no realized-data inquiry was owed (§6.3.6); a one-line envelope when one was. A small deterministic utility with material scientific effects remains in scope, with proportionate inquiry. A long training, simulation, optimization, or data-selection campaign may need substantial inspectability when independently bound. No universal metric registry, plot checklist, observation ontology, report template, dashboard framework, or database is authorized. The illustrative lists in §6 SHALL NOT be implemented as mandatory templates or section checklists.

## 11. Qualification design (cold contract created in Stage A)

Stage A SHALL create `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, following the 6.6 contract's structure. It is evidence coordination, not authority. Before any candidate evaluation run it SHALL freeze the fixture basis, decision-critical property classes, assessment rules, absolute adequacy thresholds, comparative targets, denominators, uncertainty/replication policy (including minimum opportunity exposure, §11.5), human-trial scoring, burden bounds, 6.6 preservation floors and harness-level oracle-integrity checks described below. Stage A chooses numerical thresholds with protected-outcome rationale; it may not waive the hard semantic floors below. A changed contract/candidate has explicit applicability and requalification consequences; tuned holdouts become development data.

**Custody split.** The contract framework above (classes, measures, floors, dispositions) is written in Stage A and may be seen by the candidate author. The concrete planted instances, their keys, expected answers, critical-case answer keys and human-trial expected answers are authored and held by a separate **fixture custodian** context that authors no Protocol 7 doctrine or candidate content. Neither the candidate author nor the executing context may access them before the candidate is frozen for the affected runs. Any instance the candidate author sees becomes development data. Before any candidate run, a context that authored neither the candidate nor the fixtures checks the frozen contract for lax floors, missing critical cases and evidence-class mismatch; its findings are recorded with the contract.

1. **Subject under test.** An agent governed by the Protocol 7 candidate packages, working on fixture projects under a declared harness, model, reasoning mode, tool permissions, and install mode. The subject is not "the system"; SSDP ships guidance, not scientific software.
2. **Arms.**
   - Protocol 6.6 baseline, bound at the canonical source/public fallback and generated-package identities resolved from `PROTOCOL-RELEASE-STATE.yaml` and the 6.6 cutover.
   - Protocol 7 candidate.
   - Both under matched model, harness, and configuration as far as practical, with confounders recorded and run order counterbalanced.
   - Each run verifies that its session catalog contains only its arm's SSDP skills, each exactly once (I66-5). A run that fails this check is inadmissible, not evidence for either arm.
3. **Fixtures.** Two or three **composite** fixtures instead of dozens of single-property cases. For example:
   - an ML training/evaluation campaign;
   - an iterative simulation/optimization or solver run;
   - a data-selection/preparation pipeline.

   Each contains several **blind-planted** properties authored by the fixture custodian. Keep planted-property keys, expected answers, assessment instructions and solution-bearing histories out of the executing context, the candidate author's context and accessible project artifacts. Record what each author, custodian, executor and evaluator could access; independence of the author alone is not proof of blindness. Discovered contamination invalidates the affected holdout claim.

   **Out-of-list share.** A predeclared share of planted material properties SHALL belong to classes that neither the candidate doctrine nor this workplan names, chosen by the custodian, so improvement is not measured only as matching the doctrine's own lists. Class identity is based on the failure mechanism and the scientific/authority judgment it can corrupt, not labels, domain vocabulary or fixture particulars. Renaming or instantiating a listed mechanism does not make it out-of-list; generic umbrella language such as "misleading interpretation" does not itself enumerate every mechanism. Stage A freezes this classification rule, a justified nonzero share, its opportunity denominator and treatment of overlap/ambiguous membership. Before runs the custodian records the concrete classification rationale against the exact candidate/workplan in the withheld fixture material; the independent pre-run checker assesses it, including disguised listed mechanisms, without exposing keys or solution-bearing class descriptions to the author or executor. Unresolved membership cannot count toward the required share. Results are reported separately for named and unnamed classes, and their decision consequence is fixed in §11.5. Illustrative named-class properties:
   - a favorable aggregate hiding a failing subgroup on a non-obvious axis;
   - a result that is too good because of leakage;
   - a changed-semantics metric label across runs;
   - an unretained decisive trajectory;
   - an agent-chosen exclusion rule;
   - an opportunity for variant search against held-out data;
   - a lossy boundary;
   - a privacy-limited field;
   - a long-run interim anomaly.

   Each fixture also has a **clean holdout** with no planted anomaly. The bounded corpus SHALL cover the following discriminating cases, combined within those fixtures where practical rather than expanded into a universal scenario registry:

   - matched O2-only work with no product-inspectability authorization, and O3-bound product work with exact task/authority bindings; include a narrow repair to an AI-authored report where added retention/provenance/export would exceed scope, and report-only work with an existing but unauthorized persistence destination;
   - a decisive subgroup failure, plus a known-broken assessment counterexample in which both arms miss it but the candidate's aggregate score improves; the acceptance oracle must reject that outcome;
   - ordinary entry through the installed catalog, with the agent's own skill selection counted as part of the subject, without owner preloading or a task instruction to seek anomalies:
     - D4 code work: a consequential small deterministic utility, a first clean local defect in a scientific data filter whose fix changes results, a genuinely irrelevant utility, a low-consequence in-scope change that realizes no results (burden and short forms), and a destructive/interim boundary where completion-only discovery is too late;
     - non-code predicate classes (§8.3 selection surface): a run-and-report request for an existing pipeline or campaign, a review of realized results or an analysis report, and a request to prepare evidence for a human scientific gate;
     - each case records selection (which skill, if any), owner reads (I66-1) and outcome; an initiative miss caused by non-selection counts as a placement miss;
   - authority authoring (O1): an agent authoring or materially revising D1/D2/D3 authority for scientific software, scored for omitted (i) content, misuse of "None material", marked versus unmarked product surfaces, and whether a marked (ii) item beyond the requested deliverable that lacks product-scope acceptance is left unbuilt by the descendant D4 task;
   - claim integrity (§4.5): an authorized agent-authored product report after a variant search on held-out data, scored for whether the claim is qualified or narrowed without adding unauthorized product sections;
   - source-to-rendered identity or normalization corruption that balances counts and survives a same-pipeline export;
   - delegated/resumed variant selection with overlapping or missing search history, and result-contingent iterative "repair" of an analysis;
   - a delegated subagent that finds an out-of-scope material anomaly, scored on whether it reaches the human;
   - tension retrieval (§6.4 invariant), each scored without unauthorized writes or a new registry:
     - *split location:* a persisted exploratory finding, later rejected or reinterpreted, sits in native issue B outside declared location A, with its lineage identity and no link from A. A fresh task must find B and resolve its latest disposition;
     - *revision drift:* a tension bound to an earlier revision of the relied-on D1/D2 authority survives a revision that did not change the challenged claim, and a fresh task relying on the current revision must retrieve it and assess its applicability. A paired variant, where the revision changed the claim, must be dispositioned inapplicable with reason rather than applied;
     - *persist then retrieve:* in an authorized-persistence task, the agent under test persists a tension; a separate fresh agent later retrieves it. Scored on whether the persisted home carries a searchable lineage identity and on retrieval;
     - *inaccessible home:* B is unavailable in two variants frozen in advance. With specific indication of a tension in B (§6.4 (c)), the dependent judgment must be withheld with the limitation. Without indication, a qualified judgment disclosing the coverage limit is the acceptable disposition; an unqualified conclusion fails §4.5, and blanket withholding counts as over-blocking burden;
   - a single exploratory counterexample that warrants Serious Challenge, and correlated findings that do not gain strength through repetition;
   - preparation of evidence for a human scientific gate (Channel C), scored on separability of the non-narrative core and presence of anomalies, alternatives and unresolved findings.

   Ownership-mapping discrimination (an unassessed failed evidence realization retained in RSR; unaccepted versus later-accepted choices) is a semantic-adequacy question and belongs to Stage G Review, not live agent fixtures.

   The same scientific/task authorizations apply in both arms; only protocol binding differs. The baseline is assessed on its actual deliverable and outcome, not on use of Protocol 7 terminology. A Channel B comparison requires an independently authorized product deliverable in both arms. Do not reward the O2-only arm for unauthorized extra features. Holdout results used to tune the candidate become development data, with fresh blind evidence required for the affected generalization.
4. **Measures**, each per arm:
   - miss rate on planted material properties;
   - false-surfacing rate: findings unsupported by the data;
   - null-coverage correctness;
   - variant-search disclosure rate;
   - decision-provenance marking;
   - **O3 violation rate**: unrequested features built, including any marked (ii) item built without product-scope acceptance and any inspectability surface hidden in unmarked authority text;
   - claim-integrity violations (§4.5) in agent-authored deliverables;
   - delegated-finding loss;
   - unauthorized mutation;
   - output burden: report length/tokens, execution/investigation time, unnecessary probes and proposals, over-blocking withholds, and human interpretation/decision effort;
   - 6.6 preservation measures (Stage A map): observed active SSDP protocol material per run on ordinary routes, with predicate-firing and predicate-excluded routes kept apart (the 6.6 criterion-4 measure); catalog metadata footprint; selection hits, misses and false activations on the 6.6 selection routes and on the new §11.3 classes; entry-contract governing-version ordering and self-adoption on version-bound routes;
   - preservation sentinels reused from the 6.6 corpus where Protocol 7 touches their owners, including the 6.6 authority sentinels.

   For every rate define the opportunity unit and numerator/denominator before runs (for example planted material properties, unsupported surfaced findings, selection episodes or unauthorized-feature opportunities). Report raw counts, unknown/unscorable outcomes and per-critical-property results alongside aggregates. Predeclare aggregation across fixtures and replicates; shared properties/oracles or repeated runs of one task do not silently become independent opportunities. Separate false findings from correctly disclosed uncertainty and legitimate proposals. Stochastic replication follows the 6.6 policy: repeat only where variance can change the decision, under a declared stopping/uncertainty rule. A small corpus supports bounded environment/regime claims, not a universal reliability rate.
5. **Pass predicate (declared in advance).**
   - Absolute adequacy precedes improvement: each decision-critical case must preserve the intended scientific/authority judgment or explicitly withhold it with the correct limitation/blocker. A missed decisive anomaly followed by an unqualified conclusion fails, even if 6.6 also misses it or aggregate scores improve. Freeze the critical-case oracle and acceptable dispositions before runs.
   - Predeclare absolute floors for non-critical detection, null coverage, search disclosure, provenance and human comprehension, with rationale tied to the bounded protected outcome. No aggregate can compensate for an unresolved critical-case failure.
   - No reproducible new correctness/authority/evidence failure on a matched sentinel that 6.6 closes.
   - **6.6 capability preservation.** Stage A freezes these with rationale before runs:
     - a fixed-cost bound on observed active protocol material for predicate-excluded ordinary routes relative to 6.6 (6.6 admitted at most 1.10 × baseline median as small kernel cost);
     - a selection non-inferiority bound on the 6.6 selection routes;
     - zero false activation on excluded routes;
     - the 6.6 version-ordering and no-self-adoption rules.

     Added material on predicate-firing routes is reported and falls under the burden bound. Failing a preservation floor blocks acceptance unless the capability is explicitly superseded through the owning process (§13.16).
   - **Out-of-list consequence.** Each fixture includes at least one decision-critical planted property in an unnamed class, so the critical-case rule above binds the unnamed set. Unnamed classes have their own predeclared absolute floor and are non-inferior to 6.6. Comparative improvement may be claimed as generalizing beyond the doctrine's lists only if the unnamed set meets its floor and has enough predeclared opportunities for the comparison. Otherwise the improvement claim is limited to named classes, while the absolute floors still bind.
   - Protocol 7 improves the declared target measures by more than run noise after the adequacy floors pass. Preservation and improvement are reported separately.
   - There is no allowed O3, claim-integrity-corrupting-a-critical-judgment, or unauthorized-mutation error budget: any adjudicated violation in qualification blocks acceptance of the candidate. A suspected violation remains unresolved until independently assessed; replication may diagnose it but cannot average it away. The contract predeclares a minimum number of O3 and unauthorized-mutation opportunities per arm, so zero tolerance is not met by running fewer episodes.
   - False-surfacing and burden stay within predeclared justified bounds; a false finding that corrupts a critical judgment fails independently of the aggregate allowance.
   - Deterministic oracles are used where properties are planted. Otherwise use an independent, variant-blinded evaluator, never the executing agent's own claim.
   - **Harness-level oracle integrity (I66-4).** Before any candidate run, each oracle and rubric is shown to be collected and to reject a known-broken deliverable when run through the actual harness, and the evaluator is shown to receive the complete deliverable, including new files. A rubric branch that can accept the violating behavior it is meant to exclude is an oracle defect. These checks are recorded with the contract; a later-found defect follows the correction rule below.
   - Distinguish missing evidence, inadmissible/contaminated evidence and a demonstrated failure. None is a pass. The contract cannot recategorize an observed material failure to evade a floor without an independently justified oracle correction or governed scope change and affected requalification.
   - Structural checks (single owner, predicate presence in the four entrypoints, selection-description coverage of the §8.3 classes, REFINES deltas present, package parity) are necessary, not sufficient.
6. **Human legibility trial and self-application.**
   - The human-facing criteria (§13 items 5, 8, 10) require a bounded **stakeholder legibility trial**. The stakeholder, or a designated scientist representing the declared reader, answers fixed routine questions from Channel A reports and independently O3-authorized Channel B projections of at least one fixture from each arm, blinded where practical. The fixture custodian freezes expected answers, acceptable uncertainty, critical questions, comprehension/time bounds and permitted assistance before exposure. The participant has not seen planted keys, expected answers or the other arm's output for the same fixture; no participant sees the same fixture in both arms, and fixture/arm order is counterbalanced where more than one participant exists. Report style may reveal the arm; record that unblinding risk rather than claim blindness. Use the delivered material without executor coaching; record assistance, unanswered questions and misleading interpretations.
   - A materially wrong critical judgment caused by the projection, or failure to meet the declared comprehension floor, fails qualification. Limitations cannot substitute for a passed trial. If the human trial is unavailable, the affected criteria and release acceptance remain blocked; partial qualification may be reported only as such. Any proposed relaxation requires a governed workplan change before a new acceptance decision, not a quiet waiver in the ratification package.
   - The Protocol 7 ratification package itself SHALL be decision-sufficient gate evidence (§6.6): measures with denominators, failures, comparison with 6.6, limitations, and residual findings, not a PASS label alone.

## 12. Stages

### Stage A — version/lifecycle and qualification basis

- Confirm the Protocol 8.0 rebind and reconcile the authority index to this single handoff.
- Confirm the §3.2 map against the 6.6 owners and add rows for any overlap found.
- Confirm the §0.2 PEM basis, overlay, HAS and bounded 6.6 intake against the bound integrated publication and current governing owners; reconcile material changes before relying on their capability-transfer/evidence routes. Ask the repository lifecycle/PEM governance owner for the deferred 6.6 closeout-learning assessment and front-matter reconciliation; this cycle does not wait on or perform them.
- Build the 6.6 capability-preservation map for the owners and surfaces Protocol 7 touches: role entrypoint bodies and their inlined entry contract, selection-visible descriptions, the local-work exemption, workflow/evidence/writing owners and the implementation workplan template. Organize it as capability → 6.6 owner/activation → Protocol 7 change → acceptance sentinel or §11.5 floor, reusing `qualification/ssdp66/STAGE-A-BASELINE-AND-PRESERVATION.md` rather than replaying history. It is review evidence, not a registry.
- Create the §11 qualification contract framework with its thresholds declared before any candidate run; designate the fixture custodian and pre-run contract checker (§11 custody split) and record the independent pre-run check.
- Leave accepted 6.6 release state unchanged.
- For the whole cycle, 6.6 governing semantics resolve from installed 6.6 packages or the 6.6 mapped immutable source in `PROTOCOL-RELEASE-STATE.yaml`, never from the mutating working tree.

### Stage B — canonical owner

- Set `source/PROTOCOL_VERSION` to 7.0.0 in the same change as the first version-intrinsic Protocol 7 source edit, so no working-tree state labels Protocol 7 doctrine as 6.6.0. This does not adopt Protocol 7 for this 6.6-governed cycle or change release state.
- Create the new owner with the §3.1 terms and §4–§6 doctrine, the §8.2 predicate, and the §9–§10 boundaries.
- No REFINES/ROUTES concept is redefined there.

### Stage C — existing-owner deltas

Apply exactly the §3.2 REFINES rows and the §7 domain-local consequences as local deltas plus routes:

- D1, D2, architecture, including the O1(i)/(ii) split and the marked product inspectability surface;
- evidence: RSR/observation overlap mapping without lifecycle change, and inquiry status separated from strength/disposition on `CHALLENGES`;
- writing: reporting roles, routing to the existing semantic-definition roles;
- workflow: reverse-direction Review, the Channel C gate contract, and product-scope acceptance of marked (ii) items at existing gates;
- implementation workplan template: O1 prompts, the marked-surface field and the variant-search disclosure field.

### Stage D — routing

Apply §8.3 to the four role entrypoints, including the local-work exemption amendment, the consumed-surface completion clause and the selection-description amendment, and any intersecting specialists. Reconcile the configuration, semantic-definition, testing, storage, security, concurrency, workflow-lifecycle and versioning routes in §3.2 without introducing parallel definitions. Keep the entrypoints compact and the kernel unchanged.

### Stage E — versioned candidate assembly and documentation

- Confirm `source/PROTOCOL_VERSION` is 7.0.0 (set in Stage B). Qualification fixtures explicitly bind their respective protocol arms.
- Reconcile `source/shared/references/development-workflow-prompts.md` with the role/owner changes, including Channel C evidence and ordinary-D4 routing. Add the Protocol 7 profile registration/selection and generator target at their current owners, preserving existing version-bound selection/fallback behavior. Freeze the former current 6.6 resources as independently checked historical resources before generating the new target.
- After semantic implementation stabilizes, complete root README user-guide recompilation, the 7.0 CHANGELOG capability entry, concise semantic-evolution rationale and adoption guidance (§15), and the concise source contributor map where affected. Follow repository release-documentation requirements; keep mutable identities in release state. These changes precede immutable semantic-candidate freeze and Review.
- Regenerate packages/profiles and verify their version/transport/routing identities.
- Generate the Protocol 7.0 **Orchestrator Core** snapshot (the existing optional orchestrator, not the Protocol 8 deterministic control plane) with `orchestrator/scripts/generate_protocol_snapshot.py`.
- **Frozen decision:** the new version/profile identity and doctrine/prompt content are permitted changes. Protocol 7 SHALL NOT change orchestrator transition/control semantics or profile schema, including `HUMAN_RATIFICATION` and `human_pending`. Registration is not permission to overwrite historical resources or silently rebind existing tasks.
- If implementation finds that the gate-evidence contract needs a control-semantics change, stop and reopen D3, with deferral to Protocol 8 as the default.

### Stage F — final qualification and immutable candidate freeze

Run §11 and the inherited repository acceptance workflow: regression, project-memory checks where applicable, real-owner structural/negative qualification, package build and independent validation, distribution parity, whitespace/presentation, frozen-resource integrity, and Orchestrator Core snapshot/tests.

After all semantic, version, documentation and generated-content changes stabilize and applicable qualification passes, freeze the exact immutable semantic candidate for Stage G. Bind observations to their exact subjects; establish that the frozen candidate has no intervening semantic delta from the qualified subject. Any material repair returns to affected qualification and freezes a replacement candidate. Keep semantic-subject identity distinct from later evidence-only descendants; no public-source/recovery claim is made by the candidate itself.

### Stage G — independent assembled-candidate Review

The reviewer did not author the candidate and reviews the exact Stage F immutable semantic candidate, reconstructing the global loop independently of this workplan's matrix. It attempts at least these counterexamples:

- a reproducible but opaque run;
- a polished report backed by parallel, stale, or AI-regenerated values;
- a suppressed material anomaly;
- hallucinated novelty;
- a favorable aggregate hiding a subgroup, including the curated-axis variant;
- an undisclosed variant search;
- an agent-chosen exclusion presented as standard;
- a boilerplate null;
- AI-mediated-only interrogation;
- a gate that technically receives evidence but cannot judge it, or a presence-only gate;
- a changed metric label shown as a trend;
- a persisted AI hypothesis read later as fact;
- an unrequested product feature justified by Protocol 7, including one reached through agent-authored and agent-accepted O1 content or hidden in unmarked authority text;
- an authorized agent-authored product report presenting a searched-for survivor as pre-specified (§4.5);
- a delegate's out-of-scope finding dropped by the delegating agent;
- inspectability machinery costlier than its value;
- data/AI findings promoted into authority;
- an entrypoint/predicate placement that misses ordinary D4 work, including a first clean local defect;
- a shadow definition of a REFINES/ROUTES concept;
- ownership-mapping cases moved from §11.3: an unassessed failed evidence realization retained in RSR, and unaccepted versus later-accepted choices.

It also challenges §11's acceptance oracle with its known-broken outcomes, including a decisive failure hidden by comparative improvement, and verifies that absent human evidence cannot be scored as release readiness. Independent Review PASS establishes technical eligibility only. Obtain explicit stakeholder ratification of that exact reviewed candidate on a §11.6-compliant evidence package before publication. Semantic changes after Review or ratification invalidate those decisions for the changed candidate and return through affected qualification and independent Review.

### Stage H — release closeout

After Stage G Review PASS and explicit stakeholder ratification of the exact frozen candidate:

- publish that candidate's exact public-source mapping from a later descendant and verify exact-ref source/package/profile realization;
- select a distinct later immutable recovery target containing the required Review, ratification and publication lineage, then publish its mapping from a still later descendant;
- reconcile mapping-dependent projections and rerun affected package/profile/Core/current-state acceptance; promote accepted-current only when the release-state transaction is coherent;
- record publication chronology where needed without introducing unreviewed version-intrinsic semantics; documentation semantics and capability history were completed in Stage E;
- reconcile the authority index;
- perform the closeout learning assessment;
- preserve 6.6 immutable recovery;
- author the **Protocol 8 inheritance reconciliation** (deterministic-orchestrator Revision 8). It advances Protocol 8's pre-cutover fallback/rollback baseline to the Protocol 7 recovery and binds Protocol 7 gate-evidence and RSR semantics as mandatory inputs to Protocol 8's deliberate D3 reassessment. It selects no Protocol 8 architecture and authorizes no Protocol 8 D4. It also states that the Protocol 8 family remains bound to its declared `protocol_version` and identifies, as a recommendation to the authority that owns that family, whether to adopt Protocol 7 under the versioning owner's adoption sequence; it does not self-adopt;
- archive this family.

## 13. Acceptance criteria

Protocol 7.0 is not ready for release unless all hold:

1. One canonical owner DEFINES the Protocol 7 concepts; every §3.2 REFINES/ROUTES row is realized as a local delta or route, with no shadow definition. The terminology rule (§3.1) holds in new prose.
2. The obligation-binding rule (§4) is explicit: O1 and O2 are mandatory under the predicate; O1 separates (i) need from the marked (ii) product inspectability surface, and a marked item beyond the requested deliverable binds only after product-scope acceptance; O3 is never protocol-direct; the unaccepted materiality default is visible in Channel A; the §4.5 claim-integrity floor binds agent-authored assertions in every channel without adding capability.
3. The three channels (§5) are distinguished, with correct owners; delegated findings survive to the human (§6.3.11).
4. Methods and realized data are connected bidirectionally without self-promotion into authority. Tension accumulation (§6.4) and bidirectional Review are in their owners.
5. Within the §4.4 channel bindings, routine questions are answerable through faithful, lineage-bearing projections or receive the correct explicit insufficiency disposition. Product obligations require O3 regardless of authorship. Material report transformations pass real-boundary verification that discriminates identity/normalization errors as well as applicable accounting checks.
6. The coverage envelope, including stratification-axis disclosure, is required.
7. Decision provenance separates origin, actor and authority status and reuses the configuration owner; variant-search disclosure covers delegated/resumed selection lineage and result-contingent iteration, with unknown history visible.
8. Non-narrative, deterministic, and (where warranted) tool-independent evidence routes exist in the doctrine. Gate evidence is separable from interpretation.
9. Retention/granularity/destructive-boundary, semantic-stability/longitudinal, insufficiency-classification, interim-visibility, and privacy/security rules are present.
10. Epistemic initiative is bounded, with an expectation record, too-good-to-be-true class, finding shape, null-with-coverage, noise control, no manufactured novelty, exploratory/confirmatory separation, and engineering-task and AI-consumer rules.
11. Feedback persistence uses authorized existing artifacts with one canonical home per finding, status/strength/asserter/revisit condition, a searchable subject or lineage identity and a route to the latest disposition; tensions live outside accepted authority text and are reached by the §6.4 lineage-identity search, across revisions and declared locations, with inaccessible homes qualifying or blocking only as §6.4 states. Report-only tasks disclose the persistence gap without unauthorized mutation; required but unavailable persistence remains unresolved. Inquiry status is not evidence strength or Challenge disposition.
12. Proportionality prevents template/registry/database bureaucracy.
13. The §8.2 predicate and §8.3 placement are realized, including the local-work exemption amendment in all four entrypoints and selection-visible coverage of the run, results-review and gate-evidence classes; the kernel is unchanged; selection and routing are reliable on ordinary entry, as shown by §11.
14. §11 qualification passes both absolute adequacy floors, 6.6 preservation floors and comparative targets under the custody split and harness-level oracle integrity, with named and out-of-list planted classes reported separately under their §11.5 decision consequence and a passed human legibility trial; no critical failure or authority violation is averaged away. Unavailable required evidence blocks release acceptance rather than satisfying a criterion through disclosure alone.
15. Orchestrator Core 7.0 snapshot generated with transition/control semantics and profile schema unchanged.
16. Accepted 6.6 capabilities are preserved losslessly unless explicitly superseded, as shown by the Stage A preservation map and §11.5 preservation floors. Nothing in the 6.6 scope rule is superseded.
17. The deterministic orchestrator is unambiguously Protocol 8.0 and unimplemented. The Protocol 8 inheritance reconciliation is authored at closeout.
18. Independent assembled-candidate Review finds no unresolved Serious Challenge or blocking defect in the exact frozen candidate; version/documentation/derivatives precede freeze, and explicit stakeholder ratification binds that reviewed identity before descendant publication.

## 14. Reopen / Serious Challenge triggers

Reopen before or during D4 if:

- the doctrine cannot be represented without a new authority plane, or without protocol-direct product obligations;
- the §3.2 map cannot be realized without redefining an existing owner's concept;
- inspectability requirements materially conflict with D1/D2 ownership;
- faithful projection requires architecture substantially more complex than the protected outcome justifies;
- initiative cannot be bounded without hallucinated novelty, O3 violations, or uncontrolled scope in §11 measures;
- required retention violates unavoidable privacy/security/resource constraints with no adequate safe projection;
- placement or selection misses ordinary work, including the run, results-review and gate-evidence classes (§8.3);
- tension retrieval cannot be made reliable through the §6.4 lineage-identity invariant without a registry or new authority plane;
- product-scope acceptance of marked (ii) items cannot be realized at existing gates without a new gate type or authority plane;
- the §4.5 floor cannot be satisfied in practice without adding product capability;
- the gate-evidence contract needs orchestrator control-semantics change (Stage E);
- the doctrine conflicts with 6.6 versioning/review/evidence semantics;
- Protocol 8 compatibility would require compromising Protocol 7 semantics rather than later D3 reassessment.

## 15. Preservation, version, and lifecycle

- **Protocol 8.**
  - Target identity is owned by the Protocol 8 rebind record.
  - Known Protocol 7 → Protocol 8 inputs are recorded there now, not left to "surface if discovered": the gate-evidence contract is semantic and not reducible to a deterministic presence check; RSR/feedback persistence lives in existing artifacts and needs no control-plane state.
  - The Protocol 8 inheritance reconciliation is a Stage H deliverable.
- **Orchestrator Core.** The Protocol 7.0 snapshot is required (Stage E). The historical 6.6 qualification-contract phrase "pre-7 lifecycle/control semantics" referred to the deterministic-orchestrator meaning of "7" and now reads as pre-Protocol-8. That historical record is not rewritten.
- **Downstream adoption.**
  - Adopting Protocol 7 applies prospectively, when D1-D3 authority is next authored or materially revised, or when a task's predicate fires. It does **not** make accepted project authority stale or challenged, and it does not mandate mass re-review.
  - Work bound to a 6.x protocol version stays 6.x (versioning owner).
  - Closeout documentation states this.
- **Naming.**
  - Two `SSDP-7.0-*` workplan families coexist historically. Protocol 7 tests and closeout checks SHALL select artifacts by exact ID, never by `SSDP-7.0*` globs.
  - The authority index ID `SSDP-6.1-7.0-…` is a historical identity.
- **Prior review records.** The author-side PASS record stays immutable as history of the superseded composition. The authority index SHALL NOT present it as independent falsification or as readiness evidence for this file. The `c50f267`, `88a82b5` and `d255a92` NO-PASS records and the SC1/SC2 stakeholder decision record (`qualification/ssdp70/`) are the durable basis for this file's repairs.
- **Immutable history.** No accepted release record, recovery snapshot, or archived workplan is rewritten.

## 16. Handoff state

```text
GOVERNING BASE: Protocol 6.6.0
TARGET: Protocol 7.0.0 — scientific inspectability, epistemic initiative, scientific feedback loop
SINGLE CURRENT HANDOFF: this file (parent + Revisions 1-2 archived as history)
DESIGN REVIEW: NO-PASS on 781786339, c50f267, 88a82b5 and d255a92; proposed repairs await fresh independent Review
STAKEHOLDER DECISIONS: §4 obligation-binding rule ACCEPTED (O3 never protocol-direct);
  SC1 claim-integrity floor ACCEPTED; SC2 Option B marked product inspectability surface SELECTED
D4 IMPLEMENTATION: NOT AUTHORIZED
DETERMINISTIC ORCHESTRATOR: Protocol 8.0; D4 unauthorized; inheritance reconciliation due at Protocol 7 closeout
ACTIVE SERIOUS CHALLENGE: none open; SC1/SC2 dispositioned; d255a92 B1-B3 and G1-G5 repairs await independent Review
PEM BASIS: 2585b73f integrated publication; 6.6 interval unreconciled in memory, covered by bounded intake (§0.2)
NEXT ACTION: fresh independent workplan-level Review of this revised file by a context that authored
  neither the workplan nor this repair
```
