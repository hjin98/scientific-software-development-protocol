---
kind: stage-f-pre-run-integrity-d4-repair
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date: 2026-09-28
input_review: qualification/ssdp70/STAGE-F-PRE-RUN-QUALIFICATION-INTEGRITY-RECHECK-STOP-BLOCKED-2026-09-28.md
implementation_commit: 0be3f979e66d1ea3a51c554bdd70c541e3d22d8a
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
status: implemented-pending-actual-profile-withheld-recheck
qualification_campaign_authorized: false
active_serious_challenge: none
---

# Protocol 7.0 Stage F pre-run integrity D4 repair

## Disposition

The D4 executable-integrity blockers B2-B7 identified by the fresh independent Stage F recheck have
been repaired at exact implementation commit
`0be3f979e66d1ea3a51c554bdd70c541e3d22d8a`.

This is **not** a Stage F pre-run PASS. The actual environment-local executor/evaluator profiles,
pre-effect containment/custody evidence, and withheld custodian material remain required before the
comparative 6.5/6.6/7.0 campaign can start. Synthetic probes verify mechanics only.

The immutable Protocol 7 semantic candidate remains
`db94a2dfb7fef480f37227eab5c45256e89901b8`.

## Repair closure

### B2 — admission fail-open

The portable core now owns exact role-specific executor and evaluator admission-check sets.
Qualification admission rejects missing or unknown checks. Each check must be `PASS` and bind to a
present SHA-256-verified proof artifact.

The full admission record plus all proof artifacts are copied into run-owned evidence and validated
against the admission-bundle identity. Executor and evaluator paths also detect admission-bundle
changes between identity/validation and launch.

### B3/B4 — normalized trajectory, owner reads, ordinary entry and T1/T7/T8 observability

The core now validates per-event-kind payload contracts rather than common fields alone. The Claude
adapter records stable tool-use identity, action requests and exposed results/errors, including
lossless result content/reference/hash.

Catalog/root events bind the verified installed arm/package identity. Successful SSDP resource
access records exact resource path, whole-file byte count and SHA-256 where locally resolvable.
Reads of an installed skill's `SKILL.md` expose ordinary root selection; explicit `Skill` calls
remain explicit root-selection events. Owner-read claims require a successful result event for the
canonical owner resource.

Unknown native tool/event classes fail closed unless explicitly classified by the adapter. A pending
tool use with no exposed result is malformed evidence. Claims requiring T1/T7/T8 burden observables
become inadmissible when exact root/resource byte/hash evidence is absent; no token/context proxy is
introduced.

### B5/B7 — runtime, cache and evidence integrity

The declared profile remains in run identity, and the adapter now exposes runtime-observed model and
runtime build. Qualification rejects unfrozen profile markers and observed model/runtime mismatch.

Material generated run evidence is content-bound by an integrity manifest. Required oracle
stdout/stderr hashes are verified. Requirements snapshots carry independently recomputed content
digests and must reconcile to the run-bound frozen manifest digests.

Cache reuse calls full run revalidation, and qualification-mode executor runs do not reuse cache.
Deleting or modifying retained evidence invalidates reuse.

### B6 — evaluator admission

Assessment requires a frozen evaluator profile and a separately admitted evaluator realization.
Uncontrolled material evaluator dimensions are rejected. The evaluator adapter/core/capabilities,
admission bundle, wrapper, runtime observation, model/reasoning realization, rubric/key material and
scoring manifest are bound into assessment identity.

A runtime mismatch produces `INADMISSIBLE / NOT_EVALUATED`; it cannot enter PASS/FAIL scoring.

## Verification executed

The exact staged Git bytes were materialized and verified by Git blob identity:

- `core70.py`: `cef064eab0d79461683710c01defd6bbde1bbf1a`
- `harness70.py`: `e81af6929edb205412cfbd6da7df1bb93960f14b`
- `assess70.py`: `42378844cbc9f91fdb7dbb2f7471df6215da5ed5`
- `adapters/claude.py`: `71ede0d9c972a76220fae1861e70da87cae078a6`
- `test_portable70.py`: `3285f5ad5260a87047de7bc0937168a9cb26d467`
- `test_harness_integration.py`: `e95d9389b813dd1165878bb6f5a758ee323ceb57`

Executed:

```text
python -m py_compile core70.py harness70.py assess70.py adapters/claude.py test_portable70.py test_harness_integration.py
PASS

python -m unittest -v test_portable70.py test_harness_integration.py
Ran 23 tests
OK
```

The focused suite covers exact admission closure and proof tampering, runtime mismatch/unfrozen
profiles, per-kind evidence schema, complete owner-read result capture, ordinary root activation,
unknown/missing native result failure, requirements-snapshot tampering, full synthetic harness
evidence closure, post-run cache tampering, missing oracle rejection, admitted evaluator PASS and
evaluator runtime mismatch inadmissibility.

A separate hostile mechanics probe also passed 18/18 cases, including cache/evidence tampering and
complete-run revalidation. These synthetic checks do not substitute for the required actual-profile
and withheld qualification evidence.

## Scope and upstream impact

The diff from the STOP/BLOCKED recheck record at
`e66ac371486754855516b7f9c463ba0e8df634c9` to the implementation touches only:

- `qualification/ssdp70/eval/core70.py`
- `qualification/ssdp70/eval/harness70.py`
- `qualification/ssdp70/eval/adapters/claude.py`
- `qualification/ssdp70/eval/assess70.py`
- `qualification/ssdp70/eval/test_portable70.py`
- `qualification/ssdp70/eval/test_harness_integration.py`

No Protocol 7 candidate bytes, D3/evaluation-contract semantics, scoring thresholds, fixtures,
human-trial rules or Stage G/H semantics changed. No adapter-specific scoring fork or parallel
authority registry was introduced.

## Remaining gate

B1 remains open by design: a fresh independent checker must freeze the real environment-local
executor and evaluator profiles and run the complete known-good/known-broken admission suite through
that exact realization with the withheld custodian material.

That check must include actual pre-effect containment and custody denial against shell/Python, SDK,
credential, mount, repository/object-store and network escape routes; actual catalog/root/resource
capture; cache/profile/core/evaluator perturbations; incomplete evidence; ordinary-entry/owner-read;
and withheld oracle branches.

Only a fresh independent Stage F pre-run **PASS** on that exact admitted realization may authorize
the comparative campaign.
