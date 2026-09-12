---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: f5-implementation-qualification-complete-independent-review-pending
accepted_current_protocol: 6.2.0
accepted_rollback_commit: b59adc77efe6951912cfd705cc43830c58ca27d0
semantic_candidate: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
protocol_63_public_bootstrap: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
protocol_63_public_bootstrap_mapping: PENDING_F5_PUBLICATION_BINDING
stage_f_static_sensor_commit: PENDING_F5_PUBLICATION_BINDING
stage_f_qualification_commit: PENDING_F5_PUBLICATION_BINDING
stage_f_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-12-PROTOCOL-6.3-F5.md
independent_review: pending_fresh_context
protocol_63_recovery: unavailable_pending_independent_review
---

# Protocol 6.3 Implementation State

## Current disposition

Protocol 6.3 D9 implementation-context repair is complete for immutable semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d`. Protocol 6.2 remains accepted-current at recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`. This record does not claim independent Review PASS, Protocol 6.3 recovery, lifecycle acceptance, workplan closure, or `main` cutover.

The F2/F3/F4 candidates and qualification records remain immutable historical evidence. Independent Review of F4 candidate `42eb89388dc96879157ba92db9e7f3c59f2c0b36` falsified the D8-01 oracle and found stale current-facing candidate bindings; those PASS labels do not establish current acceptance.

## D9 repair closure

The existing reconciliation path now treats changed kind, owner class, mechanism family, normalized governing claim, applicability dimensions, and applicability broadening/change as mechanically material same-ID drift requiring lineage. Only mechanically demonstrable presentation normalization or true applicability narrowing may reach `WITHIN_ENVELOPE` reconciliation, and those cases still require durable `HEALTHY` evidence. Reconciliation evidence is included in ordinary material-route/binding-health realization. The focused D8-01 test now falsifies governing-claim laundering, applicability broadening, applicability-dimension replacement, unhealthy reconciliation evidence, and confirms valid narrowing/editorial continuation.

## F5 qualification

The exact candidate passed the focused D9 repair tests, full repository unittest discovery, self-hosted PEM validation, canonical build/package/dist validation, Protocol 6.3 snapshot check, Orchestrator Core acceptance, whitespace checks, and exact-candidate remeasurement of all eleven static activation active sets. Frozen prior-version/resource invariants remain covered by the full repository and Orchestrator acceptance surfaces.

The D9 source mutation makes prior public bootstrap `42eb89388dc96879157ba92db9e7f3c59f2c0b36` historical. The exact already-existing candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d` is published as the replacement 6.3 source fallback only by the later F5 evidence descendant; it remains distinct from unavailable Protocol 6.3 recovery.

## Remaining gate

Fresh independent assembled-candidate Protocol/D3 Review of `190c8b4d352c203ef74c94d57c4f18d30eb7186d` is required. Stage G, recovery, accepted-current promotion, workplan archive, and `main` cutover remain blocked until that Review passes.
