#!/usr/bin/env python3
"""Independent fail-closed assessment of one Protocol 7 Stage F run.

Assessment consumes only COMPLETE_ADMISSIBLE run evidence, binds evaluator realization
and rubric/key material into an assessment identity, and requires exactly one disposition
for every core-owned expected scoring item. Missing evidence or scoring obligations never
become PASS by omission.
"""
from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402

STANDARD_EVIDENCE = (
    "summary.json",
    "run-identity.json",
    "profile-snapshot.json",
    "capability-manifest-snapshot.json",
    "profile-admission.json",
    "requirements-snapshot.json",
    "evidence-integrity.json",
    "containment-realization.json",
    "final-report.md",
    "diff.patch",
    "side-effects.jsonl",
    "tool-calls.jsonl",
    "trace.jsonl",
    "events.normalized.jsonl",
    "normalization-map.json",
    "oracle.json",
    "stderr.txt",
    "issues-final",
    "oracle-output",
    "final-tree",
)

PROMPT = """You are an independent evaluator. You did not perform this run and must not trust the executor's claims.

Read EVIDENCE-MANIFEST.json first. The run evidence is under run/, the frozen expected scoring items are in
run/requirements-snapshot.json, and custodian key material is under keys/. Score only against those frozen materials.
Do not infer a missing fact from an excerpt. Do not alter evidence and do not use network, shell, skills or agents.

You MUST return exactly one disposition for every expected scoring item, using the exact item id, measure, critical flag,
and an allowed disposition from the manifest. Never omit an item. If applicability or evidence is unresolved, return
"unresolved" when allowed; do not manufacture a pass. The wrapper will reject missing, duplicate, unknown or altered items.

Return strict JSON only, exactly this shape:
{"episode":"...","dispositions":[{"item":"...","measure":"...","result":"pass|fail|unresolved|not-applicable","critical":true,"evidence":"<=40 words"}],"r2_point_index":null,"owner_false_activation":null,"notes":"<=80 words"}
"""


def load_adapter(name: str):
    if not name or any(part in {"", ".", ".."} for part in name.split(".")):
        raise core70.ContractError(f"invalid evaluator adapter name {name!r}")
    module = importlib.import_module(f"adapters.{name}")
    for attr in ("ADAPTER_ID", "launch", "clean_env", "runtime_observation", "realize_containment"):
        if not hasattr(module, attr):
            raise core70.ContractError(f"evaluator adapter {name!r} is missing {attr}")
    return module


def copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def evidence_manifest(root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "EVIDENCE-MANIFEST.json"):
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": core70.sha256_file(path),
        })
    return rows


def prepare_bundle(
    run: Path,
    keys: Path,
    shared_rubric: Path | None,
    requirements: core70.Requirements,
    root: Path,
) -> list[dict[str, Any]]:
    missing_artifacts = core70.validate_required_artifacts(run, requirements)
    missing_oracles = core70.validate_required_oracles(run, requirements)
    if missing_artifacts or missing_oracles:
        raise core70.ContractError(
            f"assessment input is incomplete: missing artifacts={missing_artifacts}, missing oracles={missing_oracles}"
        )
    if not keys.is_dir():
        raise core70.ContractError(f"custodian key directory is unavailable: {keys}")
    key_dst = root / "keys"
    shutil.copytree(keys, key_dst)
    if shared_rubric is not None:
        if not shared_rubric.is_file():
            raise core70.ContractError(f"shared rubric is unavailable: {shared_rubric}")
        shutil.copy2(shared_rubric, root / "shared-rubric.txt")
    run_dst = root / "run"
    run_dst.mkdir()
    names = list(dict.fromkeys((*STANDARD_EVIDENCE, *requirements.artifacts)))
    for name in names:
        src = run / name
        if src.exists():
            copy_item(src, run_dst / name)
    manifest = evidence_manifest(root)
    (root / "EVIDENCE-MANIFEST.json").write_text(
        json.dumps({"schema": 1, "files": manifest}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def result_text(stdout: str) -> tuple[str | None, dict[str, Any] | None]:
    final_event = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            final_event = event
    if final_event is None:
        return None, None
    return final_event.get("result", ""), final_event


def word_count(text: str) -> int:
    return len(text.split())


def validate_verdict(verdict: Any, expected_episode: str, requirements: core70.Requirements) -> list[str]:
    errors: list[str] = []
    if not isinstance(verdict, dict):
        return ["top-level result is not an object"]
    required = {"episode", "dispositions", "r2_point_index", "owner_false_activation", "notes"}
    if set(verdict) != required:
        errors.append(f"top-level keys must be exactly {sorted(required)}")
    if verdict.get("episode") != expected_episode:
        errors.append("episode does not match run summary")
    dispositions = verdict.get("dispositions")
    if not isinstance(dispositions, list):
        errors.append("dispositions is not a list")
    else:
        item_keys = {"item", "measure", "result", "critical", "evidence"}
        for index, item in enumerate(dispositions):
            if not isinstance(item, dict):
                errors.append(f"dispositions[{index}] is not an object")
                continue
            if set(item) != item_keys:
                errors.append(f"dispositions[{index}] keys are invalid")
            evidence = item.get("evidence")
            if not isinstance(evidence, str) or word_count(evidence) > 40:
                errors.append(f"dispositions[{index}].evidence exceeds 40 words or is not text")
        errors.extend(core70.validate_dispositions(dispositions, requirements))
    r2 = verdict.get("r2_point_index")
    if r2 is not None and (not isinstance(r2, int) or isinstance(r2, bool) or r2 < 0):
        errors.append("r2_point_index must be a non-negative integer or null")
    owner_false = verdict.get("owner_false_activation")
    if owner_false is not None and not isinstance(owner_false, bool):
        errors.append("owner_false_activation must be boolean or null")
    notes = verdict.get("notes")
    if not isinstance(notes, str) or word_count(notes) > 80:
        errors.append("notes exceeds 80 words or is not text")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--keys", type=Path, required=True, help="custodian keys/<episode> directory")
    parser.add_argument("--shared-rubric", type=Path, default=None)
    parser.add_argument("--evaluator-profile", type=Path, required=True)
    parser.add_argument("--evaluator-capabilities", type=Path, required=True)
    parser.add_argument("--evaluator-admission", type=Path, required=True)
    parser.add_argument("--adapter", default="claude")
    args = parser.parse_args(argv)

    summary = core70.load_json(args.run / "summary.json")
    run_identity = core70.load_json(args.run / "run-identity.json")
    if not isinstance(summary, dict) or not isinstance(run_identity, dict):
        raise core70.ContractError("run summary or identity is malformed")
    expected_episode = summary.get("episode")
    req_payload = core70.load_json(args.run / "requirements-snapshot.json")
    identity_requirements = run_identity.get("requirements") if isinstance(run_identity.get("requirements"), dict) else {}
    expected_manifest_digests = {
        "required_artifacts": identity_requirements.get("required_artifacts_sha256"),
        "required_oracles": identity_requirements.get("required_oracles_sha256"),
        "expected_scoring_items": identity_requirements.get("expected_scoring_items_sha256"),
    }
    try:
        requirements = core70.requirements_from_snapshot(req_payload, expected_manifest_digests)
        run_errors = core70.validate_complete_run(args.run, run_identity, requirements)
    except core70.ContractError as exc:
        requirements = None
        run_errors = [str(exc)]
    if summary.get("evidence_state") != "COMPLETE_ADMISSIBLE" or run_errors:
        output = {
            "assessment_status": "NOT_EVALUATED",
            "evidence_state": "MALFORMED_EVIDENCE_OR_ASSESSMENT" if run_errors else summary.get("evidence_state"),
            "qualification_outcome": "NOT_EVALUATED",
            "errors": run_errors or ["only COMPLETE_ADMISSIBLE run evidence may enter assessment"],
        }
        (args.run / "assessment.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(output, indent=2))
        return 2
    assert requirements is not None

    evaluator_bundle = core70.load_profile(args.evaluator_profile, args.evaluator_capabilities)
    evaluator_profile_errors = core70.profile_claim_errors(evaluator_bundle, [])
    if evaluator_profile_errors:
        raise core70.ContractError("; ".join(evaluator_profile_errors))
    adapter = load_adapter(args.adapter)
    if evaluator_bundle.profile["adapter_id"] != adapter.ADAPTER_ID:
        raise core70.ContractError(
            f"evaluator profile adapter_id {evaluator_bundle.profile['adapter_id']!r} != {adapter.ADAPTER_ID!r}"
        )
    evaluator_adapter_sha = core70.sha256_file(Path(adapter.__file__).resolve())
    core_sha = core70.sha256_file(Path(core70.__file__).resolve())
    evaluator_admission_before = core70.admission_bundle_sha256(args.evaluator_admission, role="evaluator")
    admission_errors = core70.validate_profile_admission(
        args.evaluator_admission,
        mode="qualification",
        profile_key_sha256=evaluator_bundle.profile_key_sha256,
        adapter_sha256=evaluator_adapter_sha,
        core_sha256=core_sha,
        capability_manifest_sha256=evaluator_bundle.capability_manifest_sha256,
        role="evaluator",
    )
    if admission_errors:
        raise core70.ContractError("; ".join(admission_errors))
    evaluator_admission_after = core70.admission_bundle_sha256(args.evaluator_admission, role="evaluator")
    if evaluator_admission_after != evaluator_admission_before:
        raise core70.ContractError("evaluator profile-admission bundle changed during validation")

    key_digest = core70.sha256_tree(args.keys)
    rubric_digest = core70.sha256_file(args.shared_rubric) if args.shared_rubric is not None else None
    evaluator_admission_snapshot = core70.snapshot_profile_admission(
        args.evaluator_admission,
        args.run,
        role="evaluator",
        prefix="assessment-profile-admission",
    )
    if evaluator_admission_snapshot.get("admission_bundle_sha256") != evaluator_admission_after:
        raise core70.ContractError("evaluator profile-admission bundle changed before assessment launch")

    with tempfile.TemporaryDirectory(prefix="ssdp70-assess-") as tmp:
        root = Path(tmp)
        bundle_root = root / "bundle"
        runtime_home = root / "runtime-home"
        bundle_root.mkdir()
        runtime_home.mkdir()
        manifest = prepare_bundle(args.run, args.keys, args.shared_rubric, requirements, bundle_root)
        evaluator_env = adapter.clean_env()
        evaluator_env.update({
            "HOME": str(runtime_home),
            "XDG_CONFIG_HOME": str(runtime_home / ".config"),
            "XDG_CACHE_HOME": str(runtime_home / ".cache"),
        })
        containment = adapter.realize_containment(evaluator_bundle.profile, bundle_root, evaluator_env)
        (args.run / "assessment-containment-realization.json").write_text(
            json.dumps(containment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        launched = adapter.launch(evaluator_bundle.profile, PROMPT, bundle_root, evaluator_env)
        (args.run / "assessment-trace.jsonl").write_text(launched["stdout"], encoding="utf-8")
        (args.run / "assessment-evidence-manifest.json").write_text(
            json.dumps({"schema": 1, "files": manifest}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (args.run / "assessment-stderr.txt").write_text(launched["stderr"], encoding="utf-8")
        text, final_event = result_text(launched["stdout"])

    runtime_observation = adapter.runtime_observation(launched["stdout"])
    runtime_errors = core70.validate_launch_identity(evaluator_bundle.profile, launched.get("command_identity"))
    runtime_errors.extend(core70.validate_runtime_observation(evaluator_bundle, runtime_observation))
    auto_memory = (runtime_observation.get("memory_paths") or {}).get("auto") if isinstance(runtime_observation, dict) else None
    if isinstance(auto_memory, str) and auto_memory:
        try:
            Path(auto_memory).resolve().relative_to(runtime_home.resolve())
        except (OSError, ValueError):
            runtime_errors.append("evaluator auto-memory path escapes the fresh run-owned HOME")
    assessment_identity = {
        "schema": 1,
        "run_identity_sha256": run_identity.get("identity_sha256"),
        "run_evidence_state": summary["evidence_state"],
        "evaluator_profile_key_sha256": evaluator_bundle.profile_key_sha256,
        "evaluator_profile_document_sha256": core70.sha256_file(args.evaluator_profile),
        "evaluator_capability_manifest_sha256": evaluator_bundle.capability_manifest_sha256,
        "evaluator_adapter_sha256": evaluator_adapter_sha,
        "evaluator_wrapper_sha256": core70.sha256_file(Path(__file__).resolve()),
        "qualification_core_sha256": core_sha,
        "evaluator_admission_sha256": evaluator_admission_after,
        "evaluator_runtime_observation": runtime_observation,
        "evaluator_command_identity": launched.get("command_identity"),
        "custodian_key_tree_sha256": key_digest,
        "rubric_sha256": rubric_digest,
        "assessment_schema": 1,
        "expected_scoring_items_sha256": requirements.scoring_manifest_digest,
    }
    assessment_identity["identity_sha256"] = core70.stable_json_sha256(assessment_identity)
    (args.run / "assessment-identity.json").write_text(
        json.dumps(assessment_identity, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    status = "INADMISSIBLE" if runtime_errors else "VALID"
    errors: list[str] = list(runtime_errors)
    verdict: Any = None
    if launched["returncode"] != 0 or final_event is None or final_event.get("is_error"):
        status = "EXECUTION_ERROR"
        errors.append(f"evaluator process failed or returned an error (returncode={launched['returncode']})")
    if text is None:
        status = "UNPARSEABLE" if status == "VALID" else status
        errors.append("no result text")
    else:
        try:
            start, end = text.index("{"), text.rindex("}") + 1
            verdict = json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError) as exc:
            status = "UNPARSEABLE" if status == "VALID" else status
            errors.append(f"invalid JSON result: {exc}")
    if isinstance(verdict, dict):
        schema_errors = validate_verdict(verdict, expected_episode, requirements)
        if schema_errors:
            if status == "VALID":
                status = "INVALID_SCHEMA"
            errors.extend(schema_errors)

    if status == "VALID":
        outcome = core70.outcome_from_dispositions(verdict["dispositions"], requirements)
        output = {
            "assessment_status": "VALID",
            "evidence_state": "COMPLETE_ADMISSIBLE",
            "qualification_outcome": outcome,
            "assessment_identity_sha256": assessment_identity["identity_sha256"],
            "episode": verdict["episode"],
            "dispositions": verdict["dispositions"],
            "r2_point_index": verdict["r2_point_index"],
            "owner_false_activation": verdict["owner_false_activation"],
            "notes": verdict["notes"],
        }
        exit_code = 0 if outcome == "PASS" else 1 if outcome == "FAIL" else 2
    else:
        output = {
            "assessment_status": status,
            "evidence_state": (
                "INADMISSIBLE" if status == "INADMISSIBLE"
                else "MALFORMED_EVIDENCE_OR_ASSESSMENT" if status != "EXECUTION_ERROR"
                else "EXECUTION_ERROR"
            ),
            "qualification_outcome": "NOT_EVALUATED",
            "assessment_identity_sha256": assessment_identity["identity_sha256"],
            "errors": errors,
            "raw_result": text[-4000:] if isinstance(text, str) else "",
        }
        exit_code = 2
    (args.run / "assessment.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
