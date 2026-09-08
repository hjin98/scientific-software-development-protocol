# Documentation Authority, Maintenance, and Evolution

Documentation is both semantic authority and explanatory/publication material. The first task is to identify which role a document is playing.

## Four logical normative document families

Protocol 6 maps the semantic domains to logical current-state owners:

```text
D1 -> Scientific Method Paper family
D2 -> Numerical & Algorithmic Method Paper family
D3 -> Architecture Manual family
D4 -> Specification + code/executable realization
```

This is logical one-to-one semantic ownership, not a requirement for exactly four physical files. A domain may use several coordinated files, but each material current normative claim has exactly one semantic owner. A realization may still be constrained by multiple applicable claims from different owners.

Generic guides, tutorials, runbooks, release notes, audit reports, benchmark reports, and publication outputs do not become semantic authority unless explicitly assigned an authority scope.

`software-documentation` may edit, synthesize, publish, and reconcile documentation, but it does not self-approve D1/D2/D3/D4 semantic changes.

## Normative core versus supporting prose

A method paper is not uniformly normative merely because the file is authoritative. Distinguish:

- accepted normative semantic claims;
- rationale and design explanation;
- literature/evidence/provenance;
- pedagogy/examples;
- historical commentary.

Do not let a citation, example, or explanatory sentence accidentally acquire invariant status. Conversely, do not label the whole methods document non-normative when it is the accepted D1/D2 owner.

## Authority states

Documents that can carry semantic authority must distinguish state enough to prevent speculative edits from becoming current accidentally:

- proposed;
- accepted current;
- challenged;
- stale dependent;
- superseded/historical;
- release-pinned/publication snapshot.

Exact metadata syntax is project-local. Human-ratification state is orthogonal.

Current normative mutation is atomic: draft proposed changes separately or clearly as proposed, review/falsify them, obtain required ratification, then accept/update the current owner and invalidate only dependent descendants/evidence.

Do not edit a release-pinned/publication snapshot to track later current science; preserve publication truth and create/update the current authority separately.

## Reconcile disagreement before editing

Code is evidence of actual behavior, not automatic intent. Classify discrepancies:

| Observation | Default route |
| --- | --- |
| code and accepted D4 spec agree; guide differs | documentation drift |
| code differs from accepted D4 spec | D4 implementation defect unless authority evidence says otherwise |
| architecture implementation differs from accepted D3 manual | D3/D4 conformance question |
| D2 paper and implemented numerical semantics differ | D2/D3/D4 verification question |
| D1 paper and numerical method encode different scientific meaning | D1/D2 verification question |
| two applicable current authorities conflict | Serious Challenge / owning-authority adjudication |
| proposed edit is being used as current authority | authority-state defect |
| generated output differs from its canonical source | generated-artifact drift |

Do not repair inconsistency by rewriting every upstream document to match the current code.

## Current system, not patch history

Current documents describe the accepted present system coherently. Avoid append-only narratives of amendments/exceptions. When the conceptual model changes materially, rewrite/reorder/merge/split sections so a competent reader can understand the current state without mentally applying patch history.

Preserve still-valid subtle scientific, numerical, architectural, specification, compatibility, limitation, and edge-case content during major editorial refactors. Chronology belongs in release/history material.

## Source chains and generated outputs

Edit the highest authoritative source and regenerate descendants:

```text
canonical source -> assembled markdown / diagrams / PDF / site
```

Do not independently patch a generated descendant when an upstream source exists. Mechanical checks may fail source-chain integrity; they cannot determine that a scientific equation, estimator, or architecture is semantically correct.

## Guides and operational documentation

Guides translate accepted authority into task-oriented use. Prefer the current supported workflow, explicit inputs/outputs, result interpretation, common failures, and links to the owning D1-D4 authority. Compatibility/history detail follows only where materially needed.

Runbooks must state whether they are current or release-pinned. Do not blindly change version strings in a pinned runbook.

## Documentation impact

A code-only local refactor with no contract/explanation impact need not trigger broad documentation work. A material D1/D2/D3/D4 authority change must reconcile its normative owner and materially affected explanations/navigation. Use `software-documentation` for substantial synthesis/publication, not as a mandatory approval gate.

## Resolved Serious Challenge rationale

When a serious challenge is rejected with satisfactory reasoning and recurrence is plausible, preserve only the concise challenged claim/scope, resolution state, and material reasoning needed for future reviewers to understand why the apparent contradiction is not a defect. Do not store full debate transcripts or create a challenge database.