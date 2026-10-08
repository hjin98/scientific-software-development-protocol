#!/usr/bin/env python3
"""P9 driver: run the blinded evaluator (`eval/assess70.py`) over completed campaign runs, and collect its dispositions.

  campaign_assess.py run WORK --keys-root KEYS --evaluator-profile P --evaluator-capabilities C [--shared-rubric R] [--parallel N]
      Every run directory under WORK/runs/* whose summary is COMPLETE_ADMISSIBLE and whose arm is p72, p66 or p66b and that has no
      assessment.json yet. Needs SSDP70_OMP_PROVIDER_CREDENTIAL. Exits non-zero on the first evaluator failure that is not a
      per-run result (exit codes 0, 1 and 2 of assess70 are results: PASS, FAIL, UNRESOLVED/not evaluated).
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


def run_dirs(work: Path):
    for d in sorted((work / "runs").glob("*/*-r*")):
        if (d / "summary.json").exists() and d.name.rsplit("-", 2)[1] in GATED_ARMS:
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
    todo = [d for d in run_dirs(a.work)
            if json.loads((d / "summary.json").read_text())["evidence_state"] == "COMPLETE_ADMISSIBLE" and not (d / "assessment.json").exists()]
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
    for d in run_dirs(a.work):
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
    c.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_collect(a)


if __name__ == "__main__":
    raise SystemExit(main())
