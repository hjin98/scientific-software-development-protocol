---
kind: protocol-stage-evidence
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F
disposition: STOPPED-AT-ENTRY-UNAVAILABLE-REQUIRED-EVIDENCE
active_serious_challenge: none
---

# Protocol 7 Stage F — entry stop

Stages A–E are complete and committed on `ssdp-7.0-scientific-epistemic-closure`:

| Stage | Commit |
|---|---|
| A (closure) | `65b0121` |
| B | `645ba2e` |
| C | `980ec18` |
| D | `67977c6` |
| E | `db94a2d` |

Stage F has **not** begun. No immutable semantic candidate is frozen for runs. No candidate, paired 6.5 or paired 6.6 live run has occurred, and no qualification result exists.

## Blocker: unavailable required evidence

The frozen qualification contract §7 (`PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, SHA-256 `02dd12db…`) and workplan §11.6/§13.14 require a human legibility trial. Its terms:

- at least **four independent participants**, each the stakeholder or a designated scientist representing the declared reader;
- each participant reviews one fixture per arm, never the same fixture in both arms;
- each arm gets at least 20 routine and 4 critical answer opportunities.

"If a human trial cannot run, release acceptance remains blocked; no machine proxy or ratification narrative substitutes." The implementing context cannot supply participants. Stage F's freeze requires applicable qualification to pass, and §13.14 requires "a passed human legibility trial". Stage F therefore cannot close without a stakeholder action:

1. **Designate the participants and confirm availability** for the trial as frozen. Or,
2. **Relax or restructure the trial** through a governed workplan/contract change, which needs a fresh independent check.

Reporting only partial qualification is also possible, but it cannot count as a pass.

## Decision-relevant scale of the remaining Stage F campaign (estimate, not a commitment)

Before any candidate run the contract still requires:

- the fixture custodian's corpus (in progress, held outside the repository);
- a generic harness with scripted-delegate and issue-tracker stand-ins and side-effect capture;
- the independent withheld-instance and actual-harness pre-run checks;
- fresh paired baselines.

The live campaign reuses these 6.6 panels with both arms:

| Panel | Runs |
|---|---|
| Selection | 32 episodes per arm |
| Route probes | 38 runs per arm |
| T1/T7/T8 burden | 3 to 7 pairs, against fresh 6.5 |
| T4–T6 | 8 paired episodes |
| T2/T3 sentinels | twice each |

It also adds the composite ordinary-entry episodes per arm, plus blinded evaluator runs. The expected order is several hundred headless agent executions, likely hundreds of dollars of model usage and tens of hours of serial wall time. Parallel execution reduces the wall time. The stakeholder may want to set a budget alongside the human-trial decision.

## Carried items

- Stage D minor m5 (Markdown numbering of gapped elements) is cosmetic and allowed.
- The eight Stage A recheck minors are carried in `STAGE-A-CLOSURE-2026-09-28.md`.
- T7 mixed-mode backstop risk: `STAGE-E-CANDIDATE-ASSEMBLY.md`.
- Owner size of 45,958 B, judged not disproportionate by the Stage D checker. The pre-run checker re-judges it against the class-(iii) bound.
- Release state is unchanged, and Stages G/H are out of scope.
