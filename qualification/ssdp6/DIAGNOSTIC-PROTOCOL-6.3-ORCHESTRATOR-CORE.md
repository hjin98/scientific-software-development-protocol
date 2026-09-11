---
kind: protocol-6.3-orchestrator-core-diagnostic
candidate: 2bfcd14f339e4a58d307cfd5fc5a12770c37c65e
exit_status: 1
authority: non-normative-observation-evidence
---

# Protocol 6.3 Orchestrator Core diagnostic

Captured from the same Core acceptance runner used by ordinary CI. This is failure evidence, not acceptance.

```text
running 12 test modules across 2 workers
    ok  tests.test_config_and_projects                     28 tests    0.8s
    ok  tests.test_extension_composition                   30 tests    1.6s
    ok  tests.test_git_observation                         44 tests    1.6s
    ok  tests.test_input_binding                           31 tests    2.5s
    ok  tests.test_installed_product                       32 tests   34.7s
    ok  tests.test_layout_and_fitness                      21 tests    0.2s
    ok  tests.test_privacy_and_remote_truth                31 tests    3.6s
    ok  tests.test_protocol_source_and_profile             37 tests    0.8s
    ok  tests.test_public_api_seam                         31 tests    1.8s
    ok  tests.test_render_and_identity                     35 tests    3.1s
  FAIL  tests.test_ssdp6_profiles                          27 tests    0.3s
    ok  tests.test_workplan_resolution                     40 tests    1.0s

======================================================================
tests.test_ssdp6_profiles
======================================================================
test_legacy_alignment_retains_frozen_parent_input (tests.test_ssdp6_profiles.FrozenLegacyProfileTests.test_legacy_alignment_retains_frozen_parent_input) ... ok
test_legacy_definition_stays_schema_v1_with_nine_stages (tests.test_ssdp6_profiles.FrozenLegacyProfileTests.test_legacy_definition_stays_schema_v1_with_nine_stages) ... ok
test_legacy_packaged_bytes_keep_pre_transition_git_blob_identity (tests.test_ssdp6_profiles.FrozenLegacyProfileTests.test_legacy_packaged_bytes_keep_pre_transition_git_blob_identity) ... ok
test_legacy_profile_is_still_derived_from_legacy_prompts (tests.test_ssdp6_profiles.FrozenLegacyProfileTests.test_legacy_profile_is_still_derived_from_legacy_prompts) ... ok
test_protocol60_packaged_bytes_are_frozen (tests.test_ssdp6_profiles.FrozenProtocol60ProfileTests.test_protocol60_packaged_bytes_are_frozen) ... ok
test_protocol60_profile_is_still_derived_from_protocol60_prompts (tests.test_ssdp6_profiles.FrozenProtocol60ProfileTests.test_protocol60_profile_is_still_derived_from_protocol60_prompts) ... ok
test_protocol60_profile_stays_schema_v2_and_version_bound (tests.test_ssdp6_profiles.FrozenProtocol60ProfileTests.test_protocol60_profile_stays_schema_v2_and_version_bound) ... ok
test_protocol61_packaged_bytes_are_frozen (tests.test_ssdp6_profiles.FrozenProtocol61ProfileTests.test_protocol61_packaged_bytes_are_frozen) ... ok
test_protocol61_profile_is_still_derived_from_protocol61_prompts (tests.test_ssdp6_profiles.FrozenProtocol61ProfileTests.test_protocol61_profile_is_still_derived_from_protocol61_prompts) ... ok
test_protocol61_profile_stays_schema_v2_and_version_bound (tests.test_ssdp6_profiles.FrozenProtocol61ProfileTests.test_protocol61_profile_stays_schema_v2_and_version_bound) ... ok
test_alignment_pass_routes_by_downstream_domain_owner (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_alignment_pass_routes_by_downstream_domain_owner) ... ok
test_current_canonical_source_has_exact_domain_stage_set (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_current_canonical_source_has_exact_domain_stage_set) ... ok
test_current_profile_is_schema_v2_protocol_6 (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_current_profile_is_schema_v2_protocol_6) ... FAIL
test_current_profile_uses_protocol6_native_parent_authority_input (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_current_profile_uses_protocol6_native_parent_authority_input) ... ok
test_d3_only_authority_change_can_skip_unaffected_d4 (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_d3_only_authority_change_can_skip_unaffected_d4) ... ok
test_every_current_input_is_classified (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_every_current_input_is_classified) ... ok
test_every_transition_trigger_is_recognized (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_every_transition_trigger_is_recognized) ... ok
test_local_d4_is_plan_optional_but_review_remains_plan_governed (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_local_d4_is_plan_optional_but_review_remains_plan_governed) ... ok
test_material_authority_review_and_direct_handoffs_have_governing_plans (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_material_authority_review_and_direct_handoffs_have_governing_plans) ... ok
test_optional_d4_change_plan_must_be_current_active_authority (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_optional_d4_change_plan_must_be_current_active_authority) ... ok
test_profile_json_round_trips (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_profile_json_round_trips) ... ok
test_profile_version_mapping_is_unambiguous (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_profile_version_mapping_is_unambiguous) ... FAIL
test_reduced_routes_skip_unaffected_intermediate_domains (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_reduced_routes_skip_unaffected_intermediate_domains) ... ok
test_review_pass_can_continue_to_the_dependent_realization_domain (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_review_pass_can_continue_to_the_dependent_realization_domain) ... ok
test_risk_override_preserves_reduced_routes_and_provisional_state (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_risk_override_preserves_reduced_routes_and_provisional_state) ... ok
test_serious_challenge_stops_automatic_routing (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_serious_challenge_stops_automatic_routing) ... ok
test_task_is_not_re_requested_by_downstream_governed_stages (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_task_is_not_re_requested_by_downstream_governed_stages) ... ok

======================================================================
FAIL: test_current_profile_is_schema_v2_protocol_6 (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_current_profile_is_schema_v2_protocol_6)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/scientific-software-development-protocol/scientific-software-development-protocol/orchestrator/tests/test_ssdp6_profiles.py", line 28, in test_current_profile_is_schema_v2_protocol_6
    self.assertEqual(P.DEFAULT_PROFILE_ID, "ssdp-protocol-6.2")
AssertionError: 'ssdp-protocol-6.3' != 'ssdp-protocol-6.2'
- ssdp-protocol-6.3
?                 ^
+ ssdp-protocol-6.2
?                 ^


======================================================================
FAIL: test_profile_version_mapping_is_unambiguous (tests.test_ssdp6_profiles.SSDP6CanonicalProfileTests.test_profile_version_mapping_is_unambiguous)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/scientific-software-development-protocol/scientific-software-development-protocol/orchestrator/tests/test_ssdp6_profiles.py", line 48, in test_profile_version_mapping_is_unambiguous
    self.assertEqual(P.profile_id_for_version("6.2.0"), P.DEFAULT_PROFILE_ID)
AssertionError: 'ssdp-protocol-6.2' != 'ssdp-protocol-6.3'
- ssdp-protocol-6.2
?                 ^
+ ssdp-protocol-6.3
?                 ^


----------------------------------------------------------------------
Ran 27 tests in 0.077s

FAILED (failures=2)


387 tests across 12 modules in 37.0s -- FAILED: tests.test_ssdp6_profiles
```
