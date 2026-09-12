from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
import project_engineering_memory as pem


def family(kind="SUCCESS_PATTERN", fid="SP-001"):
    base = {
        "id": fid,
        "kind": kind,
        "state": "CURRENT",
        "maturity": "SUPPORTED",
        "temperature": "UNASSESSED",
        "summary": "bounded lesson",
        "semantic_identity": {
            "invariant_or_claim": "bounded claim",
            "owner_class": "D4",
            "mechanism_family": "bounded mechanism",
            "applicability_dimensions": "test regime",
        },
        "aggregation_scope": "test",
        "coverage_state": "PARTIAL",
        "coverage_basis": "bounded",
        "applicability": ["test"],
        "authority_binding": "EVIDENCE_ONLY",
        "guidance_level": "OBSERVED",
        "relations": [],
    }
    if kind == "SUCCESS_PATTERN":
        base.update({
            "positive_guidance_eligible": False,
            "comparative_basis": "NONE",
            "applications": [{
                "id": "A01",
                "episode_identity": "event-1",
                "lifecycle_context": "qualification",
                "source_project": "local",
                "surfaces": ["x"],
                "provenance_cluster": "CLUSTER-1",
                "outcome": "SUPPORTING",
                "observation": "observed support",
                "assessments": [{
                    "id": "AS01", "state": "ADMISSIBLE", "conclusion": "SUPPORTS_BOUNDED_CLAIM",
                    "evidence": ["fixture/project@1111111:path.md#case"],
                }],
            }],
        })
    return base


def root_text(families, *, repository="fixture/project", accepted="base-1", overlay="overlay-1", detail_files=None, notices=None):
    front = {
        "memory_schema_version": 1,
        "maintained_under_protocol": "6.3.0",
        "project_id": "fixture",
        "repository": repository,
        "scope": "repository",
        "coverage_state": "PARTIAL",
        "coverage_basis": "bounded",
        "reconciled_through": "r1",
        "accepted_base": accepted,
        "candidate_overlay": overlay,
        "detail_files": detail_files or [],
    }
    chunks = ["---\n", yaml.safe_dump(front, sort_keys=False), "---\n\n# Project Engineering Memory\n\n## Active summary\n\n<!-- BEGIN DERIVED PEM SUMMARY -->\n_stale_\n<!-- END DERIVED PEM SUMMARY -->\n\n## Families\n\n"]
    for f in families:
        chunks += [f"### {f['id']} — Fixture\n\n```yaml pem-family\n", yaml.safe_dump(f, sort_keys=False), "```\n\n"]
    if notices:
        chunks.append("## Current notices\n\n")
        for n in notices:
            chunks += [f"### {n['id']} — Fixture\n\n```yaml pem-notice\n", yaml.safe_dump(n, sort_keys=False), "```\n\n"]
    return "".join(chunks)


def write_doc(path: Path, families, **kwargs):
    path.write_text(root_text(families, **kwargs), encoding="utf-8")
    doc = pem.load_memory(path)
    pem.write_summary(doc)
    return pem.load_memory(path)


class ReopenedRepairs(unittest.TestCase):
    def test_d1_blob_as_revision_and_missing_path_do_not_pass_healthy(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
            (repo / "evidence.md").write_text("evidence\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "evidence.md"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "evidence"], check=True)
            commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            blob = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD:evidence.md"], text=True).strip()
            f = family("PRESERVATION_CAPABILITY", "PC-001")
            f["binding_health"] = "HEALTHY"
            f["evidence"] = [f"fixture/project@{commit}:evidence.md"]
            doc = write_doc(repo / "PROJECT-ENGINEERING-MEMORY.md", [f])
            self.assertEqual(pem.validate_memory(doc), [])
            f["evidence"] = [f"fixture/project@{blob}:evidence.md"]
            doc = write_doc(repo / "PROJECT-ENGINEERING-MEMORY.md", [f])
            self.assertTrue(any("blob object" in e for e in pem.validate_memory(doc)))
            f["evidence"] = [f"fixture/project@{commit}:missing.md"]
            doc = write_doc(repo / "PROJECT-ENGINEERING-MEMORY.md", [f])
            self.assertTrue(any("path is absent" in e for e in pem.validate_memory(doc)))

    def test_d2_partition_digest_and_basis_are_atomic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            part = root / "detail.md"
            front = {
                "memory_schema_version": 1, "pem_partition": True, "project_id": "fixture",
                "repository": "fixture/project", "scope": "repository", "accepted_base": "base-1", "candidate_overlay": "overlay-1",
            }
            f = family()
            part.write_text("---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n# Detail\n\n" + f"### {f['id']} — Fixture\n\n```yaml pem-family\n" + yaml.safe_dump(f, sort_keys=False) + "```\n", encoding="utf-8")
            digest = hashlib.sha256(part.read_bytes()).hexdigest()
            path = root / "PROJECT-ENGINEERING-MEMORY.md"
            path.write_text(root_text([], detail_files=[{"path": "detail.md", "sha256": digest}]), encoding="utf-8")
            self.assertIn("SP-001", pem.load_memory(path).families)
            part.write_text(part.read_text(encoding="utf-8").replace("bounded lesson", "changed lesson"), encoding="utf-8")
            with self.assertRaisesRegex(pem.PemError, "partition digest mismatch"):
                pem.load_memory(path)

    def test_d3_admissible_row_requires_observation_and_rewrite_needs_correction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            f = family()
            f["applications"][0].pop("observation")
            path = root / "missing.md"
            path.write_text(root_text([f]), encoding="utf-8")
            self.assertTrue(any("observation" in e for e in pem.validate_memory(pem.load_memory(path), check_summary=False)))
            old = family(); new = copy.deepcopy(old); new["applications"][0]["observation"] = "rewritten"
            old_path = root / "old.md"; new_path = root / "new.md"
            old_path.write_text(root_text([old]), encoding="utf-8"); new_path.write_text(root_text([new]), encoding="utf-8")
            errors = pem.validate_reconciliation(pem.load_memory(old_path), pem.load_memory(new_path))
            self.assertTrue(any("without clerical-correction provenance" in e for e in errors))
            old_hash = hashlib.sha256(b"observed support").hexdigest()
            new["applications"][0]["observation_correction"] = {"previous_sha256": old_hash, "reason": "clerical", "evidence": ["fixture/project@1111111:path.md#correction"]}
            new_path.write_text(root_text([new]), encoding="utf-8")
            self.assertEqual(pem.validate_reconciliation(pem.load_memory(old_path), pem.load_memory(new_path)), [])

    def test_d4_truthy_prior_repair_label_cannot_create_recurrence(self):
        f = family("FAILURE_FAMILY", "FF-001")
        f["maturity"] = "PROVISIONAL"
        f["occurrences"] = [{
            "id": "O01", "event_identity": "event-1", "lifecycle_context": "qualification", "source_project": "local",
            "surfaces": ["x"], "observation": "failure", "recurrence_after_accepted_repair": True,
            "prior_accepted_repair": "anything",
            "assessments": [{"id": "AS01", "state": "ADMISSIBLE", "conclusion": "CONFIRMED", "evidence": ["fixture/project@1111111:path.md#case"]}],
        }]
        with self.assertRaisesRegex(pem.PemError, "structured recurrence_basis"):
            pem.derived_counts(f)

    def test_d5_common_cluster_cannot_fake_proven_independence(self):
        f = family(); f["maturity"] = "PROVEN"; f["applications"] = []
        for i in range(3):
            app = copy.deepcopy(family()["applications"][0]); app["id"] = f"A{i+1:02d}"; app["episode_identity"] = f"event-{i}"; app["provenance_cluster"] = "ONE-COMMON-CLUSTER"; f["applications"].append(app)
        f["temperature"] = "HOT"
        f["maturity_basis"] = {"claim": "independently replicated", "obligations": [{"type": "independent_replication", "status": "CLOSED", "minimum_independent_clusters": 2, "evidence": ["fixture/project@1111111:path.md#case"]}]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"; path.write_text(root_text([f]), encoding="utf-8")
            errors = pem.validate_memory(pem.load_memory(path), check_summary=False)
            self.assertTrue(any("supporting provenance cluster" in e for e in errors))

    def test_d6_fired_or_opaque_notice_cannot_remain_current(self):
        base = {"id": "NT-001", "state": "CURRENT", "summary": "notice", "normative_status": "NON_AUTHORITATIVE", "owner": "NONE", "applicability": ["test"], "binding_health": "HEALTHY", "evidence": ["fixture/project@1111111:path.md#notice"]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "PROJECT-ENGINEERING-MEMORY.md"
            notice = copy.deepcopy(base); notice["review_trigger"] = {"type": "deadline", "at": "2000-01-01"}
            path.write_text(root_text([], notices=[notice]), encoding="utf-8")
            self.assertTrue(any("trigger is FIRED" in e for e in pem.validate_memory(pem.load_memory(path), check_summary=False)))
            notice = copy.deepcopy(base); notice["review_or_expiry"] = "whenever appropriate"
            path.write_text(root_text([], notices=[notice]), encoding="utf-8")
            self.assertTrue(any("trigger is INDETERMINATE" in e for e in pem.validate_memory(pem.load_memory(path), check_summary=False)))

    def test_d7_has_pins_basis_and_cannot_omit_accepted_entries(self):
        record = {"pem_basis": {"accepted_project_state": "base", "accepted_pem": "pem-base", "candidate_overlay_semantic_candidate": "candidate"}, "has": [{"id": "SP-001", "disposition": "APPLICABLE", "reason": "matches"}]}
        self.assertEqual(pem.validate_has(record, accepted_project_state="base", accepted_pem="pem-base", candidate_overlay_identity="candidate", accepted_ids=["SP-001"]), [])
        errors = pem.validate_has(record, accepted_project_state="base", accepted_pem="pem-base", candidate_overlay_identity="candidate", accepted_ids=["SP-001", "FF-001"])
        self.assertTrue(any("omission" in e for e in errors))
        errors = pem.validate_has(record, accepted_project_state="base", accepted_pem="pem-base", candidate_overlay_identity="candidate", accepted_ids=["SP-001"], current_accepted_project_state="new-base")
        self.assertTrue(any("basis advanced" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
