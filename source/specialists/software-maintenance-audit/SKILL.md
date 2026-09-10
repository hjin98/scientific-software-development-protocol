---
name: software-maintenance-audit
description: Audit long-lived repositories for architectural entropy, maintainability deterioration, weak test oracles, change-risk concentration, duplicated authority, dependency drift, stale compatibility/evidence, and related temporal risks under Protocol 6.2; route evidence-backed findings without becoming an approval or refactoring authority.
---

# Software Maintenance Audit

Optional non-authoritative longitudinal sensing specialist. Determine whether a repository/subsystem is becoming harder to reason about, weakly protected, or structurally fragile; prioritize semantic risk concentration rather than static ugliness or arbitrary scores.

## Routing

Before substantive audit reasoning read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md) and [Long-horizon code health](references/long-horizon-code-health.md).

Load only triggered concerns: architecture/ownership/complexity -> [Architecture and design](references/architecture-and-design.md); testing/oracle strength -> [Testing and validation](references/testing-and-validation.md); evidence staleness/dependency/history -> [Evidence, evolution, and semantic dependencies](references/evidence-evolution-and-dependencies.md); lifecycle/rework -> [Workflow and workplans](references/workflow-and-workplans.md); history/churn/change coupling -> [Git and version control](references/git-and-version-control.md); repository inspection/context economy -> [Repository intake](references/repository-intake.md); specialized analyzer relation -> [Tool-assisted engineering](references/tool-assisted-engineering.md); recurrence/family/revision economy -> [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md); documentation coherence -> [Documentation and evidence](references/documentation-and-evidence.md); scientific/numerical correctness/oracles -> [Scientific software](references/scientific-software.md); version-specific history -> [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).

Ordinary hyperlinks/package membership are not activation commands.

## Audit method

Use trustworthy version-control/history evidence when available; state the window and limitations. If history is unavailable, do not infer trends from a static snapshot.

Material signals include combinations of high churn, complexity, weak tests, change coupling, duplicated/synchronized representations, competing owners, dependency cycles/boundary erosion, wrapper/fallback/special-case accumulation, public/config/state growth, stale compatibility/migrations, recurring defect families, weak scientific/numerical oracles, stale evidence, and documentation that needs growing historical caveats to explain present truth.

Metrics are sensors, not verdicts. No universal complexity/coverage/mutation/churn threshold is protocol authority. Investigate the semantic owner and protected outcome before recommending work.

Classify each material finding by the smallest owning repair:

- equivalent local D4 repair/simplification -> `software-implementation`;
- substantial maintenance contract or accepted D3 concern -> `software-design`;
- D2/D1 defect -> route upstream to that authority;
- test/evidence weakness -> owning semantic role under the current/new workplan;
- documentation drift -> `software-documentation`;
- lifecycle/repository residue -> `repository-hygiene`;
- insufficient evidence -> WATCH rather than invented action.

Do not redesign or broadly refactor inside the audit. Apply the Lossless Representation Rule to the report: consolidate manifestations under root causes, lead with high-consequence findings, avoid replaying the full history, and keep enough evidence/provenance for each finding to be falsifiable and actionable.

## Output

Conclude with **HEALTHY**, **WATCH**, or **ACTION REQUIRED**. For each material finding give affected subsystem, evidence/trend, authority implication, smallest justified corrective scope, and expected risk/simplicity improvement. Prefer one coherent repair for a shared cause over one workplan per symptom.
