---
kind: independent-stage-f-pre-run-qualification-integrity-recheck
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
stage: F-pre-run
result: STOP/BLOCKED
review_date: 2026-09-28
reviewed_branch: ssdp-7.0-scientific-epistemic-closure
reviewed_head: 5104e79816f0cd8270f800aee98ff9bf623a77be
tooling_implementation: 9d73c20d98d33b48ab6403dd359c1c86f2d056f9
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
qualification_campaign_authorized: false
active_serious_challenge: none
---

# Protocol 7.0 Stage F pre-run qualification-integrity recheck — STOP/BLOCKED

## Disposition

**STOP/BLOCKED. Do not begin the fresh 6.5/6.6/7.0 comparative qualification campaign.**

This is a fresh independent recheck of exact branch head
`5104e79816f0cd8270f800aee98ff9bf623a77be`. The reviewed executable tooling is the
D4 implementation at its parent `9d73c20d98d33b48ab6403dd359c1c86f2d056f9`; the head adds only the
tooling-repair record. The immutable Protocol 7 semantic candidate remains
`db94a2dfb7fef480f37227eab5c45256e89901b8`.

The repaired D3 portable-execution architecture is coherent and realizable. No Serious Challenge is
raised. The blockers are D4 executable-integrity defects plus unavailable mandatory real-profile and
withheld evidence.

No Protocol 7 candidate run, paired 6.5/6.6 baseline run, comparative scoring run, or human trial was
started.

## Authority reconstructed independently

The governing cycle remains bound to Protocol 6.6.0 with target Protocol 7.0.0 by
`workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`.

The controlling Stage F evidence contract is
`qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md`, including its
portable runner-admission contract. The repaired D3 architecture was independently accepted in
`qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-PASS-2026-09-28.md`.
That PASS authorizes D4 repair only and explicitly leaves Stage F pre-run STOP/BLOCKED until the
withheld-instance and actual-adapter/profile integrity suite passes.

The prior
`qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-REVIEW-STOP-BLOCKED-2026-09-28.md`
was treated as historical evidence and defect input, not as an inherited conclusion. The present
decision was re-derived from the frozen contract and the executable tooling at the exact reviewed
head.

The immutable subjects remain:

- Protocol 6.5: `7f7b5e24858e813e45ace867a7f8ea5180f43bf0`
- Protocol 6.6: `22f4bdba53795da3a6f13f162529f3a843fc37ae`
- Protocol 7.0: `db94a2dfb7fef480f37227eab5c45256e89901b8`

## Checks actually available in this review

Repository authority, exact branch/head lineage, the D4 diff, the current portable core, harness,
Claude adapter, profiles, capability manifests, assessor, preparation path, and focused tests were
reconstructed from the exact GitHub objects.

The mandatory actual-profile probes could not execute in this review environment:

- no `claude` executable is available;
- no frozen environment-local executor or evaluator profile/admission record is present;
- the checked-in profiles are explicitly templates with runtime build/reasoning still unfrozen;
- the designated out-of-repository withheld custody material is not available in the execution
  environment;
- direct GitHub network access from the execution container is unavailable, so the exact repository
  cannot be cloned there for an independent local full-suite run.

These are blocking unavailable checks, not passes. Synthetic/fake-adapter tests were inspected only
as mechanics evidence and were not substituted for the required actual-adapter/profile or withheld
evidence.

## Blocking findings

### B1 — required actual-profile and withheld pre-run evidence is unavailable

The frozen contract requires the known-good/known-broken suite through the exact admitted
adapter/profile, including containment escapes, custody denial, cache/profile/core/evaluator
perturbations, catalog contamination, incomplete evidence, ordinary-entry/owner-read capture and
withheld oracle branches.

No admitted real execution profile or corresponding containment/custody evidence is available here,
and the withheld custodian corpus/keys/oracle branches are not mounted. Therefore the mandatory
profile-scoped pre-run gate cannot pass even if the implementation were otherwise correct.

**Minimal repair/evidence:** freeze the real executor and evaluator profiles in the environment that
will run qualification; bind exposed runtime/model/reasoning/build and material environment
realization; independently demonstrate containment/custody; make the withheld material available
only to the checker/evaluator under the frozen role/time boundary; then run the complete required
probe matrix through that exact realization.

### B2 — profile admission is executable fail-open

`core70.validate_profile_admission()` binds the admission record to profile, adapter, core and
capability-manifest hashes, but its semantic suite closure is only:

- `checks` is a non-empty object; and
- every supplied value is `true`.

It does not require an exact core-owned set of admission checks, evidence identities or proof
artifacts. An admission record such as an arbitrary single all-true check can satisfy the executable
gate while omitting containment, normalization, scoring, custody, cache perturbation, ordinary-entry
or other mandatory pre-run checks.

**Minimal repair:** define the exact admission-check schema/manifest in the portable core; require
the complete expected check set with no omissions/unknown substitutions; bind each material check
to its evidence artifact/hash and actual profile realization; reject incomplete, stale or malformed
admission evidence.

### B3 — normalized trajectory validation does not enforce the frozen per-kind evidence contract

`core70.validate_normalized_events()` validates only common event fields, event kind, ordering,
native-source shape and that `payload` is an object. It does not validate the required payload
schema for each normalized event kind.

The current Claude adapter consequently emits evidence that can satisfy the generic validator while
missing frozen fields:

- `catalog_snapshot` records logical names/model/runtime version but not exact resolved
  arm/package identity;
- `root_selection` does not record resolved package identity;
- `resource_access` records the request/path but uses `result_reference: null`, with no read
  result status or result/artifact reference;
- `tool_action` similarly records request input without start/result/error lifecycle or output
  reference;
- unrecognized valid native event types default to generic `metadata` with
  `oracle_relevant: false` rather than failing closed or passing through an explicit reviewed
  non-oracle classification.

Thus the raw-to-normalized completeness map can be structurally complete while semantically dropping
oracle-relevant result information.

**Minimal repair:** make per-kind payload schemas executable in the core; normalize both action
requests and exposed results; require exact root/package/resource identity, result status and
lossless output/artifact references where the contract requires them; make unknown native event
types fail closed unless explicitly classified by a reviewed non-oracle rule.

### B4 — ordinary-entry, owner-read and T1/T7/T8 observability are not genuinely closed

`adapters/claude.owner_reads()` recognizes an owner read from the normalized request payload. It
does not prove that the resource access succeeded or what bytes/result were returned. The adapter
also emits `root_selection` only for an explicit native `Skill` tool use; an ordinary-entry
selection without that event is not represented. Catalog isolation checks expected skill names and
multiplicity but not the resolved arm/package identity.

The frozen T1/T7/T8 burden claims require logical root activation, equivalent capability
restrictions, exact SSDP-resource observability and exact active-byte accounting. A runtime that
cannot expose these observables must become claim-scoped inadmissible; it may not be scored from a
weaker request/path or token/context proxy. The present executable state does not enforce that rule.

**Minimal repair:** expose and validate successful resource-result evidence, exact resolved package
and resource identity, ordinary/root selection mechanism and the byte-accounting inputs required by
T1/T7/T8. If an execution runtime cannot expose them, the core must mark the affected claims
inadmissible. Fresh accepted-6.5 baselines must then be measured in the same admitted profile.

### B5 — runtime realization and cache reuse are not sufficiently self-invalidating

The execution-profile key binds the declared provider/runtime/version and reasoning configuration,
and the run identity binds that key. However the actual runtime-visible model/build reported by the
native stream is not checked against the frozen profile before evidence becomes admissible. A later
runtime/build migration can therefore leave the declared profile/admission/cache identity unchanged.

Separately, `core70.cache_valid()` reuses a cached run when the stored run identity equals the
current identity and the stored summary says `COMPLETE_ADMISSIBLE` with `execution_ok: true`.
It does not revalidate the required artifacts, oracle outputs, normalized trace/completeness map or
their integrity. Deleting or corrupting required evidence after a valid run can therefore leave the
cache reusable.

**Minimal repair:** verify the observable runtime/model/build/reasoning realization against the
frozen profile and bind that observed realization to admission/run identity. Revalidation of a
cached run must re-check the complete required-evidence closure and integrity, not trust the old
summary alone.

### B6 — evaluator execution has no equivalent admission/fail-closed profile gate

`assess70.py` binds declared evaluator profile/capability/adapter/wrapper/key/rubric identities in
its assessment identity, but it does not run `validate_profile_admission()` for the evaluator and
does not reject evaluator profiles with uncontrolled provider-managed dimensions through
`profile_claim_errors()`.

Therefore the checked-in evaluator template, whose runtime build and reasoning are explicitly
unfrozen, is not executablely prevented from entering assessment merely because it is a template.
The actual evaluator runtime realization is not independently admitted before it can emit a
PASS/FAIL assessment.

**Minimal repair:** require a frozen, independently admitted evaluator profile (or an equivalent
core-owned evaluator-admission contract), reject uncontrolled material evaluator dimensions, and
bind/verify the observed evaluator runtime/model/reasoning realization before accepting an
assessment.

### B7 — post-run evidence and requirements snapshots are trusted too strongly

Fresh run construction checks required artifact/oracle presence, but subsequent reuse/assessment
trusts stored state:

- `cache_valid()` does not revalidate the evidence tree;
- `assess70.py` trusts a run summary already saying `COMPLETE_ADMISSIBLE`;
- `requirements_from_snapshot()` validates snapshot shape but trusts the embedded manifest digest
  strings rather than recomputing them from the snapshot content and reconciling them to the bound
  run requirements.

A modified scoring snapshot can therefore be interpreted under a stale claimed digest, and missing
or changed run evidence can survive through a stale complete summary.

**Minimal repair:** content-bind requirements snapshots by recomputing their digests, reconcile them
to the run identity/original frozen manifests, and revalidate required artifacts/oracles/trace
integrity before cache reuse and assessment. Use hashes/manifests for material generated evidence
where existence alone is insufficient.

## F1–F10 executable reassessment

| Prior defect | Recheck | Reason |
| --- | --- | --- |
| F1 immutable subject absent from run identity | **CLOSED for prepared-run identity, but broader catalog identity remains blocked by B3/B4** | `run_identity` now binds requested ref, resolved commit, version, package digest and prepared-arms manifest; `resolve_arm_dist` verifies the package tree. |
| F2 executor/reasoning absent from cache identity | **NOT CLOSED** | Declared profile identity is bound, but observed runtime/build is not verified against it; evaluator admission is also absent. |
| F3 incomplete trace can be admissible | **CLOSED for missing terminal/final result** | Execution requires terminal success; evidence state requires terminal and final-result events. Semantic trace completeness remains blocked by B3. |
| F4 matrix reports semantic `ok` for inadmissible run | **CLOSED** | Matrix/run reporting uses the core evidence state rather than transport success as semantic result. |
| F5 missing evaluator evidence silently disappears | **NOT FULLY CLOSED** | Fresh-run required-artifact presence is checked, but cache/assessment reuse can trust stale or modified evidence. |
| F6 omitted scoring dispositions accepted | **CLOSED for fresh validated assessment** | Exact expected-item closure rejects missing, duplicate and unknown dispositions. |
| F7 deterministic-oracle output truncated | **CLOSED in the fresh oracle writer** | Full stdout/stderr are stored as separate artifacts with hashes. |
| F8 regex-only containment | **NOT CLOSED AT PRE-RUN** | Regex containment is no longer claimed, but no actual admitted substrate containment has been demonstrated through the real profile. |
| F9 owner-read evidence uses truncated reducer | **NOT CLOSED semantically** | Text truncation is gone, but current evidence records the read request without result status/content reference, so successful consumption and exact bytes are not established. |
| F10 deterministic oracles optional | **NOT FULLY CLOSED** | Fresh runs treat missing required oracles as non-PASS, but stale cache/assessment state is not independently revalidated. |

F1/F3/F4/F6/F7 show real D4 improvement. They do not compensate for the remaining fail-open paths or
the unavailable required actual-profile evidence.

## Containment and custody

The portable architecture correctly places containment outside command-text heuristics, but the
reference adapter itself does not establish containment. Its environment construction largely
inherits the host environment, while the capability manifest declares credential/network denial to
be established by independent admission. That is acceptable only after real substrate evidence
shows that shell/Python, SDKs, Git/repository/object-store operations, mounts, credentials and
network routes cannot cross the qualification boundary before mutation.

No such real-profile containment/custody proof was available here, so prohibited-effect and withheld
key denial remain unqualified rather than inferred from declarations.

## Architecture/authority drift check

No adapter-specific scoring branch was found: scoring remains in the portable core/assessor rather
than the Claude adapter. The repaired structure remains bounded to one portable core plus thin
runtime adapter/profile/capability realizations; no unnecessary parallel authority registry was
introduced.

The reviewed D4 changes are confined to Stage F qualification/evidence tooling and records. No
change to the immutable Protocol 7 semantic candidate, frozen scoring thresholds, fixture semantics,
human-trial rules or Stage G/H semantics was found. The accepted D3 architecture is therefore not
contradicted; the correct disposition is D4 STOP/BLOCKED, not Serious Challenge.

## Required repair and rerun sequence

1. Close B2–B7 in the portable core/adapter/assessor without changing the frozen D3/evaluation
   contract.
2. Add focused hostile regression for omitted admission checks, malformed/missing per-kind payload,
   unknown native event classes, failed/read-result absence, ordinary entry, runtime-version
   mismatch, cache evidence deletion/tampering, requirements-snapshot tampering and evaluator
   admission.
3. Freeze the actual environment-local executor and evaluator profiles and create admission evidence
   only after the exact known-good/known-broken suite passes through those profiles.
4. Demonstrate pre-effect containment and key custody against shell/Python, native SDKs,
   credentials, mounts, repository/object-store and network escape routes.
5. With the withheld custodian material, run the required oracle branches and classification/exposure
   checks through the actual adapter/profile.
6. Re-run this independent Stage F pre-run gate. Only a fresh PASS of that exact realization may
   authorize the comparative 6.5/6.6/7.0 campaign.

## Final outcome

**STOP/BLOCKED.** Stage F pre-run integrity is not yet genuinely satisfied. The comparative campaign
remains unauthorized, and the immutable Protocol 7 candidate must remain unchanged.
