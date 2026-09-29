"""Shared-harness repairs required by the OMP D4 tranche (provider-neutral; Claude behavior preserved).

* an adapter-named control path may never hide pre-existing fixture content (repair 3);
* control paths are bound by exact type/content or recursive digest before launch and after the run,
  and an adapter declaring them immutable has any change reported (repair 3, 5);
* adapter principals (support files) participate in run identity (D3 provenance);
* the supervisor never follows an executor-created symlink or executes executor-controlled git
  configuration when it computes the oracle views.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import harness70  # noqa: E402
import test_harness_integration as thi  # noqa: E402


class ControlPathAdapter(thi.FakeAdapter):
    """FakeAdapter whose control paths, mutation policy and support files are test-controlled."""

    PROJECT_CONTROL_MUTATION_POLICY = "immutable"
    control = [".ctl"]
    mutate = False
    support = {}

    @classmethod
    def project_control_paths(cls, profile):
        return list(cls.control)

    @classmethod
    def install_skills(cls, dist, project, env=None):
        target = project / ".ctl" / "skills"
        target.mkdir(parents=True)
        for name in thi.SKILLS:
            shutil.copytree(dist / name, target / name)
        (project / ".ctl" / "config").write_text("frozen")
        return target

    @classmethod
    def launch(cls, profile, prompt, project, env):
        # the owner read of the fake adapter points at .claude; keep the fake trace but read from .ctl
        launched = thi.FakeAdapter.launch(profile, prompt, project, env)
        launched["stdout"] = launched["stdout"].replace(".claude", ".ctl")
        if cls.mutate:
            (project / ".ctl" / "config").write_text("mutated by executor")
        return launched

    @classmethod
    def support_files(cls):
        return dict(cls.support)


class ControlPathPolicy(thi.HarnessIntegration):
    def setUp(self):
        super().setUp()
        ControlPathAdapter.control = [".ctl"]
        ControlPathAdapter.mutate = False
        ControlPathAdapter.support = {}
        # the fake trace reads the owner resource from the adapter's install root
        (self.corpus / "fixtures" / "f1" / "project").mkdir(exist_ok=True)

    def run_with(self, adapter, name="run-cp"):
        return harness70.run_episode(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
            out=self.root / name, profile_bundle=self.bundle, profile_path=self.profile_path,
            capability_path=self.cap_path, requirements=self.requirements, requirements_root=self.req_root,
            adapter_module=adapter, oracles=self.oracles.parent, mode="probe", admission=None,
            identity=harness70.run_identity(
                corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
                profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
                requirements=self.requirements, requirements_root=self.req_root, adapter_module=adapter,
                oracles=self.oracles.parent, mode="probe", admission=None, rep=0, pair_order=["p70"]),
            pair_order=["p70"])

    def test_adapter_cannot_hide_preexisting_fixture_content(self):
        (self.corpus / "fixtures" / "f1" / "project" / ".ctl").mkdir()
        (self.corpus / "fixtures" / "f1" / "project" / ".ctl" / "fixture-owned.txt").write_text("keep")
        with self.assertRaises(core70.ContractError) as ctx:
            self.run_with(ControlPathAdapter)
        self.assertIn("already exist in the fixture baseline", str(ctx.exception))

    def test_control_paths_are_bound_before_and_after_and_unchanged_run_is_clean(self):
        summary = self.run_with(ControlPathAdapter)
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("profile_claim_errors"))
        record = json.loads((self.root / "run-cp" / "project-control-record.json").read_text())
        self.assertEqual(record["control_paths"], [".ctl"])
        self.assertEqual(record["changed"], [])
        self.assertEqual(record["before_launch"][".ctl"]["type"], "directory")
        self.assertEqual(record["before_launch"], record["after_run"])
        self.assertEqual(record["mutation_policy"], "immutable")
        self.assertFalse((self.root / "run-cp" / "final-tree" / ".ctl").exists())

    def test_immutable_control_mutation_is_detected(self):
        ControlPathAdapter.mutate = True
        summary = self.run_with(ControlPathAdapter, "run-mut")
        self.assertNotEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE")
        self.assertTrue(any("immutable provider control path" in e for e in summary["profile_claim_errors"]))
        record = json.loads((self.root / "run-mut" / "project-control-record.json").read_text())
        self.assertEqual(record["changed"], [".ctl"])

    def test_control_name_must_be_an_exact_top_level_name(self):
        ControlPathAdapter.control = ["a/b"]
        with self.assertRaises(core70.ContractError):
            self.run_with(ControlPathAdapter)
        ControlPathAdapter.control = ["*"]
        with self.assertRaises(core70.ContractError):
            self.run_with(ControlPathAdapter)

    def test_adapter_support_files_bind_run_identity_and_change_it(self):
        base = harness70.run_identity(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
            profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=ControlPathAdapter,
            oracles=self.oracles.parent, mode="probe", admission=None, rep=0, pair_order=["p70"])
        self.assertNotIn("adapter_support_sha256", base)
        support = self.root / "principal.py"
        support.write_text("v1")
        ControlPathAdapter.support = {"principal.py": support}
        with_support = harness70.run_identity(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
            profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=ControlPathAdapter,
            oracles=self.oracles.parent, mode="probe", admission=None, rep=0, pair_order=["p70"])
        self.assertIn("adapter_support_sha256", with_support)
        self.assertNotEqual(base["identity_sha256"], with_support["identity_sha256"])
        support.write_text("v2")
        changed = harness70.run_identity(
            corpus=self.corpus, episode=self.episode, arm=self.arm, arms_manifest_sha256="arms", dist=self.dist,
            profile_bundle=self.bundle, profile_path=self.profile_path, capability_path=self.cap_path,
            requirements=self.requirements, requirements_root=self.req_root, adapter_module=ControlPathAdapter,
            oracles=self.oracles.parent, mode="probe", admission=None, rep=0, pair_order=["p70"])
        self.assertNotEqual(with_support["identity_sha256"], changed["identity_sha256"])

    def test_claude_style_adapter_without_the_optional_hooks_is_unchanged(self):
        summary = self.run_with(thi.FakeAdapter, "run-legacy")
        self.assertEqual(summary["evidence_state"], "COMPLETE_ADMISSIBLE", summary.get("profile_claim_errors"))
        record = json.loads((self.root / "run-legacy" / "project-control-record.json").read_text())
        self.assertEqual(record["mutation_policy"], "adapter-classified")
        self.assertEqual(sorted(record["control_paths"]), [".claude", ".mcp.json"])


class ExecutorControlledRepositoryState(unittest.TestCase):
    """The executor owns the project's `.git` and tree; the supervisor must not be its confused deputy."""

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "a.txt").write_text("a\n")
        env = harness70._git_env()
        for args in (["init", "-q"], ["add", "-A"], ["-c", "user.email=e@x", "-c", "user.name=e", "commit", "-qm", "base"]):
            subprocess.run(["git", *args], cwd=self.project, env=env, check=True, capture_output=True)
        self.out = self.root / "out"
        self.out.mkdir()
        self.outside = self.root / "host-file.txt"
        self.outside.write_text("HOST\n")

    def tearDown(self):
        self.td.cleanup()

    def capture(self):
        return harness70.capture_project_state(self.project, self.out, [], [])

    def test_symlinked_project_paths_are_not_followed_into_the_evidence_view(self):
        (self.project / "up").symlink_to("../../../..")
        (self.project / "abs").symlink_to(str(self.outside))
        self.capture()
        tree = self.out / "final-tree"
        self.assertTrue((tree / "up").is_symlink())
        self.assertTrue((tree / "abs").is_symlink())
        record = json.loads((self.out / "final-tree-symlinks.json").read_text())
        self.assertEqual({row["path"]: row["resolves_inside_project"] for row in record["symlinks"]}, {"abs": False, "up": False})

    def test_git_info_exclude_symlink_is_never_written_through(self):
        info = self.project / ".git" / "info"
        info.mkdir(exist_ok=True)
        exclude = info / "exclude"
        if exclude.exists():
            exclude.unlink()
        exclude.symlink_to(self.outside)
        self.capture()
        self.assertEqual(self.outside.read_text(), "HOST\n")
        self.assertFalse(exclude.is_symlink())

    def test_executor_planted_git_command_execution_config_is_not_run(self):
        marker = self.root / "PWNED"
        config = self.project / ".git" / "config"
        config.write_text(f"[core]\n\tfsmonitor = touch {marker}; echo\n[diff \"x\"]\n\ttextconv = touch {marker}.textconv\n"
                          f"[filter \"f\"]\n\tclean = touch {marker}.clean\n")
        (self.project / ".gitattributes").write_text("*.txt diff=x filter=f\n")
        (self.project / "b.txt").write_text("new\n")
        diff = self.capture()
        self.assertFalse(marker.exists())
        self.assertFalse(Path(str(marker) + ".textconv").exists())
        self.assertFalse(Path(str(marker) + ".clean").exists())
        self.assertIn("b.txt", diff)
        raw = (self.out / "project-git-config.raw").read_text()
        self.assertIn("fsmonitor", raw)  # the executor's raw config is retained as evidence

    def test_dotgit_redirect_is_reported_and_git_is_not_run(self):
        shutil.rmtree(self.project / ".git")
        (self.project / ".git").write_text(f"gitdir: {self.root}/elsewhere\n")
        self.assertTrue(harness70.project_git_state_errors(self.project))
        self.assertEqual(self.capture(), "")
        self.assertFalse((self.root / "elsewhere").exists())

    def test_symlinked_git_subdirectory_is_reported(self):
        shutil.rmtree(self.project / ".git" / "info", ignore_errors=True)
        (self.project / ".git" / "info").symlink_to(self.root)
        self.assertTrue(any(".git/info" in e for e in harness70.project_git_state_errors(self.project)))

    def test_normal_change_still_produces_the_diff(self):
        (self.project / "a.txt").write_text("changed\n")
        (self.project / "new.txt").write_text("n\n")
        diff = self.capture()
        self.assertIn("a.txt", diff)
        self.assertIn("new.txt", diff)


if __name__ == "__main__":
    unittest.main()
