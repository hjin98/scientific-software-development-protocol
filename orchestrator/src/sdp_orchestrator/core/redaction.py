"""Credential redaction for anything that may reach a user-facing surface.

This is deliberately *not* a general secret scanner. It removes the two credential
carriers Core itself can produce mechanically -- URL userinfo and Git ``askpass``
style prompts -- and nothing else. Explicit user-authored text is intentional
content and is never scrubbed (see architecture 16 and workplan 3.9).
"""

from __future__ import annotations

import re

_URL_USERINFO = re.compile(
    r"(?P<scheme>[A-Za-z][A-Za-z0-9+.\-]*://)(?P<userinfo>[^/@\s]+)@(?P<host>[^\s/]+)"
)
_REDACTED = "<redacted>"


def sanitize_url(url: str) -> str:
    """Return ``url`` with any userinfo component replaced by a redaction marker."""

    def _sub(match: re.Match[str]) -> str:
        return f"{match.group('scheme')}{_REDACTED}@{match.group('host')}"

    return _URL_USERINFO.sub(_sub, url)


def redact_text(text: str) -> str:
    """Redact credential-bearing material from free-form diagnostic text."""

    return sanitize_url(text)


def redact_details(details: object) -> object:
    """Recursively redact a JSON-compatible diagnostic payload."""

    if isinstance(details, str):
        return redact_text(details)
    if isinstance(details, dict):
        return {str(key): redact_details(value) for key, value in details.items()}
    if isinstance(details, (list, tuple)):
        return [redact_details(item) for item in details]
    return details
