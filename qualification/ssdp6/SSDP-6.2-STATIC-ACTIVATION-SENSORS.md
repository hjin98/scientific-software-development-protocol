---
kind: ssdp62-static-activation-sensor-evidence
protocol_version: 6.2.0
accepted_baseline_commit: cec29671b9db59d20124a6e2ce99725ed60b8f0a
semantic_candidate: 6f71812fe79bb9996fa467cc68dfe8d988d278d6
authority: non-normative-qualification-evidence
status: measured
live_telemetry: unavailable
---

# Protocol 6.2 Static Activation Sensors

## Measurement contract

This is deterministic static source measurement, not live model/harness telemetry. Each representative trace fixes a task predicate first, then applies the activation requirements stated by the corresponding root/router at the accepted Protocol 6.1 baseline and the Protocol 6.2 candidate. Scope is therefore not narrowed after observing the measurements.

**Unique active bytes** are the sum of exact UTF-8 Git-blob bytes for the selected root `SKILL.md` plus each unique activated reference. Templates and task/product files are excluded symmetrically because this sensor measures protocol routing context only. **Unconditional reads** are reference reads required before substantive reasoning by the selected root; **conditional reads** are additional references whose explicit predicates are true for the fixed representative task. **Repeated owner loads** count duplicate paths in the declared trace before de-duplication. **Routing hops** are the maximum activation-edge depth after root selection; root -> concern router -> leaf is two hops, so a larger hop count is not automatically worse.

No numerical value is an acceptance threshold. Required information may increase a sensor; lossless semantics outrank compactness.

## Sensor table

| Representative task | 6.1 active bytes | 6.2 active bytes | Delta | 6.1 U/C reads | 6.2 U/C reads | Repeated loads 6.1/6.2 | Max hops 6.1/6.2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Local D4 Python helper repair | 100,215 | 57,930 | -42,285 (-42.2%) | 1/5 | 2/4 | 0/0 | 1/2 |
| D3 -> D4 Python workplan | 106,741 | 67,371 | -39,370 (-36.9%) | 1/6 | 2/5 | 0/0 | 1/2 |
| Independent D4 Review | 114,411 | 67,371 | -47,040 (-41.1%) | 1/7 | 2/5 | 0/0 | 1/2 |
| D2 numerical-method design | 32,786 | 23,588 | -9,198 (-28.1%) | 2/0 | 2/0 | 0/0 | 1/1 |
| D1 scientific formulation | 32,828 | 23,177 | -9,651 (-29.4%) | 2/0 | 2/0 | 0/0 | 1/1 |
| Documentation reconciliation | 25,422 | 28,522 | +3,100 (+12.2%) | 2/0 | 3/0 | 0/0 | 1/1 |
| Maintenance audit | 110,783 | 94,656 | -16,127 (-14.6%) | 5/4 | 2/9 | 0/0 | 1/1 |
| Release/package reconciliation | 100,590 | 60,761 | -39,829 (-39.6%) | 1/5 | 2/5 | 0/0 | 1/1 |
| Historical recovery/migration | 84,754 | 49,995 | -34,759 (-41.0%) | 1/4 | 2/3 | 0/0 | 1/1 |
| Closeout | 73,452 | 54,510 | -18,942 (-25.8%) | 2/4 | 3/4 | 0/0 | 1/1 |

Across these ten fixed representative traces, the unweighted sum of per-trace active protocol bytes changes from **781,982** to **527,881** (-254,101, -32.5%). This aggregate is only a descriptive sensor because traces overlap and are not a workload-frequency model.

## Trace definitions and active sets

### Local D4 Python helper repair

Fixed predicate: Equivalent local Python repair; no workplan; affected regression and impact closure required; no evidence reuse/dependency change or architecture/science change.

- 6.1: 100,215 bytes; unconditional=1; conditional=5; repeated=0; max-hops=1; active: `source/roles/software-implementation/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`
- 6.2: 57,930 bytes; unconditional=2; conditional=4; repeated=0; max-hops=2; active: `source/roles/software-implementation/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/specification-and-implementation.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`

### D3 -> D4 Python workplan

Fixed predicate: Substantial Python implementation workplan; architecture, evidence applicability, acceptance/regression design, and language semantics material; D1/D2 unchanged.

- 6.1: 106,741 bytes; unconditional=1; conditional=6; repeated=0; max-hops=1; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`
- 6.2: 67,371 bytes; unconditional=2; conditional=5; repeated=0; max-hops=2; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`

### Independent D4 Review

Fixed predicate: Ordinary substantial Python D4 implementation Review; workflow/evidence/testing/language material; no Stabilization or longitudinal-health audit and no specialized analyzer predicate assumed.

- 6.1: 114,411 bytes; unconditional=1; conditional=7; repeated=0; max-hops=1; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/long-horizon-code-health.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`
- 6.2: 67,371 bytes; unconditional=2; conditional=5; repeated=0; max-hops=2; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/language-profiles.md`, `source/shared/references/python-engineering.md`

### D2 numerical-method design

Fixed predicate: Pure D2 method decision before change-plan/evidence-design concerns; D1 meaning unchanged and no performance/historical/human-facing-paper predicate.

- 6.1: 32,786 bytes; unconditional=2; conditional=0; repeated=0; max-hops=1; active: `source/roles/numerical-algorithm-design/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/numerical-algorithm-design.md`
- 6.2: 23,588 bytes; unconditional=2; conditional=0; repeated=0; max-hops=1; active: `source/roles/numerical-algorithm-design/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/numerical-algorithm-design.md`

### D1 scientific formulation

Fixed predicate: Pure D1 formulation decision before change-plan/evidence-design/historical/human-facing-paper predicates.

- 6.1: 32,828 bytes; unconditional=2; conditional=0; repeated=0; max-hops=1; active: `source/roles/scientific-formulation/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/scientific-formulation.md`
- 6.2: 23,177 bytes; unconditional=2; conditional=0; repeated=0; max-hops=1; active: `source/roles/scientific-formulation/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/scientific-formulation.md`

### Documentation reconciliation

Fixed predicate: Current non-scientific guide reconciliation; no represented D1-D4 concern beyond documentation ownership and no specialized technical-writing predicate.

- 6.1: 25,422 bytes; unconditional=2; conditional=0; repeated=0; max-hops=1; active: `source/specialists/software-documentation/SKILL.md`, `source/shared/references/documentation-maintenance.md`, `source/shared/references/documentation-and-evidence.md`
- 6.2: 28,522 bytes; unconditional=3; conditional=0; repeated=0; max-hops=1; active: `source/specialists/software-documentation/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/documentation-maintenance.md`, `source/shared/references/documentation-and-evidence.md`

### Maintenance audit

Fixed predicate: Architecture/test/history/lifecycle maintenance audit with version-sensitive history; no scientific-numerical risk and no specialized analyzer predicate.

- 6.1: 110,783 bytes; unconditional=5; conditional=4; repeated=0; max-hops=1; active: `source/specialists/software-maintenance-audit/SKILL.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/protocol-versioning-and-compatibility.md`, `source/shared/references/long-horizon-code-health.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/git-and-version-control.md`, `source/shared/references/repository-intake.md`, `source/shared/references/convergence-and-cycle-economy.md`, `source/shared/references/documentation-and-evidence.md`
- 6.2: 94,656 bytes; unconditional=2; conditional=9; repeated=0; max-hops=1; active: `source/specialists/software-maintenance-audit/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/long-horizon-code-health.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/git-and-version-control.md`, `source/shared/references/repository-intake.md`, `source/shared/references/convergence-and-cycle-economy.md`, `source/shared/references/documentation-and-evidence.md`, `source/shared/references/protocol-versioning-and-compatibility.md`

### Release/package reconciliation

Fixed predicate: Post-implementation package/release reconciliation with package validation, lifecycle/evidence and version identity; no language-specific build-behavior question.

- 6.1: 100,590 bytes; unconditional=1; conditional=5; repeated=0; max-hops=1; active: `source/roles/software-implementation/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/release-and-distribution.md`, `source/shared/references/protocol-versioning-and-compatibility.md`
- 6.2: 60,761 bytes; unconditional=2; conditional=5; repeated=0; max-hops=1; active: `source/roles/software-implementation/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/specification-and-implementation.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/testing-and-validation.md`, `source/shared/references/release-and-distribution.md`, `source/shared/references/protocol-versioning-and-compatibility.md`

### Historical recovery/migration

Fixed predicate: D3/workplan historical recovery and compatibility reasoning; no executable-language or scientific/numerical mutation.

- 6.1: 84,754 bytes; unconditional=1; conditional=4; repeated=0; max-hops=1; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-realization.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/protocol-versioning-and-compatibility.md`
- 6.2: 49,995 bytes; unconditional=2; conditional=3; repeated=0; max-hops=1; active: `source/roles/software-design/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/architecture-and-design.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/protocol-versioning-and-compatibility.md`

### Closeout

Fixed predicate: Post-acceptance documentation/version/generated-artifact closeout with no repository residue and no product mutation; hygiene branch therefore not triggered.

- 6.1: 73,452 bytes; unconditional=2; conditional=4; repeated=0; max-hops=1; active: `source/specialists/software-documentation/SKILL.md`, `source/shared/references/documentation-maintenance.md`, `source/shared/references/documentation-and-evidence.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/protocol-versioning-and-compatibility.md`, `source/shared/references/release-and-distribution.md`
- 6.2: 54,510 bytes; unconditional=3; conditional=4; repeated=0; max-hops=1; active: `source/specialists/software-documentation/SKILL.md`, `source/shared/references/abstraction-and-concretization.md`, `source/shared/references/documentation-maintenance.md`, `source/shared/references/documentation-and-evidence.md`, `source/shared/references/workflow-and-workplans.md`, `source/shared/references/evidence-evolution-and-dependencies.md`, `source/shared/references/protocol-versioning-and-compatibility.md`, `source/shared/references/release-and-distribution.md`

## Interpretation

- This measurement repairs the Stage-F sensor omission in the original 115-case report and adds the previously omitted independent-D4-Review representative trace.
- It does not claim every individual metric improves. In particular, D3/D4 Python traces intentionally gain one routing hop in 6.2 because language leaf dispatch is moved behind `language-profiles.md`; that extra hop is the progressive-disclosure boundary, not a failure.
- Repeated owner loads are reported rather than assumed to improve. The selected traces contain no duplicate path loads under either version; the 6.2 reuse rule remains a semantic safeguard against future repeated activation.
- Static source bytes do not establish actual prompt tokens, latency, cache behavior, or model quality. No live-harness performance claim is made.
- Independent Review must assess both the fixed-predicate choices and whether any required owner was omitted from an active set. A disputed trace is an evidence issue to correct, not permission to narrow governed scope.

