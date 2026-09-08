"""The single TOML configuration normalization/validation path.

CLI and API share this owner; there is no second parser. Core-owned sections are
closed (unknown keys are rejected), which is also what keeps ad-hoc secret keys
such as ``token``/``password`` out of Core configuration without inventing a
secret scanner. ``[extensions."<ns>"]`` is the one open section: its content is
preserved verbatim as bounded raw data and only an activated extension
interprets it.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import platformdirs
from pydantic import BaseModel, ConfigDict, ValidationError

from . import _errors as E
from ._digest import SCHEME_CONFIG, canonical_json_bytes, digest_canonical
from ._limits import (
    MAX_CONFIG_BYTES,
    MAX_CONFIG_EXTENSION_BYTES,
    MAX_CONFIG_EXTENSION_NAMESPACES,
    MAX_CONFIG_NESTING,
    MAX_CONFIG_PROJECTS,
)
from ._records import DigestRef, PromptExecutionMode
from ._redact import sanitize_url

CONFIG_SCHEMA_VERSION = 1
APP_NAME = "sdp-orchestrator"
CONFIG_FILENAME = "config.toml"

_LOCAL_URL_SCHEMES = frozenset({"file"})
_WEB_URL_SCHEMES = frozenset({"https", "http", "ssh", "git"})


class _Closed(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class CoreSection(_Closed):
    default_project: str | None = None
    default_prompt_mode: PromptExecutionMode | None = None


class ProjectSection(_Closed):
    repo: str
    protocol_profile: str | None = None
    default_prompt_mode: PromptExecutionMode | None = None
    remote_name: str | None = None


class ProtocolSourceSection(_Closed):
    local_root: str | None = None
    allow_remote: bool = False
    remote_repository: str | None = None
    remote_ref: str | None = None


@dataclass(frozen=True)
class CoreConfig:
    """Normalized configuration plus its Core-semantic identity."""

    path: Path | None
    core: CoreSection
    projects: dict[str, ProjectSection]
    protocol_sources: dict[str, ProtocolSourceSection]
    extension_namespaces: dict[str, dict[str, Any]]
    identity: DigestRef

    def project(self, key: str) -> ProjectSection:
        try:
            return self.projects[key]
        except KeyError:
            E.fail(
                E.PROJECT_NOT_FOUND,
                f"no configured project named {key!r}",
                details={"configured": sorted(self.projects)},
                remediation="add a [projects.<key>] section or pass an existing --project",
            )


def _validation_summary(exc: ValidationError) -> str:
    """Describe a validation failure without echoing the offending value.

    ``ValidationError.errors()`` embeds the rejected input, which for a
    misplaced credential key would put the credential itself into a user-facing
    Problem. Only the location and error type are ever reported.
    """

    parts = []
    for error in exc.errors():
        location = ".".join(str(item) for item in error.get("loc", ())) or "<root>"
        parts.append(f"{location}: {error.get('type', 'invalid')}")
    return "; ".join(parts)


def default_config_path() -> Path:
    return Path(platformdirs.user_config_dir(APP_NAME, appauthor=False)) / CONFIG_FILENAME


def _check_depth(value: Any, depth: int = 0) -> None:
    if depth > MAX_CONFIG_NESTING:
        E.fail(E.CONFIG_INVALID, "configuration nesting exceeds the supported bound")
    if isinstance(value, Mapping):
        for item in value.values():
            _check_depth(item, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _check_depth(item, depth + 1)


def _require_noncredential_url(label: str, url: str) -> None:
    sanitized = sanitize_url(url)
    if sanitized != url:
        E.fail(
            E.CONFIG_INVALID,
            f"{label} must not embed credentials in its URL",
            details={"value": sanitized},
            remediation="use a credential-free URL and an established Git credential helper",
        )


def load_config(path: str | os.PathLike[str] | None = None) -> CoreConfig:
    """Read, bound, validate, and identify the configuration document."""

    resolved = Path(path).expanduser() if path is not None else default_config_path()
    if not resolved.exists():
        if path is not None:
            E.fail(
                E.CONFIG_INVALID,
                "configuration file does not exist",
                details={"path": str(resolved)},
            )
        return _empty_config(None)
    if not resolved.is_file():
        E.fail(
            E.CONFIG_INVALID,
            "configuration path is not a regular file",
            details={"path": str(resolved)},
        )
    size = resolved.stat().st_size
    if size > MAX_CONFIG_BYTES:
        E.fail(
            E.CONFIG_INVALID,
            "configuration file exceeds the supported size bound",
            details={"path": str(resolved), "bytes": size, "limit": MAX_CONFIG_BYTES},
        )
    try:
        chunks: list[bytes] = []
        total = 0
        with resolved.open("rb") as handle:
            while True:
                chunk = handle.read(min(64 * 1024, MAX_CONFIG_BYTES - total + 1))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > MAX_CONFIG_BYTES:
                    E.fail(
                        E.CONFIG_INVALID,
                        "configuration file exceeds the supported size bound",
                        details={"path": str(resolved), "limit": MAX_CONFIG_BYTES},
                    )
        raw_bytes = b"".join(chunks)
    except OSError as exc:
        E.fail(
            E.CONFIG_INVALID,
            f"configuration file could not be read: {type(exc).__name__}",
            details={"path": str(resolved)},
        )
    try:
        raw = tomllib.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        E.fail(
            E.CONFIG_INVALID,
            f"configuration file is not valid UTF-8 TOML: {exc}",
            details={"path": str(resolved)},
        )
    return parse_config(raw, resolved)


def _empty_config(path: Path | None) -> CoreConfig:
    core = CoreSection()
    return CoreConfig(
        path=path,
        core=core,
        projects={},
        protocol_sources={},
        extension_namespaces={},
        identity=_identity(core, {}, {}),
    )


def _identity(
    core: CoreSection,
    projects: Mapping[str, ProjectSection],
    protocol_sources: Mapping[str, ProtocolSourceSection],
) -> DigestRef:
    """Digest the Core-semantic configuration only.

    Extension namespaces are excluded on purpose: unrelated extension config must
    not perturb project/preparation/prompt identity (workplan invariant 14).
    """

    payload = {
        "schema_version": CONFIG_SCHEMA_VERSION,
        "core": core.model_dump(mode="json", exclude_none=True),
        "projects": {
            key: projects[key].model_dump(mode="json", exclude_none=True)
            for key in sorted(projects)
        },
        "protocol_sources": {
            key: protocol_sources[key].model_dump(mode="json", exclude_none=True)
            for key in sorted(protocol_sources)
        },
    }
    return digest_canonical(payload, SCHEME_CONFIG)


def parse_config(raw: Mapping[str, Any], path: Path | None = None) -> CoreConfig:
    _check_depth(raw)

    known_top = {"schema_version", "core", "projects", "protocol_sources", "extensions"}
    unknown = sorted(set(raw) - known_top)
    if unknown:
        E.fail(
            E.CONFIG_INVALID,
            "configuration contains unsupported top-level keys",
            details={"unknown": unknown, "supported": sorted(known_top)},
            remediation="Core configuration is closed; extension data belongs under [extensions.\"<ns>\"]",
        )

    schema_version = raw.get("schema_version")
    if schema_version != CONFIG_SCHEMA_VERSION:
        E.fail(
            E.CONFIG_INVALID,
            "configuration schema_version is missing or unsupported",
            details={"found": schema_version, "supported": CONFIG_SCHEMA_VERSION},
        )

    try:
        core = CoreSection(**dict(raw.get("core") or {}))
    except ValidationError as exc:
        E.fail(E.CONFIG_INVALID, f"invalid [core] section -- {_validation_summary(exc)}")

    projects_raw = dict(raw.get("projects") or {})
    if len(projects_raw) > MAX_CONFIG_PROJECTS:
        E.fail(
            E.CONFIG_INVALID,
            "configuration declares more projects than the supported bound",
            details={"count": len(projects_raw), "limit": MAX_CONFIG_PROJECTS},
        )
    projects: dict[str, ProjectSection] = {}
    for key, section in projects_raw.items():
        if not isinstance(section, Mapping):
            E.fail(E.CONFIG_INVALID, f"[projects.{key}] must be a table")
        try:
            project = ProjectSection(**dict(section))
        except ValidationError as exc:
            E.fail(E.CONFIG_INVALID, f"invalid [projects.{key}] -- {_validation_summary(exc)}")
        _require_noncredential_url(f"[projects.{key}].repo", project.repo)
        projects[key] = project

    sources_raw = dict(raw.get("protocol_sources") or {})
    protocol_sources: dict[str, ProtocolSourceSection] = {}
    for key, section in sources_raw.items():
        if not isinstance(section, Mapping):
            E.fail(E.CONFIG_INVALID, f"[protocol_sources.{key}] must be a table")
        try:
            source = ProtocolSourceSection(**dict(section))
        except ValidationError as exc:
            E.fail(E.CONFIG_INVALID, f"invalid [protocol_sources.{key}] -- {_validation_summary(exc)}")
        if source.remote_repository:
            _require_noncredential_url(
                f"[protocol_sources.{key}].remote_repository", source.remote_repository
            )
        if source.allow_remote and not (source.remote_repository and source.remote_ref):
            E.fail(
                E.CONFIG_INVALID,
                f"[protocol_sources.{key}] enables allow_remote without remote_repository and remote_ref",
                remediation="a remote Protocol source requires an explicit evidence-backed ref",
            )
        protocol_sources[key] = source

    extensions_raw = dict(raw.get("extensions") or {})
    if len(extensions_raw) > MAX_CONFIG_EXTENSION_NAMESPACES:
        E.fail(
            E.CONFIG_INVALID,
            "configuration declares more extension namespaces than the supported bound",
            details={"count": len(extensions_raw), "limit": MAX_CONFIG_EXTENSION_NAMESPACES},
        )
    extension_namespaces: dict[str, dict[str, Any]] = {}
    for key, section in extensions_raw.items():
        if not isinstance(section, Mapping):
            E.fail(E.CONFIG_INVALID, f'[extensions."{key}"] must be a table')
        try:
            encoded = canonical_json_bytes(section)
        except (TypeError, ValueError) as exc:
            E.fail(E.CONFIG_INVALID, f'[extensions."{key}"] is not JSON-representable: {exc}')
        if len(encoded) > MAX_CONFIG_EXTENSION_BYTES:
            E.fail(
                E.CONFIG_INVALID,
                f'[extensions."{key}"] exceeds the supported size bound',
                details={"bytes": len(encoded), "limit": MAX_CONFIG_EXTENSION_BYTES},
            )
        extension_namespaces[key] = dict(section)

    if core.default_project and core.default_project not in projects:
        E.fail(
            E.CONFIG_INVALID,
            "[core].default_project names an undefined project",
            details={"default_project": core.default_project, "configured": sorted(projects)},
        )

    return CoreConfig(
        path=path,
        core=core,
        projects=projects,
        protocol_sources=protocol_sources,
        extension_namespaces=extension_namespaces,
        identity=_identity(core, projects, protocol_sources),
    )
