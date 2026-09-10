# Serena: Semantic Repository Intelligence and Bounded Editing

Use Serena primarily for semantic repository intake, navigation, reference discovery, and bounded symbol-level editing when the active backend can model the relation.

## Selection boundary

Prefer Serena over repeated textual search when the material question is semantic rather than lexical: locating the implementation owner or definition of a symbol, discovering callers/references/implementations, learning a large file through bounded symbol overviews, following affected symbol chains, or applying a symbol-level edit whose semantic unit matches the intended change.

Literal strings, filenames, configuration, generated/external surfaces, runtime registration, and unsupported language constructs remain ordinary-search territory or required cross-check surfaces.

When a Serena-class question is triggered, read this method before relying solely on Grep/Read-style defaults. If Serena availability is not already known, perform a cheap non-mutating availability/capability probe when the host exposes one. When available/current/supported and directly suited to the relation, presumptively use Serena; use a concrete fallback only when the backend cannot establish the relation reliably or another already-available mechanism establishes the same claim at least as reliably and more cheaply.

## Semantic intake and navigation

- Prefer symbol overviews and targeted symbol lookup when learning a large file or locating an implementation owner.
- Use symbol-reference/caller queries to follow dependency and affected-surface chains when the active backend can model them.
- Retrieve only the bodies/signatures needed for the current question when bounded semantic retrieval is sufficient.
- **Cross-check semantic results** with text search, configuration, documentation, generated-source inspection, or runtime evidence when dynamic dispatch, reflection, runtime registration, strings, external consumers, unsupported languages, or generated code can hide dependencies.

Serena **backends and languages expose different capabilities**. Do not assume dependency search, implementations, type hierarchy, refactoring, diagnostics, or other semantic operations merely because Serena is present. Use the capabilities actually exposed by the configured client/backend. If a needed semantic operation is unavailable or unreliable, fall back to ordinary repository tools without changing the required engineering claim.

If branch changes, external edits, generated files, or other mutations make semantic results stale or inconsistent, resynchronize or restart the semantic backend when supported before relying on it again. A stale index is a concrete fallback reason only when it cannot be refreshed economically enough for the current material question.

## Symbol-level editing and mutation safety

Before replacing or extending a symbol, inspect its current body plus enough surrounding/import/decorator/context state to understand the actual edit boundary. Use a symbol-level edit only when the semantic unit matches the required change and the target is authoritative source rather than generated output or another derivative.

After a write, inspect the current file or repository diff. Successful tool execution is not correctness evidence by itself.

A failed, interrupted, or timed-out write-capable call creates an **ambiguous repository state**. Do not assume no mutation occurred. **Inspect current file/diff/status before retrying** or applying an alternative edit so duplicate or conflicting changes are not introduced.

## Memories and indexes

Treat Serena indexes, onboarding memories, and ordinary project memories as **derived/advisory context by default**. Stale or conflicting memory yields to current source and accepted authority.

Memory may summarize stable, non-obvious repository conventions when project policy permits and doing so materially reduces rediscovery. Do not hide one-off task notes, volatile line-level details, workplan obligations, acceptance evidence, or other still-binding semantics there.

A project may **explicitly promote** a selected human-reviewed Serena memory/document into governed current documentation. Promotion is explicit rather than inferred from `.serena/` location. Once promoted, the file follows the same documentation authority, versioning/supply, and snapshot-completeness rules as any other governed document.

Do not require committing `.serena` or Serena-generated state. Generated local state follows repository ignore policy unless the project deliberately governs selected files.

## Evidence boundary

Serena is semantic-navigation evidence, not an exhaustive affected-surface proof. Re-derive affected behavior from the assembled candidate and cross-check blind spots where material. Serena does not replace focused tests, affected regression, real-boundary integration, structural analysis when syntax-level completeness is the claim, or project-required analyzers.
