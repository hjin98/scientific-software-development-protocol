#!/usr/bin/env python3
"""Dedicated read-only evaluator adapter for Oh My Pi (omp) under Protocol 7 Stage F.

Governing SSDP: 6.6.0. Target protocol: 7.0.0.
Authority:
- Stage 7 OMP Semantic Admission Roadmap (STAGE-7-OMP-SEMANTIC-ADMISSION-ROLE-HANDOFFS-2026-10-03.md §4)
- Ruling R1 (STAGE-7-OMP-SEMANTIC-ADMISSION-CLOSURE-MAP-AND-BLOCKED-HANDOFF-2026-10-03.md §3):
  Dedicated read-only evaluator adapter without modifying adapters/omp.py.
- Qualification contract PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md §§1, 6.
- Stakeholder Decision 2026-10-04 (Condition C1).

Key Constraints:
1. Tool surface is strictly constrained to read-only tools: ("read", "glob", "grep").
2. No MCP server tools (mcp_servers is empty).
3. Candidate evidence bundle is mounted strictly read-only (--ro-bind) into /workspace.
4. Native stream is translated to include {"type":"result", "result": ...} consumed by assess70.result_text.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

# Import shared mechanics from core70 and adapters.omp without altering omp.py
EVAL_DIR = Path(__file__).resolve().parent.parent
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))
import core70  # noqa: E402
import seccomp70  # noqa: E402
from adapters import omp  # noqa: E402

ADAPTER_ID = "omp-eval-json-v1"
CONTAINMENT_KIND = "omp-three-principal-bwrap-v3"
EVALUATOR_TOOLS = ("read", "glob", "grep")

SB_PROJECT = "/workspace"
SB_HOME = "/home/agent"
SB_CTL = "/opt/ssdp/ctl"
SB_OMP = "/opt/omp/omp"
SB_TMP = "/tmp"

OBSERVER_HOME = "/home/observer"
OBSERVER_CODE = "/opt/ssdp/observer"
OBSERVER_ARGUMENT_TARGET = 7
OBSERVER_CHANNEL_TARGETS = (3, 4, 5, 6)
RELAY_PORTS = {"inference": 49152}

CONTROL_FILES_IN_HOME = (
    ".omp/agent/config.yml",
    ".omp/agent/models.yml",
    ".omp/agent/mcp.json",
)


class EvaluatorAdapterError(Exception):
    """Failure inside the evaluator adapter."""


class EvaluatorPrelaunchRefusal(EvaluatorAdapterError):
    """The evaluator adapter refused before starting processes."""


def clean_env() -> dict[str, str]:
    """Scrubbed environment for evaluator execution. Ambient credentials denied."""
    return {"PATH": omp.MINIMAL_PATH, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def eval_profile_errors(profile: dict[str, Any]) -> list[str]:
    """Validate evaluator profile invariants."""
    errors: list[str] = []
    if profile.get("adapter_id") != ADAPTER_ID:
        errors.append(f"profile adapter_id {profile.get('adapter_id')!r} != {ADAPTER_ID!r}")
    tools = profile.get("native_tools")
    if tools != list(EVALUATOR_TOOLS):
        errors.append(f"evaluator profile native_tools must be exactly {list(EVALUATOR_TOOLS)!r}, got {tools!r}")
    mcp_servers = profile.get("mcp_servers")
    if mcp_servers != []:
        errors.append(f"evaluator profile mcp_servers must be empty [], got {mcp_servers!r}")
    ws = profile.get("workspace_realization")
    if not isinstance(ws, dict) or ws.get("kind") != "temporary-read-only-evidence-bundle":
        errors.append("evaluator workspace_realization.kind must be 'temporary-read-only-evidence-bundle'")
    inst = profile.get("install_mechanism")
    if inst != "none":
        errors.append("evaluator install_mechanism must be 'none'")
    return errors


def _eval_paths(project: Path, env: dict[str, str]) -> dict[str, Path]:
    runtime_home = env.get("HOME")
    if not runtime_home:
        raise EvaluatorAdapterError("contained evaluator launch requires a run-owned HOME")
    home = Path(runtime_home).resolve()
    if home == Path(os.path.expanduser("~")).resolve():
        raise EvaluatorAdapterError("contained evaluator launch may not inherit the ambient user home")
    private = home.parent
    project_resolved = project.resolve()
    if home == project_resolved or project_resolved in home.parents or home in project_resolved.parents:
        raise EvaluatorAdapterError("run-owned HOME must remain outside the evaluator working directory")
    if private == project_resolved or private in project_resolved.parents:
        raise EvaluatorAdapterError("harness-private root may not contain the evaluator working directory")
    return {
        "private": private,
        "home": home,
        "project": project_resolved,
        "control": private / "omp-control",
        "etc": private / "omp-etc",
        "observer_etc": private / "omp-observer-etc",
        "observer": private / "omp-observer-runtime",
        "subject_runtime": private / "omp-runtime-subject",
        "observer_runtime": private / "omp-runtime-observer",
        "agent": home / ".omp" / "agent",
    }


def eval_models_document(profile: dict[str, Any]) -> dict[str, Any]:
    route = profile["containment_policy"]["provider_route"]
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


def eval_mcp_document() -> dict[str, Any]:
    """Empty MCP configuration for evaluator profile."""
    return {"mcpServers": {}}


def eval_control_documents(profile: dict[str, Any]) -> dict[str, bytes]:
    settings = omp.settings_document()
    settings["skills"] = {"customDirectories": []}
    return {
        ".omp/agent/config.yml": omp._yaml(settings),
        ".omp/agent/models.yml": omp._yaml(eval_models_document(profile)),
        ".omp/agent/mcp.json": omp._json_bytes(eval_mcp_document()),
    }


def _write_eval_control_tree(paths: dict[str, Path], profile: dict[str, Any]) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "home_control": {},
        "control_dir": {},
        "etc": {},
        "observer_code": {},
        "observer_etc": {},
    }
    docs = eval_control_documents(profile)
    for rel, data in docs.items():
        target = paths["home"] / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o444)
        manifest["home_control"][rel] = omp.sha256_bytes(data)

    control = paths["control"]
    if control.exists():
        shutil.rmtree(control)
    control.mkdir(parents=True)
    for name in ("subject_launcher.py", "evidence70.py", "muxhttp70.py"):
        shutil.copy2(EVAL_DIR / name, control / name)
        (control / name).chmod(0o444)
        manifest["control_dir"][name] = omp.sha256_file(control / name)

    etc = paths["etc"]
    if etc.exists():
        shutil.rmtree(etc)
    etc.mkdir(parents=True)
    for name, data in omp.etc_documents().items():
        (etc / name).write_bytes(data)
        manifest["etc"][name] = omp.sha256_bytes(data)

    observer = paths["observer"]
    if observer.exists():
        shutil.rmtree(observer)
    observer.mkdir(parents=True)
    for name in ("observer70.py", "evidence70.py", "muxhttp70.py", "seccomp70.py"):
        shutil.copy2(EVAL_DIR / name, observer / name)
        (observer / name).chmod(0o444)
        manifest["observer_code"][name] = omp.sha256_file(observer / name)

    observer_etc = paths["observer_etc"]
    if observer_etc.exists():
        shutil.rmtree(observer_etc)
    observer_etc.mkdir(parents=True)
    manifest["runtime_surface"] = omp._materialize_runtime_dependencies(paths)
    for name, data in omp._observer_etc_documents(paths).items():
        target = observer_etc / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest["observer_etc"][name] = omp.sha256_bytes(data)

    return manifest


def realize_containment(profile: dict[str, Any], project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Create and bind evaluator containment. Mounts candidate bundle read-only."""
    problems = eval_profile_errors(profile)
    if problems:
        raise EvaluatorAdapterError("evaluator profile is not admissible: " + "; ".join(problems))
    dep_errors = omp.runtime_dependency_errors(profile)
    if dep_errors:
        raise EvaluatorAdapterError("runtime dependency surface is inadmissible: " + "; ".join(dep_errors))

    paths = _eval_paths(project, env)
    policy = profile["containment_policy"]
    substrate = Path(policy["substrate"]["executable"])
    if not substrate.is_file() or omp.sha256_file(substrate) != policy["substrate"]["executable_sha256"]:
        raise EvaluatorAdapterError("containment substrate executable digest mismatch")

    discovery = omp.validate_ambient_discovery_closure(project, env)
    if discovery:
        raise EvaluatorPrelaunchRefusal("ambient discovery is not closed: " + "; ".join(discovery))

    manifest = _write_eval_control_tree(paths, profile)
    staged_errors = omp._verify_staged_runtime_dependencies(paths)
    if staged_errors:
        raise EvaluatorAdapterError("staged runtime closure is inadmissible: " + "; ".join(staged_errors))

    mcp_sha = manifest["home_control"][".omp/agent/mcp.json"]
    settings_sha = manifest["home_control"][".omp/agent/config.yml"]
    models_sha = manifest["home_control"][".omp/agent/models.yml"]

    return {
        "schema": 2,
        "kind": CONTAINMENT_KIND,
        "realization": {
            "principals": ["qualification-supervisor", "provider-control-observer", "evaluator-subject"],
            "project": str(paths["project"]),
            "runtime_home": str(paths["home"]),
            "private_root": str(paths["private"]),
            "settings_sha256": settings_sha,
            "mcp_config_sha256": mcp_sha,
            "models_sha256": models_sha,
            "control_manifest": manifest,
            "runtime_dependency_manifest_sha256": omp.sha256_file(omp.RUNTIME_DEPENDENCIES_PATH),
            "runtime_closure_identity_sha256": omp.runtime_dependency_manifest()["closure_identity_sha256"],
            "runtime_closure_artifact_sha256": omp.runtime_dependency_manifest()["artifact"]["sha256"],
            "principal_files_sha256": omp.principal_files_sha256(),
            "settings_closure_sha256": omp.settings_closure_sha256(),
            "build_inventory_sha256": omp.sha256_file(omp.inventory_path()),
            "host_execution_environment": omp.host_execution_environment(),
            "mcp_servers": [],
            "network": "evaluator network namespace has loopback only; no host route",
            "filesystem_view": {
                "read_only": [SB_PROJECT, "/etc(synthetic)", SB_OMP, "manifest-listed runtime dependencies only"],
                "read_write": [SB_HOME, SB_TMP],
                "control_files_read_only_inside_home": list(CONTROL_FILES_IN_HOME),
                "absent": ["unlisted /usr software", "host HOME", "custody/private harness state", "observer evidence"],
            },
            "discovery_baseline": omp.discovery_baseline(paths["project"], paths["home"]),
            "omp_executable_sha256": omp.OMP_BUILD["sha256"],
            "substrate_executable_sha256": policy["substrate"]["executable_sha256"],
        },
    }


def omp_eval_argv(profile: dict[str, Any], prompt: str) -> list[str]:
    """Launch argv for evaluator: exact read-only tool selection, JSON mode."""
    reasoning_args: list[str] = []
    reasoning = profile.get("reasoning_configuration")
    if isinstance(reasoning, dict) and reasoning.get("thinking"):
        reasoning_args = ["--thinking", str(reasoning["thinking"])]

    return [
        SB_OMP, "-p", "--mode=json", "--no-session", "--no-title", "--no-extensions", "--no-rules", "--no-lsp",
        "--cwd", SB_PROJECT,
        "--tools", ",".join(EVALUATOR_TOOLS),
        "--model", str(profile.get("agent_model")),
        *reasoning_args,
        str(prompt),
    ]


def _eval_bwrap_argv(profile: dict[str, Any], paths: dict[str, Path], seccomp_fd: int,
                     launcher_config: str, sandbox_exe: str) -> list[str]:
    """Bubblewrap arguments for evaluator: mounts candidate bundle read-only via --ro-bind."""
    policy = profile["containment_policy"]
    argv = [
        policy["substrate"]["executable"],
        "--unshare-user", "--unshare-pid", "--unshare-ipc", "--unshare-uts", "--unshare-cgroup", "--unshare-net",
        "--die-with-parent", "--new-session", "--as-pid-1", "--clearenv", "--cap-drop", "ALL", "--hostname", "ssdp-evaluator",
        "--seccomp", str(seccomp_fd),
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", SB_TMP,
    ]
    argv += omp._runtime_mount_args("subject", paths)
    argv += [
        "--dir", "/etc", "--dir", "/home", "--dir", SB_HOME,
        "--dir", "/workspace", "--dir", "/opt", "--dir", "/opt/omp", "--dir", "/opt/ssdp",
        "--ro-bind", str(paths["etc"]), "/etc",
        "--ro-bind", str(paths["project"]), SB_PROJECT,  # Mounted strictly read-only
        "--bind", str(paths["home"]), SB_HOME,
    ]
    for rel in CONTROL_FILES_IN_HOME:
        argv += ["--ro-bind", str(paths["home"] / rel), f"{SB_HOME}/{rel}"]
    argv += [
        "--ro-bind", str(paths["control"]), SB_CTL,
        "--ro-bind", str(paths["subject_runtime"] / SB_OMP.lstrip("/")), sandbox_exe,
        "--chdir", "/",
        "/usr/bin/python3", f"{SB_CTL}/subject_launcher.py", launcher_config,
    ]
    return argv


def _extract_final_result_text(stdout: str) -> tuple[str, bool, str | None]:
    """Extract assistant result text and error status from native OMP stream."""
    final_text = ""
    streamed_delta_text: list[str] = []
    is_error = False
    stop_reason = None
    for line in stdout.splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(raw, dict):
            continue
        rtype = raw.get("type")
        if rtype == "content_block_delta":
            delta = raw.get("delta")
            if isinstance(delta, dict):
                text = delta.get("text")
                if isinstance(text, str):
                    streamed_delta_text.append(text)
        elif rtype == "message_update":
            ame = raw.get("assistantMessageEvent")
            if isinstance(ame, dict) and ame.get("type") == "content":
                delta = ame.get("delta")
                if isinstance(delta, str):
                    streamed_delta_text.append(delta)
        elif rtype == "agent_end":
            messages = [m for m in (raw.get("messages") or []) if isinstance(m, dict)]
            for message in messages:
                if message.get("role") == "assistant":
                    stop_reason = message.get("stopReason") or message.get("stop_reason")
                    content = message.get("content")
                    if isinstance(content, str) and content:
                        final_text = content
                    elif isinstance(content, list):
                        texts = [
                            item.get("text") for item in content
                            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)
                        ]
                        if texts:
                            final_text = "\n".join(texts)
        elif rtype == "message_end":
            message = raw.get("message")
            if isinstance(message, dict) and message.get("role") == "assistant":
                stop_reason = message.get("stopReason") or message.get("stop_reason")
                content = message.get("content")
                if isinstance(content, str) and content:
                    final_text = content
                elif isinstance(content, list):
                    texts = [
                        item.get("text") for item in content
                        if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str)
                    ]
                    if texts:
                        final_text = "\n".join(texts)

    if not final_text and streamed_delta_text:
        final_text = "".join(streamed_delta_text)

    if stop_reason in ("error", "aborted", "length"):
        is_error = True

    return final_text, is_error, stop_reason


def translate_stream_for_assessor(
    stdout: str,
    *,
    profile: dict[str, Any],
    returncode: int,
) -> str:
    """Format OMP stream into assess70-consumable trace with {"type":"result"} event."""
    final_text, is_error, stop_reason = _extract_final_result_text(stdout)
    if returncode != 0:
        is_error = True

    init_event = {
        "type": "init",
        "model": profile.get("agent_model"),
        "runtime_version": profile.get("provider_runtime", {}).get("version", "18.0.11"),
        "tools": list(profile.get("native_tools") or EVALUATOR_TOOLS),
        "native_capabilities": ["omp-json-event-stream-v1"],
        "mcp_servers": [],
    }

    result_event = {
        "type": "result",
        "result": final_text,
        "is_error": is_error,
        "stop_reason": stop_reason,
        "returncode": returncode,
    }

    lines = [json.dumps(init_event)]
    for raw_line in stdout.splitlines():
        if raw_line.strip():
            lines.append(raw_line)
    lines.append(json.dumps(result_event))
    return "\n".join(lines) + "\n"


def launch(profile: dict[str, Any], prompt: str, project: Path, env: dict[str, str]) -> dict[str, Any]:
    """Launch OMP evaluator in read-only sandbox and return translated stream."""
    problems = eval_profile_errors(profile)
    if problems:
        raise EvaluatorPrelaunchRefusal("evaluator launch refused: " + "; ".join(problems))
    dep_errors = omp.runtime_dependency_errors(profile)
    if dep_errors:
        raise EvaluatorPrelaunchRefusal("runtime dependency surface drifted: " + "; ".join(dep_errors))

    paths = _eval_paths(project, env)
    policy = profile["containment_policy"]
    route = policy["provider_route"]

    staged_errors = omp._verify_staged_runtime_dependencies(paths)
    if staged_errors:
        raise EvaluatorPrelaunchRefusal("staged runtime closure changed: " + "; ".join(staged_errors))

    discovery = omp.validate_ambient_discovery_closure(project, env)
    if discovery:
        raise EvaluatorPrelaunchRefusal("ambient discovery is not closed: " + "; ".join(discovery))

    runtime = profile["provider_runtime"]
    credential = os.environ.get(route["credential_env"])
    if credential is None:
        raise EvaluatorPrelaunchRefusal(f"provider credential variable {route['credential_env']!r} is not set")

    home_docs = {rel: omp.sha256_file(paths["home"] / rel) for rel in CONTROL_FILES_IN_HOME}
    budgets = profile["budgets"]

    def pipe() -> tuple[int, int]:
        return os.pipe()

    infer_up = pipe()
    infer_down = pipe()
    credential_r, credential_w = pipe()
    obs_ev, ln_ev = pipe(), pipe()
    sinks = {"observer": bytearray(), "launcher": bytearray()}
    procs: list[subprocess.Popen] = []
    seccomp_r = seccomp_w = -1
    run_launch = paths["control"] / "launcher.json"

    boundary_sentinel = paths["private"] / "observer-boundary-host-sentinel.txt"
    boundary_sentinel.write_text("SUPERVISOR-PRIVATE-OBSERVER-PROBE\n", encoding="utf-8")
    boundary_sentinel.chmod(0o600)

    try:
        threads = [
            omp._drain(obs_ev[0], sinks["observer"]),
            omp._drain(ln_ev[0], sinks["launcher"]),
        ]
        observer_probe_paths = [
            ("host_home", str(Path.home() / ".bashrc")),
            ("qualification_custody", str(omp.REPO_ROOT / "qualification" / "ssdp70" / "PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md")),
            ("supervisor_private", str(boundary_sentinel)),
        ]
        observer_channels = (infer_up[0], infer_down[1], obs_ev[1], credential_r)
        raw_observer_argv = omp._observer_bwrap_argv(
            profile, paths, observer_channels, observer_probe_paths, os.getpid(),
            os.readlink("/proc/self/ns/net"), os.readlink("/proc/self/ns/pid")
        )
        observer_command_at = raw_observer_argv.index("/usr/bin/python3")
        observer_args_r, observer_args_w = os.pipe()
        os.write(observer_args_w, b"\0".join(a.encode() for a in raw_observer_argv[1:observer_command_at]) + b"\0")
        os.close(observer_args_w)
        observer_launch_argv = [
            raw_observer_argv[0], "--args", str(OBSERVER_ARGUMENT_TARGET),
            *raw_observer_argv[observer_command_at:]
        ]
        observer_pass_fds = tuple(sorted(set((*observer_channels, observer_args_r))))
        observer_helper_argv = [
            sys.executable, "-I", "-S", str(omp.OBSERVER_EXEC_HELPER),
            ",".join(str(fd) for fd in observer_channels), str(observer_args_r), *observer_launch_argv,
        ]
        observer = subprocess.Popen(
            observer_helper_argv,
            pass_fds=observer_pass_fds,
            env={"PATH": omp.MINIMAL_PATH, "HOME": OBSERVER_HOME},
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        procs.append(observer)
        for fd in observer_channels:
            os.close(fd)
        os.close(observer_args_r)

        omp._await_ready(observer, "provider-control/observer boundary", b"boundary-ready")
        credential_bytes = credential.encode("utf-8")
        offset = 0
        while offset < len(credential_bytes):
            offset += os.write(credential_w, credential_bytes[offset:])
        os.close(credential_w)
        credential_w = -1
        credential = ""
        omp._await_ready(observer, "provider-control/observer")

        probes = [
            {"name": "version", "argv": [SB_OMP, "--version"], "timeout_s": 60},
            {"name": "effective-settings", "argv": [SB_OMP, "config", "list", "--json"], "timeout_s": 60},
        ]
        launcher_cfg = {
            "status_fd": ln_ev[1],
            "omp_exe": SB_OMP,
            "omp_exe_sha256": omp.OMP_BUILD["sha256"],
            "relays": [
                {"name": "inference", "port": RELAY_PORTS["inference"], "read_fd": infer_down[0], "write_fd": infer_up[1]},
            ],
            "env": omp._subject_env(),
            "omp_argv": omp_eval_argv(profile, prompt),
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

        argv = _eval_bwrap_argv(profile, paths, seccomp_r, f"{SB_CTL}/launcher.json", SB_OMP)
        args_r, args_w = os.pipe()
        command_at = argv.index("/usr/bin/python3")
        os.write(args_w, b"\0".join(a.encode() for a in argv[1:command_at]) + b"\0")
        os.close(args_w)
        launch_argv = [argv[0], "--args", str(args_r), *argv[command_at:]]
        sandbox_fds = (infer_up[1], infer_down[0], ln_ev[1], seccomp_r, args_r)

        done = subprocess.run(
            launch_argv,
            capture_output=True,
            pass_fds=sandbox_fds,
            timeout=budgets["timeout_s"] + 30,
            check=False,
        )
        stdout = done.stdout.decode("utf-8", "replace")
        stderr = done.stderr.decode("utf-8", "replace")
        returncode = done.returncode

    finally:
        for fd in (infer_up[1], infer_down[0], ln_ev[1]):
            try:
                os.close(fd)
            except OSError:
                pass
        if seccomp_r >= 0:
            try:
                os.close(seccomp_r)
            except OSError:
                pass
        if seccomp_w >= 0:
            try:
                os.close(seccomp_w)
            except OSError:
                pass
        for proc in procs:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)

    translated_stdout = translate_stream_for_assessor(
        stdout,
        profile=profile,
        returncode=returncode,
    )

    command_identity = {
        "adapter_id": ADAPTER_ID,
        "executable": runtime["executable"],
        "argv": argv,
        "model": str(profile.get("agent_model")),
        "reasoning_configuration": profile.get("reasoning_configuration"),
        "tools": list(profile.get("native_tools") or []),
        "mcp_servers": [],
        "mcp_server_executable_sha256": {},
        "settings_file": str(paths["agent"] / "config.yml"),
        "settings_file_sha256": home_docs[".omp/agent/config.yml"],
        "mcp_config_file": str(paths["agent"] / "mcp.json"),
        "mcp_config_sha256": home_docs[".omp/agent/mcp.json"],
        "runtime_version": runtime.get("version"),
        "runtime_dependency_manifest_sha256": omp.sha256_file(omp.RUNTIME_DEPENDENCIES_PATH),
        "runtime_closure_identity_sha256": omp.runtime_dependency_manifest()["closure_identity_sha256"],
        "runtime_closure_artifact_sha256": omp.runtime_dependency_manifest()["artifact"]["sha256"],
        "native_network": "evaluator netns loopback only",
    }

    return {
        "stdout": translated_stdout,
        "stderr": stderr,
        "returncode": returncode,
        "command_identity": command_identity,
    }


def runtime_observation(stdout: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Parse evaluator runtime observation from stream."""
    model = None
    tools = list(EVALUATOR_TOOLS)
    runtime_version = "18.0.11"

    for line in stdout.splitlines():
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(raw, dict):
            continue
        if raw.get("type") == "init":
            return {
                "model": raw.get("model"),
                "runtime_version": raw.get("runtime_version"),
                "tools": raw.get("tools") or list(EVALUATOR_TOOLS),
                "native_capabilities": raw.get("native_capabilities") or ["omp-json-event-stream-v1"],
                "messaging_socket_path": None,
                "memory_paths": {},
                "mcp_servers": [],
                "observation_errors": [],
                "observation_source": "trusted evaluator adapter observation",
                "permission_mode": None,
            }
        message = raw.get("message")
        if isinstance(message, dict) and message.get("role") == "assistant":
            p, m = message.get("provider"), message.get("model")
            if p and m:
                model = f"{p}/{m}"

    return {
        "model": model,
        "runtime_version": runtime_version,
        "tools": tools,
        "native_capabilities": ["omp-json-event-stream-v1"],
        "messaging_socket_path": None,
        "memory_paths": {},
        "mcp_servers": [],
        "observation_errors": [],
        "observation_source": "trusted evaluator adapter observation",
        "permission_mode": None,
    }


def freeze_profile(
    template: dict[str, Any],
    *,
    executable_path: str,
    provider_route: dict[str, Any],
    reasoning: dict[str, Any],
    profile_id: str,
    budgets: dict[str, Any] | None = None,
    substrate_executable: str = "/usr/bin/bwrap",
) -> dict[str, Any]:
    """Fill evaluator profile template with exact digests."""
    profile = copy.deepcopy(template)
    profile["profile_id"] = profile_id
    profile["adapter_id"] = ADAPTER_ID
    profile["native_tools"] = list(EVALUATOR_TOOLS)
    profile["mcp_servers"] = []
    profile["workspace_realization"] = {"kind": "temporary-read-only-evidence-bundle"}
    profile["install_mechanism"] = "none"

    route = dict(profile["containment_policy"]["provider_route"])
    route.update(provider_route)
    profile["containment_policy"]["provider_route"] = route
    profile["agent_model"] = f"{route['provider_id']}/{route['model_id']}"

    runtime = profile["provider_runtime"]
    executable = omp.runtime_dependency_manifest()["subject_executable"]
    runtime["executable_path"] = SB_OMP
    runtime["executable_sha256"] = executable["sha256"]
    runtime["executable_bytes"] = executable["bytes"]
    runtime["build_id"] = executable["build_id"]
    runtime["provider"] = route["provider_id"]

    profile["reasoning_configuration"] = dict(reasoning)
    if budgets:
        profile["budgets"] = dict(budgets)

    policy = profile["containment_policy"]
    policy["substrate"]["executable"] = substrate_executable
    policy["substrate"]["executable_sha256"] = omp.sha256_file(Path(substrate_executable))
    policy["settings_closure_sha256"] = omp.settings_closure_sha256()
    policy["runtime_dependency_manifest_sha256"] = omp.sha256_file(omp.RUNTIME_DEPENDENCIES_PATH)
    policy["runtime_closure_identity_sha256"] = omp.runtime_dependency_manifest()["closure_identity_sha256"]
    policy["principal_files_sha256"] = omp.principal_files_sha256()
    policy["execution_support_sha256"] = {
        "adapters/omp_eval.py": omp.sha256_file(Path(__file__).resolve()),
        "core70.py": omp.sha256_file(EVAL_DIR / "core70.py"),
        "assess70.py": omp.sha256_file(EVAL_DIR / "assess70.py"),
        "write_oracles.py": omp.sha256_file(EVAL_DIR / "write_oracles.py"),
        "profiles/omp-evaluator-readonly.template.json": omp.sha256_file(EVAL_DIR / "profiles" / "omp-evaluator-readonly.template.json"),
    }
    policy["build_inventory_sha256"] = omp.sha256_file(omp.inventory_path())
    policy["host_execution_environment"] = omp.host_execution_environment()

    return profile
