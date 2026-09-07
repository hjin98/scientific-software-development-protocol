"""Canonical INPUT classification, binding, and structure-safe encoding.

The canonical prompt grammar is one ``NAME = value`` line per input. Every
concrete value Core inserts therefore passes through :func:`encode_scalar`, which
guarantees the value cannot terminate its own line, introduce a second
``NAME =`` line, or smuggle a NUL into the artifact.

Ownership is enforced strictly rather than leniently: an override aimed at a
first-class or mechanical binding fails instead of quietly winning or quietly
losing. Both silent outcomes produce a prompt whose authority the user cannot
predict.
"""

from __future__ import annotations

import re

from . import _errors as E
from ._limits import MAX_INPUT_OVERRIDES, MAX_INPUT_VALUE_BYTES
from ._records import (
    InputBinding,
    InputOwnership,
    ResolvedInput,
    StageDescriptor,
    WorkplanRef,
)

_ESCAPES = {"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t"}
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

#: Provenance labels recorded on each resolved input.
P_CANONICAL_DEFAULT = "canonical_default"
P_USER_OVERRIDE = "user_override"
P_FIRST_TASK = "first_task"
P_WORKPLAN = "workplan_selector"
P_GOVERNING_PROTOCOL = "governing_protocol_contract"
P_RENDER_MODE = "render_mode_dependent"


def encode_scalar(value: str) -> str:
    """Return the frozen v1 structure-safe single-line representation of ``value``.

    The encoding is reversible: a backslash always begins an escape, so
    ``\\\\``, ``\\n``, ``\\r``, ``\\t`` and ``\\xHH`` decode uniquely.
    """

    encoded = len(value.encode("utf-8"))
    if encoded > MAX_INPUT_VALUE_BYTES:
        E.fail(
            E.PROMPT_INPUT_INVALID,
            "an input value exceeds the supported size bound",
            details={"bytes": encoded, "limit": MAX_INPUT_VALUE_BYTES},
        )
    out: list[str] = []
    for char in value:
        if char in _ESCAPES:
            out.append(_ESCAPES[char])
        elif _CONTROL.match(char):
            out.append(f"\\x{ord(char):02X}")
        else:
            out.append(char)
    return "".join(out)


def decode_scalar(value: str) -> str:
    """Inverse of :func:`encode_scalar`; exists so the encoding is provably reversible."""

    out: list[str] = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "\\":
            out.append(char)
            index += 1
            continue
        marker = value[index + 1 : index + 2]
        if marker == "\\":
            out.append("\\")
            index += 2
        elif marker == "n":
            out.append("\n")
            index += 2
        elif marker == "r":
            out.append("\r")
            index += 2
        elif marker == "t":
            out.append("\t")
            index += 2
        elif marker == "x":
            out.append(chr(int(value[index + 2 : index + 4], 16)))
            index += 4
        else:  # pragma: no cover - encode_scalar never emits this
            raise ValueError(f"unrecognized escape at offset {index}")
    return "".join(out)


def normalize_overrides(pairs: tuple[tuple[str, str], ...]) -> dict[str, str]:
    if len(pairs) > MAX_INPUT_OVERRIDES:
        E.fail(
            E.PROMPT_INPUT_INVALID,
            "more input overrides were supplied than the supported bound",
            details={"count": len(pairs), "limit": MAX_INPUT_OVERRIDES},
        )
    overrides: dict[str, str] = {}
    for name, value in pairs:
        key = name.strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
            E.fail(
                E.PROMPT_INPUT_INVALID,
                "an input name is not a valid canonical INPUT identifier",
                details={"name": name[:80]},
            )
        if key in overrides and overrides[key] != value:
            E.fail(
                E.PROMPT_INPUT_CONFLICT,
                "the same input was supplied twice with different values",
                details={"name": key},
            )
        overrides[key] = value
    return overrides


def resolve_inputs(
    stage: StageDescriptor,
    *,
    workplan: WorkplanRef | None,
    first_task: str | None,
    overrides: dict[str, str],
    governing_protocol_version: str,
) -> tuple[ResolvedInput, ...]:
    """Classify and bind every canonical INPUT this stage declares.

    Mode-dependent mechanical inputs are intentionally left unvalued here: they
    belong to final render, and materializing them during preparation would make
    the preparation identity depend on a route that has not been chosen yet.
    """

    declared = {binding.name: binding for binding in stage.inputs}

    unknown = sorted(set(overrides) - set(declared))
    if unknown:
        E.fail(
            E.PROMPT_INPUT_UNKNOWN,
            f"stage {stage.stage.stage_key!r} does not declare the supplied input(s)",
            details={"unknown": unknown, "declared": sorted(declared)},
        )

    conflicting = sorted(
        name for name in overrides if not declared[name].override_allowed
    )
    if conflicting:
        E.fail(
            E.PROMPT_INPUT_CONFLICT,
            "these inputs are owned by a first-class or mechanical binding and cannot be overridden",
            details={
                "conflicting": conflicting,
                "bindings": {
                    name: declared[name].first_class_source or declared[name].ownership.value
                    for name in conflicting
                },
            },
        )

    if first_task is not None and "TASK" not in declared:
        E.fail(
            E.PROMPT_INPUT_CONFLICT,
            f"stage {stage.stage.stage_key!r} does not accept a task",
            details={"stage": stage.stage.stage_key},
            remediation="--task is a Design-stage input",
        )

    resolved: list[ResolvedInput] = []
    for binding in stage.inputs:
        resolved.append(
            _resolve_one(
                binding,
                stage=stage,
                workplan=workplan,
                first_task=first_task,
                overrides=overrides,
                governing_protocol_version=governing_protocol_version,
            )
        )
    return tuple(resolved)


def _resolve_one(
    binding: InputBinding,
    *,
    stage: StageDescriptor,
    workplan: WorkplanRef | None,
    first_task: str | None,
    overrides: dict[str, str],
    governing_protocol_version: str,
) -> ResolvedInput:
    name = binding.name

    if binding.mode_dependent:
        return ResolvedInput(
            name=name,
            ownership=binding.ownership,
            value=None,
            provenance=P_RENDER_MODE,
            mode_dependent=True,
        )

    if name == "PROTOCOL_REF":
        return ResolvedInput(
            name=name,
            ownership=binding.ownership,
            value=encode_scalar(governing_protocol_version),
            provenance=P_GOVERNING_PROTOCOL,
        )

    if binding.first_class_source == "workplan_selector":
        if workplan is None:
            E.fail(
                E.WORKPLAN_REQUIRED,
                f"stage {stage.stage.stage_key!r} requires a governing workplan for {name}",
                details={"stage": stage.stage.stage_key, "input": name},
                remediation="pass --workplan <workplan_id-or-path>",
            )
        return ResolvedInput(
            name=name,
            ownership=binding.ownership,
            value=encode_scalar(workplan.path),
            provenance=P_WORKPLAN,
        )

    if binding.first_class_source == "first_task":
        if not first_task or not first_task.strip():
            E.fail(
                E.PROMPT_INPUT_REQUIRED,
                f"stage {stage.stage.stage_key!r} requires an explicit task",
                details={"stage": stage.stage.stage_key, "input": name},
                remediation="pass --task '<description of the change or problem>'",
            )
        return ResolvedInput(
            name=name,
            ownership=binding.ownership,
            value=encode_scalar(first_task),
            provenance=P_FIRST_TASK,
        )

    if name in overrides:
        value = overrides[name]
        if not value.strip():
            E.fail(
                E.PROMPT_INPUT_INVALID,
                f"input {name} was supplied with an empty value",
                details={"input": name},
            )
        return ResolvedInput(
            name=name,
            ownership=binding.ownership,
            value=encode_scalar(value),
            provenance=P_USER_OVERRIDE,
        )

    if binding.ownership is InputOwnership.REQUIRED_USER:
        if binding.first_class_source == "workplan_selector_optional" and workplan is not None:
            return ResolvedInput(
                name=name,
                ownership=binding.ownership,
                value=encode_scalar(workplan.workplan_id),
                provenance=P_WORKPLAN,
            )
        E.fail(
            E.PROMPT_INPUT_REQUIRED,
            f"stage {stage.stage.stage_key!r} requires the user-owned input {name}",
            details={"stage": stage.stage.stage_key, "input": name},
            remediation=f"pass --input {name}='...'",
        )

    if binding.default_value is None:  # pragma: no cover - profile guarantees a default
        E.fail(
            E.PROMPT_INPUT_REQUIRED,
            f"input {name} has no canonical default and no supplied value",
            details={"input": name},
        )
    return ResolvedInput(
        name=name,
        ownership=binding.ownership,
        value=encode_scalar(binding.default_value),
        provenance=P_CANONICAL_DEFAULT,
    )
