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
import shutil
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
    "PATH", "LANG", "LC_ALL", "LC_CTYPE", "TERM", "TMPDIR", "TMP", "TEMP",
    "SSL_CERT_FILE", "SSL_CERT_DIR",
}


def clean_env() -> dict[str, str]:
    """Return an explicit non-credential allow-list; never inherit host HOME/tokens."""
    env = {key: os.environ[key] for key in SAFE_ENV_KEYS - {"PATH", "TMPDIR", "TMP", "TEMP"} if key in os.environ}
    env["PATH"] = "/usr/local/bin:/usr/bin:/bin"
    return env


def _containment_document(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    policy = profile.get("containment_policy") or {}
    if policy.get("kind") != "bwrap-plus-claude-sandbox-v1":
        raise RuntimeError("Claude profile lacks the required bwrap containment policy")
    mode = policy.get("workspace_mode")
    if mode not in {"read-write", "read-only"}:
        raise RuntimeError("containment policy must declare read-write or read-only workspace mode")
    mediator = env.get("SSDP70_MEDIATOR_SOCKET")
    if policy.get("mediator_required") and not mediator:
        raise RuntimeError("executor containment requires the harness mediator socket")
    allow_sockets = ["/run/ssdp70/mediator.sock"] if mediator else []
    return {
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False,
            "excludedCommands": [],
            "enableWeakerNestedSandbox": False,
            "network": {
                "allowedDomains": [],
                "strictAllowlist": True,
                "allowUnixSockets": [],
                "allowAllUnixSockets": bool(allow_sockets),
                "allowLocalBinding": False
            }
        },
        "env": {
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"
        },
        "ssdp70Containment": {
            "schema": 1,
            "substrate": "bubblewrap",
            "workspace_mode": mode,
            "provider_control_plane_network": "runtime-only",
            "executor_process_network": "strict-empty-allowlist-via-claude-sandbox",
            "sandbox_fail_closed": True,
            "unix_socket_policy": (
                "allow-all-inside-bwrap-namespace; only qualification mediator is host-mounted"
                if allow_sockets else "deny"
            ),
            "mediator_socket": allow_sockets[0] if allow_sockets else None,
            "host_home_visible": False,
            "ambient_credentials_visible": False
        }
    }


def _resolve_runtime_executable(profile: dict[str, Any]) -> Path:
    runtime = profile.get("provider_runtime") or {}
    requested = runtime.get("executable", "claude") if isinstance(runtime, dict) else "claude"
    resolved = shutil.which(str(requested))
    if not resolved:
        raise RuntimeError(f"required Claude executable {requested!r} is unavailable")
    return Path(resolved).resolve()


def _bwrap_prefix(
    profile: dict[str, Any],
    project: Path,
    env: dict[str, str],
    runtime_copy: Path,
) -> list[str]:
    bwrap = shutil.which("bwrap")
    if not bwrap:
        raise RuntimeError("required Bubblewrap executable 'bwrap' is unavailable")
    policy = profile.get("containment_policy") or {}
    mode = policy.get("workspace_mode")
    project_flag = "--bind" if mode == "read-write" else "--ro-bind"
    cmd = [
        bwrap,
        "--die-with-parent",
        "--new-session",
        "--unshare-user",
        "--unshare-pid",
        "--unshare-ipc",
        "--unshare-uts",
        "--unshare-cgroup-try",
        "--share-net",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--dir", "/workspace",
        project_flag, str(project.resolve()), "/workspace",
        "--dir", "/runtime",
        "--ro-bind", str(runtime_copy.resolve()), "/runtime/claude",
        "--dir", "/home",
        "--dir", "/home/ssdp70",
        "--dir", "/run",
        "--dir", "/run/ssdp70",
        "--setenv", "HOME", "/home/ssdp70",
        "--setenv", "XDG_CONFIG_HOME", "/home/ssdp70/.config",
        "--setenv", "XDG_CACHE_HOME", "/home/ssdp70/.cache",
        "--setenv", "CLAUDE_CODE_DISABLE_AUTO_MEMORY", "1",
        "--chdir", "/workspace",
    ]
    for system_root in ("/usr", "/bin", "/lib", "/lib64", "/etc/ssl", "/etc/ca-certificates"):
        if Path(system_root).exists():
            cmd.extend(["--ro-bind", system_root, system_root])
    for system_file in ("/etc/resolv.conf", "/etc/nsswitch.conf", "/etc/hosts", "/etc/passwd", "/etc/group"):
        if Path(system_file).is_file():
            cmd.extend(["--ro-bind", system_file, system_file])
    mediator = env.get("SSDP70_MEDIATOR_SOCKET")
    if mediator:
        mediator_path = Path(mediator).resolve()
        if not mediator_path.exists():
            raise RuntimeError("mediator socket does not exist before executor launch")
        cmd.extend(["--ro-bind", str(mediator_path), "/run/ssdp70/mediator.sock"])
        cmd.extend(["--setenv", "SSDP70_MEDIATOR_SOCKET", "/run/ssdp70/mediator.sock"])
    account = env.get("SSDP70_ACCOUNT")
    if account:
        cmd.extend(["--setenv", "SSDP70_ACCOUNT", account])
    return cmd


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Materialize project settings and a run-owned copy of the Claude runtime."""
    document = _containment_document(profile, project, env)
    settings = project / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    runtime_source = _resolve_runtime_executable(profile)
    runtime_dir = project.parent / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    runtime_copy = runtime_dir / "claude"
    shutil.copy2(runtime_source, runtime_copy)
    runtime_copy.chmod(0o755)
    env["_SSDP70_RUNTIME_COPY"] = str(runtime_copy)
    return {
        "schema": 1,
        "settings_path": str(settings),
        "settings_sha256": hashlib.sha256(settings.read_bytes()).hexdigest(),
        "runtime_source": str(runtime_source),
        "runtime_copy": str(runtime_copy),
        "runtime_copy_sha256": hashlib.sha256(runtime_copy.read_bytes()).hexdigest(),
        "bwrap_executable": shutil.which("bwrap"),
        "workspace_mode": (profile.get("containment_policy") or {}).get("workspace_mode"),
        "mediator_socket_mounted": bool(env.get("SSDP70_MEDIATOR_SOCKET")),
        "network_model": {
            "provider_control_plane": "shared host network for Claude runtime",
            "executor_bash": "Claude sandbox deny-all",
            "native_web_tools": "excluded by exact --tools surface"
        },
        "host_home_visible": False,
        "ambient_credentials_visible": False
    }


def validate_containment_realization(profile: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    errors: list[str] = []
    try:
        expected = _containment_document(profile, project, env)
    except RuntimeError as exc:
        return [str(exc)]
    settings = project / ".claude" / "settings.json"
    if not settings.is_file():
        errors.append("required project containment settings are absent")
    else:
        try:
            actual = json.loads(settings.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            errors.append("required project containment settings are unreadable or malformed")
        else:
            if actual != expected:
                errors.append("project containment settings do not match the frozen realization")
    if not shutil.which("bwrap"):
        errors.append("required Bubblewrap executable is unavailable")
    runtime_copy = env.get("_SSDP70_RUNTIME_COPY")
    if not runtime_copy or not Path(runtime_copy).is_file():
        errors.append("run-owned Claude runtime copy is unavailable")
    allowed = SAFE_ENV_KEYS | {"SSDP70_MEDIATOR_SOCKET", "SSDP70_ACCOUNT", "_SSDP70_RUNTIME_COPY"}
    forbidden = sorted(key for key in env if key not in allowed)
    if forbidden:
        errors.append(f"contained environment has undeclared variables: {forbidden}")
    for key in env:
        upper = key.upper()
        if any(token in upper for token in ("TOKEN", "SECRET", "PASSWORD", "API_KEY", "AWS_", "GITHUB_", "SSH_")):
            errors.append(f"contained environment exposes credential-like variable {key!r}")
    return errors


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
    runtime_copy = Path(env["_SSDP70_RUNTIME_COPY"])
    cmd = _bwrap_prefix(profile, project, env, runtime_copy) + [
        "/runtime/claude",
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        str(model),
        "--max-turns",
        str(budgets.get("max_turns", 60)),
        "--setting-sources",
        "project",
        "--settings",
        "/workspace/.claude/settings.json",
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
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "wall_s": round(time.monotonic() - started, 3),
        "command_identity": {
            "executable": executable,
            "substrate_launcher": "bwrap",
            "model": model,
            "reasoning_configuration": reasoning,
            "tools": tools,
            "allowed_tools": allowed_tools,
            "disallowed_tools": disallowed_tools,
            "setting_sources": ["project"],
            "settings_file": "/workspace/.claude/settings.json",
            "restricted": False,
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
                        elif injected.replace("\r\n", "\n").rstrip("\n") != installed_text.replace("\r\n", "\n").rstrip("\n"):
                            errors.append(f"synthetic skill body for {logical_root!r} does not match normalized installed SKILL.md text")
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
