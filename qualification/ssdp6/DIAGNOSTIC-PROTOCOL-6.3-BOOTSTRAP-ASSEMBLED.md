---
kind: protocol-6.3-bootstrap-assembled-diagnostic
bootstrap: 1484c1d3caa49d87cc15bc52a5e775399c1dae1b
authority: non-normative-observation-evidence
---

# Protocol 6.3 bootstrap assembled gate diagnostic

- repository unittest discovery: 0
- temporary dist build: 0
- standalone package validation: 0
- committed dist parity: 0
- generated snapshot parity: 0
- Orchestrator Core: 1
- whitespace diff check: 0

## core-tests failure tail

```text
running 12 test modules across 2 workers
    ok  tests.test_config_and_projects                     28 tests    0.6s
    ok  tests.test_extension_composition                   30 tests    1.4s
    ok  tests.test_git_observation                         44 tests    1.6s
    ok  tests.test_input_binding                           31 tests    2.1s
    ok  tests.test_installed_product                       32 tests   35.9s
  FAIL  tests.test_layout_and_fitness                      21 tests    0.2s
    ok  tests.test_privacy_and_remote_truth                31 tests    3.5s
    ok  tests.test_protocol_source_and_profile             37 tests    0.8s
    ok  tests.test_public_api_seam                         31 tests    1.7s
    ok  tests.test_render_and_identity                     35 tests    3.0s
    ok  tests.test_ssdp6_profiles                          30 tests    0.3s
    ok  tests.test_workplan_resolution                     40 tests    0.9s

======================================================================
tests.test_layout_and_fitness
======================================================================
test_core_declares_exactly_one_extension_entry_point_group (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_declares_exactly_one_extension_entry_point_group)
One group constant, and one place that reads entry points from it. ... ok
test_core_defines_no_higher_module_command (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_defines_no_higher_module_command) ... ok
test_core_imports_no_forbidden_machinery (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_imports_no_forbidden_machinery) ... ok
test_core_imports_no_higher_module (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_imports_no_higher_module) ... ok
test_core_introduces_no_persistence (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_introduces_no_persistence) ... ok
test_core_remote_source_reads_do_not_fetch_repository_mirrors (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_core_remote_source_reads_do_not_fetch_repository_mirrors)
Bounded archive reads avoid materializing an unrelated mirror. ... ok
test_no_higher_module_placeholders_remain (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_no_higher_module_placeholders_remain)
Guard against speculative Adapter/Scheduler scaffolding inside Core. ... ok
test_public_surfaces_import_only_within_core (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_public_surfaces_import_only_within_core) ... ok
test_target_observer_uses_no_mutating_git_subcommand (tests.test_layout_and_fitness.ArchitectureFitnessTests.test_target_observer_uses_no_mutating_git_subcommand)
The single module that touches target repositories stays read-only. ... ok
test_every_orchestrator_python_file_lives_under_the_containment_root (tests.test_layout_and_fitness.ContainmentTests.test_every_orchestrator_python_file_lives_under_the_containment_root) ... FAIL
test_legacy_core_tree_and_private_module_paths_are_absent (tests.test_layout_and_fitness.ContainmentTests.test_legacy_core_tree_and_private_module_paths_are_absent) ... ok
test_no_orchestrator_package_exists_outside_the_containment_root (tests.test_layout_and_fitness.ContainmentTests.test_no_orchestrator_package_exists_outside_the_containment_root) ... ok
test_protocol_workplans_remain_under_the_repository_convention (tests.test_layout_and_fitness.ContainmentTests.test_protocol_workplans_remain_under_the_repository_convention) ... ok
test_repository_ci_only_invokes_orchestrator_commands (tests.test_layout_and_fitness.ContainmentTests.test_repository_ci_only_invokes_orchestrator_commands)
CI may call into ``orchestrator/``; it must not host orchestrator logic. ... ok
test_sibling_repository_trees_do_not_import_orchestrator_code (tests.test_layout_and_fitness.ContainmentTests.test_sibling_repository_trees_do_not_import_orchestrator_code) ... ok
test_clipboard_is_an_optional_extra (tests.test_layout_and_fitness.NamespaceTests.test_clipboard_is_an_optional_extra) ... ok
test_declared_runtime_dependencies_are_the_justified_set (tests.test_layout_and_fitness.NamespaceTests.test_declared_runtime_dependencies_are_the_justified_set) ... ok
test_exactly_one_console_entry_point (tests.test_layout_and_fitness.NamespaceTests.test_exactly_one_console_entry_point) ... ok
test_no_distribution_owns_the_root_namespace_init (tests.test_layout_and_fitness.NamespaceTests.test_no_distribution_owns_the_root_namespace_init) ... ok
test_packaging_declares_native_namespaces (tests.test_layout_and_fitness.NamespaceTests.test_packaging_declares_native_namespaces) ... ok
test_runtime_floor_is_python_311 (tests.test_layout_and_fitness.NamespaceTests.test_runtime_floor_is_python_311) ... ok

======================================================================
FAIL: test_every_orchestrator_python_file_lives_under_the_containment_root (tests.test_layout_and_fitness.ContainmentTests.test_every_orchestrator_python_file_lives_under_the_containment_root)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/scientific-software-development-protocol/scientific-software-development-protocol/orchestrator/tests/test_layout_and_fitness.py", line 103, in test_every_orchestrator_python_file_lives_under_the_containment_root
    self.fail(f"unexpected top-level Python file outside the containment boundary: {path}")
AssertionError: unexpected top-level Python file outside the containment boundary: .github/scripts/publish_ssdp63_bootstrap.py

----------------------------------------------------------------------
Ran 21 tests in 0.170s

FAILED (failures=1)


390 tests across 12 modules in 38.1s -- FAILED: tests.test_layout_and_fitness
```
