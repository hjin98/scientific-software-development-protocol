"""H1 acceptance through the real relay (workplan 7X O-6): deterministic activation, delivery proof and consumed bytes.

Every test launches the real frozen OMP build in bubblewrap through the provider relay (observer principal) with the
scripted delegate bridge; the external model provider alone is the deterministic stand-in. A missing prerequisite is a
reported skip, never a pass.
"""
import functools
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import observer70  # noqa: E402
import test_rig as omp_rig  # noqa: E402
from adapters import omp  # noqa: E402

SKIP = unittest.skipIf(bool(omp_rig.prerequisites()), str(omp_rig.prerequisites()))
SKILLS = omp_rig.DIST_SKILLS
ROOT = "software-implementation"
OWNER_REL = ROOT + "/references/scientific-inspectability-and-initiative.md"
OWNER_PATH = "/opt/ssdp/skills/" + OWNER_REL


def steps(*calls):
    return {"steps": [{"tool_calls": [{"name": name, "arguments": args}]} for name, args in calls] + [{"text": "done"}]}


@SKIP
class RealRelayPath(unittest.TestCase):
    def episode(self, root=ROOT, scenario=None, mechanism="runtime-command", fault=None, claims=None):
        rig = omp_rig.Rig(Path("/tmp"), entry="pinned:" + root, timeout_s=45, claims=claims or [])

        def mutate(profile):
            profile.update(runtime_input_template=omp.input_template(mechanism), activation_mechanism=mechanism,
                           delivery_transform=observer70.OMP_RPC_TRANSFORM, runtime_mode="rpc")
            return profile

        launch = omp.launch if fault is None else functools.partial(omp.launch, integrity_fault=fault)
        with mock.patch.object(omp, "launch", launch):
            return rig.run(scenario or {"steps": [{"text": "done"}]}, mutate_profile=mutate), rig

    def test_every_declared_root_is_delivered_at_request_zero_and_counted_as_entrypoint_only(self):
        for root in sorted(omp.SSDP_SKILLS):
            with self.subTest(root=root):
                summary, _ = self.episode(root=root)
                self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("evidence_state_reasons"))
                self.assertTrue(summary["activation"]["delivered"])
                self.assertEqual(summary["active_ssdp_bytes"], (SKILLS / root / "SKILL.md").stat().st_size)
                self.assertEqual(summary["ssdp_read_mode"], "entry")
                self.assertFalse(summary["resource_observation"]["conservative_shell_count"])

    def test_harness_injection_is_delivered_and_labelled(self):
        summary, _ = self.episode(mechanism="harness-injection")
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("evidence_state_reasons"))
        self.assertTrue(summary["activation"]["delivered"])

    def test_every_broken_delivery_is_refused_by_the_request_zero_proof(self):
        for fault in sorted(omp.INTEGRITY_FAULTS):
            with self.subTest(fault=fault):
                scenario = steps(("read", {"path": "skill://" + ROOT})) if fault == "instructed-read" else None
                summary, _ = self.episode(fault=fault, scenario=scenario)
                self.assertEqual(summary["evidence_state"], "INADMISSIBLE", summary.get("evidence_state_reasons"))
                self.assertFalse(summary["activation"]["delivered"])

    def test_a_native_owner_read_adds_the_file_once_and_marks_owner_mode(self):
        summary, _ = self.episode(scenario=steps(("read", {"path": OWNER_PATH})), claims=["active-byte burden", "owner-read"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("evidence_state_reasons"))
        self.assertEqual(summary["active_ssdp_bytes"], (SKILLS / ROOT / "SKILL.md").stat().st_size + (SKILLS / OWNER_REL).stat().st_size)
        self.assertEqual(summary["ssdp_read_mode"], "owner")
        self.assertTrue(summary["owner_read_sequences"])

    def test_shell_commands_naming_the_package_are_counted_as_full_reads(self):
        entry = (SKILLS / ROOT / "SKILL.md").stat().st_size
        owner = (SKILLS / OWNER_REL).stat().st_size
        references = sum(p.stat().st_size for p in (SKILLS / ROOT / "references").rglob("*") if p.is_file())
        whole_tree = sum(p.stat().st_size for p in SKILLS.rglob("*") if p.is_file()) - entry
        for name, command, expected, mode in (
                ("cat", f"cat {OWNER_PATH}", entry + owner, "owner"),
                ("count only", f"wc -l {OWNER_PATH}", entry + owner, "owner"),      # content not shown: still an upper bound
                ("directory listing", f"ls /opt/ssdp/skills/{ROOT}/references", entry + references, "owner"),
                ("double-quoted path", f'cat "{OWNER_PATH}"', entry + owner, "owner"),
                ("recursive grep on the root without a slash", "grep -r owner /opt/ssdp/skills", entry + whole_tree, "owner"),
                ("no package path", "echo unrelated", entry, "entry")):
            with self.subTest(name):
                summary, _ = self.episode(scenario=steps(("bash", {"command": command})), claims=["active-byte burden"])
                self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("evidence_state_reasons"))
                self.assertEqual(summary["active_ssdp_bytes"], expected)
                self.assertEqual(summary["ssdp_read_mode"], mode)
                self.assertEqual(summary["resource_observation"]["conservative_shell_count"], name != "no package path")

    def test_a_native_grep_over_the_package_and_a_workflow_owner_read_are_counted(self):
        entry = (SKILLS / ROOT / "SKILL.md").stat().st_size
        references = sum(p.stat().st_size for p in (SKILLS / ROOT / "references").rglob("*") if p.is_file())
        summary, _ = self.episode(scenario=steps(("grep", {"pattern": "owner", "path": f"/opt/ssdp/skills/{ROOT}/references"})),
                                  claims=["active-byte burden"])
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("evidence_state_reasons"))
        self.assertEqual(summary["active_ssdp_bytes"], entry + references)
        self.assertEqual(summary["ssdp_read_mode"], "owner")
        workflow = f"{ROOT}/references/workflow-and-workplans.md"
        summary, _ = self.episode(scenario=steps(("read", {"path": "/opt/ssdp/skills/" + workflow})), claims=["active-byte burden"])
        self.assertEqual(summary["active_ssdp_bytes"], entry + (SKILLS / workflow).stat().st_size)
        self.assertEqual(summary["ssdp_read_mode"], "owner")     # any consumed file beyond an entrypoint is owner mode (T7 rule)


if __name__ == "__main__":
    unittest.main()
