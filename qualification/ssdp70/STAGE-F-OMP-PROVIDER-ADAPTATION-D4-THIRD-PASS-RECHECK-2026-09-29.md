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

1. **Implementation identity.** Commit `3811104a876b0510c1839a1260e5c86c5e7fa093`, parent `758ba1755938e663b0e07a1921998eca8aababf4`, on `ssdp-7.0-scientific-epistemic-closure`. The exact requested starting head was verified before editing; there were no intervening commits. The full regression below ran on this implementation commit.

2. **No production `preexec_fn`.** `test_omp_units.ObserverLaunchSafety.test_real_omp_launch_path_has_no_preexec_fn_and_binds_exec_helper` checks the production adapter source, traverses locally reachable functions from `launch`, and checks the actual Popen call is passed the helper argv with `pass_fds` and `close_fds`. It also checks the helper is included in digest-bound support and performs the reviewed FD-copy/exec operations. No production OMP observer path contains or invokes `preexec_fn`.

3. **Exact FD inheritance and sentinel.** `test_omp_integration.ThirdPassObserverLaunchSafety.test_real_observer_fd_map_excludes_inheritable_supervisor_sentinel` opens an unrelated inheritable supervisor sentinel at FD 256 or above, then runs the real assembled path. It verifies the exact 3/4/5/6 channel map, Bubblewrap argument FD 7, exact five-entry `pass_fds`, successful inference and MCP, and a denied observer read through the sentinel's `/proc/self/fd` path. It also verifies the helper digest is present in run identity and that observer evidence closes with boundary, post-lockdown credential receipt, readiness, request, and response records.

4. **Multithreaded assembled launch and outer watchdog.** `test_omp_integration.ThirdPassObserverLaunchSafety.test_repeated_launches_with_active_threads_have_an_outer_watchdog` runs three complete `harness70.run_episode → adapters.omp → helper → Bubblewrap → frozen OMP 18.0.11 → local provider stand-in → supervisor MCP bridge/mediator → evidence normalization` episodes while four unrelated supervisor threads actively churn. All three reached `COMPLETE_ADMISSIBLE`, performed provider inference and a normalized MCP operation, and produced a valid observer chain in the order boundary → credential receipt → ready → request/response. The parent worker is supervised by an independent 90-second watchdog while each episode has its normal 120-second timeout; a construction hang therefore fails the test before normal episode timeout ownership. All three completed within the outer bound.

5. **Observer privilege separation preserved.** The full suite passed the assembled hostile probes for Bubblewrap filesystem, user, PID, IPC, cgroup, and private-network isolation; capability drop, no-new-privileges, and observer seccomp; credential-after-lockdown; connected provider route success and unrelated-egress denial; host HOME, custody, supervisor, mediator, and evidence-state denial; Bash inference/MCP denial and second-OMP relay denial; minimal runtime dependencies with omitted host software; and the positive local-IPC denial probe. No boundary, seccomp, capability, route, credential, or observer-evidence drain was removed or weakened.

6. **Second-pass B1 preserved.** B1 remained PASS for this bounded feasibility recheck. The full suite passed runtime-derived catalog, native-tool, MCP, and configuration evidence; exact native-tool-surface and raw-to-normalized completeness checks; request/response binding; mutation, omission, duplicate, truncation, and reordering failures; categorical >4 MiB observer-response truncation rejection; and successful-read plus actual-model-consumption root/resource selection. The MCP bridge remains supervisor-owned and the mediator implementation is unchanged.

7. **Second-pass B2 preserved.** B2 remained PASS for this bounded feasibility recheck. The assembled privilege/route/credential and hostile-probe checks above passed, including `B2PrivilegeSeparationWhileInferenceWorks.test_discriminating_external_local_ipc_sentinel_is_unreachable`. The test attempted local IPC inside the observer while inference and MCP worked; it was not skipped. No new principal or communication edge was required.

8. **Second-pass B3 preserved.** B3 remained PASS for exact-build discovery closure. The full suite passed exact-build inventory and hostile discovery/state cases, including ancestor-directory, project, HOME, dotenv, and prompt/configuration sources. Repository discovery residue remains cleaned; the repair adds no discovery state.

9. **Other preserved mechanisms.** The same exact-commit run passed provider-managed retry and runtime-steering fail-closed checks; mediator store/query/object/version/delegation normalization; descriptor-bound inference transport; launcher-started-instance authorization; unchanged native surface; immutable control/package/configuration and tamper checks; and shared control-path protections. No new executable evidence contradicted these second-pass mechanisms.

10. **T1/T7/T8 observability.** The existing assembled instrumentation still records explicit logical-root selection only after a successful read and model consumption, and exact consumed resource bytes; `RootSelectionAndConsumedResources` cases passed. This establishes observability behavior in this local stand-in profile only. No T1/T7/T8 burden comparison, exact-profile operator probe, or qualification claim was run or authorized; claims requiring such evidence remain unqualified/claim-scoped inadmissible.

11. **Exact-head full suite.** On implementation commit `3811104a876b0510c1839a1260e5c86c5e7fa093`, with outer sandbox permission enabled for the local AF_UNIX/AF_INET provider probes:

        python3 -m unittest discover -s qualification/ssdp70/eval -p 'test_*.py' -v
        Ran 231 tests in 524.617s — OK; 0 skipped.

    The added launch tests both ran and passed. The suite included the shared Claude adapter and Stage F regressions. The outer sandbox otherwise denied local provider socket setup, so the requested suite was run with approved elevated execution; no required test was skipped or unavailable.

12. **Compile/static checks.** On the same implementation commit, `python3 -m compileall -q qualification/ssdp70/eval` passed, and `git diff --check` passed with no output. The working tree was clean after the implementation commit and these checks.

13. **Claude/shared regression.** Passed in the same 231-test command, including `test_portable70.ClaudeAdapterTests`, `test_control_path_policy`, `test_harness_integration`, `test_mcp_stdio`, `test_stage_f_integrity_repairs`, and `test_stage_f_v4_repairs`. No Claude adapter or shared normalized-event behavior was changed.

14. **D3 reopen condition.** None occurred. The accepted three-principal topology, supervisor-owned MCP bridge, trusted provider-control observer, and subject executor remain intact. The helper is transient supervisor launch machinery, introduces no principal, provider proxy, mediator ownership, credential custody, daemon, or additional subject-facing edge.

15. **Required checks skipped or unavailable.** None. The exact full suite, compileall, and diff check all completed successfully. No admission or downstream qualification work was performed, as explicitly bounded by the task.

16. **Unresolved risks and limits.** OMP remains UNADMITTED. The evidence uses the declared frozen local provider stand-in and does not establish behavior with an external provider, exact-profile operator qualification, or Protocol 7 qualification subjects. The stress test covers three assembled launches with four active supervisor threads under the required outer watchdog; it is bounded evidence, not an exhaustive scheduler/race proof. The 90-second overall stress bound is intentionally independent of the 120-second per-episode timeout. Fresh independent D4 review remains required before any runner-admission decision.

## Project-memory applicability

The active workplan binds `accepted_project_state=23e46543c174a8451bbadc402df63538105eab10`, the PEM at that state, and `candidate_overlay_semantic_candidate=NONE`. Per repository policy, `main` is the integrated publication line; its current integrated state is `2585b73f00420daca185a4fbb9ac42a79473eda1`, and the HEAD PEM bytes match that current main copy. Current/base schema and publication checks passed. The attempted overlay composition check against the active workplan's older exact binding did not validate: the current root PEM metadata is not explicitly based on that workflow-selected accepted publication. This is recorded as a PEM binding discrepancy, not resolved by silently rebinding the active workplan; it did not change the single-defect process-launch decision. No PEM was edited, and the discrepancy does not establish absence of other historical lessons.

Task-local Historical Applicability Set:

- **DS-001 — APPLICABLE.** Keep decisive acceptance on the assembled real owner path; this repair's launch proof is exercised through `harness70.run_episode`, not a synthetic-only observer test. Repository-green evidence is not OMP admission.
- **PC-001 — APPLICABLE.** Preserve historical/frozen protocol profiles and qualification evidence; none were changed to accommodate OMP.
- Other surfaced memory families did not materially alter this process-creation decision. The validated-memory scope limitation above remains recorded.
