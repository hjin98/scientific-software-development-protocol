# SSDP 7.2.1 S3 independent edit review — NO-PASS

Date: 2026-10-11. Governing protocol: SSDP 6.6.0, installed software-design skill and its kernel/architecture/testing/version-binding ownership. Fresh Codex independent edit reviewer; no candidate authorship. Review subject: `60b89e266a367d386e472924b7144d1c4091ec12`, branch `ssdp-7.2.1-reduction`, worktree `.claude/worktrees/agent-a2ab8c24b157a8fe2`. Full source and assembled affected-surface diff reviewed against `24518df5627bea00c1d84708acfd26cf2c4edb41`.

## Decision and blockers

No Serious Challenge to the ratified frozen minimum. **NO-PASS** for the two defects below. O-3 lossless representation and owner consistency pass independently; that bounded result is not S3/Go closure, qualification, admission, stakeholder acceptance or promotion.

1. **D4 version-binding defect, real owner `orchestrator/src/sdp_orchestrator/core/profile.py:88-89`.** The 7.2 profile is stamped `7.2.1` while its supported exact versions include `7.2.0`. Executing the real `profile_id_for_version('7.2.0')` and then `definition(...)` returns `ssdp-protocol-7.2`, protocol version `7.2.1`. `test_ssdp6_profiles.py` expressly requires that incorrect exact-version alias. Canonical versioning's Binding versus adoption rule permits a different patch source only for a two-part `X.Y` declaration; an exact declaration requires its own version. Compatibility never adopts. Frozen 7.2.0 `2dedcfa3408f62bc11a696ac3776183a87b40438` is non-governing and NOT QUALIFIED, but remains frozen evidence; that status does not authorize reinterpretation. Preserve exact 7.2.0 semantics or fail closed for that exact request rather than alias it to the revised profile. The two-part `7.2` alias can name the patch line. Reconcile the corresponding test and CHANGELOG's claim about exact 7.2.0 resolution. This violates coherent current authority and requires D4 repair, not new doctrine.

2. **S3 declared reduction condition not met for maintenance audit.** The design lead transmitted the user's explicit requirement that every block-carrying entrypoint be smaller than 7.2.0. `software-maintenance-audit/SKILL.md` is 9,879 bytes versus 9,842, and its Scientific checks section is 4,040 versus 4,003: both grow 37 bytes. Losslessness remains hard and the generic size target is soft, but neither waives this separately explicit cycle acceptance condition. Reduce this surface while retaining its complete ratified minimum. The other five surfaces shrink (table below).

## Independence, authority and scope

Read the revision-4 implementer brief, ratified consolidated 7.0 workplan annotations M1–M10 and relevant canonical source/test/mapping definitions. Did not read other S5/S4 reports, campaign/evaluator results, OMP stage-F workspace, fixture custody or Claude auto-memory. A registry memory search found no task-applicable memory, and no memory-derived factual claim is used. Project-memory schema validation below is a repository acceptance check, not activation of historical semantic guidance.

The full source delta is the source version, generated Scientific checks fragment, builder dependency comment, and scientific-inspectability owner. Four role entrypoints plus documentation/audit receive the fragment; hygiene remains outside the predicate. Reviewed source owner statements near lines 71 and 367 and consumed-surface owner wording near line 389. Other generated owner/version/template stamps and Orchestrator snapshot were accounted for by fresh build, independent validation, parity and immutable-snapshot acceptance.

## Semantic and form assessment — PASS

Every surviving §8.3 meaning stays on its applicable consumed entrypoint. No frozen meaning was moved to owner depth as a purported reduction. Questions/element subsets match: all four roles FRVT; documentation/audit FR; D1/D2 additionally revise authority; D1/D2/D3 carry authority authoring/review content; documentation carries choices; audit does not. Variant content refers to the same-surface question, which always accompanies element 2; tension persistence refers to same-surface Persistence, always accompanying element 3. Neither reference needs an owner load.

The relief is stated with scope, before duties. The finish-all-items numbered framing is removed. Duties name their operative events; Findings inherits the stated applicability predicate and relief. Findings/nulls, selected variants, recorded tensions, choice provenance/retention and claim integrity follow recoverability of scientific result status. Before-loss inquiry follows irreversibility; resource limits follow authorized cost; persistence follows durable decision continuity and write authority; tension search/disposition and inaccessible-home rules follow evidence coverage and authority; product changes follow scope acceptance; revision records preserve predecessor and tension continuity; delegation questions and gap reporting preserve coverage through delegation. These are principled obligations, not observed-failure coaching. Existing negative formulations implement invariant boundaries rather than introducing mistake-specific advice. Long content lists remain where their independently governed information is required; headings split separate duties instead of hiding them at the tail of one numbered paragraph.

Owner line 71 now removes the task-report reader/question proposal and widens materiality-basis reporting to every owed inquiry, findings or null, unless supplied by stakeholder/authority. Owner line 367 removes the old separately owed reader/question proposal. Authority authors still owe reader/questions under O1. No deletion exceeds M1–M10; no new upstream decision was inferred.

## Independent O-3 mapping

The rows below are independently matched to the amended workplan meaning, not accepted merely because phrase tests pass. Each row states its actual consumed routes and exact candidate sentence/clauses. PASS means the full row meaning is present on every named route, with same-surface references as identified above.

### R1.inclusion — PASS

Meaning: section 8.2 predicate and label row 'scientific inspectability applies (R1)': the inclusion list

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> Apply when work produces, changes, runs or reviews software, pipelines, analyses, models or reports whose outputs mediate scientific interpretation or decisions

> data preparation, training/evaluation, simulation/optimization campaigns, numerical backends, persistence/retention, reporting/publication tooling

> authors or materially revises D1-D3 authority for them

> or prepares evidence for a human scientific gate

### R1.exclusion — PASS

Meaning: section 8.2 predicate: exclusion limit; small size and determinism alone do not establish the exclusion; section 8.3 'including on local repairs'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> Small, deterministic and local work is included; skip only tooling, infrastructure, editorial work or utilities that cannot materially affect those outputs, retained evidence or interpretation

### R1.reevaluation — PASS

Meaning: section 8.2/8.3 re-evaluation: evaluate the predicate again when a newly discovered effect makes it applicable

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> Re-evaluate scope when a newly discovered effect may change it.

### R2.depth — PASS

Meaning: R2 as amended (recommended depth-read points, no required load)

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> These checks are the complete obligation; the [owner](references/scientific-inspectability-and-initiative.md) is optional depth (definitions, examples), most useful before consequential judgments over realized results, D1-D3 authority work or gate evidence.

### L.change-only — PASS

Meaning: label 'material findings (change-only relief)' and section 6.3.6: a change realizing no scientific results owes no null and, finding nothing, adds nothing; an asked answer is still owed; no delegate gap report is removed. Also element 1 'an asked answer is owed even where a change-only report would otherwise add nothing'. Stated with the scope, and each duty is owed when its trigger occurs (brief item 2)

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> Each check applies when its trigger occurs; a change realizing no results owes no null and, finding nothing, adds nothing except answers its delegator asked for and gaps owed for its delegates.

### E1.inquiry — PASS

Meaning: element 1: look for and report material findings and gaps, including beyond task scope and from delegates

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Findings.** Look for and report material scientific findings, including delegates' and out-of-scope ones, and inspectability gaps

### L.gap — PASS

Meaning: label 'inspectability gap'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> (missing, irrecoverable, archaeology-only or misleading realized records)

### E1.before-loss — PASS

Meaning: element 1: before any step that could discard, overwrite or irreversibly aggregate realized results or retained evidence, do that inquiry first

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Before loss.** Look for findings before discarding, overwriting or irreversibly aggregating realized results or retained evidence.

### L.resources — PASS

Meaning: label 'within authorized resources'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Resources.** Probe within the declared resource budget; with none declared, only negligible probes using no shared, metered or queued resource; propose the rest.

### L.null — PASS

Meaning: label 'realized-data inquiry owed; null' and element 1 null with search envelope

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Realized results.** Producing, running or reviewing realized results or preparing gate evidence owes that inquiry: report findings or a null naming examined and materially unexamined areas

### E1.materiality-basis — PASS

Meaning: element 1 as amended by M3 (and section 4.3 by M2, specialist placement by M6, consumed-surface sufficiency by M7): whenever a realized-data inquiry was owed, whether findings or a null are reported, state the materiality basis the inquiry used unless accepted authority or the stakeholder states it

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> and, either way, the materiality basis used, unless the stakeholder or accepted authority states it.

### L.persistence — PASS

Meaning: label 'feedback persistence (element 1)': one existing authorized writable home, the content list, later status changes, the non-writing fallback, no write authority from a report or possible destination

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Persistence.** A finding or human decision changing the next scientific action goes to one existing authorized writable home (never accepted authority text; PEM only under its admission rules)

> with observation, labeled interpretation, significance, next question, searchable stable subject and authority identity

> scope/status, evidence strength, asserter stated in its content as human or AI and which agent (the writing account does not show this), and revisit condition; later status changes go to that home.

> With no such home, report decision-sufficient content, the persistence gap and a proposed custodian/destination, leaving required persistence unresolved.

> No report or possible home grants write authority.

### L.authority-identity — PASS

Meaning: label 'authority identity (elements 1, 3)': owner/path plus heading, anchor or object ID, exact revision, claim or locator

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> (owner/path and heading, anchor or object ID, exact revision, claim or locator)

### L.authority-identity-e3 — PASS

Meaning: label 'authority identity' on element 3; element 3 search covers earlier revisions, former names or paths and recorded predecessors

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> by owner/path and heading, anchor or object ID, exact revision and claim or locator, earlier revisions, former names or paths and recorded predecessors

### L.asserter-written — PASS

Meaning: label 'asserter of a written record (elements 1, 3, 5)' on element 1, inline

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> asserter stated in its content as human or AI and which agent (the writing account does not show this)

### L.asserter-written-e3 — PASS

Meaning: label 'asserter of a written record' on element 3's persisting duty, by reference to 'Persistence' (element 1, carried on every route that carries element 3)

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> with its asserter stated in its content as under Persistence.

### L.asserter-written-e5 — PASS

Meaning: label 'asserter of a written record' on element 5, inline

Consumed routes: scientific-formulation, numerical-algorithm-design.

> Each assessment states in its content whether a human or an AI made it, and which agent (the account it is written or committed through does not show this)

### Q.lead — PASS

Meaning: element 1: unless the predicate evidently excludes the delegated work, ask each delegate in the request; (that an asked answer is owed even for change-only work is item L.change-only)

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> **If you delegate** (unless the scope evidently excludes that work), put these questions in the request itself:

### Q.findings — PASS

Meaning: delegate question: findings or none, with launched-work qualifier

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> "Report your material findings, including from any tools or agents you launched, or state that you have none."

### Q.realized — PASS

Meaning: delegate question: realized results or gate evidence, null envelope, with launched-work qualifier

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> "Did your work, including any tools or agents you launched, produce, run or review realized results or prepare gate evidence? If so, give your null envelope: what you examined and what material areas you did not."

### Q.variants — PASS

Meaning: delegate question: variants incl. changes after seeing results and bug fixes; disclosure content; launched-work qualifier

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> "Did your work, including any tools or agents you launched, evaluate more than one analysis, pipeline, preprocessing, model or parameter variant, including changes made after seeing results, even bug fixes? If so, give count and kind, selection criterion and data including held-out reuse, and lineage including delegated or resumed work, without double-counting overlapping trials; where earlier history is unavailable, a known lower bound, unknown interval and claim limit."

### Q.tensions — PASS

Meaning: delegate question: tension search, conditional on relying on accepted D1/D2 authority for a consequential judgment; entries, binding, asserter; label 'tension'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> Only if it relies on accepted D1/D2 authority for a consequential judgment: "For that judgment, including any tools or agents you launched, what did you search for recorded tensions against that authority (a recorded finding bearing on it that has not been raised as a Serious Challenge), what could you not reach, and what did you find (or none), with each record's entries, binding and asserter?"

### G.gap-rule — PASS

Meaning: gap rule of elements 1-2 and section 8.3 consumed-surface sufficiency: unanswered part and uncovered rest of a partial answer are a gap, never a null or no findings; exemption for realized results

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> Report each unanswered part, including when nothing returns and the uncovered rest of a partial answer, as a gap, never as none

> : findings always; realized results unless the task evidently produced, ran and reviewed no realized results and prepared no gate evidence

### G.gap-rule-variants — PASS

Meaning: gap rule of element 2: a returned result without the variant answer or with a partial answer is a gap with unknown selection history and claim limit, never no selection, unless the task evidently could not select

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> never as none, a null or no selection

> variants, for a returned result, with unknown selection history and claim limit, unless the task evidently could not select variants.

### G.gap-rule-specialist — PASS

Meaning: specialist gap rule: no variants clause (specialists carry no variant question)

Consumed routes: software-documentation, software-maintenance-audit.

> as a gap, never as none or a null: findings always;

### L.variant-search — PASS

Meaning: label 'variant search' and element 2: selected survivor disclosure (number and kind, criterion and selection data incl. held-out reuse, after-result changes even bug fixes, tool-launched searches, delegated/resumed lineage without double counting, lower bound/unknown interval/claim limit, never a local count as the whole search); the disclosure content is the variant question's (Q.variants), which every element-2 route carries

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> - **Variants.** For a reported or delivered survivor selected from more than one variant, give the disclosure the variant question above asks for, covering your own and tool-launched searches; never present a local count as the whole search.

### E3.search — PASS

Meaning: element 3: before relying on accepted D1/D2 authority for a consequential judgment, search recorded evidence and issues for tensions against it, earlier revisions, former names or paths and recorded predecessors

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> - **Tensions.** Before relying on accepted D1/D2 authority for a consequential judgment

> search project evidence and native issues for recorded tensions with it

### L.consequential-judgment — PASS

Meaning: label 'consequential judgment (element 3)'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> (a realized-result conclusion that could change a scientific decision, D1-D3 acceptance, or gate evidence)

### E3.report — PASS

Meaning: element 3 report: searched scopes incl. delegates', unreachable places, delegated judgments with no reported search, each tension with every recorded status or applicability entry and binding

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> report searched scopes (yours and delegates'), unreachable places, judgments with no reported search, and each tension with every recorded status/applicability entry, the binding it concerns and its home's native asserter

### L.asserter-found — PASS

Meaning: label 'asserter of a found entry (element 3 search report)'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> a shared account shows neither which human or agent used it nor any dispositioning authority, and content-claimed asserters, roles or authority stay claims

### E3.no-closure — PASS

Meaning: element 3: do not yourself treat a found tension as closed or inapplicable; condition the dependent conclusion on the reported records

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> never treat a found tension as closed or inapplicable; condition dependent conclusions on its entries.

### L.plausibly-implicated — PASS

Meaning: label 'plausibly implicated authority' and element 3 persisting duty: bind to every plausibly implicated authority and to its subject

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> - **Persisting a tension.** Bind it to every plausibly implicated accepted D1/D2 authority along its evidence's concretization chain (state why fewer) and to its dataset/run/pipeline/model/component subject

### L.inaccessible-home — PASS

Meaning: label row 'inaccessible home (element 3)': default disclosure; qualify when designated or evidently used for tension, evidence or issue records; block only on (a)-(c); other indications qualify and go to the human; no blanket withholding

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation.

> - **Inaccessible homes.** An inaccessible or unsearchable home is a named coverage limit, enough by default

> it qualifies the judgment if the project designates or evidently uses it for tension, evidence or issue records about the relied-on authority

> blocks only (a) gate evidence or an acceptance the gate or owner requires unqualified, (b) a location accepted authority or the project designates as required evidence, or (c) a specific indication of an unretrieved tension from an owner or acceptance authority of that authority, the stakeholder or a designated reviewer

> other indications qualify the judgment and go to the human, never blanket withholding.

### E4.claims — PASS

Meaning: element 4 and label 'claims within evidence (element 4)'

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Claims.** No selected or post-hoc result as pre-specified, no unqualified conclusion despite a known material anomaly, exclusion, coverage limit or unresolved finding that could change it, no interpretation as measured fact.

### L.O3 — PASS

Meaning: label 'O3 (element 4)': accepted authority, explicit stakeholder/task instruction or existing external/product contract; beyond-deliverable marked item only after stakeholder/task acceptance, never technical Review alone

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation, software-maintenance-audit.

> - **Product changes** need accepted authority, explicit stakeholder/task instruction or an existing external/product contract; a marked inspectability item beyond the requested deliverable binds only after stakeholder/task acceptance, never technical Review alone.

### E5.revision — PASS

Meaning: element 5 (D1/D2 only): revising, renaming, splitting, merging or replacing D1/D2 authority; also search tensions bound to accepted concretizations; record predecessor identity and per-tension applicability assessment in the revision's record and gate evidence; agent assessment marked proposed

Consumed routes: scientific-formulation, numerical-algorithm-design.

> - **Revising D1/D2 authority.** When revising, renaming, splitting, merging or replacing D1/D2 authority, also search recorded tensions bound to its accepted concretizations.

> In the revision's own record and its gate evidence, record the predecessor identity and, per found tension, a revision-scoped applicability assessment

> an agent's assessment is marked proposed until the revision's acceptance considers it.

### L.applicability — PASS

Meaning: label 'applicability assessment (element 5)': applicable, inapplicable with its reason, or review-required; scoped to the revision; neither changes nor closes the tension's own status

Consumed routes: scientific-formulation, numerical-algorithm-design.

> applicable, inapplicable with its reason, or review-required; it neither changes nor closes the tension's own status in its home.

### E6.choices — PASS

Meaning: element 6 and label 'consequential-choice status (element 6)': consequential choices, effective choice, origin and chooser, binding cited separately (exact accepted authority, explicit stakeholder/task instruction or existing external/product contract) or proposed; instruction not ratification; unknown origin not guessed

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation.

> - **Choices.** When you build or change a scientific pipeline, analysis or report, state each consequential choice (filtering, exclusions, missing values, splits, selection, defaults), its effective value, origin and chooser (human, agent, delegate, tool default, policy or unknown), and separately its binding: cite the exact accepted authority, explicit stakeholder/task instruction or existing external/product contract fixing it, else mark it proposed/unaccepted; an instruction is not ratification and an unknown origin is not guessed.

### L.O1-content — PASS

Meaning: label 'O1 content (element 6)' and 'material realized record' list as used in element 6 (the beyond-deliverable binding of a marked item is L.O3, carried on every element-6 route)

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation.

> unless applicable accepted D1-D3 authority states the material realized record (quantities, populations/regimes, trajectories, decisions, exclusions/failures, retention/destructive boundaries; "None material, because ..." valid), reader, routine questions and visibly marked product inspectability surfaces to retain, project or expose realized records with within-deliverable status ("agent reports only" or "None" valid; draft or unaccepted text does not bind)

### L.short-form — PASS

Meaning: label row 'reader/questions and short form (element 6)', renamed by M5 'retention/projection short form (element 6)': a retention/projection statement made without O1 content; agent-chosen parts visible proposed defaults; fixed parts cite their source; 'no retention/projection change' completes only the unchanged materiality-choices statement

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation.

> - **Retention.** For that pipeline, analysis or report,

> state what the change retains, projects and omits, marking agent-chosen parts as proposed defaults and citing what fixes the rest; "no retention/projection change" completes only this statement.

### L.material-realized-record — PASS

Meaning: label 'material realized record (element 7)': realized quantities, populations/regimes, trajectories, decisions, exclusions/failures and retention/destructive boundaries

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design.

> state the material realized record (realized quantities, populations/regimes, trajectories, decisions, exclusions/failures, retention/destructive boundaries)

### L.product-surface — PASS

Meaning: label 'product inspectability surface (element 7)': the routine questions the product itself must support by retaining, projecting or exposing realized records

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design.

> visibly mark each product inspectability surface (a routine question the product itself must support by retaining, projecting or exposing realized records)

### L.product-surface-e6 — PASS

Meaning: label 'product inspectability surface (element 7)' as used by element 6 on the routes that do not carry element 7

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design, software-implementation, software-documentation.

> visibly marked product inspectability surfaces to retain, project or expose realized records with within-deliverable status

### E7.authoring — PASS

Meaning: element 7 (D1/D2/D3): material realized record, reader, routine questions, product inspectability surfaces marked within or beyond the deliverable; acceptance review checks content, unmarked requirements and misclassified marks; technical acceptance does not accept a beyond-deliverable item

Consumed routes: scientific-formulation, numerical-algorithm-design, software-design.

> - **Authority content.** When authoring or materially revising D1/D2/D3 authority for such software, state the material realized record (realized quantities, populations/regimes, trajectories, decisions, exclusions/failures, retention/destructive boundaries), intended reader and routine scientific questions (“None material, because …” valid)

> visibly mark each product inspectability surface (a routine question the product itself must support by retaining, projecting or exposing realized records) as within or beyond the requested deliverable (“answered through agent reports only” or “None” valid)

> When reviewing such authority for acceptance, check for that content, for inspectability-driven product requirements left unmarked and for marks wrongly classed as within the deliverable, and state that technical acceptance does not accept a marked item beyond the requested deliverable, which binds only after the stakeholder or task authority accepts it.

## Removed meanings — authorized

- **X.E1-reader-questions**: element 1 (7.2.0): report the provisional intended reader and routine scientific questions the inquiry used where no accepted authority or stakeholder states them. Removed only under [7.2.1 amendment] M3 (workplan section 8.3 element 1), with M1 (standing interpretation, section 0.1), M2 (section 4.3), M6 (specialist placement) and M7 (consumed-surface sufficiency). Confirmed absent from every affected consumed entrypoint and reconciled owner wording.
- **X.E6-reader-question-proposal**: element 6 (7.2.0) and the first clause of label row 'reader/questions and short form (element 6)': independently and visibly propose a reader and routine questions when neither the stakeholder nor accepted authority states them, proportionately even for local work. Removed only under [7.2.1 amendment] M4 (workplan section 8.3 element 6 paragraph) and M5 (label table row), with M7 (consumed-surface sufficiency), M8 (section 10) and M10 (section 11 qualification design). Confirmed absent from every affected consumed entrypoint and reconciled owner wording.

M9/M10 amend future qualification-design interpretation only; this edit does not revise frozen 72b custody rubrics. M1/M2 reconcile standing/default meaning; M3/M4/M5 change element and label minimum; M6/M7 reconcile specialist and consumed sufficiency; M8 reconciles short-form proportionality. The mapping's two removed records cover those two semantic removals with their complete amendment routes.

## Byte accounting

Exact UTF-8 bytes of generated `dist/skills/<skill>/SKILL.md` at each immutable ref. Section bytes run from `## Scientific checks` to the next level-2 heading, excluding trailing newlines. 6.6 has no Scientific checks section (zero). Entrypoint values include all generated entry text; reduction delta is against 7.2.0.

| Skill | 6.6 entry/section | 7.2.0 entry/section | 7.2.1 entry/section | Delta entry/section |
|---|---:|---:|---:|---:|
| scientific-formulation | 6317/0 | 16512/10193 | 16417/10098 | -95/-95 |
| numerical-algorithm-design | 6559/0 | 16754/10193 | 16659/10098 | -95/-95 |
| software-design | 8397/0 | 17905/9506 | 17796/9397 | -109/-109 |
| software-implementation | 7057/0 | 15799/8526 | 15691/8418 | -108/-108 |
| software-documentation | 6264/0 | 11591/5325 | 11562/5296 | -29/-29 |
| software-maintenance-audit | 5837/0 | 9842/4003 | 9879/4040 | +37/+37 |

References: 6.6 `22f4bdba53795da3a6f13f162529f3a843fc37ae`; 7.2.0 `2dedcfa3408f62bc11a696ac3776183a87b40438`. Full measurement and per-entrypoint SHA-256: `/tmp/ssdp721-review-bytes.json`.

## Acceptance executed

Interpreter: repository-root existing uv `.venv/bin/python`, Python 3.13.14 (>=3.11), with validation/Core dependencies. Initial sandbox DNS failures were environmental; approved network-capable reruns executed the actual required checks successfully, without altering assertions or bypassing the installed-product owner.

- Inherited regression with `SSDP_VALIDATE_PUBLIC_FALLBACK=1`: **437 tests, OK**. `/tmp/ssdp721-review-regression-network.log`. Includes structural/negative Scientific checks mapping and inherited real-owner guards.
- Orchestrator Core complete acceptance: **384 tests across 12 modules, OK**, including real installed wheel/sdist product. `/tmp/ssdp721-review-core-network.log`.
- Fresh canonical build to `/tmp/ssdp721-review-dist`: PASS (`/tmp/ssdp721-review-build.log`). Independent `validate_packages.py`: PASS (`/tmp/ssdp721-review-packages.log`). Committed distribution parity: PASS (`/tmp/ssdp721-review-parity.log`).
- Release state coherent: PASS (`/tmp/ssdp721-review-release.log`). Accepted-current/public fallback/recovery unchanged and resolved from root release-state owner.
- PEM schema/publication validation: PASS, five families/zero notices (`/tmp/ssdp721-review-pem.log`). No live PEM copied into packages.
- Orchestrator generated snapshot `--check`: PASS; current source parity plus immutable 5.16/6.0–6.6/7.1 snapshots coherent (`/tmp/ssdp721-review-snapshot.log`). The accepted 6.6 resource directory has zero diff against `22f4bdba`. No frozen prior resource was hand-edited.
- `git diff --check 24518df 60b89e2`: PASS. Worktree remains clean.

Design-lead static/Q5c supplied: PASS, actual `extract_arm(60b89e2)` static run in `/tmp/ssdp721-static-60b89e2`; entry-only 15,691 B vs 16,208 B limit (517 headroom), workflow 35,998 B vs 49,864 B (13,866 headroom); Q5d 23 tests OK. This reviewer records supplied bounded static evidence, not an independently rerun campaign. Optional owner-read outside-mode size risk is explicitly declared (61,772 vs 16,208); no claim that static passes qualify live outcomes. This static result does not discharge blocker 2's every-entrypoint reduction requirement.

Root CHANGELOG has the version entry; README closeout is intentionally deferred by the authorized brief to freeze, and this development edit is not frozen. No required executed workflow check remains missing. The profile version-binding defect and audit reduction defect are not detected by passing mechanical suites and remain blocking. Recheck those exact repairs and affected acceptance before S3/Go can close; qualification/ratification gates remain separate.

## Candidate hashes

- `source/shared/fragments/scientific-checks.md`: `1c1a8ab797492640a7250709b12f3cd2c2c4453d4edfc00eec27760369282ebc`
- `source/shared/references/scientific-inspectability-and-initiative.md`: `d8f36b23e8770f7213265ee3414a4e34e46e746e391e43a837b3f5af924e9d9b`
- `qualification/ssdp70/qual-v2/frozen-minimum-mapping.json`: `9f20410194bc890a6a121a9228018e7c4ca6030d1b5d20d5b0732eab899b247c`
- `tests/test_protocol_72_scientific_checks.py`: `be51ab384177f9fb0ea96eb725593345e255893da77b127b0c0558045ee0eecd`
- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`: `edf8253e4be07ed4a15f9d31cb9492d3281d6d430087083e97ac0540969b5a96`
- `orchestrator/src/sdp_orchestrator/core/profile.py`: `1f3a06cd2891f7bfd1fe6631d91f764e28eaf8df757d141b1972891f5326396a`
