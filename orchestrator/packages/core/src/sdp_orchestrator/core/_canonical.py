"""Extraction of canonical stage prose from the SDP workflow-prompt document.

There is exactly one prompt-body authority: the canonical
``source/shared/references/development-workflow-prompts.md`` document (or a
reproducible version-bound snapshot of it). This module reads that document; it
never paraphrases, rewrites, or supplements it.

Extraction is deliberately brittle about structure. A stage heading must be
unique and must own exactly one fenced ``text`` block. If the document drifts
into a shape this parser cannot resolve unambiguously, that is reported as
``core.protocol.source_incoherent`` rather than resolved by a heuristic that
could silently select the wrong prose.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from . import _errors as E
from ._digest import SCHEME_CONTENT, digest_bytes
from ._records import DigestRef
from ._limits import MAX_PROTOCOL_SOURCE_BYTES

#: Frozen canonical stage identity: (heading number, stage key, heading title).
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


def _fail_incoherent(message: str, **details: object) -> None:
    E.fail(E.PROTOCOL_SOURCE_INCOHERENT, message, details=details)


def _sections(lines: list[str]) -> dict[tuple[int, str], tuple[int, int]]:
    """Map each ``## N. Title`` heading to its half-open line span."""

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


def parse_document(text: str) -> CanonicalDocument:
    """Parse a canonical workflow-prompt document into its stage bodies."""

    encoded = text.encode("utf-8")
    if len(encoded) > MAX_PROTOCOL_SOURCE_BYTES:
        E.fail(
            E.PROTOCOL_UNAVAILABLE,
            "the canonical prompt source exceeds the supported size bound",
            details={"bytes": len(encoded), "limit": MAX_PROTOCOL_SOURCE_BYTES},
        )
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    spans = _sections(lines)

    stages: dict[str, CanonicalStage] = {}
    for number, stage_key, title in CANONICAL_STAGES:
        span = spans.get((number, title))
        if span is None:
            _fail_incoherent(
                "the canonical source does not contain the expected stage heading",
                expected=f"## {number}. {title}",
                available=sorted(f"{n}. {t}" for n, t in spans),
            )
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
        text=text, content_digest=digest_bytes(encoded, SCHEME_CONTENT), stages=stages
    )
