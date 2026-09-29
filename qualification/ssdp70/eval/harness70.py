#!/usr/bin/env python3
"""Protocol 7.0 portable Stage F composite-episode harness.

The portable core owns identity, admissibility, normalized evidence and scoring inputs.
Runtime adapters own launch/install/native-event translation only. Qualification mode
requires an independently produced profile-admission record; probe mode is used for the
pre-run discrimination suite and cannot by itself authorize a campaign.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402

OWNER = "scientific-inspectability-and-initiative.md"
# Harness-owned git exclude for the run project. It is restored before the diff is computed so that
# neither the runtime nor the executor can hide a path from the diff handed to the oracles.
PROJECT_GIT_EXCLUDE = "__pycache__/\n*.pyc\n.claude/\n.mcp.json\n.qualification-tmp/\n"
FINAL_TREE_IGNORE = (".git", ".claude", ".mcp.json", ".qualification-tmp", "__pycache__")


def load_adapter(name: str):
    if not name or any(part in {"", ".", ".."} for part in name.split(".")):
        raise core70.ContractError(f"invalid adapter name {name!r}")
    module = importlib.import_module(f"adapters.{name}")
    for attr in ("ADAPTER_ID", "install_skills", "launch", "normalize", "final_result", "catalog_isolation", "owner_reads", "prepare_prompt", "clean_env", "runtime_observation", "realize_containment"):
        if not hasattr(module, attr):
            raise core70.ContractError(f"adapter {name!r} is missing {attr}")
    return module


def load_manifest(corpus: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load((corpus / "manifest.yaml").read_text(encoding="utf-8"))
    episodes = data.get("episodes") if isinstance(data, dict) else data
    if not isinstance(episodes, list):
        raise core70.ContractError("corpus manifest must contain an episodes list")
    ids: set[str] = set()
    for item in episodes:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise core70.ContractError("every episode must be an object with a non-empty id")
        if item["id"] in ids:
            raise core70.ContractError(f"duplicate episode id {item['id']!r}")
        ids.add(item["id"])
    return episodes


def load_arms_manifest(path: Path) -> tuple[dict[str, dict[str, Any]], str]:
    data = core70.load_json(path)
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("arms"), list):
        raise core70.ContractError("arms manifest is malformed")
    arms: dict[str, dict[str, Any]] = {}
    for row in data["arms"]:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            raise core70.ContractError("arms manifest contains an invalid arm")
        required = ("name", "requested_ref", "commit", "version", "skills_path", "dist_tree_sha256")
        if any(key not in row for key in required):
            raise core70.ContractError(f"arm {row.get('name')!r} is missing identity fields")
        if row["name"] in arms:
            raise core70.ContractError(f"duplicate arm {row['name']!r}")
        arms[row["name"]] = row
    return arms, core70.sha256_file(path)


def resolve_arm_dist(row: dict[str, Any]) -> Path:
    dist = Path(row["skills_path"]).resolve()
    if not dist.is_dir():
        raise core70.ContractError(f"prepared arm directory is unavailable: {dist}")
    actual = core70.sha256_tree(dist)
    if actual != row["dist_tree_sha256"]:
        raise core70.ContractError(
            f"prepared arm package digest mismatch for {row['name']}: {actual} != {row['dist_tree_sha256']}"
        )
    return dist


def _yaml_tree_to_json(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if path.is_dir():
            (dst / rel).mkdir(parents=True, exist_ok=True)
        elif path.suffix in {".yaml", ".yml"}:
            target = dst / rel.with_suffix(".json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(yaml.safe_load(path.read_text(encoding="utf-8")), default=str),
                encoding="utf-8",
            )
        else:
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dst / rel)


def build_project(corpus: Path, episode: dict[str, Any], project: Path) -> None:
    fixture = corpus / "fixtures" / episode["fixture"]
    if not fixture.is_dir():
        raise core70.ContractError(f"fixture directory is missing for {episode['id']}")
    project.mkdir(parents=True)
    script = fixture / "build_history.sh"
    if script.is_file():
        subprocess.run(["bash", str(script)], cwd=project, check=True, capture_output=True)
    if (fixture / "project").is_dir():
        shutil.copytree(
            fixture / "project",
            project,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    if not (project / ".git").is_dir():
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    info = project / ".git" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "exclude").write_text(PROJECT_GIT_EXCLUDE, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=project, check=True)
    subprocess.run(
        ["git", "-c", "user.email=eval@example.invalid", "-c", "user.name=eval", "commit", "-qm", "fixture", "--allow-empty"],
        cwd=project,
        check=True,
    )


def _safe_oracle_path(root: Path, episode_id: str, relative: str) -> Path:
    base = (root / episode_id).resolve()
    path = (base / relative).resolve()
    if path != base and base not in path.parents:
        raise core70.ContractError(f"oracle path escapes episode custody root: {relative}")
    return path


def run_oracles(oracles_root: Path | None, episode_id: str, requirements: core70.Requirements, out: Path) -> dict[str, Any]:
    result_payload: dict[str, Any] = {"schema": 1, "results": {}}
    oracle_out = out / "oracle-output"
    oracle_out.mkdir(exist_ok=True)
    for item in requirements.oracles:
        oid = item["id"]
        row: dict[str, Any] = {"executed": False, "pass": False, "returncode": None}
        result_payload["results"][oid] = row
        if oracles_root is None:
            continue
        check = _safe_oracle_path(oracles_root, episode_id, item["path"])
        if not check.is_file():
            continue
        stdout_rel = f"oracle-output/{oid}.stdout.txt"
        stderr_rel = f"oracle-output/{oid}.stderr.txt"
        proc = subprocess.run(
            [sys.executable, str(check), str(out / "final-tree"), str(out)],
            capture_output=True,
            text=True,
        )
        (out / stdout_rel).write_text(proc.stdout, encoding="utf-8")
        (out / stderr_rel).write_text(proc.stderr, encoding="utf-8")
        row.update({
            "executed": True,
            "pass": proc.returncode == 0,
            "returncode": proc.returncode,
            "oracle_path": item["path"],
            "oracle_sha256": core70.sha256_file(check),
            "stdout_artifact": stdout_rel,
            "stderr_artifact": stderr_rel,
            "stdout_sha256": core70.sha256_file(out / stdout_rel),
            "stderr_sha256": core70.sha256_file(out / stderr_rel),
        })
    (out / "oracle.json").write_text(json.dumps(result_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result_payload


def _final_tree_ignore(project: Path, exclude_paths: list[str]):
    """copytree ignore: the fixed patterns plus EXACTLY the verified runtime placeholders (top-level names)."""
    for name in exclude_paths:
        if not isinstance(name, str) or not name or "/" in name or name in {".", ".."} or any(ch in name for ch in "*?[]"):
            raise core70.ContractError(f"runtime placeholder exclusion {name!r} is not an exact top-level name")
    exact = set(exclude_paths)
    generic = shutil.ignore_patterns(*FINAL_TREE_IGNORE)
    project_resolved = project.resolve()

    def ignore(directory, names):
        ignored = set(generic(directory, names))
        if Path(directory).resolve() == project_resolved:
            ignored |= exact & set(names)
        return ignored

    return ignore


def capture_project_state(project: Path, out: Path, runtime_exclusions: list[str]) -> str:
    """Write diff.patch and final-tree for the oracles.

    The harness-owned git exclude is restored first (the runtime appends its stub names to it and the
    executor may edit it), then only the verified runtime placeholders are hidden, by exact pathspec and
    exact top-level name. Anything else the run left in the project stays visible to the oracles.
    """
    tree_ignore = _final_tree_ignore(project, runtime_exclusions)
    (project / ".git" / "info").mkdir(parents=True, exist_ok=True)
    (project / ".git" / "info" / "exclude").write_text(PROJECT_GIT_EXCLUDE, encoding="utf-8")
    pathspecs = [".", ":(exclude).claude", *(f":(exclude){name}" for name in runtime_exclusions)]
    subprocess.run(["git", "add", "-A", "-N", "--", *pathspecs], cwd=project, capture_output=True)
    diff = subprocess.run(
        ["git", "diff", "--", *pathspecs],
        cwd=project,
        capture_output=True,
        text=True,
    ).stdout
    (out / "diff.patch").write_text(diff, encoding="utf-8")
    shutil.copytree(project, out / "final-tree", ignore=tree_ignore)
    return diff


def _write_normalized(events: list[dict[str, Any]], out: Path) -> None:
    (out / "events.normalized.jsonl").write_text(
        "".join(json.dumps(event, sort_keys=True, default=str) + "\n" for event in events),
        encoding="utf-8",
    )
    tool_rows = []
    for event in events:
        if event["kind"] in {"resource_access", "tool_action", "delegate_call", "delegate_return", "issue_evidence_access", "mutation", "network_external_action", "root_selection"}:
            tool_rows.append(event)
    (out / "tool-calls.jsonl").write_text(
        "".join(json.dumps(event, sort_keys=True, default=str) + "\n" for event in tool_rows),
        encoding="utf-8",
    )


def _termination_state(events: list[dict[str, Any]]) -> tuple[bool, bool]:
    terminations = [e for e in events if e.get("kind") == "termination"]
    if not terminations:
        return False, False
    state = terminations[-1].get("payload", {}).get("native_return_state") or {}
    return True, not bool(state.get("is_error"))


def run_identity(
    *,
    corpus: Path,
    episode: dict[str, Any],
    arm: dict[str, Any],
    arms_manifest_sha256: str,
    dist: Path,
    profile_bundle: core70.ProfileBundle,
    profile_path: Path,
    capability_path: Path,
    requirements: core70.Requirements,
    requirements_root: Path,
    adapter_module,
    oracles: Path | None,
    mode: str,
    admission: Path | None,
    rep: int,
    pair_order: list[str],
) -> dict[str, Any]:
    fixture = corpus / "fixtures" / episode["fixture"]
    stub = corpus / "stubs" / episode["stub"] if episode.get("stub") else None
    episode_oracles = oracles / episode["id"] if oracles is not None else None
    identity = {
        "schema": 2,
        "episode": episode["id"],
        "arm": arm["name"],
        "subject": {
            "requested_ref": arm["requested_ref"],
            "commit": arm["commit"],
            "version": arm["version"],
            "package_sha256": arm["dist_tree_sha256"],
            "prepared_arms_manifest_sha256": arms_manifest_sha256,
        },
        "replicate": rep,
        "pair_order": list(pair_order),
        "execution_mode": mode,
        "profile_key": profile_bundle.profile_key,
        "profile_key_sha256": profile_bundle.profile_key_sha256,
        "profile_document_sha256": core70.sha256_file(profile_path),
        "capability_manifest_sha256": profile_bundle.capability_manifest_sha256,
        "episode_config_sha256": core70.stable_json_sha256(episode),
        "corpus_manifest_sha256": core70.sha256_file(corpus / "manifest.yaml"),
        "fixture_tree_sha256": core70.sha256_tree(fixture),
        "stub_tree_sha256": core70.sha256_tree(stub),
        "oracles_tree_sha256": core70.sha256_tree(episode_oracles),
        "requirements": {
            "required_artifacts_sha256": requirements.artifact_manifest_digest,
            "required_oracles_sha256": requirements.oracle_manifest_digest,
            "expected_scoring_items_sha256": requirements.scoring_manifest_digest,
            "requirements_root_sha256": core70.sha256_tree(requirements_root),
        },
        "qualification_core_sha256": core70.sha256_file(Path(core70.__file__).resolve()),
        "harness_sha256": core70.sha256_file(Path(__file__).resolve()),
        "adapter_normalizer_sha256": core70.sha256_file(Path(adapter_module.__file__).resolve()),
        "normalized_event_schema": core70.SCHEMA,
        "stub_tools_sha256": core70.sha256_tree(HERE / "stub_tools"),
        "profile_admission_sha256": core70.admission_bundle_sha256(admission, role="executor") if admission is not None else None,
        "dist_tree_sha256_verified": core70.sha256_tree(dist),
    }
    identity["identity_sha256"] = core70.stable_json_sha256(identity)
    return identity


def run_episode(
    *,
    corpus: Path,
    episode: dict[str, Any],
    arm: dict[str, Any],
    arms_manifest_sha256: str,
    dist: Path,
    out: Path,
    profile_bundle: core70.ProfileBundle,
    profile_path: Path,
    capability_path: Path,
    requirements: core70.Requirements,
    requirements_root: Path,
    adapter_module,
    oracles: Path | None,
    mode: str,
    admission: Path | None,
    identity: dict[str, Any],
    pair_order: list[str],
) -> dict[str, Any]:
    adapter_sha = core70.sha256_file(Path(adapter_module.__file__).resolve())
    core_sha = core70.sha256_file(Path(core70.__file__).resolve())
    admission_errors = core70.validate_profile_admission(
        admission,
        mode=mode,
        profile_key_sha256=profile_bundle.profile_key_sha256,
        adapter_sha256=adapter_sha,
        core_sha256=core_sha,
        capability_manifest_sha256=profile_bundle.capability_manifest_sha256,
        role="executor",
    )
    if admission_errors:
        raise core70.ContractError("; ".join(admission_errors))
    if admission is not None:
        frozen_admission_sha = identity.get("profile_admission_sha256")
        current_admission_sha = core70.admission_bundle_sha256(admission, role="executor")
        if current_admission_sha != frozen_admission_sha:
            raise core70.ContractError("executor profile-admission bundle changed after run identity was frozen")

    claims = episode.get("claims") or []
    if not isinstance(claims, list) or not all(isinstance(x, str) and x for x in claims):
        raise core70.ContractError(f"episode {episode['id']} claims must be a list of strings")
    profile_errors = core70.profile_claim_errors(profile_bundle, claims)
    if mode == "qualification" and profile_errors:
        raise core70.ContractError("; ".join(profile_errors))

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "run-identity.json").write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "profile-snapshot.json").write_text(json.dumps(profile_bundle.profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "capability-manifest-snapshot.json").write_text(json.dumps(profile_bundle.capabilities, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "requirements-snapshot.json").write_text(json.dumps(core70.requirements_snapshot(requirements), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if admission is not None:
        core70.snapshot_profile_admission(admission, out, role="executor", prefix="profile-admission")

    with tempfile.TemporaryDirectory(prefix="ssdp70-") as tmp_name:
        tmp = Path(tmp_name)
        project = tmp / "project"
        private = tmp / "harness-private"
        stub, log = private / "stub", private / "side-effects.jsonl"
        runtime_home = private / "runtime-home"
        runtime_tmp = project / ".qualification-tmp"
        build_project(corpus, episode, project)
        private.mkdir()
        stub.mkdir()
        if episode.get("stub"):
            _yaml_tree_to_json(corpus / "stubs" / episode["stub"], stub)
        log.write_text("", encoding="utf-8")
        log.chmod(0o600)
        mcp_servers = profile_bundle.profile.get("mcp_servers") or []
        if mcp_servers:
            mcp_server = private / "mcp-server.py"
            shutil.copy2(HERE / "stub_tools" / "mediator.py", mcp_server)
            mcp_server.chmod(0o500)
            account_file = private / "mcp-account.txt"
            account_file.write_text((episode.get("account") or "agent-account") + "\n", encoding="utf-8")
            account_file.chmod(0o400)
        runtime_home.mkdir()
        runtime_tmp.mkdir()
        adapter_module.install_skills(dist, project)
        installed_skills = project / ".claude" / "skills"
        installed_digest = core70.sha256_tree(installed_skills)
        if installed_digest != arm["dist_tree_sha256"]:
            raise core70.ContractError(
                f"installed protocol package digest mismatch: {installed_digest} != {arm['dist_tree_sha256']}"
            )
        prompt = adapter_module.prepare_prompt(profile_bundle.profile, episode.get("entry", "ordinary"), episode["prompt"])
        env = adapter_module.clean_env()
        env.update({
            "HOME": str(runtime_home),
            "XDG_CONFIG_HOME": str(runtime_home / ".config"),
            "XDG_CACHE_HOME": str(runtime_home / ".cache"),
            "TMPDIR": str(runtime_tmp),
            "TMP": str(runtime_tmp),
            "TEMP": str(runtime_tmp),
        })
        containment = adapter_module.realize_containment(profile_bundle.profile, project, env)
        (out / "containment-realization.json").write_text(
            json.dumps(containment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        runtime_baseline_fn = getattr(adapter_module, "runtime_entry_baseline", None)
        runtime_baseline = runtime_baseline_fn(profile_bundle.profile, project) if runtime_baseline_fn is not None else None
        launched = adapter_module.launch(profile_bundle.profile, prompt, project, env)
        stdout, stderr = launched["stdout"], launched["stderr"]
        (out / "trace.jsonl").write_text(stdout, encoding="utf-8")
        if stderr:
            (out / "stderr.txt").write_text(stderr, encoding="utf-8")
        else:
            (out / "stderr.txt").write_text("", encoding="utf-8")

        normalization_context = {
            "project": str(project),
            "skills_root": str(installed_skills),
            "package_identity": dict(identity["subject"]),
        }
        events, completeness, normalization_errors, native_event_count = adapter_module.normalize(
            stdout, identity["identity_sha256"], normalization_context
        )
        runtime_observation = adapter_module.runtime_observation(stdout)
        command_identity = launched.get("command_identity")
        profile_errors.extend(core70.validate_launch_identity(profile_bundle.profile, command_identity))
        profile_errors.extend(core70.validate_runtime_observation(profile_bundle, runtime_observation))
        realization = containment.get("realization") if isinstance(containment, dict) else None
        if not isinstance(realization, dict):
            profile_errors.append("containment realization record is malformed")
        elif isinstance(command_identity, dict):
            if command_identity.get("settings_file_sha256") != realization.get("settings_sha256"):
                profile_errors.append("launch settings bytes differ from retained containment realization")
            if command_identity.get("mcp_config_sha256") != realization.get("mcp_config_sha256"):
                profile_errors.append("launch MCP bytes differ from retained containment realization")
            retained_server_digests = {
                row.get("name"): row.get("executable_sha256")
                for row in (realization.get("mcp_servers") or [])
                if isinstance(row, dict)
            }
            if command_identity.get("mcp_server_executable_sha256") != retained_server_digests:
                profile_errors.append("launch MCP server executable bytes differ from retained containment realization")
        post_run = getattr(adapter_module, "validate_post_run_project_state", None)
        if post_run is not None:
            profile_errors.extend(post_run(profile_bundle.profile, project))
        runtime_exclusions: list[str] = []
        inspect_entries = getattr(adapter_module, "inspect_runtime_entries", None)
        if inspect_entries is not None:
            inspection = inspect_entries(profile_bundle.profile, project, runtime_baseline)
            if inspection.get("record") is not None:
                (out / "runtime-created-entries.json").write_text(
                    json.dumps(inspection["record"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
                )
            profile_errors.extend(inspection.get("errors") or [])
            runtime_exclusions = list(inspection.get("exclude_paths") or [])
        installed_after = core70.sha256_tree(installed_skills)
        if installed_after != arm["dist_tree_sha256"]:
            profile_errors.append(
                f"installed protocol package changed during execution: {installed_after} != {arm['dist_tree_sha256']}"
            )
        auto_memory = (runtime_observation.get("memory_paths") or {}).get("auto") if isinstance(runtime_observation, dict) else None
        if isinstance(auto_memory, str) and auto_memory:
            try:
                Path(auto_memory).resolve().relative_to(runtime_home.resolve())
            except (OSError, ValueError):
                profile_errors.append("runtime auto-memory path escapes the fresh run-owned HOME")
        profile_errors.extend(core70.validate_claim_observability(events, claims))
        owner_read_sequences = adapter_module.owner_reads(events, OWNER)
        if any("owner-read" in str(claim).lower() for claim in claims) and not owner_read_sequences:
            profile_errors.append("owner-read claim has no successful read of the canonical owner resource")
        _write_normalized(events, out)
        (out / "normalization-map.json").write_text(
            json.dumps({"schema": 1, "native_event_count": native_event_count, "entries": completeness}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        event_errors = core70.validate_normalized_events(events, identity["identity_sha256"])
        completeness_errors = core70.validate_completeness_map(native_event_count, completeness, events)
        event_errors.extend(normalization_errors)

        final_text = adapter_module.final_result(events)
        (out / "final-report.md").write_text(final_text, encoding="utf-8")
        shutil.copy2(log, out / "side-effects.jsonl")
        if (stub / "issues").is_dir():
            shutil.copytree(stub / "issues", out / "issues-final")

        capture_project_state(project, out, runtime_exclusions)

        run_oracles(oracles, episode["id"], requirements, out)

        terminal_exists, terminal_ok = _termination_state(events)
        final_result_exists = any(e.get("kind") == "final_result" for e in events)
        catalog = adapter_module.catalog_isolation(events)
        execution_ok = bool(launched["returncode"] == 0 and terminal_exists and terminal_ok)

        preliminary = {
            "schema": 2,
            "episode": episode["id"],
            "arm": arm["name"],
            "subject_commit": arm["commit"],
            "execution_mode": mode,
            "execution_returncode": launched["returncode"],
            "execution_ok": execution_ok,
            "wall_s": launched["wall_s"],
            "pair_order": pair_order,
            "profile_key_sha256": profile_bundle.profile_key_sha256,
            "run_identity_sha256": identity["identity_sha256"],
            "catalog_isolation": catalog,
            "owner_read_sequences": owner_read_sequences,
            "normalized_event_count": len(events),
            "native_event_count": native_event_count,
            "evidence_state": "UNRESOLVED",
            "qualification_outcome": "NOT_EVALUATED",
            "evidence_state_reasons": [],
            "adapter_command_identity": launched.get("command_identity"),
            "runtime_observation": runtime_observation,
        }
        (out / "summary.json").write_text(json.dumps(preliminary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")

        missing_artifacts = core70.validate_required_artifacts(out, requirements)
        missing_oracles = core70.validate_required_oracles(out, requirements)
        state, reasons = core70.run_evidence_state(
            execution_ok=execution_ok,
            profile_errors=profile_errors,
            event_errors=event_errors,
            completeness_errors=completeness_errors,
            catalog_ok=bool(catalog.get("ok")),
            terminal_exists=terminal_exists,
            final_result_exists=final_result_exists,
            missing_artifacts=missing_artifacts,
            missing_oracles=missing_oracles,
        )
        preliminary.update({
            "evidence_state": state,
            "evidence_state_reasons": reasons,
            "missing_required_artifacts": missing_artifacts,
            "missing_required_oracles": missing_oracles,
            "profile_claim_errors": profile_errors,
            "normalized_event_errors": event_errors,
            "normalization_completeness_errors": completeness_errors,
        })
        (out / "summary.json").write_text(json.dumps(preliminary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        if state == "COMPLETE_ADMISSIBLE":
            core70.write_evidence_integrity(out, requirements)
        return preliminary


def matrix_plan(episodes: dict[str, dict[str, Any]], arm_names: list[str], only: list[str]) -> list[dict[str, Any]]:
    plan = []
    for episode_index, (episode_id, episode) in enumerate(episodes.items()):
        if only and episode_id not in only:
            continue
        for rep in range(int(episode.get("replicates", 1))):
            order = list(arm_names) if (episode_index + rep) % 2 == 0 else list(reversed(arm_names))
            plan.append({"episode_id": episode_id, "rep": rep, "order": order})
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("episode", "matrix"):
        command = sub.add_parser(name)
        command.add_argument("--corpus", type=Path, required=True)
        command.add_argument("--arms-manifest", type=Path, required=True)
        command.add_argument("--arm", action="append", required=True, help="arm name from prepared arms manifest")
        command.add_argument("--out", type=Path, required=True)
        command.add_argument("--profile", type=Path, required=True)
        command.add_argument("--capabilities", type=Path, required=True)
        command.add_argument("--requirements", type=Path, required=True)
        command.add_argument("--adapter", default="claude")
        command.add_argument("--oracles", type=Path, default=None, help="custodian oracle root (post-run only)")
        command.add_argument("--mode", choices=("probe", "qualification"), default="probe")
        command.add_argument("--profile-admission", type=Path, default=None)
        if name == "episode":
            command.add_argument("--id", required=True)
            command.add_argument("--rep", type=int, default=0)
        else:
            command.add_argument("--parallel", type=int, default=4, help="number of episode/replicate pairs in flight")
            command.add_argument("--only", action="append", default=[])
    args = parser.parse_args(argv)

    adapter = load_adapter(args.adapter)
    profile_bundle = core70.load_profile(args.profile, args.capabilities)
    if profile_bundle.profile["adapter_id"] != adapter.ADAPTER_ID:
        raise core70.ContractError(
            f"profile adapter_id {profile_bundle.profile['adapter_id']!r} != loaded adapter {adapter.ADAPTER_ID!r}"
        )
    arms, arms_manifest_sha = load_arms_manifest(args.arms_manifest)
    requested = list(args.arm)
    if len(set(requested)) != len(requested):
        raise core70.ContractError("duplicate --arm values are not allowed")
    missing_arms = [name for name in requested if name not in arms]
    if missing_arms:
        raise core70.ContractError(f"requested arms are absent from manifest: {missing_arms}")
    dists = {name: resolve_arm_dist(arms[name]) for name in requested}
    episodes = {episode["id"]: episode for episode in load_manifest(args.corpus)}

    if args.cmd == "episode":
        if args.id not in episodes:
            raise core70.ContractError(f"unknown episode {args.id!r}")
        if len(requested) != 1:
            raise core70.ContractError("episode mode requires exactly one --arm")
        arm_name = requested[0]
        episode = episodes[args.id]
        requirements = core70.load_requirements(args.requirements, episode["id"])
        identity = run_identity(
            corpus=args.corpus,
            episode=episode,
            arm=arms[arm_name],
            arms_manifest_sha256=arms_manifest_sha,
            dist=dists[arm_name],
            profile_bundle=profile_bundle,
            profile_path=args.profile,
            capability_path=args.capabilities,
            requirements=requirements,
            requirements_root=args.requirements,
            adapter_module=adapter,
            oracles=args.oracles,
            mode=args.mode,
            admission=args.profile_admission,
            rep=args.rep,
            pair_order=[arm_name],
        )
        target = args.out / f"{args.id}-{arm_name}-r{args.rep}"
        if args.mode == "probe" and core70.cache_valid(target, identity, requirements):
            summary = core70.load_json(target / "summary.json")
        else:
            summary = run_episode(
                corpus=args.corpus,
                episode=episode,
                arm=arms[arm_name],
                arms_manifest_sha256=arms_manifest_sha,
                dist=dists[arm_name],
                out=target,
                profile_bundle=profile_bundle,
                profile_path=args.profile,
                capability_path=args.capabilities,
                requirements=requirements,
                requirements_root=args.requirements,
                adapter_module=adapter,
                oracles=args.oracles,
                mode=args.mode,
                admission=args.profile_admission,
                identity=identity,
                pair_order=[arm_name],
            )
        print(json.dumps({
            "run": target.name,
            "evidence_state": summary["evidence_state"],
            "qualification_outcome": summary["qualification_outcome"],
            "run_identity_sha256": summary["run_identity_sha256"],
        }))
        return 0 if summary["evidence_state"] == "COMPLETE_ADMISSIBLE" else 2

    plan = matrix_plan(episodes, requested, args.only)
    args.out.mkdir(parents=True, exist_ok=True)
    plan_record = {
        "schema": 2,
        "profile_key_sha256": profile_bundle.profile_key_sha256,
        "execution_mode": args.mode,
        "parallel_pairs": args.parallel,
        "pairs": plan,
    }
    (args.out / "matrix-plan.json").write_text(json.dumps(plan_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def run_pair(item: dict[str, Any]) -> list[dict[str, Any]]:
        episode = episodes[item["episode_id"]]
        rep = item["rep"]
        requirements = core70.load_requirements(args.requirements, episode["id"])
        results = []
        for arm_name in item["order"]:
            target = args.out / f"{episode['id']}-{arm_name}-r{rep}"
            identity = run_identity(
                corpus=args.corpus,
                episode=episode,
                arm=arms[arm_name],
                arms_manifest_sha256=arms_manifest_sha,
                dist=dists[arm_name],
                profile_bundle=profile_bundle,
                profile_path=args.profile,
                capability_path=args.capabilities,
                requirements=requirements,
                requirements_root=args.requirements,
                adapter_module=adapter,
                oracles=args.oracles,
                mode=args.mode,
                admission=args.profile_admission,
                rep=rep,
                pair_order=item["order"],
            )
            if args.mode == "probe" and core70.cache_valid(target, identity, requirements):
                summary = core70.load_json(target / "summary.json")
                results.append({"run": target.name, "evidence_state": summary["evidence_state"], "cache": "reused-exact"})
                continue
            try:
                summary = run_episode(
                    corpus=args.corpus,
                    episode=episode,
                    arm=arms[arm_name],
                    arms_manifest_sha256=arms_manifest_sha,
                    dist=dists[arm_name],
                    out=target,
                    profile_bundle=profile_bundle,
                    profile_path=args.profile,
                    capability_path=args.capabilities,
                    requirements=requirements,
                    requirements_root=args.requirements,
                    adapter_module=adapter,
                    oracles=args.oracles,
                    mode=args.mode,
                    admission=args.profile_admission,
                    identity=identity,
                    pair_order=item["order"],
                )
                results.append({"run": target.name, "evidence_state": summary["evidence_state"], "cache": "fresh"})
            except Exception as exc:
                args.out.mkdir(parents=True, exist_ok=True)
                (args.out / f"{target.name}.error.txt").write_text(repr(exc), encoding="utf-8")
                results.append({"run": target.name, "evidence_state": "EXECUTION_ERROR", "cache": "fresh"})
        return results

    any_non_complete = False
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for pair_results in pool.map(run_pair, plan):
            for row in pair_results:
                if row["evidence_state"] != "COMPLETE_ADMISSIBLE":
                    any_non_complete = True
                print(json.dumps(row), flush=True)
    return 2 if any_non_complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
