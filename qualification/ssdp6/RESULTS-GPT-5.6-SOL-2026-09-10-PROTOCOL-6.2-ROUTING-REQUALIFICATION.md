---
kind: ssdp62-affected-requalification-result
protocol_version: 6.2.0
profile_id: ssdp-protocol-6.2
candidate_under_test: 6f71812fe79bb9996fa467cc68dfe8d988d278d6
prior_candidate: 610360683f0d36deaaeabd1e0ffc3c7127ea8374
prior_qualification_evidence: 039e36da59eed0b2339a949a5b5a9d12cabf5ec2
repair_source_commit: dbb0db8c52a3f50a4cb7ee6a30b01028f419ea6a
repair_generated_commit: 6f71812fe79bb9996fa467cc68dfe8d988d278d6
public_source_bootstrap: 1181c2031710c5d343194d87d08543290fded0ab
status: pass
independent_review: pending
authority: non-normative-qualification-evidence
---

# Protocol 6.2 Affected Requalification After Documentation Cold-Route Repair

## Disposition

**AFFECTED REQUALIFICATION PASS.** The prior 115-case run remains applicable for semantic decisions outside the repaired routing/package surface. The final semantic candidate is now `6f71812fe79bb9996fa467cc68dfe8d988d278d6`, not `610360683f0d36deaaeabd1e0ffc3c7127ea8374`.

This result is qualification evidence, not lifecycle acceptance. Protocol 6.1 remains accepted-current/rollback until independent Review and Stage G complete.

## Defect discovered after the original 115-case run

Author-owned adversarial pre-review found that `source/specialists/software-documentation/SKILL.md` declared four conditional concern routes only as prose — security, performance, storage, and release “direct concern owners” — without resolvable Markdown resources. The standalone package builder follows local Markdown reachability, so those four owners were omitted from `dist/skills/software-documentation/references/`.

That state violated the Protocol 6.2 routing/portability contract:

- an activation edge must identify a visible decision predicate and resolvable resource;
- every supported activated resource must remain source/package reachable;
- package membership is not activation, but missing package membership for a required activated resource is a cold-path defect.

The repair replaced the four implicit routes with explicit conditional links to `security-and-trust-boundaries.md`, `performance-and-parallelism.md`, `storage-and-io.md`, and `release-and-distribution.md`. Canonical `source/` remains authoritative; `dist/` was regenerated from `source/build_skills.py` rather than hand-edited.

## Executed repair evidence

One-shot materialization run `34550234097` passed:

- canonical skill distribution regeneration;
- focused Protocol 6.2 representation regression;
- independent package validation;
- whitespace validation;
- generated commit and automatic removal of the temporary materializer.

The focused regression now requires both explicit route declaration and installed-package presence for all four owners. Direct repository inspection at `6f71812...` confirms the previously absent `dist/skills/software-documentation/references/security-and-trust-boundaries.md` is present. The other three are protected by the same executed regression/package-validation step.

The repository again contains only the ordinary `protocol-check.yml` workflow.

## Evidence applicability and affected scenario requalification

The repair changes route resolvability/package closure only. It does not alter D1-D4 authority, evidence semantics, Challenge thresholds, version mappings, orchestration profile topology, or the substantive content of the four concern owners. Therefore unaffected decisions from the 115-case qualification remain reusable under the evidence-applicability rule.

Affected/rechecked obligations:

| Surface | Result | Requalification |
|---|:---:|---|
| Case 59 — generated artifact drift | PASS | `dist/` was regenerated from canonical source; no derivative was hand-authored as authority. |
| Case 102 — ordinary links do not activate | PASS | The new links are resources named inside conditional router prose. Presence/reachability does not itself activate them. |
| Case 103 — required conditional resource activation | PASS | When a documentation task materially represents security/performance/storage/release content, the relevant owner now has a resolvable local resource and packaged copy. |
| Case 104 — cycle/back-edge rejection | PASS | The four direct concern edges add no ancestor reload or activation cycle. |
| Case 105 — router prose remains authority | PASS | The specialist router itself owns the decision predicates; no graph/package manifest becomes a second routing authority. |
| Representative documentation-reconciliation trace | PASS | `software-documentation` -> universal/documentation owners -> only the materially represented concern owner; all four repaired cold routes are now reachable. |
| Standalone package transport | PASS | Focused regression + package validator establish source-link/package closure for the repaired routes. |

No live-harness context/token/performance claim is introduced. Static route/package correctness remains distinct from empirical model context use.

## Qualification impact

The original 115-case report is retained as historical evidence for the prior candidate, not silently relabeled as evidence for a changed candidate. Its unaffected scenario decisions remain applicable because the repaired change cannot alter their governing propositions or execution dependencies. The table above restores applicability for the materially affected routing/package claims.

Any further semantic mutation after `6f71812...` must again assess qualification applicability and, where material, establish a new candidate identity.

## Independent-review boundary

Independent Review must review `6f71812fe79bb9996fa467cc68dfe8d988d278d6` as the semantic candidate and must explicitly inspect this repair rather than relying on the earlier `6103606...` qualification identity. The reviewer remains free to reject the applicability argument above and demand broader requalification if a wider semantic dependency is found.
