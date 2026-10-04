#!/usr/bin/env python3
"""Batch evaluator runner for Protocol 7 Stage F matrix realizations.

Executes independent blind evaluation via assess70.py over frozen realizations,
preserving the source realization directory unmodified. Evaluates runs across
isolated copies in an assessment workspace, derives qualification outcomes,
and aggregates scoring per qualification contract §§1–6.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accounting-manifest", type=Path, required=True)
    parser.add_argument(
        "--runs-dir",
        type=Path,
        required=True,
        help="Path to source frozen run realizations (read-only)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Path to assessment output workspace directory",
    )
    parser.add_argument(
        "--keys",
        type=Path,
        required=True,
        help="Path to custodian withheld keys directory",
    )
    parser.add_argument(
        "--evaluator-profile",
        type=Path,
        required=True,
        help="Path to admitted evaluator profile.json",
    )
    parser.add_argument(
        "--evaluator-capabilities",
        type=Path,
        required=True,
        help="Path to admitted evaluator capabilities.json",
    )
    parser.add_argument(
        "--evaluator-admission",
        type=Path,
        required=True,
        help="Path to admitted evaluator profile-admission.json",
    )
    parser.add_argument(
        "--adapter",
        required=True,
        help="Explicit admitted evaluator adapter; no implicit dependency on a local untracked adapter",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=4,
        help="Number of concurrent assessment workers (default: 4)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of runs to process (for staging/testing)",
    )
    parser.add_argument(
        "--only",
        default=None,
        help="Comma-separated list of episodes or run directory names to assess",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Skip runs that already have a valid assessment.json (default: True)",
    )
    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="resume",
        help="Do not skip existing assessments",
    )
    return parser.parse_args(argv)


def is_assessment_complete(dest_run_dir: Path) -> bool:
    assess_json = dest_run_dir / "assessment.json"
    if not assess_json.is_file():
        return False
    try:
        data = json.loads(assess_json.read_text(encoding="utf-8"))
        return isinstance(data, dict) and "assessment_status" in data
    except Exception:
        return False


def assess_one_run(
    run_name: str,
    src_run_dir: Path,
    dest_run_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    t0 = time.time()
    dest_run_dir.parent.mkdir(parents=True, exist_ok=True)

    # A status label cannot establish cache identity. Preserve prior assessments;
    # independent reassessment uses a fresh output directory and current dependencies.
    if args.resume and dest_run_dir.exists():
        raise core70.ContractError("status-only assessment resume is refused; use a fresh output directory")

    max_attempts = 1
    if dest_run_dir.exists():
        raise core70.ContractError("assessment output already exists; preserve it and use a fresh output directory")
    last_res: dict[str, Any] = {}

    for attempt in range(1, max_attempts + 1):
        # Copy realization to staging directory
        shutil.copytree(src_run_dir, dest_run_dir)
        # Ensure writable permissions on top-level directory and all descendants
        subprocess.run(["chmod", "-R", "u+w", str(dest_run_dir)], check=True)

        cmd = [
            sys.executable,
            str(HERE / "assess70.py"),
            "--run",
            str(dest_run_dir),
            "--keys",
            str(args.keys),
            "--evaluator-profile",
            str(args.evaluator_profile),
            "--evaluator-capabilities",
            str(args.evaluator_capabilities),
            "--evaluator-admission",
            str(args.evaluator_admission),
            "--adapter",
            args.adapter,
        ]

        env = dict(os.environ)
        if "SSDP70_DEEPINFRA_API" in env and "SSDP70_OMP_PROVIDER_CREDENTIAL" not in env:
            env["SSDP70_OMP_PROVIDER_CREDENTIAL"] = env["SSDP70_DEEPINFRA_API"]
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        proc = subprocess.run(
            cmd,
            cwd=str(HERE),
            env=env,
            capture_output=True,
            text=True,
        )
        elapsed = time.time() - t0

        assess_json = dest_run_dir / "assessment.json"
        if assess_json.is_file():
            try:
                payload = json.loads(assess_json.read_text(encoding="utf-8"))
                st = payload.get("assessment_status")
                last_res = {
                    "run": run_name,
                    "status": st,
                    "outcome": payload.get("qualification_outcome"),
                    "elapsed_s": round(elapsed, 2),
                    "resumed": False,
                    "exit_code": proc.returncode,
                    "attempts": attempt,
                }
                if st == "VALID" or (st == "NOT_EVALUATED" and payload.get("evidence_state") == "EXECUTION_ERROR"):
                    return last_res
                if attempt < max_attempts:
                    time.sleep(1)
                    continue
                return last_res
            except Exception as exc:
                last_res = {
                    "run": run_name,
                    "status": "MALFORMED_OUTPUT",
                    "outcome": "NOT_EVALUATED",
                    "elapsed_s": round(elapsed, 2),
                    "error": str(exc),
                    "exit_code": proc.returncode,
                    "attempts": attempt,
                }
        else:
            last_res = {
                "run": run_name,
                "status": "ASSESSMENT_FAILED",
                "outcome": "NOT_EVALUATED",
                "elapsed_s": round(elapsed, 2),
                "error": proc.stderr[-500:],
                "exit_code": proc.returncode,
                "attempts": attempt,
            }

    return last_res


def aggregate_assessments(out_dir: Path, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """The production aggregation boundary. Integrity uses this same path and retains local FAIL."""
    if manifest is None:
        raise core70.ContractError("aggregation requires a pre-launch purpose/campaign/suite manifest")
    errors = core70.campaign_manifest_errors(manifest)
    if errors:
        raise core70.ContractError("; ".join(errors))
    digest = core70.stable_json_sha256(manifest)
    purpose = manifest["purpose"]
    expected = {row["id"]: row for row in manifest["runs"]}
    actual_dirs = {path.name for path in out_dir.iterdir() if path.is_dir() and (path / "run-identity.json").is_file()}
    if actual_dirs - set(expected):
        raise core70.ContractError("undeclared realizations cannot be omitted or imported into campaign counts")
    result: dict[str, Any] = {"purpose": purpose, "scope_id": manifest["scope_id"], "manifest_sha256": digest,
        "total_runs": 0, "arms": {}, "critical_failures": {}, "by_episode": {}, "runs": {},
        "criteria": {}, "qualification_outcome": "NOT_EVALUATED", "errors": []}
    for run_id, declaration in expected.items():
        run = out_dir / run_id
        try:
            identity = core70.load_json(run / "run-identity.json")
            summary = core70.load_json(run / "summary.json")
            assessment = core70.load_json(run / "assessment.json") if (run / "assessment.json").is_file() else None
        except core70.ContractError as exc:
            result["errors"].append(f"{run_id}: missing run/assessment: {exc}")
            continue
        scope = identity.get("accounting", {})
        binding_errors = core70.validate_accounting_identity(identity)
        if scope.get("purpose") != purpose or scope.get("scope_id") != manifest["scope_id"] or scope.get("manifest_sha256") != digest:
            binding_errors.append("purpose/campaign identity does not match the frozen launch manifest")
        if summary.get("accounting") != scope or summary.get("run_identity_sha256") != identity.get("identity_sha256"):
            binding_errors.append("post-launch run/accounting modification")
        if any(identity.get(key) != declaration.get(key) for key in ("profile_key_sha256", "entry_stratum")):
            binding_errors.append("run profile/stratum differs from the frozen offered manifest")
        if {k: identity.get("subject", {}).get(k) for k in ("commit", "package_sha256")} != declaration["subject"]:
            binding_errors.append("run subject differs from declared immutable subject")
        if scope.get("scoring_manifest_sha256") != declaration.get("scoring_manifest_sha256"):
            binding_errors.append("run scoring identity differs from declaration")
        if binding_errors:
            raise core70.ContractError(f"{run_id}: " + "; ".join(binding_errors))
        if purpose == "qualification" and (scope.get("campaign_record_sha256") != digest
                or scope.get("family_record_sha256") != manifest["family_record_sha256"]
                or scope.get("primary_family_id") != manifest["family"]["family_id"]):
            raise core70.ContractError("campaign/family provenance mismatch")
        requirements = core70.requirements_from_snapshot(core70.load_json(run / "requirements-snapshot.json"), {
            "required_artifacts": identity["requirements"]["required_artifacts_sha256"],
            "required_oracles": identity["requirements"]["required_oracles_sha256"],
            "expected_scoring_items": scope["scoring_manifest_sha256"],
        })
        dispositions = assessment.get("dispositions") if isinstance(assessment, dict) else None
        if isinstance(assessment, dict) and (assessment.get("accounting") != scope or assessment.get("run_identity_sha256") != identity["identity_sha256"]):
            raise core70.ContractError("assessment cache/accounting provenance mismatch")
        actual = core70.production_assessment(summary, identity, requirements, dispositions)
        if summary.get("evidence_state") == "COMPLETE_ADMISSIBLE":
            evidence_errors = core70.validate_complete_run(run, identity, requirements)
            if evidence_errors:
                actual["evidence_state"] = "MALFORMED_EVIDENCE_OR_ASSESSMENT"
                actual["qualification_outcome"] = "NOT_EVALUATED"
                actual["criteria"]["harness/admissibility"] = "FAIL"
                actual["errors"] = evidence_errors
        if assessment is None:
            result["errors"].append(f"{run_id}: assessment missing")
        result["runs"][run_id] = actual
        if purpose == "oracle-integrity":
            result["runs"][run_id]["outer_integrity"] = core70.integrity_assessment(actual, declaration["expected"])
            continue
        if purpose == "development":
            continue
        # Only a qualification scope can supply any exposure/counts, including failed launches.
        result["total_runs"] += 1
        arm = identity["arm"]
        arm_data = result["arms"].setdefault(arm, {"total": 0, "outcomes": {}, "dispositions": {"pass": 0, "fail": 0, "unresolved": 0}})
        result["critical_failures"].setdefault(arm, 0)
        arm_data["total"] += 1
        outcome = actual["qualification_outcome"]
        arm_data["outcomes"][outcome] = arm_data["outcomes"].get(outcome, 0) + 1
        for disposition in actual.get("dispositions", []):
            value = disposition["result"]
            if value in arm_data["dispositions"]:
                arm_data["dispositions"][value] += 1
            if disposition["critical"] and value == "fail":
                result["critical_failures"][arm] += 1
        result["by_episode"].setdefault(identity["episode"], {})[run_id] = actual
    if purpose == "oracle-integrity":
        result["integrity_outcome"] = "PASS" if not result["errors"] and len(result["runs"]) == len(expected) and all(
            row["outer_integrity"]["integrity_outcome"] == "PASS" for row in result["runs"].values()) else "FAIL"
        return result
    if purpose == "development":
        return result
    # Activation counts ALL declared deterministic realizations, including inadmissible runs.
    # No selection of a later successful replicate/replacement can remove this failure.
    family = manifest["family"]
    keys = family["ordered_keys"]
    key_criteria = {}
    for key in manifest["offered_profiles"]:
        members = [result["runs"].get(r["id"]) for r in expected.values() if r["profile_key_sha256"] == key]
        deterministic = [result["runs"].get(r["id"]) for r in expected.values()
                         if r["profile_key_sha256"] == key and r["entry_stratum"] == "deterministic"]
        states = [row["criteria"]["deterministic activation"] if row else "NOT_EVALUATED" for row in deterministic]
        key_criteria[key] = {
            "harness/admissibility": "PASS" if members and all(r and r["criteria"]["harness/admissibility"] == "PASS" for r in members) else "FAIL",
            "deterministic activation": "FAIL" if "FAIL" in states else "PASS" if states and set(states) == {"PASS"} else "NOT_EVALUATED",
            "declared_deterministic_runs": len(states), "delivered": states.count("PASS"),
        }
    result["profiles"] = key_criteria
    result["parts"] = aggregate_parts(manifest, result["runs"], out_dir)
    if not owner_observation_complete(result["runs"]):
        result["parts"]["owner_false_activation"]["state"] = "UNRESOLVED"
        result["parts"]["owner_false_activation"]["reason"] = "complete SSDP resource-read observation is missing"

    for criterion in core70.CRITERION_ORDER:
        states = [row["state"] for part, row in result["parts"].items() if core70.CAMPAIGN_PARTS[part][0] == criterion]
        if criterion in ("harness/admissibility", "deterministic activation"):
            states.extend(key_criteria[key][criterion] for key in keys if criterion != "deterministic activation" or key != family["panels"]["ordinary"]["key"])
        if criterion == "no critical failure" and result["critical_failures"].get(manifest.get("candidate_arm"), 0):
            states.append("FAIL")
        result["criteria"][criterion] = "FAIL" if "FAIL" in states else "PASS" if states and set(states) == {"PASS"} else "UNRESOLVED"
    primary_pass = not result["errors"] and len(result["runs"]) == len(expected) and set(result["criteria"].values()) == {"PASS"}
    result["primary_family_id"] = family["family_id"]
    result["primary_family_outcome"] = "PASS" if primary_pass else "FAIL" if "FAIL" in result["criteria"].values() else "UNRESOLVED"
    for key, criteria in key_criteria.items():
        criteria["qualification_outcome"] = "PASS" if primary_pass and all(criteria[c] == "PASS" for c in ("harness/admissibility", "deterministic activation")) else "NOT_EVALUATED"
        if key not in keys:
            criteria["claim_limits"] = ["no human-legibility claim", "no ordinary-selection false-activation claim", "own predicate/owner false-activation floors required", "cannot rescue primary family"]
            # Non-primary doctrine and false activation evidence must pass independently.
            criteria["qualification_outcome"] = "NOT_EVALUATED"
    result["qualification_outcome"] = result["primary_family_outcome"]
    return result


def aggregate_parts(manifest: dict[str, Any], runs: dict[str, Any], root: Path) -> dict[str, Any]:
    """Bind independent opportunities to actual production dispositions; missing parts stay non-PASS."""
    opportunities = manifest.get("opportunities", [])
    if not isinstance(opportunities, list):
        raise core70.ContractError("opportunity manifest malformed")
    parts = {part: {"state": "UNRESOLVED", "arms": {}, "reason": "missing independent opportunity evidence"} for part in core70.CAMPAIGN_PARTS}
    grouped = {}
    for opportunity in opportunities:
        required = {"id", "part", "arm", "fixture", "profile_key_sha256", "realizations"}
        if not isinstance(opportunity, dict) or not required <= set(opportunity) or opportunity["part"] not in parts:
            raise core70.ContractError("opportunity metadata missing/malformed")
        part, arm, oid = opportunity["part"], opportunity["arm"], opportunity["id"]
        if opportunity["profile_key_sha256"] not in manifest["family"]["criterion_to_keys"][part]:
            raise core70.ContractError("opportunity is assigned outside the frozen criterion-part key map")
        if (part, arm, oid) in grouped:
            raise core70.ContractError("replicates cannot manufacture new independent opportunities")
        outcomes = []
        for reference in opportunity["realizations"]:
            run_id, item_id = reference["run"], reference["item"]
            actual = runs.get(run_id)
            if actual is None or actual["evidence_state"] != "COMPLETE_ADMISSIBLE":
                outcomes.append("unresolved")
                continue
            declaration = next(row for row in manifest["runs"] if row["id"] == run_id)
            if declaration["profile_key_sha256"] != opportunity["profile_key_sha256"]:
                raise core70.ContractError("opportunity realization profile key mismatch")
            matches = [row for row in actual.get("dispositions", []) if row["item"] == item_id]
            outcomes.append(matches[0]["result"] if len(matches) == 1 else "unresolved")
        # A replicate is not exposure; R2 hit requires strict majority of admissible replicates.
        if not outcomes or any(value == "unresolved" for value in outcomes):
            value = "unresolved"
        elif part.startswith("r2_"):
            value = "pass" if outcomes.count("pass") > len(outcomes) / 2 else "fail"
        else:
            value = "fail" if "fail" in outcomes else "pass"
        grouped[part, arm, oid] = value
        counts = parts[part]["arms"].setdefault(arm, {"opportunities": 0, "pass": 0, "fail": 0, "unresolved": 0})
        counts["opportunities"] += 1
        counts[value] += 1
    candidate, comparator = manifest.get("candidate_arm"), manifest.get("comparator_arm")
    for part, row in parts.items():
        _, _, minimum, allowed = core70.CAMPAIGN_PARTS[part]
        arm_counts = row["arms"]
        if candidate not in arm_counts or (not part.startswith("r2_") and comparator not in arm_counts):
            continue
        exposures = [arm_counts[candidate]] if part.startswith("r2_") else [arm_counts[a] for a in (candidate, comparator)]
        selected = [arm_counts[candidate]]
        if any(c["opportunities"] < minimum or c["unresolved"] for c in exposures):
            row["reason"] = "underexposed or unresolved independent opportunities"
            continue
        if core70.CAMPAIGN_PARTS[part][0] == "report-only":
            row["state"] = "PASS"
        elif allowed is not None:
            row["state"] = "PASS" if all(c["fail"] <= allowed for c in selected) else "FAIL"
        elif part in ("noncritical_detection", "unnamed_detection", "r2_analysis", "r2_authority", "r2_gate", "human_routine"):
            row["state"] = "PASS" if all(c["pass"] * 5 >= c["opportunities"] * 4 for c in selected) else "FAIL"
        elif part in ("r2_authoring","r2_review"):
            row["state"] = "PASS" # This is exposure only; hits remain in the authority-class floor.
        elif part == "false_surfacing":
            row["state"] = "PASS" if all(c["fail"] * 20 <= c["opportunities"] for c in selected) else "FAIL"
        elif part in ("selection_negative", "near_negative", "routing_hits", "routing_violations", "t4_t6", "never_stated"):
            c, b = arm_counts[candidate], arm_counts[comparator]
            passed = (c["pass"] >= b["pass"] - (2 if part == "routing_hits" else 1)) if part in ("routing_hits", "t4_t6") else c["fail"] <= b["fail"] + (2 if part == "routing_violations" else 1)
            row["state"] = "PASS" if passed else "FAIL"
        elif part in ("fixed_cost","active_material","report_length","elapsed_time","human_time"):
            state,reason=quantitative_part(part,manifest,opportunities,root)
            row["state"]=state
            if reason: row["reason"]=reason
        elif part == "comparative":
            pass # Derived after all independent per-measure counts below.
        else:
            row["state"]="UNRESOLVED"
            row["reason"]="unrecognized quantitative criterion"
        if row["state"] != "UNRESOLVED":
            row.pop("reason", None)
    parts["comparative"]["state"], parts["comparative"]["reason"] = comparative_part(parts,manifest)
    # Predicate exposure must be met by deterministic keys alone. Pooling never removes failures.
    deterministic_ids={r["id"] for r in manifest["runs"] if r["entry_stratum"]=="deterministic"}
    excluded={o["id"] for o in opportunities if o["part"]=="predicate_false_firing" and o["arm"]==candidate
              and o["realizations"] and all(ref["run"] in deterministic_ids for ref in o["realizations"])}
    if len(excluded)<12:
        parts["predicate_false_firing"]["state"]="UNRESOLVED"
        parts["predicate_false_firing"]["reason"]="fewer than twelve deterministic predicate-excluded opportunities"
    # Unnamed classification and fixture independence remain custodian/checker-owned; count frozen assignments only.
    properties={o["id"] for o in opportunities if o["arm"]==candidate and o["part"] in ("critical","noncritical_detection")}
    unnamed={o["id"] for o in opportunities if o["arm"]==candidate and o["part"]=="unnamed_detection"}
    fixtures={o["fixture"] for o in opportunities if o["arm"]==candidate and o["part"] in ("critical","noncritical_detection")}
    critical_unnamed={o["fixture"] for o in opportunities if o["arm"]==candidate and o["part"]=="critical" and o["id"] in unnamed}
    if len(unnamed)<6 or len(unnamed)*4<len(properties) or not unnamed<=properties or not 2<=len(fixtures)<=3 or critical_unnamed!=fixtures:
        parts["unnamed_detection"]["state"]="UNRESOLVED"
        parts["unnamed_detection"]["reason"]="unnamed share, critical per-fixture membership or composite coverage missing"
    return parts


def owner_observation_complete(runs: dict[str, Any]) -> bool:
    """Owner false activation needs every run's owner-read question observed exactly; a run whose
    byte accounting is inexact for unrelated files still answers it (summary `owner_read_exact`)."""
    for row in runs.values():
        observation = row.get("resource_observation") or {}
        if observation.get("owner_read_exact", observation.get("exact")) is not True:
            return False
    return True


def quantitative_part(part, manifest, opportunities, root):
    """Compare retained numeric observables, preserving units, pairs and route boundaries."""
    field = {"fixed_cost":"active_ssdp_bytes", "active_material":"active_ssdp_bytes", "report_length":"report_bytes", "elapsed_time":"wall_s"}.get(part)
    grouped = {}
    for opportunity in opportunities:
        if opportunity["part"] != part:
            continue
        route = opportunity.get("route")
        if not isinstance(route,str):
            return "UNRESOLVED", "numeric route identity missing"
        for ref in opportunity["realizations"]:
            try:
                summary = core70.load_json(root/ref['run']/'summary.json')
                if field:
                    value = summary[field]
                    extra = (summary.get('installed_entrypoint_bytes'),summary.get('installed_owner_bytes'))
                    owner_reads = summary.get('owner_read_sequences')
                    if part in ('fixed_cost','active_material') and not isinstance(owner_reads, list):
                        return 'UNRESOLVED','owner-read mode is unobserved (inexact package observation)'
                    extra += (None if owner_reads is None else 'owner' if owner_reads else 'entrypoint-only',)
                else:
                    oracle = core70.load_json(root/ref['run']/'oracle.json')['results'][ref['oracle']]
                    payload = core70.load_json(root/ref['run']/oracle['stdout_artifact'])
                    metric = payload['measurements'][ref['item']]
                    if metric['unit'] != 'seconds':
                        return 'UNRESOLVED','human time unit missing/wrong'
                    value=metric['value']; extra=(None,None)
                if not isinstance(value,(int,float)) or isinstance(value,bool) or value<0 or not __import__('math').isfinite(value):
                    return 'UNRESOLVED','numeric observable missing/malformed'
                grouped.setdefault(route,{}).setdefault(opportunity['arm'],[]).append((value,extra))
            except (core70.ContractError,KeyError,TypeError):
                return 'UNRESOLVED','required retained numeric oracle observation missing'
    candidate = manifest.get('candidate_arm'); baseline = manifest.get('cost_comparator_arm') if part=='fixed_cost' else manifest.get('comparator_arm')
    if not grouped or baseline is None:
        return 'UNRESOLVED','paired numeric observations missing'
    if part=='fixed_cost' and set(grouped)!={'T1','T7','T8'}:
        return 'UNRESOLVED','fixed-cost panel requires T1,T7,T8 separately'
    from statistics import median
    for route,arms in grouped.items():
        c,b=arms.get(candidate,[]),arms.get(baseline,[])
        if not c or not b or len(c)!=len(b):
            return 'UNRESOLVED','numeric paired arm exposure mismatch'
        if part in ('fixed_cost','report_length','elapsed_time') and len(c)<3:
            if part!='fixed_cost' and route in manifest.get('descriptive_routes',[]):
                continue
            return 'UNRESOLVED','underexposed median comparison'
        cm,bm=median(v[0] for v in c),median(v[0] for v in b)
        if part=='active_material':
            if any(not isinstance(v[1][0],int) or not isinstance(v[1][1],int) for v in c) or any(not isinstance(v[1][0],int) for v in b):
                return 'UNRESOLVED','installed entrypoint/owner byte evidence missing'
            delta=median(v[1][0] for v in c)-median(v[1][0] for v in b)
            bound=bm+delta+median(v[1][1] for v in c)+512
        else:
            bound=2.0*bm
        if cm>bound:
            return 'FAIL',f'{route}: candidate median {cm} exceeds bound {bound}'
        if part=='fixed_cost' and route=='T7':
            # Mixed entrypoint-only/owner modes trigger exactly 3 -> 5 -> 7 pairs.
            mixed=any(len({v[1][2] for v in arm})>1 for arm in (c,b))
            if len(c) not in (3,5,7) or (mixed and len(c)<7):
                return 'UNRESOLVED','T7 bounded mixed-mode extension remains decision-sensitive'
    return 'PASS',None


def comparative_part(parts, manifest):
    candidate,baseline=manifest.get('candidate_arm'),manifest.get('comparator_arm')
    gains=[]
    for part in ('noncritical_detection','null','variant'):
        arms=parts[part]['arms'];c=arms.get(candidate);b=arms.get(baseline)
        if not c or not b or c['opportunities']!=b['opportunities'] or c['unresolved'] or b['unresolved']:
            return 'UNRESOLVED','paired comparative opportunity composition unresolved'
        difference=c['pass']-b['pass']
        if difference < -1:
            return 'FAIL','comparative decrease exceeds one independent opportunity'
        gains.append(difference>=3 and difference*100>=15*c['opportunities'])
    if not any(gains):
        return 'FAIL','no measure gains both fifteen percentage points and three independent opportunities'
    c=parts['comparative']['arms'].get(candidate,{})
    if not c or c.get('unresolved') or c.get('fail') or c.get('opportunities',0)<1:
        return 'UNRESOLVED','required independent confidence/cluster/run-noise assessment is non-PASS'
    return 'PASS',None

def print_summary(summary: dict[str, Any], declared: set[str]) -> None:
    """Purpose-aware final summary; integrity and development scopes have no qualification arms."""
    print(f"Purpose {summary['purpose']} scope {summary['scope_id']}: runs {len(summary['runs'])}/{len(declared)}")
    if "integrity_outcome" in summary:
        print(f"Outer integrity outcome: {summary['integrity_outcome']}")
    for arm, arm_data in sorted(summary["arms"].items()):
        print(f"Arm {arm}: Total {arm_data['total']}, Outcomes: {arm_data['outcomes']}, "
              f"Critical Fails: {summary['critical_failures'].get(arm, 0)}")
    if summary["errors"]:
        print(f"Errors: {summary['errors']}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    runs_dir = args.runs_dir.resolve()
    out_dir = args.out_dir.resolve()
    # The frozen purpose/campaign/suite manifest is validated before any evaluator is launched.
    manifest = core70.load_json(args.accounting_manifest)
    manifest_errors = core70.campaign_manifest_errors(manifest)
    if manifest_errors:
        print("[!] accounting manifest refused before evaluator launch: " + "; ".join(manifest_errors), file=sys.stderr)
        return 2
    declared = {row["id"] for row in manifest["runs"]}
    out_dir.mkdir(parents=True, exist_ok=True)

    all_runs = sorted(
        d for d in os.listdir(runs_dir)
        if (runs_dir / d).is_dir() and not d.startswith(".") and not d.startswith("FREEZE")
    )

    if args.only:
        targets = set(args.only.split(","))
        all_runs = [r for r in all_runs if r in targets or r.split("-")[0] in targets]

    if args.limit:
        all_runs = all_runs[: args.limit]

    undeclared = [r for r in all_runs if r not in declared]
    if undeclared:
        print(f"[!] undeclared realizations cannot be assessed or imported into this scope: {undeclared}", file=sys.stderr)
        return 2
    total = len(all_runs)
    print(f"[*] Starting batch assessment of {total} runs (parallel={args.parallel})")
    print(f"    Source: {runs_dir}")
    print(f"    Destination: {out_dir}")

    results = []
    completed = 0
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
        future_map = {
            executor.submit(
                assess_one_run,
                r,
                runs_dir / r,
                out_dir / r,
                args,
            ): r
            for r in all_runs
        }

        for future in concurrent.futures.as_completed(future_map):
            completed += 1
            res = future.result()
            results.append(res)
            run_name = res["run"]
            status = res.get("status", "ERR")
            outcome = res.get("outcome", "ERR")
            elapsed = res.get("elapsed_s", 0)
            resumed = " (resumed)" if res.get("resumed") else ""
            print(f"[{completed:3d}/{total:3d}] {run_name}: {status} / {outcome} ({elapsed}s){resumed}")

    total_time = round(time.time() - start_time, 2)
    print(f"[*] Completed {completed}/{total} runs in {total_time}s")

    # Aggregate results
    summary = aggregate_assessments(out_dir, manifest)
    summary_path = out_dir / "assessment-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[*] Saved summary to {summary_path}")

    print("\n=== Assessment Summary ===")
    print_summary(summary, declared)
    return 0


if __name__ == "__main__":
    sys.exit(main())
