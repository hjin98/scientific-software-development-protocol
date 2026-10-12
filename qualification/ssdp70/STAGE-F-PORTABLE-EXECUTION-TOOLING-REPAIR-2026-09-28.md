---
kind: protocol-stage-f-portable-execution-tooling-repair
governing_protocol_version: 6.6.0
target_protocol_version: 7.0.0
date: 2026-09-28
architecture_review: qualification/ssdp70/STAGE-F-PORTABLE-EXECUTION-ARCHITECTURE-INDEPENDENT-REVIEW-PASS-2026-09-28.md
architecture_review_commit: 8c8ef114ba0c77a31fc19e67772b722a8acf4d19
implementation_commit: 9d73c20d98d33b48ab6403dd359c1c86f2d056f9
semantic_candidate: db94a2dfb7fef480f37227eab5c45256e89901b8
status: implemented-pending-independent-pre-run-requalification
active_serious_challenge: none
qualification_campaign_authorized: false
---

# Protocol 7.0 Stage F portable execution tooling repair

## Disposition

The bounded D4 tooling repair authorized by the fresh Stage F portable-execution architecture Review has been implemented at exact commit:

`9d73c20d98d33b48ab6403dd359c1c86f2d056f9`.

This implementation does **not** authorize the 6.5/6.6/7.0 comparative qualification campaign. The Stage F pre-run gate remains STOP/BLOCKED until a fresh independent checker, with the real withheld material and an actual frozen execution profile/adapter, performs the required known-good/known-broken, containment, custody, capture, scoring-closure and ordinary-entry checks.

The immutable Protocol 7 semantic candidate remains `db94a2dfb7fef480f37227eab5c45256e89901b8`.

## Implemented D4 structure

The repair replaces the prior Claude-bound semantic coupling with the minimum accepted portable structure under `qualification/ssdp70/eval/`:

- `core70.py` — portable semantic owner for profile/capability validation, normalized-event validation, raw-to-normalized completeness, run-bound required-artifact/oracle/scoring manifests, fail-closed evidence states, exact disposition closure, cache identity and profile-admission binding;
- `adapters/claude.py` — thin Claude stream-json launch/install/normalization realization; it does not own qualification scoring or claim regex/text inspection is containment;
- `harness70.py` — profile/adapter-driven runner using exact prepared-arm identities and core-owned evidence states;
- `assess70.py` — fail-closed assessment wrapper that accepts only `COMPLETE_ADMISSIBLE` evidence and enforces exact expected-item closure;
- `profiles/*.template.json` — non-authoritative environment templates that must be frozen into an actual execution profile before qualification;
- `capabilities/*.json` — semantic capability realization declarations for the reference Claude executor and read-only evaluator;
- focused portable-core and integration tests.

`prepare_arms70.py` remains the exact-subject preparation owner and was not changed.

## F1-F10 implementation closure

| Prior defect | D4 repair |
| --- | --- |
| F1 immutable subject absent from run identity | Run identity now consumes the prepared `arms.json` arm record and binds requested ref, resolved commit, version, package digest and prepared-manifest digest. |
| F2 executor/reasoning absent from cache identity | Run identity binds the full execution-profile key, profile document, adapter/normalizer, core/harness, capability manifest and material profile fields including reasoning/runtime configuration. |
| F3 incomplete trace could be admissible | A successful transport is insufficient; normalized termination and final-result events are required before evidence can be `COMPLETE_ADMISSIBLE`. |
| F4 matrix reported semantic `ok` for inadmissible runs | Matrix output reports the core-owned `evidence_state`; process transport status is not a semantic result. |
| F5 missing evaluator evidence silently disappeared | Run-bound `required_artifacts` are validated before assessment; incomplete evidence is rejected. |
| F6 omitted dispositions were accepted | `expected_scoring_items` requires exactly one disposition per expected item, rejecting empty, missing, duplicate and unknown items. |
| F7 deterministic-oracle output was truncated | Complete stdout/stderr are retained as separate hashed artifacts and referenced by `oracle.json`. |
| F8 regex-only containment | Regex containment is removed as an admissibility mechanism. Qualification mode requires an independently generated profile-admission record bound to the current core, adapter, profile and capability manifest; containment must be proven pre-effect by the actual environment. |
| F9 owner-read evidence used a truncated reducer | Owner-read scoring consumes complete normalized `resource_access` payloads; no oracle-relevant field is truncated. |
| F10 deterministic oracles were optional | The run-bound `required_oracles` manifest owns the exact oracle set; missing/unexecuted required oracles produce non-PASS evidence. |

## Trace/completeness integrity

The adapter records a normalized event stream plus a raw-to-normalized completeness map. Native events are indexed and SHA-256-bound. The portable core checks:

- normalized schema/run/event identity;
- strictly increasing normalized sequence;
- native source identity and hashes;
- preserved native event order;
- complete native-event accounting;
- no unmapped oracle-relevant native event;
- no unknown normalized event kind.

Convenience summaries remain derived evidence and are not the zero-tolerance scoring source.

## Qualification versus probe mode

The runner has two explicit modes:

- `probe` — permits synthetic/pre-run discrimination work but cannot by itself establish qualification admission;
- `qualification` — refuses to launch without a profile-admission record whose profile/core/adapter/capability identities match the current realization and whose required admission checks are all true.

The checked-in Claude profiles are intentionally **templates**, not admitted profiles. Their provider runtime build is marked as needing environment-local freezing; the executor template also marks that material dimension uncontrolled until frozen. This prevents the reference template from silently becoming qualification evidence.

## Evidence executed in the implementation context

The final implementation bytes were tested locally with Python after the last executable change.

Executed:

```text
python -m py_compile core70.py harness70.py assess70.py adapters/claude.py test_portable70.py test_harness_integration.py
PASS

JSON parse of profiles/*.json and capabilities/*.json
PASS

python -m unittest -v
15 tests / 15 PASS
```

The focused tests include:

- material profile/capability changes invalidate profile identity;
- uncontrolled provider-managed state blocks a sensitive claim;
- empty/duplicate/missing scoring dispositions fail closed;
- missing required artifacts/oracles fail closed;
- dropped native events fail completeness;
- normalized native-event reordering is rejected;
- stale admission after core/profile change is rejected;
- full owner-read input is retained beyond the old truncation boundary;
- missing terminal evidence is observable/non-admissible;
- unknown native tools fail normalization;
- process success cannot override profile inadmissibility;
- a synthetic complete fake-runtime episode reaches `COMPLETE_ADMISSIBLE`;
- the same episode with a required oracle omitted becomes `MISSING_REQUIRED_EVIDENCE`;
- assessment rejects a missing expected scoring item.

Remote post-commit verification confirmed the exact Git blob identities for all eleven changed files and that the implementation commit is a one-commit fast-forward descendant of the architecture-PASS commit.

The repository's standard `protocol-check.yml` runs only on pull requests and pushes to `main`; this branch push therefore produced no CI status. The change does not modify protocol source, generated packages or Orchestrator Core.

## Evidence not executed / still blocking

The following required Stage F pre-run evidence was intentionally **not** manufactured in this implementation context:

- real withheld classification/key/rubric/human-trial material;
- actual frozen execution-profile admission;
- actual runtime containment/custody proof;
- actual-adapter known-good/known-broken branch discrimination;
- real external-write/network escape probes against the admitted substrate;
- full ordinary-entry and chained-delegate withheld probes;
- comparative 6.5/6.6/7.0 runs;
- human legibility trial.

Those checks require the independent custody/pre-run environment. Synthetic fixtures and the fake runtime used for D4 regression are not substitutes.

## Next gate

A fresh independent Stage F pre-run qualification-integrity review should now:

1. freeze the actual environment-local execution profile(s), including exposed runtime/build/reasoning settings and honest provider-managed unknowns;
2. verify the semantic capability manifest against effective substrate capabilities, ambient credentials, mounts, SDK/repository/object-store routes and network/external-write enforcement;
3. run the withheld known-good/known-broken suite through the actual adapter/profile;
4. verify raw-to-normalized completeness, artifact/oracle/scoring closure and cache-identity perturbations;
5. issue a profile-admission record only if every required check passes;
6. return PASS before any comparative qualification subject is run.

## Gate state

```text
SERIOUS CHALLENGE: NONE
D3 PORTABLE ARCHITECTURE: PASS
D4 PORTABLE TOOLING REPAIR: IMPLEMENTED
IMPLEMENTATION COMMIT: 9d73c20d98d33b48ab6403dd359c1c86f2d056f9
FOCUSED D4 REGRESSION: 15/15 PASS
IMMUTABLE PROTOCOL 7 SEMANTIC CANDIDATE: db94a2dfb7fef480f37227eab5c45256e89901b8 — UNCHANGED
ACTUAL PROFILE/ADAPTER PRE-RUN INTEGRITY: REQUIRED / NOT YET RUN
WITHHELD-INSTANCE CHECKS: REQUIRED / NOT YET RUN
6.5/6.6/7.0 COMPARATIVE CAMPAIGN: NOT AUTHORIZED
```
