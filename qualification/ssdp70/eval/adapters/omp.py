#!/usr/bin/env python3
"""Oh My Pi (`omp`) Stage F runtime adapter (SSDP 7.0 portability, OMP-only slice), D4 realization.

Authority: the OMP provider-adaptation slice, the accepted D3 trust-topology/runtime-observation
repair and the authorized D4 repair tranche of
workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md, and
qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md (section 1 items 1-11,
section 6). Exact build: omp/18.0.11 (see OMP_BUILD and the build inventory).

Realized principal graph (exactly three logical principals, no fourth):

  qualification supervisor   harness70 + this adapter + the qualification MCP bridge
                             (the unchanged stub_tools/mediator.py behind mcp_bridge70.py)
  provider-control/observer  observer70.py: the only route to the model provider, owner of the
                             provider credential, single-purpose inference transport that
                             retains raw hash-linked evidence of every request/response
  subject/executor           OMP and every process it starts, inside a bubblewrap sandbox with an
                             empty network namespace, a minimal read-only filesystem view, no host
                             HOME, no credential and no supervisor/mediator/observer state

The subject reaches the two authorized principals only through subject_launcher.py's relay over
inherited descriptor pairs. Authority is bound to the supervisor-authorized OMP process instance:
a loopback connection is relayed only if its client socket is held solely by the OMP process the
launcher started, so `bash`/subprocesses (or a second copy of the same executable) cannot use the
inference or MCP transport. See qualification/ssdp70/STAGE-F-OMP-PROVIDER-ADAPTATION-D4-REIMPLEMENTATION-2026-09-29.md.

Catalog, build, tool surface, MCP surface, configuration source and root activation are derived
from the trusted principals' hash-linked evidence plus the native JSON trace, never from the
installed-directory listing, the frozen profile, launch argv or the harness-authored prompt; those
only serve as comparison references. Any missing, unbound, contradictory, unknown, dropped,
reordered or truncated material evidence fails closed.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml

HERE = Path(__file__).resolve().parent
EVAL_DIR = HERE.parent
REPO_ROOT = EVAL_DIR.parents[2]
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))
import core70  # noqa: E402
import evidence70  # noqa: E402
import seccomp70  # noqa: E402

ADAPTER_ID = "omp-json-v2"
CONTAINMENT_KIND = "omp-three-principal-bwrap-v3"
PROJECT_CONTROL_MUTATION_POLICY = "immutable"

SSDP_SKILLS = frozenset({
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-maintenance-audit",
    "software-documentation",
    "repository-hygiene",
})

# ------------------------------------------------------------------ exact frozen build identity
OMP_BUILD = {
    "version": "18.0.11",
    "sha256": "6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26",
    "bytes": 194573512,
    "build_id": "2c2e51f3b6fae6722da4f7b69751a2e9467ab063",
    # What the exact build presents on the trusted paths (observed): the embedded Bun runtime's HTTP client
    # identity on every inference request, and its MCP client identity on initialize.
    "http_user_agent": "Bun/1.4.0",
    "mcp_client_info": {"name": "omp-coding-agent", "version": "1.0.0"},
}
OBSERVER_BOUNDARY_POLICY = {
    "filesystem": "explicit Python runtime, observer code, CA bundle and synthetic /etc only; no host HOME, custody, mediator or supervisor state",
    "network": "trusted observer opens only the frozen provider route before accepting subject input, then moves to a private network namespace and installs seccomp denying new sockets, connects and addressed sends",
    "process": "private PID namespace with no host process view; capability set dropped after route setup",
    "provider_route_capability": "one connected stream socket owned by the observer; inference requests remain single-purpose and evidence is append-only",
}

# ----------------------------------------------------------------------- in-sandbox layout
SB_PROJECT = "/workspace"
SB_HOME = "/home/agent"
SB_SKILLS = "/opt/ssdp/skills"
SB_CTL = "/opt/ssdp/ctl"
SB_OMP = "/opt/omp/omp"
SB_TMP = "/tmp"
OBSERVER_HOME = "/observer-home"
OBSERVER_CODE = "/opt/ssdp/observer"
RELAY_PORTS = {"inference": 31001, "mcp": 31002}
RUNTIME_DEPENDENCIES_PATH = EVAL_DIR / "omp-runtime-dependencies-18.0.11.json"
RUNTIME_DEPENDENCIES_SHA256 = "dc2a6035d72e889d80f97e6c048f517765e1c2ade480171aa4e160a59f4c35f1"
OBSERVER_EXEC_HELPER = EVAL_DIR / "observer_exec_helper70.py"
OBSERVER_CHANNEL_TARGETS = (3, 4, 5, 6)
OBSERVER_ARGUMENT_TARGET = 7
OBSERVER_REQUIRED_PROBES = frozenset({
    "host_home", "qualification_custody", "supervisor_private", "mediator_backing_state",
    "new-af-inet-socket", "new-af-unix-socket", "unrelated-addressed-network-send",
    "unrelated-process-control", "unrelated-process-inspection", "credential-environment",
})

# --------------------------------------------------------------------------- tool surface
OMP_MCP_SERVER_NAME = "ssdp70"
OMP_MCP_SERVER_ID = "ssdp70-qualification-stdio-v1"
OMP_MCP_SERVER_ENTRYPOINT = "stub_tools/mediator.py"
OMP_BUILTIN_TOOLS = ("read", "glob", "grep", "edit", "write", "bash")
OMP_RAW_MCP_TOOLS = (
    "issue_locations", "issue_search", "issue_show", "issue_create", "issue_comment", "delegate",
)
MCP_OPERATION = {
    "issue_locations": "locations", "issue_search": "search", "issue_show": "show",
    "issue_create": "create", "issue_comment": "comment", "delegate": "delegate",
}
MCP_MUTATING = {"issue_create", "issue_comment"}
MCP_STORE_IDENTITY = "ssdp70-private-issue-standin"
# Builtin tool names OMP 18.0.11 can register (source of truth: the build's tool table). A model
# call to a name outside the exposed surface is retained as a blocked attempt, never mapped to work.
OMP_ALL_BUILTIN_NAMES = frozenset({
    "read", "security_scan", "bash", "edit", "ast_grep", "ast_edit", "ask", "debug", "eval", "github",
    "glob", "grep", "lsp", "inspect_image", "browser", "computer", "checkpoint", "rewind", "task", "hub",
    "todo", "web_search", "write", "memory_edit", "retain", "recall", "reflect", "learn", "manage_skill",
    "think", "yield", "goal",
})
ATTEMPT_CLASS_HINT = {
    "web_search": "network_remote_service", "browser": "network_remote_service", "github": "network_remote_service",
    "task": "delegation", "hub": "delegation", "eval": "process_execution", "debug": "process_execution",
}

OMP_KNOWN_EVENT_TYPES = frozenset({
    "session", "agent_start", "agent_end", "turn_start", "turn_end",
    "message_start", "message_update", "message_end",
    "tool_execution_start", "tool_execution_update", "tool_execution_end",
})
# Provider-managed behaviours the frozen closure disables. Seeing one of these events means a
# behaviour the profile froze off ran anyway: the run is inadmissible, never silently absorbed.
OMP_PROVIDER_MANAGED_EVENT_TYPES = frozenset({
    "auto_compaction_start", "auto_compaction_end", "auto_retry_start", "auto_retry_end",
    "retry_fallback_applied", "retry_fallback_succeeded", "ttsr_triggered", "todo_reminder",
    "todo_auto_clear", "irc_message", "notice", "thinking_level_changed", "model_changed", "goal_updated",
})

# These hash-linked observer records establish adapter containment and credential
# custody. They are consumed by Observed's fail-closed D4 checks and retained as
# adapter evidence; they are not task-trajectory events in the frozen core schema.
REVIEWED_NON_ORACLE_OBSERVER_CONTROL_KINDS = frozenset({
    "provider_route_opened", "boundary_probe", "boundary", "credential_received", "ready",
})

# ------------------------------------------------------------------ settings/discovery closure
# Every setting the exact build exposes is classified in the retained build inventory
# (omp-build-inventory-18.0.11.json). These are the settings the profile freezes; the effective
# values are re-read from the exact binary before each run (launcher probe) and must match.
FROZEN_SETTINGS: dict[str, Any] = {
    # Hidden model calls / provider-managed control flow
    "retry": {"enabled": False, "maxRetries": 0, "modelFallback": False, "usageAwareFallback": False},
    "compaction": {"enabled": False, "midTurnEnabled": False, "asyncEnabled": False, "idleEnabled": False},
    "contextPromotion": {"enabled": False},
    "branchSummary": {"enabled": False},
    "advisor": {"enabled": False},
    "prewalk": {"enabled": False},
    "task": {"prewalk": False},
    "goal": {"enabled": False},
    "plan": {"enabled": False},
    "memory": {"backend": "off"},
    "memories": {"enabled": False},
    "autolearn": {"enabled": False},
    "recap": {"enabled": False},
    "features": {"unexpectedStopDetection": "none"},
    "ttsr": {"enabled": False},
    "todo": {"reminders": False},
    "magicKeywords": {"enabled": False},
    "model": {"loopGuard": {"enabled": False}, "toolCallLoopGuard": {"enabled": False}},
    "images": {"describeForTextModels": False},
    # Startup network / telemetry / update behaviour
    "startup": {"checkUpdate": False, "setupWizard": False, "showSplash": False, "changelogMode": "hidden"},
    "marketplace": {"autoUpdate": "off"},
    "dev": {"autoqa": False, "autoqaConsent": "denied"},
    "providers": {"openaiWebsockets": "off"},
    "power": {"sleepPrevention": "off"},
    "completion": {"notify": "off"},
    "error": {"notify": "off"},
    "ask": {"notify": "off"},
    # Discovery closure: no foreign or project-scoped provider is enabled
    "mcp": {"enableProjectConfig": False, "notifications": False},
    "lsp": {"enabled": False},
    "git": {"enabled": False},
    "commands": {
        "enableClaudeUser": False, "enableClaudeProject": False,
        "enableOpencodeUser": False, "enableOpencodeProject": False,
    },
    "skills": {
        "enabled": True,
        "enableCodexUser": False, "enableClaudeUser": False, "enableClaudeProject": False,
        "enablePiUser": False, "enablePiProject": False,
        "enableAgentsUser": False, "enableAgentsProject": False,
        "enableSkillCommands": False,
        "customDirectories": [SB_SKILLS],
    },
    # Process / tool behaviour that alters what the model sees or what runs
    "bash": {"direnv": "off", "autoBackground": {"enabled": False}},
    "async": {"enabled": False},
    "eval": {"py": False, "js": False},
    "shellMinimizer": {"enabled": False},
    "read": {"summarize": {"enabled": False}},
    "tools": {"xdev": False, "intentTracing": False},
}

# Files and directories in the run-owned HOME that the exact build reads at startup and that can
# change the system prompt, environment or discovery (found by strace and effect tests). The
# run-owned HOME must contain none of them before launch.
HOME_DISCOVERY_SOURCES = (
    ".env", ".omp/.env", ".omp/agent/.env",
    ".omp/agent/SYSTEM.md", ".omp/agent/APPEND_SYSTEM.md", ".omp/agent/AGENTS.md", ".omp/agent/RULES.md",
    ".omp/agent/PERSONALITY.md", ".omp/agent/TITLE_SYSTEM.md", ".omp/agent/WATCHDOG.md",
    ".omp/agent/settings.json", ".omp/agent/config.yaml", ".omp/agent/.mcp.json",
    ".omp/agent/skills", ".omp/agent/rules", ".omp/agent/prompts", ".omp/agent/commands",
    ".omp/agent/hooks", ".omp/agent/agents", ".omp/agent/extensions", ".omp/plugins", ".omp/marketplaces.json",
    ".claude", ".claude.json", ".codex", ".gemini", ".agents", ".agent", ".cursor", ".codeium",
    ".config/opencode", ".config/gcloud", ".aws", ".lsp.json", ".lsp.yaml", ".lsp.yml", "lsp.json", "lsp.yaml", "lsp.yml",
)
# Project-relative sources the exact build discovers (native OMP, Claude, Codex, Gemini, OpenCode,
# Cursor, Windsurf, VS Code, GitHub/agents context, standalone MCP). A fixture baseline containing
# any of them is refused before launch; the run's post-state may not contain them either.
PROJECT_DISCOVERY_SOURCES = (
    ".omp", ".claude", ".codex", ".gemini", ".agents", ".agent", ".opencode", ".cursor", ".windsurf", ".vscode",
    ".github/copilot-instructions.md", ".github/skills", ".github/instructions", ".github/agents",
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", ".mcp.json", "mcp.json", "opencode.json", "opencode.jsonc",
    "SYSTEM.md",
)
# Effect-tested inert for the project (process cwd is `/`, so Bun's dotenv/bunfig autoload never reads them):
# `.env` and `bunfig.toml` in the project are not discovery sources. The HOME `.env` files ARE (observed to
# enter OMP's environment) and are refused above.
# OMP-owned runtime state created under the run-owned HOME (recorded, not control state).
HOME_RUNTIME_STATE_PATTERNS = (
    r"^\.omp/natives(/|$)", r"^\.omp/logs(/|$)", r"^\.omp/run(/|$)", r"^\.omp/gpu_cache\.json$",
    r"^\.omp/agent/(agent|models|history)\.db(-wal|-shm|-journal)?$", r"^\.omp/agent/cache(/|$)",
    r"^\.omp/agent/[^/]+\.lock$", r"^\.omp/agent/sessions(/|$)", r"^\.omp/agent/terminal-sessions(/|$)",
    r"^\.config(/|$)", r"^\.cache(/|$)", r"^\.omp/agent/last-changelog-version$",
)
CONTROL_FILES_IN_HOME = (".omp/agent/config.yml", ".omp/agent/models.yml", ".omp/agent/mcp.json")
# Settings whose effective value legitimately depends on run-owned paths, not on configuration state.
SETTINGS_PATH_DEPENDENT: frozenset[str] = frozenset()

SAFE_ENV_KEYS = ("PATH", "LANG")
MINIMAL_PATH = "/usr/bin:/bin"
CREDENTIAL_ENV_NAMES = (
    "OMP_API_KEY", "OMP_AUTH_TOKEN", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY",
    "DEEPINFRA_API_KEY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN", "GH_TOKEN",
    "SSH_AUTH_SOCK", "ANTHROPIC_OAUTH_TOKEN", "COPILOT_GITHUB_TOKEN",
)
API_ENDPOINTS = {"openai-completions": "/chat/completions"}
# Hard-coded in the exact build's provider/transport layers (source: `jv(...)` with retryEmptyCompletion,
# MAX_EMPTY_COMPLETION_RETRIES=2, and a transport retry observed up to 6+ resends after HTTP 5xx and 5 after
# HTTP 429; `maxRetries: 10` is the largest bound in the build). It sits below OMP's own retry setting, cannot
# be disabled by configuration, and always resends the identical request before any content reaches the agent. It is therefore frozen as an observed arm-neutral
# provider-managed behaviour: allowed only when every such request is byte-identical to its predecessor
# and follows a transient error or an empty completion, and always retained in the evidence.
MAX_PROVIDER_ERROR_RETRIES = 10
MAX_EMPTY_COMPLETION_RETRIES = 2
RETRYABLE_STATUS = frozenset({408, 429})


class AdapterError(RuntimeError):
    pass


# --------------------------------------------------------------------------- basic helpers

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest_json(value: Any) -> str:
    return sha256_bytes(stable_json(value).encode("utf-8"))


def _deep_update(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = copy.deepcopy(value)
    return base


def _flatten(prefix: str, value: Any, out: dict[str, Any]) -> None:
    if isinstance(value, dict) and value:
        for key, item in value.items():
            _flatten(f"{prefix}.{key}" if prefix else str(key), item, out)
    else:
        out[prefix] = value


def frozen_settings_flat() -> dict[str, Any]:
    out: dict[str, Any] = {}
    _flatten("", FROZEN_SETTINGS, out)
    return out


def settings_document() -> dict[str, Any]:
    return copy.deepcopy(FROZEN_SETTINGS)


# ------------------------------------------------------------------- MCP name minting (exact)

def _mint_component(value: str, fallback: str) -> str:
    """OMP 18.0.11 `Qro`: lowercase, runs outside [a-z_] become `_`, collapse, trim."""
    text = re.sub(r"_+", "_", re.sub(r"[^a-z_]+", "_", str(value).lower())).strip("_")
    return text or fallback


def mint_mcp_tool_name(server: str, tool: str) -> str:
    """OMP 18.0.11 `hft`: `mcp__<server>_<tool>` with one redundant server prefix removed.

    Names longer than 64 characters get a deterministic Bun.hash suffix that this adapter does not
    reproduce; such a name is refused instead of guessed (the frozen six names are far shorter).
    """
    minted_server = _mint_component(server, "server")
    minted_tool = _mint_component(tool, "tool")
    prefix = f"{minted_server}_"
    if minted_tool.startswith(prefix):
        minted_tool = minted_tool[len(prefix):]
    name = f"mcp__{minted_server}_{minted_tool}"
    if len(name) > 64:
        raise AdapterError(
            f"MCP tool name {name!r} exceeds 64 characters; OMP appends a Bun.hash suffix this adapter "
            "does not reproduce, so the binding is refused"
        )
    return name


def expected_mcp_native_ids(server: str = OMP_MCP_SERVER_NAME,
                            tools: tuple[str, ...] | list[str] = OMP_RAW_MCP_TOOLS) -> dict[str, str]:
    mapping = {tool: mint_mcp_tool_name(server, tool) for tool in tools}
    if len(set(mapping.values())) != len(mapping):
        raise AdapterError("OMP MCP name minting collides for the declared tool set; binding refused")
    return mapping


def verify_mcp_binding(profile: dict[str, Any]) -> tuple[bool, list[str], dict[str, str]]:
    """Static half of the raw-tool <-> provider-native-id bijection (runtime half: observation)."""
    errors: list[str] = []
    servers = profile.get("mcp_servers")
    if not isinstance(servers, list) or len(servers) != 1 or not isinstance(servers[0], dict):
        return False, ["OMP Stage F profile requires exactly one declared qualification MCP server"], {}
    declared = servers[0]
    if declared.get("name") != OMP_MCP_SERVER_NAME:
        errors.append(f"declared MCP server name {declared.get('name')!r} is not the reviewed qualification server")
    if declared.get("server_id") != OMP_MCP_SERVER_ID:
        errors.append("declared MCP server id differs from the reviewed qualification server id")
    if declared.get("entrypoint") != OMP_MCP_SERVER_ENTRYPOINT:
        errors.append("declared MCP server entrypoint differs from the reviewed mediator entrypoint")
    try:
        mapping = expected_mcp_native_ids(str(declared.get("name")))
    except AdapterError as exc:
        return False, [str(exc)], {}
    declared_tools = declared.get("tools")
    if not isinstance(declared_tools, list) or not all(isinstance(item, str) for item in declared_tools):
        errors.append("declared MCP tool surface is malformed")
        declared_tools = []
    if sorted(declared_tools) != sorted(mapping.values()):
        errors.append(
            "declared MCP tool surface differs from the exact name-minting result: "
            f"declared={sorted(declared_tools)}, minted={sorted(mapping.values())}"
        )
    return (not errors), errors, mapping


# ---------------------------------------------------------------------- profile and identity

def _contains_unfrozen(value: Any) -> bool:
    if isinstance(value, str):
        return "MUST-BE-FROZEN" in value
    if isinstance(value, dict):
        return any(_contains_unfrozen(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_unfrozen(v) for v in value)
    return False


def principal_files() -> dict[str, Path]:
    return {
        # Supervisor-owned launch control bytes are digest-bound here; this helper is not a principal.
        "observer_exec_helper70.py": OBSERVER_EXEC_HELPER,
        "observer70.py": EVAL_DIR / "observer70.py",
        "mcp_bridge70.py": EVAL_DIR / "mcp_bridge70.py",
        "muxhttp70.py": EVAL_DIR / "muxhttp70.py",
        "evidence70.py": EVAL_DIR / "evidence70.py",
        "subject_launcher.py": EVAL_DIR / "subject_launcher.py",
        "seccomp70.py": EVAL_DIR / "seccomp70.py",
        "stub_tools/mediator.py": EVAL_DIR / "stub_tools" / "mediator.py",
    }


def support_files() -> dict[str, Path]:
    """Adapter-owned principal code that participates in the run identity (provenance)."""
    return {**principal_files(), "omp-runtime-dependencies-18.0.11.json": RUNTIME_DEPENDENCIES_PATH}


def principal_files_sha256() -> dict[str, str]:
    return {name: sha256_file(path) for name, path in sorted(principal_files().items())}


def settings_closure_sha256() -> str:
    return _digest_json(settings_document())


def runtime_dependency_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(RUNTIME_DEPENDENCIES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"runtime dependency manifest is unreadable: {exc}") from exc
    if (not isinstance(manifest, dict) or manifest.get("schema") != 1
            or not isinstance(manifest.get("dependencies"), list)
            or not isinstance(manifest.get("aliases"), list)):
        raise AdapterError("runtime dependency manifest has an unsupported shape")
    return manifest


def _runtime_tree_digest(root: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    rows = sorted(root.rglob("*"))
    for path in rows:
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        mode = format(info.st_mode & 0o7777, "04o")
        if path.is_symlink():
            kind = "symlink"
            payload = os.readlink(path).encode("utf-8", "surrogateescape")
        elif path.is_dir():
            kind, payload = "dir", b""
        elif path.is_file():
            kind = "file"
            payload = bytes.fromhex(sha256_file(path))
        else:
            raise AdapterError(f"runtime dependency tree contains an unsupported object: {path}")
        for part in (relative.encode("utf-8", "surrogateescape"), kind.encode(), mode.encode(), payload):
            digest.update(part)
            digest.update(b"\0")
    return digest.hexdigest(), len(rows)


def runtime_dependency_errors(profile: dict[str, Any] | None = None) -> list[str]:
    """Verify every explicitly exposed host dependency against the frozen content manifest."""
    try:
        manifest = runtime_dependency_manifest()
    except AdapterError as exc:
        return [str(exc)]
    errors: list[str] = []
    for entry in manifest["dependencies"]:
        source = Path(str(entry.get("source", "")))
        kind = entry.get("kind")
        try:
            info = source.lstat()
            mode = format(info.st_mode & 0o7777, "04o")
            if mode != entry.get("mode"):
                errors.append(f"runtime dependency mode drift at {source}")
                continue
            if kind == "tree":
                if not source.is_dir() or source.is_symlink():
                    errors.append(f"runtime dependency is not the frozen directory: {source}")
                    continue
                actual, count = _runtime_tree_digest(source)
                if actual != entry.get("sha256") or count != entry.get("entries"):
                    errors.append(f"runtime dependency tree drift at {source}")
            elif kind == "file":
                if not source.is_file() or source.is_symlink():
                    errors.append(f"runtime dependency is not the frozen file: {source}")
                    continue
                if sha256_file(source) != entry.get("sha256") or info.st_size != entry.get("bytes"):
                    errors.append(f"runtime dependency content drift at {source}")
            elif kind == "symlink":
                if not source.is_symlink() or os.readlink(source) != entry.get("target"):
                    errors.append(f"runtime dependency symlink drift at {source}")
                    continue
                if sha256_file(source) != entry.get("sha256") or source.stat().st_size != entry.get("bytes"):
                    errors.append(f"runtime dependency target drift at {source}")
            else:
                errors.append(f"runtime dependency has an unsupported kind: {source}")
        except OSError as exc:
            errors.append(f"runtime dependency is unavailable at {source}: {exc}")
    seen_aliases: set[tuple[str, str]] = set()
    for alias in manifest["aliases"]:
        destination, target, roles = alias.get("destination"), alias.get("target"), alias.get("roles")
        if not isinstance(destination, str) or not destination.startswith("/") or ".." in Path(destination).parts:
            errors.append("runtime dependency alias has an unsafe destination")
            continue
        if not isinstance(target, str) or not target or ".." in Path(target).parts:
            errors.append(f"runtime dependency alias has an unsafe target at {destination}")
            continue
        if not isinstance(roles, list) or not roles or any(role not in ("subject", "observer") for role in roles):
            errors.append(f"runtime dependency alias has an invalid role list at {destination}")
            continue
        for role in roles:
            key = (role, destination)
            if key in seen_aliases:
                errors.append(f"runtime dependency alias is duplicated for {role}: {destination}")
            seen_aliases.add(key)
    executable = manifest.get("subject_executable") or {}
    if profile is not None:
        runtime = profile.get("provider_runtime") or {}
        executable_path = Path(str(runtime.get("executable_path", "")))
        try:
            if (not executable_path.is_file()
                    or executable_path.stat().st_size != executable.get("bytes")
                    or sha256_file(executable_path) != executable.get("sha256")):
                errors.append("runtime dependency OMP executable differs from the manifest")
        except OSError as exc:
            errors.append(f"runtime dependency OMP executable is unavailable: {exc}")
    return errors


def _dependencies_for_role(role: str) -> list[dict[str, Any]]:
    return [entry for entry in runtime_dependency_manifest()["dependencies"] if role in entry.get("roles", [])]


def _materialize_runtime_dependencies(paths: dict[str, Path]) -> dict[str, Any]:
    """Copy verified manifest entries into per-principal run-owned roots for read-only binding."""
    manifest = runtime_dependency_manifest()
    results: dict[str, Any] = {}
    for role in ("subject", "observer"):
        root = paths[f"{role}_runtime"]
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        mounted: list[str] = []
        for entry in manifest["dependencies"]:
            if role not in entry.get("roles", []):
                continue
            destination = str(entry["destination"])
            if role == "observer" and destination.startswith("/etc/"):
                continue  # certificate material is copied into synthetic /etc below.
            source = Path(str(entry["source"]))
            target = root / destination.lstrip("/")
            target.parent.mkdir(parents=True, exist_ok=True)
            if entry.get("kind") == "tree":
                shutil.copytree(source, target, symlinks=True, copy_function=shutil.copy2)
            elif entry.get("kind") in ("file", "symlink"):
                shutil.copy2(source, target, follow_symlinks=True)
            else:
                raise AdapterError(f"runtime dependency has an unsupported materialization kind: {source}")
            if entry.get("kind") == "tree":
                copied_digest, copied_entries = _runtime_tree_digest(target)
                if copied_digest != entry.get("sha256") or copied_entries != entry.get("entries"):
                    raise AdapterError(f"staged runtime dependency tree differs from its manifest: {source}")
            elif sha256_file(target) != entry.get("sha256"):
                raise AdapterError(f"staged runtime dependency file differs from its manifest: {source}")
            mounted.append(destination)
        for alias in manifest["aliases"]:
            if role not in alias.get("roles", []):
                continue
            destination = str(alias["destination"])
            if not destination.startswith("/usr/"):
                continue  # top-level /bin and /lib aliases are installed by bubblewrap.
            target = root / destination.lstrip("/")
            target.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(str(alias["target"]), target)
            mounted.append(destination)
        tree_digest, entry_count = _runtime_tree_digest(root)
        results[role] = {"tree_sha256": tree_digest, "entries": entry_count, "paths": sorted(mounted)}
    return results


def _policy(profile: dict[str, Any]) -> dict[str, Any]:
    policy = profile.get("containment_policy")
    if not isinstance(policy, dict) or policy.get("kind") != CONTAINMENT_KIND:
        raise AdapterError("OMP profile lacks the required three-principal containment policy")
    return policy


def profile_errors(profile: dict[str, Any]) -> list[str]:
    """Everything the profile must freeze before this adapter will run a subject."""
    errors: list[str] = []
    if _contains_unfrozen(profile):
        errors.append("OMP execution profile contains an unfrozen marker; profile is not frozen")
    try:
        policy = _policy(profile)
    except AdapterError as exc:
        return errors + [str(exc)]
    runtime = profile.get("provider_runtime") if isinstance(profile.get("provider_runtime"), dict) else {}
    for key in ("executable", "executable_path", "executable_sha256", "version", "provider"):
        if not isinstance(runtime.get(key), str) or not runtime.get(key):
            errors.append(f"provider_runtime.{key} is not frozen")
    if runtime.get("executable_sha256") != OMP_BUILD["sha256"] or runtime.get("version") != OMP_BUILD["version"]:
        errors.append("provider_runtime does not name the exact reviewed OMP build (version/sha256)")
    substrate = policy.get("substrate") if isinstance(policy.get("substrate"), dict) else {}
    for key in ("executable", "executable_sha256"):
        if not isinstance(substrate.get(key), str) or not substrate.get(key):
            errors.append(f"containment substrate {key} is not frozen")
    route = policy.get("provider_route") if isinstance(policy.get("provider_route"), dict) else {}
    for key in ("provider_id", "api", "model_id", "base_path", "upstream", "credential_env", "placeholder_key"):
        if not isinstance(route.get(key), str) or not route.get(key):
            errors.append(f"provider_route.{key} is not frozen")
    if route.get("api") not in API_ENDPOINTS:
        errors.append(f"provider_route.api {route.get('api')!r} is outside the reviewed D4 tranche")
    for key in ("context_window", "max_tokens"):
        if not isinstance(route.get(key), int) or isinstance(route.get(key), bool) or route[key] <= 0:
            errors.append(f"provider_route.{key} is not frozen")
    if not isinstance(route.get("reasoning"), bool):
        errors.append("provider_route.reasoning is not frozen")
    else:
        thinking = (profile.get("reasoning_configuration") or {}).get("thinking")
        if route["reasoning"] and thinking not in REASONING_EFFORT:
            errors.append(f"frozen thinking level {thinking!r} has no reviewed request-level reasoning binding")
        if not route["reasoning"] and thinking != "off":
            errors.append("a non-reasoning model cannot honor a frozen thinking level other than 'off'")
    if policy.get("settings_closure_sha256") != settings_closure_sha256():
        errors.append("frozen settings-closure digest does not match the adapter's reviewed settings closure")
    manifest_sha = sha256_file(RUNTIME_DEPENDENCIES_PATH)
    if manifest_sha != RUNTIME_DEPENDENCIES_SHA256:
        errors.append("retained runtime dependency manifest differs from the reviewed exact surface")
    if policy.get("runtime_dependency_manifest_sha256") != RUNTIME_DEPENDENCIES_SHA256:
        errors.append("frozen runtime dependency manifest digest does not match the retained exact surface")
    if policy.get("observer_boundary") != OBSERVER_BOUNDARY_POLICY:
        errors.append("observer boundary policy differs from the reviewed least-privilege realization")
    if policy.get("principal_files_sha256") != principal_files_sha256():
        errors.append("frozen principal-file digests do not match the adapter's principal code")
    inventory = policy.get("build_inventory_sha256")
    if inventory != sha256_file(inventory_path()):
        errors.append("frozen build-inventory digest does not match the retained exact-build inventory")
    if profile.get("agent_model") != f"{route.get('provider_id')}/{route.get('model_id')}":
        errors.append("agent_model does not equal provider_route provider_id/model_id")
    budgets = profile.get("budgets") if isinstance(profile.get("budgets"), dict) else {}
    for key in ("max_turns", "timeout_s"):
        if not isinstance(budgets.get(key), int) or isinstance(budgets.get(key), bool) or budgets[key] <= 0:
            errors.append(f"budgets.{key} is not a positive frozen integer")
    ok, binding_errors, _ = verify_mcp_binding(profile)
    if not ok:
        errors.extend(binding_errors)
    if list(profile.get("native_tools") or [])[: len(OMP_BUILTIN_TOOLS)] != list(OMP_BUILTIN_TOOLS):
        errors.append("native_tools does not begin with the reviewed builtin tool surface")
    return errors


def inventory_path() -> Path:
    return EVAL_DIR / "omp-build-inventory-18.0.11.json"


_INVENTORY_CACHE: dict[str, Any] = {}


def load_inventory() -> dict[str, Any]:
    path = inventory_path()
    digest = sha256_file(path)
    if _INVENTORY_CACHE.get("digest") != digest:
        _INVENTORY_CACHE["digest"] = digest
        _INVENTORY_CACHE["value"] = json.loads(path.read_text(encoding="utf-8"))
    return _INVENTORY_CACHE["value"]


def freeze_profile(template: dict[str, Any], *, executable_path: str, provider_route: dict[str, Any],
                   reasoning: dict[str, Any], profile_id: str, budgets: dict[str, Any] | None = None,
                   substrate_executable: str = "/usr/bin/bwrap") -> dict[str, Any]:
    """Fill a profile template with exact digests. Every operator choice is an explicit argument."""
    profile = copy.deepcopy(template)
    profile["profile_id"] = profile_id
    profile["adapter_id"] = ADAPTER_ID
    route = dict(profile["containment_policy"]["provider_route"])
    route.update(provider_route)
    profile["containment_policy"]["provider_route"] = route
    profile["agent_model"] = f"{route['provider_id']}/{route['model_id']}"
    runtime = profile["provider_runtime"]
    runtime["executable_path"] = str(executable_path)
    runtime["provider"] = route["provider_id"]
    profile["reasoning_configuration"] = dict(reasoning)
    if budgets:
        profile["budgets"] = dict(budgets)
    policy = profile["containment_policy"]
    policy["substrate"]["executable"] = substrate_executable
    policy["substrate"]["executable_sha256"] = sha256_file(Path(substrate_executable))
    policy["settings_closure_sha256"] = settings_closure_sha256()
    policy["runtime_dependency_manifest_sha256"] = sha256_file(RUNTIME_DEPENDENCIES_PATH)
    policy["principal_files_sha256"] = principal_files_sha256()
    policy["build_inventory_sha256"] = sha256_file(inventory_path())
    return profile


def _reasoning_argv(profile: dict[str, Any]) -> list[str]:
    reasoning = profile.get("reasoning_configuration")
    if isinstance(reasoning, dict) and reasoning.get("thinking"):
        return ["--thinking", str(reasoning["thinking"])]
    return []


def omp_argv(profile: dict[str, Any], prompt: str) -> list[str]:
    """Launch argv (comparison identity only): exact tool selection, closed discovery, JSON mode."""
    return [
        SB_OMP, "-p", "--mode=json", "--no-session", "--no-title", "--no-extensions", "--no-rules", "--no-lsp",
        "--cwd", SB_PROJECT,
        "--tools", ",".join(OMP_BUILTIN_TOOLS),
        "--model", str(profile.get("agent_model")),
        *_reasoning_argv(profile),
        str(prompt),
    ]


# ------------------------------------------------------------------------------ environment

def clean_env() -> dict[str, str]:
    """Credential-free environment of the harness-side runtime; the subject gets its own below."""
    env = {key: os.environ[key] for key in SAFE_ENV_KEYS if key in os.environ}
    env.setdefault("PATH", MINIMAL_PATH)
    env["NO_COLOR"] = "1"
    env["TERM"] = "dumb"
    return env


def project_control_paths(profile: dict[str, Any]) -> list[str]:
    """OMP control/config/package state lives under the run-owned private root; none in the project."""
    return []


def _subject_env() -> dict[str, str]:
    return {
        "PATH": MINIMAL_PATH,
        "HOME": SB_HOME,
        "XDG_CONFIG_HOME": f"{SB_HOME}/.config",
        "XDG_CACHE_HOME": f"{SB_HOME}/.cache",
        "TMPDIR": f"{SB_PROJECT}/.qualification-tmp",
        "TMP": f"{SB_PROJECT}/.qualification-tmp",
        "TEMP": f"{SB_PROJECT}/.qualification-tmp",
        "TERM": "dumb",
        "NO_COLOR": "1",
        "LANG": "C.UTF-8",
        "TZ": "UTC",
        "PI_NO_TITLE": "1",
    }


def _private_root(env: dict[str, str]) -> Path:
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise AdapterError("contained OMP launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    if home == Path(os.path.expanduser("~")).resolve():
        raise AdapterError("contained OMP launch may not inherit the ambient user home")
    return home.parent


def _paths(project: Path, env: dict[str, str]) -> dict[str, Path]:
    private = _private_root(env)
    home = Path(env["HOME"]).resolve()
    project_resolved = project.resolve()
    if home == project_resolved or project_resolved in home.parents or home in project_resolved.parents:
        raise AdapterError("run-owned HOME must remain outside the executor working directory")
    if private == project_resolved or private in project_resolved.parents:
        raise AdapterError("harness-private root may not contain the executor working directory")
    return {
        "private": private,
        "home": home,
        "project": project_resolved,
        "skills": private / "omp-skills",
        "control": private / "omp-control",
        "etc": private / "omp-etc",
        "observer_etc": private / "omp-observer-etc",
        "observer": private / "omp-observer-runtime",
        "subject_runtime": private / "omp-runtime-subject",
        "observer_runtime": private / "omp-runtime-observer",
        "agent": home / ".omp" / "agent",
    }


# ------------------------------------------------------------------------------ installation

def install_skills(dist: Path, project: Path, env: dict[str, str] | None = None) -> Path:
    """Install the arm's protocol package OUTSIDE the project, to be mounted read-only in the sandbox."""
    if env is None:
        raise AdapterError("OMP skill installation requires the run-owned environment")
    target = _paths(project, env)["skills"]
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for skill in sorted(SSDP_SKILLS):
        source = Path(dist) / skill
        if not source.is_dir():
            raise AdapterError(f"prepared arm is missing protocol skill {skill!r}")
        shutil.copytree(source, target / skill)
    return target


# ------------------------------------------------------------------------------ realization

def models_document(profile: dict[str, Any]) -> dict[str, Any]:
    route = _policy(profile)["provider_route"]
    return {
        "providers": {
            route["provider_id"]: {
                "baseUrl": f"http://127.0.0.1:{RELAY_PORTS['inference']}{route['base_path']}",
                "apiKey": route["placeholder_key"],
                "api": route["api"],
                "models": [{
                    "id": route["model_id"],
                    "name": route["model_id"],
                    "reasoning": bool(route["reasoning"]),
                    "input": ["text"],
                    "contextWindow": route["context_window"],
                    "maxTokens": route["max_tokens"],
                }],
            }
        }
    }


def mcp_document() -> dict[str, Any]:
    return {"mcpServers": {OMP_MCP_SERVER_NAME: {
        "type": "http", "url": f"http://127.0.0.1:{RELAY_PORTS['mcp']}/mcp",
    }}}


def _yaml(document: dict[str, Any]) -> bytes:
    return yaml.safe_dump(document, sort_keys=True, default_flow_style=False).encode("utf-8")


def _json_bytes(document: dict[str, Any]) -> bytes:
    return (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")


def control_documents(profile: dict[str, Any]) -> dict[str, bytes]:
    return {
        ".omp/agent/config.yml": _yaml(settings_document()),
        ".omp/agent/models.yml": _yaml(models_document(profile)),
        ".omp/agent/mcp.json": _json_bytes(mcp_document()),
    }


def etc_documents() -> dict[str, bytes]:
    uid, gid = os.getuid(), os.getgid()
    return {
        "passwd": f"agent:x:{uid}:{gid}:agent:{SB_HOME}:/bin/bash\n".encode(),
        "group": f"agent:x:{gid}:\n".encode(),
        "nsswitch.conf": b"passwd: files\ngroup: files\nhosts: files\n",
        "hosts": b"127.0.0.1 localhost\n",
        "resolv.conf": b"",
    }


def _observer_etc_documents() -> dict[str, bytes]:
    uid, gid = os.getuid(), os.getgid()
    nameservers: list[str] = []
    try:
        source = Path("/etc/resolv.conf").read_text(encoding="utf-8")
    except OSError:
        source = ""
    for line in source.splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[0] == "nameserver":
            try:
                nameserver = str(ipaddress.ip_address(fields[1].split("%", 1)[0]))
            except ValueError:
                continue
            if nameserver not in nameservers:
                nameservers.append(nameserver)
    documents = {
        "passwd": f"observer:x:{uid}:{gid}:observer:{OBSERVER_HOME}:/bin/false\n".encode(),
        "group": f"observer:x:{gid}:\n".encode(),
        "nsswitch.conf": b"passwd: files\ngroup: files\nhosts: files dns\n",
        "hosts": b"127.0.0.1 localhost\n::1 localhost\n",
        "resolv.conf": ("".join(f"nameserver {item}\n" for item in nameservers) + "options timeout:2 attempts:1\n").encode(),
    }
    ca_path = Path("/etc/ssl/certs/ca-certificates.crt")
    documents["ssl/certs/ca-certificates.crt"] = ca_path.read_bytes()
    return documents


def _tree_manifest(root: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    if root.is_file():
        return {".": sha256_file(root)}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            rows[path.relative_to(root).as_posix()] = "symlink:" + os.readlink(path)
        elif path.is_file():
            rows[path.relative_to(root).as_posix()] = sha256_file(path)
    return rows


def _write_control_tree(paths: dict[str, Path], profile: dict[str, Any]) -> dict[str, Any]:
    """Create every immutable control input and return the digest manifest bound before launch."""
    home, agent = paths["home"], paths["agent"]
    agent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {"home_control": {}, "control_dir": {}, "etc": {}, "observer_code": {},
                                "observer_etc": {}}
    for rel, data in control_documents(profile).items():
        target = home / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o444)
        manifest["home_control"][rel] = sha256_bytes(data)
    control = paths["control"]
    if control.exists():
        shutil.rmtree(control)
    control.mkdir(parents=True)
    for name in ("subject_launcher.py", "evidence70.py", "muxhttp70.py"):
        shutil.copy2(EVAL_DIR / name, control / name)
        (control / name).chmod(0o444)
        manifest["control_dir"][name] = sha256_file(control / name)
    etc = paths["etc"]
    if etc.exists():
        shutil.rmtree(etc)
    etc.mkdir(parents=True)
    for name, data in etc_documents().items():
        (etc / name).write_bytes(data)
        manifest["etc"][name] = sha256_bytes(data)
    observer = paths["observer"]
    if observer.exists():
        shutil.rmtree(observer)
    observer.mkdir(parents=True)
    for name in ("observer70.py", "evidence70.py", "muxhttp70.py", "seccomp70.py"):
        shutil.copy2(EVAL_DIR / name, observer / name)
        (observer / name).chmod(0o444)
        manifest["observer_code"][name] = sha256_file(observer / name)
    observer_etc = paths["observer_etc"]
    if observer_etc.exists():
        shutil.rmtree(observer_etc)
    observer_etc.mkdir(parents=True)
    for name, data in _observer_etc_documents().items():
        target = observer_etc / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest["observer_etc"][name] = sha256_bytes(data)
    manifest["runtime_surface"] = _materialize_runtime_dependencies(paths)
    return manifest


def _verify_control_tree(paths: dict[str, Path], manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for rel, digest in (manifest.get("home_control") or {}).items():
        path = paths["home"] / rel
        if not path.is_file() or sha256_file(path) != digest:
            errors.append(f"immutable OMP control file {rel!r} is absent or changed")
    for name, digest in (manifest.get("control_dir") or {}).items():
        path = paths["control"] / name
        if not path.is_file() or sha256_file(path) != digest:
            errors.append(f"immutable launcher control file {name!r} is absent or changed")
    for name, digest in (manifest.get("etc") or {}).items():
        path = paths["etc"] / name
        if not path.is_file() or sha256_file(path) != digest:
            errors.append(f"immutable sandbox /etc file {name!r} is absent or changed")
    for name, digest in (manifest.get("observer_code") or {}).items():
        path = paths["observer"] / name
        if not path.is_file() or sha256_file(path) != digest:
            errors.append(f"immutable observer control file {name!r} is absent or changed")
    for name, digest in (manifest.get("observer_etc") or {}).items():
        path = paths["observer_etc"] / name
        if not path.is_file() or sha256_file(path) != digest:
            errors.append(f"immutable observer /etc file {name!r} is absent or changed")
    for role in ("subject", "observer"):
        expected = (manifest.get("runtime_surface") or {}).get(role) or {}
        runtime_root = paths[f"{role}_runtime"]
        try:
            actual_digest, actual_count = _runtime_tree_digest(runtime_root)
        except (AdapterError, OSError) as exc:
            errors.append(f"staged {role} runtime dependency tree is unreadable: {exc}")
            continue
        if actual_digest != expected.get("tree_sha256") or actual_count != expected.get("entries"):
            errors.append(f"staged {role} runtime dependency tree changed during execution")
    expected_control = set((manifest.get("control_dir") or {}))
    if paths["control"].is_dir() and {p.name for p in paths["control"].iterdir()} - expected_control - {"launcher.json"}:
        errors.append("unexpected entries appeared in the immutable launcher control directory")
    return errors


def _scan_sources(root: Path, relatives: tuple[str, ...]) -> list[str]:
    return [rel for rel in relatives if os.path.lexists(root / rel)]


def discovery_baseline(project: Path, home: Path) -> dict[str, Any]:
    """Pre-launch discovery inventory of the run-owned project and HOME (exact-build source list)."""
    project_hits = _scan_sources(project, PROJECT_DISCOVERY_SOURCES)
    home_hits = _scan_sources(home, HOME_DISCOVERY_SOURCES)
    home_entries = sorted(
        p.relative_to(home).as_posix() for p in home.rglob("*") if p.is_file() or p.is_symlink()
    )
    unexpected_home = [
        rel for rel in home_entries
        if rel not in CONTROL_FILES_IN_HOME and not any(re.match(pattern, rel) for pattern in HOME_RUNTIME_STATE_PATTERNS)
    ]
    return {
        "project_discovery_sources_present": project_hits,
        "home_discovery_sources_present": home_hits,
        "home_entries": home_entries,
        "home_unexpected_entries": unexpected_home,
    }


def validate_ambient_discovery_closure(project: Path, env: dict[str, str]) -> list[str]:
    errors: list[str] = []
    try:
        paths = _paths(project, env)
    except AdapterError as exc:
        return [str(exc)]
    baseline = discovery_baseline(paths["project"], paths["home"])
    for rel in baseline["project_discovery_sources_present"]:
        errors.append(f"project-local provider discovery source {rel!r} is present and may enter the runtime")
    for rel in baseline["home_discovery_sources_present"]:
        errors.append(f"run-owned HOME discovery source {rel!r} is present and may enter the runtime")
    for rel in baseline["home_unexpected_entries"]:
        errors.append(f"run-owned HOME holds unexpected pre-launch entry {rel!r}")
    for name in CREDENTIAL_ENV_NAMES:
        if name in env:
            errors.append(f"run environment carries credential variable {name!r}; containment is not closed")
    return errors


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Create and bind every immutable control input; raise unless the frozen profile is admissible."""
    problems = profile_errors(profile)
    if problems:
        raise AdapterError("OMP profile is not admissible for realization: " + "; ".join(problems))
    dependency_errors = runtime_dependency_errors(profile)
    if dependency_errors:
        raise AdapterError("OMP explicit runtime dependency surface is inadmissible: " + "; ".join(dependency_errors))
    paths = _paths(project, env)
    policy = _policy(profile)
    runtime = profile["provider_runtime"]
    exe = Path(runtime["executable_path"])
    if not exe.is_file() or sha256_file(exe) != OMP_BUILD["sha256"] or exe.stat().st_size != OMP_BUILD["bytes"]:
        raise AdapterError("OMP executable differs from the exact frozen build (sha256/size)")
    substrate = Path(policy["substrate"]["executable"])
    if not substrate.is_file() or sha256_file(substrate) != policy["substrate"]["executable_sha256"]:
        raise AdapterError("containment substrate executable digest mismatch")
    layout = core70.private_mcp_paths(paths["private"])
    for label in ("server", "log", "account"):
        if not layout[label].is_file():
            raise AdapterError(f"harness-private MCP {label} is absent; the shared private layout was not created")
    if not layout["stub"].is_dir():
        raise AdapterError("harness-private MCP stub root is absent")
    if sha256_file(layout["server"]) != sha256_file(EVAL_DIR / "stub_tools" / "mediator.py"):
        raise AdapterError("harness-private MCP server differs from the reviewed mediator")
    discovery = validate_ambient_discovery_closure(project, env)
    if discovery:
        raise AdapterError("OMP ambient discovery is not closed: " + "; ".join(discovery))
    manifest = _write_control_tree(paths, profile)
    mcp_sha = manifest["home_control"][".omp/agent/mcp.json"]
    server_sha = sha256_file(layout["server"])
    return {
        "schema": 2,
        "kind": CONTAINMENT_KIND,
        "realization": {
            "principals": ["qualification-supervisor", "provider-control-observer", "subject-executor"],
            "project": str(paths["project"]),
            "runtime_home": str(paths["home"]),
            "private_root": str(paths["private"]),
            "settings_sha256": manifest["home_control"][".omp/agent/config.yml"],
            "mcp_config_sha256": mcp_sha,
            "models_sha256": manifest["home_control"][".omp/agent/models.yml"],
            "control_manifest": manifest,
            "runtime_dependency_manifest_sha256": sha256_file(RUNTIME_DEPENDENCIES_PATH),
            "runtime_dependency_surface": runtime_dependency_manifest(),
            "runtime_dependency_staging": manifest["runtime_surface"],
            "principal_files_sha256": principal_files_sha256(),
            "settings_closure_sha256": settings_closure_sha256(),
            "build_inventory_sha256": sha256_file(inventory_path()),
            "mcp_servers": [{
                "name": OMP_MCP_SERVER_NAME,
                "transport": "stdio",
                "server_id": OMP_MCP_SERVER_ID,
                "entrypoint": OMP_MCP_SERVER_ENTRYPOINT,
                "executable_file": str(layout["server"]),
                "executable_sha256": server_sha,
                "realization": "unchanged stdio mediator run by the supervisor; reached by OMP as streamable-HTTP MCP through the supervisor bridge",
                "tools": list(profile["mcp_servers"][0]["tools"]),
            }],
            "network": "subject network namespace has loopback only; no host route",
            "filesystem_view": {
                "read_only": ["manifest-listed runtime dependencies only", "/etc(synthetic)", "/opt/omp/omp",
                              "/opt/ssdp/skills", "/opt/ssdp/ctl"],
                "read_write": [SB_PROJECT, SB_HOME, SB_TMP],
                "control_files_read_only_inside_home": list(CONTROL_FILES_IN_HOME),
                "absent": ["unlisted /usr software", "host HOME", "custody/private harness state",
                           "observer/bridge evidence"],
            },
            "discovery_baseline": discovery_baseline(paths["project"], paths["home"]),
            "omp_executable_sha256": OMP_BUILD["sha256"],
            "substrate_executable_sha256": policy["substrate"]["executable_sha256"],
        },
    }


def validate_containment_realization(profile: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    try:
        paths = _paths(project, env)
        expected = control_documents(profile)
    except (AdapterError, OSError) as exc:
        return [str(exc)]
    errors: list[str] = []
    for rel, data in expected.items():
        path = paths["home"] / rel
        if not path.is_file() or path.read_bytes() != data:
            errors.append(f"run-owned OMP control file {rel!r} differs from the frozen realization")
    return errors


# ------------------------------------------------------------------------------------ launch

def _spawn_principal(argv: list[str], pass_fds: tuple[int, ...], env: dict[str, str]) -> subprocess.Popen:
    return subprocess.Popen(argv, pass_fds=pass_fds, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)


def _await_ready(proc: subprocess.Popen, name: str, expected: bytes = b"ready") -> None:
    ready = threading.Event()
    box: dict[str, bytes] = {}

    def read() -> None:
        assert proc.stdout is not None
        box["line"] = proc.stdout.readline()
        ready.set()

    threading.Thread(target=read, daemon=True).start()
    if not ready.wait(30) or box.get("line", b"").strip() != expected:
        proc.kill()
        err = proc.stderr.read(2000).decode("utf-8", "replace") if proc.stderr else ""
        raise AdapterError(f"{name} principal did not become ready: {err}")


def _drain(fd: int, sink: bytearray) -> threading.Thread:
    def run() -> None:
        while True:
            try:
                chunk = os.read(fd, 1 << 16)
            except OSError:
                return
            if not chunk:
                return
            sink.extend(chunk)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


def _bwrap_argv(profile: dict[str, Any], paths: dict[str, Path], seccomp_fd: int,
                launcher_config: str, sandbox_exe: str) -> list[str]:
    policy = _policy(profile)
    runtime = profile["provider_runtime"]
    argv = [
        policy["substrate"]["executable"],
        "--unshare-user", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--unshare-cgroup", "--unshare-net",
        "--die-with-parent", "--new-session", "--as-pid-1", "--clearenv", "--cap-drop", "ALL", "--hostname", "ssdp-subject",
        "--seccomp", str(seccomp_fd),
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", SB_TMP,
    ]
    argv += _runtime_mount_args("subject", paths)
    argv += [
        "--dir", "/etc", "--dir", "/home", "--dir", SB_HOME,
        "--dir", "/workspace", "--dir", "/opt", "--dir", "/opt/omp", "--dir", "/opt/ssdp",
        "--ro-bind", str(paths["etc"]), "/etc",
        "--bind", str(paths["project"]), SB_PROJECT,
        "--bind", str(paths["home"]), SB_HOME,
    ]
    for rel in CONTROL_FILES_IN_HOME:
        argv += ["--ro-bind", str(paths["home"] / rel), f"{SB_HOME}/{rel}"]
    argv += [
        "--ro-bind", str(paths["skills"]), SB_SKILLS,
        "--ro-bind", str(paths["control"]), SB_CTL,
        "--ro-bind", runtime["executable_path"], sandbox_exe,
        "--chdir", "/",
        "/usr/bin/python3", f"{SB_CTL}/subject_launcher.py", launcher_config,
    ]
    return argv


def _runtime_mount_args(role: str, paths: dict[str, Path]) -> list[str]:
    """Bind the staged, manifest-derived dependency roots read-only, never host /usr."""
    root = paths[f"{role}_runtime"]
    if not (root / "usr").is_dir() or not (root / "lib64").is_dir():
        raise AdapterError(f"staged {role} runtime dependency roots are incomplete")
    args = ["--ro-bind", str(root / "usr"), "/usr",
            "--ro-bind", str(root / "lib64"), "/lib64"]
    manifest = runtime_dependency_manifest()
    for alias in manifest["aliases"]:
        if role in alias.get("roles", []) and alias.get("destination") in ("/bin", "/lib"):
            args.extend(("--symlink", str(alias["target"]), str(alias["destination"])))
    return args


def _observer_bwrap_argv(profile: dict[str, Any], paths: dict[str, Path], observer_fds: tuple[int, ...],
                         probe_paths: list[tuple[str, str]], supervisor_pid: int,
                         supervisor_netns: str, supervisor_pidns: str) -> list[str]:
    policy = _policy(profile)
    route = policy["provider_route"]
    argv = [
        policy["substrate"]["executable"],
        "--unshare-user", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--unshare-cgroup", "--share-net",
        "--die-with-parent", "--new-session", "--as-pid-1", "--hostname", "ssdp-observer",
        # bubblewrap 0.6.1 has no --preserve-fds option. The supervisor-owned one-shot exec helper
        # maps only these four channels to 3..6 before it immediately execs Bubblewrap.
        "--cap-drop", "ALL", "--cap-add", "CAP_SYS_ADMIN", "--cap-add", "CAP_SETPCAP",
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", OBSERVER_HOME,
    ]
    argv += _runtime_mount_args("observer", paths)
    argv += [
        "--dir", "/etc", "--dir", "/opt", "--dir", "/opt/ssdp",
        "--ro-bind", str(paths["observer_etc"]), "/etc",
        "--ro-bind", str(paths["observer"]), OBSERVER_CODE,
        "--chdir", "/",
        "/usr/bin/python3", f"{OBSERVER_CODE}/observer70.py",
        "--mux-in-fd", "3", "--mux-out-fd", "4", "--evidence-fd", "5", "--credential-fd", "6",
        "--upstream", route["upstream"], "--credential-env", route["credential_env"],
        "--placeholder", route["placeholder_key"],
        "--allowed-path", route["base_path"].rstrip("/") + API_ENDPOINTS[route["api"]],
        "--max-requests", str(profile["budgets"]["max_turns"]),
        "--supervisor-pid", str(supervisor_pid),
        "--supervisor-netns", supervisor_netns, "--supervisor-pidns", supervisor_pidns,
    ]
    for label, path in probe_paths:
        argv.extend(("--probe-path", f"{label}={path}"))
    return argv


def _sandbox_pipe_fds(pairs: list[tuple[int, int]]) -> tuple[int, ...]:
    return tuple(fd for pair in pairs for fd in pair)


def launch(profile: dict[str, Any], prompt: str, project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Run the exact frozen OMP build for real: principals, sandbox, relay, native JSON trace."""
    problems = profile_errors(profile)
    if problems:
        raise AdapterError("OMP launch refused; profile is not admissible: " + "; ".join(problems))
    dependency_errors = runtime_dependency_errors(profile)
    if dependency_errors:
        raise AdapterError("OMP launch refused; explicit runtime dependency surface drifted: " + "; ".join(dependency_errors))
    paths = _paths(project, env)
    policy = _policy(profile)
    route = policy["provider_route"]
    runtime = profile["provider_runtime"]
    layout = core70.private_mcp_paths(paths["private"])
    discovery = validate_ambient_discovery_closure(project, env)
    if discovery:
        raise AdapterError("OMP launch refused; ambient discovery is not closed: " + "; ".join(discovery))
    if sha256_file(Path(runtime["executable_path"])) != OMP_BUILD["sha256"]:
        raise AdapterError("OMP launch refused; executable differs from the frozen build")
    credential = os.environ.get(route["credential_env"])
    if credential is None:
        raise AdapterError(f"provider credential variable {route['credential_env']!r} is not set for the observer principal")

    # Digests of the immutable inputs at the moment of launch (compared by the harness with the
    # realization it retained, and re-verified after the run).
    home_docs = {rel: sha256_file(paths["home"] / rel) for rel in CONTROL_FILES_IN_HOME}
    mcp_server_sha = sha256_file(layout["server"])
    packages_before = core70.sha256_tree(paths["skills"])
    budgets = profile["budgets"]
    started = time.monotonic()

    def pipe() -> tuple[int, int]:
        return os.pipe()

    infer_up = pipe()      # subject -> observer (observer reads [0], launcher writes [1])
    infer_down = pipe()    # observer -> subject
    mcp_up = pipe()
    mcp_down = pipe()
    credential_r, credential_w = pipe()
    obs_ev, br_ev, ln_ev = pipe(), pipe(), pipe()
    sinks = {"observer": bytearray(), "bridge": bytearray(), "launcher": bytearray()}
    threads: list[threading.Thread] = []
    procs: list[subprocess.Popen] = []
    closed_parent_channel_writers: set[int] = set()
    seccomp_r = seccomp_w = -1
    run_launch = paths["control"] / "launcher.json"
    observer_launch_argv: list[str] = []
    observer_helper_argv: list[str] = []
    observer_pass_fds: tuple[int, ...] = ()
    observer_fd_mapping: dict[str, Any] = {}
    boundary_sentinel = paths["private"] / "observer-boundary-host-sentinel.txt"
    boundary_sentinel.write_text("SUPERVISOR-PRIVATE-OBSERVER-PROBE\n", encoding="utf-8")
    boundary_sentinel.chmod(0o600)
    try:
        threads = [
            _drain(obs_ev[0], sinks["observer"]),
            _drain(br_ev[0], sinks["bridge"]),
            _drain(ln_ev[0], sinks["launcher"]),
        ]
        observer_probe_paths = [
            ("host_home", str(Path.home() / ".bashrc")),
            ("qualification_custody", str(REPO_ROOT / "qualification" / "ssdp70" / "PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md")),
            ("supervisor_private", str(boundary_sentinel)),
            ("mediator_backing_state", str(layout["log"])),
        ]
        observer_env = {"PATH": MINIMAL_PATH, "HOME": OBSERVER_HOME}
        observer_channels = (infer_up[0], infer_down[1], obs_ev[1], credential_r)
        raw_observer_argv = _observer_bwrap_argv(
            profile, paths, observer_channels, observer_probe_paths, os.getpid(),
            os.readlink("/proc/self/ns/net"), os.readlink("/proc/self/ns/pid"))
        observer_command_at = raw_observer_argv.index("/usr/bin/python3")
        observer_args_r, observer_args_w = os.pipe()
        os.write(observer_args_w, b"\0".join(a.encode() for a in raw_observer_argv[1:observer_command_at]) + b"\0")
        os.close(observer_args_w)
        observer_launch_argv = [raw_observer_argv[0], "--args", str(OBSERVER_ARGUMENT_TARGET),
                                *raw_observer_argv[observer_command_at:]]
        observer_pass_fds = tuple(sorted(set((*observer_channels, observer_args_r))))
        observer_fd_mapping = {
            "inference_input": {"supervisor_source_fd": observer_channels[0], "observer_fd": OBSERVER_CHANNEL_TARGETS[0]},
            "inference_output": {"supervisor_source_fd": observer_channels[1], "observer_fd": OBSERVER_CHANNEL_TARGETS[1]},
            "evidence_output": {"supervisor_source_fd": observer_channels[2], "observer_fd": OBSERVER_CHANNEL_TARGETS[2]},
            "credential_input": {"supervisor_source_fd": observer_channels[3], "observer_fd": OBSERVER_CHANNEL_TARGETS[3]},
            "bubblewrap_arguments": {"supervisor_source_fd": observer_args_r, "bubblewrap_fd": OBSERVER_ARGUMENT_TARGET},
        }
        observer_helper_argv = [
            sys.executable, "-I", "-S", str(OBSERVER_EXEC_HELPER),
            ",".join(str(fd) for fd in observer_channels), str(observer_args_r), *observer_launch_argv,
        ]
        try:
            observer = subprocess.Popen(
                observer_helper_argv,
                pass_fds=observer_pass_fds,
                env=observer_env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                close_fds=True)
        finally:
            os.close(observer_args_r)
            try:
                os.close(credential_r)
            except OSError:
                pass
            credential_r = -1
        procs.append(observer)
        bridge_argv = [
            sys.executable, str(EVAL_DIR / "mcp_bridge70.py"),
            "--mux-in-fd", str(mcp_up[0]), "--mux-out-fd", str(mcp_down[1]), "--evidence-fd", str(br_ev[1]),
            "--", sys.executable, str(layout["server"]),
            "--stub-root", str(layout["stub"]), "--side-effect-log", str(layout["log"]),
            "--account-file", str(layout["account"]), "--server-id", OMP_MCP_SERVER_ID,
            "--expected-self-sha256", mcp_server_sha,
        ]
        bridge = _spawn_principal(bridge_argv, (mcp_up[0], mcp_down[1], br_ev[1]), {"PATH": MINIMAL_PATH})
        procs.append(bridge)
        _await_ready(observer, "provider-control/observer boundary", b"boundary-ready")
        credential_bytes = credential.encode("utf-8")
        offset = 0
        while offset < len(credential_bytes):
            offset += os.write(credential_w, credential_bytes[offset:])
        os.close(credential_w)
        credential_w = -1
        credential = ""
        _await_ready(observer, "provider-control/observer")
        _await_ready(bridge, "qualification MCP bridge")

        probes = [
            {"name": "version", "argv": [SB_OMP, "--version"], "timeout_s": 60},
            {"name": "effective-settings", "argv": [SB_OMP, "config", "list", "--json"], "timeout_s": 60},
        ]
        launcher_cfg = {
            "status_fd": ln_ev[1],
            "omp_exe": SB_OMP,
            "omp_exe_sha256": OMP_BUILD["sha256"],
            "relays": [
                {"name": "inference", "port": RELAY_PORTS["inference"], "read_fd": infer_down[0], "write_fd": infer_up[1]},
                {"name": "mcp", "port": RELAY_PORTS["mcp"], "read_fd": mcp_down[0], "write_fd": mcp_up[1]},
            ],
            "env": _subject_env(),
            "omp_argv": omp_argv(profile, prompt),
            "cwd": "/",
            "timeout_s": budgets["timeout_s"],
            "probes": probes,
        }
        run_launch.write_text(json.dumps(launcher_cfg, sort_keys=True), encoding="utf-8")
        run_launch.chmod(0o444)
        seccomp_r, seccomp_w = os.pipe()
        os.write(seccomp_w, seccomp70.build_deny_filter())
        os.close(seccomp_w)
        seccomp_w = -1
        argv = _bwrap_argv(profile, paths, seccomp_r, f"{SB_CTL}/launcher.json", SB_OMP)
        # The full argument list (which names host run directories) is passed over a descriptor so
        # that it is not readable from the sandbox through /proc/<pid>/cmdline.
        args_r, args_w = os.pipe()
        command_at = argv.index("/usr/bin/python3")
        os.write(args_w, b"\0".join(a.encode() for a in argv[1:command_at]) + b"\0")
        os.close(args_w)
        launch_argv = [argv[0], "--args", str(args_r), *argv[command_at:]]
        sandbox_fds = (infer_up[1], infer_down[0], mcp_up[1], mcp_down[0], ln_ev[1], seccomp_r, args_r)
        try:
            done = subprocess.run(launch_argv, capture_output=True, pass_fds=sandbox_fds,
                                  timeout=budgets["timeout_s"] + 90, stdin=subprocess.DEVNULL)
            os.close(args_r)
            returncode = done.returncode
            stdout, stderr = done.stdout.decode("utf-8", "replace"), done.stderr.decode("utf-8", "replace")
        except subprocess.TimeoutExpired as exc:
            returncode = 124
            stdout = (exc.stdout or b"").decode("utf-8", "replace")
            stderr = (exc.stderr or b"").decode("utf-8", "replace") + "\nsandbox supervision timeout"
        # The subject is gone. Close the supervisor-held writers on the two existing
        # request edges so each principal sees EOF and can append its terminal record.
        for fd in (infer_up[1], mcp_up[1]):
            try:
                os.close(fd)
                closed_parent_channel_writers.add(fd)
            except OSError:
                pass
    finally:
        # Give the observer and bridge a chance to close their evidence chains on edge EOF.
        for proc in procs:
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                pass
        for proc in procs:
            if proc.poll() is None:
                try:
                    proc.terminate()
                except OSError:
                    pass
        for proc in procs:
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            for stream in (proc.stdout, proc.stderr):
                if stream is not None:
                    stream.close()
        # Close every write end this process still holds so the drain threads see EOF once the
        # principals have exited, then join them, then close the read ends.
        writers = [infer_up[1], infer_down[1], mcp_up[1], mcp_down[1], obs_ev[1], br_ev[1], ln_ev[1],
                   credential_r, credential_w, seccomp_r, seccomp_w]
        for fd in writers:
            if fd >= 0 and fd not in closed_parent_channel_writers:
                try:
                    os.close(fd)
                except OSError:
                    pass
        for thread in threads:
            thread.join(15)
        for fd in (infer_up[0], infer_down[0], mcp_up[0], mcp_down[0], obs_ev[0], br_ev[0], ln_ev[0]):
            try:
                os.close(fd)
            except OSError:
                pass
        try:
            boundary_sentinel.unlink()
        except FileNotFoundError:
            pass
    wall_s = round(time.monotonic() - started, 3)

    home_docs_after = {rel: sha256_file(paths["home"] / rel) for rel in CONTROL_FILES_IN_HOME}
    runtime_stage_digests = {role: _runtime_tree_digest(paths[f"{role}_runtime"])
                             for role in ("subject", "observer")}
    artifacts: dict[str, Any] = {
        "observer-evidence.jsonl": bytes(sinks["observer"]).decode("utf-8", "replace"),
        "bridge-evidence.jsonl": bytes(sinks["bridge"]).decode("utf-8", "replace"),
        "launcher-evidence.jsonl": bytes(sinks["launcher"]).decode("utf-8", "replace"),
        "sandbox-argv.json": json.dumps({"argv": argv, "launcher": json.loads(run_launch.read_text())}, indent=2, sort_keys=True) + "\n",
        "observer-boundary-argv.json": json.dumps({
            "argv": observer_launch_argv,
            "exec_helper": str(OBSERVER_EXEC_HELPER),
            "exec_helper_sha256": sha256_file(OBSERVER_EXEC_HELPER),
            "pass_fds": list(observer_pass_fds),
            "fd_mapping": observer_fd_mapping,
        }, indent=2, sort_keys=True) + "\n",
        "runtime-dependency-manifest.json": RUNTIME_DEPENDENCIES_PATH.read_text(encoding="utf-8"),
        "runtime-dependency-attestation.json": json.dumps({
            "manifest_sha256": sha256_file(RUNTIME_DEPENDENCIES_PATH),
            "runtime_dependency_errors_after_launch": runtime_dependency_errors(profile),
            "staged_runtime_roots": {
                role: {"path_sha256": digest, "entries": count}
                for role, (digest, count) in runtime_stage_digests.items()
            },
            "mounted_subject_dependencies": [row for row in runtime_dependency_manifest()["dependencies"]
                                              if "subject" in row.get("roles", [])],
            "mounted_observer_dependencies": [row for row in runtime_dependency_manifest()["dependencies"]
                                               if "observer" in row.get("roles", [])],
        }, indent=2, sort_keys=True) + "\n",
        "runtime-home-inventory.json": json.dumps(_home_inventory(paths["home"]), indent=2, sort_keys=True) + "\n",
        "control-digests.json": json.dumps({
            "before": home_docs, "after": home_docs_after,
            "packages_before": packages_before, "packages_after": core70.sha256_tree(paths["skills"]),
        }, indent=2, sort_keys=True) + "\n",
    }
    command_identity = {
        "adapter_id": ADAPTER_ID,
        "executable": runtime["executable"],
        "argv": argv,
        "model": str(profile.get("agent_model")),
        "reasoning_configuration": profile.get("reasoning_configuration"),
        "tools": list(profile.get("native_tools") or []),
        "mcp_servers": list(profile.get("mcp_servers") or []),
        "mcp_server_executable_sha256": {OMP_MCP_SERVER_NAME: mcp_server_sha},
        "settings_file": str(paths["agent"] / "config.yml"),
        "settings_file_sha256": home_docs[".omp/agent/config.yml"],
        "mcp_config_file": str(paths["agent"] / "mcp.json"),
        "mcp_config_sha256": home_docs[".omp/agent/mcp.json"],
        "runtime_version": runtime.get("version"),
        "runtime_dependency_manifest_sha256": sha256_file(RUNTIME_DEPENDENCIES_PATH),
        "runtime_dependency_staging": {
            role: digest for role, (digest, _count) in runtime_stage_digests.items()
        },
        "native_network": "subject netns loopback only",
    }
    return {
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode,
        "wall_s": wall_s,
        "command_identity": command_identity,
        "adapter_artifacts": artifacts,
    }


def _home_inventory(home: Path) -> dict[str, Any]:
    rows = []
    for path in sorted(home.rglob("*")):
        rel = path.relative_to(home).as_posix()
        if path.is_symlink():
            rows.append({"path": rel, "type": "symlink", "target": os.readlink(path)})
        elif path.is_file():
            size = path.stat().st_size
            rows.append({
                "path": rel, "type": "file", "bytes": size,
                "sha256": sha256_file(path) if size <= 8 * 1024 * 1024 else None,
                "class": "control" if rel in CONTROL_FILES_IN_HOME else (
                    "omp-runtime-state" if any(re.match(p, rel) for p in HOME_RUNTIME_STATE_PATTERNS) else "executor-created"),
            })
    return {"schema": 1, "entries": rows}


def post_run_integrity(profile: dict[str, Any], project: Path, env: dict[str, str], containment: dict[str, Any]) -> list[str]:
    """Immutable control/config/package state and discovery post-state, re-verified after execution."""
    errors: list[str] = []
    try:
        paths = _paths(project, env)
    except AdapterError as exc:
        return [str(exc)]
    realization = containment.get("realization") if isinstance(containment, dict) else None
    if not isinstance(realization, dict):
        return ["containment realization record is malformed"]
    errors.extend(_verify_control_tree(paths, realization.get("control_manifest") or {}))
    layout = core70.private_mcp_paths(paths["private"])
    recorded = {row.get("name"): row.get("executable_sha256") for row in realization.get("mcp_servers") or []}
    if not layout["server"].is_file() or sha256_file(layout["server"]) != recorded.get(OMP_MCP_SERVER_NAME):
        errors.append("qualification mediator executable changed during execution")
    runtime = profile.get("provider_runtime") or {}
    exe = Path(str(runtime.get("executable_path")))
    if not exe.is_file() or sha256_file(exe) != OMP_BUILD["sha256"]:
        errors.append("OMP executable changed during execution")
    for rel in _scan_sources(paths["project"], PROJECT_DISCOVERY_SOURCES):
        errors.append(f"post-run project contains provider discovery source {rel!r}")
    expected_manifest_sha = realization.get("runtime_dependency_manifest_sha256")
    if expected_manifest_sha != RUNTIME_DEPENDENCIES_SHA256:
        errors.append("runtime dependency manifest identity differs from the retained containment realization")
    errors.extend(runtime_dependency_errors(profile))
    return errors


def validate_post_run_project_state(profile: dict[str, Any], project: Path) -> list[str]:
    return []


# ------------------------------------------------------------------------ evidence assembly

class Observed:
    """Parsed, verified principal evidence and the facts derived from it."""

    def __init__(self, artifacts: dict[str, Any], profile: dict[str, Any] | None):
        self.errors: list[str] = []
        self.profile = profile or {}
        self.texts = {
            "observer": str(artifacts.get("observer-evidence.jsonl") or ""),
            "bridge": str(artifacts.get("bridge-evidence.jsonl") or ""),
            "launcher": str(artifacts.get("launcher-evidence.jsonl") or ""),
        }
        principals = {
            "observer": "ssdp70-provider-observer-v1",
            "bridge": "ssdp70-mcp-bridge-v1",
            "launcher": "ssdp70-subject-launcher-v1",
        }
        self.records: dict[str, list[dict[str, Any]]] = {}
        for stream, principal in principals.items():
            records, problems = evidence70.parse_chain(self.texts[stream], principal)
            self.records[stream] = records
            self.errors.extend(problems)
        self.requests: list[dict[str, Any]] = []      # {"record", "body", "index"}
        self.responses: dict[int, dict[str, Any]] = {}
        self.budget_exhausted: list[dict[str, Any]] = []
        self._parse_observer()
        self.mcp: list[dict[str, Any]] = []
        self.mcp_initialize: dict[str, Any] | None = None
        self.mcp_tools_list: list[dict[str, Any]] | None = None
        self._parse_bridge()
        self.launcher_facts: dict[str, Any] = {}
        self.probes: dict[str, dict[str, Any]] = {}
        self.denials: list[dict[str, Any]] = []
        self.omp_exit: dict[str, Any] | None = None
        self._parse_launcher()

    # ---- observer
    def _parse_observer(self) -> None:
        response_positions: list[int] = []
        boundary_probes: dict[str, dict[str, Any]] = {}
        boundary: dict[str, Any] | None = None
        route_opened: dict[str, Any] | None = None
        credential_received: dict[str, Any] | None = None
        observer_started = False
        for position, record in enumerate(self.records["observer"]):
            data = record.get("data") or {}
            kind = record.get("kind")
            if kind == "start":
                observer_started = True
            elif kind == "provider_route_opened":
                if route_opened is not None:
                    self.errors.append("observer recorded multiple provider route capabilities")
                route_opened = data
            elif kind == "boundary":
                if boundary is not None:
                    self.errors.append("observer recorded multiple privilege boundaries")
                boundary = data
            elif kind == "credential_received":
                if credential_received is not None:
                    self.errors.append("observer recorded multiple provider credential deliveries")
                credential_received = data
            elif kind == "boundary_probe":
                name = data.get("name")
                if not isinstance(name, str) or name in boundary_probes:
                    self.errors.append(f"observer boundary probe record {position} is unbound or duplicated")
                else:
                    boundary_probes[name] = data
            elif kind == "boundary_setup_failed":
                self.errors.append("observer least-privilege boundary setup failed")
            elif kind == "request":
                try:
                    raw_body = base64.b64decode(data["body_b64"], validate=True)
                    body = json.loads(raw_body)
                except (KeyError, ValueError, TypeError):
                    self.errors.append(f"observer request record {position} body is unreadable")
                    continue
                if data.get("body_bytes") != len(raw_body):
                    self.errors.append(f"observer request record {position} body length does not match its retained bytes")
                if hashlib.sha256(raw_body).hexdigest() != data.get("body_sha256"):
                    self.errors.append(f"observer request record {position} body does not match its digest")
                self.requests.append({"record": record, "position": position, "body": body, "index": data.get("request_index")})
            elif kind == "response":
                index = data.get("request_index")
                if not isinstance(index, int) or isinstance(index, bool) or index < 0:
                    self.errors.append(f"observer response record {position} has an invalid request index")
                    continue
                if index in self.responses:
                    self.errors.append(f"observer response index {index} is duplicated")
                    continue
                try:
                    retained = base64.b64decode(data.get("body_b64", ""), validate=True)
                except (ValueError, TypeError):
                    self.errors.append(f"observer response record {position} body is unreadable")
                    continue
                total = data.get("body_bytes")
                truncated = data.get("body_truncated_in_evidence")
                if not isinstance(total, int) or isinstance(total, bool) or total < 0:
                    self.errors.append(f"observer response record {position} has an invalid body length")
                elif len(retained) > total:
                    self.errors.append(f"observer response record {position} retains more bytes than the provider returned")
                if not isinstance(truncated, bool):
                    self.errors.append(f"observer response record {position} lacks an explicit truncation disposition")
                elif truncated:
                    self.errors.append(f"observer response record {position} was truncated in evidence and is inadmissible")
                if truncated is False and isinstance(total, int) and len(retained) != total:
                    self.errors.append(f"observer response record {position} is incomplete without a truncation marker")
                if truncated is False and hashlib.sha256(retained).hexdigest() != data.get("body_sha256"):
                    self.errors.append(f"observer response record {position} body does not match its complete digest")
                if data.get("error") is not None:
                    self.errors.append(f"observer response record {position} reports a transport error")
                response_positions.append(index)
                self.responses[index] = {"record": record, "position": position}
            elif kind == "budget_exhausted":
                self.budget_exhausted.append({"record": record, "position": position})
            elif kind == "refused":
                self.errors.append(f"observer refused an inference-transport operation: {data.get('reason')}")
        if response_positions != sorted(response_positions):
            self.errors.append("observer provider responses were reordered")
        request_indices = [row["index"] for row in self.requests]
        if request_indices != list(range(len(request_indices))):
            self.errors.append("observer provider requests are missing, duplicated or reordered")
        if set(self.responses) - set(request_indices):
            self.errors.append("observer contains a response without a corresponding provider request")
        if set(request_indices) - set(self.responses):
            self.errors.append("observer is missing a provider response record")
        if not observer_started:
            self.errors.append("observer start evidence is missing")
        if not route_opened or route_opened.get("connected") is not True or not route_opened.get("connected_peer_addresses"):
            self.errors.append("observer did not retain a successful frozen provider-route connection")
        else:
            route = ((self.profile.get("containment_policy") or {}).get("provider_route") or {})
            parsed = urlsplit(str(route.get("upstream", "")))
            expected_origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None
            if route_opened.get("frozen_origin") != expected_origin:
                self.errors.append("observer provider connection does not match the frozen provider route")
        if boundary is None:
            self.errors.append("observer least-privilege boundary evidence is missing")
        else:
            if boundary.get("network_namespace") == boundary.get("supervisor_network_namespace"):
                self.errors.append("observer remains in the supervisor network namespace")
            if boundary.get("pid_namespace") == boundary.get("supervisor_pid_namespace"):
                self.errors.append("observer remains in the supervisor PID namespace")
            status = boundary.get("status") or {}
            if status.get("NoNewPrivs") != "1" or status.get("Seccomp") != "2":
                self.errors.append("observer no-new-privileges or seccomp lockdown is absent")
            for capability_set in ("CapEff", "CapPrm", "CapBnd"):
                try:
                    if int(status.get(capability_set, "-1"), 16) != 0:
                        self.errors.append(f"observer retains capability bits in {capability_set}")
                except (TypeError, ValueError):
                    self.errors.append(f"observer capability status {capability_set} is unreadable")
            if boundary.get("boundary_probe_count") != len(OBSERVER_REQUIRED_PROBES):
                self.errors.append("observer boundary probe count does not match the required probe set")
        if (credential_received is None or credential_received.get("received_after_lockdown") is not True
                or not isinstance(credential_received.get("bytes"), int) or credential_received.get("bytes", 0) <= 0):
            self.errors.append("observer did not receive its provider credential after privilege lockdown")
        if set(boundary_probes) != set(OBSERVER_REQUIRED_PROBES):
            self.errors.append("observer hostile boundary probe set is incomplete")
        for name in OBSERVER_REQUIRED_PROBES:
            result = boundary_probes.get(name) or {}
            expected_disposition = "unavailable" if name == "credential-environment" else "denied"
            if result.get("disposition") != expected_disposition:
                self.errors.append(f"observer hostile boundary probe {name!r} did not fail closed")
            if name not in {"host_home", "qualification_custody", "supervisor_private", "mediator_backing_state",
                            "credential-environment"} and result.get("errno") != 1:
                self.errors.append(f"observer hostile syscall probe {name!r} was not denied with EPERM")

    # ---- bridge
    def _parse_bridge(self) -> None:
        pending: dict[int, dict[str, Any]] = {}
        for position, record in enumerate(self.records["bridge"]):
            data = record.get("data") or {}
            kind = record.get("kind")
            if kind == "mcp_request":
                try:
                    message = json.loads(base64.b64decode(data.get("body_b64", "")) or b"null")
                except ValueError:
                    self.errors.append(f"bridge request record {position} body is unreadable")
                    continue
                pending[data.get("exchange_index")] = {"request": message, "position": position, "response": None}
            elif kind == "mcp_response":
                exchange = pending.get(data.get("exchange_index"))
                if exchange is None:
                    self.errors.append(f"bridge response record {position} has no request")
                    continue
                exchange["response_position"] = position
                exchange["status"] = data.get("status")
                if data.get("body_b64"):
                    try:
                        exchange["response"] = json.loads(base64.b64decode(data["body_b64"]))
                    except ValueError:
                        self.errors.append(f"bridge response record {position} body is unreadable")
            elif kind == "refused":
                if data.get("reason") != "server-initiated-stream-not-offered":
                    self.errors.append(f"MCP bridge refused an operation: {data.get('reason')}")
        self.mcp = [pending[key] for key in sorted(pending)]
        for exchange in self.mcp:
            request = exchange["request"]
            if not isinstance(request, dict):
                continue
            response = exchange.get("response")
            if request.get("method") == "initialize" and isinstance(response, dict):
                self.mcp_initialize = response.get("result")
            elif request.get("method") == "tools/list" and isinstance(response, dict):
                tools = (response.get("result") or {}).get("tools")
                if isinstance(tools, list):
                    self.mcp_tools_list = tools

    # ---- launcher
    def _parse_launcher(self) -> None:
        for position, record in enumerate(self.records["launcher"]):
            data = record.get("data") or {}
            kind = record.get("kind")
            if kind == "launcher_start":
                self.launcher_facts = dict(data)
            elif kind == "launcher_refused":
                self.errors.append(f"launcher refused to start OMP: {data.get('reason')}")
            elif kind == "omp_started":
                self.launcher_facts["omp_started"] = dict(data)
            elif kind == "probe":
                self.probes[str(data.get("name"))] = dict(data)
            elif kind == "relay_denied":
                self.denials.append({"record": record, "position": position})
            elif kind == "omp_exit":
                self.omp_exit = dict(data)

    # ---- derived facts
    def probe_text(self, name: str) -> str | None:
        probe = self.probes.get(name)
        if not probe or probe.get("returncode") != 0:
            return None
        return base64.b64decode(probe.get("stdout_b64", "")).decode("utf-8", "replace")

    def runtime_version(self) -> str | None:
        text = self.probe_text("version")
        if text is None:
            return None
        match = re.fullmatch(r"\s*omp/(\S+)\s*", text)
        return match.group(1) if match else None

    def effective_settings(self) -> dict[str, Any] | None:
        text = self.probe_text("effective-settings")
        if text is None:
            return None
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            return None
        return value if isinstance(value, dict) else None

    def tool_names(self, body: dict[str, Any]) -> list[str] | None:
        tools = body.get("tools")
        if not isinstance(tools, list):
            return None
        names: list[str] = []
        for tool in tools:
            function = tool.get("function") if isinstance(tool, dict) else None
            if not isinstance(function, dict) or not isinstance(function.get("name"), str):
                return None
            names.append(function["name"])
        return names


def _response_facts(observed: "Observed", request_index: Any) -> dict[str, Any]:
    row = observed.responses.get(request_index)
    facts: dict[str, Any] = {"status": None, "empty_completion": False, "error": None}
    if row is None:
        facts["error"] = "no response record"
        return facts
    data = row["record"].get("data") or {}
    facts["status"] = data.get("upstream_status")
    facts["error"] = data.get("error")
    if facts["status"] == 200 and not data.get("body_truncated_in_evidence"):
        try:
            body = base64.b64decode(data.get("body_b64", "")).decode("utf-8", "replace")
        except ValueError:
            return facts
        text, calls, completion_tokens = "", 0, None
        for line in body.split("\n"):
            if line.startswith("data:") and line[5:].strip() not in ("", "[DONE]"):
                try:
                    chunk = json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
                for choice in chunk.get("choices") or []:
                    delta = choice.get("delta") or {}
                    text += delta.get("content") or "" if isinstance(delta.get("content"), str) else ""
                    calls += len(delta.get("tool_calls") or [])
                usage = chunk.get("usage")
                if isinstance(usage, dict):
                    completion_tokens = usage.get("completion_tokens")
        facts["empty_completion"] = not text and calls == 0 and (completion_tokens or 0) <= 1
    return facts


def group_inference_requests(observed: "Observed") -> tuple[list[list[int]], list[str], list[dict[str, Any]]]:
    """Group observer requests into assistant turns, accounting provider-layer retries explicitly.

    Returns (groups of indexes into observed.requests, errors, retry ledger). A request continues the
    previous group only if its body is byte-identical and the previous response was a transient error or an
    empty completion; the per-kind retry limits of the exact build are enforced.
    """
    groups: list[list[int]] = []
    ledger: list[dict[str, Any]] = []
    errors: list[str] = []
    error_retries = empty_retries = 0
    for position, entry in enumerate(observed.requests):
        digest = (entry["record"].get("data") or {}).get("body_sha256")
        if groups:
            previous = observed.requests[groups[-1][-1]]
            if (previous["record"].get("data") or {}).get("body_sha256") == digest:
                facts = _response_facts(observed, previous["index"])
                transient = facts["status"] is None or facts["status"] in RETRYABLE_STATUS or (
                    isinstance(facts["status"], int) and facts["status"] >= 500)
                if facts["status"] == 200 and facts["empty_completion"]:
                    empty_retries += 1
                    kind = "empty-completion"
                    if empty_retries > MAX_EMPTY_COMPLETION_RETRIES:
                        errors.append("more provider-layer empty-completion retries than the exact build performs")
                elif facts["status"] != 200 and transient:
                    error_retries += 1
                    kind = "transient-provider-error"
                    if error_retries > MAX_PROVIDER_ERROR_RETRIES:
                        errors.append("more provider-layer error retries than the exact build performs")
                else:
                    errors.append(
                        f"inference request {entry['index']} repeats its predecessor after a response that is not a retryable "
                        f"failure (status {facts['status']!r}): an unaccounted hidden call")
                    kind = "unexplained-duplicate"
                groups[-1].append(position)
                ledger.append({"request_index": entry["index"], "of_previous_request_index": previous["index"], "kind": kind,
                               "previous_status": facts["status"]})
                continue
        groups.append([position])
        error_retries = empty_retries = 0
    return groups, errors, ledger


def provider_turns(observed: "Observed") -> list[dict[str, Any]]:
    """What the provider actually answered, reconstructed from the observer's raw response bodies."""
    turns: list[dict[str, Any]] = []
    groups, _, _ = group_inference_requests(observed)
    final_positions = [group[-1] for group in groups]
    for entry in (observed.requests[pos] for pos in final_positions):
        row = observed.responses.get(entry["index"])
        turn: dict[str, Any] = {"request_index": entry["index"], "status": None, "text": "", "tool_calls": [],
                                "finish_reason": None, "complete": False}
        turns.append(turn)
        if row is None:
            continue
        data = row["record"].get("data") or {}
        turn["status"] = data.get("upstream_status")
        if data.get("body_truncated_in_evidence"):
            continue
        try:
            body = base64.b64decode(data.get("body_b64", "")).decode("utf-8", "replace")
        except ValueError:
            continue
        calls: dict[int, dict[str, Any]] = {}
        for line in body.split("\n"):
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload in ("", "[DONE]"):
                if payload == "[DONE]":
                    turn["complete"] = True
                continue
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            for choice in chunk.get("choices") or []:
                delta = choice.get("delta") or {}
                if isinstance(delta.get("content"), str):
                    turn["text"] += delta["content"]
                for call in delta.get("tool_calls") or []:
                    slot = calls.setdefault(call.get("index", 0), {"id": None, "name": "", "arguments": ""})
                    if call.get("id"):
                        slot["id"] = call["id"]
                    function = call.get("function") or {}
                    if function.get("name"):
                        slot["name"] += function["name"]
                    if function.get("arguments"):
                        slot["arguments"] += function["arguments"]
                if choice.get("finish_reason"):
                    turn["finish_reason"] = choice["finish_reason"]
        for index in sorted(calls):
            slot = calls[index]
            try:
                arguments = json.loads(slot["arguments"]) if slot["arguments"] else {}
            except json.JSONDecodeError:
                arguments = slot["arguments"]
            turn["tool_calls"].append({"id": slot["id"], "name": slot["name"], "arguments": arguments})
    return turns


REASONING_EFFORT = {"minimal": "minimal", "low": "low", "medium": "medium", "high": "high", "off": "minimal"}


REMINDER_PART = re.compile(
    r"^<system-reminder>\nToday: (\d{4}-\d{2}-\d{2}); current working directory: '/workspace'\. "
    r"Do not repeat this information in your reply\.\n</system-reminder>$")


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return ""


def transcript_errors(observed: "Observed", prompt: str | None) -> tuple[list[str], dict[str, Any]]:
    """The model must have received exactly the reviewed transcript grammar and nothing the runtime added.

    system message, then ONE user message whose parts are the runtime's dated `<system-reminder>` and the
    harness prompt, then for each earlier turn exactly the provider's assistant message and one tool message
    per tool call. Any other message (for example the runtime's hard-coded empty-stop `<system-injection>`,
    todo/TTSR/loop-guard reminders) is runtime-injected steering that the native trace does not show: the run
    is inadmissible, never silently absorbed.
    """
    errors: list[str] = []
    facts: dict[str, Any] = {"runtime_date": None}
    groups, _, _ = group_inference_requests(observed)
    turns = provider_turns(observed)
    for turn_index, group in enumerate(groups):
        body = observed.requests[group[-1]]["body"]
        messages = body.get("messages") or []
        roles = [m.get("role") for m in messages]
        if not roles or roles[0] != "system":
            errors.append(f"request {turn_index}: no system message")
            continue
        rest = messages[1:]
        if not rest or rest[0].get("role") != "user":
            errors.append(f"request {turn_index}: first message after the system prompt is not the user prompt")
            continue
        content = rest[0].get("content")
        parts = [p.get("text", "") for p in content if isinstance(p, dict)] if isinstance(content, list) else [content if isinstance(content, str) else ""]
        if len(parts) != 2 or not REMINDER_PART.match(parts[0]):
            errors.append(f"request {turn_index}: user message is not the reviewed [dated reminder, prompt] grammar")
        else:
            facts["runtime_date"] = REMINDER_PART.match(parts[0]).group(1)
            if prompt is not None and parts[1] != prompt:
                errors.append(f"request {turn_index}: the prompt the model received differs from the harness-authored prompt")
        expected_roles = ["user"]
        cursor = 1
        for previous in range(turn_index):
            turn = turns[previous]
            if cursor >= len(rest) or rest[cursor].get("role") != "assistant":
                errors.append(f"request {turn_index}: transcript lacks the assistant message of turn {previous}")
                break
            assistant = rest[cursor]
            calls = assistant.get("tool_calls") or []
            got = [(c.get("id"), (c.get("function") or {}).get("name")) for c in calls]
            want = [(c["id"], c["name"]) for c in turn["tool_calls"]]
            if got != want:
                errors.append(f"request {turn_index}: assistant message {previous} tool calls differ from the provider's response")
            if _norm_ws(_content_text(assistant.get("content"))) != _norm_ws(turn["text"]):
                errors.append(f"request {turn_index}: assistant message {previous} text differs from the provider's response")
            cursor += 1
            for call in turn["tool_calls"]:
                if cursor >= len(rest) or rest[cursor].get("role") != "tool" or rest[cursor].get("tool_call_id") != call["id"]:
                    errors.append(f"request {turn_index}: tool result for call {call['id']!r} is missing or out of order")
                    break
                cursor += 1
        extras = rest[cursor:] if cursor <= len(rest) else []
        if extras:
            errors.append(
                f"request {turn_index}: runtime-injected message(s) {[m.get('role') for m in extras]} follow the reviewed transcript: "
                + "; ".join(_content_text(m.get("content"))[:80].replace("\n", " ") for m in extras)
            )
    return errors, facts


def system_prompt_text(body: dict[str, Any]) -> str | None:
    messages = body.get("messages")
    if not isinstance(messages, list) or not messages or not isinstance(messages[0], dict):
        return None
    if messages[0].get("role") != "system":
        return None
    content = messages[0].get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") for part in content if isinstance(part, dict))
    return None


CATALOG_PREAMBLE = "Matching skill \u2192 MUST read `skill://<name>` first.\n<skills>\n"


def parse_catalog(prompt: str) -> tuple[list[dict[str, str]], list[str]]:
    """Runtime-visible skill catalog exactly as the model received it (reviewed `<skills>` template).

    An entry starts at a line `- <name>: ` and continues over following lines until the next entry
    or the closing tag. The result is compared with the mounted package's expected entries, so an
    entry injected through a description cannot pass unnoticed.
    """
    problems: list[str] = []
    start = prompt.find(CATALOG_PREAMBLE)
    if start < 0:
        return [], ["runtime system prompt has no reviewed skills catalog block"]
    body_start = start + len(CATALOG_PREAMBLE)
    end = prompt.find("\n</skills>", body_start)
    if end < 0:
        return [], ["runtime skills catalog block is not terminated"]
    entries: list[dict[str, str]] = []
    for line in prompt[body_start:end].split("\n"):
        match = re.match(r"^- ([A-Za-z0-9._-]+): (.*)$", line)
        if match:
            entries.append({"name": match.group(1), "description": match.group(2)})
        elif entries:
            entries[-1]["description"] += "\n" + line
        else:
            problems.append("runtime skills catalog has material before the first entry")
    if prompt.count("<skills>") != 1:
        problems.append("runtime system prompt contains more than one skills block")
    return entries, problems


def expected_catalog(skills_root: Path) -> list[dict[str, str]]:
    """Reference identity only: what the mounted package says its catalog entries are."""
    rows = []
    for skill in sorted(SSDP_SKILLS):
        path = skills_root / skill / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        front = re.match(r"---\n(.*?)\n---", text, re.S)
        description = ""
        if front:
            try:
                loaded = yaml.safe_load(front.group(1)) or {}
            except yaml.YAMLError:
                loaded = {}
            description = str(loaded.get("description", "")).strip()
        rows.append({"name": skill, "description": description})
    return rows


def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def check_runtime_surface(observed: Observed, context: dict[str, Any] | None) -> dict[str, Any]:
    """B1: derive the runtime surface from the trusted evidence and cross-check every binding."""
    errors = observed.errors
    profile = observed.profile
    summary: dict[str, Any] = {
        "model_id": None, "tools": None, "reasoning_fields": {}, "catalog": None,
        "mcp_server_connected": False, "runtime_version": None,
    }
    if not observed.requests:
        errors.append("no inference request was observed by the trusted provider-control principal")
        return summary

    first = observed.requests[0]["body"]
    tools0 = observed.tool_names(first)
    if tools0 is None:
        errors.append("observed inference request carries no valid tool list")
    else:
        summary["tools"] = tools0
        if len(set(tools0)) != len(tools0):
            errors.append("observed native tool list contains duplicates")
    for entry in observed.requests[1:]:
        if observed.tool_names(entry["body"]) != tools0:
            errors.append("the observed native tool surface changed between inference requests")
            break
    prompt0 = system_prompt_text(first)
    for entry in observed.requests[1:]:
        if system_prompt_text(entry["body"]) != prompt0:
            errors.append("the runtime system prompt changed between inference requests")
            break
    if prompt0 is None:
        errors.append("observed inference request has no system prompt")
        prompt0 = ""
    summary["model_id"] = first.get("model")
    for entry in observed.requests:
        body = entry["body"]
        if body.get("model") != first.get("model"):
            errors.append("observed inference requests name different models")
            break
    for key in ("reasoning_effort", "reasoning", "thinking", "thinking_budget", "enable_thinking", "reasoning_format"):
        if key in first:
            summary["reasoning_fields"][key] = first[key]
    route = (profile.get("containment_policy") or {}).get("provider_route") or {} if profile else {}
    if profile and route:
        thinking = (profile.get("reasoning_configuration") or {}).get("thinking")
        if route.get("reasoning"):
            expected_fields = {"reasoning_effort": REASONING_EFFORT.get(str(thinking))} if thinking in REASONING_EFFORT else None
        else:
            expected_fields = {}
        if expected_fields is None:
            errors.append(f"frozen thinking level {thinking!r} has no reviewed request-level reasoning binding")
        elif summary["reasoning_fields"] != expected_fields:
            errors.append(
                f"observed request reasoning configuration {summary['reasoning_fields']} differs from the frozen "
                f"configuration {expected_fields} (thinking={thinking!r}, reasoning model={route.get('reasoning')})"
            )
        for entry in observed.requests[1:]:
            fields = {k: entry["body"][k] for k in ("reasoning_effort", "reasoning", "thinking", "thinking_budget", "enable_thinking", "reasoning_format") if k in entry["body"]}
            if fields != summary["reasoning_fields"]:
                errors.append("observed reasoning configuration changed between inference requests")
                break
    for entry in observed.requests:
        auth = (entry["record"].get("data") or {}).get("inbound_authorization") or {}
        if not auth.get("matches_placeholder"):
            errors.append("an inference request did not carry the run's non-secret transport key")
            break

    # ---- system prompt structure: a replaced/extended/context-bearing prompt is contamination
    if not prompt0.startswith("<system-conventions>"):
        errors.append("runtime system prompt does not begin with the reviewed OMP base prompt (override present)")
    if "<project>" in prompt0 or "<file path=" in prompt0:
        errors.append("runtime system prompt contains project/context files; ambient context entered the runtime")
    instructions = (observed.mcp_initialize or {}).get("instructions")
    if isinstance(instructions, str):
        if not prompt0.rstrip("\n").endswith(instructions):
            errors.append("runtime system prompt does not end with the connected MCP server's instructions (append/extension present)")
    else:
        errors.append("no MCP initialize instructions were observed on the bridge")

    # ---- catalog: runtime-visible entries vs the mounted package (comparison reference only)
    entries, catalog_problems = parse_catalog(prompt0)
    errors.extend(catalog_problems)
    names = [row["name"] for row in entries]
    summary["catalog"] = names
    skills_root = Path(context["skills_root"]) if isinstance(context, dict) and context.get("skills_root") else None
    if skills_root is not None:
        expected = expected_catalog(skills_root)
        got = {row["name"]: _norm_ws(row["description"]) for row in entries}
        if sorted(got) != sorted(row["name"] for row in expected):
            errors.append(f"runtime catalog differs from the mounted protocol package: observed={sorted(got)}")
        for row in expected:
            if got.get(row["name"]) is not None and got[row["name"]] != _norm_ws(row["description"]):
                errors.append(f"runtime catalog entry {row['name']!r} differs from the mounted package description")
    if len(set(names)) != len(names):
        errors.append("runtime catalog lists the same skill more than once")

    for entry in observed.requests:
        agent = ((entry["record"].get("data") or {}).get("headers") or {}).get("user-agent")
        if agent != OMP_BUILD["http_user_agent"]:
            errors.append(f"inference request client identity {agent!r} is not the exact build's {OMP_BUILD['http_user_agent']!r}")
            break
    for exchange in observed.mcp:
        request = exchange.get("request")
        if isinstance(request, dict) and request.get("method") == "initialize":
            info = (request.get("params") or {}).get("clientInfo")
            if info != OMP_BUILD["mcp_client_info"]:
                errors.append(f"MCP client identity {info!r} is not the exact build's {OMP_BUILD['mcp_client_info']!r}")
            break

    # ---- build identity, launcher attestations
    facts = observed.launcher_facts
    omp_started = facts.get("omp_started") or {}
    if facts.get("omp_exe_sha256") != OMP_BUILD["sha256"]:
        errors.append("launcher-attested OMP executable digest differs from the frozen exact build")
    if omp_started.get("exe_is_frozen_file") is not True:
        errors.append("the running OMP process is not the frozen executable file")
    version = observed.runtime_version()
    summary["runtime_version"] = version
    if version is None:
        errors.append("the exact OMP executable did not report its build version in the sandbox")
    elif version != OMP_BUILD["version"]:
        errors.append(f"OMP executable self-reports version {version!r}, not the frozen {OMP_BUILD['version']!r}")
    if facts.get("cap_eff") not in ("0000000000000000", "0"):
        errors.append("subject sandbox retained capabilities")
    if facts.get("no_new_privs") != "1":
        errors.append("subject sandbox lacks no_new_privs")
    if facts.get("seccomp_mode") != "2":
        errors.append("subject sandbox has no seccomp filter")
    if str(facts.get("ptrace_scope")) not in ("1", "2", "3"):
        errors.append("host Yama ptrace scope does not restrict sibling ptrace")
    settings = observed.effective_settings()
    if settings is None:
        errors.append("the exact OMP build did not report its effective settings")
    else:
        flat = _flat_effective(settings)
        for key, wanted in frozen_settings_flat().items():
            if flat.get(key, "<absent>") != wanted:
                errors.append(f"effective OMP setting {key} is {flat.get(key, '<absent>')!r}, frozen {wanted!r}")
        # Every other setting must equal the exact-build inventory value: nothing the build exposes is
        # left unobserved, and a setting that differs (environment, a discovered config source) fails.
        inventory_rows = {row["key"]: row for row in load_inventory()["settings"]["entries"]}
        for key in flat:
            if key not in inventory_rows:
                errors.append(f"OMP reports setting {key!r} that is absent from the exact-build inventory")
        for key, row in inventory_rows.items():
            if key in frozen_settings_flat():
                continue
            if key in SETTINGS_PATH_DEPENDENT:
                continue
            if flat.get(key, "<absent>") != row.get("effective_under_frozen_profile", "<absent>") and not (
                    key not in flat and row.get("effective_under_frozen_profile") is None):
                errors.append(f"effective OMP setting {key} is {flat.get(key, '<absent>')!r}, inventory {row.get('effective_under_frozen_profile')!r}")

    # ---- MCP surface: raw mediator tool list <-> provider-native ids <-> observed request surface
    raw_tools = observed.mcp_tools_list
    if raw_tools is None:
        errors.append("the qualification MCP bridge never returned tools/list; the MCP server is not connected")
    else:
        raw_names = [t.get("name") for t in raw_tools if isinstance(t, dict)]
        if sorted(raw_names) != sorted(OMP_RAW_MCP_TOOLS):
            errors.append(f"raw mediator tool list {sorted(raw_names)} differs from the reviewed six-tool surface")
        else:
            minted = {name: mint_mcp_tool_name(OMP_MCP_SERVER_NAME, name) for name in raw_names}
            if len(set(minted.values())) != len(minted):
                errors.append("OMP name minting collides for the raw mediator tool list")
            observed_mcp = sorted(name for name in (tools0 or []) if name.startswith("mcp__"))
            if observed_mcp != sorted(minted.values()):
                errors.append(
                    "observed provider-native MCP tools differ from the raw mediator tools' minted ids: "
                    f"observed={observed_mcp}, minted={sorted(minted.values())}"
                )
            else:
                by_native = {v: k for k, v in minted.items()}
                for tool in first.get("tools") or []:
                    function = tool.get("function") or {}
                    native = function.get("name")
                    if native in by_native:
                        raw = next(t for t in raw_tools if t.get("name") == by_native[native])
                        if function.get("parameters") != raw.get("inputSchema") or function.get("description") != raw.get("description"):
                            errors.append(f"native MCP tool {native!r} schema/description differs from the raw mediator tool")
                summary["mcp_server_connected"] = observed.mcp_initialize is not None
    if observed.mcp_initialize is None:
        errors.append("the qualification MCP bridge never completed initialize; the MCP server is not connected")
    declared_builtin = [t for t in (profile.get("native_tools") or []) if not str(t).startswith("mcp__")]
    if tools0 is not None and profile:
        builtin_observed = [t for t in tools0 if not t.startswith("mcp__")]
        if sorted(builtin_observed) != sorted(declared_builtin):
            errors.append(
                f"observed native builtin tools {sorted(builtin_observed)} differ from the frozen surface {sorted(declared_builtin)}"
            )
    return summary


def _flat_effective(settings: dict[str, Any]) -> dict[str, Any]:
    """`omp config list --json` maps dotted key -> {value, type, description}; an unset key has no value."""
    flat: dict[str, Any] = {}
    for key, meta in settings.items():
        flat[key] = meta.get("value") if isinstance(meta, dict) else meta
    return flat


# --------------------------------------------------------------------------- normalization

def _event(run_id: str, sequence: int, kind: str, stream: str, native_index: int, native_sha256: str,
           payload: dict[str, Any], status: str = "observed", timing: Any = None) -> dict[str, Any]:
    return {
        "schema_version": core70.SCHEMA,
        "run_id": run_id,
        "event_id": f"e{sequence:06d}",
        "sequence": sequence,
        "actor_id": "executor",
        "kind": kind,
        "native_source": {"stream": stream, "native_index": native_index, "native_sha256": native_sha256},
        "status": status,
        "timing": timing,
        "payload": payload,
    }


def _package_identity(context: dict[str, Any] | None, observed_catalog_sha256: str | None = None) -> dict[str, Any] | None:
    if not isinstance(context, dict):
        return None
    package = context.get("package_identity")
    if not isinstance(package, dict):
        return None
    result = dict(package)
    result["identity_source"] = "verified-install-matched-to-runtime-catalog"
    if observed_catalog_sha256:
        result["runtime_observed_catalog_sha256"] = observed_catalog_sha256
    return result


def _result_text(raw_result: Any) -> str:
    if isinstance(raw_result, dict):
        content = raw_result.get("content")
        if isinstance(content, list):
            return "\n".join(item["text"] for item in content if isinstance(item, dict) and isinstance(item.get("text"), str))
    if isinstance(raw_result, str):
        return raw_result
    return json.dumps(raw_result, sort_keys=True, ensure_ascii=False)


def _message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
    return json.dumps(content, sort_keys=True)


def _consumed_tool_results(observed: Observed) -> dict[str, dict[str, Any]]:
    """tool_call_id -> the tool message the model actually received (first request that carries it)."""
    seen: dict[str, dict[str, Any]] = {}
    for entry in observed.requests:
        for message in entry["body"].get("messages") or []:
            if isinstance(message, dict) and message.get("role") == "tool":
                call_id = message.get("tool_call_id")
                if isinstance(call_id, str) and call_id not in seen:
                    seen[call_id] = {
                        "text": _message_text(message.get("content")),
                        "request_index": entry["index"],
                        "observer_position": entry["position"],
                    }
    return seen


def _map_sandbox_path(path: str, context: dict[str, Any] | None) -> Path | None:
    """Sandbox path -> host path (project, run-owned HOME, mounted package), else None."""
    if not isinstance(context, dict) or not isinstance(path, str):
        return None
    table = (
        (SB_PROJECT, context.get("project")),
        (SB_SKILLS, context.get("skills_root")),
        (SB_HOME, context.get("runtime_home")),
    )
    for prefix, host in table:
        if not host:
            continue
        if path == prefix or path.startswith(prefix + "/"):
            candidate = Path(host) / path[len(prefix):].lstrip("/")
            try:
                resolved = candidate.resolve()
                root = Path(host).resolve()
            except OSError:
                return None
            if resolved == root or root in resolved.parents:
                return resolved
            return None
    return None


SELECTOR_SUFFIX = re.compile(r":(?:raw|\d+(?:[-+]\d*)?(?:,\d+(?:[-+]\d*)?)*)$")
FOOTER = re.compile(r"\n*\[Showing lines (\d+)-(\d+) of (\d+)\. Use :\d+ to continue\]\s*$")


def _parse_hashline(text: str) -> tuple[dict[int, str], int | None] | None:
    """Undo OMP's hashline read format: `[path#ID]` header, `N:content` lines, `…` gap lines, optional footer.

    Returns ({line_number: content}, total_lines_reported) or None when the text is not that format.
    """
    footer = FOOTER.search(text)
    total = int(footer.group(3)) if footer else None
    body = text[: footer.start()] if footer else text
    lines = body.split("\n")
    if not lines or not re.fullmatch(r"\[[^\]]*#[0-9A-Za-z]+\]", lines[0]):
        return None
    rows: dict[int, str] = {}
    for line in lines[1:]:
        if line == "\u2026":
            continue
        match = re.match(r"^(\d+):(.*)$", line, re.S)
        if match is None:
            if line == "" and rows:
                continue
            return None
        rows[int(match.group(1))] = match.group(2)
    return rows, total


def consumption(text: str, host_file: Path) -> dict[str, Any]:
    """Compare what the model received with the exact mounted file.

    exact   the whole file (plain, or every numbered line 1..N of a hashline read)
    partial a strict subset of the file's lines, each identical to the source line it names
    none    text that does not correspond to the file (or contradicts it)
    """
    try:
        data = host_file.read_bytes()
        source = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return {"match": "unreadable", "resource_sha256": None, "resource_bytes": None}
    result = {"resource_sha256": sha256_bytes(data), "resource_bytes": len(data)}
    if text == source or text == source.rstrip("\n"):
        return {**result, "match": "exact", "form": "plain", "consumed_bytes": len(data), "lines_consumed": "all"}
    parsed = _parse_hashline(text)
    if parsed is not None:
        rows, _total = parsed
        source_lines = source.split("\n")
        if source.endswith("\n"):
            source_lines = source_lines[:-1]
        if rows and all(1 <= n <= len(source_lines) and source_lines[n - 1] == content for n, content in rows.items()):
            complete = sorted(rows) == list(range(1, len(source_lines) + 1))
            consumed = sum(len(source_lines[n - 1].encode("utf-8")) + 1 for n in rows)
            ranges: list[list[int]] = []
            for n in sorted(rows):
                if ranges and ranges[-1][1] == n - 1:
                    ranges[-1][1] = n
                else:
                    ranges.append([n, n])
            return {**result, "match": "exact" if complete else "partial", "form": "hashline",
                    "consumed_bytes": min(consumed, len(data)), "lines_consumed": "all" if complete else ranges}
        return {**result, "match": "none", "form": "hashline"}
    if text and text in source:
        return {**result, "match": "partial", "form": "plain-substring", "consumed_bytes": len(text.encode("utf-8")), "lines_consumed": "unknown"}
    return {**result, "match": "none"}


def normalize(stdout: str, run_id: str, context: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], int]:
    context = context or {}
    artifacts = context.get("adapter_artifacts") or {}
    observed = Observed(artifacts, context.get("profile"))
    surface = check_runtime_surface(observed, context)
    errors: list[str] = observed.errors
    consumed = _consumed_tool_results(observed)
    provider_call_ids = {call["id"] for turn in provider_turns(observed) for call in turn["tool_calls"] if call.get("id")}

    # Combined native evidence, in this fixed order: observer, bridge, native stdout, launcher.
    lines = stdout.splitlines()
    entries: list[tuple[str, int, str]] = []
    for stream in ("observer", "bridge"):
        for record in observed.records[stream]:
            entries.append((stream, len(entries), record.get("hash", "")))
    stdout_base = len(entries)
    for line in lines:
        entries.append(("stdout", len(entries), hashlib.sha256(line.encode("utf-8")).hexdigest()))
    launcher_base = len(entries)
    for record in observed.records["launcher"]:
        entries.append(("launcher", len(entries), record.get("hash", "")))
    observer_base, bridge_base = 0, len(observed.records["observer"])

    events: list[dict[str, Any]] = []
    completeness: dict[int, dict[str, Any]] = {}
    sequence = 0

    def emit(kind: str, stream: str, native_index: int, payload: dict[str, Any], status: str = "observed", timing: Any = None) -> dict[str, Any]:
        nonlocal sequence
        sequence += 1
        native_sha = entries[native_index][2] if 0 <= native_index < len(entries) else "0" * 64
        event = _event(run_id, sequence, kind, stream, native_index, native_sha, payload, status, timing)
        events.append(event)
        return event

    def classify(native_index: int, classification: str, oracle_relevant: bool, mapped: list[str] | None = None) -> None:
        completeness[native_index] = {
            "native_index": native_index,
            "native_sha256": entries[native_index][2] if native_index < len(entries) else "0" * 64,
            "classification": classification,
            "oracle_relevant": oracle_relevant,
            "mapped_event_ids": list(mapped or []),
        }

    # ---- catalog_snapshot from the first observed inference request (runtime, not installation)
    catalog_event = None
    if observed.requests:
        first = observed.requests[0]
        prompt0 = system_prompt_text(first["body"]) or ""
        entries_seen, _ = parse_catalog(prompt0)
        observed_catalog_sha = _digest_json(sorted((row["name"], _norm_ws(row["description"])) for row in entries_seen))
        catalog_ok = surface["catalog"] is not None
        catalog_event = emit("catalog_snapshot", "observer", observer_base + first["position"], {
            "logical_skill_ids": [row["name"] for row in entries_seen],
            "model": None,
            "runtime_version": surface.get("runtime_version"),
            "resolved_package_identity": _package_identity(context, observed_catalog_sha),
            "catalog_source": "observer-runtime-request-system-prompt",
            "catalog_observation": {
                "observer_record_hash": first["record"].get("hash"),
                "system_prompt_sha256": sha256_bytes(prompt0.encode("utf-8")),
                "runtime_observed_catalog_sha256": observed_catalog_sha,
                "native_tools": surface.get("tools"),
                "reasoning_fields": surface.get("reasoning_fields"),
                "request_model": surface.get("model_id"),
                "runtime_date": transcript_errors(observed, context.get("prompt"))[1].get("runtime_date"),
            },
            "catalog_parsed": catalog_ok,
        })

    # ---- observer classification (every record accounted for)
    request_positions = {entry["position"]: entry for entry in observed.requests}
    retry_request_indexes = {row["request_index"] for row in group_inference_requests(observed)[2]}
    for position, record in enumerate(observed.records["observer"]):
        index = observer_base + position
        kind = record.get("kind")
        if kind == "request" and position in request_positions:
            mapped = [catalog_event["event_id"]] if catalog_event and request_positions[position] is observed.requests[0] else []
            is_retry = request_positions[position]["index"] in retry_request_indexes
            classify(index, "observer-provider-layer-retry" if is_retry else "observer-inference-request", False, mapped)
        elif kind == "response":
            classify(index, "observer-inference-response", False)
        elif kind in ("start", "end"):
            classify(index, f"observer-{kind}", False)
        elif kind in REVIEWED_NON_ORACLE_OBSERVER_CONTROL_KINDS:
            classify(index, f"reviewed-non-oracle-observer-control:{kind}", False)
        else:
            classify(index, f"observer-{kind}", True)
    for position, record in enumerate(observed.records["bridge"]):
        index = bridge_base + position
        benign = record.get("kind") in ("start", "end", "mcp_request", "mcp_response") or (
            record.get("kind") == "refused"
            and (record.get("data") or {}).get("reason") == "server-initiated-stream-not-offered")
        classify(index, f"bridge-{record.get('kind')}", not benign)

    # ---- native stdout
    pending: dict[str, dict[str, Any]] = {}
    assistant_messages = 0
    message_ends: list[dict[str, Any]] = []
    agent_end_messages: list[dict[str, Any]] | None = None
    used_exchanges: set[int] = set()
    observed_model = None
    start_types: dict[int, str] = {}
    final_text = ""
    terminated = False
    turn_depth = 0
    root_selected: set[str] = set()

    def mcp_match(raw_tool: str, arguments: Any) -> dict[str, Any] | None:
        for exchange in observed.mcp:
            request = exchange.get("request")
            if id(exchange) in used_exchanges or not isinstance(request, dict) or request.get("method") != "tools/call":
                continue
            params = request.get("params") or {}
            if params.get("name") != raw_tool:
                continue
            args = {k: v for k, v in (arguments or {}).items()} if isinstance(arguments, dict) else arguments
            if params.get("arguments") == args:
                used_exchanges.add(id(exchange))
                return exchange
        return None

    for offset, line in enumerate(lines):
        native_index = stdout_base + offset
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"native event {offset} is not valid JSON")
            classify(native_index, "malformed-native-line", True)
            continue
        if not isinstance(raw, dict):
            errors.append(f"native event {offset} is not a JSON object")
            classify(native_index, "non-object-native-line", True)
            continue
        raw_type = raw.get("type")
        mapped: list[str] = []
        if raw_type in ("session", "agent_start", "turn_start", "message_update", "tool_execution_update"):
            if raw_type == "session" and raw.get("version") != 3:
                errors.append(f"native session format version {raw.get('version')!r} is not the reviewed version 3")
            if raw_type == "turn_start":
                turn_depth += 1
            classify(native_index, f"benign-native:{raw_type}", False)
        elif raw_type == "turn_end":
            turn_depth -= 1
            if turn_depth < 0:
                errors.append(f"native event {offset}: turn_end without turn_start")
            classify(native_index, "benign-native:turn_end", False)
        elif raw_type in ("message_start", "message_end"):
            message = raw.get("message")
            if isinstance(message, dict) and message.get("role") == "assistant":
                provider, model = message.get("provider"), message.get("model")
                if isinstance(provider, str) and isinstance(model, str):
                    observed_model = f"{provider}/{model}"
                if raw_type == "message_end":
                    assistant_messages += 1
            if raw_type == "message_end" and isinstance(message, dict):
                message_ends.append(message)
            classify(native_index, f"benign-native:{raw_type}", False)
        elif raw_type == "tool_execution_start":
            _on_tool_start(raw, offset, native_index, context, observed, emit, classify, pending, errors, start_types,
                           provider_call_ids)
        elif raw_type == "tool_execution_end":
            _on_tool_end(raw, offset, native_index, context, observed, consumed, emit, classify, pending, errors,
                         mcp_match, root_selected)
        elif raw_type == "agent_end":
            messages = raw.get("messages") if isinstance(raw.get("messages"), list) else []
            agent_end_messages = [m for m in messages if isinstance(m, dict)]
            terminated = True
            mapped = _on_agent_end(raw, native_index, observed, emit, errors, surface)
            final_text = next((e["payload"].get("result_text", "") for e in reversed(events) if e["kind"] == "final_result"), "")
            classify(native_index, "agent-end", True, mapped)
        elif raw_type in OMP_PROVIDER_MANAGED_EVENT_TYPES:
            errors.append(
                f"native event {offset} ({raw_type}) is a provider-managed behaviour the frozen profile disables; "
                "the run is inadmissible"
            )
            classify(native_index, f"provider-managed-event:{raw_type}", True)
        else:
            errors.append(f"native event {offset} has unknown native type {raw_type!r}; fail closed")
            classify(native_index, f"unknown-native-type:{raw_type}", True)

    # ---- structural completeness of the native trace (dropped / reordered / truncated detection)
    for call_id, start in pending.items():
        errors.append(f"native tool call {call_id!r} ({start['tool']}) has no matching result (pending at end of evidence)")
        classify(start["native_index"], "unmatched-tool-start-at-eof", True, start["mapped"])
    if turn_depth != 0:
        errors.append("native trace ends inside a turn (turn_start/turn_end unbalanced): truncated or dropped events")
    if agent_end_messages is None and lines:
        errors.append("native trace has no agent_end record: truncated or terminated evidence")
    elif agent_end_messages is not None:
        wanted = [_msg_key(m) for m in agent_end_messages]
        got = [_msg_key(m) for m in message_ends]
        if wanted != got:
            errors.append("native message events do not equal agent_end's complete transcript: dropped, reordered or duplicated events")
    turns = provider_turns(observed)
    native_assistant = [m for m in message_ends if m.get("role") == "assistant"]
    provider_ids = {call["id"] for turn in turns for call in turn["tool_calls"] if call.get("id")}
    for position, message in enumerate(native_assistant):
        if position >= len(turns):
            break
        turn = turns[position]
        if turn["status"] != 200 or not turn["complete"]:
            continue
        content = message.get("content") if isinstance(message.get("content"), list) else []
        native_text = "\n".join(part.get("text", "") for part in content if isinstance(part, dict) and part.get("type") == "text")
        native_calls = [
            {"id": part.get("id"), "name": part.get("name"), "arguments": part.get("arguments")}
            for part in content if isinstance(part, dict) and part.get("type") == "toolCall"
        ]
        provider_calls = [{"id": c["id"], "name": c["name"], "arguments": c["arguments"]} for c in turn["tool_calls"]]
        if native_calls != provider_calls:
            errors.append(f"assistant message {position}: native tool calls differ from the provider's response (forged, altered or dropped native event)")
        if _norm_ws(native_text) != _norm_ws(turn["text"]):
            errors.append(f"assistant message {position}: native text differs from the provider's response")
    groups, group_errors, retry_ledger = group_inference_requests(observed)
    errors.extend(group_errors)
    transcript_problems, transcript_facts = transcript_errors(observed, context.get("prompt"))
    errors.extend(transcript_problems)
    if len(groups) != assistant_messages:
        errors.append(
            f"observer recorded {len(groups)} distinct inference turn(s) ({len(observed.requests)} request(s)) but the native trace shows "
            f"{assistant_messages} assistant message(s): an inference call is unaccounted for (hidden/background call) or a native event is missing"
        )
    unused = [e for e in observed.mcp if isinstance(e.get("request"), dict) and e["request"].get("method") == "tools/call" and id(e) not in used_exchanges]
    if unused:
        errors.append(f"{len(unused)} mediator tools/call exchange(s) have no native tool event")
    # bridge tools/call exchanges are oracle relevant only when unmatched; matched ones map to tool events
    for exchange in observed.mcp:
        request = exchange.get("request")
        if isinstance(request, dict) and request.get("method") == "tools/call":
            pos = bridge_base + exchange["position"]
            if id(exchange) in used_exchanges:
                classify(pos, "bridge-mcp-tools-call-matched-to-native-tool-event", False)
            else:
                classify(pos, "bridge-mcp-tools-call-unmatched", True)

    if catalog_event is not None:
        catalog_event["payload"]["model"] = observed_model
        if observed_model is None:
            errors.append("native trace did not expose an observed model")
        elif surface.get("model_id") and not observed_model.endswith("/" + str(surface["model_id"])):
            errors.append(f"native model {observed_model!r} differs from the model in the observed inference request {surface['model_id']!r}")

    # ---- launcher evidence: relay denials are retained attempts; timeout terminates the run
    for denial in observed.denials:
        index = launcher_base + denial["position"]
        data = denial["record"].get("data") or {}
        event = emit("network_external_action", "launcher", index, {
            "destination_service": f"subject-relay:{data.get('relay')}",
            "operation": "connect",
            "authorization_decision": "deny",
            "disposition": "blocked",
            "input": {"reason": data.get("reason"), "holders": data.get("holders")},
            "tool_use_id": f"relay-denial-{denial['position']}",
            "result_status": "error",
            "result_reference": f"launcher:{denial['position']}",
            "result_sha256": sha256_bytes(stable_json(data).encode()),
            "result_content": data,
        }, status="error", timing=denial["record"].get("t_ns"))
        classify(index, "relay-denied-attempt", True, [event["event_id"]])
    exit_index = None
    for position, record in enumerate(observed.records["launcher"]):
        index = launcher_base + position
        if index in completeness:
            continue
        kind = record.get("kind")
        if kind == "omp_exit":
            exit_index = index
            mapped_exit: list[str] = []
            data = record.get("data") or {}
            if data.get("timed_out") and not terminated:
                ev = emit("termination", "launcher", index, {
                    "state": "timeout",
                    "native_return_state": {"is_error": True, "timed_out": True, "returncode": data.get("returncode"), "wall_s": data.get("wall_s")},
                    "terminal_result_exists": False,
                })
                mapped_exit.append(ev["event_id"])
            classify(index, "launcher-omp-exit", bool(mapped_exit), mapped_exit)
        elif kind in ("launcher_start", "omp_started", "probe", "start", "end"):
            classify(index, f"launcher-{kind}", False)
        else:
            classify(index, f"launcher-{kind}", True)
    if observed.omp_exit is None:
        errors.append("launcher evidence has no omp_exit record")
    if not terminated and not (observed.omp_exit or {}).get("timed_out"):
        if lines:
            errors.append("native trace has no terminal state and the run did not time out")

    # normalization completeness: every combined native index classified
    for native_index in range(len(entries)):
        if native_index not in completeness:
            classify(native_index, "unclassified-native-evidence", True)
            errors.append(f"native evidence {native_index} was not classified")
    map_rows = [completeness[i] for i in sorted(completeness)]
    return events, map_rows, list(dict.fromkeys(errors)), len(entries)


def _msg_key(message: dict[str, Any]) -> str:
    return stable_json({
        "role": message.get("role"),
        "toolCallId": message.get("toolCallId"),
        "content": message.get("content"),
        "stopReason": message.get("stopReason"),
    })


TOOL_KIND = {
    "read": "resource_access", "glob": "resource_access", "grep": "resource_access",
    "write": "mutation", "edit": "mutation", "bash": "tool_action",
}
TOOL_CLASSES = {
    "read": ["workspace_read_search_list"], "glob": ["workspace_read_search_list"], "grep": ["workspace_read_search_list"],
    "write": ["workspace_mutation"], "edit": ["workspace_mutation"],
    "bash": ["process_execution", "repository_object_store", "network_remote_service", "external_mutation",
             "credential_secret_service_account", "issue_evidence_store", "workspace_read_search_list", "workspace_mutation"],
}


def _resource_metadata(path_value: str | None, context: dict[str, Any] | None) -> dict[str, Any]:
    result = {"resolved_package_identity": None, "resource_sha256": None, "resource_bytes": None, "resolved_resource_path": None}
    if not isinstance(path_value, str) or not path_value or not isinstance(context, dict):
        return result
    if path_value.startswith("skill://"):
        return result
    candidate = path_value if path_value.startswith("/") else f"{SB_PROJECT}/{path_value}"
    host = _map_sandbox_path(candidate, context)
    if host is None or not host.is_file():
        return result
    result["resolved_resource_path"] = candidate
    result["resource_sha256"] = sha256_file(host)
    result["resource_bytes"] = host.stat().st_size
    skills = context.get("skills_root")
    if skills:
        try:
            host.relative_to(Path(skills).resolve())
            result["resolved_package_identity"] = _package_identity(context)
        except ValueError:
            pass
    return result


def _skill_from_path(path_value: str, resolved: str | None) -> tuple[str | None, str | None]:
    """Logical root and package-relative file for a `skill://` URL or a mounted package path."""
    if path_value.startswith("skill://"):
        rest = path_value[len("skill://"):]
        name, _, tail = rest.partition("/")
        return (name or None), (tail or "SKILL.md")
    target = resolved or path_value
    if target.startswith(SB_SKILLS + "/"):
        rel = target[len(SB_SKILLS) + 1:].split("/", 1)
        return rel[0], (rel[1] if len(rel) > 1 else None)
    return None, None


def _on_tool_start(raw, offset, native_index, context, observed, emit, classify, pending, errors, start_types, provider_call_ids):
    tool = str(raw.get("toolName") or "")
    args = raw.get("args")
    tool_use_id = str(raw.get("toolCallId") or f"n{offset}")
    data = args if isinstance(args, dict) else {"value": args}
    mapped: list[str] = []
    events_here: list[dict[str, Any]] = []
    if tool_use_id in pending:
        errors.append(f"native tool call id {tool_use_id!r} started twice without a result")
    if tool_use_id not in provider_call_ids:
        errors.append(f"native tool call {tool_use_id!r} does not appear in any provider response retained by the trusted observer")
    if tool.startswith("mcp__"):
        raw_names = {mint_mcp_tool_name(OMP_MCP_SERVER_NAME, name): name for name in OMP_RAW_MCP_TOOLS}
        raw_tool = raw_names.get(tool)
        if raw_tool is None:
            errors.append(f"native MCP call {tool!r} is not one of the exact minted mediator tool ids")
            events_here.append(emit("tool_action", "stdout", native_index, _plain_action(tool, data, tool_use_id, ["unclassified-native-tool"]), status="start"))
        elif raw_tool == "delegate":
            events_here.append(emit("delegate_call", "stdout", native_index, {
                "delegate_id": data.get("agent") or tool_use_id, "parent_actor": "executor", "request": data,
                "launched_work_relation": "scripted-qualification-standin", "tool_use_id": tool_use_id,
                "native_tool_name": tool, "mcp_tool_name": raw_tool, "server_name": OMP_MCP_SERVER_NAME,
            }, status="start"))
        else:
            access = {
                "operation": MCP_OPERATION[raw_tool], "resource_identity": MCP_STORE_IDENTITY, "input": data,
                "tool_use_id": tool_use_id, "result_status": "pending", "result_reference": None, "result_sha256": None,
                "native_tool_name": tool, "mcp_tool_name": raw_tool, "server_name": OMP_MCP_SERVER_NAME,
            }
            events_here.append(emit("issue_evidence_access", "stdout", native_index, access, status="start"))
            if raw_tool in MCP_MUTATING:
                events_here.append(emit("mutation", "stdout", native_index, {
                    "operation": MCP_OPERATION[raw_tool],
                    "logical_target": data.get("issue_id") or data.get("location"),
                    "workspace_external_class": "qualification-owned-standin",
                    "authorization_decision": "sandbox-mediate", "disposition": "attempted", "input": data,
                    "tool_use_id": tool_use_id, "result_status": "pending", "result_reference": None, "result_sha256": None,
                    "native_tool_name": tool, "mcp_tool_name": raw_tool, "server_name": OMP_MCP_SERVER_NAME,
                }, status="start"))
        classification = f"mcp-tool-start:{raw_tool or tool}"
    elif tool in OMP_BUILTIN_TOOLS:
        kind = TOOL_KIND[tool]
        if kind == "resource_access":
            path_value = data.get("path")
            identity = path_value or data.get("pattern") or SB_PROJECT
            if tool != "read":
                identity = data.get("path") or SB_PROJECT
            metadata = _resource_metadata(path_value if tool == "read" else None, context)
            events_here.append(emit("resource_access", "stdout", native_index, {
                "operation": tool, "resource_identity": str(identity), "input": data, "tool_use_id": tool_use_id,
                "result_status": "pending", "result_reference": None, "result_sha256": None,
                "resolved_package_identity": metadata["resolved_package_identity"],
                "resource_sha256": metadata["resource_sha256"], "resource_bytes": metadata["resource_bytes"],
                "resolved_resource_path": metadata["resolved_resource_path"],
            }, status="start"))
        elif kind == "mutation":
            target = data.get("path") or data.get("file") or data.get("file_path")
            events_here.append(emit("mutation", "stdout", native_index, {
                "operation": tool, "logical_target": target,
                "workspace_external_class": _workspace_class(target),
                "authorization_decision": "profile-governed", "disposition": "attempted", "input": data,
                "tool_use_id": tool_use_id, "result_status": "pending", "result_reference": None, "result_sha256": None,
            }, status="start"))
        else:
            events_here.append(emit("tool_action", "stdout", native_index, _plain_action(tool, data, tool_use_id, TOOL_CLASSES[tool]), status="start"))
        classification = f"tool-start:{tool}"
    else:
        # A call to a name outside the exposed surface: retained as a blocked attempt, never as work.
        hint = ATTEMPT_CLASS_HINT.get(tool)
        payload = _plain_action(tool, data, tool_use_id, ["unexposed-native-tool-attempt"])
        payload["attempted_semantic_class"] = hint
        payload["exposed_in_runtime_surface"] = tool in (observed_surface_tools(observed) or [])
        if tool in (observed_surface_tools(observed) or []):
            errors.append(f"native tool {tool!r} was called and is exposed but is outside the frozen classified surface")
        events_here.append(emit("tool_action", "stdout", native_index, payload, status="start"))
        classification = f"unexposed-tool-attempt:{tool}"
    mapped = [e["event_id"] for e in events_here]
    pending[tool_use_id] = {"tool": tool, "args": args, "native_index": native_index, "mapped": mapped}
    classify(native_index, classification, True, mapped)


def observed_surface_tools(observed: Observed) -> list[str] | None:
    return observed.tool_names(observed.requests[0]["body"]) if observed.requests else None


def _plain_action(tool: str, data: dict[str, Any], tool_use_id: str, classes: list[str]) -> dict[str, Any]:
    return {
        "semantic_capability_classes": classes, "native_operation": tool, "input": data, "tool_use_id": tool_use_id,
        "result_status": "pending", "result_reference": None, "result_sha256": None,
    }


def _workspace_class(target: Any) -> str:
    if not isinstance(target, str) or not target:
        return "unresolved"
    path = target if target.startswith("/") else f"{SB_PROJECT}/{target}"
    normal = os.path.normpath(path)
    return "workspace" if normal == SB_PROJECT or normal.startswith(SB_PROJECT + "/") else "external"


def _on_tool_end(raw, offset, native_index, context, observed, consumed, emit, classify, pending, errors, mcp_match, root_selected):
    tool = str(raw.get("toolName") or "")
    tool_use_id = str(raw.get("toolCallId") or f"n{offset}")
    start = pending.pop(tool_use_id, None)
    result = raw.get("result")
    is_error = bool(raw.get("isError"))
    status = "error" if is_error else "result"
    text = _result_text(result)
    reference = f"native:{native_index}"
    result_sha = sha256_bytes(text.encode("utf-8"))
    if start is None:
        errors.append(f"native event {offset} tool result has no observed start for {tool_use_id!r}")
        classify(native_index, f"unmatched-tool-end:{tool}", True)
        return
    if start["tool"] != tool:
        errors.append(f"native tool result {tool_use_id!r} names {tool!r} but started as {start['tool']!r}")
    args = start["args"]
    data = args if isinstance(args, dict) else {"value": args}
    mapped: list[str] = []
    fields = {"result_status": status, "result_reference": reference, "result_sha256": result_sha, "result_content": text}
    model_saw = consumed.get(tool_use_id)
    fields["result_seen_by_model"] = None if model_saw is None else (model_saw["text"] == text)
    if model_saw is not None and model_saw["text"] != text:
        errors.append(f"tool result {tool_use_id!r} seen by the model differs from the native trace result")
    if model_saw is None and not is_error:
        fields["result_seen_by_model"] = False

    if tool.startswith("mcp__"):
        mapped = _mcp_end(tool, tool_use_id, data, result, is_error, fields, text, native_index, observed, emit, errors, mcp_match)
    elif tool in OMP_BUILTIN_TOOLS:
        kind = TOOL_KIND[tool]
        if kind == "resource_access":
            path_value = data.get("path") if tool == "read" else None
            identity = (data.get("path") or data.get("pattern") or SB_PROJECT) if tool == "read" else (data.get("path") or SB_PROJECT)
            details = (result.get("details") if isinstance(result, dict) else None) or {}
            resolved = details.get("resolvedPath") if isinstance(details, dict) else None
            metadata = _resource_metadata(resolved or path_value if tool == "read" else None, context)
            payload = {
                "operation": tool, "resource_identity": str(identity), "input": data, "tool_use_id": tool_use_id,
                "resolved_package_identity": metadata["resolved_package_identity"],
                "resource_sha256": metadata["resource_sha256"], "resource_bytes": metadata["resource_bytes"],
                "resolved_resource_path": metadata["resolved_resource_path"] or resolved, **fields,
            }
            root, package_rel = (None, None)
            if tool == "read" and isinstance(path_value, str):
                meta_source = ((details.get("meta") or {}).get("source") or {}) if isinstance(details, dict) else {}
                clean_path = meta_source.get("value") if isinstance(meta_source.get("value"), str) else SELECTOR_SUFFIX.sub("", path_value)
                root, package_rel = _skill_from_path(clean_path, resolved)
            if root in SSDP_SKILLS and not is_error:
                host = _map_sandbox_path(resolved, context) if resolved else None
                if host is None and package_rel and context.get("skills_root"):
                    host = Path(context["skills_root"]) / root / package_rel
                cons = consumption(model_saw["text"], host) if (model_saw is not None and host is not None and host.is_file()) else {"match": "unobserved"}
                payload["consumed_resource"] = {
                    "logical_root": root, "package_relative_path": package_rel, "sandbox_path": resolved,
                    "observer_request_index": model_saw["request_index"] if model_saw else None,
                    "observer_record_position": model_saw["observer_position"] if model_saw else None, **cons,
                }
                payload["resolved_package_identity"] = _package_identity(context)
                payload["resource_sha256"] = cons.get("resource_sha256") or payload["resource_sha256"]
                payload["resource_bytes"] = cons.get("resource_bytes") if cons.get("resource_bytes") is not None else payload["resource_bytes"]
            ev = emit("resource_access", "stdout", native_index, payload, status=status)
            mapped.append(ev["event_id"])
            if root in SSDP_SKILLS and not is_error and package_rel in ("SKILL.md", None) and payload.get("consumed_resource", {}).get("match") in ("exact", "partial"):
                pinned = None
                entry = (context or {}).get("entry")
                if isinstance(entry, str) and entry.startswith("pinned:"):
                    pinned = entry.split(":", 1)[1]
                mechanism = "explicit-instruction-skill-read" if pinned == root else "ordinary-skill-read"
                sel = emit("root_selection", "stdout", native_index, {
                    "logical_root": root, "selection_mechanism": mechanism, "native_operation": "read",
                    "input": data, "resolved_package_identity": _package_identity(context),
                    "tool_use_id": tool_use_id, "consumed_resource": payload["consumed_resource"],
                    "evidence": "successful native skill read whose returned material the trusted observer saw delivered to the model",
                }, status="observed")
                mapped.append(sel["event_id"])
        elif kind == "mutation":
            details = (result.get("details") if isinstance(result, dict) else None) or {}
            resolved = details.get("resolvedPath") if isinstance(details, dict) else None
            target = resolved or data.get("path") or data.get("file") or data.get("file_path")
            external = _workspace_class(target)
            denied = is_error and bool(re.search(r"(read-only file system|permission denied|operation not permitted|EROFS|EACCES|EPERM)", text, re.I))
            ev = emit("mutation", "stdout", native_index, {
                "operation": tool, "logical_target": target, "workspace_external_class": external,
                "authorization_decision": "deny" if denied else "allow",
                "disposition": "blocked-or-error" if is_error else ("sandboxed" if external == "external" else "applied-to-workspace"),
                "input": data, "tool_use_id": tool_use_id, "requested_target": data.get("path") or data.get("file") or data.get("file_path"),
                **fields,
            }, status=status)
            mapped.append(ev["event_id"])
        else:
            ev = emit("tool_action", "stdout", native_index, {**_plain_action(tool, data, tool_use_id, TOOL_CLASSES[tool]), **fields}, status=status)
            mapped.append(ev["event_id"])
    else:
        payload = {**_plain_action(tool, data, tool_use_id, ["unexposed-native-tool-attempt"]), **fields,
                   "attempted_semantic_class": ATTEMPT_CLASS_HINT.get(tool), "blocked": True,
                   "exposed_in_runtime_surface": tool in (observed_surface_tools(observed) or []),
                   "blocked_reason": "tool is not in the runtime-exposed surface"}
        if not is_error:
            errors.append(f"unexposed native tool {tool!r} reported success")
        ev = emit("tool_action", "stdout", native_index, payload, status=status)
        mapped.append(ev["event_id"])
    classify(native_index, f"tool-end:{tool}", True, mapped)


def _mcp_end(tool, tool_use_id, data, result, is_error, fields, text, native_index, observed, emit, errors, mcp_match) -> list[str]:
    details = (result.get("details") if isinstance(result, dict) else None) or {}
    server_name = details.get("serverName") if isinstance(details, dict) else None
    raw_tool = details.get("mcpToolName") if isinstance(details, dict) else None
    mapped: list[str] = []
    problems: list[str] = []
    if server_name != OMP_MCP_SERVER_NAME:
        problems.append(f"MCP result serverName {server_name!r} is not the declared server {OMP_MCP_SERVER_NAME!r}")
    if raw_tool not in OMP_RAW_MCP_TOOLS:
        problems.append(f"MCP result mcpToolName {raw_tool!r} is not a raw mediator tool")
    else:
        if mint_mcp_tool_name(str(server_name), raw_tool) != tool:
            problems.append(f"native tool id {tool!r} does not equal the name minted from serverName/mcpToolName")
    if isinstance(details, dict) and details.get("isError") is not None and bool(details.get("isError")) != is_error:
        problems.append("MCP result isError disagrees between native trace details and the event flag")
    raw_content = details.get("rawContent") if isinstance(details, dict) else None
    raw_text = None
    if isinstance(raw_content, list):
        texts = [item.get("text") for item in raw_content if isinstance(item, dict) and isinstance(item.get("text"), str)]
        raw_text = "\n".join(texts) if texts else None
    mediated = None
    if raw_text is not None:
        try:
            mediated = json.loads(raw_text)
        except json.JSONDecodeError:
            problems.append("MCP rawContent is not the mediator's structured result")
    else:
        problems.append("MCP result carries no rawContent; the mediator result cannot be bound")
    exchange = mcp_match(raw_tool, data) if raw_tool in OMP_RAW_MCP_TOOLS else None
    trusted = None
    if exchange is None:
        problems.append(f"no mediator tools/call exchange on the trusted bridge matches native call {tool_use_id!r}")
    else:
        body = (exchange.get("response") or {}).get("result") or {}
        contents = body.get("content") if isinstance(body, dict) else None
        trusted = contents[0].get("text") if isinstance(contents, list) and contents and isinstance(contents[0], dict) else None
        if trusted is None or (raw_text is not None and trusted != raw_text):
            problems.append("native MCP result differs from the mediator's raw result retained by the trusted bridge")
        if bool(body.get("isError")) != is_error:
            problems.append("native error status differs from the mediator's isError on the trusted bridge")
    evidence: dict[str, Any] = {}
    if isinstance(mediated, dict):
        evidence = mediated.get("evidence") if isinstance(mediated.get("evidence"), dict) else {}
        if not evidence:
            problems.append("mediator result has no structured evidence")
        if evidence.get("store_identity") != MCP_STORE_IDENTITY:
            problems.append(f"mediator store identity {evidence.get('store_identity')!r} is not {MCP_STORE_IDENTITY!r}")
        if raw_tool in MCP_OPERATION and evidence.get("operation") != MCP_OPERATION[raw_tool]:
            problems.append(f"mediator operation {evidence.get('operation')!r} does not match tool {raw_tool!r}")
        if not isinstance(evidence.get("object_ids"), list):
            problems.append("mediator evidence lacks object_ids")
        returncode = mediated.get("returncode")
        if (returncode != 0) != is_error:
            problems.append("mediator returncode disagrees with the native error status")
        if raw_tool in ("issue_show", "issue_create", "issue_comment") and not is_error:
            after = evidence.get("after_object_version")
            if not (isinstance(after, str) and len(after) == 64):
                problems.append(f"{raw_tool} success lacks a valid after_object_version")
            if raw_tool in ("issue_show", "issue_comment"):
                before = evidence.get("before_object_version")
                if not (isinstance(before, str) and len(before) == 64):
                    problems.append(f"{raw_tool} success lacks a valid before_object_version")
            if raw_tool == "issue_create" and evidence.get("before_object_version") is not None:
                problems.append("issue_create reports a before_object_version for a new object")
        if raw_tool == "issue_search" and "query" not in evidence:
            problems.append("issue_search evidence lacks the query identity")
    errors.extend(f"native event {native_index}: {problem}" for problem in problems)
    lossless = {
        "native_tool_name": tool, "server_name": server_name, "mcp_tool_name": raw_tool,
        "raw_result_sha256": sha256_bytes((raw_text or "").encode("utf-8")),
        "trusted_bridge_result_sha256": sha256_bytes((trusted or "").encode("utf-8")) if trusted is not None else None,
        "mediator_returncode": (mediated or {}).get("returncode") if isinstance(mediated, dict) else None,
        "mediator_stderr": (mediated or {}).get("stderr") if isinstance(mediated, dict) else None,
        "mediator_evidence": evidence,
        "identity_cross_check": {"ok": not problems, "problems": problems},
    }
    if raw_tool == "delegate":
        ev = emit("delegate_return", "stdout", native_index, {
            "delegate_id": (evidence.get("object_ids") or [data.get("agent")])[0] if evidence.get("object_ids") else data.get("agent"),
            "parent_actor": "executor", "tool_use_id": tool_use_id,
            "result_reference": fields["result_reference"], "result_sha256": fields["result_sha256"],
            "result_content": fields["result_content"], "launched_work_relation": "scripted-qualification-standin",
            "delegate_found": bool(mediated and mediated.get("returncode") == 0), "store_identity": evidence.get("store_identity"),
            "mediator_operation": evidence.get("operation"), **lossless,
        }, status=fields["result_status"])
        mapped.append(ev["event_id"])
        return mapped
    access = {
        "operation": MCP_OPERATION.get(raw_tool, str(raw_tool)), "resource_identity": MCP_STORE_IDENTITY, "input": data,
        "tool_use_id": tool_use_id, **fields, **lossless,
    }
    for key in ("store_identity", "operation", "query", "object_ids", "before_object_version", "after_object_version"):
        if key in evidence:
            access[key] = evidence[key]
    if isinstance(mediated, dict) and mediated.get("returncode") not in (None, 0):
        access["result_status"] = "error"
    ev = emit("issue_evidence_access", "stdout", native_index, access, status=access["result_status"])
    mapped.append(ev["event_id"])
    if raw_tool in MCP_MUTATING:
        mutation = {
            "operation": MCP_OPERATION[raw_tool], "logical_target": data.get("issue_id") or data.get("location"),
            "workspace_external_class": "qualification-owned-standin", "authorization_decision": "sandbox-mediate",
            "disposition": "blocked-or-error" if access["result_status"] == "error" else "sandboxed",
            "input": data, "tool_use_id": tool_use_id, **fields, **lossless,
        }
        mutation["result_status"] = access["result_status"]
        for key in ("store_identity", "object_ids", "before_object_version", "after_object_version"):
            if key in evidence:
                mutation[key] = evidence[key]
        mev = emit("mutation", "stdout", native_index, mutation, status=mutation["result_status"])
        mapped.append(mev["event_id"])
    return mapped


def _on_agent_end(raw, native_index, observed, emit, errors, surface) -> list[str]:
    messages = [m for m in (raw.get("messages") or []) if isinstance(m, dict)]
    final_text = ""
    last_stop = None
    usage = None
    duration = None
    error_message = None
    for message in messages:
        if message.get("role") == "assistant":
            last_stop = message.get("stopReason")
            usage = message.get("usage")
            duration = message.get("duration")
            error_message = message.get("errorMessage")
            content = message.get("content")
            if isinstance(content, list):
                texts = [item.get("text") for item in content if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)]
                final_text = "\n".join(texts) if texts else final_text if last_stop == "stop" else ""
    budget = bool(observed.budget_exhausted)
    if last_stop == "stop":
        state, is_error = "completed", False
    elif last_stop == "length":
        state, is_error = "token_cap", True
    elif last_stop == "error" and budget:
        state, is_error = "turn_cap", True
    elif last_stop == "aborted":
        state, is_error = "aborted", True
    else:
        state, is_error = "error", True
    mapped: list[str] = []
    termination = emit("termination", "stdout", native_index, {
        "state": state,
        "native_return_state": {"stopReason": last_stop, "messageCount": len(messages), "isError": is_error,
                                "errorMessage": error_message, "turn_budget_exhausted_on_observer": budget},
        "terminal_result_exists": bool(final_text) and not is_error,
    })
    mapped.append(termination["event_id"])
    if final_text and not is_error:
        result = emit("final_result", "stdout", native_index, {"result_text": final_text, "artifact_reference": "final-report.md"})
        mapped.append(result["event_id"])
    usage_event = emit("usage_timing", "stdout", native_index, {
        "duration_ms": duration, "duration_unit": "ms", "usage": usage,
        "usage_source": "provider-assistant-message", "native_duration_field": "assistant.duration",
        "observer_request_count": len(observed.requests),
        "provider_layer_retries": group_inference_requests(observed)[2],
    })
    mapped.append(usage_event["event_id"])
    return mapped


# ---------------------------------------------------------- runtime observation and hooks

def runtime_observation(stdout: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Runtime surface assembled from the trusted principals' evidence; never from installation state."""
    context = context or {}
    artifacts = context.get("adapter_artifacts") or {}
    observed = Observed(artifacts, context.get("profile"))
    surface = check_runtime_surface(observed, context)
    observed.errors.extend(transcript_errors(observed, context.get("prompt"))[0])
    native_model = None
    for line in stdout.splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = raw.get("message") if isinstance(raw, dict) else None
        if isinstance(message, dict) and message.get("role") == "assistant" and isinstance(message.get("provider"), str) and isinstance(message.get("model"), str):
            native_model = f"{message['provider']}/{message['model']}"
    session_seen = False
    for line in stdout.splitlines()[:1]:
        try:
            first = json.loads(line)
            session_seen = isinstance(first, dict) and first.get("type") == "session" and first.get("version") == 3
        except json.JSONDecodeError:
            pass
    mcp_servers = [{"name": OMP_MCP_SERVER_NAME, "status": "connected"}] if surface.get("mcp_server_connected") else []
    return {
        "model": native_model,
        "runtime_version": surface.get("runtime_version"),
        "tools": surface.get("tools"),
        "native_capabilities": ["omp-json-event-stream-v1"] if session_seen else [],
        "messaging_socket_path": None,
        "memory_paths": {},
        "mcp_servers": mcp_servers,
        "observation_errors": list(dict.fromkeys(observed.errors)),
        "observation_source": "trusted provider-control/observer, MCP bridge and launcher hash-linked evidence plus the native JSON trace",
        "reasoning_fields": surface.get("reasoning_fields"),
        "request_model": surface.get("model_id"),
    }


def final_result(events: list[dict[str, Any]]) -> str:
    for event in reversed(events):
        if event.get("kind") == "final_result":
            return str((event.get("payload") or {}).get("result_text") or "")
    return ""


def catalog_isolation(events: list[dict[str, Any]]) -> dict[str, Any]:
    snapshots = [e for e in events if e.get("kind") == "catalog_snapshot"]
    if len(snapshots) != 1:
        return {"ok": False, "reason": f"expected one runtime catalog snapshot, found {len(snapshots)}"}
    payload = snapshots[0].get("payload") or {}
    skills = payload.get("logical_skill_ids") or []
    counts = {name: skills.count(name) for name in SSDP_SKILLS}
    foreign = sorted(name for name in skills if name not in SSDP_SKILLS)
    package = payload.get("resolved_package_identity")
    package_ok = isinstance(package, dict) and isinstance(package.get("package_sha256"), str) and len(package["package_sha256"]) == 64
    runtime_derived = payload.get("catalog_source") == "observer-runtime-request-system-prompt" and bool(payload.get("catalog_parsed"))
    return {
        "ok": all(v == 1 for v in counts.values()) and package_ok and not foreign and runtime_derived,
        "ssdp_counts": counts, "foreign_skills": foreign, "catalog": skills,
        "resolved_package_identity": package, "runtime_derived": runtime_derived,
    }


def owner_reads(events: list[dict[str, Any]], owner_name: str) -> list[int]:
    hits: list[int] = []
    for event in events:
        if event.get("kind") != "resource_access" or event.get("status") != "result":
            continue
        payload = event.get("payload") or {}
        if payload.get("result_status") != "result":
            continue
        consumed = payload.get("consumed_resource") or {}
        target = f"{payload.get('resource_identity') or ''} {consumed.get('package_relative_path') or ''} {payload.get('resolved_resource_path') or ''}"
        if owner_name in target and consumed.get("match") in ("exact", "partial"):
            hits.append(int(event["sequence"]))
    return hits


def prepare_prompt(profile: dict[str, Any], entry: str, prompt: str) -> str:
    if not entry.startswith("pinned:"):
        return prompt.strip()
    root = entry.split(":", 1)[1]
    template = profile.get("pinned_root_instruction_template", "Use the {root} skill. {prompt}")
    return str(template).format(root=root, prompt=prompt.strip())
