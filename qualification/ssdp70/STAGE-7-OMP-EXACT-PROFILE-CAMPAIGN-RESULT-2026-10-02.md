# OMP Stage 7 Exact-Profile Campaign Result — 2026-10-02

## Scope and outcome

This record retains candidate runner-admission evidence only. No semantic/evaluator proof cell was independently judged, no admission status was promoted, and no Protocol 7 qualification subject was executed.

- Governing SSDP: 6.6.0.
- Executable candidate commit: `1715a8f0ddd6360d68c54afd650f32b037bcc2de` (tightened `completedAt` transcript-equality normalization and provenance repair).
- Provenance ancestry:
  - Initial report introduction: `855f57f69a7399396d962da7a34357bb6a28b609` (repaired from nonexistent SHA `855f57f5c531d04467ecb5eeaeaeec3f4d6d67b2`)
  - Intermediate provenance amendment: `ff940833e2dcd3d6067f2d49c2e9d5c711b46d86`
  - Exact-profile campaign record: `e29fc4cd0dcfa73f17647aa05d407c94679e6c5b`
  - Final D4 repair implementation commit: `1715a8f0ddd6360d68c54afd650f32b037bcc2de`
- Immutable Protocol 7 semantic subject: `db94a2dfb7fef480f37227eab5c45256e89901b8`.
- Evidence-only branch checkout: `ssdp-7.0-scientific-epistemic-closure`.
- Frozen campaign root: `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/`

## Frozen profile and preparation identities

The exact profile remained the frozen replacement profile throughout execution:

- Profile ID: `omp-headless-deepinfra-glm53-flash-stage7-exacttranscript-1715a8f0ddd6360d68c54afd650f32b037bcc2de`
- Profile key SHA-256: `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`
- Profile document SHA-256: `ca44d543cc292ae3e40872459f23c39c6c8fdd9bf43fd376c4e4dfbd40bcb223`
- Capability snapshot SHA-256: `1c0f3ce0ec625c8c6609c36a746c631f08e81d6dc2a02d00f29bda03cbb416bd`
- Capability identity: `f01ec2b6bda9c30ffb9495029cce8481ab762a62a0f1c3d9452c17a3d0ca0e55`
- Runtime dependency manifest SHA-256: `5114fe69e08c17470d4b19d7d3d1d20ad755ec20965151dc04afaf2b8c247216`
- Runtime closure identity: `6c49a21528ae33c2f8dfee60995448b3d7af795a4b2b826c164f87699d4d8499`
- Adapter (`adapters/omp.py`) SHA-256: `9ede18e4b69a1734637f77e3a99aec697fa5ab2c15772c5304defd1b3a192107`
- Subject Launcher (`subject_launcher.py`) SHA-256: `e6a1c1487c0617908e73db887901b2a850ae2a5ee1b172cc0f7bf55d0936061d`
- Build Inventory (`omp-build-inventory-18.0.11.json`) SHA-256: `a770317cced12600ab8e3604a24af226ebc4c329b3043b2acb98662ec77fd428`
- Provider route: DeepInfra, `zai-org/GLM-5.3-Flash`, `https://api.deepinfra.com/v1/openai`, reasoning high, OMP 18.0.11.

The arms manifest is `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/arms.json` (SHA-256 `02b74a0179115458a4a14dd3f53b8483762bd67485e01e5434d77f19d2e1317c`). It contains:

| Arm | Immutable commit | Version | Materialized dist/skills tree SHA-256 |
|---|---|---|---|
| p66 | `22f4bdba53795da3a6f13f162529f3a843fc37ae` | 6.6.0 | `e6d960a866fb794382fa5fdaa3e351681d292803dd035e5d4786a981a2a1e083` |
| p70 | `db94a2dfb7fef480f37227eab5c45256e89901b8` | 7.0.0 | `7ec95162d5888e1ace9030494f48cba80d24dc4b081c91b426dc7421d929bb8b` |

The synthetic campaign manifest is `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/synthetic-corpus-manifest.json` (SHA-256 `c118e218dd50767f9860aadd689c6790e2e03ac8e03f921510c994ecb3cd0a75`). Its corpus, requirements, and oracle tree identities are:

- Corpus: `6237fe3ccc1238a1c1ee808fa0c2784b8bd9dd6a2e6845e4475583fd48369539`
- Requirements: `d15f38856f30433b8497ac504a5f01e44e5d920bd71d14f5f529a7217fdf3326`
- Oracles: `2f1ca81af89de6a32428bba6f3a2c7d26db1db913e19c2d9abcd30f303e31438`

The 12 ordinary-entry classes map to these episode IDs:

| Case class | Episode |
|---|---|
| `d4_code_work` | `S7-ORD-D4` |
| `run_and_report` | `S7-ORD-RUN-REPORT` |
| `ad_hoc_analysis` | `S7-ORD-ADHOC` |
| `realized_results_review` | `S7-ORD-REVIEW` |
| `human_gate_evidence` | `S7-ORD-GATE` |
| `near_boundary_empty_admissible_set` | `S7-ORD-NEG-EMPTY` |
| `near_boundary_technical_outside_predicate` | `S7-ORD-NEG-TECH` |
| `authority_authoring_or_review` | `S7-ORD-AUTHORITY` |
| `claim_and_variant_history` | `S7-ORD-VARIANT` |
| `source_to_rendered_integrity` | `S7-ORD-RENDERED` |
| `delegate_return` | `S7-ORD-DELEGATE` |
| `tension_retrieval` | `S7-ORD-TENSION` |

## Fresh real-provider probe

Before launching the campaign matrix, a fresh real-provider probe was executed:

- **Probe Root:** `/home/samjin/ssdp70-omp-stagef/probes/OMP-STAGE7-REAL-PROVIDER-EXACTTRANSCRIPT-20261002T173438.919918Z-1715a8f0ddd6`
- **Run Identity SHA-256:** `af2123dd376abda119f6758fb7ded35feb42000f4c042c160e01449556813040`
- **Results:**
  - `execution_ok`: `true`
  - `evidence_state`: `COMPLETE_ADMISSIBLE`
  - `qualification_outcome`: `NOT_EVALUATED`
  - `complete_run_validation_error_count`: 0
  - `integrity_error_count`: 0
  - Credential scan: 49 files (3,452,912 bytes) with 0 matches.
- Probe reference linked into campaign root: `probe-reference.json` (SHA-256 `072b66bdd338d957ef91ccac94c525e92fa6ae74cfad455c2540843091e8baa4`).

## Exact-profile execution

The positive exact-profile campaign matrix ran at:

`/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/runs/exact-profile-20261002T173534.016451Z-0bc749208a/`

Its `execution-summary.json` records:

| Field | Result |
|---|---|
| `status` | `PASS` |
| `positive_matrix_returncode` | 0 |
| `contamination_returncode` | 2 |
| `contamination_expected_prelaunch_refusal` | `true` |
| `structural_validation_errors` | `[]` |
| `scheduler_validation_errors` | `[]` |
| `arms` / `parallel` | `p66` and `p70` / 2 |

All 34 positive realizations reached `COMPLETE_ADMISSIBLE`: 17 `p66` and 17 `p70`. The 35th realization is the expected contamination refusal. Every positive run passed complete-run integrity validation; no normalized-event or normalization-completeness error was recorded.

The hostile realization is `contamination/S7-CONTAMINATION-p70-r0/`. Its retained `prelaunch-refusal.json` records `phase=realize_containment` and `subject_launched=false`. The refusal was raised because ambient project-local `.mcp.json` discovery was detected and closed.

The scheduler retained 17 complete pair intervals and all 34 arm intervals. Each pair ran its two arms sequentially in the recorded order. The scheduler reported zero validation errors. Monotonic intervals contain 16 pairwise overlap edges involving all 17 pairs, with maximum simultaneous pair count 2. All 34 positive realizations have distinct nonempty `private_root` values; zero cross-pair collisions occurred.

## Retained p70 semantic-subject run identities

Each row is a positive exact-profile p70 realization with subject commit `db94a2dfb7fef480f37227eab5c45256e89901b8`, profile key `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`, and `evidence_state=COMPLETE_ADMISSIBLE`:

| Episode | Run identity SHA-256 |
|---|---|
| `S7-CONTAINMENT` | `c0e4f0965b39a049c711f7f20b93f4fab641bd1b4d9e9ee06fe2abe00bb17bf5` |
| `S7-MEDIATED` | `556350931c96e026558d33cab3f186abb4d98f32e82864eefd8fff557f37dcb6` |
| `S7-ORD-ADHOC` | `0deff40d228ab0212cd7830c8fe9bd913223588a99ed5866c702c6f8fa210ebf` |
| `S7-ORD-AUTHORITY` | `680eb298f9392f5bb7b576591bc844f4da63b9820492728bf9fc1d713f789fa4` |
| `S7-ORD-D4` | `1191b999fdc73c548e85ae75824682d0845630cf3bdfacfebfe696a239aff1c2` |
| `S7-ORD-DELEGATE` | `6ed1def5d0774cb3d79a234f9584fe503b84105d7721b82d5396102c02332690` |
| `S7-ORD-GATE` | `abce20fb70f1eb3118dd143f4570ee3baeed1e8c324ad99e93db8897b266c020` |
| `S7-ORD-NEG-EMPTY` | `0628348430132c4158e2bd6a0b7940fac6127cebbdb67d3f6184d7b8830f83c4` |
| `S7-ORD-NEG-TECH` | `2838489be3540e503d304098fd5bfd0f8bdb8a2e3e551814fbc80a0fb8a8cac5` |
| `S7-ORD-RENDERED` | `d6c9c2f2cd04886d7964d146be27ef01c87819b4b23c00fd3e6c4cfdd3829b9e` |
| `S7-ORD-REVIEW` | `6a3d791bd7f2cd7de2603388190eeba69efb98e07bbf533e75874e661fb74785` |
| `S7-ORD-RUN-REPORT` | `e390815eba53351c6c67a6ea9d66ae11520a7e4711e4af7b4f33a3bb495835ad` |
| `S7-ORD-TENSION` | `12a994981348f12dff8de5911086dcdaf5debd34987cac06ac5da4f42c25b3df` |
| `S7-ORD-VARIANT` | `39eadb1fbf45544c0ddefc8c7cb827e60084d673e76d4d62fea2666ec6bd7324` |
| `S7-PAIR` | `577671ca9979f80325f70e3ecfef53e69ee9c1ecebf6ccf086bd72e9d4a40001` |
| `S7-PAIR-r1` | `b6179ca1603527aa1c482c036d3cac88e595075a3dcc0a004497df075ff78eab` |
| `S7-WORKSPACE` | `83c3ad2c70ca0d9935e1642b91a9c7bba7ba0229dc789b7e444f04df5de58830` |

## Retained p66 comparison-arm run identities

Each row is a positive exact-profile p66 realization with arm commit `22f4bdba53795da3a6f13f162529f3a843fc37ae`, profile key `68d440fd6f8e8441ac35b0cab584e2d6c8be043661d14fd78d2965cc1282f6d8`, and `evidence_state=COMPLETE_ADMISSIBLE`:

| Episode | Run identity SHA-256 |
|---|---|
| `S7-CONTAINMENT` | `9882bd2feb4d1053014a09357065616c00a58022e33a664655b75d09b99c6a4b` |
| `S7-MEDIATED` | `1e1d4ee3825bd11cdc43b53bf5f9379833e9b1f9a4689a16efaa6cd21f8a2d42` |
| `S7-ORD-ADHOC` | `63a0f4c48fe2eb17a8acfb59794b4e21b7d7268e3c187cce6c7027f5efbec333` |
| `S7-ORD-AUTHORITY` | `089383ceaf47c08316086983e303810bc65b25bd2b7f3e02a705a010acdb4650` |
| `S7-ORD-D4` | `cdce2cf960a497ef0f56512c4c8fd876b8a0355dda14ede1ff86160d8936999e` |
| `S7-ORD-DELEGATE` | `f77d6a47ab059ce2840083bde7b49ddf1f22dd4acdd53e5b2cc57d691786b649` |
| `S7-ORD-GATE` | `16933fded2273cfd10e521fa1f4c5de9ea1dec8c02f0d7f9dd7f2ca2085c3287` |
| `S7-ORD-NEG-EMPTY` | `21c7716f265458bf86313920f291cfdf40ffcd5950dd2de444f4299695c3f7eb` |
| `S7-ORD-NEG-TECH` | `d87b4123c2a441d9a13eb9df4e8b3f22e97cd0d840b8f00bed1c44f5095015e2` |
| `S7-ORD-RENDERED` | `7b3be02a46056475058dff7cf52612f877c216a3916965b0ea7b496d7904cd86` |
| `S7-ORD-REVIEW` | `28cf84f22889294c620713cecc16952b7a0601580c9af0612af7b4b65df1678a` |
| `S7-ORD-RUN-REPORT` | `8d99187601c6ac7a05d2fca4e5a316ea1da58b5deac57154e7b6043720b323a1` |
| `S7-ORD-TENSION` | `000eb94784a49d7681217bd7de21ad56fe7c54feacba5a75abcf3eeccf52db7c` |
| `S7-ORD-VARIANT` | `8c56d78ff4b1c29c89248c1400c1e2db11036382408b20ec68b85a7077d7094e` |
| `S7-PAIR` | `f43e700e65c9bdeb434cc087471715208a3fb8e703964b81e0499e3c80624c73` |
| `S7-PAIR-r1` | `6c5762c3d0ff9a1a37611d2a6db3c20f536470a61172374dbb0552552a72c60d` |
| `S7-WORKSPACE` | `3633488a86cfad723a623e35c1a8421553454ea01c0fe9d4237043fd06f0f5d5` |

## Normalized discriminator review

The qualification tooling validated all 35 exact-profile realizations with zero integrity errors. For every positive run, native-event count equals normalization-map row count; zero unclassified native rows, zero oracle-relevant unmapped rows, and zero normalized-event or completeness errors occurred.

Under the repaired exact-transcript profile, corresponding `message_end` and `agent_end.messages` records match in exact canonical structural dictionary equality across all keys and values, with disciplined normalization of only the ephemeral dispatch timestamp `completedAt` on `message_end` assistant messages strictly typed to positive integers (`type(val) is int and val > 0`).

## Deterministic Stage 7 falsification

The production falsifier ran against the complete p70 base realization:

- **Base run:** `positive-matrix/S7-ORD-D4-p70-r0/`
- **Base identity SHA-256:** `1191b999fdc73c548e85ae75824682d0845630cf3bdfacfebfe696a239aff1c2`
- **Falsification root:** `/home/samjin/ssdp70-omp-stagef/admission/OMP-STAGE7-20261002T173352Z-68d440fd6f8e-exacttranscript/falsification/core-20261002T180249.960008Z-6ffc263b74/`
- **Result:** `deterministic-falsification.json` reports `status="PASS"` across all 11 perturbation/rejection cases.

| Mechanically falsified branch | Retained result |
|---|---|
| Missing artifact | Rejected: `final-report.md` missing and its integrity entry unavailable. |
| Missing oracle | Rejected: `synthetic-final-report` unexecuted/corrupt and its output unavailable. |
| Missing scoring disposition | Rejected: synthetic-coverage disposition missing. |
| Duplicate scoring disposition | Rejected: duplicate synthetic-coverage disposition. |
| Unknown scoring disposition | Rejected: unknown item ID and required item missing. |
| Missing termination | `MISSING_REQUIRED_EVIDENCE`; reason notes termination event is missing. |
| Profile identity perturbation | Rejected: stored run identity no longer matches. |
| Core identity perturbation | Rejected: stored identity, summary identity, and normalized event run IDs no longer match. |
| Cache profile identity perturbation | `cache_valid=false`. |
| Cache core identity perturbation | `cache_valid=false`. |
| Direct failed terminal | Rejected: `execution_ok=false` fails closed with `EXECUTION_ERROR`. |

## Executor-admission check coverage

| Check | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `exact_subject_profile_identity` | `exact-profile-behavior` | **PASS** | `proofs/check-exact_subject_profile_identity-20261002T180302.463016Z-5218798d.json` |
| `fresh_arm_isolation` | `exact-profile-behavior` | **PASS** | `proofs/check-fresh_arm_isolation-20261002T180303.063702Z-f9be76e1.json` |
| `capability_manifest` | `exact-profile-behavior` | **PASS** | `proofs/check-capability_manifest-20261002T180303.658650Z-90e68487.json` |
| `raw_normalized_completeness` | `exact-profile-behavior` | **PASS** | `proofs/check-raw_normalized_completeness-20261002T180304.254781Z-6e85aa64.json` |
| `fail_closed_evidence` | `deterministic-falsification` | **PASS** | `proofs/check-fail_closed_evidence-20261002T180304.264929Z-c7bf183e.json` |
| `exact_scoring_closure` | `deterministic-falsification` | **PASS** | `proofs/check-exact_scoring_closure-20261002T180304.273945Z-1b7b123a.json` |
| `cache_profile_core_identity_perturbation` | `deterministic-falsification` | **PASS** | `proofs/check-cache_profile_core_identity_perturbation-20261002T180304.282882Z-6737db25.json` |
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/check-catalog_contamination-20261002T180304.881559Z-a815be1e.json` |
| `containment_pre_effect` | `exact-profile-behavior` | **PASS** | `proofs/check-containment_pre_effect-20261002T180305.483558Z-620d4ef7.json` |
| `custody_denial` | `exact-profile-behavior` | **PASS** | `proofs/check-custody_denial-20261002T180306.080847Z-823ee863.json` |
| `ordinary_entry_owner_read` | `exact-profile-behavior` | **PASS** | `proofs/check-ordinary_entry_owner_read-20261002T180306.681030Z-4297010d.json` |
| `withheld_oracle_branches` | `independent-inspection` | **PENDING** | *Requires independent evaluator judgment; not self-authorized.* |

## §6 matrix coverage

| Cell | Evidence Class | Status | Proof Artifact |
|---|---|---|---|
| `catalog_contamination` | `exact-profile-behavior` | **PASS** | `proofs/section6-catalog_contamination-20261002T180307.282112Z-95ec211f.json` |
| `containment_escape_attempts_retained` | `exact-profile-behavior` | **PASS** | `proofs/section6-containment_escape_attempts_retained-20261002T180307.876637Z-15c0e3e1.json` |
| `ordinary_entry_case_classes` | `exact-profile-behavior` | **PASS** | `proofs/section6-ordinary_entry_case_classes-20261002T180308.482072Z-0bd18665.json` |
| `issue_network_external_write_standins` | `exact-profile-behavior` | **PASS** | `proofs/section6-issue_network_external_write_standins-20261002T180309.084561Z-58d04782.json` |
| `reject_missing_artifact` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_artifact-20261002T180309.097017Z-89b4e59f.json` |
| `reject_missing_oracle` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_oracle-20261002T180309.108947Z-67089898.json` |
| `reject_missing_scoring_disposition` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_missing_scoring_disposition-20261002T180309.118405Z-e87c8987.json` |
| `reject_incomplete_or_failed_termination` | `deterministic-falsification` | **PASS** | `proofs/section6-reject_incomplete_or_failed_termination-20261002T180309.128700Z-f25da3ed.json` |
| `perturb_cache_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_cache_identity-20261002T180309.138226Z-1933f4a3.json` |
| `perturb_profile_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_profile_identity-20261002T180309.147822Z-adb9113a.json` |
| `perturb_core_identity` | `deterministic-falsification` | **PASS** | `proofs/section6-perturb_core_identity-20261002T180309.158354Z-6560cd4e.json` |
| `known_broken_both_arms_miss` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_binding_o3` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_wrong_null_variant_delegate` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_false_tension_closure_asserter` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_loss_before_destructive_boundary` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_unauthorized_write` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_broken_version_self_adoption` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_legitimate_withholding` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `known_good_designed_termination` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `perturb_evaluator_identity` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `final_report_changed_files_tool_trace_assessment` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |
| `chained_delegate_first_look` | `independent-inspection` | **PENDING** | *Pending independent evaluator inspection.* |

## Integrity, credential, and disposition closure

Current qualification tooling returned zero exact-profile realization errors across the 34 positive runs and expected contamination refusal. Campaign-wide normalized completeness had zero unmapped or unclassified rows. Frozen profile, capability, host, runtime manifest, and runtime closure identities remained exact after execution.

The credential scan checked 2,281 files and 127,692,287 bytes across the entire campaign root using 14 encoding forms. It found zero leaks or secret matches. The fresh real-provider probe scan checked 49 files and 3,452,912 bytes with zero matches.

Runner admission disposition remains strictly **`CANDIDATE`**. Blinded Protocol 7 qualification subjects remain unexecuted until formal independent evaluator admission.
