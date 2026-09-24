---
kind: protocol-investigation-workplan
workplan_id: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
protocol_version: 6.4.0
subject_baseline: P0 = Protocol 6.4 at 55c085261eb827e3047637d045a8e6917ea6b962 (recovery 74bc572ef516cae417437a2027eeff52a2e25c15)
subject_candidate: P1 = NOT DESIGNED (no successor assumed)
status: active
current_phase: PHASE III COMPLETE (reviewer A) / AWAITING INDEPENDENT REVIEWER B
branch: ssdp-6.5-frontier-model-re-evaluation
created_date: 2026-09-24
active_serious_challenge: none raised against accepted 6.4 D1-D4 doctrine; see defect model for lifecycle/qualification defects
normative_protocol_mutation_in_this_pass: none
---

# Protocol 6.5 Frontier-Model Re-evaluation Workplan

## Current disposition

```text
P0 BINDING:                       FROZEN — qualification/ssdp65/P0-BASELINE-BINDING-PROTOCOL-6.4.md
EVALUATION DESIGN:                PRE-REGISTERED — qualification/ssdp65/BENCHMARK-AND-EVALUATION-DESIGN.md
PHASE I  RECONSTRUCTION:          COMPLETE (reviewer A)
PHASE II FALSIFICATION:           COMPLETE (reviewer A)
PHASE III DEFECT MODEL:           FROZEN (reviewer A) — qualification/ssdp65/reviewer-a/PHASE-III-DEFECT-MODEL.md
INDEPENDENT REVIEWER B:           NOT STARTED — handoff qualification/ssdp65/INDEPENDENT-DIAGNOSTIC-HANDOFF.md
CROSS-EXAMINATION:                BLOCKED until reviewer B's findings are frozen
PHASE IV-VIII:                    NOT AUTHORIZED
SUCCESSOR VERSION:                NOT ASSUMED; "6.4 survives" and "6.4.x patch" remain admissible outcomes
NORMATIVE SOURCE CHANGES:         NONE in this pass
```

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture and D4 specification/implementation authority. **P0** is the frozen accepted Protocol 6.4 control; **P1** is any later candidate. **Reviewer A** is the diagnostic author of this branch; **reviewer B** is an independent frontier-model reviewer who has not seen reviewer A's findings. **Project Engineering Memory (PEM)** is project-local evidence-backed decision support; a **Historical Applicability Set (HAS)** records task-local dispositions of relevant PEM entries.

## Governing authority and scope

1. Task authority: the stakeholder's re-evaluation brief of 2026-09-24 (objective: maximize reliable development intelligence subject to preservation of validated invariants; quality vector `Q = (C, F, A, E, G, U, S, K)`; mandatory phase separation I–VIII).
2. Governing protocol for conducting this work: accepted Protocol 6.4 (`protocol_version: 6.4.0`). This workplan does not reinterpret 6.4 or any version-bound 6.3-or-older work.
3. Subject of evaluation: the assembled accepted 6.4 system at P0, including canonical `source/`, generated descendants, lifecycle/qualification practice and self-hosted PEM.
4. Protocol 7 workplans remain governed by their own index entries and are not modified by this investigation.

## Non-goals of the current pass

- No edit to normative 6.4 authority (`source/`, generated `dist/`, orchestrator resources, frozen profiles, `AGENTS.md`, `README.md`, `PROJECT-ENGINEERING-MEMORY.md`, archived artifacts).
- No Protocol 6.5 design, and no assumption that a successor is necessary.
- No reading of any other frontier-model review of this investigation (none existed at creation).
- No simulated second reviewer.

## Phase plan and gates

| Phase | Output | Gate to enter next phase |
| --- | --- | --- |
| I Reconstruction | `reviewer-a/PHASE-I-RECONSTRUCTION.md` | complete authority/invariant map; deliberate doctrine distinguished from candidate defects |
| II Falsification | `reviewer-a/PHASE-II-FALSIFICATION.md`, `reviewer-a/tools/*`, `reviewer-a/evidence/*` | counterexamples in trajectory form; historical replay; executed experiments recorded |
| III Defect model | `reviewer-a/PHASE-III-DEFECT-MODEL.md` | every material finding as `(O, E, I, R, C, S)`; stop-condition decision recorded; findings committed immutably |
| — Independent reviewer B | `reviewer-b/` (to be created by reviewer B) | reviewer B freezes findings without reading `reviewer-a/` |
| — Cross-examination | `CROSS-EXAMINATION.md` | per disputed finding: strongest argument, counterargument, discriminating evidence, status |
| IV Principle extraction | coverage/exclusion/generalization arguments for any compression | admitted defects only |
| V Candidate design | minimal repair per defect at highest correct owning layer (remove > rewire > modify > add) | traceability chain complete |
| VI Implementation | canonical source + regenerated descendants on this branch | accepted design only |
| VII Qualification | pre-registered A/B, holdout, ablation, mutation (see design) | trial infrastructure available; required checks executed |
| VIII Independent assembled-candidate Review | fresh-context Review record | no author conclusions inherited |

A phase may not be entered because a plausible idea exists; it is entered only when its gate is met.

## Independence and contamination protocol

- Reviewer A's artifacts live only under `qualification/ssdp65/reviewer-a/`. They are committed before reviewer B starts, so their content is fixed.
- Shared, finding-free inputs for reviewer B: `P0-BASELINE-BINDING-PROTOCOL-6.4.md`, `BENCHMARK-AND-EVALUATION-DESIGN.md`, `INDEPENDENT-DIAGNOSTIC-HANDOFF.md`, this workplan's non-disposition sections, and the P0 repository itself.
- Reviewer B must not open `qualification/ssdp65/reviewer-a/` (or this branch's commit messages describing it) until reviewer B's own findings are committed under `qualification/ssdp65/reviewer-b/`.
- Disagreements are resolved by evidence, counterexample, formal argument or qualification — never by model prestige, majority or confidence.

## Project Engineering Memory activation and HAS

PEM is activated: this is mature protocol rework with suspected recurrence. The self-hosted memory's accepted-base selection policy is not declared by the project (see reviewer A's defect model); the basis below is therefore recorded with explicit uncertainty.

```yaml
pem_basis:
  accepted_project_state: 55c085261eb827e3047637d045a8e6917ea6b962
  accepted_pem: 55c085261eb827e3047637d045a8e6917ea6b962:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: NONE
has:
  - id: FF-001
    disposition: APPLICABLE
    reason: Any successor lifecycle must not publish immutable fallback source before its semantics are final.
  - id: PC-001
    disposition: APPLICABLE
    reason: Frozen 5.16-6.4 profiles/resources and recovery semantics must remain byte/behavior stable under any candidate.
  - id: SP-001
    disposition: APPLICABLE
    reason: Repairs to routing/representation should occur at canonical owners followed by regeneration, never by editing derivatives.
```

The memory front matter still reads `maintained_under_protocol: 6.3.0`, `reconciled_through` = Protocol 6.2 recovery and a Protocol 6.3 candidate-overlay label; `coverage_state: PARTIAL`. Absence of an entry is therefore not evidence of absence, and bounded historical intake was performed in Phase II.

## Acceptance for this workplan

This workplan may close only when one of the following is established and recorded:

1. **6.4 survives** — the frozen, cross-examined defect model contains no blocking or material defect warranting a protocol change; or
2. **Patch route** — admitted defects are corrections within 6.4 semantics and are delivered as a version-bound 6.4.x patch through the owner's normal process; or
3. **Successor accepted** — P1 satisfies every criterion in `BENCHMARK-AND-EVALUATION-DESIGN.md` §4, including independent assembled-candidate Review PASS and human acceptance where the project assigns it.

A required check that did not execute blocks closure. Unresolved Serious Challenge blocks unqualified closure.

## Open decisions requiring the human stakeholder

1. **Protocol-version acceptor.** Confirm who ratifies acceptance of an SSDP protocol version (human stakeholder, merge to `main`, or Review PASS alone).
2. **Supported model envelope** `M` for Phase VII.
3. **Downstream-project access** for holdout HO3 (for example `hjin98/mdstats`).
4. **Trial infrastructure** for matched A/B agent trials.
5. Whether admitted current-state defects in accepted 6.4 should be corrected immediately as a 6.4.x patch independent of the successor investigation.

## Reopen triggers

- Reviewer B produces a finding that contradicts a reviewer-A blocking or material finding with admissible evidence.
- A benchmark element is shown defective (apply design §8).
- Accepted 6.4 source changes on `main` before cross-examination (rebind P0 explicitly; do not silently rebase).
