---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: replacement-bootstrap-repaired-independent-review-r2-pending
accepted_current_protocol: 6.2.0
accepted_rollback_commit: b59adc77efe6951912cfd705cc43830c58ca27d0
semantic_candidate: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
protocol_63_public_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
protocol_63_public_bootstrap_mapping: a8dac814cc2813b3bb336e5b6abde5fbcf44949e
stage_f_static_sensor_commit: 092c784383868081e9dee2081e3895f3d1263630
stage_f_qualification_commit: 092c784383868081e9dee2081e3895f3d1263630
stage_f_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md
independent_review: r2_pending_after_bootstrap_repair
protocol_63_recovery: unavailable_pending_r2_review
---

# Protocol 6.3 Implementation State

## Current disposition

Protocol 6.3 D9 implementation-context repair is complete for immutable semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d`. Protocol 6.2 remains accepted-current at recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`. This record does not claim independent Review PASS, Protocol 6.3 recovery, lifecycle acceptance, workplan closure, or `main` cutover.

The F2/F3/F4 candidates and qualification records remain immutable historical evidence. Independent Review of F4 candidate `42eb89388dc96879157ba92db9e7f3c59f2c0b36` falsified the D8-01 oracle and found stale current-facing candidate bindings; those PASS labels do not establish current acceptance.

## D9 repair closure

The existing reconciliation path now treats changed kind, owner class, mechanism family, normalized governing claim, applicability dimensions, and applicability broadening/change as mechanically material same-ID drift requiring lineage. Only mechanically demonstrable presentation normalization or true applicability narrowing may reach `WITHIN_ENVELOPE` reconciliation, and those cases still require durable `HEALTHY` evidence. Reconciliation evidence is included in ordinary material-route/binding-health realization. The focused D8-01 test now falsifies governing-claim laundering, applicability broadening, applicability-dimension replacement, unhealthy reconciliation evidence, and confirms valid narrowing/editorial continuation.

## F5 qualification

The exact candidate passed the focused D9 repair tests, full repository unittest discovery, self-hosted PEM validation, canonical build/package/dist validation, Protocol 6.3 snapshot check, Orchestrator Core acceptance, whitespace checks, and exact-candidate remeasurement of all eleven static activation active sets. Frozen prior-version/resource invariants remain covered by the full repository and Orchestrator acceptance surfaces.

The D9 source mutation invalidated the prior D4R3 bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e`. F5 evidence incorrectly described semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d` as if it were itself the replacement public bootstrap even though that immutable candidate still embedded `dc22f09fd38dbbfeaeb0160152da9b284654f66e` as its fallback. Promotion review exposed this lifecycle defect. Replacement self-reference-safe source snapshot `86c13cab6bdd1991dffa94e277db8eacf87e2e11` was therefore constructed with the public fallback deliberately unavailable, fully qualified before publication, and only later published by descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e`. The semantic candidate, public bootstrap, publication descendant, and unavailable recovery are now distinct identities.

## Remaining gate

Fresh independent assembled-candidate Protocol/D3 Review R2 is required over semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d` together with repaired bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11` and publication descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e`. Earlier Review-PASS attempts are superseded by the subsequently discovered bootstrap-publication blocker. Stage G, recovery, accepted-current promotion, workplan archive, and `main` cutover remain blocked until R2 passes.
