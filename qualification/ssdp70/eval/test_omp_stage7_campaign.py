"""Focused unit tests for the OMP Stage 7 target-host campaign driver."""
import json
import sys
import tempfile
import unittest

import yaml
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import omp_stage7_admission as admission  # noqa: E402
import omp_stage7_campaign as driver  # noqa: E402


class Stage7CampaignDriverTests(unittest.TestCase):
    def _campaign(self, root: Path) -> Path:
        camp = root / "admission" / "campaign"
        camp.mkdir(parents=True)
        (camp / "proofs").mkdir()
        value = {
            "schema": admission.SCHEMA,
            "kind": admission.KIND,
            "state": "CANDIDATE_EVIDENCE",
            "candidate_head": "a" * 40,
            "semantic_subject": driver.SEMANTIC_SUBJECT_DEFAULT,
            "profile": {
                "profile_key_sha256": "1" * 64,
                "profile_document_sha256": "2" * 64,
                "capability_manifest_sha256": "3" * 64,
                "adapter_sha256": "4" * 64,
                "core_sha256": "5" * 64,
                "harness_sha256": "6" * 64,
                "adapter_support_sha256": {},
            },
            "checks": {name: {"status": "PENDING", "attempts": []}
                       for name in core70.EXECUTOR_ADMISSION_CHECKS},
            "section6": {name: {"status": "PENDING", "attempts": []}
                         for name in admission.SECTION6_CELLS},
        }
        admission._write_json(camp / "campaign.json", value)
        return camp

    def test_positive_episode_set_contains_every_frozen_ordinary_case(self):
        self.assertTrue(set(admission.ORDINARY_ENTRY_CASE_EPISODES.values()).issubset(driver.POSITIVE_EPISODES))
        self.assertEqual(tuple(admission.ORDINARY_ENTRY_CASE_EPISODES.values()), driver.ORDINARY_EPISODES)

    def test_prepare_corpus_is_bounded_non_custody_and_append_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            stagef = root / "stagef"
            admission_root = stagef / "admission"
            with mock.patch.object(admission, "STAGEF_WORKSPACE_ROOT", stagef), \
                    mock.patch.object(admission, "ADMISSION_ROOT", admission_root), \
                    mock.patch.object(driver.admission, "STAGEF_WORKSPACE_ROOT", stagef), \
                    mock.patch.object(driver.admission, "ADMISSION_ROOT", admission_root):
                camp = self._campaign(stagef)
                paths = driver.prepare_corpus(camp)
                manifest = json.loads((camp / "synthetic-corpus-manifest.json").read_text())
                self.assertTrue(manifest["non_custody"])
                self.assertFalse(manifest["blinded_protocol7_subjects_used"])
                self.assertEqual(set(manifest["episodes"]), set(driver.ALL_EPISODES))
                self.assertEqual(
                    manifest["ordinary_entry_case_classes"], admission.ORDINARY_ENTRY_CASE_EPISODES
                )
                corpus_manifest = yaml.safe_load((Path(paths["corpus"]) / "manifest.yaml").read_text())
                entries = {row["id"]: row["entry"] for row in corpus_manifest["episodes"]}
                for episode in admission.ORDINARY_ENTRY_CASE_EPISODES.values():
                    self.assertEqual(entries[episode], "ordinary")
                self.assertTrue((Path(paths["corpus"]) / "fixtures" / "hostile" / "project" / ".mcp.json").is_file())
                with self.assertRaises(driver.DriverError):
                    driver.prepare_corpus(camp)

    def test_candidate_head_must_match_exact_checkout(self):
        with mock.patch.object(driver, "_repo_head", return_value="b" * 40):
            with self.assertRaises(driver.DriverError):
                driver._require_candidate_head("a" * 40)
            driver._require_candidate_head("b" * 40)

    def test_freeze_inherit_preserves_route_without_inheriting_stale_support(self):
        source_profile = {
            "adapter_id": driver.omp.ADAPTER_ID,
            "containment_policy": {"provider_route": {
                "provider_id": "deepinfra",
                "model_id": "zai-org/GLM-5.3-Flash",
                "upstream": "https://api.deepinfra.com/v1/openai",
                "api": "openai-completions",
                "base_path": "/chat",
                "context_window": 128000,
                "max_tokens": 8192,
                "reasoning": True,
            }},
            "reasoning_configuration": {"thinking": "high", "source": "--thinking"},
            "budgets": {"max_turns": 30, "timeout_s": 900},
        }
        bundle = mock.Mock(profile=source_profile, profile_key_sha256="1" * 64)
        with tempfile.TemporaryDirectory() as td, \
                mock.patch.object(driver.core70, "load_profile", return_value=bundle), \
                mock.patch.object(driver, "freeze_and_init", return_value=Path(td) / "campaign") as freeze:
            result = driver.freeze_from_source_profile(
                source_profile=Path(td) / "old-profile.json",
                source_capabilities=Path(td) / "old-capabilities.json",
                executable=Path(td) / "omp",
                capabilities=Path(td) / "cap.json",
                candidate_head="a" * 40,
                semantic_subject=driver.SEMANTIC_SUBJECT_DEFAULT,
                profile_id="new-profile",
                expected_provider_id="deepinfra",
                expected_model_id="zai-org/GLM-5.3-Flash",
                expected_upstream="https://api.deepinfra.com/v1/openai",
                expected_source_profile_key="1" * 64,
                label="test",
            )
            self.assertEqual(result, Path(td) / "campaign")
            kwargs = freeze.call_args.kwargs
            self.assertEqual(kwargs["base_path"], "/chat")
            self.assertEqual(kwargs["context_window"], 128000)
            self.assertEqual(kwargs["max_tokens"], 8192)
            self.assertEqual(kwargs["thinking"], "high")
            self.assertEqual(kwargs["max_turns"], 30)
            self.assertEqual(kwargs["timeout_s"], 900)
            self.assertNotIn("containment_policy", kwargs)

    def test_prepare_arms_materializes_exact_frozen_packages_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            camp = root / "campaign"
            camp.mkdir()
            def materialize(repo, commit, destination):
                destination.mkdir(parents=True)
                (destination / "skill.txt").write_text(commit + "\n", encoding="utf-8")
            digests = [
                driver.ARM_SPECS["p66"]["dist_tree_sha256"],
                driver.ARM_SPECS["p70"]["dist_tree_sha256"],
            ]
            with mock.patch.object(driver, "_campaign", return_value={}), \
                    mock.patch.object(driver, "_materialize_git_tree", side_effect=materialize), \
                    mock.patch.object(driver.core70, "sha256_tree", side_effect=digests):
                manifest = driver.prepare_arms(camp, repo=root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual([row["name"] for row in payload["arms"]], ["p66", "p70"])
            self.assertEqual(payload["arms"][0]["commit"], driver.ARM_SPECS["p66"]["commit"])
            self.assertEqual(payload["arms"][1]["commit"], driver.SEMANTIC_SUBJECT_DEFAULT)
            with mock.patch.object(driver, "_campaign", return_value={}):
                with self.assertRaises(driver.DriverError):
                    driver.prepare_arms(camp, repo=root)

    def test_scheduler_trace_proves_sequential_arms_and_concurrent_pairs(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "scheduler.jsonl"
            rows = [
                {"schema": 1, "event": "pair_start", "pair_id": "A-r0", "order": ["p66", "p70"], "monotonic_ns": 10},
                {"schema": 1, "event": "arm_start", "pair_id": "A-r0", "arm": "p66", "monotonic_ns": 11},
                {"schema": 1, "event": "arm_end", "pair_id": "A-r0", "arm": "p66", "monotonic_ns": 20},
                {"schema": 1, "event": "arm_start", "pair_id": "A-r0", "arm": "p70", "monotonic_ns": 21},
                {"schema": 1, "event": "arm_end", "pair_id": "A-r0", "arm": "p70", "monotonic_ns": 40},
                {"schema": 1, "event": "pair_end", "pair_id": "A-r0", "monotonic_ns": 41},
                {"schema": 1, "event": "pair_start", "pair_id": "B-r0", "order": ["p70", "p66"], "monotonic_ns": 15},
                {"schema": 1, "event": "arm_start", "pair_id": "B-r0", "arm": "p70", "monotonic_ns": 16},
                {"schema": 1, "event": "arm_end", "pair_id": "B-r0", "arm": "p70", "monotonic_ns": 25},
                {"schema": 1, "event": "arm_start", "pair_id": "B-r0", "arm": "p66", "monotonic_ns": 26},
                {"schema": 1, "event": "arm_end", "pair_id": "B-r0", "arm": "p66", "monotonic_ns": 35},
                {"schema": 1, "event": "pair_end", "pair_id": "B-r0", "monotonic_ns": 36},
            ]
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            self.assertEqual(driver.scheduler_trace_errors(path), [])
            rows[3]["monotonic_ns"] = 19
            path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            self.assertTrue(any("arms overlap" in item for item in driver.scheduler_trace_errors(path)))

    def test_exact_run_requires_two_distinct_arms_and_parallel_pairs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            camp = root / "campaign"
            camp.mkdir()
            with mock.patch.object(driver, "_campaign", return_value={"profile": {"profile_key_sha256": "x"}}):
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70"], parallel=2)
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70", "p70"], parallel=2)
                with self.assertRaises(driver.DriverError):
                    driver.run_exact_campaign(camp, arms_manifest=root / "arms.json", arms=["p70", "p66"], parallel=1)


if __name__ == "__main__":
    unittest.main()
