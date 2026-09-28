---
kind: protocol-stage-f-portable-execution-architecture-repair
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date: 2026-09-28
status: repaired-pending-fresh-independent-review
basis_review: qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-NO-PASS-2026-09-28.md
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
active_serious_challenge: none
---

# Stage F portable execution architecture repair

## Scope

This repair responds only to the five blocking D3/qualification-contract defects in the fresh independent NO-PASS of the 62aa1bb portable architecture amendment. It changes no Protocol 7 semantic candidate bytes, scientific doctrine, fixture content, numerical floor, comparative target, human-trial floor or Stage G/H release semantics.

The portable-core + runtime-adapter boundary is retained. The repair makes the core own every semantic condition whose omission would otherwise become adapter discretion.

## B1 — execution-profile equality and hidden provider state

Closed in the repaired workplan/contract/amendment by:

- defining one execution-profile key over every exposed/controllable material condition;
- recording provider-managed unknowns without guessing;
- preclassifying each material unknown as arm-neutral stochastic/provider-managed or materially uncontrolled/not demonstrably arm-neutral;
- making the latter claim-scoped inadmissible;
- invalidating a pair on known provider/model/runtime migration.

This permits hosted/API/cloud profiles without asserting equality of hidden state that the interface cannot establish.

## B2 — capability equivalence, containment and custody

Closed by a core-owned versioned semantic capability manifest with `ALLOW`, `DENY`, and `SANDBOX/MEDIATE` scope over root/catalog, workspace access/mutation, process execution, delegation, issue/evidence stores, repository/object-store operations, network/external mutation, and credential/service-account access.

Unrestricted shell/code cannot bypass substrate containment. Prohibited live effects are blocked or redirected to qualification-owned stand-ins before the live effect. Regex-only detection is explicitly insufficient.

Machine-executor fixture/key denial is technical capability/credential separation. Audit supports that denial but does not replace it. The human-trial behavioral-access exception remains isolated to the frozen human trial.

## B3 — normalized trace and completeness

Closed by a core-owned minimum normalized event schema:

- catalog_snapshot
- root_selection
- resource_access
- tool_action
- delegate_call / delegate_return
- issue_evidence_access
- mutation
- network_external_action
- termination
- final_result
- usage_timing

Common fields bind schema/run/event identity, actor, kind, native-source linkage, status and exposed timing. Oracle-relevant identities and inputs are complete or losslessly artifact-referenced. Private chain-of-thought is not required.

Each adapter must emit a raw-to-normalized completeness map. Any unclassified/unmappable native observable capable of changing a required oracle makes the run inadmissible. Reduced summaries cannot drive zero-tolerance oracles.

## B4 — F6 exact scoring closure and fail-closed states

Closed by immutable run-bound manifests for required artifacts, required oracles and expected scoring items. The scoring manifest supplies stable item id, measure, criticality, branch and allowed dispositions. Valid assessment requires exactly one disposition for every expected applicable item, no duplicates and no unknown ids; unresolved applicability is explicit rather than omitted.

Evidence state is separate from transport success:

- COMPLETE_ADMISSIBLE
- INADMISSIBLE
- MISSING_REQUIRED_EVIDENCE
- MALFORMED_EVIDENCE_OR_ASSESSMENT
- EXECUTION_ERROR
- UNRESOLVED

Qualification outcome is separately PASS / FAIL / UNRESOLVED / NOT_EVALUATED. Missing terminal result, required artifact/oracle/disposition or malformed assessment cannot become PASS.

This closes the semantic routes for prior F3-F6 and F10, including the direct F6 empty-disposition hole.

## B5 — full provenance and profile-scoped PASS

Closed by binding run/evidence reuse to subject/package, fixtures/oracles, execution-profile key, core/harness, normalized-schema version, adapter/normalizer, capability manifest, required-evidence/scoring manifests, replicate and pair order. Assessment reuse additionally binds evaluator realization, wrapper, rubric/key and assessment schema.

Hard and zero-tolerance floors are profile-scoped. Cross-profile analysis may be separately predeclared/reviewed, but cannot rescue an inadmissible profile, average away a hard failure or establish profile equivalence.

## F1-F10 repair routing

| STOP finding | Repaired D3 contract |
| --- | --- |
| F1 wrong/missing immutable subject provenance | exact subject commit + package digest are mandatory run/evidence/cache identity |
| F2 executor/reasoning identity omitted | execution-profile key plus provider-managed-unknown rule and provenance binding |
| F3 incomplete trace admissible | required termination/final-result events plus completeness map and fail-closed state |
| F4 orchestration prints semantic ok for inadmissible | transport status separated from evidence state/outcome |
| F5 missing evaluator evidence silently omitted | required_artifacts manifest |
| F6 missing scoring dispositions accepted | expected_scoring_items manifest with exact one-per-item closure |
| F7 oracle output truncated | required oracle evidence retains complete output or lossless artifact reference |
| F8 regex-only containment | capability manifest + substrate containment/stand-ins; regex explicitly insufficient |
| F9 truncated owner-read summary | owner reads use complete resource_access records; no oracle-relevant truncation |
| F10 oracles optional | required_oracles manifest; omission is non-PASS |

## D4 boundary after this repair

D4 remains unauthorized by this authoring context until a fresh independent Review accepts these exact repaired workplan/contract/amendment bytes.

After that Review PASS, D4 may refactor or replace qualification/ssdp70/eval with the minimum implementation:

1. one portable core implementing the frozen manifests, event schema, state model and scoring;
2. one mostly-declarative execution profile/capability manifest per environment configuration;
3. one thin adapter per materially distinct native runtime/event interface, not per model or protocol arm;
4. environment-native containment/custody controls where available;
5. no adapter-specific scoring forks or parallel authority registry.

The required withheld-instance and actual-adapter known-good/known-broken pre-run qualification remains mandatory after D4 repair. No comparative campaign may start before it passes.

## Review state

This repair was authored in the same trajectory that received the NO-PASS finding and therefore does not independently accept itself. Fresh independent Review is required.
