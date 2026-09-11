---
kind: ssdp62-affected-requalification-result
protocol_version: 6.2.0
profile_id: ssdp-protocol-6.2
candidate_under_test: ebbc4591bdfed039512026b8acb3a6749475c1c5
prior_candidate: 6f71812fe79bb9996fa467cc68dfe8d988d278d6
prior_routing_requalification: qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.2-ROUTING-REQUALIFICATION.md
public_source_bootstrap: 5a062ebc472755607b9dc66d33a5ebbc4b7429aa
invalidated_bootstrap_attempt: 1181c2031710c5d343194d87d08543290fded0ab
accepted_rollback_protocol: 6.1.0
accepted_rollback_commit: 802e75af261efb4f70d71284d860613a2197b639
clean_generated_evidence_head: 74ea3136eccb18119d35f39333047a7b24898452
clean_ci_run: 34556209092
executor_model: GPT-5.6 Sol
date: 2026-09-10
status: pass
live_routing_claim: unavailable
independent_review: pending
authority: non-normative-qualification-evidence
---

# Protocol 6.2 Affected Requalification After Public-Bootstrap Repair

## Disposition

**AFFECTED REQUALIFICATION PASS.** The Protocol 6.2 semantic candidate for the next independent Review is `ebbc4591bdfed039512026b8acb3a6749475c1c5`. The replacement immutable current-6.2 public-source bootstrap is the already validated prepublication source snapshot `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`.

This file is qualification evidence, not lifecycle acceptance and not independent Review. Protocol 6.1 remains accepted-current/rollback until the remaining independent Review and Stage-G gates complete.

## Why candidate identity changed

The prior semantic candidate `6f71812fe79bb9996fa467cc68dfe8d988d278d6` correctly repaired the `software-documentation` cold-route/package-reachability defect, but the then-published 6.2 public bootstrap `1181c2031710c5d343194d87d08543290fded0ab` predated that repair. The author-context Review therefore correctly rejected the bootstrap designation even though the current branch implementation was repaired.

The repair followed the workplan's anti-self-reference staging rather than adding a compatibility wrapper:

1. current source first stopped advertising `1181c...` as valid and truthfully reported automatic current-6.2 public fallback unavailable before replacement publication;
2. the resulting self-reference-safe source candidate `5a062ebc...` passed source regression, canonical skill-package build, and independent standalone package/link validation before designation;
3. only descendant `ebbc4591...` published `6.2.0 public-source bootstrap -> 5a062ebc...` and bound the workflow prompt/portability surfaces to that exact immutable ref;
4. generated `dist/` and the 6.2 orchestrator protocol snapshot were rebuilt from canonical source, not hand-edited, and the temporary materializer was removed;
5. clean descendant `74ea3136...` passed the complete ordinary repository/orchestrator acceptance suite.

The old `1181c...` SHA remains named only as an **invalidated bootstrap attempt** and is not a current fallback identity.

## Executed evidence

### Prepublication validation of the exact bootstrap snapshot

Run `34555947806` on `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` established, before publication:

- protocol source regression: PASS;
- canonical skill-package build: PASS;
- independent generated-package validation: PASS.

At this intentionally pre-generation point, committed `dist/` and orchestrator snapshot parity were expected to be stale and therefore were not used as bootstrap-eligibility evidence.

### Publication-time exact-ref oracle

Run `34556118366` on semantic candidate `ebbc4591bdfed039512026b8acb3a6749475c1c5` passed source regression, canonical package build, and standalone package validation while the generated descendants were intentionally still pending regeneration.

The Protocol 6.2 representation regression now does more than search for the SHA string. In continuous integration it resolves the published SHA against the public remote and verifies the **actual immutable snapshot**:

- `source/PROTOCOL_VERSION == 6.2.0`;
- all seven role/specialist `SKILL.md` entrypoints resolve at the exact SHA;
- each entrypoint reaches the current `abstraction-and-concretization.md` kernel;
- the repaired `software-documentation` security/performance/storage/release routes are explicitly named;
- recursively required local Markdown resources remain within the supported shared source roots and resolve at that exact SHA;
- the bootstrap snapshot itself retains the self-reference-safe/default-branch discipline.

Thus this is a content/reachability oracle for the mapped snapshot, not merely a mapping-text oracle.

### Final generated/assembled acceptance

A one-use workflow generated `dist/` and the 6.2 orchestrator snapshot from canonical source, produced `be072ca9ba0c64e3a4c7bd5647ea65ccb9db6edf`, and was removed immediately afterward. Clean head `74ea3136eccb18119d35f39333047a7b24898452` then passed ordinary run `34556209092`:

- source regression: PASS;
- canonical skill-package build: PASS;
- independent standalone package validation: PASS;
- committed `dist/` parity: PASS;
- whitespace: PASS;
- packaged Protocol snapshot parity: PASS;
- full Orchestrator Core acceptance: PASS.

No temporary materializer remains in the normal workflow set.

## Preservation-proof closure

`qualification/ssdp6/SSDP-6.2-PRESERVATION-CENSUS.md` now closes the other NO-PASS blocker at the required granularity. It contains:

- an artifact-level finite census for all seven entrypoints, all 33 current shared references, all four shared templates, navigation, qualification, profiles, generated descendants and historical surfaces;
- a transformation-level map T01-T39. Each material transformation records the accepted 6.1 owner/obligation, current 6.2 owner, preservation relation/evidence, and explicit `PRESERVED` disposition;
- no transformed obligation is intentionally marked superseded merely for compaction.

That map remains evidence to be falsified by independent Review rather than self-certified authority.

## Bounded semantic impact analysis

The bootstrap repair changes version-bound **current 6.2 public-source resolution** and its verification oracle. It does not change D1 scientific authority, D2 numerical authority, D3 architecture semantics, D4 implementation semantics, Challenge thresholds, evidence lifecycle, language/tool routing predicates, substantive concern-owner content, or frozen 5.16/6.0/6.1 resources. The replacement bootstrap points to the repaired current Protocol 6.2 source semantics rather than a different doctrine.

Therefore prior scenario decisions remain applicable outside the version/fallback and repaired-route dependency surface. The following high-risk cases were re-derived against the new candidate rather than silently inherited:

| Case/surface | Result | Current decision |
| --- | :---: | --- |
| 50 — frozen 5.16 work | PASS | Resolve frozen `sdp-protocol-5.16`; current 6.2 fallback does not reinterpret it. |
| 51 / 79 — frozen 6.0 work/profile | PASS | Resolve frozen `ssdp-protocol-6.0`; replacement 6.2 bootstrap does not change frozen semantics. |
| 80 — frozen/current 6.1 profile identity | PASS | Explicit 6.1 work continues under `ssdp-protocol-6.1`; 6.2 remains a distinct candidate successor. |
| 81 / 92 — historical identifiers/documents | PASS | Historical names/bytes remain version-faithful and do not authorize current obsolete vocabulary. |
| 94 / 114 — current vs frozen kernel path | PASS | Current 6.2 uses `abstraction-and-concretization.md`; frozen 6.1 retains its historical path. No current alias is introduced. |
| 95 — Protocol 6.1 public fallback | PASS | 6.1 remains pinned to `47e9155632c44493644b0b02fa1fa625703cf480`; the 6.2 replacement does not alter that mapping. |
| 101 — hierarchical language route | PASS | The replacement bootstrap contains root -> `language-profiles.md` -> triggered language leaf structure. |
| 102 — ordinary link non-activation | PASS | Remote/source/package reachability remains distinct from activation; the exact-ref oracle does not redefine package membership as activation. |
| 103 — required conditional leaf | PASS | Required leaves are resolvable at the replacement bootstrap when their owning router predicate fires. |
| 105 — router prose authority | PASS | The remote exact-ref check verifies canonical router prose/resources; its traversal is evidence and does not become routing authority. |
| 115 — pre-/post-bootstrap fallback | PASS | Before publication, automatic 6.2 fallback truthfully closed as unavailable. After publication, current 6.2 resolves exactly `5a062ebc...`; default/latest/guessed refs remain forbidden. |
| documentation cold-route transport | PASS | Exact remote bootstrap contains all four repaired explicit routes and recursively resolvable owner files. |

Cases 1-49, 52-78, 82-93, 96-100, 104, and 106-113 have no changed governing proposition or execution dependency from this bootstrap publication, so their earlier qualification remains applicable. The prior cold-route requalification remains part of the evidence chain for the `software-documentation` repair.

## Falsification passes for the repaired bootstrap

1. **Stale-bootstrap recurrence — PASS.** The old `1181c...` mapping is explicitly invalidated and tests reject it as current fallback.
2. **Default/latest substitution — PASS.** Current prompt/version/portability surfaces require the exact immutable replacement and retain truthful non-closure when compatible source cannot be read.
3. **Self-reference laundering — PASS.** `5a062ebc...` did not self-name; a later descendant publishes its SHA, matching the workplan staging rule.
4. **Reachability/activation conflation — PASS.** The remote oracle proves source/package route availability only. Canonical router predicates still determine activation; ordinary links/package membership remain non-activating.

## Static/live evidence boundary

The exact-ref public bootstrap check is a transport/source-resolution realization, not model-context telemetry. It establishes that the actual remote immutable source and routed resources exist and resolve. No claim is made about live model resource loading, token reduction, cache behavior, latency, or model performance. Existing static activation-sensor evidence remains descriptive and independently challengeable.

## Independent-review boundary

The remaining gate is still the workplan-required independent D3/protocol Review by a reviewer/context that did not author the candidate or this qualification evidence. That reviewer must treat `ebbc4591bdfed039512026b8acb3a6749475c1c5` as the semantic candidate, `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` as the public bootstrap, and the completed preservation map plus this requalification as evidence to falsify.

No Protocol 6.2 recovery commit is selected or published by this result.