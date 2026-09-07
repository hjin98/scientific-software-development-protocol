# Software Development Protocol 5.15

This directory is the canonical Protocol 5.15 source.

## Governing hierarchy and authority boundary

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Protocol 5.15 preserves the Protocol 5.14 authority model:

- **Tier 1A — product/problem truth:** stakeholder research, computational, scientific, operational, correctness, reliability, compatibility, resource, performance, security, and governed external-contract demands.
- **Tier 1B — Frozen high-level architecture:** material architecture/ownership/algorithm/data-representation/resource/compatibility decisions Software Design deliberately fixes for the current implementation cycle.
- **Tier 2 — solution machinery:** lower-level realization remains replaceable unless explicitly promoted by Design for material architectural value.
- **Tier 3 — development economy:** optimize reasoning/context/tool/compute/I/O/wall time only after Tier 1 is met through the minimum justified Tier-2 system.

Implementation machinery does not become Tier 1 through existence, dependency, tests, documentation, review history, previous plan wording, or previous repair. If a current realization creates an intermediate problem, first ask whether simplifying/replacing that Tier-2 realization makes the problem disappear.

## Active simplicity

A first clean local defect remains a local owning-layer repair. Repeated patches, duplicated/synchronized state, competing authorities, accumulating wrappers/fallbacks/special cases, repeated reconciliation, or a materially simpler equivalent realization trigger Tier-2 simplification/re-derivation before another additive durable repair.

Hold Tier-1 product truth and Frozen architecture fixed, then prefer removing, narrowing, altering, consolidating, or refactoring the cause of solution-created problems. Add machinery only when a genuinely required capability is missing or one canonical mechanism replaces broader complexity.

Affected-surface expansion expands implementation/testing impact; it does not create a new product requirement or freeze the current realization. Proxy-proof acceptance follows the real production owner of the final accepted realization.

## Two-role lifecycle

```text
software-design -> software-implementation
```

- `software-design` diagnoses the real problem, separates product/problem invariants from cycle-scoped Frozen architecture and delegated solution space, chooses the globally justified high-level design, defines simplification/redesign triggers, designs acceptance, and independently reviews substantial/high-risk implementations.
- `software-implementation` realizes the accepted contract adaptively, may simplify/replace delegated machinery while preserving Tier 1, closes coherent stages semantically and functionally, and completes final accepted-contract reconciliation plus affected-surface regression/integration.

Testing and independent review are activities/modes, not extra lifecycle roles. Optional specialists remain supporting capabilities rather than approval gates.

## Development workflow prompt entrypoint

The canonical human-facing orchestration reference is:

- `shared/references/development-workflow-prompts.md`

It provides standalone prompts for Design/Workplan, Implementation, Review & Update, Verification, Stabilization/Architecture GC, downstream-workplan Alignment, Health Audit, and Closeout. Each stage exposes a small `INPUTS` block so users define task-specific values once and the prompt refers to those symbolic variables thereafter.

These prompts are entry routing for the existing protocol skills and references. They do not create a parallel lifecycle, requirement source, approval authority, or independent doctrine.

## Shared doctrine and language engineering profiles

Protocol 5.15 adds a thin language adaptation layer without creating separate protocols:

```text
shared domain doctrine
        |
        v
language profile router
        |
        +--> Python engineering
        +--> C++ engineering
        +--> both for mixed Python/C++ boundaries
```

Material executable Python/C++ design, implementation, and review load the relevant profile. Shared owners remain canonical for architecture, workplans, testing, performance, concurrency, scientific fidelity, security, storage, release, and compatibility; profiles specialize only language/runtime/build consequences.

Canonical language owners:

- routing/composition -> `shared/references/language-profiles.md`;
- Python execution/idioms/runtime/tool/package specialization -> `shared/references/python-engineering.md`;
- C++ ownership/build/safety/numerics/SIMD/tool/package specialization -> `shared/references/cpp-engineering.md`.

Python guidance derives concurrency from the actual interpreter/runtime mode rather than assuming a universal GIL. C++ guidance treats lifetime/UB/build semantics as correctness concerns and prefers tuned kernels/compiler vectorization before bespoke low-level machinery. A mixed-language boundary activates both profiles without arbitrary profile precedence.

## Performance with minimum justified complexity

The shared performance owner keeps algorithm/work reduction, data representation/movement, optimized-kernel preference, effective resource discovery, execution classes, nested parallelism, accelerator gating, benchmark comparability, and performance-claim evidence language-agnostic.

Obvious semantically equivalent improvements that remove work/copies/allocation without material complexity need not wait for a pre-change benchmark, but quantitative speedup/scaling/resource claims require representative comparable evidence. Complexity-increasing optimization—new native boundaries, bespoke kernels, explicit SIMD dispatch, additional parallel runtimes, custom allocators, backend matrices, governed PGO/LTO, or accelerators—must earn its total-system cost.

Accelerator support remains dormant unless Tier-1/Frozen architecture explicitly enables it.

## Deterministic progressive disclosure and tools

Protocol 5.15 preserves Protocol 5.13 relation-first optional-tool routing and generalizes the parent capability classes:

```text
literal/path/text -> ordinary repository search/read
symbol ownership/reference -> semantic capability (Serena when supported)
AST/syntax/structural family -> structural analyzer (Semgrep when supported)
broad input/state invariant -> language-appropriate property/generative method
interprocedural source-to-sink -> CodeQL when supported
runtime state/crash -> debugger evidence when useful
memory/lifetime/UB -> language-appropriate instrumentation
race/synchronization -> concurrency/race evidence
performance/vectorization -> profiler/compiler/hardware evidence
```

The common selection/composition owner is `shared/references/tool-assisted-engineering.md`. The direct tool-method owners remain `shared/references/tool-serena.md`, `shared/references/tool-semgrep.md`, `shared/references/tool-hypothesis.md`, and `shared/references/tool-codeql.md`.

Hypothesis remains the Python-specific property/stateful method. C++ uses project-appropriate property/generative/fuzz methods plus compiler-native/sanitizer/debugger/profiler tools according to the claim. Tool presence never creates a fixed multi-tool pipeline.

All tool output remains bounded evidence, not product truth or task authority. Tools do not replace focused checks, stage-local/final affected regression, real-boundary integration, project-required checks, or production qualification where required.

## Workplans and acceptance

A substantial accepted workplan is a compressed task-specific implementation contract, not a frozen proof script. It preserves product/problem invariants, Frozen architecture, delegated solution space, task-specific acceptance boundaries, affected surfaces, and genuine redesign/simplification triggers.

Executable changes require focused checks, stage-local affected regression for material behavior-changing stages, final affected-surface re-derivation/regression, real-boundary integration, and repository/project-required checks. Green tests do not prove an omitted obligation. Production qualification remains separate.

Required C++ behavior must survive supported optimized/production builds rather than depend on debug-only assertions or instrumentation. Instrumented builds are correctness evidence, not production-performance evidence.

## Canonical detailed owners

Lifecycle entrypoints retain high-salience invariants and deterministic triggers. Detailed semantics live in canonical references:

- human-facing workflow orchestration prompts -> `shared/references/development-workflow-prompts.md`;
- lifecycle/workplans/authority/stages/handoff/rework -> `shared/references/workflow-and-workplans.md`;
- recurrence/active simplification/review readiness/revision economy -> `shared/references/convergence-and-cycle-economy.md`;
- regression/integration/evidence reuse/proxy-proof acceptance/qualification -> `shared/references/testing-and-validation.md`;
- architecture/ownership/Tier-1/Tier-2/redesign/complexity -> `shared/references/architecture-and-design.md`;
- language routing -> `shared/references/language-profiles.md`;
- generic performance -> `shared/references/performance-and-parallelism.md`;
- generic concurrency -> `shared/references/concurrency-and-orchestration.md`;
- optional tool capability selection -> `shared/references/tool-assisted-engineering.md`;
- tool-specific methods -> the four `shared/references/tool-*.md` owners named above;
- protocol/workplan inheritance -> `shared/references/protocol-versioning-and-compatibility.md`;
- other domain concerns -> their existing canonical references.

## Build and repository acceptance

`source/` is canonical. `dist/skills/<skill-name>/` contains generated ready-to-install bundles; top-level ZIPs are generated from the same bundle trees.

Run:

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check
```

These Python commands are this repository's validation implementation, not Python-specific product doctrine. All commands must succeed before a Protocol 5.15 revision is complete.
