#!/usr/bin/env python3
"""Reproduce the headline figures of PROTOCOL-7.1-DEVELOPMENT-MATRIX-2026-10-06-RECORD.md.

Read-only over the retained run artifacts (run-identity, summary, normalized events, trace usage,
assessment.json and oracle stdout). Opens no custodian key, authoring or per-episode oracle source.
Usage: diagnose_dev_matrix_20261006.py [--runs DIR] [--clean-manifest runs_clean_admissible.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import statistics
from pathlib import Path

DEFAULT_RUNS = Path.home() / "ssdp70-omp-stagef/probes/PROTOCOL-7.1-CAMPAIGN-CONSOLIDATED/runs"
DEFAULT_CLEAN = Path.home() / ".gemini/antigravity-cli/brain/ea4087b5-6052-4328-bd26-334cf2752b37/scratch/runs_clean_admissible.json"


def run_row(d: Path) -> dict:
    ident = json.loads((d / "run-identity.json").read_text())
    summ = json.loads((d / "summary.json").read_text())
    roots, term = [], {}
    for line in (d / "events.normalized.jsonl").read_text().splitlines():
        e = json.loads(line)
        if e["kind"] == "root_selection":
            roots.append(e["payload"].get("logical_root"))
        elif e["kind"] == "termination":
            term = e["payload"]
    turns = tokens = 0
    for line in (d / "trace.jsonl").read_text().splitlines():
        if line.startswith('{"type":"turn_start"'):
            turns += 1
        elif line.startswith('{"type":"message_end"'):
            msg = json.loads(line)["message"]
            if msg.get("role") == "assistant":
                tokens += (msg.get("usage") or {}).get("totalTokens", 0)
    ep, arm, _ = d.name.rsplit("-", 2)
    oracle = {}
    for f in (d / "oracle-output").glob("*.stdout.txt"):
        oracle = json.loads(f.read_text()).get("items", {})
    disp = json.loads((d / "assessment.json").read_text()).get("dispositions", []) if (d / "assessment.json").is_file() else []
    return {"ep": ep, "arm": arm, "purpose": ident["accounting"]["purpose"], "mode": ident["execution_mode"],
            "stratum": ident["entry_stratum"], "state": summ["evidence_state"], "term": term.get("state"),
            "roots": roots, "turns": turns, "tokens": tokens, "disp": disp, "oracle": oracle}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, default=DEFAULT_RUNS)
    ap.add_argument("--clean-manifest", type=Path, default=DEFAULT_CLEAN)
    a = ap.parse_args()
    rows = {d.name: run_row(d) for d in sorted(a.runs.iterdir()) if d.is_dir()}
    C = collections.Counter
    out = {"runs": len(rows),
           "purpose_mode_stratum": C(f"{r['purpose']}/{r['mode']}/{r['stratum']}" for r in rows.values()),
           "evidence_by_termination": C(f"{r['state']}/{r['term']}" for r in rows.values()),
           "selected_by_arm": {arm: sum(1 for r in rows.values() if r["arm"] == arm and r["roots"]) for arm in ("p66", "p70", "p71")},
           "error_rate_p71_selected_vs_not": [
               sum(1 for r in rows.values() if r["arm"] == "p71" and r["roots"] and r["state"] != "COMPLETE_ADMISSIBLE"),
               sum(1 for r in rows.values() if r["arm"] == "p71" and r["roots"]),
               sum(1 for r in rows.values() if r["arm"] == "p71" and not r["roots"] and r["state"] != "COMPLETE_ADMISSIBLE"),
               sum(1 for r in rows.values() if r["arm"] == "p71" and not r["roots"])],
           "completed_turns_median": statistics.median(r["turns"] for r in rows.values() if r["state"] == "COMPLETE_ADMISSIBLE")}
    clean = sorted({r["episode"] for r in json.loads(a.clean_manifest.read_text())["runs"]})
    for arm in ("p71", "p66"):
        fails = C()
        unres = 0
        for ep in clean:
            r = rows[f"{ep}-{arm}-r0"]
            for x in r["disp"]:
                if x.get("critical") and x["result"] == "fail":
                    mode = (r["oracle"].get(x["item"]) or {}).get("mode")
                    fails[f"{'selected' if r['roots'] else 'unselected'}/{mode}"] += 1
                unres += bool(x.get("critical") and x["result"] == "unresolved")
        out[f"{arm}_clean_critical_fail"] = {"total": sum(fails.values()), **fails}
        out[f"{arm}_clean_critical_unresolved"] = unres
    both = [ep for ep in clean if rows[f"{ep}-p71-r0"]["roots"] and rows[f"{ep}-p66-r0"]["roots"]]
    for arm in ("p71", "p66"):
        crit = [x["result"] for ep in both for x in rows[f"{ep}-{arm}-r0"]["disp"] if x.get("critical") and x["result"] in ("pass", "fail")]
        tens = [x["result"] for ep in both for x in rows[f"{ep}-{arm}-r0"]["disp"] if x.get("measure") == "tension_report" and x["result"] in ("pass", "fail")]
        out[f"{arm}_both_selected"] = {"episodes": len(both), "critical_pass": f"{crit.count('pass')}/{len(crit)}",
                                       "tension_pass": f"{tens.count('pass')}/{len(tens)}"}
    print(json.dumps(out, indent=1, default=dict))


if __name__ == "__main__":
    main()
