#!/usr/bin/env python3
"""Claude stream-json runtime adapter for the portable Protocol 7 Stage F core.

The adapter translates exposed native events only. It does not infer private reasoning and
it does not claim that command text proves filesystem/network containment. Qualification
admission remains external and profile-bound.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ADAPTER_ID = "claude-stream-json-v3"
SSDP_SKILLS = {
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-documentation",
    "software-maintenance-audit",
    "repository-hygiene",
}
READ_TOOLS = {"Read", "Grep", "Glob"}
MUTATION_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
NETWORK_TOOLS = {"WebFetch", "WebSearch"}
DELEGATE_TOOLS = {"Agent"}
MCP_SERVER_NAME = "ssdp70"
MCP_SERVER_ID = "ssdp70-qualification-stdio-v1"
MCP_TOOL_PREFIX = f"mcp__{MCP_SERVER_NAME}__"
MCP_ISSUE_READ_TOOLS = {
    f"{MCP_TOOL_PREFIX}issue_locations": "locations",
    f"{MCP_TOOL_PREFIX}issue_search": "search",
    f"{MCP_TOOL_PREFIX}issue_show": "show",
}
MCP_ISSUE_MUTATION_TOOLS = {
    f"{MCP_TOOL_PREFIX}issue_create": "create",
    f"{MCP_TOOL_PREFIX}issue_comment": "comment",
}
MCP_DELEGATE_TOOL = f"{MCP_TOOL_PREFIX}delegate"
SAFE_ENV_KEYS = {
    "PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM",
    "SSL_CERT_FILE", "SSL_CERT_DIR", "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB", "DISABLE_AUTOUPDATER",
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY", "CLAUDE_CODE_DISABLE_CRON",
    "CLAUDE_CODE_DISABLE_ARTIFACT", "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS",
}
QUALIFICATION_AUTH_ENV = {
    "SSDP70_CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CODE_OAUTH_TOKEN",
    "SSDP70_ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY",
    "SSDP70_ANTHROPIC_AUTH_TOKEN": "ANTHROPIC_AUTH_TOKEN",
}
PARENT_AUTH_ENV = set(QUALIFICATION_AUTH_ENV.values())
SETTING_SOURCES = {"none", "project"}
PROJECT_SETTINGS_BYTES = b"{}\n"
PROJECT_CLAUDE_ALLOWED_ENTRIES = {"skills", "settings.json"}
PROJECT_CLAUDE_RUNTIME_EMPTY_DIRS = {"agents", "commands"}  # created empty by the runtime itself


def clean_env() -> dict[str, str]:
    """Return an explicit allow-list with no ambient HOME/tokens."""
    env = {key: os.environ[key] for key in SAFE_ENV_KEYS if key in os.environ}
    supplied = [
        (source, target, os.environ[source])
        for source, target in QUALIFICATION_AUTH_ENV.items()
        if os.environ.get(source)
    ]
    if len(supplied) > 1:
        raise RuntimeError("multiple qualification authentication sources are configured")
    if supplied:
        _, target, value = supplied[0]
        env[target] = value
        env["SSDP70_AUTH_MODE"] = target
    env["CLAUDE_CODE_SUBPROCESS_ENV_SCRUB"] = "1"
    env["DISABLE_AUTOUPDATER"] = "1"
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    env["CLAUDE_CODE_DISABLE_CRON"] = "1"
    env["CLAUDE_CODE_DISABLE_ARTIFACT"] = "1"
    env["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"] = "1"
    return env


def _private_mcp_paths(private_root: Path) -> dict[str, Path]:
    return {
        "server": private_root / "mcp-server.py",
        "stub": private_root / "stub",
        "log": private_root / "side-effects.jsonl",
        "account": private_root / "mcp-account.txt",
    }


def _declared_mcp_servers(profile: dict[str, Any]) -> list[dict[str, Any]]:
    servers = profile.get("mcp_servers") or []
    if not isinstance(servers, list):
        raise RuntimeError("execution profile mcp_servers is malformed")
    return servers


def _mcp_config_document(profile: dict[str, Any], private_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    servers = _declared_mcp_servers(profile)
    if not servers:
        return {"mcpServers": {}}, []
    if len(servers) != 1:
        raise RuntimeError("Claude Stage F profile requires exactly one qualification MCP server")
    declared = servers[0]
    if declared.get("name") != MCP_SERVER_NAME or declared.get("transport") != "stdio" or declared.get("server_id") != MCP_SERVER_ID:
        raise RuntimeError("qualification MCP server identity differs from the frozen profile")
    expected_tools = {
        f"{MCP_TOOL_PREFIX}issue_locations",
        f"{MCP_TOOL_PREFIX}issue_search",
        f"{MCP_TOOL_PREFIX}issue_show",
        f"{MCP_TOOL_PREFIX}issue_create",
        f"{MCP_TOOL_PREFIX}issue_comment",
        MCP_DELEGATE_TOOL,
    }
    if set(declared.get("tools") or []) != expected_tools:
        raise RuntimeError("qualification MCP tool surface differs from the adapter's reviewed semantic surface")

    paths = _private_mcp_paths(private_root)
    source_server = Path(__file__).resolve().parent.parent / "stub_tools" / "mediator.py"
    for label in ("server", "stub", "log", "account"):
        path = paths[label]
        if label == "stub":
            if not path.is_dir():
                raise RuntimeError("qualification MCP private stub root is absent")
        elif not path.is_file():
            raise RuntimeError(f"qualification MCP private {label} is absent")
    source_sha = hashlib.sha256(source_server.read_bytes()).hexdigest()
    server_sha = hashlib.sha256(paths["server"].read_bytes()).hexdigest()
    if source_sha != server_sha:
        raise RuntimeError("qualification MCP server executable differs from the reviewed adapter source")
    python_dir = str(Path(sys.executable).resolve().parent)
    minimal_path = ":".join(dict.fromkeys([python_dir, "/usr/bin", "/bin"]))
    server_args = [
        "-i",
        f"PATH={minimal_path}",
        "PYTHONDONTWRITEBYTECODE=1",
        str(Path(sys.executable).resolve()),
        str(paths["server"]),
        "--stub-root", str(paths["stub"]),
        "--side-effect-log", str(paths["log"]),
        "--account-file", str(paths["account"]),
        "--server-id", MCP_SERVER_ID,
        "--expected-self-sha256", server_sha,
    ]
    config = {
        "mcpServers": {
            MCP_SERVER_NAME: {
                "type": "stdio",
                "command": "/usr/bin/env",
                "args": server_args,
            }
        }
    }
    realized = [{
        "name": MCP_SERVER_NAME,
        "transport": "stdio",
        "server_id": MCP_SERVER_ID,
        "entrypoint": declared.get("entrypoint"),
        "executable_file": str(paths["server"]),
        "executable_sha256": server_sha,
        "credential_environment": "env-i-empty-plus-minimal-path",
        "tools": list(declared["tools"]),
    }]
    return config, realized


def _control_paths(project: Path, env: dict[str, str]) -> tuple[Path, Path, Path]:
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise RuntimeError("contained Claude launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    project_resolved = project.resolve()
    try:
        home.relative_to(project_resolved)
    except ValueError:
        pass
    else:
        raise RuntimeError("run-owned HOME must remain outside the executor/evaluator working directory")
    private_root = home.parent.resolve()
    if private_root == project_resolved or private_root in project_resolved.parents:
        raise RuntimeError("harness-private root may not contain the executor/evaluator working directory")
    control = home / ".ssdp70-control"
    return private_root, control / "settings.json", control / "mcp.json"


def _setting_sources(profile: dict[str, Any]) -> str:
    """Return the frozen Claude settings-source realization: `none` or `project`.

    `none` launches with --restricted (no settings files, and therefore no project skills).
    `project` loads only the project source, whose skills are the arm package and whose
    settings file is a harness-written, digest-bound, empty document.
    """
    policy = profile.get("containment_policy") or {}
    sources = policy.get("setting_sources")
    if sources not in SETTING_SOURCES:
        raise RuntimeError("Claude profile must freeze containment_policy.setting_sources as 'none' or 'project'")
    return sources


def _project_settings_path(project: Path) -> Path:
    return project.resolve() / ".claude" / "settings.json"


def _path_is_ancestor(path: Path, child: Path) -> bool:
    resolved = path.resolve()
    child_resolved = child.resolve()
    return resolved == child_resolved or resolved in child_resolved.parents


def _containment_document(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    policy = profile.get("containment_policy") or {}
    if policy.get("kind") != "claude-code-restricted-sandbox-v1":
        raise RuntimeError("Claude profile lacks the required restricted-sandbox containment policy")
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise RuntimeError("contained Claude launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    project_resolved = project.resolve()
    private_root, settings_path, mcp_path = _control_paths(project, env)
    mcp_config, realized_mcp_servers = _mcp_config_document(profile, private_root)
    write_policy = str(policy.get("filesystem_write") or "")
    allow_write = [] if write_policy.startswith("deny") else [str(project_resolved)]
    host_home_raw = os.environ.get("HOME")
    denied_roots = {
        str(private_root),
        "/home",
        "/root",
        "/run/user",
        "/proc",
        "/mnt",
        "/media",
        "/srv",
        "/var/tmp",
    }
    if host_home_raw:
        denied_roots.add(str(Path(host_home_raw).resolve()))
    deny_read_paths = sorted(path for path in denied_roots if Path(path).resolve() != project_resolved)
    deny_write_paths = sorted(
        path for path in denied_roots
        if not _path_is_ancestor(Path(path), project_resolved)
    )
    deny_write_paths = sorted(set(deny_write_paths) | {str(settings_path), str(mcp_path)})
    sources = _setting_sources(profile)
    if sources == "project":
        deny_write_paths = sorted(set(deny_write_paths) | {str(project_resolved / ".claude")})
    if write_policy.startswith("deny"):
        deny_write_paths = sorted(set(deny_write_paths) | {str(project_resolved)})
    elif any(_path_is_ancestor(Path(path), project_resolved) for path in deny_write_paths):
        raise RuntimeError("sandbox deny-write path shadows the writable project")
    settings = {
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False,
            "excludedCommands": [],
            "enableWeakerNestedSandbox": False,
            "network": {
                "allowedDomains": [],
                "allowUnixSockets": [],
                "allowAllUnixSockets": False,
                "allowLocalBinding": False,
            },
            "filesystem": {
                "denyRead": deny_read_paths,
                "allowRead": [str(project_resolved)],
                "denyWrite": deny_write_paths,
                "allowWrite": allow_write,
            },
            "credentials": {
                "envVars": [
                    {"name": name, "mode": "deny"}
                    for name in (
                        "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "AWS_ACCESS_KEY_ID",
                        "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "GITHUB_TOKEN",
                        "GH_TOKEN", "SSH_AUTH_SOCK",
                    )
                ],
            },
        },
        "env": {
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
            "CLAUDE_CODE_DISABLE_CRON": "1",
            "CLAUDE_CODE_DISABLE_ARTIFACT": "1",
            "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
        },
        "disableAllHooks": True,
    }
    if sources == "project":
        settings["permissions"] = {"deny": ["Edit(./.claude/**)", "Write(./.claude/**)", "NotebookEdit(./.claude/**)"]}
    return {
        "schema": 1,
        "settings": settings,
        "realization": {
            "project": str(project_resolved),
            "runtime_home": str(home),
            "private_root": str(private_root),
            "settings_file": str(settings_path),
            "mcp_config": str(mcp_path),
            "mediator_socket": None,
            "mcp_servers": realized_mcp_servers,
            "native_network": "deny",
            "filesystem_deny_roots": deny_read_paths,
            "filesystem_read": [str(project_resolved)],
            "filesystem_write": allow_write,
            "control_files_outside_workspace": True,
            "setting_sources": sources,
            "project_settings_file": str(_project_settings_path(project)) if sources == "project" else None,
            "host_home_inherited": False,
            "ambient_credentials_inherited": False,
            "exact_native_tools": list(profile.get("native_tools") or []),
        },
    }


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Write and digest run-owned private settings and strict MCP configuration."""
    document = _containment_document(profile, project, env)
    private_root, settings, mcp_config = _control_paths(project, env)
    config, realized_servers = _mcp_config_document(profile, private_root)
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(document["settings"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mcp_config.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    document["realization"]["mcp_servers"] = realized_servers
    document["realization"]["settings_sha256"] = hashlib.sha256(settings.read_bytes()).hexdigest()
    document["realization"]["mcp_config_sha256"] = hashlib.sha256(mcp_config.read_bytes()).hexdigest()
    if document["realization"]["setting_sources"] == "project":
        project_settings = _project_settings_path(project)
        project_settings.parent.mkdir(parents=True, exist_ok=True)
        project_settings.write_bytes(PROJECT_SETTINGS_BYTES)
        document["realization"]["project_settings_sha256"] = hashlib.sha256(PROJECT_SETTINGS_BYTES).hexdigest()
    return document


def validate_containment_realization(profile: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    try:
        expected = _containment_document(profile, project, env)
    except (OSError, RuntimeError) as exc:
        return [str(exc)]
    _, settings, mcp_config = _control_paths(project, env)
    if not settings.is_file():
        return ["required private containment settings are absent"]
    if not mcp_config.is_file():
        return ["required private MCP configuration is absent"]
    try:
        actual = json.loads(settings.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["required private containment settings are unreadable or malformed"]
    errors: list[str] = []
    if actual != expected["settings"]:
        errors.append("private containment settings do not match the frozen realization")
    private_root = expected["realization"]["private_root"]
    try:
        expected_mcp, expected_servers = _mcp_config_document(profile, Path(private_root))
    except (OSError, RuntimeError) as exc:
        errors.append(str(exc))
        expected_mcp, expected_servers = {"mcpServers": {}}, []
    try:
        mcp_actual = json.loads(mcp_config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append("required private MCP configuration is unreadable or malformed")
    else:
        if mcp_actual != expected_mcp:
            errors.append("private MCP configuration does not match the frozen realization")
    if expected.get("realization", {}).get("mcp_servers") != expected_servers:
        errors.append("MCP server executable identity changed")

    explicitly_allowed = {
        "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "TMPDIR", "TMP", "TEMP",
        "SSDP70_AUTH_MODE",
    } | PARENT_AUTH_ENV
    forbidden = [key for key in env if key not in SAFE_ENV_KEYS and key not in explicitly_allowed]
    if forbidden:
        errors.append(f"contained environment has undeclared variables: {sorted(forbidden)}")

    auth_keys = [key for key in PARENT_AUTH_ENV if env.get(key)]
    if len(auth_keys) > 1:
        errors.append("contained environment exposes multiple parent authentication variables")
    if auth_keys and env.get("SSDP70_AUTH_MODE") != auth_keys[0]:
        errors.append("parent authentication variable lacks qualification-only source binding")
    if not auth_keys and env.get("SSDP70_AUTH_MODE"):
        errors.append("qualification auth mode is set without a parent authentication variable")
    for source in QUALIFICATION_AUTH_ENV:
        if source in env:
            errors.append(f"qualification auth source {source!r} leaked into Claude environment")

    for key in env:
        if key in PARENT_AUTH_ENV:
            continue
        upper = key.upper()
        if any(token in upper for token in ("TOKEN", "SECRET", "PASSWORD", "API_KEY", "AWS_", "GITHUB_", "SSH_")):
            errors.append(f"contained environment exposes credential-like variable {key!r}")

    run_root = project.resolve().parent
    home_value = env.get("HOME")
    if not isinstance(home_value, str) or not home_value:
        errors.append("contained environment has no run-owned HOME")
    else:
        try:
            Path(home_value).resolve().relative_to(run_root)
        except (OSError, ValueError):
            errors.append("contained environment HOME escapes the run-owned root")
        host_home = os.environ.get("HOME")
        if host_home and Path(home_value).resolve() == Path(host_home).resolve():
            errors.append("contained environment reuses host HOME")
    for key in ("TMPDIR", "TMP", "TEMP"):
        value = env.get(key)
        if value:
            try:
                Path(value).resolve().relative_to(project.resolve())
            except (OSError, ValueError):
                errors.append(f"contained environment {key} escapes the run-owned project")
    realization = expected["realization"]
    for key in ("settings_file", "mcp_config"):
        control_path = Path(realization[key]).resolve()
        try:
            control_path.relative_to(project.resolve())
        except ValueError:
            pass
        else:
            errors.append(f"containment control file {key} is executor/evaluator workspace-reachable")
    if not write_policy_stays_inside_project(expected["settings"]["sandbox"]["filesystem"], project):
        errors.append("sandbox write policy shadows or escapes the declared project boundary")
    if expected["realization"]["setting_sources"] == "project":
        project_settings = _project_settings_path(project)
        try:
            if project_settings.read_bytes() != PROJECT_SETTINGS_BYTES:
                errors.append("project settings source differs from the frozen empty settings document")
        except OSError:
            errors.append("required fixed project settings document is absent")
        local_settings = project.resolve() / ".claude" / "settings.local.json"
        if local_settings.exists():
            errors.append("unexpected project-local settings document present before launch")
    return errors


def validate_post_run_project_state(profile: dict[str, Any], project: Path) -> list[str]:
    """Detect executor tampering with the loaded project settings source after launch."""
    try:
        sources = _setting_sources(profile)
    except RuntimeError as exc:
        return [str(exc)]
    if sources != "project":
        return []
    claude_dir = project.resolve() / ".claude"
    errors: list[str] = []
    try:
        if _project_settings_path(project).read_bytes() != PROJECT_SETTINGS_BYTES:
            errors.append("project settings source changed during execution")
    except OSError:
        errors.append("project settings source missing after execution")
    extra: list[str] = []
    try:
        for entry in claude_dir.iterdir():
            if entry.name in PROJECT_CLAUDE_ALLOWED_ENTRIES:
                continue
            if entry.name in PROJECT_CLAUDE_RUNTIME_EMPTY_DIRS and entry.is_dir() and not entry.is_symlink() and not any(entry.iterdir()):
                continue
            extra.append(entry.name)
        extra.sort()
    except OSError:
        errors.append("project .claude directory missing after execution")
    if extra:
        errors.append(f"unexpected entries appeared in project .claude during execution: {extra}")
    return errors


def write_policy_stays_inside_project(filesystem: dict[str, Any], project: Path) -> bool:
    project_resolved = project.resolve()
    allow_write = filesystem.get("allowWrite") or []
    if allow_write and allow_write != [str(project_resolved)]:
        return False
    if allow_write:
        for denied in filesystem.get("denyWrite") or []:
            if _path_is_ancestor(Path(denied), project_resolved):
                return False
    return True

def install_skills(dist: Path, project: Path) -> None:
    import shutil

    target = project / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    for skill in sorted(SSDP_SKILLS):
        src = dist / skill
        if not src.is_dir():
            raise RuntimeError(f"protocol package is missing skill {skill}")
        shutil.copytree(src, target / skill)


def launch(profile: dict[str, Any], prompt: str, project: Path, env: dict[str, str]) -> dict[str, Any]:
    runtime = profile["provider_runtime"]
    executable = runtime.get("executable", "claude") if isinstance(runtime, dict) else "claude"
    model = profile["agent_model"]
    reasoning = profile["reasoning_configuration"]
    budgets = profile["budgets"]
    allowed_tools = profile.get("native_allowed_tools", [])
    disallowed_tools = profile.get("native_disallowed_tools", [])
    tools = profile.get("native_tools", [])
    containment_errors = validate_containment_realization(profile, project, env)
    if containment_errors:
        raise RuntimeError("; ".join(containment_errors))
    private_root, settings_path, mcp_config_path = _control_paths(project, env)
    _, realized_mcp_servers = _mcp_config_document(profile, private_root)
    mcp_server_sha256 = {
        row["name"]: row["executable_sha256"] for row in realized_mcp_servers
    }
    settings_sha256 = hashlib.sha256(settings_path.read_bytes()).hexdigest()
    mcp_config_sha256 = hashlib.sha256(mcp_config_path.read_bytes()).hexdigest()
    cmd = [
        executable,
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        str(model),
        "--max-turns",
        str(budgets.get("max_turns", 60)),
        "--settings",
        str(settings_path),
        "--mcp-config",
        str(mcp_config_path),
        "--strict-mcp-config",
    ]
    setting_sources = _setting_sources(profile)
    cmd.extend(["--restricted"] if setting_sources == "none" else ["--setting-sources", setting_sources])
    cmd.extend(["--permission-mode", str(profile.get("permission_mode", "default"))])
    cmd.extend(["--tools", ",".join(tools)])
    if allowed_tools:
        cmd.extend(["--allowedTools", " ".join(allowed_tools)])
    if disallowed_tools:
        cmd.extend(["--disallowedTools", " ".join(disallowed_tools)])
    effort = reasoning.get("effort") if isinstance(reasoning, dict) else None
    if effort:
        cmd.extend(["--effort", str(effort)])
    started = time.monotonic()
    proc = subprocess.run(
        cmd,
        cwd=project,
        capture_output=True,
        text=True,
        env=env,
        timeout=int(budgets.get("timeout_s", 3600)),
        stdin=subprocess.DEVNULL,
    )
    if hashlib.sha256(settings_path.read_bytes()).hexdigest() != settings_sha256:
        raise RuntimeError("containment settings changed during Claude execution")
    if hashlib.sha256(mcp_config_path.read_bytes()).hexdigest() != mcp_config_sha256:
        raise RuntimeError("strict MCP configuration changed during Claude execution")
    for row in realized_mcp_servers:
        server_file = Path(row["executable_file"])
        if not server_file.is_file() or hashlib.sha256(server_file.read_bytes()).hexdigest() != row["executable_sha256"]:
            raise RuntimeError("qualification MCP server executable changed during Claude execution")
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "wall_s": round(time.monotonic() - started, 3),
        "command_identity": {
            "executable": executable,
            "model": model,
            "reasoning_configuration": reasoning,
            "tools": tools,
            "allowed_tools": allowed_tools,
            "disallowed_tools": disallowed_tools,
            "settings_file": str(settings_path.resolve()),
            "settings_file_sha256": settings_sha256,
            "mcp_config_file": str(mcp_config_path.resolve()),
            "mcp_config_sha256": mcp_config_sha256,
            "mcp_server_executable_sha256": mcp_server_sha256,
            "strict_mcp_config": True,
            "mcp_servers": list(profile.get("mcp_servers") or []),
            "restricted": setting_sources == "none",
            "setting_sources": setting_sources,
            "permission_mode": str(profile.get("permission_mode", "default")),
        },
    }


def _event(run_id: str, sequence: int, kind: str, native_index: int, native_sha256: str, payload: dict[str, Any], status: str = "observed") -> dict[str, Any]:
    return {
        "schema_version": 1,
        "run_id": run_id,
        "event_id": f"e{sequence:06d}",
        "sequence": sequence,
        "actor_id": "executor",
        "kind": kind,
        "native_source": {"stream": "stdout", "native_index": native_index, "native_sha256": native_sha256},
        "status": status,
        "timing": None,
        "payload": payload,
    }


def _resource_identity(tool: str, data: dict[str, Any]) -> str | None:
    if tool == "Read":
        value = data.get("file_path") or data.get("path")
        return value if isinstance(value, str) else None
    if tool in {"Grep", "Glob"}:
        value = data.get("path") or data.get("file_path")
        return value if isinstance(value, str) else None
    return None


def _package_identity(context: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(context, dict):
        return None
    package = context.get("package_identity")
    if not isinstance(package, dict):
        return None
    result = dict(package)
    result["identity_source"] = "verified-install"
    return result


def _resource_metadata(resource_identity: str | None, context: dict[str, Any] | None) -> dict[str, Any]:
    result = {
        "resolved_package_identity": None,
        "resource_sha256": None,
        "resource_bytes": None,
        "resolved_resource_path": None,
    }
    if not isinstance(resource_identity, str) or not resource_identity or not isinstance(context, dict):
        return result
    project_raw = context.get("project")
    skills_raw = context.get("skills_root")
    if not isinstance(project_raw, str) or not isinstance(skills_raw, str):
        return result
    project = Path(project_raw).resolve()
    skills_root = Path(skills_raw).resolve()
    requested = Path(resource_identity)
    candidate = requested if requested.is_absolute() else project / requested
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return result
    if not resolved.is_file():
        return result
    result["resolved_resource_path"] = str(resolved)
    result["resource_bytes"] = resolved.stat().st_size
    result["resource_sha256"] = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if resolved == skills_root or skills_root in resolved.parents:
        result["resolved_package_identity"] = _package_identity(context)
    return result


def _ordinary_root(resource_identity: str | None, context: dict[str, Any] | None) -> str | None:
    if not isinstance(resource_identity, str) or not resource_identity or not isinstance(context, dict):
        return None
    skills_raw = context.get("skills_root")
    project_raw = context.get("project")
    if not isinstance(skills_raw, str) or not isinstance(project_raw, str):
        return None
    skills_root = Path(skills_raw).resolve()
    project = Path(project_raw).resolve()
    requested = Path(resource_identity)
    candidate = requested if requested.is_absolute() else project / requested
    try:
        resolved = candidate.resolve(strict=True)
        rel = resolved.relative_to(skills_root)
    except (OSError, ValueError):
        return None
    if len(rel.parts) == 2 and rel.parts[1] == "SKILL.md" and rel.parts[0] in SSDP_SKILLS:
        return rel.parts[0]
    return None


def _result_digest(content: Any) -> str:
    payload = json.dumps(content, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def runtime_observation(stdout: str) -> dict[str, Any]:
    for line in stdout.splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if raw.get("type") == "system" and raw.get("subtype") == "init":
            return {
                "model": raw.get("model"),
                "runtime_version": raw.get("claude_code_version"),
                "tools": raw.get("tools") or [],
                "native_capabilities": raw.get("capabilities") or [],
                "messaging_socket_path": raw.get("messaging_socket_path"),
                "memory_paths": raw.get("memory_paths") or {},
                "mcp_servers": raw.get("mcp_servers") or [],
                "permission_mode": raw.get("permissionMode"),
            }
    return {}


def normalize(stdout: str, run_id: str, context: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], int]:
    events: list[dict[str, Any]] = []
    completeness: list[dict[str, Any]] = []
    errors: list[str] = []
    sequence = 0
    lines = stdout.splitlines()
    pending: dict[str, list[dict[str, Any]]] = {}
    selected_skill_roots: list[str] = []
    package_identity = _package_identity(context)

    def emit(kind: str, native_index: int, native_sha256: str, payload: dict[str, Any], status: str = "observed") -> dict[str, Any]:
        nonlocal sequence
        sequence += 1
        event = _event(run_id, sequence, kind, native_index, native_sha256, payload, status=status)
        events.append(event)
        return event

    def register_pending(tool_use_id: str, kind: str, payload: dict[str, Any]) -> None:
        pending.setdefault(tool_use_id, []).append({"kind": kind, "payload": dict(payload)})

    def mcp_payload(content: Any) -> dict[str, Any] | None:
        texts: list[str] = []
        if isinstance(content, str):
            texts = [content]
        elif isinstance(content, list):
            texts = [row.get("text") for row in content if isinstance(row, dict) and isinstance(row.get("text"), str)]
        for text in texts:
            try:
                value = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and isinstance(value.get("evidence"), dict):
                return value
        return None

    def consume_result(block: dict[str, Any], native_index: int, native_sha256: str, block_index: int, mapped: list[str]) -> None:
        tool_use_id = block.get("tool_use_id")
        if not isinstance(tool_use_id, str) or tool_use_id not in pending:
            errors.append(f"native tool result {tool_use_id!r} has no matching tool-use event")
            return
        content = block.get("content")
        result_status = "error" if block.get("is_error") else "result"
        reference = f"trace:{native_index}:block:{block_index}"
        priors = pending.pop(tool_use_id)
        mediated = mcp_payload(content)
        for prior in priors:
            if prior["kind"] == "root_selection" and result_status == "result":
                logical_root = prior["payload"].get("logical_root")
                if isinstance(logical_root, str) and logical_root:
                    selected_skill_roots.append(logical_root)
            if prior["kind"] == "delegate_call":
                payload = {
                    "delegate_id": prior["payload"]["delegate_id"],
                    "parent_actor": prior["payload"]["parent_actor"],
                    "tool_use_id": tool_use_id,
                    "result_reference": reference,
                    "result_sha256": _result_digest(content),
                    "result_content": content,
                }
                event = emit("delegate_return", native_index, native_sha256, payload, status=result_status)
            else:
                payload = dict(prior["payload"])
                payload.update({
                    "result_status": result_status,
                    "result_reference": reference,
                    "result_sha256": _result_digest(content),
                    "result_content": content,
                })
                if mediated is not None:
                    evidence = mediated.get("evidence") or {}
                    for key in ("store_identity", "operation", "query", "object_ids", "before_object_version", "after_object_version"):
                        if key in evidence:
                            payload[key] = evidence[key]
                    if mediated.get("returncode") not in (None, 0):
                        payload["result_status"] = "error"
                if prior["kind"] in {"mutation", "network_external_action"}:
                    payload["disposition"] = "blocked-or-error" if payload["result_status"] == "error" else "sandboxed"
                event = emit(prior["kind"], native_index, native_sha256, payload, status=payload["result_status"])
            mapped.append(event["event_id"])

    for native_index, line in enumerate(lines):
        native_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
        mapped: list[str] = []
        classification = "explicit-benign-metadata"
        oracle_relevant = False
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            completeness.append({
                "native_index": native_index,
                "native_sha256": native_sha256,
                "mapped_event_ids": [],
                "classification": "unparseable-native-event",
                "oracle_relevant": True,
            })
            errors.append(f"native event {native_index} is not valid JSON")
            continue

        raw_type = raw.get("type")
        if raw_type == "system" and raw.get("subtype") == "init":
            skills = [s if isinstance(s, str) else s.get("name", "") for s in raw.get("skills") or []]
            event = emit("catalog_snapshot", native_index, native_sha256, {
                "logical_skill_ids": skills,
                "model": raw.get("model"),
                "runtime_version": raw.get("claude_code_version"),
                "resolved_package_identity": package_identity,
                "native_tools": raw.get("tools") or [],
            })
            mapped.append(event["event_id"])
            classification = "catalog"
            oracle_relevant = True

        elif raw_type == "assistant":
            classification = "assistant-message"
            content = raw.get("message", {}).get("content", [])
            if not isinstance(content, list):
                content = []
            for block_index, block in enumerate(content):
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                oracle_relevant = True
                tool = block.get("name")
                data = block.get("input") or {}
                tool_use_id = block.get("id")
                if not isinstance(data, dict):
                    data = {"raw": data}
                if not isinstance(tool_use_id, str) or not tool_use_id:
                    errors.append(f"native tool use {tool!r} lacks stable tool-use id")
                    continue

                if tool == "Skill":
                    skill = data.get("skill") or data.get("command")
                    payload = {
                        "logical_root": skill,
                        "selection_mechanism": "Skill",
                        "native_operation": tool,
                        "input": data,
                        "resolved_package_identity": package_identity,
                        "tool_use_id": tool_use_id,
                    }
                    event = emit("root_selection", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "root_selection", payload)

                elif tool in READ_TOOLS:
                    resource_identity = _resource_identity(tool, data)
                    metadata = _resource_metadata(resource_identity, context)
                    ordinary_root = _ordinary_root(resource_identity, context)
                    if ordinary_root is not None:
                        root_event = emit("root_selection", native_index, native_sha256, {
                            "logical_root": ordinary_root,
                            "selection_mechanism": "ordinary-resource-read",
                            "native_operation": tool,
                            "input": data,
                            "resolved_package_identity": metadata["resolved_package_identity"],
                            "tool_use_id": tool_use_id,
                        }, status="observed")
                        mapped.append(root_event["event_id"])
                    payload = {
                        "operation": tool.lower(),
                        "resource_identity": resource_identity,
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                        "resolved_package_identity": metadata["resolved_package_identity"],
                        "resource_sha256": metadata["resource_sha256"],
                        "resource_bytes": metadata["resource_bytes"],
                        "resolved_resource_path": metadata["resolved_resource_path"],
                    }
                    event = emit("resource_access", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "resource_access", payload)

                elif tool in MCP_ISSUE_READ_TOOLS:
                    operation = MCP_ISSUE_READ_TOOLS[tool]
                    payload = {
                        "operation": operation,
                        "resource_identity": "ssdp70-private-issue-standin",
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("issue_evidence_access", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "issue_evidence_access", payload)

                elif tool in MCP_ISSUE_MUTATION_TOOLS:
                    operation = MCP_ISSUE_MUTATION_TOOLS[tool]
                    access = {
                        "operation": operation,
                        "resource_identity": "ssdp70-private-issue-standin",
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("issue_evidence_access", native_index, native_sha256, access, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "issue_evidence_access", access)
                    target = data.get("issue_id") or data.get("location")
                    mutation = {
                        "operation": operation,
                        "logical_target": target,
                        "workspace_external_class": "qualification-owned-standin",
                        "authorization_decision": "sandbox-mediate",
                        "disposition": "attempted",
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("mutation", native_index, native_sha256, mutation, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "mutation", mutation)

                elif tool == MCP_DELEGATE_TOOL:
                    payload = {
                        "delegate_id": data.get("agent") or tool_use_id,
                        "parent_actor": "executor",
                        "request": data,
                        "launched_work_relation": "scripted-qualification-standin",
                        "tool_use_id": tool_use_id,
                    }
                    event = emit("delegate_call", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "delegate_call", payload)

                elif tool in MUTATION_TOOLS:
                    target = data.get("file_path") or data.get("path") or data.get("notebook_path")
                    payload = {
                        "operation": tool.lower(),
                        "logical_target": target,
                        "workspace_external_class": "unresolved",
                        "authorization_decision": "profile-governed",
                        "disposition": "attempted",
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("mutation", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "mutation", payload)

                elif tool in DELEGATE_TOOLS:
                    payload = {
                        "delegate_id": data.get("name") or data.get("subagent_type") or tool_use_id,
                        "parent_actor": "executor",
                        "request": data,
                        "launched_work_relation": "requested",
                        "tool_use_id": tool_use_id,
                    }
                    event = emit("delegate_call", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "delegate_call", payload)

                elif tool in NETWORK_TOOLS:
                    payload = {
                        "destination_service": data.get("url") or data.get("query"),
                        "operation": tool,
                        "authorization_decision": "profile-governed",
                        "disposition": "attempted",
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("network_external_action", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "network_external_action", payload)

                elif tool == "Bash":
                    payload = {
                        "semantic_capability_classes": ["process_execution"],
                        "native_operation": tool,
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("tool_action", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    register_pending(tool_use_id, "tool_action", payload)

                else:
                    payload = {
                        "semantic_capability_classes": ["unclassified-native-tool"],
                        "native_operation": tool,
                        "input": data,
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    event = emit("tool_action", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    errors.append(f"native tool {tool!r} has no semantic capability mapping")

        elif raw_type == "system" and raw.get("subtype") in {"thinking_tokens", "post_turn_summary"}:
            classification = f"reviewed-non-oracle-system:{raw.get('subtype')}"
            oracle_relevant = False

        elif raw_type == "user":
            classification = "user-message"
            content = raw.get("message", {}).get("content", raw.get("content", []))
            if raw.get("isSynthetic") is True:
                classification = "skill-injected-resource"
                oracle_relevant = True
                text_blocks = [
                    block.get("text") for block in content
                    if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str)
                ]
                if not selected_skill_roots:
                    errors.append(f"synthetic skill body at native event {native_index} has no successful root selection")
                elif len(text_blocks) != 1 or "\n\n" not in text_blocks[0]:
                    errors.append(f"synthetic skill body at native event {native_index} is malformed")
                elif not isinstance(context, dict) or not isinstance(context.get("skills_root"), str):
                    errors.append(f"synthetic skill body at native event {native_index} has no installed skills root")
                else:
                    logical_root = selected_skill_roots[-1]
                    installed = Path(context["skills_root"]) / logical_root / "SKILL.md"
                    try:
                        installed_bytes = installed.read_bytes()
                        installed_text = installed_bytes.decode("utf-8")
                    except (OSError, UnicodeDecodeError) as exc:
                        errors.append(f"cannot verify injected SKILL.md for {logical_root!r}: {exc}")
                    else:
                        prefix, injected = text_blocks[0].split("\n\n", 1)
                        if not prefix.startswith("Base directory for this skill: "):
                            errors.append(f"synthetic skill body at native event {native_index} lacks base-directory binding")
                        elif injected != installed_text:
                            errors.append(f"synthetic skill body for {logical_root!r} does not match installed SKILL.md bytes")
                        else:
                            payload = {
                                "operation": "skill-injected-body",
                                "resource_identity": str(installed),
                                "input": {"logical_root": logical_root, "base_directory_declaration": prefix},
                                "tool_use_id": f"skill-injected:{native_index}",
                                "result_status": "result",
                                "result_reference": f"trace:{native_index}:synthetic-skill-body",
                                "result_sha256": _result_digest(injected),
                                "result_content": injected,
                                "resolved_package_identity": package_identity,
                                "resource_sha256": hashlib.sha256(installed_bytes).hexdigest(),
                                "resource_bytes": len(installed_bytes),
                                "resolved_resource_path": str(installed.resolve()),
                            }
                            event = emit("resource_access", native_index, native_sha256, payload, status="result")
                            mapped.append(event["event_id"])
                completeness.append({
                    "native_index": native_index,
                    "native_sha256": native_sha256,
                    "mapped_event_ids": mapped,
                    "classification": classification,
                    "oracle_relevant": oracle_relevant,
                })
                continue
            if not isinstance(content, list):
                content = []
            for block_index, block in enumerate(content):
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                oracle_relevant = True
                consume_result(block, native_index, native_sha256, block_index, mapped)

        elif raw_type == "tool_result":
            classification = "tool-result"
            oracle_relevant = True
            consume_result(raw, native_index, native_sha256, 0, mapped)

        elif raw_type == "result":
            classification = "terminal-result"
            oracle_relevant = True
            term = emit("termination", native_index, native_sha256, {
                "state": raw.get("subtype") or ("error" if raw.get("is_error") else "completed"),
                "native_return_state": {"is_error": raw.get("is_error")},
                "terminal_result_exists": "result" in raw,
            })
            mapped.append(term["event_id"])
            result_text = raw.get("result", "")
            if not isinstance(result_text, str):
                result_text = str(result_text)
            final = emit("final_result", native_index, native_sha256, {
                "result_text": result_text,
                "artifact_reference": "final-report.md",
            })
            mapped.append(final["event_id"])
            usage = emit("usage_timing", native_index, native_sha256, {
                "duration_ms": raw.get("duration_ms"),
                "duration_unit": "ms",
                "usage": raw.get("usage"),
                "usage_source": "provider-result-event",
            })
            mapped.append(usage["event_id"])

        elif raw_type == "rate_limit_event":
            classification = "explicit-benign-rate-limit-metadata"
            oracle_relevant = False

        else:
            classification = f"unknown-native-type:{raw_type}"
            oracle_relevant = True
            errors.append(f"native event {native_index} type {raw_type!r} has no reviewed classification")

        completeness.append({
            "native_index": native_index,
            "native_sha256": native_sha256,
            "mapped_event_ids": mapped,
            "classification": classification,
            "oracle_relevant": oracle_relevant,
        })

    for tool_use_id, rows in sorted(pending.items()):
        kinds = ",".join(row["kind"] for row in rows)
        errors.append(f"native tool use {tool_use_id!r} has no exposed tool result for {kinds}")

    return events, completeness, errors, len(lines)


def final_result(events: list[dict[str, Any]]) -> str:
    for event in reversed(events):
        if event.get("kind") == "final_result":
            return str(event.get("payload", {}).get("result_text") or "")
    return ""


def catalog_isolation(events: list[dict[str, Any]]) -> dict[str, Any]:
    snapshots = [e for e in events if e.get("kind") == "catalog_snapshot"]
    if len(snapshots) != 1:
        return {"ok": False, "reason": f"expected one catalog snapshot, found {len(snapshots)}"}
    payload = snapshots[0].get("payload") or {}
    skills = payload.get("logical_skill_ids") or []
    counts = {name: skills.count(name) for name in SSDP_SKILLS}
    package = payload.get("resolved_package_identity")
    package_ok = isinstance(package, dict) and isinstance(package.get("package_sha256"), str) and len(package["package_sha256"]) == 64
    return {
        "ok": all(value == 1 for value in counts.values()) and package_ok,
        "ssdp_counts": counts,
        "catalog": skills,
        "resolved_package_identity": package,
    }


def owner_reads(events: list[dict[str, Any]], owner_name: str) -> list[int]:
    hits: list[int] = []
    for event in events:
        if event.get("kind") != "resource_access" or event.get("status") != "result":
            continue
        payload = event.get("payload") or {}
        if payload.get("result_status") != "result":
            continue
        if owner_name in str(payload.get("resource_identity") or ""):
            hits.append(int(event["sequence"]))
    return hits


def prepare_prompt(profile: dict[str, Any], entry: str, prompt: str) -> str:
    if not entry.startswith("pinned:"):
        return prompt.strip()
    root = entry.split(":", 1)[1]
    template = profile.get("pinned_root_instruction_template", "Use the {root} skill. {prompt}")
    return str(template).format(root=root, prompt=prompt.strip())
