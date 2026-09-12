# Documentation Authority, Maintenance, and Evolution

Own document lifecycle, authority-state hygiene, current-vs-history separation, source-chain reconciliation, and documentation impact closure. Human-facing exposition is owned by [Scientific and technical writing](scientific-technical-writing.md); evidence/dependency/evolution semantics by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); Project Engineering Memory (PEM) semantics by [Project Engineering Memory](project-engineering-memory.md); universal representation by [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md).

## Document roles and state

Logical normative families are:

```text
D1 -> Scientific Method Paper
D2 -> Numerical & Algorithmic Method Paper
D3 -> Architecture Manual
D4 -> Specification + executable concretization
```

This is semantic ownership, not exactly four files. A domain may span coordinated files, but each material current normative claim has one owner. Guides/tutorials/runbooks/release notes/audit/benchmark reports/dependency views/history/publication outputs and `PROJECT-ENGINEERING-MEMORY.md` are not semantic authority unless a separate current owner explicitly supplies a bounded normative claim; PEM itself never becomes D1-D4 authority by document placement, repetition, temperature, count or packaging.

An authority-bearing file can contain normative claims plus rationale, evidence, pedagogy and historical commentary. Do not promote every sentence/citation/example to invariant status or declare the entire methods document non-normative when it owns accepted D1/D2 semantics.

Where ambiguity can affect governance, distinguish proposed, accepted-current, challenged, risk-accepted/provisional, stale-dependent, superseded/historical and release-pinned/publication state; human-ratification state remains orthogonal. Preserve release-pinned historical truth rather than editing it to match current terminology/science.

For PEM additionally distinguish accepted/base project memory, same-branch candidate overlay, canonical family/notice state, and derived active summary/index. A candidate overlay is not accepted merely because it is the newest file. A derived summary/index is not a second canonical memory surface.

## Reconcile before editing

Code is evidence of actual behavior, not automatic intent. Default routing:

| Observation | Route |
| --- | --- |
| owners agree; guide differs | documentation drift |
| code differs from accepted D4 specification | D4 defect unless authority changed |
| implementation differs from D3 architecture | D3/D4 conformance question |
| numerical behavior differs from accepted D2 | D2 concretization/verification question |
| scientific meaning differs from accepted D1 | D1 concretization/adequacy question |
| applicable current authorities conflict | owning-domain adjudication / Serious Challenge when warranted |
| proposed edit is used as current | authority-state defect |
| generated output differs from canonical source | regenerate source chain |
| explanatory background differs from precise owner | documentation drift or owning-domain challenge |
| stale evidence is presented as current | evidence-applicability defect |
| PEM prose/summary changes family meaning, admission, maturity, applicability, authority binding, or guidance without owning evidence/process | route to PEM + real evidence/current owner; documentation cannot self-promote |
| derived PEM summary/index differs from canonical records | regenerate/reconcile from canonical memory; never edit derivative as independent truth |

Do not repair inconsistency by rewriting upstream authority to match current code or by choosing new semantic truth editorially. Documentation edits may improve representation, terminology, navigation, background and source-chain coherence; they cannot create evidence, admit a durable project lesson, settle causality/comparative warrant, or mint an invariant.

## Current system, not patch history

Current documents should explain the accepted present system coherently. Rewrite/reorder/merge/split when conceptual structure changes instead of appending amendment/exceptions. Preserve still-valid scientific, numerical, architecture, specification, compatibility, limitation, evidence-applicability and edge-case semantics during refactor. Detailed chronology and material supersession rationale belong in release/history/semantic evolution. PEM retains only durable evidence-backed project learning likely to change future decisions, not ordinary fix chronology.

A current document may route to another supplied owner rather than repeat generic doctrine. Shared background across files is valid only when current composition is explicit and resolvable; essential meaning cannot depend on hidden chat or an unsupplied prerequisite.

If a project lesson becomes accepted generic doctrine at its real owner, reconcile duplicate active PEM guidance so memory does not remain a competing rule. Retain project-specific evidence/context only where it still changes decisions or historical understanding.

## Human-facing and source-chain maintenance

When creating/materially refactoring human-facing current material, apply the scientific-writing owner: audience-appropriate background for newly introduced non-common terminology, first-use `full term (ABC)` for non-obvious abbreviations, and explanatory definitions subordinate to precise D1-D4 owners. A human-facing PEM document/template likewise defines unfamiliar project-learning terms sufficiently for competent use while keeping schema keys/identifiers mechanically stable.

Edit the highest authoritative/canonical source and regenerate descendants. Mechanical source-chain checks establish reproducibility/integrity, not whether equations/method/architecture/evidence interpretation is correct.

For PEM, edit its one logical canonical publication root plus affected declared canonical partitions; regenerate the active summary/optional derived index from canonical records. A semantic change spanning root/partition/index must be published coherently. Never use a stale generated index to hide a canonical family or infer non-applicability.

Use bounded Markdown dependency views only when ordinary links/anchors/workplan mappings are insufficient. Current dependency views describe current relations, not history. A missing edge in a partial view is not proof of independence unless that bounded scope was explicitly reviewed complete.

Preserve concise semantic-evolution reasoning when a material model/method/architecture/concretization/evidence choice is replaced/generalized/rejected/retired/restored and future rediscovery is plausible. Current owners explain what; PEM summarizes bounded evidence-backed project learning; history explains why; Git preserves detailed chronology. Resolved Challenge rationale should be only the concise material reasoning needed to prevent recurrence, not a debate transcript/database.

## Documentation impact closure

A local code refactor with no contract/explanation/evidence-applicability/project-learning impact need not trigger broad documentation work. A material authority change must reconcile its current normative owner plus materially affected explanation/navigation, evidence/dependency records, authority-bound PEM capabilities/notices, and semantic history.

A material PEM semantic update must preserve stable family identity/lineage, applicability/counterevidence, immutable observation vs assessment, evidence/authority bindings, coverage/aggregation/project scope, current guidance and cold reachability while refreshing only affected human-facing/derived views. Schema changes are protocol changes, not editorial refactors.

Apply the Lossless Representation Rule: governed scope cannot be narrowed for editorial convenience; one detailed generic owner; local consequence + precise route; importance-weighted presentation without dropping mandatory constraints; history cold but discoverable; no append-only revision replay. `software-documentation` is support, never an approval gate.
