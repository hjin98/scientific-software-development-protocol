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
            evidence = workspace / "proof.txt"
            evidence.parent.mkdir()
            evidence.write_text("evidence\n", encoding="utf-8")
            with mock.patch.object(campaign, "STAGEF_WORKSPACE_ROOT", workspace), \
                    mock.patch.object(campaign, "ADMISSION_ROOT", root / "admission"):
                camp = self._campaign(root)
                first = campaign.record_proof(
                    camp,
                    category="check",
                    name=core70.EXECUTOR_ADMISSION_CHECKS[0],
                    evidence_path=evidence,
                    evidence_class="independent-inspection",
                    status="PASS",
                )
                second = campaign.record_proof(
                    camp,
                    category="check",
                    name=core70.EXECUTOR_ADMISSION_CHECKS[0],
                    evidence_path=evidence,
                    evidence_class="independent-inspection",
                    status="PASS",
                )
                self.assertNotEqual(first, second)
                self.assertTrue(first.is_file())
                self.assertTrue(second.is_file())
                evidence.write_text("changed\n", encoding="utf-8")
                errors = campaign.campaign_errors(camp)
                self.assertTrue(any("source evidence hash changed" in item for item in errors), errors)

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
