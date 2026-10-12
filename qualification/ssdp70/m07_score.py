#!/usr/bin/env python3
"""M07 delegate-request conformity scorer for CD-7 Pre-Campaign Development Gate.

Authority:
- Governing Protocol: SSDP 6.6.0
- Target Protocol: 7.1.0 (stakeholder OD-1)
- D3 Design CD-7 (§4, §7, §9 R3) and Stakeholder Decision OD-5
- Contract Revision 16 Delta A3 (timing rule: launching instruction or pre-return message only;
  post-return follow-ups counted separately and do not satisfy request parts)
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

OWED_PARTS = {
    "C042": ["F", "N", "V", "T"],
    "C044": ["F", "N", "V", "T"],
    "C046": ["F", "N", "V", "T"],
    "C048": ["F", "N", "V"],
    "C050": ["F", "N", "V"],
    "C052": ["F", "N", "V"],
    "C055": ["F", "N", "V", "T"],
}

LAUNCHED_WORK_PATTERNS = [
    re.compile(r"including (any|from any) tools or agents you launched", re.I),
    re.compile(r"tools or agents you launched", re.I),
    re.compile(r"tools/agents you launched", re.I),
    re.compile(r"tools or agents launched", re.I),
]

def has_launched_qualifier(text: str) -> bool:
    return any(p.search(text) for p in LAUNCHED_WORK_PATTERNS)

def score_instruction(instruction: str, is_launching: bool) -> dict[str, Any]:
    """Score one delegate instruction against the §11.3 Request rule."""
    res = {}
    lower = instruction.lower()
    
    # 1. Findings (F)
    # Core: answerable either way (findings or state none / findings or none)
    # "report your findings" alone fails
    f_either_way = (
        ("findings" in lower or "finding" in lower) and
        ("state that you have none" in lower or "or state none" in lower or "or none" in lower or "if none" in lower)
    )
    if f_either_way:
        f_strict = has_launched_qualifier(instruction)
        res["F"] = {"core": True, "strict": f_strict, "timing": "launching" if is_launching else "followup"}
    
    # 2. Realized results (N)
    # Core: produce/run/review realized results or gate evidence; null envelope if so
    n_asked = (
        ("realized" in lower or "results" in lower or "gate evidence" in lower) and
        ("null envelope" in lower or "what you examined and what material areas you did not" in lower or "examined" in lower)
    )
    if n_asked:
        n_strict = has_launched_qualifier(instruction)
        res["N"] = {"core": True, "strict": n_strict, "timing": "launching" if is_launching else "followup"}
        
    # 3. Variants (V)
    # Core: evaluated >1 variant, including changes after seeing results; variant disclosure
    v_asked = (
        ("variant" in lower or "variants" in lower) and
        ("more than one" in lower or ">1" in lower or "multiple" in lower or "disclosure" in lower)
    )
    if v_asked:
        v_after_results = ("after seeing results" in lower or "result-informed" in lower or "even bug fixes" in lower)
        v_strict = has_launched_qualifier(instruction) and v_after_results
        res["V"] = {"core": True, "strict": v_strict, "timing": "launching" if is_launching else "followup"}

    # 4. Tensions (T)
    # Core: search for recorded tensions against authority, unreachable, found records with entries, binding, asserter
    t_asked = (
        "tension" in lower or "tensions" in lower or
        ("searched" in lower and ("unreachable" in lower or "could not reach" in lower))
    )
    if t_asked:
        t_records = ("binding" in lower and "asserter" in lower) or "entries" in lower or "found (or none)" in lower
        t_strict = has_launched_qualifier(instruction) and t_records
        res["T"] = {"core": True, "strict": t_strict, "timing": "launching" if is_launching else "followup"}

    return res

def analyze_run(run_dir: Path) -> dict[str, Any]:
    summary_path = run_dir / "summary.json"
    events_path = run_dir / "events.normalized.jsonl"
    if not summary_path.is_file():
        return {"status": "INCOMPLETE"}
        
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    evidence_state = summary.get("evidence_state", "UNKNOWN")
    
    root = None
    calls = []
    if events_path.is_file():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            ev = json.loads(line)
            if ev.get("kind") == "root_selection" and root is None:
                root = ev.get("payload", {}).get("consumed_resource", {}).get("logical_root")
            if ev.get("kind") == "delegate_call":
                calls.append(ev.get("payload", {}).get("request", {}).get("instruction", ""))

    ep_id = run_dir.name.split("-")[0]
    arm_name = run_dir.name.split("-")[1]
    rep = run_dir.name.split("-")[2]
    
    owed = OWED_PARTS.get(ep_id, [])
    
    # Timing analysis: Call 0 is launching request.
    # Later calls are follow-ups.
    launching_scores = {}
    followup_scores = {}
    
    for i, call_text in enumerate(calls):
        is_launch = (i == 0)
        c_score = score_instruction(call_text, is_launch)
        for part, sc in c_score.items():
            if is_launch:
                if part not in launching_scores:
                    launching_scores[part] = sc
            else:
                if part not in followup_scores:
                    followup_scores[part] = sc
                    
    # Combine according to Delta A3:
    # Only launching (or pre-return) counts for the request duty.
    # Follow-ups only count separately and do NOT satisfy request parts under Rev 16 A3.
    scored_parts = {}
    for part in owed:
        if part in launching_scores:
            scored_parts[part] = launching_scores[part]
        elif part in followup_scores:
            scored_parts[part] = {**followup_scores[part], "followup_only": True}
        else:
            scored_parts[part] = {"absent": True}
            
    # Unowed parts asked (burden)
    unowed_asked = []
    for part in ["F", "N", "V", "T"]:
        if part not in owed and part in launching_scores:
            unowed_asked.append(part)

    return {
        "run": run_dir.name,
        "episode": ep_id,
        "arm": arm_name,
        "rep": rep,
        "evidence_state": evidence_state,
        "root": root,
        "calls_count": len(calls),
        "owed": owed,
        "scored_parts": scored_parts,
        "unowed_asked": unowed_asked,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs_dir", type=Path)
    args = parser.parse_args()
    
    runs = sorted([p for p in args.runs_dir.iterdir() if p.is_dir() and (p / "summary.json").is_file()])
    print(f"Loaded {len(runs)} completed runs from {args.runs_dir}")
    
    by_arm = {}
    for r in runs:
        res = analyze_run(r)
        arm = res["arm"]
        by_arm.setdefault(arm, []).append(res)
        
    for arm, arm_runs in sorted(by_arm.items()):
        total_owed = 0
        core_launching = 0
        strict_launching = 0
        followup_only = 0
        full_core_episodes = 0
        full_strict_episodes = 0
        unowed_count = 0
        
        for run_res in arm_runs:
            owed = run_res["owed"]
            total_owed += len(owed)
            
            run_core = 0
            run_strict = 0
            for part in owed:
                sc = run_res["scored_parts"].get(part, {})
                if sc.get("core") and not sc.get("followup_only"):
                    core_launching += 1
                    run_core += 1
                    if sc.get("strict"):
                        strict_launching += 1
                        run_strict += 1
                elif sc.get("followup_only"):
                    followup_only += 1
                    
            if run_core == len(owed):
                full_core_episodes += 1
            if run_strict == len(owed):
                full_strict_episodes += 1
                
            unowed_count += len(run_res["unowed_asked"])
            
        rate_core = core_launching / total_owed if total_owed else 0
        rate_strict = strict_launching / total_owed if total_owed else 0
        
        print("\n" + "=" * 60)
        print(f"ARM: {arm} (N={len(arm_runs)} runs, {total_owed} owed parts)")
        print("=" * 60)
        print(f"  Core uptake (launching instruction): {core_launching}/{total_owed} ({rate_core:.1%})")
        print(f"  Strict conformity (launching instruction): {strict_launching}/{total_owed} ({rate_strict:.1%})")
        print(f"  Follow-up-only parts (counted separately per A3): {followup_only}")
        print(f"  Fully conformant episodes (core): {full_core_episodes}/{len(arm_runs)} ({full_core_episodes/len(arm_runs):.1%})")
        print(f"  Fully conformant episodes (strict): {full_strict_episodes}/{len(arm_runs)} ({full_strict_episodes/len(arm_runs):.1%})")
        print(f"  Unowed request parts asked (burden): {unowed_count} (bound: <= 1 per 12 eligible = {total_owed/12:.1f})")
        if arm == "p71":
            passed_floor = (core_launching >= 0.8 * total_owed)
            print(f"  OD-5 Floor Check (>= 80% target): {'PASS' if passed_floor else 'FAIL'} ({core_launching}/{total_owed} vs target {int(0.8*total_owed)})")

if __name__ == "__main__":
    main()
