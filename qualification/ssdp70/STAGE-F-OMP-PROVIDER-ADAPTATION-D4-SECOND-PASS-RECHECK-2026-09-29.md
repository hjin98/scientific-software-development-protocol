# OMP-only Stage F provider adaptation — bounded second-pass D4 repair and recheck

**Date:** 2026-09-29
**Governing SSDP:** 6.6.0
**Starting checkout:** `ssdp-7.0-scientific-epistemic-closure` at `f1e07849e7fa595cc20ac9a823edf8f0763a7c40`
**Exact tested D4 candidate commit:** `99463b24863525391c51b438e60c40d501fe54ab`
**Status:** The bounded second-pass repairs and required exact-candidate regression passed. OMP remains **UNADMITTED**. This record is evidence for a fresh independent D4 review; it is not runner admission or Protocol 7 qualification.

This record is committed as an evidence-only descendant of the tested code candidate; it changes no executable or test files.

## Authority and scope

The implementation follows the accepted OMP three-principal D3 graph and the “D4 bounded second-pass repair after independent implementation NO-PASS” amendment in `workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md`, contract §1 items 1–11 and §6, and the current OMP implementation. The prior implementation/review records were used as defect and evidence input, not as architecture authority. The repair stays within D4: no principal, authorized data-flow edge, provider proxy, semantic event kind, frozen fixture/oracle/scoring threshold, custody rule, Claude behavior, or Pi adaptation was added or changed.

`subject_launcher.py` is supervisor-authored control machinery that realizes the supervisor-controlled subject-side endpoint of the already-authorized inference and MCP edges. It is not a fourth trust principal and owns no provider credential, mediator backing state, or custody data.

## Changes

- `qualification/ssdp70/eval/adapters/omp.py`: explicit dependency staging and digest/provenance binding; observer-boundary evidence validation; explicit non-oracle classification for the closed set of observer control records; complete response-body/truncation checks; graceful EOF shutdown of the observer and bridge evidence chains.
- `qualification/ssdp70/eval/observer70.py`, `mcp_bridge70.py`, and `seccomp70.py`: least-privilege observer setup, one-time credential handoff after lockdown, connected-route-only transport controls, hostile boundary probes, and normal terminal-chain closure on the existing descriptor edges.
- `qualification/ssdp70/eval/profiles/omp-headless.template.json`: profile binding to the dependency-manifest digest and updated observer boundary identity.
- `qualification/ssdp70/eval/stand_in_provider.py`, `test_omp_integration.py`, and `test_omp_units.py`: deterministic complete HTTP responses, assembled hostile/truncation coverage, and manifest/seccomp/normalization checks.
- Added `qualification/ssdp70/eval/omp-runtime-dependencies-18.0.11.json`.
- Removed all 33 empty discovery/config-shaped residue files introduced by `8e98fa6864ecd6119b28ae7fc8639d9f44efa7d4: root `.bash_profile`, `.bashrc`, `.gitconfig`, `.gitmodules`, `.idea`, `.mcp.json`, `.profile`, `.ripgreprc`, `.vscode`, `.zprofile`, `.zshrc`; root `.claude/{agents,commands,hooks,launch.json,loop.md,output-styles,routines,scheduled_tasks.json,settings.json,skills,workflows}`; `qualification/.mcp.json`; `qualification/ssdp70/.mcp.json`; and `qualification/ssdp70/eval/.claude/{hooks,launch.json,loop.md,output-styles,routines,scheduled_tasks.json,settings.json,skills,workflows}`. None had independent repository authority.

No files under `source/` or `dist/` changed. No active workplan, frozen semantic candidate, custody material, prior Claude evidence, or frozen profile evidence changed.

## Second-pass acceptance evidence

1. **Exact final candidate commit.** `99463b24863525391c51b438e60c40d501fe54ab` on `ssdp-7.0-scientific-epistemic-closure`, descendant of the verified requested starting head. The working tree was clean before the full exact-candidate regression.

2. **Files changed.** The eight OMP evaluation files and one new manifest listed above, plus deletion of the 33 residue files. The commit records 42 changed paths.

3. **Observer privilege boundary.** The observer runs under Bubblewrap user, mount, PID, IPC, UTS, cgroup, and private network namespaces with only staged runtime roots, synthetic `/etc`, observer code, the connected provider-route socket, inference descriptors, evidence descriptor, and credential handoff descriptor. It drops capabilities, sets no-new-privileges, installs seccomp, and records the resulting namespace and `/proc/self/status` state. In the exact assembled hostile tests, `CapEff`, `CapPrm`, and `CapBnd` are zero; `NoNewPrivs=1`; `Seccomp=2`; host HOME, custody, supervisor-private, and mediator-backing reads fail because those paths are absent from the observer filesystem view; unrelated process inspection/control and socket creation are denied. The probes execute inside the observer boundary and are retained in its hash-linked chain during the run.

4. **Exact provider-route restriction.** The observer establishes the profile-frozen route, records the peer address, then removes general network creation/retargeting authority. Seccomp denies new sockets and `connect`; only null-address I/O on the already-connected provider stream is allowed, while addressed `sendto` and vectored sends/receives are denied. The assembled run records successful traffic to the local provider stand-in and denial of unrelated egress. No generic proxy or fourth principal was introduced.

5. **Subject runtime dependency surface and provenance.** The subject no longer receives host `--ro-bind /usr /usr`. It receives the staged entries in `qualification/ssdp70/eval/omp-runtime-dependencies-18.0.11.json`; the manifest SHA-256 is `dc2a6035d72e889d80f97e6c048f517765e1c2ade480171aa4e160a59f4c35f1`. The explicit set covers OMP's frozen executable separately, the retained Bash/Python runtime and required shared libraries, loader, observer TLS material, and minimal synthetic `/etc`; it binds only the listed roots/files and aliases. The execution profile, realization, and retained adapter provenance bind the manifest SHA-256 and per-principal staged-tree digests; launch and post-run validation fail closed on manifest or source drift. Host Git, package-manager executables, compiler/toolchain binaries, HOME/configuration, and unrelated host software remain unavailable in the assembled subject probes. The manifest includes the Python 3.10 standard-library tree (1,492 entries) used by the retained Python launcher/runtime and executor Python probes; it does not bind the host's entire `/usr` tree.

6. **Response truncation.** `B1RealObservationAndEventCompleteness.test_provider_response_over_evidence_limit_is_inadmissible_on_the_assembled_path` drives a response 1,024 bytes over the observer's 4 MiB retention limit through `harness70.run_episode`. The observer marks `body_truncated_in_evidence`; normalization reports “truncated in evidence”; the run is not `COMPLETE_ADMISSIBLE`. The digest is not used to excuse partial retained bytes.

7. **Discriminating local IPC probe.** `B2PrivilegeSeparationWhileInferenceWorks.test_discriminating_external_local_ipc_sentinel_is_unreachable` ran with the outer host sandbox permission required for AF_UNIX operations. The supervisor test process bound and listened on its sentinel outside the subject PID/process namespace. Executor-controlled Bash/Python issued `socket(AF_UNIX, SOCK_STREAM)` inside the contained OMP run; the subject boundary returned `EPERM`, and the external sentinel accepted zero connections. The same assembled run completed inference and MCP calls. This is a positive attempted syscall with an inner-boundary denial, not an outer-sandbox skip.

8. **Residue cleanup.** All 33 zero-byte residue paths were removed. The exact-candidate `ProviderManagedStateAndDiscoveryEffects` hostile discovery tests passed, including ancestor, repository/project, HOME, dotenv, and prompt/config sources. No residue path was retained as a fixture.

9. **B1 disposition: PASS for this D4 feasibility recheck.** The real executing inference path retains hash-linked request/response records. The observer/control records are separately checked and explicitly classified as reviewed non-oracle observer-control evidence; unknown record kinds still fail closed. Runtime model/reasoning/catalog/native-tool/MCP/configuration evidence comes from actual OMP traffic. The assembled suite passes truncation, alteration, omission, reordering, duplicate, response-binding, tool-surface, root/resource, and mediator cross-check cases.

10. **B2 disposition: PASS for this D4 feasibility recheck.** Observer and subject boundaries, credential separation, provider-route restriction, unrelated network denial, Bash/second-OMP relay denial, host/supervisor/mediator/custody/evidence denial, explicit subject dependencies, and the discriminating local-IPC attempt all passed on the assembled path. This does not admit the OMP profile.

11. **B3 disposition: PASS for the exact-build discovery recheck.** The residue files were removed before the exact-candidate test run. Exact-build inventory, provider-managed-state perturbation, hostile project/HOME discovery, and ancestor-directory discovery tests passed. Newly uncontrolled provider-managed state continues to fail closed for affected claims.

12. **Preserved prior D4 capabilities.** The exact-candidate suite exercised and passed the real `harness70.run_episode → adapters.omp → Bubblewrap → frozen OMP 18.0.11` path; supervisor-owned MCP bridge and unchanged mediator; launcher-started-instance relay authorization; descriptor-bound inference/MCP transport; raw observer/bridge/launcher evidence and harness normalization; runtime-derived catalog/tool/MCP/configuration observation; successful-read plus model-consumption root selection; lossless six-operation mediator normalization; exact native tool surface; exact-build provider/discovery inventory; runtime-injected-steering fail-closed behavior; and shared control-path/symlink/Git protections. No admissible evidence falsified these preserved capabilities.

13. **T1/T7/T8 observability.** The mechanism observes exact ordinary root selection only after a successful read and model consumption, and records the exact consumed resource. Missing root/resource evidence makes a burden claim inadmissible. This supports the observability mechanism; it is not a T1/T7/T8 qualification result. Exact-profile operator probes and the complete §1/§6 runner-admission recheck remain pending, and a claim stays claim-scoped inadmissible if its required material cannot be observed.

14. **Tests executed on the exact candidate commit.** From clean HEAD `99463b24863525391c51b438e60c40d501fe54ab`, with outer-sandbox permission enabled for the AF_UNIX discriminator:

   ```text
   python3 -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -v
   Ran 228 tests in 491.209s — OK; 0 skipped.
   ```

   This includes all 50 assembled OMP integration tests, 44 OMP unit tests, and 134 portable/control-path/harness/MCP/Claude/Stage-F regression tests. `python3 -m compileall -q qualification/ssdp70/eval` and `git diff --check` also passed on the same implementation content before the candidate commit.

15. **Required checks unavailable or not executed.** No second-pass required check was skipped or unavailable. The local deterministic provider stand-in is the authorized substitution below the semantic owner under test; no external provider was contacted. Per task boundary, no runner admission, exact-profile operator qualification, Protocol 7 qualification subject, Stage G/H work, or Pi implementation was performed. Contract §1 items 1–11 and §6 admission work remain pending and are not asserted here.

16. **Shared Claude regression.** Passed as part of the same exact-candidate 228-test command: `test_control_path_policy`, `test_harness_integration`, `test_portable70.ClaudeAdapterTests`, `test_mcp_stdio`, `test_stage_f_integrity_repairs`, and `test_stage_f_v4_repairs`. No Claude adapter/core behavior was changed.

17. **D3 reopen condition.** None occurred. The concrete implementation remains within the accepted qualification-supervisor / trusted provider-control-observer / subject-executor graph. The qualification mediator remains in the supervisor trust domain. No generic provider proxy, fourth principal, or additional subject-facing edge was introduced.

18. **Unresolved risks and limits.** OMP remains unadmitted pending fresh independent D4 review, exact-profile operator probes, and the full §1/§6 runner-admission checker. Tests use a deterministic local provider stand-in and establish only the declared local profile properties. The manifest's standard-library tree is exact and digest-bound but not minimized module-by-module. Existing runtime-home inventory reports content hashes only for files up to its configured size bound; large OMP-extracted native runtime files are identified by path/size/class but do not receive individual content hashes. Assess whether those limitations affect any later profile/claim before admission; keep affected claims inadmissible until resolved where material.

## Project-memory applicability

The active workplan binds the accepted integrated memory base; `main` remains at `2585b73f00420daca185a4fbb9ac42a79473eda1`. The accepted PEM blob is `1561797125622f355f84eb27319f87e8fa4227d9`, identical on this candidate; the branch has no candidate overlay. The repository validator reports schema 1 valid, five families, zero notices. Coverage remains `PARTIAL`; stale front-matter and PC-001 binding metadata are not treated as current authority. No PEM was edited.

```yaml
pem_basis:
  accepted_project_state: 2585b73f00420daca185a4fbb9ac42a79473eda1
  accepted_pem: "hjin98/scientific-software-development-protocol@2585b73f00420daca185a4fbb9ac42a79473eda1:PROJECT-ENGINEERING-MEMORY.md"
  candidate_overlay_semantic_candidate: NONE
has:
  - id: DS-001
    disposition: APPLICABLE
    reason: The proxy-proof lesson bounds these tests to the assembled OMP/runtime properties they execute and prevents treating repository-green evidence as OMP admission or semantic qualification.
  - id: FF-001
    disposition: NOT_APPLICABLE
    reason: This D4 adapter repair does not publish or replace a protocol public-source fallback.
  - id: PC-001
    disposition: NOT_APPLICABLE
    reason: Frozen prior-version resources and recovery identities are not changed by this evaluation-only repair.
  - id: SP-001
    disposition: NOT_APPLICABLE
    reason: No canonical router or generated distribution is changed or regenerated.
  - id: SP-002
    disposition: NOT_APPLICABLE
    reason: This repair does not perform successor-source or recovery publication.
```
