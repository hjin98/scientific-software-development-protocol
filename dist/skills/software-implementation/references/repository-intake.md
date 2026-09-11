# Repository Intake

Own repository inspection strategy and context economy. Build enough context to make the requested decision/change safely and bound its affected behavioral, semantic, evidence, and when triggered Project Engineering Memory (PEM) surface; do not inventory the repository when ownership/impact are already clear.

## Evidence-directed inspection

Start with repository instructions, requested entry point/module/feature, owning authority/docs, callers/consumers, persisted state and relevant tests/evidence. Expand into build/CI/configuration/security/release/concurrency/performance or other concerns only when the affected chain enters them. Preserve unrelated user/concurrent work.

Choose the lowest-cost next read/search/semantic query/test/benchmark that most strongly resolves a material uncertainty or establishes required evidence:

- prefer targeted symbol/search/range inspection before loading an entire large file when sufficient;
- reuse already-established repository facts while their protocol/source/workplan/candidate/regime/scope remains applicable; re-read when exact wording/new evidence makes it necessary;
- prefer discriminating evidence over broad speculative reconnaissance;
- expand through plausible ownership/dependency/contract/evidence/behavior chains, not file adjacency;
- keep full large outputs available when useful but bring only the smallest sufficient failing/decision region into active context; never hide material warnings/failures;
- combine related read-only queries when it reduces turns without obscuring evidence.

Context economy never permits omission of required affected behavior, failure evidence, or plausible transitive impact. Apply the universal Lossless Representation Rule to active context as well as written output.

## Conditional project-memory intake

PEM is not a universal intake step. Activate it under the predicates owned by [Workflow and workplans](workflow-and-workplans.md): substantial mature rework/replacement, suspected recurrence, substantial optimization/scaling, migration/recovery/revert/restoration where prior choices matter, or an active workplan that explicitly binds relevant project learning. Mere presence of `PROJECT-ENGINEERING-MEMORY.md`, a repository with long history, or a first clean local defect does not justify eager memory/history preparation.

When triggered, use progressive disclosure:

```text
resolve accepted/base memory + explicit candidate overlay
 -> validate schema/publication state
 -> read active summary
 -> search canonical family/notice metadata for affected owner/mechanism/regime/applicability cues
 -> construct/refresh Historical Applicability Set (HAS)
 -> open matched family/detail rows
 -> follow raw evidence/history only where needed
```

Temperature and active-summary presence are salience aids, never the applicability search boundary. A relevant `COLD`, `UNASSESSED`, review-required, or summary-omitted canonical entry remains reachable. Conversely, a `HOT` entry outside the current semantic owner/mechanism/regime is not applicable merely because it is prominent.

Missing/partial/unsupported/corrupt memory, stale derived index, stale applicability tags, absent dependency edges, or an advanced `reconciled_through` watermark cannot prove no relevant lesson exists. Use bounded historical intake over the affected project scope where the decision needs stronger exclusion; otherwise preserve explicit uncertainty/`REVIEW_REQUIRED`. Do not turn that fallback into mandatory full-repository archaeology.

For established projects first adopting PEM, historical backfill may be bounded by the material affected scope and declared coverage basis rather than exhaustive global reconstruction. Report blind spots honestly; partial coverage is a first-class state.

## Affected surface

For substantial work consider only materially applicable surfaces: public API/data contracts/callers/consumers, configuration, evidence, persistence/restart, concurrency/orchestration, performance/resources, security/trust, documentation, project engineering memory/HAS when triggered, semantic dependency/history, packaging/release, and shared transitive dependencies.

Do not create a mandatory matrix when most rows are irrelevant. Conversely, Git diff is not the behavioral surface when shared contracts propagate beyond changed files. Affected-surface expansion under existing authority is not requirement expansion and does not make current implementation mechanisms invariant.

## Dependency views and bounded census

Protocol 6.3 may use bounded Markdown semantic dependency views when ordinary links/inspection are insufficient. They are aids, not automatically complete graphs:

> Absence of an edge establishes independence only when the relevant mapped scope was explicitly reviewed complete for that exclusion.

Progressive inspection remains default. Switch to a bounded census only when the governing correctness claim is itself finite/exhaustive or bounded sibling discovery is needed for safe consolidation/removal/family closure. Bound by invariant, semantic owner, transition/lifecycle class and plausible affected chain—not the whole repository.

State the completeness basis and material blind spots of symbol/static tools, dynamic registration/configuration, generated code, external consumers and runtime-only behavior. Cross-check where those can hide material members. If the family cannot be bounded confidently, do not present a partial search as exhaustive; reconsider ownership or use broader executable/property/integration evidence appropriate to the claim. Temporary closure maps are derived coordination evidence, not permanent authority.

A PEM canonical family/partition/index is likewise a bounded representation, not proof the repository has no other relevant history unless its declared coverage truly supports that exclusion. Prefer canonical metadata and project-local search to proportional loading of raw historical corpus as it grows.

## Evidence applicability and history

A test file/historical result is not automatically current evidence. When reusing prior evidence, confirm its specification still targets the claim and the realization remains applicable to candidate/regime/oracle/environment. Stale pass is not confirmation; stale fail is not refutation.

Consult `history/SEMANTIC_EVOLUTION.md` only when recurrence, restoration, rejected prior approaches, semantic lineage, or a PEM applicability/counterevidence question requires it. Current owners + qualification + semantic evolution + project memory are complementary: current owners define what is true, evidence establishes bounded observations/assessments, PEM summarizes reusable local lessons, semantic history explains material changes, and Git preserves chronology. Archived workplans stay cold unless lineage/evidence is ambiguous, unmapped, challenged, or explicitly needed for bounded backfill.

For positive-pattern admission or material strengthening, search bounded applicable unfavorable/neutral/inconclusive history as well as favorable episodes. For failure recurrence, distinguish one causal episode with many manifestations from genuinely independent reintroduction after an accepted repair. Do not use commit count, issue count, or grep hits as recurrence/application count without causal/application-episode reconciliation.

## Existing patterns, simplification, generated artifacts

Inspect adjacent implementation before inventing a new abstraction and reuse existing ownership when clean. Do not split modules/add frameworks/reorganize unrelated areas merely because the repository could be cleaner. Refactor when it materially improves the requested change, removes a failure surface, or collapses duplicated authority/machinery. When the current concretization creates the problem, consider removal/narrowing/alteration/consolidation rather than preserving it by default.

A project memory pattern is a design prior, not an instruction to copy the old implementation. Recover the bounded learned capability/cause and current authority binding, then choose the simplest current concretization. Evidence-only historical machinery remains replaceable.

Determine canonical source vs generated output before editing. Edit source and regenerate required descendants. When generated output is shipped/committed, validate both consumer-facing validity and source parity; do not commit transient caches/analysis data unless policy makes them durable. A live project PEM is project state, not a generated generic skill/profile asset and must not be copied into portable packages.

## Safety

Do not delete/revert/overwrite/broadly reformat unrelated work; do not change dependencies for local convenience; do not commit secrets, machine-specific paths, transient data/caches/benchmark noise, or sensitive evidence into PEM. Destructive/high-risk repository operations route to their owning Git/hygiene/security procedures rather than being inferred from intake.
