# Engineering Documentation and Evidence

Documentation serves two different purposes: some documents are accepted semantic authority, while others explain, operate, publish, or evidence that authority. Do not conflate them.

## Current semantic owners

Protocol 6 recognizes logical normative families:

- D1 Scientific Method Paper;
- D2 Numerical & Algorithmic Method Paper;
- D3 Architecture Manual;
- D4 Specification (with code/executable as realization/evidence).

Each material current claim has one semantic owner, though a realization may be constrained by many applicable authorities. An authority-bearing file can also contain non-normative rationale/evidence/pedagogy; scoped ownership matters more than file-wide labels.

Guides, runbooks, release notes, audit reports, benchmarks, test logs, workplans, and publication outputs are non-authoritative unless explicitly assigned a semantic scope. Workplans can carry proposed/cycle-scoped authority but do not silently supersede accepted-current domain documents.

## Evidence does not become truth by packaging

Tests, command output, benchmarks, CI, experiments, proofs, literature, and runtime observations are normally sufficient evidence in their native form. Summarize only metadata needed to interpret a material claim. Do not create evidence capsules, manifests, hashes, timestamps, or report schemas merely because they can be generated.

Never edit/select evidence to manufacture completion.

## Current authority must be reconstructable

A current normative artifact set must be semantically complete for its scope without hidden chat, unsupplied external resources, or superseded history. Explicit current cross-document composition is valid; this does not require copying every invariant into one file.

Distinguish proposed, accepted current, challenged, stale dependent, superseded/historical, and release-pinned/publication states where ambiguity could affect governance.

## Documentation specialist boundary

`software-documentation` is an editorial/publication/reconciliation specialist. It may improve structure, synthesize explanations, maintain guides, and regenerate derived outputs. It does not independently approve D1/D2/D3/D4 semantic mutations.

If documentation work discovers a semantic contradiction, route it to the owning authority rather than choosing the convenient side.

## Generated formats

Prefer editable canonical source and regenerate derived Markdown/PDF/site/diagram/package outputs. Do not independently patch a generated descendant when its source exists. Mechanical source-chain checks can establish reproducibility/integrity; they cannot decide whether an equation, estimator, architecture, or specification is semantically correct.

Generate/track derived formats only when the project actually ships or needs them.

## Cleanup and history

Current documents describe the accepted present system coherently. Move chronology to history/release notes; preserve release-pinned publication truth. Remove obsolete duplicate current documents and stale generated artifacts when they no longer own information, subject to repository policy.

Do not create an archive hierarchy solely to avoid deciding which artifact is current.