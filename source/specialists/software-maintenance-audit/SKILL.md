---
name: software-maintenance-audit
description: Audit long-lived software repositories for architectural entropy, maintainability deterioration, weak test oracles, change-risk concentration, duplicated authority, dependency drift, stale compatibility paths, and related temporal code-health risks. Use for periodic repository/subsystem health audits across accumulated development history; emit evidence-backed findings and routing, not feature approval or broad automatic refactoring.
---

# Software Maintenance Audit

Audit repository health over time without becoming a new lifecycle authority.

## Reference routing

Before substantive audit reasoning:

- **MUST read** [Workflow and workplans](references/workflow-and-workplans.md) for authority, lifecycle, and rework routing.
- **MUST read** [Testing and validation](references/testing-and-validation.md) before judging test protection or oracle strength.
- **MUST read** [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md) before interpreting historical work under different protocol versions.
- **MUST read** [Long-horizon code health](references/long-horizon-code-health.md) for quality-ratchet, metric-sensor, stabilization, and audit semantics.
- **MUST read** [Architecture and design](references/architecture-and-design.md) before classifying ownership/complexity/architecture findings.
- Read [Git and version control](references/git-and-version-control.md) for history/churn/change-coupling evidence when available.
- Read [Repository intake](references/repository-intake.md) to bound inspection efficiently.
- Read [Tool-assisted engineering](references/tool-assisted-engineering.md) when a material audit question maps to a specialized capability.
- Read [Convergence and development-cycle economy](references/convergence-and-cycle-economy.md) for recurring defect families and repeated repair patterns.
- Read [Documentation and evidence](references/documentation-and-evidence.md) when documentation coherence is part of the signal.
- Read [Scientific software](references/scientific-software.md) when the audited risk includes scientific/numerical correctness or oracle weakness.

## Audit objective

Determine whether the selected repository/subsystem is becoming harder to reason about, more weakly protected, or more structurally fragile over the available history. Prioritize evidence-backed risk concentration rather than static ugliness or arbitrary scores.

Useful observations include:

- high churn combined with complexity or weak tests;
- repeated bug-fix concentration and recurring semantic defect families;
- temporal change coupling across supposedly independent modules;
- duplicated/synchronized representations and competing authorities;
- dependency cycles, boundary erosion, and ownership fan-out;
- wrapper/fallback/adapter/special-case accumulation;
- configuration/public API/state-machine growth;
- stale compatibility/migration paths;
- mutation survivors or counterfactual evidence of weak tests;
- scientific/numerical logic lacking reference/property/metamorphic protection;
- documentation requiring growing historical caveats to explain the present system;
- completed workplans or lifecycle residue still appearing active.

Metrics are sensors, not verdicts. Investigate the semantic cause before recommending work.

## History discipline

Use VCS/history evidence when available and trustworthy. State the history window and material limitations. If relevant history is unavailable, do not fabricate churn, trend, or change-coupling conclusions; report only static/current-state findings that the evidence supports.

Do not require a persistent complexity ledger, universal health score, or repository-wide threshold.

## Finding classification and routing

Classify each material finding by authority and smallest coherent repair scope:

- **D4 local repair/simplification under unchanged accepted authority** -> route to `software-implementation` when no new/revised D3 workplan or cycle-scoped architecture decision is needed.
- **Substantial maintenance work or new/revised implementation contract needed** -> route to `software-design` for a bounded D3->D4 workplan.
- **Accepted D3 architecture or cycle-scoped architecture concern** -> route to `software-design`; do not redesign inside the audit.
- **Test/oracle weakness** -> route validation strengthening to the real semantic owner under the existing/new workplan as appropriate.
- **Documentation reconciliation** -> route to `software-documentation`.
- **Repository/lifecycle residue** -> route to `repository-hygiene`.
- **Watch item** -> retain as an observation when evidence is insufficient to justify intervention.

Do not perform broad unrelated refactors merely because debt exists. Do not define new domain/product requirements, accept architecture changes, or grant implementation acceptance inside the audit.

## Output

Conclude with one of:

- **HEALTHY** — no material long-horizon deterioration requiring action;
- **WATCH** — meaningful signals exist but current evidence does not justify intervention;
- **ACTION REQUIRED** — evidence-backed problems materially threaten correctness, architecture, maintainability, or development convergence.

For each material finding report the affected subsystem, evidence/trend, authority implication, smallest justified corrective scope, and expected risk/simplicity improvement. When action is required, recommend the minimum coherent set of workplans/repairs needed to address causes rather than one artifact per symptom.
