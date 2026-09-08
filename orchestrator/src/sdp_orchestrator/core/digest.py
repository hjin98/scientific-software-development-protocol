"""Versioned canonicalization and digest construction.

Every domain digest names the scheme that produced it. A scheme is a frozen
contract: changing what it hashes requires a new scheme name, never a silent
redefinition, because higher modules compare digests across releases.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .records import DigestRef

ALGORITHM = "sha256"

SCHEME_PROMPT_PREPARATION = "sdp.prompt-preparation.v1"
SCHEME_PROMPT_FINGERPRINT = "sdp.prompt-fingerprint.v1"
SCHEME_WORKPLAN_SEMANTIC = "sdp.workplan-semantic.v1"
SCHEME_WORKPLAN_ARTIFACT = "sdp.workplan-artifact.v1"
SCHEME_GIT_WORKING_TREE = "sdp.git-working-tree.v1"
SCHEME_CONFIG = "sdp.core-config.v1"
SCHEME_CONTENT = "sdp.content.v1"


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize ``value`` to the frozen canonical JSON byte form.

    Frozen for v1: UTF-8, sorted keys, ``(",", ":")`` separators, non-ASCII kept
    literal, no trailing newline.
    """

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_bytes(data: bytes, scheme: str | None = None) -> DigestRef:
    return DigestRef(
        algorithm=ALGORITHM, canonicalization_scheme=scheme, value=sha256_hex(data)
    )


def digest_canonical(value: Any, scheme: str) -> DigestRef:
    return digest_bytes(canonical_json_bytes(value), scheme)
