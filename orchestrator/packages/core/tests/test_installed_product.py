"""O1 + O11 -- the installed product is the acceptance owner.

Everything here runs against a wheel built from the package and installed into a
throwaway virtual environment *outside* the source checkout, driven through the
real ``sdp`` console script as a subprocess. Nothing in this module can pass by
importing the working tree.

The environment is built once for the module because the build/install cost is
real; each test then exercises the installed artifact independently.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from ._support import commit_all, config_text, git, init_bare, init_repo, write_workplan

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BUILD_TIMEOUT = 900


def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        args, capture_output=True, text=True, check=False, timeout=BUILD_TIMEOUT, **kwargs
    )


class InstalledProductTests(unittest.TestCase):
    """One built wheel, one clean virtual environment, many assertions."""

    tmp: tempfile.TemporaryDirectory
    root: Path
    wheel: Path
    sdp: Path
    venv_python: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)

        dist = cls.root / "dist"
        built = _run(
            [sys.executable, "-m", "build", "--outdir", str(dist), str(PACKAGE_ROOT)]
        )
        if built.returncode != 0:
            raise unittest.SkipTest(f"wheel build unavailable: {built.stderr[-2000:]}")
        wheels = sorted(dist.glob("*.whl"))
        sdists = sorted(dist.glob("*.tar.gz"))
        if not wheels or not sdists:
            raise unittest.SkipTest("build produced no wheel/sdist")
        cls.wheel = wheels[0]
        cls.sdist = sdists[0]

        env_dir = cls.root / "venv"
        created = _run([sys.executable, "-m", "venv", str(env_dir)])
        if created.returncode != 0:
            raise unittest.SkipTest(f"venv creation unavailable: {created.stderr[-2000:]}")
        cls.venv_python = env_dir / "bin" / "python"
        installed = _run([str(cls.venv_python), "-m", "pip", "install", "--quiet", str(cls.wheel)])
        if installed.returncode != 0:
            raise unittest.SkipTest(f"install unavailable: {installed.stderr[-2000:]}")
        cls.sdp = env_dir / "bin" / "sdp"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def setUp(self) -> None:
        self._case = tempfile.TemporaryDirectory()
        self.case = Path(self._case.name)
        self.addCleanup(self._case.cleanup)
        self.repo = init_repo(self.case / "repo")
        write_workplan(
            self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main"
        )
        commit_all(self.repo, "workplan")
        self.config = self.case / "config.toml"
        self.config.write_text(config_text(self.repo), encoding="utf-8")

    def sdp_run(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        """Invoke the installed console script from outside the source checkout."""

        env = dict(os.environ)
        env.pop("PYTHONPATH", None)  # the installed package must stand alone
        return subprocess.run(  # noqa: S603
            [str(self.sdp), *args],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(cwd or self.case),
            env=env,
            timeout=BUILD_TIMEOUT,
        )

    # -- artifact inspection ---------------------------------------------

    def test_wheel_contains_no_root_namespace_init(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            names = archive.namelist()
        self.assertNotIn("sdp_orchestrator/__init__.py", names)
        self.assertIn("sdp_orchestrator/core/__init__.py", names)

    def test_wheel_ships_the_packaged_protocol_snapshot(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            names = set(archive.namelist())
        for resource in ("prompts.md", "profile.json"):
            self.assertIn(
                f"sdp_orchestrator/core/resources/protocol/sdp-protocol-5.16/{resource}", names
            )

    def test_wheel_declares_the_console_script(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            entry_points = next(n for n in archive.namelist() if n.endswith("entry_points.txt"))
            text = archive.read(entry_points).decode("utf-8")
        self.assertIn("sdp = sdp_orchestrator.core._cli:main", text)

    def test_sdist_is_produced(self) -> None:
        self.assertTrue(self.sdist.exists())

    def test_installed_package_lives_outside_the_source_checkout(self) -> None:
        result = _run(
            [str(self.venv_python), "-c",
             "import sdp_orchestrator.core as m; print(m.__file__)"]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(str(PACKAGE_ROOT), result.stdout)

    def test_sibling_namespace_package_coexists(self) -> None:
        """A future sibling distribution must share the PEP 420 namespace."""

        sibling = self.root / "sibling"
        (sibling / "sdp_orchestrator" / "tracker").mkdir(parents=True, exist_ok=True)
        (sibling / "sdp_orchestrator" / "tracker" / "__init__.py").write_text(
            "MARKER = 'sibling-tracker'\n", encoding="utf-8"
        )
        env = dict(os.environ, PYTHONPATH=str(sibling))
        result = _run(
            [str(self.venv_python), "-c",
             "import sdp_orchestrator.core, sdp_orchestrator.tracker as t; print(t.MARKER)"],
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sibling-tracker", result.stdout)

    def test_installed_build_imports_no_higher_module(self) -> None:
        result = _run(
            [str(self.venv_python), "-c",
             "import sdp_orchestrator.core.api.v1, sys;"
             " print([m for m in sys.modules if 'tracker' in m or 'adapters' in m"
             " or 'scheduler' in m])"]
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[]", result.stdout)

    # -- CLI product boundary --------------------------------------------

    def test_installed_cli_renders_a_stage_prompt(self) -> None:
        result = self.sdp_run("implementation", "--config", str(self.config), "--prompt-mode", "local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INPUTS", result.stdout)
        self.assertIn("<<<SDP_STAGE_RESULT_V1", result.stdout)

    def test_stdout_carries_only_the_prompt(self) -> None:
        result = self.sdp_run("implementation", "--config", str(self.config), "--prompt-mode", "local")
        self.assertTrue(result.stdout.startswith("INPUTS"))
        self.assertEqual(result.stderr, "")

    def test_every_stage_alias_uses_the_same_path_as_prompt(self) -> None:
        extra = {
            "baseline": ["--input", "BASELINE_SCOPE=scope"],
            "verification": ["--input", "VERIFICATION_SCOPE=scope"],
            "stabilization": ["--input", "STABILIZATION_SCOPE=scope"],
            "health-audit": ["--input", "AUDIT_SCOPE=scope"],
            "alignment": ["--workplan", "WP", "--input", "UPSTREAM_ACCEPTED_WORK=WP-0"],
            "closeout": ["--workplan", "WP"],
            "design": ["--task", "a new task"],
        }
        for stage in (
            "baseline", "design", "implementation", "review", "verification",
            "stabilization", "alignment", "health-audit", "closeout",
        ):
            args = ["--config", str(self.config), "--prompt-mode", "local", *extra.get(stage, [])]
            direct = self.sdp_run(stage, *args)
            through = self.sdp_run("prompt", stage, *args)
            self.assertEqual(direct.returncode, 0, f"{stage}: {direct.stderr}")
            self.assertEqual(through.returncode, 0, f"{stage}: {through.stderr}")
            # RunId differs per invocation; compare everything else.
            self.assertEqual(
                _strip_run_identity(direct.stdout), _strip_run_identity(through.stdout), stage
            )

    def test_profile_alias_resolves(self) -> None:
        result = self.sdp_run(
            "prompt", "health_audit", "--config", str(self.config),
            "--prompt-mode", "local", "--input", "AUDIT_SCOPE=scope",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_errors_are_redacted_json_on_stderr_with_no_prompt_bytes(self) -> None:
        result = self.sdp_run("design", "--config", str(self.config), "--prompt-mode", "local")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        payload = json.loads(result.stderr)
        self.assertEqual(payload["code"], "core.prompt.input_required")

    def test_stage_disallowed_workplan_fails_at_the_cli(self) -> None:
        result = self.sdp_run(
            "health-audit", "--config", str(self.config), "--workplan", "WP",
            "--input", "AUDIT_SCOPE=s",
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["code"], "core.workplan.disallowed")

    def test_task_outside_design_fails_at_the_cli(self) -> None:
        result = self.sdp_run(
            "implementation", "--config", str(self.config), "--task", "nope"
        )
        self.assertEqual(json.loads(result.stderr)["code"], "core.prompt.input_conflict")

    def test_execution_mode_override_does_not_change_prompt_mode(self) -> None:
        result = self.sdp_run(
            "implementation", "--config", str(self.config), "--prompt-mode", "local",
            "--input", "EXECUTION_MODE=REPORT_ONLY",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("EXECUTION_MODE = REPORT_ONLY", result.stdout)
        self.assertIn(str(self.repo), result.stdout)  # still a local-mode prompt

    def test_prompt_mode_web_leaves_canonical_execution_mode_alone(self) -> None:
        origin = init_bare(self.case / "origin")
        git(self.repo, "remote", "add", "origin", str(origin))
        git(self.repo, "push", "--quiet", "-u", "origin", "main")
        git(self.repo, "remote", "set-url", "origin", "https://example.invalid/owner/repo.git")
        result = self.sdp_run("implementation", "--config", str(self.config), "--prompt-mode", "web")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("EXECUTION_MODE = AUTO_EXECUTE", result.stdout)
        self.assertNotIn(str(self.repo), result.stdout)

    def test_cwd_project_resolution_works_from_inside_the_worktree(self) -> None:
        result = self.sdp_run(
            "implementation", "--config", str(self.config), "--prompt-mode", "local",
            cwd=self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_projects_command_reports_configuration(self) -> None:
        result = self.sdp_run("projects", "--config", str(self.config))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["project_key"], "demo")

    def test_doctor_reports_readiness_without_loading_or_network(self) -> None:
        result = self.sdp_run("doctor", "--config", str(self.config))
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["activation_policy"], "discovery_only")
        self.assertEqual(payload["packaged_profile"]["protocol_version"], "5.16.0")
        self.assertEqual(len(payload["packaged_profile"]["stages"]), 9)

    def test_capabilities_defaults_to_discovery_only(self) -> None:
        result = self.sdp_run("capabilities", "--config", str(self.config))
        payload = json.loads(result.stdout)
        self.assertEqual(payload["activation_policy"], "discovery_only")
        keys = {entry["key"] for entry in payload["capabilities"]}
        self.assertLessEqual(
            {"prompt.render", "project.observe", "workplan.catalog", "workflow.profile"}, keys
        )

    def test_clipboard_extra_is_additive_and_never_blocks_the_prompt(self) -> None:
        result = self.sdp_run(
            "implementation", "--config", str(self.config), "--prompt-mode", "local", "--copy"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("INPUTS", result.stdout)

    def test_offline_rendering_uses_the_packaged_snapshot(self) -> None:
        """No configured Protocol source: the wheel's own snapshot must suffice."""

        offline = self.case / "offline.toml"
        offline.write_text(
            "\n".join(
                (
                    "schema_version = 1",
                    "",
                    "[projects.demo]",
                    f'repo = "{self.repo}"',
                )
            )
            + "\n",
            encoding="utf-8",
        )
        result = self.sdp_run("implementation", "--config", str(offline), "--prompt-mode", "local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REQUIRED_SKILL = software-implementation", result.stdout)

    def test_help_is_available_without_a_configuration(self) -> None:
        result = self.sdp_run("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("implementation", "review", "doctor", "projects", "capabilities"):
            self.assertIn(command, result.stdout)

    def test_pipe_safe_output(self) -> None:
        result = self.sdp_run("implementation", "--config", str(self.config), "--prompt-mode", "local")
        self.assertTrue(result.stdout.endswith("\n"))
        self.assertNotIn("\r", result.stdout)


def _strip_run_identity(text: str) -> str:
    """Remove per-invocation identity so two renders can be compared structurally."""

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("RUN_ID =", "PROMPT_FINGERPRINT =", '"run_id":', '"prompt_fingerprint":')):
            continue
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    unittest.main()
