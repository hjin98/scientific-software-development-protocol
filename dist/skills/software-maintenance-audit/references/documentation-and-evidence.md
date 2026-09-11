# Engineering Documentation and Evidence

Own how engineering documents and evidence are **communicated and composed**, not the underlying D1-D4 truth. Some documents carry accepted semantic authority; others explain, operate, publish, coordinate, or evidence it. Distinguish those roles explicitly.

Evidence lifecycle/applicability/dependency/evolution is owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); human-facing exposition by [Scientific and technical writing](scientific-technical-writing.md); document lifecycle/current-vs-history by [Documentation maintenance](documentation-maintenance.md); universal authority/representation rules by [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md).

## Authority-aware documentation

Logical normative families are D1 Scientific Method Paper, D2 Numerical & Algorithmic Method Paper, D3 Architecture Manual, and D4 Specification (with code/executable as actual concretization/evidence of behavior). One physical file may mix normative claims with rationale/evidence/pedagogy; scoped semantic ownership matters more than file labels.

Guides, runbooks, release notes, audit/benchmark/qualification reports, test logs, dependency views, semantic history, workplans and publication outputs are non-authoritative except for any explicit bounded authority they actually carry. Workplans may freeze proposed/cycle-scoped decisions but do not silently supersede accepted-current domain owners.

When ambiguity matters, distinguish proposed, accepted-current, challenged, risk-accepted/provisional, stale-dependent, superseded/historical and release-pinned/publication state.

## Evidence communication

Native tests/CI/benchmarks/experiments/proofs/literature/runtime output are normally sufficient evidence when they retain the identity needed to interpret the claim. Do not manufacture capsules/manifests/hashes/report schemas merely because they can be generated.

When evidence lifecycle matters preserve the distinction:

```text
evidence specification -> evidence realization -> observation -> evidence assessment
```

Summaries may keep raw detail cold but must retain material provenance/applicability, failures, warnings, contradictory admissible evidence, unavailable required checks and uncertainty. A stale pass is not current confirmation; a stale fail is not current refutation. Never select/edit evidence to manufacture completion.

## Current authority and composition

A current normative artifact set must be complete for its governed scope without hidden chat or unavailable history. Explicit cross-document composition is valid and preferable to duplicating every generic invariant. A historical evolution record may explain why current authority exists but must not be required to reconstruct what is true now.

When authority/concretization changes, reconcile materially dependent explanatory docs, tests/evidence, current dependency views and semantic history; preserve unaffected material rather than invalidating everything.

## Human-facing comprehension

Human-facing current documentation must introduce newly appearing non-common domain terminology for its intended competent reader before substantive reasoning depends on it, normally in a concise `Background`/`Background and terminology` section. Expand non-obvious abbreviations at first explanatory use (`full term (ABC)`). A friendly background definition does not replace the precise D1-D4 owner; material disagreement routes to that owner.

Machine fields/code identifiers/symbols/filenames/compatibility IDs need not contain pedagogical prose internally, but their human-facing reference should explain non-obvious meaning.

## Generated/source-chain discipline

Edit the highest canonical source and regenerate descendants. Do not independently patch generated Markdown/PDF/site/diagram/package/profile output when source exists. Mechanical parity proves source-chain integrity, not scientific/numerical/architectural correctness. Track/generated formats only when the supported product/repository needs them.

Use bounded dependency/history support artifacts only when they materially reduce ambiguity, invalidation risk or rediscovery. A partial dependency view is not proof of non-dependency unless its relevant scope was explicitly reviewed complete.

## Representation consequence

Apply the Lossless Representation Rule to every document/evidence summary: preserve complete governed meaning first; state generic doctrine once at its canonical owner; communicate only the local delta plus resolvable routes; lead with disposition/Challenge/blockers/current decisions and material uncertainty; keep raw evidence, chronology and specialized detail cold until relevant; do not hide lower-salience mandatory closure obligations.

`software-documentation` may restructure/synthesize/publish and repair explanatory drift, but it never self-approves D1-D4 semantic mutation.
