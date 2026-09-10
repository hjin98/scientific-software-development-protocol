# Documentation Authority, Maintenance, and Evolution

Documentation is both semantic authority and explanatory/publication material. The first task is to identify which role a document is playing.

Read [Scientific and technical writing](scientific-technical-writing.md) for Protocol 6.1 human-facing background/terminology and abbreviation standards. Read [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for dependency/history/evidence applicability.

## Background and terminology

Protocol 6.1 uses **concretization** for downstream scientific/software expression of an abstraction. **Evidence realization** means one concrete execution of an evidence specification. Current documentation should keep those relations distinct.

## Four logical normative document families

Protocol 6.1 maps the semantic domains to logical current-state owners:

```text
D1 -> Scientific Method Paper family
D2 -> Numerical & Algorithmic Method Paper family
D3 -> Architecture Manual family
D4 -> Specification + code/executable concretization
```

This is logical one-to-one semantic ownership, not a requirement for exactly four physical files. A domain may use several coordinated files, but each material current normative claim has exactly one semantic owner. A concretization may still be constrained by multiple applicable claims from different owners.

Generic guides, tutorials, runbooks, release notes, audit reports, benchmark reports, dependency views, semantic-evolution histories, and publication outputs do not become semantic authority unless explicitly assigned an authority scope.

`software-documentation` may edit, synthesize, publish, and reconcile documentation, but it does not self-approve D1/D2/D3/D4 semantic changes.

## Normative core versus supporting prose

A method paper is not uniformly normative merely because the file is authoritative. Distinguish:

- accepted normative semantic claims;
- rationale and design explanation;
- literature/evidence/provenance;
- pedagogy/examples;
- historical commentary.

Do not let a citation, example, background definition, or explanatory sentence accidentally acquire invariant status. Conversely, do not label the whole methods document non-normative when it is the accepted D1/D2 owner.

## Authority states

Documents that can carry semantic authority must distinguish state enough to prevent speculative edits from becoming current accidentally:

- proposed;
- accepted current;
- challenged;
- risk-accepted/provisional when applicable;
- stale dependent;
- superseded/historical;
- release-pinned/publication snapshot.

Exact metadata syntax is project-local. Human-ratification state is orthogonal.

Current normative mutation is atomic: draft proposed changes separately or clearly as proposed, review/falsify them, obtain required ratification, then accept/update the current owner and invalidate only materially dependent descendants/evidence.

Do not edit a release-pinned/publication snapshot to track later current science or terminology; preserve publication truth and create/update the current authority separately.

## Reconcile disagreement before editing

Code is evidence of actual behavior, not automatic intent. Classify discrepancies:

| Observation | Default route |
| --- | --- |
| code and accepted D4 spec agree; guide differs | documentation drift |
| code differs from accepted D4 spec | D4 implementation defect unless authority evidence says otherwise |
| implementation structure differs from accepted D3 manual | D3/D4 conformance question |
| D2 paper and implemented numerical semantics differ | D2/D3/D4 concretization/verification question |
| D1 paper and numerical method encode different scientific meaning | D1/D2 concretization/verification question |
| two applicable current authorities conflict | Serious Challenge / owning-authority adjudication |
| proposed edit is being used as current authority | authority-state defect |
| generated output differs from its canonical source | generated-artifact drift |
| explanatory background conflicts with the precise normative definition | documentation drift or owning-domain challenge, depending on which side is wrong |
| stale evidence is presented as current confirmation/refutation | evidence-applicability defect |

Do not repair inconsistency by rewriting every upstream document to match the current code or by redefining scientific/numerical terms editorially.

## Human-facing background and abbreviation maintenance

When creating or materially refactoring a human-facing current artifact:

- identify the intended competent reader when needed to judge assumed background;
- define newly introduced non-common domain terminology with a short explanation in an explicit background section before substantive use;
- expand non-obvious abbreviations at first explanatory use as `full term (ABC)`;
- check independently consumable summaries/captions when they may be read without the body;
- keep explanatory definitions subordinate to precise D1/D2/D3/D4 normative owners;
- avoid universal glossary/acronym registries or mechanical gates when ordinary editorial review is sufficient.

A shared background across several files is valid only when the current composition is explicit and supplied together. Current documents must not require hidden chat to decode essential terminology.

## Current system, not patch history

Current documents describe the accepted present system coherently. Avoid append-only narratives of amendments/exceptions. When the conceptual model changes materially, rewrite/reorder/merge/split sections so a competent reader can understand the current state without mentally applying patch history.

Preserve still-valid subtle scientific, numerical, architectural, specification, compatibility, limitation, evidence-applicability, and edge-case content during major editorial refactors. Chronology and material supersession rationale belong in release/history or semantic-evolution material.

## Dependency views and semantic evolution history

Use bounded Markdown dependency records only when existing links/anchors/workplan mappings are insufficient for reliable impact reasoning. The current view describes current materially relevant relationships; do not retain obsolete edges merely for history.

A missing edge in a partial view is not evidence of independence unless the mapped scope was explicitly reviewed as complete for that exclusion.

Preserve concise semantic-evolution reasoning when material model/algorithm/architecture/concretization/evidence replacement, generalization, rejection, retirement, or restoration is likely to recur or matter to later reviewers. History explains why current authority exists; current normative documents remain sufficient to explain what is true now.

## Source chains and generated outputs

Edit the highest authoritative source and regenerate descendants:

```text
canonical source -> assembled markdown / diagrams / PDF / site / packaged skill
```

Do not independently patch a generated descendant when an upstream source exists. Mechanical checks may fail source-chain integrity; they cannot determine that a scientific equation, estimator, architecture, or evidence interpretation is semantically correct.

## Guides and operational documentation

Guides translate accepted authority into task-oriented use. Prefer the current supported workflow, explicit inputs/outputs, result interpretation, common failures, and links to the owning D1-D4 authority. Introduce project/domain terminology before operational steps rely on it. Compatibility/history detail follows only where materially needed.

Runbooks must state whether they are current or release-pinned. Do not blindly change version strings or later terminology in a pinned runbook.

## Documentation impact and impact closure

A code-only local refactor with no contract/explanation/evidence-applicability impact need not trigger broad documentation work. A material D1/D2/D3/D4 authority change must reconcile its normative owner and materially affected explanations/navigation, evidence/dependency records, and semantic history when triggered.

Use `software-documentation` for substantial synthesis/publication, not as a mandatory approval gate. Closeout verifies required documentation/dependency/history updates but does not invent scientific/product truth.

## Resolved Serious Challenge rationale

When a serious challenge is rejected with satisfactory reasoning and recurrence is plausible, preserve only the concise challenged claim/scope, resolution state, and material reasoning needed for future reviewers to understand why the apparent contradiction is not a defect. Do not store full debate transcripts or create a challenge database.
