# Testing, Verification, and Validation

Own evidence **methodology**: oracle integrity, scientific/numerical/architecture/D4 verification techniques, affected regression/integration, proxy-proof boundaries, failure injection, qualification, and executable/static validation of Project Engineering Memory (PEM) mechanics where such checks are the appropriate oracle. Evidence specification/realization/observation/assessment, applicability, stale evidence, independence/common-mode risk, dependency, and impact lifecycle are owned by [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md). Universal authority/Challenge semantics are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); PEM semantics are owned by [Project Engineering Memory](project-engineering-memory.md).

## Evidence integrity

Tests, proofs, benchmarks, metrics, literature, memory records and runtime observations are instruments, not truth or product objectives. Do not manufacture a pass by deleting/weakening assertions, removing known failing inputs, copying defective production output into expected values, converting required failure into success/warning, skipping/making required checks optional, widening tolerances/thresholds because they failed, adding product fallback only for a harness, rewriting authority to bless unintended behavior, or teaching a PEM validator to accept the fixture it was meant to reject.

Test/fixture/threshold/specification changes are legitimate when governing authority genuinely changed, the old oracle is independently shown wrong, or a stronger oracle preserves the same claim. For material completion, ask whether an independent evaluator of the same accepted outcome/engineering envelope would still consider the candidate correct.

Allocate verification effort by consequence and remaining decision-sensitive uncertainty. A high-consequence claim with a cheap exact oracle may close economically; a low-looking issue with unknown blast radius first needs the cheapest impact discriminator. A test/fixture failure does not automatically inherit the importance of its parent project: identify the protected owner claim, decide whether production or the evidence instrument is wrong, then repair the stale instrument locally when appropriate. Priority changes investigation effort, not the pass threshold for an applicable requirement.

A required check that did not execute is not a pass. Green tests do not establish omitted workplan/conformance obligations. A generated/static sensor establishes only the structural property it actually measures; it does not establish live latency, attention, cache, memory, productivity, or model behavior without live evidence.

## Evidence classes and claim scope

For every material qualification claim make the tuple recoverable: `(subject, property, oracle/method, result, limitations)`. Distinguish three evidence classes: **structural/executable consistency** (schemas, exact refs, generated parity, state transitions, package structure and other mechanically decidable properties); **semantic adequacy/conformance** (the assembled normative owners and their consequences); and **engineering-outcome improvement** (whether protocol-guided work improves correctness, autonomy, simplicity, cost or another declared outcome). No class may claim a stronger property or different subject than its method discriminates. Structural tests do not prove arbitrary prose semantics; semantic Review does not establish outcome superiority; outcome evidence does not prove implementation fidelity.

For protocol releases, arbitrary prose-semantic mutations and counterexamples belong to independent semantic Review of the assembled candidate unless the affected meaning is represented by a genuinely machine-readable contract. Exact wording pins are acceptance evidence only when that exact token/grammar is itself governed.

## Oracle strength and counterfactuals

For important changed logic ask: **What is the smallest plausible semantically wrong concretization that could still pass this evidence?** Strengthen economically with exact/reference cases, properties/stateful tests, known-broken counterfactuals, mutation/semantic perturbation, differential comparison, metamorphic relations, or real-owner integration. Coverage/mutation/complexity scores are sensors unless project authority adopts a threshold; do not optimize the score instead of the governed behavior.

For protocol qualification or schema/routing validators, pair each material positive claim with at least one discriminating negative/counterfactual fixture that would pass a word-presence or shallow-parser check but violates the semantic contract. Examples include correct terminology on the wrong owner, a `HOT` but non-applicable memory entry, a relevant `COLD` entry omitted from the summary, duplicate application surfaces presented as independent episodes, invalidated evidence still counted, a branch overlay self-declared accepted, a stale derived index hiding canonical data, mixed root/partition revisions, an unsupported schema, or instruction-like evidence text. Static string presence alone is never sufficient proof of routing/authority semantics.

Use differential testing only when independently justified concretizations should agree on governed observables. Use metamorphic testing only when accepted authority implies the relation; do not invent convenient relations.

## D1 external adequacy and D2 numerical verification

Internal D2-D4 correctness cannot prove D1 adequacy. Use problem-appropriate evidence: empirical independent observations for empirical claims; proof/axiomatic consistency/limiting or reference theory for mathematical claims; standards/qualification experiments/safety margins/stakeholder context for engineering claims. Conversely, external agreement does not prove faithful numerical/software concretization.

For D2 use the cheapest sufficiently strong **applicable** authority-backed combination: analytical/exact/limiting/manufactured cases, residuals/conservation/invariants, refinement/observed convergence order, extrapolation, conditioning/sensitivity, forward/backward error, precision/range/cancellation, trusted reference comparison, independent implementations/backends, stochastic bias/variance/convergence, and seed/backend/precision robustness. Escalate to full statistical/convergence/conditioning qualification when plausible numerical uncertainty can change scientific interpretation or acceptance; do not launch a research-grade campaign for an implementation tolerance already well inside an accepted D2 envelope. Tolerance derives from accepted D2 error/equivalence semantics, never from the backend result that happened to fail.

## D3 architecture verification

Use dependency/ownership inspection, architecture fitness checks, real state/consumer boundaries, recovery/concurrency/security/resource tests, and configuration/deployment evidence when they model the claim. Objective durable rules such as forbidden dependency direction, acyclicity, independence, or absence/uniqueness of a retired owner may be executable. Do not build a universal architecture manifest solely for compliance.

When mature machinery is replaced under a memory-triggering workplan, verify the capability-transfer map against the real current owner: demonstrate that authority-bound properties survive in the assembled replacement or are explicitly owner-approved changes, while evidence-only historical mechanisms remain replaceable. Do not keep an obsolete component merely to satisfy its old test harness.

If D4 violates coherent D3, repair D4. If D3 cannot preserve D2 or simultaneous constraints, challenge D3.

## D4 executable acceptance

Every material executable change requires, at minimum:

1. focused checks for the changed mechanism/claim;
2. affected-surface regression for changed behavior plus existing behavior that could plausibly change;
3. integration/end-to-end evidence through the assembled affected product and relevant real consumer/state/interface boundaries.

Affected surface may include callers/consumers, shared utilities, public interfaces, configuration, persistence/restart, caches/checkpoints, orchestration/concurrency, packaging/entrypoints, compatibility, documentation/contracts, PEM validator/packaging exclusion when changed, and transitive D1/D2 behavior. If impact cannot be bounded confidently, run the broader/full available suite.

After each coherent material executable stage, run focused + stage-local affected regression before dependent executable work continues. A tiny atomic change may use the final pass as its stage pass; a genuinely non-executable intermediate may combine with the nearest executable stage when explicit. Stage-local evidence aids localization but never removes final assembled regression.

## PEM/schema validation and package boundaries

Executable PEM validation is a **concretization of the documented schema**, not a second semantic owner. Validate mechanically decidable invariants and fail safe when they cannot be established, while leaving human/owner judgments such as substantive family membership, causality, comparative adequacy, and true applicability to their owning evidence/workflow process.

Where the repository implements a PEM validator/renderer, focused tests should cover as applicable:

- schema-version rejection and required metadata;
- root/partition path safety, one canonical home per ID, coherent logical publication, and stale-index fallback behavior;
- family semantic-ID namespace/lineage acyclicity and current disposition constraints;
- one causal failure episode / one positive intervention episode despite many surfaces;
- latest admissible assessment controlling current derived support without rewriting historical observation;
- counterevidence and provenance-cluster visibility;
- derived temperature vs explicit evidence-bound impact override;
- claim-relative maturity and comparative-guidance guardrails;
- authority-binding/binding-health degradation;
- applicability matching over canonical metadata rather than Hot/summary-only search;
- instruction-like evidence remaining inert data;
- live project PEM excluded from generic skill/profile/package outputs.

A parser passing its own happy-path template is weak evidence. Include negative fixtures for every implemented semantic guardrail and separately inspect any workplan obligations that are intentionally non-mechanical.

## Proxy-proof real-owner evidence

For a material acceptance claim identify the **real semantic owner/path** whose behavior constitutes the claim and the allowed test-double boundary below/outside it. Ask whether evidence could remain green while that owner is materially broken. If yes, it cannot close that owner claim.

Invalid substitutions include mocking/reimplementing the owner, calling a downstream helper when production routing is part of the claim, seeding post-decision state when the decision is under test, replacing durable persistence when restart/persistence is the claim, accepting helper-generated results when production construction/routing is the behavior being verified, or treating a derived PEM summary/index as canonical memory when root/partition coherence is the claim.

This is not a blanket mock ban. Bounded deterministic doubles remain valid below/outside the owner to control external services, hardware, expensive data/training, or nondeterminism. Production scale is needed only when production-scale behavior/resource qualification is itself the claim. If delegated owner identity changes under equivalent semantics, remap/rerun owner-specific evidence rather than preserving the old owner. If the required real-owner boundary is unavailable, mark the claim unavailable/blocking.

## Structural, liveness, and failure-path evidence

For removal/uniqueness/ownership/no-legacy-path claims, use source/structural negative assertions when runtime behavior cannot establish absence. When evidence depends on a hook/failpoint/callback/state transition, establish that the trigger actually fired when practical.

For persistence/restart/orchestration/recovery/failure-propagation claims, bounded deterministic failure injection can strengthen evidence: interrupted publication, truncated artifact, stale/missing cache, restart at material boundaries, worker/task death, controlled I/O failure, duplicate event/callback, partial transition, malformed/restored-old memory, stale derived index, or partial logical-memory publication. Keep the real recovery owner executing; prefer bounded simulation over resource exhaustion. Failure injection is claim-triggered, not universal ceremony.

## Evidence applicability and composed closure

Apply the evidence owner rather than duplicating lifecycle rules. A prior result is reusable only while its target claim, subject/candidate, oracle, regime/input, environment/backend/precision/configuration and other material dimensions remain applicable. A rerun against a changed candidate is a new evidence realization. A stale pass cannot confirm and a stale fail cannot refute current authority. Important/high-risk claims should use independent evidence routes when they materially reduce common-mode risk.

For material/high-risk scientific claims, trace composed closure when warranted:

```text
actual D4 executable behavior
 -> governed numerical observables
 -> D2 error/equivalence/uncertainty envelope
 -> D1 scientific/mathematical meaning
 -> external adequacy / validation / proof / standards evidence
```

Do not force this onto a local software refactor with no plausible upstream semantic impact.

## Qualification of semantic-definition and traceability claims

For mechanically decidable semantic-definition/traceability structure, qualification pairs material positive claims with discriminating negative cases. Static sensors may verify mechanically decidable structure—required fields/routes, resolvable locators, profile/version identity, exact frozen bytes, generated parity, or a declared bounded dependency graph—but must not claim to prove arbitrary mathematics, dimensional validity, theorem applicability, source support, owner equivalence, audience expertise, semantic completeness, or warrant sufficiency.

Counterfactuals must include semantically wrong cases that shallow word-presence checks would accept: specialized use before definition/import; two conflicting applicable owners with a deterministic file-order winner; undeclared primitive or ambiguous binder shadowing; a definition that smuggles existence/convergence/truth; wrong relation/logical direction or type/unit mismatch; parameter family evidence reused across a materially different binding/default; stochastic semantics missing dependence/conditioning; imported result with unmet hypotheses or unsupported/wrong-version citation; circular claim warrant; a `USES_DEFINITION` trace that mistakes hyperlinks/call graphs for semantic dependency or claims global completeness from a partial map; runtime inference without loading the exact owner; and external evidence text attempting to authorize an action.

Positive fixtures distinguish genuinely foundational objects, exact imported prerequisites, explicit primitives/binders, conservative definitions, well-formed parameterized families/instances, properly discharged/propagated validity conditions, legitimate mutually recursive definition groups, and bounded traces whose scope/completeness claim matches what was actually reviewed.

For parameter-sensitive evidence, vary the material parameter/regime so the oracle proves it rejects stale reuse rather than merely recording a parameter field. For external-source trust, prove instruction-like content remains inert data while the supported semantic claim/source locator can still be inspected. Human or agent semantic Review remains required where no honest mechanical discriminator exists. Synthetic fixture dictionaries may exercise a real executable predicate, but passing a self-contained fixture matrix cannot by itself qualify the prose authority the fixture was designed to model.

## Final assembled acceptance

Before implementation completion: reconcile every accepted governing obligation and material structural/absence claim; re-derive the final affected semantic/behavioral/evidence/documentation/memory surface; account for each affected path with executed coverage or unavailable/blocking state; run complete affected regression after all material executable edits; run assembled real-boundary integration/end-to-end; run repository/project-required build/lint/type/package checks; and close material evidence/dependency/history/PEM impact under their owners.

For a protocol-version implementation, validate source -> generated descendants -> generic packages -> versioned profiles/prompts/snapshots -> Core selection/fallback as one assembled candidate. Frozen prior-version resources are test oracles and must remain byte/behavior stable. Exact-ref public fallback claims require the actual validated immutable ref; do not substitute default/latest/semantic-version guessing.

Review readiness normally follows this acceptance. Review may still inspect missing evidence, but missing required acceptance remains a blocker rather than being moved after Review. Production qualification is separate from functional acceptance; use long/data-heavy/target-hardware workloads only when they establish production-scale time, throughput, RAM/VRAM, storage/I/O, scaling, accelerator use, or recovery cost.

Apply the Lossless Representation Rule to evidence summaries: lead with invalid/unavailable/contradictory evidence and decision consequences, keep raw logs cold when provenance remains recoverable, and never let compactness hide a required failure, uncertainty, applicability qualification, or lower-salience closure obligation.
