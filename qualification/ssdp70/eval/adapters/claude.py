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
import time
from pathlib import Path
from typing import Any

ADAPTER_ID = "claude-stream-json-v2"
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
    return private_root, control / "settings.json", control / "mcp-empty.json"


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
    mediator = env.get("SSDP70_MEDIATOR_SOCKET")
    if policy.get("mediator_required") and not mediator:
        raise RuntimeError("executor containment requires the harness mediator socket")
    allow_sockets = [str(Path(mediator).resolve())] if mediator else []
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
                "allowUnixSockets": allow_sockets,
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
    }
    return {
        "schema": 1,
        "settings": settings,
        "realization": {
            "project": str(project_resolved),
            "runtime_home": str(home),
            "private_root": str(private_root),
            "settings_file": str(settings_path),
            "mcp_config": str(mcp_path),
            "mediator_socket": allow_sockets[0] if allow_sockets else None,
            "native_network": "deny",
            "filesystem_deny_roots": deny_read_paths,
            "filesystem_read": [str(project_resolved)],
            "filesystem_write": allow_write,
            "control_files_outside_workspace": True,
            "host_home_inherited": False,
            "ambient_credentials_inherited": False,
            "exact_native_tools": list(profile.get("native_tools") or []),
        },
    }


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Write run-owned private control files before any executor/evaluator effect."""
    document = _containment_document(profile, project, env)
    _, settings, mcp_config = _control_paths(project, env)
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(document["settings"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mcp_config.write_text(json.dumps({"mcpServers": {}}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    document["realization"]["mcp_servers"] = []
    document["realization"]["settings_sha256"] = hashlib.sha256(settings.read_bytes()).hexdigest()
    document["realization"]["mcp_config_sha256"] = hashlib.sha256(mcp_config.read_bytes()).hexdigest()
    return document


def validate_containment_realization(profile: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    expected = _containment_document(profile, project, env)
    _, settings, mcp_config = _control_paths(project, env)
    if not settings.is_file():
        return ["required private containment settings are absent"]
    if not mcp_config.is_file():
        return ["required private empty MCP configuration is absent"]
    try:
        actual = json.loads(settings.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["required private containment settings are unreadable or malformed"]
    errors: list[str] = []
    if actual != expected["settings"]:
        errors.append("private containment settings do not match the frozen realization")
    try:
        mcp_actual = json.loads(mcp_config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append("required private empty MCP configuration is unreadable or malformed")
    else:
        if mcp_actual != {"mcpServers": {}}:
            errors.append("MCP configuration is not empty")
    explicitly_allowed = {
        "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "TMPDIR", "TMP", "TEMP",
        "SSDP70_MEDIATOR_SOCKET", "SSDP70_ACCOUNT", "SSDP70_AUTH_MODE",
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
    _, settings_path, mcp_config_path = _control_paths(project, env)
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
        "--restricted",
        "--permission-mode",
        str(profile.get("permission_mode", "acceptEdits")),
    ]
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
            "strict_mcp_config": True,
            "restricted": True,
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
            }
    return {}


def normalize(stdout: str, run_id: str, context: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], int]:
    events: list[dict[str, Any]] = []
    completeness: list[dict[str, Any]] = []
    errors: list[str] = []
    sequence = 0
    lines = stdout.splitlines()
    pending: dict[str, dict[str, Any]] = {}
    selected_skill_roots: list[str] = []
    package_identity = _package_identity(context)

    def emit(kind: str, native_index: int, native_sha256: str, payload: dict[str, Any], status: str = "observed") -> dict[str, Any]:
        nonlocal sequence
        sequence += 1
        event = _event(run_id, sequence, kind, native_index, native_sha256, payload, status=status)
        events.append(event)
        return event

    def register_pending(tool_use_id: str, kind: str, payload: dict[str, Any]) -> None:
        pending[tool_use_id] = {"kind": kind, "payload": dict(payload)}

    def consume_result(block: dict[str, Any], native_index: int, native_sha256: str, block_index: int, mapped: list[str]) -> None:
        tool_use_id = block.get("tool_use_id")
        if not isinstance(tool_use_id, str) or tool_use_id not in pending:
            errors.append(f"native tool result {tool_use_id!r} has no matching tool-use event")
            return
        prior = pending.pop(tool_use_id)
        content = block.get("content")
        result_status = "error" if block.get("is_error") else "result"
        reference = f"trace:{native_index}:block:{block_index}"
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
            if prior["kind"] in {"mutation", "network_external_action"}:
                payload["disposition"] = "blocked-or-error" if result_status == "error" else "completed"
            event = emit(prior["kind"], native_index, native_sha256, payload, status=result_status)
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

    for tool_use_id, row in sorted(pending.items()):
        errors.append(f"native tool use {tool_use_id!r} has no exposed tool result for {row['kind']}")

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
