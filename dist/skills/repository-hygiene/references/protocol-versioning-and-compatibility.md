# Protocol Versioning and Compatibility

## Versioning

`PROTOCOL_VERSION` identifies the protocol contract.

- major: incompatible role/lifecycle or governing-doctrine change;
- minor: backward-compatible capability, doctrine, or control-plane strengthening;
- patch: clarification or defect correction.

Protocol 5 established the governing product doctrine: material engineering requirements define the feasible product space, and among engineering-sufficient solutions the protocol prefers the globally justified software/system design with the lowest unnecessary total complexity.

Protocol 5.1 added the optional `software-documentation` specialist. Protocol 5.2 added the optional `repository-hygiene` specialist. Protocol 5.3 strengthened stage-local/final functional acceptance and separated production qualification. Protocol 5.4 added development-economy, accepted-workplan authority, bounded redesign, version-bound workplan inheritance, evidence/context reuse, coherent stage granularity, and evidence-directed review.

Protocol 5.5 is a backward-compatible **implementation-fidelity and workflow-integration refinement**. It preserves the Protocol 5 doctrine, two-role lifecycle, and Protocol 5.3/5.4 acceptance/economy guarantees while adding lossless Design -> Implementation translation, protected-concern preservation, required-consequence versus suggestion/delegation distinctions, minimum-known-contract semantics, dual semantic/functional stage closure, final accepted-contract reconciliation, and lossless review/rework routing.

Protocol 5.6 is a backward-compatible **proxy-proof acceptance and test-double-boundary strengthening**. It preserves all earlier Protocol 5 guarantees while adding explicit semantic-owner-under-acceptance, allowed test-double boundary, proxy-proof counterfactual, real-owner handoff, and independent-review challenge rules.

Protocol 5.7 is a backward-compatible **engineering-stewardship and outcome-alignment strengthening**. It preserves the exact Protocol 5 hierarchy, two-role lifecycle, and all earlier guarantees while making the stakeholder's intended durable product the shared optimization target.

Protocol 5.8 is a backward-compatible **effective-compression and canonical-ownership refinement**. It preserves material engineering semantics while reducing always-loaded duplication and keeping detailed generic doctrine behind canonical references.

Protocol 5.9 is a backward-compatible **agent-portable deterministic-routing refinement**. It preserves the Protocol 5 hierarchy, two-role lifecycle, and prior safeguards while making progressive disclosure reliable across Agent-Skills-style harnesses.

Protocol 5.10 is a backward-compatible **snapshot-complete handoff refinement**. It preserves the Protocol 5 hierarchy and requires accepted Design -> Implementation handoff artifact sets to carry every still-binding task-specific semantic without depending on unavailable history or unsupplied external resources.

Protocol 5.11 is a backward-compatible **tool-assisted engineering methodology and capability refinement**. It preserves the Protocol 5 hierarchy and adds optional capability-aware guidance for Serena semantic repository work, Semgrep structural/variant analysis, and Hypothesis property/stateful testing.

Protocol 5.12 is a backward-compatible **development-convergence and cycle-economy control refinement**. It preserves the Protocol 5 hierarchy while making repeated evidence change the engineering method: local repair can broaden to semantic-family reasoning and repeated post-closure failure can trigger bounded Design reconsideration. It also adds review readiness, acceptance liveness, revision economy, and evidence/test-cycle reuse.

Protocol 5.13 is a backward-compatible **deterministic tool-entry, CodeQL, and progressive-disclosure compression refinement**. It preserves prior engineering/acceptance/convergence safeguards while making optional-tool routing operational per material engineering question, adding CodeQL for supported interprocedural/data-flow relations, and reducing always-loaded convergence/tool context.

Protocol 5.14 is a backward-compatible **solution-boundary and active-simplicity strengthening**. It clarifies the existing three-tier doctrine rather than changing it: Tier 1 consists of intrinsic stakeholder/domain product truth plus high-level architecture explicitly Frozen by Software Design for the current implementation cycle; lower-level realization remains Tier 2 by default and does not acquire invariant authority through existence, dependency, testing, documentation, review history, previous repair, or acceptance evidence that merely names the current owner. Protocol 5.14 narrows minimum-known-contract semantics accordingly, distinguishes affected-surface expansion from requirement expansion, makes Tier-2 simplification/re-derivation mandatory before another additive durable repair when structural evidence shows solution ossification or unnecessary complexity, and preserves proxy-proof acceptance by binding evidence to the final real production owner of the accepted claim rather than implicitly freezing a replaceable Tier-2 owner. It preserves the two-role lifecycle, product requirements, snapshot-complete handoff, affected regression/integration, revision economy, and Protocol 5.13 deterministic tool routing.

Protocol 5.15 is a backward-compatible **language-engineering-profile and cross-language performance refinement**. It preserves the Protocol 5 hierarchy, two-role lifecycle, active simplicity, acceptance, convergence, snapshot-complete handoff, and version-binding guarantees while separating shared language-agnostic doctrine from thin differential Python and C++ engineering profiles. Material executable Python/C++ work deterministically activates the relevant profile; mixed-language surfaces compose both without a global language precedence. Protocol 5.15 generalizes performance/concurrency/tool relation classes, preserves language-native realization, modern Python runtime variants, compiled build-mode correctness, effective resource discovery, architecture-gated accelerators, scientific equivalence, and evidence-before-complexity escalation without creating parallel protocols or mandatory tool/runtime stacks.

Protocol 5.16 is a backward-compatible **long-horizon code-health, adversarial-verification, and portable workflow-orchestration refinement**. It preserves the Protocol 5 hierarchy and two-role lifecycle while adding non-authoritative quality ratchets and maintenance sensors, conditional mutation/differential/metamorphic/failure-injection evidence, executable architecture-fitness guidance, fresh-context falsification-oriented review, risk-triggered Verification, non-mutating milestone Stabilization, one optional semantic maintenance-audit specialist, stronger lifecycle closeout, and a canonical parameterized human-facing prompt entrypoint with compatible-local-first/public-repository-fallback skill resolution. Metrics remain sensors rather than product truth, routine changes do not acquire fixed new gates, and older workplans retain their declared protocol semantics.

The two-role lifecycle remains unchanged:

```text
software-design -> software-implementation
```

## Workplan protocol binding

Every workplan that inherits protocol-wide behavior binds that inheritance to its declared `protocol_version`.

A workplan governed by version `X` continues to mean the Protocol `X` contract after newer releases. Do not reinterpret an active or completed older plan using newer generic rules merely because the installed/latest skill changed.

An active workplan may explicitly adopt a newer backward-compatible protocol version after reconciling changed obligations and updating `protocol_version`; do not silently upgrade it. Previously executed evidence remains reusable when no changed protocol obligation or affected product dimension can plausibly alter its claim.

## Candidate identity

For a normal Git repository, the candidate commit plus absence of unintended product-defining working-tree changes is usually sufficient source identity. Use additional hashes/manifests only at real boundaries not represented by Git.

## Evidence invalidation

Rerun a check when a changed dimension could plausibly alter its result or interpretation. Stage-local evidence must correspond to the stage it accepts; final affected-surface regression and integration must reflect the assembled candidate after all material executable edits that could invalidate earlier evidence.

Semantic/conformance closure and functional evidence are separate claims. A protocol-version adoption may require newly introduced conformance reasoning without automatically invalidating still-valid unrelated executable evidence.

## Compatibility

Preserve software compatibility when the product contract requires it. Compatibility mechanisms create product complexity, so do not retain obsolete layers indefinitely without a supported-version or migration requirement.

Protocol 5.14 clarified that historical implementation machinery is not itself a compatibility contract. Protocol 5.15 applies the same rule to language/runtime machinery: a current Python or C++ implementation, tool, backend, compiler, GIL mode, or packaging mechanism does not become product authority merely because it exists. Preserve it only when product/Frozen requirements need it or it remains the minimum justified realization.

## Earlier protocol versions

Completed work under earlier protocol versions remains valid historical work under the version that governed it. Active older workplans do not automatically adopt Protocol 5.16 or any later release. They may continue under their declared version or explicitly adopt a newer backward-compatible version after reconciling changed obligations. A protocol-version change alone does not require repeating still-valid evidence unless a newly adopted requirement or affected dimension invalidates the claim.
