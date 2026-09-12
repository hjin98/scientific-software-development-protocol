---
kind: ssdp63-bootstrap-repair-reconciliation
protocol_version: 6.3.0
authority: non-normative-lifecycle-evidence
semantic_candidate: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
historical_d4r3_bootstrap: dc22f09fd38dbbfeaeb0160152da9b284654f66e
replacement_bootstrap: 86c13cab6bdd1991dffa94e277db8eacf87e2e11
replacement_bootstrap_publication: a8dac814cc2813b3bb336e5b6abde5fbcf44949e
accepted_current_protocol: 6.2.0
recovery: unavailable_pending_r2_review
---

# Protocol 6.3 Replacement-Bootstrap Reconciliation

Promotion review discovered that F5-era evidence had conflated semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d` with a valid public bootstrap. The candidate still embedded `dc22f09fd38dbbfeaeb0160152da9b284654f66e` as its public fallback and therefore could not satisfy the repository's self-reference-safe replacement-bootstrap lifecycle.

The repair created immutable snapshot `86c13cab6bdd1991dffa94e277db8eacf87e2e11` with public fallback deliberately unavailable, retained exact version-bound 6.2 fallback semantics and inherited self-reference-safe-source wording, and ran focused bootstrap/D8-D9 tests, complete unittest discovery, PEM validation, package/dist parity, Protocol snapshot parity, Orchestrator Core, and whitespace checks before committing that snapshot. Publication descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e` then named `86c13cab6bdd1991dffa94e277db8eacf87e2e11` and repeated the exact-ref bootstrap realization plus the full assembled acceptance surface before committing the mapping. Historical invalidated bootstrap identities were retained rather than compacted away.

This repair changes publication/lifecycle state and generated descendants only; it does not replace semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d`. The earlier Review-PASS records are historical attempts superseded by the blocker found during promotion. A fresh independent R2 Review is required before recovery or accepted-current promotion.
