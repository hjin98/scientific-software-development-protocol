"""O2 -- configuration, project selection, prompt-mode precedence, extension config."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import _errors as E
from sdp_orchestrator.core._config import load_config, parse_config
from sdp_orchestrator.core._limits import MAX_CONFIG_BYTES
from sdp_orchestrator.core._records import ActivationPolicy, ApplicationRequest, PromptExecutionMode
from sdp_orchestrator.core._app import create_application

from ._support import config_text, init_repo


class ConfigValidationTests(unittest.TestCase):
    def test_missing_schema_version_is_rejected(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"core": {}})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_unknown_top_level_key_is_rejected(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "agents": {}})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_secret_bearing_core_key_is_rejected(self) -> None:
        """Core sections are closed, so an ad-hoc credential key cannot be stored."""

        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config(
                {
                    "schema_version": 1,
                    "projects": {"a": {"repo": "/tmp/x", "api_token": "sk-secret"}},
                }
            )
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)
        self.assertNotIn("sk-secret", str(caught.exception.problem.to_dict()))

    def test_credential_url_is_rejected_and_redacted(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config(
                {
                    "schema_version": 1,
                    "protocol_sources": {
                        "p": {
                            "remote_repository": "https://user:tok3n@example.invalid/r.git",
                            "allow_remote": True,
                            "remote_ref": "main",
                        }
                    },
                }
            )
        rendered = str(caught.exception.problem.to_dict())
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)
        self.assertNotIn("tok3n", rendered)
        self.assertIn("<redacted>", rendered)

    def test_remote_source_requires_explicit_ref(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config(
                {
                    "schema_version": 1,
                    "protocol_sources": {
                        "p": {"allow_remote": True, "remote_repository": "https://e.invalid/r"}
                    },
                }
            )
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_remote_is_disabled_by_default(self) -> None:
        config = parse_config(
            {"schema_version": 1, "protocol_sources": {"p": {"remote_repository": "https://e/r"}}}
        )
        self.assertFalse(config.protocol_sources["p"].allow_remote)

    def test_default_project_must_exist(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "core": {"default_project": "missing"}})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_oversized_config_is_rejected_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.toml"
            path.write_text("# padding\n" * (MAX_CONFIG_BYTES // 5), encoding="utf-8")
            with self.assertRaises(E.OrchestratorError) as caught:
                load_config(path)
            self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_malformed_toml_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.toml"
            path.write_text("schema_version = = 1\n", encoding="utf-8")
            with self.assertRaises(E.OrchestratorError) as caught:
                load_config(path)
            self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_absent_extension_namespace_is_preserved_and_inactive(self) -> None:
        config = parse_config(
            {"schema_version": 1, "extensions": {"vendor.tracker": {"retention_days": 30}}}
        )
        self.assertEqual(config.extension_namespaces["vendor.tracker"]["retention_days"], 30)

    def test_unrelated_extension_config_does_not_change_configuration_identity(self) -> None:
        """Invariant 14: unrelated extension config must not perturb Core identity."""

        base = {"schema_version": 1, "projects": {"a": {"repo": "/tmp/x"}}}
        with_ext = dict(base) | {"extensions": {"vendor.x": {"anything": [1, 2, 3]}}}
        self.assertEqual(
            parse_config(base).identity.value, parse_config(with_ext).identity.value
        )

    def test_env_override_allowlist_is_empty(self) -> None:
        """V1 defines no semantic environment-variable override surface."""

        import sdp_orchestrator.core._config as config_module

        self.assertFalse(
            [name for name in dir(config_module) if "ENV" in name and name.isupper()],
            "no environment override allowlist is defined in v1",
        )


class ProjectResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo_a = init_repo(self.root / "a")
        self.repo_b = init_repo(self.root / "b")

    def _core(self, text: str):
        path = self.root / "config.toml"
        path.write_text(text, encoding="utf-8")
        return create_application(ApplicationRequest(config_path=str(path))).core()

    def test_explicit_project_wins(self) -> None:
        core = self._core(
            config_text(self.repo_a, project="alpha", default_project="alpha")
            + f'\n[projects.beta]\nrepo = "{self.repo_b}"\n'
        )
        self.assertEqual(str(core.resolve_project_key("beta")), "beta")

    def test_cwd_containment_selects_a_unique_project(self) -> None:
        core = self._core(
            config_text(self.repo_a, project="alpha", default_project=None)
            + f'\n[projects.beta]\nrepo = "{self.repo_b}"\n'
        )
        self.assertEqual(str(core.resolve_project_key(None, cwd=self.repo_b)), "beta")

    def test_default_project_is_used_outside_any_worktree(self) -> None:
        core = self._core(
            config_text(self.repo_a, project="alpha", default_project="alpha")
            + f'\n[projects.beta]\nrepo = "{self.repo_b}"\n'
        )
        self.assertEqual(str(core.resolve_project_key(None, cwd=self.root)), "alpha")

    def test_sole_configured_project_is_used(self) -> None:
        core = self._core(config_text(self.repo_a, project="alpha", default_project=None))
        self.assertEqual(str(core.resolve_project_key(None, cwd=self.root)), "alpha")

    def test_ambiguous_project_fails_explicitly(self) -> None:
        core = self._core(
            config_text(self.repo_a, project="alpha", default_project=None)
            + f'\n[projects.beta]\nrepo = "{self.repo_b}"\n'
        )
        with self.assertRaises(E.OrchestratorError) as caught:
            core.resolve_project_key(None, cwd=self.root)
        self.assertEqual(caught.exception.code, E.PROJECT_AMBIGUOUS)

    def test_unknown_project_fails(self) -> None:
        core = self._core(config_text(self.repo_a, project="alpha", default_project="alpha"))
        with self.assertRaises(E.OrchestratorError) as caught:
            core.resolve_project_key("nope")
        self.assertEqual(caught.exception.code, E.PROJECT_NOT_FOUND)

    def test_nested_cwd_resolves_to_the_containing_project(self) -> None:
        nested = self.repo_b / "deep" / "deeper"
        nested.mkdir(parents=True)
        core = self._core(
            config_text(self.repo_a, project="alpha", default_project="alpha")
            + f'\n[projects.beta]\nrepo = "{self.repo_b}"\n'
        )
        self.assertEqual(str(core.resolve_project_key(None, cwd=nested)), "beta")


class PromptModePrecedenceTests(unittest.TestCase):
    """Built-in default is web; Core never silently falls back from web to local."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.repo = init_repo(self.root / "repo")

    def _mode(self, **kwargs: object) -> PromptExecutionMode:
        path = self.root / "config.toml"
        path.write_text(config_text(self.repo, **kwargs), encoding="utf-8")  # type: ignore[arg-type]
        application = create_application(
            ApplicationRequest(config_path=str(path), activation_policy=ActivationPolicy.NORMAL)
        )
        section = application.config().project("demo")
        if section.default_prompt_mode is not None:
            return section.default_prompt_mode
        if application.config().core.default_prompt_mode is not None:
            return application.config().core.default_prompt_mode
        return PromptExecutionMode.WEB

    def test_builtin_default_is_web(self) -> None:
        self.assertIs(self._mode(), PromptExecutionMode.WEB)

    def test_core_default_overrides_builtin(self) -> None:
        self.assertIs(self._mode(core_prompt_mode="local"), PromptExecutionMode.LOCAL)

    def test_project_default_overrides_core_default(self) -> None:
        self.assertIs(
            self._mode(core_prompt_mode="local", prompt_mode="web"), PromptExecutionMode.WEB
        )

    def test_explicit_mode_must_be_local_or_web(self) -> None:
        from sdp_orchestrator.core._cli import _prompt_mode

        with self.assertRaises(E.OrchestratorError) as caught:
            _prompt_mode("remote")
        self.assertEqual(caught.exception.code, E.PROMPT_MODE_INVALID)


if __name__ == "__main__":
    unittest.main()


class BoundedInputTests(unittest.TestCase):
    """Every externally influenced reader rejects before unbounded materialization."""

    def test_extension_namespace_count_is_bounded(self) -> None:
        from sdp_orchestrator.core._limits import MAX_CONFIG_EXTENSION_NAMESPACES

        namespaces = {f"vendor.{i}": {"v": 1} for i in range(MAX_CONFIG_EXTENSION_NAMESPACES + 1)}
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "extensions": namespaces})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_extension_namespace_size_is_bounded(self) -> None:
        from sdp_orchestrator.core._limits import MAX_CONFIG_EXTENSION_BYTES

        payload = {"blob": "x" * (MAX_CONFIG_EXTENSION_BYTES + 16)}
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "extensions": {"vendor.big": payload}})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_project_count_is_bounded(self) -> None:
        from sdp_orchestrator.core._limits import MAX_CONFIG_PROJECTS

        projects = {f"p{i}": {"repo": "/tmp/x"} for i in range(MAX_CONFIG_PROJECTS + 1)}
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "projects": projects})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_configuration_nesting_is_bounded(self) -> None:
        from sdp_orchestrator.core._limits import MAX_CONFIG_NESTING

        deep: dict = {"v": 1}
        for _ in range(MAX_CONFIG_NESTING + 4):
            deep = {"n": deep}
        with self.assertRaises(E.OrchestratorError) as caught:
            parse_config({"schema_version": 1, "extensions": {"vendor.deep": deep}})
        self.assertEqual(caught.exception.code, E.CONFIG_INVALID)

    def test_every_documented_limit_is_finite_and_positive(self) -> None:
        from sdp_orchestrator.core import _limits

        numeric = {
            name: getattr(_limits, name)
            for name in dir(_limits)
            if name.isupper() and isinstance(getattr(_limits, name), (int, float))
        }
        self.assertTrue(numeric)
        for name, value in numeric.items():
            self.assertGreater(value, 0, name)
            self.assertNotEqual(value, float("inf"), name)
