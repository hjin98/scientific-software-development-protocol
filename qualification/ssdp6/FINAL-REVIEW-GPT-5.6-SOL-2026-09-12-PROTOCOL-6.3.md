---
kind: ssdp63-independent-protocol-review
protocol_version: 6.3.0
reviewer: GPT-5.6 Sol
date: 2026-09-12
authority: independent-review-evidence
status: pass
accepted_baseline_protocol: 6.2.0
accepted_baseline_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_baseline_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted_baseline_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
semantic_candidate: 190c8b4d352c203ef74c94d57c4f18d30eb7186d
public_source_bootstrap: dc22f09fd38dbbfeaeb0160152da9b284654f66e
f5_qualification_commit: 092c784383868081e9dee2081e3895f3d1263630
stage_f_evidence_reconciliation_descendant: f8b0c0705afec7fd97a38a6eed090714ae53beb7
reviewed_branch_head_before_review: df779ac21bf113d83b21f2f677a284e76e7db962
blockers: 0
serious_challenges: 0
stage_g_performed: false
recovery_mapping_published: false
---

# Protocol 6.3 Independent D3 / Protocol Review

## Disposition

**INDEPENDENT REVIEW: PASS.**

I found no Serious Challenge to accepted Protocol 6.2 authority and no genuine blocking defect in the assembled Protocol 6.3 semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d`.

The candidate preserves the accepted Protocol 6.2 T01-T39 contract while implementing the bounded Protocol 6.3 Project Engineering Memory (PEM) design through the still-binding T40-T120 workplan contract. The final D9 repair closes the previously observed same-ID semantic-identity laundering defect and rebinds current-facing Stage-F evidence to the exact repaired candidate without broadening the architecture.

This PASS closes only the independent Review gate required before Stage G. It does **not** itself publish or choose Protocol 6.3 recovery, make Protocol 6.3 accepted-current, archive the workplan, reconcile Protocol 7, or authorize `main` cutover. Protocol 6.2 remains accepted-current until Stage G closes separately.

No workplan repair/reopen is required because no blocking owner defect remains.

## Independence basis

The review reconstructed the assembled candidate against accepted Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0`, the active Protocol 6.3 workplan, the actual canonical 6.3 owners, the PEM validator, executable D8/D9 counterfactuals, generated/package/profile surfaces, preservation census, static activation sensors, and ordinary CI. Implementer summaries, F5 labels, green CI, and prior Review conclusions were treated as evidence rather than authority.

The semantic subject is the immutable candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d`. Later descendants contain qualification publication, handoff/evidence reconciliation, test-oracle strengthening, and temporary-workflow cleanup; no later canonical `source/` semantic mutation supersedes the reviewed candidate.

## Exact identities and evidence chronology

| Surface | Identity / disposition |
| --- | --- |
| Accepted Protocol 6.2 recovery | `b59adc77efe6951912cfd705cc43830c58ca27d0` |
| Accepted Protocol 6.2 semantic candidate | `ebbc4591bdfed039512026b8acb3a6749475c1c5` |
| Accepted Protocol 6.2 public bootstrap | `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` |
| Historical F4 NO-PASS candidate | `42eb89388dc96879157ba92db9e7f3c59f2c0b36` |
| Reviewed Protocol 6.3 semantic candidate | `190c8b4d352c203ef74c94d57c4f18d30eb7186d` |
| Protocol 6.3 public-source bootstrap | `dc22f09fd38dbbfeaeb0160152da9b284654f66e` |
| F5 qualification publication | `092c784383868081e9dee2081e3895f3d1263630` |
| Stage-F evidence reconciliation descendant | `f8b0c0705afec7fd97a38a6eed090714ae53beb7` |
| Clean branch head reviewed as assembled descendant | `df779ac21bf113d83b21f2f677a284e76e7db962` |
| Ordinary final CI at clean head | run `34695322057` |

The evidence chronology is intentionally not flattened. F5 publication `092c7843...` was followed by a real Stage-F evidence correction: current-facing census text still contained F2-era identities and the D8-02 executable oracle omitted the already-required overlay self-ratification discriminator. Descendant `f8b0c070...` corrected those evidence bindings and added the missing discriminator. The underlying candidate implementation already rejected overlay self-ratification, so this was an evidence/oracle defect rather than a new semantic-source mutation. The strengthened discriminator passes in the final assembled branch regression.

Accordingly, `092c7843...` remains historical F5 publication evidence; `f8b0c070...` is the evidence-reconciliation descendant that closes the current-facing Stage-F record. Neither identity is substituted for the reviewed semantic candidate.

## Blocking-finding disposition

### D9-01 — same-ID semantic reconciliation: CLOSED

The canonical PEM validator now mechanically rejects same-ID changes to kind, owner class, mechanism family, normalized governing claim, applicability dimensions, and applicability broadening/change-of-regime. Claimant-authored `WITHIN_ENVELOPE` cannot launder those mechanically material changes.

Only mechanically bounded presentation normalization and true applicability narrowing may proceed under same-ID reconciliation. Those continuations still require the previous semantic signature, an explicit reason, and durable evidence that realizes as `HEALTHY`. Reconciliation evidence participates in the ordinary material-route and binding-health path.

The executable discriminator covers mechanism changes, governing-claim replacement, applicability broadening, applicability-dimension replacement, healthy narrowing/editorial continuation, and unhealthy reconciliation evidence.

### D9-02 — exact-candidate Stage-F binding: CLOSED

The current preservation census, static activation sensor record, implementation-state record, F5 lineage, and independent-review handoff consistently identify semantic candidate `190c8b4d...`. Earlier F2/F3/F4 identities remain explicit historical provenance rather than current acceptance subjects.

Static activation active sets and candidate-side bytes are bound to the exact semantic candidate. The record preserves the distinction among semantic candidate, public-source bootstrap, later publication/qualification descendant, and unavailable pre-Stage-G recovery.

### B4.2 — overlay basis and self-ratification: CLOSED

The overlay validation path requires the exact externally selected accepted PEM publication and rejects an overlay whose candidate identity equals the accepted memory identity. The later Stage-F repair added the workplan-required `C == M` self-ratification counterfactual to executable qualification; the final assembled regression passes it.

## Protocol 6.2 preservation and architecture

The accepted 6.2 architecture remains recognizable and authoritative: D1-D4 authority separation, evidence-not-authority, bounded invalidation, real-owner acceptance, abstraction-adequacy Review, Serious Challenge routing, minimum/cohesive ownership, and preference for reduction/rewiring/removal before compensating machinery are retained.

Protocol 6.3 adds PEM as a project-local, evidence-backed, non-authoritative learning representation rather than a fifth semantic authority domain. It remains conditionally routed for mature replacement/recovery/history-sensitive work instead of being eagerly activated on ordinary work. Canonical ledger/detail state remains distinct from derived summaries and salience; temperature does not select authority or applicability.

I found no new database/registry/daemon/global-history service, no competing architecture owner, and no wrapper layer that substitutes for correction at the existing owner seams.

## Four inherited Challenge dimensions

- **Loss:** PASS. Accepted Protocol 6.2 T01-T39 obligations remain represented, and Protocol 6.3 adds bounded T40-T120 semantics without deleting lower-salience mandatory owners.
- **Scope/materiality laundering:** PASS. Coverage/watermark separation, HAS basis, overlay identity, same-ID semantic-envelope checks, and counterevidence/evidence-health rules prevent missing or claimant-authored scope from becoming silent permission.
- **Priority inversion:** PASS. Unresolved high-impact notices, unavailable/material warrants, authority-binding uncertainty, and mandatory lower-salience constraints are not displaced by positive-pattern ranking or temperature.
- **False compaction:** PASS. Derived summaries remain non-authoritative views over canonical family/notice ledgers; cold canonical detail and owner routes remain recoverable when triggered.

## Routing, generated artifacts, and frozen resources

Static routing evidence keeps PEM cold for ordinary local D4 repair, ordinary D3 workplan/review, D1/D2 design, documentation, maintenance audit without admitted reusable-learning predicate, release reconciliation, and closeout without material learning. PEM becomes active for historical recovery/migration where prior choices matter and mature D3 replacement with demonstrated project history.

The final clean PR workflow run `34695322057` passed full protocol regression, canonical skill-package build, independent package validation, committed distribution parity, whitespace checks, packaged Protocol snapshot parity, and Orchestrator Core acceptance. Frozen 5.16/6.0/6.1/6.2 resource identities remain preserved; 6.3 is a distinct generated profile/resource set.

## Lifecycle boundary

The public-source fallback is the already-existing immutable bootstrap `dc22f09fd38dbbfeaeb0160152da9b284654f66e`, published by a later descendant. It is distinct from the reviewed semantic candidate `190c8b4d352c203ef74c94d57c4f18d30eb7186d` and is not recovery.

Under the established Protocol 6.2 precedent, the final corrected Review PASS commit may be selected as the immutable Protocol 6.3 recovery target because it contains the reviewed semantic candidate and required qualification/evidence/Review record through ancestry. Git commits cannot self-name, so any `6.3.0 -> <recovery SHA>` mapping must be published only by a later descendant.

Stage G must then regenerate mapping-bearing descendants, run targeted recovery/bootstrap-distinction/parity/package/profile/Core checks, reconcile Protocol 7 and semantic history, and only after those gates pass may Protocol 6.3 become accepted-current, the workplan be archived, and `main` be cut over.

## Completion boundary

**Independent Protocol 6.3 D3 / Protocol Review: PASS.**

Blockers: **0**. Serious Challenges: **0**.

This record intentionally stops before Stage G and does not manufacture lifecycle closure.
