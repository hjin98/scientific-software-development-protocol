"""``sdp_orchestrator.core.spi.v1`` -- the public Core provider SPI.

An extension is discovered through the single entry-point group
:data:`ENTRY_POINT_GROUP` and implements :class:`ExtensionProvider`.
``manifest()`` must be side-effect minimal: Core calls it before deciding whether
the provider may activate at all.

Providers receive only :class:`ExtensionContext`, which exposes versioned Core
services, the extension's own configuration namespace, and bounded registrars.
Event subscriptions are explicit -- a prompt-bearing event reaches only sinks that
asked for that event type by name.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..application import CORE_SPI_VERSION, ENTRY_POINT_GROUP, ExtensionContext
from ..records import (
    CapabilityKey,
    CapabilityProvision,
    CapabilityRequirement,
    EventEnvelope,
    EventSubscription,
    ExtensionId,
    ExtensionManifest,
    ExtensionRegistration,
    Multiplicity,
)

SPI_MAJOR = 1


@runtime_checkable
class ExtensionProvider(Protocol):
    def manifest(self) -> ExtensionManifest: ...

    def activate(self, context: ExtensionContext) -> ExtensionRegistration: ...


@runtime_checkable
class EventSink(Protocol):
    def __call__(self, event: EventEnvelope) -> None: ...


__all__ = [
    "CORE_SPI_VERSION",
    "ENTRY_POINT_GROUP",
    "CapabilityKey",
    "CapabilityProvision",
    "CapabilityRequirement",
    "EventEnvelope",
    "EventSink",
    "EventSubscription",
    "ExtensionContext",
    "ExtensionId",
    "ExtensionManifest",
    "ExtensionProvider",
    "ExtensionRegistration",
    "Multiplicity",
    "SPI_MAJOR",
]
