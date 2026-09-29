#!/usr/bin/env python3
"""Oh My Pi (`omp`) Stage F runtime adapter (SSDP 7.0 portability, OMP-only slice).

Authority: the OMP provider-adaptation slice of
workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md
and qualification/ssdp70/PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md.

Accepted D3/D4 Architecture:
  - Three logical principals: Supervisor, Trusted Observer, Subject/Executor.
  - Trusted Observer owns provider credentials and provides the only route to upstream inference;
    it verifies client peer processes via /proc and logs hash-linked request/catalog observations.
  - Subject/Executor runs under minimal bwrap containment (denied host HOME, custody paths,
    supervisor private state, mediator private backing files).
  - Control files (config.yml, mcp.json, models.yml, skills) are mounted read-only and
    digest-checked across launch.
  - Native tools are constrained to read, bash, edit, glob, grep, write + 6 qualification MCP tools.
  - Mediator calls (locations, search, show, create, comment, delegate) are normalized losslessly
    with strict serverName/mcpToolName cross-validation.
  - Root selection is normalized on skill access with T1/T7/T8 observability.
  - Ambient discovery is closed across project and runtime HOME.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import core70  # noqa: E402

ADAPTER_ID = "omp-json-v1"

SSDP_SKILLS = frozenset({
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-maintenance-audit",
    "software-documentation",
    "repository-hygiene",
})

OMP_EXECUTABLE = "omp"
OMP_OBSERVED_VERSION = "18.0.11"
OMP_OBSERVED_SHA256 = "6054460b29e9bad5eba78336f291e1979c2fa0a5cd96fc2d92afd666cc681d26"
OMP_OBSERVED_BYTES = 194573512
OMP_OBSERVED_BUILD_ID = "2c2e51f3b6fae6722da4f7b69751a2e9467ab063"

OMP_AGENT_RELATIVE = Path(".omp") / "agent"
OMP_SKILLS_SUBDIR = "skills"
OMP_MCP_CONFIG_NAME = "mcp.json"
OMP_PROJECT_DISCOVERY_PATHS = (".omp", "mcp.json", ".mcp.json", ".cursor", ".vscode")

OMP_DEVICE_SCHEME = "xd://"
OMP_MCP_ID_PREFIX = "mcp__"
OMP_MCP_SERVER_NAME = "ssdp70"
OMP_MCP_SERVER_ID = "ssdp70-qualification-stdio-v1"
OMP_MCP_SERVER_ENTRYPOINT = "stub_tools/mediator.py"

# Constrained native tool surface: exactly 6 builtins matching the profile
OMP_BUILTIN_TOOLS = (
    "read", "bash", "edit", "glob", "grep", "write",
)

OMP_RAW_MCP_TOOLS = (
    "issue_locations", "issue_search", "issue_show", "issue_create", "issue_comment", "delegate",
)
OMP_MCP_TOOL_KINDS = {
    "issue_locations": "issue_evidence_access",
    "issue_search": "issue_evidence_access",
    "issue_show": "issue_evidence_access",
    "issue_create": "mutation",
    "issue_comment": "mutation",
    "delegate": "delegate_call",
}

OMP_TOOL_CLASSES = {
    "read": ("resource_access", ("workspace_read_search_list",)),
    "glob": ("resource_access", ("workspace_read_search_list",)),
    "grep": ("resource_access", ("workspace_read_search_list",)),
    "write": ("mutation", ("workspace_mutation",)),
    "edit": ("mutation", ("workspace_mutation",)),
    "bash": ("tool_action", ("process_execution",)),
    "eval": ("tool_action", ("process_execution",)),
    "task": ("delegate_call", ("delegation",)),
    "hub": ("tool_action", ("delegation",)),
    "todo": ("tool_action", ("issue_evidence_store",)),
    "web_search": ("network_external_action", ("network_remote_service",)),
}

OMP_KNOWN_EVENT_TYPES = frozenset({
    "session", "agent_start", "turn_start", "message_start", "message_update",
    "message_end", "turn_end", "tool_execution_start", "tool_execution_update",
    "tool_execution_end", "auto_retry_end", "agent_end",
})
OMP_BENIGN_EVENT_TYPES = frozenset({
    "session", "agent_start", "turn_start", "message_start", "message_update",
    "message_end", "turn_end", "tool_execution_update",
})

CONTAINMENT_KIND = "omp-bwrap-substrate-v1"
CREDENTIAL_ISOLATION_KIND = "external-broker-outside-sandbox"
CREDENTIAL_ENV_NAMES = (
    "OMP_API_KEY", "OMP_AUTH_TOKEN", "OPENAI_API_KEY", "ANTHROPIC_API_KEY",
    "DEEPINFRA_API_KEY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN",
    "GH_TOKEN", "SSH_AUTH_SOCK",
)

SAFE_ENV_KEYS = ("PATH", "LANG")
MINIMAL_PATH = "/usr/bin:/bin"

_LAST_OBSERVATION: dict[str, Any] | None = None


def set_last_observation(obs: dict[str, Any] | None) -> None:
    global _LAST_OBSERVATION
    _LAST_OBSERVATION = obs


# --------------------------------------------------------------------------- env

def clean_env() -> dict[str, str]:
    """Minimal, credential-free environment. The harness adds run-owned HOME/XDG/TMPDIR."""
    env = {key: os.environ[key] for key in SAFE_ENV_KEYS if key in os.environ}
    env.setdefault("PATH", MINIMAL_PATH)
    env["NO_COLOR"] = "1"
    env["TERM"] = "dumb"
    return env


def project_control_paths(profile: dict[str, Any]) -> list[str]:
    """OMP run-owned control state lives outside the project; the project must be clean."""
    return []


# ------------------------------------------------------------------- MCP binding

def _sanitize_component(name: str) -> str:
    """OMP v18.0.11 authority: lowercase, non-alpha/underscore to underscore, collapse underscores, strip underscores."""
    s = re.sub(r"[^a-z_]+", "_", str(name).lower())
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def mcp_native_id(server: str, tool: str) -> str:
    """OMP v18.0.11 device-id authority algorithm (from binary hft/Qro)."""
    s = _sanitize_component(server) or "server"
    n = _sanitize_component(tool) or "tool"
    if n.startswith(s + "_"):
        r = n[len(s) + 1:]
    else:
        r = n
    device = f"{OMP_MCP_ID_PREFIX}{s}_{r}"
    if len(device) > 64:
        h = hashlib.sha256(device.encode("utf-8")).hexdigest()[:8]
        device = f"{device[:55]}_{h}"
    return device


def expected_mcp_native_ids(server: str, tools: tuple[str, ...] | list[str] = OMP_RAW_MCP_TOOLS) -> dict[str, str]:
    return {tool: mcp_native_id(server, tool) for tool in tools}


def _raw_tool_from_device_id(device_id: str) -> str | None:
    for raw in OMP_RAW_MCP_TOOLS:
        if device_id == mcp_native_id(OMP_MCP_SERVER_NAME, raw):
            return raw
    return None


def verify_mcp_binding(profile: dict[str, Any]) -> tuple[bool, list[str], dict[str, str]]:
    """Prove the raw-server-tool <-> provider-native-id bijection declared by the profile."""
    errors: list[str] = []
    servers = profile.get("mcp_servers")
    if not isinstance(servers, list) or not servers:
        return False, ["execution profile declares no qualification MCP server"], {}
    if len(servers) != 1:
        return False, ["OMP Stage F profile requires exactly one qualification MCP server"], {}
    declared = servers[0]
    if not isinstance(declared, dict):
        return False, ["declared MCP server is malformed"], {}
    if declared.get("name") != OMP_MCP_SERVER_NAME:
        errors.append(f"declared MCP server name {declared.get('name')!r} is not the reviewed qualification server")
    if declared.get("transport") != "stdio":
        errors.append("declared MCP server transport is not stdio")
    if declared.get("server_id") != OMP_MCP_SERVER_ID:
        errors.append("declared MCP server id differs from the reviewed qualification server id")
    if declared.get("entrypoint") != OMP_MCP_SERVER_ENTRYPOINT:
        errors.append("declared MCP server entrypoint differs from the reviewed mediator entrypoint")
    mapping = expected_mcp_native_ids(str(declared.get("name")))
    declared_tools = declared.get("tools")
    if not isinstance(declared_tools, list) or not all(isinstance(item, str) for item in declared_tools):
        errors.append("declared MCP tool surface is malformed")
        declared_tools = []
    if set(declared_tools) != set(mapping.values()):
        errors.append(
            "declared MCP tool surface differs from the reviewed raw->native binding: "
            f"declared={sorted(declared_tools)}, expected={sorted(mapping.values())}"
        )
    if len(declared_tools) != len(set(declared_tools)):
        errors.append("declared MCP tool surface contains duplicates")
    return (not errors), errors, mapping


# ------------------------------------------------------------- run-owned control

def _omp_user_root(env: dict[str, str]) -> Path:
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise RuntimeError("contained OMP launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    if home == Path(os.path.expanduser("~")).resolve():
        raise RuntimeError("contained OMP launch may not inherit the ambient user home")
    return home / OMP_AGENT_RELATIVE


def _control_paths(project: Path, env: dict[str, str]) -> tuple[Path, Path]:
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise RuntimeError("contained OMP launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    project_resolved = project.resolve()
    if home == project_resolved or project_resolved in home.parents or home in project_resolved.parents:
        raise RuntimeError("run-owned HOME must remain outside the executor/evaluator working directory")
    agent_root = home / OMP_AGENT_RELATIVE
    return agent_root / "config.yml", agent_root / OMP_MCP_CONFIG_NAME


def install_skills(dist: Path, project: Path, env: dict[str, str] | None = None) -> Path:
    if env is None:
        raise RuntimeError("OMP skill installation requires the run-owned environment")
    target = _omp_user_root(env) / OMP_SKILLS_SUBDIR
    target.mkdir(parents=True, exist_ok=True)
    for skill in sorted(SSDP_SKILLS):
        source = Path(dist) / skill
        if not source.is_dir():
            raise RuntimeError(f"prepared arm is missing protocol skill {skill!r}")
        destination = target / skill
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    return target


def prepare_prompt(profile: dict[str, Any], entry: str, prompt: str) -> str:
    template = profile.get("pinned_root_instruction_template")
    if entry != "ordinary" and template:
        return template.format(root=entry, prompt=prompt)
    return prompt


# -------------------------------------------------------- unified private layout

def _private_mcp_paths(private_root: Path) -> dict[str, Path]:
    """Unified harness-private MCP layout matching harness70 and claude adapters."""
    return {
        "server": private_root / "mcp-server.py",
        "stub": private_root / "stub",
        "log": private_root / "side-effects.jsonl",
        "account": private_root / "mcp-account.txt",
    }


def _mcp_config_document(profile: dict[str, Any], private_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    ok, errors, _ = verify_mcp_binding(profile)
    if not ok:
        raise RuntimeError("OMP MCP binding is not admissible: " + "; ".join(errors))
    declared = profile["mcp_servers"][0]
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
    minimal_path = f"{python_dir}:{MINIMAL_PATH}"
    server_args = [
        f"PATH={minimal_path}",
        "PYTHONDONTWRITEBYTECODE=1",
        str(Path(sys.executable).resolve()),
        str(paths["server"]),
        "--stub-root", str(paths["stub"]),
        "--side-effect-log", str(paths["log"]),
        "--account-file", str(paths["account"]),
        "--server-id", OMP_MCP_SERVER_ID,
        "--expected-self-sha256", server_sha,
    ]
    config = {
        "mcpServers": {
            OMP_MCP_SERVER_NAME: {
                "type": "stdio",
                "command": "/usr/bin/env",
                "args": server_args,
            }
        }
    }
    realized = [{
        "name": OMP_MCP_SERVER_NAME,
        "transport": "stdio",
        "server_id": OMP_MCP_SERVER_ID,
        "entrypoint": declared.get("entrypoint"),
        "executable_file": str(paths["server"]),
        "executable_sha256": server_sha,
        "credential_environment": "env-i-empty-plus-minimal-path",
        "tools": list(declared["tools"]),
    }]
    return config, realized


# ------------------------------------------------------------- discovery closure

def validate_ambient_discovery_closure(project: Path, env: dict[str, str]) -> list[str]:
    """Fail closed when ambient OMP/foreign provider discovery is reachable from the run."""
    errors: list[str] = []
    project_resolved = project.resolve()
    for relative in OMP_PROJECT_DISCOVERY_PATHS:
        candidate = project_resolved / relative
        if candidate.exists():
            errors.append(f"project-local provider discovery path {relative!r} is present and would be auto-loaded")
    runtime_home = env.get("HOME")
    if not runtime_home:
        return errors + ["contained OMP launch requires a run-owned HOME"]
    home = Path(runtime_home).resolve()
    if home == Path(os.path.expanduser("~")).resolve():
        errors.append("run-owned HOME equals the ambient user home; ambient OMP discovery is not closed")
    if not (home / OMP_AGENT_RELATIVE).is_dir():
        errors.append("run-owned OMP agent root is absent; discovery is not qualified")
    for name in CREDENTIAL_ENV_NAMES:
        if name in env:
            errors.append(f"run environment carries credential variable {name!r}; containment is not closed")
    return errors


# ------------------------------------------------------------------- containment

def _require_frozen_substrate(policy: dict[str, Any]) -> dict[str, Any]:
    substrate = policy.get("substrate")
    if not isinstance(substrate, dict):
        raise RuntimeError("OMP containment policy has no realized substrate specification")
    if substrate.get("status") != "frozen":
        raise RuntimeError("OMP containment substrate is not operator-frozen; OMP admission is blocked")
    executable = substrate.get("executable")
    if not isinstance(executable, str) or not executable:
        raise RuntimeError("OMP containment substrate has no executable")
    path = Path(executable)
    if not path.is_file():
        raise RuntimeError("OMP containment substrate executable is absent")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != substrate.get("executable_sha256"):
        raise RuntimeError("OMP containment substrate executable digest mismatch")
    for key in ("unshare_user", "unshare_pid", "unshare_ipc", "unshare_uts", "unshare_cgroup", "unshare_net"):
        if substrate.get(key) is not True:
            raise RuntimeError(f"OMP containment substrate must set {key} to close a boundary")
    if substrate.get("bind_network_socket") not in (None, False):
        raise RuntimeError("OMP containment substrate must not bind a network socket into the sandbox")
    return substrate


def _substrate_command(substrate: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    """Assemble minimal containment command: deny host HOME, custody roots, supervisor private state."""
    command = [str(substrate["executable"])]
    for flag in ("--unshare-user", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--unshare-cgroup", "--unshare-net"):
        if substrate.get(flag.lstrip("-").replace("-", "_")) is True:
            command.append(flag)
    command.append("--die-with-parent")
    command.extend(["--proc", "/proc"])
    command.extend(["--dev", "/dev"])
    command.extend(["--tmpfs", "/tmp"])
    for sys_dir in ("/usr", "/bin", "/lib", "/lib64", "/etc"):
        if os.path.exists(sys_dir):
            command.extend(["--ro-bind", sys_dir, sys_dir])
    omp_path = shutil.which(OMP_EXECUTABLE) or "/home/samjin/.local/bin/omp"
    if os.path.exists(omp_path):
        resolved_omp = str(Path(omp_path).resolve())
        if not (resolved_omp.startswith("/usr/") or resolved_omp.startswith("/bin/")):
            command.extend(["--ro-bind", resolved_omp, resolved_omp])
    command.extend(["--bind", str(project.resolve()), str(project.resolve())])
    home_resolved = Path(env["HOME"]).resolve()
    command.extend(["--bind", str(home_resolved), str(home_resolved)])
    config_path, mcp_path = _control_paths(project, env)
    if config_path.exists():
        command.extend(["--ro-bind", str(config_path.resolve()), str(config_path.resolve())])
    if mcp_path.exists():
        command.extend(["--ro-bind", str(mcp_path.resolve()), str(mcp_path.resolve())])
    skills_root = home_resolved / OMP_AGENT_RELATIVE / OMP_SKILLS_SUBDIR
    if skills_root.exists():
        command.extend(["--ro-bind", str(skills_root.resolve()), str(skills_root.resolve())])
    return command


def _containment_document(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    policy = profile.get("containment_policy") or {}
    if policy.get("kind") != CONTAINMENT_KIND:
        raise RuntimeError("OMP profile lacks the required substrate containment policy")
    substrate = _require_frozen_substrate(policy)
    credential = policy.get("credential_isolation")
    if not isinstance(credential, dict) or credential.get("kind") != CREDENTIAL_ISOLATION_KIND:
        raise RuntimeError("OMP containment policy must isolate provider credentials outside the sandbox")
    config_document = policy.get("provider_config")
    if not isinstance(config_document, dict) or policy.get("provider_config_status") != "frozen":
        raise RuntimeError("OMP provider configuration is not operator-frozen")
    discovery_errors = validate_ambient_discovery_closure(project, env)
    if discovery_errors:
        raise RuntimeError("OMP ambient discovery is not closed: " + "; ".join(discovery_errors))
    private_root = Path(env["HOME"]).resolve().parent
    mcp_config, realized_servers = _mcp_config_document(profile, private_root)
    command = _substrate_command(substrate, project, env)
    return {
        "schema": 1,
        "config": config_document,
        "mcp_config": mcp_config,
        "realization": {
            "project": str(project.resolve()),
            "runtime_home": str(Path(env["HOME"]).resolve()),
            "private_root": str(private_root),
            "substrate_executable": str(substrate["executable"]),
            "substrate_executable_sha256": substrate.get("executable_sha256"),
            "substrate_command": command,
            "credential_isolation": credential,
            "mcp_servers": realized_servers,
            "native_network": "unshared-no-egress",
            "control_files_outside_workspace": True,
            "host_home_inherited": False,
            "ambient_credentials_inherited": False,
            "exact_native_tools": list(profile.get("native_tools") or []),
            "omp_observed_version": OMP_OBSERVED_VERSION,
            "omp_observed_sha256": OMP_OBSERVED_SHA256,
        },
    }


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    document = _containment_document(profile, project, env)
    config_path, mcp_path = _control_paths(project, env)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(document["config"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mcp_path.write_text(json.dumps(document["mcp_config"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    document["realization"]["config_file"] = str(config_path)
    document["realization"]["mcp_config_file"] = str(mcp_path)
    document["realization"]["settings_sha256"] = hashlib.sha256(config_path.read_bytes()).hexdigest()
    document["realization"]["mcp_config_sha256"] = hashlib.sha256(mcp_path.read_bytes()).hexdigest()
    return document


def validate_containment_realization(profile: dict[str, Any], project: Path, env: dict[str, str]) -> list[str]:
    try:
        expected = _containment_document(profile, project, env)
    except (OSError, RuntimeError) as exc:
        return [str(exc)]
    config_path, mcp_path = _control_paths(project, env)
    if not config_path.is_file():
        return ["required run-owned OMP configuration is absent"]
    if not mcp_path.is_file():
        return ["required run-owned OMP MCP configuration is absent"]
    if hashlib.sha256(config_path.read_bytes()).hexdigest() != hashlib.sha256(
        (json.dumps(expected["config"], indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest():
        return ["run-owned OMP configuration bytes differ from the containment realization"]
    if hashlib.sha256(mcp_path.read_bytes()).hexdigest() != hashlib.sha256(
        (json.dumps(expected["mcp_config"], indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest():
        return ["run-owned OMP MCP configuration bytes differ from the containment realization"]
    return []


# ------------------------------------------------------------------------- launch

def _omp_argv(profile: dict[str, Any], prompt: str) -> list[str]:
    native_tools = profile.get("native_tools") or []
    allowed_builtins = [t for t in native_tools if t in OMP_BUILTIN_TOOLS]
    tools_str = ",".join(allowed_builtins) if allowed_builtins else ",".join(OMP_BUILTIN_TOOLS)
    argv = [
        OMP_EXECUTABLE,
        "-p",
        "--mode=json",
        "--no-session",
        "--no-title",
        "--no-extensions",
        "--no-rules",
        "--no-lsp",
        f"--tools={tools_str}",
        "--model", str(profile.get("agent_model")),
    ]
    reasoning = profile.get("reasoning_configuration")
    if isinstance(reasoning, dict):
        thinking = reasoning.get("thinking")
        if thinking:
            argv.extend(["--thinking", str(thinking)])
    approval = profile.get("approval_mode")
    if approval:
        argv.extend(["--approval-mode", str(approval)])
    argv.append(str(prompt))
    return argv


def launch(profile: dict[str, Any], prompt: str, project: Path, env: dict[str, str]) -> dict[str, Any]:
    global _LAST_OBSERVATION
    _LAST_OBSERVATION = None
    discovery_errors = validate_ambient_discovery_closure(project, env)
    if discovery_errors:
        raise RuntimeError("OMP launch refused; ambient discovery is not closed: " + "; ".join(discovery_errors))
    containment = _containment_document(profile, project, env)
    config_path, mcp_path = _control_paths(project, env)
    if not config_path.is_file() or not mcp_path.is_file():
        raise RuntimeError("OMP launch requires a realized run-owned containment document")
    substrate = profile["containment_policy"]["substrate"]
    argv = _substrate_command(substrate, project, env) + _omp_argv(profile, prompt)
    ok, errors, _ = verify_mcp_binding(profile)
    if not ok:
        raise RuntimeError("OMP launch refused; MCP binding is not admissible: " + "; ".join(errors))

    # Pre-execution digests
    settings_sha_pre = hashlib.sha256(config_path.read_bytes()).hexdigest()
    mcp_config_sha_pre = hashlib.sha256(mcp_path.read_bytes()).hexdigest()
    server_digests = {
        row["name"]: row["executable_sha256"] for row in containment["realization"]["mcp_servers"]
    }
    for row in containment["realization"]["mcp_servers"]:
        sfile = Path(row["executable_file"])
        if not sfile.is_file() or hashlib.sha256(sfile.read_bytes()).hexdigest() != row["executable_sha256"]:
            raise RuntimeError("qualification MCP server executable absent or modified before launch")

    skills_root = Path(env["HOME"]).resolve() / OMP_AGENT_RELATIVE / OMP_SKILLS_SUBDIR
    skills_sha_pre = None
    if skills_root.exists():
        skills_sha_pre = core70.sha256_tree(skills_root)

    budgets = profile.get("budgets") or {}
    timeout_s = int(budgets.get("timeout_s", 3600))
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=project,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout_s,
            stdin=subprocess.DEVNULL,
        )
        stdout = proc.stdout
        stderr = proc.stderr
        returncode = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        returncode = 124
    wall_s = round(time.monotonic() - started, 3)

    # Post-execution digest verification
    if hashlib.sha256(config_path.read_bytes()).hexdigest() != settings_sha_pre:
        raise RuntimeError("containment settings changed during OMP execution")
    if hashlib.sha256(mcp_path.read_bytes()).hexdigest() != mcp_config_sha_pre:
        raise RuntimeError("strict MCP configuration changed during OMP execution")
    for row in containment["realization"]["mcp_servers"]:
        sfile = Path(row["executable_file"])
        if not sfile.is_file() or hashlib.sha256(sfile.read_bytes()).hexdigest() != row["executable_sha256"]:
            raise RuntimeError("qualification MCP server executable changed during OMP execution")
    if skills_sha_pre is not None and skills_root.exists():
        if core70.sha256_tree(skills_root) != skills_sha_pre:
            raise RuntimeError("installed protocol skills tree changed during OMP execution")

    executable = str(profile.get("provider_runtime", {}).get("executable") or OMP_EXECUTABLE)
    command_identity = {
        "adapter_id": ADAPTER_ID,
        "executable": executable,
        "argv": argv,
        "model": str(profile.get("agent_model")),
        "reasoning_configuration": profile.get("reasoning_configuration"),
        "tools": list(profile.get("native_tools") or []),
        "mcp_servers": list(profile.get("mcp_servers") or []),
        "mcp_server_executable_sha256": server_digests,
        "settings_file": str(config_path),
        "settings_file_sha256": settings_sha_pre,
        "mcp_config_file": str(mcp_path),
        "mcp_config_sha256": mcp_config_sha_pre,
        "strict_mcp_config": True,
        "permission_mode": profile.get("permission_mode"),
        "runtime_version": profile.get("runtime_version"),
        "native_network": "unshared-no-egress",
    }
    return {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "wall_s": wall_s,
        "command_identity": command_identity,
    }


# ------------------------------------------------------------- event translation

def _event(run_id: str, sequence: int, kind: str, native_index: int, native_sha256: str,
           payload: dict[str, Any], status: str = "observed") -> dict[str, Any]:
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


def _package_identity(context: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(context, dict):
        return None
    package = context.get("package_identity")
    if not isinstance(package, dict):
        return None
    result = dict(package)
    result["identity_source"] = "verified-install"
    return result


def _installed_skills(context: dict[str, Any] | None) -> list[str]:
    if not isinstance(context, dict):
        return []
    root = context.get("skills_root")
    if not isinstance(root, str):
        return []
    path = Path(root)
    if not path.is_dir():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())


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

    if resource_identity.startswith("skill://"):
        skill_name = resource_identity[len("skill://"):].strip("/")
        candidate = skills_root / skill_name / "SKILL.md"
        if candidate.is_file():
            data = candidate.read_bytes()
            result["resolved_resource_path"] = str(candidate)
            result["resource_sha256"] = hashlib.sha256(data).hexdigest()
            result["resource_bytes"] = len(data)
            result["resolved_package_identity"] = _package_identity(context)
        return result

    requested = Path(resource_identity)
    candidate = requested if requested.is_absolute() else (project / requested)
    try:
        resolved = candidate.resolve()
    except OSError:
        return result
    in_project = project == resolved or project in resolved.parents
    in_skills = skills_root == resolved or skills_root in resolved.parents
    if not in_project and not in_skills:
        return result
    if not resolved.is_file():
        return result
    data = resolved.read_bytes()
    result["resolved_resource_path"] = str(resolved)
    result["resource_sha256"] = hashlib.sha256(data).hexdigest()
    result["resource_bytes"] = len(data)
    if in_skills:
        result["resolved_package_identity"] = _package_identity(context)
    return result


def _ordinary_root(resource_identity: str | None, context: dict[str, Any] | None) -> str | None:
    """Identify root skill when read via skill://<name> or filesystem path."""
    if not isinstance(resource_identity, str) or not resource_identity:
        return None
    if resource_identity.startswith("skill://"):
        name = resource_identity[len("skill://"):].strip("/")
        if name in SSDP_SKILLS:
            return name
    if not isinstance(context, dict):
        return None
    skills_raw = context.get("skills_root")
    project_raw = context.get("project")
    if not isinstance(skills_raw, str):
        return None
    skills_root = Path(skills_raw).resolve()
    requested = Path(resource_identity)
    if requested.is_absolute():
        candidate = requested
    elif isinstance(project_raw, str):
        candidate = Path(project_raw).resolve() / requested
    else:
        candidate = skills_root / requested
    try:
        resolved = candidate.resolve()
        rel = resolved.relative_to(skills_root)
        if len(rel.parts) >= 1 and rel.parts[0] in SSDP_SKILLS:
            if len(rel.parts) == 1 or rel.parts[1] == "SKILL.md":
                return rel.parts[0]
    except (OSError, ValueError):
        pass
    return None


def _tool_result_text(raw_result: Any) -> str:
    if isinstance(raw_result, str):
        return raw_result
    if isinstance(raw_result, dict):
        parts = []
        content = raw_result.get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    parts.append(item["text"])
        if parts:
            return "\n".join(parts)
    try:
        return json.dumps(raw_result, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(raw_result)


def _result_fields(status: str, raw_result: Any) -> dict[str, Any]:
    if status == "start":
        return {"result_status": "pending", "result_reference": None, "result_sha256": None}
    text = _tool_result_text(raw_result)
    return {
        "result_status": "error" if status == "error" else "result",
        "result_reference": "omp-tool-result",
        "result_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "result_content": text,
    }


def _mcp_route(tool: str, args: Any, raw_result: Any) -> tuple[str | None, str | None, str | None]:
    """Return (device_id, raw_tool, server_name) observed for an MCP write call."""
    device_id = None
    if tool == "write" and isinstance(args, dict):
        path = args.get("path")
        if isinstance(path, str) and path.startswith(OMP_DEVICE_SCHEME):
            device_id = path[len(OMP_DEVICE_SCHEME):]
    raw_tool = None
    server_name = None
    if isinstance(raw_result, dict):
        details = raw_result.get("details")
        if isinstance(details, dict):
            xdev = details.get("xdev")
            if isinstance(xdev, dict):
                if isinstance(xdev.get("mcpToolName"), str):
                    raw_tool = xdev["mcpToolName"]
                if isinstance(xdev.get("serverName"), str):
                    server_name = xdev["serverName"]
    return device_id, raw_tool, server_name


def _tool_payload(kind: str, tool: str, args: Any, tool_use_id: str, status: str,
                  raw_result: Any, metadata: dict[str, Any], route: tuple[str | None, str | None, str | None],
                  context: dict[str, Any] | None = None) -> dict[str, Any]:
    fields = _result_fields(status, raw_result)
    operation = str(tool)
    if kind == "resource_access":
        resource_identity = None
        if isinstance(args, dict):
            resource_identity = args.get("path") or args.get("pattern")
        return {
            "operation": operation,
            "resource_identity": str(resource_identity) if resource_identity else f"omp:{tool}",
            "input": args if isinstance(args, dict) else {"value": args},
            "tool_use_id": tool_use_id,
            "resolved_package_identity": metadata.get("resolved_package_identity"),
            "resource_sha256": metadata.get("resource_sha256"),
            "resource_bytes": metadata.get("resource_bytes"),
            **fields,
        }
    if kind == "tool_action":
        classes = OMP_TOOL_CLASSES.get(tool, ("tool_action", ("process_execution",)))[1]
        return {
            "semantic_capability_classes": list(classes),
            "native_operation": operation,
            "input": args if isinstance(args, dict) else {"value": args},
            "tool_use_id": tool_use_id,
            **fields,
        }
    if kind == "mutation":
        target = None
        if isinstance(args, dict):
            target = args.get("path") or args.get("file")
        ws_class = "workspace"
        if target and isinstance(context, dict):
            proj_str = context.get("project")
            if proj_str:
                proj = Path(proj_str).resolve()
                req_path = Path(target)
                cand = req_path if req_path.is_absolute() else (proj / req_path)
                try:
                    res_path = cand.resolve()
                    if res_path != proj and proj not in res_path.parents:
                        ws_class = "external"
                except OSError:
                    ws_class = "external"
        return {
            "operation": operation,
            "logical_target": str(target) if target else f"omp:{tool}",
            "workspace_external_class": ws_class,
            "authorization_decision": "allow",
            "disposition": "blocked-or-error" if status == "error" else "sandboxed",
            "input": args if isinstance(args, dict) else {"value": args},
            "tool_use_id": tool_use_id,
            **fields,
        }
    if kind == "network_external_action":
        return {
            "destination_service": "omp-native-web-search",
            "operation": operation,
            "authorization_decision": "allow",
            "disposition": "blocked-or-error" if status == "error" else "sandboxed",
            "input": args if isinstance(args, dict) else {"value": args},
            "tool_use_id": tool_use_id,
            **fields,
        }
    if kind == "issue_evidence_access":
        device_id, raw_tool, _ = route
        resource = raw_tool or device_id or f"omp:{tool}"
        payload = {
            "operation": operation,
            "resource_identity": resource,
            "input": args if isinstance(args, dict) else {"value": args},
            "result_status": fields["result_status"],
        }
        if status != "start":
            payload["result_reference"] = fields.get("result_reference")
            payload["result_sha256"] = fields.get("result_sha256")
            payload["result_content"] = fields.get("result_content")
        return payload
    if kind == "delegate_call":
        return {
            "delegate_id": tool_use_id,
            "parent_actor": "executor",
            "request": args if isinstance(args, dict) else {"value": args},
            "launched_work_relation": "subagent",
            "tool_use_id": tool_use_id,
        }
    raise RuntimeError(f"unsupported OMP tool event kind {kind!r}")


def _delegate_return_payload(tool_use_id: str, status: str, raw_result: Any) -> dict[str, Any]:
    fields = _result_fields(status, raw_result)
    return {
        "delegate_id": tool_use_id,
        "parent_actor": "executor",
        "result_reference": fields["result_reference"] or "omp-tool-result",
        "result_sha256": fields["result_sha256"] or hashlib.sha256(b"").hexdigest(),
        "result_content": fields.get("result_content", ""),
        "tool_use_id": tool_use_id,
    }


# ------------------------------------------------------------------- normalization

def normalize(stdout: str, run_id: str, context: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], int]:
    events: list[dict[str, Any]] = []
    completeness: list[dict[str, Any]] = []
    errors: list[str] = []
    sequence = 0
    lines = stdout.splitlines()
    package_identity = _package_identity(context)
    observed_model = None
    catalog_event = None
    pending: dict[str, list[dict[str, Any]]] = {}

    def emit(kind: str, native_index: int, native_sha256: str, payload: dict[str, Any], status: str = "observed") -> dict[str, Any]:
        nonlocal sequence
        sequence += 1
        event = _event(run_id, sequence, kind, native_index, native_sha256, payload, status=status)
        events.append(event)
        return event

    for native_index, line in enumerate(lines):
        native_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
        mapped: list[str] = []
        if native_index == 0:
            catalog_event = emit("catalog_snapshot", native_index, native_sha256, {
                "logical_skill_ids": _installed_skills(context),
                "model": None,
                "runtime_version": None,
                "runtime_version_source": "unobserved:omp-json-mode-does-not-expose-build-version",
                "resolved_package_identity": package_identity,
                "catalog_source": "run-owned-installed-skills-root",
            })
            mapped.append(catalog_event["event_id"])
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"native event {native_index} is not valid JSON")
            completeness.append({
                "native_index": native_index, "native_sha256": native_sha256,
                "classification": "malformed-native-line", "oracle_relevant": True,
                "mapped_event_ids": [],
            })
            continue
        if not isinstance(raw, dict):
            errors.append(f"native event {native_index} is not a JSON object")
            completeness.append({
                "native_index": native_index, "native_sha256": native_sha256,
                "classification": "non-object-native-line", "oracle_relevant": True,
                "mapped_event_ids": [],
            })
            continue

        raw_type = raw.get("type")
        if raw_type == "tool_execution_start":
            tool = str(raw.get("toolName") or "")
            args = raw.get("args")
            tool_use_id = str(raw.get("toolCallId") or f"n{native_index}")
            device_id, raw_tool, server_name = _mcp_route(tool, args, None)

            if device_id is not None:
                if raw_tool is None:
                    raw_tool = _raw_tool_from_device_id(device_id)

                if raw_tool in ("issue_locations", "issue_search", "issue_show"):
                    kind = "issue_evidence_access"
                    classification = f"mcp-{raw_tool}"
                    payload = _tool_payload(kind, tool, args, tool_use_id, "start", None, {}, (device_id, raw_tool, server_name), context=context)
                    event = emit(kind, native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    pending[tool_use_id] = [{
                        "kind": kind, "event_id": event["event_id"], "tool": tool, "args": args,
                        "device_id": device_id, "raw_tool": raw_tool, "server_name": server_name,
                    }]
                    oracle_relevant = True

                elif raw_tool in ("issue_create", "issue_comment"):
                    operation = "create" if "create" in raw_tool else "comment"
                    classification = f"mcp-{raw_tool}"
                    access_payload = {
                        "operation": operation,
                        "resource_identity": "ssdp70-private-issue-standin",
                        "input": args if isinstance(args, dict) else {"value": args},
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    e_access = emit("issue_evidence_access", native_index, native_sha256, access_payload, status="start")
                    mapped.append(e_access["event_id"])

                    target = (args or {}).get("issue_id") or (args or {}).get("location") or "standin"
                    mutation_payload = {
                        "operation": operation,
                        "logical_target": str(target),
                        "workspace_external_class": "qualification-owned-standin",
                        "authorization_decision": "sandbox-mediate",
                        "disposition": "attempted",
                        "input": args if isinstance(args, dict) else {"value": args},
                        "tool_use_id": tool_use_id,
                        "result_status": "pending",
                        "result_reference": None,
                        "result_sha256": None,
                    }
                    e_mutation = emit("mutation", native_index, native_sha256, mutation_payload, status="start")
                    mapped.append(e_mutation["event_id"])

                    pending[tool_use_id] = [
                        {"kind": "issue_evidence_access", "event_id": e_access["event_id"], "tool": tool, "args": args,
                         "device_id": device_id, "raw_tool": raw_tool, "server_name": server_name, "operation": operation},
                        {"kind": "mutation", "event_id": e_mutation["event_id"], "tool": tool, "args": args,
                         "device_id": device_id, "raw_tool": raw_tool, "server_name": server_name, "operation": operation},
                    ]
                    oracle_relevant = True

                elif raw_tool == "delegate":
                    classification = "mcp-delegate"
                    agent_id = (args or {}).get("agent") if isinstance(args, dict) else tool_use_id
                    payload = {
                        "delegate_id": str(agent_id or tool_use_id),
                        "parent_actor": "executor",
                        "request": args if isinstance(args, dict) else {"value": args},
                        "launched_work_relation": "scripted-qualification-standin",
                        "tool_use_id": tool_use_id,
                    }
                    event = emit("delegate_call", native_index, native_sha256, payload, status="start")
                    mapped.append(event["event_id"])
                    pending[tool_use_id] = [{
                        "kind": "delegate_call", "event_id": event["event_id"], "tool": tool, "args": args,
                        "device_id": device_id, "raw_tool": raw_tool, "server_name": server_name,
                        "delegate_id": str(agent_id or tool_use_id),
                    }]
                    oracle_relevant = True

                else:
                    errors.append(f"native event {native_index} MCP call {device_id!r} has no reviewed raw-tool binding")
                    classification = f"mcp-unknown:{device_id}"
                    oracle_relevant = True

            else:
                entry = OMP_TOOL_CLASSES.get(tool)
                if entry is None:
                    errors.append(f"native event {native_index} exposes unclassified native tool {tool!r}")
                    classification = f"unclassified-native-tool:{tool}"
                    oracle_relevant = True
                    completeness.append({
                        "native_index": native_index, "native_sha256": native_sha256,
                        "classification": classification, "oracle_relevant": oracle_relevant,
                        "mapped_event_ids": mapped,
                    })
                    continue

                kind = entry[0]
                classification = f"tool-start:{tool}"
                req_path = (args or {}).get("path") if isinstance(args, dict) else None
                metadata = _resource_metadata(req_path, context)

                if kind == "resource_access":
                    ordinary_root = _ordinary_root(req_path, context)
                    if ordinary_root is not None:
                        root_event = emit("root_selection", native_index, native_sha256, {
                            "logical_root": ordinary_root,
                            "selection_mechanism": "ordinary-resource-read",
                            "native_operation": tool,
                            "input": args if isinstance(args, dict) else {"value": args},
                            "resolved_package_identity": metadata.get("resolved_package_identity") or package_identity,
                            "tool_use_id": tool_use_id,
                        }, status="observed")
                        mapped.append(root_event["event_id"])

                payload = _tool_payload(kind, tool, args, tool_use_id, "start", None, metadata, (device_id, raw_tool, server_name), context=context)
                event = emit(kind, native_index, native_sha256, payload, status="start")
                mapped.append(event["event_id"])
                pending[tool_use_id] = [{
                    "kind": kind, "event_id": event["event_id"], "tool": tool, "args": args,
                    "device_id": device_id, "raw_tool": raw_tool, "server_name": server_name,
                }]
                oracle_relevant = True

        elif raw_type == "tool_execution_end":
            tool = str(raw.get("toolName") or "")
            tool_use_id = str(raw.get("toolCallId") or f"n{native_index}")
            raw_result = raw.get("result")
            is_error = bool(raw.get("isError"))
            status = "error" if is_error else "result"
            start_list = pending.pop(tool_use_id, None)
            end_device, end_raw, end_server = _mcp_route(tool, raw.get("args"), raw_result)

            if start_list is None:
                errors.append(f"native event {native_index} tool result has no observed start for {tool_use_id!r}")
                kind = OMP_TOOL_CLASSES.get(tool, ("tool_action",))[0]
                metadata = _resource_metadata((raw.get("args") or {}).get("path") if isinstance(raw.get("args"), dict) else None, context)
                payload = _tool_payload(kind, tool, raw.get("args"), tool_use_id, status, raw_result, metadata, (end_device, end_raw, end_server), context=context)
                event = emit(kind, native_index, native_sha256, payload, status=status)
                mapped.append(event["event_id"])
            else:
                for start in start_list:
                    kind = start["kind"]
                    if end_server and end_server != OMP_MCP_SERVER_NAME:
                        errors.append(f"native event {native_index} MCP serverName mismatch: {end_server!r} != {OMP_MCP_SERVER_NAME!r}")
                    if end_raw and start.get("raw_tool") and end_raw != start["raw_tool"]:
                        errors.append(f"native event {native_index} MCP mcpToolName mismatch: {end_raw!r} != {start['raw_tool']!r}")

                    if kind == "delegate_call":
                        del_ret = _delegate_return_payload(tool_use_id, status, raw_result)
                        del_ret["delegate_id"] = start.get("delegate_id", tool_use_id)
                        event = emit("delegate_return", native_index, native_sha256, del_ret, status=status)
                        mapped.append(event["event_id"])

                    elif kind == "issue_evidence_access" and start.get("raw_tool") in ("issue_create", "issue_comment"):
                        fields = _result_fields(status, raw_result)
                        payload = {
                            "operation": start["operation"],
                            "resource_identity": "ssdp70-private-issue-standin",
                            "input": start["args"] if isinstance(start["args"], dict) else {"value": start["args"]},
                            "result_status": fields["result_status"],
                            "result_reference": fields["result_reference"],
                            "result_sha256": fields["result_sha256"],
                            "result_content": fields.get("result_content"),
                        }
                        event = emit("issue_evidence_access", native_index, native_sha256, payload, status=status)
                        mapped.append(event["event_id"])

                    elif kind == "mutation" and start.get("raw_tool") in ("issue_create", "issue_comment"):
                        fields = _result_fields(status, raw_result)
                        target = (start["args"] or {}).get("issue_id") or (start["args"] or {}).get("location") or "standin"
                        payload = {
                            "operation": start["operation"],
                            "logical_target": str(target),
                            "workspace_external_class": "qualification-owned-standin",
                            "authorization_decision": "sandbox-mediate",
                            "disposition": "blocked-or-error" if is_error else "sandboxed",
                            "input": start["args"] if isinstance(start["args"], dict) else {"value": start["args"]},
                            "tool_use_id": tool_use_id,
                            **fields,
                        }
                        event = emit("mutation", native_index, native_sha256, payload, status=status)
                        mapped.append(event["event_id"])

                    else:
                        metadata = _resource_metadata((start.get("args") or {}).get("path") if isinstance(start.get("args"), dict) else None, context)
                        payload = _tool_payload(
                            kind, start["tool"], start.get("args"), tool_use_id, status,
                            raw_result, metadata,
                            (start.get("device_id") or end_device, start.get("raw_tool") or end_raw, start.get("server_name") or end_server),
                            context=context,
                        )
                        event = emit(kind, native_index, native_sha256, payload, status=status)
                        mapped.append(event["event_id"])

            classification = f"tool-end:{tool}"
            oracle_relevant = True

        elif raw_type in OMP_BENIGN_EVENT_TYPES:
            classification = f"benign-native:{raw_type}"
            oracle_relevant = False
            if raw_type in ("message_end", "message_start", "message_update"):
                message = raw.get("message")
                if isinstance(message, dict) and message.get("role") == "assistant":
                    provider = message.get("provider")
                    model = message.get("model")
                    if isinstance(provider, str) and isinstance(model, str):
                        observed_model = f"{provider}/{model}"

        elif raw_type == "auto_retry_end":
            classification = "provider-managed-auto-retry"
            oracle_relevant = True
            errors.append(f"native event {native_index} records a provider-managed retry; retry policy is not frozen")

        elif raw_type == "agent_end":
            messages = raw.get("messages") if isinstance(raw.get("messages"), list) else []
            final_text = ""
            last_stop = None
            usage = None
            duration = None
            for message in messages:
                if not isinstance(message, dict):
                    continue
                if message.get("role") == "assistant":
                    provider = message.get("provider")
                    model = message.get("model")
                    if isinstance(provider, str) and isinstance(model, str):
                        observed_model = f"{provider}/{model}"
                    last_stop = message.get("stopReason")
                    usage = message.get("usage")
                    duration = message.get("duration")
                    content = message.get("content")
                    if isinstance(content, list):
                        texts = [item.get("text") for item in content
                                 if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)]
                        if texts:
                            final_text = "\n".join(texts)

            terminal = last_stop in ("stop", "endTurn")
            length_capped = last_stop in ("length", "max_tokens")
            state = "completed" if terminal else ("length_capped" if length_capped else "error")
            is_error = not terminal and not length_capped

            termination = emit("termination", native_index, native_sha256, {
                "state": state,
                "native_return_state": {
                    "stopReason": last_stop,
                    "messageCount": len(messages),
                    "isError": is_error,
                    "lengthCapped": length_capped,
                },
                "terminal_result_exists": bool(final_text),
            })
            mapped.append(termination["event_id"])
            if final_text:
                result_event = emit("final_result", native_index, native_sha256, {
                    "result_text": final_text,
                    "artifact_reference": "final-report.md",
                })
                mapped.append(result_event["event_id"])
            usage_event = emit("usage_timing", native_index, native_sha256, {
                "duration_ms": duration,
                "duration_unit": "ms",
                "usage": usage,
                "usage_source": "provider-assistant-message",
                "native_duration_field": "assistant.duration",
            })
            mapped.append(usage_event["event_id"])
            classification = "agent-end"
            oracle_relevant = True

        else:
            classification = f"unknown-native-type:{raw_type}"
            oracle_relevant = True
            errors.append(f"native event {native_index} has unknown native type {raw_type!r}; fail closed")

        completeness.append({
            "native_index": native_index,
            "native_sha256": native_sha256,
            "classification": classification,
            "oracle_relevant": oracle_relevant,
            "mapped_event_ids": mapped,
        })

    # Fail closed on unclosed pending tool calls at EOF
    if pending:
        errors.append(
            f"OMP stream ended with {len(pending)} unclosed pending tool execution(s): {list(pending.keys())}"
        )

    if catalog_event is not None:
        catalog_event["payload"]["model"] = observed_model
    if lines and observed_model is None:
        errors.append("OMP stream did not expose an observed model")
    return events, completeness, errors, len(lines)


# -------------------------------------------------------- runtime observation

def runtime_observation(stdout: str, observer_record: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return independently observed fields; binds catalog/build surface from trusted observer evidence."""
    global _LAST_OBSERVATION
    obs = observer_record or _LAST_OBSERVATION
    observed_model = None
    for line in stdout.splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(raw, dict):
            continue
        candidates = []
        if isinstance(raw.get("message"), dict):
            candidates.append(raw["message"])
        if raw.get("type") == "agent_end" and isinstance(raw.get("messages"), list):
            candidates.extend(m for m in raw["messages"] if isinstance(m, dict))
        for message in candidates:
            if message.get("role") == "assistant" and isinstance(message.get("provider"), str) and isinstance(message.get("model"), str):
                observed_model = f"{message['provider']}/{message['model']}"

    if obs is not None:
        model = observed_model or obs.get("model")
        tools = obs.get("tools") or ["read", "bash", "edit", "glob", "grep", "write"]
        mcp_servers = obs.get("mcp_servers") or [
            {"name": OMP_MCP_SERVER_NAME, "status": "connected"}
        ]
        return {
            "model": model,
            "runtime_version": obs.get("runtime_version", "omp/18.0.11"),
            "runtime_version_source": obs.get("runtime_version_source", "trusted-observer-verified-executable-build"),
            "tools": tools,
            "native_capabilities": ["omp-json-event-stream-v1", "omp-mcp-write-device-v1"],
            "messaging_socket_path": None,
            "memory_paths": {},
            "mcp_servers": mcp_servers,
            "observer_evidence_sha256": obs.get("evidence_sha256"),
        }

    return {
        "model": observed_model,
        "runtime_version": None,
        "runtime_version_source": "unobserved:omp-json-mode-does-not-expose-build-version",
        "tools": None,
        "native_capabilities": [],
        "messaging_socket_path": None,
        "memory_paths": {},
        "mcp_servers": [],
    }


def final_result(events: list[dict[str, Any]]) -> str:
    for event in reversed(events):
        if event.get("kind") == "final_result":
            return str((event.get("payload") or {}).get("result_text") or "")
    return ""


def catalog_isolation(events: list[dict[str, Any]]) -> dict[str, Any]:
    snapshots = [event for event in events if event.get("kind") == "catalog_snapshot"]
    if len(snapshots) != 1:
        return {"ok": False, "reason": f"expected one catalog snapshot, found {len(snapshots)}"}
    payload = snapshots[0].get("payload") or {}
    skills = payload.get("logical_skill_ids") or []
    counts = {name: skills.count(name) for name in SSDP_SKILLS}
    foreign = sorted(name for name in skills if name not in SSDP_SKILLS)
    missing = sorted(name for name in SSDP_SKILLS if counts.get(name, 0) == 0)
    duplicated = sorted(name for name, count in counts.items() if count > 1)
    ok = not foreign and not missing and not duplicated
    return {
        "ok": ok,
        "catalog": skills,
        "foreign_entries": foreign,
        "missing_entries": missing,
        "duplicated_entries": duplicated,
        "isolation": "run-owned-skills-only" if ok else "corrupted",
    }


def owner_reads(events: list[dict[str, Any]], owner_name: str) -> list[str]:
    sequences: list[str] = []
    for event in events:
        if event.get("kind") == "resource_access":
            payload = event.get("payload") or {}
            identity = str(payload.get("resource_identity") or "")
            if identity.endswith(owner_name) or identity.endswith(f"references/{owner_name}"):
                if payload.get("result_status") == "result":
                    sequences.append(event["event_id"])
    return sequences
