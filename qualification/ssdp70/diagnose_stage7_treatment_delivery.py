#!/usr/bin/env python3
"""Stage 7 diagnostic: was the protocol arm actually delivered to each run?

Read-only over a frozen Stage 7 campaign. For each run it records whether the
executor selected an SSDP root (``root_selection`` event), whether it called a
delegate, and the assessed outcome and dispositions. It then reports outcomes
and M07 (delegate-request conformity) dispositions by treatment delivery.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def scan_run(run_dir: Path) -> dict:
    root = None
    delegate_requests = []
    for line in (run_dir / "events.normalized.jsonl").open(encoding="utf-8"):
        event = json.loads(line)
        kind = event.get("kind")
        payload = event.get("payload", {})
        if kind == "root_selection" and root is None:
            root = payload.get("consumed_resource", {}).get("logical_root")
        elif kind == "delegate_call":
            delegate_requests.append(payload.get("request", {}).get("instruction"))
    return {"root": root, "delegate_requests": delegate_requests}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--runs", default="semantic-runs/20261004T050108Z")
    parser.add_argument("--assessments", default="semantic-assessments/20261004T093500Z")
    args = parser.parse_args()

    runs_dir = args.campaign / args.runs
    summary = json.loads((args.campaign / args.assessments / "assessment-summary.json").read_text())
    by_episode = summary["by_episode"]

    runs = {}
    for run_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        episode, arm, _ = run_dir.name.split("-")
        assessed = by_episode.get(episode, {}).get(arm, {})
        info = scan_run(run_dir)
        info.update(
            outcome=assessed.get("outcome"),
            dispositions=assessed.get("dispositions", []),
        )
        runs[(episode, arm)] = info

    report: dict = {"runs_dir": str(runs_dir)}
    for arm in ("p66", "p70"):
        arm_runs = {e: r for (e, a), r in runs.items() if a == arm}
        outcomes = collections.Counter(
            ("root" if r["root"] else "no-root", r["outcome"]) for r in arm_runs.values()
        )
        m07 = collections.Counter(
            ("root" if r["root"] else "no-root", d["result"])
            for r in arm_runs.values()
            for d in r["dispositions"]
            if d["measure"] == "M07"
        )
        critical_fail = collections.Counter(
            "root" if r["root"] else "no-root"
            for r in arm_runs.values()
            for d in r["dispositions"]
            if d["critical"] and d["result"] == "fail"
        )
        report[arm] = {
            "runs": len(arm_runs),
            "root_selected_runs": sum(1 for r in arm_runs.values() if r["root"]),
            "root_selected_episodes": sorted(e for e, r in arm_runs.items() if r["root"]),
            "roots": dict(collections.Counter(r["root"] for r in arm_runs.values() if r["root"])),
            "runs_with_delegate_call": sum(1 for r in arm_runs.values() if r["delegate_requests"]),
            "outcome_by_delivery": {f"{k[0]}/{k[1]}": v for k, v in sorted(outcomes.items(), key=str)},
            "m07_by_delivery": {f"{k[0]}/{k[1]}": v for k, v in sorted(m07.items())},
            "critical_fail_by_delivery": dict(critical_fail),
            "root_selected_non_pass": sorted(
                e for e, r in arm_runs.items() if r["root"] and r["outcome"] != "PASS"
            ),
        }

    m07_episodes = sorted(
        {e for (e, _), r in runs.items() for d in r["dispositions"] if d["measure"] == "M07"}
    )
    report["m07_episodes"] = {
        e: {
            arm: {
                "root": runs[(e, arm)]["root"],
                "m07": [d["result"] for d in runs[(e, arm)]["dispositions"] if d["measure"] == "M07"],
                "delegate_requests": runs[(e, arm)]["delegate_requests"],
            }
            for arm in ("p66", "p70")
        }
        for e in m07_episodes
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
