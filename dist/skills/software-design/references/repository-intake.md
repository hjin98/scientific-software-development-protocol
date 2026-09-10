# Repository Intake

Own repository inspection strategy and context economy. Build enough context to make the requested decision/change safely and bound its affected behavioral, semantic and evidence surface; do not inventory the repository when ownership/impact are already clear.

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

## Affected surface

For substantial work consider only materially applicable surfaces: public API/data contracts/callers/consumers, configuration, evidence, persistence/restart, concurrency/orchestration, performance/resources, security/trust, documentation, semantic dependency/history, packaging/release, and shared transitive dependencies.

Do not create a mandatory matrix when most rows are irrelevant. Conversely, Git diff is not the behavioral surface when shared contracts propagate beyond changed files. Affected-surface expansion under existing authority is not requirement expansion and does not make current implementation mechanisms invariant.

## Dependency views and bounded census

Protocol 6.2 may use bounded Markdown semantic dependency views when ordinary links/inspection are insufficient. They are aids, not automatically complete graphs:

> Absence of an edge establishes independence only when the relevant mapped scope was explicitly reviewed complete for that exclusion.

Progressive inspection remains default. Switch to a bounded census only when the governing correctness claim is itself finite/exhaustive or bounded sibling discovery is needed for safe consolidation/removal/family closure. Bound by invariant, semantic owner, transition/lifecycle class and plausible affected chain—not the whole repository.

State the completeness basis and material blind spots of symbol/static tools, dynamic registration/configuration, generated code, external consumers and runtime-only behavior. Cross-check where those can hide material members. If the family cannot be bounded confidently, do not present a partial search as exhaustive; reconsider ownership or use broader executable/property/integration evidence appropriate to the claim. Temporary closure maps are derived coordination evidence, not permanent authority.

## Evidence applicability and history

A test file/historical result is not automatically current evidence. When reusing prior evidence, confirm its specification still targets the claim and the realization remains applicable to candidate/regime/oracle/environment. Stale pass is not confirmation; stale fail is not refutation.

Consult `history/SEMANTIC_EVOLUTION.md` only when recurrence, restoration, rejected prior approaches, or semantic lineage matters. Current owners + qualification + semantic evolution are the normal historical proof path; archived workplans stay cold unless lineage is ambiguous/unmapped/challenged.

## Existing patterns, simplification, generated artifacts

Inspect adjacent implementation before inventing a new abstraction and reuse existing ownership when clean. Do not split modules/add frameworks/reorganize unrelated areas merely because the repository could be cleaner. Refactor when it materially improves the requested change, removes a failure surface, or collapses duplicated authority/machinery. When the current concretization creates the problem, consider removal/narrowing/alteration/consolidation rather than preserving it by default.

Determine canonical source vs generated output before editing. Edit source and regenerate required descendants. When generated output is shipped/committed, validate both consumer-facing validity and source parity; do not commit transient caches/analysis data unless policy makes them durable.

## Safety

Do not delete/revert/overwrite/broadly reformat unrelated work; do not change dependencies for local convenience; do not commit secrets, machine-specific paths, transient data/caches/benchmark noise. Destructive/high-risk repository operations route to their owning Git/hygiene/security procedures rather than being inferred from intake.
