"""Focused unit tests for the OMP Stage 7 target-host campaign driver."""
import json
import sys
import tempfile
import unittest
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
                self.assertTrue((Path(paths["corpus"]) / "fixtures" / "hostile" / "project" / ".mcp.json").is_file())
                with self.assertRaises(driver.DriverError):
                    driver.prepare_corpus(camp)

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
