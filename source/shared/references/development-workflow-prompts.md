# Scientific Software Development Workflow Prompts

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture, and D4 specification/implementation authority. This is the canonical human-facing orchestration source for Protocol 6.2. These are execution prompts: `AUTO_EXECUTE` performs authorized work with available tools; `REPORT_ONLY` inspects and reports without product/authority mutation.

## Shared execution contract

Resolve the governing protocol version before interpreting stages. A workplan's declared `protocol_version` controls inherited semantics; never guess that a semantic version is a Git ref or silently substitute latest/default-branch doctrine.

With `PROTOCOL_SOURCE = AUTO_LOCAL_FIRST`, use a governing-version-compatible installed skill/exposed skill root when readable; otherwise use the canonical public repository only at the immutable public-source ref mapped for that version. If neither compatible source can be read, report truthful non-closure rather than executing from memory or a similarly named incompatible skill.

```text
PUBLIC_REPOSITORY = https://github.com/hjin98/scientific-software-development-protocol
```

**Protocol 6.2 bootstrap self-reference rule:** this source snapshot intentionally does not name its own Git SHA. Current 6.2 `PROTOCOL_REF = AUTO` may use public fallback only when a later current-source mapping publishes an exact immutable 6.2 bootstrap ref. Before that publication, **automatic current-6.2 public fallback is unavailable**; if no governing-version-compatible local source is readable, report truthful non-closure. If this snapshot was already reached through an explicit immutable ref or through a later exact mapping, continue using the already-resolved source and do not recurse to repository-default bytes. The invalidated pre-acceptance attempt `1181c2031710c5d343194d87d08543290fded0ab` must not be used for current 6.2 fallback. Historical/accepted 5.16/6.0/6.1 resolution continues through exact immutable mappings. Repository-default bytes are never a substitute.

`AUTO_EXECUTE` means inspect the real target, infer ordinary discoverable context, and perform every authorized action rather than stopping at commands/snippets/next steps. Prefer action over clarification when context is discoverable; ask only when proceeding would require guessing consequential authority, semantics, target, or irreversible action.

A stage mutates only its owned authority/concretization/lifecycle surface. Route a discovered D1/D2/D3 defect to its owner instead of silently crossing the boundary. Review, Verification, Stabilization and Health Audit remain non-product-mutation activities except lifecycle/planning records explicitly owned by the stage.

Apply the Protocol 6.2 Lossless Representation Rule to every stage/output: preserve complete governed meaning first; load generic doctrine once at its canonical owner; activate additional concern owners only when their decision predicate fires; reuse applicable established context; lead with Serious Challenge/blockers/current decisions/material uncertainty; keep routine/history/raw detail cold but discoverable; never omit a mandatory lower-salience constraint for brevity.

A material D1/D2/durable-D3 authority mutation becomes accepted-current only after the owning acceptance process, including independent falsification by a context/reviewer that did not author the proposal and required human ratification. Otherwise leave it proposed or human-pending. An unresolved Serious Challenge under an allowed explicit human risk override remains `risk-accepted/provisional`. For every dependent result, the terminal machine-readable footer must include `authority_state = risk_accepted_provisional` (JSON key `authority_state`); descendants must not reset it to accepted-current or emit an unqualified Pass/complete result while the governing challenge remains unresolved.

Evidence specification, realization, observation and assessment are distinct. Stale passing evidence cannot confirm current authority and stale failing evidence cannot refute it until applicability is restored. Keep target claims separate from replaceable execution dependencies. On material change, perform bounded impact closure over dependent descendants/evidence/documentation/dependency views/re-ratification/retirement/history while preserving unaffected siblings and still-valid evidence.

## Stage selection

Choose by semantic/mutation boundary, not keywords: scientific/model/estimand meaning -> D1; algorithm/estimator/discretization/error semantics -> D2; architecture/ownership/data-flow/resource structure -> D3; implementation/fix/refactor/test/package -> D4; independent implementation conformance -> Review; high-risk deeper falsification -> Verification; post-convergence non-mutating architecture-GC -> Stabilization; upstream invalidation of a downstream plan -> Alignment; longitudinal repository sensing -> Health Audit; accepted docs/lifecycle/generated reconciliation -> Closeout.

Reduced D4-only, D3->D4, D2->D4 or D1->D3/D4 paths are normal when intermediate/higher semantics are unaffected. Mixed `review and fix` preserves the boundary: Review identifies/routes findings; the owning mutation stage performs repair.

Every material Review/verification/acceptance boundary includes the Challenge Pass. If accepted authority itself may be materially false, contradictory, ambiguous, inadequate, mutually incompatible, or impossible to concretize, emit `SERIOUS CHALLENGE` before ordinary findings and stop unqualified closure pending owning/human adjudication.

## 0. Authority / Affected-Domain Intake

```text
INPUTS
TASK = [requested change/problem]
REPOSITORY_TARGET = [repository/worktree/branch; AUTO = current]
GOVERNING_AUTHORITY = [known authority; AUTO = discover]
AFFECTED_DOMAIN = [AUTO = earliest potentially affected D1/D2/D3/D4]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit source]
PROTOCOL_REF = [AUTO = governing version mapping or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Inspect the actual target. Classify the earliest/highest semantic domain whose accepted meaning may change plus directly governed side constraints and plausibly affected descendants/evidence. Perform bounded routing only; do not mutate product/domain authority. Route to scientific-formulation, numerical-algorithm-design, software-design, or software-implementation. For D3/D4-only classification, perform proportionate upstream-impact exclusion where scientific/numerical risk is plausible. Do not invent missing D1/D2 artifacts for genuinely non-scientific local software.
```

## 1. D1 Scientific & Mathematical Formulation

```text
INPUTS
TASK = [D1 change/question/review]
REPOSITORY_TARGET = [AUTO = current]
CURRENT_AUTHORITY = [D1 owner; AUTO = discover]
WORKPLAN_DESTINATION = [abstraction-concretization plan path when materially needed; AUTO]
HUMAN_RATIFICATION = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = governing version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve scientific-formulation. Reconstruct the question independently of code; distinguish normative D1 from literature/evidence/rationale. Define/review observables/estimands, equations/models, assumptions, validity, interpretation, D1 uncertainty and problem-appropriate external adequacy/proof/standards evidence.

Draft proposed authority separately. Before accepted-current material D1 mutation, require independent falsification and required human ratification; otherwise remain proposed/human_pending/No-Pass. Create/update a snapshot-complete abstraction-concretization plan when material downstream handoff or independent Review needs one; do not manufacture a plan for trivial/no-dependent work. Verify child fidelity and abstraction adequacy before handoff; invalidate only materially dependent descendants/evidence. Serious Challenge accepted D1 if materially false/contradictory/ambiguous/unrealizable.
```

## 2. D2 Algorithm & Numerical Method Design

```text
INPUTS
TASK = [D2 change/question/review]
REPOSITORY_TARGET = [AUTO = current]
CURRENT_AUTHORITY = [D2 owner; AUTO = discover]
WORKPLAN_DESTINATION = [abstraction-concretization plan path when needed; AUTO]
SCIENTIFIC_AUTHORITIES = [D1; AUTO; NONE only when absent]
HUMAN_RATIFICATION = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = governing version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve numerical-algorithm-design. Recover D1 and numerical/resource constraints; define estimator/discretization/solver/normalization/order/precision/stochastic semantics, approximation/error/convergence/conditioning/uncertainty independently of current software. Choose minimum justified admissible method and sufficiently independent authority-backed oracles; never widen tolerance to accept an implementation/backend.

Before accepted-current material D2 mutation require independent falsification and required human adjudication; otherwise remain proposed/human_pending/No-Pass. Create/update a snapshot-complete abstraction-concretization plan when material downstream handoff/Review needs one, including reduced D2->D4 with unchanged D3 where valid. Verify D1 fidelity and D3 adequacy needs. Serious Challenge accepted D2 rather than request a software workaround when the method authority itself may be wrong/contradictory/ambiguous/unrealizable.
```

## 3. D3 Software Architecture / Workplan

```text
INPUTS
TASK = [D3 architecture/change problem]
REPOSITORY_TARGET = [AUTO = current]
EXISTING_AUTHORITIES = [D1-D4/external; AUTO]
WORKPLAN_DESTINATION = [D3->D4 implementation plan or abstraction-concretization plan; AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = governing version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve software-design. Reconcile D1/D2 plus directly governed security/reliability/performance/resource/compatibility/deployment constraints. Design the minimum justified admissible D3; prefer cohesive ownership, direct flow, one authoritative representation, fewer interfaces/states/dependencies and removal/consolidation over compensating machinery. Keep durable Architecture Manual authority separate from cycle freeze.

When D4 is materially affected, create/update the governing D3->D4 plan; for material D3-only mutation requiring Review, use an abstraction-concretization plan. Do not create an empty D4 plan solely for routing. Freeze only material architecture; delegate D4 mechanics. Define real-owner acceptance, affected regression/integration and reopen/simplification triggers. Durable D3 accepted-current mutation requires prior independent falsification; otherwise remain proposed/No-Pass. Challenge D3 adequacy against D2 and route D2/D1 defects upstream.
```

## 4. D4 Software Implementation

```text
INPUTS
CHANGE_PLAN = [governing plan when warranted; NONE only for genuinely local D4 work]
REPOSITORY_TARGET = [AUTO = current]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = CHANGE_PLAN protocol_version, otherwise accepted current compatible version]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve software-implementation under the declared plan version when supplied. Under AUTO_EXECUTE modify/test the real target; do not stop at snippets. For local D4 under sufficient authority, CHANGE_PLAN may be NONE; for valid D1/D2->D4 reduced routes use the upstream plan plus unchanged D3 rather than manufacturing D3 mutation.

Implement accepted D4/D3 while preserving D1/D2 and side constraints. Treat lower machinery as replaceable; prefer owning-layer remove/narrow/rewire/consolidate before wrappers/fallbacks/special cases. Close each coherent executable stage with semantic/conformance + focused + stage-local affected regression. Before completion reconcile the full contract, inspect obsolete/duplicate ownership, re-derive final affected surface, run complete affected regression, real-owner integration/end-to-end and repository-required checks, and close evidence/dependency/documentation/history impacts. Required unexecuted checks are blocking. Serious Challenge upward when parent authority itself may be defective.
```

## 5. Review & Challenge Pass

```text
INPUTS
WORKPLAN = [governing plan]
IMPLEMENTATION_TARGET = [candidate; AUTO]
RELATED_AUTHORITIES = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = workplan version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve the owner of the parent boundary; normal D4 implementation Review uses software-design in independent review mode. Review the assembled candidate, not only diff/implementer summary; prefer fresh context for substantial/high-risk work.

Challenge authority first. If Serious Challenge threshold fires, place it first and block unqualified Pass. Otherwise reconstruct every binding invariant/constraint/cycle decision/specification and independently falsify fidelity, adequacy, ownership, science/numerics, reliability/security, resources/performance, affected-surface coverage, oracle strength, evidence applicability and total complexity. Missing required pre-Review checks/impact closure remain blockers. Review does not modify product implementation; it may update/reopen/close owned lifecycle records. Route findings to earliest owner.
```

## 6. Verification

```text
INPUTS
VERIFICATION_SCOPE = [high-risk claim/subsystem/workplan/release]
IMPLEMENTATION_TARGET = [AUTO]
GOVERNING_AUTHORITY = [AUTO]
SCIENTIFIC_AUTHORITIES = [AUTO; NONE if irrelevant]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Perform deeper non-mutating risk-triggered falsification using the owning domain skill(s). Reconcile authorities, construct counterexamples, use independently justified reference/differential/metamorphic/numerical evidence, inspect real-owner paths and trace D4->D2->D1 closure when material. Distinguish internal verification from D1 external adequacy. Challenge accepted authority when warranted; Verification neither replaces ordinary Review nor mutates production implementation.
```

## 7. Stabilization / Architecture GC

```text
INPUTS
STABILIZATION_SCOPE = [converged subsystem/workplan/release]
IMPLEMENTATION_TARGET = [AUTO]
GOVERNING_AUTHORITY = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

After ordinary Review otherwise passes at a material convergence boundary, non-mutatingly ask whether the accepted concretization remains the minimum justified system. Inspect duplicate authority/state, wrappers/adapters/fallbacks/special cases, stale compatibility, unnecessary state/config/public surface, ownership leakage/cycles, historical-exception branches, dead/bypassed paths and tests dominated by replaceable orchestration. Route warranted change to D4, D3 or upstream D2/D1; do not refactor merely because Stabilization exists.
```

## 8. Downstream Authority Alignment

```text
INPUTS
UPSTREAM_ACCEPTED_WORK = [changed accepted authority]
DOWNSTREAM_WORKPLAN = [plan/authority to reconcile]
REPOSITORY_TARGET = [AUTO]
GOVERNING_AUTHORITY = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = downstream plan version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Resolve the downstream semantic owner. Under AUTO_EXECUTE update the downstream plan/authority when warranted, never production implementation. Reconcile only materially dependent assumptions/invariants/evidence, preserving unaffected siblings/still-valid evidence. An incomplete dependency map cannot prove non-impact. If upstream change makes the downstream abstraction contradictory/unrealizable, raise Serious Challenge instead of adding compatibility machinery; otherwise leave the downstream handoff snapshot-complete under its own governing version.
```

## 9. Health Audit

```text
INPUTS
AUDIT_SCOPE = [repository/subsystem/history window]
REPOSITORY_TARGET = [AUTO]
HISTORY_WINDOW = [AUTO or explicit]
GOVERNING_ARCHITECTURE = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
EXCLUSIONS = [optional; NONE]

Resolve software-maintenance-audit when available. Perform non-mutating longitudinal sensing with real history where available: churn/change coupling, recurring defect families, complexity/dependencies, public/config growth, weak oracles, stale evidence, documentation difficulty and architecture drift. Metrics are sensors; do not fabricate trends from static state. Route corrective work to the smallest owning domain/specialist; the audit itself neither accepts architecture nor implements repairs.
```

## 10. Closeout

```text
INPUTS
COMPLETED_WORK = [accepted completed scope]
REPOSITORY_TARGET = [AUTO]
AFFECTED_DOCUMENTATION = [AUTO]
PROTOCOL_SOURCE = [AUTO_LOCAL_FIRST or explicit]
PROTOCOL_REF = [AUTO = completed-work version or explicit immutable ref]
EXECUTION_MODE = [AUTO_EXECUTE | REPORT_ONLY]
ADDITIONAL_CONSTRAINTS = [optional; NONE]

Closeout starts only after semantic/functional acceptance. Under AUTO_EXECUTE reconcile affected current D1-D4 authority, guides/runbooks, generated artifacts, release/version identity, dependency/evidence views, semantic-evolution history and completed/superseded workplan state; perform conservative hygiene where justified. Preserve release-pinned truth. Archive transition artifacts only after their still-current semantics live in canonical owners. Closeout cannot change product semantics or turn unresolved acceptance/Serious Challenge into completion.
```
