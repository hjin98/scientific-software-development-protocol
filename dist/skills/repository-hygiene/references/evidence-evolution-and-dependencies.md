# Evidence, Evolution, and Semantic Dependencies

Own evidence specification/realization/observation/assessment, applicability and stale-state, evidentiary target vs execution dependency, independence/common-mode risk, bounded semantic dependency/impact closure, and semantic-evolution history. Evidence is not D5 and never becomes D1-D4/external authority by packaging or repetition.

## Core model and terminology

```text
authority / governed claim
 -> evidence specification
 -> evidence realization
 -> observation
 -> evidence assessment
```

- **evidence specification** — reusable test/experiment/benchmark/proof/check/validation definition;
- **evidence realization** — one concrete execution/instantiation under identified subject, inputs/regime, environment and assumptions;
- **observation** — result produced by a realization;
- **evidence assessment** — interpretation of observations relative to a governed claim;
- **semantic evolution record** — concise historical reasoning for material authority/concretization/evidence replacement, generalization, rejection, retirement or restoration.

**Concretization** remains D1-D4 semantic descent; do not use evidence realization as a synonym.

A contradictory observation at D4 does not identify the faulty owner. Consider D4 nonconformance, D3 inadequacy, D2 numerical inadequacy, D1 model/context inadequacy, conflicting authority, defective oracle/specification, inapplicable realization, or incorrect interpretation.

## Typed relationships

Use an explicit Markdown dependency record only when it materially improves impact/review. Prefer specific direction:

```text
child CONCRETIZES -> parent abstraction
subject DERIVED_FROM -> semantic/source basis
subject DEPENDS_ON -> material semantic dependency when no narrower relation fits
subject ASSUMES -> governing assumption
subject CONSTRAINED_BY -> external/domain constraint
new SUPERSEDES / REPLACES -> old
finding/observation CHALLENGES / CONTRADICTS -> target
evidence specification EVIDENCES -> governed claim
evidence specification/realization EXECUTION_DEPENDS_ON -> machinery/data/environment
evidence realization INSTANTIATES -> evidence specification
observation GENERATED_BY -> evidence realization
```

Do not overload `DEPENDS_ON` for imports/call graphs or evidence execution dependencies. Endpoints must be recoverable without hidden chat using the cheapest sufficient stable logical/path/workplan/protocol/release/Git identity.

A dependency view is bounded evidence, not automatically complete:

> Absence of an edge establishes independence only when the relevant mapped scope was explicitly reviewed complete for that exclusion.

Otherwise inspect current authority/implementation/evidence directly.

## Target vs execution dependency

Keep separate the **evidentiary target** (proposition/invariant evaluated) and **execution dependency** (implementation, harness, fixture, dataset, environment, backend, tool or other machinery required to realize/interpret it).

A test can target D1/D2 while executing through replaceable D4. Replacing D4 may require rerun/harness remap or retirement of a concretization-specific oracle without invalidating the higher-level proposition/specification. Do not preserve obsolete product machinery merely to keep old evidence executable.

## Applicability and stale evidence

Projects may encode local status but must distinguish enough to prevent false closure: pending/unrealized; admissible/valid; review-required; inconclusive; challenged; stale/inapplicable; rejected/invalid; retired/historical.

Core rule:

> A valid failing observation is evidence. A stale failing observation is not admissible evidence against current authority. A stale passing observation is not admissible confirmation.

Use `review-required` when applicability is uncertain. PASS/accepted/closed cannot depend on stale, rejected, unavailable-required or otherwise inadmissible evidence.

Where material, applicability must be recoverable over evidence-spec revision, subject/candidate, governed-claim revision, input/validity regime, oracle semantics, environment/backend/precision/configuration, stochastic replicate identity and protocol obligation. Native CI/test/benchmark/experiment artifacts are sufficient when they already establish this; no universal evidence manifest is required.

A rerun on a changed candidate creates a new realization; it does not rewrite the old result into evidence for the new subject.

## Durability, sufficiency, and independence

When strength is equivalent, prefer evidence coupled to durable governed invariants over replaceable detail:

```text
scientific/mathematical invariant
 > algorithm/numerical property
 > behavioral/architectural contract
 > concretization-specific detail
```

This is durability, not substitution: D1 evidence does not replace D2 verification; D1/D2 evidence does not replace required D4 conformance/integration; low-level precision does not establish external adequacy.

Evidence only establishes claims its oracle and exercised semantic owner can discriminate. Apply proxy-proof real-owner rules from testing.

For important/high-risk claims, use independently justified evidence routes when they materially reduce common-mode risk. Separate executions sharing one expected-value generator, reference implementation, defective dataset/fixture or mistaken assumption are correlated. Do not suppress contradictory admissible observations to manufacture a pass.

## Change impact and closure

When accepted authority or a material concretization changes:

```text
identify materially dependent descendants/evidence
 -> preserve unaffected siblings/still-valid evidence
 -> mark only affected items review-required/stale
 -> reconcretize/remap as needed
 -> execute required evidence again
 -> verify upward over the affected surface
```

A changed parent creates a bounded review obligation; it does not prove every descendant wrong. Account proportionately for dependent authority/concretizations, evidence specifications/realizations, documentation/current dependency view, human re-ratification, revalidation/retirement and semantic history.

Before closure every material impact item is resolved, explicitly preserved as still-valid with reason, or unavailable/blocking. Old green tests never substitute for impact closure. Protocol 6.2 remains document-controlled: these are reasoning obligations, not a required universal machine graph/database.

## Semantic evolution

Git records chronology; semantic history records **why** material meaning changed. Preserve concise reasoning when likely to prevent rediscovery/confusion, including material model/method/architecture replacement/generalization/rejection/restoration, retirement of delegated machinery after recurrence/complexity evidence, invalid assumptions/regimes, evidence that triggered upstream reconsideration, or obsolete evidence propositions/oracles.

A useful entry identifies the affected authority/concretization/evidence, previous vs replacement semantics, triggering evidence/challenge, material regime/assumptions, owning disposition, dependent impact, and references to current authority/workplan/report/commit where useful.

Current dependency views describe currently applicable relationships. History explains why; current owners explain what is true; Git preserves detailed chronology. Do not make history a second current authority or preload archived workplans when current owners + qualification + semantic evolution already establish the capability lineage.

## Retirement

A superseded artifact is ordinarily retireable only when it no longer owns current authority, no supported current concretization/evidence/compatibility path materially depends on it, and material historical rationale remains recoverable. Stale tests should be retired/remapped/clearly marked rather than retained as apparent confidence.

Apply the Lossless Representation Rule: keep current applicability/impact decisions and contradictory evidence salient; keep raw realizations/history cold when their provenance and retrieval route remain adequate; never compact away a condition needed to decide whether evidence is admissible.
