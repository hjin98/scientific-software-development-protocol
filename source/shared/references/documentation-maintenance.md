# Documentation Authority, Maintenance, and Evolution

Own document lifecycle, authority-state hygiene, current-vs-history separation, source-chain reconciliation, and documentation impact closure. Human-facing exposition is owned by [Scientific and technical writing](scientific-technical-writing.md); evidence/dependency/evolution semantics by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); universal representation by [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md).

## Document roles and state

Logical normative families are:

```text
D1 -> Scientific Method Paper
D2 -> Numerical & Algorithmic Method Paper
D3 -> Architecture Manual
D4 -> Specification + executable concretization
```

This is semantic ownership, not exactly four files. A domain may span coordinated files, but each material current normative claim has one owner. Guides/tutorials/runbooks/release notes/audit/benchmark reports/dependency views/history/publication outputs are not semantic authority unless explicitly assigned a bounded scope.

An authority-bearing file can contain normative claims plus rationale, evidence, pedagogy and historical commentary. Do not promote every sentence/citation/example to invariant status or declare the entire methods document non-normative when it owns accepted D1/D2 semantics.

Where ambiguity can affect governance, distinguish proposed, accepted-current, challenged, risk-accepted/provisional, stale-dependent, superseded/historical and release-pinned/publication state; human-ratification state remains orthogonal. Preserve release-pinned historical truth rather than editing it to match current terminology/science.

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

Do not repair inconsistency by rewriting upstream authority to match current code or by choosing new semantic truth editorially.

## Current system, not patch history

Current documents should explain the accepted present system coherently. Rewrite/reorder/merge/split when conceptual structure changes instead of appending amendment/exceptions. Preserve still-valid scientific, numerical, architecture, specification, compatibility, limitation, evidence-applicability and edge-case semantics during refactor. Detailed chronology and material supersession rationale belong in release/history/semantic evolution.

A current document may route to another supplied owner rather than repeat generic doctrine. Shared background across files is valid only when current composition is explicit and resolvable; essential meaning cannot depend on hidden chat or an unsupplied prerequisite.

## Human-facing and source-chain maintenance

When creating/materially refactoring human-facing current material, apply the scientific-writing owner: audience-appropriate background for newly introduced non-common terminology, first-use `full term (ABC)` for non-obvious abbreviations, and explanatory definitions subordinate to precise D1-D4 owners.

Edit the highest authoritative source and regenerate descendants. Mechanical source-chain checks establish reproducibility/integrity, not whether equations/method/architecture/evidence interpretation is correct.

Use bounded Markdown dependency views only when ordinary links/anchors/workplan mappings are insufficient. Current dependency views describe current relations, not history. A missing edge in a partial view is not proof of independence unless that bounded scope was explicitly reviewed complete.

Preserve concise semantic-evolution reasoning when a material model/method/architecture/concretization/evidence choice is replaced/generalized/rejected/retired/restored and future rediscovery is plausible. Current owners explain what; history explains why; Git preserves detailed chronology. Resolved Challenge rationale should be only the concise material reasoning needed to prevent recurrence, not a debate transcript/database.

## Documentation impact closure

A local code refactor with no contract/explanation/evidence-applicability impact need not trigger broad documentation work. A material authority change must reconcile its current normative owner plus materially affected explanation/navigation, evidence/dependency records and semantic history.

Apply the Lossless Representation Rule: governed scope cannot be narrowed for editorial convenience; one detailed generic owner; local consequence + precise route; importance-weighted presentation without dropping mandatory constraints; history cold but discoverable; no append-only revision replay. `software-documentation` is support, never an approval gate.
