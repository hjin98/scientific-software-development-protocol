"""Application composition: the one extension registry and service registry.

Extensions are discovered through exactly one Python entry-point group,
``sdp_orchestrator.extensions.v1``. There is no directory scanning and no
repository-loaded plugin path.

Two activation policies exist, and the difference is a security boundary, not a
performance tweak:

``discovery_only``
    Reads installed distribution/entry-point *metadata* only. It never imports or
    executes third-party provider code, so it cannot observe a provider's
    manifest -- and therefore never claims capabilities or health it did not see.
    ``sdp doctor`` and ``sdp capabilities`` default here, which is what makes them
    genuinely free of hidden loading, network access, and mutation.

``normal``
    Imports providers, reads their manifests, resolves dependencies
    topologically, and activates them. Installed entry-point code is trusted
    in-process code; Core does not sandbox it. A failing or incompatible optional
    provider disables itself and its dependents while healthy Core services stay
    up.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import metadata
from typing import Any, Iterable

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from . import _errors as E
from ._config import CoreConfig, load_config
from ._events import EventBus
from ._records import (
    ActivationPolicy,
    ApplicationRequest,
    CapabilityKey,
    CapabilityRequirement,
    CapabilityStatus,
    ExtensionId,
    ExtensionManifest,
    ExtensionRegistration,
    ExtensionStatus,
    Multiplicity,
)
from ._service import CoreService

ENTRY_POINT_GROUP = "sdp_orchestrator.extensions.v1"
CORE_SPI_VERSION = "1.0.0"

#: Capabilities Core itself provisions.
CORE_CAPABILITIES: tuple[CapabilityKey, ...] = (
    CapabilityKey("prompt.render"),
    CapabilityKey("project.observe"),
    CapabilityKey("workplan.catalog"),
    CapabilityKey("workflow.profile"),
)


@dataclass
class _Registration:
    extension_id: str
    services: dict[CapabilityKey, tuple[object, int]] = field(default_factory=dict)


class ExtensionContext:
    """The only surface a provider receives.

    It exposes versioned Core services, the extension's *own* configuration
    namespace, and bounded registrars -- never Core internals, other extensions'
    configuration, or the raw configuration document.
    """

    def __init__(
        self,
        *,
        extension_id: str,
        core: CoreService,
        config_namespace: dict[str, Any],
        events: EventBus,
        registry: "_ServiceRegistry",
    ) -> None:
        self.extension_id = extension_id
        self.core_spi_version = CORE_SPI_VERSION
        self._core = core
        self._config_namespace = dict(config_namespace)
        self._events = events
        self._registry = registry

    def core(self) -> CoreService:
        return self._core

    def config(self) -> dict[str, Any]:
        return dict(self._config_namespace)

    def register_service(self, key: CapabilityKey, api_major: int, service: object) -> None:
        self._registry.register(self.extension_id, key, api_major, service)

    def subscribe(self, event_types: Iterable[str], sink: Any) -> None:
        self._events.subscribe(tuple(event_types), sink, self.extension_id)


class _ServiceRegistry:
    def __init__(self) -> None:
        self._entries: dict[CapabilityKey, list[tuple[str, int, object]]] = {}

    def register(
        self, provider: str, key: CapabilityKey, api_major: int, service: object
    ) -> None:
        entries = self._entries.setdefault(key, [])
        entries.append((provider, api_major, service))
        entries.sort(key=lambda item: item[0])

    def providers(self, key: CapabilityKey) -> list[tuple[str, int, object]]:
        return list(self._entries.get(key, ()))

    def keys(self) -> list[CapabilityKey]:
        return sorted(self._entries)


class Application:
    """Concrete ``ApplicationAPI`` v1."""

    def __init__(
        self,
        *,
        config: CoreConfig,
        core: CoreService,
        registry: _ServiceRegistry,
        events: EventBus,
        extensions: tuple[ExtensionStatus, ...],
        policy: ActivationPolicy,
    ) -> None:
        self._config = config
        self._core = core
        self._registry = registry
        self._events = events
        self._extensions = extensions
        self._policy = policy

    # -- introspection ----------------------------------------------------

    def core(self) -> CoreService:
        return self._core

    def config(self) -> CoreConfig:
        return self._config

    def events(self) -> EventBus:
        return self._events

    def activation_policy(self) -> ActivationPolicy:
        return self._policy

    def extensions(self) -> tuple[ExtensionStatus, ...]:
        return self._extensions

    def capabilities(self) -> tuple[CapabilityStatus, ...]:
        statuses = [
            CapabilityStatus(
                key=key,
                state="active",
                api_major=1,
                providers=("sdp.core",),
                detail="provisioned by sdp-orchestrator-core",
            )
            for key in CORE_CAPABILITIES
        ]
        for key in self._registry.keys():
            providers = self._registry.providers(key)
            statuses.append(
                CapabilityStatus(
                    key=key,
                    state="active",
                    api_major=providers[0][1] if providers else None,
                    providers=tuple(provider for provider, _, _ in providers),
                )
            )
        if self._policy is ActivationPolicy.DISCOVERY_ONLY:
            for status in self._extensions:
                statuses.append(
                    CapabilityStatus(
                        key=CapabilityKey(f"extension:{status.extension_id}"),
                        state="discovered",
                        api_major=None,
                        providers=(str(status.extension_id),),
                        detail=(
                            "discovered from installed entry-point metadata; provider not loaded, "
                            "so its capabilities and health are unobserved"
                        ),
                    )
                )
        return tuple(statuses)

    def has(self, requirement: CapabilityRequirement) -> bool:
        if requirement.key in CORE_CAPABILITIES:
            return True
        return bool(self._registry.providers(requirement.key))

    def service(self, requirement: CapabilityRequirement) -> object:
        if requirement.key in CORE_CAPABILITIES:
            return self._core
        providers = self._registry.providers(requirement.key)
        if not providers:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                f"no provider supplies capability {requirement.key!r}",
                details={"capability": str(requirement.key)},
            )
        if len(providers) > 1 and requirement.multiplicity is Multiplicity.SINGULAR:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                f"capability {requirement.key!r} has several providers but was requested as singular",
                details={"providers": [name for name, _, _ in providers]},
            )
        return providers[0][2]

    def services(self, requirement: CapabilityRequirement) -> tuple[object, ...]:
        if requirement.key in CORE_CAPABILITIES:
            return (self._core,)
        return tuple(service for _, _, service in self._registry.providers(requirement.key))


# --------------------------------------------------------------------------
# Discovery and activation
# --------------------------------------------------------------------------


def _entry_points() -> list[metadata.EntryPoint]:
    try:
        return sorted(metadata.entry_points(group=ENTRY_POINT_GROUP), key=lambda ep: ep.name)
    except Exception:  # noqa: BLE001 - a broken installation must not crash Core
        return []


def discover() -> tuple[ExtensionStatus, ...]:
    """Read installed entry-point metadata without importing any provider."""

    statuses: list[ExtensionStatus] = []
    for entry in _entry_points():
        distribution = getattr(entry, "dist", None)
        statuses.append(
            ExtensionStatus(
                extension_id=ExtensionId(entry.name),
                state="discovered",
                distribution=getattr(distribution, "name", None),
                entry_point=entry.value,
                version=getattr(distribution, "version", None),
                detail="entry-point metadata only; provider code was not imported",
            )
        )
    return tuple(statuses)


def _check_spi(manifest: ExtensionManifest) -> None:
    if not manifest.core_spi_spec:
        return
    try:
        specifier = SpecifierSet(manifest.core_spi_spec)
    except InvalidSpecifier:
        E.fail(
            E.EXTENSION_INCOMPATIBLE,
            "an extension declares an unparseable Core SPI specifier",
            details={"extension": str(manifest.extension_id), "spec": manifest.core_spi_spec},
        )
    try:
        current = Version(CORE_SPI_VERSION)
    except InvalidVersion:  # pragma: no cover - constant is valid
        return
    if current not in specifier:
        E.fail(
            E.EXTENSION_INCOMPATIBLE,
            "an extension requires an incompatible Core SPI version",
            details={
                "extension": str(manifest.extension_id),
                "requires": manifest.core_spi_spec,
                "core_spi": CORE_SPI_VERSION,
            },
        )


def _topological_order(
    manifests: dict[str, ExtensionManifest],
) -> list[str]:
    """Order providers so every declared dependency activates first."""

    provided: dict[str, str] = {}
    for name, manifest in manifests.items():
        for provision in manifest.provides_capabilities:
            provided.setdefault(str(provision.key), name)

    pending = dict(manifests)
    ordered: list[str] = []
    while pending:
        ready = []
        for name, manifest in pending.items():
            deps = {str(dep) for dep in manifest.requires_extensions}
            deps |= {
                provided[str(req.key)]
                for req in manifest.requires_capabilities
                if str(req.key) in provided
            }
            deps &= set(manifests)
            if deps <= set(ordered):
                ready.append(name)
        if not ready:
            E.fail(
                E.EXTENSION_DEPENDENCY_CYCLE,
                "extension dependencies form a cycle",
                details={"unresolved": sorted(pending)},
            )
        for name in sorted(ready):
            ordered.append(name)
            pending.pop(name)
    return ordered


def _activate(
    config: CoreConfig, core: CoreService, events: EventBus, registry: _ServiceRegistry
) -> tuple[ExtensionStatus, ...]:
    statuses: dict[str, ExtensionStatus] = {}
    manifests: dict[str, ExtensionManifest] = {}
    providers: dict[str, Any] = {}

    for entry in _entry_points():
        distribution = getattr(entry, "dist", None)
        base = {
            "distribution": getattr(distribution, "name", None),
            "entry_point": entry.value,
            "version": getattr(distribution, "version", None),
        }
        try:
            provider = entry.load()
            manifest = provider.manifest()
            if not isinstance(manifest, ExtensionManifest):
                raise TypeError("manifest() did not return an ExtensionManifest")
            _check_spi(manifest)
        except E.OrchestratorError as exc:
            statuses[entry.name] = ExtensionStatus(
                extension_id=ExtensionId(entry.name),
                state="disabled",
                detail=f"{exc.problem.code}: {exc.problem.message}",
                **base,
            )
            continue
        except Exception as exc:  # noqa: BLE001 - a bad provider must not break Core
            statuses[entry.name] = ExtensionStatus(
                extension_id=ExtensionId(entry.name),
                state="failed",
                detail=f"{type(exc).__name__}: {exc}",
                **base,
            )
            continue
        manifests[entry.name] = manifest
        providers[entry.name] = provider
        statuses[entry.name] = ExtensionStatus(
            extension_id=ExtensionId(entry.name), state="discovered", **base
        )

    if not manifests:
        return tuple(statuses[name] for name in sorted(statuses))

    try:
        order = _topological_order(manifests)
    except E.OrchestratorError as exc:
        for name in manifests:
            statuses[name] = statuses[name].model_copy(
                update={"state": "disabled", "detail": f"{exc.problem.code}: {exc.problem.message}"}
            )
        return tuple(statuses[name] for name in sorted(statuses))

    activated: set[str] = set()
    for name in order:
        manifest = manifests[name]
        missing = [
            str(req.key)
            for req in manifest.requires_capabilities
            if not registry.providers(req.key) and req.key not in CORE_CAPABILITIES
        ]
        unsatisfied = [dep for dep in manifest.requires_extensions if dep not in activated]
        if missing or unsatisfied:
            statuses[name] = statuses[name].model_copy(
                update={
                    "state": "disabled",
                    "detail": (
                        "unsatisfied requirements: "
                        f"capabilities={sorted(missing)} extensions={sorted(unsatisfied)}"
                    ),
                }
            )
            continue
        context = ExtensionContext(
            extension_id=name,
            core=core,
            config_namespace=config.extension_namespaces.get(str(manifest.extension_id), {}),
            events=events,
            registry=registry,
        )
        try:
            registration = providers[name].activate(context)
            if registration is not None and not isinstance(registration, ExtensionRegistration):
                raise TypeError("activate() did not return an ExtensionRegistration")
        except Exception as exc:  # noqa: BLE001 - optional provider failure degrades locally
            statuses[name] = statuses[name].model_copy(
                update={"state": "failed", "detail": f"{type(exc).__name__}: {exc}"}
            )
            continue
        activated.add(name)
        statuses[name] = statuses[name].model_copy(
            update={"state": "active", "detail": "activated"}
        )
    return tuple(statuses[name] for name in sorted(statuses))


def create_application(request: ApplicationRequest | None = None) -> Application:
    """Compose Core, then apply the requested activation policy."""

    req = request or ApplicationRequest()
    config = load_config(req.config_path)
    events = EventBus()
    core = CoreService(config, events)
    registry = _ServiceRegistry()

    if req.activation_policy is ActivationPolicy.DISCOVERY_ONLY:
        extensions = discover()
    else:
        extensions = _activate(config, core, events, registry)

    return Application(
        config=config,
        core=core,
        registry=registry,
        events=events,
        extensions=extensions,
        policy=req.activation_policy,
    )
