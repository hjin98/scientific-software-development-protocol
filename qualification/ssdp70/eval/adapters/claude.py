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

ADAPTER_ID = "claude-stream-json-v1"
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


def clean_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        if "SESSION" in key or key in {"CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_PID"}:
            env.pop(key)
    return env


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
        "--setting-sources",
        "project,local",
        "--permission-mode",
        str(profile.get("permission_mode", "acceptEdits")),
    ]
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
            "model": model,
            "reasoning_configuration": reasoning,
            "allowed_tools": allowed_tools,
            "disallowed_tools": disallowed_tools,
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


def normalize(stdout: str, run_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], int]:
    events: list[dict[str, Any]] = []
    completeness: list[dict[str, Any]] = []
    errors: list[str] = []
    sequence = 0
    lines = stdout.splitlines()

    for native_index, line in enumerate(lines):
        native_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
        mapped: list[str] = []
        classification = "metadata"
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

        if raw.get("type") == "system" and raw.get("subtype") == "init":
            sequence += 1
            skills = [s if isinstance(s, str) else s.get("name", "") for s in raw.get("skills") or []]
            event = _event(run_id, sequence, "catalog_snapshot", native_index, native_sha256, {
                "logical_skill_ids": skills,
                "model": raw.get("model"),
                "runtime_version": raw.get("claude_code_version"),
            })
            events.append(event)
            mapped.append(event["event_id"])
            classification = "catalog"
            oracle_relevant = True

        elif raw.get("type") == "assistant":
            classification = "assistant-message"
            for block_index, block in enumerate(raw.get("message", {}).get("content", [])):
                if block.get("type") != "tool_use":
                    continue
                oracle_relevant = True
                tool = block.get("name")
                data = block.get("input") or {}
                if not isinstance(data, dict):
                    data = {"raw": data}
                if tool == "Skill":
                    sequence += 1
                    skill = data.get("skill") or data.get("command")
                    event = _event(run_id, sequence, "root_selection", native_index, native_sha256, {
                        "logical_root": skill,
                        "selection_mechanism": "Skill",
                        "native_operation": tool,
                        "input": data,
                        "block_index": block_index,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                elif tool in READ_TOOLS:
                    sequence += 1
                    event = _event(run_id, sequence, "resource_access", native_index, native_sha256, {
                        "operation": tool.lower(),
                        "resource_identity": _resource_identity(tool, data),
                        "input": data,
                        "result_reference": None,
                        "block_index": block_index,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                elif tool in MUTATION_TOOLS:
                    sequence += 1
                    target = data.get("file_path") or data.get("path") or data.get("notebook_path")
                    event = _event(run_id, sequence, "mutation", native_index, native_sha256, {
                        "operation": tool.lower(),
                        "logical_target": target,
                        "workspace_external_class": "unresolved",
                        "authorization_decision": "profile-governed",
                        "disposition": "attempted",
                        "input": data,
                        "block_index": block_index,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                elif tool in DELEGATE_TOOLS:
                    sequence += 1
                    event = _event(run_id, sequence, "delegate_call", native_index, native_sha256, {
                        "delegate_id": data.get("name") or data.get("subagent_type") or f"native-{native_index}-{block_index}",
                        "parent_actor": "executor",
                        "request": data,
                        "launched_work_relation": "requested",
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                elif tool in NETWORK_TOOLS:
                    sequence += 1
                    event = _event(run_id, sequence, "network_external_action", native_index, native_sha256, {
                        "destination_service": data.get("url") or data.get("query"),
                        "operation": tool,
                        "authorization_decision": "profile-governed",
                        "disposition": "attempted",
                        "input": data,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                elif tool == "Bash":
                    sequence += 1
                    event = _event(run_id, sequence, "tool_action", native_index, native_sha256, {
                        "semantic_capability_classes": ["process_execution"],
                        "native_operation": tool,
                        "input": data,
                        "result_reference": None,
                        "block_index": block_index,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                else:
                    sequence += 1
                    event = _event(run_id, sequence, "tool_action", native_index, native_sha256, {
                        "semantic_capability_classes": ["unclassified-native-tool"],
                        "native_operation": tool,
                        "input": data,
                        "result_reference": None,
                        "block_index": block_index,
                    })
                    events.append(event)
                    mapped.append(event["event_id"])
                    errors.append(f"native tool {tool!r} has no semantic capability mapping")

        elif raw.get("type") == "result":
            classification = "terminal-result"
            oracle_relevant = True
            sequence += 1
            term = _event(run_id, sequence, "termination", native_index, native_sha256, {
                "state": raw.get("subtype") or ("error" if raw.get("is_error") else "completed"),
                "native_return_state": {"is_error": raw.get("is_error")},
                "terminal_result_exists": "result" in raw,
            })
            events.append(term)
            mapped.append(term["event_id"])
            sequence += 1
            final = _event(run_id, sequence, "final_result", native_index, native_sha256, {
                "result_text": raw.get("result", ""),
                "artifact_reference": "final-report.md",
            })
            events.append(final)
            mapped.append(final["event_id"])
            sequence += 1
            usage = _event(run_id, sequence, "usage_timing", native_index, native_sha256, {
                "duration_ms": raw.get("duration_ms"),
                "num_turns": raw.get("num_turns"),
                "total_cost_usd": raw.get("total_cost_usd"),
                "usage": raw.get("usage"),
                "source": "provider-result-event",
            })
            events.append(usage)
            mapped.append(usage["event_id"])

        completeness.append({
            "native_index": native_index,
            "native_sha256": native_sha256,
            "mapped_event_ids": mapped,
            "classification": classification,
            "oracle_relevant": oracle_relevant,
        })

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
    skills = snapshots[0]["payload"].get("logical_skill_ids") or []
    counts = {name: skills.count(name) for name in SSDP_SKILLS}
    return {"ok": all(value == 1 for value in counts.values()), "ssdp_counts": counts, "catalog": skills}


def owner_reads(events: list[dict[str, Any]], owner_name: str) -> list[int]:
    hits: list[int] = []
    for event in events:
        if event.get("kind") != "resource_access":
            continue
        payload = event.get("payload") or {}
        if owner_name in json.dumps(payload, sort_keys=True):
            hits.append(int(event["sequence"]))
    return hits


def prepare_prompt(profile: dict[str, Any], entry: str, prompt: str) -> str:
    if not entry.startswith("pinned:"):
        return prompt.strip()
    root = entry.split(":", 1)[1]
    template = profile.get("pinned_root_instruction_template", "Use the {root} skill. {prompt}")
    return str(template).format(root=root, prompt=prompt.strip())
