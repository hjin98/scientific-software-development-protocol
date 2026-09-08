"""O10 -- extension discovery, activation, degradation, and event subscription.

Discovery uses *real* installed distribution metadata: each fixture writes a
``.dist-info`` directory on ``sys.path`` so ``importlib.metadata`` finds it the
same way it finds a pip-installed package.

The sharpest assertion is that discovery-only never imports provider code. Each
fixture module records its own import in a marker file, so "was it loaded?" is
observed rather than assumed.
"""

from __future__ import annotations

import contextlib
import importlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

from sdp_orchestrator.core import _errors as E
from sdp_orchestrator.core._app import (
    ENTRY_POINT_GROUP,
    create_application,
    discover,
)
from sdp_orchestrator.core._records import (
    ActivationPolicy,
    ApplicationRequest,
    CapabilityKey,
    CapabilityRequirement,
    Multiplicity,
)

from ._support import commit_all, config_text, init_repo, write_workplan

MARKER_ENV = "SDP_TEST_IMPORT_MARKER"

PROVIDER_TEMPLATE = '''
import os
from pathlib import Path

from sdp_orchestrator.core.spi.v1 import (
    CapabilityProvision,
    CapabilityRequirement,
    EventSubscription,
    ExtensionManifest,
    ExtensionRegistration,
    Multiplicity,
)

# Recorded at import time so a test can observe whether this module was loaded.
_marker = os.environ.get({marker_env!r})
if _marker:
    Path(_marker).write_text(
        (Path(_marker).read_text() if Path(_marker).exists() else "") + {extension_id!r} + "\\n"
    )

ACTIVATED = []


class Provider:
    def manifest(self):
        return ExtensionManifest(
            extension_id={manifest_extension_id!r},
            extension_version="1.0.0",
            core_spi_spec={spi_spec!r},
            requires_extensions={requires_extensions!r},
            requires_capabilities=tuple(
                CapabilityRequirement(key=key, api_spec=api_spec)
                for key, api_spec in zip({requires_capabilities!r}, {required_api_specs!r})
            ),
            provides_capabilities=tuple(
                CapabilityProvision(
                    key=key, api_major={provide_api_major},
                    multiplicity=Multiplicity({provides_multiplicity!r})
                ) for key in {provides!r}
            ),
        )

    def activate(self, context):
        {activate_body}
        for key in {provides!r}:
            context.register_service(key, {provide_api_major}, self)
        ACTIVATED.append(context.extension_id)
        return ExtensionRegistration(
            services=tuple((k, {provide_api_major}) for k in {provides!r}),
            subscriptions=tuple(
                EventSubscription(event_types=event_types)
                for event_types in {subscriptions!r}
            ),
        )


provider = Provider()
'''


def _install_fixture(
    root: Path,
    *,
    name: str,
    extension_id: str,
    spi_spec: str = ">=1.0.0",
    manifest_extension_id: str | None = None,
    requires_extensions: tuple[str, ...] = (),
    requires_capabilities: tuple[str, ...] = (),
    required_api_specs: tuple[str, ...] = (),
    provides: tuple[str, ...] = (),
    provide_api_major: int = 1,
    provides_multiplicity: str = "singular",
    subscriptions: tuple[tuple[str, ...], ...] = (),
    activate_body: str = "pass",
) -> None:
    """Write a real installed distribution: module + ``.dist-info`` metadata."""

    module = f"sdp_fixture_{name}"
    manifest_extension_id = manifest_extension_id or extension_id
    required_api_specs = required_api_specs or tuple("" for _ in requires_capabilities)
    (root / f"{module}.py").write_text(
        PROVIDER_TEMPLATE.format(
            marker_env=MARKER_ENV,
            extension_id=extension_id,
            manifest_extension_id=manifest_extension_id,
            spi_spec=spi_spec,
            requires_extensions=requires_extensions,
            requires_capabilities=requires_capabilities,
            required_api_specs=required_api_specs,
            provides=provides,
            provide_api_major=provide_api_major,
            provides_multiplicity=provides_multiplicity,
            subscriptions=subscriptions,
            activate_body=activate_body,
        ),
        encoding="utf-8",
    )
    dist = root / f"{module}-1.0.0.dist-info"
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "METADATA").write_text(
        f"Metadata-Version: 2.1\nName: {module}\nVersion: 1.0.0\n", encoding="utf-8"
    )
    (dist / "entry_points.txt").write_text(
        f"[{ENTRY_POINT_GROUP}]\n{extension_id} = {module}:provider\n", encoding="utf-8"
    )


class ExtensionBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

        self.site = self.root / "site"
        self.site.mkdir()
        sys.path.insert(0, str(self.site))
        self.addCleanup(sys.path.remove, str(self.site))
        self.addCleanup(self._purge_modules)

        self.marker = self.root / "imported.txt"
        os.environ[MARKER_ENV] = str(self.marker)
        self.addCleanup(os.environ.pop, MARKER_ENV, None)

        self.repo = init_repo(self.root / "repo")
        write_workplan(self.repo, "workplans/active/WP.md", workplan_id="WP", target_branch="main")
        commit_all(self.repo, "workplan")
        self.config = self.root / "config.toml"
        self.config.write_text(config_text(self.repo), encoding="utf-8")

    def _purge_modules(self) -> None:
        for name in [n for n in sys.modules if n.startswith("sdp_fixture_")]:
            del sys.modules[name]
        importlib.invalidate_caches()

    def imported(self) -> list[str]:
        if not self.marker.exists():
            return []
        return [line for line in self.marker.read_text().splitlines() if line]

    def app(self, policy=ActivationPolicy.NORMAL, config_extra: str = ""):
        if config_extra:
            self.config.write_text(
                config_text(self.repo, extra=config_extra), encoding="utf-8"
            )
        importlib.invalidate_caches()
        return create_application(
            ApplicationRequest(config_path=str(self.config), activation_policy=policy)
        )

    def status(self, application, extension_id: str):
        for status in application.extensions():
            if str(status.extension_id) == extension_id:
                return status
        self.fail(f"{extension_id} was not reported")


class DiscoveryOnlyTests(ExtensionBase):
    def test_discovery_reads_metadata_without_importing_provider_code(self) -> None:
        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        application = self.app(ActivationPolicy.DISCOVERY_ONLY)
        status = self.status(application, "vendor.alpha")
        self.assertEqual(status.state, "discovered")
        self.assertEqual(self.imported(), [], "discovery must not import provider code")

    def test_discovery_does_not_claim_unobserved_capabilities(self) -> None:
        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        application = self.app(ActivationPolicy.DISCOVERY_ONLY)
        self.assertFalse(
            application.has(CapabilityRequirement(key=CapabilityKey("x.y"))),
            "an unloaded provider's capability must not be reported as available",
        )
        detail = self.status(application, "vendor.alpha").detail or ""
        self.assertIn("not imported", detail)

    def test_discovery_reports_distribution_metadata(self) -> None:
        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha")
        status = self.status(self.app(ActivationPolicy.DISCOVERY_ONLY), "vendor.alpha")
        self.assertEqual(status.version, "1.0.0")
        self.assertIn("sdp_fixture_alpha", status.entry_point or "")

    def test_discovery_is_the_default_policy(self) -> None:
        self.assertIs(ApplicationRequest().activation_policy, ActivationPolicy.DISCOVERY_ONLY)

    def test_core_stays_fully_functional_without_extensions(self) -> None:
        application = self.app(ActivationPolicy.DISCOVERY_ONLY)
        self.assertTrue(
            application.has(CapabilityRequirement(key=CapabilityKey("prompt.render")))
        )
        self.assertEqual(discover.__name__, "discover")


class NormalActivationTests(ExtensionBase):
    def test_normal_mode_imports_and_activates(self) -> None:
        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        application = self.app()
        self.assertEqual(self.status(application, "vendor.alpha").state, "active")
        self.assertEqual(self.imported(), ["vendor.alpha"])
        self.assertTrue(application.has(CapabilityRequirement(key=CapabilityKey("x.y"))))

    def test_incompatible_spi_specifier_disables_the_provider(self) -> None:
        _install_fixture(
            self.site, name="alpha", extension_id="vendor.alpha", spi_spec=">=99.0.0",
            provides=("x.y",),
        )
        application = self.app()
        status = self.status(application, "vendor.alpha")
        self.assertEqual(status.state, "disabled")
        self.assertIn("core.extension.incompatible", status.detail or "")
        self.assertFalse(application.has(CapabilityRequirement(key=CapabilityKey("x.y"))))

    def test_missing_capability_requirement_disables_the_dependent(self) -> None:
        _install_fixture(
            self.site, name="alpha", extension_id="vendor.alpha",
            requires_capabilities=("absent.capability",),
        )
        status = self.status(self.app(), "vendor.alpha")
        self.assertEqual(status.state, "disabled")
        self.assertIn("absent.capability", status.detail or "")

    def test_dependency_cycle_is_deterministic_and_non_fatal(self) -> None:
        _install_fixture(
            self.site, name="alpha", extension_id="vendor.alpha",
            provides=("cap.a",), requires_capabilities=("cap.b",),
        )
        _install_fixture(
            self.site, name="beta", extension_id="vendor.beta",
            provides=("cap.b",), requires_capabilities=("cap.a",),
        )
        application = self.app()
        for extension_id in ("vendor.alpha", "vendor.beta"):
            status = self.status(application, extension_id)
            self.assertEqual(status.state, "disabled")
            self.assertIn("core.extension.dependency_cycle", status.detail or "")
        self.assertTrue(
            application.has(CapabilityRequirement(key=CapabilityKey("prompt.render"))),
            "a broken extension graph must not disable healthy Core services",
        )

    def test_dependency_order_activates_the_provider_first(self) -> None:
        _install_fixture(self.site, name="base", extension_id="vendor.base", provides=("cap.base",))
        _install_fixture(
            self.site, name="dependent", extension_id="vendor.dependent",
            requires_capabilities=("cap.base",), provides=("cap.top",),
        )
        application = self.app()
        self.assertEqual(self.status(application, "vendor.base").state, "active")
        self.assertEqual(self.status(application, "vendor.dependent").state, "active")

    def test_failing_provider_degrades_without_breaking_core(self) -> None:
        _install_fixture(
            self.site, name="broken", extension_id="vendor.broken",
            activate_body='raise RuntimeError("activation exploded")',
        )
        _install_fixture(self.site, name="ok", extension_id="vendor.ok", provides=("cap.ok",))
        application = self.app()
        self.assertEqual(self.status(application, "vendor.broken").state, "failed")
        self.assertEqual(self.status(application, "vendor.ok").state, "active")
        self.assertTrue(application.has(CapabilityRequirement(key=CapabilityKey("cap.ok"))))

    def test_staged_registration_is_discarded_when_activation_raises(self) -> None:
        _install_fixture(
            self.site,
            name="broken_staged",
            extension_id="vendor.broken_staged",
            provides=("cap.broken",),
            activate_body=(
                "context.register_service('cap.broken', 1, self);"
                " context.subscribe(('core.prompt.rendered.v1',), lambda event: None);"
                " raise RuntimeError('activation exploded after registration')"
            ),
        )
        _install_fixture(
            self.site,
            name="dependent",
            extension_id="vendor.dependent",
            requires_capabilities=("cap.broken",),
        )
        application = self.app()
        self.assertEqual(self.status(application, "vendor.broken_staged").state, "failed")
        self.assertEqual(self.status(application, "vendor.dependent").state, "disabled")
        self.assertFalse(
            application.has(CapabilityRequirement(key=CapabilityKey("cap.broken")))
        )
        self.assertEqual(application.events()._sinks, [])  # noqa: SLF001 - atomicity oracle

    def test_capability_api_spec_is_checked_against_the_provisioned_major(self) -> None:
        _install_fixture(
            self.site,
            name="api_one",
            extension_id="vendor.api_one",
            provides=("cap.versioned",),
            provide_api_major=1,
        )
        application = self.app()
        requirement = CapabilityRequirement(
            key=CapabilityKey("cap.versioned"), api_spec=">=2"
        )
        self.assertFalse(application.has(requirement))
        with self.assertRaises(E.OrchestratorError) as caught:
            application.service(requirement)
        self.assertEqual(caught.exception.code, E.EXTENSION_INCOMPATIBLE)

    def test_entry_point_and_manifest_identity_mismatch_is_disabled(self) -> None:
        _install_fixture(
            self.site,
            name="mismatch",
            extension_id="vendor.entry",
            manifest_extension_id="vendor.manifest",
            provides=("cap.mismatch",),
        )
        application = self.app()
        self.assertEqual(self.status(application, "vendor.entry").state, "disabled")
        self.assertFalse(
            application.has(CapabilityRequirement(key=CapabilityKey("cap.mismatch")))
        )

    def test_duplicate_canonical_identity_disables_all_colliding_providers(self) -> None:
        _install_fixture(
            self.site,
            name="first_duplicate",
            extension_id="vendor.duplicate",
            provides=("cap.duplicate",),
        )
        _install_fixture(
            self.site,
            name="second_duplicate",
            extension_id="vendor.duplicate",
            provides=("cap.duplicate",),
        )
        application = self.app()
        self.assertEqual(self.status(application, "vendor.duplicate").state, "disabled")
        self.assertFalse(
            application.has(CapabilityRequirement(key=CapabilityKey("cap.duplicate")))
        )

    def test_dependent_uses_a_healthy_compatible_provider_when_another_fails(self) -> None:
        _install_fixture(
            self.site,
            name="first_provider",
            extension_id="vendor.a_fail",
            provides=("cap.shared",),
            activate_body="raise RuntimeError('first provider failed')",
        )
        _install_fixture(
            self.site,
            name="second_provider",
            extension_id="vendor.z_ok",
            provides=("cap.shared",),
        )
        _install_fixture(
            self.site,
            name="dependent_provider",
            extension_id="vendor.zz_dependent",
            requires_capabilities=("cap.shared",),
        )
        application = self.app()
        self.assertEqual(self.status(application, "vendor.a_fail").state, "failed")
        self.assertEqual(self.status(application, "vendor.z_ok").state, "active")
        self.assertEqual(self.status(application, "vendor.zz_dependent").state, "active")

    def test_multi_provider_order_is_stable_by_provider_id(self) -> None:
        _install_fixture(self.site, name="zeta", extension_id="vendor.zeta", provides=("cap.many",))
        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("cap.many",))
        application = self.app()
        services = application.services(
            CapabilityRequirement(key=CapabilityKey("cap.many"), multiplicity=Multiplicity.MANY)
        )
        self.assertEqual(len(services), 2)
        status = [
            s for s in application.capabilities() if str(s.key) == "cap.many"
        ][0]
        self.assertEqual(list(status.providers), sorted(status.providers))

    def test_singular_capability_with_several_providers_is_a_problem(self) -> None:
        _install_fixture(self.site, name="one", extension_id="vendor.one", provides=("cap.single",))
        _install_fixture(self.site, name="two", extension_id="vendor.two", provides=("cap.single",))
        application = self.app()
        with self.assertRaises(E.OrchestratorError) as caught:
            application.service(CapabilityRequirement(key=CapabilityKey("cap.single")))
        self.assertEqual(caught.exception.code, E.EXTENSION_INCOMPATIBLE)

    def test_absent_capability_request_is_a_structured_problem(self) -> None:
        with self.assertRaises(E.OrchestratorError) as caught:
            self.app().service(CapabilityRequirement(key=CapabilityKey("never.provided")))
        self.assertEqual(caught.exception.code, E.EXTENSION_INCOMPATIBLE)


class ExtensionContextTests(ExtensionBase):
    def test_extension_receives_only_its_own_configuration_namespace(self) -> None:
        _install_fixture(
            self.site, name="conf", extension_id="vendor.conf",
            activate_body=(
                'assert context.config() == {"retention": 7}, context.config();'
                ' assert "vendor.other" not in str(context.config())'
            ),
        )
        application = self.app(
            config_extra='\n[extensions."vendor.conf"]\nretention = 7\n'
            '\n[extensions."vendor.other"]\nsecret_like = "unrelated"\n'
        )
        self.assertEqual(self.status(application, "vendor.conf").state, "active")

    def test_prompt_event_reaches_only_an_explicit_subscriber(self) -> None:
        _install_fixture(
            self.site, name="sink", extension_id="vendor.sink",
            subscriptions=(("core.prompt.rendered.v1",),),
            activate_body=(
                "context.subscribe(('core.prompt.rendered.v1',),"
                " lambda event: ACTIVATED.append(event.event_type))"
            ),
        )
        _install_fixture(
            self.site, name="quiet", extension_id="vendor.quiet",
            activate_body=(
                "context.subscribe(('vendor.other.event.v1',),"
                " lambda event: ACTIVATED.append('WRONG'))"
            ),
        )
        application = self.app()
        from sdp_orchestrator.core._records import (
            ObservationPolicy,
            ProjectKey,
            PromptExecutionMode,
            PromptPreparationRequest,
            PromptRenderRequest,
            RemoteMode,
            StageSelector,
        )

        core = application.core()
        prepared = core.prepare(
            PromptPreparationRequest(
                project=ProjectKey("demo"),
                stage=StageSelector("implementation"),
                policy=ObservationPolicy(remote_mode=RemoteMode.LOCAL_ONLY),
            )
        )
        core.render(
            PromptRenderRequest(
                prepared=prepared, prompt_execution_mode=PromptExecutionMode.LOCAL
            )
        )
        sink = importlib.import_module("sdp_fixture_sink")
        quiet = importlib.import_module("sdp_fixture_quiet")
        self.assertIn("core.prompt.rendered.v1", sink.ACTIVATED)
        self.assertNotIn("WRONG", quiet.ACTIVATED)

    def test_extension_context_exposes_no_core_internals(self) -> None:
        _install_fixture(
            self.site, name="probe", extension_id="vendor.probe",
            activate_body=(
                "assert not hasattr(context, '_config');"
                " assert set(n for n in dir(context) if not n.startswith('_'))"
                " == {'core', 'config', 'register_service', 'subscribe',"
                " 'extension_id', 'core_spi_version'}, sorted(dir(context))"
            ),
        )
        self.assertEqual(self.status(self.app(), "vendor.probe").state, "active")


if __name__ == "__main__":
    unittest.main()


class PassiveDiagnosticsTests(ExtensionBase):
    """``doctor`` and ``capabilities`` must stay passive by default."""

    def setUp(self) -> None:
        super().setUp()
        # These commands report on stdout; the assertions are about side effects.
        self._quiet = contextlib.redirect_stdout(io.StringIO())
        self._quiet.__enter__()
        self.addCleanup(self._quiet.__exit__, None, None, None)

    def _repo_snapshot(self) -> dict[str, float]:
        return {
            str(path.relative_to(self.repo)): path.stat().st_mtime
            for path in sorted(self.repo.rglob("*"))
            if path.is_file()
        }

    def test_doctor_imports_no_provider_and_touches_no_repository(self) -> None:
        from sdp_orchestrator.core._cli import doctor_command

        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        before = self._repo_snapshot()
        doctor_command(config=str(self.config))
        self.assertEqual(self.imported(), [], "doctor must not import provider code")
        self.assertEqual(before, self._repo_snapshot(), "doctor must not touch the target")

    def test_capabilities_imports_no_provider_by_default(self) -> None:
        from sdp_orchestrator.core._cli import capabilities_command

        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        capabilities_command(config=str(self.config), load_extensions=False)
        self.assertEqual(self.imported(), [])

    def test_capabilities_loads_providers_only_when_asked(self) -> None:
        from sdp_orchestrator.core._cli import capabilities_command

        _install_fixture(self.site, name="alpha", extension_id="vendor.alpha", provides=("x.y",))
        capabilities_command(config=str(self.config), load_extensions=True)
        self.assertEqual(self.imported(), ["vendor.alpha"])

    def test_inactive_namespaces_are_diagnosed_without_interpretation(self) -> None:
        from sdp_orchestrator.core._config import load_config

        self.config.write_text(
            config_text(self.repo, extra='\n[extensions."never.installed"]\nweird = [1, 2]\nnested = { a = 2 }\n'),
            encoding="utf-8",
        )
        config = load_config(str(self.config))
        self.assertIn("never.installed", config.extension_namespaces)
