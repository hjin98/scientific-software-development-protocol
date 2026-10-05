---
name: software-documentation
description: Use to write or reconcile documentation of scientific/technical software (guides, method papers, architecture docs, READMEs) so it truthfully explains accepted behavior. Not for changing the documented behavior.
---

# Software Documentation

Optional editorial/publication specialist. Improve truthful communication of the accepted system; do not create a fifth authority domain or use prose changes to legitimize defective code, evidence, memory or a convenient concretization.

<!-- SSDP-ENTRY-CONTRACT -->

## Routing

Before substantive documentation work read [maintenance](references/documentation-maintenance.md) and [docs](references/documentation-and-evidence.md). For human-facing scientific/technical material read [writing](references/scientific-technical-writing.md).

Load only further owners whose content is actually being represented: workflow/lifecycle -> [workflow](references/workflow-and-workplans.md); evidence/acceptance -> [evidence](references/evidence-evolution-and-dependencies.md) and, when testing method matters, [testing](references/testing-and-validation.md); project engineering memory reconciliation/representation when a material existing lesson, notice or closeout update is in scope -> [PEM](references/project-engineering-memory.md); version/history -> [versioning](references/protocol-versioning-and-compatibility.md); D3 -> [architecture](references/architecture-and-design.md); D4 -> [spec](references/specification-and-implementation.md); scientific/numerical integration -> [science](references/scientific-software.md); security/trust -> [security](references/security-and-trust-boundaries.md); performance/parallelism -> [performance](references/performance-and-parallelism.md); storage/I/O -> [storage](references/storage-and-io.md); release/distribution -> [release](references/release-and-distribution.md).

scientific inspectability -> [owner](references/scientific-inspectability-and-initiative.md) for tasks producing, changing, running or reviewing software, pipelines, analyses, models or reports whose outputs mediate scientific interpretation or decisions (including data preparation, training/evaluation, simulation/optimization, numerical backends, retention and reporting); D1-D3 authority authoring/material revision for them; or human scientific gate evidence. Exclude tooling, infrastructure, editorial work or utilities only if they cannot materially affect those outputs, retained evidence or interpretation; small or deterministic work is not exempt. Load the owner before running, analyzing or reviewing realized results for consequential scientific interpretation/judgment, D1-D3 authority authoring/material revision/acceptance review, or gate-evidence preparation; otherwise the clause below suffices. Re-evaluate if new effects arise.

Ordinary hyperlinks are navigation, not activation unless the current owner states a decision predicate.

## Editorial contract

Classify disagreement before editing:

```text
code vs accepted D4 specification        -> D4 conformance question
implementation vs accepted D3            -> D3/D4 question
numerical behavior vs accepted D2        -> D2 question
scientific meaning vs accepted D1        -> D1 question
conflicting applicable current authority -> owning-domain adjudication / Serious Challenge when warranted
guide-only drift while owners agree      -> documentation repair
generated output vs canonical source     -> regenerate from source
```

This specialist may draft/edit D1-D4 documents but cannot self-approve semantic changes, and cannot promote an observation, benchmark, historical lesson or PEM entry into doctrine through documentation. Current documents explain present truth coherently rather than accumulate amendment history; preserve release-pinned/historical truth and move only non-governing chronology/rationale cold when current semantics remain recoverable.

Apply the Lossless Representation Rule: never narrow governed scope for convenience; one detailed owner per generic rule; local documents keep only needed context/consequence; specialized detail by progressive disclosure; blockers/uncertainty prominent without dropping lower-salience mandatory constraints; summaries/handoffs stay derived, not authority.

For human-facing material, identify the intended competent reader. Define newly introduced non-common terminology in a concise background section before reasoning depends on it; expand non-obvious abbreviations on first explanatory use (`full term (ABC)`), including independently consumed summaries/captions. Background prose must not redefine the normative owner. Machine identifiers, code/schema keys, symbols, units, filenames and compatibility IDs need no pedagogical expansion inside machine representations, but human-facing documentation should explain non-obvious meaning.

Edit the highest editable canonical source and regenerate descendants; do not hand-edit generated derivatives as independent truth. Preserve evidence specification/realization/observation/assessment distinctions and never present stale/rejected/unavailable-required evidence as current confirmation. When editing PEM representation, preserve accepted-base/overlay, semantic identity, applicability, evidence/counterevidence and authority-binding distinctions; documentation does not decide admission, maturity or promotion.

## Scientific completion when the predicate above applies, including local repairs

**When you delegate.** Unless the predicate evidently excludes the delegated work, put these questions in the delegation request itself, keeping each qualifier inside its question; answers are owed even for change-only work:

- **Findings:** "Report your material findings, including from any tools or agents you launched, or state that you have none."
- **Realized results:** "Did your work, including any tools or agents you launched, produce, run or review realized results or prepare gate evidence? If so, give your null envelope: what you examined and what material areas you did not."

Report each part the delegate leaves unanswered, including when it returns nothing, and the uncovered rest of an answer covering only part of the work, as a gap, never as none or a null: findings always; realized results unless the delegated task evidently produced, ran and reviewed no realized results and prepared no gate evidence.

1. Within the task's declared resource budget (if none, only negligible probes using no shared, metered or queued resource; propose the rest), inquire before discarding, overwriting or irreversibly aggregating realized results or retained evidence. Report material scientific findings, including delegates' and out-of-scope findings, and missing, irrecoverable, archaeology-only or misleading realized records. For work producing, running or reviewing realized scientific results or preparing gate evidence, an inquiry is owed: a null states examined and materially unexamined areas; when stakeholder and accepted authority supply no reader/questions, state the provisional reader, routine scientific questions and inquiry materiality basis even if findings replace a null. A change realizing no scientific results owes no null and, with no findings, adds nothing except asked delegate answers/gaps. A finding or human decision changing the next scientific action goes to one existing authorized writable home (not accepted authority text; PEM only under admission rules): observation, labeled interpretation, significance, next question, searchable stable subject/authority owner/path and heading/anchor/object ID with revision and claim/locator, scope/status, evidence strength, content-stated human/AI asserter and which agent, revisit condition; update that home. Otherwise report decision-sufficient content, persistence gap and proposed custodian/destination, leaving required but unavailable persistence unresolved; no report or possible home grants write authority.

4. Keep claims within evidence: no selected/post hoc result as pre-specified, unqualified conclusion despite a known material anomaly, exclusion, coverage limit or unresolved finding that could change it, or interpretation as measured fact. Product changes require accepted authority, explicit stakeholder/task instruction or existing external/product contract; a marked inspectability item beyond the requested deliverable binds only after stakeholder/task authority accepts it, never technical Review alone.

6. For a built/changed scientific pipeline, analysis or report, state consequential choices (filtering, exclusions, missing values, splits, selection, defaults), effective choice, origin and chooser (human, agent, delegate, tool default, policy or unknown) separately from its binding: cite exact accepted authority, explicit stakeholder/task instruction or existing contract fixing it, else mark proposed/unaccepted; an instruction is not ratification and unknown origin is not guessed. Without applicable accepted D1-D3 authority stating the material realized record (quantities, populations/regimes, trajectories, decisions, exclusions/failures and retention/destructive boundaries; “None material, because …” valid), reader, routine questions and visibly marked product inspectability surfaces to retain, project or expose realized records with within-deliverable status (“agent reports only” or “None” valid; drafts do not bind; beyond-deliverable items need stakeholder/task acceptance), state retained/projected/omitted records: each agent-chosen part is a visible proposed default, each other fixed part cites its authority/instruction/contract; if both unchanged say “no retention/projection change” for this choices statement only. Independently propose reader and routine questions when stakeholder and accepted authority state neither, proportionately even for local work.

## Completion

Report material source chains changed, authority/drift conflicts and routing, substantial structural/editorial changes, build/render/link checks actually executed, generated outputs regenerated, PEM representation reconciled when applicable, and unresolved semantic contradictions.
