---
kind: independent-stage-f-portable-execution-architecture-review
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_commit: f4fa583a4b825fda52f4aad3dda7e2afbdfcb301
basis_portability_commit: 62aa1bbaa9d2d1dfef1b48cede6bc1500837658f
basis_no_pass_review: qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-NO-PASS-2026-09-28.md
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
result: PASS
active_serious_challenge: none
d4_tooling_repair_authorized: true
qualification_campaign_authorized: false
pre_run_requalification_required: true
---

# Protocol 7.0 Stage F portable execution architecture — fresh independent Review — PASS

## Disposition

**PASS for the repaired Stage F D3 execution/evidence architecture at exact commit `f4fa583a4b825fda52f4aad3dda7e2afbdfcb301`.**

The five blockers B1-B5 from the independent NO-PASS of `62aa1bbaa9d2d1dfef1b48cede6bc1500837658f` are sufficiently closed. The repaired architecture is precise enough to authorize the bounded D4 refactoring/replacement of `qualification/ssdp70/eval/` into a portable qualification core plus thin runtime adapters.

This PASS authorizes **D4 tooling repair only**. It does **not** authorize the 6.5/6.6/7.0 comparative campaign. The existing Stage F pre-run STOP/BLOCKED state remains in force until the repaired tooling passes the required withheld-instance and actual-adapter known-good/known-broken integrity checks through each admitted execution profile.

No Serious Challenge is active. The architecture is coherent, preserves the frozen qualification semantics, and does not require private model chain-of-thought.

## Authority reconstructed independently

The named branch resolved to exactly `f4fa583a4b825fda52f4aad3dda7e2afbdfcb301` at review time. The governing workplan declares protocol version 6.6.0 and target 7.0.0; Protocol 6.6 remains the accepted-current governing baseline while Protocol 7 is the proposed target.

The immutable Protocol 7 semantic candidate remains:

`db94a2dfb7fef480f37227eab5c45256e89901b8`.

From the first portability amendment `62aa1bb...` to the reviewed commit, the branch advances by three commits:

1. `011b4fe5b6d8b6442040715f160f70276c360d2b` — records the independent portability NO-PASS;
2. `2f2f13fb10aba1eaa0118278adeee418e8f1c526` — repairs the Stage F portable qualification architecture;
3. `f4fa583a4b825fda52f4aad3dda7e2afbdfcb301` — reconciles repair status.

The diff from `62aa1bb...` to the reviewed commit touches only the qualification/workplan/index records expected for this D3 repair: the evaluation contract, portability amendment, prior NO-PASS record, repair record, consolidated Protocol 7 workplan, and workplan authority index. It does not modify the Protocol 7 semantic candidate or `qualification/ssdp70/eval/`.

The relevant current authority/evidence was reconstructed from:

- `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`;
- `qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`;
- `qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-AMENDMENT-2026-09-28.md`;
- `qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-REPAIR-2026-09-28.md`;
- `qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-NO-PASS-2026-09-28.md`;
- `qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md`;
- `workplans/active/SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md`.

## B1-B5 closure

### B1 — execution-profile equivalence: CLOSED AT D3

The repaired contract now gives execution-profile equality a core-owned key rather than a loose label. The key binds the exposed/controllable material conditions that can change trajectory meaning: agent/model, provider/runtime/version where exposed, reasoning configuration, adapter, material environment realization, install mechanism, budgets, capability/containment/network/credential policy, and declared provider-managed unknowns.

Hidden/provider-managed settings are handled without fabricated equality. Unknown values are recorded rather than guessed and are preclassified. A dimension that is materially uncontrolled or not demonstrably arm-neutral makes the pair claim-scoped inadmissible; a known provider/model/runtime migration inside a pair invalidates it. The arm-neutral category is limited to provider-managed variance for which the adapter has no arm-selective control under the same exposed interface/profile. Pair counterbalancing therefore treats such state as uncontrolled within-profile variance rather than as a falsely observed equality.

This is sufficient for portability: a hosted runtime need not reveal every internal backend detail, but hidden state cannot be silently asserted equivalent when it is known or materially suspected to be arm-conditioned.

### B2 — capability, containment and custody: CLOSED AT D3

The portable core now owns a versioned semantic capability manifest with `ALLOW`, `DENY`, and `SANDBOX/MEDIATE` semantics and scope. Its required classes cover catalog/root activation, workspace reads and mutations, command/process execution, delegation, issue/evidence stores, repository/object-store operations, network/remote services, external mutations, and credential/secret/service-account access.

The contract explicitly closes composite escape routes: unrestricted shell or code execution is admissible only when substrate containment still enforces file/network/credential policy, and a denied class may have no unmediated equivalent route. This covers shell/Python, cloud SDKs, repository tools, ambient credentials, mounts/object stores, and similar mechanisms by effective capability rather than tool spelling.

Containment is pre-effect, not forensic-only: prohibited live effects must be blocked before mutation or redirected to qualification-owned isolated state. Regex-only command inspection is insufficient.

Machine-executor custody is also precise: fixture keys/answers must remain outside executor-reachable capability and credential scope until frozen output. Audit supports technical denial but cannot replace it. The frozen stakeholder human-trial behavioral-access exception remains explicitly isolated to that trial.

### B3 — trace portability and completeness: CLOSED AT D3

The core-owned normalized schema is sufficient for the frozen oracle surface without requesting private reasoning. It covers:

- catalog snapshot and root selection;
- exact resource access;
- tool actions;
- delegation call/return and lineage;
- issue/evidence-store access;
- workspace/external mutations;
- network/external actions;
- termination;
- final result;
- usage/timing.

Common identity, actor, sequence, native-source, status, and exposed timing fields support ordering and provenance. Oracle-relevant identities and inputs must be complete or losslessly artifact-referenced; they may not be truncated. Owner-read scoring therefore has a canonical full-resource evidence path rather than the old reduced summary.

Each adapter must also provide a raw-to-normalized completeness map. Oracle-relevant native observations cannot be silently dropped, reordered, truncated, or left unclassified. If a required observable cannot be exposed, the affected claim is inadmissible rather than inferred from a weaker proxy.

### B4 — fail-closed evidence and scoring: CLOSED AT D3

The repaired core owns immutable run-bound manifests for:

- `required_artifacts`;
- `required_oracles`;
- `expected_scoring_items`.

The scoring manifest binds item id, measure, criticality, applicable case/branch, and allowed dispositions. A valid assessment requires exactly one disposition for every expected applicable item, with no duplicate or unknown ids; unresolved applicability is explicit `UNRESOLVED`, never omission.

The state model separates transport/process success, evidence admissibility, and qualification outcome. Only `COMPLETE_ADMISSIBLE` evidence may enter PASS/FAIL scoring. Missing terminal state/result, required artifact, oracle, scoring disposition, or malformed assessment is non-PASS by construction.

This closes the prior F6 empty-disposition defect and gives F3-F6/F10 one common fail-closed semantic owner.

### B5 — provenance, caches and profile-scoped PASS: CLOSED AT D3

Run/evidence reuse now binds every material dependency identified by the prior review: immutable subject commit/package digest; fixture/stub/oracle identities; execution-profile key; core/harness digest; normalized schema; adapter/normalizer; capability manifest; required artifact/oracle/scoring manifests; replicate; and pair order.

Assessment reuse additionally binds the evaluator realization where applicable, evaluator wrapper, rubric/key digest, and assessment schema. Separate executor and assessment caches are allowed only if each cache binds every dependency material to the artifact it reuses. A material change therefore cannot legitimately survive under the same cache identity.

PASS is profile-scoped. Hard and zero-tolerance floors and matched comparisons are evaluated within one execution-profile key. Cross-profile summaries may be separately predeclared/reviewed, but cannot rescue an inadmissible profile, average away a hard failure, or establish equivalence of materially different profiles.

## F1-F10 reassessment

These dispositions are architectural: they mean D3 now specifies the required repair unambiguously. They do not claim that the old D4 scripts already satisfy it.

| Prior Stage F tooling defect | D3 disposition | Reason |
| --- | --- | --- |
| F1 immutable subject absent from run identity | **CLOSED AT D3** | Exact subject commit + package digest are mandatory run/evidence/cache identity. |
| F2 executor/reasoning omitted from cache identity | **CLOSED AT D3** | Execution-profile key plus full run/assessment provenance binds exposed runtime/reasoning and provider-managed-unknown treatment. |
| F3 incomplete trace can be admissible | **CLOSED AT D3** | Required termination/final-result evidence, completeness mapping, and fail-closed evidence state forbid it. |
| F4 matrix can print semantic `ok` for inadmissible evidence | **CLOSED AT D3** | Transport/process status is distinct from evidence state and qualification outcome. |
| F5 missing evaluator evidence can disappear | **CLOSED AT D3** | `required_artifacts` gives exact presence/validation closure. |
| F6 missing scoring dispositions accepted | **CLOSED AT D3** | `expected_scoring_items` requires exact one-disposition-per-applicable-item closure. |
| F7 deterministic-oracle evidence truncated | **CLOSED AT D3** | Required oracle output is complete or losslessly artifact-referenced; oracle-relevant fields cannot be truncated. |
| F8 regex-only side-effect containment | **CLOSED AT D3** | Semantic capability manifest plus substrate containment/stand-ins owns effective enforcement; regex alone is prohibited. |
| F9 reduced owner-read trace misses real access | **CLOSED AT D3** | Owner reads use complete `resource_access` records and raw-normalized completeness, not reduced summaries. |
| F10 deterministic oracles optional | **CLOSED AT D3** | `required_oracles` makes omission an explicit non-PASS evidence defect. |

No F1-F10 repair is over-specified at D3. The names and minimum fields of the normalized evidence interface, admissibility states, and manifest closure are architecture-level interoperability and integrity contracts because adapters and scorers must agree on them. Concrete serialization, helper APIs, process topology, sandbox technology, retry logic, and adapter implementation remain D4.

## 6.6 preservation

The repaired logical 6.6 execution profile is faithful to the historical capability rather than to Claude syntax.

For T1/T7/T8 it preserves:

- explicit D4 root activation before task work;
- equivalent 6.6 allow/deny capability meaning;
- delegated-agent capability unavailable on that panel;
- exact SSDP resource consumption and whole-active-material byte accounting;
- same-profile matched arms;
- fresh environment-local accepted-6.5/6.6 baselines;
- the existing route correctness and burden floors.

The historical prompt prefix and Claude flags remain reference realizations only.

An environment that cannot expose selected root, exact SSDP resources, or the material required by the frozen byte metric is claim-scoped inadmissible. Token/context estimates or other weaker proxies are expressly disallowed. This preserves the 6.6 measurement rather than weakening it for portability.

## Adversarial equivalence attempts

The repaired architecture was challenged against the requested false-green routes.

- **Hidden injected/provider context:** exposed material context/configuration belongs in the profile key; genuinely hidden provider-managed dimensions are declared rather than guessed. A materially uncontrolled/not demonstrably arm-neutral dimension blocks the sensitive claim, and known migration invalidates the pair.
- **Ambient credentials, shell/Python, SDKs, repository tools, mounts:** effective capabilities must map through the versioned manifest, and denied classes may have no unmediated equivalent route. Substrate containment remains mandatory even when arbitrary code/process execution is allowed.
- **Omitted or truncated owner/resource reads:** full `resource_access` evidence plus raw-to-normalized completeness is the scoring source; reduced summaries cannot satisfy zero-tolerance oracles.
- **Provider/runtime drift:** known migration invalidates the pair; unknown provider dimensions are handled by the profile rule rather than silently collapsed.
- **Missing evaluator/scoring items:** the expected-item manifest and exact disposition closure make omission malformed/non-PASS.
- **Missing terminal state/oracle/artifact:** required manifests and the evidence-state machine prevent PASS/FAIL scoring.
- **Stale core, normalizer, capability, rubric, evaluator or assessment cache:** those identities/digests are bound at the appropriate cache layer, and the pre-run checker must perturb them.
- **Cross-profile averaging:** the primary result is profile-scoped; a hard failure or inadmissible included profile cannot be averaged away.
- **Post-hoc containment:** logging a real prohibited mutation after it happens is explicitly not containment.

No requested false-green route remains valid under the D3 contract. Actual adapter enforcement remains a required D4/pre-run evidence question.

## D3/D4 boundary and complexity

The repaired architecture is implementable without new qualification-policy invention:

1. one portable core owns frozen identities/manifests, normalized event semantics, admissibility state, pair semantics, evidence validation and scoring;
2. execution profiles/capability manifests are mostly declarative environment configuration;
3. adapters translate/enforce one materially distinct native runtime/event interface rather than proliferating by model or protocol arm;
4. native sandbox/proxy/workspace controls may realize containment/custody;
5. adapter-specific scoring forks and parallel authority registries are forbidden.

This is proportionate to the portability requirement and to the concrete F1-F10 failures already observed. It is not a general agent framework: it is a qualification boundary with a finite event/evidence interface. D4 remains free to choose implementation language, serialization, helper structure, sandbox technology, APIs, cache layout, and adapter-internal algorithms so long as the D3 contracts hold.

## Non-change verification

The repair from `62aa1bb...` to `f4fa583...` changes execution/evidence architecture and its lifecycle records only.

Patch inspection found no change to:

- Protocol 7 semantic candidate bytes;
- scientific/epistemic doctrine;
- fixture content or planted keys;
- numerical adequacy floors or comparative targets;
- human-trial participant/rules/floors;
- Stage G/H semantics.

The T1/T7/T8 contract edit adds the required observability/inadmissibility rule and changes “same execution profile” to “same execution-profile key”; it retains the existing run counts, 2.0x fresh paired accepted-6.5 median bound, 512 B static margin, and other preservation rules.

No D4 tooling file was changed by this repair.

## Evidence limits and next gate

This Review is a D3 architecture Review. It did not execute the repaired qualification core because D4 has not yet implemented it, and it did not consume withheld fixture/key material. Those are not substitutes for this Review and remain mandatory at the next gate.

After this PASS:

1. D4 may repair/refactor `qualification/ssdp70/eval/` against the accepted portable-core + adapter contract;
2. focused core/adapter regression must exercise F1-F10 and the provenance/state-machine boundaries;
3. the independent pre-run checker must run the required withheld-instance and actual-adapter known-good/known-broken suite through every admitted profile;
4. only after that pre-run gate passes may the comparative 6.5/6.6/7.0 campaign begin.

## Final decision

```text
SERIOUS CHALLENGE: NONE
RESULT: PASS
REVIEWED COMMIT: f4fa583a4b825fda52f4aad3dda7e2afbdfcb301
SEMANTIC CANDIDATE: db94a2dfb7fef480f37227eab5c45256e89901b8 — UNCHANGED
B1-B5: CLOSED AT D3
F1-F10: CLOSED AT D3 AS IMPLEMENTATION CONTRACTS; D4 REPAIR STILL REQUIRED
D4 PORTABLE-TOOLING REPAIR: AUTHORIZED
WITHHELD/ACTUAL-ADAPTER PRE-RUN REQUALIFICATION: STILL REQUIRED
6.5/6.6/7.0 COMPARATIVE CAMPAIGN: NOT AUTHORIZED YET
STAGE G/H: UNCHANGED
```
