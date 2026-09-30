# OMP-only Stage F provider adaptation — bounded third-pass D4 repair and recheck

- **Date:** 2026-09-29
- **Governing SSDP:** 6.6.0
- **Starting checkout:** `ssdp-7.0-scientific-epistemic-closure` at `758ba1755938e663b0e07a1921998eca8aababf4`
- **Exact implementation commit:** `3811104a876b0510c1839a1260e5c86c5e7fa093` (direct child of the requested starting head)
- **Status:** The bounded third-pass repair and exact-commit regression passed. OMP remains **UNADMITTED**. This implementation record is not a fresh independent D4 acceptance, runner admission, exact-profile operator qualification, or Protocol 7 qualification.

This superseding record preserves the prior recheck history. The next step is a fresh independent D4 recheck of the exact implementation commit. No Stage G/H, runner admission, Protocol 7 qualification subjects, exact-profile operator qualification, or Pi work was performed.

This record is committed separately as an evidence-only descendant of the implementation commit; it changes no executable or test files.

## Authority and scope

The repair was reconstructed from the repository `AGENTS.md`; the accepted OMP three-principal D3 architecture and B1/B2/B3 feasibility gate; the original D4 tranche, bounded second-pass repair, and the workplan amendment “D4 bounded third-pass observer-launch safety repair after independent NO-PASS”; contract §1 items 1–11 and §6; and the current implementation under `qualification/ssdp70/eval/`. The executable second-pass candidate `99463b24863525391c51b438e60c40d501fe54ab` and evidence-only descendant `7a0ecc1c198c98a861ec7b1552c614a13ecf5ba1` were treated as evidence and defect history, not as authority.

The single defect was the use of `subprocess.Popen(..., preexec_fn=_observer_fd_map(...))` after Python threads had started. The repair removes that process-creation callback from the production OMP observer launch and adds a one-shot, supervisor-owned FD preparation helper. It does not redesign the accepted architecture or change the Stage F oracle.

The implementation commit changes only these evaluation files:

- `qualification/ssdp70/eval/adapters/omp.py`
- `qualification/ssdp70/eval/observer_exec_helper70.py` (new)
- `qualification/ssdp70/eval/test_omp_units.py`
- `qualification/ssdp70/eval/test_omp_integration.py`

No file under `source/` or `dist/`, immutable Protocol 7 candidate, contract, fixture/oracle/scoring threshold, custody semantics, historical Claude evidence, prior frozen qualification evidence, Pi adaptation, normalized-event contract, or shared Claude behavior was modified.

## Repair and exact descriptor semantics

`adapters.omp.launch` now invokes `subprocess.Popen` with no `preexec_fn`, `close_fds=True`, and `pass_fds` containing exactly the four already-authorized observer channel source descriptors plus the transient Bubblewrap-argument pipe. The existing drain threads remain in their original order; safety does not depend on moving them after process creation.

Popen starts a fresh helper interpreter with isolated mode and site initialization disabled. The helper uses `F_DUPFD_CLOEXEC` to make temporary copies before remapping, so source descriptors may overlap target numbers without clobbering a later source. It duplicates only these descriptors to the observer interface:

| Capability | Supervisor source | Observer descriptor |
| --- | ---: | ---: |
| Inference input, subject to observer | `infer_up[0]` | 3 |
| Inference output, observer to subject | `infer_down[1]` | 4 |
| Append-only observer evidence output | `obs_ev[1]` | 5 |
| One-time credential input | `credential_r` | 6 |
| Transient Bubblewrap argument input | `observer_args_r` | 7 |

The four channel source numbers and argument source number are recorded in `observer-boundary-argv.json`; the runtime test verifies that the passed set contains exactly those five descriptors. The helper closes its temporary copies and non-target source descriptors, then immediately `execv`s Bubblewrap with `--args 7`. Popen's `close_fds=True` prevents unrelated inheritable supervisor descriptors from crossing into the helper; the only other descriptors are the existing controlled standard streams (stdin from `/dev/null`, stdout/stderr drained by the supervisor). The helper does not read or own credential bytes. The credential pipe remains empty until the observer has emitted `boundary-ready`; the supervisor then sends the one-time credential through descriptor 6, after lockdown and before `ready`.

There is no Python callback between process creation and exec. The multithreaded supervisor creates only a normal Popen child with no `preexec_fn`; FD manipulation runs in the new helper process, and its only post-mapping action is immediate exec of Bubblewrap. This avoids the fork-child Python callback/deadlock hazard identified for CPython 3.10 without relying on thread reordering.

The helper is a one-shot qualification-supervisor launch mechanism, not a fourth D3 principal. It owns no provider credential, mediator backing state, custody material, service, or daemon lifecycle, and creates no new subject-facing edge. Its source digest is `8891d415d3d0c10bea887caabdfda6bb9f510523f5a1e54eda4d45165a270972`; it is included in the existing adapter principal/provenance file map and `adapter_support_sha256` run identity. The assembled FD test checks the emitted helper digest against the run identity.

## Exact-commit acceptance evidence

1. **Exact implementation commit.** Commit 3811104a876b0510c1839a1260e5c86c5e7fa093, parent 758ba1755938e663b0e07a1921998eca8aababf4, on ssdp-7.0-scientific-epistemic-closure. The requested starting head was verified before editing; there were no intervening commits. The full regression ran on this implementation commit.

2. **Chosen thread-safe process-launch mechanism.** Option B was selected: a one-shot, supervisor-owned Python exec helper starts through subprocess.Popen with no preexec_fn, maps only the reviewed descriptors, then immediately execs Bubblewrap in the same PID. The existing supervisor drain threads retain their original creation order.

3. **No fork-with-Python-preexec hazard.** No Python callback runs between process creation and exec. The multithreaded supervisor makes a normal Popen call without preexec_fn; deterministic FD preparation happens in the fresh helper process, and its only post-mapping action is immediate exec. The implementation therefore does not run Python code in the forked child before exec and does not depend on reordering threads.

4. **Exact FD mapping and closure.** The mapping table above identifies the exact sources: infer_up[0] → observer FD 3, infer_down[1] → FD 4, obs_ev[1] → FD 5, credential_r → FD 6, and observer_args_r → Bubblewrap FD 7. Popen passes exactly those five source descriptors with close_fds=True; stdin is /dev/null and stdout/stderr are the existing supervisor-drained streams. The helper makes F_DUPFD_CLOEXEC temporary copies to avoid clobbering overlapping source/target numbers, duplicates only the four channels and the argument pipe to targets 3–7, closes its temporary copies and non-target source descriptors, and execs Bubblewrap with --args 7. Credential bytes are sent by the supervisor only after boundary-ready and before observer ready.

5. **Unrelated supervisor sentinel excluded.** test_omp_integration.ThirdPassObserverLaunchSafety.test_real_observer_fd_map_excludes_inheritable_supervisor_sentinel opens an unrelated inheritable supervisor FD at 256 or above and runs the real assembled path. The test confirms the sentinel path is denied inside the observer, the exact 3/4/5/6 channel map and FD 7 argument map, exact five-entry pass_fds, successful inference and MCP, a helper digest bound in run identity, and a closed observer evidence chain.

6. **Helper presence, trust ownership, and digest.** The helper was added. It is transient qualification-supervisor launch machinery, not a fourth principal; it owns no provider credential, mediator backing state, or custody material, and is not a daemon/service. Its bytes are bound through the existing adapter principal/provenance file map and adapter_support_sha256 run identity. Its SHA-256 is 8891d415d3d0c10bea887caabdfda6bb9f510523f5a1e54eda4d45165a270972, and the assembled test compares the reported digest with the run identity.

7. **Multithreaded assembled launch.** test_omp_integration.ThirdPassObserverLaunchSafety.test_repeated_launches_with_active_threads_have_an_outer_watchdog runs the complete harness70.run_episode → OMP adapter → helper → Bubblewrap → frozen OMP 18.0.11 → local provider stand-in → supervisor MCP bridge/mediator → evidence normalization path with four unrelated supervisor threads active. All runs reached COMPLETE_ADMISSIBLE, performed provider inference and a normalized MCP operation, and emitted a valid observer chain with boundary, post-lockdown credential receipt, ready, request, and response.

8. **Repeated launch and independent watchdog result.** The multithreaded test completed three assembled launches. Its independent outer watchdog is 90 seconds while the normal per-episode timeout is 120 seconds; a stall during helper/Bubblewrap process construction fails the outer test instead of waiting for the episode timeout. All three launches completed within the bound, with thread activity observed during each launch.

9. **Observer privilege separation preserved.** The full suite passed the assembled hostile probes for Bubblewrap filesystem, user, PID, IPC, cgroup, and private-network isolation; capability drop, no-new-privileges, and observer seccomp; credential-after-lockdown; connected provider route success and unrelated-egress denial; host HOME, custody, supervisor, mediator, and evidence-state denial; Bash inference/MCP denial and second-OMP relay denial; minimal runtime dependencies with omitted host software; and the positive local-IPC denial probe. No boundary, seccomp, capability, route, credential, or observer evidence drain was removed or weakened.

10. **B1 preserved.** B1 remained PASS for this bounded feasibility recheck. Runtime-derived catalog, native-tool, MCP, and configuration evidence; exact native-tool-surface and raw-to-normalized completeness; request/response binding; mutation, omission, duplicate, truncation, and reordering failures; categorical greater-than-4-MiB observer-response truncation rejection; and successful-read plus actual-model-consumption root/resource selection all passed. The MCP bridge remains supervisor-owned and the mediator implementation is unchanged. Mediator store/query/object/version/delegation normalization also passed.

11. **B2 preserved.** B2 remained PASS for this bounded feasibility recheck, including B2PrivilegeSeparationWhileInferenceWorks.test_discriminating_external_local_ipc_sentinel_is_unreachable. The test attempted local IPC inside the observer while inference and MCP worked; it was not skipped. Provider-managed retry and runtime-steering fail-closed checks, descriptor-bound inference transport, and launcher-started-instance authorization also passed.

12. **B3 preserved.** B3 remained PASS for exact-build discovery closure. Exact-build inventory and hostile ancestor-directory, project, HOME, dotenv, and prompt/configuration discovery/state cases passed. Repository discovery residue remains cleaned; the repair adds no discovery state. Immutable control/package/configuration and tamper checks, plus shared control-path protections, also passed.

13. **T1/T7/T8 observability.** Existing assembled instrumentation records explicit logical-root selection only after a successful read and model consumption, and exact consumed resource bytes; RootSelectionAndConsumedResources cases passed. This establishes observability behavior in this local stand-in profile only. No T1/T7/T8 burden comparison, exact-profile operator probe, or qualification claim was run or authorized; claims requiring such evidence remain unqualified/claim-scoped inadmissible.

14. **Exact-head suite and compile/static checks.** On implementation commit 3811104a876b0510c1839a1260e5c86c5e7fa093, with outer sandbox permission enabled for local AF_UNIX/AF_INET provider probes:

        python3 -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -v
        Ran 231 tests in 524.617s — OK; 0 skipped.

    The added launch tests both ran and passed. On the same implementation commit, python3 -m compileall -q qualification/ssdp70/eval passed, and git diff --check passed with no output.

15. **Skipped or unavailable required checks.** None. The exact full suite, compileall, and diff check all completed; no required check was skipped or unavailable. The outer sandbox denied local provider socket setup without elevated execution, so the requested suite was run with approved elevated execution. No admission or downstream qualification work was performed, as explicitly bounded by the task.

16. **Claude/shared regression.** Passed in the same 231-test command, including test_portable70.ClaudeAdapterTests, test_control_path_policy, test_harness_integration, test_mcp_stdio, test_stage_f_integrity_repairs, and test_stage_f_v4_repairs. No Claude adapter or shared normalized-event behavior was changed.

17. **D3 reopen condition.** None occurred. The accepted three-principal topology, supervisor-owned MCP bridge, trusted provider-control observer, and subject executor remain intact. The helper introduces no principal, provider proxy, mediator ownership, credential custody, daemon, or additional subject-facing edge.

18. **Unresolved risks.** OMP remains UNADMITTED. Evidence uses the declared frozen local provider stand-in and does not establish behavior with an external provider, exact-profile operator qualification, or Protocol 7 qualification subjects. The stress test covers three assembled launches with four active supervisor threads under the required outer watchdog; it is bounded evidence, not an exhaustive scheduler/race proof. The 90-second overall stress bound is independent of the 120-second per-episode timeout. Fresh independent D4 review remains required before any runner-admission decision.

## Project-memory applicability

The active workplan binds `accepted_project_state=23e46543c174a8451bbadc402df63538105eab10`, the PEM at that state, and `candidate_overlay_semantic_candidate=NONE`. Per repository policy, `main` is the integrated publication line; its current integrated state is `2585b73f00420daca185a4fbb9ac42a79473eda1`, and the HEAD PEM bytes match that current main copy. Current/base schema and publication checks passed. The attempted overlay composition check against the active workplan's older exact binding did not validate: the current root PEM metadata is not explicitly based on that workflow-selected accepted publication. This is recorded as a PEM binding discrepancy, not resolved by silently rebinding the active workplan; it did not change the single-defect process-launch decision. No PEM was edited, and the discrepancy does not establish absence of other historical lessons.

Task-local Historical Applicability Set:

- **DS-001 — APPLICABLE.** Keep decisive acceptance on the assembled real owner path; this repair's launch proof is exercised through `harness70.run_episode`, not a synthetic-only observer test. Repository-green evidence is not OMP admission.
- **PC-001 — APPLICABLE.** Preserve historical/frozen protocol profiles and qualification evidence; none were changed to accommodate OMP.
- Other surfaced memory families did not materially alter this process-creation decision. The validated-memory scope limitation above remains recorded.
