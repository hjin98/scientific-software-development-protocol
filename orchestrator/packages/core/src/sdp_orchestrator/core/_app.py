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
from typing import TYPE_CHECKING, Any, Iterable

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from . import _errors as E
from ._config import CoreConfig, load_config
from ._events import EventBus
from ._redact import redact_text
from ._records import (
    ActivationPolicy,
    ApplicationRequest,
    CapabilityKey,
    CapabilityProvision,
    CapabilityRequirement,
    CapabilityStatus,
    ExtensionId,
    ExtensionManifest,
    ExtensionRegistration,
    ExtensionStatus,
    Multiplicity,
)
from ._service import CoreService

if TYPE_CHECKING:
    from .api.v1 import ApplicationAPI, CoreAPI

ENTRY_POINT_GROUP = "sdp_orchestrator.extensions.v1"
CORE_SPI_VERSION = "1.0.0"

#: Capabilities Core itself provisions.
CORE_CAPABILITIES: tuple[CapabilityKey, ...] = (
    CapabilityKey("prompt.render"),
    CapabilityKey("project.observe"),
    CapabilityKey("workplan.catalog"),
    CapabilityKey("workflow.profile"),
)


def _api_spec_matches(api_major: int, api_spec: str) -> bool:
    if not api_spec:
        return True
    try:
        return Version(f"{api_major}.0.0") in SpecifierSet(api_spec)
    except (InvalidSpecifier, InvalidVersion):
        return False


def _provision_matches(
    requirement: CapabilityRequirement, provision: object
) -> bool:
    if not isinstance(provision, tuple):
        return False
    key, api_major, multiplicity = provision
    return (
        str(key) == str(requirement.key)
        and _api_spec_matches(api_major, requirement.api_spec)
        and (
            requirement.multiplicity is Multiplicity.MANY
            or multiplicity is Multiplicity.SINGULAR
        )
    )


@dataclass
class _Registration:
    extension_id: str
    services: dict[CapabilityKey, tuple[object, int]] = field(default_factory=dict)
    subscriptions: list[tuple[object, Any]] = field(default_factory=list)


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
        core: CoreAPI,
        config_namespace: dict[str, Any],
        events: Any,
        registry: Any,
    ) -> None:
        self.extension_id = extension_id
        self.core_spi_version = CORE_SPI_VERSION
        self._core = core
        self._config_namespace = dict(config_namespace)
        self._registration = registry

    def core(self) -> CoreAPI:
        return self._core

    def config(self) -> dict[str, Any]:
        return dict(self._config_namespace)

    def register_service(self, key: CapabilityKey, api_major: int, service: object) -> None:
        if key in CORE_CAPABILITIES:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                "an extension cannot replace a Core-owned capability",
                details={"extension": self.extension_id, "capability": str(key)},
            )
        if key in self._registration.services:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                "an extension registered the same capability more than once",
                details={"extension": self.extension_id, "capability": str(key)},
            )
        self._registration.services[key] = (service, api_major)

    def subscribe(self, event_types: Iterable[str], sink: Any) -> None:
        from ._records import EventSubscription

        subscription = EventSubscription(event_types=tuple(event_types))
        self._registration.subscriptions.append((subscription, sink))


class _ServiceRegistry:
    def __init__(self) -> None:
        self._entries: dict[CapabilityKey, list[tuple[str, int, object]]] = {}
        self._provisions: dict[tuple[CapabilityKey, str], Multiplicity] = {}

    def commit(
        self,
        provider: str,
        services: dict[CapabilityKey, tuple[object, int]],
        provisions: dict[CapabilityKey, Multiplicity],
    ) -> None:
        """Atomically publish one provider's staged service registrations."""

        entries = {key: list(values) for key, values in self._entries.items()}
        provision_meta = dict(self._provisions)
        for key, (service, api_major) in services.items():
            if key not in provisions:
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "an extension registered an undeclared capability",
                    details={"extension": provider, "capability": str(key)},
                )
            if any(existing[0] == provider for existing in entries.get(key, ())):
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "an extension published a capability more than once",
                    details={"extension": provider, "capability": str(key)},
                )
            entries.setdefault(key, []).append((provider, api_major, service))
            provision_meta[(key, provider)] = provisions[key]
        for values in entries.values():
            values.sort(key=lambda item: item[0])
        self._entries = entries
        self._provisions = provision_meta

    def providers(self, key: CapabilityKey) -> list[tuple[str, int, object]]:
        return list(self._entries.get(key, ()))

    def matching(self, requirement: CapabilityRequirement) -> list[tuple[str, int, object]]:
        return [
            entry
            for entry in self.providers(requirement.key)
            if _api_spec_matches(entry[1], requirement.api_spec)
            and (
                requirement.multiplicity is Multiplicity.MANY
                or self._provisions.get((requirement.key, entry[0]), Multiplicity.SINGULAR)
                is Multiplicity.SINGULAR
            )
        ]

    def keys(self) -> list[CapabilityKey]:
        return sorted(self._entries)


class Application:
    """Concrete ``ApplicationAPI`` v1."""

    def __init__(
        self,
        *,
        config: Any,
        core: CoreAPI,
        registry: Any,
        events: Any,
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

    def core(self) -> CoreAPI:
        return self._core

    def config(self) -> Any:
        return self._config

    def events(self) -> Any:
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
            return _api_spec_matches(1, requirement.api_spec)
        matching = self._registry.matching(requirement)
        return bool(matching) and (
            requirement.multiplicity is Multiplicity.MANY or len(matching) == 1
        )

    def service(self, requirement: CapabilityRequirement) -> object:
        if requirement.key in CORE_CAPABILITIES:
            if not _api_spec_matches(1, requirement.api_spec):
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    f"Core capability {requirement.key!r} does not satisfy the requested API",
                    details={"capability": str(requirement.key), "api_spec": requirement.api_spec},
                )
            return self._core
        providers = self._registry.matching(requirement)
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
            return (self._core,) if _api_spec_matches(1, requirement.api_spec) else ()
        return tuple(service for _, _, service in self._registry.matching(requirement))


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


def _validate_manifest(manifest: ExtensionManifest) -> dict[CapabilityKey, Multiplicity]:
    provisions: dict[CapabilityKey, Multiplicity] = {}
    for provision in manifest.provides_capabilities:
        if provision.key in CORE_CAPABILITIES:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                "an extension cannot declare a Core-owned capability",
                details={"extension": str(manifest.extension_id), "capability": str(provision.key)},
            )
        if provision.key in provisions:
            E.fail(
                E.EXTENSION_INCOMPATIBLE,
                "an extension declares the same capability more than once",
                details={"extension": str(manifest.extension_id), "capability": str(provision.key)},
            )
        provisions[provision.key] = provision.multiplicity
    for requirement in manifest.requires_capabilities:
        if requirement.api_spec:
            try:
                SpecifierSet(requirement.api_spec)
            except InvalidSpecifier:
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "an extension declares an unparseable capability API specifier",
                    details={
                        "extension": str(manifest.extension_id),
                        "capability": str(requirement.key),
                    },
                )
    return provisions


def _topological_order(
    manifests: dict[str, ExtensionManifest],
) -> list[str]:
    """Order providers so every declared dependency activates first."""

    provided: list[tuple[str, CapabilityProvision]] = [
        (name, provision)
        for name, manifest in manifests.items()
        for provision in manifest.provides_capabilities
    ]

    pending = dict(manifests)
    ordered: list[str] = []
    while pending:
        ready = []
        for name, manifest in pending.items():
            deps = {str(dep) for dep in manifest.requires_extensions}
            deps |= {
                provider
                for req in manifest.requires_capabilities
                for provider, provision in provided
                if _provision_matches(
                    req,
                    (provision.key, provision.api_major, provision.multiplicity),
                )
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


def _requirement_satisfied(
    requirement: CapabilityRequirement, _core: CoreService, registry: _ServiceRegistry
) -> bool:
    if requirement.key in CORE_CAPABILITIES:
        return _api_spec_matches(1, requirement.api_spec)
    matching = registry.matching(requirement)
    return bool(matching) and (
        requirement.multiplicity is Multiplicity.MANY or len(matching) == 1
    )


def _activate(
    config: CoreConfig, core: CoreService, events: EventBus, registry: _ServiceRegistry
) -> tuple[ExtensionStatus, ...]:
    statuses: dict[str, ExtensionStatus] = {}
    manifests: dict[str, ExtensionManifest] = {}
    providers: dict[str, Any] = {}
    provisions: dict[str, dict[CapabilityKey, Multiplicity]] = {}
    invalid_ids: set[str] = set()

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
            canonical_id = str(manifest.extension_id)
            if canonical_id in invalid_ids:
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "several installed entry points declare the same canonical extension identity",
                    details={"extension": canonical_id},
                )
            if canonical_id in manifests:
                invalid_ids.add(canonical_id)
                manifests.pop(canonical_id, None)
                providers.pop(canonical_id, None)
                provisions.pop(canonical_id, None)
                prior = statuses.get(canonical_id)
                if prior is not None:
                    statuses[canonical_id] = prior.model_copy(
                        update={
                            "state": "disabled",
                            "detail": (
                                "core.extension.incompatible: several installed entry points "
                                "declare the same canonical extension identity"
                            ),
                        }
                    )
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "several installed entry points declare the same canonical extension identity",
                    details={"extension": canonical_id},
                )
            if canonical_id != entry.name:
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "the installed entry-point name does not match the provider manifest identity",
                    details={"entry_point": entry.name, "manifest_extension": canonical_id},
                )
            _check_spi(manifest)
            manifest_provisions = _validate_manifest(manifest)
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
                detail=f"{type(exc).__name__}: {redact_text(str(exc))}",
                **base,
            )
            continue
        manifests[canonical_id] = manifest
        providers[canonical_id] = provider
        provisions[canonical_id] = manifest_provisions
        statuses[canonical_id] = ExtensionStatus(
            extension_id=ExtensionId(canonical_id), state="discovered", **base
        )

    if not manifests:
        return tuple(statuses[name] for name in sorted(statuses))

    try:
        order = _topological_order(manifests)
    except E.OrchestratorError as exc:
        for name in manifests:
            statuses[name] = statuses[name].model_copy(
                update={
                    "state": "disabled",
                    "detail": f"{exc.problem.code}: {exc.problem.message}",
                }
            )
        return tuple(statuses[name] for name in sorted(statuses))

    activated: set[str] = set()
    for name in order:
        manifest = manifests[name]
        missing = [
            str(req.key)
            for req in manifest.requires_capabilities
            if not _requirement_satisfied(req, core, registry)
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
            registry=_Registration(name),
        )
        try:
            registration = providers[name].activate(context)
            if registration is None:
                registration = ExtensionRegistration()
            if registration is not None and not isinstance(registration, ExtensionRegistration):
                raise TypeError("activate() did not return an ExtensionRegistration")
            staged = context._registration
            declared_services = {
                (str(key), api_major)
                for key, (_, api_major) in staged.services.items()
            }
            returned_services = {
                (str(key), api_major) for key, api_major in registration.services
            }
            manifest_services = {
                (str(key), api_major)
                for key, api_major in (
                    (provision.key, provision.api_major)
                    for provision in manifest.provides_capabilities
                )
            }
            if (
                len(returned_services) != len(registration.services)
                or declared_services != manifest_services
                or returned_services != declared_services
            ):
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "provider service declarations do not reconcile with its manifest and staged services",
                    details={"extension": name},
                )
            pending_subscription_types = sorted(
                tuple(subscription.event_types)
                for subscription, _ in staged.subscriptions
            )
            returned_subscription_types = sorted(
                tuple(subscription.event_types) for subscription in registration.subscriptions
            )
            if pending_subscription_types != returned_subscription_types:
                E.fail(
                    E.EXTENSION_INCOMPATIBLE,
                    "provider event subscriptions do not reconcile with its staged subscriptions",
                    details={"extension": name},
                )
            registry.commit(name, staged.services, provisions[name])
            for subscription, sink in staged.subscriptions:
                events.subscribe(subscription.event_types, sink, name)
        except Exception as exc:  # noqa: BLE001 - optional provider failure degrades locally
            if isinstance(exc, E.OrchestratorError):
                state = "disabled"
                detail = f"{exc.problem.code}: {exc.problem.message}"
            else:
                state = "failed"
                detail = f"{type(exc).__name__}: {redact_text(str(exc))}"
            statuses[name] = statuses[name].model_copy(
                update={"state": state, "detail": detail}
            )
            continue
        activated.add(name)
        statuses[name] = statuses[name].model_copy(
            update={"state": "active", "detail": "activated"}
        )
    return tuple(statuses[name] for name in sorted(statuses))


def create_application(request: ApplicationRequest | None = None) -> ApplicationAPI:
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
