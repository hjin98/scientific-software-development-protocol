# Retired harness modules (skills-only 7.2, stage S2)

Governing SSDP version: 6.6.0. These modules were deleted from the working tree after the consolidated harness
(H1–H5, design §6) passed its acceptance; git keeps them. To read one, check it out at the commit shown:
`git show <commit>:qualification/ssdp70/eval/<module>`.

| Module | Lines | Last commit | Why retired | Replacement |
|---|---|---|---|---|
| `package_ledger.py` | 591 | `42ba802` | inotify package-access ledger: more provenance than the decision needed (design L7); its premise was UNRESOLVED on every development run | `package_bytes.py` (native reads plus a conservative full-file count for shell commands that name the package path) |
| `package_premise.py` | 197 | `c1e8150` | premise witness for the ledger | none (the ledger is gone) |
| `adapters/claude.py` | 1,700 | `100621f` | Claude CLI adapter; the gating executor is OMP (SD-R2) | none; non-OMP adapters are out of scope |
| `omp_stage7_admission.py` | 951 | `46ea4a0` | Stage 7 semantic-admission scaffolding for contract revision 16 | `h4.py` Precondition C and the hash pins of run identity |
| `omp_stage7_campaign.py` | 1,531 | `55f2a62` | Stage 7 campaign driver | `harness70.py matrix` and `qual-v2/h4.py` |
| `omp_inventory_probe.py` | 381 | `fb8df78` | produced `omp-build-inventory-18.0.11.json`, which stays as pinned data | the inventory file |
| `omp_rig.py` | 237 | `9de893a` | test rig | `test_rig.py` (test code, counted in the test budget) |
| `live_verify_v4.py` | 644 | `4462f0b` | Stage F v4 live verification | `test_relay_integration.py` |
| `v4_support.py` | 90 | `dc8f156` | Stage F v4 repair support | none |
| `run_rehearsal_matrix.py` | 445 | `6d09418` | executor rehearsal matrix for the ledger | none |
| `evaluator_admission.py` | 693 | `118da52` | evaluator admission records | `h4.py` Precondition C(b) and `assess70.py` identity pins |
| `requal71.py` | 791 | `04aed27` | 7.1 requalification gates, family and campaign manifests | `qual-v2/h4.py` |
| `batch_assess70.py` | 899 | `42ba802` | batch assessment and contract revision 16 scoring | `assess70.py` plus `qual-v2/h4.py` |

Retired tests: `test_package_ledger.py` (`42ba802`), `test_package_premise.py` (`c1e8150`), `test_omp_stage7_admission.py` (`d2feaa4`),
`test_omp_stage7_campaign.py` (`55f2a62`), `test_stage_f_v4_repairs.py` (`c0cce5a`), `test_requal71.py` (`04aed27`),
`test_batch_cli.py` (`42ba802`), `test_stage_f_integrity_repairs.py` (`23a1041`), `test_activation_accounting.py` (`42ba802`) (their coverage that still
applies lives in `test_relay_integration.py`, `test_harness_integration.py`, `test_portable70.py` and `test_omp_*`).

Also retired as data: the four `claude-*` execution-profile and capability documents under `profiles/` and `capabilities/`.

Moved, not edited: `qual-v2/operating_characteristics-R2-HISTORICAL.py` is now `../qual-v2-history/operating_characteristics-R2-HISTORICAL.py`
(a superseded script kept as history, outside the harness budget scope).

The `package-access` event kind, the profile-admission records and the `accounting_manifest` / family / campaign machinery were
removed from `core70.py`, `harness70.py` and `adapters/omp.py`; runs recorded before S2 (the 2026-10-06/07 development probe)
still carry them and are read by `qual-v2/h4.py legacy` only through their summaries, terminations and oracle items.
