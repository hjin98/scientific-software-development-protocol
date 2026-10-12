---
status: pass
protocol_version: 6.6.0
target_protocol_version: 7.2.1
candidate_ref: aaeaf8b6b2121b9fb8aba31917c8265649c43954
semantic_ref: aaeaf8b6b2121b9fb8aba31917c8265649c43954
freeze_ref: 1d0d534930107a1ec2c36fbe9b738fea5d25d13d
semantic_base: 52ac475ce81d89b3e8ccb7c393fa0daa028d01b0
reviewer: Codex independent reviewer
date: 2026-10-12
scope: S7 step 7 frozen-candidate review
---

# Protocol 7.2.1 S7 independent review — PASS

**PASS for S7 frozen-candidate semantic preservation, documentation closeout, release-state coherence and locally executable acceptance. No candidate defect or new Serious Challenge found.** Remote public-fallback checks are **not executable here**, not passed. Their network-enabled execution remains with the design lead under the explicit network exception in the review instruction. This review does not close that evidence obligation, qualify the protocol statistically, bind ratification, authorize publication or promote accepted-current.

## Findings, ranked by severity and earliest owner

1. **Outstanding external acceptance evidence; no candidate defect.** Earliest owner: D4 repository acceptance / design lead, under the S7 network exception. The three remote groups (Protocol 6.2, 6.3 and 6.4 public bootstrap checks) cannot resolve network hosts here. The default regression reports three skips; forcing their execution reports 12 DNS-only failure records, including seven skill subtests in the 6.4 group. These are not interpreted as candidate failures or passes. The lead must supply the separate network-enabled results before claiming complete repository acceptance.
2. **Resolved environment limitation; no candidate defect.** Earliest owner: D4 acceptance environment. The initial Core installed-product build failed fetching setuptools. Without editing or bypassing the tests or their wheel/sdist consumer paths, setting pip's dependency source to cached wheels made all 32 installed-product tests execute and pass. The final full Core run passed all 385 tests across 12 modules. The initial failure remains recorded below and in the raw log.

No severity-ranked candidate repair is required. The already-recorded statistical no-go is retained as an acceptance limitation, not converted into statistical qualification by this Review PASS.

## Authority, independence and scope

Governing SSDP is **6.6.0**, using the installed software-implementation skill in Review mode. Reconstructed from `AGENTS.md`, the S7 brief, the eighteenth ruling set and designation amendment, the requested study summary, the requested S3 documentary-correction review, Git objects and the real release-state owner. The S7 brief's SHA-256 was independently verified as `18a9590986a656782cac31270dd60010bd6c1f9b075a18a3df82151f7fa7f9ba`.

This reviewer authored no candidate change and read no implementer report, hand-off or rationale. No campaign directories, fixture custody, evaluator outputs or excluded `/tmp/SSDP721-*` files were read. The specified study summary and S3 review were used only within the requested reconstruction; their campaign claims were not independently remeasured. A lightweight agent-memory registry lookup provided historical orientation only; all review decisions were reconstructed from the specified repository inputs and fresh execution. Project PEM retrieval/HAS was not activated: no mature mechanism replacement, recovery or memory-bound semantic work is performed here. Its mandatory schema acceptance command was executed.

Tests share the candidate's checked-in oracles, so fresh execution alone does not prove arbitrary prose adequacy or model compliance. Independent documentary reconstruction, exact tree comparison and a bounded abstraction-adequacy pass provide distinct checks within this review's scope.

## Semantic identity, history and release state

- `git diff --exit-code 52ac475ce81d89b3e8ccb7c393fa0daa028d01b0 aaeaf8b6b2121b9fb8aba31917c8265649c43954 -- source dist orchestrator tests`: exit **0**, empty. The required source/dist equality is exact; executable orchestration and test inputs are also unchanged from the S3 base. No semantic difference requires justification.
- `source/PROTOCOL_VERSION` at SEMANTIC_REF is **7.2.1**.
- Integration commit `04a803f5a8ccedc225078b9038f94025b236c92e` has parents `1682f6896ca283aee3498a2b4d71746ae70d9e54` and `71ed314e1db9fdc4c6365c153f056ced5ae94fca`. Both the S3 base and original candidate-branch tip are ancestors of SEMANTIC_REF (both `git merge-base --is-ancestor` checks exit 0). This is a history-preserving merge, with the original candidate commits retained, not a squash/rebase replacement.
- SEMANTIC_REF to FREEZE changes exactly **one line in one file**, `PROTOCOL-RELEASE-STATE.yaml`: `candidate.semantic_ref: UNFROZEN` becomes `aaeaf8b6b2121b9fb8aba31917c8265649c43954`. No other tree difference exists.
- Parsed `accepted_current` and `historical` mappings are identical at the S3 base, SEMANTIC_REF and FREEZE. Accepted-current remains 6.6.0 with public ref `22f4bdba53795da3a6f13f162529f3a843fc37ae` and recovery ref `384666764da4c55b282e6b1595ab97e2f86e1dc4`.
- At FREEZE, candidate version is 7.2.1, semantic_ref is SEMANTIC_REF, review is NOT_RUN/NONE, ratification is NOT_REQUESTED/NONE, and public_source_ref/recovery_ref are UNAVAILABLE. This is the intended pre-binding state, not premature promotion.
- `python source/release_state.py` passes both in the SEMANTIC_REF worktree and in the root checkout verified at FREEZE. The latter output is `/home/samjin/agent-skills/scientific-software-development-protocol/PROTOCOL-RELEASE-STATE.yaml: release state is coherent`.

The front matter binds the **semantic subject** to SEMANTIC_REF, as `_check_review_evidence` requires; FREEZE is recorded separately as the commit that binds that subject. Binding the review subject to FREEZE instead would mismatch candidate.semantic_ref.

## Documentation and bounded Challenge pass

The README remains a concise guide to purpose, protected meaning versus delegated mechanism, D1–D4 ownership, skill selection, development/review cycle, common workflows and current major doctrine. It routes detailed capability history to CHANGELOG and exact mutable release identity to `PROTOCOL-RELEASE-STATE.yaml`; it contains no concrete accepted-current, candidate, public or recovery mapping. `source/README.md` remains a valid concise source/contributor map and is byte-unchanged.

The README's concluding 7.2.1 table row carries an asterisk linking to its final reliability-warning section. Clause-by-clause review against the brief found every clause retained: text-only operation; no compliance enforcement; no 100% guarantee; dependence on model strength/capability; accepted with conditions; four rounds from 7.0 through 7.2.1 without a statistically robust pass; no statistically robust guarantee; explicit skill commands; personal review of consequential output; and the correct study-summary route. The warning is the last section and final text of the file.

CHANGELOG preserves the existing 7.2.1 capability content, replaces stale development/not-frozen/no-run language, and states the exact brief facts: patch to 7.2.0, one concurrent campaign, GLM-5.3-Flash executor, MiMo-V2.6-Flash evaluator, same 122 main-panel episodes, frozen rule, no-go, P1 FRAGILE with resolved failures 10.4% versus 17.1% and unresolved sensitivity, P2/P3 robust non-inferiority, and one unowed delegate-request failure/harm flag. It distinguishes stakeholder acceptance from statistical qualification and carries the warning and route. History records the 7.2.0 NOT QUALIFIED disposition and 7.2.1 reduction, no-go, conditional acceptance and semantic-line conclusion, linking the lessons instead of repeating their tables. Future deterministic SSDS 8.0+ work is direction, not a promise or current workplan. No reviewed current closeout prose calls 7.2.1 qualified or claims a statistical go.

Documentation closeout occurred in SEMANTIC_REF before the follow-up freeze. AGENTS.md's stable documentary invariants are satisfied and covered by the inherited regression; no new prose/keyword parser was added.

For the out-of-matrix adequacy pass, the protected global invariant was reconstructed independently: stakeholder acceptance, structural validity, Review PASS and statistical qualification must remain distinct; mutable release mappings must retain their sole owner. An otherwise locally green candidate could violate this by advertising guaranteed compliance or promoting itself through README/history. The assembled candidate does neither: its explicit warning preserves the failed statistical outcome and limits, and the real release-state owner still holds the unpromoted candidate. No surviving counterexample or new Serious Challenge was found within S7's non-semantic closeout scope. Unchanged 7.2.1 doctrine was not presented as freshly outcome-qualified.

## Fresh executed acceptance

Clean detached worktree: `/tmp/ssdp-s7-independent-worktree`, exactly SEMANTIC_REF, outside the root checkout. Fresh uv-created venv: `/tmp/ssdp-s7-independent-venv`, CPython **3.13.14**. Logs and dependency inventory: `/tmp/ssdp-s7-independent-evidence/`. All following acceptance commands ran in that worktree with its venv on PATH unless explicitly identified as the root FREEZE check.

Environment setup: `~/.local/bin/uv --cache-dir /tmp/ssdp-s7-independent-uv-cache venv --python python3 --seed /tmp/ssdp-s7-independent-venv` created the fresh environment but could not seed pip due to DNS. Bundled `python -m ensurepip` installed pip 26.1.2. A second plain uv invocation refused the already-existing fresh environment; it was not reused from any earlier task. The default validation pip install could not resolve PyYAML from the network. Exact cached wheel archives were recovered from the read-only pip download cache into `/tmp/ssdp-s7-independent-wheels`; no prior orchestrator artifact was installed. Offline installation then succeeded with pinned **PyYAML 6.0.2** and the actual candidate orchestrator build. Installed versions are preserved in `dependencies.txt`; `python -m pip check` found no broken requirements.

| Exact command (with venv Python/PATH) | Result | Raw log under evidence directory |
| --- | --- | --- |
| `python -m pip install --no-index --find-links /tmp/ssdp-s7-independent-wheels -r source/requirements-validation.txt` | exit 0; PyYAML 6.0.2 installed | `install-validation-offline.log` |
| `python -m unittest discover -s tests -v` | 433 tests in 15.878s; OK, skipped=3; 430 executed passes | `regression.log` |
| `SSDP_VALIDATE_PUBLIC_FALLBACK=1 python -m unittest discover -s tests -v` | exit 1; 438 tests in 15.662s; 12 DNS-only failure records; remote groups not executable here | `regression-remote-enabled.log` |
| `python source/release_state.py` | exit 0; release state coherent | `release-state.log` |
| `python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` | exit 0; PEM schema 1 valid: 5 families, 0 notices | `pem.log` |
| `python source/build_skills.py --output /tmp/ssdp-s7-independent-dist` | exit 0; all seven skill bundles and ZIPs generated | `build-skills.log` |
| `python source/validate_packages.py --dist /tmp/ssdp-s7-independent-dist` | exit 0; all directory bundles and ZIPs structurally valid | `validate-packages.log` |
| `python source/check_dist.py --expected /tmp/ssdp-s7-independent-dist --committed dist` | exit 0; committed dist matches fresh canonical build semantically | `check-dist.log` |
| `git diff --check` | exit 0, empty | `whitespace.log` |
| `python -m pip install --no-index --find-links /tmp/ssdp-s7-independent-wheels setuptools wheel -r orchestrator/requirements-dev.txt` | exit 0; fresh build/test dependencies installed | `install-build-offline.log` |
| `python -m pip install --no-index --find-links /tmp/ssdp-s7-independent-wheels ./orchestrator -r orchestrator/requirements-dev.txt` | exit 0; candidate wheel built and installed | `install-core-offline.log` |
| `python orchestrator/scripts/generate_protocol_snapshot.py --check` | exit 0; current 7.2 snapshot matches; frozen 5.16, 6.0–6.6 and 7.1 snapshots immutable/coherent | `snapshot.log` |
| `python orchestrator/scripts/run_core_tests.py` | initial run: 353 tests across 12 modules; installed-product setup DNS error, zero tests in that module | `core.log` |
| `PIP_NO_INDEX=1 PIP_FIND_LINKS=/tmp/ssdp-s7-independent-wheels python orchestrator/scripts/run_core_tests.py tests.test_installed_product` | exit 0; all 32 tests in 19.8s | `installed-product-offline.log` |
| `PIP_NO_INDEX=1 PIP_FIND_LINKS=/tmp/ssdp-s7-independent-wheels python orchestrator/scripts/run_core_tests.py` | exit 0; all 385 tests across 12 modules in 19.7s; installed-product 32 tests executed | `core-offline-full.log` |

The build output path substitutes a review-specific temporary directory for README's `/tmp/protocol-dist` to preserve unrelated artifacts. Offline pip flags only change dependency resolution, not candidate source, test code, isolation or the installed wheel/sdist semantic consumer. The final Core run covers actual installed-product consumption and frozen resources, not just helper imports. `git diff --check 52ac475 1d0d534` also exited 0.

### Exact unavailable output

Full unmodified stdout/stderr are retained in the raw logs above. The initial uv failure was:

```text
error: Failed to install seed packages into virtual environment
  Caused by: No solution found when resolving: `pip`
  Caused by: Request failed after 3 retries in 5.1s
  Caused by: Failed to fetch: `https://pypi.org/simple/pip/`
  Caused by: error sending request for url (https://pypi.org/simple/pip/)
  Caused by: client error (Connect)
  Caused by: dns error
  Caused by: failed to lookup address information: Name or service not known
```

Initial default validation dependency install (`--cache-dir /tmp/ssdp-s7-independent-pip-cache --retries 0 --timeout 5`) output:

```text
ERROR: Could not find a version that satisfies the requirement PyYAML==6.0.2 (from versions: none)
ERROR: No matching distribution found for PyYAML==6.0.2
```

Initial Core run, preserved verbatim:

```text
running 12 test modules across 12 workers
    ok  tests.test_config_and_projects                     28 tests    0.5s
    ok  tests.test_extension_composition                   30 tests    1.2s
    ok  tests.test_git_observation                         44 tests    1.3s
    ok  tests.test_input_binding                           31 tests    1.4s
  FAIL  tests.test_installed_product                        0 tests    8.1s
    ok  tests.test_layout_and_fitness                      21 tests    0.2s
    ok  tests.test_privacy_and_remote_truth                31 tests    2.8s
    ok  tests.test_protocol_source_and_profile             37 tests    0.6s
    ok  tests.test_public_api_seam                         31 tests    1.4s
    ok  tests.test_render_and_identity                     35 tests    2.3s
    ok  tests.test_ssdp6_profiles                          25 tests    0.4s
    ok  tests.test_workplan_resolution                     40 tests    0.8s

======================================================================
tests.test_installed_product
======================================================================
setUpClass (tests.test_installed_product.InstalledProductTests) ... ERROR

======================================================================
ERROR: setUpClass (tests.test_installed_product.InstalledProductTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/ssdp-s7-independent-worktree/orchestrator/tests/test_installed_product.py", line 62, in setUpClass
    raise AssertionError(f"wheel/sdist build failed: {built.stderr[-2000:]}")
AssertionError: wheel/sdist build failed: heck the permissions and owner of that directory. If executing
  pip with sudo, you should use sudo's -H flag.
< WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None,
  status=None)) after connection broken by
  'NameResolutionError("HTTPSConnection(host='pypi.org', port=443): Failed to
  resolve 'pypi.org' ([Errno -2] Name or service not known)")':
  /simple/setuptools/
< WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None,
  status=None)) after connection broken by
  'NameResolutionError("HTTPSConnection(host='pypi.org', port=443): Failed to
  resolve 'pypi.org' ([Errno -2] Name or service not known)")':
  /simple/setuptools/
< WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None,
  status=None)) after connection broken by
  'NameResolutionError("HTTPSConnection(host='pypi.org', port=443): Failed to
  resolve 'pypi.org' ([Errno -2] Name or service not known)")':
  /simple/setuptools/
< WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None,
  status=None)) after connection broken by
  'NameResolutionError("HTTPSConnection(host='pypi.org', port=443): Failed to
  resolve 'pypi.org' ([Errno -2] Name or service not known)")':
  /simple/setuptools/
< WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None,
  status=None)) after connection broken by
  'NameResolutionError("HTTPSConnection(host='pypi.org', port=443): Failed to
  resolve 'pypi.org' ([Errno -2] Name or service not known)")':
  /simple/setuptools/
< ERROR: Could not find a version that satisfies the requirement
  setuptools>=68 (from versions: none)
< ERROR: No matching distribution found for setuptools>=68
ERROR Command '['/tmp/ssdp-s7-independent-venv/bin/python', '-m', 'pip', '--python', '/tmp/build-env-y077xn4x/bin/python', 'install', '--ignore-installed', '--use-pep517', '--no-warn-script-location', '--no-compile', '--no-input', '-r', '/tmp/build-requirements-q2dmdzrc.txt']' returned non-zero exit status 1.


----------------------------------------------------------------------
Ran 0 tests in 8.044s

FAILED (errors=1)


353 tests across 12 modules in 8.1s -- FAILED: tests.test_installed_product
```

Remote-enabled regression failure identities and exact error messages (all DNS-only; full tracebacks in `regression-remote-enabled.log`):

```text
FAIL: test_published_protocol_62_bootstrap_remote_snapshot_is_real_and_route_complete (test_protocol_62_representation.Protocol62RepresentationTests.test_published_protocol_62_bootstrap_remote_snapshot_is_real_and_route_complete)
AssertionError: published bootstrap cannot resolve source/PROTOCOL_VERSION at exact ref 5a062ebc472755607b9dc66d33a5ebbc4b7429aa: <urlopen error [Errno -2] Name or service not known>
FAIL: test_published_bootstrap_snapshot_is_real_self_reference_safe_and_route_complete (test_protocol_63_bootstrap.Protocol63BootstrapTests.test_published_bootstrap_snapshot_is_real_self_reference_safe_and_route_complete)
AssertionError: Protocol 6.3 bootstrap cannot resolve source/PROTOCOL_VERSION at exact ref 86c13cab6bdd1991dffa94e277db8eacf87e2e11: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_current_routes_are_publicly_resolvable (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_current_routes_are_publicly_resolvable)
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve source/roles/scientific-formulation/SKILL.md at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_is_64_and_self_reference_safe (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_is_64_and_self_reference_safe)
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve source/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='scientific-formulation')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/scientific-formulation/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='numerical-algorithm-design')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/numerical-algorithm-design/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='software-design')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/software-design/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='software-implementation')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/software-implementation/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='software-documentation')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/software-documentation/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='repository-hygiene')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/repository-hygiene/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_package_text_surface_matches_64 (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_package_text_surface_matches_64) (skill='software-maintenance-audit')
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve dist/skills/software-maintenance-audit/PROTOCOL_VERSION at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
FAIL: test_exact_ref_profile_and_distribution_identity (test_protocol_64_bootstrap_readiness.Protocol64BootstrapReadinessTests.test_exact_ref_profile_and_distribution_identity)
AssertionError: Protocol 6.4 bootstrap candidate cannot resolve orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.4/profile.json at exact ref e09a9d1480211eea2d16d722182bb5c6de1bee12: <urlopen error [Errno -2] Name or service not known>
Ran 438 tests in 15.662s
FAILED (failures=12)
```

Final Core run, preserved verbatim:

```text
running 12 test modules across 12 workers
    ok  tests.test_config_and_projects                     28 tests    0.5s
    ok  tests.test_extension_composition                   30 tests    1.2s
    ok  tests.test_git_observation                         44 tests    1.3s
    ok  tests.test_input_binding                           31 tests    0.5s
    ok  tests.test_installed_product                       32 tests   19.6s
    ok  tests.test_layout_and_fitness                      21 tests    0.2s
    ok  tests.test_privacy_and_remote_truth                31 tests    2.8s
    ok  tests.test_protocol_source_and_profile             37 tests    0.6s
    ok  tests.test_public_api_seam                         31 tests    1.3s
    ok  tests.test_render_and_identity                     35 tests    2.3s
    ok  tests.test_ssdp6_profiles                          25 tests    0.3s
    ok  tests.test_workplan_resolution                     40 tests    0.8s

385 tests across 12 modules in 19.7s -- OK
```

## Handoff boundary

No commit, push, release-state edit, ratification binding or candidate repair was performed. The root pre-existing `.claude/` was left untouched. Only this review file is added to the root worktree. The temporary review worktree is removed with `git worktree remove`; execution logs and the venv remain outside the checkout for inspection. The short completion note is written to `/tmp/SSDP721-S7-REPORTS/REVIEW-DONE.md`. Await design-lead direction; network-enabled remote acceptance remains explicitly open.

Cleanup/record verification: `git worktree remove /tmp/ssdp-s7-independent-worktree` exited 0. Real-owner `_front_matter` and `_bound_candidate_ref` parsing passed with status `pass` and the exact SEMANTIC_REF; committed evidence-route validation is deferred to the authorized post-commit binding step. Final root status contains only the pre-existing untracked `.claude/` and this untracked review.
