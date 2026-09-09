# Engineering Documentation and Evidence

Documentation serves two different purposes: some documents are accepted semantic authority, while others explain, operate, publish, or evidence that authority. Do not conflate them.

Read [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md) for evidence specification/realization/observation, stale-evidence, dependency, and semantic-history doctrine. Read [Scientific and technical writing](scientific-technical-writing.md) for human-facing background/terminology and first-use abbreviation requirements.

## Background and terminology

Protocol 6.1 distinguishes **concretization** (a downstream scientific/software expression of an abstraction) from **evidence realization** (one concrete execution of an evidence specification). Evidence is support/challenge material for governed claims; it is not a fifth semantic authority.

## Current semantic owners

Protocol 6.1 recognizes logical normative families:

- D1 Scientific Method Paper;
- D2 Numerical & Algorithmic Method Paper;
- D3 Architecture Manual;
- D4 Specification (with code/executable as actual concretization/evidence of behavior).

Each material current claim has one semantic owner, though a concretization may be constrained by many applicable authorities. An authority-bearing file can also contain non-normative rationale/evidence/pedagogy; scoped ownership matters more than file-wide labels.

Guides, runbooks, release notes, audit reports, benchmarks, test logs, workplans, semantic-dependency views, evolution histories, and publication outputs are non-authoritative unless explicitly assigned a semantic scope. Workplans can carry proposed/cycle-scoped authority but do not silently supersede accepted-current domain documents.

## Evidence does not become truth by packaging

Tests, command output, benchmarks, continuous integration (CI), experiments, proofs, literature, and runtime observations are normally sufficient evidence in their native form. Summarize only metadata needed to interpret a material claim. Do not create evidence capsules, manifests, hashes, timestamps, or report schemas merely because they can be generated.

Never edit/select evidence to manufacture completion.

Keep separate, where material:

```text
evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

A rerun against a changed candidate creates a new evidence realization. A prior result does not silently become evidence for a new subject revision.

## Evidence applicability and stale documentation

Evidence and documentation have validity/applicability domains. A passing historical test that no longer interrogates the current claim or current semantic owner is not current confirmation. A failing stale test is not current refutation either.

When authority or a material concretization changes, reconcile materially dependent tests/evidence, explanatory documentation, current dependency records, and semantic-history obligations. Preserve unaffected evidence and documentation rather than invalidating everything indiscriminately.

## Current authority must be reconstructable

A current normative artifact set must be semantically complete for its scope without hidden chat, unsupplied external resources, or superseded history. Explicit current cross-document composition is valid; this does not require copying every invariant into one file.

Distinguish proposed, accepted current, challenged, risk-accepted/provisional, stale dependent, superseded/historical, and release-pinned/publication states where ambiguity could affect governance.

A historical semantic-evolution record may explain why current authority exists but must not be required to reconstruct what is currently true.

## Human-facing comprehension

Human-facing current documentation must introduce newly appearing non-common domain terminology for its intended competent reader before relying on it in substantive reasoning. Use a concise `Background`, `Background and terminology`, or equivalent section. Expand non-obvious abbreviations at first explanatory use with `full term (ABC)`.

A reader-friendly background explanation does not replace a precise normative definition owned by D1/D2/D3/D4. If explanatory and normative meanings disagree materially, route the disagreement to the owning domain.

Machine-facing JSON fields, code identifiers, symbols, filenames, and other opaque values need not contain pedagogical prose themselves; their human-facing reference/schema documentation must explain non-obvious meaning.

## Documentation specialist boundary

`software-documentation` is an editorial/publication/reconciliation specialist. It may improve structure, synthesize explanations, maintain guides, dependency/history support artifacts, and regenerate derived outputs. It does not independently approve D1/D2/D3/D4 semantic mutations.

If documentation work discovers a semantic contradiction, route it to the owning authority rather than choosing the convenient side.

## Generated formats

Prefer editable canonical source and regenerate derived Markdown/PDF/site/diagram/package outputs. Do not independently patch a generated descendant when its source exists. Mechanical source-chain checks can establish reproducibility/integrity; they cannot decide whether an equation, estimator, architecture, specification, or evidence interpretation is semantically correct.

Generate/track derived formats only when the project actually ships or needs them.

## Dependency and evolution support artifacts

Use existing anchors, document links, workplan mappings, and profile metadata before adding a separate semantic dependency record. Add/maintain a bounded Markdown view only when it materially reduces ambiguity, invalidation risk, rediscovery, or stale-evidence confusion.

A partial dependency view is not proof of non-dependency: absence of an edge proves independence only when the relevant scope was explicitly reviewed as complete for that exclusion.

Semantic evolution history should preserve concise reasons for material model/algorithm/architecture/concretization/evidence replacement, generalization, rejection, retirement, or restoration when future rediscovery is plausible. Git remains detailed chronology; history explains why; current normative documents explain what is true now.

## Cleanup and history

Current documents describe the accepted present system coherently. Move chronology to history/release notes/semantic-evolution records; preserve release-pinned publication truth. Remove obsolete duplicate current documents, stale evidence specifications, superseded concretizations, and stale generated artifacts when they no longer own/support a current or explicit compatibility/forensic role.

Do not create an archive hierarchy, evidence database, or documentation approval system solely to avoid deciding which artifact is current.
