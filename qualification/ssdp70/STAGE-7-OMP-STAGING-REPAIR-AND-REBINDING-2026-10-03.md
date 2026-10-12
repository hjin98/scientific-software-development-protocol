# Stage 7 OMP staging repair and replacement-profile preparation

**Governing protocol:** SSDP 6.6.0. **Roles:** D3 disposition / D4 implementation owner (AI agent `/root`).

**Status: D4 repair verified by focused, full affected regression and real-fixture staging checks; replacement campaign and executor re-entry BLOCKED.** The repair is uncommitted, so it has no immutable executable candidate head. The frozen custody package's source/profile applicability records and its independent Gate 1 PASS bind the previous harness and profile. A fresh independent checker must reconcile the replacement binding before executor re-entry; this implementation context does not grant that PASS or runner admission.

## Challenge disposition and bounded design

The [executor Serious Challenge report](STAGE-7-OMP-SEMANTIC-ADMISSION-EXECUTOR-REALIZATION-AND-SERIOUS-CHALLENGE-2026-10-03.md) correctly identifies a staging failure. Independent reproduction through the original, hash-verified `build_project` produced `CalledProcessError(1, ['git', 'init', '-q'])` on a synthetic `0500` directory / `0400` file fixture. This is a D4 concretization defect: an immutable custody source and a writable run copy can coexist. No change to the accepted three-principal architecture, fixture semantics, scoring, custody protection or protocol source is required.

Strategy A is selected under the stakeholder's upstream repair instruction. `qualification/ssdp70/eval/harness70.py::build_project` now adds owner read/write/search access to copied working directories and owner read/write access to copied files before Git setup. Existing execute and group/other bits remain unchanged. The traversal does not follow directory links or chmod file links created by a history script. Normalization applies to the run copy after copying; the frozen source is untouched. Blanket `0755`/`0644` modes were rejected because they erase executable distinctions and broaden access unnecessarily.

Strategy B is unnecessary for this defect and would require custodian-controlled repackaging, a new freeze and new pre-run evidence. The retained failed realization is preserved; no downstream evaluator completion was requested or performed.

## Candidate, profile and retained evidence

- Working checkout head: `c9e79dba0227739638c3a452f8edd213074ede98`; executable repair is an uncommitted delta. This head is **not** claimed to contain the repair.
- Immutable semantic subject remains `db94a2dfb7fef480f37227eab5c45256e89901b8`; the p66/p70 semantic arms are unchanged.
- Previous harness SHA256: `b01485bcc1513aed71afe62d9502b2de08e60993fc926737485df564f5689821`.
- Repaired harness SHA256: `4b92ca4d35e203e1501e4c0e1991a95ecd9efcaecb1104ef16b315a272e8c2ed`.
- Historical campaign: `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261003T005805Z-3ce07101a33b-hostbound`; historical profile key `3ce07101a33bb427453dcfa862f811bfdf276a073d4e2662e3624b924a0be8b6`.
- Prepared replacement profile key: `1aca2ba13f56338dfca5dcd596ad17c85389741216484add8294b5383d18613e`.
- Prepared artifact root: `/home/samjin/ssdp70-omp-stagef/admission/profile-preflights/OMP-STAGE7-STAGING-REPAIR-20261003T171024.437365Z`. `profile.json`, `capabilities.json`, `identity.json`, `staging-checks.json`, `baseline-counterexample.json`, `integrity-and-applicability.json`, preparation script and test logs are retained there. Identity explicitly states `PREPARED_PROFILE_ONLY_NOT_EXECUTOR_READY`, `candidate_head: null` and `campaign: null`.
- Prepared artifact freeze: `5044da47eb6192522e64d4c73e28584ce76053de3af271ab55ca2d7c0609b127`, covering 15 payload files; files are `0400`, directories `0500`. These same-UID permissions are behavioral tamper barriers, not cryptographic separation. The manifest supplies hash integrity; no independent custody/admission is claimed for implementer-prepared artifacts.

The production `omp.freeze_profile` regenerated execution-support, host and runtime bindings. The historical source profile and capability snapshot were loaded with `core70.load_profile` and checked against the exact historical key and DeepInfra / `zai-org/GLM-5.3-Flash` / `https://api.deepinfra.com/v1/openai` route. Route, reasoning and budgets were inherited; capability bytes were copied unchanged. `omp.profile_errors` returned no errors. This establishes profile preparation/consistency, not a real-provider probe or admission.

`profile-delta.json` confirms exactly two changed profile fields: `profile_id` and `containment_policy.execution_support_sha256.harness70.py`. Host, runtime, provider route, reasoning, budgets, principal files and other support bindings match the historical profile; capability bytes are identical.

Hash-only integrity verification checked all 423 custody payload files and all 1,222 failed-realization payload files, plus zero writable bits on payload files and directories. Manifest SHA256 values remain respectively `be7d76d7d2d9d6a79447462ae1679f303cb3ae8f009d5077bcfc8e7cad62ad7d` and `1c6af7aa8a1f03eb5aa43ae22351e6dee1295598f220d9ba898c2d9f747ff80c`. Withheld payloads were accessed for hashing only; no withheld keys or semantic contents were inspected. Old campaign/profile/custody/realization files were not edited.

## Executed evidence and limits

1. Requested portable/OMP-unit/Stage-7-campaign tests: **124 passed, zero skips**, outside the outer sandbox. The initial sandboxed run passed with one connected-stream/seccomp skip; it is incomplete evidence, superseded for this check by the complete execution. New real-owner tests cover frozen nested fixtures, Git initialization/commit/diff, file edits/creation, executable-bit preservation, source byte/mode preservation and external symlink-target protection.
2. Real `build_project` integration against all three public frozen fixture projects (`atlas`, `reactor`, `survey`): **PASS**. Each staging initialized a clean Git tree, permitted working-file edits and file creation/deletion, and preserved every source project entry's bytes and modes. No subject/provider launch occurred in these staging checks.
3. Original-harness counterexample: **expected failure reproduced** at the real Git initialization boundary; this discriminates the staging defect from an unrelated provider/runtime issue.
4. `python3 -m py_compile` on the changed modules, `git diff --check`, and PEM schema validation: **PASS**. Protocol source/generated distributions/Core snapshots are unchanged; their generation and parity are outside this local evaluation-harness change.
5. Full affected `python3 -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -v` regression outside the outer sandbox: **313 passed, zero failures/errors/skips**, in 1175.096 seconds. The focused tests are included in this count, not additional independent evidence. OMP integration tests use the real retained runtime with local controlled provider dependencies; they do not substitute for a replacement-profile real-provider admission campaign. `affected-regression.log`, `focused-tests.log`, `test-results.json` and exact `source-candidate/` bytes are retained with the prepared profile.

One preflight instrument initially required Git's newly created object files to be writable and failed that overbroad assertion. Its prepared profile directory `OMP-STAGE7-STAGING-REPAIR-20261003T170937.212378Z` and `preflight-failure.json` are retained. The instrument was corrected to check the mutable working tree, excluding `.git`; candidate source was unchanged. Two preparation profile IDs were minted with identical repair bytes and inherited route/budgets, and zero real-provider realizations were run. No semantic results or favorable matrix arms were selected.

## Rebinding and re-entry obligations

1. Obtain an authorized immutable commit of the reviewed repair, rerun any materially affected checks if bytes change, and use its actual executable head. This context did not commit, relabel the old head, or bypass `_require_candidate_head`.
2. Use the existing `omp_stage7_campaign.py freeze-inherit` owner with the historical profile/capability snapshots and explicit expected historical key/provider/model/upstream, a unique replacement profile ID/label, the actual repaired candidate head, and the unchanged semantic subject. Freeze/init a **new** campaign; preserve the historical campaign and failed realization. Regeneration must preserve the reviewed route/budgets/capabilities and bind the final executing support bytes. Do not hand-edit old profile or campaign manifests.
3. Have the fixture custodian / fresh independent pre-run checker disposition the exact applicability delta. In the custody `bound-source-applicability.json`, the harness is the only changed file among 14 bound source files; expected profile key and document identity also change. `machine-denial-audit.json` and `remaining-obligations.json` bind the historical profile/Gate 2 route. Frozen records remain historical. The independent owner must issue an explicit, hash-bound replacement applicability/rebinding disposition, or require a custodian successor freeze if its contract demands one. This implementer cannot silently carry the old PASS forward or edit the frozen audits. No fixture/oracle retuning is authorized.
4. Complete the required fresh replacement-profile real-provider probe with `execution_mode=probe`, `evidence_state=COMPLETE_ADMISSIBLE`, `qualification_outcome=NOT_EVALUATED`, preserving separate failed attempts and using only the approved credential mechanism. A missing approved credential is blocking; none was read or substituted during profile preparation.
5. Only after the applicable pre-run/source/probe gates pass, return to a fresh Stage 7 Executor context for an append-only realization under the replacement campaign and unchanged frozen semantic matrix. Preserve all failures and the frozen rerun/exposure policy; this bug-fix retry must be recorded under that policy, never silently counted as extra independent opportunities. Gate 3 evaluator admission, Gate 4 evaluation and Gate 5 independent final admission remain separate and unexecuted here. OMP remains **UNADMITTED**; no blinded Protocol 7 qualification subject is authorized.

Reopen D3 if writable-copy staging requires a changed principal boundary, weakened custody/containment, altered fixture semantics or a new production execution path. Current evidence requires none of those changes. Stop on any required check failure/skip, profile/runtime mismatch, missing independent applicability disposition or unavailable credential.

## Project-memory applicability and impact closure

The project-governed integrated PEM base is `main` at `2585b73f00420daca185a4fbb9ac42a79473eda1`; current PEM bytes have zero diff against that publication and schema 1 validation passes. No branch PEM delta is composed and no PEM update is made. Canonical metadata for all five families and current notices was searched; coverage remains partial, not proof of absent history.

An additional validation attempt on an identical snapshot copied to `/tmp` reported unavailable local Git routes because that copied file was outside its repository context. It is not admissible route-validation evidence or a defect in canonical PEM. Canonical-path validation and exact base/branch byte equality establish the stated bounded check.

```yaml
pem_basis:
  accepted_project_state: 2585b73f00420daca185a4fbb9ac42a79473eda1
  accepted_pem: hjin98/scientific-software-development-protocol@2585b73f00420daca185a4fbb9ac42a79473eda1:PROJECT-ENGINEERING-MEMORY.md
  candidate_overlay_semantic_candidate: NONE
has:
  - id: PC-001
    disposition: APPLICABLE
    reason: Preservation discipline; historical evidence remains unchanged as independently required by this task and the Stage 7 workplan. No older protocol is adopted as this task's governing authority.
  - id: DS-001
    disposition: APPLICABLE
    reason: Staging and synthetic tests cannot establish real-profile semantic admission.
  - id: FF-001
    disposition: NOT_APPLICABLE
    reason: No public-source protocol bootstrap is published.
  - id: SP-002
    disposition: NOT_APPLICABLE
    reason: No protocol fallback/recovery publication or self-reference construction changes.
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: No source router or generated package is changed.
```

This is one first-clean local staging defect, not an established recurrence or mature mechanism replacement. Closeout learning does not justify a durable PEM update. Changed evidence applicability is retained in this report and the external preflight artifact. Historical Gate 1 findings and failed execution remain inspectable; only the affected candidate/source/profile applicability is stale for replacement execution. Implementation acceptance, immutable campaign rebinding, independent pre-run clearance and final semantic admission are distinct completion boundaries.
