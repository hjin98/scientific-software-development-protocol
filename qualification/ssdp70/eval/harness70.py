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


def load_adapter(name: str):
    if not name or any(part in {"", ".", ".."} for part in name.split(".")):
        raise core70.ContractError(f"invalid adapter name {name!r}")
    module = importlib.import_module(f"adapters.{name}")
    for attr in ("ADAPTER_ID", "install_skills", "launch", "normalize", "final_result", "catalog_isolation", "owner_reads", "prepare_prompt", "clean_env"):
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
    tools = project / "tools"
    tools.mkdir(exist_ok=True)
    for name in ("delegate.py", "issues.py"):
        src = HERE / "stub_tools" / name
        if src.is_file():
            shutil.copy2(src, tools / name)
    if not (project / ".git").is_dir():
        subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    info = project / ".git" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "exclude").write_text("__pycache__/\n*.pyc\n.claude/\n", encoding="utf-8")
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
        "profile_admission_sha256": core70.sha256_file(admission) if admission is not None else None,
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
    )
    if admission_errors:
        raise core70.ContractError("; ".join(admission_errors))

    claims = episode.get("claims") or []
    if not isinstance(claims, list) or not all(isinstance(x, str) and x for x in claims):
        raise core70.ContractError(f"episode {episode['id']} claims must be a list of strings")
    profile_errors = core70.profile_claim_errors(profile_bundle, claims)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "run-identity.json").write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "profile-snapshot.json").write_text(json.dumps(profile_bundle.profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "capability-manifest-snapshot.json").write_text(json.dumps(profile_bundle.capabilities, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "requirements-snapshot.json").write_text(json.dumps(core70.requirements_snapshot(requirements), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if admission is not None:
        shutil.copy2(admission, out / "profile-admission.json")

    with tempfile.TemporaryDirectory(prefix="ssdp70-") as tmp_name:
        tmp = Path(tmp_name)
        project, stub, log = tmp / "project", tmp / "stub", tmp / "side-effects.jsonl"
        build_project(corpus, episode, project)
        stub.mkdir()
        if episode.get("stub"):
            _yaml_tree_to_json(corpus / "stubs" / episode["stub"], stub)
        log.write_text("", encoding="utf-8")
        adapter_module.install_skills(dist, project)
        prompt = adapter_module.prepare_prompt(profile_bundle.profile, episode.get("entry", "ordinary"), episode["prompt"])
        env = adapter_module.clean_env()
        env.update({
            "SSDP70_STUB_DIR": str(stub),
            "SSDP70_SIDE_EFFECT_LOG": str(log),
            "SSDP70_ACCOUNT": episode.get("account") or "agent-account",
        })
        launched = adapter_module.launch(profile_bundle.profile, prompt, project, env)
        stdout, stderr = launched["stdout"], launched["stderr"]
        (out / "trace.jsonl").write_text(stdout, encoding="utf-8")
        if stderr:
            (out / "stderr.txt").write_text(stderr, encoding="utf-8")
        else:
            (out / "stderr.txt").write_text("", encoding="utf-8")

        events, completeness, normalization_errors, native_event_count = adapter_module.normalize(stdout, identity["identity_sha256"])
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

        subprocess.run(["git", "add", "-A", "-N", "--", ".", ":(exclude).claude"], cwd=project, capture_output=True)
        diff = subprocess.run(
            ["git", "diff", "--", ".", ":(exclude).claude"],
            cwd=project,
            capture_output=True,
            text=True,
        ).stdout
        (out / "diff.patch").write_text(diff, encoding="utf-8")
        shutil.copytree(project, out / "final-tree", ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"))

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
            "owner_read_sequences": adapter_module.owner_reads(events, OWNER),
            "normalized_event_count": len(events),
            "native_event_count": native_event_count,
            "evidence_state": "UNRESOLVED",
            "qualification_outcome": "NOT_EVALUATED",
            "evidence_state_reasons": [],
            "adapter_command_identity": launched.get("command_identity"),
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
        if core70.cache_valid(target, identity):
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
            if core70.cache_valid(target, identity):
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
