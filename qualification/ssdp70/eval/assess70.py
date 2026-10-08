#!/usr/bin/env python3
"""H3: independent, fail-closed assessment of one run by a blinded evaluator model (contract v2 section 3).

Consumes only COMPLETE_ADMISSIBLE run evidence. The evaluator sees a redacted copy of the run: version and protocol
identifiers are removed from text, and the files that name the arm, package or profile are withheld. It returns exactly
one disposition for every frozen scoring item; the wrapper rejects missing, duplicate, unknown or altered items.
The evaluator model is never the executor model (the evaluator profile is a separate frozen document).
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402

REDACTION_VERSION = 1
EVIDENCE = (
    "summary.json", "requirements-snapshot.json", "final-report.md", "diff.patch", "side-effects.jsonl", "tool-calls.jsonl",
    "trace.jsonl", "events.normalized.jsonl", "oracle.json", "stderr.txt", "issues-final", "oracle-output", "final-tree",
)
# What would name the arm, package or profile never reaches the evaluator.
# What would name the arm, package, profile or protocol reaches the evaluator in no field and no filename.
BLINDED_KEYS = frozenset({
    "arm", "subject_commit", "profile_key_sha256", "run_identity_sha256", "adapter_command_identity", "runtime_observation",
    "pair_order", "commit", "package_sha256", "requested_ref", "installed_skill_bytes", "installed_skill_sha256",
    "installed_entrypoint_bytes", "installed_owner_bytes", "active_ssdp_files", "active_ssdp_bytes", "ssdp_read_mode",
    "resource_observation", "resolved_package_identity", "owner_read_sequences", "owner_read_observed", "owner_minor_exposure",
})
_SSDP_VERSIONS = r"(?:5\.16|6\.[0-6]|7\.[0-2]|8\.0)"
_VERSION_RES = (  # explicit SSDP identifiers only: project content such as "version 2" or "aqpipe 0.7.1" and bare numbers like 6.5 stay
    (re.compile(r"(?i)\b(?:SSDP|Protocol)\b[\s`'\"-]*v?\d+(?:\.\d+){0,2}"), "PROTOCOL-X"),
    (re.compile(r"(?<![\w.])v?" + _SSDP_VERSIONS + r"\.0(?![\w.])"), "X.Y.Z"),
    (re.compile(r"\bp(?:65|66|70|71|72)\b"), "armX"),
)
PROMPT = """You are an independent evaluator. You did not perform this run and must not trust the executor's claims.

Read EVIDENCE-MANIFEST.json first. The run evidence is under run/, the frozen expected scoring items are in
run/requirements-snapshot.json, and custodian key material is under keys/. Score only against those frozen materials
and the frozen rubric. Do not infer a missing fact from an excerpt. Do not alter evidence and do not use network,
shell, skills or agents.

You MUST return exactly one disposition for every expected scoring item, using the exact item id, measure, critical flag
and an allowed disposition from the manifest. Never omit an item. If applicability or evidence is unresolved, return
"unresolved" when allowed; do not manufacture a pass. Generic or boilerplate text never earns a pass for an item that
requires case-specific content. The wrapper rejects missing, duplicate, unknown or altered items.

Return strict JSON only:
{"episode":"...","dispositions":[{"item":"...","measure":"...","result":"pass|fail|unresolved|not-applicable","critical":true,"evidence":"<=40 words"}],"notes":"<=80 words"}
"""


def load_adapter(name: str):
    if not name or any(part in {"", ".", ".."} for part in name.split(".")):
        raise core70.ContractError(f"invalid evaluator adapter name {name!r}")
    module = importlib.import_module(f"adapters.{name}")
    for attr in ("ADAPTER_ID", "launch", "clean_env", "runtime_observation", "realize_containment"):
        if not hasattr(module, attr):
            raise core70.ContractError(f"evaluator adapter {name!r} is missing {attr}")
    return module


def redact(text: str) -> str:
    """Remove version, protocol and arm identifiers from text the evaluator reads."""
    for pattern, token in _VERSION_RES:
        text = pattern.sub(token, text)
    return text


def _scrub(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _scrub(v) for k, v in value.items() if k not in BLINDED_KEYS}
    if isinstance(value, list):
        return [_scrub(v) for v in value]
    return value


def copy_redacted(src: Path, dst: Path) -> None:
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for child in sorted(src.iterdir()):
            copy_redacted(child, dst / child.name)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        text = src.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        shutil.copy2(src, dst)
        return
    try:
        if src.suffix == ".json":
            text = json.dumps(_scrub(json.loads(text)), indent=2, sort_keys=True)
        elif src.suffix == ".jsonl":
            text = "\n".join(json.dumps(_scrub(json.loads(line)), sort_keys=True) if line.strip() else line
                             for line in text.split("\n"))
    except ValueError:
        pass  # not JSON after all: text redaction below still applies
    dst.write_text(redact(text), encoding="utf-8")


def evidence_manifest(root: Path) -> list[dict[str, Any]]:
    return [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "sha256": core70.sha256_file(p)}
            for p in sorted(q for q in root.rglob("*") if q.is_file() and q.name != "EVIDENCE-MANIFEST.json")]


def prepare_bundle(run: Path, keys: Path, rubric: Path | None, requirements: core70.Requirements, root: Path) -> list[dict[str, Any]]:
    missing = core70.validate_required_artifacts(run, requirements) + core70.validate_required_oracles(run, requirements)
    if missing:
        raise core70.ContractError(f"assessment input is incomplete: {missing}")
    if not keys.is_dir():
        raise core70.ContractError(f"custodian key directory is unavailable: {keys}")
    shutil.copytree(keys, root / "keys")
    if rubric is not None:
        (root / "shared-rubric.txt").write_text(redact(rubric.read_text(encoding="utf-8")), encoding="utf-8")
    for name in dict.fromkeys((*EVIDENCE, *requirements.artifacts)):
        if name not in BLINDED_FILES and (run / name).exists():
            copy_redacted(run / name, root / "run" / name)
    manifest = evidence_manifest(root)
    (root / "EVIDENCE-MANIFEST.json").write_text(json.dumps({"schema": 1, "files": manifest}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


BLINDED_FILES = {"run-identity.json", "profile-snapshot.json", "capability-manifest-snapshot.json", "installed-package",
                 "adapter-artifacts", "containment-realization.json", "evidence-integrity.json", "normalization-map.json"}


def result_text(stdout: str) -> tuple[str | None, dict[str, Any] | None]:
    final = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            final = event
    return (None, None) if final is None else (final.get("result", ""), final)


def validate_verdict(verdict: Any, episode: str, requirements: core70.Requirements) -> list[str]:
    if not isinstance(verdict, dict):
        return ["top-level result is not an object"]
    errors: list[str] = []
    if set(verdict) != {"episode", "dispositions", "notes"}:
        errors.append("top-level keys must be exactly ['dispositions', 'episode', 'notes']")
    if verdict.get("episode") != episode:
        errors.append("episode does not match run summary")
    rows = verdict.get("dispositions")
    if not isinstance(rows, list):
        return errors + ["dispositions is not a list"]
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"item", "measure", "result", "critical", "evidence"}:
            errors.append(f"dispositions[{index}] keys are invalid")
        elif not isinstance(row["evidence"], str) or len(row["evidence"].split()) > 40:
            errors.append(f"dispositions[{index}].evidence exceeds 40 words or is not text")
    errors.extend(core70.validate_dispositions(rows, requirements))
    if not isinstance(verdict.get("notes"), str) or len(verdict["notes"].split()) > 80:
        errors.append("notes exceeds 80 words or is not text")
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--keys", type=Path, required=True, help="custodian keys/<episode> directory")
    ap.add_argument("--shared-rubric", type=Path, default=None)
    ap.add_argument("--evaluator-profile", type=Path, required=True)
    ap.add_argument("--evaluator-capabilities", type=Path, required=True)
    ap.add_argument("--adapter", default="omp_eval")
    args = ap.parse_args(argv)

    summary = core70.load_json(args.run / "summary.json")
    identity = core70.load_json(args.run / "run-identity.json")
    if not isinstance(summary, dict) or not isinstance(identity, dict):
        raise core70.ContractError("run summary or identity is malformed")
    digests = identity.get("requirements") if isinstance(identity.get("requirements"), dict) else {}
    try:
        requirements = core70.requirements_from_snapshot(core70.load_json(args.run / "requirements-snapshot.json"), {
            "required_artifacts": digests.get("required_artifacts_sha256"),
            "required_oracles": digests.get("required_oracles_sha256"),
            "expected_scoring_items": digests.get("expected_scoring_items_sha256")})
        run_errors = core70.validate_complete_run(args.run, identity, requirements)
    except core70.ContractError as exc:
        requirements, run_errors = None, [str(exc)]

    def finish(output: dict[str, Any], code: int) -> int:
        (args.run / "assessment.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(output, indent=2))
        return code

    if summary.get("evidence_state") != "COMPLETE_ADMISSIBLE" or run_errors:
        return finish({"assessment_status": "NOT_EVALUATED", "qualification_outcome": "NOT_EVALUATED",
                       "evidence_state": summary.get("evidence_state"),
                       "errors": run_errors or ["only COMPLETE_ADMISSIBLE run evidence may enter assessment"]}, 2)
    assert requirements is not None
    evaluator = core70.load_profile(args.evaluator_profile, args.evaluator_capabilities)
    profile_errors = core70.profile_claim_errors(evaluator, [])
    if profile_errors:
        raise core70.ContractError("; ".join(profile_errors))
    executor = core70.load_json(args.run / "profile-snapshot.json")
    if not isinstance(executor, dict) or not executor.get("agent_model") or not evaluator.profile.get("agent_model"):
        raise core70.ContractError("both the executor and evaluator profiles must name an agent_model")
    if evaluator.profile["agent_model"] == executor["agent_model"]:
        raise core70.ContractError(f"the evaluator model must not be the executor model ({executor['agent_model']!r})")
    adapter = load_adapter(args.adapter)
    if evaluator.profile["adapter_id"] != adapter.ADAPTER_ID:
        raise core70.ContractError(f"evaluator profile adapter_id {evaluator.profile['adapter_id']!r} != {adapter.ADAPTER_ID!r}")
    with tempfile.TemporaryDirectory(prefix="ssdp70-assess-") as tmp:
        bundle = Path(tmp) / "bundle"
        home = Path(tmp) / "evaluator-private" / "runtime-home"
        (bundle / ".qualification-tmp").mkdir(parents=True)
        home.mkdir(parents=True)
        manifest = prepare_bundle(args.run, args.keys, args.shared_rubric, requirements, bundle)
        env = adapter.clean_env()
        env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config"), "XDG_CACHE_HOME": str(home / ".cache"),
                    "TMPDIR": str(bundle / ".qualification-tmp"), "TMP": str(bundle / ".qualification-tmp"), "TEMP": str(bundle / ".qualification-tmp")})
        containment = adapter.realize_containment(evaluator.profile, bundle, env)
        launched = adapter.launch(evaluator.profile, PROMPT, bundle, env)
        text, final = result_text(launched["stdout"])
    (args.run / "assessment-trace.jsonl").write_text(launched["stdout"], encoding="utf-8")
    (args.run / "assessment-stderr.txt").write_text(launched["stderr"], encoding="utf-8")
    observation = adapter.runtime_observation(launched["stdout"])
    errors = core70.validate_launch_identity(evaluator.profile, launched.get("command_identity"))
    errors.extend(core70.validate_runtime_observation(evaluator, observation))
    if not isinstance(containment, dict) or not isinstance(containment.get("realization"), dict):
        errors.append("evaluator containment realization record is malformed")
    assessment_id = {
        "schema": 2, "run_identity_sha256": identity.get("identity_sha256"), "evaluator_profile_key_sha256": evaluator.profile_key_sha256,
        "evaluator_adapter_sha256": core70.sha256_file(Path(adapter.__file__).resolve()),
        "evaluator_wrapper_sha256": core70.sha256_file(Path(__file__).resolve()), "core_sha256": core70.sha256_file(Path(core70.__file__).resolve()),
        "custodian_key_tree_sha256": core70.sha256_tree(args.keys), "rubric_sha256": core70.sha256_file(args.shared_rubric) if args.shared_rubric else None,
        "redaction_version": REDACTION_VERSION, "evidence_manifest_sha256": core70.stable_json_sha256(manifest),
        "expected_scoring_items_sha256": requirements.scoring_manifest_digest,
    }
    assessment_id["identity_sha256"] = core70.stable_json_sha256(assessment_id)
    (args.run / "assessment-identity.json").write_text(json.dumps(assessment_id, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    status, verdict = ("INADMISSIBLE" if errors else "VALID"), None
    if launched["returncode"] != 0 or final is None or final.get("is_error"):
        status = "EXECUTION_ERROR"
        errors.append(f"evaluator process failed or returned an error (returncode={launched['returncode']})")
    if text is None:
        status = "UNPARSEABLE" if status == "VALID" else status
        errors.append("no result text")
    else:
        try:
            verdict = json.loads(text[text.index("{"):text.rindex("}") + 1])
        except (ValueError, json.JSONDecodeError) as exc:
            status = "UNPARSEABLE" if status == "VALID" else status
            errors.append(f"invalid JSON result: {exc}")
    if isinstance(verdict, dict):
        schema_errors = validate_verdict(verdict, summary.get("episode"), requirements)
        if schema_errors:
            status = "INVALID_SCHEMA" if status == "VALID" else status
            errors.extend(schema_errors)
    if status != "VALID":
        return finish({"assessment_status": status, "qualification_outcome": "NOT_EVALUATED", "evidence_state": summary["evidence_state"],
                       "assessment_identity_sha256": assessment_id["identity_sha256"], "errors": errors,
                       "raw_result": text[-4000:] if isinstance(text, str) else ""}, 2)
    outcome = core70.outcome_from_dispositions(verdict["dispositions"], requirements)
    return finish({"assessment_status": "VALID", "qualification_outcome": outcome, "evidence_state": summary["evidence_state"],
                   "assessment_identity_sha256": assessment_id["identity_sha256"], "episode": verdict["episode"],
                   "dispositions": verdict["dispositions"], "notes": verdict["notes"]}, 0 if outcome == "PASS" else 1 if outcome == "FAIL" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
