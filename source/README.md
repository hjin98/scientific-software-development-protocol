# Software Development Protocol 5.16

This directory is the canonical Protocol 5.16 source.

## Governing hierarchy and authority boundary

```text
product engineering fitness > minimum justified product/system complexity > development economy
```

Protocol 5.16 preserves the Protocol 5.15 authority model:

- **Tier 1A — product/problem truth:** stakeholder research, computational, scientific, operational, correctness, reliability, compatibility, resource, performance, security, and governed external-contract demands.
- **Tier 1B — Frozen high-level architecture:** material architecture/ownership/algorithm/data-representation/resource/compatibility decisions Software Design deliberately fixes for the current implementation cycle.
- **Tier 2 — solution machinery:** lower-level realization remains replaceable unless explicitly promoted by Design for material architectural value.
- **Tier 3 — development economy:** optimize reasoning/context/tool/compute/I/O/wall time only after Tier 1 is met through the minimum justified Tier-2 system.

Implementation machinery does not become Tier 1 through existence, dependency, tests, documentation, review history, previous plan wording, or previous repair. Active simplicity still prefers removing, narrowing, altering, consolidating, or refactoring the cause of solution-created problems before adding durable machinery.

## Two-role lifecycle and quality-feedback modes

```text
software-design -> software-implementation
```

`software-design` owns diagnosis/design and independent review; `software-implementation` owns code/refactoring and executable completion. Protocol 5.16 preserves final implementation reconciliation plus final affected regression/integration/project checks before independent Review readiness.

Review, risk-triggered Verification, non-mutating Stabilization/Architecture GC, periodic Health Audit, production qualification, documentation, and hygiene are modes/supporting capabilities—not extra approval authorities. Details live in `shared/references/workflow-and-workplans.md` and `shared/references/long-horizon-code-health.md`.

## Development workflow prompt entrypoint

The canonical human-facing orchestration reference is:

- `shared/references/development-workflow-prompts.md`

It provides parameterized `INPUTS` blocks for optional Baseline/Change-Health Intake, Design/Workplan, Implementation, Review & Update, Verification, Stabilization/Architecture GC, downstream-workplan Alignment, Health Audit, and Closeout.

With `PROTOCOL_SOURCE = AUTO_LOCAL_FIRST`, resolve a governing-version-compatible installed skill through the current harness/installed-skill root first. Harness selectors such as `@software-design` or `/software-implementation` are examples, not shell commands. If local resolution fails, fall back to `https://github.com/hjin98/software-development-protocol`, read canonical `source/roles/<skill>/SKILL.md` or `source/specialists/<skill>/SKILL.md` plus required references, and preserve the protocol contract governing the task. Do not guess historical Git refs or silently upgrade older workplans.

## Long-horizon code health

`shared/references/long-horizon-code-health.md` owns the detailed 5.16 quality-feedback semantics:

- semantic changed-code/affected-surface quality ratchets;
- complexity/churn/coverage/mutation/dependency observations as sensors rather than product truth;
- conditional mutation/counterfactual oracle-strength evidence;
- differential and metamorphic testing;
- executable architecture fitness for objective stable rules;
- fresh-context falsification-oriented independent review/verification;
- non-mutating milestone stabilization;
- bounded failure-path evidence;
- periodic longitudinal maintenance sensing.

`software-maintenance-audit` is the single optional repository-level semantic health specialist. It produces findings and routing only; it does not define product requirements, Frozen architecture, or acceptance.

## Shared doctrine and language engineering profiles

Protocol 5.16 preserves Protocol 5.15's thin language adaptation layer:

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

Canonical language owners:

- routing/composition -> `shared/references/language-profiles.md`;
- Python execution/idioms/runtime/tool/package specialization -> `shared/references/python-engineering.md`;
- C++ ownership/build/safety/numerics/SIMD/tool/package specialization -> `shared/references/cpp-engineering.md`.

Protocol 5.16 makes project-configured Python fast lint/static typing (Ruff-class and Pyright/mypy-class capabilities) explicit without mandating exact tools.

## Deterministic progressive disclosure and tools

Relation-first routing remains canonical in `shared/references/tool-assisted-engineering.md`. Direct tool-method owners remain `shared/references/tool-serena.md`, `shared/references/tool-semgrep.md`, `shared/references/tool-hypothesis.md`, and `shared/references/tool-codeql.md`.

Protocol 5.16 adds conditional capability classes for test effectiveness/oracle strength, changed-code protection, objective architecture/dependency fitness, complexity/duplication hotspots, longitudinal maintenance risk, and failure/recovery evidence. Optional capabilities never create a fixed multi-tool pipeline.

## Workplans and acceptance

A substantial accepted workplan remains a compressed task-specific implementation contract, not a frozen proof script. It preserves product/problem invariants, Frozen architecture, delegated solution space, task-specific acceptance boundaries, affected surfaces, and genuine redesign/simplification triggers.

Executable changes require focused checks, stage-local affected regression for material behavior-changing stages, final affected-surface re-derivation/regression, real-boundary integration, and repository/project-required checks. Green tests do not prove an omitted obligation. Production qualification remains separate.

## Canonical detailed owners

- human-facing workflow orchestration prompts -> `shared/references/development-workflow-prompts.md`;
- lifecycle/workplans/authority/stages/handoff/rework -> `shared/references/workflow-and-workplans.md`;
- long-horizon quality/ratchets/verification/stabilization/health sensing -> `shared/references/long-horizon-code-health.md`;
- recurrence/active simplification/review readiness/revision economy -> `shared/references/convergence-and-cycle-economy.md`;
- regression/integration/oracle strength/failure-path evidence -> `shared/references/testing-and-validation.md`;
- architecture/ownership/Tier-1/Tier-2/redesign/complexity -> `shared/references/architecture-and-design.md`;
- language routing -> `shared/references/language-profiles.md`;
- optional tool capability selection -> `shared/references/tool-assisted-engineering.md`;
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

These Python commands are this repository's validation implementation, not Python-specific product doctrine. All commands must succeed before a Protocol 5.16 revision is complete.
