---
kind: ssdp63-implementation-state
protocol_version: 6.3.0
branch: ssdp-6.3-engineering-memory
authority: implementation-progress-evidence
status: reopened-stage-f-implementation-qualification-complete-independent-review-pending
accepted_current_protocol: 6.2.0
accepted_rollback_commit: b59adc77efe6951912cfd705cc43830c58ca27d0
semantic_candidate: 7f6774156e8595ac9a04227e1c0be30783525a67
protocol_63_public_bootstrap: 5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb
protocol_63_public_bootstrap_mapping: 1bfb78947eb0b94a58ec8ff4f2828538f3d4702f
mapping_bearing_generated_descendant: 7f6774156e8595ac9a04227e1c0be30783525a67
stage_f_static_sensor_commit: be4cfc1692a64d6bfb69841fb2eac383cc260ad2
stage_f_qualification_commit: 5f52fbdf05c62b307b5627d99989209578d1d95a
stage_f_qualification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-REOPENED-STAGE-F.md
independent_review: pending_fresh_context
protocol_63_recovery: unavailable_pending_independent_review
---

# Protocol 6.3 Implementation State

## Current disposition

The reopened Protocol 6.3 owner-layer repairs and implementation-context Stage-F requalification are complete. The repaired immutable semantic candidate is `7f6774156e8595ac9a04227e1c0be30783525a67`.

Protocol 6.2 remains accepted-current at recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`. Protocol 6.3 is still candidate state. This record does **not** claim independent Review PASS, Protocol 6.3 recovery, lifecycle acceptance, workplan closure, or `main` cutover.

The former candidate `8d0ad2395ccd126c133d8aad206cfc859f660124`, old public bootstrap `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, and old 260/260 report remain historical evidence only. They are not current Stage-F acceptance identities.

## Reopened repair closure

- **D1 durable evidence binding:** complete. Evidence routes are structured and current-repository material bindings must resolve through an immutable commit/tree-ish plus existing path. Blob-as-revision and missing-path counterfactuals fail. Self-hosted `PC-001` routes now bind immutable repository publications that actually contain the named evidence files.
- **D2 logical publication coherence:** complete. Optional partition declarations use root-owned SHA-256 content identity and exact project/repository/scope/accepted-base/candidate-overlay basis agreement. Mixed root/partition revisions fail closed.
- **D3 immutable observation lineage:** complete. Admissible occurrence/application evidence requires an observation. Reconciliation of the same accepted event/application cannot rewrite observation without explicit clerical-correction provenance preserving prior hash, reason, and evidence.
- **D4 recurrence lineage:** complete. Recurrence requires prior occurrence identity, accepted-repair identity/evidence, a later independent event matching the current event, and an independence basis. Truthy labels, timestamps, aliases and copies are insufficient.
- **D5 maturity/independence:** complete. `PROVEN` is claim-relative and obligation-backed; independence-sensitive obligations require distinct provenance clusters. Count, temperature, repeated use, reviewer vote, or common policy/harness cannot manufacture proof.
- **D6 notices:** complete. Typed/evaluable triggers replace opaque freshness semantics. A fired or indeterminate CURRENT notice routes to review rather than stale guidance.
- **D7 accepted-base/HAS/overlay:** complete. HAS and overlays pin exact accepted project state, accepted PEM and branch overlay; self-ratification, silent deletion-by-omission and unreconciled basis advance fail.

## Replacement bootstrap lifecycle

The repaired public bootstrap sequence now follows the accepted 6.2 self-reference discipline:

```text
replacement self-reference-safe source snapshot:
  5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb

later mapping commit that names the already-existing snapshot:
  1bfb78947eb0b94a58ec8ff4f2828538f3d4702f

mapping-bearing generated descendant / repaired semantic candidate:
  7f6774156e8595ac9a04227e1c0be30783525a67
```

The bootstrap snapshot passed readiness before publication. Exact-ref public realization then passed before the mapping-bearing descendant was accepted by the publication workflow. Final mapped-descendant run `34666676704` passed full repository tests, PEM validation, canonical build, standalone package validation, dist parity, 6.3 snapshot/profile parity, Orchestrator Core, whitespace, clean-tree and frozen-prior-resource checks.

No temporary bootstrap/diagnostic workflow remains in `.github/workflows/`; only the ordinary `protocol-check.yml` remains.

## Static activation evidence

`qualification/ssdp6/SSDP-6.3-STATIC-ACTIVATION-SENSORS.md` was freshly rebound to `7f677415...` at evidence commit `be4cfc1692a64d6bfb69841fb2eac383cc260ad2`.

The fixed routing predicates/topology remained unchanged. Exact Git-blob byte totals were recomputed from the repaired candidate instead of carrying forward stale pre-repair values. The evidence is structural only: it makes no live token, latency, cache, attention, productivity, or model-quality claim.

## Reopened Stage-F qualification

Replacement implementation-context Stage-F evidence is:

`qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-REOPENED-STAGE-F.md`

at commit `5f52fbdf05c62b307b5627d99989209578d1d95a`.

It explicitly treats the old `8d0ad239...`/`1484c1d...` 260/260 report as historical only and freshly accounts for:

```text
115 inherited Protocol 6.2 scenarios   PASS
79 Q63 scenarios                       PASS
62 F63 adversarial cases               PASS
4 inherited Challenge passes           PASS
--------------------------------------------
260 implementation-context decisions   PASS
```

The repaired high-risk rows are bound to current discriminators for durable binding, partition coherence, observation correction lineage, accepted-repair recurrence, provenance-aware maturity, notice triggering and accepted-base/HAS/overlay composition.

## Frozen/generated integrity

The repaired mapped descendant preserves frozen 5.16/6.0/6.1/6.2 resources. `dist/`, Protocol 6.3 profile/prompts/snapshot and Core resource descendants are generated from canonical source and pass parity/closure tests. Live project PEM is not packaged as generic protocol state.

## Independent Review boundary

Implementation context stops here. The next required gate is a **fresh independent assembled-candidate Protocol/D3 Review** against candidate `7f6774156e8595ac9a04227e1c0be30783525a67` and accepted Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`.

The independent reviewer must not inherit this file, the replacement 260/260 result, preservation labels, or green CI as authority. It must reconstruct the assembled candidate and attempt falsification, including D1-D7, replacement bootstrap, generated/frozen integrity, all four Challenge dimensions and the reopened workplan contract.

Until that Review passes:

```text
Stages A-D: COMPLETE
Stage E replacement bootstrap/profile/generated lifecycle: COMPLETE through pre-recovery boundary
Stage F implementation-context qualification: COMPLETE — 260/260
Independent assembled-candidate Review: PENDING
Protocol 6.3 recovery: UNAVAILABLE
Stage G: BLOCKED
Accepted-current protocol: 6.2.0
Workplan: ACTIVE
Main cutover: NOT AUTHORIZED
```

No implementation-context commit may mark T68, Stage G, recovery, accepted-current status or workplan archive closed on its own.