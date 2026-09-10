# Evidence, Evolution, and Semantic Dependencies

Protocol 6.1 treats scientific-software development as an evolving relationship among accepted authority, downstream concretizations, and evidence. This reference supplements the governing abstraction/concretization model; it does not create a fifth authority domain.

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** uses four semantic authority domains: D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation.

Protocol 6.1 uses these terms:

- **concretization** — a lower-level scientific, numerical, architectural, specification, or implementation choice constrained by one or more governing abstractions;
- **evidence specification** — a reusable definition of a test, experiment, benchmark, proof/check procedure, validation procedure, or other evidence-generating instrument;
- **evidence realization** — one concrete execution or instantiation of an evidence specification under identified subject revision, inputs/regime, environment, and assumptions;
- **observation** — the result produced by an evidence realization;
- **evidence assessment** — an interpretation of one or more observations with respect to a governed claim;
- **semantic evolution record** — concise historical reasoning that explains why a material authority, concretization, evidence expectation, or delegated mechanism was replaced, generalized, retired, or restored.

Evidence is not D5 and does not become semantic truth by packaging. It supports, challenges, or fails to resolve claims owned by D1-D4 or by applicable external authority.

## Authority-Evidence-Evolution model

Maintain three orthogonal concerns:

1. **Authority/concretization structure** — what is currently supposed to be true and how accepted abstractions are concretized downstream.
2. **Evidence structure** — what specifications, realizations, observations, and assessments bear on governed claims and under what assumptions/regimes.
3. **Evolution history** — how and why authorities, concretizations, evidence expectations, and delegated mechanisms changed over time.

The development cycle is therefore dynamic:

```text
observation/context
 -> model or authority proposal
 -> accepted abstraction
 -> downstream concretization
 -> prediction/behavior
 -> evidence realization
 -> observation
 -> evidence assessment/challenge
 -> authority or concretization revision when justified
 -> bounded dependency impact
 -> reconcretization/revalidation
```

A contradiction observed at D4 does not prove D4 is the faulty owner. Investigation must consider D4 nonconformance, D3 architecture inadequacy, D2 algorithm/numerical inadequacy, D1 model/context inadequacy, conflicting authority, an invalid evidence specification/oracle, an inapplicable evidence realization, or incorrect interpretation of an observation.

## Typed semantic relationships

When an explicit Markdown dependency record materially improves impact analysis or review, prefer semantically typed relationships over a generic graph.

Use consistent direction:

- `CONCRETIZES`: child/concretization -> governing parent abstraction;
- `DERIVED_FROM`: subject -> semantic/source basis;
- `DEPENDS_ON`: subject -> material semantic dependency only when no more specific relation fits;
- `ASSUMES`: subject -> governing assumption;
- `CONSTRAINED_BY`: subject -> external/domain constraint;
- `SUPERSEDES` / `REPLACES`: new/current item -> old/superseded item;
- `CHALLENGES` / `CONTRADICTS`: observation/assessment/finding/authority -> challenged target;
- `EVIDENCES`: evidence specification -> intended governed claim;
- `EXECUTION_DEPENDS_ON`: evidence specification or realization -> machinery/data/environment needed to execute or interpret it;
- `INSTANTIATES`: evidence realization -> evidence specification;
- `GENERATED_BY`: observation -> evidence realization.

Do not use `DEPENDS_ON` as a generic substitute for source imports, call graphs, or evidence execution dependencies.

### Reference integrity

Recorded endpoints must be recoverable without hidden chat. Use the cheapest sufficient identity, for example a stable logical name, existing workplan/domain ID, repository path and section anchor, protocol/release identity, Git commit/tag for a historical revision, or another governed project identity.

A universal claim-ID registry is not required. When a current artifact moves or is renamed and a maintained current dependency reference would become dangling or ambiguous, reconcile the reference during the same closeout.

### Bounded completeness

A dependency record is not automatically complete merely because it exists.

> Absence of an edge is not evidence of independence unless the relevant bounded scope has been explicitly reviewed as complete for that exclusion.

If completeness has not been established, affected-surface reasoning must still inspect current authority, implementation, and evidence directly.

## Evidence target versus execution dependency

Keep these separate:

- **evidentiary target** — the proposition or invariant the evidence specification evaluates;
- **execution dependency** — the implementation, harness, fixture, dataset, environment, backend, tool, or other machinery needed to realize and interpret the evidence.

A test can evidence a D1 or D2 invariant while executing through a replaceable D4 concretization. Replacing that D4 concretization may require only a rerun, a harness remap, or retirement of a concretization-specific oracle; it does not automatically invalidate the higher-level proposition or evidence specification.

## Evidence lifecycle and applicability

Projects may encode status locally, but evidence handling must distinguish enough states to prevent false closure, including:

- pending/unrealized;
- admissible/valid for the current claim and regime;
- review-required;
- inconclusive;
- challenged;
- stale/inapplicable;
- rejected/invalid;
- retired/historical.

Core rule:

> A valid failing observation is evidence. A stale failing observation is not admissible evidence against current authority. A stale passing observation is not admissible confirmation of current authority.

`stale` means the prior specification/realization mapping cannot currently support or refute the target claim without review, rerun, or remapping. It does not itself prove the governed claim false. Use `review-required` when applicability is uncertain.

A PASS/accepted/closed claim may not depend on stale, rejected, unavailable-required, or otherwise inadmissible evidence.

Where material, evidence applicability must be recoverable across the relevant combination of evidence-specification revision, candidate/subject revision, governed-claim revision, input/validity regime, oracle semantics, environment/backend/precision/configuration, stochastic replicate identity, and protocol obligation. Native test/continuous-integration/benchmark/experiment artifacts are sufficient when they already establish the needed identity; Protocol 6.1 does not require a universal evidence manifest.

A rerun against a changed candidate creates a new evidence realization. It does not mutate an old result into evidence for the new candidate.

## Evidence durability, sufficiency, and independence

When evidentiary strength is equivalent, prefer specifications coupled to durable governed invariants over replaceable concretization detail:

```text
scientific/mathematical invariant evidence
 > algorithm/numerical property evidence
 > behavioral/architectural contract evidence
 > concretization-specific evidence
```

This is a durability preference, not a substitution hierarchy. D1 evidence does not replace required D2 numerical verification; D1/D2 invariant evidence does not replace required D4 conformance/integration evidence; low-level precision does not establish scientific adequacy.

Evidence may satisfy only claims its oracle and exercised semantic owner can establish. Proxy-proof and real-owner requirements remain controlling.

For important/high-risk claims, prefer more than one independently justified evidence route when it materially reduces common-mode risk. Separate test functions are not independent when they share the same expected-value generator, reference implementation, defective dataset, fixture, or mistaken assumption.

An evidence assessment may aggregate several realizations/observations for replication, stochastic/statistical interpretation, convergence, cross-backend comparison, or independent evidence routes. Contradictory admissible observations may not be silently discarded to manufacture a pass.

## Bounded change impact and impact closure

When accepted authority or a material concretization changes:

```text
identify materially dependent descendants/evidence
 -> preserve unaffected siblings and still-valid evidence
 -> mark only affected items review-required/stale
 -> reconcretize/remap as needed
 -> realize required evidence again
 -> verify upward across the affected surface
```

A changed parent creates a review obligation over materially dependent descendants; it does not prove every descendant wrong.

For a material change, workplan/review impact reasoning should account proportionately for:

```text
changed authority/concretization
 -> affected descendant authority/concretizations
 -> affected evidence specifications/realizations
 -> affected documentation/current dependency view
 -> required human re-ratification where applicable
 -> required revalidation/retirement/history update
```

Before closure, every material impact item must be resolved, preserved as still-valid with reason, or explicitly unavailable/blocking. Old green tests are never a substitute for impact closure.

Because Protocol 6.1 remains document-controlled, these integrity checks remain reasoning obligations rather than a mandatory machine graph:

- no accepted-current concretization is knowingly bound to a superseded parent without an explicit compatibility/historical relationship;
- no PASS relies on stale/rejected/unavailable-required evidence;
- material accepted authority changes receive bounded impact closure;
- evidence targeting superseded propositions is reviewed rather than silently retained as current confirmation;
- invariant-level evidence is preserved/remapped when still applicable;
- new material authoritative claims receive appropriate evidence;
- unresolved material dependency/evidence ambiguity remains blocking rather than inferred away from an incomplete map.

## Semantic evolution history

Git records chronology but normally cannot explain semantic causation. Preserve concise historical reasoning when it is likely to prevent rediscovery or future confusion, including material model generalization/replacement, algorithm rejection, architecture supersession, retirement of delegated machinery after recurrence/complexity evidence, invalidated assumptions/regimes, evidence that triggered upstream reconsideration, evidence specifications retired because their proposition/oracle became obsolete, previously rejected approaches when recurrence is plausible, or later restoration of an older approach under new evidence.

A material entry should identify, where applicable:

- affected authority/concretization/evidence specification;
- previous and replacement semantics;
- triggering observation/evidence/challenge;
- validity regime/assumptions;
- rationale and owning-domain disposition;
- affected descendants/evidence;
- references to current authority/workplans/reports/commits.

Current dependency records describe currently applicable relationships. Evolution history explains why current state changed. Git retains detailed file chronology. Do not turn the current dependency view into append-only patch history or make history a second current authority.

## Retirement and repository hygiene

A superseded artifact is ordinarily eligible for retirement when:

1. it no longer owns current semantic authority;
2. no supported current concretization/evidence/compatibility path materially depends on it; and
3. material historical rationale needed to prevent rediscovery/confusion has been preserved through Git and/or semantic evolution history.

Stale passing tests are an authority-confusion risk because they can fabricate confidence. Retire, remap, or clearly mark them according to current applicability rather than retaining them as apparent confirmation.

## Final invariant

```text
authority defines what must be true;
concretization defines how that authority is expressed downstream;
evidence specifications define how claims are interrogated;
evidence realizations produce observations under concrete conditions;
evidence assessments determine what those observations can legitimately support or challenge;
evolution history preserves why material semantic choices changed;
bounded impact closure keeps all of these aligned over time.
```
