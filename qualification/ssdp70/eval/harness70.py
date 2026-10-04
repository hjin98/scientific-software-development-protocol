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
import inspect
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import package_ledger  # noqa: E402

OWNER = "scientific-inspectability-and-initiative.md"
# Harness-owned git exclude for the run project. It is restored before the diff is computed so that
# neither the runtime nor the executor can hide a path from the diff handed to the oracles.
# Harness-owned generic exclusions. Provider-specific control paths (for example a runtime's
# project-local settings or MCP configuration) are supplied by the adapter through
# `project_control_paths`; the harness never hard-codes a provider path here.
PROJECT_GIT_EXCLUDE_BASE = "__pycache__/\n*.pyc\n.qualification-tmp/\n"
FINAL_TREE_IGNORE_BASE = (".git", ".qualification-tmp", "__pycache__")


def _exact_top_level_names(names: Any) -> list[str]:
    result: list[str] = []
    for name in names:
        if (
            not isinstance(name, str)
            or not name
            or "/" in name
            or name in {".", ".."}
            or any(ch in name for ch in "*?[]")
        ):
            raise core70.ContractError(f"provider control path {name!r} is not an exact top-level name")
        result.append(name)
    if len(result) != len(set(result)):
        raise core70.ContractError("provider control paths contain duplicates")
    return result


def project_git_exclude(control_names: list[str]) -> str:
    return PROJECT_GIT_EXCLUDE_BASE + "".join(f"{name}\n" for name in control_names)


def final_tree_ignore(control_names: list[str]) -> tuple[str, ...]:
    return FINAL_TREE_IGNORE_BASE + tuple(control_names)


def load_adapter(name: str):
    if not name or any(part in {"", ".", ".."} for part in name.split(".")):
        raise core70.ContractError(f"invalid adapter name {name!r}")
    module = importlib.import_module(f"adapters.{name}")
    for attr in ("ADAPTER_ID", "install_skills", "launch", "normalize", "final_result", "catalog_isolation", "owner_reads", "prepare_prompt", "clean_env", "runtime_observation", "realize_containment", "project_control_paths"):
        if not hasattr(module, attr):
            raise core70.ContractError(f"adapter {name!r} is missing {attr}")
    return module


def _accepts(fn: Any, name: str) -> bool:
    """True when an optional provider-neutral hook argument is declared by the adapter function."""
    try:
        return name in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False


def _control_snapshot(project: Path, control_names: list[str]) -> dict[str, Any]:
    """Exact type + content/recursive digest of every adapter-declared project control path."""
    rows: dict[str, Any] = {}
    for name in control_names:
        path = project / name
        if path.is_symlink():
            rows[name] = {"present": True, "type": "symlink", "target": os.readlink(path)}
        elif path.is_file():
            rows[name] = {"present": True, "type": "file", "sha256": core70.sha256_file(path)}
        elif path.is_dir():
            rows[name] = {"present": True, "type": "directory", "sha256": core70.sha256_tree(path)}
        else:
            rows[name] = {"present": False, "type": None}
    return rows


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


def build_project(corpus: Path, episode: dict[str, Any], project: Path, control_names: list[str]) -> None:
    fixture = corpus / "fixtures" / episode["fixture"]
    if not fixture.is_dir():
        raise core70.ContractError(f"fixture directory is missing for {episode['id']}")
    project.mkdir(parents=True)
    script = fixture / "build_history.sh"
    if script.is_file():
        subprocess.run(["bash", str(script)], cwd=project, check=True, capture_output=True)
        # History may create aliases to custody files. Refuse shared inodes before
        # copytree can overwrite them or permission normalization can thaw them.
        for root, _, files in os.walk(project):
            for name in files:
                path = Path(root) / name
                metadata = path.lstat()
                if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink > 1:
                    raise core70.ContractError(
                        f"fixture history contains a hard-linked file: {path.relative_to(project)}"
                    )
    if (fixture / "project").is_dir():
        shutil.copytree(
            fixture / "project",
            project,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        # Custody modes protect the fixture, not its mutable working copy.
        # Add owner access only; preserve executable bits and other permissions.
        # Do not follow links created by a fixture's history script.
        for root, dirs, files in os.walk(project):
            directory = Path(root)
            directory.chmod(stat.S_IMODE(directory.stat().st_mode) | stat.S_IRWXU)
            for name in files:
                path = directory / name
                if not path.is_symlink():
                    path.chmod(stat.S_IMODE(path.stat().st_mode) | stat.S_IRUSR | stat.S_IWUSR)
    if not (project / ".git").is_dir():
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    info = project / ".git" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "exclude").write_text(project_git_exclude(control_names), encoding="utf-8")
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


def _final_tree_ignore(project: Path, exclude_paths: list[str], control_names: list[str]):
    """copytree ignore: the fixed patterns plus EXACTLY the verified runtime placeholders (top-level names)."""
    _exact_top_level_names(exclude_paths)
    exact = set(exclude_paths)
    generic = shutil.ignore_patterns(*final_tree_ignore(control_names))
    project_resolved = project.resolve()

    def ignore(directory, names):
        ignored = set(generic(directory, names))
        if Path(directory).resolve() == project_resolved:
            ignored |= exact & set(names)
        return ignored

    return ignore


GIT_SAFE_CONFIG = "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = true\n"


def _git_env() -> dict[str, str]:
    """Environment for every harness-side git command over executor-controlled repository state."""
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": "/nonexistent-home",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0",
    }


def _git(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", *args],
        cwd=project, env=_git_env(), capture_output=True, text=True,
    )


def _write_regular_file(path: Path, text: str) -> None:
    """Write without following an executor-planted symlink (the supervisor never writes through one)."""
    if path.is_symlink() or path.exists():
        path.unlink()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


def project_git_state_errors(project: Path) -> list[str]:
    """The executor owns the project's `.git`; the supervisor runs git over it only if it is plain."""
    errors: list[str] = []
    git_dir = project / ".git"
    if git_dir.is_symlink() or not git_dir.is_dir():
        return [".git is not a plain directory in the executor project (symlink/file redirects git elsewhere)"]
    for rel in ("info", "hooks", "objects", "refs"):
        path = git_dir / rel
        if path.is_symlink():
            errors.append(f".git/{rel} is a symlink planted in the executor project")
    return errors


def capture_project_state(project: Path, out: Path, runtime_exclusions: list[str], control_names: list[str]) -> str:
    """Write diff.patch and final-tree for the oracles.

    The harness-owned git exclude is restored first (the runtime appends its stub names to it and the
    executor may edit it), then only the verified runtime placeholders are hidden, by exact pathspec and
    exact top-level name. Anything else the run left in the project stays visible to the oracles.

    The executor controls `.git` (config, attributes, symlinks). The supervisor therefore never writes
    through a symlink there, retains the executor's raw config as evidence, replaces the config with a
    harness-owned one before running git, and disables config-borne command execution (fsmonitor, hooks,
    external diff, textconv); a `.git` that is not a plain directory yields an empty diff and is
    reported by `project_git_state_errors`.
    """
    tree_ignore = _final_tree_ignore(project, runtime_exclusions, control_names)
    pathspecs = [".", *(f":(exclude){name}" for name in control_names), *(f":(exclude){name}" for name in runtime_exclusions)]
    diff = ""
    if not project_git_state_errors(project):
        raw_config = project / ".git" / "config"
        if raw_config.is_symlink():
            (out / "project-git-config.raw").write_text("symlink -> " + os.readlink(raw_config) + "\n", encoding="utf-8")
        elif raw_config.is_file():
            (out / "project-git-config.raw").write_bytes(raw_config.read_bytes())
        _write_regular_file(raw_config, GIT_SAFE_CONFIG)
        attributes = project / ".git" / "info" / "attributes"
        if attributes.is_symlink() or attributes.exists():
            attributes.unlink()
        _write_regular_file(project / ".git" / "info" / "exclude", project_git_exclude(control_names))
        _git(project, "add", "-A", "-N", "--", *pathspecs)
        diff = _git(project, "diff", "--no-ext-diff", "--no-textconv", "--", *pathspecs).stdout
    (out / "diff.patch").write_text(diff, encoding="utf-8")
    # Executor-created symlinks are preserved as symlinks and never followed: following one would copy
    # arbitrary host files (or the whole host filesystem) into the evidence/oracle view.
    shutil.copytree(project, out / "final-tree", ignore=tree_ignore, symlinks=True)
    links = []
    root = project.resolve()
    for path in sorted(project.rglob("*")):
        if path.is_symlink():
            target = os.readlink(path)
            resolved = (path.parent / target).resolve() if not os.path.isabs(target) else Path(target)
            inside = resolved == root or root in resolved.parents
            links.append({"path": path.relative_to(project).as_posix(), "target": target, "resolves_inside_project": inside})
    (out / "final-tree-symlinks.json").write_text(json.dumps({"schema": 1, "symlinks": links}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
    state = terminations[-1].get("payload", {}).get("native_return_state")
    if not isinstance(state, dict) or not isinstance(state.get("is_error"), bool):
        return True, False
    return True, not state["is_error"]


def _create_realization_directory(out: Path, adapter_module) -> None:
    """Atomically claim a fresh output directory before the harness writes any run evidence."""
    out = Path(out)
    if os.path.lexists(out):
        raise core70.ContractError(f"realization collision: output directory already exists: {out}")
    allowed_roots = getattr(adapter_module, "RUN_REALIZATION_ROOTS", ())
    if allowed_roots:
        resolved_out = out.resolve(strict=False)
        allowed = False
        for root in allowed_roots:
            root = Path(root).resolve()
            try:
                if not resolved_out.relative_to(root).parts:
                    continue
                allowed = True
                break
            except ValueError:
                continue
        if not allowed:
            raise core70.ContractError(
                f"runtime adapter realization path must be beneath its approved external workspace: {out}"
            )
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        out.mkdir()
    except FileExistsError as exc:
        raise core70.ContractError(f"realization collision: output directory already exists: {out}") from exc


def entry_stratum(episode: dict[str, Any], profile: dict[str, Any]) -> str:
    # Legacy prose-pinned development inputs are ordinary instructed entry.
    # A declared deterministic input still has to prove the declared mechanism.
    return "deterministic" if episode.get("entry", "ordinary").startswith("pinned:") and profile.get("activation_mechanism") in ("runtime-command", "harness-injection") else "ordinary"


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
    accounting_manifest = episode.get("accounting_manifest")
    if accounting_manifest is not None:
        errors = core70.campaign_manifest_errors(accounting_manifest)
        if errors:
            raise core70.ContractError("; ".join(errors))
        run_slot = f"{episode['id']}-{arm['name']}-r{rep}"
        matching = [row for row in accounting_manifest["runs"] if row["id"] == run_slot]
        if len(matching) != 1:
            raise core70.ContractError("run is not enumerated in the frozen accounting manifest")
        declaration = matching[0]
        subject = {"commit": arm["commit"], "package_sha256": arm["dist_tree_sha256"]}
        if declaration["subject"] != subject or declaration["profile_key_sha256"] != profile_bundle.profile_key_sha256 or declaration["scoring_manifest_sha256"] != requirements.scoring_manifest_digest:
            raise core70.ContractError("launch does not match frozen subject/profile/scoring declaration")
        stratum = entry_stratum(episode, profile_bundle.profile)
        if declaration["entry_stratum"] != stratum:
            raise core70.ContractError("entry stratum differs from launch declaration")
        digest = core70.stable_json_sha256(accounting_manifest)
        scope = {"purpose": accounting_manifest["purpose"], "scope_id": accounting_manifest["scope_id"],
                 "manifest_sha256": digest, "scoring_manifest_sha256": requirements.scoring_manifest_digest}
        if scope["purpose"] == "qualification":
            scope.update({"campaign_record_sha256": digest, "family_record_sha256": accounting_manifest["family_record_sha256"],
                          "primary_family_id": accounting_manifest["family"]["family_id"]})
            if "integrity_test_campaign" in accounting_manifest:
                scope["integrity_test_campaign"] = accounting_manifest["integrity_test_campaign"]
        episode = {**episode, "accounting": scope}
    fixture = corpus / "fixtures" / episode["fixture"]
    stub = corpus / "stubs" / episode["stub"] if episode.get("stub") else None
    episode_oracles = oracles / episode["id"] if oracles is not None else None
    identity = {
        "schema": 2,
        "accounting_manifest": accounting_manifest,
        "entry_stratum": entry_stratum(episode, profile_bundle.profile),
        "activation_mechanism": profile_bundle.profile.get("activation_mechanism", "ordinary-read"),
        "declared_root": episode.get("entry", "ordinary").split(":", 1)[-1] if episode.get("entry", "ordinary").startswith("pinned:") else None,
        "accounting": episode.get("accounting") or {
            "purpose": "qualification" if mode == "qualification" else "development",
            "scope_id": "development:" + core70.sha256_file(corpus / "manifest.yaml"),
            "manifest_sha256": core70.sha256_file(corpus / "manifest.yaml"),
            "scoring_manifest_sha256": requirements.scoring_manifest_digest,
        },
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
    support_files = getattr(adapter_module, "support_files", None)
    if support_files is not None:
        # Provider principals (for example an observation/bridge process) are part of the
        # execution profile's provenance identity. Adapters without any add nothing.
        support = {name: core70.sha256_file(Path(path).resolve()) for name, path in sorted(support_files().items())}
        if support:
            identity["adapter_support_sha256"] = support
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

    accounting_errors = core70.validate_accounting_identity(identity)
    if accounting_errors:
        raise core70.ContractError("; ".join(accounting_errors))
    declarations = (identity.get("accounting_manifest") or {}).get("runs", [])
    slot = f"{episode['id']}-{arm['name']}-r{identity['replicate']}"
    declared_faults = [row.get("fault") for row in declarations if row["id"] == slot]
    fault = declared_faults[0] if declared_faults and declared_faults[0] in getattr(adapter_module, "INTEGRITY_FAULTS", ()) else None
    if fault is not None:
        scope = identity["accounting"]
        if scope["purpose"] != "oracle-integrity" and not scope.get("integrity_test_campaign"):
            raise core70.ContractError("fault injection is limited to predeclared integrity-suite realizations")
        declarations = identity["accounting_manifest"]["runs"]
        slot = f"{episode['id']}-{arm['name']}-r{identity['replicate']}"
        if not any(row["id"] == slot and row.get("fault") == fault for row in declarations):
            raise core70.ContractError("fault is not frozen in the launch manifest")
    if mode == "qualification" and adapter_module.ADAPTER_ID == "omp-json-v2":
        if profile_bundle.profile.get("runtime_mode") != "rpc":
            raise core70.ContractError("OMP qualification requires RPC mode")
    _create_realization_directory(out, adapter_module)
    (out / "run-identity.json").write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if identity.get("accounting_manifest") is not None:
        (out / "accounting-manifest.json").write_text(json.dumps(identity["accounting_manifest"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "profile-snapshot.json").write_text(json.dumps(profile_bundle.profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "capability-manifest-snapshot.json").write_text(json.dumps(profile_bundle.capabilities, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "requirements-snapshot.json").write_text(json.dumps(core70.requirements_snapshot(requirements), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if admission is not None:
        core70.snapshot_profile_admission(admission, out, role="executor", prefix="profile-admission")

    prelaunch_refusal_type = getattr(adapter_module, "PrelaunchRefusal", ())

    def record_prelaunch_refusal(phase: str, exc: Exception) -> dict[str, Any]:
        refusal = {
            "schema": 1,
            "phase": phase,
            "exception_type": type(exc).__name__,
            "reason": str(exc),
            "subject_launched": False,
        }
        (out / "prelaunch-refusal.json").write_text(
            json.dumps(refusal, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        summary = {
            "schema": 2,
            "episode": episode["id"],
            "arm": arm["name"],
            "subject_commit": arm["commit"],
            "execution_mode": mode,
            "accounting": identity["accounting"],
            "execution_returncode": None,
            "execution_ok": False,
            "profile_key_sha256": profile_bundle.profile_key_sha256,
            "run_identity_sha256": identity["identity_sha256"],
            "normalized_event_count": 0,
            "native_event_count": 0,
            "evidence_state": "EXECUTION_ERROR",
            "qualification_outcome": "NOT_EVALUATED",
            "evidence_state_reasons": [
                f"adapter refused during {phase} before subject launch",
                f"{type(exc).__name__}: {exc}",
            ],
            "prelaunch_refusal": refusal,
        }
        (out / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return summary

    # The adapter owns which provider control paths are harness-owned and must stay out of the
    # oracle diff/final tree. The harness only accepts exact top-level names.
    control_names = _exact_top_level_names(adapter_module.project_control_paths(profile_bundle.profile))

    runtime_state_root = getattr(adapter_module, "RUNTIME_STATE_ROOT", None)
    if runtime_state_root is not None:
        runtime_state_root = Path(runtime_state_root)
        runtime_state_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ssdp70-", dir=runtime_state_root) as tmp_name:
        tmp = Path(tmp_name)
        project = tmp / "project"
        private = tmp / "harness-private"
        layout = core70.private_mcp_paths(private)
        stub, log = layout["stub"], layout["log"]
        runtime_home = private / "runtime-home"
        runtime_tmp = project / ".qualification-tmp"
        build_project(corpus, episode, project, control_names)
        # A provider control path may never shadow fixture content: it must be absent from the
        # fixture baseline so that excluding it from the oracle views hides nothing the fixture owns.
        shadowed = [name for name in control_names if os.path.lexists(project / name)]
        if shadowed:
            raise core70.ContractError(
                f"adapter control path(s) {shadowed} already exist in the fixture baseline; refusing to hide fixture content"
            )
        private.mkdir()
        stub.mkdir()
        if episode.get("stub"):
            _yaml_tree_to_json(corpus / "stubs" / episode["stub"], stub)
        log.write_text("", encoding="utf-8")
        log.chmod(0o600)
        mcp_servers = profile_bundle.profile.get("mcp_servers") or []
        if mcp_servers or adapter_module.ADAPTER_ID == "omp-json-v2":
            mcp_server = layout["server"]
            shutil.copy2(HERE / "stub_tools" / "mediator.py", mcp_server)
            mcp_server.chmod(0o500)
            account_file = layout["account"]
            account_file.write_text((episode.get("account") or "agent-account") + "\n", encoding="utf-8")
            account_file.chmod(0o400)
        runtime_home.mkdir()
        runtime_tmp.mkdir()
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
        # The adapter owns where its runtime discovers the installed protocol package. The harness
        # hashes exactly the root the adapter reports, before and after execution, and never assumes
        # a provider-specific directory such as `.claude/skills`.
        installed_skills = Path(adapter_module.install_skills(dist, project, env))
        installed_digest = core70.sha256_tree(installed_skills)
        if installed_digest != arm["dist_tree_sha256"]:
            raise core70.ContractError(
                f"installed protocol package digest mismatch: {installed_digest} != {arm['dist_tree_sha256']}"
            )
        try:
            containment = adapter_module.realize_containment(profile_bundle.profile, project, env)
        except Exception as exc:
            return record_prelaunch_refusal("realize_containment", exc)
        (out / "containment-realization.json").write_text(
            json.dumps(containment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        control_before = _control_snapshot(project, control_names)
        runtime_baseline_fn = getattr(adapter_module, "runtime_entry_baseline", None)
        runtime_baseline = runtime_baseline_fn(profile_bundle.profile, project) if runtime_baseline_fn is not None else None
        try:
            launch_kwargs = {"integrity_fault": fault} if fault is not None else {}
            launched = adapter_module.launch(profile_bundle.profile, prompt, project, env, **launch_kwargs)
        except Exception as exc:
            if prelaunch_refusal_type and isinstance(exc, prelaunch_refusal_type):
                return record_prelaunch_refusal("launch", exc)
            raise
        stdout, stderr = launched["stdout"], launched["stderr"]
        (out / "trace.jsonl").write_text(stdout, encoding="utf-8")
        adapter_artifacts = launched.get("adapter_artifacts") or {}
        if adapter_artifacts:
            artifact_dir = out / "adapter-artifacts"
            artifact_dir.mkdir()
            for artifact_name, artifact_body in sorted(adapter_artifacts.items()):
                if "/" in artifact_name or artifact_name in {"", ".", ".."}:
                    raise core70.ContractError(f"invalid adapter artifact name {artifact_name!r}")
                if isinstance(artifact_body, bytes):
                    (artifact_dir / artifact_name).write_bytes(artifact_body)
                else:
                    (artifact_dir / artifact_name).write_text(str(artifact_body), encoding="utf-8")
        if stderr:
            (out / "stderr.txt").write_text(stderr, encoding="utf-8")
        else:
            (out / "stderr.txt").write_text("", encoding="utf-8")

        normalization_context = {
            "project": str(project),
            "skills_root": str(installed_skills),
            "package_identity": dict(identity["subject"]),
            "entry": episode.get("entry", "ordinary"),
            "profile": profile_bundle.profile,
            "adapter_artifacts": dict(adapter_artifacts),
            "runtime_home": str(runtime_home),
            "prompt": prompt,
        }
        events, completeness, normalization_errors, native_event_count = adapter_module.normalize(
            stdout, identity["identity_sha256"], normalization_context
        )
        if _accepts(adapter_module.runtime_observation, "context"):
            runtime_observation = adapter_module.runtime_observation(stdout, normalization_context)
        else:
            runtime_observation = adapter_module.runtime_observation(stdout)
        if isinstance(runtime_observation, dict):
            # Adapters that assemble their observation from trusted principals report contradictory,
            # missing or unbound observation here; the core treats each entry as a profile error.
            profile_errors.extend(str(item) for item in runtime_observation.get("observation_errors") or [])
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
        control_after = _control_snapshot(project, control_names)
        control_changes = sorted(name for name in control_names if control_before.get(name) != control_after.get(name))
        (out / "project-control-record.json").write_text(
            json.dumps({
                "schema": 1,
                "control_paths": control_names,
                "before_launch": control_before,
                "after_run": control_after,
                "changed": control_changes,
                "mutation_policy": getattr(adapter_module, "PROJECT_CONTROL_MUTATION_POLICY", "adapter-classified"),
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if control_changes and getattr(adapter_module, "PROJECT_CONTROL_MUTATION_POLICY", "adapter-classified") == "immutable":
            profile_errors.append(f"immutable provider control path(s) changed during execution: {control_changes}")
        post_integrity = getattr(adapter_module, "post_run_integrity", None)
        if post_integrity is not None:
            profile_errors.extend(post_integrity(profile_bundle.profile, project, env, containment))
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
        owner_read_sequences = adapter_module.owner_reads(events, OWNER)
        # Supervisor package-access accounting (D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION).
        ledger_hook = getattr(adapter_module, "package_access_ledger", None)
        accounting = None
        supplied_owner: list[int] = []
        if ledger_hook is not None:
            ledger_bundle = ledger_hook(adapter_artifacts, profile_bundle.profile)
            accounting = package_ledger.account(ledger_bundle.get("ledger"), ledger_bundle.get("cut_ns"), events,
                                                installed_skills, extra_errors=list(ledger_bundle.get("errors") or []))
            if accounting["exact"]:
                for rel, row in accounting["supplied"].items():
                    if rel.endswith("/references/" + OWNER):
                        supplied_owner.extend(row["sequences"])
                owner_read_sequences = sorted(set(owner_read_sequences) | set(supplied_owner))
        profile_errors.extend(core70.validate_claim_observability(
            events, claims,
            [{"rel": rel, **row} for rel, row in (accounting["supplied"].items() if accounting and accounting["exact"] else [])]))
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

        profile_errors.extend(project_git_state_errors(project))
        capture_project_state(project, out, runtime_exclusions, control_names)

        run_oracles(oracles, episode["id"], requirements, out)

        terminal_exists, terminal_ok = _termination_state(events)
        final_result_exists = any(e.get("kind") == "final_result" for e in events)
        catalog = adapter_module.catalog_isolation(events)
        execution_ok = bool(launched["returncode"] == 0 and terminal_exists and terminal_ok)

        consumed_files = {}
        for event in events:
            payload = event.get("payload", {})
            if event.get("kind") == "root_selection" and payload.get("delivery", {}).get("delivered"):
                consumed_files[f"{payload['logical_root']}/SKILL.md"] = payload["delivery"]["installed_skill_bytes"]
            if event.get("kind") == "resource_access" and payload.get("result_status") == "result":
                consumed = payload.get("consumed_resource", {})
                if consumed.get("match") in ("exact", "partial") and payload.get("resolved_package_identity"):
                    path = payload.get("resolved_resource_path")
                    if isinstance(path, str) and path.startswith("/opt/ssdp/skills/"):
                        consumed_files[path.removeprefix("/opt/ssdp/skills/")] = payload["resource_bytes"]
        # Exact package consumption needs complete observation of package access, not just native
        # read events. An adapter with a supervisor-owned package-access ledger supplies it
        # (D3-PACKAGE-ACCESS-LEDGER-OBSERVATION-DECISION); without one, any process execution
        # leaves the package read set unobserved and no exact byte total or negative owner-read
        # conclusion is published.
        process_events = [event["sequence"] for event in events
            if event.get("kind") == "tool_action" and event.get("status") == "result"
            and "process_execution" in event.get("payload", {}).get("semantic_capability_classes", [])]
        if accounting is not None:
            observation_exact = bool(accounting["exact"])
            if observation_exact:
                for rel, row in accounting["supplied"].items():
                    consumed_files.setdefault(rel, row["bytes"])
            reason = None if observation_exact else "package-access observation is not exact: " + "; ".join(accounting["reasons"])
            unresolved_events = [] if observation_exact else process_events
        else:
            observation_exact = not process_events
            reason = None if observation_exact else "process execution lacks complete SSDP resource-read observation"
            unresolved_events = process_events
        resource_observation = {"exact": observation_exact, "unresolved_process_events": unresolved_events,
            "reason": reason, "mechanism": None if accounting is None else accounting["mechanism"],
            "accounting": accounting}
        sensitive_claims = any(any(token in str(claim).lower() for token in
            ("owner", "t1", "t7", "t8", "burden", "active-byte")) for claim in claims)
        if not observation_exact and sensitive_claims:
            profile_errors.append(reason)
        opaque_package_access = not observation_exact
        declared_root = identity.get("declared_root")
        entrypoint = installed_skills / declared_root / "SKILL.md" if declared_root else None
        owner = installed_skills / declared_root / "references" / OWNER if declared_root else None
        preliminary = {
            "schema": 2,
            "episode": episode["id"],
            "arm": arm["name"],
            "subject_commit": arm["commit"],
            "execution_mode": mode,
            "execution_returncode": launched["returncode"],
            "execution_ok": execution_ok,
            "accounting": identity["accounting"],
            "wall_s": launched["wall_s"],
            "report_bytes": len(final_text.encode("utf-8")),
            "active_ssdp_files": consumed_files,
            "active_ssdp_bytes": None if opaque_package_access else sum(consumed_files.values()),
            "resource_observation": resource_observation,
            "observed_ssdp_bytes_lower_bound": sum(consumed_files.values()),
            "installed_entrypoint_bytes": entrypoint.stat().st_size if entrypoint and entrypoint.is_file() else None,
            "installed_owner_bytes": owner.stat().st_size if owner and owner.is_file() else None,
            "pair_order": pair_order,
            "profile_key_sha256": profile_bundle.profile_key_sha256,
            "run_identity_sha256": identity["identity_sha256"],
            "catalog_isolation": catalog,
            "owner_read_sequences": None if opaque_package_access else owner_read_sequences,
            "normalized_event_count": len(events),
            "native_event_count": native_event_count,
            "evidence_state": "UNRESOLVED",
            "qualification_outcome": "NOT_EVALUATED",
            "evidence_state_reasons": [],
            "adapter_command_identity": launched.get("command_identity"),
            "runtime_observation": runtime_observation,
        }
        (out / "summary.json").write_text(json.dumps(preliminary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")

        if identity["entry_stratum"] == "deterministic":
            activation_fn = getattr(adapter_module, "verify_activation", None)
            if activation_fn is None:
                activation = {"delivered": False, "errors": ["adapter has no trusted request-0 proof"]}
            else:
                observed = adapter_module.Observed(adapter_artifacts, profile_bundle.profile)
                activation = activation_fn(observed, normalization_context)
            preliminary["activation"] = activation
            if not isinstance(activation, dict) or activation.get("delivered") is not True:
                profile_errors.append("deterministic activation failed")

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
        if preliminary.get("activation", {}).get("delivered") is False:
            state = "INADMISSIBLE"
            reasons.append("deterministic activation failed, including termination before request 0")
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
        preliminary["criteria"] = core70.local_criteria(preliminary, identity)
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
        command.add_argument("--accounting-manifest", type=Path, default=None)
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
    if args.mode == "qualification" and args.accounting_manifest is None:
        raise core70.ContractError("qualification requires a frozen campaign/family/accounting manifest")
    if args.accounting_manifest is not None:
        manifest = core70.load_json(args.accounting_manifest)
        for episode in episodes.values():
            episode["accounting_manifest"] = manifest

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
    _create_realization_directory(args.out, adapter)
    plan_record = {
        "schema": 2,
        "profile_key_sha256": profile_bundle.profile_key_sha256,
        "execution_mode": args.mode,
        "parallel_pairs": args.parallel,
        "pairs": plan,
    }
    (args.out / "matrix-plan.json").write_text(json.dumps(plan_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    scheduler_path = args.out / "matrix-scheduler.jsonl"
    scheduler_lock = threading.Lock()

    def scheduler_event(event: str, item: dict[str, Any], arm: str | None = None) -> None:
        row = {
            "schema": 1,
            "event": event,
            "pair_id": f"{item['episode_id']}-r{item['rep']}",
            "episode_id": item["episode_id"],
            "rep": item["rep"],
            "order": item["order"],
            "arm": arm,
            "monotonic_ns": time.monotonic_ns(),
            "wall_time_ns": time.time_ns(),
        }
        with scheduler_lock:
            with open(scheduler_path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, sort_keys=True) + "\n")

    def run_pair(item: dict[str, Any]) -> list[dict[str, Any]]:
        episode = episodes[item["episode_id"]]
        rep = item["rep"]
        requirements = core70.load_requirements(args.requirements, episode["id"])
        results = []
        scheduler_event("pair_start", item)
        try:
            for arm_name in item["order"]:
                target = args.out / f"{episode['id']}-{arm_name}-r{rep}"
                scheduler_event("arm_start", item, arm_name)
                try:
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
                finally:
                    scheduler_event("arm_end", item, arm_name)
            return results
        finally:
            scheduler_event("pair_end", item)

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
