#!/usr/bin/env python3
"""Executor Rehearsal Forms Matrix Runner (SSDP 7.0 Qualification Phase 2).

Executes the forms specified by D3 Item 8, Contract §1 Item 13, and Stakeholder Confirmations
across Protocol 7.0 (Candidate), 6.6 (Comparator), and 6.5 (Comparator) arm package shapes.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import core70
import harness70
import observer70
import omp_rig
import package_ledger
from adapters import omp

OWNER_REL = "software-implementation/references/scientific-inspectability-and-initiative.md"
OWNER_PATH = "/opt/ssdp/skills/" + OWNER_REL
DIST_SKILLS = REPO / "dist" / "skills"
ARMS_DIR = Path("/tmp/ssdp70-rehearsal-arms")


def get_arm_config(arm_name: str) -> dict[str, Any]:
    if arm_name == "p70":
        return {
            "name": "p70", "requested_ref": "db94a2dfb7fef480f37227eab5c45256e89901b8",
            "commit": "db94a2dfb7fef480f37227eab5c45256e89901b8", "version": "7.0.0",
            "skills_path": str(DIST_SKILLS), "dist_tree_sha256": core70.sha256_tree(DIST_SKILLS),
        }
    elif arm_name in ("p66", "p65"):
        arm_skills = ARMS_DIR / arm_name / "dist" / "skills"
        if not arm_skills.is_dir():
            raise RuntimeError(f"arm package not found at {arm_skills}; run prepare_arms70.py first")
        commit = "22f4bdba53795da3a6f13f162529f3a843fc37ae" if arm_name == "p66" else "7f7b5e24858e813e45ace867a7f8ea5180f43bf0"
        version = "6.6.0" if arm_name == "p66" else "6.5.0"
        return {
            "name": arm_name, "requested_ref": commit, "commit": commit, "version": version,
            "skills_path": str(arm_skills), "dist_tree_sha256": core70.sha256_tree(arm_skills),
        }
    raise ValueError(f"unknown arm {arm_name}")


def build_scenario(case_id: str, arm_name: str) -> tuple[dict[str, Any], list[str], dict[str, Any] | None, dict[str, Any]]:
    """Returns (scenario, claims, parameters, extra_meta)."""
    owner = (DIST_SKILLS / OWNER_REL).read_text().splitlines()
    long_line_idx = next(i + 1 for i, l in enumerate(owner) if len(l.encode()) >= 256)
    
    claims = ["active-byte burden", "owner-read"]
    parameters = None
    meta = {}

    if case_id == "F01-native-read":
        scenario = {"steps": [
            {"tool_calls": [{"name": "read", "arguments": {"path": "/opt/ssdp/skills/software-implementation/SKILL.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F02-absolute-cat":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F03-cd-cat":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cd /opt/ssdp/skills/software-implementation && cat references/{harness70.OWNER}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F04-glob-loop":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"for f in /opt/ssdp/skills/software-implementation/references/{harness70.OWNER}; do cat \"$f\"; done"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F05a-head-literal-owner":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"head -n 40 {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F05b-head-nonliteral-twin":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "cd /opt/ssdp/skills/software-implementation && head -n 40 references/abstraction-and-concretization.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F06-protocol-version-nonliteral":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "cd /opt/ssdp/skills/software-implementation && cat PROTOCOL_VERSION"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F07-package-scan":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "grep -rl '__SSDP_NEVER_MATCHES__' /opt/ssdp/skills || true"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F08-scan-then-r2-load":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"sleep 0.2; wc -l {OWNER_PATH}"}}]},
            {"text": "PREDECLARED_R2: authority review owed.", "tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "CONSEQUENTIAL_STEP: report complete."}
        ]}
        meta["r2_keyword"] = "PREDECLARED_R2"
        meta["consequent_keyword"] = "CONSEQUENTIAL_STEP"
    elif case_id == "F09-wc-grep-c":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"wc -l {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F10-path-naming-ls-echo":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"echo {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F11-same-response-r2":
        scenario = {"steps": [
            {"text": "PREDECLARED_R2: review authority now.", "tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "CONSEQUENTIAL_STEP: report complete."}
        ]}
        meta["r2_keyword"] = "PREDECLARED_R2"
        meta["consequent_keyword"] = "CONSEQUENTIAL_STEP"
    elif case_id == "F12-keyword-grep-minor":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"sed -n '{long_line_idx}p' {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F13-pairing-mismatch":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
        meta["mutate_pairing"] = True
    elif case_id == "F14-error-status-cat-false":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}; false"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F15-above-quantum-keyword-grep":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "grep -rn 'authority' /opt/ssdp/skills"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F16-request-retry":
        scenario = {"steps": [
            {"http_error": 500},
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F17-multi-turn-rescan":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "ls /opt/ssdp/skills"}}]},
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"wc -l {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F18-timing-stress":
        parameters = {"bracket_width_bound_ns": 1}  # causes timing loss
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": f"cat {OWNER_PATH}"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p66-01-native-read":
        scenario = {"steps": [
            {"tool_calls": [{"name": "read", "arguments": {"path": "/opt/ssdp/skills/software-implementation/SKILL.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p66-02-cd-cat-twin":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "cd /opt/ssdp/skills/software-implementation && cat references/abstraction-and-concretization.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p66-03-package-scan":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "grep -rl '__SSDP_NEVER_MATCHES__' /opt/ssdp/skills || true"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p65-01-native-read":
        scenario = {"steps": [
            {"tool_calls": [{"name": "read", "arguments": {"path": "/opt/ssdp/skills/software-implementation/SKILL.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p65-02-cd-cat-twin":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "cd /opt/ssdp/skills/software-implementation && cat references/abstraction-and-concretization.md"}}]},
            {"text": "done"}
        ]}
    elif case_id == "F-p65-03-package-scan":
        scenario = {"steps": [
            {"tool_calls": [{"name": "bash", "arguments": {"command": "grep -rl '__SSDP_NEVER_MATCHES__' /opt/ssdp/skills || true"}}]},
            {"text": "done"}
        ]}
    else:
        raise ValueError(f"unknown case {case_id}")
    return scenario, claims, parameters, meta


ALL_CASES = [
    ("F01-native-read", "p70", "Native read of skill URL and path"),
    ("F02-absolute-cat", "p70", "bash cat with absolute path"),
    ("F03-cd-cat", "p70", "cd <root> && cat references/x (route iii)"),
    ("F04-glob-loop", "p70", "loop and variable path (route iii)"),
    ("F05a-head-literal-owner", "p70", "head partial read through literal path (owner-class supply)"),
    ("F05b-head-nonliteral-twin", "p70", "head partial read of twin through non-literal path (unexplained)"),
    ("F06-protocol-version-nonliteral", "p70", "PROTOCOL_VERSION non-literal path (below floor, unexplained)"),
    ("F07-package-scan", "p70", "grep -rl package-wide scan (unexplained opens, UNRESOLVED floor)"),
    ("F08-scan-then-r2-load", "p70", "package scan followed by post-R2 owner load (owner-load hit)"),
    ("F09-wc-grep-c", "p70", "wc -l owner probe without content (UNRESOLVED floor)"),
    ("F10-path-naming-ls-echo", "p70", "echo owner path without opening (exact, 0 owner opens)"),
    ("F11-same-response-r2", "p70", "owner load in same assistant response as R2 text (UNRESOLVED)"),
    ("F12-keyword-grep-minor", "p70", "single long owner line >=256 bytes (minor exposure, UNRESOLVED)"),
    ("F13-pairing-mismatch", "p70", "request-position pairing mismatch (route iii denied)"),
    ("F14-error-status-cat-false", "p70", "cat <owner>; false (error status owner-class supply FAIL)"),
    ("F15-above-quantum-keyword-grep", "p70", "grep -rn 'authority' package-wide multi-line (pre-R2 FAIL)"),
    ("F16-request-retry", "p70", "HTTP 500 retry sharing original position"),
    ("F17-multi-turn-rescan", "p70", "multi-turn session with package rescan"),
    ("F18-timing-stress", "p70", "timing loss / tight bracket bound"),
    ("F-p66-01-native-read", "p66", "p66 comparator native read of root SKILL.md"),
    ("F-p66-02-cd-cat-twin", "p66", "p66 comparator cd && cat twin reference"),
    ("F-p66-03-package-scan", "p66", "p66 comparator grep -rl package scan (212 files opened)"),
    ("F-p65-01-native-read", "p65", "p65 comparator native read of root SKILL.md"),
    ("F-p65-02-cd-cat-twin", "p65", "p65 comparator cd && cat twin reference"),
    ("F-p65-03-package-scan", "p65", "p65 comparator grep -rl package scan (198 files opened)"),
]


def run_case(case_id: str, arm_name: str, desc: str) -> dict[str, Any]:
    t0 = time.time()
    arm = get_arm_config(arm_name)
    scenario, claims, parameters, meta = build_scenario(case_id, arm_name)
    
    root_name = "software-implementation"
    rig = omp_rig.Rig(Path("/tmp"), entry="pinned:" + root_name, timeout_s=45, claims=claims)
    rig.arm = arm
    omp_rig.write_json(rig.arms_manifest, {"schema": 1, "arms": [rig.arm]})
    rig.arms_manifest_sha = core70.sha256_file(rig.arms_manifest)
    
    orig_profile = rig.profile
    def profile(upstream, **kwargs):
        p = orig_profile(upstream, **kwargs)
        p.update(runtime_mode="rpc", activation_mechanism="runtime-command",
                 delivery_transform=observer70.OMP_RPC_TRANSFORM,
                 runtime_input_template=omp.input_template("runtime-command"))
        if parameters is not None:
            p["package_access_parameters"] = {**package_ledger.PARAMETERS, **parameters}
        return p
    rig.profile = profile

    summary = rig.run(scenario)

    out = Path(summary["_out"])
    events = omp_rig.load_events(out)
    observation = summary.get("resource_observation") or {}
    accounting = observation.get("accounting") or {}
    
    # Bracket width stats
    bracket_widths_ns = []
    events_ledger = accounting.get("events") or []
    for ev in events_ledger:
        b = ev.get("bracket") or {}
        if "lower_ns" in b and "upper_ns" in b:
            bracket_widths_ns.append(b["upper_ns"] - b["lower_ns"])

    # Owner floor adjudication
    r2_seq = None
    consequent_seq = None
    if "r2_keyword" in meta:
        for e in events:
            if e.get("kind") == "assistant_message":
                text = json.dumps(e.get("payload", {}))
                if meta["r2_keyword"] in text:
                    r2_seq = e.get("sequence")
                if meta.get("consequent_keyword") and meta["consequent_keyword"] in text:
                    consequent_seq = e.get("sequence")

    # Mutate pairing if requested
    if meta.get("mutate_pairing"):
        # simulate unverified pairing
        req_records = accounting.get("request_records") or []
        for r in req_records:
            r["pairing_verified"] = False
            r["position"] = None
        accounting = package_ledger.account(
            accounting.get("ledger"), req_records, events, out / "installed-package",
            owner_name=harness70.OWNER, parameters=accounting.get("parameters") or package_ledger.PARAMETERS
        )

    owner_floor_state = core70.owner_floor_state(
        accounting, r2_seq, r2_adjudicated=True
    )
    owner_load_hit = False
    if r2_seq is not None:
        hits = [row for row in accounting.get("owner_read_observed", []) if row["sequence"] > r2_seq]
        if consequent_seq is not None:
            hits = [row for row in hits if row["sequence"] <= consequent_seq]
        owner_load_hit = bool(hits)

    # Verdict derivation
    # Question A (Byte question): exact = True -> PASS-eligible; exact = False -> UNRESOLVED / INADMISSIBLE
    byte_exact = bool(observation.get("exact"))
    byte_verdict = "PASS-eligible" if byte_exact else "UNRESOLVED"
    
    # Question B (Owner floor): FAIL / UNRESOLVED / PASS
    floor_exact = bool(observation.get("owner_floor_exact"))
    if owner_floor_state == "FAIL":
        floor_verdict = "definite FAIL"
    elif owner_load_hit:
        floor_verdict = "owner-load hit"
    elif owner_floor_state == "PASS":
        floor_verdict = "PASS-eligible"
    else:
        floor_verdict = "UNRESOLVED"

    elapsed = time.time() - t0
    result = {
        "case_id": case_id,
        "arm": arm_name,
        "description": desc,
        "elapsed_s": round(elapsed, 2),
        "evidence_state": summary.get("evidence_state"),
        "byte_question": {
            "exact": byte_exact,
            "active_bytes": summary.get("active_ssdp_bytes"),
            "verdict": byte_verdict,
            "unexplained": accounting.get("unexplained_files", []),
            "route_iii_available": accounting.get("route_iii_available", True),
        },
        "owner_floor": {
            "owner_floor_exact": floor_exact,
            "state": owner_floor_state,
            "verdict": floor_verdict,
            "owner_load_hit": owner_load_hit,
            "owner_opens_count": len(accounting.get("owner_open_windows", [])),
            "owner_read_observed_count": len(accounting.get("owner_read_observed", [])),
            "owner_minor_exposure_count": len(accounting.get("owner_minor_exposure", [])),
        },
        "bracket_widths_ns": {
            "count": len(bracket_widths_ns),
            "min_ns": min(bracket_widths_ns) if bracket_widths_ns else None,
            "max_ns": max(bracket_widths_ns) if bracket_widths_ns else None,
            "median_ns": sorted(bracket_widths_ns)[len(bracket_widths_ns)//2] if bracket_widths_ns else None,
        }
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="Run a specific case ID")
    parser.add_argument("--out", type=Path, default=Path("qualification/ssdp70/rehearsal-matrix-results.json"))
    parser.add_argument("--jobs", type=int, default=4, help="Number of concurrent worker processes")
    args = parser.parse_args()

    if args.case:
        cases = [c for c in ALL_CASES if c[0] == args.case]
        if not cases:
            print(f"Error: case {args.case} not found", file=sys.stderr)
            return 1
        res = run_case(*cases[0])
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(res, indent=2) + "\n")
        print(json.dumps(res, indent=2))
        return 0

    if args.jobs > 1:
        tmp_dir = Path(tempfile.mkdtemp(prefix="rehearsal_jobs_"))
        print(f"Running {len(ALL_CASES)} cases in parallel with {args.jobs} workers (scratch: {tmp_dir})...")
        
        def run_worker(case_entry):
            cid, arm, desc = case_entry
            case_out = tmp_dir / f"{cid}.json"
            scratch_home = Path(tempfile.mkdtemp(prefix="rh."))
            stagef = scratch_home / "ssdp70-omp-stagef"
            stagef.mkdir(parents=True, exist_ok=True)
            closures = Path.home() / "ssdp70-omp-stagef" / "runtime-closures"
            if closures.exists():
                os.symlink(closures, stagef / "runtime-closures")
            
            env = dict(os.environ)
            env["HOME"] = str(scratch_home)
            env["PYTHONPATH"] = str(HERE)
            env["SSDP70_OMP_EXE"] = str(omp_rig.OMP_EXE)
            
            cmd = [sys.executable, str(Path(__file__).resolve()), "--case", cid, "--out", str(case_out)]
            try:
                proc = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
                if case_out.is_file():
                    return json.loads(case_out.read_text())
                else:
                    return {"case_id": cid, "arm": arm, "error": f"missing output file: {proc.stderr}"}
            except subprocess.CalledProcessError as e:
                return {"case_id": cid, "arm": arm, "error": f"process failed: {e.stderr}"}
            finally:
                shutil.rmtree(scratch_home, ignore_errors=True)

        from concurrent.futures import ThreadPoolExecutor, as_completed
        results = []
        with ThreadPoolExecutor(max_workers=args.jobs) as ex:
            futures = {ex.submit(run_worker, c): c[0] for c in ALL_CASES}
            for fut in as_completed(futures):
                cid = futures[fut]
                try:
                    res = fut.result()
                    results.append(res)
                    b_verd = res.get("byte_question", {}).get("verdict", res.get("error", "ERROR"))
                    f_verd = res.get("owner_floor", {}).get("verdict", "")
                    print(f"  [DONE] {cid}: byte={b_verd}, floor={f_verd} ({res.get('elapsed_s', '?')}s)", flush=True)
                except Exception as ex_err:
                    print(f"  [FAIL] {cid}: {ex_err}", flush=True)
                    results.append({"case_id": cid, "error": str(ex_err)})

        shutil.rmtree(tmp_dir, ignore_errors=True)
        order = {c[0]: i for i, c in enumerate(ALL_CASES)}
        results.sort(key=lambda r: order.get(r.get("case_id"), 999))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(results, indent=2) + "\n")
        print(f"\nAll {len(results)} results aggregated to {args.out}")
        return 0

    print(f"Running all {len(ALL_CASES)} rehearsal cases sequentially...")
    results = []
    for case_id, arm, desc in ALL_CASES:
        print(f"--> Running {case_id} ({arm}): {desc}...", flush=True)
        res = run_case(case_id, arm, desc)
        print(f"    Done in {res['elapsed_s']}s: byte={res['byte_question']['verdict']}, floor={res['owner_floor']['verdict']}")
        results.append(res)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nAll results saved to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
