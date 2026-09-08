"""The single Core error contract.

Callers branch on :attr:`Problem.code`. There is intentionally no exception
subclass hierarchy mirroring the code list: codes are data, and a parallel class
tree would become a second authority that drifts from the documented contract.
"""

from __future__ import annotations

from typing import Any, Mapping, NoReturn

from .redaction import redact_details, redact_text

# --- configuration / project ---
CONFIG_INVALID = "core.config.invalid"
PROJECT_NOT_FOUND = "core.project.not_found"
PROJECT_AMBIGUOUS = "core.project.ambiguous"
REPOSITORY_INVALID = "core.repository.invalid"
CONTEXT_STALE = "core.context.stale"

# --- workplans ---
WORKPLAN_REQUIRED = "core.workplan.required"
WORKPLAN_NOT_FOUND = "core.workplan.not_found"
WORKPLAN_AMBIGUOUS = "core.workplan.ambiguous"
WORKPLAN_DISALLOWED = "core.workplan.disallowed"

# --- protocol source / profile ---
PROTOCOL_INCOMPATIBLE = "core.protocol.incompatible"
PROTOCOL_UNAVAILABLE = "core.protocol.unavailable"
PROTOCOL_SOURCE_INCOHERENT = "core.protocol.source_incoherent"

# --- stage ---
STAGE_UNKNOWN = "core.stage.unknown"

# --- remote observation ---
REMOTE_UNAVAILABLE = "core.remote.unavailable"
REMOTE_AMBIGUOUS = "core.remote.ambiguous"
REMOTE_LOCAL_ONLY = "core.remote.local_only"
REMOTE_STALE = "core.remote.stale"
REMOTE_TARGET_UNAVAILABLE = "core.remote.target_unavailable"

# --- prompt ---
PROMPT_MODE_INVALID = "core.prompt.mode_invalid"
PROMPT_INPUT_REQUIRED = "core.prompt.input_required"
PROMPT_INPUT_UNKNOWN = "core.prompt.input_unknown"
PROMPT_INPUT_CONFLICT = "core.prompt.input_conflict"
PROMPT_INPUT_INVALID = "core.prompt.input_invalid"

# --- extensions / misc ---
EXTENSION_INCOMPATIBLE = "core.extension.incompatible"
EXTENSION_ACTIVATION_FAILED = "core.extension.activation_failed"
EXTENSION_DEPENDENCY_CYCLE = "core.extension.dependency_cycle"
CLIPBOARD_UNAVAILABLE = "core.clipboard.unavailable"

ERROR_CODES: tuple[str, ...] = (
    CONFIG_INVALID,
    PROJECT_NOT_FOUND,
    PROJECT_AMBIGUOUS,
    REPOSITORY_INVALID,
    CONTEXT_STALE,
    WORKPLAN_REQUIRED,
    WORKPLAN_NOT_FOUND,
    WORKPLAN_AMBIGUOUS,
    WORKPLAN_DISALLOWED,
    PROTOCOL_INCOMPATIBLE,
    PROTOCOL_UNAVAILABLE,
    PROTOCOL_SOURCE_INCOHERENT,
    STAGE_UNKNOWN,
    REMOTE_UNAVAILABLE,
    REMOTE_AMBIGUOUS,
    REMOTE_LOCAL_ONLY,
    REMOTE_STALE,
    REMOTE_TARGET_UNAVAILABLE,
    PROMPT_MODE_INVALID,
    PROMPT_INPUT_REQUIRED,
    PROMPT_INPUT_UNKNOWN,
    PROMPT_INPUT_CONFLICT,
    PROMPT_INPUT_INVALID,
    EXTENSION_INCOMPATIBLE,
    EXTENSION_ACTIVATION_FAILED,
    EXTENSION_DEPENDENCY_CYCLE,
    CLIPBOARD_UNAVAILABLE,
)

_JSON_SCALARS = (str, int, float, bool, type(None))


def _json_safe(value: Any, depth: int = 0) -> Any:
    """Coerce a diagnostic payload into JSON-compatible data.

    Anything that is not already a JSON scalar/container becomes its ``repr``:
    ``Problem`` must never smuggle a live implementation object across the
    public boundary.
    """

    if depth > 8:
        return "<truncated>"
    if isinstance(value, _JSON_SCALARS):
        return value
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v, depth + 1) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_safe(item, depth + 1) for item in value]
    return repr(value)


class Problem:
    """Structured, redacted, JSON-safe description of a Core failure."""

    __slots__ = ("code", "message", "retryable", "details", "remediation")

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool | None = None,
        details: Mapping[str, Any] | None = None,
        remediation: str | None = None,
    ) -> None:
        self.code = code
        self.message = redact_text(message)
        self.retryable = retryable
        self.details: dict[str, Any] = dict(
            redact_details(_json_safe(dict(details or {})))  # type: ignore[arg-type]
        )
        self.remediation = redact_text(remediation) if remediation else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
            "details": self.details,
            "remediation": self.remediation,
        }

    def __repr__(self) -> str:  # pragma: no cover - diagnostic only
        return f"Problem(code={self.code!r}, message={self.message!r})"


class OrchestratorError(Exception):
    """The one exception type raised across the Core public API."""

    def __init__(self, problem: Problem) -> None:
        super().__init__(f"{problem.code}: {problem.message}")
        self.problem = problem

    @property
    def code(self) -> str:
        return self.problem.code


def fail(
    code: str,
    message: str,
    *,
    retryable: bool | None = None,
    details: Mapping[str, Any] | None = None,
    remediation: str | None = None,
) -> NoReturn:
    raise OrchestratorError(
        Problem(
            code,
            message,
            retryable=retryable,
            details=details,
            remediation=remediation,
        )
    )
