---
kind: ssdp63-independent-review-handoff
protocol_version: 6.3.0
authority: non-normative-review-handoff
semantic_candidate: 7f6774156e8595ac9a04227e1c0be30783525a67
qualification_result_commit: 5f52fbdf05c62b307b5627d99989209578d1d95a
qualification_result: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-REOPENED-STAGE-F.md
static_sensor_evidence_commit: be4cfc1692a64d6bfb69841fb2eac383cc260ad2
public_source_bootstrap: 5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb
public_source_mapping_commit: 1bfb78947eb0b94a58ec8ff4f2828538f3d4702f
accepted_protocol_62_recovery: b59adc77efe6951912cfd705cc43830c58ca27d0
accepted_protocol_62_public_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
accepted_protocol_62_semantic_candidate: ebbc4591bdfed039512026b8acb3a6749475c1c5
independent_review: required_fresh_context
protocol_63_recovery: unavailable_pending_review
accepted_current_protocol: 6.2.0
---

# Independent Protocol/D3 Review Handoff — Protocol 6.3 Reopened Candidate

## Reviewer mandate

Perform a **fresh independent assembled-candidate Protocol/D3 Review** of semantic candidate `7f6774156e8595ac9a04227e1c0be30783525a67` against accepted Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0` and the active Protocol 6.3 workplan.

Do not inherit implementation conclusions from the authoring context. Do not review only the PR diff, this handoff, green CI, preservation labels, the old 260/260 report, or the replacement 260/260 report. Reconstruct the governing semantics and inspect the assembled candidate at the exact candidate commit. Treat all qualification artifacts as evidence to challenge, not authority.

If a genuine blocker exists, identify the earliest owning layer and precise repair obligation and keep Stage G blocked. If none exists, record an independent Review PASS as a new descendant evidence commit. The Review itself must **not** establish recovery, accepted-current status, workplan archive, or `main` cutover.

## Immutable identity set

```text
accepted Protocol 6.2 recovery:           b59adc77efe6951912cfd705cc43830c58ca27d0
accepted Protocol 6.2 semantic candidate:  ebbc4591bdfed039512026b8acb3a6749475c1c5
accepted Protocol 6.2 public bootstrap:    5a062ebc472755607b9dc66d33a5ebbc4b7429aa

invalidated historical 6.3 bootstrap:       1484c1d3caa49d87cc15bc52a5e775399c1dae1b
invalidated historical 6.3 candidate:       8d0ad2395ccd126c133d8aad206cfc859f660124

replacement 6.3 public bootstrap:          5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb
later bootstrap mapping commit:             1bfb78947eb0b94a58ec8ff4f2828538f3d4702f
repaired mapped semantic candidate:         7f6774156e8595ac9a04227e1c0be30783525a67
refreshed static-sensor evidence:            be4cfc1692a64d6bfb69841fb2eac383cc260ad2
replacement Stage-F qualification commit:   5f52fbdf05c62b307b5627d99989209578d1d95a
Protocol 6.3 recovery:                       UNAVAILABLE
```

The old `8d0ad239...`/`1484c1d...` qualification chain is historical only because independent review falsified owner/oracle behavior and forced D1-D7 plus replacement-bootstrap repair. The replacement report does not rehabilitate those identities.

## Governing surfaces

Review at minimum:

- `workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md`;
- `qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md`;
- `qualification/ssdp6/IMPLEMENTATION-STATE-PROTOCOL-6.3.md`;
- `qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-REOPENED-STAGE-F.md`;
- `qualification/ssdp6/SSDP-6.3-STATIC-ACTIVATION-SENSORS.md`;
- PEM owner `source/shared/references/project-engineering-memory.md`;
- evidence owner `source/shared/references/evidence-evolution-and-dependencies.md`;
- workflow/HAS owner `source/shared/references/workflow-and-workplans.md`;
- convergence/family/recurrence owner `source/shared/references/convergence-and-cycle-economy.md`;
- D3 capability owner `source/shared/references/architecture-and-design.md`;
- testing/validation, repository-intake, Git/version-control, trust-boundary and versioning owners;
- D1/D2/D3/D4 and specialist routers;
- PEM template and executable validator `source/project_engineering_memory.py`;
- self-hosted `PROJECT-ENGINEERING-MEMORY.md`;
- `tests/test_protocol_63_engineering_memory.py`, `tests/test_protocol_63_reopened_repairs.py`, `tests/test_protocol_63_bootstrap.py`;
- generated `dist/`, Protocol 6.3 profile/prompts/snapshot, and frozen prior version resources.

## Reopened repair obligations to falsify independently

### D1 — durable evidence resolution

Material evidence routes are structured as source identity + immutable revision/artifact identity + path/artifact + optional stable locator. For the current repository, a material route claiming repository-path semantics must resolve the revision as a commit/tree-ish and the path at that revision; a blob SHA cannot masquerade as a repository revision. Non-local evidence needs unambiguous source repository/project identity.

Attempt at least: nonexistent revision, blob-as-revision path binding, missing path, ambiguous non-local source identity, and previously healthy material evidence becoming unavailable. Inspect self-hosted `PC-001`; every route currently classified healthy must actually be resolvable under its declared semantics.

### D2 — atomic logical publication

Optional partitioned PEM remains one logical canonical memory. Root declarations bind exact partition content with SHA-256 and require agreement on schema/project/repository/scope/accepted-base/candidate-overlay meaning. A stale partition spliced into a newer root must fail even when family IDs and paths still look plausible.

Attempt a mixed-revision root/partition assembly and verify derived-index failure cannot become a second authority or hide canonical entries.

### D3 — immutable observation/assessment lineage

Every admissible occurrence/application that contributes current evidence requires a preserved observation/realization result. Reassessment/invalidation changes assessment/admissibility, not historical observation. Same accepted identity with changed observation requires explicit clerical-correction provenance preserving the previous observation hash, reason and evidence.

Attempt missing observation and silent same-identity observation mutation. Confirm causal interpretation remains separately warrantable.

### D4 — accepted-repair recurrence

`recurrence_after_accepted_repair` requires a prior occurrence, an identifiable accepted repair with evidence, a materially later independent event matching the current event, and an explicit independence basis. A truthy label, timestamp order, rebase order, alias, copy or cherry-pick cannot manufacture recurrence.

Attempt recurrence without accepted repair and recurrence via copy/common event.

### D5 — provenance-aware claim maturity and comparative guidance

`PROVEN` is claim-relative and obligation-backed. Every required obligation must be CLOSED with evidence; independence-sensitive obligations require at least two independent provenance clusters. Count, temperature, reviewer vote, repeated use or shared policy/implementation/harness does not establish independence.

Absolute success remains distinct from `PREFERRED`, `DEFAULT`, or `BEST`; comparative/default guidance requires comparative warrant or accepted owner priority. Overlapping incompatible guidance needs explicit regime/tradeoff/owner boundary or remains contested.

Attempt three supporting rows from one provenance cluster and attempt works-to-best/default laundering.

### D6 — notice trigger evaluation

Current notices use evaluable trigger semantics. A fired trigger or indeterminate trigger cannot remain silently CURRENT. The compatibility phrase for accepted-base change is only an interpreted legacy route, not permission for arbitrary opaque notice text.

Attempt an expired/deadline notice, an accepted-base-change notice after basis advance, and an opaque trigger. Each must route to review/fail closed rather than stale active guidance.

### D7 — accepted-base/HAS/candidate-overlay seam

Historical Applicability Set (HAS) and branch overlay validation pin exact accepted project state, accepted PEM identity and candidate overlay. Same-branch candidate memory cannot ratify itself as accepted base. Candidate omission cannot silently delete an accepted family. A material accepted-basis advance requires reconciliation before closeout.

Attempt self-ratification, deletion-by-omission, wrong overlay base and unreconciled basis advance.

## Replacement public bootstrap

The original public bootstrap `1484c1d...` was invalidated because it lacked repaired required semantics. The replacement lifecycle must satisfy the same self-reference discipline as accepted 6.2:

1. repaired source/profile/package state validates before a replacement SHA is named;
2. immutable replacement snapshot `5ee4b3ac...` already exists and intentionally does not self-name;
3. later descendant `1bfb789...` publishes the exact version-to-ref mapping;
4. mapping-bearing generated descendant `7f677415...` is regenerated from canonical source;
5. exact-ref remote realization, full repository regression, package/dist/snapshot parity, Core, whitespace and frozen prior-resource checks pass.

Independently inspect the bootstrap snapshot and later mapping. Reject any circular/self-ratifying reading where publication success is inferred from the mapping that only exists later.

## Self-hosted PEM state

`PROJECT-ENGINEERING-MEMORY.md` remains deliberately `PARTIAL`; no exhaustive-history claim is allowed. Reconstruct current rows from the file and validator rather than trusting this handoff.

Key review questions:

- every healthy current material evidence route is resolvable;
- occurrence/application observations are present and immutable under reconciliation;
- no timestamp/truthy-label recurrence exists;
- no common provenance is counted as independent proof;
- no evidence-only family mints D1-D4 authority;
- `reconciled_through` is not used as coverage completeness;
- accepted/base and branch overlay remain distinct;
- active summary cannot starve unresolved high-impact state behind positive guidance.

## Generated/package/profile/frozen integrity

Final mapped-descendant workflow run `34666676704` passed the complete publication gate. Independently sample rather than trusting that status:

- repository regression and focused Protocol 6.3 discriminators;
- self-hosted PEM validation;
- canonical package build and standalone link validation;
- committed `dist/` parity;
- Protocol 6.3 profile/prompts/snapshot parity;
- Orchestrator Core acceptance (390 tests);
- whitespace/clean-tree checks;
- byte/content integrity of frozen 5.16/6.0/6.1/6.2 resources;
- generic package exclusion of live project PEM.

The accepted-current profile remains Protocol 6.2 until Stage G. Protocol 6.3 profile is candidate/generated state only.

## Static activation evidence and non-claims

`qualification/ssdp6/SSDP-6.3-STATIC-ACTIVATION-SENSORS.md` was recomputed against exact candidate `7f677415...` and published at `be4cfc169...`. The active-set topology remained the same as the pre-repair measurement, while affected exact byte totals changed.

The evidence is deterministic static structure only. It does not prove live token count, attention, cache behavior, latency, productivity or model quality. Attempt both polarity failures: eager PEM activation for ordinary work and failure to activate PEM when demonstrated project history materially changes a mature recovery/replacement decision.

## Replacement Stage-F evidence to challenge

`qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-11-PROTOCOL-6.3-REOPENED-STAGE-F.md` at commit `5f52fbdf05c62b307b5627d99989209578d1d95a` records implementation-context 260/260:

- inherited scenarios 1-115;
- Q63-01 through Q63-79;
- F63-A through F63-BJ;
- Loss, Scope/materiality laundering, Priority inversion and False compaction.

Do not accept `260/260` by count. Sample the reopened/high-risk rows first: Q63-06, Q63-11, Q63-45, Q63-48, Q63-53, Q63-63, Q63-64, Q63-67, Q63-68, Q63-73, Q63-74, Q63-77, Q63-78 and corresponding F63-AB, F63-AE, F63-AT, F63-AU, F63-AX, F63-AY, F63-BD, F63-BE, F63-BH, F63-BI. Then verify complete-matrix accounting and inherited 6.2 preservation.

## Four mandatory falsification dimensions

Run all four independently against the assembled candidate:

1. **Loss:** remove a distinction needed for a future decision and verify preservation/owners reject the loss.
2. **Scope/materiality laundering:** shrink governed scope or omit a lower-salience requirement and verify it cannot manufacture PASS.
3. **Priority inversion:** let Hot/positive memory crowd out mandatory current constraints or unresolved high-impact evidence and verify it fails.
4. **False compaction:** replace progressive disclosure with recursive summaries, stale/incomplete indexes, eager history, collapsed provenance/lineage or duplicate authority and verify it fails.

## Review output contract

A valid independent result must state:

- exact candidate and accepted baseline reviewed;
- preservation reconstruction and sampled frozen/generated/package integrity;
- D1-D7 and replacement-bootstrap disposition;
- all four falsification-pass disposition;
- any genuine blockers with earliest owning-layer repair instructions;
- whether the replacement implementation-context evidence remains applicable;
- PASS/NO-PASS and Serious Challenge status.

If PASS, commit the independent Review result as descendant evidence only. Stage G is still a separate lifecycle step: choose a recovery descendant only after Review PASS, publish its mapping from a later commit, regenerate mapping-bearing descendants, rerun targeted recovery/profile/package/Core acceptance, reconcile accepted PEM/HAS/semantic-evolution/Protocol-7 lifecycle state, and archive the workplan only when those actions are complete.

Until then:

```text
independent Review: PENDING
Protocol 6.3 recovery: UNAVAILABLE
Stage G: BLOCKED
accepted current: Protocol 6.2
workplan: ACTIVE
main cutover: NOT AUTHORIZED
```