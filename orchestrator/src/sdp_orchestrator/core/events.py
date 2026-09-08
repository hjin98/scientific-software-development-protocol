"""Non-durable, explicitly subscribed event dispatch.

``core.prompt.rendered.v1`` carries the complete prompt text, so it is delivered
only to sinks that subscribed to that exact event type. There is no broadcast, no
queue, and no persistence: durable history belongs to Tracker, not Core.

Sinks are installed extension code and are therefore trusted; Core neither
sandboxes nor time-limits them. What Core does guarantee is that a failing sink
cannot counterfeit the primary result -- the prompt was already fully rendered
before any sink ran.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol

from .digest import sha256_hex
from .redaction import redact_text
from .records import EventEnvelope, EventId, ProjectKey, RunId

PROMPT_RENDERED_EVENT = "core.prompt.rendered.v1"
PROMPT_RENDERED_SCHEMA_VERSION = 1


class EventSink(Protocol):
    def __call__(self, event: EventEnvelope) -> None: ...


def logical_event_id(event_type: str, run_id: str, prompt_fingerprint: str) -> EventId:
    """Stable logical identity for one (event type, run, prompt) triple.

    Repeating a render for the same run and prompt yields the same EventId, so a
    duplicate-tolerant sink can deduplicate without Core keeping state.
    """

    return EventId(
        "evt-" + sha256_hex(f"{event_type}\n{run_id}\n{prompt_fingerprint}".encode("utf-8"))[:32]
    )


@dataclass
class EventBus:
    """Synchronous dispatcher with per-event-type subscriptions."""

    _sinks: list[tuple[tuple[str, ...], EventSink, str]] = field(default_factory=list)
    _failures: list[str] = field(default_factory=list)

    def subscribe(self, event_types: tuple[str, ...], sink: EventSink, owner: str) -> None:
        self._sinks.append((tuple(event_types), sink, owner))

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(self._failures)

    def publish(self, event: EventEnvelope) -> None:
        for event_types, sink, owner in self._sinks:
            if event.event_type not in event_types:
                continue
            try:
                sink(event)
            except Exception as exc:  # noqa: BLE001 - a sink must not break the primary result
                self._failures.append(
                    f"{owner}: {type(exc).__name__}: {redact_text(str(exc))}"
                )

    def build_prompt_event(
        self,
        *,
        project_key: ProjectKey,
        run_id: RunId,
        prompt_fingerprint: str,
        payload: dict[str, object],
    ) -> EventEnvelope:
        return EventEnvelope(
            event_id=logical_event_id(PROMPT_RENDERED_EVENT, run_id, prompt_fingerprint),
            event_type=PROMPT_RENDERED_EVENT,
            schema_version=PROMPT_RENDERED_SCHEMA_VERSION,
            occurred_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            project_key=project_key,
            run_id=run_id,
            producer_extension=None,
            payload=payload,
        )
