"""Version-selected extraction of canonical Protocol prompt bodies.

The parser remains deliberately strict: every profile definition owns an exact
numbered stage set and each stage owns exactly one fenced ``text`` block. A
source that cannot be mapped unambiguously to its declared profile fails loudly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import errors as E
from .digest import SCHEME_CONTENT, digest_bytes
from .limits import MAX_PROTOCOL_SOURCE_BYTES
from .records import DigestRef

LEGACY_PROFILE_ID = "sdp-protocol-5.16"
SSDP6_PROFILE_ID = "ssdp-protocol-6.0"
SSDP61_PROFILE_ID = "ssdp-protocol-6.1"
SSDP62_PROFILE_ID = "ssdp-protocol-6.2"
SSDP63_PROFILE_ID = "ssdp-protocol-6.3"

# Kept as the legacy compatibility name because existing Core v1 tests and
# consumers import CANONICAL_STAGES directly.
CANONICAL_STAGES: tuple[tuple[int, str, str], ...] = (
    (0, "baseline", "Baseline / Change-Health Intake"),
    (1, "design", "Design / Workplan"),
    (2, "implementation", "Implementation"),
    (3, "review", "Review & Update"),
    (4, "verification", "Verification"),
    (5, "stabilization", "Stabilization / Architecture GC"),
    (6, "alignment", "Alignment of a Downstream Workplan"),
    (7, "health-audit", "Health Audit"),
    (8, "closeout", "Closeout"),
)

SSDP6_STAGES: tuple[tuple[int, str, str], ...] = (
    (0, "intake", "Authority / Affected-Domain Intake"),
    (1, "scientific-formulation", "D1 Scientific & Mathematical Formulation"),
    (2, "numerical-algorithm-design", "D2 Algorithm & Numerical Method Design"),
    (3, "software-design", "D3 Software Architecture / Workplan"),
    (4, "software-implementation", "D4 Software Implementation"),
    (5, "review", "Review & Challenge Pass"),
    (6, "verification", "Verification"),
    (7, "stabilization", "Stabilization / Architecture GC"),
    (8, "alignment", "Downstream Authority Alignment"),
    (9, "health-audit", "Health Audit"),
    (10, "closeout", "Closeout"),
)

_PROFILE_STAGES = {
    LEGACY_PROFILE_ID: CANONICAL_STAGES,
    SSDP6_PROFILE_ID: SSDP6_STAGES,
    SSDP61_PROFILE_ID: SSDP6_STAGES,
    SSDP62_PROFILE_ID: SSDP6_STAGES,
    SSDP63_PROFILE_ID: SSDP6_STAGES,
}

_HEADING = re.compile(r"^##\s+(?:(?P<number>\d+)\.\s+)?(?P<title>.+?)\s*$")
_FENCE = re.compile(r"^```(?P<info>[A-Za-z0-9_-]*)\s*$")
_INPUT_LINE = re.compile(r"^(?P<name>[A-Z][A-Z0-9_]*)\s*=\s*(?P<spec>.*)$")


@dataclass(frozen=True)
class CanonicalStage:
    stage_key: str
    heading_number: int
    title: str
    body: str
    input_names: tuple[str, ...]


@dataclass(frozen=True)
class CanonicalDocument:
    text: str
    content_digest: DigestRef
    stages: dict[str, CanonicalStage]
    profile_id: str = LEGACY_PROFILE_ID


def stages_for_profile(profile_id: str) -> tuple[tuple[int, str, str], ...]:
    try:
        return _PROFILE_STAGES[profile_id]
    except KeyError:
        E.fail(
            E.PROTOCOL_INCOMPATIBLE,
            "no canonical stage definition is available for the requested profile",
            details={"requested": profile_id, "available": sorted(_PROFILE_STAGES)},
        )


def all_stage_keys() -> tuple[str, ...]:
    """Union of CLI-safe stage keys across supported profiles, preserving order."""

    seen: list[str] = []
    for profile_id in (
        LEGACY_PROFILE_ID,
        SSDP6_PROFILE_ID,
        SSDP61_PROFILE_ID,
        SSDP62_PROFILE_ID,
        SSDP63_PROFILE_ID,
    ):
        for _, key, _ in _PROFILE_STAGES[profile_id]:
            if key not in seen:
                seen.append(key)
    return tuple(seen)


def _fail_incoherent(message: str, **details: object) -> None:
    E.fail(E.PROTOCOL_SOURCE_INCOHERENT, message, details=details)


def _sections(lines: list[str]) -> dict[tuple[int, str], tuple[int, int]]:
    starts: list[tuple[int, int | None, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not line.startswith("## "):
            continue
        match = _HEADING.match(line)
        if not match:
            continue
        number = int(match.group("number")) if match.group("number") else None
        starts.append((index, number, match.group("title")))

    spans: dict[tuple[int, str], tuple[int, int]] = {}
    for position, (index, number, title) in enumerate(starts):
        if number is None:
            continue
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        key = (number, title)
        if key in spans:
            _fail_incoherent(
                "the canonical source declares a duplicate stage heading",
                heading=f"{number}. {title}",
            )
        spans[key] = (index + 1, end)
    return spans


def _single_text_block(lines: list[str], span: tuple[int, int], heading: str) -> str:
    start, end = span
    blocks: list[str] = []
    index = start
    while index < end:
        match = _FENCE.match(lines[index])
        if not match:
            index += 1
            continue
        info = match.group("info")
        close = index + 1
        while close < end and not _FENCE.match(lines[close]):
            close += 1
        if close >= end:
            _fail_incoherent("an unterminated fenced block belongs to a stage heading", heading=heading)
        if info == "text":
            blocks.append("\n".join(lines[index + 1 : close]))
        index = close + 1
    if len(blocks) != 1:
        _fail_incoherent(
            "a canonical stage heading must own exactly one fenced text block",
            heading=heading,
            found=len(blocks),
        )
    return blocks[0]


def _input_names(body: str, heading: str) -> tuple[str, ...]:
    lines = body.splitlines()
    try:
        start = lines.index("INPUTS") + 1
    except ValueError:
        _fail_incoherent("a canonical stage body has no INPUTS block", heading=heading)
    names: list[str] = []
    for line in lines[start:]:
        if not line.strip():
            break
        match = _INPUT_LINE.match(line)
        if not match:
            _fail_incoherent(
                "a canonical INPUTS block contains an unrecognized line",
                heading=heading,
                line=line[:120],
            )
        name = match.group("name")
        if name in names:
            _fail_incoherent("a canonical INPUTS block declares a duplicate input", heading=heading, input=name)
        names.append(name)
    if not names:
        _fail_incoherent("a canonical INPUTS block is empty", heading=heading)
    return tuple(names)


def parse_document(text: str, *, profile_id: str = LEGACY_PROFILE_ID) -> CanonicalDocument:
    """Parse canonical workflow prose under one explicit profile definition."""

    encoded = text.encode("utf-8")
    if len(encoded) > MAX_PROTOCOL_SOURCE_BYTES:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the canonical prompt source exceeds the supported size bound",
            details={"bytes": len(encoded), "limit": MAX_PROTOCOL_SOURCE_BYTES},
        )
    stage_spec = stages_for_profile(profile_id)
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    spans = _sections(lines)
    expected_headings = {(number, title) for number, _, title in stage_spec}
    if set(spans) != expected_headings:
        _fail_incoherent(
            "the canonical source has extra, missing, or conflicting numbered stage headings",
            profile=profile_id,
            expected=sorted(f"{number}. {title}" for number, title in expected_headings),
            actual=sorted(f"{number}. {title}" for number, title in spans),
        )

    stages: dict[str, CanonicalStage] = {}
    for number, stage_key, title in stage_spec:
        span = spans[(number, title)]
        heading = f"{number}. {title}"
        body = _single_text_block(lines, span, heading)
        stages[stage_key] = CanonicalStage(
            stage_key=stage_key,
            heading_number=number,
            title=title,
            body=body,
            input_names=_input_names(body, heading),
        )
    return CanonicalDocument(
        text=text,
        content_digest=digest_bytes(encoded, SCHEME_CONTENT),
        stages=stages,
        profile_id=profile_id,
    )
