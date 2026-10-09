#!/usr/bin/env python3
"""P9 driver: run the blinded evaluator (`eval/assess70.py`) over completed campaign runs, and collect its dispositions.

  campaign_assess.py run WORK --keys-root KEYS --evaluator-profile P --evaluator-capabilities C [--shared-rubric R] [--parallel N]
      Every run directory under WORK/runs/<panel>-cNN whose panel is in --panels (default main, versioning, sentinels, sentinels-add: routing, unversioned and burden items are binding or recorded bytes) and whose summary is COMPLETE_ADMISSIBLE and whose arm is p72, p66 or p66b and that has no
      assessment.json yet. Needs SSDP70_OMP_PROVIDER_CREDENTIAL. Exits non-zero on the first evaluator failure that is not a
      per-run result (exit codes 0, 1 and 2 of assess70 are results: PASS, FAIL, UNRESOLVED/not evaluated).
  campaign_assess.py cost WORK --price-in P --price-cached P --price-out P     (measured tokens, hit rate, USD per run, projection)
  campaign_assess.py collect WORK --out DISPOSITIONS.json
      Reads every VALID assessment.json into {"<run>::<item>": "pass"|"fail"|...} for `build_campaign_record.py --dispositions`,
      and lists runs whose assessment is missing or not VALID. It never edits a run directory.
The evaluator model must differ from the executor (assess70 refuses otherwise). Rerunning an assessment is the analyst's decision.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSESS = HERE.parents[0] / "eval" / "assess70.py"
GATED_ARMS = ("p72", "p66", "p66b")
# Panels whose items need a model judgement. Routing, unversioned and burden items are scored by binding oracles or recorded bytes.
DEFAULT_PANELS = ("main", "versioning", "sentinels", "sentinels-add")


def in_panels(d: Path, panels) -> bool:
    key = d.parent.name                              # command key: <panel>-cNN
    return any(key.startswith(p + "-c") and key[len(p) + 2:].isdigit() for p in panels)


def run_dirs(work: Path, panels=DEFAULT_PANELS):
    for d in sorted((work / "runs").glob("*/*-r*")):
        if (d / "summary.json").exists() and d.name.rsplit("-", 2)[1] in GATED_ARMS and in_panels(d, panels):
            yield d


def one(d: Path, a) -> tuple[str, int]:
    episode = json.loads((d / "summary.json").read_text())["episode"]
    cmd = [sys.executable, str(ASSESS), "--run", str(d), "--keys", str(a.keys_root / episode),
           "--evaluator-profile", str(a.evaluator_profile), "--evaluator-capabilities", str(a.evaluator_capabilities)]
    if a.shared_rubric:
        cmd += ["--shared-rubric", str(a.shared_rubric)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    (d / "assessment.stderr.txt").write_text(p.stderr)
    return d.name, p.returncode


def cmd_run(a) -> int:
    if not os.environ.get("SSDP70_OMP_PROVIDER_CREDENTIAL"):
        print("SSDP70_OMP_PROVIDER_CREDENTIAL is not set", file=sys.stderr)
        return 2
    if not a.limit and not (a.work / "authorizations" / "evaluator-full.ok").exists():
        print("the full evaluator pass is not authorized: run the pilot (--limit) and wait for authorizations/evaluator-full.ok", file=sys.stderr)
        return 2
    todo = [d for d in run_dirs(a.work, a.panels)
            if json.loads((d / "summary.json").read_text())["evidence_state"] == "COMPLETE_ADMISSIBLE" and not (d / "assessment.json").exists()]
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(todo)} runs to assess")
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for name, rc in pool.map(lambda d: one(d, a), todo):
            print(f"{name}: assess70 exit {rc}")
            if rc not in (0, 1, 2):
                bad += 1
    return 3 if bad else 0


def cmd_collect(a) -> int:
    out, problems, n = {}, [], 0
    for d in run_dirs(a.work, a.panels):
        if json.loads((d / "summary.json").read_text())["evidence_state"] != "COMPLETE_ADMISSIBLE":
            continue
        n += 1
        path = d / "assessment.json"
        if not path.exists():
            problems.append({"run": d.name, "what": "no assessment"})
            continue
        data = json.loads(path.read_text())
        if data.get("assessment_status") != "VALID":
            problems.append({"run": d.name, "what": f"assessment {data.get('assessment_status')}"})
            continue
        for row in data["dispositions"]:
            out[f"{d.name}::{row['item'].split('::', 1)[-1]}"] = row["result"]
    a.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"admissible_runs": n, "dispositions": len(out), "problems": problems}, indent=1))
    return 0 if not problems else 4


def trace_usage(path: Path) -> dict:
    tot = {"input": 0, "cacheRead": 0, "output": 0, "turns": 0}
    for line in path.read_text().splitlines():
        if '"message_end"' not in line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        m = o.get("message", {})
        if o.get("type") == "message_end" and m.get("role") == "assistant" and isinstance(m.get("usage"), dict):
            tot["turns"] += 1
            for k in ("input", "cacheRead", "output"):
                tot[k] += int(m["usage"].get(k, 0))
    return tot


def cmd_cost(a) -> int:
    """Measured evaluator tokens and dollars (from assessment-trace.jsonl) and the projection to every evaluable run."""
    done = [d for d in run_dirs(a.work, a.panels) if (d / "assessment-trace.jsonl").exists()]
    if not done:
        print("no assessed runs yet")
        return 2
    rows = [trace_usage(d / "assessment-trace.jsonl") for d in done]
    total = {k: sum(r[k] for r in rows) for k in rows[0]}

    def dollars(r):
        return (r["input"] * a.price_in + r["cacheRead"] * a.price_cached + r["output"] * a.price_out) / 1e6

    per = dollars(total) / len(rows)
    gated = sum(c["runs"] for c in json.loads((a.work / "commands.json").read_text())["commands"]
                if c["panel"] in a.panels and not c.get("conditional"))
    hit = total["cacheRead"] / max(1, total["cacheRead"] + total["input"])
    out = {"assessed_runs": len(rows), "mean_turns": round(total["turns"] / len(rows), 1),
           "mean_tokens": {k: round(total[k] / len(rows)) for k in ("input", "cacheRead", "output")},
           "cache_hit_rate": round(hit, 3), "mean_usd_per_run": round(per, 4), "planned_evaluable_runs": gated,
           "projected_usd": round(per * gated, 2)}
    print(json.dumps(out, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    c = sub.add_parser("collect")
    for sp in (r, c):
        sp.add_argument("work", type=Path)
    r.add_argument("--keys-root", type=Path, required=True)
    r.add_argument("--evaluator-profile", type=Path, required=True)
    r.add_argument("--evaluator-capabilities", type=Path, required=True)
    r.add_argument("--shared-rubric", type=Path)
    r.add_argument("--parallel", type=int, default=4)
    r.add_argument("--limit", type=int, help="assess only the first N runs (the pilot)")
    c.add_argument("--out", type=Path, required=True)
    k = sub.add_parser("cost")
    k.add_argument("work", type=Path)
    k.add_argument("--price-in", type=float, required=True, help="USD per million uncached input tokens")
    k.add_argument("--price-cached", type=float, required=True)
    k.add_argument("--price-out", type=float, required=True)
    for sp in (r, c, k):
        sp.add_argument("--panels", nargs="+", default=list(DEFAULT_PANELS))
    a = ap.parse_args()
    return {"run": cmd_run, "collect": cmd_collect, "cost": cmd_cost}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
