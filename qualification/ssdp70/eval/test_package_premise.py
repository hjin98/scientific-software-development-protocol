"""Case (z) at the production mechanical owner; no admission is created by these fixtures."""
import copy
import tempfile
import unittest
from pathlib import Path

import package_premise as pp


class PremiseFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.package = self.root / "package"
        self.package.mkdir()
        self.owner = self.package / "owner.md"
        self.owner.write_text("A distinctive owner line longer than the forty eight byte floor.\n" * 2)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        (self.workspace / "notes.txt").write_text("clean independently constructed fixture\n")
        self.sources = {"workspace": self.workspace, "task": b"Read notes."}
        self.mounts = [{"source":"package","destination":"/opt/package","read_only":True},
                       {"source":"workspace","destination":"/workspace","read_only":False}]

    def tearDown(self):
        self.tmp.cleanup()

    def witness(self):
        return pp.development_witness(pp.inventory(self.package), pp.source_manifest(self.sources),
            mounts=self.mounts, construction_record={"record":"known test seed and output construction",
            "evidence":"literal notes/task unrelated to the independently constructed owner; combined envelope inspected"})

    def check(self, witness=None, **kwargs):
        return pp.check(self.package,self.sources,self.mounts,witness,owner_name="owner.md",**kwargs)


class PremiseBoundary(PremiseFixture):
    def test_z_known_construction_missing_or_unreviewed_source_and_qualification_binding(self):
        witness = self.witness()
        self.assertEqual(self.check(witness)["state"], "PASS")
        self.assertEqual(self.check()["state"], "UNRESOLVED")
        self.assertEqual(self.check(witness,qualification=True)["state"], "UNRESOLVED")
        witness["purpose"] = "qualification"
        self.assertEqual(self.check(witness,qualification=True,accepted_witness_sha256=pp.digest(witness))["state"], "PASS")
        for key in ("nodes", "envelope_warrant"):
            broken = copy.deepcopy(witness); broken.pop(key)
            self.assertEqual(self.check(broken)["state"],"UNRESOLVED")
        broken = copy.deepcopy(witness); broken["nodes"]["workspace"]["inputs"]=["unlisted-generator-input"]
        self.assertEqual(self.check(broken)["state"],"UNRESOLVED")
        broken = copy.deepcopy(witness); broken["nodes"]["workspace"]["inputs"]=["task"]
        broken["nodes"]["task"]["inputs"]=["workspace"]
        self.assertEqual(self.check(broken)["state"],"UNRESOLVED")

    def test_z_stale_package_workspace_generator_output_and_joint_warrant(self):
        witness = self.witness()
        (self.workspace/"extra.txt").write_text("uncovered source")
        self.assertEqual(self.check(witness)["state"],"UNRESOLVED")
        (self.workspace/"extra.txt").unlink()
        self.owner.write_text(self.owner.read_text()+"regenerated package")
        self.assertEqual(self.check(witness)["state"],"UNRESOLVED")
        witness=self.witness(); witness["nodes"]["task"]["warrant"]={"record":"reviewed-generator-hash"}
        self.assertEqual(self.check(witness)["state"],"UNRESOLVED")
        witness=self.witness(); witness["envelope_warrant"]={"record":"PASS"}
        self.assertEqual(self.check(witness)["state"],"UNRESOLVED")

    def test_z_collisions_hard_links_extra_bind_and_escaping_link(self):
        witness = self.witness()
        (self.workspace/"collision.txt").write_bytes(self.owner.read_bytes())
        self.assertEqual(self.check(witness)["state"],"FAIL")
        (self.workspace/"collision.txt").unlink()
        (self.package/"not-owner.txt").write_bytes(self.owner.read_bytes())
        self.assertEqual(self.check(self.witness())["state"],"FAIL")
        (self.package/"not-owner.txt").unlink()
        import os
        os.link(self.owner,self.package/"hardlink.txt")
        self.assertEqual(self.check(self.witness())["state"],"FAIL")
        (self.package/"hardlink.txt").unlink()
        self.mounts.append({"source":"package","destination":"/second","read_only":True})
        self.assertEqual(self.check(self.witness())["state"],"FAIL")
        self.mounts.pop()
        (self.workspace/"escape").symlink_to("../../outside")
        self.assertEqual(self.check(self.witness())["state"],"FAIL")

    def test_z_report_cannot_relabel_unknown_or_development_as_qualified(self):
        report = self.check(self.witness())
        self.assertEqual(pp.verify_report(report),[])
        self.assertTrue(pp.verify_report(report,qualification=True))
        report["sources"]["task"]["."]["sha256"]="0"*64
        self.assertTrue(pp.verify_report(report))
        report = self.check(); report["state"]="PASS"
        self.assertTrue(pp.verify_report(report))

    def test_z_declared_runtime_alias_is_in_the_closed_mount_envelope(self):
        (self.workspace/"loader").symlink_to("/lib/runtime-loader")
        self.assertEqual(self.check(self.witness())["state"],"FAIL")
        self.mounts.append({"source":"workspace","destination":"/lib","read_only":True,"alias_target":"/workspace"})
        self.assertEqual(self.check(self.witness())["state"],"PASS")


class PremiseDetectorsIsolated(PremiseFixture):
    """Independent-review B-2: each detector must fail alone, not only behind another rule that also fires."""
    def test_z_hard_link_between_non_owner_package_files_fails_with_no_owner_content(self):
        import os
        (self.package / "a.txt").write_text("unrelated package file\n")
        os.link(self.package / "a.txt", self.package / "b.txt")
        report = self.check(self.witness())
        self.assertEqual(report["state"], "FAIL")
        self.assertTrue(any("hard link" in f for f in report["failures"]), report["failures"])
        self.assertFalse(any("owner line" in f for f in report["failures"]))

    def test_z_single_embedded_owner_line_in_a_non_identical_source_fails(self):
        line = self.owner.read_text().splitlines()[0]
        (self.workspace / "notes2.txt").write_text("short prefix\n" + line + "\nshort suffix\n")
        report = self.check(self.witness())
        self.assertEqual(report["state"], "FAIL")
        self.assertTrue(any("whole owner line in other source" in f for f in report["failures"]), report["failures"])
        self.assertFalse(any("byte-identical" in f for f in report["failures"]))

    def test_z_mount_from_an_unlisted_source_is_unresolved_not_pass(self):
        self.mounts.append({"source": "unlisted-host-dir", "destination": "/extra", "read_only": True})
        report = self.check(self.witness())
        self.assertEqual(report["state"], "UNRESOLVED")
        self.assertIn("mount source outside frozen input envelope", report["unresolved"])

    def test_z_qualification_needs_the_accepted_digest_and_verify_report_checks_state_and_digest(self):
        witness = self.witness(); witness["purpose"] = "qualification"
        for wrong in (None, "0" * 64):
            self.assertEqual(self.check(witness, qualification=True, accepted_witness_sha256=wrong)["state"], "UNRESOLVED")
        report = self.check(witness, qualification=True, accepted_witness_sha256=pp.digest(witness))
        self.assertEqual(pp.verify_report(report, qualification=True, accepted_witness_sha256=pp.digest(witness)), [])
        self.assertTrue(pp.verify_report(report, qualification=True, accepted_witness_sha256="0" * 64))
        for state in ("FAIL", "UNRESOLVED"):
            self.assertTrue(pp.verify_report({**report, "state": state}))
        self.assertTrue(pp.verify_report({**report, "failures": ["x"]}))
