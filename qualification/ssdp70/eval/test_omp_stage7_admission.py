"""Focused tests for the OMP Stage 7 admission-campaign lifecycle owner."""
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
import omp_stage7_admission as campaign  # noqa: E402


class Stage7AdmissionCampaign(unittest.TestCase):
    def test_admission_workspace_is_an_authorized_realization_root(self):
        self.assertIn(campaign.STAGEF_WORKSPACE_ROOT / "admission", campaign.omp.RUN_REALIZATION_ROOTS)

    def _campaign(self, root: Path) -> Path:
        camp = root / "admission" / "campaign"
        (camp / "proofs").mkdir(parents=True)
        profile = {
            "profile_key_sha256": "1" * 64,
            "adapter_sha256": "2" * 64,
            "core_sha256": "3" * 64,
            "capability_manifest_sha256": "4" * 64,
        }
        value = {
            "schema": campaign.SCHEMA,
            "kind": campaign.KIND,
            "state": "CANDIDATE_EVIDENCE",
            "candidate_head": "a" * 40,
            "semantic_subject": "b" * 40,
            "profile": profile,
            "checks": {name: {"status": "PENDING", "attempts": []}
                       for name in core70.EXECUTOR_ADMISSION_CHECKS},
            "section6": {name: {"status": "PENDING", "attempts": []}
                         for name in campaign.SECTION6_CELLS},
        }
        campaign._write_json(camp / "campaign.json", value)
        return camp

    def test_recorded_proofs_are_append_only_and_source_bound(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            workspace = root / "workspace"
            with mock.patch.object(campaign, "STAGEF_WORKSPACE_ROOT", workspace), \
                    mock.patch.object(campaign, "ADMISSION_ROOT", root / "admission"):
                camp = self._campaign(root)
                evidence = camp / "evidence.txt"
                evidence.write_text("evidence\n", encoding="utf-8")
                first = campaign.record_proof(
                    camp,
                    category="check",
                    name="fail_closed_evidence",
                    evidence_path=evidence,
                    evidence_class="deterministic-falsification",
                    status="PASS",
                )
                second = campaign.record_proof(
                    camp,
                    category="check",
                    name="fail_closed_evidence",
                    evidence_path=evidence,
                    evidence_class="deterministic-falsification",
                    status="PASS",
                )
                self.assertNotEqual(first, second)
                self.assertTrue(first.is_file())
                self.assertTrue(second.is_file())
                evidence.write_text("changed\n", encoding="utf-8")
                errors = campaign.campaign_errors(camp)
                self.assertTrue(any("source evidence hash changed" in item for item in errors), errors)

    def test_exact_profile_label_cannot_be_applied_to_plain_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            workspace = root / "workspace"
            workspace.mkdir()
            with mock.patch.object(campaign, "STAGEF_WORKSPACE_ROOT", workspace), \
                    mock.patch.object(campaign, "ADMISSION_ROOT", root / "admission"):
                camp = self._campaign(root)
                evidence = camp / "not-a-run.txt"
                evidence.write_text("not a harness realization\n", encoding="utf-8")
                with self.assertRaises(campaign.CampaignError) as caught:
                    campaign.record_proof(
                        camp,
                        category="check",
                        name="exact_subject_profile_identity",
                        evidence_path=evidence,
                        evidence_class="exact-profile-behavior",
                        status="PASS",
                    )
                self.assertIn("must be a directory", str(caught.exception))

    def test_execution_error_without_prelaunch_refusal_is_not_exact_profile_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td) / "run"
            run.mkdir()
            summary = {
                "evidence_state": "EXECUTION_ERROR",
                "execution_ok": False,
                "qualification_outcome": "NOT_EVALUATED",
            }
            errors = campaign._prelaunch_refusal_errors(run, summary)
            self.assertTrue(any("not a retained prelaunch refusal" in item for item in errors), errors)
            campaign._write_json(run / "prelaunch-refusal.json", {
                "schema": 1,
                "phase": "realize_containment",
                "reason": "synthetic prelaunch refusal",
                "subject_launched": False,
            })
            self.assertEqual(campaign._prelaunch_refusal_errors(run, summary), [])

    def test_positive_exact_profile_claim_requires_complete_admissible(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            run = root / "run"
            run.mkdir()
            campaign._write_json(run / "run-identity.json", {"schema": 2})
            campaign._write_json(run / "summary.json", {
                "evidence_state": "EXECUTION_ERROR",
                "execution_ok": False,
                "qualification_outcome": "NOT_EVALUATED",
            })
            campaign._write_json(run / "prelaunch-refusal.json", {
                "schema": 1,
                "subject_launched": False,
            })
            with mock.patch.object(campaign, "ADMISSION_ROOT", root):
                errors = campaign._exact_profile_claim_errors(run, "check", "fresh_arm_isolation")
                self.assertTrue(any("COMPLETE_ADMISSIBLE" in item for item in errors), errors)
                self.assertEqual(
                    campaign._exact_profile_claim_errors(run, "check", "catalog_contamination"),
                    [],
                )

    def test_emitted_bundle_is_candidate_and_cannot_satisfy_admission_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            workspace = root / "workspace"
            workspace.mkdir()
            with mock.patch.object(campaign, "STAGEF_WORKSPACE_ROOT", workspace), \
                    mock.patch.object(campaign, "ADMISSION_ROOT", root / "admission"):
                camp = self._campaign(root)
                manifest = json.loads((camp / "campaign.json").read_text(encoding="utf-8"))
                for category, names in (("check", core70.EXECUTOR_ADMISSION_CHECKS),
                                        ("section6", campaign.SECTION6_CELLS)):
                    table = manifest["checks"] if category == "check" else manifest["section6"]
                    for index, name in enumerate(names):
                        source = workspace / f"{category}-{index}.txt"
                        source.write_text(name + "\n", encoding="utf-8")
                        proof = camp / "proofs" / f"{category}-{index}.json"
                        campaign._write_json(proof, {
                            "schema": campaign.SCHEMA,
                            "kind": "omp-stage7-proof-v1",
                            "category": category,
                            "name": name,
                            "status": "PASS",
                            "evidence_class": "independent-inspection",
                            "profile_key_sha256": manifest["profile"]["profile_key_sha256"],
                            **campaign._source_identity(source),
                        })
                        table[name] = {
                            "status": "PASS",
                            "attempts": [],
                            "proof_path": proof.relative_to(camp).as_posix(),
                            "proof_sha256": core70.sha256_file(proof),
                        }
                campaign._write_json(camp / "campaign.json", manifest)
                with mock.patch.object(campaign, "campaign_errors", return_value=[]):
                    candidate = campaign.emit_candidate_bundle(camp)
                payload = json.loads(candidate.read_text(encoding="utf-8"))
                self.assertEqual(payload["status"], "CANDIDATE")
                self.assertEqual(set(payload["checks"]), set(core70.EXECUTOR_ADMISSION_CHECKS))
                errors = core70.validate_profile_admission(
                    candidate,
                    mode="qualification",
                    profile_key_sha256=manifest["profile"]["profile_key_sha256"],
                    adapter_sha256=manifest["profile"]["adapter_sha256"],
                    core_sha256=manifest["profile"]["core_sha256"],
                    capability_manifest_sha256=manifest["profile"]["capability_manifest_sha256"],
                    role="executor",
                )
                self.assertTrue(any("status" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
